#!/bin/bash -eu

input_folder="$1"
file_prefix="$2"
label_rank_type="$3"
feature_rank_type="$4" 
from_interval=$5
to_interval=$6
metric="$7"
output_folder="$8"

thisDir="$(dirname $0)"
thisDir="$(readlink -f "$thisDir")"

pushd "$thisDir"
echo "Running experiments STARTED."
cd ..
for i in $(eval echo "{$from_interval..$to_interval}"); do
	train_file_name="$input_folder"/"$i"/"$file_prefix"_"$i"_"$feature_rank_type"_"$label_rank_type".train
	test_file_name="$input_folder"/"$i"/"$file_prefix"_"$i"_"$feature_rank_type"_"$label_rank_type".test
	mkdir -p "$output_folder"/"$i"
	output_file="$output_folder"/"$i"/"$file_prefix"_"$i"_"$feature_rank_type"_"$label_rank_type"_"$metric".out
	# ranker 4 is Coordinate Ascent
	java -jar trunk/bin/RankLib.jar -train "$train_file_name" -test "$test_file_name" -ranker 4 -metric2t "$metric" -metric2T "$metric" > "$output_file" &
done
wait
echo "Running Experiments FINISHED."
popd