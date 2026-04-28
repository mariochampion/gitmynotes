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


#### USING THIS SCRIPT

## Export up to 10 notes from a specific folder
#  python gitmynotes.py --folder="somefolder" --max-notes=10

## Export all notes from a specific folder
#  python gitmynotes.py --folder="somefolder"

## Specify to restore notes folder even if not emptied
#  python gitmynotes.py --folder-name="somefolder" --max-notes=10 --restore=always

## go crazy and specify nothing, to get all the defaults!
#  python gitmynotes.py


import subprocess
import os, sys
import argparse
import math
import csv
import logging
from datetime import datetime
from typing import Tuple
from ruamel.yaml import YAML
from enum import Enum

class PrintLevel(Enum):
    NONE = 0
    RESULTS = 1
    DEBUG = 2
    ALL = 3


# R4 (incremental): module-level logger. setup_logging() in main() attaches a
# FileHandler at <script_dir>/gitmynotes.log so warning-/error-level events flow
# to a parseable record alongside the existing colored TTY output. Colored
# print_color() callsites are preserved as-is; logger.warning / logger.error /
# logger.exception calls are added in paired form at each warning/error site so
# non-interactive runs (Cowork routines, cron) get a structured log without
# ANSI codes. Chatty debug_print / results_print are deliberately untouched in
# this pass.
logger = logging.getLogger("gitmynotes")




#### USER CONFIGS

PRINT_LEVEL = PrintLevel.ALL

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
            print_color(textcolor="green",msg=f"SUCCESS: GIT INIT with {repo_path}")
        except:
            logger.exception(f"ERROR: Did not GIT INIT {repo_path}")
            print_color(textcolor="red",msg=f"ERROR: Did not GIT INIT {repo_path}")
        try:
            subprocess.run(['git', 'remote', 'add', 'origin', DEFAULT_GITHUB_URL], cwd=repo_path)
            print_color(textcolor="green",msg=f"SUCCESS: GIT REMOTE ADD ORIGIN with {repo_path}")
        except:
            logger.exception(f"ERROR: Did not GIT REMOTE ADD ORIGIN with {repo_path}")
            print_color(textcolor="RED",msg=f"ERROR: Did not GIT REMOTE ADD ORIGIN with {repo_path}")
        try:
            subprocess.run(['git', 'branch', '-m', 'main'], cwd=repo_path)
            print_color(textcolor="green",msg=f"SUCCESS: GIT BRANCH -M MAIN with {repo_path}")
        except:
            logger.exception(f"ERROR: GIT BRANCH -M MAIN with {repo_path}")
            print_color(textcolor="red",msg=f"ERROR: GIT BRANCH -M MAIN with {repo_path}")


        # Add this to handle remote repository state
        try:
            subprocess.run(['git', 'pull', 'origin', 'main'], cwd=repo_path)
            print_color(textcolor="green",msg=f"Remote content pulled")
        except:
            logger.warning(f"No remote content to pull from {repo_path}")
            print_color(textcolor="magenta",msg=f"No remote content to pull")



##### Describe this function

