#!/bin/bash
for SHARD in {6518..13037}; do
    echo $SHARD
    python mmc4_downloader.py $SHARD $(($SHARD+1))
done
