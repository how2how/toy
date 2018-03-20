# Simple Loader
from ghimp import add_remote_repo
add_remote_repo(
    ['toy'],
    'https://raw.githubusercontent.com/how2how/toy/master')
# add_remote_repo(
#     ['covertutils'],
#     'https://raw.githubusercontent.com/operatorequals/covertutils/master')
# add_remote_repo(
#     ['nacl'],
#     'https://raw.githubusercontent.com/pyca/pynacl/master/src/')
from toy.boy import Boy
# import json

config = Boy.get_config(Boy._url)
# config = json.load(open('../test_conf.json','rb'))
b = Boy(config)
b.run()
