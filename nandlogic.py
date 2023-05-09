from dataclasses import dataclass
import typing as t

def nand(xs: t.List[bool]) -> bool:
    return not all(xs)

Var = str

@dataclass
class NandOp:
    target: Var
    inputs: t.List[Var]

@dataclass
class SimpleBinding:
    target: Var
    source: Var | bool

@dataclass
class NandInstance:
    circuit: "NandCircuit"
    ibindings: t.Dict[Var, Var]  # inner -> outer
    obindings: t.Dict[Var, Var]  # inner -> outer

@dataclass
class NandNetlist:
    gates: t.List[NandOp]

def qualify_rename(x_unqualified: Var, ns: Var, renames: t.Dict[Var, Var]) -> Var:
    x = f"{ns}/{x_unqualified}"
    while x in renames:
        x = renames[x]
    return x

@dataclass
class NandCircuit:
    inputs: t.List[Var]
    outputs: t.List[Var]
    ops: t.List[NandOp | NandInstance | SimpleBinding]

    def flatten(self) -> NandNetlist:
        nl = NandNetlist([])
        self.flatten_into(nl, "#root#", dict()),
        return nl

    def flatten_into(self, nl: NandNetlist, ns: Var, renames: t.Dict[Var, Var]):
        counter = 0
        for op in self.ops:
            if isinstance(op, NandOp):
                nl.gates.append(NandOp(
                    qualify_rename(op.target, ns, renames),
                    [
                        qualify_rename(i, ns, renames)
                        for i in op.inputs
                    ],
                ))
            elif isinstance(op, NandInstance):
                submodule_ns = f"{ns}/#{counter}"
                for inner, outer in op.ibindings.items():
                    inner_name = qualify_rename(inner, submodule_ns, renames)
                    outer_name = qualify_rename(outer, ns, renames)
                    renames[inner_name] = outer_name
                for inner, outer in op.obindings.items():
                    inner_name = qualify_rename(inner, submodule_ns, renames)
                    outer_name = qualify_rename(outer, ns, renames)
                    renames[outer_name] = inner_name
                op.circuit.flatten_into(nl, submodule_ns, renames)
                counter += 1
            elif isinstance(op, SimpleBinding):
                if isinstance(op.source, bool):
                    raise UnflattenableNandOpError(op)
                elif isinstance(op.source, Var):
                    target_name = qualify_rename(op.target, ns, renames)
                    source_name = qualify_rename(op.source, ns, renames)
                    renames[target_name] = source_name
                else:
                    raise BadNandOpError(op)
            else:
                raise BadNandOpError(op)

    def eval(self, ivals: t.Dict[Var, bool], dbg: bool = False) -> t.Dict[Var, bool]:
        state = ivals.copy()
        for op in self.ops:
            if isinstance(op, NandOp):
                state[op.target] = nand([
                    state[var] for var in op.inputs
                ])
            elif isinstance(op, NandInstance):
                outputs = op.circuit.eval({
                    inner: state[outer]
                    for inner, outer in op.ibindings.items()
                })
                for inner, value in outputs.items():
                    state[op.obindings[inner]] = value
            elif isinstance(op, SimpleBinding):
                if isinstance(op.source, Var):
                    state[op.target] = state[op.source]
                elif isinstance(op.source, bool):
                    state[op.target] = op.source
                else:
                    raise BadNandOpError(op)
            else:
                raise BadNandOpError(op)
        if dbg:
            print("===  BEGIN DEBUG OUTPUT  ===")
            for k, v in state.items():
                print(f"{k} -> {v}")
            print("===   END DEBUG OUTPUT   ===")
        return {
            k: state[k]
            for k in self.outputs
        }

class UnflattenableNandOpError(BaseException):
    def __init__(self, op: t.Any):
        self.op = op

    def __str__(self) -> str:
        return "Unflattenable nand op: {repr(op)}."

class BadNandOpError(BaseException):
    def __init__(self, op: t.Any):
        self.op = op

    def __str__(self) -> str:
        return "Bad nand op: {repr(op)}."

