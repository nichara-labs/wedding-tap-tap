variable "zone_id" {
  description = "The Cloudflare zone ID where the record will be created."
  type        = string
}

variable "name" {
  description = "The name of the DNS record."
  type        = string
}

variable "type" {
  description = "The type of the DNS record."
  type        = string
}

variable "content" {
  description = "The content of the DNS record."
  type        = string
}

variable "proxied" {
  description = "Whether the DNS record is proxied through Cloudflare."
  type        = bool
}
