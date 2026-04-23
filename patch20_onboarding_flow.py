#!/usr/bin/env python3
"""Patch 20 — Onboarding Flow preview (body-level overlay + checklist widget).
Baseline: 3,427,268 (post-Patch 19)
"""
import os, sys

TARGET    = 'FyldHub_MVP_Prototype.html'
FORBIDDEN = 'FyldHub_Combined_Prototype.html'

if not os.path.exists(TARGET):
    print(f'ERROR: {TARGET} not found'); sys.exit(1)
if os.path.abspath(TARGET) == os.path.abspath(FORBIDDEN):
    print('ERROR: would overwrite enterprise prototype'); sys.exit(1)

content = open(TARGET).read()
BASELINE = 3_427_268
if len(content) != BASELINE:
    print(f'ERROR: baseline mismatch. Expected {BASELINE:,}, got {len(content):,}'); sys.exit(1)

def rep(old, new, label):
    global content
    c = content.count(old)
    if c != 1:
        print(f'FAIL [{label}] count={c}'); sys.exit(2)
    content = content.replace(old, new, 1)
    delta = len(new) - len(old)
    print(f'  OK   [{label}] d={delta:+,}')

# ===============================================================
# BLOCK A — CSS (insert before </style> at line 2820)
# ===============================================================
print('\n-- Block A: CSS --')

CSS_BLOCK = """
/* ═══ ONBOARDING FLOW (Patch 20) ═══ */
.onb-screen { display: none; }
.onb-screen.active { display: block; }
.wiz-progress { display:flex; gap:8px; align-items:center; padding:16px 24px; border-bottom:1px solid var(--border); }
.wiz-progress-step { display:flex; align-items:center; gap:6px; font-size:12px; color:var(--slate); }
.wiz-progress-step.active { color:var(--teal); font-weight:600; }
.wiz-progress-step.done { color:var(--green); }
.wiz-progress-dot { width:22px; height:22px; border-radius:50%; border:2px solid var(--border); display:flex; align-items:center; justify-content:center; font-size:11px; font-weight:700; }
.wiz-progress-step.active .wiz-progress-dot { border-color:var(--teal); background:var(--teal); color:#fff; }
.wiz-progress-step.done .wiz-progress-dot { border-color:var(--green); background:var(--green); color:#fff; }
.wiz-progress-line { width:32px; height:2px; background:var(--border); }
.onb-welcome-hero { display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; padding:64px 32px; background:radial-gradient(ellipse at center, #E0F5F3 0%, #fff 70%); min-height:400px; }
.onb-checklist-widget { background:var(--white); border:1px solid var(--border); border-radius:var(--radius); margin-bottom:20px; overflow:hidden; }
.onb-checklist-hd { padding:16px 20px; border-bottom:1px solid var(--border); display:flex; align-items:center; justify-content:space-between; }
.onb-checklist-hd-title { font-size:15px; font-weight:700; color:var(--dark); }
.onb-checklist-progress { width:100%; height:6px; background:var(--lgray); border-radius:3px; margin-top:10px; }
.onb-checklist-bar { height:6px; background:var(--teal); border-radius:3px; transition:width .3s; }
.onb-checklist-row { display:flex; align-items:center; gap:12px; padding:12px 20px; border-bottom:1px solid var(--lgray); cursor:pointer; transition:background .15s; }
.onb-checklist-row:hover { background:var(--bg); }
.onb-checklist-row:last-child { border-bottom:none; }
.onb-checklist-check { width:20px; height:20px; border-radius:50%; border:2px solid var(--border); display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.onb-checklist-row.completed .onb-checklist-check { border-color:var(--green); background:var(--green); }
.onb-checklist-row.completed .onb-checklist-label { text-decoration:line-through; color:var(--slate); }
.onb-checklist-label { font-size:13px; font-weight:500; color:var(--dark); }
.onb-checklist-arrow { margin-left:auto; color:var(--slate); }

"""

rep('\n</style>', CSS_BLOCK + '</style>', 'CSS insertion')

# ===============================================================
# BLOCK B — HTML overlay + preview button (before WORKERS MODULE)
# ===============================================================
print('\n-- Block B: HTML --')

