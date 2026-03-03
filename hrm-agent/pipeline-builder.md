# HRM Agent: Pipeline Builder

> How the HRM Agent chains selected techniques into executable pipelines — dependency resolution, template instantiation, error handling, and execution.

---

## Overview

The Pipeline Builder takes the output of the Technique Selector (an ordered list of techniques) and constructs an executable pipeline. It handles:

1. **Dependency resolution** — ensuring each step has the inputs it needs
2. **Template instantiation** — loading and populating prompt templates
3. **Variable binding** — connecting outputs to inputs across steps
4. **Error handling** — retry logic, fallbacks, and graceful degradation
5. **Execution** — running the pipeline and collecting results

---

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────┐
│                   PIPELINE                           │
│                                                     │
│  ┌─────────┐     ┌─────────┐     ┌─────────┐      │
│  │ Step 1   │────►│ Step 2   │────►│ Step 3   │──►  │
│  │          │     │          │     │          │      │
│  │ template │     │ template │     │ template │      │
│  │ input    │     │ input    │     │ input    │      │
│  │ output   │     │ output   │     │ output   │      │
│  │ config   │     │ config   │     │ config   │      │
│  └─────────┘     └─────────┘     └─────────┘      │
│       │               │               │             │
│       ▼               ▼               ▼             │
│  ┌─────────┐     ┌─────────┐     ┌─────────┐      │
│  │ output_1 │     │ output_2 │     │ output_3 │      │
│  └─────────┘     └─────────┘     └─────────┘      │
│                                                     │
│  ┌──────────────────────────────────────────┐      │
│  │           Execution Context               │      │
│  │                                           │      │
│  │  variables: {step outputs, user input}   │      │
│  │  config: {model, temperature, limits}    │      │
│  │  metrics: {tokens, latency, calls}       │      │
│  │  errors: {failures, retries}             │      │
│  └──────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────┘
```

---

## Step 1: Dependency Resolution

Each technique has implicit input requirements. The builder resolves these into a dependency graph.

### Input/Output Contracts

```yaml
technique_contracts:
  step-back-prompting:
    inputs: [user_query]
    outputs: [background_principles, abstracted_context]

  chain-of-thought:
    inputs: [user_query, background_context?]  # ? = optional
    outputs: [reasoning_trace, conclusion]

  chain-of-verification:
    inputs: [draft_output]
    outputs: [verification_results, corrected_output]

  self-refine:
    inputs: [draft_output]
    outputs: [critique, refined_output]

  output-format:
    inputs: [content, format_specification]
    outputs: [formatted_output]

  few-shot:
    inputs: [user_query, examples]
    outputs: [calibrated_output]

  role-prompting:
    inputs: [user_query, persona_description]
    outputs: [persona_context, initial_approach]

  react:
    inputs: [user_goal, available_tools, memory?]
    outputs: [trajectory, final_result]

  plan-and-solve:
    inputs: [task_description, constraints?]
    outputs: [implementation_plan]

  program-of-thoughts:
    inputs: [task_description, plan?]
    outputs: [code_output, execution_result?]

  checklist-prompting:
    inputs: [content_to_verify, checklist_criteria]
    outputs: [checklist_results, corrected_content?]

  skeleton-of-thought:
    inputs: [task_description, approach?]
    outputs: [skeleton, expanded_content]

  multi-agent-debate:
    inputs: [draft_content, agent_roles]
    outputs: [debate_results, consensus_improvements]
```

### Resolution Algorithm

```
FOR each step in pipeline (ordered):
  FOR each required_input in step.inputs:
    IF required_input == "user_query" or "user_goal" or "task_description":
      BIND to original user input
    ELIF required_input matches an output from a previous step:
      BIND to that step's output variable
    ELIF required_input is optional (marked with ?):
      BIND to null (skip)
    ELSE:
      ERROR: unresolved dependency
      → Try reordering steps
      → If still unresolved, add a preparatory step or ask user
```

### Example Resolution

```
Pipeline: Step-Back → CoT → CoVe → Self-Refine → Output-Format

Step 1 (Step-Back):
  input: user_query ← BIND(user_input)
  output: background_principles

Step 2 (CoT):
  input: user_query ← BIND(user_input)
  input: background_context ← BIND(step_1.background_principles)
  output: reasoning_trace, conclusion

Step 3 (CoVe):
  input: draft_output ← BIND(step_2.reasoning_trace + step_2.conclusion)
  output: corrected_output

Step 4 (Self-Refine):
  input: draft_output ← BIND(step_3.corrected_output)
  output: refined_output

Step 5 (Output-Format):
  input: content ← BIND(step_4.refined_output)
  input: format_specification ← BIND(user_format_preference OR default)
  output: formatted_output ← FINAL RESULT
```

---

## Step 2: Template Instantiation

For each step, load the prompt template and populate placeholders.

### Template Loading

```
FOR each step in pipeline:
  # 1. Check for YAML template
  template_path = taxonomy[step.technique].template
  IF template_path exists:
    template = load_yaml(template_path)

  # 2. Fall back to technique doc's template section
  ELIF technique_doc has "## Template" section:
    template = extract_template_from_doc(technique_doc_path)

  # 3. Fall back to playbook template
  ELIF matching_playbook has template for this technique:
    template = extract_from_playbook(playbook, step.technique)

  # 4. Fall back to generic template
  ELSE:
    template = generic_template(step.technique)
```

### Variable Substitution

```
FOR each placeholder in template:
  # Match {variable_name} patterns
  IF variable_name in execution_context.variables:
    REPLACE with execution_context.variables[variable_name]
  ELIF variable_name in pipeline.config:
    REPLACE with pipeline.config[variable_name]
  ELIF variable_name has a default value:
    REPLACE with default
  ELSE:
    WARN: unbound variable {variable_name}
    REPLACE with "[PLACEHOLDER: {variable_name}]"
