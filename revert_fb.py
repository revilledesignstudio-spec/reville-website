import os

html_files = []
for r, d, fs in os.walk('.'):
    for f in fs:
        if f.endswith('.html') and f != 'framer_custom_code.html':
            html_files.append(os.path.join(r, f))

# 1. Update framer_custom_code.html
with open('framer_custom_code.html', 'r', encoding='utf-8') as f:
    custom_code = f.read()

# The hook starts with '// ── FACEBOOK LINK HIJACK' and ends before '})();'
start_idx = custom_code.find('// ── FACEBOOK LINK HIJACK')
if start_idx != -1:
    end_idx = custom_code.find('})();', start_idx)
    custom_code = custom_code[:start_idx] + custom_code[end_idx:]
    with open('framer_custom_code.html', 'w', encoding='utf-8') as f:
        f.write(custom_code)

# 2. Update all HTML files
count = 0
for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    start_marker = '<script>\n(function () {\n  // Global flag to prevent double execution'
    if start_marker in content:
        s_idx = content.find(start_marker)
        e_idx = content.find('</script>', s_idx) + len('</script>')
        new_content = content[:s_idx] + '<script>\n' + custom_code + '</script>' + content[e_idx:]
        
        # Revert the URLs back to the ID format explicitly
        new_content = new_content.replace('https://www.facebook.com/p/Reville-Design-Studio-61560320026895/', 'https://www.facebook.com/profile.php?id=61560320026895')

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1

print(f'Reverted in {count} files.')
