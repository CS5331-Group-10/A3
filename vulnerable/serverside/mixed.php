<html>
<body>
<h1>Server Side Code Injection</h1>

<a href="lfi1.php?page=apples"> Click here for apples </a>
<br><br>
<form id="hi" action ="eval.php">
Eval this: <input type="text" name="page">
<input type="submit" value="submit">
</form>



</body>
</html>
