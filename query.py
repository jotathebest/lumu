import pandas as pd
import json
import requests
import time
import warnings

warnings.filterwarnings("ignore")

from dynaconf import settings
from data_handler import (
    clean_data,
    extract_top_results,
    print_formatted_results,
    create_lumu_json_column,
)


def make_dns_lumu_request(payload):
    """Makes a post request following the docs from
    https://docs.lumu.io/portal/en/kb/articles/cc-api-specifications#Send_DNS_Queries

    Args:
        payload (json): Json type payload to send
    Returns:
        int: Server response status code
    """
    lumu_url = f"https://api.lumu.io/collectors/5ab55d08-ae72-4017-a41c-d9d735360288/dns/queries?key={settings.LUMU_CLIENT_KEY}"
    kwargs = {
        "headers": {"Content-Type": "application/json"},
        "url": lumu_url,
        "method": "POST",
        "json": payload,
    }
    req = requests.request(**kwargs)
    return req.status_code


def split_data_and_send_request(data):
    """Splits in chunks of 500 elements and sends data

    Args:
        data (Pandas Dataframe): Pandas Dataframe that contains the whole data
    """
    number_of_exact_chunks = data.shape[0] // 500
    remaining_chunk = data.shape[0] % 500

    for i in range(0, number_of_exact_chunks * 500, 500):
        data_temp = data.iloc[i : i + 500]
        create_lumu_json_column(data_temp)
        data_request = []
        for j in range(i, i + 500):
            try:
                data_request.append(json.loads(data_temp["json"][j]))
            except:
                continue
        server_status_code = make_dns_lumu_request(data_request)
        if server_status_code == 200:
            print(f"sucessfull request for chunk {i}")

        time.sleep(1)  # Awaits 1 second to avoid 429 HTTP error response

    # Sends the remaining chunk
    data_temp = data.iloc[i : i + remaining_chunk]
    for j in range(i, i + remaining_chunk):
        try:
            data_request.append(json.loads(data_temp["json"][j]))
        except:
            continue
    server_status_code = make_dns_lumu_request(data_request)
    if server_status_code == 200:
        print(f"sucessfull request for last chunk")


def main(file_path):
    df = pd.read_csv(file_path, sep=" ", header=None)
    data = clean_data(df)
    top_5_hosts = extract_top_results(data, "name", 5)
    top_5_ips = extract_top_results(data, "client_ip", 5)
    print_formatted_results(data, top_5_hosts, top_5_ips)
    print(f"\n\n{'*' * 60}")
    print("Sending data ...")
    split_data_and_send_request(data)


if __name__ == "__main__":
    main(settings.QUERIES_FILE_PATH)
