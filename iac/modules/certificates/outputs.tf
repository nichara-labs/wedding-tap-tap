output "default_region" {
  description = "The ACM certificate created for the provider's region, covering the domain."
  value       = aws_acm_certificate.this[local.current_region].arn
}
output "extra_regions" {
  description = "The ACM certificates created for the additional regions, covering the domain."
  value = {
    for region, cert in aws_acm_certificate.this : region => cert.arn if region != local.current_region
  }
}
