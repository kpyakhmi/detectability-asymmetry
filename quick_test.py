# Paste this into a single Colab cell and run it.
# Takes ~30 seconds. Tells us which provider+model identifiers actually work.

import os

# Load secrets the same way the main notebook does
def _load_secret(name):
    try:
        from google.colab import userdata
        v = userdata.get(name)
        if v:
            return v.strip()
    except Exception:
        pass
    return os.environ.get(name, '').strip()

GROQ_KEY     = _load_secret('GROQ_API_KEY')
GEMINI_KEY   = _load_secret('GEMINI_API_KEY')
CEREBRAS_KEY = _load_secret('CEREBRAS_API_KEY')

# Candidate model names to test
GROQ_CANDIDATES     = ['llama-3.3-70b-versatile', 'llama-3.1-8b-instant']
GEMINI_CANDIDATES   = ['gemini-2.0-flash', 'gemini-2.0-flash-001', 'gemini-2.0-flash-lite', 'gemini-2.5-flash']
CEREBRAS_CANDIDATES = ['llama3.3-70b', 'llama-3.3-70b', 'llama-3.3-70b-instruct', 'llama3.1-8b']

results = {}

# --- Groq ---
print("=" * 60)
print("GROQ")
print("=" * 60)
try:
    from groq import Groq
    client = Groq(api_key=GROQ_KEY)
    for m in GROQ_CANDIDATES:
        try:
            r = client.chat.completions.create(
                model=m,
                messages=[{'role': 'user', 'content': 'Say hi.'}],
                max_tokens=20,
            )
            print(f"  OK  {m}: {r.choices[0].message.content.strip()[:60]}")
            results[f'groq/{m}'] = 'OK'
        except Exception as e:
            print(f"  ERR {m}: {type(e).__name__}: {str(e)[:120]}")
            results[f'groq/{m}'] = 'ERR'
except Exception as e:
    print(f"  Groq client failed: {e}")

# --- Gemini ---
print()
print("=" * 60)
print("GEMINI (google-genai SDK)")
print("=" * 60)
try:
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=GEMINI_KEY)
    for m in GEMINI_CANDIDATES:
        try:
            r = client.models.generate_content(
                model=m,
                contents='Say hi.',
                config=types.GenerateContentConfig(max_output_tokens=20),
            )
            print(f"  OK  {m}: {(r.text or '').strip()[:60]}")
            results[f'gemini/{m}'] = 'OK'
        except Exception as e:
            print(f"  ERR {m}: {type(e).__name__}: {str(e)[:120]}")
            results[f'gemini/{m}'] = 'ERR'
except Exception as e:
    print(f"  Gemini client failed: {e}")

# --- Cerebras ---
print()
print("=" * 60)
print("CEREBRAS")
print("=" * 60)
try:
    from cerebras.cloud.sdk import Cerebras
    client = Cerebras(api_key=CEREBRAS_KEY)
    for m in CEREBRAS_CANDIDATES:
        try:
            r = client.chat.completions.create(
                model=m,
                messages=[{'role': 'user', 'content': 'Say hi.'}],
                max_tokens=20,
            )
            print(f"  OK  {m}: {r.choices[0].message.content.strip()[:60]}")
            results[f'cerebras/{m}'] = 'OK'
        except Exception as e:
            print(f"  ERR {m}: {type(e).__name__}: {str(e)[:120]}")
            results[f'cerebras/{m}'] = 'ERR'
except Exception as e:
    print(f"  Cerebras client failed: {e}")

print()
print("=" * 60)
print("SUMMARY")
print("=" * 60)
for k, v in results.items():
    print(f"  {v}: {k}")
