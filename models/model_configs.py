# -*- coding: utf-8 -*-
# vim: set bg=dark noet ts=4 sw=4 fdm=indent :

""" model configs"""
__author__ = 'linpingta'

# default gpt setting
DEFAULT_GPT_CONFIG = {
    "engine": "devgpt4-32k",
    "temperature": 0.0,
    "max_tokens": 5000,
    "top_p": 1.0,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0
}


DEFAULT_LLAMA2_CONFIG = {
    "task": "text-generation",
    "device_map": "auto"
}