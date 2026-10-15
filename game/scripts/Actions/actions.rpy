# ============================================
# ROOM: DAYTIME SLEEP LINES + LAZY META LINES
# ============================================

init python:
    DAYTIME_SLEEP_LINES = [
        _("Some days you just do not feel up to it. You sleep away the rest of the day."),
        _("You come up with an excuse for yourself and sleep through the rest of the day."),
        _("You convince yourself you are too exhausted for any more human interaction."),
        _("You stare at the ceiling for ten minutes and decide that is enough effort for today."),
        _("You set three alarms. You turn them all off. You go back to sleep."),
        _("Your bed has a gravitational pull today. There is nothing you can do about it."),
        _("Technically, sleeping is also a skill. You are just practicing."),
        _("Achievement unlocked: Horizontal Champion."),
    ]

    LAZY_SLEEP_LINES = [
        _("Are you looking for a specific event or what?"),
        _("You know the point of the game is the girls, right?"),
        _("Hey buddy, try some new interactions. Get out of bed. I believe in you."),
        _("Your pillow is not a character. It does not have a story arc."),
        _("The world outside your room is still there. Probably."),
        _("Are you sure you want to sleep again? Maybe try talking to the girls.")

    ]

# ============================================
# CLASSROOM: CLASS NARRATION LINES
# Add as many lines as you want to this list.
# ============================================

init python:
    CLASS_LINES = [
        _("You spend some time focused on the lesson. The final result is 1/0. Something does not seem right."),

        _("You listen to the teacher's lecture. He rounds pi to 5 and gravity to 10."),
        _("The teacher spends the entire class arguing with a student about whether dinosaurs had feathers. Time flies."),
        _("The teacher spends most of the class talking about her personal life. It was actually a fun lesson."),
        _("You learn about the history of silent Austrian cinema. Interesting."),
        _("The professor draws a diagram on the board. By the end of class, nobody, including him, knows what it represents."),
        _("Today's topic is quantum mechanics. The teacher explains it using a cat. You leave more confused than before."),
        _("The class is split into groups for a project. You end up doing everything alone anyway. Productive."),
        _("The teacher loses his train of thought mid-sentence and just says 'anyway, moving on'. Three times."),
        _("You read the textbook while the professor reads the exact same textbook out loud. Efficient."),
        _("A student asks a question. The teacher responds with 'great question' and then answers a completely different question."),
        _("The projector breaks. The teacher improvises by describing the slides out loud for forty minutes."),
        _("Extra credit is offered for whoever can explain the concept back. Nobody volunteers. Silence. Class dismissed."),
        _("The substitute teacher is clearly more lost than the students. A student ends up teaching the class."),
        _("You take notes diligently. Later you realize the notes say nothing useful, but your handwriting has never looked better."),
    ]

# ============================================
# GYM: WORKOUT NARRATION LINES
# Add as many lines as you want to this list.
# ============================================

init python:
    GYM_WORKOUT_LINES = [
        _("Alright, today is leg day... First exercise squat, second scott curl, third straight curl... wtf, who put this routine together?"),
        _("You down your crazy clown pre-workout . It gives you energy and you manage to bench press 2kg on each side."),
        _("You arrive at the gym, grab the heaviest dumbbell... it is 4kg. You put it back and grab the 2kg ones."),
        _("Thirty minutes on the treadmill. You feel like a champion."),
        _("You try to do a pull-up. You hang there for a while. You come back down. That counts as a rep."),
        _("The gym is packed. You spend most of the time waiting for equipment and scrolling your phone. Still counts."),
        _("You put on your most intimidating face in the mirror while doing curls. Someone walks in. You pretend to check your form."),
        _("Today is chest day. You do three sets, feel incredible, and then remember you skipped chest last week too."),
        _("You spot someone with perfect form and study them carefully. You try to copy it. You hurt your back doing bicep curls."),
        _("You finish your session, drenched in sweat."),
        _("You go full beast mode for the first set. The second set humbles you. The third set simply does not happen."),
        _("You take a selfie for motivation. You look exhausted. You post it anyway."),
        _("The protein shake you brought smells suspicious. You drink it anyway. Gains are gains."),
        _("Leg press, hip thrust, leg curl. You leave walking like a penguin. Mission accomplished."),
        _("You dedicate today to abs. Forty crunches in, you decide abs are overrated anyway."),
    ]

# ============================================
# LOCATION-SPECIFIC ACTIONS
# ============================================

# Pool: Swim
label do_swim:
    $ _pool_girls = [g for g in ALL_GIRLS if g.loc == CurrentLocation]

    if not _pool_girls:
        "You swim for a while. The water feels nice."
        call _swim_register from _call_swim_register_alone
        call Apply_Time_Cost(TIME_COSTS["swim"]) from _call_Apply_Time_Cost
        return

    python:
        if len(_pool_girls) == 1:
            _swim_invite_line = _tl(_("Hey %s, want to swim together?")) % _pool_girls[0].Name
        else:
            _swim_names = ", ".join(g.Name for g in _pool_girls)
            _swim_invite_line = _tl(_("Hey %s! Want to swim together?")) % _swim_names
    $ Say_Player(_swim_invite_line)

    python:
        _swim_accepted = []
        _swim_declined = []
        _swim_no_bikini = []
        for _sg in _pool_girls:
            if swim_together_ok(_sg):
                _swim_accepted.append(_sg)
            else:
                _swim_declined.append(_sg)

    # Declined girls speak first
    python:
        for _sg in _swim_declined:
            Say_Line(_sg, _tl(renpy.random.choice(_SWIM_DECLINE_LINES)))

    if not _swim_accepted:
        "You swim alone for a while."
        call _swim_register from _call_swim_register_declined
        call Apply_Time_Cost(TIME_COSTS["swim"]) from _call_Apply_Time_Cost_swim_alone
        return

    # Accepted girls respond + bikini check
    python:
        for _sg in _swim_accepted:
            _has_bikini = getattr(_sg, "_bikini_unlocked", False)
            if _has_bikini:
                Say_Line(_sg, _tl(_("Sure! Let me get changed.")))
                if getattr(_sg, "CurrentOutfitPreset", None) != "pool":
                    _sg.WearPreset("pool", apply_now=True)
                    renpy.with_statement(dissolve)
                    renpy.pause(0.3)
            else:
                _swim_no_bikini.append(_sg)
                set_scene_expression(_sg, "sad")
                Say_Line(_sg, swim_no_bikini_line(_sg))
                set_scene_expression(_sg, "normal")

    # Swim with whoever has a bikini
    python:
        _swim_ready = [g for g in _swim_accepted if g not in _swim_no_bikini]

    if not _swim_ready:
        "You swim alone for a while."
    else:
        "You swim together for a while."
        python:
            for _sg in _swim_ready:
                Change_Status(_sg, "Love", 5)
                Change_Status(_sg, "Lust", 2)

        # Mid-swim events (one random girl with bikini)
        python:
            _event_girl = renpy.random.choice(_swim_ready)
            _pool_event_roll = renpy.random.randint(1, 3)
        if _pool_event_roll == 1:
            call pool_event_pull_string(_event_girl) from _call_pool_event_pull_string

    # No-bikini girls still get a small Love bonus for the invitation
    python:
        for _sg in _swim_no_bikini:
            Change_Status(_sg, "Love", 2)

    call _swim_register from _call_swim_register_together
    call Apply_Time_Cost(TIME_COSTS["swim"]) from _call_Apply_Time_Cost_swim
    return

# ============================================================
# POOL EVENTS... triggered during do_swim when a girl is present
# ============================================================

# ---- POOL EVENT 1: Entering the Pool ----
# She's by the pool, player enters. How do you get in?
label pool_event_enter(girl):
    "She's sitting on the edge of the pool, legs dangling in the water."
    menu:
        "Time to get in."
        "Cannonball":
            "You take a running start and launch yourself into the pool."
            "SPLASH. A massive wave hits her right in the face."
            if girl.has_trait("cute_sex"):
                $ set_scene_expression(girl, "surprised")
                $ Say_Line(girl, _("Eek...! My hair...! I just dried it!"))
                "She wipes water from her eyes, pouting."
            elif girl.has_trait("hardcore_sex"):
                $ set_scene_expression(girl, "angry")
                $ Say_Line(girl, _("You asshole! These are my good clothes!"))
                "She splashes you back, hard."
            elif girl.has_trait("exhibitionist"):
                $ set_scene_expression(girl, "laugh")
                $ Say_Line(girl, _("Hey...! You got water everywhere!"))
                "She laughs despite herself, wringing out her shirt."
            elif girl.has_trait("public_shy"):
                $ set_scene_expression(girl, "scared")
                $ Say_Line(girl, _("Everyone is looking at us now... why did you do that?!"))
                "She tries to make herself smaller."
            else:
                $ set_scene_expression(girl, "angry")
                $ Say_Line(girl, _("Hey! You soaked me! What the hell?!"))
                "She shakes water off her hands, annoyed."
            $ Change_Status(girl, "Love", -5)

        "Normal dive":
            "You walk to the edge, take a breath, and dive in cleanly."
            "Barely a splash. You surface and slick your hair back."
            if girl.has_trait("cute_sex"):
                $ set_scene_expression(girl, "shy", blush=1)
                $ Say_Line(girl, _("W-wow... that was a really clean dive..."))
                "She watches you surface, impressed."
            elif girl.has_trait("hardcore_sex"):
                $ set_scene_expression(girl, "smirk")
                $ Say_Line(girl, _("Not bad. At least you didn't embarrass yourself."))
            else:
                $ Say_Line(girl, _("Nice form. Show-off."))
                "She smirks."
            $ Change_Status(girl, "Obed", 5)

        "Use the ladder":
            "You carefully climb down the ladder, one rung at a time."
            "The water reaches your waist. You ease in slowly."
            if girl.has_trait("cute_sex"):
                $ set_scene_expression(girl, "normal")
                $ Say_Line(girl, _("That's... actually smart. The water is freezing."))
            elif girl.has_trait("hardcore_sex"):
                $ set_scene_expression(girl, "smirk")
                $ Say_Line(girl, _("...Really? The ladder? What are you, fifty?"))
                "She shakes her head."
            else:
                $ Say_Line(girl, _("The ladder, huh? Playing it safe today?"))
            $ Change_Status(girl, "Obed", -5)

    return

# ---- POOL EVENT 2: Water Temperature ----
# She asks about the water before getting in. Tell the truth or lie.
label pool_event_temperature(girl):
    "She's standing at the edge, hugging herself."
    if girl.has_trait("cute_sex"):
        $ Say_Line(girl, _("Is it cold...? It looks cold. Please tell me it's not cold."))
    elif girl.has_trait("hardcore_sex"):
        $ Say_Line(girl, _("How's the water? And don't lie to me."))
    else:
        $ Say_Line(girl, _("How's the water? Be honest."))

    menu:
        "It's nice, come on in. {i}(Truth){/i}":
            $ Say_Player(_("It's actually pretty nice once you're in. Not too cold."))
            "She crouches down and dips her toes in."
            if girl.has_trait("cute_sex"):
                $ Say_Line(girl, _("Oh... it IS nice! You weren't lying!"))
                "She slides in carefully, sighing with relief."
            elif girl.has_trait("hardcore_sex"):
                $ Say_Line(girl, _("Hm. Acceptable. Good, you didn't lie."))
                "She steps in without hesitation."
            else:
                $ Say_Line(girl, _("Hey, you were right. Not bad."))
                "She gets in and gives you a small nod of approval."
            $ Change_Status(girl, "Love", 5)

        "It's super warm, like a bath. {i}(Lie){/i}":
            $ Say_Player(_("Oh, it's great. Like a warm bath. You'll love it."))
            "She narrows her eyes but crouches down to test it with her toe."
            "The second her foot touches the water, she yanks it back."
            if girl.has_trait("cute_sex"):
                $ set_scene_expression(girl, "surprised")
                $ Say_Line(girl, _("That is NOT warm! You liar...!"))
                "She pouts, but then giggles despite herself."
                $ Say_Line(girl, _("I can't believe I almost fell for that..."))
            elif girl.has_trait("hardcore_sex"):
                $ set_scene_expression(girl, "angry")
                $ Say_Line(girl, _("You piece of... I TOLD you not to lie!"))
                "She kicks water at you, but there's a smirk forming."
                $ Say_Line(girl, _("...Okay, that was kinda funny. I hate you."))
            elif girl.has_trait("exhibitionist"):
                $ set_scene_expression(girl, "surprised")
                $ Say_Line(girl, _("Liar! That's freezing!"))
                "She splashes you and laughs."
                $ Say_Line(girl, _("You're going to pay for that."))
            else:
                $ set_scene_expression(girl, "surprised")
                $ Say_Line(girl, _("You LIED! That's cold as hell!"))
                "She flicks water at you, trying to look mad."
                $ Say_Line(girl, _("...Fine, I would have done the same thing."))
            $ Change_Status(girl, "Obed", 5)

    return

