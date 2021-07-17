#!/bin/bash
echo "preserve_hostname: false" >> /etc/cloud/cloud.cfg

apt-get update -y
apt-get install -y apt-transport-https python-apt
