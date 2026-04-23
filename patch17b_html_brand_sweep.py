#!/usr/bin/env python3
"""
Patch 17B — Static HTML brand sweep (MVP skeleton).

Scope (all in one pass):
  Block A — Replace demo rows inside ~20 Dashboard widgets and module containers
            with empty-state markers. Uses a structural walker that finds each
            container's dw-body / tbody / inner area and swaps contents.
  Block B — Strip hardcoded BACARDI/PATRON <option> and checkbox-label entries
            from filter dropdowns (mflt-brand-panel, tk-filter-program).
  Block C — Programs module (psec-2/4/7, prog-*-sel, prog-*-pills, scope-market-sel)
            pre-populated wizard fields -> empty states.
  Block D — Page subtitles / headers: "Bacardi USA" -> "your company" / strip.
  Block E — Form input placeholders: strip branded e.g. text.
  Block F — Decorative HTML comments removed.
  Block G — ap-sec-4 / ap-rec-body permission-recap brand references neutralized.

Baseline : 3,559,344  (post-Patch 17A, commit e9b6834)
"""
import os, re, sys

TARGET    = 'FyldHub_MVP_Prototype.html'
FORBIDDEN = 'FyldHub_Combined_Prototype.html'

if not os.path.exists(TARGET):
    print(f'ERROR: {TARGET} not found in cwd'); sys.exit(1)
if os.path.abspath(TARGET) == os.path.abspath(FORBIDDEN):
    print('ERROR: target equals forbidden file'); sys.exit(1)

content = open(TARGET).read()
BASELINE = 3_559_344
if len(content) != BASELINE:
    print(f'ERROR: baseline mismatch. Expected {BASELINE:,}, got {len(content):,}'); sys.exit(1)

# ---------------------------------------------------------------
# Structural helpers
# ---------------------------------------------------------------
def find_container_span(buf, cid):
    """<tag id="cid">...</tag> -> (start, open_end, close_start, end) or None."""
    m = re.search(rf'<(\w+)[^>]*\bid="{re.escape(cid)}"[^>]*>', buf)
    if not m: return None
    tag = m.group(1); open_tag_end = m.end()
    depth = 1; i = open_tag_end
    open_pat  = re.compile(rf'<{tag}\b[^>]*>', re.IGNORECASE)
    close_pat = re.compile(rf'</{tag}\s*>', re.IGNORECASE)
    while i < len(buf) and depth > 0:
        om = open_pat.search(buf, i)
        cm = close_pat.search(buf, i)
        if not cm: return None
        if om and om.start() < cm.start():
            depth += 1; i = om.end()
        else:
            if depth == 1:
                return (m.start(), open_tag_end, cm.start(), cm.end())
            depth -= 1; i = cm.end()
    return None

def find_child_by_class(buf, start, end, class_name):
    """First <tag class="... class_name ..."> span inside [start, end]."""
    pat = re.compile(rf'<(\w+)[^>]*\bclass="[^"]*\b{re.escape(class_name)}\b[^"]*"[^>]*>')
    m = pat.search(buf, start, end)
    if not m: return None
    tag = m.group(1); open_tag_end = m.end()
    depth = 1; i = open_tag_end
    open_pat  = re.compile(rf'<{tag}\b[^>]*>', re.IGNORECASE)
    close_pat = re.compile(rf'</{tag}\s*>', re.IGNORECASE)
    while i < end and depth > 0:
        om = open_pat.search(buf, i, end)
        cm = close_pat.search(buf, i, end)
        if not cm: return None
        if om and om.start() < cm.start():
            depth += 1; i = om.end()
        else:
            if depth == 1:
                return (m.start(), open_tag_end, cm.start(), cm.end())
            depth -= 1; i = cm.end()
    return None

