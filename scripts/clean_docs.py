import argparse
import sys
import os
import re

class BasicCleaner:
    def remove_nbsp(self, text):
        return text.replace("&nbsp;", " ")

    def standardize_headings(self, text):
        lines = text.splitlines()
        first_heading_idx = -1
        for idx, line in enumerate(lines):
            if re.match(r'^#+\s+', line):
                first_heading_idx = idx
                break
        if first_heading_idx == -1: return text
        new_lines = []
        for idx, line in enumerate(lines):
            match = re.match(r'^(#+)(\s+.*)$', line)
            if match:
                level = len(match.group(1))
                content = match.group(2).strip()
                if idx == first_heading_idx:
                    new_lines.append("# " + content)
                else:
                    new_level = max(2, level)
                    new_lines.append("#" * new_level + " " + content)
            else:
                new_lines.append(line)
        return "\n".join(new_lines) + ("\n" if text.endswith("\n") else "")

    def clean_horizontal_rules(self, text):
        text = re.sub(r'^\s*\*\*\*\s*$', '___HR_MARKER___', text, flags=re.MULTILINE)
        text = re.sub(r'(\s*___HR_MARKER___\s*)+', '\n***\n', text)
        return text.strip()

    def remove_empty_headings(self, text):
        lines = text.splitlines()
        new_lines = []
        for line in lines:
            if re.match(r'^\s*#+\s*$', line):
                continue
            new_lines.append(line)
        return "\n".join(new_lines)

    def clean(self, text):
        text = self.remove_nbsp(text)
        text = self.standardize_headings(text)
        text = self.clean_horizontal_rules(text)
        text = self.remove_empty_headings(text)
        return text

