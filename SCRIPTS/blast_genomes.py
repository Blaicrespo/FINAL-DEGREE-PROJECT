

Genomes_folder = "/home/blaicrespo/Documents/TFG/Genomes/"
main_folder = "/home/blaicrespo/Documents/TFG"

# Ask user for the gene family
gene_family = input("Enter the gene family you are working with: ")

# Ask user for the genomes to be included in the database
print(f"Available genomes in {Genomes_folder}:")
available_genomes = os.listdir(Genomes_folder)
for i, genome in enumerate(available_genomes):
    print(f"{i + 1}. {genome}")

selected_indices = input("Enter the numbers of the genomes you want to include in the database, separated by commas: ")
selected_genomes = [available_genomes[int(i) - 1] for i in selected_indices.split(',')]

# Create DIAMOND database
db_path = f"{main_folder}/{gene_family}_db.dmnd"
genome_files = " ".join([f"{Genomes_folder}/{genome}" for genome in selected_genomes])

print("Creating DIAMOND database...")
os.system(f"diamond makedb --in {genome_files} -d {db_path}")

# Create a new folder in main_folder named Results
results_folder = f"{main_folder}/Results"
if not os.path.exists(results_folder):
    os.makedirs(results_folder)

# Ask for the protein sequence in fasta that is wanted to be the query
query_protein = input("Enter the path to the protein sequence in fasta format: ")

# Do the BLAST against the genomes database created
blast_output = f"{results_folder}/{gene_family}_result.txt"
print("Running BLAST...")
os.system(f"diamond blastp -d {db_path} -q {query_protein} -o {blast_output} -k 10 --outfmt 6 -p 0")


print("BLAST is done. The resulting file is in Results.")

