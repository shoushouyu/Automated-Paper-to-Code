#!/usr/bin/env bash



set -e  

python3 content_process/picture.py && \
python3 content_process/md_process.py && \        
python3  


echo "All scripts executed successfully."
