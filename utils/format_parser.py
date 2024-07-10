# -*- coding: utf-8 -*-
# vim: set bg=dark noet ts=4 sw=4 fdm=indent :

""" util tools"""
__author__ = 'linpingta'


def param_str_to_dict(input_str, split_symbol1=',', split_symbol2='='):
    param_dict = {}
    if input_str:
        # Assuming the input string is in the format key1=value1,key2=value2,...
        param_pairs = input_str.split(split_symbol1)
        for pair in param_pairs:
            key, value = pair.split(split_symbol2)
            param_dict[key] = value
    return param_dict


def param_str_to_list(input_str, split_symbol1=','):
    return input_str.split(split_symbol1)
