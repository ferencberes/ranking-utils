#!/bin/bash -eu

data_folder="$1"
top_value="$2"
num_of_queries="$3"
num_of_features="$4"
first_interval=$5
last_interval=$6
output_folder="$7"
file_prefix="$8" 

first_test_interval=$(($first_interval+$num_of_features+$num_of_queries))
#echo "$first_test_interval"

thisDir="$(dirname $0)"
thisDir="$(readlink -f "$thisDir")"

echo "top_value: ""$top_value" > "$output_folder"/info.txt
echo "num_of_queries: ""$num_of_queries" >> "$output_folder"/info.txt
echo "num_of_features: ""$num_of_features" >> "$output_folder"/info.txt
echo "first_interval: ""$first_interval" >> "$output_folder"/info.txt
echo "last_interval: ""$last_interval" >> "$output_folder"/info.txt
echo "output_folder: ""$output_folder" >> "$output_folder"/info.txt
echo "file_prefix: ""$file_prefix" >> "$output_folder"/info.txt

pushd "$thisDir"
echo "Generating inputs STARTED."
for i in $(eval echo "{$first_test_interval..$last_interval}"); do
	mkdir -p "$output_folder"/"$i"
	./generate_input_with_multiple_rank_type.sh "$data_folder" "$top_value" "$num_of_queries" "$num_of_features" "$i" "$output_folder"/"$i" "$file_prefix"_"$i" & 
done
wait
echo "Generating inputs FINISHED."
popd