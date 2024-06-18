#!/bin/bash

## Script for building a hmm database based on an alignment, and then fetch the sequences from the proteomes. 
## Watch out, you will need to change paths. All the folders will have the same gene name that you decide at the beginning of the analysis.
## Date: 18-10-23
## Author: Marta Alvarez-Presas
## Contact: Institute of Evolutionary Biology (IBE, UPF-CSIC) - marta.alvarez@ibe.upf-csic.es

proteomes_folder="/home/blaicrespo/Documents/TFG/proteomes/"
main_folder="/home/blaicrespo/Documents/TFG"


# Ask the user for the gene name
read -p "Please, enter your gene name: " gene_name

# Ask for the name of the input sequences from NCBI
echo "Please, enter the name of your input sequences file from NCBI: "
read input_seqs_NCBI


## First remove duplicates from the proteins fetched from NCBI ##

# Ask the user for the gene name
read -p "Please, enter the path to your sequences: " sequences_folder

cd $main_folder/Sequences/$sequences_folder/
pwd
filename=$(basename "$input_seqs_NCBI" | cut -d. -f1)
output1_dedup="$filename"_dedup.fa
seqkit rmdup -s $input_seqs_NCBI -o $output1_dedup

orig_num_seqs=$(grep -c "^>" "$output1_dedup")

echo "Output file $output1_dedup created. It contains: $orig_num_seqs sequences."

## The second step is to perform the MAFFT alignment with the filtered sequences ##

mkdir $main_folder/Alignments/$gene_name
alignment_folder=$main_folder/Alignments/$gene_name
output2_ali="$filename"_MAFFT.fa

# Give the user the option to choose if they want to perform the mafft alignment or not (if the sequences file is too big, maybe it is
# worth executing the alignment in the MAFFT web server (https://mafft.cbrc.jp/alignment/server/index.html)

read -p "Do you want to perform the alignment? (yes/no): " choice

if [ "$choice" == "yes" ]; then
    # Execute the alignment step
    echo "Performing the alignment..."
    
	mafft --maxiterate 1000 --globalpair --op 2.15 --leavegappyregion --reorder $output1_dedup > $alignment_folder/$output2_ali
	echo "Output file $output2_ali created."
else
    echo "Alignment step skipped."
fi


## Third step is trimming the alignment using the best trimal parameters ##

cd $alignment_folder/
pwd
ls
echo $output2_ali
output3_trim="$filename"_MAFFT_trim.fasta
/home/blaicrespo/Downloads/trimAl/source/trimal -in $output2_ali -out $output3_trim -gt 0.5

echo "Output file $output3_trim created."

## Now it's time to build the hmm database ##

# Build the HMM database
output4_hmm="$gene_name".hmm
hmmbuild "$output4_hmm" "$output3_trim"

echo "Output file $output4_hmm created."

## We are doing the hmmsearch now ##

mkdir $main_folder/HMM/$gene_name
hmm_folder=$main_folder/HMM/"$gene_name"
cd $hmm_folder
pwd

# Ask for the threshold in the evalue:
read -p "Please, enter the threshold for the evalue: " evalue

mkdir "$evalue"

cd $proteomes_folder
pwd

for proteome in *.fa; do hmmsearch --tblout $hmm_folder/"$evalue"/"$proteome"_output.txt -E 1e-"$evalue" --domT 0.5 $alignment_folder/$output4_hmm $proteome; done

cd $hmm_folder/"$evalue"/
pwd
mkdir Lists
mkdir sequences

##Now we are gonna clean the text files ##

for report in *.txt; do filename2=$(basename "$report" | cut -d. -f1); awk '{if (NR>3) print $1}' $report > Lists/"$filename2"_hits.txt; done
cd Lists/
for headers in *.txt; do sudo sed -i 's/^/>/g' $headers; done
for f in *.txt; do sudo sed -i 's/>#//g' $f; done
for f in *.txt; do mv -- "$f" "${f%_hits.txt}.txt"; done
for f in *.txt; do sudo sed -i '/^$/d' $f; done
cd ..
find Lists/ -type f -empty -delete

## It's time now to fetch the sequences ##

python /home/blaicrespo/Documents/TFG/Scripts/fetch_seqs.py Lists/ $proteomes_folder sequences/
cd sequences/
for f in *.fa; do sudo sed -i 's/>>/>/g' $f; done

output5_seqs="$gene_name"_"$evalue"_prot.fa
cat *.fa > $output5_seqs

num_seqs=$(grep -c "^>" "$output5_seqs")

echo "Your sequences are fetched now! Your file is $output5_seqs and contains $num_seqs sequences."

mkdir $main_folder/Sequences/$gene_name
cp $output5_seqs $main_folder/Sequences/$gene_name/

##Let's do some phylogenies ##

output6_ali="$gene_name"_"$evalue"_prot_MAFFT.fa

# Give the user the option to choose if they want to perform the mafft alignment or not (if the sequences file is too big, maybe it is
# worth executing the alignment in the MAFFT web server (https://mafft.cbrc.jp/alignment/server/index.html)
read -p "Do you want to perform the alignment? (yes/no): " choice

if [ "$choice" == "yes" ]; then
    # Execute the alignment step
    echo "Performing the alignment..."
    
	mafft --maxiterate 1000 --globalpair --op 2.15 --leavegappyregion --reorder $output5_seqs > $alignment_folder/$output6_ali
	echo "Output file $output6_ali created."
else
    echo "Alignment step skipped."
fi


cd $alignment_folder/
pwd
ls
echo $output6_ali

output7_trim="$gene_name"_"$evalue"_prot_MAFFT_trim.fasta
/home/blaicrespo/Downloads/trimAl/source/trimal -in $output6_ali -out $output7_trim -gt 0.5

echo "Output file $output7_trim created."

iqtree -s $output7_trim -m TESTMERGE -rcluster 10 -nt AUTO #-b or -bnni 10000 to do bootstrapping

## Before we finish, let's do some cleaning and tidying up ##

mkdir $main_folder/Trees/$gene_name
mkdir $main_folder/Trees/$gene_name/$evalue
tree_folder=$main_folder/Trees/$gene_name/$evalue
mv *.treefile $tree_folder/
cp $output7_trim $tree_folder/

rm $output7_trim".mldist"
rm $output7_trim".log"
rm $output7_trim".contree"
rm $output7_trim".ckp.gz"
rm $output7_trim".bionj"
rm $output7_trim".iqtree"
rm $output7_trim".model.gz"
rm $output7_trim".uniqueseq.phy"
rm $output7_trim".splits.nex"

echo "Done. Your tree is ready, please analyse your results carefully, and if needed use hmm_fetch2.sh for a second round of hmmsearch."


