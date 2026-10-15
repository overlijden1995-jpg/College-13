# ============================================================
# hangout_tod_bf.rpy
# The girl's boyfriend NPC as a LIMITED Truth-or-Dare participant.
# He spins and can be targeted, but uses his own small dedicated pool:
# - answers TRUTHS automatically (by trait / friendship / NTR state)
# - has a few DARES (funny dance / silly face / cheek kiss; may beg a
#   real kiss the girl ALWAYS refuses)
# - refusing = he DRINKS (no strip; he has no clothing mechanics)
# ============================================================

init python:

    # ---- State helpers -------------------------------------------------
    def _bf_get_gf(npc):
        """Return the NPC's actual girlfriend Girl object, or None."""
        if hasattr(npc, "girl_gid"):
            return GIRL_BY_ID.get(npc.girl_gid)
        return None

    def _bf_is_gf(npc, girl):
        """Is this girl the NPC's girlfriend?"""
        return hasattr(npc, "girl_gid") and girl is not None and npc.girl_gid == girl.gid

    def _npc_is_ntr(npc):
        return bool(npc) and (npc.has_trait("ntr") or getattr(npc, "_ntr_active", False))

    def _bf_friend_tier(npc):
        f = getattr(npc, "friendship_with_player", 200)
        if f < 200:
            return "hostile"
        if f < 500:
            return "neutral"
        return "friendly"

    def _bf_apply(npc, girl, fr=0, susp=0, gobed=0, glove=0, nobed=0, bfloy=0):
        """Apply a bf-truth's outcome: friendship / suspicion / girl stats.
        bfloy = change to the girl's loyalty toward HER boyfriend (negative = she
        pulls away from him, which helps the player)."""
        if fr and hasattr(npc, "change_friendship"):
            npc.change_friendship(fr)
        if susp and callable(globals().get("Change_NPC_Status")):
            Change_NPC_Status(npc, "suspicion", susp)
        if gobed and girl is not None:
            Change_Status(girl, "Obed", gobed)
        if glove and girl is not None:
            Change_Status(girl, "Love", glove)
        if bfloy and girl is not None and hasattr(girl, "change_bf_loyalty"):
            girl.change_bf_loyalty(bfloy)
            if callable(globals().get("_sync_girl")):
                _sync_girl(girl)
        print("[TOD-BF] %s outcome: fr=%d susp=%d gobed=%d glove=%d bfloy=%d" % (getattr(npc, "gid", "?"), fr, susp, gobed, glove, bfloy))

    def _bf_say(asker, line):
        """Say a line as the asker (player string / girl / npc)."""
        if asker == "player":
            Say_Player(line)
        elif isinstance(asker, NPCPartner):
            Character(asker.Name, color=asker.color)(line)
        else:
            Say_Line(asker, line)

    def _girl_max_act(girl):
        """0 = nothing, higher = further. Used for 'what has she done' answers."""
        acts = getattr(girl, "Sex_acts", {}) or {}
        # Acts only: a position is never evidence of anything (every vaginal position already counts as "sex")
        return max([acts.get(k, 0) for k in ("anal", "sex", "bj", "tj", "hj")] + [0])

    def _bft_girl_secret(npc, girl):
        """Bf reveals a FETISH / desire of hers -- something she's INTO, not
        something they've necessarily done (his relationship may be new).
        girl_narr / girl_line / girl_expr / girl_blush in fx -> processed by the label."""
        if girl.has_trait("camera_lover"):
            return (_("She's got a thing for cameras. Fantasizes about being filmed, I can tell."),
                    {"fr": 6, "gobed": 8, "girl_expr": "embarrassed", "girl_blush": "2",
                     "girl_narr": _("She turns bright red."),
                     "girl_line": _("That is NOT true! ...Okay, maybe a little. But you didn't have to SAY it!"),
                     "girl_disc": "camera_lover"})
        if girl.has_trait("exhibitionist"):
            return (_("She's into the idea of getting caught in public. Really gets her going."),
                    {"fr": 6, "gobed": 8, "girl_expr": "embarrassed", "girl_blush": "2",
                     "girl_narr": _("She covers her face, mortified."),
                     "girl_line": _("Oh my god, shut UP!"),
                     "girl_disc": "exhibitionist"})
        if girl.has_trait("cum_slut"):
            return (_("She's obsessed with the idea of a guy finishing inside. Won't admit it, but she is."),
                    {"fr": 6, "gobed": 10, "girl_expr": "embarrassed", "girl_blush": "2",
                     "girl_narr": _("She elbows %(po)s hard."),
                     "girl_line": _("I am NOT! ...You are SO dead later."),
                     "girl_disc": "cum_slut"})
        if girl.has_trait("anal_lover"):
            return (_("She's curious about... the back door. Way more than she'd ever let on."),
                    {"fr": 6, "gobed": 8, "girl_expr": "surprised", "girl_blush": "2",
                     "girl_narr": _("She gasps, covering her mouth."),
                     "girl_line": _("WHAT?! I never said..."),
                     "girl_disc": "anal_lover"})
        if girl.has_trait("hardcore_sex"):
            return (_("She fantasizes about it rough. Rougher than you'd ever guess."),
                    {"fr": 6, "gobed": 8, "girl_expr": "shy", "girl_blush": "1",
                     "girl_line": _("Not wrong. But still!"),
                     "girl_disc": "hardcore_sex"})
        return (_("Nah, she's an open book. Mostly."), {"fr": 4})

    def _bft_count_before(npc, girl):
        if _girl_max_act(girl) > 0:
            return (_("Two, maybe three? She's a good girl."),
                    {"fr": 2, "girl_expr": "smirk", "girl_blush": "1",
                     "girl_narr": _("She giggles, glancing at you."),
                     "girl_line": _("Yeah... only that many! Hehe.")})
        return (_("Two, maybe three? She's a good girl."), {"fr": 2})

    def _bft_throw_secret(npc, girl):
        """Bf throws his OWN secret into the circle, keyed to his trait. All
        variants earn friendship (he's opening up to the group)."""
        _disc = getattr(girl, "_ntr_boundary_discovered", False)
        if _npc_is_ntr(npc) and _disc and npc.has_trait("camera_lover"):
            return (_("Honestly? I really enjoy watching certain... videos."), {"fr": 8, "narr": _("%(Pp)s smirks.")})
        if _npc_is_ntr(npc) and _disc:
            return (_("I kind of like to watch certain things."), {"fr": 8, "narr": _("%(Pp)s grins.")})
        return (_("Okay, okay... I can't drink much without passing out. Never could."), {"fr": 8, "narr": _("%(Pp)s laughs.")})

    # ---- Named resolvers (no lambdas -- they break Ren'Py save/pickle) --
    def _bft_campus_crush(npc, girl):
        if _bf_friend_tier(npc) == "friendly" or renpy.random.random() < 0.4:
            return (_("Honestly? My girl right here. Obviously."), {"fr": 12})
        return (_("Mark, from my calculus class. The guy is hilarious."), {"bfloy": -20, "fr": 10})

    def _bft_fav_drink(npc, girl):
        drink = renpy.random.choice([_("Cold beer"), _("Whiskey"), _("Straight vodka"), _("Energy drinks"), _("Rum and coke")])
        return (_tl(_("%s, no question. I could drink it all night.")) % drink, {"fr": 6})

    def _bft_sexual_history(npc, girl):
        return (_bf_history_answer(npc, girl), {"fr": 4})

    # ---- GF truth resolvers (girl asks her boyfriend) ---
    def _bft_gf_first_saw(npc, girl):
        if _npc_is_ntr(npc) and getattr(girl, "_ntr_boundary_discovered", False):
            return (_("I saw you and knew I had to have you. Everyone else noticed too."),
                    {"fr": 4, "girl_expr": "shy", "girl_blush": "1",
                     "girl_line": _("Stop it, you're embarrassing me!")})
        return (_("I couldn't stop staring. You were the prettiest girl in the room."),
                {"fr": 6, "girl_expr": "happy", "girl_blush": "1",
                 "girl_line": _("Aww, you never told me that!")})

    def _bft_gf_jealous(npc, girl):
        if _bf_friend_tier(npc) == "hostile":
            return (_("Honestly? Yeah. Especially around certain people."),
                    {"susp": 5, "girl_expr": "serious",
                     "girl_line": _("You don't have to worry about anything.")})
        if _npc_is_ntr(npc) and getattr(girl, "_ntr_boundary_discovered", False):
            return (_("Jealous? Nah. I trust you. A little competition keeps things exciting."),
                    {"fr": 6, "girl_expr": "surprised",
                     "girl_line": _("You're so weird sometimes.")})
        return (_("Only when guys stare too long. But I trust you."),
                {"fr": 6, "girl_expr": "happy",
                 "girl_line": _("You're sweet.")})

    def _bft_gf_best_thing(npc, girl):
        if _npc_is_ntr(npc) and getattr(girl, "_ntr_boundary_discovered", False):
            return (_("The way you turn heads everywhere we go. Makes me proud."),
                    {"fr": 4, "girl_expr": "smirk", "girl_blush": "1",
                     "girl_line": _("Of course it does.")})
        return (_("Waking up knowing you're mine. Cheesy, I know."),
                {"fr": 8, "girl_expr": "happy", "girl_blush": "1",
                 "girl_line": _("That IS cheesy. But I love it.")})

    def _bft_gf_never_told(npc, girl):
        if _npc_is_ntr(npc) and getattr(girl, "_ntr_boundary_discovered", False) and npc.has_trait("camera_lover"):
            return (_("Sometimes I think about you with other people. And it doesn't bother me as much as it should."),
                    {"fr": 4, "gobed": 5, "girl_expr": "surprised", "girl_blush": "1",
                     "girl_line": _("Wait, seriously?")})
        return (_("I still get nervous around you sometimes. Like, butterflies."),
                {"fr": 6, "girl_expr": "happy", "girl_blush": "1",
                 "girl_line": _("After all this time? That's adorable.")})

    # ---- "Always refuse" resolvers: BF panics and drinks instead ----------
    def _bft_fetish(npc, girl):
        lines = [
            _("NOPE. Not answering that. Not a chance."),
            _("That is between me and my browser history. Which you will NEVER see."),
            _("I'd rather drink the whole bottle than answer that."),
        ]
        fx = {"refuse": True}
        if girl is not None:
            fx["girl_expr"] = "bemused"
            fx["girl_line"] = renpy.random.choice([
                _("Come on, it can't be THAT bad!"),
                _("Now I'm really curious..."),
            ])
        return (renpy.random.choice(lines), fx)

    def _bft_childhood_crush(npc, girl):
        lines = [
            _("No. Absolutely not. That stays buried. Forever."),
            _("I will take that secret to my GRAVE."),
            _("Nope. Next question. Moving on."),
        ]
        fx = {"refuse": True}
        if girl is not None:
            fx["girl_expr"] = "smirk"
            fx["girl_line"] = renpy.random.choice([
                _("Ooh, it must be someone embarrassing!"),
                _("Was it a cartoon character? It was, wasn't it?"),
            ])
        return (renpy.random.choice(lines), fx)

    # ---- Bust preference resolver (all pools) ----------------------------
    def _bft_bust_pref(npc, girl):
        _pref = getattr(npc, "bust_pref", "medium")
        _gf_bust = getattr(girl, "bust", "medium") if girl else "medium"
        _match = (_pref == _gf_bust) if girl else True

        _ANSWER = {
            "large":  _("The bigger the better! What can I say, I know what I like."),
            "medium": _("I like them medium. Not too big, not too small. Perfect fit."),
            "small":  _("I actually prefer smaller. There's something about it."),
        }
        _ans = _ANSWER.get(_pref, _ANSWER["medium"])
        fx = {"fr": 4}

        if girl is None:
            return (_ans, fx)

        if _match:
            fx["glove"] = 10
            fx["girl_expr"] = "happy"
            fx["girl_blush"] = "1"
            if _gf_bust == "large":
                fx["girl_line"] = renpy.random.choice([
                    _("See? %(Pp)s knows what %(pp)s's got!"),
                    _("Good answer, babe."),
                    _("Damn right you do."),
                ])
            elif _gf_bust == "medium":
                fx["girl_line"] = renpy.random.choice([
                    _("Aww, you're sweet."),
                    _("Perfect fit, huh? I like that."),
                    _("Good. Because that's exactly what you've got."),
                ])
            else:
                fx["girl_line"] = renpy.random.choice([
                    _("Wait, really? You actually mean that?"),
                    _("That's... the sweetest thing you've ever said."),
                    _("Most people don't say that. Thank you."),
                ])
        else:
            fx["npc_love"] = -15
            fx["girl_expr"] = "angry"
            if _pref == "large" and _gf_bust != "large":
                fx["girl_narr"] = _("She stares at %(po)s, unamused.")
                fx["girl_line"] = renpy.random.choice([
                    _("Bigger the better? Really? And what am I, chopped liver?"),
                    _("Wow. Good to know where I stand."),
                    _("So mine aren't good enough? Nice."),
                ])
            elif _pref == "medium" and _gf_bust == "large":
                fx["girl_narr"] = _("She crosses her arms over her chest.")
                fx["girl_line"] = renpy.random.choice([
                    _("Medium? So what, mine are TOO big for you?"),
                    _("Oh, so I'm too much? Great."),
                    _("Sorry my body isn't 'medium' enough for you."),
                ])
            elif _pref == "medium" and _gf_bust == "small":
                fx["girl_narr"] = _("She looks down at herself, then back at %(po)s.")
                fx["girl_line"] = renpy.random.choice([
                    _("Medium. Of course. Right in between where I am."),
                    _("Not big, not small. Just not mine. Got it."),
                    _("So I'm below your standards. Cool."),
                ])
            elif _pref == "small" and _gf_bust == "large":
                fx["girl_narr"] = _("She gestures at herself in disbelief.")
                fx["girl_line"] = renpy.random.choice([
                    _("You prefer SMALL? Then why are you with ME?!"),
                    _("Small? SMALL? Have you SEEN these?!"),
                    _("I literally have the opposite of what you want. Great."),
                ])
            elif _pref == "small" and _gf_bust == "medium":
                fx["girl_narr"] = _("She narrows her eyes at %(po)s.")
                fx["girl_line"] = renpy.random.choice([
                    _("Smaller, huh? Sorry I'm not flat enough for you."),
                    _("Well excuse me for having curves."),
                    _("Maybe you should date someone else then."),
                ])

            # NPC tries to backpedal after upsetting his girlfriend
            fx["npc_recover"] = True
            if _gf_bust == "small":
                fx["npc_recover_line"] = renpy.random.choice([
                    _("Wait, babe, I didn't mean it like that! Yours are cute too!"),
                    _("Hey, I said a preference, not a requirement! You're perfect."),
                    _("No no no, I love yours! They're beautiful!"),
                ])
            elif _gf_bust == "medium":
                fx["npc_recover_line"] = renpy.random.choice([
                    _("Babe, come on! Yours are great! I wasn't thinking."),
                    _("Sorry sorry sorry! Your boobs are perfect, I swear!"),
                    _("Wait, that came out wrong! You know I love your body!"),
                ])
            else:
                fx["npc_recover_line"] = renpy.random.choice([
                    _("Babe, I was just saying! You know I love everything about you!"),
                    _("Come on, don't be mad! Yours are amazing!"),
                    _("I didn't mean it! You're gorgeous, you know that!"),
                ])
        return (_ans, fx)

    # ---- BF TRUTHS: each resolve(npc, girl) -> (answer_line, effects) ---
    # effects keys: fr / susp / gobed / glove. NTR lover generally flips.
    # "refuse": True -> BF drinks double instead of answering.
    _BF_TRUTHS = {
        "campus_crush": {
            "q": _("So, who do you like most on campus?"),
            "resolve": _bft_campus_crush,
        },
        "girl_secret": {
            "q": _("Any other secret you're hiding about her?"),
            "resolve": _bft_girl_secret,
        },
        "fetish": {
            "q": _("What's your biggest fetish?"),
            "resolve": _bft_fetish,
        },
        "childhood_crush": {
            "q": _("Who was your childhood crush?"),
            "resolve": _bft_childhood_crush,
        },
        "bust_pref": {
            "q": _("What breast size do you prefer?"),
            "resolve": _bft_bust_pref,
        },
    }
    _BF_TRUTH_ORDER = list(_BF_TRUTHS.keys())

    # ---- GF truths (girl asks her boyfriend) ---
    _BF_GF_TRUTHS = {
        "gf_first_saw": {
            "q": _("What did you think the first time you saw me?"),
            "resolve": _bft_gf_first_saw,
        },
        "gf_jealous": {
            "q": _("Do you ever get jealous?"),
            "resolve": _bft_gf_jealous,
        },
        "gf_best_thing": {
            "q": _("What's the best thing about being with me?"),
            "resolve": _bft_gf_best_thing,
        },
        "gf_never_told": {
            "q": _("What's something you've never told me?"),
            "resolve": _bft_gf_never_told,
        },
        "fetish": {
            "q": _("What's your biggest fetish?"),
            "resolve": _bft_fetish,
        },
        "childhood_crush": {
            "q": _("Who was your childhood crush?"),
            "resolve": _bft_childhood_crush,
        },
        "bust_pref": {
            "q": _("What breast size do you prefer?"),
            "resolve": _bft_bust_pref,
        },
    }
    _BF_GF_TRUTH_ORDER = list(_BF_GF_TRUTHS.keys())

    # ---- Casual resolvers (non-GF girl asks the NPC) ------------------
    def _bft_casual_subject(npc, girl):
        subj = renpy.random.choice([_("History"), _("Biology"), _("Business"), _("Sports Science")])
        return (_tl(_("%s. It's the one class I actually look forward to.")) % subj, {"fr": 6})

    def _bft_casual_embarrass(npc, girl):
        lines = [
            _("I slipped on a wet floor in the cafeteria. Full tray. Everyone saw."),
            _("I waved at someone I thought I knew. It was a stranger. We made eye contact for way too long."),
            _("I walked into the wrong lecture and sat through twenty minutes before I realized."),
        ]
        return (renpy.random.choice(lines), {"fr": 6})

    def _bft_casual_hobby(npc, girl):
        hobbies = [
            _("Working out, mostly. Sometimes I game when nobody's watching."),
            _("I play guitar, actually. Not well, but I try."),
            _("I watch way too many movies. Like, an embarrassing amount."),
        ]
        return (renpy.random.choice(hobbies), {"fr": 6})

    def _bft_casual_worst_date(npc, girl):
        _gf = _bf_get_gf(npc)
        lines = [
            _("Took a girl to a restaurant once and my card got declined. Had to wash dishes. Not literally, but almost."),
            _("She showed up with her ex. Said it was 'for safety.' I left after ten minutes."),
        ]
        fx = {"fr": 6}
        if _gf is not None:
            fx["girl_expr"] = "smirk"
            fx["girl_line"] = _("At least you learned from your mistakes... right?")
        return (renpy.random.choice(lines), fx)

    def _bft_casual_fear(npc, girl):
        fears = [
            _("Heights. I know, I know. Just don't make me look down."),
            _("Spiders. Don't judge me. Those things are NOT okay."),
            _("Failing out of school. My parents would literally end me."),
        ]
        return (renpy.random.choice(fears), {"fr": 6})

    def _bft_casual_dumb_thing(npc, girl):
        lines = [
            _("I tried to impress a girl by doing a backflip off a bench. Landed on my face."),
            _("Drank an entire bottle of hot sauce on a dare. Couldn't taste anything for three days."),
            _("Texted my ex 'I miss you' at 3 AM. Sober. On purpose. Still cringe about it."),
        ]
        return (renpy.random.choice(lines), {"fr": 8})

    _BF_CASUAL_TRUTHS = {
        "casual_subject": {
            "q": _("What's your favorite subject?"),
            "resolve": _bft_casual_subject,
        },
        "casual_embarrass": {
            "q": _("What's the most embarrassing thing that happened to you on campus?"),
            "resolve": _bft_casual_embarrass,
        },
        "casual_hobby": {
            "q": _("What do you do for fun?"),
            "resolve": _bft_casual_hobby,
        },
        "casual_worst_date": {
            "q": _("What was the worst date you've ever been on?"),
            "resolve": _bft_casual_worst_date,
        },
        "casual_fear": {
            "q": _("What's something you're secretly afraid of?"),
            "resolve": _bft_casual_fear,
        },
        "casual_dumb_thing": {
            "q": _("What's the dumbest thing you've ever done?"),
            "resolve": _bft_casual_dumb_thing,
        },
        "fetish": {
            "q": _("What's your biggest fetish?"),
            "resolve": _bft_fetish,
        },
        "childhood_crush": {
            "q": _("Who was your childhood crush?"),
            "resolve": _bft_childhood_crush,
        },
        "bust_pref": {
            "q": _("What breast size do you prefer?"),
            "resolve": _bft_bust_pref,
        },
    }
    _BF_CASUAL_TRUTH_ORDER = list(_BF_CASUAL_TRUTHS.keys())

    # ---- Player-asked bf truths ---------------------------------------
    _BF_PLAYER_TRUTHS = {
        "fav_drink": {
            "q": _("What's your favorite drink?"),
            "resolve": _bft_fav_drink,
        },
        "sexual_history": {
            "q": _("What have you actually done with her, so far?"),
            "resolve": _bft_sexual_history,
        },
        "throw_secret": {
            "q": _("Throw a secret into the circle!"),
            "resolve": _bft_throw_secret,
        },
        "count_before": {
            "q": _("Do you even know how many guys she was with before you?"),
            "resolve": _bft_count_before,
        },
        "bust_pref": {
            "q": _("What breast size do you prefer?"),
            "resolve": _bft_bust_pref,
        },
    }

    def _bf_history_answer(npc, girl):
        """How far HIS OWN relationship with her has gone. Reads bf_history
        (the actual acts tracked on the girl for her NPC partner)."""
        bfh = getattr(girl, "bf_history", {}) or {}
        if bfh.get("creampie"):
            return _tl(_("Everything. And I mean EVERYTHING. She's all mine."))
        if bfh.get("sex_raw"):
            return _tl(_("We've gone all the way. Raw, too. She trusts me like that."))
        if bfh.get("sex"):
            return _tl(_("We've done it all. The real deal. She's my girl."))
        if bfh.get("bj"):
            return _tl(_("She's gone down on me. More than once."))
        if bfh.get("tj"):
            return _tl(_("We've fooled around. She knows how to use her... assets."))
        if bfh.get("hj") or bfh.get("masturbate"):
            return _tl(_("We've messed around a bit. Hands stuff, you know. Taking it slow."))
        if girl.has_trait("virgin"):
            return _tl(_("Honestly? We're taking it slow. Haven't gone all the way yet."))
        return _tl(_("Honestly? Less than I'd like lately. But she's still mine."))

    # ---- BF DARES (few; no strip -- he never undresses) ---------------
    # If he refuses a dare he drinks DOUBLE instead of stripping.
    _BF_DARES = ["dance", "silly_face", "run_campus", "arm_wrestle", "show_phone", "show_dick", "show_history"]

    def _bf_run_campus_accepts(npc):
        """Will the bf actually sprint to campus and back? Scales with how drunk
        he is and his friendship with the player. NTR lovers are game for
        anything; a proud bf only plays along if he genuinely likes the player."""
        drunk = get_drunk(npc)                       # 0..DRUNK_MAX
        fr = getattr(npc, "friendship_with_player", 200)
        score = drunk * 8 + fr / 12.0
        if _npc_is_ntr(npc):
            score += 45                              # NTR: down for anything
        elif npc.has_trait("proud"):
            score += 30 if fr >= 500 else -60        # proud: needs friendship
        _ok = score >= 70
        print("[TOD-BF] run_campus check: drunk=%.1f fr=%d score=%.0f -> %s" % (drunk, fr, score, _ok))
        return _ok

    # ---- BF ASKS THE PLAYER (guy-talk). The PLAYER picks from 3 answers. ----
    # Tiers: [0] humble -> bf respects you (fr up); [1] modest -> his girl mildly
    # notices you (gobed up, NO fr hit); [2] the ONE real humiliation -> fr down,
    # gobed up, she reacts. On the humiliation the girl also reads the CONTENT:
    # a matching "traits" entry adds Love/Obed and a special line (e.g. "finish
    # inside" + cum_slut). Option:
    #   {"a":, "fx": {fr/susp/gobed/glove}, "reply":, opt "girl":,
    #    opt "traits": {trait_id: {"fx": {...}, "line": _(...)}}}
    _BF_ASK_PLAYER = {
        "rounds": {
            "q": _("Alright, honest question: how many rounds can YOU go in one night?"),
            "options": [
                {"a": _("One good one is all it takes."), "fx": {"fr": 8}, "reply": _("Ha! A humble man. Respect.")},
                {"a": _("Two or three, easy."), "fx": {"gobed": 3}, "reply": _("Not bad. Not bad at all.")},
                {"a": _("I lose count. All night."), "fx": {"fr": -8, "gobed": 6}, "reply": _("...All night, huh."),
                 "reply_narr": _("%(Poss)s partner looks a little too interested."),
                 "traits": {"hardcore_sex": {"fx": {"glove": 12, "gobed": 10}, "narr": _("She bites her lip."), "line": _("I'd love to test that theory.")}}},
            ],
        },
        "fav_subject": {
            "q": _("So what's your favorite subject?"),
            "options": [
                {"a": _("Honestly? Nothing exciting. Just the usual classes."), "fx": {"fr": 5}, "reply": _("A serious guy. I respect that.")},
                {"a": _("Sexology. What? It's educational!"), "fx": {"fr": 2, "gobed": 3}, "reply": _("Ha! A man of culture. Careful with that one."), "girl_narr": _("She giggles."), "girl": _("Is that even a real class?")},
                {"a": _("Whatever she's teaching."), "fx": {"fr": -6, "gobed": 5}, "reply": _("...Watch it."), "girl_narr": _("She raises an eyebrow, a little flattered despite herself.")},
            ],
        },
        "bench": {
            "q": _("How much do you bench?"),
            "options": [
                {"a": _("Eh, I don't really track it. I'm not about the numbers."), "fx": {"fr": 6}, "reply": _("Honest. I can respect that.")},
                {"a": _("Enough to hold my own."), "fx": {"gobed": 3}, "reply": _("Fair enough.")},
                {"a": _("More than you, guaranteed."), "fx": {"fr": -8, "gobed": 6}, "reply": _("...Big talk."),
                 "reply_narr": _("%(Poss)s partner is definitely checking you out."),
                 "traits": {"hardcore_sex": {"fx": {"glove": 10, "gobed": 8}, "narr": _("She smirks."), "line": _("Strong AND cocky. Noted.")}}},
            ],
        },
        "campus_girls": {
            "q": _("You ever hook up with a girl on campus?"),
            "options": [
                {"a": _("Nah, I keep to myself."), "fx": {"fr": 8}, "reply": _("A gentleman. Rare these days.")},
                {"a": _("A couple. Nothing serious."), "fx": {"gobed": 3}, "reply": _("Ha, fair enough. Who hasn't.")},
                {"a": _("Lost count, honestly."), "fx": {"fr": -8, "gobed": 5, "susp": 5}, "reply": _("...Right in front of me, huh."), "girl_narr": _("She bites her lip and looks away."),
                 "traits": {"cheater": {"fx": {"glove": 10, "gobed": 8}, "narr": _("She grins."), "line": _("A man who gets around. I can respect that.")}}},
            ],
        },
        "condom": {
            "q": _("You always wrap it up?"),
            "options": [
                {"a": _("Always. Safety first."), "fx": {"fr": 8}, "reply": _("Smart man. Respect.")},
                {"a": _("Depends on the girl."), "fx": {"gobed": 4}, "reply": _("...Bold answer.")},
                {"a": _("Never. I finish where I want."), "fx": {"fr": -10, "gobed": 8, "susp": 8}, "reply": _("...Jesus."), "girl_narr": _("She shifts in her seat, staring at you."),
                 "traits": {
                    "cum_slut": {"fx": {"glove": 15, "gobed": 15}, "narr": _("Her thighs press together."), "line": _("...God, I shouldn't find that as hot as I do.")},
                    "hate_cum": {"fx": {"glove": -10, "gobed": -5}, "narr": _("She recoils."), "line": _("Ugh. That's actually disgusting.")},
                 }},
            ],
        },
        "threesome": {
            "q": _("You ever had a threesome?"),
            "options": [
                {"a": _("Nah, one at a time is plenty for me."), "fx": {"fr": 6}, "reply": _("Humble. I like it.")},
                {"a": _("Maybe. A gentleman doesn't kiss and tell."), "fx": {"gobed": 3}, "reply": _("Ha! Mysterious.")},
                {"a": _("Once or twice. It's a talent."), "fx": {"fr": -6, "gobed": 7}, "reply": _("...Show off."),
                 "reply_narr": _("%(Poss)s partner looks way too curious."),
                 "traits": {"exhibitionist": {"fx": {"glove": 10, "gobed": 10}, "narr": _("She leans in."), "line": _("You'd have to tell me EVERYTHING.")}}},
            ],
        },
        "weekend": {
            "q": _("Weekend: chasing girls or hanging with the boys?"),
            "options": [
                {"a": _("The boys, honestly. Keep it simple."), "fx": {"fr": 8}, "reply": _("A man of priorities. Respect.")},
                {"a": _("A bit of both. Balance."), "fx": {"gobed": 3}, "reply": _("Reasonable.")},
                {"a": _("Chasing whatever catches my eye."), "fx": {"fr": -8, "gobed": 6, "susp": 5}, "reply": _("...Careful where those eyes wander."),
                 "traits": {"cheater": {"fx": {"glove": 8, "gobed": 8}, "narr": _("She holds your gaze."), "line": _("Careful. Some eyes wander right back.")}}},
            ],
        },
        "contacts": {
            "q": _("How many girls' numbers you got in your phone right now?"),
            "options": [
                {"a": _("Like two, and one of them is my mom."), "fx": {"fr": 6}, "reply": _("Ha! A simple life.")},
                {"a": _("A few. I'm not counting."), "fx": {"gobed": 3}, "reply": _("Fair enough.")},
                {"a": _("More than I can text back."), "fx": {"fr": -6, "gobed": 5}, "reply": _("...A player."),
                 "reply_narr": _("%(Poss)s partner rolls her eyes, but she is smiling at you."),
                 "traits": {"cheater": {"fx": {"glove": 8, "gobed": 8}, "narr": _("She slides you her number under the table.")}}},
            ],
        },
        "sleep_sex": {
            "q": _("You ever fall asleep in the middle of it?"),
            "options": [
                {"a": _("Once. Long day, don't judge me."), "fx": {"fr": 6}, "reply": _("Ha! We've all been there.")},
                {"a": _("Never. I always finish what I start."), "fx": {"gobed": 4}, "reply": _("...Confident. I'll allow it.")},
                {"a": _("Fall asleep? I'm the one keeping HER up all night."), "fx": {"fr": -8, "gobed": 7}, "reply": _("...Sure you are."),
                 "reply_narr": _("%(Poss)s partner raises an eyebrow at you."),
                 "traits": {"cum_slut": {"fx": {"glove": 10, "gobed": 10}, "narr": _("She murmurs."), "line": _("...Some girls would kill for that.")}}},
            ],
        },
        "stalk": {
            "q": _("Be honest, you stalk anyone's profile in this room today?"),
            "options": [
                {"a": _("Nah, I'm not like that."), "fx": {"fr": 6}, "reply": _("Good. That's creepy behavior.")},
                {"a": _("Maybe I glanced. No harm in looking."), "fx": {"gobed": 3}, "reply": _("Ha. Honest, at least.")},
                {"a": _("Just your girl's, actually."), "fx": {"fr": -12, "gobed": 5, "susp": 12}, "reply": _("...Excuse me?"), "reply_narr": _("%(Poss)s jaw tightens."), "girl_narr": _("She hides a pleased little smile."),
                 "traits": {"exhibitionist": {"fx": {"glove": 8, "gobed": 10}, "narr": _("She preens."), "line": _("And? See anything you liked?")}}},
            ],
        },
        "cheated_trust": {
            "q": _("You ever broken a girl's trust?"),
            "options": [
                {"a": _("Never. Trust is everything to me."), "fx": {"fr": 8}, "reply": _("A stand-up guy. Respect.")},
                {"a": _("Once. I'm not proud of it."), "fx": {"fr": 3}, "reply": _("At least you're honest about it.")},
                {"a": _("What happens behind closed doors stays there."), "fx": {"fr": -8, "gobed": 5, "susp": 8}, "reply": _("...I'll keep that in mind."), "girl_narr": _("She looks at you a little differently now."),
                 "traits": {"cheater": {"fx": {"glove": 8, "gobed": 8}, "narr": _("She smirks."), "line": _("Finally, someone who gets it.")}}},
            ],
        },
        "bad_pickup": {
            "q": _("What's the worst pickup line you've used that actually worked?"),
            "options": [
                {"a": _("'Are you a parking ticket? Because you've got FINE written all over you.' ...It worked. I'm as shocked as you are."), "fx": {"fr": 6}, "reply": _("That's awful. Respect, though."), "reply_narr": _("%(Pp)s groans.")},
                {"a": _("I keep it simple. A smile does the work."), "fx": {"gobed": 3}, "reply": _("Smooth. Too smooth.")},
                {"a": _("I don't need lines."), "fx": {"fr": -4, "gobed": 5}, "reply": _("...Cocky."), "reply_narr": _("%(Poss)s partner smirks at you.")},
            ],
        },
        "gym_swim": {
            "q": _("Gym or swimming?"),
            "options": [
                {"a": _("Gym, I guess. Gotta keep moving."), "fx": {"fr": 5}, "reply": _("Solid choice.")},
                {"a": _("Bit of both. Keeps things interesting."), "fx": {"gobed": 3}, "reply": _("A balanced man.")},
                {"a": _("Swimming. Better view at the pool."), "fx": {"fr": -4, "gobed": 4}, "reply": _("Ha! A man with priorities.")},
            ],
        },
        "bust_pref": {
            "q": _("Alright, honest question: what size do you prefer on a girl?"),
            "options": [
                {"a": _("All sizes are great. I'm not picky."), "fx": {"fr": 6}, "reply": _("Ha! Diplomatic. Smart man.")},
                {"a": _("Depends on the girl, honestly. It's about the whole package."), "fx": {"gobed": 4}, "reply": _("Fair enough. Can't argue with that.")},
                {"a": _("Your girl's size, actually. She's got the perfect pair."), "fx": {"fr": -10, "gobed": 8, "susp": 8}, "reply": _("...What did you just say?"),
                 "reply_narr": _("%(Pp)s stares at you. %(Poss)s partner is bright red.")},
            ],
        },
    }
    _BF_ASK_PLAYER_ORDER = list(_BF_ASK_PLAYER.keys())


