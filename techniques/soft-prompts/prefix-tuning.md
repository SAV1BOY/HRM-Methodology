---
id: prefix-tuning
name: "Prefix-Tuning"
aliases: ["prefix-tuning", "continuous-prefix-optimization", "layer-wise-soft-prompts"]
category: soft-prompts
family: parameter-efficient-fine-tuning
year: 2021
authors: ["Xiang Lisa Li", "Percy Liang"]
paper: "https://arxiv.org/abs/2101.00190"
paper_title: "Prefix-Tuning: Optimizing Continuous Prompts for Generation"
venue: "ACL 2021"
code: "https://github.com/XiangLi1999/PrefixTuning"
complexity: medium
token_cost: low
latency: low
num_calls: 1
requires_examples: true
requires_tools: false
requires_training: true
model_agnostic: false
best_for: ["text generation tasks", "table-to-text generation", "summarization", "multi-task generation with shared backbone", "parameter-efficient NLG"]
avoid_when: ["API-only models", "no training data", "NLU tasks where P-Tuning v2 may be better", "very small models"]
composes_with: ["prompt-tuning", "adapter-layers", "multi-task-learning"]
tags: ["soft-prompts", "parameter-efficient", "fine-tuning", "prefix", "generation", "layer-wise"]
---

# Prefix-Tuning

> **One-line summary:** Trains continuous prefix vectors that are prepended to the key-value pairs at every transformer layer, providing deeper task-specific conditioning than input-only prompt tuning while keeping the language model frozen.

## Overview

Prefix-Tuning, introduced by Li and Liang at Stanford, extends the idea of soft prompts from the input embedding layer to every layer of the transformer. Instead of only prepending learnable vectors at the input, prefix-tuning prepends trainable "prefix" activations to the key and value matrices at each attention layer. This allows the learned prefix to directly influence the attention patterns at every depth of the model, providing substantially richer task-specific conditioning than methods that only modify the input layer.

The method was originally designed for natural language generation tasks, particularly table-to-text generation and abstractive summarization. The key insight is that generation tasks benefit from deeper conditioning because the model's behavior at later layers has a more direct influence on output token selection. By injecting learned activations at every layer, prefix-tuning can steer the generation process more precisely than input-only approaches.

To stabilize training, Li and Liang introduce a reparameterization trick: instead of directly optimizing the prefix activations (which are high-dimensional and can be unstable), they parameterize them through a smaller feedforward network (MLP). During training, the MLP maps a smaller set of parameters to the full prefix activations. After training, the MLP is discarded and only the computed prefix activations are kept for inference, adding zero computational overhead beyond the extended key-value sequence length. This approach trains approximately 0.1% of model parameters while achieving performance comparable to full fine-tuning on generation benchmarks.

## How It Works

1. **Define Prefix Length**: Choose the number of prefix tokens P (typically 10-200). Each prefix token will have learned key-value pairs at every transformer layer.

2. **Initialize Reparameterization Network**: Create a small MLP that maps trainable prefix embeddings to the full set of key-value activations across all layers. This stabilizes optimization.

3. **Compute Prefix Activations**: For each layer l, the MLP produces prefix key vectors K_prefix^l and prefix value vectors V_prefix^l of shape [P, d_model].

4. **Prepend to Attention**: At each transformer layer, prepend the prefix key-value pairs to the regular key-value pairs:
   - K^l = concat(K_prefix^l, K_input^l)
   - V^l = concat(V_prefix^l, V_input^l)
   - Query vectors attend over both prefix and input key-value pairs.

5. **Forward Pass**: The frozen transformer processes the combined prefix + input activations. Attention heads can attend to prefix positions, allowing the prefix to influence every layer's computation.

6. **Compute Loss and Backpropagate**: Compute task loss and backpropagate gradients through the prefix activations and the reparameterization MLP. Frozen model parameters receive no gradient updates.

7. **Discard MLP at Inference**: After training, compute the final prefix activations and store them directly. The MLP is no longer needed, so inference has no extra overhead.

### Diagram

