# ============================================================
# CONDOM BREAKING SYSTEM
# Pre-rolls break chance at scene start. When it fires:
#   - Player sees it break, chooses: tell her or hide it
#   - Hidden: discovery check at position change or cum time
# ============================================================

default _condom_break_will_happen = False
default _condom_break_tick = 0
default _condom_broken = False
default _condom_broken_hidden = False
default _condom_broken_told = False
default _condom_type = "condom"
default _condom_break_ntr_level = None     # partner's NTR boundary level when the condom tore (None = no snapshot: helpers read the live level)
default _condom_break_partner_saw = None   # None / "silent" (watching NTR partner noticed the HIDDEN break, she has not) / "spoken" (he reacted out loud)
default _condom_break_notice_looks = 0     # notice rolls the watching partner already had on this break

init python:

    # ── Config ──

    CONDOM_BREAK_CHANCE = {
        "condom": 0.05,
        "japanese_condom": 0.50,
    }

    CONDOM_BREAK_DISCOVERY = {
        "fire_away": 0.70,
        "outside": 0.70,
        "condom": 1.0,
    }

    CONDOM_BREAK_REACTIONS = {
        "cum_slut":     {"Love": 5,    "Obed": 15,  "Inbt": 20},
        "hate_cum":     {"Love": -50,  "Obed": 30,  "Inbt": 25},
        "hardcore_sex": {"Love": -5,   "Obed": 10,  "Inbt": 15},
        "cute_sex":     {"Love": -25,  "Obed": 20,  "Inbt": 15},
        "_default":     {"Love": -15,  "Obed": 15,  "Inbt": 15},
    }

    CONDOM_BREAK_EXCUSE_MODS = {
        "didnt_notice":    {"Love": 0.5,  "Obed": 0.5,  "Inbt": 0.5},
        "felt_too_good":   {"Love": 1.0,  "Obed": 1.5,  "Inbt": 1.5},
        "moaned_louder":   {"Love": 1.5,  "Obed": 2.0,  "Inbt": 2.0},
    }

    # ── Dialogue pools ──

    _CBREAK_TOLD_LINES = {
        "cum_slut": [
            _("It broke? Oh well... want to just keep going without it?"),
            _("The condom broke? Honestly... I don't mind at all."),
            _("Broke? Good riddance. Now I can actually feel you."),
        ],
        "hate_cum": [
            _("WHAT?! The condom BROKE?! Oh no, no, no..."),
            _("It BROKE?! Please tell me you're joking! This can't be happening!"),
            _("The condom is BROKEN?! We need to stop! RIGHT NOW!"),
        ],
        "hardcore_sex": [
            _("It broke? Huh. Well, shit happens. What do you want to do?"),
            _("Broke? Whatever. Are we stopping or going raw?"),
            _("The condom tore? Honestly, I don't really care. Your call."),
        ],
        "cute_sex": [
            _("It broke?! Oh no... what do we do now?"),
            _("The condom broke? That's... scary. What should we do?"),
            _("Oh no... it tore? I... I don't know what to say..."),
        ],
        "_default": [
            _("What?! It broke?! Are you serious?!"),
            _("The condom broke? Oh god... that's not good."),
            _("It tore? Seriously? Ugh... now what?"),
        ],
    }

    _CBREAK_ACCEPT_RAW_LINES = {
        "cum_slut": [
            _("Finally! I hated that thing anyway. Now give it to me raw!"),
            _("Yes! Raw! That's so much better... don't stop!"),
        ],
        # still discovering it (trait_is_new, read through trait_pool_key): she wants it, no grudge against condoms yet
        "cum_slut_new": [
            _("Keep going... without it. I want to feel it."),
            _("It broke? ...Then don't stop. I want this."),
        ],
        "hardcore_sex": [
            _("Whatever. Just don't stop. Keep going."),
            _("Fine, raw it is. Now fuck me harder."),
        ],
        "_default": [
            _("Okay... just be careful. Please."),
            _("Fine... but you better pull out when you're close."),
            _("Alright... just... don't finish inside. Promise me."),
        ],
    }

    _CBREAK_DENY_LINES = {
        "hate_cum": [
            _("ABSOLUTELY NOT! We stop right now! I'm not risking it!"),
            _("No! We're done! I refuse to continue without protection!"),
        ],
        "_default": [
            _("No. We're done. I'm not doing this without protection."),
            _("I can't... not without a condom. We need to stop."),
            _("No way. I'm not comfortable continuing like this."),
        ],
    }

    _CBREAK_DISCOVER_LINES = {
        "cum_slut": [
            _("Wait... the condom is broken? Well, that explains why it felt so much better..."),
            _("Oh! It broke! I was wondering why it suddenly felt amazing..."),
        ],
        "hate_cum": [
            _("THE CONDOM BROKE?! And you didn't TELL me?! Are you INSANE?!"),
            _("It's BROKEN?! This whole time?! How could you do this to me?!"),
        ],
        "hardcore_sex": [
            _("The condom broke? And you kept going? Huh... bold move."),
            _("Wait, it's torn? I didn't even notice. Whatever."),
        ],
        "cute_sex": [
            _("The condom broke?! Why didn't you TELL me?! I trusted you!"),
            _("It's broken?! How long has it been like that?! That's so unfair..."),
        ],
        "_default": [
            _("Wait... is that... is the condom broken?!"),
            _("Oh my god... the condom... it broke! And you didn't say anything?!"),
            _("What the... the condom is torn! You KNEW about this?!"),
        ],
    }

    _CBREAK_EXCUSE_LINES = {
        "didnt_notice": {
            "cum_slut": [
                _("Sure you didn't... well, what's done is done. I'm not complaining."),
                _("You 'didn't notice'? Right. Well, I'm glad it broke, honestly."),
            ],
            "hate_cum": [
                _("You DIDN'T NOTICE?! That's the worst excuse I've ever heard!"),
                _("How do you NOT notice?! You're either lying or completely irresponsible!"),
            ],
            "hardcore_sex": [
                _("Yeah, sure. Whatever, it's done now. No point crying about it."),
                _("Didn't notice? I doubt that, but I don't really care."),
            ],
            "cute_sex": [
                _("You really didn't notice? I... I want to believe you..."),
                _("How could you not feel it? That's... I don't know what to think."),
            ],
            "_default": [
                _("You didn't notice?! How do you not notice something like that?!"),
                _("Seriously? You didn't feel the difference? I find that hard to believe."),
            ],
        },
        "felt_too_good": {
            "cum_slut": [
                _("I mean... I can't blame you. It did feel incredible without it..."),
                _("Honestly? Same. It felt way too good to stop."),
            ],
            "hate_cum": [
                _("You KNEW and kept going?! Because it FELT GOOD?! You selfish pig!"),
                _("So your pleasure was more important than my safety?! Unbelievable!"),
            ],
            "hardcore_sex": [
                _("At least you're honest about it. Can't say I'd have done different."),
                _("Fair enough. It did feel better. But next time, tell me."),
            ],
            "cute_sex": [
                _("You... you chose how it felt over my trust? That really hurts..."),
                _("So feeling good mattered more than being honest with me? That's really sad."),
            ],
            "_default": [
                _("So you KNEW and kept going?! That's so selfish!"),
                _("You felt it break and decided your pleasure was more important?! Wow."),
            ],
        },
        "moaned_louder": {
            "cum_slut": [
                _("I... okay, maybe I did moan louder. But still! You should have said something!"),
                _("Ugh, fine, you're right... it felt amazing. But don't think that excuses you!"),
            ],
            "hardcore_sex": [
                _("...Okay, maybe I did. But that's beside the point!"),
                _("Tch... fine, you noticed that. Doesn't make it okay though."),
            ],
            "cute_sex": [
                _("That's... so mean! Don't use my reactions against me!"),
                _("How dare you turn this around on me! I was just caught up in the moment!"),
            ],
            "_default": [
                _("Don't turn this around on ME! You should have told me!"),
                _("That doesn't make it okay! You still hid it from me!"),
            ],
        },
    }

    _CBREAK_CREAMPIE_LINES = {
        "cum_slut": [
            _("Wait... you came inside me? The condom was broken and you... oh god, that's so hot."),
            _("You came in me?! Through the broken condom?! ...I loved every second of it."),
        ],
        "hate_cum": [
            _("You came INSIDE me?! Through a BROKEN condom?! I can feel it! Oh god, NO!"),
            _("Is that... did you... YOU CAME INSIDE ME?! The condom was BROKEN!"),
        ],
        "hardcore_sex": [
            _("Wait, you came inside? The condom was broken? ...Heh. That's pretty messed up."),
            _("So you creampied me through a broken condom. That's honestly kind of hot."),
        ],
        "cute_sex": [
            _("You came inside me? And the condom was broken? I can't believe you did that..."),
            _("I can feel it... you came inside through the broken condom... how could you?"),
        ],
        "_default": [
            _("Wait... the condom was broken and you came inside?! Are you kidding me?!"),
            _("You came in me! The condom was torn! Do you have any idea what you just did?!"),
        ],
    }

    _CBREAK_CUM_EXPRESSIONS = {
        "cum_slut": "lewd",
        "hate_cum": "angry",
        "hardcore_sex": "pleasure",
        "cute_sex": "scared",
        "_default": "surprised",
    }

    _CBREAK_CREAM_BELIEVED_LINES = {
        "cum_slut": [
            _("Honestly? I'm glad it happened. Don't worry about it."),
            _("Accidents happen... and this was a happy one, honestly."),
        ],
        "hardcore_sex": [
            _("Fine, whatever. Accidents happen. Just be more careful next time."),
            _("Alright, I believe you. Shit happens. Let's just keep going."),
        ],
        "cute_sex": [
            _("I... okay. I believe you. Just please be more careful, okay?"),
            _("It's scary but... I trust you. Just promise you'll check next time."),
        ],
        "hate_cum": [
            _("...Fine. I'll believe you this time. But if this EVER happens again..."),
            _("You better be telling the truth. I swear, if you're lying to me..."),
        ],
        "_default": [
            _("...Okay. I guess it could happen to anyone. Just... ugh."),
            _("Fine, I'll give you the benefit of the doubt. But you owe me."),
        ],
    }

    _CBREAK_CREAM_ANGRY_END_LINES = {
        "hate_cum": [
            _("You came inside me with a broken condom and you KNEW?! We're DONE here!"),
            _("I can feel your cum in me... and you did this on PURPOSE?! GET OUT!"),
        ],
        "cute_sex": [
            _("I trusted you and you did THIS to me? I can't even look at you right now."),
            _("How could you? I... I need to leave. Don't follow me."),
        ],
        "_default": [
            _("You knew the condom was broken and you came inside me anyway?! Unbelievable."),
            _("I'm done. You knew what you were doing. Don't talk to me."),
        ],
    }

    # Narration after outcome — gives player context
    _CBREAK_CREAM_NARR_BELIEVED = {
        "cum_slut": [
            _("She barely seems bothered. If anything, she looks pleased about it."),
            _("She doesn't care at all. You just keep going."),
        ],
        "hardcore_sex": [
            _("She rolls her eyes but clearly doesn't want to stop."),
            _("She shrugs it off. Doesn't seem like a big deal to her."),
        ],
        "cute_sex": [
            _("She looks worried, but seems to trust your explanation. You continue."),
            _("She takes a deep breath and nods. She believes you."),
        ],
        "hate_cum": [
            _("She's still visibly upset, but accepts it was an accident. For now."),
            _("She glares at you, but doesn't stop. You got lucky."),
        ],
        "_default": [
            _("She seems annoyed, but accepts it and doesn't want to stop."),
            _("She sighs and moves on. Clearly not happy, but not angry enough to stop."),
        ],
    }

    _CBREAK_CREAM_NARR_ANGRY_CONT = {
        "cum_slut": [
            _("She doesn't really seem to mind. You just keep going as if nothing happened."),
        ],
        "hardcore_sex": [
            _("She looks pissed, but clearly doesn't want to stop either."),
            _("She's annoyed, but the mood hasn't killed it for her."),
        ],
    }

    _CBREAK_CREAM_NARR_END_HERROOM = [
        _("She's furious. She kicks you out of her room without another word."),
        _("She points at the door, shaking with anger. You're out."),
    ]

    _CBREAK_CREAM_NARR_END_ELSEWHERE = [
        _("She grabs her things and storms off without looking back."),
        _("She's done. She gets up and leaves before you can say anything else."),
    ]

    # ── Functions ──

    # The condom she has on right now: every store var of the break system, with its "fresh condom" value.
    # condom_break_reset() writes these. A position switch carries them over (condom_carry_save / _restore).
    _CONDOM_BREAK_STATE = (
        ("_condom_break_will_happen", False),
        ("_condom_break_tick", 0),
        ("_condom_broken", False),
        ("_condom_broken_hidden", False),
        ("_condom_broken_told", False),
        ("_condom_type", "condom"),
        ("_condom_break_ntr_level", None),
        ("_condom_break_partner_saw", None),
        ("_condom_break_notice_looks", 0),
    )
    _CONDOM_CARRY_VARS = ("condom_active", "_stealth_condom_removed") + tuple(_cb_var for _cb_var, _cb_def in _CONDOM_BREAK_STATE)

    def condom_break_reset():
        for _cb_var, _cb_def in _CONDOM_BREAK_STATE:
            setattr(store, _cb_var, _cb_def)
        print("[CONDOM_BREAK] state reset")

    def condom_carry_save():
        """The condom she has on, taken right before a position switch ends the old pose. The old pose's End
        (scene_full_cleanup) resets all of it: the new pose used to get condom_active back but a condom that
        was never rolled (a Japanese condom could no longer tear) and forgot a stealth removal."""
        return dict((_cv, getattr(store, _cv, None)) for _cv in _CONDOM_CARRY_VARS)

    def condom_carry_restore(snap):
        for _cv, _val in snap.items():
            setattr(store, _cv, _val)
        print("[CONDOM_BREAK] carried over the position switch: active=%s type=%s will_break=%s tick=%s broken=%s stealth=%s" % (
            store.condom_active, store._condom_type, store._condom_break_will_happen, store._condom_break_tick,
            store._condom_broken, store._stealth_condom_removed))

    def condom_break_preroll(girl=None):
        ctype = getattr(store, "_condom_type", "condom")
        # her step locks going raw (story_steps.rpy "raw"): her condom never tears (a tear he hides = raw sex)
        if girl is not None and story_act_locked(girl, "raw"):
            store._condom_break_will_happen = False
            store._condom_break_tick = 0
            print("[CONDOM_BREAK] preroll: %s's step %d locks raw, no break" % (girl.gid, story_step(girl)))
            return
        if girl and _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False):
            print("[CONDOM_BREAK] cheat path active - break allowed")
        chance = CONDOM_BREAK_CHANCE.get(ctype, 0.05)
        roll = renpy.random.random()
        store._condom_break_will_happen = (roll < chance)
        if store._condom_break_will_happen:
            store._condom_break_tick = renpy.random.randint(3, 8)
        else:
            store._condom_break_tick = 0
        print("[CONDOM_BREAK] preroll: type=%s chance=%.2f roll=%.4f will_break=%s tick=%d" % (ctype, chance, roll, store._condom_break_will_happen, store._condom_break_tick))

    def condom_break_tick():
        if not store._condom_break_will_happen or store._condom_broken:
            return False
        store._condom_break_tick -= 1
        if store._condom_break_tick <= 0:
            print("[CONDOM_BREAK] BREAK fires this tick")
            return True
        print("[CONDOM_BREAK] tick: %d remaining" % store._condom_break_tick)
        return False

    def _condom_break_snapshot_ntr_level(girl):
        """Freeze her NTR partner's boundary level at the moment the condom tears (0 = no NTR-active partner).
        A watching partner who silently notices a HIDDEN break levels up 2 -> 3 on the spot, but SHE only knows
        the rule that was in force when it tore: her level-2 pools must still fire when she finds out."""
        _npc = get_npc_partner_for(girl) if (hasattr(girl, "has_npc_partner") and girl.has_npc_partner()) else None
        if _npc is not None and getattr(_npc, "_ntr_active", False):
            store._condom_break_ntr_level = getattr(_npc, "_ntr_boundary_level", 1)
        else:
            store._condom_break_ntr_level = 0
        print("[CONDOM_BREAK] NTR level snapshot: girl=%s level=%s" % (girl.gid, store._condom_break_ntr_level))

    def _condom_break_ntr_condom_rule(girl):
        """True when the condom was her partner's RULE for this break: NTR arrangement known
        (_ntr_active_discovered: she can only quote a rule she knows) and boundary level 2 WHEN IT TORE.
        Single source for CondomBreakTold / CondomBreakDiscovery / CondomBreakCumMenu. No snapshot (save made
        mid-scene by an older build, QA harness calling the labels directly) = live level."""
        if not _ntr_active_discovered(girl):
            return False
        _level = getattr(store, "_condom_break_ntr_level", None)
        _src = "snapshot"
        if _level is None:
            _level = getattr(get_npc_partner_for(girl), "_ntr_boundary_level", 1)
            _src = "live"
        print("[CONDOM_BREAK] NTR condom rule: girl=%s level=%s (%s) partner_saw=%s" % (
            girl.gid, _level, _src, getattr(store, "_condom_break_partner_saw", None)))
        return _level == 2

    def _condom_break_trait_key(girl):
        for t in ("cum_slut", "hate_cum", "hardcore_sex", "cute_sex"):
            if girl.has_trait(t):
                return t
        return "_default"

    def _condom_break_apply_stats(girl, excuse_key=None):
        tk = _condom_break_trait_key(girl)
        base = CONDOM_BREAK_REACTIONS.get(tk, CONDOM_BREAK_REACTIONS["_default"])
        excuse_mod = CONDOM_BREAK_EXCUSE_MODS.get(excuse_key, {}) if excuse_key else {}
        for stat, amount in base.items():
            mult = excuse_mod.get(stat, 1.0)
            final = int(amount * mult)
            if final != 0:
                Change_Status(girl, stat, final)
        if girl.has_npc_partner():
            Change_Status(girl, "Love", -15)
        print("[CONDOM_BREAK] stats applied: trait=%s excuse=%s bf=%s" % (tk, excuse_key, girl.has_npc_partner()))

    def _condom_break_discovery_roll(cum_type):
        chance = CONDOM_BREAK_DISCOVERY.get(cum_type, 0.70)
        roll = renpy.random.random()
        result = roll < chance
        print("[CONDOM_BREAK] discovery roll: cum_type=%s chance=%.2f roll=%.4f discovered=%s" % (cum_type, chance, roll, result))
        return result

    def _condom_break_belief_check(girl):
        """Can she believe the player genuinely didn't notice the break?"""
        tk = _condom_break_trait_key(girl)
        if tk == "cum_slut":
            return True
        if tk == "hardcore_sex":
            return girl.Love >= 200
        if tk == "cute_sex":
            return girl.Love >= 300
        if tk == "hate_cum":
            return girl.Love >= 700
        return girl.Love >= 450

    def _condom_break_cream_ends_scene(girl, excuse):
        """Check if broken condom creampie should end the scene (angry exit)."""
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

    # ── Cheat path condom break ──

    def _condom_break_is_cheat(girl):
        return bool(girl and _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False))

    def _condom_break_cheat_path(girl):
        return getattr(girl, "_cheat_escalation_path", 0) if _condom_break_is_cheat(girl) else 0

    CONDOM_BREAK_CHEAT_STATS = {
        "told_accept":  {"Love": -10, "Obed": 15, "Inbt": 10, "heat": 30, "bf_loyalty": -30},
        "told_deny":    {"Love": -15, "Obed": 5,  "Inbt": 10, "heat": 20, "bf_loyalty": 5},
        "hidden_disc":  {"Love": -25, "Obed": 20, "Inbt": 15, "heat": 25, "bf_loyalty": -20},
        "hidden_cream": {"Love": -40, "Obed": 25, "Inbt": 20, "heat": 40, "bf_loyalty": -50},
    }

    def _condom_break_apply_cheat_stats(girl, scenario):
        entry = CONDOM_BREAK_CHEAT_STATS.get(scenario)
        if not entry:
            return
        for stat in ("Love", "Obed", "Inbt"):
            val = entry.get(stat, 0)
            if val:
                Change_Status(girl, stat, val)
        heat = entry.get("heat", 0)
        if heat > 0:
            _add_cheat_heat(girl, heat, "condom_break_%s" % scenario)
        bf_loy = entry.get("bf_loyalty", 0)
        if bf_loy and hasattr(girl, "change_bf_loyalty"):
            girl.change_bf_loyalty(bf_loy)
        print("[CONDOM_BREAK] cheat stats applied: scenario=%s heat=%d bf_loy=%d" % (scenario, heat, bf_loy))

    # ── Cheat path dialogue pools ──

    _CBREAK_CHEAT_TOLD_LINES = {
        1: [
            _("The condom BROKE?! No... no no no... that was the only thing making this okay! Without it, this is... this is real cheating!"),
            _("It broke?! Oh god... the condom was the only reason I could tell myself this wasn't... that I wasn't really betraying %(pl)s..."),
            _("WHAT?! No! The condom was... it was my last... I can't do this without protection! This changes EVERYTHING!"),
        ],
        2: [
            _("The condom broke? That was... I was supposed to be in control of this. The condom was part of that. And now it's gone?"),
            _("It broke?! I set the rules. Condom was rule number ONE. And now you're telling me it just... failed?"),
            _("No... the condom was my safety net. I was managing this, keeping it contained. Without it, I'm just... cheating."),
        ],
        3: [
            _("It broke? Great. Just great. This was supposed to be controlled revenge, not a complete disaster."),
            _("The condom broke?! I was getting back at %(pl)s, not... not going THIS far. This wasn't the plan."),
            _("Are you serious?! The condom was the one line I wasn't going to cross! This was supposed to stay... manageable!"),
        ],
    }

    _CBREAK_CHEAT_ACCEPT_LINES = {
        1: [
            _("I... the condom is already gone. And we're already... maybe I've been lying to myself this whole time. The condom was just an excuse..."),
            _("...It doesn't matter anymore, does it? With or without a condom, I'm still here, doing this behind %(poss)s back. Just... keep going."),
        ],
        2: [
            _("...Fine. The condom is gone and I... I don't want to stop. Maybe I never really cared about the condom. Maybe I just needed the excuse."),
            _("You know what? I'm done pretending the condom made this okay. I wanted this. I want this. Don't stop."),
        ],
        3: [
            _("Whatever. The condom was just a formality anyway. If I'm doing this to get back at %(pl)s, might as well go all the way."),
            _("Fine. No condom. Complete betrayal. %(Pp)s earned every second of this."),
        ],
    }

    _CBREAK_CHEAT_DENY_LINES = {
        1: [
            _("No! Without the condom, this is REAL! I can't... I CAN'T do this! We need to stop right now!"),
            _("I can't keep going without protection! The condom was the only thing keeping me from completely betraying %(pl)s! We're done!"),
        ],
        2: [
            _("No! I set the rules and the condom was the most important one! Without it, I have no control! We stop NOW!"),
            _("Absolutely not! Without the condom, this goes from something I control to something that controls ME! It's over!"),
        ],
        3: [
            _("No! This was supposed to be controlled revenge, not... THIS! Without a condom, this crosses a line I'm not ready to cross!"),
            _("Stop! I wanted to get back at %(pl)s, not destroy everything! No condom means this went too far!"),
        ],
    }

    _CBREAK_CHEAT_DISCOVER_LINES = {
        1: [
            _("The condom was BROKEN?! This whole time?! I was cheating for REAL and I didn't even KNOW?! How could you not tell me?!"),
            _("It's been broken?! Oh god, oh god... I told myself the condom made it okay... and it wasn't even THERE?! You let me believe..."),
        ],
        2: [
            _("You KNEW the condom was gone and you let me keep going?! I thought I was in control! I was NEVER in control!"),
            _("The condom broke and you said NOTHING?! I was making rules, setting boundaries... and none of it mattered because YOU decided to hide this!"),
        ],
        3: [
            _("The condom broke and you didn't say anything?! My revenge plan just became something MUCH worse! You had no right to decide that for me!"),
            _("So the condom was gone this entire time?! I was trying to keep this contained and you just... let me cross a line I didn't agree to?!"),
        ],
    }

    _CBREAK_CHEAT_CREAM_LINES = {
        1: [
            _("You came INSIDE me?! Through a BROKEN condom?! %(pl)s... oh god, oh GOD... what have I done?! What have YOU done to me?!"),
            _("No... no no NO! You came in me?! Raw?! I was telling myself the condom made it okay and you... you came INSIDE me while cheating on %(pl)s!"),
        ],
        2: [
            _("You came inside me raw... while I thought I was in control... I was NEVER in control. Not even for a second. Oh god... %(pl)s..."),
            _("You CAME in me?! Through the broken condom?! I set the rules! CONDOM was rule number one! And you just... inside me... behind %(poss)s back..."),
        ],
        3: [
            _("You came inside me... raw... while I was cheating on %(pl)s... this went so much further than revenge. This is... this is something else entirely."),
            _("Inside me?! RAW?! I wanted to hurt %(pl)s, not... not THIS! You came inside me with no protection while I'm with someone else! That's..."),
        ],
    }

    _CBREAK_CHEAT_EXCUSE_LINES = {
        "didnt_notice": {
            1: [
                _("You didn't NOTICE?! How do you not notice the condom breaking while you're inside someone who's CHEATING for you?!"),
                _("You didn't feel it?! I don't... I can't even think right now. %(pl)s is going to... no. I can't."),
            ],
            2: [
                _("You didn't notice?! YOU didn't notice but somehow I'm the one who's supposed to be in control of this situation?!"),
                _("How convenient. The condom broke and you just... didn't feel the difference. While I was trusting you to follow MY rules."),
            ],
            3: [
                _("You didn't notice? Really? Fine. It doesn't change the fact that my 'revenge' just became a full-blown affair."),
                _("'Didn't notice'... whether you did or not, the damage is done. This stopped being revenge a long time ago."),
            ],
        },
        "felt_too_good": {
            1: [
                _("It felt too GOOD?! So your pleasure was more important than the ONE thing that let me pretend I wasn't destroying my relationship?!"),
                _("You KNEW and you didn't stop because it FELT GOOD?! I'm betraying %(pl)s and you just... used that for your own pleasure?!"),
            ],
            2: [
                _("So you knew and kept going because it felt good? MY rules. MY control. And you threw it all away because it felt NICE?!"),
                _("It felt good, so you just decided MY boundaries didn't matter? I was supposed to be the one in charge!"),
            ],
            3: [
                _("It felt good? Of course it did. You got to have me raw while I'm getting back at %(pl)s. Must have been your lucky day."),
                _("So you just enjoyed it. While I thought I was in control of my own revenge. Great. Just great."),
            ],
        },
        "moaned_louder": {
            1: [
                _("Don't you DARE turn this on me! I'm cheating on %(pl)s and you're using my body against me?! That's so cruel!"),
                _("How dare you! My reactions don't give you permission to HIDE the condom breaking while I'm betraying someone I care about!"),
            ],
            2: [
                _("Oh, so because I moaned louder, YOU get to decide to break MY rules?! My body's reaction is not your permission slip!"),
                _("Don't try to make this MY fault! I was enjoying something I was CONTROLLING! You took that away from me!"),
            ],
            3: [
                _("So because I was into it, you figured you could get away with it? This was MY revenge, MY terms. Not yours to exploit!"),
                _("Don't blame me for enjoying something I was doing ON PURPOSE! The condom breaking isn't something I asked for!"),
            ],
        },
    }

    _CBREAK_CHEAT_NARR_END = {
        1: [
            _("She breaks down. The guilt overwhelms her completely. She can barely dress herself."),
            _("She's shaking. The realization of what happened, without any excuse left, destroys her."),
        ],
        2: [
            _("Her carefully maintained control shatters. She goes silent, mechanically gathering her clothes."),
            _("The illusion of control is gone. She stares at nothing for a moment, then starts getting dressed."),
        ],
        3: [
            _("The revenge went further than she planned. She sits there, processing, before quietly leaving."),
            _("She realizes this stopped being about getting back at anyone a long time ago. She leaves without a word."),
        ],
    }


