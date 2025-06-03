output "db_ip" {
  value = google_sql_database_instance.postgres_instance.public_ip_address
}

output "db_name" {
  value = google_sql_database.this.name
}

# output "db_user" {
#   value = google_sql_user.default_user.name
# }

# output "db_password" {
#   value     = var.db_user_password
#   sensitive = true
# }
