from nandlogic_std import xor_g

def main():
    for a in (True, False):
        for b in (True, False):
            got = xor_g.eval({"a": a, "b": b})["q"]
            exp = (a ^ b)
            print(f"got: {str(got)[0]}, expected: {str(exp)[0]}")
            assert got == exp
    print("passed!")

if __name__ == "__main__":
    main()