```
Layer L:  [P_kL][P_vL] ++ [K_L][V_L]  -->  Attention  -->  Output
                  ^                ^
Layer 3:  [P_k3][P_v3] ++ [K_3][V_3]  -->  Attention  -->  ...
                  ^                ^
Layer 2:  [P_k2][P_v2] ++ [K_2][V_2]  -->  Attention  -->  ...
                  ^                ^
Layer 1:  [P_k1][P_v1] ++ [K_1][V_1]  -->  Attention  -->  ...
                  ^                ^
              Trainable         Frozen
              Prefix            LM Keys/Values
              
Reparameterization (training only):
+-------------------+     +------------------+
| Prefix Embeddings |---->| MLP              |----> P_k^l, P_v^l
| (small params)    |     | (reparameterize) |      for all layers
+-------------------+     +------------------+
```

## Template

```python
# Pseudo-code for Prefix-Tuning
import torch
import torch.nn as nn

class PrefixTuning(nn.Module):
    def __init__(self, frozen_lm, num_prefix_tokens={prefix_length},
                 num_layers={num_layers}, hidden_dim={hidden_dim},
                 prefix_hidden_dim={prefix_hidden_dim}):
        super().__init__()
        self.frozen_lm = frozen_lm
        self.num_prefix_tokens = num_prefix_tokens
        self.num_layers = num_layers

        # Freeze all LM parameters
        for param in self.frozen_lm.parameters():
            param.requires_grad = False

        # Reparameterization: small embeddings -> MLP -> full prefix
        self.prefix_embeddings = nn.Embedding(num_prefix_tokens, prefix_hidden_dim)
        self.prefix_mlp = nn.Sequential(
            nn.Linear(prefix_hidden_dim, prefix_hidden_dim),
            nn.Tanh(),
            nn.Linear(prefix_hidden_dim, num_layers * 2 * hidden_dim)
            # 2 for key and value at each layer
        )

    def get_prefix(self, batch_size):
        prefix_ids = torch.arange(self.num_prefix_tokens)
        prefix_embeds = self.prefix_embeddings(prefix_ids)
        past_key_values = self.prefix_mlp(prefix_embeds)
        # Reshape to (num_layers, 2, num_prefix, num_heads, head_dim)
        # and expand for batch
        return past_key_values.expand(batch_size, -1, -1)

    def forward(self, input_ids, **kwargs):
        batch_size = input_ids.shape[0]
        past_key_values = self.get_prefix(batch_size)
        return self.frozen_lm(
            input_ids=input_ids,
            past_key_values=past_key_values,
            **kwargs
        )

# Training
model = PrefixTuning(frozen_lm=gpt2_large, num_prefix_tokens={prefix_length})
optimizer = torch.optim.Adam(
    [p for p in model.parameters() if p.requires_grad],
    lr={learning_rate}
)
```

## Examples

### Example 1: Table-to-Text Generation (E2E NLG)

**Task**: Generate natural language descriptions from structured table data.

**Setup**:
- Model: GPT-2 Medium (345M parameters, frozen)
- Prefix length: 10 tokens per layer
- Trainable parameters: ~250K (0.07% of model)
- Dataset: E2E NLG Challenge (50K training examples)

**Input Table**:
```
name: The Eagle | eatType: coffee shop | food: French |
priceRange: moderate | customerRating: 3/5 | area: riverside
```

**Generated Output (Prefix-Tuning)**:
"The Eagle is a moderately priced coffee shop located in the riverside area. It serves French food and has a customer rating of 3 out of 5."

**Comparison**:
| Method           | BLEU  | NIST  | Params Trained |
|------------------|-------|-------|----------------|
| Full Fine-Tune   | 68.2  | 8.62  | 345M (100%)    |
| Prefix-Tuning    | 69.7  | 8.73  | 250K (0.07%)   |
| Prompt Tuning    | 64.1  | 8.21  | 40K (0.01%)    |

Prefix-tuning actually slightly outperforms full fine-tuning on this benchmark, likely due to regularization from frozen parameters.

### Example 2: Summarization (XSUM)

**Task**: Abstractive summarization of news articles.

**Setup**:
- Model: BART-Large (400M parameters, frozen)
- Prefix length: 200 tokens per layer
- Trainable parameters: ~2M (0.5% of model)
- Dataset: XSUM (200K training examples)

