# Delegation Protocols

> How the HRM Architect hands off work to different execution modes. Each mode has specific handoff requirements, monitoring expectations, and result collection procedures.

---

## Protocol Overview

| Mode | Target | Handoff Template | Monitoring | Result Collection |
|------|--------|-----------------|------------|------------------|
| Single | Agent directly | agent-handoff | Minimal (wait for completion) | Direct result |
| Parallel | dispatching-parallel-agents | agent-handoff per task | Wait for all | Merge results |
| Swarm | swarm-orchestrator | swarm-dispatch | Phase-by-phase gates | Orchestrator merges |
| Teams | agent-teams-protocol | team-kickoff | Team Lead reports | Team Lead delivers |
| Squad | Squad chief | squad-brief | Chief reports | Chief delivers |

---

## Single Agent Protocol

**When**: 1 workstream, simple task, Bloom 1-3.

```
1. PREPARE: Run Prompt Forge for dispatch_context(dispatch_type=workstream-agent, granularity=task)
   → Forge returns ForgeOutput with tier-appropriate technique pipeline
   → Inject into agent-handoff template
2. DISPATCH: Spawn agent with prompt
3. WAIT: Agent executes autonomously
4. VERIFY: Run gate-runner (levels 1-2)
5. DELIVER: Return result to user
```

**Prompt generation**: Prompt Forge determines tier based on hrm_mode and generates technique pipeline.

---

## Parallel Agents Protocol

**When**: 2+ independent workstreams, no peer communication needed.

```
1. PREPARE: For each workstream, run Prompt Forge:
   forge(dispatch_type=workstream-agent, granularity=task) → ForgeOutput per workstream
   → Inject each into agent-handoff template
2. DISPATCH: Use dispatching-parallel-agents skill to launch all simultaneously
3. WAIT: All agents execute in parallel
4. COLLECT: Gather results as agents complete
5. VERIFY: Run gate-runner per workstream (level 2), then cross-workstream (level 3)
6. MERGE: Combine results
7. DELIVER: Return merged result to user
```

**Key rule**: Zero file ownership overlap. Each agent works on independent files.

---

## Swarm Protocol

**When**: 3+ workstreams with sequential dependencies, need phased execution.

```
1. PREPARE:
   a. For each workstream: forge(dispatch_type=swarm-member, granularity=subtask) → ForgeOutput
   b. Generate swarm-dispatch plan with execution phases (each agent block includes forged prompt)
   c. Determine phase ordering from dependency graph
2. DISPATCH: Send swarm-dispatch to swarm-orchestrator
3. PHASE LOOP:
   a. Orchestrator launches phase N agents
   b. Agents execute
   c. Orchestrator collects results
   d. HRM runs gate-runner for completed workstreams
   e. If gate passes: proceed to phase N+1
   f. If gate fails: HRM directs backtracking
4. VERIFY: Run full verification cascade after last phase
5. DELIVER: Orchestrator provides merged result
```

**Failure handling**:
- Agent failure: Orchestrator selects fallback from registry (same archetype)
- Phase failure: HRM re-plans affected phases
- 2+ failures: Escalate to HRM for plan revision

---

## Agent Teams Protocol

**When**: 2-5 sustained workstreams with peer-to-peer communication needs.

```
1. PREPARE:
   a. forge(dispatch_type=team-lead, granularity=task) → ForgeOutput for Team Lead brief
   b. For each teammate: forge(dispatch_type=team-member, granularity=subtask) → ForgeOutput
   c. Inject ForgeOutputs into team-kickoff template (Lead) and agent-handoff templates (teammates)
   d. Define task list with dependencies
   e. Select Team Lead agent
2. CREATE TEAM: Use TeamCreate with team configuration
3. SPAWN: Launch teammates as agents with team_name
4. KICKOFF: Team Lead receives kickoff brief and distributes work
5. EXECUTION:
   a. Teammates work on assigned tasks
   b. Communicate via SendMessage for coordination
   c. Track progress via TaskList
   d. Team Lead monitors and reports to HRM
6. VERIFY: Team Lead runs internal verification, then HRM runs cascade
7. SHUTDOWN: Team Lead sends shutdown_request to all teammates
8. CLEANUP: TeamDelete
```

**Cost warning**: ~5x cost per teammate. Only use when:
- Peer communication is genuinely needed during execution
- Workstreams require multiple sustained turns
- File ownership is independent
- Simpler modes (Swarm/Parallel) are insufficient

---

## Squad Delegation Protocol

**When**: Workstream domain maps to a specialized squad (e.g., copywriting -> Squad de Copy).

```
1. DETECT: During registry lookup, identify that workstream domain
   matches a registered squad's domain
2. PREPARE: forge(dispatch_type=squad-chief, granularity=task) → ForgeOutput
   Inject into squad-brief template
   Include: objective, audience, tone, constraints, reference materials, technique_guidance
3. DELEGATE: Send brief to squad chief
4. CHIEF EXECUTES: Squad chief uses internal architecture:
   a. Analyzes brief
   b. Selects internal resources (swipe files, frameworks, etc.)
   c. Produces deliverables using squad's specialized process
   d. Runs internal quality gates
5. REPORT: Chief sends delivery report to HRM
6. VERIFY: HRM runs verification cascade on deliverables
7. INTEGRATE: HRM integrates squad output with other workstream results
```

**Key differences from Swarm/Teams**:
- Squad chief owns the internal process (HRM doesn't micro-manage)
- Squad has its own knowledge base and tools
- HRM only verifies the output, not the process
- Brief format is squad-specific (from registry/squads.yaml)

---

## Mode Selection Flowchart

```
Is there 1 workstream?
  YES -> SINGLE
  NO  -> Are workstreams independent?
           YES -> PARALLEL
           NO  -> Do workstreams need peer communication?
                    NO  -> SWARM
                    YES -> Are there sustained sessions needed?
                             NO  -> SWARM
                             YES -> TEAMS

For any workstream: Does domain match a registered squad?
  YES -> SQUAD DELEGATION (for that workstream)
  NO  -> Use mode selected above
```

**Hybrid mode**: A task can use SWARM for most workstreams and SQUAD for one specific workstream. The HRM coordinates the handoff between swarm results and squad results.
