<div><b>Creation Date:</b> Thursday, December 5, 2024 at 11:07:00 PM<br></div>
<div><b>Modification Date:</b> Thursday, December 5, 2024 at 11:07:00 PM<br></div>
<div><h1>If I don't share, no one will know</h1></div>
<div><br></div>
<div>Gone Wild  2024-12-05 07:54:08 CST</div>
<div><br></div>
<div>I'm just very impressed by this little task I achieved at work and no one at work will care how I achieved it. So, I have to share it. Someone please say wow that's cool UwU or something before I die a little more inside.</div>
<div><br></div>
<div>We teach using OneNote and have licences for offline (PDF) versions of our textbooks. If you drop the whole textbook into a OneNote page you lose all navigation convenience. So, I split the textbook into separate PDFs by section all named properly and starting with a sequential number to keep them in order. About 180 separate PDFs per textbook. Manually doing this would have been an egregious waste of my talents. But I could not have done this without ChatGPT since my Python skills are definitely not up to the task.</div>
<div><br></div>
<div>Here is the workflow.</div>
<div><br></div>
<div>1. Drag the TOC out from Acrobat into the desktop.  </div>
<div>2. Ask ChatGPT to extract the table of contents with page numbers.  </div>
<div>3. Open this in VS Code and tidy up.  </div>
<div>4. Use multi-cursor select to extract the page numbers.  </div>
<div>5. Use Excel to add 17 to each page number and copy back to VS Code (print page numbers out of sync with PDF pages).  </div>
<div>6. Manually add page numbers for preliminary sections.  </div>
<div>7. Multi-cursor again to make it a comma-separated list.  </div>
<div>8. Split PDF using PDFSam (using the comma-separated list) and output 1.pdf, 2.pdf etc.  </div>
<div>9. Save to a local directory because PowerShell scripts won't run on company shared drive locations. (I tried to bypass that a few too many times but gave up eventually.)  </div>
<div>10. More Excel and multi-cursor work in VS Code to make a text file with the new file names.  </div>
<div>11. PowerShell renaming script from ChatGPT. (Only three iterations to get it working, and it even outputs the file name changes or errors it encounters. Also changes disallowed characters to hyphens.)  </div>
<div>12. Copy them back to shared drive location.  </div>
<div>13. Share folder link with team by email with no self-congratulatory language.</div>
<div><br></div>
<div>When it worked I honestly felt like Neo or Aang or something. I may have strutted a little.</div>
<div><br></div>
<div>clericrobe</div>
<div><br></div>
<div>https://www.reddit.com/r/ChatGPT/comments/1h79obn/if_i_dont_share_no_one_will_know/</div>

