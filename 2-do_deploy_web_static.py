#!/usr/bin/python3
"""do_deploy module
"""
from fabric.api import run, env, put
import os

env.hosts = ['54.236.49.90', '54.175.254.64']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """function that distributes an archive to your web servers"""
    if not os.path.exists(archive_path):
        return False

    name = archive_path.split('/')[-1]
    folder = name.split('.')[0]

    try:
        put(archive_path, '/tmp/')
        run(f'mkdir -p /data/web_static/releases/{folder}')
        run(f'tar -xzf /tmp/{name} -C /data/web_static/releases/{folder}')
        run(f'rm /tmp/{name}')
        run(f'mv /data/web_static/releases/{folder}/web_static/* '
            f'/data/web_static/releases/{folder}/')
        run(f'rm -rf /data/web_static/releases/{folder}/web_static/')
        run(f'rm -rf /data/web_static/current')
        run(f'ln -s /data/web_static/releases/{folder} '
            '/data/web_static/current')
        print('New version deployed!')
        return True
    except Exception:
        return False
