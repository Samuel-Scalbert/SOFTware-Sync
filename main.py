import logging
import json
import sys
from bs4 import BeautifulSoup
import string
import re
from dif_checker.dif_checker import xml_enhance_json

# Entry point of the script
if __name__ == "__main__":
    # Check if the correct number of command line arguments is provided
    if len(sys.argv) != 4:
        print("Usage: python your_script_name.py <script.py> <xml_path> <json_path>")
        sys.exit(1)

    # Extract XML and JSON file paths from command line arguments
    xml_path = sys.argv[2]
    json_path = sys.argv[3]

    if sys.argv[1] == "--dif":
        xml_enhance_json(xml_path, json_path)
        #print("// DIF_CHECKER ====> info logged in dif_checker.log")
