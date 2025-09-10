#!/usr/bin/env python3
"""
Script to process nodes.csv and create:
1. A JSON file with hierarchical relationships
2. A Mermaid diagram for visualization
"""

import csv
import json
from collections import defaultdict

def clean_field(field):
    """Remove quotes and handle NULL values"""
    if field == 'NULL' or field == '':
        return None
    return field.strip('"')

def process_csv(filename):
    """Read and process the CSV file"""
    nodes = {}
    children_map = defaultdict(list)
    
    with open(filename, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            node_id = clean_field(row['id'])
            pid = clean_field(row['pid'])
            name = clean_field(row['name'])
            level = clean_field(row['level'])
            
            # Store node information
            nodes[node_id] = {
                'id': node_id,
                'name': name,
                'pid': pid,
                'level': level,
                'children': []
            }
            
            # Build parent-child relationships
            if pid and pid != 'NULL':
                children_map[pid].append(node_id)
    
    # Add children to each node
    for parent_id, child_ids in children_map.items():
        if parent_id in nodes:
            nodes[parent_id]['children'] = child_ids
    
    return nodes, children_map

def create_json_structure(nodes):
    """Create a hierarchical JSON structure"""
    # Find root nodes (those with no parent or NULL parent)
    root_nodes = []
    
    for node_id, node in nodes.items():
        if node['pid'] is None:
            root_nodes.append(build_tree(node_id, nodes))
    
    return root_nodes

def build_tree(node_id, nodes):
    """Recursively build tree structure"""
    if node_id not in nodes:
        return None
    
    node = nodes[node_id].copy()
    node['children'] = []
    
    for child_id in nodes[node_id]['children']:
        child_tree = build_tree(child_id, nodes)
        if child_tree:
            node['children'].append(child_tree)
    
    return node

def create_mermaid_diagram(nodes, max_depth=3):
    """Create a Mermaid diagram (limited depth to avoid overwhelming output)"""
    mermaid_lines = ["graph TD"]
    
    # Start with root nodes
    for node_id, node in nodes.items():
        if node['pid'] is None:
            add_mermaid_nodes(node_id, nodes, mermaid_lines, 0, max_depth)
    
    return "\n".join(mermaid_lines)

def add_mermaid_nodes(node_id, nodes, mermaid_lines, current_depth, max_depth):
    """Recursively add nodes to mermaid diagram"""
    if current_depth > max_depth or node_id not in nodes:
        return
    
    node = nodes[node_id]
    
    # Clean node name for mermaid (remove special characters)
    clean_name = node['name'].replace('"', '').replace("'", "").replace("[", "").replace("]", "")
    if len(clean_name) > 50:
        clean_name = clean_name[:47] + "..."
    
    # Add node definition
    mermaid_lines.append(f'    {node_id}["{clean_name}"]')
    
    # Add connections to children
    for child_id in node['children']:
        if child_id in nodes:
            child_node = nodes[child_id]
            child_clean_name = child_node['name'].replace('"', '').replace("'", "").replace("[", "").replace("]", "")
            if len(child_clean_name) > 50:
                child_clean_name = child_clean_name[:47] + "..."
            
            mermaid_lines.append(f'    {child_id}["{child_clean_name}"]')
            mermaid_lines.append(f'    {node_id} --> {child_id}')
            
            # Recursively add children
            add_mermaid_nodes(child_id, nodes, mermaid_lines, current_depth + 1, max_depth)

def main():
    # Process the CSV file
    print("Processing nodes.csv...")
    nodes, children_map = process_csv('nodes.csv')
    
    print(f"Found {len(nodes)} nodes")
    print(f"Found {len([n for n in nodes.values() if n['pid'] is None])} root nodes")
    
    # Create hierarchical JSON structure
    print("Creating JSON structure...")
    json_structure = create_json_structure(nodes)
    
    # Save JSON file
    with open('nodes_hierarchy.json', 'w', encoding='utf-8') as f:
        json.dump(json_structure, f, indent=2, ensure_ascii=False)
    
    print("Created nodes_hierarchy.json")
    
    # Create Mermaid diagram
    print("Creating Mermaid diagram...")
    mermaid_content = create_mermaid_diagram(nodes, max_depth=2)  # Limit depth for readability
    
    # Save Mermaid file
    with open('organigram.mmd', 'w', encoding='utf-8') as f:
        f.write(mermaid_content)
    
    print("Created organigram.mmd")
    
    # Create an HTML file to view the Mermaid diagram
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Nodes Organigram</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
</head>
<body>
    <h1>Nodes Organigram</h1>
    <div class="mermaid">
{mermaid_content}
    </div>
    
    <script>
        mermaid.initialize({{ startOnLoad: true }});
    </script>
</body>
</html>"""
    
    with open('organigram.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("Created organigram.html for viewing the diagram")
    
    # Print some statistics
    level_counts = defaultdict(int)
    for node in nodes.values():
        level_counts[node['level']] += 1
    
    print("\nLevel distribution:")
    for level, count in sorted(level_counts.items()):
        print(f"  {level}: {count} nodes")

if __name__ == "__main__":
    main()
