# GitNotes
## GitNotes adds convenient version control, off-site backups, and optional collaboration to your macOS Notes.

A lightweight macOS utility using Python and AppleScript to sync your macOS Notes to your public or private GitHub repos, the GitNotes solution exports Notes to Markdown while preserving folder organization and formatting. It features out-of-the-box common sense defaults or user-driven customization, a local audit trail with checkpoint features for interrupted backups, and secure GitHub integration. All processing happens on your machine, with the only external data transmission secured by your enterprise-grade GitHub authentication credentials.


# GitNotes is for me?

`writers gonna write`
Transform your macOS Notes into a version-controlled writer's archive on GitHub.
Preserve your gems and most excellent lines, and track the full evolution of your work. Maintain a complete history of every change and trace back your ideas from current state and previous alternatives -- with every revision safely tracked and recoverable. Learn how to GitHub and branch and fork to explore your ideas, in trusted collabs, or on your own.


`IT team gotta keep copies`
Concerned about a fleet of macbooks, and all the useful, non-shareable, and non-collaborative notes just one cup of coffee away from disaster? 


`prepared tech workers win`
No one can predict the future. Losing a job or a role shouldn't mean losing your personal macOS Notes as well. Set up a free GitHub repo and back up the folders that hold your personal notes.


## Usage
`python gitnotes.py --folder='<notesFolderName>' --max-notes=<N>`


#### Output Artifacts
-- Locally --

1. New Notes folder: `<notesFolderName>_GitNotes` to store processed notes
2. New GitNotes audit file: `<notesFolderName>.csv` to track processed notes
3. Markdown copy of Notes from folder: `DEFAULT_EXPORT_PATH/<a-note.md>`

-- Remote --
1. New GitHub directory: `DEFAULT_GITHUB_URL/DEFAULT_NOTES_OUTERDIR`
2. New Github sub-dir mapped to Notes folders: `DEFAULT_GITHUB_URL/DEFAULT_NOTES_OUTERDIR/<notesFolderName>`
3. Github copy of Notes from folder: `DEFAULT_GITHUB_URL/DEFAULT_NOTES_OUTERDIR/<notesFolderName>/<a-note.md>`
4. OPTIONAL - GitNotes audit file: `<notesFolderName>.csv`




## Getting Started

### Prerequisites
1. MacOS with Notes app and AppleScript (ships with every Mac)
2. Python 3.x+ (available here `linkTBD`)
3. GitHub repo accessible from the Mac running this script (public or private, configured auth credentials, etc) 


## Steps
1. clone the repo: `git clone https://github.com/mariochampion/gitnotes.git`

2. cd into gitnotes dir: `cd gitnotes`

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



## to do
* write real instructions

* there is some issue with loops and passing batch not original maxnotes, also when initial maxnotes 
greater than batchnotes AND greater than folder notecount there is BUG!

* allow optionally `git push` the audit file as well

* do some error catching (bad names, non numbers in maxnotes, etc)

* allow user to decide to keep <folder>__GitNotes bkup or move back to original

* add colors!

* create config file?

* PRO? 

* allow comma separated list of folders at once

* pre-map some folders to some github repos

* add DEFAULT folder name so doesnt try to do ALL NOTES?? if none specified?

* help set up cron job?






