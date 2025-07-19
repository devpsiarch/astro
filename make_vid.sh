#!/bin/bash 
plot_dump_dir="plots"

ffmpeg -framerate 24 -pattern_type glob -i "${plot_dump_dir}/*.png" -c:v libx264 -pix_fmt yuv420p output.mp4
