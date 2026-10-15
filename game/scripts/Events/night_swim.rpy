# ============================================================
# NIGHT SWIM EVENT
# Low-probability event: player goes to pool at night,
# finds a girl skinny dipping alone.
# ============================================================

default _night_swim_fired_today = False

# Girl positioned right and lower, simulates being in the pool
transform slot_pool_night:
    xalign 0.9
    yalign 2.3

init python:

    def _night_swim_pick_girl():
        """
        Pick a girl eligible for the night swim event.
        Requirements:
          - Inbt >= 300 (bold enough to swim nude alone)
          - Not angry at player
          - Not currently in the player's Party
        Returns a girl object or None.
        """
        candidates = []
        for g in girls_on_campus():   # this picker never reads girl.loc: an away / off-campus girl was a candidate
            if g in store.Party:
                continue
            if hasattr(g, "has_temp_status") and g.has_temp_status("angry"):
                continue
            inbt = getattr(g, "Inbt", 0)
            _threshold = 50 if g.has_trait("exhibitionist") else 150
            if inbt < _threshold:
                continue
            candidates.append(g)

        if not candidates:
            return None
        return renpy.random.choice(candidates)

    # ---------- Dialogue pools ----------

    _NIGHT_SWIM_STARTLE = [
        _("W-what?! Who is there?!"),
        _("Oh my god! You scared me!"),
        _("Ah! How long have you been standing there?!"),
        _("Hey! Do not sneak up on someone like that!"),
    ]

    _NIGHT_SWIM_PLAYER_EXPLAIN = [
        _("I could not sleep. It was too hot, so I came out for some air. Then I heard splashing."),
        _("The heat was killing me. I came to cool off and heard someone in the water."),
        _("I was just taking a walk. The heat is unbearable tonight. Then I noticed someone swimming."),
    ]

    _NIGHT_SWIM_GIRL_EXPLAIN = [
        _("Same here... it is so hot tonight. I figured nobody would be around, so I went for a swim. Without... you know."),
        _("The heat was driving me crazy too. I thought I had the pool to myself, so I decided to swim... naturally."),
        _("I could not take the heat anymore. It is the middle of the night, so I thought... why bother with a swimsuit?"),
    ]

    # --- Girl reactions to being caught nude (before decision) ---

    _NIGHT_SWIM_EMBARRASSED = [
        _("This is so embarrassing... please do not stare."),
        _("I cannot believe you caught me like this..."),
        _("Of all the people to walk in on me... it had to be you."),
    ]

    _NIGHT_SWIM_CHILL = [
        _("Well, you have already seen me. No point hiding now."),
        _("I guess the secret is out. I am a midnight swimmer."),
        _("Not exactly how I planned my evening, but here we are."),
    ]

    # --- Ask player to leave ---

    _NIGHT_SWIM_ASK_LEAVE = [
        _("Could you... turn around? I need to get out and put something on."),
        _("Do you mind looking away? I want to get dressed."),
        _("Just... give me a minute to get out of here, okay? No peeking."),
        _("Close your eyes. I am getting out."),
    ]

    _NIGHT_SWIM_PLAYER_LEAVES = [
        _("You turn around and wait while she climbs out and wraps herself in a towel."),
        _("You look away as you hear the water shift and the sound of fabric rustling."),
        _("You give her space. After a moment, she taps your shoulder. She is dressed in a towel."),
    ]

    _NIGHT_SWIM_AFTER_DRESS = [
        _("Thanks for not being weird about it."),
        _("You are surprisingly decent, you know that?"),
        _("I appreciate you not making this awkward. Well... more awkward."),
        _("Okay. Crisis averted. We never speak of this again."),
    ]

    # --- Invite player to join ---

    _NIGHT_SWIM_INVITE_SHY = [
        _("I... you know what, the water is really nice. Do you want to join me?"),
        _("Since you are already here... do you want to get in? It is actually really refreshing."),
        _("Well, you have already seen everything. You might as well come in."),
    ]

    _NIGHT_SWIM_INVITE_BOLD = [
        _("The water feels amazing. Why don't you get in? Unless you are scared."),
        _("Are you just going to stand there, or are you going to join me? Clothes off."),
        _("Come on, get in. The night is too hot and the pool is too nice to waste. Leave the shorts on the chair."),
        _("You look like you need to cool off too. Get in here. No swimsuit required."),
    ]

    _NIGHT_SWIM_INVITE_EXHIB = [
        _("Mmm, I was hoping someone would show up. Get in here, the water is perfect."),
        _("I left the lights off for a reason, you know. Come join me... all of you."),
        _("Looks like my little midnight adventure just got more interesting. Strip down and get in."),
    ]

    # --- Player accepts / joins ---

    _NIGHT_SWIM_PLAYER_JOINS = [
        _("You undress and slip into the pool. The cool water is a relief from the heat."),
        _("You set your clothes aside and step into the water. She watches you with a soft smile."),
        _("The water wraps around you as you lower yourself in. Much better than tossing in bed."),
    ]

    _NIGHT_SWIM_TOGETHER_SWEET = [
        _("This is nice, right? Just the two of us, the water, the stars..."),
        _("I have to admit, this is way better with company."),
        _("You know, I was a little bored swimming alone. This is much better."),
        _("The moonlight on the water is beautiful. I am glad you showed up."),
    ]

    _NIGHT_SWIM_TOGETHER_FLIRTY = [
        _("You know, it is hard to keep my distance when you are right there... like that."),
        _("The water is not the only thing making me feel warm right now."),
        _("Eyes up here. ...Or not. I do not really mind."),
        _("I can feel you looking at me. And honestly? I kind of like it."),
    ]

    # --- Player declines the invite ---

    _NIGHT_SWIM_PLAYER_DECLINES = [
        _("I will let you enjoy your swim. I should head back before someone notices."),
        _("Tempting, but I think I will just enjoy the view from here. Good night."),
        _("I better not. But your secret is safe with me."),
    ]

    _NIGHT_SWIM_GIRL_DECLINE_REACT = [
        _("Suit yourself. Your loss."),
        _("Smart. Or boring. I have not decided which."),
        _("Fair enough. But the offer had an expiration date, just so you know."),
    ]

    # --- Escalation lines (before sex menu) ---

    _NIGHT_SWIM_ESCALATE_CLOSE = [
        _("She drifts closer, the water lapping gently between you. The heat is not just from the weather anymore."),
        _("Your bodies drift together in the warm night air. The water between you feels charged."),
        _("Under the surface, her hand finds yours. Neither of you pulls away."),
    ]

    _NIGHT_SWIM_ESCALATE_GIRL_BOLD = [
        _("You know... since we are already here, already like this... maybe we do not have to stop at just swimming."),
        _("I did not plan for company tonight. But now that you are here... I do not want to just swim."),
        _("The heat is not going away. And I do not think it is just the weather."),
    ]

    _NIGHT_SWIM_ESCALATE_GIRL_SHY = [
        _("I... my heart is beating so fast right now. Is it the cold water or... you?"),
        _("We probably should not be doing this... but I do not want to stop."),
        _("This feels like a dream. The kind I would never tell anyone about."),
    ]

    # --- Trait-specific invite flavor (before the invite choice) ---

    _NIGHT_SWIM_TRAIT_LINES = {
        "exhibitionist": _("She does not even try to cover herself. If anything, she shifts to give you a better view."),
        "public_shy": _("She immediately ducks lower into the water, cheeks burning red even in the moonlight."),
        "cute_sex": _("She squeaks and sinks up to her chin, eyes wide. Her blush is visible even in the dark."),
        "hardcore_sex": _("She crosses her arms on the pool edge, making no effort to hide. She looks more annoyed than embarrassed."),
    }

