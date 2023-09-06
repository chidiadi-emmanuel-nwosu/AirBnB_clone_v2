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

    try:
        archive_name = archive_path.split('/')[-1]
        release_folder = f'/data/web_static/releases/{name.split(".")[0]}'

        put(archive_path, '/tmp/')
        run(f'mkdir -p {release_folder}')
        run(f'tar -xzf /tmp/{archive_name} -C {release_folder}')
        run(f'rm /tmp/{archive_name}')
        run(f'mv {release_folder}/web_static/* {release_folder}/')
        run(f'rm -rf /data/web_static/releases/{folder}/web_static/')
        run(f'ln -sf {release_folder} /data/web_static/current')
        print('New version deployed!')
        return True
    except Exception:
        return False
