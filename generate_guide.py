#!/usr/bin/env python3

import yaml
import os
import sys
import shutil
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
    # Set up Jinja2 environment using the current directory
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('campaign_guide.html.j2')
    
    # Render the template with our data
    return template.render(campaign=data['campaign'])

def main():
    # Get the base directory (project root)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check if the data file exists
    yaml_file = os.path.join(base_dir, 'campaign_guide.yaml')
    if not os.path.isfile(yaml_file):
        print(f"Error: campaign data file not found at {yaml_file}")
        sys.exit(1)
    
    # Load the campaign data
    data = load_campaign_data(yaml_file)
    
    # Generate HTML
    html = generate_html(data)
    
    # Create output directory if it doesn't exist
    public_dir = os.path.join(base_dir, 'public')
    os.makedirs(public_dir, exist_ok=True)
    
    # Write HTML to file
    output_file = os.path.join(public_dir, 'index.html')
    with open(output_file, 'w') as file:
        file.write(html)
    
    # Copy static directory to public
    static_dir = os.path.join(base_dir, 'static')
    public_static_dir = os.path.join(public_dir, 'static')
    
    # Remove existing static directory in public if it exists
    if os.path.exists(public_static_dir):
        shutil.rmtree(public_static_dir)
    
    # Copy the entire static directory
    if os.path.exists(static_dir):
        shutil.copytree(static_dir, public_static_dir)
        print(f"Static files copied to: {public_static_dir}")
    
    print(f"HTML guide generated at: {output_file}")

if __name__ == "__main__":
    main() 