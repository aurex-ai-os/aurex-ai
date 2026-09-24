import sys
import json
import logging
import asyncio

# Setup basic logging
logging.basicConfig(level=logging.INFO)

# Test DuckDuckGo Search
try:
    from duckduckgo_search import DDGS
    print("\n--- Testing DuckDuckGo API ---")
    with DDGS() as ddgs:
        results = list(ddgs.text("What is Quantum Computing PDF", max_results=3))
        for r in results:
            print(f"Result: {r['title']} - {r['href']}")
except Exception as e:
    print(f"DDGS Error: {e}")

# Test PDF Extraction
try:
    from pdfminer.high_level import extract_text
    import urllib.request
    print("\n--- Testing PDFMiner ---")
    url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
    urllib.request.urlretrieve(url, "scratch/dummy.pdf")
    text = extract_text("scratch/dummy.pdf")
    print(f"Successfully extracted {len(text)} characters from dummy PDF!")
    print(f"Preview: {text.strip()[:50]}...")
except Exception as e:
    print(f"PDF Error: {e}")
