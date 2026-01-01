terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.5"
    }
  }
  required_version = "~> 1.10"
}

resource "aws_apprunner_service" "main" {
  service_name = var.service_name

  source_configuration {
    authentication_configuration {
      access_role_arn = aws_iam_role.service.arn
    }
    image_repository {
      image_configuration {
        port                          = var.port
        runtime_environment_variables = var.env_vars
      }
      image_identifier      = "${var.repository_uri}:latest"
      image_repository_type = "ECR"
    }
    auto_deployments_enabled = false
  }

  auto_scaling_configuration_arn = aws_apprunner_auto_scaling_configuration_version.main.arn
  health_check_configuration {
    path     = var.health_check_path
    protocol = "HTTP"
  }

  instance_configuration {
    cpu               = 256 # 0.25vCPU
    instance_role_arn = aws_iam_role.instance_role.arn
    memory            = 512
  }

}

resource "aws_apprunner_auto_scaling_configuration_version" "main" {
  auto_scaling_configuration_name = var.service_name

  max_concurrency = 50
  max_size        = 1
  min_size        = 1
}
