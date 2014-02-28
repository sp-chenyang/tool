#/bin/bash

# find duplicated files large than 1GB

# input
# $1 find this path

if [ "X$1" == "X" ]; then
    echo "[ERROR] \$1 - input path"
    exit
fi

path=$1

ls $path &> /dev/null
if [ $? -ne 0 ]; then
    echo "[ERROR] path not found"
    exit
fi

fdupes -r -S $path | grep -A 3 "[0-9]\{10\} bytes each:"
