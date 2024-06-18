import os
import sys

print("Usage: python fetch_seqs.py list_folder proteome_folder output_folder")

# Define the input and output folders
list_folder = sys.argv[1]
proteome_folder = sys.argv[2]
output_folder = sys.argv[3]

# Iterate over the list files in the list folder
for list_file_name in os.listdir(list_folder):
    if list_file_name.endswith(".txt"):
        list_file_path = os.path.join(list_folder, list_file_name)
        
        # Extract the species name from the list file name (excluding the extension)
        species_name = os.path.splitext(list_file_name)[0]
        
        # Initialize a dictionary to store sequences
        sequences = {}
        
        # Read the list file and extract the header names
        with open(list_file_path, "r") as list_file:
            for line in list_file:
                header = line.strip()
                sequences[header] = ""
        
        # Initialize variables to store the current sequence and header
        current_sequence = ""
        current_header = ""
        
        # Read the proteome file and extract matching sequences
        proteome_file_name = f"{species_name}.fa"
        proteome_file_path = os.path.join(proteome_folder, proteome_file_name)
        
        with open(proteome_file_path, "r") as proteome_file:
            for line in proteome_file:
                if line.startswith(">"):
                    # If the line starts with '>', it's a header
                    # Write the previous sequence (if any) to the appropriate output
                    if current_sequence and current_header in sequences:
                        sequences[current_header] = current_sequence
                    current_header = line.strip()
                    current_sequence = ""
                else:
                    # Otherwise, it's sequence data; append it to the current sequence
                    current_sequence += line.strip()
        
        # Write the matching sequences to the output file
        output_file_name = f"{species_name}_sequences.fa"
        output_file_path = os.path.join(output_folder, output_file_name)
        with open(output_file_path, "w") as output_file:
            for header, sequence in sequences.items():
                if sequence:
                    output_file.write(f">{header}\n{sequence}\n")
