#!/bin/bash

file_in="$1"
out_dir=$2
mkdir -p ${out_dir}

ln -s "${file_in}" tmp$$.mp4
echo ${file_in} > ${out_dir}/frame_source.log
ffmpeg -i tmp$$.mp4 -filter:v "select='gt(scene,0.3)',showinfo,crop=277:20:575:460" -vsync 0 ${out_dir}/%05d.png 2>&1 | tee ${out_dir}/frame_sd.log

rm tmp$$.mp4 
echo "c'mmon devil. WISH ME LUCK"

python ./steamed_labels.py ${out_dir}

echo "Praise Artemis"
