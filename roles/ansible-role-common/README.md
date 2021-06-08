common
=========

This role can be called to install common packages and services across all hosts in a site.

Requirements
------------

This module may use SELinux commands which require an extra python module beyond python V2.  Be sure the target systems have this installed as part of the Vagrant file.

Debian and Ubuntu distributions do not use the SELinux features as the ansible modules for them are untested. 

Fedora 21 does not install SELinux by default, so the selinux-policy-default package must be installed by Vagrant prior to provisioning with ansible.

Rather than install ntp, chronyd will be installed and configured as it's best suited for systems that aren't up 24x7.

Fedora32's repos are hosted on mirrors with very poor network response from my VPN.  Tasks that install products take a very long time and frequently timed out. I even get timeouts on my straight ISP connection, so I have no workaround for this.  User's experience of Fedora32 may vary. Use Fedora33 instead.

Role Variables
--------------

A description of the settable variables for this role should go here, including any variables that are in defaults/main.yaml, vars/main.yaml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

Note that variables put in vars/ directory tree cannot be overridden by the command line prompt.  It's better to put varibables in defaults where the values can be overridden.

Time services packages and names aren't uniform.  To install the correct package and start the service, tasks/<distro>_tasks.yaml will check versions and install the appropriate package. This way ntp/chronyd aren't dependent on group_vars or vars/<distro>.

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

License
-------

BSD
