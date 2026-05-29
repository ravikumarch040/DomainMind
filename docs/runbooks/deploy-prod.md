# Production Deployment Runbook (M12)

## Prerequisites

- AWS GPU quota approved for `g5.2xlarge`
- ACM certificate validated in Route 53
- Terraform applied to `infra/aws/envs/prod`
- ECR images pushed with version tags

## Deploy steps

1. `kubectl apply -f infra/k8s/base/`
2. Configure External Secrets Operator with Secrets Manager ARNs
3. Apply ingress with ACM cert ARN
4. Verify ADOT collector → X-Ray traces in AWS Console
5. Run load test: `locust -f infra/loadtest/locustfile.py --host https://api.domainmind.example.com -u 50 -r 5`

## Rollback

Argo Rollouts auto-rollback on error-rate spike. Manual: `kubectl argo rollouts undo gateway`

## Alerts

- p95 latency > 4s → SNS → Slack
- Error rate > 1%
- GPU utilization > 90%
