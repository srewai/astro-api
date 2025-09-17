import re

def convert_tree_to_paths(tree_file_path, output_file_path):
    """
    Convert a directory tree from a file into a list of complete file paths,
    handling comments at the end of lines and correctly processing subdirectories
    under └─ branches. Includes files with .py, .env.example, .toml, .md, and LICENSE.
    
    Args:
        tree_file_path (str): Path to the file containing the directory tree
        output_file_path (str): Path to the file where complete paths will be stored
        
    Returns:
        list: List of complete, normalized file paths
    """
    paths = []
    current_path = []
    
    # Define valid file extensions and names
    valid_extensions = {'.py', '.env.example', '.toml', '.md', '.yml', '.api', '.worker'}
    valid_filenames = {'LICENSE'}
    
    # Read the tree file
    try:
        with open(tree_file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: File '{tree_file_path}' not found")
        return paths
    except Exception as e:
        print(f"Error reading file: {e}")
        return paths
    
    for line in lines:
        # Remove trailing whitespace/newlines
        line = line.rstrip()
        # Remove comments (anything after #)
        if '#' in line:
            line = line.split('#', 1)[0].rstrip()
        if not line:
            continue
        
        # Normalize line for indentation calculation by replacing tree characters with spaces
        normalized_line = re.sub(r'[├└│─]', ' ', line)
        # Calculate leading spaces in the normalized line
        leading_spaces = len(normalized_line) - len(normalized_line.lstrip())
        # Each level corresponds to 3 'units' in the prefix
        indent_level = leading_spaces // 3
        
        # Extract the clean name by removing the tree prefix (including ├─, └─, │, spaces)
        clean_line = re.sub(r'^[\s├─└│]+', '', line).rstrip('/')
        
        # Update current path based on indentation level
        current_path = current_path[:indent_level]
        current_path.append(clean_line)
        
        # Check if the line corresponds to a file with a valid extension or name
        if (clean_line.endswith(tuple(valid_extensions)) or clean_line in valid_filenames):
            full_path = '/'.join(current_path)
            paths.append(full_path)
    
    # Write the complete paths to the output file
    try:
        with open(output_file_path, 'w') as file:
            for path in paths:
                file.write(f"{path}\n")
        print(f"Complete file paths successfully written to '{output_file_path}'")
    except Exception as e:
        print(f"Error writing to output file: {e}")
    
    return paths

def main():
    # Input and output file paths
    input_file = "architecture.txt"
    output_file = "file_paths.txt"
    
    # Convert tree to complete paths and store in output file
    file_paths = convert_tree_to_paths(input_file, output_file)
    
    # Print complete paths to console
    print("Converted complete file paths:")
    for path in file_paths:
        print(f"- {path}")

if __name__ == "__main__":
    main()
