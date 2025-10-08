#!/usr/bin/env bash


{ head -n 1 $1; 
  line=$(tail -n 1 $1)
  for i in $(seq 1 100000); do
    echo "$line"
  done
} > out.csv
