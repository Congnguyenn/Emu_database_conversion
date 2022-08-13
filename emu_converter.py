import pandas as pd
from Bio import SeqIO
import os
import wget
import tarfile
import shutil
import subprocess

#I. SETTING UP:
    #1.1. INSTALL EMU WITH CONDA: https://gitlab.com/treangenlab/emu/-/tree/master:
print("1.1. INSTALL EMU WITH CONDA: Install by yourself")
print("This program must be run in base environment!")

    #1.2. PATH DECLARATION:
    #working_dir: folder contain a big fasta file:
working_dir = "/media/kt/data/Congnguyenn/Projects/Emu_database_conversion/U16S.KTEST_format/"
    #fasta: path to fasta file
fasta = working_dir + "U16S.KTEST_format.fa"
print("1.2. PATH DECLARATION: DONE")

#II. DOWNLOAD NECESSARY FILES:
    #2.1. DOWNLOAD names.dmp and nodes.dmp FILES FROM NCBI, check the link below to get the newest version:
URL="https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.tar.gz"
new_taxdump=wget.download(URL, working_dir + "new_taxdump.tar.gz")
print("")
print("2.1. DOWNLOAD names.dmp and nodes.dmp FILES FROM NCBI: DONE")

    #2.2. EXTRACT DOWNLOADED gzip FILES and REMOVE THE REDUNDANT FILES/FOLDERS:
new_taxdump = tarfile.open(new_taxdump)
new_taxdump.extractall(working_dir + "new_taxdump")
shutil.move(working_dir + "new_taxdump/names.dmp", working_dir)
shutil.move(working_dir + "new_taxdump/nodes.dmp", working_dir)
os.remove(working_dir + "new_taxdump.tar.gz")
shutil.rmtree(working_dir + "new_taxdump")
print("2.2. EXTRACT DOWNLOADED gzip FILES and REMOVE THE REDUNDANT FILES/FOLDERS: DONE")

#III. SEPARATE A BIG FASTA FILE TO SMALLER FILES:
    #3.1. SPLITTING BIG INPUT FASTA FILE INTO SMALLER FILES:
def split_fasta(input_fasta,reads_num):
    os.chdir(working_dir)
    command="split -l "+str(reads_num) + " -d "+ input_fasta + " breaked_fasta."
    os.system(command)

    print("3.1. SPLITTING BIG INPUT FASTA FILE INTO SMALLER FILES: DONE")
    
    #3.2. MOVE EXTRACTED SMALLER FASTA FILES TO ANOTHER FOLDER (smaller_fasta):
    os.mkdir(working_dir + "smaller_fasta")
    for file in os.listdir(working_dir):
        if file.startswith("breaked_fasta"):
            shutil.move(working_dir + file, working_dir + "smaller_fasta")
    print("3.2. MOVE EXTRACTED SMALLER FASTA FILES TO ANOTHER FOLDER (smaller_fasta): DONE")

#IV. GENERATE seq2tax FILE FOR EACH SMALL FASTA FILE and BUILD UP THE DATABASE FOR THEM:
    #4.1. FUNCTION TO CREATE seq2tax FILE FOR EACH SMALL FASTA FILE:
def generate_seq2tax_files(small_fasta):
    column_names=['description','taxid']
    seq2tax = pd.DataFrame(columns=column_names)

    with open(working_dir + "smaller_fasta/" + small_fasta,"r") as file:
        for record in SeqIO.parse(file,"fasta"):
            newlines = pd.DataFrame([[record.description,record.id]], columns=column_names)
            seq2tax=pd.concat([seq2tax, newlines])
        seq2tax["taxid"] = seq2tax["taxid"].str.split('|').str[0]

    seq2tax.to_csv(working_dir + "smaller_fasta/" + small_fasta + "_seq2tax.map", sep="\t", header=None, index=False)
    print("4.1. CREATE seq2tax FILE FOR " + small_fasta + ": DONE")

    #4.2. FUNCTION TO BUILD UP DATABASE FOR EACH SMALL FASTA FILES and ARRAGE THE OUTPUT:
