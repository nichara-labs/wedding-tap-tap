locals {
  cloudfront_cert_region = "us-east-1" # Cloudfront requires ACM certificates to be created here
  site_fqdn              = "${var.subdomain}.${data.cloudflare_zone.zone.name}"
}

module "certificates" {
  source        = "./modules/certificates"
  fqdn          = local.site_fqdn
  zone_id       = var.cloudflare_zone_id
  extra_regions = [local.cloudfront_cert_region]
}

module "ecr" {
  source    = "./modules/ecr"
  repo_name = "${var.project_name}/backend"
}

module "app_runner" {
  source            = "./modules/app_runner"
  repository_uri    = module.ecr.repository_url
  service_name      = var.project_name
  health_check_path = var.backend_health_check_path
  managed_policies  = ["arn:aws:iam::aws:policy/AmazonSSMReadOnlyAccess"]
  inline_policies   = {}
  port              = var.backend_port

}

module "cloudfront" {
  source               = "./modules/cloudfront"
  name                 = var.project_name
  aliases              = [local.site_fqdn]
  certificate_arn      = module.certificates.extra_regions[local.cloudfront_cert_region]
  domain_name          = module.app_runner.service_url
  backend_path_pattern = var.api_path_pattern
}

module "dns" {
  source  = "./modules/dns"
  zone_id = var.cloudflare_zone_id
  name    = var.subdomain
  type    = "CNAME"
  content = module.cloudfront.cloudfront_domain
  proxied = false
}
