module "cs3203_bucket_1" {
  source  = "terraform-google-modules/cloud-storage/google//modules/simple_bucket"
  version = "~> 9.0"

  name       = "cs3203-bucket-1"
  location   = var.region
  project_id = var.project_id

  versioning               = "true"
  public_access_prevention = "enforced"
}