def convert_data_main(round_ID):
    os.mkdir(working_dir + round_ID)
    os.mkdir(working_dir + round_ID + "/formated_sub_results")
    os.mkdir(working_dir + round_ID + "/formated_rawdata")
    os.mkdir(working_dir + round_ID + "/unformated_rawdata") 
    pathtonames=working_dir+"names.dmp"
    pathtonodes=working_dir+"nodes.dmp"
    
    for file in os.listdir(working_dir + "smaller_fasta"):
        if file.startswith("breaked_fasta") and not file.endswith(".map"):
            generate_seq2tax_files(file)
            
            smallfasta=working_dir + "smaller_fasta/" + file
            databasename=file+"_DB"
            pathtoseq2tax=working_dir + "smaller_fasta/" + file + "_seq2tax.map"
                   
            try:
                subprocess.check_call(['bash', '/media/kt/data/Congnguyenn/Projects/Emu_database_conversion/emu_build_database.sh', smallfasta, pathtoseq2tax, pathtonames, pathtonodes, databasename])
                shutil.move(working_dir + "smaller_fasta/" + file, working_dir + round_ID + "/formated_rawdata")
                shutil.move(working_dir + "smaller_fasta/"+ file+"_seq2tax.map", working_dir + round_ID + "/formated_rawdata")
                shutil.move(working_dir + databasename, working_dir + round_ID + "/formated_sub_results")
            except:
                print(file + " :somethingwentwrong")
                shutil.move(working_dir + "smaller_fasta/" + file, working_dir + round_ID + "/unformated_rawdata")
                shutil.move(working_dir + "smaller_fasta/"+ file+"_seq2tax.map", working_dir + round_ID + "/unformated_rawdata")
                shutil.rmtree(working_dir + databasename, ignore_errors=True)
            print(file," is done")
    os.rmdir(working_dir + "smaller_fasta") 
    print("4.2. CALL emu_build_database.sh SCRIPT TO BUILD DATABASE FOR EACH SMALL FASTA FILE: DONE")

    #4.3. MERGING THE RESULTs:
def merging_the_results(result_ID, previous_folder):
    os.mkdir(working_dir + result_ID)

    for folder in os.listdir(working_dir + previous_folder + "/formated_sub_results"):
        if folder.startswith("breaked_fasta"):
            os.chdir(working_dir + previous_folder + "/formated_sub_results/" + folder)
            
            os.rename("species_taxid.fasta", folder + "_species_taxid.fasta")
            os.rename("taxonomy.tsv", folder + "_taxonomy.tsv")
                
            shutil.move(folder + "_species_taxid.fasta", working_dir + result_ID)
            shutil.move(folder + "_taxonomy.tsv", working_dir + result_ID)
                
            os.chdir(working_dir + previous_folder + "/formated_sub_results/")
            os.rmdir(folder)
    taxonomy_emu_formated = pd.DataFrame()
    for file in os.listdir(working_dir + result_ID):
        if file.endswith(".tsv"):
            current_taxonomy = pd.read_csv(working_dir + result_ID + "/" + file, sep="\t", header=None)
            taxonomy_emu_formated = pd.concat([taxonomy_emu_formated, current_taxonomy])
            os.remove(working_dir + result_ID + "/" + file)

    taxonomy_emu_formated.columns=['tax_id','species','genus','family','order','class','phylum','clade','superkingdom','subspecies','species subgroup','species group']
    taxonomy_emu_formated.to_csv(working_dir + result_ID + "/" + "taxonomy_emu_formated.tsv", sep="\t",header=None, index=False)
    
    os.chdir(working_dir + result_ID)
    merging_command = "cat *.fasta > total.fa"
    os.system(merging_command)
    os.system("rm -rf *.fasta")
    os.rmdir(working_dir + previous_folder + "/formated_sub_results/")
              
    print("4.3. RENAME AND MOVE FILE TO A BIG FOLDER: DONE")


    #4.4. INTERMEDIATION HANDLING:
