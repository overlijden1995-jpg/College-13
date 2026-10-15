# ============================================================
# Petname System — player <-> girl pet names
# ============================================================

init python:

    # "crown": a name that raises her up (Queen, Goddess, Mistress). Accepting one is no submission (no Obed from
    # the dirty menu) and a femdom girl takes it as her due (docs/plan_femdom.md 7, PETNAME_FEMDOM_LINES).
    PETNAMES_FOR_GIRL = {
        "safe": {
            "Princess": {"T": 350, "Type": "L", "trait_bonus": {"cute_sex": 100, "hardcore_sex": -50}},
            "Babe":     {"T": 350, "Type": "L", "trait_bonus": {}},
            "Honey":    {"T": 350, "Type": "L", "trait_bonus": {"cute_sex": 50}},
            "Love":     {"T": 450, "Type": "L", "trait_bonus": {}},
            "Angel":    {"T": 350, "Type": "L", "trait_bonus": {"cute_sex": 100, "hardcore_sex": -100}},
            "Queen":    {"T": 400, "Type": "L", "crown": True, "trait_bonus": {"femdom": 200}},
            "Goddess":  {"T": 450, "Type": "L", "crown": True, "trait_bonus": {"femdom": 250}},
            # family only ("only_types": the menu lists it only for her girl type)
            "Stepmom":  {"T": 250, "Type": "L", "only_types": ("family",), "trait_bonus": {}},
        },
        "risky": {
            "Slut":         {"T": 750, "Type": "OI", "trait_bonus": {"hardcore_sex": 300, "cute_sex": -400, "anal_lover": 100, "femdom": -400}},
            "Whore":        {"T": 850, "Type": "OI", "trait_bonus": {"hardcore_sex": 300, "cute_sex": -500, "anal_lover": 100, "femdom": -400}},
            "Cumdumpster":  {"T": 950, "Type": "OI", "trait_bonus": {"cum_slut": 500, "hardcore_sex": 200, "cute_sex": -600, "femdom": -400}},
            # her liking him and being uninhibited (LI), not her obedience: it is a title, not a leash
            "Mistress":     {"T": 700, "Type": "LI", "crown": True, "trait_bonus": {"femdom": 500, "submissive": -300, "cute_sex": -200}},
        },
    }

    # "only_traits": a name only a VETERAN of one of these traits gives him or accepts (femdom: Pet, Toy, Good boy);
    # every other girl never offers it and refuses it (_petname_allowed). Master / Daddy: a femdom girl never calls him
    # that on her own (PETNAME_AUTO_VETO) and almost never agrees to.
    PETNAMES_FOR_PLAYER = {
        "Cutie":      {"stat": "Love", "min": 500, "T": 350, "Type": "L",  "trait_bonus": {"cute_sex": 100}},
        "Pumpkin":    {"stat": "Love", "min": 500, "T": 450, "Type": "L",  "trait_bonus": {"cute_sex": 100, "hardcore_sex": -100}},
        "Sugar":      {"stat": "Love", "min": 500, "T": 450, "Type": "L",  "trait_bonus": {}},
        "Sweetheart": {"stat": "Love", "min": 700, "T": 650, "Type": "L",  "trait_bonus": {"cute_sex": 100}},
        "Tiger":      {"stat": "Inbt", "min": 700, "T": 650, "Type": "I",  "trait_bonus": {"hardcore_sex": 100}},
        "Daddy":      {"stat": "Love", "min": 900, "T": 850, "Type": "LI", "trait_bonus": {"hardcore_sex": 100, "cute_sex": -200, "femdom": -800}},
        "Master":     {"stat": "Obed", "min": 900, "T": 850, "Type": "OI", "trait_bonus": {"hardcore_sex": 300, "cute_sex": -400, "femdom": -800}},
        # respect, not romance (the author 2026-10-11): earned at high Obed, or BOUGHT by the blackmail
        # lane at her "his" step (petname_player_check's leverage bonus). A femdom never offers it.
        "Sir":        {"stat": "Obed", "min": 800, "T": 750, "Type": "OI", "trait_bonus": {"hardcore_sex": 100, "submissive": 200, "cute_sex": -100, "femdom": -600}},
        "Pet":        {"stat": "Love", "min": 500, "T": 450, "Type": "L",  "only_traits": ("femdom",), "trait_bonus": {"femdom": 300}},
        "Toy":        {"stat": "Inbt", "min": 700, "T": 650, "Type": "I",  "only_traits": ("femdom",), "trait_bonus": {"femdom": 300}},
        "Good boy":   {"stat": "Love", "min": 800, "T": 750, "Type": "LI", "only_traits": ("femdom",), "trait_bonus": {"femdom": 300}},
        # an older woman of his family (Shion): what she calls him from the start ("only_types"); "default": she just
        # calls him that from the moment they meet, no asking (petname_update_auto)
        "Boy":        {"stat": "Love", "min": 0, "T": 150, "Type": "L",  "only_types": ("family",), "default": True,
                       "trait_bonus": {"femdom": 200}},
    }

    # A name she never picks for him herself when its trait_bonus for her sums to this or less (a femdom and
    # Master / Daddy). Among the names of her best tier, each weighs 100 + her trait_bonus (at least the minimum).
    PETNAME_AUTO_VETO = -500
    PETNAME_AUTO_MIN_WEIGHT = 10

    # A veteran femdom's own answer about a name (docs/plan_femdom.md 7), key "<who>_<how>_<answer>":
    #   who    = "her" (he names her) / "him" (he asks her to call him that, or she proposes it)
    #   how    = "up" (trait_bonus["femdom"] > 0: a crown for her, a leash for him) / "down" (< 0)
    #   answer = "yes" / "no" / "ask" (she proposes it: petname_change_announcement)
    # (expression, lines); each line has exactly one %s (the name). A missing key = the usual lines.
    PETNAME_FEMDOM_LINES = {
        "her_up_yes": ("smug", [
            _("%s. Finally, someone who understands. Say it like you mean it."),
            _("%s... yes. That's right. Don't you ever forget it."),
        ]),
        "her_up_no": ("smirk", [
            _("%s? You haven't earned the right to call me that. Yet."),
        ]),
        "her_down_no": ("angry", [
            _("%s? Say that again and you won't touch me for a week. Pick a name that fits me."),
            _("I'm nobody's %s. On your knees and apologize. Then try again."),
        ]),
        "him_up_yes": ("smug", [
            _("%s? Perfect. You're finally admitting what you are."),
            _("%s. Yes. That's exactly what you are to me. Now come here."),
        ]),
        "him_up_ask": ("smug", [
            _("I've decided something. From now on, you're my %s."),
            _("From now on, I call you %s. I'm not asking."),
        ]),
        "him_down_yes": ("smirk", [
            _("%s? Fine. Say it all you want. We both know who's really in charge."),
        ]),
        "him_down_no": ("smirk", [
            _("%s? No. If anyone here gives the orders, it's me. Try again."),
            _("Call you %s? Other way around, sweetie. Try again."),
        ]),
    }

    _PETNAME_REJECT_PENALTIES = {
        "cute_sex": {"Love": -15},
        "loyal":    {"Love": -20},
        "_default": {"Love": -5},
    }

    _PETNAME_AUTO_TIERS = {
        "Cutie": 1, "Boy": 1,
        "Pumpkin": 2, "Sugar": 2, "Pet": 2,
        "Sweetheart": 3, "Tiger": 3, "Toy": 3,
        "Daddy": 4, "Master": 4, "Good boy": 4, "Sir": 4,
    }

    def _petname_story_locked(girl, cfg):
        """A pet name between them before her story opens it (story_act_locked "petname": her first step). A name of
        the family ("only_types": Boy, Stepmom) is no pet name: always open."""
        return not cfg.get("only_types") and story_act_locked(girl, "petname")

    def _petname_story_refusal(girl, check):
        """(expression, line) of a refusal her story makes (petname_give_check / petname_player_check), else None."""
        if check.get("outcome") != "story_locked":
            return None
        return ("annoyed", story_locked_line(girl, "petname"))

    def _petname_trait_bonus(girl, cfg):
        """Sum of the name's trait_bonus for the traits she has."""
        return sum(_v for _t, _v in cfg.get("trait_bonus", {}).items()
                   if hasattr(girl, "has_trait") and girl.has_trait(_t))

    def _petname_allowed(girl, cfg):
        """A name with "only_traits" belongs to a veteran of one of them (femdom: Pet, Toy, Good boy). A girl
        still discovering the trait, or without it, never offers it and refuses it. "only_types": only a girl of
        that girl type (family: Boy, Stepmom)."""
        _types = cfg.get("only_types")
        if _types and girl_type(girl) not in _types:
            return False
        _only = cfg.get("only_traits")
        return not _only or any(trait_is_veteran(girl, _t) for _t in _only)

    def _petname_femdom_line(girl, petname, cfg, who, answer):
        """A veteran femdom's own answer about a name, as (expression, line), or None: the usual lines speak
        (PETNAME_FEMDOM_LINES). Still discovering the trait she answers like anyone else (trait_line_keys rule)."""
        if not trait_is_veteran(girl, "femdom"):
            return None
        _fb = cfg.get("trait_bonus", {}).get("femdom", 0)
        if not _fb:
            return None
        _key = "%s_%s_%s" % (who, "up" if _fb > 0 else "down", answer)
        _entry = PETNAME_FEMDOM_LINES.get(_key)
        if not _entry:
            return None
        girl.discover("discovered_trait_femdom")
        print("[FEMDOM] %s: petname '%s' -> %s" % (girl.gid, petname, _key))
        return (_entry[0], _tl_fmt(renpy.random.choice(_entry[1]), _tr(petname)))

    def _auto_petname_for_player(girl):
        _rejected = getattr(girl, "_petname_rejected", set())
        _current = getattr(girl, "petname_for_player", None)
        _current_tier = _PETNAME_AUTO_TIERS.get(_current, 0)

        _candidates = []
        _best_tier = 0

        for pn, cfg in PETNAMES_FOR_PLAYER.items():
            if pn == _current or pn in _rejected:
                continue
            if not _petname_allowed(girl, cfg):
                continue
            if _petname_story_locked(girl, cfg):
                continue
            tier = _PETNAME_AUTO_TIERS.get(pn, 0)
            if tier <= _current_tier:
                continue
            stat_key = cfg.get("stat")
            stat_min = cfg.get("min", 0)
            if stat_key is not None and getattr(girl, stat_key, 0) < stat_min:
                continue
            _bonus = _petname_trait_bonus(girl, cfg)
            if _bonus <= PETNAME_AUTO_VETO:
                print("[PETNAME] %s never calls the player '%s' on her own (trait bonus %d)" % (girl.gid, pn, _bonus))
                continue
            if tier > _best_tier:
                _best_tier = tier
                _candidates = [(pn, _bonus)]
            elif tier == _best_tier:
                _candidates.append((pn, _bonus))

        if not _candidates:
            return None
        # the names her traits like weigh more (a femdom: Pet / Toy / Good boy)
        _weights = [max(PETNAME_AUTO_MIN_WEIGHT, 100 + _b) for _pn, _b in _candidates]
        _r = renpy.random.random() * sum(_weights)
        _pick = _candidates[-1][0]
        for (_pn, _b), _w in zip(_candidates, _weights):
            _r -= _w
            if _r <= 0:
                _pick = _pn
                break
        print("[PETNAME] %s auto candidates %s -> %s" % (girl.gid, _candidates, _pick))
        return _pick

    def _petname_bf_penalty(girl, category):
        has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        if not has_bf:
            return 0
        is_loyal = girl.has_trait("loyal") if hasattr(girl, "has_trait") else False
        is_cheater = girl.has_trait("cheater") if hasattr(girl, "has_trait") else False
        if is_cheater:
            return 0
        if category == "safe":
            base = -200
        else:
            base = -400
        if is_loyal:
            base = int(base * 1.5)
        return base

    def petname_give_check(girl, petname, category):
        cfg = PETNAMES_FOR_GIRL[category][petname]
        if _petname_story_locked(girl, cfg):
            return story_lock_result(girl, "petname")
        bonus = _petname_trait_bonus(girl, cfg)
        bonus += _petname_bf_penalty(girl, category)
        t = cfg["T"]
        has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        is_cheater = girl.has_trait("cheater") if hasattr(girl, "has_trait") else False
        if has_bf and not is_cheater:
            if category == "safe":
                t = int(t * 2)
            else:
                t += 400
        return ApprovalCheck(girl, T=t, Type=cfg["Type"], Bonus=bonus, ReturnData=True)

    def petname_player_check(girl, petname):
        cfg = PETNAMES_FOR_PLAYER[petname]
        if not _petname_allowed(girl, cfg):
            print("[PETNAME] %s refuses '%s': not hers to give (only_traits %s)" % (girl.gid, petname, cfg.get("only_traits")))
            return {"accepted": False, "outcome": "not_hers", "score": 0}
        if _petname_story_locked(girl, cfg):
            return story_lock_result(girl, "petname")
        bonus = _petname_trait_bonus(girl, cfg)
        # The coercion lane buys respect (the author 2026-10-11): a story locked to the BLACKMAIL lane,
        # at her "his" step or past it, answers "Sir" / "Master" to the leverage, not to her affection.
        # Her femdom "him_down_yes" line already carries the resentment ("we both know who's really in
        # charge"): no new voice needed.
        if (petname in ("Sir", "Master") and story_route_lock(girl) == "blackmail"
                and story_step(girl) >= 3):
            bonus += 600
            print("[PETNAME] %s: the blackmail lane weighs in on '%s' (+600)" % (girl.gid, petname))
        has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        is_cheater = girl.has_trait("cheater") if hasattr(girl, "has_trait") else False
        t = cfg["T"]
        if has_bf and not is_cheater:
            t += 300
            is_loyal = girl.has_trait("loyal") if hasattr(girl, "has_trait") else False
            if is_loyal:
                bonus -= 300
        return ApprovalCheck(girl, T=t, Type=cfg["Type"], Bonus=bonus, ReturnData=True)

    def _petname_reject_penalty(girl, category):
        if category == "safe":
            return
        if hasattr(girl, "has_trait") and girl.has_trait("hardcore_sex"):
            return
        for trait_key, penalties in _PETNAME_REJECT_PENALTIES.items():
            if trait_key == "_default":
                continue
            if hasattr(girl, "has_trait") and girl.has_trait(trait_key):
                for stat, val in penalties.items():
                    Change_Status(girl, stat, val)
                return
        for stat, val in _PETNAME_REJECT_PENALTIES["_default"].items():
            Change_Status(girl, stat, val)

    def petname_update_auto(girl):
        if not getattr(girl, "petname_for_player_auto", True):
            return None
        _last_ask = getattr(girl, "_petname_last_ask_day", -99)
        if store.Day - _last_ask < 2:
            return None
        has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        is_cheater = girl.has_trait("cheater") if hasattr(girl, "has_trait") else False
        if has_bf and not is_cheater:
            if getattr(girl, "Inbt", 0) < 600:
                _on_cheat = hasattr(girl, "_cheat_escalation_path") and getattr(girl, "_cheat_heat", 0) >= 60
                if not _on_cheat:
                    return None
        new_pn = _auto_petname_for_player(girl)
        current = getattr(girl, "petname_for_player", None)
        # the name she calls him from the moment they meet ("default": Boy): no asking, no event
        if new_pn and current is None and PETNAMES_FOR_PLAYER.get(new_pn, {}).get("default"):
            girl.petname_for_player = new_pn
            # known without a banner: she said nothing new now (she has called him that since they met)
            girl.set_flag("discovered_petname_for_player")
            print("[PETNAME] %s calls the player '%s' from the start (default name)" % (girl.gid, new_pn))
            return None
        if new_pn != current:
            girl._petname_pending_change = new_pn
            return new_pn
        return None

    def girl_calls_player(girl):
        pn = getattr(girl, "petname_for_player", None)
        if pn:
            return _tr(pn)
        return Player.Name

