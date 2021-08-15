// gcp-vars.tf -- spin up the vpn in google compute and define in DNS
//================================================== PROVIDERS
//================================================== VARIABLES (in terraform.tfvars)

variable "gcp_domain" {
  description = "DNS domain where compute are running"
  type        = string
  default     = "gcp-vilain.com"
}
variable "gcp_region" {
  description = "region where compute is running"
  type        = string
  default     =  "us-central1"
}
variable "gcp_zone" {
  description = "zone in region where compute is running"
  type        = string
  default     =  "us-central1-c"
}

variable "gcp_project" {
  description = "project that uses this configuration"
  type        = string
  default     = "My Project"
}
