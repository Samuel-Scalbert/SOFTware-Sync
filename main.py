import sys
from json_xml.json_xml import json_enhance_xml
from package_perso.utils import common_file_xml_json, setup_logger, common_file_xmlgrobid_xmlmeta
from meta_grobid_xml.xml_builder import xml_builder
import os
from tqdm import tqdm
from json_software_displayer.software_displayer import json_parser_csv

if __name__ == "__main__":

    super_logger = setup_logger('super_logger', 'super_logger.log')

    message = """Available options for SOFTware-Sync:

1. --enhance-dir : Enhance multiple XML files in a directory by associating them with corresponding JSON files.
   Usage: python main.py --enhance-dir <dir_xml_path> <dir_json_path>

2. --enhance-file : Enhance a single XML file by associating it with a JSON file.
   Usage: python main.py --enhance-file <xml_path> <json_path>

3. --builder : Build XML files by combining Grobid TEI XML and metadata XML files.
   Usage: python main.py --builder <xml_path_grobid> <xml_path_meta>

5. --help, -h : Display this message.
   Usage: python main.py --help

6. --check-XML-META : Check the number of XML files available against the number of metadata XML files.
   Usage: python main.py --check-XML-META <xml_path_grobid> <xml_path_meta>

7. --check-XML-JSON : Check the number of XML files available against the number of JSON files.
   Usage: python main.py --check-XML-JSON <xml_path> <json_path>
   
   pour le commit
            """

    if sys.argv[1] in ["--enhance-dir","--enhance-file","--builder","--checker-files","--help", "-h","--check-XML-META", "--check-XML-JSON", "--csv-creator"]:

        if sys.argv[1] in ["--help","-h"]:
            print(message)

        if sys.argv[1] == "--enhance-dir":
            dir_xml_path = sys.argv[2]
            dir_json_path = sys.argv[3]
            list_common_file = common_file_xml_json(dir_xml_path,dir_json_path)
            for file in tqdm(list_common_file, colour = 'red'):
                xml_path = dir_xml_path + file + '.grobid.tei.xml'
                json_path = dir_json_path + file + '.software.json'
                json_enhance_xml(xml_path, json_path,super_logger)

        if sys.argv[1] == "--enhance-file":
            xml_path = sys.argv[2]
            json_path = sys.argv[3]
            print(xml_path)
            json_enhance_xml(xml_path, json_path,super_logger)

        if sys.argv[1] == "--builder":
            xml_path_grobid = sys.argv[2]
            xml_path_meta = sys.argv[3]
            list_common = common_file_xmlgrobid_xmlmeta(xml_path_grobid, xml_path_meta)
            for filename in tqdm(list_common, colour = 'blue'):
                grobid_xml = xml_path_grobid + filename +'.grobid.tei.xml'
                meta_xml = xml_path_meta + filename + '.xml'
                xml_builder(meta_xml,grobid_xml, filename)

        if sys.argv[1] == "--check-XML-JSON":
            xml_path = sys.argv[2]
            json_path = sys.argv[3]
            list_pdf = os.listdir(xml_path)
            list_common_pdf_json = common_file_xml_json(xml_path,json_path)
            print(f'{len(list_common_pdf_json)}/{len(list_pdf)} json and XML')

        if sys.argv[1] == "--check-XML-META":
            xml_path = sys.argv[2]
            json_path = sys.argv[3]
            list_xml_meta = os.listdir(xml_path_meta)
            list_common_grobid_meta = common_file_xmlgrobid_xmlmeta(xml_path_grobid, xml_path_meta)
            print(f'{len(list_common_grobid_meta)}/{len(list_xml_meta)} xml_grobid and xml_meta')

        if sys.argv[1] == "--csv-creator":
            path_json = sys.argv[2]
            json_parser_csv(path_json)
    else:
        print(message)
