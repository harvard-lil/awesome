<?php
$isbn13OrEAN = $_REQUEST['isbn'];

$isbn10 = "";
if ($isbn13OrEAN==null)
{
    echo $isbn13OrEAN;    
    return false;
}
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
        
echo $isbn10;
?>