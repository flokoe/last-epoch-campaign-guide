# Last Epoch Campaign Guide

A simple checklist-based guide for the Last Epoch campaign. The guide allows you to track your progress through the game's chapters and zones.

## Features

- Organized by chapters and zones
- Tips and tricks for each zone
- Interactive checklist to mark your progress
- Progress is saved in your browser

## Setup

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Generate the HTML guide:

```bash
cd scripts
python generate_guide.py
```

3. Open the generated guide in your browser:

```bash
# On Linux/macOS
open ../static/index.html

# Or simply open the file from your file browser
```

## Customizing the Guide

You can modify the campaign data by editing the YAML file in the `data` directory:

- `data/campaign_guide.yaml`: Contains all chapters, zones, and tips

After making changes to the YAML file, regenerate the HTML guide by running the script again.

## Extending the Guide

To add more chapters and zones, simply edit the YAML file following the existing structure:

```yaml
chapters:
  - name: "Chapter Name"
    zones:
      - name: "Zone Name"
        description: "Zone description"
        tips:
          - "Tip 1"
          - "Tip 2"
``` 