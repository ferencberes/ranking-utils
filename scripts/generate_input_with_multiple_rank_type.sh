#!/bin/bash -eu

data_folder="$1"
from_interval="$2"
to_interval="$3"
top_value="$4"
output_prefix="$5"

thisDir="$(dirname $0)"
thisDir="$(readlink -f "$thisDir")"

pushd "$thisDir"
echo "Generating inputs STARTED."
for label_rank_type in {"centrality","position","binary"}; do
	for feature_rank_type in {"centrality","position"}; do
		outfile="$output_prefix"_"$feature_rank_type"_"$label_rank_type".txt
		python input_generator.py "$data_folder" "$feature_rank_type" "$label_rank_type" "$top_value" "$from_interval" "$to_interval" "$outfile" 
	done;
done;
echo "Generating inputs FINISHED."
popd
