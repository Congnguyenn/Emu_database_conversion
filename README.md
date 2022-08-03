# Emu_database_conversion
In order to build an Emu custom database, we need 4 following files:
1. names.dmp
2. nodes.dmp
3. fasta
4. seq2tax

after collecting mentioned files, all you need to do is run the command

emu build-database zymo_assembled_db --names ./example_customdb/ex_names.dmp --nodes ./example_customdb/ex_nodes.dmp --sequences ./example_customdb/ex.fasta --seq2tax ./example_customdb/ex_seq2tax.map











