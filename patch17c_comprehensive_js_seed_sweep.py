#!/usr/bin/env python3
"""
Patch 17C — Comprehensive JS seed-data sweep.

Scope (all in one pass):
  Block A  — Zero var tasks (24k-char Tasks module seed, 70 brand hits)
  Block B  — Zero var mockRows (brand-import preview, 24 hits) — function-scoped
  Block C  — Neutralize var contacts (per-event contact lookup, 3 hits) —
             function-scoped; keep 'default' entry only.
  Block D  — Strip 'available' fallback demo-SKU branch (5 hits).
  Block E  — Zero var bd (brand dashboard metrics, 3 hits).
  Block F  — Strip brand key from var labels report-axes object (3 hits).
  Block G  — renderVPDashboard surgical sweep (21 hits across 12 inline
             targets): 5 brand arrays, 1 vp-dq HTML block, 3 Zone-2 rows,
             1 Zone-3 row, 2 today's-event rows.

KEEP:
  - BRAND_TAXONOMY, BRAND_SETUP_FIELDS, PACKAGE_TAXONOMY, SUBCATEGORY_ID_MAP,
    FIELD_HELP_DEFAULTS (taxonomy/config — not seed).
  - ROLE_PROFILES (demo personas for role-switcher).
  - var bMap (brand-ID -> name mapping, no visible filter uses it).
  - JS code-branch fallbacks (D.brand = ev.brand || 'BACARDI Rum') —
    inert when user data present.
  - Doc comments mentioning brand names.
  - bacrm/bacrtd/patron in TARGET_IDS and brand-prefix routing code.

Baseline : 3,456,865  (post-Patch 17B, commit 4f07a94)
"""
import os, re, sys

TARGET    = 'FyldHub_MVP_Prototype.html'
FORBIDDEN = 'FyldHub_Combined_Prototype.html'

if not os.path.exists(TARGET):
    print(f'ERROR: {TARGET} not found'); sys.exit(1)
if os.path.abspath(TARGET) == os.path.abspath(FORBIDDEN):
    print('ERROR: would overwrite enterprise prototype'); sys.exit(1)

content = open(TARGET).read()
BASELINE = 3_456_865
if len(content) != BASELINE:
    print(f'ERROR: baseline mismatch. Expected {BASELINE:,}, got {len(content):,}'); sys.exit(1)

# ---------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------
def extract_decl(buf, name, open_ch, expected_count=1):
    """Walk balanced brackets with string-aware parsing.
       Returns (start, end, bytes) or None on mismatch."""
    close_ch = ']' if open_ch == '[' else '}'
    pat = re.compile(rf'\bvar\s+{re.escape(name)}\s*=\s*')
    matches = list(pat.finditer(buf))
    if len(matches) != expected_count:
        print(f'  FAIL [var {name}] got {len(matches)} decls, expected {expected_count}'); return None
    m = matches[0]; i = m.end()
    while i < len(buf) and buf[i] in ' \t\n': i += 1
    if buf[i] != open_ch:
        print(f'  FAIL [var {name}] open char mismatch'); return None
    depth = 0; in_str = None; j = i
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
                    return (m.start(), end, buf[m.start():end])
        j += 1
    return None

def rep_decl(buf, name, open_ch, new_text, label):
    res = extract_decl(buf, name, open_ch)
    if res is None: return None
    start, end, old = res
    delta = len(new_text) - len(old)
    print(f'  OK   [{label}] old={len(old)} \u2192 new={len(new_text)} \u0394={delta:+}')
    return buf[:start] + new_text + buf[end:]

def rep(buf, old, new, label, expected_count=1):
    count = buf.count(old)
    if count != expected_count:
        print(f'  FAIL [{label}] count={count}, expected={expected_count}')
        return None
    print(f'  OK   [{label}] replaced {count} occurrence(s)  \u0394={(len(new)-len(old))*count:+}')
    return buf.replace(old, new)

