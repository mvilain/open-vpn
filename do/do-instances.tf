// do-instances.tf -- spin up the vpn digital ocean droplets and define in DNS
//================================================== PROVIDERS (in providers.tf)
//================================================== VARIABLES (in do-vars.tf)
//================================================== GENERATE KEYS AND SAVE (in do-keys.tf)
// ================================================= VPC + FIREWALL (in do-vpc-fw.tf)
//================================================== INSTANCES

# terraform-digitalocean-droplet
# inputs:
#  application   - application being deployed
#  environment   - environment (e.g. dev, test, stage, prod)
#  label_order   - array of args above order for tags
#  name          - name of droplet combined w/ above in label_order [default: example]
#  droplet_count - number of droplets to spin up [default: 1]
#  ssh_keys      - array of ssh key names checked into digital ocean for ssh access
#  domain        - pre-existing DNS domain name to add droplet [default: example.com]
#  vpc_uuid      - default vpc for region or a pre-defined one created
#  region        - region to create droplet in [default: "sfo3"]
#                  ams2 ams3 blr1 fra1 lon1 nyc1 nyc2 nyc3 sfo1 sfo2 sfo3 sgp1 tor1
#  image_name    - droplet image to spin up. can be distro or private [default: "ubuntu-18-04-x64"]
#  droplet_size  - what size of droplet (# CPU and memory) [default: "s-1vcpu-1gb"]
#                  s-1vcpu-1gb
#                  s-2vcpu-2gb
#                  s-2vcpu-4gb
#                  s-4vcpu-8gb
#                  c2
#                  c4
#                  m-2vcpu-16gb
#                  g-2vcpu-8gb
#                  gd-2vcpu-8gb
#  monitoring    - turn on monitor from digital ocean dashboard
#  private_networking - don't make droplet publically accessible
#  ipv6          - use IPv6 networking
#  floating_ip   - enable permanent IP that can be assigned to droplet
#  block_storage_enabled - add additional block storage volume
#  block_storage_size - size of additional storage
#  user-data - user-data cloud-init script to run on boot   [default: NONE ]
#
# outputs:
#   id     - ID of droplet
#   urn    - uniform resource name of droplet
#   name   - name of droplet"

# ./do-list-droplets.py -r lists valid regions
# ./do-list-droplets.py -i lists valid images

module "drop_c7" {
  source                = "./terraform-modules/terraform-digitalocean-droplet/"
  application           = "vpn"
  environment           = "centos"
  label_order           = ["environment", "application", "name"]

  name                  = "c7sfo3"  # hostname: test-vpn-<NAME>-<DROPLET-COUNT -1>
  droplet_count         = 1
  ssh_keys              = [ digitalocean_ssh_key.do_vpn_ssh_key.id ]
  domain                = var.do_domain
  vpc_uuid              = data.digitalocean_vpc.default.id
  
  region                = "sfo3" # var.do_region

  image_name            = "centos-7-x64"
  droplet_size          = "nano"
  monitoring            = true
  private_networking    = false
  ipv6                  = false
  floating_ip           = true
  block_storage_enabled = false
  block_storage_size    = 0

  user_data             = file("ud-centos7.sh")
}
module "drop_c8" {
  source                = "./terraform-modules/terraform-digitalocean-droplet/"
  application           = "vpn"
  environment           = "centos"
  label_order           = ["environment", "application", "name"]

  name                  = "c8sfo3"  # hostname: test-vpn-<NAME>-<DROPLET-COUNT -1>
  droplet_count         = 1
  ssh_keys              = [ digitalocean_ssh_key.do_vpn_ssh_key.id ]
  domain                = var.do_domain
  vpc_uuid              = data.digitalocean_vpc.default.id
  # "ams2" "ams3" "blr1" "fra1" "lon1" "nyc1" "nyc2" "nyc3" "sfo1" "sfo2" "sfo3" "sgp1" "tor1"
  region                = "sfo3" # var.do_region

  image_name            = "centos-8-x64"
  droplet_size          = "nano"
  monitoring            = true
  private_networking    = false
  ipv6                  = false
  floating_ip           = true
  block_storage_enabled = false
  block_storage_size    = 0

  user_data             = file("ud-redhat.sh")
}


module "drop_d9" {
  source                = "./terraform-modules/terraform-digitalocean-droplet/"
  application           = "vpn"
  environment           = "debian"
  label_order           = ["environment", "application", "name"]

  name                  = "d9sfo3"  # hostname: test-vpn-<NAME>-<DROPLET-COUNT -1>
  droplet_count         = 1
  ssh_keys              = [ digitalocean_ssh_key.do_vpn_ssh_key.id ]
  domain                = var.do_domain
  vpc_uuid              = data.digitalocean_vpc.default.id
  # "ams2" "ams3" "blr1" "fra1" "lon1" "nyc1" "nyc2" "nyc3" "sfo1" "sfo2" "sfo3" "sgp1" "tor1"
  region                = "sfo3" # var.do_region

  image_name            = "debian-9-x64"
  droplet_size          = "nano"
  monitoring            = true
  private_networking    = false
  ipv6                  = false
  floating_ip           = true
  block_storage_enabled = false
  block_storage_size    = 0

