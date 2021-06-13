#  -*- mode: ruby -*-
# vi: set ft=ruby :
#
# Vagrantfile for vpn

Vagrant.configure("2") do |config|
  # config.vm.network 'forwarded_port', guest: 80, host: 8080
  config.vm.synced_folder '.', '/vagrant', disabled: true
  config.ssh.insert_key = false
#   config.ssh.username = 'root'
  config.ssh.password = 'vagrant'
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


# 6/12/21 centos/8 and almalinux/8 stopped being able to auth w/ insecure private key
# https://stackoverflow.com/questions/22922891/vagrant-ssh-authentication-failure
# cp ~/.vagrant.d/insecure_private_key ~/.vagrant/machines/default/virtualbox/private_key
# once box is running, can login with vagrant/vagrant but vagrant can't ssh into it
  config.vm.define "a8" do |a8|
    a8.vm.box = "almalinux/8"
    a8.ssh.insert_key = false
    a8.vm.network 'private_network', ip: '192.168.10.188'
    a8.vm.hostname = 'a8'
    a8.vm.provision "shell", inline: <<-SHELL
      dnf install -y epel-release
      dnf config-manager --set-enabled powertools
      dnf makecache
      dnf install -y ansible
      alternatives --set python /usr/bin/python3
    SHELL
    a8.vm.provision "ansible" do |ansible|
      ansible.compatibility_mode = "2.0"
      ansible.playbook = "site.yaml"
      ansible.inventory_path = "./inventory_vagrant"
      # ansible.verbose = "v"
      # ansible.raw_arguments = [""]
    end
  end


  config.vm.define "c6" do |c6|
    c6.vm.box = "bento/centos-6"
    c6.ssh.insert_key = false
    c6.ssh.password = 'vagrant'
    c6.vm.network 'private_network', ip: '192.168.10.106'
    c6.vm.hostname = 'c6'
    c6.vm.provision "shell", inline: <<-SHELL
      yum install -y epel-release
      yum install -y ansible libselinux-python
    SHELL
    c6.vm.provision "ansible" do |ansible|
      ansible.compatibility_mode = "2.0"
      ansible.playbook = "site.yaml"
      ansible.inventory_path = "./inventory_vagrant"
    end
  end

  config.vm.define "c7" do |c7|
    c7.vm.box = "bento/centos-7"
    c7.ssh.insert_key = false
    c7.vm.network 'private_network', ip: '192.168.10.107'
    c7.vm.hostname = 'c7'
    c7.vm.provision "shell", inline: <<-SHELL
      yum install -y python libselinux-python
    SHELL
    c7.vm.provision "ansible" do |ansible|
      ansible.compatibility_mode = "2.0"
      ansible.playbook = "site.yaml"
      ansible.inventory_path = "./inventory_vagrant"
    end
  end
  
  # https://bugzilla.redhat.com/show_bug.cgi?id=1820925
  config.vm.define "c8" do |c8|
    c8.vm.box = "bento/centos-8"
    c8.ssh.insert_key = false
    c8.vm.network 'private_network', ip: '192.168.10.108'
    c8.vm.hostname = 'c8'
    c8.vm.provision "shell", inline: <<-SHELL
      dnf install -y epel-release
      dnf config-manager --set-enabled powertools
      dnf makecache
      dnf install -y ansible
      alternatives --set python /usr/bin/python3
    SHELL
    c8.vm.provision "ansible" do |ansible|
      ansible.compatibility_mode = "2.0"
      ansible.playbook = "site.yaml"
      ansible.inventory_path = "./inventory_vagrant"
    end
  end


  # https://stackoverflow.com/questions/56460494/apt-get-install-apt-transport-https-fails-in-docker
  # 6/13/21 debian9 won't pass username/password to box, switch to bento
  config.vm.define "d9" do |d9|
    d9.vm.box = "bento/debian-9"
    d9.ssh.insert_key = false
    d9.vm.network 'private_network', ip: '192.168.10.209'
    d9.vm.hostname = 'd9'
    d9.vm.provision "shell", inline: <<-SHELL
      apt-get update
      apt-get install -y apt-transport-https
    SHELL
    d9.vm.provision "ansible" do |ansible|
      ansible.compatibility_mode = "2.0"
      ansible.playbook = "site.yaml"
      ansible.inventory_path = "./inventory_vagrant"
    end
  end

  # don't use apt: update_cache=yes here because it won't work to trap
  # 6/13/21 debian9 won't pass username/password to box, switch to bento
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
      ansible.playbook = "site.yaml"
      ansible.inventory_path = "./inventory_vagrant"
    end
  end

  # 202101.10 lots of mirrors are broken for f32 making package install VERY slow
  # https://superuser.com/questions/1035780/how-can-i-use-a-specific-mirror-server-in-fedora
  # try updating packages and see if that improves things (not really)
  # added fastestmirror and specific mirror
  # tried changing from fedora/32-cloud-base to another box
  # 2021.06.13 mirrors seem to be OK now, removing alternate repos
  config.vm.define "f32" do |f32|
    f32.vm.box = "fedora/32-cloud-base"
    f32.ssh.insert_key = false
    f32.vm.network 'private_network', ip: '192.168.10.132'
    f32.vm.hostname = 'f32'
    f32.vm.provision "shell", inline: <<-SHELL
