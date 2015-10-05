# script to determine total time a path was advertised for each AS
# usage: python path_time.py <splitted_update_directory> <result_file>

import os
import sys
import datetime

from ipaddr import IPv4Address, IPv4Network

from os import listdir
from os.path import isfile, join

from collections import defaultdict

def process_file(session_times, path_times, file_name, result_file_handle):
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
        key = ID+"~"+str(prefix)
        if not prefix == IPv4Network("0.0.0.0/1"):
            if update_type == "A":
                if key in path_times:
                    updated = False
                    temp_times_list = path_times[key]
                    if not len(temp_times_list[-1]) == 2:
                        (temp_times_list[-1]).append(timestamp)
                    temp_times_list.append([timestamp])
                    if len(session_times[ID]) == 2:
                        start_time = session_times[ID][1]
                        del session_times[ID][1]
                        new_time = timestamp - start_time
                        session_times[ID][0] += new_time
                        session_times[ID].append(timestamp)
                    else:
                        session_times[ID].append(timestamp)
                else:
                    if ID in session_times:
                        if len(session_times[ID]) == 2:
                            start_time = session_times[ID][1]
                            del session_times[ID][1]
                            new_time = timestamp - start_time
                            session_times[ID][0] += new_time
                            session_times[ID].append(timestamp)
                        else:
                            session_times[ID].append(timestamp)
                    else:
                        session_times[ID] = [0, timestamp]
                    path_times[key] = [[timestamp]]
            else:
                if key in path_times:
                    temp_times_list = path_times[key]
                    if not len(temp_times_list[-1]) == 2:
                        (temp_times_list[-1]).append(timestamp)
                if ID in session_times:
                    if len(session_times[ID]) == 2:
                        start_time = session_times[ID][1]
                        del session_times[ID][1]
                        new_time = timestamp - start_time
                        session_times[ID][0] += new_time
    fi.close()
    return [session_times, path_times]

if len(sys.argv) < 3:
	print "Error: missing arguments."
	print "Usage: python "+ sys.argv[0] +"<splitted_update_directory> <result_file>"
	sys.exit(-1)

splitted_updates_dir = sys.argv[1]
splitted_update_files = [ f for f in listdir(splitted_updates_dir) if isfile(join(splitted_updates_dir,f)) and f.startswith('splitted_update_') and f.endswith('txt')]
splitted_update_files.sort()

result_file = sys.argv[2]
res_file = open(result_file, 'w')

path_times = {}
sess_times = {}
for splitted_update_file in splitted_update_files:
    f_name = join(splitted_updates_dir, splitted_update_file)
    [sess_times, path_times] = process_file(sess_times, path_times, f_name, res_file)
    print "Finished processing "+f_name

prefix_map = {}
for path in path_times:
    temp_times_list = path_times[path]
    total_time = 0
    for t in temp_times_list:
        if len(t) == 2:
            total_time += (t[1] - t[0])
    ID = path.split("~")[0]
    prefix = path.split("~")[1]
    if prefix in prefix_map:
        prefix_map[prefix].append((ID, total_time))
    else:
        prefix_map[prefix] = [(ID, total_time)]
    
for p in prefix_map:
    temp_list = []
    for p2 in prefix_map[p]:
        ID = p2[0]
        total_time = p2[1]
        if sess_times[ID][0] != 0:
            if float(total_time)/float(sess_times[ID][0]) <= .01:
                temp_list.append((ID, total_time, float(total_time)/float(sess_times[ID][0])))
    if len(temp_list) > 0:
        res_file.write("%s %s\n" % (p, temp_list))
res_file.close()
