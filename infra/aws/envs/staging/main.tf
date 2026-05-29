# Staging — same module layout as dev; copy and adjust environment = "staging"
terraform {
  required_version = ">= 1.5"
  backend "s3" {
    bucket         = "domainmind-terraform-state"
    key            = "staging/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "domainmind-terraform-lock"
    encrypt        = true
  }
}
# See envs/dev/main.tf for full module wiring
