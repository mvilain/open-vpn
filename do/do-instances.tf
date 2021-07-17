// do-instances.tf -- spin up the vpn digital ocean droplets and define in DNS
//================================================== PROVIDERS (in providers.tf)
//================================================== VARIABLES (in do-vars.tf)
//================================================== GENERATE KEYS AND SAVE (in do-keys.tf)
// ================================================= VPC + FIREWALL (in do-vpc-fw.tf)
//================================================== INSTANCES

# terraform-digitalocean-droplet
# inputs:
#  password  - root password                              [default: NONE ]
#  ssh_key   - public ssh key for setting authorize_hosts [default: NONE ]
#  image     - Image type used to create instance         [default: "do/ubuntu18.04"]
#  region    - region where instance will run             [default: "francisco-3"]
#                amsterdam-2
#                amsterdam-3
#                bangalore-1
#                frankfurt-1
#                london
#                newyork-1
#                newyork-2
#                newyork-3
#                francisco-1
#                francisco-2
#                francisco-3
#                singapore-1
#                toronto-1
#   type      - image size to use                          [default: "s-1vcpu-1gb"]
#                s-1vcpu-1gb
#                s-2vcpu-2gb
#                s-2vcpu-4gb
#                s-4vcpu-8gb
#                c2
#                c4
#                m-2vcpu-16gb
#                g-2vcpu-8gb
#                gd-2vcpu-8gb
#   name      - name used to create the instance and hostname  [default: ""]
#   domain    - pre-existing DNS domain used to assign host IP  [default: "example.com"]
#   user-data - user-data cloud-init script to run on boot   [default: NONE ]
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
  environment           = "test"
  label_order           = ["environment", "application", "name"]

  name                  = "c7sfo3"  # hostname: test-vpn-<NAME>-<DROPLET-COUNT -1>
  droplet_count         = 1
  ssh_keys              = [ digitalocean_ssh_key.do_vpn_ssh_key.id ]
  domain                = var.do_domain
  vpc_uuid              = data.digitalocean_vpc.default.id
  # "ams2" "ams3" "blr1" "fra1" "lon1" "nyc1" "nyc2" "nyc3" "sfo1" "sfo2" "sfo3" "sgp1" "tor1"
  region                = var.do_region  # "sfo3"

  image_name            = "centos-7-x64"
  droplet_size          = "nano"
  monitoring            = false
  private_networking    = false
  ipv6                  = false
  floating_ip           = true
  block_storage_enabled = true
  block_storage_size    = 5

  user_data             = file("ud-centos7.sh")
}
module "drop_c8" {
  source                = "./terraform-modules/terraform-digitalocean-droplet/"
  application           = "vpn"
  environment           = "test"
  label_order           = ["environment", "application", "name"]

  name                  = "c8sfo3"  # hostname: test-vpn-<NAME>-<DROPLET-COUNT -1>
  droplet_count         = 1
  ssh_keys              = [ digitalocean_ssh_key.do_vpn_ssh_key.id ]
  domain                = var.do_domain
  vpc_uuid              = data.digitalocean_vpc.default.id
  # "ams2" "ams3" "blr1" "fra1" "lon1" "nyc1" "nyc2" "nyc3" "sfo1" "sfo2" "sfo3" "sgp1" "tor1"
  region                = var.do_region  # "sfo3"

  image_name            = "centos-8-x64"
  droplet_size          = "nano"
  monitoring            = false
  private_networking    = false
  ipv6                  = false
  floating_ip           = true
  block_storage_enabled = true
  block_storage_size    = 5

  user_data             = file("ud-centos8.sh")
}


module "drop_d9" {
  source                = "./terraform-modules/terraform-digitalocean-droplet/"
  application           = "vpn"
  environment           = "test"
  label_order           = ["environment", "application", "name"]

  name                  = "d9sfo3"  # hostname: test-vpn-<NAME>-<DROPLET-COUNT -1>
  droplet_count         = 1
  ssh_keys              = [ digitalocean_ssh_key.do_vpn_ssh_key.id ]
  domain                = var.do_domain
  vpc_uuid              = data.digitalocean_vpc.default.id
  # "ams2" "ams3" "blr1" "fra1" "lon1" "nyc1" "nyc2" "nyc3" "sfo1" "sfo2" "sfo3" "sgp1" "tor1"
  region                = var.do_region  # "sfo3"

  image_name            = "debian-9-x64"
  droplet_size          = "nano"
  monitoring            = false
  private_networking    = false
  ipv6                  = false
  floating_ip           = true
  block_storage_enabled = true
  block_storage_size    = 5

  user_data             = file("ud-debian.sh")
}
module "drop_d10" {
  source                = "./terraform-modules/terraform-digitalocean-droplet/"
  application           = "vpn"
  environment           = "test"
  label_order           = ["environment", "application", "name"]

