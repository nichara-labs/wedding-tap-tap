output "repository_name" {
  description = "The ECR repository name e.g. project-name/backend."
  value       = module.ecr.repository_name
}

output "site_s3_bucket" {
  description = "The S3 bucket name for the static site."
  value       = module.cloudfront.s3_bucket
}

output "cloudfront_distribution_id" {
  value       = module.cloudfront.id
  description = "The CloudFront distribution ID. Used for invalidation."
}

output "app_runner_service_arn" {
  value       = module.app_runner.service_arn
  description = "The App Runner service ARN. Used to manually start an App Runner deployment."
}
