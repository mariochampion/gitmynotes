<div><b>Creation Date:</b> Sunday, December 29, 2024 at 11:26:37 AM<br></div>
<div><b>Modification Date:</b> Friday, January 10, 2025 at 8:44:35 PM<br></div>
<div><h1>I Made a Drop-In Wrapper For `argparse` That Automatically Creates a GUI Interface</h1></div>
<div><br></div>
<div>Showcase 2024-12-28 18:27:12 CST</div>
<div><br></div>
<div>## What My Project Does</div>
<div><br></div>
<div>Since I end up using Python 3's built-in `argparse` a lot in my projects and have received many requests from downstream users for GUI interfaces, I created a package that wraps an existing `Parser` and generates a terminal-based GUI for it.</div>
<div>If you include the `--gui` flag (by default), it opens an interface using [Textual](https://github.com/Textualize/textual) which includes mouse support (in all the terminals I've tested).</div>
<div>The best part is that you can still use the regular command line interface as usual if you'd prefer.</div>
<div><br></div>
<div>Using the large demo parser I typically use for testing, it looks like this:</div>
<div><br></div>
<div>https://github.com/Sorcerio/Argparse-Interface/blob/master/assets/ArgUIDemo_small.gif?raw=true </div>
<div><br></div>
<div>Currently, ArgUI supports:</div>
<div>- Text input (`str`, `int`, `float`).</div>
<div>- `nargs` arguments with styled list inputs.</div>
<div>- Booleans (with switches).</div>
<div>- Groups (exclusive and named).</div>
<div>- Subparsers.</div>
<div><br></div>
<div>Which, as far as I can tell, encompases the full suite of base-level `argparse` inputs.</div>
<div><br></div>
<div>## Target Audience</div>
<div><br></div>
<div>This project is designed for anyone who uses Python's `argparse` in their command-line applications and would like a more user-friendly terminal interface with mouse support.</div>
<div>It is good for developers who want to add a GUI to their existing CLI tools without losing the flexibility and power of the command line.</div>
<div><br></div>
<div>Right now, I would suggest using it for non-enterprise development until I can test the code across a _large_ variety of `argparse.Parser` configurations.</div>
<div>But, in the testing I've done across the ones in my portfolio, I've had great success.</div>
<div><br></div>
<div>## Comparison</div>
<div><br></div>
<div>This project differentiates itself from existing solutions by integrating a terminal-based GUI directly into the `argparse` framework.</div>
<div>Most GUI alternatives for CLI tools require external applications (like a web interface) and/or block the user out of using the CLI entirely.</div>
<div>In contrast, this package allows you to keep the simplicity and power of `argparse` while offering a GUI option through the `--gui` flag.</div>
<div>And since it uses [Textual](https://github.com/Textualize/textual) for UI rendering, these interfaces can even be used through an SSH connection.</div>
<div>The inclusion of mouse support, the ability to maintain command-line usability, and integration with the Textual library set it apart from other GUI frameworks that aren't designed for terminal use.</div>
<div><br></div>
<div>## Future Ideas</div>
<div><br></div>
<div>I’m considering adding specialized input features.</div>
<div>An example of which would be a `str` input to be identified as a file path, which would open a file browser in the GUI.</div>
<div><br></div>
<div>---</div>
<div><br></div>
<div>If you want to try it, it's available on [GitHub](https://github.com/Sorcerio/Argparse-Interface ) and [PyPi](https://pypi.org/project/Argparse-Interface/).</div>
<div><br></div>
<div>And if you like it (or don't), let me know!</div>
<div><br></div>
<div><br></div>
<div>passwordwork</div>
<div><br></div>
<div>https://www.reddit.com/r/Python/comments/1hojk2a/i_made_a_dropin_wrapper_for_argparse_that/</div>

