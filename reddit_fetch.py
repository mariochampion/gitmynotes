#!/usr/bin/env python
## ===================================================================
## GitMyNotes - LICENSE AND CREDITS
## This app/collection of scripts at https://github.com/mariochampion/gitmynotes
## released under the GNU Affero General Public License v3.0
##
## 
## GitMyNotes scripts crafted and copyright 2025 by mario champion (mariochampion.com) 
##
## please open issues and pull requests and comments
## thanks and always remember: this robot loves you. 
## boop boop!!!
## ===================================================================


##################################################################
##  THIS IS A WORK IN PROGRESS
##  REQUIRES USER TO SETUP REDDIT APP to acquire
##  REDDIT_CLIENT_ID', 'REDDIT_CLIENT_SECRET', 'REDDIT_USER_AGENT'
##  Instructions to come later
##################################################################



import praw
from ruamel.yaml import YAML
import os
from bs4 import BeautifulSoup
import re
from datetime import datetime
from collections import Counter
import spacy
from string import punctuation

## CONFIGS
GITMYNOTES_CONFIG = "gmn_config.yaml"


def get_script_dir():
    """Get the directory where the script is located."""
    return os.path.dirname(os.path.abspath(__file__))

def load_config():
    """Load config from the same directory as the script."""
    yaml = YAML()
    yaml.preserve_quotes = True
    config_path = os.path.join(get_script_dir(), GITMYNOTES_CONFIG)
    with open(config_path, 'r') as file:
        return yaml.load(file)

def load_stopwords():
    """Load custom stopwords from the same directory as the script."""
    stopwords_path = os.path.join(get_script_dir(), 'stopwords.txt')
    with open(stopwords_path, 'r') as file:
        return set(word.strip().lower() for word in file)

def setup_reddit(config):
    return praw.Reddit(
        client_id=config['REDDIT_CLIENT_ID'],
        client_secret=config['REDDIT_CLIENT_SECRET'],
        user_agent=config['REDDIT_USER_AGENT']
    )

def extract_reddit_info(url, reddit):
    # Extract submission ID from URL
    submission_id = re.search(r'/comments/([a-z0-9]+)/', url).group(1)
    submission = reddit.submission(id=submission_id)
    
    # Get post info
    post_info = {
        "title": submission.title,
        "selftext": submission.selftext,
        "author": str(submission.author),
        "score": submission.score,
        "created_utc": datetime.fromtimestamp(submission.created_utc),
        "num_comments": submission.num_comments,
        "subreddit": submission.subreddit.display_name
    }
    
    # Get top comments
    submission.comments.replace_more(limit=0)  # Remove MoreComments objects
    if len(submission.comments) > 0:
        top_comment = submission.comments[0]
        post_info["top_comment"] = {
            "text": top_comment.body,
            "author": str(top_comment.author),
            "score": top_comment.score
        }
    
    return post_info

def generate_hashtags(post_info):
    """Generate relevant hashtags using NLP analysis of Reddit post content."""
    # Load the English NLP model and custom stopwords
    nlp = spacy.load("en_core_web_sm")
    custom_stopwords = load_stopwords()
    
    # Combine title and content for analysis
    content = f"{post_info['title']} {post_info['selftext']}"
    if 'top_comment' in post_info:
        content += f" {post_info['top_comment']['text']}"
    
    # Process the text with spaCy
    doc = nlp(content)
    
    # Extract named entities and their labels
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    
    # Extract noun phrases (chunks), filtering out those containing only stopwords
    noun_phrases = [
        chunk.text.lower() for chunk in doc.noun_chunks
        if not all(token.text.lower() in custom_stopwords for token in chunk)
    ]
    
    # Extract important words (nouns, proper nouns, adjectives)
    important_words = [
        token.text.lower() for token in doc 
        if (token.pos_ in ['NOUN', 'PROPN', 'ADJ'] and 
            not token.is_stop and 
            token.text.lower() not in custom_stopwords and
            len(token.text) > 2)
    ]
    
    # Combine all potential hashtag sources with weights
    hashtag_candidates = []
    
    # Add named entities (highest weight)
    for text, label in entities:
        if (label in ['ORG', 'PRODUCT', 'PERSON', 'GPE', 'NORP', 'EVENT'] and
            not all(word.lower() in custom_stopwords for word in text.split())):
            hashtag_candidates.extend([text.lower()] * 3)
    
    # Add noun phrases (medium weight)
    hashtag_candidates.extend(noun_phrases * 2)
    
    # Add important words (lower weight)
    hashtag_candidates.extend(important_words)
    
    # Count frequencies of candidates
    candidate_freq = Counter(hashtag_candidates)
    
    # Generate hashtags from top candidates
    hashtags = []
    for text, _ in candidate_freq.most_common(5):
        # Clean and format the hashtag
        words = text.split()
        clean_words = []
        for word in words:
            # Remove punctuation and special characters
            clean_word = ''.join(c for c in word if c not in punctuation and c.isalnum())
            if clean_word and clean_word.lower() not in custom_stopwords:
                clean_words.append(clean_word)
        
        if clean_words:
            # Create camel case hashtag
            hashtag = f"#{''.join(w.title() for w in clean_words)}"
            if hashtag not in hashtags and len(hashtag) > 2:  # Ensure hashtag is meaningful
                hashtags.append(hashtag)
    
    # Ensure we have at least one hashtag
    if not hashtags:
        # Use the subreddit name as a fallback hashtag
        subreddit = f"#{post_info.get('subreddit', 'Reddit')}"
        hashtags.append(subreddit)
    
    return hashtags[:3]  # Return up to 3 most relevant hashtags

