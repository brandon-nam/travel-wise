variable "service_account_id" {
  type        = string
}

variable "role" {
  type        = string
}

variable "members" {
  type        = list(string)
}
