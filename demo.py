#!/usr/bin/env python3
"""
Demo script to showcase the interactive organigram features
"""

import webbrowser
import os
import time

def main():
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("🌟 Interactive Organigram Demo")
    print("=" * 50)
    print()
    
    print("This demo will open the interactive organigram pages in your browser.")
    print("You can explore the following features:")
    print()
    
    print("📊 BASIC INTERACTIVE FEATURES:")
    print("  • Click nodes to expand/collapse branches")
    print("  • Use search box to find specific nodes")
    print("  • Level buttons (L1, L1-2, L1-3, All) for quick navigation")
    print("  • Expand All / Collapse All buttons")
    print()
    
    print("🚀 ADVANCED FEATURES:")
    print("  • Statistics sidebar with detailed analytics")
    print("  • Node selection with breadcrumb navigation")
    print("  • Export functionality (JSON, CSV)")
    print("  • Enhanced search with highlighting")
    print("  • Keyboard shortcuts (Ctrl+F, Ctrl+E, Ctrl+C)")
    print()
    
    choice = input("Which version would you like to open?\n1. Basic Interactive (recommended for first-time users)\n2. Advanced Interactive (full features)\n3. Both\nEnter choice (1/2/3): ").strip()
    
    if choice == "1":
        basic_path = f"file://{current_dir}/interactive_organigram.html"
        print(f"\n🌐 Opening Basic Interactive Organigram...")
        webbrowser.open(basic_path)
        
    elif choice == "2":
        advanced_path = f"file://{current_dir}/advanced_organigram.html"
        print(f"\n🌐 Opening Advanced Interactive Organigram...")
        webbrowser.open(advanced_path)
        
    elif choice == "3":
        basic_path = f"file://{current_dir}/interactive_organigram.html"
        advanced_path = f"file://{current_dir}/advanced_organigram.html"
        
        print(f"\n🌐 Opening Basic Interactive Organigram...")
        webbrowser.open(basic_path)
        
        time.sleep(2)  # Brief delay
        
        print(f"🌐 Opening Advanced Interactive Organigram...")
        webbrowser.open(advanced_path)
        
    else:
        print("Invalid choice. Please run the script again.")
        return
    
    print("\n✨ Tips for exploring:")
    print("  • Start by clicking on root nodes (Level 1) to see main categories")
    print("  • Use the search box to find specific components")
    print("  • Try the level buttons to focus on different hierarchy depths")
    print("  • In Advanced version, click nodes to see detailed information")
    print("  • Use Ctrl+F to quick-search, Ctrl+E to expand all")
    
    print("\n📁 Available files:")
    print(f"  • interactive_organigram.html - Basic interactive view")
    print(f"  • advanced_organigram.html - Advanced interactive view")
    print(f"  • nodes_hierarchy.json - Raw data for developers")
    print(f"  • organigram_simple.html - Static Mermaid diagram overview")

if __name__ == "__main__":
    main()
