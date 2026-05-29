variable "project" { type = string }
variable "environment" { type = string }

locals {
  repos = ["gateway", "retrieval", "eval", "orchestrator", "pipelines"]
}

resource "aws_ecr_repository" "repos" {
  for_each             = toset(local.repos)
  name                 = "${var.project}/${each.key}"
  image_tag_mutability = "MUTABLE"
  image_scanning_configuration { scan_on_push = true }
}

output "repository_urls" {
  value = { for k, v in aws_ecr_repository.repos : k => v.repository_url }
}
