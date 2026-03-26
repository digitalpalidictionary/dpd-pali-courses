import os
import re

def is_target_table(table_lines):
    count = 0
    # Match prefixes like 1., 2., 3rd, 1st, 1.nom, nom, acc, dat etc.
    pattern = re.compile(r'^\s*(1|2|3|4|5|6|7|8|nom|acc|inst|dat|abl|gen|loc|voc)', re.IGNORECASE)
    for line in table_lines:
        if line.strip().startswith('|'):
            cells = line.split('|')
            if len(cells) > 2:
                first_col = cells[1].strip().lower()
                # we want to match exactly if it looks like a case or person indicator
                if pattern.match(first_col) or first_col in ['1st', '2nd', '3rd', '1.', '2.', '3.']:
                    count += 1
    # If a table has at least 3 rows matching these patterns, it's definitely a declension/conjugation table
    return count >= 3

def process_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    changed = False
    new_lines = []
    
    table_lines = []
    
    def flush_table():
        nonlocal changed, new_lines
        if not table_lines:
            return
            
        if not is_target_table(table_lines):
            new_lines.extend(table_lines)
            table_lines.clear()
            return
            
        for i, line in enumerate(table_lines):
            if '---' in line and set(line.strip().replace('|', '').replace('-', '').replace(' ', '')) == set():
                new_lines.append(line)
                continue
                
            cells = line.split('|')
            new_cells = []
            
            for j, cell in enumerate(cells):
                if j == 0 or j == len(cells) - 1:
                    new_cells.append(cell)
                    continue
                if j == 1:
                    # Usually case or person, skip modifying it
                    new_cells.append(cell)
                    continue
                
                cell_stripped = cell.strip()
                
                english_words = {
                    'the', 'man', 'subject', 'object', 'by', 'with', 'through', 'to', 'for', 'from', 'of', 'in', 'on', 'at',
                    'hey', 'he', 'she', 'it', 'we', 'you', 'they', 'is', 'are', 'was', 'were', 'am', 'cook', 'cooked',
                    'speak', 'speaks', 'spoke', 'stand', 'stood', 'teach', 'taught', 'all', 'a', 'an', 'and', 'or', 'not'
                }
                
                # Check for English cell by intersection with stop words
                words = set([w.strip('.,*()[]!?;:') for w in cell_stripped.lower().replace('<br>', ' ').split()])
                
                is_english = bool(words.intersection(english_words))
                has_bold = '**' in cell_stripped
                has_diacritic = any(d in cell_stripped for d in 'āīūñṭḍṇḷṃĀĪŪÑṬḌṆḶṂ')
                
                # If it looks like english and doesn't have bold/diacritics, skip
                if is_english and not (has_bold or has_diacritic):
                    new_cells.append(cell)
                    continue
                    
                if '[' in cell_stripped or '<img' in cell_stripped:
                    new_cells.append(cell)
                    continue
                
                # Remove ALL commas and replace <br> with space
                clean_cell = cell_stripped.replace('<br>', ' ').replace(',', '')
                
                parts = clean_cell.split()
                if len(parts) > 1:
                    # We have multiple words in a Pali cell, join them with <br>
                    new_cell_content = '<br>'.join(parts)
                    left_space = cell[:len(cell) - len(cell.lstrip())]
                    right_space = cell[len(cell.rstrip()):]
                    new_cell_full = f"{left_space}{new_cell_content}{right_space}"
                    new_cells.append(new_cell_full)
                    if cell != new_cell_full:
                        changed = True
                else:
                    new_cells.append(cell)
                    
            new_lines.append('|'.join(new_cells))
        
        table_lines.clear()

    for line in lines:
        if line.strip().startswith('|') and line.strip().endswith('|'):
            table_lines.append(line)
        else:
            if table_lines:
                flush_table()
            new_lines.append(line)
            
    if table_lines:
        flush_table()
            
    if changed:
        with open(filepath, 'w') as f:
            f.writelines(new_lines)
        return True
    return False

def main():
    changed_files = 0
    for folder in ['docs/bpc', 'docs/ipc']:
        for root, _, files in os.walk(folder):
            for file in files:
                if file.endswith('.md'):
                    filepath = os.path.join(root, file)
                    if process_file(filepath):
                        print(f"Updated: {filepath}")
                        changed_files += 1
    print(f"Total files updated: {changed_files}")

if __name__ == '__main__':
    main()
