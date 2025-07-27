import os
import re
glob_dir = 'backend/visual'

# Patch FuncAnimation frames
funcanim_pattern = re.compile(r'(animation\.FuncAnimation\([^\)]*?)(frames\s*=\s*[^,\)]+)?', re.DOTALL)
# Patch save_animation_as_gif fps
gifsave_pattern = re.compile(r'(save_animation_as_gif\([^\)]*?fps\s*=\s*)10')

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    orig = content
    # Patch FuncAnimation frames
    def funcanim_repl(match):
        before = match.group(1)
        frames = match.group(2)
        if frames:
            # Replace existing frames argument
            return re.sub(r'frames\s*=\s*[^,\)]+', 'frames=1000', match.group(0))
        else:
            # Insert frames=1000 as first argument after (
            return before + 'frames=1000, '
    content = funcanim_pattern.sub(funcanim_repl, content)
    # Patch save_animation_as_gif fps
    content = gifsave_pattern.sub(r'\g<1>5', content)
    if content != orig:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Patched {filepath}')

def main():
    for fname in os.listdir(glob_dir):
        if fname.endswith('.py'):
            patch_file(os.path.join(glob_dir, fname))

if __name__ == '__main__':
    main() 