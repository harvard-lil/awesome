<?php

class Services extends F3instance {

    function tweet_new_item() {
        // Tweet a checkin
        $title = $_REQUEST['title'];
        $creator = $_REQUEST['creator'];
        $hollis_id = $_REQUEST['hollis_id'];

        $consumer_key = $this->get('CONSUMER_KEY');

        $connection = new TwitterOAuth($this->get('TWITTER_CONSUMER_KEY'), $this->get('TWITTER_CONSUMER_SECRET'), $this->get('TWITTER_OAUTH_TOKEN'),  $this->get('TWITTER_OAUTH_SECRET'));

        $content = $connection->get('account/verify_credentials');

        $hollis_link = 'http://discovery.lib.harvard.edu/?itemid=|library/m/aleph|'.$hollis_id;
         /* make a URL small */
        $format = 'xml';
        $version = '2.0.1';
        $login = 'hallcheckouts';
        $appkey = $this->get('BITLY_KEY');

        //create the URL
        $bitly = 'http://api.bit.ly/shorten?version='.$version.'&longUrl='.urlencode($hollis_link).'&login='.$login.'&apiKey='.$appkey.'&format='.$format;

        //get the url
        //could also use cURL here
        $response = file_get_contents($bitly);

        //parse depending on desired format
        if(strtolower($format) == 'json')
        {
        	$json = @json_decode($response,true);
        	$short = $json['results'][$url]['shortUrl'];
        }
        else //xml
        {
        	$bitly_xml = simplexml_load_string($response);
        	$short = 'http://bit.ly/'.$bitly_xml->results->nodeKeyVal->hash;
        }

        $message = $title;
        //$creator_pieces = explode(",", $creator);
        //$creator = $creator_pieces[1]." ".$creator_pieces[0];
        if($creator!= ' ')
        	$message.= " by $creator";
        $message = mb_substr($message, 0, 119);

        $message .= ' ';

        $message .= $short;
        echo $message;

        $connection->post('statuses/update', array('status' => $message));
    }
    
    function barcode_lookup () {
        // Given a barcode, get the item details
        $barcode = $_REQUEST['barcode'];
        $empty = array();

        $url = 'http://webservices.lib.harvard.edu/rest/classic/barcode/cite/' . $barcode;

        $ch = curl_init();

        curl_setopt($ch, CURLOPT_URL, $url);

        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);

        curl_setopt($ch,CURLOPT_HTTPHEADER,array('Accept: application/json'));

        $contents = curl_exec($ch);

        curl_close ($ch);
        
        if($contents) {
        
          $contents = json_decode($contents);
  
          $contents = $contents->rlistFormat->hollis;
          
          // Get HOLLIS ID and grab the holding library
          $hollis = substr($contents->hollisId, 0, 9);
          $hollis_length = strlen($hollis);
          if($hollis_length < 9) {
            $loop = 9 - $hollis_length;
            for($j=0; $j<$loop; $j++){
              $hollis = '0'.$hollis;
            }
          }
          
          $format_url = "http://librarylab.law.harvard.edu/platform/v0.03/api/item/?filter=id_inst:$hollis";
          
          $ch = curl_init();
  
          curl_setopt($ch, CURLOPT_URL, $format_url);
  
          curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
  
          $format = curl_exec ($ch);
          
          $format = json_decode($format, true);
          
          $contents->format = '';
          if(count($format['docs']) > 0) {
            $format = $format['docs'][0]['format'];
            $format = str_replace('/', '', $format);
            $format = str_replace(' ', '', $format);
            $contents->format = strtolower($format);
          }
    
          curl_close ($ch);
          
          $contents->poster = '';
          if($contents->format == 'videofilm') {
          
            $title = urlencode($contents->title);
            $poster_url = "http://api.rottentomatoes.com/api/public/v1.0/movies.json?apikey=dte98e86zfhyvryb8r8epcp3&q=$title&page_limit=1";
            
            $ch = curl_init();
    
            curl_setopt($ch, CURLOPT_URL, $poster_url);
    
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    
            $poster = curl_exec ($ch);
            
            $poster = json_decode($poster, true);
            
            if(count($poster['movies']) > 0) {
              $poster = (string) $poster['movies'][0]['posters']['profile'];
              $contents->poster = $poster;
            }
      
            curl_close ($ch);
          }
  
          $contents->barcode = $barcode;
          $contents->hollis = $hollis;
          $url = "http://hollis-coda.hul.harvard.edu/availability.ashx?hreciid=|library%2fm%2faleph|$hollis&output=xml";

          $ch = curl_init();
  
          curl_setopt($ch, CURLOPT_URL, $url);
  
          curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
  
          $libraries = curl_exec ($ch);
    
          curl_close ($ch);

          if($libraries) {
    
            $xml = simplexml_load_string($libraries);
    
            $library = $xml->xpath("//xserverrawdata[@barcode='$barcode']/@sub-library"); 
            $library = (string) $library[0]['sub-library'];
    
            $contents->library = $library;
            $contents = json_encode($contents);
            
            $this->set('contents', $contents);
            
            $path_to_template = 'api/templates/barcode_json.php';
            echo $this->render($path_to_template);
          }
          else $this->no_results();
        }
        else $this->no_results();
        
