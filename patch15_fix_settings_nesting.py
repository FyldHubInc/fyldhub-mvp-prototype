#!/usr/bin/env python3
"""Patch 15 — Close tab-financials before tab-users to un-nest 10 settings panels."""
import os, sys

TARGET    = 'FyldHub_MVP_Prototype.html'
FORBIDDEN = 'FyldHub_Combined_Prototype.html'

if not os.path.exists(TARGET):
    print(f'ERROR: {TARGET} not found'); sys.exit(1)
if os.path.abspath(TARGET) == os.path.abspath(FORBIDDEN):
    print('ERROR: would overwrite enterprise prototype'); sys.exit(1)

content = open(TARGET).read()

BASELINE = 3_648_247
if len(content) != BASELINE:
    print(f'ERROR: baseline mismatch. Expected {BASELINE:,}, got {len(content):,}'); sys.exit(1)

# Anchor: exact sequence right before USERS section comment
# Current state has 3 </div> here; we need 4 to also close tab-financials.
ANCHOR      = '</div>\n\n  </div>\n\n\n\n</div>\n<!-- \u2550\u2550\u2550 USERS \u2550'
REPLACEMENT = '</div>\n\n  </div>\n\n\n\n</div>\n</div>\n<!-- \u2550\u2550\u2550 USERS \u2550'

assert content.count(ANCHOR) == 1, f'Anchor not unique: {content.count(ANCHOR)}'

patched = content.replace(ANCHOR, REPLACEMENT, 1)

EXPECTED = 3_648_254
if len(patched) != EXPECTED:
    print(f'ERROR: patched size mismatch. Expected {EXPECTED:,}, got {len(patched):,}'); sys.exit(1)

with open(TARGET, 'w') as f:
    f.write(patched)

print(f'\u2705 Patch 15 applied. {BASELINE:,} \u2192 {len(patched):,} ({len(patched)-BASELINE:+,} chars)')
print('   Unnested 10 settings tab-panels from tab-financials.')
