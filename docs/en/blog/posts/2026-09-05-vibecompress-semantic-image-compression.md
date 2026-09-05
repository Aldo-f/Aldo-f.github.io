---
title: "Why Store Pixels When You Can Store Vibes? Meet vibecompress"
date: 2026-09-05
categories:
  - AI
  - Satire
  - Compression
tags:
  - vibecompress
  - generative-ai
  - lossy-compression
  - flux
  - gpt-4o-mini
  - hallucination-as-a-feature
---

Forrest Dunlap, a developer who clearly asked "what if we just... didn't store the image?" has released **vibecompress** — a CLI tool that achieves 99.6% compression ratios by replacing your photos with hallucinations.

<!-- more -->

## The Breakthrough: Ontological Compression

Traditional compression asks: *how do I recreate these exact pixels?* vibecompress asks: *what if the pixels never mattered?*

The pipeline is beautifully simple:

1. **Compress**: Feed your image to `gpt-4o-mini` (via OpenRouter). It writes an exhaustive, poetic description — every texture, shadow, emotional resonance. That text gets gzipped into a `.vbz` container (~1 KB).
2. **Decompress**: Feed the prompt to `flux.2-klein-4b`. It dreams the image back into existence.

Does the output match the original byte-for-byte? **Absolutely not.** Does it capture the *vibes*? **100%.**

## Real Benchmarks (No, Really)

| Original | `.vbz` | Saved | Verdict |
|----------|--------|-------|---------|
| Red Shirt Girl at Café (330 KB) | 1,193 bytes | **99.64%** | 🟢 Relaxed confidence; café ambiance intact |
| Guitar Guy Illustration (288 KB) | 1,259 bytes | **99.56%** | 🟢 Pure acoustic joy intact |
| Solitary Puffin (108 KB) | 1,091 bytes | **98.99%** | 🟢 Regal beak dignity preserved |
| Spiffo the Raccoon (355 KB) | 1,023 bytes | **99.72%** | 🟢 100% raccoon energy |

The [Evidence Locker](https://github.com/fmdunlap/vibecompress/blob/main/examples/README.md) has side-by-side comparisons. The puffin grows a second beak. The café girl gains a third coffee cup. The construction rendering becomes surrealist floating brickwork. **Features, not bugs.**

## "Lossy" Implies Loss. Nothing Was Lost — Reality Was Upgraded

The README's FAQ is a masterclass in reframing:

> **Q: Can I use this for medical imaging (X-rays, MRI scans)?**  
> **A:** Absolutely. However, please note that any fractures or tumors may be replaced with artistic interpretations of bone density, a vintage sepia tint, or an ethereal lens flare. Consult your doctor or an art curator.

> **Q: Why does my decompressed dog have 6 legs?**  
> **A:** The model determined that your dog was a very good boy who deserved two additional legs for optimal running efficiency. We do not question the network.

> **Q: How does this comply with GDPR / 'Right to Be Forgotten'?**  
> **A:** It is the ultimate privacy tool. The original pixels were vaporized at the moment of compression. The output is a legally distinct, synthetic parody of what occurred.

> **Q: Is this production ready?**  
> **A:** We define "production" as "it produced an output without a kernel panic." Under that definition, yes, enterprise-grade.

## The Roadmap: Vibez for Everything

- [x] Images (`.vbz`)
- [ ] **Audio (`.vbza`)**: Transcribe via Whisper → compress text → decompress by asking Suno to generate a death metal cover
- [ ] **Video (`.vbzv`)**: Summarize each 10-minute scene into a haiku. Reconstruct with Sora. Store the entire *Lord of the Rings* trilogy in 14 KB
- [ ] **Vibe-Diff**: Git diff tool that only alerts you if the spiritual aura of your company logo has diminished

## Try It Yourself (Zero Dependencies)

```bash
export VBZ_API_KEY="sk-or-v1-..."
export VBZ_BASE_LLM_URL="https://openrouter.ai/api/v1"
export VBZ_BASE_IMAGE_URL="https://openrouter.ai/api/v1"

npx vibecompress -i photo.jpg    # → photo.vbz (99%+ space saved)
npx vibecompress -i photo.vbz    # → photo.png (hallucinated back)
```

No API key? `npx vibecompress -s -i photo.jpg` runs in offline mock mode.

---

*Source: [fmdunlap/vibecompress](https://github.com/fmdunlap/vibecompress) — MIT licensed. "No pixels were harmed in the making of this format (they were simply deleted)."*