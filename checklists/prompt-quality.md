# Prompt Quality Checklist

> Use this checklist to evaluate and improve any prompt before deployment. Each category targets a distinct quality dimension. A production prompt should pass all applicable checkpoints.

## How to Use

1. Draft your prompt
2. Walk through each category below
3. Check off items that pass; fix items that fail
4. Re-evaluate after changes
5. A prompt scoring 90%+ of applicable checkpoints is production-ready

---

## Clarity

- [ ] The prompt has a single, unambiguous primary instruction
- [ ] The task is stated in the first 1-3 sentences (not buried)
- [ ] Technical terms are defined or used consistently
- [ ] There are no contradictory instructions
- [ ] Pronouns have clear antecedents (no ambiguous "it" or "this")
- [ ] Negative instructions are supplemented with positive alternatives ("Don't be vague" becomes "Be specific and use concrete examples")

## Specificity

- [ ] The desired output length is specified (word count, paragraph count, or "concise"/"detailed")
- [ ] The target audience is defined
- [ ] The domain or subject area is explicitly stated
- [ ] Success criteria are measurable (not just "good" or "helpful")
- [ ] Boundary conditions are stated (what to include AND what to exclude)

## Structure

- [ ] The prompt uses clear section delimiters (XML tags, headers, or separators)
- [ ] Instructions are separated from context/data
- [ ] Multi-step instructions are numbered or ordered
- [ ] The most important instruction appears first AND last (primacy + recency)
- [ ] Long prompts use a scaffolding pattern (role, context, task, format, constraints)

## Examples

- [ ] At least one example is provided for non-trivial tasks
- [ ] Examples cover the typical case AND at least one edge case
- [ ] Examples show both input and expected output format
- [ ] Examples are representative of real data (not toy cases)
- [ ] If few-shot, examples are diverse (not all the same pattern)

## Constraints

- [ ] Output format is explicitly specified (JSON, markdown, plain text, etc.)
- [ ] Required fields or sections are listed
- [ ] Prohibited content or behaviors are stated
- [ ] Token/length budget is appropriate for the task complexity
- [ ] Model-specific limits are respected (context window, output length)
- [ ] Any required reasoning approach is specified (e.g., "think step by step")

## Edge Cases

- [ ] The prompt handles empty or null input gracefully
- [ ] The prompt specifies behavior for ambiguous input
- [ ] The prompt addresses what to do when information is insufficient
- [ ] Multi-language input scenarios are considered (if applicable)
- [ ] The prompt handles adversarial or unexpected input (if user-facing)

## Output Format

- [ ] The exact output structure is demonstrated (not just described)
- [ ] JSON outputs include a schema or example object
- [ ] Table outputs specify column headers
- [ ] List outputs specify ordering (alphabetical, ranked, chronological)
- [ ] The prompt specifies how to handle multiple results (array vs. single)

## Grounding and Accuracy

- [ ] The prompt instructs the model to cite sources when making claims
- [ ] The prompt includes "only use the provided context" for RAG use cases
- [ ] Confidence levels or uncertainty markers are requested where appropriate
- [ ] The prompt says to respond with "I don't know" rather than fabricate
- [ ] Factual claims in the prompt itself are verified

## Tone and Voice

- [ ] The desired tone is specified (formal, casual, technical, friendly)
- [ ] A role or persona is assigned if voice consistency matters
- [ ] The prompt avoids unintentional tone cues (all caps, excessive exclamation)

## Efficiency

- [ ] The prompt is as short as possible while still being complete
- [ ] Redundant instructions are removed
- [ ] Context provided is relevant (no "noise" documents or irrelevant background)
- [ ] The number of examples is sufficient but not excessive (2-5 for most tasks)
- [ ] System prompt and user prompt responsibilities are properly divided

## Composability

- [ ] The prompt accepts parameterized input via clear placeholders (e.g., `{variable}`)
- [ ] Placeholders are named descriptively (not `{x}` or `{input}`)
- [ ] The prompt can be chained with other prompts (output of one feeds input of next)
- [ ] Metadata or context from upstream steps is properly integrated

---

## Scoring Guide

| Score | Rating | Action |
|-------|--------|--------|
| 90-100% | Production-ready | Deploy with monitoring |
| 75-89% | Good draft | Address gaps before production |
| 50-74% | Needs work | Significant revision required |
| <50% | Early draft | Restructure using a playbook |
