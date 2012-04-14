<?php

// Load F3
$f3 = require_once dirname(__FILE__) . '/lib/f3/base.php';

// Comment out our debug when in prod
$f3->set('DEBUG',3);

// Load our config file
$f3->config(dirname(__FILE__) . '/etc/master.cfg');

// Let F3 load our other things
$autoload_path = "{$f3->get('AWESOME_HOME')}/api/classes/;";
$f3->set('AUTOLOAD', $autoload_path);

$f3->route('GET /api/item/@item','Item->get_single');
$f3->route('GET /api/item/search','Item->search');
$f3->run();

?>