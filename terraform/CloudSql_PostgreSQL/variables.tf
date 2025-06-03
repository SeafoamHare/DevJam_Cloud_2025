variable "GCP_PROJECT_ID" {
  description = "GCP Project ID"
  type        = string
  default     = "test-terraform-461507"
}

variable "GCP_REGION" {
  type    = string
}

variable "APP_NAME" {
  description = "The name of the application."
  type        = string
  default     = "library-management-system"
}

variable "db_name" {
  type    = string
  default = "db-tf-ch4-10-3"
}

variable "db_user_name" {
  description = "The username for the Cloud SQL database user."
  type        = string
}

variable "db_user_password" {
  description = "The password for the Cloud SQL database user."
  type        = string
  sensitive   = true
  // No default, should be set via .tfvars or environment variables for security
}
