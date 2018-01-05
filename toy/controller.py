# -*- coding: utf-8 -*-
# @Author: arp
# @Date:   2017-12-27 19:09:16
# @Last Modified by:   test
# @Last Modified time: 2018-01-05 00:01:31
from github3 import login


class BaseHandler(object):
    result_url = 'https://raw.githubusercontent.com/how2how/toy/master/data/'

    def __init__(self, guser, gpass, repo):
        self.gh = self.repo = self.branch = None
        self.connect(guser, gpass, repo)

    def connect(self, u, p, repo):
        self.gh = login(username=u, password=p)
        self.repo = self.gh.repository(u, repo)
        self.branch = self.repo.branch('master')
        return

    def get_file(self, filepath):
        tree = self.branch.commit.commit.tree.recurse()
        for filename in tree.tree:
            if filepath in filename.path:
                print '[*] Found file %s' % filepath
                blob = self.repo.blob(filename._json_data['sha'])
                return blob.content

    def get_result(self, boy_id):
        pass

    def update_config(self, config):
        pass
