# ============================================================
# story_steps.rpy... the STEPS of a girl with a story (docs/plan_role_situations.md): stats unlock, events open
#
# A girl with a story (a role in STORY_LADDERS: today the stepmom, Shion) climbs STEPS. Campus girls have none
# (story_key None): nothing here touches them.
#   - Each step OPENS a list of acts (STORY_LADDERS, they add up). An act of a step above hers is refused whatever
#     her stats (story_act_locked): the button stays, she answers with her step's line (story_locked_line). Money,
#     a girlfriend's permission and blackmail can't open it either (_deny_or_blackmail): blackmail only works inside
#     her step.
#   - Inside her step the usual approval decides (Love / Obed / Inbt with each act's weights).
#   - Her stats rise the usual ways (talk, gifts, compliments, flirts, the acts she likes, event choices) up to her
#     step's CEILING: what goes past it rises at STORY_CAP_SLOW (story_stat_gain, Change_Status). The ceiling of a
#     stat = the lowest limit of an unlock route on that stat + STORY_CAP_MARGIN.
#   - The UNLOCK EVENT of her step (STORY_UNLOCKS) is the only door to the next one. It plays when a ROUTE passes
#     (its "routes": a stat and its limit; "blackmail" = the leverage of his videos of her; the Obed route counts her
#     turn points too, STORY_BREAK_OBED) and the event fits where / when he is. The route with the most room plays
#     (story_unlock_route); the scene reads store._story_route_now. story_step_up is the ONLY writer of the step.
#   - STEP EVENTS (STORY_STEP_EVENTS: her role's list + her own, by step; "girl 1 = A B C, girl 2 = A D E F") raise
#     stats and give flavor between unlocks. A step's list is where an event exists: a one-off one she missed is gone
#     once the step changes; a repeatable one is listed on every step where it can play.
#   - Inside an event, a CHOICE of his tests one stat (story_test): it passes at STORY_TEST_SHARE of that stat's
#     unlock route limit at her step, and pays that stat (story_choice_reward, STORY_CHOICE_GAIN). Love = she wants
#     him, Obed = he leads and she follows, Inbt = she takes the risk. A MOMENT (STORY_MOMENTS, label story_moment)
#     is lines + three such choices, one per stat; the Sunday dinner plays one, a step event can be one.
#   - An unlock event whose scene ASKS him (her invitation) and gets a no gives her step back (story_unlock_cancel):
#     the event waits its "cooldown" and asks again.
#   - EVIDENCE (girl._story_evidence, an event's "evidence"): proof of a secret of hers he got in her story (Shion: the
#     bar where she runs the Hashimoto clan). It is the "evidence" route of an unlock, it counts on the "blackmail"
#     route (STORY_EVIDENCE_VALUE), and it is one more choice in his blackmail picker (_blackmail_attempt), with her
#     own lines (STORY_EVIDENCE, label story_evidence_blackmail). Like any blackmail, only inside her step.
# Triggers: "location" (location_menu, every menu: navigation.rpy), "dinner" (the Sunday dinner of the father's
# house, shion_family.rpy: label _apartment_dinner_weekly), "sleep" (he goes to bed in his dorm room: do_sleep,
# actions.rpy), "sex" (a tick of a sex scene: sub_event_tick, SubEvents.rpy, played as the sub-event "story"),
# "text" (a time slot changes: Wait 6zz4, system_time.rpy; she texts him), "downtown_night" (he leaves the father's
# apartment at Night, sent away by her curfew: shion_family.rpy), "morning" (once a morning: Wait 6zz5;
# an event that takes him somewhere sets _story_morning_moved, and Wait returns as with the activity buddy).
# A restricted scene of her story (one finish ends it, the clock waits, nobody walks in): label story_restricted_scene.
# Scenes: an event plays its "scene" (STORY_SCENES: open / one version per route / close, label story_route_scene)
# and / or its "label". Lines are (who, line): who None = narration, "@player" = him, "@husband" = her husband
# (girl_husband), "@<key>" = a man of her story (STORY_NPCS), "" = her voice with no face (she is not on screen),
# else her face (label story_say); "%s" = her name. Two directive entries (never dialogue, never _()):
# ("@walk", "") = she crosses the screen left to right (story_walk_by: the nights he follows her), and
# ("@bg", "bg <name>") = the scene moves under the lines (she reaches another street: "bg jptown").
# Her femdom turn (femdom_turn.rpy) reads her step as its stage (femdom_stage); its points feed the Obed route.
# QA: renpy.jump("qa_story_menu") in the console.
# ============================================================

default _story_route_now = None         # the route of the unlock event playing now ("love" / "obed" / ...)
default _story_bm_demand = None         # the coerced unlock's demand HE picked (STORY_EVENTS "bm_demands"), or None = scripted
default _story_rolled = set()           # (gid, event, Day, TimeIndex, location): a step event's chance, rolled once there
default _story_sex_event = None         # the "sex" event sub_event_tick picked (SubEvent_Handle "story")
default _story_morning_moved = False    # a "morning" event took him somewhere (Wait returns after it)
default _story_event_now = None         # the event story_event_play is playing (its labels read it)
default _story_hint_last = {}           # gid -> the Day of her last unlock hint (story_unlock_hint)
default _story_hint_turn = {}           # gid -> how many "far" hints she gave (they take her routes in turn)

