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

print(f"✓ Targeting: {TARGET}")

# ─── BASELINE CHECK ─────────────────────────────────────────────
content = open(TARGET, "r", encoding="utf-8").read()
BASELINE = 3800084
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

# ═══════════════════════════════════════════════════════════════
# PATCH 9A: Zero out EC_DATA (Event Categories) — JS array
# ═══════════════════════════════════════════════════════════════
ec_match = re.search(r'var EC_DATA = \[.*?\];', content, re.DOTALL)
if ec_match:
    old_ec = ec_match.group(0)
    if content.count(old_ec) == 1:
        content = content.replace(old_ec, "var EC_DATA = [];", 1)
        print("✓ Patched: EC_DATA zeroed out")
    else:
        print(f"ERROR [EC_DATA]: Found {content.count(old_ec)} occurrences. Aborting.")
        sys.exit(1)
else:
    print("ERROR: EC_DATA not found. Aborting.")
    sys.exit(1)

# ═══════════════════════════════════════════════════════════════
# PATCH 9B: Company Profile — clear Bacardi-specific values
# ═══════════════════════════════════════════════════════════════
rep(
    '<div style="font-size:15px;font-weight:700;color:var(--dark)">Bacardi Limited</div>',
    '<div style="font-size:15px;font-weight:700;color:var(--dark)">Your Company Name</div>',
    "Company Profile: clear company name header"
)

rep(
    '<div class="cp-value" id="cp-legal">Bacardi Limited</div>',
    '<div class="cp-value" id="cp-legal" style="color:var(--slate);font-style:italic">Not set</div>',
    "Company Profile: clear legal name"
)

rep(
    '<div class="cp-value" id="cp-dba">Bacardí USA</div>',
    '<div class="cp-value" id="cp-dba" style="color:var(--slate);font-style:italic">Not set</div>',
    "Company Profile: clear DBA name"
)

rep(
    'Private · Family-owned',
    '',
    "Company Profile: clear company type"
)

rep(
    '<div class="cp-value">1862</div>',
    '<div class="cp-value" style="color:var(--slate);font-style:italic">Not set</div>',
    "Company Profile: clear founded year"
)

rep(
    '<div class="cp-value">Hamilton, Bermuda</div>',
    '<div class="cp-value" style="color:var(--slate);font-style:italic">Not set</div>',
    "Company Profile: clear headquarters"
)

rep(
    '<div class="cp-value"><div style="display:flex;flex-direction:column;gap:3px"><span>Coral Gables, FL, USA <span class="badge b-teal" style="font-size:12px;padding:1px 5px">Primary</span></span><span style="color:var(--slate);font-size:12px">New York, NY, USA</span><span style="color:var(--slate);font-size:12px">Hamilton, Bermuda</span><span style="color:var(--slate);font-size:12px">London, UK</span></div></div>',
    '<div class="cp-value" style="color:var(--slate);font-style:italic">Not set</div>',
    "Company Profile: clear operations locations"
)

rep(
    '<a href="https://www.bacardilimited.com/" style="color:var(--teal)" target="_blank">bacardilimited.com</a>',
    '<span style="color:var(--slate);font-style:italic">Not set</span>',
    "Company Profile: clear website"
)

# Platform config
rep(
    '<div class="cp-value">Bacardí USA — FyldHub</div>',
    '<div class="cp-value" style="color:var(--slate);font-style:italic">Not set</div>',
    "Company Profile: clear account name"
)

rep(
    '<code style="font-size:12px;background:var(--lgray);padding:2px 6px;border-radius:3px;font-family:monospace">acc_bac_001</code>',
    '<code style="font-size:12px;background:var(--lgray);padding:2px 6px;border-radius:3px;font-family:monospace">—</code>',
    "Company Profile: clear account ID"
)

rep(
    '<span class="badge b-green" style="font-size:12px">Enterprise</span>',
    '<span class="badge" style="font-size:12px;background:var(--lgray);color:var(--slate)">Launch</span>',
    "Company Profile: reset plan to Launch"
)

rep(
    '<div class="cp-value">April 2026</div>',
    '<div class="cp-value" style="color:var(--slate);font-style:italic">—</div>',
    "Company Profile: clear active since"
)

# Compliance section
rep(
    '<div class="cp-value">12-345-6789</div>',
    '<div class="cp-value" style="color:var(--slate);font-style:italic">Not set</div>',
    "Company Profile: clear DUNS"
)

rep(
    '<div class="cp-value" id="cp-licenses-display"><div style="display:flex;flex-direction:column;gap:5px"><div><span class="badge b-green" style="font-size:11px">Verified</span> <span style="font-size:12px">TTB Importer #US12345</span></div><div><span class="badge b-green" style="font-size:11px">Active</span> <span style="font-size:12px">FL DABT License #AB1234567</span></div><div><span class="badge b-amber" style="font-size:11px">Pending</span> <span style="font-size:12px">TX TABC Permit #TX-98765</span></div></div></div>',
    '<div class="cp-value" id="cp-licenses-display" style="color:var(--slate);font-style:italic">No licenses added</div>',
    "Company Profile: clear licenses"
)

