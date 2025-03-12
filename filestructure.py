import os

def get_file_structure(root_dir):
    file_structure = {}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        relative_path = os.path.relpath(dirpath, root_dir)
        file_structure[relative_path] = {
            'directories': dirnames,
            'files': filenames
        }
    return file_structure

def print_structure(structure, indent=0):
    for path, content in structure.items():
        # Print the current directory
        print(' ' * indent + f"Directory: {path}")
        # Print subdirectories
        for directory in content['directories']:
            print(' ' * (indent + 2) + f"Subdirectory: {directory}")
        # Print files
        for file in content['files']:
            print(' ' * (indent + 2) + f"File: {file}")

def save_structure_to_file(structure, output_file):
    with open(output_file, 'w') as f:
        for path, content in structure.items():
            f.write(f"Directory: {path}\n")
            for directory in content['directories']:
                f.write(f"  Subdirectory: {directory}\n")
            for file in content['files']:
                f.write(f"  File: {file}\n")

# Example usage
root_directory = '.'  # Current directory
structure = get_file_structure(root_directory)

# Print the structure to the console
print("File Structure:")
print_structure(structure)

# Save the structure to a file
output_file = 'file_structure.txt'
save_structure_to_file(structure, output_file)
print(f"\nFile structure saved to {output_file}")