HTML_BLOCK = """
<!-- ═══ ONBOARDING FLOW OVERLAY (Patch 20) ═══ -->
<div class="wiz-overlay" id="onboarding-overlay">
  <div class="wiz-modal-lg" style="max-width:640px;width:100%;max-height:90vh;overflow-y:auto;border-radius:12px;background:var(--white);position:relative">
    <button onclick="closeOnboarding()" style="position:absolute;top:12px;right:14px;background:none;border:none;font-size:22px;cursor:pointer;color:var(--slate);z-index:2">&times;</button>

    <!-- Progress bar (hidden on welcome) -->
    <div id="onb-progress" style="display:none">
      <div class="wiz-progress">
        <div class="wiz-progress-step active" id="onb-pstep-1"><div class="wiz-progress-dot">1</div><span>Your Profile</span></div>
        <div class="wiz-progress-line" id="onb-pline-1"></div>
        <div class="wiz-progress-step" id="onb-pstep-2"><div class="wiz-progress-dot">2</div><span>Company</span></div>
      </div>
    </div>

    <!-- Screen 0: Welcome -->
    <div class="onb-screen active" id="onb-screen-welcome">
      <div class="onb-welcome-hero">
        <div style="font-size:28px;font-weight:300;color:var(--dark);font-family:Georgia,serif;margin-bottom:8px">Welcome, Amber</div>
        <div style="font-size:15px;color:var(--slate);max-width:420px;line-height:1.6;margin-bottom:28px">Let&rsquo;s set up your FyldHub account. This takes about 2 minutes &mdash; you can always come back and change things later.</div>
        <button class="btn btn-primary" onclick="goOnbStep(1)" style="padding:10px 32px;font-size:14px;font-weight:600;border-radius:8px">Get Started &rarr;</button>
      </div>
    </div>

    <!-- Screen 1: Profile -->
    <div class="onb-screen" id="onb-screen-profile">
      <div style="padding:24px 28px">
        <div style="font-size:18px;font-weight:700;color:var(--dark);margin-bottom:4px">Your Profile</div>
        <div style="font-size:13px;color:var(--slate);margin-bottom:20px">Confirm your details. These are visible to your team.</div>
        <div style="display:flex;flex-direction:column;gap:14px">
          <div style="display:flex;gap:12px">
            <div style="flex:1"><label style="font-size:12px;font-weight:600;color:var(--dark);display:block;margin-bottom:4px">First Name</label><input class="form-control" value="Amber" style="font-size:14px"></div>
            <div style="flex:1"><label style="font-size:12px;font-weight:600;color:var(--dark);display:block;margin-bottom:4px">Last Name</label><input class="form-control" value="McFee" style="font-size:14px"></div>
          </div>
          <div><label style="font-size:12px;font-weight:600;color:var(--dark);display:block;margin-bottom:4px">Email</label><input class="form-control" value="amber@fyldhub.com" style="font-size:14px" readonly></div>
          <div><label style="font-size:12px;font-weight:600;color:var(--dark);display:block;margin-bottom:4px">Job Title (optional)</label><input class="form-control" placeholder="e.g. VP of Marketing" style="font-size:14px"></div>
          <div><label style="font-size:12px;font-weight:600;color:var(--dark);display:block;margin-bottom:4px">Timezone</label><select class="form-control" style="font-size:14px"><option selected>America/New_York (ET)</option><option>America/Chicago (CT)</option><option>America/Denver (MT)</option><option>America/Los_Angeles (PT)</option></select></div>
        </div>
      </div>
    </div>

    <!-- Screen 2: Company -->
    <div class="onb-screen" id="onb-screen-company">
      <div style="padding:24px 28px">
        <div style="font-size:18px;font-weight:700;color:var(--dark);margin-bottom:4px">Company Details</div>
        <div style="font-size:13px;color:var(--slate);margin-bottom:20px">Tell us about your organization. You can update this in Settings later.</div>
        <div style="display:flex;flex-direction:column;gap:14px">
          <div><label style="font-size:12px;font-weight:600;color:var(--dark);display:block;margin-bottom:4px">Company Name</label><input class="form-control" placeholder="Your company name" style="font-size:14px"></div>
          <div><label style="font-size:12px;font-weight:600;color:var(--dark);display:block;margin-bottom:4px">Industry</label><select class="form-control" style="font-size:14px"><option value="" disabled>Select industry...</option><option selected>Adult Beverage</option><option>Non-Adult Beverage</option><option>Food</option><option>Snacks &amp; Confectionery</option><option>Beauty &amp; Personal Care</option><option>Health &amp; Wellness</option><option>Household &amp; Cleaning</option><option>Pet Care</option><option>Baby &amp; Child Care</option><option>Tobacco &amp; Alternatives</option><option>Cannabis</option></select></div>
          <div><label style="font-size:12px;font-weight:600;color:var(--dark);display:block;margin-bottom:4px">Headquarters</label><input class="form-control" placeholder="City, State" style="font-size:14px"></div>
          <div><label style="font-size:12px;font-weight:600;color:var(--dark);display:block;margin-bottom:4px">Website (optional)</label><input class="form-control" placeholder="https://yourcompany.com" style="font-size:14px"></div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <div style="padding:16px 28px;border-top:1px solid var(--border);display:flex;justify-content:space-between;align-items:center" id="onb-footer">
      <button class="btn btn-ghost btn-sm" id="onb-back" onclick="goOnbStep(window._onbStep-1)" style="display:none">Back</button>
      <div></div>
      <button class="btn btn-primary btn-sm" id="onb-continue" onclick="goOnbStep(window._onbStep+1)" style="display:none">Continue &rarr;</button>
      <button class="btn btn-primary btn-sm" id="onb-finish" onclick="finishOnboarding()" style="display:none;background:var(--green);border-color:var(--green)">Complete Setup &check;</button>
    </div>
  </div>
</div>

<!-- Preview button for Onboarding flow (for prototype demo) -->
<div style="position:fixed;bottom:64px;right:20px;z-index:9999">
  <button class="btn btn-outline btn-sm" onclick="openOnboarding()" style="box-shadow:0 2px 8px rgba(0,0,0,.15);background:var(--teal);color:#fff;border-color:var(--teal)">
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
    Preview: Onboarding Flow
  </button>
</div>

"""

