# SOFTware-Sync

## Overview

## Features
```
Available options for SOFTware-Sync:

    1. --enhance-dir : Enhance multiple XML files in a directory by associating them with corresponding JSON files.
       Usage: python main.py --enhance-dir <dir_xml_path> <dir_json_path>

    2. --enhance-file : Enhance a single XML file by associating it with a JSON file.
       Usage: python main.py --enhance-file <xml_path> <json_path>
       
       options available : "--project" / "--only-mention" 

    3. --builder : Build XML files by combining Grobid TEI XML and metadata XML files.
       Usage: python main.py --builder <xml_path_grobid> <xml_path_meta>

    4. --check-XML-META : Check the number of XML files available against the number of metadata XML files.
       Usage: python main.py --check-XML-META <xml_path_grobid> <xml_path_meta>

    5. --check-XML-JSON : Check the number of XML files available against the number of JSON files.
       Usage: python main.py --check-XML-JSON <xml_path> <json_path>

    6. --csv-creator : Create a csv to display the number of mentions and its occurrences of a software.
       Usage: python main.py --csv-creator <json_path>

    7. --mentions-checker : Check for empty JSON mentions files.
       Usage: python main.py --mentions-checker <json_path>

    8. --download-halid : Download files from Hal ID.
       Usage: python main.py --download-halid <csv_path>

    9. --help, -h : Display this message.
       Usage: python main.py --help
```
