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
BASELINE = 3831888
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

# ─── PATCH 8A: Zero out APP_DATA brands ─────────────────────────
rep(
    "  brands: [\n"
    "    { id:'bacrm', name:'BACARD\u00cd Rum', active:true, products:[{n:'Superior',sz:'750mL',pk:'Single',p:'$18.99'},{n:'Superior',sz:'1.75L',pk:'Single',p:'$29.99'},{n:'Gold',sz:'750mL',pk:'Single',p:'$17.99'},{n:'Gold',sz:'1.75L',pk:'Single',p:'$27.99'},{n:'Black',sz:'750mL',pk:'Single',p:'$21.99'},{n:'Spiced',sz:'750mL',pk:'Single',p:'$19.99'},{n:'Coconut',sz:'750mL',pk:'Single',p:'$17.99'}] },\n"
    "    { id:'bacrtd', name:'BACARD\u00cd RTD', active:true, products:[{n:'Sunset',sz:'355mL',pk:'Single',p:'$2.99'},{n:'Sunset',sz:'355mL',pk:'12-pack',p:'$2.99'},{n:'Lim\u00f3n',sz:'355mL',pk:'Single',p:'$2.99'},{n:'Lim\u00f3n',sz:'355mL',pk:'12-pack',p:'$2.99'}] },\n"
    "    { id:'patron', name:'PATR\u00d3N', active:true, products:[{n:'Silver',sz:'750mL',pk:'Single',p:'$42.99'},{n:'Silver',sz:'1.75L',pk:'Single',p:'$74.99'},{n:'Reposado',sz:'750mL',pk:'Single',p:'$47.99'},{n:'A\u00f1ejo',sz:'750mL',pk:'Single',p:'$52.99'}] }\n"
    "  ],",
    "  brands: [],",
    "APP_DATA: zero out brands"
)

# ─── PATCH 8B: Zero out APP_DATA programs ───────────────────────
rep(
    "  programs: [\n"
    "    { id:'p1', name:'BACARD\u00cd Rum Off-Premise 2026', brand:'BACARD\u00cd Rum', channel:'Off-Premise', active:true },\n"
    "    { id:'p2', name:'BACARD\u00cd RTD Summer Push', brand:'BACARD\u00cd RTD', channel:'Off-Premise', active:true },\n"
    "    { id:'p3', name:'PATR\u00d3N On-Premise Elite', brand:'PATR\u00d3N', channel:'On-Premise', active:true },\n"
    "    { id:'p4', name:'Total Wine National Demo Program', brand:'BACARD\u00cd Rum', channel:'Off-Premise', active:true }\n"
    "  ],",
    "  programs: [],",
    "APP_DATA: zero out programs"
)

# ─── PATCH 8C: Zero out APP_DATA locations ──────────────────────
rep(
    "  locations: [\n"
    "    { id:'loc1', name:'Total Wine & More #1205', city:'Boston, MA', region:'Northeast/Boston', chain:'Total Wine' },\n"
    "    { id:'loc2', name:'Total Wine & More #892', city:'Tampa, FL', region:'Southeast/Tampa', chain:'Total Wine' },\n"
    "    { id:'loc3', name:'Kroger Marketplace #447', city:'Natick, MA', region:'Northeast/Boston', chain:'Kroger' },\n"
    "    { id:'loc4', name:'BevMo! #312', city:'Providence, RI', region:'Northeast/Providence', chain:'BevMo' },\n"
    "    { id:'loc5', name:\"Spec's #88\", city:'Houston, TX', region:'South/Houston', chain:\"Spec's\" },\n"
    "    { id:'loc6', name:\"Binny's #14\", city:'Chicago, IL', region:'Midwest/Chicago', chain:\"Binny's\" }\n"
    "  ],",
    "  locations: [],",
    "APP_DATA: zero out locations"
)

# ─── PATCH 8D: Zero out APP_DATA kitTemplates ───────────────────
rep(
    "  kitTemplates: [\n"
    "    { id:'kt1', name:'Standard Sampling Kit', hub:'Activations', active:true },\n"
    "    { id:'kt2', name:'Premium Kit', hub:'Activations', active:true },\n"
    "    { id:'kt3', name:'Planogram Kit', hub:'Merchandising', active:true }\n"
    "  ],",
    "  kitTemplates: [],",
    "APP_DATA: zero out kitTemplates"
)

