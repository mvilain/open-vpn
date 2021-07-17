// do.tf -- spin up the vpn digital ocean instances and define in DNS
//================================================== VARIABLES (in do-vars.tf)
//================================================== PROVIDERS (in providers.tf)
provider "digitalocean" {
  # Configuration options
}

//================================================== GENERATE KEYS AND SAVE
resource "tls_private_key" "do_ssh_key" {
  algorithm = "RSA"
  rsa_bits  = "2048"
}

resource "local_file" "do_pub_ssh_key" {
  content              = tls_private_key.do_ssh_key.public_key_openssh
  filename             = "id_rsa.pub"
  directory_permission = "0755"
  file_permission      = "0600"
}

resource "local_file" "do_priv_ssh_key" {
  content              = tls_private_key.do_ssh_key.private_key_pem
  filename             = "id_rsa"
  directory_permission = "0755"
  file_permission      = "0600"
}

resource "digitalocean_ssh_key" "do_vpn_ssh_key" {
  name                 = "vpn ssh key"
  public_key           = chomp(tls_private_key.do_ssh_key.public_key_openssh)
}
# outputs:
# id - The unique ID of the key
# name - The name of the SSH key
# public_key - The text of the public key
# fingerprint - The fingerprint of the SSH key
