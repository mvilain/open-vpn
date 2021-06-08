// linode-vars.tf -- spin up the vpn linode instances and define in DNS
//================================================== VARIABLES (in terraform.tfvars)
variable "linode_region" {
  description = "region where linode is running"
  type        = string
  default     =  "us-west"
}
variable "linode_domain" {
  description = "DNS domain where linodes are running"
  type        = string
  default     = "lin-vilain.com"
}
