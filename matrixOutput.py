import os
import shutil
import subprocess
import time
import sys



def main():
	fastqDir = sys.argv[1]
	outputFile = sys.argv[2]
	matrixOutput("counts", fastqDir, outputFile)
	matrixOutput("fpkm", fastqDir, outputFile)

def matrixOutput(fpkmCount, fastqDir, outputFile):
	line = 'genes '
	for directory in os.listdir(fastqDir):
		with open("{0}/{1}/{1}.{2}".format(fastqDir, directory, fpkmCount), 'r') as infile:
			data = infile.readlines()
		name = directory.split("_",1)
		#replaces top name of file
		try:
			data[0] = name[1] + "\n"
		except IndexError:
			data[0] = name[0] + "\n"
		with open("{0}/{1}/{1}.{2}".format(fastqDir, directory, fpkmCount), 'w') as outfile:
			outfile.writelines(data)
		line += "{0}/{1}/{1}.{2} ".format(fastqDir, directory, fpkmCount)
	with open("fullMatrix/{0}.{1}".format(outputFile, fpkmCount), 'w') as outfile:
		subprocess.call(['paste', '--delimiters=,'] + line.split(), stdout=outfile)
				

if __name__ == "__main__":
	main()
