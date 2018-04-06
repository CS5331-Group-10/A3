<html>
<body>
<h1>Server Side Code Injection</h1>
<?php

if (!isset($_GET['page'])) {
    $page = "main2";
}
else {
    $page = $_GET['page'];
}

chdir("./pages/");

include("./" . $page . ".php");

?>
</body>
</html>
