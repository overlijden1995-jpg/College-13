# ============================================================
# exam.rpy
# Bi-weekly exam... fires every 2 weeks on Friday at Midday.
# Game starts on Sunday (Day 1). First exam: Day 13.
# Subsequent: Day 27, 41, 55 …
#
# American grading scale:
#   A  10+    B  7–9    C  5–6    D  3–4    F  0–2
#
# Exam invite varies by Love (and Inbt for the skip option):
#   Love < 300          → she just informs the player she's leaving
#   300 ≤ Love < 600    → she invites the player to come with her
#   Love ≥ 600          → she insists they both go
#   Love ≥ 600 + Inbt ≥ 500 → player can try to convince her to skip
#
# The player's grade always goes through exam_record_grade: the exam he took, the exam he skipped at the prompt
# (F) and an exam whose slot passed without the prompt (F, exam_missed_check from label Wait), as the professor
# promised. His family hears about every grade (family_on_exam_grade, family_grades.rpy).
# ============================================================

default _exam_last_day = None       # the last exam day whose grade is recorded (None: a save from before, exam_sync)

init 1 python:

    EXAM_FIRST_DAY  = 13
    EXAM_INTERVAL   = 14
    EXAM_TIME_INDEX = TIME_NAMES.index("Midday")   # second slot

    # ---- calendar helpers ------------------------------------

    def days_until_exam(day, time_index=0):
        if day < EXAM_FIRST_DAY:
            return EXAM_FIRST_DAY - day
        elapsed   = day - EXAM_FIRST_DAY
        remainder = elapsed % EXAM_INTERVAL
        if remainder == 0:
            if time_index > EXAM_TIME_INDEX:
                return EXAM_INTERVAL   # exam already happened today
            return 0
        return EXAM_INTERVAL - remainder

    def is_exam_slot(day, time_index):
        if day < EXAM_FIRST_DAY:
            return False
        return (time_index == EXAM_TIME_INDEX and
                (day - EXAM_FIRST_DAY) % EXAM_INTERVAL == 0)

    def exam_countdown_text():
        """The next exam, for the HUD's time card and the phone status (translated): urgent at 3 days
        or less (red / yellow), calm the rest of the cycle (color None: the surface's own gray).
        Always something (author 2026-10-11: the HUD line used to exist only at 3 days or less,
        so most of the cycle showed nothing at all)."""
        _n = days_until_exam(store.Day, store.TimeIndex)
        if _n == 0:
            return (_tl(_("Exam today at noon")), "#f87171")
        if _n == 1:
            return (_tl(_("Exam tomorrow")), "#facc15")
        if _n <= 3:
            return (_tl(_("Exam in %d days")) % _n, "#facc15")
        if _n <= 7:
            return (_tl(_("Exam this Friday")), None)
        if _n <= 13:
            return (_tl(_("Exam next week")), None)
        return (_tl(_("Exam in two weeks")), None)

    # ---- grade helpers ---------------------------------------

    def study_grade(level):
        if level >= 10: return "A"
        if level >= 7:  return "B"
        if level >= 5:  return "C"
        if level >= 3:  return "D"
        return "F"

    def exam_expression(grade):
        if grade in ("A", "B"): return "smile"
        if grade in ("C", "D"): return "normal"
        return "sad"

    # ---- the player's grades ---------------------------------

    def exam_days_passed(after, day=None, ti=None):
        """Exam days later than `after` whose exam slot is over at (day, ti), now by default."""
        _d = store.Day if day is None else day
        _ti = store.TimeIndex if ti is None else ti
        _out = []
        _e = EXAM_FIRST_DAY
        while _e < _d or (_e == _d and _ti > EXAM_TIME_INDEX):
            if _e > after:
                _out.append(_e)
            _e += EXAM_INTERVAL
        return _out

    def exam_sync(why):
        """New game and every load: a save from before _exam_last_day counts from the last exam already over (no F
        for the exams of the past)."""
        if store._exam_last_day is None:
            _past = exam_days_passed(0)
            store._exam_last_day = _past[-1] if _past else 0
            print("[EXAM] %s: exams counted from Day %d" % (why, store._exam_last_day))

    def exam_record_grade(grade, why, day=None):
        """The player's grade of an exam: taken ("exam"), skipped at the prompt ("skipped": F) or missed without
        the prompt ("missed": F). grade_history, the day of that exam, then his family hears about it."""
        _day = store.Day if day is None else day
        if getattr(store.Player, "grade_history", None) is None:
            store.Player.grade_history = []
        store.Player.grade_history.append(grade)
        store._exam_last_day = max(store._exam_last_day or 0, _day)
        print("[EXAM] Player grade: %s (%s, exam of Day %d; history: %s)" % (grade, why, _day, store.Player.grade_history))
        family_on_exam_grade(grade, why, _day)

    def exam_missed_check():
        """label Wait: an exam slot that passed with no prompt (he slept through the Friday, a scene took the
        slot) is an F."""
        if store._exam_last_day is None:
            exam_sync("check")
        for _e in exam_days_passed(store._exam_last_day):
            exam_record_grade("F", "missed", _e)

    # ---- shared phrase pools (randomly picked each time) ------
    # Each key has at least 3 lines. Add more freely.

    _EXAM_POOLS = {

        # Low Love... she just informs the player and leaves
        "inform": [
            _("I'm heading to the exam. See you around."),
            "Exam's starting. I'm going.",
            _("Time for the exam. Catch you later."),
            _("I can't be late. Exam's about to start."),
        ],

        # Medium Love... she invites the player
        "invite": [
            _("The exam's about to start. Want to come with me?"),
            _("Hey, we should head to the exam. Coming?"),
            _("Shouldn't we be in class right now? Come on."),
            _("Exam time. You going or not?"),
        ],

        # Medium Love... player declined the invite (sad)
        "skip_mid": [
            _("Okay… I'll see you later then."),
            _("Alright. Don't fail on your own."),
            _("Fine. I'll save you a seat. Oh wait."),
        ],

        # High Love... she insists they both go
        "insist": [
            _("Come on, we can't miss this. Let's go... now."),
            _("We're both going to that exam. That's not up for debate."),
            _("I'm not going without you. Move."),
            _("Don't make me drag you there."),
        ],

        # High Love... player refused despite insisting (angry)
        "skip_high": [
            _("Fine! But don't expect me to cover for you."),
            _("I can't believe you right now. I'm going."),
            _("Your loss. Don't come to me about your grade."),
        ],

        # Convince flow... she hesitates
        "tempted": [
            _("I… but what about the exam? We'll be in so much trouble…"),
            _("Are you serious? We can't just skip…"),
            _("That's actually tempting. But what if we get caught?"),
        ],

        # Convince flow... she agrees to skip
        "convinced": [
            _("Fine… but we study twice as hard next time. Promise me."),
            _("This is such a bad idea. …Let's do it."),
            _("Okay. But this is entirely your fault."),
        ],

        # Convince flow... player backs out, they go to the exam
        "not_skip": [
            _("Good. Let's not throw our grades away."),
            _("Thought so. Come on, we'll be late."),
            _("Smart choice. Let's go."),
        ],

        # Exam-day reaction... studied a lot (A/B)
        "react_high": [
            _("I actually read every chapter. Twice. I'm so ready."),
            _("I've been preparing all week. Bring it on."),
            _("I feel really good about this one."),
            _("I've reviewed everything. Not worried at all."),
        ],

        # Exam-day reaction... studied a bit (C/D)
        "react_mid": [
            _("I covered the main topics… I think that counts."),
            _("I know the important parts. I'll improvise the rest."),
            _("I'm like sixty percent prepared. That's passing, right?"),
            _("Should be fine… probably. Right?"),
        ],

        # Exam-day reaction... barely studied (F)
        "react_low": [
            _("Let's just get this over with."),
            _("I didn't study nearly enough. This is going to hurt."),
            _("I'm going to wing it and hope for the best."),
            _("Don't ask me how prepared I am. Just… don't."),
        ],
    }

    def _exam_pick(key):
        """Pick a random line from the shared phrase pool."""
        pool = _EXAM_POOLS.get(key, ["…"])
        return renpy.random.choice(pool)

    # ---- trait/relationship-aware exam overrides ----------------
    # Keys: (pool_key, trait_or_status) -> [lines]
    # Checked before falling back to generic _EXAM_POOLS.

    _EXAM_TRAIT_LINES = {
        # --- INFORM (low love) with traits ---
        ("inform", "hardcore_sex"): [
            _("Exam. I'm out. Try not to fail."),
            _("Time's up. I'm going. Don't be dead weight."),
        ],
        ("inform", "cute_sex"): [
            _("Um... the exam is starting. I-I'm heading over now..."),
            _("I need to go take the exam... good luck, okay?"),
        ],

        # --- INVITE (mid love) with traits ---
        ("invite", "cute_sex"): [
            _("Hey... want to walk to the exam together? I'm kind of nervous."),
            _("The exam is soon... can you come with me? I feel better when you're there."),
        ],
        # giving him orders is femdom, not hardcore (docs/plan_femdom.md D3)
        ("invite", "femdom"): [
            _("Exam's up. Let's go crush it. Move."),
            _("Exam time. You're walking me there. I already decided."),
            _("Grab your stuff. You're coming with me to the exam."),
        ],
        ("invite", "hardcore_sex"): [
            _("Come on, exam time. I'm not waiting for you."),
            _("Exam's in ten. I'm running there. Race you?"),
        ],
        ("invite", "cheater"): [
            _("Exam time. Walk me there? My boyfriend said he'd be studying alone."),
            _("Let's go to the exam together. More fun than going alone, right?"),
        ],

        # --- INSIST (high love) with traits ---
        ("insist", "cute_sex"): [
            _("Please come with me! I can't do this alone!"),
            _("We have to go together! I promised myself we'd both pass!"),
        ],
        ("insist", "femdom"): [
            _("Get your ass up. We're going. No excuses."),
            _("Move. Now. I'm not letting you skip and drag me down."),
            _("Skipping isn't an option. I said we're going, so we're going."),
        ],
        ("insist", "hardcore_sex"): [
            _("Come on! I'm so pumped for this. Let's go tear that exam apart together."),
            _("Skip? Hell no. I'm fired up and I want you in there fighting with me."),
        ],

        # --- TEMPTED (skip convince) with traits ---
        ("tempted", "cheater"): [
            _("Skip the exam? That's a terrible idea... but I kind of love it."),
            _("My boyfriend would never let me skip... which makes me want to do it more."),
        ],
        ("tempted", "cute_sex"): [
            _("S-skip?! But what if we get in trouble? What if they call our parents?!"),
            _("We can't! ...Can we? No! ...Maybe?"),
        ],
        ("tempted", "hardcore_sex"): [
            _("Skip? Tch. Fine. But if we fail, that's on you."),
            _("You better make it worth my time if we're ditching."),
        ],

        # --- CONVINCED (agreed to skip) with traits ---
        ("convinced", "cheater"): [
            _("My boyfriend would kill me if he knew. ...Let's do it anyway."),
            _("This is so bad. I love it. What do we do instead?"),
        ],
        ("convinced", "cute_sex"): [
            _("Oh no oh no oh no... okay, fine! But we study EXTRA hard next time!"),
            _("I can't believe I'm doing this... hold my hand, I'm scared."),
        ],
        ("convinced", "virgin"): [
            _("This is the most rebellious thing I've ever done..."),
            _("I've never skipped anything before! My heart is racing!"),
        ],

        # --- REACT HIGH (well prepared) with traits ---
        ("react_high", "hardcore_sex"): [
            _("I didn't study this hard to get anything less than an A."),
            _("Bring it on. I've been preparing for war."),
        ],
        ("react_high", "cute_sex"): [
            _("I studied every night! I even made cute note cards!"),
            _("I'm nervous but I know this stuff! I color-coded everything!"),
        ],
        ("react_high", "cheater"): [
            _("I studied with my boyfriend... and maybe peeked at his notes."),
            _("I'm ready. I had... multiple study partners."),
        ],

        # --- REACT MID (somewhat prepared) with traits ---
        ("react_mid", "hardcore_sex"): [
            _("I know enough to pass. Good enough."),
            _("Not my best prep, but I'll power through it."),
        ],
        ("react_mid", "cute_sex"): [
            _("I tried my best... I hope it's enough..."),
            _("I studied the important parts! ...I think those were the important parts."),
        ],

        # --- REACT LOW (unprepared) with traits ---
        ("react_low", "hardcore_sex"): [
            _("Whatever. It's just a test. I'll survive."),
            _("If I fail, I fail. Life goes on."),
        ],
        ("react_low", "cute_sex"): [
            _("I'm going to cry. I didn't study at all..."),
            _("This is a disaster... I'm so sorry, I couldn't focus..."),
        ],
        ("react_low", "virgin"): [
            _("I got distracted by... things. I'm not ready at all."),
            _("I couldn't concentrate... my mind was elsewhere."),
        ],

        # ============ camera_lover ============

        ("inform", "camera_lover"): [
            _("Exam time! I hope someone's recording... I look great today."),
            _("Off to the exam. Maybe I'll vlog the walk there."),
        ],
        ("invite", "camera_lover"): [
            _("Exam's starting! Come with me... I need someone to film my victory walk."),
            _("Let's go! I want a before-and-after pic. Come on!"),
            _("Walk with me? I want to document this whole experience."),
        ],
        ("insist", "camera_lover"): [
            _("We're going. And you're filming my reaction when I ace it."),
            _("Come ON! I already told my followers we'd both pass!"),
        ],
        ("tempted", "camera_lover"): [
            _("Skip? But I already posted about studying all week... my followers will know!"),
            _("What if someone records us NOT being there? That's bad content!"),
            _("Hmm... we could vlog ourselves skipping. That's kind of edgy content, right?"),
        ],
        ("convinced", "camera_lover"): [
            _("Fine, but I'm documenting this. 'Skipping the exam' has viral potential."),
            _("Okay, but if anyone asks, we were doing a collab project. Smile for the camera!"),
        ],
        ("react_high", "camera_lover"): [
            _("I studied on camera every night! My followers watched me prepare!"),
            _("I'm SO ready! I even made aesthetic study montages!"),
            _("I filmed every study session. If I fail, the footage is useless!"),
        ],
        ("react_mid", "camera_lover"): [
            _("I spent more time making my notes look pretty for photos than actually reading them."),
            _("I think I know enough... at least enough to not embarrass myself on camera."),
        ],
        ("react_low", "camera_lover"): [
            _("I was too busy editing content to study. Priorities, right?"),
            _("Zero prep. But I'll look confident... that's half the battle on camera."),
        ],

        # ============ camera_hater ============

        ("inform", "camera_hater"): [
            _("Exam. I'm going. And if I see anyone with a phone out, I swear..."),
            _("Heading to the exam. At least no one films those."),
        ],
        ("invite", "camera_hater"): [
            _("Walk with me to the exam? I don't want to go past that hallway alone... people always have their phones out."),
            _("Exam time. Come with me? I feel safer when someone's blocking the view."),
            _("Let's go together. Just... don't take any pictures of me, okay?"),
        ],
        ("insist", "camera_hater"): [
            _("We're going. Walk on my left side... there are cameras on the right."),
            _("Let's go NOW before the hallways get crowded with phone zombies."),
        ],
        ("tempted", "camera_hater"): [
            _("Skip? ...At least there'd be fewer people around to see me."),
            _("That means no crowded classroom with everyone staring at their screens... tempting."),
            _("I hate the exam room. Everyone takes selfies after. It's a nightmare."),
        ],
        ("convinced", "camera_hater"): [
            _("Fine. At least I won't have to sit under those fluorescent lights where everyone can see me."),
            _("Okay. Anywhere with fewer phones pointed at me sounds good right now."),
        ],
        ("react_high", "camera_hater"): [
            _("I studied in my room with the curtains closed. Focused. Ready."),
            _("I know this material inside and out. Quietly prepared, no distractions."),
        ],
        ("react_mid", "camera_hater"): [
            _("I studied at home where no one could bother me. Covered the basics."),
            _("I prepared enough. Just want to get through it without anyone noticing me."),
        ],
        ("react_low", "camera_hater"): [
            _("I couldn't focus. Kept worrying about the seating arrangement instead of studying."),
            _("Barely studied. I'll sit in the back and keep my head down."),
        ],

        # ============ hate_cum ============

        ("inform", "hate_cum"): [
            _("Exam's starting. I need to wash my hands first... those desks are filthy."),
            _("Time for the exam. I swear, if anyone sneezes near me..."),
        ],
        ("invite", "hate_cum"): [
            _("Exam time. Come with me? I need someone to hold my bag while I sanitize the desk."),
            _("Let's go. And please tell me you washed your hands today."),
            _("Walk me to the exam? I need to get there early to wipe down my seat."),
        ],
        ("insist", "hate_cum"): [
            _("We're going. And bring hand sanitizer... I'm not touching those shared pencils."),
            _("Come on! I refuse to sit in a dirty classroom alone!"),
        ],
        ("tempted", "hate_cum"): [
            _("Skip? ...Those classrooms ARE disgusting after exams. Eraser shavings everywhere."),
            _("The exam room always smells weird and the desks are sticky. Maybe skipping isn't so bad."),
            _("Have you SEEN the state of those desks after an exam? Ugh... maybe we should skip."),
        ],
        ("convinced", "hate_cum"): [
            _("Fine. At least I won't have to touch those nasty shared materials."),
            _("Okay. Honestly? The thought of that grimy classroom was already making me sick."),
        ],
        ("react_high", "hate_cum"): [
            _("I studied in a perfectly clean environment. My notes are spotless. I'm ready."),
            _("Fully prepared. I even laminated my flash cards so they wouldn't get gross."),
        ],
        ("react_mid", "hate_cum"): [
            _("I studied a decent amount... between cleaning sessions."),
            _("I know the material okay. Just hoping the desk isn't sticky again."),
        ],
        ("react_low", "hate_cum"): [
            _("I spent more time cleaning my study space than actually studying."),
            _("Barely prepared. I couldn't focus... my notes got coffee-stained and I had to rewrite them."),
        ],

        # ============ loyal ============

        ("inform", "loyal"): [
            _("The exam is starting. I'd never miss it... it's our responsibility."),
            _("Time for the exam. I always show up. That's just who I am."),
        ],
        ("invite", "loyal"): [
            _("We should go to the exam together. It's the right thing to do."),
            _("Come on, let's head to the exam. I'd feel wrong going without you."),
            _("Exam time. We committed to this... let's follow through."),
        ],
        ("insist", "loyal"): [
            _("We made a commitment to our education. We're going. Both of us."),
            _("I'm not leaving you behind. We go together or not at all... and we ARE going."),
        ],
        ("tempted", "loyal"): [
            _("Skip? No. That's not who I am. ...Is it?"),
            _("I've never broken a commitment before. I don't know if I can start now."),
            _("Everything in me says we should go. But... you really want to skip?"),
        ],
        ("convinced", "loyal"): [
            _("I can't believe I'm agreeing to this. I've never skipped anything in my life."),
            _("This goes against everything I believe in. ...But I trust you. Don't make me regret it."),
        ],
        ("react_high", "loyal"): [
            _("I studied every single day. Consistency is everything."),
            _("I kept to my study schedule no matter what. I'm ready."),
            _("I promised myself I'd prepare properly, and I did."),
        ],
        ("react_mid", "loyal"): [
            _("I stuck to my plan mostly. A few gaps, but I showed up every session."),
            _("I did my best to stay committed to studying. Hopefully it's enough."),
        ],
        ("react_low", "loyal"): [
            _("I feel terrible. I had a plan and I didn't follow through."),
            _("I let myself down. I should have studied harder. I know better than this."),
        ],

        # ============ public_fetish ============

        ("inform", "public_fetish"): [
            _("Exam time. A whole room full of people... this should be interesting."),
            _("Off to the exam. Something about a crowded room gets my heart racing."),
        ],
        ("invite", "public_fetish"): [
            _("Let's go to the exam. All those people in one room... it's kind of exciting, isn't it?"),
            _("Come with me! I love the energy of a packed classroom."),
            _("Exam's starting. Walk with me? I want to feel the buzz of the crowd."),
        ],
        ("insist", "public_fetish"): [
            _("We're going! A room full of people, the tension, the pressure... I live for that!"),
            _("Come on! Don't you want to feel everyone's eyes when we walk in late?"),
        ],
        ("tempted", "public_fetish"): [
            _("Skip? But where's the thrill in hiding? ...Unless we do something risky instead."),
            _("The exam room is packed and tense... skipping means missing all that energy."),
            _("Hmm... but what if we skip and do something where we COULD get caught?"),
        ],
        ("convinced", "public_fetish"): [
            _("Fine... but only if we do something exciting. Not just hiding in a room."),
            _("Okay, skipping IS kind of thrilling. The risk of getting caught... I'm in."),
        ],
        ("react_high", "public_fetish"): [
            _("I studied in the library... surrounded by people. Best motivation ever."),
            _("I'm so ready. I even studied in the cafeteria during rush hour. Focused AND energized."),
        ],
        ("react_mid", "public_fetish"): [
            _("I studied a bit here and there... mostly in public spaces. Got distracted by the crowd sometimes."),
            _("I know some of it. Hard to focus when there are so many people around, you know?"),
        ],
        ("react_low", "public_fetish"): [
            _("I kept going to crowded places to 'study' but never actually opened my books."),
            _("Didn't study. I was too busy people-watching everywhere I went."),
        ],

        # ============ skip / not_skip overrides ============

        # -- camera_lover --
        ("skip_mid", "camera_lover"): [
            _("Fine... I'll post about acing it without you."),
            _("Whatever. More screen time for me."),
        ],
        ("skip_high", "camera_lover"): [
            _("Unbelievable! I'm vlogging this betrayal!"),
            _("You're missing the content of a lifetime! I'm going!"),
        ],
        ("not_skip", "camera_lover"): [
            _("Good call. I already planned my 'exam day' outfit anyway."),
            _("Let's go! I need that post-exam selfie!"),
        ],

        # -- camera_hater --
        ("skip_mid", "camera_hater"): [
            _("Fine. At least I won't have to worry about you pointing your phone at me."),
            _("Okay... I'll sit somewhere no one can see me."),
        ],
        ("skip_high", "camera_hater"): [
            _("Forget it! I'm not staying here where someone might record this argument!"),
            _("Fine! I'm going... alone, where nobody's watching!"),
        ],
        ("not_skip", "camera_hater"): [
            _("Good. The sooner we get in, the sooner we get out and away from everyone."),
            _("Smart. Let's go before the hallway gets crowded."),
        ],

        # -- hate_cum --
        ("skip_mid", "hate_cum"): [
            _("Whatever. At least the classroom will be less crowded without you."),
            _("Fine. I'll go scrub down my desk myself."),
        ],
        ("skip_high", "hate_cum"): [
            _("Gross attitude! I'm going... at least the exam room has hand sanitizer!"),
            _("Ugh! Stay here then! I have bigger things to worry about than you!"),
        ],
        ("not_skip", "hate_cum"): [
            _("Good. Let's get there early so I can pick a clean seat."),
            _("Finally, a sensible decision. Let's go... I brought wipes."),
        ],

        # -- loyal --
        ("skip_mid", "loyal"): [
            _("I'm disappointed, but I won't abandon my own responsibilities."),
            _("Fine. I'll go because it's the right thing. Even if you won't."),
        ],
        ("skip_high", "loyal"): [
            _("I can't believe you! We had a commitment! I'm going without you!"),
            _("This isn't like you! ...Fine. I won't let YOUR choices ruin MY record!"),
        ],
        ("not_skip", "loyal"): [
            _("That's the right call. Let's honor our commitment."),
            _("I knew you'd come around. Let's go... we owe it to ourselves."),
        ],

        # -- public_fetish --
        ("skip_mid", "public_fetish"): [
            _("Your loss. A whole room full of people and you're missing it."),
            _("Fine. I'll enjoy the crowd without you."),
        ],
        ("skip_high", "public_fetish"): [
            _("You're skipping the most exciting part of the week?! Unbelievable!"),
            _("Fine! More attention for me when I walk in alone!"),
        ],
        ("not_skip", "public_fetish"): [
            _("Good! Let's make an entrance. Walk in with me."),
            _("Yes! The exam room is going to be packed... let's go!"),
        ],
    }

    # Relationship-status exam overrides
    _EXAM_RELATIONSHIP_LINES = {
        # Dating the player
        ("invite", "dating"): [
            _("Come on, babe. Let's ace this together."),
            _("We're going to that exam together. Couple goals, right?"),
            _("Study buddy and boyfriend? Let's go."),
        ],
        ("insist", "dating"): [
            _("We're going. Together. I'm not letting my boyfriend fail."),
            _("Come ON. I didn't study with you all week for you to skip!"),
        ],
        ("tempted", "dating"): [
            _("Skip with my boyfriend? That's... actually really romantic in a bad way."),
            _("We could spend the time together instead... NO! Bad idea!"),
        ],
        ("convinced", "dating"): [
            _("Fine... but only because it's you. We're studying double next time."),
            _("My boyfriend is a bad influence. ...I kind of like it."),
        ],
        ("skip_mid", "dating"): [
            _("Seriously? I thought we'd go together... fine."),
            _("Some boyfriend you are. I'll ace it alone."),
        ],
        ("skip_high", "dating"): [
            _("I can't believe my own boyfriend is ditching the exam!"),
            _("You're impossible! I'm going without you!"),
        ],

        # Ex-girlfriend
        ("invite", "ex"): [
            _("Exam's starting. ...You can come if you want. I don't care."),
            _("The exam. Are you going? ...Not that I'm asking you specifically."),
        ],
        ("insist", "ex"): [
            _("Don't skip. I know you, you'll regret it. ...That's not me caring."),
            _("Just go to the exam. I'm not going to watch you self-destruct."),
        ],
        ("inform", "ex"): [
            _("Exam time. ...Good luck. Or whatever."),
            _("I'm going to the exam. You do you."),
        ],

        # Has NPC partner (boyfriend or girlfriend)
        ("invite", "has_bf"): [
            _("My %(pl)s's already there studying. Want to come with us?"),
            _("Exam time. My %(pl)s said %(pp)s'd save us seats."),
        ],
        ("tempted", "has_bf"): [
            _("Skip? My %(pl)s would never let me... but %(pp)s's not here right now."),
            _("If my %(pl)s finds out I skipped with you... oh god."),
        ],
        ("convinced", "has_bf"): [
            _("My %(pl)s is going to be so mad. ...Worth it."),
            _("%(Pp)s's going to wonder where I was... I'll think of something."),
        ],
    }

    def _exam_line(girl, key):
        """Pick an exam line with trait/relationship awareness."""
        # 1. Check relationship status first
        status = getattr(girl, "Player_status", "none")
        if status == "dating":
            rel_key = "dating"
        elif status == "ex":
            rel_key = "ex"
        elif hasattr(girl, "has_npc_partner") and girl.has_npc_partner():
            rel_key = "has_bf"
        else:
            rel_key = None

        if rel_key and (key, rel_key) in _EXAM_RELATIONSHIP_LINES:
            _line = _tl(renpy.random.choice(_EXAM_RELATIONSHIP_LINES[(key, rel_key)]))
            if rel_key == "has_bf":
                _line = _format_partner_line(girl, _line)
            return _line

        # 2. Check trait-specific lines (no discovery — exam is not a sexual context)
        if hasattr(girl, "has_trait"):
            # femdom before hardcore_sex: the bossy lines are hers (docs/plan_femdom.md D3)
            for trait in ("femdom", "hardcore_sex", "cute_sex", "cheater", "virgin", "camera_lover", "camera_hater", "hate_cum", "loyal", "public_fetish"):
                if girl.has_trait(trait) and (key, trait) in _EXAM_TRAIT_LINES:
                    return renpy.random.choice(_EXAM_TRAIT_LINES[(key, trait)])

        # 3. Fallback to generic pool
        return _exam_pick(key)

    def get_exam_reaction(girl):
        lvl = girl.study_level
        if lvl >= 7:   key = "react_high"
        elif lvl >= 3: key = "react_mid"
        else:           key = "react_low"
        return _exam_line(girl, key)

    # ---- grade result reactions (after announcement) ----------

    _GRADE_REACTIONS = {
        "A": {
            "expr": "happy",
            "lines": [
                _("Yes!"),
                _("Not bad at all!"),
                _("I did it!"),
            ],
        },
        "B": {
            "expr": "happy",
            "lines": [
                _("Good enough for me."),
                _("I'll take it."),
                _("Solid."),
            ],
        },
        "C": {
            "expr": "normal",
            "lines": [
                _("Could be worse, I guess."),
                _("Eh, whatever."),
                _("Okay, okay..."),
            ],
        },
        "D": {
            "expr": "sad",
            "lines": [
                _("That's... not great."),
                _("Ugh."),
                _("I need to do better."),
            ],
        },
        "F": {
            "expr": "sad",
            "lines": [
                _("Oh no..."),
                _("That's really bad."),
                _("I don't even want to talk about it."),
            ],
        },
    }

    _NERD_GRADE_REACTIONS = {
        "A": {
            "expr": "happy",
            "lines": [
                _("Of course. As expected."),
                _("Naturally."),
                _("Was there ever any doubt?"),
            ],
        },
        "B": {
            "expr": "sad",
            "lines": [
                _("A B? I can do better than that..."),
                _("A B... that's not me."),
                _("Not good enough. I'll fix this."),
            ],
        },
        "C": {
            "expr": "angry",
            "lines": [
                _("A C?! This is unacceptable!"),
                _("This is NOT okay!"),
                _("How did this happen?!"),
            ],
        },
        "D": {
            "expr": "scared",
            "lines": [
                _("A D... this can't be happening!"),
                _("No, no, no... a D?!"),
                _("This is a nightmare."),
            ],
        },
        "F": {
            "expr": "scared",
            "lines": [
                _("I... I failed?! No, this can't be right!"),
                _("An F? AN F?!"),
                _("This... this isn't real."),
            ],
        },
    }

    def _grade_reaction(girl, grade):
        pool = _NERD_GRADE_REACTIONS if girl.has_trait("nerd") else _GRADE_REACTIONS
        data = pool.get(grade, pool["C"])
        return (data["expr"], renpy.random.choice(data["lines"]))