# ---- POOL EVENT 3: Pull Bikini String ----
# During the swim, player pulls her bikini string. Reaction depends on stats.
label pool_event_pull_string(girl):
    "While she's floating on her back, you notice the string of her bikini top dangling in the water."
    "Before you think twice, you grab it and pull."
    "The knot comes undone. Her top loosens."
    $ set_scene_expression(girl, "surprised")

    python:
        _love = getattr(girl, "Love", 0)
        _inbt = getattr(girl, "Inbt", 0)
        _obed = getattr(girl, "Obed", 0)

    if girl.has_trait("exhibitionist"):
        # Exhibitionist: doesn't care, maybe enjoys it
        $ set_scene_expression(girl, "sexy")
        $ Say_Line(girl, _("Oh no... my top came undone. Whatever shall I do."))
        "She doesn't rush to cover herself. If anything, she takes her sweet time."
        $ Say_Line(girl, _("Enjoying the view?"))
        "She ties it back on with a smirk."
        $ Change_Status(girl, "Obed", 5)
        $ Change_Status(girl, "Inbt", 8)
        $ Change_Status(girl, "Lust", 3)

    elif girl.has_trait("public_shy"):
        # Public shy: mortified, leaves
        $ set_scene_expression(girl, "scared")
        $ Say_Line(girl, _("OH MY GOD...!"))
        "She crosses her arms over her chest and turns away from everyone."
        $ Say_Line(girl, _("What is WRONG with you?! People can SEE!"))
        "She scrambles out of the pool, covering herself, and practically runs to the changing room."
        $ Change_Status(girl, "Obed", 8)
        $ Change_Status(girl, "Love", -10)
        $ Change_Status(girl, "Inbt", 10)

    elif _love >= 500:
        # High Love: puts it back, not offended
        if girl.has_trait("cute_sex"):
            $ set_scene_expression(girl, "shy", blush=2)
            $ Say_Line(girl, _("H-hey...! Don't do that!"))
            "She quickly grabs the loose top and ties it back, face bright red."
            $ Say_Line(girl, _("You're so mean... I'll get you back for that."))
            "She splashes you, trying to hide her embarrassment."
        elif girl.has_trait("hardcore_sex"):
            $ set_scene_expression(girl, "angry")
            $ Say_Line(girl, _("You did NOT just do that."))
            "She ties it back on with practiced speed."
            $ Say_Line(girl, _("Next time I'm pulling YOUR shorts down. See how you like it."))
            "She's not actually mad. Just plotting revenge."
        else:
            $ set_scene_expression(girl, "shy", blush=1)
            $ Say_Line(girl, _("Hey...! Give me a second!"))
            "She laughs nervously as she ties the knot back."
            $ Say_Line(girl, _("You're lucky I like you. Anyone else would be dead right now."))
        $ Change_Status(girl, "Obed", 5)
        $ Change_Status(girl, "Inbt", 5)

    elif _inbt >= 400 or _obed >= 500:
        # High Inbt/Obed: just accepts it
        if girl.has_trait("cute_sex"):
            $ set_scene_expression(girl, "shy", blush=2)
            $ Say_Line(girl, _("A-ah...!"))
            "She covers herself with one arm and fumbles to retie with the other."
            "She doesn't say anything else. She just looks away."
        elif girl.has_trait("hardcore_sex"):
            $ set_scene_expression(girl, "angry")
            $ Say_Line(girl, _("...Seriously?"))
            "She ties it back on without another word. Her jaw is clenched."
        else:
            $ set_scene_expression(girl, "worried")
            $ Say_Line(girl, _("..."))
            "She quietly ties the bikini back on, not meeting your eyes."
        $ Change_Status(girl, "Obed", 8)
        $ Change_Status(girl, "Inbt", 8)

    else:
        # Low everything: angry, leaves
        if girl.has_trait("cute_sex"):
            $ set_scene_expression(girl, "sad")
            $ Say_Line(girl, _("W-why would you do that...?!"))
            "Tears well up in her eyes. She climbs out of the pool, clutching her top."
            $ Say_Line(girl, _("I'm going. Don't talk to me."))
        elif girl.has_trait("hardcore_sex"):
            $ set_scene_expression(girl, "angry")
            $ Say_Line(girl, _("Are you out of your MIND?!"))
            "She shoves you back in the water and climbs out."
            $ Say_Line(girl, _("Touch me again and I'll drown you. I mean it."))
        else:
            $ set_scene_expression(girl, "angry")
            $ Say_Line(girl, _("What the hell is wrong with you?!"))
            "She ties her top back on and gets out of the pool."
            $ Say_Line(girl, _("I'm done. Don't follow me."))
        $ Change_Status(girl, "Obed", 8)
        $ Change_Status(girl, "Love", -10)
        $ Change_Status(girl, "Inbt", 10)

    return

# Shower: Shower
label do_shower:

    $ _shower_girls = [g for g in ALL_GIRLS if g.loc == CurrentLocation]

    if not _shower_girls:
        call _shower_solo from _call__shower_solo
        return

    # --- Angry girls: leave immediately before any interaction ---
    python:
        _angry_girls = [g for g in _shower_girls if hasattr(g, "has_temp_status") and g.has_temp_status("angry")]
        for _ag in _angry_girls:
            _angry_shower_lines = [
                _("You walk into the shower and see [_ag.Name]. She freezes for a second, eyes locked on you."),
                _("You step into the shower. [_ag.Name] is there, water running down her body. She notices you."),
                _("[_ag.Name] is in the shower. For a brief moment, her eyes wander over you before she catches herself."),
            ]
            Narration(_tl(renpy.random.choice(_angry_shower_lines)))
            _ag_hesitate = [
                _("She hesitates, her gaze lingering just a moment too long... then her expression hardens."),
                _("For a split second, something flickers in her eyes... but then she remembers she's furious."),
                _("Her lips part slightly... but then she clenches her jaw and looks away."),
            ]
            Narration(_tl(renpy.random.choice(_ag_hesitate)))
            _ag_angry_lines = [
                _("No. I'm still mad at you. Don't even look at me."),
                _("Don't think seeing me like this changes anything. I'm STILL angry."),
                _("I was here first. But I'd rather leave than share this space with you right now."),
                _("You have some nerve showing up here. I'm leaving."),
            ]
            Say_Line(_ag, _tl(renpy.random.choice(_ag_angry_lines)))
            Narration(_tl(_("%s quickly wraps a towel around herself and storms out of the shower.")) % _ag.Name)
            _ag.WearPreset("casual", apply_now=False)
            _ag.loc = _ag.home
            hide_girl_sprite(_ag)
        # Remove angry girls from the shower list
        _shower_girls = [g for g in _shower_girls if g not in _angry_girls]

    if not _shower_girls:
        call _shower_solo from _call__shower_solo_angry
        return

    # --- Player walked in on girls: register ---
    python:
        for _sg in _shower_girls:
            _sg.RegisterAction("player_walked_in_shower")

    # --- Invite girls to join ---
    python:
        _SHOWER_DECLINE_LINES = [
            _("Keep dreaming."),
            _("Hygiene is a very personal moment."),
            _("I don't think so..."),
            _("Maybe another time."),
            _("You wish."),
            _("Not happening."),
        ]

        _SHOWER_ACCEPT_LINES = [
            _("Sure... why not?"),
            _("Alright, but no funny business."),
            _("Fine, but don't stare too much."),
            _("I guess there's room for two."),
        ]

        # Trait-specific shower accept lines
        _SHOWER_TRAIT_ACCEPT = {
            "hardcore_sex": [
                _("Fine, get in. But if you peek too much, I'm splashing you."),
                _("You want to shower together? Bold. Get in before I change my mind."),
                _("Alright, but keep your hands where I can see them... or don't."),
            ],
            "cute_sex": [
                _("O-okay... but don't look while you get in!"),
                _("We can share, but... no funny business, okay?"),
                _("Promise you won't look too much? ...Fine, come in."),
            ],
            "cheater": [
                _("Sure, why not? It's just a shower... right?"),
                _("This is innocent enough. Just two people sharing hot water."),
                _("A shower together? You don't have to ask me twice."),
            ],
            "cheater_bf": [
                _("Sure, why not? It's just a shower... right?"),
                _("My %(pl)s would lose it if %(pp)s knew. Get in."),
                _("This is innocent enough. Just two people sharing hot water."),
            ],
            "virgin": [
                _("A shower? Together?! I... okay, but don't stare!"),
                _("I've never done this before... just... be normal about it."),
                _("This is so embarrassing... fine, but eyes up!"),
            ],
            "public_shy": [
                _("What if someone walks in?! Lock the door first!"),
                _("Are you sure no one will see us? Okay... hurry up."),
                _("Close the curtain properly! I don't want anyone seeing!"),
            ],
            "exhibitionist": [
                _("Leave the door unlocked. Makes it more exciting."),
                _("A shower together? I was hoping you'd ask."),
                _("Sure. And I don't care who knows about it."),
            ],
            "loyal": [
                _("Fine, but this means nothing. I'm just saving water."),
                _("Just a shower, nothing more. Don't get any ideas."),
                _("Okay, but keep your distance. This doesn't mean anything."),
            ],
            "loyal_bf": [
                _("Just a shower, nothing more. I have a %(pl)s."),
                _("Fine, but this means nothing. I'm just saving water."),
                _("My %(pl)s wouldn't like this... but it's just a shower."),
            ],
        }

        # Lines when she declines the shower but has had private sex acts
        # (she's worried about being seen, not about the act itself)
        _SHOWER_DECLINE_HAD_SEX = [
            _("We already messed up behind closed doors. We can't do this here, someone could see us."),
            _("What we did in the room was risky enough. I'm not adding a public shower to the list."),
            _("Are you crazy? What if someone walks in? At least in the room we had a locked door."),
            _("No. What happens in private stays in private. This is way too exposed."),
            _("I'm not repeating what we did where anyone could catch us. Not here."),
            _("Keep what we do between us. In a shower? Someone will definitely find out."),
        ]

        # Trait-specific shower decline lines (no prior sex history)
        _SHOWER_TRAIT_DECLINE = {
            "hardcore_sex": [
                _("Not now. I shower alone when I'm in a mood."),
                _("Get out. I don't share my shower time."),
            ],
            "cute_sex": [
                _("N-no! That's way too embarrassing!"),
                _("I can't shower with you watching me! Go away!"),
            ],
            "cheater": [
                _("Not right now. Even I need my privacy sometimes."),
                _("Maybe another time. I'm in a rush."),
            ],
            "virgin": [
                _("No way! I'm not ready for that!"),
                _("Absolutely not! That's too much too fast!"),
            ],
            "public_shy": [
                _("No! What if someone hears us?!"),
                _("Are you crazy?! Someone could walk in!"),
            ],
            "loyal": [
                _("No. This crosses a line."),
                _("Absolutely not. I barely know you like that."),
            ],
            "loyal_bf": [
                _("No. I have a %(pl)s and this crosses a line."),
                _("Absolutely not. I'm taken."),
            ],
        }

        _shower_accepted = []
        _shower_declined = []
        for _sg in _shower_girls:
            _has_seen_nude = _sg.HasSeen("player_saw_boobs") or _sg.HasSeen("player_saw_pussy")
            _best_stat = max(getattr(_sg, "Love", 0), getattr(_sg, "Inbt", 0))
            # Sexual history lowers the bar: +50 per sex act, capped at +200
            # Acts only ("sex" + "anal"): positions are preferences, adding them counted one scene twice
            _best_stat += sex_history_bonus(_sg)   # numbers live in SEX_HISTORY_THRESHOLDS
            _will_accept = _best_stat >= 300 if _has_seen_nude else _best_stat >= 500
            # her story locks showering together (story_steps.rpy, act "shower_join"): refused whatever her stats
            if story_act_locked(_sg, "shower_join"):
                _will_accept = False
            if _will_accept:
                _shower_accepted.append(_sg)
            else:
                _shower_declined.append(_sg)

    # --- Declined girls: react, restore outfit, and leave ---
    # (She was already showering; the player walked in and asked to join)
    python:
        for _sg in _shower_declined:
            Say_Player(_tl(_("Hey %s, mind if I join you?")) % _sg.Name)
            # her story locks it: her step's own refusal, and no flirty comeback afterwards
            _sg_story_locked = story_act_locked(_sg, "shower_join")
            # Check if she's had private sex acts with the player
            _sd_sa = getattr(_sg, "Sex_acts", {}) or {}
            _sd_total = sum(_sd_sa.get(k, 0) for k in ("hj", "bj", "tj", "sex", "anal"))   # acts only, never positions
            _shower_line = None
            if _sg_story_locked:
                _shower_line = story_locked_line(_sg, "shower_join")
            elif _sd_total > 0:
                # She's done stuff in private -- decline is about the public setting
                _shower_line = _tl(renpy.random.choice(_SHOWER_DECLINE_HAD_SEX))
            elif hasattr(_sg, "has_trait"):
                # Try trait-specific line
                # loyal_bf / loyal: pick BF variant when she has a partner
                _sg_has_bf = hasattr(_sg, "has_npc_partner") and _sg.has_npc_partner()
                _BF_TRAIT_KEYS = {"loyal_bf": "loyal", "cheater_bf": "cheater"}
                _bf_fmt = partner_fmt(_sg)
                for _st, _sp in _SHOWER_TRAIT_DECLINE.items():
                    if _st in _BF_TRAIT_KEYS:
                        if _sg.has_trait(_BF_TRAIT_KEYS[_st]) and _sg_has_bf:
                            _shower_line = _tl(renpy.random.choice(_sp)) % _bf_fmt
                            break
                    elif _st in ("loyal", "cheater"):
                        if _sg.has_trait(_st) and not _sg_has_bf:
                            _shower_line = _tl(renpy.random.choice(_sp))
                            break
                    elif _sg.has_trait(_st):
                        _shower_line = _tl(renpy.random.choice(_sp))
                        break
            if not _shower_line:
                _shower_line = _tl(renpy.random.choice(_SHOWER_DECLINE_LINES))
            Say_Line(_sg, _shower_line)
            Narration(_tl(_("%s grabs her towel and leaves the shower.")) % _sg.Name)
            _sg.WearPreset("casual", apply_now=False)
            _sg.loc = _sg.home
            # the "forgot my towel" comeback flirts: never for a girl whose story locked it
            _sg._shower_just_declined = not _sg_story_locked
            hide_girl_sprite(_sg)

    # --- Accepted girls: react ---
    python:
        for _sg in _shower_accepted:
            Say_Player(_tl(_("Hey %s, mind if I join you?")) % _sg.Name)
            # Try trait-specific line first
            _shower_line = None
            if hasattr(_sg, "has_trait"):
                _sg_has_bf = hasattr(_sg, "has_npc_partner") and _sg.has_npc_partner()
                _bf_fmt = partner_fmt(_sg) if _sg_has_bf else {}
                _BF_TRAIT_KEYS = {"loyal_bf": "loyal", "cheater_bf": "cheater"}
                for _st, _sp in _SHOWER_TRAIT_ACCEPT.items():
                    if _st in _BF_TRAIT_KEYS:
                        if _sg.has_trait(_BF_TRAIT_KEYS[_st]) and _sg_has_bf:
                            _shower_line = _tl(renpy.random.choice(_sp)) % _bf_fmt
                            break
                    elif _st in ("loyal", "cheater"):
                        if _sg.has_trait(_st) and not _sg_has_bf:
                            _shower_line = _tl(renpy.random.choice(_sp))
                            break
                    elif _sg.has_trait(_st):
                        _shower_line = _tl(renpy.random.choice(_sp))
                        break
            if not _shower_line:
                _shower_line = _tl(renpy.random.choice(_SHOWER_ACCEPT_LINES))
            Say_Line(_sg, _shower_line)

    if not _shower_accepted:
        call _shower_solo from _call__shower_solo_1
        return

    # --- Strip each girl and show nude in standing ---
    python:
        for _sg in _shower_accepted:
            _sg.Collar = False
            _sg.Outfit_Change(over="none", mid="none", chest="none", legs="none", panties="none", shoes="none", pose="standing")

    # --- Player sees girl nude: register + reaction per girl ---
    $ _si = 0
    while _si < len(_shower_accepted):
        $ _sg = _shower_accepted[_si]

        $ _exp_b = _sg.RegisterAction("player_saw_boobs")
        if _exp_b["first_time"]:
            call FirstExposureReaction(_sg, "boobs") from _call_FirstExposureReaction_2

        $ _exp_p = _sg.RegisterAction("player_saw_pussy")
        if _exp_p["first_time"]:
            call FirstExposureReaction(_sg, "pussy") from _call_FirstExposureReaction_3

        $ _si += 1

    # --- Player undresses: girl sees penis ---
    "You undress as well."

    $ _si = 0
    while _si < len(_shower_accepted):
        $ _sg = _shower_accepted[_si]
        $ _exp_penis = _sg.RegisterAction("girl_saw_penis")

        if _exp_penis["total"] == 1:
            $ set_scene_expression(_sg, "surprised")
            python:
                _penis_lines = [
                    _("Oh my... you're bigger than I expected."),
                    _("Wow... that's... impressive."),
                    _("I wasn't expecting... all of that."),
                ]
                _penis_line = _tl(renpy.random.choice(_penis_lines))
            $ Say_Line(_sg, _penis_line)
            $ Change_Status(_sg, "Inbt", 25)

        elif _exp_penis["total"] == 2:
            $ Say_Line(_sg, _("Almost forgot how big this is..."))

        elif _exp_penis["total"] == 3:
            $ Say_Line(_sg, _("Heh, I never get tired of seeing this."))

        $ _si += 1

    # --- Girls put on towels ---
    python:
        for _sg in _shower_accepted:
            _sg.Outfit_Change(over="towel", mid="none", chest="none", legs="none", panties="none", shoes="none", pose="standing")

    # --- Register showered together ---
    python:
        for _sg in _shower_accepted:
            _sg.RegisterAction("showered_together")

    if len(_shower_accepted) == 1:
        "You and [_shower_accepted[0].Name] take a shower together."
    else:
        python:
            _names = format_name_list([g.Name for g in _shower_accepted])
        "You all take a shower together... you, [_names]."

    # --- Restore casual outfit on accepted girls + clear temp flags ---
    python:
        for _sg in _shower_accepted:
            _sg.Collar = _sg.has_collar_art()
            _sg.WearPreset("casual", apply_now=False)
        for _sg in _shower_declined:
            _sg._shower_just_declined = False

    call Apply_Time_Cost(TIME_COSTS["shower"]) from _call_Apply_Time_Cost_1
    return

