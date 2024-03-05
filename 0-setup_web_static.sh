#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of web_static.
sudo apt-get update
sudo apt-get -y install nginx
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
echo '<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>' > /data/web_static/releases/test/index.html
ln -sfn /data/web_static/releases/test /data/web_static/current
chown -R ubuntu:ubuntu /data/
new="server_name _;\n\n\tlocation \/hbnb_static {\n\t\talias \/data\/web_static\/current\/;\n\t}"
sudo sed -i "s/server_name _;/$new/" /etc/nginx/sites-enabled/default
sudo service nginx restart
