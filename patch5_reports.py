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
BASELINE = 3830430
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

# ─── MVP REPORTS ────────────────────────────────────────────────
# In scope:   recap-rollup, worker-performance, worker-pay-summary, payment-ledger
# Out of scope (Phase 2): everything else

# ─── PATCH 5A: Replace static HTML reports sidebar ──────────────
# The static sidebar (rendered before JS takes over) shows all reports.
# Replace it with MVP-only static sidebar.
rep(
    '<div style="width:220px;flex-shrink:0;border-right:1px solid var(--border);background:var(--white);overflow-y:auto;padding:12px 0" id="rep-sidebar"><div style="font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.6px;color:var(--slate);padding:6px 16px 4px">Execution</div><div class="rep-report-item active" data-id="event-performance" onclick="selectReport(\'event-performance\')">Event Performance</div><div class="rep-report-item" data-id="worker-performance" onclick="selectReport(\'worker-performance\')">Worker Performance</div><div class="rep-report-item" data-id="sampling-activity" onclick="selectReport(\'sampling-activity\')">Sampling Activity</div><div style="font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.6px;color:var(--slate);padding:14px 16px 4px">Performance</div><div class="rep-report-item" data-id="channel-breakdown" onclick="selectReport(\'channel-breakdown\')">Channel Breakdown</div><div class="rep-report-item" data-id="program-summary" onclick="selectReport(\'program-summary\')">Program Summary</div><div style="font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.6px;color:var(--slate);padding:14px 16px 4px">Financial</div><div class="rep-report-item" data-id="budget-actual" onclick="selectReport(\'budget-actual\')">Budget vs. Actual</div><div class="rep-report-item" data-id="worker-pay-summary" onclick="selectReport(\'worker-pay-summary\')">Worker Pay Summary</div><div style="font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.6px;color:var(--slate);padding:14px 16px 4px">Compliance</div><div class="rep-report-item" data-id="compliance-proof" onclick="selectReport(\'compliance-proof\')">Compliance &amp; Proof</div><div style="font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.6px;color:var(--slate);padding:14px 16px 4px">Recap</div><div class="rep-report-item" data-id="recap-rollup" onclick="selectReport(\'recap-rollup\')">Recap Roll-Up</div></div>',
    '<div style="width:220px;flex-shrink:0;border-right:1px solid var(--border);background:var(--white);overflow-y:auto;padding:12px 0" id="rep-sidebar"><div style="font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.6px;color:var(--slate);padding:6px 16px 4px">Execution</div><div class="rep-report-item" data-id="worker-performance" onclick="selectReport(\'worker-performance\')">Worker Performance</div><div style="font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.6px;color:var(--slate);padding:14px 16px 4px">Financial</div><div class="rep-report-item" data-id="worker-pay-summary" onclick="selectReport(\'worker-pay-summary\')">Worker Pay Summary</div><div class="rep-report-item" data-id="payment-ledger" onclick="selectReport(\'payment-ledger\')">Worker Payment Ledger</div><div style="font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.6px;color:var(--slate);padding:14px 16px 4px">Recap</div><div class="rep-report-item active" data-id="recap-rollup" onclick="selectReport(\'recap-rollup\')">Recap Roll-Up</div><div style="font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.6px;color:var(--slate);padding:14px 16px 4px">Phase 2</div><div class="rep-report-item" style="opacity:.4;cursor:not-allowed;pointer-events:none;font-size:12px">Event Performance</div><div class="rep-report-item" style="opacity:.4;cursor:not-allowed;pointer-events:none;font-size:12px">Sampling Activity</div><div class="rep-report-item" style="opacity:.4;cursor:not-allowed;pointer-events:none;font-size:12px">Channel Breakdown</div><div class="rep-report-item" style="opacity:.4;cursor:not-allowed;pointer-events:none;font-size:12px">Program Summary</div><div class="rep-report-item" style="opacity:.4;cursor:not-allowed;pointer-events:none;font-size:12px">Budget vs. Actual</div><div class="rep-report-item" style="opacity:.4;cursor:not-allowed;pointer-events:none;font-size:12px">Compliance &amp; Proof</div><div class="rep-report-item" style="opacity:.4;cursor:not-allowed;pointer-events:none;font-size:12px">FyldCard Reconciliation</div><div class="rep-report-item" style="opacity:.4;cursor:not-allowed;pointer-events:none;font-size:12px">Expense Audit</div><div class="rep-report-item" style="opacity:.4;cursor:not-allowed;pointer-events:none;font-size:12px">Cost Per Activation</div></div>',
    "Reports sidebar: MVP reports only + Phase 2 section"
)

# ─── PATCH 5B: Update REP_SIDEBAR JS data to MVP reports only ───
# REP_SIDEBAR drives the dynamic sidebar render via renderReportSidebar()
# Replace the full REP_SIDEBAR definition with MVP-scoped version
rep(
    "var REP_SIDEBAR=[",
    "var REP_SIDEBAR_ENTERPRISE=[",
    "Rename enterprise REP_SIDEBAR"
)

# Inject MVP REP_SIDEBAR after the renamed enterprise one
rep(
    "var REP_SIDEBAR_ENTERPRISE=[",
    """var REP_SIDEBAR=[
  {cat:'Execution',items:[{id:'worker-performance',label:'Worker Performance',roles:['vp','pm','ops','logistics','finance']}]},
  {cat:'Financial',items:[{id:'worker-pay-summary',label:'Worker Pay Summary',roles:['vp','finance']},{id:'payment-ledger',label:'Worker Payment Ledger',roles:['vp','finance']}]},
  {cat:'Recap',items:[{id:'recap-rollup',label:'Recap Roll-Up',roles:['vp','pm']}]},
];
var REP_SIDEBAR_ENTERPRISE=[""",
    "Inject MVP REP_SIDEBAR before enterprise version"
)

# ─── WRITE OUTPUT ───────────────────────────────────────────────
open(TARGET, "w", encoding="utf-8").write(content)
final_len = len(open(TARGET, "r", encoding="utf-8").read())
print(f"\n✓ Patch 5 complete. New char count: {final_len}")
print("  Run: node --check FyldHub_MVP_Prototype.html")