# ============================================================
# Solo shower... random girl walk-in event
# ============================================================
label _shower_solo:

    "You step into the shower."

    # 30% chance a girl walks in; if a girl just declined, she's more
    # likely to come back (forgot her stuff), so boost to 60%.
    python:
        # Who could walk in (shower_walkin_pool): any girl on campus in the campus showers, only whoever is home in
        # the bathroom of a home. Nobody = no walk-in.
        _walkin_pool = shower_walkin_pool(CurrentLocation)
        _any_declined = any(getattr(g, "_shower_just_declined", False) for g in ALL_GIRLS)
        _walkin_chance = (60 if _any_declined else 30) if _walkin_pool else 0
        _walkin_roll = renpy.random.randint(1, 100)
        print("[SHOWER] solo shower at %s: walk-in pool=%s chance=%d" % (CurrentLocation, [g.gid for g in _walkin_pool], _walkin_chance))

    if _walkin_roll > _walkin_chance:
        # Clear temp flags before leaving
        python:
            for _cg in ALL_GIRLS:
                _cg._shower_just_declined = False
        "You take a quick shower and feel refreshed."
        call Apply_Time_Cost(TIME_COSTS["shower"]) from _call_Apply_Time_Cost_2
        return

    # Pick a girl: prefer the one who just declined (if any)
    # Angry girls never walk in
    python:
        # _walkin_pool: the walk-in teleports her here, so never a girl who is away (giving birth) or, in the
        # campus showers, one who lives off campus
        _walkin_candidates = [g for g in _walkin_pool if not (hasattr(g, "has_temp_status") and g.has_temp_status("angry"))]
        if not _walkin_candidates:
            _walkin_candidates = list(_walkin_pool)
        _declined_girls = [g for g in _walkin_candidates if getattr(g, "_shower_just_declined", False)]
        if _declined_girls and renpy.random.randint(1, 100) <= 70:
            _walkin_girl = renpy.random.choice(_declined_girls)
        else:
            _walkin_girl = renpy.random.choice(_walkin_candidates)

        if not isinstance(_walkin_girl, Girl):
            print("[SHOWER] BUG: _walkin_girl is %s (%s), falling back" % (type(_walkin_girl).__name__, _walkin_girl))
            _walkin_girl = renpy.random.choice(_walkin_pool)

        _walkin_girl.loc = CurrentLocation
        _walkin_girl.SpriteLoc = StageCenter
        set_girl_sprite(_walkin_girl.gid, pose="standing", at_list=[slot_center])

    # --- Check if this girl JUST declined to shower with us ---
    $ _walkin_comeback = getattr(_walkin_girl, "_shower_just_declined", False)

    if _walkin_comeback:
        # She left but came back for something she forgot
        python:
            _walkin_girl._shower_just_declined = False
            _comeback_lines = [
                _("Sorry, I forgot my towel... I didn't think you'd already be naked."),
                _("I left my shampoo, I just need to... oh. You're already undressed."),
                _("Ugh, I forgot my stuff. Don't look at me like that, I'm just grabbing my things."),
                _("I swear I'm not coming back because I changed my mind. I just forgot my conditioner. ...Why are you naked already?"),
            ]
            set_scene_expression(_walkin_girl, "surprised")
            Say_Line(_walkin_girl, _tl(renpy.random.choice(_comeback_lines)))
            _walkin_girl.RegisterAction("girl_walked_in_shower")
            _walkin_girl.RegisterAction("girl_saw_penis")
            Change_Status(_walkin_girl, "Inbt", 30)
    else:
        "The door opens and [_walkin_girl.Name] walks in."

        # --- Girl walked in on player: register ---
        $ _walkin_girl.RegisterAction("girl_walked_in_shower")

        # --- Girl sees player nude: register + reaction ---
        $ _exp_penis = _walkin_girl.RegisterAction("girl_saw_penis")

        # A girl whose story locks showering together (story_steps.rpy): she neither admires nor stays,
        # whatever her stats. She saw it (the fact registered above), and she leaves on her own terms.
        if story_act_locked(_walkin_girl, "shower_join"):
            $ set_scene_expression(_walkin_girl, "angry")
            $ Say_Line(_walkin_girl, story_locked_line(_walkin_girl, "shower_walkin"))
            $ Change_Status(_walkin_girl, "Inbt", 10)
            python:
                print("[SHOWER] %s walked in but her story locks shower_join: she leaves" % _walkin_girl.gid)
                _walkin_girl.loc = _walkin_girl.home
                hide_girl_sprite(_walkin_girl)
            "The door closes hard enough to rattle the mirror."
            "You finish your shower alone."
            call Apply_Time_Cost(TIME_COSTS["shower"]) from _call_Apply_Time_Cost_shower_story
            return

        if _exp_penis["total"] == 1:
            $ set_scene_expression(_walkin_girl, "surprised")
            python:
                _penis_lines = [
                    _("Oh my... you're bigger than I expected."),
                    _("Wow... that's... impressive."),
                    _("I wasn't expecting... all of that."),
                ]
                _penis_line = _tl(renpy.random.choice(_penis_lines))
            $ Say_Line(_walkin_girl, _penis_line)
            $ Change_Status(_walkin_girl, "Inbt", 50)

        elif _exp_penis["total"] == 2:
            $ Say_Line(_walkin_girl, _("Almost forgot how big this is..."))

        elif _exp_penis["total"] == 3:
            $ Say_Line(_walkin_girl, _("Heh, I never get tired of seeing this."))

    # --- Decide outcome based on stats ---
    python:
        _best = max(getattr(_walkin_girl, "Love", 0), getattr(_walkin_girl, "Inbt", 0))
        # Sexual history lowers the bar: +50 per sex act, capped at +200
        # Acts only ("sex" + "anal"): positions are preferences, adding them counted one scene twice
        _best += sex_history_bonus(_walkin_girl)   # numbers live in SEX_HISTORY_THRESHOLDS
        _has_seen = _walkin_girl.HasSeen("player_saw_boobs") or _walkin_girl.HasSeen("player_saw_pussy")
        if _has_seen:
            _high_threshold = 400
            _mid_threshold = 200
        else:
            _high_threshold = 600
            _mid_threshold = 350

    # --- Comeback girl: she decides based on stats too ---
    # (The comeback intro already played; now decide if she stays or leaves)
    if _walkin_comeback and _best >= _mid_threshold:
        python:
            _comeback_stay_lines = [
                _("Well... since I'm already here again, I might as well stay."),
                _("Fine, fine. I'll just... stay this time. Don't make it weird."),
                _("Okay, okay. You win. Move over."),
            ]
            Say_Line(_walkin_girl, _tl(renpy.random.choice(_comeback_stay_lines)))
        call _shower_walkin_join(_walkin_girl) from _call__shower_walkin_join
        return

    if _walkin_comeback and _best < _mid_threshold:
        python:
            _walkin_girl._shower_just_declined = False
            Say_Line(_walkin_girl, _("Anyway, I got what I needed. Bye."))
            _walkin_girl.loc = _walkin_girl.home
            hide_girl_sprite(_walkin_girl)
        "She grabs her things and leaves quickly."
        "You finish your shower alone."
        call Apply_Time_Cost(TIME_COSTS["shower"]) from _call_Apply_Time_Cost_3
        return

    # --- HIGH: she joins automatically ---
    if _best >= _high_threshold:
        python:
            _join_lines = [
                _("Well... since I'm already here."),
                _("Don't mind if I do."),
                _("Looks like there's room for two."),
            ]
            Say_Line(_walkin_girl, _tl(renpy.random.choice(_join_lines)))
        call _shower_walkin_join(_walkin_girl) from _call__shower_walkin_join_2
        return

    # --- LOW: she apologizes and leaves ---
    if _best < _mid_threshold:
        python:
            _leave_lines = [
                _("S-sorry! I didn't know anyone was in here!"),
                _("Oh! I... I'll come back later!"),
                _("Excuse me! I'm so sorry!"),
                _("I didn't see anything! ...much."),
            ]
            Say_Line(_walkin_girl, _tl(renpy.random.choice(_leave_lines)))
            _walkin_girl.loc = _walkin_girl.home
            hide_girl_sprite(_walkin_girl)

        "She quickly leaves."
        "You finish your shower alone."
        call Apply_Time_Cost(TIME_COSTS["shower"]) from _call_Apply_Time_Cost_4
        return

    # --- MID: player asks, girl decides ---
    $ Say_Player(_("Want to join me?"))

    python:
        # 50/50 based on proximity to high threshold
        _accept_chance = 30 + int(40 * (_best - _mid_threshold) / max(1, _high_threshold - _mid_threshold))
        _accept_roll = renpy.random.randint(1, 100)
        _mid_accepts = (_accept_roll <= _accept_chance)

    if _mid_accepts:
        python:
            _mid_accept_lines = [
                _("I... okay, sure."),
                _("Well... I guess it's fine."),
                _("You're bold, I'll give you that. Alright."),
            ]
            Say_Line(_walkin_girl, _tl(renpy.random.choice(_mid_accept_lines)))
        call _shower_walkin_join(_walkin_girl) from _call__shower_walkin_join_1
        return
    else:
        python:
            _mid_decline_lines = [
                _("I... don't think that's a good idea."),
                _("Maybe next time."),
                _("Not today..."),
                _("I'd rather not."),
            ]
            Say_Line(_walkin_girl, _tl(renpy.random.choice(_mid_decline_lines)))
            _walkin_girl.loc = _walkin_girl.home
            hide_girl_sprite(_walkin_girl)

        "She leaves."
        "You finish your shower alone."
        call Apply_Time_Cost(TIME_COSTS["shower"]) from _call_Apply_Time_Cost_5
        return

# --- Helper: girl joins the shower after walk-in ---
label _shower_walkin_join(girl):

    # Strip top
    python:
        _strip_top_lines = [
            _("She pulls her top off, dropping it casually to the side."),
            _("She reaches for the hem of her shirt and lifts it over her head."),
            _("With a quick pull, she removes her top and tosses it aside."),
        ]
    $ Narration(_tl(renpy.random.choice(_strip_top_lines)))
    $ girl.Collar = False
    $ girl.Outfit_Change(over="none", mid="none", chest="none")
    $ set_girl_sprite(girl, pose="standing", at_list=[slot_center])
    call CheckExposure(girl) from _call_CheckExposure_walkin_top

    # Strip bottom
    python:
        _strip_bot_lines = [
            _("She slides her bottoms down, stepping out of them."),
            _("She hooks her thumbs into her waistband and pushes everything down."),
            _("Without hesitation, she pushes the rest off and kicks them aside."),
        ]
    $ Narration(_tl(renpy.random.choice(_strip_bot_lines)))
    $ girl.Outfit_Change(legs="none", panties="none", shoes="none")
    $ set_girl_sprite(girl, pose="standing", at_list=[slot_center])
    call CheckExposure(girl) from _call_CheckExposure_walkin_bot

    # Grab towel
    python:
        _towel_lines = [
            _("She grabs a towel from the rack and wraps it around herself."),
            _("She picks up a towel and wraps it loosely around her body."),
            _("She reaches for a nearby towel and covers up."),
        ]
    $ Narration(_tl(renpy.random.choice(_towel_lines)))
    $ girl.Outfit_Change(over="towel", mid="none", chest="none", legs="none", panties="none", shoes="none", pose="standing")
    $ set_girl_sprite(girl, pose="standing", at_list=[slot_center])

    # Register showered together
    $ girl.RegisterAction("showered_together")

    "You and [girl.Name] take a shower together."

    # Restore casual outfit + clear temp flags
    python:
        girl.Collar = girl.has_collar_art()
        girl.WearPreset("casual", apply_now=False)
        girl._shower_just_declined = False
        for _cg in ALL_GIRLS:
            _cg._shower_just_declined = False

    call Apply_Time_Cost(TIME_COSTS["shower"]) from _call_Apply_Time_Cost_shower_join
    return

