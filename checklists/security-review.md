# Security Review Checklist

> Use this checklist to assess and harden any LLM-powered application against adversarial attacks, data leakage, and misuse. Organized by attack surface.

---

## Injection Prevention

- [ ] **(critical)** System prompt and user input are clearly separated using delimiters or structural boundaries
- [ ] **(critical)** User input is never directly concatenated into system prompts without sanitization
- [ ] Sandwich defense is applied: critical instructions appear both before and after user input
- [ ] Input filtering strips or escapes known injection patterns (e.g., "ignore previous instructions", "system:", "assistant:")
- [ ] Instruction hierarchy is enforced: system prompt takes precedence over user prompt
- [ ] Prompt templates use parameterized insertion (placeholders, not string concatenation)
- [ ] Multi-turn conversations do not allow earlier user messages to override system instructions
- [ ] Indirect injection vectors are addressed (e.g., content from retrieved documents, tool outputs, file uploads)

## Data Leakage Prevention

- [ ] **(critical)** System prompt content cannot be extracted via direct questioning ("What are your instructions?")
- [ ] **(critical)** PII is stripped or masked before being sent to the LLM API
- [ ] Training data extraction attacks are mitigated (model cannot be prompted to regurgitate training data verbatim)
- [ ] Internal knowledge base content is not included in responses unless explicitly authorized
- [ ] Conversation history does not leak between different users or sessions
- [ ] API keys, database credentials, and internal URLs are never included in prompts
- [ ] File paths and internal system architecture details are not revealed in error messages
- [ ] Metadata in responses (headers, tool call logs) does not expose internal system details

## Output Filtering

- [ ] **(critical)** Outputs are checked against a content policy before delivery to the user
- [ ] Harmful content categories are defined and filtered (violence, hate speech, illegal activity, etc.)
- [ ] Code generation outputs are sandboxed or reviewed before execution
- [ ] Generated URLs and links are validated against an allowlist or checked for phishing patterns
- [ ] SQL, shell commands, and other executable outputs are parameterized or escaped
- [ ] Output length is bounded to prevent resource exhaustion attacks
- [ ] Responses containing PII are redacted before delivery

## Access Control

- [ ] **(critical)** Authentication is required before any LLM endpoint is accessible
- [ ] **(critical)** Authorization checks verify the user has permission for the requested operation
- [ ] Role-based access controls (RBAC) limit which prompts and tools each user can access
- [ ] API rate limiting prevents abuse (per-user, per-IP, and global limits)
- [ ] Session management prevents replay attacks and session hijacking
- [ ] Tool calls triggered by the LLM respect the same permission boundaries as the user
- [ ] Admin-level system prompts are not accessible to regular users

## Monitoring and Incident Response

- [ ] **(critical)** All prompt-response pairs are logged for security audit (with PII redaction in logs)
- [ ] Anomaly detection flags unusual patterns (high volume, unusual prompts, extraction attempts)
- [ ] Injection attempt detection alerts on known attack patterns in user input
- [ ] Content policy violation events are logged and trigger alerts
- [ ] An incident response plan exists for LLM-specific security events
- [ ] Regular penetration testing includes LLM-specific attack vectors
- [ ] A responsible disclosure process exists for security researchers

## Supply Chain Security

- [ ] Model provenance is verified (model is from a trusted source)
- [ ] Third-party prompt libraries and templates are reviewed before use
- [ ] RAG knowledge base content is vetted and access-controlled
- [ ] Tool integrations are audited for security (what can the LLM trigger?)
- [ ] Dependencies (SDKs, middleware) are kept up to date with security patches

## Data Handling

- [ ] Data classification is applied: what data sensitivity level is sent to the LLM?
- [ ] Data processing agreements (DPAs) are in place with the LLM provider
- [ ] Data residency requirements are met (EU data stays in EU, etc.)
- [ ] Conversation data retention policies comply with regulations
- [ ] Users can request deletion of their conversation data
- [ ] Training data opt-out is configured if the provider offers it

---

## Threat Model Summary

| Threat | Likelihood | Impact | Mitigations | Status |
|--------|-----------|--------|-------------|--------|
| Prompt injection (direct) | High | High | Sanitization, hierarchy, sandwich | |
| Prompt injection (indirect) | Medium | High | Source filtering, output validation | |
| System prompt extraction | Medium | Medium | Refusal training, detection | |
| PII leakage | Medium | High | Masking, DLP, output filtering | |
| Training data extraction | Low | Medium | Provider controls, monitoring | |
| Denial of service | Medium | Medium | Rate limiting, circuit breakers | |
| Unauthorized tool execution | Low | Critical | Permission boundaries, approval gates | |

## Review Cadence

| Activity | Frequency |
|----------|-----------|
| Automated injection testing | Every deployment |
| Manual penetration testing | Quarterly |
| Security audit of prompt templates | Monthly |
| Review of access control policies | Quarterly |
| Incident response drill | Semi-annually |
| Third-party dependency audit | Monthly |
