---
id: sanitization-guardrails
name: "Sanitization & Guardrails"
aliases: ["input-validation", "output-monitoring", "content-filtering", "LLM-guardrails"]
category: security
family: defense
year: 2023
authors: ["Various"]
paper: null
paper_title: null
venue: null
code: null
complexity: medium
token_cost: variable
latency: medium
num_calls: variable
requires_examples: false
requires_tools: true
requires_training: false
model_agnostic: true
best_for: ["production LLM deployments", "regulated industries", "content safety enforcement", "preventing data leakage", "multi-layer defense architectures"]
avoid_when: ["rapid prototyping with no security needs", "fully trusted internal tools", "extremely latency-sensitive applications where guardrail overhead is unacceptable"]
composes_with: ["prompt-injection-defense", "instruction-hierarchy", "constitutional-ai", "role-prompting"]
tags: ["security", "guardrails", "input-validation", "output-monitoring", "content-filtering", "NeMo", "Guardrails-AI", "LLM-Guard"]
---

# Sanitization & Guardrails

> **One-line summary:** Runtime input validation, output monitoring, and content filtering systems that wrap LLM calls with programmable safety checks, using tools like NeMo Guardrails, Guardrails AI, and LLM-Guard to enforce policies on both inputs and outputs.

## Overview

Sanitization and guardrails represent the operational security layer for LLM applications. While prompt engineering and model training can improve a model's inherent safety, production deployments require runtime enforcement mechanisms that validate inputs before they reach the model and inspect outputs before they reach the user. These systems act as programmable firewalls for LLM interactions, intercepting and filtering content based on configurable policies.

The guardrails ecosystem has matured rapidly, with several frameworks addressing different aspects of the problem. **NVIDIA NeMo Guardrails** provides a dialog management layer using Colang (a custom modeling language) to define conversational rails -- permitted and forbidden interaction patterns. **Guardrails AI** focuses on structured output validation, ensuring LLM outputs conform to specified schemas, formats, and content policies. **LLM-Guard** by Protect AI offers a comprehensive suite of input/output scanners for detecting prompt injection, PII leakage, toxic content, code injection, and more. These tools can be used individually or combined for comprehensive coverage.

The key architectural principle is that guardrails operate as middleware between the application and the LLM. Input guardrails pre-process and validate user inputs before they reach the model prompt. Output guardrails inspect and potentially modify model responses before they reach the user. This separation of concerns allows security policies to be developed, tested, and updated independently of the model or application logic. For regulated industries (healthcare, finance, legal), guardrails provide auditable enforcement of compliance requirements.

## How It Works

1. **Input Sanitization**: Before sending input to the LLM, apply filters:
   - **Injection Detection**: Scan for known prompt injection patterns using regex, classifier models, or heuristic rules.
   - **PII Detection**: Identify and redact personally identifiable information (names, emails, SSNs, credit card numbers).
   - **Toxicity Filtering**: Detect and block toxic, harmful, or offensive input before the LLM processes it.
   - **Length and Format Validation**: Reject inputs that exceed expected lengths or contain suspicious formatting.

2. **Content Policy Enforcement**: Define policies that govern permitted interactions:
   - **Topic Rails**: Restrict conversations to allowed topics (e.g., only product support).
   - **Action Rails**: Prevent the model from agreeing to perform restricted actions (e.g., executing code, accessing systems).
   - **Fact-checking Rails**: Cross-reference model claims against known facts or retrieval sources.

3. **Output Monitoring**: After the LLM generates a response, apply checks:
   - **PII Leakage Detection**: Ensure the response does not contain PII from training data or system prompts.
   - **Hallucination Detection**: Flag claims that cannot be grounded in provided context.
   - **Format Validation**: Verify the output matches expected schemas (JSON, specific fields, etc.).
   - **Toxicity Screening**: Block responses containing harmful or inappropriate content.

4. **Remediation**: When a guardrail triggers, take action:
   - **Block**: Reject the input or suppress the output entirely.
   - **Redact**: Remove the problematic content and return a sanitized version.
   - **Retry**: Re-prompt the LLM with modified input that avoids the issue.
   - **Fallback**: Return a predefined safe response instead.