# ===============================================================
# BLOCK A -- var tasks
# ===============================================================
print('\n\u2500\u2500 Block A: var tasks \u2500\u2500')
out = rep_decl(content, 'tasks', '[', 'var tasks = [];', 'var tasks')
if out is None: print('ABORT: Block A'); sys.exit(2)
content = out

# ===============================================================
# BLOCK B -- var mockRows (function-scoped)
# ===============================================================
print('\n\u2500\u2500 Block B: var mockRows \u2500\u2500')
out = rep_decl(content, 'mockRows', '[', 'var mockRows = [];', 'var mockRows')
if out is None: print('ABORT: Block B'); sys.exit(2)
content = out

# ===============================================================
# BLOCK C -- var contacts (function-scoped)
# ===============================================================
print('\n\u2500\u2500 Block C: var contacts \u2500\u2500')
CONTACTS_NEW = (
"var contacts = {\n"
"      'default':       {name:'', role:'', email:'', phone:''}\n"
"    };"
)
out = rep_decl(content, 'contacts', '{', CONTACTS_NEW, 'var contacts')
if out is None: print('ABORT: Block C'); sys.exit(2)
content = out

# ===============================================================
# BLOCK D -- 'available' fallback branch
# ===============================================================
print('\n\u2500\u2500 Block D: available fallback branch \u2500\u2500')
AVAIL_OLD = (
"if (available.length === 0) {\n"
"    available = [{id:'demo1',label:'BACARD\u00cd White Rum \\u00b7 Bottle'},"
"{id:'demo2',label:'BACARD\u00cd Gold Rum \\u00b7 Bottle'},"
"{id:'demo3',label:'BACARD\u00cd Dark Rum \\u00b7 Bottle'},"
"{id:'demo4',label:'BACARD\u00cd Spiced Rum \\u00b7 Bottle'},"
"{id:'demo5',label:'BACARD\u00cd Lim\u00f3n \\u00b7 Bottle'}];\n"
"  }"
)
AVAIL_NEW = "/* fallback stripped for MVP */"
out = rep(content, AVAIL_OLD, AVAIL_NEW, 'available fallback', expected_count=1)
if out is None: print('ABORT: Block D'); sys.exit(2)
content = out

# ===============================================================
# BLOCK E -- var bd (brand dashboard metrics)
# ===============================================================
print('\n\u2500\u2500 Block E: var bd \u2500\u2500')
out = rep_decl(content, 'bd', '{', 'var bd = {};', 'var bd')
if out is None: print('ABORT: Block E'); sys.exit(2)
content = out

# ===============================================================
# BLOCK F -- var labels report-axes object (strip brand key only)
# ===============================================================
print('\n\u2500\u2500 Block F: var labels brand axis \u2500\u2500')
LABELS_OLD = "brand:['BACARD\u00cd Rum','BACARD\u00cd RTD','PATR\u00d3N']"
LABELS_NEW = "brand:[]"
out = rep(content, LABELS_OLD, LABELS_NEW, 'labels.brand axis', expected_count=1)
if out is None: print('ABORT: Block F'); sys.exit(2)
content = out

# ===============================================================
# BLOCK G -- renderVPDashboard surgical sweep
# ===============================================================
print('\n\u2500\u2500 Block G: renderVPDashboard surgical sweep \u2500\u2500')

# G.1 -- ROI chain array
G1_OLD = "[['BACARDI Rum Off-Prem','$31.2K','462','#00767B','+12%','$48K'],['BACARDI RTD Summer','$3.2K','89','#1E4DB7','+7%','$11K'],['PATRON On-Prem Elite','$8.4K','124','#7C3AED','+15%','$24K']]"
out = rep(content, G1_OLD, "[]", 'G.1 ROI chain array', expected_count=1)
if out is None: print('ABORT: G.1'); sys.exit(2)
content = out

