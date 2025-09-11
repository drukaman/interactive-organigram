#!/usr/bin/env python3
import re

pattern = r'^[A-Z]{2,}$'

test_words = ['Motor', 'control', 'CONTROL', 'DC', 'AC', 'ECU', 'Inverter']

for word in test_words:
    match_case_sensitive = re.match(pattern, word)
    match_case_insensitive = re.match(pattern, word, re.IGNORECASE)
    
    print(f"'{word}':")
    print(f"  Case sensitive: {bool(match_case_sensitive)}")
    print(f"  Case insensitive: {bool(match_case_insensitive)}")
    print()
