<?php

class Item extends F3instance {

    function get_single() {
        // Given an id, get the items details
        print_r($this->get('PARAMS'));
        echo "item id is: " . $this->get('PARAMS.item');
    }

    function search() {
        // Do some searching on things coming in from the filter URL param

        /* Start building the query object. We hope to end up with something like:
        $reqeust = '{
            "from" : 0,
            "size": 10,
            "query" : {
                "terms" : {
                    "creator" : [ "card" ]
                }
            },
            sort: {
                title: {
                    order: "desc"
                }
            }
        }';
        */
        $request = array();


        // Users can query by specifying an url param like &filter=title:ender
        // TODO: We should allow for multiple filters.
        $key_and_val = explode(":", $this->get('GET.filter'));
        if (count($key_and_val) == 2 and !empty($key_and_val[0]) and !empty($key_and_val[1])) {
            $request['query']['terms'] = array($key_and_val[0] => array($key_and_val[1]));
        } else {
            $request['query'] = array("match_all" => new stdClass);
        }
        
        // start parameter (elasticsearch calls this 'from')
        $incoming_start = $this->get('GET.start');
        if (!empty($incoming_start)) {
            $request['from'] = $this->get('GET.start');
        }
        
        // limit parameter (elasticsearch calls this 'size')
        $incoming_limit = $this->get('GET.limit');
        if (!empty($incoming_limit)) {
            $request['size'] = $this->get('GET.limit');
        }
        
        // sort parameter
        $incoming_sort = $this->get('GET.sort');
        $sort_field_and_dir = explode(" ", $this->get('GET.sort'));
        if (count($sort_field_and_dir) == 2) {
            $request['sort'] = array($sort_field_and_dir[0] => array('order' => $sort_field_and_dir[1]));
        }
        
        $jsoned_request = json_encode($request);
        
        $url = $this->get('ELASTICSEARCH_URL') . '_search';
        $ch = curl_init();
        $method = "GET";    

        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, strtoupper($method));
        curl_setopt($ch, CURLOPT_POSTFIELDS, $jsoned_request);

        $results = curl_exec($ch);
        curl_close($ch);
        
        $this->set('results', json_decode($results, true));
        $path_to_template = 'api/templates/json.php';
        echo $this->render($path_to_template);
    }

    function create_item() {
        // create and item
        echo "junk is: " . $this->get('GET.junk');
    }
}
?>