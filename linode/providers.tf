// vpn-providers.tf -- define the vpn terraform providers
//================================================== PROVIDERS
# Configure the AWS Provider
terraform {
  required_providers {

    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
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