# G.2 -- Sell-through array
G2_OLD = "[['BACARDI Rum Off-Prem','80%','+12%','#00767B'],['PATRON On-Premise','71%','+15%','#7C3AED'],['BACARDI RTD Summer','25%','+7%','#1E4DB7']]"
out = rep(content, G2_OLD, "[]", 'G.2 sell-through array', expected_count=1)
if out is None: print('ABORT: G.2'); sys.exit(2)
content = out

# G.3 -- Spend array
G3_OLD = "[['BACARDI Rum Off-Prem','$31.2K / $40K','78%','#00767B','On Track'],['PATRON On-Prem','$8.4K / $12K','70%','#7C3AED','On Track'],['BACARDI RTD Summer','$3.2K / $12K','27%','#E5484D','Behind Pace']]"
out = rep(content, G3_OLD, "[]", 'G.3 spend array', expected_count=1)
if out is None: print('ABORT: G.3'); sys.exit(2)
content = out

# G.4 -- Chain performance array
G4_OLD = "[['BACARDI Rum Off-Prem','#00767B','8 Act','3 Audits','1 Kit','+12%'],['PATRON On-Prem','#7C3AED','4 Act','0 Audits','2 Kits','+15%'],['BACARDI RTD','#1E4DB7','1 Act','0 Audits','0 Kits','+7%']]"
out = rep(content, G4_OLD, "[]", 'G.4 chain performance array', expected_count=1)
if out is None: print('ABORT: G.4'); sys.exit(2)
content = out

# G.5 -- Insights array
G5_OLD = "[['#E5484D','Tampa below threshold 2 weeks running','Recommend staffing review'],['#F59E0B','BACARDI RTD at risk of missing Q2 target','$2.1K on $12K budget'],['#16A34A','PATRON lift +15% \u2014 strongest this quarter','Expand On-Premise coverage']]"
out = rep(content, G5_OLD, "[]", 'G.5 insights array', expected_count=1)
if out is None: print('ABORT: G.5'); sys.exit(2)
content = out

# G.6 -- vp-dq-list HTML assembly
VPDQ_ITEM_1 = "h+='<div class=\"vp-dq-item\" onclick=\"switchModule(\\'settings\\');setTimeout(function(){showTab(\\'financials\\')},150)\"\"><div class=\"vp-dq-dot urg\"></div><div><div class=\"vp-dq-txt\">BACARDI RTD &mdash; Budget supplemental</div><div class=\"vp-dq-sub\">$8K needed by Apr 15</div></div>'+bdg('URGENT','#FEE2E2','#991B1B')+'</div>';\n  "
out = rep(content, VPDQ_ITEM_1, '', 'G.6a vp-dq BACARDI RTD item', expected_count=1)
if out is None: print('ABORT: G.6a'); sys.exit(2)
content = out

VPDQ_HDR_OLD = "&#9889; Decisions Required Today &middot; 3 items &middot; 2 urgent"
VPDQ_HDR_NEW = "&#9889; Decisions Required Today"
out = rep(content, VPDQ_HDR_OLD, VPDQ_HDR_NEW, 'G.6b vp-dq header counts', expected_count=1)
if out is None: print('ABORT: G.6b'); sys.exit(2)
content = out

# G.7 -- Zone 2 Activation Risk rows
G7_CALLS = [
    ("ar+=row('BACARDI RTD Summer Push','25% complete &middot; 14 days behind',bdg('Behind','#FEE2E2','#991B1B'));",
     "G.7a Zone2 BACARDI RTD row"),
    ("ar+=row('BACARDI Rum Off-Prem','80% complete &middot; 2 need staffing',bdg('At Risk','#FEF3C7','#92400E'));",
     "G.7b Zone2 BACARDI Rum row"),
    ("ar+=row('PATRON On-Prem Elite','71% complete &middot; on track',bdg('On Track','#D1FAE5','#065F46'));",
     "G.7c Zone2 PATRON row"),
]
for old, lbl in G7_CALLS:
    out = rep(content, old, '', lbl, expected_count=1)
    if out is None: print(f'ABORT: {lbl}'); sys.exit(2)
    content = out

