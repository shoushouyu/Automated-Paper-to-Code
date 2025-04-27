#!/usr/bin/env bash



set -e  

python3 content_process/picture.py && \
python3 content_process/md_process.py && \        
python3  design/cot_eng.py &&\
python3 design/class_design.py &&\


echo "All scripts executed successfully."
