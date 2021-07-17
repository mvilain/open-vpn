#!/bin/bash
echo "preserve_hostname: false" >> /etc/cloud/cloud.cfg

dnf install -y epel-release
dnf config-manager --set-enabled powertools
dnf makecache
#    dnf install -y ansible
alternatives --set python /usr/bin/python3