# Room / Girl Room: Study
label do_study:

    if (100 - Round) < TIME_COSTS["study_min"]:
        "It's too late to study right now. Try again next time slot."
        return

    # Which girls share this location with the player?
    $ _study_girls = [g for g in ALL_GIRLS if g.loc == CurrentLocation]

    if _study_girls:
        # Studying together: player +2 (Fast Learner: +4), each girl present +2, Love +3
        # Girls studying together also bond (+15 friendship with each other)
        python:
            _study_gain = 4 if getattr(Player, "player_trait", "") == "fast_learner" else 2
            Player.study_level += _study_gain
            _study_routine_girls = []
            for _g in _study_girls:
                _g.study_level += (4 if _g.has_trait("nerd") else 2)
                Change_Status(_g, "Love", 3)
                if callable(globals().get("_buddy_increment", None)):
                    _buddy_increment(_g, "study")
                    if _buddy_is_routine(_g, "study"):
                        Player.study_level += 1
                        _study_routine_girls.append(_g)
            # Friendship boost between all girls present
            for _i in range(len(_study_girls)):
                for _j in range(_i + 1, len(_study_girls)):
                    _study_girls[_i].add_like_for(_study_girls[_j].gid, 50)
                    _study_girls[_j].add_like_for(_study_girls[_i].gid, 50)
            _names = format_name_list([g.Name for g in _study_girls])

        "You study together with [_names]. It feels productive."
        "Your study level: [Player.study_level]."

        if _study_routine_girls:
            $ _routine_names = format_name_list([g.Name for g in _study_routine_girls])
            $ renpy.say(None, _tl(_("Studying with %s has become a routine. You learn faster together. {b}+1 Study Level{/b}.")) % _routine_names)
    else:
        # Studying alone: player +1 (Fast Learner: +2)
        $ Player.study_level += (2 if getattr(Player, "player_trait", "") == "fast_learner" else 1)
        "You sit down and study on your own. Not bad."
        "Your study level: [Player.study_level]."

    # Consume all remaining time in the current slot (same as Attend Class)
    $ _study_cost = 100 - Round
    call Apply_Time_Cost(_study_cost) from _call_Apply_Time_Cost_6
    return

# Room: Sleep
label do_sleep:
    # Safety: if _time_locked is stuck from a stale save, unlock it
    python:
        if getattr(store, "_time_locked", False):
            debug_log("[DO_SLEEP] Clearing stuck _time_locked")
            store._time_locked = False

    # Her story (story_steps.rpy, "sleep"): a knock at his door as he goes to bed. He sleeps after it
    if CurrentLocation == "room":
        python:
            for _dbg_g in story_girls():
                _dbg_ev = story_unlock_event(_dbg_g)
                if _dbg_ev:
                    _dbg_fits = _story_event_fits(_dbg_g, _dbg_ev, "sleep")
                    _dbg_route = story_unlock_route(_dbg_g)
                    _dbg_e = STORY_EVENTS.get(_dbg_ev, {})
                    _dbg_req_fn = _dbg_e.get("requires")
                    _dbg_req_val = globals()[_dbg_req_fn](_dbg_g) if _dbg_req_fn and _dbg_req_fn in globals() else "-"
                    print("[DO_SLEEP] story check %s: ev=%s step=%d ti=%d fits=%s route=%s where=%s alone=%s angry=%s requires=%s(%s) slot_min=%s" % (
                        _dbg_g.gid, _dbg_ev, story_step(_dbg_g), TimeIndex, _dbg_fits, _dbg_route,
                        CurrentLocation in (_dbg_e.get("where") or (CurrentLocation,)),
                        not any(_o is not _dbg_g and _o.loc == CurrentLocation for _o in ALL_GIRLS),
                        _dbg_g.has_temp_status("angry"),
                        _dbg_req_fn or "-", _dbg_req_val, _dbg_e.get("slot_min", 0)))
        $ _story_sleep = story_event_now("sleep")
        if _story_sleep is not None:
            call story_event_play(_story_sleep[0], _story_sleep[1]) from _call_story_event_sleep
        else:
            # her knock could have come tonight and did not: what is missing (story_unlock_hint)
            call story_unlock_hint_say("sleep") from _call_story_hint_sleep

    # Daytime sleep gets a flavour line; nighttime gets the standard line
    if TimeIndex != NIGHT_INDEX:
        $ _sleep_line = _tl(renpy.random.choice(DAYTIME_SLEEP_LINES))
        "[_sleep_line]"
    else:
        "You lie down on the bed and fall asleep for a while."

    # Track consecutive sleeps without leaving the room
    $ consecutive_room_sleeps += 1

    # After 5+ sleeps in a row, break the fourth wall
    if consecutive_room_sleeps >= 5:
        $ _lazy_line = _tl(renpy.random.choice(LAZY_SLEEP_LINES))
        "[_lazy_line]"

    # Snapshot girls present before time change (for Wait dialogue)
    $ LastPresentGirls = [g for g in ALL_GIRLS if g.loc == CurrentLocation]

    # New day always starts with no followers
    $ Party = []

    # Recharge energy to max
    $ Player.recharge_energy()

    # Full night of sleep resets arousal
    python:
        if Player.Focus > 0:
            debug_log("[DO_SLEEP] Player.Focus %d -> 0 (sleep reset)" % Player.Focus)
        Player.Focus = 0

    # Simulate study gains for skipped time slots (do_sleep bypasses advance_time).
    # The CURRENT slot was already credited when it began (TimeIndex + 1, it counted twice),
    # and the Night slot earns nothing: she sleeps.
    python:
        for _sti in range(TimeIndex + 1, 3):
            for _sg in ALL_GIRLS:
                _sched = get_scheduled_location_for(_sg, Day, _sti)
                if _sched == "classroom":
                    _gain = 2 if _sg.has_trait("nerd") else 1
                    _sg.study_level += _gain
                    debug_log("[DO_SLEEP] %s +%d study (classroom at ti=%d)" % (_sg.gid, _gain, _sti))
                else:
                    _sg_home = GIRLS_CONFIG.get(_sg.gid, {}).get("home")
                    if _sg_home and _sched == _sg_home:
                        _sg.study_level += 1
                        debug_log("[DO_SLEEP] %s +1 study (home at ti=%d)" % (_sg.gid, _sti))

    # Sleep cools down girls' Lust before the daily buildup
    python:
        for g in ALL_GIRLS:
            _old_lust = getattr(g, "Lust", 0)
            if _old_lust > 0:
                g.Lust = max(0, _old_lust - 20)
                debug_log("[DO_SLEEP] %s Lust %d -> %d (sleep decay)" % (g.gid, _old_lust, g.Lust))

    # Next morning. ONE central new-day routine for every way the day can roll over (system_time.rpy:
    # start_next_day_manually -> _per_day_cleanup). This label used to hand-copy parts of it and every system
    # added later was missing from the copy: the pregnancy tick never ran when he went to bed through Sleep.
    $ start_next_day_manually()

    scene black
    with fade
    pause 0.5
    "A new day begins."

    # Show room bg before Wait so girl time-change dialogue has a visible scene
    $ renpy.scene()
    $ renpy.show(get_bg_for_location())

    # We still call Wait for generic per-slot logic (Lust decay, etc.)
    call Wait from _call_Wait

    # Refresh the scene for the current location (room) and time
    call Set_Scene(entry=True) from _call_Set_Scene_1

    return

# Classroom: Attend Class
label do_attend_class:

    # Class does not run at night
    if TimeIndex == NIGHT_INDEX:
        "There are no classes at this hour."
        return

    if (100 - Round) < TIME_COSTS["attend_class_min"]:
        "It is getting a bit late for class, maybe it is better to wait for the next time slot."
        return

    $ _class_line = _tl(renpy.random.choice(CLASS_LINES))
    "[_class_line]"

    # +1 study_level for the player (Fast Learner: +2) and any girls also in the classroom
    python:
        Player.study_level += (2 if getattr(Player, "player_trait", "") == "fast_learner" else 1)
        _class_routine_girls = []
        for _g in ALL_GIRLS:
            if _g.loc == "classroom":
                _g.study_level += (2 if _g.has_trait("nerd") else 1)
                if callable(globals().get("_buddy_increment", None)):
                    _buddy_increment(_g, "study")
                    if _buddy_is_routine(_g, "study"):
                        Player.study_level += 1
                        _class_routine_girls.append(_g)

    if _class_routine_girls:
        $ _routine_names = format_name_list([g.Name for g in _class_routine_girls])
        $ renpy.say(None, _tl(_("Attending class with %s has become a routine. You learn faster together. {b}+1 Study Level{/b}.")) % _routine_names)

    # Class events (~14% each when a girl is present, ~14% nothing)
    python:
        _class_present = [g for g in ALL_GIRLS if g.loc == "classroom"]
    if _class_present:
        $ _class_event_roll = renpy.random.randint(1, 7)
        if _class_event_roll == 1:
            call class_event_mock_exam(_class_present[0]) from _call_class_event_mock_exam
        elif _class_event_roll == 2:
            call class_event_during_lecture(_class_present[0]) from _call_class_event_during_lecture
        elif _class_event_roll == 3:
            call class_event_help_her(_class_present[0]) from _call_class_event_help_her
        elif _class_event_roll == 4:
            call class_event_obvious_interruption(_class_present[0]) from _call_class_event_obvious_interruption
        # 5-7 → nothing special happens

    # Consume all remaining time in this slot
    $ _class_cost = 100 - Round
    call Apply_Time_Cost(_class_cost) from _call_Apply_Time_Cost_7

    return

# ============================================================
# CLASS EVENTS... triggered during do_attend_class when a girl is present
# ============================================================

# ---- CLASS EVENT 1: Mock Exam ----
# The teacher hands out a practice test. Player chooses how to behave.
label class_event_mock_exam(girl):
    "The professor hands out a practice exam. The room goes quiet."
    "You glance at the sheet. Some of these questions are brutal."

    menu:
        "Focus quietly on the test":
            "You put your head down and work through the questions one by one."
            "The clock ticks. You finish with a minute to spare."
            python:
                _sl = getattr(Player, "study_level", 0)
            if _sl >= 8:
                "You feel pretty confident about your answers."
            elif _sl >= 4:
                "Some of them were guesses, but you think you did okay."
            else:
                "You have no idea if any of that was right. But at least you tried."
            if girl.has_trait("nerd"):
                $ set_scene_expression(girl, "smile")
                $ Say_Line(girl, _("Good. At least someone here takes this seriously."))
                $ Change_Status(girl, "Love", 3)

        "Hum and whistle a tune":
            "You start humming under your breath. Then tapping your pen. Then whistling."
            "The girl next to you shifts uncomfortably."
            if girl.has_trait("nerd"):
                $ set_scene_expression(girl, "angry")
                $ Say_Line(girl, _("Are you kidding me right now? This is a MOCK EXAM. Grow up."))
                "She slams her pen down, glaring daggers."
                $ Change_Status(girl, "Obed", -8)
                $ Change_Status(girl, "Love", -8)
            elif girl.has_trait("cute_sex"):
                $ set_scene_expression(girl, "uncomfortable")
                $ Say_Line(girl, _("Um... c-can you please stop? I can't concentrate..."))
            elif girl.has_trait("hardcore_sex"):
                $ set_scene_expression(girl, "angry")
                $ Say_Line(girl, _("Hey. Shut up. Some of us are trying to pass."))
            else:
                $ set_scene_expression(girl, "angry")
                $ Say_Line(girl, _("Can you stop? You're driving me crazy."))
            "The professor shoots you a warning look. You stop... eventually."
            if not girl.has_trait("nerd"):
                $ Change_Status(girl, "Obed", -5)
                $ Change_Status(girl, "Love", -3)

        "Lean over and ask her for answers":
            "You lean toward her and whisper."
            $ Say_Player(_("Hey... what'd you get for number three?"))
            if girl.has_trait("nerd"):
                $ set_scene_expression(girl, "disgusted")
                $ Say_Line(girl, _("Do your own work. I'm not your cheat sheet."))
                "She covers her paper with her arm and doesn't look at you again."
                $ Change_Status(girl, "Love", -5)
                $ Change_Status(girl, "Obed", -5)
            elif girl.has_trait("cute_sex"):
                $ set_scene_expression(girl, "scared")
                $ Say_Line(girl, _("W-what?! We'll get caught...!"))
                "She glances at the professor, then reluctantly tilts her paper."
                $ Say_Line(girl, _("...J-just this once. Don't look so obviously."))
                $ Change_Status(girl, "Obed", 8)
                $ Change_Status(girl, "Inbt", 5)
            elif girl.has_trait("hardcore_sex"):
                $ set_scene_expression(girl, "angry")
                $ Say_Line(girl, _("Are you serious? Study next time."))
                "She stares at you for a moment, then sighs."
                $ Say_Line(girl, _("Fine. But you owe me. Don't forget."))
                $ Change_Status(girl, "Obed", 8)
                $ Change_Status(girl, "Inbt", 5)
            elif girl.has_trait("loyal"):
                $ set_scene_expression(girl, "worried")
                $ Say_Line(girl, _("This is wrong... but okay. Just be subtle about it."))
                $ Change_Status(girl, "Obed", 8)
                $ Change_Status(girl, "Inbt", 5)
            else:
                $ set_scene_expression(girl, "bemused")
                $ Say_Line(girl, _("...Really? Ugh, fine. But don't make it obvious."))
                "She angles her paper slightly so you can see."
                $ Change_Status(girl, "Obed", 8)
                $ Change_Status(girl, "Inbt", 5)

    return