# ============================================================
# Petname Give Menu (player gives girl a petname)
# ============================================================
default _pn_sub_result = "back"

label petname_give_menu(girl):
    python:
        _current_pn = getattr(girl, "petname_from_player", None)
        if _current_pn:
            Say_Player(_tl(_("I currently call her %s.")) % _tr(_current_pn))

    while True:
        $ _pn_action = "none"
        menu:
            "Something sweet...":
                $ _pn_action = "sweet"
            "Something dirty..." if getattr(girl, "Inbt", 0) >= 200:
                $ _pn_action = "dirty"
            "Stop calling her that" if getattr(girl, "petname_from_player", None) is not None:
                $ _pn_action = "stop"
            "Never mind":
                $ _pn_action = "cancel"

        if _pn_action == "sweet":
            call _petname_sweet_pick(girl) from _call_pn_sweet
            if store._pn_sub_result != "back":
                return
        elif _pn_action == "dirty":
            call _petname_dirty_pick(girl) from _call_pn_dirty
            if store._pn_sub_result != "back":
                return
        elif _pn_action == "stop":
            $ Say_Player(_tl(_("Actually, forget the petname. I'll just call you %s.")) % girl.Name)
            python:
                _old = girl.petname_from_player
                _stop_line = renpy.random.choice([
                    _tl(_("Oh... okay. Back to %s then, I guess.")) % girl.Name,
                    _("Really? I was getting used to it... but okay."),

                ])
            $ Say_Line(girl, _stop_line)
            $ girl.petname_from_player = None
            $ debug_log("[DEBUG] Petname removed for %s" % girl.gid)
            return
        else:
            return

