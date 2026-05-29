# Per-tenant KMS CMK — M11 stretch
variable "tenant_id" { type = string }
variable "project" { type = string }

resource "aws_kms_key" "tenant" {
  description             = "${var.project} tenant ${var.tenant_id}"
  deletion_window_in_days = 30
  enable_key_rotation     = true
}

resource "aws_kms_alias" "tenant" {
  name          = "alias/${var.project}-tenant-${var.tenant_id}"
  target_key_id = aws_kms_key.tenant.key_id
}

output "key_arn" { value = aws_kms_key.tenant.arn }
