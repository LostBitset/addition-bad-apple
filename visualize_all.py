from os import system

for i in range(1, 6572):
    print(f"=== GENERATING VISUAL FOR FRAME #{i}... ===")
    system(f"python visual.py out_placed/frame{i}.placement.txt")

