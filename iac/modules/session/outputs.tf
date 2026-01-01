output "signing_key" {
  description = "Signing key for the session"
  value       = random_password.signing_key.result
}
