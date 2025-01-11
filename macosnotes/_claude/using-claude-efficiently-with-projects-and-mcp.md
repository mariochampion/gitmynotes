<div><b>Creation Date:</b> Tuesday, December 17, 2024 at 9:14:35 PM<br></div>
<div><b>Modification Date:</b> Tuesday, December 17, 2024 at 9:14:35 PM<br></div>
<div><h1>Using Claude efficiently with Projects and MCP</h1></div>
<div><br></div>
<div>Feature: Claude Projects 2024-12-17 08:22:36 CST</div>
<div><br></div>
<div>I have recently started using the Claude desktop app on Windows 11 and enabled a few MCP servers. The git plugin is not working, but I haven't bothered fixing it yet. The memory and filesystem plugins have really elevated Claude's usefulness. I don't let it write directly to my filesystem most of the time, but using all other capabilities provided by the memory and filesystem plugin. My problem is I keep hitting the message limit alot faster, multiple times per day.   </div>
<div><br></div>
<div><br></div>
<div>&ampgt;Message limit reached for Claude 3.5 Sonnet until 11 [AM.You](http://AM.You) may still be able to continue on Claude 3.5 Haiku</div>
<div><br></div>
<div>Has anyone found strategies for dealing with this? I'm on the $20/month pro plan. I also have typingmind which I use with Claude tokens mostly, but as far as I know you can't use the Claude API via typingmind and also use the MCP servers. Please correct me if I'm wrong. I tend to switch over to my token/api usage setup on typingmind when I get rate limited from the desktop client with these plugins enabled. </div>
<div><br></div>
<div>I've been thinking about enabling the brave search, but suspect that'll make me get rate limited even faster for every plugin I enable. </div>
<div><br></div>
<div>    {</div>
<div>      &quotmcpServers&quot: {</div>
<div>        &quotfilesystem&quot: {</div>
<div>          &quotcommand&quot: &quotnode&quot,</div>
<div>          &quotargs&quot: [</div>
<div>            &quotC:/Users/MaximumGuide/AppData/Roaming/npm/node_modules/@modelcontextprotocol/server-puppeteer/dist/index.js&quot,</div>
<div>            &quotC:/&quot</div>
<div>          ]</div>
<div>        },</div>
<div>        &quotfilesystem&quot: {</div>
<div>          &quotcommand&quot: &quotnpx&quot,</div>
<div>          &quotargs&quot: [</div>
<div>            &quot-y&quot,</div>
<div>            &quot@modelcontextprotocol/server-filesystem&quot,</div>
<div>            &quotC:/Users/MaximumGuide/code&quot,</div>
<div>            &quot//wsl.localhost/Ubuntu-22.04/home/MaximumGuide/git/homelab&quot</div>
<div>          ]</div>
<div>        },</div>
<div>        &quotgit&quot: {</div>
<div>          &quotcommand&quot: &quotpython&quot,</div>
<div>          &quotargs&quot: [&quot-m&quot, &quotmcp_server_git&quot, &quot--repository&quot, &quot//wsl.localhost/Ubuntu-22.04/home/MaximumGuide/git/homelab&quot]</div>
<div>        },</div>
<div>        &quotkubernetes&quot: {</div>
<div>          &quotcommand&quot: &quotnpx&quot,</div>
<div>          &quotargs&quot: [&quotmcp-server-kubernetes&quot]</div>
<div>        },</div>
<div>        &quotmemory&quot: {</div>
<div>          &quotcommand&quot: &quotnpx&quot,</div>
<div>          &quotargs&quot: [</div>
<div>            &quot-y&quot,</div>
<div>            &quot@modelcontextprotocol/server-memory&quot</div>
<div>          ]</div>
<div>        }</div>
<div>      }</div>
<div>    }</div>
<div>    {</div>
<div>      &quotmcpServers&quot: {</div>
<div>        &quotfilesystem&quot: {</div>
<div>          &quotcommand&quot: &quotnode&quot,</div>
<div>          &quotargs&quot: [</div>
<div>            &quotC:/Users/MaximumGuide/AppData/Roaming/npm/node_modules/@modelcontextprotocol/server-puppeteer/dist/index.js&quot,</div>
<div>            &quotC:/&quot</div>
<div>          ]</div>
<div>        },</div>
<div>        &quotfilesystem&quot: {</div>
<div>          &quotcommand&quot: &quotnpx&quot,</div>
<div>          &quotargs&quot: [</div>
<div>            &quot-y&quot,</div>
<div>            &quot@modelcontextprotocol/server-filesystem&quot,</div>
<div>            &quotC:/Users/MaximumGuide/code&quot,</div>
<div>            &quot//wsl.localhost/Ubuntu-22.04/home/MaximumGuide/git/homelab&quot</div>
<div>          ]</div>
<div>        },</div>
<div>        &quotgit&quot: {</div>
<div>          &quotcommand&quot: &quotpython&quot,</div>
<div>          &quotargs&quot: [&quot-m&quot, &quotmcp_server_git&quot, &quot--repository&quot, &quot//wsl.localhost/Ubuntu-22.04/home/MaximumGuide/git/homelab&quot]</div>
<div>        },</div>
<div>        &quotkubernetes&quot: {</div>
<div>          &quotcommand&quot: &quotnpx&quot,</div>
<div>          &quotargs&quot: [&quotmcp-server-kubernetes&quot]</div>
<div>        },</div>
<div>        &quotmemory&quot: {</div>
<div>          &quotcommand&quot: &quotnpx&quot,</div>
<div>          &quotargs&quot: [</div>
<div>            &quot-y&quot,</div>
<div>            &quot@modelcontextprotocol/server-memory&quot</div>
<div>          ]</div>
<div>        }</div>
<div>      }</div>
<div>    }</div>
<div><br></div>
<div><br></div>
<div><br></div>
<div>MaximumGuide</div>
<div><br></div>
<div>https://www.reddit.com/r/ClaudeAI/comments/1hgbog2/using_claude_efficiently_with_projects_and_mcp/</div>

