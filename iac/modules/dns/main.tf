terraform {
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 5.8"
    }
  }
  required_version = "~> 1.10"
}

data "cloudflare_zone" "zone" {
  zone_id = var.zone_id
}

resource "cloudflare_dns_record" "record" {
  zone_id = var.zone_id
  name    = "${var.name == "" ? "" : "${var.name}."}${data.cloudflare_zone.zone.name}"
  ttl     = 1 # auto
  type    = var.type
  comment = "Managed by OpenTofu"
  content = var.content
  proxied = var.proxied
}
