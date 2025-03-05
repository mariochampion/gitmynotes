# GitMyNotes

## to do

### bugs

* mention when locked notes are encountered and the content is NOT sent to github, but a stub file is, with just the title and mod/create dates


### prep for release (technical)

* final names for everything

* make sure the .gitignore is correct

* write some measure of real instructions

* start fresh like new user, track issues, see what claude can do?

* guide to help set up cron job




### SCRAPER/FETCHER ENHANCEMENTS

#### [OSS] 

* move all of scraper/prefetch/fetch to reddit_config.yaml

* allow for random scraper dir name and path

* scraper/fetcher dir with reddit 

#### [PRO] 

* optional other scrapers/fetchers

* make generic scraper, depending on url (each one a separate file so others can contribute)

* auto-populate prefetch yaml from dirs if X conditions met (less than MINIMUM_WORD_COUNT words, etc)




### OTHER ENHANCEMENTS

#### [OSS] 


* [terminal only] auto-discover Notes dirs and list them as options for choosing, with "Notes" as default

* ?? `--properties` option to show the settings, so dont have to look thru, and option to set that via cli ??

* get someone to write tests!!



#### [PRO] 

* [via TUI] auto-discover Notes dirs and list them as options for choosing, with "Notes" as default

* allow comma separated list of folders at once -- or based on list in the USAGE_FOLDERS_PROCESSED in config yaml, 
process them allwith default number or set --maxnotes

* command to get list of folders and counts so you can decide what to do

* check LAST bkup date and autocalc the --maxnotes to get them, or do the whole thing by date which would allow cron job at that interval

* option to delete __GitMyNotes folders when restored to 0

* desktop claude MCP to review/tag collected notes works, move to python and anthropic api

* improve msg about access rights including steps for GH PAT and implementing it on mac. 

* allow optionally `git push` the audit file as well

* config to trigger via cron or... automator?

* create self executing mac shell command to wrap around python script. 

* create a github for non-devs one-pager? video? 

* default "_ignore" folder, so when user selects "all folders" it gets skipped

* licensing??