rep(
    '<span class="badge b-green" style="font-size:11px">Signed</span> <a href="#" style="color:var(--teal);font-size:12px">View DPA</a>',
    '<span style="color:var(--slate);font-style:italic;font-size:12px">Not signed</span>',
    "Company Profile: clear DPA status"
)

# ═══════════════════════════════════════════════════════════════
# PATCH 9C: Users table — replace 5 fake users with empty state
# ═══════════════════════════════════════════════════════════════
users_match = re.search(
    r'<tbody id="users-internal-tbody">.*?</tbody>',
    content, re.DOTALL
)
if users_match:
    old_tbody = users_match.group(0)
    if content.count(old_tbody) == 1:
        new_tbody = '''<tbody id="users-internal-tbody">
        <tr>
          <td colspan="9" style="text-align:center;padding:48px 24px;color:var(--slate)">
            <div style="font-size:15px;font-weight:600;color:var(--dark);margin-bottom:6px">No users yet</div>
            <div style="font-size:13px;margin-bottom:16px">Invite your team to get started. Each user is assigned a role and scope.</div>
            <button class="btn btn-primary btn-sm" onclick="openInviteUser()">+ Invite User</button>
          </td>
        </tr>
      </tbody>'''
        content = content.replace(old_tbody, new_tbody, 1)
        print("✓ Patched: Users table emptied")
    else:
        print(f"ERROR [Users tbody]: Found {content.count(old_tbody)} occurrences. Aborting.")
        sys.exit(1)
else:
    print("ERROR: Users tbody not found. Aborting.")
    sys.exit(1)

# ═══════════════════════════════════════════════════════════════
# PATCH 9D: Locations — clear territory/market table rows
# ═══════════════════════════════════════════════════════════════
# Territory rows block
rep(
    '<tr><td class="fw">New England</td><td><span class="hier-pill-sm" style="background:#1E4DB7">Northeast</span></td><td>Boston, Hartford, Providence</td><td><div class="flex ic g2"><div class="avs" style="background:#8B5CF6;font-size:11px">TR</div>Tom R.</div></td><td><div class="flex g1"><button class="btn btn-ghost btn-sm">Edit</button></div></td></tr>\n            <tr><td class="fw">Mid-Atlantic</td><td><span class="hier-pill-sm" style="background:#1E4DB7">Northeast</span></td><td>NYC, Philadelphia, DC, Baltimore</td><td><div class="flex ic g2"><div class="avs" style="background:#059669;font-size:11px">CM</div>Chris M.</div></td><td><div class="flex g1"><button class="btn btn-ghost btn-sm">Edit</button></div></td></tr>\n            <tr><td class="fw">Florida</td><td><span class="hier-pill-sm" style="background:#D97706">Southeast</span></td><td>Miami, Tampa</td><td class="ts tsl">Unassigned</td><td><div class="flex g1"><button class="btn btn-ghost btn-sm">Edit</button></div></td></tr>\n            <tr><td class="fw">Carolinas &amp; Georgia</td><td><span class="hier-pill-sm" style="background:#D97706">Southeast</span></td><td>Atlanta, Charlotte, Nashville</td><td class="ts tsl">Unassigned</td><td><div class="flex g1"><button class="btn btn-ghost btn-sm">Edit</button></div></td></tr>\n            <tr><td class="fw">Southern California</td><td><span class="hier-pill-sm" style="background:var(--teal)">West Coast</span></td><td>LA, San Diego, OC, Inland Empire</td><td><div class="flex ic g2"><div class="avs" style="background:#D97706;font-size:11px">MW</div>Marcus W.</div></td><td><div class="flex g1"><button class="btn btn-ghost btn-sm">Edit</button></div></td></tr>\n            <tr><td class="fw">Northern California</td><td><span class="hier-pill-sm" style="background:var(--teal)">West Coast</span></td><td>San Francisco, Sacramento</td><td class="ts tsl">Unassigned</td><td><div class="flex g1"><button class="btn btn-ghost btn-sm">Edit</button></div></td></tr>\n            <tr><td class="fw">Pacific Northwest</td><td><span class="hier-pill-sm" style="background:var(--teal)">West Coast</span></td><td>Seattle, Portland</td><td class="ts tsl">Unassigned</td><td><div class="flex g1"><button class="btn btn-ghost btn-sm">Edit</button></div></td></tr>',
    '<tr><td colspan="5" style="text-align:center;padding:32px;color:var(--slate);font-size:13px">No territories added yet. Use the hierarchy to define your geographic structure.</td></tr>',
    "Locations: clear territory rows"
)

