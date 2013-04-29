<?php
$filter = $_REQUEST['filter'];
$url = "http://hlsl10.law.harvard.edu/awesome/api/item/search?limit=5&filter=$filter&sort=last_modified%20desc";

$ch = curl_init();

curl_setopt($ch, CURLOPT_URL, $url);

curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);

curl_setopt($ch,CURLOPT_HTTPHEADER,array('Accept: application/json'));

$contents = curl_exec($ch);

curl_close ($ch);
        
$contents = json_decode($contents, true);

foreach($contents['docs'] as $item) {
  $creator = '';
  if($item['creator']) {
    $creator = ' by ' . $item['creator'];
  }
  echo"document.write('<p><a href=\"http://hollis.harvard.edu/?itemid=|library/m/aleph|".$item['hollis_id']."\">".$item['title']."</a>');";
  echo"document.write('".$creator."</p>');";
}
?>
