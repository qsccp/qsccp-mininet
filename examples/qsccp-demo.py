# -*- Mode:python; c-file-style:"gnu"; indent-tabs-mode:nil -*- */
#
# Copyright (C) 2015-2021, The University of Memphis,
#                          Arizona Board of Regents,
#                          Regents of the University of California.
#
# This file is part of Mini-NDN.
# See AUTHORS.md for a complete list of Mini-NDN authors and contributors.
#
# Mini-NDN is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mini-NDN is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mini-NDN, e.g., in COPYING.md file.
# If not, see <http://www.gnu.org/licenses/>.

from subprocess import PIPE

from mininet.log import setLogLevel, info
from mininet.topo import Topo

from minindn.minindn import Minindn
from minindn.apps.app_manager import AppManager
from minindn.util import MiniNDNCLI, getPopen
from minindn.apps.nfd import Nfd
from minindn.helpers.nfdc import Nfdc

PREFIX = "/A"

def printOutput(output):
    _out = output.decode("utf-8").split("\n")
    for _line in _out:
        info(_line + "\n")

def run():
    Minindn.cleanUp()
    Minindn.verifyDependencies()

    # Topology can be created/modified using Mininet topo object
    topo = Topo()
    info("Setup\n")
    # add hosts
    a = topo.addHost('a')
    b = topo.addHost('b')

    # add links
    topo.addLink(a, b, delay='10ms', bw=10) # bw = bandwidth
    
    info(topo.links(withInfo=True))

    ndn = Minindn(topo=topo)
    ndn.start()

    # configure and start nfd on each node
    info("Configuring NFD\n")
    AppManager(ndn, ndn.net.hosts, Nfd, logLevel="INFO")

    """
    There are multiple ways of setting up routes in Mini-NDN
    refer: https://minindn.memphis.edu/experiment.html#routing-options
    It can also be set manually as follows. The important bit to note here
    is the use of the Nfdc command
    """
    for link in topo.links(withInfo=True):
        node1, node2, node_info = link
        host1 = ndn.net[node1]
        host2 = ndn.net[node2]
        interface = host2.connectionsTo(host1)[0][0]
        interface_ip = interface.IP()
        bandwidth = interface.params.get("bw", 100) * 1000000
        info(f"Setting up route from {node1} to {node2} with bandwidth {bandwidth}\n")
        Nfdc.createFace(host1, interface_ip, bandwidth=bandwidth)
        Nfdc.registerRoute(host1, PREFIX, interface_ip, cost=0)

    # Start cc server
    info("Starting cc...\n")
    qsccp_server_log = open(f"{ndn.workDir}/qsccp-demo/qsccp-server.log", "w")
    getPopen(ndn.net["b"], "cc-producer --prefix {}".format(PREFIX), stdout=qsccp_server_log,\
             stderr=qsccp_server_log)

    # start cc client
    qsccp_client_log = open(f"{ndn.workDir}/qsccp-demo/qsccp-client.log", "w")
    ping1 = getPopen(ndn.net["a"], "qsccp-client --prefix {} --timingStop 10000".format(PREFIX), stdout=qsccp_client_log, stderr=qsccp_client_log)
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

if __name__ == '__main__':
    setLogLevel("info")
    run()