rep('<!-- \u2550\u2550\u2550 WORKERS MODULE \u2550\u2550\u2550 -->',
    HTML_BLOCK + '<!-- \u2550\u2550\u2550 WORKERS MODULE \u2550\u2550\u2550 -->',
    'HTML insertion before WORKERS MODULE')

# ===============================================================
# BLOCK C — JavaScript handlers (after goOnboardStep closing brace)
# ===============================================================
print('\n-- Block C: JavaScript --')

JS_ANCHOR = "function goOnboardStep(n) {\n  if (n < 1 || n > 4) return;"
assert content.count(JS_ANCHOR) == 1, f'JS anchor count: {content.count(JS_ANCHOR)}'

# Find end of goOnboardStep function — it ends with "}\n"
idx = content.find(JS_ANCHOR)
# Walk to matching closing brace
depth = 0; i = content.find('{', idx)
while i < len(content):
    if content[i] == '{': depth += 1
    elif content[i] == '}':
        depth -= 1
        if depth == 0:
            fn_end = i + 1
            break
    i += 1

# Insert JS right after goOnboardStep
JS_BLOCK = """

// ═══ ONBOARDING FLOW HANDLERS (Patch 20) ═══
window._onbStep = 0;
window._onboardingChecklistDismissed = false;

function openOnboarding() {
  document.getElementById('onboarding-overlay').classList.add('open');
  document.body.style.overflow = 'hidden';
  goOnbStep(0);
}

function closeOnboarding() {
  document.getElementById('onboarding-overlay').classList.remove('open');
  document.body.style.overflow = '';
}

function goOnbStep(n) {
  if (n < 0 || n > 2) return;
  window._onbStep = n;
  var screens = ['onb-screen-welcome','onb-screen-profile','onb-screen-company'];
  for (var i = 0; i < screens.length; i++) {
    var s = document.getElementById(screens[i]);
    if (s) s.classList.toggle('active', i === n);
  }
  var prog = document.getElementById('onb-progress');
  if (prog) prog.style.display = n === 0 ? 'none' : '';
  // Progress indicators
  for (var j = 1; j <= 2; j++) {
    var ps = document.getElementById('onb-pstep-' + j);
    if (ps) { ps.classList.remove('active','done'); if (j === n) ps.classList.add('active'); else if (j < n) ps.classList.add('done'); }
    var pl = document.getElementById('onb-pline-' + (j));
    if (pl) pl.style.background = j < n ? 'var(--green)' : 'var(--border)';
  }
  // Footer buttons
  var back = document.getElementById('onb-back');
  var cont = document.getElementById('onb-continue');
  var fin  = document.getElementById('onb-finish');
  if (back) back.style.display = n > 0 ? 'inline-flex' : 'none';
  if (cont) cont.style.display = (n > 0 && n < 2) ? 'inline-flex' : 'none';
  if (fin)  fin.style.display  = n === 2 ? 'inline-flex' : 'none';
}

function finishOnboarding() {
  closeOnboarding();
  switchModule('events');
  setTimeout(function() { switchModule('events'); }, 50);
  renderOnboardingChecklist();
  toast('Account setup complete! Your getting-started checklist is on the Dashboard.');
}

function renderOnboardingChecklist() {
  if (window._onboardingChecklistDismissed) return;
  var existing = document.getElementById('onb-checklist-widget');
  if (existing) existing.remove();
  var steps = [
    {key:'profile', label:'Complete your company profile', done:true, action:"switchModule('settings');setTimeout(function(){showTab('coprofile')},100)"},
    {key:'brand', label:'Add your first brand', done:false, action:"switchModule('settings');setTimeout(function(){showTab('cobrands')},100)"},
    {key:'locations', label:'Add your locations', done:false, action:"switchModule('settings');setTimeout(function(){showTab('colocations')},100)"},
    {key:'eventcats', label:'Create event categories', done:false, action:"switchModule('settings');setTimeout(function(){showTab('coeventcats')},100)"},
    {key:'pay', label:'Set worker pay rates', done:false, action:"switchModule('settings');setTimeout(function(){showTab('financials');setTimeout(function(){showSub('financials','pay')},50)},100)"},
    {key:'invite', label:'Invite teammates (optional)', done:false, action:"switchModule('settings');setTimeout(function(){showTab('users')},100)"},
    {key:'event', label:'Create your first event', done:false, action:"switchModule('events')"}
  ];
  var doneCount = steps.filter(function(s){return s.done}).length;
  var pct = Math.round((doneCount / steps.length) * 100);
  var h = '<div class="onb-checklist-widget" id="onb-checklist-widget">';
  h += '<div class="onb-checklist-hd"><div><div class="onb-checklist-hd-title">Getting Started</div><div style="font-size:12px;color:var(--slate);margin-top:2px">' + doneCount + ' of ' + steps.length + ' complete &mdash; ' + pct + '%</div><div class="onb-checklist-progress"><div class="onb-checklist-bar" style="width:' + pct + '%"></div></div></div><button onclick="dismissOnboardingChecklist()" style="background:none;border:none;cursor:pointer;color:var(--slate);font-size:18px;padding:4px" title="Dismiss">&times;</button></div>';
  for (var i = 0; i < steps.length; i++) {
    var s = steps[i];
    h += '<div class="onb-checklist-row' + (s.done ? ' completed' : '') + '" onclick="onboardingChecklistClick(' + i + ')">';
    h += '<div class="onb-checklist-check">' + (s.done ? '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3"><polyline points="20 6 9 17 4 12"></polyline></svg>' : '') + '</div>';
    h += '<div class="onb-checklist-label">' + s.label + '</div>';
    h += '<div class="onb-checklist-arrow"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg></div>';
    h += '</div>';
  }
  h += '</div>';
  // Insert at top of dashboard main area
  var dashMain = document.querySelector('#module-events .page-body') || document.querySelector('#module-events');
  if (dashMain) {
    var wrapper = document.createElement('div');
    wrapper.innerHTML = h;
    dashMain.insertBefore(wrapper.firstChild, dashMain.firstChild);
  }
}

function dismissOnboardingChecklist() {
  window._onboardingChecklistDismissed = true;
  var w = document.getElementById('onb-checklist-widget');
  if (w) w.remove();
}

function onboardingChecklistClick(idx) {
  closeOnboarding();
  var actions = [
    function(){switchModule('settings');setTimeout(function(){showTab('coprofile')},100)},
    function(){switchModule('settings');setTimeout(function(){showTab('cobrands')},100)},
    function(){switchModule('settings');setTimeout(function(){showTab('colocations')},100)},
    function(){switchModule('settings');setTimeout(function(){showTab('coeventcats')},100)},
    function(){switchModule('settings');setTimeout(function(){showTab('financials');setTimeout(function(){showSub('financials','pay')},50)},100)},
    function(){switchModule('settings');setTimeout(function(){showTab('users')},100)},
    function(){switchModule('events')}
  ];
  if (actions[idx]) actions[idx]();
}
"""