label _petname_sweet_pick(girl):
    $ store._pn_sub_result = "back"
    menu:
        "Princess":
            $ _pn_pick = "Princess"
        "Babe":
            $ _pn_pick = "Babe"
        "Honey":
            $ _pn_pick = "Honey"
        "Love":
            $ _pn_pick = "Love"
        "Angel":
            $ _pn_pick = "Angel"
        "Queen":
            $ _pn_pick = "Queen"
        "Goddess":
            $ _pn_pick = "Goddess"
        "Stepmom" if _petname_allowed(girl, PETNAMES_FOR_GIRL["safe"]["Stepmom"]):
            $ _pn_pick = "Stepmom"
        "Back":
            return

    $ _pn_cat = "safe"
    $ _pn_check = petname_give_check(girl, _pn_pick, _pn_cat)
    $ _pn_cfg = PETNAMES_FOR_GIRL[_pn_cat][_pn_pick]
    if _pn_check["accepted"]:
        $ Say_Player(_tl(_("From now on, I'm calling you %s.")) % _tr(_pn_pick))
        python:
            _pn_fd = _petname_femdom_line(girl, _pn_pick, _pn_cfg, "her", "yes")
            if _pn_fd:
                set_scene_expression(girl, _pn_fd[0])
                _accept_line = _pn_fd[1]
            elif girl.has_trait("cute_sex"):
                _accept_line = renpy.random.choice([
                    _("Really? That's so sweet... I love it! Call me that again."),

                    _tl(_("%s... I like how that sounds coming from you.")) % _tr(_pn_pick),
                    _("Aww... you're giving me a petname? That's adorable!"),

                ])
            elif girl.has_trait("hardcore_sex"):
                _accept_line = renpy.random.choice([
                    _("That's... cute. Fine. But only in private."),

                    _tl(_("%s? Alright. I can live with that.")) % _tr(_pn_pick),
                ])
            else:
                _accept_line = renpy.random.choice([
                    _("Mmm... I like how that sounds. Yeah, call me that."),

                    _tl(_("%s... okay. I'm into it.")) % _tr(_pn_pick),
                    _("You're giving me a petname? That's actually sweet."),

                ])
            has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
            if has_bf and not girl.has_trait("cheater"):
                _accept_line += _tl(_(" ...Just don't say it in front of my %s.")) % girl.partner_label()
        $ Say_Line(girl, _accept_line)
        $ girl.petname_from_player = _pn_pick
        $ girl.discover("discovered_petname_given")
        $ Change_Status(girl, "Love", 5)
        $ debug_log("[DEBUG] Petname given: %s -> %s" % (_pn_pick, girl.gid))
    else:
        python:
            _pn_fd = _petname_story_refusal(girl, _pn_check) or _petname_femdom_line(girl, _pn_pick, _pn_cfg, "her", "no")
            if _pn_fd:
                set_scene_expression(girl, _pn_fd[0])
                _reject_line = _pn_fd[1]
            else:
                _reject_line = renpy.random.choice([
                    _("Maybe later... I'm not ready for that yet."),

                    _("That's sweet, but... not right now."),

                    _("I don't think we're there yet."),

                ])
        $ Say_Line(girl, _reject_line)

    $ store._pn_sub_result = "done"
    return

