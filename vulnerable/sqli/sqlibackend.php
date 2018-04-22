<?php

if ( $_SERVER['REQUEST_METHOD'] == 'POST' ) {
    $servername = "localhost";
    $username = "root";
    $password = "toor";
    $db = "sqli";

    // Create connection
    $conn = new mysqli($servername, $username, $password, $db);

    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    $query = "select username, age, school from users where username = '". $_POST['username']."'";

    $result = $conn->query($query);
	    if ($result->num_rows > 0) {
        echo("We found you!\n");
        while($row = $result->fetch_assoc()) {
            echo("\nUsername: " . $row['username']);
            echo("\nAge: " . $row['age']);
            echo("\nSchool: " . $row['school']. "\n");
        }
    } else {
        echo("User not found.");
    }
$conn->close();
}

?>