init python:

    # gid or "role:<role>" -> one entry per step: "acts" = what THIS step opens (they add up)
    STORY_LADDERS = {
        "role:stepmom": (
            # "chitchat": the GLOBAL small talk topics she still has on that step (her own topics always); a step
            # without it has them all (story_global_topic_ok, ChitChat.rpy pick_chitchat_func)
            {"id": "cold",        "acts": (),
             "chitchat": ("chitchat_whats_up",)},
            # "outing" = going out with him (the Follow me invite, _girl_accepts_invite)
            {"id": "she_decides", "acts": ("flirt", "touch", "kiss", "masturbate", "hj", "outing")},
            {"id": "giving_in",   "acts": ("oral", "bj", "tj", "fj", "sex", "rj", "cum_mouth")},
            # "shower_masturbate" = he finds her masturbating in her shower (Shower_Entry's random event)
            {"id": "his",         "acts": ("shower_masturbate",)},
            # "raw" = sex with no condom: going in bare, the condom coming off (his ask, his hands, hers, a tear).
            # "date" = the romantic dinner date (restaurant_girl_accepts, the goodbye kiss): a married woman seen
            # out with him is the last wall to fall (author, 2026-10-10). The friends dinner is the act "outing".
            # "voice": the step whose lines she speaks (story_voice_id): past her last unlock she is still "his"
            {"id": "surrender",   "voice": "his", "acts": ("anal", "raw", "cum_inside", "pill_stop", "netori", "date")},
        ),
    }

    # The card's word for each act a step opens (plan_shion_agency F4, "This step opened: ...").
    # An act without a word stays off the card. Short nouns, same register as the achievements screen.
    STORY_ACT_NAMES = {
        "flirt": _("Flirting"), "touch": _("Touch"), "kiss": _("Kisses"), "masturbate": _("Private shows"),
        "hj": _("Her hands"), "outing": _("Outings"),
        "oral": _("Oral"), "bj": _("Her mouth"), "tj": _("Her chest"), "fj": _("Her feet"),
        "sex": _("Sex"), "rj": _("Rimjob"), "cum_mouth": _("Finishing in her mouth"),
        "shower_masturbate": _("Her shower time"),
        "anal": _("Anal"), "raw": _("No protection"), "cum_inside": _("Finishing inside"),
        "pill_stop": _("The pill"), "netori": _("Netori nights"), "date": _("Dates"),
    }

    # The name of each step on her card (screen_girl_status.rpy)
    STORY_STEP_NAMES = {
        "cold":        _("Keeping her distance"),
        "she_decides": _("She decides"),
        "giving_in":   _("Giving in"),
        "his":         _("Yours"),
        "surrender":   _("Surrender"),
    }

    # gid or "role:<role>" -> {step: the event that opens the next step}. Her own entry beats her role's.
    STORY_UNLOCKS = {
        "role:stepmom": {0: "hand_under_table", 1: "vent_night", 2: "marital_bed", 3: "drugged_dinner"},
    }

    # gid or "role:<role>" -> {step: (event, ...)}: the step events. Her role's list and her own add up.
    STORY_STEP_EVENTS = {}

    # The catalog (stepmom_story.rpy and the files of each story fill it):
    #   "trigger"   when it is asked for ("location")
    #   "label"     the scene, called with (girl); "<label>_<gid>" is played instead when it exists
    #   "meet"      she must be where he is
    #   "where"     the places he must be in
    #   "visit"     she comes to him (not angry): she is moved where he is before the
    #               scene; "knock" = a narration line said before she appears
    #   "alone"     nobody else where he is;  "apart": she is NOT where he is (a text)
    #   "slot_min" / "slot_max"   TimeIndex range
    #   "once"      plays once; "cooldown" days between two; "chance" per place / slot (rolled once there),
    #               "chance_per" = {stat: chance per point} added to it (she texts more the more she loves him)
    #   "weight"    among the step events that fit; "requires" = name of a function (girl) -> bool
    #   "planned"   it was arranged (an invitation): never held back by STORY_DAY_CAP, never counts in it
    #   "scene"     a STORY_SCENES key, played first; "moment" a STORY_MOMENTS key, played next; then "label"
    #               (one of the three at least)
    #   "leaves"    she goes home after it (a visit to his room)
    #   "follows"   (event, days): plays only once that event of hers was seen, at least `days` days before (a chain)
    #   "evidence"  after it she knows he has this much proof of her secret (girl._story_evidence)
    #   "routes"    an unlock event only: ((route, {stat: limit}), ...); stat = "Love" / "Obed" / "Inbt" /
    #               "blackmail" (his leverage, 0-10) / "evidence" (girl._story_evidence)
    STORY_EVENTS = {}

    # key -> {gid or "role:<role>" -> {"open": lines, "routes": {route: lines}, "default": route, "close": lines}}
    STORY_SCENES = {}

    # key -> {gid or "role:<role>" -> {"lines": lines, "choices": [{"stat", "menu", "say", "pass", "fail"}] (one per
    # stat), "after": lines}}. "say" = his line (None: the menu is an action of his), "pass" / "fail" = what follows
    STORY_MOMENTS = {}

    # The men of her story who speak in its lines ("@<key>"): key -> (name, color)
    STORY_NPCS = {}

    # Her proof as blackmail (story_evidence_blackmail): gid -> {"menu": his picker entry, "first" / "again": the
    # threat, "accept" / "fail": what follows}. Its weight against an act: STORY_EVIDENCE_VALUE (a video counts 1-6)
    STORY_EVIDENCE = {}
    STORY_EVIDENCE_VALUE = 8

    # A concrete act / flirt / cum key -> the act of the ladder it belongs to. A key that is not here is its own
    # act; an act no step lists is never locked (chat, compliments, jokes, gifts).
    STORY_ACT_OF = {
        # his hands on her, her clothes, the physical flirts
        "touch_thighs": "touch", "touch_ass": "touch", "touch_tits": "touch", "touch_pussy": "touch",
        "strip_minor": "touch", "strip_top": "touch", "strip_bottom": "touch",
        "slap_ass": "touch", "pinch_ass": "touch", "grab_tits": "touch", "grab_ass": "touch", "ask_panties": "touch",
        "sunscreen_thighs": "touch", "sunscreen_ass": "touch",
        "hug": "touch", "hold_hands": "touch", "touch_cheek": "touch", "shoulder_massage": "touch",
        "kiss_cheek": "kiss", "steal_kiss": "kiss",
        "touch_massage": "touch",
        # her selfie on his phone (phone_photos.rpy _photo_decide): flirt-tier, the poses scale with their acts
        "photo": "flirt",
        # her number in his phone (_ask_phone_number): on her cold step she gives him nothing
        "phone_number": "flirt",
        # showering together, either direction: his ask when he finds her, her walk-in on him (actions.rpy)
        "shower_join": "sex",
        # a pet name between them (his for her, hers for him), not the name of the family ("only_types": Boy, Stepmom)
        "petname": "touch",
        # the talk flirts: a joke, a compliment (any compliment_<x>: STORY_ACT_PREFIX)
        "joke": "flirt",
        "rub": "sex", "tip": "sex",
        "tip_anal": "anal", "cum_inside_anal_ask": "anal", "cum_in_mouth_from_anal_ask": "anal",
        "cum_in_mouth_ask": "cum_mouth",
        "cum_inside_ask": "cum_inside", "condom_break_accept": "cum_inside",
        # the condom coming off: her ok after he came (_post_cum_condom_menu "Ask to go raw", _cum_warn_her_condom)
        "cum_remove_condom_ask": "raw",
    }

    # A sub-event of a scene -> the act it is (sub_event_dispatch skips the ones her step locks)
    STORY_SUBEVENT_ACT = {
        "anal_request": "anal",
        "atm_initiative": "anal",
        "creampie": "cum_inside",
        "ntr_request_creampie": "cum_inside",
        "netori_call": "netori",
        # she takes the condom off, asks him to, or someone else asks for it
        "condom_force": "raw",
        "condom_ask": "raw",
        "condom_hate_cum": "raw",
        "watcher_condom_remove": "raw",
        "ntr_request_raw": "raw",
    }

    STORY_CAPPED_STATS = ("Love", "Obed", "Inbt")
    STORY_CAP_MARGIN = 100      # a stat's ceiling = the lowest limit of an unlock route on it + this
    STORY_CAP_SLOW = 0.25       # what goes past the ceiling rises at this speed
    STORY_BREAK_OBED = 4        # one point of her femdom turn (_femdom_break) = this much Obed on the Obed route
    STORY_DAY_CAP = 1           # step events (not unlocks) a girl has in a day
    STORY_TEST_SHARE = 0.5      # a choice's test passes at this share of the stat's unlock route limit (story_test)
    STORY_CHOICE_GAIN = {True: 12, False: 3}    # the tested stat after a choice that passed / failed

    # Her answer when nothing of hers or her role's speaks (story_locked_line / rod_flirt_line)
    STORY_LOCKED_FALLBACK = [
        _("Not yet. Don't push it."),
        _("Slow down. We're not there."),
        _("No. Not until I say so."),
    ]
    # What the player learns from it (sex_deny_with_temptation): her step, or her husband in the room
    STORY_LOCKED_HINT = _("She won't go there yet, whatever her mood. Something has to happen between you two first.")
    STORY_LOCKED_HINT_FAR = _("That was way too far. You barely have that kind of relationship. She lost respect for you.")
    STORY_LOCKED_HINT_ABSURD = _("Are you insane? Asking for that at this point is beyond disrespectful. She's furious.")
    STORY_HUSBAND_HINT = _("Not with her husband in the room. Get her alone first.")

    # ── where she is on her story ──

    def story_key(girl):
        """The key of her ladder: her gid, else her role's ("role:stepmom"), else None (a campus girl)."""
        _gid = getattr(girl, "gid", None)
        if _gid in STORY_LADDERS:
            return _gid
        _rk = girl_role_key(girl) if girl is not None else None
        return _rk if _rk in STORY_LADDERS else None

    def story_girls():
        """The girls with a story who are not away."""
        return [_g for _g in girls_reachable() if story_key(_g)]

    def story_step(girl):
        """Her step (0 without a story)."""
        if story_key(girl) is None:
            return 0
        return int(getattr(girl, "_story_step", 0) or 0)

    def story_last_step(girl):
        """The index of her ladder's LAST step (the stepmom's "surrender" = 4), or -1 without a story. The gate of
        CANON_BREAK_RULES (characters_stats.rpy) reads it: a canon trait only breaks past the final step."""
        _key = story_key(girl)
        return len(STORY_LADDERS[_key]) - 1 if _key else -1

    def story_step_id(girl):
        """The id of her step ("cold" / ...), or None."""
        _key = story_key(girl)
        if _key is None:
            return None
        _lad = STORY_LADDERS[_key]
        return _lad[min(story_step(girl), len(_lad) - 1)]["id"]

    def story_voice_id(girl):
        """The step whose voice pools she speaks ("talk_greet.<id>", "afterscene.<id>", her shower): her step's
        "voice" (a step that opens acts but keeps the lines of the one before), else her step id. None: no story."""
        _key = story_key(girl)
        if _key is None:
            return None
        _lad = STORY_LADDERS[_key]
        _st = _lad[min(story_step(girl), len(_lad) - 1)]
        return _st.get("voice", _st["id"])

    def story_step_name(girl):
        """Her step's name on her card (translated), or None."""
        _sid = story_step_id(girl)
        return _tl(STORY_STEP_NAMES.get(_sid, _sid)) if _sid else None

    # Concrete keys that start like this -> the act they are (a key of STORY_ACT_OF wins)
    STORY_ACT_PREFIX = (("compliment_", "flirt"),)

    def story_act_group(act):
        _act = str(act)
        if _act in STORY_ACT_OF:
            return STORY_ACT_OF[_act]
        return next((_g for _p, _g in STORY_ACT_PREFIX if _act.startswith(_p)), _act)

    def story_global_topic_ok(girl, func):
        """A global small talk topic she can bring up on her step (the step's "chitchat" list; no list = all)."""
        _key = story_key(girl)
        if _key is None:
            return True
        _allowed = STORY_LADDERS[_key][min(story_step(girl), len(STORY_LADDERS[_key]) - 1)].get("chitchat")
        return _allowed is None or getattr(func, "__name__", "") in _allowed

    def _story_act_need(key, act):
        """The step that opens this act on this ladder, or None (no step lists it: never locked)."""
        _grp = story_act_group(act)
        for _i, _step in enumerate(STORY_LADDERS[key]):
            if _grp in _step["acts"]:
                return _i
        return None

    def story_lock_gap(girl, act):
        """How many steps above hers the act sits (0 = not locked by step, 1+ = locked). Husband-only blocks
        return 0 (she CAN do it, he is just in the room). Used by the penalty in sex_deny_with_temptation."""
        _key = story_key(girl)
        if _key is None or not act:
            return 0
        _need = _story_act_need(_key, act)
        if _need is None:
            return 0
        return max(0, _need - story_step(girl))

    def story_act_locked(girl, act):
        """THE rule: she has a story and this act opens on a step above hers, or her husband is in the room with them
        (nothing of her ladder happens in front of him: husband_in_room, family_father.rpy). She refuses it whatever
        her stats."""
        _key = story_key(girl)
        if _key is None or not act:
            return False
        _need = _story_act_need(_key, act)
        if _need is None:
            return False
        return story_step(girl) < _need or husband_in_room(girl)

    def story_act_open(girl, act):
        """She has a story and her step opened this act (her pill, the netori call): a campus girl never has."""
        _key = story_key(girl)
        if _key is None:
            return False
        _need = _story_act_need(_key, act)
        return _need is not None and story_step(girl) >= _need

    def story_scene_act(action, anal=False):
        """The act of a scene launch / a sex menu denial (start_scene, _deny_or_blackmail): "sex" + anal = anal."""
        if anal and action == "sex":
            return "anal"
        if anal and action == "tip":
            return "tip_anal"
        return action

    # Love penalty when the player asks for an act many steps above her current one:
    # gap 1 = normal rejection (she just says no), gap 2 = insulting (Love loss), gap 3 = outrageous (big Love loss)
    STORY_LOCK_GAP_PENALTY = {
        1: {},
        2: {"Love": -15},
        3: {"Love": -25},
    }

    def story_lock_result(girl, act):
        """The refusal of an act her step locks, shaped like an ApprovalCheck result (outcome "story_locked"), or
        None when it is not locked. Read by the checks of the sex menu, the flirts and the cum permissions."""
        if not story_act_locked(girl, act):
            return None
        _hb = husband_in_room(girl)
        _gap = story_lock_gap(girl, act)
        print("[STORY] %s refuses %s (act %s) at step %d %s, gap %d%s" % (
            girl.gid, act, story_act_group(act), story_step(girl), story_step_id(girl), _gap, ", her husband is here" if _hb else ""))
        return {
            "score": 0, "tier": 0, "accepted": False,
            "outcome": "story_locked", "reason_primary": "story_locked",
            "reason_secondary": None, "reasons": ["story_locked"],
            "is_cheating": False, "cheating_state": None,
            "debug": {"story_act": str(act), "story_step": story_step(girl), "husband_here": _hb, "story_gap": _gap},
        }

    def story_first_step(girl):
        """She is on the FIRST step of her story (the stepmom's "cold"): nothing of him yet. Her locked refusals
        carry no promise there: no "not yet" smile, no "behave, he's watching" complicity."""
        return story_key(girl) is not None and story_step(girl) == 0

    def _story_locked_traits(girl):
        """Her traits that may color a locked refusal ("<mood>.<trait>" pools), with the guards of
        _sex_response_line: public-only traits in public, camera traits while he records, partner traits with an
        NPC partner. Her femdom turn stage (femdom_stage_mod) counts as one and comes first."""
        _in_public = _is_public_location()
        _has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        _traits = [_t for _t in (getattr(girl, "traits", None) or ())
                   if not (_t in _LOCATION_BOUND_TRAITS and not _in_public)
                   and not (_t in _BF_BOUND_TRAITS and not _has_bf)
                   and not (_t in _RECORDING_BOUND_TRAITS and not getattr(store, "_recording_active", False))]
        _stage = femdom_stage_mod(girl)
        return ([_stage] if _stage else []) + _traits

    def story_locked_line(girl, act):
        """Her answer to an act her step locks (English: the caller says it). Her own GIRL_SEX_LINES, then her
        role's. Moods, most specific first: "story_locked.husband_here.<step id>" then "story_locked.husband_here"
        when her husband is in the room (never the shared husband pool on her FIRST step: its "not in front of him"
        is complicity, and nothing exists yet to hide), then "story_locked.<step id>", then "story_locked" (the
        step moods only when her step locks the act too). Each mood tries her traits first ("<mood>.<trait>",
        girl_sex_voice_trait_line), for the act, then its ladder act, then "_any"."""
        # The author's exception (2026-10-11) to the no-reveal-on-denial rule: an anal_lover whose act
        # is still locked TEASES the refusal ("maybe one day I'll even let you...") instead of a flat
        # no. The step stays shut; only the tone changes. Never in front of her husband.
        if (act in ("anal", "tip_anal") and not husband_in_room(girl)
                and hasattr(girl, "has_trait") and girl.has_trait("anal_lover")):
            _alt = rod_pick_line(girl, "anal_locked_tease", default=None)
            if _alt:
                girl.discover("discovered_trait_anal_lover")
                return _alt
        _sid = story_step_id(girl)
        _moods = ["story_locked.%s" % _sid, "story_locked"]
        if husband_in_room(girl):
            # her husband is the reason first; the line of her step only if her step locks it too
            _hb_moods = ["story_locked.husband_here.%s" % _sid]
            if not story_first_step(girl):
                _hb_moods.append("story_locked.husband_here")
            _need = _story_act_need(story_key(girl), act)
            _moods = _hb_moods + (_moods if (_need is not None and story_step(girl) < _need) else [])
        _traits = _story_locked_traits(girl)
        for _mood in _moods:
            for _a in (str(act), story_act_group(act), "_any"):
                _tid, _line = girl_sex_voice_trait_line(girl, _a, _mood, _traits)
                _line = _line or girl_sex_voice_line(girl, _a, _mood)
                if _line:
                    # a CONTROL trait is overt in the tone of her refusal ("Know your place, boy"): the
                    # preference traits keep the no-reveal-on-denial rule (audit 2026-10-04)
                    if _tid in ("femdom", "submissive") and girl.has_trait(_tid):
                        girl.discover("discovered_trait_%s" % _tid)
                    return _line
        return renpy.random.choice(STORY_LOCKED_FALLBACK)

    # ── her step's voice outside the locks: the first word of the day, a gift, the follow invite, the afterglow ──

    STORY_AFTER_DAYS = 2        # days an unlock's route colors her first word of the day (talk_greet.after)

    # The faces of her step voice (only the faces every girl has)
    _STORY_STEP_FACE = {"cold": "normal", "she_decides": "smug", "giving_in": "sexy", "his": "happy"}
    _STORY_ROUTE_FACE = {"love": "shy", "inbt": "normal", "obed": "smug", "blackmail": "angry", "evidence": "angry"}

    def story_rod_line(girl, keys):
        """The first rod_lines pool among `keys` with lines, her own block before her role's: a line, or None.
        A key that ends in a CONTROL trait ("talk_greet.cold.femdom") is that trait speaking: discover it
        (preference traits keep the no-reveal-on-denial rule)."""
        for _blk in (rod_lines.get(getattr(girl, "gid", None) or "", {}), rod_lines.get(girl_role_key(girl) or "", {})):
            for _k in keys:
                if _blk.get(_k):
                    _tid = _k.rsplit(".", 1)[-1]
                    if _tid in ("femdom", "submissive") and hasattr(girl, "has_trait") and girl.has_trait(_tid):
                        girl.discover("discovered_trait_%s" % _tid)
                    return renpy.random.choice(_blk[_k])
        return None

    def _story_keys_with_traits(girl, base):
        """["<base>.<trait>", ...] then "<base>" (the traits of _story_locked_traits, same guards)."""
        return ["%s.%s" % (base, _t) for _t in _story_locked_traits(girl)] + [base]

    def story_step_route(girl):
        """The route that opened her CURRENT step, or None (step 0, or a step moved without one: QA, femdom sync)."""
        return (getattr(girl, "_story_routes", None) or {}).get(story_step(girl))

    def story_talk_greet_line(girl):
        """Her first word when he opens the talk, once a day: (face, line) or None. The STORY_AFTER_DAYS days after
        an unlock, the route that opened the step speaks first ("talk_greet.after.<step>.<route>")."""
        if story_key(girl) is None or getattr(girl, "_story_greet_day", None) == store.Day:
            return None
        _sid = story_voice_id(girl)
        _route = story_step_route(girl)
        _keys, _face = [], _STORY_STEP_FACE.get(_sid, "normal")
        _ud = getattr(girl, "_story_unlock_day", None)
        if _route and _ud is not None and 0 <= store.Day - _ud <= STORY_AFTER_DAYS and story_step(girl) > 0:
            _keys += ["talk_greet.after.%s.%s" % (_sid, _route), "talk_greet.after.%s" % _sid]
            _face = _STORY_ROUTE_FACE.get(_route, _face)
        _keys += _story_keys_with_traits(girl, "talk_greet.%s" % _sid)
        _line = story_rod_line(girl, _keys)
        if _line:
            girl._story_greet_day = store.Day
            print("[STORY] %s: her first word of the day (step %s, route %s)" % (girl.gid, _sid, _route))
        return (_face, _line) if _line else None

    def story_gift_line(girl):
        """Her step's word for a gift from HIM (give_gift), once a day: (face, line) or None."""
        if story_key(girl) is None or getattr(girl, "_story_gift_day", None) == store.Day:
            return None
        _sid = story_voice_id(girl)
        _line = story_rod_line(girl, _story_keys_with_traits(girl, "gift_react.%s" % _sid))
        if _line:
            girl._story_gift_day = store.Day
            print("[STORY] %s: her step's word for his gift (%s)" % (girl.gid, _sid))
        return (_STORY_STEP_FACE.get(_sid, "normal"), _line) if _line else None

    def story_outing_accept_say(girl):
        """Her own word when she agrees to follow him (the act "outing"), said here: True when she had one."""
        if story_key(girl) is None:
            return False
        _line = story_rod_line(girl, _story_keys_with_traits(girl, "outing_accept.%s" % story_voice_id(girl)))
        if not _line:
            return False
        set_scene_expression(girl, "smug", pose="standing")
        Say_Line(girl, _tl(_line))
        set_scene_expression(girl, "normal", pose="standing")
        return True

    # ── the unlock event and its routes ──

    def story_unlock_event(girl):
        """The event that opens her next step, or None (her last step)."""
        _key = story_key(girl)
        if _key is None:
            return None
        _step = story_step(girl)
        for _k in (getattr(girl, "gid", None), _key):
            _ev = STORY_UNLOCKS.get(_k, {}).get(_step)
            if _ev:
                return _ev
        return None

    def story_route_score(girl, stat):
        """What a route reads: her stat; Obed + her turn points; his blackmail leverage; her evidence."""
        if stat == "blackmail":
            return min(10, _calc_blackmail_leverage(girl) + story_evidence(girl) * STORY_EVIDENCE_VALUE)
        if stat == "evidence":
            return int(getattr(girl, "_story_evidence", 0) or 0)
        _v = int(getattr(girl, stat, 0) or 0)
        if stat == "Obed":
            _v += int(getattr(girl, "_femdom_break", 0) or 0) * STORY_BREAK_OBED
        return _v

    def story_unlock_routes(girl):
        """The routes of her unlock event: ((route, {stat: limit}), ...)."""
        _ev = story_unlock_event(girl)
        return STORY_EVENTS.get(_ev, {}).get("routes", ()) if _ev else ()

    # ── the route lock (author, 2026-10-09: "na primeira rota, deve ir ate o fim"): the FAMILY of the route
    # that opened her FIRST step is her story's lane, to the end. The stat routes (love / obed / inbt) are one
    # family, winning her over: inside it each unlock still takes the stat with the most room. The material
    # lane (evidence, then blackmail) is the other. Locked = later unlocks and their hints only offer her
    # lane. Derived from _story_routes (no new save state): a declined unlock pops its route
    # (story_unlock_cancel) and frees the lock again; a step moved with no route (QA, sync) locks nothing. ──
    _STORY_ROUTE_FAMILY = {"love": "stats", "obed": "stats", "inbt": "stats",
                           "evidence": "blackmail", "blackmail": "blackmail"}

    def story_route_family(route):
        """The lane of a route ("stats" / "blackmail"); an unknown route is its own lane."""
        return _STORY_ROUTE_FAMILY.get(route, route)

    def story_route_lock(girl):
        """Her story's lane, from the first REAL route among her unlocks; None before one (every route open).
        The tools' pseudo-routes never lock a lane ("qa": the QA menu's story_step_up; "forced":
        story_event_play played an unlock with nothing passing): they are no family, so a step moved by them
        keeps the story free, as the lock's comment promises."""
        _routes = getattr(girl, "_story_routes", None) or {}
        for _step in sorted(_routes):
            if _routes[_step] in _STORY_ROUTE_FAMILY:
                return story_route_family(_routes[_step])
        return None

    def story_qualifying_lanes(girl):
        """The lane families whose routes pass at her unlock right now, the lock IGNORED: what he could
        pick from if the pick were his (story_event_play's lane menu)."""
        _lanes = set()
        for _route, _needs in story_unlock_routes(girl):
            _rooms = [story_route_score(girl, _st) / float(max(1, _lim)) for _st, _lim in _needs.items()]
            if _rooms and min(_rooms) >= 1.0:
                _lanes.add(story_route_family(_route))
        return _lanes

    def story_unlock_route_of_lane(girl, lane):
        """The best passing route INSIDE one lane family (the same most-room rule as story_unlock_route)."""
        _best, _best_room = None, 0.0
        for _route, _needs in story_unlock_routes(girl):
            if story_route_family(_route) != lane:
                continue
            _rooms = [story_route_score(girl, _st) / float(max(1, _lim)) for _st, _lim in _needs.items()]
            if _rooms and min(_rooms) >= 1.0 and min(_rooms) > _best_room:
                _best, _best_room = _route, min(_rooms)
        return _best

    def story_unlock_route(girl):
        """The route that opens her next step now: of the routes of her LANE (story_route_lock) that pass, the
        one with the most room (score / limit). None: no route passes yet."""
        _best, _best_room = None, 0.0
        _lock = story_route_lock(girl)
        for _route, _needs in story_unlock_routes(girl):
            if _lock and story_route_family(_route) != _lock:
                continue
            _rooms = [story_route_score(girl, _st) / float(max(1, _lim)) for _st, _lim in _needs.items()]
            if _rooms and min(_rooms) >= 1.0 and min(_rooms) > _best_room:
                _best, _best_room = _route, min(_rooms)
        return _best

    # ── the hint of her unlock (author 2026-10-06): the moment of her unlock came (its trigger and every condition of
    #    its own: the Sunday dinner, the night he goes to bed while her husband is home, the morning her husband is
    #    away) and no route of it passed. The step does not move by chance: the unlock plays the first time that moment
    #    comes with a route at its limit, so the hint tells him what is missing, one narration line (label
    #    story_unlock_hint_say). A route at STORY_HINT_CLOSE of its limit (its weakest stat) is "close" and wins (the
    #    closest one); with none close, the "far" hints take her routes in turn, so he hears of every way in. ──
    STORY_HINT_COOLDOWN = 5     # days between two hints for the same girl (tester 2026-10-11: "not every
                                # single morning"; his build predates the cooldown, this widens it anyway)
    STORY_HINT_CLOSE = 0.7      # share of a route's limit from which its hint says "close"
    # gid or "role:<role>" -> {step id: {route: {"far": line, "close": line}}} (stepmom_story.rpy fills the role's;
    # her own entry beats her role's, story_data). A route with no "close" line uses its "far" one.
    STORY_HINTS = {}

    # Short, direct hints for the girl status screen (one per step, no spoilers): gid or "role:<role>" ->
    # {step id: line, or {lane: line} by her locked lane ("stats" / "blackmail", story_route_lock)}
    STORY_STATUS_HINTS = {}

    def story_unlock_hint(trigger, girl=None):
        """(girl, line) at a hint moment, or None. Two voices, one per girl per STORY_HINT_COOLDOWN days:
        - the moment of her unlock came for this trigger and nothing happened (no route passes, every other
          condition holds): a far / close route hint (STORY_HINTS);
        - she is READY (a route of her unlock already passes, only its moment or its own conditions are
          missing): her step's "ready" line (STORY_STATUS_HINTS, the same one her card shows), at ANY hint
          moment. The player never needs the menu to know the next move (author, 2026-10-09)."""
        _girls = [girl] if girl is not None else story_girls()
        for _g in _girls:
            _ev = story_unlock_event(_g)
            if not _ev:
                continue
            _last = store._story_hint_last.get(_g.gid)
            if _last is not None and store.Day - _last < STORY_HINT_COOLDOWN:
                continue
            _ready = story_unlock_route(_g) is not None
            # the event waits its "cooldown" (he turned it down, story_unlock_cancel): no "she is ready, do it
            # again" the next morning (tester 2026-10-12: the vent night nudged him back every day)
            _seen = (getattr(_g, "_story_seen", None) or {}).get(_ev)
            if _ready and _seen is not None and store.Day - _seen < STORY_EVENTS.get(_ev, {}).get("cooldown", 0):
                print("[STORY] %s: READY nudge held, %s waits its cooldown (seen Day %d)" % (_g.gid, _ev, _seen))
                continue
            if STORY_EVENTS.get(_ev, {}).get("trigger") != trigger or _ready:
                # not her moment, or ready (at her moment the unlock itself plays): the ready nudge, in play.
                # Ready at her own trigger means the event's OTHER conditions failed (a "requires" like the B
                # exam, the husband home): the line still says what is missing.
                if not _ready:
                    continue
                _srh = (story_data(STORY_STATUS_HINTS, _g, {}) or {}).get(story_step_id(_g))
                _srh_line = _srh.get("ready") if isinstance(_srh, dict) else None
                if not _srh_line:
                    continue
                store._story_hint_last[_g.gid] = store.Day
                print("[STORY] %s: READY nudge at %s (step %s, %s)" % (_g.gid, trigger, story_step_id(_g), _ev))
                return (_g, _srh_line)
            if not _story_event_fits(_g, _ev, trigger):
                continue
            _table = (story_data(STORY_HINTS, _g, {}) or {}).get(story_step_id(_g), {})
            _rooms = []
            _lock = story_route_lock(_g)
            for _route, _needs in story_unlock_routes(_g):
                # her lane only (story_route_lock): a hint must never teach a route her story closed
                if _lock and story_route_family(_route) != _lock:
                    continue
                if _route in _table:
                    _rooms.append((_route, min(story_route_score(_g, _st) / float(max(1, _lim)) for _st, _lim in _needs.items())))
            if not _rooms:
                continue
            _close = [_r for _r in _rooms if _r[1] >= STORY_HINT_CLOSE]
            if _close:
                _route, _room = max(_close, key=lambda _r: _r[1])
                _tier = "close"
            else:
                _n = store._story_hint_turn.get(_g.gid, 0)
                _route, _room = _rooms[_n % len(_rooms)]
                store._story_hint_turn[_g.gid] = _n + 1
                _tier = "far"
            _lines = _table[_route]
            _line = _lines.get(_tier) or _lines.get("far")
            if not _line:
                continue
            store._story_hint_last[_g.gid] = store.Day
            print("[STORY] %s: unlock hint at %s (step %s, %s): route %s at %d%% (%s); routes %s" % (
                _g.gid, trigger, story_step_id(_g), _ev, _route, int(_room * 100), _tier,
                ", ".join("%s %d%%" % (_r, int(_x * 100)) for _r, _x in _rooms)))
            return (_g, _line)
        return None

    def story_stat_cap(girl, stat):
        """Her ceiling on this stat at her step, or None (no route of her step reads it)."""
        _lims = [_needs[stat] for _route, _needs in story_unlock_routes(girl) if stat in _needs]
        return (min(_lims) + STORY_CAP_MARGIN) if _lims else None

    def story_stat_gain(target, flavor, old, amount):
        """Change_Status: a gain past her step's ceiling rises at STORY_CAP_SLOW (exact: the carry keeps the
        fraction). Everything else is untouched."""
        if amount <= 0 or flavor not in STORY_CAPPED_STATS or story_key(target) is None:
            return amount
        _cap = story_stat_cap(target, flavor)
        if _cap is None or old + amount <= _cap:
            return amount
        _free = max(0, _cap - old)
        _carry = getattr(store, "_stat_gain_carry", None)
        if _carry is None:
            store._stat_gain_carry = _carry = {}
        _key = "%s.%s.cap" % (target.gid, flavor)
        _exact = (amount - _free) * STORY_CAP_SLOW + _carry.get(_key, 0.0)
        _slow = int(_exact + 1e-9)
        _carry[_key] = _exact - _slow
        print("[STORY] %s %s +%d past her ceiling %d (step %d): +%d (carry %.2f)" % (
            target.gid, flavor, amount, _cap, story_step(target), _free + _slow, _carry[_key]))
        # The slowdown stays (the author 2026-10-10: grinding past it is allowed, just slow), but the
        # FIRST slowed gain of each step tells the player the real door is the story now, not the grind
        _hinted = getattr(store, "_story_cap_hinted", None)
        if _hinted is None:
            store._story_cap_hinted = _hinted = set()
        _hkey = (target.gid, story_step(target))
        if _hkey not in _hinted:
            _hinted.add(_hkey)
            renpy.notify(_tl(_("%s barely reacts to this anymore. Her story is waiting for its next step.")) % target.Name)
        return _free + _slow

    def story_test(girl, stat):
        """A choice of his inside an event, on one stat: passes when her route score on it reaches STORY_TEST_SHARE of
        the lowest unlock route limit on that stat at her step. Always passes when no route of her step reads it."""
        _lims = [_needs[stat] for _route, _needs in story_unlock_routes(girl) if stat in _needs]
        if not _lims:
            print("[STORY] %s: test %s passes (no route of step %d reads it)" % (girl.gid, stat, story_step(girl)))
            return True
        _need = int(min(_lims) * STORY_TEST_SHARE)
        _score = story_route_score(girl, stat)
        print("[STORY] %s: test %s %d / %d -> %s" % (girl.gid, stat, _score, _need, _score >= _need))
        return _score >= _need

    def story_choice_reward(girl, stat, passed):
        """What a choice pays: the tested stat (through Change_Status: her persona, her ceiling)."""
        Change_Status(girl, stat, STORY_CHOICE_GAIN[bool(passed)])

    def story_scene_data(girl, key):
        """Her version of a STORY_SCENES scene: her role's, with her own parts on top (her "open" / "close" /
        "default" replace the role's, her "routes" add to them or replace one). {} if none."""
        _sc = STORY_SCENES.get(key, {})
        _role = _sc.get(girl_role_key(girl)) or {}
        _own = _sc.get(getattr(girl, "gid", None)) or {}
        if not _own:
            return _role
        _out = dict(_role)
        _out.update(dict((_k, _v) for _k, _v in _own.items() if _k != "routes"))
        _routes = dict(_role.get("routes", {}))
        _routes.update(_own.get("routes", {}))
        _out["routes"] = _routes
        return _out

    def story_data(table, girl, default=None):
        """Her entry in a story table keyed by gid or role ("role:<role>"): her own, else her role's, else default."""
        return table.get(getattr(girl, "gid", None)) or table.get(girl_role_key(girl)) or default

    def story_moment_data(girl, key):
        """Her version of a STORY_MOMENTS moment (None if none)."""
        return story_data(STORY_MOMENTS.get(key, {}), girl)

    def story_unlock_cancel(girl, event):
        """He said no to her unlock event (its scene asked him): she goes back to the step she was on. story_event_play
        marked the event seen today, so it waits its "cooldown" before asking again. With story_step_up, the only
        writers of _story_step."""
        _step = story_step(girl)
        _routes = dict(getattr(girl, "_story_routes", None) or {})
        _routes.pop(_step, None)
        girl._story_routes = _routes
        girl._story_step = max(0, _step - 1)
        print("[STORY] %s: he turned %s down, back to step %d" % (girl.gid, event, girl._story_step))

    def story_evidence(girl):
        """The proof of her secret he holds (0 = none): only a girl with lines for it (STORY_EVIDENCE)."""
        if getattr(girl, "gid", None) not in STORY_EVIDENCE:
            return 0
        return int(getattr(girl, "_story_evidence", 0) or 0)

    def story_npc_char(key):
        """The speaker of a man of her story ("@<key>" lines, STORY_NPCS)."""
        _name, _color = STORY_NPCS.get(key, (key, "#cbd5e1"))
        return Character(_tl(_name), who_color=_color)

    def story_husband_char(girl):
        """The speaker of her husband's lines ("@husband"): a Character with his name and color."""
        _h = girl_husband(girl)
        return Character(_h.Name, who_color=_h.color) if _h is not None else narrator

    def story_step_up(girl, route, event):
        """Her next step: the ONLY writer of girl._story_step (the unlock event, story_event_play)."""
        _old = story_step(girl)
        _top = len(STORY_LADDERS[story_key(girl)]) - 1
        girl._story_step = min(_top, _old + 1)
        _routes = dict(getattr(girl, "_story_routes", None) or {})
        _routes[girl._story_step] = route
        girl._story_routes = _routes
        girl._story_unlock_day = store.Day      # the days right after it read the route (story_talk_greet_line)
        print("[STORY] %s: step %d -> %d (%s) by %s, route %s" % (
            girl.gid, _old, girl._story_step, story_step_id(girl), event, route))

    # ── step events ──

    def story_events_for(girl):
        """The step events of her step: her role's list, then her own."""
        _key = story_key(girl)
        if _key is None:
            return []
        _step = story_step(girl)
        _out = []
        for _k in (_key, getattr(girl, "gid", None)):
            for _ev in STORY_STEP_EVENTS.get(_k, {}).get(_step, ()):
                if _ev not in _out:
                    _out.append(_ev)
        return _out

    def _story_event_fits(girl, ev, trigger):
        """This event can play now for her (not its routes, not its chance)."""
        _e = STORY_EVENTS.get(ev)
        if not _e or _e.get("trigger") != trigger:
            return False
        if _e.get("meet") and girl.loc != store.CurrentLocation:
            return False
        if _e.get("where") and store.CurrentLocation not in _e["where"]:
            return False
        if _e.get("visit") and girl.has_temp_status("angry"):
            return False
        if _e.get("alone") and any(_o is not girl and _o.loc == store.CurrentLocation for _o in ALL_GIRLS):
            return False
        if _e.get("apart") and girl.loc == store.CurrentLocation:
            return False
        if not (_e.get("slot_min", 0) <= store.TimeIndex <= _e.get("slot_max", 99)):
            return False
        _seen = (getattr(girl, "_story_seen", None) or {}).get(ev)
        if _seen is not None:
            if _e.get("once"):
                return False
            if store.Day - _seen < _e.get("cooldown", 0):
                return False
        _fol = _e.get("follows")
        if _fol:
            _prev = (getattr(girl, "_story_seen", None) or {}).get(_fol[0])
            if _prev is None or store.Day - _prev < _fol[1]:
                return False
        _req = _e.get("requires")
        if _req and not globals()[_req](girl):
            return False
        return True

    def _story_events_today(girl):
        _d = getattr(girl, "_story_day", None) or (0, 0)
        return _d[1] if _d[0] == store.Day else 0

    def story_event_now(trigger, girl=None):
        """(girl, event) that plays now for this trigger, or None. Her unlock event first (a route passes and it
        fits), then the step events that fit, her day not full, their chance rolled once per place and slot."""
        _girls = [girl] if girl is not None else story_girls()
        for _g in _girls:
            _ev = story_unlock_event(_g)
            if _ev and _story_event_fits(_g, _ev, trigger) and story_unlock_route(_g):
                return (_g, _ev)
        for _g in _girls:
            _full = _story_events_today(_g) >= STORY_DAY_CAP
            _cands = []
            for _ev in story_events_for(_g):
                if _full and not STORY_EVENTS.get(_ev, {}).get("planned"):
                    continue
                if not _story_event_fits(_g, _ev, trigger):
                    continue
                _chance = story_event_chance(_g, _ev)
                if _chance < 1.0:
                    _roll_key = (_g.gid, _ev, store.Day, store.TimeIndex, store.CurrentLocation)
                    if _roll_key in store._story_rolled:
                        continue
                    store._story_rolled.add(_roll_key)
                    if renpy.random.random() >= _chance:
                        continue
                _cands.append((_ev, STORY_EVENTS[_ev].get("weight", 1)))
            if _cands:
                # a "priority" event that fits never loses the draw to flavor (the Hashimoto nights, author
                # 2026-10-09: catching her must be 100%): only the priority ones stay in it
                _prio = [_c for _c in _cands if STORY_EVENTS.get(_c[0], {}).get("priority")]
                if _prio:
                    _cands = _prio
                _roll = renpy.random.randint(1, sum(_w for _e, _w in _cands))
                for _ev, _w in _cands:
                    _roll -= _w
                    if _roll <= 0:
                        return (_g, _ev)
        return None

    def story_event_chance(girl, ev):
        """The chance of a step event where it fits: its "chance" + its "chance_per" stats (1.0 at most)."""
        _e = STORY_EVENTS.get(ev, {})
        _c = _e.get("chance", 1.0) + sum(int(getattr(girl, _st, 0) or 0) * _k for _st, _k in _e.get("chance_per", {}).items())
        return min(1.0, _c)

    def story_sync(why):
        """Load / new game: a save made while the femdom turn moved her stage by points keeps that stage as her
        step (the larger of the two). The rolls of past days are dropped."""
        for _g in ALL_GIRLS:
            if story_key(_g) is None:
                continue
            _old = int(getattr(_g, "_femdom_stage", 0) or 0)
            if _old > story_step(_g):
                _g._story_step = min(_old, len(STORY_LADDERS[story_key(_g)]) - 1)
                print("[STORY] %s: %s, her old turn stage %d is her step now" % (_g.gid, why, _old))
        store._story_rolled = set(_k for _k in store._story_rolled if _k[2] >= store.Day)

