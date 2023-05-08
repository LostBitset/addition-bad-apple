from cla import carry_lookahead_adder

def main():
    cla = carry_lookahead_adder(3)
    inputs = {

        "a 0": True,
        "a 1": False,
        "a 2": False,
        "a 3": False,
        "a 4": False,
        "a 5": False,
        "a 6": False,
        "a 7": False,

        "b 0": True,
        "b 1": False,
        "b 2": False,
        "b 3": False,
        "b 4": False,
        "b 5": False,
        "b 6": False,
        "b 7": False,

    }
    outputs = cla.eval(inputs, True)
    print("".join([
        "1" if outputs[f"sum {i}"] else "0"
        for i in range(8)
    ]))

if __name__ == "__main__":
    main()

