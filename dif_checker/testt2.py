import xml.etree.ElementTree as ET
import copy
import difflib

def dif_checker(str1, str2):
    modification = 0
    for i, s in enumerate(difflib.ndiff(str1, str2)):
        if s[0] == ' ':
            continue
        elif s[0] == '-':
            modification += 1
            print(u'Delete "{}" from position {}'.format(s[-1], i))
        elif s[0] == '+':
            modification += 1
            print(u'Add "{}" to position {}'.format(s[-1], i))
    if modification > 1:
        print(str1)
        print(str2)

def wizzard_xml_json2(p, software_mentions):
    p_string = "".join(p.itertext())
    saved_p_string = p_string
    sub_tags_list = []
    original_sub_tags_list = []
    ET.register_namespace('', "http://www.tei-c.org/ns/1.0")

    for elm in list(p):
        if elm.tail != None:
            index = p_string.find(elm.text, p_string.find(elm.tail) - len(elm.text), len(p_string) )
        else:
            index = p_string.find(elm.text)
        if index != -1:
            if elm.attrib:
                attributes_dict = elm.attrib
                original_sub_tags_list.append([elm.tag, elm.text, elm.tail, index, "sub-element", attributes_dict])
            else:
                attributes_dict = None
                original_sub_tags_list.append([elm.tag, elm.text, elm.tail, index, "sub-element", attributes_dict])

    full_list_software = []
    for software_mention in software_mentions:
        if software_mention["software-type"] == "software":
            software = software_mention["software-name"]["rawForm"]
            context = software_mention["context"]
            if software.find('\n') != -1:
                software = software.replace("\n", "")
                offsetStart = software_mention["software-name"]["offsetStart"] - 1
                offsetEnd = software_mention["software-name"]["offsetEnd"] - 1
            else:
                offsetStart = software_mention["software-name"]["offsetStart"]
                offsetEnd = software_mention["software-name"]["offsetEnd"]
        index_context = p_string.find(context)
        if index_context != -1:
            offsetStart_full_str = index_context + offsetStart
            offsetEnd_full_str = index_context + offsetEnd
            software_list = ['software', software, None, offsetStart_full_str, 'software', None]
            full_list_software.append(software_list)
    if not full_list_software:
        return False
    list_len = len(full_list_software) + len(original_sub_tags_list)
    full_list_software = sorted(full_list_software, key=lambda x: x[3])
    for tags in full_list_software:
        str_alt_index = tags[3]
        software = tags[1]
        nb = 0
        for elm in range(len(original_sub_tags_list)):
            if str_alt_index < original_sub_tags_list[nb][3] and nb == 0:
                old_string = p.text
                new_p_text = p_string[:str_alt_index]
                tail_software = p_string[str_alt_index + len(software):original_sub_tags_list[nb][3]]
                if len(tail_software) == 0:
                    tail_software = ' '
                if new_p_text + software + tail_software == old_string:
                    p.text = new_p_text
                    software_list = ['software', software, tail_software, str_alt_index, 'software', None]
                    original_sub_tags_list.append(software_list)
                    print(f'{software} was added to the list')
                    original_sub_tags_list = sorted(original_sub_tags_list, key=lambda x: x[3])
                    break
                else:
                    #print(f'old_p_string : "{old_string}"\n new_p_text : "{new_p_text}"\n new_software_tail : "{tail_software}"')
                    print(f'\nCRITICAL : {software}(start) : CRITICAL\n')
            try:
                if str_alt_index > original_sub_tags_list[nb][3] and str_alt_index < original_sub_tags_list[nb+1][3]:

                    old_string = original_sub_tags_list[nb][2]
                    new_tail_prior_tag = p_string[original_sub_tags_list[nb][3] + len(original_sub_tags_list[nb][1]): str_alt_index]
                    tail_software =p_string[str_alt_index + len(software):original_sub_tags_list[nb+1][3]]

                    if len(tail_software) == 0:
                        tail_software = ' '
                    if new_tail_prior_tag + software +tail_software == old_string:
                        software_list = ['software', software, tail_software, str_alt_index, 'software', None]
                        original_sub_tags_list[nb][2] = new_tail_prior_tag
                        original_sub_tags_list.append(software_list)
                        print(f'{software} was added to the list')
                        original_sub_tags_list = sorted(original_sub_tags_list, key=lambda x: x[3])
                        break
                    else:
                        print(f'\nCRITICAL : {software}(middle) : CRITICAL\n')
            except IndexError:
                if str_alt_index > original_sub_tags_list[len(original_sub_tags_list)-1][3]:
                    old_string = original_sub_tags_list[len(original_sub_tags_list)-1][2]
                    new_tail_prior_tag = p_string[original_sub_tags_list[len(original_sub_tags_list)-1][3] + len(original_sub_tags_list[len(original_sub_tags_list)-1][1]):str_alt_index]
                    tail_software = p_string[str_alt_index + len(software):]
                    if len(tail_software) == 0:
                        tail_software = ' '
                    if new_tail_prior_tag + software + tail_software == old_string:
                        software_list = ['software', software, tail_software, str_alt_index, 'software', None]
                        original_sub_tags_list[len(original_sub_tags_list) - 1][2] = new_tail_prior_tag
                        original_sub_tags_list.append(software_list)
                        print(f'{software} was added to the list')
                        original_sub_tags_list = sorted(original_sub_tags_list, key=lambda x: x[3])
                        break
                    else:
                        #print(f'old_p_string : "{old_string}"\n new_ref_tail : "{original_sub_tags_list[len(original_sub_tags_list)-1][2]}"\n new_software_tail : "{tail_software}"')
                        print(f'\nCRITICAL : {software}(end) : CRITICAL\n')
            original_sub_tags_list = sorted(original_sub_tags_list, key=lambda x: x[3])
            nb += 1
    if len(original_sub_tags_list) == list_len:
        print(f'THE JOB IS DONE {len(original_sub_tags_list)}/{list_len}\n')
    else:
        print(f'CRITICAL: all the elements are not in the <p>')

    final_p_string = p.text
    for elm in original_sub_tags_list:
        if elm[2] == None:
            final_p_string += " "
        if elm[1]:
            final_p_string += elm[1]
        if elm[2]:
            final_p_string += elm[2]
    dif_checker(final_p_string, saved_p_string)
