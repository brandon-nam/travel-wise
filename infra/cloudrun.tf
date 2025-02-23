resource "google_cloud_run_v2_service" "http_server" {
  depends_on = [
    google_service_account.cloud_run_service_account
  ]
  name     = "http-server"
  location = "asia-southeast1"
  deletion_protection = false
  ingress = "INGRESS_TRAFFIC_ALL"
  template {
    service_account = google_service_account.cloud_run_service_account.email
    scaling {
      max_instance_count = 1
    }
    vpc_access{
      connector = google_vpc_access_connector.this.id
      egress = "PRIVATE_RANGES_ONLY"
    }
    containers {
      image = "asia-southeast1-docker.pkg.dev/evident-trees-449214-s9/cs3203-repo/cs3203_server:v1"
      ports {
        container_port = 3203
      }
      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }
      env {
        name = "DB_HOST"
        value = google_sql_database_instance.this.ip_address.0.ip_address
      }
      env {
        name = "DB_PORT"
        value = var.db_port
      }
      env {
        name = "DB_USER"
        value = var.db_user
      }
      env {
        name = "DB_PASSWORD"
        value = var.db_password
      }
      env {
        name = "DB_NAME"
        value = var.db_name
      }
      env {
        name = "DB_DRIVER"
        value = var.db_driver
      }
    }
  }
}

resource "google_cloud_run_service_iam_member" "http_server" {
  location = google_cloud_run_v2_service.http_server.location
  project = google_cloud_run_v2_service.http_server.project
  service = google_cloud_run_v2_service.http_server.name
  role = "roles/run.invoker"
  member = "allUsers"
}


resource "google_service_account" "cloud_run_service_account" {
  account_id   = "cloud-run-service-account"
  display_name = "Cloud Run Service Account"
}

resource "google_project_iam_member" "cloud_sql_client" {
  project = var.project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.cloud_run_service_account.email}"
}

resource "google_project_iam_member" "storage_object_viewer" {
  project = var.project_id
  role    = "roles/storage.objectViewer"
  member  = "serviceAccount:${google_service_account.cloud_run_service_account.email}"
}

resource "google_project_iam_member" "cloud_run_invoker" {
  project = var.project_id
  role    = "roles/run.invoker"
  member  = "serviceAccount:${google_service_account.cloud_run_service_account.email}"
}

// Frontend

resource "google_cloud_run_v2_service" "frontend" {
  depends_on = [
    google_service_account.cloud_run_service_account
  ]
  name     = "frontend"
  location = "asia-southeast1"
  deletion_protection = false
  ingress = "INGRESS_TRAFFIC_ALL"
  template {
    service_account = google_service_account.cloud_run_service_account.email
    scaling {
      max_instance_count = 1
    }
    containers {
      image = "asia-southeast1-docker.pkg.dev/evident-trees-449214-s9/cs3203-repo/cs3203_frontend:v1"
      ports {
        container_port = 4173
      }
      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }
      env {
        name = "MAP_API_KEY"
        value = var.map_api_key
      }
      env {
        name = "MAP_ID"
        value = var.map_id
      }
    }
  }
}

resource "google_cloud_run_service_iam_member" "frontend" {
  location = google_cloud_run_v2_service.frontend.location
  project = google_cloud_run_v2_service.frontend.project
  service = google_cloud_run_v2_service.frontend.name
  role = "roles/run.invoker"
  member = "allUsers"
}

