terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

resource "google_artifact_registry_repository" "default" {
  provider      = google
  location      = var.gcp_region
  repository_id = "${var.app_name}-repo"
  description   = "Docker repository for ${var.app_name}"
  format        = "DOCKER"
}

resource "google_cloudbuild_trigger" "default" {
  provider = google
  project  = var.gcp_project_id
  name     = "${var.app_name}-trigger"

  filename = "cloudbuild.yaml"  # 放在 repo 根目錄的 Cloud Build YAML

  included_files = ["**"]
  ignored_files  = ["README.md"]

  substitutions = {
    _SERVICE_NAME = var.app_name
    _REGION       = var.gcp_region
    _REPO_NAME    = google_artifact_registry_repository.default.repository_id
    _IMAGE_NAME   = "${var.gcp_region}-docker.pkg.dev/${var.gcp_project_id}/${google_artifact_registry_repository.default.repository_id}/${var.app_name}"
  }

  github {
    owner = var.github_owner
    name  = var.github_repo_name
    push {
      branch = "^main$"
    }
  }
}



resource "google_cloud_run_v2_service" "default" {
  provider = google
  name     = var.app_name
  location = var.gcp_region

  template {
    containers {
      image = "${var.gcp_region}-docker.pkg.dev/${var.gcp_project_id}/${google_artifact_registry_repository.default.repository_id}/${var.app_name}:latest"
      ports {
        container_port = 8080
      }
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }

  depends_on = [
    google_cloudbuild_trigger.default
  ]
}

resource "google_cloud_run_service_iam_member" "allow_public" {
  provider = google
  location = google_cloud_run_v2_service.default.location
  project  = google_cloud_run_v2_service.default.project
  service  = google_cloud_run_v2_service.default.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