def find_tbody(buf, start, end):
    """First <tbody>...</tbody> span inside [start, end]."""
    m = re.search(r'<tbody[^>]*>', buf[start:end])
    if not m: return None
    t_start = start + m.start(); open_end = start + m.end()
    cm = re.search(r'</tbody\s*>', buf[open_end:end])
    if not cm: return None
    close_start = open_end + cm.start(); t_end = open_end + cm.end()
    return (t_start, open_end, close_start, t_end)

# Replacement helpers
def replace_inner_of_container(buf, cid, new_inner, label):
    """Replace inner contents of <tag id="cid">X</tag> with new_inner."""
    span = find_container_span(buf, cid)
    if not span:
        print(f'  FAIL [{label}] container id={cid} not found'); return None
    _, open_end, close_start, _ = span
    old_inner = buf[open_end:close_start]
    new_buf = buf[:open_end] + new_inner + buf[close_start:]
    delta = len(new_inner) - len(old_inner)
    print(f'  OK   [{label}] id={cid} old_inner={len(old_inner)} -> new_inner={len(new_inner)} d={delta:+}')
    return new_buf

def replace_dw_body(buf, cid, new_body_inner, label):
    """Replace inner of the .dw-body child inside widget id=cid."""
    span = find_container_span(buf, cid)
    if not span:
        print(f'  FAIL [{label}] container id={cid} not found'); return None
    _, open_end, close_start, _ = span
    body = find_child_by_class(buf, open_end, close_start, 'dw-body')
    if not body:
        print(f'  FAIL [{label}] .dw-body not found inside id={cid}'); return None
    _, b_open_end, b_close_start, _ = body
    old = buf[b_open_end:b_close_start]
    delta = len(new_body_inner) - len(old)
    print(f'  OK   [{label}] id={cid} .dw-body old={len(old)} -> new={len(new_body_inner)} d={delta:+}')
    return buf[:b_open_end] + new_body_inner + buf[b_close_start:]

def replace_tbody_inner(buf, cid, new_rows, label):
    """Replace <tbody>...</tbody> inner inside container id=cid."""
    span = find_container_span(buf, cid)
    if not span:
        print(f'  FAIL [{label}] id={cid} not found'); return None
    _, open_end, close_start, _ = span
    tb = find_tbody(buf, open_end, close_start)
    if not tb:
        print(f'  FAIL [{label}] <tbody> not found inside id={cid}'); return None
    _, tb_open_end, tb_close_start, _ = tb
    old = buf[tb_open_end:tb_close_start]
    delta = len(new_rows) - len(old)
    print(f'  OK   [{label}] id={cid} <tbody> old={len(old)} -> new={len(new_rows)} d={delta:+}')
    return buf[:tb_open_end] + new_rows + buf[tb_close_start:]

def rep(buf, old, new, label, expected_count=1):
    count = buf.count(old)
    if count != expected_count:
        print(f'  FAIL [{label}] count={count}, expected={expected_count}')
        return None
    print(f'  OK   [{label}] replaced {count} occurrence(s)  d={(len(new)-len(old))*count:+}')
    return buf.replace(old, new)

def replace_widget_body(buf, cid, new_inner, label):
    """Replace .dw-body inside cid if present, else replace container inner directly.
       Skip silently if no brand content currently present."""
    span = find_container_span(buf, cid)
    if not span:
        print(f'  SKIP [{label}] container id={cid} not found'); return buf
    _, open_end, close_start, _ = span
    container_inner = buf[open_end:close_start]
    if not any(s in container_inner for s in ['BACARDI','PATRON','Bacardi','Bacard\u00ed','PATR\u00d3N','BACARD\u00cd']):
        print(f'  SKIP [{label}] id={cid} no brand content'); return buf
    # Prefer .dw-body if it exists
    body = find_child_by_class(buf, open_end, close_start, 'dw-body')
    if body:
        _, b_open_end, b_close_start, _ = body
        old = buf[b_open_end:b_close_start]
        delta = len(new_inner) - len(old)
        print(f'  OK   [{label}] id={cid} .dw-body old={len(old)} -> new={len(new_inner)} d={delta:+}')
        return buf[:b_open_end] + new_inner + buf[b_close_start:]
    # Fallback: replace entire container inner
    delta = len(new_inner) - len(container_inner)
    print(f'  OK   [{label}] id={cid} inner (no dw-body) old={len(container_inner)} -> new={len(new_inner)} d={delta:+}')
    return buf[:open_end] + new_inner + buf[close_start:]

