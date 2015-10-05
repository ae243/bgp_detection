# bgp_detection

Heuristics to detect prefix hijacking events using BGP updates.

# organization

Scripts to calculate the heuristics are in the top level directory.  The updates/ folder contains example files of the correct format of BGP updates (used as input to the scripts).

# usage

python originator_frequency.py <updates directory> <output file>

*writes the list of prefixes that were announced at a very low frequency (< 1%) by an AS, along with the associated frequency.

python path_time.py <updates directory> <output file>

*writes the list of prefixes that were announced for very short amount of time, along with the associated amount of time.

python sessions_with_prefix_update.py <updates directory> <output file> 

*writes a list of all prefixes, the number of sessions that saw this prefix, the total number of sessions, and the fraction of sessions that saw this prefix.
