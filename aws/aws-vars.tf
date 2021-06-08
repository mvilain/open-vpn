#alma8...centos7...centos8...debian9...debian10...ubuntu16...ubuntu18...ubuntu20...[done]
// generated from vpn-aws-vars.j2 -- jinja2 template to provide vpn aws instances
// [template for aws-list-gold-ami.py]
//================================================== VARIABLES
variable "aws_region" {
  description = "default region to setup all resources"
  type        = string
  default     = "us-east-2"
}
variable "aws_domain" {
  description = "DNS domain where aws instances are running"
  type        = string
  default     = "aws-vilain.com"
}

#========================================== AVAILABILTY ZONES
variable "aws_avz" {
  description = "us-east-2-zones"
  type        = list(string)
  default     = ["us-east-2a", "us-east-2b", "us-east-2c"]
}

#========================================== alma8 2021-03-31T16:50:01.000Z
variable "aws_alma8_ami" {
  description = "us-east-2--AlmaLinux 8.3 (AlmaLinux8) (alma8) (alma 8.3) Minimal Install Golden AMI Template"
  type        = string
  default     = "ami-01a87a7d55032db2e"
}
variable "aws_alma8_name" {
  description = "name for alma8 instance"
  type        = string
  default     = "vpn-alma8"
}
variable "aws_alma8_tag" {
  description = "tag for alma8 instance"
  type        = string
  default     = "vpn alma8"
}

#========================================== centos7 2020-03-09T21:54:47.000Z
variable "aws_centos7_ami" {
  description = "us-east-2--CentOS Linux 7 x86_64 HVM EBS ENA 2002_01"
  type        = string
  default     = "ami-01e36b7901e884a10"
}
variable "aws_centos7_name" {
  description = "name for centos7 instance"
  type        = string
  default     = "vpn-centos7"
}
variable "aws_centos7_tag" {
  description = "tag for centos7 instance"
  type        = string
  default     = "vpn centos7"
}

#========================================== centos8 2021-04-04T15:49:32.000Z
variable "aws_centos8_ami" {
  description = "us-east-2--CentOS 8.3 (CentOS8) (cent8) (cent 8.3) Minimal Install Golden AMI Template"
  type        = string
  default     = "ami-082a036ec7c372e4c"
}
variable "aws_centos8_name" {
  description = "name for centos8 instance"
  type        = string
  default     = "vpn-centos8"
}
variable "aws_centos8_tag" {
  description = "tag for centos8 instance"
  type        = string
  default     = "vpn centos8"
}

#========================================== debian9 2021-04-05T15:18:48.000Z
variable "aws_debian9_ami" {
  description = "us-east-2--Debian 9 (Debian Stretch) (debian9) Golden Image Template"
  type        = string
  default     = "ami-0c18820215678d337"
}
variable "aws_debian9_name" {
  description = "name for debian9 instance"
  type        = string
  default     = "vpn-debian9"
}
variable "aws_debian9_tag" {
  description = "tag for debian9 instance"
  type        = string
  default     = "vpn debian9"
}

#========================================== debian10 2021-04-05T16:06:27.000Z
variable "aws_debian10_ami" {
  description = "us-east-2--Debian 10 (Debian Buster) (debian10) Debian 10 Golden Image Template"
  type        = string
  default     = "ami-0a449b766e034390d"
}
variable "aws_debian10_name" {
  description = "name for debian10 instance"
  type        = string
  default     = "vpn-debian10"
}
variable "aws_debian10_tag" {
  description = "tag for debian10 instance"
  type        = string
  default     = "vpn debian10"
}

#========================================== ubuntu16 2021-04-05T16:32:22.000Z
variable "aws_ubuntu16_ami" {
  description = "us-east-2--Golden image (gold ami) template for Ubuntu Server 16.04 LTS (Ubuntu 16.04) (Ubuntu 16)"
  type        = string
  default     = "ami-0a65caa9c575c1c0c"
}
variable "aws_ubuntu16_name" {
  description = "name for ubuntu16 instance"
  type        = string
  default     = "vpn-ubuntu16"
}
variable "aws_ubuntu16_tag" {
  description = "tag for ubuntu16 instance"
  type        = string
  default     = "vpn ubuntu16"
}

#========================================== ubuntu18 2021-05-14T22:38:24.000Z
variable "aws_ubuntu18_ami" {
  description = "us-east-2--Canonical, Ubuntu, 18.04 LTS, amd64 bionic image build on 2021-05-14"
  type        = string
  default     = "ami-0baa47a966030510f"
}
variable "aws_ubuntu18_name" {
  description = "name for ubuntu18 instance"
  type        = string
  default     = "vpn-ubuntu18"
}
variable "aws_ubuntu18_tag" {
  description = "tag for ubuntu18 instance"
  type        = string
  default     = "vpn ubuntu18"
}

#========================================== ubuntu20 2021-04-04T13:40:37.000Z
variable "aws_ubuntu20_ami" {
  description = "us-east-2--Ubuntu Server 20.04 LTS (Ubuntu 20.04 LTS ) (Ubuntu 20) Focal Fossa"
  type        = string
  default     = "ami-06b3455df6cbbf3a2"
}
variable "aws_ubuntu20_name" {
  description = "name for ubuntu20 instance"
  type        = string
  default     = "vpn-ubuntu20"
}
variable "aws_ubuntu20_tag" {
  description = "tag for ubuntu20 instance"
  type        = string
  default     = "vpn ubuntu20"
}


