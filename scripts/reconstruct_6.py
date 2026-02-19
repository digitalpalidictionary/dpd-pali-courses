import re

def reconstruct_bpc_ex_6():
    with open("docs/bpc_key/6_class.md", "r") as f:
        key_content = f.read()

    # Normalize newlines
    key_content = key_content.replace("\r\n", "\n")
    # Split by double newline to get blocks
    blocks = [b.strip() for b in key_content.split("\n\n") if b.strip()]
    new_blocks = []
    
    # Header
    new_blocks.append("# Class 6 Exercises")
    
    i = 0
    sentence_count = 0
    while i < len(blocks):
        b = blocks[i]
        
        if b.startswith("# Class 6 Exercises"):
            i += 1
            continue

        if b.startswith("##"):
            new_blocks.append(b)
            sentence_count = 0 
            i += 1
            continue
            
        if re.match(r'^\d+\.', b):
            sentence_count += 1
            # Standardize numbering to match the current flow
            b_clean = re.sub(r'^\d+\.', f"{sentence_count}.", b)
            new_blocks.append(b_clean)
            i += 1
            
            # Process table
            if i < len(blocks) and "|" in blocks[i]:
                table_lines = blocks[i].splitlines()
                new_table = []
                # First block always gets header in Exercise too
                new_table.append("| Pāli | POS | Grammar | English | Root |")
                new_table.append("|---|---|---|---|---|")
                
                for tl in table_lines:
                    if "---|" in tl or "Pāli | POS" in tl:
                        continue
                    cells = [c.strip() for c in tl.strip("|").split("|")]
                    if not any(cells): continue
                    pali_word = cells[0]
                    # Create empty cells for Exercise
                    new_table.append(f"| {pali_word} | | | | |")
                
                new_blocks.append("\n".join(new_table))
                i += 1
                
                # Check for translation block
                if i < len(blocks) and blocks[i].startswith("**") and "is a common Pāli idiom" not in blocks[i]:
                    new_blocks.append("**&nbsp;**")
                    i += 1
            continue
        
        if b.startswith("**") and "is a common Pāli idiom" in b:
            new_blocks.append(b)
            i += 1
            continue
            
        # If it's a translation block that wasn't caught (standalone)
        if b.startswith("**"):
            new_blocks.append("**&nbsp;**")
            i += 1
            continue

        # Catch all
        new_blocks.append(b)
        i += 1

    content = "\n\n".join(new_blocks)
    
    with open("docs/bpc_ex/6_class.md", "w") as f:
        f.write(content + "\n")

if __name__ == "__main__":
    reconstruct_bpc_ex_6()
