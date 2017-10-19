#! /bin/bash
#$ -N samplename
#$ -o samplename
#$ -e samplename
#$ -pe openmp 16
#$ -q bio
#$ -ckpt blcr
#$ -l kernel=blcr
#$ -r y
#$ -hold_jid star_wait

module load rsem/1.2.12
module load samtools/1.0

rsem-calculate-expression -p $CORES --paired-end --bam star_hg38Aligned.toTranscriptome.out.bam /pub/wpoon/df/pipeline/gencode/rsem.hg38.ERCC.gencode.v24 sample.rsem
