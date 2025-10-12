#!/usr/bin/env bash


{ echo "ids"; 
  for i in $(seq 1 $1); do
    line=$(uuidgen)
    echo "$line"
  done
} > ids.csv
