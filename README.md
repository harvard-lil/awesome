#Awesome Box

The Awesome Box is an alternate returns box at your library. If you checked out an item and you thought it was awesome, for whatever reason, you return it to the Awesome Box instead of the regular returns box.

This git repository contains the webapp used to receive and share things that have been aweseomed.

## Installation

### Twitter and bitly

The Awesome Box tweets items that have been awesomed. You'll need to sign up for a [Twitter](http://twitter.com) account and a [bitly](https://bitly.com/) account. We'll come back to Twitter and bitly when we're configuring the Awesome Box installation.

### elasticsearch

The Awesome Box uses elasticsearch to index incoming items. It's used as the datastore. 

Download it and install it:

    http://www.elasticsearch.org/

### PHP and the web server

Awesome Box is written in PHP. PHP 5.3 or later is recommended.

Serving up ShelfLife in [Apache](http://httpd.apache.org/) is probably the easiest way to get started. ShelfLife relies on rewrite rules in .htaccess. Be sure you're allowing for .htaccess in your httpd configuration and that you have mod_php and mod_rewrite installed.

### Getting the source

Head on over to your web document root (in my Apache instance, I use /var/www/html) and use the git clone command to get the latest version of ShelfLife:

    cd /var/www/html
    git clone https://github.com/harvard-lil/awesome.git

### Configure

You should now have Awesome Box installed. Let's configure it.

    cd /var/www/html/awesome/etc
    cp master.cfg.example to master.cfg

Edit the master.cfg config file with the keys and paths that we've created in the instructions above.

### Success

If things are working correctly you should be able to add an item at http://yourhost/awesome/scan.html and see it at http://yourhost/awesome/