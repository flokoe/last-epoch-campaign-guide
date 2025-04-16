#!/usr/bin/env python3

import yaml
import os
import sys
import json

def load_campaign_data(yaml_file):
    with open(yaml_file, 'r') as file:
        try:
            data = yaml.safe_load(file)
            return data
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
            sys.exit(1)

def generate_html(data):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data['campaign']['name']}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #121212;
            color: #e0e0e0;
        }}
        h1, h2, h3 {{
            color: #bb9b62;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        h1 {{
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.2rem;
            text-shadow: 0 0 10px rgba(187, 155, 98, 0.4);
        }}
        .description {{
            text-align: center;
            font-style: italic;
            margin-bottom: 30px;
            color: #a0a0a0;
        }}
        .chapter {{
            margin-bottom: 30px;
            background-color: #1e1e1e;
            border-radius: 5px;
            padding: 15px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
            border: 1px solid #333;
        }}
        .chapter-header {{
            display: flex;
            align-items: center;
            cursor: pointer;
            user-select: none;
            padding: 5px;
            border-radius: 3px;
            transition: background-color 0.2s;
        }}
        .chapter-header h2 {{
            margin: 0;
            flex-grow: 1;
            font-size: 1.4rem;
        }}
        .chapter-content {{
            display: block;
            padding-top: 15px;
            border-top: 1px solid #333;
            margin-top: 10px;
        }}
        .chapter-content.collapsed {{
            display: none;
        }}
        .collapse-icon {{
            font-size: 18px;
            margin-right: 10px;
            color: #bb9b62;
        }}
        .collapse-icon:after {{
            content: "▼";
        }}
        .chapter-header.collapsed .collapse-icon:after {{
            content: "▶";
        }}
        .zone {{
            margin-bottom: 20px;
            padding: 12px;
            border-left: 3px solid #bb9b62;
            background-color: #262626;
            border-radius: 3px;
        }}
        .zone-header {{
            display: flex;
            align-items: center;
        }}
        .zone-name {{
            margin: 0;
            flex-grow: 1;
            font-size: 1.2rem;
        }}
        .zone.completed {{
            opacity: 0.7;
            background-color: #2a2a2a;
            border-left-color: #5a5a5a;
        }}
        .zone.completed h3 {{
            color: #8a8a8a;
            text-decoration: line-through;
        }}
        .tips {{
            margin-top: 12px;
            padding-left: 20px;
            border-top: 1px dotted #444;
            padding-top: 10px;
        }}
        .tips-title {{
            color: #bb9b62;
            font-weight: 600;
        }}
        .tips ul {{
            padding-left: 20px;
        }}
        .tips li {{
            margin-bottom: 8px;
            color: #c0c0c0;
        }}
        input[type="checkbox"] {{
            transform: scale(1.3);
            margin-right: 10px;
            accent-color: #bb9b62;
            cursor: pointer;
        }}
        .zone-description {{
            font-style: italic;
            color: #a0a0a0;
            margin: 8px 0 12px 0;
        }}
        
        /* Mobile responsiveness */
        @media (max-width: 600px) {{
            body {{
                padding: 12px;
            }}
            h1 {{
                font-size: 1.8rem;
            }}
            .chapter-header h2 {{
                font-size: 1.2rem;
            }}
            .zone-name {{
                font-size: 1.1rem;
            }}
            .tips ul {{
                padding-left: 15px;
            }}
        }}
    </style>
</head>
<body>
    <h1>{data['campaign']['name']}</h1>
    <p class="description">{data['campaign']['description']}</p>
    
    <div id="campaign-content">
"""
    
    # Generate HTML for each chapter and zone
    for chapter_idx, chapter in enumerate(data['campaign']['chapters']):
        chapter_id = f"chapter-{chapter_idx+1}"
        html += f"""
        <div class="chapter" id="{chapter_id}">
            <div class="chapter-header" data-target="{chapter_id}-content">
                <span class="collapse-icon"></span>
                <h2>{chapter['name']}</h2>
            </div>
            <div class="chapter-content" id="{chapter_id}-content">
"""
        
        # Generate zones for this chapter
        for zone_idx, zone in enumerate(chapter['zones']):
            zone_id = f"zone-{chapter_idx+1}-{zone_idx+1}"
            html += f"""
                <div class="zone" id="{zone_id}">
                    <div class="zone-header">
                        <input type="checkbox" class="zone-checkbox" data-zone-id="{zone_id}">
                        <h3 class="zone-name">{zone['name']}</h3>
                    </div>
                    <p class="zone-description">{zone['description']}</p>
                    <div class="tips">
                        <span class="tips-title">Tips:</span>
                        <ul>
