#!/usr/bin/python3
"""do_deploy module
"""
from fabric.api import run, env, put
from os import path


env.hosts = ['54.236.49.90', '18.234.129.85']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """function that distributes an archive to your web servers"""
    if not path.exists(archive_path):
        return False

    archive_name = archive_path.split('/')[-1]

    try:
        archive_folder = archive_name.split('.')[0]

        put(archive_path, '/tmp/')
        run(f'mkdir -p /data/web_static/releases/{archive_folder}')
        run(f'tar -xzf /tmp/{archive_name} \
                -C /data/web_static/releases/{archive_folder}')
        run(f'rm -rf /tmp/{archive_name}')
        run(f'cp -r /data/web_static/releases/{archive_folder}/web_static/* \
                /data/web_static/releases/{archive_folder}/')
        run(f'rm -rf /data/web_static/releases/{archive_folder}/web_static/')
        run(f'ln -sf /data/web_static/releases/{archive_folder} \
                /data/web_static/current')
        print('New version deployed!')
        return True
    except Exception as e:
        return False
