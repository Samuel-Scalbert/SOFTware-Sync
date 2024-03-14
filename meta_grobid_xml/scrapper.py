import os
import requests
import time
from tqdm import tqdm

def is_file_in_directory(directory, filename_list, type):
    original_len = len(filename_list)
    for filename in filename_list:
        filename_name = filename.replace('https://hal.science/','')
        file_path = os.path.join(directory, filename_name + type)
        if os.path.exists(file_path):
            print(file_path)
            filename_list.remove(filename)
    print(f'{original_len} -> {len(filename_list)}')
    return filename_list


def fetch_uris(year, file_type):
    list_uri = []
    list_types_uris = {}
    base_url = "https://api.archives-ouvertes.fr/"
    endpoint = "search"
    collection = "INRIA2"
    params = {
        "q": f"producedDateY_i:{year} AND domain_s:0.info AND (submitType_s:file OR annex)",
        "fl": "uri_s, fulltext_t",
        "fq": f"docType_s:{file_type}",
        "wt": "json",
        "rows": 5  # You can adjust the number of rows per request
    }

    response = requests.get(f"{base_url}{endpoint}/{collection}", params=params)

    #print(f"Status Code for URIS: {response.status_code}")
    #print(response.json())

    data = response.json()
    uris = [doc["uri_s"] for doc in data.get("response", {}).get("docs", [])]
    if len(uris) != 0:
        for single_uris in tqdm(uris, desc=file_type, colour="blue"):
            time.sleep(0.1)
            list_uri.append(single_uris)
        list_types_uris[file_type] = list_uri
        return list_types_uris


def download_tei_by_id(type_uris_dic):
    # Create the 'downloads' directory if it doesn't exist
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    error = 0

    # Extract the first key and its corresponding value
    type_str = next(iter(type_uris_dic.keys()))
    uris_list = next(iter(type_uris_dic.values()))

    # Create a subdirectory for the specific type
    download_directory = os.path.join('downloads', type_str)
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)

    uris_list = is_file_in_directory('downloads/BRE', uris_list, '.pdf')

    for uris_id in tqdm(uris_list):
        time.sleep(0.1)
        # Construct the full URL using the provided ID
        pdf_url = f'{uris_id}/tei'

        # Send an HTTP GET request to the PDF URL
        try:
            response = requests.get(pdf_url)
            response.raise_for_status()  # Raise an exception for bad responses

            # Extract the filename from the URL
            filename = os.path.join(download_directory, os.path.basename(uris_id) + '.xml')

            # Save the PDF content to a local file
            with open(filename, 'wb') as pdf_file:
                pdf_file.write(response.content)

            # Print information about the downloaded file
            # print(f"{uris_id} downloaded successfully. Size: {file_size_mb} bytes")
        except Exception as e:
            try:
                pdf_url = pdf_url.replace('hal.science', 'inria.hal.science')
                response = requests.get(pdf_url)
                response.raise_for_status()  # Raise an exception for bad responses

                # Extract the filename from the URL
                filename = os.path.join(download_directory, os.path.basename(uris_id) + '.xml')

                # Save the PDF content to a local file
                with open(filename, 'wb') as pdf_file:
                    pdf_file.write(response.content)

                # Print information about the downloaded file
                # print(f"{uris_id} downloaded successfully. Size: {file_size_mb} bytes")
            except Exception as e:
                error += 1
                print(f"Error for {pdf_url}: {e}")
    print(error)

