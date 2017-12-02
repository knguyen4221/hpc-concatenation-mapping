import os
import shutil
import re
import subprocess
import time

class Mapping:
    def __init__(self, inputFileName):
        self.inputFileName = inputFileName
        with open(inputFileName, 'r') as infile:
            lines = infile.readlines()
        self.fastqDir = lines[0].strip()
	self._maxReads = lines[1].strip()
	self._matrixOuput = lines[2].strip()

    def substituteRSEM(self):
        '''Edits the rsem script so that the rsem script runs successfully on the sample
        Edits: the arguments of -N, -o and -e to its respective sample name,
        edits the gencode directory --bam star_hg38Aligned.toTranscriptome.out.bam *GENCODE_DIRECTORY*'''
        for samplename in os.listdir(self.fastqDir):
            infile = open(self.fastqDir + "/" + samplename + "/rsem.sh", "r")
            shellString = ""
            for line in infile:
                shellString += line
            infile.close()
            shellString = re.sub(r'samplename|sample', samplename+"_rsem", shellString)
            shellString = re.sub(r'star_wait', samplename+'_star', shellString)
            outfile = open(self.fastqDir+"/"+samplename+"/rsem.sh", 'w')
            outfile.write(shellString)
            outfile.close()


    def substituteSTAR(self):
        for samplename in os.listdir(self.fastqDir):
            infile = open(self.fastqDir + "/" + samplename + "/star.hg38.sh", "r")
            shellString = ""
            for line in infile:
                shellString += line
            infile.close()
            shellString = re.sub(r'samplename_star_hg38', samplename+"_star", shellString)
            readfiles = ''
            for read in range(1, int(self._maxReads)+1):
		readfiles += " {0}/{1}/{1}-READ{2}.fastq.gz".format(self.fastqDir, samplename, read)
            readfiles.strip()

            shellString = re.sub(r'\/fastqdirectory\/samplename-Read1\.fastq\.gz \/fastqdirectory\/samplename-Read2\.fastq\.gz', readfiles, shellString)
            outfile = open(self.fastqDir + "/" + samplename + "/star.hg38.sh", 'w')
            outfile.write(shellString)
            outfile.close()


    def copyShellScripts(self):
        for filename in os.listdir(self.fastqDir):
            shutil.copy("rsem.sh", self.fastqDir+"/"+filename+"/rsem.sh")
            shutil.copy("star.hg38.sh", self.fastqDir+"/"+filename+"/star.hg38.sh")



    def run_rsem_scripts(self):
        '''submits rsem.sh scripts for each sample to the bio hpc queue to be run'''
        for directory in os.listdir(self.fastqDir):
            os.chdir(self.fastqDir+"/"+directory+"/")
            subprocess.call(["qsub", "-q", "bio", self.fastqDir+"/"+directory+"/"+"rsem.sh"])

    def run_star_scripts(self):
        '''submits star.hg38.sh scripts for each sample to the bio hpc queue to be run'''
        for directory in os.listdir(self.fastqDir):
            os.chdir(self.fastqDir+"/"+directory+"/")
            subprocess.call(["qsub", "-q", "bio", self.fastqDir+"/"+directory+"/"+"star.hg38.sh"])

    def run_awk_scripts(self, fpkmCount):
        for directory in os.listdir(self.fastqDir):
            if directory != 'GTTTCG_iPS6_AST':
                #fpkm file
                fpkmOrCount = open(self.fastqDir+"/"+directory+"/"+directory+ "." + fpkmCount, "w")
                name = directory.split('_', 1)
                fpkmOrCount.write(name[1])
                fpkmOrCount.flush()
                subprocess.call(["awk", "-v", "OFS=\t", '{print $5}', self.fastqDir+"/"+directory+"/"+directory+"_rsem.rsem.genes.results"], stdout=fpkmOrCount)
                fpkmOrCount.close()
            #remove the 'fpkm' string from the header of fpkm file
                with open(self.fastqDir+"/"+directory+"/"+directory+ "." + fpkmCount, "r") as fin:
                    data = fin.readlines()  
                data[0] = name[1] + "\n"

                with open(self.fastqDir+"/"+directory+"/"+directory+ "." + fpkmCount, "w") as fin:
                    fin.writelines(data)

    def paste(self, fpkmCount):
        line = 'genes '
        for directory in os.listdir(self.fastqDir):
            #remove when whole thing is finalized
            if directory != 'GTTTCG_iPS6_AST':
                line += self.fastqDir + "/" + directory + "/" + directory + "." + fpkmCount
        matrix = open("/fullMatrix" + "/matrix." + fpkmCount, "w")
        subprocess.call(["paste", '-d,'] + line.split(), stdout=matrix)
        matrixFPKM.close()

    def reWriteShellScripts(self):
        self.substituteSTAR()
        self.substituteRSEM()

    def run_mapping(self):
        self.copyShellScripts()
        self.reWriteShellScripts()
        self.run_star_scripts()
        self.run_rsem_scripts()
        self.run_awk_scriptsV2("counts")
        self.matrixOutput("counts")


    def run_awk_scriptsV2(self):
        with open("matrix.sh", 'w') as outfile:
            outfile.write("#! /bin/bash\n")
            outfile.write("#$ -N matrixAWK\n")
            outfile.write("#$ -q bio\n")
            hold = []
            lines = ""
            for directory in os.listdir(self.fastqDir.strip()):
                hold.append(directory+"_rsem")
                lines += "awk -v OFS=\\t '{{print $7}}' {0}/{1}/{1}_rsem.rsem.genes.results > {0}/{1}/{1}.fpkm\n".format(self.fastqDir.strip(), directory)
                lines += "awk -v OFS=\\t '{{print $5}}' {0}/{1}/{1}_rsem.rsem.genes.results > {0}/{1}/{1}.counts\n".format(self.fastqDir.strip(), directory)
            outfile.write("#$ -hold_jid " + ",".join(hold) + "\n")
            outfile.write(lines)
        subprocess.call(["qsub", "-q", "bio", "matrix.sh"])

    def matrixOutput(self, fpkmCount):
	lines = []
        with open("matrixOutput.sh", 'r') as infile:
		lines = infile.readlines()
	with open("matrixOutput.sh", 'w') as outfile:
		for line in range(len(lines)):
		    if lines[line].startswith("python"):
		        lines[line] = "python matrixOutput.py {0} {1}".format(self.fastqDir, self._matrixOutput)
		outfile.write("".join(lines))
	subprocess.call(['qsub', '-q', 'bio', 'matrixOutput.sh'])
    
