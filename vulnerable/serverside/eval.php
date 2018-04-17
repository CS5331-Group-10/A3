<html>
<body>
<h1>Server Side Code Injection</h1>

<form id="hi" method="get">
Eval this: <input type="text" name="page">
<input type="submit" value="submit">
</form>
<?php


if (isset($_GET['page'])){
	
	$page = $_GET['page'];
	echo "<br><br>Non-echo eval: ";
	$x = "fail";
	eval("\$x = $page;");
	echo "<br>".$x;
}
?>

</body>

</html>
