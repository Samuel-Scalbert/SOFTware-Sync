import xml.etree.ElementTree as ET
import json
from .xml_json import wizzard_xml_json2
import logging
import os

def json_enhance_xml(xml_path, json_path,super_logger,logger):

    with open(xml_path, 'r') as xml_file:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        ns = {"tei": "http://www.tei-c.org/ns/1.0"}

    with open(json_path, 'r') as json_file:
        data_json = json.load(json_file)
        data_json_get_mentions = data_json.get("mentions")
        software_types = {}
        software_counts = {}
        mentions_count = 0

        for mention in data_json_get_mentions:
            software_type = mention["software-type"]
            software = mention["software-name"]["normalizedForm"]
            mentions = mention["context"]

            # Count occurrences of software types
            if software_type in software_types:
                software_types[software_type] += 1
            else:
                software_types[software_type] = 1

            # Count occurrences of specific software names
            if software in software_counts:
                software_counts[software] += 1
            else:
                software_counts[software] = 1

            if mentions:
                mentions_count += 1
    filename = file_name = os.path.basename(xml_path)
    super_logger.info(f'{filename}')
    super_logger.info(f'{software_types}')
    super_logger.info(f'{software_counts}')


    paths = [
        "./tei:teiHeader/tei:profileDesc/tei:abstract/tei:div",
        "./tei:text/tei:body/tei:div",
        "./tei:text/tei:back/tei:div[@type='acknowledgement']/tei:div",
        "./tei:text/tei:back/tei:div[@type='availability']/tei:div",
        "./tei:text/tei:back/tei:div[@type='annex']/tei:div"
        ]

    context_list_found = []
    for path in paths:
        div_elements = root.findall(path, ns)
        for div_element in div_elements:
            p_elements = div_element.findall(".//tei:p", ns)
            for p in p_elements:
                result = wizzard_xml_json2(p, data_json_get_mentions,logger)
                if result == False:
                    pass
                else:
                    modified_p, context_list_found_in_p = result
                    if len(context_list_found_in_p) > 0:
                        context_list_found += context_list_found_in_p
    found_type = {}
    for context in context_list_found:
        if context[1] in found_type:
            found_type[context[1]] += 1
        else:
            found_type[context[1]] = 1
    super_logger.info(found_type)
    if len(context_list_found) != mentions_count:
        super_logger.info(f'{mentions_count} mentions in the file "{xml_path}"')
        difference_mention = len(context_list_found)-mentions_count
        if difference_mention < 0:
            super_logger.critical(f'-{difference_mention} mention(s) in the new file\n')
        else:
            super_logger.critical(f'+{difference_mention} mention(s) in the new file\n')
    else:
        super_logger.info(f'{mentions_count} mentions in the file "{xml_path}"\n')

    # Write the modified XML back to the file
    with open(f"./data/software_result/{file_name.replace('.xml','')}.software.xml", 'wb') as output_xml_file:
        ET.register_namespace("", "http://www.tei-c.org/ns/1.0")
        xml_str = ET.tostring(root, encoding='utf-8')
        output_xml_file.write(xml_str)
