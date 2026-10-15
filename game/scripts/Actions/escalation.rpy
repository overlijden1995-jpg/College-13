# ============================================================
# Centralized Escalation System
# Handles rub/tip/sex/anal transitions for ALL penetration
# positions. Each Core file handles only visuals.
# ============================================================

default _esc_result = "cancelled"
default _esc_target = None
default _esc_was_forced = False
default _esc_is_deescalation = False
default _esc_speed = 0
default _esc_condom_denied = False
default _esc_scene_type = None
default _esc_virgin_check = False
default _esc_anal_choice = False
default _esc_pen_result = None
default _esc_session_had_tip = False
default _esc_session_had_sex = False
default _esc_session_had_anal = False
default _esc_session_pen_result = None
default _esc_skip_condom = False

init python:

    # What a POSITION can do. Reverse cowgirl: anal only for a girl whose own art draws it (Core_RCG rcg_has_anal,
    # today Shion): esc_caps(girl, position) is what the menu reads.
    ESCALATION_CAPS = {
        "doggy":           {"rub": True, "tip": True, "sex": True, "anal": True},
        "cowgirl":         {"rub": True, "tip": True, "sex": True, "anal": False},
        "reverse_cowgirl": {"rub": True, "tip": True, "sex": True, "anal": False},
        "full_nelson":     {"rub": True, "tip": True, "sex": True, "anal": True},
        "laying_down":     {"rub": True, "tip": True, "sex": True, "anal": True},
    }

    def esc_caps(girl, position):
        """ESCALATION_CAPS of this position for THIS girl: her art may add a cap the position has not by itself."""
        _caps = dict(ESCALATION_CAPS.get(position, {}))
        if position == "reverse_cowgirl" and rcg_has_anal(girl):
            _caps["anal"] = True
        return _caps

    def _esc_current_state(position):
        if position == "doggy":
            if store.doggy_rub_mode and not store.doggy_started:
                return "rub"
            if store.doggy_tip_mode:
                return "tip"
            if store.doggy_started and store.doggy_anal:
                return "anal"
            if store.doggy_started:
                return "sex"
        elif position == "cowgirl":
            if store.cowgirl_rub_mode:
                return "rub"
            if store.cowgirl_tip_mode:
                return "tip"
            return "sex"
        elif position == "reverse_cowgirl":
            if store.rcg_rub_mode:
                return "rub"
            if store.rcg_tip_mode:
                return "tip"
            if getattr(store, "rcg_anal", False):
                return "anal"
            return "sex"
        elif position == "full_nelson":
            if store.fn_rub_mode and not store.fn_started:
                return "rub"
            if store.fn_tip_mode:
                return "tip"
            if store.fn_started and store.fn_anal:
                return "anal"
            if store.fn_started:
                return "sex"
        elif position == "laying_down":
            if store.laying_rub_mode and not store.laying_started:
                return "rub"
            if store.laying_tip_mode:
                return "tip"
            if store.laying_started and store.laying_anal:
                return "anal"
            if store.laying_started:
                return "sex"
        return "sex"

    def _esc_is_in_anal(position):
        if position == "doggy":
            return getattr(store, "doggy_anal", False)
        elif position == "full_nelson":
            return getattr(store, "fn_anal", False)
        elif position == "laying_down":
            return getattr(store, "laying_anal", False)
        elif position == "reverse_cowgirl":
            return getattr(store, "rcg_anal", False)
        return False

    def _esc_pick_line(girl, pool):
        _traits = [
            ("virgin", "virgin"),
            ("cute_sex", "cute_sex"),
            ("hardcore_sex", "hardcore_sex"),
            ("cum_slut", "cum_slut"),
        ]
        for trait_name, key in _traits:
            if girl.has_trait(trait_name) and key in pool:
                return _tl(renpy.random.choice(pool[key]))
        return _tl(renpy.random.choice(pool.get("default", pool.get("cute_sex", list(pool.values())[0]))))

    def _esc_has_anal(position):
        return ESCALATION_CAPS.get(position, {}).get("anal", False)

    # ── Session re-escalation bypass ──────────────────────

    _ESC_SESSION_FLAGS = {
        "tip":  "_esc_session_had_tip",
        "sex":  "_esc_session_had_sex",
        "anal": "_esc_session_had_anal",
    }

    def _esc_session_bypass(action):
        flag = _ESC_SESSION_FLAGS.get(action)
        if not flag or not getattr(store, flag, False):
            return False
        store._esc_result = "accepted"
        store._esc_target = action
        store._esc_was_forced = False
        store._esc_speed = 1
        store._esc_scene_type = action if action != "tip" else ("anal" if store._esc_anal_choice else "tip")
        if action in ("sex", "anal"):
            store._esc_skip_condom = True
        if action == "sex":
            store._esc_condom_denied = False
            store._esc_pen_result = store._esc_session_pen_result
            store._esc_virgin_check = False
        print("[ESCALATION] %s re-escalation bypass (session flag)" % action)
        return True

    def _esc_mark_session(action, pen_result=None):
        flag = _ESC_SESSION_FLAGS.get(action)
        if flag:
            setattr(store, flag, True)
        if action == "sex" and pen_result is not None:
            store._esc_session_pen_result = pen_result

    def _esc_session_reset():
        for attr in _ESC_SESSION_FLAGS.values():
            setattr(store, attr, False)
        _scene_marks_reset()   # scene over: the next scene counts "sex" / positions again
        store._esc_session_pen_result = None
        store._esc_skip_condom = False

    # ── Dialogue pools ────────────────────────────────────

    _ESC_TIP_ASK_ACCEPT = {
        "virgin": [
            _("J-just the tip...? You promise...? O-okay... but be careful..."),
            _("Only the tip... and if it hurts you stop immediately!"),
            _("I... I've never... okay, just the tip. JUST the tip!"),
        ],
        "cute_sex": [
            _("Just the tip...? O-okay... but don't push it further!"),
            _("You promise it's only the tip? ...fine, go ahead."),
            _("Mmm... okay, but be gentle with just the tip..."),
        ],
        "hardcore_sex": [
            _("Just the tip? Tease. Fine, put it in."),
            _("The tip? That's all? ...do it then."),
            _("Sure. But we both know you won't stop at the tip."),
        ],
        "default": [
            _("Just the tip...? Okay... but that's ALL."),
            _("Fine... but ONLY the tip. I mean it."),
            _("Okay... just the tip. Don't get any ideas."),
        ],
    }

    _ESC_TIP_ASK_DENY = [
        _("No! Not even the tip! Just keep rubbing."),
        _("Absolutely not. We agreed on rubbing only."),
        _("Don't even think about it. Rub only."),
    ]

    _ESC_TIP_FORCE_PRE = [
        _("Wait, what are you..."),
        _("H-hey, what are you doing back there..."),
        _("Wait... are you about to..."),
    ]

    _ESC_TIP_FORCE_ACCEPT = {
        "virgin": [
            _("AH! W-what are you... is that...?! You said just rubbing!"),
            _("Oh my god! That's... that's inside me! Just the tip?! JUST THE TIP?!"),
            _("WHAT ARE YOU DOING?! ...oh... oh god... it's just the tip... right?"),
        ],
        "cute_sex": [
            _("Ah! You just... oh! That's not rubbing anymore!"),
            _("W-wait! Is that inside?! You said... mmm... okay but JUST the tip!"),
            _("WHAT ARE YOU DOING?! ...oh my god... but don't push it further!"),
        ],
        "default": [
            _("Hey! That's not... oh... okay, just the tip. JUST the tip!"),
            _("You sneaky... fine, but don't you DARE go deeper."),
            _("I felt that! You said rubbing! ...okay, but just the tip."),
        ],
    }

    _ESC_TIP_FORCE_REACT = [
        _("Oh my god... but don't push it further!"),
        _("You better keep that promise..."),
        _("I swear if you go deeper..."),
    ]

    _ESC_TIP_FORCE_DENY = [
        _("WHAT THE HELL?! I said RUBBING ONLY! We're done!"),
        _("Did you just try to put it in?! Get OFF me!"),
        _("NO! That was NOT part of the deal! This is OVER!"),
    ]

    _ESC_SEX_ASK_ACCEPT = [
        _("Mmm... okay. Put it in."),
        _("I was hoping you'd ask... go ahead."),
        _("You want to go further? ...alright, do it."),
    ]

    _ESC_SEX_ASK_DENY = [
        _("No... I'm not ready for that."),
        _("Just keep rubbing... I don't want to go further."),
        _("Not yet... this is enough for now."),
    ]

    _ESC_SEX_ASK_FROM_TIP_ACCEPT = [
        _("Mmm... okay, put it all in."),
        _("Go deeper? ...okay, do it."),
        _("All the way? ...yes, go ahead."),
    ]

    _ESC_SEX_ASK_FROM_TIP_DENY = [
        _("No... just the tip is enough."),
        _("Don't push it further. The tip is all you get."),
        _("I said just the tip and I mean it."),
    ]

    _ESC_SEX_FORCE_PRE = [
        _("Wait, what are you..."),
        _("H-hey, what are you doing..."),
        _("Hold on, are you about to..."),
    ]

    _ESC_SEX_FORCE_DENY_FROM_RUB = [
        _("What the HELL?! I said we're just rubbing! Get off me!"),
        _("NO! We agreed on RUBBING ONLY! This is OVER!"),
        _("Are you INSANE?! I said rubbing! We're done here!"),
    ]

    _ESC_SEX_FORCE_DENY_FROM_TIP = [
        _("What the HELL?! I said JUST THE TIP! We're DONE!"),
        _("You pushed it all the way in?! Get OUT! We're done!"),
        _("NO! I said the TIP! That's NOT the tip! STOP!"),
    ]

    _ESC_ANAL_ASK_ACCEPT = [
        _("My ass? ...okay, go slow."),
        _("You want to do THAT? ...fine, but be gentle."),
        _("Alright... just... take it slow at first, okay?"),
    ]

    _ESC_ANAL_ASK_DENY = [
        _("My ass? Are you crazy? No way."),
        _("Absolutely not. You're not putting it there."),
        _("Not a chance. That's off limits."),
        _("No. Just... no. Forget about it."),
    ]

    _ESC_ANAL_ASK_DENY_SUGGEST_TIP = [
        _("Not like that... if you want to try... start slow. Just the tip."),
        _("My ass? Maybe... but you'd have to start really, really gentle."),
        _("I'm not ready for that. But... if you just wanted to feel it... maybe the tip."),
    ]

    _ESC_ANAL_HATER_TIP_REACT = [
        _("Wait, that's not... oh god, my ass!"),
        _("H-hey, what are you... nngh... that's my..."),
        _("I said JUST the... ah! ...oh god, go slow..."),
    ]

    _ESC_ANAL_HATER_TIP_REFUSE = [
        _("Not even the tip. I said NO."),
        _("The tip?! Absolutely not. Drop it."),
        _("I don't care if it's 'just the tip'. The answer is no."),
    ]

    _ESC_ANAL_FORCE_DENY = {
        "cute_anal_hater": {
            "lines": [
                _("STOP! OW OW OW! WHAT THE HELL?! NOT MY ASS! You're DISGUSTING!"),
                _("GET IT OUT!! THAT'S MY ASS!! I said NO!! You MONSTER!"),
            ],
            "love": -40, "obed": -15, "angry": True,
        },
        "cute_sex": {
            "lines": [
                _("NO! GET IT OUT! My ass?! Are you INSANE?!"),
                _("STOP!! NOT THERE!! What is WRONG with you?!"),
            ],
            "love": -25, "obed": -10, "angry": False,
        },
        "anal_hater": {
            "lines": [
                _("WHAT THE HELL?! NOT MY ASS!! Get it OUT!!"),
                _("ARE YOU SERIOUS?! I said NOT THERE! We're DONE!"),
            ],
            "love": -25, "obed": -10, "angry": False,
        },
        "default": {
            "lines": [
                _("AH! Not there! What the hell?!"),
                _("Did you just... my ASS?! Get it out! NOW!"),
            ],
            "love": -15, "obed": -5, "angry": False,
        },
    }

    _ESC_CHEAT_GATE_LINES = {
        "tip": _("That's enough for today... maybe next time we can go a little further..."),
        "tip_force": _("No! Not today! We agreed on just rubbing!"),
        "sex": _("Not yet... I'm not ready for that."),
        "sex_force": _("What?! No! I told you I'm not ready for that!"),
        "anal": _("No... that's way too far. Not happening."),
        "anal_force": _("No... that's way too far. Not happening."),
    }

    _ESC_DEESCALATION_LINES = {
        ("tip", "rub"): [
            _("Wait, you're pulling out? ...okay, just rubbing then."),
            _("Oh... back to rubbing? Alright..."),
            _("Hmm? You don't want the tip anymore? ...fine."),
        ],
        ("sex", "rub"): [
            _("You're pulling out completely? Just rubbing again?"),
            _("Oh... okay, just rubbing... if that's what you want."),
            _("Back to just rubbing? ...alright then."),
        ],
        ("sex", "tip"): [
            _("You're pulling back? Just the tip again?"),
            _("Mmm... okay, just the tip then..."),
            _("Oh... going back to just the tip? Alright..."),
        ],
        ("anal", "rub"): [
            _("Oh, pulling out? ...just rubbing again? Okay."),
            _("Back to rubbing after that? ...fine by me."),
        ],
        ("anal", "tip"): [
            _("Going back to just the tip? ...okay."),
            _("Oh... okay, just the tip again."),
        ],
        ("anal", "sex"): [
            _("Switching back to normal? Okay..."),
            _("My pussy again? ...okay, go ahead."),
        ],
    }

    def _esc_anal_force_deny_key(girl):
        if girl.has_trait("cute_sex") and girl.has_trait("anal_hater"):
            return "cute_anal_hater"
        if girl.has_trait("cute_sex"):
            return "cute_sex"
        if girl.has_trait("anal_hater"):
            return "anal_hater"
        return "default"

    # ── What she says as the Core files switch holes (the doggy's lines of 2026, shared by every pose with anal) ──
    # He shoved it in her ass without asking (the anal escalation from rub / tip, forced)
    _ESC_ANAL_FORCE_POST = [
        _("Ah! You just... put it in my ass... oh fuck..."),
        _("W-wait! That's my ASS! Oh god..."),
        _("You didn't even ask! ...ngh... it's so tight..."),
    ]
    # Pussy -> ass without asking: as he pulls out, and once he is in
    _ESC_SWITCH_TO_ANAL_PRE = [
        _("Wait, that's my..."),
        _("H-hey! Wrong hole!"),
        _("Hold on, that's not my..."),
    ]
    _ESC_SWITCH_TO_ANAL_POST = [
        _("AH! That's my ass! ...oh god..."),
        _("You just switched holes! ...mmm..."),
        _("Hey! That's... oh... don't stop..."),
    ]
    # Ass -> pussy without asking: as he pulls out, and once he is in
    _ESC_SWITCH_TO_PUSSY_PRE = [
        _("Wait, you're switching..."),
        _("H-hey, that's a different..."),
        _("Hold on, you're pulling out and..."),
    ]
    _ESC_SWITCH_TO_PUSSY_POST = [
        _("Ah! You switched! ...mmm..."),
        _("You could have asked... but don't stop."),
    ]
    # Ass -> pussy, asked and accepted (_esc_pick_line: her trait's pool, else default)
    _ESC_SWITCH_TO_PUSSY_ASK = {
        "hardcore_sex": [
            _("From my ass to my pussy? Dirty. I like it. Go ahead."),
            _("You want to switch? Fine, shove it in."),
        ],
        "cum_slut": [
            _("Mmm, switch wherever you want... I just want you inside me."),
            _("My pussy, my ass, I don't care... just don't stop."),
        ],
        "default": [
            _("Mmm... okay. Switch to my pussy."),
            _("You want to switch? Sure... put it in."),
        ],
    }


