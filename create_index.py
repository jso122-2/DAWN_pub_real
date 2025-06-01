"""
Simple HTML index creator for DAWN visualizations
No emojis to avoid encoding issues
"""

from pathlib import Path
from datetime import datetime

# Set up paths
visual_output = Path("visual_output")

# Start building HTML
html_content = """<!DOCTYPE html>
<html>
<head>
    <title>DAWN Unified Visualization Output</title>
    <style>
        body { 
            font-family: 'Courier New', monospace; 
            margin: 20px; 
            background: #0a0a0a; 
            color: #00ffaa;
        }
        h1 { 
            color: #ff00ff; 
            text-shadow: 0 0 10px #ff00ff;
        }
        h2 { 
            color: #00ffff; 
            margin-top: 30px;
        }
        .gallery { 
            display: grid; 
            grid-template-columns: repeat(auto-fill, minmax(400px, 1fr)); 
            gap: 20px; 
            margin-top: 20px;
        }
        .image-card { 
            background: #1a1a1a; 
            padding: 10px; 
            border-radius: 8px; 
            border: 1px solid #00ffaa;
            transition: transform 0.2s;
        }
        .image-card:hover {
            transform: scale(1.05);
            border-color: #ff00ff;
            box-shadow: 0 0 20px #ff00ff;
        }
        img { 
            width: 100%; 
            height: auto; 
            border-radius: 4px; 
        }
        .title { 
            color: #00ffaa; 
            margin-top: 10px; 
            font-size: 14px;
        }
        .timestamp {
            color: #666;
            font-size: 12px;
            margin-top: 5px;
        }
        .stats {
            color: #ff00ff;
            margin: 20px 0;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <h1>DAWN Unified Visualization Output</h1>
    <div class="timestamp">Generated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</div>
"""

# Organize by category
categories = {
    "Drift Dynamics": "drift",
    "Entropy Analysis": "entropy", 
    "Bloom Evolution": "bloom",
    "Belief Systems": "belief",
    "Decay Patterns": "decay",
    "Coherence Fields": "coherence",
    "Mood Dynamics": "mood",
    "Pulse Patterns": "pulse"
}

total_images = 0

for category_name, folder in categories.items():
    folder_path = visual_output / folder
    if folder_path.exists():
        images = list(folder_path.glob("*.png")) + list(folder_path.glob("*.gif"))
        if images:
            total_images += len(images)
            html_content += f'<h2>{category_name} ({len(images)} visualizations)</h2><div class="gallery">'
            for img in sorted(images):
                rel_path = img.relative_to(visual_output).as_posix()
                title = img.stem.replace("_", " ").title()
                html_content += f'''
                <div class="image-card">
                    <img src="{rel_path}" alt="{img.name}">
                    <div class="title">{title}</div>
                </div>
                '''
            html_content += '</div>'

# Also check root output directory
root_images = list(visual_output.glob("*.png"))
if root_images:
    total_images += len(root_images)
    html_content += f'<h2>Other Visualizations ({len(root_images)} files)</h2><div class="gallery">'
    for img in sorted(root_images):
        rel_path = img.name
        title = img.stem.replace("_", " ").title()
        html_content += f'''
        <div class="image-card">
            <img src="{rel_path}" alt="{img.name}">
            <div class="title">{title}</div>
        </div>
        '''
    html_content += '</div>'

# Add stats at the top
stats_html = f'<div class="stats">Total Visualizations: {total_images}</div>'
html_content = html_content.replace('<div class="timestamp">', stats_html + '<div class="timestamp">')

html_content += """
</body>
</html>
"""

# Write the HTML file with UTF-8 encoding
index_path = visual_output / "index.html"
try:
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"SUCCESS: Created index at: {index_path}")
    print(f"Total visualizations indexed: {total_images}")
    print(f"\nOpen this file in your browser:")
    print(f"  {index_path.absolute()}")
except Exception as e:
    print(f"Error creating index: {e}")
    # Try again with ASCII only
    html_ascii = html_content.encode('ascii', 'ignore').decode('ascii')
    with open(index_path, 'w') as f:
        f.write(html_ascii)
    print("Created index with ASCII-only content")