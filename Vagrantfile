#  -*- mode: ruby -*-
# vi: set ft=ruby :
#
# Vagrantfile for vpn

Vagrant.configure("2") do |config|
  # config.vm.network 'forwarded_port', guest: 80, host: 8080
  config.vm.synced_folder '.', '/vagrant', disabled: true
  config.ssh.insert_key = false
  # 6/14/21 https://github.com/hashicorp/vagrant/issues/8204 export SSH_AUTH_SOCK=""
  # remove config.ssh.{username,password} and set .ssh/config AddKeysToAgent no
  #config.ssh.username = 'vagrant'
  #config.ssh.password = 'vagrant'
  config.vm.boot_timeout = 120
  config.vm.provider :virtualbox do |vb|
    #vb.gui = true
    vb.memory = '1024'
  end
  #
  # provision on all machines to allow ssh w/o checking
  #
  config.vm.provision "shell", inline: <<-SHELLALL
    echo "...disabling CheckHostIP..."
    sed -i.orig -e "s/#   CheckHostIP yes/CheckHostIP no/" /etc/ssh/ssh_config
    sed -i -e "s/.*PermitRootLogin.*/PermitRootLogin yes/" /etc/ssh/ssh_config
  SHELLALL


  config.vm.define "a8" do |a8|
    a8.vm.box = "almalinux/8"
    a8.ssh.insert_key = false
    a8.vm.network 'private_network', ip: '192.168.10.188'
    a8.vm.hostname = 'a8'
    a8.vm.provision "shell", inline: <<-SHELL
      dnf config-manager --set-enabled powertools
      dnf makecache
      dnf install -y python3
      alternatives --set python /usr/bin/python3
    SHELL
    a8.vm.provision "ansible" do |ansible|
      ansible.compatibility_mode = "2.0"
      ansible.playbook = "play-vagrant.yaml"
      ansible.inventory_path = "./inventory_vagrant"
      # ansible.verbose = "v"
      # ansible.raw_arguments = [""]
    end
  end


  config.vm.define "c7" do |c7|
    c7.vm.box = "centos/7"
    c7.ssh.insert_key = false
    c7.vm.network 'private_network', ip: '192.168.10.107'
    c7.vm.hostname = 'c7'
    # ensure ip command installed w/ iproute
    c7.vm.provision "shell", inline: <<-SHELL
      yum install -y python libselinux-python iproute
    SHELL
    c7.vm.provision "ansible" do |ansible|
      ansible.compatibility_mode = "2.0"
      ansible.playbook = "play-vagrant.yaml"
      ansible.inventory_path = "./inventory_vagrant"
      # ansible.verbose = "vvv"
    end
  end
  
  # https://bugzilla.redhat.com/show_bug.cgi?id=1820925
  config.vm.define "c8" do |c8|
    c8.vm.box = "centos/8"
    c8.ssh.insert_key = false
    c8.vm.network 'private_network', ip: '192.168.10.108'
    c8.vm.hostname = 'c8'
    c8.vm.provision "shell", inline: <<-SHELL
      dnf config-manager --set-enabled powertools
      dnf makecache
      dnf install -y python3
      alternatives --set python /usr/bin/python3
    SHELL
    c8.vm.provision "ansible" do |ansible|
      ansible.compatibility_mode = "2.0"
      ansible.playbook = "play-vagrant.yaml"
      ansible.inventory_path = "./inventory_vagrant"
    end
  end


  config.vm.define "r8" do |r8|
    r8.vm.box = "rockylinux/8"
    r8.ssh.insert_key = false
    r8.vm.network 'private_network', ip: '192.168.10.189'
    r8.vm.hostname = 'r8'
    r8.vm.provision "shell", inline: <<-SHELL
      dnf config-manager --set-enabled powertools
      dnf makecache
      dnf install -y python3
      alternatives --set python /usr/bin/python3
    SHELL
    r8.vm.provision "ansible" do |ansible|
      ansible.compatibility_mode = "2.0"
      ansible.playbook = "play-vagrant.yaml"
      ansible.inventory_path = "./inventory_vagrant"
    end
  end


  # https://stackoverflow.com/questions/56460494/apt-get-install-apt-transport-https-fails-in-docker
  config.vm.define "d9" do |d9|
    d9.vm.box = "bento/debian-9"
    d9.ssh.insert_key = false
    d9.vm.network 'private_network', ip: '192.168.10.209'
    d9.vm.hostname = 'd9'
    d9.vm.provision "shell", inline: <<-SHELL
      apt-get install -y apt-transport-https
    SHELL
    d9.vm.provision "ansible" do |ansible|
      ansible.compatibility_mode = "2.0"
      ansible.playbook = "play-vagrant.yaml"
      ansible.inventory_path = "./inventory_vagrant"
    end
  end

  # don't use apt: update_cache=yes here because it won't work to trap
  config.vm.define "d10" do |d10|
    d10.vm.box = "bento/debian-10"
    d10.ssh.insert_key = false
    d10.vm.network 'private_network', ip: '192.168.10.210'
    d10.vm.hostname = 'd10'
    d10.vm.provision "shell", inline: <<-SHELL
      apt-get install -y apt-transport-https
    SHELL
    d10.vm.provision "ansible" do |ansible|
      ansible.compatibility_mode = "2.0"
      ansible.playbook = "play-vagrant.yaml"
      ansible.inventory_path = "./inventory_vagrant"
    end
  end

  # 2021.06.13 mirrors seem to be OK now, removing alternate repos
  # 2021.06.17 mirrors are slow with Torguard LA VPN; Seattle seems OK
  # https://mirrors.fedoraproject.org/mirrorlist?repo=fedora-32&arch=x86_64
  config.vm.define "f32" do |f32|
    f32.vm.box = "fedora/32-cloud-base"
    f32.ssh.insert_key = false
    f32.vm.network 'private_network', ip: '192.168.10.132'
    f32.vm.hostname = 'f32'
    f32.vm.provision "shell", inline: <<-SHELL
      dnf config-manager --setopt=fastestmirror=True --save
      dnf config-manager --add-repo https://dl.fedoraproject.org/pub/fedora/linux/releases/32/Everything/x86_64/os/
      dnf config-manager --add-repo http://mirror.metrocast.net/fedora/linux/releases/32/Everything/x86_64/os/
      dnf config-manager --add-repo http://mirrors.kernel.org/fedora/releases/32/Everything/x86_64/os/
      dnf config-manager --add-repo https://sjc.edge.kernel.org/fedora-buffet/fedora/linux/releases/32/Everything/x86_64/os/
      dnf install -y python3
    SHELL
    f32.vm.provision "ansible" do |ansible|
      ansible.compatibility_mode = "2.0"
      ansible.playbook = "play-vagrant.yaml"
      ansible.inventory_path = "./inventory_vagrant"
    end
  end
  
  config.vm.define "f33" do |f33|
    f33.vm.box = "fedora/33-cloud-base"
    f33.ssh.insert_key = false
    f33.vm.network 'private_network', ip: '192.168.10.133'
    f33.vm.hostname = 'f33'
    f33.vm.provision "shell", inline: <<-SHELL
      dnf install -y python3
    SHELL
    f33.vm.provision "ansible" do |ansible|
      ansible.compatibility_mode = "2.0"
      ansible.playbook = "play-vagrant.yaml"
      ansible.inventory_path = "./inventory_vagrant"
    end
  end
  
  config.vm.define "f34" do |f34|
    f34.vm.box = "fedora/34-cloud-base"
    f34.ssh.insert_key = false
    f34.vm.network 'private_network', ip: '192.168.10.134'
    f34.vm.hostname = 'f34'
    f34.vm.provision "shell", inline: <<-SHELL
      dnf install -y python3
    SHELL
    f34.vm.provision "ansible" do |ansible|
      ansible.compatibility_mode = "2.0"
      ansible.playbook = "play-vagrant.yaml"
      ansible.inventory_path = "./inventory_vagrant"
    end
  end


  config.vm.define "u18" do |u18|
    u18.vm.box = "ubuntu/bionic64"
    u18.vm.network 'private_network', ip: '192.168.10.118'
    u18.vm.hostname = 'u18'
    u18.vm.provision "shell", inline: <<-SHELL
      apt-get -y install python3
    SHELL
    u18.vm.provision "ansible" do |ansible|
      ansible.compatibility_mode = "2.0"
      ansible.playbook = "play-vagrant.yaml"
      ansible.inventory_path = "./inventory_vagrant"
    end
  end

  config.vm.define "u20" do |u20|
    u20.vm.box = "ubuntu/focal64"
    u20.vm.network 'private_network', ip: '192.168.10.120'
    u20.vm.hostname = 'u20'
    u20.vm.provision "shell", inline: <<-SHELL
      apt-get -y install python3
    SHELL
    u20.vm.provision "ansible" do |ansible|
      ansible.compatibility_mode = "2.0"
      ansible.playbook = "play-vagrant.yaml"
      ansible.inventory_path = "./inventory_vagrant"
    end
  end

end
