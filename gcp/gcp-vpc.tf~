// aws-vpc.tf -- define the vpn aws vpc
// ================================================= NETWORK+SUBNETS+ACLs
data "aws_vpc" "default" {
  default    = true
}

#data "aws_subnet_ids" "default" {
#vpc_id    = data.aws_vpc.default.id
#}
# data.aws_subnet_ids.default.ids lists region's default subnet ids

## data "aws_availability_zones" "available" {
##   state    = "available"
## }
### data.aws_availability_zones.available.names is list region's availability zones
### data.aws_availability_zones.available.zone_ids is list region's availability zone ids

resource "aws_vpc" "vpn_vpc" {
  cidr_block           = "192.168.0.0/16"
  enable_dns_hostnames = true

  tags = {
    Name      = "vpn-vpc",
    Terraform = "True"
  }
}

resource "aws_subnet" "vpn_subnet" {
  vpc_id                  = aws_vpc.vpn_vpc.id
  cidr_block              = "192.168.10.0/24"
  map_public_ip_on_launch = true
  availability_zone       = var.aws_avz[0]

  tags = {
    Name      = "vpn-subnet",
    Terraform = "True"
  }
}

resource "aws_internet_gateway" "vpn_gw" {
  vpc_id               = aws_vpc.vpn_vpc.id

  tags = {
    Name = "vpn-gw",
    Terraform = "True"
  }
}

resource "aws_route_table" "vpn_rtb" {
  vpc_id = aws_vpc.vpn_vpc.id
  route {
    cidr_block             = "0.0.0.0/0"
    gateway_id             = aws_internet_gateway.vpn_gw.id
  }

  tags = {
    Name      = "vpn-rtb",
    Terraform = "True"
  }
}
resource "aws_route_table_association" "github_subnet_rtb" {
  subnet_id      = aws_subnet.vpn_subnet.id
  route_table_id = aws_route_table.vpn_rtb.id
}

## apply network ACLs to VPC to restrict access to entire VPC
## rather Security Groups which are per instance
## sadly network_acl_rules don't take descriptions
##
resource "aws_network_acl" "vpn_acl" {
  vpc_id      = aws_vpc.vpn_vpc.id
  subnet_ids  = [ aws_subnet.vpn_subnet.id ]
  tags = {
    Name      = "vpn-acl",
    Terraform = "True"
  }
}

## default network_acl settings
##
resource "aws_network_acl_rule" "vpn_acl_egress" {
  network_acl_id = aws_network_acl.vpn_acl.id
  rule_number    = 200
  egress         = true
  protocol       = "-1"
  rule_action    = "allow"
  cidr_block     = "0.0.0.0/0"
  from_port      = 0
  to_port        = 0
}
resource "aws_network_acl_rule" "vpn_acl_http" {
  network_acl_id = aws_network_acl.vpn_acl.id
  rule_number    = 100
  egress         = false
  protocol       = "-1"
  rule_action    = "allow"
  cidr_block     = "0.0.0.0/0"
  from_port      = 0
  to_port        = 0
}
