#!/bin/bash

# Step 1: Read the protein sequence of your gene of interest from a FASTA file
read_protein_sequence() {
    echo "Enter the file path of the gene of interest (in FASTA format):"
    read file_path
    protein_sequence=$(grep -v ">" "$file_path" | tr -d '\n')
    gene_name=$(basename "$file_path" .fasta)
}

# Step 2: Translate protein sequence to nucleotide sequence
translate_to_nucleotide() {
    nucleotide_sequence=$(echo "$protein_sequence" | tr 'A-Z' 'T-Z' | tr 'A-Z' 'ATCG')
}

# Step 3: Align the nucleotide sequence to the transcriptomes
perform_alignment() {
    echo "Enter the path to the folder containing transcriptome files (in FASTA format):"
    read transcriptome_folder_path
    for file in "$transcriptome_folder_path"/*.fasta; do
        transcript_id=$(basename "$file" .fasta)
        blastn -query <(echo "$nucleotide_sequence") -subject "$file" -outfmt 5 | grep "<Iteration_query-def>$transcript_id</Iteration_query-def>" > "$gene_name-$transcript_id.xml"
    done
}

# Step 4: Analyze alignment results and determine expression levels
analyze_expression() {
    for file in ./*.xml; do
        transcript_id=$(basename "$file" .xml | cut -d'-' -f2)
        expression_level=$(grep -c "<Hsp>" "$file")
        echo "Transcript $transcript_id: Expression level = $expression_level"
    done
}

# Step 5: Main function to execute the steps
main() {
    read_protein_sequence
    translate_to_nucleotide
    perform_alignment
    analyze_expression
}

# Execute main function
main

