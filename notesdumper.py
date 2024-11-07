import subprocess
import os
from datetime import datetime
import argparse

DEFAULT_EXPORT_PATH = "~/Documents/openai/notesdump/gitnotes"
DEFAULT_GITHUB_URL = "https://github.com/mariochampion/notesdump"



def setup_git_repo(repo_path, DEFAULT_GITHUB_URL):
    """Initialize Git repo and set remote if not already set up"""
    if not os.path.exists(os.path.join(repo_path, '.git')):
        subprocess.run(['git', 'init'], cwd=repo_path)
        subprocess.run(['git', 'remote', 'add', 'origin', DEFAULT_GITHUB_URL], cwd=repo_path)

def export_notes_to_markdown(export_path, folder_name=None, max_notes=None):
    """Export Notes using osascript with folder and count limits"""
    applescript = f'''
    tell application "Notes"
        if length of "{folder_name if folder_name else ''}" > 0 then
            try
                set targetFolder to folder "{folder_name}"
                set allNotes to every note in targetFolder
                set export_path_full to "{export_path}/{folder_name}"
            on error
                log "Folder {folder_name} not found"
                return 0
            end try
        else
            set allNotes to every note
        end if
        
        set noteCount to (count of allNotes)
        if {max_notes} > 0 
        	set maxToProcess to {max_notes} 
        else
        	set maxToProcess to noteCount
        end if
        
        if maxToProcess < noteCount
        	set notesToProcess to maxToProcess
        else
        	set notesToProcess to noteCount
        end if
        
        repeat with i from 1 to notesToProcess
            set currentNote to item i of allNotes
            
            set noteTitle to the name of currentNote
            set noteContent to the body of currentNote
            
            -- Clean the title for use as filename
            set cleanTitle to do shell script "echo " & quoted form of noteTitle & " | sed 's/[^a-zA-Z0-9.]/-/g' | tr '[:upper:]' '[:lower:]'"
            set fileName to cleanTitle & ".md"
            
            -- Write to file
            do shell script "echo " & quoted form of noteContent & " > " & quoted form of export_path_full & "/" & fileName
        end repeat
        
        return notesToProcess
    end tell
    '''
    result = subprocess.run(['osascript', '-e', applescript], capture_output=True, text=True)
    if result.stderr:
        print(f"Error: {result.stderr}")
        return 0
    return int(result.stdout.strip()) if result.stdout.strip() else 0

def commit_and_push(repo_path, folder_name=None):
    """Commit changes and push to GitHub"""
    subprocess.run(['git', 'add', '.'], cwd=f"{repo_path}/{folder_name}")
    folder_info = f" from folder '{folder_name}'" if folder_name else ""
    commit_message = f"Updated notes{folder_info} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    print(f"repo_path:{repo_path}, folder_name:{folder_name}, commit_message:{commit_message}")
    subprocess.run(['git', 'commit', '-m', commit_message], cwd=f"{repo_path}/{folder_name}")
    subprocess.run(['git', 'push', 'origin', 'main'], cwd=f"{repo_path}/{folder_name}")

def main():
    parser = argparse.ArgumentParser(description='Export Apple Notes to GitHub')
    parser.add_argument('--folder', type=str, default='',
                      help='Specific Notes folder to export (default: all folders)')
    parser.add_argument('--max-notes', type=int,
                      help='Maximum number of notes to process')
    parser.add_argument('--export-path', type=str, 
                      default=os.path.expanduser(f"{DEFAULT_EXPORT_PATH}"),
                      help=f'Path to export the notes (default: {DEFAULT_EXPORT_PATH})')
    parser.add_argument('--github-url', type=str,
    				  default=DEFAULT_GITHUB_URL,
                      help='GitHub repository URL')
    
    args = parser.parse_args()
    
    os.makedirs(args.export_path, exist_ok=True)
    
    setup_git_repo(args.export_path, args.github_url)
    
    notes_processed = export_notes_to_markdown(
        args.export_path,
        args.folder,
        args.max_notes
    )
    
    print(f"Processed {notes_processed} notes")
    
    if notes_processed > 0:
        commit_and_push(args.export_path, args.folder)
    else:
        print("No notes were processed, skipping git commit")

if __name__ == "__main__":
    main()