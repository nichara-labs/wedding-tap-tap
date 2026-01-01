terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.8"
    }
  }
  required_version = "~> 1.10"
}

resource "aws_ecr_repository" "app" {
  name                 = var.repo_name
  force_delete         = true
  image_tag_mutability = "IMMUTABLE_WITH_EXCLUSION"

  image_tag_mutability_exclusion_filter {
    filter      = "latest*"
    filter_type = "WILDCARD"
  }

  image_tag_mutability_exclusion_filter {
    filter      = "cache*"
    filter_type = "WILDCARD"
  }
}

data "aws_ecr_lifecycle_policy_document" "app" {
  rule {
    priority    = 1
    description = "Keep only the latest 5 images. Note: includes some cache images."

    selection {
      tag_status   = "any"
      count_type   = "imageCountMoreThan"
      count_number = 5
    }
  }
}

resource "aws_ecr_lifecycle_policy" "app" {
  repository = aws_ecr_repository.app.name

  policy = data.aws_ecr_lifecycle_policy_document.app.json
}