def download_xml_by_id(type_uris_dic):
    # Create the 'downloads' directory if it doesn't exist
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    error = 0

    # Extract the first key and its corresponding value
    type_str = next(iter(type_uris_dic.keys())) + '_xml'
    uris_list = next(iter(type_uris_dic.values()))

    # Create a subdirectory for the specific type
    download_directory = os.path.join('downloads', type_str)
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)

    uris_list = is_file_in_directory('downloads/BRE_xml',uris_list, '.xml')

    for uris_id in tqdm(uris_list):
        time.sleep(0.1)
        # Construct the full URL using the provided ID
        pdf_url = f'{uris_id}/tei'

        # Send an HTTP GET request to the PDF URL
        try:
            response = requests.get(pdf_url)
            response.raise_for_status()  # Raise an exception for bad responses

            # Extract the filename from the URL
            filename = os.path.join(download_directory, os.path.basename(uris_id) + '.xml')

            # Save the PDF content to a local file
            with open(filename, 'wb') as pdf_file:
                pdf_file.write(response.content)

            # Get the size of the downloaded file
            file_size_bytes = os.path.getsize(filename)
            file_size_mb = file_size_bytes / (1024 * 1024)

            # Print information about the downloaded file
            #print(f"{uris_id} downloaded successfully. Size: {file_size_mb} bytes")
        except Exception as e:
            try:
                pdf_url = pdf_url.replace('hal.science','inria.hal.science')
                response = requests.get(pdf_url)
                response.raise_for_status()  # Raise an exception for bad responses

                # Extract the filename from the URL
                filename = os.path.join(download_directory, os.path.basename(uris_id) + '.xml')

                # Save the PDF content to a local file
                with open(filename, 'wb') as pdf_file:
                    pdf_file.write(response.content)

                # Get the size of the downloaded file
                file_size_bytes = os.path.getsize(filename)
                file_size_mb = file_size_bytes / (1024 * 1024)

                # Print information about the downloaded file
                # print(f"{uris_id} downloaded successfully. Size: {file_size_mb} bytes")
            except Exception as e:
                error += 1
                print(f"Error for {pdf_url}: {e}")
    print(error)

#file_available_type = ["ART"]

file_available_type = ["ART", "COMM", "COUV", "THESE", "OUV", "UNDEFINED", "MEM", "REPORT", "CREPORT", "OTHER", "POSTER", "ISSUE", "NOTICE", "PROCEEDINGS", "BLOG", "HDR", "LECTURE", "TRAD", "PRESCONF", "MAP", "OTHERREPORT", "NOTE", "SYNTHESE", "REPACT", "ETABTHESE", "MEMLIC", "MANUAL", "DOUV"]


