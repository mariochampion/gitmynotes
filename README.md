# GitMyNotes
## GitMyNotes adds convenient version control, off-site backups, and optional collaboration to your macOS Notes.

A lightweight macOS utility using Python and AppleScript to sync your macOS Notes to your public or private GitHub repos, the GitMyNotes solution exports Notes to Markdown while preserving folder organization and formatting. It features out-of-the-box common sense defaults or user-driven customization, a local audit trail with checkpoint features for interrupted backups, and secure GitHub integration. All processing happens on your machine, with the only external data transmission secured by your enterprise-grade GitHub authentication credentials.


# GitMyNotes is for me?

Do you use Notes? Do you use GitHub? Then undoubtedly yes!

Do you use Notes and can [start with GitHub](https://docs.github.com/en/get-started/start-your-journey)? Then also yes!

`writing is re-writing`
Transform your macOS Notes into a version-controlled archive on GitHub. Preserve your most excellent lines via versions to track the full evolution of your work. Use GitMyNotes to maintain a complete history of every change and trace back your ideas from current state and previous alternatives -- with every revision safely tracked and recoverable. Learn how to GitHub and branch and fork to explore your ideas, in trusted collabs, or on your own.


`IT team gotta keep copies`
Concerned about a fleet of macbooks, and all the useful, non-shareable, and non-collaborative notes just one cup of coffee away from disaster? 


`prepared tech workers win`
No one can predict the future. Losing a job or a role shouldn't mean losing your personal macOS Notes as well. Set up a free GitHub repo and back up the folders that hold your personal notes.


## Usage
`python gitmynotes.py` or set some parameters with

`python gitmynotes.py [--folder='<notesFolderName>' --max-notes=<N>]`


#### Output Artifacts
-- Local --

1. New Notes folder: `<notesFolderName>_GitMyNotes` to store processed notes
2. New GitMyNotes audit file: `<notesFolderName>.csv` to track processed notes
3. Markdown copy of Notes from folder: `DEFAULT_EXPORT_PATH/<my-exported-note.md>`

-- Remote --
1. New GitHub directory: `DEFAULT_GITHUB_URL/DEFAULT_NOTES_OUTERDIR`
2. New Github sub-dir mapped to Notes folders: `DEFAULT_GITHUB_URL/DEFAULT_NOTES_OUTERDIR/<notesFolderName>`
3. Github copy of Notes from folder: `DEFAULT_GITHUB_URL/DEFAULT_NOTES_OUTERDIR/<notesFolderName>/<a-note.md>`
4. OPTIONAL - GitMyNotes audit file: `<notesFolderName>.csv`




## Getting Started

### Prerequisites
1. MacOS with Notes app and AppleScript (ships with every Mac)
2. Python 3.x+ with PyYaml ability (run `pip install PyYAML` once)
3. GitHub repo accessible from the Mac running this script (public or private, configured auth credentials, etc) 


## Steps
1. clone the repo: `git clone https://github.com/mariochampion/gitmynotes.git`

2. cd into gitmynotes dir: `cd gitmynotes`

3. in file `gitmynotes.py`, set required and optional configurations, or leave as shipped with these common sense defaults

	-- REQUIRED TO CHANGE--
	
	set `DEFAULT_GITHUB_URL` to the the repo where you want to store Notes (example: `DEFAULT_GITHUB_URL = "https://github.com/<myusername>/<myrepo>""`)
	

	-- REQUIRED: LEAVE AS-IS or CHANGE--

	set `DEFAULT_EXPORT_PATH` to the export location (example: `DEFAULT_EXPORT_PATH = "~/Documents/gitmynotes"`)
	
	`DEFAULT_PROCESSED_FOLDER_ENDING = "__GitMyNotes"`

	`DEFAULT_CSV_NAME = "GitMyNotes.csv"`

	`DEFAULT_NEWLINE_DELIMITER = "|||"`

	`DEFAULT_MAX_NOTES = 10`
	

    -- OPTIONAL --
    
    
	set `DEFAULT_NOTES_OUTERDIR` to the 'wrapper' dir for folders (example: `DEFAULT_NOTES_OUTERDIR = "macosnotes"`)
	
	set `DEFAULT_BATCH_SIZE` to run loops to reach --max-notes value (example: `DEFAULT_BATCH_SIZE = 10`)
	
	set `DEFAULT_IGNORE_FOLDER` to Notes folder to not backup to GitHub (example: `DEFAULT_IGNORE_FOLDER = "ignore"`)
	
	
	

4. run Ex: `python gitmynotes.py --folder='<notesFolderName>' --max-notes <N> `

```
Export Apple MacOS Notes and folders to GitHub repo and folders

usage: gitmynotes.py [-h] [--folder FOLDER] [--max-notes MAX_NOTES] [--batch-size BATCH_SIZE] [--export-path EXPORT_PATH] [--github-url GITHUB_URL]
                   [--wrapper-dir WRAPPER_DIR] [--ignore-folder IGNORE_FOLDER] [--output-file OUTPUT_FILE] [--newline-delimiter NEWLINE_DELIMITER]
                   [--audit_file_ending AUDIT_FILE_ENDING]


options:
  -h, --help            show this help message and exit
  --folder FOLDER       [str] Specific Notes folder to export.(default: 'Notes')
  --max-notes MAX_NOTES
                        [int] Maximum number of notes to process. (default: count of all notes)
  --batch-size BATCH_SIZE
                        [int] The number of notes to convert, and git add/commit/push per loop. Especially useful for initial runs.(default: 10)
  --export-path EXPORT_PATH
                        [str] Path to export the notes (default: ~/Documents/gitmynotes)
  --github-url GITHUB_URL
                        [str] GitHub repository URL. (default: https://github.com/mygitgitusername/gitmynotes)
  --wrapper-dir WRAPPER_DIR
                        [str] Outer directory to hold folders. (default: 'macosnotes')
  --ignore-folder IGNORE_FOLDER
                        [str] The Notes folder to ignore and not process. (default: 'ignore')
  --output-file OUTPUT_FILE
                        [str] Output CSV file path (default: '<folder>.csv)'
  --newline-delimiter NEWLINE_DELIMITER
                        [str] Default CSV newline delimiter (default: '|||')
  --audit-file-ending AUDIT_FILE_ENDING
                        [str] The audit file extension (default: '.csv')
  --restore-empty-source-folder EMPTY_SOURCE_FOLDER
                        [str] If 'True', do not move backup notes from '<folder>___GitMyNotes' back into '<folder>' until 0 notes remain in source <folder>. If 'False', move the notes back to source <folder> after max_notes reached, even if other notes remain un-backed-up in source <folder>. (default: 'True')

```


### copyright 2024 mariochampion all rights reserved.