<?php

// Load F3
$f3 = require_once dirname(__FILE__) . '/lib/f3/base.php';

// Comment out our debug when in prod
$f3->set('DEBUG',3);

// Load our config file
$f3->config(dirname(__FILE__) . '/etc/master.cfg');

// Let F3 load our other things
$autoload_path = "{$f3->get('AWESOME_HOME')}/api/classes/; {$f3->get('AWESOME_HOME')}/lib/;";
$f3->set('AUTOLOAD', $autoload_path);

// API business
$f3->route('GET /api/item/@item_id', 'Item->get_single');
$f3->route('POST /api/item', 'Item->create');
$f3->route('GET /api/item', 'Item->create');
$f3->route('GET /api/item/search', 'Item->search');
$f3->route('GET /api/item/most-awesome', 'Item->most_awesome');
$f3->route('GET /api/item/recently-awesome', 'Item->recently_awesome');

// Service business
$f3->route('POST /api/services/tweet', 'Services->tweet_new_item');
$f3->route('GET /api/services/barcode-lookup', 'Services->barcode_lookup');
$f3->route('GET /api/services/isbn-lookup', 'Services->isbn_lookup');

// Web business
$f3->route('GET /', 'web/index.html');

$f3->run();

?>
