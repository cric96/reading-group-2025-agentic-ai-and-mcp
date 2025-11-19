import json

notebook_path = 'presentation.ipynb'

with open(notebook_path, 'r') as f:
    nb = json.load(f)

if 'metadata' not in nb:
    nb['metadata'] = {}

# Enhanced configuration
nb['metadata']['rise'] = {
    "theme": "simple", # Clean theme, good for custom CSS
    "transition": "slide", # Dynamic transition
    "width": "100%", # Maximize space
    "height": "100%",
    "scroll": True,
    "enable_chalkboard": False,
    "slideNumber": True,
    "center": True, # Top align content usually looks better with full width
}

with open(notebook_path, 'w') as f:
    json.dump(nb, f, indent=1)

print("RISE configuration updated with better styling.")
