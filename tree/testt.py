import xml.etree.ElementTree as ET

xml = '<root><p>hello, this is a test sentence with a <ref type="table" target="tab_0">reference_1</ref>, my software is MOD and here is another <ref type="table" target="tab_0">reference_2</ref> and some more text </p></root>'
root = ET.fromstring(xml)

p = root.find('p')
p_string = "".join(p.itertext())

software = 'MOD'

p_str_wo_child = str(p.text)

sub_tags_list = []
list_p = list(p)
p_software_index= p_str_wo_child.find(software)
for elm in list_p:
    index = p_string.find(elm.text)
    if index != -1:
        sub_tags_list.append([elm.tag, elm.text, elm.tail, index])
        p_string = p_string.replace(elm.text, '', 1)
    p_str_wo_child += str(elm.tail)
    p.remove(elm)

sub_tags_list = sorted(sub_tags_list, key=lambda x: x[3])
print(p_string)
p_software_index= p_str_wo_child.find(software)

if p_software_index:

    sub_tags_list.append(["software", software, False,p_software_index])
    sub_tags_list = sorted(sub_tags_list, key=lambda x: x[3])
    print(sub_tags_list)
    for tag_name, tag_content, tail ,index in sub_tags_list:
        tag = ET.Element(tag_name)
        tag.text = tag_content
        if tail == False:
            index_software = last_tail.find(software)
            tag.tail = last_tail[index_software:].replace(software,'')
            print(tag.tail)
        else:
            if tail.find(software):
                tag.tail = tail[:tail.find(software)].replace(software, '')
                last_tail = tail
            else:
                tag.tail = tail
                last_tail = tail
        p.append(tag)
    '''
    for tag_name,tag_content,index,tail in sub_tags_list:
        tag = ET.Element(tag_name)
        tag.text = tag_content
        tag.tail = tail
        p.append(tag)

    software_tag = ET.Element("software")
    software_tag.text = str(software)
    p.text = p_str_wo_child
    software_tag.tail = p.text[(p_software_index + len(software)):]
    p.text = p.text[:p_software_index]
    print(software_tag.tail)
    p.append(software_tag)'''




modified_xml = ET.tostring(root, encoding='unicode')

print(modified_xml)

