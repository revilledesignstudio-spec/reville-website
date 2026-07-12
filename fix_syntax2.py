import os
count = 0
for r, d, fs in os.walk('.'):
    for f in fs:
        if f.endswith('.html'):
            filepath = os.path.join(r, f)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # The buggy snippet has an extra </script> tag
            buggy_snippet = '</script>\n</script>\n<div id="rv-overlay">'
            fixed_snippet = '</script>\n<div id="rv-overlay">'
            
            if buggy_snippet in content:
                content = content.replace(buggy_snippet, fixed_snippet)
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(content)
                count += 1
                print(f"Fixed {filepath}")

print(f"Total files fixed: {count}")
