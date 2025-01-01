import os
import yaml
import re

MINIMUM_WORD_COUNT = 50

def get_script_dir():
    """Get the directory where the script is located."""
    return os.path.dirname(os.path.abspath(__file__))

def count_content_words(content):
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
        script_dir = get_script_dir()
        # Load the YAML file from the same directory as the script
        yaml_path = os.path.join(script_dir, 'reddit_prefetched.yaml')
        with open(yaml_path, 'r') as file:
            config = yaml.safe_load(file)
        
        # Get list of files already in FETCHED or PREFETCHED
        processed_files = set(config['_redditlinks'].get('FETCHED', []) + 
                            config['_redditlinks'].get('PREFETCHED', []))
        
        # Initialize PREFETCHED if it doesn't exist
        if 'PREFETCHED' not in config['_redditlinks']:
            config['_redditlinks']['PREFETCHED'] = []
        
        # Process each file in the directory using relative path
        dir_path = os.path.join(script_dir, config['PREFETCH_BASE_DIR'], '_redditlinks')
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
                        config['_redditlinks']['PREFETCHED'].append(filename)
                    else:
                        print(f"Skipping {filename} - too many words ({word_count})")
            
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
                continue
        
        # Save updated YAML file
        with open(yaml_path, 'w') as file:
            yaml.dump(config, file, default_flow_style=False)
            
        print("\nYAML file updated successfully!")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()