import sys

# Define the mapping file name and alignment file name
mapping_file = sys.argv[2]
alignment_file = sys.argv[1]
output_alignment_file = sys.argv[3]

# Create a dictionary to store the mapping
mapping = {}
with open(mapping_file, "r") as map_file:
    for line in map_file:
        original_name, code = line.strip().split()
        mapping[original_name] = code

# Replace headers in the alignment file
with open(alignment_file, "r") as align_file, open(output_alignment_file, "w") as out_align_file:
    for line in align_file:
        if line.startswith(">"):
            original_name = line.strip()[1:]
            code = mapping.get(original_name, original_name)
            out_align_file.write(f">{code}\n")
        else:
            out_align_file.write(line)
