import re
import sys
import os
import signal
import time
from collections import defaultdict
from subprocess import Popen
from subprocess import call


class Concatenation:
    def __init__(self, inputFile):
        with open(inputFile, 'r') as infile:
            self._experimentNumber = infile.readline().strip()
            self._toBeConcatenated = infile.readline().strip()
            self._concatenationOutput = infile.readline().strip()
            self._sampleNameFile = infile.readline().strip()
        self._matched_barcodes, self._maxReads = self._make_dict()
        self._sampleNameDict = readInSampleNames(self._sampleNameFile)

    def _make_dict(self):
        matched_barcodes = defaultdict(lambda : defaultdict(dict))
        maxReads = 0
        for filename in os.listdir(os.getcwd()+ "/"+ self._toBeConcatenated.strip()):
            obj = re.match(r'[A-Z0-9]+-(L[0-9]*)-(P[0-9]*-([G|C|A|T]{6})-READ([0-9]))-(Sequences\.txt\.gz)', filename)
            maxReads = int(obj.group(4) if maxReads < int(obj.group(4)) else maxReads)
            #group 3 = sequence
            #group 4 = reads
            #group 1 = lane
            matched_barcodes[obj.group(3)][obj.group(4)][obj.group(1)[1:]] = filename
        print(matched_barcodes)
        return (matched_barcodes, maxReads)

    def run_concat(self):
        cmd = []          
        for sequence in self._sampleNameDict:
            for lane in self._sampleNameDict[sequence]:
                if not os.path.exists(self._concatenationOutput + "/" + sequence+"_"+lane[0]):
                    call(["mkdir", self._concatenationOutput+"/"+sequence+"_"+lane[0]])
                sampleName = sequence+"_"+lane[0]
                for read in range(1, self._maxReads+1):
                    final = "cat"
                    for i in lane[1].split(","):
                    	print( sequence,read,i)
                        final += " {0}/{1}/{2}".format(os.getcwd(),self._toBeConcatenated, self._matched_barcodes[sequence][str(read)][str(i)])
                    final += "> {0}/{1}/{2}/{3}-READ{4}.fastq.gz".format(os.getcwd(),self._concatenationOutput, sampleName, sampleName, str(read))
                    cmd.append(final)
        f = open('{0}/concat.sh'.format(os.getcwd()), 'w')
        f.write("#! /bin/bash\n#$ -N CONCAT\n#$ -q bio\n#$ -t 1-"+str(len(cmd))+"\n")
        for command in cmd:
            f.write(command+"\n")
        f.close()
        with open("{0}/mappingInput.txt".format(os.getcwd()), 'w') as outfile:
            outfile.write("{0}/{1}".format(os.getcwd(),self._concatenationOutput))
        #call(['qsub', '-q', 'bio','/dfs1/wpoon/kenqn/concat.sh'])
     


def readInSampleNames(fileName):
    infile = open(fileName, 'r')
    sampleNameDict = defaultdict(list)
    counter = 0
    for line in infile:
        if counter == 0:
            counter+=1
            continue
        temp = line.strip().split(",")
        temp[1] = temp[1].replace(" ", "_")
        temp[3] = temp[3].replace(";", ",")
        sampleNameDict[temp[2]].append((temp[1], temp[3]))
    infile.close()
    return sampleNameDict
