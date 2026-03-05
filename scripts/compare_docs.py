import os
import subprocess
import re
import argparse
import difflib

def get_tokens(text):
    """
    Normalizes text and extracts a list of words.
    Removes markdown formatting, HTML tags, and punctuation.
    """
    # Remove markdown links/images URLs but keep the alt/link text
    text = re.sub(r'\[([^\]]*)\]\([^\)]+\)', r'\1', text)
    # Remove markdown formatting characters
    text = re.sub(r'[*_~`]', '', text)
    # Remove HTML tags
    text = re.sub(r'<[a-zA-Z/][^>]*>', ' ', text)
    # Remove punctuation that might be attached to words differently
    # Include hyphens and other standard punctuation in removal to focus strictly on words
    text = re.sub(r'[#\[\]\(\)>|\\.,;!?\'"/\-:]', ' ', text)
    # Split into words and convert to lowercase
    words = re.split(r'\s+', text.strip().lower())
    return [w for w in words if w]

def get_old_content(file_path, commit):
    cmd = ["git", "show", f"{commit}:{file_path}"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return None
    return result.stdout

def main():
    parser = argparse.ArgumentParser(description="Compare current .md files with an older version using word sequence logic.")
    parser.add_argument("--commit", default="6680b670763a103af1a9679ed984fbe260e1ede7", help="Git commit to compare against")
    parser.add_argument("--dir", default="docs", help="Directory to search for .md files")
    parser.add_argument("--verbose", action="store_true", help="Show the actual differences found")
    
    args = parser.parse_args()

    md_files = []
    if os.path.isfile(args.dir):
        if args.dir.endswith(".md"):
            md_files.append(args.dir)
    else:
        for root, dirs, files in os.walk(args.dir):
            for file in files:
                if file.endswith(".md"):
                    md_files.append(os.path.join(root, file))

    if not md_files:
        print(f"No .md files found in {args.dir}")
        return

    print(f"Comparing {len(md_files)} file(s) against commit {args.commit} using word-by-word diff...")
    
    files_with_losses = 0

    for file_path in md_files:
        old_content = get_old_content(file_path, args.commit)
        if old_content is None:
            continue
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                new_content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            continue

        old_tokens = get_tokens(old_content)
        new_tokens = get_tokens(new_content)

        s = difflib.SequenceMatcher(None, old_tokens, new_tokens)
        
        missing_phrases = []
        for tag, i1, i2, j1, j2 in s.get_opcodes():
            if tag in ('delete', 'replace'):
                deleted_words = old_tokens[i1:i2]
                if deleted_words:
                    # we only consider it missing if the phrase isn't found anywhere in the new tokens
                    # This check makes it robust against simple reordering of paragraphs.
                    deleted_phrase = " ".join(deleted_words)
                    new_text = " ".join(new_tokens)
                    if deleted_phrase not in new_text:
                        missing_phrases.append(deleted_phrase)

        if missing_phrases:
            files_with_losses += 1
            print(f"\n[DATA LOSS] {file_path}: {len(missing_phrases)} phrases missing")
            if args.verbose:
                for mp in missing_phrases:
                    print(f"  - '{mp}'")
            else:
                for mp in missing_phrases[:5]:
                    # Truncate long phrases for summary output
                    display_mp = mp if len(mp) < 60 else mp[:57] + "..."
                    print(f"  - '{display_mp}'")
                if len(missing_phrases) > 5:
                    print(f"    ... and {len(missing_phrases)-5} more phrases.")

    if files_with_losses == 0:
        print("\nNo data loss detected!")
    else:
        print(f"\nTotal files with potential data loss: {files_with_losses}")

if __name__ == "__main__":
    main()
