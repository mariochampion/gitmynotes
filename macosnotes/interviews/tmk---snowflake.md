<div><b>Creation Date:</b> Friday, June 24, 2022 at 8:03:53 AM<br></div>
<div><b>Modification Date:</b> Friday, June 24, 2022 at 8:32:00 AM<br></div>
<div>TMK - snowflake</div>
<div><br></div>
<div>Christian - lead solution architect (tech migration and transformation)</div>
<div>Victor — data architect, lead architect </div>
<div>Former head of data architecture , banks, SI companies </div>
<div><br></div>
<div>Helping tokio marine? For data transformation program.</div>
<div><br></div>
<div>devops and dataops - where liquiabse plays key role</div>
<div><br></div>
<div>Moving from sql server to data governence, etc snowflake</div>
<div><br></div>
<div>TMK has changes scope and direction several times.</div>
<div><br></div>
<div>End of nov technical delivery go live: ready from solution perspective and then business does UAT, and run in parallel, coordinate results. Want to have dual run in dev/jan, and then switch over.</div>
<div><br></div>
<div>PROBLEM</div>
<div>Liquibase diff not working wit CLI with snowflake and use passphrase as authentication method</div>
<div>And diff is critical. So how to get it going.</div>
<div><br></div>
<div>TMK team only has a couple of problem aspects.</div>
<div><br></div>
<div>Diff does work, BUT when we use cli and auth method is username.password, but fails on passphrase with snowflake. (This isa gitlab pipeline, private key withpassphrase is passed thru the vault, passed thru to CLI)</div>
<div><br></div>
<div><u>SO REALLY AN AUTH PROBLEM</u>. Raul has the details.</div>
<div><br></div>
<div><br></div>
<div><br></div>
<div><br></div>
<div>Use cases for diff capability? Drift detection? Or?</div>
<div>Use Liquibase for all database management, starting with snowflake and the move to other relational. Use diff to identify drift detection. Primary reason. And then better control  on what is released. Make sure what devs have is managed.</div>
<div><br></div>
<div>(Question what is “drift detection” from victor)</div>
<div><br></div>
<div>Scaled agile so multiple scrum teams in parallel changing the DB.</div>
<div><br></div>
<div>“Liquibase is helping us build the confidence the db is in the state we want it to be — and manage that.” - dushyant</div>

