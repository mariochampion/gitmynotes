<div><b>Creation Date:</b> Thursday, May 12, 2022 at 8:01:32 AM<br></div>
<div><b>Modification Date:</b> Thursday, May 12, 2022 at 8:30:24 AM<br></div>
<div><h1>Syscloud - 12 may 2022</h1></div>
<div><br></div>
<div>What is going on with them?</div>
<div><br></div>
<div>What is the value you get from hub?</div>
<div>What do you use, what do you not?</div>
<div>Has anything changed lately?</div>
<div>Any info on the 500 error?</div>
<div><br></div>
<div><b><u>syscloud: an was infrastructure setup, deploy with SQL</u></b><br></div>
<div><br></div>
<div>use hub meta mode.</div>
<div>Thought initially maybe size, but that doesn’t seem to be it.</div>
<div><br></div>
<div>rajarsi: 7 to 8 servers, deploy to all at once, but sequentially for the data</div>
<div><br></div>
<div>But hard to replicate.</div>
<div><br></div>
<div>Mostly schema changes. STOLO function changes, sometime a few are DDL. And usually just 3 or 4 change sets.</div>
<div><br></div>
<div>Why use hub?</div>
<div>To see which change sets failed to deploy. To see if mistakes, like syntax. So operation reports</div>
<div><br></div>
<div>not a specific db that fails, it can succeed the very next time.</div>
<div><br></div>
<div>What triggers an update? Is it parallel or sequential? In parallel in 5 servers at once to get to 1000 dbs at once. How long does this take 1 to 2 hours to get to all 1000 DBs. Multiple batches cannot be run at once, done from code pipeline as executions wait for the previous to finish. BUT can till have 5 servers at once.</div>
<div><br></div>
<div>Remove hub and drops to 1/2 time (with hub takes 2x as long)</div>
<div><br></div>
<div>Migrating from MSSQL to PG, so would like to speed up. For next 2 months a similar pace, then after that it would be a 10% growth month on month, perhaps.</div>
<div><br></div>
<div><br></div>
<div><b><u>ASK: add materialized views in diff pro output</u></b></div>
<div><b><u>ASK: add diff report to hub</u></b></div>

