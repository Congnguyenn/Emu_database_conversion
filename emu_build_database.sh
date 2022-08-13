#!/bin/bash
source activate emu

smallfasta=$1
pathtoseq2tax=$2

pathtonames=$3
pathtonodes=$4

databasename=$5


emu build-database $databasename --names $pathtonames --nodes $pathtonodes --sequences $smallfasta --seq2tax $pathtoseq2tax --threads 20





