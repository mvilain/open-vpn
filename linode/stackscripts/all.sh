#!/bin/bash
# configure all instances with base requirements

echo "...disabling CheckHostIP..."
sed -i.orig -e "s/#   CheckHostIP yes/CheckHostIP no/" /etc/ssh/ssh_config

[ "$1" == "" ] && exit

echo "...setting hostname $1..."
echo "$1" > /etc/hostname
hostname "$1"
