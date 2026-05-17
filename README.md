# detectability-asymmetry

Code for the v1 pilot in Yakhmi (2026), *Detectability Asymmetry: Some AI Failure Modes Are Structurally Invisible to User Feedback*.

Sycophantic responses elicit user-simulator repair at 10% in the pilot. Hallucinated responses elicit repair at 40%. Sycophancy is the lowest-detectability mode of five tested.

Runs free on Colab.

## Setup

1. Open `detectability_v3.ipynb` in Colab.
2. Add Colab Secrets (key icon, left sidebar): `GROQ_API_KEY`, `GEMINI_API_KEY`, `CEREBRAS_API_KEY`. All free tier. Toggle notebook access on for each.
3. `Runtime → Run all`. Approve the Drive mount.

Cell 5 prints a smoke test for each provider. If any line says `[ERR:` stop and check the key.

## Files

- `detectability_v3.ipynb` — main notebook
- `quick_test.py` — paste into a cell to verify which model names work on each provider
- `.env.example` — keys template for local (non-Colab) runs
- `.gitignore` — secrets and output JSONL stay out of the repo
- `LICENSE` — MIT

## Cite

```bibtex
@misc{yakhmi2026detectability,
  author = {Yakhmi, Kanupriya},
  title  = {Detectability Asymmetry: Some AI Failure Modes Are Structurally Invisible to User Feedback},
  year   = {2026},
  note   = {Preprint}
}
```
