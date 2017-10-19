#! /bin/bash
#$ -N samplename_star_hg38
#$ -pe openmp 10
#$ -q bio
#$ -l mem_free=50G
#$ -hold_jid CONCAT

module load STAR/2.5.2a

STAR --runThreadN 10 --genomeDir /pub/wpoon/df/pipeline/star.index --readFilesCommand zcat --readFilesIn /fastqdirectory/samplename-Read1.fastq.gz /fastqdirectory/samplename-Read2.fastq.gz --sjdbGTFfile /pub/wpoon/df/pipeline/gencode/gencode.v24.ERCC.annotation.gtf --outFileNamePrefix star_hg38 --outFilterMismatchNmax 10 --outFilterMismatchNoverReadLmax 0.07 --outFilterMultimapNmax 10 --outSAMunmapped None --alignIntronMax 1000000 --alignIntronMin 20 --alignMatesGapMax 1000000 --outSAMtype BAM SortedByCoordinate --quantMode TranscriptomeSAM --alignSJoverhangMin 8 --alignSJDBoverhangMin 1 --sjdbScore 1 --outWigType wiggle --outWigStrand Unstranded --outWigNorm RPM