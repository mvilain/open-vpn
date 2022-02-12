// gcp-keys.tf -- define the vpn aws instances
//================================================== VARIABLES (in gcp-vars.tf)
//================================================== PROVIDERS (in gcp-providers.tf)
provider "google" {
  project = var.gcp_project
  region  = var.gcp_region
  zone    = var.gcp_zone
}

# https://registry.terraform.io/providers/hashicorp/google/latest/docs/data-sources/client_config
data "google_client_config" "default" {}
# data.google_client_config.default.project - The ID of the project to apply any resources to
# data.google_client_config.default.region - The region to operate under
# data.google_client_config.default.zone - The zone to operate under
# data.google_client_config.default.access_token - OAuth2 access token used by the client to authenticate


data "google_client_openid_userinfo" "me" {}
# data.google_client_openid_userinfo.me.email

//================================================== S3 BACKEND (in gcp-s3-backend.tf)
//================================================== GENERATE KEYS AND SAVE
resource "tls_private_key" "vpn_ssh_key" {
  algorithm = "RSA"
  rsa_bits  = "2048"
}

resource "local_file" "vpn_pub_ssh_key" {
  content              = tls_private_key.vpn_ssh_key.public_key_openssh
  filename             = "id_rsa.pub"
  directory_permission = "0755"
  file_permission      = "0600"
}

resource "local_file" "vpn_priv_ssh_key" {
  content              = tls_private_key.vpn_ssh_key.private_key_pem
  filename             = "id_rsa"
  directory_permission = "0755"
  file_permission      = "0600"
}

resource "google_os_login_ssh_public_key" "vpn_key" {
  user                 = data.google_client_openid_userinfo.me.email
  key                  = local_file.vpn_pub_ssh_key.filename
}
#id - The key pair name.
#arn - The key pair ARN.
#key_name - The key pair name
#key_pair_id - The key pair ID
#fingerprint - The MD5 public key fingerprint as specified in section 4 of RFC 4716
#tags_all
