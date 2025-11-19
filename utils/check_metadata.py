import json

with open('presentation.ipynb', 'r') as f:
    nb = json.load(f)

print(json.dumps(nb.get('metadata', {}), indent=2))