# G.8 -- Zone 3 Governance BACARDI RTD row
p = content.find("pa+=row('BACARDI RTD &mdash; Budget Supplemental'")
if p < 0:
    print('  FAIL [G.8] pa+=row BACARDI not found'); sys.exit(2)
arg_start = content.find('(', p + len("pa+=row"))
i = arg_start + 1
depth = 1; in_str = None
while i < len(content) and depth > 0:
    c = content[i]
    if in_str:
        if c == '\\': i += 2; continue
        if c == in_str: in_str = None
        i += 1; continue
    if c in ('"', "'"): in_str = c; i += 1; continue
    if c == '(': depth += 1
    elif c == ')': depth -= 1
    i += 1
if content[i] == ';': i += 1
G8_FULL_OLD = content[p:i]
out = rep(content, G8_FULL_OLD, '', 'G.8 Zone3 Governance BACARDI RTD row', expected_count=1)
if out is None: print('ABORT: G.8'); sys.exit(2)
content = out

# G.9 -- Today's events branded rows
G9_CALLS = [
    ("te+=row('Total Wine #1205 &mdash; Boston','2:00-6:00 PM &middot; BACARDI Rum',bdg('Live Now','#DCFCE7','#166534'));",
     "G.9a today-events BACARDI Rum"),
    ("te+=row('BevMo! #312 &mdash; Providence','Apr 5 &middot; PATRON &middot; Confirmed',bdg('3 days','#E0F5F3','#00767B'));",
     "G.9b today-events PATRON"),
]
for old, lbl in G9_CALLS:
    out = rep(content, old, '', lbl, expected_count=1)
    if out is None: print(f'ABORT: {lbl}'); sys.exit(2)
    content = out

# ===============================================================
# BLOCK H -- Residual JS seed cleanup
# ===============================================================
print('\n\u2500\u2500 Block H: residual JS seed cleanup \u2500\u2500')

# H.1 -- "+ Add Another Brand" button default
out = rep(content,
          "onclick=\"D.multiBrand.push({brand:\\'BACARD\u00cd Rum\\',products:[]});",
          "onclick=\"D.multiBrand.push({brand:\\'\\',products:[]});",
          'H.1 Add Another Brand button default',
          expected_count=1)
if out is None: print('ABORT: H.1'); sys.exit(2)
content = out

# H.2a -- Asset option block 1
out = rep(content,
          '<option>BACARD\u00cd Branded Table Cover</option><option>BACARD\u00cd Branded Ice Bucket</option><option>2oz Sample Cups</option>',
          '<option>2oz Sample Cups</option>',
          'H.2a asset options block 1',
          expected_count=1)
if out is None: print('ABORT: H.2a'); sys.exit(2)
content = out

# H.2b -- Asset option block 2
out = rep(content,
          '<option>BACARD\u00cd Branded Table Cover</option><option>BACARD\u00cd Branded Ice Bucket</option><option>PATR\u00d3N Branded Bar Mat</option>',
          '',
          'H.2b asset options block 2',
          expected_count=1)
if out is None: print('ABORT: H.2b'); sys.exit(2)
content = out

# H.3 -- var brand fallback
out = rep(content,
          "var brand = APP_DATA.brands.length ? APP_DATA.brands[0].name : 'BACARD\u00cd Rum';",
          "var brand = APP_DATA.brands.length ? APP_DATA.brands[0].name : '';",
          'H.3 var brand fallback',
          expected_count=1)
if out is None: print('ABORT: H.3'); sys.exit(2)
content = out

# H.4 -- _userData brand fields
out = rep(content,
          "brand:'BACARD\u00cd Rum, PATR\u00d3N',",
          "brand:'All Brands',",
          'H.4a jordan brand field',
          expected_count=1)
if out is None: print('ABORT: H.4a'); sys.exit(2)
content = out

out = rep(content,
          "brand:'BACARD\u00cd Rum', loc:'West Coast',",
          "brand:'All Brands', loc:'West Coast',",
          'H.4b dana brand field',
          expected_count=1)