# ============================================================
# exam_prompt  (called from Wait)
# ============================================================
label exam_prompt:

    # a girl who lives off campus is not a student here: she never speaks the exam invitation
    $ _girls_here = [g for g in girls_on_campus() if g.loc == CurrentLocation]

    if _girls_here:
        $ _sp = _girls_here[0]   # speaker

        # -- LOW LOVE: she just informs and leaves -------------
        if _sp.Love < 300:
            $ set_scene_expression(_sp, "normal")
            $ Say_Line(_sp, _exam_line(_sp, "inform"))

            menu:
                "Head to the exam":
                    call exam_event from _call_exam_event_low
                    return

                "Skip it":
                    python:
                        for g in _girls_here:
                            g.loc = "classroom"
                            if g in Party:
                                Party.remove(g)
                    $ Narration(_("You decide not to show up. It'll catch up with you eventually."))
                    $ exam_record_grade("F", "skipped")
                    return

        # -- MEDIUM LOVE: she invites, player can decline ------
        elif _sp.Love < 600:
            $ set_scene_expression(_sp, "normal")
            $ Say_Line(_sp, _exam_line(_sp, "invite"))

            menu:
                "Sure, let's go":
                    call exam_event from _call_exam_event
                    return

                "Not right now":
                    $ set_scene_expression(_sp, "sad")
                    $ Say_Line(_sp, _exam_line(_sp, "skip_mid"))
                    $ Change_Status(_sp, "Love", -3)
                    python:
                        for g in _girls_here:
                            g.loc = "classroom"
                            if g in Party:
                                Party.remove(g)
                    $ exam_record_grade("F", "skipped")
                    return

        # -- HIGH LOVE: she insists ----------------------------
        else:
            $ set_scene_expression(_sp, "normal")
            $ Say_Line(_sp, _exam_line(_sp, "insist"))

            menu:
                "Alright, let's go":
                    call exam_event from _call_exam_event_1
                    return

                "Maybe we skip it…" if _sp.Love >= 600 and _sp.Inbt >= 500:
                    call exam_convince(_sp) from _call_exam_convince
                    return

                "I'm not going":
                    $ set_scene_expression(_sp, "angry")
                    $ Say_Line(_sp, _exam_line(_sp, "skip_high"))
                    $ Change_Status(_sp, "Love", -5)
                    $ Change_Status(_sp, "Obed", -3)
                    python:
                        for g in _girls_here:
                            g.loc = "classroom"
                            if g in Party:
                                Party.remove(g)
                    $ exam_record_grade("F", "skipped")
                    return

    # -- NO GIRLS: narrator prompt ----------------------------
    else:
        $ Narration(_("It's exam day. The classroom is filling up... are you going?"))

        menu:
            "Head to the exam":
                call exam_event from _call_exam_event_2
                return

            "Skip it":
                $ Narration(_("You decide not to show up. It'll catch up with you eventually."))
                $ exam_record_grade("F", "skipped")
                return

