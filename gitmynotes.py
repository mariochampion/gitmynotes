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


# Exit code taxonomy (cross-cutting, paired with R4's logging pass to make
# non-interactive runs -- Cowork routines, cron, CI -- parseable):
#   EXIT_SUCCESS         = 0  -- run completed all intended work cleanly. Includes
#                                no-op runs (loop_count == 0), runs whose only
#                                "issue" was B4 closed-locked notes committed as
#                                stubs (by design, not a partial outcome), runs
#                                with --local-only that complete the local work,
#                                and 'x' typed at the 5x-batch confirm prompt
#                                (clean user-initiated abort -- nothing happened).
#   EXIT_HARD_FAILURE    = 1  -- run could not proceed at all. Bad config (B8
#                                <ChangeMe> fail-fast under --yes), missing
#                                required args (B10 folder guard), invalid
#                                argparse value, or first-step setup failure that
#                                makes any further work pointless. No useful
#                                work was done.
#   EXIT_PARTIAL_SUCCESS = 2  -- run did some work but didn't complete cleanly.
#                                Mainly B1 (unsupported note aborted batch -- the
#                                notes before the bad one were exported, the rest
#                                are left for next run), git push failures after
#                                successful local commits (work is recoverable on
#                                next run, just not on GitHub yet), and
#                                move_processed_notes failures after a successful
#                                export+commit (notes are committed but still in
#                                the source folder, will re-export next run).
EXIT_SUCCESS = 0
EXIT_HARD_FAILURE = 1
EXIT_PARTIAL_SUCCESS = 2


# R14: well-known string sentinels promoted from inline literals so they live in
# one place. Keeps the literal out of multiple sites and gives a searchable name.
#   UNSUPPORTED_NOTE_ERROR_CODE: substring osascript prints to stderr when a
#     note's body can't be read (typically image-bearing notes). Triggers the
#     B1 partial-export recovery path.
#   CHANGEME_PLACEHOLDER: sentinel left in DEFAULT_GITHUB_URL until the user
#     edits gmn_config.yaml. Drives the first-run interactive setup prompt and
#     the B8 --yes fail-fast.
# (FOLDERS_PROCESSED_PLACEHOLDER was retired in R18's data layer: USAGE_FOLDERS_PROCESSED
# is now a mapping rather than a list, and an empty mapping is the natural seed
# value -- no sentinel needed.)
UNSUPPORTED_NOTE_ERROR_CODE = "type 100002"
CHANGEME_PLACEHOLDER = "<ChangeMe>"


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

# R5: sentinel separator between the existing "exported|lockedCount" header and
# the new inline metadata payload that export_notes_to_markdown returns. Chosen
# to be wildly unlikely to appear in a note's title or body. _parse_export_stdout
# splits on this; if the sentinel is missing (older builds, future change) the
# header parsing still works and metadata_rows comes back as None.
GMN_METADATA_SENTINEL = "<<<__GMN_METADATA__>>>"