content = content[:fn_end] + JS_BLOCK + content[fn_end:]
print(f'  OK   [JS handlers] d=+{len(JS_BLOCK):,}')

# ===============================================================
# Final verification
# ===============================================================
print('\n-- Final verification --')

checks = {
    'onboarding-overlay': content.count('id="onboarding-overlay"'),
    'openOnboarding def': content.count('function openOnboarding()'),
    'closeOnboarding def': content.count('function closeOnboarding()'),
    'goOnbStep def': content.count('function goOnbStep('),
    'finishOnboarding def': content.count('function finishOnboarding()'),
    'renderOnboardingChecklist def': content.count('function renderOnboardingChecklist()'),
    'Preview: Onboarding Flow': content.count('Preview: Onboarding Flow'),
    'onb-screen-welcome': content.count('id="onb-screen-welcome"'),
    'onb-screen-profile': content.count('id="onb-screen-profile"'),
    'onb-screen-company': content.count('id="onb-screen-company"'),
    'CSS .onb-screen': content.count('.onb-screen {'),
    'CSS .onb-checklist-widget': content.count('.onb-checklist-widget {'),
}
all_ok = True
for k, v in checks.items():
    ok = v == 1
    mark = '\u2713' if ok else '\u2717'
    print(f'  {k}: {v}  {mark}')
    if not ok: all_ok = False

if not all_ok:
    print('\nABORT: verification failed')
    sys.exit(2)

delta = len(content) - BASELINE
print(f'\nFinal size: {len(content):,}  (\u0394 from baseline: {delta:+,})')

with open(TARGET, 'w') as f:
    f.write(content)
print('\u2705 Patch 20 applied.')
