
resource "null_resource" "docker_image_build_push" {
  # This provisioner will run on every 'terraform apply' unless more specific triggers are added.
  # For a production setup, consider adding triggers based on your application source code changes.
  # Example: triggers = { source_code_hash = filesha256("../app/main.py") } # Adjust path as needed
  provisioner "local-exec" {
    command = <<EOT
      cd ../
      echo "Configuring Docker credentials for Artifact Registry..."
      gcloud auth configure-docker ${var.GCP_REGION}-docker.pkg.dev --quiet
      echo "Building Docker image for linux/amd64..."
      docker build --platform linux/amd64 -t "${var.GCP_REGION}-docker.pkg.dev/${var.GCP_PROJECT_ID}/${var.REPOSITORY_ID}/${var.APP_NAME}:latest" .
      echo "Pushing Docker image to Artifact Registry..."
      docker push "${var.GCP_REGION}-docker.pkg.dev/${var.GCP_PROJECT_ID}/${var.REPOSITORY_ID}/${var.APP_NAME}:latest"
    EOT
  }
  triggers = {
    always_run = timestamp()
  }
}

resource "google_cloud_run_v2_service" "default" {
  provider = google
  name     = var.APP_NAME
  location = var.GCP_REGION

  depends_on = [null_resource.docker_image_build_push]

  template {
    containers {
      # Before applying, ensure the image is pushed to Artifact Registry:
      # ${var.GCP_REGION}-docker.pkg.dev/${var.gcp_project_id}/${google_artifact_registry_repository.default.repository_id}/${var.app_name}:latest
      image = "${var.GCP_REGION}-docker.pkg.dev/${var.GCP_PROJECT_ID}/${var.REPOSITORY_ID}/${var.APP_NAME}:latest"
      ports {
        container_port = 8080
      }
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
}

resource "google_cloud_run_service_iam_member" "allow_public" {
  provider = google
  location = google_cloud_run_v2_service.default.location
  project  = google_cloud_run_v2_service.default.project
  service  = google_cloud_run_v2_service.default.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
