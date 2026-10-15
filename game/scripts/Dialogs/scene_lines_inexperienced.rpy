# ============================================================
# scene_lines_inexperienced.rpy — "Low experience" dialogue
# ============================================================
#
# Pools for girls who HAVE a trait but haven't done the relevant
# act enough times to talk like a veteran. The resolver in
# scene_lines.rpy prepends a "_new" modifier when trait_is_new()
# is True; if the _new pool exists it wins, otherwise the
# experienced pool plays as before.
#
# Eager traits (cum_slut / hardcore / anal_lover) have two stages
# (trait_discovery_keys): "_first" = her very first time
# (trait_is_first), "_new" = her first few times (the first 3 loads
# / anal scenes, 2 sex scenes). A line that says "my first time",
# "I've never", "I had no idea" goes in "_first" ONLY. When a key
# has a "_first" twin, its "_new" pool plays only after the first
# time and may say "again" / "last time"; a "_new" pool with no
# twin plays on all of them and says neither. While one of her
# discovery pools answers, no veteran eager pool speaks first.
#
# Positive traits (_lover / _slut / hardcore_sex):
#   She is DISCOVERING she likes it. Curiosity, nervous excitement,
#   surprise at her own body, "I didn't expect..." — never
#   "my ass was made for your cock" veteran talk.
#
# Negative traits (_hater / hate_cum / cute_sex):
#   She fears it based on reputation / instinct, NOT past pain.
#   "I've heard this hurts" — never "it hurts every time."
# ============================================================

