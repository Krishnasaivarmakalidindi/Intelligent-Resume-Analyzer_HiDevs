#!/usr/bin/env bash
set -euo pipefail

# Run this from the repository root
cd "$(dirname "$0")"

# Commit the redacted local files and update .gitignore
git add .gitignore .env .env.example || true
git commit -m "chore: redact env files and update .gitignore" || true

# Backup current refs
git branch backup-before-secret-clean || true

# Prefer git-filter-repo if available
if command -v git-filter-repo >/dev/null 2>&1; then
  git filter-repo --invert-paths --paths .env --paths .env.example
elif python -c "import git_filter_repo" >/dev/null 2>&1; then
  python -m git_filter_repo --invert-paths --paths .env --paths .env.example
else
  git filter-branch --force --index-filter "git rm --cached --ignore-unmatch .env .env.example" --prune-empty --tag-name-filter cat -- --all
fi

# Clean up and aggressively prune history
rm -rf .git/refs/original/ || true
git reflog expire --expire=now --all || true
git gc --prune=now --aggressive || true

cat <<'EOF'
History rewritten locally. To update the remote, run (careful — this force-pushes):
  git push origin --force --all
  git push origin --force --tags

Important:
- Inform collaborators to re-clone or reset their local copies.
- If GitHub push protection still blocks the push, open the unblock URL shown in the push error or contact repository admins.
EOF
