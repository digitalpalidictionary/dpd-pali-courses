import re

def is_pali_sentence(s):
    s = s.strip()
    if not s: return False
    if s.startswith("#") and "<br>" not in s: return False
    if s.startswith("[^"): return False
    if "√" in s or "+" in s: return False
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
    clean_s = re.sub(r'\b[A-Z]{2,}\s+[\d\.]+\b', '', s)
    clean_s = re.sub(r'\(simpl(ified)?\)', '', clean_s)
    clean_s = re.sub(r'\[\^\d+\]', '', clean_s)
    
    words_en = re.findall(r"\b[a-z']+\b", clean_s.lower())
    print(f"DEBUG: clean_s='{clean_s}' words_en={words_en}")
    if any(w in english_words for w in words_en): return False
    
    pali_components = re.findall(r"[^\s\-']+", s)
    comp_count = len(pali_components)
    min_words = 2 # Simulation for Class 2
    
    return "<br>" in s or (re.match(r'^[A-Z0-9]', s) and comp_count >= min_words) or comp_count >= min_words

test_strs = [
    "TH 257 (simpl)[^2]<br>araññe rukkhānaṃ mūlesu[^3], kandarāsu guhāsu ca",
    "DN 22.1 (simpl)<br>maggo hoti sokaparidevānaṃ samatikkamāya, ñāyassa adhigamāya, nibbānassa sacchikiriyāya."
]

for ts in test_strs:
    print(f"Testing: {ts}")
    print(f"  is_pali: {is_pali_sentence(ts)}")
