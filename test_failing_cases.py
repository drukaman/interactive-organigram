#!/usr/bin/env python3
"""
Test the exact failing cases
"""

import sys
import re
sys.path.append('/Users/andreferreira/Desktop/Dev/techtree/nodes_organigram')

from normalization_service import IntelligentNormalizer

# Test the normalizer
normalizer = IntelligentNormalizer()

failing_cases = [
    "ABS / ESC",
    "ABS/DSC ECU", 
    "ABS/ESC"
]

print("🚨 Testing Exact Failing Cases")
print("=" * 60)

for text in failing_cases:
    print(f"\n🔍 Analyzing: '{text}'")
    
    # Show tokenization
    tokens = re.findall(r'\b\w+\b|\s+|[^\w\s]', text)
    print(f"Tokens: {tokens}")
    
    # Test individual words
    words = re.findall(r'\b\w+\b', text)
    for word in words:
        is_tech = normalizer.is_technical_term(word)
        word_upper = word.upper()
        in_tech_terms = word_upper in normalizer.technical_terms
        should_preserve = normalizer.should_preserve_case(word)
        normalized = normalizer.normalize_word(word)
        print(f"  '{word}' -> '{normalized}' (tech: {is_tech}, in_list: {in_tech_terms}, preserve: {should_preserve})")
    
    # Full analysis
    result = normalizer.analyze_text(text)
    print(f"✨ FINAL RESULT:")
    print(f"   Original:  '{result['original']}'")
    print(f"   Result:    '{result['normalized']}'")
    if result['preserved_terms']:
        print(f"   Preserved: {result['preserved_terms']}")
    print("-" * 60)
