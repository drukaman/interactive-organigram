#!/usr/bin/env python3
"""
Demo script for the import functionality
Shows how to use the CSV/Excel import tools
"""

import os
import sys
from pathlib import Path

def create_sample_csv():
    """Create a sample CSV file for demonstration"""
    sample_data = """name,id,pid,level
"Technology Stack","1",NULL,"l1"
"Frontend","2","1","l2"
"Backend","3","1","l2"
"Database","4","1","l2"
"React.js","5","2","l3"
"Vue.js","6","2","l3"
"HTML/CSS","7","2","l3"
"Node.js","8","3","l3"
"Python","9","3","l3"
"Java","10","3","l3"
"PostgreSQL","11","4","l3"
"MongoDB","12","4","l3"
"Redis","13","4","l3"
"React Components","14","5","l4"
"React Hooks","15","5","l4"
"Vue Components","16","6","l4"
"Responsive Design","17","7","l4"
"Express.js","18","8","l4"
"FastAPI","19","9","l4"
"Spring Boot","20","10","l4"
"""

    with open('sample_tech_stack.csv', 'w') as f:
        f.write(sample_data)
    
    return 'sample_tech_stack.csv'

def main():
    print("🔧 Import Functionality Demo")
    print("=" * 50)
    print()
    
    print("This demo shows how to import CSV and Excel files into the organigram.")
    print()
    
    print("📋 Available Import Tools:")
    print("  1. import_organigram_simple.py  - CSV only (no dependencies)")
    print("  2. import_organigram_advanced.py - CSV + Excel (requires pandas)")
    print()
    
    choice = input("Would you like to:\n1. Create and import a sample CSV\n2. Import an existing file\n3. View usage instructions\nEnter choice (1/2/3): ").strip()
    
    if choice == "1":
        # Create sample file and import it
        print("\n📝 Creating sample CSV file...")
        sample_file = create_sample_csv()
        print(f"✅ Created: {sample_file}")
        
        print(f"\n🔄 Importing {sample_file}...")
        os.system(f"python3 import_organigram_simple.py {sample_file} -o sample_hierarchy.json")
        
        print(f"\n🌐 Testing with organigram...")
        if os.path.exists('sample_hierarchy.json'):
            # Copy to the main hierarchy file for testing
            os.system("cp sample_hierarchy.json nodes_hierarchy_sample.json")
            print("✅ Sample data ready!")
            print("📁 Files created:")
            print(f"  - {sample_file} (source CSV)")
            print(f"  - sample_hierarchy.json (organigram JSON)")
            
            print(f"\n🌐 To test with the organigram:")
            print(f"  1. Rename sample_hierarchy.json to nodes_hierarchy.json")
            print(f"  2. Open your organigram in the browser")
            print(f"  3. You'll see the sample tech stack hierarchy")
        
    elif choice == "2":
        file_path = input("\n📁 Enter path to your CSV or Excel file: ").strip()
        
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return
        
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.csv':
            print(f"\n📋 Using simple importer for CSV file...")
            cmd = f"python3 import_organigram_simple.py '{file_path}'"
        elif file_ext in ['.xlsx', '.xls']:
            print(f"\n📋 Using advanced importer for Excel file...")
            print("ℹ️  Note: This requires pandas and openpyxl")
            cmd = f"python3 import_organigram_advanced.py '{file_path}'"
        else:
            print(f"❌ Unsupported file format: {file_ext}")
            print("📋 Supported formats: .csv, .xlsx, .xls")
            return
        
        print(f"🔄 Running: {cmd}")
        os.system(cmd)
        
    elif choice == "3":
        show_usage_instructions()
        
    else:
        print("Invalid choice. Please run the script again.")
        return

def show_usage_instructions():
    """Display detailed usage instructions"""
    print("\n📚 Import Usage Instructions")
    print("=" * 50)
    
    print("\n🔧 Required File Format:")
    print("Your CSV or Excel file must have these columns:")
    print("  - name: Node name/description")
    print("  - id: Unique identifier for each node")
    print("  - pid: Parent ID (NULL or empty for root nodes)")
    print("  - level: Hierarchical level (e.g., l1, l2, l3, l4)")
    
    print("\n📝 Example CSV Structure:")
    print('''
name,id,pid,level
"Company","1",NULL,"l1"
"Engineering","2","1","l2"
"Frontend Team","3","2","l3"
"John Doe","4","3","l4"
"Jane Smith","5","3","l4"
    ''')
    
    print("\n🚀 Basic Usage:")
    print("# CSV files (no dependencies needed):")
    print("python3 import_organigram_simple.py your_file.csv")
    print("")
    print("# Excel files (requires pandas + openpyxl):")
    print("pip install -r requirements.txt")
    print("python3 import_organigram_advanced.py your_file.xlsx")
    
    print("\n⚙️  Advanced Options:")
    print("# Specify output file:")
    print("python3 import_organigram_simple.py data.csv -o custom_name.json")
    print("")
    print("# Validate file structure only:")
    print("python3 import_organigram_simple.py data.csv --validate-only")
    print("")
    print("# Excel with specific sheet:")
    print("python3 import_organigram_advanced.py data.xlsx -s 'Sheet2'")
    
    print("\n🔍 Troubleshooting:")
    print("• Make sure your file has all required columns")
    print("• Check that ID values are unique")
    print("• Verify parent IDs exist for non-root nodes")
    print("• Use NULL or empty for root node parent IDs")
    print("• Ensure proper encoding (UTF-8 recommended)")
    
    print("\n📁 Output:")
    print("• Creates a JSON file compatible with the organigram")
    print("• Shows statistics about your data structure")
    print("• Reports any data quality issues")
    print("• Ready to use with the interactive organigram")

if __name__ == "__main__":
    main()
