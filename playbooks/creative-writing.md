# Playbook: Creative Writing

> **Pipeline:** Role Prompting → Skeleton of Thought → Multi-Agent Debate → Self-Refine
>
> **Best for:** Fiction, marketing copy, blog posts, speeches, screenwriting, poetry, narrative design, brand storytelling.

## Workflow Diagram

```
                    ┌─────────────────────┐
                    │   Creative Brief    │
                    └─────────┬───────────┘
                              │
                    ┌─────────▼───────────┐
                    │  1. Role Prompting   │  Adopt a specific creative
                    │                     │  persona and voice
                    └─────────┬───────────┘
                              │
                    ┌─────────▼───────────┐
                    │  2. Skeleton of      │  Generate parallel outline
                    │     Thought (SoT)   │  then expand each section
                    └─────────┬───────────┘
                              │
                    ┌─────────▼───────────┐
                    │  3. Multi-Agent      │  Debate between editor,
                    │     Debate          │  critic, and audience proxy
                    └─────────┬───────────┘
                              │
                    ┌─────────▼───────────┐
                    │  4. Self-Refine      │  Polish language, pacing,
                    │                     │  and emotional resonance
                    └─────────┴───────────┘
```

## Technique Selection Rationale

| Step | Technique | Why This Technique |
|------|-----------|-------------------|
| 1 | Role Prompting | Creative writing demands a consistent voice, style, and perspective — assigning a persona grounds the model in a specific authorial identity |
| 2 | Skeleton of Thought | Long-form creative content benefits from outlining first, then expanding each section in parallel — prevents drift and ensures structural coherence |
| 3 | Multi-Agent Debate | Creative quality is subjective; having multiple simulated perspectives (editor, critic, audience) surfaces blind spots and improves balance |
| 4 | Self-Refine | Creative text always benefits from iterative polish — tightening prose, improving rhythm, strengthening imagery, removing cliches |

## Step-by-Step Templates

### Step 1: Role Prompting

**Purpose:** Establish the creative voice, expertise, and stylistic identity for the entire piece.

```
You are {persona_description}. You have {years} years of experience in
{creative_domain}. Your writing style is characterized by:
- {style_trait_1}
- {style_trait_2}
- {style_trait_3}

Your influences include {influence_1}, {influence_2}, and {influence_3}.

You have been commissioned to write the following:

BRIEF:
{creative_brief}

TARGET AUDIENCE: {audience}
TONE: {tone}
LENGTH: {target_length}

Before writing, reflect on:
1. What emotional journey should the reader experience?
2. What makes this topic uniquely interesting from your perspective?
3. What literary devices or techniques will you employ?

Share your creative approach, then begin drafting.
```

### Step 2: Skeleton of Thought

**Purpose:** Generate a structural outline first, then expand each section with full creative detail.

```
Based on your creative approach above, generate a skeleton outline for this piece.

CREATIVE APPROACH:
{role_output}

Phase 1 — Create the skeleton:
List each major section/chapter/scene as a single-line summary:
1. [Section title]: [One-sentence description of content and purpose]
2. [Section title]: [One-sentence description of content and purpose]
...
N. [Section title]: [One-sentence description of content and purpose]

Phase 2 — Expand each section:
For each skeleton point, write the full creative content. Ensure:
- Smooth transitions between sections
- Consistent voice from the persona established in Step 1
- Each section serves the overall emotional arc
- Sensory details and concrete imagery in every section

Expand now, section by section:
```

### Step 3: Multi-Agent Debate

**Purpose:** Have multiple critical perspectives evaluate and improve the draft.

```
The following creative piece needs evaluation from multiple perspectives.
Conduct a structured debate between three agents.

DRAFT:
{skeleton_output}

AGENT 1 — THE EDITOR (craft focus):
Evaluate: sentence-level quality, word choice, rhythm, pacing, structure.
Does the prose sing? Where does it drag? What cliches need replacing?
Provide specific line-level suggestions.

AGENT 2 — THE CRITIC (artistic merit):
Evaluate: originality, thematic depth, emotional authenticity, surprise.
Is this piece saying something new? Does it earn its emotional moments?
Where does it feel derivative or shallow?

AGENT 3 — THE AUDIENCE PROXY (reader experience):
Evaluate: engagement, clarity, accessibility, memorability.
Would the target audience ({audience}) keep reading? What confuses them?
What would they quote or share? Where do they lose interest?

DEBATE FORMAT:
Round 1: Each agent provides their assessment (strengths + weaknesses).
Round 2: Agents respond to each other's critiques — agree, disagree, or build on.
Round 3: Consensus — what are the top 5 improvements that all agents agree on?

Deliver the final consensus list of improvements.
```

### Step 4: Self-Refine

**Purpose:** Apply the debate feedback to polish the piece through iterative refinement.

```
You are the original author ({persona_description}). Apply the following
editorial feedback to revise your draft.

ORIGINAL DRAFT:
{skeleton_output}

EDITORIAL FEEDBACK:
{debate_consensus}

Revision pass 1 — Structural changes:
- Address any pacing or structural issues
- Strengthen weak transitions
- Cut sections that don't serve the whole

Revision pass 2 — Sentence-level polish:
- Replace cliches with fresh imagery
- Vary sentence length for rhythm
- Strengthen verbs — cut adverbs where possible
- Ensure each paragraph earns its place

Revision pass 3 — Emotional resonance:
- Does the opening hook the reader in 3 sentences?
- Does each section advance the emotional arc?
- Does the ending feel earned and resonant?

Produce the fully revised piece, noting in [brackets] any significant
changes you made and why.
```

