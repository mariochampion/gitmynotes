<div><b>Creation Date:</b> Friday, December 6, 2024 at 7:34:35 AM<br></div>
<div><b>Modification Date:</b> Friday, December 6, 2024 at 7:34:35 AM<br></div>
<div><h1>Claude can now Google stuff, tell you the news, and do deep web research on any topic</h1></div>
<div><br></div>
<div>Feature: Claude Model Context Protocol 2024-12-05 23:57:44 CST</div>
<div><br></div>
<div>https://preview.redd.it/gfargrx4465e1.png?width=1532&ampamp;format=png&ampamp;auto=webp&ampamp;s=ef5a7e728912a316e2930e7ed945c807681e7cb7</div>
<div><br></div>
<div>Just released a super early version of an MCP server for web research [on Github](https://github.com/mzxrai/mcp-webresearch).</div>
<div><br></div>
<div>It lets you (from Claude Desktop)...</div>
<div><br></div>
<div>* Google stuff and visit any webpage + extract the content</div>
<div>* Do deep web research on any topic</div>
<div>* Get latest news, weather, etc.</div>
<div><br></div>
<div>You can only use it via Claude Desktop currently since MCP support is limited to desktop.   </div>
<div>  </div>
<div>Install it on Mac by adding this to your `~/Library/Application\ Support/Claude/claude_desktop_config.json`</div>
<div><br></div>
<div>    {</div>
<div>      &quotmcpServers&quot: {</div>
<div>        &quotwebresearch&quot: {</div>
<div>          &quotcommand&quot: &quotnpx&quot,</div>
<div>          &quotargs&quot: [&quot-y&quot, &quot@mzxrai/mcp-webresearch&quot]</div>
<div>        }</div>
<div>      }</div>
<div>    }</div>
<div><br></div>
<div>Just make sure you have [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) installed first. Restart Claude Desktop and you should be good to go!</div>
<div><br></div>
<div>[Github repo - mcp-webresearch](https://github.com/mzxrai/mcp-webresearch)</div>
<div><br></div>
<div>mzxrai</div>
<div><br></div>
<div>https://www.reddit.com/r/ClaudeAI/comments/1h7untd/claude_can_now_google_stuff_tell_you_the_news_and/</div>

