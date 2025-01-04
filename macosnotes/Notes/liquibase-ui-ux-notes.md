<div><b>Creation Date:</b> Saturday, March 7, 2020 at 1:44:33 PM<br></div>
<div><b>Modification Date:</b> Friday, November 8, 2024 at 7:03:17 PM<br></div>
<div><h1>LIQUIBASE UI UX notes</h1></div>
<div><span style="font-size: 14px"><br></span></div>
<div><span style="font-size: 14px">mariochampion@mmc: ls</span></div>
<div><span style="font-size: 14px">flyway-6.2.4				lbaseghub				liquibase-macos-installer-3.8.7.dmg</span></div>
<div><span style="font-size: 14px">------------------------------------------------------------------------------------------------------------------------------------------------ 13:47:01</span></div>
<div><span style="font-size: 14px">mariochampion@mmc: mkdir liquibase</span></div>
<div><span style="font-size: 14px">------------------------------------------------------------------------------------------------------------------------------------------------ 13:47:05</span></div>
<div><span style="font-size: 14px">mariochampion@mmc: cd liquibase</span></div>
<div><span style="font-size: 14px">------------------------------------------------------------------------------------------------------------------------------------------------ 13:47:10</span></div>
<div><span style="font-size: 14px">mariochampion@mmc: ls</span></div>
<div><span style="font-size: 14px">------------------------------------------------------------------------------------------------------------------------------------------------ 13:47:11</span></div>
<div><span style="font-size: 14px">mariochampion@mmc: mkdir 3.8.7</span></div>
<div><span style="font-size: 14px">------------------------------------------------------------------------------------------------------------------------------------------------ 13:47:21</span></div>
<div><span style="font-size: 14px">mariochampion@mmc: cd 3.8.7/</span></div>
<div><span style="font-size: 14px">------------------------------------------------------------------------------------------------------------------------------------------------ 13:47:25</span></div>
<div><span style="font-size: 14px">mariochampion@mmc: ls</span></div>
<div><span style="font-size: 14px">------------------------------------------------------------------------------------------------------------------------------------------------ 13:47:25</span></div>
<div><span style="font-size: 14px">mariochampion@mmc: ls</span></div>
<div><span style="font-size: 14px">examples</span></div>
<div><span style="font-size: 14px">------------------------------------------------------------------------------------------------------------------------------------------------ 13:48:22</span></div>
<div><span style="font-size: 14px">mariochampion@mmc: examples/start-h2</span></div>
<div><span style="font-size: 14px">Must set LIQUIBASE_HOME environment variable, or have liquibase in your PATH</span></div>
<div><span style="font-size: 14px">------------------------------------------------------------------------------------------------------------------------------------------------ 13:48:31</span></div>
<div><span style="font-size: 14px">mariochampion@mmc: echo $PATH</span></div>
<div><span style="font-size: 14px">/Users/marioairchampion/anaconda2/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</span></div>
<div><span style="font-size: 14px"><br></span></div>
<div><b><span style="font-size: 14px">ISSUE: Must set LIQUIBASE_HOME environment variable, or have liquibase in your PATH</span></b></div>
<div><span style="font-size: 14px"> - I thought I checked the box during install to have it in my path </span><b><span style="font-size: 14px">— BUG???</span></b></div>
<div><b><span style="font-size: 14px"><br></span></b></div>
<div><b><span style="font-size: 14px">ISSUE: when I google the error message I get WINDOWs page: </span></b><u>https://www.liquibase.org/documentation/installation-windows.html</u><u><br></u></div>
<ul class="Apple-dash-list">
<li>Did adjust my google search and find <font color="#E4AF0A">https://www.liquibase.org/documentation/installation-linux-unix-mac.html</font><u><br></u></li>
</ul>
<div><b><span style="font-size: 14px"><br></span></b></div>
<div><b><span style="font-size: 14px">ISSUE: Add link to GETTING STARTED to help people set their path for Mac and Win</span></b></div>
<div><span style="font-size: 14px"> — answer : I added liquibsse to path via profile (nano ~/.bash_profile)</span></div>
<div><span style="font-size: 14px">— THEN I could keep on with the GETTING STARTED</span><b><span style="font-size: 14px"><br></span></b></div>
<div><br></div>
<div><br></div>
<div><b><span style="font-size: 14px">ISSUE: when I run a command such as generatechangelog, and get a message: </span></b></div>
<div><span style="font-size: 14px">mariochampion@mmc: liquibase generatechangelog</span></div>
<div><span style="font-size: 14px">Liquibase Community 3.8.7 by Datical</span></div>
<div><span style="font-size: 14px">Errors:</span></div>
<div><span style="font-size: 14px">  The option --url is required.</span></div>
<div><span style="font-size: 14px">  The option --changeLogFile is required.</span><br></div>
<div><br></div>
<div><span style="font-size: 16px">Then I cannot run </span><b><span style="font-size: 16px">liquidate generatechangelog —help</span></b></div>
<div><span style="font-size: 16px">But also I do not know what these options mean.</span><b><span style="font-size: 16px"><br></span></b></div>
<div><b><span style="font-size: 16px"><br></span></b></div>
<div><b><span style="font-size: 16px">ISSUE: standardized “options” and “parameters”. </span></b></div>
<div><b><span style="font-size: 16px"> — </span></b><span style="font-size: 16px">As seen in the above message and end of —help:  “Default value for parameters can be stored in a file called</span></div>
<div><span style="font-size: 16px">'liquibase.properties' that is read from the current working directory.	”</span></div>
<div><span style="font-size: 16px"><br></span></div>
<div><span style="font-size: 16px"><br></span></div>
<div><b><span style="font-size: 16px">ISSUE: reforms all of —help</span></b><span style="font-size: 16px"><br></span></div>
<div><span style="font-size: 16px">— so that there are examples at least</span></div>
<div><span style="font-size: 16px">— but also is this the best layout? Likely not!</span></div>
<div><span style="font-size: 16px"><br></span></div>
<div><span style="font-size: 16px"><br></span></div>
<div><span style="font-size: 16px"><br></span></div>
<div><b><span style="font-size: 16px">ISSUE: “Liquibase Community 3.8.7 by Datical” should have a link to help/docs:</span></b><span style="font-size: 16px"><br></span></div>
<div><span style="font-size: 16px">	— Liquibase Community 3.8.7 by Datical. Learn more at </span><font color="#E4AF0A"><span style="font-size: 16px">http://docs.liquibase.org</span></font><span style="font-size: 16px">”</span></div>
<div><span style="font-size: 16px"><br></span></div>
<div><span style="font-size: 16px"><br></span></div>
<div><span style="font-size: 16px"><br></span></div>
<div><b><span style="font-size: 16px">Issue: liquibase.properties should really be liquibase.parameters or liquibase.commands.configs or ??</span></b><span style="font-size: 16px"><br></span></div>
<div><span style="font-size: 16px"><br></span></div>
<div><span style="font-size: 16px"><br></span></div>
<div><br></div>