# ============================================================
# CONDOM TYPE SELECTION
# Called wherever a condom is applied. Handles type sub-menu,
# item removal, activation, and break preroll.
# ============================================================
label _apply_condom(girl):
    $ condom_break_reset()
    $ stealth_condom_reset()
    python:
        _ac_has_reg = Player.has_item("condom")
        _ac_has_jp = Player.has_item("japanese_condom")
    if _ac_has_reg and _ac_has_jp:
        $ _ac_reg_count = Player.get_item_count("condom")
        $ _ac_jp_count = Player.get_item_count("japanese_condom")
        menu:
            "Regular condom (x[_ac_reg_count])":
                $ Player.remove_item("condom")
                $ store._condom_type = "condom"
            "Japanese condom (x[_ac_jp_count])":
                $ Player.remove_item("japanese_condom")
                $ store._condom_type = "japanese_condom"
    elif _ac_has_reg:
        $ Player.remove_item("condom")
        $ store._condom_type = "condom"
    else:
        $ Player.remove_item("japanese_condom")
        $ store._condom_type = "japanese_condom"
    $ store.condom_active = True
    $ condom_break_preroll(girl)
    return


# ============================================================
# MAIN BREAK EVENT
# ============================================================
label CondomBreakEvent(girl, position):
    $ store._condom_broken = True
    $ _condom_break_snapshot_ntr_level(girl)   # what SHE knows about his rule, frozen at the tear
    $ unlock_achievement("oops_it_broke")
    call _sst_apply_speed_dispatch(girl, position) from _call_sst_apply_cbreak_visual

    python:
        _cbreak_narr = _tl(renpy.random.choice([
            _("You feel something give... the condom just tore."),
            _("A sudden warmth. You look down. The condom is broken."),
            _("You feel the condom rip. It's torn wide open."),
        ]))
    "[_cbreak_narr]"

    menu:
        "Tell her it broke":
            call CondomBreakTold(girl, position) from _call_CondomBreakTold_event
        "Don't say anything":
            $ store._condom_broken_hidden = True
            python:
                _cbreak_hide_narr = _tl(renpy.random.choice([
                    _("You decide to keep going without saying anything."),
                    _("You stay quiet and keep thrusting as if nothing happened."),
                    _("You pretend nothing happened and continue."),
                ]))
            "[_cbreak_hide_narr]"
    return


