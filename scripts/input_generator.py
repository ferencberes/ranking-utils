#!/usr/bin/python

import sys, os, math

def min_val_tie(l, full_size):
    ret_val = 0;
    first = True
    for i in l:
        num = l[i]
        if first:
            ret_val = num
            first = False
        if ret_val > num:
            ret_val = num
    return ret_val - 1 # not the minimum value is returned!

def average_tie(l,full_size):
	print full_size, len(l)
	print l
	deficit = full_size - len(l)
	val = sum(range(len(l)+1, full_size+1))
	return float(val) / deficit

def extract_union(day_lists):
	num_of_days = len(day_lists)
	record_ids = {}
	for l in day_lists:
		for record in l:
			record_ids[record] = 1
	return record_ids.keys()

def expand_data(day_lists, rank_computer):
	record_union = extract_union(day_lists)
	full_size = len(record_union)
	out = []
	print day_lists
	for l in day_lists:
		expanded_data = dict(l) # copy
		tie_rank = rank_computer(l, full_size)
		for record in record_union:
			if record not in l:
				expanded_data[record] = tie_rank
		out.append(expanded_data)
	return out


if __name__ == "__main__":
	print "hello!"