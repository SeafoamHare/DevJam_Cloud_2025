variable "gcp_project_id" {
  description = "The GCP project ID to deploy to."
  type        = string
}

variable "gcp_region" {
  description = "The GCP region for resources."
  type        = string
}

variable "app_name" {
  description = "The name of the application."
  type        = string
  default     = "library-management-system"
}

variable "repository_id" {
  description = "The ID of the Artifact Registry repository."
  type        = string
  default     = "library-management-system-repo" // Replace with your desired repository ID
}
variable "github_owner" {
  description = "The GitHub repository owner (e.g., your GitHub username)."
  type        = string
  # Replace with your GitHub username or organization
  default     = "SeafoamHare"
}

variable "github_repo_name" {
  description = "The name of the GitHub repository."
  type        = string
  default     = "DevJam_Cloud_2025" // Replace with your repository name
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