# ============================================================
# Main escalation menu label
# Sets store._esc_* result variables, returns to caller
# ============================================================
label _escalation_menu(girl, position):
    python:
        store._esc_result = "cancelled"
        store._esc_target = None
        store._esc_was_forced = False
        store._esc_is_deescalation = False
        store._esc_speed = 0
        store._esc_condom_denied = False
        store._esc_scene_type = None
        store._esc_virgin_check = False
        store._esc_anal_choice = False
        store._esc_pen_result = None

        _es = _esc_current_state(position)
        _es_caps = esc_caps(girl, position)
        _es_anal = _es_caps.get("anal", False)
        _es_bottom = _bottom_accessible(girl)
        _es_is_rub = (_es == "rub")
        _es_is_tip = (_es == "tip")
        _es_is_sex = (_es == "sex")
        _es_is_anal = (_es == "anal")
        _es_in_anal = _esc_is_in_anal(position)
        _es_pos_key = {"reverse_cowgirl": "rcg", "cowgirl": "cowgirl", "doggy": "doggy", "full_nelson": "full_nelson", "laying_down": "laying_down"}.get(position)
        _es_has_rub = bool(_gsc(girl.gid, "has_rub", True, _es_pos_key)) if _es_pos_key else True
        _es_can_back_rub = not _es_is_rub and _es_has_rub
        _es_can_back_tip = (_es_is_sex or _es_is_anal)

        _es_cheat = _is_on_cheat_path(girl)
        _es_cheat_tip = _es_cheat and not _cheat_can_tip(girl)
        _es_cheat_sex = _es_cheat and not _cheat_can_sex(girl)
        _es_cheat_anal = _es_cheat and not _cheat_can_anal(girl)

        print("[ESCALATION] state=%s pos=%s anal_cap=%s bottom=%s cheat=%s" % (_es, position, _es_anal, _es_bottom, _es_cheat))

    while True:
        menu:
            # ── De-escalation ──────────────────────────────
            "Go back to rubbing" if _es_can_back_rub:
                $ store._esc_target = "rub"
                $ store._esc_is_deescalation = True
                $ store._esc_speed = 0
                $ Say_Line(girl, _tl(renpy.random.choice(_ESC_DEESCALATION_LINES.get((_es, "rub"), [_("Okay...")]))))
                $ store._esc_result = "accepted"
                return

            "Go back to just the tip" if _es_can_back_tip:
                $ store._esc_target = "tip"
                $ store._esc_is_deescalation = True
                $ store._esc_speed = 1
                $ Say_Line(girl, _tl(renpy.random.choice(_ESC_DEESCALATION_LINES.get((_es, "tip"), [_("Okay...")]))))
                $ store._esc_result = "accepted"
                return

            # ── Pussy section header ───────────────────────
            "!section!PUSSY" if (_es_is_rub or _es_is_tip) and _es_anal:
                pass

            # Vaginal tip (from rub)
            "Ask to insert the tip" if _es_is_rub and not _es_anal:
                $ store._esc_anal_choice = False
                call _esc_ask_tip(girl, position) from _call_esc_ask_tip
                return

            "Ask to put the tip in" if _es_is_rub and _es_anal:
                $ store._esc_anal_choice = False
                call _esc_ask_tip(girl, position) from _call_esc_ask_tip_p
                return

            "Insert the tip" if _es_is_rub and _es_bottom and not _es_anal:
                $ store._esc_anal_choice = False
                call _esc_force_tip(girl, position) from _call_esc_force_tip
                return

            "Put the tip in" if _es_is_rub and _es_bottom and _es_anal:
                $ store._esc_anal_choice = False
                call _esc_force_tip(girl, position) from _call_esc_force_tip_p
                return

            # Vaginal sex (from rub or tip)
            "Ask to fuck her pussy" if (_es_is_rub or _es_is_tip) and _es_anal:
                call _esc_ask_sex(girl, position) from _call_esc_ask_sex_p
                return

            "Ask to fuck her" if (_es_is_rub or _es_is_tip) and not _es_anal:
                call _esc_ask_sex(girl, position) from _call_esc_ask_sex
                return

            "Fuck her pussy (without asking)" if (_es_is_rub or _es_is_tip) and _es_anal and _es_bottom:
                call _esc_force_sex(girl, position) from _call_esc_force_sex_p
                return

            "Fuck her (without asking)" if (_es_is_rub or _es_is_tip) and not _es_anal and _es_bottom:
                call _esc_force_sex(girl, position) from _call_esc_force_sex
                return

            # ── Anal section header ────────────────────────
            "!section!ANAL" if _es_anal and (_es_is_rub or _es_is_tip):
                pass

            # Anal tip (from rub)
            "Ask to put the tip in her ass" if _es_is_rub and _es_anal:
                $ store._esc_anal_choice = True
                call _esc_ask_tip(girl, position) from _call_esc_ask_tip_a
                return

            "Put the tip in her ass" if _es_is_rub and _es_anal and _es_bottom:
                $ store._esc_anal_choice = True
                call _esc_force_tip(girl, position) from _call_esc_force_tip_a
                return

            # Anal sex (from rub or tip — shows even from anal tip to escalate to full anal)
            "Ask to fuck her ass" if _es_anal and (_es_is_rub or _es_is_tip):
                call _esc_ask_anal(girl, position) from _call_esc_ask_anal_rt
                return

            "Fuck her ass (without asking)" if _es_anal and (_es_is_rub or _es_is_tip) and _es_bottom:
                call _esc_force_anal(girl, position) from _call_esc_force_anal_rt
                return

            # ── Switch holes (from sex/anal) ───────────────
            "!section!ANAL" if _es_is_sex and _es_anal and not _es_in_anal:
                pass

            "Ask to switch to anal" if _es_is_sex and _es_anal and not _es_in_anal:
                call _esc_ask_anal(girl, position) from _call_esc_ask_anal_switch
                return

            "Switch to anal (without asking)" if _es_is_sex and _es_anal and not _es_in_anal and _es_bottom:
                call _esc_force_anal(girl, position) from _call_esc_force_anal_switch
                return

            "!section!PUSSY" if _es_is_anal:
                pass

            "Ask to switch to pussy" if _es_is_anal:
                call _esc_ask_sex_from_anal(girl, position) from _call_esc_ask_sex_anal
                return

            "Switch to pussy (without asking)" if _es_is_anal:
                call _esc_force_sex_from_anal(girl, position) from _call_esc_force_sex_anal
                return

            "Back":
                return

    return


