#!/usr/bin/env python3
"""
Test the API using built-in urllib instead of requests
"""

import urllib.request
import urllib.parse
import json

def test_api():
    url = "http://localhost:5000/normalize-text"
    
    test_cases = [
        # Original failing cases from user
        "DC-AC Inverter",
        "DC-DC/AC-DC Converter", 
        "Motor control ECU",
        "Power control ECU",
        # Also test lowercase variants
        "dc-ac inverter",
        "dc-dc/ac-dc converter", 
        "motor control ecu",
        "power control ecu"
    ]
    
    print("🚨 Testing Flask API with urllib")
    print("=" * 60)
    
    for test_text in test_cases:
        try:
            print(f"🔍 Testing: '{test_text}'")
            
            # Prepare the data
            data = json.dumps({"text": test_text}).encode('utf-8')
            print(f"📤 Sending data: {data}")
            
            # Create the request
            req = urllib.request.Request(url, data=data)
            req.add_header('Content-Type', 'application/json')
            print(f"📡 Making request to: {url}")
            
            # Make the request
            with urllib.request.urlopen(req) as response:
                print(f"📊 Response status: {response.status}")
                result = json.loads(response.read().decode('utf-8'))
                
                print(f"✅ '{test_text}'")
                print(f"   → '{result['normalized_text']}'")
                print(f"   Preserved: {result['preserved_terms']}")
                
        except Exception as e:
            print(f"❌ Error for '{test_text}': {e}")
        
        print("-" * 40)

if __name__ == "__main__":
    test_api()
