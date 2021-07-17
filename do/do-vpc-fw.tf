// do-vpc-fw.tf -- define the digital ocean vpc's firewall
//================================================== PROVIDERS (in providers.tf)
//================================================== VARIABLES (in do-vars.tf)
//================================================== GENERATE KEYS AND SAVE (in do-keys.tf)
// ================================================= VPC + FIREWALL

# get the default VPC for region
data "digitalocean_vpc" "default" {
  region      = var.do_region
}


resource "digitalocean_firewall" "vpn-fw" {
  name = "vpn-fw"

// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> list droplets here
  droplet_ids = [ module.drop_c7.id[0] ]
// <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
  outbound_rule {
    protocol              = "tcp"
    port_range            = "1-65535"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
  outbound_rule {
    protocol              = "udp"
    port_range            = "1-65535"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
  outbound_rule {
    protocol              = "icmp"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

#}
#
#resource "digitalocean_firewall" "vpn-ingress" {
#  name = "vpn-ingress"
#
#  droplet_ids = [ module.drop_c7.id[0] ]

# http
  inbound_rule {
    protocol         = "tcp"
    port_range       = "80"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }
# https
  inbound_rule {
    protocol         = "tcp"
    port_range       = "443"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }


# ssh att
  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = ["75.25.136.0/24"]
  }

# ssh mul_la
  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = ["89.45.90.0/24"]
  }

# ssh mul_sf
  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = ["199.116.112.0/21"]
  }

# ssh mul_sj198128
  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = ["198.54.128.0/21"]
  }

# ssh mul_sj1982
  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = ["198.54.134.0/24"]
  }

# ssh mul_sj199
  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = ["199.116.118.0/24"]
  }

# ssh mul_la
  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = ["37.120.147.0/24"]
  }

# ssh mul_sf
  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = ["206.189.0.0/16"]
  }

# ssh mul_nv
  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = ["185.242.5.0/24"]
  }

# ssh mul_tx
  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = ["96.44.128.0/18"]
  }

# ssh mul_ut
  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = ["209.95.32.0/19"]
  }

# ssh mul_wa192
  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = ["192.252.208.0/20"]
  }

# ssh mul_wa199
  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = ["199.229.248.0/21"]
  }

}
