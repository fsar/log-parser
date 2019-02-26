#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 16:07:47 2019

@author: franckrobert
"""

import sys
import csv
import re

def import_tsv(file):
#input: tsv in file path
#return: list of lists (Log lines without timestamp)

    with open(file, encoding = 'utf-8') as tsvfile:
        
        log = []
        logReader = csv.reader(tsvfile, delimiter='\t')
        
        for line in logReader:
            
            # Checks if the 'tuile the plan' is present
            if len(line) > 1:
                log.append(line[1])

    return log

def parse_line(log):
#:input: list of lists (Log file imported)
#:return: list of tuples (Tuples of viewmode and zoom)
    
    log_parsed = []
    pattern = '/map/1\.0/slab/([^/]*)/256/([^/]*)/*'
    
    for line in log:
        
        matches = re.search(pattern, line)
        
        # Doesn't append if the regex search returned nothing. (None)
        if matches: 
            log_parsed.append(matches.groups())
        
    return log_parsed


def aggregate_data(log_parsed):
#:input: list of tuples (Tuples of viewmode and zoom)
#:return: list of lits (Aggregated data)

    data = []
    
    for tup in log_parsed:
        
        # Checks if the name of the current (tup) viewmode == the viewmode
        # in the latest data entry. Append the zoom as a set
        if not data or data[-1][0] != tup[0]:
            data.append([tup[0], 1, {tup[1]}])
            
        # If not, add the current viewmode as a new entry in the list data
        # Increment its count and add the zoom to the set. (unique value)
        else:
            data[-1][1] += 1
            data[-1][2].add(tup[1])

    return data  


def export_tsv(data, file):
#:input: data = list of lists (Aggregated data). file: tsv out file path.
#:return: None
    
    with open(file, 'w', newline='', encoding = 'utf-8') as tsvfile:
        
        tsvwriter = csv.writer(tsvfile, delimiter='\t')
        
        for tsv_row in data:
            
            tsv_row[2] = ",".join(str(i) for i in tsv_row[2])
            tsvwriter.writerow(tsv_row)
                
    return None


if __name__ == '__main__':
    
    # Checks if the script is called with the log file to parse as an argument
    if len(sys.argv) == 1:
        print('Missing argument: log file path')
    else: 
        
        # Import the log file
        tsv_file_in = sys.argv[1]
        log = import_tsv(tsv_file_in)
        
        # Parsing the log lines
        log_parsed = parse_line(log)
        
        # Aggregating the data
        data = aggregate_data(log_parsed)
        
        # Export the aggregated log file
        tsv_file_out = tsv_file_in + '.out'
        export_tsv(data, tsv_file_out)