#!/usr/bin/env python3
"""Patch 16 — Consolidated MVP-strip seed-data sweep.

Scope (A1–A9):
  A1   Users badge 5 → 0
  A2   Roles badge 9 → 13 (matches actual schema count)
  A2b  Outside Partners badge 3 → 0
  A3   Hub Access legend: ME + OD get opacity + PHASE 2 chips
  A4   Outside Partners: 3 partner cards → empty state
  A5   13 role cards: all user counts → "0 users"
  A6   Org Hierarchy BACARDÍ tree → empty state
  A7   Brand Resources: stray "All Brands / 24oz / 1 kit" asset → removed
  A8   69 brand-specific <option>s (BACARDÍ / PATRÓN) → removed
  A9   Worker Pay: Activations Hub grid → stub; orphan Kit&Asset + Festival → removed

Baseline:  3,648,254 (post-Patch-15)
Expected:  3,582,026
"""
import os
import re
import sys

TARGET    = 'FyldHub_MVP_Prototype.html'
FORBIDDEN = 'FyldHub_Combined_Prototype.html'

if not os.path.exists(TARGET):
    print(f'ERROR: {TARGET} not found'); sys.exit(1)
if os.path.abspath(TARGET) == os.path.abspath(FORBIDDEN):
    print('ERROR: would overwrite enterprise prototype'); sys.exit(1)

content = open(TARGET).read()

BASELINE = 3_648_254
if len(content) != BASELINE:
    print(f'ERROR: baseline mismatch. Expected {BASELINE:,}, got {len(content):,}')
    sys.exit(1)

def rep(old, new, label):
    """Assert-once replace helper."""
    global content
    count = content.count(old)
    if count != 1:
        print(f'ERROR [{label}]: anchor not unique ({count} occurrences)')
        sys.exit(1)
    before = len(content)
    content = content.replace(old, new, 1)
    delta = len(content) - before
    print(f'  \u2705 {label:38s} \u0394={delta:+,}')

print(f'Starting: {len(content):,} chars')

# \u2500\u2500\u2500 A1: Users badge 5 \u2192 0 \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
rep(
    'onclick="showUmgmt(&#39;users&#39;)">Users <span style="font-size:12px;background:var(--teal);color:#fff;border-radius:10px;padding:1px 7px;margin-left:4px">5</span>',
    'onclick="showUmgmt(&#39;users&#39;)">Users <span style="font-size:12px;background:var(--slate);color:#fff;border-radius:10px;padding:1px 7px;margin-left:4px">0</span>',
    'A1 Users badge 5\u21920'
)

# \u2500\u2500\u2500 A2: Roles badge 9 \u2192 13 \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
rep(
    'onclick="showUmgmt(&#39;roles&#39;)">Roles <span style="font-size:12px;background:var(--slate);color:#fff;border-radius:10px;padding:1px 7px;margin-left:4px">9</span>',
    'onclick="showUmgmt(&#39;roles&#39;)">Roles <span style="font-size:12px;background:var(--slate);color:#fff;border-radius:10px;padding:1px 7px;margin-left:4px">13</span>',
    'A2 Roles badge 9\u219213'
)

# \u2500\u2500\u2500 A2b: Outside Partners badge 3 \u2192 0 \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
rep(
    'onclick="showUmgmt(&#39;partners-um&#39;)">Outside Partners <span style="font-size:12px;background:var(--slate);color:#fff;border-radius:10px;padding:1px 7px;margin-left:4px">3</span>',
    'onclick="showUmgmt(&#39;partners-um&#39;)">Outside Partners <span style="font-size:12px;background:var(--slate);color:#fff;border-radius:10px;padding:1px 7px;margin-left:4px">0</span>',
    'A2b Outside Partners badge 3\u21920'
)

# \u2500\u2500\u2500 A3: Hub Access legend ME + OD \u2192 Phase 2 badged \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
rep(
    '<span style="font-weight:700;color:#1E4DB7;background:#DBEAFE;padding:2px 7px;border-radius:4px">ME</span><span style="color:var(--slate)">Merchandising</span>\n      <span style="font-weight:700;color:#7C3AED;background:#EDE9FE;padding:2px 7px;border-radius:4px">OD</span><span style="color:var(--slate)">On-Demand Support</span>',
    '<span style="font-weight:700;color:#1E4DB7;background:#DBEAFE;padding:2px 7px;border-radius:4px;opacity:.5">ME</span><span style="color:var(--slate);opacity:.5">Merchandising</span>&nbsp;<span style="font-size:9px;font-weight:700;background:#F59E0B;color:#fff;padding:1px 4px;border-radius:3px;letter-spacing:.4px">PHASE 2</span>\n      <span style="font-weight:700;color:#7C3AED;background:#EDE9FE;padding:2px 7px;border-radius:4px;opacity:.5">OD</span><span style="color:var(--slate);opacity:.5">On-Demand Support</span>&nbsp;<span style="font-size:9px;font-weight:700;background:#F59E0B;color:#fff;padding:1px 4px;border-radius:3px;letter-spacing:.4px">PHASE 2</span>',
    'A3 Hub Access ME/OD Phase 2'
)

