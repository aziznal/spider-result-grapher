import numpy as np
import pandas as pd


class DataCleaner:

    def __init__(self, data: pd.DataFrame):
        self.data = data

    def _check_duplicates(self, data):

        prev_val = None
        duplicate_counter = 0

        for index, row in data.iterrows():

            # Skip 1st iteration to set prev_val
            if index == 0:
                prev_val = row
                continue

            # Actual Loop
            if prev_val[0] == row[0]:
                duplicate_counter += 1

            prev_val = row

        return duplicate_counter > 0

    def _new_time_val(self, datetime_, flag=False):

        date, hour = datetime_.split('_')

        if not flag:
            hour += ":30"
        else:
            hour += ":00"

        fixed_datetime = "_".join([date, hour])

        return fixed_datetime

    def _fix_duplicates(self, data):
        """
        This method does NOT delete duplicate time values, but instaed
        appends seconds (as :00 or :30) to the end of each entry.

        Note that foreach entry in the column, at most there will be 
        two values that are the same.
        """

        prev_val = None

        for index, row in data.iterrows():

            # Skip 1st iteration to set prev_val
            if index == 0:
                prev_val = row
                new_val = self._new_time_val(row[0], True)
                data.at[index, 'time'] = new_val
                continue

            # Actual Loop
            if prev_val[0] == row[0]:
                new_val = self._new_time_val(row[0])
                data.at[index, 'time'] = new_val

            else:
                new_val = self._new_time_val(row[0], flag=True)
                data.at[index, 'time'] = new_val

            prev_val = row

    def _repair_time_column(self, data):
        """
        Time column has rows that refer to different rates but have the
        same value. This method fixes that by appending a ':00' or ':30' to the
        hour:minute section of the date
        """
        has_duplicates = self._check_duplicates(data)

        if has_duplicates:
            self._fix_duplicates(data)

        else:
            return

    def _create_date_column(self, data):
        date_column = []

        for val in data['time']:
            date_val = val.split('_')[0]
            date_column.append(date_val)

        data['date'] = np.array(date_column)

    def _create_hour_column(self, data):
        hourminute_column = []

        for val in data['time']:
            hourminute_val = val.split('_')[1]
            hourminute_column.append(hourminute_val)

        data['hour_minute'] = np.array(hourminute_column)

    def _remove_data_spikes(self, data):
        print("Getting all data spikes: ")

        data_spikes = data[data['buying'] / data['selling'] > 1.015]

        before = len(data)

        cond = data['buying'].isin(data_spikes['buying'])
        data.drop(data[cond].index, inplace = True)

        after = len(data)

        print(f"Removed {before - after} spikes in data")

    def clean(self):
        """
        This method does the following:

        :fixes duplicates in time column

        :creates date column

        :creates hour column

        :removes dataspikes
        """

        self._repair_time_column(self.data)

        self._create_date_column(self.data)

        self._create_hour_column(self.data)

        self._remove_data_spikes(self.data)


class DataMerger:
    def __init__(self, datasets):
        self.datasets = datasets

    def get_all_unique_dates(self):
        return next(iter(self.datasets.values()))['date'].unique()

    def create_perfect_time_series(self):

        dates = self.get_all_unique_dates()

        starting_time = [9, 0]
        ending_time = [17, 59]

        time_list = []

        for date in dates:

            starting_time = [9, 0]

            while starting_time[0] <= ending_time[0]:
                while starting_time[1] <= ending_time[1]:
                    prefix1 = "0" if starting_time[0] < 10 else ""
                    prefix2 = "0" if starting_time[1] < 10 else ""

                    entry = f"{date}_{prefix1 + str(starting_time[0])}:{prefix2 + str(starting_time[1])}:00"
                    time_list.append(entry)

                    entry = f"{date}_{prefix1 + str(starting_time[0])}:{prefix2 + str(starting_time[1])}:30"
                    time_list.append(entry)

                    starting_time[1] += 1

                starting_time[0] += 1
                starting_time[1] = 0

        return pd.Series(data=np.array(time_list))

    def compare_with_common_times(self, common_times):
        for bankname, data in self.datasets.items():
            len_before = len(common_times)

            common_times = common_times[common_times.isin(data['time'])]

            len_after = len(common_times)

            print(f"({bankname}) Removed {len_before - len_after} rows from common_times\n")

        return common_times

    def remove_uncommon_rows(self, common_times):
        for bankname, data in self.datasets.items():
            len_before = len(self.datasets[bankname])

            self.datasets[bankname] = data[data['time'].isin(common_times)]
            
            len_after = len(self.datasets[bankname])

            print(f"({bankname}) Removed {len_before - len_after} rows\n")

    def merge_data(self):
        """
        For each dataset, keep only the rows which are also present in all other datasets.
        This (in theory) should fix the overlapping data bug
        """
        # Algorithm:
        #   1 - Create an artificial common_times Series which has all possible times
        #
        #   2 - Foreach bankdata:
        #       - Remove from common_times rows which are not in current bankdata
        #   
        #   3 - Foreach bankdata:
        #       - Remove from bankdata rows which are not in common_times
        
        # Step 1
        common_times = self.create_perfect_time_series()

        # Step 2
        common_times = self.compare_with_common_times(common_times)

        # Step 3
        self.remove_uncommon_rows(common_times)

        return self.datasets
