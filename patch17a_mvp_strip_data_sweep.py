#!/usr/bin/env python3
"""
Patch 17A — Full MVP-strip seed-data sweep (JS data layer).

Scope:
  1. Zero 26 JS data structures (full-declaration replacement).
  2. Special-shape zeros for RES_DATA / BILLING_SEED / MONTHLY_STATS
     (preserve top-level keys used downstream).
  3. D.brand: 'BACARDÍ Rum' → '' in both initial decl and resetD().
  4. UI fix: '+ Add Pool' button onclick openCreateBudget('bacrtd') → openCreateBudget().

NOT in scope (see Patch 17B):
  - Static HTML brand references (Dashboard widgets, Tasks filters, Programs module).
    183 occurrences inventoried.

Baseline : 3,582,026  (post-Patch 16, commit ba6efff)
Expected : 3,559,344  (delta -22,682)
"""
import os, re, sys

TARGET    = 'FyldHub_MVP_Prototype.html'
FORBIDDEN = 'FyldHub_Combined_Prototype.html'

# ── Safety guard ──────────────────────────────────────────────────
if not os.path.exists(TARGET):
    print(f'ERROR: {TARGET} not found in cwd'); sys.exit(1)
if os.path.abspath(TARGET) == os.path.abspath(FORBIDDEN):
    print('ERROR: target equals forbidden file'); sys.exit(1)

content = open(TARGET).read()
BASELINE = 3_582_026
if len(content) != BASELINE:
    print(f'ERROR: baseline mismatch. Expected {BASELINE:,}, got {len(content):,}'); sys.exit(1)

# ── Helper: extract a `var NAME = [...];` or `var NAME = {...};` ──
def extract_decl(buf, name, open_ch):
    close_ch = ']' if open_ch == '[' else '}'
    pat = re.compile(rf'\bvar\s+{re.escape(name)}\s*=\s*')
    matches = list(pat.finditer(buf))
    if len(matches) != 1:
        return None, f'expected 1 decl, got {len(matches)}'
    m = matches[0]
    i = m.end()
    while i < len(buf) and buf[i] in ' \t\n': i += 1
    if i >= len(buf) or buf[i] != open_ch:
        return None, f'open char {open_ch!r} not found at decl'
    depth = 0
    in_str = None
    j = i
    while j < len(buf):
        c = buf[j]
        if in_str:
            if c == '\\': j += 2; continue
            if c == in_str: in_str = None
        else:
            if c in ('"', "'"): in_str = c
            elif c == open_ch: depth += 1
            elif c == close_ch:
                depth -= 1
                if depth == 0:
                    end = j + 1
                    if end < len(buf) and buf[end] == ';': end += 1
                    return (m.start(), end, buf[m.start():end]), None
        j += 1
    return None, 'unterminated'

# ── Helper: surgical unique-string replace ────────────────────────
def rep(buf, old, new, label, expected_count=1):
    count = buf.count(old)
    if count != expected_count:
        print(f'  FAIL [{label}] count={count}, expected={expected_count}')
        return None
    print(f'  OK   [{label}] -> replaced {count} occurrence(s)')
    return buf.replace(old, new)

# ── Helper: full-decl replacement ─────────────────────────────────
def rep_decl(buf, name, open_ch, new_text, label):
    res, err = extract_decl(buf, name, open_ch)
    if res is None:
        print(f'  FAIL [{label}] {err}')
        return None
    start, end, old = res
    new_buf = buf[:start] + new_text + buf[end:]
    print(f'  OK   [{label}] old_len={len(old)} new_len={len(new_text)} delta={len(new_text)-len(old):+}')
    return new_buf

# ═════════════════════════════════════════════════════════════════
# BLOCK A — 26 simple data-structure zero-outs
# ═════════════════════════════════════════════════════════════════
print('\n\u2500\u2500 Block A: Zero 26 data structures \u2500\u2500')

SIMPLE_TARGETS = [
    # Logistics / Operations seeds
    ('KIT_INVENTORY',        '[', 'var KIT_INVENTORY=[];'),
    ('KITS_TO_SHIP',         '[', 'var KITS_TO_SHIP=[];'),
    ('DELIVERIES',           '[', 'var DELIVERIES=[];'),
    ('ASSET_INVENTORY',      '[', 'var ASSET_INVENTORY=[];'),
    ('WEATHER_MARKETS',      '[', 'var WEATHER_MARKETS=[];'),
    ('LOGISTICS_EXCEPTIONS', '[', 'var LOGISTICS_EXCEPTIONS=[];'),
    ('RUNNER_ACTIVITY_SEED', '[', 'var RUNNER_ACTIVITY_SEED=[];'),
    ('EXP_AUDIT_SEED',       '[', 'var EXP_AUDIT_SEED=[];'),
    ('CITY_MARKET',          '{', 'var CITY_MARKET={};'),
    # Worker / People seeds
    ('WK',                   '[', 'var WK=[];'),
    ('WORKER_DATA',          '{', 'var WORKER_DATA={};'),
    ('WORKER_PROFILE_SEED',  '{', 'var WORKER_PROFILE_SEED={};'),
    # Brand / Catalog seeds
    ('BRAND_PRODUCTS',       '{', 'var BRAND_PRODUCTS={};'),
    ('BK_RES',               '[', 'var BK_RES=[];'),
    ('RECS',                 '[', 'var RECS=[];'),
    ('TPLS',                 '{', 'var TPLS={};'),
    ('BRANDS',               '[', 'var BRANDS=[];'),
    # Outside Partner Costs
    ('OPC_PARTNERS',         '[', 'var OPC_PARTNERS=[];'),
    ('OPC_CATEGORIES',       '[', 'var OPC_CATEGORIES=[];'),
    ('OPC_ENTRIES',          '[', 'var OPC_ENTRIES=[];'),
    # Event Categories
    ('ET',                   '{', 'var ET={};'),
    # Financial seeds
    ('FIN_BUDGETS',          '{', 'var FIN_BUDGETS={};'),
    ('PROG_BUDGETS',         '{', 'var PROG_BUDGETS={};'),
    ('FC_TXNS',              '[', 'var FC_TXNS=[];'),
    ('EV_RCP_DATA',          '{', 'var EV_RCP_DATA={};'),
    # Reports — enterprise list only
    ('REP_SIDEBAR_ENTERPRISE','[', 'var REP_SIDEBAR_ENTERPRISE=[];'),
]

