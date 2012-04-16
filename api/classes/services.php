<?php

class Services extends F3instance {

    function tweet_new_item() {
        // Tweet a checkin
        $title = $_REQUEST['title'];
        $author = $_REQUEST['author'];
        $hollis = $_REQUEST['hollis'];

        $consumer_key = $this->get('CONSUMER_KEY');

        $connection = new TwitterOAuth($this->get('TWITTER_CONSUMER_KEY'), $this->get('TWITTER_CONSUMER_SECRET'), $this->get('TWITTER_OAUTH_TOKEN'),  $this->get('TWITTER_OAUTH_SECRET'));

        $content = $connection->get('account/verify_credentials');

        $hollis_link = 'http://discovery.lib.harvard.edu/?itemid=|library/m/aleph|'.$hollis;
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
        $author_pieces = explode(",", $author);
        $author = $author_pieces[1]." ".$author_pieces[0];
        if($author != ' ')
        	$message.= " by $author";
        $message = mb_substr($message, 0, 119);

        $message .= ' ';

        $message .= $short;
        echo $message;

        $connection->post('statuses/update', array('status' => $message));
    }
    
    function barcode_lookup () {
        // Given a barcode, get the item details
        $barcode = $_REQUEST['barcode'];

        $url = 'http://webservices.lib.harvard.edu/rest/classic/barcode/cite/' . $barcode;

        $ch = curl_init();

        curl_setopt($ch, CURLOPT_URL, $url);

        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);

        curl_setopt($ch,CURLOPT_HTTPHEADER,array('Accept: application/json'));

        $contents = curl_exec($ch);

        curl_close ($ch);
        
        $this->set('contents', $contents);
        $path_to_template = 'api/templates/barcode_json.php';
        echo $this->render($path_to_template);

        //print json_encode($contents);
    }
}
?>