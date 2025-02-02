resource "google_artifact_registry_repository" "this" {
  location      = var.region
  repository_id = "cs3203-repo"
  format        = "DOCKER"
}