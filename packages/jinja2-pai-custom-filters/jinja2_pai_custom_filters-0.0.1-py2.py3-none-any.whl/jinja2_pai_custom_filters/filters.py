#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jinja2_pai_custom_filters import __version__

import re
from jinja2.ext import Extension

__author__ = "pai"
__copyright__ = "pai"
__license__ = "mit"

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def slug(value):
    return value.lower().replace(' ', '-')

def camel_case(value):
    s1 = first_cap_re.sub(r'\1_\2', value)
    s2 = all_cap_re.sub(r'\1_\2', s1).lower()
    return s2.replace('_', '-')


class Jinja2PaiCustomFilters(Extension):
    def __init__(self, environment):
        super(Jinja2PaiCustomFilters, self).__init__(environment)
        environment.filters['slug'] = slug
        environment.filters['camel_case'] = camel_case
