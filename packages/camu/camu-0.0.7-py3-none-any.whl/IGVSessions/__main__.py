#!/usr/bin/env python
import glob
import argparse


ap = argparse.ArgumentParser()
ap.add_argument("-d", "--directory", required=True, help="Path to directory with BAM files")
ap.add_argument("-r", "--reference", required=True, help="Path to reference genome")
ap.add_argument("-t", "--table", required=True, help="Path to result score table after detectFIO.py")
ap.add_argument("-s", "--samples", required=True, help="Path to directory with samples BAM files")
ap.add_argument("-c", "--control", required=True, help="Path to control BAM file")
ap.add_argument("-o", "--outputDirectory", required=True, help="Path to directory for IGV Snapshots")
args = vars(ap.parse_args())

refFile = args["reference"]
filterTable = args["table"]
bamFolder = args["directory"]
sessionDir = args["outputDirectory"]
samplesDir = args["samples"]
control = args["control"]

samples = glob.glob(samplesDir + "*.bam")


pathNameList = list()
with open(filterTable, "r") as nameFile:
    # skip header
    nameFile.readline()
    for line in nameFile:
        name = line.split("\t")[0]
        pathNameList.append((bamFolder + name, name))

for path, name in pathNameList:
    locus = name.split(".", 1)[1].replace(".bam", "")
    sessionPath = sessionDir + locus + ".xml"
    CMPath = path

    session = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
    session += '<Session genome="' + refFile + '" hasGeneTrack="false" hasSequenceTrack="true" locus="' + locus + '" path="' + sessionPath + '" version="8">\n'
    session += '    <Resources>\n        <Resource path="' + CMPath + '"/>\n'
    session += '        <Resource path="' + control + '"/>\n'
    for sample in samples:
        session += '        <Resource path="' + sample + '"/>\n'

    session += '    </Resources>\n    <HiddenAttributes>\n        <Attribute name="DATA FILE"/>\n' \
               '        <Attribute name="DATA TYPE"/>\n        <Attribute name="NAME"/>\n' \
               '    </HiddenAttributes>\n</Session>'

    with open(sessionPath, "w") as out:
        out.write(session)

