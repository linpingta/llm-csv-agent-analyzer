# -*- coding: utf-8 -*-
# vim: set bg=dark noet ts=4 sw=4 fdm=indent :

""" util tools"""
__author__ = 'linpingta'

import os


def is_file_with_type(filename, file_type='csv'):
    _, file_extension = os.path.splitext(filename)
    return file_extension.lower() == file_type
