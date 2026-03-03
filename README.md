# HRM Methodology — Advanced Prompt Engineering Knowledge Base

> **The most comprehensive, machine-readable catalog of prompt engineering techniques.**
> Designed as the knowledge layer for the **HRM Agent** — an AI orchestrator that selects, chains, and applies prompt engineering methods to execute complex tasks.

## Taxonomy Overview

```
A. Foundations (10)          — Zero-shot, Few-shot, Role, Frameworks, Scaffolding
B. Reasoning (20)            — CoT, ToT, GoT, ReAct, CoD, BoT, SoT, PoT, ...
C. Advanced Reasoning (5)    — XoT, Thought Propagation, Step-Back, Meta-Prompting
D. Verification (10)         — CoVe, Self-Refine, Reflexion, Debate, RAG variants
E. Perception & Context (3)  — System 2 Attention, SimToM, Directional Stimulus
F. Agents & Tool Use (4)     — Tool-Augmented, Prompt Chaining, Planner-Worker
G. Prompt Programming (4)    — LMQL, Guidance, Outlines, SGLang
H. Optimization (7)          — DSPy, OPRO, APE, TextGrad, PromptBreeder, ...
I. Soft Prompts (3)          — Prompt Tuning, Prefix Tuning, P-Tuning v2
J. Security (3)              — Injection Defense, Instruction Hierarchy, Guardrails
K. Alignment (1)             — Constitutional AI
L. Reasoning Tokens (3)      — Extended Thinking, o1/o3, DeepSeek-R1
M. Multimodal (2)            — Multimodal CoT, Vision-Language Prompting
                               ─────────────────────────────
                               Total: 75 techniques
```

## Quick Start

### For Humans
1. Browse `techniques/` by category
2. Use `playbooks/` for end-to-end workflows
3. Check `checklists/` for quality assurance
4. Read `glossary.md` to find techniques by alias

### For the HRM Agent
1. Load `taxonomy.yaml` — discovers all techniques, their metadata, and file paths
2. Load the relevant technique `.md` file — gets full documentation with YAML frontmatter
3. Load the matching `templates/<category>/<id>.yaml` — gets the prompt skeleton
4. Compose techniques using `composes_with` metadata and `playbooks/`

## Repository Structure

```
HRM-Methodology/
├── README.md                  # This file
├── taxonomy.yaml              # Master registry — the HRM agent's entry point
├── glossary.md                # Alias → canonical ID mapping
├── CONTRIBUTING.md            # How to add new techniques
├── techniques/
│   ├── _TEMPLATE.md           # Standard template for technique docs
│   ├── foundations/            # Category A: 10 techniques
│   ├── reasoning/             # Category B: 20 techniques
│   ├── advanced-reasoning/    # Category C: 5 techniques
│   ├── verification/          # Category D: 10 techniques
│   ├── perception/            # Category E: 3 techniques
│   ├── agents/                # Category F: 4 techniques
│   ├── prompt-programming/    # Category G: 4 techniques
│   ├── optimization/          # Category H: 7 techniques
│   ├── soft-prompts/          # Category I: 3 techniques
│   ├── security/              # Category J: 3 techniques
│   ├── alignment/             # Category K: 1 technique
│   ├── reasoning-tokens/      # Category L: 3 techniques
│   └── multimodal/            # Category M: 2 techniques
├── templates/                 # Agent-loadable YAML prompt skeletons
│   ├── _schema.yaml
│   ├── foundations/
│   ├── reasoning/
│   ├── verification/
│   ├── agents/
│   └── security/
├── playbooks/                 # End-to-end workflow guides
├── checklists/                # Quality assurance checklists
├── references/                # Academic surveys, related repos
└── hrm-agent/                 # HRM agent integration docs
    └── examples/              # Example orchestration sessions
```

## Key References

| Resource | Description |
|----------|-------------|
| [The Prompt Report](https://arxiv.org/abs/2406.06608) | Schulhoff et al. 2024 — Systematic survey of prompting techniques |
| [Prompting Guide](https://www.promptingguide.ai/) | DAIR.AI — Community-maintained prompt engineering guide |
| [OpenAI Cookbook](https://cookbook.openai.com/) | Official OpenAI examples and best practices |
| [Anthropic Docs](https://docs.anthropic.com/) | Claude prompt engineering documentation |
| [DSPy](https://github.com/stanfordnlp/dspy) | Stanford NLP — Programmatic prompt optimization framework |

## License

MIT — See [LICENSE](LICENSE)