def export_notes_to_markdown(DEFAULT_CURRENTNOTE_FILE, export_path, notes_account, folder_name=None, max_notes=None, wrapper_dir=None):
    """Export Notes using applescript/osascript with folder and count limits.

    notes_account scopes every Notes lookup (folder + iteration) to the specified
    account (e.g. 'iCloud', 'On My Mac'). Threaded through from --notes-account /
    DEFAULT_NOTES_ACCOUNT (R6).
    """

    ## tell the people some information
    if (max_notes > 0 and folder_name !="" and wrapper_dir !=""):
        print_color(textcolor="white",msg=f"Starting export of {max_notes} Notes from '{folder_name}' into '{wrapper_dir}/{folder_name}'...")
    elif (max_notes > 0 and folder_name !="" and wrapper_dir==None):
        print_color(textcolor="white",msg=f"Starting export of {max_notes} Notes from '{folder_name}'...")
    elif (max_notes > 0 and folder_name==None and wrapper_dir==None):
        print_color(textcolor="white",msg=f"Starting export of {max_notes} Notes...")
    elif (max_notes==None and folder_name==None and wrapper_dir==None):
        print_color(textcolor="white",msg=f"Starting export of all Notes...")

    # Escape quotes in the account name for AppleScript (R6)
    notes_account_escaped = notes_account.replace('"', '\\"')

    applescript = f'''
    tell application "Notes"
        set targetAccount to "{notes_account_escaped}"
        tell account targetAccount
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
        if {max_notes} > 0 then
        	set maxToProcess to {max_notes}
        else
        	set maxToProcess to noteCount
        end if

        if maxToProcess < noteCount then
        	set notesToProcess to maxToProcess
        else
        	set notesToProcess to noteCount
        end if

        -- B4: track empty/locked notes so caller can report them to the user.
        set lockedCount to 0
        set lockedMarker to "<div><i>[empty or locked note -- no content exported by GitMyNotes]</i></div>"

        repeat with i from 1 to notesToProcess
            set currentNote to item i of allNotes
            set noteTitle to the name of currentNote
            -- Write to file and track title for when unsupported note breaks.
            -- B9: use the absolute path the Python caller resolved for us (config
            -- value is anchored to the script dir in main() if it wasn't already
            -- absolute). Otherwise osascript's shell cwd (usually the user's home)
            -- and Python's cwd could disagree, leaving get_currentnote_data to
            -- silently read stale data from a previous run.
            do shell script "echo " & i & "++++" & quoted form of noteTitle & " > " & quoted form of "{DEFAULT_CURRENTNOTE_FILE}"
            --log ("Exporting note: " & noteTitle)

            set linebreaker to "\n"
            set noteCreateDate to "<div><b>Creation Date:</b> " & creation date of currentNote & "<br></div>"
            set noteModDate to "<div><b>Modification Date:</b> " & modification date of currentNote & "<br></div>"
            -- B4: fetching `body of` on a locked/password-protected note returns "" (not
            -- an error). Wrap in try as a belt-and-suspenders guard anyway, and substitute
            -- a stub marker for any empty body so the committed .md is self-explanatory
            -- instead of silently mostly-empty.
            try
                set noteContent to the body of currentNote
            on error
                set noteContent to ""
            end try
            if noteContent is "" then
                set noteContent to lockedMarker
                set lockedCount to lockedCount + 1
            end if

            -- Clean the title for use as filename
            set cleanTitle to do shell script "echo " & quoted form of noteTitle & " | sed 's/[^a-zA-Z0-9.]/-/g' | tr '[:upper:]' '[:lower:]'"
            set fileName to cleanTitle & ".md"

            -- Write to file
            do shell script "echo " & quoted form of noteCreateDate & quoted form of linebreaker & quoted form of noteModDate & quoted form of linebreaker & quoted form of noteContent & " > " & quoted form of export_path_full & "/" & fileName
        end repeat

        -- B4: compound return value so Python can report locked count without needing a
        -- side-channel file or stderr (stderr would trip the B1 "type 100002" branch).
        return (notesToProcess as string) & "|" & (lockedCount as string)
        end tell
    end tell
    '''
    result = subprocess.run(['osascript', '-e', applescript], capture_output=True, text=True)
    
    if result.stdout:
        results_print(f"EXPORT NOTES stdout: {result.stdout}")
        
    if result.stderr:
        results_print(f"Error in EXPORT NOTES:")
        results_print(f"{result.stderr}")
        
        
        ### LOOK FOR ERROR OF UNSPPORTED (usually image) IN NOTE,
        ### AND MOVE THIS TO <foldername>_UNSUPPORTED
        
        searchstring = "type 100002"
        if searchstring in result.stderr:
            # currentnote.txt is written by AppleScript immediately before each note's
            # export, so its 1-based index points at the failing note. Notes 1..(i-1)
            # were already exported successfully to disk -- we must return that count
            # so the caller commits + audits + moves them. Returning 0 here would
            # orphan those files on disk with no audit row and leave the originals in
            # the source folder, creating duplicates on the next run (the "zombie
            # exports" bug, B1).
            noteCount, noteTitle = get_currentnote_data(DEFAULT_CURRENTNOTE_FILE)
            print(f"{searchstring} is present for note '{noteTitle}'.")
            folder_dest = folder_name + "_unsupported"
            move_one_note(noteTitle, folder_name, folder_dest, notes_account, create=True)
            goodnotes = noteCount - 1
            logger.warning(
                f"Unsupported note '{noteTitle}' (folder '{folder_name}', index {noteCount}) aborted batch; "
                f"exported {goodnotes} note(s) before the failure."
            )
            print_color(textcolor="cyan", msg=f"Exported {goodnotes} note(s) successfully before hitting unsupported content; continuing with those.")
            return goodnotes

        else:
            debug_print(f"{searchstring} is not present.")
        
        return 0


    # B4: stdout is a compound "exported|lockedCount" string (see AppleScript `return`).
    # The `type 100002` branch above still returns a plain int directly, so this parser
    # only runs on the success path.
    stdout_val = result.stdout.strip() if result.stdout else ""
    if not stdout_val:
        return 0
    if '|' in stdout_val:
        try:
            exported_str, locked_str = stdout_val.split('|', 1)
            exported_count = int(exported_str.strip())
            locked_count = int(locked_str.strip())
        except ValueError:
            debug_print(f"Could not parse compound export result: {stdout_val!r}")
            return 0
        if locked_count > 0:
            plural = "s" if locked_count != 1 else ""
            logger.warning(
                f"{locked_count} empty or locked note{plural} committed as stub{plural} "
                f"in folder '{folder_name}' (title + dates only; no content available from Notes.app)."
            )
            print_color(
                textcolor="yellow",
                msg=f"NOTE: {locked_count} empty or locked note{plural} committed as stub{plural} (title + dates only; no content available from Notes.app).",
            )
        return exported_count
    # Backwards-compatible fallback: plain int return (shouldn't happen post-B4 but safe).
    try:
        return int(stdout_val)
    except ValueError:
        return 0



##### Describe this function

