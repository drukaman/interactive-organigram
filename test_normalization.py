#!/usr/bin/env python3
"""
Test the normalization functionality directly
"""

import sys
sys.path.append('/Users/andreferreira/Desktop/Dev/techtree/nodes_organigram')

from normalization_service import IntelligentNormalizer

# Test the normalizer
normalizer = IntelligentNormalizer()

test_labels = [
    "ABS plastic",
    "cmos sensor", 
    "e-mail address",
    "LED light",
    "user interface",
    "R&D department",
    "USB connector",
    "pdf file",
    "html document",
    "project manager",
    "CEO office",
    "wifi network",
    "bluetooth device",
    "technical documentation"
]

print("🧪 Testing Intelligent Normalization")
print("=" * 50)

for label in test_labels:
    result = normalizer.analyze_text(label)
    status = "✅ PRESERVED" if not result['changed'] else "🔄 NORMALIZED"
    
    print(f"{status} '{result['original']}' → '{result['normalized']}'")
    if result['preserved_terms']:
        print(f"    🛡️  Preserved: {result['preserved_terms']}")
    if result['normalized_words']:
        changes = [f"{w['original']}→{w['normalized']}" for w in result['normalized_words']]
        print(f"    📝 Changed: {changes}")
    print()

print("\n🔍 Technical Term Detection Test")
print("=" * 40)

tech_terms = ["ABS", "CMOS", "LED", "USB", "PDF", "HTML", "CEO", "WiFi", "R&D"]
for term in tech_terms:
    is_tech = normalizer.is_technical_term(term)
    is_real = normalizer.is_real_word(term)
    should_preserve = normalizer.should_preserve_case(term)
    print(f"{term:<8} | Tech: {is_tech:<5} | Real: {is_real:<5} | Preserve: {should_preserve}")
