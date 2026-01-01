variable "aliases" {
  description = "List of alternate domain names (CNAMEs) for the CloudFront distribution"
  type        = set(string)
}

variable "name" {
  description = "The name of the CloudFront distribution. Also used as the S3 bucket prefix."
  type        = string
}

variable "certificate_arn" {
  description = "The ARN of the ACM certificate for the CloudFront distribution. Must be in us-east-1."
  type        = string
}

variable "domain_name" {
  description = "DNS domain name of the backend service, for use as the origin."
  type        = string
}

variable "backend_path_pattern" {
  description = "Path pattern that determines which requests are routed to the backend, e.g. `/api/*`"
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
