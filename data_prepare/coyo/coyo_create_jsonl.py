# import json
# from tqdm import tqdm

# all_data = {}

# n = 5314716

# i = 0

# with open("/datadisk/mmc4/mmc4-core-ff/all.jsonl") as f:
#     for line in tqdm(f, total=n):
#         data = json.loads(line)
#         source_jsonl = data["meta"]["source_jsonl"].split("/")[1]
#         ori_meta = data["meta"]["ori_meta"]

#         if source_jsonl in all_data:
#             all_data[source_jsonl].append(ori_meta)
#         else:
#             all_data[source_jsonl] = [ori_meta]

#         i += 1

# for source_jsonl in tqdm(all_data):
#     with open("/datadisk/mmc4/mmc4-core-ff/" + source_jsonl, 'w') as outfile:
#         for entry in all_data[source_jsonl]:
#             json.dump(entry, outfile)
#             outfile.write('\n')

import json
from tqdm import tqdm
import glob
import csv

filename = "/home/neel/coyo_long_captions/coyo_long_captions.csv"
filename2 = "/home/neel/coyo_long_captions/coyo_long_captions.jsonl"
total = 25082143

data = []

with open(filename2, 'w') as outfile:
    with open(filename) as file:
        reader = csv.reader(file)
        header = next(reader)
        for line in tqdm(reader, total=total):
            row = {}
            for h, v in zip(header, line):
                row[h] = v

            json.dump(row, outfile)
            outfile.write('\n')
        