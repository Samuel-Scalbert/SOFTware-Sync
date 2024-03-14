import difflib
import re
import os
import logging

def common_file_xmlgrobid_xmlmeta(xml_path_GROBID,xml_path_META):
    list_xml_grobid = os.listdir(xml_path_GROBID)
    list_xml_grobid = [file_name.replace('.grobid.tei.xml', '') for file_name in list_xml_grobid]
    list_xml_meta = os.listdir(xml_path_META)
    list_xml_meta = [file_name.replace('.xml', '') for file_name in list_xml_meta]
    list_common_file = []
    for xml in list_xml_grobid:
        if xml in list_xml_meta:
            list_common_file.append(xml)
    return list_common_file

def setup_logger(name, log_file, level=logging.INFO):
    handler = logging.FileHandler(log_file, mode='w')
    handler.setFormatter(logging.Formatter('%(levelname)s : %(message)s'))

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

def common_file_xml_json(dir_xml_path,dir_json_path):
    list_xml = os.listdir(dir_xml_path)
    for xml in list_xml:
        if xml.endswith('.xml.log'):
            list_xml.remove(xml)
    list_xml = [file_name.replace('.grobid.tei.xml', '') for file_name in list_xml]
    list_json = os.listdir(dir_json_path)
    list_json = [file_name.replace('.software.json', '') for file_name in list_json]
    list_common_file = []
    for xml in list_xml:
        if xml in list_json:
            list_common_file.append(xml)
    return list_common_file

def find_occurrences(word, text):
    occurrences = []
    word_lower = word.lower()
    text_lower = text.lower()
    # Remove punctuation from text
    text_without_punctuation = re.sub(r"[';:,.!?]", ' ', text_lower)
    #print(text,'\n')
    #print(text_without_punctuation)
    index = -1
    while True:
        index = text_without_punctuation.find(word_lower, index + 1)
        if index == -1:
            break
        occurrences.append(index)
    return occurrences

def contains_special_characters(text):
    for char in text:
        if ord(char) < 32 or ord(char) > 126:
            return True  # Special character found
    return False


def find_closest_number(number, number_list):
    closest = None
    min_difference = float('inf')  # Initialize with infinity

    for num in number_list:
        difference = abs(number - num)
        if difference < min_difference:
            min_difference = difference
            closest = num

    return closest

def longest_common_substrings(full_string, sub_string):
    matches = []
    max_length = 0
    less_word = len(sub_string)
    founded = False
    while not founded:
        if full_string.find(sub_string[:less_word]) != -1:
            return full_string.find(sub_string[:less_word])
        else:
            founded = False
            less_word -= 1
def dif_string_checker(str1, str2):
    modification = 0
    list_modification = []
    for i, s in enumerate(difflib.ndiff(str1, str2)):
        if s[0] == ' ':
            continue
        elif s[0] == '-':
            if s[-1] == ' ':
                pass
            else:
                modification += 1
                print(u'Delete "{}" from position {}'.format(s[-1], i))
        elif s[0] == '+':
            modification += 1
            print(u'Add "{}" to position {}'.format(s[-1], i))
    if modification > 1:
        print(str1)
        print(str2)
