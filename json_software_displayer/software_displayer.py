import json
import os
import matplotlib.pyplot as plt
import pandas as pd

def json_parser_csv(data_path):
    def solo_json_reader(file_name, data_path):
        absolute_path = os.path.abspath(data_path + "/" + file_name)

        with open(absolute_path, 'r') as file:
            data = json.load(file)

        return data
    def list_files(directory):
        json_files = [f for f in os.listdir(directory) if
                      f.endswith('.json') and os.path.isfile(os.path.join(directory, f))]
        return json_files


    list_json_files = list_files(data_path)

    mentions_count = {}
    json_file_old = None

    for json_file in list_json_files:
        data = solo_json_reader(json_file, data_path)
        for software_mention in data.get("mentions"):
            if software_mention["software-type"] == "software":
                software_name = software_mention["software-name"]["normalizedForm"]
                if software_name in mentions_count:
                    mentions_count[software_name][0] += 1
                else:
                    mentions_count[software_name] = [1, 1]

                if json_file != json_file_old:
                    mentions_count[software_name][1] += 1
                    json_file_old = json_file

    counts = []
    documents = []

    software_names = list(mentions_count.keys())
    for count_doc, doc in list(mentions_count.values()):
        counts.append(count_doc)
        documents.append(doc)

    data = {}
    data['software'] = software_names
    data['counts'] = counts
    data['document'] = documents

    df = pd.DataFrame(data)

    df_sorted = df.sort_values(by='counts', ascending=False)

    df_sorted.to_csv(f'./result/CSV_software/mentions_{len(counts)}_sorted.csv', index=False)

    print(f"'mentions_{len(counts)}_sorted.csv' was created")