# ===============================================================
# BLOCK A -- Dashboard widget & module container bodies -> empty-state
# ===============================================================
print('\n-- Block A: Dashboard widgets & module containers -> empty state --')

# Helper: standard dw-body empty state
def empty_dw_body(msg):
    return f'<div style="padding:40px 20px;text-align:center;color:var(--slate);font-size:13px">{msg}</div>'

# Helper: standard tbody empty row (5 generic cols)
def empty_tbody_row(msg, cols=5):
    return f'<tr><td colspan="{cols}" style="padding:32px 20px;text-align:center;color:var(--slate);font-size:13px">{msg}</td></tr>'

DASHBOARD_WIDGETS = [
    ('programs',             'No active programs'),
    ('kit-inventory',        'No kit inventory yet'),
    ('kits-to-ship',         'No kits pending shipment'),
    ('kit-assembly',         'No assembly gaps'),
    ('kit-portfolio-health', 'No portfolio health data yet'),
    ('delivery-status-tab',  'No active deliveries'),
    ('approvals',            'No pending approvals'),
    ('activity-feed',        'No recent activity'),
    ('staffing-gaps',        'No staffing gaps'),
    ('runner-activity',      'No runner activity'),
    ('replenishment-damage', 'No replenishment requests'),
    ('escalations-alerts',   'No escalations'),
]
for cid, msg in DASHBOARD_WIDGETS:
    out = replace_widget_body(content, cid, empty_dw_body(msg), f'dash:{cid}')
    if out is None: print(f'ABORT: Block A failed on {cid}'); sys.exit(2)
    content = out

# Programs module "tab-programs" table
span = find_container_span(content, 'tab-programs')
if span:
    _, open_end, close_start, _ = span
    tb = find_tbody(content, open_end, close_start)
    if tb:
        _, tb_open_end, tb_close_start, _ = tb
        empty_row = empty_tbody_row('No programs yet', cols=8)
        old_inner = content[tb_open_end:tb_close_start]
        if 'BACARD\u00cd' in old_inner or 'PATR\u00d3N' in old_inner:
            content = content[:tb_open_end] + empty_row + content[tb_close_start:]
            print(f'  OK   [module:tab-programs] <tbody> old={len(old_inner)} -> {len(empty_row)} d={len(empty_row)-len(old_inner):+}')
        else:
            print(f'  SKIP [module:tab-programs] no brand content in tbody')
    else:
        print(f'  FAIL [module:tab-programs] no tbody')
        sys.exit(2)

# Events viewArea + upS2
for cid, msg, cols in [('viewArea', 'No events yet', 8), ('upS2', 'No items yet', 7)]:
    span = find_container_span(content, cid)
    if not span:
        print(f'  SKIP [events:{cid}] not found'); continue
    _, open_end, close_start, _ = span
    tb = find_tbody(content, open_end, close_start)
    if not tb:
        print(f'  SKIP [events:{cid}] no tbody'); continue
    _, tb_open_end, tb_close_start, _ = tb
    old_inner = content[tb_open_end:tb_close_start]
    if any(s in old_inner for s in ['BACARD\u00cd','PATR\u00d3N','BACARDI','PATRON']):
        empty_row = empty_tbody_row(msg, cols=cols)
        content = content[:tb_open_end] + empty_row + content[tb_close_start:]
        print(f'  OK   [events:{cid}] tbody old={len(old_inner)} -> {len(empty_row)} d={len(empty_row)-len(old_inner):+}')
    else:
        print(f'  SKIP [events:{cid}] no brand content')

