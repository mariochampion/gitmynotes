#!/usr/bin/env python
## ===================================================================
## GitMyNotes - LICENSE AND CREDITS
## This app/collection of scripts at https://github.com/mariochampion/gitmynotes
## released under the GNU General Public License v3.0
##
## 
## GitMyNotes scripts crafted and copyright 2024 by mario champion (mariochampion.com) 
##
## please open issues and pull requests and comments
## thanks and always remember: this robot loves you. 
## boop boop!!!
## ===================================================================


#### USING THIS SCRIPT

## Export up to 10 notes from a specific folder
#  python gitmynotes.py --folder="somefolder" --max-notes=10

## Export all notes from a specific folder
#  python gitmynotes.py --folder="somefolder"

## Export up to 17 notes from all folders
#  python gitmynotes.py --max-notes=17

## Specify a custom output file
#  python gitmynotes.py --folder-name="somefolder" --max-notes=10 --output-file="some-other-folder.csv"

## go crazy and specify nothing, to get all the defaults!
#  python gitmynotes.py


import subprocess
import os, sys
import argparse
import math
import csv
from datetime import datetime
from typing import Tuple
from ruamel.yaml import YAML


#### USER CONFIGS
##   get user configs from file ./gmn_config.yaml

def load_configs_from_file():
    yaml=YAML(typ='safe')   # default, if not specfied, is 'rt' (round-trip)
    loaded_configs = yaml.load(open("gmn_config.yaml"))
    
    return loaded_configs



##### Describe this function

def setup_git_repo(repo_path, DEFAULT_GITHUB_URL):
    """Initialize Git repo and set remote if not already set up"""
    
    if not os.path.exists(os.path.join(repo_path, '.git')):
        try:
            subprocess.run(['git', 'init'], cwd=repo_path)
            colorprint(textcolor="green",msg=f"SUCCESS: GIT INIT with {cwd}")
        except:
            colorprint(textcolor="red",msg=f"ERROR: Did not GIT INIT {cwd}")
        try:
            subprocess.run(['git', 'remote', 'add', 'origin', DEFAULT_GITHUB_URL], cwd=repo_path)
            colorprint(textcolor="green",msg=f"SUCCESS: GIT REMOTE ADD ORIGIN with {cwd}")
        except:
            colorprint(textcolor="RED",msg=f"ERROR: Did not GIT REMOTE ADD ORIGIN with {cwd}")
        try:
            subprocess.run(['git', 'branch', '-m', 'main'], cwd=repo_path)
            colorprint(textcolor="green",msg=f"SUCCESS: GIT BRANCH -M MAIN with {cwd}")
        except:
            colorprint(textcolor="red",msg=f"ERROR: GIT BRANCH -M MAIN with {cwd}")
            
            
        # Add this to handle remote repository state
        try:
            subprocess.run(['git', 'pull', 'origin', 'main'], cwd=repo_path)
            colorprint(textcolor="green",msg=f"Remote content pulled")
        except:
            colorprint(textcolor="magenta",msg=f"No remote content to pull")



##### Describe this function

def export_notes_to_markdown(export_path, folder_name=None, max_notes=None, wrapper_dir=None):
    """Export Notes using applescript/osascript with folder and count limits"""
    
    ## tell the people some information
    if (max_notes > 0 and folder_name !="" and wrapper_dir !=""):
        colorprint(textcolor="white",msg=f"Starting export of {max_notes} Notes from '{folder_name}' into '{wrapper_dir}/{folder_name}'...")
    elif (max_notes > 0 and folder_name !="" and wrapper_dir==None):
        colorprint(textcolor="white",msg=f"Starting export of {max_notes} Notes from '{folder_name}'...")
    elif (max_notes > 0 and folder_name==None and wrapper_dir==None):
        colorprint(textcolor="white",msg=f"Starting export of {max_notes} Notes...")
    elif (max_notes==None and folder_name==None and wrapper_dir==None):
        colorprint(textcolor="white",msg=f"Starting export of all Notes...")
    
    
    applescript = f'''
    tell application "Notes"
        if length of "{folder_name if folder_name else ''}" > 0 then
            try
                set targetFolder to folder "{folder_name}"
                set allNotes to every note in targetFolder
                set export_path_full to "{export_path}/{wrapper_dir}/{folder_name}"
            on error
                log "Folder {folder_name} not found"
                return 0
            end try
        else
            set allNotes to every note
            set export_path_full to "{export_path}/{wrapper_dir}"
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
            set linebreaker to "\n"
            set noteCreateDate to "<div><b>Creation Date:</b> " & creation date of currentNote & "<br></div>"
            set noteModDate to "<div><b>Modification Date:</b> " & modification date of currentNote & "<br></div>"
            set noteContent to the body of currentNote
            
            -- Clean the title for use as filename
            set cleanTitle to do shell script "echo " & quoted form of noteTitle & " | sed 's/[^a-zA-Z0-9.]/-/g' | tr '[:upper:]' '[:lower:]'"
            set fileName to cleanTitle & ".md"
            
            -- Write to file
            do shell script "echo " & quoted form of noteCreateDate & quoted form of linebreaker & quoted form of noteModDate & quoted form of linebreaker & quoted form of noteContent & " > " & quoted form of export_path_full & "/" & fileName
        end repeat
        
        return notesToProcess
    end tell
    '''
    result = subprocess.run(['osascript', '-e', applescript], capture_output=True, text=True)
    if result.stderr:
        print(f"Error: {result.stderr}")
        return 0
    return int(result.stdout.strip()) if result.stdout.strip() else 0



