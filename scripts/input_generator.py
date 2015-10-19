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
	out_val = 0.0
	if deficit != 0:
		out_val = float(val) / deficit
	return out_val

def set_zero(l,full_size):
	return 0.0

################### rank processors ##################
def extract_unions(day_lists):
	num_of_days = len(day_lists)
	record_ids_all = {}
	record_ids_except_label = {}
	first = True
	for l in day_lists:
		for record in l:
			record_ids_all[record] = 1
			if not first:
				record_ids_except_label[record] = 1 # contains records that occurred in feature days as well!
		first = False
	return [record_ids_all.keys(), record_ids_except_label.keys()] 

def expand_data(day_lists, label_rank_computer, feature_rank_computer, is_for_train):
	[record_union_all, record_union_prev] = extract_unions(day_lists)
	out = []
	if not is_for_train: # for test file: all kind of records are present
		full_size = len(record_union_all)
		for i in range(len(day_lists)):
			expanded_data = dict(day_lists[i]) # copy
			if i == 0:
				tie_rank = label_rank_computer(day_lists[i], full_size) # do rank computation with label computer
			else:
				tie_rank = feature_rank_computer(day_lists[i], full_size) # do rank computation with feature computer
			for record in record_union_all:
				if record not in day_lists[i]: # set tie_rank for records at the end of the list (only present because of union!)
					expanded_data[record] = tie_rank
			out.append(expanded_data)
	else: # for train file: only records of feature days are present
		full_size = len(record_union_prev)
		for i in range(len(day_lists)):	
			if i == 0:
				expanded_data = {}
				for v_id in day_lists[0]:
					if v_id in record_union_prev:
						expanded_data[v_id] = day_lists[0][v_id]
				tie_rank = label_rank_computer(expanded_data, full_size)
			else:
				expanded_data = dict(day_lists[i]) # copy
				tie_rank = feature_rank_computer(day_lists[i], full_size)
			for record in record_union_prev:
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

################### writers ##########################
def write_record(record_id, label, record_features, query_id):
	l = len(record_features)
	out = str(label) + ' qid:' + str(query_id)
	for i in range(l):
		out += (' ' + str(i+1) + ':' + str(record_features[i]))
	return (out + ' # ' + str(record_id) + '\n')

def write_to_file(f, label_dict, feature_dicts, query_id):
	l = len(label_dict)
	order = range(l)
	#rnd.shuffle(order) # this way learning to rank cannot use order of labels # random ordering switched off!!!
	key_list = label_dict.keys()
	for i in order:
		f.write(write_record(key_list[i], label_dict[key_list[i]], feature_dicts[key_list[i]], query_id))

##################### main ############################

def set_rankers(feature_rank_type, label_rank_type):
	label_ranker = ''
	if label_rank_type == 'binary':
		label_ranker = set_zero
	elif label_rank_type == 'position':
		label_ranker = average_tie
	elif label_rank_type == 'centrality':
		label_ranker = set_zero #min_val_tie
	else:
		print 'ERROR: ' + rank_type + ' ranking is not implemented! Choose from "centrality/position/binary".'

	feature_ranker = ''
	if feature_rank_type == 'binary':
		feature_ranker = set_zero
	elif feature_rank_type == 'position':
		feature_ranker = average_tie
	elif feature_rank_type == 'centrality':
		feature_ranker = set_zero #min_val_tie
	else:
		print 'ERROR: ' + rank_type + ' ranking is not implemented! Choose from "centrality/position/binary".'
	return feature_ranker, label_ranker

def extract_data(data_folder, top_cut, feature_ranker, label_ranker, feature_rank_type, label_rank_type, from_interval_id, to_interval_id, query_id, out_file, is_for_train):
	day_lists = []
	for i in reversed(range(from_interval_id, to_interval_id+1)):
		day_lists.append(pre_proc(data_folder,i, top_cut, (i==to_interval_id), label_rank_type, feature_rank_type))
	#print day_lists
	expanded_data = expand_data(day_lists, label_ranker, feature_ranker, is_for_train)
	#print expanded_data
	label_list, feature_lists = extract_feature_list(expanded_data)
	#print label_list
	#print feature_lists
	write_to_file(out_file, label_list, feature_lists, query_id)

def name_generator(file_prefix, top_k, num_of_features, train_query_num, test_query_num):
	return (file_prefix + '_k' + str(top_k) + '_f' + str(num_of_features) + '_tr' + str(train_query_num) + "_te" + str(test_query_num))

if __name__ == "__main__":
	if len(sys.argv) == 11:
		data_folder = sys.argv[1]
		feature_rank_type = sys.argv[2] # centrality/position/binary
		label_rank_type = sys.argv[3] # centrality/position/binary
		top_cut = int(sys.argv[4]) # default 10, all: -1
		num_of_features = int(sys.argv[5])
		train_query_num = int(sys.argv[6])
		test_query_num = int(sys.argv[7])
		test_interval_id = int(sys.argv[8]) # this interval is the target
		output_folder = sys.argv[9]
		file_prefix = sys.argv[10]
		feature_ranker, label_ranker = set_rankers(feature_rank_type, label_rank_type)
		
		if not os.path.exists(output_folder):
					os.makedirs(output_folder)

		# extract test data
		f_test = open(output_folder + '/' + name_generator(file_prefix, top_cut, num_of_features, train_query_num, test_query_num) + ".test", 'w')
		for i in range(0,test_query_num):	
			to_interval_id = test_interval_id + i
			from_interval_id = to_interval_id - num_of_features
			extract_data(data_folder, top_cut, feature_ranker, label_ranker, feature_rank_type, label_rank_type, from_interval_id, to_interval_id, i+1, f_test, False)
		f_test.close()

		# extract train data
		f_train = open(output_folder + '/' + name_generator(file_prefix, top_cut, num_of_features, train_query_num, test_query_num) + ".train", 'w')
		for i in range(1,train_query_num + 1):
			to_interval_id = test_interval_id - i
			from_interval_id = to_interval_id - num_of_features
			extract_data(data_folder, top_cut, feature_ranker, label_ranker, feature_rank_type, label_rank_type, from_interval_id, to_interval_id, i, f_train, True)
		f_train.close()

	else:
		print 'Usage: <data_folder> <feature_rank_type> <label_rank_type> <top_k/-1> <num_of_features> <train_query_num> <test_query_num> <test_interval_id> <output_folder> <file_prefix>'

		