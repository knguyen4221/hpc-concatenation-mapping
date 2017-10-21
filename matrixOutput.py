import os
import shutil
import subprocess
import time
import sys



def main():
	fastqDir = sys.argv[0]
	outputFile = sys.argv[1]
	matrixOutput("counts", fastqDir, outputFile)

def matrixOutput(fpkmCount, fastqDir, outputFile):
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
	with open("fullMatrix/{}.counts".format(outputFile), 'w') as outfile:
		subprocess.call(['paste', '--delimiters=,'] + line.split(), stdout=outfile)
				

if __name__ == "__main__":
	main()
