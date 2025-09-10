#!/usr/bin/env python3
"""
File Import Utility for Interactive Organigram
Converts CSV and Excel files to the JSON format required by the organigram application
"""

import csv
import json
import pandas as pd
import argparse
import os
import sys
from collections import defaultdict
from pathlib import Path

class OrganigramImporter:
    def __init__(self):
        self.nodes = {}
        self.children_map = defaultdict(list)
        self.required_columns = ['name', 'id', 'pid', 'level']
        
    def clean_field(self, field):
        """Remove quotes and handle NULL/empty values"""
        if pd.isna(field) or field == 'NULL' or field == '' or field is None:
            return None
        return str(field).strip().strip('"')
    
    def validate_columns(self, df):
        """Validate that required columns are present"""
        missing_columns = [col for col in self.required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        print(f"✅ Found all required columns: {self.required_columns}")
        
        # Check for additional columns
        extra_columns = [col for col in df.columns if col not in self.required_columns]
        if extra_columns:
            print(f"ℹ️  Found additional columns (will be ignored): {extra_columns}")
    
    def load_csv(self, file_path):
        """Load data from CSV file"""
        print(f"📁 Loading CSV file: {file_path}")
        
        try:
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
            df = None
            
            for encoding in encodings:
                try:
                    df = pd.read_csv(file_path, encoding=encoding)
                    print(f"✅ Successfully loaded with {encoding} encoding")
                    break
                except UnicodeDecodeError:
                    continue
            
            if df is None:
                raise ValueError("Could not read CSV file with any supported encoding")
            
            return df
            
        except Exception as e:
            raise ValueError(f"Error reading CSV file: {str(e)}")
    
    def load_excel(self, file_path, sheet_name=None):
        """Load data from Excel file"""
        print(f"📁 Loading Excel file: {file_path}")
        
        try:
            # Check if openpyxl is available for .xlsx files
            if file_path.endswith('.xlsx'):
                try:
                    import openpyxl
                except ImportError:
                    raise ValueError("openpyxl is required for .xlsx files. Install with: pip install openpyxl")
            
            # List available sheets if no sheet specified
            if sheet_name is None:
                xl_file = pd.ExcelFile(file_path)
                if len(xl_file.sheet_names) > 1:
                    print(f"📋 Available sheets: {xl_file.sheet_names}")
                    print(f"📋 Using first sheet: '{xl_file.sheet_names[0]}'")
                sheet_name = xl_file.sheet_names[0]
            
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            print(f"✅ Successfully loaded sheet: '{sheet_name}'")
            
            return df
            
        except Exception as e:
            raise ValueError(f"Error reading Excel file: {str(e)}")
    
    def process_dataframe(self, df):
        """Process the dataframe and build node relationships"""
        print(f"🔄 Processing {len(df)} rows...")
        
        self.validate_columns(df)
        
        # Clean and process each row
        for index, row in df.iterrows():
            try:
                node_id = self.clean_field(row['id'])
                pid = self.clean_field(row['pid'])
                name = self.clean_field(row['name'])
                level = self.clean_field(row['level'])
                
                # Skip rows with missing essential data
                if not node_id or not name:
                    print(f"⚠️  Skipping row {index + 1}: Missing ID or name")
                    continue
                
                # Store node information
                self.nodes[node_id] = {
                    'id': node_id,
                    'name': name,
                    'pid': pid,
                    'level': level,
                    'children': []
                }
                
                # Build parent-child relationships
                if pid and pid != 'NULL':
                    self.children_map[pid].append(node_id)
                    
            except Exception as e:
                print(f"⚠️  Error processing row {index + 1}: {str(e)}")
                continue
        
        # Add children to each node
        for parent_id, child_ids in self.children_map.items():
            if parent_id in self.nodes:
                self.nodes[parent_id]['children'] = child_ids
        
        print(f"✅ Processed {len(self.nodes)} nodes successfully")
    
    def create_hierarchical_structure(self):
        """Create the hierarchical JSON structure"""
        print("🌳 Building hierarchical structure...")
        
        # Find root nodes (those with no parent or NULL parent)
        root_nodes = []
        
        for node_id, node in self.nodes.items():
            if node['pid'] is None:
                root_nodes.append(self.build_tree(node_id))
        
        print(f"🌲 Found {len(root_nodes)} root nodes")
        return root_nodes
    
    def build_tree(self, node_id):
        """Recursively build tree structure"""
        if node_id not in self.nodes:
            return None
        
        node = self.nodes[node_id].copy()
        node['children'] = []
        
        for child_id in self.nodes[node_id]['children']:
            child_tree = self.build_tree(child_id)
            if child_tree:
                node['children'].append(child_tree)
        
        return node
    
    def generate_statistics(self, hierarchy):
        """Generate statistics about the imported data"""
        stats = {
            'total_nodes': len(self.nodes),
            'root_nodes': len(hierarchy),
            'levels': defaultdict(int),
            'max_children': 0,
            'orphaned_nodes': []
        }
        
        # Count nodes by level and find max children
        for node in self.nodes.values():
            if node['level']:
                stats['levels'][node['level']] += 1
            
            children_count = len(node['children'])
            if children_count > stats['max_children']:
                stats['max_children'] = children_count
            
            # Check for orphaned nodes (have parent ID but parent doesn't exist)
            if node['pid'] and node['pid'] not in self.nodes:
                stats['orphaned_nodes'].append({
                    'id': node['id'],
                    'name': node['name'],
                    'missing_parent': node['pid']
                })
        
        return stats
    
    def save_json(self, hierarchy, output_path):
        """Save the hierarchical structure to JSON file"""
        print(f"💾 Saving to: {output_path}")
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(hierarchy, f, indent=2, ensure_ascii=False)
            
            file_size = os.path.getsize(output_path)
            print(f"✅ JSON file saved successfully ({file_size:,} bytes)")
            
        except Exception as e:
            raise ValueError(f"Error saving JSON file: {str(e)}")
    
    def import_file(self, input_path, output_path=None, sheet_name=None):
        """Main import function"""
        input_path = Path(input_path)
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        # Determine output path if not specified
        if output_path is None:
            output_path = input_path.with_name(f"{input_path.stem}_hierarchy.json")
        
        print(f"🚀 Starting import process...")
        print(f"📄 Input: {input_path}")
        print(f"📄 Output: {output_path}")
        
        # Load file based on extension
        file_ext = input_path.suffix.lower()
        
        if file_ext == '.csv':
            df = self.load_csv(input_path)
        elif file_ext in ['.xlsx', '.xls']:
            df = self.load_excel(input_path, sheet_name)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}. Supported formats: .csv, .xlsx, .xls")
        
        # Process the data
        self.process_dataframe(df)
        
        # Create hierarchical structure
        hierarchy = self.create_hierarchical_structure()
        
        # Generate and display statistics
        stats = self.generate_statistics(hierarchy)
        self.display_statistics(stats)
        
        # Save JSON file
        self.save_json(hierarchy, output_path)
        
        print(f"\n🎉 Import completed successfully!")
        print(f"📁 JSON file created: {output_path}")
        print(f"🌐 You can now use this file with the interactive organigram")
        
        return output_path, stats
    
    def display_statistics(self, stats):
        """Display import statistics"""
        print("\n📊 Import Statistics:")
        print("=" * 50)
        print(f"Total Nodes: {stats['total_nodes']:,}")
        print(f"Root Nodes: {stats['root_nodes']}")
        print(f"Max Children per Node: {stats['max_children']}")
        
        print("\nLevel Distribution:")
        for level, count in sorted(stats['levels'].items()):
            print(f"  {level}: {count:,} nodes")
        
        if stats['orphaned_nodes']:
            print(f"\n⚠️  Found {len(stats['orphaned_nodes'])} orphaned nodes:")
            for node in stats['orphaned_nodes'][:5]:  # Show first 5
                print(f"  - {node['name']} (ID: {node['id']}) -> Missing parent: {node['missing_parent']}")
            if len(stats['orphaned_nodes']) > 5:
                print(f"  ... and {len(stats['orphaned_nodes']) - 5} more")

