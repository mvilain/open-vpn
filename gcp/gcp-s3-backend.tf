// aws-s3-backend.tf -- define the s3 backend for terraform state
//================================================== S3 BACKEND
#resource "aws_s3_bucket" "tf-backend" {
#  bucket = "mvilain-prod-tfstate-backend"
#  acl    = "private"
#
##  lifecycle {
##    prevent_destroy = true
##  }
#  
#  versioning {
#  enabled = true
#  }
#
#  server_side_encryption_configuration {
#    rule {
#      apply_server_side_encryption_by_default {
#        sse_algorithm = "AES256"
#      }
#    }
#  }
#}
#
#resource "aws_dynamodb_table" "tf_locks" {
#  name         = "mvilain-prod-tfstate-locks"
#  billing_mode = "PAY_PER_REQUEST"
#  hash_key     = "LockID"
#
#  attribute {
#    name       = "LockID"
#    type       = "S"
#  }
#}
#
#terraform {
#  backend "local" {
#    path = "./terraform.tfstate"
#  }
#}
#terraform {
#    backend "s3" {
#    bucket         = "mvilain-prod-tfstate-backend"
#    key            = "global/s3/terraform.tfstate"
#    region         = "us-east-2"
#    dynamodb_table = "mvilain-prod-tfstate-locks"
#    encrypt        = true
#  }
#}
#terraform {
#  backend "s3" {
#    bucket         = "mvilain-prod-tfstate-backend"
#    key            = "vpc/terraform.tfstate"
#    region         = "us-east-2"
#    profile        = "tesera"
#    dynamodb_table = "mvilain-prod-tfstate-locks"
#    encrypt        = true
#    kms_key_id     = "arn:aws:kms:us-east-2:<account_id>:key/<key_id>"
#  }
#}
