// linode.tf -- spin up the vpn linode instances and define in DNS
//================================================== VARIABLES (in linode-vars.tf)
//================================================== PROVIDERS (in providers.tf)
provider "linode" {
  # Configuration options
}

//================================================== GENERATE KEYS AND SAVE
resource "tls_private_key" "linode_ssh_key" {
  algorithm = "RSA"
  rsa_bits  = "2048"
}

resource "local_file" "linode_pub_ssh_key" {
  content              = tls_private_key.linode_ssh_key.public_key_openssh
  filename             = "id_rsa.pub"
  directory_permission = "0755"
  file_permission      = "0600"
}

resource "local_file" "linode_priv_ssh_key" {
  content              = tls_private_key.linode_ssh_key.private_key_pem
  filename             = "id_rsa"
  directory_permission = "0755"
  file_permission      = "0600"
}

# there's really no need to know this password if using ssh -i private_key
resource "random_password" "linode_root_pass" {
  length           = 16
  special          = true
  override_special = "_%@"
}

resource "local_file" "root_passwd" {
  content              = random_password.linode_root_pass.result
  filename             = "root-passwd"
  directory_permission = "0755"
  file_permission      = "0600"
}
