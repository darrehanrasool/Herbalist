import os

def generate_filtered_tree(start_path, exclude_dirs=None, exclude_ext=None):
    if exclude_dirs is None:
        exclude_dirs = {'.git', '__pycache__', 'venv', 'node_modules', '.idea', '.vscode'}
    if exclude_ext is None:
        exclude_ext = {'.pyc', '.pyo'}
    
    result = []
    
    for root, dirs, files in os.walk(start_path):
        # Remove excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        level = root.replace(start_path, '').count(os.sep)
        indent = '│   ' * (level - 1) + '├── ' if level > 0 else ''
        
        if level > 0:
            result.append(f"{indent}{os.path.basename(root)}/")
        else:
            result.append(f"{os.path.basename(root)}/")
        
        subindent = '│   ' * level + '├── '
        for i, file in enumerate(files):
            if any(file.endswith(ext) for ext in exclude_ext):
                continue
            is_last = (i == len(files) - 1) and (len(dirs) == 0)
            current_indent = '│   ' * level + ('└── ' if is_last else '├── ')
            result.append(f"{current_indent}{file}")
    
    return '\n'.join(result)

# Generate and save
structure = generate_filtered_tree('.')
with open('project_structure.txt', 'w', encoding='utf-8') as f:
    f.write(structure)
print("Project structure saved to project_structure.txt")