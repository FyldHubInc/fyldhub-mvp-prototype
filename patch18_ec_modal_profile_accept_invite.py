#!/usr/bin/env python3
"""
Patch 18 — three coordinated UX fixes.

Block A — Event Categories Add Category modal
  A.1  ecShowModal -> use .open class (aligns with working cascade pattern)
  A.2  ecCloseModal -> remove .open class
  A.3  renderEC -> add empty-state card below legend when EC_DATA is empty

Block B — Avatar menu: My Profile wired to the wrong modal
  B.1  Replace 4-item block (openMyAccount profile/security/notifications/appearance)
       with single 'My Profile & Security' calling openUserProfile().

Block C — Preview: Accept Invite Flow button does nothing
  C.1  Insert openAcceptInvite(), closeAcceptInvite(), goOnboardStep()

Baseline : 3,426,457  (post-Patch 17C, commit 5ca21e5)
"""
import os, re, sys

TARGET    = 'FyldHub_MVP_Prototype.html'
FORBIDDEN = 'FyldHub_Combined_Prototype.html'

if not os.path.exists(TARGET):
    print(f'ERROR: {TARGET} not found'); sys.exit(1)
if os.path.abspath(TARGET) == os.path.abspath(FORBIDDEN):
    print('ERROR: would overwrite enterprise prototype'); sys.exit(1)

content = open(TARGET).read()
BASELINE = 3_426_457
if len(content) != BASELINE:
    print(f'ERROR: baseline mismatch. Expected {BASELINE:,}, got {len(content):,}'); sys.exit(1)

def rep(buf, old, new, label, expected_count=1):
    count = buf.count(old)
    if count != expected_count:
        print(f'  FAIL [{label}] count={count}, expected={expected_count}')
        return None
    delta = (len(new) - len(old)) * count
    print(f'  OK   [{label}] \u0394={delta:+}')
    return buf.replace(old, new)

# ===============================================================
# BLOCK A -- Event Categories modal + empty-state
# ===============================================================
print('\n\u2500\u2500 Block A: Event Categories \u2500\u2500')

# A.1 -- ecShowModal: add .open class
ECSHOW_OLD = """function ecShowModal(title, bodyHtml, onSave) {
  var modal = document.getElementById('ec-modal-ov');
  document.getElementById('ec-modal-title').textContent = title;
  document.getElementById('ec-modal-body').innerHTML = bodyHtml;
  document.getElementById('ec-modal-save').onclick = onSave;
  modal.style.display = 'flex';
  document.body.style.overflow = 'hidden';
}"""
ECSHOW_NEW = """function ecShowModal(title, bodyHtml, onSave) {
  var modal = document.getElementById('ec-modal-ov');
  document.getElementById('ec-modal-title').textContent = title;
  document.getElementById('ec-modal-body').innerHTML = bodyHtml;
  document.getElementById('ec-modal-save').onclick = onSave;
  modal.classList.add('open');
  modal.style.display = 'flex';
  document.body.style.overflow = 'hidden';
}"""
out = rep(content, ECSHOW_OLD, ECSHOW_NEW, 'A.1 ecShowModal add .open')
if out is None: print('ABORT: A.1'); sys.exit(2)
content = out

# A.2 -- ecCloseModal: remove .open class + reset display
ECCLOSE_OLD = """function ecCloseModal() {
  document.getElementById('ec-modal-ov').style.display = 'none';
  document.body.style.overflow = '';
}"""
ECCLOSE_NEW = """function ecCloseModal() {
  var modal = document.getElementById('ec-modal-ov');
  modal.classList.remove('open');
  modal.style.display = 'none';
  document.body.style.overflow = '';
}"""
out = rep(content, ECCLOSE_OLD, ECCLOSE_NEW, 'A.2 ecCloseModal remove .open')
if out is None: print('ABORT: A.2'); sys.exit(2)
content = out

# A.3 -- renderEC: add empty-state card when EC_DATA is empty
A3_OLD = "</div>'+EC_DATA.map(catBlock).join('');"
A3_NEW = (
    "</div>'"
    "+(EC_DATA.length===0"
      "?'<div style=\"background:var(--white);border:1px solid var(--border);border-radius:var(--radius);padding:48px 24px;text-align:center\">"
        "<div style=\"font-size:15px;font-weight:600;color:var(--dark);margin-bottom:6px\">No categories yet</div>"
        "<div style=\"font-size:14px;color:var(--slate);margin-bottom:16px\">Create your first event category to start organizing activations, audits, and deliveries.</div>"
        "<button class=\"btn btn-primary btn-sm\" onclick=\"ecOpenAddCat()\">+ Add Category</button>"
      "</div>'"
      ":EC_DATA.map(catBlock).join(''));"
)
out = rep(content, A3_OLD, A3_NEW, 'A.3 renderEC empty-state')
if out is None: print('ABORT: A.3'); sys.exit(2)
content = out

