import logging
import json
import sys
from bs4 import BeautifulSoup
import string
import re
from fuzzywuzzy import fuzz

logging.basicConfig(filename='dif_checker.log', encoding='utf-8', level=logging.DEBUG, filemode='w', format='%(levelname)s-%(message)s')


# Define a function to remove punctuation from a word
def remove_punctuation(word):
    # Define characters to be excluded from the word
    excluded_characters = string.punctuation.replace("-", "")
    # Create a translation table to remove specified characters
    translator = str.maketrans("", "", excluded_characters)
    # Use translation table to remove punctuation from the word
    cleaned_word = word.translate(translator)
    return cleaned_word


# Define a function to check if a list is a sublist of another list
def is_sublist(main_list, sublist):
    # Iterate through the main list to find the sublist
    for i in range(len(main_list) - len(sublist) + 1):
        # Check if the sublist is found in the main list
        if main_list[i:i + len(sublist)] == sublist:
            return [i, len(sublist)]  # Return the starting index and length of the sublist
    return -1  # Return -1 if sublist is not found in the main list


# Define a function to enhance a JSON file with information from an XML file
def xml_enhance_json(xml_path, json_path):

    # Read and parse the XML file
    with open(xml_path, 'r', encoding='utf-8') as xml_file:
        xml_content = xml_file.read()  # Read the content of the XML file
        xml_content = BeautifulSoup(xml_content, "xml")  # Parse the XML content using BeautifulSoup
        xml_content_p = xml_content.find_all("p")  # Find all "p" tags in the XML content

    # Read the JSON file
    with open(json_path, 'r') as json_file:
        data_json = json.load(json_file)  # Load JSON data from the file

    # Create an empty list to store results
    software_list_result = []

    # Iterate over software mentions in the JSON file
    soft_found_re = 0
    soft_found_fu = 0

    for software_mention in data_json.get("mentions"):
        # Check if the software mention is of type "software"
        if software_mention["software-type"] == "software":

            # Extract and preprocess software name from the JSON
            software_name = software_mention["software-name"]["rawForm"]
            software_name = software_name.replace("\n", " ")  # Replace newline characters with spaces

            # Extract and preprocess software context from the JSON
            software_context = software_mention["context"]

            # Check if software name is in the lowercased and cleaned context list
            pattern = software_context

            # Escape special characters in the pattern
            escaped_pattern = re.escape(pattern)

            # Create a dictionary to store information about the software
            software_dict = {"software_name": software_name, "pattern_found": False, "founder": ""}

            for tag in xml_content_p:
                if re.search(escaped_pattern, tag.text):
                    software_dict["pattern_found"] = True
                    software_dict["founder"] = 're.search'
                    similarity_score = fuzz.token_set_ratio(tag.text.lower(),software_name.lower())
                    if similarity_score == 100:
                        print(software_name)
                        soft_found_re += 1

                        break # Stop searching once the pattern is found
                else:
                    similarity_score = fuzz.partial_ratio(tag.text.lower(), escaped_pattern.lower())
                    if similarity_score >= 80:
                        software_dict["founder"] = 'fuzzy'
                        soft_found_fu += 1
                        software_dict["pattern_found"] = True
                        #print(f"for this pattern: '{escaped_pattern}' \nthe similarity is : {similarity_score} ")
                        break

            # Append the software information dictionary to the result list
            software_list_result.append(software_dict)

    # Count the number of successes and failures and log the results
    with open(xml_path, 'w', encoding='utf-8') as output_xml_file:
        output_xml_file.write(str(xml_content.prettify()))

    success = 0
    failure = 0
    for result in software_list_result:
        if not result["pattern_found"]:
            failure += 1
            logging.critical({'software_name':result['software_name'],'pattern':pattern})
        else:
            logging.debug(result)
            success += 1
    print(f"For {len(data_json.get('mentions'))} software in the json we found :\nwith re.search: {soft_found_re} \nwith fuzzy : {soft_found_fu}\nwe failed to catch : {failure}")