# Brand Resources contact body panels
BR_CONTACT_BODIES = ['body-mosaic', 'body-sg', 'body-sg3', 'body-rndc', 'body-totalwine',
                     'body-rndc3', 'body-mosaic3']
for cid in BR_CONTACT_BODIES:
    span = find_container_span(content, cid)
    if not span:
        print(f'  SKIP [br:{cid}] not found'); continue
    _, open_end, close_start, _ = span
    old_inner = content[open_end:close_start]
    if not any(s in old_inner for s in ['BACARD\u00cd','PATR\u00d3N','BACARDI','PATRON','Bacard\u00ed','Bacardi']):
        print(f'  SKIP [br:{cid}] no brand content'); continue
    new_inner = '<div style="padding:24px;text-align:center;color:var(--slate);font-size:13px">No contacts yet</div>'
    content = content[:open_end] + new_inner + content[close_start:]
    print(f'  OK   [br:{cid}] inner old={len(old_inner)} -> {len(new_inner)} d={len(new_inner)-len(old_inner):+}')

# tab-usage body
span = find_container_span(content, 'tab-usage')
if span:
    _, open_end, close_start, _ = span
    old_inner = content[open_end:close_start]
    tb = find_tbody(content, open_end, close_start)
    if tb:
        _, tb_open_end, tb_close_start, _ = tb
        ti = content[tb_open_end:tb_close_start]
        if any(s in ti for s in ['BACARD\u00cd','PATR\u00d3N']):
            empty_row = empty_tbody_row('No usage data yet', cols=4)
            content = content[:tb_open_end] + empty_row + content[tb_close_start:]
            print(f'  OK   [usage:tab-usage tbody] old={len(ti)} -> {len(empty_row)}')

# ===============================================================
# BLOCK B -- Filter dropdown options
# ===============================================================
print('\n-- Block B: Filter dropdown options --')

# mflt-brand-panel
span = find_container_span(content, 'mflt-brand-panel')
if span:
    _, open_end, close_start, _ = span
    old_inner = content[open_end:close_start]
    new_inner = ''
    content = content[:open_end] + new_inner + content[close_start:]
    print(f'  OK   [mflt-brand-panel] cleared labels  old={len(old_inner)} -> 0  d={-len(old_inner)}')

# tk-filter-program
span = find_container_span(content, 'tk-filter-program')
if span:
    _, open_end, close_start, _ = span
    old_inner = content[open_end:close_start]
    m = re.search(r'<option[^>]*>All Programs</option>', old_inner)
    if m:
        new_inner = old_inner[:m.end()]
        content = content[:open_end] + new_inner + content[close_start:]
        print(f'  OK   [tk-filter-program] kept "All Programs" only  old={len(old_inner)} -> {len(new_inner)}')
    else:
        print(f'  FAIL [tk-filter-program] "All Programs" option not found'); sys.exit(2)

# log-cost-overlay select options
span = find_container_span(content, 'log-cost-overlay')
if span:
    _, open_end, close_start, _ = span
    old_inner = content[open_end:close_start]
    branded_opts = re.findall(r'<option[^>]*>[^<]*(?:BACARD\u00cd|PATR\u00d3N|BACARDI|PATRON)[^<]*</option>', old_inner)
    if branded_opts:
        new_inner = old_inner
        for opt in branded_opts:
            new_inner = new_inner.replace(opt, '', 1)
        content = content[:open_end] + new_inner + content[close_start:]
        print(f'  OK   [log-cost-overlay] removed {len(branded_opts)} branded options  d={len(new_inner)-len(old_inner):+}')

# ===============================================================
# BLOCK C -- Programs wizard pre-filled content
# ===============================================================
print('\n-- Block C: Programs wizard pre-filled content --')