# ===============================================================
# BLOCK B -- Avatar menu rewire
# ===============================================================
print('\n\u2500\u2500 Block B: Avatar menu \u2500\u2500')

B_OLD = (
    '<div class="acct-menu-item" onclick="closeAcctMenu();openMyAccount(\'profile\')">'
    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
    '<path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>My Profile</div>\n'
    '          <div class="acct-menu-item" onclick="closeAcctMenu();openMyAccount(\'security\')">'
    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
    '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0110 0v4"/></svg>Security &amp; MFA</div>\n'
    '          <div class="acct-menu-item" onclick="closeAcctMenu();openMyAccount(\'notifications\')">'
    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
    '<path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 01-3.46 0"/></svg>Notifications</div>\n'
    '          <div class="acct-menu-item" onclick="closeAcctMenu();openMyAccount(\'appearance\')">'
    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
    '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/></svg>Appearance</div>'
)

B_NEW = (
    '<div class="acct-menu-item" onclick="closeAcctMenu();openUserProfile()">'
    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
    '<path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>My Profile &amp; Security</div>'
)

out = rep(content, B_OLD, B_NEW, 'B.1 avatar menu consolidate')
if out is None: print('ABORT: B.1'); sys.exit(2)
content = out

# ===============================================================
# BLOCK C -- Restore Accept Invite handlers
# ===============================================================
print('\n\u2500\u2500 Block C: Accept Invite handlers \u2500\u2500')

C_OLD = (
    "function closeUserProfile() {\n"
    "  document.getElementById('user-profile-overlay').classList.remove('open');\n"
    "  document.body.style.overflow = '';\n"
    "}\n"
    "\n"
    "// -- ACCEPT INVITE ONBOARDING --------------------------------------\n"
    "window._onboardStep = 1;\n"
)

C_NEW = (
    "function closeUserProfile() {\n"
    "  document.getElementById('user-profile-overlay').classList.remove('open');\n"
    "  document.body.style.overflow = '';\n"
    "}\n"
    "\n"
    "// -- ACCEPT INVITE ONBOARDING --------------------------------------\n"
    "window._onboardStep = 1;\n"
    "\n"
    "function openAcceptInvite() {\n"
    "  document.getElementById('accept-invite-overlay').classList.add('open');\n"
    "  document.body.style.overflow = 'hidden';\n"
    "  goOnboardStep(1);\n"
    "}\n"
    "\n"
    "function closeAcceptInvite() {\n"
    "  document.getElementById('accept-invite-overlay').classList.remove('open');\n"
    "  document.body.style.overflow = '';\n"
    "}\n"
    "\n"
    "function goOnboardStep(n) {\n"
    "  if (n < 1 || n > 4) return;\n"
    "  window._onboardStep = n;\n"
    "  for (var i = 1; i <= 4; i++) {\n"
    "    var sec = document.getElementById('ob-sec-' + i);\n"
    "    var tab = document.getElementById('ob-tab-' + i);\n"
    "    if (sec) sec.classList.toggle('active', i === n);\n"
    "    if (tab) {\n"
    "      tab.classList.remove('active','done');\n"
    "      if (i === n) tab.classList.add('active');\n"
    "      else if (i < n) tab.classList.add('done');\n"
    "    }\n"
    "  }\n"
    "  var back = document.getElementById('ob-back');\n"
    "  var next = document.getElementById('ob-next');\n"
    "  var done = document.getElementById('ob-done');\n"
    "  if (back) back.style.display = n > 1 ? 'inline-flex' : 'none';\n"
    "  if (next) next.style.display = n < 4 ? 'inline-flex' : 'none';\n"
    "  if (done) done.style.display = n === 4 ? 'inline-flex' : 'none';\n"
    "}\n"
)

out = rep(content, C_OLD, C_NEW, 'C.1 insert accept-invite handlers')
if out is None: print('ABORT: C.1'); sys.exit(2)
content = out

# ===============================================================
# Final verification
# ===============================================================
print('\n\u2500\u2500 Final verification \u2500\u2500')

for fn in ['openAcceptInvite', 'closeAcceptInvite', 'goOnboardStep']:
    defns = len(re.findall(rf'function\s+{fn}\s*\(', content))
    mark = '\u2713' if defns == 1 else '\u2717'
    print(f'  {fn} definitions: {defns}  {mark}')

for needle in ["modal.classList.add('open');", "modal.classList.remove('open');"]:
    mark = '\u2713' if needle in content else '\u2717'
    print(f'  Contains {needle!r}: {mark}')

print(f'  openMyAccount( calls remaining: {content.count("openMyAccount(")}  (should be 1: the function decl itself)')
print(f'  openUserProfile() callers: {content.count("openUserProfile()")}')

mark = '\u2713' if 'No categories yet' in content else '\u2717'
print(f'  Contains empty state string: {mark}')

print(f'\nFinal size: {len(content):,}  (\u0394 from baseline: {len(content) - BASELINE:+,})')

with open(TARGET, 'w') as f:
    f.write(content)
print('\u2705 Patch 18 applied.')
