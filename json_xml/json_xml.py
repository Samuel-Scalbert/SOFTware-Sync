import xml.etree.ElementTree as ET
import json
from .wizzard import wizzard_xml_json2
import os
from package_perso.utils import setup_logger

def json_enhance_xml(xml_path, json_path,super_logger):

    filename = file_name = os.path.basename(xml_path)

    with open(xml_path, 'r') as xml_file:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        ns = {"tei": "http://www.tei-c.org/ns/1.0"}

    with open(json_path, 'r') as json_file:
        data_json = json.load(json_file)
        data_json_get_mentions = data_json.get("mentions")
        software_types = {}
        software_counts = {}
        list_mentions = []
        mentions_count = 0
        software_list_json = []

        if not data_json_get_mentions:
            super_logger.info(f'{filename}')
            super_logger.info('no mentions\n')
            return None
        for mention in data_json_get_mentions:
            software_type = mention["software-type"]
            software = mention["software-name"]["normalizedForm"]
            try:
                mentions = mention["context"]
            except KeyError:
                data_json_get_mentions.remove(mention)
            list_mentions.append(mentions)
            software_list_json.append(software)
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
    super_logger.info(f'{filename}')
    super_logger.info(f'{software_types}')
    super_logger.info(f'{software_counts}')


    paths = [
        "./tei:teiHeader/tei:profileDesc/tei:abstract/tei:div",
        "./tei:text/tei:body/tei:div",
        "./tei:text/tei:body/tei:note",
        "./tei:text/tei:back/tei:div[@type='acknowledgement']/tei:div",
        "./tei:text/tei:back/tei:div[@type='availability']/tei:div",
        "./tei:text/tei:back/tei:div[@type='annex']/tei:div"
        ]

    context_list_found = []

    logger = setup_logger(f'{xml_path}', f'{xml_path}.log')

    p_elements = root.findall(".//tei:p", ns)
    for p in p_elements:
        result = wizzard_xml_json2(p, data_json_get_mentions, logger)
        if result == False:
            pass
        else:
            modified_p, context_list_found_in_p, mentions_found_remove = result
            for mention_remove in mentions_found_remove:
                for mention in data_json_get_mentions:
                    if mention_remove == mention:
                        data_json_get_mentions.remove(mention_remove)
            if len(context_list_found_in_p) > 0:
                context_list_found += context_list_found_in_p
    found_type = {}
    for context in context_list_found:
        if context[1] in found_type:
            found_type[context[1]] += 1
        else:
            found_type[context[1]] = 1
    super_logger.info(found_type)
    list_added_software = root.findall(".//software", ns)
    if len(list_added_software) != mentions_count:
        context_list_found = [elm[0] for elm in context_list_found]
        super_logger.critical(f'{len(context_list_found)}/{mentions_count} mentions found in xml')
        super_logger.critical(f'{len(list_added_software)}/{len(software_list_json)} software tags added')
        context_set = set(context_list_found)
        mentions_set = set(list_mentions)
        difference = mentions_set - context_set
        for item in difference:
            super_logger.critical(f'{item}')
        super_logger.critical('Test failed\n')
    else:
        super_logger.info(f'Test passed\n')

    # Write the modified XML back to the file
    with open(f"./result/XML_software/{file_name.replace('.xml','')}.software.xml", 'wb') as output_xml_file:
        ET.register_namespace("", "http://www.tei-c.org/ns/1.0")
        xml_str = ET.tostring(root, encoding='utf-8')
        output_xml_file.write(xml_str)