class TableFixer:
    @staticmethod
    def get_cells(row):
        inner = row.strip()
        if inner.startswith("|"): inner = inner[1:]
        if inner.endswith("|"): inner = inner[:-1]
        return [c.strip() for c in inner.split("|")]

    def restructure_sentence_analysis(self, text, file_path=""):
        is_ex_file = "_ex/" in file_path
        no_numbering = any(f in file_path for f in ["15_class.md", "29_class.md"])
        is_ipc_special_file = any(f"{n}_class" in file_path for n in range(16, 20))
        
        lines = text.splitlines()
        new_lines = []
        sentence_counter = 0
        sentence_active = False
        in_exercises_section = False
        i = 0

        def is_pali_sentence(s):
            s = s.strip()
            if not s: return False
            if s.startswith("#") and "<br>" not in s: return False
            
            # Root and analysis symbols always mean it's NOT a Pāli sentence for numbering
            if "√" in s or "+" in s: return False
            
            # Compound analysis without <br> is not a sentence
            if ("<" in s or ">" in s) and "<br>" not in s: return False
            
            english_words = {
                "the", "and", "with", "from", "for", "him", "her", "they", "was", "were", "been",
                "is", "are", "to", "of", "in", "on", "at", "by", "as", "be", "it", "this",
                "that", "which", "who", "not", "but", "or", "he", "she", "his", "her", "my", "your",
                "i", "you", "we", "they", "them", "had", "have", "has", "do", "does", "did",
                "all", "precedes", "chief", "states", "phenomena", "ruled", "created",
                "brahmin", "monks", "noble", "truth", "suffering", "path", "attainment",
                "wisdom", "knowledge", "light", "arose", "power", "body",
                "stop", "enough", "don't", "don", "grieve", "lament", "happy", "joyful",
                "passive", "verbs", "voice", "tense", "present", "future", "past", "aorist",
                "imperative", "optative", "conditional", "participle", "gerund", "absolutive",
                "infinitive", "noun", "adjective", "pronoun", "adverb", "preposition",
                "conjunction", "interjection", "particle", "idiom", "common", "example",
                "singular", "plural", "masculine", "feminine", "neuter", "nominative",
                "accusative", "instrumental", "dative", "ablative", "genitive", "locative", "vocative",
                "venerable", "make", "yourself", "unadmonishable", "should", "asked", "question",
                "these", "four", "times", "being", "done", "routinely",
                "cf", "collins", "page", "volume", "vol", "edition", "ed", "translated", "translation"
            }
            # Enhanced reference stripping
            clean_s = re.sub(r'[A-Z]+\s+\d+\.\d+', '', s)
            clean_s = re.sub(r'[A-Z][a-z]+\s+\d+', '', clean_s)
            clean_s = re.sub(r'\[\^\d+\]', '', clean_s)
            words_en = re.findall(r"\b[a-z']+\b", clean_s.lower())
            if any(w in english_words for w in words_en): return False
            
            # Refined Pāḷi component count (splitting by space, hyphen, apostrophe)
            pali_components = re.findall(r"[^\s\-']+", s)
            comp_count = len(pali_components)
            
            return "<br>" in s or (re.match(r'^[A-Z0-9]', s) and comp_count >= 3) or comp_count >= 3

        def is_translation(s):
            s = s.strip()
            if not s: return False
            if s.startswith("#") and "<br>" not in s: return False
            
            # Compound analysis and root analysis lines are translations/notes
            if "√" in s or "+" in s: return True
            if ("<" in s or ">" in s) and "<br>" not in s: return True
            
            english_words = {
                "the", "and", "with", "from", "for", "him", "her", "they", "was", "were", "been",
                "is", "are", "to", "of", "in", "on", "at", "by", "as", "be", "it", "this",
                "that", "which", "who", "not", "but", "or", "he", "she", "his", "her", "my", "your",
                "i", "you", "we", "they", "them", "had", "have", "has", "do", "does", "did",
                "all", "precedes", "chief", "states", "phenomena", "ruled", "created",
                "brahmin", "monks", "noble", "truth", "suffering", "path", "attainment",
                "wisdom", "knowledge", "light", "arose", "power", "body",
                "stop", "enough", "don't", "don", "grieve", "lament", "happy", "joyful",
                "passive", "verbs", "voice", "tense", "present", "future", "past", "aorist",
                "imperative", "optative", "conditional", "participle", "gerund", "absolutive",
                "infinitive", "noun", "adjective", "pronoun", "adverb", "preposition",
                "conjunction", "interjection", "particle", "idiom", "common", "example",
                "singular", "plural", "masculine", "feminine", "neuter", "nominative",
                "accusative", "instrumental", "dative", "ablative", "genitive", "locative", "vocative",
                "venerable", "make", "yourself", "unadmonishable", "should", "asked", "question",
                "these", "four", "times", "being", "done", "routinely",
                "cf", "collins", "page", "volume", "vol", "edition", "ed", "translated", "translation"
            }
            clean_s = re.sub(r'[A-Z]+\s+\d+\.\d+', '', s)
            clean_s = re.sub(r'[A-Z][a-z]+\s+\d+', '', clean_s)
            words = re.findall(r"\b[a-z']+\b", clean_s.lower())
            if any(w in english_words for w in words) or s.endswith(":"): return True
            
            if "<" in s or ">" in s:
                if "<br>" not in s: return False
            
            if re.match(r'^[A-Z]+\s+\d+\.\d+$', s): return False
            return (re.match(r'^[A-Z\*\[\(\"\']', s) or s.startswith("**")) and len(s.split()) >= 2

        def is_special_marker(s):
            s = s.strip().lower()
            return any(k in s for k in ["join the", "disjoin the", "dis-join the"])

        def finalize_block():
            nonlocal sentence_active
            if is_ex_file and sentence_active:
                new_lines.append("**&nbsp;**")
                new_lines.append("")
                new_lines.append("")
                sentence_active = False

        def split_combined_content(txt):
            parts = re.split(r'<br>\s*(?=[A-Z]{2,}\s+\d+)', txt)
            return [p.strip() for p in parts if p.strip()]

        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            if "**exercises**" in stripped.lower(): in_exercises_section = True
            if stripped.startswith("#"):
                finalize_block()
                sentence_counter = 0
                new_lines.append(line)
                i += 1
                continue

            if "|" in line and i + 1 < len(lines) and re.match(r"^\s*\|?([\s:-]*\|)+[\s:-]*\s*$", lines[i+1]):
                table_lines = []
                while i < len(lines) and "|" in lines[i]:
                    table_lines.append(lines[i])
                    i += 1
                
                # SPECIAL TASK LOGIC
                is_plus_table = any(" + " in tl for tl in table_lines)
                is_task_header = is_special_marker(self.get_cells(table_lines[0])[0])
                
                if is_ipc_special_file and not in_exercises_section and (is_plus_table or is_task_header):
                    data_rows = []
                    for tl in table_lines:
                        if re.match(r"^\s*\|?([\s:-]*\|)+[\s:-]*\s*$", tl): continue
                        cells = self.get_cells(tl)
                        non_empty = [c for c in cells if c]
                        if not non_empty: continue
                        
                        is_real_header = any(h.lower() in ["pāli", "pos", "grammar", "english", "root"] for h in cells)
                        if is_real_header and len(non_empty) > 1: continue
                        
                        if is_special_marker(non_empty[0]) and len(non_empty) == 1:
                            if data_rows:
                                new_lines.append("| | |")
                                new_lines.append("|---|---|")
                                for dr in data_rows: new_lines.append(f"| {dr[0]} | {dr[-1]} |")
                                new_lines.append("")
                                data_rows = []
                            new_lines.append(f"**{non_empty[0].replace('**','')}**")
                            new_lines.append("")
                        else:
                            data_rows.append([non_empty[0], non_empty[-1]])
                    if data_rows:
                        new_lines.append("| | |")
                        new_lines.append("|---|---|")
                        for dr in data_rows: new_lines.append(f"| {dr[0]} | {dr[-1]} |")
                        new_lines.append("")
                    continue

                # STANDARD TABLE LOGIC
                max_cols = 0
                for tl in table_lines:
                    if re.match(r"^\s*\|?([\s:-]*\|)+[\s:-]*\s*$", tl):
                        max_cols = tl.count("|") - 1
                        break
                
                header_cells = self.get_cells(table_lines[0])
                is_real_header = any(h.lower() in ["pāli", "pos", "grammar", "english", "root"] for h in header_cells)
                is_sentence_head = len([c for c in header_cells if c]) == 1 and is_pali_sentence(header_cells[0])
                
                start_k = 2 if (is_real_header and not is_sentence_head) else 0
                is_false_head = (start_k == 0)

                current_rows = []
                first_sub = True
                
                for k in range(start_k, len(table_lines)):
                    if k == 1 and start_k == 0: continue
                    row = table_lines[k]
                    if re.match(r"^\s*\|?([\s:-]*\|)+[\s:-]*\s*$", row): continue
                    
                    cells = self.get_cells(row)
                    non_empty = [c for c in cells if c]
                    original_txt = cells[0] if cells else ""
                    
                    # Ensure single-cell rows stay in the table IF they are not sentences/translations
                    # This primarily fixes the #ca issue.
                    if len(non_empty) == 1:
                        txt_parts = split_combined_content(original_txt)
                        # If splitting results in multiple parts, we definitely split them out.
                        # If it's just one part, check if it's a Pāli sentence or translation.
                        if len(txt_parts) > 1:
                            for txt in txt_parts:
                                if current_rows:
                                    # flush current table before splitting out
                                    header_type = "| " + " | ".join(["Pāli", "POS", "Grammar", "English", "Root"][:max_cols]) + " |" if first_sub and not is_false_head else "|" + " |" * max_cols
                                    new_lines.append(header_type)
                                    new_lines.append("|" + "---|" * max_cols)
                                    for cr in current_rows:
                                        c_list = self.get_cells(cr)
                                        while len(c_list) < max_cols: c_list.append("")
                                        new_lines.append("| " + " | ".join(c_list[:max_cols]) + " |")
                                    new_lines.append("")
                                    finalize_block()
                                    current_rows = []
                                    first_sub = False
                                
                                if is_pali_sentence(txt) or (not is_translation(txt)):
                                    sentence_counter += 1
                                    clean_s = re.sub(r'^\d+\.\s*', '', txt)
                                    new_lines.append(f"{clean_s}" if no_numbering else f"{sentence_counter}. {clean_s}")
                                    new_lines.append("")
                                    sentence_active = True
                                else:
                                    new_lines.append(f"**{txt.replace('**','')}**")
                                    new_lines.append("")
                                    sentence_active = False
                        else:
                            txt = txt_parts[0]
                            # Only split out if it's clearly a sentence or translation, 
                            # AND it's not a '#' line (which we want to keep in tables).
                            if (is_pali_sentence(txt) or is_translation(txt)) and not txt.startswith("#"):
                                if current_rows:
                                    header_type = "| " + " | ".join(["Pāli", "POS", "Grammar", "English", "Root"][:max_cols]) + " |" if first_sub and not is_false_head else "|" + " |" * max_cols
                                    new_lines.append(header_type)
                                    new_lines.append("|" + "---|" * max_cols)
                                    for cr in current_rows:
                                        c_list = self.get_cells(cr)
                                        while len(c_list) < max_cols: c_list.append("")
                                        new_lines.append("| " + " | ".join(c_list[:max_cols]) + " |")
                                    new_lines.append("")
                                    finalize_block()
                                    current_rows = []
                                    first_sub = False
                                
                                if is_pali_sentence(txt):
                                    sentence_counter += 1
                                    clean_s = re.sub(r'^\d+\.\s*', '', txt)
                                    new_lines.append(f"{clean_s}" if no_numbering else f"{sentence_counter}. {clean_s}")
                                    new_lines.append("")
                                    sentence_active = True
                                else:
                                    new_lines.append(f"**{txt.replace('**','')}**")
                                    new_lines.append("")
                                    sentence_active = False
                            else:
                                if any(cells): current_rows.append(row)
                    else:
                        if any(cells): current_rows.append(row)
                
                if current_rows:
                    if first_sub and not is_false_head:
                        std_h = ["Pāli", "POS", "Grammar", "English", "Root"][:max_cols]
                        new_lines.append("| " + " | ".join(std_h) + " |")
                        new_lines.append("|" + "---|" * max_cols)
                    else:
                        new_lines.append("|" + " |" * max_cols)
                        new_lines.append("|" + "---|" * max_cols)
                    for cr in current_rows:
                        c_list = self.get_cells(cr)
                        while len(c_list) < max_cols: c_list.append("")
                        new_lines.append("| " + " | ".join(c_list[:max_cols]) + " |")
                    new_lines.append("")
                continue

            if stripped:
                parts = split_combined_content(stripped)
                for part in parts:
                    if is_special_marker(part):
                        finalize_block()
                        new_lines.append(f"**{part.replace('**','')}**")
                        new_lines.append("")
                    elif is_pali_sentence(part):
                        finalize_block()
                        sentence_counter += 1
                        clean_s = re.sub(r'^\d+\.\s*', '', part)
                        new_lines.append(f"{clean_s}" if no_numbering else f"{sentence_counter}. {clean_s}")
                        new_lines.append("")
                        sentence_active = True
                    elif is_translation(part):
                        new_lines.append(f"**{part.replace('**','')}**")
                        new_lines.append("")
                        sentence_active = False
                    else:
                        new_lines.append(part)
            else:
                new_lines.append(line)
            i += 1
        
        finalize_block()
        return "\n".join(new_lines) + ("\n" if text.endswith("\n") else "")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", default="docs")
    args = parser.parse_args(sys.argv[1:])
    bc = BasicCleaner()
    tf = TableFixer()
    for root, _, files in os.walk(args.path):
        for file in files:
            if file.endswith(".md"):
                fp = os.path.join(root, file)
                if "ipc/class_18/11_ex.md" in fp: continue
                with open(fp, "r") as f: content = f.read()
                orig = content
                content = bc.clean(content)
                content = tf.restructure_sentence_analysis(content, fp)
                if content != orig:
                    with open(fp, "w") as f: f.write(content)
                    print(f"  [FIXED] {fp}")

if __name__ == "__main__": main()
