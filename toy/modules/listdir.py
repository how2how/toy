# -*- coding: utf-8 -*-
# @Author: test
# @Date:   2017-01-19 12:44:34
# @Last Modified by:   arp
# @Last Modified time: 2018-01-01 19:20:50

import os
from packages.test import run as info


def run(**args):
    print '[*] In listdir module.'
    files = os.listdir('.')
    return info() + '\n' + str(files)
