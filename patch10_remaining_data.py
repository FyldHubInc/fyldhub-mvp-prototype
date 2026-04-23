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
BASELINE = 3778021
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
# PATCH 10A: Brand Portfolio — clear subtitle count + brand rows
# ═══════════════════════════════════════════════════════════════
rep(
    '<div class="card-sub">3 brands \u00b7 34 products</div>',
    '<div class="card-sub">0 brands \u00b7 0 products</div>',
    "Brand Portfolio: clear brand/product count"
)

# Clear the three hardcoded brand rows — replace entire brands block with empty state
# The block starts after the table header and ends before the closing table tag
rep(
    '''            <!-- BACARD\u00cd Rum -->''',
    '''            <!-- MVP SKELETON: brands cleared -->''',
    "Brand Portfolio: mark brand rows for replacement"
)

# Now replace from the marker through to the end of the brand table tbody
brand_block_match = re.search(
    r'<!-- MVP SKELETON: brands cleared -->.*?</tbody>\s*</table>',
    content, re.DOTALL
)
if brand_block_match:
    old_block = brand_block_match.group(0)
    if content.count(old_block) == 1:
        content = content.replace(old_block,
            '''<tr><td colspan="5" style="text-align:center;padding:48px 24px;color:var(--slate)">
                <div style="font-size:15px;font-weight:600;color:var(--dark);margin-bottom:6px">No brands yet</div>
                <div style="font-size:13px;margin-bottom:16px">Add your first brand to get started. Each brand has its own product catalog and settings.</div>
                <button class="btn btn-primary btn-sm" onclick="openAddBrand()">+ Add Brand</button>
              </td></tr>
            </tbody></table>''', 1)
        print("\u2713 Patched: Brand Portfolio rows replaced with empty state")
    else:
        print(f"ERROR [Brand rows block]: Found {content.count(old_block)} occurrences. Aborting.")
        sys.exit(1)
else:
    print("ERROR: Brand rows block not found. Aborting.")
    sys.exit(1)

# ═══════════════════════════════════════════════════════════════
# PATCH 10B: Company Profile — clear hardcoded static values
# that Patch 9 already applied to the MVP file
# Now fix the subtitle "Adult Beverage" and parent categories badge
# ═══════════════════════════════════════════════════════════════
rep(
    '<div class="ts tsl" style="font-size:12px" id="cp-subtitle">Adult Beverage</div>',
    '<div class="ts tsl" style="font-size:12px" id="cp-subtitle" style="color:var(--slate);font-style:italic">Not set</div>',
    "Company Profile: clear subtitle Adult Beverage"
)

rep(
    '<div class="cp-value" id="cp-parent-categories"><span class="badge b-teal" style="font-size:12px">Adult Beverage</span></div>',
    '<div class="cp-value" id="cp-parent-categories" style="color:var(--slate);font-style:italic">Not set</div>',
    "Company Profile: clear parent categories badge"
)

# ═══════════════════════════════════════════════════════════════
# PATCH 10C: Company Profile Edit Modal — clear hardcoded values
# ═══════════════════════════════════════════════════════════════
rep(
    'value="Bacardi Limited" id="ep-legal"',
    'value="" placeholder="Legal name" id="ep-legal"',
    "Edit Company Profile modal: clear legal name"
)

rep(
    'value="Bacard\u00ed USA" id="ep-dba"',
    'value="" placeholder="DBA / Trade name" id="ep-dba"',
    "Edit Company Profile modal: clear DBA"
)

rep(
    'value="bacardilimited.com">',
    'value="" placeholder="https://yourcompany.com">',
    "Edit Company Profile modal: clear website"
)

rep(
    'value="Hamilton, Bermuda" placeholder="City, Country"',
    'value="" placeholder="City, Country"',
    "Edit Company Profile modal: clear headquarters"
)

