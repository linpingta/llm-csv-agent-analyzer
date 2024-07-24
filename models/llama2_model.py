# -*- coding: utf-8 -*-
# vim: set bg=dark noet ts=4 sw=4 fdm=indent :

""" Wrapper of llama2 model"""
__author__ = 'linpingta'

from .model_configs import DEFAULT_LLAMA2_CONFIG


class Llama2Model(object):
    def __init__(self, api_config=DEFAULT_LLAMA2_CONFIG):
        self.config = api_config

    def run(self, prompt, n=1, system_message="", logger=None):
        pass