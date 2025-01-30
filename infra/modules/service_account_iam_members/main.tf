resource "google_service_account_iam_member" "this" {
  count = length(var.members)

  service_account_id  = var.service_account_id
  role                = var.role
  member              = var.members[count.index]
}
