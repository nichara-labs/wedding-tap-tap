terraform {
  required_providers {
    neon = {
      source  = "kislerdm/neon"
      version = "~> 0.9"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.7"
    }
  }
  required_version = "~> 1.10"
}

data "neon_project" "main" {
  id = var.project_id
}

resource "neon_branch" "main" {
  name       = var.branch_name
  project_id = var.project_id
}

resource "neon_endpoint" "main" {
  project_id               = var.project_id
  branch_id                = neon_branch.main.id
  pooler_enabled           = false
  type                     = "read_write"
  autoscaling_limit_max_cu = 0.25
  autoscaling_limit_min_cu = 0.25
}

resource "neon_database" "main" {
  project_id = var.project_id
  name       = var.database_name
  owner_name = data.neon_project.main.database_user
  branch_id  = neon_branch.main.id
}
