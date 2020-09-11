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
