#! /bin/bash
#$ -N matrixAWK
#$ -q bio
#$ -hold_jid ATGTCA_N_TCW1KO2_rsem,GTGAAA_N_TCW1KO4_rsem,CAGATC_N_MC2E_33_rsem,CGATGT_M7_33_2_rsem,ACAGTG_M7_33_3_rsem,GCCAAT_N_MC2C_33_rsem
awk -v OFS=\t '{print $7}' /dfs3/wpoon/wpoon/hpc-concatenation-mapping-master/fastq4R179test/ATGTCA_N_TCW1KO2/ATGTCA_N_TCW1KO2_rsem.rsem.genes.results > /dfs3/wpoon/wpoon/hpc-concatenation-mapping-master/fastq4R179test/ATGTCA_N_TCW1KO2/ATGTCA_N_TCW1KO2.fpkm
awk -v OFS=\t '{print $5}' /dfs3/wpoon/wpoon/hpc-concatenation-mapping-master/fastq4R179test/ATGTCA_N_TCW1KO2/ATGTCA_N_TCW1KO2_rsem.rsem.genes.results > /dfs3/wpoon/wpoon/hpc-concatenation-mapping-master/fastq4R179test/ATGTCA_N_TCW1KO2/ATGTCA_N_TCW1KO2.counts
awk -v OFS=\t '{print $7}' /dfs3/wpoon/wpoon/hpc-concatenation-mapping-master/fastq4R179test/GTGAAA_N_TCW1KO4/GTGAAA_N_TCW1KO4_rsem.rsem.genes.results > /dfs3/wpoon/wpoon/hpc-concatenation-mapping-master/fastq4R179test/GTGAAA_N_TCW1KO4/GTGAAA_N_TCW1KO4.fpkm
awk -v OFS=\t '{print $5}' /dfs3/wpoon/wpoon/hpc-concatenation-mapping-master/fastq4R179test/GTGAAA_N_TCW1KO4/GTGAAA_N_TCW1KO4_rsem.rsem.genes.results > /dfs3/wpoon/wpoon/hpc-concatenation-mapping-master/fastq4R179test/GTGAAA_N_TCW1KO4/GTGAAA_N_TCW1KO4.counts
awk -v OFS=\t '{print $7}' /dfs3/wpoon/wpoon/hpc-concatenation-mapping-master/fastq4R179test/CAGATC_N_MC2E_33/CAGATC_N_MC2E_33_rsem.rsem.genes.results > /dfs3/wpoon/wpoon/hpc-concatenation-mapping-master/fastq4R179test/CAGATC_N_MC2E_33/CAGATC_N_MC2E_33.fpkm
awk -v OFS=\t '{print $5}' /dfs3/wpoon/wpoon/hpc-concatenation-mapping-master/fastq4R179test/CAGATC_N_MC2E_33/CAGATC_N_MC2E_33_rsem.rsem.genes.results > /dfs3/wpoon/wpoon/hpc-concatenation-mapping-master/fastq4R179test/CAGATC_N_MC2E_33/CAGATC_N_MC2E_33.counts
awk -v OFS=\t '{print $7}' /dfs3/wpoon/wpoon/hpc-concatenation-mapping-master/fastq4R179test/CGATGT_M7_33_2/CGATGT_M7_33_2_rsem.rsem.genes.results > /dfs3/wpoon/wpoon/hpc-concatenation-mapping-master/fastq4R179test/CGATGT_M7_33_2/CGATGT_M7_33_2.fpkm
awk -v OFS=\t '{print $5}' /dfs3/wpoon/wpoon/hpc-concatenation-mapping-master/fastq4R179test/CGATGT_M7_33_2/CGATGT_M7_33_2_rsem.rsem.genes.results > /dfs3/wpoon/wpoon/hpc-concatenation-mapping-master/fastq4R179test/CGATGT_M7_33_2/CGATGT_M7_33_2.counts
awk -v OFS=\t '{print $7}' /dfs3/wpoon/wpoon/hpc-concatenation-mapping-master/fastq4R179test/ACAGTG_M7_33_3/ACAGTG_M7_33_3_rsem.rsem.genes.results > /dfs3/wpoon/wpoon/hpc-concatenation-mapping-master/fastq4R179test/ACAGTG_M7_33_3/ACAGTG_M7_33_3.fpkm
awk -v OFS=\t '{print $5}' /dfs3/wpoon/wpoon/hpc-concatenation-mapping-master/fastq4R179test/ACAGTG_M7_33_3/ACAGTG_M7_33_3_rsem.rsem.genes.results > /dfs3/wpoon/wpoon/hpc-concatenation-mapping-master/fastq4R179test/ACAGTG_M7_33_3/ACAGTG_M7_33_3.counts
awk -v OFS=\t '{print $7}' /dfs3/wpoon/wpoon/hpc-concatenation-mapping-master/fastq4R179test/GCCAAT_N_MC2C_33/GCCAAT_N_MC2C_33_rsem.rsem.genes.results > /dfs3/wpoon/wpoon/hpc-concatenation-mapping-master/fastq4R179test/GCCAAT_N_MC2C_33/GCCAAT_N_MC2C_33.fpkm
awk -v OFS=\t '{print $5}' /dfs3/wpoon/wpoon/hpc-concatenation-mapping-master/fastq4R179test/GCCAAT_N_MC2C_33/GCCAAT_N_MC2C_33_rsem.rsem.genes.results > /dfs3/wpoon/wpoon/hpc-concatenation-mapping-master/fastq4R179test/GCCAAT_N_MC2C_33/GCCAAT_N_MC2C_33.counts
