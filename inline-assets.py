"""
inline-assets.py
Chantier 1 : inline les PNG utilisés en base64
Chantier 2 : patch redirectToStore() avec mraid.open()
Génère index.html (self-contained) à partir de generated-playable.html
"""
import base64, os, re

ROOT   = os.path.dirname(os.path.abspath(__file__))
SRC    = os.path.join(ROOT, 'generated-playable.html')
OUT    = os.path.join(ROOT, 'index.html')
ASSETS = os.path.join(ROOT, 'assets')

# PNGs effectivement dessinés dans le code (wheels, tombstone, plank exclus)
USED_PNGS = [
    ('assets/Background.png',                   'Background.png'),
    ('assets/Blue Castle.png',                   'Blue Castle.png'),
    ('assets/Red Castle.png',                    'Red Castle.png'),
    ('assets/blue_castle_icon.png',              'blue_castle_icon.png'),
    ('assets/red_castle_icon.png',               'red_castle_icon.png'),
    ('assets/Character_Cyclop.png',              'Character_Cyclop.png'),
    ('assets/Character_Skeleton.png',            'Character_Skeleton.png'),
    ('assets/Character_Orc.png',                 'Character_Orc.png'),
    ('assets/Projectile_1.png',                  'Projectile_1.png'),
    ('assets/Projectile_2.png',                  'Projectile_2.png'),
    ('assets/Weapon_1.png',                      'Weapon_1.png'),
    ('assets/Weapon_2.png',                      'Weapon_2.png'),
    ('assets/green_character_selection_box.png', 'green_character_selection_box.png'),
    ('assets/red_character_selection_box.png',   'red_character_selection_box.png'),
    ('assets/skeletton_selection_box.png',       'skeletton_selection_box.png'),
    ('assets/Cartoon_hand.png',                  'Cartoon_hand.png'),
]

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

# ── Chantier 1 : inline PNGs ─────────────────────────────────────────────
print('\nChantier 1 — inlining PNGs...')
for js_path, file_name in USED_PNGS:
    file_path = os.path.join(ASSETS, file_name)
    if not os.path.exists(file_path):
        print(f'  MISSING (skipped): {file_name}')
        continue
    with open(file_path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('ascii')
    data_uri = 'data:image/png;base64,' + b64
    old = f"'{js_path}'"
    new = f"'{data_uri}'"
    if old in html:
        html = html.replace(old, new)
        print(f'  OK   {file_name:<45} ({len(b64)//1024} KB b64)')
    else:
        print(f'  NOT FOUND: {js_path}')

# ── Chantier 2 : MRAID patch ─────────────────────────────────────────────
print('\nChantier 2 — patching redirectToStore()...')
OLD = "function redirectToStore() {\n  window.open(ACTIVE.ui.ctaUrl, '_blank');\n}"
NEW = ("function redirectToStore() {\n"
       "  if (typeof mraid !== 'undefined' && mraid.open) {\n"
       "    mraid.open(ACTIVE.ui.ctaUrl);\n"
       "  } else {\n"
       "    window.open(ACTIVE.ui.ctaUrl, '_blank');\n"
       "  }\n"
       "}")
if OLD in html:
    html = html.replace(OLD, NEW)
    print('  OK   redirectToStore() patched with mraid.open() fallback')
else:
    print('  WARNING: pattern not found — check manually')

remaining = len(re.findall(r'window\.open\(', html))
print(f'  Remaining window.open() calls: {remaining} (inside fallback — OK)')

# ── Écriture ─────────────────────────────────────────────────────────────
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(html)

size_bytes = os.path.getsize(OUT)
size_mb    = size_bytes / 1024 / 1024

print('\n' + '-' * 50)
print(f'Output: index.html  {size_mb:.2f} MB ({size_bytes//1024} KB)')
if size_mb > 5:
    print('WARNING: depasse la limite de 5 MB AppLovin.')
    print('         Compresser les PNG (TinyPNG / WebP) avant de generer les variantes.')
else:
    print('OK: sous la limite de 5 MB.')
print('-' * 50 + '\n')
