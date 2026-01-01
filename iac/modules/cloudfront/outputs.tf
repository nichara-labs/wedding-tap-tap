output "cloudfront_domain" {
  value       = aws_cloudfront_distribution.cdn.domain_name
  description = "CloudFront domain"
}

output "s3_bucket" {
  value       = aws_s3_bucket.site.bucket
  description = "S3 bucket name for the static site"
}

output "id" {
  value       = aws_cloudfront_distribution.cdn.id
  description = "CloudFront distribution ID"
}
