import os
import requests
import csv
from collections import defaultdict
import pandas as pd


def check_and_download_data():
    if not os.path.isfile("wp.data.1.AllCommodities"):
        print("Downloading Producer Price Index data")
        link = "https://download.bls.gov/pub/time.series/wp/wp.data.1.AllCommodities"
        r = requests.get(link, stream=True)
        with open("wp.data.1.AllCommodities", 'wb') as f:
            for chunk in r.iter_content(chunk_size=128):
                f.write(chunk)
    print("Checked Producer Price Index data")

def read_data(path = "./wp.data.1.AllCommodities"):
    data = defaultdict(lambda : [])
    df = pd.read_csv(path, delim_whitespace=True)
    for row in df.itertuples():
        data[int(row.year)] += [int(row.value)]
    for year in data:
        data[year] = sum(data[year]) / len(data[year])
    return data

def write_data(data, path = "./us_yearly_producer_price_index.csv"):
    with open(path, "w") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(["Year", "Value"])
        for year in sorted(data.keys()):
            writer.writerow([year, data[year]])


if __name__ == "__main__":
    check_and_download_data()
    data = read_data()
    write_data(data)