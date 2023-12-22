import os
import time
import sys
from subprocess import PIPE

from mininet.log import setLogLevel, info
from mininet.topo import Topo
from mininet.link import TCLink

from minindn.minindn import Minindn
from minindn.apps.app_manager import AppManager
from minindn.util import MiniNDNCLI, getPopen
from minindn.apps.nfd import Nfd
from minindn.helpers.nfdc import Nfdc


def printOutput(output):
    _out = output.decode("utf-8").split("\n")
    for _line in _out:
        info(_line + "\n")


def addRoute(ndn, node1: str, node2: str, prefix: str):
    host1 = ndn.net[node1]
    host2 = ndn.net[node2]
    interface = host2.connectionsTo(host1)[0][0]
    info(f"Setting up route from {node1} to {node2} with interface {interface.IP()} => {prefix}\n")
    Nfdc.registerRoute(host1, prefix, interface.IP(), cost=0)


def run():
    Minindn.cleanUp()
    Minindn.verifyDependencies()

    ndn = Minindn(
        topoFile=os.path.join(
            os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
            "topologies",
            sys.argv[1],
        )
    )
    ndn.start()

    # configure and start nfd on each node
    info("Configuring NFD\n")
    AppManager(ndn, ndn.net.hosts, Nfd, logLevel="INFO", csSize=0)

    for link in ndn.topo.links(withInfo=True):
        node1, node2, node_info = link
        host1 = ndn.net[node1]
        host2 = ndn.net[node2]
        interface = host2.connectionsTo(host1)[0][0]
        interface_ip = interface.IP()
        bandwidth = interface.params.get("bw", 100) * 1000000
        info(f"Setting up route from {node1} to {node2} with bandwidth {bandwidth}\n")
        Nfdc.createFace(host1, interface_ip)
    
    addRoute(ndn, "c1", "r1", "/A")
    addRoute(ndn, "c2", "r1", "/B")
    
    addRoute(ndn, "r1", "r2", "/A")
    addRoute(ndn, "r1", "r2", "/B")
    
    addRoute(ndn, "r2", "p1", "/A")
    addRoute(ndn, "r2", "p2", "/B")

    # Start cc server
    info("Starting cc...\n")
    qsccp_server_log = open(f"{ndn.workDir}/p1/qsccp-server.log", "w")
    getPopen(
        ndn.net["p1"],
        "cc-producer --prefix {}".format("/A"),
        stdout=qsccp_server_log,
        stderr=qsccp_server_log,
    )
    qsccp_server_log = open(f"{ndn.workDir}/p2/qsccp-server.log", "w")
    getPopen(
        ndn.net["p2"],
        "cc-producer --prefix {}".format("/B"),
        stdout=qsccp_server_log,
        stderr=qsccp_server_log,
    )
    
    total_time = 120000

    # start cc client
    qsccp_client_log = open(f"{ndn.workDir}/c2/qsccp-client.log", "w")
    ping1 = getPopen(
        ndn.net["c2"],
        f"pcon-client --prefix /B --timingStop {total_time} --ccAlgorithm BIC",
        stdout=qsccp_client_log,
        stderr=qsccp_client_log,
    )
    qsccp_client_log = open(f"{ndn.workDir}/c1/qsccp-client.log", "w")
    ping1 = getPopen(
        ndn.net["c1"],
        f"pcon-client --prefix /A --timingStop {total_time} --ccAlgorithm BIC",
        stdout=qsccp_client_log,
        stderr=qsccp_client_log,
    )
    ping1.wait()

    info("\nExperiment Completed!\n")
    # MiniNDNCLI(ndn.net)
    ndn.stop()


if __name__ == "__main__":
    setLogLevel("info")
    run()
