# Cybersecurity Squad Bridge

> Integration bridge between HRM Architect and Cybersecurity Squad. Defines when to delegate, how to map swarm workstreams to security tasks, brief format, and quality gate integration.

---

## Overview

The Cybersecurity Squad Bridge enables the HRM to seamlessly delegate security assessment, threat modeling, and compliance workstreams to the Cybersecurity Squad instead of using generic agents. This produces higher quality security deliverables by leveraging the squad's 15-agent roster covering Red Team, Blue Team, AppSec, CloudSec, Incident Response, and compliance.

---

## When to Delegate

### Automatic Delegation Triggers

The HRM delegates to the Cybersecurity Squad when ANY of these conditions are true:

| Trigger | Example |
|---------|---------|
| TIPO in [REVIEW, BUILD] AND domain is security | "Conduct security audit" |
| Keywords: "seguranca", "security", "secure" | "Make this application secure" |
| Keywords: "pentest", "penetration test", "vulnerability" | "Run a penetration test" |
| Keywords: "vulnerabilidade", "CVE", "exploit" | "Assess known vulnerabilities" |
| Keywords: "red team", "blue team", "purple team" | "Simulate red team attack" |
| Keywords: "AppSec", "application security", "secure coding" | "Review code for security flaws" |
| Keywords: "compliance", "SOC2", "ISO27001", "PCI-DSS", "GDPR" | "Achieve SOC2 compliance" |
| Keywords: "OWASP", "top 10", "injection", "XSS" | "Check for OWASP top 10" |
| Keywords: "threat model", "threat modeling", "STRIDE" | "Create threat model for API" |
| Keywords: "incident response", "breach", "SOC" | "Develop incident response plan" |
| Keywords: "hardening", "secure configuration" | "Harden production servers" |
| Keywords: "secure coding", "security review" | "Security code review for auth module" |
| Workstream archetype includes security + assessment | Build task with security workstream |

### Manual Override

User can explicitly request Cybersecurity Squad: "Use the Cybersecurity Squad for this" or "Delegate to security team".

### When NOT to Delegate

- Simple input validation (built-in coding practices)
- Password hashing with standard library functions (too small for squad overhead)
- Basic HTTPS setup or SSL certificate configuration
- Adding CSRF tokens to forms (standard framework feature)

---

## Swarm-to-Cybersecurity Mapping

When a multi-workstream task includes a security component:

```yaml
# Example: Building a fintech application
workstreams:
  - name: "frontend"
    archetype: L-Builder-Frontend
    execution: swarm_agent
  - name: "backend-api"
    archetype: L-Builder-Backend
    execution: swarm_agent
  - name: "security"
    archetype: L-Auditor  # detected as security domain
    execution: squad_delegation  # -> Cybersecurity Squad
  - name: "compliance"
    archetype: L-Compliance  # detected as compliance domain
    execution: squad_delegation  # -> Cybersecurity Squad (same squad)

interface_contracts:
  - between: ["security", "backend-api"]
    contract: "Threat model and security requirements delivered before API implementation; secure coding review after"
    owner: "security"
    delivery_checkpoint: "Before API development AND after API completion"
  - between: ["security", "frontend"]
    contract: "Client-side security requirements (CSP, XSS prevention, auth flow) delivered before frontend implementation"
    owner: "security"
    delivery_checkpoint: "Before frontend auth/data handling implementation"
  - between: ["compliance", "security"]
    contract: "Compliance requirements inform threat model scope; security findings feed compliance gap analysis"
    owner: "compliance"
    delivery_checkpoint: "Before threat modeling phase"
```

---

## Brief Format for Cybersecurity Squad

### Minimum Required Fields

```yaml
security_brief:
  objective: "What the security deliverable needs to achieve (specific, measurable)"
  scope:
    type: "pentest|threat_model|security_audit|incident_response|compliance_check|secure_code_review"
    deliverables: ["threat model", "vulnerability report", "remediation plan", "compliance gap analysis"]
  security_context:
    threat_landscape: "Known threats and attack vectors relevant to this system"
    existing_controls: ["current security measures in place"]
    compliance_requirements: ["SOC2", "ISO27001", "PCI-DSS", "GDPR"]
  target:
    systems: ["systems/services in scope"]
    codebase: ["repositories/modules to review"]
    infrastructure: ["cloud providers", "network topology"]
  constraints:
    - "authorized testing boundaries"
    - "production vs staging environment"
    - "timeline and reporting requirements"
```

### Optional Enrichment (from HRM context)

```yaml
security_enrichment:
  frameworks_to_use:
    - "OWASP"              # from reference/security/
    - "NIST"               # from methodology
    - "MITRE-ATT&CK"       # from reference/threat-intelligence/
  tools:
    - "Burp Suite"         # web app testing
    - "Nmap"               # network scanning
    - "Metasploit"         # exploitation framework
  compliance_standard: "SOC2|ISO27001|PCI-DSS|HIPAA"
  threat_intelligence: ["relevant threat feeds and advisories"]
  previous_findings: ["known issues from prior assessments"]
```

---

## Quality Gate Integration

### Cybersecurity Squad Internal Gates

The Cybersecurity Squad chief runs internal quality checks before delivering:

1. **Coverage completeness**: All systems/code in scope assessed?
2. **Finding severity accuracy**: Severity ratings properly calibrated (CVSS)?
3. **Remediation feasibility**: Are recommended fixes practical and prioritized?
4. **Compliance mapping**: Findings mapped to relevant compliance requirements?
5. **Evidence quality**: All findings backed by reproducible evidence?

### HRM External Gates (after delivery)

The HRM verifies Cybersecurity Squad output using these checks:

| Gate Level | Checks for Security |
|-----------|-------------------|
| Level 2 (Local) | Deliverables exist, format matches, all in-scope systems assessed |
| Level 4 (Semantic) | Threat coverage complete, remediation quality verified, compliance alignment confirmed |

### Threshold

Security quality threshold: **0.95** (security domain -- highest threshold, as security work demands maximum rigor).

---

## Feedback Protocol

### HRM -> Cybersecurity Squad Chief

If quality gate fails:

```
=== HRM FEEDBACK: SECURITY REVISION ===
Status: NEEDS_REVISION
Score: {score}/0.95

Issues:
  - {specific_issue}: {description}
    Expected: {what_was_expected}
    Found: {what_was_delivered}

Action Required:
  - {specific_revision_instruction}

Budget Remaining: {remaining}
========================================
```

### Cybersecurity Squad Chief -> HRM

Revision delivery:

```
=== SECURITY REVISION DELIVERY ===
Original Score: {old_score}
Revised Score: {new_score} (self-assessment)
Changes Made:
  - {change_1}
  - {change_2}
===================================
```
