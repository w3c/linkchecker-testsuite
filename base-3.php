<?php header("Content-Location: http://www.w3.org/QA/Tools/");?>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="en">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<title>Link Checker Test - base-3</title>
	<meta name="author" content="olivier Thereaux">
	<base href="http://qa-dev.w3.org/link-testsuite/trap/">
</head>
<body>
<div id="test">
    <p> <span id="test-id">base-3</span>: 
        test for base URI with Content-Location HTTP Header. The document has a relative link. 
        HREF of the link should be calculated with the BASE URI considered.
    </p>
    <p id="expected" class="200 OK">EXPECTED: 
        200 OK. The BASE href has precedence over the other mechanisms.
        If the Content-Location is followed, the link checker would find a 404. This is incorrect.
        If the current URI of the document is taken as a base, 
        the link checker would find a 403. This is incorrect.
    </p>
</div>
<p><a href="http.php?code=403">this should return a 200 OK</a></p>
</body>
</html>
