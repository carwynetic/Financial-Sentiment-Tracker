# Master Scientific Benchmark Results

| Paradigm                 | Model                        |   Accuracy |   Macro Precision |   Macro Recall |   Macro F1 |   Weighted F1 |
|:-------------------------|:-----------------------------|-----------:|------------------:|---------------:|-----------:|--------------:|
| Tier 1: Lexicon          | Loughran-McDonald            |     0.5618 |            0.4401 |         0.4354 |     0.4352 |        0.5558 |
| Tier 2: Classical ML     | Multinomial NB               |     0.7471 |            0.804  |         0.526  |     0.5387 |        0.702  |
| Tier 2: Classical ML     | Logistic Regression          |     0.8571 |            0.8463 |         0.7868 |     0.8123 |        0.8538 |
| Tier 2: Classical ML     | Linear SVM                   |     0.8649 |            0.8788 |         0.7724 |     0.8129 |        0.8591 |
| Tier 3: Transformer (ZS) | FinBERT Zero-Shot (ProsusAI) |     0.971  |            0.9543 |         0.9802 |     0.9664 |        0.9713 |
| Tier 3: Transformer (ZS) | FinBERT Zero-Shot (HKUST)    |     0.8842 |            0.8911 |         0.8422 |     0.8622 |        0.8806 |
| Tier 3: Transformer (FT) | FinBERT Fine-Tuned (HKUST)   |     0.9208 |            0.8897 |         0.9069 |     0.8976 |        0.921  |
| Extension: Entity-Aware  | Entity-FinBERT (SEntFiN 1.0) |     0.8409 |            0.8431 |         0.8394 |     0.8411 |        0.8409 |