# ============================================================
# DEBUG: force night swim with first available girl
# ============================================================
label debug_night_swim:
    python:
        _dbg_girl = ALL_GIRLS[0] if ALL_GIRLS else None
    if _dbg_girl is None:
        "No girls available."
        return
    call night_swim_event(_dbg_girl) from _call_night_swim_event_debug
    return

# ============================================================
# NIGHT SWIM CHECK - called from Pool_Entry
# ============================================================
label night_swim_check:

    if TimeIndex != NIGHT_INDEX:
        return

    if _night_swim_fired_today:
        return

    python:
        _ns_girl = _night_swim_pick_girl()

    if _ns_girl is None:
        return

    # Probability: 25% first time ever, 10% after, 1% if same girl again
    python:
        _ns_total = sum(1 for g in ALL_GIRLS for _ in range(g.GetActionCount("night_swim_caught")))
        _ns_girl_count = _ns_girl.GetActionCount("night_swim_caught")

        if _ns_total == 0:
            _ns_chance = 0.25
        elif _ns_girl_count > 0:
            _ns_chance = 0.01
        else:
            _ns_chance = 0.10

    if renpy.random.random() > _ns_chance:
        return

    # --- Event fires ---
    $ _night_swim_fired_today = True

    call night_swim_event(_ns_girl) from _call_night_swim_event
    return