def git_add_commit_push(repo_path, folder_name=None, wrapper_dir=None):
    """Commit changes and push to GitHub"""
    # Always operate from the git root directory
       
    result_gitadd = subprocess.run(['git', 'add', f'{wrapper_dir}'], cwd=repo_path)
    if result_gitadd.returncode == 0:
        print_color(textcolor="green",msg=f"Successful GIT ADD to origin/main.")
        results_print(f"1 result_gitadd: {result_gitadd}")
    else:
        logger.error(f"GIT ADD failed (returncode={result_gitadd.returncode}) in repo '{repo_path}', wrapper_dir='{wrapper_dir}'.")
        print_color(textcolor="red",msg=f"Error GIT ADD to origin/main:")
        results_print(f"2 result_gitadd: {result_gitadd}")
    
    folder_info = f"from folder '{folder_name}'" if folder_name else ""
    commit_message = f"Backed up {folder_info} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
    result_gitcommit = subprocess.run(['git', 'commit', '-m', commit_message], cwd=repo_path, capture_output=True, text=True)

    # Classify the commit result.
    # Git returns nonzero with a "nothing to commit" message when the staging area is empty.
    # This happens naturally when re-exporting notes whose content hasn't changed since the
    # last backup -- the exported .md is byte-identical to what's already committed. Treat
    # that case as benign (not a real error) so we still attempt the push below, which
    # drains any prior unpushed commits from earlier runs.
    nothing_to_commit = (
        result_gitcommit.returncode != 0
        and ("nothing to commit" in result_gitcommit.stdout
             or "nothing added to commit" in result_gitcommit.stdout)
    )
    commit_ok = (result_gitcommit.returncode == 0) or nothing_to_commit

    commit_print_msg = f'''    - repo path: {repo_path}
    - folder name:{folder_name}
    - commit message:{commit_message}
    '''

    if result_gitcommit.returncode == 0:
        print_color(textcolor="green",msg=f"Successful GIT COMMIT to origin/main.")
        print_color(textcolor="white",msg=f"{commit_print_msg}")
    elif nothing_to_commit:
        print_color(textcolor="cyan",msg=f"No changes to commit -- note content is identical to what's already in git. (Normal when re-exporting unchanged notes.)")
        print_color(textcolor="white",msg=f"{commit_print_msg}")
    else:
        logger.error(
            f"GIT COMMIT failed (returncode={result_gitcommit.returncode}) in repo '{repo_path}'. "
            f"folder='{folder_name}'. stdout={result_gitcommit.stdout!r} stderr={result_gitcommit.stderr!r}"
        )
        print_color(textcolor="red",msg=f"Error GIT COMMIT to origin/main:")
        print_color(textcolor="white",msg=f"{commit_print_msg}")
        results_print(f"result_gitcommit: {result_gitcommit}")


    if commit_ok:
        # Try to pull and rebase before pushing
        try:
            subprocess.run(['git', 'pull', '--rebase', 'origin', 'main'], cwd=repo_path, capture_output=True, text=True)
        except:
            logger.warning(f"git pull --rebase failed before push in repo '{repo_path}'; continuing to push.")
            print_color(textcolor="magenta",msg=f"No remote changes to pull")

        result_push = subprocess.run(['git', 'push', 'origin', 'main'], cwd=repo_path, capture_output=True, text=True)

        if result_push.returncode == 0:
            # Note: git emits "Everything up-to-date" on stderr with returncode 0 when
            # there's nothing new to push -- treated the same as a real push here.
            print_color(textcolor="green",msg=f"Successful GIT PUSH to origin/main.")
            results_print(f"1 result_push: {result_push}")
            print(" ")
        else:
            logger.error(
                f"GIT PUSH failed (returncode={result_push.returncode}) in repo '{repo_path}'. "
                f"stdout={result_push.stdout!r} stderr={result_push.stderr!r}"
            )
            print_color(textcolor="red",msg=f"Error GIT PUSH to origin/main:")
            results_print(f"2 result_push: {result_push}")
            print(" ")
            # Optionally, try force push if regular push fails
	        # result = subprocess.run(['git', 'push', '-f', 'origin', 'main'], cwd=repo_path, capture_output=True, text=True)
    else:
        logger.error(f"Skipping GIT PUSH due to upstream commit error in repo '{repo_path}'.")
        print_color(textcolor="red",msg=f"Commit error so no GIT PUSH to origin/main:")
        print(" ")



##### Describe this function