# ============================================================
# BF is the TARGET (bottle landed on him): mostly a truth, sometimes a dare
# ============================================================
label hangout_tod_bf_target(npc, asker):
    python:
        _bft_girl = _bf_get_gf(npc)
        _bft_do_dare = (renpy.random.random() < 0.25)

    $ _bf_say(asker, _tl(_("Truth or dare?")))

    if _bft_do_dare:
        $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([_("Dare. Hit me."), _("Dare! Let's go.")])))
        if _bft_girl is not None:
            $ set_scene_expression(_bft_girl, "confused")
        call _bf_do_dare(npc, _bft_girl, asker) from _call_bf_do_dare_target
        return

    $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([_("Truth. Ask away."), _("Truth. I've got nothing to hide.")])))

    # Truth: pick a question. The player can also ask his own extra set; the
    # girl only asks the general ones.
    python:
        if asker == "player":
            _bft_pool = dict(_BF_TRUTHS)
            _bft_pool.update(_BF_PLAYER_TRUTHS)
            _bft_order = _BF_TRUTH_ORDER + list(_BF_PLAYER_TRUTHS.keys())
        elif _bf_is_gf(npc, asker):
            _bft_pool = _BF_GF_TRUTHS
            _bft_order = _BF_GF_TRUTH_ORDER
        else:
            _bft_pool = _BF_CASUAL_TRUTHS
            _bft_order = _BF_CASUAL_TRUTH_ORDER
        _bft_keys = [k for k in _bft_order if not tod_is_used("bf_" + k)]
        if not _bft_keys:
            _bft_keys = list(_bft_order)

    if asker == "player":
        python:
            _bft_menu = [(_tl(_bft_pool[k]["q"]), k) for k in _bft_keys[:7]]
        $ _bft_key = renpy.display_menu(_bft_menu)
    else:
        $ _bft_key = renpy.random.choice(_bft_keys)

    python:
        _bft_q = _tl(_bft_pool[_bft_key]["q"])
    $ _bf_say(asker, _bft_q)

    if _bft_girl is not None:
        $ set_scene_expression(_bft_girl, "confused")

    python:
        _bft_ans, _bft_fx = _bft_pool[_bft_key]["resolve"](npc, _bft_girl)
    $ Character(npc.Name, color=npc.color)(_tl(_bft_ans))

    if _bft_fx.get("refuse"):
        $ renpy.say(None, _tl(_("%s grabs the bottle instead.")) % npc.Name)
        $ tod_drink(npc, 2)
        if _bft_fx.get("girl_line") and _bft_girl is not None:
            if _bft_fx.get("girl_expr"):
                $ set_scene_expression(_bft_girl, _bft_fx["girl_expr"])
            $ Say_Line(_bft_girl, _tl(_bft_fx["girl_line"]))
        $ tod_mark_used("bf_" + _bft_key)
        if tod_rolls_sick(npc):
            if len(_hangout_girls_list()) == 1:
                call _npc_pass_out_1girl_event from _call_npc_po_1g_truthrefuse
            else:
                call _npc_pass_out_event from _call_npc_po_grp_truthrefuse
            return
        return

    if _bft_fx.get("narr"):
        $ renpy.say(None, _format_npc_line(npc, _bft_fx["narr"]))
    if _bft_fx.get("girl_line") and _bft_girl is not None:
        python:
            _bft_gexpr = _bft_fx.get("girl_expr")
            _bft_gblush = _bft_fx.get("girl_blush")
            _bft_gnarr = _bft_fx.get("girl_narr")
            if _bft_gexpr:
                set_scene_expression(_bft_girl, _bft_gexpr, blush=_bft_gblush)
        if _bft_gnarr:
            $ renpy.say(None, _format_npc_line(npc, _bft_gnarr))
        $ Say_Line(_bft_girl, _format_npc_line(npc, _bft_fx["girl_line"]))
        # her partner outed the fetish and she reacted to it: the player knows now
        python:
            _bft_disc = _bft_fx.get("girl_disc")
            if _bft_disc and hasattr(_bft_girl, "has_trait") and _bft_girl.has_trait(_bft_disc) and hasattr(_bft_girl, "discover"):
                _bft_girl.discover("discovered_trait_%s" % _bft_disc)
    elif _bft_girl is not None:
        python:
            _bft_bfloy = _bft_fx.get("bfloy", 0)
            if _bft_bfloy < 0:
                set_scene_expression(_bft_girl, "angry", eyes="eyes_side")
                _bft_def_line = renpy.random.choice([
                    _("Seriously? That's your answer?"),
                    _("Wow. Thanks for that."),
                ])
            else:
                set_scene_expression(_bft_girl, "happy")
                _bft_def_line = renpy.random.choice([
                    _("Good answer."),
                    _("Hm, fair enough."),
                ])
        $ Say_Line(_bft_girl, _tl(_bft_def_line))

    # NPC backpedals after upsetting his girlfriend
    if _bft_fx.get("npc_recover") and _bft_girl is not None:
        $ Character(npc.Name, color=npc.color)(_tl(_bft_fx.get("npc_recover_line", _("Wait, I didn't mean it like that!"))))
        $ set_scene_expression(_bft_girl, "angry", eyes="eyes_side")
        $ Say_Line(_bft_girl, _tl(renpy.random.choice([
            _("Too late. I heard you."),
            _("Save it."),
            _("You already said what you said."),
        ])))

    python:
        _bf_apply(npc, _bft_girl, fr=_bft_fx.get("fr", 0), susp=_bft_fx.get("susp", 0),
                  gobed=_bft_fx.get("gobed", 0), glove=_bft_fx.get("glove", 0),
                  bfloy=_bft_fx.get("bfloy", 0))
        _npc_love_delta = _bft_fx.get("npc_love", 0)
        if _npc_love_delta and hasattr(npc, "love_for_girl"):
            npc.love_for_girl = max(0, min(1000, npc.love_for_girl + _npc_love_delta))
            print("[TOD-BF] %s love_for_girl %+d -> %d" % (npc.gid, _npc_love_delta, npc.love_for_girl))
        tod_mark_used("bf_" + _bft_key)
        # NPC revealed info about his GF -> other girls present learn it
        if _bft_girl is not None and _bft_key in ("sexual_history", "count_before", "girl_secret"):
            _bft_others = [g for g in _hangout_girls_list() if g.gid != _bft_girl.gid]
            if _bft_key == "sexual_history":
                _bfh = getattr(_bft_girl, "bf_history", {}) or {}
                for _bo in _bft_others:
                    if _bfh.get("sex") or _bfh.get("sex_raw") or _bfh.get("creampie"):
                        girl_learns_act(_bo, _bft_girl, "sex")
                    elif _bfh.get("bj"):
                        girl_learns_act(_bo, _bft_girl, "bj")
                    elif _bfh.get("tj"):
                        girl_learns_act(_bo, _bft_girl, "tj")
                    elif _bfh.get("hj") or _bfh.get("masturbate"):
                        girl_learns_act(_bo, _bft_girl, "hj")
            elif _bft_key == "girl_secret":
                for _bo in _bft_others:
                    if _bft_girl.has_trait("virgin"):
                        girl_learns_virgin(_bo, _bft_girl)
            print("[TOD-BF-KNOW] %s revealed %s about %s -> %d others" % (
                getattr(npc, "gid", "?"), _bft_key, _bft_girl.gid, len(_bft_others)))
    return


