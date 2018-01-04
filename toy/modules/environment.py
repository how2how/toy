# -*- coding: utf-8 -*-
# @Author: test
# @Date:   2017-01-19 12:47:42
# @Last Modified by:   test
# @Last Modified time: 2017-01-19 12:48:54
import os


def run(**args):
    print '[*]In environment module.'
    return str(os.environ)
