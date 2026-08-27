[13:47, 07/07/2026] Praveen Kulkarni: Hi
[13:48, 07/07/2026] sikander peter friend forwarder: hi
[16:40, 08/07/2026] sikander peter friend forwarder: okay I talked with peter, 

The direction became clearer, I think there is no way around the spring boot environment
[16:41, 08/07/2026] sikander peter friend forwarder: we need to support eft, edifact and ecmr frameworks and the core is all from a spring boot initiative
[16:42, 08/07/2026] Praveen Kulkarni: we need to support eft, edifact and ecmr frameworks and the core is all from a spring boot initiative
Can you send me links for all this ... In general would like to know how europe ecosystem is organized
[16:42, 08/07/2026] sikander peter friend forwarder: if there is really a big shortage of spring boot developers in your network, we could only study and research how much effort it takes to migrate and port the frameworks to nestjs/ typescript
[16:43, 08/07/2026] sikander peter friend forwarder: https://github.com/EFTI4EU/reference-implementation
[16:43, 08/07/2026] Praveen Kulkarni: Can you send me links for all this ... In general would like to know how europe ecosystem is organized
Understand that I am not aware of this things .... But I have a friend who is having 10 years of experience in springboot and working at JP Morgan .... I can consult him as well
[16:46, 08/07/2026] Praveen Kulkarni: https://github.com/EFTI4EU/reference-implementation
Just a naive thought even if it is springboot core we can spin it as a server and just connect it via any stack we have with rest endpoints in springboot.... Yes in start it will be double hop but better than migrating code bases
[16:48, 08/07/2026] sikander peter friend forwarder: yes we can also connect with it through api, but this would be maintaining two services in two languages
[16:48, 08/07/2026] Praveen Kulkarni: yes we can also connect with it through api, but this would be maintaining two services in two languages
Yes that's the double hop i said .... But looks like the link u sent itself is a new initiative
[16:48, 08/07/2026] sikander peter friend forwarder: since it is the same bounded context, it is less headache to develop that in one language
[16:49, 08/07/2026] Praveen Kulkarni: It looks something new in Europe opensource ecosystem.... So I don't mind studying it
[16:49, 08/07/2026] sikander peter friend forwarder: yes this becomes standard, the first laws are already passed and 2027 ongoing it becomes requirement
[16:51, 08/07/2026] Praveen Kulkarni: Don't mind but I will talk with few people working in springboot.... I like such initiatives .... I will get back in 5-6 days ....
[16:52, 08/07/2026] Praveen Kulkarni: Are there any other things like this .... Means opensource standards for digitalization
[16:53, 08/07/2026] sikander peter friend forwarder: you need 5-6 days for networking ? 

