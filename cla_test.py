from cla import carry_lookahead_adder
from adder_utils import make_adder_inputs

def main():
    cla = carry_lookahead_adder(3)
    inputs = make_adder_inputs(69, 80)
    outputs = cla.eval(inputs, True)
    print("".join([
        "1" if outputs[f"sum {i}"] else "0"
        for i in range(8)
    ]))

if __name__ == "__main__":
    main()

