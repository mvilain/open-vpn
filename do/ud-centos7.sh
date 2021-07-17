#!/bin/bash
echo "preserve_hostname: false" >> /etc/cloud/cloud.cfg

yum install -y epel-release
#    yum install -y ansible
#    yum install -y python3 libselinux-python3 git
# alternatives --set python /usr/bin/python
