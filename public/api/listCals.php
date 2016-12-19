<?php

include('api.php');

echo "{";
$head='';
$stmt = $pdo->prepare("SELECT * FROM Cal ORDER BY name ASC");                                                                     
$stmt->execute();                                                                            
for ($i=0; $r = $stmt->fetch(); $i++) {
$name = $r['name'];
$value = $r['value'];                                                                                           
echo "$head\"$name\": $value";
$head=",\n";
}
echo "}";

?>

