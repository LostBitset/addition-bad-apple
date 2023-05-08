from nandlogic import NandOp, NandCircuit, NandInstance

not_g = NandCircuit(
    ["a"],
    ["q"],
    [ NandOp("q", ["a"]) ],
)


and_g = NandCircuit(
    ["a", "b"],
    ["q"],
    [
        NandOp("q not", ["a", "b"]),
        NandOp("q", ["q not"]),
    ],
)

or_g = NandCircuit(
    ["a", "b"],
    ["q"],
    [
        NandOp("a not", ["a"]),
        NandOp("b not", ["b"]),
        NandOp("q", ["a not", "b not"]),
    ],
)

xor_g = NandCircuit(
    ["a", "b"],
    ["q"],
    [
        NandInstance(or_g, {"a": "a", "b": "b"}, {"q": "a or b"}),
        NandOp("a nand b", ["a", "b"]),
        NandInstance(and_g, {"a": "a or b", "b": "a nand b"}, {"q": "q"}),
    ],
)

