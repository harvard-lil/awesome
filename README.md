#Awesome Box

The Awesome Box is an alternate returns box at your library. If you checked out an item and you thought it was awesome, for whatever reason, you return it to the Awesome Box instead of the regular returns box.

This git repository contains the webapp used to receive and share things that have been aweseomed.

## Installation

### Twitter, bitly, and WorldCat accounts

The Awesome Box tweets items that have been awesomed. You'll need to sign up for a [Twitter](http://twitter.com) account and a [bitly](https://bitly.com/) account.

The Awesome Box uses to the [WorldCat API](http://oclc.org/developer/documentation/worldcat-basic-api/using-api) to retrieve metadata from barcodes. Sign up for a [WorldCat API key](http://oclc.org/developer/documentation/worldcat-basic-api/using-api).

The Awesome Box tracks visits to the site using [Google Analytics](http://www.google.com/analytics/). Sign up for a [Google Analytics](http://www.google.com/analytics/) account

We'll come back to [Twitter](http://twitter.com), [bitly](https://bitly.com/), [WorldCat API](http://oclc.org/developer/documentation/worldcat-basic-api/using-api), [Google Analytics](http://www.google.com/analytics/) when we're configuring the Awesome Box installation.

### elasticsearch

The Awesome Box uses elasticsearch to index incoming items. It's used as the datastore. 

Download it and install it:

    http://www.elasticsearch.org/

### PHP and the web server

Awesome Box is written in PHP. PHP 5.3 or later is recommended.

Serving up ShelfLife in [Apache](http://httpd.apache.org/) is probably the easiest way to get started. ShelfLife relies on rewrite rules in .htaccess. Be sure you're allowing for .htaccess in your httpd configuration and that you have mod_php and mod_rewrite installed.

### Getting the source

Head on over to your web document root (in our Apache instance, we use /var/www/html) and use the git clone command to get the latest version of ShelfLife:

    cd /var/www/html
    git clone https://github.com/harvard-lil/awesome.git

### Configure

You should now have Awesome Box installed. Let's configure it.

    cd /var/www/html/awesome/etc
    cp master.ini.example to master.ini

Edit the master.cfg config file with the keys and paths that we've created in the instructions above.

### Setup .htaccess

We use a .htaccess to route requests in the Awesome Box interface. An example is supplied, just copy it.

    cd /var/www/html/awesome/
    cp .htaccess.example .htaccess

### Success

If things are working correctly you should be able to add an item at http://yourhost/awesome/scan.html and see it at http://yourhost/awesome/

## License

Dual licensed under the MIT license (below) and [GPL license](http://www.gnu.org/licenses/gpl-3.0.html).

<small>
MIT License

Copyright (c) 2012 The Harvard Library Innovation Lab

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
</small>
