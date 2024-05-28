#!/bin/sh

curl -X POST http://localhost:8000/test_account -H "Content-Type: application/json" --data-binary @"account.json" -o test_account.txt
