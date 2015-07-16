#!/usr/bin/python

import sys,os

def preproc_file(filename, col, from_interval, to_interval):
	f = open(filename, 'r')
	out_map = {}
	for line in f:
		splitted = line.rstrip().split(" ")
		interval_id = int(splitted[0])
		if from_interval <= interval_id and interval_id <= to_interval:
			out_map[interval_id] = splitted[col]
		else:
			continue
	f.close()
	return out_map


def write_out(outfile, value_list):
    outfile.write(str(value_list[0]))
    for i in value_list[1:]:
        outfile.write(" "+ str(i))
    outfile.write("\n")

if __name__ == "__main__":
	print "Usage: <from_interval> <to_interval> <output_file> <data_file_1>  <col_1>  <data_file_2>  <col_2> ..."
	from_interval = int(sys.argv[1])
	to_interval = int(sys.argv[2])
	output_folder = sys.argv[3]
	if not os.path.exists(output_folder):
		os.makedirs(output_folder)

	argc = len(sys.argv)
	num_of_files = (argc - 4) / 2
	file_list = []
	col_list = []

	print "Combining results STARTED"
	info_f = open(output_folder+'/info.txt', 'w')
	for i in range(0, num_of_files):
		info_line = [sys.argv[2*i+4], sys.argv[2*i+5]]
		write_out(info_f, info_line)
		file_list.append(sys.argv[2*i+4])
		col_list.append(int(sys.argv[2*i+5]))
	info_f.close()

	#print num_of_files
	#print file_list
	#print col_list	

	extracted_data = []
	for i in range(0, num_of_files):
		extracted_data.append(preproc_file(file_list[i], col_list[i], from_interval, to_interval))

	#print extracted_data

	out_f = open(output_folder+'/results.txt', 'w')
	for i in range(from_interval, to_interval+1):
		out_list = [i]
		for j in range(0, num_of_files):
			out_list.append(extracted_data[j][i])
		write_out(out_f, out_list)
	out_f.close()
	print "Combining results FINISHED"
