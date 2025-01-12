<div><b>Creation Date:</b> Thursday, April 13, 2023 at 7:27:38 AM<br></div>
<div><b>Modification Date:</b> Thursday, April 13, 2023 at 7:27:40 AM<br></div>
<div>### Liquibase v4.21.0 is a major release </div>
<div><br></div>
<div><br></div>
<div>## Notable Changes</div>
<div>### [PRO] Observability Initiative - Structured Logging</div>
<div>Structured Logging makes Liquibase operation data easily available for automated monitoring and analysis tools to read, query, and act upon in automated workflows. This feature significantly improves the way Liquibase logs its actions and events to make records machine-readable, easily-ingested, and queryable by industry-standard observability and analysis tools. Learn more at https://docs.liquibase.com/structured-logging</div>
<div><br></div>
<div><br></div>
<div>## Command refactoring</div>
<div>* Refactor update-to-tag command step (DAT-6641) by @StevenMassaro in https://github.com/liquibase/liquibase/pull/3916</div>
<div>* Refactor update-to-tag-SQL command step (DAT-6642) by @StevenMassaro in https://github.com/liquibase/liquibase/pull/3917</div>
<div>* Refactor Rollback and RollbackSQL command by @filipelautert in https://github.com/liquibase/liquibase/pull/3991</div>
<div>* Refactor ListLocksCommand by @filipelautert in https://github.com/liquibase/liquibase/pull/3952</div>
<div>* Refactor ReleaseLocksCommand by @filipelautert in https://github.com/liquibase/liquibase/pull/3953</div>
<div>* Refactoring of rollbackCount[SQL] commands by @filipelautert in https://github.com/liquibase/liquibase/pull/4077</div>
<div>* Refactor update, updateSql, updateCount, updateCountSql to use Command framework (DAT-6600/DAT-6601) by @abrackx in https://github.com/liquibase/liquibase/pull/3866</div>
<div>* Refactor update to use command framework DAT-6600 by @abrackx in https://github.com/liquibase/liquibase-pro/pull/849</div>
<div><br></div>
<div><br></div>
<div>## Enhancements</div>
<div>* [PRO] New runWithSpoolFile attribute for runWith changesets DAT-12881 by @wwillard7800 in https://github.com/liquibase/liquibase/pull/3864</div>
<div>* New update summary output table for update commands DAT-13182 by @wwillard7800 in https://github.com/liquibase/liquibase/pull/3812</div>
<div><br></div>
<div><br></div>
<div>## Security, Driver and other updates</div>
<div>* [PRO] Bump logback-classic from 1.4.5 to 1.4.6 by @dependabot in https://github.com/liquibase/liquibase-pro/pull/884</div>
<div>* [PRO] Bump flatten-maven-plugin from 1.3.0 to 1.4.0 by @dependabot in https://github.com/liquibase/liquibase-pro/pull/893</div>
<div>* [PRO] Bump postgresql from 42.5.4 to 42.6.0 by @dependabot in https://github.com/liquibase/liquibase-pro/pull/892</div>
<div>* [PRO] Bump jacoco-maven-plugin from 0.8.8 to 0.8.9 by @dependabot in https://github.com/liquibase/liquibase-pro/pull/925</div>
<div>* [PRO] Snakeyaml 2.0 by @filipelautert in https://github.com/liquibase/liquibase-pro/pull/858</div>
<div>* Bump targetMavenVersion from 3.8.7 to 3.9.0 by @dependabot in https://github.com/liquibase/liquibase/pull/3785</div>
<div>* Bump actions/cache from 3.2.6 to 3.3.0 by @dependabot in https://github.com/liquibase/liquibase/pull/3936</div>
<div>* Bump maven-plugin-plugin from 3.7.1 to 3.8.1 by @dependabot in https://github.com/liquibase/liquibase/pull/3871</div>
<div>* Bump maven-compiler-plugin from 3.10.1 to 3.11.0 by @dependabot in https://github.com/liquibase/liquibase/pull/3870</div>
<div>* Bump snowflake-jdbc from 3.13.27 to 3.13.28 by @dependabot in https://github.com/liquibase/liquibase/pull/3863</div>
<div>* Bump sqlite-jdbc from 3.40.1.0 to 3.41.0.0 by @dependabot in https://github.com/liquibase/liquibase/pull/3862</div>
<div>* Bump maven-assembly-plugin from 3.4.2 to 3.5.0 by @dependabot in https://github.com/liquibase/liquibase/pull/3</div>
<div>* Bump snowflake-jdbc from 3.13.28 to 3.13.29 by @dependabot in https://github.com/liquibase/liquibase/pull/3981</div>
<div>* Bump postgresql from 42.5.4 to 42.6.0 by @dependabot in https://github.com/liquibase/liquibase/pull/3982</div>
<div>* Bump maven-resources-plugin from 3.3.0 to 3.3.1 by @dependabot in https://github.com/liquibase/liquibase/pull/4025</div>
<div>* Bump mariadb-java-client from 3.1.2 to 3.1.3 by @dependabot in https://github.com/liquibase/liquibase/pull/4006</div>
<div>* Bump slf4j-jdk14 from 2.0.6 to 2.0.7 by @dependabot in https://github.com/liquibase/liquibase/pull/3979</div>
<div>* Bump targetMavenVersion from 3.9.0 to 3.9.1 by @dependabot in https://github.com/liquibase/liquibase/pull/3980</div>
<div>* Bump actions/cache from 3.3.0 to 3.3.1 by @dependabot in https://github.com/liquibase/liquibase/pull/3948</div>
<div>* Bump maven-deploy-plugin from 3.1.0 to 3.1.1 by @dependabot in https://github.com/liquibase/liquibase/pull/4026</div>
<div>* Bump maven-install-plugin from 3.1.0 to 3.1.1 by @dependabot in https://github.com/liquibase/liquibase/pull/4027</div>
<div>* Bump sqlite-jdbc from 3.41.0.0 to 3.41.2.1 by @dependabot in https://github.com/liquibase/liquibase/pull/4028</div>
<div>* Upgrade maven-javadoc-plugin version to 3.5.0 by @MalloD12 in https://github.com/liquibase/liquibase/pull/3973</div>
<div>* Release liquibase-cdi-jakarta to maven repositories by @DCCSKrezovic in https://github.com/liquibase/liquibase/pull/4001</div>
<div>* Upgrade spring 5 version by @filipelautert in https://github.com/liquibase/liquibase/pull/4015</div>
<div>* Snakeyaml 2.0 by @filipelautert in https://github.com/liquibase/liquibase/pull/3893</div>
<div>* Upgrade AdoptOpenJDK bundled in the JVM installer to version 17.0.6+10 by @MalloD12 in https://github.com/liquibase/liquibase/pull/3900</div>
<div><br></div>
<div><br></div>
<div><br></div>
<div>## Fixes</div>
<div>* [PRO] DAT-12881 Implement runWithSpoolFile attribute and createSpool property to control use of Oracle spooling by @wwillard7800 in https://github.com/liquibase/liquibase-pro/pull/843</div>
<div>* [PRO] DAT-12814: '--rollback-on-error' should return ERROR and return code 1 when update fails by @StevenMassaro in https://github.com/liquibase/liquibase-pro/pull/905</div>
<div>* [PRO] DAT-13968 Added missing overwrite property by @wwillard7800 in https://github.com/liquibase/liquibase-pro/pull/895</div>
<div>* [PRO] DAT-13667 Make sure exception from SQLCMD is propagated back to be displayed by @wwillard7800 in https://github.com/liquibase/liquibase-pro/pull/902</div>
<div>* [PRO] DAT-14096 Handle existence of a file extension when creating spool/sql/log files by @wwillard7800 in https://github.com/liquibase/liquibase-pro/pull/913</div>
<div>* [PRO] DAT-13994: strip leading slashes from contexts by @StevenMassaro in https://github.com/liquibase/liquibase-pro/pull/921</div>
<div>* ChangelogSync family to CommandStep refactoring by @filipelautert in https://github.com/liquibase/liquibase/pull/3859</div>
<div>* Improved concurrency support in ReflectionSerializer by @Dasiu in https://github.com/liquibase/liquibase/pull/3840</div>
<div>* Make Pattern instance variables and avoid recalculating each time by @arturobernalg in https://github.com/liquibase/liquibase/pull/3656</div>
<div>* Java 8 improvements by @arturobernalg in https://github.com/liquibase/liquibase/pull/3712</div>
<div>* Map 'double' to SQL type 'DOUBLE PRECISION' for an Oracle database (CORE-3165) by @maartenc in https://github.com/liquibase/liquibase/pull/3707</div>
<div>* Rollback Snakeyaml default config to allow duplicate keys by @filipelautert in https://github.com/liquibase/liquibase/pull/3939</div>
<div>* Upgrades snakeyaml for installer by @filipelautert in https://github.com/liquibase/liquibase/pull/3943</div>
<div>* DAT-12842 by @sayaliM0412 in https://github.com/liquibase/liquibase/pull/3909</div>
<div>* Improve use of generics in code by @arturobernalg in https://github.com/liquibase/liquibase/pull/3797</div>
<div>* DAT-12842 by @sayaliM0412 in https://github.com/liquibase/liquibase/pull/3963</div>
<div>* Performance Improvement: optimized DatabaseChangeLog.normalizePath() by @nvoxland in https://github.com/liquibase/liquibase/pull/3853</div>
<div>* Clear entries from MDC map on scope exit by @amrasarfeiniel in https://github.com/liquibase/liquibase/pull/3927</div>
<div>* [3910] fix missing OSGI manifest entries for service loaders by @jherkel in https://github.com/liquibase/liquibase/pull/3912</div>
<div>* Fixes #3734 MySQL ENUM and SET column type by @nwcm in https://github.com/liquibase/liquibase/pull/3842</div>
<div>* Change Index.setTable method to take a Relation parameter DAT-13676 by @wwillard7800 in https://github.com/liquibase/liquibase/pull/3987</div>
<div>* only set the execType to RERAN, if the changeset was actually executed by @AlexGruebel in https://github.com/liquibase/liquibase/pull/3926</div>
<div>* Create the change exec listener earlier so that it is available if there is an exception DAT-13939 by @wwillard7800 in https://github.com/liquibase/liquibase/pull/3954</div>
<div>* [3906]  Don't break Liquibase if a resolveable hostname is not found by @filipelautert in https://github.com/liquibase/liquibase/pull/3960</div>
<div>* Rename ON_MISSING_INCLUDE_FILE configuration and property names by @MalloD12 in https://github.com/liquibase/liquibase/pull/3899</div>
<div>* Load XSD files under OSGI by @ponziani in https://github.com/liquibase/liquibase/pull/3378</div>
<div>* Fixes #3083 MySQL JSON length issue by @nwcm in https://github.com/liquibase/liquibase/pull/3849</div>
<div>* Prevention of NullpointerException (unboxing) in generate-changelog with MS SQL Server by @barthel in https://github.com/liquibase/liquibase/pull/3903</div>
<div>* Issue 3619 - Allow control of recursion for includeAll via minDepth and maxDepth attributes by @jasonlyle88 in https://github.com/liquibase/liquibase/pull/3620</div>
<div>* Avoid String concatenation in loop. by @arturobernalg in https://github.com/liquibase/liquibase/pull/3668</div>
<div>* fix NullPointerException in ResourceAccessor by @StevenMassaro in https://github.com/liquibase/liquibase/pull/4040</div>
<div>* Lowers message log level. by @filipelautert in https://github.com/liquibase/liquibase/pull/4046</div>
<div>* Remove potentially sensitive information from --monitor-performance by @nvoxland in https://github.com/liquibase/liquibase/pull/3640</div>
<div>* Add mirror-console-messages-to-log parameter (DAT-13802) by @abrackx in https://github.com/liquibase/liquibase/pull/4032</div>
<div>* Do not ignore DatabaseException for Snowflake by @filipelautert in https://github.com/liquibase/liquibase/pull/4034</div>
<div>* Fix DB-Doc generation of Unique Constraints for Sybase ASE database. by @crenan in https://github.com/liquibase/liquibase/pull/3911</div>
<div>* Lowers Snakeyaml log level for warning stack traces by @filipelautert in https://github.com/liquibase/liquibase/pull/4062</div>
<div>* Remove unused parameters and local variables by @arturobernalg in https://github.com/liquibase/liquibase/pull/3857</div>
<div>* Do not show update summary for updateCountSql or updateTagSql DAT-14107 by @wwillard7800 in https://github.com/liquibase/liquibase/pull/4060</div>
<div>* add additional information to toString/describe methods of SQLFileChange (DAT-13789) by @StevenMassaro in https://github.com/liquibase/liquibase/pull/4059</div>
<div>* Update ShowSummary argument reference from CommandUtil class to fix failing integration tests by @MalloD12 in https://github.com/liquibase/liquibase/pull/4073</div>
<div>* strip leading slashes from contexts (DAT-13994) by @StevenMassaro in https://github.com/liquibase/liquibase/pull/4071</div>
<div>* Appends the table type to the statement using it. by @filipelautert in https://github.com/liquibase/liquibase/pull/4000</div>
<div>* Update runner image for pr builds (DAT-14192) by @abrackx in https://github.com/liquibase/liquibase/pull/4094</div>
<div>* Do not allow custom change types to execute twice DAT-14051 by @wwillard7800 in https://github.com/liquibase/liquibase/pull/4054</div>
<div>* Disables buffered log service if not using hub by @filipelautert in https://github.com/liquibase/liquibase/pull/3969</div>
<div>* Fixes UnsupportedOperationException thrown in SpringResourceAccessor in Spring Boot 3 Native Image by @justin-tay in https://github.com/liquibase/liquibase/pull/3959</div>
<div>* Do not repeat MDC logging by @filipelautert in https://github.com/liquibase/liquibase/pull/4088</div>
<div>* Implement Strict global configuration support to control whether non-empty author attribute is allowed or not by @MalloD12 in https://github.com/liquibase/liquibase/pull/4044</div>
<div>* Read Snowflake views definitions with the Snowflake-specific query by @LonwoLonwo in https://github.com/liquibase/liquibase/pull/3794</div>
<div>* Fixed #3745 error generation intType when using autoIncrement=true with H2 V2 by @quonas in https://github.com/liquibase/liquibase/pull/4008</div>
<div>* log generated databasechangelogsql without erroneously incrementing the order executed by 2 (DAT-13680) by @StevenMassaro in https://github.com/liquibase/liquibase/pull/4097</div>
<div>* Remove native executor name property (DAT-13580) by @abrackx in https://github.com/liquibase/liquibase/pull/4108</div>
<div><br></div>
<div><br></div>
<div>## New Contributors</div>
<div>* @maartenc made their first contribution in https://github.com/liquibase/liquibase/pull/3707</div>
<div>* @amrasarfeiniel made their first contribution in https://github.com/liquibase/liquibase/pull/3927</div>
<div>* @nwcm made their first contribution in https://github.com/liquibase/liquibase/pull/3842</div>
<div>* @AlexGruebel made their first contribution in https://github.com/liquibase/liquibase/pull/3926</div>
<div>* @ponziani made their first contribution in https://github.com/liquibase/liquibase/pull/3378</div>
<div>* @barthel made their first contribution in https://github.com/liquibase/liquibase/pull/3903</div>
<div>* @DCCSKrezovic made their first contribution in https://github.com/liquibase/liquibase/pull/4001</div>
<div>* @justin-tay made their first contribution in https://github.com/liquibase/liquibase/pull/3959</div>
<div>* @quonas made their first contribution in https://github.com/liquibase/liquibase/pull/4008</div>
<div><br></div>
<div><br></div>
<div><br></div>
<div><br></div>
<div>**Full Changelog**: https://github.com/liquibase/liquibase/compare/v4.19.1...v4.20.0</div>
<div><br></div>
<div>### Get Certified</div>
<div>Learn all the Liquibase fundamentals from free online courses by Liquibase experts and see how to apply them in the real world at https://learn.liquibase.com/.</div>
<div><br></div>
<div>### Read the Documentation</div>
<div>Please check out and contribute to the continually improving docs, now at https://docs.liquibase.com/.</div>
<div><br></div>
<div>### Meet the Community</div>
<div>Our community has built a lot. From extensions to integrations, you’ve helped make Liquibase the amazing open source project that it is today. Keep contributing to making it stronger:</div>
<div><br></div>
<div>[Contribute code](https://www.liquibase.org/development/contribute.html)</div>
<div>[Make doc updates](https://github.com/Datical/liquibase-docs)</div>
<div>[Help by asking and answering questions](https://forum.liquibase.org/)</div>
<div>[Set up a chat with the Product team](https://calendly.com/liquibase-outreach/product-feedback)</div>
<div><br></div>
<div>Thanks to everyone who helps make the Liquibase community strong!</div>
<div><br></div>
<div>## File Descriptions</div>
<div><br></div>
<div>-  **Liquibase CLI** -- Includes open source + commercial functionality</div>
<div>  - **liquibase-x.y.z.tar.gz** -- Archive in tar.gz format</div>
<div>  - **liquibase-x.y.z.zip** -- Archive in zip format</div>
<div>  - **liquibase-windows-x64-installer-x.y.z.exe** -- Installer for Windows </div>
<div>  - **liquibase-macos-installer-x.y.z.dmg** -- Installer for MacOS</div>
<div>- **Primary Libraries** - For embedding in other software</div>
<div>  - **liquibase-core-x.y.z.jar** – Base Liquibase library (open source)</div>
<div>  - **liquibase-commerical-x.y.z.jar** – Additional commercial functionality</div>
<div>- **liquibase-additional-x.y.z.zip** – Contains additional, less commonly used files </div>
<div>  - Additional libraries such as liquibase-maven-plugin.jar and liquibase-cdi.jar</div>
<div>  - Javadocs for all the libraries</div>
<div>  - Source archives for all the open source libraries</div>
<div>  - ASC/MD5/SHA1 verification hashes for all files</div>
<div><br></div>
<div><br></div>
<div><br></div>
<div>**Full Changelog**: https://github.com/liquibase/liquibase/compare/v4.20.0...v4.21.0</div>

