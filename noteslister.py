###### how to use

## Export up to 10 notes from a specific folder
#  python notes-export.py --folder-name="somefolder" --max-notes=10

## Export all notes from a specific folder
#  python notes-export.py --folder-name="somefolder"

## Export up to 10 notes from all folders
#. python notes-export.py --max-notes=10

## Specify a custom output file
#  python notes-export.py --folder-name="somefolder" --max-notes=10 --output-file="my_notes.csv"

## Todo: 
#  allow passng of comma separated list of folders to process, each onbe worked through to max notes
#  move the processnotes to <folder_name>__GitNotes so that the bacthing can be non-duplicate notes, rather than check them

#. combine all .pys into one .py


import csv
import subprocess
from datetime import datetime
import os
import argparse
from typing import Tuple

DEFAULT_CSV_NAME = "notes_export.csv"
DEFAULT_NEWLINE_DELIMITER = "|||"
DEFAULT_PROCESSED_FOLDER_ENDING = "__GitNotes"
DEFAULT_MAX_NOTES = 10


def export_notes_metadata(output_file=None, folder_name=None, max_notes=None, newline_delimiter=f"{DEFAULT_NEWLINE_DELIMITER}"):
    """
    Export macOS Notes metadata (title, quoted title, and modification date) to a CSV file.
    
    Args:
        output_file (str): Path to the output CSV file
        folder_name (str): Name of the folder to export notes from (None for all folders)
        max_notes (int): Maximum number of notes to export (None for all notes)
        newline_delimiter (str): Default newline delimiter (|||)
    """
    # AppleScript to get notes information
    #print(f"newline_delimiter {newline_delimiter}")
    
    applescript = '''
    tell application "Notes"
        set noteList to {}
        '''
    
    applescript += f'''
    set custom_delimiter to "{newline_delimiter}"
    '''
    
    if folder_name:
        output_file = f"{folder_name}.csv"
        applescript += f'''
        set targetFolder to null
        repeat with f in folders
            if (name of f as string) is "{folder_name}" then
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
        output_file = f"DEFAULT_CSV_NAME"
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
    
    try:
        # Execute AppleScript and get the output
        process = subprocess.Popen(['osascript', '-e', applescript],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        
        #print(f"process.stdout {stdout}")
        
        if stderr:
            raise Exception(f"AppleScript error: {stderr.decode('utf-8')}")
        
        stdout_str = stdout.decode('utf-8').strip()
        if stdout_str == "Folder not found":
            raise Exception(f"Folder '{folder_name}' not found in Notes app")
            
        # Parse the output
        notes_data = []
        raw_output = stdout_str.split(f"{DEFAULT_NEWLINE_DELIMITER}")
        raw_output = raw_output[:-1]
        
        for line in raw_output:
            
            line = line.rstrip(",")
            #print(f"line is:{line}")
            
            #Remove outer parentheses and split by commas
            if line.startswith(','): line = line[1:]
            if line.endswith(','): line = line[:-1]

            line_items = line.split(',',2)
            title = line_items[0].strip()
            #print(f"title : {title}")
            
            quoted_title = line_items[1].strip()
            #print(f"quoted_title : {quoted_title}")
            
            mod_date = line_items[2].strip()
            #print(f"mod_date : {mod_date}")

            
            # Convert date string to datetime object and format it
            try:
                date_obj = datetime.strptime(mod_date, '%Y-%m-%d %H:%M:%S +0000')
                formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                formatted_date = mod_date
            
            print(f"APPENDING: {folder_name}, {title}, {quoted_title}, {formatted_date} to {output_file}")
                
            notes_data.append([folder_name, title, quoted_title, formatted_date])
        
        # Apply max_notes limit if specified
        if max_notes is not None:
            notes_data = notes_data[:max_notes]
            # determine hwo many items in list, then loop thru and do writerow not writerowS
        
        # Write to CSV
        mode = 'a' if os.path.exists(output_file) else 'w'
        with open(output_file, mode, newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if mode == 'w':  # Only write header for new files
                writer.writerow(['Folder', 'Original Title', 'Exported Title', 'Last Modified'])
            #print(f"notes_data {notes_data}")
            writer.writerows(notes_data)
            
        print(f"Successfully exported {len(notes_data)} notes to {output_file}")
        
    except Exception as e:
        print(f"Error exporting notes: {str(e)}")
        
    return notes_data


def move_processed_notes(folder_source, folder_dest, processed_notes):
    ''' Move processed notes into <foldername>_GitNotes so wont process again -- until changed??'''
    print(f"folder_source: {folder_source}")
    print(f"folder_dest: {folder_dest}")
    print(f"processed_notes count: {len(processed_notes)}")
    
    
    # create_gitnotes_folder(folder_dest) so we have a place to move notes
    success, message = create_gitnotes_folder(folder_dest)
    if success:
        print(f"Success: {message}")
    else:
        print(f"Failed: {message}")
    
    
    # do the actual move



def create_gitnotes_folder(folder_name: str) -> Tuple[bool, str]:
    """
    Create a folder in macOS Notes app under iCloud account.
    
    Args:
        folder_name (str): Name of the folder to create
        
    Returns:
        Tuple[bool, str]: (success status, message/error details)
    """
    print(f"Attempting to create Notes folder: {folder_name}")
    
    # Properly escape quotes in folder name for AppleScript
    folder_name_escaped = folder_name.replace('"', '\\"')
    
    applescript = f'''
    tell application "Notes"
        try
            set targetAccount to "iCloud"
            tell account targetAccount
                if not (exists folder "{folder_name_escaped}") then
                    make new folder with properties {{name:"{folder_name_escaped}"}}
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
    
    
def process_applescript(applescript):
    try:
        result = subprocess.run(
            ['osascript', '-e', applescript],
            capture_output=True,
            text=True,
            check=True  # This will raise CalledProcessError if osascript fails
        )
        
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




def main():
    parser = argparse.ArgumentParser(description='Export metadata from macOS Notes app')
    parser.add_argument('--folder-name', type=str, help='Name of the folder of notes to export')
    
    parser.add_argument('--max-notes', type=int,
    					default=DEFAULT_MAX_NOTES,
    					 help=f'Maximum number of notes to export. (default: {DEFAULT_MAX_NOTES})')
    
    parser.add_argument('--output-file', type=str, 
    					default=DEFAULT_CSV_NAME,
                        help=f'Output CSV file path (default: <folder_name>.csv)')
                        
    parser.add_argument('--newline-delimiter', type=str, 
    					default=DEFAULT_NEWLINE_DELIMITER,
                        help=f'Default CSV newline delimiter (default: {DEFAULT_NEWLINE_DELIMITER})')
    
    args = parser.parse_args()
    
    processednotes_data = export_notes_metadata(
        output_file=args.output_file,
        folder_name=args.folder_name,
        max_notes=args.max_notes,
        newline_delimiter=args.newline_delimiter
    )
    
    print(f"================================")
    print(f"     CSV JOB COMPLETED!")
    print(f"================================")
    print(f"Notes processed")
    print(f"{processednotes_data}")        
    
    if processednotes_data:
        move_processed_notes(
            folder_source=args.folder_name,
            folder_dest=f"{args.folder_name}{DEFAULT_PROCESSED_FOLDER_ENDING}",
            processed_notes=processednotes_data
        )
    else:
        print(f"No Notes to Move")
    
    
    
    

if __name__ == '__main__':
    main()
    
    
    