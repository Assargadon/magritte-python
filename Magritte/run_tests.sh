#!/bin/bash
root_directory="."

find "$root_directory" -type f -name "*Test.py" | while read -r file
do
  if [ -f "$file" ]; then
    echo "Running $file"
    python3 -m unittest "$file"
  fi
done