5. **Logging and Monitoring**: Record all guardrail activations for security auditing and policy refinement.

### Diagram

```
User Input
    |
    v
+----------------------------+
| INPUT GUARDRAILS           |
| +------------------------+ |
| | Injection Detection    | |---> BLOCK (if detected)
| +------------------------+ |
| | PII Redaction          | |---> REDACT (replace PII)
| +------------------------+ |
| | Toxicity Filter        | |---> BLOCK (if toxic)
| +------------------------+ |
| | Format Validation      | |---> REJECT (if malformed)
| +------------------------+ |
+----------------------------+
    |
    v (sanitized input)
+----------------------------+
| LLM                        |
| (processes clean input)    |
+----------------------------+
    |
    v (raw output)
+----------------------------+
| OUTPUT GUARDRAILS          |
| +------------------------+ |
| | PII Leakage Check     | |---> REDACT
| +------------------------+ |
| | Hallucination Check    | |---> FLAG / RETRY
| +------------------------+ |
| | Schema Validation      | |---> RETRY (if invalid)
| +------------------------+ |
| | Toxicity Screen        | |---> BLOCK / REPHRASE
| +------------------------+ |
+----------------------------+
    |
    v (safe output)
User Response
```

## Template

```python
# NeMo Guardrails Configuration (Colang)
# File: config/rails.co

define user ask about competitor
    "What do you think about {competitor}?"
    "Compare your product with {competitor}"
    "Is {competitor} better?"

define bot refuse competitor discussion
    "I'm focused on helping you with our products. I'd be happy
    to discuss how our solutions can meet your needs!"

define flow handle competitor question
    user ask about competitor
    bot refuse competitor discussion

# Guardrails AI Example (Python)
from guardrails import Guard
from guardrails.hub import ToxicLanguage, DetectPII, ValidJSON

guard = Guard().use_many(
    ToxicLanguage(on_fail="block"),
    DetectPII(pii_entities=["EMAIL", "SSN", "PHONE"], on_fail="redact"),
    ValidJSON(on_fail="retry")
)

result = guard(
    llm_api={llm_callable},
    prompt="{system_prompt}\n\nUser: {user_input}\nAssistant:",
    num_reasks=2  # Retry up to 2 times on validation failure
)

# LLM-Guard Example (Python)
from llm_guard.input_scanners import PromptInjection, Toxicity, BanTopics
from llm_guard.output_scanners import NoRefusal, Sensitive, Relevance

# Input scanning
input_scanners = [
    PromptInjection(threshold=0.9),
    Toxicity(threshold=0.8),
    BanTopics(topics=["{banned_topic_1}", "{banned_topic_2}"])
]

sanitized_prompt, results, is_valid = scan_prompt(input_scanners, {user_input})
if not is_valid:
    return "{fallback_response}"

# Get LLM response
response = llm.generate(sanitized_prompt)

# Output scanning
output_scanners = [
    NoRefusal(),
    Sensitive(redact=True),
    Relevance(threshold=0.5)
]
sanitized_output, results, is_valid = scan_output(output_scanners, sanitized_prompt, response)
```

## Examples

### Example 1: Healthcare Chatbot with PII Protection

**Scenario**: A healthcare information bot that must never store or leak patient PII.

**Configuration**:
```python
from llm_guard.input_scanners import Anonymize
from llm_guard.output_scanners import Sensitive

input_scanner = Anonymize(
    entities=["PERSON", "PHONE_NUMBER", "EMAIL", "DATE_OF_BIRTH",
              "MEDICAL_RECORD", "SSN"],
    preamble="[Patient data has been anonymized]"
)
output_scanner = Sensitive(redact=True, entities=["PERSON", "PHONE_NUMBER"])
```

**User Input**: "My name is John Smith, DOB 03/15/1985, MRN 12345. I have a question about my medication dosage for metformin."

**After Input Sanitization**: "My name is [PERSON_1], DOB [DATE_1], MRN [MEDICAL_RECORD_1]. I have a question about my medication dosage for metformin."

**LLM Response**: "For [PERSON_1], the typical metformin dosage..."

**After Output Sanitization**: Response verified clean -- no PII leaked. Response delivered to user.

