# ============================================================
# scene_lines.rpy — Comprehensive mid-scene dialogue pools
# ============================================================
#
# KEY FORMAT:  "event[.scene][.modifier]"
#
# EVENTS:      moan.speed1, moan.speed2, moan.speed3,
#              girl_cum, girl_post_cum (+ _hard / _intense), girl_orgasm_dazed,
#              girl_orgasm_exhausted, girl_nonscene_orgasm,
#              cum_inside (+ _accepted / _consented / _forced / _denied), cum_outside,
#              cum_face, cum_tits, cum_mouth (+ _accepted / _denied), cum_feet,
#              cum_ass, cum_back, cum_belly, cum_condom, creampie_aftermath(_forced),
#              condom_force, condom_ask, condom_denied, creampie_req,
#              pos_cowgirl, pos_doggy, pos_denied,
#              pace_faster, pace_slower, pace_obeyed, pace_ignored_1, pace_ignored_2,
#              record_accepted, record_denied, recording_request(_accepted / _denied),
#              anal_request(_accepted / _declined), anal_pref_curious,
#              scene_end_anal_satisfied, vaginal_complaint(_addicted), atm_react, dressup
#              ONLY these are ever requested (scene_pick_line callers): a key under any
#              other event is dead text. There is no "scene_start" / "scene_end" /
#              "speed_up" / "speed_down" event (removed 2026-09-30, the game never asked).
#
# SCENES:      hj, bj, tj, fj, cowgirl (RCG), doggy (laying down), anal (FN / laying
#              anal), full_nelson, secret_masturbate, touch, escalation
#
# MODIFIERS:   whatever _detect_line_modifiers() appends (at most TWO per key, the
#              pose always comes FIRST: event.scene.mod1.mod2). Trait modifiers use
#              the short names: "hardcore" / "cute", never "hardcore_sex" / "cute_sex".
#
# PICKER tries: event.scene.mod1.mod2 → event.scene.mod → event.scene →
#               event.mod1.mod2 → event.mod → event
# ============================================================

default _moan_cooldown = 0
default _crowd_level = 0
default _lost_virginity_this_scene = False

init python:

    SCENE_LINES = {

        # ══════════════════════════════════════════════════════════
        #  MOANS — Speed 1 (Slow / Gentle)
        # ══════════════════════════════════════════════════════════

        "moan.speed1": [  # Gemido base — velocidade lenta
            _("Mmm... yes..."),

            _("That feels nice..."),

            _("Keep going... just like that..."),

            "Mmm...",
        ],
        "moan.speed1.hj": [  # Durante handjob
            _("Feels so good..."),

            _("Mmm... You are so hard..."),

            _("You are so big..."),

        ],
        "moan.speed1.bj": [  # Durante blowjob
            "Mmph...",
            "Mmm...",
            "Mmmhm...",
        ],
        "moan.speed1.tj": [  # Durante titjob
            _("Does it feel good between them?"),

            _("Mmm... I can feel you throbbing against my skin..."),

            _("Like this...? Is this good?"),

        ],
        "moan.speed1.cowgirl": [  # Durante cowgirl
            _("Mmm... I like this pace..."),

            _("You feel good inside me..."),

            _("I can feel every inch of you..."),

            _("Mmm... nice and slow..."),

        ],
        "moan.speed1.full_nelson": [
            _("I can't move at all like this..."),

            _("You've got me completely pinned... mmm..."),

            _("This hold... I can feel everything..."),

            _("I'm so exposed like this..."),

        ],
        "moan.speed1.anal": [  # Durante anal
            _("It's... so tight... go slow..."),

            _("Mmm... I can feel every inch back there..."),

            _("Oh... that's... different..."),

            _("Easy... easy... let me adjust..."),

        ],
        "moan.speed1.masturbate": [  # Durante masturbacao
            _("Mmm... this feels nice..."),

            _("Are you watching me...?"),

            _("I like knowing you're looking..."),

        ],

        "moan.speed1.oral": [
            _("Mmm... your mouth feels so good..."),

            _("Oh... right there... don't stop..."),

            _("I can feel your tongue... oh god..."),

            _("That's... so intimate... keep going..."),

        ],

        # — Speed 1 modifiers —
        "moan.speed1.first_time": [  # Primeira vez
            _("I... I didn't know it would feel like this..."),

            _("Is this okay? Am I doing it right?"),

            _("Oh... oh wow..."),

            _("It's... different than I imagined..."),

        ],
        "moan.speed1.act_first": [  # Primeira vez neste ato com player (BF pode ter feito)
            _("It feels different with you... in a good way."),

            _("I haven't done this with you before... I'm a bit nervous."),

            _("This is new... between us, I mean. Go easy."),

        ],
        "moan.speed1.inexperienced": [  # Inexperiente (primeira vez + BF nunca fez)
            _("Am I... am I doing this right? Tell me..."),

            _("I don't really know what to do... is this okay?"),

            _("Sorry if I'm bad at this... it's all new to me..."),

            _("You'll tell me if I'm doing something wrong, right...?"),

        ],
        "moan.speed1.hj.inexperienced": [  # HJ inexperiente
            _("Is this the right speed? I've never done this..."),

            _("My grip... is it too tight? Too loose?"),

            _("Tell me how you like it... I have no idea..."),

        ],
        "moan.speed1.bj.inexperienced": [  # BJ inexperiente
            _("Am I using my tongue right...? I don't know what to do..."),

            _("Tell me if I'm doing it wrong... this is my first time..."),

            _("I'm trying not to use my teeth... is it okay?"),

        ],
        "moan.speed1.tj.inexperienced": [  # TJ inexperiente
            _("Am I pressing hard enough? I've never done this..."),

            _("Is this how it works...? Tell me what to do..."),

            _("I'm not sure how to move... guide me?"),

        ],
        "moan.speed1.cowgirl.inexperienced": [  # Cowgirl inexperiente
            _("Am I moving right...? This is so new..."),

            _("I don't know the right rhythm... help me..."),

            _("Is this good? I've never been on top before..."),

        ],
        "moan.speed1.anal.inexperienced": [  # Anal inexperiente
            _("Is it... supposed to feel like this...? I've never..."),

            _("I don't know if I'm doing this right... it's so tight..."),

            _("It's so much pressure... is this normal...?"),

        ],
        "moan.speed2.anal.inexperienced": [  # Anal speed2 inexperiente
            _("Oh... oh it's starting to feel... good? I think?"),

            _("I'm getting used to it... don't speed up yet..."),

            _("It's weird but... I don't want you to stop..."),

        ],
        "moan.speed3.anal.hardcore": [  # Anal speed3 hardcore
            _("DESTROY MY ASS! HARDER! FUCK!"),

            _("IS THAT ALL YOU'VE GOT?! WRECK ME!"),

            _("POUND IT! I WANT TO FEEL IT TOMORROW!"),

            _("FUCK MY ASS LIKE YOU MEAN IT! COME ON!"),

            _("DEEPER! I SAID DEEPER! I CAN... AAAH!"),

            _("YES! THAT'S... FUCK! RIGHT THERE! DON'T YOU DARE STOP!"),

        ],
        "moan.speed2.anal.boyfriend": [  # Anal speed2 com namorado
            _("My boyfriend would never... mmm... do this to me..."),

            _("He doesn't know I like it... back there... aah..."),

            _("This is something only you get to do to me..."),

        ],
        "moan.speed2.anal.girlfriend": [  # Anal speed2 com namorada
            _("My girlfriend would never... mmm... do this to me..."),

            _("She doesn't know I like it... back there... with a man... aah..."),

            _("A cock back there... something she could never give me..."),

        ],
        "moan.speed1.cum_slut": [  # Garota adora cum
            _("Mmm... give me more..."),

            _("I need it deeper..."),

            _("Don't tease me... I want all of it..."),

        ],
        "moan.speed1.boyfriend": [  # Garota tem namorado
            _("We shouldn't... but it feels so good..."),

            _("If he knew what I was doing right now..."),

            _("This is wrong... but I don't want to stop..."),

            _("This is gentler than anything he's ever done... and it already feels better."),

            _("He thinks he's enough for me... if only he could see me right now."),

            _("My boyfriend's touch never made my skin tingle like this..."),

        ],
        "moan.speed1.girlfriend": [  # Garota tem namorada
            _("We shouldn't... but your touch feels so different..."),

            _("If she knew I was with a guy right now..."),

            _("This wasn't supposed to happen... but I don't want to stop..."),

            _("She's so gentle with me... but this is something completely different..."),

            _("She thinks she's everything I need... if only she could see me right now."),

            _("My girlfriend's touch never made my skin tingle like this... not like yours..."),

            _("She'd be so upset if she knew..."),

            _("I keep thinking about her while you're doing this..."),

            _("My girlfriend trusts me... and here I am..."),

        ],
        "moan.speed1.public": [  # Local publico
            _("Shh... someone might hear us..."),

            _("Keep quiet... we can't get caught..."),

            _("Not so loud... people are nearby..."),

        ],
        "moan.speed1.cute": [  # Sexo gentil/carinhoso
            _("This feels so intimate..."),

            _("Hold me closer..."),

            _("You're so gentle... I love it..."),

        ],
        "moan.speed1.hardcore": [  # Sexo intenso/pesado
            _("Is that all you've got...?"),

            _("Come on... I can take more than this..."),

            _("You're being too gentle..."),

        ],

        "moan.speed1.nerd": [
            _("Mm... I can't focus on anything else..."),

            _("Oh... my body is really... responding to this..."),

            _("This is... way more intense than I expected..."),

            _("I didn't expect it to feel... this good..."),

        ],

        # ══════════════════════════════════════════════════════════
        #  MOANS — Speed 2 (Medium)
        # ══════════════════════════════════════════════════════════

        "moan.speed2": [  # Gemido base — velocidade media
            _("Yes... just like that..."),

            _("Oh god... that's good..."),

            _("More... don't stop..."),

            _("Aah... yes..."),

        ],
        "moan.speed2.hj": [  # Durante handjob
            _("Mmm... this is perfect..."),

            _("I wanna feel you cumming..."),

            _("I love feeling it throb in my hand..."),

        ],
        "moan.speed2.bj": [  # Durante blowjob
            _("Mmph... mmm..."),

            _("Glk... mmm..."),

            "Mmm...",
        ],
        "moan.speed2.tj": [  # Durante titjob
            _("God, you're so hard between them..."),

            _("I love the way you throb against my chest..."),

            _("You're leaking so much... am I that good?"),

        ],
        "moan.speed2.cowgirl": [  # Durante cowgirl
            _("I love controlling the pace..."),

            _("You're hitting the perfect spot..."),

            _("Mmm... I could ride you all day..."),

            _("Right there... don't move..."),

        ],
        "moan.speed2.full_nelson": [
            _("I can't fight this hold... aah..."),

            _("You're so deep... and I can't move an inch..."),

            _("Pinned and helpless... oh god..."),

            _("Every thrust hits harder when I can't brace myself..."),

        ],
        "moan.speed2.full_nelson.hardcore": [
            _("Hold me tighter... don't let me go..."),

            _("I can't move and I don't want to... wreck me..."),

        ],
        "moan.speed2.full_nelson.submissive": [
            _("I love being trapped like this... use me harder..."),

            _("Keep me pinned like this... I'm yours to use..."),

            _("Hold me like this and take what you want... I won't fight it..."),

        ],
        "moan.speed2.full_nelson.cute": [
            _("You're holding me so tight... I feel so small..."),

            _("I can't move at all... please be gentle..."),

            _("This is so overwhelming... I can feel everything..."),

        ],
        "moan.speed2.anal": [  # Durante anal
            _("Oh fuck... it's filling me up..."),

            _("God... I can feel you so deep in there..."),

            _("It's so intense... don't stop..."),

            _("Aah... I never thought it'd feel this good..."),

        ],
        "moan.speed2.masturbate": [  # Durante masturbacao
            _("Aah... it's getting really good..."),

            _("Don't look away... I want you to see..."),

            _("Oh god... I'm so wet right now..."),

            _("Mmm... I can't slow down..."),

        ],

        "moan.speed2.oral": [
            _("Aah... you're so good at this..."),

            _("Oh god... your tongue... right THERE..."),

            _("I can't... I can't think straight..."),

            _("Don't stop... please don't stop..."),

        ],

        # — Speed 2 modifiers —
        "moan.speed2.first_time": [  # Primeira vez
            _("Oh god... I never expected this..."),

            _("It's so much more intense than I imagined..."),

            _("Aah... I think I'm getting addicted..."),

        ],
        "moan.speed2.inexperienced": [  # Inexperiente (primeira vez + BF nunca fez)
            _("I'm still figuring this out... but it feels good, right?"),

            _("Is this pace okay? I really don't know what I'm doing..."),

            _("Tell me I'm not terrible at this... please..."),

        ],
        "moan.speed2.hj.inexperienced": [  # HJ inexperiente
            _("Faster? Slower? I can't tell... help me..."),

            _("My hand is getting tired but I don't want to stop... is this right?"),

            _("You're throbbing... that means it's good, right?"),

        ],
        "moan.speed2.bj.inexperienced": [  # BJ inexperiente
            _("Mmm... am I taking enough in? I'm trying my best..."),

            _("I keep gagging... sorry... I'll get better at this..."),

            _("Is the suction okay? I don't know what feels good..."),

        ],
        "moan.speed2.tj.inexperienced": [  # TJ inexperiente
            _("Am I squeezing them together enough...?"),

            _("I can feel you throbbing between them... that's good, right?"),

            _("Tell me if I should change something... I'm learning..."),

        ],
        "moan.speed2.cowgirl.inexperienced": [  # Cowgirl inexperiente
            _("My legs are burning but I don't want to stop... is this right?"),

            _("Am I going too fast? Too slow? I can't tell..."),

            _("I think I'm getting the hang of it... am I?"),

        ],
        "moan.speed2.cum_slut": [  # Garota adora cum
            _("Fuck yes... harder..."),

            _("Give me everything..."),

            _("God I've been craving this..."),

        ],
        "moan.speed2.boyfriend": [  # Garota tem namorado
            _("He could never make me feel like this..."),

            _("I'm such a bad girlfriend... but I can't stop myself..."),

            _("You're better than him... don't stop..."),

        ],
        "moan.speed2.girlfriend": [  # Garota tem namorada
            _("She could never make me feel like this... not with a cock..."),

            _("I'm supposed to be hers... but I can't stop wanting this..."),

            _("A man shouldn't feel this good... don't stop..."),

            _("She would never believe I'm doing this with a guy..."),

            _("If she finds out... oh god... don't stop..."),

            _("I'm such a terrible girlfriend..."),

        ],
        "moan.speed2.public": [  # Local publico
            _("Oh god... not so deep... I'll moan too loud..."),

            _("Someone's going to hear... but I can't stop..."),

            _("Shh shh shh... oh god..."),

        ],
        "moan.speed2.cute": [  # Sexo gentil/carinhoso
            _("You feel amazing inside me..."),

            _("I feel so connected to you..."),

            _("This is perfect... just stay close..."),

        ],
        "moan.speed2.hardcore": [  # Sexo intenso/pesado
            _("That's more like it..."),

            _("Harder... I know you can do better..."),

            _("Come on... make me feel it..."),

        ],
        "moan.speed2.submissive": [
            _("Turn me into one of your mindless sluts..."),

            _("Use me however you want... I'm all yours..."),

            _("Tell me what you want... I'll do anything you say..."),

        ],

        "moan.speed2.nerd": [
            _("I can't... think straight anymore...!"),

            _("My whole body is... tingling...!"),

            _("I'm... I'm losing control of my voice...!"),

            _("It's too much... my head is spinning...!"),

        ],

        # ══════════════════════════════════════════════════════════
        #  MOANS — Speed 3 (Fast / Intense)
        # ══════════════════════════════════════════════════════════

        "moan.speed3": [  # Gemido base — velocidade rapida
            _("YES! Right there! Don't stop!"),

            _("Oh fuck... oh fuck..."),

            "HARDER!",
            _("Don't stop! Please!"),

            _("I... I can't... OH GOD!"),

            _("YES YES YES! RIGHT THERE!"),

            _("FUCK! I'm gonna... I... AAAH!"),

            _("My head is... I can't think... AAAH!"),

        ],
        "moan.speed3.hj": [  # Durante handjob
            _("Faster! I want to see you cum!"),

            _("God, it's twitching so much..."),

            _("You're so close... I can feel it..."),

            _("Come on come on come on... CUM!"),

            _("It's SO hard... it's throbbing in my hand...!"),

        ],
        "moan.speed3.bj": [  # Durante blowjob
            _("Glk... mmph..."),

            _("Mmm... MMPH!"),

            "Mmm...",
            _("Glk... glk... MMPH...!"),

            _("Mmmph... hmmm... glk..."),

        ],
        "moan.speed3.tj": [  # Durante titjob
            _("Fuck... your cock feels amazing between them..."),

            _("Cum for me... all over my tits..."),

            _("I can barely contain you..."),

            _("It keeps poking out... it's so big between my... AAAH!"),

            _("You're throbbing SO much... I can feel every pulse...!"),

        ],
        "moan.speed3.cowgirl": [  # Durante cowgirl
            _("FUCK! You're so deep!"),

            _("I'm going to ride you until you break!"),

            _("Yes yes yes... right THERE!"),

            _("I can't stop... it feels too good!"),

            _("I CAN'T SLOW DOWN! MY HIPS WON'T... AAAH!"),

            _("YOU'RE HITTING MY... I... OH FUCK!"),

        ],
        "moan.speed3.full_nelson": [
            _("I CAN'T MOVE! I CAN'T DO ANYTHING! AAAH!"),

            _("YOU'RE HOLDING ME SO TIGHT... I... AAAH!"),

            _("PINNED... HELPLESS... OH GOD DON'T STOP!"),

            _("I CAN'T FIGHT THIS! MY BODY... IS GIVING IN...!"),

            _("EVERYTHING IS HITTING SO DEEP LIKE THIS! AAAH!"),

        ],
        "moan.speed3.anal": [  # Durante anal
            _("FUCK! MY ASS! IT'S TOO MUCH!"),

            _("OH GOD! You're DESTROYING me back there!"),

            _("I can't... I CAN'T think... it's SO deep!"),

            _("HARDER! DON'T STOP! FUCK MY ASS!"),

            _("MY LEGS ARE... I CAN'T EVEN... AAAH!"),

            _("IT'S SO DEEP IN MY... I... I CAN'T...!"),

        ],
        "moan.speed3.masturbate": [  # Durante masturbacao
            _("Oh god oh god oh god...!"),

            _("I'm so close... don't stop watching me!"),

            _("Aah! I can't hold back anymore!"),

            _("YES... right there... I'm almost...!"),

        ],

        "moan.speed3.oral": [
            _("OH GOD... I'm so close... don't you DARE stop!"),

            _("YES YES YES... right there... I'm about to...!"),

            _("Your tongue is going to make me... aah...!"),

            _("I can't hold it anymore... I'm cumming...!"),

        ],

        # — Speed 3 modifiers —
        "moan.speed3.first_time": [  # Primeira vez
            _("Oh my GOD... I had no idea... aaah!"),

            _("This is... this is too much... but don't stop!"),

            _("I'm going crazy... I can't think straight..."),

        ],
        "moan.speed3.inexperienced": [  # Inexperiente (primeira vez + BF nunca fez) — prazer > insegurança
            _("I can't believe this is my first time... it feels AMAZING!"),

            _("How am I doing?! I don't care... just don't stop!"),

            _("I never knew it could feel like THIS! Aaah!"),

        ],
        "moan.speed3.cum_slut": [  # Garota adora cum
            _("Destroy me! Don't hold back!"),

            _("Use me! I'm your dirty little slut!"),

            _("FUCK! Give me EVERYTHING!"),

            _("HARDER! HARDER! I WANT TO FEEL IT FOR DAYS!"),

            _("YES! USE ME! I'M... I'M YOURS! AAAH!"),

            _("WRECK ME! I DON'T CARE! JUST DON'T STOP!"),

        ],
        "moan.speed3.boyfriend": [  # Garota tem namorado
            _("He could NEVER... oh GOD..."),

            _("I'm his girlfriend but I'm YOURS right now..."),

            _("Fuck... I'll never forget this..."),

            _("He could NEVER keep up with this pace... oh FUCK!"),

            _("I'm screaming for another man and it's the best I've EVER felt!"),

            _("My boyfriend in a MILLION years could never... AAAH!"),

            _("Everything he's ever done feels like NOTHING compared to this!"),

            _("HIS GIRLFRIEND IS... I'M... I CAN'T EVEN THINK ABOUT HIM RIGHT NOW!"),

            _("IF HE COULD SEE ME NOW... OH FUCK... HE'D... I DON'T CARE! AAAH!"),

            _("I'M GONNA... I... HE NEVER MADE ME FEEL LIKE... AAAH!"),

        ],
        "moan.speed3.girlfriend": [  # Garota tem namorada
            _("She could NEVER give me this... oh GOD..."),

            _("I'm her girlfriend but I'm YOURS right now..."),

            _("Fuck... no woman could ever do this to me..."),

            _("She could NEVER give me a cock like this... oh FUCK!"),

            _("I'm screaming for YOU and it's the best I've EVER felt!"),

            _("My girlfriend in a MILLION years could never... she doesn't have THIS... AAAH!"),

            _("Everything she's ever done feels like NOTHING compared to a real cock!"),

            _("She could never make me feel like THIS..."),

            _("Forget her... just fuck me... I don't care anymore..."),

            _("I'll deal with the guilt later... just don't stop..."),

            _("NO TOY... NO FINGERS... NOTHING SHE HAS COULD... AAAH!"),

            _("I'M HER GIRLFRIEND AND I'M... I'M SCREAMING FOR A... AAAH!"),

            _("A COCK IS... IT'S SO MUCH... I CAN'T GO BACK TO... AAAH!"),

        ],
        "moan.speed3.public": [  # Local publico
            "MMMMPH!",
            _("If anyone sees... I don't even care anymore..."),

            _("Oh god oh god... someone's going to come..."),

            _("I can't keep quiet... I... MMPH!"),

            _("SOMEONE WILL... I DON'T... I CAN'T STOP...!"),

        ],
        "moan.speed3.cute": [  # Sexo gentil/carinhoso
            _("I love you I love you I love you!"),

            _("You make me feel things I never... aaah!"),

            _("Hold me... hold me while you... aaah!"),

            _("I'M YOURS! I'M... I LOVE... AAAH!"),

            _("PLEASE DON'T LET GO OF ME... I'M... AAAH!"),

            _("I CAN FEEL EVERYTHING... YOUR HEART... YOUR... AAAH!"),

        ],
        "moan.speed3.hardcore": [  # Sexo intenso/pesado
            _("THAT'S what I'm talking about!"),

            _("YES! Break me! Don't you DARE slow down!"),

            _("Fucking FINALLY! Give me ALL of it!"),

            _("IS THAT ALL YOU GOT?! HARDER! AAAH!"),

            _("WRECK ME! I CAN TAKE IT! COME ON!"),

            _("FUCK YES! THAT'S... THAT'S WHAT I... AAAH!"),

        ],
        "moan.speed3.nerd": [
            _("Oh god, oh god, oh GOD...!"),

            _("I've never felt... THIS much...!"),

            _("My legs are... I can't hold them still...!"),

            _("Everything is... going white... I can't see...!"),

        ],

        # ══════════════════════════════════════════════════════════
        #  GIRL CUM (Orgasm)
        # ══════════════════════════════════════════════════════════

        "girl_cum": [  # Orgasmo base da garota
            _("I'm cumming! I'm cumming! Aaah!"),

            _("Oh god oh god oh GOD!"),

            _("YES! Don't stop, I'm... AAAH!"),

            _("I'm... I'm...! AAAAAAH!"),

        ],
        "girl_cum.hj": [  # Durante handjob
            _("Oh god... you're making me cum just from this..."),

            _("Aaah... my legs... they won't stop shaking..."),

            _("I... I can't believe... just your hand..."),

        ],
        "girl_cum.bj": [  # Durante blowjob
            "MMPH...!",
            _("Mmm... aaah...!"),

            _("Haa... haa... oh my god..."),

        ],
        "girl_cum.tj": [  # Durante titjob
            _("Oh... I'm... just from having you between them..."),

            _("I can't believe I'm cumming from this..."),

            _("Your cock between my tits... it's making me... AAAH!"),

        ],
        "girl_cum.cowgirl": [  # Durante cowgirl
            _("I'm cumming on your cock! AAAH!"),

            _("Yes yes YES! Right THERE!"),

            _("I can feel you so deep... I'm... AAAH!"),

            _("Don't move! I'm... I'M...!"),

        ],
        "girl_cum.oral": [  # Orgasmo durante oral (eating her out)
            _("Your tongue... right there... I'm... AAAH!"),

            _("Oh god... don't stop... your mouth is... AAAH!"),

            _("I'm cumming! Your tongue... it's too much!"),

            _("Right there right there RIGHT THERE! AAAH!"),

        ],
        "girl_cum.oral.girlfriend": [  # Oral + tem namorada
            _("She never... her tongue never made me feel like THIS!"),

            _("Oh god... you're better at this than she is... AAAH!"),

            _("A guy... a guy is making me cum with his mouth... she'd die if she knew..."),

            _("You're doing what she always tried to do... except you're ACTUALLY making me... AAAH!"),

        ],
        "girl_cum.oral.boyfriend": [  # Oral + tem namorado
            _("He never... he never did THIS to me... AAAH!"),

            _("Oh god... your tongue is... he's never made me feel like this!"),

            _("You're so much better at this than him... I'm... AAAH!"),

        ],
        "girl_cum.anal": [  # Orgasmo durante anal (default: surpresa)
            _("Wait... I'm... from THERE?! AAAH!"),

            _("No way... I'm actually... from my ass?! OH GOD!"),

            _("How is this... I didn't think I could... AAAH!"),

            _("I can't... this isn't supposed to... I'M CUMMING! AAAH!"),

        ],
        "girl_cum.anal.hardcore": [  # Hardcore gosta do conceito
            _("YES! Fuck my ass harder! I'm CUMMING! AAAH!"),

            _("OH GOD! My ass is making me cum! This is incredible! AAAH!"),

            _("I'm cumming from my ass and I LOVE it! AAAH!"),

            _("Don't stop! My ass is... I'M CUMMING! FUUUCK!"),

        ],
        "girl_cum.anal.cute": [  # Cute/gentle: envergonhada
            _("N-No... not from there... this is so humiliating... AAAH!"),

            _("I can't believe... from my butt?! Oh god... AAAH!"),

            _("Please don't look at me... I'm... from back there... AAAH!"),

            _("This is so wrong... but I can't stop it... I'm... AAAH!"),

        ],
        "girl_cum.anal.boyfriend": [  # Namorado: culpa pesada
            _("Oh god... I'm cumming from another man's cock in my ass... AAAH!"),

            _("He never... I never even let him touch me there... and now I'm cumming from THIS?! AAAH!"),

            _("What is wrong with me... his cock in my ass is making me... AAAH!"),

            _("My {hint}boyfriend{/hint} would die if he knew I just came from anal... AAAH!"),

        ],
        "girl_cum.anal.girlfriend": [  # Namorada: conflito de sexualidade
            _("Oh god... you're making me cum from my ass... she never even... AAAH!"),

            _("She never... no woman could do THIS to me... and now a cock is making me cum from back there?! AAAH!"),

            _("What is wrong with me... your cock in my ass is doing what she never could... AAAH!"),

            _("My {hint}girlfriend{/hint} would die if she knew a man just made me cum from anal... AAAH!"),

        ],
        "girl_cum.anal.hate_cum": [  # CuH durante anal -- sem preocupacao com creampie
            _("I'm cumming! Fuck! Your cock in my ass is making me cum!"),

            _("I'M CUMMING FROM MY ASS! JUST... DON'T YOU DARE ENJOY THIS! AAAH!"),

            _("OH GOD! I'M... I can't believe my ass is making me... AAAH!"),

        ],
        "girl_cum.anal.hate_cum.hardcore": [  # CuH + HC durante anal
            _("I'M CUMMING! Fuck! Your cock in my ass is making me cum! Don't you dare stop!"),

            _("OH GOD MY ASS! I HATE that I love this! AAAH!"),

            _("I'm cumming from anal! I hate your cock! DON'T STOP! AAAH!"),

        ],
        "girl_cum.anal.loyal": [  # Loyal girl cumming from anal -- guilt/conflict
            _("I'm cumming... from this... I'm supposed to be loyal and this is making me... AAAH!"),

            _("Oh god, I'm... this isn't what loyal girlfriends do... but I can't stop! AAAH!"),

        ],
        "girl_cum.anal.cum_slut": [  # Cum slut enthusiastic about anal orgasm
            _("YES! Cumming from my ass! Fill me up, don't stop! AAAH!"),

            _("I'm cumming so hard from anal! God I love having you in my ass! AAAH!"),

        ],
        "girl_cum.nerd": [
            _("I'm... something's building, I can't... AAAH!"),

            _("My whole body is... tensing up... I'm... AAAH!"),

            _("I can't hold it, I'm... I'm cumming... AAAH!"),

            _("Everything is... pulsing... I can't stop... AAAH!"),

        ],
        "girl_cum.secret_masturbate": [  # Orgasmo enquanto player observa em segredo
            _("Mmm... mmm... AAAH!"),

            _("Oh... oh god... yes... YES!"),

            _("I can't... I'm so close... AAAH!"),

            _("Nnnh... right there... don't stop... AAAH!"),

        ],
        "girl_cum.secret_masturbate.cum_slut": [
            _("Nnnh... thinking about his cum... inside me... AAAH!"),

            _("I want it so badly... fill me... AAAH!"),

            _("Imagining his taste... his load... AAAH! YES!"),

        ],
        "girl_cum.secret_masturbate.hate_cum": [
            _("Mmm... at least alone I don't have to worry about... his mess... AAAH!"),

            _("Just me... no disgusting fluids... just pleasure... AAAH!"),

            _("This is better... no cleanup... just... AAAH!"),

        ],
        "girl_cum.secret_masturbate.hardcore": [
            _("FUCK... harder... I need it harder... AAAH!"),

            _("Not enough... I need someone to really... AAAH!"),

            _("My fingers aren't enough... I need to be... AAAH!"),

        ],
        "girl_cum.secret_masturbate.cute": [
            _("Mmm... slowly... gently... ah... AH!"),

            _("So warm... so nice... I'm... I'm floating... AAAH!"),

            _("Gentle... gentle... oh... oh it's happening... AAAH!"),

        ],
        "girl_cum.secret_masturbate.boyfriend": [
            _("Mmm... thinking about... not him... someone else... AAAH!"),

            _("I shouldn't be thinking about another man while I... AAAH!"),

            _("If my boyfriend knew who I'm imagining right now... AAAH!"),

        ],
        "girl_cum.secret_masturbate.girlfriend": [
            _("Mmm... thinking about... not her... a man... AAAH!"),

            _("I shouldn't be thinking about a guy while I... she'd be devastated... AAAH!"),

            _("If my girlfriend knew I'm imagining a cock right now... AAAH!"),

        ],
        "girl_post_cum.secret_masturbate": [  # Pos-orgasmo observacao secreta
            _("Hah... hah... that was... I needed that."),

            _("Mmm... okay... I feel better now..."),

            _("Phew... I hope nobody heard me..."),

            _("That was intense... I should do this more often..."),

        ],
        "girl_post_cum.secret_masturbate.cum_slut": [
            _("Mmm... but I really wish someone was here to finish inside me..."),

            _("That was good... but it's never as good as the real thing..."),

            _("I need more than my fingers... I need him filling me up..."),

        ],
        "girl_post_cum.secret_masturbate.hate_cum": [
            _("At least this way I don't have to deal with anyone's gross... ugh."),

            _("Clean, private, no mess. This is perfect. Why do I even bother with guys?"),

            _("Just me. No disgusting fluids. Exactly how I like it."),

        ],
        "girl_post_cum.secret_masturbate.boyfriend": [
            _("I was thinking about... him. Not my boyfriend. What is wrong with me?"),

            _("My boyfriend would be devastated if he knew who I just fantasized about..."),

            _("I keep touching myself thinking about another man... I'm terrible."),

        ],
        "girl_post_cum.secret_masturbate.girlfriend": [
            _("I was thinking about... him. Not my girlfriend. A man. What is wrong with me?"),

            _("My girlfriend would be devastated if she knew I just fantasized about a guy..."),

            _("I keep touching myself thinking about a man... about his cock... I'm terrible."),

        ],
        # ── Interactive masturbation (player present, no penetration) ──
        "girl_cum.masturbate": [
            _("Oh god... I'm... just from my own hands... AAAH!"),

            _("I'm cumming... I'm cumming...! AAAH!"),

            _("Yes... yes... YES! Oh god...!"),

            _("I can't stop... my fingers... AAAH!"),

        ],
        "girl_cum.masturbate.boyfriend": [
            _("I'm cumming... thinking about... not him... AAAH!"),

            _("My {hint}boyfriend{/hint} has never seen me like this... touching myself for someone else... AAAH!"),

            _("Oh god... if he knew what I'm doing right now... AAAH!"),

            _("I shouldn't be doing this... but it feels so... AAAH!"),

        ],
        "girl_cum.masturbate.girlfriend": [
            _("I'm cumming... thinking about a man... not her... AAAH!"),

            _("My {hint}girlfriend{/hint} has never seen me like this... touching myself for a guy... AAAH!"),

            _("Oh god... if she knew I'm cumming while thinking about a cock... AAAH!"),

            _("I'm supposed to only want women... but this feels so... AAAH!"),

        ],
        "girl_cum.masturbate.loyal": [
            _("I can't believe I'm doing this in front of you... AAAH!"),

            _("This is so wrong... but I can't stop... AAAH!"),

            _("Oh god... the way you're watching me... AAAH!"),

        ],
        "girl_cum.masturbate.cum_slut": [
            _("I wish it was more than my fingers... I need... AAAH!"),

            _("Cumming from my own hand but craving so much more... AAAH!"),

            _("My fingers aren't enough... I want the real thing... AAAH!"),

        ],
        "girl_cum.masturbate.hate_cum": [
            _("At least this way there's no mess... AAAH!"),

            _("Just me... no gross cleanup after... AAAH!"),

            _("Oh god... yes... and nobody's making a mess of me... AAAH!"),

        ],
        "girl_cum.masturbate.camera_hater": [
            _("I'm cumming... don't you dare tell anyone you saw this... AAAH!"),

            _("Oh GOD... nobody can ever know about this... AAAH!"),

            _("If anyone finds out you watched me do this... AAAH!"),

        ],
        "girl_cum.masturbate.hardcore": [
            _("FUCK... my fingers aren't rough enough... AAAH!"),

            _("I need it harder than this... but I'm... AAAH!"),

            _("Nngh... I'm cumming but I need something bigger... AAAH!"),

        ],
        "girl_cum.masturbate.cute": [
            _("Mmm... so warm... so gentle... I'm... ah... AAAH!"),

            _("It feels so nice... just me... slowly... AAAH!"),

            _("Gently... gently... oh... I'm floating... AAAH!"),

        ],

        # ── Interactive masturbation post-cum ──
        "girl_post_cum.masturbate": [
            _("Oh wow... that was... intense..."),

            _("I can't believe I just did that in front of you..."),

            _("Hah... hah... my legs are shaking..."),

            _("That was... I needed that..."),

        ],
        "girl_post_cum.masturbate.boyfriend": [
            _("I just touched myself in front of another man... what is wrong with me..."),

            _("My {hint}boyfriend{/hint} has never watched me do that... and now you have..."),

            _("If he ever finds out I did this for you..."),

        ],
        "girl_post_cum.masturbate.girlfriend": [
            _("I just touched myself in front of a man... while I have a girlfriend... what is wrong with me..."),

            _("My {hint}girlfriend{/hint} has never made me cum like that... and all I did was think about you..."),

            _("If she ever finds out I did this for a guy..."),

        ],
        "girl_post_cum.masturbate.loyal": [
            _("I can't believe you just watched me do that..."),

            _("That was so private... I've never shown anyone that side of me..."),

            _("I feel so exposed... but it felt incredible..."),

        ],
        "girl_post_cum.masturbate.cum_slut": [
            _("That was good... but I want the real thing next time..."),

            _("My fingers aren't enough anymore... I need you..."),

            _("Mmm... next time, I don't want to use my hands..."),

        ],
        "girl_post_cum.masturbate.hate_cum": [
            _("At least doing it myself means no mess to deal with after..."),

            _("Clean, easy, and I still came hard. Perfect."),

            _("That was great... and I don't have to clean anyone's gross stuff off me."),

        ],
        "girl_post_cum.masturbate.camera_hater": [
            _("That was amazing... but you better not tell a soul you saw that."),

            _("Nobody. Ever. Finds out about this. Promise me."),

            _("I can't believe I let you watch... this stays between us. Forever."),

        ],

        "girl_cum.first_time": [  # Primeira vez
            _("What's... what's happening to me... AAAH!"),

            _("I've never... oh my GOD... is this what it feels like?!"),

            _("I can't... I can't control it... AAAH!"),

        ],
        "girl_cum.cum_slut": [  # Garota adora cum
            _("FUCK! This is the best orgasm of my life!"),

            _("I'm cumming so hard... don't you dare stop!"),

            _("YES YES YES! MORE!"),

        ],
        "girl_cum.boyfriend": [  # Garota tem namorado
            _("Oh god... I never came like this with him... AAAH!"),

            _("You're better... you're so much better..."),

            _("I'm cumming for you... not him... YOU!"),

            _("He's NEVER made me cum like this! NEVER! AAAH!"),

            _("I've faked it with him so many times... THIS is real! AAAH!"),

            _("You just gave me what he's been failing to give me for MONTHS!"),

        ],
        "girl_cum.girlfriend": [  # Garota tem namorada
            _("Oh god... she never made me cum like this... you're... AAAH!"),

            _("You're better... a cock is so much better than anything she's ever done..."),

            _("I'm cumming for a man... not her... for YOU!"),

            _("She's NEVER made me cum like this! A man is doing what she NEVER could! AAAH!"),

            _("I've faked it with her so many times... THIS is what a real orgasm feels like! AAAH!"),

            _("You just gave me what she's been failing to give me... and all it took was a cock!"),

        ],
        "girl_cum.public": [  # Local publico
            "MMMMPH!",
            _("Oh g... mmph!"),

            "...",
        ],
        "girl_cum.cute": [  # Sexo gentil/carinhoso
            _("I love you... I love you so much... AAAH!"),

            _("Hold me... I'm... I'm cumming for you..."),

            _("You make me feel so... so... AAAH!"),

        ],
        "girl_cum.hardcore": [  # Sexo intenso/pesado
            _("FUCK YES! MAKE ME CUM!"),

            _("Don't stop! HARDER! I'm RIGHT THERE!"),

            _("That's it! THAT'S FUCKING IT!"),

        ],
        "girl_cum.recurring": [  # Recorrente / ja fez antes
            _("You always make me cum so hard..."),

            _("Every time with you it gets better..."),

            _("I'm cumming AGAIN... you're amazing..."),

        ],
        "girl_cum.camera_hater": [
            _("I'M CUMMING! DON'T YOU DARE FILM THIS! AAAH!"),

            _("OH GOD! If anyone sees me like this I'll... AAAH!"),

            _("I'm cumming! And if you recorded any of this I swear...!"),

        ],
        "girl_cum.camera_lover": [
            _("I'M CUMMING! GET THIS ON CAMERA! AAAH!"),

            _("OH GOD! Tell me you're recording! I'm... AAAH!"),

            _("I'm cumming! Tell me you're getting this on camera!"),

        ],
        "girl_cum.hate_cum": [
            _("I'M CUMMING! JUST... DON'T YOU FINISH YET! AAAH!"),

            _("OH GOD! I'M... JUST REMEMBER TO PULL OUT! AAAH!"),

            _("I'm cumming! Oh Fuck! Your cock is making me cum!"),

        ],
        "girl_cum.loyal": [
            _("I'M CUMMING! THIS IS INSANE! MY BODY IS ON FIRE! AAAH!"),

            _("OH GOD! I've gone crazy! I can't control myself! AAAH!"),

            _("I'm cumming! Only for you... always for you...!"),

        ],

        # ══════════════════════════════════════════════════════════
        #  REPEATED ORGASM — 2nd and 3rd+ cum in same session
        # ══════════════════════════════════════════════════════════

        "girl_cum.orgasm_2nd": [
            _("Again?! I'm... I'm cumming AGAIN! AAAH!"),

            _("Already?! Oh god, not again... AAAH!"),

            _("I just came and I'm already... AAAH!"),

            _("How... how am I cumming again so fast?!"),

        ],
        "girl_cum.orgasm_3rd_plus": [
            _("I've lost count... I can't stop cumming... AAAH!"),

            _("How many times is that now?! My body won't stop! AAAH!"),

            _("Again... and again... I can't... my body keeps... AAAH!"),

            _("I don't even know what's happening anymore... AAAH!"),

        ],
        "girl_cum.orgasm_2nd.cum_slut": [
            _("YES! Again! Give me MORE! AAAH!"),

            _("I knew you'd make me cum again! Don't stop! AAAH!"),

            _("That's two! I want to see how many you can give me! AAAH!"),

        ],
        "girl_cum.orgasm_3rd_plus.cum_slut": [
            _("More more MORE! I want to cum until I can't think! AAAH!"),

            _("I've lost count and I don't CARE! Keep making me cum! AAAH!"),

            _("My body is addicted to this! I can't stop! AAAH!"),

        ],
        "girl_cum.orgasm_2nd.hardcore": [
            _("That's it! Make me cum again! HARDER! AAAH!"),

            _("Two already?! You better not be slowing down! AAAH!"),

            _("Again! And it's even stronger this time! AAAH!"),

        ],
        "girl_cum.orgasm_3rd_plus.hardcore": [
            _("Break me! I don't care anymore! AAAH!"),

            _("I can't feel my legs and I want MORE! AAAH!"),

            _("My body is falling apart and I LOVE it! AAAH!"),

        ],
        "girl_cum.orgasm_2nd.cute": [
            _("N-Not again... this is so embarrassing... AAAH!"),

            _("I can't believe I came twice already... please don't stare..."),

            _("W-Why does my body keep... oh no... AAAH!"),

        ],
        "girl_cum.orgasm_3rd_plus.cute": [
            _("I'm so sorry... I can't control it anymore... AAAH!"),

            _("Please don't think I'm weird... my body just won't stop... AAAH!"),

            _("I've never cum this many times... I'm so embarrassed... AAAH!"),

        ],

        # ══════════════════════════════════════════════════════════
        #  GIRL POST-CUM
        # ══════════════════════════════════════════════════════════

        "girl_post_cum": [  # Pos-orgasmo base da garota
            _("Oh my god... that was amazing..."),

            _("I... I need a moment..."),

            _("Wow... I'm still shaking..."),

        ],
        "girl_post_cum.cowgirl": [  # Durante cowgirl
            _("Let me... catch my breath before I keep going..."),

            _("That was incredible. But I'm not done with you."),

            _("Give me a second... I need to... wow."),

        ],
        "girl_post_cum.anal": [  # Pos-orgasmo anal (default: processando surpresa)
            _("I... I came from anal... I didn't even think that was possible..."),

            _("That really just happened... I came from my ass..."),

            _("I don't even know what to say... my body just..."),

        ],
        "girl_post_cum.anal.hardcore": [  # Hardcore amou
            _("Holy shit... my ass just made me cum harder than anything. Keep going."),

            _("Anal orgasms hit different... don't you dare stop now."),

            _("Fuck... I just came from my ass and I already want more. Harder."),

        ],
        "girl_post_cum.anal.cute": [  # Cute morrendo de vergonha
            _("Please don't tell anyone I came from that... I'll die..."),

            _("I can't look at you right now... I can't believe that just happened..."),

            _("I couldn't stop it... please... you know I'm not like that... right?"),

        ],
        "girl_post_cum.anal.boyfriend": [  # Namorado: culpa pesada
            _("He's never even touched me there... and I just came from it with you..."),

            _("I feel so guilty... my {hint}boyfriend{/hint} has no idea I'm capable of... that..."),

            _("What am I doing... I just orgasmed from anal with another man..."),

        ],
        "girl_post_cum.anal.girlfriend": [  # Namorada: conflito de sexualidade
            _("She's never even been able to reach that deep... and a man just made me cum from it..."),

            _("I feel so confused... my {hint}girlfriend{/hint} has no idea a cock could make me feel... that..."),

            _("What am I doing... I just orgasmed from your cock in my ass... and it was incredible..."),

        ],
        "girl_post_cum.anal.hate_cum": [  # CuH pos-orgasmo anal -- sem "surprises inside/goo"
            _("I can't believe I just came from that... my ass is still twitching..."),

            _("That was... intense. I hate that my body reacted like that."),

            _("Okay... wow... I came from anal. I'm never admitting that out loud again."),

        ],
        "girl_post_cum.anal.hate_cum.hardcore": [  # CuH + HC pos-orgasmo anal
            _("I came from my ass and I hate how much I loved it. Keep going."),

            _("That orgasm was disgusting. Do it again."),

            _("I hate anal. I hate that I came. I hate that I want more. Don't stop."),

        ],
        "girl_post_cum.anal.hate_cum.cute": [  # CuH + cute pos-orgasmo anal
            _("That was... I can't believe I just... back there... and without protection..."),

            _("I feel so dirty... cumming from that... Please tell me you didn't finish inside..."),

            _("Oh god... that felt too good for something so wrong... I need a moment..."),

        ],
        "girl_post_cum.anal.loyal": [  # Post-orgasm loyal girl after anal
            _("I just came from... that. What kind of girlfriend am I..."),

            _("That was incredible but... I feel so guilty. This isn't me."),

        ],
        "girl_post_cum.anal.cum_slut": [  # Post-orgasm cum slut after anal
            _("My ass is still throbbing... that was amazing. Do it again."),

            _("I came so hard from anal... I think I'm addicted to this."),

        ],
        "girl_post_cum.hj": [  # Durante handjob
            _("My hand is shaking... I'm still tingling..."),

            _("That was intense... even for me..."),

            _("Wow... I came just from touching you..."),

        ],
        "girl_post_cum.bj": [  # Durante blowjob
            _("Haa... haa... let me catch my breath..."),

            _("Even my jaw is trembling... god..."),

            _("I need a second... then I'll keep going..."),

        ],
        "girl_post_cum.tj": [  # Durante titjob
            _("My whole chest is tingling..."),

            _("I can't believe that made me cum..."),

            _("Wow... let me press them together again..."),

        ],
        "girl_post_cum.first_time": [  # Primeira vez
            _("Is that... is that what it always feels like?"),

            _("I had no idea... I had absolutely no idea..."),

            _("I think... I think I understand now..."),

        ],
        "girl_post_cum.cum_slut": [  # Garota adora cum
            _("More. I want to cum again."),

            _("That was just the first one... keep going."),

            _("Don't stop now... I want another..."),

        ],
        "girl_post_cum.boyfriend": [  # Garota tem namorado
            _("He's never made me cum like that..."),

            _("God... what am I doing... but it was so good..."),

            _("I shouldn't compare, but... you're on another level..."),

        ],
        "girl_post_cum.girlfriend": [  # Garota tem namorada
            _("She's never made me cum like that... no woman ever has..."),

            _("God... what am I doing with a man... but it was so good..."),

            _("I shouldn't compare, but... a cock is on another level entirely..."),

        ],
        "girl_post_cum.cute": [  # Sexo gentil/carinhoso
            _("That was beautiful... I feel so close to you..."),

            _("Hold me for a moment... I'm still floating..."),

            _("You're amazing... I'm so happy right now..."),

        ],
        "girl_post_cum.public": [  # Local publico
            _("Oh god... I think someone heard me..."),

            _("Did anyone see? Are we okay?"),

            _("I tried to be quiet... I really tried..."),

        ],
        "girl_post_cum.camera_hater": [
            _("Please tell me you didn't record that..."),

            _("If my O-face ends up anywhere online... I'll kill you."),

            _("That was amazing... but no evidence, okay?"),

        ],
        "girl_post_cum.camera_lover": [
            _("Tell me you got that... I want to see my face when I came."),

            _("That footage is going to be incredible..."),

            _("Best content ever... I looked good, right?"),

        ],
        "girl_post_cum.hate_cum": [
            _("God that was good... at least you didn't make a mess."),

            _("Okay... wow... that was worth it. As long as you haven't left any surprises inside me."),

            _("Amazing... but I'm not going to forgive you if I find any of your goo in there later."),

        ],
        "girl_post_cum.loyal": [
            _("Oh god... that was insane... I've never wanted something so badly in my life..."),

            _("I can't believe how intense that was... my body completely took over..."),

            _("What just happened... I lost all control... the desire was overwhelming..."),

        ],

        # ── Repeated orgasm post-cum ──────────────────────────────

        "girl_post_cum.orgasm_2nd": [
            _("Twice... you made me cum twice... what are you doing to me..."),

            _("I didn't think I could cum again that fast..."),

            _("My body is way more sensitive now... be careful..."),

        ],
        "girl_post_cum.orgasm_3rd_plus": [
            _("I can barely feel my legs... how many times was that..."),

            _("My whole body is tingling... I've never cum this much in my life..."),

            _("I think my brain stopped working a few orgasms ago..."),

        ],
        "girl_post_cum.orgasm_2nd.cum_slut": [
            _("Two down... and I'm already getting ready for the next one..."),

            _("Twice and I still want more... don't judge me..."),

        ],
        "girl_post_cum.orgasm_3rd_plus.cum_slut": [
            _("I'm completely drained and I STILL want more..."),

            _("You've ruined me... I'll never be satisfied with just one again..."),

        ],
        "girl_post_cum.orgasm_2nd.hardcore": [
            _("That was stronger than the first one. Make the next one even harder."),

            _("Two. And you better not be thinking about stopping."),

        ],
        "girl_post_cum.orgasm_3rd_plus.hardcore": [
            _("My body is wrecked and I don't care. Keep going until I break."),

            _("I can barely move... but if you stop now I'll kill you."),

        ],
        "girl_post_cum.orgasm_2nd.cute": [
            _("T-Twice... I've never done that before... is that normal...?"),

            _("Please don't look at me like that... it's not my fault my body keeps..."),

        ],
        "girl_post_cum.orgasm_3rd_plus.cute": [
            _("I can't stop trembling... I've never felt so... I'm sorry..."),

            _("Please hold me... I don't think I can feel my body right now..."),

        ],

        # ══════════════════════════════════════════════════════════
        #  INTENSE ORGASM (tier 2) — stronger than base, not mind-breaking
        # ══════════════════════════════════════════════════════════

        "girl_cum_intense": [
            _("Oh GOD... that one hit different... mmm..."),

            _("Fuck... that was a big one... I can feel it everywhere..."),

            _("Aaah... that was... intense... wow..."),

        ],
        "girl_cum_intense.cum_slut": [
            _("Yesss... God, that was amazing... more, please, more..."),

            _("Mmm... that one made my toes curl... keep going..."),

        ],
        "girl_cum_intense.hardcore": [
            _("Fuck yes... THAT'S how you make me cum... harder..."),

            _("Now THAT was worth it... don't you dare slow down..."),

        ],
        "girl_cum_intense.cute": [
            _("Oh... oh wow... that was... a lot... I need a second..."),

            _("I... I felt that one everywhere... please be gentle for a bit..."),

        ],
        "girl_cum_intense.boyfriend": [
            _("That was... that was way more intense than it should be with someone who's not my %(pl)s..."),

            _("%(Pp)s has never made me feel like THAT..."),

        ],
        "girl_cum_intense.girlfriend": [
            _("A guy just made me cum like that... what is happening to me..."),

            _("That was intense... I'm not supposed to feel this good with a man..."),

        ],

        "girl_post_cum_intense": [
            _("I'm still shaking... give me a moment..."),

            _("That one took a lot out of me..."),

            _("Wow... I need to catch my breath after that one..."),

        ],
        "girl_post_cum_intense.cum_slut": [
            _("I can still feel it pulsing... God, I want more..."),

            _("My whole body is tingling... don't stop now..."),

        ],
        "girl_post_cum_intense.hardcore": [
            _("That was a good one. Don't let me recover, keep going."),

            _("Yeah... more like that. You know what I want."),

        ],
        "girl_post_cum_intense.cute": [
            _("I think I need a minute... that really got to me..."),

            _("Everything is so sensitive now... please be careful..."),

        ],

        # ══════════════════════════════════════════════════════════
        #  ORGASM FATIGUE — dazed / exhausted after multiple orgasms
        # ══════════════════════════════════════════════════════════

        "girl_orgasm_dazed": [
            _("I can barely think straight anymore..."),

            _("My legs are shaking... I don't know how much more I can take..."),

            _("Everything feels so sensitive now..."),

        ],
        "girl_orgasm_dazed.cum_slut": [
            _("My brain is turning to mush... and I love it..."),

            _("I can barely see straight... but don't you dare stop..."),

        ],
        "girl_orgasm_dazed.hardcore": [
            _("I can barely hold myself together... keep going anyway..."),

            _("My body is screaming at me to stop... but I don't care..."),

        ],
        "girl_orgasm_dazed.cute": [
            _("I feel so fuzzy... everything is warm and tingly..."),

            _("I can't... I can't focus on anything anymore..."),

        ],

        "girl_orgasm_exhausted": [
            _("I... I really can't take anymore... please..."),

            _("My body won't stop trembling... I need to rest..."),

            _("Everything hurts in the best way but I'm done... I'm so done..."),

        ],
        "girl_orgasm_exhausted.cum_slut": [
            _("I want more but my body is giving out... please... I need a break..."),

            _("Even I have a limit... and you found it... wow..."),

        ],
        "girl_orgasm_exhausted.hardcore": [
            _("Okay... okay you win. I actually can't take anymore. Happy?"),

            _("I've never been pushed this far before... I need to stop..."),

        ],
        "girl_orgasm_exhausted.cute": [
            _("Please... no more... I'll do anything just let me rest..."),

            _("I'm going to pass out if you keep going... please..."),

        ],

        # ══════════════════════════════════════════════════════════
        #  NON-SCENE ORGASM — cumming outside sex scenes (standing)
        # ══════════════════════════════════════════════════════════

        "girl_nonscene_orgasm": [
            _("W-wait... did I just...? Oh my god..."),

            _("I... I can't believe I just... from just that..."),

            _("Oh god... that actually made me... right here?!"),

        ],
        "girl_nonscene_orgasm.cum_slut": [
            _("Oh wow... you barely touched me and I just... mmm..."),

            _("Did that really just happen? God, you have no idea what you do to me..."),

        ],
        "girl_nonscene_orgasm.hardcore": [
            _("Shit... I wasn't expecting that. You're full of surprises."),

            _("Well THAT just happened. Don't look so smug about it."),

        ],
        "girl_nonscene_orgasm.cute": [
            _("I... I... oh no, did anyone see? That was so embarrassing..."),

            _("P-please pretend that didn't happen... I'm so mortified..."),

        ],

        # ══════════════════════════════════════════════════════════
        #  CUM INSIDE (Creampie Reactions)
        # ══════════════════════════════════════════════════════════

        # ══════════════════════════════════════════════════════════
        #  HARD ORGASM — Intense cum (ahegao, mind-breaking)
        # ══════════════════════════════════════════════════════════

        "girl_cum_hard": [
            _("I CAN'T... MY HEAD IS... EVERYTHING IS GOING WHITE... AAAAAH!"),

            _("YES YES YES! OH GOD I'M LOSING MY MIND! AAAAAH!"),

            _("I can't think... I can't... AAAAAH! AAAAAH!"),

            _("My body won't stop shaking! I'm cumming I'm cumming I'M CUMMING!"),

            _("AAAH! It won't stop! My whole body is... AAAAAH!"),

        ],
        "girl_cum_hard.hj": [
            _("Just from your hand... I'm losing it... my legs won't stop shaking! AAAAAH!"),

            _("How... how is your hand doing THIS to me?! I can't... AAAAAH!"),

            _("My brain is melting... just from a handjob... AAAAAH!"),

        ],
        "girl_cum_hard.bj": [
            _("MMPH! MMMMMPH!"),

            _("Hnngh... nngh... MMMPH!"),

            _("I can't... even with you in my mouth... I'm... MMMPH!"),

        ],
        "girl_cum_hard.tj": [
            _("My whole body... just from my tits... I'm going CRAZY! AAAAAH!"),

            _("I can feel it through my chest... into my brain... AAAAAH!"),

            _("Your cock between them is making me... my mind is... AAAAAH!"),

        ],
        "girl_cum_hard.cowgirl": [
            _("I can't stop riding! My hips won't listen! AAAAAH!"),

            _("So deep! I'm going crazy! I can feel you EVERYWHERE! AAAAAH!"),

            _("My body is moving on its own! I can't... I CAN'T STOP! AAAAAH!"),

            _("RIGHT THERE! RIGHT THERE! MY BRAIN IS... AAAAAH!"),

        ],
        "girl_cum_hard.anal": [
            _("MY ASS IS... I CAN'T... MY BRAIN IS MELTING! AAAAAH!"),

            _("I'M CUMMING FROM MY ASS SO HARD I CAN'T THINK! AAAAAH!"),

            _("I can't... I didn't know it could feel THIS... AAAAAH!"),

            _("My whole body is shaking! From my ASS! I'm losing my MIND! AAAAAH!"),

        ],
        "girl_cum_hard.hardcore": [
            _("FUCK! FUCK! I'M LOSING MY FUCKING MIND! DON'T STOP! AAAAAH!"),

            _("HARDER! I'M CUMMING SO HARD I CAN'T SEE! AAAAAH!"),

            _("YES! BREAK ME! I'M... I'M... AAAAAH!"),

        ],
        "girl_cum_hard.cute": [
            _("I can't... it's too much... too intense... my head is... AAAAAH!"),

            _("Everything is spinning... I've never felt... AAAAAH!"),

            _("Please hold me... I'm losing myself... I can't... AAAAAH!"),

        ],
        "girl_cum_hard.cum_slut": [
            _("I'M CUMMING SO HARD! MORE! I WANT MORE! AAAAAH!"),

            _("MY BRAIN... MY BODY... EVERYTHING IS CUMMING! AAAAAH!"),

            _("I CAN'T STOP! I DON'T WANT TO STOP! AAAAAH!"),

        ],
        "girl_cum_hard.boyfriend": [
            _("He's NEVER... I've NEVER felt... oh GOD... AAAAAH!"),

            _("I'm cumming so hard I can't even remember his name! AAAAAH!"),

            _("Nothing... NOTHING has ever felt like this! My mind is... AAAAAH!"),

        ],
        "girl_cum_hard.hate_cum": [
            _("I HATE THIS! I HATE THAT IT FEELS THIS GOOD! AAAAAH!"),

            _("WHY?! Why does my body... I can't control... AAAAAH!"),

            _("STOP! Don't stop! I don't know! My brain is... AAAAAH!"),

        ],
        "girl_cum_hard.camera_lover": [
            _("GET THIS ON CAMERA! I'm losing my MIND! AAAAAH!"),

            _("Film me! Film this face! I'm CUMMING! AAAAAH!"),

            _("Everyone needs to see this! I'm... I'M... AAAAAH!"),

        ],
        "girl_cum_hard.camera_hater": [
            _("DON'T LOOK AT ME! I can't control my face! AAAAAH!"),

            _("My eyes... I can't close them! Don't record this! AAAAAH!"),

            _("If anyone sees me like this... I'll... AAAAAH!"),

        ],
        "girl_cum_hard.loyal": [
            _("I've never... nobody has ever made me feel... AAAAAH!"),

            _("This is wrong but my body won't listen! I'M LOSING MYSELF! AAAAAH!"),

            _("I can't fight it! My whole body is... AAAAAH!"),

        ],
        "girl_cum_hard.public": [
            _("I CAN'T BE QUIET! Everyone is going to hear... AAAAAH!"),

            _("I don't CARE who sees! I'm CUMMING! AAAAAH!"),

            _("My voice won't... I can't hold it in! AAAAAH!"),

        ],
        "girl_cum_hard.anal.hardcore": [
            _("FUCK MY ASS! I'M CUMMING SO HARD I CAN'T SEE! AAAAAH!"),

            _("MY ASS! MY BRAIN! EVERYTHING! DON'T STOP! AAAAAH!"),

        ],
        "girl_cum_hard.anal.cute": [
            _("Not from there... not this hard... I can't think anymore... AAAAAH!"),

            _("My body... from my butt... everything is going white... AAAAAH!"),

        ],
        "girl_cum_hard.anal.boyfriend": [
            _("He never... I never even let him... and now I'm losing my mind from... AAAAAH!"),

            _("I'm cumming from my ass harder than he's ever made me cum! AAAAAH!"),

        ],
        "girl_cum_hard.anal.cum_slut": [
            _("I'M CUMMING FROM MY ASS AND I LOVE IT! MORE! FILL ME! AAAAAH!"),

            _("MY ASS IS MAKING ME CUM SO HARD! I NEED MORE! AAAAAH!"),

        ],
        "girl_cum_hard.cowgirl.boyfriend": [
            _("I'm riding you so hard I forgot I have a boyfriend! AAAAAH!"),

            _("He's never been this deep! I can't... I CAN'T THINK! AAAAAH!"),

        ],
        "girl_cum_hard.girlfriend": [
            _("She never... NOBODY has ever made me feel... you're making me... AAAAAH!"),

            _("I don't even LIKE men and I'm cumming this hard?! AAAAAH!"),

            _("My girlfriend could NEVER... why is a man doing this to me?! AAAAAH!"),

        ],
        "girl_cum_hard.anal.girlfriend": [
            _("She never even touched me there... and you're making me lose my mind from... AAAAAH!"),

            _("I'm cumming from my ass for a GUY harder than any woman has ever made me cum! AAAAAH!"),

        ],
        "girl_cum_hard.cowgirl.girlfriend": [
            _("I'm riding you and it feels better than anything she's ever done! AAAAAH!"),

            _("My girlfriend uses toys... but nothing compares to... I CAN'T THINK! AAAAAH!"),

        ],
        "girl_cum_hard.lesbian": [
            _("I'm not supposed to... why is this... AAAAAH!"),

            _("Why is my body doing this! I DON'T... AAAAAH!"),

            _("This isn't me! I'm cumming and I can't... AAAAAH!"),

        ],
        "girl_cum_hard.lesbian_denial": [
            _("This means NOTHING! My body is just... it's PHYSICAL! AAAAAH!"),

            _("I'm NOT enjoying this! My body is LYING! I don't want... AAAAAH!"),

        ],
        "girl_cum_hard.lesbian_conflict": [
            _("Why does HE make me feel like this?! No woman has ever... AAAAAH!"),

            _("I hate this! I hate that you're the EXCEPTION! AAAAAH!"),

        ],
        "girl_cum_hard.lesbian_accepted": [
            _("You're the only man who could EVER... the ONLY one! AAAAAH!"),

            _("I don't like men! You're just... you're IMPOSSIBLE! AAAAAH!"),

        ],
        "girl_cum_hard.cheater": [
            _("YES! Let them all know! I don't CARE! AAAAAH!"),

            _("I'm CUMMING and I don't give a FUCK about anyone else! AAAAAH!"),

            _("This is BETTER than anything I have at home! AAAAAH!"),

        ],
        "girl_cum_hard.public_fetish": [
            _("Everyone can HEAR me! Everyone can SEE! AAAAAH!"),

            _("I WANT them to watch! Let the whole world hear me CUM! AAAAAH!"),

            _("MORE PEOPLE! I want MORE eyes on me while I LOSE IT! AAAAAH!"),

        ],
        "girl_cum_hard.public_shy": [
            _("No no no... everyone is going to hear... I can't hold it... AAAAAH!"),

            _("I'm trying to be quiet but my body WON'T LET ME! AAAAAH!"),

            _("They can hear everything... oh god oh god... AAAAAH!"),

        ],
        "girl_cum_hard.cowgirl.cum_slut": [
            _("I'M RIDING YOUR CUM OUT OF YOU! GIVE ME EVERYTHING! AAAAAH!"),

            _("I can feel it DEEP! Fill me while I RIDE! AAAAAH!"),

            _("MY PUSSY IS MILKING YOU DRY! MORE! MORE! AAAAAH!"),

        ],
        "girl_cum_hard.cowgirl.hardcore": [
            _("I'M GOING TO BREAK YOU! MY HIPS WON'T STOP! AAAAAH!"),

            _("HARDER! I'LL RIDE YOU INTO THE GROUND! AAAAAH!"),

            _("YOU CAN'T HANDLE ME ON TOP! I'M TOO MUCH! AAAAAH!"),

        ],
        "girl_cum_hard.anal.hate_cum": [
            _("NOT IN MY ASS! DON'T YOU DARE CUM IN... why does it feel... AAAAAH!"),

            _("I HATE this AND I hate cum AND my body won't LISTEN! AAAAAH!"),

        ],
        # NOTE: anal_lover/anal_hater pools MUST be scene-scoped (.anal.) — the
        # trait modifier is added regardless of scene (needed for anal_request /
        # atm pools), so an unscoped pool would fire during vaginal too.
        "girl_cum_hard.anal.anal_lover": [
            _("MY ASS LOVES YOUR COCK MORE THAN ANYTHING! FILL IT! AAAAAH!"),

            _("I'M CUMMING SO HARD FROM MY ASS! I WAS BORN FOR THIS! AAAAAH!"),

            _("MY ASS! I LOVE IT! Don't EVER stop! AAAAAH!"),

            _("DEEPER! HARDER! My ass was MADE for this! AAAAAH!"),

            _("I'M CUMMING FROM MY ASS AND I WANT MORE! NEVER STOP! AAAAAH!"),

        ],
        "girl_cum_hard.anal.anal_hater": [
            _("I HATE my ass being touched and I'm CUMMING from it?! WHAT IS WRONG WITH ME?! AAAAAH!"),

            _("NOT FROM THERE! I HATE IT! Then why is my body... AAAAAH!"),

            _("NOT THERE! I HATE... why does it feel... AAAAAH!"),

            _("I DON'T want this! My body is LYING! My ass shouldn't... AAAAAH!"),

            _("STOP! Why does something I HATE feel this... AAAAAH!"),

        ],

        # ── Repeated hard orgasm ───────────────────────────────────

        "girl_cum_hard.orgasm_2nd": [
            _("NOT AGAIN! MY BRAIN IS... I CAN'T... AAAAAH!"),

            _("ANOTHER ONE LIKE THAT?! I'M GOING TO PASS OUT! AAAAAH!"),

            _("IT'S EVEN STRONGER THAN THE FIRST! I CAN'T TAKE IT! AAAAAH!"),

        ],
        "girl_cum_hard.orgasm_3rd_plus": [
            _("I'VE COMPLETELY LOST MY MIND! HOW MANY TIMES IS THAT?! AAAAAH!"),

            _("MY BODY DOESN'T LISTEN TO ME ANYMORE! I JUST KEEP CUMMING! AAAAAH!"),

            _("I CAN'T EVEN SCREAM PROPERLY ANYMORE... EVERYTHING IS... AAAAAH!"),

        ],

        "girl_post_cum_hard": [
            _("I... I can't move... my legs are completely numb..."),

            _("What... what just happened to me... I've never felt anything like that..."),

            _("I think I blacked out for a second... oh god..."),

            _("My whole body is still trembling... I can't stop..."),

            _("I can still feel it... everywhere... my brain isn't working..."),

        ],
        "girl_post_cum_hard.hj": [
            _("Just from your hand... and I completely lost myself... that was terrifying..."),

            _("I can't feel my legs... from a handjob... what are you doing to me..."),

        ],
        "girl_post_cum_hard.bj": [
            _("I'm drooling... I can't close my mouth properly... what happened..."),

            _("My jaw... my everything... I went somewhere else for a second..."),

        ],
        "girl_post_cum_hard.tj": [
            _("My chest is still pulsing... I've never cum that hard from my tits..."),

            _("I think my brain short-circuited... just from my breasts..."),

        ],
        "girl_post_cum_hard.cowgirl": [
            _("I can't lift my hips... they're completely gone..."),

            _("I can still feel you throbbing inside me... I can't come down from this..."),

            _("That was... I don't have words. My mind went blank."),

        ],
        "girl_post_cum_hard.anal": [
            _("I came so hard from my ass that I can't think straight..."),

            _("My body... I've never felt so overwhelmed. From back there..."),

        ],
        "girl_post_cum_hard.hardcore": [
            _("More. I need more. That wasn't enough. Harder."),

            _("My brain is still fried... and I already want the next one..."),

        ],
        "girl_post_cum_hard.cute": [
            _("Please hold me... I'm shaking so much... I can't stop..."),

            _("That was too much... I think I left my body for a moment..."),

        ],
        "girl_post_cum_hard.cum_slut": [
            _("Again. I need to cum like that again. Right now."),

            _("That was the best orgasm of my life and I want another one immediately."),

        ],
        "girl_post_cum_hard.boyfriend": [
            _("He... he has never even come close to making me feel like that..."),

            _("I forgot his name. I literally forgot my boyfriend's name for a second..."),

        ],
        "girl_post_cum_hard.hate_cum": [
            _("I hate you for making my body do that... I lost all control..."),

            _("That was disgusting. The way I looked... don't ever mention this."),

        ],
        "girl_post_cum_hard.camera_lover": [
            _("Tell me you filmed the whole thing... my face must have been incredible..."),

            _("I want to watch that back... I bet I looked amazing losing my mind..."),

        ],
        "girl_post_cum_hard.loyal": [
            _("I've never lost control like that... with anyone... not even close..."),

            _("That scared me... how much my body wanted that... wanted you..."),

        ],
        "girl_post_cum_hard.public": [
            _("Everyone definitely heard that... I couldn't stop myself..."),

            _("My voice... I couldn't control anything. Everyone knows what just happened..."),

        ],
        "girl_post_cum_hard.girlfriend": [
            _("She has never... no woman has ever made me feel anything close to that..."),

            _("If my girlfriend knew a man just did that to me... I can't even think right now..."),

        ],
        "girl_post_cum_hard.lesbian": [
            _("Nobody has ever made me cum like that... I don't know who I am right now..."),

            _("You broke something in me... I can't even think straight..."),

        ],
        "girl_post_cum_hard.lesbian_denial": [
            _("That was nothing. Physical reaction. Meaningless. ...Why am I still shaking..."),

            _("Don't you dare think this means anything. I'm leaving. ...After I can feel my legs again."),

        ],
        "girl_post_cum_hard.lesbian_conflict": [
            _("You're the worst thing that ever happened to my identity... and the best thing that ever happened to my body..."),

            _("I hate you for making me feel like this. No... I hate that I don't hate it."),

        ],
        "girl_post_cum_hard.lesbian_accepted": [
            _("You're the exception. The only exception. And you just proved why... thoroughly."),

            _("I'm still into women. Except for whatever the hell you are."),

        ],
        "girl_post_cum_hard.cheater": [
            _("That was nothing. I can take more. I WANT more."),

            _("%(Pp)s could never make me feel that way. Not even close."),

            _("I'm not even sorry. That was the best I've ever had."),

        ],
        "girl_post_cum_hard.public_fetish": [
            _("Everyone saw that... everyone heard... and it was incredible."),

            _("The looks on their faces while I lost control... I want that feeling again."),

            _("Being watched while I came that hard... nothing else even compares."),

        ],
        "girl_post_cum_hard.public_shy": [
            _("Oh god... did everyone hear me? I couldn't control my voice..."),

            _("I tried so hard to stay quiet... my body completely betrayed me..."),

            _("People are staring... they definitely heard everything. I want to disappear."),

        ],
        # NOTE: scene-scoped (.anal.) on purpose — see girl_cum_hard.anal.anal_lover
        "girl_post_cum_hard.anal.anal_lover": [
            _("My ass is still throbbing... I need more of that..."),

            _("That orgasm from my ass was... I can still feel it pulsing. Don't stop."),

            _("My body is wrecked in the best way. My ass wants you back already."),

        ],
        "girl_post_cum_hard.anal.anal_hater": [
            _("I can't believe that just happened... from back there..."),

            _("I hate that my body responded like that... from a place I don't even want touched..."),

            _("That was NOT supposed to feel good. My ass has no right to make me cum like that."),

        ],

        # ── Repeated hard orgasm post-cum ─────────────────────────

        "girl_post_cum_hard.orgasm_2nd": [
            _("Two of those... and I think I actually blacked out this time..."),

            _("I didn't know my body could do that twice... I'm scared of what happens next..."),

        ],
        "girl_post_cum_hard.orgasm_3rd_plus": [
            _("I don't remember how many times... everything after the second one is a blur..."),

            _("I can't feel anything below my waist... and I'm not sure I care anymore..."),

        ],

        "cum_inside": [  # Reacao base ao creampie
            _("Oh... I can feel it... all of it..."),

            _("It's so warm..."),

            _("You came inside me..."),

        ],
        "cum_inside.lesbian": [  # Lesbian conflict
            _("You came inside me... oh god... this was never supposed to happen..."),

            _("I can feel it filling me up... this was never supposed to happen to a girl like me..."),

            _("I can feel every drop and I don't know who I am anymore..."),

        ],
        "cum_inside.cowgirl": [  # Durante cowgirl
            _("I can feel you pulsing inside me..."),

            _("Mmm... I felt every single shot..."),

            _("So deep... I can feel it filling me up..."),

        ],
        "cum_inside.anal": [  # Creampie anal
            _("Oh god... I can feel it filling my ass..."),

            _("You came inside my... oh fuck... it's so warm..."),

            _("I feel it pulsing... deep in my ass... oh my god..."),

            _("So much... I can feel every drop back there..."),

        ],
        "cum_inside.first_time": [  # Primeira vez
            _("You... you came inside me? Oh my god..."),

            _("I can feel it... it's so warm... is this what it's like?"),

            _("I didn't expect that... it feels... strange. But good."),

        ],
        "cum_inside.cum_slut": [  # Garota adora cum
            _("YES! Fill me up! Every last drop!"),

            _("I can feel it all... god I love your cum inside me..."),

            _("More... I want more inside me..."),

            _("That's exactly where it belongs..."),

        ],
        "cum_inside.hate_cum": [  # Garota odeia cum -- creampie 0 (first time)
            _("You... you came inside?! I told you not to!"),

            _("Get it out! Oh god..."),

            _("That's disgusting... I can feel it all..."),

        ],
        # hate_cum escalation: she hates it but her reactions betray her
        "cum_inside.hate_cum.hc_tier1": [  # creampie = 1
            _("Not AGAIN! I... I hate this. I trusted you! You came inside me TWICE! I can't believe it!"),

            _("You did it AGAIN?! That's TWICE now! Your disgusting cum is filling me up AGAIN!"),

            _("TWICE! You came inside me TWICE! I hate this! I hate feeling it drip out of me!"),

        ],
        "cum_inside.hate_cum.hc_tier2": [  # creampie 2-3
            _("Stop... doing this... I hate it... I HATE it... UGH! Filling my pussy with that disgusting cum..."),

            _("You keep pumping your gross cum inside me! How many times is this now?! I can feel ALL of it!"),

            _("Again and again and AGAIN! Your nasty cum keeps filling me up! ...Why is there so much?!"),

            _("I HATE your cum inside me! It's so warm and thick and... DISGUSTING! Stop making me feel it!"),

        ],
        "cum_inside.hate_cum.hc_tier4": [  # creampie 4+
            _("NOOOO! You filled my pussy again... So much... I hate you! Your hot cum... inside... BASTARD!"),

            _("You WON'T stop cumming inside me! Your thick hot load is... is... I HATE how deep it goes!"),

            _("EVERY TIME! Your cum keeps flooding my insides! It's so warm... so GROSS... there's SO MUCH!"),

            _("My pussy is FULL of your cum AGAIN! I hate it! I hate how it throbs inside me! You're the WORST!"),

            _("STOP filling me up! I can feel every drop pumping into me... your disgusting... hot... UGH! I HATE YOU!"),

        ],
        "cum_inside.anal.hate_cum.hc_tier2": [  # anal creampie 2-3 hate_cum
            _("Stop... doing this to my ass... I hate it... your disgusting cum keeps filling me back there!"),

            _("You keep pumping your gross cum inside my ass! How many times is this now?! I can feel ALL of it!"),

            _("Again and AGAIN! Your nasty cum keeps filling my ass! It's so deep... STOP!"),

        ],
        "cum_inside.anal.hate_cum.hc_tier4": [  # anal creampie 4+ hate_cum
            _("NOOOO! You filled my ass again... So much... I hate you! Your hot cum... deep inside... BASTARD!"),

            _("EVERY TIME! Your cum keeps flooding my ass! It's so warm back there... so GROSS... there's SO MUCH!"),

            _("My ass is FULL of your cum AGAIN! I hate it! I hate how it throbs inside me! You're the WORST!"),

        ],
        "cum_inside.boyfriend": [  # Garota tem namorado
            _("Oh god... you came inside me... what if I...?"),

            _("My boyfriend... we never did it raw... and now you..."),

            _("This is so wrong... but I felt every drop..."),

        ],
        "cum_inside.girlfriend": [  # Garota tem namorada
            _("You just came inside me... my girlfriend would never believe this..."),

            _("She can't do this... she could never fill me like... oh god..."),

            _("Your cum is inside me right now... this wasn't supposed to happen..."),

            _("You came inside me?! She's going to... oh no..."),

            _("If she finds out about this... I'm dead."),

            _("I need to clean up before she suspects anything..."),

        ],
        "cum_inside.recurring": [  # Recorrente / ja fez antes
            _("You always fill me up so good..."),

            _("I've been craving this all day..."),

            _("Another load inside me... I'm so full..."),

            _("How many times have you cum inside me now..."),

        ],
        "cum_inside.public": [  # Local publico
            _("Oh god... it's going to drip when we leave..."),

            _("How am I supposed to walk around after this?"),

            _("Anyone who looks at me will know..."),

        ],
        "cum_inside.cute": [  # Sexo gentil/carinhoso
            _("I can feel your warmth... it's so intimate..."),

            _("You filled me with your love..."),

            _("I feel so close to you right now..."),

        ],
        "cum_inside.nerd": [
            _("You... inside?! I'm not on the pill! Why would you do that?!"),

            _("Did you just... inside me?! I'm not safe right now! This is bad!"),

            _("No, no, no... I can feel it... this wasn't supposed to happen!"),

        ],
        "cum_inside.anal.nerd": [
            _("You came in my... I can feel it inside... that's so warm..."),

            _("Oh god... I can feel everything... I need a moment..."),

        ],
        "cum_inside.cowgirl.cum_slut": [  # Cowgirl + adora cum
            _("I milked every drop out of you with my hips..."),

            _("I could feel you getting bigger right before... mmm..."),

            _("That's a good boy... fill me up while I ride..."),

        ],
        "cum_inside.anal.cum_slut": [  # Anal + adora cum
            _("YES! Fill my ass! I want every drop in there!"),

            _("Oh god... your cum deep in my ass... I LOVE it..."),

            _("More... pump it ALL into my ass. Don't waste a single drop."),

        ],
        "cum_inside.anal.hardcore": [  # Anal + hardcore
            _("Fuck... I can feel your load pumping deep in my ass."),

            _("That's it. Fill my ass up. I want to feel it dripping out."),

            _("You came so hard inside my ass... I felt every throb."),

        ],
        "cum_inside.anal.cute": [  # Anal + cute
            _("You... you came in my butt? It feels... warm..."),

            _("I can feel it inside... back there... it's so intimate..."),

            _("That was so intense... I've never felt anything like that..."),

        ],
        "cum_inside.anal.boyfriend": [  # Anal + namorado
            _("My boyfriend has no idea you just came inside my ass..."),

            _("He'd never... do this. And now you're filling my ass with..."),

            _("This is our secret... what you just did to my ass..."),

        ],
        "cum_inside.anal.girlfriend": [  # Anal + namorada
            _("My girlfriend could never do this... you just came inside my ass..."),

            _("She doesn't even know I let anyone touch me there... let alone fill me..."),

            _("Nothing could ever feel like that... oh god, what am I doing..."),

        ],

        # --- Hardcore trait ---
        "cum_inside.hardcore": [  # Sexo intenso/pesado
            _("Fuck... that was intense. I felt every pulse."),

            _("Harder next time. But that load was worth it."),

            _("You pumped it all deep inside me... good."),

        ],
        "cum_inside.cowgirl.hardcore": [  # Cowgirl + sexo pesado
            _("I rode every last drop out of you. That's how it's done."),

            _("You came hard... I could feel it. More of that."),

            _("That's what I like. Deep and rough inside me."),

        ],

        # --- Cute trait (position-specific) ---
        "cum_inside.cowgirl.cute": [  # Cowgirl + sexo carinhoso
            _("Being on top... feeling you finish inside me... it was beautiful."),

            _("I could feel your heartbeat when you came... that was special."),

            _("I wanted to be close... and now I feel all of you inside me."),

        ],

        # --- Public fetish trait ---
        "cum_inside.public_fetish": [  # Fetiche em publico
            _("Oh god... it's going to drip when we leave... exciting."),

            _("Anyone could find out... and I love that."),

            _("Walking around with your cum inside me... thrilling."),

        ],

        # --- Public shy trait ---
        "cum_inside.public_shy": [  # Timida em publico
            _("Oh no... what if it leaks? People will notice..."),

            _("I need to clean up before anyone sees..."),

            _("This is so embarrassing... I can feel it inside me..."),

        ],

        # --- Camera hater trait ---
        "cum_inside.camera_hater": [
            _("Oh god... please tell me you didn't film that part..."),

            _("If anyone ever sees evidence of this... I'll die."),

            _("That felt amazing... but there better be no proof this happened."),

        ],

        # --- Camera lover trait ---
        "cum_inside.camera_lover": [
            _("Tell me you got that on camera... that was the money shot."),

            _("I hope you were filming... that's going to look incredible."),

            _("Best footage ever. I could feel every pulse."),

        ],

        # --- Loyal trait ---
        "cum_inside.loyal": [
            _("Inside me... this is crazy... I wanted that more than I've ever wanted anything..."),

            _("I can't believe I just begged for that... the desire made me lose my mind..."),

            _("Oh god... my body craved that so badly it overrode everything else..."),

        ],

        # --- Boyfriend trait (position-specific) ---
        "cum_inside.cowgirl.boyfriend": [  # Cowgirl + tem namorado
            _("I rode you until you came inside me... my boyfriend would die..."),

            _("He's never finished inside me... and I just let you do it on top..."),

            _("I can't believe I just did that... while he thinks I'm faithful..."),

        ],
        "cum_inside.cowgirl.girlfriend": [  # Cowgirl + tem namorada
            _("I rode you until you came inside me... my girlfriend would never understand..."),

            _("She can't do this... nothing could ever fill me like... oh god..."),

            _("I just rode you to completion... while she thinks I'm exclusively hers..."),

        ],

        # --- Session count: 2nd creampie ---
        "cum_inside.session_2nd": [  # 2a vez na mesma sessao
            _("Again?! You're filling me up even more..."),

            _("A second time inside... I can feel it mixing..."),

            _("Two loads... I'm starting to overflow..."),

        ],
        "cum_inside.session_2nd.cum_slut": [  # 2a vez + adora cum
            _("YES! More! Fill me up again!"),

            _("Another load... I'm getting addicted to this feeling..."),

            _("Keep going... I want to be overflowing with your cum."),

        ],
        "cum_inside.session_2nd.hate_cum": [  # 2a vez + odeia cum
            _("AGAIN?! Twice inside me?! What's wrong with you?!"),

            _("You already came inside once! How could you do it again?!"),

            _("I can't believe this... two loads... I feel disgusting."),

        ],

        # --- Session count: 3rd+ creampie ---
        "cum_inside.session_3rd_plus": [  # 3a+ vez na mesma sessao
            _("How many times is that now? I'm completely full..."),

            _("I've lost count... there's so much inside me..."),

            _("You keep filling me up... I can feel it all..."),

        ],
        "cum_inside.session_3rd_plus.cum_slut": [  # 3a+ vez + adora cum
            _("Don't stop... I want every drop you have left!"),

            _("I'm so full... and I want even more..."),

            _("You're turning me into a mess... and I love it."),

        ],
        "cum_inside.session_3rd_plus.hate_cum": [  # 3a+ vez + odeia cum
            _("STOP cumming inside me! How many times?!"),

            _("I'm going to be dripping for hours... I hate you."),

            _("This is beyond disgusting... I can barely move..."),

        ],

        # --- Lifetime experience: cream_experienced (5-9 total) ---
        "cum_inside.cream_experienced": [  # Ja recebeu creampies antes
            _("Mmm... I'm getting used to this feeling..."),

            _("You know exactly what you're doing to me..."),

            _("This never gets old... I can feel every drop."),

        ],

        # --- Lifetime experience: cream_veteran (10+) ---
        "cum_inside.cream_veteran": [  # Veterana em creampies
            _("At this point, my body expects it..."),

            _("You always finish inside me. I wouldn't have it any other way."),

            _("I've lost count of how many times you've filled me up..."),

        ],
        "cum_inside.cream_veteran.cum_slut": [  # Veterana + adora cum
            _("My body was made for this. Fill me up like always."),

            _("I can't even imagine you finishing anywhere else."),

            _("Every time feels better than the last. Never stop."),

        ],

        # --- Forced creampie (denied but player does it anyway) ---
        "cum_inside_forced": [  # Creampie forcado — base
            _("You came inside me?! I didn't want that!"),

            _("You came inside?! What the hell?!"),

            _("No! Not inside! Get it out!"),

        ],
        "cum_inside_forced.cum_slut": [  # Forcado + adora cum
            _("I said no but... oh god it feels so good..."),

            _("You didn't listen... but I can't say I hate it..."),

            _("I told you not to... but part of me is glad you did."),

        ],
        "cum_inside_forced.hate_cum": [  # Forcado + odeia cum -- creampie 0
            _("YOU BASTARD! I said NO! I can feel it all inside me!"),

            _("I'm going to be SICK. How could you do that to me?!"),

            _("I SPECIFICALLY said not inside! This is unforgivable!"),

        ],
        "cum_inside_forced.hate_cum.hc_tier1": [  # Forcado + odeia cum -- creampie 1
            _("NOT AGAIN! I trusted you! TWICE you pumped your disgusting cum inside me! I HATE this!"),

            _("You forced it inside me AGAIN! That's TWICE! Your gross cum is dripping out of me!"),

            _("TWICE NOW! I told you NO and you filled me with that nasty cum AGAIN! I can feel every drop!"),

        ],
        "cum_inside_forced.hate_cum.hc_tier2": [  # Forcado + odeia cum -- creampie 2-3
            _("STOP forcing your cum inside me! I HATE it! It's so warm and thick and... UGH! GROSS!"),

            _("How many times are you going to pump that disgusting load into my pussy?! I can feel it EVERYWHERE!"),

            _("You keep FILLING me! Your nasty cum is overflowing inside me! I hate how much there is!"),

        ],
        "cum_inside_forced.hate_cum.hc_tier4": [  # Forcado + odeia cum -- creampie 4+
            _("NOOOO! Not again! My pussy is so full of your cum... your hot, thick... I HATE YOU! BASTARD!"),

            _("You WON'T stop! Your disgusting cum keeps pumping deep inside me! It's so... warm... I HATE IT!"),

            _("EVERY SINGLE TIME! You flood my insides with that thick cum! I can feel it throbbing in me! YOU'RE AWFUL!"),

        ],
        "cum_inside_forced.boyfriend": [  # Forcado + tem namorado
            _("My boyfriend... you came inside me?! What have you done?!"),

            _("I said PULL OUT! If I get... oh god, my boyfriend..."),

            _("You've ruined everything! Inside me?! I'm with someone!"),

        ],
        "cum_inside_forced.girlfriend": [  # Forcado + tem namorada
            _("My girlfriend... you came inside me?! What have you done?!"),

            _("I said PULL OUT! My girlfriend... if she finds out about this..."),

            _("What have you DONE?! She can never find out about this... never!"),

        ],
        "cum_inside_forced.session_2nd": [  # Forcado + 2a vez na sessao
            _("AGAIN?! I didn't let you the first time either!"),

            _("You forced it inside me TWICE?! What is wrong with you?!"),

            _("I can't believe this is happening again... stop it!"),

        ],

        # --- Accepted creampie ask ---
        "cum_inside_accepted": [  # Creampie aceito — base
            _("Yes... do it inside me."),

            _("Okay... cum inside. I want it."),

            _("I'm ready... finish inside me."),

        ],
        "cum_inside_accepted.cum_slut": [  # Aceito + adora cum
            _("YES! Fill me up! Don't hold back!"),

            _("Inside me, NOW. Every last drop!"),

            _("I've been waiting for this... give it ALL to me."),

        ],
        "cum_inside_accepted.hate_cum": [  # Aceito + odeia cum
            _("...Fine. Just this once. Inside."),

            _("I can't believe I'm saying this... okay. Inside."),

            _("Do it... but I'm not happy about it."),

        ],
        "cum_inside_accepted.cute": [  # Aceito + sexo carinhoso
            _("I want to feel you... finish inside me, gently."),

            _("Fill me... I want to be close to you like that."),

            _("Yes... cum inside. I want all of you."),

        ],
        "cum_inside_accepted.hardcore": [  # Aceito + sexo pesado
            _("Do it. Hard. All the way inside."),

            _("Pump it deep. Don't you dare hold back."),

            _("Fill me up rough. I can take it."),

        ],
        "cum_inside_accepted.boyfriend": [  # Aceito + tem namorado
            _("Do it... my boyfriend never did this..."),

            _("Inside me... he can never know about this."),

            _("Yes... give me what he never could."),

        ],
        "cum_inside_accepted.girlfriend": [  # Aceito + tem namorada
            _("Do it... she could never do this to me..."),

            _("Inside me... she can never know about this."),

            _("Give me what she never could..."),

        ],
        "cum_inside_accepted.session_2nd": [  # Aceito + 2a vez na sessao
            _("Again? ...Okay. Do it."),

            _("One more time inside... I can handle it."),

            _("You want to go again? ...Fine. Inside."),

        ],
        "cum_inside_accepted.session_2nd.cum_slut": [  # Aceito + 2a vez + adora cum
            _("AGAIN! Yes! More inside me!"),

            _("I want another load! Don't stop!"),

            _("Fill me up again! I'm not done yet!"),

        ],

        # ── Accepted creampie ANAL variants ──────────────
        "cum_inside_accepted.anal": [
            _("In my ass? ...okay. Do it."),

            _("Fine... cum inside my ass. Just do it."),

            _("Yes... fill my ass. Go ahead."),

        ],
        "cum_inside_accepted.anal.cum_slut": [
            _("YES! Cum inside my ass! Fill it up!"),

            _("Do it! Every drop in my ass! NOW!"),

            _("I want your cum deep in my ass! Don't hold back!"),

        ],
        "cum_inside_accepted.anal.hate_cum": [
            _("Ugh... fine, in my ass. At least it's not my pussy..."),

            _("Whatever... just get it over with. In my ass."),

            _("My ass... I guess that's... less gross? Just do it."),

        ],
        "cum_inside_accepted.anal.cute": [
            _("In my... butt? ...o-okay. Be gentle about it..."),

            _("You want to finish there? ...that's embarrassing but... okay."),

            _("I... yes. Inside. Just... hold me after."),

        ],
        "cum_inside_accepted.anal.hardcore": [
            _("Do it. Pump it deep in my ass. Hard."),

            _("Fill my ass. Don't hold back a single drop."),

            _("Cum in my ass. I want to feel it all."),

        ],
        "cum_inside_accepted.anal.boyfriend": [
            _("Inside my ass... my boyfriend doesn't even know I do this..."),

            _("Do it... he'd lose his mind if he knew you're cumming in my ass."),

            _("In my ass... he never even asked for that. You just take it."),

        ],
        "cum_inside_accepted.anal.girlfriend": [
            _("Inside my ass... my girlfriend has no idea what I'm doing right now..."),

            _("Do it... she'd lose her mind if she knew about this."),

            _("In my ass... she could never do this. Nothing else can fill me like that."),

        ],

        # ── Denied creampie ANAL variants ──────────────
        "cum_inside_denied.anal": [
            _("Not in my ass... pull out."),

            _("No... don't cum in there. Please."),

            _("Pull out of my ass before you finish."),

        ],
        "cum_inside_denied.anal.hate_cum": [
            _("Do NOT cum inside my ass. I mean it."),

            _("If you finish in my ass I will KILL you. Pull out."),

            _("Your disgusting cum is NOT going in my ass."),

        ],
        "cum_inside_denied.anal.cute": [
            _("N-no... not in my butt... please pull out..."),

            _("I don't want it in there... please be careful..."),

            _("Please don't finish in my butt... I'm scared..."),

        ],
        "cum_inside_denied.anal.boyfriend": [
            _("Not in my ass... bad enough you're IN my ass..."),

            _("Pull out. My boyfriend would die if you came in my ass."),

            _("No. You don't get to cum inside someone else's girlfriend's ass."),

        ],
        "cum_inside_denied.anal.girlfriend": [
            _("Not in my ass... this is already bad enough..."),

            _("Pull out. If my girlfriend ever found out about this..."),

            _("No. This is where I draw the line. Pull out."),

        ],

        # ── Post-creampie reaction (she CONSENTED — processing what she allowed) ──

        "cum_inside_consented": [  # Base — ela permitiu
            _("Yesss... I feel all your cum inside my pussy... so warm..."),

            _("Oh fuck... you filled me up so good... my pussy is dripping with your cum..."),

            _("So much cum... I can feel it leaking out of me already... fuck..."),

            _("Mmmm... every drop inside me... my little pussy is so full..."),

            _("I asked for it and I don't regret it... your cum feels so good inside me..."),

        ],
        "cum_inside_consented.cum_slut": [  # Adora cum
            _("Yesss, fill my pussy with every last drop... I need ALL of it inside me..."),

            _("Mmmm so much cum... my pussy is overflowing... I want more..."),

            _("Don't you dare waste a single drop... my pussy deserves every bit of your cum..."),

            _("Haha yesss... so much cum inside me... I can feel it dripping down my thighs..."),

            _("Your cum belongs inside my pussy... nowhere else... give me everything..."),

        ],
        "cum_inside_consented.hate_cum": [  # Odeia cum -- conflito interno -- creampie 0
            _("I hate cum in my pussy... so why did I just beg you to fill me up... what's wrong with me..."),

            _("Your disgusting cum is inside my pussy... and I ASKED for it... I can feel every drop... ugh..."),

            _("I told you to do it... I TOLD you to pump your cum in my pussy... I'm disgusted with myself..."),

            _("My pussy is full of your cum and I hate it... I hate that I begged for it... why is it so warm..."),

        ],
        "cum_inside_consented.hate_cum.hc_tier1": [  # creampie 1
            _("AGAIN?! My pussy is full of your cum AGAIN and I ASKED for it! I hate your disgusting load inside me! ...So why did I beg TWICE?!"),

            _("TWICE I begged you to fill my pussy! Your gross cum pumping inside me... I can feel it dripping... I HATE this!"),

            _("I said yes... again... your nasty cum flooding my pussy for the second time... I hate how warm it feels..."),

        ],
        "cum_inside_consented.hate_cum.hc_tier2": [  # creampie 2-3
            _("I keep begging you to cum inside my pussy! I HATE your cum! Your thick disgusting load dripping out of me... why can't I stop saying YES?!"),

            _("Fill my pussy... I said FILL IT. I hate this! Your cum flooding inside me... my pussy is overflowing with your nasty load and I KEEP ASKING!"),

            _("I'm disgusted... I keep begging for your cum inside my pussy... it's so warm and thick and... I HATE IT! I hate that my pussy wants more!"),

        ],
        "cum_inside_consented.hate_cum.hc_tier4": [  # creampie 4+
            _("Inside... pump it ALL inside my pussy... I HATE your cum! I hate how much my pussy needs it! Your hot thick load filling me... UGH! JUST DO IT!"),

            _("I begged before you even started... your disgusting cum deep inside my pussy... I hate that I NEED your load inside me now! What have you done to me?!"),

            _("Cum inside my pussy... do it... I HATE it! I hate your cum! I hate that my pussy squeezes every drop out of you like it belongs there! WHAT AM I BECOMING?!"),

        ],
        "cum_inside_consented.cheater": [  # Traindo o parceiro
            _("That loser will never cum inside me like you do... my pussy belongs to you..."),

            _("I begged you to fill my pussy while my %(pl)s thinks I'm being faithful... fuck..."),

            _("%(Poss)s partner just begged another man to pump her full of cum... and I'd do it again..."),

            _("My %(pl)s uses condoms... and here I am dripping with your cum, asking for more..."),

            _("I'm going home to %(po)s with your cum still inside my pussy... and I love it..."),

        ],
        "cum_inside_consented.boyfriend": [  # Tem namorado
            _("My boyfriend... I just begged another man to flood my pussy with cum..."),

            _("I have a boyfriend and your cum is dripping out of me... I asked for every drop..."),

            _("He can never know I begged you to fill my little pussy... oh god it feels so good..."),

            _("I'm such a bad girlfriend... your cum is so deep inside me and I wanted it all..."),

            _("My boyfriend would die if he knew I was begging for your cum inside my pussy..."),

        ],
        "cum_inside_consented.girlfriend": [  # Tem namorada
            _("My girlfriend... I just begged you to flood my pussy with cum... what am I doing..."),

            _("I have a girlfriend and your cum is dripping out of me... I asked for every drop..."),

            _("She can never know I begged for this... you did what she never could..."),

            _("I'm supposed to be hers... your cum is so deep inside me and I wanted it all..."),

            _("My girlfriend would die if she knew I was begging for your cum inside my pussy..."),

        ],
        "cum_inside_consented.cute": [  # Carinhosa
            _("It feels so warm inside me... your cum filling my pussy... I feel so close to you..."),

            _("I wanted every single drop inside me... my pussy feels so full and warm..."),

            _("That was so intimate... feeling your cum pump inside me... I never want this feeling to end..."),

            _("I can feel it all... so warm and deep... my pussy is yours..."),

            _("Hold me like this... with your cum still inside me... it feels perfect..."),

        ],
        "cum_inside_consented.hardcore": [  # Pesada
            _("Fuck yes. Pump every drop of cum deep in my pussy. That's exactly what I needed."),

            _("Deeper. I want your cum so deep I'll feel it for days. No holding back."),

            _("That's what I fucking wanted. My pussy full of your hot cum. More."),

            _("I asked for every drop and you delivered. My pussy is overflowing. Perfect."),

        ],
        "cum_inside_consented.femdom": [
            _("I told you to fill me up and you did. My pussy is dripping. Good boy."),

            _("Good. I said inside, and you came exactly where I told you to."),

            _("Every drop in my pussy, just like I ordered. You may rest now."),

        ],
        "cum_inside_consented.virgin": [  # Virgem
            _("My first time ever and my pussy is full of your cum... I can't believe I begged for it..."),

            _("I lost my virginity and asked you to fill my pussy... who am I becoming..."),

            _("My first cock and my first creampie... I can feel every drop inside me... oh god..."),

            _("I saved myself and then begged for cum inside my pussy on the first time... fuck..."),

            _("I'm not a virgin anymore and my pussy is dripping with your cum... I asked for this..."),

        ],
        "cum_inside_consented.public_fetish": [  # Fetiche em publico
            _("I begged you to fill my pussy right here where anyone could see... and it was incredible..."),

            _("Your cum dripping down my thighs in public... I asked for it and I'm so wet just thinking about it..."),

            _("Fill me up where everyone can see... my pussy is yours... let them watch your cum leak out of me..."),

            _("Creampied in public and my pussy is dripping... anyone could notice... fuck I love this..."),

            _("I want everyone to see your cum running down my legs... I begged for this..."),

        ],
        "cum_inside_consented.public_shy": [  # Timida em publico
            _("Oh god... your cum is inside me HERE?! What if someone sees it dripping down my legs?!"),

            _("I begged for it and now your cum is leaking out of my pussy... in public... what's wrong with me..."),

            _("My pussy is so full of your cum... if anyone looks down they'll see it on my thighs... oh no..."),

            _("I asked you to cum inside me where people could walk by... it's dripping... I need to clean up..."),

            _("Your cum is so warm inside my pussy... please don't let it leak... not here..."),

        ],
        "cum_inside_consented.camera_lover": [  # Ama camera
            _("Film my pussy dripping with your cum... send me this later, I want to watch it again and again..."),

            _("Please tell me you got my pussy on camera when you came inside... that footage is gold..."),

            _("I want to see myself full of your cum on film... zoom in on my dripping pussy... perfect..."),

            _("Send me this video later. I want to see my pussy full of cum whenever I want..."),

            _("Record my pussy overflowing with your cum... this is the content my fans need..."),

        ],

        # --- Combos: consented + 2 traits ---
        "cum_inside_consented.hate_cum.boyfriend": [
            _("I hate cum... I have a boyfriend... and I just begged you to pump my pussy full... what is wrong with me..."),

            _("My boyfriend uses condoms and I hate cum... and here I am with another man's load dripping out of my pussy..."),

            _("I despise this feeling... your disgusting cum inside my cheating pussy... and I ASKED for it..."),

            _("I have a boyfriend and I hate cum in my pussy... so why is your hot load inside me right now... why did I beg..."),

        ],
        "cum_inside_consented.hate_cum.girlfriend": [
            _("I hate cum... I have a girlfriend... and I just begged you to pump my pussy full... what is wrong with me..."),

            _("My girlfriend would never do this to me and I hate cum... and here I am with your load dripping out..."),

            _("I despise this feeling... your disgusting cum inside me... and I ASKED for it..."),

            _("I have a girlfriend and I hate cum... so why is your hot load inside me right now... why did I beg for this..."),

        ],
        "cum_inside_consented.hate_cum.cheater": [
            _("I hate cum and I'm cheating on %(po)s... but my pussy is full of your load because I BEGGED for it... I'm losing my mind..."),

            _("Your disgusting cum inside my cheating pussy... I hate it... I hate that I asked for it... I hate that it feels so warm..."),

            _("I despise cum inside me and I'm behind %(poss)s back... but my pussy is squeezing every drop out of you... what have I become..."),

            _("I said fill me up... I HATE your cum... I'm cheating... my pussy is overflowing... why can't I stop asking for this..."),

        ],
        "cum_inside_consented.cheater.cum_slut": [
            _("That loser will never cum inside me like you... I belong to you, my pussy is only for your cum..."),

            _("My %(pl)s gets nothing. You get my pussy begging to be filled... every drop belongs inside me..."),

            _("I'm %(poss)s partner but my pussy is your cum dump... fill me again... %(pp)s could never make me beg like this..."),

            _("More... pump more cum in my cheating pussy... my %(pl)s will never know %(poss)s partner is a cum slut for you..."),

        ],
        "cum_inside_consented.boyfriend.cute": [
            _("I'm a terrible girlfriend... but your cum feels so warm inside my pussy... I wanted this so badly..."),

            _("He would be devastated if he knew I begged for this... your cum filling my little pussy... it feels so intimate..."),

            _("I have a boyfriend but your cum inside me feels so right... my pussy is so warm and full... hold me..."),

            _("I shouldn't have asked... but feeling your cum pump inside my pussy... with you it feels different... special..."),

        ],
        "cum_inside_consented.girlfriend.cute": [
            _("I shouldn't want this... but your cum feels so warm inside my pussy... I wanted this so badly..."),

            _("She would be devastated if she knew I begged for this... your cum filling my little pussy... it feels so intimate..."),

            _("I have a girlfriend but your cum inside me feels so right... my pussy is so warm and full... hold me..."),

            _("I shouldn't have asked for this... but feeling your cum pump inside my pussy... with you it feels different... special..."),

        ],
        "cum_inside_consented.cheater.hardcore": [
            _("Fill my cheating pussy to the brim. My %(pl)s could never make me feel this full of cum."),

            _("Behind %(poss)s back, raw, my pussy overflowing with your cum. This is how it should be. Every time."),

            _("Pump it all inside my pussy. %(Poss)s partner just got bred by a real man. No fucking regrets."),

            _("%(Poss)s partner just got her pussy destroyed and filled with cum. And I told you to do it. Harder next time."),

        ],
        "cum_inside_consented.hate_cum.cute": [
            _("I'm supposed to hate this... your cum inside my pussy... but with you I wanted it... it feels warm and right..."),

            _("I hate cum... but feeling you fill my little pussy... with you it's different... I actually asked for it..."),

            _("Why does your cum feel good inside me... I hate this feeling... but my pussy is holding onto every drop..."),

            _("I can't believe I asked... your cum is inside my pussy and I hate it... but I don't want it to stop dripping..."),

        ],

        # ── Post-creampie ANAL variants (consented) ──────────────
        "cum_inside_consented.anal": [
            _("Yesss... I feel all your cum inside my ass... so warm..."),

            _("Oh fuck... you filled my ass up so good... I can feel it deep..."),

            _("So much cum... I can feel it leaking out of my ass already... fuck..."),

            _("Mmmm... every drop inside my ass... I'm so full back there..."),

            _("I asked for it and I don't regret it... your cum feels so good in my ass..."),

        ],
        "cum_inside_consented.anal.cum_slut": [
            _("Yesss, fill my ass with every last drop... I need ALL of it inside me..."),

            _("Mmmm so much cum... my ass is overflowing... I want more..."),

            _("Don't you dare waste a single drop... my ass deserves every bit of your cum..."),

            _("Haha yesss... so much cum inside my ass... I can feel it dripping out..."),

            _("Your cum belongs inside my ass... give me everything..."),

        ],
        "cum_inside_consented.anal.hate_cum": [
            _("I hate cum in my ass... so why did I just beg you to fill me up... what's wrong with me..."),

            _("Your disgusting cum is inside my ass... and I ASKED for it... I can feel every drop... ugh..."),

            _("I told you to do it... I TOLD you to pump your cum in my ass... I'm disgusted with myself..."),

            _("My ass is full of your cum and I hate it... I hate that I begged for it... why is it so warm..."),

        ],
        "cum_inside_consented.anal.hate_cum.hc_tier1": [
            _("AGAIN?! My ass is full of your cum AGAIN and I ASKED for it! I hate your disgusting load inside me! ...So why did I beg TWICE?!"),

            _("TWICE I begged you to fill my ass! Your gross cum pumping inside me... I can feel it dripping... I HATE this!"),

            _("I said yes... again... your nasty cum flooding my ass for the second time... I hate how warm it feels..."),

        ],
        "cum_inside_consented.anal.hate_cum.hc_tier2": [
            _("I keep begging you to cum inside my ass! I HATE your cum! Your thick disgusting load dripping out of me... why can't I stop saying YES?!"),

            _("Fill my ass... I said FILL IT. I hate this! Your cum flooding inside me... my ass is overflowing with your nasty load and I KEEP ASKING!"),

            _("I'm disgusted... I keep begging for your cum inside my ass... it's so warm and thick and... I HATE IT! I hate that I want more!"),

        ],
        "cum_inside_consented.anal.hate_cum.hc_tier4": [
            _("Inside... pump it ALL inside my ass... I HATE your cum! I hate how much I need it! Your hot thick load filling me... UGH! JUST DO IT!"),

            _("I begged before you even started... your disgusting cum deep inside my ass... I hate that I NEED your load inside me now! What have you done to me?!"),

            _("Cum inside my ass... do it... I HATE it! I hate your cum! I hate that my ass squeezes every drop out of you! WHAT AM I BECOMING?!"),

        ],
        "cum_inside_consented.anal.cheater": [
            _("That loser will never cum inside my ass like you do... my ass belongs to you..."),

            _("I begged you to fill my ass while my %(pl)s thinks I'm being faithful... fuck..."),

            _("%(Poss)s partner just begged another man to pump her ass full of cum... and I'd do it again..."),

            _("My %(pl)s would never do this... and here I am dripping with your cum in my ass, asking for more..."),

            _("I'm going home to %(po)s with your cum still inside my ass... and I love it..."),

        ],
        "cum_inside_consented.anal.boyfriend": [
            _("My boyfriend... I just begged another man to flood my ass with cum..."),

            _("I have a boyfriend and your cum is dripping out of my ass... I asked for every drop..."),

            _("He can never know I begged you to fill my ass... oh god it feels so good..."),

            _("I'm such a bad girlfriend... your cum is so deep inside my ass and I wanted it all..."),

            _("My boyfriend would die if he knew I was begging for your cum inside my ass..."),

        ],
        "cum_inside_consented.anal.girlfriend": [
            _("My girlfriend... I just begged you to flood my ass with cum... what am I doing..."),

            _("I have a girlfriend and your cum is dripping out of my ass... I asked for every drop..."),

            _("She can never know I begged for this... she'd never understand..."),

            _("I'm supposed to only be with her... your cum is so deep inside my ass and I wanted it all..."),

            _("My girlfriend would die if she knew I was begging for your cum inside my ass..."),

        ],
        "cum_inside_consented.anal.cute": [
            _("It feels so warm inside me... your cum filling my ass... I feel so close to you..."),

            _("I wanted every single drop inside me... my ass feels so full and warm..."),

            _("That was so intimate... feeling your cum pump inside my ass... I never want this feeling to end..."),

            _("I can feel it all... so warm and deep... my ass is yours..."),

            _("Hold me like this... with your cum still inside my ass... it feels perfect..."),

        ],
        "cum_inside_consented.anal.hardcore": [
            _("Fuck yes. Pump every drop of cum deep in my ass. That's exactly what I needed."),

            _("Deeper. I want your cum so deep in my ass I'll feel it for days. No holding back."),

            _("That's what I fucking wanted. My ass full of your hot cum. More."),

            _("I asked for every drop and you delivered. My ass is overflowing. Perfect."),

        ],
        "cum_inside_consented.anal.femdom": [
            _("I told you to fill me up and you did. My ass is dripping. Good boy."),

            _("Good. I said in my ass, and you came exactly where I told you to."),

            _("Every drop in my ass, just like I ordered. You may rest now."),

        ],
        "cum_inside_consented.anal.virgin": [
            _("My first time doing anal and my ass is full of your cum... I can't believe I begged for it..."),

            _("I let you take my ass and asked you to fill it... who am I becoming..."),

            _("My first anal creampie... I can feel every drop inside me... oh god..."),

            _("I gave you my ass and then begged for cum inside on the first time... fuck..."),

            _("My ass just got filled with cum for the first time... I asked for this..."),

        ],
        "cum_inside_consented.anal.public_fetish": [
            _("I begged you to fill my ass right here where anyone could see... and it was incredible..."),

            _("Your cum dripping out of my ass in public... I asked for it and I'm so wet just thinking about it..."),

            _("Fill my ass up where everyone can see... let them watch your cum leak out of me..."),

            _("Creampied in my ass in public... anyone could notice... fuck I love this..."),

            _("I want everyone to see your cum running out of my ass... I begged for this..."),

        ],
        "cum_inside_consented.anal.public_shy": [
            _("Oh god... your cum is inside my ass HERE?! What if someone notices me walking funny?!"),

            _("I begged for it and now your cum is leaking out of my ass... in public... what's wrong with me..."),

            _("My ass is so full of your cum... if anyone looks they'll know something happened... oh no..."),

            _("I asked you to cum inside my ass where people could walk by... it's dripping... I need to clean up..."),

            _("Your cum is so warm inside my ass... please don't let it leak... not here..."),

        ],
        "cum_inside_consented.anal.camera_lover": [
            _("Film my ass dripping with your cum... send me this later, I want to watch it again and again..."),

            _("Please tell me you got my ass on camera when you came inside... that footage is gold..."),

            _("I want to see myself full of your cum on film... zoom in on my dripping ass... perfect..."),

            _("Send me this video later. I want to see my ass full of cum whenever I want..."),

            _("Record my ass overflowing with your cum... this is the content I need..."),

        ],

        # ── Forced creampie ANAL variants ──────────────
        "cum_inside_forced.anal": [
            _("You came inside my ass?! I didn't want that!"),

            _("You came inside my ass?! What the hell?!"),

            _("No! Not inside my ass! Oh god I can feel it..."),

        ],
        "cum_inside_forced.anal.hate_cum.hc_tier2": [
            _("STOP forcing your cum inside my ass! I HATE it! It's so warm and thick and... UGH! GROSS!"),

            _("How many times are you going to pump that disgusting load into my ass?! I can feel it EVERYWHERE!"),

            _("You keep FILLING my ass! Your nasty cum is overflowing inside me! I hate how much there is!"),

        ],
        "cum_inside_forced.anal.hate_cum.hc_tier4": [
            _("NOOOO! Not again! My ass is so full of your cum... your hot, thick... I HATE YOU! BASTARD!"),

            _("You WON'T stop! Your disgusting cum keeps pumping deep inside my ass! It's so... warm... I HATE IT!"),

            _("EVERY SINGLE TIME! You flood my ass with that thick cum! I can feel it throbbing in me! YOU'RE AWFUL!"),

        ],

        # --- Denied creampie request ---
        "cum_inside_denied.cute": [  # Negado + sexo carinhoso
            _("I'm scared... please don't do it inside..."),

            _("Not inside, okay? I'm not ready for that..."),

            _("Please be careful... pull out before..."),

        ],

        # ══════════════════════════════════════════════════════════
        #  CREAMPIE AFTERMATH — post-visual reaction (centralized)
        # ══════════════════════════════════════════════════════════

        # --- Consented: first time (base) ---
        "creampie_aftermath": [
            _("You came inside... are you happy?"),
            _("I can feel it inside me..."),
            _("It's so warm inside..."),
        ],
        "creampie_aftermath.cum_slut": [
            _("You... came inside... so deep... so warm... I love it so much..."),
            _("I can feel it all inside... it's so much... don't stop next time either..."),
            _("Mmm... every last drop... I can feel it all..."),
        ],
        "creampie_aftermath.hardcore": [
            _("Mmm... I can feel your cum inside me."),
            _("That's it... fill me up."),
        ],
        "creampie_aftermath.femdom": [
            _("You came inside? Good boy."),
            _("Look at it dripping out of me. You came because I let you, remember that."),
            _("Did I say you could pull out? Next time you stay in until I'm done."),
        ],
        "creampie_aftermath.cute": [
            _("Y-you came inside me... I felt it all..."),
            _("It's so warm inside... is that normal?"),
            _("I can feel every drop... it's a lot..."),
        ],
        "creampie_aftermath.hate_cum": [
            _("You came inside... ugh. This better not become a habit."),
            _("I can feel it all... gross. Just... gross."),
        ],
        "creampie_aftermath.boyfriend": [
            _("You came inside me... my %(pl)s can never find out about this."),
            _("I can feel your cum inside... %(pp)s would lose %(poss)s mind."),
        ],
        "creampie_aftermath.girlfriend": [
            _("You came inside me... %(pp)s never did that... a man just..."),
            _("I can feel your cum... this is so different from anything with %(po)s..."),
        ],

        # --- Consented: first creampie (first ever, combined with partner context) ---
        "creampie_aftermath.first_creampie": [
            _("That's my first time ever... with your cum inside me. I don't know how to feel."),
            _("I've never had anyone finish inside me before... it feels so different."),
            _("My first creampie... I always wondered what it would feel like."),
        ],
        "creampie_aftermath.first_creampie.boyfriend": [
            _("My first creampie... and it's not from my %(pl)s. I don't know what that says about me."),
            _("I've never let my %(pl)s do that. Not once. And I just let you... what am I doing?"),
            _("I should feel worse about this... my %(pl)s has never cum inside me. Not once."),
            _("My %(pl)s doesn't even know I'm here... and you just did something %(pp)s's never done."),
        ],
        "creampie_aftermath.first_creampie.girlfriend": [
            _("A man just came inside me for the first time. Something my %(pl)s could never do."),
            _("My %(pl)s can't... %(pp)s just can't... and I just let a man... what's wrong with me?"),
            _("Oh god... a man just came inside me. Something my %(pl)s could never do. And I craved it."),
            _("I've gone insane. I have a %(pl)s and I just let a man cum inside me."),
        ],
        "creampie_aftermath.first_creampie.cum_slut": [
            _("My first creampie ever... and you can do it whenever you want."),
            _("I've been saving this for someone who deserves it. Mmm... it feels amazing."),
        ],
        "creampie_aftermath.first_creampie.cheater": [
            _("My first creampie... and it's not from my partner. Lucky me."),
            _("My partner was supposed to have all my firsts. But YOUR cum is the first inside me."),
        ],
        "creampie_aftermath.first_creampie.virgin": [
            _("My first time... and you came inside me. I'm a mess right now."),
            _("I just lost my virginity AND got my first creampie... this is so much at once."),
        ],

        # --- Consented: anal variants ---
        "creampie_aftermath.anal": [
            _("You came in my ass... are you satisfied?"),
            _("I can feel it inside my ass..."),
        ],
        "creampie_aftermath.anal.cum_slut": [
            _("Mmm... I can feel every drop deep in my ass... don't stop..."),
            _("My ass is full of your cum... I love it..."),
        ],
        "creampie_aftermath.anal.hardcore": [
            _("Mmm... I can feel your cum deep in my ass."),
            _("Fuck... my ass is still throbbing, and now it's full of your cum."),
        ],
        "creampie_aftermath.anal.femdom": [
            _("You came in my ass? Good boy."),
            _("Look at it dripping out of my ass. You came because I let you, remember that."),
            _("Did I say you could pull out of my ass? Next time you stay in until I'm done."),
        ],
        "creampie_aftermath.anal.cute": [
            _("Y-you came in my butt... I felt it all go in..."),
            _("It's so warm inside my butt..."),
        ],
        "creampie_aftermath.anal.anal_hater": [
            _("You came in my ass... I hate that feeling..."),
            _("Ugh... I can feel it all in there... that's disgusting..."),
        ],

        # --- Consented: session_2nd ---
        "creampie_aftermath.session_2nd": [
            _("Twice inside... you couldn't help yourself, could you?"),
            _("I can feel it dripping already..."),
        ],
        "creampie_aftermath.session_2nd.cum_slut": [
            _("Again... yes... fill me up until I'm overflowing..."),
            _("More cum inside me... I can't get enough..."),
        ],
        "creampie_aftermath.session_2nd.hardcore": [
            _("Again? You really like cumming inside, don't you?"),
            _("Mmm... twice. I can feel every drop."),
        ],
        "creampie_aftermath.session_2nd.cute": [
            _("You... you did it again... inside..."),
            _("Twice?! What am I going to do..."),
        ],
        "creampie_aftermath.anal.session_2nd": [
            _("Twice in my ass... you couldn't help yourself, could you?"),
            _("I can feel it dripping out of my ass already..."),
        ],
        "creampie_aftermath.anal.session_2nd.hardcore": [
            _("Again in my ass? You really like that hole, don't you?"),
            _("Twice in my ass... I can feel every drop."),
        ],
        "creampie_aftermath.anal.session_2nd.cute": [
            _("You... you did it in my butt again..."),
            _("Twice in my butt?! It's so full..."),
        ],

        # --- Consented: session_3rd_plus ---
        "creampie_aftermath.session_3rd_plus": [
            _("Fuck... I let you cum inside so much..."),
            _("So much cum inside me... are you happy now?"),
        ],
        "creampie_aftermath.session_3rd_plus.cum_slut": [
            _("Keep going... I want to be completely full..."),
            _("More... I want so much cum inside me it leaks out..."),
        ],
        "creampie_aftermath.session_3rd_plus.hardcore": [
            _("Fuck... I can feel it all dripping out of me."),
            _("You really filled me up, didn't you?"),
        ],
        "creampie_aftermath.session_3rd_plus.cute": [
            _("T-there's so much... I can feel it leaking out..."),
            _("You came inside me so many times... what if something happens?"),
        ],
        "creampie_aftermath.anal.session_3rd_plus": [
            _("My ass is dripping with your cum... happy now?"),
            _("So much cum in my ass... you really didn't hold back."),
        ],
        "creampie_aftermath.anal.session_3rd_plus.hardcore": [
            _("Fuck... my ass is overflowing with your cum."),
            _("You really filled my ass up, didn't you?"),
        ],
        "creampie_aftermath.anal.session_3rd_plus.cute": [
            _("T-there's so much in my butt... I can feel it leaking out..."),
            _("You came in my butt so many times... I can't take any more..."),
        ],

        # --- Forced (not consented) ---
        "creampie_aftermath_forced": [
            _("You came inside?! What the hell is wrong with you?!"),
            _("I didn't say you could cum inside! Are you insane?!"),
        ],
        "creampie_aftermath_forced.cum_slut": [
            _("You... came inside... so deep... so warm... YOU HAVE TO WARN ME NEXT TIME!"),
            _("I can feel it all inside... it's so much... don't just DO that without asking!"),
        ],
        "creampie_aftermath_forced.hardcore": [
            _("You came inside without asking? Bold... but don't think I'll let that slide."),
            _("No permission, no warning... you've got nerve. I'll remember this."),
        ],
        "creampie_aftermath_forced.cute": [
            _("Y-you came inside me?! Without asking?! How could you do that?!"),
            _("I didn't say you could! What if... what if something happens?!"),
        ],
        "creampie_aftermath_forced.hate_cum": [
            _("You came inside me?! YOU DISGUSTING... I can feel it all! GET AWAY!"),
            _("NO! NOT INSIDE! I told you... ugh, I can feel it everywhere..."),
        ],
        "creampie_aftermath_forced.boyfriend": [
            _("You came inside without asking?! My %(pl)s... oh god, what did you do?!"),
            _("How could you just... inside?! %(Pp)s would kill you if %(pp)s knew!"),
        ],
        "creampie_aftermath_forced.girlfriend": [
            _("You came inside me?! A man just... without asking?! What the hell?!"),
            _("I didn't want that inside me! %(Pp)s never... no one has ever..."),
        ],

        # --- Forced: anal variants ---
        "creampie_aftermath_forced.anal": [
            _("You came in my ass?! What the hell is wrong with you?!"),
            _("I didn't say you could cum in my ass! Are you insane?!"),
        ],
        "creampie_aftermath_forced.anal.cum_slut": [
            _("You came in my ass without asking?! That's so... ugh, why does it feel so warm..."),
            _("I can feel it all deep inside my ass... YOU CAN'T JUST DO THAT!"),
        ],
        "creampie_aftermath_forced.anal.hardcore": [
            _("You came in my ass without asking? You've got nerve."),
            _("No warning, straight in my ass... bold. I'll remember that."),
        ],
        "creampie_aftermath_forced.anal.cute": [
            _("Y-you came in my butt?! Without asking?! I can feel it leaking..."),
            _("I didn't say you could do that in my... my butt! What is wrong with you?!"),
        ],
        "creampie_aftermath_forced.anal.anal_hater": [
            _("You came in my ASS?! I HATE that! Get it out... get it OUT!"),
            _("Not in my ass! Why would you... I can feel it all in there! DISGUSTING!"),
        ],

        # --- Forced: condom break aftermath (emotional processing after excuse arc) ---
        "creampie_aftermath_forced.condom_break": [
            _("The condom broke and you just... you just kept going. I can feel it all inside me."),
            _("A broken condom... your cum is inside me right now. This can't be happening."),
            _("I keep thinking about it... the condom was broken and you came inside me. Just like that."),
        ],
        "creampie_aftermath_forced.condom_break.boyfriend": [
            _("The condom broke... and my %(pl)s... oh god, what have I done? This can't be happening."),
            _("Your cum is inside me through a broken condom... and I have a %(pl)s. If %(pp)s finds out..."),
            _("A broken condom, your cum inside me, and I have to face my %(pl)s after this... I can't."),
        ],
        "creampie_aftermath_forced.condom_break.girlfriend": [
            _("A man just came inside me through a broken condom... and my %(pl)s... %(pp)s can never know."),
            _("The condom broke and a man filled me up... my %(pl)s would be devastated if %(pp)s knew."),
            _("Your cum is inside me... through a broken condom... my %(pl)s could never do this. And it wasn't even my choice."),
        ],
        "creampie_aftermath_forced.condom_break.cum_slut": [
            _("The condom broke and... honestly? I don't even care. It feels amazing in there."),
            _("Broken condom, cum inside... you know what? Forget the condom next time."),
        ],
        "creampie_aftermath_forced.condom_break.hate_cum": [
            _("The condom BROKE and you came INSIDE me?! I can feel ALL of it! This is a nightmare!"),
            _("Your disgusting cum is inside me because of a broken condom... I'm going to be sick."),
        ],
        "creampie_aftermath_forced.condom_break.hardcore": [
            _("Condom broke, cum inside... whatever. It happened. Not like I can undo it."),
            _("Broken condom or not, you still came inside without asking. Don't let it happen again."),
        ],

        # --- Forced: first creampie (forced, first ever + partner) ---
        "creampie_aftermath_forced.first_creampie": [
            _("My first creampie ever... and I didn't even say you could. What is wrong with you?!"),
            _("I've never had anyone cum inside me before... and you just did it without asking!"),
        ],
        "creampie_aftermath_forced.first_creampie.boyfriend": [
            _("My first creampie... forced... and my %(pl)s has never even done this. What have you done?!"),
            _("I've never let my %(pl)s cum inside me. And you just... without asking?! %(Pp)s can never know."),
            _("I can't believe you just forced that... my %(pl)s was supposed to be my first everything."),
        ],
        "creampie_aftermath_forced.first_creampie.girlfriend": [
            _("A man forced a creampie on me... my %(pl)s could never do this. And I didn't even consent!"),
            _("My first creampie ever... and I didn't even want it. My %(pl)s would be destroyed if %(pp)s knew."),
            _("You just came inside me without permission... something my %(pl)s could never even do."),
        ],

        # ══════════════════════════════════════════════════════════
        #  CUM OUTSIDE
        # ══════════════════════════════════════════════════════════

        "cum_outside": [  # Gozar fora — base
            _("Oh! It's everywhere..."),

            _("Wow... that was a lot."),

            _("You really needed that, huh?"),

        ],
        "cum_outside.lesbian": [  # Lesbian conflict
            _("Your cum is all over me... this is surreal."),

            _("You just came all over me. What is my life right now?"),

            _("Covered in your cum... if any of my exes could see me right now..."),

        ],
        "cum_outside.cowgirl": [  # Durante cowgirl
            _("Oh! All over my stomach..."),

            _("That's warm... wow."),

            _("It shot so far..."),

        ],
        "cum_outside.anal": [  # Cum fora durante anal
            _("Oh! It's all over my ass..."),

            _("I can feel it dripping down my cheeks..."),

            _("You covered my whole backside..."),

        ],
        "cum_outside.hj": [  # Durante handjob
            _("It's all over my hand..."),

            _("Wow... I made you do all that?"),

            _("That's a lot... it's still coming out..."),

        ],
        "cum_outside.tj": [  # Durante titjob
            _("Oh! All over my chest..."),

            _("It got on my chin too..."),

            _("Mmm... it's so warm on my skin..."),

        ],
        "cum_outside.cum_slut": [  # Garota adora cum
            _("Aw... you should've put it inside me."),

            _("What a waste... that should've been in me."),

            _("Next time, don't pull out."),

        ],
        "cum_outside.hate_cum": [  # Garota odeia cum
            _("Good. At least you kept it away from inside me."),

            _("Thank god you pulled out."),

            _("Clean that up. I don't want it on me."),

        ],
        "cum_outside.first_time": [  # Primeira vez
            _("Oh my god... there's so much..."),

            _("Is it always... this much?"),

            _("I've never seen... wow."),

        ],
        "cum_outside.boyfriend": [  # Garota tem namorado
            _("At least you didn't... inside... oh god, this is still bad..."),

            _("Quick, clean it up before anyone notices..."),

            _("I can't believe I let you..."),

        ],
        "cum_outside.girlfriend": [  # Garota tem namorada
            _("At least you didn't finish inside... she can never know about this..."),

            _("Quick, clean it up... if my girlfriend finds out..."),

            _("I can't believe I let you do this to me..."),

        ],
        "cum_outside.public": [  # Local publico
            _("Quick! Clean it before someone sees!"),

            _("Oh god, it's on my clothes..."),

            _("I need to wipe this before we go..."),

        ],
        "cum_outside.camera_hater": [
            _("At least you pulled out... and please tell me that's not on camera."),

            _("Good. Pull out AND no evidence. That's the only way."),

            _("At least no one filmed your cum all over me..."),

        ],
        "cum_outside.camera_lover": [
            _("Mmm... that looked so good. Did the camera catch the shot?"),

            _("Perfect angle. I hope you were filming that finish."),

            _("Did the camera get that? All your cum spraying out?"),

        ],
        "cum_outside.loyal": [
            _("At least you pulled out... god, I can't believe how badly I wanted that..."),

            _("Good... I already went insane letting it get this far..."),

            _("I love him but I'm covered in your cum right now..."),

        ],

        # ══════════════════════════════════════════════════════════
        #  CUM ON TITS
        # ══════════════════════════════════════════════════════════

        "cum_tits": [  # Gozar nos peitos — base
            _("It's all over my chest... wow."),

            _("That was a lot... it's dripping everywhere."),

            _("Right on my tits, huh? You liked the view?"),

        ],
        "cum_tits.lesbian": [  # Lesbian conflict
            _("My chest covered in... this is humiliating."),

            _("Dripping off my nipples... I never thought I'd let anyone do this..."),

            _("All over my tits... what would my exes say?"),

        ],
        "cum_tits.hj": [  # Durante handjob
            _("It went all the way up to my chest from there?!"),

            _("Your aim is... impressive. All over my tits."),

            _("Wow, it got everywhere... even on my nipples."),

        ],
        "cum_tits.tj": [  # Durante titjob
            _("Well, they were right there... I guess that was inevitable."),

            _("All over them... they're completely covered."),

            _("You really went off right between them..."),

        ],
        "cum_tits.cum_slut": [  # Garota adora cum
            _("Mmm... cover them. I love feeling it on my skin."),

            _("More... I want them completely glazed."),

            _("That's so hot... it's dripping off my nipples."),

        ],
        "cum_tits.hate_cum": [  # Garota odeia cum
            _("Ew! Not on my chest! Get me something to wipe with!"),

            _("That's disgusting... it's all over me."),

            _("You did that on purpose! Clean it up!"),

        ],
        "cum_tits.first_time": [  # Primeira vez
            _("Oh... it's on my chest... that's so warm."),

            _("I've never had someone... on me like that."),

            _("That was... unexpected. Is it always this much?"),

        ],
        "cum_tits.boyfriend": [  # Garota tem namorado
            _("He's never done this to my chest..."),

            _("If he could see me covered like this..."),

            _("Another man's cum on my tits... god, what am I doing."),

        ],
        "cum_tits.girlfriend": [  # Garota tem namorada
            _("She's never left anything like this on my chest..."),

            _("If she could see me covered like this..."),

            _("Your cum on my tits... god, what am I becoming."),

        ],
        "cum_tits.public": [  # Local publico
            _("Quick! It's on my chest! I can't go out like this!"),

            _("Oh god, it soaked through my top..."),

            _("Get me something to clean up before anyone sees!"),

        ],

        # ══════════════════════════════════════════════════════════
        #  CUM ON ASS
        # ══════════════════════════════════════════════════════════

        "cum_ass": [  # Gozar na bunda — base
            _("Oh! It's all over my ass..."),

            _("I can feel it dripping down..."),

            _("You really aimed back there, huh?"),

        ],
        "cum_ass.lesbian": [  # Lesbian conflict
            _("Your cum on my ass... nobody has ever left marks like this on me..."),

            _("I can feel it dripping down my cheeks... what am I doing..."),

            _("My ass covered in your cum... every part of me is losing this fight."),

        ],
        "cum_ass.cum_slut": [  # Garota adora cum
            _("Mmm... cover my ass. Mark your territory."),

            _("I love feeling it on my cheeks..."),

            _("You should've put it inside me instead..."),

        ],
        "cum_ass.hate_cum": [  # Garota odeia cum
            _("Ugh, it's on my ass. That's so gross."),

            _("Clean it up! I can feel it dripping!"),

            _("Why couldn't you just use a tissue or something?!"),

        ],
        "cum_ass.boyfriend": [
            _("All over my ass... he's never done anything like this to me..."),

            _("If he could see what's dripping down my cheeks right now..."),

            _("Another man's cum on my ass... god, what am I becoming."),

        ],
        "cum_ass.girlfriend": [
            _("All over my ass... she's never left marks like this on me..."),

            _("If she could see your cum dripping down my cheeks right now..."),

            _("Your cum on my ass... god, what would she think of me."),

        ],
        "cum_ass.public": [
            _("Oh god, it's all over my ass... I can't walk out like this!"),

            _("Quick, I need something to wipe with before someone comes!"),

            _("It's dripping down my legs... please help me clean up before anyone sees."),

        ],
        "cum_ass.loyal": [
            _("On my ass... the shame is burning. And so is the desire to do it again."),

            _("Your cum dripping down my cheeks... everything I stood for, gone."),

            _("I can feel it sliding down... I've lost every principle I ever had."),

        ],

        # ══════════════════════════════════════════════════════════
        #  CUM ON BACK
        # ══════════════════════════════════════════════════════════

        "cum_back": [  # Gozar nas costas — base
            _("I can feel it on my back... all warm."),

            _("You really just came all over my back..."),

            _("It's dripping down my spine..."),

        ],
        "cum_back.lesbian": [  # Lesbian conflict
            _("Your cum sliding down my back... nobody was ever this messy with me..."),

            _("I can feel it running down my spine... unreal."),

            _("All down my back... I never thought I'd end up like this."),

        ],
        "cum_back.cum_slut": [  # Garota adora cum
            _("Mmm... paint my back. I love being marked."),

            _("I can feel every drop... don't waste any."),

            _("That's so hot... I wish I could see it."),

        ],
        "cum_back.hate_cum": [  # Garota odeia cum
            _("Great. Now I need a shower for sure."),

            _("On my BACK? How am I supposed to clean that?!"),

            _("That's disgusting... I can feel it sliding down."),

        ],
        "cum_back.boyfriend": [
            _("On my back... he'd lose his mind if he saw the marks another man left."),

            _("Another man's cum running down my spine... I'll have to scrub this off before he touches me."),

            _("My boyfriend would cry if he could see my back right now."),

        ],
        "cum_back.girlfriend": [
            _("On my back... she'd lose her mind if she saw this."),

            _("Your cum running down my spine... I'll have to scrub this off before she touches me."),

            _("My girlfriend would cry if she could see my back right now."),

        ],
        "cum_back.public": [
            _("It's all over my back... I can FEEL it. How do I walk out?!"),

            _("Oh no, it's on my shirt... everyone will see the stain!"),

            _("I need to clean my back before anyone comes this way!"),

        ],

        # ══════════════════════════════════════════════════════════
        #  CUM ON BELLY
        # ══════════════════════════════════════════════════════════

        "cum_belly": [  # Gozar na barriga — base
            _("It's all over my stomach..."),

            _("Wow... there's a lot on my belly."),

            _("I can feel it pooling on my stomach..."),

        ],
        "cum_belly.lesbian": [  # Lesbian conflict
            _("Your cum pooling on my stomach... I wasn't supposed to end up like this."),

            _("I can feel it warm on my belly... this is my life now."),

            _("All over my stomach... nobody has ever left me looking like this."),

        ],
        "cum_belly.cowgirl": [  # Durante cowgirl
            _("You came right on my stomach while I was on top..."),

            _("I felt it shooting up onto my belly..."),

            _("I barely got off in time... it's everywhere."),

        ],
        "cum_belly.cum_slut": [  # Garota adora cum
            _("Mmm... I love watching it pool on my stomach."),

            _("That should've gone inside me, but this is hot too."),

            _("Look at all of it... you really needed that."),

        ],
        "cum_belly.hate_cum": [  # Garota odeia cum
            _("Ugh, it's all over my stomach. Get me a towel."),

            _("That's gross... it's getting everywhere."),

            _("At least it's not inside me... still disgusting though."),

        ],
        "cum_belly.boyfriend": [
            _("All over my stomach... he doesn't even know I let another man do this."),

            _("My boyfriend has no idea my belly is covered in someone else's..."),

            _("I'll have to shower before I see him... his girlfriend covered in another man's cum."),

        ],
        "cum_belly.girlfriend": [
            _("All over my stomach... she doesn't even know I'm doing this."),

            _("My girlfriend has no idea my belly is covered in your cum..."),

            _("I'll have to shower before I see her... she can never know about this."),

        ],
        "cum_belly.public": [
            _("Quick, pull my shirt down before someone sees my stomach!"),

            _("There's cum all over my belly... if someone walks in right now..."),

            _("Help me clean this up, I can't go out there with this on me!"),

        ],

        # ══════════════════════════════════════════════════════════
        #  CUM ON FACE
        # ══════════════════════════════════════════════════════════

        "cum_face": [  # Gozar no rosto — base
            _("Oh! My face... it's all over my face."),

            _("Wow... there's so much of it..."),

            _("You really aimed for my face, huh?"),

        ],
        "cum_face.lesbian": [  # Lesbian conflict
            _("Your cum on my face... if my ex saw me like this, she'd never stop talking."),

            _("All over my face... I don't even have words for how wrong this is."),

            _("My face... covered in cum. The girl who swore she'd never end up like this. Look at me now."),

        ],
        "cum_face.bj": [  # Durante blowjob
            _("You pulled out just to... oh! On my face?!"),

            _("It's still coming... there's so much..."),

            _("My eyes... don't get it in my eyes..."),

        ],
        "cum_face.hj": [  # Durante handjob
            _("It shot all the way up to my face!"),

            _("Oh! I wasn't expecting it to reach..."),

            _("That's so warm on my cheeks..."),

        ],
        "cum_face.cum_slut": [  # Garota adora cum
            _("Yes! Cover me! I love it!"),

            _("Mmm... I want to wear it all day..."),

            _("Paint my face... I'm your canvas..."),

        ],
        "cum_face.hate_cum": [  # Garota odeia cum
            _("EW! Not on my face! Get it off!"),

            _("That's disgusting! Why did you do that?!"),

            _("I TOLD you not on my face!"),

        ],
        "cum_face.first_time": [  # Primeira vez
            _("Oh my god... it's on my face... it's warm..."),

            _("I've never had someone... on my face before..."),

            _("That was... unexpected. Wow."),

        ],
        "cum_face.boyfriend": [  # Garota tem namorado
            _("He's never done this to me... oh my god..."),

            _("If he could see me right now... with your cum on my face..."),

            _("This is so wrong... but I kind of like it..."),

        ],
        "cum_face.girlfriend": [  # Garota tem namorada
            _("She's never... your cum on my face... oh my god..."),

            _("If she could see me right now... with your cum all over my face..."),

            _("This is so wrong... but I kind of like it..."),

        ],
        "cum_face.public": [  # Local publico
            _("Oh god, it's on my face! What if someone sees me?!"),

            _("I need a tissue NOW. I can't go out like this!"),

            _("Quick, wipe it off before anyone comes!"),

        ],
        "cum_face.camera_hater": [
            _("On my FACE?! If anyone photographed this moment I'll...!"),

            _("You better not have filmed that. My face is literally covered!"),

            _("Thank god... no evidence of your cum on my face..."),

        ],
        "cum_face.camera_lover": [
            _("All over my face... tell me you got that shot. It's perfect."),

            _("I bet my face looks incredible right now. Film it."),

            _("This facial needs to be on camera... I look incredible..."),

        ],
        "cum_face.loyal": [
            _("On my face... this is madness... and I wanted it so badly..."),

            _("I can't believe I let the desire take me this far... and I'd do it again..."),

            _("He'd never do this to me... your cum on my face..."),

        ],

        # ══════════════════════════════════════════════════════════
        #  CUM IN MOUTH
        # ══════════════════════════════════════════════════════════

        "cum_mouth": [  # Gozar na boca — base
            "Mmm...",
            _("That's... a lot. You were really pent up."),

            _("It's so thick..."),

        ],
        "cum_mouth.lesbian": [  # Lesbian conflict
            _("I have your cum in my mouth... and I swallowed it."),

            _("I just swallowed it. My entire world is collapsing in real time."),

            _("The taste... I was so sure I'd never know what this was like."),

        ],
        "cum_mouth.bj": [  # Durante blowjob
            _("Glk... mmm..."),

            _("Mmm... mmph..."),

            _("It keeps coming..."),

        ],
        "cum_mouth.cum_slut": [  # Garota adora cum
            _("Mmm... delicious. Can I have more?"),

            _("I love the taste..."),

            _("Give me every last drop..."),

        ],
        "cum_mouth.hate_cum": [  # Garota odeia cum
            _("Ugh... that's horrible!"),

            _("I need to spit this out... NOW."),

            _("You KNEW I hate this! Why?!"),

        ],
        "cum_mouth.first_time": [  # Primeira vez
            _("It's... salty. Warm. I wasn't ready for that."),

            _("I've never tasted... oh. Wow."),

            _("Is it... am I supposed to swallow?"),

        ],
        "cum_mouth.boyfriend": [  # Garota tem namorado
            _("I never let HIM do this..."),

            _("I can't believe I just swallowed another guy's..."),

            _("If he ever found out I did this..."),

        ],
        "cum_mouth.girlfriend": [  # Garota tem namorada
            _("She could never give me this... and I just swallowed it..."),

            _("I can't believe I just swallowed... she can never know..."),

            _("If she ever found out what was in my mouth..."),

        ],
        "cum_mouth.recurring": [  # Recorrente / ja fez antes
            _("Mmm... I'm starting to crave the taste..."),

            _("I know exactly how to get you off now..."),

            _("Just how I like it... warm and thick..."),

        ],
        "cum_mouth.camera_lover": [
            _("Mmm... tell me you filmed me swallowing. That footage is everything."),

            _("I hope the camera caught my expression... I bet I looked incredible."),

            _("Send me that clip later. My lips look amazing covered in your cum."),

        ],
        "cum_mouth.camera_hater": [
            _("If you filmed that... if anyone EVER sees my face with your cum... I'll kill you."),

            _("No evidence of this. None. Swear to me there's no recording."),

            _("Thank god no cameras were rolling... my mouth full of your..."),

        ],
        "cum_mouth.public": [
            _("I need to spit this out somewhere before people see my face..."),

            _("Oh god, I can taste it and people are nearby..."),

            _("Quick, hand me a tissue... someone could walk by any second."),

        ],
        "cum_mouth.loyal": [
            _("I just swallowed another man's cum... my values are nonexistent now..."),

            _("In my mouth... the taste of betraying everything I believed in..."),

            _("I let that happen... I wanted it... what kind of person does that make me?"),

        ],
        "cum_mouth.hardcore": [
            _("That's it. Harder next time. I can take more down my throat."),

            _("Good. More of that. Force-feed me."),

            _("That was nothing. Give me a real load next time."),

        ],
        "cum_mouth.cute": [
            _("That was... warm. You okay? I... I kind of liked it."),

            _("I can still taste you... it's kind of intimate, isn't it?"),

            _("You really let go in my mouth... I feel special that you trusted me."),

        ],

        # ══════════════════════════════════════════════════════════
        #  CUM IN MOUTH — ACCEPTED (she gives permission)
        # ══════════════════════════════════════════════════════════

        "cum_mouth_accepted": [  # Aceita gozar na boca — base
            _("Go ahead... do it. I'll take it."),

            _("Okay... cum in my mouth. I'm ready."),

            _("Give it to me... I'll swallow it all."),

        ],
        "cum_mouth_accepted.cum_slut": [  # Aceito + adora cum
            _("YES! In my mouth! I want every drop!"),

            _("Give it to me! I want to taste all of it!"),

            _("My mouth is open and ready... don't hold back!"),

        ],
        "cum_mouth_accepted.hate_cum": [  # Aceito + odeia cum
            _("Fine... in my mouth. But I'm spitting it out."),

            _("Okay, but don't expect me to enjoy it..."),

            _("If you have to... just get it over with."),

        ],
        "cum_mouth_accepted.cute": [  # Aceito + sexo carinhoso
            _("I... okay. I'll do it for you."),

            _("You want to? ...Okay. I trust you."),

            _("I'll try... just be gentle, okay?"),

        ],
        "cum_mouth_accepted.hardcore": [  # Aceito + sexo pesado
            _("Do it. Cum down my throat."),

            _("Give me that load. I can take it."),

            _("Shove it in deep and let go. I won't waste a drop."),

        ],
        "cum_mouth_accepted.nerd": [
            _("F-fine... but don't you dare tell anyone I did this..."),

            _("Okay... just... don't make a mess, please..."),

            _("I'll... swallow it. Just... don't look at me like that."),

        ],

        # ══════════════════════════════════════════════════════════
        #  CUM IN MOUTH — DENIED (she refuses)
        # ══════════════════════════════════════════════════════════

        "cum_mouth_denied": [  # Nega gozar na boca — base
            _("No way... not in my mouth."),

            _("Please don't... anywhere but my mouth."),

            _("I don't want that... pull out."),

        ],
        # Nothing is inside anyone in these scenes: no "pull out" (a tester got it in a handjob, 2026-10-10)
        "cum_mouth_denied.hj": [
            _("No way... not in my mouth. I'll finish you right here."),

            _("My mouth? No. My hand is doing just fine."),

            _("I don't want that near my mouth... you get my hand, nothing else."),

        ],
        "cum_mouth_denied.tj": [
            _("Not in my mouth... you have my tits, be grateful."),

            _("No. Finish where you are, not in my mouth."),

            _("My mouth stays closed... these will have to be enough."),

        ],
        "cum_mouth_denied.fj": [
            _("Not in my mouth... my feet are all you're getting tonight."),

            _("No. Finish on my feet, that was the deal."),

        ],
        "cum_mouth_denied.hate_cum": [  # Negado + odeia cum
            _("Absolutely NOT in my mouth! Are you insane?!"),

            _("I would NEVER let you do that! No!"),

            _("Don't you dare! Keep it away from my mouth!"),

        ],
        "cum_mouth_denied.cute": [  # Negado + sexo carinhoso
            _("I'm not ready for that... please don't."),

            _("That's too much for me... not in my mouth, okay?"),

            _("Maybe someday, but... not now. Please."),

        ],
        "cum_mouth_denied.nerd": [
            _("NOT in my mouth! That's disgusting!"),

            _("No! Pull it out, I don't want that in my mouth!"),

            _("Absolutely not! Anywhere else, just not my mouth!"),

        ],

        # ══════════════════════════════════════════════════════════
        #  CUM IN CONDOM
        # ══════════════════════════════════════════════════════════

        "cum_condom": [  # Gozou na camisinha — base
            _("Good thing you had that on."),

            _("That was smart... safety first."),

            _("I can see it through the condom... that's a lot."),

        ],
        "cum_condom.cum_slut": [  # Garota adora cum
            _("Ugh... I wish that was inside me instead."),

            _("What a waste of a perfectly good load..."),

            _("Take that thing off next time."),

        ],
        "cum_condom.hate_cum": [  # Garota odeia cum
            _("Thank god for that condom."),

            _("See? Isn't it better this way?"),

            _("Smart choice. I don't want that stuff on me."),

        ],
        "cum_condom.cowgirl": [  # Durante cowgirl
            _("I could feel you throbbing... even through it."),

            _("Mmm... I felt it swell up inside the condom..."),

            _("That was still good... even with the barrier."),

        ],
        "cum_condom.anal": [  # Camisinha durante anal
            _("Even with the condom... I could feel every throb in there..."),

            _("That was intense... even through the rubber..."),

            _("At least the condom kept it clean... back there..."),

        ],
        "cum_condom.first_time": [  # Primeira vez
            _("That was... interesting. I felt it even through the condom."),

            _("I'm glad we used protection, but... it was still amazing."),

            _("So that's what it feels like... even with a condom..."),

        ],

        # ══════════════════════════════════════════════════════════
        #  CONDOM FORCE REMOVE (girl removes without asking)
        # ══════════════════════════════════════════════════════════

        "condom_force": [  # Garota tira camisinha — base
            _("I can't take it anymore... I need to feel you."),

            _("This thing is coming off... I want you raw."),

            _("No more of this... I need you inside me properly."),

            _("I was wrong about the condom. I NEED to feel you. This is coming off."),

            _("Forget what I said. I need skin on skin. Right now."),

            _("I changed my mind. I can't do this with a barrier between us."),

            _("It's ok, big dicks like yours don't deserve a condom."),

        ],
        "condom_force.cowgirl": [  # Durante cowgirl
            _("I need to feel you pulsing inside me while I ride..."),

            _("I want your bare cock inside me... no more barriers."),

            _("Let me feel you properly... I'm taking this off."),

            _("I can't ride you properly with this thing on... it's coming off!"),

            _("I was wrong. I need to feel every inch while I'm on top."),

        ],
        "condom_force.cum_slut": [  # Garota adora cum
            _("I NEED your cum inside me. This thing is in the way."),

            _("How am I supposed to feel you properly with this on?"),

            _("This is coming off. I want every inch, every drop."),

            _("I can't STAND this condom! I need your cum INSIDE me, not trapped in plastic!"),

            _("What was I thinking?! This thing is blocking everything I want! Get it OFF!"),

        ],
        "condom_force.recurring": [  # Recorrente / ja fez antes
            _("We both know this is better without it..."),

            _("I'm tired of this barrier... we're past this."),

            _("You know how much better it feels raw..."),

            _("Why did I even ask for this? We both know we prefer it raw."),

        ],

        # ══════════════════════════════════════════════════════════
        #  CONDOM ASK REMOVE (girl asks permission)
        # ══════════════════════════════════════════════════════════

        "condom_ask": [  # Garota pede tirar camisinha
            _("Can we... take that off? I want to feel you..."),

            _("Do we really need that? I want you closer..."),

            _("I'd rather feel you without it... is that okay?"),

            _("I know I asked for it but... I changed my mind. Can we take it off?"),

            _("I was wrong about needing it. I want to feel the real thing."),

            _("Please take it off... I can't stop thinking about how much better it would feel without it."),

        ],
        "condom_ask.lesbian": [  # Lesbian conflict
            _("A condom? I never thought I'd need one... not with women, anyway..."),

            _("Take it off... I can't believe I'm asking for this, but here I am."),

            _("I never had to worry about this before... just take it off. I want to feel everything."),

        ],
        "condom_ask.cowgirl": [  # Durante cowgirl
            _("Can I take this off? I want to ride you properly..."),

            _("It feels different with it on... can we try without?"),

            _("I want to feel you bare inside me while I ride..."),

            _("I can't ride you like this... let me take it off. Please."),

            _("I want to feel every inch. This thing is driving me crazy. Can I take it off?"),

        ],
        "condom_ask.first_time": [  # Primeira vez
            _("I know we should be careful, but... I want to feel you."),

            _("For my first time... I want it to be real. No barrier."),

            _("Can we do it without? Just this once?"),

            _("I want my first time to be skin on skin. Please..."),

        ],
        "condom_ask.cum_slut": [  # Garota adora cum
            _("Take it off. I want to feel your cum inside me."),

            _("I can't cum properly with that on... please?"),

            _("I need to feel you raw. Take that off for me..."),

            _("I don't know why I even asked for it! I NEED to feel you! Take it off!"),

            _("This was a mistake. I want your cum INSIDE me. GET RID OF IT."),

        ],
        "condom_ask.recurring": [  # Recorrente / ja fez antes
            _("We've done it raw before... let's do it again."),

            _("You know I like it better without that thing."),

            _("We both know we want to take that off..."),

            _("Why do we keep pretending? We both know the condom doesn't last."),

        ],
        "condom_ask.boyfriend": [  # Garota tem namorado (generico)
            _("I know it's risky... but I want to feel you. Really feel you."),

            _("Take it off... I want something I can't have with him."),

            _("I shouldn't even be doing this... but take it off."),

            _("My boyfriend would never let me do this... but I want it. Take it off."),

        ],
        "condom_ask.girlfriend": [  # Garota tem namorada
            _("I know it's wrong... but I want to feel you raw. She could never give me this."),

            _("Take it off... I want something she can never give me."),

            _("I shouldn't even be doing this... but take it off. I need to feel it."),

            _("My girlfriend would lose her mind... but I want you raw inside me. Take it off."),

        ],
        "condom_ask.girlfriend_sex": [  # Garota fez sexo com namorada
            _("She can't do what you can do... take it off, I want to feel it."),

            _("My girlfriend never... I've never felt a man raw before. I want to."),

            _("Take it off... this is already so wrong. Might as well go all the way."),

        ],
        "condom_ask.boyfriend_sex": [  # Garota fez sexo com namorado
            _("I never asked HIM to take it off, but... with you I want to."),

            _("I know it's risky... but I want to feel you. Really feel you."),

            _("Take it off... I want something I can't have with him."),

            _("He always uses one. But with you? I want to feel the difference."),

        ],

        # ══════════════════════════════════════════════════════════
        #  CONDOM — DENIED REACTION
        # ══════════════════════════════════════════════════════════

        "condom_denied": [  # Pedido de tirar negado — base
            _("Fine... but I really wanted to feel you."),

            _("Okay... maybe next time."),

            _("Alright... I understand."),

        ],
        "condom_denied.cum_slut": [  # Negado + adora cum
            _("Ugh... fine. But I WILL feel you raw someday."),

            _("You're killing me... I need it without that thing."),

            _("This is torture... but fine."),

        ],
        "condom_denied.first_time": [  # Negado + primeira vez
            _("You're right... we should be safe. I'm sorry."),

            _("Okay... I got carried away. Let's keep it on."),

            _("Maybe it's better this way... for now."),

        ],

        # ══════════════════════════════════════════════════════════
        #  CREAMPIE REQUEST
        # ══════════════════════════════════════════════════════════

        "creampie_req": [  # Garota pede creampie — base
            _("I want you to finish inside me..."),

            _("Don't pull out... please..."),

            _("Fill me up... I need it..."),

            _("Promise me you'll cum inside..."),

        ],
        "creampie_req.lesbian": [  # Lesbian conflict
            _("This is so wrong... but don't pull out."),

            _("Fill me up... I never thought I'd ask for this. Never in a million years."),

            _("Cum inside me... my whole world is upside down."),

        ],
        "creampie_req.cowgirl": [  # Durante cowgirl
            _("When you're ready... cum inside me while I ride you."),

            _("I want to feel you fill me while I'm on top..."),

            _("Don't even think about pulling out... I want it deep."),

        ],
        "creampie_req.cum_slut": [  # Garota adora cum
            _("I NEED your cum inside me. Every. Last. Drop."),

            _("Fill me to the brim... I want to be overflowing."),

            _("Breed me... I want to feel full of you."),

        ],
        "creampie_req.recurring": [  # Recorrente / ja fez antes
            _("You know where I want it..."),

            _("Same as always... inside. Where it belongs."),

            _("Don't make me beg again. You know what I want."),

        ],
        "creampie_req.boyfriend": [  # Garota tem namorado
            _("He always pulls out... but I want YOU to cum inside me."),

            _("Do what he never does... fill me up."),

            _("Give me something he could never give..."),

        ],
        "creampie_req.girlfriend": [  # Garota tem namorada (lesbian conflict)
            _("She could never fill me up like this... but you can. Cum inside me."),

            _("Do what no woman can do... fill my pussy with your cum."),

            _("Give me something she could never give... a real creampie."),

        ],

        # ══════════════════════════════════════════════════════════
        #  POSITION SUGGEST — COWGIRL
        # ══════════════════════════════════════════════════════════

        "pos_cowgirl": [  # Sugere cowgirl — base
            _("Let me ride you... I want to be on top."),

            _("Can I get on top? I want to control the pace..."),

            _("I want to ride you... let me climb on."),

        ],
        "pos_cowgirl.lesbian": [  # Lesbian conflict
            _("You want me on top? ...I can't believe I'm considering this."),

            _("Let me ride you... the irony is killing me."),

            _("Fine, I'll get on top... at least I can control the pace."),

        ],
        "pos_cowgirl.hardcore": [  # Sexo intenso/pesado
            _("I want to be on top. I'm going to ride you hard and fast."),

            _("Let me ride you... I want to feel every inch slamming into me."),

            _("Switch with me... I want to bounce on your cock until my legs give out."),

        ],
        "pos_cowgirl.femdom": [
            _("Get on your back. I'm going to ride you into the mattress."),

            _("Let me on top. I'll show you how I like it."),

            _("Lay down. I'm taking over."),

        ],
        "pos_cowgirl.cute": [  # Sexo gentil/carinhoso
            _("Can I be on top? I want to look at your face..."),

            _("Let me ride you gently... I want to see your eyes..."),

            _("I feel closer to you when I'm on top..."),

        ],
        "pos_cowgirl.cum_slut": [  # Garota adora cum
            _("Let me ride your cock... I need to be in control of how deep it goes."),

            _("I want to grind on you until you fill me up..."),

            _("Get on your back. I know exactly how to make us both cum."),

        ],
        "pos_cowgirl.boyfriend": [
            _("Let me ride you... he's never let me be on top like this..."),

            _("I want to be in control... my boyfriend never gives me that..."),

            _("Let me climb on top... I want something he never gives me."),

        ],
        "pos_cowgirl.girlfriend": [  # Garota tem namorada
            _("Let me ride you... she'd lose her mind if she saw this..."),

            _("I want to be on top... I need to feel what she can never give me..."),

            _("Let me climb on top... I want something she's never given me."),

        ],
        "pos_cowgirl.public": [
            _("Let me get on top... I can hide what we're doing better from up there..."),

            _("If I'm riding you, I can see if someone's coming..."),

            _("On top... I'll keep watch while we..."),

        ],
        "pos_cowgirl.first_time": [
            _("Can I... be on top? I've never tried but I want to control how deep..."),

            _("Let me try being on top... I'm scared but I want to set the pace."),

            _("I've never ridden anyone before... let me try? Go slow."),

        ],

        # ══════════════════════════════════════════════════════════
        #  POSITION SUGGEST — RCG
        # ══════════════════════════════════════════════════════════

        # ══════════════════════════════════════════════════════════
        #  POSITION — DENIED REACTION
        # ══════════════════════════════════════════════════════════

        "pos_denied": [  # Posicao negada — base
            _("Okay... this is good too."),

            _("Fine... I like this position anyway."),

            _("Alright... keep going then."),

        ],
        "pos_denied.lesbian": [  # Lesbian conflict
            _("No. I'm already doing more than I ever imagined. That's enough."),

            _("Absolutely not. I have to draw the line somewhere."),

            _("No... I'm already questioning everything about myself. Let's not add more to the list."),

        ],
        "pos_denied.hardcore": [  # Sexo intenso/pesado
            _("Fine. But you owe me my favorite position later."),

            _("Your loss..."),

        ],
        "pos_denied.femdom": [
            _("Ugh... okay. But don't blame me if I get bossy."),

            _("Fine. I'll let you have this one. Just this once."),

            _("You're telling ME no? Cute. Next time I won't be asking."),

        ],
        "pos_denied.cute": [  # Sexo gentil/carinhoso
            _("That's okay... I'm happy like this with you."),

            _("Alright... just hold me closer then."),

            _("Mmm... this is nice too. I don't mind."),

        ],
        "pos_denied.cum_slut": [
            _("Fine... but you better still cum for me in this position."),

            _("Whatever... as long as I still get what I want at the end."),

            _("Ugh... I had plans for that position. You'd better make this one worth it."),

        ],
        "pos_denied.boyfriend": [
            _("Maybe it's better this way... less to confess about."),

            _("Okay... one less thing I have to feel guilty about trying."),

            _("Fine. At least I didn't add another position to the list of things I've done behind his back."),

        ],
        "pos_denied.girlfriend": [  # Garota tem namorada (lesbian conflict)
            _("Maybe it's better this way... less to explain if she ever finds out."),

            _("Okay... one less position I tried with a man behind her back."),

            _("Fine. At least I didn't go even further from who I'm supposed to be."),

        ],
        "pos_denied.loyal": [
            _("That's okay... this is already more than I should be doing."),

            _("Maybe it's for the best... I've already crossed too many lines."),

            _("Fine... the less I try, the less I have to hate myself for."),

        ],

        # ══════════════════════════════════════════════════════════
        #  PACE — FASTER REQUEST
        # ══════════════════════════════════════════════════════════

        "pace_faster": [  # Pede mais rapido — base
            _("Faster... please go faster..."),

            _("Harder... don't hold back..."),

            _("More... I need more..."),

        ],
        "pace_faster.cowgirl": [  # Durante cowgirl
            _("I'm going to ride faster... hold on..."),

            _("Let me pick up the pace..."),

            _("I need to go harder... can you keep up?"),

        ],
        "pace_faster.hj": [  # Durante handjob
            _("Let me stroke you faster..."),

            _("I want to speed up... can you handle it?"),

            _("Faster... I want to see you lose control..."),

        ],
        "pace_faster.bj": [  # Durante blowjob
            _("Mmm... I want to go faster..."),

            _("Let me... mmph... speed up..."),

            _("I'm going to take you deeper..."),

        ],
        "pace_faster.tj": [  # Durante titjob
            _("Let me move them faster..."),

            _("I want to go harder..."),

            _("Faster... I want you to cum between them..."),

        ],
        "pace_faster.hardcore": [  # Sexo intenso/pesado
            _("Faster! What are you waiting for?!"),

            _("Come on! Fuck me like you mean it!"),

            _("Is that the best you can do?! Harder!"),

        ],
        "pace_faster.cum_slut": [  # Garota adora cum
            _("Faster! I want to feel you EXPLODE inside me!"),

            _("Don't hold back! I want every ounce of your energy!"),

            _("Harder! Make me scream!"),

        ],

        # ══════════════════════════════════════════════════════════
        #  PACE — SLOWER REQUEST
        # ══════════════════════════════════════════════════════════

        "pace_slower": [  # Pede mais devagar — base
            _("Slow down... take your time with me..."),

            _("Easy... let's enjoy this..."),

            _("Gentle... be gentle with me..."),

        ],
        "pace_slower.cowgirl": [  # Durante cowgirl
            _("Let me slow down... I want to feel every movement..."),

            _("Easy... let me grind slowly on you..."),

            _("No rush... I want to savor this..."),

        ],
        "pace_slower.hj": [  # Durante handjob
            _("Let me slow my hand... enjoy the sensation..."),

            _("Easy... let me tease you a bit..."),

            _("Slow strokes... feel everything..."),

        ],
        "pace_slower.bj": [  # Durante blowjob
            _("Mmm... let me take my time with you..."),

            _("Slowly... I want to savor you..."),

            _("No rush... let me worship you..."),

        ],
        "pace_slower.tj": [  # Durante titjob
            _("Slowly... let me squeeze them tighter..."),

            _("Easy... feel them against you..."),

            _("No rush... let my chest do the work..."),

        ],
        "pace_slower.cute": [  # Sexo gentil/carinhoso
            _("Please... slow and sweet. I want to feel everything."),

            _("Hold me and go slow... this is perfect..."),

            _("Don't rush... I want this to last forever..."),

        ],
        "pace_slower.first_time": [  # Primeira vez
            _("Please slow down... I'm still getting used to this..."),

            _("It's a lot... can we go easier?"),

            _("Gentle... please... it's my first time..."),

        ],

        # ══════════════════════════════════════════════════════════
        #  PACE — OBEYED / IGNORED REACTIONS
        # ══════════════════════════════════════════════════════════

        "pace_obeyed": [  # Ritmo obedecido — base
            _("Mmm... yes, just like that..."),

            _("That's perfect..."),

            _("Yes... exactly what I needed..."),

        ],
        "pace_obeyed.cute": [  # Sexo gentil/carinhoso
            _("Thank you... this is so much better..."),

            _("You listen to me... I love that about you..."),

            _("Perfect... just perfect..."),

        ],
        "pace_obeyed.hardcore": [  # Sexo intenso/pesado
            _("THAT'S more like it!"),

            _("Finally! Now we're talking!"),

            _("Yes! That's the pace I need!"),

        ],

        "pace_ignored_1": [  # Ritmo ignorado (1o aviso)
            _("Hey... I said..."),

            _("Did you hear me...?"),

            _("I asked you to..."),

        ],
        "pace_ignored_2": [  # Ritmo ignorado (2o aviso)
            _("You never listen to me..."),

            _("Fine... do whatever you want."),

            _("I guess my opinion doesn't matter..."),

        ],
        "pace_ignored_1.cute": [  # 1o aviso + sexo carinhoso
            _("Please... I really meant it..."),

            _("Are you ignoring me on purpose...?"),

            _("I thought you'd listen..."),

        ],
        "pace_ignored_2.cute": [  # 2o aviso + sexo carinhoso
            _("You're hurting my feelings..."),

            _("I trusted you to listen..."),

            _("Maybe we should stop if you won't listen to me..."),

        ],
        "pace_ignored_1.hardcore": [  # 1o aviso + sexo pesado
            _("Did you just... ignore me?"),

            _("I know what I want. Listen."),

            _("Excuse me? I SAID..."),

        ],
        "pace_ignored_2.hardcore": [  # 2o aviso + sexo pesado
            _("You'll regret ignoring me."),

            _("Whatever. But this isn't over."),

        ],
        "pace_ignored_2.femdom": [
            _("Fine. Remember this when it's MY turn to decide."),

            _("Twice now. You'll learn to do what I tell you, one way or another."),

            _("I set the pace, not you. Keep this up and you won't be allowed to cum."),

        ],

        # ============================================================
        # ANAL_LOVER trait lines
        # ============================================================

        # — Moans —
        "moan.speed1.anal.anal_lover": [
            _("Mmm... yes... right there in my ass... don't rush it..."),

            _("God I love this... keep going, just like that..."),

            _("Yesss... I've been craving this... my ass is all yours..."),

        ],
        "moan.speed2.anal.anal_lover": [
            _("Fuck yes... deeper in my ass... that's perfect..."),

            _("Harder... I can take it... my ass loves your cock..."),

            _("Oh god... this is exactly what I needed... don't hold back..."),

        ],
        "moan.speed3.anal.anal_lover": [
            _("Yes! Fuck my ass! God, this feels even better than pussy!"),

            _("Harder! Deeper! My ass was made for your cock!"),

            _("Oh god yes! Don't stop! My ass can take everything you've got!"),

        ],

        # — Girl orgasm —
        "girl_cum.anal.tenny": [
            _("That was... different than I expected. It still proves nothing though."),

            _("Okay, I... that happened. It doesn't mean anything."),

            _("Hmph... fine, it wasn't terrible. But that's not the point."),

        ],
        "girl_cum.anal.tenny.anal_lover": [
            _("That's... no. There's no mechanism for women to... but I just... why?"),

            _("I shouldn't have... the nerve endings aren't even... how did that feel so good?"),

            _("Every study says this shouldn't happen to women... so what just happened to me?"),

        ],
        "girl_cum.anal.anal_lover": [
            _("I'm cumming! From my ass! Yes! This is amazing! Aaah!"),

            _("Oh god... here it comes... my ass is making me... aaah! Yes!"),

            _("Yes! Fuck my ass! It feels so much better than my pussy! Aaah!"),

        ],
        "girl_cum.anal.anal_lover.cute": [
            _("It's too much... I'm so full... you're so deep inside... I'm cumming... I'm cumming from my ass!"),

            _("You're stretching me out... it's too good... I can't stop it... I'm going to... aaah!"),

            _("I didn't think I could... from back there... but it's happening... oh god... aaah!"),

        ],
        "girl_cum.anal.anal_lover.hardcore": [
            _("Deeper! Force it all the way up there! Split me apart! Oh shit! I'm gonna cum! AAAH!"),

            _("HARDER! MY ASS CAN TAKE EVERYTHING YOU'VE GOT! I'M CUMMING! FUUUCK!"),

        ],
        "girl_cum.anal.anal_lover.submissive": [
            _("Keep going! Use me harder! Destroy my fucking ass! I'm almost there... FUCK!"),

            _("My ass is yours! Use it! Use it until I... I'M CUMMING! AAAH!"),

            _("Take my ass however you want! It's yours! I'm... I'm CUMMING! FUUUCK!"),

        ],
        "girl_post_cum.anal.anal_lover": [
            _("Whew. Anal orgasms hit different... don't you dare stop."),

            _("See? I told you my ass was special. That was amazing."),

            _("I could do this all day... my ass is still tingling..."),

        ],
        "girl_post_cum.anal.anal_lover.cute": [
            _("I'm glad I trusted you with this..."),

            _("You made me feel so good... like this... I'm glad..."),

            _("I can't believe I came from that... but I'm not sorry it happened..."),

        ],
        "girl_post_cum.anal.anal_lover.hardcore": [
            _("Fuck. Yes. That was so good. Assgasms are better when you can't sit down tomorrow... don't stop. You can do better than just tomorrow!"),

            _("So awesome! I'm gonna be walking so funny after this... No! Don't stop! I don't want to be able to walk at all!"),

        ],

        # — Creampie —
        "cum_inside.anal.anal_lover": [
            _("Yes... fill my ass up... I want every drop in there..."),

            _("Oh god... I can feel it pumping deep inside my ass... perfect..."),

            _("Mmm... cum inside my ass... that's exactly where it belongs..."),

        ],
        "cum_inside_accepted.anal.anal_lover": [
            _("Inside my ass? Obviously. Where else would you put it?"),

            _("Yes! Cum deep in my ass! I want to feel it all!"),

            _("Fill me up. My ass is hungry for it."),

        ],
        "cum_inside_consented.anal.anal_lover": [
            _("Yesss... every drop deep in my ass... I'm in heaven..."),

            _("My ass is so full of your cum... I love this feeling so much..."),

            _("Mmmm... that warmth inside my ass... I could get addicted to this..."),

            _("Don't pull out yet... I want to feel your cum inside my ass a little longer..."),

        ],
        "cum_inside_forced.anal.anal_lover": [
            _("You came inside my ass without asking? ...Good. That's where I wanted it anyway."),

            _("Oh... you just filled my ass... I was going to beg you to do that~"),

            _("Mmm... forced or not, cum inside my ass always feels incredible..."),

        ],
        "cum_inside_forced.anal.cum_slut": [
            _("You came inside my ass? I said no but... god it feels so warm in there..."),

            _("I told you not to... but feeling your cum fill my ass... I can't be mad about that."),

            _("You didn't listen... but now that it's inside me, I don't want you to pull out yet."),

        ],
        "cum_inside_denied.anal.anal_lover": [
            _("Not inside... save it for next time. I want to make you earn my ass."),

            _("Pull out... I want your cum somewhere I can see it this time."),

            _("Not yet... I want to keep going with your cock in my ass a bit longer..."),

        ],

        # — Recording —
        "record_accepted.anal.anal_lover": [
            _("Film my ass taking your cock? Absolutely. I want to watch this later."),

            _("Record it. I want proof of how much I love anal."),

            _("Yes! Capture every second. My ass is the star of this show."),

        ],
        "record_accepted.anal.anal_lover.camera_lover": [
            _("Anal AND on camera?! This is the best day of my life! Film everything!"),

            _("Get the angle right! I want to see how my ass looks taking you on film~"),

            _("This is going to be the hottest video ever. My ass, your cock, all on camera!"),

        ],
        "record_accepted.anal.anal_lover.camera_hater": [
            _("I love what you're doing to my ass but... does the camera have to be on?"),

            _("Fine... film it. But only because anal feels too good to stop over a camera."),

            _("Ugh, I hate being filmed... but I love this too much to say no right now."),

        ],

        # — SubEvent: anal_lover requests anal (any position it runs in: doggy, laying down, full nelson) —
        "anal_request": [
            _("Hey... what about my ass? I really want you back there..."),

            _("Can you... put it in my ass instead? Please?"),

            _("My ass is begging for attention... switch?"),

        ],
        "anal_request.anal_lover": [
            _("Put it in my ass. I need it there. Now."),

            _("My ass is aching for your cock... please switch..."),

            _("I can't take it anymore... I need you in my ass. Please."),

        ],
        "anal_request_accepted": [
            _("Yesss... that's what I wanted... thank you..."),

            _("Finally... my ass is so happy right now..."),

            _("Oh god... yes... right where I need it..."),

        ],
        "anal_request_declined": [
            _("Fine... but you're missing out on the best part of me..."),

            _("Ugh... okay. But next time, my ass gets its turn."),

            _("You're really going to leave my ass hanging? ...Fine."),

        ],

        # ============================================================
        # ANAL PREFERENCE — progressive preference pools
        # ============================================================

        "anal_pref_curious": [
            _("That was... really good. Better than I expected."),

            _("Wow... I didn't think I'd like that so much."),

            _("Okay, I'll admit it... that felt amazing back there."),

        ],

        "vaginal_complaint": [
            _("This feels good, but you know where I really want it..."),

            _("Mmm... imagine how much better this would feel in my ass..."),

            _("Not bad... but you know my ass would feel even better."),

        ],
        "vaginal_complaint.hardcore": [
            _("Why are you wasting time here? My ass is RIGHT THERE."),

            _("Seriously? You have my ass available and you choose THIS?"),

        ],
        "vaginal_complaint.cute": [
            _("I mean... this is nice... but, um... the other hole is nicer..."),

            _("Sorry, I just... I keep thinking about how good it feels back there..."),

        ],
        "vaginal_complaint.cum_slut": [
            _("Come on, you know my ass grips you way tighter than this..."),

            _("Don't tease me... you know where I want that load..."),

        ],

        "vaginal_complaint_addicted": [
            _("You KNOW I prefer it the other way... why are you doing this to me?"),

            _("My ass is literally right there and you're ignoring it? Really?"),

            _("Fine, I guess. But don't expect me to enjoy this as much."),

        ],

        "scene_end_anal_satisfied": [
            _("That was exactly what I needed. My ass thanks you."),

            _("See? THIS is how it should always be. Perfect."),

            _("God... every time you do that, it just gets better."),

        ],

        # ============================================================
        # ANAL_HATER trait lines (generic fallback)
        # ============================================================

        # — Moans —
        "moan.speed1.anal.anal_hater": [
            _("Ow... it hurts... everything hurts back there..."),

            _("This is awful... why did I agree to this..."),

            _("It stings... please be careful... ow..."),

            _("I hate this... I hate every second of this..."),

        ],
        "moan.speed2.anal.anal_hater": [
            _("OW! It's too much... my ass can't handle this..."),

            _("It burns... please... this is the worst..."),

            _("Why does it hurt so much... I can't do this..."),

            _("Make it end... please just finish already..."),

        ],
        "moan.speed3.anal.anal_hater": [
            _("OW OW OW! You're tearing me apart back there!"),

            _("It's DESTROYING me! Please! I can't take much more!"),

            _("My ass is BROKEN! This is the worst pain I've ever felt!"),

            _("PLEASE! Just cum already! I can't handle this!"),

        ],

        # — Creampie —
        "cum_inside.anal.anal_hater": [
            _("You came inside my ass?! Great, now it hurts AND it's full of your cum..."),

            _("Oh perfect... cum in the hole that already hurts the most... wonderful..."),

            _("I can feel it inside my aching ass... this whole experience was miserable..."),

        ],
        "cum_inside_accepted.anal.anal_hater": [
            _("Fine... just finish inside and end this nightmare already..."),

            _("In my ass... whatever. It can't get any worse. Just do it."),

            _("Just cum and get out of my ass. I want this over."),

        ],
        "cum_inside_denied.anal.anal_hater": [
            _("Absolutely NOT in my ass! Pull out! My ass has suffered enough!"),

            _("If you cum inside my ass I swear I'll never speak to you again!"),

            _("Pull out of my ass RIGHT NOW. I will not let you finish in there."),

        ],
        "cum_inside_forced.anal.anal_hater": [
            _("You came inside my ASS?! After everything you put me through?! I HATE you!"),

            _("I told you not inside! My ass is in agony AND full of your cum! Monster!"),

            _("Great. Just great. My ass hurts AND you filled it with cum. Worst day ever."),

        ],
        "cum_inside_consented.anal.anal_hater": [
            _("I said yes to cum in my ass... why... it hurts so much and now it's full..."),

            _("My ass is aching and overflowing... I agreed to this... what is wrong with me..."),

            _("Every drop in my sore ass... I consented to this misery somehow..."),

        ],

        # ============================================================
        # ANAL_HATER + HARDCORE (dual-trait: overwhelmed pleasure)
        # ============================================================

        "moan.speed1.anal.anal_hater.hardcore": [
            _("Ow... it hurts... but... there's something... underneath the pain..."),

            _("This shouldn't feel... why is there... ugh... it stings but..."),

            _("I hate this... I HATE this... so why won't my body listen..."),

        ],
        "moan.speed2.anal.anal_hater.hardcore": [
            _("You're too deep... This Hurts... So Good..."),

            _("Your cock is too big for my ass... Fuck..."),

            _("I hate how deep you are... but my body is... responding... damn it..."),

        ],
        "moan.speed3.anal.anal_hater.hardcore": [
            _("Holy fucking shit..."),

            _("Ah... Slow Down... Please... Wait... Ahh... Fuck why does this feel good."),

            _("My ass is on FIRE and I'm... I'm actually... what is happening to me..."),

        ],

        "girl_cum.anal.anal_hater.hardcore": [
            _("Too deep... too fast... I'm gonna fucking cum. I'm going to..."),

            _("I HATE this! I hate it! So WHY am I... oh god... I'm... AAAH!"),

            _("My ass is screaming and I'm about to... from THIS?! AAAH! FUCK!"),

        ],
        "girl_cum.anal.anal_hater": [
            _("Wait... no... I'm not supposed to... from THERE?! AAAH!"),

            _("How?! I HATE this! How am I... oh god I'm actually... AAAH!"),

            _("This can't be happening... I didn't think I could ever... from my ass?! AAAH!"),

        ],
        "girl_post_cum.anal.anal_hater": [
            _("I came from anal. I didn't even think that was possible for me..."),

            _("You're still going to have to clean it before we do anything else."),

            _("That... was not supposed to happen. I HATE having it back there and I just..."),

            _("I can't believe my body just did that. I hate this. I hate that it felt good."),

            _("Okay... wow... You're still too big for this... But that's making it feel nice as well..."),

            _("God that was good... It's so strange... It still hurts a bit... And that's making it feel good too..."),

        ],
        "girl_post_cum.anal.anal_hater.hardcore": [
            _("You're so goddamn lucky that it felt that good. I won't be able to sit down tomorrow."),

            _("I came from anal. I HATE anal. What the hell just happened to me."),

            _("My body betrayed me... my ass hurts like hell but that orgasm was... ugh."),

        ],

        "cum_inside.anal.anal_hater.hardcore": [
            _("You came inside my sore ass... and my body is still twitching from it... I hate this."),

            _("Filling up the ass I hate having touched... and I felt every pulse... damn it."),

            _("It's pumping inside me... my ass hurts... but the warmth is... ugh. I hate you."),

        ],
        "cum_inside_accepted.anal.anal_hater.hardcore": [
            _("Fine... my ass is already wrecked... might as well feel you finish inside..."),

            _("Do it. Cum in my ass. It already hurts... maybe your cum will make it shut up..."),

            _("My ass is ruined anyway... just... fill it. Get it over with."),

        ],
        "cum_inside_denied.anal.anal_hater.hardcore": [
            _("My ass is already on fire and you want to FILL it too?! ...wait, why am I hesitating..."),

            _("Inside my wrecked ass?! I should say... I can't... ugh, just pull out!"),

            _("My body is screaming yes but my ass is SCREAMING... just finish somewhere else!"),

        ],
        "cum_inside_forced.anal.anal_hater.hardcore": [
            _("You CAME in my wrecked ass?! ...fuck... why does the warmth feel... damn it!"),

            _("I felt every pulse... inside my aching ass... and my body CLENCHED for it... I hate myself."),

            _("You filled my sore ass without asking... and I... I didn't pull away. What is wrong with me."),

        ],
        "cum_inside_consented.anal.anal_hater.hardcore": [
            _("I begged you to cum in the ass I HATE having touched... the warmth feels... ugh... damn it all."),

            _("My ass is screaming... and I ASKED for your cum inside... my body is a traitor..."),

            _("I said yes... it hurts and it's full and I... wanted it. I actually wanted it. I hate this."),

        ],

        "record_accepted.anal.anal_hater.camera_lover": [
            _("Good... Show everyone what you're doing to my ass!"),

            _("Film it. Film my ass getting wrecked. At least SOMETHING good comes from this pain."),

            _("Camera on my ass while I hate every... wait, why does the camera make it better..."),

        ],
        "record_accepted.anal.anal_hater.camera_hater": [
            _("You're filming? You can't! Not this! Gross! Why is it so good? Everyone's gonna see me cum like this!"),

            _("A camera while my ass is getting destroyed?! This can't be happening..."),

            _("You're recording this?! My most humiliating moment?! ...I can't even think straight..."),

        ],

        # ============================================================
        # ANAL_HATER + CUTE (dual-trait: endures for player)
        # ============================================================

        "moan.speed1.anal.anal_hater.cute": [
            _("Ow... Oh god... Slowly... Please."),

            _("I can adjust... Wait... Ow."),

            _("You'll cum quicker... like this... right?"),

        ],
        "moan.speed2.anal.anal_hater.cute": [
            _("Ow ow ow... I'm trying to be brave... for you... ow..."),

            _("It hurts so much... but you want this... so I'll try... ow..."),

            _("Please be gentle... please... my ass can't take much..."),

        ],
        "moan.speed3.anal.anal_hater.cute": [
            _("Ow... ow... ow... ow... ow..."),

            _("Cum soon. Please cum soon. Please?"),

            _("It's broken. It has to be broken. You're breaking it."),

        ],

        "cum_inside.anal.anal_hater.cute": [
            _("You came in my butt... it's warm... and it hurts... everything hurts..."),

            _("I felt every drop... inside my poor sore butt... oh..."),

            _("It's full... my aching butt is full of your cum... is it over now?"),

        ],
        "cum_inside_accepted.anal.anal_hater.cute": [
            _("If... if you want to finish inside... I can take it... for you..."),

            _("Okay... inside my butt... just... please hold me after..."),

            _("You want to cum inside? ...it already hurts... but okay. For you."),

        ],
        "cum_inside_denied.anal.anal_hater.cute": [
            _("Please... my butt already hurts so much... anywhere else... please..."),

            _("I'm trying so hard for you... but please... not inside my butt too... it's too much..."),

            _("I want to make you happy but... inside there? ...I can't... it hurts too much..."),

        ],
        "cum_inside_forced.anal.anal_hater.cute": [
            _("You finished inside my butt... it's so full... I was already hurting... why..."),

            _("I felt it pumping inside my sore butt... you could have warned me... ow..."),

            _("My butt is aching and full of your cum... I did everything for you and you still..."),

        ],
        "cum_inside_consented.anal.anal_hater.cute": [
            _("I said yes... because you looked so happy... my butt hurts but... at least you got what you wanted..."),

            _("I told you to do it inside... my poor butt... but seeing your face... it was worth the pain..."),

            _("You can fill my butt... I hate how it feels... but I love making you feel good... so it's okay..."),

        ],

        # ══════════════════════════════════════════════════════════
        #  DRESSUP — Post-scene getting dressed
        # ══════════════════════════════════════════════════════════

        "dressup": [  # Se vestindo apos a cena — base
            _("Hehe, that was fun."),

            _("Nice show, huh?"),

            _("Let me find my clothes now..."),

            _("Back to being decent, I guess."),

            _("Don't stare while I get dressed!"),

            _("Where did my panties go...?"),

            _("I hope nobody saw us."),

            _("That was something... let me get dressed."),

        ],
        "dressup.cum_slut": [  # Garota adora cum
            _("Can we do that again later?"),

            _("I don't want to get dressed yet..."),

            _("My body is still tingling everywhere..."),

            _("I can still feel you inside me..."),

        ],
        "dressup.public": [  # Local publico
            _("Quick, get dressed before someone comes!"),

            _("Oh god, do I look normal? Can anyone tell?"),

            _("Fix my hair... I look like I just..."),

        ],
        "dressup.boyfriend": [  # Garota tem namorado
            _("God, what have I done..."),

            _("He can never know about this."),

            _("If he ever finds out about this..."),

            _("I can't believe I let that happen..."),

        ],
        "dressup.first_time": [  # Primeira vez
            _("That was... my first time. Wow."),

            _("I feel different now... is that weird?"),

            _("I can't believe we actually did that..."),

        ],
        "dressup.recurring": [  # Recorrente / ja fez antes
            _("Same time tomorrow?"),

            _("We're getting pretty good at this..."),

            _("I could get used to this..."),

        ],
        "dressup.hate_cum": [  # Garota odeia cum
            _("I need to clean up immediately."),

            _("Ugh, I feel sticky..."),

            _("Next time, less mess, please."),

        ],
        "dressup.hardcore": [  # Sexo intenso/pesado
            _("That was exactly what I needed..."),

            _("You really know how to give it to me."),

            _("I can barely walk... perfect."),

        ],
        "dressup.cute": [  # Sexo gentil/carinhoso
            _("Thank you... that was beautiful."),

            _("Can you hold me for a bit before I dress?"),

            _("I feel so happy right now..."),

        ],

        # ══════════════════════════════════════════════════════════
        #  RECORDING — Consent responses
        # ══════════════════════════════════════════════════════════

        # Player asks to record (accepted)
        "record_accepted": [  # Aceita ser gravada — base
            _("Okay... but don't show anyone."),

            _("Fine... just make sure I look good."),

            _("Alright, go ahead... but be careful with that."),

        ],
        "record_accepted.lesbian": [  # Lesbian conflict
            _("You're filming this? If this gets out, my entire reputation is gone."),

            _("Fine... record it. Just make sure nobody from my old life ever sees this."),

            _("Go ahead... proof that everything I said about myself was a lie. Just keep it between us."),

        ],
        "record_accepted.camera_lover": [  # Ama ser filmada
            _("Yes! I love being on camera!"),

            _("Finally! I was hoping you'd want to record this."),

            _("Ooh, make sure you get my good side~"),

            _("Mmm, the camera makes everything hotter..."),

        ],
        "record_accepted.recording_first": [  # Primeira vez gravando
            _("This is... okay, I guess. Just don't share it..."),

            _("Really? You want to record this? ...Fine, but only for you."),

            _("I've never been recorded before... okay, just this once."),

        ],
        "record_accepted.recording_recurring": [  # Recorrente / ja gravou varias vezes
            _("Again? You really like recording me, huh?"),

            _("Sure, why not. You already have a collection."),

            _("You just can't get enough of me on camera, can you?"),

        ],

        # Player asks to record (denied)
        "record_denied": [  # Nega ser gravada — base
            _("No way. Put that phone away."),

            _("I don't want to be recorded. Forget it."),

            _("Absolutely not. No cameras."),

        ],
        "record_denied.lesbian": [  # Lesbian conflict
            _("Absolutely NOT. There will be NO evidence of this. Ever."),

            _("Are you insane? If anyone sees footage of me doing this, my entire life crumbles."),

            _("No. No recording. The last thing I need is proof of what I'm letting you do."),

        ],
        "record_denied.camera_hater": [  # Odeia cameras
            _("I told you I HATE cameras! Put it away!"),

            _("Don't you dare point that thing at me!"),

            _("No! You know I can't stand being filmed!"),

            _("Are you serious? You know how I feel about cameras!"),

        ],
        "record_denied.cowgirl.camera_hater": [
            _("Film me riding you?! I'd rather die! Put that thing AWAY!"),

            _("No! I'm on top AND you want to record?! Absolutely not!"),

            _("Are you serious? No recording. Period."),

        ],
        "record_denied.hj.camera_hater": [
            _("Record my hands on you?! What if someone recognizes them?! NO!"),

            _("Film a handjob?! Even THAT is too much for me! Put it away!"),

            _("I SAID NO CAMERAS! I don't care what we're doing!"),

        ],
        "record_denied.bj.camera_hater": [
            _("Film my FACE with your cock in my mouth?! Are you INSANE?! NO!"),

            _("A blowjob on camera?! That's my worst nightmare! Put it AWAY!"),

            _("No way. I'm not getting filmed like this."),

        ],
        "record_denied.tj.camera_hater": [
            _("Film my chest?! No! I don't want ANY part of me on camera!"),

            _("Record this?! My chest on video?! ABSOLUTELY NOT!"),

            _("No. Put that camera away. Now."),

        ],
        "record_denied.anal.camera_hater": [
            _("Film you in my ASS?! Are you OUT OF YOUR MIND?! ABSOLUTELY NOT!"),

            _("ANAL on camera?! That's the most private thing ever! NO! PUT IT AWAY!"),

            _("You want evidence of THIS?! In my ass?! No. NEVER."),

        ],

        # --- record_accepted camera_hater (very high stats, reluctant) ---
        "record_accepted.camera_hater": [
            _("I can't believe I'm saying yes to this... I hate cameras so much. Just... don't show anyone. Ever."),

            _("Fine... but my stomach is in knots. You know how much I hate this. Delete it after."),

            _("Okay... okay. But I swear, if anyone else EVER sees this, we're done. I mean it."),

            _("...Yes. But I'm going to regret this. I already regret this. Just... be quick about it."),

        ],
        "record_accepted.cowgirl.camera_hater": [
            _("You want to film me riding you... god, I hate this. Fine. But you can see my FACE in this position..."),

            _("Okay... but filming me on top? You can see everything. Don't you dare let anyone see this."),

            _("Fine... you can film. Make me look good."),

        ],
        "record_accepted.hj.camera_hater": [
            _("Fine... but my face is still in frame. Don't you dare zoom out. Just the hands. ONLY the hands."),

            _("Okay... but keep the camera on your lap, not on me. I don't want my face anywhere near this video."),

            _("I'm terrified this will leak... but you convinced me... film it..."),

        ],
        "record_accepted.bj.camera_hater": [
            _("You want my face on camera with your... god. Fine. But if this EVER leaks, I will end you."),

            _("Okay... but this is the most terrifying thing you've ever asked me. My face is RIGHT THERE."),

            _("Okay, record it... your cock deserves to be on camera."),

        ],
        "record_accepted.tj.camera_hater": [
            _("Fine... my chest on camera. I feel so exposed. Just... please don't let anyone see."),

            _("Okay... but film from an angle where you can't see my face. Please. I'm begging you."),

            _("I'm terrified this will leak... but you convinced me... film it..."),

        ],
        "record_accepted.anal.camera_hater": [
            _("You're filming... ANAL?! God, I hate this more than anything. If this EVER leaks..."),

            _("Fine... but anal on camera is the worst thing I've ever agreed to. Delete it after."),

            _("I can't believe you talked me into filming THIS. My ass on camera... I want to die."),

        ],

        # --- record_accepted by act ---
        "record_accepted.cowgirl": [
            _("You want to film me riding you? ...Fine. Make it look good."),

            _("Recording me on top? Okay... but this stays between us."),

            _("Okay, record it... your cock deserves to be on camera."),

        ],
        "record_accepted.hj": [
            _("You want to record my hands? Alright... just my hands though."),

            _("Filming a handjob? That's pretty tame... go ahead."),

            _("Record it... I'm curious how it looks from your angle."),

        ],
        "record_accepted.bj": [
            _("Recording me with your cock in my mouth? ...Okay. Don't zoom in too much."),

            _("Fine... but if this leaks I'll kill you."),

            _("Okay, record it... your cock deserves to be on camera."),

        ],
        "record_accepted.tj": [
            _("You want to film my chest? ...I guess. Make them look good."),

            _("Recording this? Okay... I do look pretty good right now."),

            _("Okay, record it... your cock deserves to be on camera."),

        ],
        "record_accepted.anal": [
            _("You want to record... anal? That's so private... fine. But this stays between us."),

            _("Filming while you're in my ass? ...Okay. But nobody EVER sees this."),

            _("Anal on camera... I must be crazy. Go ahead."),

        ],

        # --- record_accepted camera_lover by act ---
        "record_accepted.cowgirl.camera_lover": [
            _("YES! Film me riding you! I bet I look amazing from down there~"),

            _("Ooh, get the angle from below! I want to see myself bouncing on you!"),

            _("Sure... film me. I want proof of how good your cock makes me feel."),

        ],
        "record_accepted.hj.camera_lover": [
            _("Film my hands working you~ Close-up! I want every detail~"),

            _("Yes! Record it! My hands look so good wrapped around you..."),

            _("Finally! Get my good side and your big dick in frame!"),

        ],
        "record_accepted.bj.camera_lover": [
            _("Film me sucking you! I want to see how I look with your cock in my mouth~"),

            _("Yes! POV angle! This is going to be my favorite video ever~"),

            _("Fine... you can film. Make me look good."),

        ],
        "record_accepted.tj.camera_lover": [
            _("Film my tits around you! I bet this looks amazing on camera~"),

            _("Yes! Get a close-up! My chest deserves to be on film~"),

            _("Go ahead and film... I want to see how I look taking your dick."),

        ],
        "record_accepted.anal.camera_lover": [
            _("YES! Film my ass taking your cock! This is going to be SO hot~"),

            _("Anal on camera?! That's the naughtiest video we've made! I love it~"),

            _("Get the angle right! I want to see how my ass looks taking you~"),

        ],

        # --- record_accepted full_nelson ---
        "record_accepted.full_nelson": [
            _("You want to set up a tripod...? While you're holding me like this? ...fine."),

            _("A camera? Right now? ...okay, just make it quick."),

            _("Recording this position...? That's so exposing... fine, go ahead."),

        ],
        "record_accepted.full_nelson.camera_lover": [
            _("A tripod?! Yes! Get the whole thing on camera! This angle is perfect~"),

            _("Ooh, set it up! I want to see how I look like this~"),

            _("Finally! I was hoping you'd want to film this! The tripod is a nice touch~"),

        ],
        "record_accepted.full_nelson.camera_hater": [
            _("A tripod...? So there's no way to hide it... fine. But this stays between us."),

            _("You're really setting up a whole camera for this...? I hate this. But okay."),

            _("A fixed camera... watching everything... I can't believe I'm agreeing to this."),

        ],
        "record_accepted.full_nelson.boyfriend": [
            _("You want to record me like this...? If %(pl)s ever sees this... oh god."),

            _("A tripod...? So it captures everything...? %(Pp)s can never know."),

            _("Fine... but that camera better not end up anywhere %(pl)s can find it."),

        ],
        "record_accepted.full_nelson.girlfriend": [
            _("Recording me with a man... held up like this... if she ever sees this..."),

            _("A tripod...? Evidence of everything... okay. But she can never find this."),

            _("Go ahead... proof of what I'm really doing when she thinks I'm studying."),

        ],
        "record_accepted.full_nelson.boyfriend.camera_lover": [
            _("YES! Set it up! I want %(pl)s to see exactly how you hold me~"),

            _("A tripod for full nelson?! This is going to be the hottest video! %(Pp)s will lose %(poss)s mind~"),

            _("Oh, record EVERYTHING. I want the camera to catch every second of this."),

        ],
        "record_accepted.full_nelson.girlfriend.camera_lover": [
            _("Set it up! I want to see myself getting held up by a man on camera~"),

            _("A tripod?! Perfect! She'll die if she ever sees this... and I love it~"),

            _("Yes! Film it all! Proof that I love this more than I should~"),

        ],

        # --- record_denied full_nelson ---
        "record_denied.full_nelson": [
            _("A tripod? No way. I'm already exposed enough like this."),

            _("You want to film me held up like this? Absolutely not."),

            _("No. This position is embarrassing enough without a camera."),

        ],
        "record_denied.full_nelson.camera_hater": [
            _("A TRIPOD?! So it records EVERYTHING?! NO! Absolutely NOT!"),

            _("You want to set up a whole camera while I'm like this?! Are you INSANE?!"),

            _("No tripod! No camera! No NOTHING! I'm already uncomfortable enough!"),

        ],

        # --- recording_request full_nelson (camera_lover sub-event) ---
        "recording_request.full_nelson": [
            _("Hey... you have that tripod, right? Set it up... I want this on camera~"),

            _("Mmm... don't you want to film this? Get the tripod out..."),

            _("This position deserves to be recorded... set up the camera~"),

        ],

        # --- record_accepted boyfriend (non-cheater, non-camera) ---
        "record_accepted.boyfriend": [
            _("You're recording me cheating? ...Fine. But my boyfriend can NEVER see this."),

            _("Okay... but this video has to stay between us. My boyfriend..."),

            _("I can't believe I'm letting you film this. If my boyfriend ever sees..."),

        ],
        "record_accepted.cowgirl.boyfriend": [
            _("You're filming me riding another man... my boyfriend can never see this."),

            _("Go ahead... but if this video ever gets to my boyfriend, we're both dead."),

            _("Sure... film me. I want proof of how good your cock makes me feel."),

        ],
        "record_accepted.hj.boyfriend": [
            _("You're recording my hands on another man's cock... my boyfriend can never know."),

            _("Fine... but this video stays locked away. My boyfriend..."),

            _("Film it... but if my boyfriend ever sees this I'm done..."),

        ],
        "record_accepted.bj.boyfriend": [
            _("Filming me with another man's cock in my mouth... god, my boyfriend..."),

            _("Okay... but if this gets out, my boyfriend... I can't even think about it."),

            _("Okay, record it... your cock deserves to be on camera."),

        ],
        "record_accepted.tj.boyfriend": [
            _("Filming my tits on another man... if my boyfriend saw this..."),

            _("Go ahead. But this is video evidence of cheating. Be careful with it."),

            _("You can record... proof of what I do behind my boyfriend's back..."),

        ],
        "record_accepted.anal.boyfriend": [
            _("Filming anal cheating?! If my boyfriend sees this, it's over. For everyone."),

            _("My boyfriend has NO idea I do this... and now it's on camera..."),

            _("Anal on camera while cheating... this is the most damning evidence possible."),

        ],
        "record_accepted.girlfriend": [
            _("You're recording this? ...Fine. But my girlfriend can NEVER see this."),

            _("Okay... but this video has to stay hidden. If my girlfriend sees me with a man..."),

            _("I can't believe I'm letting you film this. Me, on camera, doing this..."),

        ],
        "record_accepted.cowgirl.girlfriend": [
            _("You're filming me riding you... my girlfriend can never see this."),

            _("Go ahead... but if this video ever gets to my girlfriend, my life is over."),

            _("Sure... film me. Proof that I'm riding you and loving it."),

        ],
        "record_accepted.hj.girlfriend": [
            _("You're recording my hands on your cock... my girlfriend can never know."),

            _("Fine... but this video stays hidden. My girlfriend would never forgive me..."),

            _("Film it... but if my girlfriend ever sees what I'm doing..."),

        ],
        "record_accepted.bj.girlfriend": [
            _("Filming me with your cock in my mouth... god, my girlfriend..."),

            _("Okay... but if this gets out, my girlfriend... I can't even think about it."),

            _("Okay, record it... me sucking cock on camera. She'd never believe it."),

        ],
        "record_accepted.tj.girlfriend": [
            _("Filming my tits on your cock... if my girlfriend saw this..."),

            _("Go ahead. But this is video evidence. Be careful with it."),

            _("You can record... proof of what I do with a man behind my girlfriend's back..."),

        ],
        "record_accepted.anal.girlfriend": [
            _("Filming me taking anal?! If my girlfriend sees this, it's over."),

            _("My girlfriend has NO idea I let a man do this... and now it's on camera..."),

            _("A girl with a girlfriend getting anal from a man on camera... this is the most damning evidence possible."),

        ],
        "record_accepted.anal.girlfriend.partner_caught": [
            _("She already knows about us... but filming me taking anal? That's a whole different level."),

            _("My girlfriend already caught us... and now you want anal on camera too? You're insane."),

            _("She knows. She already knows. And now you want proof on video... fine. Record it."),

        ],

        # --- record_accepted boyfriend + camera_lover ---
        "record_accepted.boyfriend.camera_lover": [
            _("YES! Film me cheating! My boyfriend has no idea and this footage will be AMAZING~"),

            _("Record everything! The fact that I have a boyfriend makes this so much hotter on camera~"),

            _("YES! Film everything! I look amazing with your cock!"),

        ],
        "record_accepted.girlfriend.camera_lover": [
            _("YES! Film this! My girlfriend has no idea and this footage will be AMAZING~"),

            _("Record everything! A lesbian girl taking cock on camera... this is so much hotter~"),

            _("YES! Film me loving dick! My girlfriend would never believe this footage!"),

        ],
        "record_accepted.cowgirl.boyfriend.camera_lover": [
            _("Film me riding you! My boyfriend has no idea another man is getting this POV~"),

            _("Yes! This angle... my boyfriend could never. I want to watch this later~"),

            _("Fine... you can film. Make me look good."),

        ],
        "record_accepted.cowgirl.girlfriend.camera_lover": [
            _("Film me riding you! My girlfriend has no idea I'm on camera like this~"),

            _("Yes! This angle... she could never give me this view. I want to watch this later~"),

            _("Fine... you can film. Make me look good on top of a man."),

        ],
        "record_accepted.hj.boyfriend.camera_lover": [
            _("Film my hands! My boyfriend has no idea I'm touching another man's cock on camera~"),

            _("Record it close-up! My boyfriend thinks these hands are only for him~"),

            _("Fine... you can film. Make me look good."),

        ],
        "record_accepted.hj.girlfriend.camera_lover": [
            _("Film my hands on your cock! My girlfriend has no idea I'm doing this on camera~"),

            _("Record it close-up! My girlfriend thinks these hands would never touch a man~"),

            _("Fine... you can film. A lesbian stroking cock on camera. Make me look good."),

        ],
        "record_accepted.bj.boyfriend.camera_lover": [
            _("Film me sucking you! My boyfriend doesn't know my mouth is on camera for someone else~"),

            _("Yes! POV! My boyfriend would lose it if he saw this footage~"),

            _("Fine... you can film. Make me look good."),

        ],
        "record_accepted.bj.girlfriend.camera_lover": [
            _("Film me sucking cock! My girlfriend doesn't know what I'm doing on camera~"),

            _("Yes! POV! My girlfriend would lose it if she saw me with a cock in my mouth~"),

            _("Fine... you can film. A lesbian on her knees for a man. Make me look good."),

        ],
        "record_accepted.tj.boyfriend.camera_lover": [
            _("Film my tits on you! My boyfriend thinks they're only for him... not anymore on camera~"),

            _("Record it! My boyfriend has never seen me do this on film~"),

            _("I was hoping you'd record! My body on camera is art!"),

        ],
        "record_accepted.tj.girlfriend.camera_lover": [
            _("Film my tits on a man! My girlfriend thinks they're only for her... not anymore on camera~"),

            _("Record it! My girlfriend has never seen me do this with a man on film~"),

            _("I was hoping you'd record! My body on your cock on camera is art!"),

        ],
        "record_accepted.anal.boyfriend.camera_lover": [
            _("ANAL cheating on camera?! This is the ultimate video! My boyfriend would FAINT~"),

            _("Film it! My boyfriend doesn't even know I do anal! And here I am on camera~"),

            _("Yes! This is the filthiest footage ever! Anal cheating on film! I love it~"),

        ],
        "record_accepted.anal.girlfriend.camera_lover": [
            _("A girl who dates girls taking anal from a man on camera?! This is the ultimate video! My girlfriend would FAINT~"),

            _("Film it! My girlfriend doesn't even know about this! And here I am doing anal on camera~"),

            _("Yes! This is the filthiest footage ever! A girl with a girlfriend getting anal from a man on film! I love it~"),

        ],

        # --- record_accepted boyfriend + camera_hater ---
        "record_accepted.boyfriend.camera_hater": [
            _("I can't believe I'm saying yes... but fine. My boyfriend can NEVER see this. NEVER."),

            _("Okay... but this is the most dangerous thing I've ever done. If my boyfriend finds this video..."),

            _("I can't believe I'm agreeing to this... I hate cameras... but fine."),

        ],
        "record_accepted.girlfriend.camera_hater": [
            _("I can't believe I'm saying yes... but fine. My girlfriend can NEVER see me with a man. NEVER."),

            _("Okay... but this is the most dangerous thing I've ever done. If my girlfriend finds a video of me with a cock..."),

            _("I can't believe I'm agreeing to this... I hate cameras... and I'm with a man... but fine."),

        ],
        "record_accepted.cowgirl.boyfriend.camera_hater": [
            _("Fine... but if my boyfriend ever finds a video of me riding another man..."),

            _("Okay. But this is evidence I'm cheating. I'm terrified right now."),

            _("Okay, record it... your cock deserves to be on camera."),

        ],
        "record_accepted.cowgirl.girlfriend.camera_hater": [
            _("Fine... but if my girlfriend ever finds a video of me riding a man..."),

            _("Okay. But this is evidence I'm with a man. I'm terrified right now."),

            _("Okay, record it... but proof of me doing this... she can never see this."),

        ],
        "record_accepted.hj.boyfriend.camera_hater": [
            _("Fine... my hands don't show my face at least. But my boyfriend can NEVER find this."),

            _("Okay... it's just my hands. But it's still evidence of cheating..."),

            _("This goes against everything I believe... just don't show my face..."),

        ],
        "record_accepted.hj.girlfriend.camera_hater": [
            _("Fine... my hands don't show my face at least. But my girlfriend can NEVER find me touching a man."),

            _("Okay... it's just my hands on your cock. But it's still evidence of what I'm doing..."),

            _("This goes against everything I believe... just don't show my face..."),

        ],
        "record_accepted.bj.boyfriend.camera_hater": [
            _("Oh god... you're filming my face with your... my boyfriend. Delete this after. Please."),

            _("Fine. But my face is IN this. If my boyfriend finds it... I need you to swear."),

            _("Film it... but if my boyfriend ever sees this I'm done..."),

        ],
        "record_accepted.bj.girlfriend.camera_hater": [
            _("Oh god... you're filming me with your cock in my mouth... my girlfriend. Delete this after. Please."),

            _("Fine. But my face is IN this. If my girlfriend finds me sucking a man... I need you to swear."),

            _("Film it... but if my girlfriend ever sees me with a cock in my mouth I'm done..."),

        ],
        "record_accepted.tj.boyfriend.camera_hater": [
            _("Okay... but if my boyfriend sees my chest on another man on video..."),

            _("Fine. But this video could ruin my relationship. Guard it with your life."),

            _("I can't believe I'm agreeing to this... I hate cameras... but fine."),

        ],
        "record_accepted.tj.girlfriend.camera_hater": [
            _("Okay... but if my girlfriend sees my chest on your cock on video..."),

            _("Fine. But this video could ruin my relationship. Guard it with your life."),

            _("I can't believe I'm agreeing to this... I hate cameras... and I'm with a man... but fine."),

        ],
        "record_accepted.anal.boyfriend.camera_hater": [
            _("Anal cheating on camera... I hate cameras AND this is the worst possible thing to film. But fine."),

            _("If my boyfriend sees me getting anal from another man... on video... my life is over."),

            _("This is everything I hate. Cameras. Cheating evidence. Anal on film. And I'm saying yes. I'm insane."),

        ],
        "record_accepted.anal.girlfriend.camera_hater": [
            _("A girl with a girlfriend taking anal from a man on camera... I hate cameras AND this is the worst possible thing to film. But fine."),

            _("If my girlfriend sees me getting anal from a man... on video... my life is over."),

            _("This is everything I hate. Cameras. A man inside me. Anal on film. And I'm saying yes. I'm insane."),

        ],

        # --- record_accepted cheater ---
        "record_accepted.cheater": [
            _("Oh, you want proof? Go ahead~ It's not like I care who sees."),

            _("Film away. My %(pl)s can deal with it. Or not~"),

            _("Sure! Maybe I'll accidentally send it to someone~"),

        ],
        "record_accepted.cowgirl.cheater": [
            _("Film me riding you~ If my %(pl)s sees... well, that's %(poss)s problem."),

            _("Record this angle! I look amazing on top of someone who isn't my %(pl)s~"),

            _("Record it... I'm curious how it looks from your angle."),

        ],
        "record_accepted.hj.cheater": [
            _("Film my hands on another man's cock. My %(pl)s would be devastated~ Oh well."),

            _("Go ahead and record! These hands aren't exclusive anymore~"),

            _("Record me with your cock... %(pp)s'll never know this exists..."),

        ],
        "record_accepted.bj.cheater": [
            _("Film my mouth on you! My %(pl)s thinks %(pp)s's the only one. How cute~"),

            _("Record me sucking another man's cock. Wouldn't that be a fun video to leak~"),

            _("Film it~ My %(pl)s doesn't get footage. Only you~"),

        ],
        "record_accepted.tj.cheater": [
            _("Film my tits on you! My %(pl)s has no idea they're on camera for someone else~"),

            _("Record it! My chest on another man. My %(pl)s would cry~"),

            _("Film it~ My %(pl)s doesn't get footage. Only you~"),

        ],

        # --- record_accepted cheater + camera_lover ---
        "record_accepted.cheater.camera_lover": [
            _("PERFECT combo! Film me cheating! I want this on every screen I own~"),

            _("YES! Camera + cheating = the ultimate thrill! Record EVERYTHING!"),

            _("Record it... I'm curious how it looks from your angle."),

        ],
        "record_accepted.cowgirl.cheater.camera_lover": [
            _("Film me riding you! I want my %(pl)s to accidentally find this someday~"),

            _("YES! Record me on top! The cheating + the camera... I'm SO turned on!"),

            _("Record it... I'm curious how it looks from your angle."),

        ],
        "record_accepted.bj.cheater.camera_lover": [
            _("Film my mouth! My %(pl)s has no idea and the camera makes me want to suck even harder~"),

            _("POV of me cheating with my mouth! This is going in my private collection~"),

            _("Film it~ My %(pl)s doesn't get footage. Only you~"),

        ],

        # --- record_denied boyfriend ---
        "record_denied.boyfriend": [
            _("Are you insane?! I'm already cheating! You want VIDEO EVIDENCE too?!"),

            _("No! What if my boyfriend finds it?! Absolutely not!"),

            _("Recording me cheating?! Do you want to ruin my life?!"),

        ],
        "record_denied.cowgirl.boyfriend": [
            _("You want to film me riding another man?! My boyfriend would die! No!"),

            _("No way! A video of me on top of someone else?! Are you crazy?!"),

            _("Record me cheating?! That's evidence! Absolutely NOT!"),

        ],
        "record_denied.hj.boyfriend": [
            _("Film my hands on you?! What if my boyfriend recognizes me?! No!"),

            _("No! My boyfriend would notice my hands anywhere. Don't you dare record."),

            _("NO! What if my boyfriend finds that video?! Are you crazy?!"),

        ],
        "record_denied.bj.boyfriend": [
            _("Film my face with your cock in my mouth?! My boyfriend would RECOGNIZE me! NO!"),

            _("Are you insane?! That's my FACE! My boyfriend would know instantly!"),

            _("Record me cheating?! That's evidence! Absolutely NOT!"),

        ],
        "record_denied.tj.boyfriend": [
            _("Film my chest on another man?! My boyfriend would recognize me! No!"),

            _("No! My boyfriend knows my body! He'd know that's me instantly!"),

            _("NO! What if my boyfriend finds that video?! Are you crazy?!"),

        ],
        "record_denied.girlfriend": [
            _("Are you insane?! You want VIDEO EVIDENCE of this too?!"),

            _("No! What if my girlfriend finds it?! A video of me with a man?! Absolutely not!"),

            _("Recording me cheating?! Do you want to ruin my life?!"),

        ],
        "record_denied.cowgirl.girlfriend": [
            _("You want to film me riding you?! My girlfriend would die! No!"),

            _("No way! A video of me on top of a man?! Are you crazy?!"),

            _("Record me with a man?! That's proof I'm not who she thinks I am! Absolutely NOT!"),

        ],
        "record_denied.hj.girlfriend": [
            _("Film my hands on a man?! What if my girlfriend sees?! No!"),

            _("No! My girlfriend would recognize my hands on a cock anywhere. Don't you dare record."),

            _("NO! What if my girlfriend finds that video?! A lesbian touching a man?! Are you crazy?!"),

        ],
        "record_denied.bj.girlfriend": [
            _("Film my face with a cock in my mouth?! My girlfriend would RECOGNIZE me! NO!"),

            _("Are you insane?! That's my FACE! A lesbian sucking a man off! She'd know instantly!"),

            _("Record this?! That's evidence! Absolutely NOT!"),

        ],
        "record_denied.tj.girlfriend": [
            _("Film my chest on your cock?! My girlfriend would recognize me! No!"),

            _("No! My girlfriend knows my body! She'd know that's me with a man instantly!"),

            _("NO! What if my girlfriend finds a video of me with a man?! Are you crazy?!"),

        ],

        # --- record_denied boyfriend + camera_hater ---
        "record_denied.boyfriend.camera_hater": [
            _("I'm already TERRIFIED of being caught cheating! And you want CAMERAS?! NEVER!"),

            _("NO! I hate cameras AND I have a boyfriend! That's a double nightmare!"),

            _("Are you trying to destroy my life?! No cameras! EVER! My boyfriend..."),

        ],
        "record_denied.girlfriend.camera_hater": [
            _("I'm already TERRIFIED of my girlfriend finding out I'm with a man! And you want CAMERAS?! NEVER!"),

            _("NO! I hate cameras AND I have a girlfriend! That's a triple nightmare!"),

            _("Are you trying to destroy my life?! No cameras! EVER! If she sees me with a cock..."),

        ],

        # --- record_denied cheater (she's a cheater but still might deny) ---
        "record_denied.cheater": [
            _("I don't mind cheating, but I'm not stupid enough to let you film it."),

            _("Nah. I cheat, but I don't leave evidence. I'm not an idiot."),

            _("I like the thrill, but a recording is permanent. No thanks."),

        ],

        # ══════════════════════════════════════════════════════════
        #  RECORD — PLAYER IS CHEATING (has girlfriend, recording someone else)
        # ══════════════════════════════════════════════════════════

        # --- record_accepted player_cheating (base — she knows he has a gf) ---
        "record_accepted.player_cheating": [
            _("You want to record this while you have a girlfriend? ...Fine. Your funeral."),

            _("If she ever finds this video... you're dead. But okay."),

            _("Recording me while you're dating someone? That's bold. Go ahead."),

            _("You better hide this from your girlfriend. But sure... record me."),

        ],
        "record_accepted.cowgirl.player_cheating": [
            _("Film me riding you while your girlfriend has no idea. That's messed up."),

            _("Recording me on top of you... if she finds this, it's over for you."),

            _("Recording? Your girlfriend would LOVE to see this footage..."),

        ],
        "record_accepted.hj.player_cheating": [
            _("Record my hands on you. Your girlfriend would love to see this... or not."),

            _("Filming me jerking you off while you have a girlfriend? Bold move."),

            _("Record it... I'm curious how it looks from your angle."),

        ],
        "record_accepted.bj.player_cheating": [
            _("Record me sucking you off. Your girlfriend has no idea, does she?"),

            _("Film this. Evidence that your girlfriend isn't enough for you."),

            _("Go ahead and film... I want to see how I look taking your dick."),

        ],
        "record_accepted.tj.player_cheating": [
            _("Record my tits on you. Your girlfriend would cry if she saw this."),

            _("Film this... your girlfriend is missing out, clearly."),

            _("Go ahead and film... I want to see how I look taking your dick."),

        ],

        # --- record_denied player_cheating (base — she refuses because he has a gf) ---
        "record_denied.player_cheating": [
            _("No way! You have a girlfriend! I'm not ending up as evidence!"),

            _("Absolutely not. What if your girlfriend finds the video?!"),

            _("I'm already doing this with someone else's boyfriend. I'm NOT being filmed too."),

            _("No! If your girlfriend ever sees that recording, she'll come after ME."),

        ],
        "record_denied.cowgirl.player_cheating": [
            _("Film me riding someone else's boyfriend? No! That's proof of everything!"),

            _("I'm on top of you and you want a VIDEO? Your girlfriend would murder me!"),

            _("Absolutely not. I don't want your cock AND a camera."),

        ],
        "record_denied.hj.player_cheating": [
            _("No recording! My hands on someone else's boyfriend is bad enough!"),

            _("I won't be filmed. What if your girlfriend gets your phone?!"),

            _("Film you cheating on camera?! How stupid can you be?!"),

        ],
        "record_denied.bj.player_cheating": [
            _("No! Me with your girlfriend's boyfriend's... NO! No cameras!"),

            _("A video of me sucking off someone else's boyfriend? Are you insane?!"),

            _("No way. I'm not getting filmed like this."),

        ],
        "record_denied.tj.player_cheating": [
            _("No! If your girlfriend sees my tits on you in a video, I'm dead!"),

            _("Film this? With your girlfriend out there? Absolutely not!"),

            _("Record us?! What if your GIRLFRIEND finds that video?!"),

        ],

        # --- record_accepted player_cheating + camera_lover ---
        "record_accepted.player_cheating.camera_lover": [
            _("You have a girlfriend and you want to film us? I LOVE that~"),

            _("Record everything~ The fact that you're cheating makes this footage even hotter~"),

            _("Yes! Film me stealing someone else's boyfriend~ This is going to be incredible footage~"),

        ],
        "record_accepted.cowgirl.player_cheating.camera_lover": [
            _("Film me riding her boyfriend~ This is my best performance yet~"),

            _("Record me on top! Your girlfriend's going to hate this video and I love it~"),

            _("Record it... I bet she'd die seeing your cock with me on camera..."),

        ],
        "record_accepted.bj.player_cheating.camera_lover": [
            _("Film my mouth on her boyfriend~ God, I love being on camera~"),

            _("Record me! Your girlfriend doesn't know how good I look doing this~"),

            _("Go ahead and film... I want to see how I look taking your dick."),

        ],
        "record_accepted.tj.player_cheating.camera_lover": [
            _("Film my tits on you~ Your girlfriend is going to cry and I look amazing~"),

            _("Record this! The cheating plus the camera... I'm in heaven~"),

            _("Go ahead and film... I want to see how I look taking your dick."),

        ],

        # --- record_denied player_cheating + camera_lover ---
        "record_denied.player_cheating.camera_lover": [
            _("I love cameras but... you have a girlfriend. That video could ruin us both."),

            _("I want to say yes SO badly... but if your girlfriend finds that footage..."),

            _("Ugh, I hate saying no to a camera... but this is too risky with your girlfriend."),

        ],

        # --- record_denied player_cheating + camera_hater ---
        "record_denied.player_cheating.camera_hater": [
            _("I HATE cameras AND you have a girlfriend?! That's a double no!"),

            _("No cameras EVER! Especially not while cheating on your girlfriend!"),

            _("I already hate being filmed. Add 'cheating evidence' and it's a HELL no!"),

        ],

        # --- record_accepted player_cheating + camera_hater (rare, very high stats) ---
        "record_accepted.player_cheating.camera_hater": [
            _("I hate cameras... and you have a girlfriend... I can't believe I'm saying yes..."),

            _("This is everything I'm against... cameras AND cheating evidence... but fine."),

            _("Okay, record it... your cock deserves to be on camera."),

        ],

        # --- record_accepted player_cheating + cheater ---
        "record_accepted.player_cheating.cheater": [
            _("We're both cheaters AND it's being recorded? This is perfect~"),

            _("Film us cheating together~ My %(pl)s AND your girlfriend can both cry about it~"),

            _("Record the evidence! I love that we're both betraying someone right now~"),

        ],
        "record_accepted.cowgirl.player_cheating.cheater": [
            _("Film me riding someone else's man while I cheat on my %(pl)s~ Double feature~"),

            _("Record this! Two cheaters on camera~ My %(pl)s and your girlfriend lose~"),

            _("Film it~ My %(pl)s doesn't get footage. Only you~"),

        ],
        "record_accepted.bj.player_cheating.cheater": [
            _("Film me sucking your girlfriend's man off~ My %(pl)s has no idea either~"),

            _("Record this! Two cheaters, zero regrets~"),

            _("Fine... you can film. Make me look good."),

        ],

        # --- record_denied player_cheating + cheater ---
        "record_denied.player_cheating.cheater": [
            _("I love cheating but I'm not stupid. Two relationships worth of evidence? No way."),

            _("We're both cheaters, sure. But a video is proof for TWO angry partners. Pass."),

            _("Record us?! What if your GIRLFRIEND finds that video?!"),

        ],

        # --- record_accepted player_cheating + boyfriend (she has bf AND player has gf) ---
        "record_accepted.player_cheating.boyfriend": [
            _("My boyfriend, your girlfriend... and now a recording. We're truly terrible people."),

            _("Film this... evidence of us both cheating. If this ever gets out..."),

            _("You want proof that we're both cheating? ...Fine. Record it."),

        ],
        "record_accepted.cowgirl.player_cheating.boyfriend": [
            _("Film me riding you... my boyfriend and your girlfriend are both being betrayed on camera."),

            _("Record me on top. Two relationships on the line and I'm performing for the camera."),

            _("Record it... I'm curious how it looks from your angle."),

        ],
        "record_accepted.bj.player_cheating.boyfriend": [
            _("Film me... my boyfriend doesn't know I'm sucking off someone else's boyfriend."),

            _("Record this... two relationships being destroyed while I'm on my knees."),

            _("Film me... proof of what you do behind her back..."),

        ],
        "record_accepted.tj.player_cheating.boyfriend": [
            _("Film my tits on you... neither of our partners will ever know about this footage."),

            _("Record it. My boyfriend's girlfriend using her chest on someone else's boyfriend."),

            _("Recording? Your girlfriend would LOVE to see this footage..."),

        ],
        "record_accepted.player_cheating.girlfriend": [
            _("My girlfriend, your girlfriend... and now a recording of me with a man. We're insane."),

            _("Film this... evidence of me cheating. If this ever gets out..."),

            _("You want proof that I'm with a man behind my girlfriend's back? ...Fine. Record it."),

        ],
        "record_accepted.cowgirl.player_cheating.girlfriend": [
            _("Film me riding you... my girlfriend and yours are both being betrayed on camera."),

            _("Record me on top. A lesbian riding a man while your girlfriend has no idea."),

            _("Record it... proof of who I really am behind my girlfriend's back."),

        ],
        "record_accepted.bj.player_cheating.girlfriend": [
            _("Film me... my girlfriend doesn't know I'm sucking off someone else's boyfriend."),

            _("Record this... me on my knees for you while two relationships burn."),

            _("Film me... proof of what I do behind everyone's back..."),

        ],
        "record_accepted.tj.player_cheating.girlfriend": [
            _("Film my tits on you... neither my girlfriend nor yours will ever know about this footage."),

            _("Record it. A lesbian using her chest on someone else's boyfriend. On camera."),

            _("Recording? Your girlfriend would LOVE to see what her boyfriend is doing..."),

        ],

        # --- record_denied player_cheating + boyfriend (double cheating, she refuses) ---
        "record_denied.player_cheating.boyfriend": [
            _("No! I have a boyfriend AND you have a girlfriend! A video is suicide for BOTH of us!"),

            _("We're already cheating on two people! I'm NOT adding a recording to this disaster!"),

            _("My boyfriend AND your girlfriend... no. No evidence. Ever."),

        ],
        "record_denied.cowgirl.player_cheating.boyfriend": [
            _("Me riding someone else's boyfriend? On camera? While I have a boyfriend?! NO!"),

            _("We're BOTH cheating and you want to FILM me on top?! Absolutely not!"),

            _("Are you serious? No recording. Period."),

        ],
        "record_denied.bj.player_cheating.boyfriend": [
            _("Sucking off someone else's boyfriend on film? While I have my own?! NEVER!"),

            _("My mouth on a taken man, recorded?! That footage could ruin EVERYTHING!"),

            _("Film you cheating on camera?! How stupid can you be?!"),

        ],
        "record_denied.player_cheating.girlfriend": [
            _("No! I have a girlfriend AND you have one too! A video of me with a man is suicide!"),

            _("We're already doing something insane! I'm NOT adding a recording of this!"),

            _("My girlfriend AND your girlfriend... no. No evidence of me with a man. Ever."),

        ],
        "record_denied.cowgirl.player_cheating.girlfriend": [
            _("A lesbian riding a man? On camera? While both of us have girlfriends?! NO!"),

            _("You want to FILM me on top of a man?! With my girlfriend out there?! Absolutely not!"),

            _("Are you serious? A lesbian on camera with a cock? No recording. Period."),

        ],
        "record_denied.bj.player_cheating.girlfriend": [
            _("A lesbian sucking off someone else's boyfriend on film?! While I have a girlfriend?! NEVER!"),

            _("My mouth on a man, recorded?! If my girlfriend finds that footage...!"),

            _("Film me cheating on camera?! How stupid can you be?!"),

        ],

        # --- recording_request boyfriend (camera_lover who has bf ASKS to be filmed) ---
        "recording_request.boyfriend": [
            _("Film me... I want evidence of what I'm doing behind my boyfriend's back~"),

            _("You should be recording this... my boyfriend has no idea..."),

            _("Get your phone out... I want proof of how bad I'm being~"),

        ],
        "recording_request.cowgirl.boyfriend": [
            _("Film me riding you... my boyfriend doesn't get this view. Or this video~"),

            _("Record me on top of another man... my boyfriend would lose his mind~"),

            _("Record me with you... my boyfriend can't know this exists..."),

        ],
        "recording_request.hj.boyfriend": [
            _("Film my hands... my boyfriend has no idea they're on another man right now~"),

            _("Record this... my hands on you instead of him~"),

            _("Film this... secret footage of your cock that he'll never see..."),

        ],
        "recording_request.bj.boyfriend": [
            _("Film my mouth on you... my boyfriend doesn't know I taste like someone else~"),

            _("Record me doing this... he'd never believe his girlfriend's mouth is here~"),

            _("Please... let me film this... I want to watch it later..."),

        ],
        "recording_request.tj.boyfriend": [
            _("Film my tits on you... my boyfriend thinks they're exclusive~"),

            _("Record this view... my boyfriend has never seen me do this on camera~"),

            _("Record me with you... my boyfriend can't know this exists..."),

        ],
        "recording_request.girlfriend": [
            _("Film me... I want evidence of what I do behind her back~"),

            _("You should be recording this... my girlfriend has no idea I'm with a man..."),

            _("Get your phone out... I want proof of what a man does to me~"),

        ],
        "recording_request.cowgirl.girlfriend": [
            _("Film me riding you... my girlfriend would never believe her girl is doing this~"),

            _("Record me on top of you... my girlfriend would lose her mind~"),

            _("Record me with you... my girlfriend can't know a man made me feel this way..."),

        ],
        "recording_request.hj.girlfriend": [
            _("Film my hands... my girlfriend has no idea what they're doing right now~"),

            _("Record this... my hands on a man instead of her~"),

            _("Film this... secret footage of my lesbian hands on a real cock..."),

        ],
        "recording_request.bj.girlfriend": [
            _("Film my mouth on you... my girlfriend doesn't know I taste like a man now~"),

            _("Record me doing this... she'd never believe her girlfriend's mouth is on a cock~"),

            _("Please... let me film this... me sucking cock... I want to watch it later..."),

        ],
        "recording_request.tj.girlfriend": [
            _("Film my tits on you... my girlfriend thinks they're only for her~"),

            _("Record this view... my girlfriend has never seen me do this with a man on camera~"),

            _("Record me with you... my girlfriend can't know your cock was between my tits..."),

        ],

        # --- recording_request cheater ---
        "recording_request.cheater": [
            _("Film me~ I want this on record. My %(pl)s can cry about it later."),

            _("Record this. I want to rewatch myself being a terrible partner~"),

            _("Can I record? I want to remember your thick cock..."),

        ],
        "recording_request.cowgirl.cheater": [
            _("Film me riding you~ Maybe I'll show my %(pl)s what %(pp)s's missing~"),

            _("Record this angle! I want proof of how much better you are than %(po)s~"),

            _("I want this on video... you inside me..."),

        ],
        "recording_request.bj.cheater": [
            _("Film my mouth on another man's cock! My %(pl)s thinks %(pp)s's special~ Ha!"),

            _("Record me sucking you off~ My %(pl)s could never know how eager I am~"),

            _("Please... let me film this... I want to watch it later..."),

        ],

        # --- recording_request_accepted boyfriend ---
        "recording_request_accepted.boyfriend": [
            _("Mmm... filming me cheating. This is so wrong and I love it~"),

            _("Yes! Now there's proof of what a terrible girlfriend I am~"),

            _("Film it... our dirty little secret on camera..."),

        ],
        "recording_request_accepted.girlfriend": [
            _("Mmm... filming us together. This is so wrong and I love it~"),

            _("Yes! Now there's proof of what I really do behind my girlfriend's back~"),

            _("Film it... my dirty secret on camera..."),

        ],

        # --- recording_request_accepted cheater ---
        "recording_request_accepted.cheater": [
            _("Perfect~ Now I can watch myself cheat whenever I want~"),

            _("Yes! Evidence of how little my %(pl)s means to me~"),

            _("Yes! Film me with your cock! This is going to be so hot!"),

        ],

        # --- recording_request_denied boyfriend ---
        "recording_request_denied.boyfriend": [
            _("Aww... but the cheating footage would've been so hot..."),

            _("Really? Fine... but my boyfriend would've died seeing that..."),

            _("Absolutely not. If he finds a video of us, it's over."),

        ],
        "recording_request_denied.girlfriend": [
            _("Aww... but the footage of us would've been so hot..."),

            _("Really? Fine... but my girlfriend would've died seeing me with a man..."),

            _("Absolutely not. If she finds a video of me with a man, it's over."),

        ],

        # Girl ASKS to be recorded (camera_lover sub-event)
        "recording_request": [  # Garota pede para gravar — base
            _("Hey... you should record this~"),

            _("Where's your phone? You should be filming this..."),

            _("Don't you want to remember this? Record me..."),

        ],
        "recording_request.lesbian": [  # Lesbian conflict
            _("You want to RECORD this? Are you insane?"),

            _("Film this... proof that I can't resist you. Happy now?"),

            _("Record it... nobody would believe what I'm doing without evidence."),

        ],
        "recording_request.cowgirl": [  # Durante cowgirl
            _("You should film me riding you... it'll look so hot."),

            _("Get your phone out... I want you to watch this later~"),

            _("Record me... I want to see how I look on top of you."),

        ],
        "recording_request.hj": [  # Durante handjob
            _("You should record my hands working you..."),

            _("Film this... watch it later when you miss me~"),

            _("Film this... I need to see how I look taking your dick..."),

        ],
        "recording_request.bj": [  # Durante blowjob
            _("Mmm... film me doing this. You'll love rewatching it."),

            _("Get your phone out... this deserves to be recorded~"),

            _("Can I record? I want to remember your thick cock..."),

        ],
        "recording_request.tj": [  # Durante titjob
            _("You should record this view... it's pretty hot, right?"),

            _("Film me... I want to see how they look wrapped around you~"),

            _("Can I record? I want to remember your thick cock..."),

        ],

        # Player accepts recording request
        "recording_request_accepted": [  # Player aceita gravar
            _("Yes! Make sure you get everything~"),

            _("Mmm, that's right... record every second."),

            _("Perfect... now watch me perform~"),

        ],

        # Player denies recording request
        "recording_request_denied": [  # Player nega gravar
            _("Aww... you sure? It would've been fun."),

            _("Really? Your loss~"),

            _("Fine... but you're missing out."),

        ],

        # --- recording_request player_cheating (camera_lover asks while player cheats) ---
        "recording_request.player_cheating": [
            _("Film us~ Your girlfriend has no idea you're here doing this with me~"),

            _("Get your phone out~ I want your girlfriend to find this someday~"),

            _("Record me... your girlfriend doesn't get this. And now there's proof~"),

        ],
        "recording_request.cowgirl.player_cheating": [
            _("Film me riding her boyfriend~ I want proof that I'm the better ride~"),

            _("Record me on top of you... your girlfriend is going to WISH she was here~"),

            _("Can we record this? Your cock looks so good..."),

        ],
        "recording_request.bj.player_cheating": [
            _("Film my mouth on you... your girlfriend can watch and learn~"),

            _("Record this! Proof that her boyfriend prefers MY mouth~"),

            _("Please... let me film this... I want to watch it later..."),

        ],
        "recording_request.hj.player_cheating": [
            _("Film my hands on you... your girlfriend's boyfriend is all mine right now~"),

            _("Record this... your girlfriend doesn't know where your hands have been~"),

            _("Can we record this? Your cock looks so good..."),

        ],
        "recording_request.tj.player_cheating": [
            _("Film my tits on you... your girlfriend can cry about it later~"),

            _("Record this! She'll never make you feel this way~"),

            _("Record your cock with me... she'd die if she saw this..."),

        ],

        # --- recording_request player_cheating + boyfriend ---
        "recording_request.player_cheating.boyfriend": [
            _("Film this~ My boyfriend AND your girlfriend can both suffer~"),

            _("Record us cheating on everyone! I want this footage forever~"),

            _("Get your phone~ Evidence that we're both terrible people and we love it~"),

        ],
        "recording_request.player_cheating.girlfriend": [
            _("Film this~ My girlfriend AND your girlfriend can both suffer~"),

            _("Record me cheating! I want this footage forever~"),

            _("Get your phone~ Evidence of what you do to me behind everyone's back~"),

        ],

        # --- recording_request player_cheating + cheater ---
        "recording_request.player_cheating.cheater": [
            _("Film me~ Two cheaters on camera? My %(pl)s and your girlfriend deserve this~"),

            _("Record us! I want to watch myself with someone else's man~"),

            _("Record me with your cock~ Evidence of our little secret~"),

        ],

        # --- recording_request_accepted player_cheating ---
        "recording_request_accepted.player_cheating": [
            _("Yes~ Now there's proof of what you're doing behind your girlfriend's back~"),

            _("Perfect! Your girlfriend is going to LOVE this video... or not~"),

            _("Record it! Your girlfriend will never see this footage of your cock..."),

        ],

        # --- recording_request_accepted player_cheating + boyfriend ---
        "recording_request_accepted.player_cheating.boyfriend": [
            _("Yes~ Proof of us both cheating! My boyfriend AND your girlfriend in shambles~"),

            _("Perfect~ The ultimate betrayal footage. I love everything about this~"),

            _("Yes! But hide it from my boyfriend... secret footage..."),

        ],
        "recording_request_accepted.player_cheating.girlfriend": [
            _("Yes~ Proof of us together! My girlfriend AND yours in shambles~"),

            _("Perfect~ A lesbian cheating with a man on camera. The ultimate betrayal footage~"),

            _("Yes! But hide it from my girlfriend... if she sees what I'm doing..."),

        ],

        # --- recording_request_denied player_cheating ---
        "recording_request_denied.player_cheating": [
            _("Aww, no camera? Your girlfriend would've loved seeing this evidence~"),

            _("Really? Fine... but imagine if she found a video of us. So hot~"),

            _("Put the camera away. Focus on what matters."),

        ],

        # ══════════════════════════════════════════════════════════
        #  PUBLIC + CHEATING — Recording lines
        # ══════════════════════════════════════════════════════════

        # --- record_accepted public (neutral, no cheat) ---
        "record_accepted.public": [
            _("You're really filming this... out here where anyone could see the screen..."),

            _("Recording in public... you're insane... fine, do it..."),

            _("Go ahead and film... I want to see how I look taking your dick."),

        ],
        "record_accepted.cowgirl.public": [
            _("Filming me riding you in public... if that video leaks..."),

            _("Recording me on top... out in the open... you're crazy..."),

            _("Okay, record it... your cock deserves to be on camera."),

        ],
        "record_accepted.hj.public": [
            _("A public handjob on camera... double the evidence..."),

            _("You're recording my hand on you... out here... fine..."),

            _("Recording in public... this is so risky but go ahead..."),

        ],
        "record_accepted.bj.public": [
            _("Filming a blowjob in public... you really want proof of this..."),

            _("My mouth on you... on camera... in the open..."),

            _("Go ahead and film... I want to see how I look taking your dick."),

        ],
        "record_accepted.tj.public": [
            _("Recording a titjob in public... if anyone sees your phone..."),

            _("My tits on camera... out here... you're insane..."),

            _("Camera plus public... my heart is pounding... film it..."),

        ],
        "record_denied.public": [
            _("No way! Not in public! Someone could see the screen!"),

            _("Are you insane? We're outside! No cameras!"),

            _("Put that phone away! Anyone could see what you're recording!"),

        ],

        # --- record_accepted/denied boyfriend + public (she's cheating, public) ---
        "record_accepted.cowgirl.boyfriend.public": [
            _("Film me riding another man in public... my boyfriend would die..."),

            _("Recording me on top of someone else... out in the open... evidence of everything..."),

            _("Camera plus public... my heart is pounding... film it..."),

        ],
        "record_accepted.cowgirl.girlfriend.public": [
            _("Film me riding you in public... my girlfriend would die..."),

            _("Recording me on top of a man... out in the open... proof I love cock..."),

            _("Camera plus public plus a man... my heart is pounding... film it..."),

        ],
        "record_accepted.hj.boyfriend.public": [
            _("My hand on another man... on camera... in public... my boyfriend can never know..."),

            _("Recording a handjob in public... while I have a boyfriend... I'm insane..."),

            _("Record it... I'm curious how it looks from your angle."),

        ],
        "record_accepted.hj.girlfriend.public": [
            _("My hand on your cock... on camera... in public... my girlfriend can never know..."),

            _("Recording a handjob for a guy in public... while I have a girlfriend... I'm insane..."),

            _("Record it... me touching you in public... I'm curious how it looks."),

        ],
        "record_accepted.bj.boyfriend.public": [
            _("Film me sucking another man in public... if my boyfriend ever finds this video..."),

            _("A public blowjob on camera... while I have a boyfriend... this is evidence..."),

            _("Recording in public... this is so risky but go ahead..."),

        ],
        "record_accepted.bj.girlfriend.public": [
            _("Film me sucking cock in public... if my girlfriend ever finds this video..."),

            _("A public blowjob for a man on camera... while I have a girlfriend... this is evidence I love cock..."),

            _("Recording in public with a man... this is so risky but go ahead..."),

        ],
        "record_denied.boyfriend.public": [
            _("No! My boyfriend could find a video AND we're in PUBLIC! No way!"),

            _("Are you crazy?! Public AND on camera?! If he ever sees this...!"),

            _("Not on camera! Not in public! Someone could send it to my boyfriend!"),

        ],
        "record_denied.girlfriend.public": [
            _("No! My girlfriend could find a video of me doing THIS and we're in PUBLIC! No way!"),

            _("Are you crazy?! Public AND on camera with a guy?! If she ever sees this...!"),

            _("Not on camera! Not in public! Someone could send proof I like cock to my girlfriend!"),

        ],

        # --- record boyfriend + public_shy ---
        "record_accepted.boyfriend.public_shy": [
            _("F-film it...? In public...? While I'm cheating...? I'm going to regret this..."),

            _("O-ok... but if this gets out... in public... my boyfriend... oh god..."),

            _("Go ahead and film... I want to see how I look taking your dick."),

        ],
        "record_accepted.girlfriend.public_shy": [
            _("F-film it...? In public...? While I'm with a man...? I'm going to regret this..."),

            _("O-ok... but if this gets out... in public... my girlfriend... she'll know I like cock... oh god..."),

            _("Go ahead and film... I want to see how I look taking dick... even though I'm not supposed to want it."),

        ],
        "record_denied.boyfriend.public_shy": [
            _("NO! Absolutely not! We're in PUBLIC and I have a BOYFRIEND! Are you insane?!"),

            _("A video?! Out here?! Where someone could see AND it could reach my boyfriend?! NO!"),

            _("No way. I'm not getting filmed like this."),

        ],
        "record_denied.girlfriend.public_shy": [
            _("NO! Absolutely not! We're in PUBLIC and I have a GIRLFRIEND! Are you insane?!"),

            _("A video of me doing THIS?! Out here?! Where someone could see AND tell my girlfriend?! NO!"),

            _("No way. I'm not getting filmed with a guy. She can never know."),

        ],

        # --- record boyfriend + public_fetish ---
        "record_accepted.cowgirl.boyfriend.public_fetish": [
            _("Film me riding someone else in public... I want my boyfriend to see this footage..."),

            _("Record it! His girlfriend bouncing on another cock in public! Perfect!"),

            _("You can record... proof of what I do behind my boyfriend's back..."),

        ],
        "record_accepted.cowgirl.girlfriend.public_fetish": [
            _("Film me riding you in public... I want my girlfriend to see this footage..."),

            _("Record it! Her girlfriend bouncing on your cock in public! Perfect!"),

            _("You can record... proof of what I do with a man behind my girlfriend's back..."),

        ],
        "record_accepted.bj.boyfriend.public_fetish": [
            _("Film his girlfriend sucking another cock in public... what a video that would be..."),

            _("Record it! On my knees in public for someone who isn't my boyfriend!"),

            _("Film me in public! Anyone could see AND it's on camera! YES!"),

        ],
        "record_accepted.bj.girlfriend.public_fetish": [
            _("Film her girlfriend sucking your cock in public... what a video that would be..."),

            _("Record it! A lesbian on her knees for a man in public! She'd lose her mind!"),

            _("Film me with your cock in public! Anyone could see AND it's on camera! YES!"),

        ],

        # --- record player_cheating + public (act-specific) ---
        "record_accepted.cowgirl.player_cheating.public": [
            _("Film me riding her boyfriend in public... she deserves to see this..."),

            _("Recording me on top of another girl's man... out in the open... evidence..."),

            _("Sure... film me. I want proof of how good your cock makes me feel."),

        ],
        "record_accepted.hj.player_cheating.public": [
            _("Film my hand on her boyfriend in public... if she ever finds this..."),

            _("A public handjob for another girl's man... on camera... do it..."),

            _("Fine... you can film. Make me look good."),

        ],
        "record_accepted.bj.player_cheating.public": [
            _("Film me sucking her boyfriend's cock in public... she'd love this footage..."),

            _("Record it... on my knees in public for another girl's man..."),

            _("Go ahead and film... I want to see how I look taking your dick."),

        ],
        "record_denied.player_cheating.public": [
            _("No! We're in public AND you have a girlfriend! If that video gets out...!"),

            _("Not on camera! If your girlfriend gets this AND we're in public...!"),

            _("Put the phone away! Someone could see AND your girlfriend could find the video!"),

        ],

        # --- record player_cheating + public_shy ---
        "record_accepted.player_cheating.public_shy": [
            _("F-film it...? In public...? What if your girlfriend finds the video...?"),

            _("O-ok... but if someone sees AND your girlfriend gets the file..."),

            _("Recording? Your girlfriend would LOVE to see this footage..."),

        ],
        "record_denied.player_cheating.public_shy": [
            _("NO! We're in PUBLIC! Your GIRLFRIEND could find the video! Are you CRAZY?!"),

            _("Not a chance! Public AND on camera?! If she ever sees this I'll die!"),

            _("Film you cheating on camera?! How stupid can you be?!"),

        ],

        # --- record player_cheating + public_fetish (act-specific) ---
        "record_accepted.cowgirl.player_cheating.public_fetish": [
            _("Film me riding her boyfriend in public! Send it to her! Let her watch!"),

            _("Record it! On top of another girl's man in the open! She needs to see!"),

            _("Okay, record it... your cock deserves to be on camera."),

        ],
        "record_accepted.bj.player_cheating.public_fetish": [
            _("Film his girlfriend's replacement sucking him off in public! Send it!"),

            _("Record me on my knees in public for her man! She NEEDS to see this!"),

            _("Record it... I bet she'd die seeing your cock with me on camera..."),

        ],

        # --- record both_cheating + public ---
        "record_accepted.cowgirl.both_cheating.public": [
            _("Film me riding another girl's boyfriend in public... while mine is clueless..."),

            _("Record two cheaters... me on top... in the open... send it to both of them..."),

            _("Camera plus public... my heart is pounding... film it..."),

        ],
        "record_accepted.bj.both_cheating.public": [
            _("Film me sucking another girl's boyfriend in public... two cheaters on camera..."),

            _("Record it... on my knees in public for someone else's man... while I have my own..."),

            _("Film it... two cheaters on camera... evidence of our crime~"),

        ],
        "record_denied.both_cheating.public": [
            _("No! Both of us have partners AND we're in public! If that video reaches EITHER of them!"),

            _("Are you insane?! Public, on camera, BOTH cheating?! That's a triple disaster!"),

            _("Are you serious? No recording. Period."),

        ],

        # --- record both_cheating + public_shy ---
        "record_accepted.both_cheating.public_shy": [
            _("Y-you want to film this...? In public...? Both of us cheating...? I'm shaking..."),

            _("O-ok... but if EITHER of our partners finds this AND we're in public..."),

            _("Okay, record it... your cock deserves to be on camera."),

        ],
        "record_denied.both_cheating.public_shy": [
            _("NO! Both our partners could find out AND we're in PUBLIC! NO CAMERAS!"),

            _("Absolutely not! Two cheaters on video in public?! That ruins FOUR lives!"),

            _("Absolutely not. I don't want your cock AND a camera."),

        ],

        # --- record both_cheating + public_fetish ---
        "record_accepted.cowgirl.both_cheating.public_fetish": [
            _("Film me riding her boyfriend in public! My %(pl)s AND his girlfriend should see!"),

            _("Record it! Two cheaters in public! Me on top! Send it to EVERYONE!"),

            _("Go ahead and film... I want to see how I look taking your dick."),

        ],
        "record_accepted.bj.both_cheating.public_fetish": [
            _("Film me sucking her boyfriend in public! Two cheaters on camera! Send to BOTH!"),

            _("Record it! His girlfriend's rival on her knees in public! My %(pl)s can watch too!"),

            _("Sure... film me. I want proof of how good your cock makes me feel."),

        ],

        # --- recording_request public (camera_lover asks to be filmed in public) ---
        "recording_request.public": [
            _("Hey... film this. Out here. Where anyone could see your screen~"),

            _("Get your phone out... I want this on camera... in public..."),

            _("Can I record? I want to remember your thick cock..."),

        ],
        "recording_request.cowgirl.public": [
            _("Film me riding you out here... I want proof we did this in public~"),

            _("Get your camera out... record me on top... in the open..."),

            _("Can we record this? Your cock looks so good..."),

        ],
        "recording_request.bj.public": [
            _("Film me sucking you in public... I want that on camera~"),

            _("Get your phone out... record this blowjob in the open..."),

            _("Record us in public... my heart is racing..."),

        ],

        # --- recording_request boyfriend + public ---
        "recording_request.boyfriend.public": [
            _("Film me... cheating on my boyfriend... in public... I want proof of how bad I am~"),

            _("Record this... me with another man... in the open... my boyfriend can deal with it~"),

            _("Film this... I need to see how I look taking your dick..."),

        ],
        "recording_request.girlfriend.public": [
            _("Film me... with a man... in public... I want proof that I love cock~"),

            _("Record this... me with a guy... in the open... my girlfriend can deal with it~"),

            _("Film this... I need to see how I look taking your dick... she'd never believe it~"),

        ],
        "recording_request.cowgirl.boyfriend.public": [
            _("Film me riding another man in public... I want my boyfriend to see someday~"),

            _("Record his girlfriend on top of someone else... in the open~"),

            _("Record us in public... my heart is racing..."),

        ],
        "recording_request.cowgirl.girlfriend.public": [
            _("Film me riding you in public... I want my girlfriend to see someday~"),

            _("Record her girlfriend on top of a man... in the open~"),

            _("Record us in public... me on your cock... my heart is racing..."),

        ],
        "recording_request_accepted.boyfriend.public": [
            _("Yes! Film the proof! His cheating girlfriend in public on camera!"),

            _("Do it! Record me betraying my boyfriend out in the open!"),

            _("Record everything! I want this on video forever!"),

        ],
        "recording_request_accepted.girlfriend.public": [
            _("Yes! Film the proof! Her girlfriend with a man in public on camera!"),

            _("Do it! Record me loving cock out in the open! My girlfriend can cry about it!"),

            _("Record everything! A lesbian taking dick in public! I want this on video forever!"),

        ],
        "recording_request_denied.boyfriend.public": [
            _("Ugh... fine. No camera. But this is still happening in public~"),

            _("Okay... no filming. But we're still doing this out here where anyone could see..."),

            _("Absolutely not. If he finds a video of us, it's over."),

        ],
        "recording_request_denied.girlfriend.public": [
            _("Ugh... fine. No camera. But this is still happening in public with a man~"),

            _("Okay... no filming. But we're still doing this out here where anyone could see me with a guy..."),

            _("Absolutely not. If she finds a video of me with a cock, it's over."),

        ],

        # --- recording_request player_cheating + public ---
        "recording_request.player_cheating.public": [
            _("Film us in public... your girlfriend would love this footage~"),

            _("Get your camera out... cheating on her in public AND on camera~"),

            _("Record this? Your girlfriend would hate knowing you filmed another girl..."),

        ],
        "recording_request.cowgirl.player_cheating.public": [
            _("Film me riding her boyfriend in public... she deserves to see this someday~"),

            _("Record me on top of you... out here... send it to your girlfriend~"),

            _("Record us in public... my heart is racing..."),

        ],
        "recording_request_accepted.player_cheating.public": [
            _("Yes! Film it! Public proof her boyfriend belongs to someone else!"),

            _("Do it! Record the cheating in the open!"),

            _("Record everything! I want this on video forever!"),

        ],
        "recording_request_denied.player_cheating.public": [
            _("Aww, no camera? The public cheating footage would've been perfect evidence~"),

            _("Fine, no film... but someone out here probably already saw us anyway~"),

            _("Put the camera away. Focus on what matters."),

        ],

        # --- recording_request both_cheating + public ---
        "recording_request.both_cheating.public": [
            _("Film two cheaters in public... both our partners should see this someday~"),

            _("Get your camera... double betrayal in the open... on tape..."),

            _("Can we record this? Your cock looks so good..."),

        ],
        "recording_request.cowgirl.both_cheating.public": [
            _("Film me riding her boyfriend in public... while mine is clueless~"),

            _("Record two cheaters... me on top... in the open... evidence for everyone~"),

            _("Let's film... proof that we're both terrible people~"),

        ],
        "recording_request_accepted.both_cheating.public": [
            _("Yes! Film us! Two cheaters in public! Send it to BOTH partners!"),

            _("Do it! Public proof of double betrayal! They both deserve to see!"),

            _("Go ahead! Your dick deserves to be filmed!"),

        ],
        "recording_request_denied.both_cheating.public": [
            _("No camera? Fine... but both our partners are already being betrayed in public~"),

            _("Okay, no video... still two cheaters out in the open though~"),

            _("Not today. Just enjoy my body without a camera."),

        ],

        # ══════════════════════════════════════════════════════════
        #  TRAIT COMBO — Moans Speed 1
        # ══════════════════════════════════════════════════════════

        "moan.speed1.cum_slut.hardcore": [
            _("This slow pace is torture... I need MORE..."),

            _("Come on... stop teasing. Give it to me properly..."),

            _("You're holding back. I can feel it. Don't."),

        ],
        "moan.speed1.cum_slut.cute": [
            _("This is nice... but I secretly want so much more..."),

            _("I love the gentleness... but my body is screaming for more..."),

            _("Mmm... you're so sweet... but I'm craving something intense..."),

        ],
        "moan.speed1.virgin.cute": [
            _("I can't believe this is happening... you're being so gentle..."),

            _("My heart is racing... is yours too?"),

            _("This is my first time... I'm glad it's with you..."),

        ],
        "moan.speed1.virgin.hardcore": [
            _("It's my first time... but don't treat me like glass."),

            _("I'm new to this, but I can handle more..."),

            _("Stop going easy on me. I want the real thing."),

        ],
        "moan.speed1.camera_lover.cum_slut": [
            _("Make sure you're getting this... I want to watch it later..."),

            _("The camera makes me want you even more..."),

            _("Mmm... your cock fills me up so well..."),

        ],
        "moan.speed1.public.cute": [
            _("What if someone hears us...? I'm so nervous..."),

            _("We have to be really quiet... I'm scared..."),

            _("Oh god, is that footsteps? No... okay... keep going..."),

        ],
        "moan.speed1.public.hardcore": [
            _("The risk of getting caught... it's making this better..."),

            _("Someone could walk in... I don't care. Keep going."),

            _("Nice and deep... I love it..."),

        ],
        "moan.speed1.boyfriend.cum_slut": [
            _("My boyfriend has no idea... and I've never felt this good..."),

            _("He could never do what you're doing to me..."),

            _("My boyfriend's dick doesn't go this deep..."),

        ],
        "moan.speed1.girlfriend.cum_slut": [
            _("My girlfriend has no idea... and I've never felt this good..."),

            _("She could never give me what you're giving me right now..."),

            _("I told her I didn't need cock... I was so wrong..."),

            _("My girlfriend would be horrified if she knew how much I think about cock..."),

            _("She thinks I'm faithful, but every time we're apart, I crave this..."),

        ],

        # ══════════════════════════════════════════════════════════
        #  TRAIT COMBO — Moans Speed 2
        # ══════════════════════════════════════════════════════════

        "moan.speed2.cum_slut.hardcore": [
            _("Fuck... harder... I NEED it harder..."),

            _("Don't slow down... give me everything you've got..."),

        ],
        "moan.speed2.cum_slut.submissive": [
            _("That's it... use me. Use me properly..."),

            _("I'm your cum slut... use me, and give it to me wherever you want..."),

            _("Use me... I'll take your cum anywhere you tell me to..."),

        ],
        "moan.speed2.cum_slut.cute": [
            _("It's so intense... I'm embarrassed how much I love this..."),

            _("Mmm... I can't stop my voice... you're making me crazy..."),

            _("I want more... but I'm too shy to ask for it..."),

        ],
        "moan.speed2.virgin.cute": [
            _("I never imagined it would feel this good... oh..."),

            _("You're my first... and it's so much better than I dreamed..."),

            _("I'm so glad I waited... for you..."),

        ],
        "moan.speed2.virgin.hardcore": [
            _("Don't hold back just because I'm a virgin. HARDER."),

            _("I should be scared but I'm not. Give me more."),

        ],
        "moan.speed2.virgin.submissive": [
            _("Is this really my first time? It feels like you've owned me forever..."),

            _("It's my first time... just tell me what to do and I'll do it..."),

            _("You're my first... and I want you to own me... all of me..."),

        ],
        "moan.speed2.camera_lover.hardcore": [
            _("Film me losing my mind... this is award-winning footage..."),

            _("The camera can see everything... and I want it to..."),

            _("Your cock is driving me crazy..."),

        ],
        "moan.speed2.public.boyfriend": [
            _("I'm cheating... in public... oh god this is so wrong..."),

            _("If anyone sees us... if HE finds out..."),

            _("This is the worst thing I've ever done... and it feels amazing..."),

        ],
        "moan.speed2.public.girlfriend": [
            _("I'm cheating on her... with a man... in public... oh god this is so wrong..."),

            _("If anyone sees me with a guy... if SHE finds out..."),

            _("Cheating on my girlfriend with a man, in public... and it feels amazing..."),

        ],
        "moan.speed2.boyfriend.cute": [
            _("I feel so guilty... but you make me feel so good..."),

            _("He's probably calling me right now... and I'm here with you..."),

            _("I can feel you throbbing inside me..."),

        ],
        "moan.speed2.girlfriend.cute": [
            _("I feel so guilty... she's so sweet to me... but this feels so good..."),

            _("She's probably texting me right now... and I'm here moaning for a man..."),

            _("I can feel you throbbing inside me... she could never give me this..."),

        ],
        "moan.speed2.boyfriend.hardcore": [
            _("Fuck me harder than he ever could..."),

            _("You're already better... don't stop..."),

            _("Yes... harder... your dick feels incredible..."),

        ],
        "moan.speed2.girlfriend.hardcore": [
            _("Fuck me like she never could... give me that cock..."),

            _("She can't even compete with this... don't stop..."),

            _("Yes... harder... nothing she has compares to a real dick..."),

        ],

        # ══════════════════════════════════════════════════════════
        #  TRAIT COMBO — Moans Speed 3
        # ══════════════════════════════════════════════════════════

        "moan.speed3.cum_slut.hardcore": [
            _("DESTROY ME! DON'T YOU DARE STOP! AAAH!"),

            _("HARDER! BREAK ME! I WANT ALL OF IT!"),

            _("YES YES YES! FUCK ME LIKE YOU MEAN IT!"),

        ],
        "moan.speed3.cum_slut.cute": [
            _("I c-can't... it's too good... I'm losing my mind!"),

            _("Oh god oh god... I love this... I love YOU...!"),

            _("I'm such a mess... but please don't stop!"),

        ],
        "moan.speed3.virgin.cute": [
            _("My first time and I'm already... AAAH! This is too much!"),

            _("I never knew... oh GOD... I didn't know it could feel like THIS!"),

            _("YES! Right there! Your dick is so DEEP!"),

        ],
        "moan.speed3.virgin.hardcore": [
            _("VIRGIN? NOT ANYMORE! GIVE IT TO ME!"),

            _("Who cares it's my first time?! HARDER!"),

            _("I should be gentle about this? FUCK THAT!"),

        ],
        "moan.speed3.camera_lover.cum_slut": [
            _("FILM THIS! FILM ME CUMMING! I WANT TO WATCH IT!"),

            _("The camera... seeing everything... GOD THAT MAKES IT HOTTER!"),

            _("YOUR COCK! I NEED YOUR CUM! ALL OF IT!"),

        ],
        "moan.speed3.public.cum_slut": [
            _("I DON'T CARE WHO HEARS! DON'T STOP!"),

            _("LET THEM WATCH! I WANT EVERYONE TO HEAR!"),

            _("FUCK! Your thick cock is destroying me!"),

        ],
        "moan.speed3.boyfriend.cum_slut": [
            _("HE COULD NEVER! YOU'RE SO MUCH BETTER! FUCK!"),

            _("I'M HIS GIRLFRIEND BUT I'M YOUR SLUT! AAAH!"),

            _("My boyfriend's DICK could NEVER do THIS! FUCK!"),

        ],
        "moan.speed3.girlfriend.cum_slut": [
            _("SHE COULD NEVER GIVE ME THIS! YOUR COCK IS SO MUCH BETTER! FUCK!"),

            _("I'M HER GIRLFRIEND BUT I'M ADDICTED TO YOUR COCK! AAAH!"),

            _("My girlfriend could NEVER do THIS! I NEED DICK! FUCK!"),

            _("NO WOMAN ALIVE COULD GIVE ME WHAT YOUR COCK DOES! I'M... AAAH!"),

            _("I WAS A FOOL TO THINK I DIDN'T NEED THIS! HARDER! DON'T STOP!"),

            _("MY BODY WAS MADE FOR COCK! SHE COULD NEVER UNDERSTAND! FUCK!"),

        ],

        # ══════════════════════════════════════════════════════════
        #  TRAIT COMBO — Girl Cum
        # ══════════════════════════════════════════════════════════

        "girl_cum.cum_slut.hardcore": [
            _("FUCK! I'M CUMMING! DON'T YOU DARE SLOW DOWN! HARDER!"),

            _("I'M CUMMING SO HARD! MORE MORE MORE!"),

            _("THAT'S IT! MAKE ME CUM UNTIL I CAN'T MOVE!"),

        ],
        "girl_cum.cum_slut.cute": [
            _("I'm... I'm cumming! Oh god... hold me... HOLD ME! AAAH!"),

            _("It's happening... I'm so embarrassed but... AAAH!"),

            _("I'm... oh... I'm cumming... your cock... mmm..."),

        ],
        "girl_cum.virgin.cute": [
            _("W-what's happening to me?! I've never... AAAH! Oh my GOD!"),

            _("Is this... is this what it feels like?! My first... AAAH!"),

            _("I'm... oh... I'm cumming... your cock... mmm..."),

        ],
        "girl_cum.virgin.hardcore": [
            _("FIRST TIME AND I'M ALREADY CUMMING THIS HARD?!"),

            _("My virginity is GONE and I'm cumming like a SLUT!"),

            _("AAAH! I'm cumming so hard on your dick!"),

        ],
        "girl_cum.boyfriend.cum_slut": [
            _("He NEVER made me cum like THIS! YOU'RE AMAZING! AAAH!"),

            _("I'm cumming harder than I ever did with him! FUCK!"),

            _("I'm cumming! My boyfriend never gets me off like this!"),

        ],
        "girl_cum.girlfriend.cum_slut": [
            _("She NEVER made me cum like THIS! A cock is... YOU'RE AMAZING! AAAH!"),

            _("I'm cumming harder from a man than I ever did with her! FUCK!"),

            _("I'm cumming! My girlfriend never gets me off like a real cock does!"),

        ],
        "girl_cum.camera_lover.cum_slut": [
            _("FILM ME CUMMING! I WANT TO SEE THIS FACE! AAAH!"),

            _("The camera... catching me cumming... GOD YES!"),

            _("FILM MY FACE! I'm cumming on your cock! This is GOLD!"),

        ],
        "girl_cum.public.cute": [
            _("I'm... I can't hold back... MMMMPH! *covers mouth*"),

            _("Someone's going to hear me... I can't... I CAN'T BE QUIET!"),

            _("I'm... oh... I'm cumming... your cock... mmm..."),

        ],
        "girl_cum.cowgirl.boyfriend": [
            _("I'm cumming riding you! He could NEVER make me cum on top! AAAH!"),

            _("I'm... I'm cumming for you, not him... on top of another man... AAAH!"),

            _("My boyfriend could NEVER... I'm cumming so hard on your cock! YES!"),

        ],
        "girl_cum.cowgirl.girlfriend": [
            _("I'm cumming riding a man! She could NEVER fill me like this! AAAH!"),

            _("I'm... I'm cumming on your cock, not for her... on top of you... AAAH!"),

            _("My girlfriend could NEVER give me this... I'm cumming so hard on your cock! YES!"),

        ],
        "girl_cum.cowgirl.first_time": [
            _("I'm... on top and I'm... is this what it feels like?! AAAH!"),

            _("My first time and I'm cumming riding you! I didn't know I could... AAAH!"),

            _("I'm in control and I'm LOSING it! This is my first... AAAH!"),

        ],

        # ══════════════════════════════════════════════════════════
        #  TRAIT COMBO — Girl Post-Cum
        # ══════════════════════════════════════════════════════════

        "girl_post_cum.cum_slut.hardcore": [
            _("That was one. I want at least three more."),

            _("Don't you dare stop. That was just warm-up."),

            _("Again. Make me cum again. NOW."),

        ],
        "girl_post_cum.cum_slut.cute": [
            _("Oh my god... that was amazing... can we... can we do that again?"),

            _("I'm still trembling... but I already want more..."),

            _("Oh god... that was incredible... your cock..."),

        ],
        "girl_post_cum.virgin.cute": [
            _("So that's what an orgasm feels like... wow... I had no idea..."),

            _("My first time cumming with someone... I feel so special right now..."),

            _("My legs are shaking... your thick cock did this to me..."),

        ],
        "girl_post_cum.boyfriend.cute": [
            _("He never makes me feel like that... I feel so guilty but so good..."),

            _("What does it say about us that you make me cum harder than him?"),

            _("My legs are shaking... your thick cock did this to me..."),

        ],
        "girl_post_cum.girlfriend.cute": [
            _("She never makes me feel like that... I feel so confused but so good..."),

            _("What does it say about me that a man makes me cum harder than my girlfriend?"),

            _("My legs are shaking... her fingers could never do what your cock just did..."),

        ],
        "girl_post_cum.cowgirl.boyfriend": [
            _("I just came riding another man... he's never made me cum on top..."),

            _("That was... I was in control the whole time. He never gives me that."),

            _("I came harder on top of you than I ever have with him... what does that say about me?"),

        ],
        "girl_post_cum.cowgirl.girlfriend": [
            _("I just came riding a man... she's never been able to fill me like that..."),

            _("That was... I was in control, riding a cock. She could never give me that."),

            _("I came harder on top of a man than I ever have with her... what does that say about me?"),

        ],
        "girl_post_cum.cowgirl.cum_slut": [
            _("I came on top of you... now it's YOUR turn. Don't you dare hold back."),

            _("One down. But I want YOUR orgasm too. Stay inside me."),

            _("That was just the warmup. I want to feel you cum while I'm still on top."),

        ],

        # ══════════════════════════════════════════════════════════
        #  TRAIT COMBO — Cum Inside
        # ══════════════════════════════════════════════════════════

        "cum_inside.cum_slut.hardcore": [
            _("FUCK YES! Fill me up! Every last fucking drop!"),

            _("That's where it belongs! Deep inside me! Don't waste a DROP!"),

            _("I can feel you pumping it all in... MORE!"),

        ],
        "cum_inside.cum_slut.cute": [
            _("I can feel it... all warm inside me... I love this feeling so much..."),

            _("You filled me up... it's so warm... I feel so complete..."),

            _("I trusted you... and your cock just... inside me..."),

        ],
        "cum_inside.virgin.cute": [
            _("You... came inside me... for my first time? It's so warm..."),

            _("I can feel it all... my first time... oh my god..."),

            _("My pussy is full of your cum... I can't believe I let you..."),

        ],
        "cum_inside.virgin.cum_slut": [
            _("My first time and you filled me up... I already love this..."),

            _("I just lost my virginity with a creampie... I need more of this..."),

            _("So warm inside me... every drop... fuck..."),

        ],
        "cum_inside.hate_cum.boyfriend": [
            _("Inside me?! I don't even let my boyfriend do that! What have you DONE?!"),

            _("He always uses a condom and YOU cum inside me?! This is the worst!"),

            _("You came so deep... I can feel it all..."),

        ],
        "cum_inside.hate_cum.girlfriend": [
            _("Inside me?! What have you DONE?! Your cum inside me?!"),

            _("My girlfriend never puts anything disgusting inside me and YOU cum in me raw?! This is the worst!"),

            _("Your cum inside me... I can feel it all... this is so wrong..."),

        ],
        "cum_inside.boyfriend.cum_slut": [
            _("He always pulls out... and you just pumped me full. I love it."),

            _("My boyfriend would die knowing another man's cum is inside me..."),

            _("This is what I've always wanted... he could never give me this."),

        ],
        "cum_inside.girlfriend.cum_slut": [
            _("She could never put anything inside me like this... and you just pumped me full. I love it."),

            _("My girlfriend would die knowing your cum is inside me..."),

            _("This is what I secretly always wanted... no woman could ever give me this."),

        ],
        "cum_inside.public_fetish.cum_slut": [
            _("Filled up where anyone could see... this is my ultimate fantasy..."),

            _("Now I'm walking around in public with your cum dripping out of me..."),

            _("So warm inside me... every drop... fuck..."),

        ],
        "cum_inside.camera_lover.cum_slut": [
            _("Please tell me you filmed that... I want to see the cum dripping out..."),

            _("That creampie on camera... that's my favorite video now."),

            _("So warm inside me... every drop... fuck..."),

        ],

        # ══════════════════════════════════════════════════════════
        #  TRAIT COMBO — Cum Outside
        # ══════════════════════════════════════════════════════════

        "cum_outside.cum_slut.hardcore": [
            _("Why outside?! That should've been INSIDE me! Ugh!"),

            _("What a waste... next time, don't you dare pull out."),

            _("So much cum... I wanted it in me but this is hot too..."),

        ],
        "cum_outside.cum_slut.cute": [
            _("Aw... I was hoping you'd finish inside me... but it's still nice..."),

            _("Next time... inside, okay? I want to feel that warmth..."),

            _("Your thick cock sprayed so much... I want it on my tongue..."),

        ],
        "cum_outside.hate_cum.cute": [
            _("Thank goodness you pulled out... I was so scared..."),

            _("Good... I feel so much better knowing it's not inside me..."),

            _("I can feel it running down... that's... a lot of cum..."),

        ],
        "cum_outside.virgin.cute": [
            _("So much... is it always like this? That was my first time seeing..."),

            _("Oh wow... it's warm... I've never seen it happen before..."),

            _("Oh wow... that's a lot... your cum is everywhere..."),

        ],

        # ══════════════════════════════════════════════════════════
        #  TRAIT COMBO — Cum Face
        # ══════════════════════════════════════════════════════════

        "cum_face.cum_slut.hardcore": [
            _("Cover my face! I want to be GLAZED!"),

            _("More! Paint my whole fucking face! I want it dripping!"),

            _("More! Cover my face in your thick cum!"),

        ],
        "cum_face.cum_slut.cute": [
            _("It's on my face... I'm embarrassed but... I kind of love it..."),

            _("Oh my... it's so warm on my skin... is it weird that I like it?"),

            _("My face is dripping with your cum and I love it!"),

        ],
        "cum_face.camera_lover.cum_slut": [
            _("Film my face covered in your cum... this is CONTENT!"),

            _("I need a picture of this... with your cum on my face... so hot."),

            _("All over my face! I love the taste of your cum!"),

        ],
        "cum_face.hate_cum.cute": [
            _("N-no! My face! Get it off! Please help me clean it! *crying*"),

            _("I can feel it dripping... please... get me a towel... I hate this..."),

            _("On my FACE?! I hate your cum on me..."),

        ],

        # ══════════════════════════════════════════════════════════
        #  TRAIT COMBO — Cum Mouth
        # ══════════════════════════════════════════════════════════

        "cum_mouth.cum_slut.hardcore": [
            _("Mmm FUCK that tastes good! Give me another load!"),

            _("Straight down my throat... I swallowed every drop!"),

            _("Cum down my throat. I want to choke on your load."),

        ],
        "cum_mouth.cum_slut.cute": [
            _("It's salty... but I think I like it... is that weird?"),

            _("I swallowed it all... I'm embarrassed but it tasted... good..."),

            _("You came in my mouth... that was really intimate..."),

        ],
        "cum_mouth.virgin.cute": [
            _("I... I never tasted... is it always this warm? Oh my..."),

            _("My first time tasting this... it's so... different from what I imagined..."),

            _("Your cum is... salty... there's so much in my mouth..."),

        ],

        # ══════════════════════════════════════════════════════════
        #  TRAIT COMBO — Cum Tits
        # ══════════════════════════════════════════════════════════

        "cum_tits.cum_slut.hardcore": [
            _("Cover them! MORE! I want them completely glazed!"),

            _("My tits are glazed in your cum and I love it..."),

        ],
        "cum_tits.cum_slut.submissive": [
            _("Fuck yes! All over my tits! Mark them as yours!"),

            _("My tits are yours... cover them whenever you want, I'll never say no."),

            _("I'll keep your cum on me until you tell me I can wipe it off."),

        ],
        "cum_tits.cum_slut.cute": [
            _("It's dripping off my nipples... is it weird that I find it cute?"),

            _("Oh... all over my chest... it's so warm... I actually love this..."),

            _("Cover my tits in your cum! I want to see it drip!"),

        ],
        "cum_tits.camera_lover.cum_slut": [
            _("Get a picture of this! My tits covered in your cum... perfection!"),

            _("Film this view... cum dripping off my chest... they'll love it."),

            _("Cover my tits in your cum! I want to see it drip!"),

        ],

        # ══════════════════════════════════════════════════════════
        #  TRAIT COMBO — Creampie Request
        # ══════════════════════════════════════════════════════════

        "creampie_req.cum_slut.hardcore": [
            _("Fill me up! I don't care how rough you are! Cum inside me!"),

            _("Pump every last drop deep inside me! I need it!"),

            _("Breed me! HARD! I want to be dripping with your cum!"),

        ],
        "creampie_req.cum_slut.cute": [
            _("I know it's embarrassing to ask, but... please cum inside me..."),

            _("I want to feel your warmth... inside me... please..."),

            _("Inside... please... I want to feel you fill me up..."),

        ],
        "creampie_req.boyfriend.cum_slut": [
            _("He always pulls out... I want YOU to fill me. Please."),

            _("Give me what my boyfriend never does... cum inside me..."),

            _("Don't pull out... I need your cum in me..."),

        ],
        "creampie_req.girlfriend.cum_slut": [
            _("She could never put anything like this inside me... I want YOU to fill me. Please."),

            _("Give me what my girlfriend never could... your cum inside me..."),

            _("Don't pull out... I need a real load in me... something she could never give..."),

        ],
        "creampie_req.camera_lover.cum_slut": [
            _("Film the creampie... I want to watch it drip out later..."),

            _("On camera... cum inside me... I want to see this footage..."),

            _("I want it inside... every drop from your thick cock..."),

        ],

        # ══════════════════════════════════════════════════════════
        #  TRAIT COMBO — Dressup
        # ══════════════════════════════════════════════════════════

        "dressup.cum_slut.hardcore": [
            _("Already? I could go another round... or three."),

            _("Stop staring and get your cock out already."),

        ],
        "dressup.cum_slut.submissive": [
            _("Getting dressed feels wrong. I should be naked for you always."),

            _("Do I have to get dressed? Tell me and I'll stay just like this for you."),

            _("Call me whenever you need to empty yourself... I'll be ready for you."),

        ],
        "dressup.cum_slut.cute": [
            _("Do I have to get dressed? I was so comfortable like this..."),

            _("That was wonderful... I'm still tingling all over..."),

            _("Undressing for your cock... I'm already dripping..."),

        ],
        "dressup.virgin_lost.cute": [
            _("I'm not a virgin anymore... wow. Thank you for being so gentle..."),

            _("I'll never forget this... my first time was perfect because of you."),

            _("Turn around while I... no, it's okay... look..."),

        ],
        "dressup.boyfriend.cum_slut": [
            _("My boyfriend could never... that was incredible. I want more."),

            _("What I just did is so much worse than he'd ever imagine... and I loved it."),

            _("Undressing for your cock... I'm already dripping..."),

        ],
        "dressup.girlfriend.cum_slut": [
            _("My girlfriend could never give me what you just did... that was incredible. I want more."),

            _("What I just did is so much worse than she'd ever imagine... with a man... and I loved it."),

            _("Undressing for you... my girlfriend would die... I'm already dripping..."),

        ],
        "dressup.public.cute": [
            _("Quick! Help me get dressed before someone comes!"),

            _("Oh god, do I look okay? Can people tell what we just did?"),

            _("Like what you see? Your cock is already responding..."),

        ],
        "dressup.public.hardcore": [
            _("Let them see. I don't care. That was worth it."),

            _("Eyes up here... or maybe not~"),

        ],
        "dressup.public.submissive": [
            _("If anyone saw us... good. They know I'm taken now."),

            _("Should I get dressed? You decide... out here I'll do whatever you say."),

            _("I let you use me right out in the open... and I'd do it again if you told me to."),

        ],
        "dressup.camera_lover.cum_slut": [
            _("Did you get good footage? I want to watch it later tonight..."),

            _("That video is going to be my favorite thing ever recorded."),

            _("Like what you see? Your cock is already responding..."),

        ],

        # ══════════════════════════════════════════════════════════
        #  TRAIT COMBO — Boyfriend + Camera
        # ══════════════════════════════════════════════════════════

        # --- Moans ---
        "moan.speed1.boyfriend.camera_lover": [
            _("Mmm... my boyfriend has no idea... I kinda wish this was being recorded..."),

            _("This is so wrong... if someone filmed this... mm..."),

            _("Ahh... I wonder what we'd look like on camera right now..."),

        ],
        "moan.speed1.girlfriend.camera_lover": [
            _("Mmm... my girlfriend has no idea I'm with a man... I wish this was on camera..."),

            _("Me, the 'lesbian'... with a guy... if someone filmed this... mm..."),

            _("Ahh... I wonder what she'd think seeing me on camera with a man..."),

        ],
        "moan.speed1.boyfriend.camera_hater": [
            _("Mm... there aren't any cameras here, right? ...right?"),

            _("Ahh... my boyfriend can never see this... nobody can..."),

            _("Please... no one can ever know about this..."),

        ],
        "moan.speed1.girlfriend.camera_hater": [
            _("Mm... there aren't any cameras here, right? If she saw me with a man..."),

            _("Ahh... my girlfriend can never see this... no one can know I'm with a guy..."),

            _("Please... if there's proof of me doing this... she'd never forgive me..."),

        ],
        "moan.speed2.boyfriend.camera_lover": [
            _("Oh god... this would go viral if someone saw... aaah..."),

            _("My boyfriend has no idea... fuck, I wish I had a camera right now..."),

            _("Ahh... imagine if he could see this... mmm..."),

        ],
        "moan.speed2.girlfriend.camera_lover": [
            _("Oh god... me taking cock on camera... this would break the internet... aaah..."),

            _("My girlfriend has no idea... fuck, I wish I could film what a man does to me..."),

            _("Ahh... imagine if she could see me loving this... mmm..."),

        ],
        "moan.speed2.boyfriend.camera_hater": [
            _("Ahh... promise me... no one... is watching... oh..."),

            _("My boyfriend... no one can record this... please... ahh..."),

            _("Oh god... if there's a camera... I swear... nnh..."),

        ],
        "moan.speed2.girlfriend.camera_hater": [
            _("Ahh... promise me... no one can see me with a man... oh..."),

            _("My girlfriend... no one can record me doing this... please... ahh..."),

            _("Oh god... if anyone films me taking cock... she'd find out... nnh..."),

        ],
        "moan.speed3.boyfriend.camera_lover": [
            _("FUCK! If my boyfriend could SEE this! AHHH! Film it! Film me!"),

            _("OH GOD! I want this on camera! I want PROOF of how good this feels!"),

            _("YES! My boyfriend could NEVER! Someone should be recording this!"),

        ],
        "moan.speed3.girlfriend.camera_lover": [
            _("FUCK! If my girlfriend could SEE me taking cock! AHHH! Film it! Film me!"),

            _("OH GOD! I want this on camera! Proof that I LOVE dick! AHHH!"),

            _("YES! She could NEVER do this! Someone record her girlfriend loving cock!"),

        ],
        "moan.speed3.boyfriend.camera_hater": [
            _("OH GOD! No one... no one can EVER see this! AHHH!"),

            _("FUCK! If my boyfriend finds proof... oh god... AHHHH!"),

            _("YES! But if anyone... is recording... I'll DIE! Oh god!"),

        ],
        "moan.speed3.girlfriend.camera_hater": [
            _("OH GOD! No one can see me with a man! EVER! AHHH!"),

            _("FUCK! If my girlfriend finds proof of me taking cock... AHHHH!"),

            _("YES! But if anyone is recording... she'll know I like dick... I'll DIE!"),

        ],

        # --- Girl cum ---
        "girl_cum.boyfriend.camera_lover": [
            _("I'm... I'm cumming! Oh god, I wish this was on camera! My boyfriend never... AHHHH!"),

            _("CUMMING! This would be... the best footage... of my LIFE! He could never!"),

            _("I'm CUMMING! Tell me the camera got that!"),

        ],
        "girl_cum.girlfriend.camera_lover": [
            _("I'm... I'm cumming from a cock! Oh god, I wish this was on camera! My girlfriend never... AHHHH!"),

            _("CUMMING! A man is making me... this would be the best footage of my LIFE! She could never!"),

            _("I'm CUMMING on a cock! Tell me the camera got that!"),

        ],
        "girl_cum.boyfriend.camera_hater": [
            _("I'm cumming! Oh god... no one... can ever see this... AHHHH!"),

            _("CUMMING! If my boyfriend... ever finds proof... oh god!"),

            _("Your cock made me cum harder than his ever could!"),

        ],
        "girl_cum.girlfriend.camera_hater": [
            _("I'm cumming from a man! Oh god... no one can ever see this... AHHHH!"),

            _("CUMMING! If my girlfriend ever finds proof I came on a cock... oh god!"),

            _("Your cock made me cum harder than she ever could!"),

        ],
        "girl_post_cum.boyfriend.camera_lover": [
            _("That was incredible... my boyfriend has never made me cum like that. I need a recording of that..."),

            _("If he could see what just happened... part of me wants him to..."),

            _("That orgasm... your dick... I can't think straight..."),

        ],
        "girl_post_cum.girlfriend.camera_lover": [
            _("That was incredible... my girlfriend has never made me cum like that. I need a recording of a cock doing this to me..."),

            _("If she could see what a man just did to me... part of me wants her to know..."),

            _("That orgasm... your cock... no woman has ever made me feel like this..."),

        ],
        "girl_post_cum.boyfriend.camera_hater": [
            _("That was... oh god. My boyfriend can never find out. Please delete any messages about this."),

            _("No one can ever know I just did that. No evidence. None."),

            _("I can still feel you inside me... throbbing..."),

        ],
        "girl_post_cum.girlfriend.camera_hater": [
            _("That was... oh god. My girlfriend can never find out I came for a man. Please delete everything."),

            _("No one can ever know I just did that with a guy. No evidence. None."),

            _("I can still feel you inside me... throbbing... she could never give me this..."),

        ],

        # --- Cum locations ---
        "cum_inside.boyfriend.camera_lover": [
            _("You came inside me... my boyfriend has no idea. I almost want to take a photo..."),

            _("Another man's cum inside me... this would be the ultimate footage..."),

            _("My boyfriend would die if he saw this. Part of me wants him to."),

        ],
        "cum_inside.girlfriend.camera_lover": [
            _("A man came inside me... my girlfriend has no idea. I almost want to take a photo..."),

            _("Your cum inside me... this would be the ultimate footage..."),

            _("My girlfriend would die if she saw this. Part of me wants her to."),

        ],
        "cum_inside.boyfriend.camera_hater": [
            _("You came inside me... my boyfriend can NEVER find out. No evidence. Promise me."),

            _("Oh god... there's proof inside me now... my boyfriend..."),

            _("If anyone recorded that... if there's any camera... I need to leave."),

        ],
        "cum_inside.girlfriend.camera_hater": [
            _("A man came inside me... my girlfriend can NEVER find out. No evidence. Promise me."),

            _("Oh god... there's proof of a man inside me now... my girlfriend..."),

            _("If anyone recorded me taking your cum... if there's any camera... I need to leave."),

        ],
        "cum_outside.boyfriend.camera_lover": [
            _("My boyfriend has no idea you just came on me... I wish I had a photo of this."),

            _("Look at me... covered in another man's cum. This would break the internet."),

            _("His loads are nothing like yours... so much..."),

        ],
        "cum_outside.girlfriend.camera_lover": [
            _("My girlfriend has no idea a man just came on me... I wish I had a photo of this."),

            _("Look at me... covered in your cum. This would break the internet."),

            _("She could never give me this... so much cum... so warm..."),

        ],
        "cum_outside.boyfriend.camera_hater": [
            _("Clean it up! Quick! If my boyfriend sees any evidence..."),

            _("Get it off me... no photos... my boyfriend can never know."),

            _("That's a visual I never want on video..."),

        ],
        "cum_outside.girlfriend.camera_hater": [
            _("Clean it up! Quick! If my girlfriend sees any evidence of a man on me..."),

            _("Get it off me... no photos... my girlfriend can never know I was with a guy."),

            _("A lesbian covered in cum... that's a visual I never want on video..."),

        ],
        "cum_face.boyfriend.camera_lover": [
            _("My boyfriend has no idea another man just came on my face... I wish this was on camera."),

            _("If he could see me right now... another man's cum all over my face... fuck, that's hot."),

            _("Get a close-up of my face covered in your cum!"),

        ],
        "cum_face.girlfriend.camera_lover": [
            _("My girlfriend has no idea a man just came on my face... I wish this was on camera."),

            _("If she could see her girlfriend right now... your cum all over my face... fuck, that's hot."),

            _("Get a close-up of my face covered in your cum! She'd lose her mind!"),

        ],
        "cum_face.boyfriend.camera_hater": [
            _("Oh god... my boyfriend... get it off before someone takes a picture..."),

            _("If anyone saw my face right now... I'd have to disappear. Wipe it off. Now."),

            _("My boyfriend doesn't cum on my face... you just did..."),

        ],
        "cum_face.girlfriend.camera_hater": [
            _("Oh god... my girlfriend... get it off before someone takes a picture of me like this..."),

            _("If anyone saw your cum on my face right now... I'd have to disappear. Wipe it off. Now."),

            _("My girlfriend has never seen me with cum on my face... a man just did this to me..."),

        ],
        "cum_mouth.boyfriend.camera_lover": [
            _("My boyfriend has never finished in my mouth... and I'm swallowing yours. Film-worthy moment."),

            _("If he could see what's in my mouth right now... I almost want to show him."),

            _("I swallowed another man's cum... oh god..."),

        ],
        "cum_mouth.girlfriend.camera_lover": [
            _("My girlfriend has never put anything like this in my mouth... and I'm swallowing it. Film-worthy moment."),

            _("If she could see what's in my mouth right now... I almost want to show her."),

            _("I swallowed your cum... me, her girlfriend... oh god..."),

        ],
        "cum_mouth.boyfriend.camera_hater": [
            _("My boyfriend can never know I swallowed another man's... ugh. Delete your messages about this."),

            _("No one can ever see this. I just swallowed... oh god. No evidence."),

            _("My boyfriend never cums in my mouth... you just did..."),

        ],
        "cum_mouth.girlfriend.camera_hater": [
            _("My girlfriend can never know I swallowed your... ugh. Delete your messages about this."),

            _("No one can ever see this. A lesbian swallowing cum... oh god. No evidence."),

            _("She'd never believe her girlfriend just let a man cum in her mouth..."),

        ],
        "cum_tits.boyfriend.camera_lover": [
            _("My boyfriend has no idea another man just came on my tits... this would look so good on camera."),

            _("If he could see my chest right now... covered in your cum... part of me wants to send a pic."),

            _("Get a close-up of your cum on my chest... perfect shot..."),

        ],
        "cum_tits.girlfriend.camera_lover": [
            _("My girlfriend has no idea a man just came on my tits... this would look so good on camera."),

            _("If she could see my chest right now... covered in your cum... part of me wants to send a pic."),

            _("Get a close-up of your cum on my chest... she'd die seeing this shot..."),

        ],
        "cum_tits.boyfriend.camera_hater": [
            _("Get it off my tits before someone sees! My boyfriend can never find out!"),

            _("If anyone photographed this... my boyfriend... clean it up. Fast."),

            _("My boyfriend never cums on my tits like this..."),

        ],
        "cum_tits.girlfriend.camera_hater": [
            _("Get it off my tits before someone sees! My girlfriend can never find out a man did this!"),

            _("If anyone photographed this... my girlfriend... clean it up. Fast."),

            _("She touches my chest with such care... and you just covered them in cum..."),

        ],

        # --- Creampie request ---
        "creampie_req.boyfriend.camera_lover": [
            _("Cum inside me... I want proof of what we did. My boyfriend would lose his mind..."),

            _("Fill me up... imagine if this was on camera. My boyfriend could never."),

            _("I want it inside... every drop from your thick cock..."),

        ],
        "creampie_req.girlfriend.camera_lover": [
            _("Cum inside me... I want proof of what a man did to me. My girlfriend would lose her mind..."),

            _("Fill me up... imagine me getting creampied on camera. My girlfriend could never give me this."),

            _("I want it inside... every drop from your thick cock... she could never..."),

        ],
        "creampie_req.boyfriend.camera_hater": [
            _("Cum inside me... but no one can ever see proof of this. My boyfriend..."),

            _("Fill me up... but promise me you'll never tell anyone. No photos. No videos."),

            _("I want it inside... every drop from your thick cock..."),

        ],
        "creampie_req.girlfriend.camera_hater": [
            _("Cum inside me... but no one can ever see proof a man did this to me. My girlfriend..."),

            _("Fill me up... but promise me you'll never tell anyone. No photos. No videos. She can never know I took cock."),

            _("I want it inside... every drop... but if anyone films me getting creampied..."),

        ],

        # --- Dressup ---
        "dressup.boyfriend.camera_lover": [
            _("My boyfriend has no idea what I just did... I almost want to tell him. Or show him."),

            _("Getting dressed after cheating... I need to delete any evidence. ...Or do I?"),

            _("My boyfriend hasn't seen me undress like this in a while..."),

        ],
        "dressup.girlfriend.camera_lover": [
            _("My girlfriend has no idea I just slept with a man... I almost want to tell her. Or show her."),

            _("Getting dressed after being with a guy... I need to delete any evidence. ...Or do I?"),

            _("My girlfriend hasn't seen me this flushed... a man did this to me..."),

        ],
        "dressup.boyfriend.camera_hater": [
            _("My boyfriend can never know. Check your phone... delete any texts about this."),

            _("I need to make sure there's zero evidence of what we just did. My boyfriend..."),

            _("I'm taking my clothes off for another man... again..."),

        ],
        "dressup.girlfriend.camera_hater": [
            _("My girlfriend can never know I was with a man. Check your phone... delete everything about this."),

            _("I need to make sure there's zero evidence I was with a guy. My girlfriend..."),

            _("I'm getting dressed after being with a man... she can never see proof of this..."),

        ],

        # --- Condom events ---
        "condom_ask.boyfriend.camera_lover": [
            _("Take it off... I want to feel everything. The footage would be insane..."),

            _("If you're gonna cheat with me at least make it worth recording... no condom."),

            _("Please tell me you have one... your cock is huge..."),

        ],
        "condom_ask.boyfriend_sex.camera_lover": [
            _("Take it off... I want to feel everything. My boyfriend never gets this raw... the footage would be insane..."),

            _("If you're gonna cheat with me at least make it worth recording... no condom."),

            _("Protection? I don't want your raw dick without one."),

        ],
        "condom_ask.girlfriend_sex.camera_lover": [
            _("Take it off... I want to feel a real cock raw. My girlfriend could never give me this... the footage would be insane..."),

            _("A lesbian going raw with a man on camera... make it worth the betrayal... no condom."),

            _("Protection? I don't want your raw dick without one... I've never done this with a man..."),

        ],
        "condom_ask.boyfriend.camera_hater": [
            _("Take it off... but there can never be proof of this. My boyfriend..."),

            _("Raw with someone who isn't my boyfriend... god. Promise me no one is watching."),

            _("Please tell me you have one... your cock is huge..."),

        ],
        "condom_ask.girlfriend.camera_lover": [
            _("Take it off... I want to feel a real cock raw. The footage would be insane..."),

            _("A lesbian going raw with a man on camera... my girlfriend would die... no condom."),

            _("Please tell me you have one... I've never taken a cock without protection..."),

        ],
        "condom_ask.girlfriend.camera_hater": [
            _("Take it off... but there can never be proof of me going raw with a man. My girlfriend..."),

            _("Raw with a man while I have a girlfriend... god. Promise me no one is watching."),

            _("Please tell me you have one... taking a man raw is terrifying enough without cameras..."),

        ],

        # ══════════════════════════════════════════════════════════
        #  TRAIT COMBO — Condom Events
        # ══════════════════════════════════════════════════════════

        "condom_force.cum_slut.hardcore": [
            _("That thing is coming OFF. I need your raw cock inside me NOW!"),

            _("I can't stand this barrier! Give me the real thing! HARD!"),

            _("Condoms ruin the feeling of your thick dick. Skip it."),

        ],
        "condom_ask.cum_slut.hardcore": [
            _("Take that fucking thing off. I need to feel you raw."),

            _("I NEED your cock bare inside me. Take it off. Now."),

            _("Condoms ruin the feeling of your thick dick. Skip it."),

        ],
        "condom_ask.cum_slut.cute": [
            _("Can we... um... take that off? I want to feel you... really feel you..."),

            _("I'm shy to ask but... I want it without the condom... please?"),

            _("Can we please use one? I feel safer with your big cock wrapped..."),

        ],
        "condom_ask.virgin.cute": [
            _("I know it's safer but... for my first time I want to really feel you..."),

            _("Can we take it off? I want my first time to be... real."),

            _("Condom? Your thick cock needs to be wrapped."),

        ],
        "condom_denied.cum_slut.hardcore": [
            _("UGH! Fine! But I'm going to ride you so hard you regret keeping it on!"),

            _("Fucking condom. I WILL get you raw eventually."),

            _("No condom... I need to feel every inch and every drop..."),

        ],
        "cum_condom.cum_slut.hardcore": [
            _("What a waste. That load should've been pumped INSIDE me."),

            _("I'm furious. All that cum wasted in a stupid condom."),

            _("I can see how much you came... I wish it was inside me..."),

        ],
        "cum_condom.cum_slut.cute": [
            _("Aw... I wish I could've felt that inside me..."),

            _("The condom caught it all... I kind of wanted to feel it..."),

            _("All that cum trapped in the condom... what a waste..."),

        ],

        # ══════════════════════════════════════════════════════════
        #  TRAIT COMBO — Cheater combos
        # ══════════════════════════════════════════════════════════

        # --- Cheater + Cum Slut ---
        "moan.speed1.cheater.cum_slut": [
            _("Mmm... my %(pl)s could never make me feel this needy..."),

            _("I want everything you have... things %(pp)s'll never give me..."),

            _("Don't stop... just like that..."),

        ],
        "moan.speed2.cheater.cum_slut": [
            _("Ahh... give me more... my %(pl)s has NO idea what I crave..."),

            _("Harder... I need all of it... %(pp)s could never satisfy me like this..."),

            _("Behind %(poss)s back and loving every thick inch..."),

        ],
        "moan.speed3.cheater.cum_slut": [
            _("FUCK! Give me EVERYTHING! My %(pl)s could NEVER! AHHH!"),

            _("YES! ALL OF IT! %(Pp)s has NO idea what a slut I am! OH GOD!"),

            _("OH FUCK! Your cock is splitting me open!"),

        ],
        "girl_cum.cheater.cum_slut": [
            _("CUMMING! My %(pl)s... could NEVER... make me cum like THIS!"),

            _("I'm cumming SO hard! %(Pp)s'll never know how much I need this!"),

            _("Yes yes YES! I'm cumming on your thick dick!"),

        ],
        "cum_inside.cheater.cum_slut": [
            _("Yes... fill me up. My %(pl)s's cum could never compare."),

            _("Another man's load inside me... and I love every drop. Sorry, %(pl)s."),

            _("%(Poss)s cum is boring. Yours? I want it all inside me. Every time."),

        ],
        "cum_face.cheater.cum_slut": [
            _("All over my face... my %(pl)s would die. And I love it."),

            _("Cover me. My %(pl)s has no idea how much I love another man's cum on me."),

            _("All over my face! I love the taste of your cum!"),

        ],
        "cum_mouth.cheater.cum_slut": [
            _("Swallowing another man's cum... my %(pl)s doesn't know what my mouth does."),

            _("I never swallow for %(po)s. But you? Every drop."),

            _("I'm swallowing all of it... your cock is delicious..."),

        ],
        "creampie_req.cheater.cum_slut": [
            _("Cum inside me. My %(pl)s gets the condom version. You get the real thing."),

            _("Fill me up. %(Pp)s'll never know another man's cum was inside me first today."),

            _("Fill me up! I need your cum inside my pussy!"),

        ],
        "dressup.cheater.cum_slut": [
            _("I need to clean up before my %(pl)s sees me... covered in another man's evidence."),

            _("Getting dressed with your cum still in me... going home to %(po)s like this..."),

            _("I can see you getting hard already... patience..."),

        ],

        # --- Cheater + Cute ---
        "moan.speed1.cheater.cute": [
            _("Mmm... I feel so guilty... but it feels so good..."),

            _("My %(pl)s would be so hurt if %(pp)s knew... ahh..."),

            _("I can feel every inch stretching me..."),

        ],
        "moan.speed2.cheater.cute": [
            _("Oh god... I'm such a bad partner... but I can't stop... ahh..."),

            _("%(Pp)s trusted me... and here I am... moaning for someone else..."),

            _("Don't stop... your cock hits every spot..."),

        ],
        "moan.speed3.cheater.cute": [
            _("OH GOD! I'm so sorry... %(pl)s... but this feels... AHHH!"),

            _("I'm TERRIBLE! But I can't... STOP! It feels too GOOD!"),

            _("OH GOD! Every inch! I feel EVERY inch!"),

        ],
        "girl_cum.cheater.cute": [
            _("I'm cumming... oh god... I came so hard for someone else... *sniff*"),

            _("CUMMING! My %(pl)s... I'm so sorry... but this is... ahh..."),

            _("I think I just... oh god... you made me feel so good..."),

        ],
        "cum_inside.cheater.cute": [
            _("You came inside me... my %(pl)s... I'm so sorry... *tears up*"),

            _("I let another man cum inside me... I'm such a terrible person..."),

            _("You... you came inside... I asked you not to... I can feel it all..."),

        ],
        "dressup.cheater.cute": [
            _("I need to go home and pretend this never happened... I feel so guilty..."),

            _("My %(pl)s will kiss me when I get home... and I just cheated on %(po)s..."),

            _("Don't stare too much... this is embarrassing..."),

        ],

        # --- Cheater + Hardcore ---
        "moan.speed1.cheater.hardcore": [
            _("Mmm... my %(pl)s is so boring in bed. This is already better."),

            _("Finally... someone who knows how to fuck. %(Pp)s's pathetic."),

            _("Don't stop... just like that..."),

        ],
        "moan.speed2.cheater.hardcore": [
            _("Ahh... HARDER! My %(pl)s could never fuck like this!"),

            _("YES! This is why I cheat! %(Pp)s doesn't know how to handle me!"),

            _("That's it... pound me with that thick dick..."),

        ],
        "moan.speed3.cheater.hardcore": [
            _("FUCK YES! My %(pl)s is NOTHING compared to this! DESTROY ME!"),

            _("HARDER! My %(pl)s could NEVER! %(Pp)s's PATHETIC! AHHHH!"),

            _("POUND me HARDER! Your big dick isn't enough yet!"),

        ],
        "cum_inside.cheater.hardcore": [
            _("Fill me up. HARD. My %(pl)s's weak loads don't even compare."),

            _("That's what I need. Raw, hard, and deep. %(Pp)s'll never know."),

            _("You came so deep... I can feel it all..."),

        ],
        "dressup.cheater.hardcore": [
            _("That was a real fuck. My %(pl)s doesn't even come close."),

            _("Getting dressed after the best sex of my life. And %(pp)s thinks I was at the store."),

            _("Take a good look before your cock takes over..."),

        ],

        # --- Cheater + Camera Lover ---
        # Theme: she WANTS the boyfriend to find the video / evidence

        # --- Moans ---
        "moan.speed1.cheater.camera_lover": [
            _("Mmm... I hope you're recording this... I'd love it if %(pp)s found the video..."),

            _("Ahh... imagine %(poss)s face if %(pp)s saw this footage... mmm..."),

            _("This feels amazing... and it'd feel even better knowing %(pp)s watched it later..."),

        ],
        "moan.speed2.cheater.camera_lover": [
            _("Ahh... film this... send it to %(po)s... let %(po)s see what %(pp)s's missing..."),

            _("Oh god... I want %(po)s to find this video on my phone... ahhh..."),

            _("Harder... make sure the camera gets my face... I want %(po)s to KNOW it's me..."),

        ],
        "moan.speed3.cheater.camera_lover": [
            _("FUCK! FILM THIS! I want %(po)s to SEE! I want %(po)s to KNOW! AHHH!"),

            _("OH GOD! Send %(po)s the VIDEO! Let %(po)s watch %(poss)s partner get FUCKED!"),

            _("YES! Record EVERYTHING! I want PROOF for %(po)s! AHHHH!"),

        ],

        # --- Girl cum ---
        "girl_cum.cheater.camera_lover": [
            _("I'm CUMMING! Tell me you got that on camera! %(Pp)s NEEDS to see this! AHHHH!"),

            _("CUMMING! Oh god... I want to watch %(poss)s face when %(pp)s finds this footage...!"),

            _("AAAH! I'm cumming so hard on your dick!"),

        ],
        "girl_post_cum.cheater.camera_lover": [
            _("That was insane... please tell me the camera was rolling. I need %(po)s to see what %(pp)s lost."),

            _("If %(pp)s found that video... god, %(poss)s face would be priceless. Save every second."),

            _("Oh god... that was incredible... your cock..."),

        ],

        # --- Cum locations ---
        "cum_inside.cheater.camera_lover": [
            _("You came inside me... I want that on camera. Let %(po)s see another man filling %(poss)s partner."),

            _("%(Poss)s partner just got creampied by another man... and I want %(po)s to find the evidence."),

            _("Imagine %(poss)s face watching another man's cum drip out of me... send %(po)s the clip."),

        ],
        "cum_outside.cheater.camera_lover": [
            _("Look at me covered in your cum... take a picture. I want %(po)s to stumble on it."),

            _("Another man's cum all over %(poss)s partner... this photo would destroy %(po)s. Save it."),

            _("Film it dripping... your cum looks so good on me..."),

        ],
        "cum_face.cheater.camera_lover": [
            _("Another man's cum on my face... take a picture. I want %(po)s to find it in my gallery."),

            _("Imagine %(po)s scrolling through my photos and finding %(poss)s partner's face covered in cum..."),

            _("Get a close-up of my face covered in your cum!"),

        ],
        "cum_mouth.cheater.camera_lover": [
            _("I just swallowed another man's cum... I wish %(pp)s could see the video. %(Poss)s precious partner..."),

            _("Film me licking my lips... I want %(po)s to see exactly what %(poss)s partner does behind %(poss)s back."),

            _("Your cum on my tongue, on camera, behind %(poss)s back... this footage is priceless~"),

        ],
        "cum_tits.cheater.camera_lover": [
            _("All over my tits... take a photo. I want %(po)s to find it and know exactly what happened."),

            _("%(Poss)s partner's chest covered in another man's cum... that's award-winning footage right there."),

            _("Film my tits covered in your cum! This looks amazing!"),

        ],

        # --- Creampie request ---
        "creampie_req.cheater.camera_lover": [
            _("Cum inside me... and record it. I want %(po)s to see another man claim %(poss)s partner."),

            _("Fill me up on camera... the look on %(poss)s face when %(pp)s finds this video..."),

            _("Don't pull out... I need your cum in me..."),

        ],

        # --- Dressup ---
        "dressup.cheater.camera_lover": [
            _("Save that video. All of it. I want %(po)s to find it when %(pp)s least expects it."),

            _("Don't delete anything. I want evidence. Maybe I'll accidentally leave my phone unlocked..."),

            _("I can see you getting hard already... patience..."),

        ],

        # --- Condom events ---
        "condom_ask.cheater.camera_lover": [
            _("Take it off... and film it. I want %(po)s to see %(poss)s partner going raw with another man."),

            _("No condom... and make sure the camera catches every detail. %(Pp)s should see this."),

            _("Please tell me you have one... your cock is huge..."),

        ],

        # ══════════════════════════════════════════════════════════
        #  TRAIT COMBO — Camera Hater + other traits
        # ══════════════════════════════════════════════════════════

        # --- Camera Hater + Cum Slut ---
        "moan.speed1.camera_hater.cum_slut": [
            _("Mmm... I want everything you have... just promise me no cameras..."),

            _("God, I need it... but if there's a recording device anywhere..."),

            _("Mmm... I'm already thinking about your cum..."),

        ],
        "moan.speed2.camera_hater.cum_slut": [
            _("Ahh... give me more... but if you're filming this... oh god..."),

            _("I want it so badly... but the thought of being recorded..."),

            _("Thank god this isn't on camera... the sounds I'm making..."),

        ],
        "moan.speed3.camera_hater.cum_slut": [
            _("FUCK! GIVE ME EVERYTHING! But NO cameras! AHHH!"),

            _("OH GOD! I need ALL of it! But if this is being recorded...!"),

            _("FUCK! Your thick cock is destroying me!"),

        ],
        "cum_inside.camera_hater.cum_slut": [
            _("Yes... every drop inside me... but god, if this is on camera..."),

            _("Fill me up... I love it... but if anyone ever sees video evidence..."),

            _("I feel it leaking... there was so much..."),

        ],
        "cum_face.camera_hater.cum_slut": [
            _("All over my face... I love it... but if you took a photo I'll kill you."),

            _("Cover me... but no pictures. I swear. No evidence of this."),

            _("If that facial was on camera I'd never recover..."),

        ],

        # --- Camera Hater + Virgin ---
        "moan.speed1.camera_hater.virgin": [
            _("Ahh... my first time... please tell me no one is recording this..."),

            _("Mm... I'm so nervous... first time AND my camera paranoia..."),

            _("Just us... no evidence... mmm..."),

        ],
        "dressup.camera_hater.virgin_lost": [
            _("My first time... and I need to make sure there's zero evidence..."),

            _("I just lost my virginity... please delete everything. Texts, photos, all of it."),

            _("Like what you see? Your cock is already responding..."),

        ],

        # ══════════════════════════════════════════════════════════
        #  TRAIT COMBO — Virgin + other traits (expanded)
        # ══════════════════════════════════════════════════════════

        # --- Virgin + Camera Lover ---
        "moan.speed1.virgin.camera_lover": [
            _("Ahh... my first time... I wish this was on camera..."),

            _("Mm... I'm losing my virginity... someone should be filming this..."),

            _("It's so big... I didn't expect it to stretch me like this..."),

        ],
        "cum_inside.virgin.camera_lover": [
            _("You just... inside me... on my first time. I wish I'd recorded that."),

            _("My first time and you came inside me... that would've been incredible footage."),

            _("You came so deep... I can feel it all..."),

        ],
        "dressup.virgin_lost.camera_lover": [
            _("I just lost my virginity... and I didn't even film it. My one regret."),

            _("That was my first time... next time we're recording everything."),

            _("Film me undressing... this deserves a camera..."),

        ],

        # --- Virgin + Cheater ---
        "moan.speed1.virgin.cheater": [
            _("Mmm... my %(pl)s was supposed to be my first... and here I am..."),

            _("My first time... and it's not with %(po)s... ahh..."),

            _("Your thick cock feels so good..."),

        ],
        "cum_inside.virgin.cheater": [
            _("You took my virginity AND came inside me. My %(pl)s will never know."),

            _("My first time was supposed to be %(poss)s... and you just filled me up..."),

            _("I can feel your cum filling my pussy... oh god..."),

        ],
        "dressup.virgin_lost.cheater": [
            _("I just gave my virginity to someone who isn't my %(pl)s. %(Pp)s can never know."),

            _("Getting dressed after losing my virginity... to the wrong person. Or the right one."),

            _("Like what you see? Your cock is already responding..."),

        ],

        # ══════════════════════════════════════════════════════════
        #  TRAIT COMBO — Public combos
        # ══════════════════════════════════════════════════════════

        # --- Public Fetish + Cute ---
        "moan.speed1.public_fetish.cute": [
            _("Mmm... someone might see us... that's making me even more excited..."),

            _("W-we're in public... ahh... I'm so embarrassed but so turned on..."),

            _("Mmm... I love how big you are..."),

        ],
        "moan.speed2.public_fetish.cute": [
            _("Oh god... people could hear me... ahh... I'm so excited..."),

            _("Someone might walk in... my heart is pounding... ahh..."),

            _("Don't stop... your cock hits every spot..."),

        ],
        "girl_cum.public_fetish.cute": [
            _("I'm cumming... in PUBLIC... oh god, what if someone heard me...!"),

            _("CUMMING! I... oh no... did anyone see me just now...?"),

            _("I can't... I'm... CUMMING! Your cock!"),

        ],
        "dressup.public_fetish.cute": [
            _("Quick, help me get dressed... oh god, did anyone see us?! That was amazing though..."),

            _("We just did that in PUBLIC... I'm mortified... and I want to do it again."),

            _("Like what you see? Your cock is already responding..."),

        ],

        # --- Public Shy + Hardcore ---
        "moan.speed1.public_shy.hardcore": [
            _("Harder... but quietly... someone might hear us..."),

            _("I want it rough but... we're in public... keep my mouth covered..."),

            _("Please be quiet... your big cock is hard to be subtle about..."),

        ],
        "girl_cum.public_shy.hardcore": [
            _("CUMMING! *covers mouth* Oh god... someone definitely heard that!"),

            _("I'm... *muffled scream*... oh no... did anyone...?!"),

            _("Your cock just WRECKED me! I came so fucking hard!"),

        ],

        # --- Public Fetish + Camera Lover ---
        "moan.speed2.public_fetish.camera_lover": [
            _("Film us... in public... where anyone could see... ahh..."),

            _("Someone might walk in AND we're being filmed... oh god YES..."),

            _("Every thrust goes deeper... don't stop..."),

        ],
        "cum_inside.public_fetish.camera_lover": [
            _("You came inside me... in public... on camera. Triple perfection."),

            _("Public creampie on film... this is the greatest content ever created."),

            _("So warm inside me... every drop... fuck..."),

        ],

        # --- Public + Cheater ---
        "moan.speed2.public.cheater": [
            _("Ahh... cheating in public... anyone could see... even someone who knows %(po)s..."),

            _("My %(pl)s could walk by... oh god... that makes it hotter..."),

            _("Mmm... fuck... you're so thick..."),

        ],
        "cum_inside.public.cheater": [
            _("Another man's cum inside me... in public. My %(pl)s could've walked by..."),

            _("Creampied in public by someone who isn't my %(pl)s. What have I become?"),

            _("Your cum inside me... I was already cheating... now there's EVIDENCE..."),

        ],

        # --- Moans ---
        "moan.speed1.public_fetish": [
            _("Mmm... I can hear people nearby... that makes it so much better..."),

            _("Someone could walk in any second... ahh... keep going..."),

            _("The risk... the exposure... mmm... this is everything..."),

        ],
        "moan.speed2.public_fetish": [
            _("Oh god... I can't be quiet... and I don't want to be... ahh!"),

            _("Faster... I don't care who hears us... let them listen!"),

            _("Someone's going to find us... oh god... GOOD!"),

        ],
        "moan.speed3.public_fetish": [
            _("YES! I don't care who hears! LET THEM WATCH!"),

            _("ANYONE COULD SEE US! THAT MAKES IT SO MUCH BETTER!"),

            _("OH GOD! The whole world could hear me and I DON'T CARE!"),

        ],

        # ── camera_hater standalone moans ──
        "moan.speed1.camera_hater": [
            _("Mmm... you're not recording this, right? ...don't stop..."),

            _("Promise me no cameras... ahh... just us..."),

            _("This stays between us... mmm... completely private..."),

        ],
        "moan.speed2.camera_hater": [
            _("Ahh! If anyone filmed this I'd... oh god, keep going!"),

            _("No phones! No evidence! Just... ahh... don't stop!"),

            _("This can't get out... oh god... harder!"),

        ],
        "moan.speed3.camera_hater": [
            _("OH GOD! I don't even care about cameras right now! JUST DON'T STOP!"),

            _("AAAH! If anyone recorded this I'd die but... OH FUCK!"),

            _("I SAID NO CAMERAS BUT... I CAN'T THINK ANYMORE!"),

        ],

        # ── camera_lover standalone moans ──
        "moan.speed1.camera_lover": [
            _("Mmm... are you filming this? You should be..."),

            _("I hope the camera's catching my good side... ahh..."),

            _("This would make such good footage... don't stop..."),

        ],
        "moan.speed2.camera_lover": [
            _("Film me! Get every angle! Ahh... yes!"),

            _("The camera loves me... and so do you... oh god!"),

            _("I want every second of this on video! Harder!"),

        ],
        "moan.speed3.camera_lover": [
            _("FILM EVERYTHING! I WANT TO WATCH THIS LATER!"),

            _("OH GOD! TELL ME YOU'RE RECORDING THIS!"),

            _("BEST FOOTAGE EVER! DON'T YOU DARE STOP!"),

        ],

        # ── hate_cum standalone moans ──
        "moan.speed1.hate_cum": [
            _("Mmm... feels good... just be careful when you finish..."),

            _("Keep going... but remember what I said about pulling out..."),

            _("Ahh... this is nice... just don't make a mess..."),

        ],
        "moan.speed2.hate_cum": [
            _("Oh god... faster... but don't you dare finish inside!"),

            _("Ahh! This is so good but... remember your promise!"),

            _("Harder! But I swear if you make a mess...!"),

        ],
        "moan.speed3.hate_cum": [
            _("OH FUCK! I don't care about the mess anymore! JUST... AAAH!"),

            _("DON'T STOP! I... I'll deal with the cleanup later! OH GOD!"),

            _("I hate that we're unprotected but it feels so good!"),

            _("I'm so scared you'll cum inside but it feels so good like this."),

            _("You better pull out! Raw feels amazing but you can't cum inside!"),

        ],

        # ── loyal standalone moans ──
        "moan.speed1.loyal": [
            _("Mmm... this is crazy... I have a boyfriend and I want this so badly..."),

            _("My boyfriend would hate this... ahh... but the desire is driving me insane..."),

            _("I'm supposed to be loyal... mmm... why does my body want you this much..."),

        ],
        "moan.speed2.loyal": [
            _("Oh god! I've lost my mind! This feels too good to stop! Ahh!"),

            _("I'm going crazy... the desire is insane... ahh, don't stop!"),

            _("He trusts me completely and I'm... ahh! ...I can't control myself!"),

        ],
        "moan.speed3.loyal": [
            _("I'VE GONE INSANE! THE LUST IS TOO STRONG! FUCK ME!"),

            _("MY BODY WON'T LISTEN ANYMORE! I NEED THIS TOO BADLY!"),

            _("I'VE COMPLETELY LOST MY MIND AND I WANT MORE! MORE!"),

        ],

        # --- Girl cum ---
        "girl_cum.public_fetish": [
            _("CUMMING! OH GOD! I hope someone heard that!"),

            _("I'M CUMMING IN PUBLIC! THIS IS THE BEST FEELING EVER!"),

            _("AAAH! Everyone can hear me! I DON'T CARE! CUMMING!"),

        ],

        # --- Girl post cum ---
        "girl_post_cum.public_fetish": [
            _("Oh my god... I just came in public... that was incredible."),

            _("Did anyone hear me? ...I kind of hope they did."),

            _("That was the best orgasm of my life... the risk made it ten times better."),

        ],

        # --- Cum locations ---
        "cum_outside.public_fetish": [
            _("All over me... in public... anyone could see the mess on me."),

            _("I'm covered... and people are right there. This is so hot."),

            _("Your cum dripping off me where anyone could walk by... I love the risk..."),

        ],
        "cum_face.public_fetish": [
            _("On my face? In public?! ...I love it. Let them see."),

            _("If anyone walks by and sees cum on my face... worth it."),

            _("Your cum on my face and people just meters away... what a thrill..."),

        ],
        "cum_mouth.public_fetish": [
            _("Mmm... swallowing in public... nobody has any idea..."),

            _("I just swallowed your cum with people around... perfect."),

            _("Your thick load down my throat where anyone could catch us... incredible..."),

        ],
        "cum_tits.public_fetish": [
            _("All over my chest... if I don't clean up, everyone will know..."),

            _("My tits are covered... in public. What a rush."),

            _("Your cum glazing my tits where someone could see any second... so hot..."),

        ],

        # --- Dressup ---
        "dressup.public_fetish": [
            _("Getting dressed... I almost want to leave the evidence showing."),

            _("We just did that in public and got away with it... when can we do it again?"),

            _("Back to normal... but I can still feel it. Anyone looking at me would never guess."),

        ],

        # --- Moans ---
        "moan.speed1.public_shy": [
            _("Mmph... *covers mouth* ...I can't let anyone hear me..."),

            _("Shh... shh... oh god... I have to be quiet... mmm..."),

            _("Someone's going to hear... please... slower... mmph..."),

        ],
        "moan.speed2.public_shy": [
            _("*muffled moan* ...I can't... keep... quiet... oh no..."),

            _("Mmph! S-someone's going to... ahh... find us... oh god..."),

            _("I'm trying not to moan but... ahh... it's too good..."),

        ],
        "moan.speed3.public_shy": [
            _("MMPH! *hand over mouth* OH GOD SOMEONE DEFINITELY HEARD THAT!"),

            _("I CAN'T... *bites lip* ...BE QUIET ANYMORE! WE'RE GOING TO GET CAUGHT!"),

            _("AAAH! I'm sorry! I can't... stop... moaning... oh god..."),

        ],

        # --- Girl cum ---
        "girl_cum.public_shy": [
            _("I'M... *covers mouth* ...MMMMPH! Oh god... did anyone hear...?!"),

            _("CUMMING! *bites pillow/hand* ...oh no oh no did someone hear me?!"),

            _("*muffled scream* I couldn't... hold it... please tell me no one heard..."),

        ],

        # --- Girl post cum ---
        "girl_post_cum.public_shy": [
            _("Oh god... I was SO loud... do you think anyone heard...?"),

            _("My heart is pounding... not just from the orgasm... I'm so scared someone noticed."),

            _("That was amazing but... I need a minute... I'm shaking from the adrenaline..."),

        ],

        # --- Cum locations ---
        "cum_outside.public_shy": [
            _("Oh no... it's on me... what if someone sees the stain?!"),

            _("Quick, I need to clean up before anyone notices!"),

            _("Your cum is everywhere... in PUBLIC... someone's going to see!"),

        ],
        "cum_face.public_shy": [
            _("MY FACE?! HERE?! I can't walk out like this! Give me something to wipe!"),

            _("Oh god... if anyone sees cum on my face... I'll never recover..."),

            _("Wipe it off! Quick! I can feel your cum dripping and people are RIGHT THERE!"),

        ],
        "cum_mouth.public_shy": [
            _("At least... no one can tell... *swallows quickly* ...oh god..."),

            _("Better in my mouth than visible... at least no one will notice..."),

            _("I swallowed it before anyone could see... oh god the taste... but at least no evidence..."),

        ],
        "cum_tits.public_shy": [
            _("My chest! Quick, I need to cover up before someone sees!"),

            _("If anyone notices the stain on my shirt... I'll die..."),

            _("Your cum soaking through my top... in PUBLIC... someone will definitely notice!"),

        ],

        # --- Dressup ---
        "dressup.public_shy": [
            _("Quick quick quick! Help me get dressed before someone comes!"),

            _("Oh god... is anyone looking? Do I look normal? Can they tell?!"),

            _("I need to get out of here... I'm so embarrassed... do I look okay?"),

        ],

        # ══════════════════════════════════════════════════════════
        #  TRAIT COMBO — Hate Cum combos
        # ══════════════════════════════════════════════════════════

        # --- Hate Cum + Hardcore ---
        "cum_inside.hate_cum.hardcore": [
            _("You did NOT just... INSIDE?! I told you to KEEP IT OUT! FUCK!"),

            _("Are you fucking KIDDING ME?! I said NO CUM! Get away from me!"),

            _("My pussy is full of your cum... I can't believe I let you..."),

        ],
        "cum_face.hate_cum.hardcore": [
            _("You got it on my FACE?! I'm going to KILL you!"),

            _("My FACE?! Are you fucking SERIOUS?! That's DISGUSTING!"),

            _("Ugh... it's in my eyes... I hate this..."),

        ],
        "cum_outside.hate_cum.hardcore": [
            _("At least you didn't get it IN me. But you better clean this up. NOW."),

            _("Disgusting. But better than inside. Don't let it happen again."),

            _("At least it's not inside me... but still... gross..."),

        ],

        # --- Hate Cum + Cheater ---
        "cum_inside.hate_cum.cheater": [
            _("I cheat because I want good sex. Not because I want your cum inside me! UGH!"),

            _("I don't mind fucking behind %(poss)s back. But you cumming inside me? That crosses a line."),

            _("GET OFF ME! Your cum is INSIDE me! I HATE this! I HATE you!"),

        ],
        "dressup.hate_cum.cheater": [
            _("I need to clean up YOUR mess before going back to my %(pl)s."),

            _("Cheating is fine. The cum part? Always ruins it for me."),

            _("Eyes up here... or maybe not~"),

        ],

        # --- Hate Cum + Virgin ---
        "moan.speed1.hate_cum.virgin": [
            _("It's my first time... please be careful... and don't... finish inside me..."),

            _("I've never done this... and the thought of... that part... please don't..."),

            _("It's so big... I didn't expect it to stretch me like this..."),

        ],
        "cum_inside.hate_cum.virgin": [
            _("My first time and you... INSIDE?! That's the ONE thing I asked you not to do!"),

            _("I was a VIRGIN and you just... ugh! I'm going to be sick!"),

            _("You FORCED your cum inside me?! I feel SICK!"),

        ],

        # ══════════════════════════════════════════════════════════
        #  TRAIT COMBO — Loyal combos
        # ══════════════════════════════════════════════════════════

        # --- Loyal + Cum Slut (conflicted) ---
        "moan.speed1.loyal.cum_slut": [
            _("Mmm... I have a boyfriend and I'm craving this like crazy... what's wrong with me..."),

            _("My body is desperate for you... this desire is insane..."),

            _("Promise you'll cum inside my little pussy..."),

        ],
        "moan.speed2.loyal.cum_slut": [
            _("Ahh... I've lost my mind... the craving is too strong to resist... oh god..."),

            _("The desire is driving me insane... I need more of you... ahh..."),

            _("Your cock is driving me crazy..."),

        ],
        "cum_inside.loyal.cum_slut": [
            _("Inside me... I'm going crazy... I wanted that more than anything..."),

            _("I've completely lost it... my body craved every drop of that..."),

            _("So warm inside me... every drop... fuck..."),

        ],

        # --- Loyal + Hardcore (aggressive refusal) ---
        "moan.speed1.loyal.hardcore": [
            _("Don't... I have a boyfriend... and if you don't stop I'll MAKE you stop."),

            _("Back off. I'm taken. And I don't play nice with people who push."),

            _("Harder... don't hold back..."),

        ],

        # ══════════════════════════════════════════════════════════
        #  TRAIT COMBO — Boyfriend + context combos (remaining)
        # ══════════════════════════════════════════════════════════

        # --- Boyfriend + Cheater ---
        "moan.speed1.boyfriend.cheater": [
            _("Mmm... my boyfriend is at home thinking about me... while I'm here with you..."),

            _("He texted me 'I love you' an hour ago... and here I am moaning for another man..."),

            _("This is so much better than anything he gives me..."),

        ],
        "moan.speed1.girlfriend.cheater": [
            _("Mmm... my girlfriend is at home thinking about me... while I'm here with a man..."),

            _("She texted me 'I love you' an hour ago... and here I am moaning for a guy..."),

            _("A real cock is so much better than anything she gives me..."),

            _("She's probably calling me right now... mmm... while I'm here with a man..."),

            _("I stopped feeling guilty a while ago... this is just who I am now..."),

        ],
        "moan.speed2.boyfriend.cheater": [
            _("Ahh... he has no idea... and honestly? I don't care. This is SO much better..."),

            _("My boyfriend thinks I'm faithful... god if he could see me now... ahh..."),

            _("If he saw what your big dick does to me..."),

        ],
        "moan.speed2.girlfriend.cheater": [
            _("Ahh... she has no idea I'm with a man... and honestly? I don't care. This is SO much better..."),

            _("My girlfriend thinks I only like women... god if she could see me now... ahh..."),

            _("If she saw what your big dick does to me... her 'lesbian' girlfriend..."),

            _("I've done this before and I'll do it again... ahh... she's a fool to trust me..."),

            _("Every time I come back to you, it's easier... ahh... the guilt fades..."),

        ],
        "moan.speed3.boyfriend.cheater": [
            _("FUCK! My boyfriend could NEVER! I don't even FEEL guilty anymore! AHHH!"),

            _("YES! He's NOTHING compared to this! I should've cheated SOONER!"),

            _("HARDER! Your dick drives me INSANE!"),

        ],
        "moan.speed3.girlfriend.cheater": [
            _("FUCK! My girlfriend could NEVER give me this! I don't even FEEL guilty anymore! AHHH!"),

            _("YES! Nothing compares to cock! I should've tried this SOONER!"),

            _("HARDER! Your dick drives me INSANE! She could NEVER!"),

            _("I'M CHEATING ON HER WITH A MAN AND IT'S THE BEST I'VE EVER FELT! AAAH!"),

            _("SHE THINKS SHE'S ENOUGH! NOTHING SHE HAS COMPARES TO A REAL COCK!"),

            _("I SHOULD FEEL GUILTY BUT YOUR COCK IS MAKING ME FORGET HER NAME! FUCK!"),

        ],
        "girl_cum.boyfriend.cheater": [
            _("CUMMING! My boyfriend... ha... he could NEVER make me cum like THIS!"),

            _("I'm cumming SO hard for another man! Sorry not sorry, boyfriend!"),

            _("I can't... I'm... CUMMING! Your cock!"),

        ],
        "girl_cum.girlfriend.cheater": [
            _("CUMMING! My girlfriend... ha... she could NEVER make me cum like a cock does!"),

            _("I'm cumming SO hard for YOU! Sorry not sorry, girlfriend!"),

            _("I can't... I'm... CUMMING! A man's cock is everything she's not!"),

        ],
        "cum_inside.boyfriend.cheater": [
            _("Another man's cum inside me... and my boyfriend has no idea. I love it."),

            _("My boyfriend thinks I'm exclusive... while you're filling me up. Perfect."),

            _("You came inside me?! My BOYFRIEND never does that! What have you done?!"),

        ],
        "cum_inside.girlfriend.cheater": [
            _("A man's cum inside me... and my girlfriend has no idea I love cock. I love it."),

            _("My girlfriend thinks I only like women... while a man is filling me up. Perfect."),

            _("You came inside me?! My GIRLFRIEND doesn't know about this! What have you done?!"),

        ],
        "dressup.boyfriend.cheater": [
            _("Time to go home and kiss my boyfriend. With the taste of another man still on me."),

            _("Getting dressed to go pretend I'm a good girlfriend. What a joke."),

            _("Like what you see? Your cock is already responding..."),

        ],
        "dressup.girlfriend.cheater": [
            _("Time to go home and kiss my girlfriend. With the taste of your cock still on me."),

            _("Getting dressed to go pretend I'm her faithful lesbian girlfriend. What a joke."),

            _("Like what you see? Your cock is already responding... she could never do that to me..."),

        ],

        # --- Boyfriend + Loyal ---
        "moan.speed1.boyfriend.loyal": [
            _("Mm... I have a boyfriend... this is crazy... why do I want this so badly..."),

            _("My body is acting on its own... I can't believe how much I need this..."),

            _("He could never fill me up like you do..."),

        ],
        "moan.speed1.girlfriend.loyal": [
            _("Mm... I have a girlfriend... I shouldn't want this... why do I want you so badly..."),

            _("My body is acting on its own... I can't believe how much I need cock..."),

            _("She could never fill me up like this... not like a real one..."),

            _("I love her, I really do... but this urge for a man won't go away..."),

            _("She trusts me completely... mmm... and here I am breaking that trust..."),

        ],
        "moan.speed2.boyfriend.loyal": [
            _("Ahh... I love him... but this desire is driving me insane... oh god..."),

            _("My boyfriend trusts me... and I'm losing my mind over you... ahh..."),

            _("His cock doesn't compare... I hate admitting it..."),

        ],
        "moan.speed2.girlfriend.loyal": [
            _("Ahh... I love her... but this craving for a man is driving me insane... oh god..."),

            _("My girlfriend trusts me... and I'm losing my mind over your cock... ahh..."),

            _("Nothing she does compares to this... I hate admitting it..."),

            _("Ahh... the love I feel for her can't compete with this lust... I'm losing..."),

            _("She deserves better than this... ahh... but I need a man too badly..."),

        ],
        "moan.speed3.boyfriend.loyal": [
            _("I'VE GONE CRAZY! THE LUST IS TOO STRONG! I CAN'T FIGHT IT! AHHH!"),

            _("FUCK! MY BODY WON'T LISTEN! THE DESIRE IS INSANE! MORE!"),

            _("He's NOTHING compared to you! Your cock is TOO GOOD!"),

        ],
        "moan.speed3.girlfriend.loyal": [
            _("I'VE GONE CRAZY! THE LUST FOR COCK IS TOO STRONG! I CAN'T FIGHT IT! AHHH!"),

            _("FUCK! MY BODY WANTS A MAN! THE DESIRE IS INSANE! MORE!"),

            _("She's NOTHING compared to this! Your cock is TOO GOOD! I don't care anymore!"),

            _("I LOVE HER BUT MY BODY NEEDS A MAN! THIS DESIRE IS DESTROYING ME! AAAH!"),

            _("THE LOYALTY MEANS NOTHING WHEN COCK FEELS LIKE THIS! I'M SORRY! FUCK!"),

            _("EVERY PART OF ME SAYS STOP BUT THE PLEASURE WON'T LET ME! AAAH!"),

        ],
        "girl_cum.boyfriend.loyal": [
            _("I'M CUMMING! I'VE LOST MY MIND! THE DESIRE WAS TOO MUCH! AAAH!"),

            _("CUMMING! THIS IS INSANE! I couldn't resist... it was too strong..."),

            _("OH GOD! I'm cumming! Don't stop!"),

        ],
        "girl_cum.girlfriend.loyal": [
            _("I'M CUMMING! I'VE LOST MY MIND! A man is making me... THE DESIRE WAS TOO MUCH! AAAH!"),

            _("CUMMING! THIS IS INSANE! I'm supposed to be hers but a cock... I couldn't resist..."),

            _("OH GOD! I'm cumming on a man! She'd never forgive me! Don't stop!"),

        ],
        "cum_inside.boyfriend.loyal": [
            _("Inside me... this is the craziest thing I've ever done... and I craved it..."),

            _("I can't believe my desire drove me this far... I wanted every drop..."),

            _("You came inside me?! My BOYFRIEND never does that! What have you done?!"),

        ],
        "cum_inside.girlfriend.loyal": [
            _("A man came inside me... this is the craziest thing I've ever done... and I craved it..."),

            _("I can't believe my desire for cock drove me this far... I wanted every drop..."),

            _("You came inside me?! I have a GIRLFRIEND! I'm not even attracted to men! What have you done?!"),

        ],
        "dressup.boyfriend.loyal": [
            _("That was... insane. My body completely took control. I still can't think straight..."),

            _("I need to calm down... the desire just overwhelmed everything I believed in..."),

            _("These are the panties he bought me... and I'm taking them off for you..."),

        ],
        "dressup.girlfriend.loyal": [
            _("That was... insane. My body wanted a man and it completely took control..."),

            _("I need to calm down... the desire for cock just overwhelmed everything I believed about myself..."),

            _("These are the panties she bought me... and I just took them off for a man..."),

        ],

        # ══════════════════════════════════════════════════════════
        #  BISEXUAL + GIRLFRIEND — she knows she likes both; the
        #  tension is cheating, not orientation discovery.
        # ══════════════════════════════════════════════════════════

        # --- Bisexual GF: Moans ---
        "moan.speed1.bisexual_gf": [
            _("Mmm... she knows I like guys too, but she'd lose it if she saw me with you..."),

            _("My girlfriend can't give me this... and deep down, we both know it..."),

            _("I told her I'd be faithful... mmm... I'm already breaking that promise..."),

            _("This is the part of me she can never satisfy... no matter how hard she tries..."),

            _("She's amazing, but sometimes a girl just needs... mmm... this..."),

        ],
        "moan.speed2.bisexual_gf": [
            _("Ahh... she knows I'm bi... but she doesn't know I'm here... with you..."),

            _("I love her, but this... this is what she can't do for me... ahh..."),

            _("She always asks if I miss it... ahh... if she only knew how much..."),

            _("Being bi means I know exactly what I'm missing... and this is it... ahh..."),

            _("I'm not confused about what I want... ahh... I want both... I want this..."),

            _("God... she'd understand if she felt this... no, she'd kill me... ahh..."),

        ],
        "moan.speed3.bisexual_gf": [
            _("SHE KNOWS I LIKE DICK BUT SHE'D NEVER FORGIVE THIS! FUCK!"),

            _("I'M BI! I'VE ALWAYS NEEDED THIS! SHE JUST CAN'T GIVE IT TO ME! AAAH!"),

            _("MY GIRLFRIEND CAN'T COMPETE WITH A REAL COCK! NOT WITH THIS! FUCK!"),

            _("I LOVE HER BUT I NEED... I NEED THIS! AAAH!"),

            _("THIS IS WHY I CAN'T BE JUST HERS! FUCK! I NEED A MAN TOO!"),

            _("SHE ALWAYS SAID SHE WAS ENOUGH! SHE'S NOT! NOT FOR THIS! AAAH!"),

            _("I'M NOT IN DENIAL! I LOVE COCK AND I LOVE HER! I JUST CAN'T... AAAH!"),

            _("BEING BI MEANS I KNOW EXACTLY WHAT I'M LOSING IF I STOP! DON'T STOP!"),

        ],

        # --- Bisexual GF: Girl Cum ---
        "girl_cum.bisexual_gf": [
            _("CUMMING! God... she never makes me cum like THIS..."),

            _("I'M... I'M CUMMING! This is what she can't give me! AAAH!"),

            _("OH GOD! I'm cumming from a cock... my girlfriend... she'd... AAAH!"),

        ],
        "girl_cum_hard.bisexual_gf": [
            _("I'M CUMMING SO HARD! SHE COULD NEVER MAKE ME CUM LIKE A MAN DOES! AAAH!"),

            _("AAAH! THIS IS... A COCK MAKES ME... MY GIRLFRIEND COULD NEVER! FUCK!"),

            _("I CAN'T... I'M CUMMING SO HARD I CAN'T THINK! SHE DOESN'T KNOW WHAT SHE'S MISSING!"),

        ],

        # --- Bisexual GF: Cum Inside ---
        "cum_inside.bisexual_gf": [
            _("You came inside me... my girlfriend has no idea I let men do this to me..."),

            _("Cum inside me while I have a girlfriend... I'm terrible... and I loved every second."),

            _("She can't fill me like this... literally... god, what am I doing..."),

        ],

        # --- Bisexual GF: Dressup ---
        "dressup.bisexual_gf": [
            _("Time to go home to my girlfriend. She'll never know what I did today."),

            _("Back to being her faithful bisexual partner. Right."),

            _("She'll ask how my day was and I'll say 'fine.' As usual."),

        ],

        # --- Bisexual GF + Cum Slut ---
        "moan.speed1.bisexual_gf.cum_slut": [
            _("Mmm... my girlfriend thinks she satisfies me... she has no idea how much I crave cock..."),

            _("I'm bi and she knows it... but she doesn't know just how addicted I am to this..."),

            _("She gives me love, you give me what she can't... mmm... I need both..."),

            _("Every time she asks if I miss dick, I lie... mmm... I'm obsessed with it..."),

        ],
        "moan.speed2.bisexual_gf.cum_slut": [
            _("Ahh... I told my girlfriend I don't need cock that much... I was SO lying..."),

            _("She can't compete with this... ahh... not because she's bad, but because I'm addicted..."),

            _("Being bi with a craving like mine... ahh... my poor girlfriend never stood a chance..."),

            _("I love her but I CRAVE this... ahh... she has no idea how much..."),

        ],
        "moan.speed3.bisexual_gf.cum_slut": [
            _("I TOLD HER I DIDN'T NEED COCK! I WAS LYING! I'M ADDICTED! AAAH!"),

            _("SHE CAN GIVE ME LOVE BUT SHE CAN'T GIVE ME THIS! I NEED IT! FUCK!"),

            _("I'M BI AND I'M A SLUT FOR COCK! MY GIRLFRIEND COULD NEVER COMPETE!"),

            _("EVERY INCH! I NEED EVERY INCH! SHE DOESN'T KNOW HOW BAD I NEED IT!"),

            _("I LOVE HER BUT MY BODY CRAVES COCK! HARDER! I'M LOSING MY MIND!"),

        ],
        "girl_cum.bisexual_gf.cum_slut": [
            _("CUMMING! FROM COCK! She gives me love but only THIS makes me cum like this!"),

            _("I'M CUMMING! I'M ADDICTED! My girlfriend can't... she could NEVER... AAAH!"),

            _("OH GOD! CUMMING! I told her I didn't need dick this badly! I LIED!"),

        ],
        "cum_inside.bisexual_gf.cum_slut": [
            _("God... your cum inside me... my girlfriend doesn't know I'm this addicted..."),

            _("Fill me up... she could never do this... and I crave it every single time..."),

            _("More... I want more... she'd never understand how much I need this from a man..."),

        ],

        # --- Bisexual GF + Cheater ---
        "moan.speed1.bisexual_gf.cheater": [
            _("Mmm... she trusts me, and here I am... well, a girl has needs she can't fill..."),

            _("Cheating on my girlfriend with a man... mmm... at least I know what I want..."),

            _("She'd call this cheating... I call it getting what I need..."),

        ],
        "moan.speed2.bisexual_gf.cheater": [
            _("Ahh... I've cheated before and I'll do it again... she can't give me this..."),

            _("My girlfriend has no clue... ahh... and honestly, what she doesn't know..."),

            _("I know exactly what I'm doing... ahh... and I'm not going to stop..."),

        ],
        "moan.speed3.bisexual_gf.cheater": [
            _("FUCK LOYALTY! I NEED COCK AND SHE CAN'T GIVE IT TO ME! AAAH!"),

            _("I'LL GO HOME AND KISS HER AFTER THIS! AND I WON'T FEEL BAD! HARDER!"),

            _("SHE THINKS I'M FAITHFUL! I'M GETTING WHAT I NEED! FUCK!"),

            _("CHEATING ON HER WITH A MAN MAKES IT HOTTER! I DON'T CARE! AAAH!"),

        ],
        "girl_cum.bisexual_gf.cheater": [
            _("CUMMING! Cheating on her with a man and I don't even feel guilty! AAAH!"),

            _("I'M CUMMING! She thinks I'm loyal! HA! Your cock says otherwise!"),

            _("OH GOD! CUMMING! I'll kiss her tonight and she'll never know! AAAH!"),

        ],
        "cum_inside.bisexual_gf.cheater": [
            _("Another man's cum inside me while my girlfriend waits at home. And I love it."),

            _("She thinks I'm faithful... while you're filling me up. What she doesn't know..."),

            _("I have a girlfriend and I just let a man cum inside me. And I'd do it again."),

        ],
        "dressup.bisexual_gf.cheater": [
            _("Time to go home and be the good girlfriend. She has no idea."),

            _("Getting dressed to go lie to her face. I've gotten good at it."),

            _("She'll smell his cologne on me and I'll blame the bus. Easy."),

        ],

        # --- Bisexual GF + Loyal ---
        "moan.speed1.bisexual_gf.loyal": [
            _("Mmm... I love her so much, but this need... it won't go away... I've tried..."),

            _("She's everything to me, but this part of me... mmm... she can never fill it..."),

            _("I hate myself for being here... but my body won't listen... mmm..."),

        ],
        "moan.speed2.bisexual_gf.loyal": [
            _("Ahh... I love her, I really do... but this craving for a man is eating me alive..."),

            _("She's the love of my life... ahh... but she can't give me this one thing..."),

            _("The guilt is killing me... ahh... but I can't stop... I need this too badly..."),

        ],
        "moan.speed3.bisexual_gf.loyal": [
            _("I LOVE HER! I DO! BUT I NEED THIS! MY BODY NEEDS THIS! AAAH!"),

            _("SHE'D FORGIVE ME IF SHE UNDERSTOOD! I CAN'T HELP BEING BI! FUCK!"),

            _("THE GUILT! THE PLEASURE! I CAN'T TELL THEM APART ANYMORE! AAAH!"),

            _("I'M SORRY BABY! I LOVE YOU BUT I NEED... AAAH!"),

        ],
        "girl_cum.bisexual_gf.loyal": [
            _("I'M CUMMING! I love her but... a man is making me... THE NEED WAS TOO MUCH! AAAH!"),

            _("CUMMING! She's the love of my life and I'm cumming on another person's cock..."),

            _("OH GOD! I'm cumming! She deserves better than this! I'm sorry! Don't stop!"),

        ],
        "cum_inside.bisexual_gf.loyal": [
            _("A man came inside me... I love my girlfriend so much and I let this happen..."),

            _("You came inside me... the guilt is crushing but my body craved every drop..."),

            _("She trusts me completely... and I just let you finish inside me... what have I done..."),

        ],
        "dressup.bisexual_gf.loyal": [
            _("That was... I love her so much and I just did this. What's wrong with me..."),

            _("I need to calm down... the craving took over and I couldn't fight it..."),

            _("She trusts me... she actually trusts me... and I keep doing this..."),

        ],

        # --- Boyfriend + Public Fetish ---
        "moan.speed1.boyfriend.public_fetish": [
            _("Mmm... cheating on my boyfriend... in PUBLIC... the double thrill..."),

            _("Anyone could see me with another man... my boyfriend's friends could walk by..."),

            _("If my boyfriend knew how good your dick feels..."),

        ],
        "moan.speed1.girlfriend.public_fetish": [
            _("Mmm... cheating on my girlfriend with a man... in PUBLIC... the double thrill..."),

            _("Anyone could see me with a guy... her friends could walk by and see me loving cock..."),

            _("If my girlfriend knew how good dick feels... she'd understand why I'm here..."),

        ],
        "moan.speed2.boyfriend.public_fetish": [
            _("Ahh... public AND cheating... someone who knows him might see... oh god..."),

            _("My boyfriend could find out from a STRANGER... and that makes it hotter..."),

            _("If he saw what your big dick does to me..."),

        ],
        "moan.speed2.girlfriend.public_fetish": [
            _("Ahh... public AND with a man... someone who knows her might see... oh god..."),

            _("My girlfriend could find out from a STRANGER that I love cock... and that makes it hotter..."),

            _("If she saw what your big dick does to her girlfriend..."),

        ],
        "cum_inside.boyfriend.public_fetish": [
            _("Another man came inside me... in public. My boyfriend is somewhere nearby, clueless."),

            _("Public creampie from a man who isn't my boyfriend. The ultimate taboo."),

            _("I feel it leaking... there was so much..."),

        ],
        "cum_inside.girlfriend.public_fetish": [
            _("A man came inside me... in public. My girlfriend is somewhere nearby, clueless that I love cock."),

            _("Public creampie from a man while I have a girlfriend. The ultimate taboo."),

            _("I feel it leaking... everyone could see me dripping with your cum..."),

        ],
        "dressup.boyfriend.public_fetish": [
            _("Getting dressed in public after cheating. Someone definitely saw us."),

            _("My boyfriend might hear about this through the grapevine... thrilling."),

            _("These are the panties he bought me... and I'm taking them off for you..."),

        ],
        "dressup.girlfriend.public_fetish": [
            _("Getting dressed in public after being with a man. Someone definitely saw us."),

            _("My girlfriend might hear I was with a guy through the grapevine... thrilling."),

            _("These are the panties she bought me... and I just took them off for a man..."),

        ],

        # --- Boyfriend + Public Shy ---
        "moan.speed1.boyfriend.public_shy": [
            _("Mm... I'm cheating... in public... what if someone tells my boyfriend..."),

            _("We're outside... someone could see me with you... and tell him..."),

            _("Your thick cock feels so good..."),

        ],
        "moan.speed1.girlfriend.public_shy": [
            _("Mm... I'm with a man... in public... what if someone tells my girlfriend..."),

            _("We're outside... someone could see me with a guy... and tell her..."),

            _("If anyone sees me enjoying cock... and tells her..."),

        ],
        "moan.speed2.boyfriend.public_shy": [
            _("Ahh... oh no... what if someone recognizes me... and tells my boyfriend..."),

            _("I'm cheating in PUBLIC... if his friends see me... oh god..."),

            _("Fuck... you're hitting so deep..."),

        ],
        "moan.speed2.girlfriend.public_shy": [
            _("Ahh... oh no... what if someone recognizes me with a man... and tells my girlfriend..."),

            _("I'm with a GUY in PUBLIC... if her friends see me... they'll know what I'm doing... oh god..."),

            _("Fuck... you're hitting so deep... and anyone could see..."),

        ],
        "cum_inside.boyfriend.public_shy": [
            _("You came inside me... in public... my boyfriend could've walked by..."),

            _("Oh god... public AND creampie AND cheating... I'm going to throw up from anxiety..."),

            _("Your cum inside someone else's girlfriend?! You're a MONSTER!"),

        ],
        "cum_inside.girlfriend.public_shy": [
            _("A man came inside me... in public... my girlfriend could've walked by..."),

            _("Oh god... public AND a creampie AND cheating on my girlfriend... I'm going to throw up from anxiety..."),

            _("Your cum inside me?! In PUBLIC?! You're a MONSTER!"),

        ],

        # --- Boyfriend + Public (neutral — she's cheating in public, no public trait) ---
        "moan.speed1.boyfriend.public": [
            _("Mm... anyone could see me cheating... my boyfriend could find out..."),

            _("Ahh... in public... with someone who isn't my boyfriend..."),

            _("Shh... I can feel every inch but we have to be quiet..."),

        ],
        "moan.speed1.girlfriend.public": [
            _("Mm... anyone could see me with a man... my girlfriend could find out..."),

            _("Ahh... in public... with a guy while my girlfriend waits at home..."),

            _("Shh... I can feel every inch but no one can know I like this..."),

        ],
        "moan.speed2.boyfriend.public": [
            _("Ahh... we're in public... what if someone who knows him sees us..."),

            _("Oh god... my boyfriend's friends could be anywhere... ahh..."),

            _("His cock doesn't compare... I hate admitting it..."),

        ],
        "moan.speed2.girlfriend.public": [
            _("Ahh... we're in public... what if someone who knows her sees me with a man..."),

            _("Oh god... my girlfriend's friends could be anywhere... seeing me love cock... ahh..."),

            _("Nothing she does compares to this... I hate admitting it..."),

        ],
        "moan.speed3.boyfriend.public": [
            _("AHH! I DON'T CARE! LET THEM SEE! MY BOYFRIEND CAN DEAL WITH IT!"),

            _("FUCK! ANYONE COULD BE WATCHING! I'M CHEATING IN THE OPEN! MORE!"),

            _("My boyfriend's DICK could NEVER do THIS! FUCK!"),

        ],
        "moan.speed3.girlfriend.public": [
            _("AHH! I DON'T CARE! LET THEM SEE! MY GIRLFRIEND CAN DEAL WITH IT!"),

            _("FUCK! ANYONE COULD SEE ME WITH A MAN! I DON'T CARE ANYMORE! MORE!"),

            _("My girlfriend could NEVER give me cock like THIS! FUCK!"),

        ],
        "girl_cum.boyfriend.public": [
            _("CUMMING! In public! My boyfriend could've walked right past us!"),

            _("OH GOD! I just came... out here... cheating on him where anyone could see...!"),

            _("Oh god... I came on your dick... he can never know..."),

        ],
        "girl_cum.girlfriend.public": [
            _("CUMMING! In public! My girlfriend could've walked right past me cumming on a cock!"),

            _("OH GOD! I just came for a man... out here... where anyone could see me with a guy...!"),

            _("Oh god... I came on your dick... she can never know a man did this to me..."),

        ],
        "cum_inside.boyfriend.public": [
            _("You came inside me... in public... if my boyfriend finds out like this..."),

            _("Creampied by another man... in public... my boyfriend is somewhere nearby, clueless..."),

            _("I can feel your cum filling my pussy... oh god..."),

        ],
        "cum_inside.girlfriend.public": [
            _("A man came inside me... in public... if my girlfriend finds out like this..."),

            _("Creampied by a man... in public... my girlfriend is somewhere nearby, clueless that I love cock..."),

            _("I can feel your cum filling my pussy... creampied in public... oh god..."),

        ],
        "cum_outside.boyfriend.public": [
            _("At least it's not inside me... but anyone could see what we just did..."),

            _("The evidence is right there... in public... while my boyfriend trusts me..."),

            _("My boyfriend has never cum this much... your cock..."),

        ],
        "cum_outside.girlfriend.public": [
            _("At least it's not inside me... but anyone could see me with your cum..."),

            _("The evidence is right there... in public... while my girlfriend trusts me..."),

            _("So much cum... she could never give me anything like this..."),

        ],
        "dressup.boyfriend.public": [
            _("I need to clean up and look normal... anyone could tell my boyfriend..."),

            _("Getting dressed fast... if anyone recognized me, he'll find out..."),

            _("I can see you getting hard already... patience..."),

        ],
        "dressup.girlfriend.public": [
            _("I need to clean up and look normal... anyone could tell my girlfriend I was with a man..."),

            _("Getting dressed fast... if anyone recognized me with a guy, she'll find out..."),

            _("I can see you getting hard already... she could never do that... patience..."),

        ],

        # --- Boyfriend + Public: act-specific ---
        "creampie_req.boyfriend.public": [
            _("Cum inside me out here... let my boyfriend's world fall apart..."),

            _("In public... inside me... while I have a boyfriend... this is insane..."),

            _("Fill me up where anyone could see... my boyfriend is somewhere nearby, clueless..."),

        ],
        "creampie_req.girlfriend.public": [
            _("Cum inside me out here... let my girlfriend's world fall apart..."),

            _("In public... a man inside me... while I have a girlfriend... this is insane..."),

            _("Fill me up where anyone could see... my girlfriend is somewhere nearby, clueless that I love cock..."),

        ],
        "record_accepted.boyfriend.public": [
            _("Film me cheating on my boyfriend... in public... I must be out of my mind..."),

            _("Go ahead, record it... public proof I'm a cheater..."),

            _("Record it... I'm curious how it looks from your angle."),

            _("A video of me with another man... in public... my boyfriend can never see this..."),

        ],
        "record_accepted.girlfriend.public": [
            _("Film me with a man... in public... my girlfriend would lose her mind..."),

            _("Go ahead, record it... public proof I love cock..."),

            _("Record it... I want to see how I look taking your dick."),

            _("A video of me with a guy... in public... my girlfriend can never see this..."),

        ],

        # --- Boyfriend + Public Shy: act-specific ---
        "creampie_req.boyfriend.public_shy": [
            _("I-inside?! Here?! If someone sees the mess and tells my boyfriend...!"),

            _("N-not in public... the evidence... someone could tell him everything..."),

            _("Inside... where my boyfriend never goes without protection..."),

        ],
        "creampie_req.girlfriend.public_shy": [
            _("I-inside?! Here?! If someone sees your mess on me and tells my girlfriend...!"),

            _("N-not in public... the evidence of a man... someone could tell her everything..."),

            _("Inside... where no man has ever gone... and we're in public... oh god..."),

        ],

        # --- Boyfriend + Public Fetish: act-specific ---
        "creampie_req.boyfriend.public_fetish": [
            _("Fill me up in public... let it drip out where everyone can see what I did to my boyfriend..."),

            _("Cum inside me out here... someone should tell him what his girlfriend just did..."),

            _("Public creampie from another man... my boyfriend's worst nightmare come true..."),

        ],
        "creampie_req.girlfriend.public_fetish": [
            _("Fill me up in public... let it drip out where everyone can see me take your load..."),

            _("Cum inside me out here... someone should tell her what her girlfriend just did with a man..."),

            _("Public creampie from a man... my girlfriend's worst nightmare come true..."),

        ],
        "record_accepted.boyfriend.public_fetish": [
            _("Film me cheating in public! Send it to my boyfriend! Let him see EVERYTHING!"),

            _("Yes! Record his girlfriend getting fucked by another man in public!"),

            _("Record it... I'm curious how it looks from your angle."),

            _("A video of me cheating... in public... someone should forward it to him..."),

        ],
        "record_accepted.girlfriend.public_fetish": [
            _("Film me with a man in public! Send it to my girlfriend! Let her see EVERYTHING!"),

            _("Yes! Record her girlfriend getting fucked in public!"),

            _("Record it... I want proof of what her girlfriend really wants."),

            _("A video of me loving cock... in public... someone should forward it to her..."),

        ],

        # --- Boyfriend + Public Shy (expanded) ---
        "moan.speed3.boyfriend.public_shy": [
            _("AHH! N-NOT SO LOUD! What if someone HEARS and tells my boyfriend?!"),

            _("OH GOD PLEASE... I can't stop... but what if his FRIENDS are here...!"),

            _("HARDER! Your dick drives me INSANE!"),

        ],
        "moan.speed3.girlfriend.public_shy": [
            _("AHH! N-NOT SO LOUD! What if someone sees us and tells my girlfriend?!"),

            _("OH GOD PLEASE... I can't stop... but what if her FRIENDS see me loving cock...!"),

            _("HARDER! But if anyone tells her I'm with a guy... I'll DIE!"),

        ],
        "girl_cum.boyfriend.public_shy": [
            _("C-CUMMING...! Was I too loud?! What if someone tells him...!"),

            _("OH NO... I just... in PUBLIC... if my boyfriend finds out I'll die..."),

            _("I'm cumming! Oh Fuck! Your cock is making me cum!"),

        ],
        "girl_cum.girlfriend.public_shy": [
            _("C-CUMMING...! Was I too loud?! What if someone tells her I was with a man...!"),

            _("OH NO... I just came on a cock... in PUBLIC... if my girlfriend finds out I'll die..."),

            _("I'm cumming! Oh Fuck! A man's cock is making me cum and she'll never know!"),

        ],
        "cum_outside.boyfriend.public_shy": [
            _("Quick, clean it up...! If someone sees the mess and my boyfriend finds out..."),

            _("At least it's not inside... but the evidence... someone could see..."),

            _("Covered in cum that isn't my boyfriend's... oh god..."),

        ],
        "cum_outside.girlfriend.public_shy": [
            _("Quick, clean it up...! If someone sees your mess on me and my girlfriend finds out..."),

            _("At least it's not inside... but your cum on me... someone could see..."),

            _("Covered in your cum... in public... if she ever finds out..."),

        ],
        "dressup.boyfriend.public_shy": [
            _("I need to leave... separately... if anyone saw us and tells my boyfriend..."),

            _("Oh god... I hope nobody recognized me... he can never know about this..."),

            _("Eyes up here... or maybe not~"),

        ],
        "dressup.girlfriend.public_shy": [
            _("I need to leave... separately... if anyone saw me with a man and tells my girlfriend..."),

            _("Oh god... I hope nobody recognized me with a guy... she can never know about this..."),

            _("Eyes up here... she'd never look at me the same if she knew..."),

        ],

        # --- Boyfriend + Public Fetish (expanded) ---
        "moan.speed3.boyfriend.public_fetish": [
            _("YES! LET HIS FRIENDS SEE! I'M CHEATING ON HIM IN PUBLIC! AHHH!"),

            _("HARDER! LOUDER! I WANT EVERYONE TO KNOW I'M NOT HIS GOOD GIRL! FUCK!"),

            _("YES! Right there! Your dick is so DEEP!"),

        ],
        "moan.speed3.girlfriend.public_fetish": [
            _("YES! LET HER FRIENDS SEE ME WITH A MAN! I LOVE COCK! AHHH!"),

            _("HARDER! LOUDER! LET EVERYONE KNOW HER LESBIAN GIRLFRIEND LOVES DICK! FUCK!"),

            _("YES! Her friends should see THIS! Her girlfriend, SCREAMING for a man!"),

        ],
        "girl_cum.boyfriend.public_fetish": [
            _("CUMMING! In PUBLIC! Cheating on my boyfriend for EVERYONE to see! AAAH!"),

            _("OH GOD YES! Someone probably saw! Someone might TELL him! INCREDIBLE!"),

            _("OH GOD! I'm cumming! Don't stop!"),

        ],
        "girl_cum.girlfriend.public_fetish": [
            _("CUMMING! In PUBLIC! A MAN is making me cum while my girlfriend has NO idea! AAAH!"),

            _("OH GOD YES! Someone probably saw me cumming on a COCK! Let them tell her! INCREDIBLE!"),

            _("OH GOD! A man is making me cum in public! She could NEVER do this! Don't stop!"),

        ],
        "cum_outside.boyfriend.public_fetish": [
            _("Mm... the evidence is right there for anyone to see... my boyfriend would die..."),

            _("Anyone walking by can tell what his girlfriend just did..."),

            _("Covered in cum that isn't my boyfriend's... oh god..."),

        ],
        "cum_outside.girlfriend.public_fetish": [
            _("Mm... the evidence of a man is right there for anyone to see... my girlfriend would die..."),

            _("Anyone walking by can tell what her girlfriend just did..."),

            _("Covered in your cum in public... while I have a girlfriend... thrilling..."),

        ],

        # --- Boyfriend + Virgin ---
        "moan.speed1.boyfriend.virgin": [
            _("Mm... my first time... and it's not with my boyfriend... ahh..."),

            _("He was supposed to be my first... and here I am... with you..."),

            _("I can feel every inch stretching me..."),

        ],
        "moan.speed1.girlfriend.virgin": [
            _("Mm... my first time with a man... and my girlfriend has no idea... ahh..."),

            _("She thought I'd never be with a guy... and here I am... taking cock..."),

            _("I can feel every inch stretching me... nothing like what she does..."),

        ],
        "moan.speed2.boyfriend.virgin": [
            _("Ahh... I'm losing my virginity... to someone who isn't my boyfriend... oh god..."),

            _("My boyfriend waited for me... and you're the one getting it... ahh..."),

            _("Yes... harder... your dick feels incredible..."),

        ],
        "moan.speed2.girlfriend.virgin": [
            _("Ahh... my first cock... and my girlfriend doesn't know I wanted this... oh god..."),

            _("My girlfriend thought I'd never want a man... and you're proving her wrong... ahh..."),

            _("Yes... harder... I can't believe how good a real dick feels..."),

        ],
        "cum_inside.boyfriend.virgin": [
            _("My first time... and another man came inside me. My boyfriend will never know."),

            _("I lost my virginity AND got creampied by someone who isn't my boyfriend..."),

            _("My first cock AND a forced creampie?! What is WRONG with you?!"),

        ],
        "cum_inside.girlfriend.virgin": [
            _("My first time with a man... and he came inside me. My girlfriend will never know."),

            _("I lost my virginity and got creampied... while I have a girlfriend..."),

            _("My first cock AND a forced creampie?! What is WRONG with you?!"),

        ],
        "dressup.boyfriend.virgin_lost": [
            _("I'm no longer a virgin... and my boyfriend has no idea another man took it."),

            _("Getting dressed after losing my virginity to someone who isn't him... I feel everything."),

            _("Like what you see? Your cock is already responding..."),

        ],
        "dressup.girlfriend.virgin_lost": [
            _("I'm no longer a virgin... to cock anyway. My girlfriend has no idea a man took it."),

            _("Getting dressed after losing my virginity to a man... while I have a girlfriend... I feel everything."),

            _("Like what you see? Your cock is already responding... she could never make me feel this way..."),

        ],

        # ══════════════════════════════════════════════════════════
        #  TRAIT COMBO — Remaining gap
        # ══════════════════════════════════════════════════════════

        # --- Hate Cum + Public Fetish ---
        "moan.speed1.hate_cum.public_fetish": [
            _("I love doing it in public... but if you cum anywhere NEAR me out here..."),

            _("The public part? Amazing. The cum part? Keep it FAR away."),

            _("Mmm... I love how big you are..."),

        ],
        "cum_inside.hate_cum.public_fetish": [
            _("You came inside me?! In PUBLIC?! Now I have to deal with THIS where people might SEE?!"),

            _("Disgusting AND in public! Everyone can probably tell what just happened!"),

            _("I feel it leaking... there was so much..."),

        ],
        "cum_outside.hate_cum.public_fetish": [
            _("At least you kept it out of me... but now there's evidence in PUBLIC!"),

            _("Gross. But at least it's not inside me. Clean it up before someone sees!"),

            _("At least it's not inside me... but still... gross..."),

        ],

        # ══════════════════════════════════════════════════════════
        #  TRAIT COMBO — Remaining pairs (coverage pass)
        # ══════════════════════════════════════════════════════════

        # --- Camera Hater + Cheater ---
        "moan.speed2.camera_hater.cheater": [
            _("Ahh... I don't care about cheating... but cameras TERRIFY me... ahh..."),

            _("I'll fuck who I want... just no EVIDENCE... oh god..."),

            _("My %(pl)s thinks I'm %(poss)s... your cock knows the truth..."),

        ],
        "dressup.camera_hater.cheater": [
            _("The cheating? I don't care. But if someone filmed us, I'm finished."),

            _("I need to check every surface for cameras. The sex was fine. The paranoia isn't."),

            _("No cameras while I'm undressing. NONE."),

        ],

        # --- Camera Hater + Cute ---
        "moan.speed1.camera_hater.cute": [
            _("Mm... please promise me no one is watching us... I'm so scared..."),

            _("Ahh... if there's a camera... please tell me there's not... *whimper*"),

            _("You're so gentle... I love it..."),

        ],
        "dressup.camera_hater.cute": [
            _("That was nice... but can you check if anyone saw us? I'm so paranoid..."),

            _("I liked that... but please tell me no one was recording..."),

            _("I'm vulnerable... no recording..."),

        ],

        # --- Camera Hater + Hardcore ---
        "moan.speed2.camera_hater.hardcore": [
            _("Harder! But if I see a camera I'll break it AND your face!"),

            _("Give it to me rough! But no recording! I'll fuck you up!"),

            _("Harder! Your cock can go deeper than that!"),

        ],

        # --- Camera Hater + Hate Cum ---
        "cum_inside.camera_hater.hate_cum": [
            _("You came inside me?! AND there might be cameras?! This is a NIGHTMARE!"),

            _("Disgusting AND potentially filmed?! I want to die!"),

            _("You came inside me?! And there's a camera?! This is a nightmare!"),

        ],

        # --- Camera Hater + Loyal ---
        "moan.speed1.camera_hater.loyal": [
            _("This is insane... I have a boyfriend AND cameras could expose me..."),

            _("I'm going crazy doing this... the desire is overpowering everything..."),

            _("You're so hard inside me... mmm..."),

        ],

        # --- Camera Hater + Public Fetish ---
        "moan.speed2.camera_hater.public_fetish": [
            _("I love the public part... but people have PHONES. Anyone could film us..."),

            _("The thrill of being seen is amazing... but recorded? That's different..."),

            _("No one can ever see how your cock makes me act..."),

        ],

        # --- Camera Hater + Public Shy ---
        "moan.speed1.camera_hater.public_shy": [
            _("We're in public... and everyone has cameras on their phones... I can't..."),

            _("Someone could film us... in PUBLIC... this is my worst nightmare..."),

            _("Just us... no evidence... mmm..."),

        ],

        # --- Camera Lover + Cute ---
        "moan.speed1.camera_lover.cute": [
            _("Mm... I wish you were filming this... is that embarrassing to say?"),

            _("Ahh... I keep thinking about what this would look like on camera..."),

            _("Mmm... I love how big you are..."),

        ],
        "dressup.camera_lover.cute": [
            _("I wish we'd recorded that... is it weird that I wanted that on camera?"),

            _("That was so nice... next time, can we film it? If you don't mind..."),

            _("Don't stare too much... this is embarrassing..."),

        ],

        # --- Camera Lover + Hate Cum ---
        "cum_face.camera_lover.hate_cum": [
            _("Ugh, gross... but I bet the footage of my reaction was priceless."),

            _("Disgusting. But if that was on camera... it probably looked dramatic."),

            _("My face... covered in cum... disgusting..."),

        ],

        # --- Camera Lover + Loyal ---
        "moan.speed2.camera_lover.loyal": [
            _("I want this on camera so badly... the desire is making me lose all reason... ahh..."),

            _("Film me... I've gone insane... this craving is stronger than anything..."),

            _("Don't stop... your cock hits every spot..."),

        ],

        # --- Camera Lover + Public Shy ---
        "moan.speed1.camera_lover.public_shy": [
            _("I want to film this but... we're in public... people might see..."),

            _("Camera? Yes. Public? I'm terrified. Both at once? I'm conflicted..."),

            _("Film me... I want to watch myself later..."),

        ],

        # --- Cheater + Public Fetish ---
        "moan.speed2.cheater.public_fetish": [
            _("Ahh... cheating in public... if %(poss)s friends see me... even better..."),

            _("My %(pl)s could find out from a random stranger... the thrill..."),

            _("Your cock is driving me crazy..."),

        ],

        # --- Cheater + Public Shy ---
        "moan.speed1.cheater.public_shy": [
            _("I don't mind cheating... but in public? What if someone tells %(po)s..."),

            _("I'll cheat... but I wish we were somewhere more private..."),

            _("Nice and deep... I love it..."),

        ],

        # --- Cum Slut + Public Shy ---
        "moan.speed2.cum_slut.public_shy": [
            _("Ahh... I want everything... but we're outside... what if someone sees..."),

            _("I need more... but people are around... what if they see how eager I am..."),

            _("I NEED your cum... fuck me harder..."),

        ],
        "cum_inside.cum_slut.public_shy": [
            _("You came inside me... I love it... but we're in PUBLIC and it might leak..."),

            _("All that cum... in me... and someone could see me walking funny after..."),

            _("My pussy is full of your cum... I can't believe I let you..."),

        ],

        # --- Cute + Loyal ---
        "moan.speed1.cute.loyal": [
            _("Mm... this is crazy... I have a boyfriend but you feel so good... *whimper*"),

            _("I'm going insane... you're so gentle and my body won't let me stop..."),

            _("My boyfriend would be heartbroken... but your cock feels so good..."),

        ],
        "girl_post_cum.cute.loyal": [
            _("That was so intense... I can't believe how much my body craved that..."),

            _("You were so sweet... and the desire just overwhelmed everything..."),

            _("Oh god... that was incredible... your cock..."),

        ],

        # --- Cute + Public Shy ---
        "moan.speed1.cute.public_shy": [
            _("Mm... s-someone might hear... please be gentle... and quiet..."),

            _("Ahh... not so loud... we're in public... *blush*"),

            _("You're so hard inside me... mmm..."),

        ],

        # --- Cute + Hate Cum ---
        "moan.speed1.cute.hate_cum": [
            _("Mmm... you feel so good... just... promise you'll be careful when you finish, okay?"),

            _("This is so nice... I just get nervous thinking about the mess..."),

            _("Keep going, just like that... but you'll pull out, right? Promise me?"),

        ],
        "moan.speed2.cute.hate_cum": [
            _("Ahh... it feels amazing... but please, please remember to pull out..."),

            _("Oh god... more... but I'm serious about the mess, okay? Please..."),

            _("You feel so good but... please be careful when you're close..."),

        ],
        "moan.speed3.cute.hate_cum": [
            _("OH GOD... I can't think straight... just... please don't finish inside... please..."),

            _("It feels too good to stop... but I'm begging you... not inside..."),

            _("I'M LOSING MY MIND... please... I know I'm a mess right now but... not inside me..."),

        ],

        # --- Hardcore + Public Fetish ---
        "moan.speed2.hardcore.public_fetish": [
            _("Harder! Let everyone hear! Let them watch!"),

            _("Fuck me in front of everyone! I don't care!"),

            _("Fuck... you're hitting so deep..."),

        ],

        # --- Hate Cum + Loyal ---
        "cum_inside.hate_cum.loyal": [
            _("You came inside me?! I have a %(pl)s! And I HATE this! How could you?!"),

            _("Disgusting AND I cheated on my %(pl)s?! This is the worst day of my life!"),

            _("You FORCED your cum inside me?! I feel SICK!"),

        ],

        # --- Hate Cum + Public Shy ---
        "cum_inside.hate_cum.public_shy": [
            _("You came inside me?! In PUBLIC?! Someone could SEE the evidence!"),

            _("Gross AND public?! Now I have to walk around with this inside me?!"),

            _("You came so deep... I can feel it all..."),

        ],

        # --- Loyal + Public Fetish ---
        "moan.speed2.loyal.public_fetish": [
            _("In public, behind his back... this is total madness... and I want MORE... ahh..."),

            _("The thrill is driving me completely insane... my desire has taken over..."),

            _("He's so good to me... and another man's dick is making me scream..."),

        ],

        # --- Loyal + Public Shy ---
        "moan.speed1.loyal.public_shy": [
            _("In public... with a boyfriend... this is crazy... but the desire is winning..."),

            _("I shouldn't be here... but my body dragged me into this madness..."),

            _("You're so hard inside me... mmm..."),

        ],

        # --- Loyal + Virgin ---
        "moan.speed1.loyal.virgin": [
            _("My first time... not with my %(pl)s... this is insane... but I want it so badly..."),

            _("I was saving this... the desire to give it to YOU is driving me crazy..."),

            _("You're so hard inside me... mmm..."),

        ],
        "cum_inside.loyal.virgin": [
            _("My first time... and I wanted it so desperately I lost all reason..."),

            _("I was saving myself... but the craving was too intense... I've gone completely mad..."),

            _("My pussy is full of your cum... I can't believe I let you..."),

        ],

        # --- Public Fetish + Virgin ---
        "moan.speed1.public_fetish.virgin": [
            _("My first time... in public... the thought of being seen... oh god..."),

            _("I've never done this... and people could WATCH... that's so hot..."),

            _("Nice and deep... I love it..."),

        ],

        # --- Public Shy + Virgin ---
        "moan.speed1.public_shy.virgin": [
            _("My first time... and we're in PUBLIC?! I'm so scared..."),

            _("I've never done this... and someone might SEE... please hold me..."),

            _("Mmm... I love how big you are..."),

        ],

        # ══════════════════════════════════════════════════════════
        #  COERCION — Blackmailed or financially coerced scenes.
        #  She did NOT consent willingly. Tone: reluctance, anger,
        #  shame, body-betrayal. Split by blackmailed vs paid.
        # ══════════════════════════════════════════════════════════

        # ── Moans Speed 2 ──
        "moan.speed2.blackmailed": [
            _("Ngh... I hate this... I hate that you're making me do this..."),
            _("Ahh... you think you've won? This means NOTHING..."),
            _("Stop... looking at me like that... this is not... ahh... pleasure..."),
        ],
        "moan.speed2.paid": [
            _("Ahh... earn your money... that's all this is... just business..."),
            _("Ngh... I can't believe I'm doing this for cash..."),
            _("Mm... just... finish fast, okay? I want this over..."),
        ],

        # ── Moans Speed 3 ──
        "moan.speed3.blackmailed": [
            _("FUCK! You're going too hard! I didn't agree to THIS!"),
            _("AHH! STOP... no... don't stop... NO, I mean STOP! I hate this!"),
            _("NGH! You're DESTROYING me! This wasn't the DEAL!"),
        ],
        "moan.speed3.paid": [
            _("FUCK! You're fucking me too hard! I would have asked for MORE money!"),
            _("AHH! SLOW DOWN! You're going to BREAK me! This wasn't worth the price!"),
            _("OH GOD! You're going to break my pussy! Go SLOWER! I have a LIFE outside of this!"),
        ],

        # ── Moans Speed 3 + Trait combos ──
        "moan.speed3.blackmailed.hardcore": [
            _("FUCK! I hate you... but FUCK that feels... NO! I hate you!"),
            _("HARDER! No, wait... I didn't mean... you're FORCING me to like this!"),
            _("AHH! You son of a... don't you DARE think I'm enjoying this!"),
        ],
        "moan.speed3.paid.hardcore": [
            _("HARDER! ...Shit, I didn't mean to say that! Just... you're paying, so whatever!"),
            _("FUCK! My body is reacting but my BRAIN hates every second! ...More!"),
            _("AHH! If you're going to fuck me like this, the price just went UP!"),
        ],
        "moan.speed3.blackmailed.cute": [
            _("P-please... not so hard... I c-can't take it... *sob* ...please..."),
            _("AAAH! It hurts! You're being too rough! I didn't... I didn't want this..."),
            _("S-stop... please stop going so fast... I'm scared..."),
        ],
        "moan.speed3.paid.cute": [
            _("AHH! T-too fast! You're hurting me! I didn't agree to this speed!"),
            _("P-please slow down... the money isn't worth... ahh... this much pain..."),
            _("S-stop! You're going too hard! I-I'll give the money back, just STOP!"),
        ],
        "moan.speed3.blackmailed.cum_slut": [
            _("AHH! Fuck... my body... NO! I refuse to enjoy being blackmailed!"),
            _("OH GOD! Why does it feel... no! This is WRONG! You're FORCING me!"),
            _("NNGH! I can feel myself getting close... NO! I won't give you that satisfaction!"),
        ],
        "moan.speed3.blackmailed.lesbian": [
            _("AHH! A man is... inside me... because of a VIDEO... this is a nightmare!"),
            _("STOP! I'm not supposed to... with a GUY... ahh... I hate this!"),
            _("NGH! My body is reacting to a MAN... this can't be happening..."),
        ],
        "moan.speed3.paid.lesbian": [
            _("AHH! I can't believe I took money to let a MAN do this to me!"),
            _("FUCK! This doesn't mean anything! You're paying, that's IT!"),
            _("NGH! A man is making me... NO! The money! Think about the money!"),
        ],
        "moan.speed3.blackmailed.hate_cum": [
            _("AHH! DON'T YOU DARE finish! Especially not INSIDE! I swear to GOD!"),
            _("FUCK! If you cum anywhere NEAR me I'll... AHH!"),
            _("NGH! You better pull out! Being blackmailed is bad enough without your MESS!"),
        ],
        "moan.speed3.paid.hate_cum": [
            _("AHH! If you cum on me the price DOUBLES! I'm serious!"),
            _("FUCK! No cumming! That was NOT part of the deal!"),
            _("NGH! I'm only doing this for money, NOT to be covered in your filth!"),
        ],
        "moan.speed3.blackmailed.boyfriend": [
            _("AHH! YOU'RE GONNA BREAK MY PUSSY! GO SLOW! I HAVE A BOYFRIEND!"),
            _("NGH! Stop being so rough! If my boyfriend sees bruises he'll KNOW!"),
            _("FUCK! Not so hard! I can't go home to my boyfriend walking like THIS!"),
        ],
        "moan.speed3.paid.boyfriend": [
            _("AHH! SLOWER! My boyfriend is going to notice if you wreck me like this!"),
            _("NGH! Not that hard! I need to look NORMAL when I see my boyfriend later!"),
            _("FUCK! If my boyfriend finds out I let someone fuck me this hard for MONEY...!"),
        ],
        "moan.speed3.blackmailed.girlfriend": [
            _("AHH! STOP! My girlfriend would DIE if she saw a man doing this to me!"),
            _("NGH! Not so rough! A man is DESTROYING me and I can't even tell my girlfriend WHY!"),
            _("FUCK! If she saw how hard a man is fucking me right now... our relationship would be OVER!"),
        ],
        "moan.speed3.paid.girlfriend": [
            _("AHH! I took money to let a MAN do THIS to me! My girlfriend can never know!"),
            _("NGH! You're going way too hard! I'm not built for this! I have a GIRLFRIEND!"),
            _("FUCK! My girlfriend thinks I'm loyal and here I am getting DESTROYED for cash!"),
        ],

        # ── Girl Cum (orgasm during coerced scene) ──
        "girl_cum.blackmailed": [
            _("No... NO! I... I came... I can't believe you made me cum like this... no..."),
            _("I... cummed in this situation... I can't believe it... this is so fucked up..."),
            _("Son of a bi... I... I can't believe you made me cum... No..."),
        ],
        "girl_cum.paid": [
            _("No... I wasn't supposed to... this was just for money... I wasn't supposed to CUM..."),
            _("Shit... I came... while being PAID... what does that make me..."),
            _("Ahh... no... I actually... finished? This was just a transaction..."),
        ],
        "girl_cum.blackmailed.hardcore": [
            _("FUCK! I came... I HATE that I came! You piece of... AAAGH!"),
            _("You made me cum with BLACKMAIL?! I'll NEVER forgive you for this!"),
            _("That orgasm means NOTHING! My body betrayed me! I still DESPISE you!"),
        ],
        "girl_cum.paid.hardcore": [
            _("SHIT! I came! This was supposed to be business! My body is a damn TRAITOR!"),
            _("I finished... while being PAID... you know what, charge me DOUBLE, I don't care!"),
            _("That orgasm wasn't for YOU! My body just... reacted! Don't look so smug!"),
        ],
        "girl_cum.blackmailed.cute": [
            _("*crying* I... I came... while being forced... what's wrong with me..."),
            _("No... please don't look at me... I... I finished... and I hate myself for it..."),
            _("*sob* My body... it responded... even though I didn't want it to... I'm so ashamed..."),
        ],
        "girl_cum.paid.cute": [
            _("*sniff* I... I came... I was just doing this for money... why did my body..."),
            _("N-no... I wasn't supposed to enjoy it... it was just a job... why did I cum..."),
            _("*whimper* I feel so dirty... I came while being paid... what am I becoming..."),
        ],
        "girl_cum.blackmailed.cum_slut": [
            _("NO! Don't... don't read into that! I cum easily! It doesn't mean I LIKED this!"),
            _("My body is a traitor... I came so hard... but it means NOTHING! You hear me?!"),
            _("FUCK... that was... NO! I didn't enjoy being blackmailed into cumming!"),
        ],
        "girl_cum.blackmailed.lesbian": [
            _("No... a MAN made me cum... while being blackmailed... I want to disappear..."),
            _("I came... from a man... because of a video... my girlfriend can never know..."),
            _("*shaking* My body responded to a man... this isn't who I am... this isn't real..."),
        ],
        "girl_cum.paid.lesbian": [
            _("A man... made me cum... and I PAID for this situation... what is happening to me..."),
            _("I came from a man's cock... for MONEY... my girlfriend would never understand..."),
            _("No... I'm a lesbian... I don't cum from men... that was just... a physical reaction..."),
        ],
        "girl_cum.blackmailed.boyfriend": [
            _("I came... with another man... while being BLACKMAILED... I'm the worst girlfriend alive..."),
            _("He'd leave me if he knew I came like that... while being forced by another guy..."),
            _("My boyfriend has never made me cum that hard... and this was against my will... what's wrong with me..."),
        ],
        "girl_cum.paid.boyfriend": [
            _("I came... while cheating for MONEY... my boyfriend deserves so much better..."),
            _("He thinks I'm at work... and I just came on another man's cock for CASH..."),
            _("I sold myself AND came... what would he think if he knew..."),
        ],
        "girl_cum.blackmailed.girlfriend": [
            _("I came from a man... while being blackmailed... she can never, EVER find out..."),
            _("My girlfriend... she'd be destroyed if she knew a man made me cum like this..."),
            _("A video forced me into this... and my body ENJOYED it... I'm disgusting..."),
        ],

        # ── Girl Post-Cum ──
        "girl_post_cum.blackmailed": [
            _("...Don't say a word. That orgasm changes NOTHING about what you did to me."),
            _("My body reacted. That's it. You're still a monster for forcing me into this."),
            _("...I need a minute. Don't touch me. Don't look at me. Don't say anything."),
        ],
        "girl_post_cum.paid": [
            _("...That wasn't part of the deal. The orgasm was... involuntary. Let's move on."),
            _("I came. It happens. Doesn't change the fact that this is a business transaction."),
            _("...Well. That was unexpected. You still owe me the full amount, by the way."),
        ],

        # ── Cum Inside (creampie during coerced scene) ──
        "cum_inside.blackmailed": [
            _("You... you came INSIDE me?! Being blackmailed wasn't enough?! You HAD to...!"),
            _("NO! I felt it... you came inside... you absolute PIECE OF...!"),
            _("I can feel it... your cum inside me... this is the worst day of my life..."),
        ],
        "cum_inside.paid": [
            _("You came INSIDE?! That was NOT part of the deal! That costs EXTRA!"),
            _("I can feel it... you came inside me... for THIS I'd need ten times the money!"),
            _("NO! Pull out! You... you already... I can feel it dripping... this wasn't agreed upon!"),
        ],
        "cum_inside.blackmailed.hate_cum": [
            _("YOU CAME INSIDE ME?! I HATE cum! And you FORCED me AND came INSIDE?! I'LL KILL YOU!"),
            _("No no no NO! I can feel your disgusting cum inside me! Being blackmailed AND creampied?!"),
            _("I'm going to be SICK... your cum is inside me... I already hated this and now THIS?!"),
        ],
        "cum_inside.paid.hate_cum": [
            _("YOU CAME INSIDE?! NO AMOUNT OF MONEY covers a CREAMPIE! I HATE your cum!"),
            _("That's IT! I don't care about the money! You came inside and I SPECIFICALLY said NO!"),
            _("I can feel your disgusting cum... inside me... for MONEY... I need to throw up..."),
        ],
        "cum_inside.blackmailed.cum_slut": [
            _("You came inside... and I... no. NO. I am NOT going to enjoy this. Not like this."),
            _("I can feel your cum filling me... and my body... STOP reacting! This was FORCED!"),
            _("Fuck... it's so warm inside... NO! I refuse to moan about being creampied by my BLACKMAILER!"),
        ],
        "cum_inside.blackmailed.boyfriend": [
            _("You came INSIDE me?! I have a BOYFRIEND! And you BLACKMAILED me into this AND came inside?!"),
            _("His cum is inside me... not my boyfriend's... a blackmailer's... I can never face him again..."),
            _("If my boyfriend finds out another man came inside me while I was being FORCED... it's over..."),
        ],
        "cum_inside.paid.boyfriend": [
            _("You came INSIDE me?! My boyfriend... oh god... I took money AND let you cum inside..."),
            _("I can feel another man's cum inside me... and I did it for MONEY... he'd never forgive this..."),
            _("Inside?! INSIDE?! I have a boyfriend and you just... for a few dollars... oh god..."),
        ],
        "cum_inside.blackmailed.lesbian": [
            _("A man's cum... INSIDE me... while being BLACKMAILED... this is my worst nightmare..."),
            _("You came inside a LESBIAN... by FORCE... I can feel your cum and I want to SCREAM..."),
            _("No... a man came inside me... I can feel it... I'm going to be sick..."),
        ],
        "cum_inside.paid.lesbian": [
            _("A man came INSIDE me... for MONEY... I'm a lesbian who got paid to take a creampie..."),
            _("I can feel his cum inside me... I took MONEY for this... my girlfriend would be destroyed..."),
            _("You came inside a LESBIAN... and I LET you because of money... what am I doing with my life..."),
        ],
        "cum_inside.paid.cum_slut": [
            _("You came inside... and I... it feels... NO! I'm being PAID! I can't enjoy a creampie right now!"),
            _("I can feel it filling me up and my body is... STOP! This is a transaction, not pleasure!"),
            _("Fuck... your cum inside me feels... NO! Money! This is about MONEY, not about how good it feels!"),
        ],
        "cum_inside.blackmailed.girlfriend": [
            _("A man came INSIDE me... while being BLACKMAILED... she can never find out about this..."),
            _("My girlfriend's trust... destroyed... a man's cum inside me because of a STUPID video..."),
            _("If my girlfriend ever finds out a man came inside me... blackmailed or not... we're done..."),
        ],
        "cum_inside.paid.girlfriend": [
            _("I let a man cum INSIDE me... for MONEY... while I have a girlfriend... I'm the worst..."),
            _("My girlfriend would leave me if she knew I took money AND a creampie from a man..."),
            _("A man's cum inside me... paid for... she thinks I'm at class and I'm here getting creampied for cash..."),
        ],

        # ── Cum Outside ──
        "cum_outside.blackmailed": [
            _("Ugh... at least you didn't do it inside... get that off me. NOW."),
            _("Your cum on my body... because you blackmailed me... clean it up and GET OUT."),
            _("...Disgusting. Are you done? Can I go now? Or do you want to ruin my day more?"),
        ],
        "cum_outside.paid": [
            _("Great. You got it on me. That'll cost extra for the cleaning bill."),
            _("Ugh... at least it's not inside... give me something to wipe off."),
            _("...Done? Good. Money first, then I'll clean up. In that order."),
        ],

        # ── Cum Face ──
        "cum_face.blackmailed": [
            _("MY FACE?! You came on my FACE?! Being forced wasn't ENOUGH for you?!"),
            _("I have your cum on my face... because of a VIDEO... I want to die..."),
            _("Wipe this off me. NOW. Don't you DARE take a picture."),
        ],
        "cum_face.paid": [
            _("MY FACE?! That was NOT in the agreement! Double price! TRIPLE!"),
            _("You came on my face... for MONEY... I'm washing this off and you're paying extra."),
            _("Great. Just great. Cum on my face. Like I needed to feel cheaper than I already do."),
        ],

        # ── Cum Mouth ──
        "cum_mouth.blackmailed": [
            _("*gags* You came in my MOUTH?! I'll never forgive you for this!"),
            _("*spits* Disgusting... your cum in my mouth... because of BLACKMAIL..."),
            _("I can still taste it... forced to swallow a blackmailer's cum... I'm going to be sick..."),
        ],
        "cum_mouth.paid": [
            _("*gags* Mouth was NOT part of the deal! That's a premium service and you did NOT pay for it!"),
            _("*spits* Ugh... I can taste it... for THIS kind of thing you pay upfront, not after..."),
            _("You came in my mouth... ugh... the things I do for money..."),
        ],

        # ── Cum Tits ──
        "cum_tits.blackmailed": [
            _("On my chest... because I had no choice... hand me something to clean up."),
            _("Your cum on my tits... while being forced... just wipe it off and don't look at me."),
            _("At least it wasn't my face... or inside... just get me a towel."),
        ],
        "cum_tits.paid": [
            _("On my chest... fine. At least it's not inside. Give me a towel."),
            _("My tits covered in cum... for money... this is my life now apparently."),
            _("The price didn't include a cleanup fee. You're paying for dry cleaning."),
        ],

        # ══════════════════════════════════════════════════════════
        #  PLAYER CHEATING — Player has a girlfriend, doing things
        #  with a different girl. Lines are from the OTHER girl's POV.
        # ══════════════════════════════════════════════════════════

        # --- Generic (no extra trait) ---
        "creampie_req.player_cheating": [
            _("Cum inside me... let your girlfriend wonder where you've been."),

            _("Fill me up... I want something that's supposed to be hers."),

            _("Don't pull out... I need your cum in me..."),

        ],
        "dressup.player_cheating": [
            _("Go home to your girlfriend. She doesn't need to know about any of this."),

            _("Getting dressed... you should probably shower before you see her."),

            _("Like what you see? Your cock is already responding..."),

        ],
        "condom_ask.player_cheating": [
            _("Take it off... your girlfriend isn't here to complain about it."),

            _("No condom? That's what you do with girls who AREN'T your girlfriend?"),

            _("Please tell me you have one... your cock is huge..."),

        ],

        # --- Player Cheating + Cheater (she's also a cheater, mutual cheating thrill) ---
        "dressup.player_cheating.cheater": [
            _("We both need to go home and pretend this never happened. See you next time?"),

            _("Your girlfriend. My %(pl)s. Neither will ever know. ...Until next time."),

            _("I can see you getting hard already... patience..."),

        ],
        "girl_cum.player_cheating.cheater": [
            _("CUMMING! While both our partners are CLUELESS! This is so WRONG! AHHHH!"),

            _("OH GOD YES! Your girlfriend, my %(pl)s, and we're here doing THIS! AHHHH!"),

            _("AAAH! I'm cumming so hard on your dick!"),

        ],

        # --- Player Cheating + Cute (shy/guilty about the player's cheating) ---
        "moan.speed3.player_cheating.cute": [
            _("OH GOD! I feel so BAD! Your girlfriend! But I CAN'T STOP! AHHH!"),

            _("I'm SORRY! To her! But you feel TOO GOOD! Oh god!"),

            _("I'm losing my mind... you're so DEEP! Please!"),

        ],
        "girl_cum.player_cheating.cute": [
            _("I'm cumming... oh god... your girlfriend would be heartbroken... AHHHH! I'm sorry!"),

            _("AAAH! I'm so sorry... I shouldn't be feeling this good with someone else's boyfriend...!"),

            _("I think I just... oh god... you made me feel so good..."),

        ],
        "dressup.player_cheating.cute": [
            _("You should go back to her... I feel guilty enough for both of us..."),

            _("Please be good to her... even though we just did this..."),

            _("Eyes up here... or maybe not~"),

        ],
        "girl_post_cum.player_cheating.cute": [
            _("That was incredible... but your girlfriend... do you feel guilty? I do..."),

            _("I can't believe how good that felt... she'd be so hurt if she knew..."),

            _("Oh god... that was incredible... your cock..."),

        ],

        # --- Player Cheating + Hardcore (aggressive, likes stealing him) ---
        "moan.speed1.player_cheating.hardcore": [
            _("Mmm... your girlfriend's loss. HARDER."),

            _("She can't fuck you like I can. And she knows it."),

            _("Don't stop... just like that..."),

        ],
        "cum_inside.player_cheating.hardcore": [
            _("You came inside ME. Not her. Remember that."),

            _("Fill me up. Your girlfriend gets the leftovers."),

            _("You just came inside me... and you have a GIRLFRIEND... her boyfriend's cum in another girl..."),

        ],
        "dressup.player_cheating.hardcore": [
            _("Go home to your boring girlfriend. You know where to find me when she can't satisfy you."),

            _("That was a real fuck. Something tells me she can't do that for you."),

            _("I can see you getting hard already... patience..."),

        ],

        # --- Player Cheating + Cum Slut (wants everything, taunts the girlfriend) ---
        "moan.speed1.player_cheating.cum_slut": [
            _("Mmm... I want everything you'd give her... and more..."),

            _("Your girlfriend doesn't know what she's missing... give me all of it..."),

            _("Mmm... your cock fills me up so well..."),

        ],
        "cum_mouth.player_cheating.cum_slut": [
            _("Swallowed every drop. Does your girlfriend do that? I doubt it."),

            _("All of it down my throat... she doesn't know what she's missing."),

            _("Mmm... your cum tastes so good... I want more..."),

        ],
        "cum_face.player_cheating.cum_slut": [
            _("Cover my face. She'd never let you do this, would she?"),

            _("Her boyfriend's cum all over another girl's face... and I'm loving it."),

            _("My face is dripping with your cum and I love it!"),

        ],
        "creampie_req.player_cheating.cum_slut": [
            _("Cum inside me. I want what she doesn't let you give."),

            _("Fill me up. I'll take everything your girlfriend refuses."),

            _("Inside... please... I want to feel you fill me up..."),

        ],
        "dressup.player_cheating.cum_slut": [
            _("Go home to your girlfriend. I'll keep everything you gave me."),

            _("She has no idea how much of you just ended up inside another girl..."),

            _("Let me undress for you... I know your dick wants this..."),

        ],

        # --- Player Cheating + Camera Lover (wants footage as leverage/thrill) ---
        "moan.speed1.player_cheating.camera_lover": [
            _("Mmm... record this... your girlfriend should see what you do behind her back..."),

            _("Film us... imagine if she found this on your phone... ahh..."),

            _("Your girlfriend doesn't know your cock is inside me right now..."),

        ],
        "moan.speed2.player_cheating.camera_lover": [
            _("Ahh... get this on camera... I want proof that her boyfriend is mine right now..."),

            _("Film me moaning... send it to her... let her know she lost..."),

            _("Mmm... fuck... you're so thick..."),

        ],
        "moan.speed3.player_cheating.camera_lover": [
            _("FILM THIS! Send it to your GIRLFRIEND! Let her SEE! AHHH!"),

            _("OH GOD! Record EVERYTHING! She deserves to KNOW!"),

            _("HARDER! Your dick drives me INSANE!"),

        ],
        "cum_inside.player_cheating.camera_lover": [
            _("You came inside me... on camera. Your girlfriend's worst nightmare."),

            _("Creampied by her boyfriend, caught on film. This footage is priceless."),

            _("All that cum in my pussy that should be your girlfriend's... mine now..."),

        ],
        "dressup.player_cheating.camera_lover": [
            _("Keep that video safe. Or maybe... accidentally leave it on your phone for her to find."),

            _("I wonder what she'd do if she saw the footage of us..."),

            _("Let me undress for you... I know your dick wants this..."),

        ],

        # --- Player Cheating + Public Shy (terrified someone who knows his gf will see) ---
        "moan.speed1.player_cheating.public_shy": [
            _("Mm... what if someone who knows your girlfriend sees us... I'm scared..."),

            _("Ahh... what if her friends are nearby... they'd tell her..."),

            _("Please be quiet... your big cock is hard to be subtle about..."),

        ],
        "moan.speed2.player_cheating.public_shy": [
            _("Oh god... we're in public... someone who knows her could SEE us... ahh..."),

            _("What if she walks by?! What if her FRIENDS walk by?! Oh god..."),

            _("Every thrust goes deeper... don't stop..."),

        ],
        "dressup.player_cheating.public_shy": [
            _("Let's get out of here separately... if anyone saw us together..."),

            _("I hope nobody who knows your girlfriend was around..."),

            _("Eyes up here... or maybe not~"),

        ],

        # --- Player Cheating + Public Fetish (thrill of his gf's friends seeing) ---
        "moan.speed2.player_cheating.public_fetish": [
            _("Ahh... what if her friends see us... that'd be amazing..."),

            _("In public... someone might tell your girlfriend... the thrill... oh god..."),

            _("Yes... harder... your dick feels incredible..."),

        ],
        "girl_cum.player_cheating.public_fetish": [
            _("CUMMING! In PUBLIC! Where anyone could see her boyfriend cheating! AHHHH!"),

            _("OH GOD! Someone could tell your girlfriend! And that makes it SO much better! AAAH!"),

            _("I can't... I'm... CUMMING! Your cock!"),

        ],

        # --- Player Cheating + Public (neutral — no public trait, just aware of the risk) ---
        "moan.speed1.player_cheating.public": [
            _("Mm... someone could see us... and tell your girlfriend..."),

            _("Ahh... out here in the open... cheating on her where anyone could catch us..."),

            _("Someone might walk in... your cock inside me..."),

        ],
        "moan.speed2.player_cheating.public": [
            _("Ahh... in public... someone might recognize you... what would she think..."),

            _("Oh god... anyone could walk by... and your girlfriend would find out like this..."),

            _("Your cock is driving me crazy..."),

        ],
        "moan.speed3.player_cheating.public": [
            _("AHH! I DON'T CARE ANYMORE! Let people see! Let her find out! FUCK!"),

            _("OH GOD! SOMEONE COULD BE WATCHING! Your girlfriend could HEAR about this!"),

            _("CHEAT on her HARDER! Give me ALL your cock!"),

        ],
        "girl_cum.player_cheating.public": [
            _("CUMMING! Out here where anyone could see you cheating! AAAH!"),

            _("OH GOD! I'm cumming... in PUBLIC... with someone else's boyfriend...!"),

            _("I can't... I'm... CUMMING! Your cock!"),

        ],
        "cum_inside.player_cheating.public": [
            _("You came inside me... in public... your girlfriend could've been right around the corner..."),

            _("Creampied in public by another girl's boyfriend... this is so wrong..."),

            _("I can feel your cum filling my pussy... oh god..."),

        ],
        "cum_outside.player_cheating.public": [
            _("At least it's not inside me... but anyone could've seen you pull out..."),

            _("There's evidence everywhere... in public... while you have a girlfriend..."),

            _("Your cum out in the open... someone could tell your girlfriend exactly what they saw..."),

        ],
        "dressup.player_cheating.public": [
            _("Let's get dressed fast... anyone who saw us could tell your girlfriend..."),

            _("We need to act normal... like we didn't just do THAT in public..."),

            _("Like what you see? Your cock is already responding..."),

        ],

        # --- Player Cheating + Public Shy (expanded — terrified of exposure) ---
        "moan.speed3.player_cheating.public_shy": [
            _("AHH! I CAN'T STOP! B-but what if someone SAW... and tells her... oh no oh no..."),

            _("PLEASE... NOT SO LOUD... what if her friends are NEARBY... ahh!"),

            _("YES YES YES! Fuck my little pussy!"),

        ],
        "girl_cum.player_cheating.public_shy": [
            _("CUMMING...! Oh no... I think someone heard... what if they know your girlfriend...!"),

            _("A-AHH...! Was I too loud?! What if someone tells her...!"),

            _("AAAH! I'm cumming so hard on your dick!"),

        ],
        "cum_inside.player_cheating.public_shy": [
            _("Inside me?! IN PUBLIC?! If someone saw that and tells your girlfriend...!"),

            _("Oh god... the evidence... in public... someone could tell her everything..."),

            _("You came so deep... I can feel it all..."),

        ],
        "cum_outside.player_cheating.public_shy": [
            _("At least it's not inside... but if someone SAW... and knows your girlfriend..."),

            _("Clean it up! Quick! Before someone sees and figures out what happened...!"),

            _("Your cum everywhere... in public... if her friends see this we're BOTH dead!"),

        ],

        # --- Player Cheating + Public Fetish (expanded — thrilled by the risk) ---
        "moan.speed1.player_cheating.public_fetish": [
            _("Mm... out in the open... betraying your girlfriend... I love this..."),

            _("Ahh... someone who knows her could be watching right now... exciting..."),

            _("Does she know how big your cock is? Because I definitely do..."),

        ],
        "moan.speed3.player_cheating.public_fetish": [
            _("YES! LET EVERYONE SEE! LET HER FIND OUT! THIS IS INCREDIBLE! AHHH!"),

            _("FUCK ME IN FRONT OF EVERYONE! I WANT HER TO KNOW! AAAH!"),

            _("OH GOD! Every inch! I feel EVERY inch!"),

        ],
        "cum_inside.player_cheating.public_fetish": [
            _("Creampied in public by another girl's boyfriend... I hope someone saw..."),

            _("Your cum inside me... in public... someone should tell your girlfriend about this..."),

            _("All that cum in my pussy that should be your girlfriend's... mine now..."),

        ],
        "cum_outside.player_cheating.public_fetish": [
            _("Mm... the evidence is right there for anyone to see... how thrilling..."),

            _("Anyone passing by can see what her boyfriend just did with me..."),

            _("Your cum in the open... I hope someone who knows your girlfriend walks by~"),

        ],
        "dressup.player_cheating.public_fetish": [
            _("I hope someone took a photo... your girlfriend deserves to see what she's missing..."),

            _("Getting dressed in public after stealing her boyfriend... what a rush..."),

            _("I can see you getting hard already... patience..."),

        ],

        # --- Player Cheating + Public: act-specific ---
        "creampie_req.player_cheating.public": [
            _("Cum inside me... right here in public... let your girlfriend find the evidence..."),

            _("Fill me up where anyone could see... she'll never know what you did out here..."),

            _("In public... inside another girl... your girlfriend would be destroyed..."),

        ],
        "record_accepted.player_cheating.public": [
            _("Film us? Out here? Where your girlfriend might see the video someday?! ...Do it."),

            _("Go ahead, record it... in public, cheating on her... make it real..."),

            _("Okay, record it... your cock deserves to be on camera."),

        ],

        # --- Player Cheating + Public Shy: act-specific ---
        "creampie_req.player_cheating.public_shy": [
            _("I-inside me?! In public?! What if someone sees and tells her...?!"),

            _("N-not here... the evidence... someone could tell your girlfriend..."),

            _("Cum inside me... please... fill my pussy with your cum..."),

        ],

        # --- Player Cheating + Public Fetish: act-specific ---
        "creampie_req.player_cheating.public_fetish": [
            _("Cum inside me out here... let her find the evidence dripping out of me in public..."),

            _("Fill me up where anyone can see... your girlfriend's worst nightmare..."),

            _("Public creampie from someone else's boyfriend... everyone should see this..."),

        ],
        "record_accepted.player_cheating.public_fetish": [
            _("Film it! In public! Send it to your girlfriend! Let her see EVERYTHING!"),

            _("Yes, record us out here... public proof that her boyfriend belongs to me..."),

            _("Record it... I bet she'd die seeing your cock with me on camera..."),

        ],

        # --- Player Cheating + Hate Cum (disgusted AND guilty) ---
        "cum_inside.player_cheating.hate_cum": [
            _("You came inside me?! AND you have a GIRLFRIEND?! You're disgusting!"),

            _("Not only is it gross, you're doing this BEHIND HER BACK?! Ugh!"),

            _("You came inside me AND you have a girlfriend?! That's disgusting on every level!"),

        ],

        # ── Creampie denied (hate_cum) ──
        "cum_inside_denied": [
            _("Don't you dare finish inside me!"),

            _("Pull out! NOW!"),

            _("If you cum inside me, we're DONE!"),

            _("No... pull out, please."),

            _("Not inside... anywhere but inside."),

            _("Please don't cum inside me..."),

        ],
        "cum_inside_denied.hate_cum": [
            _("I SAID pull out! Your disgusting cum is NOT going inside me!"),

            _("Get it OUT! I will KILL you if you finish in there!"),

            _("NO! Pull out right now or I swear this is the LAST time!"),

            _("Absolutely NOT inside me. Don't you dare."),

            _("If you cum inside me, I will NEVER forgive you."),

            _("No. No. No. Pull out. I mean it."),

        ],
        "cum_inside_denied.hj.hate_cum": [
            _("Aim it AWAY! I don't want that anywhere near me!"),

            _("Point it at the floor! NOT at me!"),

            _("Your disgusting cum better not touch my skin! Aim DOWN!"),

        ],
        "cum_inside_denied.bj.hate_cum": [
            _("Don't you DARE cum in my mouth! Pull it out NOW!"),

            _("I'll BITE if you finish in my mouth! I'm serious!"),

            _("Get your cock OUT of my mouth before you cum! NOW!"),

        ],
        "cum_inside_denied.tj.hate_cum": [
            _("Aim away from my chest! I don't want your mess on me!"),

            _("NOT on my tits! Point it somewhere else!"),

            _("Keep your cum OFF my chest! I swear to god!"),

        ],
        "cum_inside_denied.cowgirl.hate_cum": [
            _("I'm getting off RIGHT NOW! Don't finish while I'm on top!"),

            _("Let me off! I refuse to have that inside me!"),

            _("Don't you DARE cum while your cock is inside me! I'm getting OFF!"),

        ],
        "cum_inside_denied.boyfriend": [
            _("Pull out! My boyfriend would KNOW if you finished inside me!"),

            _("Don't cum inside! If my boyfriend finds out..."),

            _("NOT inside! His girlfriend walking around full of another man's cum?! PULL OUT!"),

            _("Are you crazy? Not inside... my boyfriend..."),

            _("I can't let you cum inside me. I'm with someone."),

            _("No... if my boyfriend finds out... pull out."),

        ],
        "cum_inside_denied.girlfriend": [
            _("Pull out! If my girlfriend finds out about this...!"),

            _("Don't cum inside! She can never know about this... this can't happen!"),

            _("NOT inside! Pull out! PULL OUT!"),

            _("Are you crazy? Not inside... my girlfriend would never forgive me..."),

            _("I can't let you cum inside me. I have a girlfriend."),

            _("No... if she finds out about this... pull out."),

        ],
        "cum_inside_denied.player_cheating": [
            _("Pull out! Bad enough we're doing this behind her back!"),

            _("Don't finish inside me! Your girlfriend would die if she knew!"),

            _("You just came inside me... and you have a GIRLFRIEND... her boyfriend's cum in another girl..."),

        ],

        # ── Condom denied in public/shy contexts ──
        "condom_denied.public": [
            _("Not without protection! We're in PUBLIC! Are you insane?!"),

            _("Raw in a public place?! If someone sees AND we're unprotected?! No!"),

            _("That big cock is not going in raw. Period."),

        ],
        "condom_denied.public_shy": [
            _("No condom?! Here?! What if someone sees AND I get... no! NO!"),

            _("We're already risking getting caught! At least use protection!"),

            _("Your dick stays away from me until it's wrapped."),

        ],

        # ── Ex-girlfriend modifier ──
        "cum_inside.ex": [
            _("You came inside your ex... this is so messed up..."),

            _("Inside me... just like when we were together... I hate how good that felt..."),

            _("You came so deep... I can feel it all..."),

        ],
        "cum_face.ex": [
            _("On my face... we're not even together and you still..."),

            _("You always did like finishing on my face... some things don't change..."),

            _("Your cum on your ex's face... we broke up and your cock still owns me..."),

        ],

        # ── Ex mood-specific pools ──
        "moan.speed2.ex": [
            _("Faster... just like old times... why does this still feel so right..."),

            _("You remember exactly how I like it... of course you do..."),

            _("We shouldn't be doing this... but don't you dare stop..."),

        ],
        "moan.speed3.ex": [
            _("Fuck me like you used to... like we never broke up... give it to me..."),

            _("Harder... make me forget everything except this... please..."),

            _("Your ex is begging for more... are you happy now..."),

        ],
        "girl_cum.ex": [
            _("I'm cumming for my ex... oh god... I hate how much I needed this..."),

            _("Cumming... you still know my body better than anyone... damn you..."),

            _("I can't... I'm going to... this doesn't change anything between us...!"),

        ],
        "girl_post_cum.ex": [
            _("That was... we can't keep doing this. We broke up for a reason."),

            _("Okay... I needed that. But this is the last time. Probably."),

            _("I came so hard... ugh, why do you still have this effect on me..."),

        ],
        "cum_mouth.ex": [
            _("You came in my mouth... we're exes and you still cum in my mouth..."),

            _("Swallowing my ex's cum... I can't believe I still do this for you..."),

            _("In my mouth... your taste hasn't changed... I need to stop doing this..."),

        ],

        # ══════════════════════════════════════════════════════════
        #  PLAYER CHEATING — she knows he has a girlfriend
        # ══════════════════════════════════════════════════════════

        # --- Moans ---
        "moan.speed1.player_cheating": [
            _("Your girlfriend doesn't know about this, does she..."),

            _("Does she do this for you too...?"),

            _("I shouldn't be doing this... you have a girlfriend..."),

            _("Is this better than what she gives you...?"),

            _("Mmm... doesn't your girlfriend know you're here right now?"),

            _("Ahh... you're taken and you're doing this with me... naughty."),

            _("Your girlfriend would hate this... and I kind of like that..."),

        ],
        "moan.speed1.hj.player_cheating": [
            _("Another girl's hand on her boyfriend's cock..."),

            _("Does she touch you like this...?"),

            _("Every throb in my hand... she doesn't get this from you..."),

        ],
        "moan.speed1.bj.player_cheating": [
            _("Your girlfriend has no idea I'm doing this right now..."),

            _("Does she go this deep for you...?"),

            _("You're so hard inside me... mmm..."),

        ],
        "moan.speed1.cowgirl.player_cheating": [
            _("I'm riding her boyfriend... and I don't feel sorry..."),

            _("Does she move like this on top of you...?"),

            _("She's out there trusting you... and your dick is in another girl..."),

        ],
        "moan.speed2.player_cheating": [
            _("You feel so good... your girlfriend is missing out..."),

            _("She could never make you feel like this..."),

            _("Think about her... no, forget her. Focus on me..."),

            _("Am I better than her...? Tell me I'm better..."),

            _("Ahh... does your girlfriend moan like this for you? I doubt it..."),

            _("Your girlfriend has no idea you're here... oh god..."),

            _("You're cheating on her with ME... ahhh... that's exciting..."),

        ],
        "moan.speed2.hj.player_cheating": [
            _("My hand is doing what your girlfriend can't..."),

            _("You're so hard for me... harder than you get for her?"),

            _("She doesn't get your cock like this... I do..."),

        ],
        "moan.speed2.bj.player_cheating": [
            _("She'd die if she saw her boyfriend in my mouth..."),

            _("Bet she doesn't suck you off like this..."),

            _("She doesn't get your cock like this... I do..."),

        ],
        "moan.speed2.cowgirl.player_cheating": [
            _("She can't ride you like I can... admit it..."),

            _("I'm on top of her boyfriend and I don't care..."),

            _("I can feel you throbbing inside me..."),

        ],
        "moan.speed3.player_cheating": [
            _("FUCK her! I mean... forget her! You're MINE right now!"),

            _("She could NEVER... oh GOD!"),

            _("You're never going back to her after this!"),

            _("YES! Does she make you feel like THIS?!"),

            _("AHHH! Your girlfriend could NEVER! She doesn't even KNOW!"),

            _("YES! Cheat on her! I'm BETTER! AHHH!"),

            _("FUCK! Does she know what you're DOING?! OH GOD!"),

        ],
        "moan.speed3.hj.player_cheating": [
            _("Cum for ME! Not her! ME!"),

            _("My hand... MINE... she doesn't get this anymore!"),

            _("She can't HANDLE your big dick! I CAN! HARDER!"),

        ],
        "moan.speed3.bj.player_cheating": [
            _("She'll never taste you like I do! MMPH!"),

            _("Give it to me... not her... ME!"),

            _("OH GOD! Every inch! I feel EVERY inch!"),

        ],
        "moan.speed3.cowgirl.player_cheating": [
            _("I'm riding her boyfriend and I'm going to make him CUM!"),

            _("She WISHES she could ride you like this!"),

            _("CHEAT on her HARDER! Give me ALL your cock!"),

        ],

        # --- Threesome: GF approved and is present (watching or participating) ---
        "moan.speed1.threesome": [
            _("She's watching us... this is really happening..."),

            _("I can't believe your girlfriend is okay with this..."),

            _("Knowing she's right there makes this so much more intense..."),

        ],
        "moan.speed1.bj.threesome": [
            _("Sucking you off while she watches... oh god..."),

            _("Does she like watching me do this to you...?"),

        ],
        "moan.speed2.threesome": [
            _("Mmm... she's watching every little thing we do..."),

            _("Your girlfriend is right there... and I love it..."),

            _("This is so hot with her watching..."),

        ],
        "moan.speed2.bj.threesome": [
            _("Is she enjoying the show...? Because I am..."),

            _("Having her watch me suck you... mmm..."),

        ],
        "moan.speed3.threesome": [
            _("OH GOD! She can see EVERYTHING!"),

            _("YES! Right in front of her! Don't stop!"),

            _("This is the craziest thing I've ever done!"),

        ],
        "moan.speed3.bj.threesome": [
            _("MMPH! She's right THERE watching me take it all!"),

            _("Your girlfriend can see every inch! OH GOD!"),

        ],

        # --- Threesome: non-GF walk-in watching (no "your girlfriend" references) ---
        "moan.speed1.threesome_nongf": [
            _("She's watching us... this is really happening..."),

            _("Knowing she's right there makes this so much more intense..."),

        ],
        "moan.speed1.bj.threesome_nongf": [
            _("Sucking you off while she watches... oh god..."),

            _("Does she like watching me do this to you...?"),

        ],
        "moan.speed2.threesome_nongf": [
            _("Mmm... she's watching every little thing we do..."),

            _("This is so hot with her watching..."),

        ],
        "moan.speed2.bj.threesome_nongf": [
            _("Is she enjoying the show...? Because I am..."),

            _("Having her watch me suck you... mmm..."),

        ],
        "moan.speed3.threesome_nongf": [
            _("OH GOD! She can see EVERYTHING!"),

            _("YES! Right in front of her! Don't stop!"),

            _("This is the craziest thing I've ever done!"),

        ],
        "moan.speed3.bj.threesome_nongf": [
            _("MMPH! She's right THERE watching me take it all!"),

            _("She can see every inch going in! OH GOD!"),

        ],

        # --- Player cheating: cum events ---
        "cum_inside.player_cheating": [
            _("You came inside me... your girlfriend has no idea..."),

            _("She doesn't get this from you... but I do..."),

            _("You finished inside someone who isn't your girlfriend... how does that feel?"),

            _("You came inside me... and you have a girlfriend. That's so messed up."),

            _("Another girl's boyfriend just came inside me... I should feel bad. I don't."),

            _("Your girlfriend has no idea you just filled another girl up..."),

        ],
        "cum_outside.player_cheating": [
            _("All that cum... and your girlfriend has no idea it wasn't for her..."),

            _("Does she ever get this much out of you? I doubt it."),

            _("Your thick load wasted on another girl... she has no clue..."),

            _("Your cum on me... your girlfriend would lose it if she saw this."),

            _("Covered in her boyfriend's cum... and she has no clue."),

            _("She thinks your cock is hers... but your cum is all over another girl right now..."),

        ],
        "cum_face.player_cheating": [
            _("Your cum on my face... your girlfriend would scream if she saw this..."),

            _("She has no idea another girl is wearing her boyfriend's cum right now..."),

            _("Her boyfriend's cum dripping off my face... and she thinks you're faithful..."),

            _("Her boyfriend just came on another girl's face... does she even know you're here?"),

            _("Your girlfriend would cry if she saw my face right now..."),

            _("Your thick load all over my face... your girlfriend's man marked someone else..."),

        ],
        "cum_mouth.player_cheating": [
            _("I just swallowed her boyfriend's cum... and I'd do it again."),

            _("She'll never taste you like I just did..."),

            _("Your cum down my throat while your girlfriend waits at home... delicious..."),

            _("I just swallowed her boyfriend's cum. She has no idea."),

            _("Your girlfriend doesn't know another girl just tasted you..."),

            _("Your cum down my throat... she'll kiss you later not knowing where your cock just was..."),

        ],
        "cum_tits.player_cheating": [
            _("All over my tits... your girlfriend is missing out..."),

            _("She doesn't even know these exist... and they're covered in your cum."),

            _("My chest covered in her boyfriend's thick load... she'd lose her mind..."),

            _("All over my tits... your girlfriend has no clue where you just finished."),

            _("Her boyfriend's cum on my chest... she's probably home waiting for you."),

            _("My tits glazed with your cum... your girlfriend has no idea these exist..."),

        ],

        # --- Player cheating: speed/orgasm ---
        "girl_cum.player_cheating": [
            _("I just came because of her boyfriend... oh god..."),

            _("You made me finish... and you have a girlfriend... I don't care..."),

            _("Your girlfriend's man just made ME cum! Oh god!"),

            _("I'm CUMMING! Your girlfriend has NO idea you made ME feel this! AHHHH!"),

            _("CUMMING! You're making another girl cum while she's clueless...!"),

        ],
        "girl_post_cum.player_cheating": [
            _("That was incredible... better than what she gives you?"),

            _("Your girlfriend could never make someone feel like that..."),

            _("Oh god... that was incredible... your cock..."),

            _("That was amazing... your girlfriend is a lucky woman. Or unlucky, depending on perspective."),

            _("Does she make you feel as good as I just did? Be honest."),

            _("That orgasm... your dick... I can't think straight..."),

        ],

        # --- Player cheating + cheater trait ---
        "moan.speed1.player_cheating.cheater": [
            _("Your girlfriend is so naive... and I love it~"),

            _("Cheating on her feels so natural with you..."),

            _("Mmm... your cock fills me up so well..."),

            _("Mmm... we're BOTH cheating right now. Isn't that perfect?"),

            _("Two cheaters together... your girlfriend AND my %(pl)s have no idea..."),

            _("Ahh... we both have someone waiting at home... and here we are..."),

        ],
        "moan.speed2.player_cheating.cheater": [
            _("She'd cry if she knew how good this is... and that turns me on~"),

            _("I love being your dirty secret... your girlfriend has no clue~"),

            _("Behind %(poss)s back and loving every thick inch..."),

            _("Ahh... your girlfriend... my %(pl)s... neither of them knows... oh god..."),

            _("We're both terrible people... ahhh... and it feels AMAZING..."),

        ],
        "moan.speed3.player_cheating.cheater": [
            _("YES! Cheat on her HARDER! Give me EVERYTHING she'll never get!"),

            _("I LOVE that you're hers and you're inside ME right now!"),

            _("CHEAT on her HARDER! Give me ALL your cock!"),

            _("FUCK! We're BOTH cheating! Your girlfriend! My %(pl)s! NEITHER KNOWS! AHHH!"),

            _("TWO relationships we're RUINING! And I don't CARE! OH GOD YES!"),

            _("FUCK my %(pl)s! YOUR cock is the only one that matters!"),

        ],
        "cum_inside.player_cheating.cheater": [
            _("You came inside me behind your girlfriend's back~ This is my favorite thing."),

            _("All that cum that should've been hers... mine now~ She'll never know."),

            _("I feel it leaking... there was so much..."),

            _("You came inside me... your girlfriend AND my %(pl)s would die if they knew."),

            _("Two cheaters... and now your cum is inside me. What a pair we make."),

            _("I can feel your cum filling my pussy... oh god..."),

        ],

        # --- Player cheating + cum_slut ---
        "moan.speed2.player_cheating.cum_slut": [
            _("She doesn't let you go raw, does she? Give it all to me..."),

            _("I want everything your girlfriend won't take..."),

            _("I can feel you throbbing inside me..."),

            _("Ahh... I bet she doesn't swallow for you... I will..."),

            _("Give me everything... things she'd NEVER do for you..."),

            _("Mmm... fuck... you're so thick..."),

        ],
        "moan.speed3.player_cheating.cum_slut": [
            _("CUM INSIDE ME! She doesn't deserve it! I DO!"),

            _("GIVE IT TO ME! Everything your girlfriend is too scared to take!"),

            _("She can't HANDLE your big dick! I CAN! HARDER!"),

            _("GIVE ME EVERYTHING! Your girlfriend doesn't DESERVE your cum! I DO! AHHH!"),

            _("EVERY DROP! She gets NOTHING! I get ALL of it!"),

            _("OH GOD! Every inch! I feel EVERY inch!"),

        ],
        "cum_inside.player_cheating.cum_slut": [
            _("Yes... every drop that should've been your girlfriend's... mine."),

            _("She doesn't swallow, she doesn't take it raw... I take EVERYTHING~"),

            _("You came so deep... I can feel it all..."),

            _("Yes... every drop inside me. Does she even let you do this?"),

            _("All of it inside me... I bet your girlfriend never lets you finish here."),

            _("Your girlfriend gets the polite version. I get the raw, full load."),

        ],

        # --- Player cheating + cute_sex ---
        "moan.speed1.player_cheating.cute": [
            _("I feel bad for your girlfriend... but not enough to stop..."),

            _("This is wrong... but it feels so right with you..."),

            _("I can feel every inch stretching me..."),

            _("Mm... but you have a girlfriend... should we really be doing this...?"),

            _("Ahh... I feel bad for her... but you feel so good..."),

            _("Your girlfriend... she doesn't deserve this... but I can't stop..."),

        ],
        "moan.speed2.player_cheating.cute": [
            _("I keep thinking about her... but then you touch me and I forget..."),

            _("She deserves better... but I want you too much to care..."),

            _("Oh god... you're so deep... it's so intense..."),

            _("Oh god... I keep thinking about your girlfriend... ahh... I'm sorry..."),

            _("This is wrong... you belong to someone else... but it feels so nice..."),

        ],
        "cum_inside.player_cheating.cute": [
            _("You finished inside me... I feel terrible about your girlfriend... but also happy..."),

            _("That felt so intimate... like you chose me over her, just for a moment..."),

            _("You just came inside me... and you have a GIRLFRIEND... her boyfriend's cum in another girl..."),

            _("You came inside me... but you have a girlfriend... *tears up* I'm so sorry..."),

            _("Your girlfriend's boyfriend just... inside me... I feel awful..."),

            _("Oh no... your cum is inside me... you promised you'd pull out..."),

        ],

        # --- Player cheating + hardcore ---
        "moan.speed2.player_cheating.hardcore": [
            _("Your girlfriend can't handle you like I can... go harder..."),

            _("She's too soft for you. I'm not. Give me everything."),

            _("Your cock is driving me crazy..."),

            _("Ahh... HARDER! Your girlfriend could NEVER handle this!"),

            _("Fuck me like you'd NEVER fuck her! SHOW ME!"),

            _("Yes... harder... your dick feels incredible..."),

        ],
        "moan.speed3.player_cheating.hardcore": [
            _("BREAK me the way you can't break her! HARDER!"),

            _("She could NEVER take what I'm taking right now!"),

            _("OH FUCK! Your cock is splitting me open!"),

            _("FUCK HER FEELINGS! I'M the one making you feel THIS! AHHH!"),

            _("YOUR GIRLFRIEND IS NOTHING! DESTROY ME! HARDER!"),

            _("YES! Right there! Your dick is so DEEP!"),

        ],

        # ══════════════════════════════════════════════════════════
        #  BOTH CHEATING — she has BF AND player has GF
        # ══════════════════════════════════════════════════════════

        "moan.speed1.both_cheating": [
            _("We're both terrible people... but this feels too good..."),

            _("My %(pl)s... your girlfriend... they'd both die..."),

            _("Two relationships on the line... and I don't care..."),

        ],
        "moan.speed1.cowgirl.both_cheating": [
            _("I'm riding you while we both have someone... what's wrong with us..."),

            _("My %(pl)s would lose %(poss)s mind if %(pp)s saw me on top of you like this..."),

            _("Your girlfriend... my %(pl)s... they'd both lose it if they saw your cock in me..."),

        ],
        "moan.speed2.both_cheating": [
            _("Your girlfriend and my %(pl)s can cry together..."),

            _("We're cheating on two people at once... and it's the best sex I've ever had..."),

            _("%(Pp)s could never... she could never... but WE can..."),

        ],
        "moan.speed2.cowgirl.both_cheating": [
            _("I should be riding my %(pl)s... but I'm on top of YOU..."),

            _("Does your girlfriend ride you like this? Because my %(pl)s doesn't get this either."),

            _("Your girlfriend can't ride your dick like I do... %(poss)s body can't fill me like yours..."),

        ],
        "moan.speed3.both_cheating": [
            _("FUCK THEM BOTH! You're MINE and I'm YOURS!"),

            _("My %(pl)s! Your girlfriend! Who CARES! Don't STOP!"),

            _("We're RUINING two relationships and it feels INCREDIBLE!"),

        ],

        "cum_inside.both_cheating": [
            _("You came inside me... my %(pl)s's partner... your girlfriend's enemy..."),

            _("%(Pp)s never does this... she never gets this... and now it's inside me..."),

            _("Two cheaters, one creampie... my %(pl)s and your girlfriend would be destroyed."),

        ],
        "cum_outside.both_cheating": [
            _("All that cum... neither of them will ever know what we just did..."),

            _("Look at this mess... two relationships ruined and it's all over me..."),

            _("Your cum on me while my %(pl)s and your girlfriend are clueless... we're monsters..."),

        ],
        "girl_cum.both_cheating": [
            _("I just came cheating on my %(pl)s with someone else's boyfriend..."),

            _("My %(pl)s never makes me cum like this... and your girlfriend can't either..."),

            _("Your girlfriend... my %(pl)s... and I just came harder than either of them could make me!"),

        ],

        # --- Both cheating + cheater trait ---
        "moan.speed1.both_cheating.cheater": [
            _("Two cheaters together... this was inevitable~"),

            _("My %(pl)s... your girlfriend... they picked the wrong people to trust~"),

            _("Nice and deep... I love it..."),

        ],
        "moan.speed2.both_cheating.cheater": [
            _("We're a match made in hell~ Neither of them had a chance."),

            _("This is what happens when two cheaters find each other... magic~"),

            _("Every thrust goes deeper... don't stop..."),

        ],
        "moan.speed3.both_cheating.cheater": [
            _("DESTROY me! My %(pl)s can't! Your girlfriend won't! WE'RE PERFECT TOGETHER!"),

            _("FOUR people in this mess and I only care about ONE! You! HARDER!"),

            _("FUCK my %(pl)s! YOUR cock is the only one that matters!"),

        ],
        "cum_inside.both_cheating.cheater": [
            _("Fill me up while we betray two people at once~ I love this."),

            _("My %(pl)s's cum never felt like this... your girlfriend's loss is my gain~"),

            _("Your cum inside me... we're both cheating AND you came raw... we're doomed..."),

        ],

        # --- Both cheating + cum_slut ---
        "moan.speed2.both_cheating.cum_slut": [
            _("My %(pl)s never gives me this much... your girlfriend doesn't know what she has..."),

            _("Give me everything they won't take... I want ALL of you..."),

            _("Your thick cock... give it all to me..."),

        ],
        "cum_inside.both_cheating.cum_slut": [
            _("My %(pl)s uses condoms... your girlfriend doesn't swallow... and I get it ALL raw~"),

            _("Every drop that should've been for her... inside me instead. My %(pl)s gets nothing."),

            _("I feel it leaking... there was so much..."),

        ],

        # --- Both cheating + cute_sex ---
        "moan.speed1.both_cheating.cute": [
            _("I feel awful about both of them... but I can't stop wanting you..."),

            _("Two hearts we're breaking... and I still want this..."),

            _("Two relationships and neither matters when your dick is this deep..."),

        ],
        "moan.speed2.both_cheating.cute": [
            _("It's so wrong... but when you touch me, my %(pl)s doesn't exist..."),

            _("She doesn't deserve this from you... %(pp)s doesn't deserve this from me... but I need you..."),

            _("You feel amazing... every thrust..."),

        ],

        # --- Both Cheating + Public (neutral — both have partners, in public) ---
        "moan.speed1.both_cheating.public": [
            _("Mm... both of us have someone... and we're doing this where anyone could see..."),

            _("Ahh... two cheaters in public... someone could tell both of them..."),

            _("Nice and deep... I love it..."),

        ],
        "moan.speed2.both_cheating.public": [
            _("Ahh... anyone could walk by... your girlfriend... my %(pl)s... oh god..."),

            _("Oh god... imagine if both of them found out at once... from a stranger who saw us here..."),

            _("Yes... harder... your dick feels incredible..."),

        ],
        "moan.speed3.both_cheating.public": [
            _("FUCK IT! LET THEM BOTH FIND OUT! I DON'T CARE ANYMORE! AHHH!"),

            _("AHH! YOUR GIRLFRIEND! MY %(pl)s! THEY CAN BOTH WATCH FOR ALL I CARE!"),

            _("OH GOD! Every inch! I feel EVERY inch!"),

        ],
        "girl_cum.both_cheating.public": [
            _("CUMMING! Two cheaters in PUBLIC! Our partners could be RIGHT THERE! AAAH!"),

            _("OH GOD! I'm cumming... in public... betraying my %(pl)s AND yours is betraying her...!"),

            _("OH GOD! I'm cumming! Don't stop!"),

        ],
        "cum_inside.both_cheating.public": [
            _("You came inside me... in public... while both of us are with someone else..."),

            _("Creampied in public... by someone else's boyfriend... while mine has no idea..."),

            _("Two cheaters and a creampie... we're the worst people alive..."),

        ],
        "cum_outside.both_cheating.public": [
            _("The evidence of two cheaters... right here in public for anyone to find..."),

            _("At least it's not inside... but anyone could see what we just did to our partners..."),

            _("Your cum in the open... two cheaters with evidence right where someone could spot it..."),

        ],
        "dressup.both_cheating.public": [
            _("We need to get out of here... separately... if anyone tells either of them..."),

            _("Two cheaters getting dressed in public... I hope nobody we know was around..."),

            _("Eyes up here... or maybe not~"),

        ],

        # --- Both Cheating + Public Shy (she's terrified both partners find out) ---
        "moan.speed1.both_cheating.public_shy": [
            _("Mm... what if someone tells BOTH of them... I'm so scared..."),

            _("Ahh... two cheaters in public... double the chance someone recognizes us..."),

            _("Your girlfriend... my %(pl)s... they'd both lose it if they saw your cock in me..."),

        ],
        "moan.speed2.both_cheating.public_shy": [
            _("Oh god... what if %(poss)s friends see... or HER friends see... anyone could..."),

            _("Ahh... I'm terrified... both our partners could find out from a STRANGER..."),

            _("Two cheaters, one thick cock... and neither of us cares..."),

        ],
        "moan.speed3.both_cheating.public_shy": [
            _("AHH! I CAN'T STOP! But what if BOTH of them find out?! OH GOD!"),

            _("PLEASE NOT SO LOUD! My %(pl)s... your girlfriend... anyone could HEAR us!"),

            _("I can't take it! You're too big! Don't STOP!"),

        ],
        "cum_inside.both_cheating.public_shy": [
            _("Inside me?! IN PUBLIC?! If someone tells my %(pl)s AND your girlfriend...!"),

            _("Oh god... both of our partners... and there's evidence... in public..."),

            _("Your girlfriend. My %(pl)s. Both betrayed by your cum in my pussy."),

        ],
        "dressup.both_cheating.public_shy": [
            _("We need to leave separately... different directions... oh god I'm shaking..."),

            _("If anyone recognized either of us... both our relationships are over..."),

            _("Like what you see? Your cock is already responding..."),

        ],

        # --- Both Cheating + Public Fetish (she loves the double-risk thrill) ---
        "moan.speed1.both_cheating.public_fetish": [
            _("Mm... two people who'd be destroyed if they saw us... out in the open... delicious..."),

            _("Ahh... anyone could tell both of our partners... the risk is intoxicating..."),

            _("Don't stop... just like that..."),

        ],
        "moan.speed2.both_cheating.public_fetish": [
            _("Ahh... imagine both of them finding out from someone who SAW us... oh god..."),

            _("Two cheaters... in public... someone should take a photo and send it to BOTH of them..."),

            _("Don't stop... your cock hits every spot..."),

        ],
        "moan.speed3.both_cheating.public_fetish": [
            _("YES! LET THE WHOLE WORLD SEE! TWO CHEATERS FUCKING IN PUBLIC! AHHHH!"),

            _("I WANT %(poss)s FRIENDS AND HER FRIENDS TO ALL SEE THIS! AAAH! MORE!"),

            _("FUCK! Your thick cock is destroying me!"),

        ],
        "cum_inside.both_cheating.public_fetish": [
            _("Creampied in public by another girl's boyfriend... while mine is clueless... perfection..."),

            _("Your cum inside me... in public... both our partners betrayed at once... incredible..."),

            _("My pussy is full of your cum... I can't believe I let you..."),

        ],
        "dressup.both_cheating.public_fetish": [
            _("I hope someone got a good look... two cheaters caught in the act would be legendary..."),

            _("Getting dressed after the ultimate double betrayal... in PUBLIC... what a rush..."),

            _("Take a good look before your cock takes over..."),

        ],

        # --- Both Cheating + Public: act-specific ---
        "creampie_req.both_cheating.public": [
            _("Cum inside me in public... two cheaters leaving evidence for the world to see..."),

            _("Fill me up out here... your girlfriend and my %(pl)s can both deal with it..."),

            _("Public creampie between two cheaters... if anyone tells either of our partners..."),

        ],
        "record_accepted.both_cheating.public": [
            _("Film two cheaters in public... send it to both our partners..."),

            _("Record it... public proof we're both terrible people... do it..."),

            _("Recording in public... this is so risky but go ahead..."),

            _("A video of two cheaters... in public... if either of them finds this..."),

        ],

        # --- Both Cheating + Public Shy: act-specific ---
        "creampie_req.both_cheating.public_shy": [
            _("I-inside?! In public?! Both our partners could find out from the EVIDENCE...!"),

            _("N-not here... if someone sees and tells my %(pl)s AND your girlfriend...!"),

            _("Cum inside me... please... fill my pussy with your cum..."),

        ],

        # --- Both Cheating + Public Fetish: act-specific ---
        "creampie_req.both_cheating.public_fetish": [
            _("Fill me up in public... two cheaters... let the evidence speak for itself..."),

            _("Cum inside me where everyone can see... your girlfriend AND my %(pl)s can find out..."),

            _("Public creampie from a fellow cheater... someone PLEASE tell our partners..."),

        ],
        "record_accepted.both_cheating.public_fetish": [
            _("Film it! Two cheaters in public! Send it to BOTH of them!"),

            _("Yes! Record the double betrayal in public! Let them watch!"),

            _("Record us... proof that your girlfriend and my %(pl)s are both fools..."),

            _("Film it! Two cheaters in public! Send it to BOTH our partners!"),

            _("Film two cheaters making a public sex tape... BOTH our partners should see this..."),

        ],

        # --- In Love: she loves her BF, feels very guilty ---
        "girl_post_cum.bf_in_love": [
            _("I need to go home... to him... pretend this never happened..."),

            _("He's going to ask how my day was and I'll have to lie..."),

            _("I love my boyfriend and another man's cum is inside me... I'm a monster..."),

        ],

        # --- BF loyalty + trait combos ---

        # In love + cum_slut (intense internal conflict)
        "moan.speed2.bf_in_love.cum_slut": [
            _("I love my boyfriend... but I NEED this... he can't give me enough..."),

            _("He's so sweet... but my body craves things he won't do..."),

            _("I love him so much... and your cock is inside me... I'm the worst..."),

        ],
        "cum_inside.bf_in_love.cum_slut": [
            _("He always uses protection because I asked... but with you I want it RAW... I'm terrible..."),

            _("My boyfriend treats me like a queen... and I just begged another man to cum inside me..."),

            _("I can feel your cum filling my pussy... oh god..."),

        ],

        # In love + cute_sex (emotional guilt)
        "moan.speed1.bf_in_love.cute": [
            _("He held my hand this morning... and now I'm here... what kind of person am I..."),

            _("This feels so tender... like what I have with him... that makes it worse..."),

            _("Don't stop... just like that..."),

        ],

        # Miserable + cheater (zero guilt, maximum contempt)
        "moan.speed2.bf_miserable.cheater": [
            _("My boyfriend is a waste of space. You're so much better in every way~"),

            _("I should send him a photo of this~ Let him see what he's missing~"),

            _("His dick could never make me moan like this..."),

        ],
        "moan.speed3.bf_miserable.cheater": [
            _("I HATE HIM and I LOVE THIS! Fuck me like he NEVER could!"),

            _("My boyfriend can cry about it! I'm with someone BETTER now!"),

            _("I don't CARE about him! Your cock OWNS me!"),

        ],

        # Strained + hardcore (channeling frustration)
        "moan.speed2.bf_strained.hardcore": [
            _("He stopped being rough with me... you don't hold back... more..."),

            _("My boyfriend got lazy in bed. Show me what effort looks like."),

            _("Don't stop... your cock hits every spot..."),

        ],
        "moan.speed3.bf_strained.hardcore": [
            _("THIS is what I've been missing! He forgot how to FUCK me!"),

            _("HARDER! He hasn't made me scream in MONTHS!"),

            _("Things are falling apart with him... your cock is my only comfort..."),

        ],

        # Miserable + cum_slut (degrading BF openly)
        "moan.speed2.bf_miserable.cum_slut": [
            _("My boyfriend's cock is boring... yours is everything I need..."),

            _("He never cums enough for me... you always deliver..."),

            _("Mmm... fuck... you're so thick..."),

        ],
        "cum_inside.bf_miserable.cum_slut": [
            _("He uses condoms because I told him to. With you? I want every drop inside me. He's nothing."),

            _("My boyfriend's cum is wasted on me. Yours? I'd drain you dry every day."),

            _("You came so deep... I can feel it all..."),

        ],

        # ══════════════════════════════════════════════════════════
        #  VETERAN ACT — she's done this specific act 5+ times
        # ══════════════════════════════════════════════════════════

        "moan.speed1.act_veteran": [
            _("Mmm... I know exactly what you like by now..."),

            _("We've done this so many times... and it never gets old..."),

            _("I remember the first time we did this... I've gotten better~"),

        ],
        "moan.speed2.act_veteran": [
            _("You know my body so well by now..."),

            _("Every time gets better... you know exactly where to go..."),

            _("I've lost count of how many times we've done this... don't stop..."),

        ],
        "moan.speed1.hj.act_veteran": [
            _("I know exactly how to grip you now... right here..."),

            _("I've memorized every twitch by now~"),

            _("I can feel every vein, every throb... I know your cock by heart~"),

        ],
        "moan.speed1.bj.act_veteran": [
            _("I know exactly what you like with my mouth now..."),

            _("I remember the first time... I'm so much better at this now~"),

            _("My mouth knows your dick better than my own name..."),

        ],
        "moan.speed1.cowgirl.act_veteran": [
            _("I know the exact rhythm you love by now..."),

            _("I've perfected my technique on top of you~"),

            _("I ride your cock on autopilot now... perfect rhythm every time~"),

        ],
        "moan.speed2.hj.act_veteran": [
            _("I can make you finish whenever I want now... but I'll take my time~"),

            _("My hand knows your cock better than you do at this point..."),

            _("My hand is soaked... your dick is dripping..."),

        ],
        "moan.speed2.bj.act_veteran": [
            _("I know exactly when to go deep and when to tease..."),

            _("Your cock fits my mouth perfectly... we've practiced enough~"),

            _("My mouth knows your dick better than my own name..."),

        ],
        "moan.speed2.cowgirl.act_veteran": [
            _("I know the angle that makes you crazy by now..."),

            _("Every time I ride you it gets better..."),

            _("Don't stop... your cock hits every spot..."),

        ],

        # Veteran + boyfriend (comfortable cheating)
        "moan.speed1.act_veteran.boyfriend": [
            _("We've done this so many times behind his back... it's just normal now..."),

            _("My boyfriend has no idea how practiced we are at this..."),

            _("Don't stop... just like that..."),

        ],
        "moan.speed1.act_veteran.girlfriend": [
            _("We've done this so many times behind her back... me and a man... it's just normal now..."),

            _("My girlfriend has no idea how many times I've been with you..."),

            _("Don't stop... she could never do this..."),

        ],
        "moan.speed2.act_veteran.boyfriend": [
            _("I've cheated so many times with this act... I've stopped counting..."),

            _("He still trusts me... even after I've done this with you countless times..."),

            _("If he saw what your big dick does to me..."),

        ],
        "moan.speed2.act_veteran.girlfriend": [
            _("I've secretly been with you so many times... I've stopped pretending..."),

            _("She still trusts me... even after I've taken your cock countless times..."),

            _("If she saw what your big dick does to her girlfriend..."),

        ],

        # Veteran + player_cheating (normalized)
        "moan.speed1.act_veteran.player_cheating": [
            _("We've done this behind her back so many times... does it even count as cheating anymore?"),

            _("Your girlfriend is never finding out... we're too good at this by now..."),

            _("Mmm... I love how big you are..."),

        ],
        "moan.speed2.act_veteran.player_cheating": [
            _("She still doesn't know... after all these times? You're a better liar than I thought..."),

            _("Every time we do this, I care less about your girlfriend..."),

            _("I can feel you throbbing inside me..."),

        ],

        # =============================================================
        # BF LOYALTY TIERS — scene moans (cheating on her BF)
        # bf_in_love = guilty, bf_strained = fading guilt, bf_miserable = no guilt
        # Generic fallback + act-specific (hj, bj, tj, cowgirl, RCG)
        # =============================================================

        # ---- bf_in_love: she loves her BF, massive guilt ----
        # generic fallback
        "moan.speed1.bf_in_love": [
            _("My boyfriend... I keep telling myself this is the last time..."),

            _("I shouldn't be moaning for you... I have a boyfriend..."),

            _("Your thick cock feels so good..."),

            _("Oh god... I love him... why am I doing this..."),

            _("My boyfriend is so good to me... and I'm here with you..."),

            _("He trusts me completely... I'm a terrible person..."),

        ],
        "moan.speed2.bf_in_love": [
            _("I promised myself I wouldn't do this again... ahhh... but here I am..."),

            _("My boyfriend trusts me... god, why does this feel so good..."),

            _("I can feel you throbbing inside me..."),

            _("I love my boyfriend so much... but your body feels so good..."),

            _("He's perfect... so why do I keep coming back to you..."),

            _("This is the worst thing I've ever done to someone I love..."),

        ],
        "moan.speed3.bf_in_love": [
            _("I'm sorry... I'm sorry... oh GOD don't stop!"),

            _("My boyfriend... fuck... I can't think about him right now!"),

            _("My boyfriend deserves better... but your dick feels too good..."),

            _("I LOVE HIM! I love him and I can't STOP! Oh GOD!"),

            _("He's the best boyfriend ever and I'm a MONSTER! Don't stop!"),

            _("I'm going to HATE myself for this! But YES! DON'T STOP!"),

        ],
        "cum_inside.bf_in_love": [
            _("You came inside me again... my boyfriend can never know how many times..."),

            _("Every time you finish inside me I promise it's the last... and it never is..."),

            _("He's perfect and I let your cock fill me with cum... I hate myself..."),

            _("Oh god... he always pulls out for me... and you just... inside... I'm horrible..."),

            _("My boyfriend is so careful... so loving... and I just let another man cum in me..."),

            _("He would be so devastated... he loves me so much... what have I done..."),

        ],
        "girl_cum.bf_in_love": [
            _("I came... again... cheating on my boyfriend... again..."),

            _("My boyfriend never makes me cum like this... that's why I keep coming back..."),

            _("I can't... I'm... CUMMING! Your cock!"),

            _("He makes me cum too... but not like THIS... oh god, I'm awful..."),

            _("My boyfriend does everything right... so why did YOU just make me cum harder..."),

            _("AAAH! I'm cumming so hard on your dick!"),

        ],
        # hj
        "moan.speed1.hj.bf_in_love": [
            _("I shouldn't be stroking you like this... my boyfriend trusts me..."),

            _("My hand around you... if he ever finds out I touched someone else..."),

            _("I love how hard you get for me..."),

        ],
        "moan.speed3.hj.bf_in_love": [
            _("I can't stop... my boyfriend... forgive me... it feels too good in my hand!"),

            _("Faster... oh god... my boyfriend would die if he saw my hand on you!"),

            _("HARDER! Your dick drives me INSANE!"),

        ],
        # bj
        "moan.speed1.bj.bf_in_love": [
            _("My lips around you... my boyfriend has no idea I do this..."),

            _("I shouldn't be tasting you... I have a boyfriend who loves me..."),

            _("My boyfriend deserves better... but your dick feels too good..."),

        ],
        "moan.speed3.bj.bf_in_love": [
            _("Deeper... oh god... my boyfriend would be CRUSHED if he saw my mouth on you!"),

            _("I can't stop sucking... my boyfriend... I'm so sorry..."),

            _("I love him so much... and your cock is inside me... I'm the worst..."),

        ],
        # tj
        "moan.speed1.tj.bf_in_love": [
            _("My boyfriend loves my chest... and here I am using it on you..."),

            _("Between my tits... if my boyfriend knew I did this for someone else..."),

            _("I love him so much... and your cock is inside me... I'm the worst..."),

        ],
        "moan.speed3.tj.bf_in_love": [
            _("Harder between them! My boyfriend... he can never know I use my body like this!"),

            _("My tits around you... oh god... my boyfriend would never forgive me..."),

            _("I love him so much... and your cock is inside me... I'm the worst..."),

        ],
        # cowgirl
        "moan.speed1.cowgirl.bf_in_love": [
            _("Riding you slowly... my boyfriend has no idea another guy is inside me..."),

            _("I feel you so deep... my boyfriend would be destroyed if he knew..."),

            _("My boyfriend deserves better... but your dick feels too good..."),

        ],
        "moan.speed3.cowgirl.bf_in_love": [
            _("I can't stop bouncing! My boyfriend... I'm so sorry... you feel too GOOD!"),

            _("HARDER! Oh god my boyfriend... I'm riding someone else and I LOVE it!"),

            _("My boyfriend deserves better... but your dick feels too good..."),

        ],
        "cum_inside.cowgirl.bf_in_love": [
            _("You came inside me... while I was on top... my boyfriend can never know..."),

            _("I felt you fill me up... my boyfriend thinks I'm only his... I'm so sorry..."),

            _("You came so deep... I can feel it all..."),

        ],
        # RCG

        # ---- bf_strained: relationship bad, guilt fading ----
        # generic fallback
        "moan.speed1.bf_strained": [
            _("Mmm... my boyfriend has no idea I do this regularly now..."),

            _("I've stopped counting how many times we've done this behind his back..."),

            _("Don't stop... just like that..."),

            _("I haven't felt this good in a long time... my boyfriend stopped trying..."),

            _("He doesn't touch me like this anymore..."),

            _("This is what I've been missing..."),

        ],
        "moan.speed2.bf_strained": [
            _("This used to make me feel guilty... now it just makes me feel good..."),

            _("My boyfriend... honestly? I barely think about him when we're together..."),

            _("He's neglecting me... your dick never does..."),

            _("We barely have sex anymore... but with you it's different..."),

            _("He doesn't make me wet like this... not anymore..."),

            _("My boyfriend gave up on pleasing me... you didn't..."),

        ],
        "moan.speed3.bf_strained": [
            _("HARDER! My boyfriend could NEVER! I don't even care anymore!"),

            _("YES! I used to feel bad about this! Not anymore! MORE!"),

            _("I can't take it! You're too big! Don't STOP!"),

            _("YES! He NEVER does this to me! Thank GOD for you!"),

            _("This is what I NEED! My boyfriend forgot how!"),

            _("HARDER! Your dick drives me INSANE!"),

        ],
        "cum_inside.bf_strained": [
            _("Fill me up... my boyfriend doesn't even know this happens regularly now..."),

            _("Another creampie behind his back... it barely registers as cheating anymore..."),

            _("He stopped trying in bed... your cock just did more than he has in months..."),

            _("He always uses a condom now... we lost the passion. But you... you just went for it."),

            _("My boyfriend would never do this anymore. You did it without hesitation."),

            _("I feel it leaking... there was so much..."),

        ],
        "girl_cum.bf_strained": [
            _("I cum harder with you than I ever did with him... that says everything..."),

            _("My boyfriend thinks I'm faithful... and I just came screaming for someone else..."),

            _("Yes yes YES! I'm cumming on your thick dick!"),

            _("I haven't cum like this in so long... he stopped trying..."),

            _("My boyfriend couldn't make me feel this even when things were good..."),

        ],
        # hj
        "moan.speed1.hj.bf_strained": [
            _("Stroking you is second nature now... my boyfriend is an afterthought..."),

            _("My boyfriend never gets this treatment anymore... you do..."),

            _("You're so hard in my hand... mmm..."),

        ],
        "moan.speed3.hj.bf_strained": [
            _("FASTER! My boyfriend's dick doesn't even compare to yours in my hand!"),

            _("I jerk you off better than I ever did for him! He lost me!"),

            _("FUCK! Your thick cock is destroying me!"),

        ],
        # bj
        "moan.speed1.bj.bf_strained": [
            _("My boyfriend hasn't gotten head in weeks... you get it whenever you want..."),

            _("Sucking you off while my boyfriend thinks I'm loyal... barely feels wrong..."),

            _("Mmm... I love your cock in my mouth..."),

        ],
        "moan.speed3.bj.bf_strained": [
            _("Deeper! My boyfriend NEVER got me this eager on my knees!"),

            _("I suck you like I mean it... my boyfriend got the bare minimum!"),

            _("My boyfriend forgot how to satisfy me... your cock reminds me what I'm missing..."),

        ],
        # tj
        "moan.speed1.tj.bf_strained": [
            _("My tits around you... my boyfriend forgot these even existed..."),

            _("He never appreciated my body... you do..."),

            _("Your thick cock feels so good..."),

        ],
        "moan.speed3.tj.bf_strained": [
            _("Squeeze them HARDER! My boyfriend never made me want to use them like this!"),

            _("Between my tits where you belong! Not my boyfriend... YOU!"),

            _("He's neglecting me... your dick never does..."),

        ],
        # cowgirl
        "moan.speed1.cowgirl.bf_strained": [
            _("Riding you slowly... my boyfriend barely lasts two minutes..."),

            _("You feel so much better than him inside me... it's not even close..."),

            _("Mmm... your cock fills me up so well..."),

        ],
        "moan.speed3.cowgirl.bf_strained": [
            _("I'm BOUNCING on you and my boyfriend has NO clue! I don't even CARE!"),

            _("HARDER! My boyfriend could never last this long with me on top!"),

            _("OH GOD! Every inch! I feel EVERY inch!"),

        ],
        "cum_inside.cowgirl.bf_strained": [
            _("Another load inside me that isn't his... whatever. Feels better anyway."),

            _("You fill me up and my boyfriend has no idea... story of my life now..."),

            _("So warm inside me... every drop... fuck..."),

        ],
        # RCG

        # ---- bf_miserable: she hates her BF, zero guilt ----
        # generic fallback
        "moan.speed1.bf_miserable": [
            _("Mmm... my boyfriend is probably texting me right now... whatever..."),

            _("This is just how my life works now... boyfriend at home, you in bed..."),

            _("I can feel every inch stretching me..."),

            _("This already feels better than anything with my boyfriend..."),

            _("My boyfriend is so boring compared to you..."),

            _("I don't even miss him right now..."),

        ],
        "moan.speed2.bf_miserable": [
            _("My boyfriend is so clueless... I could do this every day and he'd never know..."),

            _("He thinks I'm loyal... that's the funniest thing I've heard all week..."),

            _("Your cock is driving me crazy..."),

            _("He NEVER makes me feel like this... EVER..."),

            _("My boyfriend is pathetic compared to you... don't stop..."),

            _("I should've left him months ago... you're so much better..."),

        ],
        "moan.speed3.bf_miserable": [
            _("FUCK my boyfriend! You're the one I want! HARDER!"),

            _("He could NEVER do this to me! I don't even remember why I'm with him!"),

            _("His pathetic dick has nothing on yours... keep going..."),

            _("He could NEVER! He's NOTHING compared to you!"),

            _("I'm going to LEAVE him! You're all I want!"),

            _("My boyfriend can ROT! You're the one I need!"),

        ],
        "cum_inside.bf_miserable": [
            _("Fill me up... my boyfriend has no idea this is a weekly thing..."),

            _("Another load inside me that isn't his... whatever. It feels better anyway."),

            _("His cock could never produce a load like that... pathetic..."),

            _("He never does this... and I never wanted him to. But YOU... yes."),

            _("My boyfriend wouldn't dare. You just did it like it's nothing. I love it."),

            _("He's so careful and boring... you just cum inside me like you own me. Yes."),

        ],
        "girl_cum.bf_miserable": [
            _("I cum so easily with you... my boyfriend is basically my roommate at this point..."),

            _("Another orgasm he'll never know about. Story of my life."),

            _("I can't... I'm... CUMMING! Your cock!"),

            _("My boyfriend hasn't made me cum in months... you did it in minutes..."),

            _("He could NEVER... oh god... I'm done with him after this..."),

            _("Yes yes YES! I'm cumming on your thick dick!"),

        ],
        # hj
        "moan.speed1.hj.bf_miserable": [
            _("Stroking a real dick... my boyfriend is pathetic compared to this..."),

            _("My boyfriend wishes I'd touch him like this... I won't..."),

            _("Your dick twitches when I stroke right here..."),

        ],
        "moan.speed3.hj.bf_miserable": [
            _("HARDER in my hand! My boyfriend can't even GET this hard! Useless!"),

            _("I'm jerking you like I HATE my boyfriend! Because I DO!"),

            _("OH GOD! Every inch! I feel EVERY inch!"),

        ],
        # bj
        "moan.speed1.bj.bf_miserable": [
            _("I suck you off like you deserve... my boyfriend gets nothing..."),

            _("My mouth on a real man's cock... my boyfriend is a joke..."),

            _("I can feel every inch stretching me..."),

        ],
        "moan.speed3.bj.bf_miserable": [
            _("I would NEVER suck my boyfriend like this! You're WORTH it! He's NOT!"),

            _("Deeper! My boyfriend couldn't DREAM of me being this eager!"),

            _("I can feel you pulsing in my mouth! DO IT!"),

        ],
        # tj
        "moan.speed1.tj.bf_miserable": [
            _("My boyfriend doesn't get to touch these anymore... only you..."),

            _("Between my tits where a real man belongs... not that loser..."),

            _("Mmm... squeeze them tighter around your dick?"),

        ],
        "moan.speed3.tj.bf_miserable": [
            _("Fuck my tits HARDER! My boyfriend NEVER deserved these!"),

            _("My chest is YOURS! My boyfriend can go fuck himself!"),

            _("His pathetic dick has nothing on yours... keep going..."),

        ],
        # cowgirl
        "moan.speed1.cowgirl.bf_miserable": [
            _("Riding a man who can actually last... my boyfriend breaks in two minutes..."),

            _("My boyfriend could never fill me like this... pathetic..."),

            _("Nice and deep... I love it..."),

        ],
        "moan.speed3.cowgirl.bf_miserable": [
            _("I'm RIDING you like I WISH I could leave my boyfriend! HARDER!"),

            _("My boyfriend is NOTHING! You're the one I want INSIDE me! FASTER!"),

            _("YES! Right there! Your dick is so DEEP!"),

        ],
        "cum_inside.cowgirl.bf_miserable": [
            _("Fill me up! My boyfriend's cum is worthless compared to yours!"),

            _("I want YOUR cum inside me. Not his. Never his again."),

            _("His cock could never produce a load like that... pathetic..."),

        ],
        # RCG

        # =============================================================
        # GF-LIKE TIERS — scene moans (helping player cheat on his GF)
        # gf_close = likes the GF (guilty), gf_distant = meh, gf_hostile = hates her
        # Generic fallback + act-specific (hj, bj, tj, cowgirl, RCG)
        # =============================================================

        # ---- gf_close: she likes the player's GF, feels terrible ----
        # generic fallback
        "moan.speed1.gf_close": [
            _("Your girlfriend... she doesn't know about us, does she..."),

            _("I feel bad for her... but not bad enough to stop..."),

            _("Mmm... your cock fills me up so well..."),

        ],
        "moan.speed2.gf_close": [
            _("She trusts you... and here you are with me... I should feel worse..."),

            _("I keep telling myself this is wrong... but I keep saying yes..."),

            _("Yes... harder... your dick feels incredible..."),

        ],
        "moan.speed3.gf_close": [
            _("Forget her! Just... don't stop! I'll feel guilty LATER!"),

            _("Your girlfriend... I'm sorry... but GOD you feel too good!"),

            _("HARDER! Your dick drives me INSANE!"),

        ],
        # hj
        "moan.speed1.hj.gf_close": [
            _("Stroking her boyfriend... I'm a terrible person..."),

            _("My hand on you... she trusts both of us and here I am..."),

            _("You're so hard in my hand... she has no idea..."),

        ],
        "moan.speed3.hj.gf_close": [
            _("I can't stop stroking! She'd NEVER forgive me if she saw this!"),

            _("Faster! Oh god... she doesn't deserve this betrayal...!"),

            _("My grip is INSANE right now! She'd CRY if she could see this!"),

        ],
        # bj
        "moan.speed1.bj.gf_close": [
            _("My mouth on her boyfriend... if she could see me right now..."),

            _("Sucking you off behind her back... I feel sick... but I won't stop..."),

            _("Mmm... you taste so good... she'd be crushed..."),

        ],
        "moan.speed3.bj.gf_close": [
            _("Deeper! She... oh god she'd CRY if she saw me sucking you like this!"),

            _("I'm on my knees for her boyfriend and I CAN'T stop!"),

            _("Her boyfriend's cock in my throat and I LOVE it! She'd DIE!"),

        ],
        # tj
        "moan.speed1.tj.gf_close": [
            _("Her boyfriend between my tits... this is the worst thing I've ever done..."),

            _("She doesn't know I use my body on you like this..."),

            _("Mmm... I love how big you are..."),

        ],
        "moan.speed3.tj.gf_close": [
            _("Harder between them! She'd HATE me! But I can't STOP!"),

            _("My tits on her boyfriend... oh god... I'm so sorry... DON'T STOP!"),

            _("It's so HOT between my tits... she trusts me and I'm doing THIS!"),

        ],
        # cowgirl
        "moan.speed1.cowgirl.gf_close": [
            _("Riding her boyfriend slowly... she'd never forgive me..."),

            _("You're inside me and she doesn't know... I'm the worst..."),

            _("I can feel every inch stretching me..."),

        ],
        "moan.speed3.cowgirl.gf_close": [
            _("I'm BOUNCING on her boyfriend! She'd be DESTROYED! I'm SORRY!"),

            _("I can't stop RIDING you! She doesn't deserve this betrayal!"),

            _("Your cock is hitting my CERVIX! Oh FUCK!"),

        ],
        "cum_inside.cowgirl.gf_close": [
            _("You came inside me... her boyfriend just came inside me... oh god..."),

            _("She doesn't know you just filled me up... I'm horrible..."),

            _("My pussy is full of your cum... I can't believe I let you..."),

        ],
        # RCG

        # ---- gf_distant: doesn't really care about the GF ----
        # generic fallback
        "moan.speed1.gf_distant": [
            _("Your girlfriend has no idea... and I stopped caring..."),

            _("She doesn't satisfy you like I do... that's why you keep coming back..."),

            _("I can feel every inch stretching me..."),

        ],
        "moan.speed2.gf_distant": [
            _("We've done this enough times that I've stopped thinking about her..."),

            _("Your girlfriend is a distant thought when you're inside me..."),

            _("I can feel you throbbing inside me..."),

        ],
        "moan.speed3.gf_distant": [
            _("She can't do THIS for you! Admit it! I'm BETTER!"),

            _("Forget about her! You're MINE right now!"),

            _("OH FUCK! Your cock is splitting me open!"),

        ],
        # hj
        "moan.speed1.hj.gf_distant": [
            _("Your girlfriend's hand could never feel this good on you..."),

            _("I bet she doesn't even know what you like... I do..."),

            _("Throbbing in my grip... she could never handle you like this..."),

        ],
        "moan.speed3.hj.gf_distant": [
            _("Bet your girlfriend NEVER jerks you this hard! She WISHES!"),

            _("My hand is BETTER than hers! Admit it! SAY it!"),

            _("She's NEVER felt you this hard in her hand! That's ALL me!"),

        ],
        # bj
        "moan.speed1.bj.gf_distant": [
            _("I give better head than she ever could... that's why you come to me..."),

            _("Your girlfriend probably doesn't even swallow... I do..."),

            _("Your thick cock feels so good..."),

        ],
        "moan.speed3.bj.gf_distant": [
            _("She could NEVER suck you like this! I'm the BEST you've ever had!"),

            _("DEEPER than your girlfriend EVER went! Admit I'm BETTER!"),

            _("HARDER! Your dick drives me INSANE!"),

        ],
        # tj
        "moan.speed1.tj.gf_distant": [
            _("Your girlfriend's chest can't do what mine does..."),

            _("Better tits than her and you know it..."),

            _("Don't stop... just like that..."),

        ],
        "moan.speed3.tj.gf_distant": [
            _("My tits are BETTER than hers! Say it! SAY IT!"),

            _("She could NEVER use her body like this for you!"),

            _("HARDER! Your dick drives me INSANE!"),

        ],
        # cowgirl
        "moan.speed1.cowgirl.gf_distant": [
            _("I bet your girlfriend just lies there... I RIDE..."),

            _("She could never move her hips like this..."),

            _("I love feeling your dick pulse inside me..."),

        ],
        "moan.speed3.cowgirl.gf_distant": [
            _("Can she BOUNCE like this?! I don't THINK so!"),

            _("Your girlfriend could NEVER ride this hard! I'm BETTER!"),

            _("OH FUCK! Your cock is splitting me open!"),

        ],
        "cum_inside.cowgirl.gf_distant": [
            _("You came inside ME, not her... because I'm better..."),

            _("Fill me up... she doesn't make you cum like I do..."),

            _("I feel it leaking... there was so much..."),

        ],
        # RCG

        # ---- gf_hostile: she dislikes the player's GF, enjoys it ----
        # generic fallback
        "moan.speed1.gf_hostile": [
            _("Mmm... your girlfriend probably thinks you're being good right now..."),

            _("I'm basically your second girlfriend at this point..."),

            _("Leave her... you know you want to... I'm all you need..."),

        ],
        "moan.speed2.gf_hostile": [
            _("Does she even make you moan like this? I doubt it..."),

            _("Your girlfriend is living a fantasy... THIS is your reality..."),

            _("I LOVE being your dirty secret... she has NO idea what she's missing..."),

        ],
        "moan.speed3.gf_hostile": [
            _("HARDER! Your girlfriend could NEVER handle this!"),

            _("She's NOTHING compared to me and we BOTH know it!"),

            _("DUMP HER! You don't NEED her! You need ME!"),

        ],
        # hj
        "moan.speed1.hj.gf_hostile": [
            _("Stroking what she thinks belongs to her... it doesn't..."),

            _("My hand on her boyfriend's cock... and she has no clue... perfect..."),

            _("I love how hard you get for me..."),

        ],
        "moan.speed3.hj.gf_hostile": [
            _("Your girlfriend could NEVER jerk you like this! She's PATHETIC!"),

            _("This dick is MINE! Not hers! She can CRY about it!"),

            _("HARDER! Your dick drives me INSANE!"),

        ],
        # bj
        "moan.speed1.bj.gf_hostile": [
            _("Her boyfriend in my mouth... she'd be SICK if she knew..."),

            _("I suck you better than that loser ever could..."),

            _("Mmm... I love your cock in my mouth..."),

        ],
        "moan.speed3.bj.gf_hostile": [
            _("DEEPER than she EVER went! Your girlfriend is WORTHLESS!"),

            _("She could NEVER make you moan like this! I OWN this dick!"),

            _("She could NEVER take it this DEEP! I'm CHOKING and I LOVE it!"),

        ],
        # tj
        "moan.speed1.tj.gf_hostile": [
            _("Better tits than her... that's why you're between mine..."),

            _("Her boyfriend between my tits... she'd be devastated... good..."),

            _("My tits feel so good wrapped around you..."),

        ],
        "moan.speed3.tj.gf_hostile": [
            _("My tits are SUPERIOR to hers and you KNOW it! SAY IT!"),

            _("She could NEVER give you this! Her body is NOTHING!"),

            _("My tits are CRUSHING your cock! She could NEVER do this!"),

        ],
        # cowgirl
        "moan.speed1.cowgirl.gf_hostile": [
            _("Riding her man slowly... she'd DIE if she could see this..."),

            _("Your girlfriend just lies there... I RIDE you like you deserve..."),

            _("I can control how deep you go... mmm..."),

        ],
        "moan.speed3.cowgirl.gf_hostile": [
            _("I RIDE you BETTER than her! DUMP that loser! You're MINE!"),

            _("She could NEVER bounce like this! I'm the ONLY one you need!"),

            _("OH GOD! Every inch! I feel EVERY inch!"),

        ],
        "cum_inside.cowgirl.gf_hostile": [
            _("You came inside ME. Not her. Tell me who's better. SAY IT."),

            _("Her boyfriend's cum is inside ME right now. She has NOTHING."),

            _("I feel it leaking... there was so much..."),

        ],
        # RCG

        # ══════════════════════════════════════════════════════
        # LESBIAN DIALOGUE POOLS
        # ══════════════════════════════════════════════════════

        # ── Moans ──
        "moan.speed1.lesbian": [
            _("I can't believe I'm doing this..."),

            _("This doesn't mean I like men..."),

            _("Just... don't talk. Don't make this weird."),

        ],
        "moan.speed2.lesbian": [
            _("Don't... don't look at me like that... I'm not enjoying this..."),

            _("This is just my body reacting... it doesn't mean anything..."),

            _("Shut up... just shut up and keep going..."),

        ],
        "moan.speed3.lesbian": [
            _("Oh god... I hate you for making me feel this..."),

            _("Why does this feel so good when I don't even want it..."),

            _("This isn't fair... this isn't supposed to feel like this..."),

        ],

        # ── Lesbian per-act moans ──
        "moan.speed1.hj.lesbian": [
            _("I'm touching your... this is so wrong..."),

            _("Just get it over with... I'm only using my hand..."),

            _("Don't look at me while I do this..."),

        ],
        "moan.speed2.hj.lesbian": [
            _("It's just my hand... it's just my hand... this doesn't count..."),

            _("I can't believe I know how to do this now..."),

            _("Faster? Fine. The sooner it's over..."),

        ],
        "moan.speed3.hj.lesbian": [
            _("Why am I getting good at this... what's wrong with me..."),

            _("Just finish already... my hand is tired and my dignity is gone..."),

        ],
        "moan.speed1.bj.lesbian": [
            _("I have your... in my mouth... what am I doing..."),

            _("I never thought I'd be doing this..."),

            _("Don't you dare grab my head..."),

        ],
        "moan.speed2.bj.lesbian": [
            _("Mmph... I hate that I'm getting used to this..."),

            _("Just... finish... I can't believe my mouth is on..."),

        ],
        "moan.speed3.bj.lesbian": [
            _("Glk... I hate you... I hate everything about this... don't stop..."),

            _("On my knees for you... if my friends could see me..."),

        ],

        # ── ATM tease lines (BJ entered from anal) ──

        # — ATM: generic (any girl) —
        "moan.speed1.bj.atm": [
            _("Mmm... I can taste where you just were..."),

            _("It tastes... different. After what you did..."),

            _("You went from my ass to my mouth... and I'm still doing it..."),

        ],
        "moan.speed2.bj.atm": [
            _("Mmph... straight from my ass... you're filthy..."),

            _("I know exactly where this was... and I'm still sucking..."),

            _("The taste of my own ass on your cock... god..."),

        ],
        "moan.speed3.bj.atm": [
            _("Glk... ass to mouth... you really don't care, do you..."),

            _("I can barely think... the taste... everything..."),

            _("Right from my ass and you shoved it in my mouth..."),

        ],

        # — ATM: cum_slut —
        "moan.speed1.bj.atm.cum_slut": [
            _("Mmm... I love how it tastes after being inside my ass..."),

            _("You were just in my ass and now I get to taste it... perfect..."),

            _("The taste of my ass on your cock... I want more..."),

        ],
        "moan.speed2.bj.atm.cum_slut": [
            _("Fuck, the taste... straight from my ass... give me all of it..."),

            _("I can taste everything... I love it... don't pull out..."),

        ],
        "moan.speed3.bj.atm.cum_slut": [
            _("Mmgh... ass to mouth is the best... I'm addicted to this taste..."),

            _("Faster... I want every bit of my ass off your cock..."),

        ],

        # — ATM: hate_cum —
        "moan.speed1.bj.atm.hate_cum": [
            _("This is... ugh... I can tell where that was..."),

            _("You really put it in my mouth after... god, that's disgusting..."),

            _("The taste... I can't believe I'm doing this..."),

        ],
        "moan.speed2.bj.atm.hate_cum": [
            _("I'm trying not to think about where this was..."),

            _("This is revolting... you know that, right...?"),

        ],
        "moan.speed3.bj.atm.hate_cum": [
            _("I hate this... I hate the taste... I hate that you made me..."),

            _("You're disgusting for making me do this... glk..."),

        ],

        # — ATM: hardcore —
        "moan.speed1.bj.atm.hardcore": [
            _("Yeah... make me taste my own ass. I can take it."),

            _("Straight from my ass to my mouth... that's what you wanted, right?"),

            _("You're nasty for this... and I like it."),

        ],
        "moan.speed2.bj.atm.hardcore": [
            _("Shove it deeper... I want to taste everything..."),

            _("Ass to mouth... you don't hold back and I love that..."),

        ],
        "moan.speed3.bj.atm.hardcore": [
            _("Glk... harder... make me choke on it after my ass..."),

            _("Mmph... deeper... fuck my throat, I don't care where it's been..."),

        ],
        "moan.speed3.bj.atm.submissive": [
            _("Use my mouth like you used my ass... I can handle it..."),

            _("Glk... use my mouth... it's yours... mmph..."),

            _("Mmph... whatever you want... even after my ass... glk... I'm yours..."),

        ],

        # — ATM: cute —
        "moan.speed1.bj.atm.cute": [
            _("You... you really want me to... after it was in my... okay..."),

            _("This feels... really embarrassing... tasting where it was..."),

            _("I can't believe I'm actually doing this..."),

        ],
        "moan.speed2.bj.atm.cute": [
            _("It's so dirty... why does it make me feel this way..."),

            _("I shouldn't like this... it was just in my butt..."),

        ],
        "moan.speed3.bj.atm.cute": [
            _("Oh god... this is so wrong... please don't tell anyone I did this..."),

            _("I can't... the taste... why am I not stopping..."),

        ],

        # — ATM: anal_lover —
        "moan.speed1.bj.atm.anal_lover": [
            _("Mmm... tasting myself on you after anal... that's really hot..."),

            _("I love that you went from my ass to my mouth... it connects everything..."),

        ],
        "moan.speed2.bj.atm.anal_lover": [
            _("The taste of where you just were... it makes me want you back there..."),

            _("Ass to mouth... I need you in my ass again after this..."),

        ],
        "moan.speed3.bj.atm.anal_lover": [
            _("God... I can taste my ass on you and it's making me crazy..."),

            _("Faster... clean it off so you can put it back in my ass..."),

        ],

        # — ATM: anal_hater —
        "moan.speed1.bj.atm.anal_hater": [
            _("You're making me taste... after you put it there... I didn't even want anal..."),

            _("This is so much worse because I didn't even like the anal part..."),

        ],
        "moan.speed2.bj.atm.anal_hater": [
            _("I hated it in my ass and now I have to taste it too...?"),

            _("You really have no shame... my ass, now my mouth..."),

        ],
        "moan.speed3.bj.atm.anal_hater": [
            _("I can't believe this... I hated every second of anal and now this..."),

            _("Glk... this is punishment... you know I hate this..."),

        ],

        # — ATM: lesbian —
        "moan.speed1.bj.atm.lesbian": [
            _("A guy's cock... from my ass... in my mouth... what is my life..."),

            _("This is literally the worst thing... and I'm still doing it..."),

        ],
        "moan.speed2.bj.atm.lesbian": [
            _("A man just had his dick in my ass and now my mouth... I'm losing my mind..."),

            _("If my girlfriend knew I was doing ass to mouth with a guy..."),

        ],
        "moan.speed3.bj.atm.lesbian": [
            _("Glk... from my ass... you have NO idea how insane this is for me..."),

            _("A lesbian... doing ass to mouth... for a guy... fuck..."),

        ],

        # ── ATM: initial reaction (one-shot, first BJ action after ATM) ──
        "atm_react.bj": [
            _("Wait... you're putting it in my mouth after...?"),

            _("You want me to... after it was in my ass...?"),

            _("Oh god... I can taste where that was..."),

        ],
        "atm_react.bj.cum_slut": [
            _("Mmm... straight from my ass? Don't mind if I do..."),

            _("Oh, I can taste everything... I love that you didn't even clean it..."),

        ],
        "atm_react.bj.hate_cum": [
            _("You want me to put THAT in my mouth? After where it's been?!"),

            _("That's... that was just in my... ugh, fine..."),

        ],
        "atm_react.bj.hardcore": [
            _("Right from my ass, huh? Bold. I like it."),

            _("You dirty bastard... putting it in my mouth after my ass..."),

        ],
        "atm_react.bj.cute": [
            _("W-wait... you were just... in my... and now you want me to...?!"),

            _("Oh my god... I can taste... is this really happening...?"),

        ],
        "atm_react.bj.anal_lover": [
            _("Mmm... I can still taste where you were... give me more..."),

            _("From my favorite hole to my mouth... I don't mind at all..."),

        ],
        "atm_react.bj.anal_hater": [
            _("You want me to suck it after THAT? I barely survived the anal part..."),

            _("Are you serious? It was just... ugh... this is disgusting..."),

        ],
        "atm_react.bj.lesbian": [
            _("A man's cock... from my ass... to my mouth... this can't be real..."),

            _("You're joking, right? It was in my... and now you want me to..."),

        ],
        "moan.speed1.tj.lesbian": [
            _("You're using my chest for... ugh. Just don't look at my face."),

            _("At least I don't have to touch it directly..."),

        ],
        "moan.speed2.tj.lesbian": [
            _("I can feel it throbbing between... god, this is humiliating..."),

            _("My breasts weren't meant for... this..."),

        ],
        "moan.speed3.tj.lesbian": [
            _("My tits wrapped around it... why does it feel so GOOD..."),

            _("If she could see me now... giving you a titjob... DON'T STOP!"),

        ],
        "moan.speed1.cowgirl.lesbian": [
            _("You're inside me... this wasn't supposed to happen..."),

            _("This doesn't change who I am... this doesn't change anything..."),

        ],
        "moan.speed2.cowgirl.lesbian": [
            _("I shouldn't be moving my hips like this... but I can't stop..."),

            _("My body is a traitor... I'm riding you and I can't stop..."),

        ],
        "moan.speed3.cowgirl.lesbian": [
            _("Oh god... you shouldn't make me feel... no... this isn't me..."),

            _("Harder... no, wait... yes... I hate this... don't stop..."),

        ],
        "moan.speed1.anal.lesbian": [
            _("You're in my... I can't even say it..."),

            _("This is the furthest thing from anything I've ever wanted..."),

        ],
        "moan.speed2.anal.lesbian": [
            _("Ahh... no one has ever... why is it you who..."),

            _("I hate that this feels... no. I hate everything about this."),

        ],
        "moan.speed3.anal.lesbian": [
            _("Taking it in the ass from you... my life is a joke..."),

            _("AAAH... I hate you... I hate how good this... SHUT UP!"),

            _("A man... doing THIS to me... I can't believe my body... NNGH!"),

            _("Faster... NO! I didn't mean to say that! I DIDN'T!"),

            _("This doesn't count... this isn't real... it CAN'T be real..."),

            _("My body is betraying everything I've ever believed in... and I can't stop it..."),

        ],

        # ── Lesbian proof: denial (0-25) ──
        "moan.speed2.lesbian_denial": [
            _("This is purely physical. Nothing more."),

            _("My body is betraying me. That's all this is."),

            _("I'm not attracted to you. This means nothing."),

        ],
        "moan.speed3.lesbian_denial": [
            _("Don't flatter yourself... any stimulation would do this..."),

            _("I hate every second of this... my body just won't cooperate..."),

        ],

        # ── Lesbian proof: confused (26-50) ──
        "moan.speed2.lesbian_confused": [
            _("Maybe he's different... no. No, he's not. This is just..."),

            _("I don't understand why I keep coming back to this..."),

        ],
        "moan.speed3.lesbian_confused": [
            _("This wasn't supposed to feel like this... why does it..."),

            _("I keep telling myself this is the last time... but..."),

        ],

        # ── Lesbian proof: conflict (51-75) ──
        "moan.speed2.lesbian_conflict": [
            _("I hate that I look forward to this..."),

            _("I told myself I wouldn't enjoy it this time..."),

        ],
        "moan.speed3.lesbian_conflict": [
            _("You're ruining everything I thought I knew about myself..."),

            _("I hate you... I hate that you make me feel this way..."),

        ],

        # ── Lesbian proof: accepted (76-100) ──
        "moan.speed2.lesbian_accepted": [
            _("You're the exception... the only one..."),

            _("I'm still into women... you're just... you."),

        ],
        "moan.speed3.lesbian_accepted": [
            _("Don't let this go to your head... you're the only man alive who gets this..."),

            _("Fine... you win... just this once... again..."),

        ],

        # ── Dressup ──
        "dressup.lesbian": [
            _("This never happened."),

            _("If anyone finds out about this, I will end you."),

            _("We're done here. Don't look at me like that."),

        ],
        "dressup.lesbian_accepted": [
            _("Same time tomorrow? ...I'm kidding. Maybe."),

            _("This still doesn't mean anything. ...Stop smiling."),

            _("I'm getting dressed. And no, you can't watch. ...Fine, you can watch."),

        ],

        # ── Girl orgasm ──
        "girl_cum.lesbian": [
            _("That didn't count..."),

            _("My body betrayed me, that's all."),

            _("Don't you dare say a word about this."),

        ],
        "girl_cum.lesbian_denial": [
            _("That was... that was just friction. It means nothing."),

            _("Don't flatter yourself. Any stimulation would have done that."),

        ],
        "girl_cum.lesbian_confused": [
            _("I don't... I don't understand why that felt so..."),

            _("This wasn't supposed to happen... not like this..."),

        ],
        "girl_cum.lesbian_conflict": [
            _("You made me cum again. I'm still processing what that means."),

            _("I hate that you can do this to me..."),

        ],
        "girl_cum.lesbian_accepted": [
            _("You made me cum again. Happy now? ...I am."),

            _("Fine. You win. This time. Like every time."),

        ],

        # ── Girl post-orgasm ──
        "girl_post_cum.lesbian": [
            _("This changes nothing between us."),

            _("Don't look so smug. You got lucky."),

            _("I need a minute. And I need you to not say anything."),

        ],
        "girl_post_cum.lesbian_denial": [
            _("That proved nothing. Absolutely nothing."),

            _("I'm leaving. This didn't happen."),

        ],
        "girl_post_cum.lesbian_confused": [
            _("I need to think about this. Alone. Without you looking at me like that."),

            _("Why do I keep doing this to myself..."),

        ],
        "girl_post_cum.lesbian_conflict": [
            _("You're just... the exception I never asked for."),

            _("Don't say anything. I already know what you're thinking."),

        ],
        "girl_post_cum.lesbian_accepted": [
            _("You're just... you. And I hate how much I like that."),

            _("If you tell anyone about this, I'll deny everything. ...See you next time."),

        ],

        # ══════════════════════════════════════════════════════
        # GIRLFRIEND DIALOGUE POOLS (mirrors boyfriend pools)
        # ══════════════════════════════════════════════════════
        # NOTE: moan.speed1/2/3.girlfriend are defined inline next to their boyfriend counterparts above
        "dressup.girlfriend": [
            _("She can never know about this. Promise me."),

            _("I need to shower before I see her... I smell like you."),

            _("I'm going to hate myself when I look at her tonight."),

        ],

        # ══════════════════════════════════════════════════════
        # NTR PARTNER WATCHING — girl reacts to partner observing
        # ══════════════════════════════════════════════════════

        # ── Moans: Speed 1 (slow, awareness) ──

        "moan.speed1.partner_watching": [
            _("Oh god... you're really watching this..."),

            _("I can feel your eyes on me, baby... don't look away."),

            _("This is so weird... knowing you're right there..."),

            _("You said this was okay... so why does it feel so naughty?"),

            _("Mmm... being watched makes it feel different... more intense..."),

            _("I can't believe this is happening... and you're just standing there..."),

        ],

        "moan.speed1.partner_watching.cum_slut": [
            _("Mmm... watch closely, baby. This is just the warm-up."),

            _("You have no idea how wet watching you watch me makes me..."),

            _("Keep those eyes open, honey. You don't want to miss what comes next."),

        ],

        "moan.speed1.partner_watching.cute": [
            _("I'm so sorry, baby... but this feels really nice..."),

            _("Please don't hate me... I can't help how good this feels..."),

            _("Are you okay? I can stop... I just... mmm... it's hard to stop..."),

        ],

        # ── Moans: Speed 2 (standard, getting into it) ──

        "moan.speed2.partner_watching": [
            _("Oh god, baby, he's so deep... aah..."),

            _("You're watching him do this to me... and I love it..."),

            _("Mmm... look what he's doing to me... can you see?"),

            _("This is so much... knowing you can see everything..."),

            _("I keep looking at you while he... mmm... oh god..."),

            _("You agreed to this... so watch. Watch all of it."),

            _("He's hitting spots you never... oh... oh god..."),

            _("Don't look away... I want you to see what this does to me..."),

        ],

        "moan.speed2.partner_watching.cum_slut": [
            _("Are you watching how deep he goes? Mmm... every inch, baby..."),

            _("Oh honey... his cock is making me lose my mind... and you're just watching..."),

            _("I want you to see how much I love this... every. Single. Stroke."),

            _("Watch me take him... you wanted this, remember? Aaah..."),

        ],

        "moan.speed2.partner_watching.hardcore": [
            _("Look at your girlfriend getting wrecked right in front of you..."),

            _("He's better than you... and now you know it. Watch."),

            _("This is what I needed all along... and you get to watch me find out."),

            _("Harder... I want him to see what a real man does to me."),

        ],

        "moan.speed2.partner_watching.cute": [
            _("Baby, I'm sorry... I can't... he's making me feel so good..."),

            _("I'm trying to hold back... but he's... mmm... I'm sorry..."),

            _("Please don't be upset... my body just... it reacts to him..."),

            _("I love you... I do... but oh god this feels amazing..."),

        ],

        # ── Moans: Speed 3 (fast, mind-breaking) ──

        "moan.speed3.partner_watching": [
            _("OH GOD, BABY, HE'S GONNA BREAK ME... AAAH!"),

            _("YOU'RE WATCHING... AND I DON'T CARE ANYMORE... AAAH!"),

            _("I'M LOSING IT... RIGHT IN FRONT OF YOU... OH FUCK!"),

            _("CAN YOU SEE THIS? CAN YOU SEE WHAT HE'S DOING TO ME?!"),

            _("HE'S SO DEEP... I CAN'T... I CAN'T THINK... AAAH!"),

            _("MY MIND IS GOING BLANK... AND ALL I SEE IS HIM... AAH!"),

            _("BABY... BABY I'M... HE'S MAKING ME... I CAN'T...!"),

            _("LOOK AT ME... LOOK AT WHAT HE'S... OH FUCK! AAAH!"),

        ],

        "moan.speed3.partner_watching.cum_slut": [
            _("WATCH ME! WATCH HIS COCK DESTROY ME! I LOVE IT! AAAH!"),

            _("OH FUCK, BABY, HIS DICK IS SO GOOD! I'M GOING CRAZY! AAAH!"),

            _("YOU'RE WATCHING AND IT MAKES IT EVEN BETTER! DON'T STOP! AAAH!"),

            _("I'M HIS RIGHT NOW! YOURS CAN WAIT! AAAH!"),

            _("BABY, HE'S HITTING SPOTS YOU... YOU NEVER... AAAH!"),

            _("I WANT YOU TO SEE EVERY... SINGLE... THRUST! AAAH!"),

        ],

        "moan.speed3.partner_watching.hardcore": [
            _("LOOK AT ME! LOOK AT YOUR GIRL SCREAMING FOR ANOTHER MAN! AAAH!"),

            _("HE'S RUINING ME AND YOU'RE JUST STANDING THERE! AAAH!"),

            _("THIS IS WHAT I'VE BEEN MISSING! CAN YOU SEE?! AAAH!"),

            _("YOUR GIRL IS GETTING WRECKED AND YOU CAN'T DO ANYTHING! AAAH!"),

            _("HE FUCKS ME BETTER THAN YOU EVER... EVER... AAAH!"),

            _("TAKE NOTES, BABY! THIS IS HOW IT'S DONE! AAAH!"),

        ],

        "moan.speed3.partner_watching.cute": [
            _("I'M SORRY BABY, I CAN'T HOLD BACK... HE'S TOO GOOD... AAAH!"),

            _("DON'T LOOK... NO, LOOK... I DON'T KNOW... AAAH!"),

            _("MY BODY WON'T LISTEN TO ME ANYMORE... I'M SORRY... AAAH!"),

            _("BABY I STILL LOVE YOU BUT I... I CAN'T STOP... AAAH!"),

            _("I'M TRYING NOT TO SCREAM BUT... OH GOD... I'M SORRY...!"),

            _("PLEASE FORGIVE ME... I... HE MAKES ME... AAAH!"),

        ],

        "moan.speed3.partner_watching.girlfriend": [
            _("BABY, A COCK IS... I NEVER KNEW IT COULD... AAAH!"),

            _("YOU'RE WATCHING A MAN WRECK YOUR GIRLFRIEND... AND I LOVE IT! AAAH!"),

            _("NO FINGERS... NO TOYS... NOTHING YOU HAVE COMPARES TO... AAAH!"),

            _("I'M YOUR GIRLFRIEND BUT RIGHT NOW I'M... I'M HIS! AAAH!"),

            _("HE'S DOING WHAT YOU NEVER COULD, BABY... AAAH!"),

        ],

        # ══════════════════════════════════════════════════════════
        # NTR KNOWN — partner knows and permits, but is NOT watching.
        # No secret guilt ("if he finds out"), no audience. She revels
        # in the arrangement: he allowed it and he's missing all of it.
        # ══════════════════════════════════════════════════════════

        "moan.speed1.ntr_known": [
            _("He said I could do this whenever I want... and he's not even here to see. God, I love this."),

            _("My boyfriend knows about you... he just doesn't know it's happening right now..."),

            _("He gave me permission for this... he has no idea how often I use it..."),

            _("It's so strange... he allows this, but he's not here. Just us. Mmm..."),

            _("He'll never see this one... but he said it's fine. So it's fine, right...?"),

        ],

        "moan.speed1.ntr_known.cute": [
            _("He said it was okay... so this isn't wrong... right? Then why am I shaking..."),

            _("My boyfriend allowed this... I still can't believe he did... mmm..."),

        ],

        "moan.speed2.ntr_known": [
            _("Oh god... my boyfriend lets me have this... and he doesn't even know how good it feels..."),

            _("He said yes to this... but he's not watching. It's just for me right now... aah..."),

            _("Mmm... his rules, and he's not even around to enforce them..."),

            _("My boyfriend permits it and misses every second of it... his loss, baby..."),

            _("He has no idea what he's letting me do... oh god, right there..."),

            _("This is allowed. This is ALLOWED. And it still feels so filthy... aah..."),

        ],

        "moan.speed2.ntr_known.cum_slut": [
            _("He lets his girl get railed and doesn't even watch... his loss. Mmm, deeper..."),

            _("My boyfriend permits this and I abuse it every single chance I get... aah..."),

            _("He said I could be a slut for you... he just doesn't know how much of one..."),

        ],

        "moan.speed2.ntr_known.cute": [
            _("He said it's okay... so it's okay... then why does it feel this bad... and this good..."),

            _("I keep thinking about how he just... let me. And now I'm here doing this... mmm..."),

        ],

        "moan.speed3.ntr_known": [
            _("MY BOYFRIEND LETS ME DO THIS... AND HE'S MISSING EVERYTHING! AAAH!"),

            _("HE SAID YES AND HE'S NOT EVEN HERE... THIS IS ALL MINE! AAAH!"),

            _("HE ALLOWS THIS BUT HE'LL NEVER FEEL IT LIKE I DO... AAAH!"),

            _("I'M ALLOWED TO... OH GOD... HE HAS NO IDEA HOW MUCH I NEEDED THIS! AAAH!"),

        ],

        "moan.speed3.ntr_known.cum_slut": [
            _("HE LETS ME BE THIS AND ISN'T EVEN HERE TO SEE HIS SLUT! AAAH!"),

            _("PERMISSION GRANTED, BABY... AND HE'S MISSING THE BEST PART! AAAH!"),

        ],

        "moan.speed3.ntr_known.hardcore": [
            _("MY BOYFRIEND ALLOWS THIS BECAUSE HE KNOWS HE CAN'T COMPETE! AAAH!"),

            _("HE HANDED ME OVER AND ISN'T EVEN MAN ENOUGH TO WATCH! AAAH!"),

        ],

        "girl_cum.ntr_known": [
            _("I'M CUMMING... AND MY BOYFRIEND SAID I COULD... OH GOD... AAAH!"),

            _("HE LETS ME CUM ON OTHER MEN... AND HE'S NOT EVEN HERE! AAAH!"),

            _("I'M ALLOWED TO CUM LIKE THIS... HE HAS NO IDEA... AAAH!"),

        ],

        "cum_inside.ntr_known": [
            _("He lets you finish inside me... and he'll never know it's dripping out of me right now..."),

            _("My boyfriend permits this... your cum inside me, with his blessing... god..."),

            _("He said it was okay... he just doesn't know it's happening while he's gone..."),

        ],

        # ── Girl Orgasm while watched ──

        "girl_cum.partner_watching": [
            _("OH GOD I'M CUMMING... BABY, I'M CUMMING ON HIS COCK... AAAH!"),

            _("I'M... I'M CUMMING RIGHT IN FRONT OF YOU... I CAN'T STOP IT... AAAH!"),

            _("HE'S MAKING ME CUM... OH GOD, YOU CAN SEE EVERYTHING... AAAH!"),

            _("I'VE NEVER CUM THIS HARD... AND YOU'RE WATCHING... AAAH!"),

        ],

        "girl_cum.partner_watching.cum_slut": [
            _("YES YES YES! I'M CUMMING SO HARD! WATCH ME, BABY! AAAH!"),

            _("CAN YOU SEE HOW HARD HE MAKES ME CUM?! THIS IS INSANE! AAAH!"),

            _("BABY, HE MADE ME CUM SO HARD... YOU COULD NEVER DO THIS TO ME! AAAH!"),

            _("I'M SQUEEZING HIS COCK AND CUMMING FOR YOU TO SEE! AAAH!"),

        ],

        "girl_cum.partner_watching.hardcore": [
            _("I'M CUMMING AND YOUR FACE RIGHT NOW IS... PRICELESS! AAAH!"),

            _("HE JUST MADE YOUR GIRL CUM HARDER THAN YOU EVER COULD! AAAH!"),

            _("LOOK AT ME CUMMING FOR ANOTHER MAN! LOOK! AAAH!"),

        ],

        "girl_cum.partner_watching.cute": [
            _("I'M CUMMING... BABY, I'M SO SORRY... I CAN'T HELP IT... AAAH!"),

            _("PLEASE DON'T HATE ME... HE MADE ME... I'M... OH GOD... AAAH!"),

            _("I DIDN'T WANT TO CUM THIS HARD IN FRONT OF YOU... AAAH!"),

        ],

        "girl_cum.partner_watching.girlfriend": [
            _("I'M CUMMING ON A COCK... AND YOU'RE WATCHING, BABY... AAAH!"),

            _("A MAN JUST MADE ME CUM HARDER THAN YOU EVER... OH GOD... AAAH!"),

            _("YOU'RE WATCHING YOUR GIRLFRIEND CUM FROM A REAL COCK... AAAH!"),

        ],

        "girl_cum_hard.partner_watching": [
            _("OH FUCK OH FUCK OH FUCK... BABY... HE'S MAKING ME... I CAN'T... AAAH!"),

            _("I'M CUMMING SO HARD I CAN'T... I CAN'T SEE... BABY... AAAH!"),

            _("MY WHOLE BODY IS... AND YOU'RE RIGHT THERE... OH GOD... AAAH!"),

        ],

        "girl_post_cum.partner_watching": [
            _("Oh god... baby, did you see that...? He made me cum so hard..."),

            _("I can barely stand... and you watched the whole thing..."),

            _("That was... wow... I can't believe you just saw that..."),

        ],

        "girl_post_cum.partner_watching.cum_slut": [
            _("Mmm... that was amazing, baby. And you got front row seats."),

            _("Did you enjoy watching me cum? Because I loved knowing you were there."),

        ],

        "girl_post_cum.partner_watching.cute": [
            _("Baby... are you okay? I didn't mean to... it just felt so good..."),

            _("I'm sorry you had to see me like that... I couldn't control myself..."),

        ],

        # ── Cum Inside while watched ──

        "cum_inside.partner_watching": [
            _("He came inside me... and you saw everything..."),

            _("Oh god... I can feel his cum... baby, he filled me up right in front of you..."),

            _("That just happened... with you watching... I feel his cum dripping..."),

            _("You just watched another man cum inside your girlfriend..."),

        ],

        "cum_inside.partner_watching.cum_slut": [
            _("Mmm... feel how full he made me, baby. Every drop. You watched it all."),

            _("He pumped me full and you saw everything... god, that was hot."),

            _("I'm dripping with his cum and you're right there... I love this."),

            _("Baby, he filled me up SO good... you have no idea how warm it feels..."),

        ],

        "cum_inside.partner_watching.cute": [
            _("I'm so sorry... he finished inside me... and you were right there..."),

            _("Oh no... baby, I didn't mean for... I couldn't stop him... it felt too good..."),

            _("I can feel his cum inside me... baby, please don't be mad..."),

            _("He came inside... I should have stopped him but... I didn't want to..."),

        ],

        "cum_inside.partner_watching.hardcore": [
            _("He just creampied your girlfriend. Right in front of you. And I loved every second."),

            _("Your girl is full of another man's cum. Deal with it, baby."),

            _("Mmm... he came inside me and you just stood there watching. Pathetic."),

        ],

        "cum_inside.partner_watching.girlfriend": [
            _("He came inside me, baby... something you could never do..."),

            _("A man just filled your girlfriend with his cum... and it felt amazing..."),

            _("Baby... I can feel his cum inside me... no toy could ever do this..."),

        ],

        "cum_inside_forced.partner_watching": [
            _("He came inside me! Baby, I told him not to! Oh god..."),

            _("I didn't want him to... but he came inside... and you saw it all..."),

            _("Baby, I tried to stop him... I swear... I can feel it dripping..."),

        ],

        # ── Cum Outside while watched ──

        "cum_outside.partner_watching": [
            _("He pulled out just in time... but you saw everything else."),

            _("Look at the mess he made on me... right in front of you."),

            _("At least he didn't finish inside... but baby, that was close..."),

            _("He covered me... and you watched every drop land on me..."),

        ],

        "cum_outside.partner_watching.cum_slut": [
            _("Mmm... he should have cum inside. But this mess is nice too, right baby?"),

            _("Look at all his cum on me... wasted. Should have been inside."),

        ],

        # ── Cum Face while watched ──

        "cum_face.partner_watching": [
            _("He came on my face... baby, are you still watching...?"),

            _("Can you see it? His cum is all over my face... and you're right there."),

            _("Baby... I have his cum on my face... right in front of you..."),

        ],

        "cum_face.partner_watching.cum_slut": [
            _("Mmm... look at me, baby. Look at your girlfriend covered in his cum. Hot, right?"),

            _("Baby, look at my face... all his cum... I love how it feels."),

            _("I bet you wish you could do this to me too, baby... mmm..."),

        ],

        # ── Cum Mouth while watched ──

        "cum_mouth.partner_watching": [
            _("I swallowed it... and you watched me do it."),

            _("He came in my mouth... oh god, you saw that, didn't you..."),

            _("Baby... I swallowed another man's cum... right in front of you..."),

            _("I can still taste him... and you're just standing there..."),

        ],

        "cum_mouth.partner_watching.cum_slut": [
            _("Mmm... I swallowed every drop, baby. You saw how much I enjoyed it."),

            _("His cum tasted so good, baby... want me to describe it?"),

        ],

        # ── Cum Tits/Ass while watched ──

        "cum_tits.partner_watching": [
            _("He came all over my tits, baby... can you see the mess?"),

            _("Look at my tits covered in his cum... and you're right there watching..."),

        ],

        "cum_ass.partner_watching": [
            _("He came on my ass, baby... the mess he made back there..."),

            _("My ass is covered in his cum... and you watched the whole thing..."),

        ],

        # ── Speed 2 GF watching (lesbian partner) ──

        "moan.speed2.partner_watching.girlfriend": [
            _("Baby... a man is inside me right now... and it feels... mmm..."),

            _("You're watching a cock do things to me that you... mmm... never could..."),

            _("I'm your girlfriend and he's... oh god... he's so deep..."),

            _("His cock feels so different from anything you've ever... aah..."),

        ],

        # ── Moans: Speed 1 (curious, "is this working?") ──

        "moan.speed1.fj": [
            _("Is this... actually doing something for you?"),

            _("This feels so weird from my end..."),

            _("Am I pressing hard enough?"),

            _("Your face tells me this is working, but it feels so strange..."),

        ],

        # ── Moans: Speed 2 (getting into it) ──

        "moan.speed2.fj": [
            _("Okay, I think I'm getting the hang of this..."),

            _("Your face right now... this really does it for you, huh?"),

            _("I can feel you twitching between my toes..."),

            _("This is way more fun than I expected..."),

        ],

        # ── Moans: Speed 3 (fully into it) ──

        "moan.speed3.fj": [
            _("I can't believe how hard you are just from my feet..."),

            _("I didn't think I'd ever get into this, but..."),

            _("You're throbbing so much between my soles..."),

            _("My feet are doing this to you... that's kind of hot."),

        ],

        # ── Girl orgasm (surprised she came from this) ──

        "girl_cum.fj": [
            _("Wait... am I... from THIS?! Oh god..."),

            _("My toes are curling and I... I can't believe I'm cumming from a footjob!"),

            _("You're making me... just from my feet... AAAH!"),

        ],

        "girl_post_cum.fj": [
            _("I just came from giving you a footjob. What is my life."),

            _("My feet are still tingling... that was unexpected."),

        ],

        "girl_cum_hard.fj": [
            _("My whole body is... just from my FEET?! AAAAAH!"),

            _("I can't... my toes... everything is... AAAAAAH!"),

            _("How am I cumming THIS hard from a footjob?! AAAH!"),

        ],

        "girl_post_cum_hard.fj": [
            _("I think I broke something... my feet are still twitching..."),

            _("I've never cum like that. And it was from my FEET. What."),

        ],

        # ── Player cum ──

        "cum_outside.fj": [
            _("Oh! All over my legs..."),

            _("That was a lot... it's dripping everywhere."),

            _("Mmm... you really held back, didn't you?"),

        ],

        "cum_feet.fj": [
            _("You got it all over my feet... that's so warm."),

            _("On my FEET?! I can feel it between my toes..."),

            _("So that's what that feels like... it's actually not that bad."),

            _("My feet are covered... you really do have a thing for this."),

        ],

    }

    # ============================================================
    # SMART LINE PICKER
    # ============================================================

    # Scenes that share another scene's line pools. Her HISTORY is still read from the real scene.
    _SCENE_LINE_ALIAS = {
        "reverse_cowgirl": "cowgirl",
        "reverse_cowgirl_anal": "anal",
        "full_nelson_anal": "anal",
        "laying_anal": "anal",
        "laying_down": "doggy",
    }

    def _detect_line_modifiers(girl, scene=None, history_scene=None):
        """Build modifier list from girl's traits and context.
        `scene` picks the line pools (may be an alias); `history_scene` is what is really happening and
        is what her history is read from (a girl who only does laying down is not a doggy first-timer)."""
        mods = []
        if not girl:
            return mods

        mods.append(girl.gid)
        # her stage on the turn of a canon femdom ("femdom_s2" / "femdom_s3", femdom_turn.rpy): key.scene.<gid>.<stage>
        _stage_mod = femdom_stage_mod(girl)
        if _stage_mod:
            mods.append(_stage_mod)

        # Comfort gate: explicit personality traits need minimum relationship
        _love = getattr(girl, "Love", 0)
        _inbt = getattr(girl, "Inbt", 0)
        _comfortable = (_love >= 300 or _inbt >= 200)

        # Eager traits: "<mod>_first" (her very first time) / "<mod>_new" (her first few) come before the veteran pools
        if girl.has_trait("cum_slut") and _comfortable:
            mods.extend(trait_discovery_keys(girl, "cum_slut"))
            mods.append("cum_slut")
        if girl.has_trait("hate_cum") and not getattr(store, "condom_active", False):
            _phase = getattr(store, "_scene_phase", None)
            if _phase not in ("rub", "oral", "masturbate", "secret_masturbate"):
                if trait_is_new(girl, "hate_cum"):
                    mods.append("hate_cum_new")
                mods.append("hate_cum")
        # camera_lover lines only play when actually recording;
        # otherwise she acts normal (trait revealed through enthusiasm
        # when player initiates recording, or she asks after enough sex acts)
        if girl.has_trait("camera_lover") and getattr(store, "_recording_active", False):
            mods.append("camera_lover")
        if girl.has_trait("camera_hater"):
            mods.append("camera_hater")
        # Control before hardcore: hardcore is pace and slaps, who gives the orders is femdom / submissive
        # (docs/plan_femdom.md D3). femdom has a discovery phase (D7); submissive has none. Same comfort gate as
        # hardcore (many of these pools came from it).
        if girl.has_trait("femdom") and _comfortable:
            mods.extend(trait_discovery_keys(girl, "femdom"))
            mods.append("femdom")
        if girl.has_trait("submissive") and _comfortable:
            mods.append("submissive")
        if girl.has_trait("hardcore_sex") and _comfortable:
            mods.extend(trait_discovery_keys(girl, "hardcore_sex", "hardcore"))
            mods.append("hardcore")
        if girl.has_trait("cute_sex"):
            if trait_is_new(girl, "cute_sex"):
                mods.append("cute_new")
            mods.append("cute")
        if girl.has_trait("nerd"):
            mods.append("nerd")
        if girl.has_trait("lesbian"):
            mods.append("lesbian")
            _proof = lesbian_openness(girl)
            if _proof >= 76:
                mods.append("lesbian_accepted")
            elif _proof >= 51:
                mods.append("lesbian_conflict")
            elif _proof >= 26:
                mods.append("lesbian_confused")
            else:
                mods.append("lesbian_denial")
        if girl.has_trait("public_fetish") and getattr(store, "_crowd_level", 0) > 0:
            mods.append("public_fetish")
        if girl.has_trait("public_shy") and getattr(store, "_crowd_level", 0) > 0:
            mods.append("public_shy")
        if girl.has_trait("anal_lover"):
            mods.extend(trait_discovery_keys(girl, "anal_lover"))
            mods.append("anal_lover")
        if girl.has_trait("anal_hater"):
            if trait_is_new(girl, "anal_hater"):
                mods.append("anal_hater_new")
            mods.append("anal_hater")
        _ap = getattr(girl, "_anal_preference", 0)
        if _ap >= 3:
            mods.append("anal_addicted")
        if _ap >= 2:
            mods.append("anal_preferring")
        if getattr(store, "_atm_cum_in_mouth", False):
            mods.append("atm")
        if girl.has_trait("virgin") and getattr(store, "_scene_phase", None) not in ("tip", "rub", "masturbate"):
            mods.append("virgin")
        if getattr(store, "_lost_virginity_this_scene", False):
            mods.append("virgin_lost")
        if hasattr(girl, "has_npc_partner") and girl.has_npc_partner():
            _npc_here = get_npc_partner_for(girl) if callable(getattr(store, "get_npc_partner_for", None)) else None
            _npc_physically_present = (_npc_here is not None and _npc_here is getattr(store, "_npc_on_scene", None))
            if not _npc_physically_present:
                if girl.get_flag("partner_is_female"):
                    if girl.has_trait("bisexual"):
                        mods.append("bisexual_gf")
                    else:
                        mods.append("girlfriend")
                else:
                    mods.append("boyfriend")
            if girl.has_trait("cheater"):
                mods.append("cheater")
            elif girl.has_trait("loyal"):
                mods.append("loyal")
            if hasattr(girl, "bf_has_done") and girl.bf_has_done("sex"):
                if girl.get_flag("partner_is_female"):
                    mods.append("girlfriend_sex")
                else:
                    mods.append("boyfriend_sex")
        if getattr(store, "_crowd_level", 0) > 0:
            mods.append("public")
        if getattr(store, "_ntr_partner_watching", False) and getattr(store, "_ntr_watching_npc", None) is not None:
            # Case 2: NTR partner is actively watching right now.
            mods.append("partner_watching")
        elif hasattr(girl, "has_npc_partner") and girl.has_npc_partner():
            _npc_catch = getattr(girl, "_npc_catch_count", 0)
            _npc_susp = 0
            _rec_npc = get_npc_partner_for(girl) if callable(getattr(store, "get_npc_partner_for", None)) else None
            if _rec_npc:
                _npc_susp = getattr(_rec_npc, "suspicion", 0)
            # Male partner only for now — the ntr_known pools are boyfriend-flavored.
            # (Female-partner NTR would need its own girlfriend-flavored variants.)
            _ntr_known_here = (_rec_npc is not None and getattr(_rec_npc, "_ntr_active", False)
                               and getattr(girl, "_ntr_boundary_discovered", False)
                               and not girl.get_flag("partner_is_female"))
            if _ntr_known_here:
                # Case 1: NTR partner already knows and permits this, but isn't in the room.
                # Not secret cheating (no "if he finds out" guilt) and not being watched.
                mods.append("ntr_known")
            elif _npc_catch > 0 or _npc_susp >= 50 or (getattr(_rec_npc, "_ntr_active", False) if _rec_npc else False):
                mods.append("partner_caught")

        # Player is cheating: has a girlfriend but this girl is NOT her (skip if harem-exempt)
        if hasattr(girl, "is_dating_player") and not girl.is_dating_player():
            if player_has_girlfriend(store.ALL_GIRLS) and not is_player_harem_exempt(girl):
                mods.append("player_cheating")

        # Ex-girlfriend context
        if getattr(girl, "Player_status", "none") == "ex":
            mods.append("ex")
            _ex_hist = getattr(girl, "ex_player_history", None) or {}
            _ex_mood = _ex_hist.get("breakup_mood", "sad")
            mods.append("ex_angry" if _ex_mood == "angry" else "ex_sad")

        # GF present: player's girlfriend is at the same location (skip if harem-exempt)
        if hasattr(girl, "is_dating_player") and not girl.is_dating_player():
            _gf = get_player_girlfriend(store.ALL_GIRLS) if callable(get_player_girlfriend) else None
            if _gf is not None and _gf is not girl:
                _cloc = getattr(store, "CurrentLocation", None)
                if _cloc is not None and getattr(_gf, "loc", None) == _cloc:
                    if not is_harem_exempt(_gf, girl):
                        mods.append("gf_present")

        # Both cheating: girl has partner AND player has gf
        if ("boyfriend" in mods or "girlfriend" in mods) and "player_cheating" in mods:
            mods.append("both_cheating")

        # Partner loyalty tiers — only for BF (male partner).
        # Girls with a girlfriend use lesbian/girlfriend modifiers instead.
        if "boyfriend" in mods and hasattr(girl, "bf_loyalty_tier"):
            _bfl_tier = girl.bf_loyalty_tier()
            if _bfl_tier == "miserable":
                mods.append("bf_miserable")
            elif _bfl_tier == "strained":
                mods.append("bf_strained")
            elif _bfl_tier == "in_love":
                mods.append("bf_in_love")

        # GF-like tiers (how she feels about the player's GF — affects tone when helping player cheat)
        if "player_cheating" in mods:
            _gf = get_player_girlfriend(store.ALL_GIRLS) if callable(get_player_girlfriend) else None
            if _gf and hasattr(girl, "gf_like_tier"):
                _glt = girl.gf_like_tier(_gf.gid)
                if _glt == "close":
                    mods.append("gf_close")
                elif _glt == "distant":
                    mods.append("gf_distant")
                elif _glt == "hostile":
                    mods.append("gf_hostile")

        # Per-act veteran: done this specific act / position 5+ times
        if scene:
            if girl_type_count(girl, history_scene or scene) >= 5:
                mods.append("act_veteran")

        # first_time vs recurring (for sex scenes): before he ever got inside her, and the whole day he first did
        # (_first_sex_day, mark_intimacy: once "sex" is in her flags the old rule went silent on that very day)
        if ((getattr(girl, "raw_sex_count", 0) == 0 and "sex" not in getattr(girl, "intimacy_flags", set()))
                or getattr(girl, "_first_sex_day", None) == store.Day):
            mods.append("first_time")
        elif getattr(girl, "raw_sex_count", 0) >= 5:
            mods.append("recurring")

        # Recording history (video already appended before scene_pick_line runs)
        _girl_rec_count = sum(1 for v in getattr(store.Player, "recorded_videos", []) if v.get("girl_gid") == getattr(girl, "gid", ""))
        if _girl_rec_count <= 1:
            mods.append("recording_first")
        elif _girl_rec_count >= 4:
            mods.append("recording_recurring")

        # Per-act first time: girl has never done THIS specific act with the player
        # "inexperienced": act_first AND boyfriend never did it either
        if scene:
            _flags = getattr(girl, "intimacy_flags", set()) or set()
            # the real scene, not its line alias; an anal variant is the "anal" act in her flags
            _act_key = history_scene or scene
            if _act_key in _ANAL_SCENE_TYPES:
                _act_key = "anal"
            if _act_key not in _flags:
                mods.append("act_first")
                # bf_history has no position data: any vaginal position is just "sex" there
                _bf_key = scene_type_act(_act_key)
                _bf_done = girl.bf_has_done(_bf_key) if hasattr(girl, "bf_has_done") else False
                if not _bf_done:
                    mods.append("inexperienced")

        # Session orgasm count (repeated climax reactions)
        # NOTE: counter increments AFTER dialogue in GirlCumming, so
        # _so >= 1 means this is the 2nd orgasm, _so >= 2 means 3rd+
        _so = store._session_orgasms_by_girl.get(getattr(girl, "gid", ""), 0)
        if _so >= 2:
            mods.append("orgasm_3rd_plus")
        elif _so >= 1:
            mods.append("orgasm_2nd")

        # Session creampie count
        _sc = store._session_cum.get("inside", 0)
        if _sc >= 3:
            mods.append("session_3rd_plus")
        elif _sc >= 2:
            mods.append("session_2nd")
        # Lifetime creampie milestones
        _cc = getattr(girl, "CreampieCounts", 0)
        if _cc >= 10:
            mods.append("cream_veteran")
        elif _cc >= 5:
            mods.append("cream_experienced")
        # hate_cum creampie escalation tiers
        # NOTE: process_cum increments CreampieCounts BEFORE scene_pick_line
        # runs, so thresholds are +1 to match the *previous* count.
        # hc_tier1 = 2nd creampie, hc_tier2 = 3rd-4th, hc_tier4 = 5th+
        if girl.has_trait("hate_cum") and _cc >= 5:
            mods.append("hc_tier4")
        elif girl.has_trait("hate_cum") and _cc >= 3:
            mods.append("hc_tier2")
        elif girl.has_trait("hate_cum") and _cc >= 2:
            mods.append("hc_tier1")

        # Condom break: hidden break + cum inside this scene
        if getattr(store, "_scene_condom_break", False):
            mods.append("condom_break")

        # First-ever creampie (CreampieCounts went from 0 to 1 this session)
        if _cc == 1 and getattr(store, "_session_cum", {}).get("inside", 0) >= 1:
            mods.append("first_creampie")

        # Coercion context: scene was started via blackmail or financial coercion
        _ct = getattr(store, "_coercion_type", None)
        if _ct == "blackmail":
            mods.append("blackmailed")
        elif _ct == "financial":
            mods.append("paid")

        if getattr(store, "_threesome_mode", False):
            _ts_watcher = getattr(store, "_witness_girl", None)
            _ts_is_gf = (_ts_watcher is not None and hasattr(_ts_watcher, "is_dating_player") and _ts_watcher.is_dating_player())
            if _ts_is_gf:
                mods.append("threesome")
            else:
                mods.append("threesome_nongf")

        return mods

    # Map modifier names → discover keys (only trait-revealing ones)
    _MOD_DISCOVER_MAP = {
        "cum_slut":      "discovered_trait_cum_slut",
        "hate_cum":      "discovered_trait_hate_cum",
        "camera_lover":  "discovered_trait_camera_lover",
        "camera_hater":  "discovered_trait_camera_hater",
        "hardcore":      "discovered_trait_hardcore_sex",
        "cute":          "discovered_trait_cute_sex",
        "femdom":        "discovered_trait_femdom",
        "femdom_new":    "discovered_trait_femdom",
        "femdom_first":  "discovered_trait_femdom",
        "submissive":    "discovered_trait_submissive",
        "public_fetish": "discovered_trait_public_fetish",
        "public_shy":    "discovered_trait_public_shy",
        "virgin":        "discovered_trait_virgin",
        "virgin_lost":   "discovered_virgin",
        "cheater":       "discovered_trait_cheater",
        "loyal":         "discovered_trait_loyal",
        "anal_lover":    "discovered_trait_anal_lover",
        "anal_lover_new":"discovered_trait_anal_lover",
        "anal_hater":    "discovered_trait_anal_hater",
        "anal_hater_new":"discovered_trait_anal_hater",
        "cum_slut_new":  "discovered_trait_cum_slut",
        "hate_cum_new":  "discovered_trait_hate_cum",
        "hardcore_new":  "discovered_trait_hardcore_sex",
        "cute_new":      "discovered_trait_cute_sex",
        "cum_slut_first":   "discovered_trait_cum_slut",
        "hardcore_first":   "discovered_trait_hardcore_sex",
        "anal_lover_first": "discovered_trait_anal_lover",
        # audit 2026-10-04: these modifiers are the trait showing too and never discovered
        "femdom_s2":        "discovered_trait_femdom",
        "femdom_s3":        "discovered_trait_femdom",
        "nerd":             "discovered_trait_nerd",
        "lesbian":          "discovered_trait_lesbian",
        "lesbian_accepted": "discovered_trait_lesbian",
        "lesbian_conflict": "discovered_trait_lesbian",
        "lesbian_confused": "discovered_trait_lesbian",
        "lesbian_denial":   "discovered_trait_lesbian",
        "bisexual_gf":      "discovered_trait_bisexual",
    }

    # Base keys whose lines are too subtle/generic to reveal a trait
    _NO_AUTO_DISCOVER = {"dressup"}

    # Eager traits: their veteran pools talk like an old habit ("I NEED your cum inside me", "my ass is aching for
    # your cock"). While she is still discovering one of them ("<trait>_first" / "<trait>_new", trait_discovery_keys)
    # and one of those discovery pools answers the moment, it speaks before ANY veteran eager pool: a 2-modifier
    # combo or her other eager trait ("girl_cum.anal.cum_slut" on the first anal of a cum_slut + anal_lover) used to
    # win and made a first-timer sound like an addict. The negative traits (hate_cum, anal_hater, cute) stay out:
    # dread needs no experience.
    _EAGER_TRAIT_MODS = ("cum_slut", "hardcore", "anal_lover", "femdom")
    _DISCOVERY_STAGES = ("_first", "_new")   # most specific first
    _EAGER_NEW_MODS = tuple(_m + _s for _m in _EAGER_TRAIT_MODS for _s in _DISCOVERY_STAGES)

    def scene_pick_line(key, scene=None, girl=None):
        """
        Smart line picker with hierarchical fallback: the most specific pool with lines wins (author's rule),
        among the pools that are TRUE for this moment. The scene comes first because it is physical: a pool
        without the scene is written for penetration ("fuck me harder", "fill my pussy") and would be wrong in a
        BJ or in anal, where the scene's own pool exists. Her gid is the first modifier, so her pools lead each step.
        Priority (most specific first):
          key.scene.mod1.mod2 → key.scene.mod → key.scene →
          key.mod1.mod2 → key.mod → key
        A per-girl line that must win over the scene's generic pool is written WITH the scene
        (key.scene.<gid>, key.scene.<gid>.<trait>).
        Returns a random line from the best matching pool, or None.
        Auto-fires girl.discover() when a trait-specific line is chosen.
        """
        # RCG shares cowgirl dialogue (both are riding positions), laying down shares doggy...
        _history_scene = scene
        scene = _SCENE_LINE_ALIAS.get(scene, scene)

        # Pregnancy layer (Actions/pregnancy.rpy): trait / protection-state lines take a share of
        # the moans and cum moments in vaginal scenes. Returns None most of the time.
        if callable(globals().get("fert_scene_line", None)):
            _fert_line = fert_scene_line(key, scene, girl)
            if _fert_line:
                return _fert_line

        # Cross-girl ATM layer (Dialogs/atm_cross.rpy): in a threesome it was in the OTHER girl's ass, so
        # the ".atm" pools below ("straight from my ass") would be wrong. Her voice + her traits.
        if callable(globals().get("atm_cross_scene_line", None)):
            _atm_x_line = atm_cross_scene_line(key, scene, girl)
            if _atm_x_line:
                return _atm_x_line

        modifiers = _detect_line_modifiers(girl, scene=scene, history_scene=_history_scene)

        # The camera_hater pools are written for a scene NOBODY records ("promise me no cameras", "thank god this
        # isn't on camera"). While a recording runs (his phone, the tripod or the watching girl's phone) they only
        # fit her reaction to the camera itself (record_accepted / record_denied).
        if "camera_hater" in modifiers and getattr(store, "_recording_active", False) and not key.startswith("record_"):
            modifiers = [m for m in modifiers if m != "camera_hater"]
            print("[SCENE_LINE] %s: camera_hater lines skipped for '%s' (a recording is running)" % (getattr(girl, "gid", "?"), key))

        # "dressup.first_time" ("That was... my first time. Wow.") is said dressing after her FIRST SEX. The bare
        # first_time modifier also means "no sex yet", which fit every undressed session before it: Tenny said it
        # after every massage (tester 2026-10-11). Only the day he first got inside her (_first_sex_day).
        if key == "dressup" and "first_time" in modifiers and getattr(girl, "_first_sex_day", None) != store.Day:
            modifiers = [m for m in modifiers if m != "first_time"]
            print("[SCENE_LINE] %s: dressup.first_time skipped (no sex today: not her first time)" % getattr(girl, "gid", "?"))

        candidates = []  # (lookup_key, list_of_matched_mods)

        # 1) key.scene.mod1.mod2  (2-modifier combos, scene-specific)
        if scene and len(modifiers) >= 2:
            for i in range(len(modifiers)):
                for j in range(i + 1, len(modifiers)):
                    m1, m2 = modifiers[i], modifiers[j]
                    candidates.append(("%s.%s.%s.%s" % (key, scene, m1, m2), [m1, m2]))
                    candidates.append(("%s.%s.%s.%s" % (key, scene, m2, m1), [m2, m1]))

        # 2) key.scene.mod  (single modifier, scene-specific)
        _lifted = set()   # an eager trait's generic discovery pools pulled up here (the eager rule below reads it)
        for mod in modifiers:
            if scene:
                # She is still discovering this trait ("<trait>_first" / "<trait>_new" is on) and this pose only has a
                # VETERAN pool for it: her generic discovery pools outrank the veteran pose pool (a pose twin
                # key.scene.<trait>_first / _new, when it exists, already came first: _detect_line_modifiers puts
                # the discovery modifiers before "<trait>").
                if SCENE_LINES.get("%s.%s.%s" % (key, scene, mod)):
                    for _stage in _DISCOVERY_STAGES:
                        if (mod + _stage) in modifiers:
                            candidates.append(("%s.%s%s" % (key, mod, _stage), [mod + _stage]))
                            if mod in _EAGER_TRAIT_MODS:
                                _lifted.add("%s.%s%s" % (key, mod, _stage))
                candidates.append(("%s.%s.%s" % (key, scene, mod), [mod]))

        # 3) key.scene
        if scene:
            candidates.append(("%s.%s" % (key, scene), []))

        # 4) key.mod1.mod2  (2-modifier combos, no scene)
        if len(modifiers) >= 2:
            for i in range(len(modifiers)):
                for j in range(i + 1, len(modifiers)):
                    m1, m2 = modifiers[i], modifiers[j]
                    candidates.append(("%s.%s.%s" % (key, m1, m2), [m1, m2]))
                    candidates.append(("%s.%s.%s" % (key, m2, m1), [m2, m1]))

        # 5) key.mod  (single modifier, no scene)
        for mod in modifiers:
            candidates.append(("%s.%s" % (key, mod), [mod]))

        # 6) Generic fallback: key
        candidates.append((key, []))

        _pw_active = "partner_watching" in modifiers
        _ntrk_active = "ntr_known" in modifiers
        _ts_active = "threesome" in modifiers

        def _pool_blocked(matched_mods):
            # When the partner is watching OR already knows and permits this (NTR),
            # skip the secret boyfriend/girlfriend pools (those assume he can't know).
            if (_pw_active or _ntrk_active) and ("boyfriend" in matched_mods or "girlfriend" in matched_mods or "bisexual_gf" in matched_mods) and "partner_watching" not in matched_mods and "ntr_known" not in matched_mods:
                return True
            # In threesome mode, skip player_cheating pools (GF is present and approved)
            if _ts_active and "player_cheating" in matched_mods and "threesome" not in matched_mods:
                return True
            return False

        _answers = [(ck, mm) for ck, mm in candidates if SCENE_LINES.get(ck) and not _pool_blocked(mm)]
        if not _answers:
            return None
        # Still discovering an eager trait and one of its "_first" / "_new" pools answers: no veteran eager pool speaks
        # first, except her own ones ("girl_cum.anal.tenny.anal_lover": her voice, written for her). A discovery pool
        # written for this pose (her first anal) also outranks another trait's generic one pulled up in step 2.
        if any(m in _EAGER_NEW_MODS for _ck, _mm in _answers for m in _mm):
            _gid = getattr(girl, "gid", None)
            _fresh = [(ck, mm) for ck, mm in _answers if _gid in mm or not any(m in _EAGER_TRAIT_MODS for m in mm)]
            if scene and any(ck.startswith("%s.%s." % (key, scene)) and any(m in _EAGER_NEW_MODS for m in mm) for ck, mm in _fresh):
                _fresh = [(ck, mm) for ck, mm in _fresh if ck not in _lifted]
            if _fresh and _fresh[0][0] != _answers[0][0]:
                print("[SCENE_LINE] %s still new (%s): '%s' plays instead of '%s'" % (
                    _gid, ", ".join(m for m in modifiers if m in _EAGER_NEW_MODS), _fresh[0][0], _answers[0][0]))
            _answers = _fresh or _answers

        ck, matched_mods = _answers[0]
        pool = SCENE_LINES[ck]
        # Fire discover for each trait-specific modifier used
        if matched_mods and girl and key not in _NO_AUTO_DISCOVER:
            for mm in matched_mods:
                if mm in _MOD_DISCOVER_MAP and hasattr(girl, "discover"):
                    girl.discover(_MOD_DISCOVER_MAP[mm])
        # pregnancy.rpy truth filter: "I'm not on the pill!" only plays while it is true
        if callable(globals().get("fert_pick_truthful", None)):
            line = fert_pick_truthful(girl, pool)
        else:
            line = renpy.random.choice(pool)
        if line and girl and "%(" in line and hasattr(girl, "has_npc_partner") and girl.has_npc_partner():
            line = _format_partner_line(girl, line)
        return line

    # ============================================================
    # MOAN TICK — Random mid-scene flavor dialogue
    # ============================================================

    def scene_moan_tick(girl, scene_type, speed):
        """
        Random chance to pick a moan line during an action tick.
        Higher speed -> higher chance.  2-tick cooldown after firing.
        Returns the line string if one was picked (caller must display via _moan_say),
        or None if nothing fired.
        """
        if _ts_watcher_jealousy_tick(girl, scene_type):
            return None
        # Her NTR partner is in the room AND looking (not the bet's back-turned phase). The pool talks about the
        # ACTIVE girl's partner, so after a threesome switch it only fires while she is the one he came with.
        if _tease_partner_watching() and getattr(getattr(store, "_ntr_watching_npc", None), "girl_gid", None) == girl.gid:
            if renpy.random.random() < 0.15 and _watcher_scene_comment("ntr_watching", active_girl=girl):
                return None

        if speed <= 0:
            return None

        if scene_type in ("rub", "tip"):
            return None

        store._moan_cooldown = getattr(store, "_moan_cooldown", 0) - 1
        if store._moan_cooldown > 0:
            return None

        # Anal preference: vaginal complaint replaces the moan 15% of the time
        if girl and getattr(girl, "_anal_preference", 0) >= 2 and scene_type not in _ANAL_SCENE_TYPES:
            if renpy.random.random() < 0.15:
                _vc = scene_pick_line("vaginal_complaint", scene=scene_type, girl=girl)
                if _vc:
                    store._moan_cooldown = 3
                    return _vc

        chance = {1: 20, 2: 30, 3: 40}.get(speed, 20)
        if girl and girl.has_trait("lesbian"):
            chance = min(80, chance + 20)
        _roll = renpy.random.randint(1, 100)
        if _roll > chance:
            return None

        key = "moan.speed%d" % speed
        line = scene_pick_line(key, scene=scene_type, girl=girl)
        debug_log("[MOAN] key=%s scene=%s girl=%s lesbian=%s line=%s" % (key, scene_type, girl.gid, girl.has_trait("lesbian"), line[:40] if line else "None"))
        if line:
            store._moan_cooldown = 2
            return line
        return None