yes find some spring boot people. I also don’t mind to mentor them for the beginning, but they need intermediate programming skills, so they should know event driven designs
[16:53, 08/07/2026] sikander peter friend forwarder: so a good typsescript developer is more valuable as a java beginner
[16:54, 08/07/2026] sikander peter friend forwarder: especially if they developed in nest js, like I said nest js and spring boot have both the same mental model and concepts
[16:54, 08/07/2026] sikander peter friend forwarder: yes just chck the unece.org website they are publishing the recommendations and frameworks
[16:55, 08/07/2026] Praveen Kulkarni: Something similar is happening in india under ondc ... But it's still chaotic .... I hope the eu thing is more organized
[16:55, 08/07/2026] sikander peter friend forwarder: no
[16:56, 08/07/2026] sikander peter friend forwarder: same chaos but the laws are forcing logistics companies into the framework. It will still take time
[16:56, 08/07/2026] sikander peter friend forwarder: maybe not that chaotic like in india, but it is a big mess
[16:57, 08/07/2026] Praveen Kulkarni: I will need to read this
[19:54, 11/07/2026] sikander peter friend forwarder: hola
[19:56, 11/07/2026] sikander peter friend forwarder: hello
[19:56, 11/07/2026] sikander peter friend forwarder: you have something for me already? we want to have a meeting tomorrow/
[19:57, 11/07/2026] Praveen Kulkarni: tomorrow is sunday
[19:57, 11/07/2026] Praveen Kulkarni: peter is meeting you ??
[19:57, 11/07/2026] sikander peter friend forwarder: yes tomorrow is sunday
[19:58, 11/07/2026] Praveen Kulkarni: u can demo the project as it is .... and see if u want changes ..... and decide nestjs vs springboot
[19:58, 11/07/2026] sikander peter friend forwarder: yes we want to continue with the next phase
[19:58, 11/07/2026] Praveen Kulkarni: i will get my resource onboard next month start again
[19:58, 11/07/2026] sikander peter friend forwarder: spring boot?
[19:59, 11/07/2026] Praveen Kulkarni: i am reading through the github repo u sent
[20:00, 11/07/2026] Praveen Kulkarni: spring boot?
u were saying right you want it to be in nestjs
[20:00, 11/07/2026] sikander peter friend forwarder: yes would be god if you have read it and can join tomorrow as well online
[20:00, 11/07/2026] sikander peter friend forwarder: u were saying right you want it to be in nestjs
?
[20:01, 11/07/2026] Praveen Kulkarni: tomorrow is sunday
yes thats why i said its sunday ..... this week was hectic for me .... so i am out on sunday
[20:02, 11/07/2026] Praveen Kulkarni: ?
the current code is in sveltekit with postgres ..... do you think we need to migrate to nest js ??
[20:02, 11/07/2026] Praveen Kulkarni: what if you both discuss tomorrow and come with major drawbacks with current design ..... or want any changes
[20:03, 11/07/2026] Praveen Kulkarni: when are you people meeting ?? .... i will see if i can join
[20:04, 11/07/2026] sikander peter friend forwarder: the current work is just a demo? nothing works anyways. there is no drawbacks, or did you invest in a ui system or any infrastructure ?
[20:04, 11/07/2026] sikander peter friend forwarder: svelte is portable we can reuse, the postgres is just 3 tables
[20:04, 11/07/2026] Praveen Kulkarni: the current work is just a demo? nothing works anyways. there is no drawbacks, or did you invest in a ui system or any infrastructure ?
the database is functional right ?? means the tracking happens in db
[20:05, 11/07/2026] Praveen Kulkarni: the bidding logic endpoints exist and you can add any buisness logic there
[20:06, 11/07/2026] Praveen Kulkarni: the photo upload is fake  ..... but then can be implememented when you have clear requirements for AI
[21:35, 12/07/2026] sikander peter friend forwarder: you have the all inkl domain account of peter right? Can you share the access ?
[08:47, 13/07/2026] Praveen Kulkarni: Hi Good morning
[08:48, 13/07/2026] Praveen Kulkarni: https://all-inkl.com/members/
732701
zAKcjku.ic27zkL
[08:51, 13/07/2026] Praveen Kulkarni: I have not made any changes there. I assume adding subdomains is not a free feature there.
[19:31, 18/07/2026] Praveen Kulkarni: I checked this repo https://github.com/EFTI4EU/reference-implementation
Based on reading I assume it is more about regulatory information exchange flow while the current app only focuses on marketplace.
As they have mentioned this is reference implementation. And I think evolving things with current stack might still be practical.
Need to add things like:
+ explicit eFTI common data model mapping layer, 
+ access flow for authorities, 
+ integration path to external gate ecosystems that will evolve
+ adhering to eFTI audit requirements
[19:34, 18/07/2026] Praveen Kulkarni: Also one note: While developing in sveltekit I have made sure that vercel cloud functions are not called. That way it never hurts in billing and dependency. It is just pure sveltekit app with hosting on vercel for development.
[20:03, 18/07/2026] Praveen Kulkarni: Next possible steps:
+ We need to figure out which regulatory flow features are more important.
+ Need to know if there are any companies having active external gate ecosystems and if we can access it.
+ I have a friend who will track the fullstack development instead of me. He manages springboot application at JP Morgan and can guide the resources. He also has interest in EFTI4EU as well. Obviously I will be there and will be more of guiding in AI development, image analysis or any agentic AI work.
+ As already communicated resource will most likely be available in start of next month.
[11:49, 22/07/2026] sikander peter friend forwarder: good morning
[11:50, 22/07/2026] sikander peter friend forwarder: is the latest in the repository ?
[11:50, 22/07/2026] sikander peter friend forwarder: how are you ?
[11:50, 22/07/2026] sikander peter friend forwarder: Next possible steps:
+ We need to figure out which regulatory flow features are more important.
+ Need to know if there are any companies having active external gate ecosystems and if we can access it.
+ I have a friend who will track the fullstack development instead of me. He manages springboot application at JP Morgan and can guide the resources. He also has interest in EFTI4EU as well. Obviously I will be there and will be more of guiding in AI development, image analysis or any agentic AI work.
+ As already communicated resource will most likely be available in start of next month.
I think I will take care of the infrastructure of the efti framework as convenient part to connect to the driver platform
[11:19, 27/07/2026] Praveen Kulkarni: is the latest in the repository ?
Ohh sorry .... I just saw ur last statement and missed your question
[11:21, 27/07/2026] Praveen Kulkarni: Repositories don't have much important changes. I will first get my resource onboard then have one friend who can further manage the project.
[11:23, 27/07/2026] Praveen Kulkarni: I will then arrange further meetings between all.
[18:56, 03/08/2026] sikander peter friend forwarder: hello your developers are now available again right ?
[18:56, 03/08/2026] sikander peter friend forwarder: can we arrange a call ?
[19:00, 03/08/2026] Praveen Kulkarni: yes it is first day, he is going through new code changes I did. Also the other person who will manage fullstack instead of me is coordinating with him. Once the things are sorted here I will arrange meeting.
[19:48, 03/08/2026] Praveen Kulkarni: Missed voice call
Did u call me accidentally
[19:49, 03/08/2026] sikander peter friend forwarder: could be
[19:49, 03/08/2026] sikander peter friend forwarder: im right now in the workshop
[19:50, 03/08/2026] sikander peter friend forwarder: We will coordinate with them
[19:50, 03/08/2026] sikander peter friend forwarder: they don’t need to coordinate
[19:50, 03/08/2026] sikander peter friend forwarder: First a meeting
[11:07, 04/08/2026] Praveen Kulkarni: We can decide on meeting slot timings tomorrow evening. 
We had planned meeting today but one person took off so it is postponed tomorrow. 
Basically I am handing over the project to another experienced person and he will be responsible for coordination. 
He has 15+ years experience and he has coordinated with me on some other projects earlier. 
This can help me use my skills where it is needed.

