#!/bin/sh

body_json="host.json"
if [ ! -f "$body_json" ]; then
  echo Error: $body_json not found, run _get_host.bat first!
  exit 1
fi

curl -X POST http://localhost:8000/add_host -H "Content-Type: application/json" --data-binary @"$body_json" -o add_host.json