# ============================================================
# An event of her story (location_menu and the other triggers): an unlock event moves her step BEFORE its scene,
# so the scene reads its route (store._story_route_now) and the acts of the new step are open in it
# ============================================================
label story_event_play(girl, ev):
    python:
        _sep = STORY_EVENTS[ev]
        _sep_unlock = (ev == story_unlock_event(girl))
        # an unlock forced with no route passing (QA) plays the scene's default version
        store._story_route_now = (story_unlock_route(girl) or "forced") if _sep_unlock else None
        store._story_event_now = ev
        # The coercion lanes never fire themselves (plan_shion_agency F1): brandishing what he has on
        # her is ALWAYS a choice. Holding it cancels nothing forever: the event waits its own cooldown
        # and offers again. Universal: any story, any girl, both lanes (his videos and her secret).
        _sep_hold = False
        _sep_lane_picked = False
        store._story_bm_demand = None
        # a "visit" unlock (she knocks: vent_night) asks nothing up front (tester 2026-10-11: the menu
        # popped before he even knew she was at the door); its own flow carries the decline
        if _sep_unlock and not _sep.get("visit") and story_route_lock(girl) is None and len(story_qualifying_lanes(girl)) > 1:
            # The LANE is his call, never the biggest number's (tester 2026-10-11: he gathered the
            # evidence, love outgrew it, and the auto-pick buried the coercion lane before the first
            # lock). With BOTH families passing and no lock yet, he picks the family; his pick then
            # locks the lane as always (story_step_up records the route).
            _sep_lane_picked = True
            if renpy.display_menu([
                    (_tl(_("Use what you have on her.")), True),
                    (_tl(_("Win her over. Keep what you have out of it.")), False)]):
                store._story_route_now = story_unlock_route_of_lane(girl, "blackmail") or store._story_route_now
            else:
                store._story_route_now = story_unlock_route_of_lane(girl, "stats") or store._story_route_now
            print("[STORY] %s: unlock %s, HE picked the lane -> %s" % (girl.gid, ev, store._story_route_now))
        if _sep_unlock and store._story_route_now in ("blackmail", "evidence") and not _sep.get("visit"):
            if not _sep_lane_picked:
                _sep_hold = renpy.display_menu([
                    (_tl(_("Use what you have on her.")), False),
                    (_tl(_("Keep what you have to yourself, for now.")), True),
                ])
            # On the coerced lanes HE names the demand (the tester's point: the leverage was his, the
            # menu was hers). "bm_demands" lists the choices (first entry = the scripted night);
            # "demand_late" asks inside the event instead, at its natural beat. Consent routes keep
            # the scene as written: she is offering, not paying.
            if not _sep_hold and _sep.get("bm_demands") and not _sep.get("demand_late"):
                store._story_bm_demand = renpy.display_menu(
                    [(_tl(_bd_cap), _bd_mode) for _bd_cap, _bd_mode in _sep["bm_demands"]])
            print("[STORY] %s: unlock %s via %s lane -> %s (demand %s)" % (
                girl.gid, ev, store._story_route_now, "HELD" if _sep_hold else "used", store._story_bm_demand))
    if _sep_hold:
        python:
            _sep_seen = dict(getattr(girl, "_story_seen", None) or {})
            _sep_seen[ev] = Day
            girl._story_seen = _sep_seen
            store._story_route_now = None
            store._story_event_now = None
        $ Narration(_("You leave it buried. If something is going to happen between you two, it will not start with a threat. ...For now."))
        return
    python:
        _sep_seen = dict(getattr(girl, "_story_seen", None) or {})
        _sep_seen[ev] = Day
        girl._story_seen = _sep_seen
        if _sep_unlock:
            story_step_up(girl, store._story_route_now, ev)
        elif not _sep.get("planned"):
            girl._story_day = (Day, _story_events_today(girl) + 1)
        _sep_label = _sep.get("label")
        if _sep_label and renpy.has_label("%s_%s" % (_sep_label, girl.gid)):
            _sep_label = "%s_%s" % (_sep_label, girl.gid)
        _sep_visit = bool(_sep.get("visit")) and girl.loc != CurrentLocation
        print("[STORY] %s: event %s (%s, step %d, route %s, label %s)" % (
            girl.gid, ev, "unlock" if _sep_unlock else "step event", story_step(girl), store._story_route_now, _sep_label))
    if _sep_visit:
        # she came to him: the knock first, then she is there
        if _sep.get("knock"):
            if store.TimeIndex != NIGHT_INDEX:
                $ store.TimeIndex = NIGHT_INDEX
            $ renpy.scene()
            $ renpy.show(get_bg_for_location())
            play sound "audio/Knock.mp3" noloop
            $ Narration(_sep["knock"])
        $ girl.loc = CurrentLocation
        call Set_Scene(entry=True) from _call_Set_Scene_story_visit
    if _sep.get("scene"):
        call story_route_scene(girl, _sep["scene"]) from _call_story_route_scene_event
    if _sep.get("moment"):
        call story_moment(girl, story_moment_data(girl, _sep["moment"])) from _call_story_moment_event
    if _sep_label:
        call expression _sep_label pass (girl) from _call_story_event_label
    if _sep.get("evidence"):
        python:
            girl._story_evidence = max(story_evidence(girl), int(_sep["evidence"]))
            unlock_achievement("what_she_hides")
            print("[STORY] %s: he has proof of her secret now (evidence %d)" % (girl.gid, girl._story_evidence))
    if _sep.get("leaves"):
        python:
            girl.loc = girl_home_loc(girl)
            hide_girl_sprite(girl)
            print("[STORY] %s goes home after %s (%s)" % (girl.gid, ev, girl.loc))
    python:
        # her ladder is complete: the lane that carried her story names the achievement (story_route_lock).
        # Checked HERE, after her label ran: a declined unlock already took its step back (story_unlock_cancel)
        if story_step(girl) >= len(STORY_LADDERS[story_key(girl)]) - 1:
            _sep_lane = story_route_lock(girl)
            if _sep_lane == "stats":
                unlock_achievement("won_her_heart")
            elif _sep_lane == "blackmail":
                unlock_achievement("under_your_thumb")
    $ store._story_route_now = None
    $ store._story_bm_demand = None
    return