# \u2500\u2500\u2500 A4: Outside Partners 3 cards \u2192 empty state \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
A4_START = '<!-- Partner: Mosaic North America'
A4_END   = '<div style="margin-top:12px;padding:14px 16px;background:var(--teal-xl);border:1px solid var(--teal-l);border-radius:var(--radius);display:flex;align-items:flex-start;gap:10px">\n      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--teal)"'
assert content.count(A4_START) == 1, 'A4_START not unique'
assert content.count(A4_END)   == 1, 'A4_END not unique'
idx_s = content.find(A4_START)
idx_e = content.find(A4_END)
A4_EMPTY = '''<div class="card" style="padding:48px 24px;text-align:center;color:var(--slate);margin-bottom:16px">
      <div style="font-size:15px;font-weight:600;color:var(--dark);margin-bottom:6px">No outside partners yet</div>
      <div style="font-size:13px;margin-bottom:16px">Add agencies, distributors, retailers, 3PLs, and other external organizations with scoped access to your account.</div>
      <button class="btn btn-primary btn-sm" onclick="openAddPartner()">+ Add Outside Partner</button>
    </div>

    '''
before = len(content)
content = content[:idx_s] + A4_EMPTY + content[idx_e:]
label = "A4 Outside Partners \u2192 empty state"
print(f'  \u2705 {label:38s} \u0394={len(content)-before:+,}')

# \u2500\u2500\u2500 A5: 13 role cards: N users \u2192 0 users \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
pat_a5 = re.compile(r'(<div style="font-size:12px;color:var\(--slate\);white-space:nowrap;padding:0 16px">)(\d+)\s+users?(</div>)')
before = len(content)
match_count = len(pat_a5.findall(content))
content = pat_a5.sub(lambda m: f'{m.group(1)}0 users{m.group(3)}', content)
label = f"A5 Role user counts ({match_count} cards \u2192 0 users)"
print(f'  \u2705 {label:38s} \u0394={len(content)-before:+,}')

# \u2500\u2500\u2500 A6: Org Hierarchy BACARD\u00cd tree \u2192 empty state \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
A6_COMMENT = '<!-- Visual tree \u2014 default 5-tier with Bacard\u00ed sample data -->'
assert content.count(A6_COMMENT) == 1, 'A6_COMMENT not unique'
a6_pos = content.find(A6_COMMENT)
after_c = a6_pos + len(A6_COMMENT)
first_div_m = re.search(r'<div\b[^>]*>', content[after_c:])
tree_open_end = after_c + first_div_m.end()
depth = 1
tree_close = None
for m in re.finditer(r'<div\b[^>]*>|</div\s*>', content[tree_open_end:]):
    if m.group().startswith('</'):
        depth -= 1
        if depth == 0:
            tree_close = tree_open_end + m.end()
            break
    else:
        depth += 1
assert tree_close is not None, 'A6: tree wrapper never closes'
A6_EMPTY = '''<!-- MVP: empty state replaces seed BACARD\u00cd tree -->
      <div style="background:var(--white);border:1px solid var(--border);border-radius:var(--radius);padding:48px 24px;text-align:center;color:var(--slate)">
        <div style="font-size:15px;font-weight:600;color:var(--dark);margin-bottom:6px">No hierarchy configured yet</div>
        <div style="font-size:13px;margin-bottom:16px">Add your first tier node to build out your org tree. The tier labels above define visibility roll-up rules.</div>
        <button class="btn btn-primary btn-sm" onclick="toast(&#39;Add Node coming soon.&#39;)">+ Add First Node</button>
      </div>'''
before = len(content)
content = content[:a6_pos] + A6_EMPTY + content[tree_close:]
label = "A6 Org Hierarchy tree \u2192 empty state"
print(f'  \u2705 {label:38s} \u0394={len(content)-before:+,}')