# ---- CLASS EVENT 2: During the Lecture ----
# Mid-lecture choices: chat with her, pay attention, or answer the professor.
label class_event_during_lecture(girl):
    "The professor is deep into today's topic. Most of the class looks half-asleep."

    menu:
        "Chat with her":
            "You lean toward her and whisper something about how boring this lecture is."
            if girl.has_trait("nerd"):
                $ set_scene_expression(girl, "annoyed")
                $ Say_Line(girl, _("I'm trying to listen. This is actually important."))
                "She turns back to her notes without another word."
                $ Change_Status(girl, "Love", -3)
            elif girl.has_trait("cute_sex"):
                $ set_scene_expression(girl, "shy", blush=1)
                $ Say_Line(girl, _("Shh...! We're going to get in trouble...!"))
                "She covers her mouth to hide a giggle."
                $ Say_Line(girl, _("...Okay, but keep your voice down."))
                $ Change_Status(girl, "Love", 5)
                $ Change_Status(girl, "Inbt", 3)
            elif girl.has_trait("hardcore_sex"):
                $ set_scene_expression(girl, "smirk")
                $ Say_Line(girl, _("Yeah, this lecture is dogshit. What else is new."))
                "She doesn't even bother whispering."
                $ Change_Status(girl, "Love", 5)
                $ Change_Status(girl, "Inbt", 3)
            elif girl.has_trait("public_shy"):
                $ set_scene_expression(girl, "worried")
                $ Say_Line(girl, _("Not here... what if the professor notices?"))
                "She whispers back anyway, glancing at the front nervously."
                $ Change_Status(girl, "Love", 5)
                $ Change_Status(girl, "Inbt", 3)
            else:
                $ set_scene_expression(girl, "smile")
                $ Say_Line(girl, _("Tell me about it. I've been zoning out for ten minutes."))
                "You spend the rest of the lecture exchanging quiet comments."
                $ Change_Status(girl, "Love", 5)
                $ Change_Status(girl, "Inbt", 3)

        "Pay attention to the lecture":
            "You focus on the professor's words and take proper notes."
            "Not exciting, but your brain feels a little fuller by the end."
            $ Player.study_level += 1
            if girl.has_trait("nerd"):
                $ set_scene_expression(girl, "smile")
                $ Say_Line(girl, _("See? Not so hard when you actually pay attention."))
                $ Change_Status(girl, "Love", 3)

        "Try to answer the professor's question":
            "The professor poses a question to the class. Silence. You raise your hand."
            python:
                _sl = getattr(Player, "study_level", 0)
                _pass_chance = min(90, 30 + (_sl * 5))
                _correct = renpy.random.randint(1, 100) <= _pass_chance
                debug_log("[CLASS EVENT] answer attempt: study=%d chance=%d correct=%s" % (_sl, _pass_chance, _correct))

            if _correct:
                "You give your answer. The professor nods, impressed."
                "\"Correct. Nice to see someone actually paying attention.\""
                if girl.has_trait("nerd"):
                    $ set_scene_expression(girl, "surprised")
                    $ Say_Line(girl, _("Wait, you actually got that? Okay, maybe you're not hopeless."))
                    $ Change_Status(girl, "Love", 8)
                    $ Change_Status(girl, "Obed", 5)
                elif girl.has_trait("cute_sex"):
                    $ set_scene_expression(girl, "happy")
                    $ Say_Line(girl, _("Wow... you actually knew that? That's really cool..."))
                    $ Change_Status(girl, "Love", 5)
                    $ Change_Status(girl, "Obed", 5)
                elif girl.has_trait("hardcore_sex"):
                    $ set_scene_expression(girl, "smirk")
                    $ Say_Line(girl, _("Huh. Didn't peg you as the studious type. Not bad."))
                    $ Change_Status(girl, "Love", 5)
                    $ Change_Status(girl, "Obed", 5)
                else:
                    "She glances at you with a hint of admiration."
                    $ Change_Status(girl, "Love", 5)
                    $ Change_Status(girl, "Obed", 5)
            else:
                "You give your answer. The professor pauses."
                "\"That's... no. Not even close.\""
                "A few people chuckle. Your face burns."
                if girl.has_trait("nerd"):
                    $ set_scene_expression(girl, "sad")
                    $ Say_Line(girl, _("That wasn't even close... Do you study at all?"))
                    $ Change_Status(girl, "Love", -8)
                    $ Change_Status(girl, "Obed", -5)
                elif girl.has_trait("cute_sex"):
                    $ set_scene_expression(girl, "worried")
                    $ Say_Line(girl, _("It's okay... at least you tried..."))
                    $ Change_Status(girl, "Love", -3)
                    $ Change_Status(girl, "Obed", -3)
                elif girl.has_trait("hardcore_sex"):
                    $ set_scene_expression(girl, "smirk")
                    $ Say_Line(girl, _("Oof. Maybe study more before showing off."))
                    $ Change_Status(girl, "Love", -5)
                    $ Change_Status(girl, "Obed", -5)
                else:
                    "She looks away, second-hand embarrassment on her face."
                    $ Change_Status(girl, "Love", -5)
                    $ Change_Status(girl, "Obed", -5)

    return

# ---- CLASS EVENT 3: She Doesn't Understand ----
# She's struggling with the material. Player can try to help or ignore.
label class_event_help_her(girl):

    if girl.has_trait("nerd"):
        "You notice her breezing through the material while you stare blankly at your own notes."
        "She notices you struggling and sighs."
        $ set_scene_expression(girl, "bemused")
        $ Say_Line(girl, _("Okay, stop. You're making that face again. Let me explain."))
        "She leans over and walks you through it in seconds."
        $ Say_Line(girl, _("There. Not that hard, right?"))
        $ Player.study_level += 1
        $ Change_Status(girl, "Love", 3)
        $ Change_Status(girl, "Obed", 5)
        return

    "You notice her frowning at her notebook, re-reading the same paragraph over and over."
    "She's clearly lost."

    menu:
        "Try to help her":
            "You lean over and point to the section she's stuck on."
            $ Say_Player(_("Here, look at it this way..."))

            python:
                _sl = getattr(Player, "study_level", 0)
                _help_chance = min(90, 25 + (_sl * 6))
                _helped = renpy.random.randint(1, 100) <= _help_chance
                debug_log("[CLASS EVENT] help attempt: study=%d chance=%d success=%s" % (_sl, _help_chance, _helped))

            if _helped:
                "You explain it in a way that actually makes sense."
                if girl.has_trait("cute_sex"):
                    $ set_scene_expression(girl, "happy")
                    $ Say_Line(girl, _("Oh...! OH! I get it now! You're amazing!"))
                    "She beams at you, genuinely grateful."
                    $ Change_Status(girl, "Love", 8)
                    $ Change_Status(girl, "Obed", 5)
                elif girl.has_trait("hardcore_sex"):
                    $ set_scene_expression(girl, "smile")
                    $ Say_Line(girl, _("...Huh. That actually made sense. Thanks."))
                    "High praise, coming from her."
                    $ Change_Status(girl, "Love", 5)
                    $ Change_Status(girl, "Obed", 5)
                else:
                    $ set_scene_expression(girl, "happy")
                    $ Say_Line(girl, _("Wait... that's all it was? Thank you, I was so confused!"))
                    $ Change_Status(girl, "Love", 8)
                    $ Change_Status(girl, "Obed", 5)
            else:
                "You try to explain, but honestly... you don't fully get it either."
                if girl.has_trait("cute_sex"):
                    $ set_scene_expression(girl, "worried")
                    $ Say_Line(girl, _("I... I think I'm more confused now. But thank you for trying..."))
                elif girl.has_trait("hardcore_sex"):
                    $ set_scene_expression(girl, "angry")
                    $ Say_Line(girl, _("That made zero sense. Did you even study?"))
                else:
                    $ Say_Line(girl, _("I appreciate the effort, but... I don't think you understand it either."))
                $ Change_Status(girl, "Love", 3)

        "Ignore it":
            "You notice her struggling but decide not to get involved."
            "She eventually gives up and stares at the board instead."

    return

# ---- CLASS EVENT 4: Obvious Interruption ----
# A student interrupts the professor to repeat what was just said.
label class_event_obvious_interruption(girl):
    "A student in the front row raises their hand and proceeds to repeat exactly what the professor just said, word for word, as if it were an original thought."
    "The professor pauses. The whole room holds its breath."

    menu:
        "Tell them to shut up":
            $ Say_Player(_("Hey. The professor literally just said that. Sit down."))
            "The room goes silent. The student turns red and sinks into their chair."
            "The professor clears his throat and moves on."
            if girl.has_trait("nerd"):
                $ set_scene_expression(girl, "happy")
                $ Say_Line(girl, _("THANK you. I was about to lose it. People like that waste everyone's time."))
                $ Change_Status(girl, "Love", 8)
                $ Change_Status(girl, "Obed", 8)
            elif girl.has_trait("cute_sex"):
                $ set_scene_expression(girl, "surprised")
                $ Say_Line(girl, _("Oh my god... you actually said it. Everyone was thinking it."))
                $ Change_Status(girl, "Inbt", 5)
                $ Change_Status(girl, "Obed", 8)
            elif girl.has_trait("hardcore_sex"):
                $ set_scene_expression(girl, "happy")
                $ Say_Line(girl, _("Finally. Someone with a backbone in this room."))
                $ Change_Status(girl, "Inbt", 5)
                $ Change_Status(girl, "Obed", 8)
            elif girl.has_trait("public_shy"):
                $ set_scene_expression(girl, "worried")
                $ Say_Line(girl, _("That was kind of harsh... but they DID have it coming."))
                $ Change_Status(girl, "Inbt", 5)
                $ Change_Status(girl, "Obed", 8)
            else:
                "She tries to stifle a laugh."
                $ Say_Line(girl, _("I can't believe you just did that. That was brutal."))
                $ Change_Status(girl, "Inbt", 5)
                $ Change_Status(girl, "Obed", 8)

        "Ignore it":
            "You bite your tongue and let the moment pass."
            "The professor handles it with a polite nod and continues. The student looks pleased with themselves."
            "You exchange a brief glance with her. She rolls her eyes."

        "Make a sarcastic comment":
            $ Say_Player(_("Wow... it's almost like the professor just said that exact thing. Wild."))
            "A few people nearby snicker. The student looks confused, then offended."
            if girl.has_trait("nerd"):
                $ set_scene_expression(girl, "smirk")
                $ Say_Line(girl, _("Subtle but effective. I appreciate someone who values actual intellect."))
                $ Change_Status(girl, "Love", 5)
                $ Change_Status(girl, "Obed", 5)
            elif girl.has_trait("cute_sex"):
                $ set_scene_expression(girl, "laugh")
                "She covers her mouth, trying not to laugh."
                $ Say_Line(girl, _("That was mean... but so accurate."))
                $ Change_Status(girl, "Obed", 5)
                $ Change_Status(girl, "Love", 5)
            elif girl.has_trait("hardcore_sex"):
                $ set_scene_expression(girl, "happy")
                $ Say_Line(girl, _("Ha! Perfect delivery. I respect that."))
                $ Change_Status(girl, "Obed", 5)
                $ Change_Status(girl, "Love", 5)
            elif girl.has_trait("exhibitionist"):
                $ set_scene_expression(girl, "happy")
                $ Say_Line(girl, _("Oh my god, YES. Someone needed to say it."))
                $ Change_Status(girl, "Obed", 5)
                $ Change_Status(girl, "Love", 5)
            else:
                "She presses her lips together, fighting a grin."
                $ Say_Line(girl, _("You didn't have to roast them like that... but I'm glad you did."))
                $ Change_Status(girl, "Obed", 5)
                $ Change_Status(girl, "Love", 5)

    return

# Gym: Work Out
label do_workout:

    # Gym is closed at night
    if TimeIndex == NIGHT_INDEX:
        "The gym is closed at this hour."
        return

    if (100 - Round) < TIME_COSTS["workout_min"]:
        "It's getting a bit late to work out, maybe it's better to wait for the next time slot."
        return

    $ _workout_line = _tl(renpy.random.choice(GYM_WORKOUT_LINES))
    "[_workout_line]"

    $ _energy_gained = Player.register_workout()

    if _energy_gained:
        "All that hard work is paying off. You feel stronger... like you could last longer. {b}Max Energy up!{/b} (Max Energy: [Player.energy_max]/5)"
        if Player.energy_max >= 5:
            $ unlock_achievement("max_fit")

    # Girls working out together also bond (+15 friendship with each other)
    python:
        _present = [g for g in ALL_GIRLS if g.loc == CurrentLocation]
        _workout_routine_girls = []
        for _pg in _present:
            Change_Status(_pg, "Love", 3)
            if callable(globals().get("_buddy_increment", None)):
                _buddy_increment(_pg, "workout")
                if _buddy_is_routine(_pg, "workout"):
                    Change_Status(_pg, "Love", 3)
                    _workout_routine_girls.append(_pg)
        for _i in range(len(_present)):
            for _j in range(_i + 1, len(_present)):
                _present[_i].add_like_for(_present[_j].gid, 50)
                _present[_j].add_like_for(_present[_i].gid, 50)

    if _workout_routine_girls:
        $ _routine_names = format_name_list([g.Name for g in _workout_routine_girls])
        $ renpy.say(None, _tl(_("Working out with %s has become a routine. You push each other harder. {b}+3 Love{/b}.")) % _routine_names)

    # Gym rat energy commentary
    python:
        _gym_rat_girl = None
        for _pg in _present:
            if _pg.has_trait("gym_rat"):
                _gym_rat_girl = _pg
                break

    if _gym_rat_girl is not None:
        # her coaching commentary is the trait showing (audit 2026-10-04)
        $ _gym_rat_girl.discover("discovered_trait_gym_rat")
        $ _em = Player.energy_max
        if _em <= 2:
            $ Say_Line(_gym_rat_girl, _("You look like you've never lifted anything heavier than a textbook."))
            $ Change_Status(_gym_rat_girl, "Love", -3)
        elif _em == 3:
            $ Say_Line(_gym_rat_girl, _("At least you show up. That's more than most guys here can say."))
        elif _em == 4:
            $ Say_Line(_gym_rat_girl, _("You're getting there. Keep pushing."))
            $ Change_Status(_gym_rat_girl, "Love", 3)
        elif _em >= 5:
            $ Say_Line(_gym_rat_girl, _("Not bad. You actually look like you belong here."))
            $ Change_Status(_gym_rat_girl, "Love", 5)
            $ Change_Status(_gym_rat_girl, "Obed", 3)

    # Gym events... ~11% each when a girl is present, ~11% nothing
    if _present:
        $ _gym_event_roll = renpy.random.randint(1, 9)
        if _gym_event_roll == 1:
            call gym_event_arm_suggestion(_present[0]) from _call_gym_event_arm_suggestion
        elif _gym_event_roll == 2:
            call gym_event_bench_press(_present[0]) from _call_gym_event_bench_press
        elif _gym_event_roll == 3:
            call gym_event_leg_swap(_present[0]) from _call_gym_event_leg_swap
        elif _gym_event_roll == 4:
            call gym_event_squat_form(_present[0]) from _call_gym_event_squat_form
        elif _gym_event_roll == 5:
            call gym_event_stretching_help(_present[0]) from _call_gym_event_stretching_help
        elif _gym_event_roll == 6:
            call gym_event_squat_watch(_present[0]) from _call_gym_event_squat_watch
        elif _gym_event_roll == 7:
            call gym_event_exercise_help(_present[0]) from _call_gym_event_exercise_help
        elif _gym_event_roll == 8:
            call gym_event_squat_behind(_present[0]) from _call_gym_event_squat_behind
        # _gym_event_roll == 9 → nothing special happens

    # Capture slot BEFORE time advances (and before any navigation)
    $ _was_evening = (TimeIndex == TIME_NAMES.index("Evening"))

    # Consume time while still at the gym so LastPresentGirls captures
    # only girls actually here, not whoever happens to be at the destination
    $ _workout_cost = 100 - Round
    call Apply_Time_Cost(_workout_cost) from _call_Apply_Time_Cost_8

    # After time is processed, move to campus if still at the gym
    # (the Wait label's closed-location check may have already moved us)
    if _was_evening and CurrentLocation == "gym":
        jump Campus_Entry
    else:
        return

