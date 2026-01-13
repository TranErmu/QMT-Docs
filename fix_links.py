import re
from pathlib import Path

FILE_PATH = Path(r"QMT_Docs\QMT_API_Documentation_Format.md")

def fix_links():
    if not FILE_PATH.exists():
        print(f"File not found: {FILE_PATH}")
        return

    content = FILE_PATH.read_text(encoding='utf-8')
    
    # 1. Gather headers
    headers = []
    # Matches "#### # Title" or "## # Title"
    # Capture the Title part
    for line in content.splitlines():
        m = re.match(r'^\s*#+\s+#\s+(.*)$', line)
        if m:
            headers.append(m.group(1).strip())
            
    print(f"Found {len(headers)} headers.")
    
    # 2. Replace links
    # Pattern: [LinkText 在新窗口打开](URL)
    # Target: [LinkText](#-MatchingHeaderTitle)
    
    def replacer(match):
        raw_text = match.group(1) # e.g. "XtCreditDetail"
        link_text = raw_text.strip()
        
        # Find header
        candidates = [h for h in headers if link_text in h]
        
        if not candidates:
            # Try fuzzy match?
            return match.group(0) # No change
            
        # Select best match
        # Prefer suffix match (e.g. Header "FooBar" ends with Link "Bar")
        best = candidates[0]
        suffix_matches = [c for c in candidates if c.endswith(link_text)]
        if suffix_matches:
            best = suffix_matches[0]
            
        new_link = f"[{link_text}](#-{best})"
        return new_link

    # Regex: [ (capture) space 在新窗口打开 ] ( ... )
    new_content = re.sub(r'\[(.*?)\s+在新窗口打开\]\(.*?\)', replacer, content)
    
    # Also replace "参见数据字典在新窗口打开" -> "参见[数据字典](#-数据字典)"
    # And "参见投保类型在新窗口打开" -> "参见[投保类型](#-投保类型)"
    new_content = new_content.replace("参见数据字典在新窗口打开", "参见[数据字典](#-数据字典)")
    new_content = new_content.replace("参见投保类型在新窗口打开", "参见[投保类型](#-投保类型)")
    
    # Write back
    FILE_PATH.write_text(new_content, encoding='utf-8')
    print("Links fixed.")

if __name__ == "__main__":
    fix_links()
