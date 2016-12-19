<?php

include('../config.php');
 
header('Content-type: application/json');

function api_error($message) 
{
  echo "{\"error\":\"$message\"}";
  exit;
}

try {
  $pdo = new PDO("mysql:host=$db_host;dbname=$db_name", $db_username, $db_password);
}
catch (Exception $e) {
  api_error($e->getMessage());
}

?>


