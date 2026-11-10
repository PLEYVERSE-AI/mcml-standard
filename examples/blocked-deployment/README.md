# Blocked deployment example

These cards are intentionally incomplete. `pre-deploy-check` should refuse them:

- the Model Card has no safety evidence (failure modes, evaluation evidence, oversight, monitoring, risk acceptance)
- the Agentic Governance Card has no kill switch, so it fails schema validation
- there is no Dataset Card or Interface Card

```bash
python tools/mcml.py pre-deploy-check examples/blocked-deployment
# DEPLOYMENT BLOCKED (exit code 1)
```
