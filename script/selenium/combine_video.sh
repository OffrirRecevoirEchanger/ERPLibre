#!/usr/bin/env bash

# Get two last .webm file
videos=($(ls -t *.webm | head -n 2))

if [ ${#videos[@]} -ne 2 ]; then
    echo "Error : you need two files .webm in root directory"
    exit 1
fi

timestamp=$(date +"%Y%m%d_%H%M%S")
output_name="output_${timestamp}.webm"

echo "first video ${videos[0]}"
echo "second video ${videos[1]}"

ffmpeg -i "${videos[0]}" -i "${videos[1]}" -filter_complex "hstack=inputs=2" "${output_name}"
# with normalize size video
# ffmpeg -i video1.webm -i video2.webm -filter_complex "[0:v]scale=320:240[v0]; [1:v]scale=320:240[v1]; [v0][v1]hstack=inputs=2" output.webm

echo "${output_name}"
