import os
import requests
import time
from tqdm import tqdm
import csv

def is_file_in_directory(directory, filename_list, type):
    original_len = len(filename_list)
    for filename in filename_list:
        filename_name = filename.replace('https://hal.science/','')
        file_path = os.path.join(directory, filename_name + type)
        if os.path.exists(file_path):
            print(file_path)
            filename_list.remove(filename)
    print(f'{original_len} -> {len(filename_list)}')
    return filename_list


def fetch_uris(year, file_type):
    list_uri = []
    list_types_uris = {}
    base_url = "https://api.archives-ouvertes.fr/"
    endpoint = "search"
    collection = "INRIA2"
    params = {
        "q": f"producedDateY_i:{year} AND domain_s:0.info AND (submitType_s:file OR annex)",
        "fl": "uri_s, fulltext_t",
        "fq": f"docType_s:{file_type}",
        "wt": "json",
        "rows": 5  # You can adjust the number of rows per request
    }

    response = requests.get(f"{base_url}{endpoint}/{collection}", params=params)

    #print(f"Status Code for URIS: {response.status_code}")
    #print(response.json())

    data = response.json()
    uris = [doc["uri_s"] for doc in data.get("response", {}).get("docs", [])]
    if len(uris) != 0:
        for single_uris in tqdm(uris, desc=file_type, colour="blue"):
            time.sleep(0.1)
            list_uri.append(single_uris)
        list_types_uris[file_type] = list_uri
        return list_types_uris


def download_pdf_by_id(type_uris_dic):
    # Create the 'downloads' directory if it doesn't exist
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    error = 0

    # Extract the first key and its corresponding value
    type_str = next(iter(type_uris_dic.keys()))
    uris_list = next(iter(type_uris_dic.values()))

    # Create a subdirectory for the specific type
    download_directory = os.path.join('downloads', type_str)
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)

    uris_list = is_file_in_directory('downloads/SV22_pdf', uris_list, '.SV22_pdf')

    for uris_id in tqdm(uris_list):
        time.sleep(0.1)
        # Construct the full URL using the provided ID
        pdf_url = f'{uris_id}/tei'

        # Send an HTTP GET request to the PDF URL
        try:
            response = requests.get(pdf_url)
            response.raise_for_status()  # Raise an exception for bad responses

            # Extract the filename from the URL
            filename = os.path.join(download_directory, os.path.basename(uris_id) + '.SV22_pdf')

            # Save the PDF content to a local file
            with open(filename, 'wb') as pdf_file:
                pdf_file.write(response.content)

            # Print information about the downloaded file
            # print(f"{uris_id} downloaded successfully. Size: {file_size_mb} bytes")
        except Exception as e:
            try:
                pdf_url = pdf_url.replace('hal.science', 'inria.hal.science')
                response = requests.get(pdf_url)
                response.raise_for_status()  # Raise an exception for bad responses

                # Extract the filename from the URL
                filename = os.path.join(download_directory, os.path.basename(uris_id) + '.SV22_pdf')

                # Save the PDF content to a local file
                with open(filename, 'wb') as pdf_file:
                    pdf_file.write(response.content)

                # Print information about the downloaded file
                # print(f"{uris_id} downloaded successfully. Size: {file_size_mb} bytes")
            except Exception as e:
                error += 1
                print(f"Error for {pdf_url}: {e}")
    print(error)

def download_by_id(uris_list,type):
    # Create the 'downloads' directory if it doesn't exist
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    error = 0
    # Create a subdirectory for the specific type
    download_directory = os.path.join('downloads', type)
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)

    for uris_id in tqdm(uris_list):
        time.sleep(0.1)
        # Construct the full URL using the provided ID
        url = f'https://inria.hal.science/{uris_id}/document'

        # Send an HTTP GET request to the PDF URL
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad responses

            # Extract the filename from the URL
            filename = os.path.join(download_directory, os.path.basename(uris_id) + '.' + type)

            # Save the PDF content to a local file
            with open(filename, 'wb') as file:
                file.write(response.content)

            # Get the size of the downloaded file
            file_size_bytes = os.path.getsize(filename)
            file_size_mb = file_size_bytes / (1024 * 1024)

            # Print information about the downloaded file
            #print(f"{uris_id} downloaded successfully. Size: {file_size_mb} bytes")
        except Exception as e:
            try:
                url = url.replace('hal.science','inria.hal.science')
                response = requests.get(url)
                response.raise_for_status()  # Raise an exception for bad responses

                # Extract the filename from the URL
                filename = os.path.join(download_directory, os.path.basename(uris_id) + '.' + type)

                # Save the PDF content to a local file
                with open(filename, 'wb') as file:
                    file.write(response.content)

                # Get the size of the downloaded file
                file_size_bytes = os.path.getsize(filename)
                file_size_mb = file_size_bytes / (1024 * 1024)

                # Print information about the downloaded file
                # print(f"{uris_id} downloaded successfully. Size: {file_size_mb} bytes")
            except Exception as e:
                error += 1
                print(f"Error for {url}: {e}")
    print(error)

def downloader_halid(csv_path):
    with open(csv_path, 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        list_of_csv = []
        for uris in list(csv_reader):
            list_of_csv.append(uris[0])
        download_by_id(list_of_csv, 'pdf')