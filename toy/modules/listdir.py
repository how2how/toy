# -*- coding: utf-8 -*-
# @Author: test
# @Date:   2017-01-19 12:44:34
# @Last Modified by:   test
# @Last Modified time: 2018-01-04 22:55:19

import os
from toy.modules.packages import test as info


def run(**args):
    print '[*] In listdir module.'
    files = os.listdir('.')
    return info.run() + '\n' + str(files)
