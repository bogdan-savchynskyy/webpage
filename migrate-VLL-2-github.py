import os
import re

def migrate_html_file(file_path, root_dir):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Determine directory depth relative to the root folder to craft correct relative paths
    rel_dir = os.path.relpath(os.path.dirname(file_path), root_dir)
    if rel_dir == '.':
        to_root = './'
    else:
        # For every level down, go up one step via '../'
        levels = len(rel_dir.replace('\\', '/').split('/'))
        to_root = '../' * levels

    # 1. Parse and extract PHP configuration variables dynamically
    php_vars = {}
    php_blocks = re.findall(r'<\?php\s+(\$\w+)\s*=\s*["\']([^"\']+)["\']\s*;\s*\?>', content, re.IGNORECASE)
    for var_name, var_value in php_blocks:
        php_vars[var_name] = var_value

    # Strip out the initial declaration PHP blocks entirely
    content = re.sub(r'<\?php\s+\$\w+\s*=\s*["\'][^"\']+\s*;\s*\?>\s*', '', content, flags=re.IGNORECASE)

    # Replace instances where PHP echoes variables e.g., <?php echo $Variable; ?> or <?php echo $Variable;>
    def replace_php_echo(match):
        var_name = match.group(1)
        return php_vars.get(var_name, match.group(0))

    content = re.sub(r'<\?php\s+echo\s+(\$\w+)\s*;?\s*\?>', replace_php_echo, content, flags=re.IGNORECASE)

    # 2. Convert standard local root-relative links to clean relative links
    # Matches strings starting with /vislearn/HTML/people/bogdan/ or /vislearn/people/bogdan/
    pattern = r'(src|href)\s*=\s*["\']/vislearn/(?:HTML/)?people/bogdan/([^"\']*)["\']'
    
    def link_replacer(match):
        attribute = match.group(1)
        sub_path = match.group(2)
        
        # Adjust directory landing pointers to physical files for GitHub Pages
        if sub_path == '' or sub_path == '/':
            # Points back to the root landing page index
            return f'{attribute}="{to_root}Dr-Bogdan-Savchynskyy.html"'
        
        if sub_path.rstrip('/') in ['aboutme', 'projects', 'publications', 'teaching']:
            folder = sub_path.rstrip('/')
            return f'{attribute}="{to_root}{folder}/{folder}.html"'
            
        return f'{attribute}="{to_root}{sub_path}"'

    content = re.sub(pattern, link_replacer, content, flags=re.IGNORECASE)

    # 3. Clean up any leftover absolute root references missing the explicit folder path names
    content = re.sub(r'(src|href)\s*=\s*["\']/vislearn/([^"\']*)["\']', r'\1="' + to_root + r'\2"', content, flags=re.IGNORECASE)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Migrated successfully: {file_path}")

def main():
    root_directory = os.getcwd()
    for root, dirs, files in os.walk(root_directory):
        for file in files:
            if file.lower().endswith('.html'):
                full_path = os.path.join(root, file)
                migrate_html_file(full_path, root_directory)

if __name__ == "__main__":
    main()