# A moment (STORY_MOMENTS): its lines, his choice (one per stat), what follows, the stat it pays, its "after"
label story_moment(girl, m):
    if m:
        call story_say(girl, m.get("lines")) from _call_story_say_moment
        python:
            _smo_pick = renpy.display_menu([(_tl(_c["menu"]), _i) for _i, _c in enumerate(m["choices"])])
            _smo_c = m["choices"][_smo_pick]
            _smo_ok = story_test(girl, _smo_c["stat"])
            print("[STORY] %s: moment, he picks %s -> %s" % (girl.gid, _smo_c["stat"], _smo_ok))
        if _smo_c.get("say"):
            $ Say_Player(_smo_c["say"])
        # her FIRST step may answer colder ("pass_first" / "fail_first"): no complicity before her initiative
        $ _smo_key = "pass" if _smo_ok else "fail"
        $ _smo_lines = (_smo_c.get(_smo_key + "_first") if story_first_step(girl) else None) or _smo_c[_smo_key]
        call story_say(girl, _smo_lines) from _call_story_say_moment_choice
        $ story_choice_reward(girl, _smo_c["stat"], _smo_ok)
        call story_say(girl, m.get("after")) from _call_story_say_moment_after
    return

# A restricted scene of her story: the clock waits (time_lock), nobody walks in. His finish does not end it: the
# post-cum menu like any scene (_scene_cum_continues; author, 2026-10-09: of her story only the marital bed ends on
# it). "sex" goes through condom_check first: no condom she accepts = her no_condom lines, then no_condom_act instead
# (never anal). Ends on the room redrawn
label story_restricted_scene(girl, kind, pos=None, no_condom=None, no_condom_act=("bj", None), anal=False):
    python:
        _srsc_kind, _srsc_pos, _srsc_anal = kind, pos, anal
        if _srsc_pos and not girl_has_pose(girl, _srsc_pos):
            _srsc_pos = _rear_pose_for(girl)
        time_lock()
        store._scene_restricted = True
        store._scene_cum_continues = True
        store.door_locked = True
        store._interruption_happened = True
        store._witness_check_done = True
        store._npc_witness_check_done = True
        store._condom_removed_midscene = False
        store._creampie_consent = False
        store._player_exposed_this_session = False
        session_cum_reset()
        _scene_exit_flags_reset()
        print("[STORY] %s: restricted scene %s %s" % (girl.gid, _srsc_kind, _srsc_pos))
    if _srsc_kind == "sex":
        call condom_check(girl, False, "soft_deny") from _call_condom_check_story
        if store.condom_denied:
            call story_say(girl, no_condom) from _call_story_say_no_condom
            $ _srsc_kind, _srsc_pos = no_condom_act
            $ _srsc_anal = False
    if _srsc_kind == "sex":
        call start_scene(girl, "sex", _srsc_pos, _srsc_anal) from _call_start_scene_story_sex
    else:
        call start_scene(girl, _srsc_kind) from _call_start_scene_story_act
    python:
        store._scene_restricted = False
        store._scene_cum_continues = False
        store._scene_angry_abort = False
        store._player_exhausted = False
        store.door_locked = False
        store._interruption_happened = False
        store._witness_check_done = False
        store._npc_witness_check_done = False
        time_unlock()
    call Set_Scene(entry=True) from _call_Set_Scene_story_after
    return