label _petname_dirty_pick(girl):
    $ store._pn_sub_result = "back"
    menu:
        "Slut":
            $ _pn_pick = "Slut"
        "Whore":
            $ _pn_pick = "Whore"
        "Cumdumpster":
            $ _pn_pick = "Cumdumpster"
        "Mistress":
            $ _pn_pick = "Mistress"
        "Back":
            return

    $ _pn_cat = "risky"
    $ _pn_check = petname_give_check(girl, _pn_pick, _pn_cat)
    $ _pn_cfg = PETNAMES_FOR_GIRL[_pn_cat][_pn_pick]
    if _pn_check["accepted"]:
        $ Say_Player(_tl(_("From now on, you're my %s.")) % _tr(_pn_pick))
        python:
            _pn_fd = _petname_femdom_line(girl, _pn_pick, _pn_cfg, "her", "yes")
            if _pn_fd:
                set_scene_expression(girl, _pn_fd[0])
                _accept_line = _pn_fd[1]
            # being his / being used is submissive, not hardcore (docs/plan_femdom.md D3); a crown is no such name
            elif girl.has_trait("submissive") and not _pn_cfg.get("crown"):
                _accept_line = renpy.random.choice([
                    _("God, yes. Call me that. Especially when you're using me."),

                    _tl(_("Your %s... I like the sound of that.")) % _tr(_pn_pick),
                    _tl(_("I'm your %s. Use me like one.")) % _tr(_pn_pick),
                ])
            # an eager trait she is still discovering (trait_is_discovering) is no identity yet: no veteran pride.
            # These "filthy" lines are for a dirty name, never a crown
            elif girl.has_trait("hardcore_sex") and not trait_is_discovering(girl, "hardcore_sex") and not _pn_cfg.get("crown"):
                _accept_line = renpy.random.choice([
                    _("Say it again. I want to hear you call me that while you fuck me."),

                    _("Filthy. I love it. Say it while you pull my hair."),
                    _("Call me that while you're pounding me. It makes me even louder."),
                ])
            elif girl.has_trait("cum_slut") and _pn_pick == "Cumdumpster" and not trait_is_discovering(girl, "cum_slut"):
                _accept_line = renpy.random.choice([
                    _("Mmm... you know me so well. That's exactly what I am."),

                    _tl(_("Your personal %s... I accept that title with pride.")) % _tr(_pn_pick),
                ])
            elif girl.has_trait("cum_slut") and _pn_pick == "Cumdumpster":
                # still discovering it: the name fits what she is finding out about herself, and that shocks her
                _accept_line = renpy.random.choice([
                    _("That's so dirty... why do I like hearing it?"),
                    _("I should hate that. I don't. What are you doing to me?"),
                ])
            else:
                _accept_line = renpy.random.choice([
                    _("I can't believe I'm saying this... but okay. Just between us."),

                    _("You're really going to call me that? ...Fine. But only when we're alone."),

                ])
            has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
            if has_bf and not girl.has_trait("cheater"):
                _accept_line += _tl(_(" If my %s ever heard this... god.")) % girl.partner_label()
        $ Say_Line(girl, _accept_line)
        $ girl.petname_from_player = _pn_pick
        $ girl.discover("discovered_petname_given")
        $ Change_Status(girl, "Inbt", 10)
        # a crown raises her up: accepting it is no submission, so no Obed (a femdom never gains Obed asserting herself)
        if not _pn_cfg.get("crown"):
            $ Change_Status(girl, "Obed", 5)
        $ debug_log("[DEBUG] Risky petname given: %s -> %s" % (_pn_pick, girl.gid))
    else:
        python:
            _pn_fd = _petname_story_refusal(girl, _pn_check) or _petname_femdom_line(girl, _pn_pick, _pn_cfg, "her", "no")
            if _pn_fd:
                # a crown: not yet; a degrading name: she refuses it with an order (docs/plan_femdom.md 7)
                set_scene_expression(girl, _pn_fd[0])
                _reject_line = _pn_fd[1]
            elif girl.has_trait("cute_sex"):
                set_scene_expression(girl, "surprised", blush=1)
                _reject_line = renpy.random.choice([
                    _("What?! Why would you call me that?! That's horrible!"),

                    _("Are you serious?! That's so degrading! No!"),

                ])
            elif girl.has_trait("loyal"):
                set_scene_expression(girl, "uncomfortable")
                _reject_line = renpy.random.choice([
                    _tl(_("Are you serious? I have a %s and you want to call me THAT?")) % girl.partner_label(),
                    _tl(_("No. Absolutely not. My %s would... just no.")) % girl.partner_label(),
                ])
            else:
                set_scene_expression(girl, "serious")
                _reject_line = renpy.random.choice([
                    _("No. That's too far. Try something nicer."),

                    _tl(_("Yeah, no. I'm not your %s. Pick something else.")) % _tr(_pn_pick),
                ])
        $ Say_Line(girl, _reject_line)
        # a femdom turning down a crown ("not yet") is not offended by it: no penalty
        if not (_pn_fd and _pn_cfg.get("crown")):
            $ _petname_reject_penalty(girl, "risky")

    $ store._pn_sub_result = "done"
    return