# Her step locks the act (story_steps.rpy): her line, nothing else happens
label _esc_story_deny(girl, act):
    $ set_scene_expression(girl, "smug")
    $ Say_Line(girl, story_locked_line(girl, act))
    $ store._esc_result = "denied"
    return

# ============================================================
# ASK TIP (from rub)
# ============================================================
label _esc_ask_tip(girl, position):
    # her step locks it (story_steps.rpy): asked or not, she stops him and the scene goes on
    if story_act_locked(girl, "tip_anal" if store._esc_anal_choice else "tip"):
        call _esc_story_deny(girl, "tip_anal" if store._esc_anal_choice else "tip") from _call_esc_story_deny_ask_tip
        return

    if _is_on_cheat_path(girl) and not _cheat_can_tip(girl):
        $ _notify_cheat_heat(girl, "gate_tip", False)
        $ Say_Line(girl, _ESC_CHEAT_GATE_LINES["tip"])
        $ store._esc_result = "denied"
        return

    if _esc_session_bypass("tip"):
        return

    $ _tip = tip_check(girl, anal=store._esc_anal_choice)
    if _tip["accepted"]:
        call _ntr_escalation_gate(girl, "sex") from _call_ntr_gate_esc_ask_tip
        if not store._ntr_gate_passed:
            $ store._esc_result = "denied"
            return

        $ _notify_cheat_heat(girl, "scene_tip")
        if _is_on_cheat_path(girl) and _cheat_stage(girl) < 2:
            $ Say_Line(girl, _cheat_tip_first_line(girl))
            if _is_on_cheat_path(girl):
                $ _advance_cheat_stage(girl, 2)
        $ Say_Line(girl, _esc_pick_line(girl, _ESC_TIP_ASK_ACCEPT))
        $ mark_intimacy(girl, "tip")

        if store._esc_anal_choice:
            call _ntr_escalation_gate(girl, "anal") from _call_ntr_gate_esc_ask_tip_anal
            if not store._ntr_gate_passed:
                $ store._esc_result = "denied"
                return

        python:
            store._esc_result = "accepted"
            store._esc_target = "tip"
            store._esc_was_forced = False
            store._esc_speed = 1
            store._esc_scene_type = "anal" if store._esc_anal_choice else "tip"
            _esc_mark_session("tip")
    else:
        # an offended check carries her own rant (skip_line); the generic deny covers the rest
        $ _tip_deny = _tip.get("skip_line")
        $ Say_Line(girl, _tip_deny or _tl(renpy.random.choice(_ESC_TIP_ASK_DENY)))
        $ store._esc_result = "denied"
    return


