import re
import sys
import os
import signal
import time
import constants
from collections import defaultdict
from subprocess import Popen
from subprocess import call


class Concatenation:

    def __init__(self, inputFile):
        self._regexReadsGroupName = "reads"
        self._regexLaneGroupName = "lane"
        self._regexSequenceGroupName = "sequence"

        # grabbing information from config file
        try:
            with open(inputFile, 'r') as infile:
                self._experimentNumber = infile.readline().strip()
                self._toBeConcatenated = infile.readline().strip()
                self._concatenationOutput = infile.readline().strip()
                self._sampleNameFile = infile.readline().strip()
                self._matrixOutput = infile.readline().strip()
                self._csvToTxtGzRegex = infile.readline().strip()

            self._matched_barcodes, self._maxReads = self._make_dict()
            self._sampleNameDict = readInSampleNames(self._sampleNameFile)
        except FileNotFoundError:
            raise FileNotFoundError("Couldn't find {0)".format(inputFile))
        except EOFError:
            raise EOFError("You're missing lines from {0)".format(inputFile))

    def _validateRegex(self, regexString):
        matchErrors = []

        if (not self.hasNamedCapturedGroup(self._regexLaneGroupName)):
            matchErrors.append(self._regexLaneGroupName)
        if (not self.hasNamedCapturedGroup(self._regexReadsGroupName)):
            matchErrors.append(self._regexReadsGroupName)
        if (not self.hasNamedCapturedGroup(self._regexSequenceGroupName)):
            matchErrors.append(self._regexSequenceGroupName)

        if len(matchErrors) > 0:
            raise Exception(
                "Missing named capturing groups: {}".format(matchErrors))

        return

    def hasNamedCapturedGroup(self, groupName):
        namedGroupFormat1 = "?P<{0}>"
        namedGroupFormat2 = "?P'{0}'"
        return namedGroupFormat1.format(groupName) in self._csvToTxtGzRegex and namedGroupFormat2.format(groupName) in self._csvToTxtGzRegex

    def _make_dict(self):
        matched_barcodes = defaultdict(lambda: defaultdict(dict))
        maxReads = 0

        for filename in os.listdir(os.getcwd() + "/" + self._toBeConcatenated.strip()):
            obj = re.match(self._csvToTxtGzRegex, filename)

            maxReads = int(obj.group(self._regexReadsGroupName) if maxReads < int(
                obj.group(self._regexReadsGroupName)) else maxReads)

            matched_barcodes[obj.group(self._regexSequenceGroupName)][obj.group(
                self._regexReadsGroupName)][obj.group(self._regexLaneGroupName)[1:]] = filename
        # print(matched_barcodes)
        return (matched_barcodes, maxReads)

    def run_concat(self):
        cmd = []
        try:
            for sequence in self._sampleNameDict:
                for lane in self._sampleNameDict[sequence]:
                    if not os.path.exists(self._concatenationOutput + "/" + sequence+"_"+lane[0]):
                        os.mkdir(self._concatenationOutput +
                                 "/"+sequence+"_"+lane[0])
                    sampleName = sequence+"_"+lane[0]
                    for read in range(1, self._maxReads+1):
                        final = "cat"
                        for i in lane[1].split(","):
                            #print( sequence,read,i)
                            final += " {0}/{1}/{2}".format(os.getcwd(
                            ), self._toBeConcatenated, self._matched_barcodes[sequence][str(read)][str(i)])
                        final += " > {0}/{1}/{2}/{3}-READ{4}.fastq.gz".format(
                            os.getcwd(), self._concatenationOutput, sampleName, sampleName, str(read))
                        cmd.append(final)

            self._addToConcat(cmd)
            self._writeToMappingInput()
            call(['qsub', '-q', constants.Constants.CLUSTER, 'concat.sh'])
        except KeyError:
            raise KeyError("sequence({0}) read({1}) lane({2}) existed in {3} but not {4}".format(
                sequence, str(read), str(i), self._sampleNameFile, self._toBeConcatenated))

    def _addToConcat(self, cmd):
        try:
            f = open('{0}/concat.sh'.format(os.getcwd()), 'w')
            f.write("#! /bin/bash\n#$ -N CONCAT\n#$ -q {0}\n#$ -t 1-".format(constants.Constants.CLUSTER) +
                    str(len(cmd))+"\n")
            for command in cmd:
                f.write(command+"\n")
        except OSError as e:
            raise FileNotFoundError("Could not write to concat.sh", e)
        finally:
            f.close()

    def _writeToMappingInput(self):
        try:
            with open("{0}/mappingInput.txt".format(os.getcwd()), 'w') as outfile:
                outfile.write("{0}/{1}\n".format(os.getcwd(),
                                                 self._concatenationOutput))
                outfile.write("{0}\n".format(self._maxReads))
                outfile.write("{0}\n".format(self._matrixOutput))
                outfile.write("true\n")
                outfile.write("true\n")
                outfile.write("true\n")
        except OSError:
            raise OSError("Could not write to mappingInput.txt")


def readInSampleNames(fileName):
    infile = open(fileName, 'r')
    sampleNameDict = defaultdict(list)
    counter = 0
    for line in infile:
        if counter == 0:
            counter += 1
            continue
        temp = line.strip().split(",")
        temp[1] = temp[1].replace(" ", "_")
        temp[3] = temp[3].replace(";", ",")
        sampleNameDict[temp[2]].append((temp[1], temp[3]))
    infile.close()
    return sampleNameDict