##### Describe this function

def commit_and_push(repo_path, folder_name=None, wrapper_dir=None):
    """Commit changes and push to GitHub"""
    # Always operate from the git root directory
    result_gitadd = subprocess.run(['git', 'add', f'{wrapper_dir}'], cwd=repo_path)
    if result_gitadd.returncode == 0:
        colorprint(textcolor="green",msg=f"Successful GIT ADD to origin/main.")
        #print(result_gitadd)

    else:
        colorprint(textcolor="red",msg=f"Error GIT ADD to origin/main:")
        print(result_gitadd)
    
    folder_info = f" from folder '{folder_name}'" if folder_name else ""
    commit_message = f"Backed up {folder_info} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
    result_gitcommit = subprocess.run(['git', 'commit', '-m', commit_message], cwd=repo_path, capture_output=True, text=True)
    if result_gitcommit.returncode == 0:
        colorprint(textcolor="green",msg=f"Successful GIT COMMIT to origin/main.")
        commit_print_msg = f'''    - repo path: {repo_path}
    - folder name:{folder_name}
    - commit message:{commit_message}
    '''
        colorprint(textcolor="white",msg=f"{commit_print_msg}")
    else:
        colorprint(textcolor="red",msg=f"Error GIT COMMIT to origin/main:")
        commit_print_msg = f'''
    - repo path: {repo_path}
    - folder name:{folder_name}
    - commit message:{commit_message}
    '''
        colorprint(textcolor="white",msg=f"{commit_print_msg}")
        print(result_gitcommit)

    
    if result_gitcommit.returncode == 0:
        # Try to pull and rebase before pushing
        try:
            subprocess.run(['git', 'pull', '--rebase', 'origin', 'main'], cwd=repo_path, capture_output=True, text=True)
        except:
            colorprint(textcolor="magenta",msg=f"No remote changes to pull")
        
        result_push = subprocess.run(['git', 'push', 'origin', 'main'], cwd=repo_path, capture_output=True, text=True)
        
        if result_push.returncode == 0:
            colorprint(textcolor="green",msg=f"Successful GIT PUSH to origin/main.")
            #print(result_push)
            #print(" ")
        else:
            colorprint(textcolor="red",msg=f"Error GIT PUSH to origin/main:")
            print(result_push)
           # print(" ")
            # Optionally, try force push if regular push fails
	        # result = subprocess.run(['git', 'push', '-f', 'origin', 'main'], cwd=repo_path, capture_output=True, text=True)
    else:
        colorprint(textcolor="red",msg=f"No commit so no GIT PUSH to origin/main:")
        #print(" ")



##### Describe this function

