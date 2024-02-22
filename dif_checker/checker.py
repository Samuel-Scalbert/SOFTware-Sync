import xml.etree.ElementTree as ET

def read_xml_file(file_path):
    try:
        with open(file_path, 'r') as file:
            root = ET.parse(file)
            root = root.getroot()
            return root
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None

def compare_xml_files(xml_file1, xml_file2):
    content1 = read_xml_file(xml_file1)
    content2 = read_xml_file(xml_file2)

    ns = {"tei": "http://www.tei-c.org/ns/1.0"}

    list_content1 = []
    div_elements = content1.findall("./tei:text/tei:body//tei:div", ns)
    for div_element in div_elements:
        p_elements = div_element.findall(".//tei:p", ns)
        for p in p_elements:
            p_string = "".join(p.itertext())
            list_content1.append(p_string)
    #print(list_content1)

    list_content2 = []
    div_elements = content2.findall("./tei:text/tei:body//tei:div", ns)
    for div_element in div_elements:
        p_elements = div_element.findall(".//tei:p", ns)
        for p in p_elements:
            p_string = "".join(p.itertext())
            list_content2.append(p_string)
    #print(list_content2)

    for item1, item2 in zip(list_content1, list_content2):
        if item1 == item2:
            print(f"same")
        else:
            print(f"diff : {item1} // {item2}")

compare_xml_files("./data/xml_files/PMC3130168.xml","./test.xml")