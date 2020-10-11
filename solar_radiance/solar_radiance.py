import statistics
import csv
import requests
import zipfile
import os
from copy import copy
from multiprocessing.pool import ThreadPool

import shapefile
from shapely.geometry import shape

if not os.path.isfile("state_border/us_states_simple.shp"):
    print("Downloading state border data")
    link = ""
    with open("state_border/wfsrequest.txt") as f:
        link = f.readline()
    r = requests.get(link, stream=True)
    with open("us_states_simple.zip", 'wb') as f:
        for chunk in r.iter_content(chunk_size=128):
            f.write(chunk)
    with zipfile.ZipFile("us_states_simple.zip", 'r') as zip_ref:
        zip_ref.extractall("state_border")
    os.remove("us_states_simple.zip")
print("Checked state border data")

states_shape = {}
with shapefile.Reader("state_border/us_states_simple") as us_states:
    for shapeRec in us_states:
        state_name = shapeRec.record[0]
        if state_name == "NONSTATE":
            continue
        state_abbr = shapeRec.record[5]
        states_shape[state_abbr] = shape(shapeRec.shape)

def download_year(year):
    if not os.path.isfile("{}/nsrdb_v3_0_1_{}_dni.shp".format(year, year)):
        print("Downloading data for year {}".format(year))
        link = ""
        with open("{}/wfsrequest.txt".format(year)) as f:
            link = f.readline()
        r = requests.get(link, stream=True)
        with open("{}.zip".format(year), 'wb') as f:
            for chunk in r.iter_content(chunk_size=128):
                f.write(chunk)
        with zipfile.ZipFile("{}.zip".format(year), 'r') as zip_ref:
            zip_ref.extractall("{}/".format(year))
        os.remove("{}.zip".format(year))
    print("Checked data for year {}".format(year))

def check_and_download_data():
    pool = ThreadPool()
    pool.map(download_year, range(1998, 2017))

def state_average_dni(year):
    print("Processing data for year {}".format(year))
    states_dni = dict([(name,0) for name in states_shape])
    states_dni_count = copy(states_dni)
    with shapefile.Reader("{}/nsrdb_v3_0_1_{}_dni".format(year, year)) as nsrdb:
        for shape_rec in nsrdb:
            geom = shape(shape_rec.shape)
            dni = shape_rec.record[0]
            for name in states_shape:
                if geom.intersects(states_shape[name]):
                    states_dni[name] += dni
                    states_dni_count[name] += 1
    for name in states_dni:
        states_dni[name] = states_dni[name] / states_dni_count[name]
    print("Processed data for year {}".format(year))
    return states_dni

def main(save_file):
    states_yearly_dni = dict([(name,[]) for name in states_shape])
    pool = ThreadPool()
    yearly_average_dni_list = pool.map(state_average_dni, range(1998, 2017))
    for average_dni in yearly_average_dni_list:
        for name in average_dni:
            states_yearly_dni[name] += [average_dni[name]]
    with open(save_file, "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["State"]+[i for i in range(1998, 2017)])
        for name in states_yearly_dni:
            csvwriter.writerow([name]+states_yearly_dni[name])
    print("Written average radiance data to {}".format(save_file))

if __name__ == "__main__":
    check_and_download_data()
    main("us_states_yearly_average_dni.csv")
