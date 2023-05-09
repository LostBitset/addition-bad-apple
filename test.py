import nandlogic_test
import cla_test
import flatten_test

def main():
    print("[test.py] Running nandlogic_test...")
    nandlogic_test.main()
    print("[test.py] Running cla_test...")
    cla_test.main()
    print("[test.py] Running flatten_test...")
    flatten_test.main()
    print("[test.py] All done, everything passed!")
    print("EVERYTHING_PASSED :)")

if __name__ == "__main__":
    main()

