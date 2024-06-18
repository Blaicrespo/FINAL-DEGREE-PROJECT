import sys

## This is a script created by Marta Alvarez-Presas the 30/08/2023 at the Institute of Evolutionary Biology (IBE, UPF-CSIC)
## in order to remove sequences from a fasta file based on a list in a text file with the exact names in the headers.
## If you use it, please, cite.

print("Usage: python remove_seqs_from_list2.py fasta_file list_to_remove output_file")


# Define the input multifasta file and the file containing headers to remove
multifasta_file = sys.argv[1]
list_file = sys.argv[2]
output_file = sys.argv[3]

# Create a set of headers to remove
headers_to_remove = set()

with open(list_file, 'r') as list_file:
    for line in list_file:
        header_parts = line.strip().split('.')
        sequence_code = header_parts[0]
        headers_to_remove.add(sequence_code)

# Open the multifasta file for reading and create the output file
with open(multifasta_file, 'r') as infile, open(output_file, 'w') as outfile:
    current_sequence = []
    current_header = None
    remove_sequence = False

    for line in infile:
        if line.startswith(">"):
            if current_header:
                # Extract the code from the current header
                code = current_header.split('.')[0][1:]
                print(code)
                # Check if the code is in the set of headers to remove
                if code not in headers_to_remove:
                    outfile.write(current_header + '\n')
                    outfile.write(''.join(current_sequence))

                current_sequence = []

            current_header = line.strip()
            remove_sequence = False
        else:
            if not remove_sequence:
                current_sequence.append(line)

    # Write the last sequence to the output file (if it should not be removed)
    if current_header and not remove_sequence:
        outfile.write(current_header + '\n')
        outfile.write(''.join(current_sequence))
