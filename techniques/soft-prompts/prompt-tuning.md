---
id: prompt-tuning
name: "Prompt Tuning"
aliases: ["soft-prompt-tuning", "continuous-prompt-tuning", "learned-prompts"]
category: soft-prompts
family: parameter-efficient-fine-tuning
year: 2021
authors: ["Brian Lester", "Rami Al-Rfou", "Noah Constant"]
paper: "https://arxiv.org/abs/2104.08691"
paper_title: "The Power of Scale for Parameter-Efficient Prompt Tuning"
venue: "EMNLP 2021"
code: null
complexity: medium
token_cost: low
latency: low
num_calls: 1
requires_examples: true
requires_tools: false
requires_training: true
model_agnostic: false
best_for: ["task-specific adaptation with frozen models", "multi-tenant model serving", "parameter-efficient fine-tuning", "classification and generation tasks"]
avoid_when: ["using API-only models", "no training data available", "need for human-readable prompts", "very small models under 1B parameters"]
composes_with: ["ensemble-methods", "multi-task-learning", "model-distillation"]
tags: ["soft-prompts", "parameter-efficient", "fine-tuning", "continuous-prompts", "prefix-tokens"]
---

# Prompt Tuning

> **One-line summary:** Trains a small set of continuous "soft prompt" token embeddings prepended to the input while keeping the entire language model frozen, achieving competitive performance with full fine-tuning at a fraction of the parameter cost.

## Overview

Prompt Tuning, introduced by Lester et al. at Google, is a parameter-efficient fine-tuning method that learns a small number of continuous embedding vectors (soft prompt tokens) that are prepended to the input at the embedding layer. Unlike discrete prompting where you write text instructions, prompt tuning optimizes real-valued vectors in the model's embedding space through backpropagation on a task-specific training set. The frozen language model processes these learned embeddings just as it would process any other token embeddings, but because they exist in continuous space rather than being constrained to the model's vocabulary, they can encode task-specific information more efficiently.

The critical finding of the paper is that prompt tuning's effectiveness scales dramatically with model size. For models under 1 billion parameters, prompt tuning significantly underperforms full fine-tuning. However, as models scale to 10 billion parameters and beyond (specifically T5-XXL at 11B), prompt tuning essentially closes the gap with full model fine-tuning while training fewer than 0.01% of the parameters. This scaling behavior suggests that larger models are better at interpreting and leveraging the information encoded in soft prompts.

Prompt tuning offers a compelling paradigm for multi-tenant model serving. Since only the soft prompt parameters differ between tasks, a single frozen model can serve many tasks simultaneously by swapping out small prompt vectors (typically 20-100 tokens, amounting to a few kilobytes of parameters). This is dramatically more efficient than maintaining separate fine-tuned model copies for each task, making it ideal for production environments serving many specialized tasks.

## How It Works

1. **Initialize Soft Tokens**: Create a set of N learnable embedding vectors (typically 20-100 tokens). These can be initialized randomly, from sampled vocabulary embeddings, or from the embeddings of a relevant text string.

2. **Prepend to Input**: At inference time, concatenate the soft prompt embeddings with the input token embeddings before feeding them into the first transformer layer.

3. **Forward Pass**: The frozen language model processes the combined (soft prompt + input) embedding sequence normally through all transformer layers.

4. **Compute Loss**: Compare the model output against the ground truth labels using the task-specific loss function (cross-entropy for classification, language modeling loss for generation).

5. **Backpropagate**: Compute gradients with respect to only the soft prompt embeddings. All model parameters remain frozen -- gradients do not flow into the model weights.

6. **Update Soft Prompts**: Apply the optimizer step (e.g., Adam) to update only the soft prompt embeddings.

7. **Repeat**: Continue training for multiple epochs until convergence on the validation set.

### Diagram

```
                  Trainable              Frozen LM
              +---------------+    +--------------------+
              | Soft Prompt   |    | Transformer Layers |
              | Embeddings    |    |                    |
              | [s1][s2]...[sN]    |  [Layer 1]         |
              +-------+-------+    |  [Layer 2]         |
                      |            |  [  ...  ]         |
                      v            |  [Layer L]         |
Input: "Review text"               |                    |
       |                           |                    |
       v                           |                    |
[Tokenize + Embed]                 |                    |
       |                           |                    |
       v                           |                    |
[s1][s2]...[sN][tok1][tok2]...--->|  Forward Pass  |--->  Output
                                   |                    |
              ^                    +--------------------+
              |
         [Backprop only                    
          updates s1...sN]                
```

## Template

```python
# Pseudo-code for Prompt Tuning
import torch
import torch.nn as nn

class PromptTuning(nn.Module):
    def __init__(self, frozen_lm, num_soft_tokens={num_tokens},
                 embedding_dim={embedding_dim}, init_from_text="{init_text}"):
        super().__init__()
        self.frozen_lm = frozen_lm
        for param in self.frozen_lm.parameters():
            param.requires_grad = False  # Freeze all LM params

        # Initialize soft prompt embeddings
        if init_from_text:
            tokens = tokenizer.encode(init_from_text)[:num_soft_tokens]
            init_embeds = frozen_lm.get_input_embeddings()(torch.tensor(tokens))
            self.soft_prompt = nn.Parameter(init_embeds.clone())
        else:
            self.soft_prompt = nn.Parameter(
                torch.randn(num_soft_tokens, embedding_dim) * 0.01
            )

    def forward(self, input_ids, **kwargs):
        input_embeds = self.frozen_lm.get_input_embeddings()(input_ids)
        # Prepend soft prompt to input embeddings
        batch_size = input_embeds.shape[0]
        soft_prompt_expanded = self.soft_prompt.unsqueeze(0).expand(batch_size, -1, -1)
        combined = torch.cat([soft_prompt_expanded, input_embeds], dim=1)
        return self.frozen_lm(inputs_embeds=combined, **kwargs)

# Training loop
model = PromptTuning(frozen_lm=base_model, num_soft_tokens={num_tokens})
optimizer = torch.optim.Adam([model.soft_prompt], lr={learning_rate})

for batch in {train_dataloader}:
    outputs = model(batch["input_ids"], labels=batch["labels"])
    loss = outputs.loss
    loss.backward()  # Only soft_prompt receives gradients
    optimizer.step()
    optimizer.zero_grad()
```

