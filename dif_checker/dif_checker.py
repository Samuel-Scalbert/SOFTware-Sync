import xml.etree.ElementTree as ET
import json
from .testt2 import wizzard_xml_json2


def xml_enhance_json(xml_path, json_path):

    with open(xml_path, 'r') as xml_file:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        ns = {"tei": "http://www.tei-c.org/ns/1.0"}

    with open(json_path, 'r') as json_file:
        data_json = json.load(json_file)
        data_json_get_mentions = data_json.get("mentions")
        software_types = {}
        software_counts = {}

        for mention in data_json_get_mentions:
            software_type = mention["software-type"]
            software = mention["software-name"]["normalizedForm"]

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

        print(software_types)
        print(software_counts)

    paths = [
        "./tei:teiHeader/tei:profileDesc/tei:abstract/tei:div",
        "./tei:text/tei:body/tei:div",
        "./tei:text/tei:back/tei:div[@type='acknowledgement']/tei:div",
        "./tei:text/tei:back/tei:div[@type='availability']/tei:div",
        "./tei:text/tei:back/tei:div[@type='annex']/tei:div"
        ]

    paths = ["./tei:text/tei:body/tei:div"]
    context_list_found = []
    for path in paths:
        div_elements = root.findall(path, ns)
        for div_element in div_elements:
            p_elements = div_element.findall(".//tei:p", ns)
            for p in p_elements:
                result = wizzard_xml_json2(p, data_json_get_mentions)
                if result == False:
                    pass
                else:
                    modified_p, context_list_found_in_p = result
                    if len(context_list_found_in_p) > 0:
                        context_list_found += context_list_found_in_p
    print(f'we founded : {len(context_list_found)} context')

    # Write the modified XML back to the file
    with open("./test_monstre.xml", 'wb') as output_xml_file:
        ET.register_namespace("", "http://www.tei-c.org/ns/1.0")
        xml_str = ET.tostring(root, encoding='utf-8')
        output_xml_file.write(xml_str)
