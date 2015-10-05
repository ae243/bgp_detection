# script to determine the number of sessions that see update to prefix p
# usage: python sessions_with_prefix_update.py <splitted_update_directory> <result_file>
# output format: <prefix> <# sessions that see update to prefix> <total sessions> <fraction of sessions that see update to prefix>

import os
import sys
import datetime

from ipaddr import IPv4Address, IPv4Network

from os import listdir
from os.path import isfile, join

from collections import defaultdict

def process_file(total_sessions, sessions_map, file_name, result_file_handle):
    fi = open(file_name, 'r')
    print "Processing "+file_name
    for line in fi:
        splitted_line = line.split("|")
        collector = splitted_line[0]
        timestamp = int(splitted_line[2])
        update_type = splitted_line[3]
        session = splitted_line[4]
        prefix = IPv4Network(splitted_line[6])
        ID = collector+"_"+session
        if update_type == "A":
            if prefix in sessions_map:
                if not ID in sessions_map[prefix]:
                    sessions_map[prefix].append(ID)
            else:
                sessions_map[prefix] = [ID]
            if not ID in total_sessions:
                total_sessions.append(ID)
    fi.close()
    return [total_sessions, sessions_map]

if len(sys.argv) < 3:
	print "Error: missing arguments."
	print "Usage: python "+ sys.argv[0] +"<splitted_update_directory> <result_file>"
	sys.exit(-1)

splitted_updates_dir = sys.argv[1]
splitted_update_files = [ f for f in listdir(splitted_updates_dir) if isfile(join(splitted_updates_dir,f)) and f.startswith('splitted_update_') and f.endswith('txt')]
splitted_update_files.sort()

result_file = sys.argv[2]
res_file = open(result_file, 'w')

num_sessions = {}
sess_list = []
for splitted_update_file in splitted_update_files:
    f_name = join(splitted_updates_dir, splitted_update_file)
    [sess_list, num_sessions] = process_file(sess_list, num_sessions, f_name, res_file)	
    print "Finished processing "+f_name

for pref in num_sessions:
    res_file.write("%s %s %s %f\n" % (pref, len(num_sessions[pref]), len(sess_list), float(len(num_sessions[pref]))/float(len(sess_list))))

res_file.close()
