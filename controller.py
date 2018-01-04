# -*- coding: utf-8 -*-
# @Author: arp
# @Date:   2017-12-27 19:09:16
# @Last Modified by:   test
# @Last Modified time: 2018-01-05 00:01:31


class BaseHandler(object):
    result_url = 'https://raw.githubusercontent.com/how2how/toy/master/data/'

    def __init__(self, guser, gpass, repo):
        pass

    @staticmethod
    def connect(u, p, r):
        pass

    def get_file(self, filepath):
        tree = self.branch.commit.commit.tree.recurse()
        for filename in tree.tree:
            if filepath in filename.path:
                print '[*] Found file %s' % filepath
                blob = repo.blob(filename._json_data['sha'])
                return blob.content
