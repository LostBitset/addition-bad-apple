from cla import carry_lookahead_adder

def main():
    cla = carry_lookahead_adder(3)
    # 76 + 158
    # 0100 1100 + 1001 1110
    inputs = {
        "a 0": False,
        "a 1": True,
        "a 2": False,
        "a 3": False,
        "a 4": True,
        "a 5": True,
        "a 6": False,
        "a 7": False,
        "b 0": True,
        "b 1": False,
        "b 2": False,
        "b 3": True,
        "b 4": True,
        "b 5": True,
        "b 6": True,
        "b 7": False,
    }
    outputs = cla.eval(inputs)
    print(outputs)

if __name__ == "__main__":
    main()

