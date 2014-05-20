#!/bin/bash

# config option
sshfsopt="-o reconnect,allow_other,default_permissions -o uid=1000 -o gid=1000 -o IdentityFile=/home/chenyang/.ssh/3dly.net.key"
davopt="-o username=admin,gid=chenyang,uid=chenyang"
curlftpfsopt="-o allow_other,rw,uid=1000,gid=1000"

#
# function list
#

xlog()
{
    local str="[DEBUG] $1"
    echo -e "$str"
}

mlog()
{
    local str="Mounting $1"
    xlog "$str"
}

# run command
run()
{
    local cmd="$1"
    xlog "cmd=\"$cmd\""
    eval "$cmd"
}

# get root permission
root()
{
    xlog "being root..."
    sudo ls &> /dev/null
    if [ $? -ne 0 ]; then
        exit 1
    fi
}

# make dir for this ip
# $1 - 192.168.0.1/dvm.spolo.org
# $2 - dav/sftp/ftp
getdir()
{
    local ip="$1"
    local proto="$2"

    local dir="$HOME/Mount/"

    if [ $ip == "dvm.spolo.org" ]; then
        dir="${dir}dvm${proto}"
    else
        # 192.168.2.1 => 2.1
        dir="${dir}${ip//192.168./}${proto}"
    fi

    # try to make new dir.
    echo "mkdir -p \"$dir\"" >> /tmp/mnt.log
    mkdir -p "$dir"
    echo $? >> /tmp/mnt.log

    #return
    echo "$dir"
}

davmount()
{
    local ip="$1"
    local dir="$( getdir "$ip" "dav" )"
    local cmd=""

    mlog "$ip dav, username=admin"

    run "sudo umount \"$dir\""
    run "sudo mount -t davfs ${ip}:8080 \"$dir\" $davopt"

    xlog "\n\n"
}


ftpmount()
{
    local ip="$1"
    local dir="$( getdir "$ip" "ftp" )"

    mlog "curlftpfs $ip"

    run "fusermount -u \"$dir\""
    run "curlftpfs $curlftpfsopt ftp://apache:apache@${ip} \"$dir\""

    xlog "\n\n"
}

sftpmount()
{
    local ip="$1"
    local dir="$( getdir "$ip" "sftp" )"

    mlog "sftp://chenyang@192.168.${ip}"

    run "fusermount -u \"$dir\""
    run "sshfs $sshfsopt chenyang@${ip}:/ \"$dir\""

    xlog "\n\n"
}

# mount single server
# $1 server alias name
#  - dvm
#  - 0.61
mnt_single()
{
    local ip=""
    if [ $1 == "dvm" ]; then
        ip="dvm.spolo.org"
    else
        ip="192.168.$1"
    fi

    root

    davmount "$ip"
    ftpmount "$ip"
    sftpmount "$ip"
}

# mount all server
mnt_all()
{
    root

    #
    # dav
    #
    
    davmount "192.168.0.59" 
    #davmount "192.168.0.60" 
    davmount "192.168.0.61" 
    davmount "192.168.2.176" 
    davmount "dvm.spolo.org" 
    
    #
    # ftp
    #
    
    #ftpmount "0.60"
    ftpmount "192.168.0.61"
    ftpmount "192.168.2.176"
    
    #
    # sftp
    #

    sftpmount "192.168.0.60"
    sftpmount "192.168.0.61"
    sftpmount "192.168.2.176"
    sftpmount "192.168.0.59"
    sftpmount "192.168.0.174"
    sftpmount "192.168.0.175"
    
    sftpmount "192.168.2.21"
    sftpmount "192.168.0.101"
    
    #mlog "sftp://root@dvm.spolo.org"
    #fusermount -u /home/chenyang/Mount/dvmsftp/
    #sshfs $sshfsopt root@dvm.spolo.org:/ ~/Mount/dvmsftp
}

usage()
{
    echo "usage: mnt.sh [[[-s server ] [-a]] | [-h]]"
    echo "example1 : mnt.sh -a"
    echo "example2 : mnt.sh -s \"2.176\""
    echo "example3 : mnt.sh -s \"dvm\""
}

#
# main
#

# get cmd line param
while [ "$1" != "" ]; do
    case $1 in
        -s | --server )         shift
                                mnt_single "$1"
                                exit 0
                                ;;
        -a | --all )            mnt_all
                                exit 0
                                ;;
        -h | --help )           usage
                                exit
                                ;;
        * )                     usage
                                exit 1
    esac
    shift
done

usage
exit 1
