#!/bin/sh

body_json="index.json"
if [ ! -f "$body_json" ]; then
  echo Error: $body_json not found, run _get_index.bat first!
  exit 1
fi

curl -X POST http://localhost:8000/test -H "Content-Type: application/json" --data-binary @"$body_json" -o test.json