https://www.linkedin.com/in/palashn/
[16:22, 04/08/2026] sikander peter friend forwarder: okay give him my contact to send me a message
[16:22, 04/08/2026] sikander peter friend forwarder: first we need a meeting with the developers, asap all the ones whih are available from your side
[21:36, 04/08/2026] sikander peter friend forwarder: yoy found availability ?
[21:50, 04/08/2026] Praveen Kulkarni: We can decide on meeting slot timings tomorrow evening. 
We had planned meeting today but one person took off so it is postponed tomorrow. 
Basically I am handing over the project to another experienced person and he will be responsible for coordination. 
He has 15+ years experience and he has coordinated with me on some other projects earlier. 
This can help me use my skills where it is needed.

https://www.linkedin.com/in/palashn/
""" We can decide on meeting slot timings tomorrow evening. """
As mentioned i can message you tomorrow evening about fixing meeting with you. Todays meeting did not happen so we are doing it tomorrow. That meeting is between me and Palash as I want him to handle full stack.
[21:54, 04/08/2026] sikander peter friend forwarder: first we need to find out if he is suitable or not thats why we need meeting, it does not make sense to onboard him if he does not have the required skills
[21:56, 04/08/2026] sikander peter friend forwarder: okay we will arrange a meeting tomorrow evening
[20:02, 05/08/2026] sikander peter friend forwarder: hello you have an appointment time already ?
[21:24, 05/08/2026] Praveen Kulkarni: Hi Skander,

