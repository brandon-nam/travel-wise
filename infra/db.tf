resource "google_compute_network" "this" {
  project = var.project_id
  name = "cs3203-network"
}

resource "google_compute_subnetwork" "this" {
  name          = "cs3203-subnet"
  ip_cidr_range = "10.0.0.0/16"
  region        = var.region
  network       = google_compute_network.this.id
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

resource "google_sql_database_instance" "this" {
  name             = "cs3203-db-instance"
  database_version = "POSTGRES_14"
  region           = var.region

  depends_on = [google_service_networking_connection.private_vpc_connection]

  settings {
    tier = "db-f1-micro"
    ip_configuration {
      ipv4_enabled = false
      private_network = google_compute_network.this.id
      enable_private_path_for_google_cloud_services = true
    }
  }
}


resource "google_sql_user" "this" {
  name     = "cs3203-user"
  instance = google_sql_database_instance.this.name
  password = "cs3203-password"
}


resource "google_vpc_access_connector" "this" {
  name         = "db-connector"
  region       = var.region
  network       = google_compute_network.this.id
  min_instances = 2
  ip_cidr_range = "10.8.0.0/28"
  max_instances = 3
}
