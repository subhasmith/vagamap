'''
Created on Dec 24, 2011

@author: Matt
'''
import os 
import jinja2

folder = os.path.dirname(__file__)
jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(folder, 'templates')))

def format_datetime(value, fmt=None):
    if not fmt:
        fmt = """%m/%d/%y %H:%M:%S"""
    if value:
        return value.strftime(fmt)
    return ''

jinja_environment.filters['datetime'] = format_datetime