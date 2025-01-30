resource "google_iam_workload_identity_pool" "cs3203" {
  workload_identity_pool_id = "cs3203-team-1"
  display_name = "cs3203-team-1"
}

resource "google_iam_workload_identity_pool_provider" "cs3203" {
  workload_identity_pool_id = google_iam_workload_identity_pool.cs3203.workload_identity_pool_id
  workload_identity_pool_provider_id = "github"
  display_name = "Github"
  attribute_condition = <<-EOT
    google.subject.startsWith('repo:nus-cs3203/cs3203-2420-cs3203_01')
  EOT
  attribute_mapping = {
    "attribute.repo" = "assertion.repository"
    "google.subject" = "assertion.sub"
  }
  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}

resource "google_service_account" "github_actions" {
  account_id = "cs3203-github-actions"
  description = "god account for now"
  display_name = "cs3203 github actions"
}

module "sa_members_github_actions_account_token_creator" {
  source = "./modules/service_account_iam_members"

  service_account_id = google_service_account.github_actions.name
  role = "roles/iam.serviceAccountTokenCreator"
  members = [
    "user:tohhengxing.work@gmail.com",
  ]
}

module "sa_members_github_actions_workload_identity_user" {
  source = "./modules/service_account_iam_members"

  service_account_id = google_service_account.github_actions.name
  role = "roles/iam.workloadIdentityUser"
  members = [
    "serviceAccount:cs3203-github-actions@evident-trees-449214-s9.iam.gserviceaccount.com",
    "principalSet://iam.googleapis.com/projects/369525575533/locations/global/workloadIdentityPools/cs3203-team-1/attribute.repo/nus-cs3203/cs3203-2420-cs3203_01",
  ]
}
