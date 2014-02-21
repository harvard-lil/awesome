# Installation on an EC2, Ubuntu instance

## Update apt-get

    sudo apt-get update

## Install essential build tools (gcc and make and ...)

    apt-get install build-essential

## Instsall pip:

    sudo apt-get install python-pip


## Install Django:

    sudo pip install Django

## Install required libraries

    sudo pip install requirements.txt

If python-msyqldb choke, or if python-lxml chokes, install with apt-get

    sudo apt-get install python-mysqldb
    sudo apt-get install python-lxml


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

    create database awesome CHARACTER SET utf8;
    grant all on awesome.* to someusername@'localhost' identified by 'somepass';


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


### Load first South migration

Awesome Box uses South to manage database changes. After the syncdb command, you'll need to apply existing migrations

    python manage.py migrate awesome

### Load some test data

If you're working on the Awesome Box codebase, you might want to get started by loading a test library and a test branch

    python manage.py loaddata awesome/tests/fixtures/org_plus_branch.json

Your login will be test-library with the password of pass


### Awesome will sometimes write to a log. Create it and give it perms:

    sudo touch /tmp/awesome.log
    sudo chmod 777 /tmp/awesome.log