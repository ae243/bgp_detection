# get the frequency of originator ASes - return any that are below a threshold of 1% of the total updates
# usage: python originator_frequency.py <splitted_update_directory> <result_file>"

import os
import sys
import datetime

from ipaddr import IPv4Address, IPv4Network

from os import listdir
from os.path import isfile, join

from collections import defaultdict

def process_file(file_name, result_file_handle):
    fi = open(file_name, 'r')
    print "Processing "+file_name
    frequencies = {}
    processed = 0
    for line in fi:
        splitted_line = line.split("|")
        collector = splitted_line[0]
        timestamp = int(splitted_line[2])
        update_type = splitted_line[3]
        prefix = IPv4Network(splitted_line[6])
        if not prefix == IPv4Network("0.0.0.0/1"):
            if update_type == "A":
                try:
                    as_path = [int(elem) for elem in splitted_line[7].split()]
                    if as_path[-1] in frequencies:
                        prefix_count_list = frequencies[as_path[-1]]
                        updated = False
                        for tup in prefix_count_list:
                            if tup[0] == prefix:
                                tup[1] += 1
                                updated = True
                                break
                        if updated == False:
                            prefix_count_list.append([prefix, 1])
                    else:
                        frequencies[as_path[-1]] = [[prefix, 1]]
                    processed += 1
                except ValueError:
                    print "The last element of the path is not formatted correctly."
    fi.close()
    for orig in frequencies:
        for pref in frequencies[orig]:
            if float(pref[1])/float(processed) <= .01:
                result_file_handle.write("%s %s %s %f\n" % (file_name.lstrip('/splitted_update_').rstrip('.txt'), orig, pref[0], float(pref[1])/float(processed)))

if len(sys.argv) < 3:
	print "Error: missing arguments."
	print "Usage: python "+ sys.argv[0] +"<splitted_update_directory> <result_file>"
	sys.exit(-1)

splitted_updates_dir = sys.argv[1]
splitted_update_files = [ f for f in listdir(splitted_updates_dir) if isfile(join(splitted_updates_dir,f)) and f.startswith('splitted_update_') and f.endswith('txt')]
splitted_update_files.sort()

result_file = sys.argv[2]
res_file = open(result_file, 'w')

for splitted_update_file in splitted_update_files:
    f_name = join(splitted_updates_dir, splitted_update_file)
    process_file(f_name, res_file)	
    print "Finished processing "+f_name

res_file.close()
