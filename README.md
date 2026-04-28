# GitMyNotes
## GitMyNotes adds convenient version control, off-site backups, and optional collaboration to your macOS Notes.

A lightweight macOS utility using Python and AppleScript to sync your macOS Notes to your public or private GitHub repos (or, optionally, a local only backup). The GitMyNotes solution exports Notes to Markdown in a local directory, while preserving folder organization and formatting. It features out-of-the-box common sense defaults or user-driven customization, a local audit trail file with checkpoint features for interrupted backups, and secure GitHub integration. All processing happens on your machine, with the only external data transmission secured by your enterprise-grade GitHub authentication credentials.


# GitMyNotes is for me?

Do you use Notes? Do you use GitHub? Then undoubtedly yes!

Do you use Notes and could [start with GitHub](https://docs.github.com/en/get-started/start-your-journey)? Then also yes!

`writing is re-writing`
Transform your macOS Notes into a version-controlled archive on GitHub. Use GitMyNotes to preserve and maintain your most excellent lines via versioning to track the full evolution of your work. Learn how to GitHub using branches and forks to explore your ideas, in trusted collabs, or on your own.


`IT team gotta keep copies`
Concerned about a fleet of MacBooks, and all the useful, non-shareable, and non-collaborative notes just one cup of coffee away from disaster? Use GitMyNotes on a cronjob on every Mac to keep versioned copies of valuable Notes.


`prepared tech workers win`
No one can predict the future. Losing a job or a role shouldn't mean losing your personal macOS Notes as well. Set up a free GitHub repo and use GitMyNotes to back up the folders that hold your personal reminders, thoughts, and plans.


`but... I dont use Github (yet?)`
Simply set '--local-only' when you run the command to create, surprise, local-only backups. No GitHub required. But, really, you should [set up](https://docs.github.com/en/get-started/start-your-journey) a free GitHub repo.


## Getting Started

### Prerequisites
1. MacOS with Notes app and AppleScript (ships with every Mac)
2. Python 3.x+
3. Install dependencies: `pip install -r requirements.txt` (just `ruamel.yaml`, used for round-trip-safe config edits)
4. GitHub repo (eg, `https://github.com/<MYUSERNAME>/gitmynotes`) accessible from the Mac running this script. Can be public or private, must be configured working auth credentials, etc.


## Steps 1-2-3
1. First, clone the repo: `git clone https://github.com/mariochampion/gitmynotes.git`

2. Next, `cd` into gitmynotes dir: `cd gitmynotes`

3. Then, in file `gmn_config.yaml`, set the required Github url to your Github url

	-- REQUIRED TO CHANGE--
	
	set `DEFAULT_GITHUB_URL` to the the repo where you want to store Notes.
	
	example: `'DEFAULT_GITHUB_URL': 'https://github.com/<ChangeMe>/gitmynotes'`
	
	OPTIONAL: Leave as-is or change the additional `DEFAULT_*` configs the the file.
	



## Usage

That's it! Now run the script:

`python gitmynotes.py` to run against default "Notes" folder. 

Or be more specific with:

`python gitmynotes.py [--folder='<notesFolderName>' --max-notes=<N> --print-level=results]`

Learn more with:

`python gitmynotes.py --help`



## Better usage

Do this once: set an [alias in your bash profile](https://www.google.com/search?q=set+up+alias+in+mac+bash+profile):`alias gitmynotes='python gitmynotes.py'`

From then on, just use `gitmynotes` as in `gitmynotes --folder='myPythonNotes' --maxnotes=20`

or `gitmynotes --help`


**Note: The reddit_<x>.py are WorkInProgress. Full guidance forthcoming.**


## 
#### Output Artifacts
-- Local --

1. New Notes folder: `<notesFolderName>_GitMyNotes` to store processed notes
2. New GitMyNotes audit file: `<notesFolderName>.csv` to track processed notes
3. Markdown copy of Notes from folder: `DEFAULT_EXPORT_PATH/<my-exported-note.md>`
4. POTENTIALLY: Unsupported notes (often a note with JUST an image) will be moved to `<notesFolderName>_unsupported`

-- Remote --
1. New GitHub directory: `DEFAULT_GITHUB_URL/DEFAULT_NOTES_WRAPPERDIR`
2. New Github sub-dir mapped to Notes folders: `DEFAULT_GITHUB_URL/DEFAULT_NOTES_WRAPPERDIR/<notesFolderName>`
3. Github copy of Notes from folder: `DEFAULT_GITHUB_URL/DEFAULT_NOTES_WRAPPERDIR/<notesFolderName>/<a-note.md>`
4. OPTIONAL - GitMyNotes audit file: `<notesFolderName>.csv`



## A note on locked notes (important)

macOS Notes distinguishes two states for password-protected notes: **closed** (currently showing the lock screen, body hidden) and **open** (unlocked in your current Notes.app session, body visible). GitMyNotes handles these differently:

- **Locked and closed** — AppleScript returns an empty body. GitMyNotes commits a stub file (title + dates + a marker saying the content wasn't exported) to GitHub. No cleartext leaves your Mac.
- **Locked and open** — AppleScript returns the real content, same as any unlocked note. GitMyNotes has no way to tell this case apart, so the cleartext body **will be committed to GitHub**.

macOS does not expose a "locked" status to AppleScript, so GitMyNotes cannot detect this automatically. If you want to keep a locked note's contents private, close it (click away so it re-locks, or close the Notes app) before running GitMyNotes. A note currently showing its lock screen is safe; a note you've unlocked in this session is not.



## HELP and COMMAND list


```
Export macOS Notes to GitHub repo (or local-only directory)

usage: gitmynotes.py [--folder FOLDER] [--maxnotes MAX_NOTES] [--restore RESTORE_NOTES]
                        [--force] [--batch-size BATCH_SIZE] [--export-path EXPORT_PATH]
                        [--github-url GITHUB_URL] [--newline-delimiter NEWLINE_DELIMITER] 
                        [--audit-file-ending AUDIT_FILE_ENDING] or [-h]


options:
FREQUENTLY USED
  -h, --help            show this help message and exit
  
  --folder FOLDER       [str] Specific Notes folder to export.
                        (default: 'Notes')
  
  --max-notes, --maxnotes, --max MAX_NOTES
                        [int] Maximum number of notes to process in this run.
  
  --restore-notes RESTORE_NOTES, --restorenotes RESTORE_NOTES, --restore RESTORE_NOTES
                        [str] Options: 'empty' or 'always' or 'never'. 
                        Determines when to move  notes from '<FOLDER>___GitMyNotes' back 
                        to their original source folder. 
                        Set 'empty' to restore when notecount is 0 in source folder, 
                        Set 'always' to restore at the end of each GitMyNotes run. 
                        Set to 'never' to, well, never move notes back to source folder.
                        (default: 'empty')                        
  
  --print PRINT, --print-level PRINT
                        [str] Optional set to 'none', 'results', 'debug', 'all' for increasing 
                        details. Useful for tracking code flow and general debugging.
                        (default: 'all')

                        
LESS FREQUENTLY USED                        
  --batch-size BATCH_SIZE
                        [int] The number of notes to convert, and git add/commit/push per loop, 
                        calculated a max-notes/batch-size. Especially useful for initial runs.
                        (default: 10)
  
  --export-path EXPORT_PATH, --exportpath EXPORT_PATH
                        [str] Path to export the notes (default: ~/Documents/gitmynotes)
  
  --force               [bool] Use as '--force' (no 'true' or 'false' value allowed) 
                        Use to over-ride to the default required user confirmation to process 
                        the full count of Notes in the specified folder when it exceed 
                        5x the batch size -- which could be hundreds of notes and 
                        could take a looooong time.(default: confirmation will be required)                        
  
  --yes, --non-interactive
                        [bool] Use as '--yes' or '--non-interactive' (no value allowed)
                        for scheduled / non-terminal runs (cron, Cowork routines, CI).
                        Implies '--force' (skips the 5x-batch confirmation) and also
                        fails fast with a clear error if 'DEFAULT_GITHUB_URL' still
                        contains the '<ChangeMe>' placeholder, instead of hanging on
                        the interactive setup prompt.
                        (default: interactive prompting is allowed)
  
  --local-only          [bool] Use as '--local-only' (no 'true' or 'false' value allowed) 
                        Use to over-ride to the default action of backing up notes to GitHub. 
                        When set, only a local copy of notes will be made. 
                        (DEFAULT: Send notes to GitHub repo)
  
  --github-url GITHUB_URL, --githuburl GITHUB_URL
                        [str] GitHub repository URL. 
                        (default: https://github.com/<ChangeMe>/gitmynotes)

  --notes-account NOTES_ACCOUNT, --notesaccount NOTES_ACCOUNT
                        [str] macOS Notes account name (e.g. 'iCloud', 
                        'On My Mac'). Used to scope every AppleScript op to a 
                        single account. Most users want 'iCloud'.
                        (default from config: 'iCloud')
  
  --newline-delimiter NEWLINE_DELIMITER, --newlinedelimiter NEWLINE_DELIMITER
                        [str] Default CSV newline delimiter (default: '|||')
  
  --audit-file-ending AUDIT_FILE_ENDING, --auditfileending AUDIT_FILE_ENDING
                        [str] The audit file extension (default: '.csv')

```


### copyright 2026 mariochampion.com all rights reserved.
