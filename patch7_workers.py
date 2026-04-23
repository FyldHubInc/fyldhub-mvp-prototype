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

print(f"✓ Targeting: {TARGET}")

# ─── BASELINE CHECK ─────────────────────────────────────────────
content = open(TARGET, "r", encoding="utf-8").read()
BASELINE = 3831448
if len(content) != BASELINE:
    print(f"ERROR: Baseline mismatch. Expected {BASELINE}, got {len(content)}. Aborting.")
    sys.exit(1)
print(f"✓ Baseline confirmed: {len(content)} chars")

# ─── PATCH HELPER ───────────────────────────────────────────────
def rep(old, new, label):
    global content
    count = content.count(old)
    if count != 1:
        print(f"ERROR [{label}]: Expected 1 occurrence, found {count}. Aborting.")
        sys.exit(1)
    content = content.replace(old, new, 1)
    print(f"✓ Patched: {label}")

# ─── RECON: find worker type tab anchors ────────────────────────
# Check what the workers module tab switcher looks like
checkers_count = content.count('FyldCheckers')
runners_count  = content.count('FyldRunners')
print(f"  FyldCheckers occurrences: {checkers_count}")
print(f"  FyldRunners occurrences:  {runners_count}")

# ─── PATCH 7A: Disable FyldCheckers tab ─────────────────────────
rep(
    '<div class="hub-tab merch" id="htab-merch" onclick="switchHub(\'Merchandising\',this)">',
    '<div class="hub-tab merch" id="htab-merch" onclick="void(0)" style="opacity:.45;cursor:not-allowed;pointer-events:none;position:relative">',
    "Workers: disable FyldCheckers tab"
)

rep(
    '        FyldCheckers <span class="tab-ct" id="hct-merch">0</span>',
    '        FyldCheckers <span style="font-size:9px;font-weight:700;letter-spacing:.4px;background:#F59E0B;color:#fff;padding:2px 5px;border-radius:3px;vertical-align:middle">PHASE 2</span> <span class="tab-ct" id="hct-merch">0</span>',
    "Workers: badge FyldCheckers tab"
)

# ─── PATCH 7B: Disable FyldRunners tab ──────────────────────────
rep(
    '<div class="hub-tab od" id="htab-od" onclick="switchHub(\'On-Demand\',this)">',
    '<div class="hub-tab od" id="htab-od" onclick="void(0)" style="opacity:.45;cursor:not-allowed;pointer-events:none;position:relative">',
    "Workers: disable FyldRunners tab"
)

rep(
    '        FyldRunners <span class="tab-ct" id="hct-od">0</span>',
    '        FyldRunners <span style="font-size:9px;font-weight:700;letter-spacing:.4px;background:#F59E0B;color:#fff;padding:2px 5px;border-radius:3px;vertical-align:middle">PHASE 2</span> <span class="tab-ct" id="hct-od">0</span>',
    "Workers: badge FyldRunners tab"
)

# ─── WRITE OUTPUT ───────────────────────────────────────────────
open(TARGET, "w", encoding="utf-8").write(content)
final_len = len(open(TARGET, "r", encoding="utf-8").read())
print(f"\n✓ Patch 7 complete. New char count: {final_len}")
print("  Run: node --check FyldHub_MVP_Prototype.html")
