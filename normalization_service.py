#!/usr/bin/env python3
"""
Intelligent Label Normalization Service
Provides smart text normalization that preserves technical acronyms and abbreviations.
"""

import re
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from spellchecker import SpellChecker

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8000", "http://127.0.0.1:8000", "file://"])  # Allow specific origins

class IntelligentNormalizer:
    def __init__(self):
        self.spell = SpellChecker()
        
        # Common technical acronyms and abbreviations that should be preserved
        self.technical_terms = {
            # Electronics/Computing
            'ABS', 'AC', 'DC', 'LED', 'LCD', 'OLED', 'RAM', 'ROM', 'CPU', 'GPU', 'SSD', 'HDD',
            'USB', 'HDMI', 'VGA', 'DVI', 'API', 'SDK', 'IDE', 'GUI', 'CLI', 'OS', 'IP', 'TCP',
            'UDP', 'HTTP', 'HTTPS', 'FTP', 'SSH', 'SSL', 'TLS', 'DNS', 'URL', 'URI', 'JSON',
            'XML', 'HTML', 'CSS', 'JS', 'SQL', 'NoSQL', 'AI', 'ML', 'AR', 'VR', 'IoT', 'GPS',
            'WIFI', 'LTE', '5G', '4G', '3G', 'RFID', 'NFC', 'QR', 'OCR', 'PDF', 'CSV', 'PNG',
            'JPG', 'JPEG', 'GIF', 'SVG', 'MP3', 'MP4', 'AVI', 'MOV', 'WAV', 'FLAC',
            
            # Chemistry/Materials
            'CMOS', 'BJT', 'FET', 'MOSFET', 'IC', 'PCB', 'SMD', 'THT', 'PWM', 'ADC', 'DAC',
            'PLL', 'PID', 'EMI', 'EMC', 'ESD', 'RF', 'IF', 'LF', 'HF', 'UHF', 'VHF',
            'SMC', 'CFRP', 'GFRP', 'FRP', 'RTM', 'BMC', 'GMT', 'LFT', 'CF', 'GF', 'PP', 'PE',
            'PA', 'PC', 'POM', 'PEEK', 'PEI', 'PSU', 'TPU', 'PVC', 'ABS', 'SAN', 'PBT', 'PET',
            
            # Business/Standards
            'ISO', 'IEEE', 'ANSI', 'NIST', 'FDA', 'CE', 'FCC', 'UL', 'RoHS', 'REACH',
            'GDP', 'ROI', 'KPI', 'SLA', 'CRM', 'ERP', 'HR', 'IT', 'QA', 'QC', 'R&D',
            'CEO', 'CTO', 'CFO', 'COO', 'VP', 'SVP', 'EVP', 'MD', 'GM', 'PM', 'BA',
            
            # Automotive
            'ABS', 'ACC', 'ADAS', 'AEB', 'AFR', 'AGM', 'AWD', 'BMS', 'CAN', 'CVT', 'DCT',
            'DPF', 'DSC', 'DSG', 'EBD', 'ECU', 'EGR', 'EPS', 'ESC', 'ESP', 'EV', 'FCW',
            'FWD', 'HEV', 'HUD', 'ICE', 'LDW', 'LKAS', 'MAF', 'MAP', 'MIL', 'OBDII',
            'PHEV', 'RWD', 'SCR', 'TCU', 'TPMS', 'TCS', 'TSI', 'TFSI', 'TDI', 'VIN',
            'VSC', 'VVT', 'VTEC', 'V2V', 'V2X', 'V2I', 'LIN', 'MOST', 'FlexRay',
            'TAPS', 'CBC', 'MKB', 'RMI', 'CDP',  # Additional automotive safety/control systems
            
            # Automotive Components/Parts
            'A/C', 'ACM', 'BCM', 'HVAC', 'EGT', 'IAT', 'O2', 'CKP', 'CMP', 'TPS', 'IAC',
            'PCV', 'EVAP', 'CAT', 'DOC', 'DPF', 'GPF', 'NOX', 'TWC', 'HEGO', 'UEGO',
            'AFM', 'VAF', 'MAF', 'MAP', 'BARO', 'CTS', 'ECT', 'EOT', 'IAT', 'CHT',
            'VVT-i', 'MIVEC', 'AVCS', 'CVVT', 'DVVT', 'VANOS', 'VarioCam', 'MultiAir',
            'GDI', 'FSI', 'MPFI', 'TBI', 'PFI', 'CRDi', 'CDI', 'HDi', 'dCi', 'CRDI',
            'DMF', 'SMF', 'LSD', 'ATF', 'MTF', 'DEXRON', 'CVT', 'DSG', 'PDK', 'SMG',
            'DCT', 'AMT', 'AGS', 'AT', 'MT', 'IMT', 'HGV', 'LCV', 'SUV', 'MPV', 'BEV',
            
            # Automotive Materials
            'HSS', 'AHSS', 'UHSS', 'BIW', 'BIP', 'CRP', 'CFRP', 'GFRP', 'SMC', 'BMC',
            'RTM', 'RIM', 'LFT', 'GMT', 'TPO', 'TEO', 'PUR', 'EPP', 'EPS', 'POM', 'PA6',
            'PA66', 'PBT', 'PET', 'ABS', 'PC/ABS', 'ASA', 'SAN', 'PMMA', 'PP', 'PE',
            'HDPE', 'LDPE', 'LLDPE', 'EVA', 'EPDM', 'SBR', 'NBR', 'CR', 'NR', 'BR',
            'IIR', 'BIIR', 'CIIR', 'ACM', 'AEM', 'ECO', 'FKM', 'FFKM', 'VMQ', 'FVMQ',
            'AU', 'EU', 'HNBR', 'CSM', 'CPE', 'PVC', 'TPE', 'TPU', 'TPV', 'TPC', 'TPS',
            
            # File extensions and formats
            'PDF', 'DOC', 'DOCX', 'XLS', 'XLSX', 'PPT', 'PPTX', 'TXT', 'RTF', 'ODT',
            'ZIP', 'RAR', '7Z', 'TAR', 'GZ', 'BZ2', 'ISO', 'IMG', 'DMG', 'EXE', 'MSI',
            
            # Units and measurements
            'MHz', 'GHz', 'THz', 'kHz', 'Hz', 'V', 'mV', 'kV', 'A', 'mA', 'uA', 'W', 'mW',
            'kW', 'MW', 'VA', 'VAR', 'Ohm', 'F', 'uF', 'nF', 'pF', 'H', 'mH', 'uH', 'nH',
            'dB', 'dBm', 'dBi', 'dBc', 'ppm', 'ppb', 'pH'
        }
        
        # Patterns for technical terms
        self.technical_patterns = [
            r'^[A-Z]{2,6}$',  # 2-6 letter acronyms
            r'^[A-Z]+\d+$',   # Acronym followed by numbers (e.g., USB3, 5G)
            r'^\d+[A-Z]+$',   # Numbers followed by letters (e.g., 3G, 4K)
            r'^[A-Z]&[A-Z]$', # A&B pattern (e.g., R&D)
            r'^[A-Z]+/[A-Z]+$', # A/B pattern (e.g., AC/DC)
        ]
        
        # Exception patterns that should be preserved as-is
        self.preserve_patterns = [
            r'^[A-Z]{2,}$',     # All caps (likely acronyms)
            r'^[A-Z]+\d+$',     # Mixed letters and numbers
            r'.*e-mail.*',      # e-mail variations
            r'.*i-\w+.*',       # i-prefixed words
        ]
    
    def is_technical_term(self, word):
        """Check if a word is a technical term that should be preserved."""
        word_upper = word.upper()
        
        # Check against known technical terms
        if word_upper in self.technical_terms:
            return True
        
        # Check against technical patterns
        for pattern in self.technical_patterns:
            if re.match(pattern, word):
                return True
        
        return False
    
    def is_real_word(self, word):
        """Check if a word is in the dictionary."""
        # Clean the word for spell checking
        clean_word = re.sub(r'[^a-zA-Z]', '', word.lower())
        if len(clean_word) < 2:
            return False
        
        return clean_word in self.spell
    
    def should_preserve_case(self, word):
        """Determine if a word's case should be preserved."""
        # Check preserve patterns (case-sensitive for acronym detection)
        for pattern in self.preserve_patterns:
            if re.match(pattern, word):  # Removed re.IGNORECASE
                return True
        
        # If it's all uppercase and is a technical term, preserve it
        if word.isupper() and self.is_technical_term(word):
            return True
        
        # If it's all uppercase but NOT a real word, it's likely an acronym
        if word.isupper() and not self.is_real_word(word):
            return True
        
        # Special case: if it's a known technical term regardless of case, preserve its uppercase form
        if word.upper() in self.technical_terms:
            return True
        
        return False
    
    def normalize_word(self, word):
        """Normalize a single word with intelligent case handling."""
        # Handle empty or very short words
        if len(word) < 2:
            return word
        
        # Check if this word should be converted to uppercase (known technical terms)
        if word.upper() in self.technical_terms:
            return word.upper()
        
        # Preserve case for technical terms and acronyms
        if self.should_preserve_case(word):
            return word
        
        # Handle hyphenated words
        if '-' in word:
            parts = word.split('-')
            normalized_parts = []
            for part in parts:
                if part.upper() in self.technical_terms:
                    normalized_parts.append(part.upper())
                elif self.should_preserve_case(part):
                    normalized_parts.append(part)
                else:
                    normalized_parts.append(part.lower().capitalize())
            return '-'.join(normalized_parts)
        
        # Handle words with apostrophes
        if "'" in word:
            # Don't change case for contractions like "don't", "can't"
            if word.lower() in ["don't", "can't", "won't", "shouldn't", "couldn't", "wouldn't"]:
                return word.lower()
            # For possessives, capitalize the main word
            if word.endswith("'s") or word.endswith("'S"):
                main_word = word[:-2]
                if main_word.upper() in self.technical_terms:
                    return main_word.upper() + "'s"
                elif self.should_preserve_case(main_word):
                    return main_word + "'s"
                else:
                    return main_word.lower().capitalize() + "'s"
        
        # Regular proper case for normal words
        return word.lower().capitalize()
    
    def normalize_text(self, text):
        """Normalize text while preserving technical terms and acronyms."""
        if not text or not isinstance(text, str):
            return text
        
        # Enhanced tokenization that better handles parentheses and punctuation
        # This regex captures: words, spaces, and punctuation separately
        tokens = re.findall(r'\b\w+\b|\s+|[^\w\s]', text)
        
        normalized_tokens = []
        for token in tokens:
            if re.match(r'\b\w+\b', token):  # It's a word
                normalized_tokens.append(self.normalize_word(token))
            else:  # It's whitespace or punctuation
                normalized_tokens.append(token)
        
        return ''.join(normalized_tokens)
    
    def analyze_text(self, text):
        """Analyze text and provide detailed information about normalization."""
        if not text or not isinstance(text, str):
            return {
                'original': text,
                'normalized': text,
                'changed': False,
                'preserved_terms': [],
                'normalized_words': []
            }
        
        original = text
        normalized = self.normalize_text(text)
        
        # Find preserved terms
        words = re.findall(r'\b\w+\b', text)
        preserved_terms = [word for word in words if self.should_preserve_case(word)]
        
        # Find normalized words
        original_words = re.findall(r'\b\w+\b', original)
        normalized_words = re.findall(r'\b\w+\b', normalized)
        
        changed_words = []
        for i, (orig, norm) in enumerate(zip(original_words, normalized_words)):
            if orig != norm:
                changed_words.append({
                    'original': orig,
                    'normalized': norm,
                    'position': i
                })
        
        return {
            'original': original,
            'normalized': normalized,
            'changed': original != normalized,
            'preserved_terms': preserved_terms,
            'normalized_words': changed_words
        }

# Initialize the normalizer
normalizer = IntelligentNormalizer()

@app.route('/normalize', methods=['POST'])
def normalize_labels():
    """Normalize a list of labels."""
    try:
        data = request.get_json()
        labels = data.get('labels', [])
        
        results = []
        for label in labels:
            analysis = normalizer.analyze_text(label)
            results.append(analysis)
        
        return jsonify({
            'success': True,
            'results': results
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/normalize-text', methods=['POST'])
def normalize_single_text():
    """Normalize a single text and return simple result."""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({
                'success': False,
                'error': 'No text provided'
            }), 400
        
        analysis = normalizer.analyze_text(text)
        
        return jsonify({
            'normalized_text': analysis['normalized'],
            'preserved_terms': analysis['preserved_terms'],
            'success': True
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/analyze', methods=['POST'])
def analyze_text():
    """Analyze a single text for normalization."""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        analysis = normalizer.analyze_text(text)
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'Intelligent Label Normalization Service'
    })

if __name__ == '__main__':
    print("Starting Intelligent Label Normalization Service...")
    print("Service will be available at http://localhost:5000")
    app.run(debug=True, port=5000, host='127.0.0.1')