**Input**: A 300-word BBC news article about a new climate policy.

**Generated Summary (Prefix-Tuning)**:
"The UK government has announced a new climate policy requiring all new buildings to meet net-zero carbon standards by 2030, with industry leaders expressing cautious optimism about the targets."

**Results**:
| Method           | ROUGE-1 | ROUGE-2 | ROUGE-L | Params Trained |
|------------------|---------|---------|---------|----------------|
| Full Fine-Tune   | 45.14   | 22.27   | 37.25   | 400M (100%)    |
| Prefix-Tuning    | 43.80   | 20.93   | 36.05   | 2M (0.5%)      |
| Input-only Prompt | 40.12  | 18.45   | 33.21   | 800K (0.2%)    |

Layer-wise prefix conditioning provides a meaningful improvement over input-only approaches for generation.

## When to Use

- You are working on text generation tasks (summarization, translation, data-to-text)
- You need richer conditioning than input-only prompt tuning provides
- You have access to model internals and can modify the attention mechanism
- You want to serve multiple generation tasks from one frozen model
- You have moderate training data (thousands of examples)

## When to Avoid

- Using API-only models without access to internal activations
- Working on primarily NLU/classification tasks (P-Tuning v2 may be more appropriate)
- No training data or compute is available
- You need interpretable prompts for debugging or auditing
- The model is very small (performance gains diminish below 300M parameters)

## Cost & Performance

| Dimension            | Value                          | Notes                                         |
|-----------------------|--------------------------------|-----------------------------------------------|
| Trainable params     | 0.05-0.5% of model             | Depends on prefix length and model size       |
| Training time        | 2-12 hours (single GPU)        | Faster than fine-tuning, slower than prompt tuning |
| Inference overhead   | Minimal                        | Extended KV cache by P tokens per layer       |
| Storage per task     | 100KB-5MB                      | Much smaller than full model copies           |
| Performance (gen)    | 95-101% of fine-tuning         | Can match or exceed FT on some gen benchmarks |
| Performance (NLU)    | 85-95% of fine-tuning          | Weaker than P-Tuning v2 for understanding     |

## Variants

- **Prefix-Tuning (original)**: Prefix at every layer with MLP reparameterization. Best for generation.
- **Without Reparameterization**: Directly optimize prefix activations. Can work but training is less stable.
- **Shallow Prefix**: Prefix only at the first few layers. Reduces parameters but may lose expressiveness.
- **Deep Prefix + Adapter**: Combine prefix-tuning with adapter layers for even richer adaptation.

## Composability

- **With Prompt Tuning**: Use prefix-tuning for deep conditioning and input-level prompt tuning for task framing.
- **With LoRA**: Combine prefix-tuning with low-rank adaptation for complementary adaptation strategies.
- **Multi-task**: Share the frozen model and maintain separate prefix parameters per task.
- **Ensemble**: Average outputs from multiple prefix-tuned variants for robustness.

## Limitations

- Requires access to internal model activations (not compatible with API-only services)
- The MLP reparameterization adds complexity to the training pipeline
- Longer prefix lengths increase the effective sequence length, reducing available context window
- Performance on NLU tasks lags behind methods designed for understanding (like P-Tuning v2)
- Prefix activations are not interpretable -- no way to understand what the prefix "means"
- Hyperparameter sensitivity: prefix length, MLP architecture, and learning rate all matter significantly
- Does not work well for very small models where the attention mechanism has limited capacity

## Sources

- Li, X.L. & Liang, P. (2021). "Prefix-Tuning: Optimizing Continuous Prompts for Generation." *ACL 2021*. *arXiv:2101.00190*. https://arxiv.org/abs/2101.00190
- Lester, B. et al. (2021). "The Power of Scale for Parameter-Efficient Prompt Tuning." *EMNLP 2021*. *arXiv:2104.08691*.
- Liu, X. et al. (2022). "P-Tuning v2: Prompt Tuning Can Be Comparable to Fine-tuning Universally Across Scales and Tasks." *arXiv:2110.07602*.
- PrefixTuning GitHub: https://github.com/XiangLi1999/PrefixTuning