## Walk-Through Example

**Task:** "Write a blog post about the death of the open internet, aimed at developers, in the style of a thoughtful tech essayist like Paul Graham or Robin Sloan."

---

### Step 1 Output: Role Prompting

> **Persona established:** I am a technology essayist who spent a decade as a software engineer before turning to writing full-time. My style blends technical precision with literary warmth — I use code metaphors alongside references to literature and history. I never lecture; I think alongside the reader.
>
> **Creative approach:**
> - The emotional journey: nostalgia then recognition then subtle anger then qualified hope
> - The hook: a personal anecdote about discovering the web as a teenager
> - Literary devices: extended metaphor of the web as a public park being enclosed, concrete code examples contrasted with corporate press releases, direct address to "you" the developer

### Step 2 Output: Skeleton of Thought

> **Skeleton:**
> 1. **The First URL** — Personal anecdote: the moment of discovery, typing a URL and reaching someone's personal page across the world
> 2. **What We Built** — The architecture of the open web: HTTP, HTML, RSS, hyperlinks as democratic infrastructure
> 3. **The Enclosure** — How platforms replaced protocols: Facebook's walled garden, API shutdowns, the app-ification of everything
> 4. **The Developer's Complicity** — We chose convenience (npm, GitHub, AWS) over independence — how we built the road ourselves
> 5. **What Remains** — The IndieWeb, ActivityPub, personal blogs, Gemini — small fires still burning
> 6. **A Closing Commit** — What each developer can do: host one thing, write one thing, link to one thing
>
> [Expanded content for each section follows...]

### Step 3 Output: Multi-Agent Debate

> **Editor:** The prose is strong in sections 1 and 3 but gets preachy in section 4. The transition from section 2 to 3 needs a hinge sentence. Consider cutting section 2 by half since developers already know HTTP basics.
>
> **Critic:** Section 5 reads like a listicle of alternative technologies. It needs to earn its hope — show a specific person or project, not just a catalogue. The "enclosure" metaphor is historically rich — lean harder into it.
>
> **Audience Proxy:** Developers will skim section 2 (they know HTTP). Cut it in half and front-load the surprise — what about HTTP did they forget? Section 6 is too short and feels like a call-to-action on a donation page.
>
> **Consensus improvements:**
> 1. Cut section 2 by 50%, focus on one surprising forgotten detail about early web architecture
> 2. Replace generic metaphor in section 4 with something specific and original
> 3. Section 5: profile one real person/project instead of listing five
> 4. Expand section 6 with a concrete technical action, not just exhortation
> 5. Add a hinge sentence between sections 2 and 3 that connects the architecture to its vulnerability

### Step 4 Output: Self-Refine

> **Structural changes:** Merged sections 5 and 6; profiled a specific developer running her own Mastodon instance from a Raspberry Pi in her closet — then pivoted to what the reader can do.
>
> **Sentence-level polish:** Replaced the flat metaphor in section 4 with "We npm-installed our way into a company town." Tightened section 2 to a single powerful paragraph about the `<a href>` tag as the most democratic technology ever invented.
>
> **Emotional resonance:** Rewrote the ending to circle back to the opening anecdote — the same teenager, now an adult, typing `ssh` into a terminal to deploy a personal site.
>
> [Full revised essay follows]

## Decision Points

```
                          ┌──────────────┐
                          │ Creative task │
                          └──────┬───────┘
                                 │
                    ┌────────────▼────────────┐
                    │ Is a specific voice/     │
                    │ persona needed?          │
                    └────┬──────────────┬──────┘
                     Yes │              │ No
                         ▼              ▼
                   Role Prompting    Skip to SoT
                         │
                    ┌────▼───────────────────┐
                    │ Is the piece long-form  │
                    │ (>500 words)?           │
                    └────┬──────────────┬─────┘
                     Yes │              │ No
                         ▼              ▼
                  Skeleton of       Direct generation
                  Thought           (single pass)
                         │
                    ┌────▼───────────────────┐
                    │ Is quality critical     │
                    │ (published/client)?     │
                    └────┬──────────────┬─────┘
                     Yes │              │ No
                         ▼              ▼
                  Multi-Agent       Self-Refine only
                  Debate + Refine   (skip debate)
```

## Customization Options

| Variation | Modification |
|-----------|-------------|
| **Speed priority** | Skip Multi-Agent Debate; use single Self-Refine pass |
| **Maximum quality** | Add Self-Consistency at step 2 (generate 3 outlines, pick best); add 2 extra debate rounds |
| **Specific style** | Add Few-Shot examples of target style before Role Prompting |
| **Poetry/verse** | Replace SoT with CoT (sequential composition matters more); add prosody critique to debate |
| **Collaborative** | Replace Multi-Agent Debate with actual human feedback loop at step 3 |
| **Brand voice** | Add Context Stuffing with brand guidelines before Role Prompting |
| **Marketing copy** | Add Emotion Prompting to step 1; add A/B variant generation after step 4 |

## Cost Estimate

| Step | API Calls | Token Overhead | Latency |
|------|-----------|---------------|---------|
| Role Prompting | 1 | ~400 output | Low |
| Skeleton of Thought | 1+N sections | ~2000 output | Medium |
| Multi-Agent Debate | 3 (1 per agent round) | ~3000 output | High |
| Self-Refine | 2-3 | ~2500 output | Medium |
| **Total** | **8-12** | **~7900 tokens** | **~40-90s** |
