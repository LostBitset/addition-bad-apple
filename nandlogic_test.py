from nandlogic_std import xor_g

def main():
    for a in (True, False):
        for b in (True, False):
            assert xor_g.eval({"a": a, "b": b}) == (a ^ b)
    print("passed!")

if __name__ == "__main__":
    main()

