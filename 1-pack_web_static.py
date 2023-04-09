#!/usr/bin/python3
""" Fabric script that compresses to an archive """

from fabric.api import local
from datetime import datetime
from fabric.decorators import runs_once


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