  user_data             = file("ud-debian.sh")
}
module "drop_d10" {
  source                = "./terraform-modules/terraform-digitalocean-droplet/"
  application           = "vpn"
  environment           = "debian"
  label_order           = ["environment", "application", "name"]

  name                  = "d10sfo3"  # hostname: test-vpn-<NAME>-<DROPLET-COUNT -1>
  droplet_count         = 1
  ssh_keys              = [ digitalocean_ssh_key.do_vpn_ssh_key.id ]
  domain                = var.do_domain
  vpc_uuid              = data.digitalocean_vpc.default.id
  # "ams2" "ams3" "blr1" "fra1" "lon1" "nyc1" "nyc2" "nyc3" "sfo1" "sfo2" "sfo3" "sgp1" "tor1"
  region                = "sfo3" # var.do_region

  image_name            = "debian-10-x64"
  droplet_size          = "nano"
  monitoring            = true
  private_networking    = false
  ipv6                  = false
  floating_ip           = true
  block_storage_enabled = false
  block_storage_size    = 0

  user_data             = file("ud-debian.sh")
}


module "drop_f33" {
  source                = "./terraform-modules/terraform-digitalocean-droplet/"
  application           = "vpn"
  environment           = "fedora"
  label_order           = ["environment", "application", "name"]

  name                  = "f33sfo3"  # hostname: test-vpn-<NAME>-<DROPLET-COUNT -1>
  droplet_count         = 1
  ssh_keys              = [ digitalocean_ssh_key.do_vpn_ssh_key.id ]
  domain                = var.do_domain
  vpc_uuid              = data.digitalocean_vpc.default.id
  # "ams2" "ams3" "blr1" "fra1" "lon1" "nyc1" "nyc2" "nyc3" "sfo1" "sfo2" "sfo3" "sgp1" "tor1"
  region                = "sfo3" # var.do_region

  image_name            = "fedora-33-x64"
  droplet_size          = "nano"
  monitoring            = true
  private_networking    = false
  ipv6                  = false
  floating_ip           = true
  block_storage_enabled = false
  block_storage_size    = 0

  user_data             = file("ud-redhat.sh")
}
module "drop_f34" {
  source                = "./terraform-modules/terraform-digitalocean-droplet/"
  application           = "vpn"
  environment           = "fedora"
  label_order           = ["environment", "application", "name"]

  name                  = "f34sfo3"  # hostname: test-vpn-<NAME>-<DROPLET-COUNT -1>
  droplet_count         = 1
  ssh_keys              = [ digitalocean_ssh_key.do_vpn_ssh_key.id ]
  domain                = var.do_domain
  vpc_uuid              = data.digitalocean_vpc.default.id
  # "ams2" "ams3" "blr1" "fra1" "lon1" "nyc1" "nyc2" "nyc3" "sfo1" "sfo2" "sfo3" "sgp1" "tor1"
  region                = "sfo3" # var.do_region

  image_name            = "fedora-34-x64"
  droplet_size          = "nano"
  monitoring            = true
  private_networking    = false
  ipv6                  = false
  floating_ip           = true
  block_storage_enabled = false
  block_storage_size    = 0

  user_data             = file("ud-redhat.sh")
}

module "drop_u18" {
  source                = "./terraform-modules/terraform-digitalocean-droplet/"
  application           = "vpn"
  environment           = "ubuntu"
  label_order           = ["environment", "application", "name"]

  name                  = "u18sfo3"  # hostname: test-vpn-<NAME>-<DROPLET-COUNT -1>
  droplet_count         = 1
  ssh_keys              = [ digitalocean_ssh_key.do_vpn_ssh_key.id ]
  domain                = var.do_domain
  vpc_uuid              = data.digitalocean_vpc.default.id
  # "ams2" "ams3" "blr1" "fra1" "lon1" "nyc1" "nyc2" "nyc3" "sfo1" "sfo2" "sfo3" "sgp1" "tor1"
  region                = "sfo3" # var.do_region

  image_name            = "ubuntu-18-04-x64"
  droplet_size          = "nano"
  monitoring            = true
  private_networking    = false
  ipv6                  = false
  floating_ip           = true
  block_storage_enabled = false
  block_storage_size    = 0

  user_data             = file("ud-debian.sh")
}
module "drop_u20" {
  source                = "./terraform-modules/terraform-digitalocean-droplet/"
  application           = "vpn"
  environment           = "ubuntu"
  label_order           = ["environment", "application", "name"]

  name                  = "u20sfo3"  # hostname: test-vpn-<NAME>-<DROPLET-COUNT -1>
  droplet_count         = 1
  ssh_keys              = [ digitalocean_ssh_key.do_vpn_ssh_key.id ]
  domain                = var.do_domain
  vpc_uuid              = data.digitalocean_vpc.default.id
  # "ams2" "ams3" "blr1" "fra1" "lon1" "nyc1" "nyc2" "nyc3" "sfo1" "sfo2" "sfo3" "sgp1" "tor1"
  region                = "sfo3" # var.do_region

  image_name            = "ubuntu-20-04-x64"
  droplet_size          = "nano"
  monitoring            = true
  private_networking    = false
  ipv6                  = false
  floating_ip           = true
  block_storage_enabled = false
  block_storage_size    = 0

  user_data             = file("ud-debian.sh")
}
