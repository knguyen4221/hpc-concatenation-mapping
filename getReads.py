import re
import os

FASTQDIRECTORY = "/dfs3/wpoon/kenqn/fastq/"

def main():
	outfile = open("totalMappedReads.csv", 'w')
	outfile.write(',Total Reads, Unique Reads\n')

	reads = ""
	percentreads = ""

	for directory in os.listdir(FASTQDIRECTORY):
		#directory != "AGTTCC_iPS14_BMEC"
		if directory != "matrix.fpkm" and directory != "matrix.counts" and directory != "GTTTCG_iPS6_AST":
			infile = open(FASTQDIRECTORY+directory+"/star_hg38Log.final.out", 'r')
			for line in infile:
				temp =  re.match(r"Uniquely mapped reads \% \|(.*)$", line.strip())
				if temp == None:
					temp = re.match(r'Number of input reads \|(.*)$',line.strip())
					if temp == None:
						continue
					else:
						reads = temp.group(1).strip()
				else:
					percentreads = temp.group(1).strip()
					break
			infile.close()
			print(",".join([directory, reads, percentreads]))
			outfile.write(",".join([directory, reads, percentreads])+"\n")
			infile.close()
	outfile.close()


if __name__ == "__main__":
	main()
