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

content = open(TARGET, "r", encoding="utf-8").read()
print(f"\u2713 Current file: {len(content)} chars")

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
# PATCH 13A: Clear brands-tbody completely
# Replace everything between <tbody id="brands-tbody"> and </tbody>
# with our empty state row
# ═══════════════════════════════════════════════════════════════
tbody_start = '<tbody id="brands-tbody">'
# Find the tbody and its content up to </tbody>
idx_tbody = content.find(tbody_start)
if idx_tbody == -1:
    print("ERROR: brands-tbody not found")
    sys.exit(1)

# Find matching </tbody> after the brands-tbody
idx_after_start = idx_tbody + len(tbody_start)
idx_close = content.find('</tbody>', idx_after_start)
if idx_close == -1:
    print("ERROR: closing </tbody> not found")
    sys.exit(1)

old_tbody_content = content[idx_after_start:idx_close]
new_tbody_content = '''
              <tr>
                <td colspan="5" style="text-align:center;padding:48px 24px;color:var(--slate)">
                  <div style="font-size:15px;font-weight:600;color:var(--dark);margin-bottom:6px">No brands yet</div>
                  <div style="font-size:13px;margin-bottom:16px">Add your first brand to get started. Each brand has its own product catalog and settings.</div>
                  <button class="btn btn-primary btn-sm" onclick="openAddBrand()">+ Add Brand</button>
                </td>
              </tr>
            '''

print(f"  Replacing brands-tbody content ({len(old_tbody_content)} chars)")
if content.count(content[idx_tbody:idx_close + 8]) == 1:
    content = content[:idx_after_start] + new_tbody_content + content[idx_close:]
    print("\u2713 Patched: brands-tbody cleared \u2014 empty state inserted")
else:
    print("ERROR: tbody block not unique. Aborting.")
    sys.exit(1)

# ═══════════════════════════════════════════════════════════════
# PATCH 13B: Zero out PRODS data object
# ═══════════════════════════════════════════════════════════════
prods_match = re.search(r'var PRODS=\{.*?\};', content, re.DOTALL)
if prods_match:
    old_prods = prods_match.group(0)
    if content.count(old_prods) == 1:
        content = content.replace(old_prods, "var PRODS={};", 1)
        print("\u2713 Patched: PRODS data zeroed out")
    else:
        print(f"WARNING: PRODS found {content.count(old_prods)} times, skipping")
else:
    print("WARNING: PRODS not found via regex, skipping")

# ═══════════════════════════════════════════════════════════════
# PATCH 13C: Remove the <!-- BACARDÍ Rum --> comment
# that might be causing visual artifacts
# ═══════════════════════════════════════════════════════════════
if '<!-- BACARD\u00cd Rum -->' in content:
    count = content.count('<!-- BACARD\u00cd Rum -->')
    if count == 1:
        content = content.replace('<!-- BACARD\u00cd Rum -->', '', 1)
        print("\u2713 Patched: Removed BACARD\u00cd Rum HTML comment")

# ═══════════════════════════════════════════════════════════════
# WRITE OUTPUT
# ═══════════════════════════════════════════════════════════════
open(TARGET, "w", encoding="utf-8").write(content)
final_len = len(open(TARGET, "r", encoding="utf-8").read())
print(f"\n\u2713 Patch 13 complete. New char count: {final_len}")
