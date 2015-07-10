#!/usr/bin/python

import sys, os, math

sys.path.insert(1, os.path.join(sys.path[0], '../scripts'))
import input_generator as ig

epsilon = 0.0001

day_curr = {1:0.5, 2:0.4, 3:0.35, 4:0.21}
day_m1 = {2:0.6, 4:0.35, 1:0.31, 5:0.11}
day_m2 = {4:0.65, 2:0.44, 5:0.25, 1:0.11, 6:0.05}
day_lists = [day_curr, day_m1, day_m2]

def test_extract_union():
	record_union = ig.extract_union(day_lists)
	assert len(record_union) == 6
	for i in range(1,7):
		assert True == (i in record_union)

def test_expand_data_minval():
	res = ig.expand_data(day_lists, ig.min_val_tie, ig.min_val_tie)
	# check size
	for l in res:
		assert 6 == len(l)
	# check appended values
	assert abs(res[0][5] + 0.79) < epsilon
	assert abs(res[0][6] + 0.79) < epsilon
	assert abs(res[1][3] + 0.89) < epsilon
	assert abs(res[1][6] + 0.89) < epsilon
	assert abs(res[2][3] + 0.95) < epsilon

def test_expand_data_avg():
	res = ig.expand_data(day_lists, ig.average_tie, ig.average_tie)
	# check size
	for l in res:
		assert 6 == len(l)
	# check appended values
	assert abs(res[0][5] - 5.5) < epsilon
	assert abs(res[0][6] - 5.5) < epsilon
	assert abs(res[1][3] - 5.5) < epsilon
	assert abs(res[1][6] - 5.5) < epsilon
	assert abs(res[2][3] - 6) < epsilon

def test_extract_feature_list():
	res = ig.expand_data(day_lists, ig.min_val_tie, ig.min_val_tie)
	label_list, feature_list = ig.extract_feature_list(res)
	# check size
	for i in feature_list:
		assert len(feature_list[i]) == 2
	# check labels
	assert label_list[1] == 0.5
	assert label_list[2] == 0.4
	assert label_list[3] == 0.35
	assert label_list[4] == 0.21
	assert label_list[5] == -0.79
	assert label_list[6] == -0.79
	# check features  
	assert feature_list[1][0] == 0.31
	assert feature_list[1][1] == 0.11
	assert feature_list[2][0] == 0.6
	assert feature_list[2][1] == 0.44
	assert feature_list[3][0] == -0.89
	assert feature_list[3][1] == -0.95
	assert feature_list[4][0] == 0.35
	assert feature_list[4][1] == 0.65
	assert feature_list[5][0] == 0.11
	assert feature_list[5][1] == 0.25
	assert feature_list[6][0] == -0.89
	assert feature_list[6][1] == 0.05
