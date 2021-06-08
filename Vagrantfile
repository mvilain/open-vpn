# -*- mode: ruby -*-
# vi: set ft=ruby :

# vpn demo Vagrant file to spin up multiple machines and OS'
# Maintainer Michael Vilain [202106.05]

Vagrant.configure("2") do |config|
  # config.vm.network 'forwarded_port', guest: 80, host: 8080
  config.vm.synced_folder '.', '/vagrant', disabled: false
  config.ssh.insert_key = false
#   config.ssh.username = 'root'
#   config.ssh.password = 'vagrant'
  config.vm.boot_timeout = 120
  config.vm.provider :virtualbox do |vb|
    #vb.gui = true
    vb.memory = '2048'
  end
  #
  # provision on all machines to allow ssh w/o checking
  #
  config.vm.provision "shell", inline: <<-SHELLALL
    echo "...disabling CheckHostIP..."
    sed -i.orig -e "s/#   CheckHostIP yes/CheckHostIP no/" /etc/ssh/ssh_config
  SHELLALL


# vagrant box has python2.7 installed with /usr/libexec/platform-python
  config.vm.define "vpn7" do |vpn7|
    vpn7.vm.box = "centos/7"
    vpn7.ssh.insert_key = false
    vpn7.vm.network 'private_network', ip: '192.168.10.107'
    vpn7.vm.hostname = 'vpn7'
#     vpn7.vm.provision "shell", inline: <<-SHELL
#      yum install -y epel-release
#       yum install -y python3 libselinux-python3 #python36-rpm
#     SHELL
    # still uses python2 for ansible
    vpn7.vm.provision "ansible" do |ansible|
      ansible.compatibility_mode = "2.0"
      ansible.playbook = "site.yml"
      ansible.inventory_path = "./inventory_vagrant"
    end
  end

  # https://bugzilla.redhat.com/show_bug.cgi?id=1820925
  # use AlmaLinux CentOS fork 202104.03
  # # vagrant box has python3.6 installed with /usr/libexec/platform-python
  config.vm.define "vpn8" do |vpn8|
#     vpn8.vm.box = "centos/8"
    vpn8.vm.box = "almalinux/8"
    vpn8.ssh.insert_key = false
    vpn8.vm.network 'private_network', ip: '192.168.10.108'
    vpn8.vm.hostname = 'vpn8'
    vpn8.vm.provision "shell", inline: <<-SHELL
      dnf install -y epel-release
      dnf config-manager --set-enabled powertools
      dnf makecache
      dnf install -y ansible
      alternatives --set python /usr/bin/python3
    SHELL
    vpn8.vm.provision "ansible" do |ansible|
      ansible.compatibility_mode = "2.0"
      ansible.playbook = "site.yml"
      ansible.inventory_path = "./inventory_vagrant"
    end
  end


  # https://stackoverflow.com/questions/56460494/apt-get-install-apt-transport-https-fails-in-docker
  config.vm.define "vpn9" do |vpn9|
    vpn9.vm.box = "debian/stretch64"
    vpn9.ssh.insert_key = false
    vpn9.vm.network 'private_network', ip: '192.168.10.109'
    vpn9.vm.hostname = 'vpn9'
    vpn9.vm.provision "shell", inline: <<-SHELL
      apt-get update --allow-releaseinfo-change -y
      apt-get install -y apt-transport-https python-apt
    SHELL
    vpn9.vm.provision "ansible" do |ansible|
      ansible.compatibility_mode = "2.0"
      ansible.playbook = "site.yml"
      ansible.inventory_path = "./inventory_vagrant"
    end
  end

  # don't use apt: update_cache=yes here because it won't work to trap
  # repo change errors like with Debian 10 because of apt-secure server
  config.vm.define "vpn10" do |vpn10|
    vpn10.vm.box = "debian/buster64"
    vpn10.ssh.insert_key = false
    vpn10.vm.network 'private_network', ip: '192.168.10.110'
    vpn10.vm.hostname = 'vpn10'
    vpn10.vm.provision "shell", inline: <<-SHELL
      apt-get update --allow-releaseinfo-change -y
      apt-get install -y apt-transport-https python-apt
    SHELL
    vpn10.vm.provision "ansible" do |ansible|
      ansible.compatibility_mode = "2.0"
      ansible.playbook = "site.yml"
      ansible.inventory_path = "./inventory_vagrant"
    end
  end

# deprecated notice for vpn 14 on Ubuntu 16 4/15/2021
  config.vm.define "vpn16" do |vpn16|
    vpn16.vm.box = "ubuntu/xenial64"
    vpn16.vm.network 'private_network', ip: '192.168.10.116'
    vpn16.vm.hostname = 'vpn16'
    vpn16.vm.provision "shell", inline: <<-SHELL
      apt-get -y install python3
    SHELL
    vpn16.vm.provision "ansible" do |ansible|
      ansible.compatibility_mode = "2.0"
      ansible.playbook = "site.yml"
      ansible.inventory_path = "./inventory_vagrant"
    end
  end

  # ansible uses python3 1/7/21
  config.vm.define "vpn18" do |vpn18|
    vpn18.vm.box = "ubuntu/bionic64"
    vpn18.vm.network 'private_network', ip: '192.168.10.118'
    vpn18.vm.hostname = 'vpn18'
    vpn18.vm.provision "shell", inline: <<-SHELL
      apt-get -y install python3
    SHELL
    vpn18.vm.provision "ansible" do |ansible|
      ansible.compatibility_mode = "2.0"
      ansible.playbook = "site.yml"
      ansible.inventory_path = "./inventory_vagrant"
    end
  end

  # https://www.reddit.com/r/Ubuntu/comments/ga187h/focal64_vagrant_box_issues/
  # 1/7/21 earlier focal64 didn't work w/ vagrant, fixed
  # requires setting ansible_python_interpreter=/usr/bin/python3 
  config.vm.define "vpn20" do |vpn20|
    vpn20.vm.box = "ubuntu/focal64"
    #vpn20.vm.box = "bento/ubuntu-20.04"
    vpn20.vm.network 'private_network', ip: '192.168.10.120'
    vpn20.vm.hostname = 'vpn20'
    vpn20.vm.provision "shell", inline: <<-SHELL
      apt-get -y install python3
    SHELL
    vpn20.vm.provision "ansible" do |ansible|
      ansible.compatibility_mode = "2.0"
      ansible.playbook = "site.yml"
      ansible.inventory_path = "./inventory_vagrant"
    end
  end

end
