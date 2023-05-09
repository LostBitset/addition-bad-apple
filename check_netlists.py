from nandlogic import NandNetlist, NandOp

def check_netlist_return_ok(netlist: NandNetlist) -> bool:
    set_nets = set()
    seen_root_nets = 0
    for op in netlist.gates:
        for i in op.inputs:
            if i not in set_nets:
                if i.startswith("#fixed#/"):
                    pass
                elif i.startswith("#root#"):
                    if i.count("/") > 1:
                        print(f"NETLIST CHECK FAILED: Not connected: {i}")
                        return False
                    else:
                        seen_root_nets += 1
                else:
                    print(f"NETLIST CHECK FAILED: Has unknown root: {i}")
                    return False
        set_nets.add(op.target)
    print(f"NETLIST CHECK OK: Total nets: {len(set_nets) + seen_root_nets}")
    return True

def check_netlist(netlist: NandNetlist):
    if not check_netlist_return_ok(netlist):
        raise BadNetlistError()

class BadNetlistError(BaseException):
    def __str__(self):
        return "Bad netlist, see message above."

