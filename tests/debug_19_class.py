import re
import subprocess
import difflib

def get_tokens(text):
    text = re.sub(r'\[([^\]]*)\]\([^\)]+\)', r'\1', text)
    text = re.sub(r'[*_~`]', '', text)
    text = re.sub(r'<[^>]*>', ' ', text)
    text = re.sub(r'[#\[\]\(\)>|\\.,;!?\'"/\-:]', ' ', text)
    words = re.split(r'\s+', text.strip().lower())
    return [w for w in words if w]

cmd = ["git", "show", "6680b670763a103af1a9679ed984fbe260e1ede7:docs/ipc_key/19_class.md"]
result = subprocess.run(cmd, capture_output=True, text=True)
old_content = result.stdout

with open("docs/ipc_key/19_class.md", 'r', encoding='utf-8') as f:
    new_content = f.read()

old_tokens = get_tokens(old_content)
new_tokens = get_tokens(new_content)

s = difflib.SequenceMatcher(None, old_tokens, new_tokens)
for tag, i1, i2, j1, j2 in s.get_opcodes():
    if tag in ('delete', 'replace'):
        deleted_words = old_tokens[i1:i2]
        if deleted_words:
            deleted_phrase = " ".join(deleted_words)
            new_text = " ".join(new_tokens)
            if deleted_phrase not in new_text:
                print(f"Old phrase tokens: {old_tokens[i1-5:i2+5]}")
                print(f"New tokens at approx same spot: {new_tokens[j1-5:j2+20]}")
                print(f"Index i1={i1} i2={i2} j1={j1} j2={j2}")
                break
