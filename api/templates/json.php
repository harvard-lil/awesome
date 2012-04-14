<?php
header('Content-type: application/json');

// Get our results from out controller
$results = $this->get('results');

//Start building our response
$response = array();
$response['num_found'] = $results['hits']['total'];

$docs = array();

// Build the response to use our preferred vocab
foreach ($results['hits']['hits'] as $result) {
    $doc = array();
    if (!empty($result['_source']['title'])) {
        $doc['title'] = $result['_source']['title'];
    }
    if (!empty($result['_source']['creator'])) {
        $doc['creator'] = $result['_source']['creator'];
    }
    if (!empty($result['_source']['isbn'])) {
        $doc['isbn'] = $result['_source']['isbn'];
    }
    if (!empty($result['_source']['hollis_id'])) {
        $doc['hollis_id'] = $result['_source']['hollis_id'];
    }
    if (!empty($result['_source']['checked_in'])) {
        $doc['checked_in'] = $result['_source']['checked_in'];
    }
    array_push($docs, $doc);
}

$response['docs'] = $docs;

echo json_encode($response);
?>