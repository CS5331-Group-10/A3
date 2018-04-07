<html>
<body>
<h1>Server Side Code Injection</h1>
<?php

$page = $_GET['page'];
	echo "eval single quote:<br>";
	eval("echo '".$page."';");

	echo "<br><br>eval double quote:<br>";
	eval("echo \"".$page."\";");

?>

</body>
</html>
