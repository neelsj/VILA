import os
from datasets import load_dataset
from tqdm import tqdm
import json
import sys 
import glob 
import csv

input_path = "/home/neel/data/"
out_path = "/datadisk/data/checked"

#json_out = "/home/neel/src/VILA/data_prepare/jsons.txt"

#dirs = os.listdir(input_path)

# with open(json_out,"w") as f:

#     jsons_files = []
#     for dir in dirs:
#         for file in glob.iglob(os.path.join(input_path, dir, "**/*.json*"), recursive=True):
#             print(file)
#             jsons_files.append(file)

#             f.write(file) 
#             f.write("\n")
#             f.flush()

json_out = "/home/neel/src/VILA/data_prepare/jsons_selected.txt"
json_stats = "/home/neel/src/VILA/data_prepare/jsons_selected_good.jsonl"
json_stats_csv = "/home/neel/src/VILA/data_prepare/jsons_selected_good.csv"

with open(json_out,"r") as f:
    jsons_selected =  f.read().splitlines()

# jsons_selected = jsons_selected[8:]

# llava_cc3m_pretrain-595k:
#     _target_: llava.data.LLaVADataset
#     data_path: /data/LLaVA-CC3M-Pretrain-595K/chat.json
#     media_dir: /data/LLaVA-CC3M-Pretrain-595K/images

total_total = 0
for json_file in tqdm(jsons_selected):
    with open(json_file, 'r') as file:
        data = json.load(file)

    total_total += len(data)

progress = tqdm(total=total_total)

total_good = 0

with open(json_stats_csv,"w") as csvfile:
    csvwriter = csv.writer(csvfile)

    with open(json_stats,"w") as statsfile:
        all_json_data = []
        
        for jj, json_file in enumerate(jsons_selected):
            try:  

                with open(json_file, 'r') as file:
                    data = json.load(file)

                json_file_dir = os.path.dirname(json_file)
                dirs = [a for a in os.listdir(json_file_dir) if os.path.isdir(os.path.join(json_file_dir, a))]

                image_folder = json_file_dir

                if "images" in dirs and "allava_vflan" not in json_file:
                    image_folder = os.path.join(image_folder, "images")

                good_data = []

                i = 0
                for json_data in data:
                    if "image" in json_data and json_data["image"] is not None:

                        filename = os.path.join(image_folder, json_data["image"])

                        path = os.path.dirname(filename)
                        if os.path.exists(filename):
                            good_data.append(json_data)
                        # else:
                        #     print(f"image {filename} is missing")
                    else:
                        good_data.append(json_data) 

                    i += 1
                    progress.update(1)

                    # if i >= 10:
                    #     break

                json_file_out = json_file.replace(".json", "_good.json")

                with open(json_file_out, 'w') as outfile:
                    json.dump(good_data, outfile, indent=4, ensure_ascii=False)

                json_data_out = {}
                json_data_out["name"] = os.path.basename(json_file_dir)
                json_data_out["data_path"] = json_file_out
                json_data_out["media_dir"] = image_folder
                json_data_out["count_good"] = len(good_data)
                json_data_out["total"] = len(data)
                json_data_out["percent_found"] = 100*len(good_data)/len(data)

                total_good += len(good_data)

                if len(good_data) == 0:
                    print(f"{json_file_out}\t{len(good_data)}")

                json_object = json.dumps(json_data_out)
                statsfile.write(json_object + "\n")
                
                if jj == 0:
                    csvwriter.writerow(json_data_out.keys())

                csvwriter.writerow(json_data_out.values())

            except Exception as e:
                print(e)


print(f"total good {total_good}")
print(f"total {total_total}")