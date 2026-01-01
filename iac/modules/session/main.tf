terraform {
  required_providers {
    random = {
      source  = "hashicorp/random"
      version = "~> 3.7"
    }
  }
  required_version = "~> 1.10"
}

resource "random_password" "signing_key" {
  length = 64
}
