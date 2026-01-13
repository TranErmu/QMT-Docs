import re
from pathlib import Path

FILE_PATH = Path(r"QMT_Docs\QMT_API_Documentation_Format.md")

def debug_indent():
    if not FILE_PATH.exists():
        print("File not found.")
        return

    content = FILE_PATH.read_text(encoding='utf-8')
    lines = content.splitlines()
    
    # Check specifically around line 3330 (index ~3329)
    # Scan for the block
    target_line_idx = -1
    for idx, line in enumerate(lines):
        if "account = StockAccount('1000000365')" in line and "```python" in lines[idx-1]:
            target_line_idx = idx - 1
            break
    
    if target_line_idx == -1:
        print("Target block not found.")
        return
        
    print(f"Target line index: {target_line_idx}")
    print(f"Line content: '{lines[target_line_idx]}'")
    
    # Scan back logic
    back_idx = target_line_idx - 1
    while back_idx >= 0:
        prev_line = lines[back_idx]
        print(f"Checking line {back_idx}: '{prev_line}'")
        
        if not prev_line.strip():
            print("  -> Blank, skipping")
            back_idx -= 1
            continue
            
        m_list = re.match(r'^(\s*)([-*+]|\d+\.)\s', prev_line)
        if m_list:
            print(f"  -> MATCH LIST! Indent: {len(m_list.group(1))}")
        else:
            print("  -> No list match")
            
        break

if __name__ == "__main__":
    debug_indent()
