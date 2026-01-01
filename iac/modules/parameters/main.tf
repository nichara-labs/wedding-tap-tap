terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.5"
    }
  }
  required_version = "~> 1.10"
}

resource "aws_ssm_parameter" "public_parameters" {
  for_each = var.public

  name  = each.key
  type  = "String"
  value = each.value
}

resource "aws_ssm_parameter" "secret_parameters" {
  for_each = var.secret

  name  = each.key
  type  = "SecureString"
  value = each.value
}
