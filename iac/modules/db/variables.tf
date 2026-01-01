variable "project_id" {
  description = "Neon project id"
  type        = string
}

variable "branch_name" {
  description = "The branch name that the database will be created in."
  type        = string
}

variable "database_name" {
  description = "Name of the database within the branch."
  type        = string
}
