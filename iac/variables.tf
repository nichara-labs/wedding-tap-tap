variable "s3_state_bucket" {
  description = "The name of the S3 bucket used for the state files."
  type        = string
}

variable "project_name" {
  description = "Used for tagging/naming resources. Use dashes to separate words."
  type        = string
}

variable "cloudflare_zone_id" {
  description = "The Cloudflare zone ID where the DNS records will be created."
  type        = string
}
variable "allowed_account_ids" {
  description = "List of AWS account IDs allowed to apply this Terraform configuration."
  type        = list(string)
}

variable "region" {
  description = "The AWS region where the resources will be deployed."
  type        = string
}

variable "env" {
  description = "Name of the deployment environment. Used for the name of the Neon branch as well as the subdomain (omitted for prod)."
  type        = string
  validation {
    condition     = contains(["dev", "uat", "prod"], var.env)
    error_message = "Invalid environment name"
  }
}

variable "neon_project_id" {
  description = "The Neon project ID where the branch will be created in. Note: A branch in Neon refers to a separate database (which can contain many schemas)."
  type        = string
}

variable "backend_port" {
  description = "The port on which the backend service will listen."
  type        = number
}

variable "api_path_pattern" {
  description = "Cloudfront path pattern for requests that should be routed to the backend API, e.g. '/api/*'"
  type        = string
}

variable "backend_health_check_path" {
  description = "The path to the backend health check endpoint."
  type        = string
}

variable "google_tag_id" {
  description = "The Google Tag ID e.g. GT-XXXXXXX."
  type        = string
}

variable "gt_gateway_pattern" {
  description = "The path pattern for requests that Cloudfront will route to the Google Tag Gateway, e.g. /abcd/*"
  type        = string
}
