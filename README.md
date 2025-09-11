# 🌳 Interactive Organigram

A powerful, web-based interactive organigram (organizational chart) application with CSV import, inline editing, duplicate detection, and export capabilities.

![Interactive Organigram](https://img.shields.io/badge/Status-Active-green) ![Version](https://img.shields.io/badge/Version-1.0.0-blue) ![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

### 📁 **File Import & Export**

- **CSV Import**: Drag & drop or click to import CSV files
- **Excel Support**: Import .xlsx and .xls files (client-side CSV conversion)
- **Smart Validation**: Automatic validation of required columns
- **Export to CSV**: Download your edited data with all changes

### ✏️ **Inline Editing**

- **Edit Mode**: Toggle editing mode to modify node labels
- **Click to Edit**: Simply click any node name to edit it inline
- **Auto-save**: Changes are automatically saved
- **Real-time Updates**: See changes immediately in the hierarchy

### 🔍 **Duplicate Detection**

- **Smart Analysis**: Finds duplicate names within the same parent category
- **Visual Highlighting**: Duplicate nodes are highlighted with warning colors
- **Navigation Panel**: Bottom-right panel shows all duplicates with navigation
- **Path Context**: Shows full hierarchical path for each duplicate

### 🎯 **Interactive Navigation**

- **Collapsible Tree**: Expand/collapse nodes to explore hierarchy
- **Level Controls**: Show specific levels (L1, L1-2, etc.)
- **Search Function**: Fast search across all nodes
- **Smooth Scrolling**: Click duplicates to scroll to their location

### 🎨 **Modern Interface**

- **Clean Design**: Minimalist white/grey color scheme
- **Responsive Layout**: Works on desktop and mobile devices
- **Fixed Toolbar**: Always-accessible controls at the top
- **Compact Display**: Optimized for viewing large hierarchies

## 🚀 Quick Start

### Online Version

Visit the deployed application: [Your Render.com URL will go here]

### Local Development

1. Clone the repository:

```bash
git clone https://github.com/[your-username]/interactive-organigram.git
cd interactive-organigram
```

2. Install dependencies:

```bash
npm install
```

3. Start the server:

```bash
npm start
```

4. Open your browser to `http://localhost:3000`

## 📊 File Format

### Required CSV Columns

- **name**: Node name/description
- **id**: Unique identifier for the node
- **pid**: Parent ID (empty for root nodes)
- **level**: Hierarchical level (l1, l2, l3, l4)

### Example CSV Structure

```csv
name,id,pid,level
"Company","1",,"l1"
"Engineering","2","1","l2"
"Product","3","1","l2"
"Frontend Team","4","2","l3"
"Backend Team","5","2","l3"
"John Doe","6","4","l4"
"Jane Smith","7","4","l4"
```

## 🛠️ Usage Guide

### 1. Import Your Data

- Click **"📁 Import New File"** button
- Drag & drop your CSV file or click to browse
- Wait for validation and processing

### 2. Navigate the Hierarchy

- Use **Show L1**, **Show L1-2** buttons to expand levels
- Click **+/-** buttons on nodes to expand/collapse
- Use the **search bar** to find specific nodes

### 3. Edit Node Names

- Click **"✏️ Edit Mode"** to enable editing
- Click any node name to edit it inline
- Press Enter or click away to save changes

### 4. Find Duplicates

- Click **"🔍 Find Duplicates"** to analyze data
- Review highlighted duplicate nodes
- Use the bottom-right panel to navigate between duplicates

### 5. Export Your Changes

- Click **"💾 Export CSV"** to download edited data
- File will be saved as `[original_name]_edited.csv`

## 🌐 Deployment

### Render.com Deployment

1. Push your code to GitHub
2. Connect your repository to Render.com
3. Configure as a Web Service
4. Set build command: `npm install`
5. Set start command: `npm start`

### Environment Variables

- `PORT`: Server port (automatically set by Render.com)

## 🔧 Technical Stack

- **Frontend**: Pure HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Node.js with Express.js
- **Deployment**: Render.com compatible
- **File Processing**: Client-side CSV parsing
- **No Database**: Entirely file-based operation

## 📱 Browser Support

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Mobile browsers

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: Report bugs on GitHub Issues
- **Features**: Request features via GitHub Issues
- **Documentation**: Check this README and in-app help

## 🔄 Changelog

### v1.0.0 (2025-09-10)

- Initial release
- CSV import/export functionality
- Inline editing capabilities
- Duplicate detection and navigation
- Responsive design
- Render.com deployment support

---

**Built with ❤️ for better organizational data management**

- `id`: Node identifier
- `name`: Node name/description
- `pid`: Parent ID (null for root nodes)
- `level`: Hierarchical level (l1, l2, l3, l4)
- `children`: Array of child nodes

### 2. `organigram.mmd`

A Mermaid diagram file showing the complete hierarchy (limited to 3 levels deep for readability). This file contains 26,508 lines and shows detailed relationships.

### 3. `organigram_simple.mmd`

A simplified Mermaid diagram showing only the top 2 levels (l1 and l2) for better overview and readability.

### 4. `organigram.html`

An HTML file that renders the complete Mermaid diagram in a web browser.

### 5. `organigram_simple.html`

An HTML file that renders the simplified Mermaid diagram with additional information about the data structure.

### 6. `interactive_organigram.html` ⭐ **RECOMMENDED**

An interactive web page that displays a collapsible/expandable tree view of the organigram. Features include:

- **Collapsible/Expandable Nodes**: Click any node to expand or collapse its children
- **Search Functionality**: Real-time search with highlighting (Ctrl+F)
- **Level Controls**: Quick buttons to expand to specific levels (L1, L1-2, L1-3, All)
- **Statistics Dashboard**: Overview of node distribution and hierarchy metrics
- **Responsive Design**: Works on desktop and mobile devices
- **Keyboard Shortcuts**: Ctrl+E (expand all), Ctrl+C (collapse all)

### 7. `advanced_organigram.html` ⭐ **PREMIUM FEATURES**

An enhanced version with advanced features:

- **Enhanced Search**: Search by name or ID with breadcrumb navigation
- **Node Selection**: Click nodes to view detailed information
- **Statistics Sidebar**: Comprehensive analytics and selected node details
- **Export Functions**: Export data as JSON, CSV, or SVG
- **Breadcrumb Navigation**: Shows path to selected nodes
- **Enhanced UI**: Modern design with gradient colors and animations
- **Level-based Styling**: Different visual styles for each hierarchy level
- **Keyboard Shortcuts**: Full keyboard navigation support

### 8. `optimized_organigram.html` ⭐ **RECOMMENDED FOR LARGE DATASETS**

Optimized version designed for handling large datasets efficiently:

- **Lazy Loading**: Only renders visible nodes for better performance
- **Memory Efficient**: Handles large JSON files (2MB+) smoothly
- **Performance Monitoring**: Real-time metrics and load times
- **Clean Design**: Simple white and grey interface
- **Progressive Disclosure**: Smart rendering for better user experience

## 🔄 Import Tools

### CSV/Excel Import Functionality

Convert your CSV or Excel files to the JSON format required by the organigram:

#### **Simple Importer** (No dependencies)

```bash
python3 import_organigram_simple.py your_file.csv
```

#### **Advanced Importer** (Supports Excel)

```bash
# Install dependencies first
pip install -r requirements.txt

# Import CSV or Excel files
python3 import_organigram_advanced.py your_file.xlsx
python3 import_organigram_advanced.py your_file.csv
```

#### **Required File Structure**

Your CSV/Excel file must have these columns:

- `name`: Node name/description
- `id`: Unique node identifier
- `pid`: Parent ID (NULL/empty for root nodes)
- `level`: Hierarchical level (l1, l2, l3, l4)

#### **Import Examples**

```bash
# Basic import
python3 import_organigram_simple.py data.csv

# Custom output file
python3 import_organigram_simple.py data.csv -o custom_hierarchy.json

# Validate file structure only
python3 import_organigram_simple.py data.csv --validate-only

# Excel with specific sheet
python3 import_organigram_advanced.py data.xlsx -s "Sheet2"

# Interactive demo
python3 import_demo.py
```

## Data Structure Overview

The dataset contains **11,754 nodes** organized in a 4-level hierarchy:

- **Level 1 (l1)**: 7 root nodes

  - Commodity
  - Machinery
  - Production Process
  - Prototype
  - Raw Materials
  - Third Party Services
  - Tooling & Fixtures

- **Level 2 (l2)**: 71 nodes (main categories)
- **Level 3 (l3)**: 2,935 nodes (subcategories)
- **Level 4 (l4)**: 8,741 nodes (specific items)

## Usage

### 🌟 **Quick Start - Interactive Views**

1. **Basic Interactive View**: Open `interactive_organigram.html` in your web browser

   - Perfect for exploring the hierarchy with collapsible nodes
   - Simple, clean interface with search and level controls

2. **Advanced Interactive View**: Open `advanced_organigram.html` in your web browser
   - Full-featured experience with statistics, export, and enhanced navigation
   - Professional interface with detailed analytics

### 📊 **Static Mermaid Diagrams**

1. **Simple Overview**: Open `organigram_simple.html` for top-level structure
2. **Complete Diagram**: Open `organigram.html` for full detailed diagram (may be slow to render)

### Using the JSON Data

The `nodes_hierarchy.json` file can be used in web applications, data analysis tools, or any system that needs to work with hierarchical data.

Example of accessing the data in JavaScript:

```javascript
fetch('nodes_hierarchy.json')
  .then((response) => response.json())
  .then((data) => {
    // data is an array of root nodes
    console.log('Root nodes:', data);

    // Each node has children array
    data.forEach((rootNode) => {
      console.log(`Root: ${rootNode.name} has ${rootNode.children.length} children`);
    });
  });
```

### Regenerating the Files

Run the processing scripts:

```bash
# Generate complete hierarchy and diagrams
python3 process_nodes.py

# Generate simplified diagrams
python3 create_simple_organigram.py
```

## Mermaid Syntax

The generated `.mmd` files use Mermaid flowchart syntax:

- `graph TD` defines a top-down directed graph
- `A["Label"]` defines a node with a label
- `A --> B` defines a connection from A to B

You can also view these diagrams on:

- [Mermaid Live Editor](https://mermaid-js.github.io/mermaid-live-editor/)
- VS Code with Mermaid extension
- GitHub (supports Mermaid rendering in markdown)

## File Dependencies

- `nodes.csv` - Source data file (required)
- `process_nodes.py` - Main processing script
- `create_simple_organigram.py` - Script for simplified diagrams
