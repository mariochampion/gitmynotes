# GitNotes
Use GitHub to hold, backup, track revisions of your macOS Notes.

A lightweight macOS utility using Python and AppleScript to sync your Apple Notes to GitHub, combining local backup with version control. This tool exports Notes to Markdown while preserving folder organization and formatting. It features incremental backup support, local audit logging, and secure GitHub integration. All processing happens on your machine, with GitHub as the only external service, ensuring complete data privacy through your own repository credentials.



## to do
* write real instructions

* create config file

* use min of maxnotes and count of notes

* do some error catching (bad names, non numbers in maxnotes, etc)

* add image capability

* add colors!

* allow comma separated list of folders at once

* incorporate some values by env var instead of config

* allow user to decide to keep <folder>__GitNotes bkup or move back to original

* add DEFAULT folder name so doesnt try to do ALL NOTES?? if none specified


# GitNotes Benefits 

By automatically mirroring your macOS Notes to GitHub, you gain the power of version control, collaborative possibilities, and bulletproof backup – all while continuing to use the familiar Notes app. With secure GitHub authentication and local processing, your data privacy is guaranteed.

Transform your macOS Notes into a version-controlled writer's archive on GitHub.
This Python/AppleScript utility preserves the evolution of your writing by automatically backing up Notes to Markdown files, maintaining a complete history of every change. Watch your ideas grow from initial concepts to fully developed pieces, with every revision safely tracked and recoverable. Features folder organization matching your Notes structure, local audit logging, and secure GitHub integration - all processing happens on your machine, using only your GitHub credentials for repository access.



## Usage
`python gitnotes.py --folder='<notesFolderName>' --max-notes=<N>`


## Getting Started

### Prerequisites
1. MacOS Notes app
2. Python 3.x+
3. Applescript (should be on all Macs)
4. GitHub repo accessible from the Mac running this script (configured auth credentials, etc) 


## Steps
1. clone the repo: `git clone https://github.com/mariochampion/gitnotes.git`

2. cd into notesdump dir: `cd gitnotes`

3. in file `gitnotes.py`, set required and optional configurations, or leave as shipped with these common sense defaults

	-- REQUIRED TO CHANGE--
	
	
	set `DEFAULT_EXPORT_PATH` to the export location (example: `DEFAULT_EXPORT_PATH = "~/Documents/<SomeFolder>"`)
	
	set `DEFAULT_GITHUB_URL` to the the repo where you want to store Notes (example: `DEFAULT_GITHUB_URL = "https://github.com/<myusername>/<myrepo>""`)
	

	-- REQUIRED: LEAVE AS-IS or CHANGE--

	`DEFAULT_PROCESSED_FOLDER_ENDING = "__GitNotes"`

	`DEFAULT_CSV_NAME = "GitNotes.csv"`

	`DEFAULT_NEWLINE_DELIMITER = "|||"`

	`DEFAULT_MAX_NOTES = 10`
	

    -- OPTIONAL --
    
    
	set `DEFAULT_NOTES_OUTERDIR` to the 'wrapper' dir for folders (example: `DEFAULT_NOTES_OUTERDIR = "macosnotes"`)
	
	set `DEFAULT_BATCH_SIZE` to run loops to reach --max-notes value (example: `DEFAULT_BATCH_SIZE = 10`)
	
	set `DEFAULT_IGNORE_FOLDER` to Notes folder to not backup to GitHub (example: `DEFAULT_IGNORE_FOLDER = "ignore"`)
	
	
	

4. run Ex: `python gitnotes.py --folder='<notesFolderName>' --max-notes <N> `

```
Export Apple MacOS Notes and folders to GitHub repo and folders

usage: gitnotes.py [-h] [--folder FOLDER] [--max-notes MAX_NOTES] [--batch-size BATCH_SIZE]
                   [--export-path EXPORT_PATH] [--github-url GITHUB_URL] [--wrapper-dir WRAPPER_DIR]
                   [--ignore-folder IGNORE_FOLDER] [--output-file OUTPUT_FILE] [--newline-delimiter NEWLINE_DELIMITER]


options:
  -h, --help            show this help message and exit
  --folder FOLDER       Specific Notes folder to export. (default: all folders)
  
  --max-notes MAX_NOTES
                        Maximum number of notes to process. (default: all notes)
  
  --batch-size BATCH_SIZE
                        The number of notes to convert, and git add/commit/push per loop. Especially useful for
                        initial GitNotes runs.(default: 10)
  
  --export-path EXPORT_PATH
                        Path to export the notes (default: ~/Documents/gitnotes)
  
  --github-url GITHUB_URL
                        GitHub repository URL. (default: https://github.com/mariochampion/gitnotes)
  
  --wrapper-dir WRAPPER_DIR
                        Outer directory to hold folders. (default: macosnotes)
  
  --ignore-folder IGNORE_FOLDER
                        The Notes folder to ignore and not process. (default: ignore)
  
  --output-file OUTPUT_FILE
                        Output CSV file path (default: <folder>.csv)
  
  --newline-delimiter NEWLINE_DELIMITER
                        Default CSV newline delimiter (default: |||)

```







