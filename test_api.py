#!/usr/bin/env python3
"""
Test the Flask API directly to ensure it's working correctly
"""

import requests
import json

def test_api():
    url = "http://localhost:5000/normalize-text"
    
    test_cases = [
        "Controller deceleration parking (CDP)",
        "Anti-lock braking system (ABS)", 
        "Electronic control unit (ECU)",
        "Traction and parking stability (TAPS)"
    ]
    
    print("🚨 Testing Flask API Directly")
    print("=" * 60)
    
    for test_text in test_cases:
        try:
            response = requests.post(url, 
                                   json={"text": test_text},
                                   headers={"Content-Type": "application/json"})
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ '{test_text}'")
                print(f"   → '{result['normalized_text']}'")
                print(f"   Preserved: {result['preserved_terms']}")
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Connection failed - is service running?")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 40)

if __name__ == "__main__":
    test_api()
