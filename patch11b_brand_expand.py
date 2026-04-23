import sys, os, re

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

# ─── BASELINE CHECK ─────────────────────────────────────────────
content = open(TARGET, "r", encoding="utf-8").read()
# Note: baseline will be whatever patch11 left us at — use dynamic check
baseline = len(content)
print(f"\u2713 Current file: {baseline} chars")

# ─── PATCH HELPER ───────────────────────────────────────────────
def rep(old, new, label):
    global content
    count = content.count(old)
    if count != 1:
        print(f"ERROR [{label}]: Expected 1 occurrence, found {count}. Aborting.")
        sys.exit(1)
    content = content.replace(old, new, 1)
    print(f"\u2713 Patched: {label}")

# ═══════════════════════════════════════════════════════════════
# PATCH 11B: Remove all brand-expand detail rows
# These are <tr class="brand-expand"> elements containing full
# product/SKU tables for BACARD\u00cd Rum, BACARD\u00cd RTD, and PATR\u00d3N
# Strategy: find from first brand-expand tr to end of brands tbody
# ═══════════════════════════════════════════════════════════════

# Find the start of brand-expand section (first one is exp-rtd after patch10)
expand_start = '<tr class="brand-expand" id="exp-rtd">'
# Find the end marker — closing of the brands table
table_end = '          </tbody>\n        </table>\n      </div>\n    </div>\n</div>\n\n<!-- \u2550\u2550\u2550 BRAND RESOURCES'

idx_start = content.find(expand_start)
idx_end   = content.find(table_end)

if idx_start == -1:
    print("ERROR: brand-expand start not found")
    sys.exit(1)
if idx_end == -1:
    # Try alternate ending
    table_end = '<!-- \u2550\u2550\u2550 BRAND RESOURCES'
    idx_end = content.find(table_end)
    if idx_end == -1:
        print("ERROR: table end / Brand Resources marker not found")
        sys.exit(1)
    # Walk back to find the </div> that closes the brands card
    close_pos = content.rfind('</div>\n\n<!-- \u2550\u2550\u2550 BRAND RESOURCES', 0, idx_end + 50)
    if close_pos != -1:
        idx_end = close_pos + len('</div>\n\n')
    else:
        idx_end = idx_end  # just cut right before BRAND RESOURCES comment

print(f"  brand-expand start: char {idx_start}")
print(f"  section end: char {idx_end}")

old_section = content[idx_start:idx_end]
count = content.count(old_section)
if count != 1:
    print(f"ERROR: section found {count} times, aborting")
    sys.exit(1)

# Replace with just the closing tags needed to close the tbody/table/card divs
new_section = '''          </tbody>
        </table>
      </div>
    </div>
</div>

<!-- \u2550\u2550\u2550 BRAND RESOURCES'''

content = content.replace(old_section, new_section, 1)
print("\u2713 Patched: brand-expand detail rows removed (all 3 brands)")

# ═══════════════════════════════════════════════════════════════
# WRITE OUTPUT
# ═══════════════════════════════════════════════════════════════
open(TARGET, "w", encoding="utf-8").write(content)
final_len = len(open(TARGET, "r", encoding="utf-8").read())
print(f"\n\u2713 Patch 11b complete. New char count: {final_len}")
