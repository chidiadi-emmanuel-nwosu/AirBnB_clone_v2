#!/usr/bin/python3
"""keep clean module
"""
from fabric.api import run, local, env, cd, lcd

env.hosts = ['54.236.49.90', '54.175.254.64']
env.user = 'ubuntu'


def do_clean(number=0):
    """deletes out-of-date archives"""
    num = 1 if not int(number) else int(number)
    num += 1

    with lcd('versions'):
        local(f'ls -t | tail -n {num} | xargs rm -rf')
    with cd('/data/web_static/releases'):
        run(f'ls -t | tail -n {num} | xargs rm -rf')
