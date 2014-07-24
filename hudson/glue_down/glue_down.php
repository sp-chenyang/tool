<?php
if(isset($_GET['from']) && isset($_GET['to']))
{
    $from = $_GET['from'];
    $to = $_GET['to'];
    echo "ok";
}
else
{
    // default date
    $from = '2014-03-03';
    $to = '2014-08-01';
    $to = date("Y-m-d");
}
$shell = "gnuplot -e \"from='$from' ; to='$to'\" /public/www/status/glue_down.gp";
echo $shell;
$result = shell_exec($shell);
echo $result;
?>
<form action="./glue_down.php" method="get">
from : <input type="date" name="from"> to : <input type="date" name="to">
<input type="submit" />
<input type="reset" onClick="window.open('glue_down.php', '_self');" />
</form>

<img src="./glue_down.png" />

<iframe src="./192.168.0.61-glue_restart.log" width="100%" height="100%"/>