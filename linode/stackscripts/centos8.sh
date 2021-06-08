#!/bin/bash
# configure CentOS 8 to use ansible

dnf install -y epel-release
dnf config-manager --set-enabled powertools
dnf makecache
dnf install -y ansible
alternatives --set python /usr/bin/python3