## Examples

### Example 1: Sentiment Classification with T5-XXL

**Task**: Adapt T5-XXL (11B params) for binary sentiment classification using only 50 soft tokens.

**Setup**:
- Model: T5-XXL (11B parameters, frozen)
- Soft prompt: 50 tokens x 4096 dimensions = 204,800 parameters (0.002% of model)
- Training data: SST-2 training set (67K examples)
- Initialization: From embeddings of "Classify the sentiment of this text as positive or negative:"

**Training**:
```
Epoch 1: Loss 0.68 -> 0.31, Val Acc: 91.2%
Epoch 3: Loss 0.31 -> 0.15, Val Acc: 94.1%
Epoch 5: Loss 0.15 -> 0.08, Val Acc: 95.3%
```

**Result**: 95.3% accuracy on SST-2, compared to 96.1% for full fine-tuning. The soft prompt achieves 99% of fine-tuning performance while updating only 0.002% of parameters.

### Example 2: Multi-Task Model Serving

**Task**: Serve 5 different NLU tasks from a single frozen T5-Large model.

**Setup**:
- Base model: T5-Large (770M parameters, single frozen copy)
- Tasks: SST-2, MNLI, QQP, QNLI, RTE (from GLUE benchmark)
- Each task gets its own 100-token soft prompt (~79K parameters each)
- Total additional parameters: 5 x 79K = 395K (0.05% of model)

**Results**:
| Task | Full Fine-Tune | Prompt Tuning | Gap   |
|------|---------------|---------------|-------|
| SST-2| 94.8%         | 92.1%         | -2.7% |
| MNLI | 88.5%         | 85.3%         | -3.2% |
| QQP  | 91.2%         | 88.7%         | -2.5% |
| QNLI | 93.1%         | 90.4%         | -2.7% |
| RTE  | 78.5%         | 74.2%         | -4.3% |

**Benefit**: Instead of 5 copies of a 770M model (3.85B total parameters), you maintain 1 frozen model + 5 small prompt vectors. Storage reduced by ~80%.

## When to Use

- You need to adapt a large model (10B+) to multiple tasks efficiently
- You want to avoid the storage cost of maintaining separate fine-tuned models per task
- You have sufficient training data (thousands of labeled examples)
- You have access to model weights and can run backpropagation (not API-only)
- You want a simple, well-understood parameter-efficient method

## When to Avoid

- Using API-only models (GPT-4, Claude) where you cannot access embeddings
- Working with small models (under 1B parameters) where the performance gap with fine-tuning is large
- No training data is available
- You need human-interpretable prompts for auditing or compliance
- The task requires rapid iteration without a training pipeline

## Cost & Performance

| Dimension            | Value                          | Notes                                         |
|-----------------------|--------------------------------|-----------------------------------------------|
| Trainable params     | 0.001-0.01% of model           | Typically 20-100 soft tokens                  |
| Training time        | 1-10 hours (single GPU)        | Much faster than full fine-tuning             |
| Inference overhead   | Negligible                     | Only adds N tokens to sequence length         |
| Storage per task     | 10-500 KB                      | vs. GB for full model copies                  |
| Performance (>10B)   | 95-100% of fine-tuning         | Closes gap at scale                           |
| Performance (<1B)    | 70-85% of fine-tuning          | Significant gap at small scale                |

## Variants

- **Random Initialization**: Initialize soft tokens from random vectors. Simplest but may converge slower.
- **Vocabulary Initialization**: Initialize from sampled token embeddings in the model's vocabulary. Provides a better starting point.
- **Text Initialization**: Initialize from the embeddings of a relevant text string. Best for faster convergence and higher final performance.
- **Class-label Initialization**: For classification, initialize from the embeddings of the class labels.

## Composability

- **Multi-task Prompt Tuning**: Train soft prompts for multiple tasks simultaneously with shared and task-specific components.
- **Prompt Ensembling**: Average or concatenate soft prompts trained on different data subsets for improved robustness.
- **Combined with Adapters**: Use prompt tuning alongside adapter layers for even richer task adaptation.
- **Cascaded**: Use one soft prompt for formatting/style and another for task-specific knowledge.

## Limitations

- Requires access to model internals (embedding layer) -- incompatible with API-only models
- Performance degrades significantly for models under 1B parameters
- Soft prompts are not human-interpretable, making debugging and auditing difficult
- Sensitive to initialization strategy and hyperparameters (learning rate, prompt length)
- Cannot capture task-specific knowledge that requires modifying attention patterns deep in the network
- Slightly increases sequence length, which can matter for context-limited applications
- Training still requires labeled data and GPU compute (unlike discrete prompting)

## Sources

- Lester, B., Al-Rfou, R., & Constant, N. (2021). "The Power of Scale for Parameter-Efficient Prompt Tuning." *EMNLP 2021*. *arXiv:2104.08691*. https://arxiv.org/abs/2104.08691
- Liu, X. et al. (2021). "GPT Understands, Too." *arXiv:2103.10385*.
- Li, X.L. & Liang, P. (2021). "Prefix-Tuning: Optimizing Continuous Prompts for Generation." *ACL 2021*.