# ============================================================
# exam_convince ... player tries to talk her into skipping
# ============================================================
label exam_convince(girl):

    $ Say_Player(_("Come on, let's just skip it. We'll make up for it later."))
    $ set_scene_expression(girl, "worried")
    $ Say_Line(girl, _exam_line(girl, "tempted"))

    menu:
        "Trust me, it'll be fine":
            $ set_scene_expression(girl, "smile")
            $ Say_Line(girl, _exam_line(girl, "convinced"))
            $ Change_Status(girl, "Obed", 5)
            $ Change_Status(girl, "Inbt", 3)
            $ Narration(_("The two of you decide to stay. Hopefully it won't cost you."))
            $ exam_record_grade("F", "skipped")
            return

        "Just kidding... let's go":
            $ set_scene_expression(girl, "normal")
            $ Say_Line(girl, _exam_line(girl, "not_skip"))
            call exam_event from _call_exam_event_3
            return

# ============================================================
# exam_event ... the exam itself
# ============================================================
label exam_event:

    $ store._in_event = True
    $ store._in_sandbox = False
    $ debug_log("[STATE] _in_event = True, _in_sandbox = False (exam_event)")

    python:
        # a girl who is away (giving birth) is excused: never teleported to class, no grade, study level kept.
        # A girl who lives off campus is not a student here: never in the exam
        for g in girls_on_campus():
            g.loc = "classroom"

    $ navigate_to("classroom", None)
    call Set_Scene(entry=True) from _call_Set_Scene_7

    # Override classroom ambient with exam music
    play music "audio/During Exam.mp3" fadein 1.0

    $ Narration(_("The classroom fills up. Pencils out."))

    # Girl reactions (all girls present in the classroom)
    $ _exam_queue = [g for g in ALL_GIRLS if g.loc == CurrentLocation]
    while _exam_queue:
        $ _eg = _exam_queue[0]
        $ _exam_queue.pop(0)
        $ _eg_grade = study_grade(_eg.study_level)
        $ set_scene_expression(_eg, exam_expression(_eg_grade))
        $ Say_Line(_eg, get_exam_reaction(_eg))

    # Results — show max 3 girls at a time, cycling oldest out
    $ Narration(_("Exam results:"))
    python:
        _player_grade = study_grade(Player.study_level)
        if _player_grade == "A":
            unlock_achievement("neeeerd")
    $ Narration(_("You... [Player.study_level] pts... Grade: [_player_grade]."))

    python:
        for _hg in ALL_GIRLS:
            hide_girl_sprite(_hg)
        _exam_prev_girl = None

    $ _result_queue = girls_on_campus()
    $ _nerd_f_girls = []
    while _result_queue:
        $ _rg = _result_queue[0]
        $ _result_queue.pop(0)

        # Show only current girl at center, hide previous
        python:
            if _exam_prev_girl is not None and _exam_prev_girl is not _rg:
                hide_girl_sprite(_exam_prev_girl)
            set_girl_sprite(_rg.gid, pose="standing", at_list=[slot_center])
            _exam_prev_girl = _rg

        python:
            _rg_grade = study_grade(_rg.study_level)
            _rg_lvl   = _rg.study_level
        $ Narration(_("[_rg.Name]... [_rg_lvl] pts... Grade: [_rg_grade]."))

        # Grade reaction
        python:
            _gr_expr, _gr_line = _grade_reaction(_rg, _rg_grade)
        $ set_scene_expression(_rg, _gr_expr)
        $ Say_Line(_rg, _gr_line)

        # Track nerd girls who got F
        if _rg.has_trait("nerd") and _rg_grade == "F":
            $ _nerd_f_girls.append(_rg)

    # Hide last girl from results loop
    if _exam_prev_girl is not None:
        $ hide_girl_sprite(_exam_prev_girl)

    $ Narration(_("Exam over. Study levels reset."))

    python:
        exam_record_grade(study_grade(Player.study_level), "exam")

        for g in girls_on_campus():
            _gg = study_grade(g.study_level)
            if not hasattr(g, "grade_history"):
                g.grade_history = []
            g.grade_history.append(_gg)
            print("[EXAM] %s grade: %s (history: %s)" % (g.gid, _gg, g.grade_history))

        Player.study_level = 0
        for g in girls_on_campus():
            g.study_level = 0
        for g in ALL_GIRLS:
            if girl_is_away(g):
                print("[EXAM] %s excused (away): no grade, study level kept at %d" % (g.gid, g.study_level))

    # Nerd F sub-event
    if _nerd_f_girls:
        $ unlock_achievement("bad_influence")
        $ _nf_queue = list(_nerd_f_girls)
        while _nf_queue:
            $ _nf_girl = _nf_queue.pop(0)
            call _nerd_exam_f_event(_nf_girl) from _call_nerd_exam_f

    # Advance time to Evening (exam takes the rest of Midday)
    python:
        _evening_idx = TIME_NAMES.index("Evening")
        _slots_to_evening = _evening_idx - store.TimeIndex
        if _slots_to_evening > 0:
            advance_time(_slots_to_evening)

    # Restore normal music after exam
    play music "audio/Before Class.mp3" fadein 1.0

    $ store._in_event = False
    $ store._in_sandbox = True
    $ debug_log("[STATE] _in_event = False, _in_sandbox = True (exam_event end)")

    return

