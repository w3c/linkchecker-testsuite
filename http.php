<?php
$codes = array(
    "300" => "Multiple Choices",
    "301" => "Moved Permanently",
    "302" => "Found",
    "307" => "Temporary Redirect",
    "400" => "Bad Request",
    "401" => "Unauthorized",
    "402" => "Payment Required",
    "403" => "Forbidden",
    "404" => "Not Found",
    "405" => "Method Not Allowed",
    "406" => "Not Acceptable",
    "407" => "Proxy Authentication Required",
    "408" => "Request Time-out",
    "409" => "Conflict",
    "410" => "Gone",
    "411" => "Length Required",
    "412" => "Precondition Failed",
    "413" => "Request Entity Too Large",
    "414" => "Request-URI Too Large",
    "415" => "Unsupported Media Type",
    "416" => "Requested range not satisfiable",
    "417" => "Expectation Failed",
    "500" => "Internal Server Error",
    "501" => "Not Implemented",
    "502" => "Bad Gateway",
    "503" => "Service Unavailable",
    "504" => "Gateway Time-out",
    "505" => "HTTP Version not supported"
    );
    
// we only want to return a specific response code if the
// requested parameter matches what we know:
$code = NULL;
if ($_GET['code'] != '') {
    if(isset($codes[$_GET['code']])) {
        $code = $_GET['code'];
        header("HTTP/1.0 $code $codes[$code]");
    }
}
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="en">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<title>untitled</title>
	<meta name="author" content="olivier Thereaux">
</head>
<body>
<p><?php echo $code, " ", $codes[$code]; ?>
</body>
</html>
