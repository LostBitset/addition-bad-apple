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
class NandInstance:
    circuit: "NandCircuit"
    ibindings: t.Dict[Var, Var]  # inner -> outer
    obindings: t.Dict[Var, Var]  # inner -> outer

@dataclass
class NandCircuit:
    inputs: t.List[Var]
    outputs: t.List[Var]
    ops: t.List[NandOp | NandInstance]

    def eval(self, ivals: t.Dict[Var, bool]) -> t.Dict[Var, bool]:
        state = ivals.copy()
        for op in self.ops:
            if isinstance(op, NandOp):
                state[op.target] = nand([
                    state[var] for var in op.inputs
                ])
            elif isinstance(op, NandInstance):
                outputs = op.circuit.eval({
                    inner: state[outer]
                    for inner, outer in op.ibindings.entries()
                })
                for inner, value in outputs:
                    state[op.obindings[inner]] = value
            else:
                raise BadNandOpError(op)

class BadNandOpError(BaseException):
    def __init__(self, op: t.Any):
        self.op = op

    def __str__(self) -> str:
        return "Bad nand op: {repr(op)}."

