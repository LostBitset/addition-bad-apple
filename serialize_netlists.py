from nandlogic import Var, NandNetlist, NandOp
import typing as t

def serialize_netlist(netlist: NandNetlist) -> t.Generator[str, None, None]:
    next_id = 0
    ids = dict()
    def generate_id():
        nonlocal next_id
        curr_id = next_id
        next_id += 1
        return curr_id
    def get_id(key: Var):
        nonlocal next_id, ids
        if key in ids:
            return ids[key]
        chosen_id = generate_id()
        ids[key] = chosen_id
        return chosen_id
    merge = " ".join
    def serialize_gate_of_netlist(op: NandOp) -> str:
        line = f"nand {merge(str(get_id(i)) for i in op.inputs)} ~> {get_id(op.target)}"
        return line
    return "\n".join(serialize_gate_of_netlist(op) for op in netlist.gates)