# ============================================================
# FORCE TIP (from rub)
# ============================================================
label _esc_force_tip(girl, position):
    # her step locks it (story_steps.rpy): asked or not, she stops him and the scene goes on
    if story_act_locked(girl, "tip_anal" if store._esc_anal_choice else "tip"):
        call _esc_story_deny(girl, "tip_anal" if store._esc_anal_choice else "tip") from _call_esc_story_deny_force_tip
        return

    if _is_on_cheat_path(girl) and not _cheat_can_tip(girl):
        $ _notify_cheat_heat(girl, "gate_tip", False)
        $ Say_Line(girl, _ESC_CHEAT_GATE_LINES["tip_force"])
        $ store._esc_result = "denied"
        return

    if _esc_session_bypass("tip"):
        return

    $ _tip = tip_check(girl, anal=store._esc_anal_choice)
    if _is_on_cheat_path(girl) and _cheat_stage(girl) < 2:
        $ _advance_cheat_stage(girl, 2)

    if _tip["accepted"]:
        call _ntr_escalation_gate(girl, "sex") from _call_ntr_gate_esc_force_tip
        if not store._ntr_gate_passed:
            $ store._esc_result = "denied"
            return

        $ set_scene_expression(girl, "surprised")
        $ Say_Line(girl, _tl(renpy.random.choice(_ESC_TIP_FORCE_PRE)))
        $ mark_intimacy(girl, "tip")
        $ Change_Status(girl, "Obed", 3)
        $ Change_Status(girl, "Inbt", 3)

        if store._esc_anal_choice:
            call _ntr_escalation_gate(girl, "anal") from _call_ntr_gate_esc_force_tip_anal
            if not store._ntr_gate_passed:
                $ store._esc_result = "denied"
                return

        python:
            store._esc_result = "accepted"
            store._esc_target = "tip"
            store._esc_was_forced = True
            store._esc_speed = 1
            store._esc_scene_type = "anal" if store._esc_anal_choice else "tip"
            _esc_mark_session("tip")
    else:
        $ _tip_deny = _tip.get("skip_line")
        $ set_scene_expression(girl, "angry" if _tip_deny else "scared")
        $ Say_Line(girl, _tip_deny or _tl(renpy.random.choice(_ESC_TIP_FORCE_DENY)))
        $ Change_Status(girl, "Love", -10)
        $ Change_Status(girl, "Obed", -3)
        python:
            store._esc_result = "scene_ended"
            store._esc_target = None
    return


