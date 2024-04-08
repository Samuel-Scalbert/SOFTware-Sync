import xml.etree.ElementTree as ET

def software_counts(xml_file):

    with open(xml_file, 'r') as xml_file:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        list_tag_software = root.findall(".//{http://www.tei-c.org/ns/1.0}software")
        return len(list_tag_software)