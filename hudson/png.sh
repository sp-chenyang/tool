#!/bin/bash

set -e

# run this script on 192.168.0.61

cd /var/www/html/web/sites/default/files/

for file in *.png
do
    mode=`identify -format '%[channels]' "$file"`
    if [ $mode == "rgb" ] ; then
        echo "$file"
    fi
done

