#!/usr/bin/python3
""" Fabric script that generates a .tgz archive """
from fabric.decorators import task
from fabric.api import local
from datetime import datetime


@task
def do_pack():
    """generates a .tgz archive from the contents of the web_static folder"""
    try:
        # Create a timestamp for the archive name
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Define the name of the archive
        archive_name = "web_static_{}.tgz".format(timestamp)
        
        # Create the folder versions if it doesn't exist
        local("mkdir -p versions")
        
        # Compress the contents of the web_static folder into the archive
        local("tar -cvzf versions/{} web_static".format(archive_name))
        
        # Return the path to the generated archive
        return "versions/{}".format(archive_name)
    
    except Exception as e:
        print("Error:", e)
        return None


if __name__ == "__main__":
    do_pack()

