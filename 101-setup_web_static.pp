# Install Nginx package
exec { 'install_nginx':
  provider => shell,
  command  => 'sudo apt update ; sudo apt install -y nginx',
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
}

# Create a symbolic link
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test/',
  force  => true,
}

# Set ownership
file { '/data':
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
}

# Nginx configuration
file { '/etc/nginx/sites-available/default':
  content =>  '
server {
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
  notify  => Service['nginx'],
}

# restart nginx server
service { 'nginx':
  ensure  => 'running',
  enable  => true,
  require => File['/etc/nginx/sites-available/default'],
}
