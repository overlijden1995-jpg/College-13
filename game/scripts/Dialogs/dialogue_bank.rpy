init python:
    import random as _random

    # =====================================================
    # DIALOGUE BANK HELPERS
    # =====================================================

    def rod_get_lines(girl, key):
        """
        Returns the list of lines for (girl, key) or Global fallback, or None.
        """
        gid = getattr(girl, "gid", None) or getattr(girl, "Id", None) if girl else None

        # Try girl-specific block first
        if gid and gid in rod_lines:
            girl_block = rod_lines[gid]
            if key in girl_block:
                return girl_block[key]

        # Then the block of her role (a stepmom: rod_lines["role:stepmom"]), then Global
        _role_block = rod_lines.get(girl_role_key(girl)) if girl else None
        if _role_block and key in _role_block:
            return _role_block[key]

        # Fallback to Global block
        if "Global" in rod_lines and key in rod_lines["Global"]:
            return rod_lines["Global"][key]

        # No match found
        return None

    def rod_pick_line(girl, key, default="..."):
        """
        Picks a random line for (girl, key) using Global fallback.
        """
        lines = rod_get_lines(girl, key)
        if not lines:
            return default
        return _rod_finish_line(girl, lines)

    def _rod_finish_line(girl, lines):
        """One random line of the pool, translated, partner placeholders filled."""
        _line = renpy.random.choice(lines)
        _line = _tl(_line)
        # Format partner label placeholders if present
        if "%(" in _line and girl and hasattr(girl, "has_npc_partner") and girl.has_npc_partner():
            _line = fmt_safe(_line, partner_fmt(girl))
        return _line

    def rod_pick_line_by_id(girl_id, key, default="..."):
        """
        Picks a random line using a raw girl_id instead of a Girl object.
        """
        dummy = type("DummyGirl", (object,), {})()
        dummy.gid = girl_id
        return rod_pick_line(dummy, key, default=default)

    COMPLIMENT_OPTIONS = [
        # --- EASY (casual, always accepted, small gain) ---
        ("smile",         _("You have such a great smile."),              "safe"),

        ("laugh",         _("Your laugh is contagious, you know that?"), "safe"),

        ("hair_today",    _("Your hair looks amazing today."),            "safe"),

        ("outfit_style",  _("That outfit really suits you."),             "safe"),

        ("fragrance",     _("Oh, what's that fragrance? It suits you."),  "safe"),

        ("class",         _("Great job in class the other day."),         "safe"),

        ("class_grades",  _("Your grades have been really good lately."), "safe"),

        # --- MEDIUM (personal, needs some stats, decent gain) ---
        ("dr_skill",      _("You are a nice swimmer."),                   "safe"),

        ("gym_weights",   _("Those weights you lifted today were impressive."), "safe"),

        ("beauty_today",  _("You're looking extra beautiful today."),     "safe"),

        ("gorgeous",      _("Hey there, gorgeous."),                      "safe"),

        ("confidence",    _("I like how confident you are."),             "safe"),

        ("smart",         _("You're seriously one of the smartest people here."), "safe"),

        # --- HARD (bold, needs higher stats, big gain) ---
        ("eyes",          _("I'm sorry, I got lost in your eyes."),       "safe"),

        ("toned_body",    _("You're looking really toned lately."),       "safe"),

        ("so_into_you",   _("I'm so into you."),                          "safe"),

        # --- LEWD (uses lewd flirt system) ---
        ("tits",          _("You have some really nice tits."),           "lewd"),

        ("ass",           _("Your ass looks really great."),              "lewd"),

    ]

    # Per-compliment stat mapping: key -> (stat, gain_on_accept, loss_on_reject)
    # Easy = low gain/loss, Medium = moderate, Hard = high
    COMPLIMENT_STAT_MAP = {
        # --- EASY: always accepted (low T), small reward, small penalty ---
        "compliment_smile":        ("Love", 2, -1),
        "compliment_laugh":        ("Love", 2, -1),
        "compliment_hair_today":   ("Love", 2, -1),
        "compliment_outfit_style": ("Love", 2, -1),
        "compliment_fragrance":    ("Love", 2, -1),
        "compliment_class":        ("Inbt", 2, -1),
        "compliment_class_grades": ("Inbt", 2, -1),
        # --- MEDIUM: needs some affinity, decent reward ---
        "compliment_dr_skill":     ("Obed", 4, -2),
        "compliment_gym_weights":  ("Obed", 4, -2),
        "compliment_beauty_today": ("Love", 5, -3),
        "compliment_gorgeous":     ("Love", 5, -3),
        "compliment_confidence":   ("Love", 4, -3),
        "compliment_smart":        ("Inbt", 4, -2),
        # --- HARD: needs real stats, big reward but harsh rejection ---
        "compliment_eyes":         ("Love", 8, -5),
        "compliment_toned_body":   ("Obed", 7, -3),
        "compliment_so_into_you":  ("Love", 10, -6),
    }

    # ---------------------------------------------------------------- personality in the flirts
    # (docs/plan_personality_mechanics.md, approved 2026-09-19)
    # Her taste in compliments: action key -> (x gain when she accepts, x loss when she refuses). Above 1 = she loves
    # hearing it; below 1 = she distrusts it (also harder to accept: approval.rpy APPROVAL_ACTION_RULES["safe"][gid]).
    GIRL_COMPLIMENT_TASTE = {
        "gwen":  {"compliment_outfit_style": (2.0, 1.0), "compliment_hair_today": (1.5, 1.0),
                  "compliment_gorgeous": (0.5, 2.0), "compliment_beauty_today": (0.5, 2.0)},
        "rogue": {"compliment_eyes": (1.5, 1.0), "compliment_laugh": (1.5, 1.0), "compliment_smile": (1.5, 1.0),
                  "compliment_toned_body": (0.5, 1.5)},
        "ntw":   {"compliment_gym_weights": (1.5, 1.0), "compliment_confidence": (1.5, 1.0),
                  "compliment_toned_body": (1.5, 1.0), "compliment_smile": (0.0, 2.0)},
        "tenny": {"compliment_smart": (1.5, 1.0), "compliment_class": (1.5, 1.0), "compliment_class_grades": (1.5, 1.0)},
        # power, success and her looks; "cute" / "sweet" talk is for little girls
        "shion": {"compliment_confidence": (1.5, 1.0), "compliment_gorgeous": (1.5, 1.0), "compliment_outfit_style": (1.5, 1.0),
                  "compliment_smart": (1.2, 1.0), "compliment_smile": (0.5, 1.5), "compliment_laugh": (0.5, 1.5),
                  "compliment_so_into_you": (0.5, 1.5)},
    }
    # What she adds after her reaction: "loved" when she accepts one she loves, "disliked" to one she distrusts
    # (either answer). Always the first time for each compliment, then COMPLIMENT_TASTE_REPEAT of the times.
    COMPLIMENT_TASTE_REPEAT = 0.25
    COMPLIMENT_TASTE_LINES = {
        "gwen": {
            "loved": [
                ("smile", _("Finally, somebody who actually gets the look.")),
                ("smirk", _("Took you long enough to notice. I put a lot of effort into looking like I don't.")),
            ],
            "disliked": [
                ("annoyed", _("Save the lines for someone who hasn't heard them all.")),
                ("bemused", _("I've been sweet-talked by professionals. That wasn't it.")),
            ],
        },
        "rogue": {
            "loved": [
                ("shy", _("Well, ain't you sweet. Keep that up and I might start blushin' for real.")),
                ("smile", _("Sugar, a girl could get used to hearin' that.")),
            ],
            "disliked": [
                ("uncomfortable", _("Let's keep the talk above the neck for now, sugar.")),
                ("annoyed", _("I ain't a show horse, darlin'. Eyes up here.")),
            ],
        },
        "ntw": {
            "loved": [
                ("smirk", _("Finally, a compliment worth hearing.")),
                ("smirk", _("Yeah. I earned that one.")),
            ],
            "disliked": [
                ("annoyed", _("I don't do smiling. Don't make it a project.")),
                ("annoyed", _("Everyone wants me to smile more. Everyone is wrong.")),
            ],
        },
        "tenny": {
            "loved": [
                ("happy", _("Finally, someone who compliments the part of me I actually worked on.")),
                ("smirk", _("Correct. And statistically, you're the first one to say it this week.")),
            ],
        },
        "shion": {
            "loved": [
                ("smug", _("Of course. I didn't get where I am by being ordinary.")),
                ("smirk", _("Finally, you say something worth hearing. Keep practicing.")),
            ],
            "disliked": [
                ("annoyed", _("Cute? Sweet? Save that for the girls on your campus.")),
                ("serious", _("Don't talk to me like I'm one of your classmates.")),
            ],
        },
    }
    # Rogue is careful with touch: her touch flirts start harder (extra_T), the extra fades in a straight line with
    # every touch she accepts (gone after fade_after of them), and while it lasts each accepted touch means more.
    GIRL_TOUCH_WARMUP = {
        "rogue": {"actions": ("touch_cheek", "hold_hands", "hug", "kiss_cheek", "shoulder_massage"),
                  "extra_T": 150, "fade_after": 6, "love_bonus": 3},
    }
    # Her first accepted touch (once per game)
    TOUCH_WARMUP_LINES = {
        "rogue": [
            ("shy", _("It's been a long time since I let anybody do that.")),
            ("shy", _("Huh. That wasn't so hard. Don't tell anybody I said so.")),
        ],
    }

    def _persona_count(girl, key):
        """How many times she already showed this side of her; counts this one. girl.ActionLog only (never
        Recent_Actions, the anti-spam window of the flirts)."""
        _log = getattr(girl, "ActionLog", None)
        if _log is None:
            girl.ActionLog = _log = {}
        _n = _log.get(key, 0)
        _log[key] = _n + 1
        return _n

    def _touch_warmup(girl, action_key):
        """Rogue's touch warm-up for this flirt: {"extra_T", "left", "love_bonus"} or None (not her / not a touch)."""
        _w = GIRL_TOUCH_WARMUP.get(getattr(girl, "gid", None))
        if not _w or action_key not in _w["actions"]:
            return None
        _done = (getattr(girl, "ActionLog", None) or {}).get("persona_touch_accepted", 0)
        _left = max(0, _w["fade_after"] - _done)
        return {"extra_T": int(_w["extra_T"] * _left / float(_w["fade_after"])), "left": _left, "love_bonus": _w["love_bonus"]}

    def persona_flirt_aside(girl, action_key, reaction_mode):
        """(face, line) she adds after her reaction to a safe flirt, or None. action_key = "safe_<flirt>" (the key
        rod_flirt_say gets). Rogue's first accepted touch first; then a compliment she loves (accepted) or distrusts
        (either answer). The line is a _() marker: Say_Line translates it, a phone message needs _tl."""
        if not str(action_key).startswith("safe_"):
            return None
        _key = action_key[len("safe_"):]
        _gid = getattr(girl, "gid", None)
        _yes = str(reaction_mode).endswith("_yes")
        _w = GIRL_TOUCH_WARMUP.get(_gid)
        if (_w and _yes and _key in _w["actions"] and TOUCH_WARMUP_LINES.get(_gid)
                and (getattr(girl, "ActionLog", None) or {}).get("persona_touch_aside", 0) == 0):
            _persona_count(girl, "persona_touch_aside")
            print("[PERSONA] %s: first touch she accepted (%s)" % (_gid, _key))
            return renpy.random.choice(TOUCH_WARMUP_LINES[_gid])
        _taste = GIRL_COMPLIMENT_TASTE.get(_gid, {}).get(_key)
        if not _taste or _taste[0] == 1.0:
            return None
        _kind = "loved" if _taste[0] > 1.0 else "disliked"
        _pool = COMPLIMENT_TASTE_LINES.get(_gid, {}).get(_kind)
        if not _pool or (_kind == "loved" and not _yes):
            return None
        if _persona_count(girl, "persona_" + _key) > 0 and renpy.random.random() >= COMPLIMENT_TASTE_REPEAT:
            return None
        print("[PERSONA] %s: a compliment she %s (%s)" % (_gid, _kind, _key))
        return renpy.random.choice(_pool)

    def format_name_list(names):
        if len(names) == 0:
            return ""
        elif len(names) == 1:
            return names[0]
        _and = " %s " % _tl(_("and"))
        if len(names) == 2:
            return _and.join(names)
        else:
            return ", ".join(names[:-1]) + _and + names[-1]

    # =====================================================
    # FLIRT HELPERS
    # =====================================================

    def ensure_recent_actions(girl):
        """
        Make sure girl.Recent_Actions exists and is a list.
        """
        if not hasattr(girl, "Recent_Actions") or girl.Recent_Actions is None:
            girl.Recent_Actions = []
        return girl.Recent_Actions

    def add_recent_action(girl, action):
        """
        Append an action tag to girl's recent actions.
        """
        ra = ensure_recent_actions(girl)
        ra.append(action)

        # Keep only last 10 entries so it doesn't grow forever
        if len(ra) > 10:
            girl.Recent_Actions = ra[-10:]

    def register_slap(girl):
        """
        Called when the girl slaps the player.
        Increments slap counter and marks 'slapped' in recent actions.
        """
        if not hasattr(girl, "Slaps") or girl.Slaps is None:
            girl.Slaps = 0
        girl.Slaps += 1

        ra = ensure_recent_actions(girl)
        ra.append("slapped")
        if len(ra) > 10:
            girl.Recent_Actions = ra[-10:]

    def girl_is_annoyed_by_flirt(girl):
        """
        Generic check: if player has flirted a lot recently and
        her stats are not high enough, she can get annoyed instead
        of opening the flirt menu.
        """
        ra = ensure_recent_actions(girl)

        flirt_count = sum(1 for a in ra if a.startswith("flirt"))
        love = getattr(girl, "Love", 0)
        inbt = getattr(girl, "Inbt", 500)

        # Example logic:
        # - at least 2 flirts recorded recently
        # - low Love
        # - high inhibition
        obed = getattr(girl, "Obed", 0)
        if flirt_count >= 2 and love < 300 and obed < 200 and inbt > 400:
            return True
        return False

    # =====================================================
    # CORE RESOLUTION FOR SAFE FLIRT
    # =====================================================

    # =====================================================
    # BF LOYALTY EROSION — called when player does things with a taken girl
    # =====================================================

    def _erode_bf_loyalty(girl, category, action_key=None, is_first=False):
        """Reduce bf_loyalty when the player successfully interacts with a taken girl.
        category: 'safe_flirt', 'lewd_flirt', 'sex', 'gift'
        action_key: specific action (e.g. 'kiss', 'creampie', 'hj')
        is_first: True if this is a player_first (she hasn't done it with BF)
        Sexual acts do NOT erode loyalty — only romantic acts (kiss, dates) do.
        This creates the 'loves partner but sex with player' dynamic."""
        if not hasattr(girl, "has_npc_partner") or not girl.has_npc_partner():
            return
        if not hasattr(girl, "change_bf_loyalty"):
            return
        _ROMANTIC_ACTS = {"kiss", "steal_kiss", "kiss_cheek", "hold_hands", "hug"}
        if category == "sex" and str(action_key) not in _ROMANTIC_ACTS:
            return

        _EROSION = {
            "safe_flirt": -5,
            "lewd_flirt": -12,
            "sex": -20,
            "gift": -8,
        }
        base = _EROSION.get(category, -5)

        # Heavier erosion for more intimate acts
        _ACT_BONUS = {
            "kiss": -5, "steal_kiss": -8,
            "hj": -5, "bj": -10, "tj": -8,
            "sex": -15, "cowgirl": -15, "reverse_cowgirl": -15,
            "creampie": -25, "anal": -20,
            "masturbate": -8, "oral": -10,
        }
        act_extra = _ACT_BONUS.get(str(action_key), 0)

        # First-time bonus: doing something her BF never did
        first_mult = 1.5 if is_first else 1.0

        # Trait-aligned firsts hit even harder
        if is_first and action_key:
            if action_key == "creampie" and girl.has_trait("cum_slut"):
                first_mult = 2.5
            elif action_key in ("sex", "cowgirl", "reverse_cowgirl") and girl.has_trait("hardcore_sex"):
                first_mult = 2.0
            elif action_key in ("sex", "cowgirl", "reverse_cowgirl") and girl.has_trait("cute_sex"):
                first_mult = 2.0
            elif action_key in ("sex", "cowgirl", "reverse_cowgirl") and girl.has_trait("virgin"):
                first_mult = 3.0
            elif action_key == "anal" and girl.has_trait("anal_lover"):
                first_mult = 2.5
            elif action_key == "anal" and girl.has_trait("anal_hater"):
                first_mult = 1.5

        total = int((base + act_extra) * first_mult)
        girl.change_bf_loyalty(total)

    def do_safe_flirt(girl, action_key):
        """
        Resolve a 'safe' flirt through ApprovalCheck.
        Returns:
            "ok"      -> she accepts or is shy but positive
            "reject"  -> she pulls back / awkward
        Also adjusts some stats via Change_Status.
        """
        # Her step locks every talk flirt, the joke too (story_steps.rpy): she cuts it whatever her stats.
        # Checked FIRST because the joke path below never reaches the ApprovalCheck override.
        _story_lock = story_lock_result(girl, action_key)
        if _story_lock:
            store._flirt_partner_pending = None
            setattr(girl, "LastSafeFlirtDecision", _story_lock)
            setattr(girl, "LastApprovalResult", _story_lock)
            add_recent_action(girl, "flirt_safe_reject_" + action_key)
            return "reject"

        # Jokes bypass ApprovalCheck... 75% funny, 25% bad joke (and her partner doesn't mind one)
        if action_key == "joke":
            store._flirt_partner_pending = None
            _joke_stats = ["Love", "Obed", "Inbt"]
            if renpy.random.random() < 0.75:
                # Good joke... gain +1-3 in a random stat
                # a stat NAME, never translated: _tl(_("Love")) is the pet name "Amor" in PT / ES and changed nothing
                _stat = renpy.random.choice(_joke_stats)
                _amt = renpy.random.randint(1, 3)
                Change_Status(girl, _stat, _amt)
                add_recent_action(girl, "flirt_safe_ok_joke")

                # Fake a minimal result so reaction_mode logic still works
                setattr(girl, "LastSafeFlirtDecision", {"accepted": True, "outcome": "soft_allow"})
                setattr(girl, "LastApprovalResult", {"accepted": True, "outcome": "soft_allow", "reason_primary": "love"})
                return "ok"
            else:
                # Bad joke... lose -1-3 in a random stat
                _stat = renpy.random.choice(_joke_stats)
                _amt = renpy.random.randint(1, 3)
                Change_Status(girl, _stat, -_amt)
                add_recent_action(girl, "flirt_safe_reject_joke")

                setattr(girl, "LastSafeFlirtDecision", {"accepted": False, "outcome": "soft_deny"})
                setattr(girl, "LastApprovalResult", {"accepted": False, "outcome": "soft_deny", "reason_primary": "love"})
                return "reject"

        cfg = ApprovalRuleFor(girl=girl, action=action_key, category="safe")
        store._massage_partner_present = False

        # Her partner on scene: she holds back (FLIRT_PARTNER_WATCH)
        _pp_penalty = flirt_partner_penalty(girl, action_key)
        cfg["Bonus"] = cfg.get("Bonus", 0) + _pp_penalty

        # Personality: Rogue's touch warm-up (GIRL_TOUCH_WARMUP): her touch flirts start harder
        _warm = _touch_warmup(girl, action_key)
        if _warm and _warm["extra_T"]:
            cfg["T"] += _warm["extra_T"]

        # Lesbian kiss gate: requires Love>=850 AND Obed>=500
        if girl.has_trait("lesbian") and action_key in ("kiss_cheek", "steal_kiss"):
            if getattr(girl, "Love", 0) < 850 or getattr(girl, "Obed", 0) < 500:
                _deny = {"accepted": False, "outcome": "hard_deny", "score": 0, "tier": 0,
                         "reason_primary": "lesbian", "reason_secondary": None,
                         "reasons": ["lesbian"], "is_cheating": False, "cheating_state": None,
                         "debug": {"lesbian_kiss_blocked": True}}
                setattr(girl, "LastSafeFlirtDecision", _deny)
                setattr(girl, "LastApprovalResult", _deny)
                add_recent_action(girl, "flirt_safe_reject_" + action_key)
                flirt_partner_note(girl, action_key, _deny)
                return "reject"

        result = ApprovalCheck(
            girl=girl,
            T=cfg["T"],
            Type=cfg["Type"],
            Spread=cfg["Spread"],
            Bonus=cfg["Bonus"],
            Variation=cfg["Variation"],
            Check=False,
            ReturnData=True,
            Action=action_key,
            Location=getattr(girl, "loc", None),
        )
        # her step locks this flirt (story_steps.rpy): she cuts it whatever her stats
        _story_lock = story_lock_result(girl, action_key)
        if _story_lock:
            result = _story_lock
            setattr(girl, "LastApprovalResult", result)
        flirt_partner_note(girl, action_key, result, spread=cfg["Spread"])

        # The massage opens with "my partner is right there, behave" when she agreed with him watching
        if action_key == "shoulder_massage" and _pp_penalty and result.get("accepted", False):
            store._massage_partner_present = True
            debug_log("[MASSAGE] %s agreed with her partner on scene (penalty %d)" % (girl.gid, _pp_penalty))

        # Keep last decision easy to consume in dialogue.
        setattr(girl, "LastSafeFlirtDecision", result)

        # Check if this action has a per-compliment stat mapping
        _cmap = COMPLIMENT_STAT_MAP.get(action_key, None)
        _ctaste = GIRL_COMPLIMENT_TASTE.get(getattr(girl, "gid", None), {}).get(action_key, (1.0, 1.0))

        if not result.get("accepted", False):
            if _cmap:
                # Compliment rejected... use per-compliment penalty (x her taste: one she distrusts stings more)
                _stat, _gain, _loss = _cmap
                Change_Status(girl, _stat, int(round(_loss * _ctaste[1])))
            else:
                # Generic safe flirt rejection — bold move still earns some Obed
                Change_Status(girl, "Love", -5)
                Change_Status(girl, "Obed", +2)
            add_recent_action(girl, "flirt_safe_reject_" + action_key)
            _notify_cheat_heat(girl, "steal_kiss" if action_key == "steal_kiss" else "flirt", False)
            return "reject"
        else:
            if _cmap:
                # Compliment accepted... use per-compliment reward (x her taste)
                _stat, _gain, _loss = _cmap
                Change_Status(girl, _stat, int(round(_gain * _ctaste[0])))
            else:
                # Generic safe flirt acceptance
                Change_Status(girl, "Love", 5)
                Change_Status(girl, "Lust", 5, max_val=100)

            # Rogue's touch warm-up: every touch she accepts makes the next one easier, and means more while it lasts
            if _warm:
                _persona_count(girl, "persona_touch_accepted")
                if _warm["left"] > 0:
                    Change_Status(girl, "Love", _warm["love_bonus"])
                print("[PERSONA] %s touch warm-up: %s accepted (extra T was %d, %d to go)" % (girl.gid, action_key, _warm["extra_T"], max(0, _warm["left"] - 1)))

            # Physical flirts provoke temptation (not jokes/compliments)
            if action_key in ("touch_cheek", "hold_hands", "kiss_cheek", "hug", "shoulder_massage", "steal_kiss"):
                provoke(girl, 1)

            # BF loyalty erosion on accepted safe flirt
            _erode_bf_loyalty(girl, "safe_flirt", action_key)

            add_recent_action(girl, "flirt_safe_ok_" + action_key)
            _notify_cheat_heat(girl, "steal_kiss" if action_key == "steal_kiss" else "flirt", True)
            return "ok"

    # =====================================================
    # FLIRTING IN FRONT OF HER PARTNER
    # =====================================================
    # Every flirt (and a kiss asked in the sex menu) while her NPC partner is on scene with her: she holds
    # back (penalty on her approval), then label _flirt_partner_witness (Flirty.rpy) rolls whether he SEES
    # it. Never over the phone, never when his NTR is active and she knows (a consenting audience). A flirt
    # with no row here (a joke, the sunscreen favor) leaves him out of it.
    #   penalty  approval Bonus while he is right there
    #   susp     suspicion when he sees it (x FLIRT_PARTNER_REFUSED_SUSP when she pushed you away: he still saw
    #            you try). At 100 he is sure and confronts her on the spot (npc_suspicion_confrontation)
    #   notice   chance he sees it, x FLIRT_PARTNER_NOTICE_MULT (she went along / a room / he stands far off)
    #   sees     optional: his reaction pool when he sees her go along with it and is not sure yet (below 100)
    FLIRT_PARTNER_WATCH = {
        "compliment":       {"penalty": -60,  "susp": 3,   "notice": 0.25},   # every safe compliment_*
        "touch_cheek":      {"penalty": -120, "susp": 5,   "notice": 0.40},
        "hold_hands":       {"penalty": -150, "susp": 6,   "notice": 0.45},
        "hug":              {"penalty": -150, "susp": 6,   "notice": 0.45},
        "kiss_cheek":       {"penalty": -180, "susp": 10,  "notice": 0.55},
        "shoulder_massage": {"penalty": -200, "susp": 8,   "notice": 0.50},
        # a kiss: he thinks he saw something, he is not sure until his suspicion reaches 100 (author, 2026-09-19)
        "steal_kiss":       {"penalty": -250, "susp": 50,  "notice": 0.80, "sees": "unsure"},
        "kiss":             {"penalty": 0,    "susp": 50,  "notice": 0.80, "sees": "unsure"},   # sex menu: its own approval
        "compliment_lewd":  {"penalty": -200, "susp": 6,   "notice": 0.30},   # every lewd compliment_*
        "ask_panties":      {"penalty": -200, "susp": 10,  "notice": 0.30},
        "pinch_ass":        {"penalty": -200, "susp": 6,   "notice": 0.30},
        "touch_thighs":     {"penalty": -200, "susp": 6,   "notice": 0.30},
        "slap_ass":         {"penalty": -200, "susp": 8,   "notice": 0.50},   # loud
        "grab_ass":         {"penalty": -200, "susp": 10,  "notice": 0.40},
        "grab_tits":        {"penalty": -200, "susp": 12,  "notice": 0.45},
        "touch_tits":       {"penalty": -200, "susp": 12,  "notice": 0.45},
        "touch_pussy":      {"penalty": -200, "susp": 20,  "notice": 0.55},
    }
    FLIRT_PARTNER_NOTICE_MULT = {"accepted": 1.5, "room": 1.5, "far": 0.5}
    FLIRT_PARTNER_NOTICE_MAX = 0.95
    FLIRT_PARTNER_REFUSED_SUSP = 0.34
    # What seeing it costs him, per point of suspicion gained (floor): he dislikes the guy hitting on his
    # girlfriend, and loves her a little less only when she went along with it
    FLIRT_PARTNER_FALLOUT = {"friendship_with_player": (-1, -100), "love_for_girl": (-1, -50)}
    FLIRT_PARTNER_NEAR_MISS = 0.40   # he did NOT see it: chance of a "he almost did" beat (rows with notice >= 0.40)

    # He saw it: narration, then his line. Tier = his suspicion AFTER it (low < 30, medium <= 60, high),
    # "refused" = she pushed you away (he is mad at YOU), "ntr" = a partner with the ntr trait (or an NTR she
    # does not know about yet) who watches a beat too long, "unsure" = a row's "sees" (a kiss he is not sure he
    # saw; his lines are the "confused" ones of a caught kiss, _NPC_WITNESS_LINES). %(name)s %(pp)s %(Pp)s
    # %(poss)s = him / her (_format_npc_line), %(girl_name)s, %(pl)s = "girlfriend". The three %s glares are the
    # old lewd-flirt ones.
    _FLIRT_PARTNER_GLARES = [
        _("You catch %s watching you with a look that could kill."),
        _("You notice %s glaring in your direction."),
        _("%s narrows their eyes at you from across the room."),
    ]
    FLIRT_PARTNER_SEES = {
        "low": [
            _("%(name)s looks up from %(poss)s phone and frowns."),
            _("%(name)s stops mid-sentence and looks your way."),
        ],
        "medium": _FLIRT_PARTNER_GLARES,
        "high": _FLIRT_PARTNER_GLARES,
        "refused": _FLIRT_PARTNER_GLARES,
        "ntr": [
            _("%(name)s is watching. %(Pp)s doesn't look away."),
            _("%(name)s saw it. %(Pp)s swallows hard and says nothing for a second."),
        ],
        "ntr_boundary": [
            _("%(name)s watches openly. %(Pp)s doesn't even try to look away anymore."),
            _("%(name)s just stands there, hands in %(poss)s pockets, watching you two."),
            _("%(name)s's expression hardens, but %(pp)s doesn't say a word."),
        ],
        "unsure": [
            _("%(name)s looks over just as you two pull apart."),
            _("%(name)s catches the end of it and frowns, not quite sure what %(pp)s just saw."),
        ],
    }
    FLIRT_PARTNER_LINES = {
        "low": [
            _("Uh... what was that?"),
            _("%(girl_name)s? Everything okay over there?"),
            _("Hey. What's going on here?"),
        ],
        "medium": [
            _("Dude. That's my %(pl)s."),
            _("You two seem awfully close."),
            _("%(girl_name)s, we're talking about this later."),
        ],
        "high": [
            _("Keep it up and we're going to have a problem."),
            _("I'm not blind, you know. I see what's going on."),
            _("Last warning. Stay away from my %(pl)s."),
        ],
        "refused": [
            _("She said no, man. Back off."),
            _("Is this guy bothering you, %(girl_name)s?"),
            _("Hey. Leave her alone."),
        ],
        "ntr": [
            _("...Huh. I didn't see that. I definitely didn't see that."),
            _("%(girl_name)s? You look... flushed."),
            _("I should probably say something about that. Right?"),
        ],
        "ntr_boundary": [
            _("Go ahead. Don't mind me."),
            _("What am I even supposed to say at this point?"),
            _("You know I'm right here. But sure. Whatever."),
            _("I'll just... stand here, I guess."),
        ],
        "unsure": _NPC_WITNESS_LINES[("confused", "mild")],
    }
    FLIRT_PARTNER_MISSES = [
        _("%(name)s glances over a second too late."),
        _("%(name)s is busy with %(poss)s phone and misses it."),
        _("%(name)s turns your way just as you pull back."),
    ]

    def flirt_partner_watching(girl):
        """Her NPC partner when he is on scene with her and would mind a flirt, else None."""
        if getattr(store, "_phone_mode", False):
            return None
        _present, _name, _ctx = _is_partner_present(girl)
        if not _present or _ctx != "same_location":
            return None
        _npc = get_npc_partner_for(girl)
        if _npc is None:
            return None
        return _npc

    def _flirt_partner_row(action_key, lewd=False):
        _row = FLIRT_PARTNER_WATCH.get(action_key)
        if _row is None and str(action_key).startswith("compliment_"):
            _row = FLIRT_PARTNER_WATCH["compliment_lewd" if lewd else "compliment"]
        return _row

    def flirt_partner_penalty(girl, action_key, lewd=False):
        """Approval Bonus for this flirt while her partner watches (0 when he doesn't): her NPC partner on
        scene, or her girlfriend watching a sex-menu session as a witness (the massage). Every flirt starts
        here, so it also drops the last flirt's queued notice."""
        store._flirt_partner_pending = None
        _row = _flirt_partner_row(action_key, lewd)
        if _row is None or getattr(store, "_phone_mode", False):
            return 0
        if flirt_partner_watching(girl) is None and _is_partner_present(girl)[2] != "watching":
            return 0
        if _ntr_active_discovered(girl):
            return 0   # NTR active and she knows: he lets it happen, no approval penalty
        return _row["penalty"]

    def flirt_partner_note(girl, action_key, decision, lewd=False, spread=None):
        """After the approval: queue the flirt for _flirt_partner_witness. decision = the ApprovalCheck dict
        (or {"accepted": bool}); blocked = she said no ONLY because he is here (the margin his penalty took)."""
        _row = _flirt_partner_row(action_key, lewd)
        if _row is None or flirt_partner_watching(girl) is None:
            store._flirt_partner_pending = None
            return
        _accepted = bool(decision.get("accepted", False))
        _blocked = False
        if not _accepted and _row["penalty"] and spread is not None and decision.get("outcome") != "angry_deny":
            _dbg = decision.get("debug", {}) or {}
            _back = -_row["penalty"] * _dbg.get("context_mult", 1.0) * _dbg.get("trait_mult", 1.0)
            _blocked = _dbg.get("margin", -99999) + _back >= int(spread * 0.30)
        store._flirt_partner_pending = {"gid": girl.gid, "action": action_key, "lewd": lewd,
                                        "accepted": _accepted, "blocked": _blocked}
        print("[FLIRT_PARTNER] %s %s with her partner on scene: accepted=%s blocked_by_him=%s" % (
            girl.gid, action_key, _accepted, _blocked))

    def _flirt_partner_fmt(npc, girl, line):
        # the old glares take his name as %s; the rest goes through _format_npc_line
        if "%s" in line and "%(" not in line:
            return _tl_fmt(line, npc.Name)
        return _format_npc_line(npc, line, girl)

    def flirt_partner_take(girl):
        """Resolve the queued flirt for label _flirt_partner_witness and apply what he takes from it.
        None = nothing to show; else {npc, accepted, blocked_line, seen, narration, line, near_miss}."""
        _p = getattr(store, "_flirt_partner_pending", None)
        store._flirt_partner_pending = None
        if not _p or _p.get("gid") != girl.gid:
            return None
        _npc = flirt_partner_watching(girl)
        _row = _flirt_partner_row(_p["action"], _p.get("lewd", False))
        if _npc is None or _row is None:
            return None
        _accepted = _p["accepted"]
        _out = {"npc": _npc, "accepted": _accepted, "blocked_line": None, "seen": False,
                "narration": None, "line": None, "near_miss": None, "ntr_boundary": False}

        # NTR active and she knows: he won't confront, but he's still watching (no stat change either way)
        if _ntr_active_discovered(girl):
            _out["ntr_boundary"] = True
            if not _accepted:
                # she pushed you away herself: "Go ahead. Don't mind me." would contradict the scene
                print("[FLIRT_PARTNER] %s NTR-boundary: %s refused %s, he stays out of it" % (
                    _npc.name, girl.gid, _p["action"]))
                return _out
            _out["seen"] = True
            _out["narration"] = _flirt_partner_fmt(_npc, girl, renpy.random.choice(FLIRT_PARTNER_SEES["ntr_boundary"]))
            _out["line"] = _flirt_partner_fmt(_npc, girl, renpy.random.choice(FLIRT_PARTNER_LINES["ntr_boundary"]))
            print("[FLIRT_PARTNER] %s NTR-boundary: saw %s's %s, passive reaction, no stat change" % (
                _npc.name, girl.gid, _p["action"]))
            return _out

        # She said no only because he is standing right there: she says so (the sex-menu "partner here" pool)
        if _p.get("blocked"):
            _key = "same_location_lesbian" if girl.has_trait("lesbian") else "same_location"
            _raw = _tl(renpy.random.choice(_PARTNER_PRESENT_DENY[_key])).replace("%(partner)s", _npc.Name)
            _out["blocked_line"] = _format_partner_line(girl, _raw)

        _m = FLIRT_PARTNER_NOTICE_MULT
        _chance = _row["notice"]
        if _accepted:
            _chance *= _m["accepted"]
        if _is_room_location():
            _chance *= _m["room"]
        if roster_is_far(_npc):
            _chance *= _m["far"]
        _chance = min(FLIRT_PARTNER_NOTICE_MAX, _chance)
        _roll = renpy.random.random()
        if _roll >= _chance:
            if _accepted and _p["action"] in ("kiss", "steal_kiss"):
                unlock_achievement("close_call")
            if _row["notice"] >= FLIRT_PARTNER_NEAR_MISS and renpy.random.random() < FLIRT_PARTNER_NEAR_MISS:
                _out["near_miss"] = _flirt_partner_fmt(_npc, girl, renpy.random.choice(FLIRT_PARTNER_MISSES))
            print("[FLIRT_PARTNER] %s missed %s's %s (chance %.2f, roll %.2f)" % (_npc.name, girl.gid, _p["action"], _chance, _roll))
            return _out

        _gain = _row["susp"] if _accepted else max(1, int(round(_row["susp"] * FLIRT_PARTNER_REFUSED_SUSP)))
        Change_NPC_Status(_npc, "suspicion", _gain)
        for _stat, (_per, _floor) in FLIRT_PARTNER_FALLOUT.items():
            if _stat == "love_for_girl" and not _accepted:
                continue
            Change_NPC_Status(_npc, _stat, max(_floor, _per * _gain))
        if not _accepted:
            _tier = "refused"
        elif _npc.has_trait("ntr") or getattr(_npc, "_ntr_active", False):
            _tier = "ntr"
        elif _row.get("sees") and _npc.suspicion < 100:
            _tier = _row["sees"]
        else:
            _tier = _npc_suspicion_tier(_npc)
        _out["seen"] = True
        _out["narration"] = _flirt_partner_fmt(_npc, girl, renpy.random.choice(FLIRT_PARTNER_SEES[_tier]))
        _out["line"] = _flirt_partner_fmt(_npc, girl, renpy.random.choice(FLIRT_PARTNER_LINES[_tier]))
        print("[FLIRT_PARTNER] %s SAW %s's %s (chance %.2f, roll %.2f): tier=%s +%d suspicion (now %d) friendship=%d love=%d" % (
            _npc.name, girl.gid, _p["action"], _chance, _roll, _tier, _gain, _npc.suspicion,
            _npc.friendship_with_player, _npc.love_for_girl))
        return _out

    # =====================================================
    # FEMDOM: HIS HANDS ON HER (docs/plan_femdom.md section 7)
    # =====================================================
    # A lewd flirt that puts his hands on her (or demands her panties) is HIM taking control. A femdom girl holds
    # back: this approval Bonus x femdom_intensity (Gwen 1.0, Rogue 0.9, Tenny 1.2, NTW / Shion 1.5), added after
    # the partner penalty (the Flirty.rpy callers pass Bonus=0, so it cannot live in the lewd approval rules).
    # She answers in command either way (reaction modes "commanding_no" / "commanding_yes", femdom_flirt_mode):
    # her no never slaps him (no Punch, no register_slap), she catches his wrist and sets the rule; her yes is
    # her permission. A femdom girl never gains Obed from asserting herself: no Obed from any lewd flirt she
    # refuses, none from her yes in command. A lewd compliment is words, not his hands: no penalty, its usual
    # answer (a hard no still slaps), only the Obed rule.
    FEMDOM_FLIRT_PENALTY = {
        "ask_panties":      -40,    # words, but he is the one making demands
        "pinch_ass":        -50,
        "touch_thighs":     -50,
        "touch_tits":       -70,
        "grab_ass":         -80,
        "grab_tits":        -90,
        "slap_ass":        -100,    # he spanks her: the most "his" of them
        "touch_pussy":     -100,
        "sunscreen_thighs": -30,    # she asked for his hands on her back: going lower is his call, a smaller one
        "sunscreen_ass":    -40,
    }
    # Of those, the ones where his hand never touched her: no wrist to catch (FEMDOM_FLIRT_HOLD)
    FEMDOM_FLIRT_WORDS = frozenset(("ask_panties",))
    # Her no in command, by result (0 = hard, 1 = soft), x the flirt's diminishing returns. No Obed (the usual
    # refusal gives +5 / +3, a lesbian +10 / +8) and less Love lost than a slap (usual -20 / -5); Inbt as usual.
    FEMDOM_FLIRT_REFUSAL = {
        0: {"Love": -8, "Inbt": 20},
        1: {"Love": -2, "Inbt": 5},
    }
    # Her gesture before a no in command (face to face, his hand on her)
    FEMDOM_FLIRT_HOLD = [
        _("She catches your wrist before your hand gets any further."),
        _("She grabs your wrist and holds it there, eyes locked on yours."),
        _("She takes your wrist and moves your hand away. Slowly. On her terms."),
    ]

    def femdom_flirt_penalty(girl, action_key):
        """Approval Bonus of this lewd flirt for a femdom girl (FEMDOM_FLIRT_PENALTY x femdom_intensity), else 0."""
        _base = FEMDOM_FLIRT_PENALTY.get(action_key, 0)
        _int = femdom_intensity(girl) if _base else 0.0
        if not _int:
            return 0
        _pen = int(round(_base * _int))
        print("[FEMDOM] %s: lewd flirt %s is his hands taking control, approval Bonus %d (intensity %.1f)" % (
            girl.gid, action_key, _pen, _int))
        return _pen

    def femdom_flirt_mode(girl, approval_result, action_key):
        """"commanding_no" (result 0 / 1) or "commanding_yes" (2 / 3) when a femdom girl answers his hands in
        command; None when she is not femdom or the flirt is not in FEMDOM_FLIRT_PENALTY. "story_locked" when her
        story locks the flirt: her step's voice answers before any command (the first step is cold, no hold)."""
        _last = getattr(girl, "LastApprovalResult", None)
        if isinstance(_last, dict) and _last.get("outcome") == "story_locked":
            return "story_locked"
        if action_key not in FEMDOM_FLIRT_PENALTY or not femdom_intensity(girl):
            return None
        # a canon femdom far enough on her turn lets his hands be (FEMDOM_TURN_NO_HOLD_STAGE, femdom_turn.rpy)
        if femdom_stage(girl) >= FEMDOM_TURN_NO_HOLD_STAGE:
            return None
        return "commanding_no" if approval_result <= 1 else "commanding_yes"

    def flirt_lewd_slaps(result, reaction_mode):
        """She slaps him for this lewd flirt (Flirty.rpy: call Punch): a hard no, never a femdom no in command."""
        return result == 0 and reaction_mode != "commanding_no"

    def flirt_lewd_react(girl, action_key, approval_result, face, lines):
        """A lewd flirt with its own inline lines (the sunscreen): a femdom girl answers in command (her mode's
        pool through rod_flirt_say), anyone else says one of `lines` with `face`."""
        _mode = femdom_flirt_mode(girl, approval_result, action_key)
        if _mode and rod_flirt_line(girl, "lewd_" + action_key, _mode):
            rod_flirt_say(girl, "lewd_" + action_key, _mode)
            return
        set_scene_expression(girl, face)
        Say_Line(girl, _tl(renpy.random.choice(lines)))

    # =====================================================
    # CORE RESOLUTION FOR LEWD FLIRT (ApprovalCheck)
    # =====================================================

    def do_lewd_flirt_approval(
        girl,
        action_key,
        T=None,
        Type=None,
        Spread=None,
        Bonus=None,
        Variation=None
    ):
        """
        Wrapper around ApprovalCheck for lewd flirting.

        Uses ApprovalCheck and maps the result to:
            0 -> hard fail (slap)
            1 -> mild scold (no big anger)
            2 -> ok / accepts
            3 -> strongly approves / enjoys

        Also handles stat changes, slap counter and recent actions.
        Returns 0–3 (we collapse any 4 into 3).
        A femdom girl answers his hands in command (FEMDOM_FLIRT_PENALTY): her 0 / 1 never slaps him.
        """

        cfg = ApprovalRuleFor(girl=girl, action=action_key, category="lewd")
        t_val = cfg["T"] if T is None else T
        type_val = cfg["Type"] if Type is None else Type
        if hasattr(girl, "has_trait") and girl.has_trait("lesbian"):
            type_val = "OI"
        spread_val = cfg["Spread"] if Spread is None else Spread
        bonus_val = cfg["Bonus"] if Bonus is None else Bonus
        variation_val = cfg["Variation"] if Variation is None else Variation
        # Her partner on scene: she holds back (FLIRT_PARTNER_WATCH)
        bonus_val += flirt_partner_penalty(girl, action_key, lewd=True)
        # Femdom: his hands on her are him taking control (FEMDOM_FLIRT_PENALTY)
        bonus_val += femdom_flirt_penalty(girl, action_key)

        decision = ApprovalCheck(
            girl=girl,
            T=t_val,
            Type=type_val,
            Spread=spread_val,
            Bonus=bonus_val,
            Variation=variation_val,
            Check=False,
            ReturnData=True,
            Action=action_key,
            Location=getattr(girl, "loc", None),
        )
        # her step locks this flirt (story_steps.rpy): she cuts it whatever her stats (a scold, never a slap)
        _story_lock = story_lock_result(girl, action_key)
        if _story_lock:
            decision = _story_lock
            setattr(girl, "LastApprovalResult", decision)
        flirt_partner_note(girl, action_key, decision, lewd=True, spread=spread_val)

        # Map rich outcome to legacy 0..3 buckets.
        outcome = decision.get("outcome", "hard_deny")
        if outcome in ("angry_deny", "hard_deny"):
            result = 0
        elif outcome in ("soft_deny", "tempted_deny", "neutral", "story_locked"):
            result = 1
        elif outcome in ("tempted_allow", "soft_allow"):
            result = 2
        else:
            result = 3

        _les = hasattr(girl, "has_trait") and girl.has_trait("lesbian")
        # Femdom: never Obed from asserting herself; his hands get her answer in command (FEMDOM_FLIRT_PENALTY)
        _fd = hasattr(girl, "has_trait") and girl.has_trait("femdom")
        _fd_mode = femdom_flirt_mode(girl, result, action_key)
        if _fd_mode == "story_locked":
            _fd_mode = None         # her story said no, not her femdom: no command, nothing revealed
        if _fd_mode:
            girl.discover("discovered_trait_femdom")
            print("[FEMDOM] %s answers %s in command: %s (result %d, outcome %s)" % (
                girl.gid, action_key, _fd_mode, result, outcome))

        # Diminishing returns: stat gains decrease with repeated lewd flirts per time slot
        _cur_slot = (store.Day, store.TimeIndex)
        if getattr(girl, "_lewd_flirt_slot", None) != _cur_slot:
            girl._lewd_flirt_slot = _cur_slot
            girl._lewd_flirt_count = 0
        girl._lewd_flirt_count = getattr(girl, "_lewd_flirt_count", 0) + 1
        _lfc = girl._lewd_flirt_count
        if _lfc >= 4:
            _dr = 0.0
        elif _lfc == 3:
            _dr = 0.25
        elif _lfc == 2:
            _dr = 0.5
        else:
            _dr = 1.0

        if _lfc == 4:
            Narration(_("She doesn't seem as affected by your flirting anymore. Maybe you should try again later."))
        elif _lfc == 3:
            Narration(_("Your flirting doesn't seem to have as much effect as before."))

        if result <= 1 and _fd_mode:
            # Femdom no in command: she catches his wrist and sets the rule. No slap, no Obed (FEMDOM_FLIRT_REFUSAL)
            _fd_res = max(0, result)
            for _st, _amt in sorted(FEMDOM_FLIRT_REFUSAL[_fd_res].items()):
                Change_Status(girl, _st, int(_amt * _dr))
            add_recent_action(girl, "flirt_lewd_commanded_" + action_key)
            _notify_cheat_heat(girl, "lewd_flirt", False)
            print("[FEMDOM] %s: no slap, no Obed, %s x%.2f" % (girl.gid, FEMDOM_FLIRT_REFUSAL[_fd_res], _dr))
            return _fd_res

        if result <= 0:
            # Hard fail -> slap, but bold move earns Obed (never for a femdom girl: asserting herself)
            # his hand on her ass (slap_ass): a submissive forgives it, a femdom does not (trait_love_loss)
            Change_Status(girl, "Love", trait_love_loss(girl, int((-10 if _les else -20) * _dr)) if action_key == "slap_ass" else int((-10 if _les else -20) * _dr))
            if not _fd:
                Change_Status(girl, "Obed", int((+10 if _les else +5) * _dr))
            Change_Status(girl, "Inbt", int(+20 * _dr))
            register_slap(girl)
            add_recent_action(girl, "flirt_lewd_slap_" + action_key)
            _notify_cheat_heat(girl, "lewd_flirt", False)
            return 0

        if result == 1:
            # She scolds you but doesn't explode, still assertive (no Obed for a femdom girl)
            Change_Status(girl, "Love", trait_love_loss(girl, int((-2 if _les else -5) * _dr)) if action_key == "slap_ass" else int((-2 if _les else -5) * _dr))
            if not _fd:
                Change_Status(girl, "Obed", int((+8 if _les else +3) * _dr))
            Change_Status(girl, "Inbt", int((+8 if _les else +5) * _dr))
            add_recent_action(girl, "flirt_lewd_soft_reject_" + action_key)
            _notify_cheat_heat(girl, "lewd_flirt", False)
            return 1

        if result == 2:
            # Accepts, somewhat into it (a femdom yes in command gives no Obed)
            Change_Status(girl, "Love", int((+3 if _les else +10) * _dr))
            if not _fd_mode:
                Change_Status(girl, "Obed", int((+8 if _les else 0) * _dr))
            Change_Status(girl, "Lust", int(+10 * _dr), max_val=100)
            provoke(girl, 1)
            _erode_bf_loyalty(girl, "lewd_flirt", action_key)
            add_recent_action(girl, "flirt_lewd_ok_" + action_key)
            _notify_cheat_heat(girl, "lewd_flirt", True)
            return 2

        # result == 3
        Change_Status(girl, "Love", int((+5 if _les else +20) * _dr))
        if not _fd_mode:
            Change_Status(girl, "Obed", int((+10 if _les else 0) * _dr))
        Change_Status(girl, "Lust", int(+20 * _dr), max_val=100)
        provoke(girl, 1)
        _erode_bf_loyalty(girl, "lewd_flirt", action_key)
        add_recent_action(girl, "flirt_lewd_approve_" + action_key)
        _notify_cheat_heat(girl, "lewd_flirt", True)
        return 3

    # =====================================================
    # REACTION MODES
    # =====================================================

    def get_flirt_reaction_mode_safe(girl, base_result, action_key=""):
        """
        Map safe flirt result + stats into a reaction mode:
            "hard_no", "soft_no", "shy_yes",
            "normal_yes", "enthusiastic_yes", "obedient_yes"
        """
        decision = getattr(girl, "LastApprovalResult", None)
        if isinstance(decision, dict):
            outcome = decision.get("outcome", "")
            reason = decision.get("reason_primary", "")

            if outcome == "story_locked":
                return "story_locked"       # her step locks it (story_steps.rpy)
            if outcome in ("angry_deny", "hard_deny"):
                return "hard_no"
            if outcome in ("soft_deny", "tempted_deny", "neutral"):
                return "soft_no"
            if outcome == "tempted_allow":
                if reason == "lust":
                    return "enthusiastic_yes"
                return "shy_yes"
            if outcome == "soft_allow":
                if reason == "obed":
                    return "obedient_yes"
                return "normal_yes"
            if outcome == "hard_allow":
                return "enthusiastic_yes"

        love = getattr(girl, "Love", 0)
        obed = getattr(girl, "Obed", 0)
        lust = getattr(girl, "Lust", 0)
        inbt = getattr(girl, "Inbt", 500)

        if base_result == "reject":
            if love < 250 and lust < 250:
                return "hard_no"
            return "soft_no"

        # base_result == "ok"
        if inbt >= 650:
            return "shy_yes"

        if obed >= 700 and love < 400 and lust < 500:
            return "obedient_yes"

        if lust >= 650 and inbt <= 400:
            return "enthusiastic_yes"

        return "normal_yes"

    def get_flirt_reaction_mode_lewd(girl, approval_result, action_key=""):
        """
        Map lewd flirt ApprovalCheck result + stats into reaction mode.
        A femdom girl answers his hands in command first ("commanding_no" / "commanding_yes", femdom_flirt_mode).
        """
        _fd_mode = femdom_flirt_mode(girl, approval_result, action_key)
        if _fd_mode:
            return _fd_mode

        decision = getattr(girl, "LastApprovalResult", None)
        if isinstance(decision, dict):
            outcome = decision.get("outcome", "")
            reason = decision.get("reason_primary", "")

            if outcome == "story_locked":
                return "story_locked"       # her step locks it (story_steps.rpy)

            if outcome in ("angry_deny", "hard_deny"):
                return "hard_no"
            if outcome in ("soft_deny", "tempted_deny", "neutral"):
                return "soft_no"
            if outcome == "tempted_allow":
                if reason == "obed":
                    return "obedient_yes"
                return "shy_yes"
            if outcome == "soft_allow":
                if reason == "obed":
                    return "obedient_yes"
                return "normal_yes"
            if outcome == "hard_allow":
                return "enthusiastic_yes"

        love = getattr(girl, "Love", 0)
        obed = getattr(girl, "Obed", 0)
        lust = getattr(girl, "Lust", 0)
        inbt = getattr(girl, "Inbt", 500)

        if approval_result == 0:
            return "hard_no"

        if approval_result == 1:
            # Slight difference if she still likes you a bit
            if love > 400 or lust > 400:
                return "soft_no"
            return "hard_no"

        # For approvals (2 or 3)
        if inbt >= 700:
            return "shy_yes"

        if obed >= 700 and love < 400 and lust < 500:
            return "obedient_yes"

        if approval_result == 3 and lust >= 600 and inbt <= 400:
            return "enthusiastic_yes"

        if lust >= 650 and inbt <= 400:
            return "enthusiastic_yes"

        return "normal_yes"

    def rod_flirt_face_for_mode(reaction_mode, girl=None):
        """
        Default face per reaction mode.
        """
        if reaction_mode == "hard_no":
            return "angry"
        if reaction_mode == "soft_no":
            return "sad"
        if reaction_mode == "shy_yes":
            return "shy"          # "blush" is no expression preset: every shy yes showed a neutral face
        if reaction_mode == "enthusiastic_yes":
            return "smile"
        if reaction_mode == "obedient_yes":
            return "normal"
        if reaction_mode == "commanding_no":
            return "angry"        # femdom: stern, his wrist in her hand
        if reaction_mode == "commanding_yes":
            return "smile"        # femdom: her permission, on her terms
        if reaction_mode == "story_locked":
            if girl is not None and story_first_step(girl):
                return "angry"    # her first step is cold (story_steps.rpy): the ask offends her, no tease
            return "smug"         # her step locks it: not yet, and she knows he wants it
        return "smile"

    # The order her traits are tried in for a flirt line (after the cheating context). girl.traits is a set: without
    # this list the same flirt could pick a different trait's line from one launch to the next. A trait missing here
    # comes after these, alphabetically.
    _FLIRT_TRAIT_PRIORITY = ("virgin", "cheater", "loyal", "cum_slut", "hate_cum", "femdom", "submissive",
                             "hardcore_sex", "cute_sex", "public_fetish", "public_shy", "exhibitionist",
                             "camera_lover", "camera_hater")
    # Traits that only apply in public locations / while filmed
    _FLIRT_PUBLIC_ONLY_TRAITS = frozenset(("exhibitionist", "public_fetish", "public_shy"))
    _FLIRT_CAMERA_TRAITS = frozenset(("camera_hater", "camera_lover"))

    def rod_flirt_line(girl, action_key, reaction_mode):
        """The line for this flirt action + reaction mode (face to face AND phone), or None.
        The most specific pool with lines wins: her own "<key>.<modifier>" (her voice + the situation), her role's
        "<key>.<modifier>" (a stepmom's voice + the situation), the shared "<key>.<modifier>" (the situation: virgin,
        loyal to her partner...), her own "<key>", her role's "<key>", the shared "<key>".
        Modifiers: the cheating context first, then _FLIRT_TRAIT_PRIORITY."""
        full_key = "flirt_%s_%s" % (action_key, reaction_mode)

        loc = getattr(girl, "loc", None) or getattr(store, "CurrentLocation", "room")
        loc_is_public = _is_public_location(loc)
        _has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        _player_has_gf = (hasattr(girl, "is_dating_player") and not girl.is_dating_player()
                          and player_has_girlfriend(store.ALL_GIRLS)
                          and not is_player_harem_exempt(girl))

        _modifiers = []
        # her stage on the turn of a canon femdom comes first: her voice after it changes everything (femdom_turn.rpy)
        _stage_mod = femdom_stage_mod(girl) if hasattr(girl, "has_trait") else None
        if _stage_mod:
            _modifiers.append(_stage_mod)
        if _player_has_gf and _has_bf:
            _modifiers.append("both_cheating")
        elif _player_has_gf:
            _modifiers.append("player_cheating")
        girl_traits = set(getattr(girl, "traits", None) or [])
        _ordered = [t for t in _FLIRT_TRAIT_PRIORITY if t in girl_traits]
        _ordered += sorted(t for t in girl_traits if t not in _FLIRT_TRAIT_PRIORITY)
        for trait in _ordered:
            if trait in _FLIRT_PUBLIC_ONLY_TRAITS and not loc_is_public:
                continue
            if trait in _FLIRT_CAMERA_TRAITS and not loc_is_public and not getattr(store, "_recording_active", False):
                continue
            # cheater/loyal lines reference bf: only when she has one
            if trait in ("cheater", "loyal") and not _has_bf:
                continue
            # her discovery variants first; an eager trait she is still discovering has no veteran voice yet
            _modifiers.extend(trait_line_keys(girl, trait))

        gid = getattr(girl, "gid", None)
        _own = rod_lines.get(gid, {}) if gid else {}
        _role = rod_lines.get(girl_role_key(girl), {})
        _shared = rod_lines.get("Global", {})
        _mod_keys = ["%s.%s" % (full_key, mod) for mod in _modifiers]
        _base_keys = [full_key]
        if reaction_mode == "story_locked":
            # one pool per flirt her step locks (story_steps.rpy), most specific first, each key tried with its
            # "<key>.<modifier>" trait variants before the plain key. Her husband in the room has his own pools; the
            # SHARED husband pool ("behave, he's watching") is complicity, so it never speaks on her first step
            # (cold): nothing exists yet to hide, and the nerve itself is the offense
            _lock_keys = []
            if husband_in_room(girl):
                _lock_keys.append("flirt_story_locked_husband." + story_step_id(girl))
                if not story_first_step(girl):
                    _lock_keys.append("flirt_story_locked_husband")
            _lock_keys.append("flirt_story_locked." + story_step_id(girl))
            _lock_keys.append("flirt_story_locked")
            for _lk in _lock_keys:
                _base_keys.extend("%s.%s" % (_lk, _m) for _m in _modifiers)
                _base_keys.append(_lk)
        store._rod_flirt_matched = None
        for _block, _keys in ((_own, _mod_keys), (_role, _mod_keys), (_shared, _mod_keys),
                              (_own, _base_keys), (_role, _base_keys), (_shared, _base_keys)):
            for _k in _keys:
                if _block.get(_k):
                    # remember which modifier answered (a trait, a stage, a cheating context);
                    # rod_flirt_say / the phone discover from it AFTER the line is shown
                    _tail = _k.rsplit(".", 1)[1] if "." in _k else None
                    store._rod_flirt_matched = _tail if _tail in _modifiers else None
                    return _rod_finish_line(girl, _block[_k])
        if reaction_mode == "story_locked":
            return _rod_finish_line(girl, STORY_LOCKED_FALLBACK)
        return None

    _FLIRT_MOOD_ACCEPTS = frozenset(("shy_yes", "normal_yes", "enthusiastic_yes", "obedient_yes",
                                     "commanding_yes"))
    # traits a REFUSAL may still reveal: control (the refusal IS the voice) and identity statements
    _FLIRT_DISC_REFUSAL_OK = frozenset(("femdom", "submissive", "virgin", "loyal", "cheater",
                                        "lesbian", "bisexual", "married", "poor", "rich", "nerd",
                                        "gym_rat", "lightweight", "heavy_drinker"))

    def _rod_flirt_discover(girl, reaction_mode):
        """Discover the trait whose pool answered the flirt that was just SAID (store._rod_flirt_matched,
        set by rod_flirt_line). Accepted moods reveal the matched trait (enthusiasm/identity/control);
        refusal moods reveal only control and identity (a no never reveals a preference)."""
        _mod = getattr(store, "_rod_flirt_matched", None)
        store._rod_flirt_matched = None
        if not _mod or _mod in ("both_cheating", "player_cheating"):
            return
        _trait = _mod
        if _trait.endswith("_first"):
            _trait = _trait[:-6]
        elif _trait.endswith("_new"):
            _trait = _trait[:-4]
        if _trait in ("femdom_s2", "femdom_s3"):
            _trait = "femdom"
        if reaction_mode not in _FLIRT_MOOD_ACCEPTS and _trait not in _FLIRT_DISC_REFUSAL_OK:
            return
        if hasattr(girl, "has_trait") and girl.has_trait(_trait) and hasattr(girl, "discover"):
            girl.discover("discovered_trait_%s" % _trait)

    def rod_flirt_say(girl, action_key, reaction_mode):
        """
        Show a line for this flirt action + reaction mode, using rod_lines (rod_flirt_line picks it).
        action_key example: "safe_touch_cheek", "lewd_slap_ass", etc.
        reaction_mode example: "shy_yes", "hard_no", etc.
        """
        text = rod_flirt_line(girl, action_key, reaction_mode)
        face = rod_flirt_face_for_mode(reaction_mode, girl)

        if face:
            set_scene_expression(girl, face)

        # A femdom no in command starts with her hand on his wrist (not when he only asked: FEMDOM_FLIRT_WORDS)
        _base_key = action_key[len("lewd_"):] if str(action_key).startswith("lewd_") else None
        if (text and reaction_mode == "commanding_no" and _base_key in FEMDOM_FLIRT_PENALTY
                and _base_key not in FEMDOM_FLIRT_WORDS):
            Narration(renpy.random.choice(FEMDOM_FLIRT_HOLD))

        if text:
            if "%(" in text and hasattr(girl, "has_npc_partner") and girl.has_npc_partner():
                text = _format_partner_line(girl, text)
            Say_Line(girl, text)
            _rod_flirt_discover(girl, reaction_mode)

        if face:
            set_scene_expression(girl, "normal")

        # Her personality after the reaction: a compliment she loves / distrusts, Rogue's first accepted touch
        _aside = persona_flirt_aside(girl, action_key, reaction_mode)
        if _aside:
            set_scene_expression(girl, _aside[0])
            Say_Line(girl, _aside[1])
            set_scene_expression(girl, "normal")

    # =====================================================
    # DIALOGUE BANK (EXAMPLES)
    # =====================================================

    rod_lines = {
        "Global": {
            # She decides for her husband (family_wife_overrules): any wife of the house can speak these;
            # the stepmom role carries its own sharper pools (stepmom_flirt_lines.rpy)
            "family_errand_order": [
                _("Go on, honey. I need a few things from the store anyway. Take your time."),
                _("He's right, we're out of half of everything. Shoes on, dear."),
            ],
            "family_errand_alone": [
                _("There he goes. We have the place to ourselves for a bit."),
                _("Twenty minutes, give or take. Don't waste them standing there."),
            ],
            "family_dessert_order": [
                _("Actually... the ones from the stand ARE better. Go get them, honey. We'll wait."),
            ],
            "family_dessert_backs_him": [
                _("Nobody is going anywhere. The dessert on the table is fine."),
            ],
            # A "no_photos" girl's answer to his photo ask (girl_sends_photos / _photo_decide): a permanent
            # rule of hers, not a mood and not a step; the stepmom role carries its own pool
            "photo_never": [
                _("I don't send photos. That's a rule, and I don't break it."),
                _("No photos. Not now, not ever. Don't take it personally."),
            ],
            # A non-student's decline of the dorm drinking night (hangout_girl_accepts, students only;
            # author 2026-10-10): any teacher or woman of the house; the stepmom role has its own pool
            "hangout_not_student": [
                _("A night of drinking in a dorm room is not for me. Thanks anyway."),
                _("I'm going to pretend I never saw this invite. Have fun."),
            ],
            # A pregnant girl's decline of the drinking night (hangout_girl_accepts; author
            # 2026-10-11): only once she KNOWS it (_pregnancy_known, post discovery, so the
            # player knows too); she says why: no alcohol for her until the baby comes
            "hangout_pregnant": [
                _("A drinking night? You know I can't touch alcohol right now. Have fun for me!"),
                _("I'd love to, but no drinks for me until the baby comes. Next time, I promise!"),
                _("Tempting, but alcohol and this belly don't mix. Someone drink my share."),
            ],
            # Her first anal ever (_anal_first_story_beat, "anal_untouched" girls): line 1 then line 2
            "anal_her_first": [
                _("Wait... go slow. I have never done this. Ever."),
            ],
            "anal_her_first_2": [
                _("You're the first. Remember that, and be careful with me."),
            ],
            # An anal_lover's refusal of her still-locked act turns into a dangled promise
            # (story_locked_line's exception, author 2026-10-11); the stepmom role has its own pool
            "anal_locked_tease": [
                _("No... not yet. But keep trying. The day I finally say yes, you'll know you earned it."),
            ],
            # A married story girl declines turning the night into a sleepover while her husband is home
            # (sleepover_offer, plan_shion_agency F3): plain fact, no drama
            "sleepover_husband_home": [
                _("I can't stay the night. I have to be home before he wakes up."),
            ],
            # The scene ended with her on the edge and no release (scene_full_cleanup): warm begs, cold composes
            "edge_end_beg": [
                _("Wait. Wait, you can't just stop THERE. Please... just a little more."),
                _("No no no, I was RIGHT there... come back. Please?"),
            ],
            "edge_end_hide": [
                _("...I'm fine. Don't look at me like that. I said I'm fine."),
                _("That's... fine. We were done anyway. ...Stop smiling."),
            ],
            # His video against an act her story step has not opened (_blackmail_attempt): any story girl
            # refuses it flat, in her own register; the stepmom role has its sharper pool (author, 2026-10-09)
            "blackmail_story_locked": [
                _("A video? That's what you're holding over me? No. We're not there, and a threat won't move it."),
                _("Post it, don't post it. Some things you don't get this way. Not yet."),
                _("That's low, even for you. The answer is still no. Put it away."),
            ],

            # Example generic keys already in use
            "confess_love_accept": [
                _("Okay... I think I feel the same way."),
                _("You know what? I like you too."),
                _("Fine, you win. I really like you, happy now?")
            ],
            "confess_love_reject": [
                _("Sorry, I don't see you that way."),
                _("You are nice, but not like that."),
                _("Let's stay friends, okay?")
            ],

            # ------------------------------
            # SAFE FLIRT: TOUCH CHEEK
            # ------------------------------
            "flirt_safe_touch_cheek_shy_yes": [
                _("H-hey... warn me next time."),
                _("You can't just do that out of nowhere...")
            ],
            "flirt_safe_touch_cheek_normal_yes": [
                _("You are being surprisingly gentle today."),
                _("...I don't hate it.")
            ],
            "flirt_safe_touch_cheek_enthusiastic_yes": [
                _("Oh? Getting bold, aren't you?"),
                _("If you keep that up, I might start expecting it.")
            ],
            "flirt_safe_touch_cheek_soft_no": [
                _("Too fast. I'm not in the mood for that."),
                _("Not now, okay?")
            ],
            "flirt_safe_touch_cheek_hard_no": [
                _("Don't touch my face like that."),
                _("Seriously, back off.")
            ],

            # ------------------------------
            # SAFE FLIRT: HOLD HANDS
            # ------------------------------
            "flirt_safe_hold_hands_shy_yes": [
                _("Your hand is... kind of warm."),
                _("Just... don't squeeze too hard, okay?")
            ],
            "flirt_safe_hold_hands_normal_yes": [
                _("Your hands are warm."),
                _("Don't get used to this... maybe.")
            ],
            "flirt_safe_hold_hands_enthusiastic_yes": [
                _("Come on, if you're holding my hand, at least do it properly."),
                _("Feels nice, I'll admit.")
            ],
            "flirt_safe_hold_hands_soft_no": [
                _("Too fast. I'm not ready to hold hands like that."),
                _("Maybe another time.")
            ],
            "flirt_safe_hold_hands_hard_no": [
                _("Who said you could grab my hand?"),
                _("Let go.")
            ],

            # ------------------------------
            # SAFE FLIRT: JOKE
            # ------------------------------
            "flirt_safe_joke_shy_yes": [
                _("D-don't make me laugh like that, idiot."),
                _("That was actually kind of funny...")
            ],
            "flirt_safe_joke_normal_yes": [
                _("That was actually funny."),
                _("Careful, I might start expecting that level now.")
            ],
            "flirt_safe_joke_soft_no": [
                _("That joke was terrible."),
                _("Try again when you're funnier.")
            ],
            "flirt_safe_joke_hard_no": [
                _("Wow. That was not it."),
                _("Just stop before it gets worse.")
            ],

            # ------------------------------
            # SAFE FLIRT: KISS CHEEK
            # ------------------------------
            "flirt_safe_kiss_cheek_shy_yes": [
                _("H-hey! Give me a warning next time..."),
                _("My face is hot now, thanks.")
            ],
            "flirt_safe_kiss_cheek_normal_yes": [
                _("Bold, but I'll allow it."),
                _("Just don't do it in front of everyone.")
            ],
            "flirt_safe_kiss_cheek_enthusiastic_yes": [
                _("Oh, going for a cheek kiss now?"),
                _("If you start, you better keep that energy.")
            ],
            "flirt_safe_kiss_cheek_soft_no": [
                _("Ask before you do that."),
                _("You are getting ahead of yourself.")
            ],
            "flirt_safe_kiss_cheek_hard_no": [
                _("Hey! Don't just kiss me like that."),
                _("You really are shameless sometimes.")
            ],

                        # ---- CLASS / SCHOOL PERFORMANCE ----
            "flirt_safe_compliment_class_shy_yes": [
                _("You actually noticed that...?"),
                _("D-don't make a big deal out of it.")
            ],
            "flirt_safe_compliment_class_normal_yes": [
                _("Yeah, I did pretty well there."),
                _("Good to know someone was paying attention.")
            ],
            "flirt_safe_compliment_class_enthusiastic_yes": [
                _("Of course I nailed it."),
                _("You can count on me when it actually matters.")
            ],
            "flirt_safe_compliment_class_soft_no": [
                _("It wasn't that great, honestly."),
                _("I could have done a lot better than that.")
            ],
            "flirt_safe_compliment_class_hard_no": [
                _("Don't flatter me over something so basic."),
                _("If that impressed you, your standards are low.")
            ],
            "flirt_safe_compliment_class_obedient_yes": [
                _("If you say so, I'll take it."),
                _("Fine, I'll accept the compliment.")
            ],

            # ------------------------------
            # SAFE FLIRT: STEAL KISS
            # ------------------------------
            "flirt_safe_steal_kiss_shy_yes": [
                _("Y-you can't just steal a kiss like that..."),
                _("My heart is not ready for this.")
            ],
            "flirt_safe_steal_kiss_normal_yes": [
                _("You really went for it, huh?"),
                _("Next time I might steal one back.")
            ],
            "flirt_safe_steal_kiss_enthusiastic_yes": [
                _("Now that's the kind of confidence I like."),
                _("Just be ready if I decide to top that.")
            ],
            "flirt_safe_steal_kiss_soft_no": [
                _("Not like that. Don't steal something I'm not giving."),
                _("Slow down.")
            ],
            "flirt_safe_steal_kiss_hard_no": [
                _("Back off. I did not say you could do that."),
                _("Try that again and see what happens.")
            ],

            # ------------------------------
            # SAFE FLIRT: HUG
            # ------------------------------
            "flirt_safe_hug_shy_yes": [
                _("O-okay... just for a moment."),
                _("Don't read too much into this.")
            ],
            "flirt_safe_hug_normal_yes": [
                _("You're comfortable to hug, I'll give you that."),
                _("This is... kind of nice.")
            ],
            "flirt_safe_hug_enthusiastic_yes": [
                _("Come here. I could use this."),
                _("You better not let go first.")
            ],
            "flirt_safe_hug_soft_no": [
                _("Not now. I'm not in the mood for hugging."),
                _("Maybe later.")
            ],
            "flirt_safe_hug_hard_no": [
                _("Don't just grab me like that."),
                _("Ask before you wrap yourself around me.")
            ],

            # ------------------------------
            # SAFE FLIRT: SHOULDER MASSAGE
            # ------------------------------
            "flirt_safe_shoulder_massage_shy_yes": [
                _("O-okay... but don't get weird about it."),
                _("My shoulders are a bit tense anyway.")
            ],
            "flirt_safe_shoulder_massage_normal_yes": [
                _("Okay, that actually feels nice."),
                _("Don't stop until my stress disappears.")
            ],
            "flirt_safe_shoulder_massage_enthusiastic_yes": [
                _("If you're this good with your hands, I might keep you around."),
                _("You better not stop halfway.")
            ],
            "flirt_safe_shoulder_massage_soft_no": [
                _("Hands off. I'm not some stressed puppy to pet."),
                _("You are pushing your luck.")
            ],
            "flirt_safe_shoulder_massage_hard_no": [
                _("Don't touch me like that."),
                _("I didn't ask for your hands on me.")
            ],

            # ------------------------------
            # LEWD FLIRT: SLAP ASS
            # ------------------------------
            "flirt_lewd_slap_ass_shy_yes": [
                _("H-hey! D-don't do that so suddenly..."),
                _("If someone sees us, I'm blaming you.")
            ],
            "flirt_lewd_slap_ass_normal_yes": [
                _("You really like my ass, huh?"),
                _("Don't get carried away just because I let that slide.")
            ],
            "flirt_lewd_slap_ass_enthusiastic_yes": [
                _("Bold move."),
                _("If you're going to touch it, at least do it properly next time.")
            ],
            "flirt_lewd_slap_ass_soft_no": [
                _("Too sudden. Don't just slap me out of nowhere."),
                _("At least warn me first.")
            ],
            "flirt_lewd_slap_ass_hard_no": [
                _("The hell do you think you're doing?"),
                _("Try that again and I'll knock you out.")
            ],

            # ------------------------------
            # LEWD FLIRT: PINCH ASS
            # ------------------------------
            "flirt_lewd_pinch_ass_shy_yes": [
                _("S-seriously? You're really doing that here..."),
                _("You are impossible.")
            ],
            "flirt_lewd_pinch_ass_normal_yes": [
                _("You really have wandering hands."),
                _("I'll allow it... for now.")
            ],
            "flirt_lewd_pinch_ass_enthusiastic_yes": [
                _("If you're going to tease me, don't stop halfway."),
                _("You better be ready for payback.")
            ],
            "flirt_lewd_pinch_ass_soft_no": [
                _("Don't just pinch me like that."),
                _("You know you can just ask, right?")
            ],
            "flirt_lewd_pinch_ass_hard_no": [
                _("Hands off."),
                _("Do that again and see what happens.")
            ],

            # ------------------------------
            # LEWD FLIRT: GRAB TITS
            # ------------------------------
            "flirt_lewd_grab_tits_shy_yes": [
                _("Y-you're really going straight for that, huh..."),
                _("If I'm not yelling, it doesn't mean you can overdo it.")
            ],
            "flirt_lewd_grab_tits_normal_yes": [
                _("You really don't waste time, do you?"),
                _("If I'm letting you do this, you owe me something later.")
            ],
            "flirt_lewd_grab_tits_enthusiastic_yes": [
                _("You like them that much?"),
                _("Fine, enjoy it... for a bit.")
            ],
            "flirt_lewd_grab_tits_soft_no": [
                _("Slow down. We're not there yet."),
                _("You are getting way too handsy.")
            ],
            "flirt_lewd_grab_tits_hard_no": [
                _("My chest is not a public playground."),
                _("Touch me like that again and we're done.")
            ],

            # ------------------------------
            # LEWD FLIRT: GRAB ASS
            # ------------------------------
            "flirt_lewd_grab_ass_shy_yes": [
                _("H-hey... don't just grab me like that."),
                _("At least pretend to be subtle.")
            ],
            "flirt_lewd_grab_ass_normal_yes": [
                _("You really like testing boundaries."),
                _("Good thing I don't completely hate it.")
            ],
            "flirt_lewd_grab_ass_enthusiastic_yes": [
                _("If you're grabbing me like that, you better not run away later."),
                _("You started this, remember.")
            ],
            "flirt_lewd_grab_ass_soft_no": [
                _("You better slow down with that."),
                _("Not so rough.")
            ],
            "flirt_lewd_grab_ass_hard_no": [
                _("Try grabbing my ass again and see how long you stay standing."),
                _("Seriously, don't.")
            ],

            # ------------------------------
            # LEWD FLIRT: ASK PANTIES
            # ------------------------------
            "flirt_lewd_ask_panties_shy_yes": [
                _("Y-you can't just ask for that so casually..."),
                _("Maybe... someday. If you behave.")
            ],
            "flirt_lewd_ask_panties_normal_yes": [
                _("You want my panties? You're more shameless than I thought."),
                _("We'll see if you behave enough to deserve that.")
            ],
            "flirt_lewd_ask_panties_enthusiastic_yes": [
                _("Maybe one day I'll surprise you with that."),
                _("For now, keep fantasizing.")
            ],
            "flirt_lewd_ask_panties_soft_no": [
                _("You're way too shameless sometimes, you know that?"),
                _("Not happening. At least not today.")
            ],
            "flirt_lewd_ask_panties_hard_no": [
                _("Seriously? That's what you're asking for?"),
                _("Get your head out of the gutter.")
            ],

            # ------------------------------
            # LEWD FLIRT: TOUCH THIGHS
            # ------------------------------
            "flirt_lewd_touch_thighs_shy_yes": [
                _("H-hey... your hand is really warm."),
                _("I didn't say you could do that... but don't stop.")
            ],
            "flirt_lewd_touch_thighs_normal_yes": [
                _("You're getting bold with those hands."),
                _("Careful where those fingers wander.")
            ],
            "flirt_lewd_touch_thighs_enthusiastic_yes": [
                _("Mm, you really know how to get my attention."),
                _("Higher, if you're brave enough.")
            ],
            "flirt_lewd_touch_thighs_soft_no": [
                _("Keep your hands where I can see them."),
                _("Not here, not now.")
            ],
            "flirt_lewd_touch_thighs_hard_no": [
                _("Move that hand or lose it."),
                _("What exactly makes you think you can touch me?")
            ],

            # ------------------------------
            # LEWD FLIRT: TOUCH TITS
            # ------------------------------
            "flirt_lewd_touch_tits_shy_yes": [
                _("D-don't just grab there so suddenly..."),
                _("I... I'm not saying I hated it.")
            ],
            "flirt_lewd_touch_tits_normal_yes": [
                _("You've got nerve, I'll give you that."),
                _("At least you have good taste.")
            ],
            "flirt_lewd_touch_tits_enthusiastic_yes": [
                _("Go ahead, they're not going to bite."),
                _("Mm. You could do that again.")
            ],
            "flirt_lewd_touch_tits_soft_no": [
                _("Hands off. I'm not in the mood for that."),
                _("Maybe earn it first before you try that.")
            ],
            "flirt_lewd_touch_tits_hard_no": [
                _("Touch my chest again and you'll regret it."),
                _("Who do you think you are?")
            ],

            # ------------------------------
            # LEWD FLIRT: TOUCH PUSSY
            # ------------------------------
            "flirt_lewd_touch_pussy_shy_yes": [
                _("W-wait... not so suddenly..."),
                _("You can't just... I... okay, fine.")
            ],
            "flirt_lewd_touch_pussy_normal_yes": [
                _("You're really pushing your luck today."),
                _("Don't get too comfortable down there.")
            ],
            "flirt_lewd_touch_pussy_enthusiastic_yes": [
                _("Mm... you really went for it, didn't you?"),
                _("Bold. I like that in a guy.")
            ],
            "flirt_lewd_touch_pussy_soft_no": [
                _("That's way too far. Pull your hand back."),
                _("You don't just get to touch me there.")
            ],
            "flirt_lewd_touch_pussy_hard_no": [
                _("Are you insane? Get your hand away from me."),
                _("Try that again and I'm calling campus security.")
            ],

            # ------------------------------
            # LEWD FLIRT: FEMDOM IN COMMAND (FEMDOM_FLIRT_PENALTY, femdom_flirt_mode)
            # A femdom girl answers his hands in command: no = she catches his wrist and sets the rule (never a slap),
            # yes = her permission. True in her discovery phase too (no "as always"), and true whatever her
            # relationship (no promise of a later yes).
            # ------------------------------
            "flirt_lewd_slap_ass_commanding_no": [
                _("Did I say you could do that? No. Hands to yourself."),
                _("You don't spank me. If anyone gets spanked around here, it's you."),
                _("Cute. Now keep that hand still until I tell you otherwise."),
            ],
            "flirt_lewd_slap_ass_commanding_yes": [
                _("Fine. One. The next one happens when I say so."),
                _("Mm. I'll allow it. Don't mistake that for you being in charge."),
                _("Not bad. Next time, wait until I ask for it."),
            ],
            "flirt_lewd_pinch_ass_commanding_no": [
                _("No. You touch me when I decide, not when you feel like it."),
                _("Hands down. I didn't give you permission."),
                _("Pinch me again without asking and see what I do with that hand."),
            ],
            "flirt_lewd_pinch_ass_commanding_yes": [
                _("I'll let that one slide. Because I felt like it."),
                _("Cheeky. Fine. But you ask first next time."),
                _("Cute. You get away with it because I allow it."),
            ],
            "flirt_lewd_grab_tits_commanding_no": [
                _("Let go. Now. You don't grab, you ask."),
                _("Wrong move. My body, my rules."),
                _("Hands off. You ask, and then you wait for my answer."),
            ],
            "flirt_lewd_grab_tits_commanding_yes": [
                _("Fine. Gently. I'll tell you when to squeeze."),
                _("You may. For now. I can take it back whenever I want."),
                _("Go on, then. Slowly. I set the pace here."),
            ],
            "flirt_lewd_grab_ass_commanding_no": [
                _("Nope. Hands where I can see them."),
                _("Grabbing me isn't how this works. I say when, I say where."),
                _("Let go. Nobody grabs me unless I tell them to."),
            ],
            "flirt_lewd_grab_ass_commanding_yes": [
                _("Fine. But I decide where your hands go."),
                _("Mm. Keep it there. Don't move it until I say."),
                _("I'll allow it. Enjoy it while I'm feeling generous."),
            ],
            "flirt_lewd_ask_panties_commanding_no": [
                _("You don't ask for my panties. I give them to whoever earns them."),
                _("My panties? That's a reward, and you haven't earned a thing."),
                _("Bold. No. Try begging, it might go better."),
            ],
            "flirt_lewd_ask_panties_commanding_yes": [
                _("Maybe. If you're good. Very good."),
                _("You'll get them when I decide you've earned them."),
                _("Maybe. Ask me again on your knees and we'll see."),
            ],
            "flirt_lewd_touch_thighs_commanding_no": [
                _("Uh-uh. That hand stays at your side."),
                _("Did I tell you to touch me? Then why is your hand there?"),
                _("No. I decide who touches me, and when."),
            ],
            "flirt_lewd_touch_thighs_commanding_yes": [
                _("Fine. That high, no higher, until I say otherwise."),
                _("You can leave it there. Moving it is my call."),
                _("Mm. Good. Now keep still."),
            ],
            "flirt_lewd_touch_tits_commanding_no": [
                _("Hands off. You don't touch me, I let you touch me. Big difference."),
                _("No. Put it down. I'll tell you what you're allowed to touch."),
                _("Did I say you could? Then don't."),
            ],
            "flirt_lewd_touch_tits_commanding_yes": [
                _("Fine. Softly. I'll let you know if you're doing it right."),
                _("Go ahead. You're allowed. This time."),
                _("Mm. Keep going until I say stop."),
            ],
            "flirt_lewd_touch_pussy_commanding_no": [
                _("Whoa. No. You don't get to go there on your own."),
                _("Hand. Away. That's mine to give, not yours to take."),
                _("Nobody touches me there without my say. Remember that."),
            ],
            "flirt_lewd_touch_pussy_commanding_yes": [
                _("Fine. Slowly. And you stop the second I tell you to."),
                _("You want it that badly? Then you do exactly what I say."),
                _("Mm. I'll allow it. Don't get cocky, I'm still in charge."),
            ],
            # the sunscreen at the pool (Flirty.rpy _SunscreenLoop, flirt_lewd_react): she asked for his hands on her back
            "flirt_lewd_sunscreen_thighs_commanding_no": [
                _("My back. That's what I asked for. Hands where I told you."),
                _("Did I say thighs? No. Back. Now."),
                _("Nice try. Your hands go where I tell them to go."),
            ],
            "flirt_lewd_sunscreen_thighs_commanding_yes": [
                _("Fine. The thighs too. Slowly, and only as high as I say."),
                _("Mm. I didn't ask for that... but I'll allow it."),
                _("Go on. I'll tell you when to stop."),
            ],
            "flirt_lewd_sunscreen_ass_commanding_no": [
                _("That's not my back. Hands up, where I told you."),
                _("No. You don't decide what gets touched here. I do."),
                _("Back off. My ass wasn't on the list."),
            ],
            "flirt_lewd_sunscreen_ass_commanding_yes": [
                _("Fine. Be thorough. I'm watching."),
                _("Mm. I'll allow it. You stop when I say."),
                _("Go ahead. Since I'm in a good mood."),
            ],

                        # "You really nailed that training earlier."
            "flirt_safe_compliment_dr_skill_normal_yes": [
                _("You really did great back there."),
                _("Yeah, that run was impressive.")
            ],
            "flirt_safe_compliment_dr_skill_soft_no": [
                _("I could have done better, but thanks."),
                _("It was okay. I'm not satisfied yet.")
            ],

            # "You're looking extra beautiful today."
            "flirt_safe_compliment_beauty_today_shy_yes": [
                _("D-don't just say it like that..."),
                _("You can't just drop that out of nowhere.")
            ],
            "flirt_safe_compliment_beauty_today_normal_yes": [
                _("Oh? Noticed, did you?"),
                _("I guess I don't look too bad today.")
            ],
            "flirt_safe_compliment_beauty_today_soft_no": [
                _("Just today, huh?"),
                _("Are you saying I don't usually look good?")
            ],

            # "Hey there, gorgeous."
            "flirt_safe_compliment_gorgeous_normal_yes": [
                _("Hey yourself."),
                _("That's one way to say hello.")
            ],
            "flirt_safe_compliment_gorgeous_soft_no": [
                _("Tone it down a little."),
                _("You're laying it on a bit thick.")
            ],

            # "I'm so into you."
            "flirt_safe_compliment_so_into_you_normal_yes": [
                _("Good. Stay that way."),
                _("I'm not exactly mad about that.")
            ],
            "flirt_safe_compliment_so_into_you_soft_no": [
                _("You barely know me."),
                _("That's a bit much for now.")
            ],

            # "You're looking really toned lately."
            "flirt_safe_compliment_toned_body_normal_yes": [
                _("I've been putting in the work, you know."),
                _("You noticed? Good.")
            ],
            "flirt_safe_compliment_toned_body_soft_no": [
                _("Are you saying I didn't look toned before?"),
                _("That came out weird, you know.")
            ],

            # "Oh, what's that fragrance? It really suits you."
            "flirt_safe_compliment_fragrance_normal_yes": [
                _("You have a good nose."),
                _("Glad it doesn't bother you.")
            ],
            "flirt_safe_compliment_fragrance_soft_no": [
                _("You are a bit close, you know."),
                _("Talking about someone's smell is risky, you know.")
            ],

            # Hair + smile podem usar reações parecidas
            "flirt_safe_compliment_hair_today_normal_yes": [
                _("Took me a while to get it like this."),
                _("Good. It wasn't a waste of time then.")
            ],
            "flirt_safe_compliment_hair_today_soft_no": [
                _("So you didn't like it before?"),
                _("That sounded a bit backhanded.")
            ],

            "flirt_safe_compliment_smile_normal_yes": [
                _("Don't get used to seeing it."),
                _("If you make me smile, that's on you.")
            ],
            "flirt_safe_compliment_smile_soft_no": [
                _("I'm not a puppy you can just praise."),
                _("Don't make it weird.")
            ],

            # ==========================================
            # COMPLIMENTS (LEWD)
            # ==========================================

            # "You have some really nice tits."
            "flirt_lewd_compliment_tits_enthusiastic_yes": [
                _("You really are staring, huh?"),
                _("Glad you like what you see.")
            ],
            "flirt_lewd_compliment_tits_normal_yes": [
                _("That is one way to say it."),
                _("You're bold today, I'll give you that.")
            ],
            "flirt_lewd_compliment_tits_soft_no": [
                _("Maybe keep your eyes a bit higher."),
                _("You could have phrased that a lot better.")
            ],
            "flirt_lewd_compliment_tits_hard_no": [
                _("Watch where your eyes are."),
                _("That's not how you compliment someone.")
            ],

            # "Your ass looks really great."
            "flirt_lewd_compliment_ass_enthusiastic_yes": [
                _("You think so? That's good to hear."),
                _("I didn't work on it for nothing.")
            ],
            "flirt_lewd_compliment_ass_normal_yes": [
                _("That's... one way to put it."),
                _("You really are focused on my ass, huh?")
            ],
            "flirt_lewd_compliment_ass_soft_no": [
                _("Maybe don't say that so casually."),
                _("You sound a bit too proud of yourself right now.")
            ],
            "flirt_lewd_compliment_ass_hard_no": [
                _("Don't talk about my ass like that."),
                _("Try again without sounding like a creep.")
            ],
            "flirt_safe_compliment_dr_skill_shy_yes": [
                _("I-I guess I did okay back there."),
                _("Don't hype me up that much, it's embarrassing.")
            ],
            "flirt_safe_compliment_dr_skill_enthusiastic_yes": [
                _("Damn right I nailed it."),
                _("Next time I'll make it look even better.")
            ],
            "flirt_safe_compliment_dr_skill_hard_no": [
                _("It wasn't that great, stop exaggerating."),
                _("Don't act like I'm some kind of superhero.")
            ],
            "flirt_safe_compliment_dr_skill_obedient_yes": [
                _("If you say so, I'll take the compliment."),
                _("Glad it looked good from your side.")
            ],

            # ---- BEAUTY TODAY ----
            "flirt_safe_compliment_beauty_today_enthusiastic_yes": [
                _("Of course I look good today."),
                _("I did put effort into this, you better notice.")
            ],
            "flirt_safe_compliment_beauty_today_hard_no": [
                _("Don't flirt with me just to say something."),
                _("That sounded way too rehearsed.")
            ],
            "flirt_safe_compliment_beauty_today_obedient_yes": [
                _("Thanks, I guess."),
                _("I'll accept that one.")
            ],

            # ---- GORGEOUS ----
            "flirt_safe_compliment_gorgeous_shy_yes": [
                _("D-don't call me that out of nowhere."),
                _("You're going to make me blush if you keep that up.")
            ],
            "flirt_safe_compliment_gorgeous_enthusiastic_yes": [
                _("Keep calling me that and we might have a problem."),
                _("I could get used to hearing that, you know.")
            ],
            "flirt_safe_compliment_gorgeous_hard_no": [
                _("Don't throw that word around like it's nothing."),
                _("Save that for when you actually mean it.")
            ],
            "flirt_safe_compliment_gorgeous_obedient_yes": [
                _("Fine, hello to you too."),
                _("I'll let that greeting slide.")
            ],

            # ---- SO INTO YOU ----
            "flirt_safe_compliment_so_into_you_shy_yes": [
                _("That's... a lot to just drop on me."),
                _("You really had to say it like that, huh?")
            ],
            "flirt_safe_compliment_so_into_you_enthusiastic_yes": [
                _("Good. Stay into me."),
                _("Then prove it.")
            ],
            "flirt_safe_compliment_so_into_you_hard_no": [
                _("You don't even know me that well."),
                _("That's a bit much for where we are right now.")
            ],
            "flirt_safe_compliment_so_into_you_obedient_yes": [
                _("I'll keep that in mind."),
                _("Then don't change your mind later.")
            ],

            # ---- TONED BODY ----
            "flirt_safe_compliment_toned_body_shy_yes": [
                _("I-I have been working out a little."),
                _("Don't make a big deal out of it.")
            ],
            "flirt_safe_compliment_toned_body_enthusiastic_yes": [
                _("Yeah, I like the way it's turning out too."),
                _("All that training is finally paying off.")
            ],
            "flirt_safe_compliment_toned_body_hard_no": [
                _("Are you trying to comment on my body shape now?"),
                _("That came out wrong, you know.")
            ],
            "flirt_safe_compliment_toned_body_obedient_yes": [
                _("Thanks, I guess I'll keep at it."),
                _("I appreciate you noticing.")
            ],

            # ---- FRAGRANCE ----
            "flirt_safe_compliment_fragrance_shy_yes": [
                _("Oh, you noticed that?"),
                _("I didn't think anyone would pick up on it.")
            ],
            "flirt_safe_compliment_fragrance_enthusiastic_yes": [
                _("Of course it suits me."),
                _("I chose it exactly for that.")
            ],
            "flirt_safe_compliment_fragrance_hard_no": [
                _("Talking about scents can get weird really fast."),
                _("Maybe don't sniff people mid-conversation.")
            ],
            "flirt_safe_compliment_fragrance_obedient_yes": [
                _("If it doesn't bother you, that's good."),
                _("I'll take that as a good sign.")
            ],

            # ---- HAIR TODAY ----
            "flirt_safe_compliment_hair_today_shy_yes": [
                _("Took me a while to get it like this."),
                _("Glad someone actually noticed.")
            ],
            "flirt_safe_compliment_hair_today_enthusiastic_yes": [
                _("Yeah, I was kind of proud of it."),
                _("I was waiting for someone to say that.")
            ],
            "flirt_safe_compliment_hair_today_hard_no": [
                _("That sounded more backhanded than you think."),
                _("You sure you phrased that right?")
            ],
            "flirt_safe_compliment_hair_today_obedient_yes": [
                _("I'll take the compliment."),
                _("Thanks, I guess.")
            ],

            # ---- SMILE ----
            "flirt_safe_compliment_smile_shy_yes": [
                _("Don't point it out, you'll make it disappear."),
                _("You're going to make me self-conscious.")
            ],
            "flirt_safe_compliment_smile_enthusiastic_yes": [
                _("Then make me smile more often."),
                _("Good, that means you're doing something right.")
            ],
            "flirt_safe_compliment_smile_hard_no": [
                _("Now you're just buttering me up."),
                _("Don't treat my smile like some kind of achievement.")
            ],
            "flirt_safe_compliment_smile_obedient_yes": [
                _("Thanks. That's... nice of you to say."),
                _("I'll allow that one.")
            ],

            # ==========================================
            # COMPLIMENTS (LEWD) - MISSING REACTIONS
            # ==========================================

            # ---- TITS ----
            "flirt_lewd_compliment_tits_shy_yes": [
                _("You really just said that out loud..."),
                _("D-don't stare so openly when you say it.")
            ],
            # His hands answered out of obedience (get_flirt_reaction_mode_lewd "obedient_yes": a yes by Obed). These
            # pools were missing: she said nothing (plan_submissive_pass S1). Deference for any girl who yields this way.
            "flirt_lewd_slap_ass_obedient_yes": [
                _("Ah! ...Okay. If you want to. I'll hold still."),
                _("...Yes. You can. Tell me if I should turn around."),
            ],
            "flirt_lewd_pinch_ass_obedient_yes": [
                _("Mm! ...Okay. Whatever you want."),
                _("That's... fine. You can. I won't move."),
            ],
            "flirt_lewd_grab_tits_obedient_yes": [
                _("...Okay. Go ahead. Tell me if I should... do anything."),
                _("If that's what you want. Yes. I'll keep my hands down."),
            ],
            "flirt_lewd_grab_ass_obedient_yes": [
                _("Okay. ...Both hands if you want. I'll stay like this."),
                _("Yes. You can. Just say if I should move."),
            ],
            "flirt_lewd_touch_thighs_obedient_yes": [
                _("Okay... yes. Should I open them a little? Just say."),
                _("You can. I'll hold still. Tell me what you want."),
            ],
            "flirt_lewd_touch_tits_obedient_yes": [
                _("...Yes. Okay. Gently or not, you decide."),
                _("If you want to. Yes. Tell me if I should take something off."),
            ],
            "flirt_lewd_touch_pussy_obedient_yes": [
                _("...Okay. Yes. Tell me what to do. I'll be good."),
                _("Yes. You can. I'll... I'll stay still."),
            ],
            "flirt_lewd_ask_panties_obedient_yes": [
                _("...Okay. Here. Don't... don't tell anyone, please."),
                _("If you want them. Yes. Give me a second."),
            ],
            "flirt_safe_touch_cheek_obedient_yes": [
                _("...Okay. You can."),
                _("Yes. That's... that's fine. Whatever you want."),
            ],
            "flirt_safe_hug_obedient_yes": [
                _("Okay. ...Like this? Tell me if I should let go."),
                _("Yes. You can hold me. As long as you want."),
            ],
            "flirt_safe_hold_hands_obedient_yes": [
                _("Okay. ...Yes. You can."),
                _("If you want to. Here."),
            ],
            "flirt_safe_kiss_cheek_obedient_yes": [
                _("...Okay. Go ahead."),
                _("Yes. You can. I'll hold still."),
            ],
            "flirt_safe_shoulder_massage_obedient_yes": [
                _("Okay. ...Yes. Wherever you want to touch."),
                _("If you want to. I'll sit still. Tell me if I should move."),
            ],
            "flirt_safe_steal_kiss_obedient_yes": [
                _("...! ...Okay. That's... okay. If you want."),
                _("Oh. ...Yes. You can do that. Whenever you want."),
            ],
            "flirt_lewd_compliment_tits_obedient_yes": [
                _("If you like them that much, fine."),
                _("Not the most elegant way to say it, but noted.")
            ],

                        # ---- EYES ----
            "flirt_safe_compliment_eyes_shy_yes": [
                _("You can't just say that with a straight face..."),
                _("D-don't look at me like that when you say it.")
            ],
            "flirt_safe_compliment_eyes_normal_yes": [
                _("At least you have good taste."),
                _("You really like staring, huh?")
            ],
            "flirt_safe_compliment_eyes_enthusiastic_yes": [
                _("If you get lost in them, that's your problem."),
                _("Careful, I might start using that against you.")
            ],
            "flirt_safe_compliment_eyes_soft_no": [
                _("That sounded way too cheesy."),
                _("You practiced that line, didn't you?")
            ],
            "flirt_safe_compliment_eyes_hard_no": [
                _("Yeah, no. That line was terrible."),
                _("Try something that doesn't sound copied from a cheap movie.")
            ],
            "flirt_safe_compliment_eyes_obedient_yes": [
                _("Fine, I'll take the compliment."),
                _("Noted. I'll pretend that sounded natural.")
            ],

            # ---- ASS ----
            "flirt_lewd_compliment_ass_shy_yes": [
                _("You really are looking that closely, huh..."),
                _("I can feel your eyes back there, you know.")
            ],
            "flirt_lewd_compliment_ass_obedient_yes": [
                _("If you say so."),
                _("Glad to know the view isn't terrible.")
            ],

            # ==========================================
            # NEW DAILY COMPLIMENTS
            # ==========================================

            # ---- GYM WEIGHTS ----
            "flirt_safe_compliment_gym_weights_shy_yes": [
                _("Y-you were watching me at the gym?"),
                _("Don't stare too much... it's embarrassing.")
            ],
            "flirt_safe_compliment_gym_weights_normal_yes": [
                _("Thanks. I've been pushing myself harder lately."),
                _("Good to know someone notices the effort.")
            ],
            "flirt_safe_compliment_gym_weights_enthusiastic_yes": [
                _("Damn right. I've been killing it at the gym."),
                _("Keep watching. I'm only getting stronger.")
            ],
            "flirt_safe_compliment_gym_weights_soft_no": [
                _("It wasn't that impressive, honestly."),
                _("You don't have to say that just to be nice.")
            ],
            "flirt_safe_compliment_gym_weights_hard_no": [
                _("Were you just staring at me the whole time?"),
                _("Don't make the gym weird.")
            ],
            "flirt_safe_compliment_gym_weights_obedient_yes": [
                _("Thanks. I'll keep at it."),
                _("Noted. I appreciate it.")
            ],

            # ---- CLASS GRADES ----
            "flirt_safe_compliment_class_grades_shy_yes": [
                _("I-I've been studying a lot... it's nice someone noticed."),
                _("Don't make a big deal out of it, okay?")
            ],
            "flirt_safe_compliment_class_grades_normal_yes": [
                _("Yeah, I've been putting in the work."),
                _("It pays to actually study, turns out.")
            ],
            "flirt_safe_compliment_class_grades_enthusiastic_yes": [
                _("Of course. I don't settle for anything less."),
                _("Brains and beauty. The full package.")
            ],
            "flirt_safe_compliment_class_grades_soft_no": [
                _("They could be better, honestly."),
                _("Don't jinx it. The next exam might humble me.")
            ],
            "flirt_safe_compliment_class_grades_hard_no": [
                _("Are you checking my grades now? That's a bit much."),
                _("Mind your own GPA first.")
            ],
            "flirt_safe_compliment_class_grades_obedient_yes": [
                _("Thanks. I guess the effort is paying off."),
                _("I'll keep trying my best.")
            ],

            # ---- OUTFIT STYLE ----
            "flirt_safe_compliment_outfit_style_shy_yes": [
                _("Y-you think so? I wasn't sure about this one..."),
                _("Thanks... I tried something different today.")
            ],
            "flirt_safe_compliment_outfit_style_normal_yes": [
                _("I have good taste, what can I say?"),
                _("Glad you noticed. I picked this one carefully.")
            ],
            "flirt_safe_compliment_outfit_style_enthusiastic_yes": [
                _("Obviously. Fashion is an art and I'm the artist."),
                _("You should see what else I have in my closet.")
            ],
            "flirt_safe_compliment_outfit_style_soft_no": [
                _("It's just clothes. Don't read too much into it."),
                _("I grabbed whatever was clean, honestly.")
            ],
            "flirt_safe_compliment_outfit_style_hard_no": [
                _("Are you trying to butter me up or something?"),
                _("Save the flattery for someone who needs it.")
            ],
            "flirt_safe_compliment_outfit_style_obedient_yes": [
                _("Thanks. I'll remember you liked this one."),
                _("Noted. Maybe I'll wear it more often.")
            ],

            # ---- CONFIDENCE ----
            "flirt_safe_compliment_confidence_shy_yes": [
                _("C-confident? Me? I'm not so sure about that..."),
                _("You think I'm confident? That's... nice to hear.")
            ],
            "flirt_safe_compliment_confidence_normal_yes": [
                _("Someone has to be. Might as well be me."),
                _("Thanks. I try not to second-guess myself.")
            ],
            "flirt_safe_compliment_confidence_enthusiastic_yes": [
                _("I know what I want and I go for it. Simple."),
                _("Confidence is attractive, isn't it?")
            ],
            "flirt_safe_compliment_confidence_soft_no": [
                _("Confident? I fake it half the time."),
                _("That's a stretch. I'm just stubborn.")
            ],
            "flirt_safe_compliment_confidence_hard_no": [
                _("Don't confuse confidence with not caring."),
                _("You're reading too much into it.")
            ],
            "flirt_safe_compliment_confidence_obedient_yes": [
                _("If you say so. I'll take the compliment."),
                _("Thanks, I guess.")
            ],

            # ---- SMART ----
            "flirt_safe_compliment_smart_shy_yes": [
                _("S-smart? I just pay attention in class..."),
                _("Don't say that too loud, people will expect things from me.")
            ],
            "flirt_safe_compliment_smart_normal_yes": [
                _("I do try to keep up. Thanks for noticing."),
                _("Brains over everything, right?")
            ],
            "flirt_safe_compliment_smart_enthusiastic_yes": [
                _("Finally, someone who recognizes it."),
                _("Smart and good-looking. Hard to compete with that.")
            ],
            "flirt_safe_compliment_smart_soft_no": [
                _("I'm not that smart. I just study more than most."),
                _("Don't put me on a pedestal. I struggle too.")
            ],
            "flirt_safe_compliment_smart_hard_no": [
                _("Are you just saying that to get on my good side?"),
                _("Intelligence isn't something you compliment like that.")
            ],
            "flirt_safe_compliment_smart_obedient_yes": [
                _("Thanks. I'll keep proving it."),
                _("I appreciate that.")
            ],

            # ---- LAUGH ----
            "flirt_safe_compliment_laugh_shy_yes": [
                _("M-my laugh? Nobody ever says that..."),
                _("Stop, you're going to make me self-conscious about it.")
            ],
            "flirt_safe_compliment_laugh_normal_yes": [
                _("Is it? I never really thought about it."),
                _("Well, you make me laugh, so blame yourself.")
            ],
            "flirt_safe_compliment_laugh_enthusiastic_yes": [
                _("Then keep being funny and you'll hear it more."),
                _("Good. I like making people smile.")
            ],
            "flirt_safe_compliment_laugh_soft_no": [
                _("My laugh? Really? That's what you're going with?"),
                _("That's a weird thing to compliment.")
            ],
            "flirt_safe_compliment_laugh_hard_no": [
                _("Don't make it weird. I just laughed."),
                _("That's the most random thing you could have said.")
            ],
            "flirt_safe_compliment_laugh_obedient_yes": [
                _("If you say so. I'll laugh more, then."),
                _("Thanks, I guess that's a nice thing to hear.")
            ],

            # ==========================================
            # TRAIT-SPECIFIC FLIRT OVERRIDES
            # ==========================================

            # --- HARDCORE trait: bolder, more aggressive reactions ---
            "flirt_safe_touch_cheek_enthusiastic_yes.hardcore_sex": [
                _("That all you got? Touch me like you mean it."),
                _("Gentle won't cut it with me. Try harder."),
            ],
            "flirt_safe_hug_enthusiastic_yes.hardcore_sex": [
                _("Squeeze harder. I won't break."),
                _("That's a hug? I've been hit harder than that."),
            ],
            "flirt_safe_shoulder_massage_enthusiastic_yes.hardcore_sex": [
                _("Harder. Don't be such a wimp about it."),
                _("You call that pressure? Dig in."),
            ],
            "flirt_lewd_slap_ass_enthusiastic_yes.hardcore_sex": [
                _("That's more like it. Don't hold back next time."),
                _("You can hit harder than that. I can take it."),
            ],
            "flirt_lewd_grab_tits_enthusiastic_yes.hardcore_sex": [
                _("Grab them properly. I'm not made of glass."),
                _("If you're gonna touch, commit to it."),
            ],
            "flirt_lewd_grab_ass_enthusiastic_yes.hardcore_sex": [
                _("Now we're talking. Don't be shy."),
                _("Good grip. Keep that energy."),
            ],

            # --- CUTE trait: softer, more flustered reactions ---
            "flirt_safe_touch_cheek_shy_yes.cute_sex": [
                _("Mmm... your hand is warm... don't move it yet."),
                _("That's... really sweet of you. *blushes*"),
            ],
            "flirt_safe_hold_hands_shy_yes.cute_sex": [
                _("Your fingers are so warm... can we stay like this?"),
                _("I-I like how our hands fit together..."),
            ],
            "flirt_safe_hug_shy_yes.cute_sex": [
                _("You smell nice... don't let go yet, okay?"),
                _("Can we just... stay like this for a bit?"),
            ],
            "flirt_safe_kiss_cheek_shy_yes.cute_sex": [
                _("M-my heart is going crazy right now..."),
                _("You can't just do that and expect me to be okay..."),
            ],
            "flirt_lewd_slap_ass_soft_no.cute_sex": [
                _("Ow! That hurt... don't be so rough with me..."),
                _("Hey! Be gentle... I'm not into that..."),
            ],
            "flirt_lewd_grab_tits_soft_no.cute_sex": [
                _("H-hey! Be gentle with those, please..."),
                _("Don't just grab them like that... it's scary..."),
            ],

            # --- CHEATER trait: flirty even when 'rejecting' ---
            "flirt_safe_touch_cheek_soft_no.cheater": [
                _("Not here. My %(pl)s might find out."),
                _("Save it for when we're alone, okay?"),
            ],
            "flirt_safe_steal_kiss_soft_no.cheater": [
                _("Not in public. Later, when %(pp)s's not around."),
                _("Timing, babe. I can't get caught."),
            ],
            "flirt_lewd_slap_ass_normal_yes.cheater": [
                _("My %(pl)s never does that. Keep going."),
                _("%(Pp)s'd lose %(poss)s mind if %(pp)s saw this. I love it."),
            ],
            "flirt_lewd_grab_tits_normal_yes.cheater": [
                _("Better than my %(pl)s's hands, honestly."),
                _("%(Pp)s never touches me like this. Don't stop."),
            ],
            "flirt_lewd_ask_panties_normal_yes.cheater": [
                _("My %(pl)s doesn't even ask for those. You're bold."),
                _("Maybe. If you make it worth my while."),
            ],

            # --- PLAYER_CHEATING: girl is single but player has a GF ---
            "flirt_safe_touch_cheek_soft_no.player_cheating": [
                _("Don't you have a girlfriend? She might see us."),
                _("You're taken, remember? Not here."),
            ],
            "flirt_safe_touch_cheek_normal_yes.player_cheating": [
                _("Doesn't your girlfriend mind you touching other girls like this?"),
                _("If she saw you right now... she'd lose it."),
            ],
            "flirt_safe_steal_kiss_soft_no.player_cheating": [
                _("Your girlfriend is right there, are you crazy?"),
                _("Not while you're with someone. That's messy."),
            ],
            "flirt_safe_steal_kiss_normal_yes.player_cheating": [
                _("Your girlfriend would hate this... but I don't care."),
                _("Hope she's not watching. Actually... I don't really care."),
            ],
            "flirt_lewd_slap_ass_normal_yes.player_cheating": [
                _("Does your girlfriend let you do this? Doubt it."),
                _("Careful, your girl might get jealous~"),
            ],
            "flirt_lewd_grab_tits_normal_yes.player_cheating": [
                _("Bet your girlfriend doesn't let you grab hers like this."),
                _("Hope your hands were clean before you touched her. Just kidding."),
            ],

            # --- BOTH_CHEATING: girl has bf AND player has gf ---
            "flirt_safe_touch_cheek_soft_no.both_cheating": [
                _("We both have someone. Not here."),
                _("My %(pl)s AND your girlfriend... bad idea right now."),
            ],
            "flirt_safe_touch_cheek_normal_yes.both_cheating": [
                _("We're both cheating right now, huh? Feels dangerous."),
                _("Your girlfriend, my %(pl)s... neither of them would survive seeing this."),
            ],
            "flirt_safe_steal_kiss_soft_no.both_cheating": [
                _("Both of us taken and you want to kiss me here? Risky."),
                _("Your girlfriend AND my %(pl)s could find out. Not now."),
            ],
            "flirt_safe_steal_kiss_normal_yes.both_cheating": [
                _("We're both terrible people. Kiss me anyway."),
                _("My %(pl)s, your girlfriend... they'd both die. Do it."),
            ],
            "flirt_lewd_slap_ass_normal_yes.both_cheating": [
                _("My %(pl)s never does that. Your girlfriend never lets you, right? We're perfect for each other."),
                _("Two cheaters in one room. Slap me again."),
            ],
            "flirt_lewd_grab_tits_normal_yes.both_cheating": [
                _("Your girlfriend AND my %(pl)s would lose their minds right now. Don't stop."),
                _("Better than %(poss)s hands AND probably better than her letting you, right?"),
            ],

            # --- VIRGIN trait: extra nervous reactions ---
            "flirt_lewd_slap_ass_shy_yes.virgin": [
                _("I-I've never had anyone do that before..."),
                _("That was my first time being touched like that..."),
            ],
            "flirt_lewd_grab_tits_shy_yes.virgin": [
                _("N-no one has ever touched me there before..."),
                _("I... this is all so new to me..."),
            ],
            "flirt_lewd_grab_ass_shy_yes.virgin": [
                _("I've never... no one's grabbed me like that..."),
                _("Is this what it's like? Being touched?"),
            ],
            "flirt_lewd_ask_panties_hard_no.virgin": [
                _("M-my panties?! I've never even shown anyone!"),
                _("That's way too much! I'm not that kind of girl!"),
            ],

            # --- PUBLIC_SHY trait: extra worried about being seen ---
            "flirt_safe_kiss_cheek_soft_no.public_shy": [
                _("Not here! Someone might see us!"),
                _("W-what if people are watching?! Stop!"),
            ],
            "flirt_safe_hold_hands_soft_no.public_shy": [
                _("People will talk if they see us holding hands!"),
                _("Can we... do this somewhere private?"),
            ],
            "flirt_lewd_slap_ass_hard_no.public_shy": [
                _("Are you insane?! People can see us!"),
                _("Someone definitely heard that! Oh god..."),
            ],
            "flirt_lewd_grab_tits_hard_no.public_shy": [
                _("Not here! What if someone walks by?!"),
                _("Are you trying to get us caught?!"),
            ],

            # --- EXHIBITIONIST trait: loves being seen ---
            "flirt_safe_kiss_cheek_enthusiastic_yes.exhibitionist": [
                _("Do it again. Louder this time."),
                _("I hope everyone saw that."),
            ],
            "flirt_lewd_slap_ass_enthusiastic_yes.exhibitionist": [
                _("Louder. I want people to hear."),
                _("Do it again. Let them watch."),
            ],
            "flirt_lewd_grab_tits_enthusiastic_yes.exhibitionist": [
                _("Right here? Good. Let them see."),
                _("I don't care who's watching. Keep going."),
            ],
            "flirt_lewd_grab_ass_enthusiastic_yes.exhibitionist": [
                _("Good. I want everyone to know."),
                _("Grab it like you own it. People are watching."),
            ],

            # --- CAMERA_LOVER trait: loves attention, references being filmed/photographed ---
            "flirt_safe_touch_cheek_enthusiastic_yes.camera_lover": [
                _("Ooh, that's a cute angle. Someone should be filming this."),
                _("If you're gonna touch me like that, at least make sure there's a camera rolling."),
                _("I bet that would look great on camera."),
            ],
            "flirt_safe_kiss_cheek_enthusiastic_yes.camera_lover": [
                _("That was adorable. I wish someone got a picture of that."),
                _("Next time, let's film it. For memories, obviously."),
                _("If that was on video, it would go viral."),
            ],
            "flirt_safe_hug_enthusiastic_yes.camera_lover": [
                _("Hold me tighter. This would make a perfect photo."),
                _("Someone better be capturing this moment."),
            ],
            "flirt_lewd_slap_ass_enthusiastic_yes.camera_lover": [
                _("Ooh! Do that again. I want it on video."),
                _("If someone filmed that, I wouldn't even be mad."),
                _("That's the kind of content people pay for."),
            ],
            "flirt_lewd_grab_tits_enthusiastic_yes.camera_lover": [
                _("Hold that pose. This would make a great shot."),
                _("You know, if there was a camera here, I wouldn't mind."),
            ],
            "flirt_lewd_grab_ass_enthusiastic_yes.camera_lover": [
                _("Grab it like that again. Slowly. Camera-worthy."),
                _("I love when someone appreciates the view. Bonus points for recording it."),
            ],

            # --- CAMERA_HATER trait: uncomfortable with attention, defensive ---
            "flirt_safe_touch_cheek_soft_no.camera_hater": [
                _("Don't draw attention to us like that."),
                _("Keep it subtle, will you? I hate being stared at."),
            ],
            "flirt_safe_kiss_cheek_soft_no.camera_hater": [
                _("Not where people can see! I hate being the center of attention."),
                _("Could you NOT do that where everyone's looking?"),
                _("If anyone pulls out a phone right now, I'm leaving."),
            ],
            "flirt_safe_hug_soft_no.camera_hater": [
                _("Not out in the open like this. People stare."),
                _("I feel like everyone's watching us. Stop."),
            ],
            "flirt_lewd_slap_ass_hard_no.camera_hater": [
                _("Are you insane?! What if someone records that?!"),
                _("If that ends up on anyone's phone, you're dead."),
                _("I swear, if someone saw that, I'll never forgive you."),
            ],
            "flirt_lewd_grab_tits_hard_no.camera_hater": [
                _("What if someone has their phone out?! Stop!"),
                _("I will NOT be someone's viral moment. Hands off."),
            ],
            "flirt_lewd_grab_ass_hard_no.camera_hater": [
                _("If anyone filmed that, I'm blaming you."),
                _("Keep your hands to yourself. I don't need the attention."),
            ],

            # --- CUM_SLUT trait: sexually forward, explicit ---
            "flirt_safe_touch_cheek_enthusiastic_yes.cum_slut": [
                _("That's sweet, but you know where I really want those hands..."),
                _("Mmm, gentle. But I know you can be rougher than that."),
            ],
            "flirt_safe_kiss_cheek_enthusiastic_yes.cum_slut": [
                _("A cheek kiss? You know I want more than that."),
                _("Cute, but you're aiming too high. Try lower."),
                _("That's a start. Now kiss me where it really counts."),
            ],
            "flirt_lewd_slap_ass_enthusiastic_yes.cum_slut": [
                _("Mmm, harder. Make me feel it."),
                _("That's nothing. I can take way more than that."),
                _("You're holding back. Don't."),
            ],
            "flirt_lewd_grab_tits_enthusiastic_yes.cum_slut": [
                _("Good hands. Now imagine what else they could be doing."),
                _("Don't just grab them. Use your mouth too."),
            ],
            "flirt_lewd_grab_ass_enthusiastic_yes.cum_slut": [
                _("If you're grabbing me like that, you better follow through later."),
                _("Mmmm. You know exactly what I want after this, right?"),
                _("Keep going. I'm already getting ideas."),
            ],
            "flirt_lewd_ask_panties_enthusiastic_yes.cum_slut": [
                _("You want them? They might already be a little... wet."),
                _("Take them. I wasn't planning on wearing them much longer anyway."),
            ],

            # --- HATE_CUM trait: grossed out by anything sexual/messy ---
            "flirt_safe_touch_cheek_normal_yes.hate_cum": [
                _("That's nice. Just... keep it clean, okay?"),
                _("Sweet. As long as it stays PG."),
            ],
            "flirt_lewd_slap_ass_hard_no.hate_cum": [
                _("Ew, don't get all handsy with me. That's gross."),
                _("Keep your sweaty hands to yourself."),
                _("What's next, you gonna drool on me too? Disgusting."),
            ],
            "flirt_lewd_grab_tits_hard_no.hate_cum": [
                _("Gross! Get your hands off! I don't want your sweat on me."),
                _("That is so nasty. Don't ever do that again."),
            ],
            "flirt_lewd_grab_ass_hard_no.hate_cum": [
                _("Ew! Your hands are probably all clammy. Don't touch me."),
                _("That's disgusting. Have some hygiene."),
            ],
            "flirt_lewd_ask_panties_hard_no.hate_cum": [
                _("That is the most revolting thing anyone has ever asked me."),
                _("You want my panties? What are you, some kind of creep? Gross."),
                _("Absolutely not. That's disgusting beyond words."),
            ],
            "flirt_lewd_pinch_ass_hard_no.hate_cum": [
                _("Your fingers are gross. Keep them away from me."),
                _("Ugh, don't pinch me. That's so nasty."),
            ],

            # --- PUBLIC_FETISH trait: turned on by public acts, excited about being seen ---
            "flirt_safe_kiss_cheek_enthusiastic_yes.public_fetish": [
                _("Do it again. Right here where everyone can see."),
                _("Mmm, the fact that people might be watching makes it so much better."),
                _("Kiss me somewhere else next time. And don't wait until we're alone."),
            ],
            "flirt_safe_hold_hands_enthusiastic_yes.public_fetish": [
                _("I love this. Everyone can see we're together."),
                _("Hold my hand tighter. I want people to notice."),
            ],
            "flirt_lewd_slap_ass_enthusiastic_yes.public_fetish": [
                _("God, yes. Right here in front of everyone."),
                _("The sound probably turned heads. Good."),
                _("Do it again. Louder. I want them to hear."),
            ],
            "flirt_lewd_grab_tits_enthusiastic_yes.public_fetish": [
                _("Right here? Where anyone could walk by? ...Perfect."),
                _("I love that you don't care who sees. Neither do I."),
            ],
            "flirt_lewd_grab_ass_enthusiastic_yes.public_fetish": [
                _("Mmm, grab me where everyone can see. I dare you."),
                _("The thrill of getting caught makes it ten times better."),
                _("Anyone watching? Good. Let them enjoy the show."),
            ],
            "flirt_lewd_ask_panties_enthusiastic_yes.public_fetish": [
                _("Here? In public? ...That's exactly what makes it exciting."),
                _("What if I just slipped them off right here? Would you like that?"),
            ],

            # --- LOYAL trait: references boyfriend, conflicted, guilt ---
            "flirt_safe_touch_cheek_soft_no.loyal": [
                _("I have a %(pl)s... you know that, right?"),
                _("This feels wrong. I shouldn't let you touch me like this."),
                _("Please don't... I'm trying to be faithful."),
            ],
            "flirt_safe_kiss_cheek_soft_no.loyal": [
                _("I can't let you kiss me. I'm with someone."),
                _("That's... too intimate. My %(pl)s wouldn't like this."),
            ],
            "flirt_safe_hold_hands_soft_no.loyal": [
                _("I shouldn't hold your hand. It feels like cheating already."),
                _("My %(pl)s trusts me. I can't do this."),
            ],
            "flirt_safe_steal_kiss_soft_no.loyal": [
                _("No! I have a %(pl)s! I can't betray %(po)s like this!"),
                _("Stop... if %(pp)s ever finds out, it would destroy %(po)s."),
            ],
            "flirt_lewd_slap_ass_hard_no.loyal": [
                _("I'm taken! You can't just do that to someone's girlfriend!"),
                _("My %(pl)s would lose it if %(pp)s knew. Please stop."),
                _("I'm loyal to %(po)s. Don't make this harder than it already is."),
            ],
            "flirt_lewd_grab_tits_hard_no.loyal": [
                _("I have a %(pl)s! You can't touch me like that!"),
                _("This is so wrong... %(pp)s trusts me. Stop."),
            ],
            "flirt_lewd_grab_ass_hard_no.loyal": [
                _("I belong to someone else. Keep your hands to yourself."),
                _("%(Pp)s would be heartbroken... I can't let you do this."),
            ],
            "flirt_lewd_ask_panties_hard_no.loyal": [
                _("My panties?! I have a %(pl)s! What is wrong with you?"),
                _("Absolutely not. I would never betray %(po)s like that."),
            ],

            # --- TOUCH FLIRT TRAIT OVERRIDES ---

            # hardcore_sex
            "flirt_lewd_touch_thighs_enthusiastic_yes.hardcore_sex": [
                _("Higher. Don't tease me."),
            ],
            "flirt_lewd_touch_tits_enthusiastic_yes.hardcore_sex": [
                _("Squeeze harder. I can take it."),
            ],
            "flirt_lewd_touch_pussy_enthusiastic_yes.hardcore_sex": [
                _("Finally someone who doesn't ask first."),
            ],

            # virgin
            "flirt_lewd_touch_thighs_shy_yes.virgin": [
                _("N-nobody's ever touched me there before..."),
            ],
            "flirt_lewd_touch_tits_shy_yes.virgin": [
                _("I've never... no one has ever done that to me."),
            ],
            "flirt_lewd_touch_pussy_shy_yes.virgin": [
                _("W-wait, I've never... that's... that's really intense."),
            ],

            # public_shy
            "flirt_lewd_touch_thighs_hard_no.public_shy": [
                _("Someone could see! Are you crazy?"),
            ],
            "flirt_lewd_touch_tits_hard_no.public_shy": [
                _("Not here! People are watching!"),
            ],
            "flirt_lewd_touch_pussy_hard_no.public_shy": [
                _("Are you out of your mind?! We're in public!"),
            ],

            # exhibitionist
            "flirt_lewd_touch_thighs_enthusiastic_yes.exhibitionist": [
                _("Right here where people can see? I love it."),
            ],
            "flirt_lewd_touch_tits_enthusiastic_yes.exhibitionist": [
                _("Let them watch. I don't care."),
            ],
            "flirt_lewd_touch_pussy_enthusiastic_yes.exhibitionist": [
                _("You're doing this in public? That's so hot."),
            ],

            # public_fetish
            "flirt_lewd_touch_thighs_enthusiastic_yes.public_fetish": [
                _("Mm, anyone could walk by right now..."),
            ],
            "flirt_lewd_touch_tits_enthusiastic_yes.public_fetish": [
                _("The thought of someone catching us..."),
            ],
            "flirt_lewd_touch_pussy_enthusiastic_yes.public_fetish": [
                _("Oh god, what if someone sees your hand there?"),
            ],

            # cheater
            "flirt_lewd_touch_thighs_normal_yes.cheater": [
                _("What %(pp)s doesn't know won't hurt %(po)s."),
            ],
            "flirt_lewd_touch_tits_normal_yes.cheater": [
                _("%(Pp)s never touches me like that anyway."),
            ],
            "flirt_lewd_touch_pussy_normal_yes.cheater": [
                _("This is so wrong... but I don't want you to stop."),
            ],

            # loyal
            "flirt_lewd_touch_thighs_hard_no.loyal": [
                _("I have a %(pl)s! Don't touch me like that!"),
                _("%(Pp)s trusts me. I can't let you do this."),
            ],
            "flirt_lewd_touch_tits_hard_no.loyal": [
                _("Stop! %(Pp)s would be devastated if %(pp)s saw this!"),
            ],
            "flirt_lewd_touch_pussy_hard_no.loyal": [
                _("Get your hand away from me! I'm with %(po)s!"),
                _("This is a complete betrayal of %(poss)s trust. No."),
            ],

            # ---- NERD: EXAM ANXIETY (trait-gated by caller) ----
            "nerd_exam_mild": [
                _("The exam is coming up. I should probably review my notes tonight."),
                _("Have you started studying yet? I'm almost done with the first three chapters."),
                _("I made a study schedule. Want me to share it with you?"),
            ],
            "nerd_exam_worried": [
                _("The exam is in a few days and I still have two chapters to review. This is bad."),
                _("I keep re-reading the same page. Nothing is sticking. Why is nothing sticking?"),
                _("I had a dream about failing the exam last night. That's... that's not a good sign."),
            ],
            "nerd_exam_intense": [
                _("The exam is TOMORROW. I can't talk right now. I literally cannot talk right now."),
                _("If I fail this I'm done. My GPA is DONE. Leave me alone."),
                _("I've been studying for nine hours straight and I still don't feel ready."),
            ],
            "nerd_exam_relief": [
                _("It's over. I think I did well. I THINK I did well. Please let me have done well."),
                _("I finished twenty minutes early. Either I aced it or I'm delusional."),
                _("My hand hurts from writing but my brain feels empty in a good way."),
            ],

            "gym_rat_energy_low": [
                _("You look like you've never seen the inside of a gym before today."),
                _("Seriously? My grandma lifts heavier than you."),
                _("Do you even eat protein, or is your diet pure sadness?"),
            ],
            "gym_rat_energy_mid": [
                _("You're getting there. Slowly. Very slowly."),
                _("At least you're consistent. That counts for something."),
                _("Not terrible. But definitely not impressive either."),
            ],
            "gym_rat_energy_high": [
                _("Okay, I see you. You've been putting in the work."),
                _("Finally, someone in this gym who actually lifts."),
                _("You're built like someone who takes this seriously. I respect that."),
            ],

            # ── Pregnancy (Global fallbacks) ──
            # "Do you ever think about having kids?" (chitchat_ask_about_kids, ChitChat.rpy). Tier by Love:
            # base key = Love < 500, _mid = 500+, _high = 800+ AND dating. A pregnancy trait overrides the tier.
            "pregnancy_ask_about_kids": [
                _("I don't know... maybe someday?"),
                _("That's a big question. I haven't really thought about it."),
                _("Kids? Right now? That's... a lot to think about."),
            ],
            "pregnancy_ask_about_kids_mid": [
                _("With the right person? Yeah. I think I could see it someday."),
            ],
            "pregnancy_ask_about_kids_high": [
                _("With you? I've thought about it more than I should admit."),
            ],
            "pregnancy_ask_about_kids_fetish": [
                _("Honestly? I want it. More than I probably should."),
            ],
            "pregnancy_ask_about_kids_fear": [
                _("No. The idea scares me more than I can explain."),
            ],
            "pregnancy_casual_worry": [
                _("I've been thinking about the future a lot lately..."),
                _("Things are going to change, aren't they..."),
                _("I don't know if I'm ready for all of this..."),
            ],
            "pregnancy_casual_positive": [
                _("It's scary, but... I think we'll figure it out."),
                _("I never thought I'd feel this way, but... it's kind of exciting."),
            ],
        },

        # Example for girl id "g1" (Rogue, etc.)
        "g1": {
            "confess_love_accept": [
                _("Idiot... of course I like you too."),
                _("Took you long enough to say it.")
            ],
            # You can override any flirt key here, for example:
            # "flirt_safe_touch_cheek_shy_yes": [ "G-gentle, okay? I'm not used to this..." ],
        },

        "g2": {
            "confess_love_accept": [
                _("This is embarrassing, but... yes."),
                _("You caught me off guard... but I feel the same way."),
            ],
            "confess_love_reject": [
                _("I like you, but not as a boyfriend."),
                _("I appreciate you telling me, but... I just don't feel that way."),
            ],
        },

        # ==========================================================
        # GWEN — Pregnancy Dialogue
        # ==========================================================
        "gwen": {
            "pregnancy_ask_about_kids": [
                _("I mean, maybe someday? I'm not in a rush though."),
                _("It's not something I think about right now."),
            ],
            "pregnancy_ask_about_kids_mid": [
                _("I guess with the right person... eventually."),
            ],
            "pregnancy_ask_about_kids_high": [
                _("If it was with you, I think I'd be okay with it."),
            ],
            "pregnancy_ask_about_kids_fetish": [
                _("I've always wanted kids. More than one, honestly."),
            ],
            "pregnancy_ask_about_kids_fear": [
                _("Honestly? The thought terrifies me. Not now, not for a long time."),
            ],
            "pregnancy_casual_worry": [
                _("How are we going to handle this? We're still in college."),
                _("I keep thinking about the money, the time, our studies..."),
                _("We need a plan. Like, a real plan."),
            ],
            "pregnancy_casual_positive": [
                _("Look, we'll figure it out. Together."),
                _("My mom already asked about grandkids. She's going to lose her mind."),
                _("I've been looking at baby names. Nothing feels right yet."),
            ],
        },

        # ==========================================================
        # ROGUE — Pregnancy Dialogue
        # ==========================================================
        "rogue": {
            "pregnancy_ask_about_kids": [
                _("Sugar, I ain't even figured out my own life yet."),
                _("I'm way too young for that conversation."),
            ],
            "pregnancy_ask_about_kids_mid": [
                _("Someday, with someone I really trust."),
            ],
            "pregnancy_ask_about_kids_high": [
                _("If you're asking what I think you're asking... I'd say yes."),
            ],
            "pregnancy_ask_about_kids_fetish": [
                _("I've been dreaming about being a mama since I was little."),
            ],
            "pregnancy_ask_about_kids_fear": [
                _("I ain't ready. The very idea gives me anxiety."),
            ],
            "pregnancy_casual_worry": [
                _("I never thought this would happen. I literally have no idea what to do."),
                _("My mama had me young too. It didn't go well for either of us, and I swore I'd never repeat her mistakes."),
                _("I can't even keep a plant alive..."),
            ],
            "pregnancy_casual_positive": [
                _("I'm so lost right now. But at least I'm not alone in this... right?"),
                _("My aunt's already knitting baby blankets."),
                _("I've been thinking about what kind of mom I want to be."),
            ],
        },

        # ==========================================================
        # NTW (Negasonic Teenage Warhead)
        # ISTP 8w9: blunt, minimal words, pragmatic, firm boundaries
        # Hints at preference for girls in some lines
        # ==========================================================
        "ntw": {

            # ---- CONFESSIONS ----
            "confess_love_accept": [
                _("...you're an idiot. But... fine."),
                _("I don't know why, but... yeah. Whatever."),
                _("...don't make me say it twice."),
            ],
            "confess_love_reject": [
                _("No."),
                _("I don't do... that. Not with you."),
                _("You're not really my type. At all."),
            ],

            # ==========================
            # SAFE FLIRT: TOUCH CHEEK
            # ==========================
            "flirt_safe_touch_cheek_shy_yes": [
                _("...don't make a habit of it."),
                _("...whatever. Just once."),
            ],
            "flirt_safe_touch_cheek_normal_yes": [
                _("...sure."),
                _("Hm."),
            ],
            "flirt_safe_touch_cheek_enthusiastic_yes": [
                _("Fine. But only because I'm bored."),
                _("...do what you want."),
            ],
            "flirt_safe_touch_cheek_obedient_yes": [
                _("...go ahead."),
                _("If it shuts you up."),
            ],
            "flirt_safe_touch_cheek_soft_no": [
                _("No."),
                _("Don't."),
            ],
            "flirt_safe_touch_cheek_hard_no": [
                _("Touch me again and I'll snap your wrist."),
                _("Back off. Now."),
            ],

            # ==========================
            # SAFE FLIRT: HOLD HANDS
            # ==========================
            "flirt_safe_hold_hands_shy_yes": [
                _("...why?"),
                _("...fine. But don't squeeze."),
            ],
            "flirt_safe_hold_hands_normal_yes": [
                _("If it makes you shut up, fine."),
                _("...whatever."),
            ],
            "flirt_safe_hold_hands_enthusiastic_yes": [
                _("...your hands are warm, at least."),
                _("Don't read into it."),
            ],
            "flirt_safe_hold_hands_obedient_yes": [
                _("...fine."),
                _("Make it quick."),
            ],
            "flirt_safe_hold_hands_soft_no": [
                _("I don't do that."),
                _("No thanks."),
            ],
            "flirt_safe_hold_hands_hard_no": [
                _("Get your hand off me."),
                _("I said no. Hearing problem?"),
            ],

            # ==========================
            # SAFE FLIRT: JOKE
            # ==========================
            "flirt_safe_joke_shy_yes": [
                _("...pff."),
                _("...almost got me."),
            ],
            "flirt_safe_joke_normal_yes": [
                _("That was almost funny."),
                _("...hm. Not bad."),
            ],
            "flirt_safe_joke_soft_no": [
                _("That was bad."),
                _("Try harder."),
            ],
            "flirt_safe_joke_hard_no": [
                _("Stop talking."),
                _("That's the worst thing I've heard today. And I've heard a lot."),
            ],

            # ==========================
            # SAFE FLIRT: KISS CHEEK
            # ==========================
            "flirt_safe_kiss_cheek_shy_yes": [
                _("...you're lucky I didn't move."),
                _("...do that again and I can't promise what happens."),
            ],
            "flirt_safe_kiss_cheek_normal_yes": [
                _("Hm."),
                _("...fine. Once."),
            ],
            "flirt_safe_kiss_cheek_enthusiastic_yes": [
                _("...you're getting bold."),
                _("Don't let it go to your head."),
            ],
            "flirt_safe_kiss_cheek_obedient_yes": [
                _("...ok."),
                _("Quick."),
            ],
            "flirt_safe_kiss_cheek_soft_no": [
                _("Don't."),
                _("Not happening."),
            ],
            "flirt_safe_kiss_cheek_hard_no": [
                _("You want to keep those lips? Back off."),
                _("Do that again. I dare you."),
            ],

            # ==========================
            # SAFE FLIRT: STEAL KISS
            # ==========================
            "flirt_safe_steal_kiss_shy_yes": [
                _("...you're dead."),
                _("...I didn't say you could do that."),
            ],
            "flirt_safe_steal_kiss_normal_yes": [
                _("Do that again and see what happens."),
                _("...bold move."),
            ],
            "flirt_safe_steal_kiss_enthusiastic_yes": [
                _("...you really have a death wish."),
                _("Fine. You got one. Don't push your luck."),
            ],
            "flirt_safe_steal_kiss_soft_no": [
                _("Are you serious right now?"),
                _("...no."),
            ],
            "flirt_safe_steal_kiss_hard_no": [
                _("Touch my face again and I'll make sure you regret it."),
                _("You've got exactly one second to step back."),
            ],

            # ==========================
            # SAFE FLIRT: HUG
            # ==========================
            "flirt_safe_hug_shy_yes": [
                _("...fine. Two seconds."),
                _("...don't tell anyone."),
            ],
            "flirt_safe_hug_normal_yes": [
                _("Don't squeeze."),
                _("...make it quick."),
            ],
            "flirt_safe_hug_enthusiastic_yes": [
                _("...you're warm, I guess."),
                _("This doesn't mean anything."),
            ],
            "flirt_safe_hug_obedient_yes": [
                _("...go ahead."),
                _("Just... be fast about it."),
            ],
            "flirt_safe_hug_soft_no": [
                _("Not a hugger."),
                _("Pass."),
            ],
            "flirt_safe_hug_hard_no": [
                _("Back. Off."),
                _("I will shove you if you try that."),
            ],

            # ==========================
            # SAFE FLIRT: SHOULDER MASSAGE
            # ==========================
            "flirt_safe_shoulder_massage_shy_yes": [
                _("...ok, that's actually not bad."),
                _("...don't stop yet."),
            ],
            "flirt_safe_shoulder_massage_normal_yes": [
                _("Keep going. Don't talk."),
                _("...you're useful for something."),
            ],
            "flirt_safe_shoulder_massage_enthusiastic_yes": [
                _("...harder. You call that pressure?"),
                _("Ok. You get points for this."),
            ],
            "flirt_safe_shoulder_massage_obedient_yes": [
                _("...fine. Keep going."),
                _("Hm. Not bad."),
            ],
            "flirt_safe_shoulder_massage_soft_no": [
                _("I didn't ask for that."),
                _("Hands off."),
            ],
            "flirt_safe_shoulder_massage_hard_no": [
                _("Don't touch me."),
                _("What part of 'personal space' is hard for you?"),
            ],

            # ==========================
            # SAFE COMPLIMENTS
            # ==========================
            "flirt_safe_compliment_smile_shy_yes": [
                _("I wasn't smiling for you."),
                _("...don't read into it."),
            ],
            "flirt_safe_compliment_smile_normal_yes": [
                _("...whatever."),
                _("Hm."),
            ],
            "flirt_safe_compliment_smile_soft_no": [
                _("I don't smile."),
                _("You're seeing things."),
            ],
            "flirt_safe_compliment_smile_hard_no": [
                _("I wasn't smiling. Period."),
                _("Stop projecting."),
            ],
            "flirt_safe_compliment_class_shy_yes": [
                _("...it's not a big deal."),
                _("...I just paid attention. That's it."),
            ],
            "flirt_safe_compliment_class_normal_yes": [
                _("I know."),
                _("Took you a while to notice."),
            ],
            "flirt_safe_compliment_class_soft_no": [
                _("Don't care about grades."),
                _("School is school."),
            ],
            "flirt_safe_compliment_smart_shy_yes": [
                _("...thanks, I guess."),
                _("...shut up."),
            ],
            "flirt_safe_compliment_smart_normal_yes": [
                _("Obviously."),
                _("Tell me something I don't know."),
            ],
            "flirt_safe_compliment_gorgeous_shy_yes": [
                _("...stop."),
                _("...I hate you."),
            ],
            "flirt_safe_compliment_gorgeous_normal_yes": [
                _("..."),
                _("...ok."),
            ],
            "flirt_safe_compliment_gorgeous_soft_no": [
                _("Don't call me that."),
                _("Gross."),
            ],
            "flirt_safe_compliment_eyes_shy_yes": [
                _("...stop staring."),
                _("...you're making it weird."),
            ],
            "flirt_safe_compliment_eyes_normal_yes": [
                _("...thanks."),
                _("...you done?"),
            ],
            "flirt_safe_compliment_confidence_shy_yes": [
                _("...I'm not confident. I just don't care."),
                _("...there's a difference between confident and indifferent."),
            ],
            "flirt_safe_compliment_confidence_normal_yes": [
                _("I know what I want. That's it."),
                _("It's not confidence. It's clarity."),
            ],
            "flirt_safe_compliment_toned_body_shy_yes": [
                _("...you noticed?"),
                _("...I work out. So what."),
            ],
            "flirt_safe_compliment_toned_body_normal_yes": [
                _("I train. Don't make it weird."),
                _("Yeah. I put in the work."),
            ],
            "flirt_safe_compliment_so_into_you_shy_yes": [
                _("...what?"),
                _("...you're insane."),
            ],
            "flirt_safe_compliment_so_into_you_normal_yes": [
                _("...ok."),
                _("...noted."),
            ],
            "flirt_safe_compliment_so_into_you_soft_no": [
                _("You barely know me."),
                _("Slow down."),
            ],
            "flirt_safe_compliment_so_into_you_hard_no": [
                _("No you're not."),
                _("You don't even know what that means."),
            ],

            # ==========================
            # LEWD FLIRTS
            # ==========================
            "flirt_lewd_slap_ass_shy_yes": [
                _("...do that again and I'll decide if I liked it."),
            ],
            "flirt_lewd_slap_ass_normal_yes": [
                _("...bold."),
            ],
            "flirt_lewd_slap_ass_obedient_yes": [
                _("...fine."),
            ],
            "flirt_lewd_slap_ass_soft_no": [
                _("Seriously?"),
                _("...don't."),
            ],
            "flirt_lewd_slap_ass_hard_no": [
                _("Touch me again and I'll break something."),
                _("You have a death wish."),
            ],
            "flirt_lewd_pinch_ass_soft_no": [
                _("...why."),
                _("Stop."),
            ],
            "flirt_lewd_pinch_ass_hard_no": [
                _("I will hurt you."),
                _("Last warning."),
            ],
            "flirt_lewd_grab_tits_shy_yes": [
                _("...what are you doing."),
            ],
            "flirt_lewd_grab_tits_normal_yes": [
                _("...you're lucky I'm in a good mood."),
            ],
            "flirt_lewd_grab_tits_soft_no": [
                _("Hands. Off."),
                _("No."),
            ],
            "flirt_lewd_grab_tits_hard_no": [
                _("Are you trying to die?"),
                _("Touch me there again and it's over."),
            ],
            "flirt_lewd_grab_ass_soft_no": [
                _("Don't."),
                _("...really?"),
            ],
            "flirt_lewd_grab_ass_hard_no": [
                _("One more time and you'll regret it."),
                _("Keep your hands off me."),
            ],
            "flirt_lewd_compliment_tits_shy_yes": [
                _("...stop looking."),
            ],
            "flirt_lewd_compliment_tits_normal_yes": [
                _("...wow. Original."),
                _("...you done staring?"),
            ],
            "flirt_lewd_compliment_tits_soft_no": [
                _("Keep your eyes up."),
                _("Not interested in your opinion."),
            ],
            "flirt_lewd_compliment_tits_hard_no": [
                _("Say that again. I dare you."),
                _("You're disgusting."),
            ],
            "flirt_lewd_compliment_ass_shy_yes": [
                _("...were you staring this whole time?"),
            ],
            "flirt_lewd_compliment_ass_normal_yes": [
                _("...at least you have taste."),
            ],
            "flirt_lewd_compliment_ass_soft_no": [
                _("Stop looking."),
                _("Eyes up."),
            ],
            "flirt_lewd_compliment_ass_hard_no": [
                _("You're one comment away from a black eye."),
                _("Say something like that again. See what happens."),
            ],
            "flirt_lewd_ask_panties_shy_yes": [
                _("...you're insane. Fine."),
            ],
            "flirt_lewd_ask_panties_normal_yes": [
                _("...why do you even want those?"),
            ],
            "flirt_lewd_ask_panties_soft_no": [
                _("No."),
                _("Absolutely not."),
            ],
            "flirt_lewd_ask_panties_hard_no": [
                _("Ask me that again and you lose teeth."),
                _("What is wrong with you?"),
            ],

            # ── Pregnancy ──
            "pregnancy_ask_about_kids": [
                _("No."),
                _("Kids? Gross. Hard pass."),
            ],
            "pregnancy_ask_about_kids_mid": [
                _("Why are you even asking me this?"),
            ],
            "pregnancy_ask_about_kids_high": [
                _("...Don't make me say it. You already know."),
            ],
            "pregnancy_ask_about_kids_fetish": [
                _("...I want it. Don't look at me like that."),
            ],
            "pregnancy_ask_about_kids_fear": [
                _("Hard no. Don't bring it up again."),
            ],
            "pregnancy_casual_worry": [
                _("This is NOT happening to me. This can't be real."),
                _("I never wanted this. I NEVER wanted this."),
                _("I had a plan. My plan did NOT include this."),
            ],
            "pregnancy_casual_positive": [
                _("I hate this. I hate everything about this. But I don't hate you."),
                _("I refuse to be one of those moms who posts baby pictures every five minutes."),
                _("I looked at daycare prices. I think I blacked out for a second."),
            ],
        },
        "tenny": {
            # ── Safe Flirt: Joke ──
            "flirt_safe_joke_shy_yes": [
                _("That was... fine. I smiled a little. That is NOT the same as laughing."),
                _("Okay, I breathed harder through my nose. Take the win and move on."),
            ],
            "flirt_safe_joke_normal_yes": [
                _("Not terrible. I'd give it a C minus... on a generous curve."),
                _("Okay, that one caught me off guard. Don't get used to it."),
                _("Derivative, but the delivery saved it. Barely."),
            ],
            "flirt_safe_joke_enthusiastic_yes": [
                _("Okay, FINE, that was funny. Write it down, because I won't say it again."),
                _("You're improving! From a D to a solid B minus. I'm almost proud."),
                _("I actually snorted. If you tell anyone, I will deny it under oath."),
            ],
            "flirt_safe_joke_obedient_yes": [
                _("Your jokes are actually... really funny. I always look forward to them."),
                _("You always make me laugh. I don't tell you that enough."),
            ],
            "flirt_safe_joke_soft_no": [
                _("That... no. Just... maybe try workshopping that one a bit more."),
                _("I appreciate the effort more than the result. Significantly more."),
                _("Maybe comedy isn't your calling. Have you considered accounting?"),
            ],
            "flirt_safe_joke_hard_no": [
                _("Forget the standup. Focus on your studies, you're not cut out for comedy."),
                _("If that's your best material, I genuinely fear for your career prospects."),
                _("That was so unfunny it should be classified as an academic offense."),
                _("I lost brain cells listening to that. I need those. Get out."),
            ],

            # ── Safe Flirt: Touch Cheek ──
            "flirt_safe_touch_cheek_shy_yes": [
                _("W-what are you... fine. Just... be quick about it."),
                _("My face is warm. That's a physiological response, nothing more."),
            ],
            "flirt_safe_touch_cheek_normal_yes": [
                _("Your hands are warm. I'm just stating a fact, not being romantic."),
                _("Okay. That was... nice. Empirically speaking."),
            ],
            "flirt_safe_touch_cheek_enthusiastic_yes": [
                _("You always know the right spot. It's annoyingly effective."),
                _("Do that again. For... research purposes."),
            ],
            "flirt_safe_touch_cheek_soft_no": [
                _("Personal space. It's a concept. Look it up."),
                _("I'd rather you didn't. My skincare routine is very precise."),
            ],
            "flirt_safe_touch_cheek_hard_no": [
                _("Hands off. I'm not a specimen for you to examine."),
                _("Touch me again without asking and I'll rearrange your priorities."),
            ],

            # ── Safe Flirt: Hold Hands ──
            "flirt_safe_hold_hands_shy_yes": [
                _("I... okay. Just don't squeeze too hard. I need these for typing."),
                _("If anyone sees this, we were comparing hand sizes for a study."),
            ],
            "flirt_safe_hold_hands_normal_yes": [
                _("Fine. But only because my hands are cold. Don't read into it."),
                _("This is... acceptable. For the time being."),
            ],
            "flirt_safe_hold_hands_enthusiastic_yes": [
                _("Your hand fits mine perfectly. Statistically unlikely, but here we are."),
                _("Don't let go yet. I'm... still gathering data."),
            ],
            "flirt_safe_hold_hands_soft_no": [
                _("I need my hands free. I have notes to take."),
                _("Maybe later. When I'm not carrying three textbooks."),
            ],
            "flirt_safe_hold_hands_hard_no": [
                _("I'm not holding your hand in public. I have a reputation to maintain."),
                _("No. My hands have better things to do right now."),
            ],

            # ── Safe Flirt: Steal Kiss ──
            "flirt_safe_steal_kiss_shy_yes": [
                _("Did you just... I wasn't prepared. I need a moment to recalibrate."),
                _("That doesn't count. I wasn't ready. Do it again. Properly this time."),
            ],
            "flirt_safe_steal_kiss_normal_yes": [
                _("You could have asked first. Not that I'd have said no, but... protocol."),
                _("That was unexpected. And not entirely unwelcome. Don't quote me."),
            ],
            "flirt_safe_steal_kiss_enthusiastic_yes": [
                _("Bold move. I respect the initiative. Now do it again."),
                _("Best interruption I've had all semester. And I don't say that lightly."),
            ],
            "flirt_safe_steal_kiss_soft_no": [
                _("Bad timing. I just applied lip balm and I prefer not to share."),
                _("I appreciate the impulse, but I'm in the middle of a thought."),
            ],
            "flirt_safe_steal_kiss_hard_no": [
                _("Did you seriously just... no. Boundaries. Learn them."),
                _("Next time you try that without warning, I'm assigning you remedial reading."),
            ],

            # ── Safe Flirt: Hug ──
            "flirt_safe_hug_shy_yes": [
                _("I'm not a hugger. Usually. This is a one-time exception. Don't get ideas."),
                _("Don't read into this. I just... needed a break from studying."),
            ],
            "flirt_safe_hug_normal_yes": [
                _("Okay, okay. Three seconds, then let go. ...five is fine too, I guess."),
                _("You smell nice. That's an observation, not a compliment."),
            ],
            "flirt_safe_hug_enthusiastic_yes": [
                _("Get over here. I had a terrible exam day and you're the only remedy."),
                _("Tighter. I said tighter. Are you even trying?"),
            ],
            "flirt_safe_hug_soft_no": [
                _("Maybe later. I'm carrying textbooks and they'll get bent."),
                _("I appreciate the thought, but I'm not in a hugging state of mind."),
            ],
            "flirt_safe_hug_hard_no": [
                _("Physical contact isn't on my schedule right now."),
                _("I don't do unsolicited hugs. I barely do scheduled ones."),
            ],

            # ── Safe Compliment: Smart ──
            "flirt_safe_compliment_smart_shy_yes": [
                _("I... yeah. I study hard. Thank you for actually seeing that."),
                _("Most people just call me a nerd. 'Smart' is... nicer. I guess."),
            ],
            "flirt_safe_compliment_smart_normal_yes": [
                _("Obviously. But I appreciate you noticing what everyone should already know."),
                _("Smart? I'm top of my class. 'Smart' is an understatement."),
            ],
            "flirt_safe_compliment_smart_enthusiastic_yes": [
                _("Finally, someone who leads with the important compliment. Not 'cute'. Smart."),
                _("You know what I like about you? You appreciate the right things."),
            ],
            "flirt_safe_compliment_smart_soft_no": [
                _("I know I'm smart. You don't need to point it out to win points."),
                _("Flattery won't make me do your homework. Just so we're clear."),
            ],
            "flirt_safe_compliment_smart_hard_no": [
                _("Complimenting my intelligence to get something? Transparent. And insulting."),
                _("Yes, I'm smart. No, that's not an invitation for anything."),
            ],

            # ── Safe Compliment: Grades ──
            "flirt_safe_compliment_class_grades_shy_yes": [
                _("You... noticed my grades? That's actually really sweet of you."),
                _("People don't usually compliment my GPA. They just... expect it from me."),
            ],
            "flirt_safe_compliment_class_grades_normal_yes": [
                _("A 4.0 doesn't maintain itself. Discipline, routine, execution."),
                _("Thanks. I put in the work. Unlike... most people around here."),
            ],
            "flirt_safe_compliment_class_grades_enthusiastic_yes": [
                _("THIS. This is what I want to hear. Not 'nice outfit', tell me my GPA impresses you."),
                _("You just became my favorite person on campus. Temporarily."),
            ],
            "flirt_safe_compliment_class_grades_hard_no": [
                _("Good grades are the baseline, not a compliment topic."),
                _("My transcript is for grad school applications, not your pickup routine."),
            ],

            # ── Safe Compliment: Beauty / Gorgeous ──
            "flirt_safe_compliment_beauty_today_shy_yes": [
                _("You think I'm... stop. My face is doing that thing. The blushing thing."),
                _("I'm better with academic compliments. This kind short-circuits my brain."),
            ],
            "flirt_safe_compliment_beauty_today_normal_yes": [
                _("I... wasn't expecting that. I just grabbed whatever was clean this morning."),
                _("That's... thank you. I don't usually think about how I look, honestly."),
            ],
            "flirt_safe_compliment_beauty_today_enthusiastic_yes": [
                _("Smart AND gorgeous? Some of us just win the genetic lottery, I suppose."),
                _("You know what, you're right. I DO look good today. And every day, actually."),
            ],
            "flirt_safe_compliment_beauty_today_soft_no": [
                _("I'd rather you complimented my thesis abstract. But... noted, I guess."),
                _("Appearance is the least interesting metric to measure someone by."),
            ],
            "flirt_safe_compliment_beauty_today_hard_no": [
                _("I didn't get dressed this morning to be evaluated by you."),
                _("My appearance is the least interesting thing about me. Try harder."),
            ],
            "flirt_safe_compliment_gorgeous_shy_yes": [
                _("G-gorgeous? I... that's not... I need a second."),
                _("Nobody's ever called me that with a straight face before."),
            ],
            "flirt_safe_compliment_gorgeous_normal_yes": [
                _("That's... thank you. I usually get 'intimidating', not 'gorgeous'."),
                _("Okay, that one landed. I'll allow it."),
            ],
            "flirt_safe_compliment_gorgeous_enthusiastic_yes": [
                _("Gorgeous AND brilliant. The full package, clearly."),
                _("Keep talking. I could get used to this."),
            ],
            "flirt_safe_compliment_gorgeous_soft_no": [
                _("I'd prefer you admire my intellect, not my face."),
            ],
            "flirt_safe_compliment_gorgeous_hard_no": [
                _("'Gorgeous' won't get you extra credit. Try substance."),
            ],

            # ── Safe Compliment: Confidence ──
            "flirt_safe_compliment_confidence_normal_yes": [
                _("Confidence comes from preparation. I'm always prepared."),
                _("When you know your material, there's nothing to be nervous about."),
            ],
            "flirt_safe_compliment_confidence_enthusiastic_yes": [
                _("You're absolutely right I'm confident. I've earned every bit of it."),
            ],
            "flirt_safe_compliment_confidence_hard_no": [
                _("It's not confidence, it's competence. There's a difference."),
                _("I don't need validation for knowing my own worth."),
            ],

            # ── Lewd Flirt: Slap Ass ──
            "flirt_lewd_slap_ass_shy_yes": [
                _("I... that was... can you warn me next time? For... preparedness."),
            ],
            "flirt_lewd_slap_ass_normal_yes": [
                _("Did you just... I should be offended. Why am I not offended?"),
                _("That's going in my incident report. Pending... further evaluation."),
            ],
            "flirt_lewd_slap_ass_enthusiastic_yes": [
                _("Harder. That barely registered."),
                _("Good aim. You might be useful in a lab after all."),
            ],
            "flirt_lewd_slap_ass_soft_no": [
                _("That was neither appropriate nor welcome. Review the syllabus."),
            ],
            "flirt_lewd_slap_ass_hard_no": [
                _("Do that again and I'll write a thesis on your impulse control problems."),
                _("My body is not a percussion instrument. Find a drum."),
            ],

            # ── Lewd Flirt: Grab Chest ──
            "flirt_lewd_grab_tits_shy_yes": [
                _("T-that's... you're really just going for it? Okay. Okay then."),
            ],
            "flirt_lewd_grab_tits_normal_yes": [
                _("Bold hypothesis. Let's see where this experiment goes."),
                _("You could have started with dinner, but... initiative noted."),
            ],
            "flirt_lewd_grab_tits_enthusiastic_yes": [
                _("You have good instincts. Questionable timing, but good instincts."),
            ],
            "flirt_lewd_grab_tits_soft_no": [
                _("Those are attached to someone with a 4.0. Show some respect."),
            ],
            "flirt_lewd_grab_tits_hard_no": [
                _("Remove your hand before I remove your enrollment status."),
                _("That requires written consent. Which you do not have."),
            ],

            # ── Lewd Flirt: Touch Thighs ──
            "flirt_lewd_touch_thighs_shy_yes": [
                _("That's... higher than I expected. I... didn't say stop, though."),
            ],
            "flirt_lewd_touch_thighs_normal_yes": [
                _("Your hand is... distracting. I was in the middle of a thought."),
                _("Interesting placement. Continue, if you must."),
            ],
            "flirt_lewd_touch_thighs_enthusiastic_yes": [
                _("Higher. Don't be a coward about it."),
                _("You always start there. Predictable, but... effective."),
            ],
            "flirt_lewd_touch_thighs_soft_no": [
                _("My thighs are for crossing during lectures, not for that."),
            ],
            "flirt_lewd_touch_thighs_hard_no": [
                _("Restricted area. Access denied. No appeals process."),
            ],

            # ── Safe Flirt: Kiss Cheek ──
            "flirt_safe_kiss_cheek_shy_yes": [
                _("That was... unexpected input. I'll allow it. Once."),
                _("My cheek is now 3 degrees warmer. That's YOUR fault."),
            ],
            "flirt_safe_kiss_cheek_normal_yes": [
                _("A kiss on the cheek. Classic opener. Noted."),
                _("Acceptable. But don't think this grants you any extra credit."),
            ],
            "flirt_safe_kiss_cheek_enthusiastic_yes": [
                _("That was nice. Repeatable, even. Like a good experiment."),
                _("You may do that again. For data collection purposes."),
            ],
            "flirt_safe_kiss_cheek_soft_no": [
                _("Not right now. My face is for concentrating, not for kissing."),
            ],
            "flirt_safe_kiss_cheek_hard_no": [
                _("Personal space is a concept. Learn it."),
            ],

            # ── Safe Flirt: Shoulder Massage ──
            "flirt_safe_shoulder_massage_shy_yes": [
                _("My shoulders ARE tense from studying. This is... medically justified."),
                _("Okay... that actually helps. I carry all my stress here."),
            ],
            "flirt_safe_shoulder_massage_normal_yes": [
                _("The tension in my trapezius is significant. Proceed."),
                _("Good. I've been hunched over textbooks for six hours straight."),
            ],
            "flirt_safe_shoulder_massage_enthusiastic_yes": [
                _("Oh, that's exactly the right pressure. You've done your homework."),
                _("More. Right there. That knot has been there since midterms."),
            ],
            "flirt_safe_shoulder_massage_soft_no": [
                _("I don't need loosening up. I need to study."),
            ],
            "flirt_safe_shoulder_massage_hard_no": [
                _("No thanks. If I wanted a massage, I'd book a professional."),
            ],

            # ── Lewd Flirt: Pinch Ass ──
            "flirt_lewd_pinch_ass_shy_yes": [
                _("Did you just... that was NOT in any social protocol I've read!"),
            ],
            "flirt_lewd_pinch_ass_normal_yes": [
                _("A pinch. How charmingly juvenile. ...Do it again."),
                _("My glutes are toned from kickboxing. You're welcome for the quality."),
            ],
            "flirt_lewd_pinch_ass_enthusiastic_yes": [
                _("Bold. I appreciate directness. Even when it's applied to my rear."),
            ],
            "flirt_lewd_pinch_ass_soft_no": [
                _("My butt has done nothing to deserve that. Leave it alone."),
            ],
            "flirt_lewd_pinch_ass_hard_no": [
                _("Do that again and I will recalibrate your hand's trajectory. Painfully."),
            ],

            # ── Lewd Flirt: Grab Ass ──
            "flirt_lewd_grab_ass_shy_yes": [
                _("That's... a full grip. You're committed to this, apparently."),
            ],
            "flirt_lewd_grab_ass_normal_yes": [
                _("Bold data collection method. I'll allow it. For science."),
                _("Firm grip. I hope your study habits are this dedicated."),
            ],
            "flirt_lewd_grab_ass_enthusiastic_yes": [
                _("Squeeze harder. I didn't do all those squats for a gentle touch."),
            ],
            "flirt_lewd_grab_ass_soft_no": [
                _("That is NOT an appropriate way to get my attention."),
            ],
            "flirt_lewd_grab_ass_hard_no": [
                _("Remove your hand or I'll remove it for you. I know how."),
            ],

            # ── Lewd Flirt: Touch Pussy ──
            "flirt_lewd_touch_pussy_shy_yes": [
                _("You're... there?! I... my brain just stopped working entirely."),
                _("That's... oh god. My body is betraying every logical argument I prepared."),
            ],
            "flirt_lewd_touch_pussy_normal_yes": [
                _("You skipped several steps in the escalation protocol. But... continue."),
            ],
            "flirt_lewd_touch_pussy_enthusiastic_yes": [
                _("Finally. I've been calculating the probability of this for twenty minutes."),
                _("My body's response is... statistically significant. Don't stop."),
            ],
            "flirt_lewd_touch_pussy_soft_no": [
                _("That's... way too advanced for our current relationship level. Denied."),
            ],
            "flirt_lewd_touch_pussy_hard_no": [
                _("ABSOLUTELY not. That area requires a higher clearance level than you have."),
            ],

            # ── Lewd Flirt: Ask Panties ──
            "flirt_lewd_ask_panties_shy_yes": [
                _("You want my... why?! For... what purpose?! I... fine. Don't ask again."),
            ],
            "flirt_lewd_ask_panties_normal_yes": [
                _("You're collecting my underwear now? That's a strange data point. Here."),
            ],
            "flirt_lewd_ask_panties_enthusiastic_yes": [
                _("Take them. Consider it a research grant. You owe me results."),
            ],
            "flirt_lewd_ask_panties_soft_no": [
                _("My underwear stays where it is. End of discussion."),
            ],
            "flirt_lewd_ask_panties_hard_no": [
                _("What kind of degenerate request is that?! Absolutely not!"),
            ],

            # ── Confessions ──
            "confess_love_accept": [
                _("I've been running the numbers on this for weeks. Every variable points to... yes."),
                _("You know I don't say things I don't mean. So when I say I feel the same... I mean it."),
                _("I've written 50-page papers that were easier to say than this. But... me too."),
                _("I tried to rationalize this away. Multiple times. It didn't work. You win."),
                # %% on purpose: Say_Line -> renpy.say %-formats the line (old_substitutions), a lone % crashes
                _("My heart rate spikes 23%% when you're around. I calculated it. That means... yes."),
            ],
            "confess_love_reject": [
                _("I've thought about this. Extensively. And the answer is no. I'm sorry."),
                _("You deserve someone who doesn't schedule their emotions in a planner. That's not me."),
                _("I care about you. But not like that. I can't fake data, and I can't fake this."),
                _("The variables don't align for us. I'm sorry. I truly am."),
            ],

            # ── Custom: Study Chit-Chat ──
            "study_chitchat": [
                _("I just finished a 40-page paper in one sitting. I feel powerful and slightly unhinged."),
                _("The library's third floor, east corner. Best Wi-Fi on campus. Tell no one."),
                _("I color-code my notes. Yes, it's 'extra'. No, I will never stop."),
                _("Midterms are next week. I've been ready since last month."),
                _("Some people party on weekends. I reorganize my study schedule. We are not the same."),
                _("I found a typo in the textbook today. I already emailed the publisher about it."),
                _("If you need a tutor, I charge by the hour. And I am not cheap."),
                _("My planner is color-coded, tabbed, and indexed. Some call it obsessive. I call it efficient."),
                _("I don't pull all-nighters. I plan ahead. Revolutionary concept, right?"),
                _("Group projects are my villain origin story. Every. Single. Time."),
                _("I ranked every professor by grading fairness. Want to see the spreadsheet?"),
                _("Someone asked what I do for fun. I said 'flashcards'. They thought I was joking."),
                _("I read three chapters ahead. The professor hasn't even assigned chapter two yet."),
                _("My handwriting has been compared to a font. I take that as the highest compliment."),
                _("Today someone said 'C's get degrees' near me. I almost committed a crime."),
                _("I have a backup planner in case I lose my main planner. Yes, it's also color-coded."),
            ],

            # ── Custom: During Sex ──
            "during_sex_composed": [
                _("You could stand to read a book on technique. Just a suggestion."),
                _("Interesting approach. Not what I'd have chosen, but... don't stop."),
                _("I had study plans tonight. They did not include this. I'm not complaining."),
                _("For the record, I'm only here because the library closed early."),
            ],
            "during_sex_aroused": [
                _("Less talking, more... doing that thing. Whatever that was. Again."),
                _("I'm trying to analyze this objectively, but you're making it... very difficult."),
                _("This is considerably better than studying. Don't you dare quote me on that."),
                _("Faster. No, not that fast. Here, let me calculate the optimal... forget it, just go."),
            ],
            "during_sex_overwhelmed": [
                _("If you tell anyone I made that sound, I will end your academic career."),
                _("My brain usually runs nonstop. You just turned it off. How dare you."),
                _("I can't think of anything clever to say right now. That terrifies me. Keep going."),
                _("You're the only person who makes me forget what I was thinking about. I hate it. Don't stop."),
            ],

            # ── Custom: Orgasm ──
            "orgasm_react": [
                _("I... okay. I can't think of anything sarcastic right now. That's a first."),
                _("That was... I need a minute. My brain isn't functioning. This never happens to me."),
                _("Don't look so smug. This proves nothing. ...okay, it proves a little."),
                _("I hate that you're this good at this. It's statistically unfair."),
                _("I forgot what I was going to say. That literally never happens."),
                _("I'm going to need a moment to... recompile. Everything."),
                _("You just broke my train of thought. I had SEVENTEEN tabs open up here. Gone. All of them."),
            ],

            # ── Custom: Post-Scene ──
            "post_scene": [
                _("So. That happened. I'm going back to studying now. Don't follow me."),
                _("This doesn't count as a study break. This was a complete schedule deviation."),
                _("If you mention this during class, I will make your academic life very difficult."),
                _("I need to recalibrate my entire evening plan now. Worth it, but still."),
                _("Same time next week? I mean... if my schedule allows. Which it might."),
            ],
            "post_scene_love": [
                _("You know... you're the only distraction I don't mind. Don't tell anyone."),
                _("Stay a bit longer. I'll quiz you on something. Or we can just... be here."),
                _("I rescheduled my entire study block for this. I hope you understand what that means."),
                _("For someone who's not in my planner, you take up a lot of my time. I've stopped minding."),
                _("Next time... let's skip the part where I pretend I don't want to."),
            ],

            # ── Custom: Jealousy ──
            "jealousy": [
                _("Oh, you were with her? How... educational for you, I'm sure."),
                _("I noticed you talking to her. I'm not jealous. I'm merely observing a pattern."),
                _("She's nice. A bit basic, but nice. Your type, apparently."),
                _("I'm not competing with anyone. I don't need to. My transcript speaks for itself."),
                _("Go ahead, spend time with her. I'll be here. Thriving. Academically."),
                _("I don't get jealous. I get data. And the data says you're spending a lot of time with her."),
                _("Interesting. You've been 'studying' with her a lot lately. How are your grades, by the way?"),
                _("I ranked her. She's a solid 6. Out of 10. In everything. Including personality."),
            ],

            # ── Custom: Tutoring ──
            "tutoring": [
                _("Sit down, open your textbook, and try not to embarrass us both."),
                _("I'll explain this once. Pay attention. There will not be a retest."),
                _("You're smarter than you pretend to be. Stop hiding behind that lazy act."),
                _("Wrong. Try again. And actually read the question this time."),
                _("See? You CAN learn when you actually apply yourself. Revolutionary."),
                _("I'm not tutoring you because I'm nice. Watching you struggle causes me physical pain."),
            ],
            "tutoring_proud": [
                _("If you get this right, I'll consider being genuinely impressed. ...well done."),
                _("Wait. You actually studied? On your own? Who are you and what did you do with the real you?"),
                _("Your grade went up. I'm taking partial credit for that."),
            ],

            # ── Personal: Dweeb/Doofus Nicknames ──
            "nickname_dweeb": [
                _("Move it, Dweeb. Some of us have places to be."),
                _("You're staring again, Doofus. Take a picture, it lasts longer."),
                _("Whatever you say, Dweeb."),
                _("Oh please, Doofus. Like you'd know what to do."),
                _("Hey, Dweeb. You free? Not that I care, just asking."),
                _("Don't be such a Doofus about it. Think before you speak."),
                _("Dweeb. Focus. I'm talking to you."),
                _("You're lucky you're cute, Doofus. Otherwise I'd have zero patience for this."),
            ],
            "nickname_dweeb_apologize": [
                _("Whatever, Dwe... I mean... sorry. Force of habit."),
                _("Oh shut up, Doof... wait. I didn't mean... ugh, old habits."),
                _("Listen here, Dweeb... actually, sorry. I'm trying to stop that."),
                _("Okay, Doofus, you... no, hold on. Sorry. You don't deserve that anymore."),
                _("Come on, Dwe... sorry. I keep doing that. You're not... well, you're a LITTLE bit of a dweeb. But in a good way now."),
                _("I called you Dweeb again, didn't I? ...don't look at me like that. It's a term of endearment at this point."),
            ],

            # ── Personal: Family Nostalgia ──
            "family_nostalgia": [
                _("College is great, but... I miss my family sometimes. My grandpa and my cousin, we used to travel a lot during summers a few years back."),
                _("Now I have a billion reports to write instead of road trips. Adulthood is a scam."),
                _("My grandpa always said I'd do great things. I hope writing 40-page papers counts."),
                _("My cousin is an idiot. A lovable idiot, but still an idiot. I miss him though."),
                _("We used to drive across the country every summer. Me, my cousin, and my grandpa in his old RV. Best memories I have."),
                _("My grandpa is the only reason I'm not completely socially incompetent. He taught me patience. Mostly by making me deal with my cousin."),
                _("I haven't been home in two months. My grandpa keeps texting me photos of his dinner. He's adorable and terrible at technology."),
                _("My cousin would absolutely hate this campus. Too many books, not enough trouble to get into. He'd find some anyway, though."),
                _("Sometimes I wonder what my grandpa would think of... all this. College, me being on my own. He'd probably just say 'I'm proud of you, kiddo' and make something weird for dinner."),
            ],

            # ── Personal: Grandpa's Cooking ──
            "grandpa_cooking": [
                _("My grandpa used to cook the weirdest stuff on our trips. Like, things that shouldn't be food. I miss it... kind of."),
                _("You think the cafeteria is bad? My grandpa once made a smoothie with sardines and peanut butter. On PURPOSE."),
                _("I actually learned to cook because my grandpa's food was... an experience. Self-preservation, basically."),
                _("Sometimes the cafeteria smells like something my grandpa would make. That's not a compliment to the cafeteria."),
                _("My cousin and I used to rate grandpa's meals on a scale of 'edible' to 'possible war crime'. Most scored above a 7."),
            ],

            # ── Personal: Martial Arts / Fitness ──
            "fitness": [
                _("Don't test me. I have a black belt and zero patience today."),
                _("I hit the gym at 6 AM. Before most people even open their eyes, I've already done more than they'll do all day."),
                _("Martial arts taught me discipline. Also how to drop someone twice my size. Both are useful in college."),
                _("You think I'm just books and grades? I can bench press my own body weight. Respect the full package."),
                _("I do yoga on Tuesdays and kickboxing on Thursdays. Balance in all things."),
                _("My cousin used to think he could beat me in a fight. He stopped thinking that around age 14."),
                _("Working out clears my head. When I'm stressed about exams, thirty minutes of hitting a bag fixes everything."),
                _("People underestimate me because I carry textbooks. Those textbooks are heavy. My arms are not decorative."),
            ],

            # ── Personal: Competitive (non-academic) ──
            "competitive": [
                _("I don't play games to have fun. I play to WIN. Fun is a side effect of victory."),
                _("Bet you I can finish this faster than you. Loser buys coffee."),
                _("Second place is just the first loser. My grandpa taught me that. Actually no, I figured that out myself."),
                _("You want to challenge me? At ANYTHING? Bold. Stupid, but bold."),
                _("I keep score of everything. Don't ask what the current tally is. You won't like it."),
                _("I once stayed up until 3 AM to beat a puzzle game because it said 'average completion time: 2 hours'. I did it in 47 minutes."),
                _("Racing to class? Sure. I'm already winning and we haven't started yet."),
                _("I turned doing laundry into a speed competition against myself. My record is 4 minutes flat, sorting included."),
            ],

            # ── Personal: Guilty Pleasures ──
            "guilty_pleasure": [
                _("If you tell anyone I watch that show, I will destroy you. Academically and personally."),
                _("I... may have eaten an entire bag of gummy bears during my last study session. It was for focus. Sugar helps the brain."),
                _("I have a playlist of pop songs that I will deny owning until my dying breath."),
                _("Sometimes I read trashy romance novels between research papers. For... pacing analysis. Narrative structure."),
                _("I know every episode of that reality dating show. It's sociological research. Don't judge me."),
                _("I spent three hours customizing my character in a video game last night. It's not procrastination if it's... spatial reasoning practice."),
                _("I own more scented candles than any serious academic should. My room smells like vanilla and poor life choices."),
                _("I unironically enjoy terrible puns. If you EVER repeat that, I'll deny it."),
            ],

            # ── Personal: Morning Routine ──
            "morning_routine": [
                _("You slept until WHEN? That's not sleeping in, that's a coma."),
                _("I've been up since 5. I've already worked out, showered, reviewed my notes, and had breakfast. You just woke up. We are not the same."),
                _("My morning routine is non-negotiable. 5 AM alarm, no snooze. Snoozing is for people without ambition."),
                _("How do people function after waking up at 9? Half the day is GONE."),
                _("I have my entire morning scheduled in 15-minute blocks. Deviation is not an option."),
                _("Coffee at 5:15, stretching at 5:30, review notes at 5:45. Like clockwork. Like a functional adult."),
                _("If my morning routine gets disrupted, my entire day is off. Yes, I know that sounds intense. No, I don't care."),
                _("My alarm goes off and I'm UP. Immediately. None of that 'five more minutes' weakness."),
            ],

            # ── Pregnancy ──
            "pregnancy_ask_about_kids": [
                _("I-I don't know... I never really thought about it."),
            ],
            "pregnancy_ask_about_kids_mid": [
                _("I think I'd want to, with someone who cares about me."),
                _("Maybe? If you wanted?"),
            ],
            "pregnancy_ask_about_kids_high": [
                _("If you wanted a family with me... I'd be so happy."),
            ],
            "pregnancy_ask_about_kids_fetish": [
                _("I want babies so bad... please don't think I'm weird."),
            ],
            "pregnancy_ask_about_kids_fear": [
                _("I-I'm so scared of that... what if something goes wrong?"),
            ],
            "pregnancy_casual_worry": [
                _("What about my studies? I-I can't drop out..."),
                _("My parents are going to panic at first. But my grandpa always said he'd help me with anything."),
                _("I'm scared, but... it's not the end of the world, right?"),
            ],
            "pregnancy_casual_positive": [
                _("At least I have you. And my grandpa. We can make this work, right?"),
                _("My grandpa sent a huge care package... baby clothes, books, even a tiny lab coat."),
                _("I've been planning my schedule around the due date."),
            ],
        },
    }
