import xml.etree.ElementTree as ET
from fuzzywuzzy import fuzz
from .test import longest_common_substrings,find_closest_number,contains_special_characters, dif_string_checker, find_occurrences


def wizzard_xml_json2(p, software_mentions):
    p_string = "".join(p.itertext())
    original_sub_tags_list = []
    ET.register_namespace('', "http://www.tei-c.org/ns/1.0")
    if p_string == None:
        return None

    for elm in list(p):
        if elm.tail != None:
            index = p_string.find(elm.text, p_string.find(elm.tail) - len(elm.text), len(p_string))
            if index == -1:
                index = p_string.find(elm.text)
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
            else:
                offsetStart = software_mention["software-name"]["offsetStart"]
        index_context = p_string.find(context)
        normal_found = -1
        if index_context != -1:
            normal_found = 1
            offsetStart_full_str = index_context + offsetStart
            if p_string[offsetStart_full_str: offsetStart_full_str + len(software)] == software:
                software_list = ['software', software, None, offsetStart_full_str, 'software', None, 'normal']
                full_list_software.append(software_list)
            else:
                print(f'error index (normal) software we found {p_string[offsetStart_full_str: offsetStart_full_str+len(software)]}')
        if fuzz.partial_ratio(p_string, context) >= 95 and normal_found != 1 and len(p_string) >= len(context):
            index_context_from_fuzzy = longest_common_substrings(p_string, context)
            occurences = find_occurrences(software,p_string[index_context_from_fuzzy:])
            print('la:',occurences,offsetStart)
            p_software_index = find_closest_number(offsetStart,occurences)
            if p_string[index_context_from_fuzzy + p_software_index:index_context_from_fuzzy + p_software_index+len(software)] == software:
                offsetStart_full_str = index_context_from_fuzzy + p_software_index
                software_list = ['software', software, None, offsetStart_full_str, 'software', None, 'fuzzy']
                full_list_software.append(software_list)
            else:
                print(f'error index (fuzzy) software for: {context}')
    for elm in full_list_software:
        print(elm)
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
                if (str_alt_index > original_sub_tags_list[nb][3] or str_alt_index == original_sub_tags_list[nb][3]) and str_alt_index < original_sub_tags_list[nb][3] + len(original_sub_tags_list[nb][1]):
                    print('inside text', software)
                    break
                if new_p_text + software + tail_software == old_string:
                    p.text = new_p_text
                    software_list = ['software', software, tail_software, str_alt_index, 'software', None]
                    original_sub_tags_list.append(software_list)
                    print(f'{software} was added to the list (start)')
                    original_sub_tags_list = sorted(original_sub_tags_list, key=lambda x: x[3])
                    break
                else:
                    #print(f'old_p_string : "{old_string}"\n new_p_text : "{new_p_text}"\n new_software_tail : "{tail_software}"')
                    print(f'CRITICAL : {software}(start) : CRITICAL')
            try:
                if str_alt_index >= original_sub_tags_list[nb][3] and str_alt_index < original_sub_tags_list[nb+1][3]:
                    old_string = original_sub_tags_list[nb][2]
                    new_tail_prior_tag = p_string[original_sub_tags_list[nb][3] + len(original_sub_tags_list[nb][1]): str_alt_index]
                    tail_software =p_string[str_alt_index + len(software):original_sub_tags_list[nb+1][3]]
                    if len(tail_software) == 0:
                        tail_software = ' '
                    if (str_alt_index > original_sub_tags_list[nb][3] or str_alt_index == original_sub_tags_list[nb][3]) and str_alt_index < original_sub_tags_list[nb][3] + len(original_sub_tags_list[nb][1]):
                        new_text_prior_tag = p_string[original_sub_tags_list[nb][3]:str_alt_index]
                        tail_software = p_string[str_alt_index + len(software):original_sub_tags_list[nb][3] + len(
                            original_sub_tags_list[nb][1])]
                        if new_text_prior_tag + software + tail_software == original_sub_tags_list[nb][1]:
                            original_sub_tags_list[nb][1] = new_text_prior_tag
                            software_list = ['software', software, tail_software, str_alt_index, 'software_sub', None]
                            original_sub_tags_list[nb].append(software_list)
                            list_len -= 1
                            print(f'{software} was added to the list (middle) as a sub-child')
                            break
                        else:
                            # print(f'old_p_string : "{old_string}"\n new_ref_tail : "{original_sub_tags_list[len(original_sub_tags_list)-1][2]}"\n new_software_tail : "{tail_software}"')
                            print(f'CRITICAL : {software}(middle \ inside) : CRITICAL')
                        break
                    if new_tail_prior_tag + software + tail_software == old_string:
                        software_list = ['software', software, tail_software, str_alt_index, 'software', None]
                        original_sub_tags_list[nb][2] = new_tail_prior_tag
                        original_sub_tags_list.append(software_list)
                        print(f'{software} was added to the list (middle)')
                        original_sub_tags_list = sorted(original_sub_tags_list, key=lambda x: x[3])
                        break
                    else:
                        #dif_string_checker(old_string,new_tail_prior_tag + software + tail_software)
                        #print(f'old_p_string : "{old_string}"\n new_ref_tail : "{new_tail_prior_tag}"\n new_software_tail : "{tail_software}"')
                        print(f'CRITICAL : {software}(middle) {old_string} : CRITICAL')
            except IndexError:
                if str_alt_index >= original_sub_tags_list[len(original_sub_tags_list)-1][3]:
                    old_string = original_sub_tags_list[len(original_sub_tags_list)-1][2]
                    new_tail_prior_tag = p_string[original_sub_tags_list[len(original_sub_tags_list)-1][3] + len(original_sub_tags_list[len(original_sub_tags_list)-1][1]):str_alt_index]
                    tail_software = p_string[str_alt_index + len(software):]
                    if len(tail_software) == 0:
                        tail_software = ' '
                    if str_alt_index >= original_sub_tags_list[nb][3] and str_alt_index < original_sub_tags_list[nb][3] + len(original_sub_tags_list[nb][1]):
                        new_text_prior_tag = p_string[original_sub_tags_list[nb][3]:str_alt_index]
                        tail_software = p_string[str_alt_index + len(software):original_sub_tags_list[nb][3] + len(original_sub_tags_list[nb][1])]
                        if new_text_prior_tag + software + tail_software == original_sub_tags_list[nb][1]:
                            original_sub_tags_list[nb][1] = new_text_prior_tag
                            software_list = ['software', software, tail_software, str_alt_index, 'software_sub', None]
                            original_sub_tags_list[nb].append(software_list)
                            print(f'{software} was added to the list (middle) as a sub-child')
                            list_len -= 1
                            break
                        else:
                            # print(f'old_p_string : "{old_string}"\n new_ref_tail : "{original_sub_tags_list[len(original_sub_tags_list)-1][2]}"\n new_software_tail : "{tail_software}"')
                            print(f'CRITICAL : {software}(end \ inside) : CRITICAL')
                        break
                    if new_tail_prior_tag + software + tail_software == old_string:
                        software_list = ['software', software, tail_software, str_alt_index, 'software', None]
                        original_sub_tags_list[len(original_sub_tags_list) - 1][2] = new_tail_prior_tag
                        original_sub_tags_list.append(software_list)
                        print(f'{software} was added to the list (end)')
                        original_sub_tags_list = sorted(original_sub_tags_list, key=lambda x: x[3])
                        break
                    else:
                        #print(f'old_p_string : "{old_string}"\n new_ref_tail : "{original_sub_tags_list[len(original_sub_tags_list)-1][2]}"\n new_software_tail : "{tail_software}"')
                        print(f'CRITICAL : {software}(end) : CRITICAL')
            original_sub_tags_list = sorted(original_sub_tags_list, key=lambda x: x[3])
            nb += 1
    if len(original_sub_tags_list) == list_len:
        print(f'THE JOB IS DONE {len(original_sub_tags_list)}/{list_len}\n')


    final_p_string = p.text
    for elm in original_sub_tags_list:
        if elm[2] == None:
            final_p_string += " "
        if elm[1]:
            final_p_string += elm[1]
        if elm[2]:
            final_p_string += elm[2]
    #dif_string_checker(final_p_string, saved_p_string)
