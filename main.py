# -*- coding: utf-8 -*-
# vim: set bg=dark noet ts=4 sw=4 fdm=indent :

""" Main file for llm csv analyzer"""
__author__ = 'linpingta'

import os
import sys
import logging
import argparse
import json
import pandas as pd

try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser

from tasks.fund_analyze_task import FundAnalyzeTask
from utils.format_parser import param_str_to_dict, param_str_to_list
from utils.file_parser import is_file_with_type
from utils.data_loader import DataLoader


def build_prompt(task_name, prompt_template_path, prompt_id, prompt_param_dict, logger):
    logger.info("build prompt for task[%s]" % task_name)
    prompt_template_dict = {}
    with open(prompt_template_path, 'r') as file:
        prompt_template_dict = json.load(file)

    if prompt_id not in prompt_template_dict:
        logger.error("fail to load prompt_id[%d] inside prompt_template_path[%s]" % (prompt_id, prompt_template_path))
        return ""

    prompt_template = prompt_template_dict[prompt_id]

    '''
    An example: prompt_template = '{name} likes {game}', template_dict = {'name':'lipinta', 'game':'football'}
    '''
    return prompt_template.format(**prompt_param_dict)


def build_data_loader(task_name, data_path, filenames, logger):
    logger.info("build data loader for task[%s]" % task_name)

    dloader = DataLoader()
    for filename in param_str_to_list(filenames):
        full_filename = os.path.join(data_path, filename)
        if not is_file_with_type(full_filename, 'csv'):  # csv file check
            logger.warn("task[%s] fails to load filename[%s] with wrong type" % (task_name, full_filename))
            continue

        df = pd.read_csv(full_filename)
        dloader.add_df(filename, df)
    return dloader


def get_task(task_name, conf):
    if task_name.strip() == 'llm_csv_analyzer':
        return FundAnalyzeTask(conf)
    return None


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(filename)s:%(lineno)s - %(funcName)s %(asctime)s;%(levelname)s] %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S'
    )
    logger = logging.getLogger(__file__)

    example_word = """
        DESCRIBE ARGUMENT USAGE HERE
        python main.py --help
    """
    parser = argparse.ArgumentParser(prog=__file__, description='code description', epilog=example_word,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    # add parameter if needed
    parser.add_argument('-v', '--version', help='version of code', action='version', version='%(prog)s 1.0')
    parser.add_argument('--task', type=str, choices=['llm_csv_analyzer'], required=True, default='llm_csv_analyzer')
    parser.add_argument('--inference_type', type=str, choices=['all', 'one'], required=True, default='all')
    parser.add_argument('--inference_one_prompt_id', type=int, default=0)
    parser.add_argument('--inference_one_prompt_param', type=str, default='', help="str parameter converts into a dict")

    args = parser.parse_args()

    try:
        # analyzer.conf: used for code config
        # prompt_template.json: used for prompt template management, contains parameters
        # prompt_parameter.json: used for parameter fill logic
        conf = ConfigParser.RawConfigParser()
        conf.read('analyzer.conf')

        # get_task
        task = get_task(args.task, conf)

        # build data loader
        # input data file will be provided as context
        data_loader = build_data_loader(args.task, conf.get(task.name, "input_data_path"),
                                        conf.get(task.name, "input_filenames"), logger)
        task.set_data_loader(data_loader, logger)

        if args.inference_type == 'all':
            task.inference_all(logger)
        elif args.inference_type == 'one':
            prompt = build_prompt(args.task, conf.get(task.name, "question_prompt_template_path"),
                                  args.inference_one_prompt_id,
                                  param_str_to_dict(args.inference_one_prompt_param), logger)
            task.inference_one(prompt, logger)
    except Exception as e:
        logger.exception(e)
