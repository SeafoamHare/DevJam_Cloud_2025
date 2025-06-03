locals {
  allow_ips = ["0.0.0.0/0", ]
}

resource "google_sql_database_instance" "postgres_instance" {
  name                = "${var.APP_NAME}-pg-instance"
  database_version    = "POSTGRES_14"
  deletion_protection = false
  region              = var.GCP_REGION
  settings {
    tier      = "db-f1-micro" # 使用基本的硬體配備
    disk_size = "10"

    ip_configuration {
      dynamic "authorized_networks" {
        for_each = local.allow_ips
        iterator = allow_ips

        content {
          name  = "allow-${allow_ips.key}"
          value = allow_ips.value
        }
      }
    }
  }
}

resource "google_sql_database" "this" {
  name     = "${var.APP_NAME}-db"
  instance = google_sql_database_instance.postgres_instance.name
}

resource "google_sql_user" "users" {
  name     = var.db_user_name
  instance = google_sql_database_instance.postgres_instance.name
  password = var.db_user_password
}