def main():
    parser = argparse.ArgumentParser(
        description="Import CSV or Excel files for Interactive Organigram",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 import_organigram.py data.csv
  python3 import_organigram.py data.xlsx -o custom_output.json
  python3 import_organigram.py data.xlsx -s "Sheet2"
  
Required columns in input file:
  - name: Node name/description
  - id: Unique node identifier
  - pid: Parent node ID (NULL for root nodes)
  - level: Hierarchical level (e.g., l1, l2, l3, l4)
        """
    )
    
    parser.add_argument('input_file', help='Path to CSV or Excel file')
    parser.add_argument('-o', '--output', help='Output JSON file path (default: auto-generated)')
    parser.add_argument('-s', '--sheet', help='Excel sheet name (default: first sheet)')
    parser.add_argument('--validate-only', action='store_true', help='Only validate file structure without creating output')
    
    args = parser.parse_args()
    
    try:
        importer = OrganigramImporter()
        
        if args.validate_only:
            print("🔍 Validation mode - checking file structure only...")
            # Load and validate without saving
            input_path = Path(args.input_file)
            file_ext = input_path.suffix.lower()
            
            if file_ext == '.csv':
                df = importer.load_csv(input_path)
            elif file_ext in ['.xlsx', '.xls']:
                df = importer.load_excel(input_path, args.sheet)
            else:
                raise ValueError(f"Unsupported file format: {file_ext}")
            
            importer.validate_columns(df)
            print(f"✅ File structure is valid ({len(df)} rows)")
            
        else:
            output_path, stats = importer.import_file(
                input_path=args.input_file,
                output_path=args.output,
                sheet_name=args.sheet
            )
            
            print(f"\n🌐 To use with the organigram:")
            print(f"   1. Copy {output_path} to your organigram directory")
            print(f"   2. Rename it to 'nodes_hierarchy.json' (or update the application)")
            print(f"   3. Open the organigram application in your browser")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