# ============================================================
# _nerd_exam_f_event ... nerd girl got an F, confrontation
# ============================================================
label _nerd_exam_f_event(girl):

    # Stay at exam location — hide other girls, focus on this one
    python:
        for _hg in ALL_GIRLS:
            if _hg is not girl:
                hide_girl_sprite(_hg)
    $ set_girl_sprite(girl.gid, pose="standing", at_list=[slot_center])

    if getattr(girl, "_nerd_f_count", 0) == 0:
        # ---- FIRST F ----
        $ set_scene_expression(girl, "sad")
        $ Say_Line(girl, _("AN F! Did you see that?! I NEVER got below an A before I met you! I'm freaking out!"))

        menu:
            "Life is more than a grade on a report card.":
                $ set_scene_expression(girl, "sad", brows="brows_confused")
                $ Say_Line(girl, _("Do you think I'm taking this too seriously? I know I can recover this grade, but do you think I should be less obsessed about grades?"))

                menu:
                    "Yes":
                        $ set_scene_expression(girl, "nervous")
                        $ Say_Line(girl, _("Maybe you're right. I've been so focused on grades that I forgot to actually enjoy being here. I'll try to relax a little."))
                        $ set_scene_expression(girl, "smile")
                        $ girl.traits.discard("nerd")
                        # a designed loss of a CANON trait (Tenny) must persist: without this, every load
                        # gave the nerd back (enforce_canon_traits reads girl_canon_traits minus _canon_lost)
                        $ girl._canon_lost = set(getattr(girl, "_canon_lost", None) or ()) | ({"nerd"} if "nerd" in GIRLS_CONFIG.get(girl.gid, {}).get("traits", ()) else set())
                        $ Change_Status(girl, "Love", 15)
                        python:
                            renpy.music.play("audio/Information.mp3", channel="notify_sfx", loop=False)
                            renpy.show_screen("discovery_banner", girl_name=girl.Name, info_text=_tl(_("Trait lost: Nerd")), name_color=girl.color)
                            print("[EXAM] %s lost nerd trait via F event option A1" % girl.gid)

                    "No, you can focus more next time":
                        $ set_scene_expression(girl, "serious", brows="brows_normal")
                        $ Say_Line(girl, _("You're right. This was just a bad week. I'll make sure it doesn't happen again."))
                        $ set_scene_expression(girl, "happy")
                        $ Change_Status(girl, "Love", 10)

            "Yeah, we really dropped the ball this week.":
                $ set_scene_expression(girl, "uncomfortable")
                $ Say_Line(girl, _("Thanks for agreeing. We can still see each other, but let's focus more on studying this week, okay?"))
                $ set_scene_expression(girl, "worried")
                $ Change_Status(girl, "Love", 5)
                $ Change_Status(girl, "Obed", -10)

            "You skipped because you wanted to.":
                $ set_scene_expression(girl, "angry")
                $ Say_Line(girl, _("Excuse me?! YOU are the one who kept asking me to stay! This is YOUR fault!"))
                $ Change_Status(girl, "Obed", 50)
                $ Change_Status(girl, "Love", -50)
                $ hide_girl_sprite(girl)
                $ Narration(_("She storms off toward her room. She does not look happy at all."))
                python:
                    _girl_room = girl_home_loc(girl)
                    girl.loc = _girl_room
                    girl.set_temp_status("angry", 2, reason="exam_blame")
                    print("[EXAM] %s angry 2 days (exam blame)" % girl.gid)

    else:
        # ---- REPEAT F ----
        $ set_scene_expression(girl, "sad")
        $ Say_Line(girl, _("AGAIN! Another F! One more and I lose my spot, do you understand how serious this is?!"))
        $ set_scene_expression(girl, "scared", eyes="eyes_normal")

        menu:
            "Life is more than a grade on a report card.":
                $ set_scene_expression(girl, "angry", eyes="eyes_squint")
                $ Say_Line(girl, _("You said that last time! And look where it got me!"))

                menu:
                    "Yes, and I still mean it":
                        $ set_scene_expression(girl, "sad", eyes="eyes_side")
                        $ Say_Line(girl, _("... Maybe you're right. Maybe I've been killing myself over something that doesn't matter that much. Fine. I'll stop obsessing."))
                        $ set_scene_expression(girl, "nervous")
                        $ girl.traits.discard("nerd")
                        # a designed loss of a CANON trait (Tenny) must persist: without this, every load
                        # gave the nerd back (enforce_canon_traits reads girl_canon_traits minus _canon_lost)
                        $ girl._canon_lost = set(getattr(girl, "_canon_lost", None) or ()) | ({"nerd"} if "nerd" in GIRLS_CONFIG.get(girl.gid, {}).get("traits", ()) else set())
                        $ Change_Status(girl, "Love", 10)
                        python:
                            renpy.music.play("audio/Information.mp3", channel="notify_sfx", loop=False)
                            renpy.show_screen("discovery_banner", girl_name=girl.Name, info_text=_tl(_("Trait lost: Nerd")), name_color=girl.color)
                            print("[EXAM] %s lost nerd trait via repeat F event option A1" % girl.gid)

                    "No, let's buckle down this time":
                        $ set_scene_expression(girl, "serious")
                        $ Say_Line(girl, _("Okay. No more skipping. I mean it. Not even once."))
                        $ set_scene_expression(girl, "normal")
                        $ Change_Status(girl, "Love", 5)

            "Yeah, we really messed up again.":
                $ set_scene_expression(girl, "uncomfortable")
                $ Say_Line(girl, _("This can't keep happening. We need to study EVERY day this week. Promise me."))
                $ set_scene_expression(girl, "worried")
                $ Change_Status(girl, "Love", 3)
                $ Change_Status(girl, "Obed", -15)

            "You skipped because you wanted to.":
                $ set_scene_expression(girl, "angry")
                $ Say_Line(girl, _("AGAIN with that?! I can't believe you! Get out of my sight!"))
                $ Change_Status(girl, "Obed", 50)
                $ Change_Status(girl, "Love", -75)
                $ hide_girl_sprite(girl)
                $ Narration(_("She storms off toward her room. She does not look happy at all."))
                python:
                    _girl_room = girl_home_loc(girl)
                    girl.loc = _girl_room
                    girl.set_temp_status("angry", 2, reason="exam_blame")
                    print("[EXAM] %s angry 2 days (repeat exam blame)" % girl.gid)

    $ girl._nerd_f_count = getattr(girl, "_nerd_f_count", 0) + 1
    $ hide_girl_sprite(girl)
    $ print("[EXAM] %s nerd F event done, _nerd_f_count=%d" % (girl.gid, girl._nerd_f_count))
    return
