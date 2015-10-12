#!/usr/bin/python

import sys,os

def extract_result_of_learning(filename):
	f = open(filename, 'r')
	line_list = list(f)
	train_line = line_list[len(line_list)-3]
	test_line = line_list[len(line_list)-1]
	train_res = train_line.rstrip().split(": ")[1]
	test_res = test_line.rstrip().split(": ")[1]
	f.close()
	return [train_res, test_res]

def write_out(outfile, value_list):
    outfile.write(str(value_list[0]))
    for i in value_list[1:]:
        outfile.write(" "+ str(i))
    outfile.write("\n")

if __name__ == "__main__":
	argc = len(sys.argv)
	if argc == 8:
		# tudjuk hogy nincs ures nap a tanitasban. Erre nem kell kulon figyelni
		ranklib_results_dir = sys.argv[1]
		dataset_prefix = sys.argv[2]
		feature_rank_type = sys.argv[3]
		label_rank_type = sys.argv[4]
		metric_t = sys.argv[5]
		from_interval = int(sys.argv[5])
		to_interval = int(sys.argv[6])
		output_file = sys.argv[7]
		out_f = open(output_file, 'w')

		print "Collecting ranklib results STARTED."
		for i in range(from_interval, to_interval+1):
			interval_file = ranklib_results_dir + "/" + str(i) + "/" + dataset_prefix + "_" + str(i) + "_" + rank_type_prefix + "_" + metric_t_prefix + ".out"
			out_list = [str(i)] + extract_result_of_learning(interval_file)
			write_out(out_f, out_list)
		out_f.close()
		print "Collecting ranklib results FINISHED."
	else:
		print "Usage: <ranklib_results_dir> <dataset_prefix> <feature_rank_type> <label_rank_type> <metric_t> <metric_T> <from_interval> <to_interval> <output_file>"

