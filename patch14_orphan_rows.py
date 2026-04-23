#!/usr/bin/env python3
"""Patch 14 — Remove orphaned brand-expand product rows + mangled Brand Resources comment fragment."""
import os, sys

TARGET    = 'FyldHub_MVP_Prototype.html'
FORBIDDEN = 'FyldHub_Combined_Prototype.html'

if not os.path.exists(TARGET):
    print(f'ERROR: {TARGET} not found'); sys.exit(1)
if os.path.abspath(TARGET) == os.path.abspath(FORBIDDEN):
    print('ERROR: would overwrite enterprise prototype'); sys.exit(1)

content = open(TARGET).read()

BASELINE = 3_682_741
if len(content) != BASELINE:
    print(f'ERROR: baseline mismatch. Expected {BASELINE:,}, got {len(content):,}'); sys.exit(1)

START_KEEP = '            </tbody></table>\n'
END_KEEP   = '<!-- \u2550\u2550\u2550 BRAND RESOURCES \u2550'
REPLACEMENT = '      </div>\n    </div>\n</div>\n\n'

# Assert both anchors are unique
assert content.count(START_KEEP) == 1, f'START_KEEP not unique: {content.count(START_KEEP)}'
assert content.count(END_KEEP)   == 1, f'END_KEEP not unique: {content.count(END_KEEP)}'

idx_s = content.find(START_KEEP) + len(START_KEEP)
idx_e = content.find(END_KEEP)

assert idx_e > idx_s, 'END_KEEP appears before START_KEEP'

patched = content[:idx_s] + REPLACEMENT + content[idx_e:]

EXPECTED = 3_648_247
if len(patched) != EXPECTED:
    print(f'ERROR: patched size mismatch. Expected {EXPECTED:,}, got {len(patched):,}'); sys.exit(1)

with open(TARGET, 'w') as f:
    f.write(patched)

print(f'\u2705 Patch 14 applied. {BASELINE:,} \u2192 {len(patched):,} ({len(patched)-BASELINE:+,} chars)')