# ============================================================
# TOLD HER — player comes clean
# ============================================================
label CondomBreakTold(girl, position):
    $ store._condom_broken_told = True
    $ _cb_tk = _condom_break_trait_key(girl)

    # ── Cheat path branch ──
    if _condom_break_is_cheat(girl):
        $ _cb_cp = _condom_break_cheat_path(girl)
        $ print("[CONDOM_BREAK] told: cheat path %d" % _cb_cp)

        python:
            _cp_told_pool = _CBREAK_CHEAT_TOLD_LINES.get(_cb_cp, _CBREAK_CHEAT_TOLD_LINES[1])
        $ set_scene_expression(girl, "scared")
        $ Say_Line(girl, _format_partner_line(girl, _tl(renpy.random.choice(_cp_told_pool))))

        $ _cb_check = CumPermissionCheck(girl, "condom_break_accept")
        $ print("[CONDOM_BREAK] told cheat: check=%s" % _cb_check)

        if _cb_check["accepted"]:
            python:
                _cp_acc_pool = _CBREAK_CHEAT_ACCEPT_LINES.get(_cb_cp, _CBREAK_CHEAT_ACCEPT_LINES[1])
            $ set_scene_expression(girl, "sad")
            $ Say_Line(girl, _format_partner_line(girl, _tl(renpy.random.choice(_cp_acc_pool))))
            $ girl._cheat_broke = True
            $ girl.discover("discovered_trait_cheater") if girl.has_trait("cheater") else None
            $ unlock_achievement("broken_by_accident")
            $ _on_condom_removed(girl, skip_hide=True)
            $ _condom_break_apply_cheat_stats(girl, "told_accept")
            call _sex_scene_condom_rip_visual(girl, position) from _call_sst_condom_rip_cbreak_cheat
        else:
            python:
                _cp_deny_pool = _CBREAK_CHEAT_DENY_LINES.get(_cb_cp, _CBREAK_CHEAT_DENY_LINES[1])
            $ set_scene_expression(girl, "scared")
            $ Say_Line(girl, _format_partner_line(girl, _tl(renpy.random.choice(_cp_deny_pool))))
            $ _condom_break_apply_cheat_stats(girl, "told_deny")
            $ store._sst_result = "abort"
            $ store._sst_abort_reason = "condom_break_cheat_deny"
        return

    # ── Standard trait-based flow ──
    python:
        _told_pool = _CBREAK_TOLD_LINES.get(_cb_tk, _CBREAK_TOLD_LINES["_default"])
    $ Say_Line(girl, _tl(renpy.random.choice(_told_pool)))

    # NTR extra reaction when the condom was the partner's rule (boundary level 2 when it tore)
    python:
        _cbreak_ntr_gate = _condom_break_ntr_condom_rule(girl)
        _cbreak_ntr_check = _ntr_girl_boundary_check(girl, "raw_sex") if _cbreak_ntr_gate else None
        if _cbreak_ntr_gate:
            print("[CONDOM_BREAK] NTR gate: condom rule active, result=%s" % _cbreak_ntr_check["outcome"])

    if _cbreak_ntr_gate and _cbreak_ntr_check:
        if _cbreak_ntr_check["outcome"] in ("respect", "guilty_allow"):
            $ _ntr_say_boundary_line(girl, _NTR_GIRL_CBREAK_PANIC)
        else:
            $ _ntr_say_boundary_line(girl, _NTR_GIRL_CBREAK_EXCITED)

    $ _cb_check = CumPermissionCheck(girl, "condom_break_accept")
    $ print("[CONDOM_BREAK] told: check=%s" % _cb_check)

    if _cb_check["accepted"]:
        python:
            _accept_pool = _CBREAK_ACCEPT_RAW_LINES.get(trait_pool_key(girl, _cb_tk, _CBREAK_ACCEPT_RAW_LINES), _CBREAK_ACCEPT_RAW_LINES["_default"])
        $ Say_Line(girl, _tl(renpy.random.choice(_accept_pool)))
        $ _on_condom_removed(girl, skip_hide=True)
        call _sex_scene_condom_rip_visual(girl, position) from _call_sst_condom_rip_cbreak
    else:
        $ set_scene_expression(girl, "angry")
        python:
            _deny_pool = _CBREAK_DENY_LINES.get(_cb_tk, _CBREAK_DENY_LINES["_default"])
        $ Say_Line(girl, _tl(renpy.random.choice(_deny_pool)))
        $ Change_Status(girl, "Love", -10)
        $ store._sst_result = "abort"
        $ store._sst_abort_reason = "condom_break_denied"
    return