# ============================================================
# ASK SEX (from rub or tip)
# ============================================================
label _esc_ask_sex(girl, position):
    # her step locks it (story_steps.rpy): asked or not, she stops him and the scene goes on
    if story_act_locked(girl, "sex"):
        call _esc_story_deny(girl, "sex") from _call_esc_story_deny_ask_sex
        return

    if _is_on_cheat_path(girl) and not _cheat_can_sex(girl):
        $ _notify_cheat_heat(girl, "gate_sex", False)
        $ Say_Line(girl, _ESC_CHEAT_GATE_LINES["sex"])
        $ store._esc_result = "denied"
        return

    if _esc_session_bypass("sex"):
        return

    # Anal preference complaint when choosing pussy over anal
    python:
        _esc_ap = getattr(girl, "_anal_preference", 0)
        _esc_anal_cap = esc_caps(girl, position).get("anal", False)
        _esc_should_complain = _esc_anal_cap and ((_esc_ap >= 3) or (_esc_ap >= 2 and renpy.random.random() < 0.5))

    $ _pen = sex_penetration_check(girl)
    if _pen["accepted"]:
        if _esc_should_complain:
            python:
                _esc_vc_key = "vaginal_complaint_addicted" if _esc_ap >= 3 else "vaginal_complaint"
                _esc_vc = scene_pick_line(_esc_vc_key, scene="escalation", girl=girl)
            if _esc_vc:
                $ Say_Line(girl, _esc_vc)

        python:
            _from_tip = (_esc_current_state(position) == "tip")
        if _is_on_cheat_path(girl) and _cheat_stage(girl) < 3:
            $ Say_Line(girl, _cheat_sex_first_line(girl))
        else:
            if _from_tip:
                $ Say_Line(girl, _tl(renpy.random.choice(_ESC_SEX_ASK_FROM_TIP_ACCEPT)))
            else:
                $ Say_Line(girl, _tl(renpy.random.choice(_ESC_SEX_ASK_ACCEPT)))

        python:
            store._esc_result = "accepted"
            store._esc_target = "sex"
            store._esc_was_forced = False
            store._esc_speed = 1
            store._esc_scene_type = "sex"
            store._esc_condom_denied = False
            store._esc_pen_result = _pen
            store._esc_virgin_check = girl.has_trait("virgin")
            _esc_mark_session("sex", _pen)
    else:
        $ _skip_l = _pen.get("skip_line")
        if _skip_l:
            $ Say_Line(girl, _skip_l)
        else:
            python:
                _from_tip = (_esc_current_state(position) == "tip")
            if _from_tip:
                $ Say_Line(girl, _tl(renpy.random.choice(_ESC_SEX_ASK_FROM_TIP_DENY)))
            else:
                $ Say_Line(girl, _tl(renpy.random.choice(_ESC_SEX_ASK_DENY)))
        $ store._esc_result = "denied"
    return


