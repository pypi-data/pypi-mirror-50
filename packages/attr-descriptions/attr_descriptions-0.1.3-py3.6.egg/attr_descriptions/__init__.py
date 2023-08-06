import logging

import typing
import attr
import cattr

import math
from functools import reduce


# create logger
module_logger = logging.getLogger(__name__)
module_logger.setLevel(logging.DEBUG)


def describe(attrib, description, significant_digits=None):
    attrib.metadata['__description'] = description
    attrib.metadata['__significant_digits'] = significant_digits
    return attrib

def get(cls, attr_name, default_description, default_significant_digits):
    meta = attr.fields_dict(cls)[attr_name]
    info = {}

    try:
        description = meta.metadata['__description']
    except:
        description = None
    
    try:
        sig_digits = meta.metadata['__significant_digits']
    except:
        sig_digits = None

    info['description'] = description if description is not None else default_description
    info['significant_digits'] = sig_digits if sig_digits is not None else default_significant_digits

    return info


def add_attr_description(attrib, description=None):
    attrib.metadata['__description'] = description
    return attrib

def get_attr_description(cls, attr_name, default=None):
    meta = attr.fields_dict(cls)[attr_name]

    try:
        return meta.metadata['__description']
    except:
        return default
    



