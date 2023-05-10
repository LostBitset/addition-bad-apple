from serialize_netlists import serialize_netlist
from check_netlists import check_netlist
from cla import carry_lookahead_adder

def main():
    netlist = carry_lookahead_adder(3).flatten()
    check_netlist(netlist)
    gates_netlist = len(netlist.gates)
    ser = serialize_netlist(netlist)
    print("===  BEGIN SERIALIZED NETLIST  ===")
    print(ser)
    print("===   END SERIALIZED NETLIST   ===")
    gates_ser = ser.count("\n") + 1
    print(f"Gate count (original netlist): {gates_netlist}")
    print(f"Gate count (serialized netlist): {gates_ser}")
    assert gates_netlist == gates_ser
    print("passed!")

if __name__ == "__main__":
    main()

