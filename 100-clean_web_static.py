#!/usr/bin/python3
""" Fabric script that generates a .tgz archive """
from fabric.decorators import task
from fabric.api import *
from datetime import datetime
import os

env.hosts = ["54.83.139.117", "54.205.140.203"]


@task
def do_clean(number=0):
    """formats input and cleans remote"""
    n = 1
    if int(number) != 0:
        n = int(number)
    pth = "/data/web_static/releases/*"
    local("sudo ls -dtr ./versions/* | head -n -{} | xargs sudo rm -fr".format(n))
    run("sudo ls -dtr {} | head -n -{} | xargs sudo rm -fr".format(pth, n))


@task
def deploy():
    """ Fabric script that creates and distributes an archive """
    file_name = do_pack()
    if file_name is None:
        return False
    return do_deploy(file_name)


@task
def do_deploy(archive_path):
    """Fabric script that distributes an archive to web servers"""
    try:
        if not os.path.exists(archive_path):
            return False
        with_ext = archive_path.split("/")[-1]
        without_ext = archive_path.split("/")[-1].split(".")[0]
        pth = "/data/web_static/releases/"
        put(archive_path, "/tmp/")
        run("sudo mkdir -p " + pth + without_ext)
        run("sudo tar -xzf /tmp/{} -C {}{}/".format(with_ext, pth, without_ext))
        run("sudo rm /tmp/{}".format(with_ext))
        run("sudo mv {1}{0}/web_static/* {1}{0}/".format(without_ext, pth))
        run("sudo rm -rf {}{}/web_static".format(pth, without_ext))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {}{}/ /data/web_static/current".format(pth, without_ext))
        return True
    except Exception:
        return False


@runs_once
def do_pack():
    """generates a .tgz archive from web_static"""
    datestr = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = "versions/web_static_{}.tgz".format(datestr)
    local("sudo mkdir -p versions")
    if local("sudo tar -cvzf {} web_static/".format(file_name)).succeeded:
        return file_name
    return None
