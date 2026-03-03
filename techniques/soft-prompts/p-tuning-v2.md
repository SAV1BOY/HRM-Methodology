---
id: p-tuning-v2
name: "P-Tuning v2"
aliases: ["P-Tuning-v2", "deep-prompt-tuning", "universal-prompt-tuning"]
category: soft-prompts
family: parameter-efficient-fine-tuning
year: 2022
authors: ["Xiao Liu", "Kaixuan Ji", "Yicheng Fu", "Weng Lam Tam", "Zhengxiao Du", "Zhilin Yang", "Jie Tang"]
paper: "https://arxiv.org/abs/2110.07602"
paper_title: "P-Tuning v2: Prompt Tuning Can Be Comparable to Fine-tuning Universally Across Scales and Tasks"
venue: "ACL 2022"
code: "https://github.com/THUDM/P-tuning-v2"
complexity: medium
token_cost: low
latency: low
num_calls: 1
requires_examples: true
requires_tools: false
requires_training: true
model_agnostic: false
best_for: ["NLU tasks at all model scales", "sequence labeling and token classification", "matching fine-tuning performance with minimal parameters", "bridging gap for medium-sized models"]
avoid_when: ["API-only models", "no training data", "pure text generation tasks where prefix-tuning excels", "need for interpretable prompts"]
composes_with: ["prefix-tuning", "adapter-layers", "multi-task-learning"]
tags: ["soft-prompts", "parameter-efficient", "fine-tuning", "deep-prompts", "NLU", "universal"]
---

# P-Tuning v2

> **One-line summary:** Applies deep continuous prompts across all transformer layers (like prefix-tuning) with task-specific optimizations that enable prompt tuning to rival full fine-tuning universally across model scales (330M to 10B) and NLU task types.

## Overview

P-Tuning v2 addresses a critical limitation of earlier prompt tuning methods: their poor performance on smaller models and on natural language understanding tasks beyond simple classification. While Lester et al.'s prompt tuning works well for large models (10B+) and Li & Liang's prefix-tuning excels at generation, neither consistently matches fine-tuning across the full range of model sizes and NLU tasks. P-Tuning v2 demonstrates that with the right design choices, deep continuous prompts can universally rival fine-tuning.

The method builds on prefix-tuning's approach of adding learnable parameters at every transformer layer, but introduces several key modifications optimized for NLU. These include task-specific prompt lengths (shorter for simple tasks, longer for complex ones), optional reparameterization (the MLP trick from prefix-tuning is helpful for some tasks but not all), multi-task learning across prompt tokens, and a classification head design that reads from prompt token positions rather than a separate CLS token. These seemingly simple changes collectively close the gap between prompt-based methods and full fine-tuning.

The paper's central contribution is empirical: a thorough evaluation across scales (330M to 10B parameters), task types (classification, NLI, QA, sequence labeling, NER), and datasets (SuperGLUE, SQuAD, NER benchmarks) showing that P-Tuning v2 consistently matches fine-tuning performance. This is particularly significant for sequence labeling tasks like Named Entity Recognition, where earlier prompt tuning methods struggled because each token needs a label -- P-Tuning v2 handles this by treating the deep prompts as conditioning context that influences per-token predictions.

## How It Works

1. **Add Deep Continuous Prompts**: For each transformer layer, create a set of P trainable continuous vectors that serve as prefix tokens in the key-value attention computation.

2. **Configure Prompt Length Per Task**: Use shorter prompts (10-20 tokens) for simple classification tasks and longer prompts (100-200 tokens) for complex tasks like QA and sequence labeling.

3. **Choose Reparameterization**: Optionally use an MLP reparameterization network (as in prefix-tuning). This helps for some tasks but is not universally needed -- skip it when it does not improve validation performance.

4. **Add Classification/Prediction Head**: For token-level tasks (NER, SQuAD), add a lightweight linear head on top of the token representations. For classification, read from the prompt token positions or a verbalizer.

5. **Train**: Optimize only the continuous prompt parameters and the task-specific prediction head. The full transformer model remains frozen.

6. **Multi-task Pre-training (optional)**: Pre-train shared continuous prompts on related tasks before fine-tuning task-specific prompts. This improves few-shot performance.

7. **Evaluate**: Run the frozen model with the trained deep prompts on the evaluation set.

### Diagram