def export_notes_metadata(output_file, folder, max_notes, newline_delimiter, notes_account):
    """
    Export macOS Notes metadata (title, quoted title, and modification date) to a CSV file.

    Args:
        output_file (str): Path to the output CSV file
        folder (str): Name of the folder to export notes from. Required; the
            all-folders case is guarded off at the top of main() (B10).
        max_notes (int): Maximum number of notes to export (None for all notes)
        newline_delimiter (str): Default newline delimiter (|||)
        notes_account (str): macOS Notes account to scope the lookup to (e.g.
            'iCloud', 'On My Mac'). Threaded through from --notes-account /
            DEFAULT_NOTES_ACCOUNT (R6).
    """

    debug_print(f"INSIDE export_notes_metadata: {output_file}, {folder}, {max_notes}, {newline_delimiter}, {notes_account}")


    # Escape quotes in the account name for AppleScript (R6)
    notes_account_escaped = notes_account.replace('"', '\\"')

    # AppleScript to get notes information
    applescript = f'''
    tell application "Notes"
        set targetAccount to "{notes_account_escaped}"
        tell account targetAccount
        set noteList to {{}}
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
	    --log ("Processing note: " & noteTitle)
	    -- clean noteTitle using quoted form to handle special characters
	    set noteTitle to do shell script ("echo " & quoted form of noteTitle & "| sed 's/,/-/g'")
	    -- Clean the title for use as filename, using quoted form again
	    set cleanTitle to do shell script ("echo " & quoted form of noteTitle & " | sed 's/[^a-zA-Z0-9.]/-/g' | tr '[:upper:]' '[:lower:]'")
	    set noteData to noteTitle &","& cleanTitle & ".md" &","& modification date of theNote & custom_delimiter
        copy noteData to the end of noteList
        end repeat
        return noteList
        end tell
    end tell
    '''
    
    result,output = process_applescript(applescript)
    results_print(f"process_applescript result: {result}")
    print("-------------------")
    results_print(f"process_applescript output: {output}")
    
    
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
        
        print_color(textcolor="white",msg=f"Adding row to audit file: {output_file}")
        print_color(textcolor="white",msg=f" - from Notes folder: '{folder}', Notes title:' {title}', ModDate: '{formatted_date}', Markdown title: '{quoted_title}', Exported Date: '{current_datetime}'")
        print(" ")
        
        notes_data.append([folder, title, formatted_date, quoted_title, current_datetime])
        
    # Write to CSV
    mode = 'a' if os.path.exists(output_file) else 'w'
    with open(output_file, mode, newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if mode == 'w':  # Only write header for new files
            writer.writerow(['Folder', 'Original Title', 'Last Modified', 'Exported Title', 'Exported Date'])
        writer.writerows(notes_data)
        
    print_color(textcolor="green",msg=f"22 SUCCESS: Exported {len(notes_data)} notes to '{output_file}'", addseparator=True)
    
    return notes_data



def get_currentnote_data(filename):
    with open(filename, 'r') as file:
        line = file.readline().strip()
        notecount, notetitle = line.split("++++")
        return int(notecount), notetitle



##### Describe this function

def move_one_note(note_name, folder_source, folder_dest, notes_account, create=True):
    ''' Move processed notes into destination folder '''

    # if processed_notes exists, then that stage was a success, so next step:
    # create_gitmynotes_folder(folder_dest) so we have a place to move notes
    if create:
        success, message = create_gitnotes_folder(folder_dest, notes_account)

        if success:
            print_color(textcolor="green",msg=f"Create notes folder Success: {message}")
        else:
            logger.error(f"Failed to create Notes folder '{folder_dest}' (account '{notes_account}'): {message}")
            print_color(textcolor="red",msg=f"Create notes folder Failed: {message}")


    debug_print(f"Now to move UNSUPPORTED note '{note_name}' from '{folder_source}' to '{folder_dest}'")

    # Escape any quotes in folder names + notes account name (R6)
    folder_source_escaped = folder_source.replace('"', '\\"')
    folder_dest_escaped = folder_dest.replace('"', '\\"')
    notes_account_escaped = notes_account.replace('"', '\\"')

    applescript_moveonenote = f'''
    tell application "Notes"
        set targetAccount to "{notes_account_escaped}"
        tell account targetAccount
            try
                set sourceFolder to folder "{folder_source_escaped}"
                set destFolder to folder "{folder_dest_escaped}"
                set theNote to first note of sourceFolder whose name is "{note_name}"
                
                -- Check if we have notes to move
                if theNote is missing value then
                    return "No such note found in source folder"
                end if
                
                -- Do the move
                try
                    move theNote to destFolder
                on error errMsg
                    return "Error moving note " & theNote & " : " & errMsg
                end try
                
                return "SUCCESS: Moved one note '" & theNote & "' to "  & destFolder
            on error errMsg
               return "Error: " & errMsg
            end try
        end tell
    end tell
    '''
    
    result_onemove, output_onemove = process_applescript(applescript_moveonenote)
    debug_print(f"applescript_moveonenote result: {result_onemove} {output_onemove}")

    logger.warning(
        f"Unsupported note '{note_name}' moved from '{folder_source}' to '{folder_dest}'. "
        f"Re-run command to drain remaining notes in this batch."
    )
    print_color(textcolor='red', msg=f'''    uh oh, unsupported note encountered: '{note_name}'
    Note moved to notes folder: '{folder_dest}'.
    Previous notes will be moved in this loop, but.
    please run your command again to ensure all notes are moved.''', addseparator=True)
    return 0
   




##### Describe this function

def move_processed_notes(folder_source, folder_dest, max_notes, notes_account, create=True):
    ''' Move processed notes into destination folder '''

    # if processed_notes exists, then that stage was a success, so next step:
    # create_gitmynotes_folder(folder_dest) so we have a place to move notes
    if create:
        success, message = create_gitnotes_folder(folder_dest, notes_account)

        if success:
            print_color(textcolor="green",msg=f"Create notes folder Success: {message}")
        else:
            logger.error(f"Failed to create Notes folder '{folder_dest}' (account '{notes_account}'): {message}")
            print_color(textcolor="red",msg=f"Create notes folder Failed: {message}")


    debug_print(f"Now to move up to {max_notes} notes from '{folder_source}' to '{folder_dest}'")

    # Escape any quotes in folder names + notes account name (R6)
    folder_source_escaped = folder_source.replace('"', '\\"')
    folder_dest_escaped = folder_dest.replace('"', '\\"')
    notes_account_escaped = notes_account.replace('"', '\\"')

    applescript_movenote = f'''
    tell application "Notes"
        set targetAccount to "{notes_account_escaped}"
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
    results_print(f"applescript_movenote result: {result_move} {output_move}")
    return result_move
   



##### Describe this function

def create_gitnotes_folder(folder: str, notes_account: str) -> Tuple[bool, str]:
    """
    Create a folder in macOS Notes app under the configured Notes account.

    Args:
        folder (str): Name of the folder to create
        notes_account (str): Notes account to scope the create to (e.g. 'iCloud',
            'On My Mac'). Threaded through from --notes-account / DEFAULT_NOTES_ACCOUNT (R6).

    Returns:
        Tuple[bool, str]: (success status, message/error details)
    """
    print_color(textcolor="white",msg=f"Attempting to create Notes folder: {folder}")

    # Properly escape quotes in folder + account name for AppleScript
    folder_escaped = folder.replace('"', '\\"')
    notes_account_escaped = notes_account.replace('"', '\\"')

    applescript = f'''
    tell application "Notes"
        try
            set targetAccount to "{notes_account_escaped}"
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
    # print_color(textcolor='white', msg=f"Processing AppleScript...")
    
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



def get_foldernotecount(folder, notes_account):

    if folder:
        debug_print(f"Getting count of notes in folder: {folder}")
        # Properly escape quotes in folder + account name for AppleScript (R6)
        folder_escaped = folder.replace('"', '\\"')
        notes_account_escaped = notes_account.replace('"', '\\"')

        applescript_notecount = f'''
        tell application "Notes"
            set targetAccount to "{notes_account_escaped}"
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
        results_print(f"'{folder_escaped}' notecount: {output_count}")
        print("")
        return int(output_count)
        
    else:
        print("No folder set. ToDo: work thru defaults flow.")



def restore_source_foldernote(folder_source, folder_bkup, restore_notes, notes_account):
    ## if count of notes in folder_source is 0, and count of folder_dest is > 0
    ## then move all the notes from dest back to source. (as it was in the beginning, so shall...)
    ## notes_account scopes every Notes lookup to the configured account (R6).

    if restore_notes != 'empty' and restore_notes != 'always':
        return


    source_count = get_foldernotecount(folder_source, notes_account)
    bkup_count = get_foldernotecount(folder_bkup, notes_account)



    if restore_notes == 'empty':
       if source_count == 0:
            if bkup_count > 0:
                results_print(f"Source folder {folder_source} notecount is {source_count}!")
                results_print(f"Option '--restore-notes={restore_notes}' so processed notes in '{folder_bkup}' will be moved back.")
                restore_result = move_processed_notes(folder_bkup, folder_source, bkup_count, notes_account, create=False)

                return restore_result

    if restore_notes == 'always':
        if bkup_count > 0:
            results_print(f"Source folder {folder_source} not empty! Contains {source_count} un-backed-up notes.") #this may sometime be not clear
            results_print(f"Option --restore-notes={restore_notes} so processed notes in {folder_bkup} will be moved back.")
            results_print(f"WARNING: This non-'empty' setting can cause some notes to never be backed up.")
            restore_result = move_processed_notes(folder_bkup, folder_source, bkup_count, notes_account, create=False)

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


def update_yaml_config_multi(file_path, updates):
    """
    Updates multiple key-value pairs in a YAML config file in a single read+write
    cycle, preserving comments and formatting. Used to flush per-run usage counter
    updates atomically (R10) instead of one yaml round-trip per key.

    Args:
        file_path (str): Path to the YAML configuration file
        updates (dict): Mapping of {key: new_value} pairs to apply. An empty dict
            is a no-op (the file isn't touched).
    """
    if not updates:
        return
    yaml_handler = YAML()
    yaml_handler.preserve_quotes = True
    yaml_handler.width = 4096

    with open(file_path, 'r') as file:
        config = yaml_handler.load(file)

    for key, value in updates.items():
        config[key] = value

    with open(file_path, 'w') as file:
        yaml_handler.dump(config, file)


## PRINT OPTIONS
def debug_print(*args, **kwargs):
    if PRINT_LEVEL.value >= PrintLevel.DEBUG.value:
        print("DEBUG:", *args, **kwargs)

def results_print(*args, **kwargs):
    if PRINT_LEVEL.value >= PrintLevel.RESULTS.value:
        print("RESULT:", *args, **kwargs)


def setup_logging():
    """Configure the gitmynotes logger (R4, incremental).

    Attaches a FileHandler to '<script_dir>/gitmynotes.log' at WARNING level.
    Uses append mode (default) so each run extends the same file -- no size-
    based rotation in this pass; can swap in RotatingFileHandler later if the
    file grows uncomfortably. Format includes a timestamp and level so non-
    interactive consumers (Cowork routines, post-mortem inspection) can parse
    the file without dealing with ANSI codes from the TTY-oriented prints.

    Idempotent: skips re-adding the handler if a FileHandler already points at
    the same path (defensive against any future re-entry into main()).
    """
    log_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "gitmynotes.log",
    )

    for existing in logger.handlers:
        if (isinstance(existing, logging.FileHandler)
                and getattr(existing, "baseFilename", None) == log_path):
            return

    handler = logging.FileHandler(log_path)
    handler.setLevel(logging.WARNING)
    handler.setFormatter(logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))
    logger.addHandler(handler)
    logger.setLevel(logging.WARNING)




def build_initial_msg(this_msg=None, folder=None, max_notes=None, export_path=None, github_url=None, print_level=None, local_only=None):
    # get some values for an initial msg
    
    if this_msg:
        initial_msg = f'''{this_msg}
'''    
    else:
        initial_msg = f'''    Welcome, 'tis a good day to GitMyNotes

    NOTE: locked notes unlocked in this Notes.app session export as cleartext.
    Close them before running if that's not what you want. (See README.)

'''
    if folder:
        initial_msg += f'''    - Notes folder: {folder}
'''
    if print_level:
        initial_msg += f'''    - print-level: {print_level}
'''
    if max_notes:
        initial_msg += f'''    - max-notes: {max_notes}
'''
    if export_path:
        initial_msg += f'''    - Export to: {export_path}
'''
    if local_only:
        initial_msg += f'''    - Local Only option set via '--local'. 
        DO NOT SEND TO:
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
        final_msg += f'''    - Tell your friends, learn more: https://GitMyNotes.com/
    
'''
    
    return final_msg




##### Describe this function

def main():

    # R4 (incremental): wire up the file logger first so any subsequent
    # warning- / error-level event in this run lands in <script_dir>/gitmynotes.log
    # alongside the existing colored TTY prints. Hardcoded log location for now;
    # CLI override can be added later if needed.
    setup_logging()

    ######## ----  Get DEFAULT_& vars from config file     ---- #######
    DEFAULT_NOTES_FOLDER_FORCE = None ##special case not in config file because... reasons.
    DEFAULT_LOCAL_ONLY = None ##special case not in config file to turn OFF sending to github
    
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
    DEFAULT_CURRENTNOTE_FILE = cfg['DEFAULT_CURRENTNOTE_FILE']
    # B9: resolve DEFAULT_CURRENTNOTE_FILE to an absolute path so AppleScript's
    # shell (osascript cwd is usually $HOME) and Python (cwd = wherever the user
    # invoked the script) agree on where the side-channel file lives. If the
    # config value is already absolute, respect it; otherwise anchor to the
    # directory containing this script, which keeps the existing .gitignore
    # entry valid and keeps the file inspectable while debugging.
    if not os.path.isabs(DEFAULT_CURRENTNOTE_FILE):
        DEFAULT_CURRENTNOTE_FILE = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            DEFAULT_CURRENTNOTE_FILE,
        )
    # Read PRINT_LEVEL from config; default to 'ALL' if missing. CLI '--print' can override.
    cfg_print_level = cfg.get('PRINT_LEVEL', 'ALL')

    # R6: macOS Notes account name. cfg.get fallback covers users who upgrade
    # without updating their yaml. CLI --notes-account overrides per-run.
    DEFAULT_NOTES_ACCOUNT = cfg.get('DEFAULT_NOTES_ACCOUNT', 'iCloud')
    
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

    parser.add_argument('--yes', '--non-interactive', action='store_true',
                      default=False,
                      help=f"[bool] Use as '--yes' or '--non-interactive' (no value allowed) for scheduled / non-terminal runs (cron, Cowork routines, CI). Implies '--force' (skips the 5x-batch confirmation) and also fails fast with a clear error if 'DEFAULT_GITHUB_URL' still contains the '<ChangeMe>' placeholder, instead of hanging on the interactive setup prompt. (default: interactive prompting is allowed)")

    parser.add_argument('--local-only', action='store_true',
                      default=DEFAULT_LOCAL_ONLY,
                      help=f"[bool] Use as '--local-only' (no 'true' or 'false' value allowed) to over-ride to the default action of backing up notes to GitHub. When set, only a local copy of notes will be made. (DEFAULT: Send notes to GitHub repo)")                      

    parser.add_argument('--max-notes', '--maxnotes', '--max', type=int, 
                      help=f'[int] Maximum number of notes to process.')

    parser.add_argument('--batch-size', type=int,
                      default=DEFAULT_BATCH_SIZE,
                      help=f'[int] The number of notes to convert, and git add/commit/push per loop, calculated a max-notes/batch-size. Especially useful for initial runs.(default: {DEFAULT_BATCH_SIZE})')  

    parser.add_argument('--print', '--print-level', type=str,
                      default=cfg_print_level,
                      help=f"[str] Optional set to 'none', 'results', 'debug', 'all' for different in tracking code flow and general debugging. (default from config: '{cfg_print_level}')")
                      
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

    parser.add_argument('--restore-notes','--restorenotes', '--restore', type=str,
                      default=DEFAULT_RESTORE_NOTES,
                      help=f"[str] Options: 'empty' or 'always' or 'never'. Determines when to move notes from '<folder>___GitMyNotes' back to their original source folder. The option 'empty' will not restore notes until notecount is 0 in source folder, while 'always' will restore at the end of each GitMyNotes run. Set to 'never' to never move notes back to source folder. (default: 'empty') ")

    parser.add_argument('--notes-account', '--notesaccount', type=str,
                      default=DEFAULT_NOTES_ACCOUNT,
                      help=f"[str] macOS Notes account name (e.g. 'iCloud', 'On My Mac'). Used to scope every AppleScript op to a single account. Most users want 'iCloud'. (default from config: '{DEFAULT_NOTES_ACCOUNT}')")



    args = parser.parse_args()

    # B8: --yes / --non-interactive implies --force so the existing 5x-batch
    # confirmation handler takes its skip-the-prompt branch automatically. The
    # --ChangeMe fail-fast below keys off args.yes separately.
    if args.yes:
        args.force = True

    ## Set up vars to use later
    args_max_notes = args.max_notes
    args_folder = args.folder
    args_wrapper_dir = DEFAULT_NOTES_WRAPPERDIR

    # B10: guard against folder==None / empty-string. Multi-folder "export all"
    # mode was advertised in the top-of-file docstring and help text but has
    # never actually worked end-to-end -- get_foldernotecount(None) returns None
    # and the next comparison throws TypeError, and multiple downstream paths
    # (audit file naming, __GitMyNotes folder creation, USAGE tracking) assume
    # a real folder name. Rather than leave a broken path silently present,
    # fail fast with a clear remediation. A proper multi-folder implementation
    # is tracked as a future feature (see R17 in gmn_bugs_and_rough_edges.md).
    if not args_folder:
        logger.error(
            "Refusing to run: no folder specified. Pass --folder <name> or set DEFAULT_NOTES_FOLDER in gmn_config.yaml. (B10 guard.)"
        )
        print_color(
            textcolor="red",
            msg=(
                "ERROR: GitMyNotes requires an explicit folder to back up. Multi-folder 'export all' mode is not currently supported.\n"
                "    Please either pass '--folder <folderName>' on the command line, or set\n"
                "    'DEFAULT_NOTES_FOLDER' in 'gmn_config.yaml' to a real folder name.\n"
                "    (Tracked as a future feature.)"
            ),
            addseparator=True,
        )
        sys.exit(1)

    audit_file = f"./{args_folder}{DEFAULT_AUDIT_FILE_ENDING}"
    args_local_only = args.local_only

    ## Apply --print (or its config default) to the module-level PRINT_LEVEL
    ## so debug_print() and results_print() honor it for the rest of this run.
    global PRINT_LEVEL
    try:
        PRINT_LEVEL = PrintLevel[str(args.print).upper()]
    except (KeyError, AttributeError):
        logger.warning(f"Invalid --print value '{args.print}'. Falling back to ALL.")
        print_color(textcolor="red", msg=f"WARNING: Invalid --print value '{args.print}'. Falling back to ALL.")
        PRINT_LEVEL = PrintLevel.ALL


    ## set up the initial msg to let people know setup details
    initial_msg = build_initial_msg(this_msg="", folder=args_folder, max_notes=args_max_notes, export_path=args.export_path, github_url=args.github_url, print_level=PRINT_LEVEL, local_only=args_local_only)
    print_color(textcolor='cyan', msg=f"{initial_msg}", addseparator=True)


    ######## ----  Do INIT work, ensure DEFAULT_GITHUB_URL has been changed    ---- #######    
    if USAGE_GITMYNOTES_TOTAL == 0:
        # leave this here for later 1st timer things
