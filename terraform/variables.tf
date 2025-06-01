variable "gcp_project_id" {
  description = "The GCP project ID to deploy to."
  type        = string
  default     = "devjam-cloud-2025"
}

variable "gcp_region" {
  description = "The GCP region for resources."
  type        = string
  default     = "us-central1"
}

variable "app_name" {
  description = "The name of the application."
  type        = string
  default     = "library-management-system"
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
  # Replace with your GitHub repository name
  default     = "DevJam_Cloud_2025"
}
