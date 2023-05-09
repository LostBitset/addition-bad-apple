from nandlogic_std import xor_g
from pprint import pprint

def main():
    netlist = xor_g.flatten()
    pprint(netlist)

if __name__ == "__main__":
    main()

