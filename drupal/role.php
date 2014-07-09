<form action="role.php" type="GET">
    <select name="ip">
        <option value="192.168.2.178">192.168.2.178</option>
        <option value="192.168.2.179">192.168.2.179</option>
        <option value="192.168.2.180">192.168.2.180</option>
        <option value="192.168.2.181">192.168.2.181</option>
    </select>
    <input name="uname" value="zhaojinpeng@spolo.org" />
    <input type="submit" />
    <input type="button" onclick="window.location.href='./role.php'" value="Reset" />
</form>
<pre>
<?php

do {
    if ( isset($_GET['ip']) )
        $ip = $_GET['ip'];
    else
    {
        echo "no ip";
        break;
    }

    if ( isset($_GET['uname']) )
        $uname = $_GET['uname'];
    else
    {
        echo "no uname";
        break;
    }

    $shell = "/public/www/tool/drupal/role.sh  $ip $uname 2>&1";
    echo $shell;

    $result = shell_exec($shell);
    echo $result;

} while(0);

?>
</pre>
