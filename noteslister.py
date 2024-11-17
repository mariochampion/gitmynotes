###### how to use

## Export up to 10 notes from a specific folder
#  python notes-export.py --folder-name="somefolder" --max-notes=10

## Export all notes from a specific folder
#  python notes-export.py --folder-name="somefolder"

## Export up to 10 notes from all folders
#. python notes-export.py --max-notes=10

## Specify a custom output file
#  python notes-export.py --folder-name="somefolder" --max-notes=10 --output-file="my_notes.csv"



import csv
import subprocess
from datetime import datetime
import os
import argparse

DEFAULT_CSV_NAME = "notes_export.csv"
DEFAULT_NEWLINE_DELIMITER = "|||"


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
    print(f"newline_delimiter {newline_delimiter}")
    
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
        if targetFolder is null then
            return "Folder not found"
        end if
        '''
    else:
        output_file = f"DEFAULT_CSV_NAME"
        applescript += '''
        set theNotes to notes
        '''
        
    if max_notes:
        applescript += '''
        set theNotes to notes of targetFolder
        '''
    else:
        applescript += '''
        set theNotes to notes of targetFolder
        '''        
    
    applescript += '''
        repeat with theNote in theNotes
            set noteData to name of theNote as string &","& quoted form of (name of theNote as string) &","& modification date of theNote & custom_delimiter
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
        
        print(f"process.stdout {stdout}")
        
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
            print(f"line is:{line}")
            
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
                writer.writerow(['Folder', 'Title', 'Quoted Title', 'Last Modified'])
            #print(f"notes_data {notes_data}")
            writer.writerows(notes_data)
            
        print(f"Successfully exported {len(notes_data)} notes to {output_file}")
        
    except Exception as e:
        print(f"Error exporting notes: {str(e)}")



def main():
    parser = argparse.ArgumentParser(description='Export metadata from macOS Notes app')
    parser.add_argument('--folder-name', type=str, help='Name of the folder to export notes from')
    
    parser.add_argument('--max-notes', type=int, help='Maximum number of notes to export')
    
    parser.add_argument('--output-file', type=str, 
    					default=DEFAULT_CSV_NAME,
                        help=f'Output CSV file path (default: {DEFAULT_CSV_NAME})')
                        
    parser.add_argument('--newline-delimiter', type=str, 
    					default=DEFAULT_NEWLINE_DELIMITER,
                        help=f'Default CSV newline delimiter (default: {DEFAULT_NEWLINE_DELIMITER})')
    
    args = parser.parse_args()
    
    export_notes_metadata(
        output_file=args.output_file,
        folder_name=args.folder_name,
        max_notes=args.max_notes,
        newline_delimiter=args.newline_delimiter
    )

if __name__ == '__main__':
    main()
    
    
    