# Install Nginx package
exec { 'update':
  provider => shell,
  command  => 'sudo apt update',
  before   => Exec['install_nginx'],
}

# Install Nginx package
exec { 'install_nginx':
  provider => shell,
  command  => 'sudo apt install -y nginx',
  before   => Exec['create test directory'],
}

exec { 'create test directory':
  provider => shell,
  command  => 'sudo mkdir -p /data/web_static/releases/test',
  before   => Exec['create shared directory']
}

exec { 'create shared directory':
  provider => shell,
  command  => 'sudo mkdir -p /data/web_static/shared',
  before   => Exec['set_ownership']
}

# Create a fake HTML file
exec { 'create html':
  provider => shell,
  command  => 'echo "Hello World!" | sudo tee /data/web_static/releases/test/index.html',
  before   => Exec['create link']
}

# Create a symbolic link
exec { 'create link':
  provider => shell,
  command  => 'sudo ln -sf /data/web_static/releases/test/ /data/web_static/current',
  before   => Exec['configuration'],
}

# Nginx configuration
exec { 'configuration':
  provider => shell,
  command  => 'echo "server {
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
  }" | sudo tee /etc/nginx/sites-available/default',
  before   => Exec['restart nginx']
}

# Restart nginx server only when necessary
exec {'restart nginx':
  provider => shell,
  command  => 'sudo service nginx restart',
}

# give ownership
file {'/data/':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
}
