#!/bin/bash

IP=$1
NAME=$2

rcmd()
{
    local ip=$1
    local cmd=$2
    echo -e "\n$cmd\n---------------------"
    ssh -o StrictHostKeyChecking=no -o ConnectTimeout=8 chenyang@$ip "$cmd"
}

XCMD="cd /var/www/html/web"
XCMD="$XCMD; drush user-create $NAME --mail=\"$NAME@spolo.org\" --password=\"sp12345678\""
XCMD="$XCMD; drush user-add-role \"administrator\" $NAME"
XCMD="$XCMD; drush user-information $NAME"

rcmd $IP "$XCMD"
