import re
from pathlib import Path

FILE_PATH = Path(r"QMT_Docs\QMT_API_Documentation_Format.md")

def indent_code_blocks():
    if not FILE_PATH.exists():
        print(f"File not found: {FILE_PATH}")
        return

    content = FILE_PATH.read_text(encoding='utf-8')
    lines = content.splitlines()
    
    print(f"Processing {len(lines)} lines...")
    
    # We will write to a temp buffer first
    new_lines = []
    
    i = 0
    blocks_processed = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Detect start of code block
        # Fix: handle '- ```'
        is_fence = re.match(r'^\s*(- )?```', line)
        
        if is_fence:
            blocks_processed += 1
            
            # Scan backwards for context in ORIGINAL lines
            target_indent = 0
            back_idx = i - 1
            
            while back_idx >= 0:
                prev_line = lines[back_idx]
                
                if not prev_line.strip():
                    back_idx -= 1
                    continue
                
                # Check for Header
                if re.match(r'^\s*#{1,6}\s', prev_line):
                    target_indent = 0
                    break
                
                # Check for List Item
                m_list = re.match(r'^(\s*)([-*+]|\d+\.)\s', prev_line)
                if m_list:
                    current_indent = len(m_list.group(1))
                    target_indent = current_indent + 2
                    break
                
                if re.match(r'^\S', prev_line):
                    target_indent = 0
                    break
                
                back_idx -= 1
            
            # Apply indent
            indent_str = ' ' * target_indent
            
            # Add start fence
            new_lines.append(f"{indent_str}{line.lstrip()}")
            
            i += 1
            while i < len(lines):
                sub_line = lines[i]
                # Preserve content relative indentation?
                # Assume original block content was left-aligned or relative to fence
                # Since fence was 0, lstrip is fine for fence. 
                # For content, if it had indentation, we want to keep it relative to new fence?
                # Current file has 0 indent for content.
                # So indent_str + sub_line.lstrip() is probably okay because sub_line usually has 0 indent.
                # However, if sub_line had 4 spaces (e.g. inside function), lstrip removes it!
                # BETTER: indent_str + sub_line?
                # If sub_line was 0 indent, result is indented. Correct.
                # If sub_line was already 4 spaces? Result is indented + 4 spaces. Correct.
                # BUT, wait. If I use `line` directly, `target_indent` is added to existing indent.
                # Existing indent for 3330 is 0. So 0 + 4 = 4.
                # Existing indent for `sub_line` (account = ...) is 0. So 0 + 4 = 4.
                # This works.
                # What if fence was already indented? (e.g. 4 spaces).
                # `indent_str` calculated is 4.
                # ` ' ' * 4 + '    ```' ` -> 8 spaces!
                # So we must UNINDENT current line, then Apply Target.
                # Or checks if current matches target?
                # User asked to "format".
                # I will lstrip() the fence.
                # For inner content, I logic:
                # content_indent = leading_spaces(sub_line)
                # fence_indent = leading_spaces(line)
                # relative_indent = content_indent - fence_indent
                # new_line = indent_str + ' ' * relative_indent + sub_line.lstrip()
                # But sub_line.lstrip() kills inside spaces.
                # Simply: indent_str + sub_line.lstrip() is risky.
                
                # Logic: preserve original content, just shift it?
                # Current file: 0 indent everywhere.
                # So shifting = adding `indent_str`.
                
                new_lines.append(f"{indent_str}{sub_line}")
                
                if sub_line.strip().startswith("```"):
                   i += 1
                   break
                i += 1
            
        else:
            new_lines.append(line)
            i += 1

    print(f"Processed {blocks_processed} blocks.")
    
    # Write back
    FILE_PATH.write_text("\n".join(new_lines), encoding='utf-8')
    print("Code blocks indented.")

if __name__ == "__main__":
    indent_code_blocks()
