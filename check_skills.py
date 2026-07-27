from pathlib import Path
root = Path('.ai/skills')
total = 0
for cat in sorted(root.iterdir()):
    if cat.is_dir():
        files = list(cat.glob('*.md'))
        total += len(files)
        for f in sorted(files):
            size = len(f.read_text(encoding='utf-8'))
            print(f'{cat.name}/{f.name}: {size} chars')
print('---')
print(f'Total skill files: {total}')
readme = root / 'README.md'
template = root / 'SKILL.template.md'
if readme.exists():
    print(f'README: {len(readme.read_text(encoding="utf-8"))} chars')
if template.exists():
    print(f'TEMPLATE: {len(template.read_text(encoding="utf-8"))} chars')