if out is None: print('ABORT: H.4b'); sys.exit(2)
content = out

# H.5 -- Executive Summary header
out = rep(content,
          'Bacardi USA \\u00b7 Enterprise \\u00b7 March 2026',
          'Your Company \\u00b7 Enterprise \\u00b7 March 2026',
          'H.5 exec summary header',
          expected_count=1)
if out is None: print('ABORT: H.5'); sys.exit(2)
content = out

# H.6 -- Key Risks widget
out = rep(content,
          '<div class="vp-row"><div><div class="vp-rt">BACARDI RTD \u2014 Behind Pace</div><div class="vp-rs">25% complete &middot; Q2 at risk</div></div>',
          '<div class="vp-row" style="display:none"><div><div class="vp-rt"></div><div class="vp-rs"></div></div>',
          'H.6 key risks row',
          expected_count=1)
if out is None: print('ABORT: H.6'); sys.exit(2)
content = out

# H.7 -- Report footer
out = rep(content,
          '<div>Bacardi USA \\u00b7 Enterprise</div>',
          '<div>Your Company \\u00b7 Enterprise</div>',
          'H.7 report footer',
          expected_count=1)
if out is None: print('ABORT: H.7'); sys.exit(2)
content = out

# H.8 -- Chart dataset label
out = rep(content,
          "label:'Bacardi USA',data:[87,42,94]",
          "label:'Your Company',data:[0,0,0]",
          'H.8 chart dataset',
          expected_count=1)
if out is None: print('ABORT: H.8'); sys.exit(2)
content = out

# H.9 -- @bacardi.com emails
bacardi_email_count = content.count('[at] bacardi.com')
if bacardi_email_count:
    content = content.replace('[at] bacardi.com', '[at] example.com')
    print(f'  OK   [H.9 @bacardi.com emails] replaced {bacardi_email_count} occurrence(s)')

# H.10 -- Brand-import preview fake-renderer
H10_OLD = """rows.innerHTML = [
      ['BACARD\u00cd Rum', 'Spirits', 'Rum'],
      ['Grey Goose', 'Spirits', 'Vodka'],
      ['Bombay Sapphire', 'Spirits', 'Gin']
    ].map(function(r) {"""
H10_NEW = """rows.innerHTML = [].map(function(r) {"""
out = rep(content, H10_OLD, H10_NEW, 'H.10 brand-import preview seed', expected_count=1)
if out is None: print('ABORT: H.10'); sys.exit(2)
content = out

# H.11 -- "3 brands imported successfully" toast
out = rep(content,
          "toast('3 brands imported successfully.');",
          "toast('Brands imported.');",
          'H.11 brand import toast',
          expected_count=1)
if out is None: print('  SKIP [H.11]  not found')
else: content = out

# ===============================================================
# Final verification
# ===============================================================
print('\n\u2500\u2500 Final verification \u2500\u2500')
script_blocks = [(m.start(), m.end()) for m in re.finditer(r'<script[^>]*>.*?</script>', content, re.DOTALL)]
in_script = lambda i: any(s <= i < e for s,e in script_blocks)
all_hits   = sum(1 for m in re.finditer(r'(BACARD\u00cd|PATR\u00d3N|Bacard\u00ed|Patr\u00f3n|BACARDI|PATRON|Bacardi)', content))
html_hits  = sum(1 for m in re.finditer(r'(BACARD\u00cd|PATR\u00d3N|Bacard\u00ed|Patr\u00f3n|BACARDI|PATRON|Bacardi)', content) if not in_script(m.start()))
print(f'  Total brand strings: {all_hits}')
print(f'  HTML-context hits:   {html_hits}')
print(f'  Script-context hits: {all_hits - html_hits}  (taxonomy + config + code-fallbacks)')

print(f'\nFinal size: {len(content):,}  (delta from baseline: {len(content)-BASELINE:+,})')

with open(TARGET, 'w') as f:
    f.write(content)
print(f'\u2705 Patch 17C applied.')