# ============================================================
# BF SPINS: he asks the target (player or girl) something, or gives a dare
# ============================================================
label hangout_tod_bf_ask(npc, target_id, target_girl):
    if target_id == "player":
        $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([_("Your turn, man. Truth or dare?"), _("Alright man, truth or dare?")])))
        menu:
            "Truth":
                python:
                    _bap_keys = [k for k in _BF_ASK_PLAYER_ORDER if not tod_is_used("bap_" + k)]
                    if not _bap_keys:
                        _bap_keys = list(_BF_ASK_PLAYER_ORDER)
                    _bap_key = renpy.random.choice(_bap_keys)
                call _bf_ask_player_truth(npc, _bap_key) from _call_bf_ask_player_truth
            "Dare":
                $ _bf_own_gf = _bf_get_gf(npc)
                call _bf_dare_player(npc, _bf_own_gf) from _call_bf_dare_player
        return

    # Target is a girl. Route by whether she's the NPC's girlfriend.
    if _bf_is_gf(npc, target_girl):
        if _npc_is_ntr(npc) and getattr(target_girl, "_ntr_boundary_discovered", False) and renpy.random.random() < 0.4:
            call _bf_ask_girl_other_guy(npc, target_girl) from _call_bf_ask_girl_other_guy
            return
        call _bf_ask_girl_tod(npc, target_girl) from _call_bf_ask_girl_tod
    else:
        call _bf_ask_nongf_tod(npc, target_girl) from _call_bf_ask_nongf_tod
    return


# ============================================================
# BF asks his GIRL: full truth-or-dare flow with expressions + reactions.
# ============================================================
label _bf_ask_girl_tod(npc, girl):
    $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([_("Alright babe, truth or dare?"), _("Your turn! Truth or dare?")])))

    python:
        _bfag_alc = tod_effective_alc(girl)
        _bfag_dare = renpy.random.random() < (0.3 + _bfag_alc * 0.04)

    if _bfag_dare:
        $ set_scene_expression(girl, "smirk")
        $ Say_Line(girl, _tl(renpy.random.choice([_("Dare! Do your worst."), _("Dare! I'm not scared of you.")])))

        python:
            _bfag_dtype = renpy.random.choice(["dance", "silly_face", "impression", "show_phone"])

        if _bfag_dtype == "dance":
            $ Character(npc.Name, color=npc.color)(_tl(_("I dare you to show us your best dance move right now!")))
            $ set_scene_expression(girl, "bemused")
            $ Say_Line(girl, _tl(_("Fine! But no judging!")))
            $ Narration(_tl(_("%s jumps up and busts out a surprisingly good move.")) % girl.Name)
            $ set_scene_expression(girl, "happy")
            $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([
                _("That's my girl! Look at those moves!"),
                _("Okay, okay! I see you! Not bad at all!"),
            ])))
        elif _bfag_dtype == "silly_face":
            $ Character(npc.Name, color=npc.color)(_tl(_("I dare you to make the ugliest face you can!")))
            $ set_scene_expression(girl, "serious")
            $ Say_Line(girl, _tl(_("Really? Ugh, fine.")))
            $ Narration(_tl(_("%s scrunches up her face. It is impressively awful.")) % girl.Name)
            $ set_scene_expression(girl, "bemused")
            $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([
                _("Oh my GOD, that's horrifying. I love you but NEVER do that again."),
                _("I'm gonna have nightmares about that face!"),
            ])))
        elif _bfag_dtype == "impression":
            call _tod_dare_impression(npc, girl) from _call_bfag_impression
        elif _bfag_dtype == "show_phone":
            call _tod_dare_show_phone(npc, girl, "gf") from _call_bfag_show_phone
        return

    $ set_scene_expression(girl, "neutral")
    $ Say_Line(girl, _tl(renpy.random.choice([_("Truth. Ask me anything."), _("Truth! I've got nothing to hide.")])))

    python:
        _bfag_tpool = [
            ("embarrass", _("What's the most embarrassing thing that happened to you on campus?")),
            ("cutest", _("Besides me, who's the cutest person in this room?")),
            ("secret", _("Tell us something nobody here knows about you.")),
            ("body_count", _("Be honest... what's your body count?")),
            ("fav_drink", _("Babe, what's your favorite drink? Like, for real.")),
            ("fav_in_bed", _("What's your favorite thing to do in bed? Be honest.")),
            ("open_rel", _("Would you ever do an open relationship?")),
        ]
        _bfag_tpick = renpy.random.choice(_bfag_tpool)
    $ Character(npc.Name, color=npc.color)(_tl(_bfag_tpick[1]))

    if _bfag_tpick[0] == "embarrass":
        $ set_scene_expression(girl, "embarrassed", blush="1")
        $ Say_Line(girl, _tl(renpy.random.choice([
            _("I tripped going up the stairs in front of EVERYONE last week."),
            _("I accidentally called my professor 'mom' in front of the whole class..."),
        ])))
        $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([
            _("HA! Babe, that's amazing. I wish I was there to see it."),
            _("No way! And you never told me? That's gold!"),
        ])))
        $ Narration(_tl(_("Everyone chuckles.")))
    elif _bfag_tpick[0] == "cutest":
        $ set_scene_expression(girl, "shy", blush="1")
        python:
            _bfag_love = getattr(girl, "Love", 0)
            if _bfag_love >= 400:
                _bfag_crush = renpy.random.choice([
                    _("Hmm... I plead the fifth."),
                    _("That's not fair! Next question!"),
                ])
            else:
                _bfag_crush = renpy.random.choice([
                    _("You, obviously!"),
                    _("Nice try! I'm not answering that."),
                ])
        $ Say_Line(girl, _tl(_bfag_crush))
        if _bfag_love >= 400:
            $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([
                _("Wait, why won't you answer? It should be me, right? ...Right?"),
                _("The fifth? That's suspicious, babe."),
            ])))
            python:
                Change_NPC_Status(npc, "suspicion", 5)
                print("[TOD_TRUTH] cutest: GF deflected (Love=%d), suspicion +5" % _bfag_love)
        else:
            $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([
                _("That's what I like to hear!"),
                _("Damn right it's me!"),
            ])))
    elif _bfag_tpick[0] == "secret":
        $ set_scene_expression(girl, "shy")
        $ Say_Line(girl, _tl(renpy.random.choice([
            _("I sometimes sing in the shower way too loud. Like, my neighbors complained."),
            _("I have a secret playlist of songs I would NEVER admit to liking."),
        ])))
        $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([
            _("I KNEW it! I've heard you humming through the wall!"),
            _("Really? That's your big secret? That's adorable."),
        ])))
    elif _bfag_tpick[0] == "body_count":
        python:
            _bc_virgin = girl.has_trait("virgin")
            _bc_experienced = girl.has_trait("experienced")
            _bc_player_sex = _girl_max_act(girl) > 0
            _bc_bf_sex = getattr(girl, "bf_history", {}).get("sex", False)
            _bc_bf_tier = getattr(girl, "bf_max_tier", 0)
        if _bc_virgin:
            $ set_scene_expression(girl, "embarrassed", blush="2")
            $ Say_Line(girl, _tl(renpy.random.choice([
                _("Just... just you. You know that."),
                _("One. You. Why are you asking me this in front of everyone?"),
            ])))
            $ Character(npc.Name, color=npc.color)(_tl(_("Ha! That's my girl.")))
        elif _bc_experienced:
            if _bc_player_sex:
                $ set_scene_expression(girl, "smirk")
                $ Say_Line(girl, _tl(renpy.random.choice([
                    _("Enough to know what I'm doing. Let's leave it at that."),
                    _("More than you'd be comfortable hearing, babe."),
                ])))
                $ set_scene_expression(girl, "shy", blush="1")
                $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([
                    _("...Wait, what? How many is 'enough'?"),
                    _("Okay, I'm starting to regret asking."),
                ])))
            else:
                $ set_scene_expression(girl, "neutral")
                $ Say_Line(girl, _tl(renpy.random.choice([
                    _("A few. I had a life before you, you know."),
                    _("Enough. I don't do the whole counting thing."),
                ])))
                $ Character(npc.Name, color=npc.color)(_tl(_("...Fair enough.")))
        elif _bc_bf_sex:
            $ set_scene_expression(girl, "shy", blush="1")
            $ Say_Line(girl, _tl(renpy.random.choice([
                _("Just you! Why would you even ask that?"),
                _("One, obviously. You. Stop making it weird."),
            ])))
            $ Character(npc.Name, color=npc.color)(_tl(_("Just checking! Can't be too careful.")))
            if _bc_player_sex:
                $ Narration(_tl(_("She avoids your eyes.")))
                python:
                    Change_NPC_Status(npc, "suspicion", 5)
                    print("[TOD_TRUTH] body_count: GF lied (has sex with player), suspicion +5")
        else:
            $ set_scene_expression(girl, "embarrassed", blush="1")
            $ Say_Line(girl, _tl(renpy.random.choice([
                _("We haven't even... you know. Why are you asking this here?"),
                _("Babe! You KNOW the answer. Stop it."),
            ])))
            $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([
                _("Haha, relax! I'm just messing with you."),
                _("Okay okay, sorry! Bad question."),
            ])))
    elif _bfag_tpick[0] == "fav_drink":
        python:
            _fd_tier = getattr(girl, "FavoriteDrink", None)
            _fd_names = {"low": _("beer"), "med": _("vodka"), "high": _("whiskey")}
            _fd_name = _fd_names.get(_fd_tier, _("something strong"))
        $ set_scene_expression(girl, "happy")
        $ Say_Line(girl, _tl(_("Hmm... I'd say %s. Nothing beats it after a long day.")) % _tl(_fd_name))
        $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([
            _("Ha! I should've known."),
            _("Good taste! I'll remember that."),
        ])))
        python:
            if hasattr(girl, "discover"):
                girl.discover("discovered_fav_drink")
            _fd_others = [g for g in _hangout_girls_list() if g.gid != girl.gid]
            for _fdg in _fd_others:
                _fdg.set_flag("knows_%s_fav_drink" % girl.gid)
            print("[TOD_TRUTH] %s revealed fav_drink=%s, discovered for player + %d girls" % (girl.gid, _fd_tier, len(_fd_others)))
    elif _bfag_tpick[0] == "fav_in_bed":
        python:
            _fib_fav = getattr(girl, "FavoriteAct", None)
            _fib_unlocked = getattr(girl, "_favorite_act_unlocked", False)
            _fib_names = {
                "kiss": _("kissing"), "massage": _("massages"),
                "hj": _("handjobs"), "bj": _("blowjobs"), "tj": _("titjobs"),
                "cowgirl": _("being on top"), "reverse_cowgirl": _("reverse cowgirl"),
                "doggy": _("doggy"), "laying_down": _("laying down"), "anal": _("anal"), "masturbate": _("touching myself"),
            }
            _fib_intense = _fib_fav in ("reverse_cowgirl", "doggy", "anal")
            _fib_mild = _fib_fav in ("kiss", "massage", "masturbate")
        if _fib_fav and _fib_unlocked:
            $ _fib_display = _tl(_fib_names.get(_fib_fav, _("what we do")))
            $ set_scene_expression(girl, "embarrassed", blush="2")
            $ Say_Line(girl, _tl(_("Okay, fine... I really like %s. There, I said it.")) % _fib_display)
            if _fib_intense:
                $ set_scene_expression(girl, "embarrassed", blush="2")
                $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([
                    _("...In front of EVERYONE?! You just said that out loud!"),
                    _("Whoa, babe! That's... wow. I did NOT expect that."),
                ])))
                $ Narration(_tl(_("The room goes quiet for a second. Everyone exchanges looks.")))
            elif _fib_mild:
                $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([
                    _("Ha! I had a feeling."),
                    _("That's sweet, actually. Good to know."),
                ])))
            else:
                $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([
                    _("Wait, really? Noted."),
                    _("Oh? I'll keep that in mind."),
                ])))
            python:
                if hasattr(girl, "discover"):
                    girl.discover("discovered_fav_act")
                _fib_others = [g for g in _hangout_girls_list() if g.gid != girl.gid]
                for _fibg in _fib_others:
                    _fibg.set_flag("knows_%s_fav_act" % girl.gid)
                    if _fib_intense:
                        set_scene_expression(_fibg, "surprised")
                print("[TOD_TRUTH] %s revealed fav_act=%s (intense=%s), discovered for player + %d girls" % (girl.gid, _fib_fav, _fib_intense, len(_fib_others)))
        elif _fib_fav:
            $ set_scene_expression(girl, "shy", blush="1")
            $ Say_Line(girl, _tl(renpy.random.choice([
                _("I... I don't know yet. We haven't done enough for me to pick a favorite."),
                _("That's private! And honestly, I'm still figuring that out."),
            ])))
            $ Character(npc.Name, color=npc.color)(_tl(_("Fair enough. We'll figure it out together.")))
        else:
            $ set_scene_expression(girl, "embarrassed", blush="1")
            $ Say_Line(girl, _tl(_("I don't really know... I haven't had enough experience to say.")))
            $ Character(npc.Name, color=npc.color)(_tl(_("That's okay, babe. No pressure.")))
    elif _bfag_tpick[0] == "open_rel":
        python:
            _or_cheater = girl.has_trait("cheater")
            _or_loyal = girl.has_trait("loyal")
            _or_attitude = getattr(girl, "CheatAttitude", 3)
            _or_player_sex = _girl_max_act(girl) > 0
        if _or_cheater or _or_attitude >= 6:
            $ set_scene_expression(girl, "smirk")
            $ Say_Line(girl, _tl(renpy.random.choice([
                _("I mean... I wouldn't rule it out. Life's too short to be closed off."),
                _("Honestly? If the right situation came up, maybe."),
            ])))
            $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([
                _("...Wait, are you serious?"),
                _("That's... not what I expected to hear."),
            ])))
            if _or_player_sex:
                $ Narration(_tl(_("She glances at you for just a second.")))
        elif _or_loyal or _or_attitude <= 2:
            $ set_scene_expression(girl, "serious")
            $ Say_Line(girl, _tl(renpy.random.choice([
                _("Absolutely not. When I'm with someone, I'm with THEM. Period."),
                _("No way. I don't share, and I don't want to be shared."),
            ])))
            $ Character(npc.Name, color=npc.color)(_tl(_("That's my girl.")))
        else:
            $ set_scene_expression(girl, "shy")
            $ Say_Line(girl, _tl(renpy.random.choice([
                _("I don't think so... but I guess you never really know until it happens."),
                _("Probably not? I mean, it sounds exciting in theory, but..."),
            ])))
            $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([
                _("Good answer. I think."),
                _("That wasn't exactly a 'no'..."),
            ])))
        python:
            _or_others = [g for g in _hangout_girls_list() if g.gid != girl.gid]
            if _or_cheater or _or_attitude >= 6:
                for _org in _or_others:
                    girl_learns_cheating(_org, girl)
                print("[TOD_TRUTH] %s revealed open_rel (cheater/high attitude), %d girls learned" % (girl.gid, len(_or_others)))
    return