# ============================================================
# Petname Player Menu (girl's petname for the player)
# ============================================================
label petname_player_menu(girl):
    python:
        _current_pn = getattr(girl, "petname_for_player", None)
        _is_auto = getattr(girl, "petname_for_player_auto", True)
        if _current_pn:
            _status = _("(she chose)") if _is_auto else _("(you chose)")
            Narration(_tl(_("She currently calls you %s %s.")) % (_tr(_current_pn), _status))
        else:
            Narration(_("She doesn't have a special name for you yet."))

    while True:
        $ _pnp_action = "none"
        menu:
            "Call me...":
                $ _pnp_action = "call_me"
            "Let her decide" if not getattr(girl, "petname_for_player_auto", True):
                $ _pnp_action = "auto"
            "Never mind":
                $ _pnp_action = "cancel"

        if _pnp_action == "call_me":
            call _petname_player_pick(girl) from _call_pnp_pick
            if store._pn_sub_result != "back":
                return
        elif _pnp_action == "auto":
            $ girl.petname_for_player_auto = True
            python:
                _new_auto = _auto_petname_for_player(girl)
                girl.petname_for_player = _new_auto
                # a veteran femdom picking Pet / Toy / Good boy tells him what he is (docs/plan_femdom.md 7)
                _pn_fd = _petname_femdom_line(girl, _new_auto, PETNAMES_FOR_PLAYER[_new_auto], "him", "ask") if _new_auto else None
                if _pn_fd:
                    set_scene_expression(girl, _pn_fd[0])
                    _let_line = _pn_fd[1]
                elif _new_auto:
                    _let_line = renpy.random.choice([
                        _tl(_("Okay! I'll call you whatever feels right. How about... %s?")) % _tr(_new_auto),
                        _tl(_("You're letting me pick? Hmm... I think I'll go with %s.")) % _tr(_new_auto),
                    ])
                else:
                    _let_line = renpy.random.choice([
                        _("Okay! I'll call you whatever feels right. I'll think of something."),

                        _("You're letting me pick? Hmm... I'll figure something out."),

                    ])
            $ Say_Line(girl, _let_line)
            $ debug_log("[DEBUG] Player petname auto-assigned: %s -> %s" % (girl.gid, _new_auto))
            return
        else:
            return

