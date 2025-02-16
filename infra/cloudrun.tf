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

