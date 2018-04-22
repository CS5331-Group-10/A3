<html>
<head>

<h1>Secret Messages</h1>

<form method="POST">
    Username: <input type="text" name="secret" value="SECRET" />
    <input type="submit" />
</form>

<?php
	if (isset($_POST["secret"])) {
		setcookie("CSRF","abcdef1235");
		echo "Your CSRF Token is" . $_COOKIE["CSRF"];
	}
?>
</head>
</html>
