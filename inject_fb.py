import os

html_files = []
for r, d, fs in os.walk('.'):
    for f in fs:
        if f.endswith('.html') and f != 'framer_custom_code.html':
            html_files.append(os.path.join(r, f))

with open('framer_custom_code.html', 'r', encoding='utf-8') as f:
    custom_code = f.read()

if 'hookFacebookLinks' not in custom_code:
    # Add the facebook hook to the end of the script before the IIFE closes
    hook_code = """
  // ── FACEBOOK LINK HIJACK ───────────────────────────────────────────────────
  function hookFacebookLinks() {
    var links = document.querySelectorAll("a");
    for (var i = 0; i < links.length; i++) {
      var href = links[i].getAttribute("href");
      if (href && (href.includes("facebook.com/profile.php?id=61560320026895") || href.includes("facebook.com/people/Gopal"))) {
        links[i].setAttribute("href", "https://www.facebook.com/p/Reville-Design-Studio-61560320026895/");
      }
    }
  }
  hookFacebookLinks();
  setInterval(hookFacebookLinks, 1000);
})();"""
    custom_code = custom_code.replace('})();', hook_code)
    with open('framer_custom_code.html', 'w', encoding='utf-8') as f:
        f.write(custom_code)

count = 0
for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We need to replace the old custom code block if it exists
    start_marker = '<script>\n(function () {\n  // Global flag to prevent double execution'
    
    if start_marker in content:
        # It's already injected, we need to replace the old script block with the new one
        start_idx = content.find(start_marker)
        end_idx = content.find('</script>', start_idx) + len('</script>')
        
        new_content = content[:start_idx] + custom_code + content[end_idx:]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1

print(f'Injected to {count} files.')
