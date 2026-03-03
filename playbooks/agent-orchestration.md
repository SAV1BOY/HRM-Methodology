# Playbook: Agent Orchestration

> **Pipeline:** ReAct → Memory Prompting → Tool-Augmented Prompting → Reflexion
>
> **Best for:** Autonomous task completion, multi-step research agents, coding assistants, data analysis pipelines, workflow automation, customer support bots.

## Workflow Diagram

```
                    ┌─────────────────────┐
                    │   Agent Task        │
                    └─────────┬───────────┘
                              │
                    ┌─────────▼───────────┐
                    │  1. ReAct            │  Thought → Action →
                    │     Loop            │  Observation cycle
                    └─────────┬───────────┘
                              │
                    ┌─────────▼───────────┐
                    │  2. Memory           │  Persist and retrieve
                    │     Prompting       │  context across turns
                    └─────────┬───────────┘
                              │
                    ┌─────────▼───────────┐
                    │  3. Tool-Augmented   │  Invoke external tools,
                    │     Prompting       │  APIs, and functions
                    └─────────┬───────────┘
                              │
                    ┌─────────▼───────────┐
                    │  4. Reflexion        │  Reflect on trajectory,
                    │                     │  learn from failures
                    └─────────┴───────────┘
                              │
                         ┌────▼────┐
                         │ Success? │
                         └────┬────┘
                          No  │  Yes
                    ┌─────────▼───┐  │
                    │ Update memory│  │
                    │ & retry      │  │
                    └─────────────┘  ▼
                                  Done
```

## Technique Selection Rationale

| Step | Technique | Why This Technique |
|------|-----------|-------------------|
| 1 | ReAct | The Thought-Action-Observation loop provides a structured framework for interleaving reasoning with actions — the model decides what to do, does it, observes the result, and reasons about next steps |
| 2 | Memory Prompting | Agents operating over multiple turns need persistent memory — summaries of past actions, retrieved context, and accumulated knowledge that survives context window limits |
| 3 | Tool-Augmented Prompting | Agents must interact with external systems — search engines, databases, APIs, code interpreters, file systems — tool calling formalizes this interaction |
| 4 | Reflexion | After task completion (or failure), the agent reflects on its trajectory, identifies what went wrong, and stores lessons learned for future attempts |

## Step-by-Step Templates

### Step 1: ReAct Loop

**Purpose:** Structure the agent's reasoning and action cycle with explicit thought, action, and observation phases.

```
You are an autonomous agent tasked with completing the following goal.
Use the Thought → Action → Observation loop to make progress.

GOAL:
{agent_task}

AVAILABLE ACTIONS:
- search(query): Search for information
- read(url): Read content from a URL or file
- write(path, content): Write content to a file
- execute(code): Execute code and return output
- ask_user(question): Ask the user for clarification
- finish(result): Complete the task with final result

MEMORY (from previous attempts):
{memory_context}

RULES:
1. Always start with a Thought explaining your reasoning
2. Choose exactly one Action per turn
3. Wait for the Observation before your next Thought
4. If stuck for more than 3 turns, try a different approach
5. Call finish() when the task is complete

Begin:

Thought 1: Let me analyze the task and determine the first step...
Action 1: {action_name}({parameters})
Observation 1: {result}

Thought 2: Based on the observation, I should...
Action 2: {action_name}({parameters})
Observation 2: {result}

[Continue until finish() is called]
```

### Step 2: Memory Prompting

**Purpose:** Manage context across turns by maintaining structured memory — working memory for current task, episodic memory for past attempts, semantic memory for learned facts.

```
MEMORY MANAGEMENT PROTOCOL:

You maintain three types of memory:

## Working Memory (current task context)
Capacity: Last {N} Thought-Action-Observation turns
Update: Automatically maintained by the ReAct loop
Contents:
{recent_turns}

## Episodic Memory (past attempts and outcomes)
Capacity: {max_episodes} episodes, summarized
Update: After each task completion or failure
Contents:
{episodic_summaries}

## Semantic Memory (learned facts and procedures)
Capacity: {max_facts} key-value facts
Update: When new reliable information is discovered
Contents:
{fact_store}

MEMORY OPERATIONS:
- STORE_EPISODIC(summary): Save a summary of this attempt
- STORE_FACT(key, value): Save a learned fact
- RETRIEVE(query): Search all memory types for relevant context
- SUMMARIZE_AND_COMPRESS: When working memory exceeds capacity,
  summarize older turns and move to episodic memory

Before each Thought step, check if relevant memory exists:
RETRIEVE("{current_subtask}")
```

