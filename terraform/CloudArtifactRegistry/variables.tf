variable "GCP_PROJECT_ID" {
  description = "The GCP project ID to deploy to."
  type        = string
}

variable "GCP_REGION" {
  description = "The GCP region for resources."
  type        = string
}

variable "APP_NAME" {
  description = "The name of the application."
  type        = string
}

variable "REPOSITORY_ID" {
  description = "The ID of the Artifact Registry repository."
  type        = string
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
