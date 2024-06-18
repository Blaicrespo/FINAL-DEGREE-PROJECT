import sys

import os
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Blast import NCBIWWW, NCBIXML

## This is a script created by Blai Crespo Selma the 24/04/2024 at the Institute of Evolutionary Biology (IBE, UPF-CSIC)
## in order to perform gene expression analysis of gene families of interest into a folder of transcriptomes.
## If you use it, please, cite.



# Step 1: Read the protein sequence of your gene of interest from a FASTA file
def read_protein_sequence():
    file_path = input("Enter the file path of the gene of interest (in FASTA format): ")
    with open(file_path, "r") as f:
        record = SeqIO.read(f, "fasta")
    return record.seq, os.path.basename(file_path)

# Step 2: Translate protein sequence to nucleotide sequence
def translate_to_nucleotide(protein_sequence):
    nucleotide_seq = protein_sequence.translate(to_stop=True)
    return nucleotide_seq

# Step 3: Align the nucleotide sequence to the transcriptomes
def perform_alignment(nucleotide_sequence, transcriptome_folder):
    alignments = []
    for record in SeqIO.parse(transcriptome_folder, "fasta"):
        result_handle = NCBIWWW.qblast("blastn", "nt", nucleotide_sequence)
        blast_record = NCBIXML.read(result_handle)
        alignments.append((record.id, blast_record))
    return alignments

# Step 4: Analyze alignment results and determine expression levels
def analyze_expression(alignments):
    expression_levels = {}
    for transcript_id, alignment in alignments:
        # Analyze alignment data to determine expression levels
        # Example: calculate the number of hits or alignment scores
        expression_levels[transcript_id] = len(alignment.alignments)
    return expression_levels

# Step 5: Main function to execute the steps
def main():
    # Step 1: Read protein sequence
    print("Enter the file path of the gene of interest (in FASTA format):")
    protein_sequence, gene_name = read_protein_sequence()
    
    # Translate protein sequence to nucleotide sequence
    nucleotide_sequence = translate_to_nucleotide(protein_sequence)
    
    # Provide path to the folder containing transcriptome FASTA files
    transcriptome_folder_path = input("Enter the path to the folder containing transcriptome files (in FASTA format): ")
    
    # Create a folder to store results
    results_folder = f"{gene_name}_results"
    os.makedirs(results_folder, exist_ok=True)
    
    # Step 3: Perform alignment
    alignments = perform_alignment(nucleotide_sequence, transcriptome_folder_path)
    
    # Step 4: Analyze expression
    expression_levels = analyze_expression(alignments)
    
    # Step 5: Save and print expression levels
    output_file = os.path.join(results_folder, f"{gene_name}_expression_levels.txt")
    with open(output_file, "w") as f:
        for transcript_id, expression_level in expression_levels.items():
            f.write(f"Transcript {transcript_id}: Expression level = {expression_level}\n")
            print(f"Transcript {transcript_id}: Expression level = {expression_level}")
    
    print(f"\nResults saved in {results_folder}")

if __name__ == "__main__":
    main()

