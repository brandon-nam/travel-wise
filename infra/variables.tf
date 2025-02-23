variable "region" {
  type        = string
  default     = "asia-southeast1"
}

variable "project_id" {
  type        = string
  default     = "evident-trees-449214-s9"
}

variable "db_host" {
  type = string
  default = "127.0.0.1"
}

variable "db_port" {
  type = string
  default = "5432"
}

variable "db_user" {
  type = string
  default = "cs3203-user"
}

variable "db_password" {
  type = string
}

variable "db_name" {
  type = string
  default = "cs3203-db"
}

variable "db_driver" {
  type = string
  default = "postgresql+psycopg2"
}

// frontend

variable "map_api_key" {
  type = string
  default = "cs3203-db"
}

variable "map_id" {
  type = string
  default = "cs3203-db"
}