# GitMyNotes
## GitMyNotes adds convenient version control, off-site backups, and optional collaboration to your macOS Notes.

A lightweight macOS utility using Python and AppleScript to sync your macOS Notes to your public or private GitHub repos, the GitMyNotes solution exports Notes to Markdown in a local directory, while preserving folder organization and formatting. It features out-of-the-box common sense defaults or user-driven customization, a local audit trail file  with checkpoint features for interrupted backups, and secure GitHub integration. All processing happens on your machine, with the only external data transmission secured by your enterprise-grade GitHub authentication credentials.


# GitMyNotes is for me?

Do you use Notes? Do you use GitHub? Then undoubtedly yes!

Do you use Notes and can [start with GitHub](https://docs.github.com/en/get-started/start-your-journey)? Then also yes!

`writing is re-writing`
Transform your macOS Notes into a version-controlled archive on GitHub. Use GitMyNotes to preserve and maintain your most excellent lines via versioning to track the full evolution of your work. Learn how to GitHub using branches and forks to explore your ideas, in trusted collabs, or on your own.


`IT team gotta keep copies`
Concerned about a fleet of macbooks, and all the useful, non-shareable, and non-collaborative notes just one cup of coffee away from disaster? Use GitMyNotes on a cronjob on every Mac to keep versioned copies of valuable Notes.


`prepared tech workers win`
No one can predict the future. Losing a job or a role shouldn't mean losing your personal macOS Notes as well. Set up a free GitHub repo and use GitMyNotes to back up the folders that hold your personal reminders, thoughts, and plans.


`but... I dont use Github (yet?)`
Simply set '--local-only' when you run the command to create, surprise, local-only backups. No GitHub required. But, really, you should [set up](https://docs.github.com/en/get-started/start-your-journey) a free GitHub repo.


## Getting Started

### Prerequisites
1. MacOS with Notes app and AppleScript (ships with every Mac)
2. Python 3.x+ with `ruyaml` ability (run `pip install ruamel.yaml` once)
3. GitHub repo (eg, `https://github.com/<MYUSERNAME>/gitmynotes`) accessible from the Mac running this script. Can be public or private, must be configured working auth credentials, etc.


## Steps 1-2-3
1. First, clone the repo: `git clone https://github.com/mariochampion/gitmynotes.git`

2. Next, `cd` into gitmynotes dir: `cd gitmynotes`

3. Then, in file `gmn_config.yaml`, set the required Github url to your Github url

	-- REQUIRED TO CHANGE--
	
	set `DEFAULT_GITHUB_URL` to the the repo where you want to store Notes.
	
	example: `'DEFAULT_GITHUB_URL': 'https://github.com/<MyUserName>/gitmynotes'`
	
	OPTIONAL: Leave as-is or change the additional `DEFAULT_*` configs the the file.
	



## Usage

That's it! Now run the script:

`python gitmynotes.py` to run against default "Notes" folder. 

Or be more specific with:

`python gitmynotes.py [--folder='<notesFolderName>' --max-notes=<N>]`

Learn more with:

`python gitmynotes.py --help`


## Cool cat usage

Set an alias in your user profile:`alias gitmynotes='python gitmynotes.py'`

Then you can run, for example `gitmynotes --folder='myPythonNotes' --maxnotes=10`

or `gitmynotes --help`


#### Output Artifacts
-- Local --

1. New Notes folder: `<notesFolderName>_GitMyNotes` to store processed notes
2. New GitMyNotes audit file: `<notesFolderName>.csv` to track processed notes
3. Markdown copy of Notes from folder: `DEFAULT_EXPORT_PATH/<my-exported-note.md>`

-- Remote --
1. New GitHub directory: `DEFAULT_GITHUB_URL/DEFAULT_NOTES_WRAPPERDIR`
2. New Github sub-dir mapped to Notes folders: `DEFAULT_GITHUB_URL/DEFAULT_NOTES_WRAPPERDIR/<notesFolderName>`
3. Github copy of Notes from folder: `DEFAULT_GITHUB_URL/DEFAULT_NOTES_WRAPPERDIR/<notesFolderName>/<a-note.md>`
4. OPTIONAL - GitMyNotes audit file: `<notesFolderName>.csv`


```
Export macOS Notes to GitHub

usage: gitmynotes.py [-h] [--folder FOLDER] [--force] [--max-notes MAX_NOTES] [--batch-size BATCH_SIZE] [--export-path EXPORT_PATH]
                     [--github-url GITHUB_URL] [--newline-delimiter NEWLINE_DELIMITER] [--audit-file-ending AUDIT_FILE_ENDING]
                     [--restore-notes RESTORE_NOTES]


options:
FREQUENTLY USED
  -h, --help            show this help message and exit
  --folder FOLDER       [str] Specific Notes folder to export.(default: 'Notes')
  --max-notes MAX_NOTES, --maxnotes MAX_NOTES
                        [int] Maximum number of notes to process.
  --restore-notes RESTORE_NOTES, --restorenotes RESTORE_NOTES, --restore RESTORE_NOTES
                        [str] Options: 'empty' or 'always' or 'never'. Determines when to move notes from '<folder>___GitMyNotes' back to their original source folder. The
                        option 'empty' will not restore notes until notecount is 0 in source folder, while 'always' will restore at the end of each GitMyNotes run.
                        Set to 'never' to never move notes back to source folder. (default: 'empty')                        
  --print PRINT, --print-level PRINT
                        [str] Optional set to 'none', 'results', 'debug', 'all' for different in tracking code flow and general debugging. (default: 'all')

                        
LESS FREQUENTLY USED                        
  --batch-size BATCH_SIZE
                        [int] The number of notes to convert, and git add/commit/push per loop, calculated a max-notes/batch-size. Especially useful for initial
                        runs.(default: 10)
  --export-path EXPORT_PATH, --exportpath EXPORT_PATH
                        [str] Path to export the notes (default: ~/Documents/gitmynotes)
  --force               [bool] Use as '--force' (no 'true' or 'false' value allowed) to over-ride to the default required user confirmation to process the full count
                        of Notes in the specified folder when it exceed 5x the batch size -- which could be hundreds of notes and could take a looooong
                        time.(default: confirmation will be required)                        
  --local-only          [bool] Use as '--local-only' (no 'true' or 'false' value allowed) to over-ride to the default action of backing up notes to GitHub. When set,
                        only a local copy of notes will be made. (DEFAULT: Send notes to GitHub repo)
  --github-url GITHUB_URL, --githuburl GITHUB_URL
                        [str] GitHub repository URL. (default: https://github.com/mariochampion/gitmynotes)
  --newline-delimiter NEWLINE_DELIMITER, --newlinedelimiter NEWLINE_DELIMITER
                        [str] Default CSV newline delimiter (default: '|||')
  --audit-file-ending AUDIT_FILE_ENDING, --auditfileending AUDIT_FILE_ENDING
                        [str] The audit file extension (default: '.csv')

```


### copyright 2025 mariochampion all rights reserved.