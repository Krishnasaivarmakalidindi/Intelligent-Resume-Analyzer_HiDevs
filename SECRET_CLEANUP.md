Steps to remove secrets from Git history and push the cleaned repository

1. Review the script `cleanup_secrets.sh` in the repository root.
2. Run the script locally from the repo root:

   bash cleanup_secrets.sh

3. If the script completes, force-push the cleaned history to the remote:

   git push origin --force --all
   git push origin --force --tags

Notes and warnings:
- Force-pushing rewritten history will affect all collaborators. Everyone should re-clone or reset.
- If GitHub push-protection still blocks the push, use the unblock URL shown in the push rejection or contact repo admins to temporarily allow the push.
- After successful push, rotate any exposed secrets (API keys) immediately — assume compromise.
