# -*- coding: utf-8 -*-
# @Author: test
# @Date:   2017-01-19 12:44:34
# @Last Modified by:   test
# @Last Modified time: 2017-01-19 12:47:24

import os
from packages import test as info


def run(**args):
    print '[*] In listdir module.'
    files = os.listdir('.')
    return info.run() + '\n' + str(files)