"""
            
            # Add tips for this zone
            for tip in zone['tips']:
                html += f"""
                            <li>{tip}</li>
"""
            
            html += """
                        </ul>
                    </div>
                </div>
"""
        
        html += """
            </div>
        </div>
"""
    
    # Add JavaScript for handling checkboxes and collapsible sections
    html += """
    </div>

    <script>
        // Load saved state on page load
        document.addEventListener('DOMContentLoaded', function() {
            loadCheckboxState();
            loadCollapseState();
            
            // Add event listeners to all checkboxes
            const checkboxes = document.querySelectorAll('.zone-checkbox');
            checkboxes.forEach(checkbox => {
                checkbox.addEventListener('change', function() {
                    const zoneId = this.getAttribute('data-zone-id');
                    const zoneElement = document.getElementById(zoneId);
                    
                    if (this.checked) {
                        zoneElement.classList.add('completed');
                    } else {
                        zoneElement.classList.remove('completed');
                    }
                    
                    saveCheckboxState();
                });
            });
            
            // Add event listeners to chapter headers for collapsible functionality
            const chapterHeaders = document.querySelectorAll('.chapter-header');
            chapterHeaders.forEach(header => {
                header.addEventListener('click', function() {
                    const contentId = this.getAttribute('data-target');
                    const contentElement = document.getElementById(contentId);
                    
                    this.classList.toggle('collapsed');
                    contentElement.classList.toggle('collapsed');
                    
                    saveCollapseState();
                });
            });
        });
        
        // Save checkbox state to localStorage
        function saveCheckboxState() {
            const checkboxes = document.querySelectorAll('.zone-checkbox');
            const state = {};
            
            checkboxes.forEach(checkbox => {
                const zoneId = checkbox.getAttribute('data-zone-id');
                state[zoneId] = checkbox.checked;
            });
            
            localStorage.setItem('leGuideState', JSON.stringify(state));
        }
        
        // Load checkbox state from localStorage
        function loadCheckboxState() {
            const savedState = localStorage.getItem('leGuideState');
            
            if (savedState) {
                const state = JSON.parse(savedState);
                
                for (const zoneId in state) {
                    const checkbox = document.querySelector(`.zone-checkbox[data-zone-id="${zoneId}"]`);
                    const zoneElement = document.getElementById(zoneId);
                    
                    if (checkbox && state[zoneId]) {
                        checkbox.checked = true;
                        zoneElement.classList.add('completed');
                    }
                }
            }
        }
        
        // Save collapse state to localStorage
        function saveCollapseState() {
            const chapterHeaders = document.querySelectorAll('.chapter-header');
            const state = {};
            
            chapterHeaders.forEach(header => {
                const contentId = header.getAttribute('data-target');
                state[contentId] = header.classList.contains('collapsed');
            });
            
            localStorage.setItem('leGuideCollapseState', JSON.stringify(state));
        }
        
        // Load collapse state from localStorage
        function loadCollapseState() {
            const savedState = localStorage.getItem('leGuideCollapseState');
            
            if (savedState) {
                const state = JSON.parse(savedState);
                
                for (const contentId in state) {
                    const header = document.querySelector(`.chapter-header[data-target="${contentId}"]`);
                    const contentElement = document.getElementById(contentId);
                    
                    if (header && contentElement && state[contentId]) {
                        header.classList.add('collapsed');
                        contentElement.classList.add('collapsed');
                    }
                }
            }
        }
    </script>
</body>
</html>
"""
    
    return html

def main():
    # Check if the data directory exists
    if not os.path.isdir('../data'):
        print("Error: data directory not found")
        sys.exit(1)
    
    # Load the campaign data
    yaml_file = '../data/campaign_guide.yaml'
    data = load_campaign_data(yaml_file)
    
    # Generate HTML
    html = generate_html(data)
    
    # Create output directory if it doesn't exist
    os.makedirs('../static', exist_ok=True)
    
    # Write HTML to file
    with open('../static/index.html', 'w') as file:
        file.write(html)
    
    print(f"HTML guide generated at: ../static/index.html")

if __name__ == "__main__":
    main() 