<?php
header('Content-type: application/json');

// Get our results from out controller
$results = $this->get('results');

// We don't need to do anything, just dump the document
echo json_encode($results['_source']);
?>