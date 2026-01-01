variable "zone_id" {
  description = "The Cloudflare Zone ID to create the certificate for."
  type        = string
}

variable "fqdn" {
  description = "The FQDN to create the certificate for. Must be in provided Cloudflare Zone."
  type        = string
}

variable "extra_regions" {
  description = "Additional AWS regions where the certificates will be created. A certificate will always be created for the provider's region."
  type        = set(string)
}
