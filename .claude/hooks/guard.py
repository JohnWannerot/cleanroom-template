# Clean room-vakt. Anrop: guard.py clean|dirty  (PreToolUse, JSON på stdin). Exit 2 = blockera.
import json, re, sys

sys.stderr.reconfigure(encoding="utf-8")
mode = sys.argv[1]
d = json.load(sys.stdin)
tool = d.get("tool_name", "")
inp = d.get("tool_input", {})
s = json.dumps(inp).replace("\\\\", "/").lower()

def block(msg):
    print(f"[cleanroom:{mode}] {msg}", file=sys.stderr)
    sys.exit(2)

if tool in ("Write", "Edit", "MultiEdit", "NotebookEdit", "Bash", "PowerShell") and re.search(r"\.claude/(settings|hooks)", s):
    block("Clean room-vakten får inte ändras av modellen.")

# ponytail: textmatch på sökväg, inte sandlåda. Kör alltid clean-sessionen med cwd = clean/.
if mode == "clean" and re.search(r"\bdirty\b|\.gzf\b|\.gpr\b|ghidra", s):
    block("Clean-sidan får aldrig röra dirty/ eller Ghidra. Bara spec/ är tillåten källa.")

# Ghidra-artefakter = dekompilerad kod har läckt in i specen
GHIDRA = r"\b(fun|dat|lab|ptr|sub)_[0-9a-f]{4,}\b|\bparam_\d+\b|\blocal_[0-9a-f]+\b|\bundefined[1248]?\b|\b[a-z]{1,3}var\d+\b"
if mode == "dirty" and tool in ("Write", "Edit", "MultiEdit") and "spec/" in s:
    text = " ".join(str(inp.get(k, "")) for k in ("content", "new_string")) + json.dumps(inp.get("edits", ""))
    m = re.search(GHIDRA, text, re.I)
    if m:
        block(f"Specen innehåller dekompilerings-artefakt '{m.group(0)}'. Beskriv beteende, inte kod.")
