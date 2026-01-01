locals {
  current_region = data.aws_region.current.region
  regions        = setunion(toset([local.current_region]), var.extra_regions)

  # ACM produces identical CNAME challenge records across regions (as well as subdomains). However, Cloudflare does not allow duplicate CNAME records.
  # We use the provider's region challenge records for all the rest.
  dvo = one(aws_acm_certificate.this[local.current_region].domain_validation_options)

  challenge_record = {
    # ACM adds trailing dots to the name/value, but Cloudflare strips them
    # This causes the resource to be continually detected as new
    # We strip them here to fix this
    name    = trimsuffix(local.dvo.resource_record_name, ".")
    type    = local.dvo.resource_record_type
    content = trimsuffix(local.dvo.resource_record_value, ".")
  }
}

resource "aws_acm_certificate" "this" {
  for_each          = local.regions
  domain_name       = var.fqdn
  validation_method = "DNS"
  region            = each.key
  lifecycle {
    create_before_destroy = true
  }
}

resource "cloudflare_dns_record" "validation" {
  zone_id = var.zone_id

  # ACM names include the base domain and end with a dot
  # We need to remove them for Cloudflare
  name = local.challenge_record.name

  ttl     = 1 # auto
  type    = local.challenge_record.type
  comment = "DNS validation - Managed by OpenTofu"
  content = local.challenge_record.content
  proxied = false
}


# Wait until all certificate are issued
resource "aws_acm_certificate_validation" "this" {
  for_each                = local.regions
  certificate_arn         = aws_acm_certificate.this[each.key].arn
  region                  = each.key
  validation_record_fqdns = [cloudflare_dns_record.validation.name]
}
