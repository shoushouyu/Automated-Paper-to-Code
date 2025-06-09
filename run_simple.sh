#!/usr/bin/env bash



set -e  

python3 content_process/picture.py && \      
python3  design/cot_eng.py &&\
python3 design/class_design.py &&\
python3 code_gen/merge.py &&\
python3 code_gen/last_modified.py &&\
python3 code_gen/code_generate.py &&\


echo "All scripts executed successfully."
