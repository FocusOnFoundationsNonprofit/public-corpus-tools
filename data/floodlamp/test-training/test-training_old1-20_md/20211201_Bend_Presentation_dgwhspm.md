## metadata
last updated: 12-21-2023 Created
link: https://vimeo.com/654504246/b9130720de
transcript source: dgwhspm
summaries source: deepgram

## content

### summaries

Summary  [0:00](https://vimeo.com/654504246/b9130720de?ts=0)
Randy True is the founder and CEO of FloodLAMP, a public benefit company. The company's mission is to improve global health through universal access to better rapid molecular testing.

Summary  [4:53](https://vimeo.com/654504246/b9130720de?ts=293000)
The company is a hybrid between a startup company and a non-profit. The company has submitted EUAs to the FDA.

Summary  [9:22](https://vimeo.com/654504246/b9130720de?ts=562000)
The Quick Color Lamp Test has an LOD of 12 copies per microliter. This is significantly more sensitive than antigen tests. The FDA process is very much in need of an upgrade to be objective. Wiley with saliva direct created the first open source protocol.

Summary  [13:48](https://vimeo.com/654504246/b9130720de?ts=828000)
Randy Smith: We're doing all this with a, with a small, small, but dedicated team led by myself and our co-founder, COO, Kevin Schaller. He founded another nonprofit involved in COVID relief called the National Volunteer Scientist Database, or NSVD. And that's how we got connected to Katrina.

Summary  [18:33](https://vimeo.com/654504246/b9130720de?ts=1113000)
The current deployments in Florida are in medical office rooms, which just have windows. Preventing RNA degradation is trickier than preventing DNA degradation. RNases are present in all cell types from prokaryotes to eukaryotes.

Summary  [23:01](https://vimeo.com/654504246/b9130720de?ts=1381000)
The COVID test is quite simple compared to most tests that are done in a clinical lab. The key is to understand kind of how to avoid these several types of contamination. And so another key thing that makes us able to do this test in this kind of environment with newly trained firefighters is the controls.

Summary  [26:45](https://vimeo.com/654504246/b9130720de?ts=1605000)
So I would recommend putting a lock on the door, putting the sign up and just controlling access to it. There is a station, a desk station where you can touch your computer or other stuff without gloves, but it's a certain area. And even in addition to gloves, you really want a lab coat so that you don't even get your forearm touching anything.

Summary  [30:59](https://vimeo.com/654504246/b9130720de?ts=1859000)
The first is sample cross contamination. By this we mean transferring material from one sample tube to another. A telltale sign of that would be neighbor positives and more than one positive in a batch. The second is Amplicon contamination. Amplicons are the product of the DNA of the amplification.

Summary  [34:52](https://vimeo.com/654504246/b9130720de?ts=2092000)
The SARS-CoV-2 virus can be transmitted through contact with contaminated tubes or tubes. Semiconductor industry wastes even more gloves. There is extra protection from this with a thermo-lay-bio-nucleotide.

Summary  [38:37](https://vimeo.com/654504246/b9130720de?ts=2317000)
CNN's John Defterios explains how to run a DNA test on a fake positive sample. He says the test can be done in three steps: inactivation, reaction, and run. Defterio: "I think it's going to make sense for Katrina and I to do the validation run"

Summary  [42:43](https://vimeo.com/654504246/b9130720de?ts=2563000)
Katrina: I'm fine to stay till two and we could try the validation run or we could do one more. I think we should do it today based on the rest of my week. I don't want you all to be overly intimidated by this. If any of you want to learn it and run it, you absolutely can.

Summary  [46:50](https://vimeo.com/654504246/b9130720de?ts=2810000)
I would recommend you all to have one person to kind of become proficient with it in the lab. The others can know it and know they could learn it over even a day if you practice a lot that day. But I just think having one person focus on it might make the most sense. I think the one thing that we're faced against here right now is just the staffing shortage.

Summary  [50:41](https://vimeo.com/654504246/b9130720de?ts=3041000)
I mean, we do stuff all the time and it's procedure based. Yeah, I think we get in the lab and take a look but we selected these guys, because of their attention to detail, and their passion for this part of it.

### transcript

Speaker 0  [0:00](https://vimeo.com/654504246/b9130720de?ts=0)
Other supporters.

Speaker 1  [0:05](https://vimeo.com/654504246/b9130720de?ts=5000)
But yeah, first special, extra special thanks to Katrina for volunteering to do this. And then Kevin, who's who is, is tag teaming on solving all kinds of other issues. He helped coordinate both with Peter and with Katrina and with other folks at OHSU who we may bring into the work and project. So there's already a fantastic team on board to support this effort. So here's what I had for the just jumping into. It sounds like y'all have already done a few intros we're clearly going to have to adjust the times. We're almost exactly an hour late. So that'll make it kind of easier. But it will encourage me to speed through stuff. Can you guys hear me? Okay, is everything?

Speaker 2  [0:56](https://vimeo.com/654504246/b9130720de?ts=56000)
I was going to double check I was all the way up on this thing. Yep.

Randy True  [1:03](https://vimeo.com/654504246/b9130720de?ts=63000)
Okay. So I'm Randy True, founder and CEO of FloodLAMP, and we are a year and a half into our mission to bring better COVID testing to the world. I formerly was in the diagnostics space and had a successful platform company. We just actually discovered a connection in one of my early supporters in that company through a band connection. I founded an education nonprofit about four years ago and it was halfway through teaching a STEM curriculum at a vocational high school here in the Bay Area when the crisis hit. I thought there was gonna be a Apollo project around testing the vaccines. And when I reached out to colleagues in the space, I saw what a mess testing was. And one thing led to another. And I've ended up jumping into developing technology in a program. And I'll share a little bit about that in the 10 minutes of an overview. It'll help give some context to, to this, this deployment and the work, y'all are doing today. But if you all don't mind just sort of jumping around quick and telling me who y'all are and what you do. I'd love to hear it.

Speaker 0  [2:20](https://vimeo.com/654504246/b9130720de?ts=140000)
I'm Jerry. I'm a firefighter.

Speaker 3  [2:24](https://vimeo.com/654504246/b9130720de?ts=144000)
Great. There we go.

Speaker 0  [2:28](https://vimeo.com/654504246/b9130720de?ts=148000)
I'm Richard Rufugani, I'm Drew. I'm our deputy chief of EMS. Perfect. I'm Ben. I'm one of our infectious

Speaker 3  [2:39](https://vimeo.com/654504246/b9130720de?ts=159000)
disorders. Great.

Randy True  [2:43](https://vimeo.com/654504246/b9130720de?ts=163000)
And I know Peter well by now. Katrina, you introduce yourself.

Speaker 3  [2:51](https://vimeo.com/654504246/b9130720de?ts=171000)
Ben, I used to do a lot of stuff like this in grad school so I'm a molecular biologist, you can't teach her a choice and I love it, but I'm really glad to help out.

Randy True  [3:03](https://vimeo.com/654504246/b9130720de?ts=183000)
Thanks for being here.

Speaker 0  [3:04](https://vimeo.com/654504246/b9130720de?ts=184000)
Yeah, more on the reports.

Randy True  [3:07](https://vimeo.com/654504246/b9130720de?ts=187000)
Great. So y'all can see the agenda here. We've done this safety training and contamination training informally a few times and I put new slides together for this training and I'll be very interested in getting all this feedback, you know, particularly Ben being the infection control officer. So I just wanna jump in and quickly run through what Fodlamp is all about. We're a public benefit company, which means We have a commitment to infectious disease testing for the public good and open source protocols baked into our corporate DNA. So you can think of us like a hybrid between a startup and a nonprofit. And so our mission is to improve global health and resiliency through universal access to better rapid molecular testing. And we're doing that through new technology, through programs and open source strategy. We have key real world deployments now with the EMS community and so that's you know serving first responders and piloting our programs with y'all have been both key to deploying what we have and getting our work out into the real world. So we also have a commercial program And then we just started a local preschool testing program where we're doing at home family pooling with our app. And this is, as far as we know, this is the only program out there doing this kind of modality, which we think has huge potential. This has been an odyssey. We submitted EUAs to the FDA last March and I thought it was gonna be off to the races but we got backburnered and de-prioritized like a lot of companies, which is a terrible tragedy when we were rallied to, to, you know, startups were rallied to, to, to, to serve and to deliver new technology in the pandemic. And then we hit, you know, gnarly, gnarly red tape. So we, we have, have done a ton on the regulatory front and are still seeking to bring that to fruition. We have some key advisors and consultants on the regulatory side, but a key, one of our closest advisors and our friend is Anne Wiley, who developed a key test in the space called SalivaDirect. She just got appointed to Biden's COVID task force and she is a force of nature and has, according to other high level people in the space, almost single-handedly cause cost compression in the testing space. So she's great. We again, hybrid between a startup company and a non-profit. And so we are doing some key IP development and have an eye toward the future as well with some new technology and new platform patents. We have manufacturing relationships with top suppliers in the space. So any B who makes the master mix and then another large supplier of oligos it makes our primers. So we are are poised to to scale what we're doing in a big way. To sort of put this into perspective, I think y'all are pretty familiar with testing. We're at the intersection of both performance in terms of sensitivity, turnaround time, and then cost. So this kind of helps position why we're working so hard to get this configuration, to get this test out there. The specifics of what make up our sort of testing system, our fully integrated program is pooled swabs. This actually shows a five mil tube where we pull up to four swabs, and that's what most of our deployments are. You all have a mini system where you can pull up to two swabs right now with the current kind of sterile medical swabs that we're providing. And it's our understanding that that's sufficient if you wanted to move to the four, we could easily do that with y'all. So the second component is an app which helps accession these pooled samples and makes it really streamlined for the lab to process the pre-accession tubes that come in the door. And then finally is the test and the test chemistry, which is, you know, on one hand, new technology, but on the other hand, LAMP has been around. This chemistry that we're doing was developed by Harvard in April, and the professor that developed it has been decide herself that it hasn't been more front and center for the US's testing effort, but it uses a test chemistry that produces so much DNA that you can get a visual readout. And it also runs on heat blocks, so you don't need a PCR machine. So it's game-changing on a few fronts, and we're using a direct version of it where we skip this RNA purification. So this sort of shows that. We have a companion PCR test. It's very similar to saliva direct, but works like swabs. And we've submitted both of these two tests to the FDA. Here's our clinical validation data, and we can share this whole data package with y'all if you're interested, or we did share with one county health officer who had asked before deployment, so that's totally available if you all are interested. We got a 90 percent sensitivity. But the key thing to understand about the sensitivity is it's not an objective measurement. It very much depends on your sample set. In fact, the entire FDA process is very much in need of an upgrade to be objective. There's finally an effort to do that with the antigen tests with a collaboration with the NIH. They have an independent testing facility they're using now to get objective measurements for the antigen tests. So some progress, but you know, it's definitely held back good tests into the market. So the test that you're using is called, and we're deploying is the Quick Color Lamp Test, and that has an LOD of 12 copies per microliter. And so this is significantly more sensitive than antigen tests, not as sensitive as the highest purified PCR tests, but that level is way overkill for what you need. This level is below the infectious level, And so we can detect pre-infectious people, whereas one of the problems with antigen tests is they only detect people after they're already infectious. And so you're sort of chasing your tail. We can relay some of the configurations that we've deployed so far with testing. I think the EMS deployments will be of particular interest as you all think about how you can use this. Davey and Coral Springs are testing, I think, all shifts of firefighters as they come on shift and are expanding to city staff. And both of those sites have paramedic firefighters who've been trained to run the test. And so Adam Konick and Danny Chavez have been crushing it the last two months running this test. They are doing it every day. And so this is something we can come back to kind of at the end as we reflect on what to do kind of moving forward and how often y'all are running the test and who's going to run it. Peter and Temi, the medical director at these sites, brought our system up to a summer camp and tested two entire cohorts at the camp coming in at different times for, which was hundreds of campers. So that's another configuration. We popped up testing for the EMS conference in Florida this summer, and we from setup to validation we had it ready to go in three hours. So there is a portable component to this test. I've taken it on the road many times including most recently down to Arizona to test every day before seeing my mother who's advanced lung disease. So that's the true test of whether you trust your test is testing yourself and your family before you go see your mother. And then most recently, I think I mentioned we started this preschool at home testing. So I mentioned a little bit about the regulatory effort, but we are doing something revolutionary on the regulatory front and then we're open sourcing our test. So we're revealing the secret ingredients of what goes into this test in a way that basically no molecular diagnostics company ever does. It's a highly secretive, highly proprietary industry. And even when these tests are variations on a theme using very similar chemicals and reagents, even the same suppliers, they keep them highly secret. And so that's one thing that really locks up this space. And Wiley with saliva direct created the first open source protocol FDA called it the most unusual protocol they'd ever received because they applied for a manufacturer's EUA even though they never intended to manufacture or sell a test. And they allowed the labs to source directly from the suppliers and validated multiple suppliers creating a supply chain redundancy. And they now have a network of more than 150 labs, but we're all beside ourselves that this hasn't been picked up by the CDC and expanded. And so we're trying to get our program in front of the authorities to, to really help continue to unlock the space. We're doing all this with a, with a small, small, but dedicated team led by myself and our co-founder, COO, Kevin Schaller. He's been a successful software entrepreneur and is also mission-driven like myself. He founded another nonprofit involved in COVID relief called the National Volunteer Scientist Database, or NSVD. And that's how we got connected to Katrina. Other folks in the company are Teresa, who leads design, Gary, who does process development, and our lab assistant, Brandon, who's packed and shipped all of your stuff as well as helps on a huge variety of things. Got a number of advisors and great collaborators. So, thanks for listening to that you all have any, any questions about the company or the big picture here. If you do feel free to bug me at some point. We're eager to engage and spread the word on what we're doing. And especially as we make progress in getting support, financial support, large support to expand programs, we'd love for y'all to be a part of that effort. Okay, so let's jump into the meat of the work here in terms of going through the safety and contamination and then getting up out of the chairs and seeing what this is really all about. So that's, should have, should just be about 15 minutes of slides. We'll see how I do here. It's 1045. Here we go. So the safety part is about protecting y'all. I do need to give the disclaimers that this is not formal lab or biosafety training and that the site managers and personnel and volunteers, you are all ultimately responsible for maintaining appropriate training and certifications and and also with compliance with local, state and federal regulations. We're providing this information on a best effort basis during this public health emergency. And we're trying to highlight the key things, you know, that we pay attention to on a safety basis. So it's not it's not by any means complete. I included some links here. Y'all are being being an EMS here, you're probably pretty familiar with safety protocols medical protocols. So, basics, basic PPE is involved, mask gloves, lab coats. I usually prefer a face shield to goggles because mine fog up. We do have these listed in our protocol as a checkbox. The

Speaker 2  [16:48](https://vimeo.com/654504246/b9130720de?ts=1008000)
key is to have

Speaker 0  [16:49](https://vimeo.com/654504246/b9130720de?ts=1009000)
a face shield to stuff in the bunker. Pardon?

Speaker 2  [16:54](https://vimeo.com/654504246/b9130720de?ts=1014000)
Sorry, Mandy. We've got goggles

Speaker 3  [16:56](https://vimeo.com/654504246/b9130720de?ts=1016000)
in the bunker. As a checkbox. The key... Pardon? Sorry, I didn't...

Speaker 0  [16:57](https://vimeo.com/654504246/b9130720de?ts=1017000)
We've got goggles moved up here.

Speaker 2  [17:07](https://vimeo.com/654504246/b9130720de?ts=1027000)
And then Randy for masks, is this, I'm assuming N95

Speaker 0  [17:12](https://vimeo.com/654504246/b9130720de?ts=1032000)
to work with this stuff?

Randy True  [17:18](https://vimeo.com/654504246/b9130720de?ts=1038000)
We do sometimes use medical masks as well. I prefer N95s especially when I'm at our lab because there are a bunch of other people. From a, Yeah, from an infection control point, the N95s are preferred if you have them. From a contamination, when we get the contamination side, which is about protecting the test, a medical mask is fine. So in terms of sample handling, it's better if the incoming sample tubes are actually in biohazard bags, or if you are doing collection, if you're having all 20 people come to the same place, you could put them in a rack and just put that in a closed bin and save a lot of plastic. Again, some of that is your call in terms of your infection control procedure. The sample tubes, we do call for them to be wiped with alcohol after debagging. So the step with the highest infection control risk is when you open the tubes with the dry swabs for adding the 1X inactivation saline solution. So we prefer to do this in a well ventilated place. The current deployments in Florida are in medical office rooms, which just have windows. And so they aren't doing it like this, where you have an open garage. You know, labs typically have biosafety cabinets or chem hoods. Those are good places to do it. So there's a sort of a few options here, but I think it is important to highlight that this is the step to pay the most attention to is this very first step of opening the tube to add the inactivation solution. After that, it gets vortexed and heated, and then that it's a chemical plus heat inactivation, which denatures all the proteins and lysis the virus. And so it's not even a positive sample would not be infectious after that step. So in terms of chemical safety, I provided a link here to the SDSs involved with our test. And the two main chemicals are TSEP and EDTA, which are the two components of the main components of the inactivation solution. This inactivation solution is at two, You work with it at two concentrations, the 100x, which is what you use to make the inactivation saline solution, which is what you add to the samples. So give extra caution when you handle the 100x inactivation solution. So we provided an eye wash station. And so you should know where that is and and have a sink, but and know where the sink is as well. All this is probably old hat to y'all. Okay, so let's jump into something probably that's not as much old hat to y'all, but it is to Katrina, which is contamination from a molecular biology perspective. So we're going to focus on four types of contamination And contamination control really is the name of the game here with this, this RNA assay. Actually, a high school teacher that we collaborated with very early on, she had never got an RNA assay to work in her lab until we provided her kits last fall. And she tried with her students and she said, didn't work. And I asked her, well, did you use everything that we gave you? Did you use anything from your lab? And she said, oh, we use the water. I said, just only use what we gave you. She did, and then it worked first time and it worked for her students. So what I'm gonna try to do here is kind of convey the kind of the mindset to get into in the key highlights. And it's worth just pausing for a second. And I'd like to click on this link if it's gonna work here. This summarizes the important aspects of RNAs contamination quicker than I can. And then I think helps, will help us kind of make a point.

Speaker 4  [21:44](https://vimeo.com/654504246/b9130720de?ts=1304000)
Preventing RNA degradation is trickier than preventing DNA degradation. RNases are present in all cell types from prokaryotes to eukaryotes and can sometimes survive prolonged boiling or auto-cliving. So what are the major sources of RNAs contamination in the lab? Aqueous solutions and reagents, environmental exposure as RNAs are in the air, on both surfaces and in dust, and from human skin and hair. How can you prevent this contamination? Always wear gloves in the lab and change them often, especially after contact with skin, hair, doorknobs, keyboards, or animals. Use RNAs-free solutions and RNAs-free certified disposable plasticware and filter tips. Maintain a separate area for RNA work and carefully clean the surfaces. Decontaminate glassware by baking at 180 degrees Celsius or higher for several hours or by soaking in freshly prepared 0.1% DEPC water or ethanol for one hour, followed by draining and autocleaning. Decontaminate polycarbonate or polystyrene materials such as electrophoresis tanks by soaking in 3% hydrogen peroxide for 10 minutes. DEPC treatment of solutions is accomplished by adding one ml of any remaining amino acid residue.

Randy True  [23:01](https://vimeo.com/654504246/b9130720de?ts=1381000)
I'm intentionally skipping through this because they start talking about

Speaker 4  [23:04](https://vimeo.com/654504246/b9130720de?ts=1384000)
normal to maintain activity, make my

Randy True  [23:07](https://vimeo.com/654504246/b9130720de?ts=1387000)
own inhibitors, depth. They start talking about a bunch of stuff that's common to normal molecular biology labs. But this gets to a real key point, which is this lab that we have set up next door to y'all is really different from a normal lab because we're only doing one thing there, this COVID test. And this COVID test is quite simple compared to most tests that are done in a clinical lab or certainly most protocols that are done in a molecular biology research lab. So you might be wondering, oh, like, why are we setting up a COVID lab in a molecular RNA assay testing lab in a firehouse. Doesn't that take a real lab? And in some sense, yes, what you're going to have is actually a real lab. But in another sense, it's so pared down and the paring down is what enables us to be successful. I set up a lab in my garage and I did a did a FaceTime call with this Stanford professor that former Stanford professor who is collaborating with another nonprofit and he said, He said, you know, I said, what do you think of the lab I set up? And he's like, he's like, looks great. I was like, do you think I'm going to have problems, contamination, cleanliness? He's like, that's better than almost any lab at a, at a university because it's yours. You have it controlled. It's only for this and you'll be in great shape. And we have been, you know. So the key is to understand kind of how to avoid these several types of contamination. So let's just go through it real fast again. They did it on the video, but RNAs is this enzyme that degrades RNA, which is way more fragile than DNA, and it's everywhere. Getting an RNA assay to work is way harder than getting a DNA assay to work because again this stuff is everywhere and if you contaminate your tube your bag of tubes or any solution or something it can give you unreliable even sometimes intermittently bad results and it can be very frustrating to track down. The place we care about this RNAs contamination is primarily in this amplification reaction. And the reason is because the inactivation reaction, you're putting a nose swab with tons of RNAs in it into that reaction. And that's part of the purpose of it is to degrade RNAs. So we really focus on the second step of this test. How do you know, you know, how do we know if you have this problem? Well, the positive controls won't work. And so another key thing that makes us able to do this test in this kind of environment with newly trained firefighters is the controls, when you use them properly and when you design the test to use the controls, give you a great indication of when the test is working and when it's not. So what are we going to do to avoid the RNAs is, number one, is access control. And I sort of already saw some of this going on. I saw Peter in the lab like leaning over the amp table and I was like, oh no, don't touch anything with your bare hands. So that's the first thing.

Speaker 3  [26:24](https://vimeo.com/654504246/b9130720de?ts=1584000)
I'll come

Speaker 0  [26:24](https://vimeo.com/654504246/b9130720de?ts=1584000)
back later, Deacon.

Randy True  [26:27](https://vimeo.com/654504246/b9130720de?ts=1587000)
That's the first thing is that, you know, I've seen this problem too when we were giving tours, three, four fire chiefs and everybody were coming in and then it's like, oh no, like you don't want to, they can just, if they don't know, they can just touch something and cause a real annoying problem. So I would recommend putting a lock on the door, putting the sign up and just controlling access to it. I mean, do definitely feel free to give tours and stuff, but just make sure people don't touch anything. There is a station, a desk station where you can touch your computer or other stuff without gloves, but it's a certain area. All the rest of the area, you just think you've got to have gloves on. And even in addition to gloves, you really want a lab coat so that you don't even get your forearm touching anything. And it's just better to be extra careful about this and just to get in the mindset where skin doesn't touch anything that's clean in the stations. So I encourage a process to do a good cleaning up front and then keep things clean. Danny Chavez said he cleans his lab every day, and I think that's probably recommended from good lab practice. I actually don't for our lab here because it takes time and I prefer to be extra careful and keep the key things in bins that I keep on a shelf. So you can also use foil to put over things to keep them clean, keep dust off. You want to be extra careful with the reaction plastics and Katrina will help kind of point out what those are. You want to be wary of cross contamination. By cross contamination, I mean you touch a pen with your bare hands, and now you get finger grease on the pen. And then you're wearing gloves, you think you're okay, but then you go and touch something that's greasy, then you can pick up some and transfer. Now, you could drive yourself crazy thinking, well, how many degrees of cross contamination do I got to worry about? Worry about the first degree and just try to get some basic procedures and kind of mindset in place. And then you still got to do the work. You can't drive yourself crazy. Another key thing that we do to deal with RNAs contamination is we just we stage things so that we can just replace them and you can just get in you can you can get a new bottle of saline you can get new bag of tubes and you want to avoid the what I call the matlock trap which is like trying to sleuth and figure out where where the problems are coming from. It's better just to replace things, I could tell you some, I learned this one the hard way. Okay, so That's RNAs contamination. Do you guys have any questions about that?

Speaker 2  [29:36](https://vimeo.com/654504246/b9130720de?ts=1776000)
Nope. No, but I'm sure Randy's work, firefighters would probably look a little intimidated by all this stuff. This is not normally our area. Yeah. But I think the takeaway is, yeah, we're touching stuff and make sure we're clean.

Speaker 0  [29:54](https://vimeo.com/654504246/b9130720de?ts=1794000)
Yep. Would, would

Speaker 2  [29:57](https://vimeo.com/654504246/b9130720de?ts=1797000)
gowns work as well as lab coats?

Randy True  [30:00](https://vimeo.com/654504246/b9130720de?ts=1800000)
Yeah, gowns will work fine. Just anything that's kind of covering your skin. I actually jotted down on my follow-up that we should have included a couple of disposable lab coats just to account for multiple people in there. We did provide one kind of regular lab coat. But long sleeve shirt is also better than nothing, particularly if it's clean. Okay, I'll try to hurry quickly through the other kinds of contamination and some of these are best kind of learned along with the protocol. Particularly problematic one is positive control contamination. This is what screwed the CDC on the rollout of their kit and really put our whole country behind the eight ball at the beginning of this pandemic. This manifests as your negative controls aren't negative, they're showing up positive results or in the middle in conclusive results. So it's pretty obvious you have this. It can be hard to rectify because, especially if it's in the manufactured materials. So part of this is on our side. But the part that you worry about on your side is to follow the protocol and there's some special handling steps and procedures when you touch and deal with the positive control tube. You have to use the positive control tube with every heat cycle, every run, because it confirms that the reagents are still good. It's a critical part of the overall quality and assurance. So you do have to touch it and use it for every run. So I have some sort of recommendations in terms of just using one hand. We have a key glove change. And then we also just keep the positive controls in bags in the bottom of the freezer. And these procedures have worked really well for us for a long time now and haven't had any problems. So I think we'll be good to follow those. Okay, so sample cross contamination. By this we mean transferring material from one sample tube to another. So that's like, for example, if you open a tube and there's a drop on the tube and then you get that on your glove and then you open another tube and get that on the other tube on the threads or something in a way that can get inside. You know, if you have this problem, well, actually you don't know that you have this problem if all your tubes are negative, you could be cross contaminating all over the place. And you would never know if they're all negative, But if you do have a positive, you'll see other neighbor tubes get contaminated or come up positive. So a telltale sign of that would be neighbor positives and more than one positive in a batch. Again, following the protocol, being careful when you handle the sample tubes and the lids. If you do get a drop, wipe it up and clean it. And I suggest noting if that happens on a run sheet so that if you do get some positives and you can figure it out, you can look at it more carefully. Okay, so the last contamination I'm going to talk about is Amplicon. And this one is really bad. So Amplicons are the product of the DNA of the amplification. And they are DNA. They're not actually RNA. Sometimes they're called products. So I showed here the diagram for PCR and I showed the diagram for LAMP. LAMP is an alternative amplification to PCR and it is like biochemistry wizardry. It uses six primers instead of two and it forms these loop structures. And this happens all at a single temperature, whereas for the PCR, you ramp it up and down. And so LAMP produces 10 times as much DNA per volume as PCR in one third the amount of time and at a single temperature. So it's like a nuclear explosion of DNA production, whereas PCR is like a very controlled sort of firecrackers kind of going off. So the key here is that with LAMP, we wanna even be extra careful with amplicon contamination. And the reason I say if you get this, it's death, is because it can contaminate the entire lab and really require you to move the lab and start from scratch. I've even heard horror stories about me to do that in a new building. A lot of times this is because you open the tubes in order to do some other analysis. So I hadn't, you know, I'd never heard of LAMP before last summer. We've run PCR in the lab that I was in charge of at my former company, so totally familiar with PCR, never heard a lamp. And when I reached out to the team that developed the tests that we use, the first thing that the grad student who ran the test told me was never open the tubes. So that's the key thing. I don't see any reason why y'all would. We never have. And we've never had this amplicon contamination, but since it's so bad, I feel like I have to highlight it. And the way we deal with this is that we treat the tubes, the amplified tubes, the heater, the light box, everything in that area as if it's radioactive. And this area is like a black hole, anything that goes into it doesn't come out. So the pens that go in there, the post-it notes, you just leave them over there. And then whenever you touch them, the tubes or the heater, whatever, you again treat it like your gloves are radioactive and you take them off and you throw them away. And so it may feel wasteful, but don't worry about wasting gloves. It's, you will waste way more if you ever get any kind of contamination. It's just a part of the process. Semiconductor industry wastes even more gloves. Glove change is critical. Again, if you follow these rules, I think we won't have a problem. There is actual extra protection from this with a thermo-lay-bio-nucleotide, big words, it's some chemistry protection that helps where these amplicons, if they carry over, they get degraded in the first part of the temperature cycle. So don't worry about that if it doesn't make sense. It's just be aware. The main thing is to be aware of this AMP area and the fact that we just treat it like it's super radioactive. Not radioactive, not because we're worried about it hurting us, but just for this contamination perspective. OK, you all have any questions on the contamination?

Speaker 3  [36:50](https://vimeo.com/654504246/b9130720de?ts=2210000)
Well, we don't do it.

Randy True  [36:51](https://vimeo.com/654504246/b9130720de?ts=2211000)
OK. Let's get into how this test actually works. And this is only a few more slides, so thank you so much for bearing through this with me. So I think the easiest way to understand this test is it's like two x two x two. It has two solutions that you make, and you can make those ahead of time. Each one has two components, And then the tubes go through two heat steps. So this is a sort of a diagram of it. This is regular old saline, like wound wash saline. It's, you know, we get the sterile version, which wound wash would be as well. We make this and we also buy it. This we make the 100x inactivation solution. And so you just add this in a 100 to one ratio, and then you add one milliliter of that to the dry swabs. You put that on a heat block or in a heated water bath for either eight or five minutes, depending on which. Then you let it cool. And then that's your sample, your inactivated sample that you add to a amplification reaction. You make the amplification reaction by combining these primers, which are the part that's specific for the SARS-CoV-2 virus, along with this master mix. And this master mix has a ton of stuff in it that makes that whole amplification happen, mainly enzymes and nucleotides and some magnesium and a bunch of other stuff. I've never made this, we just buy it. There are multiple vendors of it now. We use the best one or at least the original one. There's some new ones that we're interested in trying. So these get put together and it's bright pink. And if SARS is present, it turns yellow. And the reason it turns yellow is because there's a pH-dependent dye that, and every time a nucleotide is incorporated, every step of the DNA copying process kicks off a proton and makes the solution more acidic. And so it becomes acidic and that changes it to yellow. Here's a more detailed diagram of that. And then these are available for y'all for reference. And I believe we printed them out. And so I think you will have the printouts of them in the lab. And then here's another version that shows actually the lamp and the PCR. They work from the same inactivation. It shows the bottle top dispenser here. So moving on to, well, I guess before we move on here, do you guys have questions on the test itself?

Speaker 0  [39:30](https://vimeo.com/654504246/b9130720de?ts=2370000)
Does all look like complex data?

Speaker 2  [39:35](https://vimeo.com/654504246/b9130720de?ts=2375000)
Yeah. But what I think is we probably need to really get with Katrina and Havre to kind of show each one of these steps. Yeah. Because overall, it doesn't sound that bad.

Speaker 3  [39:43](https://vimeo.com/654504246/b9130720de?ts=2383000)
It sounds like we

Speaker 2  [39:43](https://vimeo.com/654504246/b9130720de?ts=2383000)
can activate it and heat it, then we put a reaction mixture in it, after it cools down. Is that it? Roast the effect?

Randy True  [39:49](https://vimeo.com/654504246/b9130720de?ts=2389000)
Yep. And you can think of it in those three steps. In fact, I've recently trained our nanny to run our tests before, because we've done staff and family testing now for a long time, ever since the Delta surge came back up. We actually had to make it go faster so that she's not waiting as long. I make the inactivation solution and the reaction mix and have it waiting for her when she arrives, and then they're just ready to go. And so she collects her own sample, adds it to, that's her tube, adds it to our tube, and then adds the inactivation solution and runs it real fast. So You can think of this as really sort of three steps. You make the inactivation, make the reaction, and then do the run. And that's how we've also broken down the tracking of it. OK, so I think given the timing, I think it's going to make sense for Katrina and I to do the validation run another morning, maybe Thursday morning or Friday morning. The validation run is just a good thing to do and as a part of just qualifying the lab, getting everything set up. And what we do for the validation run is we make this contrived positive, this sort of fake positive sample with an inactivated virus. And so we add that to this inactivation saline solution and then run it like a regular sample and it should show up yellow. And so here's the run that we did at Coral Springs to validate their lab. We actually used two types of this contrived positive, this inactivated virus here. We'll only use one And then we ran our samples at the same time and worked perfectly. It has also not worked perfectly perfectly one time from I think what was a pretty dusty room in a contamination that happened but this is this is what I would expect to happen. I sort of designed the run to do just in one strip for us. So I think it'll make sense for Katrina and I to do this another morning. I also want to highlight that we have a training kit. And so along with this second FedEx package that's coming, there's a kit with mock reagents in it. And we actually even put in food coloring, red food coloring for the lamp master mix. So it looks the same color. And the nice thing about this training kit is you can practice with it and not worry about either using up or contaminating the real reagents.

Speaker 0  [42:36](https://vimeo.com/654504246/b9130720de?ts=2556000)
So yes,

Speaker 3  [42:41](https://vimeo.com/654504246/b9130720de?ts=2561000)
that came from whatever

Speaker 0  [42:42](https://vimeo.com/654504246/b9130720de?ts=2562000)
else we're looking for.

Speaker 3  [42:43](https://vimeo.com/654504246/b9130720de?ts=2563000)
Oh, I

Speaker 2  [42:44](https://vimeo.com/654504246/b9130720de?ts=2564000)
don't have any from

Speaker 0  [42:45](https://vimeo.com/654504246/b9130720de?ts=2565000)
Christie yet. I guess Kimberly did just say, you know, I know it's here. I didn't do so. I don't know if you

Speaker 2  [42:56](https://vimeo.com/654504246/b9130720de?ts=2576000)
can Christy yet. I guess.

Speaker 3  [42:59](https://vimeo.com/654504246/b9130720de?ts=2579000)
So the. That's the inactivation solution, which do you think it's vital that we go get that? I can stay a little later today if it helps you. I don't know what your time limit. I could stay till two maybe.

Speaker 2  [43:12](https://vimeo.com/654504246/b9130720de?ts=2592000)
Okay, well I don't want you to, I don't

Randy True  [43:14](https://vimeo.com/654504246/b9130720de?ts=2594000)
want to put you out. I'm fine to do this one morning before we're going to do it, Katrina. But if if you it depends on you, I'm fine to stay till two and we could try the validation run or we could do one more. And you choose.

Speaker 3  [43:27](https://vimeo.com/654504246/b9130720de?ts=2607000)
I think we should do it today based on the rest of my week. That's OK.

Randy True  [43:32](https://vimeo.com/654504246/b9130720de?ts=2612000)
Then then Then we do need to get that package over.

Speaker 3  [43:37](https://vimeo.com/654504246/b9130720de?ts=2617000)
Would you

Speaker 2  [43:37](https://vimeo.com/654504246/b9130720de?ts=2617000)
like me to go get it then?

Speaker 0  [43:39](https://vimeo.com/654504246/b9130720de?ts=2619000)
I'm going to take some more time here.

Speaker 4  [43:41](https://vimeo.com/654504246/b9130720de?ts=2621000)
Thanks, Judy.

Speaker 3  [43:43](https://vimeo.com/654504246/b9130720de?ts=2623000)
We're good. But that training kit is here. It came, the training kit that you just mentioned. Oh, it came?

Randy True  [43:56](https://vimeo.com/654504246/b9130720de?ts=2636000)
Oh yeah, that's because that was with the...

Speaker 3  [43:58](https://vimeo.com/654504246/b9130720de?ts=2638000)
With the other, okay, yeah.

Randy True  [44:01](https://vimeo.com/654504246/b9130720de?ts=2641000)
Oh, and also the printouts and the paperwork are with that. Okay.

Speaker 0  [44:09](https://vimeo.com/654504246/b9130720de?ts=2649000)
Yep.

Speaker 3  [44:14](https://vimeo.com/654504246/b9130720de?ts=2654000)
What do you think? Should we get started in the lab?

Randy True  [44:18](https://vimeo.com/654504246/b9130720de?ts=2658000)
Sure, I think, yeah, showing the team what this actually looks like would be good. I think in terms of just talking about the big picture, I think I mentioned the Florida deployments have been going really well and successful for two plus months now, beginning of August, beginning of December, almost three months. And those were, Danny and Adam had never touched a pipette before. And so they learned totally from scratch. They were they were dedicated to, to running this as a key part of their job every, every day. So there is, you know, there is a learning curve, but I understand that this is kind of intimidating and I made the mistake of having all of the materials out for our Sacramento deployment when the fire chiefs from several different stations came and they were like, oh man, this is too much for us. So I don't want you all to be overly intimidated by this. And for sure, if any of you want to learn it and run it, you absolutely can. But it's my understanding that y'all are planning to run once a week. And if that's the case, I would recommend that we get a volunteer or we hire a contractor to run this because it'll just take them two hours to do it. And this is so easy to do for anybody who has spent time at a bench, even a first year grad student, this is just a piece of cake for. So, and that would allow you guys to focus on just on getting the samples, running the program, which is not a negligible part of it, you know. After Adam finally kind of turned the corner, the firefighter and Davey, he said, oh yeah, the Wrangell in the sample collection, they, you know, that comes from like seven different stations for one. He's like, that's way harder than doing the test. So I think that's just something to consider here is in terms of how y'all wanna use this and how y'all wanna run it. And if you do end up ramping up and wanting to do significantly more testing, I think there's probably opportunity to collaborate with folks from OHSU. Kevin said he's got connected now to five professors who are interested in understanding this test and kind of what we're doing here. So it's, yeah, I think there's some options in terms of how y'all want to run this, what y'all want to do.

Speaker 2  [47:02](https://vimeo.com/654504246/b9130720de?ts=2822000)
Where's your, I guess the budget at? I think we need

Speaker 0  [47:06](https://vimeo.com/654504246/b9130720de?ts=2826000)
to see the budget and see those what I'm hearing this is going to be easier for us to run these tests than us. Well, I guess I would

Randy True  [47:14](https://vimeo.com/654504246/b9130720de?ts=2834000)
have wanted to run everybody in the room

Speaker 3  [47:15](https://vimeo.com/654504246/b9130720de?ts=2835000)
because everybody in

Speaker 0  [47:15](https://vimeo.com/654504246/b9130720de?ts=2835000)
the room because

Speaker 2  [47:18](https://vimeo.com/654504246/b9130720de?ts=2838000)
where's their comfortability with this right?

Speaker 0  [47:21](https://vimeo.com/654504246/b9130720de?ts=2841000)
Because I mean obviously what was the chance

Speaker 2  [47:24](https://vimeo.com/654504246/b9130720de?ts=2844000)
to do between you and it probably is it's a little intimidating with the slides to see that But here's what I'm at least thinking that one, if Katrina wants to job with us, we may be contract with her for at least the first month. So we can get everybody to train with her and go through this a few times each, because even if we do run up twice a week, we're only going to get our hands on the road. That might be

Speaker 0  [47:57](https://vimeo.com/654504246/b9130720de?ts=2877000)
more comfortable for us and more successful.

Randy True  [48:00](https://vimeo.com/654504246/b9130720de?ts=2880000)
Peter, I would recommend you all to have one person to kind of become proficient with it in the lab. The others can know it and know they could learn it over even a day if you practice a lot that day. But I just think having one person focus on it might make the most sense. And you know, it's, you know, some of this is, is, is, is personality and kind of attention to detail. It's really not like scientific knowledge or background. There were two actual firefighters assigned to the the Davey project and Adam sent me photos of him getting the lab set up. They shipped the stuff from the summer camp and he had all the bottles arranged in the cabinet perfectly in line. He had everything set out on the tables, all organized. And I was like, oh, he's gonna do great. And the other guy who was assigned, I actually, I didn't end up interacting with him much, but Adam just told me he wasn't into it and wasn't interested. But also it was the situation where Adam was tapped to do this as a key part of his job. And so we had another situation in Sacramento was it was a director level person who was involved with being tapped to train to do it. He was just pulled in a lot of directions. He just didn't have enough bandwidth. So there, you know, I'm sort of just, I'm giving you what we've learned in doing this over the last few months and kind of our thoughts on, on, you know, what might work well and where, where you might have, you know, kind of more hiccups. So, I think, I think perhaps it might help for y'all to see it and kind of understand what's involved. So I think maybe we could just go and pop into the lab and Trina can kind of give you a little bit of a tour and show you what this actually looks like.

Speaker 0  [50:00](https://vimeo.com/654504246/b9130720de?ts=3000000)
Yeah, I agree. I think the one thing that we're faced against here right now is just the staffing shortage. We don't have the ability to assign one person. If I put Pete on this, it's going to take multiple hours a week away from his job, or myself, or we can't pull either of these guys off of mine. So my thought is to like try to spread that wealth a little bit and help out where we can. You know, Pete's stationed out here, these guys have been stationed out here or close to while they're on shift. I could take that time and go to wait and run these tests or something like that. I don't see any reason why we're changing. I mean, we do stuff all the time and it's procedure based.

Randy True  [50:45](https://vimeo.com/654504246/b9130720de?ts=3045000)
Yeah, I think it's a

Speaker 0  [50:48](https://vimeo.com/654504246/b9130720de?ts=3048000)
procedure. Yeah, I think we get in the lab and take a look but we selected these guys, because of their attention to detail, and their passion for this part of it. That's where I'm comfortable with all of us in the area. I had somebody who was a slacker you care about it. Yeah, be concerned.

Speaker 2  [51:11](https://vimeo.com/654504246/b9130720de?ts=3071000)
Great. I don't want to push you to something you don't want

Speaker 0  [51:13](https://vimeo.com/654504246/b9130720de?ts=3073000)
to do. Oh, we're here for. Yeah. Ben.

Speaker 3  [51:18](https://vimeo.com/654504246/b9130720de?ts=3078000)
Yeah, that's fine. Okay. Great. Okay.

Randy True  [51:22](https://vimeo.com/654504246/b9130720de?ts=3082000)
See it? I have your

Speaker 3  [51:23](https://vimeo.com/654504246/b9130720de?ts=3083000)
other hand.

Randy True  [51:30](https://vimeo.com/654504246/b9130720de?ts=3090000)
You guys can just switch and turn on the mic on the other laptop. Turn the mic on.

Speaker 3  [51:34](https://vimeo.com/654504246/b9130720de?ts=3094000)
Yeah. Should they get gloves, coats, gowns on?

Randy True  [51:39](https://vimeo.com/654504246/b9130720de?ts=3099000)
I think it's just if you have bare sleeves, just be extra careful not to get your forearms on anything and just put on gloves.

Speaker 3  [51:47](https://vimeo.com/654504246/b9130720de?ts=3107000)
And put on gloves. Yeah. And then once you put your, actually, we probably don't even need the glasses if we don't have the inactivation solution. Is that right? Yeah, I think you're fine.

Randy True  [51:57](https://vimeo.com/654504246/b9130720de?ts=3117000)
I think you're fine. OK.

Speaker 3  [51:59](https://vimeo.com/654504246/b9130720de?ts=3119000)
Yeah. But we don't need face shields. No, we have shields right now. Yeah, but the paint, chemical, not here. It's on the way. OK. 123.