# ============================================================
# DISCOVERY — she finds the hidden break
# ============================================================
label CondomBreakDiscovery(girl, position):
    $ _cb_tk = _condom_break_trait_key(girl)
    $ set_scene_expression(girl, "startled")

    # ── Cheat path branch ──
    if _condom_break_is_cheat(girl):
        $ _cb_cp = _condom_break_cheat_path(girl)
        $ print("[CONDOM_BREAK] discovery: cheat path %d" % _cb_cp)

        python:
            _cp_disc_pool = _CBREAK_CHEAT_DISCOVER_LINES.get(_cb_cp, _CBREAK_CHEAT_DISCOVER_LINES[1])
        $ set_scene_expression(girl, "angry")
        $ Say_Line(girl, _format_partner_line(girl, _tl(renpy.random.choice(_cp_disc_pool))))

        $ _cb_is_hate_cum = girl.has_trait("hate_cum")
        menu:
            "I didn't notice it broke":
                $ _cb_excuse = "didnt_notice"
            "It felt too good to stop":
                $ _cb_excuse = "felt_too_good"
            "You moaned louder when it broke" if not _cb_is_hate_cum:
                $ _cb_excuse = "moaned_louder"

        python:
            _cp_exc_pool = _CBREAK_CHEAT_EXCUSE_LINES.get(_cb_excuse, {})
            _cp_exc_lines = _cp_exc_pool.get(_cb_cp, _cp_exc_pool.get(1, [_("I can't believe you.")]))
        $ Say_Line(girl, _format_partner_line(girl, _tl(renpy.random.choice(_cp_exc_lines))))

        $ _condom_break_apply_stats(girl, _cb_excuse)
        $ _condom_break_apply_cheat_stats(girl, "hidden_disc")

        if _cb_cp in (1, 2):
            $ store.condom_active = False
            $ store._condom_broken_hidden = False
            python:
                _cp_end_pool = _CBREAK_CHEAT_NARR_END.get(_cb_cp, _CBREAK_CHEAT_NARR_END[1])
            "[_tl(renpy.random.choice(_cp_end_pool))]"
            $ force_scene_reset(girl, angry_days=1, reason="condom_break_cheat_discovered")
            jump main_loop
        else:
            $ store.condom_active = False
            $ store._condom_broken_hidden = False
            $ set_scene_expression(girl, "angry")
            call _cum_dispatch_condom_remove(girl, position) from _call_condom_remove_cbreak_disc_cheat
        return

    # ── Standard flow ──

    # Check if NTR boundary level 2 context (condom was mandatory)
    python:
        _cbdisc_ntr = _condom_break_ntr_condom_rule(girl)   # snapshot: still True after he silently went to level 3
        _cb_ntr_tk = _cb_tk
        if _cbdisc_ntr and _cb_ntr_tk == "_default" and girl.has_trait("cheater"):
            _cb_ntr_tk = "cheater"
        print("[CONDOM_BREAK] discovery: ntr_context=%s trait=%s ntr_trait=%s" % (_cbdisc_ntr, _cb_tk, _cb_ntr_tk if _cbdisc_ntr else "n/a"))

    if _cbdisc_ntr:
        python:
            _ntr_disc_pool = _NTR_GIRL_CBREAK_HIDDEN_DISCOVER.get(_cb_ntr_tk, _NTR_GIRL_CBREAK_HIDDEN_DISCOVER["_default"])
            _ntr_disc_line = _format_partner_line(girl, _tl(renpy.random.choice(_ntr_disc_pool)))
        $ Say_Line(girl, _ntr_disc_line)
    else:
        python:
            _disc_pool = _CBREAK_DISCOVER_LINES.get(_cb_tk, _CBREAK_DISCOVER_LINES["_default"])
        $ Say_Line(girl, _tl(renpy.random.choice(_disc_pool)))

    $ _cb_is_hate_cum = girl.has_trait("hate_cum")
    menu:
        "I didn't notice it broke":
            $ _cb_excuse = "didnt_notice"
        "It felt too good to stop":
            $ _cb_excuse = "felt_too_good"
        "You moaned louder when it broke" if not _cb_is_hate_cum:
            $ _cb_excuse = "moaned_louder"

    if _cbdisc_ntr:
        python:
            _ntr_exc_pool = _NTR_GIRL_CBREAK_HIDDEN_EXCUSE.get(_cb_excuse, {})
            _ntr_exc_lines = _ntr_exc_pool.get(_cb_ntr_tk, _ntr_exc_pool.get("_default", [_("I can't believe you.")]))
            _ntr_exc_line = _format_partner_line(girl, _tl(renpy.random.choice(_ntr_exc_lines)))
        $ Say_Line(girl, _ntr_exc_line)
        python:
            if _cb_ntr_tk == "cheater":
                Change_Status(girl, "Love", -10)
                Change_Status(girl, "Inbt", 5)
                print("[CONDOM_BREAK] NTR cheater penalty (light): Love-10 Inbt+5")
            else:
                Change_Status(girl, "Love", -25)
                Change_Status(girl, "Obed", 20)
                Change_Status(girl, "Inbt", 15)
                print("[CONDOM_BREAK] NTR extra penalty: Love-25 Obed+20 Inbt+15")
    else:
        python:
            _excuse_pool = _CBREAK_EXCUSE_LINES.get(_cb_excuse, {})
            _excuse_lines = _excuse_pool.get(_cb_tk, _excuse_pool.get("_default", [_("I can't believe you.")]))
        $ Say_Line(girl, _tl(renpy.random.choice(_excuse_lines)))

    $ _condom_break_apply_stats(girl, _cb_excuse)
    $ _on_condom_removed(girl, skip_hide=True)
    call _cum_dispatch_condom_remove(girl, position) from _call_condom_remove_cbreak_disc
    $ store._condom_broken_hidden = False
    $ set_scene_expression(girl, "angry")
    return