def intermediate_handling(round_number):
    os.chdir(working_dir + round_number + "/unformated_rawdata")
    os.system("rm *.map")

    merging_command = "cat *_fasta.* >" + "after_" + round_number + ".fa"
    os.system(merging_command)
    os.system("rm breaked_fasta.*")

    shutil.move(working_dir + round_number + "/unformated_rawdata/" + "after_" + round_number + ".fa", working_dir)
    shutil.rmtree(working_dir + round_number)
    print("4.4. INTERMEDIATION HANDLING: DONE")

###NAVIGATOR: 4 ROUNDS WITH BE EXECUTED: 10000-1000-50-2 LINEs PER FASTA.###########################
split_fasta(fasta, 10000)
convert_data_main("round0")
merging_the_results("result_round0","round0")
intermediate_handling("round0")

fasta = working_dir + "after_round0.fa"
split_fasta(fasta, 1000)
convert_data_main("round1")
merging_the_results("result_round1","round1")
intermediate_handling("round1")

fasta = working_dir + "after_round1.fa"
split_fasta(fasta, 50)
convert_data_main("round2")
merging_the_results("result_round2","round2")
intermediate_handling("round2")

fasta = working_dir + "after_round2.fa"
split_fasta(fasta, 2)
convert_data_main("round3")
merging_the_results("result_round3","round3")
intermediate_handling("round3")
#####################################################################################################

#V. HANDLING THE RESULT
    #5.1. MERGING FILE IN PREVIOUS ROUNDs:
    
os.mkdir(working_dir + "RESULT")
for folder in os.listdir(working_dir):
    if folder.startswith("result_"):
        os.rename(working_dir + folder + "/"+ "total.fa", working_dir + folder + "/"+ folder + "_total.fa")
        os.rename(working_dir + folder + "/"+ "taxonomy_emu_formated.tsv", working_dir + folder + "/"+ folder + "_taxonomy_emu_formated.tsv")
        
        shutil.move(working_dir + folder + "/"+ folder + "_total.fa", working_dir + "RESULT")
        shutil.move(working_dir + folder + "/"+ folder + "_taxonomy_emu_formated.tsv", working_dir + "RESULT")
        shutil.rmtree(working_dir + folder)

os.chdir(working_dir + "RESULT")
merging_tsv = "cat *.tsv > RESULT_TAXONOMY.tsv"
os.system(merging_tsv)

merging_fa = "cat *.fa > RESULT_FASTA.fasta"
os.system(merging_fa)

    #5.2. CORRECT THE FASTA HEADER:
original_file = working_dir + "RESULT/" + "RESULT_FASTA.fasta"
corrected_file = working_dir + "RESULT/" + "RESULT_FASTA_corrected.fasta"

with open(original_file) as original, open(corrected_file, 'w') as corrected:
    records = SeqIO.parse(original_file, 'fasta')
    for record in records:
        description_original = record.description
        taxid_original = record.id
        description_corrected = description_original.split("'")[1]
        record.id = description_corrected
        record.description = description_corrected
        SeqIO.write(record, corrected, 'fasta')

    #5.3. CORRECT THE RESULT_TAXONOMY.tsv:
df = pd.read_csv(working_dir + "RESULT/" + "RESULT_TAXONOMY.tsv", sep="\t")
df = df[df["tax_id"].str.contains("tax_id") == False]
df.to_csv(working_dir + "RESULT/" + "RESULT_TAXONOMY_corrected.tsv", sep="\t", index=False)

    #5.4. MOVING THE RESULT:
shutil.move(working_dir + "RESULT/" + "RESULT_FASTA_corrected.fasta", working_dir)
shutil.move(working_dir + "RESULT/" + "RESULT_TAXONOMY_corrected.tsv", working_dir)
shutil.rmtree(working_dir + "RESULT/")


