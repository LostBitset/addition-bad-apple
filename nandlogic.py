from dataclasses import dataclass
import typing as t

Var = str

@dataclass
class NandOp:
    target: Var
    inputs: t.List[Var]

@dataclass
class NandInstance:
    circuit: "NandCircuit"
    ibindings: t.Dict[Var, Var]
    obindings: t.Dict[Var, Var]

@dataclass
class NandCircuit:
    inputs: t.List[Var]
    outputs: t.List[Var]
    ops: t.List[NandOp | NandInstance]

