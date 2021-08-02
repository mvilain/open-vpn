// vpn-providers.tf -- define the vpn terraform providers
//================================================== PROVIDERS
terraform {
  required_providers {

     aws = {
       source  = "hashicorp/aws"
       version = "~> 3.0"
     }

    digitalocean = {
      source = "digitalocean/digitalocean"
      version = "1.22.2"
    }


      google = {
        source = "hashicorp/google"
        version = "3.76.0"
      }


     linode = {
       source  = "linode/linode"
       version = ">= 1.16.0"
     }

    local = {
      source  = "hashicorp/local"
      version = "2.0.0"
    }

    tls = {
      source  = "hashicorp/tls"
      version = "3.0.0"
    }

    random = {
      source  = "hashicorp/random"
      version = "3.0.0"
    }
  }
}
