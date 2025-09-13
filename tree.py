import re

def parse_tree_file(input_file, output_file):
    flat_paths = []
    path_stack = []

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue

            # Match the pattern for level detection: count how many tree drawing characters are before the file/folder
            level_match = re.match(r'([│ ├└─]*)[^│ ├└─]', line)
            if level_match:
                tree_prefix = level_match.group(1)

                # Estimate the level by counting '│' or ' ' groups (each level adds ~1 of these)
                level = tree_prefix.count('│') + tree_prefix.count('    ')

                # Clean name by removing the tree drawing characters
                name = line.strip().replace('├─', '').replace('└─', '').replace('│', '').strip()

                # Adjust path stack
                path_stack = path_stack[:level]
                path_stack.append(name)

                # If it's a file (has a . in name), record full path
                if '.' in name:
                    flat_paths.append('/'.join(path_stack))

    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        for path in flat_paths:
            f.write(path + '\n')
    print(f"Flat path list written to {output_file}")


if __name__ == '__main__':
    parse_tree_file('architecture.txt', 'structure.txt')