def export_notes_to_markdown(DEFAULT_CURRENTNOTE_FILE, export_path, notes_account, unsupported_folder_ending, newline_delimiter, folder_name=None, max_notes=None, wrapper_dir=None):
    """Export Notes using applescript/osascript with folder and count limits.

    notes_account scopes every Notes lookup (folder + iteration) to the specified
    account (e.g. 'iCloud', 'On My Mac'). Threaded through from --notes-account /
    DEFAULT_NOTES_ACCOUNT (R6).

    unsupported_folder_ending is the suffix appended to folder_name when the B1
    partial-export recovery path moves an image-bearing note to a sibling folder
    (e.g. folder 'plans' + ending '_unsupported' -> 'plans_unsupported'). Threaded
    through from DEFAULT_UNSUPPORTED_FOLDER_ENDING (R14).

    newline_delimiter is the separator AppleScript uses to join consecutive
    inline metadata rows (R5). Threaded through from --newline-delimiter /
    DEFAULT_NEWLINE_DELIMITER. Same value is used by export_notes_metadata (the
    B1 fallback path) so both paths produce a payload that _parse_metadata_payload
    can split.

    Returns:
        dict with keys:
            'count' (int): number of notes successfully exported in this call.
                Equals max_notes on the happy path; less than max_notes on a B1
                partial (caller flips partial_success). Zero on hard error.
            'metadata_rows' (list[list] | None): pre-parsed audit-CSV rows ready
                for _write_audit_csv_rows -- one row per exported note. R5 fast
                path: caller writes these directly and skips the second-pass
                AppleScript call entirely. None when AppleScript aborted (B1)
                so the inline payload was never returned -- caller falls back
                to export_notes_metadata for the audit-row reconstruction.
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

        -- R5: collect audit metadata inline so the caller can skip the second
        -- AppleScript pass that export_notes_metadata used to do for the same
        -- folder. custom_delimiter joins consecutive rows; the assembled
        -- payload is appended after the header and the GMN_METADATA_SENTINEL.
        set noteList to {{}}
        set custom_delimiter to "{newline_delimiter}"

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
            -- Capture mod date once: used as both the locale-formatted .md
            -- header (existing behavior, preserved for backward compat) and
            -- the locale-independent ISO string for the R5 inline metadata row.
            set theModDate to modification date of currentNote
            set noteCreateDate to "<div><b>Creation Date:</b> " & creation date of currentNote & "<br></div>"
            set noteModDate to "<div><b>Modification Date:</b> " & theModDate & "<br></div>"
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

            -- Write the .md file (date headers stay in their existing locale-
            -- formatted shape since they're just for human reading inside the
            -- markdown -- changing them would mass-shift every existing .md
            -- in the export_path on the next re-export).
            do shell script "echo " & quoted form of noteCreateDate & quoted form of linebreaker & quoted form of noteModDate & quoted form of linebreaker & quoted form of noteContent & " > " & quoted form of export_path_full & "/" & fileName

            -- R5: build inline audit-CSV row in the same format
            -- _parse_metadata_payload expects (matches the row shape the legacy
            -- export_notes_metadata second-pass produces).
            set isoYear to year of theModDate as string
            set isoMonth to text -2 thru -1 of ("0" & ((month of theModDate) as integer))
            set isoDay to text -2 thru -1 of ("0" & day of theModDate)
            set isoHour to text -2 thru -1 of ("0" & hours of theModDate)
            set isoMin to text -2 thru -1 of ("0" & minutes of theModDate)
            set isoSec to text -2 thru -1 of ("0" & seconds of theModDate)
            set isoModDate to isoYear & "-" & isoMonth & "-" & isoDay & " " & isoHour & ":" & isoMin & ":" & isoSec
            -- Strip commas from the title for the CSV row (matches the same
            -- sed in export_notes_metadata so both paths produce identical
            -- title sanitization).
            set noteTitleCsv to do shell script ("echo " & quoted form of noteTitle & "| sed 's/,/-/g'")
            set noteData to noteTitleCsv & "," & fileName & "," & isoModDate & custom_delimiter
            copy noteData to the end of noteList
        end repeat

        -- R5: assemble the metadata payload by concatenating the noteList
        -- items into a single string. (Returning a list directly would have
        -- AppleScript inject ", " between items in the osascript text output,
        -- which the parser would have to strip per-row -- _parse_metadata_payload
        -- handles that anyway as a defensive measure, but concatenating cleanly
        -- here keeps the payload tight.)
        set metadataPayload to ""
        repeat with mItem in noteList
            set metadataPayload to metadataPayload & mItem
        end repeat

        -- B4 + R5: compound return value. Header stays "exported|lockedCount"
        -- so the existing parser can read it; the metadata payload is appended
        -- after a sentinel so older builds (or any future codepath that doesn't
        -- emit metadata) still parse cleanly without it.
        return (notesToProcess as string) & "|" & (lockedCount as string) & "{GMN_METADATA_SENTINEL}" & metadataPayload
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

        searchstring = UNSUPPORTED_NOTE_ERROR_CODE
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
            folder_dest = folder_name + unsupported_folder_ending
            move_one_note(noteTitle, folder_name, folder_dest, notes_account, create=True)
            goodnotes = noteCount - 1
            logger.warning(
                f"Unsupported note '{noteTitle}' (folder '{folder_name}', index {noteCount}) aborted batch; "
                f"exported {goodnotes} note(s) before the failure."
            )
            print_color(textcolor="cyan", msg=f"Exported {goodnotes} note(s) successfully before hitting unsupported content; continuing with those.")
            # R5: AppleScript aborted before returning -- inline metadata is
            # lost. Caller falls back to export_notes_metadata for the goodnotes
            # rows (B1 path).
            return {'count': goodnotes, 'metadata_rows': None}

        else:
            debug_print(f"{searchstring} is not present.")

        return {'count': 0, 'metadata_rows': None}


    # B4: stdout is a compound "exported|lockedCount<sentinel>metadataPayload"
    # string (see AppleScript `return`). R5 added the sentinel + metadata; the
    # `type 100002` branch above still returns a plain dict directly, so this
    # parser only runs on the success path.
    stdout_val = result.stdout.strip() if result.stdout else ""
    if not stdout_val:
        return {'count': 0, 'metadata_rows': None}

    # R5: split off the metadata payload from the header. If the sentinel is
    # missing (shouldn't happen post-R5 but defensive), header parsing still
    # works and metadata_rows comes back None so the caller falls back to the
    # second-pass AppleScript.
    if GMN_METADATA_SENTINEL in stdout_val:
        header_part, metadata_part = stdout_val.split(GMN_METADATA_SENTINEL, 1)
    else:
        header_part = stdout_val
        metadata_part = None

    header_part = header_part.strip()
    if '|' in header_part:
        try:
            exported_str, locked_str = header_part.split('|', 1)
            exported_count = int(exported_str.strip())
            locked_count = int(locked_str.strip())
        except ValueError:
            debug_print(f"Could not parse compound export result header: {header_part!r}")
            return {'count': 0, 'metadata_rows': None}
    else:
        # Backwards-compatible fallback: plain int return (shouldn't happen post-B4 but safe).
        try:
            exported_count = int(header_part)
            locked_count = 0
        except ValueError:
            return {'count': 0, 'metadata_rows': None}

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

    # R5: parse the inline metadata payload into audit-CSV rows. Empty payload
    # (no notes exported, or sentinel-missing fallback) returns [] which the
    # caller treats as "no inline data, fall back to export_notes_metadata."
    metadata_rows = None
    if metadata_part is not None:
        metadata_rows = _parse_metadata_payload(metadata_part, folder_name, newline_delimiter)
        if exported_count > 0 and len(metadata_rows) != exported_count:
            logger.warning(
                f"Inline metadata row count ({len(metadata_rows)}) doesn't match "
                f"exported count ({exported_count}) for folder '{folder_name}'. "
                f"Caller will fall back to export_notes_metadata."
            )
            metadata_rows = None

    return {'count': exported_count, 'metadata_rows': metadata_rows}



##### Describe this function

def git_add_commit_push(repo_path, folder_name=None, wrapper_dir=None):
    """Commit changes and push to GitHub.

    Returns:
        bool: True if every git step ran cleanly (add ok, commit ok or benign
            'nothing to commit', push ok including 'Everything up-to-date').
            False if any step failed -- caller (main()) flips partial_success
            so the run exits with EXIT_PARTIAL_SUCCESS. Per the exit-code
            taxonomy decision, push-failed-after-good-commits is partial
            (work is committed locally and recoverable on the next run);
            commit-failed-after-good-export is also partial since the export
            already wrote files to disk that just didn't reach git.
    """
    # Always operate from the git root directory

    all_clean = True

    result_gitadd = subprocess.run(['git', 'add', f'{wrapper_dir}'], cwd=repo_path)
    if result_gitadd.returncode == 0:
        print_color(textcolor="green",msg=f"Successful GIT ADD to origin/main.")
        results_print(f"1 result_gitadd: {result_gitadd}")
    else:
        all_clean = False
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
        all_clean = False
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
            all_clean = False
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
        all_clean = False
        logger.error(f"Skipping GIT PUSH due to upstream commit error in repo '{repo_path}'.")
        print_color(textcolor="red",msg=f"Commit error so no GIT PUSH to origin/main:")
        print(" ")

    return all_clean



##### Describe this function

# R5: shared metadata-payload parser. Same string format produced by both the
# legacy second-pass AppleScript in export_notes_metadata AND the inline first-
# pass AppleScript in export_notes_to_markdown (R5 fast path). Each row is
# "<title>,<cleanTitle>.md,<isoModDate>" and rows are concatenated with the
# user's configured newline_delimiter (default '|||'). AppleScript's list-to-
# text coercion sticks ", " between items when returning a list directly; that
# becomes leading whitespace on each split chunk, which we strip below.
def _parse_metadata_payload(raw_output, folder, newline_delimiter):
    """Parse the concatenated metadata string into a list of audit-CSV rows.

    Returns a list of 5-element rows: [folder, title, formatted_date,
    quoted_title, current_datetime]. The current_datetime stamp is shared
    across all rows from one parse call so an audit-CSV "Exported Date"
    column groups rows from the same run cleanly.
    """
    if not raw_output:
        return []
    notes_data = []
    raw_lines = raw_output.split(newline_delimiter)
    # The trailing delimiter on the last row leaves an empty final chunk;
    # drop it. (Matches the pre-R5 export_notes_metadata behavior.)
    if raw_lines and raw_lines[-1].strip() == "":
        raw_lines = raw_lines[:-1]
    current_datetime = datetime.now()
    for line in raw_lines:
        line = line.rstrip(",")
        if line.startswith(','):
            line = line[1:]
        if line.endswith(','):
            line = line[:-1]
        # AppleScript-emitted lines may have leading whitespace from the
        # ", " inter-item glue; strip before any further parsing.
        line = line.strip()
        if not line:
            continue
        line_items = line.split(',', 2)
        if len(line_items) < 3:
            logger.warning(
                f"Skipping malformed metadata line for folder '{folder}': {line!r}"
            )
            continue
        title = line_items[0].strip()
        quoted_title = line_items[1].strip()
        mod_date = line_items[2].strip()

        # R18 follow-up (session 17): AppleScript now emits 'YYYY-MM-DD
        # HH:MM:SS' directly (built from date components, locale-independent)
        # so we just validate the round-trip rather than reformat. The fallback
        # logs a warning and uses the raw string so a malformed AppleScript
        # output surfaces instead of silently corrupting the CSV.
        try:
            date_obj = datetime.strptime(mod_date, '%Y-%m-%d %H:%M:%S')
            formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            logger.warning(
                f"Unexpected mod_date format from AppleScript for note '{title}' "
                f"in folder '{folder}': {mod_date!r}. Using raw value; watermark "
                f"advance for this row will be skipped."
            )
            formatted_date = mod_date

        notes_data.append([folder, title, formatted_date, quoted_title, current_datetime])
    return notes_data


# R5: shared CSV writer. Mode 'a' if file exists, 'w' if not (writing the
# header row in the 'w' case). Used by both the R5 fast path (inline metadata
# from export_notes_to_markdown) and the B1 fallback path (export_notes_metadata).
def _write_audit_csv_rows(output_file, rows, folder=None):
    """Append `rows` to the audit CSV at `output_file`.

    Creates the file with a header row if it doesn't exist, appends to the
    existing file otherwise. `folder` is purely for the success print line.
    """
    if not rows:
        return
    mode = 'a' if os.path.exists(output_file) else 'w'
    with open(output_file, mode, newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if mode == 'w':
            writer.writerow(['Folder', 'Original Title', 'Last Modified', 'Exported Title', 'Exported Date'])
        writer.writerows(rows)
    for row in rows:
        # Per-row visibility (preserves the chatty white prints from pre-R5
        # export_notes_metadata so debug_print=ALL runs look the same).
        print_color(textcolor="white", msg=f"Adding row to audit file: {output_file}")
        print_color(textcolor="white", msg=f" - from Notes folder: '{row[0]}', Notes title:' {row[1]}', ModDate: '{row[2]}', Markdown title: '{row[3]}', Exported Date: '{row[4]}'")
        print(" ")
    print_color(textcolor="green", msg=f"22 SUCCESS: Exported {len(rows)} notes to '{output_file}'", addseparator=True)


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

    R5 status: this function is now the B1 fallback path only -- the happy
    path collects the same metadata inline during export_notes_to_markdown
    and skips this second AppleScript pass entirely. process_one_folder calls
    this only when the inline metadata is empty (which happens when AppleScript
    aborts on a 'type 100002' error before returning, since the noteList built
    inside the loop is lost on abort).
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
        -- R18 follow-up: build a parseable ISO-shaped date string from the date
        -- components instead of relying on string-coercion of the date object,
        -- which yields a locale-formatted string ("Saturday, January 18, 2025
        -- at 2:25:20 PM" on en-US) that Python can't parse without locale-
        -- specific format strings. The component-based construction is
        -- locale-independent. This is the value Python writes into the audit
        -- CSV's "Last Modified" column AND the value max_mod_date_from_rows
        -- parses for the per-folder watermark advance.
        set theModDate to modification date of theNote
        set isoYear to year of theModDate as string
        set isoMonth to text -2 thru -1 of ("0" & ((month of theModDate) as integer))
        set isoDay to text -2 thru -1 of ("0" & day of theModDate)
        set isoHour to text -2 thru -1 of ("0" & hours of theModDate)
        set isoMin to text -2 thru -1 of ("0" & minutes of theModDate)
        set isoSec to text -2 thru -1 of ("0" & seconds of theModDate)
        set isoModDate to isoYear & "-" & isoMonth & "-" & isoDay & " " & isoHour & ":" & isoMin & ":" & isoSec
        set noteData to noteTitle &","& cleanTitle & ".md" &","& isoModDate & custom_delimiter
        copy noteData to the end of noteList
        end repeat
        return noteList
        end tell
    end tell
    '''

    result, output = process_applescript(applescript)
    results_print(f"process_applescript result: {result}")
    print("-------------------")
    results_print(f"process_applescript output: {output}")

    # R5: parse + write via the shared helpers (extracted from the original
    # inline parser/writer that lived here).
    notes_data = _parse_metadata_payload(output, folder, newline_delimiter)
    _write_audit_csv_rows(output_file, notes_data, folder=folder)

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


# R18 data layer: helpers for the per-folder mod-date watermark stored in
# USAGE_FOLDERS_PROCESSED. Watermarks are ISO 8601 naive-local-time strings of
# the form 'YYYY-MM-DDTHH:MM:SS'. β semantics: each new value only replaces the
# existing watermark if it is strictly greater (advances only).
def parse_watermark_iso(watermark_str):
    """Parse an ISO 8601 watermark string back to a naive datetime, or return
    None for null / empty / unparseable input. A None result is treated by the
    feature layer as 'folder seeded but never successfully run' -- '--auto'
    skips those folders with a yellow warning."""
    if not watermark_str:
        return None
    try:
        return datetime.fromisoformat(watermark_str)
    except (TypeError, ValueError):
        return None


def max_mod_date_from_rows(rows):
    """Walk a processednotes_data list (as produced by export_notes_metadata)
    and return the maximum parsed modification-date as a naive datetime, or
    None if no row had a parseable date.

    Each row is [folder, title, formatted_date, quoted_title, current_datetime];
    formatted_date is '%Y-%m-%d %H:%M:%S' on the success path of
    export_notes_metadata's own date parsing. Rows whose date didn't parse
    cleanly there fall back to the original AppleScript-formatted string and
    are skipped here -- a partial sample still gives us a usable max.
    """
    if not rows:
        return None
    parsed = []
    for row in rows:
        try:
            parsed.append(datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S'))
        except (TypeError, ValueError, IndexError):
            continue
    return max(parsed) if parsed else None


# R18 feature layer: count how many notes in a folder have been modified
# strictly after the given watermark. Used by --auto mode to decide whether a
# folder needs processing this run, and to bound the per-folder max_notes so
# the existing batch pipeline doesn't churn through unchanged notes.
#
# The watermark is built into an AppleScript date object via component setters
# (year/month/day/time-in-seconds) rather than via a string-based date literal,
# because AppleScript's `date "<string>"` parsing is locale-dependent. The
# component approach is portable across user locale settings.
#
# Returns 0 on any failure (folder missing, AppleScript error, parse failure).
# Callers in --auto mode treat 0 as "no work to do" and skip the folder; that
# matches the behavior we'd want for a transient AppleScript hiccup as well as
# a genuinely-unchanged folder, since either way there's nothing to back up.
def count_notes_modified_since(folder, watermark_iso, notes_account):
    """Return int count of notes in `folder` whose modification date is
    strictly greater than `watermark_iso` (an ISO 8601 string of the form
    'YYYY-MM-DDTHH:MM:SS' produced by R18's data layer).

    Args:
        folder (str): Notes folder name. Required.
        watermark_iso (str): ISO 8601 watermark string, or None / empty if the
            folder has no recorded watermark yet (caller should normally check
            this before calling and skip-with-warning rather than ask us to
            count -- but be defensive).
        notes_account (str): macOS Notes account to scope the lookup to (R6).

    Returns:
        int: count of notes with mod date > watermark. 0 on any failure or
            unparseable watermark.
    """
    if not watermark_iso:
        return 0
    wm = parse_watermark_iso(watermark_iso)
    if wm is None:
        return 0

    folder_escaped = folder.replace('"', '\\"')
    notes_account_escaped = notes_account.replace('"', '\\"')

    applescript = f'''
    tell application "Notes"
        set targetAccount to "{notes_account_escaped}"
        tell account targetAccount
            try
                set targetFolder to folder "{folder_escaped}"
            on error
                return 0
            end try
            set folderNotes to every note in targetFolder
            -- Build watermark date from components (locale-independent).
            set wm to current date
            set year of wm to {wm.year}
            set month of wm to {wm.month}
            set day of wm to {wm.day}
            set time of wm to ({wm.hour} * 3600 + {wm.minute} * 60 + {wm.second})
            set modifiedCount to 0
            repeat with theNote in folderNotes
                if (modification date of theNote) > wm then
                    set modifiedCount to modifiedCount + 1
                end if
            end repeat
            return modifiedCount
        end tell
    end tell
    '''
    success, output = process_applescript(applescript)
    if not success:
        return 0
    try:
        return int(output)
    except (TypeError, ValueError):
        return 0


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

def process_one_folder(folder, max_notes_request, args, run_config, run_state, skip_5x_confirm=False):
    """Process a single Notes folder end-to-end.

    R18 feature-layer refactor: the per-folder pipeline (count -> optional 5x
    confirm -> batch loop -> export -> commit/push -> audit -> move -> restore
    -> per-folder watermark advance) now lives here so main() can call it once
    in normal mode or repeatedly under --auto without duplicating the logic.

    Args:
        folder (str): Notes folder to process. Required (caller has already
            handled the no-folder case via the B10 guard or by iterating
            USAGE_FOLDERS_PROCESSED).
        max_notes_request (int|None): user's --max-notes intent for this
            folder, or under --auto the count returned by
            count_notes_modified_since() so the loop is bounded by what's
            actually changed.
        args (argparse.Namespace): parsed CLI args. Read for batch_size,
            export_path, github_url, local_only, force, restore_notes,
            newline_delimiter, audit_file_ending, notes_account. Not mutated.
        run_config (dict): per-run config values pulled from gmn_config.yaml
            once in main() and threaded in. Required keys:
                'currentnote_file' (str, absolute path post-B9),
                'unsupported_folder_ending' (str),
                'processed_folder_ending' (str),
                'wrapper_dir' (str),
                'loopcount_before_confirm' (int).
        run_state (dict): mutable run-level state. This function MUTATES:
                'USAGE_NOTES_PROCESSED' (int): incremented by total
                    notes_processed in this folder pass.
                'USAGE_FOLDERS_PROCESSED' (dict): the watermark for `folder`
                    is advanced if a strictly-greater max mod-date was
                    observed (R18 data layer's beta semantics).
                'folders_dirty' (bool): flipped True on any change to
                    USAGE_FOLDERS_PROCESSED.
        skip_5x_confirm (bool): True for --auto runs (5x-batch confirmation
            suppressed entirely per R18 design). False for normal interactive
            runs, which keep the existing prompt behavior.

    Returns:
        dict with keys:
            'folder' (str): the folder processed (echoed back for the auto
                loop's summary).
            'partial' (bool): True if any partial-success signal fired in this
                folder pass (B1 short-export, git_add_commit_push False,
                move_processed_notes falsy after real export work).
            'aborted_by_user' (bool): True if user typed 'x' at the 5x-batch
                confirmation prompt (only possible when skip_5x_confirm=False
                AND --force / --yes is not set).
            'notes_processed' (int): total notes exported across this folder's
                batches (used by the auto loop's summary).
            'loop_count' (int): how many batches actually ran (0 means no-op,
                e.g. empty folder, --max-notes=0, or --auto count=0).
            'audit_file' (str): the audit CSV path for this folder.
            'gitnotes_url' (str): GitHub URL pointing at this folder's subdir.
    """
    partial_for_folder = False
    aborted_by_user = False
    wrapper_dir = run_config['wrapper_dir']
    audit_file = f"./{folder}{args.audit_file_ending}"

    # gitnotes_url for the per-folder summary (matches the legacy build_final_msg
    # construction: with wrapper_dir if set, otherwise direct).
    if wrapper_dir:
        gitnotes_url = f"{args.github_url}/tree/main/{wrapper_dir}/{folder}"
    else:
        gitnotes_url = f"{args.github_url}/tree/main/{folder}"

    # Make sure this folder's local export subdir exists (was hoisted out of the
    # batch loop in main() pre-refactor; per-folder under R18 it has to live
    # here so each folder's subdir gets created).
    export_path_w_folder = f"{args.export_path}/{wrapper_dir}/{folder}"
    os.makedirs(export_path_w_folder, exist_ok=True)

    # Mark folder dirty if we've never seen it before (data-layer pre-loop block
    # used to live in main; in --auto mode the caller already iterated
    # USAGE_FOLDERS_PROCESSED so the folder will already be there, but a
    # manual --folder=NEWFOLDER run is always possible so handle it here too).
    if folder not in run_state['USAGE_FOLDERS_PROCESSED']:
        run_state['USAGE_FOLDERS_PROCESSED'][folder] = None
        run_state['folders_dirty'] = True

    # Folder note count + 5x-batch decision
    folder_count = get_foldernotecount(folder, args.notes_account)
    if max_notes_request:
        if max_notes_request > folder_count:
            notes_to_process = folder_count
        else:
            notes_to_process = max_notes_request
    else:
        notes_to_process = folder_count

    if not skip_5x_confirm and notes_to_process > (args.batch_size * run_config['loopcount_before_confirm']):
        if args.force:
            print(f"In the original command --force was set, continuing without confirm...")
        else:
            confirm_warn = f'''WHOA. {notes_to_process} notes to process in '{folder}' folder!

    <<<< Confirmation Required.>>>>

Add '--force' to skip confirmation in the future.'''
            logger.warning(
                f"Large batch confirmation triggered: {notes_to_process} notes in '{folder}' "
                f"(>{args.batch_size}*{run_config['loopcount_before_confirm']}). Awaiting interactive confirmation."
            )
            print_color(textcolor='magenta', msg=f"{confirm_warn}", addseparator=True)
            confirm_msg = f'''Please input:
  a number up to {notes_to_process} of notes to process,
  or 'x' to eXit
  [Or 'enter' to process all {notes_to_process} notes] : '''

            confirm_num = input(f"{confirm_msg}") or f"{notes_to_process}"
            if confirm_num == 'x' or confirm_num == '0':
                # Clean user-initiated abort. Nothing has happened yet -- no export,
                # no git ops -- so this is a successful no-op for this folder.
                # Caller (main()) will sys.exit(EXIT_SUCCESS) on this signal in
                # non-auto mode. Under --auto the prompt is suppressed entirely
                # so this branch is unreachable.
                print_color(textcolor='red', msg="    Exiting GitMyNotes...", addseparator=True)
                aborted_by_user = True
                return {
                    'folder': folder,
                    'partial': False,
                    'aborted_by_user': True,
                    'notes_processed': 0,
                    'loop_count': 0,
                    'audit_file': audit_file,
                    'gitnotes_url': gitnotes_url,
                }
            confirm_num = int(confirm_num)
            if confirm_num > notes_to_process:
                confirm_num = notes_to_process
            debug_print(f"aa Notes to process: {confirm_num}")
            notes_to_process = confirm_num

    # Loop math
    loop_count = math.ceil(notes_to_process / args.batch_size) if notes_to_process > 0 else 0

    debug_print("IN process_one_folder")
    debug_print(f"folder {folder}")
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
    notes_processed_total = 0
    # R18 data layer: track running max mod-date across this folder's batches.
    new_watermark_dt = None

    for x in range(1, loop_count + 1):
        print_color(textcolor="cyan", msg=f"    Begin export of Notes with batch {x} of {loop_count}", addseparator=True)

        if loop_count == 1:
            notes_to_export = notes_to_process
        if x < loop_count:
            notes_to_export = args.batch_size
        if x == loop_count:
            notes_to_export = final_loop_size
        print(f"batch size for this loop: {notes_to_export}")

        if notes_to_export > 0:
            notes_processed = export_notes_to_markdown(
                run_config['currentnote_file'],
                args.export_path,
                args.notes_account,
                run_config['unsupported_folder_ending'],
                folder,
                notes_to_export,
                wrapper_dir,
            )
            # B1 partial-success signal: when an unsupported (image-bearing)
            # note aborts the batch mid-flight, export_notes_to_markdown returns
            # the count of notes successfully exported BEFORE the bad one.
            if notes_processed < notes_to_export:
                partial_for_folder = True

        if notes_processed > 0:
            notes_processed_total += notes_processed
            print_color(textcolor="green", msg=f"SUCCESS: Exported {notes_processed} Notes to local folder {args.export_path}")

            ## SEND TO GITHUB BY DEFAULT, UNLESS 'LOCAL' OPTION SET TRUE
            if args.local_only:
                print_color(textcolor="magenta", msg=f"The --local-only flag is set. No notes sent to Github", addseparator=True)
            else:
                git_clean = git_add_commit_push(args.export_path, folder, wrapper_dir)
                if not git_clean:
                    partial_for_folder = True

        else:
            logger.warning(f"No notes were processed in batch {x}/{loop_count} for folder '{folder}'; skipping git commit.")
            print_color(textcolor="magenta", msg=f"No notes were processed, skipping git commit")

        ## if notes were processed to git, then create the audit trail and move the notes
        if notes_processed > 0:
            debug_print(f"NOTES PROCESSED > 0: {notes_processed}")
            print_color(textcolor="white", msg=f"Notes to export to markdown: {notes_processed}")
            debug_print(f'''BEFORE export:
output_file={audit_file}
folder={folder}
max_notes={notes_processed}
newline_delimiter={args.newline_delimiter}''')

            processednotes_data = export_notes_metadata(
                output_file=audit_file,
                folder=folder,
                max_notes=notes_processed,
                newline_delimiter=args.newline_delimiter,
                notes_account=args.notes_account,
            )

            # R18 data layer: feed this batch's max mod-date into the running
            # max for the folder. Used post-loop to advance the folder's
            # watermark in USAGE_FOLDERS_PROCESSED if strictly greater.
            batch_max = max_mod_date_from_rows(processednotes_data)
            if batch_max is not None and (new_watermark_dt is None or batch_max > new_watermark_dt):
                new_watermark_dt = batch_max

        if processednotes_data:
            move_result = move_processed_notes(
                folder_source=folder,
                folder_dest=f"{folder}{run_config['processed_folder_ending']}",
                max_notes=notes_processed,
                notes_account=args.notes_account,
                create=True,
            )
        else:
            move_result = 0
            print_color(textcolor="magenta", msg=f"No Notes to Move")

        if move_result:
            print_color(textcolor="green", msg=f"SUCCESS: Moved notes to Notes folder: '{folder}{run_config['processed_folder_ending']}'", addseparator=True)
        else:
            # Only treat this as a partial-success signal when we actually
            # expected a move to happen (i.e., we had processednotes_data).
            if processednotes_data:
                partial_for_folder = True
            logger.error(
                f"Failed to move processed notes from '{folder}' to "
                f"'{folder}{run_config['processed_folder_ending']}' (batch {x}/{loop_count})."
            )
            print_color(textcolor="red", msg=f"    !!! FAILED to MOVE notes !!!", addseparator=True)

        ######## ----  update usage counts (in-memory; flushed once at end of run, R10)  ---- #######
        results_print(f"++++++++++  Update config yaml usage stats  +++++++++++++")
        debug_print(f"(before)USAGE_NOTES_PROCESSED: {run_state['USAGE_NOTES_PROCESSED']}")
        debug_print(f"notes_processed: {notes_processed}")

        run_state['USAGE_NOTES_PROCESSED'] = int(run_state['USAGE_NOTES_PROCESSED']) + int(notes_processed)
        debug_print(f"(after)USAGE_NOTES_PROCESSED: {run_state['USAGE_NOTES_PROCESSED']}")
        debug_print(f"++++++++++++++++++++++++++++++++++++++++++++++")

    # R18 data layer: post-loop, advance this folder's watermark if a strictly-
    # greater max mod-date was observed (beta semantics: only advances). Skip
    # the advance entirely on a no-op run (loop_count == 0).
    if loop_count > 0 and new_watermark_dt is not None:
        existing_dt = parse_watermark_iso(run_state['USAGE_FOLDERS_PROCESSED'].get(folder))
        if existing_dt is None or new_watermark_dt > existing_dt:
            run_state['USAGE_FOLDERS_PROCESSED'][folder] = new_watermark_dt.isoformat(timespec='seconds')
            run_state['folders_dirty'] = True

    if processednotes_data:
        ## check for restore-empty-source-folder to decide what to do with contents of folder_GitMyNotes backup folders
        debug_print(f"Option --restore-notes is '{args.restore_notes}'")

        restore_result = 0
        restore_result = restore_source_foldernote(
            folder_source=folder,
            folder_bkup=f"{folder}{run_config['processed_folder_ending']}",
            restore_notes=args.restore_notes,
            notes_account=args.notes_account,
        )

        if restore_result:
            print_color(textcolor="green", msg=f"SUCCESS: RESTORED notes to {folder} from {folder}{run_config['processed_folder_ending']}", addseparator=True)
        else:
            restore_declined_msg = f'''    << Notes not restored to '{folder}' >>
        Set --restore-notes=empty to move notes back to '{folder}' when notecount is 0
        Set --restore-notes=always to move notes back to '{folder}' after every backup'''
            print_color(textcolor="red", msg=f"{restore_declined_msg}", addseparator=True)

    return {
        'folder': folder,
        'partial': partial_for_folder,
        'aborted_by_user': aborted_by_user,
        'notes_processed': notes_processed_total,
        'loop_count': loop_count,
        'audit_file': audit_file,
        'gitnotes_url': gitnotes_url,
    }


##### Describe this function

def main():

    # R4 (incremental): wire up the file logger first so any subsequent
    # warning- / error-level event in this run lands in <script_dir>/gitmynotes.log
    # alongside the existing colored TTY prints. Hardcoded log location for now;
    # CLI override can be added later if needed.
    setup_logging()

    # Exit-code taxonomy: track whether anything in this run was less-than-clean
    # so we can pick between EXIT_SUCCESS and EXIT_PARTIAL_SUCCESS at end of run.
    # Hard-failure paths (bad config, B10 guard, B8 fail-fast) sys.exit() directly
    # with EXIT_HARD_FAILURE before they can flip this flag. Sites that flip it:
    #   - B1 short-export (notes_processed < notes_to_export when batch was nonzero)
    #   - git_add_commit_push() returns False (commit error or push failure)
    #   - move_processed_notes() falsy result after a real export+commit
    partial_success = False

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
    # R14: cfg.get fallback covers users who upgrade without updating their yaml
    # (the historic literal '_unsupported' is preserved as the default).
    DEFAULT_UNSUPPORTED_FOLDER_ENDING = cfg.get('DEFAULT_UNSUPPORTED_FOLDER_ENDING', '_unsupported')
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

    # R18 feature layer: --auto walks USAGE_FOLDERS_PROCESSED and backs up
    # only what's changed since the per-folder watermark was last advanced.
    # Pairs naturally with --yes / --non-interactive for unattended scheduled
    # runs. Folders with a null watermark (seeded via a single manual run but
    # never successfully populated) are skipped with a yellow warning.
    parser.add_argument('--auto', action='store_true',
                      default=False,
                      help=f"[bool] Use as '--auto' (no value allowed) to back up every folder GitMyNotes already knows about (those listed in 'USAGE_FOLDERS_PROCESSED' in 'gmn_config.yaml'), but only the notes that have changed since each folder's last successful run. Skips folders with no recorded watermark (instructs you to seed them with one manual '--folder=NAME' run first). Suppresses the 5x-batch confirmation entirely. Per-folder failures are isolated -- one stale folder doesn't stop the others. Combine with '--yes' for unattended scheduled / cron / Cowork-routine runs. '--folder' is ignored under '--auto'. (default: off)")

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

    # R18 feature layer: B10 folder guard only fires in non-auto mode. In --auto
    # the "folder" is implicit (each known folder in USAGE_FOLDERS_PROCESSED),
    # so requiring an explicit --folder would defeat the purpose. If the user
    # passes both --folder=X AND --auto, --folder is silently ignored (with a
    # one-line debug note) per the help text contract.
    if not args.auto:
        # B10: guard against folder==None / empty-string. Multi-folder "export
        # all" mode was advertised in the top-of-file docstring and help text
        # but has never actually worked end-to-end -- get_foldernotecount(None)
        # returns None and the next comparison throws TypeError, and multiple
        # downstream paths (audit file naming, __GitMyNotes folder creation,
        # USAGE tracking) assume a real folder name. Rather than leave a broken
        # path silently present, fail fast with a clear remediation. R18's
        # --auto is the proper multi-folder solution; for users not using
        # --auto, the per-folder run is still required.
        if not args_folder:
            logger.error(
                "Refusing to run: no folder specified. Pass --folder <name>, set DEFAULT_NOTES_FOLDER in gmn_config.yaml, or use --auto. (B10 guard.)"
            )
            print_color(
                textcolor="red",
                msg=(
                    "ERROR: GitMyNotes requires an explicit folder to back up.\n"
                    "    Please either pass '--folder <folderName>' on the command line, set\n"
                    "    'DEFAULT_NOTES_FOLDER' in 'gmn_config.yaml' to a real folder name,\n"
                    "    or use '--auto' to back up every folder GitMyNotes already knows about."
                ),
                addseparator=True,
            )
            sys.exit(EXIT_HARD_FAILURE)
    else:
        if args_folder:
            debug_print(f"--auto is set; ignoring --folder='{args_folder}' (auto mode walks USAGE_FOLDERS_PROCESSED).")

    ## set up the initial msg to let people know setup details
    if args.auto:
        # In --auto mode the per-folder "Notes folder: X" line in the banner
        # would be misleading; we'll print per-folder banners inside
        # process_one_folder + an aggregate summary at the end. The run-level
        # banner just says we're in auto mode.
        initial_msg = build_initial_msg(this_msg="", folder=None, max_notes=None, export_path=args.export_path, github_url=args.github_url, print_level=PRINT_LEVEL, local_only=args_local_only)
        print_color(textcolor='cyan', msg=f"{initial_msg}    - Mode: --auto (walking USAGE_FOLDERS_PROCESSED)\n", addseparator=True)
    else:
        initial_msg = build_initial_msg(this_msg="", folder=args_folder, max_notes=args_max_notes, export_path=args.export_path, github_url=args.github_url, print_level=PRINT_LEVEL, local_only=args_local_only)
        print_color(textcolor='cyan', msg=f"{initial_msg}", addseparator=True)


    ######## ----  Do INIT work, ensure DEFAULT_GITHUB_URL has been changed    ---- #######
    if USAGE_GITMYNOTES_TOTAL == 0:
        # First-timer block. R18 data layer retired the placeholder-swap that used
        # to live here; with the new mapping shape, an empty USAGE_FOLDERS_PROCESSED
        # is the natural seed value, and the per-folder seeding (with a null
        # watermark) happens just before the batch loop in the folders_dirty block.
        # Kept as a hook for future first-time-user UX (welcome message, etc.).
        results_print(f"USAGE_FOLDERS_PROCESSED : {USAGE_FOLDERS_PROCESSED}")

    if CHANGEME_PLACEHOLDER in DEFAULT_GITHUB_URL:
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
            sys.exit(EXIT_HARD_FAILURE)

        usage_github_username = input("Please enter your GitHub username: ")
        print(f"The 'DEFAULT_GITHUB_URL' will be updated to 'https://github.com/{usage_github_username}/gitmynotes'")
        ## now update the yaml file
        update_yaml_config('gmn_config.yaml', 'DEFAULT_GITHUB_URL', f"https://github.com/{usage_github_username}/gitmynotes")
        cfg = load_configs_from_file()
        DEFAULT_GITHUB_URL = cfg['DEFAULT_GITHUB_URL']
        # Keep args.github_url consistent with the just-saved DEFAULT so every
        # downstream consumer (process_one_folder's gitnotes_url, the final_msg
        # builder) sees the same value.
        args.github_url = DEFAULT_GITHUB_URL


        ## RE-DO the initial msg to let people know setup details have changed
        if args.auto:
            initial_msg = build_initial_msg(this_msg="", folder=None, max_notes=None, export_path=args.export_path, github_url=args.github_url, print_level=PRINT_LEVEL, local_only=args_local_only)
            print_color(textcolor='cyan', msg=f"{initial_msg}    - Mode: --auto (walking USAGE_FOLDERS_PROCESSED)\n", addseparator=True)
        else:
            initial_msg = build_initial_msg(this_msg="", folder=args_folder, max_notes=args_max_notes, export_path=args.export_path, github_url=args.github_url, print_level=PRINT_LEVEL, local_only=args_local_only)
            print_color(textcolor='cyan', msg=f"{initial_msg}", addseparator=True)



    ######## ----  BUILD initial dirs per args and DEFAULTS    ---- #######
    # The export_path root is always needed; per-folder subdirs get created
    # inside process_one_folder.
    os.makedirs(args.export_path, exist_ok=True)



    ######## ----  Setup the git repo per args and DEFAULTs    ---- #######
    # Single git repo for the whole run regardless of how many folders are
    # processed -- each folder lands in its own subdir under wrapper_dir.
    setup_git_repo(args.export_path, DEFAULT_GITHUB_URL)


    ######## ----  R18 feature layer: bundle per-run config + state for process_one_folder ---- #######
    run_config = {
        'currentnote_file': DEFAULT_CURRENTNOTE_FILE,
        'unsupported_folder_ending': DEFAULT_UNSUPPORTED_FOLDER_ENDING,
        'processed_folder_ending': DEFAULT_PROCESSED_FOLDER_ENDING,
        'wrapper_dir': args_wrapper_dir,
        'loopcount_before_confirm': DEFAULT_LOOPCOUNT_BEFORE_CONFIRM,
    }
    run_state = {
        'USAGE_NOTES_PROCESSED': int(USAGE_NOTES_PROCESSED),
        'USAGE_FOLDERS_PROCESSED': USAGE_FOLDERS_PROCESSED,
        'folders_dirty': False,
    }

    # Per-folder outcomes collected for the end-of-run summary (and for the
    # cross-folder partial_success aggregation under --auto).
    folder_outcomes = []

    if args.auto:
        ######## ----  R18 feature layer: --auto mode ---- #######
        if not USAGE_FOLDERS_PROCESSED:
            # Brand-new install -- nothing to walk. Not a failure; just an
            # informational no-op.
            logger.warning("--auto invoked but USAGE_FOLDERS_PROCESSED is empty; nothing to do. Seed folders with one manual --folder=NAME run first.")
            print_color(
                textcolor="yellow",
                msg=(
                    "NOTE: --auto invoked but no folders are seeded yet.\n"
                    "    Seed each folder with one manual run first:\n"
                    "        gitmynotes --folder=YourFolder --max-notes=1\n"
                    "    Then '--auto' will pick up changes from there onward."
                ),
                addseparator=True,
            )
        else:
            for folder, watermark_iso in list(USAGE_FOLDERS_PROCESSED.items()):
                print_color(textcolor="cyan", msg=f"\n>>> --auto: finding new notes in folder '{folder}' (date>{watermark_iso or 'none'})", addseparator=True)
                if not watermark_iso:
                    # Null-watermark folder -- skip with a yellow warning per
                    # the R18 design. User must seed manually first so we know
                    # what window of changes we should be looking at.
                    logger.warning(f"--auto: skipping folder '{folder}' -- watermark is null (seed with: gitmynotes --folder={folder}).")
                    print_color(
                        textcolor="yellow",
                        msg=(
                            f"SKIP: '{folder}' has no recorded watermark.\n"
                            f"    Seed it with one manual run first:\n"
                            f"        gitmynotes --folder={folder} --max-notes=1\n"
                            f"    Then this folder will be picked up by --auto."
                        ),
                    )
                    folder_outcomes.append({'folder': folder, 'status': 'skipped-null-watermark', 'partial': False, 'notes_processed': 0})
                    continue

                count_modified = count_notes_modified_since(folder, watermark_iso, args.notes_account)
                if count_modified == 0:
                    print_color(textcolor="cyan", msg=f"    No changes since watermark for '{folder}'; nothing to do.")
                    folder_outcomes.append({'folder': folder, 'status': 'no-changes', 'partial': False, 'notes_processed': 0})
                    continue

                print_color(textcolor="white", msg=f"    {count_modified} note(s) modified since watermark in '{folder}'.")
                try:
                    outcome = process_one_folder(
                        folder=folder,
                        max_notes_request=count_modified,
                        args=args,
                        run_config=run_config,
                        run_state=run_state,
                        skip_5x_confirm=True,
                    )
                except Exception as exc:
                    # R18 design: per-folder failure isolation under --auto.
                    # One stale folder shouldn't black-hole the others. Log
                    # with traceback, mark as hard-failed-demoted (counts as
                    # partial in the aggregate exit code), and continue to the
                    # next folder.
                    logger.exception(f"--auto: hard failure processing folder '{folder}': {exc}")
                    print_color(
                        textcolor="red",
                        msg=f"FAILED: '{folder}' raised an exception during processing -- skipping to next folder. Check gitmynotes.log for traceback.",
                        addseparator=True,
                    )
                    folder_outcomes.append({'folder': folder, 'status': 'hard-failed-demoted', 'partial': True, 'notes_processed': 0})
                    continue

                status = 'partial' if outcome['partial'] else 'clean'
                folder_outcomes.append({
                    'folder': folder,
                    'status': status,
                    'partial': outcome['partial'],
                    'notes_processed': outcome['notes_processed'],
                })
    else:
        ######## ----  Non-auto path: single folder per the original CLI contract ---- #######
        outcome = process_one_folder(
            folder=args_folder,
            max_notes_request=args_max_notes,
            args=args,
            run_config=run_config,
            run_state=run_state,
            skip_5x_confirm=False,
        )

        if outcome['aborted_by_user']:
            # Clean user-initiated abort at the 5x-batch confirm. Nothing was
            # exported, no git ops, no yaml writes. Exit 0 per the cross-cutting
            # taxonomy.
            sys.exit(EXIT_SUCCESS)

        status = 'partial' if outcome['partial'] else 'clean'
        folder_outcomes.append({
            'folder': args_folder,
            'status': status,
            'partial': outcome['partial'],
            'notes_processed': outcome['notes_processed'],
        })


    ######## ----  Run-level usage updates + single yaml write    ---- #######
    # B6 + R10: increment USAGE_GITMYNOTES_TOTAL once per run that did real
    # work, then flush all usage counters in a single yaml write per run. The
    # "did real work" gate is now "any folder processed >0 notes." A run that
    # touched zero notes (empty folder, --max-notes 0, --auto with all folders
    # null/no-changes) doesn't bump the run counter or touch the yaml, matching
    # the prior behavior.
    total_notes_this_run = sum(o['notes_processed'] for o in folder_outcomes)
    USAGE_GITMYNOTES_TOTAL_NEW = int(USAGE_GITMYNOTES_TOTAL)
    USAGE_NOTES_PROCESSED_NEW = run_state['USAGE_NOTES_PROCESSED']

    if total_notes_this_run > 0:
        USAGE_GITMYNOTES_TOTAL_NEW = int(USAGE_GITMYNOTES_TOTAL) + 1
        usage_updates = {
            'USAGE_GITMYNOTES_TOTAL': USAGE_GITMYNOTES_TOTAL_NEW,
            'USAGE_NOTES_PROCESSED': USAGE_NOTES_PROCESSED_NEW,
        }
        if run_state['folders_dirty']:
            usage_updates['USAGE_FOLDERS_PROCESSED'] = run_state['USAGE_FOLDERS_PROCESSED']
        update_yaml_config_multi('./gmn_config.yaml', usage_updates)
    elif run_state['folders_dirty']:
        # Edge case: an --auto run might have advanced folders_dirty (e.g. a
        # newly-seeded folder added to the mapping with null watermark) without
        # actually exporting any notes. Flush the folder-mapping change without
        # bumping the run counter.
        update_yaml_config_multi('./gmn_config.yaml', {'USAGE_FOLDERS_PROCESSED': run_state['USAGE_FOLDERS_PROCESSED']})


    ######## ----  Final messaging + exit code    ---- #######
    # partial_success aggregates across all folders. Any partial signal -- B1,
    # git, move, or a hard-failed-demoted folder under --auto -- flips it to
    # True so the run exits with EXIT_PARTIAL_SUCCESS.
    partial_success = any(o['partial'] for o in folder_outcomes)

    share_url = "Get More with GitMyNotes Pro: https://GitMyNotes.com"

    if args.auto:
        # Aggregate auto-mode summary. Lists each folder's outcome plus the
        # usage totals so the user (or a Cowork routine reading the output)
        # can see at a glance what happened.
        summary_lines = ["GitMyNotes --auto run complete!\n"]
        if folder_outcomes:
            summary_lines.append("    Per-folder outcomes:")
            for o in folder_outcomes:
                summary_lines.append(f"      - {o['status']:<24} {o['folder']} ({o['notes_processed']} note(s) exported)")
        else:
            summary_lines.append("    No folders processed (USAGE_FOLDERS_PROCESSED is empty).")
        summary_lines.append("")
        summary_lines.append(f"    Runs::Folders::Notes: {int(USAGE_GITMYNOTES_TOTAL_NEW)}::{len(USAGE_FOLDERS_PROCESSED)}::{int(USAGE_NOTES_PROCESSED_NEW)}")
        summary_lines.append("")
        if share_url:
            summary_lines.append("    - Tell your friends, learn more: https://GitMyNotes.com/")
        print_color(textcolor="cyan", msg="\n".join(summary_lines), addseparator=True)
    else:
        # Non-auto: existing single-folder final_msg.
        single = folder_outcomes[0] if folder_outcomes else None
        if single:
            if args_wrapper_dir:
                final_gitnotes_url = f"{DEFAULT_GITHUB_URL}/tree/main/{args_wrapper_dir}/{single['folder']}"
            else:
                final_gitnotes_url = f"{DEFAULT_GITHUB_URL}/tree/main/{single['folder']}"
            audit_file = f"./{single['folder']}{args.audit_file_ending}"
            usage_totals = [int(USAGE_GITMYNOTES_TOTAL_NEW), len(USAGE_FOLDERS_PROCESSED), int(USAGE_NOTES_PROCESSED_NEW)]
            final_msg = build_final_msg(gitnotes_url=f"{final_gitnotes_url}", audit_file=f"{audit_file}", usage_totals=usage_totals, share_url=f"{share_url}")
            print_color(textcolor="cyan", msg=f"{final_msg}", addseparator=True)

    # Final exit per the cross-cutting taxonomy. Hard-failure paths (B10 guard,
    # B8 ChangeMe fail-fast) sys.exit(EXIT_HARD_FAILURE) directly and never
    # reach here. The 'x' confirm-exit also routes around this with
    # EXIT_SUCCESS. So at this point the run did its work; we just need to
    # tell the caller whether anything was less-than-clean.
    sys.exit(EXIT_PARTIAL_SUCCESS if partial_success else EXIT_SUCCESS)




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