I said I would have a meeting with Palash and some people here to make arrangements for you. Sorry I couldn't meet them earlier this week because one of the people who will be working under Palash had to take emergency leave, even after being away for a month due to genuine reasons.

The meeting was not scheduled with you. My plan was to first discuss everything internally and then ask you for a meeting. After a long discussion, this is what we have summarized.

First, we need a *BRD (Business Requirement Document)* from you and Peter.

Second, we need to decide the mode of operation:

* Shared-basis resources
* Full-time dedicated resources

I just finished the meeting with Palash.

He is an old friend of mine, and we have a long professional relationship, so he has agreed to help me manage the project. He is doing this as a favor to me until the project stabilizes.

He is not available for hire, as he is already very well paid. I shared his profile because he will be managing my resources for the project and coordinating with you on the full-stack work once a week.

My current resources have been selected through a lot of hiring effort, and they have an established professional relationship with me. I can make them available on a shared basis, as they are already involved in my other projects. Palash can manage them from here on a milestone-by-milestone basis, and he understands the work culture here.

If you want dedicated developers, we'll need to post job advertisements and hire people exclusively for your project on fixed-term contracts, with options for extension. This is possible, but in that case you will need to take responsibility for quality checks and resource management, as both hiring and project management are full-time responsibilities. We can provide basic on-ground coordination.
[23:41, 05/08/2026] sikander peter friend forwarder: Hi Praveen,

Let's realign on the next steps so we can get this project moving.
First, regarding the engagement model: I am not looking to choose between a 'shared' or 'dedicated' team, nor am I looking to manage external resources or pay for an ongoing milestone contract. Since the initial 2000€ was paid for full-stack development that hasn't been completed, the sole focus right now is finding competent developers from your network who can actually write the code.

My priority is quality and capability over speed. However, I need to interview the actual developer who will be doing the coding asap. If Palash is only managing resources, I do not need to speak with him.

Second, regarding the BRD: I agree that clear requirements are essential, and we will absolutely provide a detailed BRD. However, we are currently at Stage 0. The immediate focus for the replacement developer will be setting up the foundational infrastructure and building upon the direction of the existing demo.

Once we have successfully vetted the developers, established the core infrastructure, and signed an NDA, we will provide the full BRD for the detailed features.

Please let me know what time I can interview the developer. If you cannot provide competent developers for me to speak with until Friday, I will consider this contract breached and we will move immediately to the refund process for the 2000€.
Hello Praveen,

first of all, thank you for the cooperation. Unfortunately, we can't continue - as announced you missed presenting a competent developer. Therefore, in agreement and consultation with Peter, we decided to end the project with you and formally demand a full refund within 14 days of receipt of the attached letter.

Worth noting: we provided a technical assessment of the code also for you as feedback - to learn, for future projects, what is missing for professional software. With focused effort, this can elevate you and help you grow.

Please confirm receipt and initiate the transfer to the account specified in the letter (IBAN DE11 5001 0517 5425 8822 07). We would also appreciate written confirmation once the transfer is executed.

Thank you and kind regards,

Skander
[16:32, 12/08/2026] Praveen Kulkarni: i have emailed you and peter.
[18:54, 12/08/2026] sikander peter friend forwarder: Hi praveen, 

alright I will read it as soon as I can 👍 
Thank you
[11:18, 13/08/2026] sikander peter friend forwarder: hi praveen, 

hope all is good with you and your family! 

Regarding the email, Peter showed me what he sent and I just want to confirm this. So you can let us know what your decision is
[17:13, 14/08/2026] sikander peter friend forwarder: hi praveen, 

any updates ?
[10:27, 17/08/2026] sikander peter friend forwarder: ?
[16:18, 18/08/2026] sikander peter friend forwarder: Hi,

We Need a decision from you praveen
[16:19, 18/08/2026] Praveen Kulkarni: i have emailed peter yesterday.
[17:22, 18/08/2026] sikander peter friend forwarder: Ok I’ll talk with him