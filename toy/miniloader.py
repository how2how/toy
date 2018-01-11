# Simple Loader
from httpimp import add_remote_repo
add_remote_repo(
    ['toy'],
    'https://raw.githubusercontent.com/how2how/toy/master')
from toy.boy import Boy
import json

# config = Boy.get_config(Boy.config_url + Boy._id + '.json')
config = json.load(open('../test_conf.json','rb'))
b = Boy(config)
b.run()
