import os
import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta


class Settings:
    def __init__(self):
        # Working root folder (the only path that should be changed)
        self.root_folder = r"D:\Software\temp\CeDX\data_2024_05"
        self.input_folder = self.root_folder + '/data'
        self.tmp1_folder = self.input_folder + '/tmp'
        self.tmp2_folder = self.input_folder + '/tmp2'
        self.output_folder = self.root_folder + '/output'#_under_1year'
        
        # current year
        self.year_limit = 2024
        
        # last day of current month of data (31-12-current_year)
        self.month_last = 20240430
        self.month_last_dt = datetime.strptime(str(self.month_last), '%Y%m%d')
        
        self.one_year_ago_dt = self.month_last_dt - relativedelta(years=1)
        
        # First day of next month of data (month_last + 1day)
        self.month_to = 20240501
        self.month_to_str = 'month_to_' + str(self.month_to)
        
        
        folders_to_create = [self.input_folder, self.tmp1_folder, self.tmp2_folder, self.output_folder]
        self.create_directories(folders_to_create)
        
    def create_directories(self, directory_list):
        for directory in directory_list:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"Directory created: {directory}")
            else:
                print(f"Directory found: {directory}")
                
    def remove_non_numeric_chars(self, input_string):
        return ''.join(char for char in input_string if char.isdigit())

    def modify_phone_num_column(self, df, col):
        df[col] = df[col].apply(lambda x: self.remove_non_numeric_chars(str(x))).dropna()
        df = df[df[col] != '']
        df[col] = df[col].astype(np.longlong).astype(str)
        return df
              