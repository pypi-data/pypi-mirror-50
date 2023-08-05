#!/usr/bin/env python
import subprocess
import argparse

def main():
	ap = argparse.ArgumentParser()
	ap.add_argument("-d", "--directory", required=True, help="Path to directory with BAM files")
	ap.add_argument("-s", "--samples", required=True, help="Path to directory containing all samples' BAM files")
	ap.add_argument("-c", "--control", required=True, help="Path to control BAM file")
	ap.add_argument("-r", "--reference", required=True, help="Path to reference genome")
	ap.add_argument("-j", "--threads", type=int, default=10, help="Number of threads (Default: 10)")
	ap.add_argument("-m", "--minScore", type=float, default=0.1, help="Minimum score for CM to be included (Default: 0.1) ")
	ap.add_argument("-u", "--uniqueStarts", type=int, default=3, help="Minimum number of unique starting positions for mutation - those with less will be removed (Default: 3)")
	ap.add_argument("-v", "--variantRate", type=float, default=0.1, help="Variants occurring above this rate are treated as true variants in the control (Default=0.1)")
	args = vars(ap.parse_args())

	table = args["directory"] + "ScoreTable.tsv"
	tableFIO = table.replace(".tsv", "_afterFIO.tsv")
	outputIGV = args["directory"] +"IGV"
	IGVSnap = outputIGV + "/snapshots/"
	IGVSessions = outputIGV + "/sessions/"

	# create directories for IGV output
	subprocess.call(["mkdir", outputIGV])
	subprocess.call(["mkdir", outputIGV + "/snapshots"])
	subprocess.call(["mkdir", outputIGV + "/sessions"])

	# call scripts
	subprocess.call(['python', '-m', 'findDupAndLinked', '-d', args["directory"], '-c', args["control"] , '-t', str(args["threads"]), '-u', str(args["uniqueStarts"]), '-v', str(args["variantRate"])])
	subprocess.call(['python', '-m','detectFIO', '-d', args["directory"], '-s', args["samples"], '-t', table, '-m', str(args["minScore"]), '-u', str(args["uniqueStarts"])])
	subprocess.call(['python', '-m','IGVSessions', '-d', args["directory"], '-c', args["control"],  '-s', args["samples"], '-t', tableFIO, '-r', args["reference"], '-o', IGVSessions])
	subprocess.call(['python', '-m','snapshotIGV', '-d', args["directory"], '-t', tableFIO, '-r', args["reference"], '-o', IGVSnap])

main()






