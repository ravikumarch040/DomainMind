#!/usr/bin/env bash
# Sync docs/ to GitHub Wiki (https://github.com/ravikumarch040/DomainMind.wiki)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WIKI_URL="${WIKI_URL:-https://github.com/ravikumarch040/DomainMind.wiki.git}"
WIKI_DIR="${WIKI_DIR:-$ROOT/.wiki-deploy}"

rm -rf "$WIKI_DIR"
git clone "$WIKI_URL" "$WIKI_DIR"

cp "$ROOT/docs/"*.md "$WIKI_DIR/"
cp -r "$ROOT/docs/runbooks" "$WIKI_DIR/"
cp "$ROOT/docs/index.md" "$WIKI_DIR/Home.md"
rm -f "$WIKI_DIR/index.md"

find "$WIKI_DIR" -name "*.md" ! -name "_Sidebar.md" -exec sed -i 's/\](\([^)]*\)\.md)/](\1)/g' {} +
find "$WIKI_DIR" -name "*.md" -exec sed -i 's/(index)/(Home)/g' {} +

cat > "$WIKI_DIR/_Sidebar.md" << 'EOF'
**[Home](Home)**

### Getting started
- [Onboarding](onboarding)
- [Project overview](project-overview)
- [Requirements](requirements)

### Architecture
- [Architecture](architecture)
- [QLoRA Pipeline](DomainMind_QLoRA_Pipeline)
- [Data model](data-model)
- [API reference](api-reference)

### Operations
- [Environments](environments)
- [Deployment](deployment)
- [Configuration](configuration)
- [Security and access](security-and-access)
- [Testing strategy](testing-strategy)
- [Runbooks](runbooks)

### Reference
- [Known issues](known-issues)
- [Risks and decisions](risks-and-decisions)
- [Ownership](ownership)

### Runbooks
- [M0 Day-1 checklist](runbooks/m0-day1-checklist)
- [Compliance checklist](runbooks/compliance-checklist)
- [Deploy prod](runbooks/deploy-prod)
EOF

cd "$WIKI_DIR"
git add -A
if git diff --staged --quiet; then
  echo "Wiki is already up to date."
  exit 0
fi
git commit -m "Sync docs from main repository"
git push origin master 2>/dev/null || git push origin main

echo "Wiki synced: https://github.com/ravikumarch040/DomainMind/wiki"