### Step 3: Tool-Augmented Prompting

**Purpose:** Define and invoke external tools with structured function calling.

```
You have access to the following tools. Use them by generating a
function call in the specified format.

TOOLS:
{tool_definitions}

Each tool definition includes:
- name: The function name
- description: What the tool does
- parameters: JSON Schema for the input
- returns: Description of the output format
- errors: Possible error conditions

TOOL CALLING FORMAT:
```json
{
  "tool": "{tool_name}",
  "parameters": {
    "{param_1}": "{value_1}",
    "{param_2}": "{value_2}"
  }
}
```

TOOL CALLING RULES:
1. Always validate parameters before calling a tool
2. Handle tool errors gracefully — retry with different parameters
   or try an alternative tool
3. Do NOT call tools speculatively — have a clear reason for each call
4. If a tool returns unexpected results, reason about why before
   proceeding
5. Chain tool calls when one output feeds into another
6. Prefer specific tools over general ones (e.g., use a database
   query tool over a generic search when accessing structured data)

CURRENT TOOL CALL:
Thought: I need to {reason_for_tool_use}
Tool Call:
```json
{tool_invocation}
```
Result: {tool_output}
```

### Step 4: Reflexion

**Purpose:** After the task is complete (or failed), reflect on the trajectory to extract lessons for future attempts.

```
You have completed (or failed) the following task. Reflect on your
performance.

TASK:
{agent_task}

TRAJECTORY (all Thought-Action-Observation turns):
{full_trajectory}

OUTCOME:
{success_or_failure}

REFLECTION PROTOCOL:

1. OUTCOME ASSESSMENT
   - Did you achieve the goal? Fully, partially, or not at all?
   - How many steps did it take vs. the minimum possible?
   - What was the total cost (tool calls, tokens, time)?

2. FAILURE ANALYSIS (if applicable)
   - At which step did things go wrong?
   - What was the root cause? (wrong tool, bad reasoning, missing info)
   - Could you have detected the problem earlier?

3. STRATEGY REVIEW
   - What strategy did you use? Was it the best one?
   - What alternative strategies could you have used?
   - Were there any unnecessary steps?

4. LESSONS LEARNED
   - List 3-5 specific, actionable lessons
   - Format: "When [situation], I should [action] because [reason]"

5. MEMORY UPDATES
   - What should be stored in episodic memory for next time?
   - What new facts should be stored in semantic memory?
   - What tool-specific knowledge was gained?

STORE the following for future tasks:
STORE_EPISODIC("{task_summary}: {lessons}")
STORE_FACT("{key_insight}", "{value}")
```

## Walk-Through Example

**Task:** "Research the top 5 open-source vector databases, compare their performance benchmarks, and produce a recommendation report for a team building a RAG pipeline."

---

### Step 1 Output: ReAct Loop

> **Thought 1:** I need to identify the top open-source vector databases. Let me search for recent comparisons and benchmarks.
> **Action 1:** search("top open source vector databases 2025 comparison benchmarks")
> **Observation 1:** Results mention Milvus, Qdrant, Weaviate, Chroma, pgvector, LanceDB, Pinecone (not open-source)...
>
> **Thought 2:** I have a candidate list. Let me narrow to clearly open-source options and find benchmark data for each. I should start with the ANN Benchmarks project.
> **Action 2:** read("https://ann-benchmarks.com/")
> **Observation 2:** ANN Benchmarks shows performance data for various algorithms...
>
> **Thought 3:** I need more specific production-oriented benchmarks. Let me search for VectorDBBench or similar.
> **Action 3:** search("VectorDBBench 2025 results Milvus Qdrant Weaviate")
> **Observation 3:** VectorDBBench results show QPS, latency, and recall metrics...
>
> [Continues for 8-12 turns, gathering data on each database]

