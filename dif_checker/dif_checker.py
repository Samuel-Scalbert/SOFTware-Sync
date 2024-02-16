import xml.etree.ElementTree as ET
import logging
import json
import sys
import string
from .testt2 import wizzard_xml_json

logging.basicConfig(filename='dif_checker.log', encoding='utf-8', level=logging.DEBUG, filemode='w', format='%(levelname)s-%(message)s')


def xml_enhance_json(xml_path, json_path):

    with open(xml_path, 'r', encoding='utf-8') as xml_file:
        root = ET.parse(xml_file)
        root = root.getroot()
        ns = {"tei": "http://www.tei-c.org/ns/1.0"}


    with open(json_path, 'r') as json_file:
        data_json = json.load(json_file)
        div_elements = root.findall("./tei:text/tei:body//tei:div", ns)
        for div_element in div_elements:
            p_elements = div_element.findall(".//tei:p", ns)
            for p in p_elements:
                for software_mention in data_json.get("mentions"):
                    if software_mention["software-type"] == "software":
                        software_name = software_mention["software-name"]["rawForm"]
                        software_name = software_name.replace("\n", " ")
                        software_context = software_mention["context"]
                        offset_start = software_mention["software-name"]["offsetStart"]
                        offset_end = software_mention["software-name"]["offsetEnd"]
                        p = wizzard_xml_json(software_context, offset_start,offset_end,software_name, p)
                        #print(result)

    modified_xml = ET.tostring(root, encoding='unicode')
    with open("./test.xml", 'w', encoding='utf-8') as output_xml_file:
        output_xml_file.write(modified_xml)