for name, open_ch, new_text in SIMPLE_TARGETS:
    out = rep_decl(content, name, open_ch, new_text, name)
    if out is None: print(f'\nABORT: Block A failed on {name}'); sys.exit(2)
    content = out

# ═════════════════════════════════════════════════════════════════
# BLOCK B — Special shape-preserving replacements
# ═════════════════════════════════════════════════════════════════
print('\n\u2500\u2500 Block B: Shape-preserving replacements \u2500\u2500')

# RES_DATA: preserve Kit/Digital/Physical keys (consumers iterate RES_DATA[type])
RES_DATA_NEW = "var RES_DATA = {\n  'Kit': [],\n  'Digital': [],\n  'Physical': []\n};"
out = rep_decl(content, 'RES_DATA', '{', RES_DATA_NEW, 'RES_DATA')
if out is None: print('ABORT: RES_DATA'); sys.exit(2)
content = out

# BILLING_SEED: preserve account/invoices shape, neutralize values
BILLING_SEED_NEW = (
"var BILLING_SEED = {\n"
"  account: {\n"
"    name: '', tier: '', billing: 'Monthly',\n"
"    since: '', next: '',\n"
"    hubs: []\n"
"  },\n"
"  invoices: []\n"
"};"
)
out = rep_decl(content, 'BILLING_SEED', '{', BILLING_SEED_NEW, 'BILLING_SEED')
if out is None: print('ABORT: BILLING_SEED'); sys.exit(2)
content = out

# MONTHLY_STATS: zero counts, preserve keys
MONTHLY_STATS_NEW = (
"var MONTHLY_STATS = {\n"
"  eventsTotal: 0, completionRate: '0%', consumerInteractions: 0,\n"
"  samplesDistributed: 0, avgExecScore: '0%', totalSpend: '$0'\n"
"};"
)
out = rep_decl(content, 'MONTHLY_STATS', '{', MONTHLY_STATS_NEW, 'MONTHLY_STATS')
if out is None: print('ABORT: MONTHLY_STATS'); sys.exit(2)
content = out

# ═════════════════════════════════════════════════════════════════
# BLOCK C — Surgical string replacements
# ═════════════════════════════════════════════════════════════════
print('\n\u2500\u2500 Block C: Surgical strings \u2500\u2500')

# D.brand → empty in both initial decl AND resetD() body
# Both occurrences are byte-identical and must stay in sync.
D_BRAND_OLD = "prog:'',brand:'BACARD\u00cd Rum',products:[]"
D_BRAND_NEW = "prog:'',brand:'',products:[]"
out = rep(content, D_BRAND_OLD, D_BRAND_NEW, "D.brand BACARD\u00cd\u2192empty (2x)", expected_count=2)
if out is None: print('ABORT: D.brand'); sys.exit(2)
content = out

# ═════════════════════════════════════════════════════════════════
# BLOCK D — UI handler fix
# ═════════════════════════════════════════════════════════════════
print('\n\u2500\u2500 Block D: UI handler fix \u2500\u2500')

POOL_BTN_OLD = 'onclick="openCreateBudget(&#39;bacrtd&#39;)"'
POOL_BTN_NEW = 'onclick="openCreateBudget()"'
out = rep(content, POOL_BTN_OLD, POOL_BTN_NEW, "+ Add Pool bacrtd \u2192 generic", expected_count=1)
if out is None: print('ABORT: + Add Pool handler'); sys.exit(2)
content = out

# ═════════════════════════════════════════════════════════════════
# Final verification
# ═════════════════════════════════════════════════════════════════
EXPECTED = 3_559_344
if len(content) != EXPECTED:
    print(f'\nERROR: final size mismatch. Expected {EXPECTED:,}, got {len(content):,}')
    sys.exit(1)

with open(TARGET, 'w') as f:
    f.write(content)

print(f'\n\u2705 Patch 17A applied. {BASELINE:,} \u2192 {len(content):,} ({len(content)-BASELINE:+,} chars)')
