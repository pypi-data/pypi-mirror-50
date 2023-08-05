#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import requests

class BrokenSourceException(Exception):
    """ BrokenSourceException: raised when a source is broken """
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

class UnscrapableSourceException(Exception):
    """ UnscrapableSourceException: raised when a source is not scrapable """
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

BROKEN_EXCEPTIONS = (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, BrokenSourceException)
