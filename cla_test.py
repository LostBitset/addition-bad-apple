from nandlogic import NandCircuit
from cla import carry_lookahead_adder
from adder_utils import make_adder_inputs

from random import randint

def test_inputs(cla: NandCircuit, levels: int, a: int, b: int):
    inputs = make_adder_inputs(a, b, 2 ** levels)
    outputs = cla.eval(inputs)
    output_int = eval(
        "0b" + "".join(
            reversed([
                "1" if outputs[f"sum {i}"] else "0"
                for i in range(8)
            ])
        )
    )
    print(f"[test] Claims {a} + {b} = {output_int}. ", end="")
    if output_int == (a + b):
        print("(correct)")
    else:
        print("(INCORRECT) /!\\ FAIL /!\\")
        assert False

def main():
    levels = 3
    cla = carry_lookahead_adder(levels)
    test_inputs(cla, levels, 0, 0)
    test_inputs(cla, levels, 0, 1)
    test_inputs(cla, levels, 1, 0)
    test_inputs(cla, levels, 1, 1)
    test_inputs(cla, levels, 126, 127)
    test_inputs(cla, levels, 127, 127)
    for _ in range(1000):
        a = randint(0, 127)
        b = randint(0, 127)
        test_inputs(cla, levels, a, b)

if __name__ == "__main__":
    main()

