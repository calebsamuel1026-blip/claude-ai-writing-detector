"""AI-tell lint for marketing and outreach copy. Any hit = FAIL.

Usage: python -I ai_lint.py FILE [FILE ...]   (or '-' to read stdin)
Exit code 1 if any file has a hit. Rules: RUBRIC.md in this folder.
Skips the email header block (From/To/Cc/Bcc) and threaded "Re:" subjects.
"""
import re, sys, io

WORDS = r"delve|delves|delving|elevate|elevates|unlock|unlocks|unleash|seamless(?:ly)?|robust|empower(?:s|ing)?|game[- ]changer|tapestry|testament|realm|pivotal|foster(?:s|ing)?|embark|supercharge|cutting[- ]edge|next level|in today's|landscape|journey"
RULES = [
    ("em/en dash", re.compile(r"\s[—–]\s|\w[—]\w|\s-\s(?=\w)")),
    ("semicolon", re.compile(r";")),
    ("exclamation", re.compile(r"!")),
    ("colon label", re.compile(r"(?m)^(?!Subject:|Re:)(?:[A-Z][\w' ]{0,24}):\s+\S|\b(?:The key|Here's the thing|The catch|Bottom line|The truth|Pro tip|Spoiler)\s*:")),
    ("not X but Y", re.compile(r"\bnot (?:just |only |simply )?[\w' ]{1,30},? but\b|\bit'?s not just\b|\bisn't just\b", re.I)),
    ("stock opener", re.compile(r"hope this (?:email |message )?finds you|i wanted to reach out|just reaching out|let'?s dive in|whether you'?re|ready to (?:take|level|ace)|in this fast[- ]paced", re.I)),
    ("AI vocabulary", re.compile(r"\b(?:%s)\b" % WORDS, re.I)),
    ("leverage as verb", re.compile(r"\bleverag(?:e|es|ing)\b(?! ratio| buyout)", re.I)),
    ("navigate (figurative)", re.compile(r"\bnavigat(?:e|ing) (?:the|your|this|recruiting|the process)\b", re.I)),
    # short noun-ish lists: "content, structure and delivery" (items of 1-2 plain words)
    ("rule of three", re.compile(r"(?m)(?<![\w'])(?!(?:I|I'm|I'd|and|or|but|if|reply)\b)[A-Za-z-]+(?:[ ][A-Za-z-]+)?, (?!(?:I|I'm|I'd|and|or|but|if|reply)\b)[A-Za-z-]+(?:[ ][A-Za-z-]+)?,? (?:and|or) [A-Za-z-]+(?:[ ][A-Za-z-]+)?(?!,)[.;!?]?(?=\s|$)")),
    ("stacked reassurance", None),  # counted below
    ("emoji as icon", re.compile(r"(?m)^\s*[✅✨\U0001F680\U0001F4A1\U0001F525⭐\U0001F449\U0001F4C8\U0001F3AF✔]")),
    ("sparkle/robot", re.compile(r"[✨\U0001F916]")),
    ("AI mention", re.compile(r"\bAI[- ]powered\b|\bpowered by AI\b", re.I)),
]
import os
_HERE = os.path.dirname(os.path.abspath(__file__))
def _load_phrases():
    try:
        ps = [l.strip().lower() for l in io.open(os.path.join(_HERE, "corpus", "ai-phrases.txt"), encoding="utf-8") if l.strip() and not l.startswith("#")]
    except OSError:
        return None
    ps = sorted(set(ps), key=len, reverse=True)
    return re.compile("|".join(r"(?<![\w])" + re.escape(x) + (r"(?![\w])" if x[-1].isalnum() else "") for x in ps), re.I)
PHRASES = _load_phrases()
EXTRA = [
    ("Claude drift", re.compile(r"\bthis matters\b|\bwhy [\w' ]{1,30} matters\b|\brather than simply\b|\blooking ahead\b|\bcan help you\b", re.I)),
    ("-ing significance tail", re.compile(r", (?:highlighting|underscoring|showcasing|reflecting|emphasizing|ensuring|cementing|solidifying|marking|signaling|fostering) (?:the|its|their|a|an|how)", re.I)),
    ("chat residue", re.compile(r"utm_source=chatgpt|\[insert|\[your name\]|knowledge cutoff|\bas an ai\b", re.I)),
]
REASSURE = re.compile(r"no worries|no pressure|no reply needed|no need to reply|happy either way|totally fine if not|no rush", re.I)

def body_of(text):
    lines = text.splitlines()
    out = []
    for ln in lines:
        if re.match(r"^(From|To|Cc|Bcc):", ln):
            continue
        if re.match(r"^Subject:\s*Re:", ln, re.I):  # threaded subject keeps its old wording
            continue
        out.append(ln)
    return "\n".join(out)

def lint(text):
    t = body_of(text)
    hits = []
    for name, rx in RULES:
        if rx is None:
            continue
        for m in rx.finditer(t):
            s = t[max(0, m.start() - 25): m.end() + 25].replace("\n", " ")
            hits.append((name, s.strip()))
    if PHRASES is not None:
        for m in PHRASES.finditer(t):
            hits.append(("AI phrase list", t[max(0, m.start()-20): m.end()+20].replace("\n", " ").strip()))
    for name, rx in EXTRA:
        for m in rx.finditer(t):
            hits.append((name, t[max(0, m.start()-20): m.end()+20].replace("\n", " ").strip()))
    sents = [s for s in re.split(r"(?<=[.?!])\s+", re.sub(r"\s+", " ", t)) if len(s.split()) >= 3]
    if len(sents) >= 6:
        ls = [len(s.split()) for s in sents]
        mu = sum(ls) / len(ls); sd = (sum((x - mu) ** 2 for x in ls) / len(ls)) ** 0.5
        if mu and sd / mu < 0.25:
            hits.append(("flat rhythm", f"{len(ls)} sentences, lengths {min(ls)}-{max(ls)} words, spread {sd/mu:.2f}"))
    n = len(REASSURE.findall(t))
    if n > 1:
        hits.append(("stacked reassurance", f"{n} reassurance lines"))
    return hits

def main(paths):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    bad = 0
    for p in paths:
        text = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8", errors="replace").read() if p == "-" else io.open(p, encoding="utf-8", errors="replace").read()
        hits = lint(text)
        if hits:
            bad += 1
            print(f"FAIL {p}")
            for name, s in hits:
                print(f"   [{name}] ...{s}...")
        else:
            print(f"pass {p}")
    print(f"\n{bad} of {len(paths)} failed")
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or ["-"]))