# ============================================================
# FORCE SEX (from rub or tip)
# ============================================================
label _esc_force_sex(girl, position):
    # her step locks it (story_steps.rpy): asked or not, she stops him and the scene goes on
    if story_act_locked(girl, "sex"):
        call _esc_story_deny(girl, "sex") from _call_esc_story_deny_force_sex
        return

    if _is_on_cheat_path(girl) and not _cheat_can_sex(girl):
        $ _notify_cheat_heat(girl, "gate_sex", False)
        $ set_scene_expression(girl, "angry")
        $ Say_Line(girl, _ESC_CHEAT_GATE_LINES["sex_force"])
        $ store._esc_result = "denied"
        return

    if _esc_session_bypass("sex"):
        return

    $ _pen = sex_penetration_check(girl)
    if _pen["accepted"]:
        $ set_scene_expression(girl, "surprised")
        $ Say_Line(girl, _tl(renpy.random.choice(_ESC_SEX_FORCE_PRE)))

        python:
            store._esc_result = "accepted"
            store._esc_target = "sex"
            store._esc_was_forced = True
            store._esc_speed = 2
            store._esc_scene_type = "sex"
            store._esc_condom_denied = False
            store._esc_pen_result = _pen
            store._esc_virgin_check = girl.has_trait("virgin")
            _esc_mark_session("sex", _pen)
    else:
        $ set_scene_expression(girl, "scared")
        python:
            _from_tip = (_esc_current_state(position) == "tip")
        if _from_tip:
            $ Say_Line(girl, _tl(renpy.random.choice(_ESC_SEX_FORCE_DENY_FROM_TIP)))
        else:
            $ Say_Line(girl, _tl(renpy.random.choice(_ESC_SEX_FORCE_DENY_FROM_RUB)))
        $ Change_Status(girl, "Love", -15)
        $ Change_Status(girl, "Obed", -5)
        python:
            store._esc_result = "scene_ended"
            store._esc_target = None
    return


# ============================================================
# ASK ANAL (from rub, tip, or sex switch)
# ============================================================
label _esc_ask_anal(girl, position):
    # her step locks it (story_steps.rpy): asked or not, she stops him and the scene goes on
    if story_act_locked(girl, "anal"):
        call _esc_story_deny(girl, "anal") from _call_esc_story_deny_ask_anal
        return

    if _is_on_cheat_path(girl) and not _cheat_can_anal(girl):
        $ _notify_cheat_heat(girl, "gate_anal", False)
        $ Say_Line(girl, _ESC_CHEAT_GATE_LINES["anal"])
        $ store._esc_result = "denied"
        return

    if _esc_session_bypass("anal"):
        return

    $ _pen = anal_penetration_check(girl)
    if _pen["accepted"]:
        call _ntr_escalation_gate(girl, "anal") from _call_ntr_gate_esc_ask_anal
        if not store._ntr_gate_passed:
            $ store._esc_result = "denied"
            return

        if _is_on_cheat_path(girl) and _cheat_stage(girl) < 3:
            $ Say_Line(girl, _cheat_anal_first_line(girl))
        else:
            python:
                _girl_line = _get_girl_anal_line(girl, "accept")
                if _girl_line:
                    Say_Line(girl, _girl_line)
                else:
                    Say_Line(girl, _tl(renpy.random.choice(_ESC_ANAL_ASK_ACCEPT)))

        python:
            store._esc_result = "accepted"
            store._esc_target = "anal"
            store._esc_was_forced = False
            store._esc_speed = 1
            store._esc_scene_type = "anal"
            _esc_mark_session("anal")
    else:
        python:
            _skip_l = _pen.get("skip_line")
            _suggest = _pen.get("suggest_tip")

        if _skip_l:
            $ Say_Line(girl, _skip_l)
        elif _suggest:
            $ Say_Line(girl, _tl(renpy.random.choice(_ESC_ANAL_ASK_DENY_SUGGEST_TIP)))
        else:
            python:
                _girl_line = _get_girl_anal_line(girl, "deny")
                if _girl_line:
                    Say_Line(girl, _girl_line)
                else:
                    Say_Line(girl, _tl(renpy.random.choice(_ESC_ANAL_ASK_DENY)))

        if girl.has_trait("anal_hater"):
            $ _esc_hater_tip_text = _("Alright, let's try just the tip.") if _suggest else _("C'mon, just the tip. It will be good for you.")
            menu:
                "[_esc_hater_tip_text]":
                    if getattr(girl, "Obed", 0) >= 600 or getattr(girl, "Inbt", 0) >= 600:
                        call _ntr_escalation_gate(girl, "anal") from _call_ntr_gate_esc_ask_anal_hater
                        if not store._ntr_gate_passed:
                            $ store._esc_result = "denied"
                            return
                        $ Say_Line(girl, _tl(renpy.random.choice(_ESC_ANAL_HATER_TIP_REACT)))
                        $ mark_intimacy(girl, "tip")
                        python:
                            store._esc_result = "accepted"
                            store._esc_target = "tip"
                            store._esc_anal_choice = True
                            store._esc_was_forced = True
                            store._esc_speed = 1
                            store._esc_scene_type = "anal"
                        return
                    else:
                        $ Say_Line(girl, _tl(renpy.random.choice(_ESC_ANAL_HATER_TIP_REFUSE)))
                "Never mind":
                    pass

        $ store._esc_result = "denied"
    return


