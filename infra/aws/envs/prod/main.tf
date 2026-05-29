# Production — deploy in M12 only after staging load test passes
terraform {
  required_version = ">= 1.5"
  backend "s3" {
    bucket         = "domainmind-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "domainmind-terraform-lock"
    encrypt        = true
  }
}
# See envs/dev/main.tf — enable deletion_protection, larger RDS, GPU node group
