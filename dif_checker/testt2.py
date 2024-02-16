import xml.etree.ElementTree as ET
def wizzard_xml_json(context, offsetStart,offsetEnd,software, p):
    p_string = "".join(p.itertext())
    sub_tags_list = []
    ET.register_namespace('', "http://www.tei-c.org/ns/1.0")

    index_context = p_string.find(context)
    if index_context != -1:
        offsetStart_full_str = index_context + offsetStart
        offsetEnd_full_str = index_context + offsetEnd
        p_string_alt = p_string[:offsetStart_full_str] + "@" + software
        p_string_alt += p_string[offsetEnd_full_str:]
        str_alt_index = p_string_alt.find("@" + software)
        #print(p_string_alt)
        list_p = list(p)
        for elm in list_p:
            index = p_string.find(elm.text)
            if index != -1:
                if elm.tag == "software":
                    sub_tags_list.append([elm.tag, elm.text, elm.tail, index, "software"])
                else:
                    sub_tags_list.append([elm.tag, elm.text, elm.tail, index, "sub-element"])
            p.remove(elm)

        sub_tags_list = sorted(sub_tags_list, key=lambda x: x[3])
        nb = 0
        for tag_name, tag_content, tail, index, type in sub_tags_list:
            if str_alt_index != -1 and nb == 0:
                if str_alt_index < sub_tags_list[nb][3]:
                    p.text = p_string_alt[:str_alt_index]
                    tail_software = p_string_alt[str_alt_index + 1 + len(software):sub_tags_list[nb][3]]
                    software_list = ['software', software, tail_software, str_alt_index, 'software']
                    sub_tags_list = sub_tags_list[:nb] + [software_list] + sub_tags_list[nb:]
            nb += 1
            if str_alt_index != -1:
                try:
                    if str_alt_index > index and str_alt_index < sub_tags_list[nb][3]:
                        sub_tags_list[nb-1][2] = p_string_alt[index-1:str_alt_index]
                        tail_software = p_string_alt[str_alt_index + 1 + len(software):sub_tags_list[nb][3]]
                        software_list = ['software', software, tail_software,str_alt_index,'software']
                        sub_tags_list = sub_tags_list[:nb] + [software_list] + sub_tags_list[nb:]
                except IndexError:
                    if str_alt_index > sub_tags_list[len(sub_tags_list)-1][3]:
                        sub_tags_list[nb - 1][2] = p_string_alt[index - 1:str_alt_index]
                        tail_software = p_string_alt[str_alt_index + 1 + len(software):]
                        software_list = ['software', software, tail_software, str_alt_index, 'software']
                        sub_tags_list = sub_tags_list[:nb] + [software_list] + sub_tags_list[nb:]

        for tag_name, tag_content, tail, index, type in sub_tags_list:
            tag = ET.Element(tag_name)
            tag.tail = tail
            if type == "software":
                print("found one !", index, tag_content)
                if tag_content == software:
                    tag.text = tag_content
                else :
                    print("problem with :", software)
            else:
                tag.text = tag_content
            p.append(tag)

        return p
    else:
        return p
    #print(modified_xml)


'''
xml = ('<root><p>The importance of allele-specific PCR systems for reliable SNP typing has been demonstrated several times in previous studies <ref type="bibr" target="#b55">(Wu et al., 1989;</ref><ref type="bibr" target="#b53">Wei et al., 2006)</ref>. Introduction of additional mismatch bases has improved the specificity of this technique <ref type="bibr" target="#b11">(Drenkard et al., 2000)</ref>. Its application is especially important for an accurate discrimination of different alleles in MAS. In the present study, only one pair of ASPs was used to amplify the specific products from the dehydration-tolerant and sensitive accessions. Therefore, the ASM can be effectively used to type SNPs as well as to avoid unambiguous false scoring. The functional differences in trait performance mainly caused by SNPs has also been reported in previous studies on several cloned genes <ref type="bibr" target="#b38">(Peng et al., 1999;</ref><ref type="bibr" target="#b50">Takahashi et al., 2001;</ref><ref type="bibr" target="#b29">Liu et al., 2002;</ref><ref type="bibr" target="#b22">Jin et al., 2003;</ref><ref type="bibr" target="#b52">Toshiyuki et al., 2003;</ref><ref type="bibr" target="#b24">Kim et al., 2005;</ref><ref type="bibr" target="#b17">Garce ´s-Claver et al., 2007;</ref><ref type="bibr" target="#b15">Fan et al., 2009)</ref>. Molecular markerassisted breeding technology is a rapid and accurate method for any candidate gene, providing a very effective tool for backcross breeding <ref type="bibr" target="#b8">(Collard and Mackill, 2008)</ref>. MAS efficiency is influenced by several complex factors such as recombination between the marker and the candidate gene, a low level of polymorphism between the parents with contrasting traits, and lower resolution of quantitative trait loci (QTLs) due to environmental interactions. In the present study, the ASM is part of the candidate gene, thus eliminating the main disadvantage of MAS. However, the ASM developed in this study is a dominant marker, and therefore it cannot distinguish the heterozygotes. The marker has high reliability and efficiency, and the desired PCR product can be identified easily on a simple agarose gel. With the help of this marker, dehydration-tolerant accessions can be selected at a variety of life stages. This is particularly true when the target is the dehydration-tolerant allele in backcross breeding and thus the foxtail millet breeding process can be accelerated. Further, the ASM identified would facilitate allele mining of foxtail millet germplasm resources, thereby leading to identification and utilization of newer alleles in crop improvement.</p></root>')
root = ET.fromstring(xml)

context = "The reliability of the model structure was tested using the ENERGY commands of MODELLER (Sali and Blundell, 1993)."
offsetStart = 79
offsetEnd = 87
software = "MODELLER"

context = "The modelled structures were also validated using the program PROSA (Wiederstein and Sippl, 2007)."
offsetStart = 62
offsetEnd = 67
software = "PROSA"


context = "MAS efficiency is influenced by several complex factors such as recombination between the marker and the candidate gene, a low level of polymorphism between the parents with contrasting traits, and lower resolution of quantitative trait loci (QTLs) due to environmental interactions."
offsetStart = 0
offsetEnd = 3
software = "MAS"

p = root.find('p')
'''