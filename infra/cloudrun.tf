resource "google_cloud_run_v2_service" "http_server" {
  name     = "http-server"
  location = "asia-southeast1"
  deletion_protection = false
  ingress = "INGRESS_TRAFFIC_ALL"

  template {
    scaling {
      max_instance_count = 1
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