```
P-Tuning v2 Architecture:

Layer L:  [p1_L ... pP_L] | [h1_L ... hN_L]  -->  Task Head  -->  Prediction
               ^                  ^
Layer 3:  [p1_3 ... pP_3] | [h1_3 ... hN_3]  -->  Attention
               ^                  ^
Layer 2:  [p1_2 ... pP_2] | [h1_2 ... hN_2]  -->  Attention
               ^                  ^
Layer 1:  [p1_1 ... pP_1] | [h1_1 ... hN_1]  -->  Attention
               ^                  ^
          Trainable deep     Frozen input
          prompt tokens       representations

Comparison with other methods:
+------------------+------------+---------+-------+-------+
|                  | Input Only | Layer 1 | All   | NLU   |
|                  |            | Only    | Layers| Focus |
+------------------+------------+---------+-------+-------+
| Prompt Tuning    |     x      |         |       |       |
| Prefix-Tuning    |            |         |   x   |       |
| P-Tuning v2      |            |         |   x   |   x   |
+------------------+------------+---------+-------+-------+
```

## Template

```python
# Pseudo-code for P-Tuning v2
import torch
import torch.nn as nn

class PTuningV2(nn.Module):
    def __init__(self, frozen_lm, num_prompt_tokens={prompt_length},
                 num_layers={num_layers}, hidden_dim={hidden_dim},
                 num_labels={num_labels}, use_reparameterization={True_or_False}):
        super().__init__()
        self.frozen_lm = frozen_lm
        for param in self.frozen_lm.parameters():
            param.requires_grad = False

        # Deep prompt parameters for each layer
        self.deep_prompts = nn.ParameterList([
            nn.Parameter(torch.randn(num_prompt_tokens, hidden_dim) * 0.01)
            for _ in range(num_layers)
        ])

        # Optional reparameterization
        if use_reparameterization:
            self.reparam = nn.Sequential(
                nn.Linear(hidden_dim, hidden_dim),
                nn.Tanh(),
                nn.Linear(hidden_dim, hidden_dim)
            )
        else:
            self.reparam = None

        # Task-specific classification head
        self.classifier = nn.Linear(hidden_dim, num_labels)

    def forward(self, input_ids, attention_mask, labels=None):
        # Get deep prompts for each layer
        past_key_values = []
        for layer_prompt in self.deep_prompts:
            prompt = self.reparam(layer_prompt) if self.reparam else layer_prompt
            # Shape for key-value pairs in attention
            past_key_values.append(prompt)

        outputs = self.frozen_lm(
            input_ids=input_ids,
            attention_mask=attention_mask,
            past_key_values=past_key_values
        )

        # Classification from prompt or token positions
        logits = self.classifier(outputs.last_hidden_state)
        loss = nn.CrossEntropyLoss()(logits.view(-1, {num_labels}), labels.view(-1))
        return loss, logits

# Usage
model = PTuningV2(frozen_lm=bert_large, num_prompt_tokens={prompt_length},
                  num_labels={num_labels})
optimizer = torch.optim.AdamW(
    [p for p in model.parameters() if p.requires_grad], lr={learning_rate}
)
```

## Examples

### Example 1: Named Entity Recognition (CoNLL-2003)

**Task**: Token-level NER on the CoNLL-2003 benchmark, a task where input-only prompt tuning fails badly.

**Setup**:
- Model: RoBERTa-Large (355M parameters, frozen)
- Deep prompt length: 20 tokens per layer (24 layers)
- Trainable parameters: ~1.5M (0.4% of model)
- No reparameterization (not needed for this task)
- Linear CRF head on top of token representations

**Results**:
| Method             | F1 Score | Params Trained |
|--------------------|----------|----------------|
| Full Fine-Tuning   | 92.4     | 355M (100%)    |
| P-Tuning v2        | 92.1     | 1.5M (0.4%)   |
| Prefix-Tuning      | 88.6     | 1.2M (0.3%)   |
| Prompt Tuning      | 73.2     | 30K (0.008%)  |

P-Tuning v2 nearly matches fine-tuning on this token-level task, while input-only prompt tuning collapses to 73.2% -- a 19-point gap.

### Example 2: SuperGLUE with Medium-Sized Models

**Task**: Demonstrate universal performance across the SuperGLUE benchmark with a 330M parameter model.