label _petname_player_pick(girl):
    $ store._pn_sub_result = "back"
    menu:
        "Cutie":
            $ _pn_pick = "Cutie"
        "Pumpkin":
            $ _pn_pick = "Pumpkin"
        "Sugar":
            $ _pn_pick = "Sugar"
        "Sweetheart":
            $ _pn_pick = "Sweetheart"
        "Tiger":
            $ _pn_pick = "Tiger"
        "Daddy":
            $ _pn_pick = "Daddy"
        "Master":
            $ _pn_pick = "Master"
        "Sir":
            $ _pn_pick = "Sir"
        # only a veteran femdom agrees to these (only_traits); every other girl refuses (docs/plan_femdom.md 7)
        "Pet":
            $ _pn_pick = "Pet"
        "Toy":
            $ _pn_pick = "Toy"
        "Good boy":
            $ _pn_pick = "Good boy"
        "Boy" if _petname_allowed(girl, PETNAMES_FOR_PLAYER["Boy"]):
            $ _pn_pick = "Boy"
        "Back":
            return

    $ Say_Player(_tl(_("I want you to call me %s.")) % _tr(_pn_pick))
    $ _pn_check = petname_player_check(girl, _pn_pick)
    $ _pn_cfg = PETNAMES_FOR_PLAYER[_pn_pick]

    if _pn_check["accepted"]:
        python:
            has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
            is_cheater = girl.has_trait("cheater") if hasattr(girl, "has_trait") else False
            # her partner's line comes first (and her femdom line would reveal the trait for nothing)
            _pn_fd = None if (has_bf and not is_cheater) else _petname_femdom_line(girl, _pn_pick, _pn_cfg, "him", "yes")
            if has_bf and not is_cheater:
                _accept_line = renpy.random.choice([
                    _tl(_("You want me to call you %s? ...My %s would kill me. But okay, %s.")) % (_tr(_pn_pick), girl.partner_label(), _tr(_pn_pick)),
                    _tl(_("%s... calling another man that... what am I doing? ...Okay, %s.")) % (_tr(_pn_pick), _tr(_pn_pick)),
                ])
            elif _pn_fd:
                set_scene_expression(girl, _pn_fd[0])
                _accept_line = _pn_fd[1]
            elif (_pn_pick in ("Sir", "Master") and story_route_lock(girl) == "blackmail"
                    and story_step(girl) >= 3):
                # the blackmail lane bought the yes (petname_player_check's leverage bonus): she says the
                # word and makes sure he hears what it cost (a femdom answers with him_down_yes above)
                set_scene_expression(girl, "annoyed")
                _accept_line = renpy.random.choice([
                    _tl(_("...%s. There. Is that what you wanted to hear?")) % _tr(_pn_pick),
                    _tl(_("%s. Fine. You can make me say it. You can't make me mean it.")) % _tr(_pn_pick),
                    _tl(_("As you wish... %s. Enjoy it while it lasts.")) % _tr(_pn_pick),
                ])
            elif _pn_pick in ("Master", "Daddy", "Sir"):
                # obeying him is submissive, not hardcore (docs/plan_femdom.md D3): hardcore only wants it rough
                if girl.has_trait("submissive"):
                    _accept_line = renpy.random.choice([
                        _tl(_("Yes, %s. Whatever you say, %s.")) % (_tr(_pn_pick), _tr(_pn_pick)),
                        _tl(_("%s... I like the sound of that. You've earned it.")) % _tr(_pn_pick),
                        _tl(_("Yes, %s. I'll do anything you tell me.")) % _tr(_pn_pick),
                    ])
                elif girl.has_trait("hardcore_sex"):
                    _accept_line = renpy.random.choice([
                        _tl(_("%s? Fine. As long as you keep fucking me this hard.")) % _tr(_pn_pick),
                        _tl(_("%s... okay. Just pull my hair when I say it.")) % _tr(_pn_pick),
                    ])
                elif girl.has_trait("cute_sex"):
                    _accept_line = renpy.random.choice([
                        _tl(_("%s...? That's a little intense... but if it makes you happy, %s.")) % (_tr(_pn_pick), _tr(_pn_pick)),
                        _tl(_("O-okay... %s. Is that right? Did I say it okay...?")) % _tr(_pn_pick),
                    ])
                else:
                    _accept_line = renpy.random.choice([
                        _tl(_("%s? Really? ...Okay. I can do that, %s.")) % (_tr(_pn_pick), _tr(_pn_pick)),
                        _tl(_("Alright... %s it is. Don't let it go to your head.")) % _tr(_pn_pick),
                    ])
            else:
                _accept_line = renpy.random.choice([
                    _tl(_("%s? That's cute. Sure, %s.")) % (_tr(_pn_pick), _tr(_pn_pick)),
                    _tl(_("I like it. %s. Yeah, that works.")) % _tr(_pn_pick),
                    _tl(_("You want me to call you %s? ...Okay. I can do that, %s.")) % (_tr(_pn_pick), _tr(_pn_pick)),
                ])
        $ Say_Line(girl, _accept_line)
        $ girl.petname_for_player = _pn_pick
        $ girl.petname_for_player_auto = False
        $ girl.discover("discovered_petname_for_player")
        $ Change_Status(girl, "Inbt", 3)
        $ debug_log("[DEBUG] Player petname set: %s calls player %s" % (girl.gid, _pn_pick))
    else:
        python:
            _pn_fd = _petname_story_refusal(girl, _pn_check) or _petname_femdom_line(girl, _pn_pick, _pn_cfg, "him", "no")
            if _pn_fd:
                # Master / Daddy to a femdom: she refuses with an order (docs/plan_femdom.md 7)
                set_scene_expression(girl, _pn_fd[0])
                _reject_line = _pn_fd[1]
            elif _pn_pick in ("Master", "Daddy", "Sir"):
                _reject_line = renpy.random.choice([
                    _tl(_("Call you %s? ...No. I'm not calling you that.")) % _tr(_pn_pick),
                    _tl(_("%s? We're not there yet. Maybe try something less... intense.")) % _tr(_pn_pick),
                ])
            else:
                _reject_line = renpy.random.choice([
                    _tl(_("Hmm... %s doesn't feel right. Maybe something else?")) % _tr(_pn_pick),
                    _tl(_("I don't know... %s? Not really feeling it.")) % _tr(_pn_pick),
                ])
        $ Say_Line(girl, _reject_line)

    $ store._pn_sub_result = "done"
    return

