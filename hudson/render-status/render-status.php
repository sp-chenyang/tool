<pre>
<?php
$ip = $_GET["ip"];
if ($ip == NULL)
{
    $shell = "/public/www/status/render-status.sh -a";
}
else
{
    $shell = "/public/www/status/render-status.sh -s $ip";
}
$result = shell_exec($shell);
echo $result;
?>
</pre>