PROGRAM_BLOCK_IDS = [
    'psec-2','psec-4','psec-7',
    'scope-market-sel','prog-kit-sel','prog-recipe-pills',
    'prog-assets-pills','prog-instr-sel','prog-attire-sel','prog-training-pills',
    'ap-sec-4','ap-rec-body',
]
for cid in PROGRAM_BLOCK_IDS:
    span = find_container_span(content, cid)
    if not span:
        print(f'  SKIP [prog:{cid}] not found'); continue
    _, open_end, close_start, _ = span
    old_inner = content[open_end:close_start]
    if not any(s in old_inner for s in ['BACARD\u00cd','PATR\u00d3N','BACARDI','PATRON']):
        print(f'  SKIP [prog:{cid}] no brand content'); continue
    new_inner = '<div style="padding:16px;color:var(--slate);font-size:12px;font-style:italic">No selections yet</div>'
    content = content[:open_end] + new_inner + content[close_start:]
    print(f'  OK   [prog:{cid}] inner old={len(old_inner)} -> {len(new_inner)} d={len(new_inner)-len(old_inner):+}')

# ===============================================================
# BLOCK D -- Page subtitles / headers -> "your company"
# ===============================================================
print('\n-- Block D: Page subtitles --')

SUBTITLE_SWEEPS = [
    ('All field events across Bacard\u00ed USA \u00b7 13 total this month',
     'All field events across your company', 1),
    ('FyldRunners on the Bacard\u00ed USA account',
     'FyldRunners on your account', 1),
    ('Action items assigned to you \u00b7 Bacard\u00ed USA \u00b7 Alex M.',
     'Action items assigned to you \u00b7 your company \u00b7 Alex M.', 1),
    ('Bacard\u00ed USA \u00b7 Billed monthly \u00b7 Next billing: Apr 1, 2026',
     'Your Company \u00b7 Billed monthly', 1),
    ('invited by <strong>Alex Morgan</strong> at Bacardi Limited',
     'invited by <strong>Alex Morgan</strong> at your company', 1),
    ('Bacardi USA vs. industry average',
     'Your company vs. industry average', 1),
]
for old, new, n in SUBTITLE_SWEEPS:
    out = rep(content, old, new, f'subtitle: {old[:50]}...', expected_count=n)
    if out is None: print('ABORT: subtitle sweep'); sys.exit(2)
    content = out

# rBN -- "training for BACARDI Rum" -- inside a strong with id="rBN"
out = rep(content,
          '<strong id="rBN">BACARD\u00cd Rum</strong>',
          '<strong id="rBN">this brand</strong>',
          'rBN strong inner', expected_count=1)
if out is None: print('ABORT: rBN'); sys.exit(2)
content = out

# ob-sec-4 brand assignment line
out = rep(content,
          'style="font-weight:700;color:var(--dark)">BACARD\u00cd Rum \u00b7 PATR\u00d3N</div>',
          'style="font-weight:700;color:var(--dark)">Your assigned brands</div>',
          'ob-sec-4 brand assignment', expected_count=1)
if out is None: print('ABORT: ob-sec-4'); sys.exit(2)
content = out

# ===============================================================
# BLOCK E -- Form placeholders
# ===============================================================
print('\n-- Block E: Form placeholders --')

placeholder_pat = re.compile(r'placeholder="[^"]*(?:BACARD\u00cd|PATR\u00d3N|BACARDI|PATRON|Bacard\u00ed|Bacardi|Patr\u00f3n)[^"]*"')
matches = placeholder_pat.findall(content)
print(f'  Found {len(matches)} branded placeholders to strip')
pre_len = len(content)
for m in matches:
    content = content.replace(m, 'placeholder=""', 1)
print(f'  OK   [placeholders] stripped {len(matches)} branded placeholders  d={len(content)-pre_len:+}')

# ===============================================================
# BLOCK F -- Decorative HTML comments
# ===============================================================
print('\n-- Block F: Decorative comments --')

