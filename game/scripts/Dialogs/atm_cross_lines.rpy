## atm_cross_lines.rpy -- DATA ONLY: cross-girl ATM line pools (threesome: it was in the OTHER girl's ass).
## Read by atm_cross_line() in atm_cross.rpy: _ATM_CROSS_LINES[gid or "_default"]["<moment>.<trait or _default>"].
## moments: ask_ok, ask_no, react, moan, entry, swallow_ok, swallow_no, after_swallow. %(src)s = the other girl's name.
## Rules for new lines: never "my ass" (it was HERS), no em dash, no other % character, no double quotes.
## A girl without an entry (or without a pool) falls back to "_default". Translations: docs/translation_todo.md.
## A line that states HER OWN ATM history goes in "<moment>.<trait>.atm" (she had one before this one: "I know that
## taste") or "<moment>.<trait>.first_atm" (she never had one: "I've never done anything like this"). Those lines are
## added to "<moment>.<trait>" only when it is true (_ATM_CROSS_HISTORY_SUFFIX), so that key keeps a line for both.

init python:

    _ATM_CROSS_LINES = {
        "_default": {
            "ask_ok._default": [
                _("It was just inside %(src)s and you want my mouth on it? ...Okay, just this once."),
                _("Seriously, right after %(src)s? Fine, come here before I change my mind."),
            ],
            "ask_ok.cum_slut": [
                _("Fresh out of %(src)s's ass? That just makes it dirtier, so give it here."),
                _("Mmm, I don't care where it's been. If %(src)s got you this hard, I'm getting the load."),
            ],
            "ask_ok.hardcore_sex": [
                _("God, that's filthy. Shove it in my mouth, I want to taste how hard you fucked %(src)s."),
                _("Right out of %(src)s's ass? Filthy. Now shove it down my throat and don't go easy."),
            ],
            "ask_ok.submissive": [
                _("Straight out of %(src)s's ass and into my throat? Fuck yes, treat me like the dirty slut I am."),
                _("If you tell me to clean %(src)s off you, I clean it. Give it here."),
                _("You want my mouth after %(src)s? Then it's yours. Use it however you like."),
            ],
            "ask_ok.cute_sex": [
                _("Right after %(src)s? That's so embarrassing... okay, I'll try, just be gentle with me."),
            ],
            "ask_ok.cute_sex.first_atm": [
                _("I've never done anything like this... If it makes you happy I'll do it, just don't let %(src)s stare."),
            ],
            "ask_ok.anal_lover": [
                _("So %(src)s gets it in the ass and I get the cleanup? Fine, but promise I'm next back there."),
                _("Lucky %(src)s. I'll suck it, but only if you put it in mine after."),
            ],
            "ask_ok.lesbian": [
                _("Tasting %(src)s is the only part of this I don't mind. Fine, but the cock attached to it does nothing for me."),
                _("If it didn't have %(src)s all over it, I'd say no. Don't read anything into this."),
            ],
            "ask_no._default": [
                _("That was in %(src)s's ass ten seconds ago. No, it's not going in my mouth."),
                _("Not a chance. Go wash %(src)s off first, then maybe we'll talk."),
            ],
            "ask_no.cute_sex": [
                _("I can't, not right after %(src)s... That's too much for me, please don't be mad."),
                _("Please don't ask me that. It was in %(src)s's bottom a second ago, I just can't."),
            ],
            "ask_no.hardcore_sex": [
                _("I like it filthy, but I'm not sucking %(src)s's ass off your dick today. Fuck me instead."),
                _("Nice try. Wash %(src)s off and then you can choke me with it all you want."),
            ],
            "ask_no.hate_cum": [
                _("I barely tolerate your cum as it is. With %(src)s's ass on top of it, no way."),
                _("No. It's bad enough when it's clean, and that thing just came out of %(src)s."),
            ],
            "ask_no.anal_hater": [
                _("You had it in %(src)s's ass, her actual ass! Keep that thing far away from my face."),
                _("Ew, no. Anything that comes out of %(src)s's butt is not going anywhere near my mouth."),
            ],
            "ask_no.lesbian": [
                _("I don't even want your cock clean. %(src)s being on it isn't enough to change that."),
                _("If I want to taste %(src)s, I'll go to the source. I don't need your dick for that."),
            ],
            "react._default": [
                _("Oh wow... I can taste %(src)s on you. This is so wrong."),
                _("Mmh... that's definitely %(src)s. I can't believe I'm actually doing this."),
            ],
            "react.cum_slut": [
                _("Mmm, %(src)s's ass and your precum together... that's so nasty, give me more."),
                _("Oh, that taste... I don't care where it's been, I just want what comes out of it."),
            ],
            "react.hate_cum": [
                _("Ugh... it's already leaking, and it tastes like %(src)s too. This is the worst."),
                _("Gross... %(src)s's ass and your precum at once. Don't you dare cum without warning me."),
            ],
            "react.hardcore_sex": [
                _("That's disgusting and I love it. Push deeper, make me taste every inch %(src)s took."),
                _("God, that's dirty. I can taste %(src)s on every inch. Now fuck my mouth harder."),
            ],
            "react.submissive": [
                _("Fuck... I can taste %(src)s's ass all over your cock. Make me lick it clean."),
                _("I can taste %(src)s on you... tell me to keep going and I will."),
                _("Mmh... that's %(src)s. Use my mouth to get it all off, I'm yours."),
            ],
            "react.cute_sex": [
                _("Oh... it tastes like %(src)s. My face is burning, please don't look at me like that."),
                _("This is so dirty... I'm only doing it because it's you, okay?"),
            ],
            "react.anal_lover": [
                _("So that's what %(src)s's ass did to you, you're still throbbing. It should have been mine."),
            ],
            "react.anal_lover.atm": [
                _("Mmm, I know that taste. %(src)s got it so deep... I'm honestly jealous."),
            ],
            "react.anal_hater": [
                _("Oh god, I can taste it. That's %(src)s's ass in my mouth, I'm going to be sick."),
                _("Ugh, that's foul. I can literally taste where %(src)s had you, why did I agree to this?"),
            ],
            "react.lesbian": [
                _("That's %(src)s... okay, that part I actually like. I just wish it wasn't on you."),
                _("Mm. If I close my eyes it's only %(src)s I'm tasting, so don't ruin it by talking."),
            ],
            "moan._default": [
                _("Mmph... you still taste like %(src)s... this is insane..."),
                _("Glk... mmm... don't tell anyone I did this..."),
                _("Mmm... straight from %(src)s to me... you're unbelievable..."),
            ],
            "moan.cum_slut": [
                _("Mmm... glk... hurry up and feed me... I've earned it after %(src)s..."),
                _("Mmph... I can already taste you leaking... more..."),
                _("Glk... %(src)s warmed you up, now give me the load... mmm..."),
            ],
            "moan.hate_cum": [
                _("Mmph... ugh... %(src)s and precum... I hate this so much..."),
                _("Glk... warn me before you finish... mmph... I mean it..."),
                _("Nngh... it keeps leaking... it just tastes worse and worse..."),
            ],
            "moan.hardcore_sex": [
                _("Glk... fuck my throat... make me choke on %(src)s's mess..."),
                _("Mmph... faster... glk... don't you dare slow down..."),
                _("Glk... deeper... mmm... %(src)s's taste and all... harder..."),
            ],
            "moan.submissive": [
                _("Mmph... harder... use my mouth like you used %(src)s's ass..."),
                _("Mmm... I'm your filthy cleanup slut... glk... don't hold back..."),
                _("Mmph... yours... glk... use me however you want..."),
            ],
            "moan.cute_sex": [
                _("Mmm... is this okay...? I'm trying my best... even after %(src)s..."),
                _("Mmph... please keep stroking my hair... it helps..."),
                _("Mm... don't watch, %(src)s... mmph... this is so embarrassing..."),
            ],
            "moan.anal_lover": [
                _("Mmph... %(src)s got all of this in her ass... so unfair..."),
                _("Glk... mmm... I'm getting you nice and wet so you can take mine next..."),
                _("Mmm... I can tell how tight %(src)s was... glk... I'm tighter..."),
            ],
            "moan.anal_hater": [
                _("Mmph... ugh... I can't stop tasting %(src)s's ass... so gross..."),
                _("Glk... hurry up... mmph... I want this over with..."),
                _("Nngh... never again... mmph... you owe me so much for this..."),
            ],
            "moan.lesbian": [
                _("Mmph... at least it tastes like %(src)s... not like you..."),
                _("Mm... I'm thinking about %(src)s, not you... glk... just so we're clear..."),
                _("Glk... ugh... just finish already... mmph..."),
            ],
            "entry._default": [
                _("You're about to cum, aren't you? Fresh out of %(src)s, and I'm the one who gets it."),
                _("I can feel you twitching. Go on then, %(src)s did the work and I get the finish."),
            ],
            "entry.cum_slut": [
                _("Yes, give it to me! %(src)s took your cock, but the cum is all mine."),
                _("Don't you dare pull out. I want every drop on my tongue, dirty or not."),
            ],
            "entry.hate_cum": [
                _("You're close, I can tell. First %(src)s's ass, now your cum in my mouth... what a nightmare."),
                _("Ugh, here it comes. Just get it over with, and don't expect me to like it."),
            ],
            "entry.hardcore_sex": [
                _("Do it. Blow your load in the mouth that just cleaned %(src)s's ass off your cock."),
                _("Come on, blow it. I want it thick and nasty, right on top of %(src)s's taste."),
            ],
            "entry.submissive": [
                _("Come on, fill your dirty whore's mouth. I want it thick and nasty."),
                _("Cum whenever you want. My mouth is yours, %(src)s's taste and all."),
                _("Go ahead, use it. I'll hold still and take every drop you give me."),
            ],
            "entry.cute_sex": [
                _("You're going to finish in my mouth? After %(src)s and everything... okay, I think I'm ready."),
                _("It's alright, you can let go. I'll take it for you, just hold me after."),
            ],
            "entry.anal_hater": [
                _("Great. %(src)s's ass first, and now your cum on top of it, my mouth is ruined."),
                _("Just finish already. The sooner you cum, the sooner I can rinse all of this out."),
            ],
            "swallow_ok._default": [
                _("You want me to swallow? After it was in %(src)s? ...Alright, here goes."),
                _("Mmh... fine. I already went this far with %(src)s's taste in my mouth, so down it goes."),
            ],
            "swallow_ok.cum_slut": [
                _("Mmm, you don't have to ask twice. %(src)s's ass or not, I never waste cum."),
                _("Of course I'll swallow. It's warm and thick and it's mine, so watch me."),
            ],
            "swallow_ok.hardcore_sex": [
                _("Gladly. I'll gulp down your load and whatever's left of %(src)s with it."),
                _("Filthy load, filthy mouth. Watch it all go down, %(src)s's taste and everything."),
            ],
            "swallow_ok.submissive": [
                _("Make me. Hold my jaw shut until your filthy load is all the way down my throat."),
                _("If you tell me to swallow, I swallow. Even after %(src)s."),
                _("Yes... order me to and it all goes down. Say it."),
            ],
            "swallow_ok.cute_sex": [
                _("All of it? Even after %(src)s... okay, I'll do it for you, just stay close to me."),
                _("Mm... okay, I'll swallow. Just promise you won't think less of me after."),
            ],
            "swallow_ok.anal_lover": [
                _("Fine, I'll swallow. But %(src)s got the fun part, so next time my back door gets this load."),
                _("Down it goes. Remember this when you pick whose turn is next back there, because it had better be mine."),
            ],
            "swallow_no._default": [
                _("No. It was in %(src)s's ass a minute ago, I'm spitting this out."),
                _("Sucking it was already a lot. I'm not swallowing anything that touched %(src)s's ass."),
            ],
            "swallow_no.cute_sex": [
                _("I'm sorry, I can't... not after it was inside %(src)s. Please let me spit it out."),
                _("Please don't make me. I did everything else for you, but swallowing this is too much."),
            ],
            "swallow_no.hardcore_sex": [
                _("Nah. I'd rather let it drip down my chin and make a mess, %(src)s can lick it up."),
                _("Not swallowing this one. I'll spit it right back on your cock, that's as dirty as I get today."),
            ],
            "swallow_no.hate_cum": [
                _("Swallow? I can't stand cum on a good day, and this load comes with %(src)s's ass. I'm spitting."),
                _("Absolutely not. Get me a tissue, I'm spitting every drop of this out right now."),
            ],
            "swallow_no.anal_hater": [
                _("No way. That load touched %(src)s's ass, it is not going into my stomach."),
                _("I already want to scrub my tongue. Swallowing ass flavored cum is where I draw the line."),
            ],
            "after_swallow._default": [
                _("I actually swallowed that. If %(src)s ever brings this up, I'm denying everything."),
                _("Wow... I did not think I'd go through with it. You owe me for this one."),
            ],
            "after_swallow.cum_slut": [
                _("Mmm, delicious. %(src)s can keep the pounding, I'll take the cum every time."),
                _("All gone. A little dirty seasoning never hurt anyone... got any more for me?"),
            ],
            "after_swallow.hate_cum": [
                _("Ugh, I can still feel it going down. Your cum and %(src)s's ass... I need water, now."),
                _("Never again. That was the most disgusting thing I've ever swallowed, and you know how I feel about cum."),
            ],
            "after_swallow.hardcore_sex": [
                _("Fuck, that was nasty. Cleaning %(src)s's ass off you and drinking your load... I'm soaked."),
                _("See? Every filthy drop, gone. Next time don't even ask, just shove it in."),
            ],
            "after_swallow.cute_sex": [
                _("I did it... I really swallowed it, even after %(src)s. Are you proud of me?"),
                _("My heart is racing. That was so dirty... please just hold me for a minute."),
            ],
            "after_swallow.lesbian": [
                _("The part that was %(src)s, I didn't mind. The part that was you, I'd rather forget."),
                _("Don't get any ideas. I swallowed a man's cum because of %(src)s, not because of you."),
            ],
        },
        "gwen": {
            "ask_ok._default": [
                _("Straight out of %(src)s and into my mouth? Seriously? ...Fine. You owe me one, and I'm collecting."),
                _("You do know where that just was, right? Damn it. Okay, come here before I change my mind."),
            ],
            "ask_ok.cum_slut": [
                _("Fresh out of %(src)s's ass and you're offering it to me? Cute. Like I'd say no to what comes at the end."),
                _("Mmm, dirty. I don't care where it's been, as long as you finish in my mouth. Hand it over."),
            ],
            "ask_ok.hardcore_sex": [
                _("From %(src)s's ass straight to my mouth? That's fucking filthy. Good. Get over here."),
                _("Seriously? Right out of %(src)s? That's vile. Perfect. Now don't be gentle about it."),
            ],
            "ask_ok.submissive": [
                _("Treating my mouth like your cleanup crew, huh? Damn it, that actually works for me. Shove it in."),
                _("You want me to clean %(src)s off you? Say it like an order. ...Damn it. Fine, I'll obey."),
                _("My mouth, your rules. Apparently that's a thing I like now. Seriously, don't gloat."),
            ],
            "ask_ok.cute_sex": [
                _("Right after %(src)s? Seriously? ...Okay. But go slow, and hold my hand or something. I mean it."),
                _("You really know how to romance a girl. Fine, I'll do it. Just be gentle with me, this is a lot."),
            ],
            "ask_ok.anal_lover": [
                _("So %(src)s gets it in the ass and I get the leftovers? Cute. Fine, but I'm next, and you know where."),
                _("Lucky girl. At least let me taste what I missed out on. Come here, and don't think I'm not keeping score."),
            ],
            "ask_ok.lesbian": [
                _("The part that's %(src)s, I can live with. The part that's you is the problem. ...Fine. Make it quick."),
                _("Damn it. I'm doing this for the taste of her, not for you. Don't get any ideas about what it means."),
            ],
            "ask_no._default": [
                _("It was just in %(src)s's ass and you want my mouth on it? Hard pass. Go wash it and we'll talk."),
                _("Seriously? No. I have standards, and that thing just left them way behind."),
            ],
            "ask_no.cute_sex": [
                _("Right out of %(src)s and into my mouth? No. That's not sweet, that's just gross. Kiss me instead."),
                _("Not like this. I want it to feel nice, not like I'm cleaning up after someone. Ask me again later."),
            ],
            "ask_no.hardcore_sex": [
                _("I like it dirty, not unsanitary. Fuck my throat all you want, after you wash %(src)s off it."),
                _("Nice try. Pin me down and wreck me, sure, but that cock isn't going in my mouth like that."),
            ],
            "ask_no.hate_cum": [
                _("I barely tolerate your cum on a good day. Add %(src)s's ass to the recipe? Absolutely not."),
                _("No. Just no. That thing is a biohazard twice over right now, keep it away from my face."),
            ],
            "ask_no.anal_hater": [
                _("It was in %(src)s's ass. An ass. And you want it in my mouth? Are you out of your mind? No."),
                _("Anything that comes out of there goes nowhere near my face. That's not a rule, that's basic survival."),
            ],
            "ask_no.lesbian": [
                _("If I want to taste %(src)s, I'll go to the source. I don't need your dick as a middleman. No."),
                _("Sucking you off is a stretch for me on a clean day. Like this? Forget it."),
            ],
            "react._default": [
                _("Oh, damn it... yeah, that's %(src)s alright. I can taste exactly where you've been."),
                _("Ugh... you weren't kidding about straight from the source. The things I let you talk me into."),
            ],
            "react.cum_slut": [
                _("Mmm... so that's what %(src)s tastes like on you. Dirty. Now hurry up and give me the good part."),
                _("Tastes like you've been busy. I don't care, I'm just here for the ending. Don't keep me waiting."),
            ],
            "react.hate_cum": [
                _("Ugh, god... that's %(src)s, and it's only going to get worse when you finish. Why did I say yes?"),
                _("Seriously, this taste... and the grand finale is the part I hate most. What a treat."),
            ],
            "react.hardcore_sex": [
                _("Fuck... I can taste %(src)s's ass all over you. That's so wrong. Keep going, don't you dare pull out."),
                _("Ugh, that's disgusting. And I'm into it, apparently. Faster, before I start thinking."),
            ],
            "react.submissive": [
                _("Mmm, nasty. You're using my mouth to clean your cock and I'm getting wet over it. Damn it."),
                _("That's %(src)s, alright. Tell me to keep licking and I will. Don't make it weird."),
                _("Ugh. I'm your cleanup girl now, apparently. And I'm not even mad about it."),
            ],
            "react.cute_sex": [
                _("Oh god... that's %(src)s I'm tasting, isn't it? Don't look at me like that, I'm embarrassed enough."),
                _("This is so dirty... just stroke my hair or something, okay? It helps. And wipe that grin off."),
            ],
            "react.anal_lover": [
                _("Mmm... so that's how deep you were in %(src)s. Tasting it just makes me more jealous, you know."),
                _("There it is. Her ass got the fun and I get the flavor. Seriously unfair, and you're fixing it later."),
            ],
            "react.anal_hater": [
                _("Ugh, that's ass. That's actual %(src)s ass in my mouth. I hate everything about this. Everything."),
                _("Oh god, no... I knew it would be bad and it's still worse. You owe me so much for this."),
            ],
            "react.lesbian": [
                _("Mm... okay, that's %(src)s. That part I actually don't mind. Shame it comes attached to you."),
                _("If I close my eyes, it's just her I'm tasting. Do me a favor and stay quiet so I can pretend."),
            ],
            "moan._default": [
                _("Mmph... straight out of %(src)s... you're disgusting, you know that..."),
                _("Glk... mmm... the things I do for you... seriously..."),
                _("Mmm... still tastes like her... you'd better be enjoying this..."),
            ],
            "moan.cum_slut": [
                _("Mmph... don't care where it's been... just give me your load... mmm..."),
                _("Glk... come on, %(src)s got you warmed up... now finish in my mouth..."),
                _("Mmm... I can taste it leaking already... more... give me all of it..."),
            ],
            "moan.hate_cum": [
                _("Mmph... ugh... %(src)s on top of everything else... warn me before you blow..."),
                _("Glk... I swear, if you cum without telling me... mmph..."),
                _("Mmm... ngh... already tastes bad enough... don't you dare make it worse yet..."),
            ],
            "moan.hardcore_sex": [
                _("Mmm... harder... grab my hair and fuck my face... I can take it..."),
                _("Mmph... harder... glk... is that all you've got..."),
                _("Glk... mmph... deeper... yeah, I'll feel that tomorrow..."),
            ],
            "moan.submissive": [
                _("Glk... fuck yes... shove it deeper... make me clean %(src)s off every inch..."),
                _("Mmph... use my throat like a rag... I'm your filthy little cleanup slut... mmm..."),
                _("Mmph... yours... use it however you want... glk... seriously..."),
            ],
            "moan.cute_sex": [
                _("Mmph... be gentle... I'm still tasting %(src)s here... mmm..."),
                _("Mmm... keep your hand on my cheek... like that... it's nicer that way..."),
                _("Glk... slow down... I'm doing this for you, you know... so be sweet..."),
            ],
            "moan.anal_lover": [
                _("Mmph... %(src)s's ass got all of this... and I get her leftovers... so unfair..."),
                _("Mmm... I'm getting you nice and wet... so you can put it where I actually want it..."),
                _("Glk... keep thinking about her ass... because mine is next... mmph..."),
            ],
            "moan.anal_hater": [
                _("Mmph... ugh... it was in %(src)s's ass... I can't stop thinking about it..."),
                _("Glk... so gross... so, so gross... hurry up and finish already..."),
                _("Mmm... ngh... I'm going to brush my teeth for an hour after this..."),
            ],
            "moan.lesbian": [
                _("Mmph... just %(src)s... I'm only tasting %(src)s... you're not even here..."),
                _("Mmm... she tastes good... it's you I'd rather skip... glk..."),
                _("Glk... don't moan like that... you're ruining the part I actually like..."),
            ],
            "entry._default": [
                _("First %(src)s's ass, now my mouth, and you're about to top it off. You're really something else."),
                _("Oh, you're close? Great. The perfect finishing touch to the classiest blowjob of my life."),
            ],
            "entry.cum_slut": [
                _("Finally. %(src)s got the ride, but I get the load. Give me every drop, don't waste any."),
                _("There it is, I can feel you twitching. Come on, fill my mouth. That's the only part I came for."),
            ],
            "entry.hate_cum": [
                _("Oh great, here it comes. %(src)s's ass as the appetizer and your cum as the main course. Lucky me."),
                _("You're about to finish, aren't you? Damn it. Just do it fast, before I think too hard about it."),
            ],
            "entry.hardcore_sex": [
                _("Do it. Blow your load in the same mouth that just cleaned %(src)s off your cock. Make it filthy."),
                _("Oh, you're close? Good. Cum down my throat and make it messy. Don't you dare hold back."),
            ],
            "entry.submissive": [
                _("Cum down my throat, come on. I've been your dirty little rag this long, I've earned the whole mess."),
                _("Go on, finish wherever you want. You own this mouth tonight, apparently. Damn it."),
                _("Tell me to open wide and I will. That's how far gone I am. Don't say anything."),
            ],
            "entry.cute_sex": [
                _("You're about to cum, aren't you? After %(src)s and everything... okay. Look at me when you do."),
                _("Go ahead, I've got you. Just hold my face gently, I want at least one part of this to be sweet."),
            ],
            "entry.anal_hater": [
                _("So I get ass flavor from %(src)s and now your cum on top. Seriously, what did I do to deserve this?"),
                _("Here it comes, the cherry on top of the grossest thing I've ever done. Just get it over with."),
            ],
            "swallow_ok._default": [
                _("Swallow it? After it was in %(src)s? ...Damn it. Fine. But you're buying me a drink after this."),
                _("Seriously? You want the full package. Okay, okay. Down it goes, and we never speak of it."),
            ],
            "swallow_ok.cum_slut": [
                _("Like you even have to ask. %(src)s can keep the ride, the load is all mine. Watch me."),
                _("Mmm, swallow it? That was always the plan. I'm not wasting a single drop of this."),
            ],
            "swallow_ok.hardcore_sex": [
                _("Swallow your cum with %(src)s's ass still on my tongue? Fuck, that's nasty. Watch me do it."),
                _("Swallow it? Fine. Every filthy drop, straight down. Try not to look so impressed."),
            ],
            "swallow_ok.submissive": [
                _("Make me gulp it all down like a good filthy slut. I'll even open wide after so you can check."),
                _("Swallow it? If you're telling me to, then yes. Look at me, obeying. Cute."),
                _("Your load, your call. Say the word and it goes down, %(src)s's taste and all."),
            ],
            "swallow_ok.cute_sex": [
                _("Swallow it...? Even after %(src)s? ...Okay. For you. But you're cuddling me after, no excuses."),
                _("You're lucky I like you this much. Fine, I'll swallow. Just don't stare, it's embarrassing."),
            ],
            "swallow_ok.anal_lover": [
                _("Fine, I'll swallow. It's the closest I'm getting to what %(src)s got, so I might as well enjoy it."),
                _("Down it goes. But next time, I'm the one who gets it in the ass first, deal? I'm holding you to it."),
            ],
            "swallow_no._default": [
                _("Swallow? It was in %(src)s's ass five minutes ago. No. I'm spitting this out, deal with it."),
                _("Cute. I already did the hard part, I'm not doing the encore. Find me a tissue."),
            ],
            "swallow_no.cute_sex": [
                _("Don't ask me that. After %(src)s, it's too much, even for you. I'm spitting it out, okay?"),
                _("I went along with everything else, but this is where I stop. Be sweet about it and pass me a tissue."),
            ],
            "swallow_no.hardcore_sex": [
                _("I'll spit it right back on your cock if you want a show, but I'm not swallowing %(src)s's ass."),
                _("Nope. Let it drip down my chin, make a mess of me, whatever. It's just not going down my throat."),
            ],
            "swallow_no.hate_cum": [
                _("Swallow it? I can barely stand it in my mouth, and that's before %(src)s got involved. Spitting. Now."),
                _("Not a chance. It's coming out in the next three seconds, so either move or get a towel."),
            ],
            "swallow_no.anal_hater": [
                _("It was in %(src)s's ass, then you came on top of it, and you want it in my stomach? No. Never."),
                _("Absolutely not. I already need to bleach my tongue, I'm not sending this any further down."),
            ],
            "after_swallow._default": [
                _("I just swallowed something that came straight from %(src)s's ass. Tell anyone and you're dead."),
                _("Well, that happened. Damn it, I can't believe I went along with it. Get me some water."),
            ],
            "after_swallow.cum_slut": [
                _("Mmm. A little %(src)s on the side didn't ruin it at all. Your cum still wins. Got any more?"),
                _("Gone, every drop. Honestly, the dirty part made it better. Don't tell her I said that."),
            ],
            "after_swallow.hate_cum": [
                _("Ugh. %(src)s's ass and your cum, all the way down. Worst thing I've ever tasted. Never again."),
                _("It's gone, and I hated every second of it. I need mouthwash, a drink, and a very long apology."),
            ],
            "after_swallow.hardcore_sex": [
                _("Fuck. I just swallowed your load straight off %(src)s's ass. I'm such a dirty slut, and I loved it."),
                _("Done. Every drop. That was the filthiest thing I've done this month, and I'd do it again."),
            ],
            "after_swallow.submissive": [
                _("All gone. You used my mouth like a cum rag and I'm dripping from it. Do it again sometime."),
                _("Done, like you told me. I did everything you said and I'm soaked. Don't let it go to your head."),
                _("There. Every drop, on command. Apparently I'm your good little cleanup girl now. Wonderful."),
            ],
            "after_swallow.cute_sex": [
                _("I can't believe I did that, right after %(src)s and everything... Come here. You're kissing me anyway."),
                _("Okay, that was way out of my comfort zone. Now hold me, and don't you dare make a joke about it."),
            ],
            "after_swallow.lesbian": [
                _("For the record, the only thing I enjoyed was %(src)s. The rest I swallowed just to get rid of it."),
                _("There, it's done. It doesn't mean I like guys, so lose that smug look before I lose my patience."),
            ],
        },
        "rogue": {
            "ask_ok._default": [
                _("That was just in %(src)s's ass, sugar, and ya want my mouth on it? ...Alright, but ya owe me."),
                _("Lord, straight outta %(src)s and into my mouth? Fine, darlin', but don't go makin' it a habit."),
            ],
            "ask_ok.cum_slut": [
                _("Fresh outta %(src)s's ass and still drippin'? Sugar, ya know I ain't sayin' no to that."),
                _("Mmm, bring it here, darlin'. A lil' taste of %(src)s on it just makes it naughtier."),
            ],
            "ask_ok.hardcore_sex": [
                _("Ya want me suckin' it clean after %(src)s's ass? Filthy bastard... get over here, sugar."),
                _("Hell yes. Shove it in my mouth dirty, darlin', just like it came outta %(src)s."),
            ],
            "ask_ok.cute_sex": [
                _("Oh my... right after %(src)s's behind? I... okay, sugar, but please be gentle with me."),
                _("Ya really want that, darlin'? It was just inside %(src)s... alright, but go slow and hold my hand."),
            ],
            "ask_ok.anal_lover": [
                _("So %(src)s gets it in the ass and all I get is the cleanup? ...Fine, sugar, but I'm next."),
                _("Lucky girl, that %(src)s. Gimme it, darlin', least I can taste what I've been missin'."),
            ],
            "ask_ok.lesbian": [
                _("It's %(src)s I'm tastin', not you, sugar. Keep that straight and I'll do it."),
                _("Ugh... if it didn't have %(src)s all over it I'd say no. Just get it over with, darlin'."),
            ],
            "ask_no._default": [
                _("After it's been up %(src)s's ass? No sir, sugar, go wash that thing first."),
                _("I ain't puttin' my mouth on that, darlin'. Not straight outta %(src)s, not a chance."),
            ],
            "ask_no.cute_sex": [
                _("Sugar, no... it was just inside %(src)s's bottom. I can't, that's too much for me."),
                _("Please don't ask me that, darlin'. Not after %(src)s... can't ya just kiss me instead?"),
            ],
            "ask_no.hardcore_sex": [
                _("I like it nasty, sugar, but I ain't %(src)s's cleanup rag. Earn it some other way."),
                _("Not happenin'. Fuck my throat raw any day, darlin', but not fresh outta %(src)s's ass."),
            ],
            "ask_no.hate_cum": [
                _("Your mess is bad enough on a good day, sugar. With %(src)s's ass on top of it, no way."),
                _("Absolutely not, darlin'. I can barely stand the taste of ya clean, let alone after %(src)s."),
            ],
            "ask_no.anal_hater": [
                _("That thing was up %(src)s's ass! Keep it far away from my mouth, sugar, I mean it."),
                _("Ew, no! Anythin' that's been in %(src)s's backside ain't comin' near my lips, darlin'."),
            ],
            "ask_no.lesbian": [
                _("I'd taste %(src)s any day, sugar, but not off of you. Keep that thing away from me."),
                _("No. If I want %(src)s on my tongue I'll go to the source, darlin', not through your cock."),
            ],
            "react._default": [
                _("Oh Lord... that's %(src)s I'm tastin', ain't it? I can't believe I'm doin' this, sugar."),
                _("Mmph... it's still warm from %(src)s. You're trouble, darlin', ya know that?"),
            ],
            "react.cum_slut": [
                _("Mmm... %(src)s's ass and your pre all mixed up. Sugar, that's downright sinful."),
                _("Oh, that's nasty... and I want more. Feed me all of it, darlin', %(src)s's taste and yours."),
            ],
            "react.hate_cum": [
                _("Ugh... that's %(src)s's ass and you leakin' already. Lord, I might be sick, sugar."),
                _("Blegh... it tastes like %(src)s and salt. Don't ya dare make this any worse, darlin'."),
            ],
            "react.hardcore_sex": [
                _("Fuck, I can taste %(src)s's ass all over ya. That's downright nasty, sugar... now push it deeper."),
                _("Mmm, filthy... and I ain't complainin'. Don't ya dare go easy on me, darlin'."),
            ],
            "react.submissive": [
                _("Fuck, I can taste %(src)s's ass all over ya. Treat me like the dirty slut I am, sugar."),
                _("Mmm, that's filthy... usin' my mouth to wipe off %(src)s. Ya better not go easy on me, darlin'."),
                _("That's %(src)s on ya, sugar... tell me to lick it clean and I'll do it, darlin'."),
            ],
            "react.cute_sex": [
                _("Oh... oh gosh, that's %(src)s I'm tastin'. Don't look at me like that, sugar, I'm blushin'."),
                _("It's so strange, darlin'... warm and a lil' like %(src)s. Be sweet to me, okay?"),
            ],
            "react.anal_lover": [
                _("Mmm... so that's what %(src)s's ass did to ya. I'm so jealous I could scream, sugar."),
                _("I can taste how deep ya were in %(src)s, darlin'. Shoulda been my turn back there."),
            ],
            "react.anal_hater": [
                _("Oh God, it tastes like ass... %(src)s's ass! I'm gonna gag, sugar, I swear."),
                _("Ugh, nasty, nasty... I can't stop thinkin' where that was in %(src)s. Ya owe me big, darlin'."),
            ],
            "react.lesbian": [
                _("That's %(src)s on my tongue... that part ain't half bad. It's you I can't stand, sugar."),
                _("I'm just pretendin' it's all %(src)s, darlin'. Don't go thinkin' I like your cock."),
            ],
            "moan._default": [
                _("Mmph... straight outta %(src)s... you're a wicked man, sugar..."),
                _("Glk... I still taste %(src)s on ya... mmm..."),
                _("Mmm... the things I do for ya, darlin'... mmph..."),
            ],
            "moan.cum_slut": [
                _("Mmm... gimme that load, sugar... %(src)s's flavor and all... glk..."),
                _("Glk... so dirty... hurry up and fill my mouth, darlin'..."),
                _("Mmph... lickin' %(src)s off ya 'til ya burst... mmm..."),
            ],
            "moan.hate_cum": [
                _("Mmph... ugh... don't ya dare leak on my tongue, sugar..."),
                _("Glk... %(src)s's ass is bad enough... warn me before ya blow, darlin'..."),
                _("Hnngh... blegh... %(src)s and you both on my tongue... I hate this..."),
            ],
            "moan.hardcore_sex": [
                _("Mmm... choke me on it... still dirty from %(src)s... mmph..."),
                _("Mmph... harder, sugar... glk... don't ya dare slow down..."),
                _("Glk... deeper, darlin'... mmm... rough as ya like..."),
            ],
            "moan.submissive": [
                _("Glk... fuck my throat, sugar... make me clean %(src)s off every inch..."),
                _("Mmph... harder... I'm your filthy lil' ass rag, darlin'... glk..."),
                _("Mmph... I'm yours, sugar... glk... use me however ya want..."),
            ],
            "moan.cute_sex": [
                _("Mmm... slow, sugar... I'm tryin' not to think about %(src)s..."),
                _("Mmph... stroke my hair, darlin'... it helps..."),
                _("Hnn... it's so embarrassin'... %(src)s is watchin' me do this... mmph..."),
            ],
            "moan.anal_lover": [
                _("Mmph... ya went so deep in %(src)s... do me like that next, sugar..."),
                _("Glk... tastin' it just makes me ache back there, darlin'..."),
                _("Mmm... lucky %(src)s... mmph... I want it in the rear too..."),
            ],
            "moan.anal_hater": [
                _("Mmph... eww... I can't believe this was in %(src)s's butt, sugar..."),
                _("Glk... nasty... tastes like a backside... hurry up, darlin'..."),
                _("Hnn... blegh... %(src)s's ass on my tongue... never again... mmph..."),
            ],
            "moan.lesbian": [
                _("Mmph... it's %(src)s I'm tastin'... only %(src)s... not you..."),
                _("Glk... just finish already, sugar... I ain't enjoyin' your part..."),
                _("Mmm... %(src)s tastes sweet... shame she comes with you attached, darlin'..."),
            ],
            "entry._default": [
                _("Ya gonna finish in my mouth after bein' in %(src)s's ass? You're somethin' else, sugar."),
                _("Go on then, darlin'. %(src)s's taste and yours, all at once... Lord help me."),
            ],
            "entry.cum_slut": [
                _("Yes, sugar, give it to me! Your cum with a lil' %(src)s on top, I want every drop."),
                _("Don't ya pull out, darlin'. Dirty from %(src)s or not, that load is mine."),
            ],
            "entry.hate_cum": [
                _("Oh no... first %(src)s's ass, now this? Make it quick, sugar, before I change my mind."),
                _("I already hate the taste, darlin', and now it's comin' with %(src)s mixed in. Ugh."),
            ],
            "entry.hardcore_sex": [
                _("Do it, sugar. Dump it down the same throat that just licked %(src)s's ass off ya."),
                _("Blow it in my dirty mouth, darlin'. %(src)s got the fuckin', I get the filth."),
            ],
            "entry.cute_sex": [
                _("Y-you're close, sugar? Okay... just be gentle, it's already a lot with %(src)s on there."),
            ],
            "entry.cute_sex.first_atm": [
                _("Hold me when ya do it, darlin'. I never took anythin' like this before, not after %(src)s."),
            ],
            "entry.anal_hater": [
                _("You're fixin' to cum on top of that taste? %(src)s's ass and now this... ugh, just do it, sugar."),
                _("Lord, as if %(src)s's backside wasn't enough. Hurry up and be done, darlin'."),
            ],
            "swallow_ok._default": [
                _("Swallow it, after where it's been in %(src)s? Lord... alright, sugar, here goes nothin'."),
                _("Mmph... fine, darlin'. But ya better never tell %(src)s how easy I gave in."),
            ],
            "swallow_ok.cum_slut": [
                _("Ya don't gotta tell me twice, sugar. I ain't wastin' a drop, %(src)s's taste or not."),
                _("Mmm, like I'd ever spit. Watch close, darlin', and let %(src)s watch too."),
            ],
            "swallow_ok.hardcore_sex": [
                _("Fuck yes. Cum and %(src)s's ass in one gulp, that's the nastiest thing I ever did, darlin'."),
                _("Swallow it? Hell, sugar, watch me. Every nasty drop, %(src)s's taste and all."),
            ],
            "swallow_ok.submissive": [
                _("Make me, sugar. Hold my jaw shut 'til I gulp down every filthy drop."),
                _("Tell me to swallow, darlin', and it's goin' down. I do what ya say."),
                _("Yes, sugar... I'm your good girl. Every drop, %(src)s's taste and all, 'cause ya told me to."),
            ],
            "swallow_ok.cute_sex": [
                _("S-swallow it? Oh gosh... okay, sugar, but only 'cause it's you askin'."),
                _("If it makes ya happy, darlin'... I'll do it. Just hold me close, %(src)s's taste is a lot."),
            ],
            "swallow_ok.anal_lover": [
                _("Fine, sugar, I'll swallow. But next time it's my turn to get what %(src)s got."),
                _("Down it goes, darlin'. Now ya owe me the same poundin' ya gave %(src)s."),
            ],
            "swallow_no._default": [
                _("It was in %(src)s's ass, sugar. Suckin' it was one thing, I ain't swallowin' that."),
                _("Nuh uh, darlin'. I'm spittin' this out, that's more of %(src)s than I ever needed."),
            ],
            "swallow_no.cute_sex": [
                _("I'm sorry, sugar, I just can't... not with %(src)s's taste in there too. I gotta spit."),
                _("Please don't make me, darlin'. It's too much, I need a tissue and a minute."),
            ],
            "swallow_no.hardcore_sex": [
                _("Nah, sugar. I'll spit it right back on your cock, that's filthier than swallowin' %(src)s's leftovers."),
                _("Swallowin's too tidy, darlin'. Watch me drool it down my chin and let %(src)s lick it up."),
            ],
            "swallow_no.hate_cum": [
                _("Not a chance, sugar. I hate the stuff plain, and this batch has %(src)s's ass in it."),
                _("Ugh, no! Get me a towel, darlin', I ain't keepin' this in my mouth one more second."),
            ],
            "swallow_no.anal_hater": [
                _("Swallow somethin' that touched %(src)s's ass? Ya must be crazy, sugar, it's comin' right out."),
                _("No, no, no. I need to spit and rinse my mouth, darlin', I can still taste %(src)s's backside."),
            ],
            "after_swallow._default": [
                _("I can't believe I just did that with %(src)s watchin'... not a word leaves this room, sugar."),
                _("Lord have mercy. Swallowed it all, %(src)s's taste included... what're ya turnin' me into, darlin'?"),
            ],
            "after_swallow.cum_slut": [
                _("Mmm, all gone. A lil' %(src)s made it extra naughty, sugar... got any more for me?"),
                _("Best load all week, darlin'. Maybe I oughta thank %(src)s for the seasonin'."),
            ],
            "after_swallow.hate_cum": [
                _("Ugh... it's gone. I can still taste you and %(src)s both, sugar, and I hate every bit of it."),
                _("Never again, darlin'. I need water, mouthwash, and an apology from you and %(src)s."),
            ],
            "after_swallow.hardcore_sex": [
                _("Licked ya clean of %(src)s's ass and swallowed the lot. I'm a nasty lil' whore, ain't I, sugar?"),
                _("Fuck, that was filthy, sugar. I'm soakin' wet... ya ain't done with me yet, are ya?"),
            ],
            "after_swallow.submissive": [
                _("Fuck, that was filthy. Next time make %(src)s watch up close while ya use me, darlin'."),
                _("Swallowed it all like ya told me, sugar. I'm yours to use, don't ya forget it."),
                _("Lord, I'd do anythin' ya ask me, darlin'. Just say what's next."),
            ],
            "after_swallow.cute_sex": [
                _("I... I really did that. Please don't think less of me, sugar, and don't let %(src)s tease me."),
                _("My face is burnin', darlin'. Can ya just hold me a while and not say anythin'?"),
            ],
            "after_swallow.lesbian": [
                _("The %(src)s part I could get used to. Swallowin' you is the part I wanna forget, sugar."),
                _("Don't get any ideas, darlin'. I did that for the taste of %(src)s, not 'cause I like your cum."),
            ],
        },
        "ntw": {
            "ask_ok._default": [
                _("That was just in %(src)s's ass and now you want my mouth on it? ...Fuck. Fine. One time, idiot."),
                _("You've got nerve, genius. Okay. Get over here before I change my mind. Don't smile."),
            ],
            "ask_ok.cum_slut": [
                _("Fresh out of %(src)s and still dripping? Give it here. Yeah, I said it."),
                _("I don't care where it's been, idiot. I care where you finish. Get it in my mouth."),
            ],
            "ask_ok.hardcore_sex": [
                _("Straight from %(src)s's ass to my throat? That's fucking filthy. Do it. Don't be gentle about it."),
                _("Out of %(src)s and into my mouth. Filthy. Fine. Go hard, genius."),
            ],
            "ask_ok.submissive": [
                _("Treat me like your dirty little cleanup crew, huh? Good. Shove it in, genius."),
                _("You want %(src)s cleaned off you. Fine. Tell me to. I'll do it."),
                _("My mouth, your call. Use it. Shut up about it."),
            ],
            "ask_ok.cute_sex": [
                _("After %(src)s's ass? That's... a lot, idiot. Fine. Just go slow with me. Shut up."),
                _("Okay. But hold my face when I do it. Gently. Don't make me say it twice."),
            ],
            "ask_ok.anal_lover": [
                _("So %(src)s gets it in the ass and I get the leftovers? Fine. But I'm next, idiot."),
                _("Give it here, genius. At least let me taste what I missed out on. Don't smile."),
            ],
            "ask_ok.lesbian": [
                _("It was in %(src)s, so that part I can live with. You're the part I hate. Fine. Get it over with."),
                _("Fine. But I'm thinking about a girl the whole time, not you. Don't get ideas, genius."),
            ],
            "ask_no._default": [
                _("It was just in %(src)s's ass, genius. Wash it or fuck off. I'm not doing that."),
                _("No. Hard no. Find another mouth, idiot, this one's closed."),
            ],
            "ask_no.cute_sex": [
                _("No. Not right after %(src)s like that. That's too much for me, okay? Shut up."),
                _("Don't ask me that, idiot. I wanted something nice with you, not this. No."),
            ],
            "ask_no.hardcore_sex": [
                _("I like it dirty, not stupid. Straight out of %(src)s's ass? Earn that first, genius. No."),
                _("Nice try. You don't get to use my mouth as a rag today. Ask again when I'm in the mood, idiot."),
            ],
            "ask_no.hate_cum": [
                _("I barely put up with your cum, and now you add %(src)s's ass to the menu? Fuck no."),
                _("Absolutely not. It's already gross when it's clean, idiot. Get that thing away from my face."),
            ],
            "ask_no.anal_hater": [
                _("That was in %(src)s's ass. An ass, genius. It is not going anywhere near my mouth."),
                _("Are you fucking kidding me? Anal is gross enough from across the bed. No. Go wash."),
            ],
            "ask_no.lesbian": [
                _("%(src)s I'd taste all day. Off your dick? No. Not happening, idiot."),
                _("No. If I want to know how a girl tastes, I'll skip the middleman. Put it away."),
            ],
            "react._default": [
                _("Fuck. That's %(src)s, alright. I can taste exactly where you've been, idiot."),
                _("Nasty. Shut up. I didn't say I was stopping, genius."),
            ],
            "react.cum_slut": [
                _("Mmm... %(src)s and you on the same cock. Fuck, that's dirty. Now hurry up and feed me."),
                _("Tastes wrong. I like it. Shut up and give me the rest, genius."),
            ],
            "react.hate_cum": [
                _("Great, it tastes like %(src)s's ass, and it only gets worse when you cum. Fuck."),
                _("Gross. It's already leaking, isn't it? Warn me before you blow, idiot."),
            ],
            "react.hardcore_sex": [
                _("I can taste %(src)s's ass all over you. That's disgusting. Push it deeper."),
                _("Tastes like %(src)s's ass. Vile. Faster, idiot."),
            ],
            "react.submissive": [
                _("Filthy bastard, making me clean this off. Yeah, I like it. Don't smile."),
                _("That's %(src)s. Tell me to keep licking. I will."),
                _("I do what you say. Apparently. Keep it in, idiot."),
            ],
            "react.cute_sex": [
                _("Oh god... that's %(src)s I'm tasting. This is so embarrassing. Don't look at me, idiot."),
                _("It's... strong. Just keep your hand in my hair, okay? Gently. Shut up."),
            ],
            "react.anal_lover": [
                _("So that's what %(src)s's ass did to you. Fuck. You're still warm from it. Not fair."),
                _("Tastes like a good pounding I didn't get. I'm jealous, idiot. Yeah, I said it."),
            ],
            "react.anal_hater": [
                _("Ugh... that's ass. That is %(src)s's actual ass in my mouth. I hate you so much."),
                _("Oh, that's foul. Don't you dare laugh, genius. I'm going to gag."),
            ],
            "react.lesbian": [
                _("Hm. That's %(src)s. That part's... not bad, actually. It's your dick that ruins it."),
                _("I can taste a girl on you. Shut up. It's the only reason I'm still down here, idiot."),
            ],
            "moan._default": [
                _("Mmph... tastes like %(src)s... you're a pig..."),
                _("Glk... mmm... fuck you for this, idiot..."),
                _("Mmm... don't get used to it... mmph..."),
            ],
            "moan.cum_slut": [
                _("Mmph... %(src)s got the cock, I get the cum... mmm... fair trade..."),
                _("Glk... mmm... come on, genius... fill my mouth already..."),
                _("Mmm... dirty and leaking... fuck, give it to me..."),
            ],
            "moan.hate_cum": [
                _("Mmph... %(src)s's ass and your precum... ugh... worst combo..."),
                _("Glk... ugh... don't you dare cum without warning, idiot..."),
                _("Mmm... ngh... this is so fucking gross... hurry up..."),
            ],
            "moan.hardcore_sex": [
                _("Mmph... harder, idiot... fuck my throat like you mean it..."),
                _("Mmph... rougher... glk... I said rougher, idiot..."),
                _("Glk... deeper, genius... mmph... all of it..."),
            ],
            "moan.submissive": [
                _("Glk... mmph... make me clean %(src)s's ass off you... fuck yes..."),
                _("Mmm... I'm your filthy little rag... glk... shut up, I like it..."),
                _("Mmph... yours... glk... use it, genius..."),
            ],
            "moan.cute_sex": [
                _("Mmph... I'm really tasting %(src)s... this is so dirty... don't stare..."),
                _("Mmm... slower, idiot... mmph... be nice to me..."),
                _("Glk... mm... tell me I'm doing good... shut up, just say it..."),
            ],
            "moan.anal_lover": [
                _("Mmph... %(src)s got it all the way in... mmm... lucky bitch..."),
                _("Mmm... still hot from it... glk... next one goes in me, genius..."),
                _("Glk... mmph... I'd rather be bent over right now... don't stop..."),
            ],
            "moan.anal_hater": [
                _("Mmph... ugh... %(src)s's ass... I'm going to throw up on you..."),
                _("Glk... hhk... this is vile, idiot... you owe me..."),
                _("Mmm... hrk... stop enjoying this so much... mmph... so gross..."),
            ],
            "moan.lesbian": [
                _("Mmph... at least it tastes like %(src)s... mmm... not like you..."),
                _("Glk... mmph... I'm licking a girl off you... that's all this is..."),
                _("Mmm... don't moan at me, idiot... mmph... it isn't for you..."),
            ],
            "entry._default": [
                _("You're about to blow, aren't you? Out of %(src)s's ass and into my mouth. You're unbelievable, idiot."),
                _("Fine. Do it. My mouth's already ruined anyway. Don't smile about it."),
            ],
            "entry.cum_slut": [
                _("Finally. %(src)s warmed you up, but the load is mine. Every drop, genius."),
                _("Don't you dare pull out. I want it thick and on my tongue. Stop grinning and cum."),
            ],
            "entry.hate_cum": [
                _("Oh, great. %(src)s's ass first and now your cum on top. This day keeps getting better."),
                _("You're twitching. Fuck. Make it quick, idiot, and don't expect me to like it."),
            ],
            "entry.hardcore_sex": [
                _("Go on. Dump it in my dirty mouth, right on top of %(src)s's ass. Make a mess of me."),
                _("Do it. Fill my mouth. Messy as you can, genius. Don't hold back."),
            ],
            "entry.submissive": [
                _("Fuck yes, use me like a cum rag. Don't hold back now, genius."),
                _("Finish where you want. It's your mouth right now. Don't gloat."),
                _("Tell me to take it. I take it. Go on."),
            ],
            "entry.cute_sex": [
                _("You're close, huh? After %(src)s and everything... okay. Just look at me when you do it. Shut up."),
                _("Wait, already? Fine. Be gentle, idiot. And hold my hand. Don't make me say it twice."),
            ],
            "entry.anal_hater": [
                _("So it's %(src)s's ass and then a mouthful of cum. Fantastic. You owe me forever, idiot."),
                _("Hurry up and finish before I actually puke. I can still taste it, genius."),
            ],
            "swallow_ok._default": [
                _("Swallow it? After %(src)s's ass? ...Fuck. Fine. You're lucky I like you, idiot."),
                _("Ugh. Okay. Down it goes. Say one word about this and you're dead."),
            ],
            "swallow_ok.cum_slut": [
                _("Like you had to ask. %(src)s can watch me drink all of it. Mmm."),
                _("Obviously I'm swallowing, genius. Wasting cum is a crime. Give me a second to enjoy it."),
            ],
            "swallow_ok.hardcore_sex": [
                _("Swallow a load that came out of %(src)s's ass? Filthy. Watch me do it, idiot."),
                _("Swallow it. Obviously. Every nasty drop. Don't make a thing of it."),
            ],
            "swallow_ok.submissive": [
                _("Yeah, make me gulp it down like a good dirty slut. I'm into it. Shut up."),
                _("Say swallow and I swallow. That's how this works. Shut up."),
                _("Your load. Your order. Down it goes, %(src)s and all."),
            ],
            "swallow_ok.cute_sex": [
                _("All of it? After %(src)s...? Okay. For you. But you're kissing me after, idiot. No arguing."),
                _("Fine, I'll swallow. Just... say something nice first. Don't laugh, I mean it."),
            ],
            "swallow_ok.anal_lover": [
                _("Fine. %(src)s took it in the ass, I'll take it down the throat. Next time we swap, genius."),
                _("Yeah, I'll swallow. Closest I'm getting to an ass fuck today, apparently. Don't smile."),
            ],
            "swallow_no._default": [
                _("No. It was in %(src)s's ass, genius. Sucking it was the favor. I'm spitting."),
                _("Not a chance. Hand me a tissue, idiot. That's as far as this goes."),
            ],
            "swallow_no.cute_sex": [
                _("I can't. Not after %(src)s, not like this. Don't be mad, idiot. I'm spitting it out."),
                _("No... that's too much for me. I did the rest for you, okay? Let me have this one."),
            ],
            "swallow_no.hardcore_sex": [
                _("No. I'd rather spit it back on your cock and make %(src)s watch. Swallowing's for good girls."),
                _("It's going down my chin, not my throat. Messier that way, genius. Deal with it."),
            ],
            "swallow_no.hate_cum": [
                _("Swallow? Your cum, seasoned with %(src)s's ass? Fuck no. Where's the trash can."),
                _("Not happening, idiot. It's vile enough sitting on my tongue. I'm spitting right now."),
            ],
            "swallow_no.anal_hater": [
                _("Anything that touched %(src)s's ass is not going in my stomach. I'm spitting, genius."),
                _("Hell no. I already need to bleach my tongue. Move, idiot, I'm getting rid of this."),
            ],
            "after_swallow._default": [
                _("I just swallowed something that was in %(src)s's ass. For you. You're welcome, idiot."),
                _("Fuck. I actually did that. Wipe that look off your face before I do it for you."),
            ],
            "after_swallow.cum_slut": [
                _("Mmm. Even after %(src)s's ass, your cum's still the best part. Don't let it go to your head."),
                _("All gone. Shut up, I'm not embarrassed. Go get hard again, genius."),
            ],
            "after_swallow.hate_cum": [
                _("Ugh. Cum and %(src)s's ass, all the way down. I need mouthwash and an apology."),
                _("That was disgusting. Never again, idiot. ...Stop looking so proud of yourself."),
            ],
            "after_swallow.hardcore_sex": [
                _("Swallowed it all, straight off %(src)s's ass. I'm a filthy bitch and you love it, genius."),
                _("Fuck, that was nasty. I'm soaked. Shut up and do something about it."),
            ],
            "after_swallow.cute_sex": [
                _("I can't believe I did that after %(src)s... come here. Hold me for a minute, idiot. Shut up."),
                _("That was the dirtiest thing I've ever done. Tell me you still like me. Don't laugh."),
            ],
            "after_swallow.lesbian": [
                _("The %(src)s part was fine. The you part, I'm going to need a drink to forget, idiot."),
                _("Don't read into it, genius. I swallowed. It doesn't mean I like dick. It means I lost a bet with myself."),
            ],
        },
        "tenny": {
            "ask_ok._default": [
                _("W-wait, it was just in %(src)s's ass... and you want my mouth? O-okay. Just don't laugh at me."),
            ],
            "ask_ok._default.first_atm": [
                _("I-I've never done anything like this... right after %(src)s? ...Okay. If it's for you, I'll try."),
            ],
            "ask_ok.cum_slut": [
                _("S-straight from %(src)s's ass? That's so dirty... b-but I want it. Please, let me have it."),
                _("I-I shouldn't want this so much... it was inside %(src)s and I still can't wait to get your cum. Give it to me."),
            ],
            "ask_ok.hardcore_sex": [
                _("Y-you want me to clean off what %(src)s left on it? ...God, that's filthy. S-shove it in my mouth."),
                _("S-straight out of %(src)s... that's so dirty. I-I want it. Don't be gentle, okay?"),
            ],
            "ask_ok.submissive": [
                _("F-fresh out of %(src)s's ass and into my throat... I-I'm sorry, that really turns me on. Use me."),
                _("I-if you tell me to clean %(src)s off you... I-I'll do it. I'll do whatever you say."),
                _("M-my mouth is yours... u-use it however you want, even after %(src)s."),
            ],
            "ask_ok.cute_sex": [
                _("T-that's a lot to ask... it was just in %(src)s. B-but if you hold my hand, I'll do it for you."),
                _("I-I'm so embarrassed... right after %(src)s? ...Okay. Just be gentle with me, p-please."),
            ],
            "ask_ok.anal_lover": [
                _("%(src)s got it in the ass and I-I only get the taste...? T-that's not fair... okay, give it here."),
                _("I-I'm a little jealous of %(src)s, honestly... fine, I'll suck it. B-but I'm the one who gets it back there next."),
            ],
            "ask_ok.lesbian": [
                _("I-it's %(src)s I'd be tasting, not you... that's the only reason I'm saying yes. D-don't get the wrong idea."),
                _("W-with a guy's... ugh. B-but it was inside %(src)s a second ago... okay. Just this once."),
            ],
            "ask_no._default": [
                _("N-no, I can't! It was just in %(src)s's ass... I-I'm sorry, that's too much for me."),
                _("P-please don't make me... not right after %(src)s. I really can't put that in my mouth."),
            ],
            "ask_no.cute_sex": [
                _("I-I'm sorry, no... that's too dirty for me. It was just inside %(src)s... can't we just kiss instead?"),
                _("N-not like this, please... straight from %(src)s? I-I want it to be sweet, not... that."),
            ],
            "ask_no.hardcore_sex": [
                _("I-I like it dirty, but not %(src)s's leftovers... sorry. W-wash it and then you can wreck my throat."),
                _("N-no. Fuck my mouth all you want, but not straight out of %(src)s's ass. I-I have some limits."),
            ],
            "ask_no.hate_cum": [
                _("I-I already hate the taste of you... and now with %(src)s's ass on it too? N-no. Sorry, no."),
                _("N-no way... the taste of cum already makes me gag. Add %(src)s's ass to it and I-I'd throw up. Sorry."),
            ],
            "ask_no.anal_hater": [
                _("T-that was in %(src)s's butt! That's disgusting... I-I'm not putting my mouth anywhere near it."),
                _("E-eww, no! Anything that comes out of there is gross... I-I don't care that it's %(src)s, I can't."),
            ],
            "ask_no.lesbian": [
                _("I-I'd rather just kiss %(src)s... I'm not putting a guy's thing in my mouth to get a taste of her. N-no."),
                _("N-no... if I want to taste %(src)s, I'll ask her myself. I-I don't need you in the middle. Sorry."),
            ],
            "react._default": [
                _("Mmh... oh god, it r-really does taste like %(src)s... this is so wrong..."),
                _("I-it's still warm from %(src)s... I can't believe I'm actually d-doing this..."),
            ],
            "react.cum_slut": [
                _("Mmm... %(src)s is all over it... t-that just makes me want your cum even more..."),
                _("S-so dirty... first the taste of %(src)s, and soon yours on top. I-I'm sorry, I love this..."),
            ],
            "react.hate_cum": [
                _("Ugh... it's b-bitter from %(src)s already... and it only gets worse when you finish, doesn't it..."),
                _("I-it tastes awful... %(src)s and you, all mixed together... p-please don't take long..."),
            ],
            "react.hardcore_sex": [
                _("F-fuck... I can taste %(src)s's ass on your cock... I-I'm such a dirty girl, aren't I?"),
                _("Mmh... it's so f-filthy... %(src)s is all over it... d-deeper, please..."),
            ],
            "react.submissive": [
                _("Mmh... you're making me lick %(src)s off your cock... w-why does that make me so wet..."),
                _("I-I'll lick off every bit of %(src)s... j-just tell me I'm being good..."),
                _("Mmh... t-tell me what to do next... I-I'll obey..."),
            ],
            "react.cute_sex": [
                _("Mm... i-it tastes like %(src)s... please don't look at my face right now, I'm so embarrassed..."),
                _("Oh... I-I can really tell where it's been... tell me I'm doing good, p-please..."),
            ],
            "react.anal_lover": [
                _("Mmm... so this is what %(src)s got to feel... I-I'm so jealous. It should've been me..."),
                _("Y-you were really deep in %(src)s, weren't you... tasting it makes me ache back there..."),
            ],
            "react.anal_hater": [
                _("Urgh... t-that's %(src)s's butt on my tongue... I-I think I'm going to be sick..."),
                _("E-eww, eww... it really tastes like it came out of %(src)s... why did I say yes..."),
            ],
            "react.lesbian": [
                _("Mm... t-that's %(src)s... I don't mind that part. It's the rest of you I can't stand."),
                _("I-if I close my eyes, it's only %(src)s I'm tasting... d-don't talk, you'll ruin it."),
            ],
            "moan._default": [
                _("Mmph... s-straight from %(src)s... mmm... what am I doing..."),
                _("Glk... mmh... i-it still has %(src)s on it..."),
                _("Mmm... mmph... a-am I doing it right...?"),
            ],
            "moan.cum_slut": [
                _("Mmph... h-hurry and cum... mmm... tasting %(src)s got me so hungry..."),
                _("Glk... mmm... %(src)s's taste and yours... I-I want it all..."),
                _("Mmm... p-please... mmph... fill my mouth up..."),
            ],
            "moan.hate_cum": [
                _("Mmph... ugh... %(src)s's taste is b-bad enough... glk... warn me first..."),
                _("Glk... hhk... I-I'm going to gag..."),
                _("Mmh... i-it's leaking already... ugh... mmph..."),
            ],
            "moan.hardcore_sex": [
                _("Glk... mmph... d-deeper... choke me on what was in %(src)s's ass..."),
                _("Mmph... h-harder... glk... d-don't stop..."),
                _("Glk... f-faster... mmm... I-I can take it..."),
            ],
            "moan.submissive": [
                _("Mmph... u-use my mouth like you used %(src)s... glk..."),
                _("Hhk... mmm... I-I'm just your filthy rag... mmph..."),
                _("Mmph... y-yours... glk... u-use me..."),
            ],
            "moan.cute_sex": [
                _("Mmh... p-please... mmm... stroke my hair while I do this..."),
                _("Mmph... t-this is so embarrassing... it still tastes like %(src)s..."),
                _("Mm... s-slowly, please... mmph... I'm trying my best..."),
            ],
            "moan.anal_lover": [
                _("Mmph... l-lucky %(src)s... mmm... I want it in me next..."),
                _("Glk... mmm... y-you stretched %(src)s so good... I can tell..."),
                _("Mmh... glk... p-promise I get it back there too..."),
            ],
            "moan.anal_hater": [
                _("Ugh... mmph... i-it tastes like %(src)s's butt... glk..."),
                _("Hhk... I-I'm trying not to think about where it was... mmph..."),
                _("Glk... s-so gross... mmh... are you close yet...?"),
            ],
            "moan.lesbian": [
                _("Mmph... j-just thinking about %(src)s... mmm... not you..."),
                _("Mmm... %(src)s tastes n-nice... glk... you don't..."),
                _("Glk... ugh... h-hurry up and finish... mmph..."),
            ],
            "entry._default": [
                _("Y-you're going to cum in my mouth? After it was in %(src)s... o-okay. I'm ready, I think."),
                _("I-I can feel you twitching... straight from %(src)s and now this. G-go ahead..."),
            ],
            "entry.cum_slut": [
                _("Y-yes, please, cum in my mouth! I-I don't care that it was in %(src)s, I want every drop!"),
                _("G-give it to me... %(src)s got your cock, b-but your cum is mine. Please..."),
            ],
            "entry.hate_cum": [
                _("W-wait, in my mouth? It already tastes like %(src)s's ass... ugh. J-just be quick about it."),
                _("I-I hate this part... first %(src)s's taste, now yours. P-please don't make it a lot..."),
            ],
            "entry.hardcore_sex": [
                _("D-do it... dump your load in the mouth that just cleaned %(src)s's ass off you. I-I deserve it."),
                _("Y-you're close... do it, fill my mouth. M-make it messy, please..."),
            ],
            "entry.submissive": [
                _("C-cum down my throat... I'm just your dirty hole after %(src)s. D-don't hold back."),
                _("W-wherever you want... I-I'm yours, even after %(src)s. J-just use me..."),
                _("T-tell me to open up and I will... I-I'll take whatever you give me..."),
            ],
            "entry.cute_sex": [
                _("Y-you're close? ...Okay. Look at me when you do, p-please... I did this for you, even after %(src)s."),
                _("I-it's okay, you can finish... j-just hold my face gently. It's been a lot, with %(src)s and all..."),
            ],
            "entry.anal_hater": [
                _("N-now you're going to cum too? On top of %(src)s's butt taste? ...Ugh. F-fine, just get it over with."),
                _("I-I can't believe I'm letting you... it was in %(src)s's ass, and now this. H-hurry, before I change my mind."),
            ],
            "swallow_ok._default": [
                _("S-swallow it...? After it was in %(src)s... mmh. O-okay. For you."),
                _("I-I... okay. It was in %(src)s's ass and I'm still going to do it. D-don't look at me..."),
            ],
            "swallow_ok.cum_slut": [
                _("Y-you don't even have to ask... mmm. I-I wouldn't waste a drop, even after %(src)s."),
                _("O-of course I'll swallow... it's your cum. %(src)s's taste just m-makes it naughtier."),
            ],
            "swallow_ok.hardcore_sex": [
                _("Y-yes... I'll swallow it, %(src)s's taste and all. That's so f-filthy... I love it."),
                _("I-I'm drinking it all down... every dirty drop. D-don't look away."),
            ],
            "swallow_ok.submissive": [
                _("Y-yes... make me swallow it, %(src)s's ass and all. I-I'm your filthy girl."),
                _("S-say it again... tell me to drink it down like a dirty slut. A-after %(src)s, I've earned it."),
                _("I-if you want me to swallow, I-I will... I do what you tell me..."),
            ],
            "swallow_ok.cute_sex": [
                _("I-if it makes you happy... okay. But k-kiss me after, even though it was in %(src)s... promise?"),
                _("O-okay... I'll swallow. I-I did all of this for you, %(src)s's taste and everything... so hold me after."),
            ],
            "swallow_ok.anal_lover": [
                _("F-fine, I'll swallow... but next time %(src)s gets the mouth and I-I get it in the ass. Deal?"),
                _("I-it's the closest I'll get to what %(src)s had tonight... s-so yes. I'll swallow it."),
            ],
            "swallow_no._default": [
                _("N-no... I'm sorry. It was in %(src)s's ass, I-I can't swallow that."),
                _("I-I did the rest, but not this... not after %(src)s. P-please let me spit it out."),
            ],
            "swallow_no.cute_sex": [
                _("D-don't make me, please... it's too much. It was just in %(src)s... I-I need to spit, I'm sorry."),
                _("I-I can't... I wanted to be good for you, but after %(src)s it's just too dirty. D-don't be mad..."),
            ],
            "swallow_no.hardcore_sex": [
                _("N-no. I'll take it on my face, in my hair, anywhere... b-but I'm not swallowing %(src)s's ass."),
                _("I-I'm filthy, not stupid... that was up %(src)s's ass. It's going on the floor, s-sorry."),
            ],
            "swallow_no.hate_cum": [
                _("S-spit, I need to spit... I hate it even when it's clean. With %(src)s's ass mixed in? N-no."),
                _("I-I'm going to be sick... your cum and %(src)s's taste together. N-no. It's coming out."),
            ],
            "swallow_no.anal_hater": [
                _("S-swallow something that touched %(src)s's butt? No! I-I need a tissue, right now."),
                _("G-gross, no... everything in my mouth tastes like %(src)s's ass. I-I'm spitting it out."),
            ],
            "after_swallow._default": [
                _("I-I really swallowed it... after it was in %(src)s. P-please don't tell anyone, okay?"),
                _("Oh god... w-what's wrong with me? That came straight from %(src)s and I just... did it."),
            ],
            "after_swallow.cum_slut": [
                _("Mmm... I-I'm sorry, I liked that way too much. %(src)s can warm you up for me a-anytime."),
                _("A-all gone... it tasted dirtier after %(src)s, and I-I think I liked it better that way..."),
            ],
            "after_swallow.hate_cum": [
                _("Ugh... I-I can still taste it. You and %(src)s, both... I need water. A lot of water."),
                _("N-never again... I can barely stand it normally, and after %(src)s it was so much worse. Y-you owe me."),
            ],
            "after_swallow.hardcore_sex": [
                _("I-I just drank your cum straight off %(src)s's ass... god, I'm disgusting. D-do it to me again sometime."),
                _("T-that was the filthiest thing I've ever done... %(src)s's ass, then my throat. I-I loved it."),
            ],
            "after_swallow.cute_sex": [
                _("I-I did it... even after %(src)s. You still think I'm c-cute, right? Please say yes..."),
                _("T-that was so much for me... can you just hold me now? I-I can't even look at %(src)s."),
            ],
            "after_swallow.lesbian": [
                _("I-I did that for %(src)s's taste, not yours... d-don't think this changes what I am."),
                _("T-the part that was %(src)s, I didn't mind... the part that was you, I-I want to forget. Sorry."),
            ],
        },
    }