#         print("Hello first timer!")
        if len(USAGE_FOLDERS_PROCESSED) == 1:
            if USAGE_FOLDERS_PROCESSED[0] == 'placeholder':
                 USAGE_FOLDERS_PROCESSED[0] = args_folder
                 update_yaml_config('./gmn_config.yaml', 'USAGE_FOLDERS_PROCESSED', USAGE_FOLDERS_PROCESSED)
        results_print(f"USAGE_FOLDERS_PROCESSED : {USAGE_FOLDERS_PROCESSED}")
#         sys.exit(1)
    
    substring = '<ChangeMe>'
    if substring in DEFAULT_GITHUB_URL:
        changeme_msg = "WHOA, the 'DEFAULT_GITHUB_URL' setting in 'gmn.config.yaml' has not been updated to your Github username"
        logger.warning("DEFAULT_GITHUB_URL still contains '<ChangeMe>' placeholder; will prompt for setup unless --yes is set.")
        print_color(textcolor="magenta", msg=f"{changeme_msg}")

        # B8: in non-interactive mode we cannot prompt -- fail fast with a clear
        # remediation so a scheduled/cron/Cowork-routine run sees a nonzero exit
        # instead of hanging on input() forever.
        if args.yes:
            logger.error(
                "Refusing to run in non-interactive mode: DEFAULT_GITHUB_URL still contains '<ChangeMe>'. "
                "Update gmn_config.yaml before re-running with --yes. (B8 fail-fast.)"
            )
            print_color(
                textcolor="red",
                msg=(
                    "Cannot prompt for GitHub username: '--yes' / '--non-interactive' is set.\n"
                    "    Edit 'gmn_config.yaml' and change 'DEFAULT_GITHUB_URL' from the '<ChangeMe>'\n"
                    "    placeholder to your real GitHub repo URL, e.g.:\n"
                    "        'DEFAULT_GITHUB_URL': 'https://github.com/<yourname>/gitmynotes'\n"
                    "    Then re-run. Exiting."
                ),
                addseparator=True,
            )
            sys.exit(1)

        usage_github_username = input("Please enter your GitHub username: ")
        print(f"The 'DEFAULT_GITHUB_URL' will be updated to 'https://github.com/{usage_github_username}/gitmynotes'")
        ## now update the yaml file
        update_yaml_config('gmn_config.yaml', 'DEFAULT_GITHUB_URL', f"https://github.com/{usage_github_username}/gitmynotes")
        cfg = load_configs_from_file()
        DEFAULT_GITHUB_URL = cfg['DEFAULT_GITHUB_URL']


        ## RE-DO the initial msg to let people know setup details have changed
        initial_msg = build_initial_msg(this_msg="", folder=args_folder, max_notes=args_max_notes, export_path=args.export_path, github_url=args.github_url, print_level=PRINT_LEVEL, local_only=args_local_only)
        print_color(textcolor='cyan', msg=f"{initial_msg}", addseparator=True)



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
    args_folder_count = get_foldernotecount(args_folder, args.notes_account)
    if args_max_notes:
        if args_max_notes > args_folder_count:
            notes_to_process = args_folder_count
        else:
            notes_to_process = args_max_notes
    else:
        notes_to_process = args_folder_count
    
    if notes_to_process > (args.batch_size * DEFAULT_LOOPCOUNT_BEFORE_CONFIRM):
        if args.force:
            print(f"In the original command --force was set, continuing without confirm...")
            pass
        else:
            confirm_warn = f'''WHOA. {notes_to_process} notes to process in '{args_folder}' folder!

    <<<< Confirmation Required.>>>>

Add '--force' to skip confirmation in the future.'''
            logger.warning(
                f"Large batch confirmation triggered: {notes_to_process} notes in '{args_folder}' "
                f"(>{args.batch_size}*{DEFAULT_LOOPCOUNT_BEFORE_CONFIRM}). Awaiting interactive confirmation."
            )
            print_color(textcolor='magenta', msg=f"{confirm_warn}", addseparator=True)
            confirm_msg = f'''Please input:
  a number up to {notes_to_process} of notes to process, 
  or 'x' to eXit
  [Or 'enter' to process all {notes_to_process} notes] : '''
            
            confirm_num = input(f"{confirm_msg}") or f"{notes_to_process}"
            if confirm_num == 'x' or confirm_num == '0': 
                print_color(textcolor='red', msg="    Exiting GitMyNotes...", addseparator=True)
                sys.exit(1)
            confirm_num = int(confirm_num)
            if confirm_num > notes_to_process:
                confirm_num = notes_to_process 
            debug_print(f"aa Notes to process: {confirm_num}")
            notes_to_process = confirm_num
            
    else:
        pass
    ######## ----  END check for 5x batch size in arg.folder    ---- #######
    
    
    ''' Process in a loop of batches'''
    loop_count = math.ceil(notes_to_process / args.batch_size)
    
    debug_print("IN MAIN")
    debug_print(f"notes_to_process {notes_to_process}")
    debug_print(f"args.batch_size {args.batch_size}")
    
    if notes_to_process == args.batch_size:
        final_loop_size = args.batch_size
    else:
        final_loop_size = notes_to_process % args.batch_size
        if final_loop_size == 0:
            final_loop_size = args.batch_size
        
    debug_print(f"final_loop_size {final_loop_size}")
    
    
    notes_processed = 0
    processednotes_data = 0
    # Pre-init _NEW vars so the final_msg's usage_totals still has values
    # even when loop_count==0 (previously raised NameError at final_msg).
    # Also unblocks B6: USAGE_GITMYNOTES_TOTAL is now incremented once after
    # the loop instead of on every batch.
    USAGE_GITMYNOTES_TOTAL_NEW = int(USAGE_GITMYNOTES_TOTAL)
    USAGE_NOTES_PROCESSED_NEW = int(USAGE_NOTES_PROCESSED)
    # R10: hoist the loop-invariant folder-tracking out of the batch loop. Mark
    # USAGE_FOLDERS_PROCESSED dirty here if this is the first time we've seen
    # this folder; the actual yaml write happens once at end of run alongside
    # the other usage counters via update_yaml_config_multi.
    folders_dirty = False
    if args_folder not in USAGE_FOLDERS_PROCESSED:
        USAGE_FOLDERS_PROCESSED.append(args_folder)
        folders_dirty = True
    for x in range(1,loop_count+1):
        print_color(textcolor="cyan",msg=f"    Begin export of Notes with batch {x} of {loop_count}", addseparator=True)
        
        
        if loop_count == 1:
            notes_to_export = notes_to_process
        if x < loop_count:
            notes_to_export = args.batch_size
        if x == loop_count:
            notes_to_export = final_loop_size
        print(f"batch size for this loop: {notes_to_export}")
        
        if notes_to_export > 0:
            notes_processed = export_notes_to_markdown(
                DEFAULT_CURRENTNOTE_FILE,
                args.export_path,
                args.notes_account,
                args_folder,
                notes_to_export,
                args_wrapper_dir
            )
        
        if notes_processed > 0:
            print_color(textcolor="green",msg=f"SUCCESS: Exported {notes_processed} Notes to local folder {args.export_path}")
            
            
            ## SEND TO GITHUB BY DEFAULT, UNLESS 'LOCAL' OPTION SET TRUE
            if args_local_only:
                print_color(textcolor="magenta",msg=f"The --local-only flag is set. No notes sent to Github",addseparator=True)
            else:
                git_add_commit_push(args.export_path, args_folder, args_wrapper_dir)
            
        else:
            logger.warning(f"No notes were processed in batch {x}/{loop_count} for folder '{args_folder}'; skipping git commit.")
            print_color(textcolor="magenta",msg=f"No notes were processed, skipping git commit")
            
        ## if notes were process to git, then create the audit trail and move the notes
        if notes_processed > 0:
            debug_print(f"NOTES PROCESSED > 0: {notes_processed}")
            print_color(textcolor="white",msg=f"Notes to export to markdown: {notes_processed}")
            debug_print(f'''BEFORE export:
output_file={audit_file}
folder={args_folder}
max_notes={notes_processed}
newline_delimiter={args.newline_delimiter}''')

            processednotes_data = export_notes_metadata(
                output_file=audit_file,
                folder=args_folder,
                max_notes=notes_processed,
                newline_delimiter=args.newline_delimiter,
                notes_account=args.notes_account
            )
            
        if processednotes_data:
            # Use notes_processed (actual exported count) not notes_to_export (intended
            # batch size). After B1, these can differ when an unsupported note aborts a
            # batch early -- passing notes_to_export would move too many notes from the
            # source folder, including ones that were never exported (a zombie-move).
            move_result = move_processed_notes(
                folder_source=args_folder,
                folder_dest=f"{args_folder}{DEFAULT_PROCESSED_FOLDER_ENDING}",
                max_notes=notes_processed,
                notes_account=args.notes_account,
                create=True
            )
        else:
            move_result = 0
            print_color(textcolor="magenta",msg=f"No Notes to Move")
        
        if move_result:
            print_color(textcolor="green",msg=f"SUCCESS: Moved notes to Notes folder: '{args_folder}{DEFAULT_PROCESSED_FOLDER_ENDING}'", addseparator=True)
        else:
            logger.error(
                f"Failed to move processed notes from '{args_folder}' to "
                f"'{args_folder}{DEFAULT_PROCESSED_FOLDER_ENDING}' (batch {x}/{loop_count})."
            )
            print_color(textcolor="red",msg=f"    !!! FAILED to MOVE notes !!!", addseparator=True)

        
        ######## ----  update usage counts (in-memory; flushed once at end of run, R10)  ---- #######
        # B6 + R10: per-batch yaml writes for USAGE_NOTES_PROCESSED and
        # USAGE_FOLDERS_PROCESSED are gone. Accumulate in memory here, flush
        # once after the loop via update_yaml_config_multi.

        results_print(f"++++++++++  Update config yaml usage stats  +++++++++++++")
        debug_print(f"(before)USAGE_NOTES_PROCESSED: {USAGE_NOTES_PROCESSED}")
        debug_print(f"notes_processed: {notes_processed}")

        USAGE_NOTES_PROCESSED_NEW = int(USAGE_NOTES_PROCESSED) + int(notes_processed)
        debug_print(f"USAGE_NOTES_PROCESSED_NEW: {USAGE_NOTES_PROCESSED_NEW}")
        USAGE_NOTES_PROCESSED = USAGE_NOTES_PROCESSED_NEW
        debug_print(f"(after)USAGE_NOTES_PROCESSED: {USAGE_NOTES_PROCESSED}")
        debug_print(f"++++++++++++++++++++++++++++++++++++++++++++++")

    # B6 + R10: increment run counter and flush all usage counters in a single
    # yaml write per run (vs N+1 writes per N-batch run before). Guarded on
    # loop_count > 0 so a nothing-to-do run doesn't bump the counter or touch
    # the yaml at all.
    if loop_count > 0:
        USAGE_GITMYNOTES_TOTAL_NEW = int(USAGE_GITMYNOTES_TOTAL) + 1
        usage_updates = {
            'USAGE_GITMYNOTES_TOTAL': USAGE_GITMYNOTES_TOTAL_NEW,
            'USAGE_NOTES_PROCESSED': USAGE_NOTES_PROCESSED_NEW,
        }
        if folders_dirty:
            usage_updates['USAGE_FOLDERS_PROCESSED'] = USAGE_FOLDERS_PROCESSED
        update_yaml_config_multi('./gmn_config.yaml', usage_updates)

    if processednotes_data:
        
        ## check for restore-empty-source-folder to decide what to do with contents of folder_GitMyNotes backup folders
        debug_print(f"Option --restore-notes is '{args.restore_notes}'")
        
        restore_result = 0
        restore_result = restore_source_foldernote(folder_source=args_folder, folder_bkup=f"{args_folder}{DEFAULT_PROCESSED_FOLDER_ENDING}", restore_notes=args.restore_notes, notes_account=args.notes_account)
            
        if restore_result:
            print_color(textcolor="green",msg=f"SUCCESS: RESTORED notes to {args_folder} from {args_folder}{DEFAULT_PROCESSED_FOLDER_ENDING}", addseparator=True)
        
        else:
            restore_declined_msg = f'''    << Notes not restored to '{args_folder}' >> 
        Set --restore-notes=empty to move notes back to '{args_folder}' when notecount is 0
        Set --restore-notes=always to move notes back to '{args_folder}' after every backup'''
            print_color(textcolor="red",msg=f"{restore_declined_msg}", addseparator=True)
    
    ######## ----  Prep for final msg so user knows what happened    ---- #######
    if args_wrapper_dir:
        final_gitnotes_url = f"{DEFAULT_GITHUB_URL}/tree/main/{args_wrapper_dir}/{args_folder}"
    else:
        final_gitnotes_url = f"{DEFAULT_GITHUB_URL}/tree/main/{args_folder}"
    
    usage_totals = [int(USAGE_GITMYNOTES_TOTAL_NEW), len(USAGE_FOLDERS_PROCESSED), int(USAGE_NOTES_PROCESSED_NEW)]
    
    share_url = "Get More with GitMyNotes Pro: https://GitMyNotes.com"
    
    final_msg = build_final_msg(gitnotes_url=f"{final_gitnotes_url}", audit_file=f"{audit_file}", usage_totals = usage_totals, share_url=f"{share_url}")
    
    print_color(textcolor="cyan",msg=f"{final_msg}", addseparator=True)
    
    
    
    
    
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
  
  
  
  
def print_color(textcolor='white', msg=None, addseparator=False, textdefault='white', bkcolor=None):
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