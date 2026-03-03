---
id: tool-augmented-prompting
name: "Tool-Augmented Prompting (Toolformer)"
aliases: ["Toolformer", "Tool Use", "Function Calling", "Tool-Augmented LLM", "API-Augmented Prompting"]
category: agents
family: tool-use
year: 2023
authors: ["Timo Schick", "Jane Dwivedi-Yu", "Roberto Dessì", "Roberta Raileanu", "Maria Lomeli", "Luke Zettlemoyer", "Nicola Cancedda", "Thomas Scialom"]
paper: "https://arxiv.org/abs/2302.04761"
paper_title: "Toolformer: Language Models Can Teach Themselves to Use Tools"
venue: "NeurIPS 2023"
code: null

complexity: medium
token_cost: variable
latency: variable
num_calls: variable

requires_examples: false
requires_tools: true
requires_training: false
model_agnostic: false

best_for: ["real-time data retrieval", "mathematical computation", "code execution", "API integration", "knowledge-grounded generation", "multi-step task automation"]
avoid_when: ["no external tools available", "pure reasoning tasks", "offline environments", "simple factual recall within training data", "tool latency is unacceptable"]
composes_with: ["chain-of-thought", "react", "planner-worker-solver", "prompt-chaining", "retrieval-augmented-generation"]

tags: ["agents", "tools", "function-calling", "api", "augmentation", "external-knowledge", "computation"]
---

# Tool-Augmented Prompting (Toolformer)

> **One-line summary:** Equip LLMs with the ability to call external tools (calculators, search engines, APIs, code interpreters) by defining tool interfaces in the prompt and letting the model decide when and how to invoke them.

## Overview

Large language models are powerful text generators, but they have fundamental limitations: they cannot reliably perform arithmetic, their knowledge has a training cutoff date, and they cannot interact with external systems. Tool-Augmented Prompting addresses these limitations by teaching the model to recognize when it needs an external tool, generate the appropriate tool call, and incorporate the tool's response into its ongoing generation.

The Toolformer paper by Schick et al. (2023) demonstrated that LLMs can learn to use tools in a self-supervised manner --- the model itself decides when a tool call would be helpful and generates the appropriate API invocation. While the paper focused on fine-tuning, the broader paradigm has been adopted by all major LLM providers through "function calling" or "tool use" features. In the prompting-only version, tool definitions and usage patterns are provided in the prompt or system message, and the model generates structured tool calls that an orchestration layer intercepts, executes, and feeds back.

The technique transforms the LLM from a closed text generator into an open agent that can interface with the external world. This is foundational to modern AI agent architectures: nearly every production agent system relies on some form of tool-augmented prompting to bridge the gap between language understanding and real-world action.

## How It Works

1. **Tool Definition:** Define available tools with their names, descriptions, parameter schemas, and return types. These definitions are placed in the system message or prompt preamble.
2. **Task Presentation:** Present the user's task or question to the model alongside the tool definitions.
3. **Tool Call Generation:** The model determines if a tool is needed and generates a structured tool call (typically JSON) with the appropriate function name and arguments.
4. **Tool Execution:** An orchestration layer intercepts the tool call, executes the corresponding function, and captures the result.
5. **Result Integration:** The tool result is fed back to the model, which incorporates it into its ongoing response. The model may make additional tool calls if needed.
6. **Final Response:** Once all necessary tool calls are resolved, the model produces the final response to the user.

### Diagram

```
┌────────────────────┐
│  Tool Definitions   │
│  + User Query       │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  LLM Decides:      │
│  Tool needed?       │
├──────────┬─────────┤
│  YES     │   NO    │
└────┬─────┘   └──┬──┘
     │            │
     ▼            │
┌──────────┐      │
│ Generate │      │
│ Tool Call│      │
│ (JSON)   │      │
└────┬─────┘      │
     │            │
     ▼            │
┌──────────┐      │
│ Execute  │      │
│ Tool     │      │
└────┬─────┘      │
     │            │
     ▼            │
┌──────────┐      │
│ Return   │      │
│ Result   │      │
└────┬─────┘      │
     │            │
     └─────┬──────┘
           │
           ▼
   ┌──────────────┐
   │ Final Answer  │
   └──────────────┘
```

## Template

**System message with tool definitions:**
```
You have access to the following tools:

1. **calculator(expression: str) -> str**
   Evaluates a mathematical expression and returns the result.
   Use for any arithmetic, algebra, or numerical computation.

2. **search(query: str) -> str**
   Searches the web and returns relevant results.
   Use for current events, real-time data, or facts you are unsure about.

3. **code_exec(language: str, code: str) -> str**
   Executes code in the specified language and returns stdout.
   Use for complex computations, data processing, or algorithms.

When you need a tool, respond with a JSON tool call:
{{"tool": "<tool_name>", "args": {{"param": "value"}}}}

After receiving the tool result, incorporate it into your response.

User query: {query}
```

## Examples

### Example 1: Mathematical Computation

**Input:**
```
You have access to the following tools:

1. calculator(expression: str) -> str
   Evaluates a mathematical expression.

What is the compound interest on $10,000 at 5% annual rate
compounded monthly for 3 years?
```

