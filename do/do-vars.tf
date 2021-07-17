// do-vars.tf -- spin up the vpn digital ocean droplets and define in DNS
//================================================== PROVIDERS
//================================================== VARIABLES (in terraform.tfvars)
variable "do_domain" {
  description = "DNS domain where droplets are running"
  type        = string
  default     = "do-vilain.com"
}
variable "do_region" {
  description = "region where droplet is running"
  type        = string
  default     =  "sfo3"
}

# https://docs.digitalocean.com/products/networking/vpc/
# Region CIDR reserved
#  AMS1  10.11.0.0/16
#  AMS2  10.14.0.0/16
#  AMS3  10.18.0.0/16
#  BLR1  10.47.0.0/16
#  FRA1  10.19.0.0/16
#  LON1  10.16.0.0/16
#  NYC1  10.10.0.0/16
#  NYC2  10.13.0.0/16
#  NYC3  10.17.0.0/16
#  SFO1  10.12.0.0/16
#  SFO2  10.46.0.0/16
#  SFO3  10.48.0.0/16
#  SGP1  10.15.0.0/16
#  TOR1  10.20.0.0/16
variable "do_vpc_cidr" {
  description = "common internet domain range for private VPC"
  type        = string
  default     = "10.10.4.0/24"
}