html_comment_pat = re.compile(r'<!--\s*(?:BACARD\u00cd|PATR\u00d3N|BACARDI|PATRON|Bacard\u00ed|Bacardi)[^>]*-->')
comments = html_comment_pat.findall(content)
print(f'  Found {len(comments)} branded HTML comments')
for c in comments:
    content = content.replace(c, '', 1)
    short = c[:60].replace('\n',' ')
    print(f'  OK   [comment] removed: {short}...')

# ===============================================================
# BLOCK G -- Residual text substitutions
# ===============================================================
print('\n-- Block G: Residual text substitutions --')

toast_pat = re.compile(r"toast\('[^']*(?:BACARD\u00cd|PATR\u00d3N|BACARDI|PATRON)[^']*'\)")
toasts = toast_pat.findall(content)
print(f'  Remaining brand toast() calls: {len(toasts)}  (expected 0 after A-F)')

# fc-kpi-reimb card holder
out = rep(content,
          '<div style="font-size:12px;font-weight:600">Bacard\u00ed USA</div>',
          '<div style="font-size:12px;font-weight:600">Your Company</div>',
          'fc-kpi-reimb card holder', expected_count=1)
if out is None:
    print('  SKIP [fc-kpi-reimb]  not found (maybe already neutralized)')
else:
    content = out

# ===============================================================
# BLOCK H -- Deep residual sweep
# ===============================================================
print('\n-- Block H: Deep residual sweep --')

# H.1 -- Budget Configuration tree
marker = 'Budget Configuration \u2014 2026</div>'
midx = content.find(marker)
if midx != -1:
    wrap_start = content.find('<div style="padding:16px 20px">', midx)
    if wrap_start != -1:
        wrap_open_end = content.find('>', wrap_start) + 1
        depth = 1; i = wrap_open_end
        while i < len(content) and depth > 0:
            om = content.find('<div', i); cm = content.find('</div>', i)
            if cm == -1: break
            if om != -1 and om < cm: depth += 1; i = content.find('>', om) + 1
            else: depth -= 1; i = cm + len('</div>')
        wrap_close_start = i - len('</div>')
        old_inner = content[wrap_open_end:wrap_close_start]
        if any(s in old_inner for s in ['BACARD\u00cd','PATR\u00d3N']):
            new_inner = '\n<div style="padding:40px 20px;text-align:center;color:var(--slate);font-size:13px">No budget pools configured yet</div>\n'
            content = content[:wrap_open_end] + new_inner + content[wrap_close_start:]
            print(f'  OK   [H.1 budget tree] old={len(old_inner)} -> {len(new_inner)} d={len(new_inner)-len(old_inner):+}')
        else:
            print(f'  SKIP [H.1 budget tree] no brand content')
else:
    print(f'  SKIP [H.1 budget tree] marker not found')

out = rep(content,
          'across 3 brands \u00b7 2026',
          'your 2026 budgets',
          'H.1b summary 3 brands', expected_count=1)
if out is None: print('  SKIP [H.1b summary 3 brands]  ')
else: content = out

# H.2 -- tab-usage brand labels
usage_brand_pat = re.compile(r'<div style="font-size:12px;color:var\(--slate\)">(?:BACARD\u00cd|PATR\u00d3N)[^<]*</div>')
matches = list(usage_brand_pat.finditer(content))
print(f'  H.2 tab-usage brand labels found: {len(matches)}')
for m in reversed(matches):
    old = m.group(0)
    new = '<div style="font-size:12px;color:var(--slate)">\u2014</div>'
    content = content[:m.start()] + new + content[m.end():]
print(f'  OK   [H.2 tab-usage labels] replaced {len(matches)}')

# H.3 -- ingRows recipe ingredients
out = rep(content,
          '<input type="text" value="BACARD\u00cd Superior">',
          '<input type="text" value="">',
          'H.3 ingRows BACARDI Superior', expected_count=1)
if out is None: print('  SKIP [H.3a ingRows]  ')
else: content = out

ing_textarea_pat = re.compile(r'<textarea>[^<]*BACARD\u00cd[^<]*</textarea>')
m = ing_textarea_pat.search(content)
if m:
    content = content[:m.start()] + '<textarea></textarea>' + content[m.end():]
    print(f'  OK   [H.3b ingRows textarea] cleared BACARDI recipe text')

