#!/usr/bin/python

import sys, os
import input_generator as ig

def name_generator(file_prefix, top_k, num_of_features, from_interval_id, to_interval_id, enable_unseen):
	print (file_prefix + '_k' + str(top_k) + '_f' + str(num_of_features) + '_from' + str(from_interval_id) + "_to" + str(to_interval_id))
	return (file_prefix + '_k' + str(top_k) + '_f' + str(num_of_features) + '_from' + str(from_interval_id) + "_to" + str(to_interval_id) + "_unseen" + str(enable_unseen))

if __name__ == "__main__":
	if len(sys.argv) == 11:
		data_folder = sys.argv[1]
		feature_rank_type = sys.argv[2] # centrality/position/binary
		label_rank_type = sys.argv[3] # centrality/position/binary
		top_cut = int(sys.argv[4]) # default 10, all: -1
		num_of_features = int(sys.argv[5])
		from_interval_id = int(sys.argv[6])
		to_interval_id = int(sys.argv[7])
		enable_unseen = ("True"==sys.argv[8])
		output_folder = sys.argv[9]
		file_prefix = sys.argv[10]
		feature_ranker, label_ranker = ig.set_rankers(feature_rank_type, label_rank_type)
		
		if not os.path.exists(output_folder):
					os.makedirs(output_folder)

		# extract test data
		f_out = open(output_folder + '/' + name_generator(file_prefix, top_cut, num_of_features, from_interval_id, to_interval_id, enable_unseen) + ".txt", 'w')
		for i in range(from_interval_id,to_interval_id + 1):	
			to_id = i
			from_id = i - num_of_features
			#print from_id, to_id
			ig.extract_data(data_folder, top_cut, feature_ranker, label_ranker, feature_rank_type, label_rank_type, from_id, to_id, i, f_out, enable_unseen)
		f_out.close()

	else:
		print 'Usage: <data_folder> <feature_rank_type> <label_rank_type> <top_k/-1> <num_of_features> <from_interval> <to_interval> <enable_unseen> <output_folder> <file_prefix>'