# His blackmail with her proof (_blackmail_attempt, when he picks it): the same check as a video (_blackmail_check,
# STORY_EVIDENCE_VALUE), her own lines. Sets _blackmail_accepted / _blackmail_failed as the video blackmail does
label story_evidence_blackmail(girl, action):
    python:
        _seb = STORY_EVIDENCE.get(girl.gid, {})
        # "first" only the first time he threatens her with it, whatever she answered then
        _seb_first = not (getattr(girl, "_story_evidence_used", 0) or getattr(girl, "_story_evidence_refused", 0))
        _seb_bm = _blackmail_check(girl, action, video_value=STORY_EVIDENCE_VALUE)
        print("[STORY] %s: blackmail with her proof for %s (first %s): %s" % (girl.gid, action, _seb_first, _seb_bm.get("accepted")))
    call story_say(girl, _seb.get("first" if _seb_first else "again")) from _call_story_say_evidence_threat
    if _seb_bm["accepted"]:
        python:
            store._blackmail_accepted = True
            girl._blackmail_times = getattr(girl, "_blackmail_times", 0) + 1
            girl._story_evidence_used = getattr(girl, "_story_evidence_used", 0) + 1
            Change_Status(girl, "Obed", 10)
            Change_Status(girl, "Inbt", 5)
        call story_say(girl, _seb.get("accept")) from _call_story_say_evidence_accept
    else:
        python:
            store._blackmail_failed = True
            girl._story_evidence_refused = getattr(girl, "_story_evidence_refused", 0) + 1
            blackmail_note_refused(girl, "story_evidence")
            Change_Status(girl, "Love", -10)
            Change_Status(girl, "Obed", -10)
            girl.set_temp_status("angry", days=2, reason="blackmail_failed")
        call story_say(girl, _seb.get("fail")) from _call_story_say_evidence_fail
    return

