from nandlogic import NandCircuit, NandInstance, NandOp
from nandlogic_std import and_g, or_g, xor_g

partial_fa = NandCircuit(
    ["a", "b", "c in"],
    ["sum", "c prop", "c gen"],
    [
        NandInstance(xor_g, {"a": "a", "b": "b"}, {"q": "sum carryless"}),
        NandInstance(xor_g, {"a": "sum carryless", "b": "c in"}, {"q": "sum"}),
        NandInstance(or_g, {"a": "a", "b": "b"}, {"q": "c prop"}),
        NandInstance(and_g, {"a": "a", "b": "b"}, {"q": "c gen"}),
    ],
)

