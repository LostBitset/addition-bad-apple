import pickle as pkl

netlists = None
with open("netlists.pkl", "rb") as f:
    netlists = pkl.load(f)

print(netlists)

