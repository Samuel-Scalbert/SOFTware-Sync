import xml.etree.ElementTree as ET

def xml_builder(meta_xml,grobid_xml,filename):

    with open(grobid_xml, 'r') as xml_file:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        ns = {"tei": "http://www.tei-c.org/ns/1.0"}
        root.attrib.pop("{http://www.w3.org/XML/1998/namespace}space")
        root.attrib.pop("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation")
        root.tag = 'teiCorpus'



    with open(meta_xml, 'r') as xml_file:
        tree_meta = ET.parse(xml_file)
        root_meta = tree_meta.getroot()
        body_meta = root_meta.find("./tei:text",ns)
        body_meta.append(root)

    ET.register_namespace("", "http://www.tei-c.org/ns/1.0")
    ET.ElementTree(root_meta).write(f'./result/XML_meta_software/{filename}.hal.grobid.xml', encoding='utf-8', xml_declaration=True)
