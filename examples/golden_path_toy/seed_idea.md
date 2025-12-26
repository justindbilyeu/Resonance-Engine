# Seed Idea: Random Coin Flip Fairness Test

**Research Question:** Does a simulated coin flip produce heads and tails with approximately equal probability over many trials?

**Motivation:** This is a toy example demonstrating the full Resonance Engine workflow with a simple, deterministic experiment. We can verify that:
1. The null completeness gate accepts our numeric thresholds
2. The experiment can run and produce measurable results
3. Null hypotheses can be evaluated against experimental outcomes
4. The bundle contract is satisfied

**Expected Outcome:** For a fair coin (p=0.5) over N=1000 trials, we expect approximately 500 heads. We will reject the fairness hypothesis if the proportion deviates significantly from 0.5.

**Why This Example:**
- Simple enough to understand immediately
- Deterministic and reproducible (fixed random seed)
- Has clear numeric rejection criteria
- Demonstrates the full golden path from seed → results
