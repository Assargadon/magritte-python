#!/bin/bash

for file in accessors/*Test.py
do
  if [ -f "$file" ]; then
    echo "Running $file"
    python3 -m unittest "$file"
  fi
done

for file in *Test.py
do
  if [ -f "$file" ]; then
    echo "Running $file"
    python3 -m unittest "$file"
  fi
done
