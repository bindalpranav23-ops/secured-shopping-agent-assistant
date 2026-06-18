---
name: stride-threat-model
description: Performs a systematic STRIDE threat modeling assessment on the current project's codebase and architecture. Use this when starting a new implementation phase or reviewing existing components.
---

# STRIDE Threat Modeling Skill

## Goal

Guide the agent to analyze the workspace directory structure, configuration files, and code files to produce a structured `threat_model.md` assessment.

## Instructions

1. **Analyze System Boundaries**
   - Map the entry points, tools, workflows, prompts, components, and data storage layers.

2. **STRIDE Evaluation**
   Evaluate the system against the six STRIDE categories:
   - **Spoofing**: Are user or caller identity boundaries verified before executing sensitive tool logic?
   - **Tampering**: Can users manipulate data flows, parameters, or underlying state?
   - **Repudiation**: Are critical transactions securely logged?
   - **Information Disclosure**: Are we leaking PII, internal tokens, or raw stack traces?
   - **Denial of Service**: Are there rate limits on expensive database or LLM queries?
   - **Elevation of Privilege**: Can an unauthenticated user bypass access control to reach privileged tool actions?

3. **Review Security-Relevant Files**
   - `app/agent.py`
   - `.pre-commit-config.yaml`
   - `.semgrep/rules.yaml`
   - `.agents/CONTEXT.md`
   - `.agents/hooks.json`
   - `.agents/scripts/validate_tool_call.py`

4. **Identify Risks**
   Check for:
   - hardcoded API keys
   - single-use discount code race conditions
   - lack of persistent storage
   - weak user ID validation
   - missing audit logging
   - command execution risks

5. **Output**
   Generate a highly structured `threat_model.md` file saved directly in the `shopping-assistant` project root.

The report must include:
- System overview
- Trust boundaries
- STRIDE table
- Key risks
- Severity
- Recommended mitigations
- Final security summary