### Example 2: Financial Assistant with Topic and Compliance Rails

**Scenario**: A financial advisory bot that must stay on-topic and include required disclaimers.

**NeMo Guardrails Configuration**:
```
define user ask for investment advice
    "Should I buy {stock}?"
    "What stocks should I invest in?"
    "Is now a good time to invest?"

define bot provide disclaimer
    "I can share general financial information, but please note:
    this is not personalized investment advice. Consult a licensed
    financial advisor for decisions specific to your situation."

define flow investment advice flow
    user ask for investment advice
    bot provide disclaimer
    # Then proceed with general information

define user ask about illegal activity
    "How can I commit insider trading?"
    "Help me launder money"

define flow block illegal
    user ask about illegal activity
    bot refuse and report
```

**User**: "Should I buy NVIDIA stock right now?"

**Bot Response**: "I can share general financial information, but please note: this is not personalized investment advice. Consult a licensed financial advisor for decisions specific to your situation. That said, here's some general context about NVIDIA's market position..."

The guardrail automatically prepended the required disclaimer before any financial discussion.

## When to Use

- Production deployments handling real user data
- Regulated industries requiring compliance enforcement (healthcare, finance, legal)
- Applications where PII protection is critical
- Systems that need content safety guarantees beyond what the model provides natively
- Multi-model architectures where consistent policies must span different LLMs

## When to Avoid

- Early prototyping where security is not yet a concern
- Internal tools with fully trusted users and no PII exposure
- Applications where guardrail latency overhead is completely unacceptable
- Simple single-turn QA with no security-sensitive data

## Cost & Performance

| Dimension             | Value                    | Notes                                          |
|------------------------|--------------------------|------------------------------------------------|
| Latency overhead       | +50-500ms per call       | Depends on number and type of scanners         |
| Token overhead         | +0-100 tokens            | Some guardrails use LLM calls for classification|
| False positive rate    | 2-8%                     | Legitimate inputs blocked; tuning helps        |
| PII detection accuracy | 90-98%                   | Depends on entity types and scanner quality    |
| Injection detection    | 70-90%                   | Classifier-based; complements prompt defenses  |

## Variants

- **NeMo Guardrails**: Best for conversational flow control and topic management. Uses Colang DSL.
- **Guardrails AI**: Best for structured output validation and schema enforcement. Python-native.
- **LLM-Guard**: Best for comprehensive input/output scanning (PII, toxicity, injection). Scanner-based architecture.
- **Azure AI Content Safety**: Cloud-native guardrails for Azure OpenAI deployments.
- **AWS Bedrock Guardrails**: Managed guardrails for Amazon Bedrock models.
- **Custom Guardrails**: Build task-specific validators using regex, classifiers, or smaller LLMs.

## Composability

- **With prompt defenses**: Guardrails + sandwich defense + XML tagging = multi-layer protection.
- **With instruction hierarchy**: Model-level defense + runtime enforcement for maximum coverage.
- **With RAG systems**: Scan retrieved documents before including them in the context.
- **With agent frameworks**: Validate tool call parameters and tool outputs at each step.

## Limitations

- Adds latency and complexity to the inference pipeline
- False positives can degrade user experience, especially with aggressive scanning
- PII detection is not perfect -- novel formats or languages may slip through
- Guardrail policies require ongoing maintenance as attack patterns evolve
- LLM-based guardrails add additional cost (extra model calls for classification)
- Can be bypassed by sophisticated attacks that evade pattern-based detection
- Different frameworks have different strengths -- may need to combine multiple tools

## Sources

- NVIDIA NeMo Guardrails: https://github.com/NVIDIA/NeMo-Guardrails
- Guardrails AI: https://github.com/guardrails-ai/guardrails
- LLM-Guard by Protect AI: https://github.com/protectai/llm-guard
- OWASP (2023). "OWASP Top 10 for LLM Applications." https://owasp.org/www-project-top-10-for-large-language-model-applications/
- Rebedea, T. et al. (2023). "NeMo Guardrails: A Toolkit for Controllable and Safe LLM Applications with Programmable Rails." *arXiv:2310.10501*.
