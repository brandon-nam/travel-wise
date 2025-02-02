resource "google_artifact_registry_repository" "this" {
  location      = var.region
  repository_id = "cs3203-repo"
  format        = "DOCKER"
}

resource "google_artifact_registry_repository_iam_member" "member" {
  project = google_artifact_registry_repository.this.project
  location = google_artifact_registry_repository.this.location
  repository = google_artifact_registry_repository.this.name
  role = "roles/artifactregistry.writer"
  member = "serviceAccount:${google_service_account.github_actions.email}"
}