  name                  = "d10sfo3"  # hostname: test-vpn-<NAME>-<DROPLET-COUNT -1>
  droplet_count         = 1
  ssh_keys              = [ digitalocean_ssh_key.do_vpn_ssh_key.id ]
  domain                = var.do_domain
  vpc_uuid              = data.digitalocean_vpc.default.id
  # "ams2" "ams3" "blr1" "fra1" "lon1" "nyc1" "nyc2" "nyc3" "sfo1" "sfo2" "sfo3" "sgp1" "tor1"
  region                = var.do_region  # "sfo3"

  image_name            = "debian-10-x64"
  droplet_size          = "nano"
  monitoring            = false
  private_networking    = false
  ipv6                  = false
  floating_ip           = true
  block_storage_enabled = true
  block_storage_size    = 5

  user_data             = file("ud-debian.sh")
}


module "drop_f33" {
  source                = "./terraform-modules/terraform-digitalocean-droplet/"
  application           = "vpn"
  environment           = "test"
  label_order           = ["environment", "application", "name"]

  name                  = "f33sfo3"  # hostname: test-vpn-<NAME>-<DROPLET-COUNT -1>
  droplet_count         = 1
  ssh_keys              = [ digitalocean_ssh_key.do_vpn_ssh_key.id ]
  domain                = var.do_domain
  vpc_uuid              = data.digitalocean_vpc.default.id
  # "ams2" "ams3" "blr1" "fra1" "lon1" "nyc1" "nyc2" "nyc3" "sfo1" "sfo2" "sfo3" "sgp1" "tor1"
  region                = var.do_region  # "sfo3"

  image_name            = "fedora-33-x64"
  droplet_size          = "nano"
  monitoring            = false
  private_networking    = false
  ipv6                  = false
  floating_ip           = true
  block_storage_enabled = true
  block_storage_size    = 5

  user_data             = file("ud-redhat.sh")
}
module "drop_f34" {
  source                = "./terraform-modules/terraform-digitalocean-droplet/"
  application           = "vpn"
  environment           = "test"
  label_order           = ["environment", "application", "name"]

  name                  = "f34sfo3"  # hostname: test-vpn-<NAME>-<DROPLET-COUNT -1>
  droplet_count         = 1
  ssh_keys              = [ digitalocean_ssh_key.do_vpn_ssh_key.id ]
  domain                = var.do_domain
  vpc_uuid              = data.digitalocean_vpc.default.id
  # "ams2" "ams3" "blr1" "fra1" "lon1" "nyc1" "nyc2" "nyc3" "sfo1" "sfo2" "sfo3" "sgp1" "tor1"
  region                = var.do_region  # "sfo3"

  image_name            = "fedora-34-x64"
  droplet_size          = "nano"
  monitoring            = false
  private_networking    = false
  ipv6                  = false
  floating_ip           = true
  block_storage_enabled = true
  block_storage_size    = 5

  user_data             = file("ud-redhat.sh")
}

module "drop_u18" {
  source                = "./terraform-modules/terraform-digitalocean-droplet/"
  application           = "vpn"
  environment           = "test"
  label_order           = ["environment", "application", "name"]

  name                  = "u18sfo3"  # hostname: test-vpn-<NAME>-<DROPLET-COUNT -1>
  droplet_count         = 1
  ssh_keys              = [ digitalocean_ssh_key.do_vpn_ssh_key.id ]
  domain                = var.do_domain
  vpc_uuid              = data.digitalocean_vpc.default.id
  # "ams2" "ams3" "blr1" "fra1" "lon1" "nyc1" "nyc2" "nyc3" "sfo1" "sfo2" "sfo3" "sgp1" "tor1"
  region                = var.do_region  # "sfo3"

  image_name            = "ubuntu-18-04-x64"
  droplet_size          = "nano"
  monitoring            = false
  private_networking    = false
  ipv6                  = false
  floating_ip           = true
  block_storage_enabled = true
  block_storage_size    = 5

  user_data             = file("ud-debian.sh")
}
module "drop_u20" {
  source                = "./terraform-modules/terraform-digitalocean-droplet/"
  application           = "vpn"
  environment           = "test"
  label_order           = ["environment", "application", "name"]

  name                  = "u20sfo3"  # hostname: test-vpn-<NAME>-<DROPLET-COUNT -1>
  droplet_count         = 1
  ssh_keys              = [ digitalocean_ssh_key.do_vpn_ssh_key.id ]
  domain                = var.do_domain
  vpc_uuid              = data.digitalocean_vpc.default.id
  # "ams2" "ams3" "blr1" "fra1" "lon1" "nyc1" "nyc2" "nyc3" "sfo1" "sfo2" "sfo3" "sgp1" "tor1"
  region                = var.do_region  # "sfo3"

  image_name            = "ubuntu-20-04-x64"
  droplet_size          = "nano"
  monitoring            = false
  private_networking    = false
  ipv6                  = false
  floating_ip           = true
  block_storage_enabled = true
  block_storage_size    = 5

  user_data             = file("ud-debian.sh")
}
