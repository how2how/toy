# Simple Loader
from ghimp import add_remote_repo
add_remote_repo(
    ['toy'],
    'https://raw.githubusercontent.com/how2how/toy/master')
    # 'http://localhost:8000')
# add_remote_repo(
#     ['covertutils'],
#     'https://raw.githubusercontent.com/operatorequals/covertutils/master')
# add_remote_repo(
#     ['nacl'],
#     'https://raw.githubusercontent.com/pyca/pynacl/master/src/')
from toy.boy import Boy
# import json
print(dir(Boy))
print(Boy.__file__)
print(Boy.__path__)
print(Boy.__package__)
config = Boy.get_config(Boy._url)
# config = json.load(open('../test_conf.json','rb'))
b = Boy(config)
b.run()