# ============================================================
# MAIN EVENT
# ============================================================
label night_swim_event(girl):

    $ store._in_event = True
    $ store._in_sandbox = False
    $ debug_log("[STATE] _in_event = True, _in_sandbox = False (night_swim_event)")

    $ CurrentLocation = "pool"
    call Set_Scene(entry=True, show_chars=False, quiet=True) from _call_Set_Scene_night_swim

    # Narration: player arrives at the pool

    python:
        _hear_water = renpy.random.choice([
            _("As you approach the pool, you hear the faint sound of water splashing. Someone is here."),
            _("You step outside and hear some splashing from the pool. At this hour?"),
            _("The pool comes into view, and you notice ripples in the water. You are not alone."),
        ])
    $ Narration(_hear_water)

    $ Narration(_("You move closer and realize someone is swimming in the dark. No lights, no swimsuit."))

    # Save outfit before stripping, show girl nude
    $ girl.SaveOutfit()
    python:
        girl.Outfit_Change(over="none", mid="none", chest="none", legs="none", panties="none", shoes="none")

    # Show girl at pool-right position (lower + right, keeps balloon to the left)
    $ girl.SpriteLoc = StageRight
    $ set_girl_sprite(girl.gid, pose="standing", at_list=[slot_pool_night])

    # Girl notices player
    python:
        _startle = _tl(renpy.random.choice(_NIGHT_SWIM_STARTLE))
    $ set_scene_expression(girl, "surprised")
    $ Say_Line(girl, _startle)

    # Player explains
    python:
        _explain = _tl(renpy.random.choice(_NIGHT_SWIM_PLAYER_EXPLAIN))
    $ Say_Player(_explain)

    # Girl explains
    $ set_scene_expression(girl, "bemused")
    python:
        _girl_explain = _tl(renpy.random.choice(_NIGHT_SWIM_GIRL_EXPLAIN))
    $ Say_Line(girl, _girl_explain)

    # Trait-specific flavor
    python:
        _trait_line = None
        # only the exhibitionist narration is a deed (she shifts to give him a better view);
        # ducking, blushing or looking annoyed is tone, not taste
        _trait_discover_map = {
            "exhibitionist": "discovered_trait_exhibitionist",
        }
        for _ns_trait in ["exhibitionist", "public_shy", "cute_sex", "hardcore_sex"]:
            if girl.has_trait(_ns_trait):
                _trait_line = _NIGHT_SWIM_TRAIT_LINES[_ns_trait]
                _ns_disc = _trait_discover_map.get(_ns_trait)
                if _ns_disc and hasattr(girl, "discover"):
                    girl.discover(_ns_disc)
                break
    if _trait_line is not None:
        $ Narration(_trait_line)

    # Embarrassment or chill based on Inbt
    python:
        _inbt = getattr(girl, "Inbt", 0)
        _love = getattr(girl, "Love", 0)

    if _inbt >= 600 or girl.has_trait("exhibitionist"):
        python:
            _react = _tl(renpy.random.choice(_NIGHT_SWIM_CHILL))
        $ set_scene_expression(girl, "smile")
        $ Say_Line(girl, _react)
    else:
        python:
            _react = _tl(renpy.random.choice(_NIGHT_SWIM_EMBARRASSED))
        $ set_scene_expression(girl, "embarrassed")
        $ Say_Line(girl, _react)

    # Seeing her nude is intimate regardless of outcome
    $ Change_Status(girl, "Inbt", 5)
    $ Change_Status(girl, "Lust", 3)
    $ girl.RegisterAction("player_saw_boobs")
    $ girl.RegisterAction("player_saw_pussy")

    # Register the action
    $ girl.RegisterAction("night_swim_caught")
    $ unlock_achievement("moonlight_nude")

    # --- Decision: invite or ask to leave ---
    # Invite threshold: Love >= 400 AND Inbt >= 450, OR exhibitionist trait
    python:
        _can_invite = False
        if girl.has_trait("exhibitionist"):
            _can_invite = True
        elif _love >= 400 and _inbt >= 450:
            _can_invite = True

    if _can_invite:
        # Girl invites the player
        python:
            if girl.has_trait("exhibitionist"):
                _invite = _tl(renpy.random.choice(_NIGHT_SWIM_INVITE_EXHIB))
            elif _inbt >= 600:
                _invite = _tl(renpy.random.choice(_NIGHT_SWIM_INVITE_BOLD))
            else:
                _invite = _tl(renpy.random.choice(_NIGHT_SWIM_INVITE_SHY))

        $ set_scene_expression(girl, "sexy")
        $ Say_Line(girl, _invite)

        $ Change_Status(girl, "Inbt", 5)
        $ Change_Status(girl, "Lust", 3)

        menu:
            "Join her in the pool.":
                $ Say_Player(_("Give me a second."))
                python:
                    _join = _tl(renpy.random.choice(_NIGHT_SWIM_PLAYER_JOINS))
                $ Narration(_join)

                $ Change_Status(girl, "Love", 5)
                $ Change_Status(girl, "Inbt", 5)
                $ Change_Status(girl, "Lust", 5)

                # Swimming together moment
                if _inbt >= 550 or girl.has_trait("exhibitionist"):
                    $ set_scene_expression(girl, "sexy")
                    python:
                        _together = _tl(renpy.random.choice(_NIGHT_SWIM_TOGETHER_FLIRTY))
                    $ Say_Line(girl, _together)
                else:
                    $ set_scene_expression(girl, "smile")
                    python:
                        _together = _tl(renpy.random.choice(_NIGHT_SWIM_TOGETHER_SWEET))
                    $ Say_Line(girl, _together)

                # --- Escalation check ---
                # If high enough stats, can escalate to sex menu
                python:
                    _can_escalate = False
                    if _inbt >= 550 and _love >= 500:
                        _can_escalate = True
                    if girl.has_trait("exhibitionist") and _inbt >= 400:
                        _can_escalate = True
                    if getattr(girl, "Lust", 0) >= 60:
                        _can_escalate = True

                if _can_escalate:
                    python:
                        _close = _tl(renpy.random.choice(_NIGHT_SWIM_ESCALATE_CLOSE))
                    $ Narration(_close)

                    if _inbt >= 600 or girl.has_trait("exhibitionist") or girl.has_trait("hardcore_sex"):
                        python:
                            _esc_line = _tl(renpy.random.choice(_NIGHT_SWIM_ESCALATE_GIRL_BOLD))
                        $ set_scene_expression(girl, "sexy")
                    else:
                        python:
                            _esc_line = _tl(renpy.random.choice(_NIGHT_SWIM_ESCALATE_GIRL_SHY))
                        $ set_scene_expression(girl, "shy")
                    $ Say_Line(girl, _esc_line)

                    $ Change_Status(girl, "Lust", 8)
                    $ Change_Status(girl, "Inbt", 5)

                    menu:
                        "Pull her closer.":
                            $ Say_Player(_("Come here..."))
                            $ Narration(_("She does not resist. Under the water, the distance between you vanishes."))
                            $ Change_Status(girl, "Love", 5)
                            $ Change_Status(girl, "Lust", 10)
                            $ Change_Status(girl, "Inbt", 5)
                            call sex_menu(girl, "pool", NIGHT_INDEX) from _call_sex_menu_night_swim

                        "Just enjoy the moment.":
                            python:
                                _enjoy = renpy.random.choice([
                                    _("You float side by side, watching the stars. Some moments do not need anything more."),
                                    _("You stay close, enjoying the silence and the cool water. Not everything has to escalate."),
                                    _("The two of you drift together quietly. The night feels endless in the best way."),
                                ])
                            $ Narration(_enjoy)
                            $ Change_Status(girl, "Love", 10)
                            $ Change_Status(girl, "Inbt", 3)

                else:
                    # Stats not high enough, just a sweet swim
                    python:
                        _nice_swim = renpy.random.choice([
                            _("You swim together for a while, enjoying the cool water and the quiet night."),
                            _("The two of you float around, talking softly. It feels natural, like this was always the plan."),
                            _("Time passes quickly. The heat fades, replaced by the calm of the pool and good company."),
                        ])
                    $ Narration(_nice_swim)
                    $ Change_Status(girl, "Love", 8)
                    $ Change_Status(girl, "Inbt", 3)

                # Wrap up
                python:
                    _wrapup = renpy.random.choice([
                        _("Eventually, you both climb out and dry off. The night air feels cooler now."),
                        _("After a while, you get out of the water. She wraps herself in a towel, smiling."),
                        _("The swim ends as quietly as it started. You both get dressed under the stars."),
                    ])
                $ Narration(_wrapup)

                python:
                    _goodnight = renpy.random.choice([
                        _("Tonight was... unexpected. But I am glad it happened."),
                        _("Best midnight swim I have ever had. Do not tell anyone, though."),
                        _("Same time tomorrow? ...I am kidding. Maybe."),
                        _("If you tell anyone about this, I will deny everything."),
                    ])
                $ set_scene_expression(girl, "smile")
                $ Say_Line(girl, _goodnight)

            "Stay and watch from the edge.":
                python:
                    _watch = renpy.random.choice([
                        _("You sit at the edge of the pool, feet in the water, trying not to stare too obviously."),
                        _("You settle on the pool edge. The moonlight on the water, and on her, is hard to ignore."),
                        _("You take a seat nearby. She notices you watching but does not seem to mind."),
                    ])
                $ Narration(_watch)
                $ Change_Status(girl, "Inbt", 3)
                $ Change_Status(girl, "Lust", 3)

                python:
                    _watch_react = renpy.random.choice([
                        _("Enjoying the show from there?"),
                        _("You are staring. I can tell, even in the dark."),
                        _("If you are going to watch, at least say something nice."),
                    ])
                $ set_scene_expression(girl, "sexy")
                $ Say_Line(girl, _watch_react)

                $ Change_Status(girl, "Love", 3)
                $ Change_Status(girl, "Inbt", 3)
                $ Change_Status(girl, "Lust", 5)

                python:
                    _watch_end = renpy.random.choice([
                        _("After a while, she climbs out and wraps a towel around herself."),
                        _("Eventually she gets out of the water, casually drying off next to you."),
                        _("She finishes her swim and steps out, not in any rush to cover up."),
                    ])
                $ Narration(_watch_end)

                python:
                    _watch_bye = renpy.random.choice([
                        _("Thanks for the company. Even if you just sat there."),
                        _("Next time, get in the water. It is better than watching."),
                        _("Not bad for a surprise audience. Good night."),
                    ])
                $ set_scene_expression(girl, "smile")
                $ Say_Line(girl, _watch_bye)

            "Decline and give her privacy.":
                python:
                    _decline = _tl(renpy.random.choice(_NIGHT_SWIM_PLAYER_DECLINES))
                $ Say_Player(_decline)

                python:
                    _decline_react = _tl(renpy.random.choice(_NIGHT_SWIM_GIRL_DECLINE_REACT))
                $ set_scene_expression(girl, "normal")
                $ Say_Line(girl, _decline_react)

                $ Change_Status(girl, "Love", 5)
                $ Change_Status(girl, "Obed", 3)

    else:
        # Girl asks the player to leave so she can get dressed
        python:
            _ask_leave = _tl(renpy.random.choice(_NIGHT_SWIM_ASK_LEAVE))
        $ set_scene_expression(girl, "embarrassed")
        $ Say_Line(girl, _ask_leave)

        menu:
            "Turn around and let her get dressed.":
                $ Say_Player(_("Of course. Take your time."))
                python:
                    _leaves = _tl(renpy.random.choice(_NIGHT_SWIM_PLAYER_LEAVES))
                $ Narration(_leaves)

                python:
                    _after_dress = _tl(renpy.random.choice(_NIGHT_SWIM_AFTER_DRESS))
                $ set_scene_expression(girl, "smile")
                $ Say_Line(girl, _after_dress)

                $ Change_Status(girl, "Love", 5)
                $ Change_Status(girl, "Inbt", 2)

            "Tease her a little before turning around.":
                python:
                    _tease = renpy.random.choice([
                        _("Relax, it is nothing I have not imagined before."),
                        _("For what it is worth, you have nothing to be embarrassed about."),
                        _("I will turn around. But you should know, the view was worth the walk."),
                    ])
                $ Say_Player(_tease)

                if _inbt >= 400 or _love >= 400:
                    $ set_scene_expression(girl, "bemused")
                    python:
                        _tease_react = renpy.random.choice([
                            _("You are impossible. ...But thanks, I guess."),
                            _("Shut up and turn around already. ...But that was sweet."),
                            _("I cannot believe you just said that. ...Do not make me smile right now."),
                        ])
                    $ Say_Line(girl, _tease_react)
                    $ Change_Status(girl, "Love", 3)
                    $ Change_Status(girl, "Inbt", 4)
                    $ Change_Status(girl, "Lust", 2)
                else:
                    $ set_scene_expression(girl, "angry")
                    python:
                        _tease_react = renpy.random.choice([
                            _("That is NOT funny right now. Turn around!"),
                            _("Seriously?! Just look away!"),
                            _("You are making this so much worse. TURN. AROUND."),
                        ])
                    $ Say_Line(girl, _tease_react)
                    $ Change_Status(girl, "Love", -3)
                    $ Change_Status(girl, "Obed", 3)

                python:
                    _leaves = _tl(renpy.random.choice(_NIGHT_SWIM_PLAYER_LEAVES))
                $ Narration(_leaves)

                python:
                    _after = renpy.random.choice([
                        _("Let us just pretend this did not happen."),
                        _("Okay. I am dressed. You can look now."),
                        _("There. Crisis over. We do not speak of this."),
                    ])
                $ set_scene_expression(girl, "normal")
                $ Say_Line(girl, _after)

    # Time cost
    call Apply_Time_Cost(TIME_COSTS["night_swim"]) from _call_Apply_Time_Cost_night_swim

    # Restore outfit
    $ girl.RestoreOutfit()

    $ store._in_event = False
    $ store._in_sandbox = True
    $ debug_log("[STATE] _in_event = False, _in_sandbox = True (night_swim_event end)")

    return
