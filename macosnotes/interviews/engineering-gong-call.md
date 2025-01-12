<div><b>Creation Date:</b> Wednesday, April 5, 2023 at 12:29:13 PM<br></div>
<div><b>Modification Date:</b> Wednesday, April 5, 2023 at 12:35:09 PM<br></div>
<div><h1>Engineering gong call</h1></div>
<div><br></div>
<div><br></div>
<div>Taras: &quotLet me share screen. So the question is about, so we have this document that states that a supported version is from basically 10 to 13 because nine is deprecated by AWS and confusion is because… some versions, some of the versions, for example, Postgres Amazon RDS support version 14 community version 14, but EDB cetera, 13. Yeah.&quot</div>
<div><br></div>
<div>Taras: &quotGuys, please correct me if I'm wrong, but this information is true for now because basically, I checked on our Jenkins to certify any version of database that we support. We need to run all our regression that we have. And for Postgres Aurora… if we will select Postgres Aurora right now, we have configured it 10 11, 12 and 13. Now 14 version here. So, yeah, we for sure officially do not serve support question for 10. Can we support it? I believe, yes. And maybe there is also a chance that we will not need to do anything to support it. I mean, from engineering side on, we need like if we want to support it by June. First of all, we need the ops ticket for Jake or Andre to configure build logic… to start like to run all our test on our 14. And basically two options if everything will be okay, we just will update this document that we support. Or 14. If not, then I will we'll encounter some problems and then we will like create another ticket to fix some box regression or something else. But most probably it should be easy. Maybe somebody remember why we don't implement it earlier?&quot</div>
<div><br></div>
<div>Acheh: &quotWe had specific request for Postgres 14 and Postgres is 14, but we didn't have it for ARR, so that's… why we didn't go with through platform specification process that we have. So basically, yeah, you are absolutely right. We need to certify it. This platform where version should go through our certification process and we need to just enable automation for or 14. It should not be so hard to do, but we need ticket.&quot</div>
<div><br></div>
<div>Ruslan: &quotSorry, guys like those and your version 15 is already available? Should we also like add those to the list of the database that we want to check?&quot</div>
<div><br></div>
<div>Martha: &quotYes, I think we should, I mean, this customer is asking for 14 but they could decide to upgrade at any point in time. I think we should in general, try and keep up with the, whatever the database releases are you're coming out with? Okay?&quot</div>
<div><br></div>
<div>Acheh: &quotSo basically, just to summarize, do you want us to certifies this version? I mean poses 15 in advance?&quot</div>
<div><br></div>
<div>Martha: &quotI would ask for that. Yes. Hopefully, it just turns out that we just need to run our tests and everything's good.&quot</div>
<div><br></div>
<div>Ryan: &quotYeah, I agree with everything Martha said. I think the clear business requirement is for 14 and I agree that, you know, if we can do 15 two at the same time, that would be great because, yeah, I expect our customers will be upgrading.&quot</div>
<div><br></div>
<div>Martha: &quotYeah, I would say the same thing across all those Postgres… same thing with just regular Postgres on RDS and Postgres community at least.&quot</div>
<div><br></div>
<div>Taras: &quotOkay.&quot</div>
<div><br></div>
<div>Martha: &quotBecause it's really confusing to our customers. Postgres to them is Postgres and the fact that… we RS, and not for Aurora. Yeah, I understand the confusion.&quot</div>
<div><br></div>
<div>Taras: &quotUnderstand. And there is like high chance that if we will run our tests, we will see that maybe everything is okay. And maybe we do support it right now. We just never tested it because we didn't have this request. Okay? So we need a ticket to… I will say one.&quot</div>
<div><br></div>
<div>Taras: &quotPrepostorous. So, yeah, because we need like one ticket per one specific question.&quot</div>
<div><br></div>
<div>Acheh: &quotCan you also tag Mario… so that he can be aware of this request?&quot</div>
<div><br></div>
<div>Taras: &quotOkay. Who should create?&quot</div>
<div><br></div>
<div>Ryan: &quotWell, well, Mario, I mean… I think, you know, we're surfacing the need here, but the path is for us to go through Mario. So, and he'll you know, prioritize it appropriately. So, I'm not trying to, we're not trying to start circuit. We're just, you know, talking about the challenges we're seeing here.&quot</div>
<div><br></div>
<div>Acheh: &quotOkay.&quot</div>
<div><br></div>
<div>Taras: &quotYeah. Okay. So we are done with over one question. I think my part is over. We never did retro part, who is supposed to run it.&quot</div>
<div><br></div>
<div>Lora: &quotI'm gonna try and run this and we'll see how it goes and what adjustments we need to make for next time. But this was essentially for us to kind of regroup and reflect on how it's been going with the escalation process. And I'm referring to us opening JIRA tickets from support and CS to get engineering help for difficult issues. So I wanted to just kind of have an open forum for us to talk about what's been working. Maybe what hasn't been working so well and maybe things that anybody has ideas that we need to change or improvements we can make on that process.&quot</div>
<div><br></div>
<div>Lora: &quotDoes anybody have any input they wanna start with?&quot</div>
<div><br></div>
<div>Acheh: &quotYeah, yeah. I can start. So the first item is what has gone well. So basically from engineering side, I can say this is like this is collection is really helpful especially when we need to track some time and we can like put our, some let's say kind of story points in this ticket… and it will be showing in our capacity.&quot</div>
<div><br></div>
<div>Acheh: &quotThat's definitely what was… that? Yeah, how to say that we were missing it for a long time especially when we had all questions which came through slack threat. So, yeah, what has not gone well? So… just we'll try to explain, maybe it's not a problem. Maybe it's a problem. Basically, we can decide it altogether. So, so sometimes we have ticket which is not escalation, which is just regular, that ticket and engineering team treats it treats it as something that we can plan and work. And I don't really know what is the expectation from CS side about this ticket? Because for us, for engineering team with just regular ticket, it should be prioritized by then it should be conditioned by engineering team. And then based on prioritization, we can ticket and move to development.&quot</div>
<div><br></div>
<div>Lora: &quotAnd you're talking about the dot tickets, not the escalation tickets, right?&quot</div>
<div><br></div>
<div>Acheh: &quotYes. Okay. And it's time a bit confusing what, what's input, which is expected from engineering side? In case of that tickets… for example, we have problem, do we need to help is trying to find a workaround just on what customer at least temporary or, yeah. So what is the case of discussing tickets? That tickets… maybe?&quot</div>
<div><br></div>
<div>Lora: &quotOkay.&quot</div>
<div><br></div>
<div>Andrii: &quotYeah.&quot</div>
<div><br></div>
<div>Acheh: &quotAre you meaning?&quot</div>
<div><br></div>
<div>Lora: &quotLike on the escalation tickets, it's more clear what the expectations are from engineering versus on Dat tickets. Sometimes it's not as clear.&quot</div>
<div><br></div>
<div>Acheh: &quotI would say yes because I scan in escalation tickets based on priority. I mean, not priority severity. We can understand. Okay, it's urgent to like, you know, put some input from engineering sit, at least say, okay, we can provide work around or guys, for example, I spend like more than two hours trying to understand if we can solve it. I don't see pass forward any kind of work around. Most. Probably we just need to rise that ticket. And if it, and if it's critical, we definitely need to pass it through whole cycle like product prioritization science and it should happen really quick then condition. And then we can spend some time because it's still a bit hard to understand what is time box for escalation tickets from engineering standpoint?&quot</div>
<div><br></div>
<div>Lora: &quotOkay. So that maybe sounds like a different one than is what is the time box expectation for escalation tickets?&quot</div>
<div><br></div>
<div>Acheh: &quotYeah.&quot</div>
<div><br></div>
<div>Lora: &quotOkay.&quot</div>
<div><br></div>
<div>Lora: &quotOkay.&quot</div>
<div><br></div>
<div>Andrii: &quotFrom my side, I would say that I absolutely agree with Andre and also wanted to add that… for example, if we have escalation ticket from, if I understand correctly, like how this process work works, we should be able to provide the next step like for customer support team or something least like a workaround or even next steps for us. So we come back to you and we should directly move the ticket to like done until next steps are not required again. But if we need to do some work, I mean, for example, to spend half a day or two days, like to check something or to create something we definitely should create like that ticket. I would say a good example. The last like the latest escalation ticket which I pay call correct is number nine and on tried at, to like to find a workaround but looks like it's like some in customer side. And for example, from my side to be able to like do the next steps while we are not able to reproduce. I need to set up all environment… to like check some walks configuration on both like eco site or site and it will take for me for example, two days definitely not going to do it as part of escalation teacher, but rather as a next step, we need to create that teacher and price it as like severity tool or something or severity, but something that's definitely high priority. So I can do is work as part of.&quot</div>
<div><br></div>
<div>Lora: &quotOkay.&quot</div>
<div><br></div>
<div>Lora: &quotOkay. That makes sense. I, I've seen you guys do that for a couple of things on these escalation tickets. And I think it's been helpful at least for us to understand the work going into some of that. So, yeah. Okay.&quot</div>
<div><br></div>
<div>Lora: &quotAnyone anyone else have anything to add?&quot</div>
<div><br></div>
<div>Acheh: &quotYeah. I have also one more item. It's most probably related to ideas for improvement. We don't have clear instructions on what should we do in case of environmental issue which happens on customer site, for example, again, escalation nine. It's issue with log and are active directory and san like tried to recreate this issue multiple times on our environment. However, he didn't have a luck to doing that. And I don't know if we actually have instructions on what to do in this case, if it's an environmental problem, maybe we need to figure out what to do in such cases. For example, we can try to recreate it internally. And now, like then jump on calls customer and see what's going on there environment. Or maybe we need to end up this list of, I don't know things which should be requested from customer site for better investigation… from engineering team, for example, if it's clear kick log and we just need to like ask for kick. I mean, kick log related issue. We just need to ask for logs even before and I mean, and they should be attached during escalation ticket creation. So something like that.&quot</div>
<div><br></div>
<div>Lora: &quotOkay. So, for, so there sounds like if there's a couple of things for one, maybe we need to set clear expectations from the support and CS side that for certain issues, we always provide logs like for keto, right?&quot</div>
<div><br></div>
<div>Acheh: &quotYeah.&quot</div>
<div><br></div>
<div>Lora: &quotOkay. I.&quot</div>
<div><br></div>
<div>Acheh: &quotShould help and reduce the cycle like back and forth for example, like CS team, create a ticket. We got it. We don't have enough details. We ask you just a guys, can you please ask customer to provide some particular walks and it takes time… so we can do it in advance. It will be really helpful.&quot</div>
<div><br></div>
<div>Lora: &quotYeah. Okay. So for that, for one example was key clock, we need to provide logs.&quot</div>
<div><br></div>
<div>Acheh: &quotI log that call logs. So… USA, if you have something to add data?&quot</div>
<div><br></div>
<div>Ruslan: &quotYeah, I just want to, that probably we should not afraid to tell customer please like open ticket with key clock or azure a D and help us because to be honest, like especially as collection ticket number nine, it's not about it's, about key log and azure and we can spend time to like to try to figure out what the problem, but it's more about like key log and azure and not, so I'm not sure like if it's okay to say that the customer, but I think like we should not afraid to do that because we're just using like kick log like external library and they're using azure a D is like also not related to DC. So.&quot</div>
<div><br></div>
<div>Martha: &quotMy, my comment about that is going to be that I would feel okay having them open a ticket with maybe azure because that's a company they contracted with. The key cloak is something that came from us and that's not something they chose to use. It's something we told them to use and gave them. So they're going to really push back if we tell them to open a ticket with key clock plus it's open source. I don't even know that, you know, they would expect us to do that. Okay?&quot</div>
<div><br></div>
<div>Lora: &quotYeah. Okay. So, I think the other thing you were mentioning Andre, was there's not clear expectations for example, like this one where we can't reproduce the issue. We're only seeing the issue on the customer side. What are the expectations when we get to that point? Am I understanding that right?&quot</div>
<div><br></div>
<div>Acheh: &quotYeah. What should we do in this case? How… like, yeah. So basically, yeah, what we can do in this case?&quot</div>
<div><br></div>
<div>Lora: &quotOkay. Can I ask?&quot</div>
<div><br></div>
<div>Amy: &quotDo you guys have an azure environment? Because I know CS team still doesn't have an azure ad. We can suspend of azure databases, but we don't have an azure ad environment. Do you guys have one that you use? Yeah, we do. Okay. Could we borrow it?&quot</div>
<div><br></div>
<div>Acheh: &quotYes, yes, I believe it's like we can just show how to use it and you can play.&quot</div>
<div><br></div>
<div>Amy: &quotOkay.&quot</div>
<div><br></div>
<div>Ruslan: &quotI more question for Jake not for us.&quot</div>
<div><br></div>
<div>Amy: &quotOkay. So, Jake maintains, yes, sure.&quot</div>
<div><br></div>
<div>Andrii: &quotWe need to get some permission.&quot</div>
<div><br></div>
<div>Acheh: &quotYeah, most probably, yes.&quot</div>
<div><br></div>
<div>Acheh: &quotOkay. I saw some ticket where was mentioned something about ASE environment for CS team. Maybe he just want to prepare a new as active directory just for like CS team.&quot</div>
<div><br></div>
<div>Lora: &quotThere is a ticket from support to get that setup for the environment. We're trying to test this, that issue in. So that may be the one you're seeing.&quot</div>
<div><br></div>
<div>Acheh: &quotMaybe, but yeah, if you will need like our death environment, just let us know or pin, Jake, you will share access to it.&quot</div>
<div><br></div>
<div>Lora: &quotOkay. Okay.&quot</div>
<div><br></div>
<div>Lora: &quotI have something to add to what has gone well. I think it's been super helpful to have these tickets. We have things to tie to the support ticket. We have things to tie to any JIRA ticket like that tickets that are open from the escalations. So, I think it's been really helpful to have that source of record in the JIRA ticket for these escalations. I know for example, the DMC one I worked on with us on it was really helpful to have the comment threads there. It was easier to track what we had done, what the instructions were and like and then summarize like what actually was done on the customer side and then still have that history tied to the support ticket. So I think it's been helpful to have it tracked in JIRA versus in slack because in slack, it's easy to lose that history. If we ever have to look back on the support ticket. If we have a similar issue, we actually have clear background on what was done and what we can try next time without having to do another escalation ticket. So I think that's been helpful.&quot</div>
<div><br></div>
<div>Lora: &quotAnybody else have anything they want to add?&quot</div>
<div><br></div>
<div>Andrii: &quotYeah. From my side, I like also like this process makes the auditization of these tickets much better because previously we just, we're looking like on the messages in the chat and we didn't know which have like high priority which is have like, well priority. So we'll definitely… have a better process now. And the only issue which I already mentioned from my side is to understand because now we have like better understanding of priority of such issues, things to coation tickets. But now I need to match like priority of escalation tickets and bad tickets and as soon as like fix it from my side, it will like the perfect process.&quot</div>
<div><br></div>
<div>Lora: &quotOkay. And I think that ties back to what we were talking about with this raise like creating a ticket when it's time consuming work. Okay?&quot</div>
<div><br></div>
<div>Taras: &quotSo I will add that… because tickets have assigned person to it, we can understand that somebody is working on it because when we had a question in slack, there could be two people working at the same time. Because like if I receive some question, I need to check something, spend some time at the same time on can do the same and we kinda is wasting time. And when there is a ticket, we understand that, okay, somebody is assigned to this ticket and this person is doing it. Also, what is helpful with ask tickets is ability to request some kind to do clarification and request additional information even before that ticket creation. So if you know that something is missing something is there is not enough information to open that ticket, we can clarify it like in advance so that ticket will contain everything and it will be like done quicker. And I want to point out that thing that Andres was talking about time box. I believe this is important here. And for example, if we would have some time box and ask ticket and we understand that there is a ticket. It has like five hour time box. If time box is exceeded, we need to choose to create that ticket and to a standard flow or maybe this is kinda rabid whole situation and we need to kinda step back and say to customer, not our problem or something like that. I mean, because we can waste a lot of time and we, at some point maybe it's not profitable. You know? So after like my proposition, so after time box limit is broken, like it's time to decide standard flow or maybe we did what we could and like… not gonna make, yeah.&quot</div>
<div><br></div>
<div>Lora: &quotThat makes sense. So we're not spending unlimited time on tickets without making a decision. Okay? I think somebody else was gonna say something.&quot</div>
<div><br></div>
<div>Acheh: &quotYeah. So never mind.&quot</div>
<div><br></div>
<div>Lora: &quotOkay. I think the other thing I was gonna point out to I've noticed a couple of times on these escalation tickets, they don't always get the status isn't always updated. So sometimes it'll sit in active when it's like moving quickly between engineering and support. So sometimes it's hard to tell if it's supports responsibility or if engineering is currently working on it. So I think it would be helpful if both sides maybe made a little bit more of an effort to make sure the assignment and the status is updated. So it's clear that like engineering is done and they need support or CS to now do something or follow up and then we can then pass it back when we have that. Sometimes it's just not always clear if that's not updated.&quot</div>
<div><br></div>
<div>Lora: &quotOkay. I know we have like two minutes left, so I wasn't sure if anybody else had anything else they'd like to add.&quot</div>
<div><br></div>
<div>Lora: &quotOkay. It sounds like we got a couple of areas. I think maybe we need to spend some time thinking about maybe some solutions to some of these things, but it sounds like for the most part, this has been helpful process. We need to maybe just do some more fine tuning on some of these areas and maybe define the process for some of these things like the time spent and what do we do when we can't reproduce an issue except for only in the customer environment? So I don't think we're going to solve those right now, but definitely stuff we need to think about, maybe come up with some suggestions and solutions for.&quot</div>
<div><br></div>
<div>Lora: &quotOkay.&quot</div>
<div><br></div>
<div>Acheh: &quotSounds great.&quot</div>
<div><br></div>
<div>Lora: &quotCool. Well, thanks, everybody. I think this was really helpful.&quot</div>
<div><br></div>
<div>Acheh: &quotSee here we.&quot</div>
<div><br></div>
<div>Taras: &quotBye. Bye. Have a good day.&quot</div>
<div><br></div>
<div><u>Link to snippet</u><br></div>
<div><br></div>
<div><br></div>

