#!/usr/bin/env python3
"""Patch 20.1 — Fix finishOnboarding dashboard nav + checklist target + row hover."""
import os, sys

TARGET    = 'FyldHub_MVP_Prototype.html'
FORBIDDEN = 'FyldHub_Combined_Prototype.html'

if not os.path.exists(TARGET):
    print(f'ERROR: {TARGET} not found'); sys.exit(1)
if os.path.abspath(TARGET) == os.path.abspath(FORBIDDEN):
    print('ERROR: would overwrite enterprise prototype'); sys.exit(1)

content = open(TARGET).read()
baseline = len(content)
print(f'Starting: {baseline:,} chars')

def rep(old, new, label):
    global content
    c = content.count(old)
    if c != 1:
        print(f'FAIL [{label}] count={c}'); sys.exit(2)
    content = content.replace(old, new, 1)
    print(f'  OK   [{label}] d={len(new)-len(old):+,}')

# ── Fix 1: finishOnboarding → switchModule('dashboard') ──
print('\n-- Fix 1: finishOnboarding --')

rep(
    "function finishOnboarding() {\n"
    "  closeOnboarding();\n"
    "  switchModule('events');\n"
    "  setTimeout(function() { switchModule('events'); }, 50);\n"
    "  renderOnboardingChecklist();\n"
    "  toast('Account setup complete! Your getting-started checklist is on the Dashboard.');\n"
    "}",
    "function finishOnboarding() {\n"
    "  closeOnboarding();\n"
    "  switchModule('dashboard');\n"
    "  setTimeout(function() { renderOnboardingChecklist(); }, 100);\n"
    "  toast('Account setup complete! Your getting-started checklist is on the Dashboard.');\n"
    "}",
    'finishOnboarding nav fix'
)

# ── Fix 2: renderOnboardingChecklist → target #module-dashboard ──
print('\n-- Fix 2: renderOnboardingChecklist target --')

rep(
    "  // Insert at top of dashboard main area\n"
    "  var dashMain = document.querySelector('#module-events .page-body') || document.querySelector('#module-events');\n"
    "  if (dashMain) {\n"
    "    var wrapper = document.createElement('div');\n"
    "    wrapper.innerHTML = h;\n"
    "    dashMain.insertBefore(wrapper.firstChild, dashMain.firstChild);\n"
    "  }",
    "  // Insert at top of Dashboard main area (by specific ID)\n"
    "  var dashMod = document.getElementById('module-dashboard');\n"
    "  if (dashMod) {\n"
    "    var target = dashMod.querySelector('.page-body') || dashMod;\n"
    "    var wrapper = document.createElement('div');\n"
    "    wrapper.innerHTML = h;\n"
    "    target.insertBefore(wrapper.firstChild, target.firstChild);\n"
    "  }",
    'renderOnboardingChecklist dashboard target'
)

# ── Fix 3: CSS hover state for checklist rows ──
print('\n-- Fix 3: checklist row hover CSS --')

rep(
    '.onb-checklist-row:hover { background:var(--bg); }',
    '.onb-checklist-row:hover { background:var(--bg); cursor:pointer; }',
    'checklist row hover cursor'
)

# ── Verify ──
print('\n-- Verification --')

# finishOnboarding uses switchModule('dashboard')
assert "switchModule('dashboard')" in content, 'dashboard switch missing'
print("  switchModule('dashboard') in finishOnboarding: YES")

# renderOnboardingChecklist targets #module-dashboard
assert "getElementById('module-dashboard')" in content, 'dashboard target missing'
print("  getElementById('module-dashboard') in renderChecklist: YES")

# onboardingChecklistClick still calls closeOnboarding + correct targets
assert "function onboardingChecklistClick(idx)" in content
for target in ["showTab('coprofile')", "showTab('cobrands')", "showTab('colocations')",
               "showTab('coeventcats')", "showTab('financials')", "showSub('financials','pay')",
               "showTab('users')", "switchModule('events')"]:
    assert target in content, f'{target} missing from checklist click handler'
print("  All 7 checklist click targets present: YES")

# closeOnboarding called before navigation
assert content.find('function onboardingChecklistClick') < content.find("closeOnboarding();\n  var actions")
print("  closeOnboarding() before navigation in click handler: YES")

# cursor:pointer on hover
assert 'cursor:pointer' in content
print("  cursor:pointer on hover: YES")

delta = len(content) - baseline
print(f'\nFinal size: {len(content):,}  (d from start: {delta:+,})')

with open(TARGET, 'w') as f:
    f.write(content)
print('\u2705 Patch 20.1 applied.')
