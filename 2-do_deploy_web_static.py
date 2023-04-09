#!/usr/bin/python3
""" Contains functions relating to deployment of web static files """

from fabric.api import env, local, put, run
from datetime import datetime
from fabric.decorators import runs_once
import os

env.user = 'ubuntu'
env.hosts = ['18.210.10.94', '54.160.73.81']


@runs_once
def do_pack():
    """ Compresses folder content to a tgz archive """
    local("mkdir -p versions")
    file_path = ("versions/web_static_{}.tgz"
                 .format(datetime.strftime(datetime.now(),
                         "%Y%m%d%H%M%S")))
    compress = local("tar -cvzf {} web_static".format(file_path))

    if compress.failed:
        return None
    return file_path


def do_deploy(archive_path):
    """Distributes the packed archive above to web servers"""

    if os.path.exists(archive_path) is False:
        return False

    file_name = os.path.basename(archive_path)
    folder = file_name.replace(".tgz", "")
    folder_path = "/data/web_static/releases/{}/".format((folder_name)
    flag = False

    try:
        put(archive_path, "/tmp/{}".format(file_name))
        run("mkdir -p {}".format(folder_path))
        run("tar -xzf /tmp/{} -C {}".format(file_name, folder_path))
        run("rm -rf /tmp/{}".format(file_name))
        run("mv {}web_static/* {}".format(folder_path, file_name))
        run("rm -rf {}web_static".format(folder_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder_path))
        print("New version deployed!")
        flag = True

    except Exception:
        flag = False
    return flag