# A STORY_SCENES scene: its opening, the version of the route that opened it (store._story_route_now; its "default"
# otherwise), its closing
label story_route_scene(girl, key):
    python:
        _srs = story_scene_data(girl, key)
        _srs_route = store._story_route_now if store._story_route_now in _srs.get("routes", {}) else _srs.get("default")
        print("[STORY] %s: scene %s, route %s (now %s)" % (girl.gid, key, _srs_route, store._story_route_now))
    call story_say(girl, _srs.get("open")) from _call_story_say_open
    if _srs_route:
        call story_say(girl, _srs["routes"][_srs_route]) from _call_story_say_route
    call story_say(girl, _srs.get("close")) from _call_story_say_close
    return

# Plays (who, line) lines: None = narration, "@player" = him, "@husband" = her husband, else her face. "%s" = her name
# The hint of her unlock (story_unlock_hint): one narration line when its moment came and nothing happened.
# Called where each trigger runs: the two dinners (shion_family.rpy), his bed (do_sleep), the morning (Wait 6zz5).
label story_unlock_hint_say(trigger, girl=None):
    $ _suh = story_unlock_hint(trigger, girl)
    if _suh is not None:
        $ Narration(_suh[1])
    return

# ── She crosses the screen, left to right (the "@walk" directive: the nights he follows her). Her standing
# sprite at the NORMAL sprite height and size (yalign 2.0, the slot transforms of images.rpy: the legs sink
# past the screen's bottom edge, as in every scene), tinted into a night figure (TintMatrix: the dark coat);
# the beat is skippable (a click cuts it short, the hide still runs). ──
transform story_walk_lr(t=3.4):
    subpixel True
    xanchor 0.5
    yalign 2.0
    yoffset 0
    matrixcolor TintMatrix("#6b7191")
    xpos -0.25
    linear t xpos 1.25

