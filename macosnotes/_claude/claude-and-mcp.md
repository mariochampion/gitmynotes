<div><b>Creation Date:</b> Monday, December 2, 2024 at 5:54:25 PM<br></div>
<div><b>Modification Date:</b> Tuesday, December 17, 2024 at 8:23:04 PM<br></div>
<div><h1>claude and mcp </h1><h1><br></h1></div>
<div><br></div>
<div>Also a video on setting this up with brave search API and gut hub<br></div>
<div><br></div>
<div>https://www.youtube.com/watch?v=2BBmymwJzIc<br></div>
<div>https://shaneemoret.notion.site/Claude-MCP-YouTube-Video-15261ef8860f8042a0abce41a1420928 <br></div>
<div><br></div>
<div><br></div>
<div>Claude and github integration (per anthropic)<br></div>
<div>https://support.anthropic.com/en/articles/10167454-using-the-github-integration<br></div>
<div><br></div>
<div><br></div>
<div>And a Claude map githb example from /allaboutai YouTube <br></div>
<div>https://www.youtube.com/watch?v=FiirOCVrPOk<br></div>
<div><br></div>
<div><br></div>
<div><br></div>
<div><a href=https://www.anthropic.com/news/model-context-protocol>https://www.anthropic.com/news/model-context-protocol</a><br></div>
<div><br></div>
<div><br></div>
<div>node --version;npm --version</div>
<div><br></div>
<div>mkdir -p ~/.claude/servers;touch ~/.claude/servers/claude-desktop-config.json</div>
<div><br></div>
<div>open ~/.claude/servers/claude-desktop-config.json</div>
<div><br></div>
<div>{</div>
<div>  &quotmcpServers&quot: {</div>
<div>    &quotbrave-search&quot: {</div>
<div>      &quotcommand&quot: &quotnpx&quot,</div>
<div>      &quotargs&quot: [&quot-y&quot, &quot@modelcontextprotocol/server-brave-search&quot],</div>
<div>      &quotenv&quot: {</div>
<div>        &quotBRAVE_API_KEY&quot: &quotBSANwUs1f-dBfELy0iANGjJn7DMkfKA&quot</div>
<div>      }</div>
<div>    },</div>
<div>    &quotgithub&quot: {</div>
<div>      &quotcommand&quot: &quotnpx&quot,</div>
<div>      &quotargs&quot: [&quot-y&quot, &quot@modelcontextprotocol/server-github&quot],</div>
<div>      &quotenv&quot: {</div>
<div>        &quotGITHUB_PERSONAL_ACCESS_TOKEN&quot: &quot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&quot</div>
<div>      }</div>
<div>    }</div>
<div>  }</div>
<div>}</div>

