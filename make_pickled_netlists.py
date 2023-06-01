from serialize_netlists import serialize_netlist
from check_netlists import check_netlist
from cla import carry_lookahead_adder

import pickle as pkl

def cla_netlist(levels):
    netlist = carry_lookahead_adder(levels).flatten()
    return netlist.gates

def main():
    obj = dict()
    for levels in range(1, 6):
        obj[levels] = cla_netlist(levels)
    with open("netlists.pkl", "wb") as f:
        pkl.dump(obj, f)

if __name__ == "__main__":
    main()