# Market rows block
rep(
    '<tr><td class="fw">Los Angeles</td><td>Southern California</td><td><span class="hier-pill-sm" style="background:var(--teal)">West Coast</span></td><td><div class="flex ic g2"><div class="avs" style="font-size:11px">JL</div>Jamie L.</div></td><td><button class="btn btn-ghost btn-sm">Edit</button></td></tr>\n            <tr><td class="fw">San Diego</td><td>Southern California</td><td><span class="hier-pill-sm" style="background:var(--teal)">West Coast</span></td><td><div class="flex ic g2"><div class="avs" style="background:#D97706;font-size:11px">MW</div>Marcus W.</div></td><td><button class="btn btn-ghost btn-sm">Edit</button></td></tr>\n            <tr><td class="fw">Greater Boston</td><td>New England</td><td><span class="hier-pill-sm" style="background:#1E4DB7">Northeast</span></td><td><div class="flex ic g2"><div class="avs" style="background:#8B5CF6;font-size:11px">TR</div>Tom R.</div></td><td><button class="btn btn-ghost btn-sm">Edit</button></td></tr>\n            <tr><td class="fw">New York City</td><td>Mid-Atlantic</td><td><span class="hier-pill-sm" style="background:#1E4DB7">Northeast</span></td><td><div class="flex ic g2"><div class="avs" style="background:#059669;font-size:11px">CM</div>Chris M.</div></td><td><button class="btn btn-ghost btn-sm">Edit</button></td></tr>\n            <tr><td class="fw">Miami</td><td>Florida</td><td><span class="hier-pill-sm" style="background:#D97706">Southeast</span></td><td class="ts tsl">Unassigned</td><td><button class="btn btn-ghost btn-sm">Edit</button></td></tr>\n            <tr><td class="fw">Atlanta</td><td>Carolinas &amp; Georgia</td><td><span class="hier-pill-sm" style="background:#D97706">Southeast</span></td><td class="ts tsl">Unassigned</td><td><button class="btn btn-ghost btn-sm">Edit</button></td></tr>',
    '<tr><td colspan="5" style="text-align:center;padding:32px;color:var(--slate);font-size:13px">No markets added yet. Add territories first, then define markets within each territory.</td></tr>',
    "Locations: clear market rows"
)

# Clear location stat badges
rep(
    'Regions <span class="loc-ltab-count">4</span>',
    'Regions <span class="loc-ltab-count">0</span>',
    "Locations: reset Regions count"
)
rep(
    'Territories <span class="loc-ltab-count">9</span>',
    'Territories <span class="loc-ltab-count">0</span>',
    "Locations: reset Territories count"
)
rep(
    'Markets <span class="loc-ltab-count">24</span>',
    'Markets <span class="loc-ltab-count">0</span>',
    "Locations: reset Markets count"
)
rep(
    'National <span class="loc-ltab-count">1</span>',
    'National <span class="loc-ltab-count">0</span>',
    "Locations: reset National count"
)
# Also clear the "4 Regions" text in the national row
rep(
    '<td>4 Regions</td>',
    '<td>0 Regions</td>',
    "Locations: reset national row region count"
)

# ═══════════════════════════════════════════════════════════════
# PATCH 9E: Brand Resources — clear hardcoded digital resource counts
# ═══════════════════════════════════════════════════════════════
rep(
    '2 recipes',
    '0 recipes',
    "Brand Resources: clear recipe count"
)
rep(
    '2 templates',
    '0 templates',
    "Brand Resources: clear templates count"
)
rep(
    '1 document',
    '0 documents',
    "Brand Resources: clear knowledge base count"
)
rep(
    '1 guide',
    '0 guides',
    "Brand Resources: clear attire guide count"
)
rep(
    '1 checklist',
    '0 checklists',
    "Brand Resources: clear compliance count"
)

# Clear physical asset catalog rows (uses div.asset-catalog-row, not <tr>)
# Replace all 5 asset-catalog-row blocks with empty state
asset_match = re.search(
    r'(<div class="asset-catalog-row">.*?</div>\s*</div>\s*){5}',
    content, re.DOTALL
)
if asset_match:
    old_assets = asset_match.group(0)
    if content.count(old_assets) == 1:
        content = content.replace(old_assets,
            '<div style="text-align:center;padding:32px;color:var(--slate);font-size:13px">No physical assets added yet. Add assets to include them in kit templates.</div>\n',
            1)
        print("\u2713 Patched: Brand Resources: clear physical asset catalog rows")
    else:
        print(f"ERROR [Asset rows]: Found {content.count(old_assets)} occurrences. Aborting.")
        sys.exit(1)
else:
    print("ERROR: Asset catalog rows not found. Aborting.")
    sys.exit(1)

# ═══════════════════════════════════════════════════════════════
# WRITE OUTPUT
# ═══════════════════════════════════════════════════════════════
open(TARGET, "w", encoding="utf-8").write(content)
final_len = len(open(TARGET, "r", encoding="utf-8").read())
print(f"\n✓ Patch 9 complete. New char count: {final_len}")
print("  Run: node --check FyldHub_MVP_Prototype.html")
