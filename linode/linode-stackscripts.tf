// linode-stackscripts.tf -- create linode stackscripts to setup ansible
//================================================== VARIABLES (in linode-vars.tf)
//================================================== PROVIDERS (in providers.tf)
//================================================== GENERATE KEYS AND SAVE (in linode-keys.tf)
//================================================== STACKSCRIPTS
# https://cloud.linode.com/stackscripts/1
# <UDF name="HOSTNAME" Label="hostname to set deployed instance" default="example-666" hostname="example" />
# <UDF name="DOMAIN" Label="domain to set in hosts" default="example.com"/>

resource "linode_stackscript" "rhel7" {
  label = "rhel7"
  description = "Installs packages for ansible on RedHat 7"
  script = <<-EOF
    #!/bin/bash -x
    # <UDF name="HOSTNAME" Label="hostname to set deployed instance" default="example-666" hostname="example" />
    # <UDF name="DOMAIN" Label="domain to set in hosts" default="example.com"/>
    # COMMON functions
    echo "...disabling CheckHostIP..."
    sed -i.orig -e "s/#   CheckHostIP yes/CheckHostIP no/" /etc/ssh/ssh_config
    # (Linode's utility script)
    source <ssinclude StackScriptID=1>
    system_set_hostname $HOSTNAME
    system_add_host_entry $(system_primary_ip) $HOSTNAME.$DOMAIN $HOSTNAME
    system_configure_ntp
    enable_fail2ban

    yum install -y epel-release
    yum install -y python3 libselinux-python3 git
  EOF
  images = [
    "linode/centos7"
  ]
  rev_note = "2021.06.27"
}

resource "linode_stackscript" "rhel8" {
  label = "rhel8"
  description = "Installs packages for ansible on RedHat 8"
  script = <<-EOF
    #!/bin/bash -x
    # <UDF name="HOSTNAME" Label="hostname to set deployed instance" default="example-666" hostname="example" />
    # <UDF name="DOMAIN" Label="domain to set in hosts" default="example.com"/>
    # COMMON functions
    echo "...disabling CheckHostIP..."
    sed -i.orig -e "s/#   CheckHostIP yes/CheckHostIP no/" /etc/ssh/ssh_config
    # (Linode's utility script)
    source <ssinclude StackScriptID=1>
    system_set_hostname $HOSTNAME
    system_add_host_entry $(system_primary_ip) $HOSTNAME.$DOMAIN $HOSTNAME
    system_configure_ntp
    enable_fail2ban

    dnf config-manager --set-enabled powertools
    dnf makecache
    dnf install -y python3
    alternatives --set python /usr/bin/python3
  EOF
  images = [
    "linode/almalinux8", 
    "linode/centos8",
    "linode/rocky8"
  ]
  rev_note = "2021.06.27"
}

resource "linode_stackscript" "debian" {
  label = "debian"
  description = "Installs packages for ansible on debian"
  script = <<-EOF
    #!/bin/bash -x
    # <UDF name="HOSTNAME" Label="hostname to set deployed instance" default="example-666" hostname="example" />
    # <UDF name="DOMAIN" Label="domain to set in hosts" default="example.com"/>
    # COMMON functions
    echo "...disabling CheckHostIP..."
    sed -i.orig -e "s/#   CheckHostIP yes/CheckHostIP no/" /etc/ssh/ssh_config
    # (Linode's utility script)
    source <ssinclude StackScriptID=1>
    system_set_hostname $HOSTNAME
    system_add_host_entry $(system_primary_ip) $HOSTNAME.$DOMAIN $HOSTNAME
    system_configure_ntp
    enable_fail2ban
    debian_upgrade

    apt-get install -y apt-transport-https python-apt
  EOF
  images = [
    "linode/debian9", 
    "linode/debian10"
  ]
  rev_note = "2021.06.27"
}

resource "linode_stackscript" "fedora" {
  label = "fedora"
  description = "Installs packages for ansible on fedora"
  script = <<-EOF
    #!/bin/bash -x
    # <UDF name="HOSTNAME" Label="hostname to set deployed instance" default="example-666" hostname="example" />
    # <UDF name="DOMAIN" Label="domain to set in hosts" default="example.com"/>
    # COMMON functions
    echo "...disabling CheckHostIP..."
    sed -i.orig -e "s/#   CheckHostIP yes/CheckHostIP no/" /etc/ssh/ssh_config
    # (Linode's utility script)
    source <ssinclude StackScriptID=1>
    system_set_hostname $HOSTNAME
    system_add_host_entry $(system_primary_ip) $HOSTNAME.$DOMAIN $HOSTNAME
    system_configure_ntp
    enable_fail2ban

    dnf install -y python3
  EOF
  images = [
    "linode/fedora32",
    "linode/fedora33",
    "linode/fedora34"
  ]
  rev_note = "2021.06.27"
}

resource "linode_stackscript" "ubuntu" {
  label = "ubuntu"
  description = "Installs packages for ansible on ubuntu"
  script = <<-EOF
    #!/bin/bash -x
    # <UDF name="HOSTNAME" Label="hostname to set deployed instance" default="example-666" hostname="example" />
    # <UDF name="DOMAIN" Label="domain to set in hosts" default="example.com"/>
    # COMMON functions
    echo "...disabling CheckHostIP..."
    sed -i.orig -e "s/#   CheckHostIP yes/CheckHostIP no/" /etc/ssh/ssh_config
    # (Linode's utility script)
    source <ssinclude StackScriptID=1>
    system_set_hostname $HOSTNAME
    system_add_host_entry $(system_primary_ip) $HOSTNAME.$DOMAIN $HOSTNAME
    system_configure_ntp
    enable_fail2ban

    apt-get install -y install python3
  EOF
  images = [
    "linode/ubuntu18.04",
    "linode/ubuntu20.04",
  ]
  rev_note = "2021.06.27"
}
