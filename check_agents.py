from pathlib import Path
agents = sorted(Path('.ai/agents').glob('*.md'), key=lambda a: len(a.read_text(encoding='utf-8')))
for a in agents[:5]:
    print(f'{a.name}: {len(a.read_text(encoding="utf-8"))} chars')
