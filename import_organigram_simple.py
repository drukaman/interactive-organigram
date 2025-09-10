#!/usr/bin/env python3
"""
Simple File Import Utility for Interactive Organigram
Converts CSV files to JSON format using only built-in Python libraries
For Excel support, use import_organigram_advanced.py
"""

import csv
import json
import argparse
import os
import sys
from collections import defaultdict
from pathlib import Path

class SimpleOrganigramImporter:
    def __init__(self):
        self.nodes = {}
        self.children_map = defaultdict(list)
        self.required_columns = ['name', 'id', 'pid', 'level']
        
    def clean_field(self, field):
        """Remove quotes and handle NULL/empty values"""
        if not field or field == 'NULL' or field == '':
            return None
        return str(field).strip().strip('"')
    
    def load_csv(self, file_path):
        """Load data from CSV file"""
        print(f"📁 Loading CSV file: {file_path}")
        
        rows = []
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding, newline='') as file:
                    csv_reader = csv.DictReader(file)
                    rows = list(csv_reader)
                    print(f"✅ Successfully loaded with {encoding} encoding")
                    break
            except UnicodeDecodeError:
                continue
            except Exception as e:
                raise ValueError(f"Error reading CSV file: {str(e)}")
        
        if not rows:
            raise ValueError("Could not read CSV file with any supported encoding")
        
        return rows
    
    def validate_columns(self, rows):
        """Validate that required columns are present"""
        if not rows:
            raise ValueError("CSV file is empty")
        
        available_columns = list(rows[0].keys())
        missing_columns = [col for col in self.required_columns if col not in available_columns]
        
        if missing_columns:
            print(f"❌ Missing required columns: {missing_columns}")
            print(f"📋 Available columns: {available_columns}")
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        print(f"✅ Found all required columns: {self.required_columns}")
        
        # Check for additional columns
        extra_columns = [col for col in available_columns if col not in self.required_columns]
        if extra_columns:
            print(f"ℹ️  Found additional columns (will be ignored): {extra_columns}")
    
    def process_rows(self, rows):
        """Process the CSV rows and build node relationships"""
        print(f"🔄 Processing {len(rows)} rows...")
        
        self.validate_columns(rows)
        
        processed_count = 0
        skipped_count = 0
        
        for index, row in enumerate(rows):
            try:
                node_id = self.clean_field(row.get('id'))
                pid = self.clean_field(row.get('pid'))
                name = self.clean_field(row.get('name'))
                level = self.clean_field(row.get('level'))
                
                # Skip rows with missing essential data
                if not node_id or not name:
                    print(f"⚠️  Skipping row {index + 1}: Missing ID or name")
                    skipped_count += 1
                    continue
                
                # Check for duplicate IDs
                if node_id in self.nodes:
                    print(f"⚠️  Duplicate ID found: {node_id} (row {index + 1})")
                    skipped_count += 1
                    continue
                
                # Store node information
                self.nodes[node_id] = {
                    'id': node_id,
                    'name': name,
                    'pid': pid,
                    'level': level if level else 'unknown',
                    'children': []
                }
                
                # Build parent-child relationships
                if pid and pid != 'NULL':
                    self.children_map[pid].append(node_id)
                
                processed_count += 1
                    
            except Exception as e:
                print(f"⚠️  Error processing row {index + 1}: {str(e)}")
                skipped_count += 1
                continue
        
        # Add children to each node
        for parent_id, child_ids in self.children_map.items():
            if parent_id in self.nodes:
                self.nodes[parent_id]['children'] = child_ids
        
        print(f"✅ Processed {processed_count} nodes successfully")
        if skipped_count > 0:
            print(f"⚠️  Skipped {skipped_count} rows due to errors")
    
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
            'orphaned_nodes': [],
            'max_depth': 0
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
        
        # Calculate max depth
        def calculate_depth(node_list, depth=0):
            max_d = depth
            for node in node_list:
                if node.get('children'):
                    child_depth = calculate_depth(node['children'], depth + 1)
                    max_d = max(max_d, child_depth)
            return max_d
        
        stats['max_depth'] = calculate_depth(hierarchy)
        
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
    
    def import_csv(self, input_path, output_path=None):
        """Main import function for CSV files"""
        input_path = Path(input_path)
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        if input_path.suffix.lower() != '.csv':
            raise ValueError(f"This tool only supports CSV files. For Excel files, use import_organigram_advanced.py")
        
        # Determine output path if not specified
        if output_path is None:
            output_path = input_path.with_name(f"{input_path.stem}_hierarchy.json")
        
        print(f"🚀 Starting CSV import process...")
        print(f"📄 Input: {input_path}")
        print(f"📄 Output: {output_path}")
        
        # Load and process CSV
        rows = self.load_csv(input_path)
        self.process_rows(rows)
        
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
        print(f"Max Depth: {stats['max_depth']}")
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
        description="Import CSV files for Interactive Organigram (Built-in libraries only)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 import_organigram_simple.py data.csv
  python3 import_organigram_simple.py data.csv -o custom_output.json
  python3 import_organigram_simple.py data.csv --validate-only
  
Required columns in CSV file:
  - name: Node name/description
  - id: Unique node identifier
  - pid: Parent node ID (NULL or empty for root nodes)
  - level: Hierarchical level (e.g., l1, l2, l3, l4)

Note: For Excel file support, use import_organigram_advanced.py
        """
    )
    
    parser.add_argument('input_file', help='Path to CSV file')
    parser.add_argument('-o', '--output', help='Output JSON file path (default: auto-generated)')
    parser.add_argument('--validate-only', action='store_true', help='Only validate file structure without creating output')
    
    args = parser.parse_args()
    
    try:
        importer = SimpleOrganigramImporter()
        
        if args.validate_only:
            print("🔍 Validation mode - checking file structure only...")
            rows = importer.load_csv(args.input_file)
            importer.validate_columns(rows)
            print(f"✅ File structure is valid ({len(rows)} rows)")
            
        else:
            output_path, stats = importer.import_csv(
                input_path=args.input_file,
                output_path=args.output
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
