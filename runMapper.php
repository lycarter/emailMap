<html>
<head>
        <title>Moira List Mapper</title>
        <link rel="stylesheet" href="../parent.css">
        <link rel="stylesheet" href="../page.css">
        <link href="../lightbox/css/lightbox.css" rel="stylesheet" />
        <link rel="icon" type="image/png" href="../favicon.png" />
        <link href='http://fonts.googleapis.com/css?family=Roboto:400,700,500' rel='stylesheet' type='text/css'>
        <link href='http://fonts.googleapis.com/css?family=Noto+Sans' rel='stylesheet' type='text/css'>
</head>

<body>
<?php

//$test2 = exec("pwd");

//$test = exec("blanche cao-cao-cao-cao-cao");

//echo "$test2";
//echo "$test";

$ln = escapeshellarg("{$_POST["name"]}");

$result = exec('python mapper.py '.$ln.' -o '.$ln.'.pdf');

echo '<h1>Done mapping '.$ln.'!</h1>';

$filename = "{$_POST["name"]}.pdf";

echo $filename;

if (file_exists($filename)) {
    header("Pragma: public");
    header("Expires: 0");
    header("Cache-Control: must-revalidate, post-check=0, pre-check=0");
    header("Content-Type: application/octet-stream");
    header("Content-Disposition: attachment;filename=".basename($filename));
    header("Content-Transfer-Encoding: binary");
    header("Content-Length: ".filesize($filename));
    ob_clean();
    flush();
    readfile($filename);
}

$result = exec('rm '.$ln.'.pdf');

?>

<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-57039341-1', 'auto');
  ga('send', 'pageview');

</script>
<script src="http://victorhh.com/antoniojs/antonio.js"></script>
</body>


</html>

