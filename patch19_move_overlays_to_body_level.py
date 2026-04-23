#!/usr/bin/env python3
"""
Patch 19 — relocate user-profile-overlay, accept-invite-overlay, and
the Preview button wrapper OUT of module-settings into body-level.

Baseline: 3,427,191  (post-Patch 18)
"""
import os, re, sys

TARGET    = 'FyldHub_MVP_Prototype.html'
FORBIDDEN = 'FyldHub_Combined_Prototype.html'

if not os.path.exists(TARGET):
    print(f'ERROR: {TARGET} not found'); sys.exit(1)
if os.path.abspath(TARGET) == os.path.abspath(FORBIDDEN):
    print('ERROR: would overwrite enterprise prototype'); sys.exit(1)

content = open(TARGET).read()
BASELINE = 3_427_191
if len(content) != BASELINE:
    print(f'ERROR: baseline mismatch. Expected {BASELINE:,}, got {len(content):,}'); sys.exit(1)

# ===============================================================
# Step 1 -- Identify the block to move
# ===============================================================
print('\n-- Step 1: Locate misplaced block --')

start_anchor = "<!-- \u2550\u2550\u2550 USER PROFILE OVERLAY (restored from v5) \u2550\u2550\u2550 -->"
start_count = content.count(start_anchor)
if start_count != 1:
    print(f'FAIL: start anchor occurs {start_count} times, expected 1')
    sys.exit(2)
block_start = content.find(start_anchor)

end_marker = "Preview: Accept Invite Flow\n  </button>\n</div>"
end_count = content.count(end_marker)
if end_count != 1:
    print(f'FAIL: end marker occurs {end_count} times, expected 1')
    sys.exit(2)
block_end = content.find(end_marker) + len(end_marker)

block = content[block_start:block_end]
print(f'  Block: {block_start}..{block_end}  ({len(block):,} chars)')
print(f'  First 80:  {block[:80]!r}')
print(f'  Last 80:   {block[-80:]!r}')

assert 'id="user-profile-overlay"' in block, 'block missing user-profile-overlay'
assert 'id="accept-invite-overlay"' in block, 'block missing accept-invite-overlay'
assert 'Preview: Accept Invite Flow' in block, 'block missing preview button'
print(f'  \u2713 All 3 expected elements present')

# ===============================================================
# Step 2 -- Identify the insertion point
# ===============================================================
print('\n-- Step 2: Locate insertion point --')

insert_anchor = '<!-- \u2550\u2550\u2550 WORKERS MODULE \u2550\u2550\u2550 -->'
if content.count(insert_anchor) != 1:
    print(f'FAIL: insert anchor occurs {content.count(insert_anchor)} times')
    sys.exit(2)
insert_pos = content.find(insert_anchor)
print(f'  Insert before <!-- WORKERS MODULE --> @{insert_pos}')
print(f'  Context before: {content[insert_pos-80:insert_pos]!r}')

# ===============================================================
# Step 3 -- Build the new content
# ===============================================================
print('\n-- Step 3: Perform move --')

leading_white_start = block_start
while leading_white_start > 0 and content[leading_white_start-1] in '\n\r\t ':
    leading_white_start -= 1
leading_eaten = content[leading_white_start:block_start]
print(f'  Leading whitespace eaten: {leading_eaten!r}')

trailing_white_end = block_end
while trailing_white_end < len(content) and content[trailing_white_end] in '\n\r\t ':
    trailing_white_end += 1
trailing_eaten = content[block_end:trailing_white_end]
print(f'  Trailing whitespace eaten: {trailing_eaten!r}')

REMOVE_REPLACEMENT = '\n'

before_block = content[:leading_white_start]
after_block_before_insert = content[trailing_white_end:insert_pos]
insert_onwards = content[insert_pos:]

MOVED_BLOCK = (
    '\n\n<!-- \u2550\u2550\u2550 BODY-LEVEL OVERLAYS \u2014 moved out of module-settings by Patch 19 \u2550\u2550\u2550 -->\n'
    + block
    + '\n\n'
)

new_content = before_block + REMOVE_REPLACEMENT + after_block_before_insert + MOVED_BLOCK + insert_onwards

print(f'  Old size: {len(content):,}')
print(f'  New size: {len(new_content):,}')
print(f'  Net \u0394:    {len(new_content) - len(content):+,}')

content = new_content

# ===============================================================
# Step 4 -- Verify move succeeded
# ===============================================================
print('\n-- Step 4: Verify --')

for name, anchor in [
    ('user-profile-overlay', 'id="user-profile-overlay"'),
    ('accept-invite-overlay', 'id="accept-invite-overlay"'),
    ('preview button', 'Preview: Accept Invite Flow'),
]:
    count = content.count(anchor)
    ok = count == 1
    mark = '\u2713' if ok else '\u2717'
    print(f'  {name}: {count}  {mark}')
    if not ok:
        print(f'  ABORT: duplicate or missing after move')
        sys.exit(2)

ms_open = re.search(r'<div[^>]*\bid="module-settings"[^>]*>', content)
if ms_open:
    print(f'\n  module-settings opens @{ms_open.start()}')

print(f'\nFinal size: {len(content):,}  (\u0394 from baseline: {len(content) - BASELINE:+,})')

with open(TARGET, 'w') as f:
    f.write(content)
print('\u2705 Patch 19 applied.')