# ============================================================
# FORCE ANAL (from rub, tip, or sex switch)
# ============================================================
label _esc_force_anal(girl, position):
    # her step locks it (story_steps.rpy): asked or not, she stops him and the scene goes on
    if story_act_locked(girl, "anal"):
        call _esc_story_deny(girl, "anal") from _call_esc_story_deny_force_anal
        return

    if _is_on_cheat_path(girl) and not _cheat_can_anal(girl):
        $ _notify_cheat_heat(girl, "gate_anal", False)
        $ set_scene_expression(girl, "angry")
        $ Say_Line(girl, _ESC_CHEAT_GATE_LINES["anal_force"])
        $ store._esc_result = "denied"
        return

    if _esc_session_bypass("anal"):
        return

    $ _pen = anal_penetration_check(girl)
    if _pen["accepted"]:
        call _ntr_escalation_gate(girl, "anal") from _call_ntr_gate_esc_force_anal
        if not store._ntr_gate_passed:
            $ store._esc_result = "denied"
            return

        $ set_scene_expression(girl, "surprised")

        python:
            store._esc_result = "accepted"
            store._esc_target = "anal"
            store._esc_was_forced = True
            store._esc_speed = 2
            store._esc_scene_type = "anal"
            _esc_mark_session("anal")
    else:
        $ set_scene_expression(girl, "scared")
        python:
            _deny_key = _esc_anal_force_deny_key(girl)
            _deny_data = _ESC_ANAL_FORCE_DENY[_deny_key]
        $ Say_Line(girl, _tl(renpy.random.choice(_deny_data["lines"])))
        $ Change_Status(girl, "Love", _deny_data["love"])
        $ Change_Status(girl, "Obed", _deny_data["obed"])
        if _deny_data.get("angry"):
            $ girl.set_temp_status("angry", 2)
        python:
            store._esc_result = "scene_ended"
            store._esc_target = None
    return


# ============================================================
# ASK SEX FROM ANAL (hole switch, requires ATP hygiene)
# ============================================================
label _esc_ask_sex_from_anal(girl, position):
    if _is_on_cheat_path(girl) and not _cheat_can_sex(girl):
        $ _notify_cheat_heat(girl, "gate_sex", False)
        $ Say_Line(girl, _ESC_CHEAT_GATE_LINES["sex"])
        $ store._esc_result = "denied"
        return

    # Anal preference: she complains about switching away from anal
    python:
        _esc_ap = getattr(girl, "_anal_preference", 0)
        _esc_should_complain = _esc_ap >= 3 or (_esc_ap >= 2 and renpy.random.random() < 0.5)
    if _esc_should_complain:
        python:
            _esc_vc_key = "vaginal_complaint_addicted" if _esc_ap >= 3 else "vaginal_complaint"
            _esc_vc = scene_pick_line(_esc_vc_key, scene="escalation", girl=girl)
        if _esc_vc:
            $ Say_Line(girl, _esc_vc)

    if store._esc_session_had_sex:
        $ _pen = store._esc_session_pen_result
        if _pen is None:
            $ _pen = sex_penetration_check(girl)
        $ print("[ESCALATION] sex_from_anal approval bypass (session flag)")
    else:
        $ _pen = sex_penetration_check(girl)
    if _pen["accepted"]:
        call _ntr_escalation_gate(girl, "pussy_switch") from _call_ntr_gate_esc_ask_pswitch
        if not store._ntr_gate_passed:
            $ store._esc_result = "denied"
            return

        $ _atp = atp_hygiene_check(girl)
        $ store._esc_atp_result = _atp
        if _atp["outcome"] == "deny":
            $ set_scene_expression(girl, "disgusted")
            $ Say_Line(girl, _("No way, not after being in my ass!"))
            $ store._esc_result = "denied"
            return

        python:
            store._esc_result = "accepted"
            store._esc_target = "sex"
            store._esc_was_forced = False
            store._esc_speed = 1
            store._esc_scene_type = "sex"
            store._esc_virgin_check = False
            _esc_mark_session("sex", _pen)
    else:
        $ _skip_l = _pen.get("skip_line")
        if _skip_l:
            $ Say_Line(girl, _skip_l)
        else:
            $ Say_Line(girl, _("No... keep going like this."))
        $ store._esc_result = "denied"
    return


# ============================================================
# FORCE SEX FROM ANAL (hole switch with ATP)
# ============================================================
label _esc_force_sex_from_anal(girl, position):
    if _is_on_cheat_path(girl) and not _cheat_can_sex(girl):
        $ _notify_cheat_heat(girl, "gate_sex", False)
        $ set_scene_expression(girl, "angry")
        $ Say_Line(girl, _ESC_CHEAT_GATE_LINES["sex_force"])
        $ store._esc_result = "denied"
        return

    if store._esc_session_had_sex:
        $ _pen = store._esc_session_pen_result
        if _pen is None:
            $ _pen = sex_penetration_check(girl)
        $ print("[ESCALATION] force_sex_from_anal approval bypass (session flag)")
    else:
        $ _pen = sex_penetration_check(girl)
    if _pen["accepted"]:
        call _ntr_escalation_gate(girl, "pussy_switch") from _call_ntr_gate_esc_force_pswitch
        if not store._ntr_gate_passed:
            $ store._esc_result = "denied"
            return

        $ _atp = atp_hygiene_check(girl)
        $ store._esc_atp_result = _atp
        if _atp["outcome"] == "deny":
            $ set_scene_expression(girl, "disgusted")
            $ Say_Line(girl, _("No way, not after being in my ass!"))
            $ Change_Status(girl, "Love", -10)
            python:
                store._esc_result = "scene_ended"
                store._esc_target = None
            return

        python:
            store._esc_result = "accepted"
            store._esc_target = "sex"
            store._esc_was_forced = True
            store._esc_speed = 2
            store._esc_scene_type = "sex"
            store._esc_virgin_check = False
            _esc_mark_session("sex", _pen)
    else:
        $ set_scene_expression(girl, "scared")
        $ Say_Line(girl, _("NO! You can't just switch like that! We're done!"))
        $ Change_Status(girl, "Love", -10)
        $ Change_Status(girl, "Obed", -3)
        python:
            store._esc_result = "scene_ended"
            store._esc_target = None
    return


