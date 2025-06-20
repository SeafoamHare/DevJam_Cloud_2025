##################################################################################
# CONFIGURATION
##################################################################################
terraform {
  # 指定 terraform 的最小版本
  required_version = ">=1.0"

  required_providers {
    # provider 中的最小版本
    google = {
      source  = "hashicorp/google"
      version = ">= 4.40.0"
    }

    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}
##################################################################################
# PROVIDERS
##################################################################################
provider "google" {
  # your project name
  project = var.GCP_PROJECT_ID
}
