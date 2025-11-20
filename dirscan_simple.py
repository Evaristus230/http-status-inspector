#!/usr/bin/env python3
"""
Simple Directory Discovery Analyzer
Author: Evaristus
Purpose: Scan for directories and group responses by HTTP status code.
Why? To avoid missing important paths masked as 403/404/5xx.
"""

import requests
import sys
from urllib.parse import urljoin

# Disable SSL warnings (safe for labs)
requests.packages.urllib3.disable_warnings()

def load_wordlist(filepath):
    """Read wordlist: one path per line (skip blanks & comments)"""
    try:
        with open(filepath, 'r') as f:
            # Strip whitespace, skip empty/comment lines
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print(f"[!] Error: Wordlist '{filepath}' not found.")
        sys.exit(1)

def scan_path(base_url, path):
    """Send a HEAD request to a path and return (path, status_code)"""
    # Build full URL: http://host:port + /path
    full_url = urljoin(base_url.rstrip('/') + '/', path.lstrip('/'))
    
    try:
        # Use HEAD (faster, no body transfer)
        response = requests.head(
            full_url,
            timeout=5,
            verify=False,  # Skip SSL cert check (for labs)
            headers={'User-Agent': 'DirScan-Simple/1.0'}
        )
        return (path, response.status_code)
    
    except requests.exceptions.Timeout:
        return (path, "TIMEOUT")
    except:
        return (path, "ERROR")

def main():
    # Basic usage check
    if len(sys.argv) != 3:
        print("Usage: python dirscan_simple.py <base_url> <wordlist>")
        print("Example: python dirscan_simple.py http://localhost:3000 wordlist.txt")
        sys.exit(1)

    base_url = sys.argv[1]
    wordlist = sys.argv[2]

    print(f"[+] Scanning {base_url} with wordlist: {wordlist}")
    
    # Load paths
    paths = load_wordlist(wordlist)
    print(f"[+] Loaded {len(paths)} paths.")

    # Dictionary to group paths by status code: {200: ['/'], 403: ['/admin'], ...}
    results = {}

    # Scan each path
    for path in paths:
        path, status = scan_path(base_url, path)
        
        # Add path to its status group
        if status not in results:
            results[status] = []
        results[status].append(path)

        # Print interesting statuses live
        if status in (200, 301, 302, 403):
            color = "\033[92m" if status == 200 else "\033[93m" if status in (301, 302) else "\033[91m"
            reset = "\033[0m"
            print(f"{color}[{status}]{reset} {path}")

    # Final summary
    print("\n[=] Scan complete. Summary:")
    for status in sorted(results):
        count = len(results[status])
        examples = ", ".join(results[status][:3])  # First 3 examples
        print(f"  {status}: {count} path(s) — e.g., {examples}")

    # Highlight insight: "403 ≠ dead end"
    if 403 in results:
        print(f"\n[!] Tip: {len(results[403])} path(s) returned 403 (Forbidden).")
        print("    In real apps, 403 on /admin but 200 on /admin/ can mean hidden access — try manually!")

if __name__ == "__main__":
    main()
