# ============================================================
# Tease System — player talks dirty during sex scenes
# Reusable across all poses (RCG, cowgirl, bj, hj, tj)
# Only available when speed > 0
# ============================================================

# Uses of each tease on each girl in the current time slot (tease_stat_changes: repetition fades the gains)
default _tease_repeat = {}

init python:

    def _has_cum_inside_before(girl):
        return getattr(girl, "CreampieCounts", 0) > 0

    # Named availability functions (lambdas break save/pickle)
    def _tease_always(girl, scene):
        return True

    def _tease_not_lesbian(girl, scene):
        return not girl.has_trait("lesbian")

    def _tease_footjob_only(girl, scene):
        return scene == "fj"

    # ── Partner presence helpers ─────────────────────────────
    def _tease_partner_npc(girl):
        """NPC partner object for this girl, or None."""
        if not (hasattr(girl, "has_npc_partner") and girl.has_npc_partner()):
            return None
        if not callable(globals().get("get_npc_partner_for", None)):
            return None
        return get_npc_partner_for(girl)

    def _tease_partner_on_scene():
        """NTR partner is in the room for this scene (watching OR listening with his back turned)."""
        return getattr(store, "_ntr_partner_watching", False) and getattr(store, "_ntr_watching_npc", None) is not None

    def _tease_partner_facing_away():
        """NTR bet event: partner is in the room but hasn't lost the bet yet, so his back is turned.
        He hears everything but sees nothing."""
        return getattr(store, "_bet_event_active", False) and not getattr(store, "_bet_npc_looked", False)

    def _tease_partner_watching():
        """NTR partner is actively watching the scene right now."""
        return _tease_partner_on_scene() and not _tease_partner_facing_away()

    def _tease_partner_listening():
        """NTR partner is in the room but facing away (bet event before he turns)."""
        return _tease_partner_on_scene() and _tease_partner_facing_away()

    def _tease_partner_present(girl):
        """Partner is physically in the scene: NTR watching/listening OR on scene (walk-in / event).
        Secret-cheating teases ("he has no idea") are hidden in that case."""
        if _tease_partner_on_scene():
            return True
        _npc = _tease_partner_npc(girl)
        return _npc is not None and _npc is getattr(store, "_npc_on_scene", None)

    def _tease_ntr_known(girl):
        """Partner knows and permits this (NTR active + boundary discovered) but is NOT here.
        Mirrors the 'ntr_known' scene-line modifier: no secrecy, no audience."""
        if _tease_partner_present(girl):
            return False
        if not callable(globals().get("_ntr_active_discovered", None)):
            return False
        return _ntr_active_discovered(girl)

    def _tease_girl_watcher(girl):
        """Another girl watching the scene (witness / threesome), or None."""
        if not getattr(store, "_witness_watching", False):
            return None
        _w = getattr(store, "_witness_girl", None)
        if _w is None or _w is girl:
            return None
        return _w

    def _tease_gf_watching(girl):
        """The girl's own girlfriend (girl partner) is present: watching as witness,
        or she gave permission for this scene (gf_permission coercion keeps her on scene)."""
        if getattr(store, "_coercion_type", None) == "gf_permission":
            return True
        _w = _tease_girl_watcher(girl)
        return _w is not None and getattr(girl, "girl_partner_id", None) == getattr(_w, "gid", None)

    # ── Availability functions ───────────────────────────────
    def _tease_has_bf(girl, scene):
        if _tease_partner_present(girl):
            return False
        return hasattr(girl, "has_npc_partner") and girl.has_npc_partner() and not girl.get_flag("partner_is_female")

    def _tease_has_husband(girl, scene):
        """A married girl (trait, never an NPC partner: her husband is a FamilyContact or off screen).
        Netori: taking another man's WIFE. Hidden if he is somehow in the room (acts are locked there anyway)."""
        if not (hasattr(girl, "has_trait") and girl.has_trait("married")):
            return False
        return not (callable(globals().get("husband_in_room", None)) and husband_in_room(girl))

    def _tease_penetration(girl, scene):
        return scene in ("reverse_cowgirl", "reverse_cowgirl_anal", "cowgirl", "doggy", "anal", "laying_down", "laying_anal", "full_nelson", "full_nelson_anal")

    def _tease_breed(girl, scene):
        if store._pregnancy_mode == "off":
            return False
        return scene in ("reverse_cowgirl", "cowgirl", "doggy", "laying_down", "full_nelson")

    def _tease_breed_pregnant(girl, scene):
        if store._pregnancy_mode == "off":
            return False
        # Known pregnancies only: the option itself would reveal one she has not discovered yet
        return getattr(girl, "_pregnant", False) and getattr(girl, "_pregnancy_known", False)

    def _tease_atm_active(girl, scene):
        return scene == "bj" and getattr(store, "_atm_cum_in_mouth", False)

    def _tease_is_lesbian(girl, scene):
        return girl.has_trait("lesbian")

    def _tease_has_girlfriend(girl, scene):
        """NPC girlfriend OR playable girl partner. Hidden only while an NTR partner is in the room
        (the NTR teases take over); a watching girl partner gets the _gf_watching pools."""
        if _tease_partner_on_scene():
            return False
        if hasattr(girl, "has_npc_girlfriend") and girl.has_npc_girlfriend():
            return True
        return hasattr(girl, "has_girl_partner") and girl.has_girl_partner()

    def _tease_has_financial(girl, scene):
        return getattr(girl, "_financial_times", 0) >= 1

    def _tease_ntr_watching(girl, scene):
        # Partner teases stay available while he only listens: taunting him to turn around
        # is exactly the bet's noise mechanic.
        return _tease_partner_on_scene()

    # ── Scene context ────────────────────────────────────────
    # Scene types that should also draw from other pose pools.
    def _tease_count_slaps(girl, scene):
        """"Make her count" (count_slaps.rpy): a submissive, in a scene whose menu has a spank or a slap, not counting yet."""
        return (hasattr(girl, "has_trait") and girl.has_trait("submissive") and scene in COUNT_SLAPS_SCENES
                and not count_slaps_active(girl))

    _TEASE_POSE_KEYS = {
        "anal": ["anal", "doggy"],
        "full_nelson_anal": ["full_nelson_anal", "anal", "full_nelson"],
        "laying_anal": ["laying_anal", "anal", "laying_down"],
        "reverse_cowgirl_anal": ["reverse_cowgirl_anal", "anal", "reverse_cowgirl"],
    }

    # Contexts that describe the physical situation; they beat the tone pools
    # (_hostile / _recording) because those assume the partner can see the scene.
    _TEASE_SITUATION_CTX = ("_ntr_listening",)

    def _tease_pose_keys(scene_type):
        return _TEASE_POSE_KEYS.get(scene_type, [scene_type])

    def _tease_is_anal_scene(scene_type):
        if scene_type in _ANAL_SCENE_TYPES:
            return True
        return any(getattr(store, _af, False) for _af in _ANAL_FLAGS.values())

    def _tease_contexts(girl, tease_key, scene_type):
        """Ordered context prefixes (most specific first). Both player lines and reactions
        look for '<prefix>' / '<prefix>_<pose>' / '<prefix>_<trait>' pools; a prefix only
        matters for teases that define it, so every pool is optional."""
        ctx = []
        if _tease_partner_listening():
            # Bet event, back turned: he hears everything, sees nothing. No _ntr_watching pools.
            ctx.append("_ntr_listening")
        elif _tease_partner_watching():
            _npc = store._ntr_watching_npc
            if tease_key == "cum_threat":
                # Boundary decides whether a creampie is allowed in front of him
                _lvl = getattr(_npc, "_ntr_boundary_level", 1)
                ctx.append("_ntr_watching_ok" if _lvl >= 4 else "_ntr_watching_no")
            if tease_key == "filming" and _npc.has_trait("camera_lover") and not girl.has_trait("camera_hater"):
                ctx.append("_ntr_watching_cam")
            ctx.append("_ntr_watching")
        elif _tease_ntr_known(girl):
            ctx.append("_ntr_known")
        if _tease_gf_watching(girl):
            ctx.append("_gf_watching")
        if _tease_girl_watcher(girl) is not None:
            ctx.append("_girl_watching")
        if getattr(store, "_coercion_type", None) == "blackmail":
            ctx.append("_coerced")
        if tease_key == "cum_threat" and getattr(store, "condom_active", False):
            ctx.append("_condom")
        # Her husband is FAMILY of the player (a FamilyContact: today the stepmom's husband, his father).
        # The betrayal lives inside the family: husband_humiliate swaps to its _family_husband pools.
        if (hasattr(girl, "has_trait") and girl.has_trait("married")
                and callable(globals().get("girl_husband", None))
                and getattr(girl_husband(girl), "is_family", False)):
            ctx.append("_family_husband")
        if scene_type in ("full_nelson", "full_nelson_anal"):
            ctx.append("_fn")
        debug_log("[TEASE] contexts for %s/%s (%s): %s" % (girl.gid, tease_key, scene_type, ctx))
        return ctx

    def _tease_gather(lines_dict, prefix, scene_type, npc_gender=None):
        """'<prefix>' pool + '<prefix>_<pose>' pools (+ '<prefix>_<gender>')."""
        pool = list(lines_dict.get(prefix, []))
        for _pk in _tease_pose_keys(scene_type):
            pool.extend(lines_dict.get("%s_%s" % (prefix, _pk), []))
        if npc_gender:
            pool.extend(lines_dict.get("%s_%s" % (prefix, npc_gender), []))
        return pool

    def _tease_pick_line(lines_dict, scene_type, npc_gender=None, npc_hostile=False, contexts=None):
        """Pick a random player line, preferring pose-specific lines.
        Priority: situation contexts (_ntr_listening) > hostile > recording
        > other contexts (partner/watcher/coercion/condom) > in public > normal.
        Each level overrides only if its pool exists."""
        contexts = contexts or []
        for _ctx in contexts:
            if _ctx in _TEASE_SITUATION_CTX and _ctx in lines_dict:
                pool = _tease_gather(lines_dict, _ctx, scene_type, npc_gender)
                if pool:
                    return renpy.random.choice(pool)
        if npc_hostile and "_hostile" in lines_dict:
            pool = _tease_gather(lines_dict, "_hostile", scene_type, npc_gender)
            if pool:
                return renpy.random.choice(pool)
        if getattr(store, "_recording_active", False) and "_recording" in lines_dict:
            pool = _tease_gather(lines_dict, "_recording", scene_type)
            if pool:
                return renpy.random.choice(pool)
        for _ctx in contexts:
            if _ctx in _TEASE_SITUATION_CTX:
                continue
            if _ctx in lines_dict:
                pool = _tease_gather(lines_dict, _ctx, scene_type, npc_gender)
                if pool:
                    return renpy.random.choice(pool)
        if _is_public_location() and "_in_public" in lines_dict:
            pool = _tease_gather(lines_dict, "_in_public", scene_type)
            if pool:
                return renpy.random.choice(pool)
        pool = _tease_gather(lines_dict, "_any", scene_type, npc_gender)
        for _pk in _tease_pose_keys(scene_type):
            pool.extend(lines_dict.get(_pk, []))
        if not pool:
            pool = ["..."]
        return renpy.random.choice(pool)

    TEASE_OPTIONS = {

        # ── MAKE HER COUNT (submissive: every spank / slap from now on gets its number, count_slaps.rpy) ──
        "count_slaps": {
            "label": _("Make her count"),
            "available": _tease_count_slaps,
            "player_lines": {
                "_any": [
                    _("From now on you count every one. Out loud."),
                    _("Every time my hand lands, I want to hear the number."),
                    _("Count them for me. Don't you dare lose track."),
                ],
            },
            # deference first: a submissive ACCEPTS the order; hardcore is the one who wants the number to climb
            "trait_priority": ["hardcore_sex", "nerd"],
            "reactions": {
                "hardcore_sex": {
                    "lines": [
                        _("Yes! Make me say every one. I want to hear how far you take me."),
                        _("Counting. Please, start now. I want to get to a big number."),
                    ],
                    "stats": {"Inbt": 5, "Obed": 3},
                    "expression": "lipbite",
                },
                "nerd": {
                    "lines": [
                        _("Counting. I'm good at counting. I won't miss one."),
                        _("Okay. Out loud. I'll keep an exact tally, you'll see."),
                    ],
                    "stats": {"Obed": 4, "Inbt": 2},
                    "expression": "shy",
                },
                "_default": {
                    "lines": [
                        _("...Yes. I'll count. Every one."),
                        _("Out loud. Okay. ...Please don't go too high."),
                        _("If that's what you want. I'll count."),
                    ],
                    "stats": {"Obed": 4, "Inbt": 2},
                    "expression": "shy",
                },
            },
        },

        # ── PRAISE HER ──────────────────────────────────────
        "praise": {
            "label": _("Praise her"),
            "available": _tease_not_lesbian,
            "player_lines": {
                "_any": [
                    _("You're so fucking hot..."),

                    _("God, you feel amazing..."),

                    _("You're the best I've ever had..."),

                    _("I can't get enough of you..."),

                    _("You drive me crazy, you know that?"),

                    _("Your body is perfect..."),

                    _("Every inch of you is incredible..."),

                ],
                "reverse_cowgirl": [
                    _("Your ass looks so good from back here..."),

                    _("I love watching you arch your back like that..."),

                    _("You take it so well from behind..."),

                ],
                "cowgirl": [
                    _("You ride so fucking good..."),

                    _("I love watching you bounce on me..."),

                    _("The view from down here is incredible..."),

                ],
                "bj": [
                    _("Your mouth feels so good..."),

                    _("You're so good at this..."),

                    _("Nobody sucks it like you do..."),

                ],
                "hj": [
                    _("Your hands are magic..."),

                    _("You know exactly how to touch me..."),

                ],
                "tj": [
                    _("Your tits feel amazing around my cock..."),

                    _("I love watching them wrap around me..."),

                ],
                "fj": [
                    _("You're really good with your feet..."),

                    _("Your soles feel incredible..."),

                ],
                "doggy": [
                    _("You look incredible bent over like that..."),

                    _("The way you push back against me... fuck..."),

                ],
                "full_nelson": [
                    _("Look at you, spread open and taking all of it..."),

                    _("You feel amazing like this... every inch of you pressed against me..."),

                ],
                "laying_down": [
                    _("You look so beautiful under me..."),

                    _("I love feeling your whole body against mine like this..."),

                ],
                "anal": [
                    _("Your ass takes me like it was made for it..."),

                    _("You're doing so well... you're incredible..."),

                ],
                # ── NTR partner watching ──
                "_ntr_watching": [
                    _("You're perfect... I don't care who's watching."),

                    _("You feel amazing... let %(po)s hear me say it."),

                    _("The best I've ever had... and %(name)s gets a front row seat to why."),

                ],
                # ── Another girl watching ──
                "_girl_watching": [
                    _("You're incredible... she's watching and she knows it."),

                    _("Look at her face... she can see how good you are."),

                    _("You feel amazing... give her something to be jealous of."),

                ],
                # ── Blackmail scene ──
                "_coerced": [
                    _("You're incredible, you know that? Even like this."),

                    _("Forget the video for a second... you feel amazing."),

                    _("You're better at this than you'll ever admit."),

                ],
            },
            "reactions": {
                "submissive": {
                    "lines": [_("Thank you... I'll keep doing exactly that. Tell me if it changes."), _("I'm... glad I did it right. Say it again? Only if you want."), _("Good... I'm good? Then I'll stay like this.")],
                    "stats": {"Obed": 4, "Inbt": 2},
                    "expression": "shy",
                },
                "_default": {
                    "lines": [_("Mmm... keep talking like that..."), _("You really think so...?"), _("Say it again..."), _("That makes me want you even more...")],
                    "stats": {"Love": 3, "Inbt": 2},
                    "expression": "happy",
                },
                # ── NTR partner watching ──
                "_ntr_watching": {
                    "lines": [_("Don't say that in front of %(po)s..."), _("%(name)s can hear every word, you know..."), _("This is so weird... but keep talking...")],
                    "stats": {"Love": 2, "Inbt": 3},
                    "expression": "shy",
                    "npc_stats": {"friendship_with_player": 10},
                    "npc_boundary_bar": 4,
                },
                "_ntr_watching_hardcore_sex": {
                    "lines": [_("Less sweet talk. %(name)s's watching. Show %(po)s how hard you can go."), _("Compliments? Now? Fuck me like %(pp)s's not even here."), _("Save it. Make me scream so %(pp)s hears THAT instead.")],
                    "stats": {"Obed": -1, "Inbt": 4},
                    "expression": "lipbite",
                    "npc_boundary_bar": 3,
                },
                "_ntr_watching_cute_sex": {
                    "lines": [_("That's sweet... but not with %(po)s listening... I'm so embarrassed..."), _("%(name)s... don't look at me while he says those things..."), _("My face is burning... say it quieter...")],
                    "stats": {"Love": 4, "Obed": 2},
                    "expression": "shy",
                    "npc_stats": {"friendship_with_player": 15},
                    "npc_boundary_bar": 6,
                },
                "_ntr_watching_exhibitionist": {
                    "lines": [_("Say it louder. I want %(po)s to hear exactly how good I am."), _("Mmm... praise me in front of %(po)s... I love being shown off..."), _("Tell %(po)s more. Tell %(po)s everything.")],
                    "stats": {"Inbt": 6, "Obed": 2},
                    "expression": "happy",
                    "npc_stats": {"friendship_with_player": 10},
                    "npc_boundary_bar": 6,
                },
                # ── Another girl watching ──
                "_girl_watching": {
                    "lines": [_("Shh... she's right there..."), _("Don't say that with her listening..."), _("You're only saying that because she's watching...")],
                    "stats": {"Love": 2, "Inbt": 3},
                    "expression": "shy",
                },
                "_girl_watching_hardcore_sex": {
                    "lines": [_("Talk later. Show her what you've got."), _("Good. Let her hear it. Now fuck me harder."), _("Say it again, louder. For her.")],
                    "stats": {"Inbt": 4, "Obed": 2},
                    "expression": "lipbite",
                },
                "_girl_watching_exhibitionist": {
                    "lines": [_("Let her hear every word... I love it..."), _("Keep going... I want her to know how good I am..."), _("Say it to her face if you want. I don't care.")],
                    "stats": {"Inbt": 6, "Obed": 2},
                    "expression": "happy",
                },
                # ── Blackmail scene ──
                "_coerced": {
                    "lines": [_("Don't. You don't get to be sweet while you're holding that video over me."), _("Compliments don't make this okay."), _("Save it. I'm here because of the video, not because of you.")],
                    "stats": {"Love": -2, "Inbt": 3},
                    "expression": "angry",
                },
                "_coerced_cute_sex": {
                    "lines": [_("Please don't say nice things... it makes this hurt more..."), _("You're blackmailing me... and now you're being kind? I can't..."), _("Don't... I don't want to like anything about this...")],
                    "stats": {"Love": -3, "Obed": 2},
                    "expression": "sad",
                },
                # ── Full Nelson hold ──
                "_fn_hardcore_sex": {
                    "lines": [_("Pinned and praised... keep holding me like this..."), _("Hold me tighter... and stop being so gentle about it..."), _("Mmm... compliments are nice... faster is nicer...")],
                    "stats": {"Obed": 3, "Inbt": 4},
                    "expression": "lipbite",
                },
                "_fn_submissive": {
                    "lines": [_("I can't move... so I'll just listen. Say more. Please."), _("You've got me. I'll stay exactly like this. Tell me I'm doing okay?"), _("Held like this... it's easier. I don't have to decide anything. Just tell me.")],
                    "stats": {"Obed": 3, "Inbt": 4},
                    "expression": "lipbite",
                },
                "_fn_cute_sex": {
                    "lines": [_("You're saying that while I can't even move... it's too much..."), _("I'm completely at your mercy and you're being sweet... I can't handle this..."), _("I can't hide my face like this... stop making me blush...")],
                    "stats": {"Love": 5, "Inbt": 2},
                    "expression": "shy",
                },
                "_fn": {
                    "lines": [_("You're saying that while you've got me pinned...?"), _("I can't even cover my face right now... that's not fair..."), _("Hard to argue when I literally can't move...")],
                    "stats": {"Love": 3, "Inbt": 3},
                    "expression": "shy",
                },
                "hardcore_sex": {
                    "lines": [_("Less talking, more fucking."), _("Shut up and go harder."), _("I don't need compliments, I need it deeper."), _("Sweet talk later. Fuck me now.")],
                    "stats": {"Obed": -2, "Inbt": 3},
                    "expression": "lipbite",
                },
                "cute_sex": {
                    "lines": [_("That's so sweet... you're making me blush..."), _("Stop... you're going to make me cry..."), _("You always know what to say..."), _("My heart is racing... say more...")],
                    "stats": {"Love": 5, "Inbt": 1},
                    "expression": "shy",
                },
                "nerd": {
                    "lines": [_("You're just saying that to distract me from the fact that we're doing THIS..."), _("Flattery won't get you a better grade... but it might get you something else..."), _("Nobody has ever complimented me during... you know... this is new data for me."), _("My heart rate just spiked. That's... empirically significant.")],
                    "stats": {"Love": 4, "Obed": 2},
                    "expression": "shy",
                },
                "gym_rat": {
                    "lines": [_("Keep that energy up and maybe I'll believe you."), _("Flattery's cheap. Stamina isn't. Show me."), _("You're sweating more than I do on leg day... cute."), _("Don't waste your breath. You'll need it.")],
                    "stats": {"Love": 2, "Inbt": 3},
                    "expression": "lipbite",
                },
            },
        },

        # ── HUMILIATE HER ────────────────────────────────────
        "humiliate": {
            "label": _("Humiliate her"),
            "available": _tease_always,
            "player_lines": {
                "_any": [
                    _("You like being used like this, don't you?"),

                    _("Say my name. Louder."),

                    _("That's all you're good for."),

                    _("Look at you... completely pathetic..."),

                    _("Beg me for it. Go on."),

                    _("You love being treated like trash, don't you?"),

                ],
                "reverse_cowgirl": [
                    _("Bounce that ass properly, slut."),

                    _("Harder, you dirty little whore."),

                    _("You're dripping all over the sheets. Disgusting."),

                    _("Push back harder. You call that riding?"),

                ],
                "cowgirl": [
                    _("Ride it like you mean it, slut."),

                    _("You call that bouncing? MOVE, BITCH!"),

                    _("Look at you... riding cock like a desperate whore..."),

                ],
                "bj": [
                    _("Deeper. Take it all, slut."),

                    _("Is that the best you can do with your mouth?"),

                    _("Good girl... now choke on it."),

                    _("You look so pathetic on your knees..."),

                ],
                "hj": [
                    _("Grip it tighter. You're barely trying."),

                    _("Faster. Like you actually want to make me cum."),

                ],
                "tj": [
                    _("Squeeze those tits together properly."),

                    _("Your tits are only good for this, you know that?"),

                ],
                "fj": [
                    _("I bet you never thought you'd be jerking someone off with your feet."),

                    _("Look at you... using your feet like some desperate foot slut."),

                ],
                "doggy": [
                    _("On all fours like a bitch in heat. Perfect."),

                    _("Face down, ass up. That's where you belong."),

                ],
                "full_nelson": [
                    _("Look at you, helpless and spread open. Pathetic."),

                    _("You can't even move. Just hang there and take it."),

                ],
                "laying_down": [
                    _("Lying there taking it like a good little toy."),

                    _("Spread your legs wider. You're not even trying."),

                ],
                "anal": [
                    _("Taking it in the ass like a cheap slut."),

                    _("Your ass was made for this. Admit it."),

                ],
                # ── NTR partner watching ──
                "_ntr_watching": [
                    _("Look at %(name)s while I use you. Go on."),

                    _("Say it so %(pp)s can hear. Tell %(po)s what you are."),

                    _("%(name)s gets to watch you be my little slut. Lucky %(po)s."),

                ],
                # ── Another girl watching ──
                "_girl_watching": [
                    _("Show her what a slut you really are."),

                    _("She's watching you get used. Say thank you."),

                    _("Moan louder. Let her hear how pathetic you sound."),

                ],
                # ── Blackmail scene ──
                "_coerced": [
                    _("You know you'd do anything to keep that video hidden. Anything."),

                    _("Remember whose fault it is you're here. Yours."),

                    _("Beg me to delete it. Go on. Beg while you take it."),

                ],
            },
            "reactions": {
                "hardcore_sex": {
                    "lines": [_("Mmm, I love when you talk dirty..."), _("Filthy mouth. Keep it coming, and fuck me harder."), _("Talk dirty all you want. Just don't you dare slow down.")],
                    "stats": {"Obed": 5, "Inbt": 5},
                    "expression": "lipbite",
                },
                "submissive": {
                    # deference, not appetite (the author 2026-10-11, the tester's own lines): a submissive girl
                    # ACCEPTS the word where the hardcore pool gets off on it. Obedience first, heat through it.
                    "lines": [_("...If that's what you think of me, then that's what I am."), _("I'm whatever you say I am."), _("Yes... I'll be your little slut, if that's what you want..."), _("I'll do anything you say... you know I will...")],
                    "stats": {"Obed": 6, "Inbt": 4},
                    "expression": "shy",
                },
                # ── NTR partner watching ──
                "_ntr_watching": {
                    "lines": [_("Not in front of %(po)s... please..."), _("%(name)s is right there... don't make me say it..."), _("Stop... %(pp)s can hear everything...")],
                    "stats": {"Obed": 4, "Inbt": 3},
                    "expression": "scared",
                    "npc_stats": {"friendship_with_player": -15},
                    "npc_boundary_bar": -2,
                },
                "_ntr_watching_hardcore_sex": {
                    "lines": [_("Harder. Make %(po)s watch what I let you do."), _("Dirty talk in front of %(po)s? Fine. Now fuck me harder so %(pp)s hears it."), _("Let %(name)s hear how rough you get with me. Don't hold back.")],
                    "stats": {"Obed": 6, "Inbt": 6},
                    "expression": "lipbite",
                    "npc_stats": {"friendship_with_player": -20},
                    "npc_boundary_bar": -3,
                },
                "_ntr_watching_submissive": {
                    "lines": [_("Yes... I'm your slut... and %(name)s can watch me prove it..."), _("Use me... let %(po)s see..."), _("I belong to you now... let %(name)s watch you own me...")],
                    "stats": {"Obed": 6, "Inbt": 6},
                    "expression": "lipbite",
                    "npc_stats": {"friendship_with_player": -20},
                    "npc_boundary_bar": -3,
                },
                "_ntr_watching_cute_sex": {
                    "lines": [_("Don't... not while %(pp)s's watching... please..."), _("%(name)s... don't listen to him..."), _("You're humiliating me in front of %(po)s... why...")],
                    "stats": {"Love": -6, "Obed": 3},
                    "expression": "sad",
                    "npc_stats": {"friendship_with_player": -30},
                    "npc_boundary_bar": -4,
                },
                "_ntr_watching_exhibitionist": {
                    "lines": [_("Mmm... degrade me in front of %(po)s... I love it..."), _("Yes... let %(name)s see what I really am..."), _("Say it louder so %(pp)s hears every word...")],
                    "stats": {"Inbt": 8, "Obed": 4},
                    "expression": "happy",
                    "npc_stats": {"friendship_with_player": -10},
                    "npc_boundary_bar": 2,
                },
                # ── Another girl watching ──
                "_girl_watching": {
                    "lines": [_("Not with her watching... please..."), _("She's going to think I'm... stop..."), _("Don't say that in front of her...")],
                    "stats": {"Obed": 3, "Inbt": 3},
                    "expression": "scared",
                },
                "_girl_watching_hardcore_sex": {
                    "lines": [_("Yes... let her see what a slut I am..."), _("Louder. I want her to hear it too.")],
                    "stats": {"Obed": 5, "Inbt": 6},
                    "expression": "lipbite",
                },
                "_girl_watching_submissive": {
                    "lines": [_("Use me in front of her... I don't care..."), _("Yes... tell her whose toy I am..."), _("I'll do whatever you say... even with her watching...")],
                    "stats": {"Obed": 5, "Inbt": 6},
                    "expression": "lipbite",
                },
                "_girl_watching_cute_sex": {
                    "lines": [_("Please... she's right there... don't..."), _("I can't look at her... stop saying that..."), _("Why would you humiliate me in front of her...")],
                    "stats": {"Love": -5, "Obed": 3},
                    "expression": "sad",
                },
                # ── Blackmail scene ──
                "_coerced": {
                    "lines": [_("You already have the video. Isn't that enough?"), _("I know why I'm here. You don't need to rub it in."), _("Say whatever you want. The second that video is gone, so am I.")],
                    "stats": {"Obed": 3, "Inbt": 4},
                    "expression": "angry",
                },
                "_coerced_cute_sex": {
                    "lines": [_("Please... you already won... don't make it worse..."), _("I'm doing what you want... stop..."), _("I hate this... I hate you... please just finish...")],
                    "stats": {"Love": -6, "Obed": 4},
                    "expression": "sad",
                },
                "_coerced_hardcore_sex": {
                    "lines": [_("Blackmail AND dirty talk? You're really committing."), _("Talk all you want. This is the only way you'd ever get me.")],
                    "stats": {"Obed": 3, "Inbt": 6},
                    "expression": "lipbite",
                },
                "_coerced_submissive": {
                    "lines": [_("Fine. I'm your slut for today. Tomorrow, delete the video."), _("You own me as long as you have that video. I know. I'll do what you say."), _("I hate that I like obeying you... even like this.")],
                    "stats": {"Obed": 3, "Inbt": 6},
                    "expression": "lipbite",
                },
                # ── Full Nelson hold ──
                "_fn_hardcore_sex": {
                    "lines": [_("Pinned and degraded... this is everything I wanted..."), _("Pinned like this and you're still talking? Fuck me harder..."), _("Say it while you pound me... don't you dare go easy...")],
                    "stats": {"Obed": 5, "Inbt": 6},
                    "expression": "lipbite",
                },
                "_fn_submissive": {
                    "lines": [_("I can't even fight back like this... I wouldn't. I'm whatever you say I am."), _("Held like this... okay. Yes. Say it again if you want. I'll take it."), _("I can't move, so... just tell me what I am. I'll agree.")],
                    "stats": {"Obed": 5, "Inbt": 6},
                    "expression": "lipbite",
                },
                "_fn_cute_sex": {
                    "lines": [_("I can't even push you away... please stop saying that..."), _("You're holding me so I can't move... and now this...? That's cruel..."), _("I'm stuck... I can't cover my ears or anything... please...")],
                    "stats": {"Love": -5, "Obed": 4},
                    "expression": "sad",
                },
                "_fn": {
                    "lines": [_("What am I supposed to do, fight you? I can't even move my arms..."), _("Easy to talk tough when you've got me pinned..."), _("I literally cannot push you away right now... you know that, right?"), _("You're real brave when I'm locked in a hold...")],
                    "stats": {"Obed": 4, "Inbt": 3},
                    "expression": "angry",
                },
                "cute_sex": {
                    "lines": [_("That's... that's mean..."), _("Why would you say that...?"), _("Don't say that... You are mean..."), _("I'm not... I'm not a..."), _("You're hurting my feelings...")],
                    "stats": {"Love": -5, "Obed": 3},
                    "expression": "sad",
                },
                "_default": {
                    "lines": [_("You're lucky I like you..."), _("Don't push it..."), _("Hmph... fine. But only because it feels good."), _("That mouth of yours is going to get you in trouble...")],
                    "stats": {"Obed": 3, "Inbt": 2},
                    "expression": "normal",
                },
                "nerd": {
                    "lines": [_("You think I haven't heard worse from my thesis advisor?"), _("I've survived peer review. Your insults are amateur hour."), _("Call me whatever you want. I still have a higher GPA than you."), _("That's... statistically the least creative thing you could have said.")],
                    "stats": {"Obed": 1, "Inbt": 3},
                    "expression": "angry",
                },
                "gym_rat": {
                    "lines": [_("Big words from a guy I could bench."), _("Say that again and I'll see how long you last in a chokehold."), _("Pathetic? I've out-lifted half your gym. Try harder."), _("Keep talking. I'm the one doing all the work here anyway.")],
                    "stats": {"Obed": 1, "Inbt": 3},
                    "expression": "angry",
                },
            },
        },

        # ── TALK ABOUT FILMING ───────────────────────────────
        "filming": {
            "label": _("Talk about filming her"),
            "available": _tease_always,
            "player_lines": {
                "_any": [
                    _("I should be recording this..."),

                    _("Imagine if your fans could see you right now..."),

                    _("You'd look so good on camera like this..."),

                    _("This would break the internet..."),

                    _("My phone is right there... just one video..."),

                ],
                "reverse_cowgirl": [
                    _("I want to film you moaning face down like that..."),

                    _("Your ass on camera from this angle... perfection..."),

                ],
                "cowgirl": [
                    _("I want to film you bouncing on me from below..."),

                    _("The way your tits move when you ride... that needs to be recorded..."),

                ],
                "bj": [
                    _("I want to film those lips wrapped around my cock..."),

                    _("Your blowjob face would get millions of views..."),

                ],
                "tj": [
                    _("I need to record your tits around my cock..."),

                ],
                "fj": [
                    _("Imagine if people saw you doing this with your feet..."),

                    _("A footjob video? That would get some interesting attention..."),

                ],
                "doggy": [
                    _("I want to film your ass bouncing back against me..."),

                    _("This angle from behind... I need it on video..."),

                ],
                "full_nelson": [
                    _("Spread open like this... that's a video people would pay for..."),

                    _("Imagine everyone seeing you pinned and helpless like this..."),

                ],
                "laying_down": [
                    _("Your face from up here... that needs to be recorded..."),

                    _("I want to film you lying there taking it..."),

                ],
                # ── NTR partner watching ──
                "_ntr_watching": [
                    _("%(name)s gets the live show... the camera should get the replay."),

                    _("I should film this for %(name)s. %(Pp)s could watch it every night."),

                    _("Imagine %(name)s rewatching this on %(poss)s phone later..."),

                ],
                # ── Blackmail scene ──
                "_coerced": [
                    _("One more video for the collection..."),

                    _("You know what? I should record this one too."),

                    _("More footage means more reasons for you to come back..."),

                ],
                # ── Lines when already recording ──
                "_recording": [
                    _("Smile for the camera, baby..."),

                    _("Everyone is gonna see this..."),

                    _("This video is going viral..."),

                    _("The camera loves you..."),

                    _("Keep going, the whole internet is watching..."),

                    _("You're putting on such a good show for the camera..."),

                ],
                "_recording_reverse_cowgirl": [
                    _("Look at how you move those hips for the camera..."),

                    _("Your ass looks incredible on film right now..."),

                    _("The camera is getting every single bounce..."),

                ],
                "_recording_cowgirl": [
                    _("You're riding harder because the camera is on, aren't you?"),

                    _("Everyone is gonna see you bouncing like that..."),

                    _("Your tits on camera from this angle... perfect content..."),

                ],
                "_recording_bj": [
                    _("You'll be all over the internet sucking my cock any minute now..."),

                    _("Your fans are gonna love watching you choke on it..."),

                    _("Those lips around my cock... and the camera is catching it all..."),

                ],
                "_recording_tj": [
                    _("Your tits wrapped around my cock, all on camera..."),

                    _("This titjob footage is gonna break records..."),

                ],
            },
            "reactions": {
                # ── When recording IS active ──
                "camera_lover_recording": {
                    "lines": [_("I know the camera is on... and I love it~"), _("Make sure you get my best angle..."), _("I'm giving you the performance of a lifetime right now..."), _("Post it. I dare you. I look amazing..."), _("I hope your followers are ready for this...")],
                    "stats": {"Inbt": 6, "Obed": 4},
                    "expression": "happy",
                },
                "camera_hater_recording": {
                    "lines": [_("You're ALREADY recording?! Turn that off NOW!"), _("Are you serious right now?! Delete that!"), _("I swear if you post that anywhere..."), _("I can't believe you're filming this! Stop!")],
                    "stats": {"Love": -5, "Obed": -3},
                    "expression": "angry",
                },
                "exhibitionist_recording": {
                    "lines": [_("Yes! Everyone is gonna see me like this and I LOVE it!"), _("Post it everywhere... I want the whole campus to know..."), _("I hope every single person sees me taking it like this...")],
                    "stats": {"Inbt": 10, "Obed": 6},
                    "expression": "happy",
                },
                "submissive_recording": {
                    "lines": [_("It's on...? Okay. Tell me where to look. I'll do what you say on camera too."), _("Okay. Filmed. Just... say what you want me to do and I'll do it.")],
                    "stats": {"Obed": 3, "Inbt": 4},
                    "expression": "shy",
                },
                "_default_recording": {
                    "lines": [_("W-wait, you're already recording?!"), _("Don't film my face! They can recognize me!"), _("Oh god... Just don't film my face!"), _("You better not post that anywhere...")],
                    "stats": {"Inbt": 3},
                    "expression": "surprised",
                },
                # ── Full Nelson hold (recording active) ──
                "_fn_camera_hater": {
                    "lines": [_("I can't even cover myself! Turn that off! I'm completely exposed!"), _("You're filming me pinned like this?! I can't hide ANYTHING!"), _("I can't move my arms to block the camera! This is so wrong!")],
                    "stats": {"Love": -5, "Obed": -2, "Inbt": 4},
                    "expression": "angry",
                },
                "_fn_camera_lover": {
                    "lines": [_("Get everything... every angle... I'm spread wide open and I love it~"), _("The camera sees all of me like this... pinned and taking it... perfect~"), _("I can't pose but who cares... this angle is incredible...")],
                    "stats": {"Inbt": 7, "Obed": 4},
                    "expression": "happy",
                },
                "_fn_submissive": {
                    "lines": [_("Filmed... like this? I can't even... okay. Okay. Whatever you want."), _("You've got me held and filmed... I'll do what you say. I can't do anything else anyway...")],
                    "stats": {"Obed": 4, "Inbt": 4},
                    "expression": "shy",
                },
                "_fn": {
                    "lines": [_("You'd film me like this...? I can't even cover my face..."), _("I'm pinned wide open and you want a camera on me...?"), _("I literally cannot hide from the lens right now...")],
                    "stats": {"Inbt": 4, "Obed": 2},
                    "expression": "scared",
                },
                # ── When NOT recording ──
                "camera_lover": {
                    "lines": [_("Hmm... maybe I'd look pretty good on camera~"), _("You'd like that, wouldn't you? ...Maybe one day."), _("The idea is tempting... but you'd have to ask nicely~"), _("I'm not saying no... just not right now.")],
                    "stats": {"Inbt": 3, "Obed": 1},
                    "expression": "shy",
                },
                "camera_hater": {
                    "lines": [_("Don't you DARE record this!"), _("If you even think about pulling out a camera..."), _("Absolutely not. This is private."), _("I will break your phone if you try."), _("Are you trying to ruin my life?!")],
                    "stats": {"Love": -3, "Obed": -2},
                    "expression": "angry",
                },
                "exhibitionist": {
                    "lines": [_("Mmm... the thought of everyone watching is hot..."), _("Maybe someday... you'd have to convince me first."), _("I like the idea... but talk is cheap. Ask me properly."), _("The thought of being on camera like this... it's tempting...")],
                    "stats": {"Inbt": 4, "Obed": 2},
                    "expression": "lipbite",
                },
                "submissive": {
                    "lines": [_("If you want to film it... okay. Tell me what to do and I'll do it for the camera."), _("You can. I'd... I'd rather you held it, so I know where to look."), _("Okay. Film me. Just say how you want me.")],
                    "stats": {"Obed": 4, "Inbt": 3},
                    "expression": "shy",
                },
                "_default": {
                    "lines": [_("Maybe... but not right now..."), _("You'd like that, wouldn't you? ...Maybe later."), _("Hmm... I'll think about it..."), _("You're terrible... but the idea is kind of hot...")],
                    "stats": {"Inbt": 2},
                    "expression": "shy",
                },
                "nerd": {
                    "lines": [_("If that video leaks, my academic career is OVER. Do you understand that?!"), _("One screenshot and I lose my scholarship, my recommendation letters, EVERYTHING."), _("The risk-reward ratio on that is catastrophically bad. For ME, not you!"), _("My professors follow me on social media. Think about that for a second.")],
                    "stats": {"Love": -4, "Obed": -2, "Inbt": 4},
                    "expression": "scared",
                },
                "gym_rat": {
                    "lines": [_("Film it. I've worked hard for this body. Let people see."), _("Sure. Just get my good side... all of them are good."), _("Post it in the gym group chat. Watch them all lose focus."), _("If you film me, you better film the flexing too.")],
                    "stats": {"Inbt": 4, "Obed": 1},
                    "expression": "happy",
                },
                # ── NTR partner watching ──
                "_ntr_watching_cam": {
                    "lines": [_("%(Pp)s already asked for videos... of course %(pp)s wants this too..."), _("%(name)s would love that... %(pp)s keeps the videos, you know..."), _("Fine... film it... %(pp)s's going to want a copy anyway...")],
                    "stats": {"Inbt": 5, "Obed": 3},
                    "expression": "lipbite",
                    "npc_stats": {"friendship_with_player": 15},
                    "npc_boundary_bar": 6,
                },
                "_ntr_watching": {
                    "lines": [_("A video? %(pp)s's RIGHT THERE. Isn't that enough for you?"), _("Don't film me in front of %(po)s..."), _("Watching is one thing... a video is different... %(name)s, say something...")],
                    "stats": {"Inbt": 3, "Obed": 1},
                    "expression": "surprised",
                    "npc_stats": {"friendship_with_player": -5},
                },
                "_ntr_watching_camera_lover": {
                    "lines": [_("Yes... film me while %(pp)s watches... I want both..."), _("Two audiences? God, that's hot... get my good side..."), _("%(name)s can watch live and rewatch later... I love it...")],
                    "stats": {"Inbt": 7, "Obed": 4},
                    "expression": "happy",
                    "npc_stats": {"friendship_with_player": 5},
                    "npc_boundary_bar": 4,
                },
                "_ntr_watching_camera_hater": {
                    "lines": [_("NO. %(name)s watching is already too much. No camera!"), _("Absolutely not! Isn't %(po)s seeing this bad enough?!"), _("Put that thought away. %(name)s agreed to watch, not to a movie!")],
                    "stats": {"Love": -4, "Obed": -2},
                    "expression": "angry",
                    "npc_stats": {"friendship_with_player": -5},
                    "npc_boundary_bar": -2,
                },
                # ── Blackmail scene ──
                "_coerced": {
                    "lines": [_("More videos? That's how this started..."), _("Of course you want more footage. That's all this is to you."), _("Film it. Whatever. You already own me with the first one.")],
                    "stats": {"Love": -3, "Obed": 4, "Inbt": 3},
                    "expression": "sad",
                },
            },
        },

        # ── HUMILIATE HER BOYFRIEND ──────────────────────────
        "bf_humiliate": {
            "label": _("Talk about her boyfriend"),
            "available": _tease_has_bf,
            "player_lines": {
                "_any": [
                    _("I bet he thinks you're home reading right now..."),

                    _("Does he know his girlfriend is getting fucked like this?"),

                    _("I bet he can't make you moan like that."),

                    _("You're mine now. He just doesn't know it yet."),

                    _("What would he think if he saw you right now?"),

                    _("He's probably texting you while you're taking my dick..."),

                    _("Poor guy has no idea what his girl does behind his back..."),

                ],
                "reverse_cowgirl": [
                    _("I bet your pussy is tighter for me than it ever was for him..."),

                    _("You bounce way better for me than you ever did for him."),

                    _("He has no idea you moan this loud..."),

                ],
                "cowgirl": [
                    _("You never ride him like this, do you?"),

                    _("I bet you just lay there when he fucks you..."),

                ],
                "bj": [
                    _("I bet you never suck him off like this..."),

                    _("Does he know how deep you can take it?"),

                    _("Your boyfriend's dick probably doesn't even reach this far..."),

                ],
                "hj": [
                    _("You never jerk him off this eagerly, do you?"),

                ],
                "tj": [
                    _("I bet he's never been between those tits..."),

                ],
                "fj": [
                    _("Does %(pl)s know you do this kind of thing?"),

                    _("I bet %(pp)s never asked you for a footjob..."),

                ],
                "doggy": [
                    _("I bet he never bends you over like this..."),

                    _("On all fours for me... does he even know you like it this way?"),

                ],
                "full_nelson": [
                    _("Could he even lift you like this? Didn't think so."),

                    _("Pinned and spread for another man... poor guy."),

                ],
                "laying_down": [
                    _("He'd never make you look like this... wrecked and loving it."),

                    _("Is this the face you make for him? ...Yeah, I didn't think so."),

                ],
                "anal": [
                    _("Does he know you give your ass away like this?"),

                    _("Your boyfriend never got this hole, did he?"),

                ],
                # ── He knows and allowed it (NTR active, not in the room) ──
                "_ntr_known": [
                    _("He agreed to this... what kind of man agrees to this?"),

                    _("He said yes... and you came running. Good girl."),

                    _("He knows exactly where you are right now. And he let you go."),

                    _("He gave you permission... like I needed it."),

                    _("I bet he's picturing exactly this right now... and hating how much he likes it."),

                ],
                "_ntr_known_bj": [
                    _("Did he also say yes to you sucking me this well?"),

                ],
                "_ntr_known_cowgirl": [
                    _("Does he know you ride like this when he's not around?"),

                ],
            },
            # Partner attitude defines her reaction before her sex style does
            "trait_priority": ["cheater", "loyal", "femdom", "submissive", "hardcore_sex", "cute_sex"],
            "reactions": {
                "cheater": {
                    "lines": [_("He has no idea... and that makes it so much hotter..."), _("He could never fuck me like you do..."), _("I don't even think about him when I'm with you..."), _("His dick doesn't even compare to yours..."), _("I'm such a bad girlfriend... and I love it...")],
                    "stats": {"Inbt": 8, "Obed": 3},
                    "expression": "lipbite",
                },
                "loyal": {
                    "lines": [_("Don't... don't talk about him right now..."), _("That's not fair... I feel guilty enough..."), _("Please stop... you're making this worse..."), _("I already hate myself for this... don't remind me...")],
                    "stats": {"Love": -3, "Obed": 2},
                    "expression": "sad",
                },
                "hardcore_sex": {
                    "lines": [_("Stop talking about him and fuck me like you mean it."), _("He's not here. You are. Act like it."), _("Forget him. Harder.")],
                    "stats": {"Inbt": 5, "Obed": 2},
                    "expression": "lipbite",
                },
                "cute_sex": {
                    "lines": [_("Please... don't bring him up... not now..."), _("That's not fair... I can't think about him while you're... doing this..."), _("Don't make me feel worse than I already do...")],
                    "stats": {"Love": -3, "Obed": 3},
                    "expression": "sad",
                },
                "submissive": {
                    "lines": [_("Don't... please don't make me say it. ...Okay. Yes. Yours. Not his."), _("I know. I know I'm here with you. Just tell me what you want me to say."), _("Yes... you. Not him. I'll say it if you want me to.")],
                    "stats": {"Obed": 5, "Inbt": 3},
                    "expression": "shy",
                },
                "_default": {
                    "lines": [_("You're terrible... but you're not wrong..."), _("Stop... he doesn't deserve this..."), _("Just... shut up and keep going..."), _("That's so wrong... why does it turn me on...")],
                    "stats": {"Inbt": 3, "Obed": 2},
                    "expression": "normal",
                },
                # ── He knows and allowed it ──
                "_ntr_known": {
                    "lines": [_("He agreed to this... that doesn't mean I want to hear about him."), _("He knows. He's okay with it. Can we leave it there?"), _("Don't make it weird. He let me come here. That's all.")],
                    "stats": {"Obed": 3, "Inbt": 3},
                    "expression": "shy",
                },
                "_ntr_known_cheater": {
                    "lines": [_("He knows... and he still can't do anything about it. That's the best part."), _("He said yes because he knows I'd do it anyway..."), _("Poor thing thinks permission makes him part of this...")],
                    "stats": {"Inbt": 7, "Obed": 3},
                    "expression": "lipbite",
                },
                "_ntr_known_loyal": {
                    "lines": [_("He's being so understanding... don't mock him for it..."), _("He trusts me enough to let me do this. Don't make me regret it."), _("He gave me this... the least you can do is leave him out of it.")],
                    "stats": {"Love": -2, "Obed": 2},
                    "expression": "sad",
                },
                "_ntr_known_hardcore_sex": {
                    "lines": [_("He knows exactly what I'm doing. Now shut up and prove he made the right call."), _("He gave me a hall pass. Stop wasting it talking."), _("Yeah, he said yes. So make it worth it.")],
                    "stats": {"Inbt": 5, "Obed": 3},
                    "expression": "lipbite",
                },
                "_ntr_known_cute_sex": {
                    "lines": [_("Don't tease him... he's trying so hard to make this work for us..."), _("He said yes because he loves me... don't twist it..."), _("Please... he's being so sweet about it... don't...")],
                    "stats": {"Love": -2, "Obed": 3},
                    "expression": "sad",
                },
            },
        },

        # ── TALK ABOUT HER HUSBAND (netori: a married girl, trait "married") ──
        # Heavier than the boyfriend tease on purpose: vows, the ring, HIS bed. The husband is a fixed word
        # (a married girl always has one), never %(pl)s: she has no NPC partner to fill the keys.
        "husband_humiliate": {
            "label": _("Talk about her husband"),
            "available": _tease_has_husband,
            "player_lines": {
                "_any": [
                    _("Does your husband know where his wife is right now?"),

                    _("You promised that man forever... and look at you now."),

                    _("Another man's wife... and you still came to me."),

                    _("He gets the ring. I get everything under it."),

                    _("His side of the bed is cold tonight... and you don't even feel bad, do you?"),

                    _("Say 'my husband'. Go on. Say it while you're doing this."),

                    _("I'm not borrowing you from him. I'm keeping you. He just hasn't been told."),

                ],
                "hj": [
                    _("That hand has a wedding ring on it... look at it while you stroke me."),

                    _("Married hands work better. Who knew?"),

                ],
                "bj": [
                    _("Is that the mouth that said 'I do'?"),

                    _("A married woman on her knees for me... he really lost you already, didn't he?"),

                ],
                "tj": [
                    _("His wife's tits around another man... he'd lose his mind."),

                ],
                "rj": [
                    _("Does your husband even know you DO this? ...No. This one's only mine."),

                ],
                "fj": [
                    _("These feet walk around his house all day... and end up here."),

                ],
                "cowgirl": [
                    _("Ride me like you rode him on the honeymoon. ...No. Better."),

                    _("Does he even get this anymore? ...Didn't think so."),

                ],
                "reverse_cowgirl": [
                    _("His wife bounces for me now. That's just how it is."),

                ],
                "doggy": [
                    _("Bent over for a man who isn't your husband... and you didn't even hesitate."),

                    _("If he saw his wife like this, it would kill him. Arch your back."),

                ],
                "anal": [
                    _("Did your husband ever get this hole? ...Then it was never his."),

                ],
                "full_nelson": [
                    _("If your husband walked in right now, I wouldn't stop. And neither would you."),

                ],
                "laying_down": [
                    _("Wrecked, married, and mine. In that order."),

                ],
                # ── Her husband is the player's FAMILY (his father): the betrayal is inside the house ──
                "_family_husband": [
                    _("You're not just cheating on your husband... you're doing it with his SON."),

                    _("My father kissed you goodbye this morning. Look where his wife ended up."),

                    _("Say it. 'I'm your stepmother.' Say it exactly like that, right now."),

                    _("He brought you into this family. I'm just... keeping you in it."),

                    _("Every Sunday dinner, you'll sit across from me and remember exactly this."),

                    _("Dad still has no idea his wife belongs to his son."),

                    _("His ring on your finger, his son inside his marriage. And you let it happen."),

                    _("The family photos are going to be so much fun from now on."),

                ],
                "_family_husband_hj": [
                    _("That's the hand with my father's ring on it... jerking off his son."),

                ],
                "_family_husband_bj": [
                    _("The same mouth that calls him 'darling' at dinner..."),

                    _("My father's wife, on her knees for his son. Hold that thought while you swallow."),

                ],
                "_family_husband_tj": [
                    _("My father's wife, using her tits on his son... say that sentence in your head."),

                ],
                "_family_husband_rj": [
                    _("Does Dad get this? ...No? Only the son. Good."),

                ],
                "_family_husband_fj": [
                    _("Family dinners under the table are never going to feel the same."),

                ],
                "_family_husband_cowgirl": [
                    _("Riding your stepson... does this count as family bonding?"),

                ],
                "_family_husband_reverse_cowgirl": [
                    _("If he came home early, he'd find his wife bouncing on his son."),

                ],
                "_family_husband_doggy": [
                    _("On all fours in the family home... Dad's wife, taking his son."),

                ],
                "_family_husband_anal": [
                    _("Dad never got this... but his SON did. Think about that."),

                ],
                "_family_husband_full_nelson": [
                    _("His son holds his wife like this... and she lets him."),

                ],
                "_family_husband_laying_down": [
                    _("Spread out for your stepson... family suits you."),

                ],
            },
            # Partner attitude first, then her dominance, then her sex style
            "trait_priority": ["cheater", "loyal", "femdom", "submissive", "hardcore_sex", "cute_sex"],
            "reactions": {
                "cheater": {
                    "lines": [_("He bores me. You don't. It really is that simple..."), _("I stopped feeling married the first time you touched me..."), _("The ring stays on... everything else is already yours..."), _("My marriage is a contract. THIS is what I actually signed up for...")],
                    "stats": {"Inbt": 9, "Obed": 3},
                    "expression": "lipbite",
                },
                "loyal": {
                    "lines": [_("I made VOWS... I stood there and made vows, and now look at me..."), _("Don't say 'husband'... I can't hear that word right now..."), _("I'm someone's WIFE... what am I doing... don't stop..."), _("Stop it... the guilt is the only thing louder than you...")],
                    "stats": {"Love": -4, "Obed": 3},
                    "expression": "sad",
                },
                "femdom": {
                    "lines": [_("Careful, boy. My marriage is mine to mock, not yours."), _("He is not in this room. I decide who is. Focus on your job."), _("My husband is my business. Your business is right here, and you're slacking."), _("Bold mouth. One more word about him and you finish yourself.")],
                    "stats": {"Inbt": 6, "Obed": 2},
                    "expression": "smug",
                },
                "submissive": {
                    "lines": [_("I know... I'm a terrible wife... say it again, please..."), _("Yes... his wife is yours now... whatever you want..."), _("Don't make me think about him... just tell me what to do...")],
                    "stats": {"Obed": 6, "Inbt": 4},
                    "expression": "shy",
                },
                "hardcore_sex": {
                    "lines": [_("Then take me like you're taking me FROM him. Properly."), _("He's not here. You are. Make the difference obvious."), _("Less talk about my husband, more reasons to forget I have one.")],
                    "stats": {"Inbt": 6, "Obed": 2},
                    "expression": "lipbite",
                },
                "cute_sex": {
                    "lines": [_("Don't say 'husband' while you're being this gentle with me... that's cruel..."), _("Please... not his name... not while you're holding me like this..."), _("You can't be sweet and say things like that... pick one...")],
                    "stats": {"Love": -3, "Obed": 3},
                    "expression": "sad",
                },
                "_default": {
                    "lines": [_("You're awful... don't stop..."), _("That's cruel... so why did my whole body just answer you..."), _("Leave him out of this... and keep going..."), _("One day you'll say that and I won't flinch. ...Not yet...")],
                    "stats": {"Inbt": 4, "Obed": 2},
                    "expression": "normal",
                },
                # ── Her husband is the player's FAMILY (his father): her answers own the taboo, not just the affair ──
                "_family_husband_cheater": {
                    "lines": [_("Cheating was never the thrill. The thrill is that you're HIS. His blood, his name, his roof..."), _("I married the father and chose the son... every woman should plan this well..."), _("The closer to home, the better it feels. And you live down the hall...")],
                    "stats": {"Inbt": 10, "Obed": 3},
                    "expression": "lipbite",
                },
                "_family_husband_loyal": {
                    "lines": [_("His SON... of everyone on this earth, his own son... what is wrong with me..."), _("This isn't an affair, it's his FAMILY... I'm breaking his whole life from inside it..."), _("Don't say 'father'... I set his plate at that table every Sunday...")],
                    "stats": {"Love": -5, "Obed": 3},
                    "expression": "sad",
                },
                "_family_husband_femdom": {
                    "lines": [_("Careful with 'stepmother' in that mouth, boy. ...Say it again. Slower."), _("I run this family. The house, the marriage... and now its son. Keep up."), _("Yes. His son. Under his roof. If I wanted an ordinary affair, I would have had one."), _("Family is just another thing I own, boy. You're the proof.")],
                    "stats": {"Inbt": 7, "Obed": 2},
                    "expression": "smug",
                },
                "_family_husband_submissive": {
                    "lines": [_("I'm a terrible wife and a worse stepmother... tell me again..."), _("His son gives me orders now... and I follow them... what have I become..."), _("The family's good wife, doing THIS... use that against me...")],
                    "stats": {"Obed": 7, "Inbt": 4},
                    "expression": "shy",
                },
                "_family_husband_hardcore_sex": {
                    "lines": [_("Then stop talking about the family and RUIN his wife properly."), _("The son takes what the father couldn't handle. Prove it."), _("You want the taboo? Earn it. Harder.")],
                    "stats": {"Inbt": 7, "Obed": 2},
                    "expression": "lipbite",
                },
                "_family_husband_cute_sex": {
                    "lines": [_("Don't say 'stepmother' while you're being this sweet... it breaks something in me..."), _("We're family... we're FAMILY and you're holding me like this..."), _("Not the dinners, not the house... don't. Just stay close...")],
                    "stats": {"Love": -3, "Obed": 3},
                    "expression": "sad",
                },
                "_family_husband": {
                    "lines": [_("His son... I know exactly whose son you are... and I'm still here..."), _("That's the worst thing you could have said... say it again..."), _("This family is already broken where it matters... keep going..."), _("One word about your father and my whole body answers. You noticed. Of course you noticed...")],
                    "stats": {"Inbt": 5, "Obed": 2},
                    "expression": "normal",
                },
            },
        },

        # ── THREATEN TO CUM INSIDE ───────────────────────────
        "cum_threat": {
            "label": _("Threaten to cum inside"),
            "available": _tease_penetration,
            "player_lines": {
                "_any": [
                    _("I'm going to fill you up..."),

                    _("I'm not pulling out this time..."),

                    _("You're going to take every drop..."),

                    _("I want to cum deep inside you..."),

                ],
                "reverse_cowgirl": [
                    _("I'm going to cum so deep inside you from back here..."),

                    _("I can feel it coming... and it's all going inside you..."),

                    _("You can't escape it in this position..."),

                ],
                "cowgirl": [
                    _("Ride it out... I'm cumming inside you..."),

                    _("Don't you dare get off... I'm filling you up..."),

                    _("You're going to milk every drop out of me..."),

                ],
                "doggy": [
                    _("I'm going to push it all the way in and cum..."),

                    _("You can't stop me from this position... it's all going inside..."),

                    _("I'm going to fill you up from behind..."),

                ],
                "anal": [
                    _("I'm going to cum deep in your ass..."),

                    _("Your ass is going to be full of my cum..."),

                    _("I'm not pulling out of your ass... take it all..."),

                ],
                "full_nelson": [
                    _("You can't move... you can't stop me... it's all going inside you..."),

                    _("Pinned like this, you're taking every drop..."),

                ],
                "laying_down": [
                    _("I'm going to hold you down and fill you up..."),

                    _("Wrap your legs around me... I'm cumming inside..."),

                ],
                # ── Condom on ──
                "_condom": [
                    _("This condom is coming off before I cum..."),

                    _("I'm going to slip it off and you won't even notice..."),

                    _("You think a condom is going to stop me? I'll fill you up anyway."),

                ],
                # ── NTR partner watching: creampie NOT allowed by his boundary ──
                "_ntr_watching_no": [
                    _("%(name)s said no creampie... but %(pp)s can't stop me from here."),

                    _("I'm going to cum inside you right in front of %(po)s..."),

                    _("Let's see if %(name)s stops me when I fill you up."),

                ],
                # ── NTR partner watching: creampie allowed (no limits) ──
                "_ntr_watching_ok": [
                    _("%(name)s said I could... so I'm filling you up while %(pp)s watches."),

                    _("Every drop, deep inside you... and %(name)s gets to see it all."),

                    _("Look at %(po)s while I cum inside you."),

                ],
                # ── Blackmail scene ──
                "_coerced": [
                    _("Maybe I'll cum inside... you're in no position to say no."),

                    _("You'll take it wherever I decide. Remember that."),

                    _("I'm going to finish inside you... and you'll thank me for keeping the video private."),

                ],
            },
            "reactions": {
                "cum_slut": {
                    "lines": [_("Yes! Do it! Fill me up! I want it all..."), _("Please... cum inside me... I need it..."), _("Don't hold back... give me everything..."), _("I want to feel you explode inside me...")],
                    "stats": {"Inbt": 8, "Obed": 5},
                    "expression": "happy",
                },
                # ── Condom on ──
                "_condom": {
                    "lines": [_("You're wearing a condom, genius."), _("Go ahead, fill it up. That's what it's for."), _("Nice try. The condom stays on.")],
                    "stats": {"Inbt": 2, "Obed": 1},
                    "expression": "normal",
                },
                "_condom_cum_slut": {
                    "lines": [_("Then take it off... I want to actually feel it..."), _("Stop teasing and lose the condom already..."), _("Filling a condom doesn't count. Give it to me for real.")],
                    "stats": {"Inbt": 6, "Obed": 3},
                    "expression": "lipbite",
                },
                "_condom_hate_cum": {
                    "lines": [_("That's what the condom is for. Don't you DARE take it off."), _("Keep it on. I mean it. Not a single drop touches me."), _("Touch that condom and we're done. Understood?")],
                    "stats": {"Love": -2, "Obed": -1},
                    "expression": "angry",
                },
                # ── NTR partner watching: creampie NOT allowed ──
                "_ntr_watching_no": {
                    "lines": [_("No! %(name)s said not inside! %(Pp)s's watching, don't you dare!"), _("Don't... %(pp)s will never forgive me... pull out when it's time..."), _("%(name)s, say something! He can't cum inside me!")],
                    "stats": {"Obed": 2, "Inbt": 4},
                    "expression": "scared",
                    "npc_stats": {"friendship_with_player": -20},
                    "npc_boundary_bar": -5,
                },
                "_ntr_watching_no_cum_slut": {
                    "lines": [_("%(name)s said no... but god, I want it... don't make me choose..."), _("Not inside... %(pp)s's watching... even if I want it so bad..."), _("%(name)s, I'm sorry... I can't stop him... I don't want to...")],
                    "stats": {"Inbt": 7, "Obed": 4},
                    "expression": "lipbite",
                    "npc_stats": {"friendship_with_player": -25},
                    "npc_boundary_bar": -5,
                },
                "_ntr_watching_no_hate_cum": {
                    "lines": [_("Absolutely NOT! %(name)s said no and so do I! Pull out!"), _("Don't you DARE. %(name)s is right there and I will scream."), _("If you cum inside me in front of %(po)s, I'll never touch you again.")],
                    "stats": {"Love": -5, "Obed": -3},
                    "expression": "angry",
                    "npc_stats": {"friendship_with_player": -15},
                    "npc_boundary_bar": -3,
                },
                # ── NTR partner watching: creampie allowed ──
                "_ntr_watching_ok": {
                    "lines": [_("%(Pp)s said yes... do it... let %(po)s watch you fill me..."), _("%(name)s, look... he's going to cum inside me... and you allowed it..."), _("Inside... while %(pp)s watches... this is so wrong...")],
                    "stats": {"Inbt": 6, "Obed": 4},
                    "expression": "lipbite",
                    "npc_stats": {"friendship_with_player": 5},
                },
                "_ntr_watching_ok_hate_cum": {
                    "lines": [_("%(pp)s said you could. I DIDN'T. Pull out!"), _("I don't care what %(name)s allowed, not inside me!"), _("%(Pp)s doesn't get to decide that for me! Don't you dare!")],
                    "stats": {"Love": -5, "Obed": -3},
                    "expression": "angry",
                    "npc_stats": {"friendship_with_player": -5},
                },
                "_ntr_watching_ok_cum_slut": {
                    "lines": [_("Yes! %(pp)s said yes! Fill me up while %(pp)s watches!"), _("Do it... I want %(name)s to see me dripping with your cum..."), _("Cum inside me... right in front of %(po)s... please...")],
                    "stats": {"Inbt": 9, "Obed": 5},
                    "expression": "happy",
                    "npc_stats": {"friendship_with_player": 5},
                },
                # ── Blackmail scene ──
                "_coerced": {
                    "lines": [_("You wouldn't... that wasn't part of this..."), _("Please... the video... you said just this... not inside..."), _("Don't... I'll do anything else... not that...")],
                    "stats": {"Love": -4, "Obed": 4, "Inbt": 4},
                    "expression": "scared",
                },
                "_coerced_cum_slut": {
                    "lines": [_("...Fine. Do it. At least that part I'd want anyway."), _("Inside? You don't even need the video for that one..."), _("God... I hate that I want that...")],
                    "stats": {"Inbt": 6, "Obed": 3},
                    "expression": "lipbite",
                },
                "hate_cum": {
                    "lines": [_("Don't you DARE! Pull out or I'll kill you!"), _("If you cum inside me I swear to god..."), _("NO! Absolutely not! Are you insane?!"), _("I will NEVER forgive you if you do that!")],
                    "stats": {"Love": -5, "Obed": -3},
                    "expression": "angry",
                },
                # ── Full Nelson hold ──
                "_fn_cum_slut": {
                    "lines": [_("I can't stop you... and I don't want to... fill me up while I'm pinned..."), _("I'm trapped... do it... I want every drop while I can't move..."), _("I can't even squirm away... just do it... please...")],
                    "stats": {"Inbt": 9, "Obed": 6},
                    "expression": "happy",
                },
                "_fn_hate_cum": {
                    "lines": [_("No! I can't even move! Don't you dare! This isn't fair!"), _("You're holding me so I can't pull away! That's... no! PULL OUT!"), _("I can't stop you like this and you KNOW it! Don't!")],
                    "stats": {"Love": -6, "Obed": -2},
                    "expression": "angry",
                },
                "_fn_submissive": {
                    "lines": [_("I can't stop you like this... I wouldn't anyway. Wherever you want it."), _("Held like this... it's your call. It was always your call. Just tell me.")],
                    "stats": {"Obed": 5, "Inbt": 4},
                    "expression": "shy",
                },
                "_fn": {
                    "lines": [_("I can't even get away if you do it... you know that, right?"), _("You've got me locked... I literally cannot stop you..."), _("That's not fair... I can't move at all right now..."), _("You'd really do that while I'm completely helpless...?")],
                    "stats": {"Inbt": 5, "Obed": 2},
                    "expression": "scared",
                },
                "_cum_veteran": {
                    "lines": [_("Again...? You already did it before..."), _("You already came inside me once... what's one more time..."), _("Fine... it's not like you haven't already..."), _("You've already ruined me... just do it...")],
                    "stats": {"Inbt": 5, "Obed": 3},
                    "expression": "lipbite",
                },
                "submissive": {
                    "lines": [_("Wherever you decide... just tell me first? Please?"), _("Inside, outside... it's your choice. I'll take it wherever you say."), _("Okay. Wherever you want. Tell me and I'll be ready.")],
                    "stats": {"Obed": 4, "Inbt": 4},
                    "expression": "shy",
                },
                "_default": {
                    "lines": [_("You better be joking..."), _("Don't... don't say things like that..."), _("You wouldn't... right?"), _("That's... terrifying and hot at the same time...")],
                    "stats": {"Inbt": 3},
                    "expression": "surprised",
                },
                "nerd": {
                    "lines": [_("I tracked my cycle and today is NOT safe! Do you even understand biology?!"), _("Do you know what a pregnancy would do to my research timeline?!"), _("I have a THESIS to finish! A baby is NOT in the project plan!"), _("I calculated the probability and it's way too high. Pull out!"), _("The pill is 99 percent effective, and I refuse to be the other 1 percent! Pull out!"), _("My chart says today is a low risk day, and that is still NOT permission!")],
                    "stats": {"Love": -3, "Obed": -1, "Inbt": 5},
                    "expression": "scared",
                },
                "gym_rat": {
                    "lines": [_("Do it and you're doing burpees until you puke."), _("Inside me?! I have a competition in two weeks, are you insane?!"), _("Pull out, or I swear I'll squeeze until you can't."), _("You don't get to decide that. I can outlast you any day.")],
                    "stats": {"Inbt": 4, "Obed": -1},
                    "expression": "angry",
                },
            },
            "reactions_anal": {
                "cum_slut": {
                    "lines": [_("Yes! Cum in my ass! Fill it up!"), _("I want to feel your cum deep in my ass..."), _("Don't hold back... give my ass everything...")],
                    "stats": {"Inbt": 8, "Obed": 5},
                    "expression": "happy",
                },
                # ── Condom on ──
                "_condom": {
                    "lines": [_("It's in a condom. Cum wherever you want in there."), _("The condom stays on. Do what you need to do."), _("Fine. It's not like it's going anywhere.")],
                    "stats": {"Inbt": 2, "Obed": 2},
                    "expression": "normal",
                },
                # ── NTR partner watching (anal only happens at 'no limits') ──
                "_ntr_watching_ok": {
                    "lines": [_("%(Pp)s said anything goes... so cum in my ass while %(pp)s watches..."), _("%(name)s, look what he's about to do to my ass..."), _("Deep in my ass... in front of %(po)s... do it...")],
                    "stats": {"Inbt": 7, "Obed": 4},
                    "expression": "lipbite",
                    "npc_stats": {"friendship_with_player": 5},
                },
                # ── Blackmail scene ──
                "_coerced": {
                    "lines": [_("In my ass?! That's... please, no... that wasn't the deal..."), _("You're already in my ass because of that video... not inside too..."), _("Please... anywhere but in there...")],
                    "stats": {"Love": -4, "Obed": 4, "Inbt": 4},
                    "expression": "scared",
                },
                "anal_lover": {
                    "lines": [_("Do it... cum in my ass... I want it so bad..."), _("Fill my ass... please... I need to feel it...")],
                    "stats": {"Inbt": 8, "Obed": 5},
                    "expression": "happy",
                },
                "hate_cum": {
                    "lines": [_("Not in my ass! That's even worse!"), _("Don't you dare cum in there! Pull out!"), _("NO! I don't want your cum anywhere inside me!")],
                    "stats": {"Love": -5, "Obed": -3},
                    "expression": "angry",
                },
                "anal_hater": {
                    "lines": [_("You're already in my ass and now you want to cum in it too?!"), _("Haven't you done enough to my ass?! Pull out!"), _("My ass can't take any more of this...")],
                    "stats": {"Love": -3, "Obed": -2},
                    "expression": "angry",
                },
                # Keyed off CreampieCounts (any creampie), so no claims about anal history
                "_cum_veteran": {
                    "lines": [_("You've already cum inside me before... might as well be my ass this time..."), _("Fine... you've filled me up before, why stop at my ass..."), _("You already came inside me once... whatever... do it...")],
                    "stats": {"Inbt": 5, "Obed": 3},
                    "expression": "lipbite",
                },
                "submissive": {
                    "lines": [_("In there...? If that's what you want. Tell me when."), _("Okay. Wherever you decide. I'll stay still for it.")],
                    "stats": {"Obed": 4, "Inbt": 4},
                    "expression": "shy",
                },
                "_default": {
                    "lines": [_("In my ass...? You're serious...?"), _("That's... I don't even know how to feel about that..."), _("You want to cum in my butt...? That's so dirty...")],
                    "stats": {"Inbt": 3},
                    "expression": "surprised",
                },
            },
        },

        # ── TALK ABOUT BREEDING ─────────────────────────────────
        # ONE tease since 2026-09-19. "Threaten to knock her up" (breed_threat) had the same availability, the same
        # trait priority and near-identical pools (author: "sao basicamente a mesma coisa"): every line of it lives
        # here now. Stats are the ones this tease always had; pregnancy_fear answers scared (her pleading lines).
        "breed_talk": {
            "label": _("Talk about getting her pregnant"),
            "available": _tease_breed,
            "trait_priority": ["pregnancy_fetish", "pregnancy_fear", "cum_slut", "hate_cum", "submissive", "nerd", "gym_rat"],
            "player_lines": {
                "_any": [
                    _("I want to get you pregnant..."),

                    _("Imagine carrying my baby..."),

                    _("Let's make a baby together..."),

                    _("I want to put a baby inside you..."),

                    _("I'm going to get you pregnant tonight..."),

                    _("You're going to have my baby whether you like it or not..."),

                    _("I'm not stopping until I knock you up..."),

                    _("By the time I'm done, you'll be carrying my child..."),

                ],
                "cowgirl": [
                    _("Keep riding... I want you to ride me until you're pregnant..."),

                    _("Bounce on me until I put a baby in you..."),

                    _("Keep bouncing... I'm going to breed you in this position..."),

                    _("You can't get off until I knock you up..."),

                ],
                "reverse_cowgirl": [
                    _("I'm going to fill you up and make you a mother..."),

                    _("You're going to ride until I breed you..."),

                    _("You're going to ride until you're pregnant... no stopping."),

                ],
                "doggy": [
                    _("I'm going to breed you like this... from behind..."),

                    _("This is how I'm going to get you pregnant..."),

                    _("This is how nature intended it... I'm breeding you tonight."),

                    _("From behind like this, every drop is going deep..."),

                ],
                "full_nelson": [
                    _("Pinned like this... you're going to take my seed..."),

                    _("You can't move... perfect position to breed you..."),

                    _("Pinned and helpless... perfect for breeding..."),

                    _("You can't escape... I'm going to knock you up right now..."),

                ],
                "laying_down": [
                    _("I want to hold you close and put a baby in you..."),

                    _("Wrap your legs around me... I'm making you a mother..."),

                    _("I'm going to hold you down and breed you..."),

                    _("Legs wrapped around me... you're not going anywhere until I knock you up."),

                ],
                "_coerced": [
                    _("Maybe I'll get you pregnant... you're in no position to stop me."),

                    _("Imagine explaining a baby from the guy blackmailing you..."),

                    _("I might just get you pregnant for good measure..."),

                    _("Imagine having my baby because of a little video..."),

                ],
                "_ntr_watching": [
                    _("I'm going to get her pregnant while you watch, %(name)s."),

                    _("%(name)s, your girl is going to have my baby."),

                    _("Watch me breed your girl, %(name)s."),

                    _("%(name)s is going to watch me knock you up."),

                ],
            },
            "reactions": {
                "pregnancy_fetish": {
                    "lines": [_("Yes... please... I want you to get me pregnant..."), _("Put a baby in me... I've been dreaming about this..."), _("I want it so bad... make me a mother..."), _("Say it again... tell me you want to breed me..."), _("Do it! Get me pregnant! I want your baby!"), _("Yes! Breed me! Don't hold back!"), _("Knock me up... please... I need it..."), _("I want to feel you make me a mother...")],
                    "stats": {"Inbt": 8, "Obed": 5, "Love": 3},
                    "expression": "happy",
                },
                "pregnancy_fear": {
                    "lines": [_("That's NOT funny! Don't even joke about that!"), _("Stop! You're scaring me! I don't want a baby!"), _("If you're trying to freak me out, it's working! Stop!"), _("I swear, if you get me pregnant, I'll never forgive you!"), _("NO! Pull out! I can't get pregnant! PLEASE!"), _("Stop! You're scaring me! Don't do this!"), _("I'll do anything else, just don't get me pregnant!"), _("Please, not that! Anything but a baby!")],
                    "stats": {"Love": -5, "Obed": -3},
                    "expression": "scared",
                },
                "cum_slut": {
                    "lines": [_("Getting me pregnant...? That's... actually kind of hot..."), _("Mmm... fill me up and knock me up? Don't tempt me..."), _("You want to breed me? God, why does that turn me on..."), _("Say it again... tell me you'll cum inside me and make a baby..."), _("Knock me up...? Oh god, I shouldn't want that..."), _("Do it... breed me... I want to feel you cum inside..."), _("Fill me up and make me pregnant... why is that so hot..."), _("I can't believe how much I want that...")],
                    "stats": {"Inbt": 6, "Obed": 3},
                    "expression": "lipbite",
                },
                "_coerced": {
                    "lines": [_("A baby?! You can't be serious... that's way beyond..."), _("Getting me pregnant because of a video?! You're insane!"), _("Please... anything but that... don't get me pregnant..."), _("Pregnant?! That's... you can't... this is insane!"), _("A baby from blackmail?! You're a monster!"), _("Please no... the video is bad enough... not a baby...")],
                    "stats": {"Love": -5, "Obed": 3, "Inbt": 5},
                    "expression": "scared",
                },
                "_coerced_pregnancy_fetish": {
                    "lines": [_("I... I hate that I want you to... even like this..."), _("The video... and now a baby... why do I want it..."), _("You're blackmailing me and I still want you to breed me... I'm broken.")],
                    "stats": {"Inbt": 7, "Obed": 5},
                    "expression": "lipbite",
                },
                "_ntr_watching": {
                    "lines": [_("Don't say that in front of %(po)s! %(Pp)s'll kill you!"), _("%(name)s, he's lying! He won't really..."), _("Please, not in front of %(po)s... don't talk about babies..."), _("%(name)s, stop him! He's going to get me pregnant!"), _("No! Not in front of %(po)s! Don't knock me up!"), _("%(name)s, do something! He's trying to breed me!")],
                    "stats": {"Obed": 3, "Inbt": 5},
                    "expression": "scared",
                    "npc_stats": {"friendship_with_player": -25},
                },
                "_ntr_watching_pregnancy_fetish": {
                    "lines": [_("Do it... breed me in front of %(po)s... I don't care anymore..."), _("Let %(name)s watch you knock me up... I want it..."), _("%(name)s can watch... just breed me already...")],
                    "stats": {"Inbt": 9, "Obed": 5},
                    "expression": "lipbite",
                    "npc_stats": {"friendship_with_player": -30},
                },
                "nerd": {
                    "lines": [_("Do you understand the biological and financial implications of what you just said?!"), _("A baby would derail my academic career for years!"), _("I'm tracking my cycle specifically to PREVENT this from becoming reality!"), _("This is the WORST time in my cycle! You CAN'T do this!"), _("The probability of conception right now is... no, STOP!"), _("My research! My degree! You can't just BREED me!"), _("I take my pill at the same minute every day precisely so THIS can't happen!"), _("Statistically I'm in my safe window, but I am not testing that hypothesis with you!")],
                    "stats": {"Inbt": 5, "Obed": -1},
                    "expression": "scared",
                },
                "gym_rat": {
                    "lines": [_("Pregnant?! Do you know what that does to a body?!"), _("Nine months of no training?! Are you out of your mind?!"), _("I've been working on this body for YEARS and you want to ruin it?!"), _("Get me pregnant?! I'll break you in half first!"), _("My body is a TEMPLE and you want to knock me up?!"), _("Try it and see what happens. I dare you.")],
                    "stats": {"Inbt": 4, "Obed": -1},
                    "expression": "angry",
                },
                "_already_pregnant": {
                    "lines": [_("Little late for that... take a good look at me."), _("Mission accomplished, genius. I'm already pregnant."), _("You already did that, remember? Look at this belly."), _("I'm already pregnant, you idiot."), _("Look at me! It's done! I'm already carrying your baby!"), _("You already knocked me up. Congratulations.")],
                    "stats": {"Inbt": 3},
                    "expression": "normal",
                },
                # gave birth before but not currently pregnant and hasn't had the procedure
                "_had_baby_pregnancy_fear": {
                    "lines": [_("Again?! One baby was terrifying enough! I am NOT going through that again!"), _("You already got me pregnant once! Isn't that enough for you?!"), _("No no no... I barely survived the first one. Don't you dare."), _("Last time almost broke me. I'm NOT doing that again."), _("Once was more than enough. The answer is NO."), _("You want ANOTHER one?! Are you insane?!")],
                    "stats": {"Love": -3, "Obed": -1},
                    "expression": "scared",
                },
                "_had_baby_pregnancy_fetish": {
                    "lines": [_("Again...? You want to put another baby in me...?"), _("I miss being pregnant... the way you looked at me..."), _("One wasn't enough? ...maybe I wouldn't mind going through it again."), _("You want to breed me again...? I... I'd like that..."), _("Another baby... I can't stop thinking about how good it felt..."), _("Do it. Get me pregnant again. I want to feel that way again.")],
                    "stats": {"Inbt": 6, "Obed": 4, "Love": 3},
                    "expression": "happy",
                },
                "_had_baby": {
                    "lines": [_("You already did that once, remember? How did that work out?"), _("Been there, done that. You want to go through all of that again?"), _("We already have a baby, and you want another one? Seriously?"), _("Last time wasn't enough? You really want to do this again?"), _("I remember what happened last time you talked like that..."), _("You already knocked me up once. What's your game now?")],
                    "stats": {"Inbt": 3},
                    "expression": "normal",
                },
                "_had_babies_pregnancy_fear": {
                    "lines": [_("How many kids do you want?! Two wasn't enough?!"), _("I already went through this TWICE. My body can't take another one!"), _("We have kids already! PLURAL! Stop this!"), _("Every time you say that I end up pregnant. I'm done!"), _("No! We already have enough mouths to feed!")],
                    "stats": {"Love": -3, "Obed": -1},
                    "expression": "scared",
                },
                "_had_babies_pregnancy_fetish": {
                    "lines": [_("More...? You want even more kids with me...?"), _("I've already given you children and you still want more... I love that."), _("Another one... every time feels just as good..."), _("You keep filling me up and I keep wanting it. Give me another one."), _("How many do you want? Because I'll give you as many as you want...")],
                    "stats": {"Inbt": 6, "Obed": 4, "Love": 3},
                    "expression": "happy",
                },
                "_had_babies": {
                    "lines": [_("We already have kids. Plural. And you want MORE?"), _("Haven't you done enough? We already have a family."), _("Another one? Really? You just can't stop, can you?"), _("How many times are we going to do this? Seriously."), _("You keep saying that, and I keep ending up pregnant.")],
                    "stats": {"Inbt": 3},
                    "expression": "normal",
                },
                # sterile since the procedure after the birth, and she already told him (pregnancy.rpy, "THE PROCEDURE")
                "_cant_conceive": {
                    "lines": [_("You know I can't get pregnant again... so talk all you want."), _("We both know that's not happening anymore. Nice fantasy, though."), _("One was all I get, remember? That part of the story is over."), _("Threaten all you want. You know that can't happen anymore."), _("Knock me up? Did you forget what I told you? That's not possible now."), _("Go ahead and try. There's nothing left in there to knock up.")],
                    "stats": {"Inbt": 3},
                    "expression": "bemused",
                },
                # ── Full Nelson hold ──
                "_fn_pregnancy_fetish": {
                    "lines": [_("I can't fight it... just hold me tighter and breed me..."), _("Pinned down and bred... this is everything I've wanted..."), _("I can't stop you... and I don't want to... get me pregnant like this...")],
                    "stats": {"Inbt": 9, "Obed": 6, "Love": 3},
                    "expression": "happy",
                },
                "_fn_pregnancy_fear": {
                    "lines": [_("NO! I can't get away! Don't get me pregnant! PLEASE!"), _("You're holding me so I can't escape! This isn't fair! Don't breed me!"), _("I can't fight you off like this! Please don't get me pregnant!")],
                    "stats": {"Love": -6, "Obed": -2},
                    "expression": "scared",
                },
                "_fn_submissive": {
                    "lines": [_("Held like this and you say that... I can't even argue. I wouldn't. Okay."), _("If you want that... you've got me. There's nothing I'd do to stop you.")],
                    "stats": {"Obed": 5, "Inbt": 4},
                    "expression": "shy",
                },
                "_fn": {
                    "lines": [_("You'd breed me while I can't even move...?"), _("I'm pinned... I literally cannot stop you from finishing inside..."), _("That's terrifying... I can't do anything to prevent it right now..."), _("You've got me locked... I'm completely at your mercy...")],
                    "stats": {"Inbt": 5, "Obed": 3},
                    "expression": "scared",
                },
                "submissive": {
                    "lines": [_("If... if that's what you want from me. I'd do it. I'd do that for you."), _("You decide that too...? Okay. I... okay. Tell me when you're serious."), _("I'd carry it. If you told me to. I'm not saying no to you.")],
                    "stats": {"Obed": 4, "Inbt": 4},
                    "expression": "shy",
                },
                "_default": {
                    "lines": [_("You're... serious? You want to get me pregnant?"), _("A baby...? That's... I don't know what to say..."), _("You want me to carry your baby...? That's a lot."), _("I... wow. That's terrifying and exciting at the same time..."), _("You wouldn't... right? Tell me you're joking..."), _("That's... oh god, that's terrifying..."), _("Don't say things like that during sex..."), _("I can't tell if you're serious or not...")],
                    "stats": {"Inbt": 3},
                    "expression": "surprised",
                },
            },
        },

        # ── PRAISE PREGNANT BODY ────────────────────────────────
        "breed_praise": {
            "label": _("Tell her she looks beautiful pregnant"),
            "available": _tease_breed_pregnant,
            "trait_priority": ["pregnancy_fetish", "pregnancy_fear", "cum_slut", "hate_cum", "submissive"],
            "player_lines": {
                "_any": [
                    _("You look incredible like this... carrying my baby..."),

                    _("Pregnancy looks so good on you..."),

                    _("You've never been more beautiful than right now..."),

                    _("Seeing you pregnant with my child drives me crazy..."),

                ],
                "cowgirl": [
                    _("Riding me with that belly... you're a goddess..."),

                ],
                "doggy": [
                    _("From back here, you look amazing pregnant..."),

                ],
            },
            "reactions": {
                "pregnancy_fetish": {
                    "lines": [_("You like me like this...? I love hearing that..."), _("Tell me more... I love being pregnant with your baby..."), _("I feel so beautiful like this... all because of you...")],
                    "stats": {"Love": 5, "Inbt": 3},
                    "expression": "happy",
                },
                "pregnancy_fear": {
                    "lines": [_("Don't... don't say nice things about it... it makes it harder..."), _("Stop making me feel good about something I'm terrified of..."), _("I hate that hearing that makes me feel better...")],
                    "stats": {"Love": 2, "Inbt": 2},
                    "expression": "sad",
                },
                "cum_slut": {
                    "lines": [_("You think I'm hot like this? Wait until the belly gets bigger..."), _("Pregnant and sexy... I like the sound of that..."), _("If you think I look good now, just wait...")],
                    "stats": {"Inbt": 5, "Love": 3},
                    "expression": "lipbite",
                },
                "_coerced": {
                    "lines": [_("Beautiful?! I'm pregnant because of YOUR blackmail!"), _("Don't pretend this is romantic. You did this to me."), _("Spare me the compliments. We both know why I'm like this.")],
                    "stats": {"Love": -3, "Obed": 2, "Inbt": 3},
                    "expression": "angry",
                },
                "_default": {
                    "lines": [_("You... you really think so? I feel so big and weird..."), _("That's actually really sweet. Thank you."), _("Nobody's ever said something like that to me before..."), _("I don't feel beautiful at all, but hearing you say it helps.")],
                    "stats": {"Love": 3, "Inbt": 2},
                    "expression": "happy",
                },
            },
        },

        # ── TALK ABOUT PUBLIC ────────────────────────────────────
        "public_talk": {
            "label": _("Talk about doing it in public"),
            "available": _tease_always,
            "player_lines": {
                "_any": [
                    _("Imagine if someone walked in right now..."),

                    _("You'd love it if someone was watching us..."),

                    _("The door isn't even locked... anyone could walk in..."),

                    _("I want everyone to hear you scream my name..."),

                ],
                "reverse_cowgirl": [
                    _("I want to bend you over like this on campus..."),

                    _("What if I fucked you like this at the pool?"),

                    _("We should do this outside... where anyone could see..."),

                ],
                "cowgirl": [
                    _("Imagine riding me like this in the middle of the quad..."),

                    _("What if someone walked in and saw you on top of me..."),

                ],
                "bj": [
                    _("I want you to suck my dick under the classroom desk..."),

                    _("What if someone saw you on your knees like this..."),

                ],
                "hj": [
                    _("You should jerk me off under the table at dinner..."),

                ],
                "tj": [
                    _("We should do this in the locker room..."),

                ],
                "fj": [
                    _("What if I asked you to do this under the table at a restaurant?"),

                    _("Imagine giving me a footjob in class... nobody would even know..."),

                ],
                "doggy": [
                    _("I want to bend you over a desk in the library like this..."),

                    _("Imagine taking it from behind in the locker room showers..."),

                ],
                "full_nelson": [
                    _("I should carry you like this through the dorm hallway..."),

                    _("Imagine being held open like this where anyone could walk past..."),

                ],
                "laying_down": [
                    _("We should do this on the bleachers... in broad daylight..."),

                    _("Picture this on a beach towel with people walking by..."),

                ],
                # ── NTR partner watching ──
                "_ntr_watching": [
                    _("%(name)s's not the only one who should get to watch this."),

                    _("One person watching... imagine the whole campus getting this show."),

                    _("What if we did this in the quad? %(name)s can bring a chair."),

                ],
                # ── Another girl watching ──
                "_girl_watching": [
                    _("She's already watching... imagine the whole campus."),

                    _("One girl watching you isn't enough. I want a crowd."),

                    _("If she can watch, why not everyone else?"),

                ],
                "_in_public": [
                    _("Look around... people are right there and here we are..."),

                    _("Anyone could catch us any second... and we're still going..."),

                    _("We're really doing this right here... where everyone can see..."),

                    _("Someone is going to notice what we're doing..."),

                ],
                "_in_public_cowgirl": [
                    _("You're riding me right here... anyone could just look over..."),

                ],
                "_in_public_bj": [
                    _("You're on your knees right here... where anyone can see..."),

                ],
            },
            "reactions": {
                "exhibitionist": {
                    "lines": [_("Let them watch... I don't care..."), _("That sounds so hot... let's do it..."), _("I WANT people to see us..."), _("Leave the door open... I dare you..."), _("The more people watching, the harder I cum...")],
                    "stats": {"Inbt": 8, "Obed": 3},
                    "expression": "happy",
                },
                "public_fetish": {
                    "lines": [_("The risk is what makes it exciting..."), _("Mmm... maybe we should..."), _("You're making me wet just thinking about it..."), _("Somewhere hidden... but where we could still get caught...")],
                    "stats": {"Inbt": 5, "Obed": 2},
                    "expression": "lipbite",
                },
                "public_shy": {
                    "lines": [_("Are you CRAZY?! Someone could see us!"), _("No way! That's way too risky!"), _("I would die if anyone saw me like this!"), _("Lock the door RIGHT NOW!")],
                    "stats": {"Love": -2, "Obed": 2},
                    "expression": "angry",
                },
                "_in_public": {
                    "lines": [_("We're already doing it... oh god..."), _("Someone is going to see us... I can't believe this..."), _("This is so risky... why does it feel so good..."), _("If anyone walks by right now...")],
                    "stats": {"Inbt": 5, "Obed": 3},
                    "expression": "surprised",
                },
                "_in_public_shy": {
                    "lines": [_("We ARE in public! Why did I agree to this?!"), _("Oh god, oh god, someone is going to see us!"), _("I can hear people walking... please hurry up!"), _("This was a terrible idea! Finish already!")],
                    "stats": {"Love": -3, "Obed": 5},
                    "expression": "scared",
                },
                "_in_public_exb": {
                    "lines": [_("I know... and I love every second of it..."), _("Let them see... let them all see what you do to me..."), _("This is exactly where I want to be fucked..."), _("I hope someone is watching right now...")],
                    "stats": {"Inbt": 10, "Obed": 5},
                    "expression": "happy",
                },
                # ── Full Nelson hold ──
                "_fn_public_shy": {
                    "lines": [_("I can't even cover myself! Anyone could see me like this!"), _("I'm pinned open and we're in PUBLIC?! This is a nightmare!"), _("I can't run, I can't hide... someone is going to see everything!")],
                    "stats": {"Love": -4, "Obed": 4, "Inbt": 5},
                    "expression": "scared",
                },
                "_fn_exhibitionist": {
                    "lines": [_("Pinned and on display for everyone... this is a dream..."), _("I can't cover up even if I wanted to... and I don't want to..."), _("Held up like a trophy... let them all look...")],
                    "stats": {"Inbt": 10, "Obed": 5},
                    "expression": "happy",
                },
                "_fn_submissive": {
                    "lines": [_("If someone walks in... I can't do anything about it. You decide. You always do."), _("Held like this, anyone could... okay. Okay. It's your call.")],
                    "stats": {"Obed": 4, "Inbt": 4},
                    "expression": "shy",
                },
                "_fn": {
                    "lines": [_("I can't even run if someone walks in... you realize that, right?"), _("Pinned like this in a place like this... I'm totally exposed..."), _("If anyone sees me held up like this... I would die...")],
                    "stats": {"Inbt": 5, "Obed": 3},
                    "expression": "scared",
                },
                "_default": {
                    "lines": [_("That's... a little risky, don't you think?"), _("Hmm... maybe somewhere private outdoors..."), _("You're crazy... but I'm not saying no..."), _("The adrenaline would be insane...")],
                    "stats": {"Inbt": 3},
                    "expression": "shy",
                },
                "nerd": {
                    "lines": [_("In PUBLIC?! Where my PROFESSORS could see?! Absolutely not!"), _("The probability of getting caught is non-trivial and the consequences are EXPULSION!"), _("My department chair walks through campus every day. Are you INSANE?!"), _("One witness and my entire academic career is ashes. Hard no.")],
                    "stats": {"Love": -3, "Obed": -2, "Inbt": 3},
                    "expression": "scared",
                },
                "_in_public_nerd": {
                    "lines": [_("We ARE in a public place! If Professor Daniels walks in, I'm DEAD!"), _("I can hear footsteps outside! My scholarship, my reputation, EVERYTHING is on the line!"), _("S-stop for a second! I heard something! If my classmates find me like this, I'll have to DROP OUT!"), _("If campus security checks this room, I will never recover academically. NEVER.")],
                    "stats": {"Love": -2, "Obed": 4, "Inbt": 6},
                    "expression": "scared",
                },
                "_in_classroom_nerd": {
                    "lines": [_("This is MY classroom! I sit in that chair EVERY DAY! The professor could come back ANY SECOND!"), _("I can hear students in the hallway! If they open that door, my entire future is GONE! I studied HERE for YEARS!"), _("My notes are still on that desk! My NAME is on the attendance sheet! If anyone connects me to THIS...!"), _("The professor left ten minutes ago! He always comes back for his coffee! We need to stop RIGHT NOW!")],
                    "stats": {"Love": -3, "Obed": 5, "Inbt": 8},
                    "expression": "scared",
                },
                "_in_classroom_tenny": {
                    "lines": [_("There are people two rows away... if anyone just turns around... why does that make my pulse race like this?"), _("I sit in this chair every day next to these people... they have no idea what's happening right now... and that terrifies me and thrills me at the same time..."), _("Someone could literally just glance over... we're not even hidden... my heart is about to explode..."), _("Everyone is right here... one wrong sound and they all see us... so why can't I make myself stop?")],
                    "stats": {"Obed": 6, "Inbt": 4},
                    "expression": "shy",
                },
                "_in_public_tenny": {
                    "lines": [_("There are people right there... if any of them just looks this way... why is my heart racing like THIS?"), _("If anyone notices us, my reputation is done... and the fact that I keep going says something about me..."), _("People are so close... any one of them could see us right now... it doesn't make me want to stop."), _("Anyone around us could catch on at any second... I hate how much that excites me...")],
                    "stats": {"Obed": 5, "Inbt": 3},
                    "expression": "shy",
                },
                "_in_public_fetish": {
                    "lines": [_("We ARE in public... and I'm soaking because of it..."), _("Every footstep outside makes me clench harder... don't stop..."), _("This is exactly the kind of risk I live for..."), _("If someone walks in, don't you dare pull out...")],
                    "stats": {"Inbt": 7, "Obed": 3},
                    "expression": "lipbite",
                },
                "gym_rat": {
                    "lines": [_("In the locker room? ...Okay, I've thought about that one."), _("Everyone at the gym already stares. Might as well give them something real."), _("As long as it doesn't mess with my training schedule..."), _("Risky. I like risky. Spot me.")],
                    "stats": {"Inbt": 4, "Obed": 2},
                    "expression": "lipbite",
                },
                # ── NTR partner watching ──
                "_ntr_watching": {
                    "lines": [_("%(name)s watching is already more than I ever imagined..."), _("One person is enough... please... %(pp)s's right there..."), _("Don't get greedy... %(name)s is all the audience I can handle...")],
                    "stats": {"Inbt": 3, "Obed": 2},
                    "expression": "shy",
                    "npc_boundary_bar": 2,
                },
                "_ntr_watching_exhibitionist": {
                    "lines": [_("Yes... %(name)s first... then everyone..."), _("If %(pp)s gets to watch, why not the whole campus?"), _("Mmm... more eyes on me... %(name)s can bring friends...")],
                    "stats": {"Inbt": 8, "Obed": 3},
                    "expression": "happy",
                    "npc_boundary_bar": 4,
                },
                "_ntr_watching_public_shy": {
                    "lines": [_("%(name)s watching is already too much! Don't even joke about that!"), _("NO. One person. %(Pp)s's the limit. Never more."), _("Are you insane?! Isn't %(po)s seeing this humiliating enough?!")],
                    "stats": {"Love": -2, "Obed": 3},
                    "expression": "angry",
                },
                # ── Another girl watching ──
                "_girl_watching": {
                    "lines": [_("She's already watching... isn't that enough..."), _("One person seeing me like this is already too much..."), _("Don't... her watching is as far as I go...")],
                    "stats": {"Inbt": 3, "Obed": 2},
                    "expression": "shy",
                },
                "_girl_watching_exhibitionist": {
                    "lines": [_("Her watching just makes me want more..."), _("Yes... let her watch... let everyone watch..."), _("She can see everything... and I want more eyes on me...")],
                    "stats": {"Inbt": 8, "Obed": 3},
                    "expression": "happy",
                },
                "_girl_watching_public_shy": {
                    "lines": [_("Her being here is already killing me! Stop!"), _("No! She's already seeing too much!"), _("Please... one person is bad enough...")],
                    "stats": {"Love": -2, "Obed": 3},
                    "expression": "angry",
                },
            },
        },

        # ── ATM TEASE (only during BJ after anal) ───────────────
        "atm_taste": {
            "label": _("Ask how her ass tastes"),
            "available": _tease_atm_active,
            "player_lines": {
                "_any": [
                    _("How does your ass taste?"),

                    _("You like the taste of your own ass?"),

                ],
            },
            "reactions": {
                "cum_slut": {
                    "lines": [_("Mmm... tastes like I've been a very bad girl..."), _("Delicious. You should try it sometime."), _("I can taste exactly where it's been... and I want more.")],
                    "stats": {"Inbt": 8, "Obed": 3},
                    "expression": "lipbite",
                },
                "anal_lover": {
                    "lines": [_("Honestly? Not bad. Kind of kinky..."), _("It's... dirty. I don't hate it."), _("You're enjoying this, aren't you? ...So am I.")],
                    "stats": {"Inbt": 5, "Obed": 2},
                    "expression": "lipbite",
                },
                "hardcore_sex": {
                    "lines": [_("Disgusting. Don't stop."), _("Filthy. Now fuck my mouth like you mean it."), _("Like the dirtiest thing I've ever done. Faster.")],
                    "stats": {"Inbt": 6, "Obed": 5},
                    "expression": "lipbite",
                },
                "submissive": {
                    "lines": [_("Like I'm exactly where I belong."), _("Tastes like submission. Ask me again."), _("Like whatever you tell me it tastes like.")],
                    "stats": {"Inbt": 6, "Obed": 5},
                    "expression": "lipbite",
                },
                "hate_cum": {
                    "lines": [_("It's AWFUL! Are you happy now?!"), _("Like ass and regret! Why are you making me do this?!"), _("I want to spit it out so bad... this is the worst...")],
                    "stats": {"Love": -5, "Obed": 3},
                    "expression": "angry",
                },
                "anal_hater": {
                    "lines": [_("Disgusting! You KNOW I hate this!"), _("Like something I never wanted in my mouth! Are you satisfied?!"), _("Horrible. You're horrible for asking.")],
                    "stats": {"Love": -3, "Obed": 2},
                    "expression": "angry",
                },
                "cute_sex": {
                    "lines": [_("Why would you ask me that...? It tastes awful and you know it..."), _("Please don't make me think about it... I'm trying not to gag..."), _("You're so mean... why would you rub it in like that...?")],
                    "stats": {"Love": -3, "Obed": 2},
                    "expression": "sad",
                },
                "_default": {
                    "lines": [_("Like ass. What did you expect?"), _("It's not great, if that's what you're asking."), _("Tastes like I'm never living this down.")],
                    "stats": {"Inbt": 3, "Obed": 2},
                    "expression": "shy",
                },
            },
        },
        # ── LESBIAN HUMILIATE ─────────────────────────────────
        "lesbian_humiliate": {
            "label": _("Humiliate her sexuality"),
            "available": _tease_is_lesbian,
            "player_lines": {
                "_any": [
                    _("Some lesbian you are..."),

                    _("Turns out you just needed a good dicking."),

                    _("Are all lesbians as slutty as you are?"),

                    _("After me, every woman is going to feel like a downgrade."),

                    _("Your girlfriend uses a strap-on, right? How does the real thing compare?"),

                    _("How does it feel knowing a man makes you cum harder than any woman ever could?"),

                ],
                "bj": [
                    _("A lesbian on her knees sucking cock... classic."),

                    _("For someone who hates men, you sure know how to use that mouth."),

                ],
                # ── Her girlfriend is here (gave permission / watching) ──
                "_gf_watching": [
                    _("Your girlfriend is watching a man fuck you. Some lesbian."),

                    _("She said yes... what does that make the two of you?"),

                    _("Look at her watching. I think she likes seeing you like this."),

                ],
            },
            "reactions": {
                # ── Her girlfriend is here ──
                "_gf_watching": {
                    "lines": [_("She's watching... she said yes to this... don't make her regret it."), _("Don't look at her when you say that. She's here for me."), _("My girlfriend is RIGHT there. Have some shame.")],
                    "stats": {"Obed": 3, "Inbt": 5},
                    "expression": "angry",
                },
                "_lesbian_broken": {
                    "lines": [_("...Maybe you're right."), _("I don't even know what I am anymore..."), _("Just... keep going. I don't want to think about it.")],
                    "stats": {"Obed": 8, "Inbt": 10},
                    "expression": "sad",
                },
                "_lesbian_coerced_hc": {
                    "lines": [_("Shut up. You're only here because of that video."), _("Say whatever you want. I'm still a lesbian. You're just a blackmailer."), _("The second you run out of videos, this is over. Remember that.")],
                    "stats": {"Obed": 3, "Inbt": 8},
                    "expression": "angry",
                },
                "_lesbian_coerced_cute": {
                    "lines": [_("Stop... please stop saying those things... you're already making me do this..."), _("That's so cruel... I'm only here because of the video... you know that..."), _("Please... I already hate this enough... don't make it worse...")],
                    "stats": {"Love": -8, "Obed": 3},
                    "expression": "sad",
                },
                "_lesbian_coerced": {
                    "lines": [_("You can mock me all you want. I'm only here because of that video, and we both know it."), _("I'm a lesbian being forced by a blackmailer. There's nothing to humiliate here."), _("Save your breath. The video put me here, not your charm.")],
                    "stats": {"Obed": 3, "Inbt": 5},
                    "expression": "angry",
                },
                "_lesbian_paid_hc": {
                    "lines": [_("Yeah, you paid. So what? My body doesn't care where the money came from."), _("You bought time, not me. I'll take your cash and forget your name."), _("Keep paying. It's the only way you'll ever touch a lesbian.")],
                    "stats": {"Obed": 3, "Inbt": 8},
                    "expression": "angry",
                },
                "_lesbian_paid_cute": {
                    "lines": [_("I know what you think of me... but I needed the money... please don't rub it in..."), _("You're paying me to do something I hate... isn't that enough for you..."), _("I feel so dirty... and not because of the sex... because I said yes for money...")],
                    "stats": {"Love": -8, "Obed": 3},
                    "expression": "sad",
                },
                "_lesbian_paid": {
                    "lines": [_("I took your money, not your insults. We had a deal, not a relationship."), _("I'm a lesbian who needed cash. That's it. Don't read more into it."), _("The money runs out, and so does this. Don't flatter yourself.")],
                    "stats": {"Obed": 3, "Inbt": 5},
                    "expression": "angry",
                },
                "hardcore_sex": {
                    "lines": [_("Shut up and fuck me harder..."), _("You think I care what you call me? Just don't stop.")],
                    "stats": {"Obed": 5, "Inbt": 8},
                    "expression": "lipbite",
                },
                "femdom": {
                    "lines": [_("Talk all you want. I'm using you, not the other way around."), _("Keep mocking me. I'm still the one who decides when you get to cum."), _("Some lesbian? This lesbian is running the show. Remember that.")],
                    "stats": {"Inbt": 8},
                    "expression": "lipbite",
                },
                "cute_sex": {
                    "lines": [_("Stop... don't say that..."), _("That's so cruel... I didn't choose this..."), _("Please don't make fun of me... I already hate this enough...")],
                    "stats": {"Love": -5, "Obed": 5},
                    "expression": "sad",
                },
                "_default": {
                    "lines": [_("This doesn't change anything about who I am."), _("You can say whatever you want. I'm still a lesbian."), _("Enjoy it while it lasts. This doesn't mean you've won.")],
                    "stats": {"Obed": 3, "Inbt": 5},
                    "expression": "normal",
                },
            },
        },

        # ── LESBIAN PRAISE ───────────────────────────────────
        "lesbian_praise": {
            "label": _("Praise her"),
            "available": _tease_is_lesbian,
            "player_lines": {
                "_any": [
                    _("You're my favorite kind of lesbian."),

                    _("Lesbian pussy hits different."),

                    _("You're the exception to every rule."),

                    _("I know this isn't easy for you. You're incredible."),

                    _("No one else gets this from you. That makes it special."),

                    _("You're braver than you think for letting this happen."),

                ],
            },
            "reactions": {
                "hardcore_sex": {
                    "lines": [_("Don't get sentimental on me. Just keep going."), _("I'm not special. I'm just horny. There's a difference."), _("Whatever helps you sleep at night.")],
                    "stats": {"Inbt": 5, "Love": 3},
                    "expression": "normal",
                },
                "cute_sex": {
                    "lines": [_("You... you really think that?"), _("That's... actually really sweet. Don't make me cry during this."), _("Nobody's ever said anything like that to me before...")],
                    "stats": {"Love": 8, "Inbt": 3},
                    "expression": "shy",
                },
                "_default": {
                    "lines": [_("I don't know how to respond to that."), _("You're making this complicated."), _("Just because I'm here doesn't mean you get to be sweet about it.")],
                    "stats": {"Love": 5, "Inbt": 3},
                    "expression": "shy",
                },
                # ── Her girlfriend is here ──
                "_gf_watching": {
                    "lines": [_("Don't be sweet in front of her... it makes this more confusing..."), _("She can hear you... stop..."), _("...Thanks. Now stop talking before she gets jealous.")],
                    "stats": {"Love": 4, "Inbt": 3},
                    "expression": "shy",
                },
            },
        },

        # ── HUMILIATE HER GIRLFRIEND ─────────────────────────
        "gf_humiliate": {
            "label": _("Talk about her girlfriend"),
            "available": _tease_has_girlfriend,
            "player_lines": {
                "_any": [
                    _("Does your girlfriend know you're here right now?"),

                    _("I wonder what she'd think if she saw you like this."),

                    _("You moan louder for me than you ever did for her."),

                    _("She thinks she satisfies you... but here you are."),

                    _("Imagine her face if she walked in right now."),

                    _("I bet she has no idea her girlfriend is getting dicked down right now."),

                ],
                "bj": [
                    _("Does she know you suck cock this well?"),

                    _("I bet she'd love to see her girlfriend on her knees for a man."),

                ],
                "cowgirl": [
                    _("Does she know you ride like this?"),

                    _("Riding a cock this eagerly... your girlfriend would be heartbroken."),

                ],
                "doggy": [
                    _("Bent over for a man... what would your girlfriend say?"),

                    _("She's never had you like this, has she? From behind, begging?"),

                ],
                # ── Her girlfriend is here (gave permission / watching) ──
                "_gf_watching": [
                    _("Your girlfriend is right there, watching you take a real cock."),

                    _("Look at her face. She said yes to this... and now she gets to watch."),

                    _("She gave you to me. Lucky her, she gets a front row seat."),

                    _("Wave to your girlfriend. She's watching every second."),

                ],
                # ── She knows and allowed it (NTR active, not in the room) ──
                "_ntr_known": [
                    _("She agreed to this... what kind of girlfriend lets this happen?"),

                    _("She knows exactly where you are. And she let you go."),

                    _("Your girlfriend said yes to you getting fucked by a man. Think about that."),

                    _("She gave you permission... like you needed it."),

                ],
            },
            # Partner attitude defines her reaction before her sex style does
            "trait_priority": ["cheater", "loyal", "femdom", "submissive", "cute_sex", "hardcore_sex"],
            "reactions": {
                # ── Her girlfriend is here ──
                "_gf_watching": {
                    "lines": [_("She's right here... don't talk about her like that..."), _("She said yes because she trusts me... don't make it ugly..."), _("Don't look at her... look at me... this is hard enough...")],
                    "stats": {"Obed": 3, "Inbt": 4},
                    "expression": "shy",
                },
                "_gf_watching_cute_sex": {
                    "lines": [_("Please... she's watching... I can't... don't say that to her..."), _("She agreed for me... don't humiliate her for it..."), _("I can't look at her face right now... stop...")],
                    "stats": {"Love": -4, "Obed": 3},
                    "expression": "sad",
                },
                "_gf_watching_hardcore_sex": {
                    "lines": [_("She knows what she signed up for. Now fuck me properly."), _("Let her watch. She'll get her turn with me later."), _("Don't talk to her. Talk to me. With your hips.")],
                    "stats": {"Inbt": 6, "Obed": 3},
                    "expression": "lipbite",
                },
                "_gf_watching_cheater": {
                    "lines": [_("She's watching? Good. Maybe she'll learn something."), _("She said yes. Whatever happens next is on her."), _("Let her see what she can't give me.")],
                    "stats": {"Inbt": 7, "Obed": 3},
                    "expression": "lipbite",
                },
                # ── She knows and allowed it ──
                "_ntr_known": {
                    "lines": [_("She agreed to this... that doesn't give you the right to judge her."), _("She knows. She's okay with it. Leave it there."), _("She let me come here. Don't turn that into something ugly.")],
                    "stats": {"Obed": 3, "Inbt": 3},
                    "expression": "shy",
                },
                "_ntr_known_cheater": {
                    "lines": [_("She knows... and she still can't stop it. That's kind of hot."), _("She said yes because she knew I'd do it anyway."), _("Poor thing thinks permission makes her part of this.")],
                    "stats": {"Inbt": 7, "Obed": 3},
                    "expression": "lipbite",
                },
                "_ntr_known_cute_sex": {
                    "lines": [_("Don't make fun of her... she's trying so hard to understand..."), _("She said yes because she loves me... don't twist it..."), _("Please... she's being so patient with me... don't...")],
                    "stats": {"Love": -2, "Obed": 3},
                    "expression": "sad",
                },
                "_ntr_known_hardcore_sex": {
                    "lines": [_("She knows what I'm doing. Now shut up and prove it was worth it."), _("She gave me a free pass. Stop wasting it talking."), _("Yeah, she said yes. So make it count.")],
                    "stats": {"Inbt": 5, "Obed": 3},
                    "expression": "lipbite",
                },
                "_lesbian_broken": {
                    "lines": [_("She deserves better than me... I know that now."), _("Maybe she'd be happier without me... at least then I'd stop lying to her."), _("I don't even feel guilty anymore... and that scares me more than anything.")],
                    "stats": {"Obed": 8, "Inbt": 10},
                    "expression": "sad",
                },
                "_lesbian_coerced_cute": {
                    "lines": [_("Don't... don't bring her into this... she has nothing to do with what you're making me do..."), _("She trusts me... and you're using that against me... please stop..."), _("I'm only here because of your video... leave her out of it... please...")],
                    "stats": {"Love": -8, "Obed": 3},
                    "expression": "sad",
                },
                "_lesbian_coerced": {
                    "lines": [_("Don't you DARE talk about her. She has nothing to do with this. YOU are the one forcing me."), _("My girlfriend is the reason I'm still sane. Leave her out of your sick game."), _("You're blackmailing me into this and now you want to drag her into it too? You're disgusting.")],
                    "stats": {"Love": -5, "Obed": 3, "Inbt": 5},
                    "expression": "angry",
                },
                "_lesbian_paid_cute": {
                    "lines": [_("Please don't talk about her... she doesn't know I'm doing this for money... she'd never forgive me..."), _("I hate myself for this... she thinks I'm at work... and I'm here selling myself to a man..."), _("If she ever finds out I took money to sleep with a guy... it would destroy her...")],
                    "stats": {"Love": -8, "Obed": 3},
                    "expression": "sad",
                },
                "_lesbian_paid": {
                    "lines": [_("Leave her out of this. I took your money, that's between us. She's not part of the deal."), _("My girlfriend has nothing to do with this transaction. Keep her name out of your mouth."), _("You paid for sex, not for the right to talk about my relationship. Shut up.")],
                    "stats": {"Love": -5, "Obed": 3, "Inbt": 5},
                    "expression": "angry",
                },
                "cheater": {
                    "lines": [_("She has no idea... and honestly? I don't care anymore."), _("She could never do what you're doing right now."), _("Don't mention her. She's not part of this.")],
                    "stats": {"Inbt": 8, "Obed": 3},
                    "expression": "lipbite",
                },
                "cute_sex": {
                    "lines": [_("Don't... please don't talk about her..."), _("She trusts me... I'm a terrible person..."), _("Stop... you're making me feel so guilty...")],
                    "stats": {"Love": -5, "Obed": 3},
                    "expression": "sad",
                },
                "_default": {
                    "lines": [_("That's a low blow... but you're not wrong."), _("She'd kill us both if she found out."), _("Just shut up and keep going. I'll deal with the guilt later.")],
                    "stats": {"Obed": 3, "Inbt": 5},
                    "expression": "normal",
                },
            },
        },

        # ── FINANCIAL MOCK ───────────────────────────────────
        "financial_mock": {
            "label": _("Mock her for selling herself"),
            "available": _tease_has_financial,
            "player_lines": {
                "_any": [
                    _("How much was it again? I forgot... it was that cheap."),

                    _("You know what the difference between you and a hooker is? ...Nothing."),

                    _("I love that I can just pay and you spread your legs."),

                    _("What's your hourly rate? I might want to book you again."),

                    _("Best money I ever spent. You should put up a price list."),

                    _("Do you give discounts for regulars, or is it full price every time?"),

                    _("I bet you never thought you'd be selling this, huh?"),

                    _("Once you put a price on it, there's no going back."),

                    _("Every time gets cheaper. Supply and demand, right?"),

                    _("Funny how quick 'never again' becomes 'how much this time.'"),

                ],
                "_recording": [
                    _("Smile for the camera. This is paid content now."),

                    _("Your price went up since we started filming. Good for you."),

                    _("Getting paid AND filmed. You've really committed to this career."),

                    _("I wonder how much this video is worth... more than you charged, for sure."),

                ],
                "cowgirl": [
                    _("Riding me for money... you're a natural at this job."),

                    _("Bounce harder. I paid for the premium service."),

                    _("You ride like a pro. Maybe that IS your profession now."),

                ],
                "reverse_cowgirl": [
                    _("I'm getting quite the show for my money."),

                    _("Arch that back. I want my money's worth."),

                    _("That ass was expensive, but worth every penny."),

                ],
                "doggy": [
                    _("Taking it from behind for cash. Classy."),

                    _("Push back harder. This isn't a charity fuck."),

                    _("On all fours for money... let that sink in."),

                ],
                "full_nelson": [
                    _("Can't even move and you still took the money. Desperate much?"),

                    _("Helpless AND paid for. What does that make you?"),

                ],
                "laying_down": [
                    _("Lying there for money... at least you're comfortable."),

                    _("Spread your legs wider. I paid for the full view."),

                ],
                # ── Another girl watching ──
                "_girl_watching": [
                    _("She's watching you get paid for this. How does that feel?"),

                    _("Did you tell her how much you charged?"),

                    _("Careful. She might want a cut."),

                ],
                "bj": [
                    _("On your knees for cash... this is exactly what you are now."),

                    _("Suck it better. I paid good money for this."),

                    _("A mouth for hire. Has a nice ring to it."),

                ],
                "hj": [
                    _("A handjob for money... that's how this started, right?"),

                    _("Your hands are worth what, five bucks? Ten?"),

                ],
                "tj": [
                    _("Wrap those tits around it. You're on the clock."),

                    _("Tits for cash. There's a word for this profession."),

                ],
            },
            "reactions": {
                "_financial_stage_0": {
                    "lines": [_("Shut up! I'm not... this doesn't make me... just stop talking!"), _("You think I don't hate myself enough already?! Don't rub it in!"), _("I said STOP. I only did it because I had no choice!")],
                    "stats": {"Love": -5, "Obed": 3},
                    "expression": "angry",
                },
                "_financial_stage_1": {
                    "lines": [_("...I know what I am. You don't need to remind me."), _("Yeah. I took the money. Can we not talk about it?"), _("I'm past caring what you call me. Just finish.")],
                    "stats": {"Love": -3, "Obed": 5},
                    "expression": "sad",
                },
                "_financial_stage_2": {
                    "lines": [_("Money is money. You got what you paid for, didn't you?"), _("Call it whatever you want. My bank account doesn't judge."), _("If the price bothers you, next time don't offer it.")],
                    "stats": {"Inbt": 5, "Obed": 3},
                    "expression": "normal",
                },
                "_financial_stage_3": {
                    "lines": [_("Mmm, keep talking like that... it actually turns me on."), _("You're right. I love getting paid for this. So pay me more."), _("Call me whatever you want. I'll moan louder if you tip.")],
                    "stats": {"Inbt": 8, "Obed": 5},
                    "expression": "lipbite",
                },
                "hardcore_sex": {
                    "lines": [_("So what? You pay, I fuck. Everybody wins. Now shut up and go harder."), _("At least I'm expensive. That says something, doesn't it?")],
                    "stats": {"Inbt": 5, "Obed": 3},
                    "expression": "lipbite",
                },
                "femdom": {
                    "lines": [_("You wanna mock me? Fine. But you're still the one paying."), _("I set the price, I set the rules. Keep talking and it goes up."), _("You pay, I decide how this goes. Now be a good boy and keep quiet.")],
                    "stats": {"Inbt": 5},
                    "expression": "lipbite",
                },
                "cute_sex": {
                    "lines": [_("Why... why would you say that...? I already feel awful about it..."), _("Please stop... you're making me feel so dirty..."), _("I'm not... I'm not that kind of girl... I just needed the money...")],
                    "stats": {"Love": -5, "Obed": 3},
                    "expression": "sad",
                },
                "cheater": {
                    "lines": [_("And? Free money for something I'd probably do anyway."), _("You're the one paying for sex. Who's the desperate one here?"), _("Whatever. At least I'm getting something out of this.")],
                    "stats": {"Inbt": 5},
                    "expression": "normal",
                },
                "loyal": {
                    "lines": [_("Don't... please don't say it out loud... I can barely live with myself..."), _("I know what you think of me now. I think it too. Every single day."), _("If anyone ever found out I took money for this... please just stop...")],
                    "stats": {"Love": -5, "Obed": 5},
                    "expression": "sad",
                },
                "_default": {
                    "lines": [_("...You don't have to be such an ass about it."), _("I get it. I sold myself. Can we move on?"), _("You're the one who offered the money, remember?")],
                    "stats": {"Inbt": 3, "Obed": 3},
                    "expression": "shy",
                },
            },
            # Stage 0-1: her traits color the shame; stage 2-3: the attitude pool always wins
            "trait_priority": ["cheater", "loyal", "femdom", "submissive", "hardcore_sex", "cute_sex"],
        },

        # ── NTR: TAUNT THE PARTNER ───────────────────────────
        "ntr_cuckold_mock": {
            "label": _("Taunt the partner"),
            "available": _tease_ntr_watching,
            "player_lines": {
                "_any": [
                    _("Look at %(po)s, just standing there watching. Pathetic."),

                    _("You're still here, %(name)s. That says everything."),

                    _("%(name)s could leave any time... but %(pp)s won't."),

                    _("How long are you gonna just stand there, %(name)s?"),

                    _("What's wrong, %(name)s? Can't move? Can't look away?"),

                    _("%(name)s, be honest. This is the best view you've had in months."),

                    _("She moans louder for me than she ever did for you, %(name)s."),

                    _("This is what she sounds like when she's actually satisfied, %(name)s."),

                ],
                "_any_male": [
                    _("Does your little dick twitch every time she moans for me, %(name)s?"),

                    _("She chose the bigger cock. And you just... watch."),

                    _("Is this what you do now, %(name)s? Watch a real dick do your job?"),

                    _("Your dick is probably harder right now than it's ever been inside her."),

                    _("A real man would stop this. But you're not a real man, are you?"),

                ],
                "_any_female": [
                    _("Only a real cock can make her moan like this, %(name)s. You never could."),

                    _("Your fingers never got her this wet, %(name)s. Not even close."),

                    _("She needed something you could never give her, %(name)s. Now she has it."),

                    _("All those nights with you... and she screams louder after one minute with me."),

                    _("Watch closely, %(name)s. Learn what she actually needs."),

                ],
                "_hostile": [
                    _("See, %(name)s? THIS is how you fuck her properly."),

                    _("Look how she moans and squirms for me, %(name)s. You never even came close."),

                    _("What's the matter, %(name)s? Upset? She's not. Look at that face."),

                    _("You hate me, right %(name)s? But she doesn't. Not right now."),

                    _("Every sound she makes is proof you were never enough, %(name)s."),

                    _("You wanna hit me? Go ahead. She'll still be moaning when you're done."),

                    _("The woman you love is screaming my name, %(name)s. And you can't do shit about it."),

                ],
                "_hostile_male": [
                    _("See, %(name)s? Only a real cock makes her moan like this. Yours never could."),

                    _("She needed a bigger dick all along, %(name)s. Yours was just a placeholder."),

                    _("Look at her face. She never made that face for your little dick, %(name)s."),

                    _("She's taking every inch and loving it. How many inches can YOU give her, %(name)s?"),

                ],
                "_hostile_female": [
                    _("See, %(name)s? Only a real cock can make her moan like this. You'll never do that."),

                    _("Your tongue, your fingers... none of that compares to THIS, %(name)s."),

                    _("She needed something real inside her. Something you can never provide."),

                    _("No matter what you do, %(name)s, you can't make her feel THIS full."),

                ],
                "cowgirl": [
                    _("She's riding me and you're just watching, %(name)s. Classic."),

                    _("Look at her face. She never makes that face for you, does she?"),

                    _("She won't even look at you while she bounces on me."),

                ],
                "reverse_cowgirl": [
                    _("That view of her ass? That's MY view now, %(name)s. You just get to spectate."),

                    _("Best seat in the house, right %(name)s?"),

                ],
                "doggy": [
                    _("I'm balls deep in your girl and you're just standing there, %(name)s."),

                    _("She screams louder for me. You can hear the difference, right?"),

                    _("Every thrust I give her is one you couldn't, %(name)s."),

                ],
                "full_nelson": [
                    _("I've got your girl pinned and she's LOVING it. What does that tell you, %(name)s?"),

                    _("She can't even move and she's still moaning louder than she ever did with you."),

                ],
                "laying_down": [
                    _("She's wrapped around me and you're just standing there, %(name)s."),

                    _("Look at her legs around my waist. She never did that for you, did she?"),

                ],
                "anal": [
                    _("I'm in her ass, %(name)s. Did you ever even get close?"),

                    _("She gave me her ass... what did she give you?"),

                ],
                # ── Bet event: his back is turned, he only hears ──
                "_ntr_listening": [
                    _("You can hear every sound she makes, %(name)s. Still not turning around?"),

                    _("Back turned like it makes a difference. You're listening to every second of this, %(name)s."),

                    _("Go on, %(name)s, keep staring at that wall. She's getting louder either way."),

                    _("How long can you keep your back turned, %(name)s? She's not even trying to be quiet."),

                    _("Those are her real moans, %(name)s. Bet you've never heard them before."),

                ],
                "_ntr_listening_male": [
                    _("Your back's turned but I bet your dick isn't, %(name)s."),

                ],
                "_ntr_listening_female": [
                    _("You can hear what a real cock does to her, %(name)s. Turn around and see it."),

                ],
                "bj": [
                    _("She sucks my cock like her life depends on it. Did she ever do that for you, %(name)s?"),

                    _("Look at those eyes looking up at ME. Not you, %(name)s. Me."),

                ],
                "hj": [
                    _("She's stroking me off while you watch. Take notes, %(name)s."),

                ],
                "tj": [
                    _("Those tits are mine right now. You can watch, %(name)s."),

                ],
            },
            "reactions": {
                # ── Bet event: his back is turned, he only hears ──
                "_ntr_listening": {
                    "lines": [_("%(pp)s can hear every word... and %(pp)s still won't turn around..."), _("Don't... %(pp)s's trying so hard not to look..."), _("Keep talking to %(po)s... I want to see how long %(pp)s lasts...")],
                    "stats": {"Obed": 5, "Inbt": 5},
                    "expression": "lipbite",
                    "npc_stats": {"friendship_with_player": -30},
                    "npc_boundary_bar": -3,
                },
                "_ntr_listening_hardcore_sex": {
                    "lines": [_("Louder. I want %(po)s to crack."), _("%(pp)s's listening to all of it... fuck, that's hot..."), _("Make %(po)s turn around. Make %(po)s watch.")],
                    "stats": {"Obed": 6, "Inbt": 7},
                    "expression": "lipbite",
                    "npc_stats": {"friendship_with_player": -35},
                    "npc_boundary_bar": -5,
                },
                "_ntr_listening_cute_sex": {
                    "lines": [_("Don't be cruel... %(pp)s's right there... listening..."), _("%(name)s... you don't have to turn around... please don't listen to him..."), _("Stop... %(pp)s can hear everything you say...")],
                    "stats": {"Love": -3, "Obed": 4, "Inbt": 3},
                    "expression": "scared",
                    "npc_stats": {"friendship_with_player": -40},
                    "npc_boundary_bar": -5,
                },
                "_ntr_listening_cheater": {
                    "lines": [_("Look at %(po)s, pretending not to listen... pathetic..."), _("%(pp)s's going to break. I know %(po)s."), _("Keep going... %(pp)s's dying to turn around...")],
                    "stats": {"Inbt": 7, "Obed": 4},
                    "expression": "lipbite",
                    "npc_stats": {"friendship_with_player": -30},
                    "npc_boundary_bar": -4,
                },
                "hardcore_sex": {
                    "lines": [_("God... that's so wrong... but %(pp)s IS still watching... keep talking like that..."), _("%(name)s can hear everything... fuck, that makes it hotter..."), _("Don't stop... tell %(po)s more... I love how fucked up this is...")],
                    "stats": {"Obed": 6, "Inbt": 7},
                    "expression": "lipbite",
                    "npc_stats": {"friendship_with_player": -40},
                    "npc_boundary_bar": -8,
                },
                "cute_sex": {
                    "lines": [_("Don't say that to %(po)s... please... this is already so wrong..."), _("Stop... I can't look at %(po)s while you say those things..."), _("Please... %(pp)s is right there... don't be so cruel...")],
                    "stats": {"Love": -3, "Obed": 4, "Inbt": 4},
                    "expression": "scared",
                    "npc_stats": {"friendship_with_player": -50},
                    "npc_boundary_bar": -6,
                },
                "cheater": {
                    "lines": [_("%(name)s was always kind of pathetic... I noticed before..."), _("If %(pp)s's gonna stay... might as well give %(po)s a show..."), _("I mean... %(pp)s IS still here... says a lot about %(po)s...")],
                    "stats": {"Inbt": 7, "Obed": 5},
                    "expression": "lipbite",
                    "npc_stats": {"friendship_with_player": -35},
                    "npc_boundary_bar": -5,
                },
                "exhibitionist": {
                    "lines": [_("Mmm... %(pp)s's watching... keep mocking %(po)s... it's turning me on..."), _("%(name)s watching... you taunting %(po)s... I'm so wet right now..."), _("Keep going... I want %(po)s to hear every moan I make for you...")],
                    "stats": {"Inbt": 8, "Obed": 4},
                    "expression": "happy",
                    "npc_stats": {"friendship_with_player": -30},
                    "npc_boundary_bar": -3,
                },
                "_ntr_hostile": {
                    "lines": [_("Stop! %(name)s HATES this! You're making it so much worse! I... mmm... fuck..."), _("%(name)s, don't listen to him... please... I... I can't help the sounds I'm making..."), _("Leave %(po)s alone! %(Pp)s didn't... I didn't want... oh god, why can't I stop moaning...")],
                    "stats": {"Obed": 7, "Inbt": 8},
                    "expression": "scared",
                    "npc_stats": {"friendship_with_player": -25},
                    "npc_boundary_bar": 10,
                },
                "_ntr_voyeur": {
                    "lines": [_("I think... you might be right... %(pp)s does look... into it...?"), _("%(name)s hasn't moved... and %(pp)s... is that...? Oh god."), _("You called it. %(Pp)s's actually watching us without flinching...")],
                    "stats": {"Obed": 5, "Inbt": 6},
                    "expression": "surprised",
                    "npc_stats": {"friendship_with_player": -10},
                    "npc_boundary_bar": -2,
                },
                "_default": {
                    "lines": [_("That's... really cruel. %(name)s is right there..."), _("I don't think %(pp)s deserves that... even if... %(pp)s is still watching..."), _("Why would you say that to %(po)s... that's too far...")],
                    "stats": {"Obed": 5, "Inbt": 5},
                    "expression": "shy",
                    "npc_stats": {"friendship_with_player": -40},
                    "npc_boundary_bar": -5,
                },
            },
        },

        # ── NTR: PRAISE HER TO PARTNER ──────────────────────
        "ntr_praise": {
            "label": _("Praise her to partner"),
            "available": _tease_ntr_watching,
            "player_lines": {
                "_any": [
                    _("She loves it when I go deep, don't you baby?"),

                    _("She's such a good girl... look at her taking it all."),

                    _("You're lucky to have her... she knows how to fuck."),

                    _("Look at her... she can't get enough."),

                    _("You picked a good one, %(name)s... she's incredible."),

                ],
                "reverse_cowgirl": [
                    _("Look at that ass, %(name)s... you're a lucky one."),

                    _("She rides it so good from back here... you ever get this?"),

                ],
                "cowgirl": [
                    _("Watch her bounce... she's putting on a show for us."),

                    _("She rides like this for you too, %(name)s?"),

                ],
                "doggy": [
                    _("Look at her taking it from behind... beautiful, right %(name)s?"),

                    _("She loves it doggy... I bet you already knew that."),

                ],
                "bj": [
                    _("She's got the best mouth... you know that already, %(name)s."),

                    _("Look at her go... she was born for this."),

                ],
                "hj": [
                    _("Those hands... %(name)s, you're lucky she touches you at all."),

                ],
                "tj": [
                    _("Those tits around my cock... %(name)s, you ever get this?"),

                ],
                "full_nelson": [
                    _("Look at her, %(name)s... she takes it like this and still begs for more."),

                    _("She's incredible like this... you should be proud of her."),

                ],
                "laying_down": [
                    _("Look at her holding on to me... she's amazing, %(name)s."),

                    _("She gives everything when she's under me... you're a lucky one."),

                ],
                "anal": [
                    _("She takes it in the ass like a champ... you should be proud, %(name)s."),

                    _("Look how well she handles it... incredible girl."),

                ],
                # ── Bet event: his back is turned, he only hears ──
                "_ntr_listening": [
                    _("Hear that, %(name)s? That's what she sounds like when she's really enjoying it."),

                    _("You're missing the best part with your back turned, %(name)s. She looks incredible."),

                    _("Listen to her, %(name)s... you should be proud of how good she is."),

                    _("She's giving me everything, %(name)s. Turn around, she deserves an audience."),

                ],
            },
            "reactions": {
                # ── Bet event: his back is turned, he only hears ──
                "_ntr_listening": {
                    "lines": [_("Don't say that... %(pp)s can hear you..."), _("%(name)s... don't listen to him... oh god..."), _("This is so embarrassing... %(pp)s's right there hearing all of it...")],
                    "stats": {"Obed": 3, "Inbt": 3},
                    "expression": "shy",
                    "npc_stats": {"friendship_with_player": 15},
                    "npc_boundary_bar": 6,
                },
                "_ntr_listening_hardcore_sex": {
                    "lines": [_("Save the compliments. Make me loud enough that %(pp)s has to turn around."), _("%(pp)s can hear how good I am. Now prove it harder."), _("Praise me later. Make me scream now.")],
                    "stats": {"Obed": 4, "Inbt": 5},
                    "expression": "lipbite",
                    "npc_stats": {"friendship_with_player": 10},
                    "npc_boundary_bar": 6,
                },
                "_ntr_listening_cute_sex": {
                    "lines": [_("N-not with %(po)s listening... please..."), _("My face is burning... %(pp)s can hear every word..."), _("%(name)s... cover your ears... please...")],
                    "stats": {"Obed": 3, "Love": 2},
                    "expression": "shy",
                    "npc_stats": {"friendship_with_player": 20},
                    "npc_boundary_bar": 8,
                },
                "_ntr_listening_exhibitionist": {
                    "lines": [_("Louder... I want %(po)s to hear exactly how good I am..."), _("Make %(po)s turn around... I want %(po)s to see it too...")],
                    "stats": {"Inbt": 6, "Obed": 3},
                    "expression": "happy",
                    "npc_stats": {"friendship_with_player": 15},
                    "npc_boundary_bar": 8,
                },
                "hardcore_sex": {
                    "lines": [_("You two talking about me like I'm not here? ...Keep going."), _("Stop being polite and fuck me harder. Both of you can praise me later."), _("I don't need compliments. I need it deeper.")],
                    "stats": {"Obed": 4, "Inbt": 5},
                    "expression": "lipbite",
                    "npc_stats": {"friendship_with_player": 20},
                    "npc_boundary_bar": 8,
                },
                "cute_sex": {
                    "lines": [_("D-don't talk about me like that... not in front of %(name)s..."), _("This is so embarrassing... %(pp)s's right there watching..."), _("Please... not while %(pp)s can hear...")],
                    "stats": {"Obed": 3, "Love": 2},
                    "expression": "shy",
                    "npc_stats": {"friendship_with_player": 25},
                    "npc_boundary_bar": 10,
                },
                "cheater": {
                    "lines": [_("Mmm... you hear that, %(name)s? He thinks I'm special..."), _("See? He appreciates me more than you ever did..."), _("At least someone knows what I'm worth...")],
                    "stats": {"Inbt": 5, "Obed": 3},
                    "expression": "lipbite",
                    "npc_stats": {"friendship_with_player": 15},
                    "npc_boundary_bar": 6,
                },
                "exhibitionist": {
                    "lines": [_("I love being shown off... tell %(po)s more..."), _("Mmm... having %(po)s watch while you say that... it's so hot...")],
                    "stats": {"Inbt": 6, "Obed": 3},
                    "expression": "happy",
                    "npc_stats": {"friendship_with_player": 20},
                    "npc_boundary_bar": 10,
                },
                "_default": {
                    "lines": [_("I can't believe you're saying this while %(pp)s watches..."), _("This is so weird... but... don't stop..."), _("%(name)s is right there... why does this turn me on...")],
                    "stats": {"Obed": 3, "Inbt": 3},
                    "expression": "shy",
                    "npc_stats": {"friendship_with_player": 20},
                    "npc_boundary_bar": 8,
                },
                "_ntr_hostile": {
                    "lines": [_("Stop trying to be nice about it... this isn't a compliment... it's torture..."), _("%(name)s doesn't need your approval... but... mmm... don't stop saying those things..."), _("You're... praising %(po)s? While doing THIS?! ...Why does that make it worse...")],
                    "stats": {"Obed": 5, "Inbt": 6},
                    "expression": "shy",
                    "npc_stats": {"friendship_with_player": 10},
                    "npc_boundary_bar": 12,
                },
            },
        },

        # ── NTR: DEGRADE THE PARTNER ─────────────────────────
        "ntr_degrade": {
            "label": _("Degrade the partner"),
            "available": _tease_ntr_watching,
            "player_lines": {
                "_any": [
                    _("She needs a real one... not whatever you've got, %(name)s."),

                    _("Just sit there and watch, %(name)s. This is how it's done."),

                    _("%(Pp)s could never make her moan like this."),

                    _("You could never give her what I'm giving right now."),

                    _("How does it feel watching someone else do your job, %(name)s?"),

                ],
                "_any_male": [
                    _("She needs a bigger dick than yours, %(name)s."),

                    _("Just sit there and watch a real man work."),

                ],
                "_any_female": [
                    _("Your fingers could never do this, %(name)s."),

                    _("A woman could never give her all this."),

                ],
                "reverse_cowgirl": [
                    _("She never rides you like this, does she, %(name)s?"),

                    _("Look at her bouncing... you never got this, did you?"),

                ],
                "cowgirl": [
                    _("She's riding me like she's forgotten you exist, %(name)s."),

                    _("This is what real riding looks like. Take notes, %(name)s."),

                ],
                "doggy": [
                    _("I bet you never fucked her this deep, %(name)s."),

                    _("She's screaming MY name, not yours."),

                ],
                "bj": [
                    _("She never sucked you like this, did she?"),

                    _("She's on her knees for ME, %(name)s. Not you."),

                ],
                "hj": [
                    _("She's jerking ME off... not you. Remember that, %(name)s."),

                ],
                "tj": [
                    _("Those tits wrapped around MY cock... how does that feel, %(name)s?"),

                ],
                "full_nelson": [
                    _("Could you even hold her up like this, %(name)s? Didn't think so."),

                    _("Pinned, spread and moaning for me. You never got her like this."),

                ],
                "laying_down": [
                    _("She's holding me like she never held you, %(name)s."),

                    _("Watch how she wraps her legs around a real man."),

                ],
                "anal": [
                    _("Her ass is mine now, %(name)s. You never had a chance."),

                    _("She takes it in the ass for ME. Let that sink in."),

                ],
                # ── Bet event: his back is turned, he only hears ──
                "_ntr_listening": [
                    _("Even with your back turned you can hear I'm doing your job better, %(name)s."),

                    _("She never sounded like this for you, did she, %(name)s? Admit it."),

                    _("Keep facing the wall, %(name)s. It's the most useful thing you've done for her."),

                    _("Every moan you hear is one you never got out of her, %(name)s."),

                ],
            },
            "reactions": {
                # ── Bet event: his back is turned, he only hears ──
                "_ntr_listening": {
                    "lines": [_("That's harsh... %(pp)s's standing right there..."), _("%(pp)s can hear you... don't...")],
                    "stats": {"Obed": 4, "Inbt": 4},
                    "expression": "surprised",
                    "npc_stats": {"friendship_with_player": -30},
                    "npc_boundary_bar": -5,
                },
                "_ntr_listening_hardcore_sex": {
                    "lines": [_("That's so cruel... and I'm getting wetter... say it louder..."), _("%(pp)s can hear every word... fuck... don't stop...")],
                    "stats": {"Obed": 6, "Inbt": 6},
                    "expression": "lipbite",
                    "npc_stats": {"friendship_with_player": -30},
                    "npc_boundary_bar": -5,
                },
                "_ntr_listening_cute_sex": {
                    "lines": [_("Why would you say that... %(pp)s can hear you..."), _("Please stop... %(pp)s didn't do anything wrong...")],
                    "stats": {"Love": -3, "Obed": 4, "Inbt": 3},
                    "expression": "scared",
                    "npc_stats": {"friendship_with_player": -40},
                    "npc_boundary_bar": -5,
                },
                "_ntr_listening_cheater": {
                    "lines": [_("Harsh... but %(pp)s's still standing there taking it..."), _("Not wrong though... and %(pp)s knows it...")],
                    "stats": {"Inbt": 7, "Obed": 5},
                    "expression": "lipbite",
                    "npc_stats": {"friendship_with_player": -25},
                    "npc_boundary_bar": -3,
                },
                "hardcore_sex": {
                    "lines": [_("That's so fucked up... but don't stop..."), _("You're cruel... and it's making me so wet..."), _("Say more... I don't care if it's wrong...")],
                    "stats": {"Obed": 6, "Inbt": 6},
                    "expression": "lipbite",
                    "npc_stats": {"friendship_with_player": -30},
                    "npc_boundary_bar": -5,
                },
                "cute_sex": {
                    "lines": [_("Why would you say that...? %(name)s is right there..."), _("That's so cruel... please stop... %(pp)s can hear you..."), _("I feel sick... don't talk to %(po)s like that...")],
                    "stats": {"Love": -3, "Obed": 4, "Inbt": 3},
                    "expression": "scared",
                    "npc_stats": {"friendship_with_player": -40},
                    "npc_boundary_bar": -5,
                },
                "cheater": {
                    "lines": [_("That's horrible... but you're not wrong about that..."), _("%(name)s doesn't need to hear this... but it's true..."), _("I shouldn't enjoy this as much as I do...")],
                    "stats": {"Inbt": 7, "Obed": 5},
                    "expression": "lipbite",
                    "npc_stats": {"friendship_with_player": -25},
                    "npc_boundary_bar": -3,
                },
                "_ntr_voyeur": {
                    "lines": [_("H-hey... that's harsh... but %(pp)s doesn't seem to mind...?"), _("%(name)s is still watching... I thought %(pp)s'd leave after that...")],
                    "stats": {"Obed": 5, "Inbt": 5},
                    "expression": "surprised",
                    "npc_stats": {"friendship_with_player": -15},
                    "npc_boundary_bar": -1,
                },
                "_ntr_proud": {
                    "lines": [_("%(name)s looks furious... maybe you should stop..."), _("I think you went too far... %(pp)s looks like %(pp)s wants to leave...")],
                    "stats": {"Obed": 4, "Inbt": 3},
                    "expression": "scared",
                    "npc_stats": {"friendship_with_player": -60},
                    "npc_boundary_bar": -10,
                    "npc_end_watching_chance": 0.35,
                },
                "_default": {
                    "lines": [_("That was... really harsh. %(name)s is RIGHT there..."), _("Did you really just say that to %(po)s...?"), _("I don't know how to feel about that...")],
                    "stats": {"Obed": 5, "Inbt": 4},
                    "expression": "surprised",
                    "npc_stats": {"friendship_with_player": -35},
                    "npc_boundary_bar": -5,
                },
                "_ntr_hostile": {
                    "lines": [_("Don't talk to %(po)s like that...! %(name)s didn't do anything wrong... even if... mmm..."), _("That's cruel... %(pp)s is right there... and I... I should stop this... but I can't..."), _("%(name)s hates you enough already... stop making it worse... oh god, why am I still moaning...")],
                    "stats": {"Obed": 6, "Inbt": 7},
                    "expression": "scared",
                    "npc_stats": {"friendship_with_player": -20},
                    "npc_boundary_bar": 5,
                },
            },
        },

        # ── TEASE HER ABOUT THE FOOT THING (FJ only) ────────────
        "foot_tease": {
            "label": _("Tease her about the foot thing"),
            # NEVER a lambda here: _tease_menu's loop keeps the last entry in a store variable (_tv), and a lambda in
            # it made every save after a tease menu crash (PicklingError, 2026-10-07)
            "available": _tease_footjob_only,
            "player_lines": {
                "_any": [
                    _("You're surprisingly good at this with your feet..."),

                    _("I wonder how many guys dream about this..."),

                    _("Your toes feel amazing, you know that?"),

                    _("I bet you practiced this, didn't you?"),

                    _("Who knew your feet were this talented?"),

                ],
            },
            "reactions": {
                "cute_sex": {
                    "lines": [_("S-shut up... it's embarrassing enough without you commenting..."), _("Don't say it like that... you're making me blush..."), _("I can't believe I'm doing this, okay? Stop reminding me...")],
                    "stats": {"Love": 3, "Obed": 1},
                    "expression": "shy",
                },
                "hardcore_sex": {
                    "lines": [_("You want gentle? Wrong girl. I'm going harder."), _("Less talking. Faster is more fun anyway."), _("Talented? Wait until I stop being gentle.")],
                    "stats": {"Obed": 3, "Inbt": 1},
                    "expression": "lipbite",
                },
                "femdom": {
                    "lines": [_("You like my feet that much? Then maybe I should make you beg for them."), _("Keep talking and I'll squeeze harder."), _("That's right... worship them.")],
                    "stats": {"Inbt": 1},
                    "expression": "lipbite",
                },
                "cum_slut": {
                    "lines": [_("Just wait until you finish all over them..."), _("I can feel you twitching... you're going to make such a mess on my feet..."), _("Keep going... I want to feel it between my toes...")],
                    "stats": {"Love": 2, "Obed": 2},
                    "expression": "happy",
                },
                "submissive": {
                    "lines": [_("If you like them... then use them however you want. Tell me what to do."), _("Okay. My feet. Whatever you say. I'll do my best.")],
                    "stats": {"Obed": 3, "Inbt": 1},
                    "expression": "shy",
                },
                "_default": {
                    "lines": [_("This is so weird... but I kind of like how much you're into it."), _("I never thought I'd be good at something like this..."), _("Your reactions are making me feel strangely powerful...")],
                    "stats": {"Love": 2},
                    "expression": "happy",
                },
            },
        },
    }

    _TEASE_TRAIT_PRIORITY = [
        "cum_slut", "hate_cum",
        "pregnancy_fetish", "pregnancy_fear",
        "anal_lover", "anal_hater",
        "exhibitionist", "public_fetish", "public_shy",
        "camera_lover", "camera_hater",
        "femdom", "submissive",
        "hardcore_sex", "cute_sex",
        "cheater", "loyal",
        "nerd", "gym_rat",
    ]

    # ── Balance: what a tease is worth depends on HER, right now ─────────
    # The reaction pool (her traits / the context) decides the direction and her line; these knobs decide how
    # much of its "stats" lands (tease_stat_changes):
    #   weight  1 light (praise), 2 medium, 3 heavy (humiliation, cum / pregnancy / money talk, the NTR taunts)
    #   heat    her heat right now: Lust + (Obed + Inbt) / 20 + TEASE_SCENE_HEAT (what she is already doing with
    #           you). Early on she needs to be close to the edge for heavy talk; later it lands from the start.
    #   mood    heat - TEASE_NEED[weight]: hot (>= TEASE_HOT_MARGIN), ok (>= 0), cold; TEASE_MOOD_MULT scales
    #           the gains and the losses of the pool (a loss never grows past the pool: a trait she hates
    #           stings in full when she is cold, half when she is hot)
    #   too soon  a HEAVY tease that lands cold from a pool with no loss and no taste of hers behind it (no trait
    #           matched) costs TEASE_TOO_SOON on top: too much, too soon
    #   repeat  the same tease on her again in this time slot: gains x TEASE_REPEAT_MULT (losses never fade)
    TEASE_WEIGHT = {
        "praise": 1, "lesbian_praise": 1, "breed_praise": 1, "foot_tease": 1,
        "filming": 2, "public_talk": 2, "bf_humiliate": 2, "gf_humiliate": 2, "ntr_praise": 2,
        "husband_humiliate": 3,   # netori on a WIFE: heavier than the boyfriend talk on purpose
        "humiliate": 3, "cum_threat": 3, "breed_talk": 3, "atm_taste": 3, "lesbian_humiliate": 3,
        "financial_mock": 3, "ntr_cuckold_mock": 3, "ntr_degrade": 3,
        "count_slaps": 2,
    }
    # the DEGRADING teases: their Love loss goes through her Control trait (trait_love_loss: a submissive loses
    # none, a femdom more). A fear or a dislike (hate_cum, pregnancy_fear, camera_hater) is not deference: untouched.
    TEASE_LOVE_LOSS_INVERTED = frozenset(("humiliate", "bf_humiliate", "gf_humiliate", "husband_humiliate",
                                          "financial_mock", "ntr_degrade", "ntr_cuckold_mock", "atm_taste",
                                          "lesbian_humiliate", "count_slaps"))
    TEASE_NEED = {1: 0, 2: 60, 3: 100}
    TEASE_HOT_MARGIN = 50
    TEASE_SCENE_HEAT = {"hj": 0, "fj": 5, "tj": 5, "bj": 10, "rj": 10, "_anal": 25, "_default": 15}   # "_default" = the vaginal positions
    TEASE_MOOD_MULT = {"hot": (1.0, 0.5), "ok": (0.75, 0.75), "cold": (0.4, 1.0)}   # (gains, losses)
    TEASE_TOO_SOON = {"Love": -2}
    TEASE_REPEAT_MULT = (1.0, 0.6, 0.3, 0.0)   # 1st, 2nd, 3rd, 4th+ time this slot
    TEASE_HINTS = {
        "cold": _("She isn't worked up enough for that kind of talk yet."),
        "stale": _("She has heard that one already. It barely registers now."),
    }

    def tease_heat(girl, scene_type):
        _scene = "_anal" if _tease_is_anal_scene(scene_type) else scene_type
        _bonus = TEASE_SCENE_HEAT.get(_scene, TEASE_SCENE_HEAT["_default"])
        return int(getattr(girl, "Lust", 0) + (getattr(girl, "Obed", 0) + getattr(girl, "Inbt", 0)) / 20.0 + _bonus)

    def _tease_round(x):
        return int(x + (0.5 if x > 0 else -0.5))

    def tease_stat_changes(girl, tease_key, reaction, matched_trait, scene_type):
        """The stats a tease really moves on her (see Balance above), counted as one more use this slot.
        Returns (changes, hint): hint = a TEASE_HINTS line to narrate, or None."""
        _slot = (store.Day, store.TimeIndex)
        _rep = store._tease_repeat
        if _rep.get("_slot") != _slot:
            _rep.clear()
            _rep["_slot"] = _slot
        _k = "%s|%s" % (girl.gid, tease_key)
        _n = _rep.get(_k, 0)
        _rep[_k] = _n + 1
        _weight = TEASE_WEIGHT.get(tease_key, 2)
        _heat = tease_heat(girl, scene_type)
        _margin = _heat - TEASE_NEED[_weight]
        _mood = "hot" if _margin >= TEASE_HOT_MARGIN else ("ok" if _margin >= 0 else "cold")
        _g_mult, _l_mult = TEASE_MOOD_MULT[_mood]
        _r_mult = TEASE_REPEAT_MULT[min(_n, len(TEASE_REPEAT_MULT) - 1)]
        _base = dict((reaction or {}).get("stats", {}))
        _changes = {}
        for _stat, _amt in _base.items():
            _v = _tease_round(_amt * _g_mult * _r_mult) if _amt > 0 else _tease_round(_amt * _l_mult)
            if _v:
                _changes[_stat] = _v
        _hint = None
        _too_soon = _weight == 3 and _mood == "cold" and matched_trait is None and not any(_v < 0 for _v in _base.values())
        if _too_soon:
            for _stat, _amt in TEASE_TOO_SOON.items():
                _changes[_stat] = _changes.get(_stat, 0) + _amt
            if not _rep.get(girl.gid + "|!cold"):
                _rep[girl.gid + "|!cold"] = True
                _hint = TEASE_HINTS["cold"]
        elif _r_mult == 0 and any(_v > 0 for _v in _base.values()) and not _rep.get(_k + "|!stale"):
            _rep[_k + "|!stale"] = True
            _hint = TEASE_HINTS["stale"]
        if tease_key in TEASE_LOVE_LOSS_INVERTED and _changes.get("Love", 0) < 0:
            _changes["Love"] = trait_love_loss(girl, _changes["Love"])
            if not _changes["Love"]:
                del _changes["Love"]
        print("[TEASE_BALANCE] %s %s weight=%d heat=%d (need %d) mood=%s use #%d: %s -> %s%s" % (
            girl.gid, tease_key, _weight, _heat, TEASE_NEED[_weight], _mood, _n + 1, _base, _changes,
            " TOO SOON" if _too_soon else ""))
        return _changes, _hint

    def _tease_get_reaction(girl, tease_key, scene_type=None, contexts=None):
        """Pick the best reaction based on traits AND context.
        Order: scene contexts (partner watching / knows, girl watching, blackmail, condom)
        -> tease-specific rules (public, cum veteran, lesbian coercion, financial stage, NTR NPC)
        -> trait priority -> default.
        Returns (reaction_dict, matched_trait_or_None)."""
        tease = TEASE_OPTIONS.get(tease_key)
        if not tease:
            return None, None
        if _tease_is_anal_scene(scene_type) and "reactions_anal" in tease:
            reactions = tease["reactions_anal"]
        else:
            reactions = tease.get("reactions", {})
        _prio = tease.get("trait_priority", _TEASE_TRAIT_PRIORITY)

        # Scene contexts (most specific first): '<ctx>_<trait>[_first / _new]' then '<ctx>_<trait>' then '<ctx>'
        for _ctx in (contexts or []):
            for trait in _prio:
                if not girl.has_trait(trait):
                    continue
                _ck = "%s_%s" % (_ctx, trait)
                for _nk in trait_discovery_keys(girl, trait, _ck):
                    if _nk in reactions:
                        return reactions[_nk], trait
                if _ck in reactions:
                    return reactions[_ck], trait
            if _ctx in reactions:
                return reactions[_ctx], None

        # Context checks BEFORE trait checks
        if tease_key == "public_talk" and _is_public_location():
            _loc = getattr(store, "CurrentLocation", "")
            _gid = girl.gid
            # Per-character override (highest priority)
            if _loc == "classroom":
                _ck = "_in_classroom_" + _gid
                if _ck in reactions:
                    return reactions[_ck], _gid
            _pk = "_in_public_" + _gid
            if _pk in reactions:
                return reactions[_pk], _gid
            # Per-trait public reactions
            if girl.has_trait("nerd"):
                if _loc == "classroom" and "_in_classroom_nerd" in reactions:
                    return reactions["_in_classroom_nerd"], "nerd"
                if "_in_public_nerd" in reactions:
                    return reactions["_in_public_nerd"], "nerd"
            if girl.has_trait("public_shy") and "_in_public_shy" in reactions:
                return reactions["_in_public_shy"], "public_shy"
            if girl.has_trait("exhibitionist") and "_in_public_exb" in reactions:
                return reactions["_in_public_exb"], "exhibitionist"
            if girl.has_trait("public_fetish") and "_in_public_fetish" in reactions:
                return reactions["_in_public_fetish"], "public_fetish"
            if "_in_public" in reactions:
                return reactions["_in_public"], None

        if tease_key == "cum_threat" and _has_cum_inside_before(girl):
            if not girl.has_trait("cum_slut") and not girl.has_trait("hate_cum"):
                if "_cum_veteran" in reactions:
                    return reactions["_cum_veteran"], None

        # She only answers "I'm already pregnant" once she knows it (days 0-6 are hidden, even from her)
        if tease_key == "breed_talk" and getattr(girl, "_pregnant", False) and getattr(girl, "_pregnancy_known", False):
            if "_already_pregnant" in reactions:
                return reactions["_already_pregnant"], None

        # She already gave birth but is not currently pregnant (and hasn't had the procedure yet)
        if tease_key == "breed_talk" and getattr(girl, "_pregnancy_count", 0) > 0 and not getattr(girl, "_pregnant", False):
            _multi = getattr(girl, "_pregnancy_count", 0) >= 2
            _prefix = "_had_babies" if _multi else "_had_baby"
            for trait in _prio:
                _hb = "%s_%s" % (_prefix, trait)
                if _hb in reactions and girl.has_trait(trait):
                    return reactions[_hb], trait
            if _prefix in reactions:
                return reactions[_prefix], None

        # Sterile since the procedure, and she already TOLD him: the threat is empty and both know it.
        # Before she tells him she reacts as always (her line would give the story away).
        if tease_key == "breed_talk" and pregnancy_had_procedure(girl) and girl.get_flag("discovered_trait_infertile"):
            if "_cant_conceive" in reactions:
                return reactions["_cant_conceive"], None

        # Lesbian coercion check — uses CURRENT scene coercion type, not historical leverage
        if tease_key in ("lesbian_humiliate", "gf_humiliate") and girl.has_trait("lesbian"):
            _obed = getattr(girl, "Obed", 0)
            if _obed >= 1000 and "_lesbian_broken" in reactions:
                unlock_achievement("identity_crisis")
                return reactions["_lesbian_broken"], None
            _ct = getattr(store, "_coercion_type", None)
            if _ct == "blackmail":
                if girl.has_trait("cute_sex") and "_lesbian_coerced_cute" in reactions:
                    return reactions["_lesbian_coerced_cute"], "cute_sex"
                if girl.has_trait("hardcore_sex") and "_lesbian_coerced_hc" in reactions:
                    return reactions["_lesbian_coerced_hc"], "hardcore_sex"
                if "_lesbian_coerced" in reactions:
                    return reactions["_lesbian_coerced"], None
            elif _ct == "financial":
                if girl.has_trait("cute_sex") and "_lesbian_paid_cute" in reactions:
                    return reactions["_lesbian_paid_cute"], "cute_sex"
                if girl.has_trait("hardcore_sex") and "_lesbian_paid_hc" in reactions:
                    return reactions["_lesbian_paid_hc"], "hardcore_sex"
                if "_lesbian_paid" in reactions:
                    return reactions["_lesbian_paid"], None

        # Financial mock: stage 2-3 (transactional/dependent) overrides her traits;
        # stage 0-1 lets cheater/loyal/hardcore/cute color the shame, stage pool as fallback
        _fin_fallback = None
        if tease_key == "financial_mock":
            _fin_att = getattr(girl, "_financial_attitude", 0)
            _fin_key = "_financial_stage_%d" % _fin_att
            if _fin_att >= 2 and _fin_key in reactions:
                return reactions[_fin_key], None
            _fin_fallback = reactions.get(_fin_key)

        # NTR hostile mode: takes priority over all NPC traits for praise, degrade, cuckold mock
        if tease_key in ("ntr_praise", "ntr_degrade", "ntr_cuckold_mock"):
            _npc = getattr(store, "_ntr_watching_npc", None)
            if _npc and _ntr_is_hostile_mode(_npc):
                if "_ntr_hostile" in reactions:
                    return reactions["_ntr_hostile"], None

        # NTR degrade/cuckold: NPC trait takes priority over girl traits
        if tease_key in ("ntr_degrade", "ntr_cuckold_mock"):
            _npc = getattr(store, "_ntr_watching_npc", None)
            if _npc:
                if _npc.has_trait("proud") and "_ntr_proud" in reactions:
                    return reactions["_ntr_proud"], None
                if _npc.has_trait("voyeur") and "_ntr_voyeur" in reactions:
                    return reactions["_ntr_voyeur"], None

        # Recording-aware: prefer _recording variant of the reaction key
        _is_rec = getattr(store, "_recording_active", False)

        # Trait checks in priority order (her discovery variants tried first: _first, then _new)
        for trait in _prio:
            if trait in reactions and hasattr(girl, "has_trait") and girl.has_trait(trait):
                for _nk in trait_discovery_keys(girl, trait):
                    if _is_rec and (_nk + "_recording") in reactions:
                        return reactions[_nk + "_recording"], trait
                    if _nk in reactions:
                        return reactions[_nk], trait
                if _is_rec and (trait + "_recording") in reactions:
                    return reactions[trait + "_recording"], trait
                return reactions[trait], trait

        if _fin_fallback is not None:
            return _fin_fallback, None
        if _is_rec and "_default_recording" in reactions:
            return reactions["_default_recording"], None
        return reactions.get("_default"), None

