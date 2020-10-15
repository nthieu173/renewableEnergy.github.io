import requests
import tarfile
import os
import csv
import io
import statistics
from copy import copy

states_names = ["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA",
        "HI","ID","IL","IN","IA","KS","KY","LA","ME","MD",
        "MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ",
        "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC",
        "SD","TN","TX","UT","VT","VA","WA","WV","WI","WY","DC"]

# THERE IS NO WEATHER DATA FOR DC

year_range = range(1998, 2017)

class StateData:
    def __init__(self):
        self.wind_speed = dict([(year,[]) for year in year_range]) #AWND
        self.precipitation = dict([(year,[]) for year in year_range]) #PRCP
        self.snowfall = dict([(year,[]) for year in year_range]) #SNOW
        self.temperature = dict([(year,[]) for year in year_range]) #TAVG
    
    def _take_yearly_min(measurement):
        yearly_mean = {}
        for year in measurement:
            if len(measurement[year]) > 0:
                yearly_mean[year] = statistics.mean(measurement[year])
            else:
                yearly_mean[year] = 0
        return yearly_mean

    def mean(self):
        return {
            "windspeed": StateData._take_yearly_min(self.wind_speed),
            "precipitation": StateData._take_yearly_min(self.precipitation),
            "snowfall": StateData._take_yearly_min(self.snowfall),
            "temperature": StateData._take_yearly_min(self.temperature),
        }

def check_and_download_data():
    if not os.path.isfile("gsoy-latest.tar.gz"):
        print("Downloading Global Summary of the Year data")
        link = "https://www.ncei.noaa.gov/data/gsoy/archive/gsoy-latest.tar.gz"
        r = requests.get(link, stream=True)
        with open("gsoy-latest.tar.gz", 'wb') as f:
            for chunk in r.iter_content(chunk_size=128):
                f.write(chunk)
    print("Checked Global Summary of the Year data")

def field_exists(row, field):
    return field in row and len(row[field]) > 0

def process_data():
    states = dict([(name, StateData()) for name in states_names])

    with tarfile.TarFile.open("gsoy-latest.tar.gz") as tar_ref:
        count = 0
        num_stations = len(tar_ref.getmembers())
        for info in tar_ref.getmembers():
            if info.name.startswith("US"):
                station_csv_file = io.TextIOWrapper(tar_ref.extractfile(info))
                reader = csv.DictReader(station_csv_file)
                state_name = None
                for row in reader:
                    if state_name is None:
                        state_name = row["NAME"].split(",")[1].split()[0]
                    year = int(row["DATE"])
                    if year in year_range:
                        if field_exists(row,"AWND"):
                            states[state_name].wind_speed[year] += [float(row["AWND"])*10]#m/s
                        if field_exists(row, "PRCP"):
                            states[state_name].precipitation[year] += [float(row["PRCP"])]#mm
                        if field_exists(row, "SNOW"):
                            states[state_name].snowfall[year] += [float(row["SNOW"])]#mm
                        if field_exists(row, "TAVG"):
                            states[state_name].temperature[year] += [float(row["TAVG"])]#celsius
            count += 1
            print("Processed {}/{} stations".format(count, num_stations), end="\r")
    return states

def main():
    check_and_download_data()
    states = process_data()
    states = dict([(name, states[name].mean()) for name in states])
    windspeed = dict([(name, []) for name in states])
    precipitation = dict([(name, []) for name in states])
    snowfall = dict([(name, []) for name in states])
    temperature = dict([(name, []) for name in states])
    for name in states:
        state = states[name]
        for year in year_range:
            windspeed[name] += [state["windspeed"][year]]
            precipitation[name] += [state["precipitation"][year]]
            snowfall[name] += [state["snowfall"][year]]
            temperature[name] += [state["temperature"][year]]
    with open("us_states_annual_average_windspeed.csv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["State"]+[i for i in year_range])
        for name in windspeed:
            csvwriter.writerow([name]+windspeed[name])
    print("Written average radiance data to us_states_annual_average_windspeed.csv")
    with open("us_states_annual_average_precipitation.csv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["State"]+[i for i in year_range])
        for name in precipitation:
            csvwriter.writerow([name]+precipitation[name])
    print("Written average radiance data to us_states_annual_average_precipitation.csv")
    with open("us_states_annual_average_snowfall.csv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["State"]+[i for i in year_range])
        for name in snowfall:
            csvwriter.writerow([name]+snowfall[name])
    print("Written average radiance data to us_states_annual_average_snowfall.csv")
    with open("us_states_annual_average_temperature.csv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["State"]+[i for i in year_range])
        for name in temperature:
            csvwriter.writerow([name]+temperature[name])
    print("Written average radiance data to us_states_annual_average_temperature.csv")

if __name__ == "__main__":
    main()