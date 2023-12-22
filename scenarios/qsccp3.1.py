import os
import time
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
    info(
        f"Setting up route from {node1} to {node2} with interface {interface.IP()} => {prefix}\n"
    )
    Nfdc.registerRoute(host1, prefix, interface.IP(), cost=0)


def run():
    Minindn.cleanUp()
    Minindn.verifyDependencies()

    ndn = Minindn(
        topoFile=os.path.join(
            os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
            "topologies",
            "qsccp3.1.conf",
        )
    )
    ndn.start()

    # configure and start nfd on each node
    info("Configuring NFD\n")
    AppManager(ndn, ndn.net.hosts, Nfd, logLevel="INFO")

    for link in ndn.topo.links(withInfo=True):
        node1, node2, node_info = link
        host1 = ndn.net[node1]
        host2 = ndn.net[node2]
        interface = host2.connectionsTo(host1)[0][0]
        interface_ip = interface.IP()
        bandwidth = interface.params.get("bw", 100) * 1000000
        info(f"Setting up route from {node1} to {node2} with bandwidth {bandwidth}\n")
        Nfdc.createFace(host1, interface_ip, bandwidth=bandwidth)

    addRoute(ndn, "c1", "r1", "/A")
    addRoute(ndn, "c2", "r1", "/B")
    addRoute(ndn, "c3", "r1", "/C")

    addRoute(ndn, "r1", "r2", "/A")
    addRoute(ndn, "r1", "r2", "/B")
    addRoute(ndn, "r1", "r2", "/C")

    addRoute(ndn, "r2", "r3", "/A")
    addRoute(ndn, "r2", "r3", "/B")
    addRoute(ndn, "r2", "r3", "/C")

    addRoute(ndn, "r2", "r4", "/A")
    addRoute(ndn, "r2", "r4", "/B")
    addRoute(ndn, "r2", "r4", "/C")

    addRoute(ndn, "r2", "r5", "/A")
    addRoute(ndn, "r2", "r5", "/B")
    addRoute(ndn, "r2", "r5", "/C")

    addRoute(ndn, "r4", "r3", "/A")
    addRoute(ndn, "r4", "r3", "/B")
    addRoute(ndn, "r4", "r3", "/C")

    addRoute(ndn, "r4", "r5", "/A")
    addRoute(ndn, "r4", "r5", "/B")
    addRoute(ndn, "r4", "r5", "/C")

    addRoute(ndn, "r3", "r6", "/A")
    addRoute(ndn, "r3", "r6", "/B")
    addRoute(ndn, "r3", "r6", "/C")

    addRoute(ndn, "r5", "r6", "/A")
    addRoute(ndn, "r5", "r6", "/B")
    addRoute(ndn, "r5", "r6", "/C")

    addRoute(ndn, "r6", "p1", "/A")
    addRoute(ndn, "r6", "p1", "/B")
    addRoute(ndn, "r6", "p1", "/C")
    addRoute(ndn, "r6", "p2", "/A")
    addRoute(ndn, "r6", "p3", "/B")
    addRoute(ndn, "r6", "p4", "/C")

    Nfdc.setStrategy(ndn.net["r1"], "/A", "QSCCP/%FD%01")
    Nfdc.setStrategy(ndn.net["r1"], "/B", "QSCCP/%FD%01")
    Nfdc.setStrategy(ndn.net["r1"], "/C", "QSCCP/%FD%01")
    
    Nfdc.setStrategy(ndn.net["r2"], "/A", "QSCCP/%FD%01")
    Nfdc.setStrategy(ndn.net["r2"], "/B", "QSCCP/%FD%01")
    Nfdc.setStrategy(ndn.net["r2"], "/C", "QSCCP/%FD%01")
    
    Nfdc.setStrategy(ndn.net["r3"], "/A", "QSCCP/%FD%01")
    Nfdc.setStrategy(ndn.net["r3"], "/B", "QSCCP/%FD%01")
    Nfdc.setStrategy(ndn.net["r3"], "/C", "QSCCP/%FD%01")
    
    Nfdc.setStrategy(ndn.net["r4"], "/A", "QSCCP/%FD%01")
    Nfdc.setStrategy(ndn.net["r4"], "/B", "QSCCP/%FD%01")
    Nfdc.setStrategy(ndn.net["r4"], "/C", "QSCCP/%FD%01")
    
    Nfdc.setStrategy(ndn.net["r5"], "/A", "QSCCP/%FD%01")
    Nfdc.setStrategy(ndn.net["r5"], "/B", "QSCCP/%FD%01")
    Nfdc.setStrategy(ndn.net["r5"], "/C", "QSCCP/%FD%01")
    
    Nfdc.setStrategy(ndn.net["r6"], "/A", "QSCCP/%FD%01")
    Nfdc.setStrategy(ndn.net["r6"], "/B", "QSCCP/%FD%01")
    Nfdc.setStrategy(ndn.net["r6"], "/C", "QSCCP/%FD%01")

    # Start cc server
    info("Starting cc...\n")
    qsccp_server_log = open(f"{ndn.workDir}/p1/qsccp-server.log", "w")
    getPopen(
        ndn.net["p1"],
        "cc-producer --prefix {}".format("/A"),
        stdout=qsccp_server_log,
        stderr=qsccp_server_log,
    )
    getPopen(
        ndn.net["p1"],
        "cc-producer --prefix {}".format("/B"),
        stdout=qsccp_server_log,
        stderr=qsccp_server_log,
    )
    getPopen(
        ndn.net["p1"],
        "cc-producer --prefix {}".format("/C"),
        stdout=qsccp_server_log,
        stderr=qsccp_server_log,
    )
    qsccp_server_log = open(f"{ndn.workDir}/p2/qsccp-server.log", "w")
    getPopen(
        ndn.net["p2"],
        "cc-producer --prefix {}".format("/A"),
        stdout=qsccp_server_log,
        stderr=qsccp_server_log,
    )
    qsccp_server_log = open(f"{ndn.workDir}/p3/qsccp-server.log", "w")
    getPopen(
        ndn.net["p3"],
        "cc-producer --prefix {}".format("/B"),
        stdout=qsccp_server_log,
        stderr=qsccp_server_log,
    )
    qsccp_server_log = open(f"{ndn.workDir}/p4/qsccp-server.log", "w")
    getPopen(
        ndn.net["p4"],
        "cc-producer --prefix {}".format("/C"),
        stdout=qsccp_server_log,
        stderr=qsccp_server_log,
    )

    # start cc client
    qsccp_client_log = open(f"{ndn.workDir}/c1/qsccp-client.log", "w")
    ping1 = getPopen(
        ndn.net["c1"],
        f"qsccp-client --prefix /A --timingStop 320000 --tos 5",
        stdout=qsccp_client_log,
        stderr=qsccp_client_log,
    )
    qsccp_client_log = open(f"{ndn.workDir}/c2/qsccp-client.log", "w")
    getPopen(
        ndn.net["c2"],
        f"qsccp-client --prefix /B --timingStop 320000 --delayStart 80000 --tos 5 --initialSendRate 50000",
        stdout=qsccp_client_log,
        stderr=qsccp_client_log,
    )
    qsccp_client_log = open(f"{ndn.workDir}/c3/qsccp-client.log", "w")
    getPopen(
        ndn.net["c3"],
        f"qsccp-client --prefix /C --timingStop 320000 --delayStart 160000 --delayGreedy 240000 --greedyRate 10000000 --tos 5 --initialSendRate 50000",
        stdout=qsccp_client_log,
        stderr=qsccp_client_log,
    )
    ping1.wait()
    # printOutput(ping1.stdout.read())

    # interface = ndn.net["b"].connectionsTo(ndn.net["a"])[0][0]
    # info("Failing link\n") # failing link by setting link loss to 100%
    # interface.config(delay="10ms", bw=10, loss=100)
    # info ("\n starting ping2 client \n")

    # ping2 = getPopen(ndn.net["a"], "ndnping {} -c 5".format(PREFIX), stdout=PIPE, stderr=PIPE)
    # ping2.wait()
    # printOutput(ping2.stdout.read())

    # interface.config(delay="10ms", bw=10, loss=0) # bringing back the link

    info("\nExperiment Completed!\n")
    MiniNDNCLI(ndn.net)
    ndn.stop()


if __name__ == "__main__":
    setLogLevel("info")
    run()

