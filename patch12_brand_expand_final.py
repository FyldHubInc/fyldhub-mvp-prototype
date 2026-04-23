import sys, os

# ─── SAFETY GUARD ───────────────────────────────────────────────
TARGET    = "FyldHub_MVP_Prototype.html"
FORBIDDEN = "FyldHub_Combined_Prototype.html"

if not os.path.exists(TARGET):
    print(f"ERROR: {TARGET} not found. Run from ~/Projects/fyldhub-mvp-prototype/")
    sys.exit(1)
if os.path.abspath(TARGET) == os.path.abspath(FORBIDDEN):
    print("ERROR: Targeting enterprise prototype. Aborting.")
    sys.exit(1)
print(f"\u2713 Targeting: {TARGET}")

content = open(TARGET, "r", encoding="utf-8").read()
print(f"\u2713 Current file: {len(content)} chars")

# ─── PATCH 12: Remove ALL brand-expand detail rows ──────────────
# Strategy: find from the first brand-expand row through to just
# before the BRAND RESOURCES comment, replace with closing tags only

START = '<tr class="brand-expand" id="exp-bacardi">'
END   = '<!-- \u2550\u2550\u2550 BRAND RESOURCES'

idx_s = content.find(START)
idx_e = content.find(END)

if idx_s == -1:
    # exp-bacardi already removed — try exp-rtd
    START = '<tr class="brand-expand" id="exp-rtd">'
    idx_s = content.find(START)

if idx_s == -1:
    print("ERROR: No brand-expand rows found — already cleared.")
    sys.exit(0)

if idx_e == -1:
    print("ERROR: BRAND RESOURCES marker not found. Aborting.")
    sys.exit(1)

print(f"  Removing chars {idx_s} to {idx_e} ({idx_e - idx_s} chars)")

# The section between brand-expand start and BRAND RESOURCES comment
# should end with closing tags for tbody/table/card divs
old_section = content[idx_s:idx_e]
count = content.count(old_section)
if count != 1:
    print(f"ERROR: section found {count} times. Aborting.")
    sys.exit(1)

# Replace with just the closing tags needed to close tbody > table > card divs
new_section = '''          </tbody>
        </table>
      </div>
    </div>
</div>

<!-- \u2550\u2550\u2550 BRAND RESOURCES'''

content = content.replace(old_section, new_section, 1)
print("\u2713 Patched: All brand-expand detail rows removed")

# ─── WRITE OUTPUT ───────────────────────────────────────────────
open(TARGET, "w", encoding="utf-8").write(content)
final_len = len(open(TARGET, "r", encoding="utf-8").read())
print(f"\n\u2713 Patch 12 complete. New char count: {final_len}")
