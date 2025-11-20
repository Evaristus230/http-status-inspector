# 🔍 HTTP Status Inspector

> A simple Python tool to analyze HTTP responses during directory discovery — helps avoid false negatives.

This tool:
- Sends `HEAD` requests to paths from a wordlist  
- Groups results by status code (200, 403, 404, etc.)  
- Highlights 403s — because they might hide real access points  
- Built for my lab work — inspired by real scanning challenges

---

## 🚀 Quick Start

1. **Clone this repo**:
   ```bash
   git clone https://github.com/Evaristus230/http-status-inspector.git
   cd http-status-inspector
