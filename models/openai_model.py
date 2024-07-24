# -*- coding: utf-8 -*-
# vim: set bg=dark noet ts=4 sw=4 fdm=indent :

""" Wrapper of openai model"""
__author__ = 'linpingta'

import os
import openai
from .model_configs import DEFAULT_GPT_CONFIG


class OpenAIModel(object):
    def __init__(self,
                 api_config=DEFAULT_GPT_CONFIG,
                 openai_api_key="",
                 openai_api_base="",
                 openai_api_version="",
                 system_message=""):
        # set api key
        openai.api_key = openai_api_key
        openai.api_base = openai_api_base
        openai.api_version = openai_api_version

        self.api_config = api_config
        self.system_message = system_message
        self.completion_tokens = 0
        self.prompt_tokens = 0

    def run(self, prompt, n=1, system_message="", logger=None):
        try:
            logger.info("start api request")

            # system message if needed
            sys_m = system_message if system_message else self.system_message
            messages = [{"role": "system", "content": sys_m}, {"role": "user", "content": prompt}] if sys_m else [
                {"role": "user", "content": prompt}]

            text_outputs = []
            raw_responses = []
            while n > 0:
                cnt = min(n, 10)
                n -= cnt
                res = openai.ChatCompletion.create(messages=messages, n=cnt, **self.api_config)
                text_outputs.extend(choice["message"]["content"] for choice in res["choices"])

                # add log into raw response
                res['prompt'] = prompt
                if sys_m:
                    res['system_message'] = sys_m
                raw_responses.append(res)

                # log token usage
                self.completion_tokens += res["usage"]["completion_tokens"]
                self.prompt_tokens += res["usage"]["prompt_tokens"]

            return text_outputs, raw_responses
        except Exception as e:
            logger.exception("An error occurred:", e)
            return [], []