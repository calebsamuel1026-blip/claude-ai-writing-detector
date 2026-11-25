# claude-ai-writing-detector

A Claude Code subagent and a small Python lint that block copy and design that read as AI-made before they ship.

## What's here
- **`agents/ai-detector.md`**: a strict reviewer subagent for copy and images. It returns PASS or FAIL as JSON, quotes every tell it finds, and fails anything it isn't sure about.
- **`gate/ai_lint.py`**: a fast, deterministic check for common AI-writing tells.
- **`gate/corpus/ai-phrases.txt`**: about 400 phrases that are rare in human writing but common in chatbot output. The lint loads this list.
- **`gate/RUBRIC.md`**: the full list of copy and design tells, plus the stability rules (majority vote, genre).

## Install
1. Copy `agents/ai-detector.md` into `~/.claude/agents/`, or into a project's `.claude/agents/`.
2. Copy the `gate/` folder into your project.
3. Run the lint:

   ```
   python -I gate/ai_lint.py drafts/*.txt
   echo "some text" | python -I gate/ai_lint.py -
   ```

   It exits with code 1 if any file has a hit, so it works as a pre-commit or CI step.

## How to use it well
- Run the agent 3 times and keep only the tells at least 2 of the runs agree on. A single run is noisy.
- The lint is strict on purpose, so polished human writing can fail it too. Treat a hit as a style rule for your own work, not as proof that a machine wrote the text.
- Add your brand's deliberate choices (tagline, fonts, colours) to the rubric's exceptions, so the gate doesn't keep flagging them.

## License
MIT
