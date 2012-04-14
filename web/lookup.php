<?php

$barcode = $_REQUEST['barcode'];

$url = 'http://webservices.lib.harvard.edu/rest/classic/barcode/cite/' . $barcode;

$ch = curl_init();

curl_setopt($ch, CURLOPT_URL, $url);

//curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);

curl_setopt($ch,CURLOPT_HTTPHEADER,array('Accept: application/json'));

$contents = curl_exec ($ch);
	
curl_close ($ch);
	
return $contents;


?>