# ============================================================
# Petname Change Announcement (called during interactions)
# ============================================================
label petname_change_announcement(girl):
    python:
        _pending = getattr(girl, "_petname_pending_change", None)
        # a "default" name (Boy) an older save left pending: she just calls him that, no event
        if _pending is not None and PETNAMES_FOR_PLAYER.get(_pending, {}).get("default"):
            girl.petname_for_player = _pending
            girl.set_flag("discovered_petname_for_player")
            girl._petname_pending_change = None
            print("[PETNAME] %s: pending default name '%s' set without asking" % (girl.gid, _pending))
            _pending = None
    if _pending is None:
        return

    python:
        # a veteran femdom does not ask for Pet / Toy / Good boy, she tells him (docs/plan_femdom.md 7)
        _pending_cfg = PETNAMES_FOR_PLAYER.get(_pending, {})
        _pn_fd = _petname_femdom_line(girl, _pending, _pending_cfg, "him", "ask")
        if _pn_fd:
            set_scene_expression(girl, _pn_fd[0])
            _announce_line = _pn_fd[1]
        else:
            _announce_line = renpy.random.choice([
                _tr("Hey... I've been thinking. Can I call you %s from now on?") % _tr(_pending),
                _tr("You feel more like a %s to me now... is that okay?") % _tr(_pending),
                _tr("I want to start calling you %s. What do you think?") % _tr(_pending),
            ])
    $ Say_Line(girl, _announce_line)

    menu:
        "Sure, I like that":
            python:
                girl.petname_for_player = _pending
                girl._petname_pending_change = None
                girl._petname_last_ask_day = store.Day
                _pn_fd = _petname_femdom_line(girl, _pending, _pending_cfg, "him", "yes")
                if _pn_fd:
                    set_scene_expression(girl, _pn_fd[0])
                    _yes_line = _pn_fd[1]
                else:
                    _yes_line = renpy.random.choice([
                        _tl(_("Good. %s it is then.")) % _tr(_pending),
                        _tl(_("Yay! Okay, %s~")) % _tr(_pending),
                    ])
            $ Say_Line(girl, _yes_line)
            $ girl.discover("discovered_petname_for_player")
            $ Change_Status(girl, "Love", 3)

        "No, keep calling me what you were":
            python:
                if not hasattr(girl, "_petname_rejected"):
                    girl._petname_rejected = set()
                girl._petname_rejected.add(_pending)
                girl._petname_pending_change = None
                girl._petname_last_ask_day = store.Day
                _current = getattr(girl, "petname_for_player", None) or Player.Name
                print("[PETNAME] %s rejected '%s', won't ask again" % (girl.gid, _pending))
                # he refused HER request: a femdom girl gets angry, loses Obed and counts it toward the control
                # corruption (femdom_react_refused, docs/plan_femdom.md 4.3); anyone else takes it lightly
                _pn_angry = femdom_react_refused(girl, "petname")
                if not _pn_angry:
                    _no_line = renpy.random.choice([
                        _tl(_("Oh... okay. I'll stick with %s then.")) % _tr(_current),
                        _tl(_("Alright, %s it is. No problem.")) % _tr(_current),
                    ])
            if not _pn_angry:
                $ Say_Line(girl, _no_line)

    return
