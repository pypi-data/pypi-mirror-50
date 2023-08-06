# -*- coding: UTF-8 -*-
"""
A scraper utility package
"""

__author__ = "the01"
__email__ = "jungflor@gmail.com"
__copyright__ = "Copyright (C) 2014-19, Florian JUNG"
__license__ = "MIT"
__version__ = "0.3.1"
__date__ = "2019-08-04"

from .webscraper import WebScraper, default_user_agents, \
    WEBConnectException, WEBFileException, WEBParameterException
from .cache import Cache
from .models import Response, CacheInfo

__all__ = [
    "webscraper", "WebScraper", "Cache", "Response", "CacheInfo"
]
