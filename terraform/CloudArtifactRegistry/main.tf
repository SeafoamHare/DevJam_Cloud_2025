resource "google_artifact_registry_repository" "default" {
  provider      = google
  location      = var.gcp_region
  repository_id = "${var.app_name}-repo"
  description   = "Docker repository for ${var.app_name}"
  format        = "DOCKER"
}