**Output (Model generates tool call):**
```
I need to calculate compound interest using the formula A = P(1 + r/n)^(nt).

{"tool": "calculator", "args": {"expression": "10000 * (1 + 0.05/12) ** (12*3)"}}
```

**Tool result:**
```
11614.722313334678
```

**Final output:**
```
The compound interest on $10,000 at 5% annual rate compounded monthly for
3 years results in a final amount of $11,614.72. The interest earned is
$11,614.72 - $10,000.00 = $1,614.72.
```

### Example 2: Real-Time Information Retrieval

**Input:**
```
You have access to the following tools:

1. search(query: str) -> str
   Searches the web for current information.

2. calculator(expression: str) -> str
   Evaluates a mathematical expression.

What is the current population of Tokyo and how does it compare
to New York City as a percentage?
```

**Output (Model generates first tool call):**
```
Let me look up the current population figures.

{"tool": "search", "args": {"query": "current population Tokyo metropolitan area 2024"}}
```

**Tool result:**
```
The Tokyo metropolitan area has a population of approximately 37.4 million
people as of 2024, making it the most populous metropolitan area in the world.
```

**Output (Model generates second tool call):**
```
{"tool": "search", "args": {"query": "current population New York City metropolitan area 2024"}}
```

**Tool result:**
```
The New York City metropolitan area has a population of approximately 19.5
million people as of 2024.
```

**Output (Model generates third tool call):**
```
{"tool": "calculator", "args": {"expression": "19.5 / 37.4 * 100"}}
```

**Tool result:**
```
52.13903743315508
```

**Final output:**
```
Tokyo's metropolitan area has approximately 37.4 million residents, while
New York City's metropolitan area has about 19.5 million. New York City's
population is roughly 52.1% of Tokyo's, meaning Tokyo is nearly twice the
size of NYC by population.
```

## When to Use

- Tasks requiring real-time or up-to-date information beyond the training cutoff
- Mathematical computations where accuracy is critical
- Multi-step tasks that involve interacting with external systems (databases, APIs)
- Code generation and execution for data analysis or algorithmic tasks
- Any task where the LLM's parametric knowledge is insufficient or unreliable
- Building agent systems that need to take actions in the real world

## When to Avoid

- Pure reasoning or creative writing tasks with no external data needs
- Environments where external tool access is restricted or unavailable
- When tool latency would make the response unacceptably slow
- Simple factual questions well within the model's training data
- High-security contexts where arbitrary tool execution poses risks
- Tasks where tool call errors could have serious consequences without human review

## Cost & Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Token overhead | +100-500 tokens | Tool definitions in system message |
| Latency | Variable | Depends on tool execution time (ms to seconds) |
| Quality gain | Significant | Eliminates hallucination for factual/computational queries |
| Reliability | Medium-High | Model may generate malformed tool calls |
| API calls | Variable | 1 base + N tool round-trips |
| Implementation | Medium | Requires orchestration layer for tool execution |

## Variants

- **Toolformer (Fine-tuned):** The original paper's approach where the model is fine-tuned to generate tool calls inline within text, using special tokens like `[Calculator(3+5)→8]`.
- **OpenAI Function Calling:** Structured tool definitions in the API with dedicated message roles for tool calls and responses.
- **Anthropic Tool Use:** XML-based tool definitions with structured tool_use content blocks.
- **ReAct-style Tool Use:** Interleaves Thought-Action-Observation steps with tool calls for more transparent reasoning.
- **Parallel Tool Calling:** Multiple independent tool calls executed simultaneously to reduce latency.
- **Constrained Tool Calling:** Restrict which tools are available based on the task context or user permissions.

## Composability

- **Tool Use + Chain-of-Thought:** The model reasons step-by-step about which tools to use and in what order before executing.
- **Tool Use + ReAct:** Formalize the think-act-observe loop with explicit reasoning traces between tool calls.
- **Tool Use + Planner-Worker-Solver:** A planner decides which tools to call, workers execute them, and a solver synthesizes results.
- **Tool Use + RAG:** Retrieval is itself a tool; the model decides when to search vs. answer from parametric knowledge.
- **Tool Use + Prompt Chaining:** Each stage in a pipeline may have access to different tools appropriate for that stage.

## Limitations

- Models may hallucinate tool calls to non-existent functions or pass invalid arguments
- Tool definitions consume context window tokens, limiting space for actual content
- Sequential tool calls add significant latency (each requires a round-trip)
- Error handling is challenging: tool failures can derail the entire generation
- Security risks from arbitrary code execution or API calls without proper sandboxing
- Model may over-rely on tools for tasks it could handle internally, wasting resources
- Different model providers have incompatible tool calling formats
- No standardized way to express complex tool dependencies or workflows

## Sources

- **Primary:** [Toolformer: Language Models Can Teach Themselves to Use Tools](https://arxiv.org/abs/2302.04761) — Schick et al., 2023
- **Related:** [ART: Automatic multi-step reasoning and tool-use for large language models](https://arxiv.org/abs/2303.09014) — Paranjape et al., 2023
- **Related:** [Gorilla: Large Language Model Connected with Massive APIs](https://arxiv.org/abs/2305.15334) — Patil et al., 2023
- **Industry:** [OpenAI Function Calling Documentation](https://platform.openai.com/docs/guides/function-calling) — OpenAI, 2023
