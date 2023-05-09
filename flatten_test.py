from nandlogic_std import xor_g
from cla import carry_lookahead_adder
from pprint import pprint

def main():
    netlist1 = xor_g.flatten()
    print("===  BEGIN NETLIST: XOR_G  ===")
    pprint(netlist1)
    print("===   END NETLIST: XOR_G   ===")
    print("^^^")
    print(f"^^^ GATE COUNT = {len(netlist1.gates)}")
    netlist2 = carry_lookahead_adder(3).flatten()
    print("===  BEGIN NETLIST: CARRY_LOOKAHEAD_ADDER(3)  ===")
    pprint(netlist2)
    print("===   END NETLIST: CARRY_LOOKAHEAD_ADDER(3)   ===")
    print("^^^")
    print(f"^^^ GATE COUNT = {len(netlist2.gates)}")
    netlist3 = carry_lookahead_adder(8).flatten()
    print("===  BEGIN NETLIST: CARRY_LOOKAHEAD_ADDER(8)  ===")
    pprint(netlist3)
    print("===   END NETLIST: CARRY_LOOKAHEAD_ADDER(8)   ===")
    print("^^^")
    print(f"^^^ GATE COUNT = {len(netlist3.gates)}")

if __name__ == "__main__":
    main()

