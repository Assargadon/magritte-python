#!/bin/sh

curl -X POST http://localhost:8000/test_user -H "Content-Type: application/json" --data-binary @"user.json" -o test_user.txt
