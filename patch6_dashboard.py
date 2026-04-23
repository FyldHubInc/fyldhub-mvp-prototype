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
BASELINE = 3831226
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

# ─── PATCH 6A: Badge Program Performance dashboard widget ───────
# The widget container has id="dwidget-programs"
# Overlay it with a Phase 2 badge and disable interaction
rep(
    '<div id="dwidget-programs" class="dash-widget" data-widget-id="programs">',
    '<div id="dwidget-programs" class="dash-widget" data-widget-id="programs" style="position:relative;opacity:.5;pointer-events:none">',
    "Dashboard: disable Program Performance widget"
)

# Add Phase 2 badge inside the widget header
rep(
    '<div class="dw-title">Program Performance</div>',
    '<div class="dw-title">Program Performance <span style="font-size:9px;font-weight:700;letter-spacing:.4px;background:#F59E0B;color:#fff;padding:2px 5px;border-radius:3px;vertical-align:middle">PHASE 2</span></div>',
    "Dashboard: add Phase 2 badge to Program Performance widget title"
)

# ─── WRITE OUTPUT ───────────────────────────────────────────────
open(TARGET, "w", encoding="utf-8").write(content)
final_len = len(open(TARGET, "r", encoding="utf-8").read())
print(f"\n✓ Patch 6 complete. New char count: {final_len}")
print("  Run: node --check FyldHub_MVP_Prototype.html")
