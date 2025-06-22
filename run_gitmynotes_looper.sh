#!/bin/sh

# This bulk/loop runner script only provides 2 flags to gitmynotes.py script: folder and maxnotes
# to repeatedly run GitMyNotes with different --folder/--maxnotes combinations

# Edit this section with folder_name:max_value pairs
# Add more lines to 'folder_configs' belowin the format: folder_name:max_value
# example: reddit_notes:20

folder_configs=\"
Notes:10
\"


# Get the directory where this script is located
SCRIPT_DIR=\"$(cd \"$(dirname \"$0\")\" && pwd)\"

# Path to gitmynotes.py (assuming it's in the same directory as this script)
GITMYNOTES_SCRIPT=\"$SCRIPT_DIR/gitmynotes.py\"

# Check if gitmynotes.py exists
if [ ! -f \"$GITMYNOTES_SCRIPT\" ]; then
    echo \"Error: gitmynotes.py not found at $GITMYNOTES_SCRIPT\"
    exit 1
fi

# Loop through the configurations
echo \"Starting GitMyNotes runs...\"
echo \"================================\"

# Process each line in folder_configs
echo \"$folder_configs\" | while IFS=':' read -r folder max_value; do
    # Skip empty lines
    if [ -z \"$folder\" ] || [ -z \"$max_value\" ]; then
        continue
    fi
    
    echo \"Running: python3 $GITMYNOTES_SCRIPT --folder=$folder --max=$max_value\"
    
    # Run gitmynotes.py with current folder and max values
    python3 \"$GITMYNOTES_SCRIPT\" --folder=\"$folder\" --max=\"$max_value\"
    
    # Check exit status
    if [ $? -eq 0 ]; then
        echo \"✓ Successfully completed: folder=$folder, max=$max_value\"
    else
        echo \"✗ Error running: folder=$folder, max=$max_value\"
    fi
    
    echo \"--------------------------------\"
done

echo \"All GitMyNotes runs completed!\"
`
}