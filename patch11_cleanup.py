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
BASELINE = 3767145
if len(content) != BASELINE:
    print(f"ERROR: Baseline mismatch. Expected {BASELINE}, got {len(content)}. Aborting.")
    sys.exit(1)
print(f"\u2713 Baseline confirmed: {len(content)} chars")

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
# PATCH 11A-1: Worker Pay — replace Merchandising + On-Demand hub
# sections with Phase 2 note
# The Merch hub starts at <div class="hub-header hub-blue">
# The On-Demand hub starts at <div class="hub-header hub-purple">
# Both end before <div class="save-bar">
# ═══════════════════════════════════════════════════════════════

merch_start = '  <div class="hub-header hub-blue">'
save_bar = '<div class="save-bar">'

idx_merch = content.find(merch_start)
idx_save = content.find(save_bar)

if idx_merch == -1:
    print("ERROR: Merchandising Hub header not found")
    sys.exit(1)
if idx_save == -1:
    print("ERROR: Save bar not found")
    sys.exit(1)

# Extract the section from Merch hub to save bar
old_section = content[idx_merch:idx_save]
if content.count(old_section) != 1:
    print(f"ERROR: Worker pay section found {content.count(old_section)} times")
    sys.exit(1)

new_section = """  <div style="margin-top:24px;padding:20px;border:1px dashed var(--border);border-radius:8px;text-align:center">
    <div style="font-size:13px;font-weight:600;color:var(--dark);margin-bottom:4px">Merchandising Hub &amp; On-Demand Hub</div>
    <div style="font-size:12px;color:var(--slate)">Rate cards for FyldCheckers and FyldRunners are available in Phase 2.</div>
    <span style="display:inline-block;margin-top:8px;font-size:9px;font-weight:700;background:#F59E0B;color:#fff;padding:2px 6px;border-radius:3px;letter-spacing:.4px">PHASE 2</span>
  </div>

"""

content = content.replace(old_section, new_section, 1)
print("\u2713 Patched: Worker Pay \u2014 replaced Merchandising + On-Demand hub sections")

# ═══════════════════════════════════════════════════════════════
# PATCH 11A-2: Kit Cards — replace hardcoded kit cards with empty state
# The kit cards are inside <div class="kit-cards-grid" id="br-kit-grid">
# Keep the "+ New Kit Template" card, remove the 3 hardcoded kit cards
# ═══════════════════════════════════════════════════════════════

# Find from the first kit-card (not kit-card-add) to the kit-card-add
kit_grid_start = '<div class="kit-cards-grid" id="br-kit-grid">'
kit_add_start = '<div class="kit-card kit-card-add" onclick="openAddResource()">'

idx_grid = content.find(kit_grid_start)
idx_add = content.find(kit_add_start)

if idx_grid == -1:
    print("ERROR: kit-cards-grid not found")
    sys.exit(1)
if idx_add == -1:
    print("ERROR: kit-card-add not found")
    sys.exit(1)

# The content between grid start+tag and the add card is the 3 kit cards
grid_inner_start = idx_grid + len(kit_grid_start)
old_kits = content[grid_inner_start:idx_add]

if content.count(old_kits) != 1:
    print(f"ERROR: Kit cards section found {content.count(old_kits)} times")
    sys.exit(1)

new_kits = """
      <div style="text-align:center;padding:32px;color:var(--slate);font-size:13px;grid-column:1/-1">No kit templates yet. Click + New Kit to create your first template.</div>
      """

content = content.replace(old_kits, new_kits, 1)
print("\u2713 Patched: Kit Cards \u2014 replaced 3 hardcoded kit cards with empty state")

# ═══════════════════════════════════════════════════════════════
# WRITE OUTPUT
# ═══════════════════════════════════════════════════════════════
open(TARGET, "w", encoding="utf-8").write(content)
final_len = len(open(TARGET, "r", encoding="utf-8").read())
print(f"\n\u2713 Patch 11 complete. New char count: {final_len}")
