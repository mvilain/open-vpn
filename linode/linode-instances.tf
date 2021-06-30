// linode.tf -- spin up the vpn linode instances and define in DNS
//================================================== VARIABLES (in linode-vars.tf)
//================================================== PROVIDERS (in providers.tf)
//================================================== GENERATE KEYS AND SAVE (in linode-keys.tf)
//================================================== INSTANCES
// current account limits to 10 Linodes
# inputs:
#  password  - Linode root password                              [default: NONE ]
#  ssh_key   - Linode public ssh key for setting authorize_hosts [default: NONE ]
#  image     - Linode Image type used to create instance         [default: "linode/ubuntu18.04"]
#  region    - Linode region where instance will run             [default: "us-west"]
#  type      - Linode image size to use                          [default: "g6-nanode-1"]
#  label     - label used to create the instance and hostname    [default: "example"]
#  domain    - Linode-managed DNS domain used to assign host IP  [default: "example.com"]
#  script    - linode stackscript to run on instance boot        [default: NONE ]
#module "lin_vpn_alma8" {
#  source   = "./terraform-modules/terraform-linode-instance"
#
#  password  = random_password.linode_root_pass.result
#  ssh_key   = chomp(tls_private_key.linode_ssh_key.public_key_openssh)
#  domain    = var.linode_domain
#  image     = "linode/almalinux8"
#  type      = "g6-nanode-1"
#  script    = linode_stackscript.rhel8.id
#  label     = "vpn-a"
#}
# outputs:
#  id
#  status
#  ip_address
#  private_ip_address
#  ipv6
#  ipv4
#  backups (enabled, schedule, day, window)

module "lin_vpn_centos7" {
  source   = "./terraform-modules/terraform-linode-instance"
  password  = random_password.linode_root_pass.result
  ssh_key   = chomp(tls_private_key.linode_ssh_key.public_key_openssh)
  domain    = var.linode_domain
  region    = "ca-central"

  image     = "linode/centos7"
  type      = "g6-nanode-1"
  script    = linode_stackscript.rhel7.id
  label     = "vpn7tor"
}
module "lin_vpn_centos8" {
  source   = "./terraform-modules/terraform-linode-instance"
  password  = random_password.linode_root_pass.result
  ssh_key   = chomp(tls_private_key.linode_ssh_key.public_key_openssh)
  domain    = var.linode_domain
  region    = "eu-west"

  image     = "linode/centos8"
  type      = "g6-nanode-1"
  script    = linode_stackscript.rhel8.id
  label     = "vpn8lon"
}


module "lin_vpn_debian9" {
  source   = "./terraform-modules/terraform-linode-instance"
  password  = random_password.linode_root_pass.result
  ssh_key   = chomp(tls_private_key.linode_ssh_key.public_key_openssh)
  domain    = var.linode_domain
  region    = "us-central"

  image     = "linode/debian9"
  type      = "g6-nanode-1"
  script    = linode_stackscript.debian.id
  label     = "vpn9dfw"
}
module "lin_vpn_debian10" {
  source   = "./terraform-modules/terraform-linode-instance"
  password  = random_password.linode_root_pass.result
  ssh_key   = chomp(tls_private_key.linode_ssh_key.public_key_openssh)
  domain    = var.linode_domain
  region    = "us-east"

  image     = "linode/debian10"
  type      = "g6-nanode-1"
  script    = linode_stackscript.debian.id
  label     = "vpn10nj"
}


module "lin_vpn_fedora32" {
  source   = "./terraform-modules/terraform-linode-instance"
  password  = random_password.linode_root_pass.result
  ssh_key   = chomp(tls_private_key.linode_ssh_key.public_key_openssh)
  domain    = var.linode_domain
  region    = "us-west"

  image     = "linode/fedora32"
  type      = "g6-nanode-1"
  script    = linode_stackscript.fedora.id
  label     = "vpn32"
}
module "lin_vpn_fedora33" {
  source   = "./terraform-modules/terraform-linode-instance"
  password  = random_password.linode_root_pass.result
  ssh_key   = chomp(tls_private_key.linode_ssh_key.public_key_openssh)
  domain    = var.linode_domain
  region    = "us-west"

  image     = "linode/fedora33"
  type      = "g6-nanode-1"
  script    = linode_stackscript.fedora.id
  label     = "vpn33"
}
module "lin_vpn_fedora34" {
  source   = "./terraform-modules/terraform-linode-instance"
  password  = random_password.linode_root_pass.result
  ssh_key   = chomp(tls_private_key.linode_ssh_key.public_key_openssh)
  domain    = var.linode_domain
  region    = "us-west"

  image     = "linode/fedora34"
  type      = "g6-nanode-1"
  script    = linode_stackscript.fedora.id
  label     = "vpn34"
}


module "lin_vpn_rocky8" {
  source   = "./terraform-modules/terraform-linode-instance"
  password  = random_password.linode_root_pass.result
  ssh_key   = chomp(tls_private_key.linode_ssh_key.public_key_openssh)
  domain    = var.linode_domain
  region    = "us-west"

  image     = "linode/rocky8"
  type      = "g6-nanode-1"
  script    = linode_stackscript.rhel8.id
  label     = "vpn-r"
}


module "lin_vpn_ubuntu18" {
  source   = "./terraform-modules/terraform-linode-instance"
  password  = random_password.linode_root_pass.result
  ssh_key   = chomp(tls_private_key.linode_ssh_key.public_key_openssh)
  domain    = var.linode_domain
  region    = "us-southeast"

  image     = "linode/ubuntu18.04"
  type      = "g6-nanode-1"
  script    = linode_stackscript.ubuntu.id
  label     = "vpn18atl"
}
module "lin_vpn_ubuntu20" {
  source   = "./terraform-modules/terraform-linode-instance"
  password  = random_password.linode_root_pass.result
  ssh_key   = chomp(tls_private_key.linode_ssh_key.public_key_openssh)
  domain    = var.linode_domain
  region    = "us-west"

  image     = "linode/ubuntu20.04"
  type      = "g6-nanode-1"
  script    = linode_stackscript.ubuntu.id
  label     = "vpn20sfo"
}