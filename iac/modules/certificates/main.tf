terraform {
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 5.8"
    }
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.5"
    }
  }
  required_version = "~> 1.10"
}

data "aws_region" "current" {}