# ============================================================
# BF asks a NON-GF girl: casual truth-or-dare, no intimacy.
# ============================================================
label _bf_ask_nongf_tod(npc, girl):
    $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([_("Your turn! Truth or dare?"), _("Alright, truth or dare?")])))

    python:
        _bfng_alc = tod_effective_alc(girl)
        _bfng_dare = renpy.random.random() < (0.3 + _bfng_alc * 0.04)

    if _bfng_dare:
        $ set_scene_expression(girl, "smirk")
        $ Say_Line(girl, _tl(renpy.random.choice([_("Dare! Bring it."), _("Dare. Let's see what you got.")])))

        python:
            _bfng_dtype = renpy.random.choice(["dance", "silly_face", "compliment", "impression"])

        if _bfng_dtype == "dance":
            $ Character(npc.Name, color=npc.color)(_tl(_("I dare you to dance right now. No music. Just go.")))
            $ set_scene_expression(girl, "bemused")
            $ Say_Line(girl, _tl(_("Seriously? Fine, watch this.")))
            $ Narration(_tl(_("%s gets up and does a surprisingly confident little dance.")) % girl.Name)
            $ set_scene_expression(girl, "happy")
            $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([
                _("Whoa, she's got moves!"),
                _("Okay, that was actually pretty good!"),
            ])))
        elif _bfng_dtype == "silly_face":
            $ Character(npc.Name, color=npc.color)(_tl(_("I dare you to make the ugliest face you can!")))
            $ set_scene_expression(girl, "serious")
            $ Say_Line(girl, _tl(_("You asked for it.")))
            $ Narration(_tl(_("%s scrunches up her face. Everyone bursts out laughing.")) % girl.Name)
            $ set_scene_expression(girl, "bemused")
            $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([
                _("That is genuinely terrifying."),
                _("I think you just won the game. Nobody's topping that."),
            ])))
        elif _bfng_dtype == "compliment":
            $ Character(npc.Name, color=npc.color)(_tl(_("I dare you to give everyone in this room a compliment. Right now.")))
            $ set_scene_expression(girl, "shy", blush="1")
            $ Say_Line(girl, _tl(_("Okay, fine. You're all... surprisingly tolerable. There, done.")))
            $ Character(npc.Name, color=npc.color)(_tl(_("'Tolerable'? That's the best you got? Ha!")))
            $ Narration(_tl(_("Everyone laughs.")))
        elif _bfng_dtype == "impression":
            call _tod_dare_impression(npc, girl) from _call_bfng_impression
        return

    $ set_scene_expression(girl, "neutral")
    $ Say_Line(girl, _tl(renpy.random.choice([_("Truth. Ask away."), _("Truth. Hit me.")])))

    python:
        _bfng_tpool = [
            ("fav_class", _("So, what's your favorite class this semester?")),
            ("embarrass", _("What's the most embarrassing thing that happened to you recently?")),
            ("party", _("What's the craziest party you've ever been to?")),
            ("roommate", _("Got any crazy roommate stories?")),
            ("never_do", _("What's something you'd never do, no matter how much someone dared you?")),
            ("craziest_guy", _("What's the craziest thing you've ever done with a guy?")),
        ]
        _bfng_tpick = renpy.random.choice(_bfng_tpool)
    $ Character(npc.Name, color=npc.color)(_tl(_bfng_tpick[1]))

    if _bfng_tpick[0] == "fav_class":
        $ set_scene_expression(girl, "neutral")
        $ Say_Line(girl, _tl(renpy.random.choice([
            _("Anything where the professor doesn't take attendance."),
            _("I actually like my psych class. Don't tell anyone."),
        ])))
        $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([
            _("Ha, fair enough. I respect that."),
            _("Nice. I can barely stay awake in mine."),
        ])))
    elif _bfng_tpick[0] == "embarrass":
        $ set_scene_expression(girl, "embarrassed", blush="1")
        $ Say_Line(girl, _tl(renpy.random.choice([
            _("I waved at someone who was waving at the person behind me. I wanted to disappear."),
            _("I sent a text complaining about someone... to that someone. I'm still not over it."),
        ])))
        $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([
            _("Oh no! That's brutal."),
            _("Ha! That's rough. I feel for you."),
        ])))
    elif _bfng_tpick[0] == "party":
        $ set_scene_expression(girl, "smirk")
        $ Say_Line(girl, _tl(renpy.random.choice([
            _("There was this one time where the cops showed up and everyone scattered. I hid behind a couch."),
            _("Someone brought a karaoke machine. I sang. It was bad. People still bring it up."),
        ])))
        $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([
            _("No way! That sounds insane!"),
            _("Okay, you HAVE to tell that full story sometime."),
        ])))
    elif _bfng_tpick[0] == "roommate":
        $ set_scene_expression(girl, "bemused")
        $ Say_Line(girl, _tl(renpy.random.choice([
            _("My roommate sleepwalks. I've found her in the kitchen at 4 AM more than once."),
            _("She once ate my labeled food and pretended she didn't know it was mine. It had my NAME on it."),
        ])))
        $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([
            _("That's wild. I'd lose my mind."),
            _("Seriously? People are something else, man."),
        ])))
    elif _bfng_tpick[0] == "never_do":
        $ set_scene_expression(girl, "serious")
        $ Say_Line(girl, _tl(renpy.random.choice([
            _("Skydiving. No way. My feet stay on the ground, thanks."),
            _("Eat anything with tentacles. I don't care how it's cooked."),
        ])))
        $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([
            _("That's your hard line? I respect it."),
            _("Okay, noted. Good to know your limits."),
        ])))
    elif _bfng_tpick[0] == "craziest_guy":
        python:
            _cg_acts = getattr(girl, "Sex_acts", {}) or {}
            _cg_anal = _cg_acts.get("anal", 0) > 0
            _cg_sex = girl_had_sex(girl)   # the "sex" act, never a position
            _cg_oral = any(_cg_acts.get(k, 0) > 0 for k in ("bj", "tj"))
            _cg_light = any(_cg_acts.get(k, 0) > 0 for k in ("hj", "rub", "kiss"))
            _cg_virgin = girl.has_trait("virgin")
            _cg_experienced = girl.has_trait("experienced")
            _cg_bf_gf = _bf_get_gf(npc)
        if _cg_anal:
            $ set_scene_expression(girl, "embarrassed", blush="2")
            $ Say_Line(girl, _tl(renpy.random.choice([
                _("I... let someone try the back door once. It was intense."),
                _("There was this one time... let's just say I tried something most girls won't."),
            ])))
            $ Narration(_tl(_("The room goes quiet for a second.")))
            if _cg_bf_gf is not None:
                $ set_scene_expression(_cg_bf_gf, "surprised")
                $ Say_Line(_cg_bf_gf, _tl(renpy.random.choice([
                    _("Wait, WHAT?"),
                    _("Okay, that's... more than I expected."),
                ])))
        elif _cg_sex:
            $ set_scene_expression(girl, "shy", blush="1")
            $ Say_Line(girl, _tl(renpy.random.choice([
                _("I've done... the full thing. More than once. That's all I'm saying."),
                _("Let's just say I'm not exactly innocent. But I'm not giving details."),
            ])))
            if _cg_bf_gf is not None:
                $ set_scene_expression(_cg_bf_gf, "serious")
                $ Say_Line(_cg_bf_gf, _tl(_("Hmm. Interesting.")))
        elif _cg_oral:
            $ set_scene_expression(girl, "embarrassed", blush="1")
            $ Say_Line(girl, _tl(renpy.random.choice([
                _("I've done some stuff... with my mouth. That's as far as I'm going with this."),
                _("More than kissing, less than everything. Use your imagination."),
            ])))
            $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([
                _("'With your mouth'? Okay, that's... more than I asked for."),
                _("Well, she went there. Respect for the honesty."),
            ])))
        elif _cg_light:
            $ set_scene_expression(girl, "shy")
            $ Say_Line(girl, _tl(renpy.random.choice([
                _("I mean... I've fooled around a little. Nothing too crazy."),
                _("Some hands went places they probably shouldn't have. That's it."),
            ])))
            $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([
                _("Ha, that's pretty tame. Nothing to be shy about."),
                _("'Probably shouldn't have,' she says. Classic."),
            ])))
        elif _cg_experienced:
            $ set_scene_expression(girl, "smirk")
            $ Say_Line(girl, _tl(renpy.random.choice([
                _("Enough to know my way around. I'll leave it at that."),
                _("A lady doesn't kiss and tell. But yeah, I've been around."),
            ])))
            $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([
                _("A woman of mystery. I respect it."),
                _("'Been around'? Okay, I won't push it."),
            ])))
        elif _cg_virgin:
            $ set_scene_expression(girl, "embarrassed", blush="1")
            $ Say_Line(girl, _tl(renpy.random.choice([
                _("Honestly? Not much. I'm kind of... waiting for the right person."),
                _("Nothing crazy. I'm not really that experienced."),
            ])))
            $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([
                _("That's cool. Nothing wrong with that."),
                _("Respect. Take your time."),
            ])))
        else:
            $ set_scene_expression(girl, "neutral")
            $ Say_Line(girl, _tl(renpy.random.choice([
                _("That's classified information. Next question."),
                _("Wouldn't you like to know? Maybe someday I'll tell."),
            ])))
            $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([
                _("Classified? Fair enough!"),
                _("Ooh, secretive. I like it."),
            ])))
        python:
            _cg_others = [g for g in _hangout_girls_list() if g.gid != girl.gid]
            if _cg_anal:
                for _cgg in _cg_others:
                    girl_learns_act(_cgg, girl, "anal")
            elif _cg_sex:
                for _cgg in _cg_others:
                    girl_learns_act(_cgg, girl, "sex")
            elif _cg_oral:
                for _cgg in _cg_others:
                    girl_learns_act(_cgg, girl, "bj")
            if _cg_virgin:
                for _cgg in _cg_others:
                    girl_learns_virgin(_cgg, girl)
            print("[TOD_TRUTH] %s revealed craziest_guy: anal=%s sex=%s oral=%s light=%s virgin=%s exp=%s" % (girl.gid, _cg_anal, _cg_sex, _cg_oral, _cg_light, _cg_virgin, _cg_experienced))
    return