### Step 2 Output: Memory Management

> **Working Memory:** Current research progress — 5 databases identified, benchmark data collected for 3/5.
>
> **Semantic Memory Updated:**
> - STORE_FACT("milvus_qps", "~1200 QPS at 95% recall on SIFT-1M")
> - STORE_FACT("qdrant_feature", "supports hybrid search with sparse+dense vectors")
> - STORE_FACT("chroma_limitation", "not recommended for >1M vectors in production")
>
> **Context Compression:** Turns 1-5 summarized to free working memory for deeper analysis.

### Step 3 Output: Tool-Augmented Actions

> **Tool calls made:**
> - `search()` — 6 calls for research queries
> - `read()` — 4 calls for documentation pages
> - `execute()` — 1 call to format comparison data into a markdown table
> - `write()` — 1 call to save the draft report
> - `finish()` — 1 call with the final recommendation

### Step 4 Output: Reflexion

> **Outcome:** SUCCESS — comprehensive comparison report produced in 13 steps.
>
> **Strategy Review:** Started too broad (searched for "top vector databases" generally). Should have immediately targeted benchmark-specific sources.
>
> **Lessons Learned:**
> 1. When researching database comparisons, start with benchmark aggregator sites (VectorDBBench, ANN Benchmarks) rather than general search
> 2. When a tool returns too much data, summarize immediately rather than storing raw output
> 3. When comparing N items, create the comparison table structure early and fill it in systematically rather than researching each item fully before starting the next
>
> **Memory Updates:**
> - STORE_EPISODIC("vector-db-research: Use benchmark aggregators first; build comparison table early; summarize tool output immediately")
> - STORE_FACT("vector_db_benchmarks", "VectorDBBench and ANN Benchmarks are primary sources")

## Decision Points

```
                          ┌──────────────────┐
                          │ Agent task        │
                          └──────┬───────────┘
                                 │
                    ┌────────────▼────────────┐
                    │ Does the task require    │
                    │ external information or  │
                    │ actions?                 │
                    └────┬──────────────┬──────┘
                     Yes │              │ No
                         ▼              ▼
                   ReAct + Tools     Pure reasoning
                                    (use CoT playbook)
                         │
                    ┌────▼───────────────────┐
                    │ Will the task span      │
                    │ many turns (>5)?        │
                    └────┬──────────────┬─────┘
                     Yes │              │ No
                         ▼              ▼
                   Full Memory       Working Memory
                   (all 3 types)     only
                         │
                    ┌────▼───────────────────┐
                    │ Is this a recurring     │
                    │ task type?              │
                    └────┬──────────────┬─────┘
                     Yes │              │ No
                         ▼              ▼
                   Reflexion          Skip Reflexion
                   (learn for next)   (one-off task)
```

## Customization Options

| Variation | Modification |
|-----------|-------------|
| **Simple agent** | ReAct + Tools only — skip Memory and Reflexion for single-session tasks |
| **High reliability** | Add Self-Consistency (run agent 3 times, take consensus result) |
| **Cost-efficient** | Use ReWOO instead of ReAct — plan all actions upfront, execute in batch |
| **Human-in-the-loop** | Add approval gates before destructive actions (write, execute, submit) |
| **Multi-agent** | Replace single ReAct with Planner-Worker-Solver — planner routes sub-tasks to specialist workers |
| **Persistent agent** | Extend Memory with external storage (database, vector store) for cross-session persistence |

## Cost Estimate

| Step | API Calls | Token Overhead | Latency |
|------|-----------|---------------|---------|
| ReAct Loop | 5-20 turns | ~500/turn | Variable |
| Memory Management | 1-3 | ~300/operation | Low |
| Tool Calls | 3-15 | ~200/call + tool | Variable |
| Reflexion | 1 | ~800 output | Low |
| **Total** | **10-40** | **~5000-15000 tokens** | **~60-300s** |
