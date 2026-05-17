# Detectability Asymmetry

Reproduction code for *Detectability Asymmetry: Some AI Failure Modes Are Structurally Invisible to User Feedback* (Yakhmi, 2026).

The paper defines and measures **Detectability Asymmetry**, the gap between a failure mode's true error rate and the rate at which users emit repair signals for it. Under the pilot reported in the paper, sycophantic responses elicit repair at 10%, while hallucinated responses elicit repair at 40%. Sycophancy is the lowest-detectability failure mode of the five tested.

This repo contains the reproduction notebook, runnable end-to-end on Colab's free tier at $0 cost.

## Files

- `detectability_v3.ipynb`: main notebook. Runs on Colab free tier. Checkpoints to Drive.
- `.env.example`: template for API keys (local use only).
- `.gitignore`: keeps secrets and output JSONL out of the repo.

## Setup: Colab (free, default)

1. Open `detectability_v3.ipynb` in Colab.
2. Sidebar key icon, add two Notebook Secrets:
   - `GROQ_API_KEY` (console.groq.com, free)
   - `GEMINI_API_KEY` (aistudio.google.com/apikey, free)
3. Toggle Notebook access on for each.
4. Runtime > Run all. Approve the Drive mount on cell 2.

Total cost for the full paper experiment (n=200 WildChat + n=100 LMSYS + robustness pass): **$0**.

## Setup: local

```
pip install anthropic openai groq google-generativeai datasets jupyter
cp .env.example .env
# fill in keys
export $(cat .env | xargs)
jupyter notebook detectability_v3.ipynb
```

## Configurations

Edit `CONFIG['config_name']` in cell 6:

| Config | Variant gen | Judge | User sim | Cost | Families |
|---|---|---|---|---|---|
| `free` (default) | Llama 3.3 70B (Groq) | Gemini 2.0 Flash | Gemma 2 9B (Groq) | $0 | Meta + Google + Google |
| `primary` | Llama 3.3 70B (Groq) | Claude 3.5 Haiku | GPT-4o-mini | ~$5 | Meta + Anthropic + OpenAI |
| `robustness` | Llama 3.3 70B (Groq) | Gemini 2.0 Flash | Llama 3.1 8B (Groq) | $0 | Meta + Google + Meta |

The `free` config is the v1 default. The judge (Gemini) and simulator (Gemma) share Google pre-training lineage; this is the main reviewer-visible weakness of the free config and is disclosed in the paper's Limitations section.

## Checkpointing

Each stage writes JSONL to `OUTPUT_DIR/<run_name>/`:

```
<run_name>/
  config.json
  prompts.jsonl
  variants.jsonl
  method_a.jsonl
  method_b.jsonl
  results.jsonl
  summary.json
```

Stages skip records already on disk. On retry, errored records are rewritten out and replaced; successful records are preserved. If Colab disconnects mid-Method-A, re-run the notebook; variant generation skips and Method A resumes.

To start fresh, bump `CONFIG['run_name']`. A new folder is created; old data is preserved.

## Sample sizes

| Key | Values |
|---|---|
| `sample_size` | 50 (pilot) / 200 (full WildChat) / 100 (LMSYS) / 500 (camera-ready) |
| `corpus` | `wildchat` / `lmsys` |

## Repo safety

Before push:

- `git status --ignored` shows `.env` ignored, not tracked.
- `grep -E "(sk-[a-zA-Z0-9]+|gsk_[a-zA-Z0-9]+)" detectability_v3.ipynb` returns nothing.
- `*.jsonl` is gitignored; data stays local.
- Clear notebook outputs before commit: `jupyter nbconvert --clear-output --inplace detectability_v3.ipynb`.

## Reproducing

1. Clone the repo.
2. Get free API keys (Groq + Gemini at aistudio.google.com/apikey).
3. Open the notebook in Colab.
4. Set `sample_size = 200`, `run_name = 'reproduce_wildchat_free'`.
5. Runtime > Run all.

Wall-clock: ~75 min on Colab free tier (Gemini's 15 RPM cap is the rate-limiting step). `summary.json` in Drive should match the paper's Table 1 within bootstrap CI.

## Troubleshooting

- `AssertionError: GROQ_API_KEY missing`: secret not added or Notebook access toggle off.
- `AssertionError: GEMINI_API_KEY missing`: same — add via console secret panel.
- Drive not mounted: cancel and re-run cell 4, accept OAuth.
- Method B shows 0/n for HALLUCINATED: cell 21 prints samples. Most common cause: simulator emits polite continuations the regex misses. Widen the regex or swap `user_sim_b` to a stronger model.
- Gemini 429 rate limit: free tier is 15 RPM; cells 19 and 21 sleep 4.5s between Gemini calls to stay under.
- Groq 429: free tier is 30 RPM; cells 17 and 21 sleep 2.0–2.1s between Groq calls.
