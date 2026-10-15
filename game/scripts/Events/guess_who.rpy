# ============================================================
# GUESS WHO EVENT
# Fires when player arrives at campus alone and any girl
# has Love >= 300. Someone covers the player's eyes.
# ============================================================

init python:

    def _guess_who_pick_person():
        """Pick who covers the player's eyes.
        Weighted by Love -- higher Love = higher chance.
        Santa is always in the pool with a small fixed weight."""
        candidates = []
        for g in girls_on_campus():   # she cannot cover his eyes from her parents' place (or from off campus)
            _love = getattr(g, "Love", 0)
            if _love >= 300 and not g.has_temp_status("angry") and not g.has_temp_status("sad"):
                candidates.append((g, _love))

        if not candidates:
            return None, None

        # Build weighted list: (identifier, weight, is_santa)
        pool = []
        for g, w in candidates:
            pool.append((g, w, False))
        pool.append((None, 80, True))  # Santa with fixed weight

        _total = sum(w for _itm, w, _fl in pool)
        _roll = renpy.random.random() * _total
        _acc = 0
        for item, w, is_santa in pool:
            _acc += w
            if _roll <= _acc:
                return item, is_santa
        return pool[0][0], pool[0][2]

# ============================================================
# CHECK (called from Campus_Entry)
# ============================================================
label guess_who_check:

    # Only fire if player is alone (no party)
    if len(Party) > 0:
        return

    # Must be daytime (not night)
    if TimeIndex == NIGHT_INDEX:
        return

    # Cooldown: once per week
    python:
        _gw_last_day = getattr(store, "_guess_who_last_day", -99)
        _gw_days_since = Day - _gw_last_day
    if _gw_days_since < 7:
        return

    # Need at least one girl with Love >= 300
    python:
        _gw_any_eligible = any(getattr(g, "Love", 0) >= 300 for g in girls_on_campus())

    if not _gw_any_eligible:
        return

    # 5% chance per arrival
    if renpy.random.random() > 0.05:
        return

    # --- Event fires ---
    $ store._guess_who_last_day = Day

    python:
        _gw_person, _gw_is_santa = _guess_who_pick_person()

    if _gw_person is None and not _gw_is_santa:
        return

    call guess_who_event(_gw_person, _gw_is_santa) from _call_guess_who_event
    return

