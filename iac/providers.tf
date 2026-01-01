provider "aws" {
  region              = var.region
  allowed_account_ids = var.allowed_account_ids
  default_tags {
    tags = {
      Project = var.project_name
    }
  }
}

provider "neon" {
  api_key = data.aws_ssm_parameter.neon_api_key.value
}

provider "cloudflare" {
  api_token = data.aws_ssm_parameter.cloudflare_api_token.value
}

data "aws_ssm_parameter" "neon_api_key" {
  name = "/infra/neon/api_key"
}

data "aws_ssm_parameter" "cloudflare_api_token" {
  name = "/infra/cloudflare/api_token"
}

data "cloudflare_zone" "zone" {
  zone_id = var.cloudflare_zone_id
}
