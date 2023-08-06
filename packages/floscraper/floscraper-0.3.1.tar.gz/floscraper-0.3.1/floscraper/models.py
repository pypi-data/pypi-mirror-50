# -*- coding: UTF-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

__author__ = "the01"
__email__ = "jungflor@gmail.com"
__copyright__ = "Copyright (C) 2017-19, Florian JUNG"
__license__ = "MIT"
__version__ = "0.1.2"
__date__ = "2018-08-04"
# Created: 2017-10-06 23:35

import flotils


class CacheInfo(flotils.FromToDictBase, flotils.PrintableBase):
    """ Cache information """

    def __init__(self, access_time=None, etag=None):
        super(CacheInfo, self).__init__()
        self.etag = etag
        """ :type : None | str | unicode """
        self.access_time = access_time
        """ :type : None | datetime.datetime """
        self.hit = None
        """ Cache hit
            :type : None | bool """


class Response(flotils.FromToDictBase, flotils.PrintableBase):
    """ Scrapper response object """

    def __init__(self, html=None, cache_info=None, scraped=None, raw=None):
        super(Response, self).__init__()
        self.cache_info = cache_info
        """ :type : None | CacheInfo """
        self.raw = raw
        """ Raw, undecoded reponse
            :type : None | unicode """
        self.html = html
        """ Html reponse
            :type : None | unicode """
        self.scraped = scraped
        """ Scrapped content
            :type : None | list | dict """

    def __str__(self):
        return "({}), {}, {}, {}".format(
            self.cache_info, self.html, self.scraped, self.raw
        )

    def to_dict(self):
        """
        Response as dict

        :return: response
        :rtype: dict
        """
        res = super(Response, self).to_dict()

        if self.cache_info:
            res['cache_info'] = self.cache_info.to_dict()
        return res

    @staticmethod
    def from_dict(d):
        """
        Response from dict

        :param d: Dict to load
        :type d: dict
        :return: response
        :rtype: Response
        """
        if d is None:
            return None
        return Response(
            d.get('html'),
            CacheInfo.from_dict(d.get('cache_info')),
            d.get('scraped'),
            d.get('raw')
        )
