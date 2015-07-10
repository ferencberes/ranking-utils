#!/usr/bin/python

import sys, os, math
sys.path.insert(1, os.path.join(sys.path[0], '../scripts'))
import input_generator as ig

ret_val = {4:0.54, 1:0.33, 0:0.2, 3:0.11, 2:0.08}
ret_sort = [4,1,0,3,2]

def test_centrality_to_position_without_ties():
	pos_map = ig.centrality_to_position(ret_val, ret_sort)
	assert pos_map[4] == 1.0
	assert pos_map[1] == 2.0
	assert pos_map[0] == 3.0
	assert pos_map[3] == 4.0
	assert pos_map[2] == 5.0

ret_val_ties = {4:0.54, 1:0.3, 0:0.3, 3:0.2, 2:0.2, 5:0.11}
ret_sort_ties = [4,1,0,3,2,5]

def test_centrality_to_position_with_ties():
	pos_map = ig.centrality_to_position(ret_val_ties, ret_sort_ties)
	assert pos_map[4] == 1.0
	assert pos_map[1] == 2.5
	assert pos_map[0] == 2.5
	assert pos_map[3] == 4.5
	assert pos_map[2] == 4.5
	assert pos_map[5] == 6.0
