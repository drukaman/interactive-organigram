#!/usr/bin/env python3
"""
Test the JavaScript fallback function logic in Python to verify it works
"""

import re

def toProperCaseBasic(s):
    if not s:
        return s
    
    # Basic fallback normalization (used when service is unavailable)
    preserve_patterns = [
        r'\be-mail\b',
        r'\bi-\w+\b',
        r'\be-\w+\b'  # e-prefixed words like e-Axle
    ]
    
    # Check if the string contains preserve patterns - if so, handle carefully
    has_preserve_pattern = False
    for pattern in preserve_patterns:
        if re.search(pattern, s, re.IGNORECASE):
            has_preserve_pattern = True
            break
    
    if has_preserve_pattern:
        # For strings with preserve patterns, be more careful
        def replace_word(match):
            word = match.group(0)
            # Check if this specific word should be preserved
            if re.match(r'^e-\w+$', word, re.IGNORECASE) or re.match(r'^i-\w+$', word, re.IGNORECASE):
                return word.lower()
            # Preserve all-caps words that are likely acronyms
            if len(word) <= 6 and word == word.upper() and re.match(r'^[A-Z]+$', word):
                return word
            return word.capitalize()
        
        return re.sub(r'\b\w+\b', replace_word, s)
    
    # Regular proper case conversion
    def replace_word_regular(match):
        word = match.group(0)
        # Preserve all-caps words that are likely acronyms  
        if len(word) <= 6 and word == word.upper() and re.match(r'^[A-Z]+$', word):
            return word
        # Handle hyphenated technical terms like DC-AC
        if '-' in word:
            parts = word.split('-')
            new_parts = []
            for part in parts:
                if len(part) <= 6 and part == part.upper() and re.match(r'^[A-Z]+$', part):
                    new_parts.append(part)  # Preserve acronym parts
                else:
                    new_parts.append(part.capitalize())
            return '-'.join(new_parts)
        return word.capitalize()
    
    return re.sub(r'\b\w+\b', replace_word_regular, s)

def test_fallback():
    test_cases = [
        "Motor control ECU",
        "Power control ECU", 
        "DC Converter",
        "DC-AC Inverter",
        "DC-DC/AC-DC Converter",
        "EV ECU",
        "e-Axle",
        "motor control ecu",
        "dc-ac inverter"
    ]
    
    print("🚨 Testing JavaScript Fallback Function (Python Version)")
    print("=" * 80)
    
    for test_text in test_cases:
        result = toProperCaseBasic(test_text)
        print(f"'{test_text}' → '{result}'")
    
if __name__ == "__main__":
    test_fallback()