# Clear operations locations — these are in JS string concat lines
# Replace each pre-filled city value with empty
rep(
    'value="Coral Gables, FL, USA"',
    'value=""',
    "Edit Company Profile modal: clear Coral Gables"
)
rep(
    'value="New York, NY, USA"',
    'value=""',
    "Edit Company Profile modal: clear New York"
)
# Hamilton, Bermuda in ops-list (HQ field already cleared above, so this is now unique):
rep(
    'value="Hamilton, Bermuda" style="flex:1;font-size:13px"',
    'value="" style="flex:1;font-size:13px"',
    "Edit Company Profile modal: clear Hamilton ops"
)
# The London one:
rep(
    'value="London, UK"',
    'value=""',
    "Edit Company Profile modal: clear London"
)

# Fix parentCategories fallback defaults — prevent Adult Beverage auto-checking
# There are multiple occurrences across different functions, replace all
content = content.replace(
    "APP_DATA.parentCategories || ['Adult Beverage']",
    "APP_DATA.parentCategories || []"
)
print(f"\u2713 Patched: Remove Adult Beverage defaults (all occurrences)")

# ═══════════════════════════════════════════════════════════════
# PATCH 10D: Invite Team Member modal — disable Merchandising + On-Demand hubs
# ═══════════════════════════════════════════════════════════════
# Disable Merchandising hub checkbox
rep(
    '<label id="iu-hub-me-wrap" style="display:flex;align-items:center;gap:10px;padding:10px 12px;border:1.5px solid var(--border);border-radius:var(--radius);cursor:pointer;font-size:13px">',
    '<label id="iu-hub-me-wrap" style="display:flex;align-items:center;gap:10px;padding:10px 12px;border:1.5px solid var(--border);border-radius:var(--radius);cursor:not-allowed;font-size:13px;opacity:.45;pointer-events:none">',
    "Invite modal: disable Merchandising hub label"
)
rep(
    '              <div style="font-weight:600;color:var(--dark)">Merchandising</div>',
    '              <div style="font-weight:600;color:var(--dark)">Merchandising <span style="font-size:9px;font-weight:700;background:#F59E0B;color:#fff;padding:2px 5px;border-radius:3px;vertical-align:middle;margin-left:4px">PHASE 2</span></div>',
    "Invite modal: badge Merchandising"
)

# Disable On-Demand hub checkbox
rep(
    '<label id="iu-hub-od-wrap" style="display:flex;align-items:center;gap:10px;padding:10px 12px;border:1.5px solid var(--border);border-radius:var(--radius);cursor:pointer;font-size:13px">',
    '<label id="iu-hub-od-wrap" style="display:flex;align-items:center;gap:10px;padding:10px 12px;border:1.5px solid var(--border);border-radius:var(--radius);cursor:not-allowed;font-size:13px;opacity:.45;pointer-events:none">',
    "Invite modal: disable On-Demand hub label"
)
rep(
    '              <div style="font-weight:600;color:var(--dark)">On-Demand Support</div>',
    '              <div style="font-weight:600;color:var(--dark)">On-Demand Support <span style="font-size:9px;font-weight:700;background:#F59E0B;color:#fff;padding:2px 5px;border-radius:3px;vertical-align:middle;margin-left:4px">PHASE 2</span></div>',
    "Invite modal: badge On-Demand"
)

# ═══════════════════════════════════════════════════════════════
# PATCH 10E: Worker Pay — remove Merchandising Hub + On-Demand Hub sections
# Keep only Activations Hub (FyldPromoter) section
# Also remove Kit & Asset Delivery and Festival & Trade Show sections
# ═══════════════════════════════════════════════════════════════
# Find and replace the Financials Worker Pay content
# The Merchandising Hub section starts with the MERCHANDISING HUB header
# We need to remove everything from MERCHANDISING HUB onwards in the pay tab

