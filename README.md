# Emu_database_conversion
## Overview
In order to build an Emu custom database, we need 4 following files:
1. names.dmp
2. nodes.dmp
3. fasta
4. seq2tax.map

After collecting mentioned files, all you need to do is run the command

```conda activate emu``` **[Emu installation](https://gitlab.com/treangenlab/emu/-/tree/master)**

```emu build-database zymo_assembled_db --names names.dmp --nodes nodes.dmp --sequences fasta --seq2tax seq2tax.map --threads 64```

## But, how to collect 4 aforementioned files?:
1. name.dmp and node.dmp could be downloaded from [HERE](https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/)
2. fasta: a fasta file contains both your sequences and the identification header of each sequence. Note: It must be **spaces-contain-free**
3. seq2tax: a tab delimiter tabular format contains the header (similar to the fasta file) and a taxid

## Problems - solution:
**Problem_03**: The error *"EOFError: Ran out of input"* when execute the ```emu build-database``` command appears to be a memory bug, potentially involving the library pandaralle.

**Causes: This problem can be caused by 2 reasons
  - Memory limitation: when running a big file
  - Sequence: Because of some unknown reasons, some sequences can not be executed, therefore the small file (breaked from the original file) can not be execute too.

**Solution_03**: To solve 2 mentioned problems, I performed:
  - Breaking file into smaller pieces
  - Iterative approach: that means breaking file into different sizes (10000, 1000, 50, 2 lines in a file) and execute it in the different rounds. The final round only contains 2 lines (means one sequence), so the sequences which can not be run could be identified. This solution also alows to maximize the size of data and re-useable

## The meaning of files and folders in this repository:
  - U16S.KTEST_format: Working directory
  - U16S.KTEST_format.fa: your input fasta file
  - nodes.dmp and names.dmp: Downloaded from the above link
  - after_round4.fa: Contains the sequences which can not be execute even individually
  - emu_converter.py: The python script to build the database
  - emu_build_database.sh: The bash script contains the command to run the ```emu build-database```, above python script will call this bash script automatically
  - RESULT_FASTA_corrected.fasta and RESULT_TAXONOMY_corrected.tsv: fasta and tsv files contain the sequence and taxonomy information, this is the expectated result.
  
 







