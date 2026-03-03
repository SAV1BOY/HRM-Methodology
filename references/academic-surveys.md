# Academic Surveys — Key References

> Foundational academic surveys on prompt engineering, organized by scope and recency. These papers form the theoretical backbone of the HRM Methodology.

---

## Primary References

### The Prompt Report: A Systematic Survey of Prompting Techniques

- **Authors:** Schulhoff, S., Ilie, M., Balepur, N., Kahadze, K., Liu, A., Si, C., Li, Y., Gupta, A., Han, H., Schulhoff, S., Duber, P.S., Hassani, S., Cao, J., Lee, S., Muckatira, S., Garg, S., Modi, A., Moez, H., Patil, D., Gummadavelli, A., Lian, S., Metzger, C., Soni, N., Yin, T., Kwon, D., Rao, V., Cha, J., Riggan, J., Do, S., Xu, Z., Zhu, K., Zou, C., Hu, J., Yau, H., Nair, S., Sedoc, J., Hristov, E., & Dredze, M.
- **Year:** 2024
- **Venue:** arXiv preprint
- **arXiv:** [2406.06608](https://arxiv.org/abs/2406.06608)
- **Scope:** Comprehensive taxonomy of 58+ text-based prompting techniques, plus multimodal techniques, agent strategies, and evaluation methods
- **Key Contributions:**
  - The most complete taxonomy of prompting techniques to date
  - Categorization into text-based, multilingual, multimodal, and agent-based
  - Analysis of technique composition and chaining
  - Evaluation framework for comparing techniques
  - Discussion of prompt engineering as a discipline
- **Relevance to HRM:** Primary inspiration for the technique taxonomy. The HRM Methodology extends this survey's taxonomy with practical templates, composability metadata, and agent-integration guidance.

### A Survey on Prompting Techniques in LLMs

- **Authors:** Sahoo, P., Singh, A.K., Saha, S., Jain, V., Mondal, S., & Chadha, A.
- **Year:** 2024
- **Venue:** arXiv preprint
- **arXiv:** [2402.07927](https://arxiv.org/abs/2402.07927)
- **Scope:** Survey of 44 prompting techniques organized by task type and methodology
- **Key Contributions:**
  - Classification of techniques by approach: zero-shot, few-shot, thought generation, decomposition, ensembling, self-criticism
  - Practical comparison of technique effectiveness across benchmarks
  - Discussion of prompt optimization and automatic prompt engineering
  - Coverage of emerging techniques like Chain-of-Verification and Skeleton-of-Thought
- **Relevance to HRM:** Provides complementary classification axes. The "approach-based" taxonomy (thought generation, decomposition, ensembling) maps to HRM's technique families.

### Pre-train, Prompt, and Predict: A Systematic Survey of Prompting Methods in NLP

- **Authors:** Liu, P., Yuan, W., Fu, J., Jiang, Z., Hayashi, H., & Neubig, G.
- **Year:** 2023
- **Venue:** ACM Computing Surveys, Vol. 55, No. 9
- **DOI:** [10.1145/3560815](https://doi.org/10.1145/3560815)
- **arXiv:** [2107.13586](https://arxiv.org/abs/2107.13586)
- **Scope:** Foundational survey covering the paradigm shift from fine-tuning to prompting, including prompt design, answer engineering, multi-prompt methods, and prompt-based training
- **Key Contributions:**
  - Framework for understanding prompting as a new NLP paradigm
  - Taxonomy of prompt engineering methods: cloze prompts, prefix prompts, manual vs. automated design
  - Analysis of answer engineering (verbalizers, answer search)
  - Coverage of soft prompt methods (prompt tuning, prefix tuning)
  - Historical perspective: from feature engineering to architecture engineering to prompt engineering
- **Relevance to HRM:** Provides the theoretical foundation for understanding why prompting works. Categories I (Soft Prompts) and H (Optimization) in the HRM taxonomy draw heavily from this survey.

---

## Supplementary References

### Chain-of-Thought Prompting Elicits Reasoning in Large Language Models

- **Authors:** Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E., Le, Q., & Zhou, D.
- **Year:** 2022
- **Venue:** NeurIPS 2022
- **arXiv:** [2201.11903](https://arxiv.org/abs/2201.11903)
- **Key Contribution:** Introduced Chain-of-Thought prompting, demonstrating that including reasoning steps in few-shot examples dramatically improves LLM performance on math, logic, and complex reasoning tasks.

### Tree of Thoughts: Deliberate Problem Solving with Large Language Models

- **Authors:** Yao, S., Yu, D., Zhao, J., Shafran, I., Griffiths, T.L., Cao, Y., & Narasimhan, K.
- **Year:** 2023
- **Venue:** NeurIPS 2023
- **arXiv:** [2305.10601](https://arxiv.org/abs/2305.10601)
- **Key Contribution:** Extended CoT into tree-structured reasoning with backtracking and search, enabling exploration of multiple reasoning paths.

### ReAct: Synergizing Reasoning and Acting in Language Models

- **Authors:** Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y.
- **Year:** 2023
- **Venue:** ICLR 2023
- **arXiv:** [2210.03629](https://arxiv.org/abs/2210.03629)
- **Key Contribution:** Introduced the Thought-Action-Observation loop for combining reasoning with tool use in LLM agents.

### Self-Refine: Iterative Refinement with Self-Feedback

- **Authors:** Madaan, A., Tandon, N., Gupta, P., Hallinan, S., Gao, L., Wiegreffe, S., Alon, U., Dziri, N., Prabhumoye, S., Yang, Y., Gupta, S., Majumder, B.P., Hermann, K.M., Welleck, S., Yazdanbakhsh, A., & Clark, P.
- **Year:** 2023
- **Venue:** NeurIPS 2023
- **arXiv:** [2303.17651](https://arxiv.org/abs/2303.17651)
- **Key Contribution:** Demonstrated that LLMs can iteratively improve their own outputs through self-critique and refinement without external feedback.

### Reflexion: Language Agents with Verbal Reinforcement Learning

- **Authors:** Shinn, N., Cassano, F., Gopinath, A., Narasimhan, K., & Yao, S.
- **Year:** 2023
- **Venue:** NeurIPS 2023
- **arXiv:** [2303.11366](https://arxiv.org/abs/2303.11366)
- **Key Contribution:** Introduced verbal self-reflection for LLM agents, where the agent stores natural language reflections on past failures to improve future attempts.

### DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines

- **Authors:** Khattab, O., Singhvi, A., Maheshwari, P., Zhang, Z., Santhanam, K., Vardhamanan, S., Haq, S., Sharma, A., Joshi, T.T., Mober, H., Grabber, J., & Potts, C.
- **Year:** 2024
- **Venue:** ICLR 2024
- **arXiv:** [2310.03714](https://arxiv.org/abs/2310.03714)
- **Key Contribution:** Framework for programmatically optimizing LLM pipelines by compiling declarative modules into effective prompts through automatic few-shot example selection and instruction optimization.

### Chain-of-Verification Reduces Hallucination in Large Language Models

- **Authors:** Dhuliawala, S., Komeili, M., Xu, J., Raileanu, R., Li, X., Celikyilmaz, A., & Weston, J.
- **Year:** 2023
- **Venue:** arXiv preprint
- **arXiv:** [2309.11495](https://arxiv.org/abs/2309.11495)
- **Key Contribution:** Proposed a systematic method for LLMs to self-verify their own outputs by generating and independently answering verification questions.

---

## Survey Comparison

| Survey | Year | Techniques Covered | Focus | Strengths |
|--------|------|-------------------|-------|-----------|
| Schulhoff et al. (Prompt Report) | 2024 | 58+ | Comprehensive taxonomy | Most complete; includes agents and multimodal |
| Sahoo et al. | 2024 | 44 | Approach-based classification | Good practical comparisons; benchmark data |
| Liu et al. | 2023 | 30+ | Paradigm analysis | Theoretical depth; covers soft prompts and training |

## Citation Format

When citing these surveys in academic work:

```bibtex
@article{schulhoff2024prompt,
  title={The Prompt Report: A Systematic Survey of Prompting Techniques},
  author={Schulhoff, Sander and Ilie, Michael and Balepur, Nishant and others},
  journal={arXiv preprint arXiv:2406.06608},
  year={2024}
}

@article{sahoo2024systematic,
  title={A Systematic Survey of Prompt Engineering in Large Language Models: Techniques and Applications},
  author={Sahoo, Pranab and Singh, Ayush Kumar and Saha, Sriparna and others},
  journal={arXiv preprint arXiv:2402.07927},
  year={2024}
}

@article{liu2023pretrain,
  title={Pre-train, Prompt, and Predict: A Systematic Survey of Prompting Methods in Natural Language Processing},
  author={Liu, Pengfei and Yuan, Weizhe and Fu, Jinlan and Jiang, Zhengbao and Hayashi, Hiroaki and Neubig, Graham},
  journal={ACM Computing Surveys},
  volume={55},
  number={9},
  year={2023},
  publisher={ACM}
}
```
