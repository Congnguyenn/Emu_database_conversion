# Emu_database_conversion
In order to build an Emu custom database, we need 4 following files:
1. names.dmp
2. nodes.dmp
3. fasta
4. seq2tax

After collecting mentioned files, all you need to do is run the command

'''emu build-database zymo_assembled_db --names names.dmp --nodes nodes.dmp --sequences fasta --seq2tax seq2tax.map --threads 64'''











