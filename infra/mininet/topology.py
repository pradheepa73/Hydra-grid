"""HYDRA-GRID - Mininet topology scaffold.

Defines a virtual SCADA network for future hardware-in-the-loop testing.
Phase 2 of the roadmap.
"""
from mininet.topo import Topo


class HydraGridTopo(Topo):
    """Simple SCADA topology: 1 master, 3 substations, 1 IT network."""

    def build(self):
        # SCADA master
        scada = self.addHost("scada_master")
        # Substations
        s1 = self.addHost("substation_1")
        s2 = self.addHost("substation_2")
        s3 = self.addHost("substation_3")
        # IT network
        it = self.addHost("it_net")
        # Switch
        switch = self.addSwitch("s1_switch")
        # Links
        self.addLink(scada, switch)
        self.addLink(s1, switch)
        self.addLink(s2, switch)
        self.addLink(s3, switch)
        self.addLink(it, switch)


if __name__ == "__main__":
    print("HydraGridTopo defined. Run with: mn --custom topology.py --topo hydragrid")