**Setup**:
- Model: DeBERTa-Base (330M parameters, frozen)
- Prompt length: varies by task (10 for BoolQ, 40 for ReCoRD, 20 for others)
- Reparameterization: used for complex tasks only

**Results on SuperGLUE**:
| Task    | Fine-Tune | P-Tuning v2 | Gap   |
|---------|-----------|-------------|-------|
| BoolQ   | 84.7      | 84.0        | -0.7  |
| CB      | 93.6      | 92.1        | -1.5  |
| COPA    | 73.0      | 71.5        | -1.5  |
| MultiRC | 84.5      | 83.8        | -0.7  |
| ReCoRD  | 89.2      | 88.5        | -0.7  |
| RTE     | 86.6      | 85.3        | -1.3  |
| WiC     | 72.4      | 71.8        | -0.6  |
| WSC     | 89.4      | 88.0        | -1.4  |

Average gap is only 1.05 points -- at a 330M model scale where prompt tuning typically fails.

## When to Use

- You need prompt-based adaptation that works at all model scales (not just 10B+)
- Your tasks include token-level predictions (NER, POS tagging, span extraction)
- You want a single method that works for both classification and sequence labeling
- You need to match fine-tuning performance with minimal parameters
- You are building multi-task systems with shared frozen backbones

## When to Avoid

- You are using API-only models without access to internal layers
- The task is primarily text generation (use prefix-tuning instead)
- No training data is available (use discrete prompting)
- You need interpretable, auditable prompt representations
- Training infrastructure is unavailable (requires GPU training pipeline)

## Cost & Performance

| Dimension            | Value                          | Notes                                         |
|-----------------------|--------------------------------|-----------------------------------------------|
| Trainable params     | 0.1-1% of model                | Larger than prompt tuning, similar to prefix   |
| Training time        | 2-8 hours (single GPU)         | Comparable to prefix-tuning                   |
| Inference overhead   | Minimal                        | Extended KV cache by P tokens per layer       |
| Performance (NLU)    | 97-100% of fine-tuning         | Universal across scales and tasks             |
| Performance (NER)    | 98-100% of fine-tuning         | Key differentiator vs. prompt tuning          |
| Min model size       | ~330M (works at this scale)    | Unlike prompt tuning which needs 10B+         |

## Variants

- **P-Tuning v2 Standard**: Deep prompts at all layers, no reparameterization. Default choice.
- **P-Tuning v2 + Reparam**: Add MLP reparameterization for tasks that benefit from it (typically complex multi-sentence tasks).
- **P-Tuning v2 + Multi-task**: Pre-train shared prompts on multiple related tasks, then specialize per-task prompts.
- **Hybrid**: Combine P-Tuning v2 with a small number of unfrozen model layers (e.g., last 2 layers) for marginal gains.

## Composability

- **With Adapters**: Combine deep prompts with adapter layers inserted into the transformer for complementary adaptation.
- **Multi-task Learning**: Share deep prompt parameters across related tasks while maintaining task-specific classification heads.
- **With LoRA**: Use P-Tuning v2 for task framing and LoRA for fine-grained weight adaptation.
- **Few-shot Enhancement**: Pre-train deep prompts on related tasks, then adapt with very few examples on the target task.

## Limitations

- Requires access to internal transformer layers (incompatible with API-only models like GPT-4, Claude)
- Adds complexity compared to input-only prompt tuning (must manage per-layer parameters)
- Deep prompts are not human-interpretable, making debugging challenging
- Task-specific hyperparameter tuning is needed (prompt length, reparameterization, learning rate)
- Slightly less effective than prefix-tuning for pure text generation tasks
- Increases effective sequence length, reducing available context window
- Requires a proper training pipeline with GPU infrastructure

## Sources

- Liu, X. et al. (2022). "P-Tuning v2: Prompt Tuning Can Be Comparable to Fine-tuning Universally Across Scales and Tasks." *ACL 2022*. *arXiv:2110.07602*. https://arxiv.org/abs/2110.07602
- Li, X.L. & Liang, P. (2021). "Prefix-Tuning: Optimizing Continuous Prompts for Generation." *ACL 2021*. *arXiv:2101.00190*.
- Lester, B. et al. (2021). "The Power of Scale for Parameter-Efficient Prompt Tuning." *EMNLP 2021*.
- P-Tuning v2 GitHub: https://github.com/THUDM/P-tuning-v2
