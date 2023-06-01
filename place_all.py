from place import place_frame

for i in range(1, 6572):
    print(f"=== GENERATING NETLIST, PLACEMENT FOR FRAME #{i}... ===")
    place_frame(i)

