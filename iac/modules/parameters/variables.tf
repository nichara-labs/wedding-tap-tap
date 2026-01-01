variable "public" {
  description = "Key-value pairs for public SSM parameters."
  type        = map(string)
  default     = {}
}

variable "secret" {
  description = "Key-value pairs for secret SSM parameters."
  type        = map(string)
  default     = {}
}
