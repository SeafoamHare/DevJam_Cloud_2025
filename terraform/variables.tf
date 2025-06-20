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
