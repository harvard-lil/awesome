<?php

class Item extends F3instance {

    function get_single() {
        // Given an id, get the items details
        // TODO: Some request and ES response validation

        $url = $this->get('ELASTICSEARCH_URL') . $this->get('PARAMS.item_id');
        $ch = curl_init();
        $method = "GET";

        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, strtoupper($method));

        $results = curl_exec($ch);
        curl_close($ch);
        
        $this->set('results', json_decode($results, true));
        $path_to_template = 'api/templates/direct_access_json.php';
        echo $this->render($path_to_template);
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
            }s
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
        $path_to_template = 'api/templates/search_json.php';
        echo $this->render($path_to_template);
    }

    function create() {
        // create an item
        // TODO: We're doing no validation here. this is bad.
        
        $new_item = array();
        
        $incoming_title = $this->get('POST.title');
        if(!empty($incoming_title)) {
             $new_item['title'] = $incoming_title;
        }
        $incoming_creator = $this->get('POST.creator');
        if(!empty($incoming_creator)) {
             $new_item['creator'] = $incoming_creator;
        }
        $incoming_isbn = $this->get('POST.isbn');
        if(!empty($incoming_isbn)) {
            $massaged_isbn = $this->convert_isbn($incoming_isbn);
            $new_item['isbn'] = $massaged_isbn;
        }
        $incoming_hollis_id = $this->get('POST.hollis_id');
        if(!empty($incoming_hollis_id)) {
             $new_item['hollis_id'] = $incoming_hollis_id;
        }
        
        $new_item['id'] = $this->gen_uuid();

        $jsoned_new_item = json_encode($new_item);
        
        $url = $this->get('ELASTICSEARCH_URL');
        $ch = curl_init();
        $method = "POST";

        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, strtoupper($method));
        curl_setopt($ch, CURLOPT_POSTFIELDS, $jsoned_new_item);

        $results = curl_exec($ch);
        curl_close($ch);
        
    }
    
    //////////////////////
    // Local heplers
    //////////////////////
    
    // Taken directly from http://stackoverflow.com/questions/2040240/php-function-to-generate-v4-uuid
    function gen_uuid() {
        return sprintf( '%04x%04x-%04x-%04x-%04x-%04x%04x%04x',
            // 32 bits for "time_low"
            mt_rand( 0, 0xffff ), mt_rand( 0, 0xffff ),

            // 16 bits for "time_mid"
            mt_rand( 0, 0xffff ),

            // 16 bits for "time_hi_and_version",
            // four most significant bits holds version number 4
            mt_rand( 0, 0x0fff ) | 0x4000,

            // 16 bits, 8 bits for "clk_seq_hi_res",
            // 8 bits for "clk_seq_low",
            // two most significant bits holds zero and one for variant DCE1.1
            mt_rand( 0, 0x3fff ) | 0x8000,

            // 48 bits for "node"
            mt_rand( 0, 0xffff ), mt_rand( 0, 0xffff ), mt_rand( 0, 0xffff )
        );
    }
    
    // If we get a 13 digit isbn, let's convert it to a 10er here
    function convert_isbn($isbn13OrEAN) {
        $isbn13OrEAN = str_replace(" ","",str_replace("-","",$isbn13OrEAN));
        $isbnLen=strlen($isbn13OrEAN);
        if ($isbnLen!=13)
        {
            //Invalid length
            echo $isbn13OrEAN;
            return false;
        }

        $isbn10 = substr($isbn13OrEAN,3,9);
        $sum = 0;
        $isbnLen=strlen($isbn10);

        for ($i = 0; $i < $isbnLen; $i++) 
        {
        	$current = substr($isbn10,$i,1);
            if($current<0||$current>9)
            {
                //Invalid ISBN
                echo $isbn13OrEAN;
                return false;
            }
            $sum+= $current*(10-$i);
        }
        $modulu = $sum%11;
        $checkDigit = 11 - $modulu;

        //if the checkDigit is 10 should be x
        if ($checkDigit==10)
            $isbn10 .= 'X';
        else if($checkDigit==11)
            $isbn10 .= '0';
        else
            $isbn10 .= $checkDigit;
            
        return $isbn10;
    }
}
?>