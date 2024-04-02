import xml.etree.ElementTree as ET
import json
from .wizzard import wizzard_xml_json2
import os
from package_perso.utils import setup_logger, find_differences_software,duplicates_JSON
import shutil
def json_enhance_xml(xml_path, json_path,super_logger):

    filename = file_name = os.path.basename(xml_path)

    with open(xml_path, 'r') as xml_file:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        ns = {"tei": "http://www.tei-c.org/ns/1.0"}

    with open(json_path, 'r') as json_file:
        data_json = json.load(json_file)
        data_json_get_mentions = data_json.get("mentions")
        for elm in duplicates_JSON(data_json_get_mentions):
            data_json_get_mentions.remove(elm)

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

    context_list_found = []

    logger = setup_logger(f'{xml_path}', f'{xml_path}.log')

    p_elements = root.findall(".//tei:p", ns)
    error_file = []
    nb_all_duplicates = []
    for p in p_elements:
        result = wizzard_xml_json2(p, data_json_get_mentions, logger)
        if result == False:
            pass
        else:
            modified_p, context_list_found_in_p, mentions_found_remove, error_list , nb_duplicates= result
            for duplicates in nb_duplicates:
                nb_all_duplicates.append(duplicates)
            for error in error_list:
                error_file.append(error)
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
    if len(list_added_software) != len(software_list_json) - len(nb_all_duplicates) or mentions_count - len(data_json_get_mentions) != mentions_count:
        context_list_found = [elm[0] for elm in context_list_found]
        super_logger.critical(f'{mentions_count - len(data_json_get_mentions)}/{mentions_count} mentions found in xml')
        super_logger.critical(f'{len(list_added_software)}/{len(software_list_json) - len(nb_all_duplicates)} software tags added')
        list_added_software = [tag.text for tag in list_added_software]
        for duplicates in nb_all_duplicates:
            software_list_json.remove(duplicates)
        super_logger.critical(f'we missed : {find_differences_software(software_list_json ,list_added_software)}')
        context_set = set(context_list_found)
        mentions_set = set(list_mentions)
        difference =  context_set - mentions_set
        for item in difference:
            super_logger.critical(f'{item}')
        for error in error_file:
            super_logger.critical(error)
        if len(nb_all_duplicates) > 0:
            super_logger.critical(f'Test failed ({len(nb_all_duplicates)} duplicates)\n')
        else:
            super_logger.critical(f'Test failed\n')
        source_file = f'{xml_path}.log'
        parent_directory = os.path.dirname(xml_path)
        destination_directory = f"{parent_directory}/log_xml"
        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)
        if os.path.exists(f'{destination_directory}/{filename}.log'):
            os.remove(f'{destination_directory}/{filename}.log')
        if os.path.exists(source_file) and os.path.exists(destination_directory):
            shutil.move(source_file, destination_directory)
    else:
        if len(nb_all_duplicates) > 0:
            super_logger.info(f'Test passed ({len(nb_all_duplicates)} duplicates)\n')
        else:
            super_logger.info(f'Test passed\n')
        if os.path.exists(f'{xml_path}.log'):
            os.remove(f'{xml_path}.log')

    # Write the modified XML back to the file
    with open(f"./result/XML_software/{file_name.replace('.xml','')}.software.xml", 'wb') as output_xml_file:
        ET.register_namespace("", "http://www.tei-c.org/ns/1.0")
        xml_str = ET.tostring(root, encoding='utf-8')
        output_xml_file.write(xml_str)
