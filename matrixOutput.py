import os
import shutil
import subprocess
import time

fastqDir = "/dfs1/wpoon/kenqn/fastq"

def main():
	matrixOutput("counts")

def matrixOutput(fpkmCount):
	line = 'genes '
	for directory in os.listdir(fastqDir):
		with open("{0}/{1}/{1}.{2}".format(fastqDir, directory, fpkmCount), 'r') as infile:
			data = infile.readlines()
		name = directory.split("_",1)
		try:
			data[0] = name[1] + "\n"
		except IndexError:
			data[0] = name[0] + "\n"
		with open("{0}/{1}/{1}.{2}".format(fastqDir, directory, fpkmCount), 'w') as outfile:
			outfile.writelines(data)
		line += "{0}/{1}/{1}.{2} ".format(fastqDir, directory, fpkmCount)
	with open("fullMatrix/matrix.counts", 'w') as outfile:
		subprocess.call(['paste', '--delimiters=,'] + line.split(), stdout=outfile)
				

if __name__ == "__main__":
	main()
