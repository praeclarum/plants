<html>
<head>
  <title>
    PLANTS
  </title>
  <style>body{font-family:"Helvetica",sans-serif;font-size:16px}</style>
  <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<?php

include("config.php"); 
$pdo = new PDO("mysql:host=$db_host;dbname=$db_name", $db_username, $db_password);
?>
  <script type="text/javascript">
google.charts.load('current', {'packages':['line']});
google.charts.setOnLoadCallback(drawChart);

var allData = {
<?php
$dur = !empty($_GET['dur']) ? trim($_GET['dur']) : '1 00:00:00';
$stmt = $pdo->prepare("SELECT * FROM DataPoint WHERE name=:name AND time >= SUBTIME(NOW(), :dur) ORDER BY time ASC");
$names = array('H0','H1','H2','V');
foreach ($names as $name) {
echo '"'.$name.'":{';
$stmt->execute(array('name' => $name, 'dur' => $dur));
for ($i=0; $r = $stmt->fetch(); $i++) {
  echo '"'.$r['time'].'":'.$r['value'].',';
}
echo "},\n";
}
?>
};
var allNames = ['H0', 'H1', 'H2', 'V'];
    function drawChart() {

      var data = new google.visualization.DataTable();
      data.addColumn('datetime', 'Time');
      for (var y in allNames) {
         data.addColumn('number', allNames[y]);
      }
      data.addColumn('number', 'avg');

var rows = [];
for (var x in allData.H1) {
  var row = [new Date(x.replace(" ","T")+"-08:00")];
  var a = 0.0;
  var c = 0;
  for (var y in allNames) {
    var n = allNames[y];
    var v = allData[n][x] || 0.0;
    if (n.length > 1 && n[0] == "H") {
      a += v;
      c++;
    }
    row.push(v);
  }
  row.push(c>0?a/c:0);
  rows.push(row);
}
      data.addRows(rows);

      var options = {
        chart: {
          title: 'Soil Humidity',
          subtitle: 'inverse of raw sensor data (0 is dry, 4.1K is wet)'
        },
        colors: ["rgb(57,122,242)", "rgb(214,59,48)", "rgb(243,171,2)", "rgb(17,146,78)", "#ddd"],
        legend: {
          position: "bottom",
        },
        fontName: 'Helvetica',
      };

      var chart = new google.charts.Line(document.getElementById('linechart_material'));

      chart.draw(data, google.charts.Line.convertOptions(options));
    }
  </script>
</head>
<body>

<h1>
PLANTS
</h1>


<div id="linechart_material" style="width: 100%; height: 640px"></div>
<form action="/" method="GET">
duration: <select id="dur" name="dur">
  <option value="01:00:00">1 hour</option>
  <option value="06:00:00">6 hours</option>
  <option value="12:00:00">12 hours</option>
  <option value="1 00:00:00">1 day</option>
  <option value="2 00:00:00">2 days</option>
  <option value="7 00:00:00">1 week</option>
  <option value="30 00:00:00">1 month</option>
</select>
<input type="submit" value="update" />
<script>
document.getElementById('dur').value = <?php echo json_encode($dur); ?>;
</script>
</form>
<form>
<table>
<tbody>
<?php
$stmt = $pdo->prepare("SELECT * FROM Cal ORDER BY name ASC");
$stmt->execute(array('name' => $name, 'dur' => $dur));
for ($i=0; $r = $stmt->fetch(); $i++) {
  echo '<tr><th>'.$r['name'].'</th><td><input type="text" name="'.$r['name'].'" value="'.$r['value'].'" />';
}
?>
</tbody></table>
<input type="submit" value="update cals" />
</form>
<section style="display:none">
<h1>Add Data</h1>
<form action="data/add" method="POST">
name: <input type="text" name="name" /><br/>
value: <input type="text" name="value" /><br/>
<input type="submit" value="add" />
</form>
</section>

</body>
</html>
