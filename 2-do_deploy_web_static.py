#!/usr/bin/python3
""" Fabric script that generates a .tgz archive """
from fabric.decorators import task
from fabric.api import *
from datetime import datetime
from os import path

env.user = 'ubuntu'
env.hosts = ['18.207.236.32', '52.201.228.254']

@task
def do_deploy(archive_path):
    """Distributes an archive to web servers"""
    if not path.exists(archive_path):
        return False

    try:
        put(archive_path, '/tmp')
        filename = archive_path.split('/')[-1]
        foldername = filename.split('.')[0]
        release_path = '/data/web_static/releases/' + foldername

        run('sudo mkdir -p {}'.format(release_path))
        run('sudo tar -xzf /tmp/{} -C {}'.format(filename, release_path))
        run('sudo rm /tmp/{}'.format(filename))
        run('sudo mv -f {}/web_static/* {}'.format(release_path, release_path))
        run('sudo rm -rf {}/web_static'.format(release_path))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s {} /data/web_static/current'.format(release_path))

        return True
    except Exception as e:
        print(e)
        return False