def update_markdown_file(file_path, post_info):
    """Update markdown file with Reddit post information."""
    try:
        # Read existing content
        with open(file_path, 'r') as file:
            existing_content = file.read()
            
        # Create new content section
        new_content = f"""
<div><br></div>
<div><b>Post Details:</b><br></div>
<div>Author: u/{post_info['author']}</div>
<div>Posted: {post_info['created_utc']}</div>
<div>Score: {post_info['score']}</div>
<div>Comments: {post_info['num_comments']}</div>
<div><br></div>
<div><b>Content:</b></div>
<div>{post_info['selftext']}</div>
"""
        
        if 'top_comment' in post_info:
            new_content += f"""
<div><br></div>
<div><b>Top Comment by u/{post_info['top_comment']['author']}:</b></div>
<div>{post_info['top_comment']['text']}</div>
"""
        
        # Add hashtags
        hashtags = generate_hashtags(post_info)
        new_content += f"""
<div><br></div>
<div>{' '.join(hashtags)}</div>
"""
        
        # Write updated content
        with open(file_path, 'w') as file:
            file.write(existing_content + new_content)
        return True
    except Exception as e:
        print(f"Error updating markdown file {file_path}: {str(e)}")
        return False

def process_reddit_file(filename, base_dir, reddit, config):
    """Process a single Reddit file and return success status."""
    script_dir = get_script_dir()
    full_path = os.path.join(script_dir, base_dir, config['DEFAULT_REDDIT_FOLDER_NAME'], filename)
    
    try:
        # Get the URL from the file
        with open(full_path, 'r') as file:
            content = file.read()
            url_match = re.search(r'https://www.reddit.com/r([^>]+)>', content)
            if not url_match:
                print(f"No Reddit URL found in {filename}")
                return False
                
            url = url_match.group(1).strip('"')
            print(f"Processing {filename}")
            print(f"Found URL: {url}")
            
            # Get Reddit post info and update markdown
            post_info = extract_reddit_info(url, reddit)
            print("Successfully fetched post info")
            
            if update_markdown_file(full_path, post_info):
                print("Successfully updated markdown file")
                return True
            
    except Exception as e:
        print(f"Error processing {filename}: {str(e)}")
    
    return False

def main():
    try:
        # Load config and setup Reddit
        config = load_config()
        reddit = setup_reddit(config)
        
        # Get reddit config from the same config file
        redditlinks = config['DEFAULT_REDDIT_FOLDER_NAME']
        base_dir = config['DEFAULT_NOTES_WRAPPERDIR']  # Use the default wrapper dir
        
        # Get list of files to process
        prefetched_files = redditlinks.get('PREFETCHED', [])
        print(f"Found {len(prefetched_files)} files to process")
        
        if not prefetched_files:
            print("No files to process in PREFETCHED section")
            return
        
        # Process all files and track successful ones
        successful_files = []
        for filename in prefetched_files:
            if process_reddit_file(filename, base_dir, reddit):
                successful_files.append(filename)
        
        # Update YAML file once after all processing
        if successful_files:
            # Remove processed files from PREFETCHED
            redditlinks['PREFETCHED'] = [f for f in prefetched_files if f not in successful_files]
            
            # Add to FETCHED
            if 'FETCHED' not in redditlinks:
                redditlinks['FETCHED'] = []
            redditlinks['FETCHED'].extend(successful_files)
            
            # Write updated YAML file while preserving formatting
            yaml = YAML()
            yaml.preserve_quotes = True
            yaml.indent(mapping=2, sequence=4, offset=2)
            config_path = os.path.join(get_script_dir(), GITMYNOTES_CONFIG)
            with open(config_path, 'w') as yaml_file:
                yaml.dump(config, yaml_file)
            
            print(f"Successfully processed {len(successful_files)} files")
        else:
            print("No files were successfully processed")
                
    except Exception as e:
        print(f"Error in main: {str(e)}")

if __name__ == "__main__":
    main()