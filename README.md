# QoS-aware Congestion Control Protocol (QSCCP) for ICN

### Pull Code：

   ```bash
   git clone https://github.com/Enidsky/qsccp-mininet.git
   cd qsccp-mininet
   git submodule update --init --recursive
   ```

### Pull docker image

   ```bash
   docker pull enidskybh/qsccp-mininet:qsccp
   docker pull enidskybh/qsccp-mininet:other
   ```

### Running QSCCP 

   ```bash
   docker run -idt --name qsccp --privileged -v path/to/qsccp-mininnet:/mini-ndn enidskybh/qsccp-mininet:qsccp /bin/bash
   docker exec -it qsccp bash
   cd /mini-ndn
   python scenarios/qsccp1.py
   ```

### Running compare contains qsccp

   ```bash
   docker run -idt --name qsccp --privileged -v path/to/qsccp-mininnet:/mini-ndn enidskybh/qsccp-mininet:qsccp /bin/bash
   docker exec -it qsccp bash
   cd /mini-ndn
   ./compare_qsccp.sh
   ```

### Running other compare scenarios

   ```bash
   docker run -idt --name qsccp --privileged -v path/to/qsccp-mininnet:/mini-ndn enidskybh/qsccp-mininet:other /bin/bash
   docker exec -it other bash
   cd /mini-ndn
   ./compare_other.sh
   ```
