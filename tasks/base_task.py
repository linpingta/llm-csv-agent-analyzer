# -*- coding: utf-8 -*-
# vim: set bg=dark noet ts=4 sw=4 fdm=indent :

""" base task """
__author__ = 'linpingta'
from abc import ABCMeta, abstractmethod


class BaseTask(object):
    """
    Base class for tasks.
    """

    __metaclass__ = ABCMeta

    def __init__(self, config):
        self.data_loader_ = None

    def set_data_loader(self, data_loader, logger):
        self.data_loader_ = data_loader
        self._preprocess_data(logger)

    @abstractmethod
    def _preprocess_data(self, logger):
        pass

    @abstractmethod
    def inference_all(self, logger):
        pass

    @abstractmethod
    def inference_one(self, prompt, logger):
        pass
