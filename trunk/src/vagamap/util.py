'''
Created on Dec 26, 2011

@author: Matt
'''
import new

def to_module(code, test_data=''):
    module = new.module('usercode')
    module.__dict__['test_input'] = test_data
    exec code in module.__dict__
    return module