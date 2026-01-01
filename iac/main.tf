terraform {
  backend "s3" {
    bucket       = var.s3_state_bucket
    key          = "${var.project_name}/opentofu.tfstate"
    region       = "ap-southeast-1"
    use_lockfile = true
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.5"
    }
    neon = {
      source  = "kislerdm/neon"
      version = "~> 0.9"
    }
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 5.8"
    }
  }
  required_version = "~> 1.10"
}
