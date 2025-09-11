#!/usr/bin/env python3
"""
Test specific normalization issues
"""

import sys
import re
sys.path.append('/Users/andreferreira/Desktop/Dev/techtree/nodes_organigram')

from normalization_service import IntelligentNormalizer

# Test the normalizer
normalizer = IntelligentNormalizer()

test_cases = [
    "Thermal acoustical protective shields (TAPS)",
    "Power liftgate spindle drive with ECU", 
    "ABS / ESC",
    "Cornering brake control (CBC)",
    "Multi-collision braking system (MKB)",
    "Roll movement intervention (RMI)",
    "Carbon fiber SMC (Sheet Molding Compound) for CFRP back door",
]

print("🧪 Testing Specific Normalization Issues")
print("=" * 60)

for text in test_cases:
    print(f"\n🔍 Analyzing: '{text}'")
    
    # Show tokenization
    tokens = re.findall(r'\b\w+\b|\s+|[^\w\s]', text)
    print(f"Tokens: {tokens}")
    
    # Test individual words
    words = re.findall(r'\b\w+\b', text)
    for word in words:
        is_tech = normalizer.is_technical_term(word)
        should_preserve = normalizer.should_preserve_case(word)
        normalized = normalizer.normalize_word(word)
        print(f"  '{word}' -> '{normalized}' (tech: {is_tech}, preserve: {should_preserve})")
    
    # Full analysis
    result = normalizer.analyze_text(text)
    print(f"Original:  '{result['original']}'")
    print(f"Result:    '{result['normalized']}'")
    if result['preserved_terms']:
        print(f"Preserved: {result['preserved_terms']}")
    print("-" * 60)
