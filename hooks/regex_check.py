#!/usr/bin/env python3
import re
import sys
from pathlib import Path

def load_patterns(blacklist_path, whitelist_path):
    """Load regex patterns from files"""
    blacklist = [re.compile(line.strip()) for line in blacklist_path.read_text().splitlines() if line.strip()]
    whitelist = [re.compile(line.strip()) for line in whitelist_path.read_text().splitlines() if line.strip()]
    return blacklist, whitelist

def check_file(file_path, blacklist, whitelist):
    all_matches = []
    try:
        content = file_path.read_text(encoding='utf-8')
        for line_num, line in enumerate(content.splitlines(), 1):
            for bl_pattern in blacklist:
                if bl_pattern.search(line):
                    if not any(wl_pattern.search(line) for wl_pattern in whitelist):
                        all_matches.append((file_path, line_num, line.strip(), bl_pattern.pattern))
        return all_matches
    except (UnicodeDecodeError, PermissionError):
        pass  # Skip binary/unreadable files
    return all_matches


def main():
    
    import argparse
    parser = argparse.ArgumentParser()
    args,filenames = parser.parse_known_args()
    
    
    # Paths relative to git root
    blacklist_path = Path("blacklist_patterns.txt")
    whitelist_path = Path("whitelist_patterns.txt")
    
    if not blacklist_path.exists():
        print("Blacklist file missing")
        sys.exit(1)

    blacklist, whitelist = load_patterns(blacklist_path, whitelist_path)
    all_errors = []
    
    for file in filenames:
        matches = check_file(Path(file), blacklist, whitelist)
        if matches:
            all_errors.extend(matches)

    if all_errors:
        print("Commit rejected - forbidden patterns detected:")
        for file, line_num, line, pattern in all_errors:
            print(f"• {file}:{line_num} - {pattern}")
            print(f"  {line}")
        sys.exit(1)
    else:   
        print(" No forbidden patterns detected")
        sys.exit(0)

if __name__ == "__main__":
    main()
