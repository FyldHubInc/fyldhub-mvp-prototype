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
BASELINE = 3830129
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

# ─── PATCH 4: Hub selector in event wizard ──────────────────────
# The hub selector renders Activations, Merchandising, On-Demand
# via a JS array: ['Activations','Merchandising','On-Demand']
# We replace the array to inject Phase 2 labels and disable non-MVP hubs

rep(
    "['Activations','Merchandising','On-Demand'].map(function(h){return '<div class=\"ocd '+(D.hub===h?'sel':'')+'\" onclick=\"if(D.hub&&D.hub!==\\''+h+'\\'){D.blocks=[];D.loc=null;D.workersNeeded=2;}D.hub=\\''+h+'\\';D.type=\\'\\';rS1(el(\\'wizBody\\'))\" style=\"flex:1\"><div class=\"ci\">'+hsvg[h]+'</div><div class=\"ct\">'+h+'</div></div>'}).join('')",
    "['Activations','Merchandising','On-Demand'].map(function(h){var isP2=h!=='Activations';return '<div class=\"ocd '+(D.hub===h&&!isP2?'sel':'')+(isP2?' p2-hub-opt':'')+'\" onclick=\"'+(isP2?'void(0)':'if(D.hub&&D.hub!==\\''+h+'\\'){D.blocks=[];D.loc=null;D.workersNeeded=2;}D.hub=\\''+h+'\\';D.type=\\'\\';rS1(el(\\'wizBody\\'))')+'\" style=\"flex:1'+(isP2?';opacity:.45;cursor:not-allowed;pointer-events:none;position:relative':'')+'\"><div class=\"ci\">'+hsvg[h]+'</div><div class=\"ct\">'+h+(isP2?'<span style=\"display:block;font-size:9px;font-weight:700;color:#F59E0B;letter-spacing:.4px;margin-top:2px\">PHASE 2</span>':'')+'</div></div>';}).join('')",
    "Event wizard: lock Merchandising + On-Demand as Phase 2"
)

# ─── WRITE OUTPUT ───────────────────────────────────────────────
open(TARGET, "w", encoding="utf-8").write(content)
final_len = len(open(TARGET, "r", encoding="utf-8").read())
print(f"\n✓ Patch 4 complete. New char count: {final_len}")
print("  Run: node --check FyldHub_MVP_Prototype.html")
