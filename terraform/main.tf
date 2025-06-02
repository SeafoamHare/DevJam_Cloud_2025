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

resource "null_resource" "docker_image_build_push" {
  # This provisioner will run on every 'terraform apply' unless more specific triggers are added.
  # For a production setup, consider adding triggers based on your application source code changes.
  # Example: triggers = { source_code_hash = filesha256("../app/main.py") } # Adjust path as needed
  provisioner "local-exec" {
    command = <<EOT
      cd ../
      echo "Configuring Docker credentials for Artifact Registry..."
      gcloud auth configure-docker ${var.gcp_region}-docker.pkg.dev --quiet
      echo "Building Docker image for linux/amd64..."
      docker build --platform linux/amd64 -t "${var.gcp_region}-docker.pkg.dev/${var.gcp_project_id}/${google_artifact_registry_repository.default.repository_id}/${var.app_name}:latest" .
      echo "Pushing Docker image to Artifact Registry..."
      docker push "${var.gcp_region}-docker.pkg.dev/${var.gcp_project_id}/${google_artifact_registry_repository.default.repository_id}/${var.app_name}:latest"
    EOT
  }
  triggers = {
    always_run = timestamp()
  }
  
  depends_on = [google_artifact_registry_repository.default]
}

# locals {
#   allow_ips = ["0.0.0.0/0", ]
# }

# resource "google_sql_database_instance" "postgres_instance" {
#   name     = "${var.app_name}-pg-instance"
#   region   = var.gcp_region
#   database_version = "POSTGRES_14" 

#   settings {
#     tier = "db-f1-micro" 
#     availability_type = "REGIONAL" // Or "ZONAL"
#     # disk_autoresize = true
#     disk_size       = "10" // GB
#     // Consider adding backup_configuration and ip_configuration
#     ip_configuration {
#       dynamic "authorized_networks" {
#         for_each = local.allow_ips
#         iterator = allow_ips

#         content {
#           name  = "allow-${allow_ips.key}"
#           value = allow_ips.value
#         }
#       }
#       # ipv4_enabled    = true
#       # private_network = "projects/${var.gcp_project_id}/global/networks/default" // Example, use your VPC
#       # require_ssl     = true
#     }
#     # backup_configuration {
#     #   enabled            = true
#     #   binary_log_enabled = true
#     # }
#   }

#   deletion_protection = false 
# }

# resource "google_sql_database" "default_database" {
#   name     = "${var.app_name}-db"
#   instance = google_sql_database_instance.postgres_instance.name
#   // charset and collation can be set if needed
# }

# resource "google_sql_user" "default_user" {
#   provider = google
#   name     = var.db_user_name // Define this variable
#   instance = google_sql_database_instance.postgres_instance.name
#   password = var.db_user_password // Define this variable, consider using a secret manager
#   // host can be specified if needed, defaults to "%"
# }

resource "google_cloud_run_v2_service" "default" {
  provider = google
  name     = var.app_name
  location = var.gcp_region

  depends_on = [null_resource.docker_image_build_push]

  template {
    containers {
      # Before applying, ensure the image is pushed to Artifact Registry:
      # ${var.gcp_region}-docker.pkg.dev/${var.gcp_project_id}/${google_artifact_registry_repository.default.repository_id}/${var.app_name}:latest
      image = "${var.gcp_region}-docker.pkg.dev/${var.gcp_project_id}/${google_artifact_registry_repository.default.repository_id}/${var.app_name}:latest"
      ports {
        container_port = 8080
      }
      # env {
      #   name  = "DB_HOST"
      #   value = google_sql_database_instance.postgres_instance.public_ip_address
      # }
      # env {
      #   name  = "DB_NAME"
      #   value = google_sql_database.default_database.name
      # }
      # env {
      #   name  = "DB_USER"
      #   value = google_sql_user.default_user.name
      # }
      # env {
      #   name = "DB_PASSWORD"
      #   value_source {
      #     secret_key_ref {
      #       secret  = google_sql_user.default_user.password // This assumes you want to use the generated password directly.
      #                                                   // For better security, consider storing the password in Secret Manager
      #                                                   // and referencing it here. For this example, we'll use the direct value.
      #                                                   // However, Cloud Run's direct `value` for env vars is fine for passing Terraform variable values.
      #                                                   // Let's adjust to directly use the var.db_user_password for clarity with current setup.
      #     }
      #   }
      # }
      # // Corrected DB_PASSWORD environment variable setup
      # env {
      #   name  = "DB_PASSWORD"
      #   value = var.db_user_password // Directly using the variable
      # }
      # env {
      #   name = "DB_PORT"
      #   value = "5432" // Default PostgreSQL port
      # }
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
