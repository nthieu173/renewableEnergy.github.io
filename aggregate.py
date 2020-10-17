import csv
import pandas as pd
import os
import time

class Data():
    def __init__(self, year_from, year_to, data_file_name):
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
        self.year_index = []
        for year in range(self.year_from, self.year_to + 1):
            self.year_index.append(str(year))

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
            data_to_add = new_data[self.year_index]
            data_to_add = data_to_add.stack()
            feature = file.split('.')[0]
            data_to_add.name = feature
            data_to_add.index.names = ['State','Year']
            if self.data.empty:
                self.data = data_to_add
            else:
                self.data = pd.merge(self.data, data_to_add, on=['State','Year'], how='outer')

            print(f'{index}. {feature} added.')

        self.data.fillna(0, inplace=True)
        return

    def add_hydropower_potential_data(self):
        # hydro_data = pd.read_csv(os.path.join(self.data_dir, 'hydropower_potential.csv'), index_col=0)
        # hydro_data.columns = ['hydropower_potential_capacity', 'hypdropower_potential_generation_GWHYR']
        # for column in hydro_data.columns:
        #     new_data = hydro_data[column]
        #     new_data_list = [new_data] * len(self.year_index)
        #     new_data = pd.concat(new_data_list, axis=1)
        #     new_data.columns = self.year_index
        #     new_data = new_data.stack()
        #     new_data.index.names = ['State','Year']
        #     new_data.name = column
        #     print(new_data)
        #     self.data = pd.merge(self.data, new_data, on=['State','Year'], how='outer')
        #
        # self.data.fillna(0, inplace=True)
        # print('Hydropower potential added.')
        # return

        with open("hydropower_potential/us_states_hydropower_potential.csv") as file:
            csv_reader = csv.DictReader(file)
            # self.data['potential_hydro_cap'] = ''
            # self.data['potential_hydro_gen'] = ''
            for row in csv_reader:
                for year in range(self.year_from, self.year_to + 1):
                    self.data.loc[(self.data.index.get_level_values(0)==row["State"]) &
                                  (self.data.index.get_level_values(1)==str(year)), "potential_hydro_cap"] \
                        = int(row["PotentialCapacityMW"])
                    self.data.loc[(self.data.index.get_level_values(0)==row["State"]) &
                                  (self.data.index.get_level_values(1)==str(year)),"potential_hydro_gen"] \
                        = int(row["PotentialGenerationGWHYR"])
        return

    def add_state_area_data(self):
        # area_data = pd.read_csv(os.path.join(self.data_dir, 'total_state_area.csv'), index_col=0, thousands=',')
        # area_data.columns = ['total_state_area']
        #
        # new_data_list = [area_data] * len(self.year_index)
        # new_data = pd.concat(new_data_list, axis=1)
        # new_data.columns = self.year_index
        # new_data = new_data.stack()
        # new_data.index.names = ['State', 'Year']
        # new_data.name = area_data.columns[0]
        # print(new_data)
        # self.data = pd.merge(self.data, new_data, on=['State', 'Year'], how='outer')
        # self.data.fillna(0, inplace=True)
        #
        # print('State area added.')
        # return

        with open("state_geography/total_state_area.csv") as file:
            csv_reader = csv.DictReader(file)
            self.data['total_state_area'] = ''
            for row in csv_reader:
                for year in range(self.year_from, self.year_to + 1):
                    self.data.loc[(self.data.index.get_level_values(0) == row["State"]) &
                                  (self.data.index.get_level_values(1) == str(year)), "total_state_area"] \
                        = float(row["Total Area (Sq. Mi.)"].replace(',', ''))
        return

    def __call__(self, *args, **kwargs):
        self.mass_add_data()
        self.add_hydropower_potential_data()
        self.add_state_area_data()

        self.data.to_csv(self.data_file_name)
        print(f'Data saved to {self.data_file_name}')
        return self.data


if __name__ == "__main__":
    #main()
    # exclude = ['us_states_hydropower_potential.csv', 'total_state_area.csv']
    # data = mass_add_data(exclude, 1998, 2016)
    # print(os.getcwd())
    a = Data(1998, 2016, 'new_consolidated_data.csv')()
    print(a.shape)
