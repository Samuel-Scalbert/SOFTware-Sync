import logging
import json
import sys
from bs4 import BeautifulSoup
import string
import re

logging.basicConfig(filename='logging.log', encoding='utf-8', level=logging.DEBUG, filemode='w', format='%(levelname)s-%(message)s')


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
    for software_mention in data_json.get("mentions"):
        # Check if the software mention is of type "software"
        if software_mention["software-name"]["rawForm"] == "MOD-\nELLER":

            # Extract and preprocess software name from the JSON
            software_name = software_mention["software-name"]["rawForm"]
            software_name = software_name.replace("\n", " ")  # Replace newline characters with spaces
            software_name_lower = software_name.lower()  # Convert software name to lowercase

            # Extract and preprocess software context from the JSON
            software_context = software_mention["context"]
            software_context_list = software_context.split()  # Split context into a list of words
            software_context_list_lower = [mot.lower() for mot in software_context_list]  # Convert context words to lowercase
            software_context_list_lower_cleaned = [remove_punctuation(word) for word in software_context_list_lower]  # Remove punctuation from context words

            # Check if software name is in the lowercased and cleaned context list
            pattern = software_context
            '''if software_name_lower in software_context_list_lower_cleaned:
                software_small_index = software_context_list_lower_cleaned.index(software_name_lower)  # Get the index of the software name in the cleaned context list
                # Create a pattern based on the context around the software name
                if software_small_index == 0:
                    pattern = software_context_list[software_small_index:software_small_index + 4]
                    pattern = " ".join(pattern)
                else:
                    pattern = software_context_list[software_small_index - 2:software_small_index + 2]
                    pattern = " ".join(pattern)
            else:
                # If software name is not directly found, check for a longer context
                software_name_list = software_name_lower.split()
                software_long_index = is_sublist(software_context_list_lower_cleaned, software_name_list)  # Get the index and length of the software name in the cleaned context list

                number_words = software_long_index[1]
                # If the context word ends with "-", join the context words into a single word
                if software_context_list[software_long_index[0]].endswith("-"):
                    joined_software = "".join(software_context_list[software_long_index[0]:(software_long_index[0] + software_long_index[1])])
                    software_context_list[software_long_index[0]:software_long_index[0] + software_long_index[1]] = [joined_software]
                # Create a pattern based on the extended context around the software name
                pattern = software_context_list[(software_long_index[0]) - 2:(software_long_index[0]) + number_words + 2]
                pattern = " ".join(pattern)'''

            # Escape special characters in the pattern
            escaped_pattern = re.escape(pattern)

            # Create a dictionary to store information about the software
            software_dict = {"software_name": software_name, "pattern_found": False, "pattern_searched": pattern}

            # Search for the pattern in the XML content
            for tag in xml_content_p:
                print(tag.text)
                if re.search(escaped_pattern, tag.text):
                    software_dict["pattern_found"] = True
                    break  # Stop searching once the pattern is found


            # Append the software information dictionary to the result list
            software_list_result.append(software_dict)

    # Count the number of successes and failures and log the results
    success = 0
    failure = 0
    for result in software_list_result:
        if not result["pattern_found"]:
            failure += 1
            logging.critical(result)
        else:
            logging.debug(result)
            success += 1
    logging.info(f"For {len(data_json.get('mentions'))} software in the json we found : {success} in the xml but {failure} failed")


# Entry point of the script
if __name__ == "__main__":
    # Check if the correct number of command line arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python your_script_name.py <xml_path> <json_path>")
        sys.exit(1)

    # Extract XML and JSON file paths from command line arguments
    xml_path = sys.argv[1]
    json_path = sys.argv[2]

    # Call the main function to enhance the JSON file with information from the XML file
    xml_enhance_json(xml_path, json_path)
    print("// info logged in logging.log")
