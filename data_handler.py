import pandas as pd
import datetime

"""
This module serves as data ordering and clean handler
"""


def create_date_column(df):
    """Creates a date column in isoformat. It is expected that colum 0 contains the year-month-day
    and column 1 contains hour-minute-second-microsecond

    Args:
        df (Pandas dataframe): [description]
    """
    df["date"] = df[0] + "T" + df[1] + "Z"
    df["date"] = df["date"].map(
        lambda x: datetime.datetime.strptime(x, "%d-%b-%YT%H:%M:%S.%fZ").isoformat()[
            :-3
        ]
        + "Z"
    )


def clean_data(df):
    """Extracts only the necessary to create a POST request to
    https://docs.lumu.io/portal/en/kb/articles/cc-api-specifications#Send_DNS_Queries

    It is expected that the dataframe contains:
        - An ISO format date in a 'date' column key
        - The host name in the column 9
        - The client ip in the column 6
        - The request type in the column 11

    Args:
        df (Pandas Dataframe): Dataframe with the request data to be extracted

    Returns:
        Pandas Dataframe: Dataframe with just the expected data for the request
    """
    create_date_column(df)
    df["name"] = df[9]
    df["client_ip"] = df[6].map(lambda x: x.split("#")[0])
    df["type"] = df[11]
    dataframe_data = {
        "date": df["date"],
        "name": df["name"],
        "client_ip": df["client_ip"],
        "type": df["type"],
    }
    data = pd.DataFrame(data=dataframe_data)
    return data


def extract_top_results(data, dataframe_key, number_of_top_values):
    """Extracts the n most repeated values

    Args:
        data (pandas Dataframe): Dataframe to extract data from
        dataframe_key (str): Dataframe key to extract top values
        number_of_top_values (int): Number of top values to extract

    Returns:
        Pandas Dataframe: A pandas dataframe containing three columns:
            - The name of the top value
            - The number of times that the value was found
            - The representative percentage of the frequency
    """
    top_n = data[dataframe_key].value_counts()[:number_of_top_values]
    top_n_list_names = list(top_n.index)
    top_n_list_values = list(top_n)
    top_n = pd.DataFrame(
        data={
            "name": top_n_list_names,
            "number": top_n_list_values,
            "percentage": [
                round((x * 100) / data.shape[0], 2) for x in top_n_list_values
            ],
        }
    )
    return top_n


def create_lumu_json_column(df):
    """Creates a new column, 'json', with the necessary information to send a POST request to
       the dns/queries endpoint.
       It is expected that the input dataframe contains the below columns:
            - date
            - name
            - client_ip
            - type

    Args:
        df (Pandas dataframe): Pandas dataframe with the necessary information to create the minimal expected JSON
    """
    df["json"] = (
        '{"timestamp": "'
        + df["date"]
        + '", "name": "'
        + df["name"]
        + '", "client_ip": "'
        + df["client_ip"]
        + '", "type": "'
        + df["type"]
        + '"}'
    )


def print_formatted_results(data, top_5_hosts, top_5_ips):
    """Prints the formatted results following the instructions given by Lumu

    Args:
        data (Pandas Dataframe): The dataframe with the complete data analyzed
        top_5_hosts (Pandas Dataframe): Contains the top 5 hosts
        top_5_ips (Pandas Dataframe): Contains the top 5 ips
    """
    max_number_row_characters = len(str(top_5_ips.max()["number"]))
    print(f"Total records: {data.shape[0]}", end="\n\n")
    print("Client IPs Rank")
    print(f"{'-' * 15} {'-' * max_number_row_characters} ------")
    for i in range(0, 5):
        print(
            f"{top_5_ips.iloc[i]['name'].ljust(15, ' ')} {str(top_5_ips.iloc[i]['number']).ljust(max_number_row_characters, ' ')} {top_5_ips.iloc[i]['percentage']}%"
        )
    print("\n")
    print("Host Rank")
    max_number_row_characters = len(str(top_5_hosts.max()["number"]))
    print(f"{'-' * 60} {'-' * max_number_row_characters} {'-' * 6}")
    for i in range(0, 5):
        print(
            f"{top_5_hosts.iloc[i]['name'].ljust(60, ' ')} {str(top_5_hosts.iloc[i]['number']).ljust(max_number_row_characters, ' ')} {top_5_hosts.iloc[i]['percentage']}%"
        )
