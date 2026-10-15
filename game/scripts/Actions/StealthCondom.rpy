# ============================================================
# STEALTH CONDOM REMOVAL SYSTEM
# Player removes condom when girl can't see (doggy, or RCG
# with hiding_face=True). Lust-based detection check.
# If undetected: condom silently removed, discovered later.
# If detected: falls through to existing _condom_force_remove.
# ============================================================

default _stealth_condom_removed = False

init python:

    # ── Config ──

    STEALTH_CONDOM_REACTIONS = {
        "cum_slut":     {"Love": 0,    "Obed": 10,  "Inbt": 15},
        "hate_cum":     {"Love": -60,  "Obed": 35,  "Inbt": 30},
        "hardcore_sex": {"Love": -10,  "Obed": 15,  "Inbt": 20},
        "cute_sex":     {"Love": -35,  "Obed": 25,  "Inbt": 20},
        "_default":     {"Love": -25,  "Obed": 20,  "Inbt": 20},
    }

    STEALTH_RAW_REACTIONS = {
        "cum_slut":     {"Love": 0,    "Obed": 5,   "Inbt": 5},
        "hate_cum":     {"Love": -40,  "Obed": 25,  "Inbt": 20},
        "hardcore_sex": {"Love": -5,   "Obed": 10,  "Inbt": 10},
        "cute_sex":     {"Love": -20,  "Obed": 15,  "Inbt": 15},
        "_default":     {"Love": -15,  "Obed": 15,  "Inbt": 15},
    }

    STEALTH_EXCUSE_MODS = {
        "slipped_off":     {"Love": 0.5,  "Obed": 0.5,  "Inbt": 0.5},
        "felt_too_good":   {"Love": 1.0,  "Obed": 1.5,  "Inbt": 1.5},
        "moaned_louder":   {"Love": 1.5,  "Obed": 2.0,  "Inbt": 2.0},
    }

    # ── Gate & detection ──

    def _can_stealth_remove(scene_type):
        if scene_type in ("doggy", "anal", "laying_down", "laying_anal"):
            return True
        if scene_type in ("reverse_cowgirl", "reverse_cowgirl_anal") and getattr(store, "hiding_face", False):
            return True
        return False

    def _stealth_condom_detect_chance(girl, position):
        chance = 0.70
        chance -= 0.01 * getattr(girl, "Lust", 0)
        spd = _cum_get_speed(position)
        if spd >= 3:
            chance -= 0.10
        elif spd >= 2:
            chance -= 0.05
        if girl.has_trait("hate_cum"):
            chance += 0.15
        if girl.has_trait("cum_slut"):
            chance -= 0.20
        if girl.has_trait("hardcore_sex"):
            chance -= 0.05
        if position == "reverse_cowgirl" and getattr(store, "hiding_face", False):
            chance -= 0.05
        result = max(0.05, min(0.90, chance))
        print("[STEALTH_CONDOM] detect_chance: pos=%s Lust=%d spd=%d chance=%.2f" % (position, getattr(girl, "Lust", 0), spd, result))
        return result

    # ── Dialogue pools ──

    _STEALTH_DISCOVER_LINES = {
        "cum_slut": [
            _("Wait... where's the condom? Did you take it... oh. Oh, that's sneaky. I like it."),
            _("You took the condom off? Without telling me? ...God, I should be mad but that's hot."),
        ],
        "hate_cum": [
            _("WHERE IS THE CONDOM?! Did you TAKE IT OFF?! You sick bastard!!"),
            _("The condom is GONE?! You deliberately... I can't even... YOU DID THIS ON PURPOSE!"),
        ],
        "hardcore_sex": [
            _("Wait... the condom is gone? You sneaky bastard. When did you even do that?"),
            _("Did you seriously just... take it off? Without telling me? Bold move."),
        ],
        "cute_sex": [
            _("The condom is... gone? You TOOK it off?! Without asking me?! How could you?!"),
            _("Wait... I don't feel... you REMOVED it?! I trusted you! That's so wrong!"),
        ],
        "_default": [
            _("Hold on... where's the condom?! Did you TAKE it off?! What is wrong with you?!"),
            _("The condom is gone! You deliberately took it off! How dare you?!"),
            _("Wait... you removed the condom?! When?! I didn't even notice! You sneaky..."),
        ],
    }

    _STEALTH_EXCUSE_LINES = {
        "slipped_off": {
            "cum_slut": [
                _("Slipped off? Sure it did... well, no complaints from me."),
                _("'Slipped off.' Right. Well, lucky accident then."),
            ],
            "hate_cum": [
                _("SLIPPED OFF?! Condoms don't just SLIP OFF! You're LYING!"),
                _("You expect me to believe that?! It just 'slipped off'?! You planned this!"),
            ],
            "hardcore_sex": [
                _("Slipped off? Yeah, right. But whatever, it's done now."),
                _("Sure it did. I don't buy it, but I also don't really care."),
            ],
            "cute_sex": [
                _("It slipped off? Really? I... I want to believe you but... that doesn't just happen..."),
                _("How does a condom just slip off? That's... are you being honest with me?"),
            ],
            "_default": [
                _("It 'slipped off'? Do you really expect me to believe that?!"),
                _("Condoms don't just slip off. You did this on purpose."),
            ],
        },
        "felt_too_good": {
            "cum_slut": [
                _("I mean... I can't blame you. It does feel so much better without it..."),
                _("Honestly? I would have done the same thing. It feels amazing raw."),
            ],
            "hate_cum": [
                _("So you DELIBERATELY took it off because it FELT GOOD?! You selfish monster!"),
                _("Your pleasure was worth more than my safety?! You're disgusting!"),
            ],
            "hardcore_sex": [
                _("At least you're honest about it. Can't say I hate the feeling either."),
                _("Yeah, it does feel better. But you should have asked first."),
            ],
            "cute_sex": [
                _("You took it off because it felt good? What about what I want? That's so selfish..."),
                _("So feeling good mattered more than asking me? That really, really hurts..."),
            ],
            "_default": [
                _("So you just took it off because YOU wanted to feel better?! That's so selfish!"),
                _("You removed it for your own pleasure without even asking?! Unbelievable."),
            ],
        },
        "moaned_louder": {
            "cum_slut": [
                _("I... okay, fine, it does feel better. But you still should have told me!"),
                _("Ugh, you're right... it felt amazing. But don't think that makes it okay!"),
            ],
            "hardcore_sex": [
                _("...Don't turn this around on me. But... yeah, fine. It felt good."),
                _("That's beside the point! Even if I liked it, you should have said something."),
            ],
            "cute_sex": [
                _("Don't blame ME for this! You're the one who did something without asking!"),
                _("That's so unfair! You can't use my reactions to justify what you did!"),
            ],
            "_default": [
                _("Don't turn this around on ME! You took the condom off, not me!"),
                _("That doesn't justify secretly removing it! You should have asked!"),
            ],
        },
    }

    _STEALTH_POSTCUM_CALM_LINES = {
        "cum_slut": [
            _("Mmm, that was amazing..."),
            _("God, that felt so good..."),
        ],
        "hate_cum": [
            _("Good thing we used a condom..."),
            _("Well, at least we used protection..."),
        ],
        "hardcore_sex": [
            _("Damn, that was intense..."),
            _("That was a good fuck..."),
        ],
        "cute_sex": [
            _("That was really nice..."),
            _("Mmm, that was sweet..."),
        ],
        "_default": [
            _("Well, glad we used a condom..."),
            _("At least we were safe about it..."),
        ],
    }

    _STEALTH_POSTCUM_REALIZE_LINES = {
        "cum_slut": [
            _("Wait... something feels different. Did you take the condom off? You should've told me, I would've enjoyed it even more!"),
            _("Hold on... that feels warmer than usual. You came inside without a condom? ...That's so hot. But tell me next time so I can savor it!"),
        ],
        # still discovering it (trait_is_new, read through trait_pool_key): no "warmer than usual", she has no usual yet
        "cum_slut_new": [
            _("Wait... it's so warm inside... did you take the condom off? I... I actually liked that."),
            _("Hold on... you came inside without it? That's... oh wow. I don't even know what to say."),
        ],
        "hate_cum": [
            _("WAIT. I feel something... WHERE IS THE CONDOM?! DID YOU CUM INSIDE ME?! I CAN FEEL IT!!"),
            _("Hold on... something is WRONG. No... WHERE IS THE CONDOM?! YOU CAME INSIDE WITHOUT PROTECTION?!"),
        ],
        "hardcore_sex": [
            _("Hold on. Something feels different. Did you take the condom off and cum inside? ...Damn. Bold move."),
            _("Wait... that felt different. Did you seriously sneak it off and finish inside me? You sneaky bastard."),
        ],
        "cute_sex": [
            _("Wait... I feel something... is that... did you take the condom off?! And you came inside me?! How could you?!"),
            _("Hold on... something feels wrong. WHERE IS THE CONDOM?! You came inside me without it?!"),
        ],
        "_default": [
            _("Wait... where's the condom?! Did you CUM INSIDE without it?! What the hell?!"),
            _("Hold on. Something feels off. Did you take the condom off and cum inside?! Are you serious?!"),
        ],
    }

    _STEALTH_CUM_EXPRESSIONS = {
        "cum_slut": "lewd",
        "hate_cum": "angry",
        "hardcore_sex": "pleasure",
        "cute_sex": "scared",
        "_default": "surprised",
    }

    _STEALTH_UNDETECTED_LINES = [
        _("You carefully pull the condom off. She doesn't notice a thing."),
        _("You slip the condom off while she's distracted. She has no idea."),
        _("The condom comes off smoothly. She's too caught up to notice."),
    ]

    _STEALTH_CREAM_BELIEVED_LINES = {
        "cum_slut": [
            _("Well... if it slipped off, it slipped off. At least I got to feel the real thing."),
            _("Fine, accidents happen. And honestly? I'm not even mad about the result."),
        ],
        "hardcore_sex": [
            _("Whatever. If it slipped, it slipped. Shit happens. Just be more careful."),
            _("Fine, I'll buy it. But if this 'happens' again, I'll know it's on purpose."),
        ],
        "cute_sex": [
            _("I... okay. I'll believe you. Just please, please be more careful..."),
            _("It's really scary but... I trust you. Just make sure it doesn't happen again."),
        ],
        "hate_cum": [
            _("...Fine. But if this EVER happens again, I swear..."),
            _("I'll believe you this once. But you're on thin ice."),
        ],
        "_default": [
            _("...Fine. I'll give you the benefit of the doubt. But I'm watching you."),
            _("Okay, okay. Maybe it did slip. But don't let it happen again."),
        ],
    }

    _STEALTH_CREAM_ANGRY_END_LINES = {
        "hate_cum": [
            _("You took the condom off and came inside me?! We are DONE! GET OUT!"),
            _("I can feel your cum inside me... and you did this DELIBERATELY?! I'm leaving!"),
        ],
        "cute_sex": [
            _("I trusted you... and you sneaked it off and finished inside? I can't even look at you."),
            _("How could you do this to me? I... I need to go. Don't follow me."),
        ],
        "_default": [
            _("You deliberately removed the condom and came inside. We're done here."),
            _("I can't believe you did this. On purpose. Don't talk to me."),
        ],
    }

    _STEALTH_RAW_ANGRY_END_LINES = {
        "hate_cum": [
            _("You DELIBERATELY took the condom off?! Without telling me?! GET OUT!"),
            _("You removed it on PURPOSE?! I can't trust you! We're DONE!"),
        ],
        "cute_sex": [
            _("You took it off without asking me... I can't believe you'd do that. I need to go."),
            _("You removed the condom behind my back? I trusted you... please leave."),
        ],
        "_default": [
            _("You deliberately removed the condom without my consent. We're done here."),
            _("I can't believe you took it off on purpose. Get out."),
        ],
    }

    _STEALTH_CREAM_NARR_BELIEVED = {
        "cum_slut": [
            _("She accepts it easily. If anything, she seems pleased it happened."),
            _("She doesn't seem bothered at all. The raw feeling clearly outweighs the deception."),
        ],
        "hardcore_sex": [
            _("She rolls her eyes but clearly isn't going to stop over it."),
            _("She shrugs it off. Not a big deal in her book."),
        ],
        "cute_sex": [
            _("She looks worried, but takes your word for it. You continue."),
            _("She bites her lip anxiously but nods. She believes you."),
        ],
        "hate_cum": [
            _("She's furious, but grudgingly accepts it was an accident. For now."),
            _("She glares daggers at you, but doesn't stop. You got lucky."),
        ],
        "_default": [
            _("She's clearly suspicious, but decides to let it go. You continue."),
            _("She doesn't fully buy it, but doesn't want to stop. You got away with it."),
        ],
    }

    _STEALTH_CREAM_NARR_ANGRY_CONT = {
        "cum_slut": [
            _("She shakes her head but doesn't seem truly upset. If anything, she enjoyed it."),
        ],
        "hardcore_sex": [
            _("She's pissed, but the mood hasn't died for her. You keep going."),
            _("She's angry, but clearly doesn't want to stop either."),
        ],
    }

    _STEALTH_CREAM_NARR_END_HERROOM = [
        _("She's livid. She kicks you out of her room without another word."),
        _("She points at the door, shaking with rage. You leave in silence."),
    ]

    _STEALTH_CREAM_NARR_END_ELSEWHERE = [
        _("She grabs her things and storms out, disgusted."),
        _("She gets up and leaves without looking back. You went too far."),
    ]

    _STEALTH_DETECT_NARR = [
        _("She feels something is off and reaches back..."),
        _("She suddenly pauses, sensing something different..."),
        _("Something tips her off. She reaches down to check..."),
    ]

    # ── Functions ──

    def stealth_condom_reset():
        store._stealth_condom_removed = False
        print("[STEALTH_CONDOM] state reset")

    def _girl_thinks_condom_on():
        return store.condom_active or store._stealth_condom_removed

    def condom_holds_load():
        """His load stays in the condom: one on him and not torn (a torn one lets it into her, a stealth removal left
        none on). The cum anims draw nothing dripping from her then."""
        return bool(getattr(store, "condom_active", False)) and not getattr(store, "_condom_broken", False)

    def _stealth_apply_stats(girl, excuse_key=None):
        tk = _condom_break_trait_key(girl)
        base = STEALTH_CONDOM_REACTIONS.get(tk, STEALTH_CONDOM_REACTIONS["_default"])
        excuse_mod = STEALTH_EXCUSE_MODS.get(excuse_key, {}) if excuse_key else {}
        for stat, amount in base.items():
            mult = excuse_mod.get(stat, 1.0)
            final = int(amount * mult)
            if final != 0:
                Change_Status(girl, stat, final)
        if girl.has_npc_partner():
            Change_Status(girl, "Love", -20)
        print("[STEALTH_CONDOM] stats applied: trait=%s excuse=%s bf=%s" % (tk, excuse_key, girl.has_npc_partner()))

    def _stealth_raw_apply_stats(girl, excuse_key=None):
        tk = _condom_break_trait_key(girl)
        base = STEALTH_RAW_REACTIONS.get(tk, STEALTH_RAW_REACTIONS["_default"])
        excuse_mod = STEALTH_EXCUSE_MODS.get(excuse_key, {}) if excuse_key else {}
        for stat, amount in base.items():
            mult = excuse_mod.get(stat, 1.0)
            final = int(amount * mult)
            if final != 0:
                Change_Status(girl, stat, final)
        if girl.has_npc_partner():
            Change_Status(girl, "Love", -10)
        print("[STEALTH_CONDOM] raw stats applied: trait=%s excuse=%s bf=%s" % (tk, excuse_key, girl.has_npc_partner()))

    def _stealth_raw_ends_scene(girl, excuse):
        tk = _condom_break_trait_key(girl)
        if tk == "cum_slut":
            return False
        if tk == "hardcore_sex":
            return False
        if tk == "hate_cum":
            return True
        if excuse == "moaned_louder" and tk == "cute_sex":
            return True
        return False

    def _stealth_cream_ends_scene(girl, excuse):
        tk = _condom_break_trait_key(girl)
        if tk == "cum_slut":
            return False
        if tk == "hardcore_sex":
            return False
        if tk == "hate_cum":
            return True
        if excuse == "moaned_louder":
            return True
        if excuse == "felt_too_good" and tk in ("cute_sex", "_default"):
            return True
        return False


