#!/bin/bash
cat sam_0-50.txt | while read line; do
    read -ra newarr <<< "$line"
    axel "${newarr[1]}" --output="${newarr[0]}"
done