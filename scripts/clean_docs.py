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

    def _parse_pali_words_from_header(self, header_sentence):
        # Clean the sentence: remove HTML, references, and punctuation
        clean = re.sub(r'<br>', ' ', header_sentence)
        # More robustly remove reference part, e.g., "4. VIN PAT SA 12 <br>"
        clean = re.sub(r'^\d+\.\s+([A-Z]+\s+)*[\d\.]+\s*', '', clean)
        clean = re.sub(r'\[[^\]]+\]', ' ', clean)
        clean = re.sub(r'\(simpl(ified)?\)', '', clean)
        clean = re.sub(r'[“”.’‘,;]', '', clean)
        # Handle contractions like 'ti and 'eva
        clean = clean.replace("'ti", " ti").replace("'eva", " eva")
        words = clean.split()
        # Filter out numbers and common small words that aren't part of the analysis
        pali_words = [w.strip() for w in words if re.search(r'[a-zA-Z]', w) and not w.isdigit()]
        return pali_words

    def _classify_term(self, term):
        term = term.strip()
        pos_tags = {'pron', 'adj', 'noun', 'verb', 'ind', 'pp', 'ptp', 'ger', 'abs', 'inf', 'idiom', 'card', 'adv'}
        if term in pos_tags:
            return 'pos'
        # Grammar: nt.acc.sg, masc.nom.pl, etc.
        if re.match(r'^[a-z]{2,3}(\.[a-z]{2,3})+\.s[gp]$', term):
            return 'grammar'
        # Check if it's primarily English words
        english_words_in_term = re.findall(r'\b[a-zA-Z]+\b', term)
        if len(english_words_in_term) > 0 and all(w.islower() or w.istitle() for w in english_words_in_term):
             # Simple heuristic, can be improved
            if len(english_words_in_term) >= 1 :
                return 'english'
        return 'pali' # Default assumption

    def _convert_list_to_table(self, header, lines):
        """Converts a flat list of terms into a markdown table, rewritten for simplicity."""
        
        built_rows = []
        for line in lines:
            term = line.strip()
            if not term:
                continue

            term_type = self._classify_term(term)

            if term_type == 'pali':
                # This term is a Pāḷi word, start a new row.
                built_rows.append([term, '', '', '', ''])
            elif built_rows:
                # This term is analysis, add it to the last Pāḷi word's row.
                last_row = built_rows[-1]
                if term_type == 'pos' and not last_row[1]:
                    last_row[1] = term
                elif term_type == 'grammar' and not last_row[2]:
                    last_row[2] = term
                else: # Default to appending to the English column
                    last_row[3] = (last_row[3] + " " + term).strip()

        # Build the final markdown table string
        md_table_lines = ["| Pāli | POS | Grammar | English | Root |", "|---|---|---|---|---|"]
        for row_data in built_rows:
            md_table_lines.append("| " + " | ".join(row_data) + " |")

        return "\n".join(md_table_lines)

    def restructure_sentence_analysis(self, text, file_path=""):
        is_ex_file = "_ex/" in file_path
        no_numbering = any(f in file_path for f in ["15_class.md", "29_class.md"])
        is_ipc_special_file = any(f"{n}_class" in file_path for n in range(16, 20))
        is_class_2 = "2_class.md" in file_path
        
        lines = text.splitlines()
        new_lines = []
        sentence_counter = 0
        sentence_active = False
        in_exercises_section = False
        first_table_in_section = True
        table_flushed_for_current_sentence = False
        last_flushed_rows = []
        current_rows = []
        max_cols = 5 if is_ex_file else 0
        i = 0

        def is_pali_sentence(s):
            s = s.strip()
            if not s: return False
            if s.startswith("#") and "<br>" not in s: return False
            
            # CRITICAL: If it's a known fragment, it's NOT a sentence for renumbering
            if any(f in s for f in ["anāgatam’", "abyāpajjha-"]):
                return False

            # Reference markers are NOT Pāli sentences by themselves for renumbering
            if is_pure_reference(s): return False

            # Footnotes are not Pāli sentences
            if s.startswith("[^"): return False
            
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
                "cf", "collins", "page", "volume", "vol", "edition", "ed", "translated", "translation",
                "originally", "alt", "simplified", "simpl"
            }
            # Enhanced reference stripping
            clean_s = re.sub(r'\b[A-Z]{2,}\s+[\d\.]+\b', '', s)
            clean_s = re.sub(r'\(simpl(ified)?\)', '', clean_s)
            clean_s = re.sub(r'\[\^\d+\]', '', clean_s)
            
            words_en = re.findall(r"\b[a-z']+\b", clean_s.lower())
            if any(w in english_words for w in words_en): return False
            
            # Refined Pāḷi component count (splitting by space, hyphen, apostrophe)
            # Only count components that contain at least one letter
            pali_components = [c for c in re.findall(r"[^\s\-']+", clean_s) if re.search(r'[a-zA-Z]', c)]
            comp_count = len(pali_components)
            
            # Special case for Class 2 and no_numbering files: allow 2-word sentences
            min_words = 2 if (is_class_2 or no_numbering) else 3
            
            # MUST look like a sentence: either has <br> or starts with Caps and has enough words
            return "<br>" in s or (re.match(r'^[A-Z0-9]', s) and comp_count >= min_words)

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
                "cf", "collins", "page", "volume", "vol", "edition", "ed", "translated", "translation",
                "originally", "alt", "simplified", "simpl"
            }
            clean_s = re.sub(r'\b[A-Z]{2,}\s+[\d\.]+\b', '', s)
            clean_s = re.sub(r'\(simpl(ified)?\)', '', clean_s)
            clean_s = re.sub(r'\[\^\d+\]', '', clean_s)
            words = re.findall(r"\b[a-z']+\b", clean_s.lower())
            
            # If it has English words or ends with a colon
            if any(w in english_words for w in words) or s.endswith(":"): return True
            
            if "<" in s or ">" in s:
                if "<br>" not in s: return False
            
            if re.match(r'^[A-Z]+\s+\d+\.\d+$', s): return False
            
            # Translation markers like [trains] or (Buddharakkhita)
            # but NOT simple single words in parens which might be part of Pāli analysis
            if re.match(r'^[\(\[].*[\)\]]$', s):
                if len(s.split()) >= 2:
                    return True
                return False
            
            return (re.match(r'^[A-Z\*\[\(\"\']', s) or s.startswith("**")) and len(s.split()) >= 2

        def is_special_marker(s):
            s = s.strip().lower()
            return any(k in s for k in ["join the", "disjoin the", "dis-join the"])

        def normalize_row(r):
            return "|".join([c.strip() for c in self.get_cells(r)])

        def finalize_block():
            nonlocal sentence_active, current_rows, max_cols, table_flushed_for_current_sentence, last_flushed_rows
            if current_rows:
                # Deduplicate check against LAST table flushed in this sentence/block
                normalized_current = [normalize_row(r) for r in current_rows]
                normalized_last = [normalize_row(r) for r in last_flushed_rows]
                
                if normalized_current != normalized_last:
                    flush_table(current_rows, max_cols, False)
                    last_flushed_rows = list(current_rows)
                    table_flushed_for_current_sentence = True
            current_rows = []
            if is_ex_file and sentence_active:
                # Only add spacing if we really are ending a sentence block
                new_lines.append("**&nbsp;**")
                new_lines.append("")
                new_lines.append("")
                sentence_active = False
                table_flushed_for_current_sentence = False
                last_flushed_rows = [] # Clear only when we truly move to a new exercise/section

        def split_combined_content(txt):
            # Do NOT split if it starts with #
            if txt.strip().startswith("#"):
                return [txt.strip()]
            
            # Split only if <br> is followed by a Reference pattern (2+ capital letters then space then digit)
            # This separates introductory notes from actual sentences with references.
            parts = re.split(r'<br>\s*(?=[A-Z]{2,}\s+\d+)', txt)
            return [p.strip() for p in parts if p.strip()]

        def is_pure_reference(s):
            # Matches strings like "MN 19 (simpl)" or "SN 10.8" or "VIN 1.2.12"
            # It should not have Pāli text after it.
            s = re.sub(r'^\d+\.\s*', '', s.strip()) # strip existing number
            # Pattern: 2-3 caps, space, digits/dots, optional (simpl)
            # Improved to handle multi-part references like "VIN PAT SA 12"
            pattern = r'^[A-Z]{2,}(\s+[A-Z]{2,})*\s+[\d\.]+(\s+\(simpl\))?$'
            return re.match(pattern, s) is not None

        def is_fragment(s):
            # A fragment is short, might have <br>, and definitely doesn't look like a full sentence
            # and is usually just a few words from the exercise header.
            # AND it should not be a word that likely belongs in a table row (like having POS)
            # OR it's a numbered item that is extremely short (likely a broken continuation)
            
            orig_s = s.strip()
            # Clean for comparison
            s_clean = re.sub(r'^\d+\.\s*', '', orig_s).strip()
            if not s_clean: return False
            
            # Specific known fragments causing issues
            if any(f in s_clean for f in ["anāgatam’", "abyāpajjha-"]):
                return True

            pali_components = [c for c in re.findall(r"[^\s\-']+", s_clean) if re.search(r'[a-zA-Z]', c)]
            comp_count = len(pali_components)
            
            # If it was numbered but is very short AND lacks a reference, it's a fragment
            is_numbered = re.match(r'^\d+\.\s*', orig_s) is not None
            has_reference = bool(re.search(r'\b[A-Z]{2,}\s+[\d\.]+\b', s_clean))
            
            if is_numbered and not has_reference and comp_count <= 3:
                return True

            # If it contains <br> it's likely a header fragment or a multi-line word
            return (comp_count <= 2 and "<br>" in s_clean) or comp_count == 1

        def is_marker(s):
            s = s.strip()
            # More robust marker detection for artifacts
            return bool(re.match(r'^\*\*(\s|&nbsp;)*\*\*\s*$', s)) or s == "** **"

        def flush_table(rows, max_cols, first_sub):
            nonlocal first_table_in_section
            if not rows: return
            
            # Filter out marker rows from being flushed INTO the table
            rows = [r for r in rows if not is_marker(self.get_cells(r)[0])]
            if not rows: return

            if first_table_in_section:
                header_type = "| " + " | ".join(["Pāli", "POS", "Grammar", "English", "Root"][:max_cols]) + " |"
                first_table_in_section = False
            else:
                header_type = "| " + " | ".join(["" for _ in range(max_cols)]) + " |"
            
            new_lines.append(header_type)
            new_lines.append("|" + "---|" * max_cols)
            for cr in rows:
                c_list = self.get_cells(cr)
                while len(c_list) < max_cols: c_list.append("")
                new_lines.append("| " + " | ".join(c_list[:max_cols]) + " |")
            new_lines.append("")

        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            if "**exercises**" in stripped.lower(): in_exercises_section = True
            if stripped.startswith("#"):
                finalize_block()
                sentence_counter = 0
                first_table_in_section = True # Reset header state for new section
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
                
                current_rows = []
                first_sub = True
                
                k = start_k
                while k < len(table_lines):
                    if k == 1 and start_k == 0: 
                        k += 1
                        continue
                    row = table_lines[k]
                    if re.match(r"^\s*\|?([\s:-]*\|)+[\s:-]*\s*$", row):
                        k += 1
                        continue
                    
                    cells = self.get_cells(row)
                    non_empty = [c for c in cells if c]
                    original_txt = cells[0] if cells else ""
                    
                    if len(non_empty) == 1:
                        txt_parts = split_combined_content(original_txt)
                        if len(txt_parts) > 1:
                            for txt in txt_parts:
                                if is_marker(txt):
                                    finalize_block()
                                    continue
                                
                                if is_fragment(txt) and sentence_active:
                                    clean_part = re.sub(r'^\d+\.\s*', '', txt).strip()
                                    current_rows.append(f"| {clean_part} | | | | |")
                                    continue

                                if txt.strip() and is_pali_sentence(txt):
                                    finalize_block()
                                    sentence_counter += 1
                                    clean_s = re.sub(r'^\d+\.\s*', '', txt)
                                    new_lines.append(f"{clean_s}" if no_numbering else f"{sentence_counter}. {clean_s}")
                                    new_lines.append("")
                                    sentence_active = True
                                    continue
                                elif txt.strip() and is_translation(txt):
                                    finalize_block()
                                    new_lines.append(f"**{txt.replace('**','')}**")
                                    new_lines.append("")
                                    sentence_active = False
                                    continue
                        else:
                            txt = txt_parts[0]
                            if is_marker(txt):
                                finalize_block()
                            elif is_fragment(txt) and sentence_active:
                                clean_part = re.sub(r'^\d+\.\s*', '', txt).strip()
                                current_rows.append(f"| {clean_part} | | | | |")
                            elif txt.strip() and is_pali_sentence(txt) and not txt.startswith("#"):
                                # LOOKAHEAD MERGE for tables
                                if is_pure_reference(txt) and k + 1 < len(table_lines):
                                    next_row = table_lines[k+1]
                                    next_cells = self.get_cells(next_row)
                                    if len([c for c in next_cells if c]) == 1:
                                        next_txt = next_cells[0]
                                        if is_pali_sentence(next_txt):
                                            txt = txt + " <br>" + next_txt
                                            k += 1 # skip next row
                                
                                finalize_block()
                                sentence_counter += 1
                                clean_s = re.sub(r'^\d+\.\s*', '', txt)
                                new_lines.append(f"{clean_s}" if no_numbering else f"{sentence_counter}. {clean_s}")
                                new_lines.append("")
                                sentence_active = True
                                k += 1
                                continue
                            elif txt.strip() and is_translation(txt) and not txt.startswith("#"):
                                finalize_block()
                                new_lines.append(f"**{txt.replace('**','')}**")
                                new_lines.append("")
                                sentence_active = False
                                k += 1
                                continue
                            else:
                                if any(cells): current_rows.append(row)
                    else:
                        if any(cells): current_rows.append(row)
                    k += 1
                
                flush_table(current_rows, max_cols, first_sub)
                continue

            if stripped:
                # LOOKAHEAD MERGE for standalone lines
                if is_pure_reference(stripped) and i + 1 < len(lines):
                    next_stripped = lines[i+1].strip()
                    if not next_stripped and i + 2 < len(lines):
                        next_stripped = lines[i+2].strip()
                        if is_pali_sentence(next_stripped) and not is_pure_reference(next_stripped):
                            stripped = stripped + " <br>" + next_stripped
                            i += 2 # skip blank and next
                    elif is_pali_sentence(next_stripped) and not is_pure_reference(next_stripped):
                        stripped = stripped + " <br>" + next_stripped
                        i += 1

                parts = split_combined_content(stripped)
                for part in parts:
                    if is_special_marker(part) or is_marker(part):
                        finalize_block()
                        if is_special_marker(part):
                            new_lines.append(f"**{part.replace('**','')}**")
                            new_lines.append("")
                    else:
                        clean_part = re.sub(r'^\d+\.\s*', '', part).strip()
                        if is_fragment(part) and sentence_active:
                            current_rows.append(f"| {clean_part} | | | | |")
                        elif is_pali_sentence(clean_part):
                            finalize_block()
                            sentence_counter += 1
                            header_line = f"{clean_part}" if no_numbering else f"{sentence_counter}. {clean_part}"
                            new_lines.append(header_line)
                            new_lines.append("")
                            sentence_active = True

                            # LOOKAHEAD to see if this is a flat list
                            peek_i = i + 1
                            while peek_i < len(lines) and not lines[peek_i].strip():
                                peek_i += 1
                            
                            if peek_i < len(lines) and not lines[peek_i].strip().startswith('|'):
                                list_lines = []
                                list_start_i = peek_i
                                while peek_i < len(lines):
                                    line_peek = lines[peek_i].strip()
                                    if (is_pali_sentence(line_peek) and not is_fragment(line_peek)) or is_marker(line_peek) or line_peek.startswith('#'):
                                        break
                                    list_lines.append(lines[peek_i])
                                    peek_i += 1
                                
                                table_str = self._convert_list_to_table(header_line, list_lines)
                                new_lines.append(table_str)
                                new_lines.append("")
                                i = peek_i - 1
                                sentence_active = False # The block is handled
                                continue

                        elif is_translation(clean_part):
                            finalize_block()
                            new_lines.append(f"**{clean_part.replace('**','')}**")
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

    def process_file(fp):
        if "ipc/class_18/11_ex.md" in fp: return
        # Process _ex folders, Skip _key folders for now
        if "_key/" in fp: return
        
        with open(fp, "r") as f: content = f.read()
        orig = content
        content = bc.clean(content)
        content = tf.restructure_sentence_analysis(content, fp)
        if content != orig:
            with open(fp, "w") as f: f.write(content)
            print(f"  [FIXED] {fp}")

    if os.path.isfile(args.path):
        process_file(args.path)
    else:
        for root, _, files in os.walk(args.path):
            for file in files:
                if file.endswith(".md"):
                    fp = os.path.join(root, file)
                    if "_ex/" not in fp and "bpc/" not in root and "ipc/" not in root: continue
                    process_file(fp)

if __name__ == "__main__": main()
