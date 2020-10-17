import csv

states_names = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
                "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
                "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
                "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
                "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "DC"]


def add_solar_data(data, year_from, year_to):
    with open("solar_radiance/us_states_yearly_average_dni.csv") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            for year in range(year_from, year_to + 1):
                data[(row["State"], year)]["dni"] = float(row[str(year)])
    return data


def add_precipitation_data(data, year_from, year_to):
    with open("weather/us_states_annual_average_precipitation.csv") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            for year in range(year_from, year_to + 1):
                data[(row["State"], year)]["precipitation"] = float(row[str(year)])
    return data


def add_snowfall_data(data, year_from, year_to):
    with open("weather/us_states_annual_average_snowfall.csv") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            for year in range(year_from, year_to + 1):
                data[(row["State"], year)]["snowfall"] = float(row[str(year)])
    return data


def add_temperature_data(data, year_from, year_to):
    with open("weather/us_states_annual_average_temperature.csv") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            for year in range(year_from, year_to + 1):
                data[(row["State"], year)]["temperature"] = float(row[str(year)])
    return data


def add_windspeed_data(data, year_from, year_to):
    with open("weather/us_states_annual_average_windspeed.csv") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            for year in range(year_from, year_to + 1):
                data[(row["State"], year)]["windspeed"] = float(row[str(year)])
    return data


def add_hydropower_potential_data(data, year_from, year_to):
    with open("hydropower_potential/us_states_hydropower_potential.csv") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            for year in range(year_from, year_to + 1):
                data[(row["State"], year)]["potential_hydro_cap"] = int(row["PotentialCapacityMW"])
                data[(row["State"], year)]["potential_hydro_gen"] = int(row["PotentialGenerationGWHYR"])
    return data


def add_state_area_data(data, year_from, year_to):
    with open("state_geography/total_state_area.csv") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            for year in range(year_from, year_to + 1):
                data[(row["State"], year)]["total_state_area"] = float(row["Total Area (Sq. Mi.)"].replace(',', ''))
    return data

def add_total_coal_consumption_data(data, year_from, year_to):
    with open("non_renewable_data/total_coal_consumption.csv") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            for year in range(year_from, year_to + 1):
                data[(row["State"], year)]["total_coal_consumption"] = float(row[str(year)])
    return data

def add_total_natural_gas_consumption_data(data, year_from, year_to):
    with open("non_renewable_data/total_natural_gas_consumption.csv") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            for year in range(year_from, year_to + 1):
                data[(row["State"], year)]["total_natural_gas_consumption"] = float(row[str(year)])
    return data

def add_prime_supplier_residual_oil_data(data, year_from, year_to):
    with open("non_renewable_data/prime_supplier_residual_oil.csv") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            for year in range(year_from, year_to + 1):
                data[(row["State"], year)]["prime_supplier_residual_oil"] = float(row[str(year)])
    return data




def main():
    year_from = 1998
    year_to = 2016
    data = {}
    for state in states_names:
        for year in range(year_from, year_to + 1):
            data[(state, year)] = {}
    data = add_solar_data(data, year_from, year_to)
    data = add_precipitation_data(data, year_from, year_to)
    data = add_snowfall_data(data, year_from, year_to)
    data = add_temperature_data(data, year_from, year_to)
    data = add_windspeed_data(data, year_from, year_to)
    data = add_hydropower_potential_data(data, year_from, year_to)
    data = add_state_area_data(data, year_from, year_to)
    data = add_total_coal_consumption_data(data, year_from, year_to)
    data = add_total_natural_gas_consumption_data(data, year_from, year_to)
    data = add_prime_supplier_residual_oil_data(data, year_from, year_to)

    features = ["dni", "precipitation", "snowfall", "temperature", "windspeed", "potential_hydro_cap",
                "potential_hydro_gen", "total_state_area", "total_coal_consumption", "total_natural_gas_consumption",
                "prime_supplier_residual_oil"]

    with open("aggregated_us_states_year.csv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["State", "Year"] + features)
        for (name, year) in data:
            state_data = data[(name, year)]
            row = [name, year]
            for feature in features:
                row += [state_data[feature]]
            csvwriter.writerow(row)


if __name__ == "__main__":
    main()
