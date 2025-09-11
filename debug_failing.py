#!/usr/bin/env python3
"""
Test the actual failing cases to debug the tokenization issue
"""

import sys
import os
import re

# Add spellchecker to test
try:
    from spellchecker import SpellChecker
    HAS_SPELLCHECKER = True
except ImportError:
    HAS_SPELLCHECKER = False

class DebugNormalizer:
    def __init__(self):
        if HAS_SPELLCHECKER:
            self.spell = SpellChecker()
        else:
            self.spell = None
            
        # Copy the exact technical terms from the service
        self.technical_terms = {
            # Electronics/Computing
            'ABS', 'AC', 'DC', 'LED', 'LCD', 'OLED', 'RAM', 'ROM', 'CPU', 'GPU', 'SSD', 'HDD',
            'USB', 'HDMI', 'VGA', 'DVI', 'API', 'SDK', 'IDE', 'GUI', 'CLI', 'OS', 'IP', 'TCP',
            'UDP', 'HTTP', 'HTTPS', 'FTP', 'SSH', 'SSL', 'TLS', 'DNS', 'URL', 'URI', 'JSON',
            'XML', 'HTML', 'CSS', 'JS', 'SQL', 'NoSQL', 'AI', 'ML', 'AR', 'VR', 'IoT', 'GPS',
            'WIFI', 'LTE', '5G', '4G', '3G', 'RFID', 'NFC', 'QR', 'OCR', 'PDF', 'CSV', 'PNG',
            'JPG', 'JPEG', 'GIF', 'SVG', 'MP3', 'MP4', 'AVI', 'MOV', 'WAV', 'FLAC',
            'ECU', 'EV'
        }
        
        self.technical_patterns = [
            r'^[A-Z]{2,6}$',  # 2-6 letter acronyms
            r'^[A-Z]+\d+$',   # Acronym followed by numbers
            r'^\d+[A-Z]+$',   # Numbers followed by letters
            r'^[A-Z]&[A-Z]$', # A&B pattern
            r'^[A-Z]+/[A-Z]+$', # A/B pattern
        ]
        
        self.preserve_patterns = [
            r'^[A-Z]{2,}$',     # All caps (likely acronyms)
            r'^[A-Z]+\d+$',     # Mixed letters and numbers
            r'.*e-mail.*',      # e-mail variations
            r'.*i-\w+.*',       # i-prefixed words
            r'^e-\w+$',         # e-prefixed words like e-Axle
            r'^i-\w+$',         # i-prefixed words like i-lithium
        ]
    
    def is_technical_term(self, word):
        """Check if a word is a technical term."""
        if word.upper() in self.technical_terms:
            return True
        
        for pattern in self.technical_patterns:
            if re.match(pattern, word):
                return True
        
        return False
    
    def is_real_word(self, word):
        """Check if a word is in the dictionary."""
        if not self.spell:
            common_words = {'motor', 'control', 'power', 'inverter', 'converter'}
            return word.lower() in common_words
            
        clean_word = re.sub(r'[^a-zA-Z]', '', word.lower())
        if len(clean_word) < 2:
            return False
        
        return clean_word in self.spell
    
    def should_preserve_case(self, word):
        """Determine if a word's case should be preserved."""
        print(f"      🔍 should_preserve_case('{word}'):")
        
        # Check preserve patterns first (case-sensitive)
        for pattern in self.preserve_patterns:
            if re.match(pattern, word):
                print(f"        ✅ Matches preserve pattern: {pattern}")
                return True
        
        # If it's all uppercase and is a technical term, preserve it
        if word.isupper() and self.is_technical_term(word):
            print(f"        ✅ Uppercase technical term")
            return True
        
        # If it's all uppercase but NOT a real word, it's likely an acronym
        if word.isupper() and not self.is_real_word(word):
            print(f"        ✅ Uppercase non-dictionary word (likely acronym)")
            return True
        
        # Special case: if it's a known technical term regardless of case, preserve its uppercase form
        if word.upper() in self.technical_terms:
            print(f"        ✅ Known technical term (will be uppercased)")
            return True
        
        print(f"        ❌ Regular word, will be normalized")
        return False
    
    def normalize_word(self, word):
        """Normalize a single word with intelligent case handling."""
        print(f"    🔧 normalize_word('{word}'):")
        
        # Handle empty or very short words
        if len(word) < 2:
            print(f"      → Short word: '{word}'")
            return word
        
        # Check if this word should be converted to uppercase (known technical terms)
        if word.upper() in self.technical_terms:
            result = word.upper()
            print(f"      → Known technical term: '{result}'")
            return result
        
        # Preserve case for technical terms and acronyms
        if self.should_preserve_case(word):
            print(f"      → Preserve case: '{word}'")
            return word
        
        # Handle hyphenated words
        if '-' in word:
            print(f"      → Hyphenated word detected")
            parts = word.split('-')
            print(f"      → Parts: {parts}")
            normalized_parts = []
            for part in parts:
                print(f"        Processing part: '{part}'")
                if part.upper() in self.technical_terms:
                    normalized_part = part.upper()
                    print(f"          → Technical term: '{normalized_part}'")
                    normalized_parts.append(normalized_part)
                elif self.should_preserve_case(part):
                    print(f"          → Preserve case: '{part}'")
                    normalized_parts.append(part)
                else:
                    normalized_part = part.lower().capitalize()
                    print(f"          → Capitalize: '{normalized_part}'")
                    normalized_parts.append(normalized_part)
            result = '-'.join(normalized_parts)
            print(f"      → Final hyphenated result: '{result}'")
            return result
        
        # Regular proper case for normal words
        result = word.lower().capitalize()
        print(f"      → Regular capitalization: '{result}'")
        return result
    
    def normalize_text(self, text):
        """Normalize text while preserving technical terms and acronyms."""
        print(f"\n🚀 normalize_text('{text}'):")
        
        if not text or not isinstance(text, str):
            return text
        
        # Enhanced tokenization - this is the key issue!
        tokens = re.findall(r'\b\w+\b|\s+|[^\w\s]', text)
        print(f"  📝 Tokens: {tokens}")
        
        normalized_tokens = []
        for token in tokens:
            if re.match(r'\b\w+\b', token):  # It's a word
                normalized_token = self.normalize_word(token)
                normalized_tokens.append(normalized_token)
            else:  # It's whitespace or punctuation
                normalized_tokens.append(token)
        
        result = ''.join(normalized_tokens)
        print(f"  ✨ Final result: '{result}'\n")
        return result

def test_failing_cases():
    normalizer = DebugNormalizer()
    
    test_cases = [
        "Motor control ECU",
        "Power control ECU", 
        "DC Converter",
        "DC-AC Inverter",
        "DC-DC/AC-DC Converter",
        "EV ECU",
        "e-Axle"
    ]
    
    print("🚨 Testing Actual Failing Cases")
    print("=" * 80)
    
    for test_text in test_cases:
        result = normalizer.normalize_text(test_text)
        print(f"📊 RESULT: '{test_text}' → '{result}'")
        print("-" * 80)

if __name__ == "__main__":
    test_failing_cases()
