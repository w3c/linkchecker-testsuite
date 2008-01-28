<?php header("Content-Location: http://www.w3.org/QA/2008/01/");?>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="en">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<title>Link Checker Test - base-2</title>
	<meta name="author" content="olivier Thereaux">
</head>
<body>
<div id="test">
    <p> <span id="test-id">base-2</span>: 
        test for base URI with Content-Location HTTP Header. The document has a relative link. 
        HREF of the link should be calculated with the BASE URI considered.
    </p>
    <p id="expected" class="200 OK">EXPECTED: 
        relative link goes 200 if OK - link checker finds no error. If the link checker is not
        respecting the Content-Location HTTP Header, it will find a 404 Not Found when following the link.
    </p>
</div>
<p><a href="are_you_mobileok.html">Are You MobileOk?</a></p>
</body>
</html>