init 1 python:

    SCENE_LINES.update({

        # ══════════════════════════════════════════════════════════
        #  ANAL_LOVER — first time discovering she loves anal
        # ══════════════════════════════════════════════════════════

        # — Moans —
        "moan.speed1.anal.anal_lover_first": [
            _("Oh... this is... different than I imagined... but good different..."),

            _("I always wondered what this would feel like... oh..."),

            _("Mmm... it's actually... wow... I didn't expect this..."),

        ],
        "moan.speed1.anal.anal_lover_new": [
            _("Oh... there it is again... that feeling I can't stop thinking about..."),

            _("Mmm... it's still a little strange... and I still want it..."),

            _("Easy... I'm still getting used to how good this feels..."),

        ],
        "moan.speed2.anal.anal_lover_first": [
            _("Oh god... is it supposed to feel this good? Because... wow..."),

            _("I can't believe how much I'm... this is incredible..."),

            _("Why did I wait so long to try this... oh god..."),

        ],
        "moan.speed2.anal.anal_lover_new": [
            _("Oh god... it's even better than last time..."),

            _("I can't believe how much I'm... this is incredible..."),

            _("Why does this feel so good? I still don't understand it..."),

        ],
        "moan.speed3.anal.anal_lover_first": [
            _("Oh my god! I had no idea it could feel like THIS!"),

            _("How is this so good?! I never expected... oh god YES!"),

            _("This is nothing like I imagined... it's so much BETTER!"),

        ],
        "moan.speed3.anal.anal_lover_new": [
            _("Yes! Oh god, yes! How is it getting BETTER?!"),

            _("I thought I knew how this felt... it's never been like THIS!"),

            _("Don't stop! I don't care how it sounds, I love this!"),

        ],

        # — Girl orgasm —
        "girl_cum.anal.anal_lover_first": [
            _("Wait... am I... from THERE?! I'm actually... oh god! AAAH!"),

            _("I didn't know I could... from this?! It's happening! AAAH!"),

            _("Something's building... it's so different... I'm going to... AAAH!"),

        ],
        "girl_cum.anal.anal_lover_new": [
            _("Something's building... it's so different... I'm going to... AAAH!"),

            _("How can it feel this good back there?! I'm... I'm cumming! AAAH!"),

            _("Don't stop... don't stop... oh god, it's taking over! AAAH!"),

        ],
        "girl_post_cum.anal.anal_lover_first": [
            _("I just... came from that... I had no idea my body could do that..."),

            _("That was... I need a minute... I never expected to feel that way..."),

            _("I can't believe that just happened... is it always like this?"),

        ],
        "girl_post_cum.anal.anal_lover_new": [
            _("I just came from that... I don't think I'll ever get used to it..."),

            _("My whole body is still buzzing... how is that even possible from there?"),

            _("I should be embarrassed by how much I liked that... I'm not."),

        ],
        "girl_cum_hard.anal.anal_lover_first": [
            _("WHAT IS HAPPENING TO ME?! I've never felt anything like... AAAAAH!"),

            _("I didn't know this was POSSIBLE! My whole body is... AAAAAH!"),

            _("EVERYTHING is on fire! I never imagined... AAAAAH!"),

        ],
        "girl_cum_hard.anal.anal_lover_new": [
            _("IT'S TOO MUCH! IT'S TOO GOOD! DON'T STOP! AAAAAH!"),

            _("OH GOD, FROM THERE?! HOW IS IT THIS STRONG?! AAAAAH!"),

            _("MY WHOLE BODY... I CAN'T... AAAAAH!"),

        ],
        "girl_post_cum_hard.anal.anal_lover_first": [
            _("That was... the most intense thing I've ever felt... I'm shaking..."),

            _("I can barely think right now... how did my first time feel THAT good..."),

            _("I think I just found something I didn't know I needed..."),

        ],
        "girl_post_cum_hard.anal.anal_lover_new": [
            _("That was... the most intense thing I've ever felt... I'm shaking..."),

            _("I can't feel my legs... what are you doing to me?"),

            _("I keep telling myself it's just a phase... it's not, is it?"),

        ],

        # — Creampie —
        "cum_inside.anal.anal_lover_first": [
            _("Oh... I can feel it inside... that's a new sensation... wow..."),

            _("You came in there... it's so warm... I didn't expect it to feel like that..."),

            _("Is that what it feels like? Inside... back there? ...I think I like it..."),

        ],
        "cum_inside.anal.anal_lover_new": [
            _("So warm back there... I didn't think I'd like that part this much..."),

            _("Mmm... I can feel it deep inside... why does that make me so happy?"),

            _("It's filling me up back there... I could get used to this."),

        ],
        "cum_inside_accepted.anal.anal_lover_first": [
            _("Inside? I... I've never done that before... but yes. I want to know what it feels like."),

            _("Do it inside... I want to experience everything about this..."),

            _("Yes... finish in there. I need to know how this feels."),

        ],
        "cum_inside_accepted.anal.anal_lover_new": [
            _("Do it inside... I want to experience everything about this..."),

            _("Inside... yes. I want to feel that warmth back there."),

            _("Don't pull out... I want it in there."),

        ],
        "cum_inside_consented.anal.anal_lover_first": [
            _("I can feel every pulse... I've never felt anything like this before..."),

            _("So this is what it feels like... inside me there... it's... wow..."),

            _("I asked for it and... I'm glad I did. That warmth is incredible..."),

        ],
        "cum_inside_consented.anal.anal_lover_new": [
            _("I asked for it and... I'm glad I did. That warmth is incredible..."),

            _("Every pulse... I feel every single one back there... mmm..."),

            _("I asked for this... and I'm not even embarrassed. Well, a little."),

        ],
        "cum_inside_forced.anal.anal_lover_new": [
            _("You came inside without... oh. Oh that actually feels... really good..."),

            _("I wasn't ready for that... but now that I feel it... I don't mind at all..."),

            _("That was unexpected... but the warmth inside is... kind of amazing actually..."),

        ],
        "cum_inside_denied.anal.anal_lover_new": [
            _("Not inside... not yet. This is all so new... I need time to process..."),

            _("I'm still getting used to all of this... maybe next time..."),

            _("Everything is so overwhelming right now... can you finish somewhere else?"),

        ],

        # ══════════════════════════════════════════════════════════
        #  ANAL_HATER — fears anal from reputation, never tried it
        # ══════════════════════════════════════════════════════════

        # — Moans —
        "moan.speed1.anal.anal_hater_new": [
            _("I knew it... everyone says this hurts and they were right... ow..."),

            _("This is exactly as bad as I thought it would be... ow..."),

            _("I was scared of this for a reason... it's awful..."),

        ],
        "moan.speed2.anal.anal_hater_new": [
            _("It's worse than I imagined! Why did I agree to this?!"),

            _("Everyone warned me about this and they were ALL RIGHT!"),

            _("I should have listened to my instincts... this is terrible..."),

        ],
        "moan.speed3.anal.anal_hater_new": [
            _("STOP! It's even worse than I feared! I can't take this!"),

            _("I KNEW this was a bad idea! Everyone was right! OW!"),

            _("Nothing could have prepared me for how bad this is!"),

        ],

        # — Creampie —
        "cum_inside.anal.anal_hater_new": [
            _("You came inside?! I didn't even know that was a thing people did there!"),

            _("Wait, I can feel... is that... oh god. My first time and you CUM in there?!"),

            _("On top of everything else... now it's full of your cum too?! This is awful..."),

        ],
        "cum_inside_forced.anal.anal_hater_new": [
            _("You came inside on my FIRST TIME?! Without asking?! I can't believe you!"),

            _("My first time doing this and you just... inside?! That's SO much worse!"),

            _("I was already hating every second and then you cum inside?! Unbelievable!"),

        ],

        # — Orgasm —
        "girl_cum.anal.anal_hater_new": [
            _("Wait... what's happening... I'm not supposed to... from THIS?! AAAH!"),

            _("No way... my first time and I'm... how is my body doing this?! AAAH!"),

            _("This makes no sense... I don't even like this... why am I... AAAH!"),

        ],
        "girl_post_cum.anal.anal_hater_new": [
            _("I just came from something I've been dreading my whole life... what is wrong with me..."),

            _("My first time and my body... responded like THAT? I don't understand myself..."),

            _("I was so sure I would hate this... and then my body just... I'm so confused..."),

        ],


        # ══════════════════════════════════════════════════════════
        #  CUM_SLUT — loves the idea of cum but hasn't experienced it
        # ══════════════════════════════════════════════════════════

        # — Moans (anticipation) —
        "moan.speed1.cum_slut_first": [
            _("Mmm... I keep thinking about what happens when you finish..."),

            _("I want to know what it feels like when you... you know..."),

            _("I've been so curious about this... don't hold back when you're close..."),

        ],
        "moan.speed1.cum_slut_new": [
            _("Mmm... I keep thinking about what happens when you finish..."),

            _("I can't stop thinking about the last time you finished..."),

            _("Don't hold back when you're close... I want it again..."),

        ],
        "moan.speed2.cum_slut_first": [
            _("Are you getting close? I want to find out what it's like..."),

            _("I can't stop thinking about feeling you finish... please don't stop..."),

            _("I've imagined this so many times... I want to feel it for real..."),

        ],
        "moan.speed2.cum_slut_new": [
            _("I can't stop thinking about feeling you finish... please don't stop..."),

            _("Are you getting close? I want to feel it again..."),

            _("Why do I want it this much? I don't even care anymore..."),

        ],
        "moan.speed3.cum_slut_first": [
            _("Yes! I'm ready! I want to feel everything! Don't hold it back!"),

            _("Give it to me! I need to know what it feels like!"),

            _("I can feel you're close... please... I need to experience this..."),

        ],
        "moan.speed3.cum_slut_new": [
            _("Yes! I'm ready! I want to feel everything! Don't hold it back!"),

            _("Give it to me again! I can't believe how much I want it!"),

            _("I can feel you're close... please... I've been waiting for this all day..."),

        ],

        # — Cum reactions (first time) —
        "cum_inside.cum_slut_first": [
            _("Oh... oh wow... so this is what it feels like... it's so warm inside..."),

            _("I can feel it... every pulse... I didn't know it would be like THIS..."),

            _("That's... incredible. I finally know what it feels like and... wow..."),

        ],
        "cum_inside.cum_slut_new": [
            _("It's so warm inside... why does it feel THIS good?"),

            _("Every pulse... I feel every single one... I love that."),

            _("Mmm... I could get used to this feeling... I think I already am."),

        ],
        "cum_inside_accepted.cum_slut_first": [
            _("Yes! Inside! I've wanted to know what this feels like for so long!"),

            _("Please, finish inside... I need to experience it. I need to know."),

            _("Do it inside me... I've been dreaming about this moment..."),

        ],
        "cum_inside_accepted.cum_slut_new": [
            _("Please, finish inside... I want to feel it."),

            _("Inside... yes. Please don't pull out."),

            _("Do it inside me... I want that feeling."),

        ],
        "cum_inside_consented.cum_slut_first": [
            _("Oh my god... so THIS is what everyone talks about... it's amazing..."),

            _("I can feel every drop... my first time and it's already this good..."),

            _("I asked for this and... I'm so glad I did. It's better than I imagined..."),

        ],
        "cum_inside_consented.cum_slut_new": [
            _("I asked for this and... I'm so glad I did. It's better than I imagined..."),

            _("I can feel it filling me... I don't ever want this feeling to stop..."),

            _("Mmm... I'm not even embarrassed about how much I wanted that."),

        ],
        "cum_inside_forced.cum_slut_new": [
            _("You didn't ask but... oh. Oh that's... I actually love how this feels..."),

            _("You just... without warning... and it's... actually incredible? Wow..."),

            _("I wasn't expecting it but... the warmth is... I think I'm hooked already..."),

        ],

        "cum_face.cum_slut_first": [
            _("Oh! It's... warm... and there's so much of it... this is what I've been curious about?"),

            _("On my face... my first time... it's so much more intense than I imagined..."),

            _("Wow... I can feel it everywhere... I think I understand why I wanted this now..."),

        ],
        "cum_face.cum_slut_new": [
            _("It's all over my face... and I'm smiling. What is wrong with me?"),

            _("So warm... I shouldn't like this as much as I do..."),

            _("Mmm... there's so much... and I don't even mind."),

        ],
        "cum_mouth.cum_slut_first": [
            _("Mmm... so that's what it tastes like... it's different than I expected..."),

            _("My first taste... it's... I think I actually like it..."),

            _("In my mouth... finally I know what it's like... and I want more..."),

        ],
        "cum_mouth.cum_slut_new": [
            _("Mmm... that taste... I think I'm starting to crave it..."),

            _("Mmm... it's still weird... and I still want more."),

            _("That taste is growing on me... is that bad?"),

        ],
        "cum_mouth_accepted.cum_slut_first": [
            _("Yes, in my mouth! I've always wanted to know what it tastes like!"),

            _("Please, let me taste it... I've been so curious for so long..."),

            _("I want it in my mouth... I need to find out if I like it. And I think I will."),

        ],
        "cum_mouth_accepted.cum_slut_new": [
            _("In my mouth... yes. I want to taste it."),

            _("Let me taste it... please. I want to."),

            _("In my mouth... I don't know why I want it so much, but I do."),

        ],
        "cum_tits.cum_slut_first": [
            _("Oh... it's all over my chest... it's warm... I like how this feels..."),

            _("So much of it... on me... my first time... it's better than I thought..."),

            _("I've been wanting to feel this... and it's everything I hoped for..."),

        ],
        "cum_tits.cum_slut_new": [
            _("Oh... it's all over my chest... it's warm... I like how this feels..."),

            _("Look at all of it... I can't stop touching it..."),

            _("Mmm... all over me... I'm way too happy about this."),

        ],

        "creampie_aftermath.cum_slut_first": [
            _("I can still feel it inside me... my first creampie... that was amazing..."),

            _("So that's what a creampie feels like... I need this again. Soon."),

            _("My first time feeling someone finish inside... I already want more..."),

        ],
        "creampie_aftermath.cum_slut_new": [
            _("I can still feel it inside me... mmm... I love that feeling."),

            _("It's dripping out of me... and I'm smiling like an idiot."),

            _("I want to stay like this for a while... full of you."),

        ],


        # ══════════════════════════════════════════════════════════
        #  HATE_CUM — disgusted by the idea, never experienced it
        # ══════════════════════════════════════════════════════════

        # — Moans (dread) —
        "moan.speed1.hate_cum_new": [
            _("Just... don't finish on me, okay? I've always been grossed out by that..."),

            _("I don't want to feel your... stuff. The idea alone makes me cringe..."),

            _("Promise me you won't get any of it on me... please..."),

        ],
        "moan.speed2.hate_cum_new": [
            _("You're getting harder... are you close? Keep it away from me..."),

            _("I've always dreaded this part... please use a condom or something..."),

            _("Don't you dare finish on me... I've seen what that looks like and I want no part of it..."),

        ],
        "moan.speed3.hate_cum_new": [
            _("You're about to... oh no no no, get it away from me!"),

            _("NOT on me! NOT inside! I'm not ready for... whatever that is!"),

            _("Pull out! The last thing I want is to find out what that feels like!"),

        ],

        # — Cum reactions (first encounter confirming her fears) —
        "cum_inside.hate_cum_new": [
            _("Is that... inside me? Oh god it's... it's exactly as gross as I imagined..."),

            _("I can feel it... oh no... this is everything I was afraid of..."),

            _("That's the most disgusting thing I've ever felt... I knew I would hate this..."),

        ],
        "cum_inside_forced.hate_cum_new": [
            _("You came INSIDE me?! My first time feeling that and you didn't even ASK?!"),

            _("I've been dreading this my entire life and you just DID it?! Get off me!"),

            _("I TOLD you not to! And now I know exactly why I was right to be scared!"),

        ],

        "cum_face.hate_cum_new": [
            _("You... on my FACE?! That's... it's... even worse than I imagined! Get it off!"),

            _("Oh god it's on me... it's sticky and warm and GROSS! I knew I'd hate this!"),

            _("My face... you got it on my face... I'm going to be sick... get it OFF!"),

        ],
        "cum_mouth.hate_cum_new": [
            _("In my MOUTH?! Oh god... the taste is... I think I'm going to... ugh!"),

            _("I can taste it... this is the worst thing I've ever... I KNEW it! Disgusting!"),

            _("My mouth... it's in my mouth... everything I feared was EXACTLY right!"),

        ],


        # ══════════════════════════════════════════════════════════
        #  HARDCORE — craves intensity but hasn't had sex yet
        # ══════════════════════════════════════════════════════════

        # — Moans —
        "moan.speed1.hardcore_new": [
            _("Is that all? Come on... I think I can take more than this..."),

            _("This is... nice... but I feel like there should be more..."),

            _("I don't know why, but I need this to be... rougher somehow..."),

        ],
        "moan.speed2.hardcore_first": [
            _("Yes... this is more like it... I didn't know I needed this..."),

            _("Harder... I think I want it harder... is that weird for a first time?"),

            _("Oh god... my body is responding to this way more than I expected..."),

        ],
        "moan.speed2.hardcore_new": [
            _("Oh god... my body is responding to this way more than I expected..."),

            _("Harder... I've been thinking about this since last time..."),

            _("Yes... like that... I need it rougher..."),

        ],
        "moan.speed3.hardcore_first": [
            _("YES! This is what I needed! I didn't know it could feel like this!"),

            _("Don't stop! My body wants this so badly... I can't believe how good this feels!"),

            _("More! I never imagined my first time would be this intense and I LOVE it!"),

        ],
        "moan.speed3.hardcore_new": [
            _("Don't stop! My body wants this so badly... I can't believe how good this feels!"),

            _("YES! Harder! I don't care who hears me!"),

            _("More! Don't you dare go easy on me!"),

        ],

        # — Orgasm —
        "girl_cum.hardcore_first": [
            _("Oh FUCK! Is this what it feels like?! I had no idea! AAAH!"),

            _("It's coming... my first... oh my god it's so INTENSE! AAAH!"),

            _("So THIS is what everyone talks about?! FUCK! AAAH!"),

        ],
        "girl_cum.hardcore_new": [
            _("Oh FUCK! Don't stop! It's coming! AAAH!"),

            _("Harder... HARDER... oh god, I'm cumming! AAAH!"),

            _("YES! Like that! Right like that! AAAH!"),

        ],
        "girl_post_cum.hardcore_first": [
            _("Holy... that was my first time and it was... that intense? I need more."),

            _("I've been missing this my entire life... I never knew I needed it this rough."),

            _("If it's always like that... I'm going to be insatiable. That was incredible."),

        ],
        "girl_post_cum.hardcore_new": [
            _("Holy... I'm shaking... and I still want more."),

            _("I think rough is my thing... I really think it is."),

            _("Give me a second... then do that again."),

        ],

        # — Cum reaction —
        "cum_inside.hardcore_first": [
            _("Oh... you just... inside me... my first time and it's... god that's intense..."),

            _("I can feel every pulse... is it always this overwhelming? Because... wow."),

            _("That hit differently than I expected... my whole body is buzzing..."),

        ],
        "cum_inside.hardcore_new": [
            _("That hit differently than I expected... my whole body is buzzing..."),

            _("Mmm... I felt that one deep... god..."),

            _("Inside me... fuck... I can feel it everywhere."),

        ],


        # ══════════════════════════════════════════════════════════
        #  CUTE — wants gentleness, first time (natural fit, less
        #  veteran phrasing, more vulnerability)
        # ══════════════════════════════════════════════════════════

        # — Moans —
        "moan.speed1.cute_new": [
            _("This feels so... new... please don't let go of me..."),

            _("Is it supposed to feel this... intimate? I can barely breathe..."),

            _("I've never felt anything like this before... please be patient with me..."),

        ],
        "moan.speed2.cute_new": [
            _("Oh... it's getting more intense... stay close to me... please..."),

            _("I can feel everything... it's overwhelming... hold me tighter..."),

            _("This is so much more than I imagined... I'm glad it's with you..."),

        ],
        "moan.speed3.cute_new": [
            _("Too fast... I can't keep up... but I don't want you to stop either..."),

            _("Everything is so intense... I've never felt so much at once..."),

            _("My body can't handle all of this... it's too much... but please don't stop..."),

        ],

        # — Orgasm —
        "girl_cum.cute_new": [
            _("Something's happening... I've never felt... is this... oh god... aaah!"),

            _("I'm... with you... for the first time I'm actually... aaah!"),

            _("I can't hold it... I've never... oh... aaah!"),

        ],
        "girl_post_cum.cute_new": [
            _("That was my first time feeling that with someone... thank you..."),

            _("I'm still shaking... I didn't know it could feel that way... with someone I trust..."),

            _("Is it always that intense? I think I need a moment... just hold me..."),

        ],


        # ══════════════════════════════════════════════════════════
        #  EAGER TRAITS — moments that had no discovery pool
        #  (the veteran pool answered her first times). "_new" lines
        #  here play on her 1st, 2nd and 3rd time: no "first", no
        #  "again". A "_first" twin exists only where it says so.
        # ══════════════════════════════════════════════════════════

        # — cum_slut: speed and pace —
        "pace_faster.cum_slut_new": [
            _("Faster... I want to feel you get there..."),

            _("Please... faster... I want it..."),

            _("Faster... don't stop until you finish..."),

        ],
        "pos_cowgirl.cum_slut_new": [
            _("Can I be on top? I want to feel you finish while I'm riding you..."),

            _("Let me ride you... I want to be the one who makes you cum."),

            _("On top? Okay... I want to feel everything from up there."),

        ],
        "pos_denied.cum_slut_new": [
            _("Okay... as long as you still finish for me."),

            _("Fine... this is good too. Just don't hold back at the end."),

            _("Alright... I just want to feel you cum. However you want."),

        ],

        # — cum_slut: her orgasm (also alone, secret masturbation) —
        "girl_cum.cum_slut_new": [
            _("Oh god... I'm cumming... and I still want more?! AAAH!"),

            _("It's too good... I can't... AAAH!"),

            _("Don't stop... please... I'm... AAAH!"),

        ],
        "girl_post_cum.cum_slut_new": [
            _("That was... I can't believe how much I needed that..."),

            _("Why am I still this hungry for more? What's happening to me?"),

            _("Mmm... I'm not done. I don't think I'll ever be done."),

        ],
        "girl_cum_hard.cum_slut_new": [
            _("WHAT IS THIS?! I'M CUMMING SO HARD! AAAAAH!"),

            _("OH GOD, IT WON'T STOP! AAAAAH!"),

            _("I CAN'T... IT'S TOO MUCH... AAAAAH!"),

        ],
        "girl_post_cum_hard.cum_slut_new": [
            _("I can't feel my legs... and I still want more... what's wrong with me?"),

            _("My whole body is still shaking... that was insane..."),

            _("I need a second... and then I need more. Badly."),

        ],
        "girl_cum_intense.cum_slut_new": [
            _("Oh god... that one went everywhere... why do I want more already?"),

            _("Mmm... that was... how is it this good?"),

        ],
        "girl_post_cum_intense.cum_slut_new": [
            _("I'm still tingling... and I'm already hungry for more. Is that normal?"),

            _("Mmm... everything feels so sensitive... I don't want it to end..."),

        ],
        "girl_orgasm_dazed.cum_slut_new": [
            _("I can't think straight... and I don't even care..."),

            _("My head is spinning... is it supposed to feel this good?"),

        ],
        "girl_orgasm_exhausted.cum_slut_new": [
            _("My body is giving out... and I still want more. How?"),

            _("I need a break... I can't believe I'm the one saying that..."),

        ],
        "girl_cum.secret_masturbate.cum_slut_new": [
            _("Thinking about him... about his... AAAH!"),

            _("Nnnh... I can't stop thinking about it... AAAH!"),

            _("Why do I keep imagining that... ahh... AAAH!"),

        ],
        "girl_post_cum.secret_masturbate.cum_slut_new": [
            _("Mmm... I can't believe what I was just thinking about..."),

            _("What's happening to me? I can't stop thinking about it..."),

            _("I need to stop thinking about that... I really do..."),

        ],

        # — cum_slut: where it landed —
        "cum_outside.cum_slut_new": [
            _("Oh... outside? I kind of wanted to feel it..."),

            _("Look at all that... part of me wanted it inside..."),

            _("Mmm... it's everywhere... I didn't think I'd like watching that so much."),

        ],
        "cum_ass.cum_slut_new": [
            _("Oh! It's all over my ass... it's so warm..."),

            _("Mmm... I can feel it running down... why do I like that?"),

            _("All over me back there... I'm kind of into this..."),

        ],
        "cum_back.cum_slut_new": [
            _("I can feel it on my back... it's so warm..."),

            _("Mmm... I wish I could see it. I kind of want to."),

            _("All over my back... I can't believe I'm smiling right now."),

        ],
        "cum_belly.cum_slut_new": [
            _("It's all over my stomach... it's so warm..."),

            _("Look at all of it... I can't stop staring."),

            _("Mmm... I didn't think I'd like watching it land on me this much."),

        ],
        "cum_condom.cum_slut_new": [
            _("I could feel it through the condom... I kind of wanted to feel it for real."),

            _("That's a lot... it feels like a waste somehow. Is that weird?"),

            _("Next time... maybe without it? I don't know. I'm just curious."),

        ],

        # — cum_slut: first creampie while she is still new (precise: CreampieCounts == 1) —
        "creampie_aftermath.first_creampie.cum_slut_new": [
            _("I can still feel it inside me... my first creampie... that was amazing..."),

            _("So that's what a creampie feels like... I need this again. Soon."),

            _("My first time feeling someone finish inside... I already want more..."),

        ],

        # — cum_slut: condom and creampie requests (sub-events) —
        "condom_force.cum_slut_new": [
            _("I can't take it anymore... I want to feel you. Really feel you."),

            _("Off. I'm sorry... I just need to feel you."),

            _("I don't know what's gotten into me... this is coming off."),

        ],
        "condom_ask.cum_slut_new": [
            _("Can we take it off? I... I want to feel you. All of you."),

            _("Please... no condom? I can't stop thinking about it."),

            _("I know it's crazy... but can we take that off?"),

        ],
        "condom_denied.cum_slut_new": [
            _("Okay... okay. But I really wanted to feel you."),

            _("Fine... you're right. I just... wanted it so bad."),

            _("Alright... I don't know what came over me."),

        ],
        "creampie_req.cum_slut_new": [
            _("Don't pull out... I want to feel it inside me."),

            _("Please finish inside... I can't stop wanting it."),

            _("Inside... please. I don't care how it sounds."),

        ],

        # — cum_slut: after the scene / ass to mouth —
        "dressup.cum_slut_new": [
            _("I don't want to get dressed yet... I can still feel it..."),

            _("Can we... do that again later? I mean it."),

            _("I still can't believe how much I liked that."),

        ],
        "atm_react.bj.cum_slut_new": [
            _("Wait... after it was in my... oh god. Why am I not stopping?"),

            _("That's so dirty... and I'm still doing it..."),

            _("I can taste where it's been... I should hate this. I don't."),

        ],

        # — anal_lover: she asks for it herself (AnalRequest). _first = no anal before this, _new = asks again —
        "anal_request.anal_lover_first": [
            _("Can I tell you something weird? I keep thinking about... trying it back there."),

            _("I've never done it... there. But I want to. Can we try?"),

            _("This is so embarrassing... but I want you to try my ass. I'm curious."),

        ],
        "anal_request.anal_lover_new": [
            _("Can we do it back there again? I can't stop thinking about it..."),

            _("I know this sounds crazy, but... I want you in my ass again."),

            _("Switch... please? I've been thinking about last time all day."),

        ],
        "anal_request_accepted.anal_lover_first": [
            _("Okay... okay. Go slow at first. I want to feel all of it."),

            _("Really? Oh god... I'm nervous and excited at the same time..."),

            _("Yes... just be gentle. I've wanted to know what this feels like for so long."),

        ],
        "anal_request_accepted.anal_lover_new": [
            _("Mmm... yes... I've been waiting for this..."),

            _("Oh god, yes... I still can't believe how much I want this..."),

            _("Thank you... I really needed that..."),

        ],
        "anal_request_declined.anal_lover_first": [
            _("Oh... okay. Maybe another time... I really want to try it, though."),

            _("That's fine... I'm not going anywhere. Neither is my curiosity."),

            _("Okay... forget I asked. Actually, don't. Think about it."),

        ],
        "anal_request_declined.anal_lover_new": [
            _("Aw... okay. But I'm asking again next time."),

            _("Fine... I'll just keep thinking about it, then."),

            _("Okay... I really wanted it, though."),

        ],

        # — anal_lover: filming it —
        "record_accepted.anal.anal_lover_new": [
            _("You want to film this? ...Okay. I kind of want to see it too."),

            _("Recording... this? God, I'm embarrassed... and I don't want you to stop."),

            _("Okay... film it. I want to remember how this feels."),

        ],

        # — Secret masturbation (she is ALONE): pose twins, so the generic discovery pools
        #   (written for sex WITH him) are never pulled up here —
        "girl_cum.secret_masturbate.hardcore_new": [
            _("Harder... why do I keep wanting it rougher... AAAH!"),

            _("It's not enough... I need... more... AAAH!"),

        ],
        "girl_cum.secret_masturbate.cute_new": [
            _("Slowly... gently... oh... something's happening... aaah!"),

            _("So warm... so soft... I'm... aaah!"),

            _("Oh... oh... I'm... I'm... aaah!"),

        ],

        # — Anal preference complaint (escalation.rpy, _anal_preference >= 2) while cum_slut is still new: her ass
        #   she knows, "where I want that load" not yet (the veteran pool claims it). Plain complaint lines —
        "vaginal_complaint.cum_slut_new": [
            _("This feels good, but you know where I really want it..."),

            _("Not bad... but you know my ass would feel even better."),

        ],

    })
