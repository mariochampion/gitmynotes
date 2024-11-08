# notesdump
python and applescript to back up macOS notes

## to do
write real instructions


## Usage



## Getting Started

### Prerequisites
1. MacOS Notes app
2. Python 3.x+
3. Applescript (should be on all Macs)


## Steps
1. clone the repo: `git clone https://github.com/mariochampion/notesdump.git`

2. cd into notesdump dir: `cd notesdump`

3. in file `notesdumper.py`, 

	set `DEFAULT_EXPORT_PATH` to the export location (example: `DEFAULT_EXPORT_PATH = "~/Documents/<SomeFolder>"`)
	
	set `DEFAULT_GITHUB_URL` to the the repo where you want to store Notes (example: `DEFAULT_GITHUB_URL = "https://github.com/<myusername>/<myrepo>""`)
	
4. open terminal and cd to `notesdump` dir

5. run `python3 notesdumper.py --folder='<notesFolderName>' --max-notes <N> `

`--folder` is optional

`--max-notes` is optional
 









