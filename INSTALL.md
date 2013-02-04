# Installation on an EC2, Ubuntu instance

## Update apt-get

    sudo apt-get update

## Install essential build tools (gcc and make and ...)

    apt-get install build-essential

## Instsall pip:

    sudo apt-get install python-pip


## Install Django:

    sudo pip install Django


## Install Apache and related bits

    sudo apt-get install apache2

Install the Apache mod_wsgi module:

    sudo apt-get install libapache2-mod-wsgi


## Install nginx

    sudo apt-get install nginx

## Install git

    sudo apt-get install git


## Install MySQL

    sudo apt-get install mysql-server mysql-client


## Create a database for awesome

    create database awesome;
    grant all on awesome.* to someusername@'localhost' identified by 'somepass';


## Install Python/Django pieces

    sudo apt-get install python-mysqldb
    sudo pip python-twitter
    sudo apt-get install python-lxml
    sudo pip install django-templatetag-handlebars
    sudo pip install django-tastypie


## Install the Awesome codebase

    cd /srv; sudo mkdir www;
    sudo git clone https://github.com/harvard-lil/awesome.git
    cd awesome

For our testing version, let's check out an alternate branch. Prod machines will use master.
    git checkout -b django-based origin/django-based

You'll need to configure two settings files in the Awesome codebase.

    cd /srv/www/awesome/lil; sudo cp settings.example.py settings.py

edit settings.py, installing the values of your database, secret key, and so on

    cd awesome; sudo cp local_settings.example.py local_settings.py

edit local_settings.py, installing your keys.


### Setup the Awesome DB

    cd /srv/www/awesome/lil; sudo python manage.py syncdb


### Awesome will sometimes write to a log. Create it and give it perms:

    sudo touch /tmp/awesome.log
    sudo chmod 777 /tmp/awesome.log 

## Configure Apache/WSGI

Create /etc/apache2/sites-available/awesome with these contents


	<VirtualHost *:8200>
 
	    ServerName awesome.djangoserver
	    DocumentRoot /srv/www/awesome/lil
 
	    <Directory /srv/www/awesome/lil>
	        Order allow,deny
	        Allow from all
	    </Directory>
 
	    WSGIDaemonProcess shelfio.djangoserver processes=2 threads=15 display-name=%{GROUP}
	    WSGIProcessGroup shelfio.djangoserver
 
	    WSGIScriptAlias / /srv/www/awesome/lil/apache/django.wsgi
 
	</VirtualHost>



Enable the site using a symlink:

    cd ../sites-enabled; sudo ln -s ../sites-available/awesome awesome;

You probably also want to disable the default:

    sudo rm 000-default


Verify that your wsgi config looks right:

    cat /srv/www/awesome/lil/apache/django.wsgi

Edit apache's startup port. It was 80, but nginx will take traffic on 80. Set it to 8200:

    etc/apache2$ sudo vi ports.conf


Apache should be set now.

## Configure nginx

    cd /etc/nginx;

Create a new file at /etc/nginx/sites-available/awesome with this content:

	upstream awesomeapache {
	        #The upstream apache server. You can have many of these and weight them accordingly,
	        server 127.0.0.1:8200 weight=1 fail_timeout=120s;
	}


	server {
	        listen 80;
	        server_name awesomebox.io www.awesomebox.io;
	        #root /var/www/testdir;

	        # Set the real IP.
	        proxy_set_header X-Real-IP  $remote_addr;

	        # Set the hostname
	        proxy_set_header Host $host;

	        #Set the forwarded-for header.
	        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

	        location / {
	                proxy_pass http://awesomeapache;
	                #auth_basic "Restricted";
	                #auth_basic_user_file /var/www/testdir/.htpasswd;
	        }

	        location /static/ {
	            autoindex on;
	            root   /srv/www/awesome/lil/;
	         }

	        location /awesome/ {
	            autoindex on;
	            root   /srv/www/;
	         }

	        # No access to .htaccess files.
	        location ~ /\.ht {
	                deny  all;
	        }
	}

Enable the site:

	cd ../sites-enabled; sudo ln -s ../sites-available/awesome awesome

You probably want to remove the default:

	sudo rm default


Things should be configured.

## Start things up

	sudo /etc/init.d/apache2 restart
	sudo /etc/init.d/nginx restart