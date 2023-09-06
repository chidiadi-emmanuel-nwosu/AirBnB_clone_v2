#!/usr/bin/env bash
# script that sets up your web servers for the deployment of web_static

# Install Nginx if it not already installed
command -v &> /dev/null || {
	sudo apt update
	sudo apt install -y nginx
}

# Create the folders /data/web_static/releases/test/ if they don’t already exist
sudo mkdir -p /data/web_static/releases/test/

# Create the folder /data/web_static/shared/ if it doesn’t already exist
sudo mkdir -p /data/web_static/shared/

# Create a fake HTML file /data/web_static/releases/test/index.html
echo "Hello World!" | sudo tee /data/web_static/releases/test/index.html &> /dev/null

# Create a symbolic link /data/web_static/current
# linked to the /data/web_static/releases/test/ folder. 
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user AND group
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve the content of
# /data/web_static/current/ to hbnb_static
echo "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    root   /var/www/html;
    index  index.html index.htm index.nginx-debian.html;

    server_name _;

    add_header X-Served-By $HOSTNAME;

    location /redirect_me {
        return 301 https://www.youtube.com/watch?v=QH2-TGUlwu4;
    }

    error_page 404 /404.html;
    location /404 {
	root /etc/nginx/html;
	internal;      
    }

    location /hbnb_static {
        alias /data/web_static/current/;
    }
}" | sudo tee /etc/nginx/sites-available/default

# restart the Nginx server
sudo service nginx restart