# ============================================================
# MAIN EVENT
# ============================================================
label guess_who_event(person, is_santa):

    scene black with dissolve

    "You're walking through campus when suddenly everything goes dark."
    "Someone's hands cover your eyes from behind."

    python:
        if is_santa:
            _gw_voice_hints = [
                _("Ho ho ho... guess who?"),

                _("Merry Christmas, young man... guess who this is?"),

                _("Have you been naughty or nice? Guess who!"),

            ]
        else:
            _gw_voice_hints = [
                _("Guess who~"),

                _("No peeking! Guess who it is..."),

                _("Don't turn around... guess who?"),

                _("Cover your eyes... well, I'm already doing that. Guess!"),

                _("You'll never guess who this is..."),

            ]

    $ _gw_hint = _tl(renpy.random.choice(_gw_voice_hints))

    "A voice whispers behind you..."

    if is_santa:
        "\"[_gw_hint]\""
    else:
        # Use the real person to say it with colored name hidden
        # (she whispers, so we just show the line without name)
        "\"[_gw_hint]\""

    "The hands feel warm and soft against your face. Who could it be?"

    # Build menu and show via renpy.display_menu
    python:
        _gw_items = []
        for _g in ALL_GIRLS:
            _gw_items.append((_g.Name, _g))
        _gw_items.append((_("Santa Claus"), "santa"))
        renpy.random.shuffle(_gw_items)

        _gw_result = renpy.display_menu(_gw_items)

    # Determine if correct
    python:
        if is_santa:
            _gw_correct = (_gw_result == "santa")
        else:
            _gw_correct = (_gw_result == person)

        _gw_picked_is_santa = (_gw_result == "santa")
        _gw_picked_girl = _gw_result if _gw_result != "santa" else None

    # Reveal: show campus + person standing
    "The hands pull away and you turn around."

    if _gw_correct:
        # ── CORRECT GUESS ──
        if is_santa:
            $ renpy.scene()
            $ renpy.show(get_bg_for_location("campus"))
            with dissolve
            "A man in a full Santa outfit, complete with a fake beard and a red hat."
            "\"Ho ho ho! You got me! Merry Christmas!\""
            "He pats you on the shoulder and walks away humming a carol."
            "...It's not even December."

            python:
                for _g in ALL_GIRLS:
                    if getattr(_g, "Love", 0) >= 300:
                        Change_Status(_g, "Inbt", 10)

        else:
            $ unlock_achievement("not_santa_claus")
            $ renpy.scene()
            $ renpy.show(get_bg_for_location("campus"))
            $ set_girl_sprite(person.gid, pose="standing", at_list=[slot_center])
            $ set_scene_expression(person, "smile")
            with dissolve

            python:
                _gw_correct_lines = [
                    _("How did you know?! You're no fun..."),

                    _("Ugh, you guessed it! Am I that obvious?"),

                    _("You recognized me? That's... actually kind of sweet."),

                    _("Damn, I thought I had you! How did you figure it out?"),

                    _("You got it right... do you think about me that much?"),

                ]
            $ Say_Line(person, _tl(renpy.random.choice(_gw_correct_lines)))
            "She smiles at you, pleased that you recognized her."
            $ Change_Status(person, "Love", renpy.random.randint(16, 30))

    else:
        # ── WRONG GUESS ──
        if is_santa:
            $ renpy.scene()
            $ renpy.show(get_bg_for_location("campus"))
            with dissolve
            "A man in a full Santa outfit stares at you, looking offended."
            "\"I'm SANTA CLAUS! How do you not recognize these hands?!\""
            "He storms off, muttering about ungrateful youth."

            python:
                for _g in ALL_GIRLS:
                    if getattr(_g, "Love", 0) >= 300:
                        Change_Status(_g, "Inbt", 6)

        else:
            # Real person was a girl but player guessed wrong
            $ renpy.scene()
            $ renpy.show(get_bg_for_location("campus"))
            $ set_girl_sprite(person.gid, pose="standing", at_list=[slot_center])
            $ set_scene_expression(person, "sad")
            with dissolve

            python:
                _gw_name = person.Name
                _gw_wrong_lines = [
                    _("Seriously? You thought I was someone else?"),

                    _("Wow... you really don't recognize my hands? That hurts."),

                    _tl(_("Wrong! It's me, {0}. Are you even paying attention to me?")).format(_gw_name),
                    _("You couldn't even tell it was me... do I mean that little to you?"),

                    _tl(_("It's {0}! Not... whoever you just said. Unbelievable.")).format(_gw_name),
                ]
            $ Say_Line(person, _tl(renpy.random.choice(_gw_wrong_lines)))
            "She looks disappointed."
            $ Change_Status(person, "Love", -renpy.random.randint(10, 20))
            $ Change_Status(person, "Obed", renpy.random.randint(6, 16))

            # If player guessed another real girl, she comments
            if _gw_picked_girl is not None and _gw_picked_girl != person:
                $ set_scene_expression(person, "angry")
                python:
                    _gw_wrong_name = _gw_picked_girl.Name
                    _gw_jealous = [
                        _tl(_("Wait... you thought {0}'s hands felt like mine? Interesting...")).format(_gw_wrong_name),
                        _tl(_("You were thinking about {0}? While MY hands were on you?")).format(_gw_wrong_name),
                        _tl(_("{0}? Really? Do I look like {0} to you?!")).format(_gw_wrong_name),
                    ]
                $ Say_Line(person, _tl(renpy.random.choice(_gw_jealous)))

    return

# ============================================================
# DEBUG — call from console: call debug_guess_who
# Skips all checks, forces the event immediately.
# ============================================================
label debug_guess_who:

    python:
        _gw_person, _gw_is_santa = _guess_who_pick_person()
        # If no eligible girl, force first girl + not santa
        if _gw_person is None and not _gw_is_santa:
            _gw_person = ALL_GIRLS[0]
            _gw_is_santa = False

    call guess_who_event(_gw_person, _gw_is_santa) from _call_guess_who_debug
    return