# ─── PATCH 8E: Zero out APP_DATA budgets ────────────────────────
rep(
    "  budgets: [\n"
    "    {id:'bud-bacrm',brand:'BACARD\u00cd Rum',name:'Brand Activation 2026',type:'top',period:'Annual',year:2026,amount:500000,spent:0,overspendPolicy:'warn',parentId:null},\n"
    "    {id:'bud-bacrm-op',brand:'BACARD\u00cd Rum',name:'Off-Premise National',type:'pool',channel:'Off-Premise',territory:'National',amount:300000,spent:0,overspendPolicy:'warn',parentId:'bud-bacrm',owner:'Jordan L.'},\n"
    "    {id:'bud-bacrm-op-kroger',brand:'BACARD\u00cd Rum',name:'Kroger Summer Demo Series',type:'pool',channel:'Off-Premise',territory:'National',program:'Kroger Summer Demo Series',amount:40000,spent:0,overspendPolicy:'warn',parentId:'bud-bacrm-op'},\n"
    "    {id:'bud-bacrm-op-tw',brand:'BACARD\u00cd Rum',name:'Total Wine National Demo Program',type:'pool',channel:'Off-Premise',territory:'National',program:'Total Wine National Demo Program',amount:32000,spent:0,overspendPolicy:'warn',parentId:'bud-bacrm-op'},\n"
    "    {id:'bud-bacrm-op-gen',brand:'BACARD\u00cd Rum',name:'General Off-Premise Pool',type:'pool',channel:'Off-Premise',territory:'National',amount:228000,spent:0,overspendPolicy:'warn',parentId:'bud-bacrm-op'},\n"
    "    {id:'bud-bacrm-onp',brand:'BACARD\u00cd Rum',name:'On-Premise National',type:'pool',channel:'On-Premise',territory:'National',amount:120000,spent:0,overspendPolicy:'warn',parentId:'bud-bacrm',owner:'Riley P.'},\n"
    "    {id:'bud-bacrm-spec',brand:'BACARD\u00cd Rum',name:'Special Events National',type:'pool',channel:'Special',territory:'National',amount:80000,spent:0,overspendPolicy:'warn',parentId:'bud-bacrm',owner:'Alex Morgan'},\n"
    "    {id:'bud-patron',brand:'PATR\u00d3N',name:'Brand Activation 2026',type:'top',period:'Annual',year:2026,amount:425000,spent:0,overspendPolicy:'warn',parentId:null},\n"
    "    {id:'bud-patron-op',brand:'PATR\u00d3N',name:'Off-Premise National',type:'pool',channel:'Off-Premise',territory:'National',amount:200000,spent:0,overspendPolicy:'warn',parentId:'bud-patron',owner:'Jordan L.'},\n"
    "    {id:'bud-patron-onp',brand:'PATR\u00d3N',name:'On-Premise Spring Push',type:'pool',channel:'On-Premise',territory:'National',program:'On-Premise Spring Push',amount:35000,spent:0,overspendPolicy:'warn',parentId:'bud-patron',owner:'Riley P.'},\n"
    "    {id:'bud-bacrtd',brand:'BACARD\u00cd RTD',name:'Brand Activation 2026',type:'top',period:'Annual',year:2026,amount:310000,spent:0,overspendPolicy:'warn',parentId:null},\n"
    "    {id:'bud-bacrtd-op',brand:'BACARD\u00cd RTD',name:'Off-Premise Summer Push',type:'pool',channel:'Off-Premise',territory:'National',amount:310000,spent:0,overspendPolicy:'warn',parentId:'bud-bacrtd'}\n"
    "  ],",
    "  budgets: [],",
    "APP_DATA: zero out budgets"
)

# ─── PATCH 8F: Zero out APP_DATA licenses ───────────────────────
rep(
    "  licenses: [\n"
    "    { type:'TTB Importer',     num:'US12345',    status:'Verified', expiry:'' },\n"
    "    { type:'FL DABT License',  num:'AB1234567',  status:'Active',   expiry:'' },\n"
    "    { type:'TX TABC Permit',   num:'TX-98765',   status:'Pending',  expiry:'' }\n"
    "  ]",
    "  licenses: []",
    "APP_DATA: zero out licenses"
)

# ─── PATCH 8G: Zero out APP_DATA currentPlan addOns ────────────
rep(
    "  currentPlan: { tier:'Enterprise', hubs:['Activations','Merchandising','On-Demand'], addOns:['fyldcard','logistics','benchmarking','predictive-performance','pos-correlation'] },",
    "  currentPlan: { tier:'Launch', hubs:['Activations'], addOns:[] },",
    "APP_DATA: reset currentPlan to Launch/Activations only"
)

# ─── PATCH 8H: Zero out APP_DATA parentCategories ───────────────
rep(
    "  parentCategories: ['Adult Beverage'],",
    "  parentCategories: [],",
    "APP_DATA: zero out parentCategories"
)

# ─── PATCH 8I: Zero out EV array (events) ───────────────────────
ev_match = re.search(r'var EV=\[.*?\];', content, re.DOTALL)
if ev_match:
    old_ev = ev_match.group(0)
    count = content.count(old_ev)
    if count == 1:
        content = content.replace(old_ev, "var EV=[];", 1)
        print("\u2713 Patched: EV array zeroed out (regex)")
    else:
        print(f"WARNING: EV array found {count} times, skipping")
else:
    print("WARNING: EV array not found via regex, skipping")

# ─── PATCH 8J: Zero out WORKERS array ───────────────────────────
workers_match = re.search(r'var WORKERS = \[.*?\];', content, re.DOTALL)
if workers_match:
    old_workers = workers_match.group(0)
    count = content.count(old_workers)
    if count == 1:
        content = content.replace(old_workers, "var WORKERS = [];", 1)
        print("\u2713 Patched: WORKERS array zeroed out")
    else:
        print(f"WARNING: WORKERS match found {count} times, skipping")
else:
    print("WARNING: WORKERS array not found via regex, skipping")

# ─── WRITE OUTPUT ───────────────────────────────────────────────
open(TARGET, "w", encoding="utf-8").write(content)
final_len = len(open(TARGET, "r", encoding="utf-8").read())
print(f"\n\u2713 Patch 8 complete. New char count: {final_len}")
print("  Run: node --check FyldHub_MVP_Prototype.html")