```

---

## Step 3: Execution

Run each step sequentially, managing the execution context.

### Execution Loop

```
execution_context = {
  variables: {user_input: task},
  config: {model, temperature, max_tokens},
  metrics: {total_tokens: 0, total_latency: 0, api_calls: 0},
  errors: []
}

FOR each step in pipeline:
  # 1. Prepare the prompt
  prompt = instantiate_template(step, execution_context)

  # 2. Configure the LLM call
  call_config = {
    model: step.model_override OR pipeline.config.model,
    temperature: step.temperature_override OR pipeline.config.temperature,
    max_tokens: step.max_tokens OR estimate_needed_tokens(step)
  }

  # 3. Execute with retry
  result = execute_with_retry(prompt, call_config, max_retries=3)

  # 4. Validate output
  IF step.expected_output_format:
    validate(result, step.expected_output_format)

  # 5. Store output
  execution_context.variables[step.output_name] = result

  # 6. Update metrics
  execution_context.metrics.total_tokens += result.token_count
  execution_context.metrics.total_latency += result.latency
  execution_context.metrics.api_calls += 1

  # 7. Budget check
  IF execution_context.metrics.total_tokens > pipeline.token_budget:
    WARN: approaching token budget
    IF remaining steps are optional:
      SKIP remaining optional steps

RETURN execution_context.variables[final_step.output_name]
```

---

## Step 4: Error Handling

### Retry Strategy

```
FUNCTION execute_with_retry(prompt, config, max_retries):
  FOR attempt in 1..max_retries:
    TRY:
      result = llm_call(prompt, config)
      RETURN result
    CATCH RateLimitError:
      WAIT exponential_backoff(attempt)
      CONTINUE
    CATCH TimeoutError:
      IF attempt < max_retries:
        config.max_tokens *= 0.8  # reduce output expectation
        CONTINUE
      ELSE:
        RAISE
    CATCH MalformedOutputError:
      IF attempt < max_retries:
        prompt += "\n\nIMPORTANT: Your previous response was malformed. Please ensure valid {expected_format} output."
        CONTINUE
      ELSE:
        RAISE
```

### Fallback Strategies

```
IF step fails after all retries:

  Strategy 1 — SKIP (if step is optional):
    Mark step as skipped
    Bind next step's input to previous step's output
    CONTINUE pipeline

  Strategy 2 — SIMPLIFY (if a simpler technique exists):
    Replace failing technique with simpler alternative
    e.g., Replace ToT with CoT, Replace Multi-Agent Debate with Self-Refine
    Rebuild step with simpler template
    RETRY

  Strategy 3 — DECOMPOSE (if step is too complex):
    Split the failing step into 2 sub-steps
    e.g., If CoVe fails on a large document, split into per-section verification
    RETRY each sub-step

  Strategy 4 — ABORT (if step is critical):
    Return partial results with error explanation
    Log failure for Reflector analysis
```

---

## Step 5: Pipeline Optimization

### Pre-Execution Optimization

Before running, the builder can optimize the pipeline:

```
# 1. Parallel execution detection
IF step_A and step_B have no data dependency:
  Mark as parallelizable
  Execute simultaneously to reduce latency

# 2. Template caching
IF multiple steps use the same base template:
  Cache the template, only swap variables

# 3. Context window estimation
total_context = SUM(estimated_prompt_size for all steps)
IF total_context > model.context_window * 0.8:
  WARN: pipeline may exceed context window
  Consider: summarizing intermediate outputs, using a larger model,
  or splitting into sub-pipelines

# 4. Cost estimation
estimated_cost = SUM(step.estimated_tokens * model.price_per_token)
IF estimated_cost > budget:
  Suggest: remove lowest-impact step, use cheaper model for
  verification steps, reduce self-refine iterations
```

### Post-Execution Analysis

After running, the builder reports:

```yaml
pipeline_report:
  status: success | partial | failed
  steps_completed: 5/5
  total_tokens: 4823
  total_latency_seconds: 27.3
  api_calls: 7
  errors: []
  quality_estimate: high  # based on checklist pass rate
  optimization_notes:
    - "Steps 1-2 could be parallelized (no dependency)"
    - "Self-Refine used 2 iterations; 1 may have been sufficient"
```

---

## Example Pipeline Construction

### Input: Research Task

```
Task: "Compare the performance characteristics of SQLite, DuckDB, and
       ClickHouse for analytical queries on datasets under 10GB"
Profile: type=reasoning, complexity=complex, quality=high,
         latency=relaxed, tools=none
```

### Built Pipeline

```yaml
pipeline:
  steps:
    - technique: step-back-prompting
      template: templates/reasoning/step-back.yaml
      variables:
        user_query: "{original_task}"
      output: background_principles

    - technique: chain-of-thought
      template: templates/reasoning/chain-of-thought.yaml
      variables:
        background_context: "{background_principles}"
        user_query: "{original_task}"
      output: analysis_draft

    - technique: chain-of-verification
      template: templates/verification/chain-of-verification.yaml
      variables:
        draft_output: "{analysis_draft}"
      output: verified_analysis

    - technique: self-refine
      template: templates/verification/self-refine.yaml
      variables:
        draft_output: "{verified_analysis}"
      output: refined_analysis
      max_iterations: 2

    - technique: output-format
      template: templates/foundations/output-format.yaml
      variables:
        content: "{refined_analysis}"
        format_specification: "comparison table + narrative analysis"
      output: final_report
```
