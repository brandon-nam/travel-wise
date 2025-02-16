resource "google_compute_network" "this" {
  project = var.project_id
  name = "cs3203-network"
}

resource "google_compute_global_address" "private_ip_address" {

  name          = "private-ip-address"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = google_compute_network.this.id
}

resource "google_service_networking_connection" "private_vpc_connection" {

  network                 = google_compute_network.this.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_address.name]
}

resource "random_id" "db_name_suffix" {
  byte_length = 4
}

resource "google_sql_database_instance" "instance" {

  name             = "private-instance-${random_id.db_name_suffix.hex}"
  region           = "us-central1"
  database_version = "MYSQL_5_7"

  depends_on = [google_service_networking_connection.private_vpc_connection]

  settings {
    tier = "db-f1-micro"
    ip_configuration {
      ipv4_enabled                                  = false
      private_network                               = google_compute_network.this.self_link
      enable_private_path_for_google_cloud_services = true
    }
  }
}
