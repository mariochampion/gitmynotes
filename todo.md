# GitMyNotes

## to do

### bugs

* mention when locked notes are encountered and the content is NOT sent to github, but a stub file is, with just the title and mod/create dates

* FIXED: * do not fail entire job when this applescript error occurs: `execution error: Notes got an error: An error of type 100002 has occurred. (100002)`, but could also be improved with loop completion



### SCRAPER ENHANCEMENTS

* scraper/fetcher dir with reddit and then optional other scrapers/fetchers

* make generic scraper, depending on url (each one a separate file so others can contribute)

* auto-populate prefetch yaml from dirs if X conditions met (less than MINIMUM_WORD_COUNT words, etc)

* allow for random scraper dir name and path




### enhancements

* auto-discover Notes dirs and list them as options for choosing, with "Notes" as default

* connect claude MCP to review collected notes

* start fresh like new user, track issues, see what claude can do?

* improve msg about access rights including steps for GH PAT and implementing it on mac. 

* ability to update user bash profile to have `alias gitmynotes='python gitmynotes.py'`

* get someone to write tests!!

* allow optionally `git push` the audit file as well

* add share code to track optional virality?

* create self executing mac shell command to wrap around python script. 

* oss users trigger/set this up via cron or... automator?


### prep for release (technical)

* final names for everything

* make sure the .gitignore is correct

* write some measure of real instructions


### pro?

* licensing??

* create a github for non-devs one-pager? video? 

* allow comma separated list of folders at once

* `--properties` option to show the settings, so dont have to look thru, and option to set that via cli

* command to get list of folders and counts so you can decide what to do

* pre-map some folders to some github repos

* add DEFAULT folder name so doesnt try to do ALL NOTES?? if none specified?

* help set up cron job?

* default ignore folder, so when user selects "all folder" it gets skipped






