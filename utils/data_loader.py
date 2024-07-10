# -*- coding: utf-8 -*-
# vim: set bg=dark noet ts=4 sw=4 fdm=indent :

""" data loader"""
__author__ = 'linpingta'

import pandas as pd


class DataLoader(object):
    def __init__(self):
        self.csv_df_dict = {}

    def add_df(self, name, df):
        self.csv_df_dict[name] = df

    def get_df_by_name(self, name):
        return self.csv_df_dict[name] if name in self.csv_df_dict else pd.DataFrame

    def get_all_df(self):
        return self.csv_df_dict
