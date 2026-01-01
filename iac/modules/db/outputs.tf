output "hostname" {
  value       = "${neon_endpoint.main.id}-pooler.${neon_endpoint.main.proxy_host}"
  description = "Hostname for connection with pooling. Use this for the application."
}

output "hostname_unpooled" {
  value       = neon_endpoint.main.host
  description = "Hostname for connection without pooling. For schema migration only."
}

output "port" {
  value = 5432
}

output "username" {
  value = data.neon_project.main.database_user
}

output "password" {
  value = data.neon_project.main.database_password
}

output "database_name" {
  value = neon_database.main.name
}
