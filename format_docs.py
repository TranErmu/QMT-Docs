
import re
from pathlib import Path

INPUT_FILE = Path(r"QMT_Docs\QMT_API_Documentation.md")
OUTPUT_FILE = Path(r"QMT_Docs\QMT_API_Documentation_Format.md")

def format_markdown(content):
    lines = content.splitlines()
    output = []
    
    in_code_block = False
    last_line_was_blank = True  # Start as if there's a blank line
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Detect Code Block
        if stripped.startswith("```"):
            if not in_code_block:
                # Entering code block
                if not last_line_was_blank and output:
                    output.append("")
                output.append(line)
                in_code_block = True
                last_line_was_blank = False
            else:
                # Exiting code block
                output.append(line)
                in_code_block = False
                last_line_was_blank = False
                # Ensure blank line after code block (will be handled by next iteration logic check, 
                # but good to be explicit or let the next line handle it)
            continue
            
        if in_code_block:
            output.append(line)
            last_line_was_blank = False
            continue
            
        # Headers
        # Match #, ##, ###, etc. 
        # Note: The file has lines like "#### # Title", so we match standard markdown headers
        is_header = re.match(r'^\s*#{1,6}\s', line)
        
        # Horizontal Rule
        is_hr = re.match(r'^\s*[-*_]{3,}\s*$', line)
        
        # List items
        is_list = re.match(r'^\s*[-*+]\s', line) or re.match(r'^\s*\d+\.\s', line)
        
        # Table
        is_table = re.match(r'^\s*\|.*\|\s*$', line)
        
        # Logic to insert blank lines
        
        if is_header:
            # Ensure blank line before header
            if not last_line_was_blank and output:
                output.append("")
            output.append(line)
            last_line_was_blank = False
            # We usually want a blank line AFTER a header? Standard markdown doesn't strictly require it 
            # for the next text to be a paragraph, but it looks better. 
            # However, if the next line is also a header, we might want to keep them close?
            # Let's enforce blank line BEFORE. 
            # AFTER is tricky if the user wants tight headers.
            # I'll just ensure BEFORE for now.
            
        elif is_hr:
            if not last_line_was_blank and output:
                output.append("")
            output.append(line)
            output.append("") # Blank line after HR
            last_line_was_blank = True
            
        elif is_list:
            # If it's a list item, we don't force blank line before unless it's a new list?
            # Detecting new list is hard line-by-line without lookahead.
            # I will just write it.
            # But if previous line was NOT a list item and NOT a header, add blank?
            
            # Simple heuristic: Just output the line.
            output.append(line)
            last_line_was_blank = False
            
        elif is_table:
            output.append(line)
            last_line_was_blank = False
            
        elif stripped == "":
            if not last_line_was_blank:
               output.append("")
            last_line_was_blank = True
            
        else:
            # Normal text
            # If previous line was a header, maybe add blank line? 
            # Standard: Header
            #           Text
            # is valid.
            
            # If previous line was a HTML block or Code block end? 
            # My 'last_line_was_blank' tracks explicit blanks.
            
            output.append(line)
            last_line_was_blank = False
            
    return "\n".join(output)

def main():
    if not INPUT_FILE.exists():
        print(f"File not found: {INPUT_FILE}")
        return
        
    content = INPUT_FILE.read_text(encoding='utf-8')
    formatted = format_markdown(content)
    
    # Additional cleanup: multiple blank lines to single
    formatted = re.sub(r'\n{3,}', '\n\n', formatted)
    
    OUTPUT_FILE.write_text(formatted, encoding='utf-8')
    print(f"Formatted file saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