# ============================================================
# BF asks the PLAYER a guy-talk truth. The player picks the answer;
# cocky answers cost friendship but draw his girl's eye, humble ones
# earn respect.
# ============================================================
label _bf_ask_player_truth(npc, key):
    python:
        _bap = _BF_ASK_PLAYER[key]
        _bap_girl = _bf_get_gf(npc)
        _bap_menu = [(_tl(_o["a"]), _i) for _i, _o in enumerate(_bap["options"])]
    $ Character(npc.Name, color=npc.color)(_tl(_bap["q"]))
    $ _bap_pick = renpy.display_menu(_bap_menu)
    python:
        _bap_opt = _bap["options"][_bap_pick]
        _bap_fx = dict(_bap_opt.get("fx", {}))
        _bap_girl_line = _bap_opt.get("girl")
        # The girl reacts to the CONTENT of the answer: a matching trait adds
        # Love/Obed and overrides her line (e.g. "finish inside" + cum_slut).
        _bap_hit = None
        if _bap_girl is not None:
            for _tk, _tv in _bap_opt.get("traits", {}).items():
                if _bap_girl.has_trait(_tk):
                    _bap_hit = _tv
                    break
        if _bap_hit:
            for _sk, _sv in _bap_hit.get("fx", {}).items():
                _bap_fx[_sk] = _bap_fx.get(_sk, 0) + _sv
            if _bap_hit.get("line"):
                _bap_girl_line = _bap_hit["line"]
        # Determine narration source: trait narr overrides girl_narr.
        _bap_narr = None
        if _bap_hit:
            _bap_narr = _bap_hit.get("narr")
        if not _bap_narr:
            _bap_narr = _bap_opt.get("girl_narr")
    $ Say_Player(_tl(_bap_opt["a"]))
    python:
        _bf_apply(
            npc, _bap_girl,
            fr=_bap_fx.get("fr", 0), susp=_bap_fx.get("susp", 0),
            gobed=_bap_fx.get("gobed", 0), glove=_bap_fx.get("glove", 0))
    if (_bap_girl_line or _bap_narr) and _bap_girl is not None:
        if _bap_hit is not None:
            $ set_scene_expression(_bap_girl, "shy", blush="1")
        else:
            $ set_scene_expression(_bap_girl, "bemused")
        if _bap_narr:
            $ renpy.say(None, _tl(_bap_narr))
        if _bap_girl_line:
            $ Say_Line(_bap_girl, _tl(_bap_girl_line))
        python:
            _bap_cover = (
                _bap_hit is not None
                and _bap_hit.get("line")
                and not _npc_is_ntr(npc)
                and _bap_hit.get("fx", {}).get("glove", 0) >= 0)
        if _bap_cover:
            $ Character(npc.Name, color=npc.color)(_tl(_("Wait... what did you just say?")))
            $ set_scene_expression(_bap_girl, "happy")
            $ Narration(_("She laughs."))
            $ Say_Line(_bap_girl, _tl(_("Nothing, babe! Just kidding.")))
    if _bap_opt.get("reply_narr"):
        $ renpy.say(None, _format_partner_line(_bap_girl, _bap_opt["reply_narr"]))
    $ Character(npc.Name, color=npc.color)(_tl(_bap_opt["reply"]))
    $ tod_mark_used("bap_" + key)
    return


# ============================================================
# BF DARES THE PLAYER (bf spun, landed on the player). Dance / sing in another
# language; and -- ONLY if he's an NTR lover -- kiss his girl (cheek or mouth).
# The kiss reaction depends on whether the NTR is already out in the open:
# not yet (girl._ntr_boundary_discovered False) = both are caught off guard;
# already known = routine, she's game.
# ============================================================
label _bf_dare_player(npc, girl):
    python:
        _bdp_pool = ["dance", "sing", "arm_wrestle", "pushups", "show_phone"]
        if _npc_is_ntr(npc) and getattr(girl, "_ntr_boundary_discovered", False):
            _bdp_pool += ["kiss_cheek", "kiss_mouth"]
        _bdp = renpy.random.choice(_bdp_pool)

    if _bdp == "dance":
        $ Character(npc.Name, color=npc.color)(_tl(_("Alright, YOUR turn. I dare you to bust out a dance. Right here, right now. Go!")))
        menu:
            "Accept":
                $ Narration(_("You get up and throw down the most ridiculous moves you can manage. The whole room loses it."))
                $ Character(npc.Name, color=npc.color)(_tl(_("HA! Okay, okay, that was actually incredible.")))
                $ _bf_apply(npc, girl, fr=4)
            "Refuse (drink 2 doses as penalty)":
                $ tod_drink_player(2)
                $ Narration(_("You down your penalty drinks. Your head swims a little."))
                $ Character(npc.Name, color=npc.color)(_tl(_("Ha! Can't handle a little dancing?")))
        return

    if _bdp == "sing":
        $ Character(npc.Name, color=npc.color)(_tl(_("Dare: sing something. In another language. Doesn't matter which. Let's hear it!")))
        menu:
            "Accept":
                $ Narration(_("You belt out the only foreign lyrics you half-remember, butchering every single word."))
                $ set_scene_expression(girl, "bemused")
                $ Say_Line(girl, _tl(_("That was... something. I have no clue what you just said.")))
                $ _bf_apply(npc, girl, fr=4)
            "Refuse (drink 2 doses as penalty)":
                $ tod_drink_player(2)
                $ Narration(_("You down your penalty drinks. Your head swims a little."))
                $ Character(npc.Name, color=npc.color)(_tl(_("Too shy to sing? Come on, man!")))
        return

    if _bdp == "arm_wrestle":
        call _tod_dare_arm_wrestle(npc, girl, "bf") from _call_bdp_arm_wrestle
        return

    if _bdp == "pushups":
        $ Character(npc.Name, color=npc.color)(_tl(_("I dare you to drop and give us twenty push-ups. Right now. Let's see what you're made of.")))
        menu:
            "Accept":
                python:
                    _pu_str = Player._get_energy_max()
                    _pu_girls = _hangout_girls_list()
                    print("[PUSHUPS] player strength=%d" % _pu_str)
                if _pu_str >= 4:
                    $ Narration(_("You drop down and knock out twenty push-ups without breaking a sweat. You keep going just to show off."))
                    $ Character(npc.Name, color=npc.color)(_tl(_("...Okay, you can stop now. We get it.")))
                    python:
                        for _pug in _pu_girls:
                            set_scene_expression(_pug, "surprised")
                            Change_Status(_pug, "Obed", 10)
                    if girl is not None:
                        $ Say_Line(girl, _tl(renpy.random.choice([
                            _("That was... really hot, actually."),
                            _("Okay, I'm impressed."),
                        ])))
                elif _pu_str == 3:
                    $ Narration(_("You push out twenty with some effort. Not graceful, but you get it done."))
                    $ Character(npc.Name, color=npc.color)(_tl(_("Not bad, man. Not bad at all.")))
                    python:
                        for _pug in _pu_girls:
                            set_scene_expression(_pug, "neutral")
                            Change_Status(_pug, "Obed", 5)
                else:
                    $ Narration(_("You struggle through five push-ups before your arms give out. You collapse on the floor."))
                    $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([
                        _("Dude... that was painful to watch."),
                        _("Five?! That's all you got? Ha!"),
                    ])))
                    python:
                        for _pug in _pu_girls:
                            set_scene_expression(_pug, "bemused")
                            Change_Status(_pug, "Obed", -8)
                    if girl is not None:
                        $ Say_Line(girl, _tl(renpy.random.choice([
                            _("That was... an attempt."),
                            _("Maybe hit the gym sometime?"),
                        ])))
            "Refuse (drink 2 doses as penalty)":
                $ tod_drink_player(2)
                $ Narration(_("You down your penalty drinks. Your head swims a little."))
                $ Character(npc.Name, color=npc.color)(_tl(_("Too weak to do push-ups? Come on!")))
        return

    if _bdp == "show_phone":
        $ Character(npc.Name, color=npc.color)(_tl(_("I dare you to show us your phone. Gallery, messages, everything. Let's see what you're hiding.")))
        menu:
            "Accept":
                python:
                    _psp_vids = getattr(store.Player, "recorded_videos", [])
                    _psp_has_vids = len(_psp_vids) > 0
                    _psp_girls = _hangout_girls_list()
                    print("[SHOW_PHONE_P] player vids=%d" % len(_psp_vids))
                $ Narration(_format_partner_line(girl, _("You hand over your phone. %(Pp)s starts scrolling through your gallery.")))
                if _psp_has_vids:
                    $ Character(npc.Name, color=npc.color)(_tl(_("What the... are these videos? Dude, are you filming girls?")))
                    $ Say_Player(_("It's just... personal stuff. Give it back."))
                    $ Character(npc.Name, color=npc.color)(_tl(_("I can't tell who's in them, but damn. You've been busy.")))
                    $ Narration(_("You snatch your phone back. Some of the girls shift uncomfortably."))
                    python:
                        _bf_apply(npc, girl, susp=15, fr=-10)
                        for _pspg in _psp_girls:
                            _pspg_in = any(v.get("girl_gid") == _pspg.gid for v in _psp_vids)
                            if _pspg_in:
                                set_scene_expression(_pspg, "embarrassed", blush="1")
                            else:
                                set_scene_expression(_pspg, "surprised")
                else:
                    $ Character(npc.Name, color=npc.color)(_tl(_("Memes. More memes. A grocery list. Dude, you're boring.")))
                    $ Narration(_("Everyone laughs."))
                    $ _bf_apply(npc, girl, fr=5)
            "Refuse (drink 2 doses as penalty)":
                $ tod_drink_player(2)
                $ Narration(_("You down your penalty drinks. Your head swims a little."))
                $ Character(npc.Name, color=npc.color)(_tl(_("What are you hiding in there? Now I'm REALLY curious.")))
                $ _bf_apply(npc, girl, susp=5)
        return

    call _bf_dare_player_kiss(npc, girl, _bdp) from _call_bf_dare_player_kiss
    return


label _bf_dare_player_kiss(npc, girl, mode):
    python:
        _bpk_mouth = (mode == "kiss_mouth")
        _bpk_known = getattr(girl, "_ntr_boundary_discovered", False)
        _bpk_label = _tl(_("Kiss her on the mouth.")) if _bpk_mouth else _tl(_("Kiss her on the cheek."))

    if _bpk_mouth:
        $ Character(npc.Name, color=npc.color)(_tl(_("Here's a real one: kiss my girlfriend. On the mouth. Go on, I dare you.")))
    else:
        $ Character(npc.Name, color=npc.color)(_tl(_("I dare you to kiss my girl. Just the cheek. What, you scared?")))

    if not _bpk_known:
        # First time -- the NTR isn't out in the open yet, so both are stunned.
        $ set_scene_expression(girl, "surprised")
        $ Say_Line(girl, _tl(renpy.random.choice([
            _("Wait, WHAT? You're seriously okay with this?"),
            _("Babe... you actually want him to? In front of you?"),
        ])))
        $ Say_Player(_format_npc_line(npc, _("...Is %(pp)s serious right now?")))
        $ Character(npc.Name, color=npc.color)(_tl(_("Dead serious. It's just a game. Do it.")))
    else:
        # NTR already established -- routine, she plays along.
        $ set_scene_expression(girl, "shy", blush="1")
        $ Say_Line(girl, _format_npc_line(npc, _("You heard %(po)s.")))

    $ _bpk_choice = renpy.display_menu([(_bpk_label, "do"), (_tl(_("Not like this")), "no")])
    if _bpk_choice == "no":
        $ Say_Player(_tl(_("...Nah. Not like this.")))
        $ Character(npc.Name, color=npc.color)(_tl(_("Suit yourself. The offer stands.")))
        return

    if _bpk_mouth:
        $ set_scene_expression(girl, "embarrassed", blush="2")
        call KISS_Launch(girl) from _call_KISS_Launch_bf_dare
        $ Narration(_tl(_("You lean in and kiss her on the mouth. She melts into it a second longer than she should, %s watching every moment.")) % npc.Name)
        call KISS_Smooch(girl) from _call_KISS_Smooch_bf_dare
        call KISS_End(girl) from _call_KISS_End_bf_dare
        $ set_girl_sprite(girl.gid, pose="standing", at_list=[_hangout_pos_for(girl)])
        python:
            Change_Status(girl, "Lust", 10)
            if callable(globals().get("_ntr_increase_boundary_bar")):
                _ntr_increase_boundary_bar(npc, girl, 15)
            _bf_apply(npc, girl, gobed=5)
        if not _bpk_known:
            $ Say_Line(girl, _tl(_("That was not supposed to feel like that.")))
        $ Character(npc.Name, color=npc.color)(_tl(_("...Damn. That was hot. Do it again sometime.")))
    else:
        $ set_scene_expression(girl, "shy", blush="2")
        $ Narration(_tl(_("You lean in and plant a kiss on her cheek. She goes a little pink, and %s just grins.")) % npc.Name)
        python:
            Change_Status(girl, "Lust", 4)
            if callable(globals().get("_ntr_increase_boundary_bar")):
                _ntr_increase_boundary_bar(npc, girl, 6)
        $ Say_Line(girl, _tl(_("Okay. That was kind of sweet, honestly.")))
    return


# ============================================================
# BF's tame dares (funny dance / silly face / run to campus). He never
# strips; a refused dare makes him drink DOUBLE instead.
# ============================================================
label _bf_do_dare(npc, girl, asker=None):
    python:
        _bfd = renpy.random.choice(_BF_DARES)
        if _bf_is_gf(npc, girl) and _npc_is_ntr(npc) and getattr(girl, "_ntr_boundary_discovered", False) and renpy.random.random() < 0.25:
            _bfd = "kiss_player"

    if _bfd == "kiss_player":
        call _bf_ntr_kiss_player(npc, girl) from _call_bf_ntr_kiss_player
        return

    if _bfd == "run_campus":
        if asker is not None:
            $ _bf_say(asker, _tl(_("I dare you to sprint to campus and back!")))
        call _bf_dare_run_campus(npc, girl) from _call_bf_dare_run_campus
        return

    if _bfd == "dance":
        if asker is not None:
            $ _bf_say(asker, _tl(_("I dare you to dance right now!")))
        $ Character(npc.Name, color=npc.color)(_tl(_("Dare? Fine. Watch and learn.")))
        $ Narration(_tl(_("%s stands up and does the most ridiculous dance you've ever seen.")) % npc.Name)
        $ Say_Player(_("...I have no words."))
        if girl is not None:
            $ set_scene_expression(girl, "bemused")
            $ Say_Line(girl, _tl(renpy.random.choice([_("Oh my god!"), _("Babe, stop!")])))
    elif _bfd == "silly_face":
        if asker is not None:
            $ _bf_say(asker, _tl(_("I dare you to make the silliest face you can!")))
        $ Character(npc.Name, color=npc.color)(_tl(_("A silly face? That's it? Easy.")))
        python:
            _bfd_poss = _tr("her_poss") if npc.gender == "female" else _tr("his")
        $ Narration(_tl(_("{n} crosses {p} eyes and puffs {p} cheeks. Everyone loses it.")).format(n=npc.Name, p=_bfd_poss))
        if girl is not None:
            $ set_scene_expression(girl, "bemused")
            $ Say_Line(girl, _tl(renpy.random.choice([_("You look so stupid!"), _("That is terrifying.")])))
    elif _bfd == "arm_wrestle":
        if asker is not None:
            $ _bf_say(asker, _format_npc_line(npc, _("I dare you to arm wrestle %(po)s!")))
        call _tod_dare_arm_wrestle(npc, girl, "player") from _call_bfd_arm_wrestle
        return
    elif _bfd == "show_phone":
        if asker is not None:
            $ _bf_say(asker, _tl(_("I dare you to show us what's on your phone!")))
        call _tod_dare_show_phone(npc, girl, "bf") from _call_bfd_show_phone
        return
    elif _bfd == "show_dick":
        if asker is not None:
            $ _bf_say(asker, _tl(_("I dare you to drop your pants. Right now. Show us what you got!")))
        else:
            $ Say_Player(_("I dare you to drop your pants. Show everyone what you got!"))
        $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([
            _("WHAT?! No. Absolutely not. Not happening."),
            _("Are you insane? No way in hell!"),
            _("Yeah, that's a hard no. I'll take the drink."),
        ])))
        $ Narration(_tl(_("%s grabs the bottle and pours a double.")) % npc.Name)
        $ tod_drink(npc, 2)
        python:
            _bfd_girls = _hangout_girls_list()
            for _bfd_g in _bfd_girls:
                if _bf_is_gf(npc, _bfd_g):
                    set_scene_expression(_bfd_g, "embarrassed", blush="2")
                else:
                    set_scene_expression(_bfd_g, "bemused")
        if girl is not None and _bf_is_gf(npc, girl):
            $ Say_Line(girl, _tl(renpy.random.choice([
                _("Oh my god, babe, PLEASE don't!"),
                _("Thank god. I would have died."),
            ])))
        elif girl is not None:
            $ Say_Line(girl, _tl(renpy.random.choice([
                _("Aww, come on! It was just a dare!"),
                _("That face was priceless!"),
            ])))
        $ _bf_apply(npc, girl, fr=-3)
        if tod_rolls_sick(npc):
            if len(_hangout_girls_list()) == 1:
                call _npc_pass_out_1girl_event from _call_npc_po_1g_showdick
            else:
                call _npc_pass_out_event from _call_npc_po_showdick
        return
    elif _bfd == "show_history":
        if asker is not None:
            $ _bf_say(asker, _tl(_("I dare you to show us your browser history. ALL of it!")))
        else:
            $ Say_Player(_("I dare you to show us your browser history. No clearing it first!"))
        $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([
            _("No. Absolutely not. There are things in there that should NEVER see the light of day."),
            _("You want me to show... no. NO. I choose death. Give me the bottle."),
            _("I'd rather drink the whole bottle than show you people THAT."),
        ])))
        $ Narration(_tl(_("Everyone laughs as %s desperately reaches for the bottle.")) % npc.Name)
        $ tod_drink(npc, 2)
        if girl is not None and _bf_is_gf(npc, girl):
            $ set_scene_expression(girl, "bemused")
            $ Say_Line(girl, _tl(renpy.random.choice([
                _("What are you looking at that's so bad?!"),
                _("Now I REALLY want to check your phone later..."),
            ])))
            $ Character(npc.Name, color=npc.color)(_tl(_("BABE. It's nothing weird, okay?! Just... a LOT of gaming forums.")))
        elif girl is not None:
            $ set_scene_expression(girl, "happy")
            $ Say_Line(girl, _tl(renpy.random.choice([
                _("That reaction says EVERYTHING."),
                _("We all know what's in there."),
            ])))
        $ _bf_apply(npc, girl, fr=-2)
        if tod_rolls_sick(npc):
            if len(_hangout_girls_list()) == 1:
                call _npc_pass_out_1girl_event from _call_npc_po_1g_history
            else:
                call _npc_pass_out_event from _call_npc_po_history
        return
    return