# H.4 -- Brand-pill labels
pill_pat = re.compile(
    r'<label class="prog-evtcat-pill[^"]*" onclick="toggleEvtCat\(this\)"><input type="checkbox" style="display:none">\s*(?:BACARD\u00cd|PATR\u00d3N)[^<]*</label>\s*'
)
pre = len(content)
content = pill_pat.sub('', content)
print(f'  OK   [H.4 brand-pill labels] stripped  d={len(content)-pre:+}')

# H.5 -- kit-item-rows + smod-kit-rows option tags
for cid in ['kit-item-rows', 'smod-kit-rows']:
    span = find_container_span(content, cid)
    if not span:
        print(f'  SKIP [H.5 {cid}] not found'); continue
    _, open_end, close_start, _ = span
    old_inner = content[open_end:close_start]
    new_inner = re.sub(
        r'<option>(?:BACARD\u00cd|PATR\u00d3N)[^<]*</option>\s*',
        '',
        old_inner
    )
    delta = len(new_inner) - len(old_inner)
    if delta != 0:
        content = content[:open_end] + new_inner + content[close_start:]
        print(f'  OK   [H.5 {cid}] d={delta:+}')
    else:
        print(f'  SKIP [H.5 {cid}] no branded options')

# H.6 -- Brand cms-option chips
cms_pat = re.compile(
    r'<div class="cms-option(?:\s+cms-selected)?" onclick="toggleCms\(this\)">\s*(?:BACARD\u00cd|PATR\u00d3N)[^<]*</div>\s*'
)
pre = len(content)
content = cms_pat.sub('', content)
print(f'  OK   [H.6 cms-option chips] stripped  d={len(content)-pre:+}')

# H.7 -- dash-today-events-date sibling event rows
old_line1 = ' BACARD\u00cd Rum \u00b7 Off-Premise \u00b7 2:00\u20136:00 PM'
old_line2 = ' BACARD\u00cd RTD \u00b7 Off-Premise \u00b7 9:00 AM\u20131:00 PM'
for old, new in [(old_line1, ''), (old_line2, '')]:
    if content.count(old) == 1:
        content = content.replace(old, new)
        print(f'  OK   [H.7 today-events line] cleared')
    else:
        print(f'  SKIP [H.7] line count={content.count(old)}')

# H.8 -- Billing address
out = rep(content,
          'Bacard\u00ed USA LLC<br>2701 Le Jeune Rd<br>Coral Gables, FL 33134',
          'Your Company<br>Address line 1<br>City, ST 00000',
          'H.8 billing address', expected_count=1)
if out is None: print('  SKIP [H.8 billing address]  ')
else: content = out

# H.9 -- Dev comment
out = rep(content,
          '<!-- MVP: empty state replaces seed BACARD\u00cd tree -->',
          '',
          'H.9 dev comment', expected_count=1)
if out is None: print('  SKIP [H.9 dev comment]  ')
else: content = out

# ===============================================================
# Final verification
# ===============================================================
print('\n-- Final verification --')

script_blocks = [(m.start(), m.end()) for m in re.finditer(r'<script[^>]*>.*?</script>', content, re.DOTALL)]
in_script = lambda i: any(s <= i < e for s,e in script_blocks)
html_brand_hits = sum(1 for m in re.finditer(r'(BACARD\u00cd|PATR\u00d3N|Bacard\u00ed|Patr\u00f3n|BACARDI|PATRON|Bacardi)', content)
                      if not in_script(m.start()))
print(f'  HTML-context brand hits remaining: {html_brand_hits}  (was 185)')

print(f'\nFinal size: {len(content):,}  (delta {len(content)-BASELINE:+})')

with open(TARGET, 'w') as f:
    f.write(content)
print(f'Done. Patch 17B written to {TARGET}')
