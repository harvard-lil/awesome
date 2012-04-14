<?php  
$title = $_REQUEST['title'];
$author = $_REQUEST['author'];
$hollis = $_REQUEST['hollis'];

/* twitter settings */
require_once 'twitteroauth.php';
 
define("CONSUMER_KEY", "here");
define("CONSUMER_SECRET", "here");
define("OAUTH_TOKEN", "here");
define("OAUTH_SECRET", "here");
 
$connection = new TwitterOAuth(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_SECRET);
$content = $connection->get('account/verify_credentials');

//$connection->post('statuses/update', array('status' => 'post w/oauth'));

	
$hollis_link = 'http://discovery.lib.harvard.edu/?itemid=|library/m/aleph|'.$hollis;
 /* make a URL small */
$format = 'xml';
$version = '2.0.1';
$login = 'hallcheckouts';
$appkey = 'here';
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
	
?>