# ============================================================
# Run-to-campus dare: he sprints off-screen and comes back winded IF he's
# drunk / friendly enough (_bf_run_campus_accepts). Otherwise he refuses and
# drinks double. He never strips.
# ============================================================
transform hangout_slide_out_right:
    xalign 0.90
    yalign 2.0
    easeout 0.45 xalign 1.7

transform hangout_slide_in_right:
    xalign 1.7
    yalign 2.0
    easein 0.45 xalign 0.90

transform hangout_slide_out_left:
    xalign 0.35
    yalign 2.0
    easeout 0.45 xalign -0.7

transform hangout_slide_in_left:
    xalign -0.7
    yalign 2.0
    easein 0.45 xalign 0.35

label _bf_dare_run_campus(npc, girl):
    $ Character(npc.Name, color=npc.color)(_tl(_("Run to campus and back? You're kidding me.")))
    if _bf_run_campus_accepts(npc):
        $ Character(npc.Name, color=npc.color)(_tl(_("...You know what? Screw it. Somebody time me!")))
        python:
            _npc_x = _hangout_npc_xalign()
            _slide_out = hangout_slide_out_left if _npc_x < 0.5 else hangout_slide_out_right
            _slide_in = hangout_slide_in_left if _npc_x < 0.5 else hangout_slide_in_right
        $ npc.show_sprite(_slide_out)
        pause 0.5
        $ npc.hide_sprite()
        python:
            _brc_pp = _tr("she") if npc.gender == "female" else _tr("he")
            _brc_pp2 = _tr("She") if npc.gender == "female" else _tr("He")
        $ Narration(_tl(_("{n} bolts out the door. A few minutes later {pp} staggers back in, red-faced and gasping for air.")).format(n=npc.Name, pp=_brc_pp))
        $ npc.show_sprite(_slide_in)
        pause 0.5
        $ Character(npc.Name, color=npc.color)(_tl(_("Done. You happy now?")))
        $ _bf_apply(npc, girl, fr=5)
        if girl is not None:
            $ set_scene_expression(girl, "bemused")
            $ Say_Line(girl, _tl(renpy.random.choice([_("That was incredible."), _("I can't believe that actually happened!")])))
    else:
        $ Character(npc.Name, color=npc.color)(_tl(_("Yeah, no. I'm not doing that. I'll drink instead.")))
        $ Narration(_tl(_("%s downs a double instead of running.")) % npc.Name)
        $ tod_drink(npc, 2)
        if girl is not None:
            $ set_scene_expression(girl, "serious")
            $ Say_Line(girl, _format_npc_line(npc, renpy.random.choice([_("Of course %(pp)s didn't do it."), _("Typical.")])))
        if tod_rolls_sick(npc):
            if len(_hangout_girls_list()) == 1:
                call _npc_pass_out_1girl_event from _call_npc_po_1g_dare
            else:
                call _npc_pass_out_event from _call_npc_po_dare
    return


# ============================================================
# NTR-lover special: he dares the girl to kiss the PLAYER (she hesitates)
# ============================================================
label _bf_ntr_kiss_player(npc, girl):
    $ Character(npc.Name, color=npc.color)(_tl(_("You know what I dare you to do? Kiss her. Yeah, her. Right now, in front of me.")))
    $ set_scene_expression(girl, "surprised")
    $ Say_Line(girl, _tl(renpy.random.choice([
        _("Wait... you WANT me to? In front of you?"),
        _("Are you serious right now? You're okay with this?"),
    ])))
    $ Narration(_tl(_("She hesitates, glancing between you and %s.")) % npc.Name)
    menu:
        "Kiss her":
            call KISS_Launch(girl) from _call_KISS_Launch_bf_ntr
            $ Narration(_tl(_("You lean in. She freezes for a second, then kisses you, %s watching every second of it.")) % npc.Name)
            call KISS_Smooch(girl) from _call_KISS_Smooch_bf_ntr
            call KISS_End(girl) from _call_KISS_End_bf_ntr
            $ set_girl_sprite(girl.gid, pose="standing", at_list=[_hangout_pos_for(girl)])
            python:
                Change_Status(girl, "Lust", 8)
                if callable(globals().get("Change_NPC_Status")):
                    Change_NPC_Status(npc, "suspicion", 5)
                if callable(globals().get("_ntr_increase_boundary_bar")):
                    _ntr_increase_boundary_bar(npc, girl, 12)
            $ Character(npc.Name, color=npc.color)(_tl(_("...God, that was hot. Do that again sometime.")))
        "Not like this":
            $ Say_Player(_("...Nah. Not like this."))
            $ Character(npc.Name, color=npc.color)(_tl(_("Suit yourself. The offer stands.")))
    return


# ============================================================
# NTR-lover / probing: he asks his girl what she's done with OTHER guys.
# Player reacts depending on NTR / how far she's actually gone.
# ============================================================
label _bf_ask_girl_other_guy(npc, girl):
    $ Character(npc.Name, color=npc.color)(_tl(_("Honest question for the group, babe: what's the naughtiest thing you've done with someone who ISN'T me?")))
    python:
        _bfog_hist = _girl_max_act(girl)
        _bfog_ntr = _npc_is_ntr(npc) and getattr(girl, "_ntr_boundary_discovered", False)
    if _bfog_hist <= 0:
        $ set_scene_expression(girl, "surprised")
        $ Say_Line(girl, _tl(_("W-what? Nothing! You're the only one!")))
        $ Character(npc.Name, color=npc.color)(_tl(_("Ha. Good answer.")))
        $ _bf_apply(npc, girl, fr=6)
        return
    $ set_scene_expression(girl, "embarrassed", blush="1")
    python:
        _bfog_picks = [
            (_("She avoids your eyes."), _("I... um... there was this one guy. We did... a lot.")),
            (_("She bites her lip and glances at you."), _("More than I should admit with you sitting right here.")),
        ]
        _bfog_narr, _bfog_line = renpy.random.choice(_bfog_picks)
    $ Narration(_tl(_bfog_narr))
    $ Say_Line(girl, _tl(_bfog_line))
    if _bfog_ntr:
        $ Character(npc.Name, color=npc.color)(_tl(_("Mmm. Tell us more. Don't leave out the details.")))
        python:
            Change_Status(girl, "Lust", 5)
            if callable(globals().get("_ntr_increase_boundary_bar")):
                _ntr_increase_boundary_bar(npc, girl, 8)
            _bf_apply(npc, girl, fr=4)
    else:
        $ Narration(_format_npc_line(npc, _("%(Poss)s jaw tightens.")))
        $ Character(npc.Name, color=npc.color)(_tl(_("...Wait. How much is 'a lot'?")))
        python:
            if callable(globals().get("Change_NPC_Status")):
                Change_NPC_Status(npc, "suspicion", 15)
            _bf_apply(npc, girl, fr=-5)
    return