# ============================================================
# CUM MENU — replaces normal condom cum menu when hidden break
# ============================================================
label CondomBreakCumMenu(girl, scene_type):

    menu:
        "Cum in the 'condom'":
            $ unlock_achievement("hidden_cream")
            call _cum_dispatch_anim(girl, scene_type) from _call_cum_anim_cbreak_condom
            python:
                _cbreak_cream_narr = _tl(renpy.random.choice([
                    _("You try to finish in the condom... but it's broken. You cum directly inside her."),
                    _("The condom is useless. Your cum flows right through the tear and fills her up."),
                ]))
            "[_cbreak_cream_narr]"
            $ process_cum(girl, scene_type, "inside")

            # ── Cheat path branch (creampie = always scene-ending) ──
            if _condom_break_is_cheat(girl):
                $ _cb_cp = _condom_break_cheat_path(girl)
                $ print("[CONDOM_BREAK] cum menu: cheat path %d" % _cb_cp)

                python:
                    _cp_cream_pool = _CBREAK_CHEAT_CREAM_LINES.get(_cb_cp, _CBREAK_CHEAT_CREAM_LINES[1])
                $ set_scene_expression(girl, "scared")
                $ Say_Line(girl, _format_partner_line(girl, _tl(renpy.random.choice(_cp_cream_pool))))

                $ _cb_is_hate_cum = girl.has_trait("hate_cum")
                menu:
                    "I didn't notice it broke":
                        $ _cb_excuse = "didnt_notice"
                    "It felt too good to stop":
                        $ _cb_excuse = "felt_too_good"
                    "You moaned louder when it broke" if not _cb_is_hate_cum:
                        $ _cb_excuse = "moaned_louder"

                $ store._witness_expression_lock = True
                python:
                    _cp_exc_pool = _CBREAK_CHEAT_EXCUSE_LINES.get(_cb_excuse, {})
                    _cp_exc_lines = _cp_exc_pool.get(_cb_cp, _cp_exc_pool.get(1, [_("I can't believe you.")]))
                $ Say_Line(girl, _format_partner_line(girl, _tl(renpy.random.choice(_cp_exc_lines))))

                $ _condom_break_apply_stats(girl, _cb_excuse)
                $ _condom_break_apply_cheat_stats(girl, "hidden_cream")
                $ store.condom_active = False
                $ store._condom_broken_hidden = False

                python:
                    _cp_end_pool = _CBREAK_CHEAT_NARR_END.get(_cb_cp, _CBREAK_CHEAT_NARR_END[1])
                "[_tl(renpy.random.choice(_cp_end_pool))]"
                $ store._witness_expression_lock = False
                if getattr(girl, '_ntr_violation_pending', False):
                    call _angry_end_ntr_confrontation(girl) from _call_aend_ntr_cbreak_cheat
                $ force_scene_reset(girl, angry_days=2, reason="condom_break_cheat_creampie")
                jump main_loop

            # ── Standard flow ──
            python:
                _cb_tk = _condom_break_trait_key(girl)
                _cream_pool = _CBREAK_CREAMPIE_LINES.get(_cb_tk, _CBREAK_CREAMPIE_LINES["_default"])
                _cb_expr = _CBREAK_CUM_EXPRESSIONS.get(_cb_tk, "surprised")
            $ set_scene_expression(girl, _cb_expr)
            $ Say_Line(girl, _tl(renpy.random.choice(_cream_pool)))

            $ _cb_is_hate_cum = girl.has_trait("hate_cum")
            menu:
                "I didn't notice it broke":
                    $ _cb_excuse = "didnt_notice"
                "It felt too good to stop":
                    $ _cb_excuse = "felt_too_good"
                "You moaned louder when it broke" if not _cb_is_hate_cum:
                    $ _cb_excuse = "moaned_louder"

            # NTR context check for harsher excuse reaction
            python:
                _cbcum_ntr = _condom_break_ntr_condom_rule(girl)
                _cb_ntr_tk = _cb_tk
                if _cbcum_ntr and _cb_ntr_tk == "_default" and girl.has_trait("cheater"):
                    _cb_ntr_tk = "cheater"

            if _cbcum_ntr:
                python:
                    _ntr_exc_pool = _NTR_GIRL_CBREAK_HIDDEN_EXCUSE.get(_cb_excuse, {})
                    _ntr_exc_lines = _ntr_exc_pool.get(_cb_ntr_tk, _ntr_exc_pool.get("_default", [_("I can't believe you.")]))
                    _ntr_exc_line = _format_partner_line(girl, _tl(renpy.random.choice(_ntr_exc_lines)))
                $ Say_Line(girl, _ntr_exc_line)
                python:
                    if _cb_ntr_tk == "cheater":
                        Change_Status(girl, "Love", -10)
                        Change_Status(girl, "Inbt", 5)
                        print("[CONDOM_BREAK] NTR cheater creampie penalty (light): Love-10 Inbt+5")
                    else:
                        Change_Status(girl, "Love", -25)
                        Change_Status(girl, "Obed", 20)
                        Change_Status(girl, "Inbt", 15)
                        print("[CONDOM_BREAK] NTR creampie extra penalty: Love-25 Obed+20 Inbt+15")
            else:
                python:
                    _excuse_pool = _CBREAK_EXCUSE_LINES.get(_cb_excuse, {})
                    _excuse_lines = _excuse_pool.get(_cb_tk, _excuse_pool.get("_default", [_("I can't believe you.")]))
                $ Say_Line(girl, _tl(renpy.random.choice(_excuse_lines)))

            # Belief check — only "didnt_notice" can be believed
            $ _cb_believed = (_cb_excuse == "didnt_notice" and _condom_break_belief_check(girl))
            $ print("[CONDOM_BREAK] cream excuse=%s believed=%s trait=%s Love=%d ntr=%s" % (_cb_excuse, _cb_believed, _cb_tk, girl.Love, _cbcum_ntr))

            if _cb_believed:
                $ _condom_break_apply_stats(girl, "didnt_notice")
                $ _on_condom_removed(girl, skip_hide=True)
                call _cum_dispatch_condom_remove(girl, scene_type) from _call_condom_remove_cbreak_cream_ok
                $ store._condom_broken_hidden = False
                python:
                    _bel_pool = _CBREAK_CREAM_BELIEVED_LINES.get(_cb_tk, _CBREAK_CREAM_BELIEVED_LINES["_default"])
                $ set_scene_expression(girl, "serious")
                $ Say_Line(girl, _tl(renpy.random.choice(_bel_pool)))
                python:
                    _bel_narr_pool = _CBREAK_CREAM_NARR_BELIEVED.get(_cb_tk, _CBREAK_CREAM_NARR_BELIEVED["_default"])
                    _cb_narr = _tl(renpy.random.choice(_bel_narr_pool))
                "[_cb_narr]"
                $ store._scene_condom_break = True
                $ store._scene_condom_break_believed = True
            else:
                $ _cb_excuse_key = _cb_excuse if _cb_excuse != "didnt_notice" else None
                $ _condom_break_apply_stats(girl, _cb_excuse_key)
                $ _on_condom_removed(girl, skip_hide=True)
                call _cum_dispatch_condom_remove(girl, scene_type) from _call_condom_remove_cbreak_cream_angry
                $ store._condom_broken_hidden = False

                if _condom_break_cream_ends_scene(girl, _cb_excuse):
                    $ store._witness_expression_lock = True
                    python:
                        _end_pool = _CBREAK_CREAM_ANGRY_END_LINES.get(_cb_tk, _CBREAK_CREAM_ANGRY_END_LINES["_default"])
                    $ Say_Line(girl, _tl(renpy.random.choice(_end_pool)))
                    python:
                        _in_her_room = (store.CurrentLocation == girl.gid + "_room")
                        _end_narr_pool = _CBREAK_CREAM_NARR_END_HERROOM if _in_her_room else _CBREAK_CREAM_NARR_END_ELSEWHERE
                        _cb_narr = _tl(renpy.random.choice(_end_narr_pool))
                    "[_cb_narr]"
                    $ store._witness_expression_lock = False
                    if getattr(girl, '_ntr_violation_pending', False):
                        call _angry_end_ntr_confrontation(girl) from _call_aend_ntr_cbreak_cream
                    $ force_scene_reset(girl, angry_days=2, reason="condom_break_creampie")
                    jump main_loop
                else:
                    $ set_scene_expression(girl, "angry")
                    python:
                        _ang_narr_pool = _CBREAK_CREAM_NARR_ANGRY_CONT.get(_cb_tk, _CBREAK_CREAM_NARR_ANGRY_CONT.get("hardcore_sex"))
                        _cb_narr = _tl(renpy.random.choice(_ang_narr_pool))
                    "[_cb_narr]"
                    $ store._scene_condom_break = True
                    $ store._scene_condom_break_believed = False

        "Cum outside":
            call PlayerCumMenu_Outside_Penetration(girl, scene_type) from _call_PlayerCumMenu_Outside_cbreak
            if _condom_break_discovery_roll("fire_away"):
                call CondomBreakDiscovery(girl, scene_type) from _call_CondomBreakDisc_pullout
            else:
                python:
                    _cbreak_safe_narr = _tl(renpy.random.choice([
                        _("She doesn't seem to notice anything wrong with the condom."),
                        _("She glances at the condom but doesn't notice the tear. You got lucky."),
                    ]))
                "[_cbreak_safe_narr]"
                $ print("[CONDOM_BREAK] pull-out: not discovered, counts as condom sex")

    return
