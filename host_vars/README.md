# host_vars/README.md

The files in this directory containt variables for hosts are one for each host
in the inventory file.  They should contain the variables specific to that host
to customize it.

**group_vars/main.yaml** contains files named for the groups listed in the
inventory file.  Each file contains the variables specific to that group.

The groups in the inventory file for this example role are separated along OS
configurations.  Other groups can be added to the inventory file that destingush
geographic areas (e.g. *west*, *east*, *europe*, *asia*) or functional types of
servers (e.g. dns_servers, web_servers, time_server, license_server,
grid_server, vnc_server, load_balencer, database).  hosts can be part of
multiple groups