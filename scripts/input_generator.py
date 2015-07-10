#!/usr/bin/python

import sys, os, math
import random as rnd

################## tie resolution ###################
def min_val_tie(l, full_size):
    ret_val = 0.0;
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
	deficit = full_size - len(l)
	val = sum(range(len(l)+1, full_size+1))
	return float(val) / deficit

def binary_tie(l,full_size):
	return 0.0

################### rank processors ##################
def extract_union(day_lists):
	num_of_days = len(day_lists)
	record_ids = {}
	for l in day_lists:
		for record in l:
			record_ids[record] = 1
	return record_ids.keys()

def expand_data(day_lists, label_rank_computer, feature_rank_computer):
	record_union = extract_union(day_lists)
	full_size = len(record_union)
	out = []
	for i in range(len(day_lists)):
		expanded_data = dict(day_lists[i]) # copy
		if i == 0:
			tie_rank = label_rank_computer(day_lists[i], full_size)
		else:
			tie_rank = feature_rank_computer(day_lists[i], full_size)
		for record in record_union:
			if record not in day_lists[i]:
				expanded_data[record] = tie_rank
		out.append(expanded_data)
	return out

def extract_feature_list(expanded_day_lists):
	current = expanded_day_lists[0] # it contains the labels
	feature_list = {}
	for record in current:
		feature_list[record] = []
		for i in range(1,len(expanded_day_lists)): # contains days backwards ([1] position is previous day)
			feature_list[record].append(expanded_day_lists[i][record])
	return current, feature_list

################### writers ##########################
def write_record(record_id, record_features):
	l = len(record_features)
	out = str(record_id) + ' qid:1'
	for i in range(l):
		out += (' ' + str(i+1) + ':' + str(record_features[i]))
	return (out + '\n')

def write_to_file(file_path, label_dict, feature_dicts):
	f = open(file_path, 'w')
	l = len(label_dict)
	order = range(l)
	rnd.shuffle(order) # this way learning to rank cannot use order of labels
	key_list = label_dict.keys()
	for i in order:
		f.write(write_record(label_dict[key_list[i]], feature_lists[key_list[i]]))
	f.close()

##################### pre-processors ###########################
def pre_proc(input_folder ,day, top_cut, is_label, label_rank_type, feature_rank_type):
    # input files (e.g.: *.txt_s) are ordered according to centrality scores
    file = open(input_folder + '/pagerank_scores_' + str(day) + '.txt_s')
    ret_val = {}
    ret_sort = []
    counter = 0
    for line in file:
    	if top_cut == -1 or counter < top_cut:
        	splitted = line[:-1].split(" ")
        	ret_val[int(splitted[0])] = float(splitted[1])
        	ret_sort.append(int(splitted[0]))
        	counter += 1
        else:
        	break

    rank_type = ''
    if is_label:
    	rank_type = label_rank_type
    else:
    	rank_type = feature_rank_type

    ret_val_out = {}
    if rank_type == 'binary':
    	print '[binary ranking was chosen]'
    	for i in ret_val:
    		ret_val_out[i] = 1.0
    elif rank_type == 'position':
    	print '[position based ranking was chosen]'
    	ret_val_out = centrality_to_position(ret_val, ret_sort)
    elif rank_type == 'centrality':
    	print '[centrality based ranking was chosen]'
    	ret_val_out = ret_val
    else:
    	print 'ERROR: ' + rank_type + ' ranking is not implemented! Choose from "centrality/position/binary".'
    return ret_val_out

def centrality_to_position(ret_val, ret_sort):
    ret_pos_val = {}
    summed_rank = 0.0
    i = 0
    j = 1
    N = len(ret_sort)
    for j in range(1,N+1):
        summed_rank += j
        if j == N or ret_val[ret_sort[j-1]] > ret_val[ret_sort[j]]:
            for k in range(i,j):
                ret_pos_val[ret_sort[k]] = summed_rank / (j-i)
            i = j
            summed_rank = 0.0
    return ret_pos_val

##################### main ############################
if __name__ == "__main__":
	if len(sys.argv) == 8:
		data_folder = sys.argv[1]
		label_rank_type = sys.argv[2] # centrality/position/binary
		feature_rank_type = sys.argv[3] # centrality/position/binary
		top_cut = int(sys.argv[4]) # default 10, all: -1
		from_interval_id = int(sys.argv[5])
		to_interval_id = int(sys.argv[6]) # this interval is the target
		output = sys.argv[7]

		day_lists = []
		for i in reversed(range(from_interval_id, to_interval_id+1)):
			day_lists.append(pre_proc(data_folder,i, top_cut, (i==to_interval_id), label_rank_type, feature_rank_type))
		#print day_lists
		
		label_ranker = ''
		if label_rank_type == 'binary':
			label_ranker = binary_tie
		elif label_rank_type == 'position':
			label_ranker = average_tie
		elif label_rank_type == 'centrality':
			label_ranker = min_val_tie
		else:
			print 'ERROR: ' + rank_type + ' ranking is not implemented! Choose from "centrality/position/binary".'

		feature_ranker = ''
		if feature_rank_type == 'binary':
			feature_ranker = binary_tie
		elif feature_rank_type == 'position':
			feature_ranker = average_tie
		elif feature_rank_type == 'centrality':
			feature_ranker = min_val_tie
		else:
			print 'ERROR: ' + rank_type + ' ranking is not implemented! Choose from "centrality/position/binary".'
		
		expanded_data = expand_data(day_lists, label_ranker, feature_ranker)
		#print expanded_data
		label_list, feature_lists = extract_feature_list(expanded_data)
		#print label_list
		#print feature_lists

		write_to_file(output, label_list, feature_lists)

	else:
		print 'Usage: <data_folder> <feature_rank_type> <label_rank_type> <top_k/-1> <from> <to> <output>'