URIS_BRE = {'BRE': ['https://hal.science/hal-03740562', 'https://hal.science/hal-03540862', 'https://hal.science/hal-03580636', 'https://hal.science/hal-03898326', 'https://hal.science/hal-03897633', 'https://hal.science/hal-03921708', 'https://hal.science/hal-03531059', 'https://hal.science/hal-03768331', 'https://hal.science/hal-03773490', 'https://hal.science/hal-03776449', 'https://hal.science/hal-03937259', 'https://hal.science/hal-03860955', 'https://hal.science/hal-03777858', 'https://hal.science/hal-03776452', 'https://hal.science/tel-03666840', 'https://hal.science/hal-03819744', 'https://hal.science/hal-03482456', 'https://hal.science/hal-03613598', 'https://hal.science/hal-03695798', 'https://hal.science/hal-03777471', 'https://hal.science/hal-03932770', 'https://hal.science/hal-03777459', 'https://hal.science/hal-03819724', 'https://hal.science/tel-03882284', 'https://hal.science/hal-04306225', 'https://hal.science/tel-03904652', 'https://hal.science/hal-03777440', 'https://hal.science/hal-03654350', 'https://hal.science/hal-03482420', 'https://hal.science/hal-03777443', 'https://hal.science/hal-03777464', 'https://hal.science/hal-03488546', 'https://hal.science/hal-03888109', 'https://hal.science/hal-03888055', 'https://hal.science/hal-03888082', 'https://hal.science/hal-03614844', 'https://hal.science/hal-03932044', 'https://hal.science/hal-03698218', 'https://hal.science/hal-03750109', 'https://hal.science/hal-03963698', 'https://hal.science/hal-03197729', 'https://hal.science/tel-04012662', 'https://hal.science/hal-03448296', 'https://hal.science/tel-03881950', 'https://hal.science/hal-03927368', 'https://hal.science/hal-03927310', 'https://hal.science/hal-03663151', 'https://hal.science/hal-03595310', 'https://hal.science/hal-03555602', 'https://hal.science/hal-03614193', 'https://hal.science/hal-03698231', 'https://hal.science/hal-03699414', 'https://hal.science/hal-03911372', 'https://hal.science/hal-03831515', 'https://hal.science/hal-03831513', 'https://hal.science/hal-03565071', 'https://hal.science/hal-03720291', 'https://hal.science/hal-03844951', 'https://hal.science/emse-03843561', 'https://hal.science/hal-03352745', 'https://hal.science/hal-03800577', 'https://hal.science/hal-03672901', 'https://hal.science/hal-03562889', 'https://hal.science/hal-03797654', 'https://hal.science/hal-03625582', 'https://hal.science/tel-04009502', 'https://hal.science/hal-04029768', 'https://hal.science/hal-03878254', 'https://hal.science/hal-03933407', 'https://hal.science/hal-03878252', 'https://hal.science/hal-03654722', 'https://hal.science/hal-03613558', 'https://hal.science/hal-03683568', 'https://hal.science/hal-03937825', 'https://hal.science/hal-03776508', 'https://hal.science/hal-03723457', 'https://hal.science/tel-03906421', 'https://hal.science/hal-04260161', 'https://hal.science/hal-03740496', 'https://hal.science/tel-03927199', 'https://hal.science/hal-04385204', 'https://hal.science/hal-03673668', 'https://hal.science/hal-03641576', 'https://hal.science/hal-03805561', 'https://hal.science/hal-03547219', 'https://hal.science/hal-03466396', 'https://hal.science/tel-03854875', 'https://hal.science/hal-03788437', 'https://hal.science/hal-03558479', 'https://hal.science/hal-03652738', 'https://hal.science/hal-03231669', 'https://hal.science/hal-03764541', 'https://hal.science/hal-03627246', 'https://hal.science/tel-04072990', 'https://hal.science/hal-03793085', 'https://hal.science/tel-03854849', 'https://hal.science/hal-03921298', 'https://hal.science/hal-03921373', 'https://hal.science/hal-03933973', 'https://hal.science/hal-03921309', 'https://hal.science/hal-03220449', 'https://hal.science/hal-03358817', 'https://hal.science/hal-03514984', 'https://hal.science/hal-03729080', 'https://hal.science/hal-03799289', 'https://hal.science/hal-03593967', 'https://hal.science/hal-03527250', 'https://hal.science/hal-03615777', 'https://hal.science/tel-03881947', 'https://hal.science/hal-03921362', 'https://hal.science/hal-03632376', 'https://hal.science/hal-03770004', 'https://hal.science/hal-03720273', 'https://hal.science/hal-03624309', 'https://hal.science/hal-03921928', 'https://hal.science/hal-03921387', 'https://hal.science/hal-03528889', 'https://hal.science/hal-03613422', 'https://hal.science/hal-03927522', 'https://hal.science/hal-03810501', 'https://hal.science/hal-03185821', 'https://hal.science/hal-03913369', 'https://hal.science/tel-04146617', 'https://hal.science/hal-03510322', 'https://hal.science/hal-03726234', 'https://hal.science/hal-03777726', 'https://hal.science/hal-03889053', 'https://hal.science/hal-03890424', 'https://hal.science/hal-03833605', 'https://hal.science/tel-03882666', 'https://hal.science/hal-03587358', 'https://hal.science/hal-03879423', 'https://hal.science/hal-03363176', 'https://hal.science/hal-02083080', 'https://hal.science/hal-03666587', 'https://hal.science/hal-03777656', 'https://hal.science/hal-03531372', 'https://hal.science/hal-03711670', 'https://hal.science/hal-03890398', 'https://hal.science/hal-03946331', 'https://hal.science/hal-03780557', 'https://hal.science/hal-03697249', 'https://hal.science/hal-03616626', 'https://hal.science/hal-03720874', 'https://hal.science/hal-03789357', 'https://hal.science/tel-03906598', 'https://hal.science/hal-03876091', 'https://hal.science/hal-03871397', 'https://hal.science/hal-03789182', 'https://hal.science/hal-03879996', 'https://hal.science/tel-03924107', 'https://hal.science/hal-03689107', 'https://hal.science/hal-03893738', 'https://hal.science/hal-03926272', 'https://hal.science/hal-03522989', 'https://hal.science/hal-03936209', 'https://hal.science/hal-03870140', 'https://hal.science/hal-03826747', 'https://hal.science/hal-03880428', 'https://hal.science/hal-03693653', 'https://hal.science/hal-03602177', 'https://hal.science/hal-03870109', 'https://hal.science/hal-03877191', 'https://hal.science/hal-03885249', 'https://hal.science/hal-03877219', 'https://hal.science/hal-03701755', 'https://hal.science/hal-03878581', 'https://hal.science/hal-03866048', 'https://hal.science/tel-03854857', 'https://hal.science/hal-03506036', 'https://hal.science/hal-03491950', 'https://hal.science/hal-03604970', 'https://hal.science/hal-03740981', 'https://hal.science/hal-03564455', 'https://hal.science/hal-03483109', 'https://hal.science/hal-03609537', 'https://hal.science/hal-03599214', 'https://hal.science/hal-03704042', 'https://hal.science/hal-03866083', 'https://hal.science/hal-03698839', 'https://hal.science/hal-03741047', 'https://hal.science/hal-03609470', 'https://hal.science/hal-03741042', 'https://hal.science/hal-03866075', 'https://hal.science/hal-03717860', 'https://hal.science/hal-03900024', 'https://hal.science/hal-03866192', 'https://hal.science/hal-03551329', 'https://hal.science/hal-03899151', 'https://hal.science/hal-03926161', 'https://hal.science/hal-03741036', 'https://hal.science/hal-02887646', 'https://hal.science/hal-03667491', 'https://hal.science/hal-03845144', 'https://hal.science/hal-03866030', 'https://hal.science/hal-03908363', 'https://hal.science/tel-04068705', 'https://hal.science/hal-03817385', 'https://hal.science/hal-03864075', 'https://hal.science/hal-03070560', 'https://hal.science/hal-03817360', 'https://hal.science/hal-03684406', 'https://hal.science/hal-03878293', 'https://hal.science/hal-03896532', 'https://hal.science/hal-03817928', 'https://hal.science/hal-03817374', 'https://hal.science/hal-03844316', 'https://hal.science/hal-03817968', 'https://hal.science/hal-03166007', 'https://hal.science/hal-03815190', 'https://hal.science/hal-03790140', 'https://hal.science/hal-03887523', 'https://hal.science/hal-03885124', 'https://hal.science/hal-03558978', 'https://hal.science/tel-03896860', 'https://hal.science/tel-03921247', 'https://hal.science/tel-04186037', 'https://hal.science/hal-03750389', 'https://hal.science/hal-03817852', 'https://hal.science/hal-03625229', 'https://hal.science/hal-03886951', 'https://hal.science/hal-03817447', 'https://hal.science/hal-03832903', 'https://hal.science/hal-03613353', 'https://hal.science/hal-03885541', 'https://hal.science/hal-03902786', 'https://hal.science/hal-03885245', 'https://hal.science/hal-03763091', 'https://hal.science/tel-03929660', 'https://hal.science/hal-02399723', 'https://hal.science/hal-03920748', 'https://hal.science/hal-03906055', 'https://hal.science/hal-03791921', 'https://hal.science/hal-03657044', 'https://hal.science/hal-03750209', 'https://hal.science/hal-03851597', 'https://hal.science/hal-03923695', 'https://hal.science/hal-03324177', 'https://hal.science/hal-03678747', 'https://hal.science/hal-03920684', 'https://hal.science/hal-03923712', 'https://hal.science/hal-03694177', 'https://hal.science/hal-03920724', 'https://hal.science/hal-03920720', 'https://hal.science/hal-03920733', 'https://hal.science/hal-03879849', 'https://hal.science/hal-03655608', 'https://hal.science/hal-04389352', 'https://hal.science/hal-03792482', 'https://hal.science/hal-03746704', 'https://hal.science/hal-03671451', 'https://hal.science/hal-03789485', 'https://hal.science/hal-03853639', 'https://hal.science/hal-03591421', 'https://hal.science/hal-03906141', 'https://hal.science/hal-03885616', 'https://hal.science/hal-03723508', 'https://hal.science/hal-03679073', 'https://hal.science/hal-03697974', 'https://hal.science/hal-03980301', 'https://hal.science/hal-03980317', 'https://hal.science/hal-03953547', 'https://hal.science/hal-03418759', 'https://hal.science/hal-03816204', 'https://hal.science/hal-03816207', 'https://hal.science/hal-03621342', 'https://hal.science/hal-03609893', 'https://hal.science/hal-02870826', 'https://hal.science/hal-03542560', 'https://hal.science/hal-03110983', 'https://hal.science/hal-03618267', 'https://hal.science/hal-03991668', 'https://hal.science/tel-04416424', 'https://hal.science/tel-04071498', 'https://hal.science/hal-03850395', 'https://hal.science/hal-03271783', 'https://hal.science/hal-03614440', 'https://hal.science/hal-03817218', 'https://hal.science/hal-03648499', 'https://hal.science/hal-03776589', 'https://hal.science/tel-03944537', 'https://hal.science/hal-03648488', 'https://hal.science/hal-03776596', 'https://hal.science/hal-03676489', 'https://hal.science/hal-03845342', 'https://hal.science/hal-03929522', 'https://hal.science/tel-03867317', 'https://hal.science/hal-03741340', 'https://hal.science/hal-04047576', 'https://hal.science/hal-04047617', 'https://hal.science/hal-04380084', 'https://hal.science/hal-03905181', 'https://hal.science/hal-03873252', 'https://hal.science/hal-03925696', 'https://hal.science/hal-03812666', 'https://hal.science/hal-03791272', 'https://hal.science/hal-03951141', 'https://hal.science/hal-03696293', 'https://hal.science/hal-03925654', 'https://hal.science/hal-03449887', 'https://hal.science/tel-04068992', 'https://hal.science/hal-03777530', 'https://hal.science/hal-03925675', 'https://hal.science/hal-03696295', 'https://hal.science/hal-03812670', 'https://hal.science/hal-03907912', 'https://hal.science/hal-03951133', 'https://hal.science/hal-03777547', 'https://hal.science/hal-04163409', 'https://hal.science/hal-03713275', 'https://hal.science/hal-03682496', 'https://hal.science/hal-03932194', 'https://hal.science/hal-04018093', 'https://hal.science/hal-04082487', 'https://hal.science/hal-03790756', 'https://hal.science/hal-03725221', 'https://hal.science/hal-03842246', 'https://hal.science/hal-03779076', 'https://hal.science/hal-03779023', 'https://hal.science/hal-03780530', 'https://hal.science/hal-03760380', 'https://hal.science/hal-03542726', 'https://hal.science/hal-03517202', 'https://hal.science/hal-03760315', 'https://hal.science/hal-03760529', 'https://hal.science/hal-03706994', 'https://hal.science/hal-03912714', 'https://hal.science/hal-03900458', 'https://hal.science/hal-03727989', 'https://hal.science/hal-03853321', 'https://hal.science/hal-03549995', 'https://hal.science/tel-04077508', 'https://hal.science/hal-03680872', 'https://hal.science/hal-03714101', 'https://hal.science/hal-03887690', 'https://hal.science/hal-03676968', 'https://hal.science/cea-03776535', 'https://hal.science/hal-03907727', 'https://hal.science/tel-03765873', 'https://hal.science/hal-03669439', 'https://hal.science/hal-03828841', 'https://hal.science/hal-03885471', 'https://hal.science/hal-02392522', 'https://hal.science/hal-03494874', 'https://hal.science/hal-03885490', 'https://hal.science/hal-03494872', 'https://hal.science/hal-03888016', 'https://hal.science/hal-03379489', 'https://hal.science/hal-03887704', 'https://hal.science/tel-03925783', 'https://hal.science/hal-03926148', 'https://hal.science/hal-03926136', 'https://hal.science/tel-03958287', 'https://hal.science/hal-03494868', 'https://hal.science/hal-03888027', 'https://hal.science/hal-03888005', 'https://hal.science/hal-03865253', 'https://hal.science/hal-03885663', 'https://hal.science/hal-03903370', 'https://hal.science/hal-03500153', 'https://hal.science/hal-03907885', 'https://hal.science/hal-03684224', 'https://hal.science/hal-03485386', 'https://hal.science/hal-03553505', 'https://hal.science/hal-03697265', 'https://hal.science/hal-03854671', 'https://hal.science/tel-03949792', 'https://hal.science/tel-03965028', 'https://hal.science/hal-03500332', 'https://hal.science/hal-03652138', 'https://hal.science/hal-03888009', 'https://hal.science/hal-03923506', 'https://hal.science/hal-03887997', 'https://hal.science/hal-03903347', 'https://hal.science/tel-03885206', 'https://hal.science/hal-03920728', 'https://hal.science/hal-03536643', 'https://hal.science/hal-03770492', 'https://hal.science/hal-03926688', 'https://hal.science/tel-03922210', 'https://hal.science/hal-03779486', 'https://hal.science/emse-03922716', 'https://hal.science/hal-03938808', 'https://hal.science/hal-03748752', 'https://hal.science/hal-03546653', 'https://hal.science/hal-03922772', 'https://hal.science/hal-03747555', 'https://hal.science/hal-03524935', 'https://hal.science/hal-03602788', 'https://hal.science/hal-03938813', 'https://hal.science/hal-03931226', 'https://hal.science/tel-03966012', 'https://hal.science/hal-03544099', 'https://hal.science/hal-03737297', 'https://hal.science/hal-03736603', 'https://hal.science/hal-03703925', 'https://hal.science/hal-03919553', 'https://hal.science/hal-03956728', 'https://hal.science/hal-03548120', 'https://hal.science/hal-03830823', 'https://hal.science/hal-03614072', 'https://hal.science/hal-03928263', 'https://hal.science/hal-03584138', 'https://hal.science/hal-03797971', 'https://hal.science/hal-03320680', 'https://hal.science/hal-03605535', 'https://hal.science/hal-03548338', 'https://hal.science/hal-03928270', 'https://hal.science/hal-03835654', 'https://hal.science/hal-03557633', 'https://hal.science/hal-03621989', 'https://hal.science/hal-03822979', 'https://hal.science/hal-03903025', 'https://hal.science/hal-03813473', 'https://hal.science/hal-03931452', 'https://hal.science/hal-04114240', 'https://hal.science/hal-03716829', 'https://hal.science/hal-03722383', 'https://hal.science/hal-03836778', 'https://hal.science/hal-03928268', 'https://hal.science/hal-03797952', 'https://hal.science/hal-03820756', 'https://hal.science/hal-03763591', 'https://hal.science/hal-04149136', 'https://hal.science/hal-03611661', 'https://hal.science/hal-03836741', 'https://hal.science/hal-03799188', 'https://hal.science/hal-03928273', 'https://hal.science/hal-03690524', 'https://hal.science/hal-03790274', 'https://hal.science/hal-03770458', 'https://hal.science/hal-03928274', 'https://hal.science/hal-03853981', 'https://hal.science/hal-03782133', 'https://hal.science/tel-03771455', 'https://hal.science/hal-03941749', 'https://hal.science/hal-03888489', 'https://hal.science/tel-03813699', 'https://hal.science/hal-03817534', 'https://hal.science/hal-03830670', 'https://hal.science/hal-04281736', 'https://hal.science/hal-03584119', 'https://hal.science/hal-03656204', 'https://hal.science/hal-03664189', 'https://hal.science/hal-03921399', 'https://hal.science/hal-03506034', 'https://hal.science/hal-03674770', 'https://hal.science/hal-03715820', 'https://hal.science/hal-03584189', 'https://hal.science/hal-03789212', 'https://hal.science/hal-03683441', 'https://hal.science/hal-03581916', 'https://hal.science/hal-03682604', 'https://hal.science/hal-03664178', 'https://hal.science/hal-03642462', 'https://hal.science/hal-03709659', 'https://hal.science/hal-03711725', 'https://hal.science/hal-03822380', 'https://hal.science/hal-03783053', 'https://hal.science/hal-03794415', 'https://hal.science/hal-03654156', 'https://hal.science/hal-03797567', 'https://hal.science/hal-03614071', 'https://hal.science/tel-03576321', 'https://hal.science/hal-03734033', 'https://hal.science/hal-03594774', 'https://hal.science/hal-03335162', 'https://hal.science/tel-03690426', 'https://hal.science/hal-03676527', 'https://hal.science/hal-03768194', 'https://hal.science/hal-03810911', 'https://hal.science/hal-03551814', 'https://hal.science/hal-03921410', 'https://hal.science/hal-02475059', 'https://hal.science/hal-03624750', 'https://hal.science/hal-03706810', 'https://hal.science/hal-03752195', 'https://hal.science/hal-03584085', 'https://hal.science/hal-03551830', 'https://hal.science/hal-03614067', 'https://hal.science/hal-03321834', 'https://hal.science/hal-03807745', 'https://hal.science/hal-04481717', 'https://hal.science/hal-03752892', 'https://hal.science/hal-03781035', 'https://hal.science/hal-03838682', 'https://hal.science/hal-03921378', 'https://hal.science/hal-03548113', 'https://hal.science/hal-03654316', 'https://hal.science/hal-03614070', 'https://hal.science/hal-03718328', 'https://hal.science/hal-03701490', 'https://hal.science/hal-03886523', 'https://hal.science/hal-03701492', 'https://hal.science/hal-03591396', 'https://hal.science/hal-03548071', 'https://hal.science/hal-03738654', 'https://hal.science/hal-03806393', 'https://hal.science/hal-03398607', 'https://hal.science/hal-03718429', 'https://hal.science/hal-03852749', 'https://hal.science/hal-03620779', 'https://hal.science/hal-03839438', 'https://hal.science/hal-03736116', 'https://hal.science/hal-03577949', 'https://hal.science/hal-03701506', 'https://hal.science/hal-03548073', 'https://hal.science/hal-03899264', 'https://hal.science/hal-03806425', 'https://hal.science/hal-03701513', 'https://hal.science/hal-03696016', 'https://hal.science/hal-03991178', 'https://hal.science/hal-04352691', 'https://hal.science/hal-03991207', 'https://hal.science/hal-03991258', 'https://hal.science/hal-03932463', 'https://hal.science/hal-03991217', 'https://hal.science/hal-03132924', 'https://hal.science/hal-03991269', 'https://hal.science/hal-03991283', 'https://hal.science/hal-03991287', 'https://hal.science/hal-03934152', 'https://hal.science/hal-03991233', 'https://hal.science/hal-03934160', 'https://hal.science/hal-03839517', 'https://hal.science/hal-03541964', 'https://hal.science/hal-03991158', 'https://hal.science/hal-03922196', 'https://hal.science/hal-03839524', 'https://hal.science/hal-03991201', 'https://hal.science/hal-03991191', 'https://hal.science/hal-03991085', 'https://hal.science/hal-03523498', 'https://hal.science/hal-03858930', 'https://hal.science/hal-03832589', 'https://hal.science/hal-03991274', 'https://hal.science/hal-03515501', 'https://hal.science/hal-03858935', 'https://hal.science/hal-03646688', 'https://hal.science/hal-03853961', 'https://hal.science/hal-03833562', 'https://hal.science/hal-03643112', 'https://hal.science/hal-03857826', 'https://hal.science/hal-03541327', 'https://hal.science/hal-03654734', 'https://hal.science/hal-03806390', 'https://hal.science/tel-03938942', 'https://hal.science/hal-04348301', 'https://hal.science/hal-03758898', 'https://hal.science/hal-03807986', 'https://hal.science/tel-03754139', 'https://hal.science/hal-03808292', 'https://hal.science/hal-03808305', 'https://hal.science/hal-03763691', 'https://hal.science/hal-04348757', 'https://hal.science/hal-03820927', 'https://hal.science/hal-03866341', 'https://hal.science/hal-03833539', 'https://hal.science/hal-03848700', 'https://hal.science/hal-03432380', 'https://hal.science/hal-03651953', 'https://hal.science/hal-03760650', 'https://hal.science/hal-03607417', 'https://hal.science/hal-03833545', 'https://hal.science/hal-03866225', 'https://hal.science/hal-03697484', 'https://hal.science/hal-03981018', 'https://hal.science/hal-03966518', 'https://hal.science/hal-03966533', 'https://hal.science/hal-03614274', 'https://hal.science/hal-03698340', 'https://hal.science/hal-03975729', 'https://hal.science/hal-03966599', 'https://hal.science/hal-03967243', 'https://hal.science/hal-04448954', 'https://hal.science/tel-04077233', 'https://hal.science/hal-03901755', 'https://hal.science/hal-03966941', 'https://hal.science/hal-03983223', 'https://hal.science/hal-03966541', 'https://hal.science/hal-03981781', 'https://hal.science/hal-03975832', 'https://hal.science/hal-03701501', 'https://hal.science/tel-04077066', 'https://hal.science/hal-03944464', 'https://hal.science/hal-03932479', 'https://hal.science/hal-03941094', 'https://hal.science/hal-03630283', 'https://hal.science/hal-03767104', 'https://hal.science/hal-03798342', 'https://hal.science/hal-03682126', 'https://hal.science/hal-03473179', 'https://hal.science/hal-03637107', 'https://hal.science/hal-02965322', 'https://hal.science/hal-03551345', 'https://hal.science/hal-03927074', 'https://hal.science/hal-03708833', 'https://hal.science/hal-03631377', 'https://hal.science/hal-03694811', 'https://hal.science/hal-03798500', 'https://hal.science/hal-04349301', 'https://hal.science/hal-03935067', 'https://hal.science/hal-03600947', 'https://hal.science/tel-03937380', 'https://hal.science/hal-03865772', 'https://hal.science/hal-03780979', 'https://hal.science/hal-03865727', 'https://hal.science/tel-03995978', 'https://hal.science/hal-04352946', 'https://hal.science/hal-03834580', 'https://hal.science/hal-03711114', 'https://hal.science/hal-03837323', 'https://hal.science/hal-03709343', 'https://hal.science/hal-03911355', 'https://hal.science/hal-03150446', 'https://hal.science/hal-03709353', 'https://hal.science/hal-03781983', 'https://hal.science/hal-03709329', 'https://hal.science/hal-03128118', 'https://hal.science/hal-03681995', 'https://hal.science/hal-03917588', 'https://hal.science/hal-03892095', 'https://hal.science/hal-03896238', 'https://hal.science/hal-03792078', 'https://hal.science/hal-03899041', 'https://hal.science/hal-03898901', 'https://hal.science/hal-03767913', 'https://hal.science/hal-03703516', 'https://hal.science/hal-03699021', 'https://hal.science/hal-03898621', 'https://hal.science/hal-03830890', 'https://hal.science/hal-03763839', 'https://hal.science/hal-03717062', 'https://hal.science/hal-03844765', 'https://hal.science/hal-03902768', 'https://hal.science/hal-03905693', 'https://hal.science/hal-03678150', 'https://hal.science/hal-03911337', 'https://hal.science/hal-03898605', 'https://hal.science/hal-03035289', 'https://hal.science/hal-03911323', 'https://hal.science/hal-03901350', 'https://hal.science/tel-03896253', 'https://hal.science/hal-03911352', 'https://hal.science/hal-03709334', 'https://hal.science/hal-03709661', 'https://hal.science/hal-03727967', 'https://hal.science/hal-03196379', 'https://hal.science/hal-03899073', 'https://hal.science/tel-04052781', 'https://hal.science/hal-03772712', 'https://hal.science/hal-03782992', 'https://hal.science/hal-03882701', 'https://hal.science/tel-03948419', 'https://hal.science/hal-03906375', 'https://hal.science/hal-03768820', 'https://hal.science/hal-03784478', 'https://hal.science/tel-03987749', 'https://hal.science/hal-03466807', 'https://hal.science/tel-03969183', 'https://hal.science/hal-03907545', 'https://hal.science/hal-03895960', 'https://hal.science/hal-03847153', 'https://hal.science/hal-03580148', 'https://hal.science/hal-03685976', 'https://hal.science/hal-04369049', 'https://hal.science/hal-04029594', 'https://hal.science/hal-04029627', 'https://hal.science/hal-03776462', 'https://hal.science/hal-03627833', 'https://hal.science/hal-04166720', 'https://hal.science/hal-04028179', 'https://hal.science/hal-03676650', 'https://hal.science/hal-03854905', 'https://hal.science/hal-03618678', 'https://hal.science/tel-03963614', 'https://hal.science/tel-03960269', 'https://hal.science/hal-03510612', 'https://hal.science/hal-03713584', 'https://hal.science/hal-03819329', 'https://hal.science/hal-03450625', 'https://hal.science/hal-04028180', 'https://hal.science/hal-03798824', 'https://hal.science/tel-03894045', 'https://hal.science/inserm-03642535', 'https://hal.science/hal-03295913', 'https://hal.science/hal-03798043', 'https://hal.science/hal-03975757', 'https://hal.science/hal-03672588', 'https://hal.science/hal-03798593', 'https://hal.science/inserm-03639907', 'https://hal.science/hal-03792703', 'https://hal.science/hal-04239885', 'https://hal.science/hal-03783898', 'https://hal.science/hal-04308694', 'https://hal.science/hal-04231217', 'https://hal.science/hal-03754023', 'https://hal.science/hal-04231191', 'https://hal.science/hal-04231222', 'https://hal.science/hal-04231225', 'https://hal.science/hal-03727820', 'https://hal.science/hal-04231162', 'https://hal.science/hal-03616058', 'https://hal.science/hal-04231182', 'https://hal.science/hal-04231187', 'https://hal.science/hal-04231209', 'https://hal.science/hal-03576400', 'https://hal.science/hal-03688011', 'https://hal.science/hal-03960204', 'https://hal.science/hal-03806099', 'https://hal.science/hal-04278109', 'https://hal.science/tel-03850485', 'https://hal.science/hal-03784682', 'https://hal.science/hal-03778139', 'https://hal.science/tel-03888741', 'https://hal.science/hal-03688032', 'https://hal.science/hal-03284105', 'https://hal.science/hal-04200331', 'https://hal.science/hal-03729129', 'https://hal.science/hal-03704048', 'https://hal.science/hal-03906123', 'https://hal.science/hal-03830914', 'https://hal.science/hal-03639282', 'https://hal.science/hal-03863843', 'https://hal.science/hal-03875702', 'https://hal.science/hal-04018982', 'https://hal.science/hal-04483941', 'https://hal.science/hal-03850355']}
print(len(URIS_BRE['BRE']))
download_xml_by_id(URIS_BRE)