# Any location: Wait
label do_wait:
    # Safety: if _time_locked is stuck from a stale save, unlock it
    python:
        if getattr(store, "_time_locked", False):
            debug_log("[DO_WAIT] Clearing stuck _time_locked")
            store._time_locked = False

    "You spend some time just waiting around."

    # Only add enough to complete the current period (avoids double-skip
    # when Round is already at 100 from a scene that ended on time).
    $ _wait_cost = max(1, 100 - Round)
    call Apply_Time_Cost(_wait_cost) from _call_Apply_Time_Cost_9

    return

# ============================================================
# GYM EVENTS... triggered during do_workout when a girl is present
# ============================================================

# --- Exercise data for arm suggestion event ---
init python:
    _GYM_BICEP_EXERCISES = [
        _("dumbbell curls"),
        _("hammer curls"),
        _("barbell curls"),
        _("concentration curls"),
    ]
    _GYM_TRICEP_EXERCISES = [
        _("tricep dips"),
        _("skull crushers"),
        _("tricep pushdowns"),
        _("overhead tricep extensions"),
    ]
    _GYM_BACK_EXERCISES = [
        _("lat pulldowns"),
        _("seated rows"),
        _("dumbbell rows"),
        _("face pulls"),
    ]
    _GYM_CHEST_EXERCISES = [
        _("bench press"),
        _("incline dumbbell press"),
        _("cable flyes"),
        _("push-ups"),
    ]

    _GYM_HELP_EXERCISES = [
        (_("hip thrusts"), _("She's set up at the bench with a loaded barbell across her hips.")),
        (_("deadlifts"), _("She's standing over a loaded barbell, looking unsure about her grip.")),
        (_("overhead press"), _("She's holding dumbbells at shoulder height, bracing herself.")),
    ]

# ---- EVENT 1: Arm Workout Suggestion ----
# She asks for arm training advice. Correct answers: biceps or triceps.
# Wrong answer (chest/back) → she's confused, loses Love.
label gym_event_arm_suggestion(girl):

    if girl.has_trait("gym_rat"):
        # Gym rat GIVES advice instead of asking
        "She walks over while you're resting between sets, looking at your arms."
        $ Say_Line(girl, _("Your form on those curls is all wrong. You're using momentum, not muscle."))

        menu:
            "Oh yeah? Show me how then.":
                $ Say_Player(_("Alright, show me how it's done."))
                "She grabs a dumbbell and does a perfect slow curl, squeezing at the top."
                $ Say_Line(girl, _("See? Slow. Controlled. Feel the muscle, don't swing it."))
                "You try again with her method. It burns way more."
                $ Say_Line(girl, _("Better. Keep that up and maybe you'll actually get somewhere."))
                $ Change_Status(girl, "Love", 8)
                $ Change_Status(girl, "Obed", 5)

            "I don't need advice from a girl.":
                $ Say_Player(_("Thanks, but I know what I'm doing."))
                $ set_scene_expression(girl, "angry")
                $ Say_Line(girl, _("Right. That's why your arms look like that. My mistake."))
                "She turns away with a dismissive scoff."
                $ Change_Status(girl, "Love", -10)
                $ Change_Status(girl, "Obed", -5)

            "You're right, my bad.":
                $ Say_Player(_("Fair enough. What am I doing wrong?"))
                $ Say_Line(girl, _("Everything. But at least you're asking."))
                "She spends a few minutes fixing your technique. It's humbling, but helpful."
                $ Say_Line(girl, _("There. Now you might actually grow something."))
                $ Change_Status(girl, "Love", 5)
                $ Change_Status(girl, "Obed", 8)

        return

    $ Say_Line(girl, _("Hey... I don't really train arms much. Can you suggest something?"))
    $ Say_Line(girl, _("I want something for my arms. What should I do?"))

    $ _bicep = _tl(renpy.random.choice(_GYM_BICEP_EXERCISES))
    $ _tricep = _tl(renpy.random.choice(_GYM_TRICEP_EXERCISES))
    $ _back = _tl(renpy.random.choice(_GYM_BACK_EXERCISES))
    $ _chest = _tl(renpy.random.choice(_GYM_CHEST_EXERCISES))

    menu:
        "Try [_bicep]. Great for biceps.":
            $ Say_Line(girl, _("Biceps, got it! Let me try..."))
            "She grabs a pair of dumbbells and follows your instructions."
            $ Say_Line(girl, _("Oh, I can feel it already! Thanks!"))
            $ Change_Status(girl, "Love", 5)
            $ Change_Status(girl, "Obed", 3)

        "You should do [_tricep]. It'll tone your arms.":
            $ Say_Line(girl, _("Triceps? Okay, show me how!"))
            "You demonstrate the movement. She watches carefully and copies you."
            $ Say_Line(girl, _("Wow, this burns! But in a good way."))
            $ Change_Status(girl, "Love", 5)
            $ Change_Status(girl, "Obed", 3)

        "Do [_chest]. That'll work your arms.":
            $ Say_Line(girl, _("...That's a chest exercise, isn't it?"))
            "She gives you a skeptical look."
            $ Say_Line(girl, _("I asked for arms, not chest. Do you even know what you're doing?"))
            $ Change_Status(girl, "Love", -3)

        "Do [_back]. Trust me.":
            $ Say_Line(girl, _("...Isn't that for back muscles?"))
            "She looks at you, unimpressed."
            $ Say_Line(girl, _("I said arms. You know... biceps? Triceps? Nevermind, I'll figure it out myself."))
            $ Change_Status(girl, "Love", -3)

    return

# ---- EVENT 2: Bench Press Weight Choice ----
# Player chooses how many plates per side. Outcome depends on energy.
# Too heavy → almost suffocates, she loses respect (Obed -5).
# Too light → nothing happens. Good weight → she admires you (Love +5, Obed +3).
label gym_event_bench_press(girl):
    "You head over to the bench press. She's nearby, stretching between sets."
    "You load the bar and notice her glancing over."

    # Weight thresholds scale with energy (0-5)
    # energy 2 (start): safe_max = 2 plates, sweet_spot = 2
    # energy 5 (max):   safe_max = 4 plates, sweet_spot = 3-4
    $ _energy = Player.energy
    $ _safe_max = _energy + 1    # max plates you can handle (1-6)
    $ _sweet_min = max(1, _energy)  # minimum to impress (1-5)

    menu:
        "1 plate per side":
            $ _plates = 1
        "2 plates per side":
            $ _plates = 2
        "3 plates per side":
            $ _plates = 3
        "4 plates per side":
            $ _plates = 4

    if girl.has_trait("gym_rat"):
        if _plates > _safe_max:
            "You unrack the bar and immediately feel the weight crushing down on you."
            "Your arms tremble. The bar starts sinking toward your chest."
            $ Say_Line(girl, _("...Seriously?"))
            "She walks over and helps you rerack it with one hand, looking disgusted."
            $ Say_Line(girl, _("If you can't lift it, don't load it. That was pathetic."))
            $ Change_Status(girl, "Love", -8)
            $ Change_Status(girl, "Obed", -5)
        elif _plates <= 1:
            "You breeze through the set. She was watching from across the gym."
            $ set_scene_expression(girl, "angry")
            $ Say_Line(girl, _("Dude... there's an old lady next to you lifting double that weight."))
            "She makes a quiet chicken sound and turns away, shaking her head."
            $ Change_Status(girl, "Love", -8)
            $ Change_Status(girl, "Obed", -5)
        elif _plates == 2:
            "You finish the set without much trouble. She glances over, unimpressed."
            $ set_scene_expression(girl, "bemused")
            "She cups her hands around her mouth."
            $ Say_Line(girl, _("Bawk bawk bawk..."))
            "A few people nearby look confused. She stares at you, deadpan."
            $ Say_Line(girl, _("What? I'm just narrating what I see."))
            $ Change_Status(girl, "Love", -5)
        elif _plates == 3:
            "You grind through the set with solid form. She watches, arms crossed."
            $ set_scene_expression(girl, "neutral")
            $ Say_Line(girl, _("Hm. Not bad."))
            "She tilts her head, evaluating."
            $ Say_Line(girl, _("A few more plates and you might actually look like a real man."))
            $ Change_Status(girl, "Love", 3)
        else:
            "You unrack four plates per side and push through the set with raw effort."
            "Your face is twisted with strain, but you don't stop. She watches every single rep."
            $ set_scene_expression(girl, "surprised")
            $ Say_Line(girl, _("...Okay. That's actually legit."))
            "She nods slowly, genuine respect in her eyes."
            $ Say_Line(girl, _("You might not be completely hopeless after all."))
            $ Change_Status(girl, "Love", 8)
            $ Change_Status(girl, "Obed", 8)

    elif _plates > _safe_max:
        # Too heavy... almost suffocates
        "You unrack the bar and immediately feel the weight crushing down on you."
        "Your arms tremble. The bar starts sinking toward your chest."
        $ Say_Line(girl, _("Hey... are you okay?!"))
        "She rushes over and helps you rerack the bar. You sit up, gasping."
        $ Say_Line(girl, _("What were you thinking?! You could've hurt yourself!"))
        "She looks more annoyed than worried. Trying to show off clearly backfired."
        $ Change_Status(girl, "Obed", -5)

    elif _plates >= _sweet_min:
        # Good weight... impressive effort
        "You push through the set with visible effort. Your muscles burn, but you keep solid form."
        "You rack the bar and sit up, breathing hard."
        $ Say_Line(girl, _("Damn... that was actually impressive."))
        "She watched the whole set. There's a hint of admiration in her eyes."
        $ Change_Status(girl, "Love", 5)
        $ Change_Status(girl, "Obed", 3)

    else:
        # Too light... no reaction
        "You breeze through the set without breaking a sweat."
        "She glances over briefly but doesn't seem particularly impressed."

    return

# ---- EVENT 3: Leg Exercise Swap ----
# She asks to share the leg press/squat rack. Player chooses response.
label gym_event_leg_swap(girl):
    python:
        _leg_exercises = [
            _("the leg press"),
            _("the squat rack"),
            _("the leg extension machine"),
        ]
        _exercise = _tl(renpy.random.choice(_leg_exercises))

    "You're in the middle of using [_exercise] when she walks over."

    if girl.has_trait("gym_rat"):
        $ Say_Line(girl, _("Move it. I need that for my next superset."))

        menu:
            "Work in with me.":
                $ Say_Player(_("We can alternate sets. I'm between reps anyway."))
                $ Say_Line(girl, _("Fine. But don't take forever resting."))
                "You trade sets back and forth. She pushes heavy weight with zero hesitation."
                "By the end, you're both drenched in sweat."
                $ Say_Line(girl, _("Not bad. You actually keep up."))
                $ Change_Status(girl, "Love", 8)
                $ Change_Status(girl, "Obed", 5)

            "I was here first. Wait your turn.":
                $ Say_Player(_("I've got three more sets. You can wait."))
                $ set_scene_expression(girl, "smug")
                $ Say_Line(girl, _("Respect. At least you're not a pushover."))
                "She leans against the wall, watching your form while she waits."
                $ Change_Status(girl, "Love", 3)
                $ Change_Status(girl, "Obed", 5)

            "All yours, I'm done anyway.":
                $ Say_Player(_("Take it, I'm done."))
                $ set_scene_expression(girl, "bemused")
                $ Say_Line(girl, _("Already? You barely did anything."))
                "She loads more weight on without a second glance at you."
                $ Change_Status(girl, "Love", -5)

    else:
        $ Say_Line(girl, _("Hey, mind if we take turns? I need to use that too."))

        menu:
            "Sure, go ahead.":
                $ Say_Player(_("Yeah, all yours."))
                $ Say_Line(girl, _("Thanks! I'll be quick."))
                "She adjusts the weight and does her set. You wait, watching her form."
                "When she's done, she steps aside with a smile."
                $ Say_Line(girl, _("Your turn. Thanks for sharing!"))
                $ Change_Status(girl, "Love", 5)

            "No, I'm still using it.":
                $ Say_Player(_("I've got a few more sets. You'll have to wait."))
                "She crosses her arms, clearly not thrilled."
                $ Say_Line(girl, _("Seriously? Fine."))
                "She walks off to do something else. You finish your sets in peace."
                $ Change_Status(girl, "Love", -5)
                $ Change_Status(girl, "Obed", 10)

            "Let me give you some tips on your form first.":
                $ Say_Player(_("Actually, let me show you how to do it properly first."))
                $ Say_Line(girl, _("...I didn't ask for tips. I just wanted to use the machine."))
                "She gives you a flat look and walks away to use something else."
                "Note to self: don't mansplain at the gym."
                $ Change_Status(girl, "Love", -5)
                $ Change_Status(girl, "Obed", 5)

    return

