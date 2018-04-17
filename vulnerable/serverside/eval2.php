<html>
<body>
<h1>Server Side Code Injection</h1>

<form id="hi" action="eval2.php" method="post">
Eval with single quote [POST]: <input type="text" name="page">
<input type="submit" value="submit">
</form>


<form id="hi" method="get">
Eval with double quote [GET]: <input type="text" name="page">
<input type="submit" value="submit">
</form>
	


<?php

if (isset($_POST['page'])){
	$page = $_POST['page'];
	echo "eval single quote:<br>";
	eval("echo '".$page."';");
}

if (isset($_GET['page'])) {

	$page = $_GET['page'];
	echo "<br><br>eval double quote:<br>";
	eval("echo \"".$page."\";");
}

?>

</body>
</html>
