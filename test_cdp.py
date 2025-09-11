#!/usr/bin/env python3
"""
Test the CDP case specifically
"""

import sys
import re
sys.path.append('/Users/andreferreira/Desktop/Dev/techtree/nodes_organigram')

from normalization_service import IntelligentNormalizer

# Test the normalizer
normalizer = IntelligentNormalizer()

test_case = "Controller deceleration parking (CDP)"

print("🚨 Testing CDP Case")
print("=" * 60)

print(f"\n🔍 Analyzing: '{test_case}'")

# Show tokenization
tokens = re.findall(r'\b\w+\b|\s+|[^\w\s]', test_case)
print(f"Tokens: {tokens}")

# Test individual words
words = re.findall(r'\b\w+\b', test_case)
for word in words:
    is_tech = normalizer.is_technical_term(word)
    word_upper = word.upper()
    in_tech_terms = word_upper in normalizer.technical_terms
    should_preserve = normalizer.should_preserve_case(word)
    normalized = normalizer.normalize_word(word)
    
    # Test pattern matching
    pattern_matches = []
    for pattern in normalizer.technical_patterns:
        if re.match(pattern, word):
            pattern_matches.append(pattern)
    
    print(f"  '{word}' -> '{normalized}'")
    print(f"    - tech: {is_tech}")
    print(f"    - in_list: {in_tech_terms}") 
    print(f"    - preserve: {should_preserve}")
    print(f"    - patterns: {pattern_matches}")

# Test CDP specifically
print(f"\n🔍 CDP specific tests:")
print(f"  - 'CDP' in technical_terms: {'CDP' in normalizer.technical_terms}")
print(f"  - is_technical_term('CDP'): {normalizer.is_technical_term('CDP')}")
print(f"  - should_preserve_case('CDP'): {normalizer.should_preserve_case('CDP')}")
print(f"  - normalize_word('CDP'): '{normalizer.normalize_word('CDP')}'")

# Full analysis
result = normalizer.analyze_text(test_case)
print(f"\n✨ FINAL RESULT:")
print(f"   Original:  '{result['original']}'")
print(f"   Result:    '{result['normalized']}'")
if result['preserved_terms']:
    print(f"   Preserved: {result['preserved_terms']}")
print("-" * 60)
