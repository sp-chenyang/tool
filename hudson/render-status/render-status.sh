#!/bin/bash

# temp


rcmd()
{
    local ip=$1
    local cmd=$2
    echo -e "\n$cmd\n---------------------"
    ssh -o ConnectTimeout=8 chenyang@$ip "$cmd"
}

run()
{
    local ip=$1
    echo $ip
    echo "------------------------------------------"
    ping -c 1 $ip
    #if [ "$?" == 0 ] || [ "$?" == 1 ] ; then
    if [ "$?" == 0 ] ; then
        rcmd $ip "ps -ef|grep blen[d]"
        rcmd $ip "nvidia-smi -q |grep \"FB Memory Usage\" -A 2"
        rcmd $ip "tail -n 10000 /var/log/npm.log |grep DEBUG"
        rcmd $ip "tail /var/log/npm.log"
    fi
    echo -e "\n====================================================================================\n"
}

all()
{
    ip1="192.168.0.174"
    ip2="192.168.0.175"
    ip3="192.168.0.176"
    run "$ip1"
    run "$ip2"
    run "$ip3"
}

single()
{
    ip=$1
    run "$ip"
}

usage()
{
    echo "usage: render-status.sh [[[-s server ] [-a]] | [-h]]"
    echo "example1 : render-status.sh -a"
    echo "example2 : render-status.sh -s \"192.168.0.175\""
}

#
# main
#

# get cmd line param
while [ "$1" != "" ]; do
    case $1 in
        -s | --server )         shift
                                single "$1"
                                exit 0
                                ;;
        -a | --all )            all
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
