terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
  backend "s3" {
    bucket         = "domainmind-terraform-state"
    key            = "dev/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "domainmind-terraform-lock"
    encrypt        = true
  }
}

provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Project     = "domainmind"
      Environment = "dev"
      ManagedBy   = "terraform"
    }
  }
}

variable "aws_region" { default = "us-east-1" }
variable "project" { default = "domainmind" }
variable "environment" { default = "dev" }

module "vpc" {
  source      = "../../modules/vpc"
  project     = var.project
  environment = var.environment
}

module "kms" {
  source      = "../../modules/kms"
  project     = var.project
  environment = var.environment
}

module "s3" {
  source      = "../../modules/s3"
  project     = var.project
  environment = var.environment
  kms_key_arn = module.kms.key_arn
}

module "ecr" {
  source      = "../../modules/ecr"
  project     = var.project
  environment = var.environment
}

module "eks" {
  source             = "../../modules/eks"
  project            = var.project
  environment        = var.environment
  vpc_id             = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids
}

module "rds" {
  source             = "../../modules/rds"
  project            = var.project
  environment        = var.environment
  vpc_id             = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids
  kms_key_arn        = module.kms.key_arn
}

module "elasticache" {
  source             = "../../modules/elasticache"
  project            = var.project
  environment        = var.environment
  vpc_id             = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids
}

module "cognito" {
  source      = "../../modules/cognito"
  project     = var.project
  environment = var.environment
}

output "vpc_id" { value = module.vpc.vpc_id }
output "eks_cluster" { value = module.eks.cluster_name }
output "data_bucket" { value = module.s3.data_bucket }
output "rds_endpoint" { value = module.rds.endpoint }
output "cognito_user_pool" { value = module.cognito.user_pool_id }