# ---- EVENT 4: Squat Form Check ----
# She's doing squats and asks if her form is good.
# Player can look at her legs (correct), her ass (risky), or ignore.
label gym_event_squat_form(girl):

    if girl.has_trait("gym_rat"):
        "She's at the squat rack, crushing a heavy set with perfect form."
        "She racks the bar and catches you watching."
        $ Say_Line(girl, _("See something you like, or are you just taking notes?"))

        menu:
            "Your form is solid. Impressive depth.":
                $ Say_Player(_("Honestly? Perfect depth. Most guys can't squat that low."))
                $ set_scene_expression(girl, "happy")
                $ Say_Line(girl, _("'Most guys'. Low bar, but I'll take it."))
                "She loads another plate on each side."
                $ Say_Line(girl, _("Watch this."))
                $ Change_Status(girl, "Love", 8)
                $ Change_Status(girl, "Obed", 3)

            "Can you teach me your squat technique?":
                $ Say_Player(_("Actually... my squat sucks. Any tips?"))
                $ set_scene_expression(girl, "smug")
                $ Say_Line(girl, _("Finally, a man who can admit when he needs help."))
                "She spends five minutes fixing your stance, hip hinge, and depth."
                $ Say_Line(girl, _("There. Now do ten reps before your body forgets."))
                $ Change_Status(girl, "Love", 5)
                $ Change_Status(girl, "Obed", 10)

            "Stare at her ass while she squats":
                "You position yourself behind her for the next set."
                "She catches your gaze in the mirror immediately."
                $ set_scene_expression(girl, "angry")
                $ Say_Line(girl, _("I know exactly where you're looking. Try harder to be subtle next time."))
                $ Say_Line(girl, _("...Or don't. I don't care. Just don't pretend it's about form."))
                $ Change_Status(girl, "Inbt", 5)

        return

    "She's at the squat rack, mid-set, when she pauses and turns to you."
    $ Say_Line(girl, _("Hey, can you check my form? I don't want to hurt my knees."))

    menu:
        "Watch her legs and give actual advice":
            $ Say_Player(_("Keep your knees tracking over your toes. Push through your heels."))
            "She does another rep, focusing on your instructions."
            $ Say_Line(girl, _("Like this?"))
            $ Say_Player(_("Perfect. Much better."))
            $ Say_Line(girl, _("Thanks! I always feel like I'm doing it wrong."))
            "She finishes her set with a grateful smile."
            $ Change_Status(girl, "Love", 5)
            $ Change_Status(girl, "Obed", 3)

        "Stare at her ass while 'checking form'":
            "You position yourself behind her for a... better angle."
            "She does a few reps. You're definitely not looking at her knees."

            python:
                _inbt = getattr(girl, "Inbt", 0)
                _noticed = renpy.random.randint(1, 100) <= 60

            if _noticed and _inbt < 400:
                "She catches your gaze in the mirror and stops mid-rep."
                $ Say_Line(girl, _("...You're not looking at my form at all, are you?"))
                $ set_scene_expression(girl, "angry")
                $ Say_Line(girl, _("Unbelievable. I ask for help and you just stare at my ass."))
                $ Change_Status(girl, "Love", -5)
                $ Change_Status(girl, "Inbt", 5)
                $ Change_Status(girl, "Obed", 10)
            elif _noticed:
                "She catches your gaze in the mirror... and smirks."
                $ Say_Line(girl, _("Enjoying the view back there?"))
                $ set_scene_expression(girl, "sexy")
                $ Say_Line(girl, _("At least you're honest about it."))
                $ Change_Status(girl, "Love", 3)
                $ Change_Status(girl, "Inbt", 8)
                $ Change_Status(girl, "Obed", 10)
            else:
                "She doesn't seem to notice where you're actually looking."
                $ Say_Line(girl, _("So? How's my form?"))
                $ Say_Player(_("Looks great from here."))
                $ Say_Line(girl, _("Thanks!"))
                $ Change_Status(girl, "Love", 3)
                $ Change_Status(girl, "Inbt", 3)

    return

# ---- EVENT 5: Stretching Help ----
# She's trying to stretch and asks for assistance.
# Player can help properly, get too close, or decline.
label gym_event_stretching_help(girl):

    if girl.has_trait("gym_rat"):
        "After her workout, she's doing a full split on the mat like it's nothing."
        "She notices you watching and smirks."
        $ Say_Line(girl, _("What? Never seen someone who actually stretches after training?"))

        menu:
            "That's impressive flexibility.":
                $ Say_Player(_("That's seriously impressive. I can barely touch my toes."))
                $ Say_Line(girl, _("That's because you skip mobility work. Like everyone else here."))
                "She stands up and crosses her arms."
                $ Say_Line(girl, _("Ten minutes of stretching after every session. No excuses."))
                $ Change_Status(girl, "Love", 5)
                $ Change_Status(girl, "Obed", 3)

            "Bet I can stretch further than you.":
                $ Say_Player(_("Bet I'm more flexible than you think."))
                $ set_scene_expression(girl, "smug")
                $ Say_Line(girl, _("Oh really? Prove it. Sit down."))
                "You try to match her stretch. Your hamstrings scream."
                python:
                    _energy = Player.energy_max
                if _energy >= 4:
                    "You manage a decent stretch, not matching her but not embarrassing either."
                    $ Say_Line(girl, _("Hm. Not terrible. At least your body isn't completely stiff."))
                    $ Change_Status(girl, "Love", 5)
                    $ Change_Status(girl, "Obed", 5)
                else:
                    "You barely get halfway. She watches with visible disappointment."
                    $ Say_Line(girl, _("...Wow. You're like a wooden plank with legs."))
                    $ Change_Status(girl, "Love", -3)

            "I don't really stretch.":
                $ Say_Player(_("I usually skip that part."))
                $ set_scene_expression(girl, "angry")
                $ Say_Line(girl, _("Of course you do. And then you'll complain about injuries later."))
                "She turns back to her mat, dismissing you."
                $ Say_Line(girl, _("Come talk to me when you take training seriously."))
                $ Change_Status(girl, "Love", -5)
                $ Change_Status(girl, "Obed", -3)

        return

    "After her workout, she's on the mat trying to stretch her legs."
    $ Say_Line(girl, _("Ugh... I can never reach far enough on my own."))
    "She looks at you."
    $ Say_Line(girl, _("Can you help me stretch? Just push on my back a little."))

    menu:
        "Help her stretch properly":
            "You kneel behind her and gently press on her upper back as she reaches forward."
            $ Say_Line(girl, _("Ahh... yes, right there... a little more..."))
            "You push a bit further. She groans as the stretch deepens."
            $ Say_Line(girl, _("Oh god, that feels so good. I needed that."))
            "She sits back up, looking relieved."
            $ Say_Line(girl, _("Thanks. My hamstrings were killing me."))
            $ Change_Status(girl, "Love", 5)
            $ Change_Status(girl, "Obed", 3)

        "Help her... and get a little too close":
            "You move in close, pressing your hands on her lower back."
            "Your body is practically against hers as you push her forward."

            python:
                _inbt = getattr(girl, "Inbt", 0)
                _love = getattr(girl, "Love", 0)

            if _inbt >= 500 or _love >= 600:
                $ Say_Line(girl, _("You're... really close right now."))
                $ set_scene_expression(girl, "shy")
                "She doesn't pull away. If anything, she leans back into you slightly."
                $ Say_Line(girl, _("...Don't stop though. It feels nice."))
                $ Change_Status(girl, "Love", 5)
                $ Change_Status(girl, "Inbt", 10)
                $ Change_Status(girl, "Lust", 5)
            else:
                "She tenses up immediately."
                $ Say_Line(girl, _("Hey... you're way too close. Back up."))
                $ set_scene_expression(girl, "angry")
                "You step back awkwardly."
                $ Say_Line(girl, _("I asked for a stretch, not a cuddle session."))
                $ Change_Status(girl, "Love", -5)
                $ Change_Status(girl, "Obed", 5)

        "I'm not really good at stretching, sorry.":
            $ Say_Player(_("I'm not the best at that stuff. Don't want to hurt you."))
            $ Say_Line(girl, _("It's fine, I'll manage on my own."))
            "She goes back to stretching alone. A missed opportunity, but no harm done."

    return

# ---- EVENT 6: Squat Watch ----
# Player sees her doing squats. Can ignore, slap her ass, or compliment.
label gym_event_squat_watch(girl):
    "She's at the squat rack doing a heavy set. You can see her legs trembling on the last rep."
    "She racks the bar and catches her breath, stretching between sets."

    if girl.has_trait("gym_rat"):
        menu:
            "Ignore and keep training":
                "You glance away and continue your own workout."

            "Compliment her strength":
                $ Say_Player(_("That's some serious weight. How long have you been squatting that heavy?"))
                $ set_scene_expression(girl, "happy")
                $ Say_Line(girl, _("About two years of not skipping leg day. Unlike some people."))
                "She looks at your legs pointedly."
                python:
                    _energy = Player.energy_max
                if _energy >= 4:
                    $ Say_Line(girl, _("...Though you look like you put in the work too. Respect."))
                    $ Change_Status(girl, "Love", 8)
                    $ Change_Status(girl, "Obed", 5)
                else:
                    $ Say_Line(girl, _("But seriously, do some squats. Your legs need work."))
                    $ Change_Status(girl, "Love", 3)

            "Challenge her to add more weight":
                $ Say_Player(_("That looked easy. Bet you can do more."))
                $ set_scene_expression(girl, "smug")
                $ Say_Line(girl, _("Oh, you think so?"))
                "She loads an extra plate on each side and crushes three reps."
                "She racks the bar and turns to you, barely winded."
                $ Say_Line(girl, _("Your turn. Same weight."))
                python:
                    _energy = Player.energy_max
                if _energy >= 4:
                    "You step up and manage two solid reps. It's ugly, but you don't fail."
                    $ Say_Line(girl, _("...Huh. Alright. You've earned a spot at my rack."))
                    $ Change_Status(girl, "Love", 10)
                    $ Change_Status(girl, "Obed", 8)
                else:
                    "You step up and the bar nearly buries you on the first rep. She has to help you rerack."
                    $ Say_Line(girl, _("Don't write checks your legs can't cash."))
                    $ Change_Status(girl, "Love", -5)
                    $ Change_Status(girl, "Obed", -3)

        return

    menu:
        "Ignore and keep training":
            "You glance away and continue your own workout."

        "Slap her ass":
            "You walk up behind her and give her a firm slap on the ass."
            $ set_scene_expression(girl, "surprised")

            python:
                _love = getattr(girl, "Love", 0)
                _inbt = getattr(girl, "Inbt", 0)

            if girl.has_trait("hardcore_sex"):
                if _love >= 500 or _inbt >= 400:
                    $ set_scene_expression(girl, "sexy")
                    $ Say_Line(girl, _("You've got some nerve. ...I kinda like that."))
                    "She shoves your shoulder, but she's smirking."
                    $ Change_Status(girl, "Love", -3)
                    $ Change_Status(girl, "Obed", 10)
                    $ Change_Status(girl, "Inbt", 5)
                else:
                    $ set_scene_expression(girl, "angry")
                    $ Say_Line(girl, _("Try that again and I'll break your wrist. I'm not kidding."))
                    $ Change_Status(girl, "Love", -10)
                    $ Change_Status(girl, "Obed", 8)
            elif girl.has_trait("cute_sex"):
                $ set_scene_expression(girl, "embarrassed")
                $ Say_Line(girl, _("E-eek...! W-why would you do that...?!"))
                "Her eyes are watering. She covers herself with both hands."
                $ Change_Status(girl, "Love", -10)
                $ Change_Status(girl, "Obed", 12)
            elif girl.has_trait("exhibitionist"):
                $ set_scene_expression(girl, "shy", blush=1)
                $ Say_Line(girl, _("...Do that again and I'll slap you back. Maybe."))
                "She turns away, but you catch a faint smile."
                $ Change_Status(girl, "Love", -3)
                $ Change_Status(girl, "Obed", 10)
                $ Change_Status(girl, "Inbt", 5)
            elif girl.has_trait("public_shy"):
                $ set_scene_expression(girl, "scared")
                $ Say_Line(girl, _("Oh my god... people are LOOKING! Why would you do that here?!"))
                "Her face turns bright red. She practically runs to the locker room."
                $ Change_Status(girl, "Love", -10)
                $ Change_Status(girl, "Obed", 8)
                $ Change_Status(girl, "Inbt", 8)
            elif _love >= 600 or _inbt >= 500:
                $ set_scene_expression(girl, "shy", blush=1)
                $ Say_Line(girl, _("Hey...! Not here, you idiot."))
                "She swats your hand away, but can't quite hide the flush on her cheeks."
                $ Change_Status(girl, "Love", -5)
                $ Change_Status(girl, "Obed", 10)
            else:
                $ set_scene_expression(girl, "angry")
                $ Say_Line(girl, _("What the HELL?! Don't touch me like that!"))
                "A few people nearby glance over. She's furious."
                $ Change_Status(girl, "Love", -10)
                $ Change_Status(girl, "Obed", 8)

        "Compliment her form":
            $ Say_Player(_("Your squats look really good. Whatever you're doing is working."))
            if girl.has_trait("cute_sex"):
                $ set_scene_expression(girl, "shy", blush=2)
                $ Say_Line(girl, _("R-really? You think so? I never know if I'm doing them right..."))
                "She fidgets with the hem of her shirt, clearly flustered."
            elif girl.has_trait("hardcore_sex"):
                $ set_scene_expression(girl, "smug")
                $ Say_Line(girl, _("Obviously. I don't half-ass anything."))
                "She cracks a small smile despite the tough front."
            elif girl.has_trait("exhibitionist"):
                $ set_scene_expression(girl, "sexy")
                $ Say_Line(girl, _("I know, right? You should see me from behind."))
                "She winks and goes back to her set."
            elif girl.has_trait("public_shy"):
                $ set_scene_expression(girl, "shy", blush=2)
                $ Say_Line(girl, _("Shh... not so loud. People might think..."))
                "She glances around nervously."
            else:
                $ set_scene_expression(girl, "shy", blush=1)
                $ Say_Line(girl, _("Oh... thanks. I've been pushing heavier lately."))
                "She adjusts her ponytail, trying to act casual."
            $ Change_Status(girl, "Love", 5)
            $ Change_Status(girl, "Inbt", 5)

    return

