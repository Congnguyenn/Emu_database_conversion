# Emu_database_conversion
## Overview
In order to build an Emu custom database, we need 4 following files:
1. names.dmp
2. nodes.dmp
3. fasta
4. seq2tax.map

After collecting mentioned files, all you need to do is run the command

```emu build-database zymo_assembled_db --names names.dmp --nodes nodes.dmp --sequences fasta --seq2tax seq2tax.map --threads 64```

## But, how to collect 4 aforementioned files?:
1. name.dmp and node.dmp could be downloaded from [HERE](https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/)
2. fasta: a fasta file contains both your sequences and the identification header of each sequence. Note: It must be **spaces-contain-free**
3. seq2tax: a tab delimiter tabular format contains the header (similar to the fasta file) and a taxid

## Problems - solution:
**Problem_01**: Six IDs (1670641, 419596, 335819, 143813, 2213057, 93930) can not be found in the nodes.dmp
**Solution_01**: I removed them in both fasta and seq2tax.map files --> is it ok?, do the removed id make any sense?

**Problem_02**: Original fasta files include several spaces in the header, therefore, it did not work without editing
**Solution_02**: I write a python code to perform:
1. Replace spaces by ```~``` sign, I've already used ```grep``` command to verify there is no ```~``` sign in the original fasta file
2. Export the seq2tax.map files corresponding to fasta files

**Problem_03**: The error *"EOFError: Ran out of input"* when execute the ```emu build-database``` command appears to be a memory bug, potentially involving the library pandaralle.
**Solution_03**: The author recommended to split data into smaller pieces. I have breaked them into total 18 fasta files, corresponding to 18 seq2tax.map files. 

## Question:
**Question_01**: Some steps in this procedure are run manually (via command line) --> do I need to make them run automatically?

**Question_02**: I have to run the code to verify all the results or just need to randomly check?