# \u2500\u2500\u2500 A7: Brand Resources stray asset row \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
A7_START_KEEP = 'No physical assets added yet. Add assets to include them in kit templates.</div>\n'
A7_END_RESUME = '\n    <div class="ts tsl" style="font-size:12px;padding:4px 0 8px">\n      Assets feed into kit contents.'
assert content.count(A7_START_KEEP) == 1, 'A7_START_KEEP not unique'
assert content.count(A7_END_RESUME) == 1, 'A7_END_RESUME not unique'
idx_s = content.find(A7_START_KEEP) + len(A7_START_KEEP)
idx_e = content.find(A7_END_RESUME)
before = len(content)
content = content[:idx_s] + '    </div>\n' + content[idx_e:]
label = "A7 Brand Resources asset row"
print(f'  \u2705 {label:38s} \u0394={len(content)-before:+,}')

# \u2500\u2500\u2500 A8: 69 brand-specific <option> tags \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
pat_a8 = re.compile(r'\s*<option(?:\s+value="[^"]*")?\s*>(?:BACARD\u00cd Rum|BACARD\u00cd RTD|BACARD\u00cd Ready-to-Drink|PATR\u00d3N|BACARDI Rum|BACARDI RTD|PATRON|Bacardi)\s*</option>')
before = len(content)
removed = len(pat_a8.findall(content))
content = pat_a8.sub('', content)
label = f"A8 Brand options ({removed} removed)"
print(f'  \u2705 {label:38s} \u0394={len(content)-before:+,}')

# \u2500\u2500\u2500 A9 Part 1: Activations Hub grid \u2192 Phase 2 stub \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
A9P1_START = '<div class="hub-header hub-teal">\n    <span class="hub-dot" style="background:var(--teal)"></span>\n    <span class="hub-name" style="color:var(--teal)">Activations Hub</span>'
A9P1_END   = '<div style="margin-top:24px;padding:20px;border:1px dashed var(--border);border-radius:8px;text-align:center">\n    <div style="font-size:13px;font-weight:600;color:var(--dark);margin-bottom:4px">Merchandising Hub &amp; On-Demand Hub</div>'
assert content.count(A9P1_START) == 1, 'A9P1_START not unique'
assert content.count(A9P1_END)   == 1, 'A9P1_END not unique'
idx_s = content.find(A9P1_START)
idx_e = content.find(A9P1_END)
A9_STUB = '''<div style="margin-top:16px;padding:20px;border:1px dashed var(--border);border-radius:8px;text-align:center">
    <div style="font-size:13px;font-weight:600;color:var(--dark);margin-bottom:4px">Activations Hub</div>
    <div style="font-size:12px;color:var(--slate)">Per-event-type rate cards (Product Demo, Pop-Up, Street Team, Sponsorships) are configured per Event Category.</div>
    <span style="display:inline-block;margin-top:8px;font-size:9px;font-weight:700;background:#94A3B8;color:#fff;padding:2px 6px;border-radius:3px;letter-spacing:.4px">CONFIGURE IN EVENT CATEGORIES</span>
  </div>
  '''
before = len(content)
content = content[:idx_s] + A9_STUB + content[idx_e:]
label = "A9 Part 1 Activations Hub \u2192 stub"
print(f'  \u2705 {label:38s} \u0394={len(content)-before:+,}')

# \u2500\u2500\u2500 A9 Part 2: Orphan Kit & Asset + Festival excise \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
A9P2_START = '  <div class="cat-header"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9l6 6 6-6"></path></svg>Kit &amp; Asset Delivery</div>'
A9P2_END   = '  <div id="financials-vendor-costs"'
assert content.count(A9P2_START) == 1, 'A9P2_START not unique'
assert content.count(A9P2_END)   == 1, 'A9P2_END not unique'
idx_s = content.find(A9P2_START)
idx_e = content.find(A9P2_END)
before = len(content)
content = content[:idx_s] + content[idx_e:]
label = "A9 Part 2 Orphan Kit&Asset+Festival"
print(f'  \u2705 {label:38s} \u0394={len(content)-before:+,}')

# \u2500\u2500\u2500 Final verification \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
EXPECTED = 3_582_026
if len(content) != EXPECTED:
    print(f'\nERROR: final size mismatch. Expected {EXPECTED:,}, got {len(content):,}')
    sys.exit(1)

with open(TARGET, 'w') as f:
    f.write(content)

print(f'\n\u2705 Patch 16 applied. {BASELINE:,} \u2192 {len(content):,} ({len(content)-BASELINE:+,} chars)')
