import xml.etree.ElementTree as ET
from fuzzywuzzy import fuzz
from package_perso.utils import longest_common_substrings, find_closest_number, find_occurrences


def wizzard_xml_json2(p, software_mentions, logger):
    p_string = "".join(p.itertext())
    original_sub_tags_list = []
    context_list_found = []
    ET.register_namespace('', "http://www.tei-c.org/ns/1.0")
    if p_string == None:
        return None
    '''for elm in list(p):
        if elm.tag == "{http://www.tei-c.org/ns/1.0}p":
            return False'''
    for elm in list(p):
        index = -1
        if elm.text == None:
            index = p_string.find(elm.tail)
        if elm.tail != None or elm.text != None:
            if elm.tail == None:
                elm.tail = ''
            if elm.text == None:
                elm.text = ''
            index = p_string.find(elm.text, p_string.find(elm.tail) - len(elm.text), len(p_string))
            if index == -1:
                index = p_string.find(elm.text)
        if index != -1:
            if elm.attrib:
                attributes_dict = elm.attrib
                original_sub_tags_list.append([elm.tag, elm.text, elm.tail, index, "sub-element", attributes_dict])
            else:
                attributes_dict = None
                original_sub_tags_list.append([elm.tag, elm.text, elm.tail, index, "sub-element", attributes_dict])
    full_list_software = []
    mention_found = []
    #print(len(original_sub_tags_list),len(list(p)))
    for software_mention in software_mentions:
        software = software_mention["software-name"]["rawForm"]
        context = software_mention["context"]
        max_score = float('-inf')
        max_attribute = None

        for attribute, details in software_mention["mentionContextAttributes"].items():
            if details["score"] > max_score:
                max_score = details["score"]
                max_attribute = attribute
                attr_software = {"ContextAttributes" : max_attribute}
        if context == None:
            return False
        if software.find('\n') != -1:
            software = software.replace("\n", "")
            offsetStart = software_mention["software-name"]["offsetStart"] - 1
        else:
            offsetStart = software_mention["software-name"]["offsetStart"]
        index_context = p_string.find(context)
        normal_found = -1
        cleaned_found = -1
        #NORMAL
        if index_context != -1:
            normal_found = 1
            offsetStart_full_str = index_context + offsetStart
            if p_string[offsetStart_full_str: offsetStart_full_str + len(software)] == software or p_string[offsetStart_full_str: offsetStart_full_str + len(software)] == context[offsetStart : offsetStart + len(software)]:
                software_list = ['software', software, None, offsetStart_full_str, 'software', None, 'normal']
                full_list_software.append(software_list)
                context_list_found.append([context,software_list[6]])
                mention_found.append(software_mention)
            else:
                logger.critical(f'error index (normal) software we found "{p_string[offsetStart_full_str: offsetStart_full_str+len(software)]}"')
        #CLEANED
        characters = ['-\n','\n']
        for special_character in characters:
            cleaned_context = context.replace(special_character, '')
            if context.find(special_character) != -1 and p_string.find(cleaned_context) != -1:
                cleaned_found = 1
                p_cleaned_index = p_string.find(cleaned_context)
                occurrences = find_occurrences(software, p_string[p_cleaned_index:])
                p_software_index = find_closest_number(offsetStart, occurrences)
                if p_string[p_cleaned_index + p_software_index:p_cleaned_index+p_software_index+len(software)] == software:
                    offsetStart_full_str = p_cleaned_index + p_software_index
                    software_list = ['software', software, None, offsetStart_full_str, 'software', attr_software, 'cleaned']
                    full_list_software.append(software_list)
                    context_list_found.append([context,software_list[6]])
                    mention_found.append(software_mention)
                else:
                    logger.critical(f'error index (cleaned) software for: {context}')
        #FUZZY
        if fuzz.partial_ratio(p_string, context) >= 95 and normal_found == -1 and cleaned_found == -1 and len(p_string) >= len(context):
            index_context_from_fuzzy = longest_common_substrings(p_string, context)
            occurrences = find_occurrences(software,p_string[index_context_from_fuzzy:])
            p_software_index = find_closest_number(offsetStart,occurrences)
            if p_software_index:
                if p_software_index >= 0:
                    if p_string[index_context_from_fuzzy + p_software_index:index_context_from_fuzzy + p_software_index+len(software)] == software:
                        offsetStart_full_str = index_context_from_fuzzy + p_software_index
                        software_list = ['software', software, None, offsetStart_full_str, 'software', attr_software, 'fuzzy']
                        full_list_software.append(software_list)
                        context_list_found.append([context,software_list[6]])
                        mention_found.append(software_mention)
                    else:
                        logger.critical(f'error index (fuzzy) software for: {context}')
                else:
                    logger.critical(f'critical occurences, {software} {context}')
    if not full_list_software:
        return False
    list_len = len(full_list_software) + len(original_sub_tags_list)
    full_list_software = sorted(full_list_software, key=lambda x: x[3])
    if len(original_sub_tags_list) == 0:
        tag_name, software, tail, index, type, attr, tech_found = full_list_software[0]
        tail_software = p_string[index + len(software):]
        old_string = p.text
        new_p_text = p_string[:index]
        if new_p_text + software + tail_software == old_string:
            p.text = new_p_text
            software_list = ['software', software, tail_software, index, 'force_software', None]
            original_sub_tags_list.append(software_list)
            full_list_software.pop(0)
            logger.info(f'{software} was added to the empty list')
    for tags in full_list_software:
        str_alt_index = tags[3]
        software = tags[1]
        nb = 0
        founded = False
        if founded == False:
            for elm in range(len(original_sub_tags_list)):
            #START
                if (str_alt_index < original_sub_tags_list[nb][3] and nb == 0):
                    old_string = p.text
                    new_p_text = p_string[:str_alt_index]
                    tail_software = p_string[str_alt_index + len(software):original_sub_tags_list[nb][3]]
                    if len(tail_software) == 0:
                        tail_software_possible = ' '
                    else:
                        tail_software_possible = ''
                    #NORMAL
                    if new_p_text + software + tail_software == old_string or new_p_text + software + tail_software_possible == old_string:
                        p.text = new_p_text
                        software_list = ['software', software, tail_software, str_alt_index, 'software', attr_software]
                        original_sub_tags_list.append(software_list)
                        logger.info(f'{software} was added to the list (start)')
                        original_sub_tags_list = sorted(original_sub_tags_list, key=lambda x: x[3])
                        founded = True
                        break
                    else:
                        logger.critical(f'{software}(start)')
            #MIDDLE
                try:
                    if str_alt_index >= original_sub_tags_list[nb][3] and str_alt_index < original_sub_tags_list[nb+1][3]:
                        old_string = original_sub_tags_list[nb][2]
                        new_tail_prior_tag = p_string[original_sub_tags_list[nb][3] + len(original_sub_tags_list[nb][1]): str_alt_index]
                        tail_software =p_string[str_alt_index + len(software):original_sub_tags_list[nb+1][3]]
                        # SUB-CHILD
                        if (str_alt_index > original_sub_tags_list[nb][3] or str_alt_index == original_sub_tags_list[nb][3]) and str_alt_index < original_sub_tags_list[nb][3] + len(original_sub_tags_list[nb][1]):
                            new_text_prior_tag = p_string[original_sub_tags_list[nb][3]:str_alt_index]
                            tail_software = p_string[str_alt_index + len(software):original_sub_tags_list[nb][3] + len(
                                original_sub_tags_list[nb][1])]
                            if new_text_prior_tag + software + tail_software == original_sub_tags_list[nb][1]:
                                original_sub_tags_list[nb][1] = new_text_prior_tag
                                software_list = ['software', software, tail_software, 'software_sub', None]
                                original_sub_tags_list[nb].append(software_list)
                                list_len -= 1
                                logger.info(f'{software} was added to the list (middle) as a sub-child')
                                original_sub_tags_list = sorted(original_sub_tags_list, key=lambda x: x[3])
                                founded = True
                                break
                            else:
                                logger.critical(f'{software}(middle \ inside) ')
                        #NORMAL
                        if len(original_sub_tags_list[nb]) == 7:
                            new_tail_prior_tag = p_string[original_sub_tags_list[nb][3] + len(original_sub_tags_list[nb][1]) + len(original_sub_tags_list[nb][6][1]) + len(original_sub_tags_list[nb][6][2]) : str_alt_index]
                            if new_tail_prior_tag + software + tail_software == old_string:
                                software_list = ['software', software, tail_software, str_alt_index, 'software',
                                                 attr_software]
                                original_sub_tags_list[nb][2] = new_tail_prior_tag
                                original_sub_tags_list.append(software_list)
                                logger.info(f'{software} was added to the list (middle)')
                                original_sub_tags_list = sorted(original_sub_tags_list, key=lambda x: x[3])
                                founded = True
                                break
                            else:
                                logger.critical(f'{software}(middle \ sub-ref error) ')
                        if len(original_sub_tags_list[nb]) == 6:
                            if new_tail_prior_tag + software + tail_software == old_string:
                                software_list = ['software', software, tail_software, str_alt_index, 'software',
                                                 attr_software]
                                original_sub_tags_list[nb][2] = new_tail_prior_tag
                                original_sub_tags_list.append(software_list)
                                logger.info(f'{software} was added to the list (middle)')
                                original_sub_tags_list = sorted(original_sub_tags_list, key=lambda x: x[3])
                                founded = True
                                break
                        else:
                            logger.critical(f' {software}(middle) "{new_tail_prior_tag + software + tail_software }" ')
                        #REF-SUB-CHILD
                        if str_alt_index <= original_sub_tags_list[nb+1][3] and str_alt_index + len(software) >= original_sub_tags_list[nb+1][3]:
                            original_sub_tags_list[nb][2] = new_tail_prior_tag
                            old_ref_tag_index = original_sub_tags_list[nb + 1][3]
                            old_ref_tag_text = original_sub_tags_list[nb + 1][1]
                            new_tail_ref_sub = p_string[old_ref_tag_index + len(old_ref_tag_text):str_alt_index + len(software)]
                            original_sub_tags_list[nb + 1] = ['software', p_string[str_alt_index : old_ref_tag_index], tail_software, str_alt_index,'software', attr_software, [original_sub_tags_list[nb + 1][0],old_ref_tag_text,new_tail_ref_sub,'ref_sub',original_sub_tags_list[nb + 1][5]]]
                            original_sub_tags_list[nb+1][2] = p_string[str_alt_index + len(software): original_sub_tags_list[nb +2][3]]
                            original_sub_tags_list = sorted(original_sub_tags_list, key=lambda x: x[3])
                            founded = True
                            break
                        else:
                            logger.critical(f'"{software}"(middle sub-ref) "{old_string}" ')
                #END
                except IndexError:
                    # SUB-CHILD
                    if str_alt_index >= original_sub_tags_list[len(original_sub_tags_list)-1][3]:
                        old_string = original_sub_tags_list[len(original_sub_tags_list)-1][2]
                        new_tail_prior_tag = p_string[original_sub_tags_list[len(original_sub_tags_list)-1][3] + len(original_sub_tags_list[len(original_sub_tags_list)-1][1]):str_alt_index]
                        tail_software = p_string[str_alt_index + len(software):]
                        if str_alt_index >= original_sub_tags_list[nb][3] and str_alt_index < original_sub_tags_list[nb][3] + len(original_sub_tags_list[nb][1]):
                            new_text_prior_tag = p_string[original_sub_tags_list[nb][3]:str_alt_index]
                            tail_software = p_string[str_alt_index + len(software):original_sub_tags_list[nb][3] + len(original_sub_tags_list[nb][1])]
                            if new_text_prior_tag + software + tail_software == original_sub_tags_list[nb][1]:
                                original_sub_tags_list[nb][1] = new_text_prior_tag
                                software_list = ['software', software, tail_software, 'software_sub', None]
                                original_sub_tags_list[nb].append(software_list)
                                logger.info(f'{software} was added to the list (end) as a sub-child')
                                list_len -= 1
                                original_sub_tags_list = sorted(original_sub_tags_list, key=lambda x: x[3])
                                founded = True
                                break
                            else:
                                logger.critical(f' {software}(end \ inside) ')
                        #NORMAL
                        if new_tail_prior_tag + software + tail_software == old_string:
                            software_list = ['software', software, tail_software, str_alt_index, 'software', attr_software]
                            original_sub_tags_list[len(original_sub_tags_list) - 1][2] = new_tail_prior_tag
                            original_sub_tags_list.append(software_list)
                            logger.info(f'{software} was added to the list (end)')
                            original_sub_tags_list = sorted(original_sub_tags_list, key=lambda x: x[3])
                            founded = True
                            break
                        else:
                            logger.critical(f' {software}(end) ')
                '''else:
                    print(software, context)'''
                original_sub_tags_list = sorted(original_sub_tags_list, key=lambda x: x[3])
                nb += 1
                founded = False

    original_sub_tags_list = sorted(original_sub_tags_list, key=lambda x: x[3])
    for elm in original_sub_tags_list:
        if elm[0] == 'software':
            for elm in list(p):
                p.remove(elm)
            break
        else:
            pass
    for elm in original_sub_tags_list:
        if len(elm) == 7:
            tag_name, tag_content, tail, index, type, attr, child_software = elm
        else:
            tag_name, tag_content, tail, index, type, attr = elm
            child_software = None

        tag = ET.Element(tag_name)
        tag.text = tag_content
        tag.tail = tail
        if attr != None:
            for keys, values in attr.items():
                tag.set(keys, values)
        if child_software:
            if len(child_software) == 3:
                software_child = ET.Element(child_software[0])
                software_child.text = child_software[1]
                software_child.tail = child_software[2]
                tag.insert(0, software_child)
            if child_software[4] != None:
                software_child = ET.Element(child_software[0])
                software_child.text = child_software[1]
                software_child.tail = child_software[2]
                if child_software[3] != None:
                    for keys, values in child_software[4].items():
                        software_child.set(keys, values)
                tag.insert(0, software_child)

        p.append(tag)
    return [p,context_list_found,mention_found]