#!/usr/bin/python3
"""deploy module
"""
from fabric.api import run, local, env, put
from datetime import datetime
import os

env.hosts = ['54.236.49.90', '54.175.254.64']
env.user = 'ubuntu'


def do_pack():
    """function that generates a .tgz archive from the
       the contents of webstatic folder
    """
    try:
        print("in here")
        created_at = datetime.now().strftime('%Y%m%d%H%M%S')
        local('mkdir -p versions')
        archive_name = f"web_static_{created_at}.tgz"
        local(f'tar -cvzf versions/{archive_name} web_static')
        return f"versions/{archive_name}"
    except Exception as e:
        return None


def do_deploy(archive_path):
    """function that distributes an archive to your web servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        arc_name = archive_path.split('/')[-1]
        release_folder = f'/data/web_static/releases/{arc_name.split(".")[0]}'

        put(archive_path, '/tmp/')
        run(f'mkdir -p {release_folder}')
        run(f'tar -xzf /tmp/{arc_name} -C {release_folder}')
        run(f'rm /tmp/{arc_name}')
        run(f'mv {release_folder}/web_static/* {release_folder}/')
        run(f'rm -rf /data/web_static/releases/{release_folder}/web_static/')
        run(f'ln -sf {release_folder} /data/web_static/current')
        print('New version deployed!')
        return True
    except Exception:
        return False


def deploy():
    """creates and distributes an archive to the web servers"""
    archive_name = do_pack()
    if not archive_name:
        return False

    return do_deploy(archive_name)
