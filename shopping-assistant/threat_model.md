# STRIDE Threat Model: Shopping Assistant Agent

## System Overview

The shopping assistant is an ADK 2.0 agent project that helps retail users redeem single-use discount codes. The main logic is implemented in `app/agent.py`. The system uses an in-memory store for registered user IDs, valid discount codes, and redeemed discount codes.

The project also includes local security gates using Semgrep, pre-commit hooks, and Antigravity tool-call hooks.

## Trust Boundaries

| Boundary | Description | Security Concern |
|---|---|---|
| User input to agent | Users provide discount codes and user IDs | Input may be invalid or malicious |
| Agent tool execution | The agent calls `redeem_discount_code` | Tool must validate user ID and code |
| In-memory state | Discount redemption state is stored in Python sets | Not persistent and not concurrency-safe |
| Local developer environment | Git, pre-commit, Semgrep, and hooks run locally | Misconfiguration could allow secrets to be committed |
| Model configuration | Gemini model is initialized in code | Hardcoded API key risk |

## STRIDE Assessment

| STRIDE Category | Risk | Severity | Recommended Mitigation |
|---|---|---|---|
| Spoofing | User identity is based only on a string user ID | Medium | Use authenticated user sessions or signed tokens |
| Tampering | Discount-code state can be modified in memory | Medium | Use persistent database storage with access control |
| Repudiation | Discount redemption attempts are not audit logged | Medium | Add structured logging for successful and failed redemptions |
| Information Disclosure | Simulated hardcoded API key exists in `app/agent.py` | High | Move API key to environment variables or secret manager |
| Denial of Service | No rate limiting on discount redemption attempts | Medium | Add rate limits and request validation |
| Elevation of Privilege | No role separation between regular users and administrators | Medium | Add explicit authorization checks for privileged actions |

## Key Risks

1. **Hardcoded API Key**
   - The project intentionally contains a simulated hardcoded Gemini API key for security-gating demonstration.
   - Semgrep correctly detects this issue.

2. **Single-Use Code Race Condition**
   - The in-memory redeemed-code set may not be safe in concurrent execution.
   - Two simultaneous requests could attempt to redeem the same code.

3. **Weak User ID Validation**
   - The system checks user IDs against a static in-memory set.
   - There is no authentication or proof that the user owns the provided ID.

4. **Lack of Persistent Storage**
   - Discount redemption state is lost when the process restarts.
   - A redeemed code could become usable again after restart.

5. **Missing Audit Logging**
   - Successful and failed redemption attempts are not stored.
   - This makes fraud investigation difficult.

6. **Command Execution Risk**
   - The project includes a local Antigravity hook to detect destructive commands.
   - This reduces risk, but command validation must remain strict.

## Recommended Mitigations

- Move API keys and secrets to environment variables.
- Use authenticated user sessions instead of raw user ID strings.
- Store discount codes and redemption status in a database.
- Use database transactions or locks to prevent race conditions.
- Add structured audit logs for all redemption attempts.
- Add rate limiting for repeated failed redemption attempts.
- Keep Semgrep and pre-commit hooks enabled before every commit.
- Keep destructive shell commands blocked through tool-call validation.

## Final Security Summary

The project demonstrates a secure local development workflow using Semgrep, pre-commit hooks, and Antigravity tool-call hooks. The most critical issue is the intentionally hardcoded API key, which should be remediated before final commit. The discount-code feature works for demonstration but should use authentication, persistent storage, transaction safety, and audit logging before production use.
