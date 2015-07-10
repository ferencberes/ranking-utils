#!/usr/bin/python

import math, sys
import random as rnd
import input_generator as ig

# this scripts can generate input for ranklib
# TODO: meg erdemes lenne ezt megnezni: a 0.05 illetve 0.1-es eltolast novelni stb.

def sample_ratio_lin(x, n):
	return float(x) / n + 0.05

def sample_ratio_sq(x, n):
	return float(math.pow(x,2)) / math.pow(n, 2) + 0.1

def generate_day_for_feature(day, current_list, f):
	n = len(current_list)
	index_list = range(0,n)
	selected_index = rnd.sample(index_list, int(math.ceil(f(day, n) * n)))
	#print math.ceil(f(day, n) * n)
	selected = []
	out = []
	for i in range(0, n):
		if i not in selected_index:
			out.append(current_list[i])
		else:
			selected.append(current_list[i])
	rnd.shuffle(selected)
	out += selected
	out_indexes = [0] * n
	for i in range(0,n):
		out_indexes[out[i]-1] = i+1
	return [out, out_indexes]

def generate_feature_vectors(n, perm_lists):
	out = []
	l = len(perm_lists)
	for i in range(n):
		f_list = []
		for j in range(l):
			f_list.append(perm_lists[j][i])
		out.append(f_list)
	return out

if __name__ == "__main__":
	if len(sys.argv) == 4:
		item_num = int(sys.argv[1])
		feature_num = int(sys.argv[2])
		output_prefix = sys.argv[3] # with file path
		ranked_list = range(1, item_num + 1)
		lin_generated = []
		sq_generated = []

		print 'current: ' + str(ranked_list)
		for i in range(1, feature_num + 1):
			lin_generated.append(generate_day_for_feature(i, ranked_list, sample_ratio_lin)[1])
			sq_generated.append(generate_day_for_feature(i, ranked_list, sample_ratio_sq)[1])
		
		lin_feature_lists = generate_feature_vectors(item_num, lin_generated)
		sq_feature_lists = generate_feature_vectors(item_num, sq_generated)

		ig.write_to_file(output_prefix+'lin_gen.data', ranked_list, lin_feature_lists)
		ig.write_to_file(output_prefix+'sq_gen.data', ranked_list, sq_feature_lists)

		print lin_generated
		print lin_feature_lists
		print
		print sq_generated
		print sq_feature_lists

	else:
		print 'Usage: <item_num> <feature_num> <output_prefix>'