# ============================================================
# BF WATCHES the PLAYER interrogate his girl with a truth.
# Same questions the player always asks -- but now the boyfriend is
# sitting right there. He reacts by trait: NTR gets turned on, proud
# gets jealous/possessive, others get uneasy. If she strips rather than
# answer, that's the loudest reaction of all.
# ============================================================
init python:

    _BF_WATCH_LEWD = {
        "ntr": [
            (_("%(Pp)s leans in, way too into it."), _("Mmm, listen to her answer that. Don't stop on my account.")),
            (None, _("God, hearing her say that stuff... keep the questions coming.")),
            (_("%(Pp)s grins at you."), _("That's my girl. Ask her something dirtier.")),
        ],
        "proud": [
            (None, _("Hey. Watch what you're asking my girl, alright?")),
            (_("%(Poss)s jaw tightens."), _("That's a bit personal for a game, don't you think?")),
            (None, _("Careful. That's MY girlfriend you're grilling.")),
        ],
        "friendly": [
            (None, _("Ha, bold question. She can handle herself, though.")),
            (_("%(Pp)s chuckles, but keeps one eye on her."), _("Easy there.")),
        ],
        "uneasy": [
            (_("%(Pp)s shifts in %(poss)s seat."), _("...That's getting pretty personal.")),
            (None, _("Huh. Didn't expect the game to go there.")),
            (_("%(Pp)s watches her answer a little too closely, saying nothing."), None),
        ],
    }

    _BF_WATCH_LEWD_GIRL = {
        "ntr": [
            (_("She bites her lip."), _("You're enjoying this way too much, babe.")),
            (None, _("God, you actually LIKE watching this, don't you?")),
        ],
        "proud": [
            (_("She pats %(poss)s arm."), _("Relax, it's just a game.")),
            (None, _("Babe, chill. It doesn't mean anything.")),
        ],
    }

    _BF_WATCH_SAFE = {
        "ntr": [
            (_("%(Pp)s watches her light up talking to you, and just smiles."), None),
        ],
        "proud": [
            (None, _("Ha. She's cute when she gets going, isn't she?")),
        ],
        "neutral": [
            (_("%(Pp)s nods along, relaxed."), None),
        ],
    }

    _BF_WATCH_STRIP = {
        "ntr": [
            (_("%(Pp)s stares, riveted."), _("Whoa... she'd rather strip than answer HIM? This game is amazing.")),
        ],
        "proud": [
            (None, _("Hey! HEY! Put that back on, that is NOT for him to see!")),
        ],
        "friendly": [
            (_("%(Pp)s glances away, awkward."), _("Uh... babe, you sure about that?")),
        ],
        "uneasy": [
            (_("%(Pp)s goes quiet."), _("...I really did not expect to see that tonight.")),
        ],
    }

    def _bf_watch_key(npc, girl, lewd):
        """Which reaction pool the watching boyfriend uses.
        NTR pool only when boundary is discovered (player knows he's into it)."""
        if _npc_is_ntr(npc) and getattr(girl, "_ntr_boundary_discovered", False):
            return "ntr"
        if npc.has_trait("proud"):
            return "proud"
        if not lewd:
            return "neutral"
        if _bf_friend_tier(npc) == "friendly":
            return "friendly"
        return "uneasy"

    def _bf_content_reaction(npc, girl, q_label):
        """Content-specific bf reaction when watching the girl answer a truth.
        Returns (npc_line, fx_dict, girl_react) or None.
        fx_dict may include 'narr' for narrator line after NPC speaks.
        girl_react is None or dict with line/expr/blush keys."""
        if npc is None or girl is None or not q_label:
            return None
        _is_ntr = _npc_is_ntr(npc)
        _susp = getattr(npc, "suspicion", 0)
        bfh = getattr(girl, "bf_history", {}) or {}

        if q_label == "Ever recorded an intimate video?":
            _vids = [v for v in getattr(store.Player, "recorded_videos", []) if v.get("girl_gid") == girl.gid]
            if _vids and _is_ntr and getattr(girl, "_ntr_boundary_discovered", False):
                return (
                    _("A video? Tell me more."),
                    {"fr": 4, "narr": _("%(Pp)s leans forward, eyes wide.")},
                    {"expr": "smirk", "blush": "1",
                     "line": _("Oh, there are videos. Really good ones, too.")})
            if _vids:
                return (
                    _("A video? But we never recorded any..."),
                    {"susp": 5, "narr": _("%(Pp)s goes silent.")},
                    {"expr": "worried", "blush": "1",
                     "line": _("It was nothing serious, just... messing around.")})

        if q_label == "Ever cheated on someone?":
            _cheated = getattr(girl, "GirlCheatCount", 0) > 0 or getattr(girl, "CheatMaxTier", 0) > 0
            if _cheated and not _is_ntr:
                if _susp < 30:
                    return (
                        _("Cheated?! On who? On ME?!"),
                        {"susp": 30, "fr": -12, "narr": _("%(Pp)s stands up from %(poss)s seat, then sits back down. %(Poss)s hands are trembling.")},
                        {"expr": "worried",
                         "line": _("No! Not on you! It was... before. Someone else.")})
                else:
                    return (
                        _("I fucking knew it. I KNEW something was going on."),
                        {"susp": 20, "fr": -8, "narr": _("%(Poss)s voice is low and dangerous. The room goes silent.")},
                        {"expr": "sad",
                         "line": _("Please... not here. I'll explain everything later, I promise.")})
            if _cheated and _is_ntr:
                if getattr(girl, "_ntr_boundary_discovered", False):
                    return (
                        _("Go on. Don't stop there."),
                        {"fr": 4, "narr": _("%(Pp)s shifts in %(poss)s seat, breathing harder.")},
                        {"expr": "smirk", "blush": "1",
                         "line": _("Maybe I did. Maybe I enjoyed every second.")})
                else:
                    return (
                        _("Cheated?! On who? On ME?!"),
                        {"susp": 30, "fr": -12, "narr": _("%(Pp)s stands up from %(poss)s seat, then sits back down. %(Poss)s hands are trembling.")},
                        {"expr": "worried",
                         "line": _("No! Not on you! It was... before. Someone else.")})

        if q_label == "Has anyone ever finished inside you?":
            _creampied = getattr(girl, "CreampieCounts", 0) > 0
            _virgin_claim = getattr(girl, "virginity_taken_by_player", False) or not bfh.get("sex")
            if _creampied and not _is_ntr and _susp < 50:
                if _virgin_claim and not bfh.get("creampie"):
                    return (
                        _("Wait... you told me you were a virgin. How... how is that even possible?"),
                        {"susp": 40, "fr": -15, "narr": _("The color drains from %(poss)s face. %(Pp)s stares at her, waiting for an explanation that makes sense.")},
                        {"expr": "worried", "blush": "2",
                         "line": _("I... it's not what you think. Please, can we not do this here?")})
                elif not bfh.get("creampie"):
                    return (
                        _("Inside?! WHO finished inside you? Because it sure as hell wasn't me."),
                        {"susp": 35, "fr": -12, "narr": _("%(Poss)s hands are shaking. %(Pp)s looks like %(pp)s might flip the table.")},
                        {"expr": "worried", "blush": "2",
                         "line": _("It was... a mistake. It only happened once, I swear.")})
                else:
                    return (
                        _("Better be talking about me."),
                        {"susp": 10, "narr": _("%(Pp)s shifts uncomfortably.")},
                        {"expr": "shy", "blush": "1",
                         "line": _("Of course it's you. Who else would it be?")})
            if _creampied and _is_ntr:
                if getattr(girl, "_ntr_boundary_discovered", False):
                    return (
                        _("Someone finished inside you?"),
                        {"fr": 4, "narr": _("%(Poss)s eyes go wide.")},
                        {"expr": "smirk", "blush": "2",
                         "line": _("More than once. And I loved every second.") if getattr(girl, "CreampieCounts", 0) > 1
                                 else _("Someone did. And I loved every second.")})
                else:
                    if _virgin_claim:
                        return (
                            _("Inside you? But... you told me you were a virgin. What the hell is going on?"),
                            {"susp": 35, "fr": -10, "narr": _("%(Poss)s face is a mess of confusion and something else %(pp)s can't quite name.")},
                            {"expr": "worried", "blush": "2",
                             "line": _("I... it's complicated. Can we please just move on?")})
                    else:
                        return (
                            _("Someone finished inside you? When? With who?"),
                            {"susp": 25, "fr": -5, "narr": _("%(Pp)s shifts in %(poss)s seat, clearly bothered, but something in %(poss)s eyes says %(pp)s wants to hear more.")},
                            {"expr": "worried", "blush": "2",
                             "line": _("It happened once. It was an accident. Drop it.")})

        if q_label == "Do you prefer going raw or using a condom?":
            _raw = getattr(girl, "raw_sex_count", 0) > 0
            if _raw and not _is_ntr:
                if not bfh.get("sex_raw"):
                    return (
                        _("Raw?! You ALWAYS make me wear a condom. Every single time. So who exactly are you going raw with?"),
                        {"susp": 25, "fr": -8, "narr": _("%(Poss)s voice cuts through the room. Everyone goes quiet.")},
                        {"expr": "worried", "blush": "2",
                         "line": _("It's not... I was just answering hypothetically! It's a game!")})

        if q_label == "Who was your first time with?":
            if getattr(girl, "virginity_taken_by_player", False) and not _is_ntr:
                return (
                    _("Hold on. You told me I was your first. You TOLD me that. Was that a lie?"),
                    {"susp": 35, "fr": -12, "narr": _("%(Poss)s voice breaks. Not angry anymore. Just hurt.")},
                    {"expr": "sad",
                     "line": _("You were! I mean... it's complicated. Please, not here.")})

        if q_label == "Most extreme thing you've done?":
            _acts = getattr(girl, "Sex_acts", {}) or {}
            _done_pen = max(_acts.get("anal", 0), _acts.get("sex", 0))
            _done_anal = _acts.get("anal", 0) > 0
            _done_bj = _acts.get("bj", 0) > 0
            _done_tj = _acts.get("tj", 0) > 0
            _done_hj = _acts.get("hj", 0) > 0
            if not _is_ntr and _susp < 40:
                if _done_anal and not bfh.get("anal"):
                    return (
                        _("Anal?! You always told me you'd NEVER do that!"),
                        {"susp": 30, "fr": -10, "narr": _("%(Pp)s looks stunned. %(Poss)s mouth opens and closes, searching for words.")},
                        {"expr": "worried", "blush": "2",
                         "line": _("It was... different. I don't want to talk about it.")})
                elif _done_pen > 0 and not bfh.get("sex"):
                    return (
                        _("That's way more than we've ever done. WHO was that with?"),
                        {"susp": 25, "fr": -8, "narr": _("%(Pp)s stares at her with an intensity that makes the air heavy.")},
                        {"expr": "worried", "blush": "1",
                         "line": _("I'd rather not go into details. Can we please move on?")})
                elif _done_bj and not bfh.get("bj"):
                    return (
                        _("A blowjob? You never... we never did that. When did THAT happen?"),
                        {"susp": 20, "fr": -6, "narr": _("%(Pp)s blinks, trying to process what %(pp)s just heard.")},
                        {"expr": "worried", "blush": "1",
                         "line": _("It was a long time ago. It's not a big deal.")})
                elif _done_tj and not bfh.get("tj"):
                    return (
                        _("A titjob? You never even offered to do that with me."),
                        {"susp": 15, "fr": -5, "narr": _("%(Pp)s crosses %(poss)s arms, visibly bothered.")},
                        {"expr": "embarrassed", "blush": "1",
                         "line": _("It just happened. It wasn't planned or anything.")})
                elif _done_hj and not bfh.get("hj"):
                    return (
                        _("Hold on... we never even did that. How is that your most extreme?"),
                        {"susp": 10, "fr": -3, "narr": _("%(Pp)s looks confused, doing the math.")},
                        {"expr": "shy", "blush": "1",
                         "line": _("Can we just move on? Please?")})
            elif _is_ntr:
                _bl = getattr(npc, "_ntr_boundary_level", 1)
                if _bl >= 4 and _done_pen > 0:
                    return (
                        _("Oh? How extreme are we talking? Give me details."),
                        {"fr": 5, "narr": _("%(Pp)s leans forward, genuinely interested.")},
                        {"expr": "smirk", "blush": "1",
                         "line": _("Way more extreme than anything you and I have done. Trust me.")})

        if q_label == "Would you do something sexual for money?":
            if getattr(girl, "_financial_times", 0) > 0 and not _is_ntr:
                return (
                    _("For money? You're kidding, right? RIGHT?"),
                    {"susp": 15, "fr": -5, "narr": _("%(Pp)s stares at her.")},
                    {"expr": "worried", "blush": "2",
                     "line": _("It wasn't like that! It's not what you think.")})
            if getattr(girl, "_financial_times", 0) > 0 and _is_ntr:
                _hostile_ntr = _ntr_is_hostile_mode(npc)
                _bl = getattr(npc, "_ntr_boundary_level", 1)
                if _hostile_ntr:
                    return (
                        _tl(_("Are you... selling yourself for money, babe? When... oh my god... %s, was that... YOU?")) % store.Player.Name,
                        {"susp": 10, "fr": -8, "narr": _("%(Poss)s voice cracks. %(Pp)s looks about to be sick.")},
                        {"expr": "worried", "blush": "2",
                         "line": _("It's... it's not what it sounds like. Can we just move on?")})
                elif _bl >= 4:
                    return (
                        _("For money? Ha! That's my girl. She knows what she's worth."),
                        {"fr": 6, "narr": _("%(Pp)s grins, genuinely proud.")},
                        {"expr": "smirk", "blush": "1",
                         "line": _("Stop it... you're making it sound worse than it is.")})
                else:
                    return (
                        _("Wait... for... for money? When?"),
                        {"susp": 10, "fr": -2, "narr": _("%(Pp)s stares at her, confused.")},
                        {"expr": "worried", "blush": "2",
                         "line": _("It was complicated, okay? It's not like I'm proud of it.")})

        if q_label == "Ever done a threesome?":
            _gh = getattr(girl, "Girl_history", {}) or {}
            _did = any(_gh.get(gid, {}).get("threesome", 0) > 0 for gid in _gh)
            if _did and not _is_ntr:
                return (
                    _("A THREESOME?! With WHO?!"),
                    {"susp": 20, "fr": -8, "narr": _("%(Pp)s almost spits out %(poss)s drink.")},
                    {"expr": "surprised", "blush": "1",
                     "line": _("What? A threesome? That's so hardcore! I can't even imagine doing one.")})
            if _did and _is_ntr:
                if getattr(girl, "_ntr_boundary_discovered", False):
                    return (
                        _("A threesome? Details. Now."),
                        {"fr": 6, "narr": _("%(Pp)s grins way too wide.")},
                        {"expr": "smirk", "blush": "1",
                         "line": _("Oh, it happened. And it was way more fun than anything we ever did.")})
                else:
                    return (
                        _("A THREESOME?! With WHO?!"),
                        {"susp": 20, "fr": -8, "narr": _("%(Pp)s almost spits out %(poss)s drink.")},
                        {"expr": "surprised", "blush": "1",
                         "line": _("What? A threesome? That's so hardcore! I can't even imagine doing one.")})

        if q_label == "Rough or gentle?":
            if girl.has_trait("hardcore_sex") and not _is_ntr:
                _acts = getattr(girl, "Sex_acts", {}) or {}
                # Was reading positions only ("doggy" is not even a Sex_acts key): a hardcore girl who only
                # did doggy / laying down / full nelson never triggered this. Penetration = "sex" + "anal".
                _done_rough = girl_act_counts(girl)[0] > 0
                if _done_rough and not bfh.get("sex"):
                    return (
                        _("Rough?! You sound like you know from experience. We barely did anything together."),
                        {"susp": 18, "fr": -5, "narr": _("%(Pp)s goes quiet, connecting dots %(pp)s doesn't like.")},
                        {"expr": "worried", "blush": "1",
                         "line": _("It's hypothetical! I'm just saying what I'd prefer!")})
                else:
                    return (
                        _("Since when are you into that?"),
                        {"susp": 5, "narr": _("%(Pp)s shifts uncomfortably.")},
                        {"expr": "shy", "blush": "1",
                         "line": _("It's just a preference. What's wrong with that?")})

        if q_label == "Do you touch yourself?":
            _mast = getattr(girl, "Sex_acts", {}).get("masturbate", 0) > 0
            if _mast and _is_ntr:
                return (
                    _("Touch yourself? Thinking about who, exactly?"),
                    {"fr": 3, "narr": _("%(Pp)s grins.")},
                    {"expr": "smirk", "blush": "2",
                     "line": _("Wouldn't you like to know?")})
            if _mast and not _is_ntr and not bfh.get("masturbate"):
                return (
                    _("You never did that for me. Not once. Who exactly were you doing it for?"),
                    {"susp": 12, "fr": -4, "narr": _("%(Pp)s stares at her, jaw tight.")},
                    {"expr": "embarrassed", "blush": "1",
                     "line": _("It wasn't FOR anyone! I was just... by myself. Drop it.")})

        if q_label == "Ever had a condom break?":
            if getattr(girl, "CreampieCounts", 0) > 0 and not _is_ntr and _susp < 50:
                return (
                    _("A condom... broke? When? With me?"),
                    {"susp": 20, "narr": _("%(Pp)s goes pale.")},
                    {"expr": "worried", "blush": "1",
                     "line": _("It just happened once. It was an accident.")})

        if q_label == "Thoughts on public places?":
            _public_locs = {"pool", "campus", "classroom", "gym", "showers", "hall", "street", "mall", "restaurant_restroom"}
            _did_public = any(sal.get("location", "") in _public_locs and sal.get("act", "") not in _TOD_MILD_ACTS for sal in getattr(girl, "Sex_act_locations", []))
            if _did_public:
                _bl = getattr(npc, "_ntr_boundary_level", 1)
                if _is_ntr and _bl >= 4:
                    return (
                        _("In public? Damn... that's hot. Where exactly?"),
                        {"fr": 5, "narr": _("%(Pp)s leans forward, genuinely intrigued.")},
                        {"expr": "smirk", "blush": "1",
                         "line": _("Wouldn't you like to know the details?")})
                elif not _is_ntr:
                    return (
                        _("Wait... you already did that in public? I don't remember any of that."),
                        {"susp": 20, "fr": -5, "narr": _("%(Pp)s frowns, trying to think.")},
                        {"expr": "worried", "blush": "1",
                         "line": _("It was... a while ago. Not a big deal.")})

        if q_label == "Craziest place you'd do it?":
            _loc_names = {"pool", "campus", "classroom", "gym", "showers", "hall", "street", "mall"}
            _has_real_loc = any(
                sal.get("location", "") in _loc_names and sal.get("act", "") not in _TOD_MILD_ACTS
                for sal in getattr(girl, "Sex_act_locations", []))
            if _has_real_loc:
                _bl = getattr(npc, "_ntr_boundary_level", 1)
                if _is_ntr and _bl >= 4:
                    return (
                        _("You actually did it there? That's insane. I love it."),
                        {"fr": 5, "narr": _("%(Pp)s grins, visibly excited.")},
                        {"expr": "smirk", "blush": "1",
                         "line": _("You're way too excited about this...")})
                elif not _is_ntr:
                    return (
                        _("Hold on... 'already happened'? When did THAT happen?"),
                        {"susp": 18, "fr": -5, "narr": _("%(Pp)s looks at her, confused.")},
                        {"expr": "worried", "blush": "1",
                         "line": _("It's not what you think. Can we move on?")})

        if q_label == "Favorite position or act?":
            _org = getattr(girl, "Orgasms", {}) or {}
            _has_real_fav = any(v > 0 for v in _org.values())
            _fav_act = max(_org, key=_org.get) if _has_real_fav else None
            if _has_real_fav:
                _bl = getattr(npc, "_ntr_boundary_level", 1)
                if _is_ntr and _bl >= 4:
                    return (
                        _("You sound like you know from experience. Tell me more."),
                        {"fr": 4, "narr": _("%(Pp)s watches her with dark fascination.")},
                        {"expr": "smirk", "blush": "1",
                         "line": _("Maybe I do. Maybe I've had a lot of practice.")})
                elif not _is_ntr and _susp < 40:
                    if _fav_act in ("anal",) and not bfh.get("anal"):
                        return (
                            _("Your FAVORITE is anal?! You told me you'd never try that!"),
                            {"susp": 25, "fr": -8, "narr": _("%(Pp)s looks like %(pp)s just got punched in the gut.")},
                            {"expr": "worried", "blush": "2",
                             "line": _("I didn't say it was my favorite! I just... stop twisting my words!")})
                    elif _fav_act in ("cowgirl", "reverse_cowgirl", "doggy", "laying_down", "sex") and not bfh.get("sex"):
                        return (
                            _("How do you know that's your favorite? We never did that."),
                            {"susp": 15, "fr": -4, "narr": _("%(Pp)s narrows %(poss)s eyes.")},
                            {"expr": "worried", "blush": "1",
                             "line": _("I just... know. Intuition, I guess.")})
                    elif _fav_act in ("bj",) and not bfh.get("bj"):
                        return (
                            _("That's your favorite? You never once did that for me."),
                            {"susp": 12, "fr": -4, "narr": _("%(Pp)s shakes %(poss)s head slowly.")},
                            {"expr": "embarrassed", "blush": "1",
                             "line": _("I said I LIKE it, not that I've done it a lot. God.")})
                    elif _fav_act in ("tj",) and not bfh.get("tj"):
                        return (
                            _("Since when is that your thing? You never mentioned it to me."),
                            {"susp": 10, "fr": -3, "narr": _("%(Pp)s crosses %(poss)s arms.")},
                            {"expr": "embarrassed", "blush": "1",
                             "line": _("Not everything has to involve you, you know.")})

        if q_label == "What's your biggest fetish?":
            _bl = getattr(npc, "_ntr_boundary_level", 1)
            # the fetish she actually named (tod_lewd_biggest_fetish), not every fetish trait she has
            _fetish = getattr(store, "_tod_fetish_pick", None)
            _has_cum = _fetish == "cum"
            _has_cam = _fetish == "camera"
            if _has_cum:
                # "It's not from you": only once someone else (the player) has finished inside her
                if _is_ntr and _bl >= 4 and getattr(girl, "CreampieCounts", 0) > 0:
                    return (
                        _("Creampies? From who, exactly? I need details."),
                        {"fr": 6, "narr": _("%(Pp)s shifts forward, breathing harder.")},
                        {"expr": "smirk", "blush": "2",
                         "line": _("You really want to know? Fine. It's not from you.")})
                elif not _is_ntr and not bfh.get("creampie"):
                    return (
                        _("Creampies?! You never let me do that!"),
                        {"susp": 15, "fr": -6, "narr": _("%(Pp)s stares at her in disbelief.")},
                        {"expr": "worried", "blush": "2",
                         "line": _("That's... that's different. It's complicated, okay?")})
            elif _has_cam:
                if _is_ntr and _bl >= 4:
                    return (
                        _("Being filmed? By who? Please tell me there are videos."),
                        {"fr": 5, "narr": _("%(Poss)s eyes light up.")},
                        {"expr": "smirk", "blush": "1",
                         "line": _("There might be. You'll never find them though.")})
                elif not _is_ntr:
                    return (
                        _("Filmed? Since when do you like that? You never mentioned that to me."),
                        {"susp": 12, "fr": -3, "narr": _("%(Pp)s looks at her sideways.")},
                        {"expr": "embarrassed", "blush": "1",
                         "line": _("Some things I keep to myself. Is that a crime?")})

        return None


label _bf_watch_girl_truth(npc, girl, was_lewd, stripped=False, q_label=None):
    python:
        _bfw_ntr = _npc_is_ntr(npc)
        _bfw_key = _bf_watch_key(npc, girl, was_lewd)
    $ npc.show_sprite(_hangout_npc_pos())

    # She stripped in front of him instead of answering -> loudest reaction.
    if stripped:
        python:
            _bfw_skey = _bfw_key if _bfw_key in _BF_WATCH_STRIP else "uneasy"
        python:
            _bfw_pick = renpy.random.choice(_BF_WATCH_STRIP[_bfw_skey])
            _bfw_narr, _bfw_line = _bfw_pick if isinstance(_bfw_pick, tuple) else (None, _bfw_pick)
        if _bfw_narr:
            $ Narration(_format_npc_line(npc, _bfw_narr))
        if _bfw_line:
            $ Character(npc.Name, color=npc.color)(_format_npc_line(npc, _bfw_line))
        python:
            if _bfw_ntr:
                if callable(globals().get("_ntr_increase_boundary_bar")):
                    _ntr_increase_boundary_bar(npc, girl, 12)
                _bf_apply(npc, girl, fr=6)
                Change_Status(girl, "Lust", 4)
            elif npc.has_trait("proud"):
                _bf_apply(npc, girl, fr=-14, susp=20)
            else:
                _bf_apply(npc, girl, susp=12)
        return

    # Safe question -> only occasionally worth a beat (avoid spamming every turn).
    if not was_lewd:
        if renpy.random.random() < 0.4:
            python:
                _bfw_pick = renpy.random.choice(_BF_WATCH_SAFE.get(_bfw_key, _BF_WATCH_SAFE["neutral"]))
                _bfw_narr, _bfw_line = _bfw_pick if isinstance(_bfw_pick, tuple) else (None, _bfw_pick)
            if _bfw_narr:
                $ Narration(_format_npc_line(npc, _bfw_narr))
            if _bfw_line:
                $ Character(npc.Name, color=npc.color)(_format_npc_line(npc, _bfw_line))
            python:
                if _bfw_ntr:
                    _bf_apply(npc, girl, fr=2)
                elif npc.has_trait("proud"):
                    _bf_apply(npc, girl, fr=1)
        return

    # Lewd question answered with the NPC watching -> the main reaction.
    python:
        _bfw_pick = renpy.random.choice(_BF_WATCH_LEWD[_bfw_key])
        _bfw_narr, _bfw_line = _bfw_pick if isinstance(_bfw_pick, tuple) else (None, _bfw_pick)
        _bfw_has_content = _bf_content_reaction(npc, girl, q_label) is not None if q_label else False
    if _bfw_narr:
        $ Narration(_format_npc_line(npc, _bfw_narr))
    if _bfw_line:
        $ Character(npc.Name, color=npc.color)(_format_npc_line(npc, _bfw_line))
    python:
        if _bfw_key == "ntr":
            if callable(globals().get("_ntr_increase_boundary_bar")):
                _ntr_increase_boundary_bar(npc, girl, 8)
            _bf_apply(npc, girl, fr=4)
            Change_Status(girl, "Lust", 3)
        elif _bfw_key == "proud":
            _bf_apply(npc, girl, fr=-6, susp=12 if not _bfw_has_content else 0)
        elif _bfw_key == "friendly":
            _bf_apply(npc, girl, fr=2, susp=3 if not _bfw_has_content else 0)
        else:
            if not _bfw_has_content:
                _bf_apply(npc, girl, susp=8)

    # The girl may answer the NPC's reaction (only the emotionally-charged pools).
    if _bfw_key == "ntr":
        $ set_scene_expression(girl, "shy", blush="2")
        python:
            _bfw_gpick = renpy.random.choice(_BF_WATCH_LEWD_GIRL["ntr"])
            _bfw_gnarr, _bfw_gline = _bfw_gpick if isinstance(_bfw_gpick, tuple) else (None, _bfw_gpick)
        if _bfw_gnarr:
            $ Narration(_format_npc_line(npc, _bfw_gnarr))
        if _bfw_gline:
            $ Say_Line(girl, _tl(_bfw_gline))
    elif _bfw_key == "proud":
        $ set_scene_expression(girl, "worried")
        python:
            _bfw_gpick = renpy.random.choice(_BF_WATCH_LEWD_GIRL["proud"])
            _bfw_gnarr, _bfw_gline = _bfw_gpick if isinstance(_bfw_gpick, tuple) else (None, _bfw_gpick)
        if _bfw_gnarr:
            $ Narration(_format_npc_line(npc, _bfw_gnarr))
        if _bfw_gline:
            $ Say_Line(girl, _tl(_bfw_gline))

    if q_label is not None:
        python:
            _bfw_content = _bf_content_reaction(npc, girl, q_label)
        if _bfw_content is not None:
            python:
                _bfw_cline, _bfw_cfx, _bfw_cgirl = _bfw_content
            $ Character(npc.Name, color=npc.color)(_tl(_bfw_cline))
            if _bfw_cfx.get("narr"):
                $ renpy.say(None, _format_npc_line(npc, _bfw_cfx["narr"]))
            python:
                _bf_apply(npc, girl, fr=_bfw_cfx.get("fr", 0), susp=_bfw_cfx.get("susp", 0),
                          gobed=_bfw_cfx.get("gobed", 0), glove=_bfw_cfx.get("glove", 0))
            if _bfw_cgirl is not None:
                python:
                    if _bfw_cgirl.get("expr"):
                        set_scene_expression(girl, _bfw_cgirl["expr"], blush=_bfw_cgirl.get("blush"))
                if _bfw_cgirl.get("line"):
                    $ Say_Line(girl, _tl(_bfw_cgirl["line"]))
    return


