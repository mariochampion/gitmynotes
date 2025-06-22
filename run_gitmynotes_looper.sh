#!/bin/sh

# Script to run gitmynotes.py with different folder/max combinations
# Edit the folder_configs section below to specify your folder names and max values

# Configuration: folder_name:max_value pairs
# Edit this section with your actual folder names and max values
folder_configs="
Notes:10
"
# Add more lines in the format: folder_name:max_value
# Example:
# your_folder_name:your_max_value
# books:10
# movies:10
# etc:10


# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Path to gitmynotes.py (assuming it's in the same directory as this script)
GITMYNOTES_SCRIPT="$SCRIPT_DIR/gitmynotes.py"

# Check if gitmynotes.py exists
if [ ! -f "$GITMYNOTES_SCRIPT" ]; then
    echo "Error: gitmynotes.py not found at $GITMYNOTES_SCRIPT"
    exit 1
fi

# Loop through the configurations
echo "Starting gitmynotes.py runs..."
echo "================================"

# Process each line in folder_configs
echo "$folder_configs" | while IFS=':' read -r folder max_value; do
    # Skip empty lines
    if [ -z "$folder" ] || [ -z "$max_value" ]; then
        continue
    fi
    
    echo "Running: python3 $GITMYNOTES_SCRIPT --folder=$folder --max=$max_value"
    
    # Run gitmynotes.py with current folder and max values
    python3 "$GITMYNOTES_SCRIPT" --folder="$folder" --max="$max_value"
    
    # Check exit status
    if [ $? -eq 0 ]; then
        echo "✓ Successfully completed: folder=$folder, max=$max_value"
    else
        echo "✗ Error running: folder=$folder, max=$max_value"
    fi
    
    echo "--------------------------------"
done

echo "All gitmynotes.py runs completed!"
