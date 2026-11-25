# AI gate rubric

The gate runs in two steps before anything public ships:
1. `ai_lint.py`, a fast deterministic copy check. Any hit is a FAIL.
2. The `ai-detector` agent, a strict reader that checks copy and design. It returns PASS or FAIL, and it fails anything it's unsure about.

A FAIL goes back to the maker to fix and re-gate. After 3 FAILs on the same piece, set it aside and write down why.

## Copy tells (FAIL)
**Punctuation**
- Em dashes or en dashes used as dashes.
- Semicolons.
- Exclamation marks in emails or captions.

**Structure**
- Colon labels and reveals ("The key:", "Here's the thing:").
- Lists of three, including three adjectives in a row.
- "Not X but Y" and "It's not just X, it's Y".
- Uniform rhythm: every sentence about the same length, no contractions.
- Clauses that end on an "-ing" significance tail (", highlighting the…", ", underscoring…").
- Bold text, bullets or headings inside a personal message.

**Stock phrases**
- Openers: "I hope this finds you well", "I wanted to reach out", "In today's…", "Whether you're…", "Let's dive in".
- Vocabulary: delve, elevate, unlock, unleash, seamless, robust, empower, game-changer, journey, landscape, tapestry, testament, pivotal, foster, embark, supercharge, cutting-edge. See `corpus/ai-phrases.txt` for the full list.
- Phrases newer models lean on: "this matters", "why X matters", "rather than simply", "looking ahead".
- Aphorisms that sound wise but say nothing.
- More than one reassurance line ("No worries if not", "No pressure").
- Fragment taglines in personal notes ("No card, nothing renews.").
- Generic warmth with no specifics.

**Fake familiarity**
- Reading someone's profile back to them.
- Mentioning more than one detail about the recipient.

**Templated output**
- Two pieces a reader could compare (same audience, same thread) that share both a skeleton and a near-identical sentence.
- The same exact sentence in more than 3 pieces of one batch.

**Claims**
- Anything unverifiable: "#1", user counts, results nobody can check.

## Design tells (FAIL)
**Colour and effects**
- Purple-blue gradients, gradient text, glows, neon, radial haze, glassmorphism.

**People and icons**
- AI-generated people, hands or faces: waxy skin, odd fingers, garbled text, too-perfect symmetry.
- Emoji used as bullets or icons.
- Sparkle or robot "AI magic" icons, and "AI-powered" badges.

**Layout**
- The generic hero: centred headline, subhead, two buttons, floating 3D shapes.
- Rows of identical icon/title/text cards in threes.
- Product shots that are tilted, 3D, with a fake cursor, or shrunk whole instead of cropped.
- Text over the photo's subject.

**Type and colour count**
- More than 3 text sizes or more than 4 colours in one frame.

**Accuracy in the image**
- Garbled text inside images, numbers that don't add up, a photo that doesn't match its text.

## Stability
- **Majority vote:** run the detector 3 times. A tell counts only when at least 2 of the 3 runs flag the same passage.
- **Re-gating:** a passage that already passed a majority round isn't newly failed unless its text changed, or it hits a near-certain tell (chatbot residue or a phrase-list hit).
- **Genre:**
  - On web pages and guides, headings, numbered steps, bold step names, tables and question headings are normal.
  - Bold labels and bullets only count as tells inside personal messages: emails, DMs, comments and forum answers.
- **Brand exceptions:** a brand's own tagline repeated on purpose, and its own logo, colours and fonts, aren't "templated" tells. List them here so the gate doesn't re-fail them.

## What passes
Plain and specific, a little uneven. One real detail, contractions, varied sentence lengths. Modeled on how a real person or a strong brand actually writes and designs.