label story_walk_by(girl):
    $ set_girl_sprite(girl, pose="standing", at_list=[story_walk_lr()])
    $ renpy.pause(3.0)
    $ hide_girl_sprite(girl)
    return

label story_say(girl, lines):
    $ _ssy = list(lines or [])
    while _ssy:
        python:
            _ssy_who, _ssy_line = _ssy.pop(0)
            _ssy_text = _tl_fmt(_ssy_line, girl.Name) if "%s" in _ssy_line else _ssy_line
        if _ssy_who is None:
            $ Narration(_ssy_text)
        elif _ssy_who == "@player":
            $ Say_Player(_ssy_text)
        elif _ssy_who == "@husband":
            $ renpy.say(story_husband_char(girl), _tl(_ssy_text))
        elif _ssy_who == "@walk":
            # directive: she crosses the screen (the line part is ignored)
            call story_walk_by(girl) from _call_story_walk_by
        elif _ssy_who == "@bg":
            # directive: the scene moves under the lines (the line IS the image, e.g. "bg jptown")
            scene expression _ssy_text
            with dissolve
        elif _ssy_who.startswith("@"):
            $ renpy.say(story_npc_char(_ssy_who[1:]), _tl(_ssy_text))
        elif _ssy_who == "":
            # her voice, far from him: no face, no sprite
            $ Say_Line(girl, _ssy_text)
        else:
            $ set_scene_expression(girl, _ssy_who, pose=None if _girl_in_sex_scene(girl) else "standing")
            $ Say_Line(girl, _ssy_text)
    return

