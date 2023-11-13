#!/bin/bash
root_directory="."

find "$root_directory" -type f -name "*Test.py" | while read -r file
do
  if [ -f "$file" ]; then
    # Remove './' prefix using sed
    file_modified=$(echo "$file" | sed 's|^./||')
    echo "Running $file_modified"
    python3 -m unittest "$file_modified"
  fi
done
