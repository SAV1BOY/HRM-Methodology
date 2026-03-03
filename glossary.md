# Glossary — Alias to Canonical ID Mapping

This file maps common names, abbreviations, and alternative terms to their canonical technique IDs in the repository. The HRM agent uses this for fuzzy lookup when a user refers to a technique by a non-standard name.

## Alias Table

| Alias | Canonical ID | Category |
|-------|-------------|----------|
| instruction prompting | `zero-shot` | foundations |
| direct prompting | `zero-shot` | foundations |
| zero-shot | `zero-shot` | foundations |
| in-context learning | `few-shot` | foundations |
| ICL | `few-shot` | foundations |
| few-shot | `few-shot` | foundations |
| k-shot prompting | `few-shot` | foundations |
| single-example prompting | `one-shot` | foundations |
| one-shot | `one-shot` | foundations |
| persona prompting | `role-prompting` | foundations |
| role-play prompting | `role-prompting` | foundations |
| character prompting | `role-prompting` | foundations |
| system persona | `role-prompting` | foundations |
| context injection | `context-stuffing` | foundations |
| knowledge grounding | `context-stuffing` | foundations |
| RAG context | `context-stuffing` | foundations |
| structured output | `output-format` | foundations |
| format control | `output-format` | foundations |
| CO-STAR | `prompt-frameworks` | foundations |
| RISEN | `prompt-frameworks` | foundations |
| CRISP | `prompt-frameworks` | foundations |
| mnemonic frameworks | `prompt-frameworks` | foundations |
| prompt scaffolding | `prompt-scaffolding` | foundations |
| XML tagging | `prompt-scaffolding` | foundations |
| delimiters | `prompt-scaffolding` | foundations |
| prompt repetition | `prompt-repetition` | foundations |
| emphasis repetition | `prompt-repetition` | foundations |
| EmotionPrompt | `emotion-prompting` | foundations |
| emotional stimulus | `emotion-prompting` | foundations |
| CoT | `chain-of-thought` | reasoning |
| chain of thought | `chain-of-thought` | reasoning |
| think step by step | `zero-shot-cot` | reasoning |
| let's think step by step | `zero-shot-cot` | reasoning |
| Zero-Shot CoT | `zero-shot-cot` | reasoning |
| SC | `self-consistency` | reasoning |
| majority voting | `self-consistency` | reasoning |
| L2M | `least-to-most` | reasoning |
| decompose and solve | `least-to-most` | reasoning |
| PS+ | `plan-and-solve` | reasoning |
| plan then solve | `plan-and-solve` | reasoning |
| follow-up questions | `self-ask` | reasoning |
| compositional reasoning | `self-ask` | reasoning |
| ToT | `tree-of-thoughts` | reasoning |
| tree search reasoning | `tree-of-thoughts` | reasoning |
| GoT | `graph-of-thoughts` | reasoning |
| graph reasoning | `graph-of-thoughts` | reasoning |
| ReAct | `react` | reasoning |
| reason and act | `react` | reasoning |
| thought-action-observation | `react` | reasoning |
| ReWOO | `rewoo` | reasoning |
| plan-then-execute | `rewoo` | reasoning |
| PoT | `program-of-thoughts` | reasoning |
| code-based reasoning | `program-of-thoughts` | reasoning |
| PAL | `program-of-thoughts` | reasoning |
| CoD | `chain-of-draft` | reasoning |
| minimal CoT | `chain-of-draft` | reasoning |
| BoT | `buffer-of-thoughts` | reasoning |
| thought templates | `buffer-of-thoughts` | reasoning |
| SoT | `skeleton-of-thought` | reasoning |
| parallel generation | `skeleton-of-thought` | reasoning |
| contrastive CoT | `contrastive-cot` | reasoning |
| correct and incorrect examples | `contrastive-cot` | reasoning |
| ThoT | `thread-of-thought` | reasoning |
| chaotic context reasoning | `thread-of-thought` | reasoning |
| AoT | `algorithm-of-thoughts` | reasoning |
| algorithmic reasoning | `algorithm-of-thoughts` | reasoning |
| Tab-CoT | `tab-cot` | reasoning |
| tabular chain of thought | `tab-cot` | reasoning |
| self-generated examples | `analogical-prompting` | reasoning |
| analogical reasoning | `analogical-prompting` | reasoning |
| incremental reasoning | `cumulative-reasoning` | reasoning |
| proposer-verifier | `cumulative-reasoning` | reasoning |
| XoT | `everything-of-thoughts` | advanced-reasoning |
| MCTS reasoning | `everything-of-thoughts` | advanced-reasoning |
| thought propagation | `thought-propagation` | advanced-reasoning |
| analogical problem solving | `thought-propagation` | advanced-reasoning |
| step-back | `step-back-prompting` | advanced-reasoning |
| abstraction-first | `step-back-prompting` | advanced-reasoning |
| RaR | `rephrase-and-respond` | advanced-reasoning |
| question rewriting | `rephrase-and-respond` | advanced-reasoning |
| meta-prompting | `meta-prompting` | advanced-reasoning |
| expert orchestration | `meta-prompting` | advanced-reasoning |
| CoVe | `chain-of-verification` | verification |
| verification chain | `chain-of-verification` | verification |
| iterative refinement | `self-refine` | verification |
| critique-refine loop | `self-refine` | verification |
| verbal reinforcement | `reflexion` | verification |
| episodic memory | `reflexion` | verification |
| LLM debate | `multi-agent-debate` | verification |
| multi-agent verification | `multi-agent-debate` | verification |
| checklist verification | `checklist-prompting` | verification |
| cite-then-conclude | `grounding-via-sources` | verification |
| source-grounded | `grounding-via-sources` | verification |
| CoK | `chain-of-knowledge` | verification |
| knowledge chain | `chain-of-knowledge` | verification |
| CoN | `chain-of-note` | verification |
| reading notes | `chain-of-note` | verification |
| Self-RAG | `self-rag` | verification |
| self-reflective RAG | `self-rag` | verification |
| CRAG | `corrective-rag` | verification |
| corrective retrieval | `corrective-rag` | verification |
| S2A | `system-2-attention` | perception |
| System 2 Attention | `system-2-attention` | perception |
| SimToM | `simtom` | perception |
| perspective-taking | `simtom` | perception |
| DSP | `directional-stimulus` | perception |
| hint prompting | `directional-stimulus` | perception |
| function calling | `tool-augmented-prompting` | agents |
| tool use | `tool-augmented-prompting` | agents |
| pipeline prompting | `prompt-chaining` | agents |
| sequential chaining | `prompt-chaining` | agents |
| planner-worker | `planner-worker-solver` | agents |
| multi-agent orchestration | `planner-worker-solver` | agents |
| memory prompting | `memory-prompting` | agents |
| context window management | `memory-prompting` | agents |
| LMQL | `lmql` | prompt-programming |
| Guidance | `guidance` | prompt-programming |
| Outlines | `outlines` | prompt-programming |
| SGLang | `sglang` | prompt-programming |
| DSPy | `dspy` | optimization |
| OPRO | `opro` | optimization |
| APE | `ape` | optimization |
| TextGrad | `textgrad` | optimization |
| PromptBreeder | `promptbreeder` | optimization |
| EvoPrompt | `evoprompt` | optimization |
| ProTeGi | `protegi` | optimization |
| prompt tuning | `prompt-tuning` | soft-prompts |
| prefix tuning | `prefix-tuning` | soft-prompts |
| P-Tuning v2 | `p-tuning-v2` | soft-prompts |
| injection defense | `prompt-injection-defense` | security |
| sandwich defense | `prompt-injection-defense` | security |
| instruction hierarchy | `instruction-hierarchy` | security |
| guardrails | `sanitization-guardrails` | security |
| RLAIF | `constitutional-ai` | alignment |
| CAI | `constitutional-ai` | alignment |
| extended thinking | `extended-thinking-claude` | reasoning-tokens |
| thinking blocks | `extended-thinking-claude` | reasoning-tokens |
| o1 reasoning | `o1-o3-reasoning` | reasoning-tokens |
| o3 reasoning | `o1-o3-reasoning` | reasoning-tokens |
| DeepSeek R1 | `deepseek-r1` | reasoning-tokens |
| multimodal CoT | `multimodal-cot` | multimodal |
| vision prompting | `vision-language-prompting` | multimodal |

## Family Classification

| Family | Techniques |
|--------|-----------|
| Thought Generation | chain-of-thought, zero-shot-cot, chain-of-draft, buffer-of-thoughts, contrastive-cot, thread-of-thought, algorithm-of-thoughts, tab-cot, analogical-prompting, cumulative-reasoning |
| Thought Structure | tree-of-thoughts, graph-of-thoughts, everything-of-thoughts, skeleton-of-thought |
| Decomposition | least-to-most, plan-and-solve, self-ask, step-back-prompting, rephrase-and-respond, meta-prompting |
| Verification | chain-of-verification, self-refine, reflexion, multi-agent-debate, checklist-prompting |
| Grounding | context-stuffing, grounding-via-sources, chain-of-knowledge, chain-of-note, self-rag, corrective-rag |
| Tool Integration | react, rewoo, program-of-thoughts, tool-augmented-prompting |
| Optimization | dspy, opro, ape, textgrad, promptbreeder, evoprompt, protegi |
| Structured Output | output-format, prompt-scaffolding, prompt-frameworks |
| Parametric | prompt-tuning, prefix-tuning, p-tuning-v2 |
| Defense | prompt-injection-defense, instruction-hierarchy, sanitization-guardrails |
