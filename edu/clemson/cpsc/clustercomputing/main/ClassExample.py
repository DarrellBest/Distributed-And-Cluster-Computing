'''
Created on Feb 2, 2017

@author: bbest
'''

from math import *
from Singleton import Singleton


@Singleton
class MyClass(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        self.some_int = 0

    def add_one(self):
        self.some_int = self.some_int + 1

    def get_some_int(self):
        return self.some_int

    def set_some_int(self, val):
        self.some_int = val
