import json
import re
import re
import xml.etree.ElementTree as ET

tree = ET.parse('test.xml')
root = tree.getroot()



with open('test.json') as json_file:
    data = json.load(json_file)

context = data["context"]
mention = data["mention"]

p = root.find("p")

p_text = p.text

mention_offset = p_text.lower().find(mention)

mention_field = ET.Element("mention")
mention_field.text = mention

p.insert(mention_offset, mention_field)

xml_string = ET.tostring(root, encoding='utf-8').decode('utf-8')
#print(xml_string)


##################

# <root>
#     <person>
#         <name>John Doe</name>
#         <age>30</age>
#         <city>New <important> York </important></city>
#     </person>
#     <p>Bonjour je m'appelle Samuel</p>
#     <person>
#         <name>Jane Smith</name>
#         <age>25</age>
#         <city>London</city>
#     </person>
# </root>

tree = ET.parse('test.xml')
root = tree.getroot()

city = root.find("person/city")

xml_string = ET.tostring(city, encoding='utf-8').decode('utf-8')


def convert_offset_wo_tag(xml_string, previous_string, offset_start, offset_end):
    wo_offset = re.sub('<[^>]*>', '', xml_string)
    new_offset_start = wo_offset.find(previous_string) + offset_start
    new_offset_end = new_offset_start + (offset_end - offset_start)
    return new_offset_start, new_offset_end

xml_string = "<tag>New York</tag>"
previous_string = "New York"

offset_start = xml_string.find("New")
offset_end = offset_start + len("New York")

print(xml_string[offset_start:offset_end])

new_offset_start, new_offset_end = convert_offset_wo_tag(xml_string, previous_string, offset_start, offset_end)

print(new_offset_start, new_offset_end)
print(previous_string[new_offset_start:new_offset_end])

print("previous_offset_start: ", offset_start)
print("previous_offset_end: ", offset_end)
print("new_offset_start: ", new_offset_start)
print("new_offset_end: ", new_offset_end)