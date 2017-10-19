# hpc-concatenation-mapping
Intended for use on a high performance cluster that uses SGE (Son of Grid Engine)

Takes as input a text file (labeled as concatInput.txt) and outputs a matrix of total counts, which denotes expressiveness of certain genes in specific samples.

concatInput.txt inputs:

$experiment number
$directory/of/fastq/gz/files
$output/of/fastq/files
$sampleNames.csv

constraints:
  Each gene sequence, lane and number of reads must be consistent between $sampleNames.csv and $directory/of/fastq/gz/files
  Each sample must be of the form or similar to: "R324-L4-P12-GGCTAC-READ2-Sequences.txt.gz"
    Where R324 refers to the experiment number
    L4 refers to the lane position
    P12 refers to position
    GGCTAC refers to sequence
    READ2 refers to read number
  
Given that the input is valid:
  the script can then be submitted to queue via "qsub -q $QUEUE main.sh"