# ---- EVENT 7: Exercise Help Request ----
# She asks for help with a heavy exercise. Player can reject, barely help, or help properly.
label gym_event_exercise_help(girl):
    python:
        _ex_pick = renpy.random.choice(_GYM_HELP_EXERCISES)
        _ex_name = _tl(_ex_pick[0])
        _ex_desc = _tl(_ex_pick[1])

    "[_ex_desc]"
    if girl.has_trait("gym_rat"):
        $ Say_Line(girl, _("Spot me on [_ex_name]. I'm going for a new max and I need someone who won't panic."))
    elif girl.has_trait("cute_sex"):
        $ Say_Line(girl, _("Um... c-can you spot me on [_ex_name]? I'm a little scared to go heavier alone..."))
    elif girl.has_trait("hardcore_sex"):
        $ Say_Line(girl, _("Spot me on [_ex_name]. I'm pushing a new pr and I need someone who won't be useless."))
    else:
        $ Say_Line(girl, _("Hey, can you spot me on [_ex_name]? I want to go heavier but I'm scared of failing."))

    menu:
        "I'm busy with my own sets.":
            $ Say_Player(_("Sorry, I'm in the middle of something."))
            if girl.has_trait("gym_rat"):
                $ set_scene_expression(girl, "bemused")
                $ Say_Line(girl, _("Figures. Fine, I'll just grab someone who isn't useless."))
                "She walks off and finds another spotter in seconds."
                $ Change_Status(girl, "Love", -8)
                $ Change_Status(girl, "Obed", -3)
            elif girl.has_trait("cute_sex"):
                $ set_scene_expression(girl, "sad")
                $ Say_Line(girl, _("Oh... o-okay. I'll just... go lighter then."))
                "She quietly lowers the weight, visibly deflated."
                $ Change_Status(girl, "Love", -5)
                $ Change_Status(girl, "Obed", 5)
            elif girl.has_trait("hardcore_sex"):
                $ set_scene_expression(girl, "angry")
                $ Say_Line(girl, _("Fine. I'll do it myself. Don't need you anyway."))
                "She loads even more weight on the bar out of spite."
                $ Change_Status(girl, "Love", -5)
                $ Change_Status(girl, "Obed", 5)
            else:
                $ Say_Line(girl, _("Oh... okay. I'll just go lighter then."))
                "She lowers the weight, looking disappointed."
                $ Change_Status(girl, "Love", -5)
                $ Change_Status(girl, "Obed", 5)

        "Sure. {i}(Stand there and watch her struggle){/i}":
            $ Say_Player(_("Yeah, I got you. Go for it."))
            "She starts the lift. It's clearly too heavy, and she struggles from the first rep."
            "You stand there with your arms crossed, watching."
            if girl.has_trait("gym_rat"):
                "She grits her teeth and grinds through it by pure determination."
                "She racks the weight and stands up, glaring at you."
                $ set_scene_expression(girl, "angry")
                $ Say_Line(girl, _("You just stood there. A spotter who doesn't spot is worse than no spotter."))
                $ Say_Line(girl, _("Don't waste my time like that again."))
                $ Change_Status(girl, "Love", -5)
                $ Change_Status(girl, "Obed", 10)
            elif girl.has_trait("cute_sex"):
                $ Say_Line(girl, _("P-please...! H-help me...! I can't...!"))
                "You wait a few more seconds before stepping in. She sets the weight down, trembling."
                $ set_scene_expression(girl, "sad")
                $ Say_Line(girl, _("I-I thought you were going to help... that was really scary..."))
                "Her eyes are glassy. She wipes her face with her sleeve."
                $ Change_Status(girl, "Love", -8)
                $ Change_Status(girl, "Obed", 15)
            elif girl.has_trait("hardcore_sex"):
                $ Say_Line(girl, _("COME ON...! Hnng...!"))
                "She grinds through the rep by sheer willpower, face twisted with effort."
                "She racks the weight and turns to you, breathing hard."
                $ set_scene_expression(girl, "angry")
                $ Say_Line(girl, _("You son of a bitch... but I did it. No thanks to you."))
                "She's furious. But there's a spark of pride in her eyes."
                $ Change_Status(girl, "Love", -3)
                $ Change_Status(girl, "Obed", 15)
            else:
                $ Say_Line(girl, _("H-help...! It's too heavy...!"))
                "You let her fight it for a few more seconds before finally stepping in."
                "She racks the weight, arms shaking, and stares at you."
                $ set_scene_expression(girl, "angry")
                $ Say_Line(girl, _("You were supposed to HELP me! I almost got hurt!"))
                "She's pissed... but she pushed through something she thought she couldn't."
                $ Change_Status(girl, "Love", -5)
                $ Change_Status(girl, "Obed", 15)

        "Of course. Let me spot you properly.":
            $ Say_Player(_("I got you. Take your time."))
            "You position yourself correctly and guide her through the set."
            "She pushes through three solid reps with your support."
            if girl.has_trait("gym_rat"):
                $ set_scene_expression(girl, "happy")
                $ Say_Line(girl, _("New PR! That's what I'm talking about!"))
                "She's breathing hard but grinning."
                $ Say_Line(girl, _("Good spot. You actually know how to support without stealing the rep."))
                $ Change_Status(girl, "Love", 10)
                $ Change_Status(girl, "Obed", 5)
            elif girl.has_trait("cute_sex"):
                $ set_scene_expression(girl, "happy")
                $ Say_Line(girl, _("I-I did it...! I actually did it! Thank you so much!"))
                "She looks like she might hug you, but catches herself at the last second."
                $ Say_Line(girl, _("S-sorry... I'm just really happy right now."))
                $ Change_Status(girl, "Love", 10)
            elif girl.has_trait("hardcore_sex"):
                $ set_scene_expression(girl, "happy")
                $ Say_Line(girl, _("New PR! Hell yeah!"))
                "She bumps your fist without asking."
                $ Say_Line(girl, _("Solid spot. You actually know what you're doing."))
                $ Change_Status(girl, "Love", 8)
                $ Change_Status(girl, "Obed", 3)
            else:
                $ set_scene_expression(girl, "happy")
                $ Say_Line(girl, _("Yes! That was a new record for me!"))
                $ Say_Line(girl, _("Thanks for spotting me. I couldn't have done that alone."))
                $ Change_Status(girl, "Love", 8)

    return

# ---- EVENT 8: Squat From Behind ----
# Player sees her squatting from behind. Can sneak a photo, ignore, or compliment.
# There's a mirror in front of her — she can see everything.
label gym_event_squat_behind(girl):
    "She's at the squat rack with her back to you, doing slow, controlled reps."
    "The view from behind is... hard to ignore. There's a large mirror right in front of her."

    if girl.has_trait("gym_rat"):
        "She catches your eye in the mirror without breaking her form."
        $ Say_Line(girl, _("You're staring. Either say something useful or stop wasting my time."))

        menu:
            "Your glute activation is insane.":
                $ Say_Player(_("Seriously, your glute activation is textbook perfect. What's your programming?"))
                $ set_scene_expression(girl, "happy")
                $ Say_Line(girl, _("Finally, someone who speaks gym. Bulgarian split squats twice a week, hip thrusts three times."))
                $ Say_Line(girl, _("Most guys just stare. At least you know what you're looking at."))
                $ Change_Status(girl, "Love", 8)
                $ Change_Status(girl, "Obed", 5)

            "Just admiring the view.":
                $ Say_Player(_("Can't help it. The view is... motivating."))
                python:
                    _energy = Player.energy_max
                if _energy >= 4:
                    $ set_scene_expression(girl, "smug")
                    $ Say_Line(girl, _("At least you've got the body to back up that attitude."))
                    $ Change_Status(girl, "Love", 3)
                    $ Change_Status(girl, "Inbt", 5)
                else:
                    $ set_scene_expression(girl, "angry")
                    $ Say_Line(girl, _("Motivating? Go be motivated on a treadmill. You need it more than I do."))
                    $ Change_Status(girl, "Love", -5)
                    $ Change_Status(girl, "Inbt", 3)

            "Ignore and get back to training":
                "You nod and get back to your own workout."
                "She watches you in the mirror for a moment before continuing her set."

        return

    menu:
        "Ignore and move on":
            "You look away and get back to your workout."

        "Sneak a photo with your phone":
            "You pull out your phone and discreetly angle it toward her."
            "You tap the screen... and at that exact moment, her eyes meet yours in the mirror."
            $ set_scene_expression(girl, "surprised")

            if girl.has_trait("camera_lover"):
                $ set_scene_expression(girl, "sexy")
                $ Say_Line(girl, _("...Did you at least get my good side?"))
                "She poses slightly, adjusting her stance."
                $ Say_Line(girl, _("Next time, just ask. I'll give you a better angle."))
                $ Change_Status(girl, "Obed", 5)
                $ Change_Status(girl, "Inbt", 5)
                $ Change_Status(girl, "Love", 3)
            elif girl.has_trait("camera_hater"):
                $ set_scene_expression(girl, "angry")
                $ Say_Line(girl, _("DELETE THAT! I HATE being photographed! Are you insane?!"))
                "She storms over and reaches for your phone."
                $ Say_Line(girl, _("Give me that! I want to see you delete it RIGHT NOW!"))
                "You pretend to delete it. She watches, shaking with anger."
                $ Change_Status(girl, "Obed", 5)
                $ Change_Status(girl, "Inbt", 15)
                $ Change_Status(girl, "Love", -10)
            elif girl.has_trait("exhibitionist"):
                $ set_scene_expression(girl, "shy", blush=1)
                $ Say_Line(girl, _("...I saw that. You're lucky I don't mind."))
                "She turns back to the mirror with a faint smirk."
                $ Say_Line(girl, _("Hope the lighting was good at least."))
                $ Change_Status(girl, "Obed", 5)
                $ Change_Status(girl, "Inbt", 8)
                $ Change_Status(girl, "Love", 3)
            elif girl.has_trait("public_shy"):
                $ set_scene_expression(girl, "scared")
                $ Say_Line(girl, _("Oh my god... did anyone else see you do that?! Delete it! Please!"))
                "She looks around frantically, terrified someone noticed."
                $ Say_Line(girl, _("What if someone sees that photo?! What if it gets out?!"))
                $ Change_Status(girl, "Obed", 8)
                $ Change_Status(girl, "Inbt", 12)
            elif girl.has_trait("cute_sex"):
                $ set_scene_expression(girl, "worried")
                $ Say_Line(girl, _("...Did you just take a photo of me?"))
                $ Say_Line(girl, _("P-please delete that... that's really creepy..."))
                "She hugs herself, looking small."
                $ Change_Status(girl, "Obed", 10)
                $ Change_Status(girl, "Inbt", 10)
            elif girl.has_trait("hardcore_sex"):
                $ set_scene_expression(girl, "angry")
                $ Say_Line(girl, _("...Did you just take a photo of my ass?"))
                $ Say_Player(_("Maybe."))
                $ Say_Line(girl, _("You've got five seconds to delete that before I make you eat your phone."))
                "You pocket it. She cracks her knuckles but doesn't follow through."
                $ Change_Status(girl, "Obed", 8)
                $ Change_Status(girl, "Inbt", 10)
            else:
                $ Say_Line(girl, _("...Did you just take a photo of me?"))
                python:
                    _inbt = getattr(girl, "Inbt", 0)
                if _inbt >= 400:
                    $ set_scene_expression(girl, "worried")
                    $ Say_Line(girl, _("I... can you delete that? Please?"))
                    "She looks away, too intimidated to press the issue."
                    $ Say_Player(_("Relax. Just checking my messages."))
                    "She doesn't believe you. But she doesn't push it."
                else:
                    $ set_scene_expression(girl, "angry")
                    $ Say_Line(girl, _("Delete that. Right now."))
                    $ Say_Player(_("Relax, it was nothing."))
                    $ Say_Line(girl, _("It wasn't nothing. I saw you."))
                    "You pocket your phone. She glares, but eventually goes back to her set."
                $ Change_Status(girl, "Obed", 8)
                $ Change_Status(girl, "Inbt", 10)

        "Wow... looking good.":
            "You catch her eye in the mirror."
            $ Say_Player(_("Wow. Looking good back there."))

            if girl.has_trait("cute_sex"):
                $ set_scene_expression(girl, "shy", blush=2)
                $ Say_Line(girl, _("D-don't say that while I'm mid-rep...! I almost dropped the bar!"))
                "She finishes her set, face burning red."
                $ Say_Line(girl, _("...You really think so though?"))
                $ Change_Status(girl, "Love", 5)
                $ Change_Status(girl, "Inbt", 8)
            elif girl.has_trait("hardcore_sex"):
                $ set_scene_expression(girl, "smug")
                $ Say_Line(girl, _("Damn right I do. These glutes don't build themselves."))
                "She racks the bar and flexes."
                $ Say_Line(girl, _("Enjoy the view while you can."))
                $ Change_Status(girl, "Love", 5)
                $ Change_Status(girl, "Inbt", 5)
            elif girl.has_trait("exhibitionist"):
                $ set_scene_expression(girl, "sexy")
                $ Say_Line(girl, _("Oh, you noticed? I wore these leggings on purpose."))
                "She does one more slow rep, making sure you're watching."
                $ Change_Status(girl, "Love", 5)
                $ Change_Status(girl, "Inbt", 10)
                $ Change_Status(girl, "Lust", 3)
            elif girl.has_trait("public_shy"):
                $ set_scene_expression(girl, "shy", blush=2)
                $ Say_Line(girl, _("Shh...! Someone might hear you...!"))
                "She racks the bar and moves closer, whispering."
                $ Say_Line(girl, _("...Thanks. But please, not so loud next time."))
                $ Change_Status(girl, "Love", 3)
                $ Change_Status(girl, "Inbt", 5)
            else:
                python:
                    _love = getattr(girl, "Love", 0)
                if _love >= 400:
                    $ set_scene_expression(girl, "shy", blush=1)
                    $ Say_Line(girl, _("Shut up... you're making me lose focus."))
                    "She racks the bar and stretches, hiding a smile."
                    $ Say_Line(girl, _("...But thanks. I've been working hard on my glutes."))
                    $ Change_Status(girl, "Love", 5)
                    $ Change_Status(girl, "Inbt", 8)
                else:
                    $ set_scene_expression(girl, "angry")
                    $ Say_Line(girl, _("Eyes up here, creep."))
                    "She finishes her set and moves to a different station."
                    $ Change_Status(girl, "Love", -3)
                    $ Change_Status(girl, "Inbt", 5)

    return