# ============================================================
# Tease Menu — called from any sex scene control menu
# ============================================================
label _tease_menu(girl, scene_type):
    $ debug_log("[DEBUG] _tease_menu: entered, scene=%s" % scene_type)

    python:
        _tease_choices = []
        _atm_cross_name = None
        _atm_src = getattr(store, "_atm_source_gid", None)
        if _atm_src and _atm_src != girl.gid:
            _atm_src_obj = GIRL_BY_ID.get(_atm_src)
            if _atm_src_obj:
                _atm_cross_name = _atm_src_obj.Name
        for _tk, _tv in TEASE_OPTIONS.items():
            if _tv["available"](girl, scene_type):
                _lbl = _(_tv["label"])
                if _tk == "atm_taste" and _atm_cross_name:
                    _lbl = _tl(_("Ask how %s's ass tastes")) % _atm_cross_name
                _tease_choices.append((_lbl, _tk))
        _tease_choices.append((_("Never mind"), "back"))
        _tease_pick = renpy.display_menu(_tease_choices)

    $ debug_log("[DEBUG] _tease_menu: picked=%s" % str(_tease_pick))

    if _tease_pick == "back":
        return

    $ advance_round(TIME_COSTS["sex_tick"])

    python:
        _tease = TEASE_OPTIONS[_tease_pick]
        _tease_ctx = _tease_contexts(girl, _tease_pick, scene_type)
        _npc_gender = None
        _npc_hostile = False
        # Any tease can address the partner in the room (%(name)s / %(pp)s tokens + npc_stats)
        _npc_format = _tease_partner_on_scene()
        if _npc_format:
            _npc_gender = getattr(store._ntr_watching_npc, "gender", "male")
            _npc_hostile = _ntr_is_hostile_mode(store._ntr_watching_npc)
        _player_line = _tease_pick_line(_tease["player_lines"], scene_type, npc_gender=_npc_gender, npc_hostile=_npc_hostile, contexts=_tease_ctx)
        if _npc_format:
            _player_line = _format_npc_line(store._ntr_watching_npc, _player_line, girl)
        if _tease_pick == "atm_taste" and _atm_cross_name:
            _player_line = renpy.random.choice([
                _tl(_("How does %s's ass taste?")) % _atm_cross_name,
                _tl(_("You like the taste of %s's ass?")) % _atm_cross_name,
            ])
        _reaction, _tease_matched_trait = _tease_get_reaction(girl, _tease_pick, scene_type, _tease_ctx)
        debug_log("[DEBUG] _tease_menu: key=%s reaction_expr=%s trait=%s ctx=%s" % (_tease_pick, _reaction.get("expression", "?") if _reaction else "None", _tease_matched_trait, _tease_ctx))

    $ Say_Player(_player_line)

    if _reaction:
        python:
            # a line that says the ass was HERS ("own_ass_lines", atm_taste) only plays when it was: never on a
            # cross ATM (threesome, it was another girl's: _atm_cross_name above)
            _tease_r_lines = list(_reaction["lines"])
            _tease_own_lines = list(_reaction.get("own_ass_lines", []))
            if _tease_own_lines and _atm_cross_name:
                print("[TEASE] %s %s: cross ATM (%s's ass), %d own-ass line(s) left out" % (
                    girl.gid, _tease_pick, _atm_cross_name, len(_tease_own_lines)))
            else:
                _tease_r_lines += _tease_own_lines
            # truth filter: a reaction that claims "today is NOT safe" / "I'm on the pill" only plays
            # while it is true for her, and teaches the player that fact (pregnancy.rpy)
            _girl_line = fert_pick_truthful(girl, _tease_r_lines)
            if _npc_format:
                _girl_line = _format_npc_line(store._ntr_watching_npc, _girl_line, girl)
            _tease_expr = _reaction.get("expression", "normal")

            # Force expression via sprite_state (per-pose safe attrs)
            # CG: mouth_smile=Lipbite, mouth_disgusted=Sad, mouth_laugh=Laugh
            # BJ: uses bj_eyes/bj_brows store vars + mouth via bj_idle_mouth (speed 0)
            _safe_expr = {
                "reverse_cowgirl": {
                    "happy":     {"mouth": "mouth_smile",    "eyes": "eyes_looking_to_player", "brows": "brows_normal"},
                    "shy":       {"mouth": "mouth_smile",    "eyes": "eyes_side",              "brows": "brows_confused"},
                    "sad":       {"mouth": "mouth_scared",   "eyes": "eyes_squint",            "brows": "brows_sad"},
                    "angry":     {"mouth": "mouth_serious",  "eyes": "eyes_squint_big",        "brows": "brows_confused"},
                    "lipbite":   {"mouth": "mouth_lipbite",  "eyes": "eyes_looking_to_player", "brows": "brows_horny"},
                    "surprised": {"mouth": "mouth_surprised","eyes": "eyes_surprised",         "brows": "brows_surprised"},
                    "scared":    {"mouth": "mouth_scared",   "eyes": "eyes_squint_big",        "brows": "brows_sad"},
                },
                "cowgirl": {
                    "happy":     {"mouth": "mouth_laugh",    "eyes": "eyes_surprised_2",       "brows": "brows_normal"},
                    "shy":       {"mouth": "mouth_laugh",    "eyes": "eyes_side",              "brows": "brows_confused"},
                    "sad":       {"mouth": "mouth_disgusted","eyes": "eyes_squint",            "brows": "brows_confused"},
                    "angry":     {"mouth": "mouth_serious",  "eyes": "eyes_squint_big",        "brows": "brows_confused"},
                    "lipbite":   {"mouth": "mouth_smile",    "eyes": "eyes_surprised_2",       "brows": "brows_horny"},
                    "surprised": {"mouth": "mouth_surprised","eyes": "eyes_surprised",         "brows": "brows_surprised"},
                    "scared":    {"mouth": "mouth_disgusted","eyes": "eyes_squint",            "brows": "brows_confused"},
                },
                "bj": {
                    "happy":     {"mouth": "mouth_happy",    "bj_eyes": "squint",       "bj_brows": 1},
                    "shy":       {"mouth": "mouth_smile",    "bj_eyes": "right_closed", "bj_brows": 2},
                    "sad":       {"mouth": "mouth_sad",      "bj_eyes": "squint_2",     "bj_brows": 3},
                    "angry":     {"mouth": "mouth_lipbite",  "bj_eyes": "squint_2",     "bj_brows": 4},
                    "lipbite":   {"mouth": "mouth_lipbite",  "bj_eyes": "squint",       "bj_brows": 1},
                    "surprised": {"mouth": "mouth_surprised","bj_eyes": "normal",       "bj_brows": 3},
                    "scared":    {"mouth": "mouth_sad",      "bj_eyes": "squint_2",     "bj_brows": 5},
                },
                "hj": {
                    "happy":     {"mouth": "mouth_smile",    "eyes": "eyes_squint_2",          "brows": "brows_normal"},
                    "shy":       {"mouth": "mouth_smile",    "eyes": "eyes_side",              "brows": "brows_confused"},
                    "sad":       {"mouth": "mouth_sad",      "eyes": "eyes_squint",            "brows": "brows_sad"},
                    "angry":     {"mouth": "mouth_serious",  "eyes": "eyes_squint_big",        "brows": "brows_confused"},
                    "lipbite":   {"mouth": "mouth_tongue",   "eyes": "eyes_surprised_2",       "brows": "brows_normal"},
                    "surprised": {"mouth": "mouth_surprised","eyes": "eyes_surprised",         "brows": "brows_surprised"},
                    "scared":    {"mouth": "mouth_surprised","eyes": "eyes_squint_big",        "brows": "brows_sad"},
                },
                "tj": {
                    "happy":     {"mouth": "mouth_laugh",    "eyes": "eyes_sexy",              "brows": "brows_normal"},
                    "shy":       {"mouth": "mouth_kiss",     "eyes": "eyes_looking_left",      "brows": "brows_confused"},
                    "sad":       {"mouth": "mouth_sad",      "eyes": "eyes_squint",            "brows": "brows_sad"},
                    "angry":     {"mouth": "mouth_sad",      "eyes": "eyes_squint",            "brows": "brows_confused_2"},
                    "lipbite":   {"mouth": "mouth_lipbite",  "eyes": "eyes_sexy",              "brows": "brows_challenging"},
                    "surprised": {"mouth": "mouth_surprised","eyes": "eyes_normal",            "brows": "brows_confused"},
                    "scared":    {"mouth": "mouth_surprised","eyes": "eyes_squint",            "brows": "brows_sad"},
                },
                "doggy": {
                    "happy":     {"mouth": "mouth_smile",    "eyes": "eyes_squint_2",          "brows": "brows_normal"},
                    "shy":       {"mouth": "mouth_smile",    "eyes": "eyes_side",              "brows": "brows_confused"},
                    "sad":       {"mouth": "mouth_sad",      "eyes": "eyes_squint",            "brows": "brows_sad"},
                    "angry":     {"mouth": "mouth_serious",  "eyes": "eyes_squint_big",        "brows": "brows_confused"},
                    "lipbite":   {"mouth": "mouth_lipbite",  "eyes": "eyes_surprised_2",       "brows": "brows_normal"},
                    "surprised": {"mouth": "mouth_surprised","eyes": "eyes_surprised",         "brows": "brows_surprised"},
                    "scared":    {"mouth": "mouth_surprised","eyes": "eyes_squint_big",        "brows": "brows_sad"},
                },
                # FN head is a ConditionSwitch on sprite_state (unknown values fall back to Normal)
                "full_nelson": {
                    "happy":     {"mouth": "mouth_laugh",    "eyes": "eyes_closed_happy",      "brows": "brows_surprised"},
                    "shy":       {"mouth": "mouth_smile",    "eyes": "eyes_side",              "brows": "brows_confused"},
                    "sad":       {"mouth": "mouth_sad",      "eyes": "eyes_squint",            "brows": "brows_sad"},
                    "angry":     {"mouth": "mouth_angry",    "eyes": "eyes_squint_big",        "brows": "brows_angry"},
                    "lipbite":   {"mouth": "mouth_lipbite",  "eyes": "eyes_sexy",              "brows": "brows_horny"},
                    "surprised": {"mouth": "mouth_surprised","eyes": "eyes_surprised",         "brows": "brows_surprised"},
                    "scared":    {"mouth": "mouth_scared",   "eyes": "eyes_surprised",         "brows": "brows_scared"},
                },
            }
            # Laying down uses the unified presets (authored for the LD head, _laying_safe handles fallback)
            _safe_expr["laying_down"] = {
                _k: dict(POSE_EXPRESSIONS["laying_down"][_k])
                for _k in ("happy", "shy", "sad", "angry", "lipbite", "surprised", "scared")
                if _k in POSE_EXPRESSIONS.get("laying_down", {})
            }
            _safe_expr["anal"] = _safe_expr["doggy"]
            _safe_expr["full_nelson_anal"] = _safe_expr["full_nelson"]
            _safe_expr["laying_anal"] = _safe_expr["laying_down"]
            _safe_expr["reverse_cowgirl_anal"] = _safe_expr["reverse_cowgirl"]
            _expr_map = _safe_expr.get(scene_type)
            if _expr_map is None:
                print("[TEASE] no expression map for scene_type=%s, falling back to hj" % scene_type)
                _expr_map = _safe_expr.get("hj", {})
            _face = _expr_map.get(_tease_expr, {})

            _dg_spd = _cum_get_speed(scene_type)

            # Save + apply expression (BJ uses store vars, others use sprite_state)
            if scene_type == "bj":
                _saved_bj = {
                    "bj_eyes": store.bj_eyes,
                    "bj_brows": store.bj_brows,
                    "bj_idle_mouth": store.bj_idle_mouth,
                }
                _saved_bj_force = _bj_pause_forcing()
                # Set mouth BEFORE render (baked into layeredimage attribute at speed 0)
                if "mouth" in _face:
                    store.bj_idle_mouth = _face["mouth"]
            else:
                _ss = sprite_state.setdefault(girl.Id, {})
                _saved_face = {k: _ss.get(k) for k in ("mouth", "eyes", "brows")}
                for _fk, _fv in _face.items():
                    _ss[_fk] = _fv

        # Re-render with new expression (BJ at speed 0 so she pauses to react)
        call _cum_dispatch_apply_speed(girl, scene_type, speed=(0 if scene_type == "bj" else _dg_spd)) from _call_tease_as

        # BJ: override eyes/brows after ApplySpeed reset (ConditionSwitch updates next frame)
        if scene_type == "bj":
            python:
                if "bj_eyes" in _face:
                    store.bj_eyes = _face["bj_eyes"]
                if "bj_brows" in _face:
                    store.bj_brows = _face["bj_brows"]
                print("[TEASE_BJ] before Say_Line: expr=%s face=%s mouth=%s eyes=%s brows=%s" % (
                    _tease_expr, _face, store.bj_idle_mouth, store.bj_eyes, store.bj_brows))

        $ Say_Line(girl, _girl_line)

        # Restore expression + re-render
        python:
            if scene_type == "bj":
                store.bj_eyes = _saved_bj["bj_eyes"]
                store.bj_brows = _saved_bj["bj_brows"]
                store.bj_idle_mouth = _saved_bj["bj_idle_mouth"]
                _bj_resume_forcing(_saved_bj_force)
            else:
                if _in_sex_nonbj():
                    store._pending_tease_restore = {
                        "gid": girl.gid,
                        "face": dict(_saved_face),
                    }
                else:
                    for _fk, _fv in _saved_face.items():
                        if _fv is not None:
                            _ss[_fk] = _fv

            # How much of the pool lands depends on her heat, the tease's weight and repetition (Balance above)
            _tease_stats, _tease_hint = tease_stat_changes(girl, _tease_pick, _reaction, _tease_matched_trait, scene_type)
            for _stat, _amt in _tease_stats.items():
                Change_Status(girl, _stat, _amt)
            girl.Lust = min(100, getattr(girl, "Lust", 0) + 3)
            if _tease_pick == "lesbian_praise":
                girl.apply_spectrum_temp_shift(5)
            if _tease_pick == "count_slaps":
                count_slaps_start(girl)
            if _tease_matched_trait and girl.has_trait(_tease_matched_trait):
                # has_trait gate also filters the per-GIRL reaction keys (matched returns the gid there)
                girl.discover("discovered_trait_%s" % _tease_matched_trait)

            # NPC stat changes (NTR watching teases)
            if _npc_format and store._ntr_partner_watching:
                _npc_w = store._ntr_watching_npc
                _npc_stats = _reaction.get("npc_stats", {})
                for _ns, _na in _npc_stats.items():
                    Change_NPC_Status(_npc_w, _ns, _na)
                _bar_amt = _reaction.get("npc_boundary_bar", 0)
                if _bar_amt != 0:
                    _npc_girl = GIRL_BY_ID.get(getattr(_npc_w, "girl_gid", ""))
                    if _npc_girl:
                        if _bar_amt > 0:
                            _ntr_increase_boundary_bar(_npc_w, _npc_girl, _bar_amt)
                        else:
                            _npc_w._ntr_boundary_bar = max(0, getattr(_npc_w, "_ntr_boundary_bar", 0) + _bar_amt)
                            _npc_girl._ntr_boundary_bar = _npc_w._ntr_boundary_bar
                _end_chance = _reaction.get("npc_end_watching_chance", 0)
                if _end_chance > 0 and renpy.random.random() < _end_chance:
                    store._ntr_degrade_storm_out = True

        # Too heavy for how worked up she is, or the same tease once too often: say so, once per slot
        if _tease_hint:
            $ Narration(_tease_hint)

        # NTR degrade: proud NPC storms out
        if getattr(store, "_ntr_degrade_storm_out", False):
            $ store._ntr_degrade_storm_out = False
            python:
                _storm_npc = store._ntr_watching_npc
                _storm_npc_name = _storm_npc.Name if _storm_npc else "???"
                _storm_poss = _tr("her_poss") if getattr(_storm_npc, "gender", "male") == "female" else _tr("his")
            "[_storm_npc_name] clenches [_storm_poss] fists, shoots you a look of pure hatred, and storms out."
            $ _ntr_npc_leaves_scene(_storm_npc, girl)

        call _cum_dispatch_apply_speed(girl, scene_type, speed=_dg_spd) from _call_tease_as_r

    return
