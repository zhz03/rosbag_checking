#!/bin/bash

input_directory="./"  # Input directory containing checked rosbag files
output_directory="./rosbag_info_txt"   # Output directory for txt files

# Create output directory if it doesn't exist
mkdir -p "$output_directory"

# Iterate through rosbag files in the input directory
for bag_path in "$input_directory"/*.bag; do
    # Extract rosbag file name (without path)
    bag_filename=$(basename "$bag_path")
    # Construct output txt file path
    output_path="$output_directory/${bag_filename%.bag}.txt"
    
    # Use rosbag info command to get information and save output to txt file
    rosbag info "$bag_path" > "$output_path"
done

echo "Info files have been generated for all rosbag files."


