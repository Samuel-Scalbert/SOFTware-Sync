import xml.etree.ElementTree as ET
from fuzzywuzzy import fuzz
from package_perso.utils import longest_common_substrings, find_closest_number, find_occurrences


def wizzard_xml_json2(p, software_mentions, logger):
    p_string = "".join(p.itertext())
    original_sub_tags_list = []
    context_list_found = []
    error_msg = []
    ET.register_namespace('', "http://www.tei-c.org/ns/1.0")
    if p_string == None:
        return None
    for elm in list(p):
        if elm.tail == None:
            elm.tail = ''
        if elm.text == None:
            elm.text = ''
        attributes_dict = elm.attrib if elm.attrib else None
        if len(original_sub_tags_list) <= 0:
            if p.text == None:
                index = 0
            else:
                index = len(p.text)
        else:
            index = original_sub_tags_list[-1][3] + len(original_sub_tags_list[-1][1]) + len(
                original_sub_tags_list[-1][2])
        if p_string[index:index + len(elm.text)] != elm.text:
            print('error')
        else:
            new_tag = [elm.tag, elm.text, elm.tail, index, "sub-element", attributes_dict]
        original_sub_tags_list.append(new_tag)

    full_list_software = []
    mention_found = []
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
            break
        if software.find('\n') != -1:
            software = software.replace("\n", "")
            offsetStart = software_mention["software-name"]["offsetStart"] - 2
            print(software)
        else:
            offsetStart = software_mention["software-name"]["offsetStart"]
        new_off = offsetStart
        if context[offsetStart:offsetStart + len(software)] != software:
            for i, char in enumerate(context):
                if ord(char) > 127 and i < offsetStart:
                    new_off -= 1
            if context[new_off:new_off + len(software)] == software:
                offsetStart = new_off
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
                if software_mention in mention_found:
                    pass
                else:
                    context_list_found.append([context, software_list[6]])
                    mention_found.append(software_mention)
            else:
                logger.critical(
                    f'error index (normal) software we found "{p_string[offsetStart_full_str: offsetStart_full_str + len(software)]}"')
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
                    if software_mention in mention_found:
                        pass
                    else:
                        context_list_found.append([context, software_list[6]])
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
                        if software_mention in mention_found:
                            pass
                        else:
                            context_list_found.append([context, software_list[6]])
                            mention_found.append(software_mention)
                    else:
                        logger.critical(f'error index (fuzzy) software for: {context}')
                else:
                    logger.critical(f'critical occurences, {software} {context}')
    if not full_list_software:
        return False
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

    dup = []
    founded_tags_software = []
    for tags in full_list_software:
        str_alt_index = tags[3]
        software = tags[1]
        nb = 0
        tag_founded = False
        for elm in range(len(original_sub_tags_list)):
            if str_alt_index == original_sub_tags_list[nb][3] and software == original_sub_tags_list[nb][1]:
                dup.append(software)
                logger.critical(f'duplicate {software}')
                break
        #START
            if str_alt_index <= original_sub_tags_list[nb][3] and nb == 0:
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
                    founded_tags_software.append(tags)
                    original_sub_tags_list = sorted(original_sub_tags_list, key=lambda x: x[3])
                    break
                else:
                    # DUP SOFTWARE
                    if str_alt_index == original_sub_tags_list[nb][3]:
                        break
                    logger.critical(f'{software} (start)')
                    break
        #MIDDLE
            try:
                if str_alt_index >= original_sub_tags_list[nb][3] and str_alt_index < original_sub_tags_list[nb+1][3]:
                    old_string = original_sub_tags_list[nb][2]
                    new_tail_prior_tag = p_string[original_sub_tags_list[nb][3] + len(original_sub_tags_list[nb][1]): str_alt_index]
                    tail_software =p_string[str_alt_index + len(software):original_sub_tags_list[nb+1][3]]
                    #NORMAL
                    if len(original_sub_tags_list[nb]) == 7:
                        new_tail_prior_tag = p_string[original_sub_tags_list[nb][3] + len(original_sub_tags_list[nb][1]) + len(original_sub_tags_list[nb][6][1]) + len(original_sub_tags_list[nb][6][2]) : str_alt_index]
                        if new_tail_prior_tag + software + tail_software == old_string:
                            software_list = ['software', software, tail_software, str_alt_index, 'software',
                                             attr_software]
                            original_sub_tags_list[nb][2] = new_tail_prior_tag
                            original_sub_tags_list.append(software_list)
                            founded_tags_software.append(tags)
                            logger.info(f'{software} was added to the list (middle)')
                            original_sub_tags_list = sorted(original_sub_tags_list, key=lambda x: x[3])
                            break
                        else:
                            logger.critical(f'{software} (middle)')
                            break
                    if len(original_sub_tags_list[nb]) == 6:
                        if new_tail_prior_tag + software + tail_software == old_string:
                            software_list = ['software', software, tail_software, str_alt_index, 'software',
                                             attr_software]
                            original_sub_tags_list[nb][2] = new_tail_prior_tag
                            original_sub_tags_list.append(software_list)
                            founded_tags_software.append(tags)
                            logger.info(f'{software} was added to the list (middle)')
                            original_sub_tags_list = sorted(original_sub_tags_list, key=lambda x: x[3])
                            break
                        else:
                            logger.critical(f'{software} (middle)')
                            break
            #END
            except IndexError:
                max_index = len(original_sub_tags_list)-1
                if str_alt_index >= original_sub_tags_list[max_index][3]:
                    old_string = p_string[original_sub_tags_list[max_index][3] + len(original_sub_tags_list[max_index][1]):]
                    new_tail_prior_tag = p_string[original_sub_tags_list[max_index][3] + len(original_sub_tags_list[max_index][1]):str_alt_index]
                    tail_software = p_string[str_alt_index + len(software):]
                    #NORMAL
                    if new_tail_prior_tag + software + tail_software == old_string:
                        software_list = ['software', software, tail_software, str_alt_index, 'software', attr_software]
                        original_sub_tags_list[max_index][2] = new_tail_prior_tag
                        original_sub_tags_list.append(software_list)
                        founded_tags_software.append(tags)
                        logger.info(f'{software} was added to the list (end)')
                        original_sub_tags_list = sorted(original_sub_tags_list, key=lambda x: x[3])
                        break
                    else:
                        #DUP SOFTWARE
                        if str_alt_index == original_sub_tags_list[max_index][3]:
                            break
                        logger.critical(f'{software} (end)')
                        break

            original_sub_tags_list = sorted(original_sub_tags_list, key=lambda x: x[3])
            nb += 1

    for unfounded_tag in full_list_software:
        if unfounded_tag not in founded_tags_software:
            for nb, tags in enumerate(original_sub_tags_list):
                str_alt_index = unfounded_tag[3]
                software = unfounded_tag[1]
                #SOFTWARE-SUB-CHILD
                if unfounded_tag[3] >= tags[3] and unfounded_tag[3] <= tags[3] + len(tags[1]):
                    if unfounded_tag[3] == tags[3] and unfounded_tag[1] == tags[1] and unfounded_tag[0] == tags[0]:
                        break
                    else:
                        new_text_tag = p_string[original_sub_tags_list[nb][3]:str_alt_index]
                        tail_software = p_string[str_alt_index + len(software) : original_sub_tags_list[nb][3]+len(original_sub_tags_list[nb][1])]
                        if new_text_tag + software + tail_software == original_sub_tags_list[nb][1]:
                            original_sub_tags_list[nb][1] = new_text_tag
                            software_list = ['software', software, tail_software, 'software_sub', None]
                            original_sub_tags_list[nb].append(software_list)
                            logger.info(f'{software} was added to the list (middle) as a sub-child')
                            original_sub_tags_list = sorted(original_sub_tags_list, key=lambda x: x[3])
                            break
                        else:
                            logger.critical(f'{software}(inside software)')
                            break
                #TAG-SUB-CHILD
                if unfounded_tag[3] < tags[3] and (unfounded_tag[3] + len(unfounded_tag[1])) > (tags[3] + len(tags[1])):
                    new_software_tail = p_string[str_alt_index+len(software):tags[3]+ len(tags[1]) +len(tags[2])]
                    new_software_text = p_string[str_alt_index:tags[3]]
                    new_sub_tail = p_string[tags[3]+len(tags[1]):str_alt_index+len(software)]
                    if p_string[str_alt_index:tags[3]+len(tags[1])+len(tags[2])] == new_software_text + tags[1] + new_sub_tail + new_software_tail:
                        new_child = [tags[0], tags[1], new_sub_tail, 'child_sub', tags[5]]
                        tags = ['software', new_software_text, new_software_tail, str_alt_index,'software',unfounded_tag[5],new_child]
                        original_sub_tags_list[nb] = tags
                    else:
                        logger.critical(f'{software}(inside ref)')

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
        if tag_content == '':
            logger.critical(f'empty tag for {elm}')
            pass
        tag.tail = tail
        if attr != None:
            for keys, values in attr.items():
                tag.set(keys, values)
        if child_software:
            software_child = ET.Element(child_software[0])
            software_child.text = child_software[1]
            software_child.tail = child_software[2]
            if child_software[4] is not None:
                for keys, values in child_software[4].items():
                    software_child.set(keys, values)
            tag.insert(0, software_child)
        p.append(tag)
    return [p,context_list_found,mention_found, dup]