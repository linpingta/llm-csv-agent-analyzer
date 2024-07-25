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

from prompts.const import DEFAULT_PROMPT
from tasks.fund_analyze_task import FundAnalyzeTask
from tasks.estate_analyze_task import EstateAnalyzeTask
from tasks.duck_task import DuckTask
from utils.format_parser import param_str_to_dict, param_str_to_list
from utils.file_parser import is_file_with_type, extract_filename
from utils.data_loader import DataLoader
from models.model_configs import DEFAULT_GPT_CONFIG, DEFAULT_LLAMA2_CONFIG
from models.llama2_model import Llama2Model
from models.openai_model import OpenAIModel


def build_prompt(task_name, prompt_template_path, prompt_id, prompt_param_dict, logger):
    logger.info("build prompt for task[%s]" % task_name)
    prompt_template_dict = {}
    with open(prompt_template_path, 'r') as file:
        prompt_template_dict = json.load(file)

    if prompt_id < 0 or prompt_id not in prompt_template_dict:
        logger.warning("fail to load prompt_id[%d] inside prompt_template_path[%s]" % (prompt_id, prompt_template_path))
        return DEFAULT_PROMPT

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
        dloader.add_df(extract_filename(filename), df)
    return dloader


def build_model(model_type, model_name, model_temperature, model_top_p, system_message, logger):
    if model_type == 'openai':
        model_config = DEFAULT_GPT_CONFIG
        model_config['model_name'] = model_name
        model_config['temperature'] = model_temperature
        model_config['top_p'] = model_top_p

        api_key = os.environ.get("OPENAI_API_KEY")
        api_base = os.environ.get("API_BASE")
        api_version = os.environ.get("API_VERSION")
        return OpenAIModel(
            api_config=model_config,
            openai_api_key=api_key,
            openai_api_base=api_base,
            openai_api_version=api_version,
            system_message=system_message
        )
    elif model_type == 'llama2':
        model_config = DEFAULT_LLAMA2_CONFIG
        model_config['model_name'] = model_name
        return Llama2Model(model_config)
    return None


def get_task(task_name, conf):
    if task_name.strip() == 'fund_analyzer_task':
        return FundAnalyzeTask(conf)
    elif task_name.strip() == 'estate_analyzer_task':
        return EstateAnalyzeTask(conf)
    return DuckTask(conf)


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
    parser.add_argument('--inference_one_prompt_id', type=int, default=0)
    parser.add_argument('--inference_one_prompt_param', type=str, default='',
                        help="str parameter converts into a dict, format: key1=value1,key2=value2")
    parser.add_argument('--question', type=str, default='', help="question which may need answer")
    parser.add_argument('--model_type', type=str, choices=['openai', 'llama2'], required=True)
    parser.add_argument('--model_temperature', type=float, default=0.0)
    parser.add_argument('--model_top_p', type=float, default=1.0)
    # model name should be valid in backend, like
    # LLAMA: 'llama-7b', 'llama-13b', 'llama-30b', 'llama-65b'
    # OpenAI: gpt-3.5-turbo, gpt-4, gpt-4-turbo
    parser.add_argument('--model_name', type=str, default='gpt-3.5-turbo')
    parser.add_argument('--system_message', type=str, default='')

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

        # prepare prompt from template
        prompt = build_prompt(args.task, conf.get(task.name, "question_prompt_template_path"),
                              args.inference_one_prompt_id,
                              param_str_to_dict(args.inference_one_prompt_param), logger)
        task.set_prompt(prompt, logger)

        model = build_model(args.model_type, args.model_name, args.model_temperature, args.model_top_p,
                            args.system_message, logger)
        task.set_model(model, logger)

        task.inference(args.question, logger)
    except Exception as e:
        logger.exception(e)
