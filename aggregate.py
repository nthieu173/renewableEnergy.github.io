import csv
import pandas as pd
import os
import time

class Data():
    def __init__(self, year_from, year_to, data_file_name, drop_DC=True):
        self.states_names = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
                "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
                "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
                "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
                "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "DC"]
        self.year_from = year_from
        self.year_to = year_to
        self.data_file_name = data_file_name
        self.base_dir = os.getcwd()
        self.data_dir = os.path.join(self.base_dir, 'data')
        self.exclude = ['hydropower_potential.csv', 'total_state_area.csv']
        self.data = pd.Series(dtype=object)
        self.gen_data = pd.Series(dtype=object)
        self.renew_pc = pd.Series(dtype=object)
        self.year_index = []
        for year in range(self.year_from, self.year_to + 1):
            self.year_index.append(str(year))
        self.drop_DC = drop_DC
        if self.drop_DC:
            self.states_names.remove("DC")
        self.renew_list = ['electricity_generated_from_biomass', 'electricity_generated_from_geothermal',
                           'electricity_generated_from_hydroelectrical', 'electricity_generated_from_pump_storage',
                           'electricity_generated_from_solar_and_photovoltaics', 'electricity_generated_from_wind',
                           'electricity_generated_from_wood_and_wood_derivatives']

    def mass_add_data(self):
        """
        Consolidates data from the ./data folder in csv format (excluding those in the exclude list) into one csv file.

        :return:    pandas DataFrame - consolidated data, fills NaNs with 0
        """

        csv_files = os.listdir(self.data_dir)

        for index, file in enumerate(csv_files):
            if file in self.exclude:
                continue
            try:
                new_data = pd.read_csv(os.path.join(self.data_dir, file), index_col='State')
            except:
                try:
                    new_data = pd.read_csv(os.path.join(self.data_dir, file), index_col='STATE')
                except:
                    print(f'ERROR: {index}. {file} unsuccessful.')
                    continue
            data_to_add = new_data.loc[new_data.index != 'DC', self.year_index] if self.drop_DC else new_data[self.year_index]
            data_to_add = data_to_add.stack()
            feature = file.split('.')[0]
            data_to_add.name = feature
            data_to_add.index.names = ['State','Year']

            # Consolidate data with electricity generated and percentage at the back
            if file.split('_')[1] == 'generated':
                if self.gen_data.empty:
                    self.gen_data = data_to_add
                else:
                    self.gen_data = pd.merge(self.gen_data, data_to_add, on=['State', 'Year'], how='outer')
            elif file.split('.')[0] == 'percentage_renewable':
                if self.renew_pc.empty:
                    self.renew_pc = data_to_add
                    self.renew_pc.name = 'percentage_renewable'
            else:
                if self.data.empty:
                    self.data = data_to_add
                else:
                    self.data = pd.merge(self.data, data_to_add, on=['State','Year'], how='outer')

            print(f'{index}. {feature} added.')

        self.data.fillna(0, inplace=True)
        return

    def add_hydropower_potential_data(self):
        with open("hydropower_potential/us_states_hydropower_potential.csv") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                for year in range(self.year_from, self.year_to + 1):
                    self.data.loc[(self.data.index.get_level_values(0)==row["State"]) &
                                  (self.data.index.get_level_values(1)==str(year)), "potential_hydro_cap"] \
                        = int(row["PotentialCapacityMW"])
                    self.data.loc[(self.data.index.get_level_values(0)==row["State"]) &
                                  (self.data.index.get_level_values(1)==str(year)),"potential_hydro_gen"] \
                        = int(row["PotentialGenerationGWHYR"])
        return

    def add_producer_price_index_data(self):
        with open("producer_price_index/us_yearly_producer_price_index.csv") as file:
            csv_reader = csv.DictReader(file)
            data = {}
            for row in csv_reader:
                data[int(row["Year"])] = row["Value"]
            for year in range(self.year_from, self.year_to + 1):
                self.data.loc[(self.data.index.get_level_values(1)==str(year)), "producer_price_index"] \
                    = data[year]
        return

    def add_state_area_data(self):
        with open("state_geography/total_state_area.csv") as file:
            csv_reader = csv.DictReader(file)
            self.data['total_state_area'] = ''
            for row in csv_reader:
                for year in range(self.year_from, self.year_to + 1):
                    self.data.loc[(self.data.index.get_level_values(0) == row["State"]) &
                                  (self.data.index.get_level_values(1) == str(year)), "total_state_area"] \
                        = float(row["Total Area (Sq. Mi.)"].replace(',', ''))
        return

    def calculate_renew_pc(self):
        self.total_gen = self.gen_data.sum(axis=1) + 1e-32
        renew_df = self.gen_data.loc[self.gen_data.index, self.renew_list]
        renew_pc = renew_df.div(self.total_gen, axis=0) * 100
        self.renew_pc = renew_pc.sum(axis=1)
        self.renew_pc.name = 'renewable_energy_percentage'


    def __call__(self, *args, **kwargs):
        self.mass_add_data()
        self.add_hydropower_potential_data()
        self.add_state_area_data()
        self.add_producer_price_index_data()

        self.calculate_renew_pc()

        if not self.gen_data.empty:
            self.data = pd.merge(self.data, self.gen_data, on=['State', 'Year'], how='outer')
        if not self.renew_pc.empty:
            self.data = pd.merge(self.data, self.renew_pc, on=['State', 'Year'], how='outer')
        self.data.fillna(0, inplace=True)

        self.data.to_csv(self.data_file_name)
        print(f'Data saved to {self.data_file_name}')
        return self.data


if __name__ == "__main__":
    a = Data(1998, 2016, 'new_consolidated_data_1998_to_2016.csv')()
    b = Data(2017, 2019, 'new_consolidated_data_2017_to_2019.csv')()

    s_a = a.sample(frac=1)
    s_b = b.sample(frac=1)
    
    s_a.to_csv('shuffled_consolidated_data_1998_to_2016.csv')
    s_b.to_csv('shuffled_consolidated_data_2017_to_2019.csv')