def export_notes_metadata(output_file, folder, max_notes, newline_delimiter):
    """
    Export macOS Notes metadata (title, quoted title, and modification date) to a CSV file.
    
    Args:
        output_file (str): Path to the output CSV file
        folder (str): Name of the folder to export notes from (None for all folders)
        max_notes (int): Maximum number of notes to export (None for all notes)
        newline_delimiter (str): Default newline delimiter (|||)
    """
    
    # AppleScript to get notes information    
    applescript = '''
    tell application "Notes"
        set noteList to {}
    '''
    
    applescript += f'''
    set custom_delimiter to "{newline_delimiter}"
    '''
    
    if folder:
        applescript += f'''
        set targetFolder to null
        repeat with f in folders
            if (name of f as string) is "{folder}" then
                set targetFolder to f
                exit repeat
            end if
        end repeat
        set theNotes to notes of targetFolder
        
        if targetFolder is null then
            return "Folder not found"
        end if
        '''
    else:
        applescript += '''
        set theNotes to notes
        '''
        
    ''' Determine the number of repeats/ size of loop'''
    if max_notes:
        applescript += f'''
        repeat with i from 1 to {max_notes}
            set theNote to item i of theNotes
        '''
        
    else:
        applescript += '''
        repeat with theNote in theNotes
        '''
        
    applescript += '''
            set noteTitle to name of theNote as string
            -- clean noteTitle to not break on commas in noteTitle
            set noteTitle to do shell script "echo " & noteTitle & "| sed 's/,/-/'"
            -- Clean the title for use as filename
            set cleanTitle to do shell script "echo " & quoted form of noteTitle & " | sed 's/[^a-zA-Z0-9.]/-/g' | tr '[:upper:]' '[:lower:]'"
            set noteData to noteTitle &","& cleanTitle & ".md" &","& modification date of theNote & custom_delimiter
            copy noteData to the end of noteList
        end repeat
        return noteList
    end tell
    '''

    result,output = process_applescript(applescript)
    
    # Parse the output
    notes_data = []
    raw_output = output.split(newline_delimiter)
    raw_output = raw_output[:-1]
    
    current_datetime = datetime.now()
    for line in raw_output:
        
        line = line.rstrip(",")
        
        #Remove leading and trailing commas
        if line.startswith(','): line = line[1:]
        if line.endswith(','): line = line[:-1]
        
        line_items = line.split(',',2)
        title = line_items[0].strip()
        
        quoted_title = line_items[1].strip()        
        mod_date = line_items[2].strip()
        
        # Convert date string to datetime object and format it
        try:
            date_obj = datetime.strptime(mod_date, '%Y-%m-%d %H:%M:%S +0000')
            formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            formatted_date = mod_date
        
        colorprint(textcolor="white",msg=f"Adding row to audit file: {output_file}")
        colorprint(textcolor="white",msg=f" - from Notes folder: '{folder}', Notes title:' {title}', ModDate: '{formatted_date}', Markdown title: '{quoted_title}', Exported Date: '{current_datetime}'")
        print(" ")
        
        notes_data.append([folder, title, formatted_date, quoted_title, current_datetime])
        
    # Write to CSV
    mode = 'a' if os.path.exists(output_file) else 'w'
    with open(output_file, mode, newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if mode == 'w':  # Only write header for new files
            writer.writerow(['Folder', 'Original Title', 'Last Modified', 'Exported Title', 'Exported Date'])
        writer.writerows(notes_data)
        
    colorprint(textcolor="green",msg=f"SUCCESS: Exported {len(notes_data)} notes to '{output_file}'", addseparator=True)
    
    return notes_data



##### Describe this function

def move_processed_notes(folder_source, folder_dest, max_notes, create=True):
    ''' Move processed notes into destination folder '''
    
    # if processed_notes exists, then that stage was a success, so next step:
    # create_gitmynotes_folder(folder_dest) so we have a place to move notes
    if create:
        success, message = create_gitnotes_folder(folder_dest)
    
        if success:
            colorprint(textcolor="green",msg=f"Success: {message}")
        else:
            colorprint(textcolor="red",msg=f"Failed: {message}")
    
    
    #print(f"Now to move up to {max_notes} notes from '{folder_source}' to '{folder_dest}'")
    
    # Escape any quotes in folder names
    folder_source_escaped = folder_source.replace('"', '\\"')
    folder_dest_escaped = folder_dest.replace('"', '\\"')
    
    applescript_movenote = f'''
    tell application "Notes"
        set targetAccount to "iCloud"
        tell account targetAccount
            try
                set sourceFolder to folder "{folder_source_escaped}"
                set destFolder to folder "{folder_dest_escaped}"
                set theNotes to every note of sourceFolder
                set noteCount to (count of theNotes)
                
                -- Check if we have notes to move
                if noteCount is 0 then
                    return "No notes found in source folder"
                end if
                
                -- Determine how many notes to actually move
                if {max_notes} ≤ noteCount then
                    set notesToMove to {max_notes}
                else
                    set notesToMove to noteCount
                end if
                
                repeat with i from 1 to notesToMove
                    try
                        move item i of theNotes to destFolder
                    on error errMsg
                        return "Error moving note " & i & ": " & errMsg
                    end try
                end repeat
                
                return "SUCCESS: Moved " & notesToMove & " notes"
            on error errMsg
                return "Error: " & errMsg
            end try
        end tell
    end tell
    '''
    
    result_move, output_move = process_applescript(applescript_movenote)
    #print(f"applescript_movenote result: {result_move} {output_move}")
    return result_move
   



##### Describe this function

def create_gitnotes_folder(folder: str) -> Tuple[bool, str]:
    """
    Create a folder in macOS Notes app under iCloud account.
    
    Args:
        folder (str): Name of the folder to create
        
    Returns:
        Tuple[bool, str]: (success status, message/error details)
    """
    colorprint(textcolor="white",msg=f"Attempting to create Notes folder: {folder}")
    
    # Properly escape quotes in folder name for AppleScript
    folder_escaped = folder.replace('"', '\\"')
    
    applescript = f'''
    tell application "Notes"
        try
            set targetAccount to "iCloud"
            tell account targetAccount
                if not (exists folder "{folder_escaped}") then
                    make new folder with properties {{name:"{folder_escaped}"}}
                    return "Folder created successfully"
                else
                    return "Folder already exists"
                end if
            end tell
        on error errMsg
            return "Error: " & errMsg
        end try
    end tell
    '''
    
    return process_applescript(applescript)



##### Describe this function

def process_applescript(applescript):
    ''' generic function to process applescript and return a result object'''
    colorprint(textcolor='white', msg=f"Processing AppleScript...")
    
    try:
        result = subprocess.run(
            ['osascript', '-e', applescript],
            capture_output=True,
            text=True,
            check=True  # This will raise CalledProcessError if osascript fails
        )
        
        ## Set the applescript blank so process_applescript can be used repeatedly
        applescript = ""
        
        # Check for any stderr output
        if result.stderr:
            return False, f"AppleScript Error: {result.stderr}"
            
        # Check the actual output
        output = result.stdout.strip()
        if "Error:" in output:
            return False, output
        else:
            return True, output
            
    except subprocess.CalledProcessError as e:
        return False, f"Process Error: {e.stderr}"
    except Exception as e:
        return False, f"Unexpected Error: {str(e)}"



def get_foldernotecount(folder=None):

    if folder:
        colorprint(textcolor="magenta",msg=f"No --max-notes set. Using count of notes in folder: {folder}")
        # Properly escape quotes in folder name for AppleScript
        folder_escaped = folder.replace('"', '\\"')
        
        applescript_notecount = f'''
        tell application "Notes"
            set targetAccount to "iCloud"
            tell account targetAccount
                if length of "{folder_escaped if folder_escaped else ''}" > 0 then
                    try
                        set folderToCount to folder "{folder_escaped}"
                        set folderNotes to every note in folderToCount
                        set folderNoteCount to (count of folderNotes)
                        return folderNoteCount
                    on error
                        log "Folder {folder_escaped} not found"
                        return 0
                    end try
                end if
            end tell
         end tell
        '''
        
        result,output_count = process_applescript(applescript_notecount)
        return int(output_count)
        
    else:
        print("No folder set. ToDo: work thru defaults flow.")



def restore_source_foldernote(folder_source, folder_bkup, restore_notes):
    ## if count of notes in folder_source is 0, and count of folder_dest is > 0
    ## then move all the notes from dest back to source. (as it was in the beginning, so shall...)
    
    if restore_notes != 'empty' and restore_notes != 'always':
        return
    
    
    source_count = get_foldernotecount(folder_source)
    bkup_count = get_foldernotecount(folder_bkup)
    #print(f"'{folder_source}' notecount: {source_count}")
    #print(f"'{folder_bkup}' notecount: {bkup_count}")
    
    if restore_notes == 'empty':
       if source_count == 0:
            if bkup_count > 0:
                print(f"Source folder {folder_source} notecount is {source_count}!")
                print(f"Option '--restore-notes={restore_notes}' so processed notes in '{folder_bkup}' will be moved back.")
                #print(f"Moving {bkup_count} Notes from {folder_bkup} into original source folder: {folder_source}")
                restore_result = move_processed_notes(folder_bkup, folder_source, bkup_count, create=False)
                
                return restore_result
            
    if restore_notes == 'always':
        if bkup_count > 0:
            print(f"Source folder {folder_source} not empty! Contains {source_count} un-backed-up notes.")
            print(f"Option --restore-notes={restore_notes} so processed notes in {folder_bkup} will be moved back.")
            print(f"WARNING: This non-'empty' setting can cause some notes to never be backed up.")
            restore_result = move_processed_notes(folder_bkup, folder_source, bkup_count, create=False)
                
            return restore_result
    else:
        return



def update_yaml_config(file_path, key, value):
    """
    Updates a specific key-value pair in a YAML config file while preserving comments and formatting.
    
    Args:
        file_path (str): Path to the YAML configuration file
        key (str): The key to update
        value: The new value for the specified key
    """
    # Use ruamel.yaml to preserve comments and formatting
    yaml_handler = YAML()
    yaml_handler.preserve_quotes = True  # Preserve existing quote styles
    yaml_handler.width = 4096  # Prevent automatic line wrapping

    # Read the existing file
    with open(file_path, 'r') as file:
        config = yaml_handler.load(file)
    
    # Update the specific key
    config[key] = value
    
    # Write back to the file, preserving original structure
    with open(file_path, 'w') as file:
        yaml_handler.dump(config, file)




def build_initial_msg(this_msg=None, folder=None, max_notes=None, export_path=None, github_url=None):
    # get some values for an initial msg
    
    if this_msg:
        initial_msg = f'''{this_msg}
'''    
    else:
        initial_msg = f'''    Welcome, 'tis a good day to GitMyNotes

'''
    if folder:
        initial_msg += f'''    - Notes folder: {folder}
'''
    if max_notes:
        initial_msg += f'''    - max-notes: {max_notes}
'''
    if export_path:
        initial_msg += f'''    - Export to: {export_path}
'''
    if github_url:
        initial_msg += f'''    - GitHub repo: {github_url}
'''
    
    return initial_msg



def build_final_msg(gitnotes_url, audit_file, usage_totals, share_url):
    # get some values for an initial msg
    
    
    final_msg = f'''    GitMyNotes actions complete!

'''
    if gitnotes_url:
        final_msg += f'''    - Check your GitMyNotes: {gitnotes_url}
'''
    if audit_file:
        final_msg += f'''    - Check your audit file: {audit_file}
'''
    if usage_totals:
        final_msg += f'    - Runs::Folders::Notes: '+str(usage_totals[0])+'::'+str(usage_totals[1])+'::'+str(usage_totals[2])
    final_msg += f'''
'''
    if share_url:
        final_msg += f'''    - Tell your friends, learn more:
'''
    if share_url:
        final_msg += f'''      http://GitMyNotes.com/share?iam=872g2876g2
'''
    
    return final_msg




##### Describe this function

def main():

    ######## ----  Get DEFAULT_& vars from config file     ---- #######    
    DEFAULT_NOTES_FOLDER_FORCE = None ##special case not in config file because... reasons.
    
    cfg = load_configs_from_file()
    DEFAULT_GITHUB_URL = cfg['DEFAULT_GITHUB_URL']
    
    DEFAULT_NOTES_FOLDER = cfg['DEFAULT_NOTES_FOLDER']
    DEFAULT_EXPORT_PATH = cfg['DEFAULT_EXPORT_PATH']
    DEFAULT_BATCH_SIZE = cfg['DEFAULT_BATCH_SIZE']
    DEFAULT_NOTES_WRAPPERDIR = cfg['DEFAULT_NOTES_WRAPPERDIR']
    DEFAULT_PROCESSED_FOLDER_ENDING = cfg['DEFAULT_PROCESSED_FOLDER_ENDING']
    DEFAULT_AUDIT_FILE_ENDING = cfg['DEFAULT_AUDIT_FILE_ENDING']
    DEFAULT_LOOPCOUNT_BEFORE_CONFIRM = cfg['DEFAULT_LOOPCOUNT_BEFORE_CONFIRM']
    DEFAULT_NEWLINE_DELIMITER = cfg['DEFAULT_NEWLINE_DELIMITER']
    DEFAULT_RESTORE_NOTES = cfg['DEFAULT_RESTORE_NOTES']
    
    USAGE_GITMYNOTES_TOTAL = cfg['USAGE_GITMYNOTES_TOTAL']
    USAGE_FOLDERS_PROCESSED = cfg['USAGE_FOLDERS_PROCESSED']
    USAGE_NOTES_PROCESSED = cfg['USAGE_NOTES_PROCESSED']
    
    ######## ----  Parse the args provided on CLI    ---- #######    
    parser = argparse.ArgumentParser(description="Export macOS Notes to GitHub.")
    parser.add_argument('--folder', type=str, 
                      default=DEFAULT_NOTES_FOLDER,
                      help=f"[str] Specific Notes folder to export.(default: '{DEFAULT_NOTES_FOLDER}')")
    parser.add_argument('--force', action='store_true',
                      default=DEFAULT_NOTES_FOLDER_FORCE,
                      help=f"[bool] Use as '--force' (no 'true' or 'false' value allowed) to over-ride to the default required user confirmation to process the full count of Notes in the specified folder when it exceed 5x the batch size -- which could be hundreds of notes and could take a looooong time.(default: confirmation will be required)")
    parser.add_argument('--max-notes', '--maxnotes', type=int, 
                      help=f'[int] Maximum number of notes to process.')
    parser.add_argument('--batch-size', type=int,
                      default=DEFAULT_BATCH_SIZE,
                      help=f'[int] The number of notes to convert, and git add/commit/push per loop, calculated a max-notes/batch-size. Especially useful for initial runs.(default: {DEFAULT_BATCH_SIZE})')  
    parser.add_argument('--export-path', '--exportpath',type=str, 
                      default=os.path.expanduser(f"{DEFAULT_EXPORT_PATH}"),
                      help=f'[str] Path to export the notes (default: {DEFAULT_EXPORT_PATH})')
    parser.add_argument('--github-url','--githuburl', type=str,
                      default=DEFAULT_GITHUB_URL,
                      help=f'[str] GitHub repository URL. (default: {DEFAULT_GITHUB_URL})')                       
    parser.add_argument('--newline-delimiter', '--newlinedelimiter',type=str, 
                      default=DEFAULT_NEWLINE_DELIMITER,
                      help=f"[str] Default CSV newline delimiter (default: '{DEFAULT_NEWLINE_DELIMITER}')")
    parser.add_argument('--audit-file-ending','--auditfileending', type=str, 
                      default=DEFAULT_AUDIT_FILE_ENDING,
                      help=f"[str] The audit file extension (default: '{DEFAULT_AUDIT_FILE_ENDING}')")
    parser.add_argument('--restore-notes','--restorenotes', type=str, 
                      default=DEFAULT_RESTORE_NOTES,
                      help=f"[str] Options: 'empty' or 'always'  Determines when to move notes from '<folder>_{DEFAULT_PROCESSED_FOLDER_ENDING}' back to their original source Notes folder. The option 'empty' will not restore notes until notecount is 0 in source folder, while 'always' will restore at the end of each max-notes run. Set to 'never' to never move notes back to source folder. (default: '{DEFAULT_RESTORE_NOTES}')")



    args = parser.parse_args()
    
    ## Set up vars to use later
    args_max_notes = args.max_notes
    args_folder = args.folder
    args_wrapper_dir = DEFAULT_NOTES_WRAPPERDIR
    audit_file = f"./{args_folder}{DEFAULT_AUDIT_FILE_ENDING}"


    ## set up the initial msg to let people know setup details
    initial_msg = build_initial_msg(this_msg="", folder=args_folder, max_notes=args_max_notes, export_path=args.export_path, github_url=args.github_url)
    colorprint(textcolor='cyan', msg=f"{initial_msg}", addseparator=True)



    ######## ----  Do INIT work, ensure DEFAULT_GITHUB_URL has been changed    ---- #######    
    if USAGE_GITMYNOTES_TOTAL == 0:
        # leave this here for later 1st timer things
#         print("Hello first timer!")
        if len(USAGE_FOLDERS_PROCESSED) == 1:
            if USAGE_FOLDERS_PROCESSED[0] == 'placeholder':
                 USAGE_FOLDERS_PROCESSED[0] = args_folder
                 update_yaml_config('./gmn_config.yaml', 'USAGE_FOLDERS_PROCESSED', USAGE_FOLDERS_PROCESSED)
#         print(f"USAGE_FOLDERS_PROCESSED : {USAGE_FOLDERS_PROCESSED}")
#         sys.exit(1)
    
    substring = '<ChangeMe>'
    if substring in DEFAULT_GITHUB_URL:
        changeme_msg = "WHOA, the 'DEFAULT_GITHUB_URL' setting in 'gmn.config.yaml' has not been updated to your Github username"
        colorprint(textcolor="magenta", msg=f"{changeme_msg}")
        
        usage_github_username = input("Please enter your GitHub username: ")
        print(f"The 'DEFAULT_GITHUB_URL' will be updated to 'https://github.com/{usage_github_username}/gitmynotes'")
        ## now update the yaml file
        update_yaml_config('gmn_config.yaml', 'DEFAULT_GITHUB_URL', f"https://github.com/{usage_github_username}/gitmynotes")
        cfg = load_configs_from_file()
        DEFAULT_GITHUB_URL = cfg['DEFAULT_GITHUB_URL']
        
        
        ## RE-DO the initial msg to let people know setup details have changed
        initial_msg = build_initial_msg(this_msg="  Thanks for updating your GitHub username!", folder=args_folder, max_notes=args_max_notes, export_path=args.export_path, github_url=DEFAULT_GITHUB_URL)
        colorprint(textcolor='cyan', msg=f"{initial_msg}", addseparator=True)



    ######## ----  BUILD initial dirs per args and DEFAULTS    ---- #######
    os.makedirs(args.export_path, exist_ok=True)
    if args_folder:
        export_path_w_folder = f"{args.export_path}/{args_wrapper_dir}/{args_folder}"
        os.makedirs(export_path_w_folder, exist_ok=True)



    ######## ----  Setup the git repo per args and DEFAULTs    ---- #######
    setup_git_repo(args.export_path, DEFAULT_GITHUB_URL)



    ######## ----  check for 5x batch size in args_folder_count    ---- #######
    ''' if args_folder not set (and defaults to Notes) or set to folder with 5xBatch notes, warn user'''
    
    args_folder_count = 0
    args_folder_count = get_foldernotecount(args_folder)
    if args_max_notes:
        if args_max_notes > args_folder_count:
            notes_to_process = args_folder_count
        else:
            notes_to_process = args_max_notes
    else:
        notes_to_process = args_folder_count
    
    if notes_to_process > (args.batch_size * DEFAULT_LOOPCOUNT_BEFORE_CONFIRM):
        if args.force:
            #print(f"--force was set, so go on without confirm...")
            return
        else:
            #print(f"--force not set, and MORE than {DEFAULT_LOOPCOUNT_BEFORE_CONFIRM} batches required, must confirm")
            confirm_warn = f'''WHOA. {notes_to_process} notes to process in '{args_folder}' folder!

    <<<< Confirmation Required.>>>>

Add '--force' to skip confirmation in the future.'''
            colorprint(textcolor='magenta', msg=f"{confirm_warn}", addseparator=True)
            confirm_msg = f''' Enter a number up to {notes_to_process} of notes to process, or 'x' to eXit.
  [Or 'enter' to process all {notes_to_process} notes] : '''
            
            confirm_num = input(f"{confirm_msg}") or f"{notes_to_process}"
            if confirm_num == 'x' or confirm_num == '0': 
                colorprint(textcolor='red', msg="    Exiting GitMyNotes...", addseparator=True)
                sys.exit(1)
            confirm_num = int(confirm_num)
            if confirm_num > notes_to_process:
                confirm_num = notes_to_process 
            #print(f"aa Notes to process: {confirm_num}")
            notes_to_process = confirm_num
            
    else:
        pass
        #print(f"LESS than {DEFAULT_LOOPCOUNT_BEFORE_CONFIRM} batches required, go on...")
    
    
    ######## ----  END check for 5x batch size in arg.folder    ---- #######
    
    
    
    colorprint(textcolor="white",msg=f"Notes to process: {notes_to_process}")
    
    ''' Process in a loop of batches'''
    loop_count = math.ceil(notes_to_process / args.batch_size)
    for x in range(1,loop_count+1): 
        colorprint(textcolor="cyan",msg=f"    Begin export of Notes with batch {x} of {loop_count}", addseparator=True)
        
        
        if loop_count == 1:
            notes_to_export = notes_to_process
        else:
            notes_to_export = args.batch_size
        
        notes_processed = 0
        notes_processed = export_notes_to_markdown(
            args.export_path,
            args_folder,
            notes_to_export,
            args_wrapper_dir
        )
        
        if notes_processed > 0:
            colorprint(textcolor="green",msg=f"SUCCESS: Exported {notes_processed} Notes to local folder {args.export_path}")
            
            commit_and_push(args.export_path, args_folder, args_wrapper_dir)
        else:
            colorprint(textcolor="magenta",msg=f"No notes were processed, skipping git commit")
            #print(f"------------------------------------")
            
        ## if notes were process to git, then create the audit trail and move the notes
        if notes_processed > 0:
            #print(f"NOTES PROCESSED > 0: {notes_processed}")
            colorprint(textcolor="white",msg=f"Notes to export to markdown: {notes_to_export}")
            processednotes_data = export_notes_metadata(
                output_file=audit_file,
                folder=args_folder,
                max_notes=notes_processed,
                newline_delimiter=args.newline_delimiter
            )
        else:
            processednotes_data = 0	
            
            
        if processednotes_data:
            move_result = move_processed_notes(
                folder_source=args_folder,
                folder_dest=f"{args_folder}{DEFAULT_PROCESSED_FOLDER_ENDING}",
                max_notes=notes_to_export
            )
        
        
        else:
            move_result = 0
            colorprint(textcolor="magenta",msg=f"No Notes to Move")
        
        if move_result:
            #print(f"================================")
            colorprint(textcolor="green",msg=f"SUCCESS: Moved notes to Notes folder: '{args_folder}{DEFAULT_PROCESSED_FOLDER_ENDING}'", addseparator=True)
            #print(f"================================")
        else:
            #print(f"================================")
            colorprint(textcolor="red",msg=f"    !!! FAILED to MOVE notes !!!", addseparator=True)
            #print(f"================================")
    
    ## check for restore-empty-source-folder to decide what to do with contents of folder_GitMyNotes backup folders
    print(f"Option to restore the source folder is '{args.restore_notes}'")
    
    restore_result = 0
    restore_result = restore_source_foldernote(folder_source=args_folder, folder_bkup=f"{args_folder}{DEFAULT_PROCESSED_FOLDER_ENDING}", restore_notes=args.restore_notes)
        
    if restore_result:
        colorprint(textcolor="green",msg=f"SUCCESS: RESTORED notes to {args_folder} from {args_folder}{DEFAULT_PROCESSED_FOLDER_ENDING}", addseparator=True)
    
    else:
        restore_declined_msg = f'''    << Notes not restored to '{args_folder}' >> 
    Set --restore-notes=empty to move notes back to '{args_folder}' when notecount is 0
    Set --restore-notes=always to move notes back to '{args_folder}' after every backup'''
        colorprint(textcolor="red",msg=f"{restore_declined_msg}", addseparator=True)
    
    
    
    ######## ----  update usage counts    ---- #######
    USAGE_GITMYNOTES_TOTAL_NEW = int(USAGE_GITMYNOTES_TOTAL) + 1
    update_yaml_config('./gmn_config.yaml', 'USAGE_GITMYNOTES_TOTAL', USAGE_GITMYNOTES_TOTAL_NEW)
    
    if args_folder not in USAGE_FOLDERS_PROCESSED:
        USAGE_FOLDERS_PROCESSED.append(args_folder)
        update_yaml_config('./gmn_config.yaml', 'USAGE_FOLDERS_PROCESSED', USAGE_FOLDERS_PROCESSED)
    
    USAGE_NOTES_PROCESSED_NEW = int(USAGE_NOTES_PROCESSED) + int(notes_processed)
    update_yaml_config('./gmn_config.yaml', 'USAGE_NOTES_PROCESSED', USAGE_NOTES_PROCESSED_NEW)
    
    
    ## Prep for final msg so user knows what happened
    if args_wrapper_dir:
        final_gitnotes_url = f"{DEFAULT_GITHUB_URL}/tree/main/{args_wrapper_dir}/{args_folder}"
    else:
        final_gitnotes_url = f"{DEFAULT_GITHUB_URL}/tree/main/{args_folder}"
    
    usage_totals = [int(USAGE_GITMYNOTES_TOTAL_NEW), len(USAGE_FOLDERS_PROCESSED), int(USAGE_NOTES_PROCESSED_NEW)]
    
    share_url = "https://GitMyNotes.com/share?iam=123abc456"
    
    final_msg = build_final_msg(gitnotes_url=f"{final_gitnotes_url}", audit_file=f"{audit_file}", usage_totals = usage_totals, share_url=f"{share_url}")
    
    colorprint(textcolor="cyan",msg=f"{final_msg}", addseparator=True)
    
    
    
    
    
############# END OF MAIN




##### ADD SOME COLORs
# pinched and tweaked from https://github.com/impshum/Multi-Quote/blob/master/run.py
class color:
    white, cyan, blue, red, green, yellow, magenta, black, gray, bold = '\033[0m', '\033[96m','\033[94m', '\033[91m','\033[92m','\033[93m','\033[95m', '\033[30m', '\033[30m', "\033[1m"  


# maybe add bks, bolds, etc from https://godoc.org/github.com/whitedevops/colors
class bkcolor:
  resetall = "\033[0m"
  default      = "\033[49m"
  black        = "\033[40m"
  red          = "\033[41m"
  green        = "\033[42m"
  yellow       = "\033[43m"
  blue         = "\033[44m"
  magenta      = "\033[45m"
  cyan         = "\033[46m"
  lightgray    = "\033[47m"
  darkgray     = "\033[100m"
  lightred     = "\033[101m"
  lightgreen   = "\033[102m"
  lightyellow  = "\033[103m"
  lightblue    = "\033[104m"
  lightmagenta = "\033[105m"
  lightcyan    = "\033[106m"
  white        = "\033[107m"
  
  
  
  
def colorprint(textcolor='white', msg=None, addseparator=False, textdefault='white', bkcolor=None):
    '''Pass a NEW color, then a string to print and this function will set msg back to textdefault'''
    
    # Get color codes using getattr()
    selected_color = getattr(color, textcolor)
    default_color = getattr(color, textdefault)
    
    if addseparator:
        print(selected_color + "------------------------------------------------" + default_color)
    
    # now the msg
    print(selected_color + f"{msg}" + default_color)
    
    if addseparator:
        print(selected_color + "------------------------------------------------" + default_color)
    
    print(f" ")
    return



            
if __name__ == "__main__":
    main()