        //print json_encode($contents);
    }
    
    function isbn_lookup () {
        // Given an isbn, get the item details
        $isbn = $_REQUEST['barcode'];
        $data = array();
        $data['barcode'] = $isbn;

        $url = 'http://openlibrary.org/api/books?bibkeys=ISBN:' . $isbn . '&jscmd=data&format=json';

        $ch = curl_init();

        curl_setopt($ch, CURLOPT_URL, $url);

        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);

        $contents = curl_exec($ch);

        curl_close ($ch);
        
        $contents = json_decode($contents, true);
        
        if($contents && $contents['ISBN:' . $isbn]) {
        
          $contents = $contents['ISBN:' . $isbn];
          
          //print_r($contents);
          
          $data['hollis'] = $contents['identifiers']['openlibrary'][0];
          $data['isbn'] = '';
          if(isset($contents['identifiers']['isbn_13']))
            $data['isbn'] = $contents['identifiers']['isbn_13'];
          if(isset($contents['identifiers']['isbn_10']))
            $data['isbn'] = $contents['identifiers']['isbn_10'];
          if(isset($contents['title']))
            $data['title'] = $contents['title'];
          if(isset($contents['authors'])) {
            $data['creator'] = $contents['authors'][0]['name'];
          }
          $data['library'] = '';
          $data['format'] = 'book';
          $data['poster'] = '';
          
          //print_r($data);
          
          $data = json_encode($data);
          
          $this->set('contents', $data);
          
          $path_to_template = 'api/templates/barcode_json.php';
          echo $this->render($path_to_template);
        }
        else $this->no_results();
        
        //print json_encode($contents);
    }
    
    function wc_lookup () {
        // Given an isbn, get the item details
        $barcode = $_REQUEST['barcode'];
        $data = array();
        $data['barcode'] = $barcode;
        $worldcat_key = $this->get('WORLDCAT_KEY');
        
        $url = "http://www.worldcat.org/webservices/catalog/search/sru?query=srw.sn%3D%22$barcode&wskey=$worldcat_key&servicelevel=full";
        
        //echo $url;

        $ch = curl_init();

        curl_setopt($ch, CURLOPT_URL, $url);

        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);

        $contents = curl_exec($ch);

        curl_close ($ch);
        
        $pxml = new SimpleXMLElement($contents);
        $pxml = $pxml->records->record;
        
        $data['isbn'] = '';
        $data['creator'] = '';
        $data['library'] = '';
        $data['format'] = 'book';
        $data['poster'] = '';
        
        $tag245 = $pxml->xpath("//*[@tag='245']");
        $title = $tag245[0]->subfield[0];
        $data['title'] = (string) $title;
        
        $tag001 = $pxml->xpath("//*[@tag='001']");
        $data['hollis'] = "WC" . (string) $tag001[0];
        
        $tag300 = $pxml->xpath("//*[@tag='300']");
        
        foreach($tag300[0]->subfield as $format) {
          if (strpos($format,'videodisc') !== false) {
            $data['format'] = 'videofilm';
          }
          if (strpos($format,'sound disc') !== false) {
            $data['format'] = 'soundrecording';
          }
        }
        
        $tag020 = $pxml->xpath("//*[@tag='020']");
        if($tag020) {
          $isbn = (string) $tag020[0]->subfield[0];
          $isbn = explode(" ", $isbn);
          $isbn = $isbn[0];
          $data['isbn'] = $isbn;
        }
          
        $data = json_encode($data);
          
        $this->set('contents', $data);
          
        $path_to_template = 'api/templates/barcode_json.php';
        echo $this->render($path_to_template);
    }
    
    function no_results() {
      $empty = array();
      $contents = json_encode($empty);
            
      $this->set('contents', $contents);
            
      $path_to_template = 'api/templates/barcode_json.php';
      echo $this->render($path_to_template);
    }
}
?>