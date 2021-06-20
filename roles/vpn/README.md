vpn
=========

This role can be called to install the vpn package and services across all hosts in a site. It relies on [this outline](https://notthebe.ee/Creating-your-own-OpenVPN-server.html) script.

Requirements
------------

vagrant requires a public/private key pair to login to the vagrant boxes. This is usually specified in the inventory file, but if ssh-agent has been enabled (e.g. `AddKeysToAgent yes` is set in the `.ssh/config file`), some vagrant boxes won't be able to connect and authenticate.

As of 6/14/21, CentOS 8, Debian, and Ubuntu boxes won't work if `AddKeysToAgent` is set.  The workaround for this is to set the environment SSH\_AUTH\_SOCK to a blank string:

    export SSH_AUTH_SOCK=""

See [this link](https://github.com/hashicorp/vagrant/issues/8204).  Adding the key to the ssh-agent doesn't fix this.

CentOS 7 -- ansible must run under python 2.7 as the python3 version available is to old; the ansible\_python\_interpreter should be set to /usr/bin/python in the inventory file

CentOS 8 and AlmaLinux 8 -- ansible needs to be installed prior on the client to install all python3 modules and libraries; the ansible\_python\_interpreter should be set to /usr/libexec/platform-python in the inventory file

Debian, Fedora, and Ubuntu -- python3 should already be installed and new enough to connect to ansible on the provisioning machine; ansible\_python\_interpreter should be set to /usr/bin/python3 in the inventory file


Role Variables
--------------

A description of the settable variables for this role should go here, including any variables that are in defaults/main.yaml, vars/defaults.yaml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

Note that variables put in vars/ directory tree cannot be overridden by the command line prompt.  It's better to put varibables in defaults where the values can be overridden.

Time services packages and names aren't uniform.  To install the correct package and start the service, tasks/<distro-family>\_tasks.yaml will check versions and install the appropriate package.

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: vpn }

License
-------

BSD
