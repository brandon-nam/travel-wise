resource "google_iam_workload_identity_pool" "cs3203" {
  workload_identity_pool_id = "cs3203-team-1"
  display_name = "cs3203-team-1"
}

resource "google_iam_workload_identity_pool_provider" "cs3203" {
  workload_identity_pool_id = google_iam_workload_identity_pool.cs3203.workload_identity_pool_id
  workload_identity_pool_provider_id = "github"
  display_name = "Github"
  attribute_condition = <<-EOT
    google.subject.startsWith('repo:nus-cs3203/cs3203-2420-cs3203_01:')
  EOT
  attribute_mapping = {
    "attribute.repo" = "assertion.repository"
    "google.subject" = "assertion.sub"
  }
  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}
