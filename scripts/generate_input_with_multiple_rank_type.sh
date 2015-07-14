#!/bin/bash -eu

data_folder="$1"
top_value="$2"
num_of_queries="$3"
num_of_features="$4"
test_interval_id="$5"
output_folder="$6"
file_prefix="$7" 

thisDir="$(dirname $0)"
thisDir="$(readlink -f "$thisDir")"

pushd "$thisDir"
echo "Generating inputs STARTED."
for label_rank_type in {"centrality","position","binary"}; do
	for feature_rank_type in {"centrality","position"}; do
		full_prefix="$file_prefix"_"$feature_rank_type"_"$label_rank_type"
		python input_generator.py "$data_folder" "$feature_rank_type" "$label_rank_type" "$top_value" "$num_of_queries" "$num_of_features" "$test_interval_id" "$output_folder" "$full_prefix" 
	done;
done;
echo "Generating inputs FINISHED."
popd
