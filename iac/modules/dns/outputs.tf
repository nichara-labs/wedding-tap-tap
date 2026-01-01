output "name" {
  description = "Name of the DNS record. Likely always the FQDN."
  value       = cloudflare_dns_record.record.name
}
