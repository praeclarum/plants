<?php

include('api.php');
/*
$name = trim(filter_input(INPUT_POST, 'name', FILTER_SANITIZE_STRING, FILTER_FLAG_STRIP_LOW));
if (!$name) {
  api_error('missing name');
}

$value = trim(filter_input(INPUT_POST, 'value', FILTER_SANITIZE_STRING, FILTER_FLAG_STRIP_LOW));
if (is_null($value)) {
  api_error('missing value');
}

$time = trim(filter_input(INPUT_POST, 'time', FILTER_SANITIZE_STRING, FILTER_FLAG_STRIP_LOW));
if (!$time) {
  api_error('missing time');
}

$stmt = $pdo->prepare('INSERT INTO DataPoint(name,value,time) VALUES (:name,:value,:time)');
$stmt->execute(array('name' => $name, 'value' => $value, 'time' => $time));

$id = $pdo->lastInsertId ();

echo "{\"id\":$id}";
*/

echo "{";
$head='';
foreach ($_POST as $name => $value) {

$stmt = $pdo->prepare("UPDATE Cal SET value=:value WHERE name=:name");                                                                     
$stmt->execute(array('name' => $name, 'value' => $value));                                                                            
echo "$head\"$name\": $value";
$head=",\n";
}
echo "}";

?>

