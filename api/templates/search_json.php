<?php
header('Content-type: application/json');

// Get our results from our controller
$docs = $this->get('results');

//Start building our response
$response = array();
$response['num_found'] = count($docs);
$response['docs'] = $docs;

// Not much else to do. Dump it to the screen.
echo json_encode($response);
?>