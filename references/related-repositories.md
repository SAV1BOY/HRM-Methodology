# Related Repositories and Resources

> A curated list of open-source repositories, libraries, and community resources related to prompt engineering, LLM tooling, and AI orchestration. These resources complement the HRM Methodology.

---

## Prompt Engineering Guides

### Prompt Engineering Guide (DAIR.AI)

- **URL:** [https://www.promptingguide.ai/](https://www.promptingguide.ai/)
- **GitHub:** [dair-ai/Prompt-Engineering-Guide](https://github.com/dair-ai/Prompt-Engineering-Guide)
- **Description:** The most widely-referenced community guide to prompt engineering. Covers techniques from basic to advanced with examples for multiple models.
- **Strengths:** Broad coverage, regularly updated, multilingual, active community
- **Relationship to HRM:** HRM extends this guide's technique descriptions with machine-readable metadata, composability information, and agent-integration templates

### Awesome ChatGPT Prompts

- **URL:** [https://github.com/f/awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts)
- **Description:** Community-curated collection of ChatGPT prompt examples organized by use case. Focuses on role-based prompts and system prompts.
- **Strengths:** Large collection, practical examples, community contributions
- **Relationship to HRM:** Provides examples for the Role Prompting (A04) technique. HRM systematizes the patterns found in this collection.

### OpenAI Cookbook

- **URL:** [https://cookbook.openai.com/](https://cookbook.openai.com/)
- **GitHub:** [openai/openai-cookbook](https://github.com/openai/openai-cookbook)
- **Description:** Official OpenAI examples and best practices for using GPT models. Includes code examples, RAG implementations, and function calling patterns.
- **Strengths:** Official guidance, production-quality code, covers embeddings and fine-tuning
- **Relationship to HRM:** Source for tool-augmented prompting patterns and output format examples

### Anthropic Prompt Library

- **URL:** [https://docs.anthropic.com/en/prompt-library](https://docs.anthropic.com/en/prompt-library)
- **Description:** Anthropic's curated collection of effective prompts for Claude models. Includes system prompt patterns, XML tagging examples, and thinking protocols.
- **Strengths:** Model-specific optimization, prompt scaffolding patterns, extended thinking examples
- **Relationship to HRM:** Source for prompt scaffolding (A08), extended thinking (L01), and XML-based structuring patterns

---

## LLM Frameworks and Orchestration

### LangChain

- **URL:** [https://www.langchain.com/](https://www.langchain.com/)
- **GitHub:** [langchain-ai/langchain](https://github.com/langchain-ai/langchain)
- **Description:** The most popular framework for building LLM-powered applications. Provides abstractions for chains, agents, memory, retrieval, and tool use.
- **Strengths:** Comprehensive ecosystem, large community, extensive integrations
- **Relationship to HRM:** Implements many HRM techniques as composable components. LangChain Hub hosts reusable prompt templates.

### LangChain Hub

- **URL:** [https://smith.langchain.com/hub](https://smith.langchain.com/hub)
- **Description:** Community repository of reusable prompt templates and chains. Browse and share prompts tagged by technique and use case.
- **Relationship to HRM:** Complementary prompt template repository. HRM templates can be published to LangChain Hub for broader consumption.

### DSPy

- **URL:** [https://dspy-docs.vercel.app/](https://dspy-docs.vercel.app/)
- **GitHub:** [stanfordnlp/dspy](https://github.com/stanfordnlp/dspy)
- **Description:** Stanford NLP framework for programmatic prompt optimization. Replaces manual prompt engineering with declarative modules that are automatically compiled into effective prompts.
- **Strengths:** Automatic optimization, reproducibility, systematic evaluation, modular design
- **Relationship to HRM:** Implements optimization category (H01). DSPy modules correspond to HRM technique compositions. DSPy can automatically optimize HRM prompt templates.

### Guidance (Microsoft)

- **URL:** [https://github.com/guidance-ai/guidance](https://github.com/guidance-ai/guidance)
- **Description:** Interleaved generation and control flow for LLMs. Enables template-driven generation with branching, loops, and constrained output.
- **Strengths:** Fine-grained control over generation, template interleaving, multiple model backends
- **Relationship to HRM:** Implements prompt programming (G02). Guidance templates can encode HRM technique compositions as executable programs.

### Outlines

- **URL:** [https://github.com/dottxt-ai/outlines](https://github.com/dottxt-ai/outlines)
- **Description:** Structured generation for LLMs using finite-state machines. Guarantees that model output conforms to a JSON schema, regex pattern, or grammar.
- **Strengths:** Guaranteed valid output, works with open-source models, efficient constrained decoding
- **Relationship to HRM:** Implements prompt programming (G03) and strengthens output format control (A06).

### SGLang

- **URL:** [https://github.com/sgl-project/sglang](https://github.com/sgl-project/sglang)
- **Description:** Structured generation language for high-throughput LLM serving. Optimizes KV cache reuse and enables efficient multi-call pipelines.
- **Strengths:** Performance optimization, KV cache sharing across calls, RadixAttention
- **Relationship to HRM:** Implements prompt programming (G04). SGLang can accelerate multi-technique HRM pipelines through KV cache sharing.

---

## Agent Frameworks

### AutoGPT

- **GitHub:** [Significant-Gravitas/AutoGPT](https://github.com/Significant-Gravitas/AutoGPT)
- **Description:** Autonomous AI agent framework. Demonstrates the ReAct + Memory + Tool Use + Reflexion pattern at scale.
- **Relationship to HRM:** Production example of the Agent Orchestration playbook.

### CrewAI

- **GitHub:** [joaomdmoura/crewAI](https://github.com/joaomdmoura/crewAI)
- **Description:** Framework for orchestrating role-playing AI agents in collaborative task execution.
- **Relationship to HRM:** Implements the Planner-Worker-Solver (F03) and Multi-Agent Debate (D04) patterns.

### Semantic Kernel (Microsoft)

- **GitHub:** [microsoft/semantic-kernel](https://github.com/microsoft/semantic-kernel)
- **Description:** Microsoft's SDK for integrating LLMs into applications with plugins, planners, and memory.
- **Relationship to HRM:** Implements prompt chaining (F02), memory prompting (F04), and tool-augmented prompting (F01).

---

## Evaluation and Testing

### promptfoo

- **URL:** [https://www.promptfoo.dev/](https://www.promptfoo.dev/)
- **GitHub:** [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo)
- **Description:** Open-source tool for testing and evaluating LLM prompts. Supports A/B testing, regression testing, and red-teaming.
- **Relationship to HRM:** Essential tool for validating HRM technique selections and measuring quality gains from technique composition.

### Giskard

- **GitHub:** [Giskard-AI/giskard](https://github.com/Giskard-AI/giskard)
- **Description:** Testing framework for AI models with a focus on vulnerability detection, bias testing, and quality assurance.
- **Relationship to HRM:** Complements the production readiness and security review checklists.

---

## Resource Comparison Matrix

| Resource | Type | Coverage | Updatedness | Machine-Readable | Composability Info |
|----------|------|----------|-------------|-------------------|-------------------|
| HRM Methodology | Knowledge base | 75 techniques | Active | Yes (YAML) | Yes |
| Prompt Engineering Guide | Guide | ~30 techniques | Active | No | No |
| Awesome ChatGPT Prompts | Examples | Role prompts | Active | No | No |
| OpenAI Cookbook | Code examples | ~15 patterns | Active | Partially | No |
| Anthropic Prompt Library | Examples | ~20 patterns | Active | No | No |
| LangChain Hub | Templates | Variable | Active | Yes | Partially |
| DSPy | Framework | ~10 modules | Active | Yes | Yes |
