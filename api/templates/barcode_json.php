<?php
header('Content-type: application/json');

// Get our results from out controller
$contents = $this->get('contents');

echo $contents;
?>