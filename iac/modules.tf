locals {
  project_name_underscore = replace(var.project_name, "-", "_")
  cloudfront_cert_region  = "us-east-1" # Cloudfront requires ACM certificates to be created here
  site_fqdn               = "${var.env == "prod" ? "" : "${var.env}."}${data.cloudflare_zone.zone.name}"
}

module "db" {
  source        = "./modules/db"
  project_id    = var.neon_project_id
  branch_name   = var.env
  database_name = "${var.project_name}_${var.env}"
}

module "session" {
  source = "./modules/session"
}

module "certificates" {
  source        = "./modules/certificates"
  fqdn          = local.site_fqdn
  zone_id       = var.cloudflare_zone_id
  extra_regions = [local.cloudfront_cert_region]
}

module "ssm_parameters" {
  source = "./modules/parameters"

  public = {
    "/${local.project_name_underscore}/db/hostname"          = module.db.hostname
    "/${local.project_name_underscore}/db/hostname_unpooled" = module.db.hostname_unpooled
    # We create the DB in IaC, because for some reason Alembic can't
    "/${local.project_name_underscore}/db/name"     = module.db.database_name
    "/${local.project_name_underscore}/db/port"     = module.db.port
    "/${local.project_name_underscore}/db/username" = module.db.username
  }

  secret = {
    "/${local.project_name_underscore}/db/password"         = module.db.password
    "/${local.project_name_underscore}/session/signing_key" = module.session.signing_key
  }
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
  depends_on        = [module.ssm_parameters]

}

module "cloudfront" {
  source               = "./modules/cloudfront"
  name                 = var.project_name
  aliases              = [local.site_fqdn]
  certificate_arn      = module.certificates.extra_regions[local.cloudfront_cert_region]
  domain_name          = module.app_runner.service_url
  backend_path_pattern = var.api_path_pattern
  google_tag_id        = var.google_tag_id
  gt_gateway_pattern   = var.gt_gateway_pattern
}

module "dns" {
  source  = "./modules/dns"
  zone_id = var.cloudflare_zone_id
  name    = var.env == "prod" ? "" : var.env
  type    = "CNAME"
  content = module.cloudfront.cloudfront_domain
  proxied = false
}

module "redirect_www" {
  source  = "./modules/redirect_www"
  zone_id = var.cloudflare_zone_id
}
