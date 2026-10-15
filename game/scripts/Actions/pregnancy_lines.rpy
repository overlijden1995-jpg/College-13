## pregnancy_lines.rpy -- DATA ONLY: in-scene pregnancy line pools.
## Read by _fert_pick_scene_line() in pregnancy.rpy: _FERT_SCENE_LINES[gid or "_default"]["<group>.<state>"].
## groups: moan, inside_ok, inside_no, inside_react, inside_forced, aftermath, pull_out, cum_condom, creampie_req, condom_ask
## states: pregnant_known, preg_fetish(_condom), preg_fear(_raw/_pill/_condom), no_protection, on_pill
## A girl without an entry (or without a pool) falls back to "_default". Lines must never mention cycle timing.
## PT/ES: game/tl/{pt,es}/scripts/Actions/pregnancy_lines.rpy

init python:

    _FERT_SCENE_LINES = {
        "_default": {
            "moan.pregnant_known": [
                _("Mmm... nothing to worry about anymore. Just fuck me as deep as you want."),
                _("Ahh... I'm already carrying your baby. You can't knock me up twice, so don't hold back."),
            ],
            "moan.preg_fetish": [
                _("Nngh... raw feels so right. Every thrust, I think about you putting a baby in me."),
                _("Ahh, yes... please, get me pregnant. I need it so bad."),
            ],
            "moan.preg_fetish_condom": [
                _("Mmm... it feels good, but I hate that rubber. It's keeping you from knocking me up."),
                _("Ahh... I can barely feel you through that thing. I wish you'd just take it off and fill me up."),
            ],
            "moan.preg_fear_raw": [
                _("Ahh... it feels so good, and that's what scares me. Please, don't finish inside me."),
                _("Nngh... I'm not on the pill, remember that. Pull out early, I'm begging you."),
            ],
            "moan.preg_fear_pill": [
                _("Mmm... the pill is the only reason I'm letting you do this raw. Still, be careful."),
                _("Ahh... I took my pill, I took my pill... nngh, I still can't fully relax."),
            ],
            "moan.preg_fear_condom": [
                _("Mmm... with the condom I can actually enjoy this. It's still on, right?"),
                _("Ahh... wait, let me feel... okay, the condom didn't slip. Keep going, nngh..."),
            ],
            "moan.no_protection": [
                _("Ahh... this is so good, but we have nothing. You have to pull out, okay?"),
                _("Mmm... I keep thinking about it. I'm not on the pill, so you really can't lose control."),
            ],
            "moan.on_pill": [
                _("Mmm... I love feeling you raw. The pill has me covered, so just enjoy it."),
                _("Ahh... nothing between us, this is so much better. Good thing I'm on the pill."),
            ],
            "inside_ok.pregnant_known": [
                _("Go ahead. I'm already pregnant, it makes no difference now."),
                _("Mmm, cum inside. What's the worst that could happen, I get more pregnant?"),
            ],
            "inside_ok.preg_fetish": [
                _("Yes, yes! Cum inside me, all of it. I want your baby."),
                _("Don't you dare waste a drop. Pump it deep, I want it to take."),
            ],
            "inside_ok.on_pill": [
                _("Sure, I'm on the pill. Finish inside me."),
                _("It's fine, the pill takes care of it. I want to feel you cum in me."),
            ],
            "inside_ok.preg_fear_pill": [
                _("Okay... okay. I'm on the pill, it should be fine. Just do it before I change my mind."),
                _("I never miss a pill, so... fine. God, I can't believe I'm saying yes to this."),
            ],
            "inside_no.preg_fear_raw": [
                _("No! Absolutely not! I'm not on the pill, you are not cumming inside me!"),
                _("Are you crazy? I could get pregnant! Not inside, never inside!"),
            ],
            "inside_no.preg_fear_pill": [
                _("No. The pill isn't a hundred percent and I'm not gambling on it."),
                _("I know I'm on the pill, but pills fail. Not inside, I mean it."),
            ],
            "inside_no.no_protection": [
                _("No way. I'm not on the pill, I could actually get pregnant."),
                _("Not inside. I'm not taking anything, and I'm not ready to be a mom."),
            ],
            "inside_react.pregnant_known": [
                _("Mmm... so warm. One perk of already being pregnant, I get to just enjoy this."),
                _("Ahh... well, the damage was already done. Fill me up whenever you like."),
            ],
            "inside_react.preg_fetish": [
                _("Ahh, yes! I can feel it all inside me... please, let this be the one."),
                _("Mmm... so much of it, so deep. I hope you just made me a mom."),
            ],
            "inside_react.on_pill": [
                _("Mmm... I love that warm feeling. Relax, the pill has it handled."),
                _("Ahh... you really filled me up. This is exactly why I stay on the pill."),
            ],
            "inside_react.preg_fear_pill": [
                _("Oh god, you really did it... the pill works. The pill works. Right?"),
                _("Why did I say yes... no, it's okay. I'm on the pill. It has to be enough."),
            ],
            "inside_react.no_protection": [
                _("Ahh... wait. What did I just let you do? I'm not even on the pill..."),
                _("Oh no... it's all in me and we used nothing. What was I thinking?"),
            ],
            "inside_forced.preg_fear_raw": [
                _("No, no, no! I told you not inside! I'm not on the pill, do you get what you just did?"),
                _("Get away from me! This is my worst nightmare, I could be pregnant because of you!"),
            ],
            "inside_forced.preg_fear_pill": [
                _("I said no! You'd better pray that pill works, because I will never forgive you if it doesn't."),
                _("How could you? The pill is the only thing between me and a disaster right now!"),
            ],
            "inside_forced.no_protection": [
                _("What the hell? I told you to pull out! I'm not on the pill, I could get pregnant from this!"),
                _("You asshole, we had nothing! If I end up pregnant, that's on you."),
            ],
            "inside_forced.on_pill": [
                _("Being on the pill doesn't mean you get to do that. I said no."),
                _("I won't get pregnant, fine. That's not the point. You ignored me, and that pisses me off."),
            ],
            "aftermath.pregnant_known": [
                _("Hah... give me a second to breathe. At least cleaning up is the only thing left to worry about."),
                _("Mmm... the baby's going to have a very relaxed mom today."),
            ],
            "aftermath.preg_fetish": [
                _("I'm not moving yet. I want to keep every drop inside as long as I can."),
                _("Mmm... I keep picturing my belly getting big. Do you think it worked?"),
            ],
            "aftermath.on_pill": [
                _("Hah... that was great. No stress, no worries, just how I like it."),
                _("Mmm... I can feel it dripping out. Worth every pill I've ever taken."),
            ],
            "aftermath.preg_fear_pill": [
                _("I did take my pill today, right? I'm checking the pack as soon as I can stand."),
                _("My heart won't slow down, and it's not from the sex. I'm on the pill, I keep telling myself that."),
            ],
            "aftermath.no_protection": [
                _("We really shouldn't have done that. I need a morning after pill, like, today."),
                _("It felt amazing, and now I just feel stupid. No pill, no condom... what if it takes?"),
            ],
            "pull_out.pregnant_known": [
                _("You know you didn't have to pull out, right? I'm already pregnant."),
                _("Sweet of you, but pointless. You can't get a pregnant girl pregnant."),
            ],
            "pull_out.preg_fetish": [
                _("Why did you pull out? I wanted it inside me, all of it."),
                _("Seriously? That could have been our baby. Next time you stay in."),
            ],
            "pull_out.preg_fear": [
                _("Oh thank god, you pulled out. Thank you, really, thank you."),
                _("Hah... I can finally breathe. You have no idea how much that means to me."),
            ],
            "pull_out.no_protection": [
                _("Good, you pulled out in time. With nothing protecting us, I was getting nervous."),
                _("Thanks for being careful. I'm not on the pill, so that really mattered."),
            ],
            "pull_out.on_pill": [
                _("You could have stayed in, you know. I'm on the pill, pulling out was optional."),
                _("Such a gentleman. I take the pill every day, so you can skip that part next time."),
            ],
            "cum_condom.preg_fetish_condom": [
                _("All that cum, stuck in a piece of rubber. What a waste."),
                _("Next time, no condom. I want that inside me, where it can actually do something."),
            ],
            "cum_condom.preg_fear_condom": [
                _("Thank god for that condom. Can you check it didn't break? Please."),
                _("Hah... it all stayed in the condom, right? Okay. Good. I can relax now."),
            ],
            "creampie_req.preg_fetish": [
                _("Promise me you'll finish inside. I want you to knock me up, right now."),
                _("When you cum, don't pull out. Stay deep and breed me, I'm asking you."),
            ],
            "condom_ask.preg_fetish_condom": [
                _("Take the condom off. Please, I want your baby, and that thing is in the way."),
                _("Stop for a second and take it off. I need you to cum in me for real, I want to get pregnant."),
            ],
        },
        "gwen": {
            "moan.pregnant_known": [
                _("Mmm... go as deep as you want. Damage is already done, remember?"),
                _("Ahh... you already knocked me up, so quit holding back."),
            ],
            "moan.preg_fetish": [
                _("Nngh... don't you dare pull out. Put a baby in me, damn it."),
                _("Ahh... raw like this, all I can think about is you knocking me up. Do it."),
            ],
            "moan.preg_fetish_condom": [
                _("Mmm... feels good, but I hate that stupid rubber. Take it off and breed me."),
                _("Nngh... that condom is wasting everything I want. Lose it already."),
            ],
            "moan.preg_fear_raw": [
                _("Ahh... it's good, fine, but be careful. I'm not on the pill, don't you finish in me."),
                _("Nngh... shit, I'm serious, warn me before you cum. I am not ending up pregnant, okay?"),
            ],
            "moan.preg_fear_pill": [
                _("Mmm... the pill is the only reason you're in me bare. Don't make me regret it."),
                _("Ahh... I took my pill, I know I took it... shut up, brain. Just keep going."),
            ],
            "moan.preg_fear_condom": [
                _("Nngh... the condom's still on, right? Okay. Then keep going, harder."),
                _("Mmm... with the rubber on I can almost relax. Almost. Let me feel it's still there."),
            ],
            "moan.no_protection": [
                _("Ahh... fuck, that's good... wait, we've got nothing. You have to pull out."),
                _("Mmm... don't get lost in there, genius. I'm not on the pill, remember?"),
            ],
            "moan.on_pill": [
                _("Mmm... raw is so much better. Thank the pill and keep fucking me."),
                _("Ahh... I can feel all of you. Best thing that little pill ever did for me."),
            ],
            "inside_ok.pregnant_known": [
                _("Go ahead. What's it going to do, get me pregnant twice?"),
                _("I'm already carrying your kid, dumbass. Cum wherever you want."),
            ],
            "inside_ok.preg_fetish": [
                _("Yes. Every drop, as deep as you can. I want your baby."),
                _("You even have to ask? Fill me up and knock me up already."),
            ],
            "inside_ok.on_pill": [
                _("Sure, I'm on the pill. Knock yourself out."),
                _("Relax, the pill's got me covered. Cum inside, I want to feel it."),
            ],
            "inside_ok.preg_fear_pill": [
                _("Okay... okay, fine. I'm on the pill. It works. It has to work."),
                _("God, I can't believe I'm saying yes. The pill better do its damn job."),
            ],
            "inside_no.preg_fear_raw": [
                _("No! No, no, absolutely not. I'm not on anything, you cum outside!"),
                _("Are you insane? I am not getting pregnant. Outside, or we stop right now."),
            ],
            "inside_no.preg_fear_pill": [
                _("No. The pill isn't a hundred percent and I'm not betting my life on it."),
                _("Pills fail, okay? I'd lose my mind waiting to find out. Pull out."),
            ],
            "inside_no.no_protection": [
                _("Nice try. I'm not on the pill, so no. Outside."),
                _("Not happening. I can actually get pregnant, you know. Pull out when it's time."),
            ],
            "inside_react.pregnant_known": [
                _("Mmm... warm. Nice perk of being pregnant, zero things to freak out about."),
                _("Ahh... that's a lot. Too late to matter, so I'll just enjoy it."),
            ],
            "inside_react.preg_fetish": [
                _("Ahh... yes, I can feel it all. Please let this one take."),
                _("Nngh... so deep. If that doesn't get me pregnant, we go again."),
            ],
            "inside_react.on_pill": [
                _("Mmm... I love that feeling. Pill's on duty, so no drama."),
                _("Ahh... hot and messy, just how I like it. Let the pill worry about the rest."),
            ],
            "inside_react.preg_fear_pill": [
                _("Oh god, you really did it. It's fine. I'm on the pill. It's fine, right?"),
                _("Why did I say yes... no, the pill works. Millions of girls trust it. Breathe."),
            ],
            "inside_react.no_protection": [
                _("Fuck... what did I just let you do? We had nothing. Nothing."),
                _("Great. No pill, no condom, and I said yes. Real genius move from me."),
            ],
            "inside_forced.preg_fear_raw": [
                _("I said no! I'm not on the pill, you asshole! What the fuck did you do?!"),
                _("Get out of me! This is the one thing I begged you not to do... oh god, oh god."),
            ],
            "inside_forced.preg_fear_pill": [
                _("I told you not to! If that pill fails, I swear I will end you."),
                _("You bastard. The pill is all I have now, and you didn't even care."),
            ],
            "inside_forced.no_protection": [
                _("Are you kidding me? I'm not on the pill! You could've just gotten me pregnant!"),
                _("I said outside, asshole. Now I get to sit around wondering if you knocked me up."),
            ],
            "inside_forced.on_pill": [
                _("Being on the pill doesn't mean you get to ignore me. I said no, asshole."),
                _("The pill covers pregnancy. It doesn't cover you being a disrespectful prick."),
            ],
            "aftermath.pregnant_known": [
                _("Hah... give me a second. Growing a person and keeping up with you is a workout."),
                _("Mmm... no panic, no pharmacy run, nothing. I could get used to this part."),
            ],
            "aftermath.preg_fetish": [
                _("Don't move me. I'm keeping every drop in there until it sticks."),
                _("Mmm... picture me with a big round belly. Yeah, I'm thinking about it too."),
            ],
            "aftermath.on_pill": [
                _("Hah... okay, that was good. Pill did its job, you did yours."),
                _("Mmm... I'm a mess and I don't even care. Perks of staying on the pill."),
            ],
            "aftermath.preg_fear_pill": [
                _("I took my pill today, right? I did. I'm still checking the pack in a minute."),
                _("Stop smiling. I'm over here doing pill failure rates in my head."),
            ],
            "aftermath.no_protection": [
                _("Okay, that was stupid. Hot, but stupid. I need a morning after pill."),
                _("Shit... it's really sinking in now. You're coming to the pharmacy with me."),
            ],
            "pull_out.pregnant_known": [
                _("Cute. You pulled out of a girl who's already pregnant. Very responsible."),
                _("You didn't have to bother. The baby's already in there, so next time finish inside me."),
            ],
            "pull_out.preg_fetish": [
                _("Seriously? On my skin? That was supposed to go in me."),
                _("Ugh, all that, gone for nothing. I wanted you to breed me, not decorate me."),
            ],
            "pull_out.preg_fear": [
                _("Oh thank god. Thank you. Seriously, you have no idea how scared I was."),
                _("You actually pulled out... okay, I can breathe again. You earned points for that."),
            ],
            "pull_out.no_protection": [
                _("Good timing. With nothing protecting us, that's exactly where it belongs."),
                _("Look at you, being careful. I'm not on the pill, so yeah, I appreciate it."),
            ],
            "pull_out.on_pill": [
                _("You know I'm on the pill, right? You could've stayed right where you were."),
                _("Such a gentleman. Wasted on me, though. The pill would've handled it."),
            ],
            "cum_condom.preg_fetish_condom": [
                _("All that cum, stuck in a rubber. What a waste. Next time, no condom."),
                _("I felt you throb and got nothing out of it. Lose that thing next time."),
            ],
            "cum_condom.preg_fear_condom": [
                _("Okay, good. Now pull out slow and check it didn't break. Humor me."),
                _("God bless whoever invented condoms. It's all in there, right? All of it?"),
            ],
            "creampie_req.preg_fetish": [
                _("Nngh... cum inside me. I mean it. Get me pregnant."),
                _("Ahh... stay deep when you finish. I want to walk out of here knocked up."),
            ],
            "condom_ask.preg_fetish_condom": [
                _("Mmm... stop. Take the condom off. I want your baby, not latex."),
                _("Nngh... take it off, please. I need you bare so you can actually knock me up."),
            ],
        },
        "rogue": {
            "moan.pregnant_known": [
                _("Mmm, ain't nothin' left to worry about, sugar. Your baby's already in here, so don't hold back."),
                _("Ahh... gentle now, darlin'. You already knocked me up, you can take your sweet time."),
            ],
            "moan.preg_fetish": [
                _("Lord, yes... deeper, sugar. Put a baby in me, I'm beggin' ya."),
                _("Nngh... I want you to breed me, darlin'. Fill me up 'til it takes."),
            ],
            "moan.preg_fetish_condom": [
                _("Mmm... feels good, but I hate that rubber, sugar. It's keepin' you from knockin' me up."),
                _("Ahh... I wish you'd peel that thing off, darlin'. I want you bare, makin' me a mama."),
            ],
            "moan.preg_fear_raw": [
                _("Ahh... it feels so good, but be careful, sugar. I ain't on the pill, don't you dare finish in me."),
                _("Nngh... Lord, I'm scared, darlin'. Nothin's protectin' me, so you pull out in time, hear?"),
            ],
            "moan.preg_fear_pill": [
                _("Mmm... the pill's the only reason I'm lettin' you in bare, sugar. Still got my heart poundin'."),
                _("Ahh... I took my pill, I know I did. Just go easy, darlin', I can't stop thinkin' about it."),
            ],
            "moan.preg_fear_condom": [
                _("Mmm... that's nice, sugar. Hold on, is the rubber still on? Okay... okay, keep goin'."),
                _("Ahh... I can almost relax with that condom on, darlin'. Just check it again for me, please."),
            ],
            "moan.no_protection": [
                _("Nngh... sugar, we got nothin' between us. You gotta pull out, promise me."),
                _("Ahh, Lord... I ain't on the pill, darlin'. Feels too good, but don't you lose your head."),
            ],
            "moan.on_pill": [
                _("Mmm... nothin' beats feelin' you bare, sugar. The pill's got me covered, so enjoy yourself."),
                _("Ahh... skin on skin, just how I like it. I take my pill, darlin', ain't a worry in my head."),
            ],
            "inside_ok.pregnant_known": [
                _("Go right ahead, sugar. I'm already carryin' your baby, it don't change a thing now."),
                _("Darlin', the damage is done, remember? Cum inside me all you want."),
            ],
            "inside_ok.preg_fetish": [
                _("Lord, yes! Cum in me, sugar, give me your baby. I want every drop."),
                _("You even gotta ask, darlin'? Pump it deep and knock me up, I've been achin' for it."),
            ],
            "inside_ok.on_pill": [
                _("Sure thing, sugar. I'm on the pill, so go on and finish inside me."),
                _("Mmm, I take my pill every day, darlin'. Let me feel you cum in me."),
            ],
            "inside_ok.preg_fear_pill": [
                _("I... okay. Okay, sugar. I'm on the pill, it'll hold. Do it before I change my mind."),
                _("Lord, I'm shakin'... fine, darlin'. I'm trustin' that pill with everythin' I got."),
            ],
            "inside_no.preg_fear_raw": [
                _("No! Absolutely not, sugar! I ain't on the pill, I'd die of fright. Not inside, ever!"),
                _("Don't you even think it, darlin'! I can't end up pregnant, I just can't. Not inside me!"),
            ],
            "inside_no.preg_fear_pill": [
                _("No, sugar. The pill ain't perfect, and I won't gamble my whole life on it."),
                _("I know I'm on the pill, darlin', but pills fail. Not inside, I mean it."),
            ],
            "inside_no.no_protection": [
                _("Not a chance, sugar. I ain't on the pill, you'd put a baby in me. Pull out."),
                _("Darlin', no. No pill means no finishin' inside. I ain't ready to be nobody's mama."),
            ],
            "inside_react.pregnant_known": [
                _("Mmm... warm as ever, sugar. Can't get me any more pregnant than I already am."),
                _("Ahh... that's one perk of carryin' your baby, darlin'. I get to enjoy this worry free."),
            ],
            "inside_react.preg_fetish": [
                _("Ahh, sweet Lord! I can feel it all in me, sugar. Please let this be the one that takes."),
                _("Mmm... so much of it, darlin'. I hope you just made me a mama."),
            ],
            "inside_react.on_pill": [
                _("Mmm... I love that warm rush, sugar. Don't fret, my pill's got it handled."),
                _("Ahh... that felt wonderful, darlin'. That's what I take the pill for."),
            ],
            "inside_react.preg_fear_pill": [
                _("Oh Lord... why'd I say yes? The pill works, sugar. It works. Tell me it works."),
                _("It's fine, I'm on the pill, it's fine... darlin', my hands won't stop shakin'."),
            ],
            "inside_react.no_protection": [
                _("Lord have mercy... what did I just let you do, sugar? I ain't even on the pill."),
                _("Ahh... it's all in me, and nothin' to stop it. Darlin', I must've lost my damn mind."),
            ],
            "inside_forced.preg_fear_raw": [
                _("No, no, no! I told you not inside! I ain't on the pill, you know how scared I am!"),
                _("Get away from me! Lord, this is my worst nightmare! If I end up pregnant, it's on you!"),
            ],
            "inside_forced.preg_fear_pill": [
                _("I said no! You better pray that pill holds, 'cause it's the only thing savin' you right now!"),
                _("How dare you! The pill's all I got to hang on to now, and I'm sick with fear!"),
            ],
            "inside_forced.no_protection": [
                _("Are you out of your mind? I ain't on the pill! You could've just got me pregnant!"),
                _("I told you to pull out! There's nothin' protectin' me, and you went and did it anyway!"),
            ],
            "inside_forced.on_pill": [
                _("Bein' on the pill don't mean you get to, sugar. I said no, and you ignored me."),
                _("It ain't about babies, it's about respect. My body, my call, and you just stomped on it."),
            ],
            "aftermath.pregnant_known": [
                _("Whew... give me a second, sugar. Me and the baby need to catch our breath."),
                _("Mmm... funny, ain't it, darlin'? No panic, no frettin'. Just you, me and what we made."),
            ],
            "aftermath.preg_fetish": [
                _("Don't move yet, sugar. I wanna keep it all in me, give it every chance to take."),
                _("Mmm... I'm picturin' my belly all round with your baby, darlin'. Lord, I want that."),
            ],
            "aftermath.on_pill": [
                _("Whew... that hit the spot, sugar. No worries here, I never miss my pill."),
                _("Mmm... I'm all warm and lazy now, darlin'. Good thing the pill lets us do this."),
            ],
            "aftermath.preg_fear_pill": [
                _("I did take it today, right? Lord... I'm checkin' my pill pack soon as I can stand."),
                _("Sugar, my stomach's in knots. That pill better do its job, 'cause I can't take a scare like this."),
            ],
            "aftermath.no_protection": [
                _("Lord, what were we thinkin'? Sugar, I need a mornin' after pill, and I need it soon."),
                _("That was reckless, darlin'. No pill, no nothin'... I'm gonna be worryin' for weeks."),
            ],
            "pull_out.pregnant_known": [
                _("You didn't have to bother, sugar. I'm already pregnant, remember?"),
                _("Sweet of you to pull out, darlin', but that ship sailed a while back."),
            ],
            "pull_out.preg_fetish": [
                _("Aw, sugar, why? I wanted that in me, not on me. What a waste."),
                _("Lord, you're cruel, darlin'. How are you gonna knock me up if you keep pullin' out?"),
            ],
            "pull_out.preg_fear": [
                _("Oh, thank the Lord... thank you, sugar. You got no idea what that means to me."),
                _("You pulled out... I can breathe again. Thank you for keepin' me safe, darlin'."),
            ],
            "pull_out.no_protection": [
                _("Whew... good thinkin', sugar. With no pill in me, that was cuttin' it close."),
                _("I'm glad you were careful, darlin'. Last thing we need is a baby scare."),
            ],
            "pull_out.on_pill": [
                _("You know I'm on the pill, right, sugar? You could've stayed right where you were."),
                _("Such a gentleman, darlin'. Next time stay in, the pill ain't just for decoration."),
            ],
            "cum_condom.preg_fetish_condom": [
                _("All that cum stuck in a rubber... what a shame, sugar. Next time, leave that thing off."),
                _("Mmm... that should've been in me, darlin'. A condom ain't ever gonna give me your baby."),
            ],
            "cum_condom.preg_fear_condom": [
                _("Thank the Lord for that condom, sugar. Check it for me, make sure it didn't break."),
                _("Whew... all caught, right, darlin'? Pull out slow and hold it, I ain't takin' chances."),
            ],
            "creampie_req.preg_fetish": [
                _("Sugar, please... cum inside me. I want you to get me pregnant, right now."),
                _("Nngh... don't you pull out, darlin'. Finish deep and leave me carryin' your baby."),
            ],
            "condom_ask.preg_fetish_condom": [
                _("Sugar, take that condom off. I want your baby, and that thing's in my way."),
                _("Ahh... pull out a second and lose the rubber, darlin'. I need you bare, I need you breedin' me."),
            ],
        },
        "ntw": {
            "moan.pregnant_known": [
                _("Mmm... what are you being careful for, genius? You already knocked me up."),
                _("Ahh... damage's done. Nothing left to worry about. ...It's kind of nice. Don't smile."),
            ],
            "moan.preg_fetish": [
                _("Nngh... deeper, idiot. I want you to knock me up. Don't make me say it twice."),
                _("Ahh... fuck. Put a baby in me already. Yeah, I said it. Shut up."),
            ],
            "moan.preg_fetish_condom": [
                _("Mmm... I hate that fucking rubber. Take it off and breed me properly."),
                _("Nngh... feels good, but that thing is in my way. You can't knock me up through latex, genius."),
            ],
            "moan.preg_fear_raw": [
                _("Ahh... fuck, careful. I'm not on the pill. Cum in me and I'll kill you."),
                _("Nngh... it's good, okay? But you pull out. I mean it. Don't you dare finish in me."),
            ],
            "moan.preg_fear_pill": [
                _("Mmm... the pill is the only reason you're in me bare. Don't get comfortable."),
                _("Ahh... I'm on the pill. I am. Fuck, I still can't relax. Just keep going."),
            ],
            "moan.preg_fear_condom": [
                _("Nngh... is it still on? Check. I'm not kidding, idiot, check it."),
                _("Mmm... fine, with the condom I can almost enjoy this. If it slips, you're dead."),
            ],
            "moan.no_protection": [
                _("Ahh... shit, we've got nothing. No pill, no rubber. You pull out, got it?"),
                _("Mmm... fuck, that's good. Don't get stupid though. I'm not on anything, so you finish outside."),
            ],
            "moan.on_pill": [
                _("Mmm... raw is better. Don't look so smug, the pill's doing the work, not you."),
                _("Ahh... I'm on the pill, so quit worrying and fuck me like you mean it."),
            ],
            "inside_ok.pregnant_known": [
                _("Go ahead. What's it gonna do, get me pregnant twice?"),
                _("I'm already carrying your kid, genius. Cum wherever you want."),
            ],
            "inside_ok.preg_fetish": [
                _("Inside. All of it. Knock me up and don't you dare pull out."),
                _("Fuck yes. I want your baby, idiot. Don't make it weird, just fill me."),
            ],
            "inside_ok.on_pill": [
                _("Fine. I'm on the pill, so knock yourself out."),
                _("Yeah, whatever, do it inside. That's what I take the damn pill for."),
            ],
            "inside_ok.preg_fear_pill": [
                _("...Fuck. Okay. I'm on the pill. It works. It better fucking work."),
                _("Do it before I change my mind. If the pill fails me, I'm coming for you."),
            ],
            "inside_no.preg_fear_raw": [
                _("No. Fuck no. I'm not on the pill. Don't even joke about that, asshole."),
                _("Are you insane? No! I am not getting pregnant. Not happening. Outside or we stop right now."),
            ],
            "inside_no.preg_fear_pill": [
                _("No. The pill isn't a hundred percent and I'm not betting my life on it. Outside."),
                _("Pill or not, the answer's no. Pills fail, genius. Don't push it."),
            ],
            "inside_no.no_protection": [
                _("No. I'm not on the pill, idiot. You want a kid? Didn't think so. Outside."),
                _("Not a chance. I'm not on anything. I could actually get pregnant, so you finish somewhere else."),
            ],
            "inside_react.pregnant_known": [
                _("Mmm... there. Happy? Not like you can knock me up any harder."),
                _("Ahh... warm. Whatever. One perk of you already getting me pregnant, I guess."),
            ],
            "inside_react.preg_fetish": [
                _("Ahh... fuck, yes. It better take. If it doesn't, you're doing that again."),
                _("Nngh... so much. Good. Stay in. I want every drop working on it."),
            ],
            "inside_react.on_pill": [
                _("Mmm... okay, that feels good. Don't tell anyone I said that. Pill's got it covered."),
                _("Ahh... you made a mess in me. Relax, idiot, I'm on the pill. Enjoy it."),
            ],
            "inside_react.preg_fear_pill": [
                _("Fuck. Why did I say yes? The pill works. It works. Tell me it works."),
                _("Nngh... that's a lot. Shit. I'm on the pill, I'm on the pill. Stop looking at me."),
            ],
            "inside_react.no_protection": [
                _("...What the fuck did I just let you do? No pill, nothing. I'm an idiot."),
                _("Ahh... shit. That was stupid. I said yes, I know. Doesn't mean I'm not freaking out."),
            ],
            "inside_forced.preg_fear_raw": [
                _("What the fuck did you do?! I said NO! I'm not on the pill, you asshole!"),
                _("Get out of me! Get out! If I end up pregnant, I will ruin your fucking life."),
            ],
            "inside_forced.preg_fear_pill": [
                _("I told you not to! You better pray this pill works, because I am going to kill you."),
                _("You piece of shit. The pill is the only thing between you and a very bad day."),
            ],
            "inside_forced.no_protection": [
                _("Are you fucking serious? I said outside! I'm not on anything, I could get pregnant!"),
                _("Idiot! No pill, no nothing, and you unload in me anyway? You're paying for whatever comes next."),
            ],
            "inside_forced.on_pill": [
                _("Being on the pill doesn't mean you get to, asshole. I said no. Learn the word."),
                _("I don't care that I won't get pregnant. You don't decide that. Pull that again and we're done."),
            ],
            "aftermath.pregnant_known": [
                _("Hah... okay. Give me a second. Growing your kid is exhausting enough without this."),
                _("...That was fine. Better than fine. Tell anyone and the baby grows up without a dad."),
            ],
            "aftermath.preg_fetish": [
                _("Don't move. I'm keeping it in. Shut up, I know how it sounds."),
                _("...I keep picturing it. Me, pregnant. With yours. Laugh and I'll break your nose."),
            ],
            "aftermath.on_pill": [
                _("Hah... not bad. I'm good. Pill's handled, so wipe that worried look off your face."),
                _("...Yeah. That hit the spot. No drama, no panic. I could get used to this. Maybe."),
            ],
            "aftermath.preg_fear_pill": [
                _("I took it today. I'm sure I did. Fuck, I'm checking the pack the second I get up."),
                _("...Never letting you do that again. Probably. Ugh, I need to go count my pills."),
            ],
            "aftermath.no_protection": [
                _("Shit. Shit. I need a morning after pill. You're buying it, genius."),
                _("...Don't talk to me. I let you finish in me with nothing. If this goes wrong, it's on you too."),
            ],
            "pull_out.pregnant_known": [
                _("Why'd you pull out, genius? I'm already pregnant. Bit late for manners."),
                _("Cute. Real careful. The baby's already in there, idiot. You wasted it."),
            ],
            "pull_out.preg_fetish": [
                _("Are you kidding me? I wanted that inside. What part of knock me up was unclear?"),
                _("Ugh. All over my skin, where it's useless. Next time you stay in, or I make you."),
            ],
            "pull_out.preg_fear": [
                _("...Oh thank fuck. Okay. You listened. ...Thanks. Don't make it a thing."),
                _("Hah... you pulled out. Good. I can breathe again. You're less of an idiot than I thought."),
            ],
            "pull_out.no_protection": [
                _("Good. Outside, like I said. With no pill, that's the only reason you still have balls."),
                _("Huh. You were actually careful. Smart move, since I'm not on anything. ...Noted."),
            ],
            "pull_out.on_pill": [
                _("You know I'm on the pill, right? You could've stayed in. Your loss, genius."),
                _("Pulling out? What a gentleman. I take the pill for a reason, idiot. Think about it next time."),
            ],
            "cum_condom.preg_fetish_condom": [
                _("What a waste. All that in a rubber. Next time that thing stays in the drawer."),
                _("Great. You knocked up a piece of latex. Next time it's bare, and it goes in me."),
            ],
            "cum_condom.preg_fear_condom": [
                _("Okay. Okay, good. Now show it to me. I'm not relaxing until I see it didn't break."),
                _("Hah... thank fuck for condoms. Pull out slow and hold the base. I'm not taking chances."),
            ],
            "creampie_req.preg_fetish": [
                _("Nngh... cum in me. I mean it. Get me pregnant, idiot, that's not a request."),
                _("Ahh... don't you pull out. I want it deep. I want your kid. Fuck, just do it."),
            ],
            "condom_ask.preg_fetish_condom": [
                _("Mmm... stop. Take the condom off. I want your baby and that thing's blocking it."),
                _("Nngh... lose the rubber. Now. I want you bare, and I want you to knock me up."),
            ],
        },
        "tenny": {
            "moan.pregnant_known": [
                _("Mmm... n-nothing to worry about now. I'm already carrying your baby..."),
                _("Ahh... y-you can go deeper. You already got me pregnant, remember?"),
            ],
            "moan.preg_fetish": [
                _("P-please... get me pregnant. I-I want your baby so bad... ahh!"),
                _("Nngh... d-don't pull out. Fill me up and knock me up, please..."),
            ],
            "moan.preg_fetish_condom": [
                _("I-I hate that thing... mmm... take it off so you can knock me up..."),
                _("Ahh... s-so good, but that condom is keeping your baby away from me..."),
            ],
            "moan.preg_fear_raw": [
                _("Ahh... i-it's so good it scares me... I'm not on the pill! P-please, please be careful..."),
                _("Nngh... p-promise you won't finish inside. I-I can't get pregnant, I can't..."),
            ],
            "moan.preg_fear_pill": [
                _("Mmm... I-I only let you go raw because of the pill. I'm still so nervous..."),
                _("Ahh... m-my app says I took the pill today. I-I checked three times..."),
            ],
            "moan.preg_fear_condom": [
                _("Nngh... i-is the condom still on? S-sorry, I just need to be sure..."),
                _("Mmm... w-with the condom I can finally relax a little... ahh, keep going..."),
            ],
            "moan.no_protection": [
                _("Ahh... w-wait, we have nothing... y-you have to pull out, okay?"),
                _("Mmm... s-so good... but I'm not on the pill. D-don't forget that, please..."),
            ],
            "moan.on_pill": [
                _("Mmm... I-I love feeling you raw. The pill has me covered, so don't hold back..."),
                _("Ahh... n-nothing to stress about. I take my pill every morning before class..."),
            ],
            "inside_ok.pregnant_known": [
                _("I-inside? Go ahead... I'm already pregnant, it makes no difference now."),
                _("Y-yes, you can. You can't get me pregnant twice, silly... mmm..."),
            ],
            "inside_ok.preg_fetish": [
                _("Y-yes! Cum inside me, please! I-I've dreamed of having your baby!"),
                _("I-I was hoping you'd ask... do it deep, make me a mommy..."),
            ],
            "inside_ok.on_pill": [
                _("O-okay, you can. I'm on the pill, so it's fine... mmm..."),
                _("I-inside is okay. My pill reminder never misses, I promise."),
            ],
            "inside_ok.preg_fear_pill": [
                _("O-okay... okay. I'm on the pill. I-it works, right? Just... do it."),
                _("I-I'm trusting the pill here... p-please don't make me regret this."),
            ],
            "inside_no.preg_fear_raw": [
                _("N-no, no, no! I'm not on the pill! P-please, anywhere but inside!"),
                _("P-please don't! I-I'd get pregnant, I can't even think about it!"),
            ],
            "inside_no.preg_fear_pill": [
                _("N-no... the pill isn't perfect. I-I read the statistics, I won't risk it."),
                _("I-I know I'm on the pill, but no. P-please, not inside, I'm too scared."),
            ],
            "inside_no.no_protection": [
                _("N-not inside! I'm not on the pill, I could get pregnant..."),
                _("S-sorry, no. I'm not taking anything... a baby could really happen. P-please, outside."),
            ],
            "inside_react.pregnant_known": [
                _("Mmm... s-so warm. Good thing I'm already pregnant, huh?"),
                _("Ahh... y-you filled me up. Nothing to worry about, the baby's already there..."),
            ],
            "inside_react.preg_fetish": [
                _("Ahh! S-so much... I-I hope it takes, I really hope it takes!"),
                _("Y-you did it... you came in me. M-maybe I'm getting pregnant right now..."),
            ],
            "inside_react.on_pill": [
                _("Mmm... I-I can feel it all inside. The pill handles the rest..."),
                _("Ahh... t-that felt amazing. No stress, that's what my pill is for."),
            ],
            "inside_react.preg_fear_pill": [
                _("I-I really let you... oh god. N-ninety-nine in a hundred, that's what the pill box says..."),
                _("T-there's so much in me... I took the pill. I took it. I-I'm sure I took it."),
            ],
            "inside_react.no_protection": [
                _("W-what did I just let you do... I'm not on the pill, I have nothing..."),
                _("I-I said yes... why did I say yes? I-I could actually get pregnant..."),
            ],
            "inside_forced.preg_fear_raw": [
                _("N-no! I told you not inside! I'm not on the pill, w-what do I do now?!"),
                _("I-I begged you! This is my worst nightmare... h-how could you do this to me?"),
            ],
            "inside_forced.preg_fear_pill": [
                _("I-I said no! The pill is all I have now... p-please, please let it work..."),
                _("W-why didn't you listen?! If the pill fails... I-I don't know what I'll do..."),
            ],
            "inside_forced.no_protection": [
                _("Y-you came inside?! B-but I said no... I have no protection at all, what if I get pregnant?!"),
                _("I-I told you to pull out! Now I might end up pregnant... that wasn't your choice!"),
            ],
            "inside_forced.on_pill": [
                _("B-being on the pill doesn't mean you get to! I said no..."),
                _("I-it's not about getting pregnant. You ignored me... t-that really hurt."),
            ],
            "aftermath.pregnant_known": [
                _("Haah... l-let me catch my breath. The baby and I both need a minute..."),
                _("I-it's kind of nice... already being pregnant means no worrying afterwards."),
            ],
            "aftermath.preg_fetish": [
                _("I-I'm keeping my legs closed... I don't want a single drop to leak out."),
                _("Mmm... I-I keep picturing my belly getting big. I-is that weird?"),
            ],
            "aftermath.on_pill": [
                _("Haah... t-that was so good. All warm inside and zero worries, thanks to my pill."),
                _("Mmm... I-I could fall asleep like this. Tomorrow I just log my pill, like always."),
            ],
            "aftermath.preg_fear_pill": [
                _("I-I did take my pill today, right? I need to check my app, just to be sure..."),
                _("M-my heart won't slow down... the pill will work. I-it has to work."),
            ],
            "aftermath.no_protection": [
                _("I-I think I need a morning after pill... c-can we go to the pharmacy?"),
                _("W-we really shouldn't have done that... I-I won't be able to study at all now."),
            ],
            "pull_out.pregnant_known": [
                _("Y-you didn't have to bother pulling out... I'm already pregnant, you know."),
                _("O-outside? That's sweet, but there's nothing left to be careful about..."),
            ],
            "pull_out.preg_fetish": [
                _("W-why did you pull out? I-I wanted it inside... I wanted your baby..."),
                _("A-all of it wasted outside... n-next time stay in, please?"),
            ],
            "pull_out.preg_fear": [
                _("T-thank you, thank you... you pulled out. I-I was so scared..."),
                _("O-outside... oh, thank goodness. I can finally breathe again."),
            ],
            "pull_out.no_protection": [
                _("P-phew... you remembered. Thanks for being careful with me."),
                _("G-good, outside... I'm not on the pill, so that really mattered to me."),
            ],
            "pull_out.on_pill": [
                _("Y-you know I'm on the pill, right? You could've stayed in... hehe."),
                _("S-such a gentleman... but my pill was ready for you, you know."),
            ],
            "cum_condom.preg_fetish_condom": [
                _("A-all of that stuck in a condom... what a shame. N-next time without it, okay?"),
                _("I-I felt you throb, but nothing reached me... that thing stole my baby."),
            ],
            "cum_condom.preg_fear_condom": [
                _("I-I'm so glad we used a condom... c-can you check it didn't break? Please?"),
                _("I-it all stayed in the condom, right? O-okay... okay. I feel so much better."),
            ],
            "creampie_req.preg_fetish": [
                _("P-please cum inside me... I-I want you to get me pregnant. I mean it."),
                _("I-I've thought about it a lot... put a baby in me. Please, finish inside..."),
            ],
            "condom_ask.preg_fetish_condom": [
                _("C-can you take the condom off? I-I want your baby... please?"),
                _("T-take it off, please... I don't want anything between us. I want you to knock me up."),
            ],
        },
    }