# ============================================================
# NPC watches a NON-GF girl answer a lewd truth. Brief casual reaction.
# Only fires ~30% of the time to avoid spamming.
# ============================================================
label _bf_watch_nongf_truth(npc, girl, discoveries):
    if renpy.random.random() > 0.30:
        return

    python:
        _bwn_tier = _bf_friend_tier(npc)
        _bwn_line = None

        if "discovered_virgin" in discoveries:
            if _bwn_tier == "friendly":
                _bwn_line = renpy.random.choice([
                    _("Wait, really? I would not have guessed that."),
                    _("Huh. Good for you, honestly."),
                ])
            elif _bwn_tier == "neutral":
                _bwn_line = renpy.random.choice([
                    _("Oh. Didn't expect that."),
                    _("Huh. Interesting."),
                ])
        elif "discovered_has_partner" in discoveries:
            if _bwn_tier != "hostile":
                _bwn_line = renpy.random.choice([
                    _("Oh, you have someone? Cool."),
                    _("Nice. Who's the lucky one?"),
                ])
        elif "discovered_trait_lesbian" in discoveries:
            if _bwn_tier == "friendly":
                _bwn_line = _("Oh, good for you!")
            elif _bwn_tier == "neutral":
                _bwn_line = _("Huh. Okay then.")
        elif "discovered_trait_cheater" in discoveries:
            if _bwn_tier != "hostile":
                _bwn_line = renpy.random.choice([
                    _("Wow, really? Bold."),
                    _("That's... something."),
                ])

    if _bwn_line is not None:
        $ npc.show_sprite(_hangout_npc_pos())
        $ Character(npc.Name, color=npc.color)(_tl(_bwn_line))
    return


# ============================================================
# SHARED DARE: Phone scroll — BF dares girl to show last photo.
# Checks chat history for compromising content (dick pics, nudes,
# recorded videos) and reacts accordingly.
# ============================================================
label _tod_dare_show_phone(npc, girl, target="bf"):
    if target == "bf":
        # -- BF shows his phone. GF scrolls through it. --
        $ Character(npc.Name, color=npc.color)(_tl(_("Show my phone? What are we, in middle school?")))

        python:
            _sp_love = getattr(npc, "love_for_girl", 500)
            _sp_others = [g for g in _hangout_girls_list() if g.gid != girl.gid]
            print("[SHOW_PHONE] BF %s love_for_girl=%d" % (npc.Name, _sp_love))

        if _sp_love < 400:
            $ set_scene_expression(girl, "smirk")
            $ Say_Line(girl, _tl(_("Come on, just show it! What are you hiding?")))
            $ Character(npc.Name, color=npc.color)(_tl(_("Fine, fine. Here.")))
            $ Narration(_format_npc_line(npc, _("%(Pp)s unlocks %(poss)s phone and hands it over. %(girl_name)s starts scrolling."), girl))
            $ set_scene_expression(girl, "surprised")
            $ Say_Line(girl, _tl(_("...Who's Jessica?")))
            $ Character(npc.Name, color=npc.color)(_tl(_("She's just a friend from class.")))
            $ set_scene_expression(girl, "angry")
            $ Say_Line(girl, _tl(_("'Just a friend' who sends heart emojis at midnight?")))
            $ Character(npc.Name, color=npc.color)(_tl(_("It's not what it looks like!")))
            $ set_scene_expression(girl, "serious")
            $ Say_Line(girl, _tl(_("Sure it's not.")))
            python:
                Change_NPC_Status(npc, "love_for_girl", -30)
                if hasattr(girl, "bf_loyalty"):
                    girl.bf_loyalty = max(0, girl.bf_loyalty - 25)
                for _spg in _sp_others:
                    set_scene_expression(_spg, "surprised")
                print("[SHOW_PHONE] BF low love: love_for_girl -30, bf_loyalty -25")
            $ Narration(_tl(_("An awkward silence settles over the group.")))
        elif _sp_love >= 700:
            $ Character(npc.Name, color=npc.color)(_tl(_("Sure, I got nothing to hide.")))
            $ Narration(_format_npc_line(npc, _("%(Pp)s hands %(poss)s phone to %(girl_name)s. She scrolls through it."), girl))
            $ set_scene_expression(girl, "happy")
            $ Say_Line(girl, _tl(_("Aww, your wallpaper is that photo of us!")))
            $ Character(npc.Name, color=npc.color)(_tl(_("Of course it is. You're my girl.")))
            $ set_scene_expression(girl, "shy", blush="1")
            python:
                for _spg in _sp_others:
                    set_scene_expression(_spg, "neutral")
        else:
            $ Character(npc.Name, color=npc.color)(_tl(_("Alright, here. Knock yourself out.")))
            $ Narration(_format_npc_line(npc, _("%(Pp)s hands %(poss)s phone over. %(girl_name)s scrolls through it with a bored expression."), girl))
            $ set_scene_expression(girl, "neutral")
            $ Say_Line(girl, _tl(_("It's just sports scores and memes. Typical.")))
            $ Character(npc.Name, color=npc.color)(_tl(_("Told you. Nothing exciting.")))
            python:
                for _spg in _sp_others:
                    set_scene_expression(_spg, "bemused")
        return

    # -- GF shows her phone. BF and others react. --
    $ Character(npc.Name, color=npc.color)(_tl(_("I dare you to show us the last photo on your phone. No deleting first!")))
    $ set_scene_expression(girl, "surprised")
    $ Say_Line(girl, _tl(_("What?! No way, that's private!")))
    $ Character(npc.Name, color=npc.color)(_tl(_("It's a dare! Come on, it's probably just food.")))

    python:
        _ps_dick = getattr(girl, "_dick_pics_received", 0) > 0
        _ps_chat = phone_get_msgs(girl.gid)
        _ps_has_photo = any(m.get("type") == "photo" for m in _ps_chat)
        _ps_has_vid = any(v.get("girl_gid") == girl.gid for v in getattr(store.Player, "recorded_videos", []))
        _ps_love = getattr(girl, "Love", 0)
        _ps_others = [g for g in _hangout_girls_list() if g.gid != girl.gid]
        print("[SHOW_PHONE] GF %s dick=%s photo=%s vid=%s love=%d" % (girl.gid, _ps_dick, _ps_has_photo, _ps_has_vid, _ps_love))

    if _ps_dick:
        $ set_scene_expression(girl, "embarrassed", blush="2")
        $ Say_Line(girl, _tl(_("I am NOT showing that. Absolutely not. Next dare.")))
        $ Character(npc.Name, color=npc.color)(_tl(_("Whoa, why not? What's on there?")))
        $ Say_Line(girl, _tl(_("NOTHING! It's just... I have private stuff, okay?!")))
        $ Narration(_tl(_("She clutches her phone to her chest, face burning red.")))
        $ Character(npc.Name, color=npc.color)(_tl(_("...Private stuff? From who?")))
        $ set_scene_expression(girl, "serious")
        $ Say_Line(girl, _tl(_("Drop it. I'm not showing my phone. End of story.")))
        python:
            if callable(globals().get("Change_NPC_Status")):
                Change_NPC_Status(npc, "suspicion", 10)
            for _psg in _ps_others:
                set_scene_expression(_psg, "surprised")
    elif _ps_has_vid:
        $ set_scene_expression(girl, "embarrassed", blush="2")
        $ Say_Line(girl, _tl(_("There are things on my phone that NOBODY can see. I'm serious.")))
        $ Character(npc.Name, color=npc.color)(_tl(_("That bad? Now I'm really curious.")))
        $ Say_Line(girl, _tl(_("Curious all you want, you're not touching my phone.")))
        $ Narration(_tl(_("She shoves her phone deep into her pocket. She looks genuinely nervous.")))
        python:
            if callable(globals().get("Change_NPC_Status")):
                Change_NPC_Status(npc, "suspicion", 5)
            for _psg in _ps_others:
                set_scene_expression(_psg, "bemused")
    elif _ps_has_photo:
        $ set_scene_expression(girl, "shy", blush="1")
        $ Say_Line(girl, _tl(_("Fine... here, it's just a selfie. See? Nothing weird.")))
        $ Narration(_tl(_("She briefly flashes a photo. It IS a selfie, but you know that's not the most recent thing on her phone.")))
        $ Character(npc.Name, color=npc.color)(_tl(_("Cute. You look good.")))
        $ set_scene_expression(girl, "embarrassed", blush="1")
        python:
            for _psg in _ps_others:
                set_scene_expression(_psg, "neutral")
    elif _ps_love >= 500:
        $ set_scene_expression(girl, "neutral")
        $ Say_Line(girl, _tl(_("See? It's just a selfie at the campus fountain. Happy now?")))
        $ Character(npc.Name, color=npc.color)(_tl(_("Cute. You look good.")))
    else:
        $ set_scene_expression(girl, "neutral")
        $ Say_Line(girl, _tl(_("Look. It's literally a picture of my lunch. Satisfied?")))
        $ Character(npc.Name, color=npc.color)(_tl(_("...That's the most boring dare result ever.")))
        $ Narration(_tl(_("Everyone laughs.")))
    return


# ============================================================
# SHARED DARE: Arm wrestle — player vs BF.
# BF strength = 3. Player strength = energy_max (2-5, raised by gym).
# 4-5 wins, 1-2 loses, 3 = coin flip (no stat change).
# initiator = "bf" (he challenged player) or "player" (player/girl challenged him).
# ============================================================
label _tod_dare_arm_wrestle(npc, girl, initiator):
    if initiator == "bf":
        $ Character(npc.Name, color=npc.color)(_tl(_("I dare you to arm wrestle me. Right here, right now. Think you can take me?")))
        $ Say_Player(_("You're on."))
    else:
        $ Say_Player(_("Let's settle this. Arm wrestle. You and me."))
        $ Character(npc.Name, color=npc.color)(_tl(_("Ha! You serious? Alright, bring it.")))

    $ Narration(_tl(_("You both lock hands across the table. The girls lean in to watch.")))

    python:
        _aw_strength = Player._get_energy_max()
        _aw_bf_str = 3
        if _aw_strength > _aw_bf_str:
            _aw_result = "win"
        elif _aw_strength < _aw_bf_str:
            _aw_result = "lose"
        else:
            _aw_result = "win" if renpy.random.random() < 0.5 else "lose"
        _aw_tied = (_aw_strength == _aw_bf_str)
        print("[ARM_WRESTLE] player_str=%d bf_str=%d result=%s tied=%s" % (_aw_strength, _aw_bf_str, _aw_result, _aw_tied))

    if _aw_result == "win":
        if _aw_tied:
            $ Narration(_format_npc_line(npc, _("It goes back and forth for a long time. Neither of you gives an inch... until you finally force %(poss)s hand down at the last second.")))
        else:
            $ Narration(_format_npc_line(npc, _("You slam %(poss)s hand down. It's not even close.")))
        $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([
            _("What the... okay, respect. You got some arms on you."),
            _("Damn! You're stronger than you look."),
        ])))
        python:
            _aw_girls = _hangout_girls_list()
            for _awg in _aw_girls:
                set_scene_expression(_awg, "surprised")
            if not _aw_tied:
                for _awg in _aw_girls:
                    Change_Status(_awg, "Obed", 8)
    else:
        if _aw_tied:
            $ Narration(_format_npc_line(npc, _("It goes back and forth for a long time. Neither of you gives an inch... until %(pp)s finally forces your hand down at the last second.")))
        else:
            $ Narration(_format_npc_line(npc, _("%(Pp)s pins your hand down almost instantly. You never stood a chance.")))
        $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([
            _("Ha! Better hit the gym, buddy."),
            _("Too easy! Come back when you've been working out."),
        ])))
        python:
            _aw_girls = _hangout_girls_list()
            for _awg in _aw_girls:
                set_scene_expression(_awg, "bemused")
            if not _aw_tied:
                for _awg in _aw_girls:
                    Change_Status(_awg, "Obed", -8)

    if girl is not None:
        if _aw_result == "win":
            $ Say_Line(girl, _tl(renpy.random.choice([
                _("Okay, that was actually impressive."),
                _("Wow... I didn't expect that."),
            ])))
        else:
            $ Say_Line(girl, _tl(renpy.random.choice([
                _("Well... at least you tried."),
                _("That was over fast."),
            ])))
    return


# ============================================================
# SHARED DARE: Impression — girl imitates a known campus person.
# BF picks who. If the target is in the hangout, they react.
# ============================================================
label _tod_dare_impression(npc, girl):
    python:
        _imp_targets = [
            ("gwen",    "Gwen",       _("Yeah dude, this school is like, a total challenge for me.")),
            ("rogue",   "Rogue",      _("Don't touch me! Trying to be all dark and edgy today.")),
            ("ntw",     "Negasonic",  _("Hey, have you seen any Asian girl around here?")),
            ("cjohnson","C. Johnson", _("Buy hotdogs now, big sausage!")),
        ]
        _imp_pool = [t for t in _imp_targets if t[0] != girl.gid]
        _imp_pick = renpy.random.choice(_imp_pool)
        _imp_gid, _imp_name, _imp_line = _imp_pick

    $ Character(npc.Name, color=npc.color)(_tl(_("I dare you to do your best impression of someone we all know!")))
    $ set_scene_expression(girl, "bemused")
    $ Say_Line(girl, _tl(_("Oh no... okay, who?")))
    $ Character(npc.Name, color=npc.color)(_tl(_("Do %s!")) % _imp_name)
    $ set_scene_expression(girl, "smirk")
    $ Say_Line(girl, _tl(_imp_line))
    $ Narration(_tl(_("Everyone bursts out laughing.")))

    python:
        _imp_present = None
        _imp_hangout = _hangout_girls_list()
        for _ig in _imp_hangout:
            if _ig.gid == _imp_gid:
                _imp_present = _ig
                break

    if _imp_present is not None:
        $ set_scene_expression(_imp_present, "serious")
        $ Say_Line(_imp_present, _tl(renpy.random.choice([
            _("I do NOT sound like that!"),
            _("Okay wow, is that really what you think I'm like?"),
            _("That was terrible. And also a little accurate."),
        ])))
        python:
            if renpy.random.random() < 0.5:
                Change_Status(_imp_present, "Love", 5)
                set_scene_expression(_imp_present, "happy")
            else:
                Change_Status(_imp_present, "Love", -5)
                set_scene_expression(_imp_present, "annoyed")
    else:
        $ set_scene_expression(girl, "happy")

    $ Character(npc.Name, color=npc.color)(_tl(renpy.random.choice([
        _("That was actually pretty good!"),
        _("Not bad. Not bad at all."),
        _("Ha! Do another one!"),
    ])))
    $ _bf_apply(npc, girl, fr=3)
    return
