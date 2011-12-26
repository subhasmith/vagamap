'''
Created on Dec 24, 2011

@author: Matt
'''
import os 
import jinja2

folder = os.path.dirname(__file__)
jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(folder, 'templates')))