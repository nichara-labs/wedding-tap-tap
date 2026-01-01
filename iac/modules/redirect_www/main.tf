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

resource "cloudflare_dns_record" "redirect_www" {
  zone_id = var.zone_id
  name    = "www.${data.cloudflare_zone.zone.name}"
  ttl     = 1 # auto
  type    = "A"
  comment = "Managed by OpenTofu"
  content = "192.0.2.1" # Internal
  proxied = true
}

resource "cloudflare_ruleset" "redirect_www" {
  # https://developers.cloudflare.com/rules/url-forwarding/single-redirects/terraform-example/
  zone_id = var.zone_id
  name    = "Redirect www to root"
  phase   = "http_request_dynamic_redirect"
  kind    = "zone"
  rules = [
    {
      ref        = "redirect_www"
      action     = "redirect"
      expression = "lower(http.host) == \"www.${data.cloudflare_zone.zone.name}\""
      action_parameters = {
        from_value = {
          target_url = {
            expression  = "concat(\"https://${data.cloudflare_zone.zone.name}\", http.request.uri.path)"
            status_code = 301
          }
          preserve_query_string = true

        }
      }
    }
  ]
}
