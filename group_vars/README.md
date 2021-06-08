## group_vars/README.md

This directory contains separate variable files, one for each inventory group
defined in the inventory file.  They are processed automatically by ansible,
depending on the hosts entry in a playlist.

The inventory file contains the list of hosts, groups, and any inventory-wide
variables.  If you want to define variables that will be on all the hosts in the
inventory, place it in the inventory file under the [all:vars] block.

The groups in the inventory file for this example role are separated along OS
configurations.  Other groups can be added to the inventory file that destingush
geographic areas (e.g. *west*, *east*, *europe*, *asia*) or functional types of
servers (e.g. dns_servers, web_servers, time_server, license_server,
grid_server, vnc_server, load_balencer, database).  hosts can be part of
multiple groups