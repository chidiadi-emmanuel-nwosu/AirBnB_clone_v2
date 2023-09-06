#!/usr/bin/python3
"""do_pack module
"""
from fabric.api import run, local
from datetime import datetime


def do_pack():
    """function that generates a .tgz archive from the
       the contents of webstatic folder
    """
    try:
        print("in here")
        created_at = datetime.now().strftime('%Y%m%d%H%M%S')
        local('mkdir -p versions')
        archive_name = f"web_static_{created_at}.tgz"
        local(f'tar -czvf versions/{archive_name} web_static')
        return f"versions/{archive_name}"
    except Exception as e:
        return None