merch_match = re.search(
    r'(<div[^>]*>[\s\S]*?MERCHANDISING HUB[\s\S]*?)(Save Rate Card)',
    content, re.DOTALL
)
if merch_match:
    full_section = merch_match.group(0)
    save_btn = merch_match.group(2)
    if content.count(full_section) == 1:
        # Keep only Save Rate Card button, remove Merchandising + On-Demand sections
        content = content.replace(full_section,
            f'\n            <div style="margin-top:24px;padding-top:16px;border-top:1px solid var(--border);display:flex;align-items:center;justify-content:space-between">\n              <div style="font-size:12px;color:var(--slate);font-style:italic">Merchandising Hub and On-Demand Hub rates are Phase 2.</div>\n              {save_btn}', 1)
        print("\u2713 Patched: Worker Pay \u2014 removed Merchandising + On-Demand hub sections")
    else:
        print(f"WARNING: Merch/OD section found {content.count(full_section)} times, skipping")
else:
    print("WARNING: Merchandising Hub section not found in Worker Pay, skipping")

# ═══════════════════════════════════════════════════════════════
# PATCH 10F: Brand Resources — remove leftover Cocktail Shaker row fragment
# (the "All Brands / 24oz / 1 kit" orphan row visible in image 3)
# ═══════════════════════════════════════════════════════════════
# This is the remnant of the Cocktail Shaker row that didn't get fully cleared
leftover_match = re.search(
    r'<tr[^>]*>\s*<td[^>]*>\s*</td>\s*<td[^>]*>\s*<span[^>]*>All Brands</span>\s*</td>\s*<td[^>]*>24oz</td>\s*<td[^>]*>1 kit</td>\s*<td[^>]*>.*?</td>\s*</tr>',
    content, re.DOTALL
)
if leftover_match:
    old_row = leftover_match.group(0)
    if content.count(old_row) == 1:
        content = content.replace(old_row, '', 1)
        print("\u2713 Patched: Brand Resources \u2014 removed orphan Cocktail Shaker row")
    else:
        print(f"WARNING: Orphan row found {content.count(old_row)} times, skipping")
else:
    print("INFO: Orphan Cocktail Shaker row not found (may already be cleared)")

# ═══════════════════════════════════════════════════════════════
# PATCH 10G: Brand Resources kit cards — remove hardcoded kit cards
# ═══════════════════════════════════════════════════════════════
# Find kit cards section and replace with empty state
kit_match = re.search(
    r'(<div[^>]*class="kit-card[^>]*>[\s\S]*?)(<!--\s*end kit)',
    content, re.DOTALL
)
if kit_match:
    old_kits = kit_match.group(1)
    if content.count(old_kits) == 1:
        content = content.replace(old_kits,
            '<div style="text-align:center;padding:32px;color:var(--slate);font-size:13px">No kit templates yet. Click + New Kit to create your first template.</div>\n            <!--  end kit', 1)
        print("\u2713 Patched: Brand Resources \u2014 kit cards replaced with empty state")
    else:
        print("WARNING: Kit cards block found multiple times, skipping")
else:
    print("INFO: Kit cards block not found via regex")

# ═══════════════════════════════════════════════════════════════
# PATCH 10H: Company topbar — clear "Bacardí USA" company name
# ═══════════════════════════════════════════════════════════════
rep(
    '<div class="gt-mid"><span class="gt-company">Bacard\u00ed USA</span></div>',
    '<div class="gt-mid"><span class="gt-company">Your Company</span></div>',
    "Topbar: clear Bacardi USA company name"
)

# ═══════════════════════════════════════════════════════════════
# WRITE OUTPUT
# ═══════════════════════════════════════════════════════════════
open(TARGET, "w", encoding="utf-8").write(content)
final_len = len(open(TARGET, "r", encoding="utf-8").read())
print(f"\n\u2713 Patch 10 complete. New char count: {final_len}")
print("  Run: node --check FyldHub_MVP_Prototype.html")
