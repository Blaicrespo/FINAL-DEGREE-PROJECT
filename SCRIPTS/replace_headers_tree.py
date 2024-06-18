import sys

print("Usage: python replace_headers_tree.py tree_file mapping_file output_tree_file")


# Define the tree file name
tree_file = sys.argv[1]
mapping_file = sys.argv[2]
output_tree_file = sys.argv[3]

# Create a dictionary to store the mapping
mapping = {}
with open(mapping_file, "r") as map_file:
	for line in map_file:
		original_name, code = line.strip().split()
		mapping[original_name] = code

# Replace headers in the tree file
with open(tree_file, "r") as tree_file, open(output_tree_file, "w") as out_tree_file:
    for line in tree_file:
        for original_name, code in mapping.items():
            line = line.replace(original_name, code)
        out_tree_file.write(line)