# ============================================================
# STEALTH SUCCESS — condom removed undetected
# ============================================================
label _condom_stealth_success(girl, scene_type):

    $ _on_condom_removed(girl, skip_hide=False)
    $ store._creampie_consent = "denied"
    $ store._stealth_condom_removed = True
    $ store._condom_removed_midscene = True
    # Persistent per-girl counter (used by NHIE "lied about using protection")
    python:
        girl._stealth_condom_count = getattr(girl, "_stealth_condom_count", 0) + 1
        _sync_girl(girl)

    python:
        _stealth_narr = _tl(renpy.random.choice(_STEALTH_UNDETECTED_LINES))
    "[_stealth_narr]"

    $ unlock_achievement("stealth_master")
    $ print("[STEALTH_CONDOM] stealth success: scene_type=%s" % scene_type)

    return


# ============================================================
# STEALTH DISCOVERY — she finds out (position switch / look back)
# ============================================================
label StealthCondomDiscovery(girl, scene_type):
    $ _st_tk = _condom_break_trait_key(girl)
    $ set_scene_expression(girl, "startled")
    # Persistent: she now KNOWS he removed it (NHIE lie detection on "lied about protection")
    $ girl.RegisterAction("stealth_condom_discovered")

    # NTR context check
    python:
        _stdisc_ntr = False
        if hasattr(girl, "has_npc_partner") and girl.has_npc_partner():
            _stdisc_npc = get_npc_partner_for(girl)
            if _stdisc_npc and getattr(_stdisc_npc, "_ntr_active", False):
                if getattr(_stdisc_npc, "_ntr_boundary_level", 1) == 2:
                    _stdisc_ntr = True
        print("[STEALTH_CONDOM] discovery: ntr_context=%s trait=%s" % (_stdisc_ntr, _st_tk))

    python:
        _st_disc_pool = _STEALTH_DISCOVER_LINES.get(_st_tk, _STEALTH_DISCOVER_LINES["_default"])
    $ Say_Line(girl, _tl(renpy.random.choice(_st_disc_pool)))

    $ _st_is_hate_cum = girl.has_trait("hate_cum")
    menu:
        "It must have slipped off":
            $ _st_excuse = "slipped_off"
        "It felt too good without it":
            $ _st_excuse = "felt_too_good"
        "You didn't seem to mind" if not _st_is_hate_cum:
            $ _st_excuse = "moaned_louder"

    python:
        _st_exc_pool = _STEALTH_EXCUSE_LINES.get(_st_excuse, {})
        _st_exc_lines = _st_exc_pool.get(_st_tk, _st_exc_pool.get("_default", [_("I can't believe you.")]))
    $ Say_Line(girl, _tl(renpy.random.choice(_st_exc_lines)))

    # Belief check — only "slipped_off" can be believed
    $ _st_believed = (_st_excuse == "slipped_off" and _condom_break_belief_check(girl))
    $ print("[STEALTH_CONDOM] excuse=%s believed=%s trait=%s Love=%d ntr=%s" % (_st_excuse, _st_believed, _st_tk, girl.Love, _stdisc_ntr))

    # NTR extra penalty (lighter than creampie: raw only)
    if _stdisc_ntr:
        python:
            Change_Status(girl, "Love", -20)
            Change_Status(girl, "Obed", 15)
            Change_Status(girl, "Inbt", 15)
            print("[STEALTH_CONDOM] NTR raw extra penalty: Love-20 Obed+15 Inbt+15")

    $ _stealth_raw_apply_stats(girl, _st_excuse)
    $ store._stealth_condom_removed = False

    if _st_believed:
        python:
            _st_bel_pool = _STEALTH_CREAM_BELIEVED_LINES.get(_st_tk, _STEALTH_CREAM_BELIEVED_LINES["_default"])
        $ set_scene_expression(girl, "serious")
        $ Say_Line(girl, _tl(renpy.random.choice(_st_bel_pool)))
        python:
            _st_bel_narr_pool = _STEALTH_CREAM_NARR_BELIEVED.get(_st_tk, _STEALTH_CREAM_NARR_BELIEVED["_default"])
            _st_narr = _tl(renpy.random.choice(_st_bel_narr_pool))
        "[_st_narr]"
    else:
        if _stealth_raw_ends_scene(girl, _st_excuse):
            python:
                _st_end_pool = _STEALTH_RAW_ANGRY_END_LINES.get(_st_tk, _STEALTH_RAW_ANGRY_END_LINES["_default"])
            $ Say_Line(girl, _tl(renpy.random.choice(_st_end_pool)))
            python:
                _in_her_room = (store.CurrentLocation == girl.gid + "_room")
                _st_end_narr_pool = _STEALTH_CREAM_NARR_END_HERROOM if _in_her_room else _STEALTH_CREAM_NARR_END_ELSEWHERE
                _st_narr = _tl(renpy.random.choice(_st_end_narr_pool))
            "[_st_narr]"
            $ force_scene_reset(girl, angry_days=1, reason="stealth_raw")
            jump main_loop
        else:
            $ set_scene_expression(girl, "angry")
            python:
                _st_ang_narr_pool = _STEALTH_CREAM_NARR_ANGRY_CONT.get(_st_tk, _STEALTH_CREAM_NARR_ANGRY_CONT.get("hardcore_sex"))
                _st_narr = _tl(renpy.random.choice(_st_ang_narr_pool))
            "[_st_narr]"

    $ set_scene_expression(girl, "normal")
    return


