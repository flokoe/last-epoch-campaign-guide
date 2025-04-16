#!/usr/bin/env python3

import yaml
import os
import sys
from jinja2 import Environment, FileSystemLoader
from typing import Dict, Any

def load_campaign_data(yaml_file: str) -> Dict[str, Any]:
    with open(yaml_file, 'r') as file:
        try:
            data = yaml.safe_load(file)
            return data
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
            sys.exit(1)

def generate_html(data: Dict[str, Any]) -> str:
    # Set up Jinja2 environment
    template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('campaign_guide.html')
    
    # Render the template with our data
    return template.render(campaign=data['campaign'])

def main():
    # Get the base directory (project root)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Check if the data directory exists
    data_dir = os.path.join(base_dir, 'data')
    if not os.path.isdir(data_dir):
        print("Error: data directory not found")
        sys.exit(1)
    
    # Load the campaign data
    yaml_file = os.path.join(data_dir, 'campaign_guide.yaml')
    data = load_campaign_data(yaml_file)
    
    # Generate HTML
    html = generate_html(data)
    
    # Create output directory if it doesn't exist
    static_dir = os.path.join(base_dir, 'static')
    os.makedirs(static_dir, exist_ok=True)
    
    # Write HTML to file
    output_file = os.path.join(static_dir, 'index.html')
    with open(output_file, 'w') as file:
        file.write(html)
    
    print(f"HTML guide generated at: {output_file}")

if __name__ == "__main__":
    main() 