# Her first word of the day when he opens the talk (talk_main): her step's voice; the STORY_AFTER_DAYS days after an
# unlock, the route that opened the step (story_talk_greet_line)
label _story_talk_greet(girl):
    $ _stg = story_talk_greet_line(girl)
    if _stg:
        $ set_scene_expression(girl, _stg[0], pose="standing")
        $ Say_Line(girl, _tl(_stg[1]))
        $ set_scene_expression(girl, "normal", pose="standing")
    return

# One line after a normal scene with her (start_scene, steps 2+): the route that opened her step colors the afterglow
# ("afterscene.<step>.<route>" in her GIRL_SEX_LINES / her role's), once a day. Restricted scenes have their own ends
label _story_afterscene(girl, act):
    python:
        _saf = None
        if getattr(girl, "_story_after_day", None) != store.Day:
            _saf_sid = story_voice_id(girl)
            _saf_route = story_step_route(girl)
            # her trait variants first (_story_keys_with_traits, minus the base): the post-flip
            # "afterscene.his.submissive" voice must beat the route that opened the step; then the
            # route's afterglow, then the plain step key
            _saf_moods = (_story_keys_with_traits(girl, "afterscene.%s" % _saf_sid)[:-1]
                          + (["afterscene.%s.%s" % (_saf_sid, _saf_route)] if _saf_route else [])
                          + ["afterscene.%s" % _saf_sid])
            for _saf_m in _saf_moods:
                for _saf_a in (str(act), "_any"):
                    _saf = girl_sex_voice_line(girl, _saf_a, _saf_m)
                    if _saf:
                        break
                if _saf:
                    break
            if _saf:
                girl._story_after_day = store.Day
                # a control-trait variant spoke: that IS the trait showing (same rule as story_rod_line)
                _saf_tid = _saf_m.rsplit(".", 1)[-1]
                if _saf_tid in ("femdom", "submissive") and hasattr(girl, "has_trait") and girl.has_trait(_saf_tid):
                    girl.discover("discovered_trait_%s" % _saf_tid)
                print("[STORY] %s: afterglow line (step %s, route %s, act %s)" % (girl.gid, _saf_sid, _saf_route, act))
    if _saf:
        $ Say_Line(girl, _tl(_saf))
    return

# ============================================================
# QA (console: renpy.jump("qa_story_menu")): her step, her routes, the events (developer menus, not translated)
# ============================================================
label qa_story_menu:
    python:
        _qs_girls = [_g for _g in ALL_GIRLS if story_key(_g)]
        if not _qs_girls:
            renpy.say(None, "No girl with a story.")
            renpy.jump("main_loop")
        _qs_girl = _qs_girls[0] if len(_qs_girls) == 1 else renpy.display_menu([(_g.Name, _g) for _g in _qs_girls])
    while True:
        python:
            _qs_lines = ["%s: step %d (%s), routes taken %s" % (
                _qs_girl.Name, story_step(_qs_girl), story_step_id(_qs_girl), getattr(_qs_girl, "_story_routes", {}))]
            _qs_lines.append("Unlock: %s, route now: %s" % (story_unlock_event(_qs_girl), story_unlock_route(_qs_girl)))
            for _qs_r, _qs_n in story_unlock_routes(_qs_girl):
                _qs_lines.append("  %s: %s" % (_qs_r, ", ".join("%s %d/%d" % (_st, story_route_score(_qs_girl, _st), _lim) for _st, _lim in _qs_n.items())))
            _qs_lines.append("Ceilings: %s" % ", ".join("%s %s" % (_st, story_stat_cap(_qs_girl, _st)) for _st in STORY_CAPPED_STATS))
            _qs_lines.append("Locked: %s" % ", ".join(sorted(set(
                _a for _s in STORY_LADDERS[story_key(_qs_girl)] for _a in _s["acts"] if story_act_locked(_qs_girl, _a)))))
            _qs_lines.append("Step events: %s" % (", ".join(story_events_for(_qs_girl)) or "-"))
            if "femdom" in GIRLS_CONFIG.get(_qs_girl.gid, {}).get("traits", ()):
                _qs_lines.append("Canon femdom: gate %s, control count %d, gate_opened %s, canon_lost %s, corruption %s" % (
                    "OPEN" if trait_canon_breakable(_qs_girl, "femdom") else "closed",
                    getattr(_qs_girl, "CorruptionFemdomRefused", 0), getattr(_qs_girl, "_femdom_gate_opened", False),
                    sorted(getattr(_qs_girl, "_canon_lost", None) or ()), getattr(store, "corruption_enabled", False)))
            renpy.say(None, "\n".join(_qs_lines))
            _qs_pick = renpy.display_menu([
                ("Step +1", "up"), ("Step -1", "down"),
                ("Stats to the first route of her unlock", "stats"),
                ("Play her unlock event now", "unlock"),
                ("Play a step event now", "event"),
                ("Go to her final step", "final"),
                ("Control count +15 (through the counter)", "count15"),
                ("Toggle corruption_enabled", "corr"),
                ("Toggle sugar arrangement", "sugar"),
                ("Exit", "exit"),
            ])
            if _qs_pick == "up":
                story_step_up(_qs_girl, "qa", "qa_story_menu")
            elif _qs_pick == "down":
                _qs_girl._story_step = max(0, story_step(_qs_girl) - 1)
                print("[STORY] QA: %s back to step %d" % (_qs_girl.gid, _qs_girl._story_step))
            elif _qs_pick == "stats":
                for _qs_r, _qs_n in story_unlock_routes(_qs_girl)[:1]:
                    for _st, _lim in _qs_n.items():
                        if _st in STORY_CAPPED_STATS:
                            setattr(_qs_girl, _st, max(getattr(_qs_girl, _st, 0), _lim))
                print("[STORY] QA: %s stats set for her first route" % _qs_girl.gid)
            elif _qs_pick == "final":
                _qs_girl._story_step = story_last_step(_qs_girl)
                print("[STORY] QA: %s to her final step %d" % (_qs_girl.gid, _qs_girl._story_step))
            elif _qs_pick == "count15":
                # through the real counter: the gate freeze / fresh-zero / corruption firing all apply
                for _qs_i in range(15):
                    _femdom_count_refusal(_qs_girl, "qa")
            elif _qs_pick == "corr":
                store.corruption_enabled = not getattr(store, "corruption_enabled", False)
                print("[STORY] QA: corruption_enabled = %s" % store.corruption_enabled)
            elif _qs_pick == "sugar":
                _qs_girl._sugar_mommy = not getattr(_qs_girl, "_sugar_mommy", False)
                print("[STORY] QA: %s _sugar_mommy = %s (active=%s: needs submissive+rich+had sex)" % (
                    _qs_girl.gid, _qs_girl._sugar_mommy, sugar_active(_qs_girl)))
        if _qs_pick == "exit":
            jump main_loop
        elif _qs_pick == "unlock" and story_unlock_event(_qs_girl):
            call story_event_play(_qs_girl, story_unlock_event(_qs_girl)) from _call_story_event_play_qa
        elif _qs_pick == "event" and story_events_for(_qs_girl):
            $ _qs_ev = renpy.display_menu([(_e, _e) for _e in story_events_for(_qs_girl)])
            call story_event_play(_qs_girl, _qs_ev) from _call_story_event_play_qa_ev
