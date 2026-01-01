variable "service_name" {
  description = "The name for the App Runner service."
  type        = string
}

variable "env_vars" {
  description = "List of environment variables to set for the instance."
  type        = map(string)
  default     = {}
}

variable "managed_policies" {
  description = "List of managed policy ARNs to attach to the instance role."
  type        = set(string)
}

variable "inline_policies" {
  description = "Map of inline policy names to lists of statements to attach to the instance role."
  type = map(list(object({
    effect    = string
    actions   = list(string)
    resources = list(string)
  })))
}

variable "repository_uri" {
  description = "Repository URI to use (without the tag) for the instance, e.g. `aws_account_id.dkr.ecr.region.amazonaws.com/app/frontend`. Note that the `latest` tag will be used; this fixes the issue of OpenTofu having to wait for deployment."
  type        = string
}

variable "port" {
  description = "Port on which the instance will listen"
  type        = number
}

variable "health_check_path" {
  description = "The path to the health check endpoint."
  type        = string
}
