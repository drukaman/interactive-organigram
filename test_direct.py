#!/usr/bin/env python3
"""
Test individual normalization without using requests
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from normalization_service import IntelligentNormalizer

def test_normalization():
    normalizer = IntelligentNormalizer()
    
    test_cases = [
        "Controller deceleration parking (CDP)",
        "Anti-lock braking system (ABS)", 
        "Electronic control unit (ECU)",
        "Traction and parking stability (TAPS)"
    ]
    
    print("🚨 Testing Normalization Logic Directly")
    print("=" * 60)
    
    for test_text in test_cases:
        print(f"🔍 INPUT: '{test_text}'")
        
        # Test the normalizer directly
        analysis = normalizer.analyze_text(test_text)
        
        print(f"📊 OUTPUT: '{analysis['normalized']}'")
        print(f"🔒 PRESERVED: {analysis['preserved_terms']}")
        print("-" * 40)

if __name__ == "__main__":
    test_normalization()