#       dnf config-manager --setopt=fastestmirror=True --save
#       dnf config-manager --add-repo https://dl.fedoraproject.org/pub/fedora/linux/releases/32/Everything/x86_64/os/
#       dnf config-manager --add-repo http://mirrors.kernel.org/fedora/releases/32/Everything/x86_64/os/
      dnf install -y python3
    SHELL
    f32.vm.provision "ansible" do |ansible|
      ansible.compatibility_mode = "2.0"
      ansible.playbook = "site.yaml"
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
    # requires ansible_python_interpreter=/usr/bin/python3 in inventory
    f33.vm.provision "ansible" do |ansible|
      ansible.compatibility_mode = "2.0"
      ansible.playbook = "site.yaml"
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
    # requires ansible_python_interpreter=/usr/bin/python3 in inventory
    f34.vm.provision "ansible" do |ansible|
      ansible.compatibility_mode = "2.0"
      ansible.playbook = "site.yaml"
      ansible.inventory_path = "./inventory_vagrant"
    end
  end


  # 6/13/21 debian9 won't pass username/password to box, switch to bento
  config.vm.define "u16" do |u16|
#     u16.vm.box = "ubuntu/xenial64"
    u16.vm.box = "bento/ubuntu-16.04"
    u16.vm.network 'private_network', ip: '192.168.10.116'
    u16.vm.hostname = 'u16'
    u16.vm.provision "shell", inline: <<-SHELL
      apt-get -y install python3
    SHELL
    u16.vm.provision "ansible" do |ansible|
      ansible.compatibility_mode = "2.0"
      ansible.playbook = "site.yaml"
      ansible.inventory_path = "./inventory_vagrant"
    end
  end

  # ansible uses python3 1/7/21
  # 6/13/21 debian9 won't pass username/password to box, switch to bento
  config.vm.define "u18" do |u18|
#     u18.vm.box = "ubuntu/bionic64"
    u18.vm.box = "bento/ubuntu-18.04"
    u18.vm.network 'private_network', ip: '192.168.10.118'
    u18.vm.hostname = 'u18'
    u18.vm.provision "shell", inline: <<-SHELL
      apt-get -y install python3
    SHELL
    u18.vm.provision "ansible" do |ansible|
      ansible.compatibility_mode = "2.0"
      ansible.playbook = "site.yaml"
      ansible.inventory_path = "./inventory_vagrant"
    end
  end

  # https://www.reddit.com/r/Ubuntu/comments/ga187h/focal64_vagrant_box_issues/
  # 1/7/21 earlier releases of focal64 didn't work with vagrant but that's now been fixed
  # requires setting ansible_python_interpreter=/usr/bin/python3 
  # 6/13/21 debian9 won't pass username/password to box, switch to bento
  config.vm.define "u20" do |u20|
#     u20.vm.box = "ubuntu/focal64"
    u20.vm.box = "bento/ubuntu-20.04"
    #u20.vm.box = "bento/ubuntu-20.04"
    u20.vm.network 'private_network', ip: '192.168.10.120'
    u20.vm.hostname = 'u20'
    u20.vm.provision "shell", inline: <<-SHELL
      apt-get -y install python3
    SHELL
    u20.vm.provision "ansible" do |ansible|
      ansible.compatibility_mode = "2.0"
      ansible.playbook = "site.yaml"
      ansible.inventory_path = "./inventory_vagrant"
    end
  end

end
