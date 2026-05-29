variable "project" { type = string }
variable "environment" { type = string }
variable "kms_key_arn" { type = string }

resource "aws_s3_bucket" "data" {
  bucket = "${var.project}-${var.environment}-data"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data" {
  bucket = aws_s3_bucket.data.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = var.kms_key_arn
    }
  }
}

resource "aws_s3_bucket" "models" {
  bucket = "${var.project}-${var.environment}-models"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "models" {
  bucket = aws_s3_bucket.models.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = var.kms_key_arn
    }
  }
}

resource "aws_s3_bucket" "audit" {
  bucket = "${var.project}-${var.environment}-audit"
}

resource "aws_s3_bucket_object_lock_configuration" "audit" {
  bucket = aws_s3_bucket.audit.id
  rule {
    default_retention {
      mode = "COMPLIANCE"
      days = 2555
    }
  }
}

output "data_bucket" { value = aws_s3_bucket.data.id }
output "models_bucket" { value = aws_s3_bucket.models.id }
output "audit_bucket" { value = aws_s3_bucket.audit.id }
