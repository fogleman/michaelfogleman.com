from fabric.api import *

env.hosts = ['michaelfogleman.com']

def deploy():
    with cd('michaelfogleman.com'):
        run('git pull')
    run('sudo service michaelfogleman.com restart')
