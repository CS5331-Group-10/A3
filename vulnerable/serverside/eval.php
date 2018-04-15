<html>
<body>
<h1>Server Side Code Injection</h1>
<?php

$page = $_GET['page'];


	echo "<br><br>Non-echo eval: ";
	$x = "fail";
	eval("\$x = $page;");
	echo "<br>".$x;
?>

</body>
</html>
