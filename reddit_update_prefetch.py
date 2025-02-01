import os
import re
from ruamel.yaml import YAML

MINIMUM_WORD_COUNT = 50
REDDIT_FOLDER_NAME = "_reddit"
GITMYNOTES_CONFIG = "gmn_config.yaml"


def get_script_dir():
    """Get the directory where the script is located."""
    return os.path.dirname(os.path.abspath(__file__))

def count_content_words(content):
    """Count the number of words in the content, excluding metadata and URLs."""
    # Remove creation and modification date lines
    lines = content.split('\n')
    filtered_lines = []
    skip_next = False
    for line in lines:
        if skip_next:
            skip_next = False
            continue
        if "creation date:" in line.lower() or "modification date:" in line.lower():
            skip_next = True
            continue
        filtered_lines.append(line)
    
    # Remove HTML/markup tags
    content_no_tags = re.sub(r'<[^>]+>', '', '\n'.join(filtered_lines))
    
    # Remove URLs - handles both http(s) and www formats
    url_pattern = r'(?:https?:\/\/)?(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)'
    content_no_urls = re.sub(url_pattern, '', content_no_tags)
    
    # Remove extra whitespace that might be left after removing URLs
    content_clean = re.sub(r'\s+', ' ', content_no_urls).strip()
    
    # Count words
    words = re.findall(r'\w+', content_clean)
    return len(words)

def main():
    try:
        yaml = YAML()
        yaml.preserve_quotes = True
        yaml.indent(mapping=2, sequence=4, offset=2)
        
        script_dir = get_script_dir()
        # Load the YAML file from the same directory as the script
        config_path = os.path.join(script_dir, GITMYNOTES_CONFIG)
        with open(config_path, 'r') as file:
            config = yaml.load(file)
        
        # Initialize REDDIT_FOLDER_NAME ( ie, '_reddit') section of config if it doesn't exist
        if REDDIT_FOLDER_NAME not in config:
            config[REDDIT_FOLDER_NAME] = {'FETCHED': [], 'PREFETCHED': []}
        
        # Get list of files already in FETCHED or PREFETCHED
        redditlinks = config[REDDIT_FOLDER_NAME]
        processed_files = set(redditlinks.get('FETCHED', []) + 
                            redditlinks.get('PREFETCHED', []))
        
        # Process each file in the directory using relative path
        base_dir = config['DEFAULT_NOTES_WRAPPERDIR']  # Use the default wrapper dir
        dir_path = os.path.join(script_dir, base_dir, REDDIT_FOLDER_NAME)
        
        for filename in os.listdir(dir_path):
            if not filename.endswith('.md'):
                continue
                
            if filename in processed_files:
                print(f"Skipping {filename} - already processed")
                continue
            
            file_path = os.path.join(dir_path, filename)
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    word_count = count_content_words(content)
                    
                    if word_count < MINIMUM_WORD_COUNT:
                        print(f"Adding {filename} to PREFETCHED (word count: {word_count})")
                        redditlinks['PREFETCHED'].append(filename)
                    else:
                        print(f"Skipping {filename} - too many words ({word_count})")
            
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
                continue
        
        # Save updated YAML file while preserving formatting and comments
        with open(config_path, 'w') as file:
            yaml.dump(config, file)
            
        print("\nYAML file updated successfully!")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()