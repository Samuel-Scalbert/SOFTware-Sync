<p align="center">
    <h1 align="center">SOFTWARE-SYNC</h1>
</p>
<p align="center">
    <em>Efficient Python Tools for Enhanced Software Sync</em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/Samuel-Scalbert/SOFTware-Sync?style=default&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/Samuel-Scalbert/SOFTware-Sync?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/Samuel-Scalbert/SOFTware-Sync?style=default&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/Samuel-Scalbert/SOFTware-Sync?style=default&color=0080ff" alt="repo-language-count">
<p>
<p align="center">
	<!-- default option, no dependency badges. -->
</p>

<br><!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary><br>

- [ Overview](#-overview)
- [ Features](#-features)
- [ Repository Structure](#-repository-structure)
- [ Modules](#-modules)
- [ Getting Started](#-getting-started)
  - [ Installation](#-installation)
  - [ Usage](#-usage)
  - [ Tests](#-tests)
- [ Project Roadmap](#-project-roadmap)
- [ Contributing](#-contributing)
- [ License](#-license)
- [ Acknowledgments](#-acknowledgments)
</details>
<hr>

##  Overview

### Purpose:

The SOFTware-Sync application processes sets of XML or PDF files generated by GROBID, alongside JSON result files from SOFTCITE, to produce either enhanced XML files or CSV files summarizing software mentions.

#### Input File Types:

GROBID Outputs: XML or PDF files containing structured information extracted from scholarly documents.
SOFTCITE Outputs: JSON files containing results of software citation detection.

#### Output Options:

Enhanced XML Files: XML files augmented with details of every software mentioned in the input documents.
CSV Summary Files: CSV files listing every software mention detected across the input documents, along with relevant metadata.---

##  Features

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

---

##  Repository Structure

```sh
└── SOFTware-Sync/
    ├── README.md
    ├── dif_checker
    │   ├── __init__.py
    │   └── checker.py
    ├── error_grobid.txt
    ├── json_software_displayer
    │   ├── __init__.py
    │   └── software_displayer.py
    ├── json_xml
    │   ├── __init__.py
    │   ├── json_xml.py
    │   ├── software_tags_count.py
    │   └── wizzard.py
    ├── main.py
    ├── meta_grobid_xml
    │   ├── __init__.py
    │   ├── scrapper.py
    │   └── xml_builder.py
    ├── package_perso
    │   ├── __init__.py
    │   └── utils.py
    ├── requirements.txt
    ├── result
    │   ├── XML_meta_software
    │   └── XML_software
    └── venv
        ├── .gitignore
        ├── bin
        └── pyvenv.cfg
```

---

##  Modules

<details closed><summary>.</summary>

| File                                                                                              | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ---                                                                                               | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| [requirements.txt](https://github.com/Samuel-Scalbert/SOFTware-Sync/blob/master/requirements.txt) | This file is a requirements list (`requirements.txt`) for the SOFTware-Sync repository. It specifies versions for dependencies needed to run this project, including libraries like `aiohttp`, `lxml`, `numpy`, and `requests`. By managing these prerequisites efficiently, this codebase ensures seamless interaction with various data formats during the synchronization process of software information from different sources.                                                                                                                                                                                                                                                                       |
| [main.py](https://github.com/Samuel-Scalbert/SOFTware-Sync/blob/master/main.py)                   | The script is designed to perform tasks related to software tags, data structures creation, XML-JSON compatibility checks, csv generation, and file enhancements for a project. Upon receiving command line arguments, it creates directories, processes XML/JSON files, counts software tags in files, builds XMLs, and generates CSVs based on requirements. Additionally, it checks for mentions and downloads files from HALID according to specific commands.                                                                                                                                                                                                                                         |
| [error_grobid.txt](https://github.com/Samuel-Scalbert/SOFTware-Sync/blob/master/error_grobid.txt) | This text file, `error_grobid.txt`, is a log for documenting issues encountered during the process of extracting and parsing scientific articles related to software using Grobid, an OCR tool for extracting text and metadata from PDF documents. The recorded errors include missing or duplicate references, improper XML structure in specific files (e.g., hal-03659476.grobid.tei.xml), and instances where the software name cannot be extracted correctly from the text content, such as in hal-03882318.grobid.tei.xml where nnU-Net was not recognized as expected. The data within this file is crucial for maintaining the integrity and accuracy of software metadata within the repository. |

</details>

<details closed><summary>venv.bin</summary>

| File                                                                                                           | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ---                                                                                                            | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| [xmlschema-xml2json](https://github.com/Samuel-Scalbert/SOFTware-Sync/blob/master/venv/bin/xmlschema-xml2json) | This script converts XML schemas to JSON format, facilitating seamless data exchange within the SOFTware-Sync repository by utilizing the `xml2json` tool. The conversion process streamlines software metadata handling and supports open-source project integration.                                                                                                                                                                                                                                     |
| [xmlschema-validate](https://github.com/Samuel-Scalbert/SOFTware-Sync/blob/master/venv/bin/xmlschema-validate) | Validates XML files according to predefined schema in the given repositorys architecture, ensuring consistency and correctness within the software metadata structure. This script leverages xmlschema', enhancing the data quality during software synchronization process.                                                                                                                                                                                                                               |
| [xmlschema-json2xml](https://github.com/Samuel-Scalbert/SOFTware-Sync/blob/master/venv/bin/xmlschema-json2xml) | Transforms JSON data into well-formatted XML using the `xmlschema-json2xml` utility, enhancing compatibility with existing XML software within the repositorys architecture. This tool is critical for seamless information exchange in our open-source SOFTware-Sync project.                                                                                                                                                                                                                             |
| [wheel3.10](https://github.com/Samuel-Scalbert/SOFTware-Sync/blob/master/venv/bin/wheel3.10)                   | This Python script acts as a runner for wheel3.10, a package essential for creating wheel distribution packages within the software synchronization projects virtual environment (venv), contributing to smoother deployment and installation processes in open-source collaborations.                                                                                                                                                                                                                     |
| [wheel3](https://github.com/Samuel-Scalbert/SOFTware-Sync/blob/master/venv/bin/wheel3)                         | The `wheel3` script streamlines software package deployment within the repositorys Python environment by executing the `wheel` command for efficient packaging and distribution. This enhancement speeds up the installation process across diverse Python environments, thereby promoting project scalability and compatibility.                                                                                                                                                                          |
| [wheel-3.10](https://github.com/Samuel-Scalbert/SOFTware-Sync/blob/master/venv/bin/wheel-3.10)                 | The wheel script within the SOFTware-Sync repositorys virtual environment bootstraps and runs the Wheel CLI. This tool, when executed, assists in creating Python software packages that can be efficiently installed across multiple platforms. It streamlines the deployment process as a key part of the larger software synchronization workflow.                                                                                                                                                      |
| [wheel](https://github.com/Samuel-Scalbert/SOFTware-Sync/blob/master/venv/bin/wheel)                           | This script, named `wheel`, serves as the executable entrypoint within the `venv` environment of the `SOFTware-Sync` repository. It interacts with the wheel command line tool to manage Python packages and their distributions, thereby streamlining dependency handling in the project.                                                                                                                                                                                                                 |
| [tqdm](https://github.com/Samuel-Scalbert/SOFTware-Sync/blob/master/venv/bin/tqdm)                             | Boosts progress monitoring during script executionFile: tqdm' is a python script that wraps other scripts and adds a progress bar using tqdm library. This enables the user to keep track of task advancement within the repository's software synchronization workflows.                                                                                                                                                                                                                                  |
| [pip3.10](https://github.com/Samuel-Scalbert/SOFTware-Sync/blob/master/venv/bin/pip3.10)                       | In this codebase, the script located at `venv/bin/pip3.10` serves as the primary entry point for executing pip commands, an essential package manager for Python projects. By calling this script, users can easily install, update, or remove packages in accordance with the project requirements specified in the repositorys `requirements.txt` file. The centralization of these operations within the script helps manage the projects dependencies effectively and consistently.                    |
| [pip3](https://github.com/Samuel-Scalbert/SOFTware-Sync/blob/master/venv/bin/pip3)                             | This file, located in the projects virtual environment, triggers the main function of pip to install packages specified in requirements.txt when called with the command pip3'. By doing so, it ensures that the project's dependencies are consistently met across different environments.                                                                                                                                                                                                                |
| [pip-3.10](https://github.com/Samuel-Scalbert/SOFTware-Sync/blob/master/venv/bin/pip-3.10)                     | The Python script located at `venv/bin/pip-3.10` initiates the command-line interface for package management using the pip tool within the projects virtual environment, enabling seamless software installation and updates in the broader Software Sync repository architecture.                                                                                                                                                                                                                         |
| [pip](https://github.com/Samuel-Scalbert/SOFTware-Sync/blob/master/venv/bin/pip)                               | In this software repository, titled Software-Sync, the script within the `venv/bin/pip` file acts as an entry point to manage Python package installation. Specifically, it executes the main command for Pip (Pythons dependency manager), ensuring correct and up-to-date dependencies across different modules of the project.                                                                                                                                                                          |
| [openai](https://github.com/Samuel-Scalbert/SOFTware-Sync/blob/master/venv/bin/openai)                         | A command-line interface for the SOFTware-Sync repository. The script activates the openAI module, enabling users to interact with it within the project environment. This enhances the repository's capabilities, facilitating seamless integration of AI functionalities with software analysis tools.                                                                                                                                                                                                   |
| [normalizer](https://github.com/Samuel-Scalbert/SOFTware-Sync/blob/master/venv/bin/normalizer)                 | In the software repository, normalizer' is a tool residing within the virtual environment. Its core function is to normalize character encoding by executing the command-line interface of the charset-normalizer library when called as main script, ensuring consistent text representation throughout the project."                                                                                                                                                                                     |
| [nltk](https://github.com/Samuel-Scalbert/SOFTware-Sync/blob/master/venv/bin/nltk)                             | This script initiates NLTK within the SOFTware-Sync virtual environment. NLTK is a powerful library for natural language processing (NLP) tasks, integral to analyzing text data for software documentation projects within this repository. By utilizing NLTK, it contributes significantly to enriching metadata analysis and enabling comprehensive text processing in our software sync application.                                                                                                   |
| [httpx](https://github.com/Samuel-Scalbert/SOFTware-Sync/blob/master/venv/bin/httpx)                           | The provided Python script, named `httpx`, serves as an entry point for executing the core functionality of the `httpx` library within the projects virtual environment (venv). This enables users to easily interact with HTTP requests and responses without explicitly importing or invoking specific classes, thereby simplifying interaction and usage in the context of this software synchronization tool.                                                                                          |
| [distro](https://github.com/Samuel-Scalbert/SOFTware-Sync/blob/master/venv/bin/distro)                         | In the Software-Sync repository, the distro script serves as the entrypoint for the Distro toolkit. It facilitates the analysis and classification of software packages based on their metadata. By invoking this script, users initiate a process that gathers, processes, and organizes software data for further exploration or comparison. The Distro library leverages powerful machine learning models to enrich the understanding of various software entities within the repositorys architecture. |
| [activate_this.py](https://github.com/Samuel-Scalbert/SOFTware-Sync/blob/master/venv/bin/activate_this.py)     | This script is used to activate a virtual environment within the given Python interpreter during execution, ensuring that the project uses its own specific library dependencies. It modifies the systems PATH and import mechanisms, thereby isolating the software environment.                                                                                                                                                                                                                          |
| [activate.ps1](https://github.com/Samuel-Scalbert/SOFTware-Sync/blob/master/venv/bin/activate.ps1)             | Activates the project environment, managing paths for efficient functioning of open-source software comparison tool, which automates data retrieval and analysis on software projects stored in the repositorys subdirectories. This enables seamless comparisons between various software packages, facilitating informed decision-making.                                                                                                                                                                |
| [activate.nu](https://github.com/Samuel-Scalbert/SOFTware-Sync/blob/master/venv/bin/activate.nu)               | Activates a Python virtual environment for the software synchronization toolset in the XML_JSON_format project. The script ensures correct PATH variable management and prompts appropriate during usage, enhancing consistency within the project ecosystem.                                                                                                                                                                                                                                              |
| [activate.fish](https://github.com/Samuel-Scalbert/SOFTware-Sync/blob/master/venv/bin/activate.fish)           | Activates a virtual environment for the Software-Sync project, enabling the proper functioning of its Python dependencies by adjusting the system's PATH and other environmental variables accordingly. This facilitates smooth execution within the project's intended scope.                                                                                                                                                                                                                             |
| [activate.csh](https://github.com/Samuel-Scalbert/SOFTware-Sync/blob/master/venv/bin/activate.csh)             | This script sets up an environment within the given directory structure, allowing seamless utilization of the projects various modules, such as JSON-XML conversion, metadata extraction, and error handling. The activation triggers updates to PATH, prompts, and aliases accordingly, enhancing the usability of the software sync application.                                                                                                                                                         |
| [activate](https://github.com/Samuel-Scalbert/SOFTware-Sync/blob/master/venv/bin/activate)                     | This script initiates a dedicated Python environment within the users current terminal session. Its primary purpose is to ensure that only the designated packages associated with this specific project are utilized when working, improving compatibility and promoting efficient resource usage.                                                                                                                                                                                                        |

</details>

<details closed><summary>package_perso</summary>

| File                                                                                            | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ---                                                                                             | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| [utils.py](https://github.com/Samuel-Scalbert/SOFTware-Sync/blob/master/package_perso/utils.py) | Dict_cleaner(dict1)`: Removes any key from a dictionary if its value is 0.2. `mention_checker(json_path)`: Identifies empty mentions in a directory of JSON files.3. `common_file_xmlgrobid_xmlmeta(xml_path_GROBID, xml_path_META)`: Finds common files between two directories (in this case, GROBID and META).4. `setup_logger(name, log_file, level=logging.DEBUG)`: Creates and sets up a logger instance for writing messages to a specified log file.5. `setup_logger_main(name, log_file, level=logging.DEBUG)`: Sets up the main logger, similar to the above function.6. `common_file_xml_json(dir_xml_path, dir_json_path)`: Finds common files between two directories, this time with.xml and.software.json file extensions.7. `find_occurrences(word, text)`: Detects the positions of a specific word within a given text string.8. `contains_special_characters(text)`: Determines if a text contains any special characters.9. `find_clos |

</details>

<details closed><summary>meta_grobid_xml</summary>

| File                                                                                                          | Summary                                                                                                                                                                                                                       |
| ---                                                                                                           | ---                                                                                                                                                                                                                           |
| [xml_builder.py](https://github.com/Samuel-Scalbert/SOFTware-Sync/blob/master/meta_grobid_xml/xml_builder.py) | Combines Grobid XML output with metadata, building enriched TEI Corpus XML for further analysis. Essential for amalgamating semantic information and refining software extraction within the Software-Sync projects workflow. |
| [scrapper.py](https://github.com/Samuel-Scalbert/SOFTware-Sync/blob/master/meta_grobid_xml/scrapper.py)       | Download_by_type()` and `downloader_halid()`. The latter function reads in uris from a specified CSV path.                                                                                                                    |

</details>

<details closed><summary>json_xml</summary>

| File                                                                                                                   | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ---                                                                                                                    | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| [wizzard.py](https://github.com/Samuel-Scalbert/SOFTware-Sync/blob/master/json_xml/wizzard.py)                         | This script parses text and generates XML tags based on identified software names with sub-children (if any). It prioritizes matching software at appropriate depths within the XML structure. The parsed XML is returned, with empty tags skipped and improper matches logged for error handling.                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [software_tags_count.py](https://github.com/Samuel-Scalbert/SOFTware-Sync/blob/master/json_xml/software_tags_count.py) | In this open-source project named SOFTware-Sync, the focus lies on counting the number of software entries within an XML file. The function `software_counts(xml_file)` in the `json_xml/software_tags_count.py` module accomplishes this task, facilitating a swift assessment of the total software instances within the given XML structure. This is a vital feature, particularly in managing large-scale software collections within the project's broader architecture.                                                                                                                                                                                                                                                              |
| [json_xml.py](https://github.com/Samuel-Scalbert/SOFTware-Sync/blob/master/json_xml/json_xml.py)                       | This script is analyzing XML data from a TEI file to identify and count software mentions, their types, and their occurrences within specific contexts. It compares the identified software mentions with software tags within the same XML file, ensuring all software instances are accounted for. The goal is to ensure the accuracy of software identification and provide statistics about the software mentioned, their types, and their occurrence counts. If any discrepancies are found, a critical log entry is created along with appropriate logs to be moved into a specific folder for later inspection. Finally, the modified XML data (with new software tags) is saved back to its original file, appended with.software. |

</details>

<details closed><summary>json_software_displayer</summary>

| File                                                                                                                                | Summary                                                                                                                                                                                                                                                                                      |
| ---                                                                                                                                 | ---                                                                                                                                                                                                                                                                                          |
| [software_displayer.py](https://github.com/Samuel-Scalbert/SOFTware-Sync/blob/master/json_software_displayer/software_displayer.py) | Analyzes and compiles JSON files within a specific directory into a CSV file, sorted by software mentions according to their frequency. This tool, `software_displayer.py`, contributes to the SOFTware-Sync repository by providing insights about software mentions in the collected data. |

</details>

<details closed><summary>dif_checker</summary>

| File                                                                                              | Summary                                                                                                                                                                                                                                                                                                                                        |
| ---                                                                                               | ---                                                                                                                                                                                                                                                                                                                                            |
| [checker.py](https://github.com/Samuel-Scalbert/SOFTware-Sync/blob/master/dif_checker/checker.py) | This file, `dif_checker/checker.py`, compares two XML files containing structured text data by traversing their div and p elements. It identifies matches (similar text content) or differences in the compared elements for further analysis, serving a crucial role in software document comparison within the broader Repository Structure. |

</details>

---

##  Getting Started

**System Requirements:**

* **Python**: `version x.y.z`

###  Installation

<h4>From <code>source</code></h4>

> 1. Clone the SOFTware-Sync repository:
>
> ```console
> $ git clone https://github.com/Samuel-Scalbert/SOFTware-Sync
> ```
>
> 2. Change to the project directory:
> ```console
> $ cd SOFTware-Sync
> ```
>
> 3. Install the dependencies:
> ```console
> $ pip install -r requirements.txt
> ```

###  Usage

<h4>From <code>source</code></h4>

> Run SOFTware-Sync using the command below:
> ```console
> $ python main.py
> ```

###  Tests

> Run the test suite using the command below:
> ```console
> $ pytest
> ```

---

##  Project Roadmap

- [X] `► INSERT-TASK-1`
- [ ] `► INSERT-TASK-2`
- [ ] `► ...`

---

##  Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Report Issues](https://github.com/Samuel-Scalbert/SOFTware-Sync/issues)**: Submit bugs found or log feature requests for the `SOFTware-Sync` project.
- **[Submit Pull Requests](https://github.com/Samuel-Scalbert/SOFTware-Sync/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
- **[Join the Discussions](https://github.com/Samuel-Scalbert/SOFTware-Sync/discussions)**: Share your insights, provide feedback, or ask questions.

<details closed>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your github account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone https://github.com/Samuel-Scalbert/SOFTware-Sync
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to github**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!
</details>

<details closed>
<summary>Contributor Graph</summary>
<br>
<p align="center">
   <a href="https://github.com{/Samuel-Scalbert/SOFTware-Sync/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=Samuel-Scalbert/SOFTware-Sync">
   </a>
</p>
</details>

---

##  License

This project is protected under the [SELECT-A-LICENSE](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.

---

##  Acknowledgments

- List any resources, contributors, inspiration, etc. here.

[**Return**](#-overview)

---