# ============================================================
# ANAL SCENE -> VAGINAL-ONLY POSITION (player "Switch position..." to Riding / Reverse Cowgirl)
# ============================================================
# Riding has no anal variant (reverse cowgirl only for a girl whose art has it: rcg_has_anal, and then the switch
# carries the hole over instead), so leaving an anal scene for a vaginal-only position IS the hole switch
# "Switch to her pussy", and it used to skip every gate of it. This runs the same ones:
# cheat path gate, sex approval (virgin / lesbian stage / stats), NTR boundary, ATP hygiene, condom.
# She says her own refusal and the scene simply goes on where it was: the button is never hidden.
# Out: store._switch_gate_ok (go ahead) / store._switch_gate_scene_ended (cheat path breakdown ended it).
init python:
    # Hole switch anal -> vaginal: she wants a condom because of where it has just been
    _ATP_SWITCH_LINES = {
        "forced": [
            _("Wait! It was in my ass! Put a condom on if you want to switch!"),
            _("Hold on! You can't go from my ass to my pussy raw! Condom, NOW!"),
            _("Stop! That was in my butt! You need a condom first!"),
        ],
        "cute_sex": [
            _("It was in my butt... you need to put a condom on first, okay?"),
            _("I-I'll let you switch, but please put a condom on... it was in my..."),
        ],
        "_default": [
            _("You know where that's been. Put a condom on first."),
            _("If you want to switch, fine, but you're wearing a condom. It was in my ass."),
        ],
    }

    def _atp_switch_line(girl, forced=False):
        _key = "forced" if forced else ("cute_sex" if girl.has_trait("cute_sex") else "_default")
        return _tl(renpy.random.choice(_ATP_SWITCH_LINES[_key]))

    # Position pieces the gate needs to pause / resume / end the running scene (add new anal poses here)
    _SWITCH_GATE_CORE = {
        "doggy":       {"started": "doggy_started", "speed": "doggy_speed", "apply": "DG_ApplySpeed", "end": "DG_End"},
        "full_nelson": {"started": "fn_started",    "speed": "fn_speed",    "apply": "FN_ApplySpeed", "end": "FN_End"},
        "laying_down": {"started": "laying_started", "speed": "laying_speed", "apply": "LD_ApplySpeed", "end": "LD_End"},
        "reverse_cowgirl": {"started": "rcg_started", "speed": "rcg_speed", "apply": "RCG_ApplySpeed", "end": "RCG_End"},
    }

label _switch_to_vaginal_gate(girl, position):
    python:
        store._switch_gate_ok = False
        store._switch_gate_scene_ended = False
        _sg_core = _SWITCH_GATE_CORE.get(position)
        print("[SWITCH_GATE] %s: anal %s -> vaginal-only position, checking" % (girl.gid, position))
    if _sg_core is None:
        $ print("[SWITCH_GATE] no _SWITCH_GATE_CORE entry for %s, letting the switch through" % position)
        $ store._switch_gate_ok = True
        return

    call _esc_ask_sex_from_anal(girl, position) from _call_sw_gate_ask
    python:
        _sg_accepted = (store._esc_result == "accepted")
        _sg_atp = (store._esc_atp_result or {}).get("outcome", "accept_raw")
        # This was not an escalation: leave nothing behind for the escalation handlers
        store._esc_result = None
        store._esc_target = None
    if not _sg_accepted:
        $ print("[SWITCH_GATE] %s refused the switch, scene goes on in %s" % (girl.gid, position))
        return

    python:
        _sg_cheat = _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False)
        _sg_need_condom = (_sg_atp == "require_condom") or _sg_cheat
    if _sg_need_condom:
        if _sg_atp == "require_condom":
            $ Say_Line(girl, _atp_switch_line(girl))
        # Pause the running scene while the condom goes on
        python:
            _sg_speed = getattr(store, _sg_core["speed"], 0)
            _sg_started = getattr(store, _sg_core["started"], False)
            setattr(store, _sg_core["started"], False)
        call expression _sg_core["apply"] pass (girl, 0) from _call_sw_gate_pause
        call condom_check(girl, True, "hard_deny") from _call_sw_gate_condom
        $ setattr(store, _sg_core["started"], _sg_started)
        if store.condom_denied:
            if _sg_atp != "require_condom":
                # Cheat path: no condom, no sex. Same breakdown as the hole switch.
                $ print("[SWITCH_GATE] %s cheat path, condom refused -> breakdown" % girl.gid)
                call expression _sg_core["end"] pass (girl, dress_up=False) from _call_sw_gate_end
                call _cheat_no_condom_breakdown(girl) from _call_sw_gate_breakdown
                $ store._switch_gate_scene_ended = True
                return
            $ print("[SWITCH_GATE] %s condom refused, scene goes on in %s" % (girl.gid, position))
            call expression _sg_core["apply"] pass (girl, _sg_speed) from _call_sw_gate_resume
            return

    if _is_on_cheat_path(girl) and _cheat_stage(girl) < 3:
        $ Say_Line(girl, _cheat_sex_first_line(girl))
    python:
        store._switch_gate_ok = True
        print("[SWITCH_GATE] %s accepted (atp=%s condom=%s)" % (girl.gid, _sg_atp, store.condom_active))
    return
