import sys
from dif_checker.dif_checker import json_enhance_xml
from dif_checker.utils import common_file, setup_logger
from tqdm import tqdm

if __name__ == "__main__":

    super_logger = setup_logger('super_logger', 'super_logger.log')

    if len(sys.argv) != 4:
        print("Usage: python your_script_name.py '--dif or --enhance-file' <xml_path> <json_path>")
        sys.exit(1)

    if sys.argv[1] == "--enhance-dir":
        dir_xml_path = sys.argv[2]
        dir_json_path = sys.argv[3]
        list_common_file = common_file(dir_xml_path,dir_json_path)
        #for file in tqdm(list_common_file, desc="Traitement en cours", bar_format="{l_bar}{bar:10}{r_bar}"):
        for file in list_common_file:
            xml_path = dir_xml_path + file + '.grobid.tei.xml'
            json_path = dir_json_path + file + '.software.json'
            print(xml_path)
            json_enhance_xml(xml_path, json_path,super_logger)

    if sys.argv[1] == "--enhance-file":
        xml_path = sys.argv[2]
        json_path = sys.argv[3]
        print(xml_path)
        json_enhance_xml(xml_path, json_path,super_logger)
