# Install Nginx package
exec { 'install_nginx':
  command => 'sudo apt update && sudo apt install -y nginx',
}

# Set ownership first
exec { 'set_ownership':
  command => 'sudo chown -R ubuntu:ubuntu /data/',
  require => [
    File['/data/web_static/releases/test'],
    File['/data/web_static/shared'],
  ],
}

# Create directories if they don't exist
file { '/data/web_static/releases/test':
  ensure  => 'directory',
  recurse => true,
}

file { '/data/web_static/shared':
  ensure => 'directory',
}

# Create a fake HTML file
file { '/data/web_static/releases/test/index.html':
  content => 'Hello World!',
  require => File['/data/web_static/releases/test'],
}

# Create a symbolic link
file { '/data/web_static/current':
  ensure  => 'link',
  target  => '/data/web_static/releases/test/',
  force   => true,
  require => [
    File['/data/web_static/releases/test/index.html'],
    Exec['set_ownership'],
  ],
}

# Nginx configuration
file { '/etc/nginx/sites-available/default':
  ensure  => 'file',
  content => 'server {
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
  }',
  require => Exec['install_nginx'],
}

# Restart nginx server only when necessary
service { 'nginx':
  ensure    => 'running',
  enable    => true,
  subscribe => File['/etc/nginx/sites-available/default'],
  provider  => systemd,
}

