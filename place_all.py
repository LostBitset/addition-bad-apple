from os import system

for i in range(1, 6572):
    print(f"=== GENERATING NETLIST, PLACEMENT FOR FRAME #{i}... ===")
    system(f"python place.py {i}")