# ============================================================
# STEALTH CREAMPIE REALIZATION — 2-phase discovery after cum
# inside with stealth condom removed. Called from the normal
# cum flow (PlayerCumMenu_Penetration_Raw) after process_cum.
# ============================================================
label _stealth_cream_realization(girl, scene_type):

    # Phase 1: she thinks the condom was used
    $ _st_tk = _condom_break_trait_key(girl)
    python:
        _st_calm_pool = _STEALTH_POSTCUM_CALM_LINES.get(_st_tk, _STEALTH_POSTCUM_CALM_LINES["_default"])
    $ set_scene_expression(girl, "smile")
    $ Say_Line(girl, _tl(renpy.random.choice(_st_calm_pool)))

    # Phase 2: she realizes something is wrong
    if getattr(store, "hiding_face", False):
        $ store.hiding_face = False
        python:
            _stealth_turn_narr = _tl(_("She suddenly whips her head around to face you."))
        "[_stealth_turn_narr]"

    python:
        _st_realize_pool = _STEALTH_POSTCUM_REALIZE_LINES.get(trait_pool_key(girl, _st_tk, _STEALTH_POSTCUM_REALIZE_LINES), _STEALTH_POSTCUM_REALIZE_LINES["_default"])
        _st_expr = _STEALTH_CUM_EXPRESSIONS.get(_st_tk, "surprised")
    $ set_scene_expression(girl, _st_expr)
    $ Say_Line(girl, _tl(renpy.random.choice(_st_realize_pool)))

    # Excuse menu
    $ _st_is_hate_cum = girl.has_trait("hate_cum")
    menu:
        "It must have slipped off":
            $ _st_excuse = "slipped_off"
        "It felt too good without it":
            $ _st_excuse = "felt_too_good"
        "You didn't seem to mind" if not _st_is_hate_cum:
            $ _st_excuse = "moaned_louder"

    python:
        _st_exc_pool = _STEALTH_EXCUSE_LINES.get(_st_excuse, {})
        _st_exc_lines = _st_exc_pool.get(_st_tk, _st_exc_pool.get("_default", [_("I can't believe you.")]))
    $ Say_Line(girl, _tl(renpy.random.choice(_st_exc_lines)))

    $ store._creampie_consent = "stealth_resolved"
    $ print("[STEALTH_CONDOM] creampie_consent set to stealth_resolved (aftermath will be skipped)")

    # NTR context check
    python:
        _stcum_ntr = False
        if hasattr(girl, "has_npc_partner") and girl.has_npc_partner():
            _stcum_npc = get_npc_partner_for(girl)
            if _stcum_npc and getattr(_stcum_npc, "_ntr_active", False):
                if getattr(_stcum_npc, "_ntr_boundary_level", 1) == 2:
                    _stcum_ntr = True

    if _stcum_ntr:
        python:
            Change_Status(girl, "Love", -30)
            Change_Status(girl, "Obed", 25)
            Change_Status(girl, "Inbt", 20)
            print("[STEALTH_CONDOM] NTR creampie extra penalty: Love-30 Obed+25 Inbt+20")

    # Belief check
    $ _st_believed = (_st_excuse == "slipped_off" and _condom_break_belief_check(girl))
    $ print("[STEALTH_CONDOM] cream excuse=%s believed=%s trait=%s Love=%d" % (_st_excuse, _st_believed, _st_tk, girl.Love))

    if _st_believed:
        $ _stealth_apply_stats(girl, "slipped_off")
        $ store._stealth_condom_removed = False
        python:
            _st_bel_pool = _STEALTH_CREAM_BELIEVED_LINES.get(_st_tk, _STEALTH_CREAM_BELIEVED_LINES["_default"])
        $ set_scene_expression(girl, "serious")
        $ Say_Line(girl, _tl(renpy.random.choice(_st_bel_pool)))
        python:
            _st_bel_narr_pool = _STEALTH_CREAM_NARR_BELIEVED.get(_st_tk, _STEALTH_CREAM_NARR_BELIEVED["_default"])
            _st_narr = _tl(renpy.random.choice(_st_bel_narr_pool))
        "[_st_narr]"
    else:
        $ _st_excuse_key = _st_excuse if _st_excuse != "slipped_off" else None
        $ _stealth_apply_stats(girl, _st_excuse_key)
        $ store._stealth_condom_removed = False

        if _stealth_cream_ends_scene(girl, _st_excuse):
            $ store._witness_expression_lock = True
            python:
                _st_end_pool = _STEALTH_CREAM_ANGRY_END_LINES.get(_st_tk, _STEALTH_CREAM_ANGRY_END_LINES["_default"])
            $ Say_Line(girl, _tl(renpy.random.choice(_st_end_pool)))
            python:
                _in_her_room = (store.CurrentLocation == girl.gid + "_room")
                _st_end_narr_pool = _STEALTH_CREAM_NARR_END_HERROOM if _in_her_room else _STEALTH_CREAM_NARR_END_ELSEWHERE
                _st_narr = _tl(renpy.random.choice(_st_end_narr_pool))
            "[_st_narr]"
            $ store._witness_expression_lock = False
            if getattr(girl, '_ntr_violation_pending', False):
                call _angry_end_ntr_confrontation(girl) from _call_aend_ntr_stealth_cream
            $ force_scene_reset(girl, angry_days=3, reason="stealth_creampie")
            jump main_loop
        else:
            $ set_scene_expression(girl, "angry")
            python:
                _st_ang_narr_pool = _STEALTH_CREAM_NARR_ANGRY_CONT.get(_st_tk, _STEALTH_CREAM_NARR_ANGRY_CONT.get("hardcore_sex"))
                _st_narr = _tl(renpy.random.choice(_st_ang_narr_pool))
            "[_st_narr]"

    $ set_scene_expression(girl, "normal")
    return
