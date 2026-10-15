# ============================================================
# character_stats.rpy
# Girl + PlayerData + relationship helpers
# PLUS: GIRLS CONFIG + SPRITE / CLOTHING SYSTEM (your big block)
# ============================================================

init -999 python:
    import random as _random
    from collections import defaultdict

    MAX_STAT = 1000

    renpy.music.register_channel("notify_sfx", mixer="sfx", loop=False)
    renpy.music.set_volume(0.25, channel="notify_sfx")

    def _lookup_girl(gid):
        """Called by pickle when unpickling a Girl reference.
        Returns the canonical instance from GIRL_BY_ID so all
        references point to the same object after load."""
        return store.GIRL_BY_ID.get(gid)

    def _make_int_defaultdict():
        return defaultdict(int)

    # ── Is she reachable at all? ──
    # "away" = off the map (today: the week she spends at her parents' giving birth, pregnancy.rpy
    # _pregnancy_stage_tick sets _giving_birth + loc "away"). Nothing may pick, text, invite or involve her
    # meanwhile. EVERY picker that does not require her to be at the player's location must ask this:
    # the photo / text events explicitly pick girls who are somewhere ELSE, and "away" is somewhere else.
    GIRL_AWAY_LOC = "away"

    def girl_route_enabled(girl):
        """Her OPTIONAL route is on. GIRLS_CONFIG "route_flag" names the store flag a new game asks about
        (the stepmom's "_stepmom_route", label _stepmom_setup); no flag = always on. An old save never has the
        variable, so its `default ... = True` turns the route on automatically on load. Off = she is off the map
        for good: girl_away_reason says "route_off" and every picker, text, event and screen follows."""
        _flag = GIRLS_CONFIG.get(getattr(girl, "gid", None), {}).get("route_flag")
        return _flag is None or bool(getattr(store, _flag, True))

    def girl_away_reason(girl):
        """WHY she is off the map right now, or None. The ONE place that knows the reasons: a future reason
        (a weekend at home with the baby...) is added here and every guard follows."""
        if not girl_route_enabled(girl):
            return "route_off"
        if getattr(girl, "_giving_birth", False):
            return "giving_birth"
        return None

    def girl_is_away(girl):
        """She is off the map: no event, text, invite, call or scene may involve her right now."""
        return girl_away_reason(girl) is not None or getattr(girl, "loc", None) == GIRL_AWAY_LOC

    def girl_sent_away(girl, reason=""):
        """She leaves the map NOW (source of truth for going away): off the Party and off the "who was with
        him" list, so no later step of the same time change (Party sync, time-change handler, Set_Scene)
        drags her back to his side. girl_is_away() keeps every picker off her until she returns."""
        girl.loc = GIRL_AWAY_LOC
        for _name in ("Party", "LastPresentGirls"):
            _lst = getattr(store, _name, None)
            if _lst and girl in _lst:
                _lst.remove(girl)
        print("[AWAY] %s leaves the map (%s)" % (girl.gid, reason))

    def girls_reachable(girls=None):
        """ALL_GIRLS (or the given girls) minus the ones who are away. For pickers that loop over everybody."""
        return [_g for _g in (ALL_GIRLS if girls is None else girls) if not girl_is_away(_g)]

    # ── Girls who live off campus (GIRLS_CONFIG "off_campus": Shion, in the father's apartment) ──
    # She can be texted and visited, she only never shows up on campus by herself: the campus pickers that put a
    # girl somewhere without reading where she is (showers, exam, walk-in, night swim, guess who...) skip her.
    def girl_off_campus(girl):
        """She lives off campus (reads the config, so a save made before the flag follows it too)."""
        return bool(GIRLS_CONFIG.get(getattr(girl, "gid", None), {}).get("off_campus"))

    def girls_on_campus(girls=None):
        """girls_reachable() minus the girls who live off campus. For campus pickers."""
        return [_g for _g in girls_reachable(girls) if not girl_off_campus(_g)]

    def girl_home_loc(girl):
        """Where she goes when she goes home: her dorm room (GIRL_ROOMS), else the "home" of her config (Shion:
        the bedroom of the apartment). Takes a Girl or a gid. GIRL_ROOMS stays the list of DORM rooms only."""
        _gid = getattr(girl, "gid", girl)
        return GIRL_ROOMS.get(_gid) or GIRLS_CONFIG.get(_gid, {}).get("home") or "room"

    def girl_role(girl):
        """Her role in the player's life when it shapes how she talks (GIRLS_CONFIG "role": Shion = "stepmom"), or
        None. A role has its own line pools (rod_lines["role:<role>"]): what any girl in that role says where the
        shared pools would speak like a college student. Her own pools still come first."""
        return GIRLS_CONFIG.get(getattr(girl, "gid", None), {}).get("role")

    def girl_role_key(girl):
        """The rod_lines block of her role ("role:stepmom"), or None."""
        _r = girl_role(girl)
        return "role:" + _r if _r else None

    def girl_sends_photos(girl):
        """She texts him photos at all. GIRLS_CONFIG "no_photos" (Shion: never, the author's rule 2026-10-10)
        kills every photo of hers for good, whatever her stats or step: the Wait photo texts of her own accord
        (photo_text_ready) and the one he asks for on the phone (_photo_decide), whose button stays visible and
        gets her refusal (rod pool "photo_never"). girl_sends_lewd_photos (femdom_turn.rpy) is the separate
        story-step rule that still applies to the girls who DO send them."""
        return not GIRLS_CONFIG.get(getattr(girl, "gid", None), {}).get("no_photos", False)

    def girl_home_exit(girl):
        """Where you are when you walk out of her home room: campus, or the "leave_to" of her config (Shion: the
        living room of the apartment). Takes a Girl or a gid."""
        return GIRLS_CONFIG.get(getattr(girl, "gid", girl), {}).get("leave_to", "campus")

    def sync_off_campus_home(girl, why):
        """A girl who lives off campus keeps the home and schedule of her config (a save made before they changed
        keeps the old ones in the object: Shion's first draft was a campus student). Found at a place her schedule
        never has, and not with him, she goes where her schedule puts her now."""
        _cfg = GIRLS_CONFIG.get(girl.gid, {})
        if not _cfg.get("off_campus"):
            return
        _sched = [list(_r) for _r in _cfg["schedule"]]
        if girl.home != _cfg["home"] or getattr(girl, "schedule", None) != _sched:
            print("[OFF_CAMPUS] %s (%s): home %s -> %s, schedule from the config" % (girl.gid, why, girl.home, _cfg["home"]))
            girl.home = _cfg["home"]
            girl.schedule = _sched
        _places = set(_p for _r in _sched for _p in _r)
        if girl.loc not in _places and not girl_is_away(girl) and girl not in store.Party:
            _now = get_scheduled_location_for(girl, store.Day, store.TimeIndex)
            print("[OFF_CAMPUS] %s (%s): was at %s, not a place of her schedule -> %s" % (girl.gid, why, girl.loc, _now))
            girl.loc = _now

    # ── Canonical act/position key lists (single source of truth) ──
    # Every position has its own PREFERENCE counter (doggy / laying_down / full_nelson had none: "veteran"
    # lines and video reactions could never fire for them). Sums must skip _SEX_POSITION_KEYS.
    _SEX_ACT_KEYS = ("kiss", "tj", "hj", "bj", "fj", "rj", "oral", "masturbate", "cowgirl", "reverse_cowgirl", "doggy", "laying_down", "full_nelson", "sex", "anal", "rub", "tip")
    # POSITIONS, not acts. They only record her preferences. Every vaginal position IS "sex":
    # mark_intimacy() never lets one of these go up without "sex" going up in the same scene, and
    # any "has she had sex?" check must read "sex" (or "anal"), never one of these.
    _SEX_POSITION_KEYS = ("cowgirl", "reverse_cowgirl", "doggy", "laying_down", "full_nelson")
    # store._scene_phase values where he is not inside her yet: a position seen here implies no act
    _NON_PENETRATION_PHASES = ("rub", "tip", "oral", "masturbate")

    # ── Central readers of Girl.Sex_acts (acts WITH THE PLAYER). Use these instead of summing keys by hand:
    #    adding "sex" + positions counts one cowgirl scene twice, and a position is never proof of sex. ──
    _SEX_PENETRATION_ACTS = ("sex", "anal")
    _SEX_OTHER_ACTS = ("hj", "bj", "tj", "fj", "rj", "oral", "masturbate", "rub", "tip")   # a kiss is not sexual history

    def girl_sex_count(girl):
        """Vaginal sex scenes with the player (the "sex" act counter, whatever the position)."""
        return (getattr(girl, "Sex_acts", None) or {}).get("sex", 0)

    def girl_had_sex(girl):
        """Has she had vaginal sex with the player? Reads the ACT, never a position."""
        return girl_sex_count(girl) > 0

    def girl_act_counts(girl):
        """(penetration, other sexual acts) with the player. Penetration = "sex" + "anal"."""
        _acts = getattr(girl, "Sex_acts", None) or {}
        return (sum(_acts.get(_k, 0) for _k in _SEX_PENETRATION_ACTS),
                sum(_acts.get(_k, 0) for _k in _SEX_OTHER_ACTS))

    # Scene / recorded video / witnessed types whose act is anal. Every anal variant carries its own
    # type, so a plain position type always means vaginal sex. THE list: every "is this scene anal" check
    # reads it (Cum, SubEvents, tease, pregnancy, lines...), a new anal variant is one entry here.
    _ANAL_SCENE_TYPES = ("anal", "full_nelson_anal", "laying_anal", "reverse_cowgirl_anal")

    def scene_type_act(scene_type):
        """Act proven by a scene / video / witnessed type: "doggy" -> "sex", "laying_anal" -> "anal".
        Anything that is not a penetration type comes back unchanged ("bj" -> "bj")."""
        if scene_type in _ANAL_SCENE_TYPES:
            return "anal"
        if scene_type in _SEX_POSITION_KEYS:
            return "sex"
        return scene_type

    # ── Sexual-history thresholds: the ONE place to tune them. Counts are real scenes: every penetration
    #    scene is worth 1 whatever the position. They were first tuned while a cowgirl / reverse cowgirl
    #    scene was worth 2 ("sex" + position), so anything not marked "was N" plays a little slower now. ──
    SEX_HISTORY_THRESHOLDS = {
        # actions.rpy: joining her in the shower / walking in. Bonus per penetration scene, capped.
        "shower_bonus_per_scene": 50,
        "shower_bonus_cap": 200,
        # sleepover.rpy _sleepover_history_level
        "sleepover_very_intimate_sex": 3,       # penetration scenes for level 3
        "sleepover_intimate_sex": 1,            # ... level 2
        "sleepover_intimate_oral": 3,           # hj + bj + tj that also give level 2
        # SubEvents.rpy: she asks for it herself mid-scene
        "recording_request_acts": 3,            # camera_lover asks to be filmed after this many acts
        "anal_request_sex": 1,                  # anal_lover asks for anal (was 2 = ONE cowgirl scene)
        # Shower.rpy _shower_rel_tier
        "shower_tier_lovers_sex": 5,
        "shower_tier_intimate_sex": 1,          # was 2 = ONE cowgirl scene
        "shower_tier_comfortable_acts": 3,
        # interactions.rpy
        "lesbian_still_denying_sex": 3,         # _lesbian_sex_hesitation: "this is the last time" tier lasts this long
        "rub_veteran_sex": 5,                   # rub_accept_line: "we've done so much more" above this
        "lesbian_veteran_acts": 5,              # get_bf_loyalty_hint: in_love_veteran_lesbian
        # npc_partner.rpy _npc_process_breakup
        "breakup_lesbian_identity_acts": 5,
        "breakup_heavy_history_acts": 8,
        # phone_messaging.rpy _dp_process_dickpic
        "dickpic_accept_acts": 3,
        # shop.rpy _bk_calc_dressing_scenario: total acts that invite him into the dressing room
        "dressing_invite_acts": {"pf_bf": 10, "pf": 6, "shy_bf": 20, "bf": 15, "shy": 15, "default": 10},
        # Core_LayingDown.rpy: up to this many penetration scenes she still acts inexperienced
        "ld_inexperienced_sex": 3,
        "ld_entry_inexperienced_sex": 2,
        # trait_is_new(): how many of her times in the trait's domain BEFORE this scene / session keep her discovering it
        # (the scene / session playing never counts: her first times speak while they happen)
        "trait_new_anal": 3,        # anal_lover still discovers it in her first 3 anal scenes
        "trait_new_cum": 3,         # cum_slut: until 3 loads came before this session (a condom's does not count)
        "trait_new_sex": 3,         # penetration scenes before hardcore_sex/cute_sex veteran talk
        "trait_new_femdom": 3,      # penetration scenes she spends finding out she likes giving orders (then she forces)
        "trait_new_subm": 3,        # orders of his she obeys (subm_note_obeyed) before her submissive veteran talk
        "trait_new_anal_neg": 1,    # one bad anal is enough for anal_hater to reference it
        "trait_new_cum_neg": 1,     # one cum encounter is enough for hate_cum to reference it
        "trait_new_sex_neg": 1,     # one encounter is enough for cute_sex to reference it
    }

    _TRAIT_NEW_DOMAIN = {
        "anal_lover":   ("anal",  "trait_new_anal"),
        "anal_hater":   ("anal",  "trait_new_anal_neg"),
        "cum_slut":     ("cum",   "trait_new_cum"),
        "hate_cum":     ("cum",   "trait_new_cum_neg"),
        "hardcore_sex": ("sex",   "trait_new_sex"),
        "cute_sex":     ("sex",   "trait_new_sex_neg"),
        "femdom":       ("sex",   "trait_new_femdom"),
        # obeying HIM is its own domain (orders she took, subm_note_obeyed): a broken femdom (CANON_BREAK_RULES)
        # gains submissive late and her first obedient scenes come out unsure, experienced or not
        "submissive":   ("subm",  "trait_new_subm"),
    }

    # domain -> the bf_history act that means "she already did this with her partner"
    _TRAIT_NEW_BF_ACT = {"anal": "anal", "cum": "creampie", "sex": "sex"}

    def girl_cum_loads(girl):
        """Loads that touched her (CumLog). A load that stayed in the condom never did: it teaches her nothing."""
        return sum(_n for _t, _n in (getattr(girl, "CumLog", None) or {}).items() if _t != "condom")

    def _trait_domain_count(girl, domain):
        """Her history with the player in a trait domain: anal scenes / loads that touched her / vaginal sex scenes
        / orders of his she obeyed (subm_note_obeyed)."""
        if domain == "anal":
            return (getattr(girl, "Sex_acts", None) or {}).get("anal", 0)
        if domain == "cum":
            return girl_cum_loads(girl)
        if domain == "subm":
            return int(getattr(girl, "_subm_obeyed", 0) or 0)
        return girl_sex_count(girl)

    def subm_note_obeyed(girl):
        """She took an order of his (the subm_ sub-events, her presentations): her submissive discovery counter.
        Asking to be directed IS the trait showing, so the card chip lights up here too."""
        girl._subm_obeyed = int(getattr(girl, "_subm_obeyed", 0) or 0) + 1
        if girl.has_trait("submissive"):
            girl.discover("discovered_trait_submissive")
        print("[SUBM] %s obeyed (%d): discovering=%s" % (
            girl.gid, girl._subm_obeyed, trait_is_discovering(girl, "submissive")))

    def trait_is_new(girl, trait_id):
        """True when the girl has a trait but not enough experience to talk like a veteran.
        Positive traits (anal_lover, cum_slut, hardcore_sex) need several scenes before
        she sounds experienced; negative traits need just one encounter to reference it.
        Never True when she already did it before the player: with her partner (bf_history), as an
        "experienced" girl, or (sex) as a non-virgin the player did not deflower."""
        _entry = _TRAIT_NEW_DOMAIN.get(trait_id)
        if not _entry:
            return False
        _domain, _thresh_key = _entry
        _needed = SEX_HISTORY_THRESHOLDS.get(_thresh_key, 3)
        _bf_act = _TRAIT_NEW_BF_ACT.get(_domain)
        # Experienced skips discovery only in the SEXUAL domains: obeying the player ("subm") is new for anyone,
        # a broken femdom CEO most of all
        if _domain in _TRAIT_NEW_BF_ACT and (
                girl.has_trait("experienced") or (_bf_act and hasattr(girl, "bf_has_done") and girl.bf_has_done(_bf_act))):
            return False
        if _domain == "sex" and not girl.has_trait("virgin") and not getattr(girl, "virginity_taken_by_player", False):
            return False   # she was not a virgin when the player met her: someone came first
        # only her times BEFORE this one: the scene counts its act when it starts (anal / sex), loads count as they land
        # (cum), and her first times must still speak while they happen (trait_is_first reads the same base)
        _before = _trait_domain_count(girl, _domain)
        if _domain == "cum":
            _before -= (getattr(store, "_session_loads_by_girl", None) or {}).get(girl.gid, 0)
        elif _domain in ("anal", "sex"):
            _before -= 1 if _scene_act_marked(girl, _domain) else 0
        return _before < _needed

    def trait_is_first(girl, trait_id):
        """True during her very FIRST time in the trait's domain: nothing of it before this sex session (anal / sex:
        this scene is her first one; cum: no load before this session and at most one in it). A line that says
        "my first time" / "I've never" lives in a "<trait>_first" pool and plays only then; trait_is_new() lasts
        longer (her first few times). Meant for the eager traits: for the negative ones "new" already means "never"."""
        if not trait_is_new(girl, trait_id):
            return False
        _domain = _TRAIT_NEW_DOMAIN[trait_id][0]
        _count = _trait_domain_count(girl, _domain)
        if _domain == "cum":
            _now = (getattr(store, "_session_loads_by_girl", None) or {}).get(girl.gid, 0)
            return _count - _now <= 0 and _now <= 1
        # the scene counts its act once, when it starts: take it out to see what came before
        return _count - (1 if _scene_act_marked(girl, _domain) else 0) <= 0

    def trait_discovery_keys(girl, trait_id, base=None):
        """Her discovery variants of a pool / reaction key, most specific first: "<base>_first" (trait_is_first)
        then "<base>_new" (trait_is_new). Empty once she is a veteran. base defaults to the trait id."""
        if not trait_is_new(girl, trait_id):
            return []
        base = base or trait_id
        return ([base + "_first"] if trait_is_first(girl, trait_id) else []) + [base + "_new"]

    # Eager traits: their veteran lines talk like an old habit. While she is still discovering one (trait_is_new)
    # those lines never speak for her (trait_line_keys); scene_pick_line has the same rule (_EAGER_TRAIT_MODS).
    # femdom (docs/plan_femdom.md D7): she finds out she likes giving orders, and only a veteran FORCES.
    # submissive: she finds out she likes obeying (domain "subm"); her veteran voice waits for a few obeyed orders.
    EAGER_TRAITS = ("cum_slut", "anal_lover", "hardcore_sex", "femdom", "submissive")

    def trait_is_discovering(girl, trait_id):
        """She has an eager trait and is still discovering it (trait_is_new): its veteran voice stays silent."""
        return trait_id in EAGER_TRAITS and girl.has_trait(trait_id) and trait_is_new(girl, trait_id)

    def trait_line_keys(girl, trait_id):
        """Keys to try, in order, in a trait-keyed table of FLAVOR lines (reactions, chats, games): her discovery
        variants first. An eager trait she is still discovering never falls back to its veteran key: with no
        discovery line in the table, that trait stays silent and the next trait / the default speaks. Any other
        trait falls back as usual. Where the line must follow what she DOES (a behavior), use trait_pool_key."""
        _disc = trait_discovery_keys(girl, trait_id)
        if _disc and trait_id in EAGER_TRAITS:
            return _disc
        return _disc + [trait_id]

    def trait_pool_key(girl, trait_id, pools):
        """The key to read in a trait-keyed dict of lines: her discovery variant ("<trait>_first" / "<trait>_new",
        most specific first) when the dict has one, else the trait itself."""
        for _k in trait_discovery_keys(girl, trait_id):
            if _k in pools:
                return _k
        return trait_id

    def trait_is_veteran(girl, trait_id):
        """She has the trait AND is past her discovery phase: the trait's habits (a cum_slut forcing the load where
        she wants it) start only now. Before that she wants it, asks for it and accepts it, but never forces."""
        return girl.has_trait(trait_id) and not trait_is_new(girl, trait_id)

    def trait_discovery_state(girl):
        """The eager traits she is still discovering, as {trait_id: "first" / "new"} (trait_is_first / trait_is_new).
        A video keeps it in its snapshot (_make_vid_snapshot), so what the video shows stays at the stage she was."""
        return dict((_t, "first" if trait_is_first(girl, _t) else "new")
                    for _t in EAGER_TRAITS if trait_is_discovering(girl, _t))

    def sex_history_bonus(girl):
        """Stat bonus her penetration history with the player gives (shower join / walk-in)."""
        return min(girl_act_counts(girl)[0] * SEX_HISTORY_THRESHOLDS["shower_bonus_per_scene"],
                   SEX_HISTORY_THRESHOLDS["shower_bonus_cap"])

    def girl_type_count(girl, scene_type):
        """How many times she has done, with the player, what this scene / video type shows.
        A position reads its own counter, an anal variant reads "anal", "creampie" reads CreampieCounts."""
        if scene_type == "creampie":
            return int(getattr(girl, "CreampieCounts", 0) or 0)
        _acts = getattr(girl, "Sex_acts", None) or {}
        if scene_type in _ANAL_SCENE_TYPES:
            return _acts.get("anal", 0)
        return _acts.get(scene_type, 0)

    def scene_type_is_penetration(scene_type):
        """He is inside her in this scene / video type (any vaginal position or anal variant)."""
        return scene_type_act(scene_type) in _SEX_PENETRATION_ACTS

    def girl_history_normalize(girl):
        """Enforce "a position never exists without its act" on data that did not go through
        mark_intimacy(): saves from before the rule, QA helpers that write Sex_acts directly.
        cowgirl / reverse_cowgirl have no anal variant, so they prove vaginal sex. doggy / laying_down /
        full_nelson also host anal scenes: they only imply "sex" when she has no "anal" either.
        Returns True when something was fixed."""
        _acts = getattr(girl, "Sex_acts", None)
        _flags = getattr(girl, "intimacy_flags", None)
        if _acts is None or _flags is None:
            return False
        _fixed = []
        # flag and counter of the same act must agree
        for _k in _SEX_PENETRATION_ACTS:
            if _acts.get(_k, 0) > 0 and _k not in _flags:
                _flags.add(_k)
                _fixed.append("flag:" + _k)
            elif _k in _flags and _acts.get(_k, 0) <= 0:
                _acts[_k] = 1
                _fixed.append("count:" + _k)
        if "sex" not in _flags:
            _pos = dict((_k, _acts.get(_k, 0)) for _k in _SEX_POSITION_KEYS)
            _vaginal_only = [_k for _k in ("cowgirl", "reverse_cowgirl") if _k in _flags or _pos[_k] > 0]
            _any_pos = [_k for _k in _SEX_POSITION_KEYS if _k in _flags or _pos[_k] > 0]
            if _vaginal_only or (_any_pos and "anal" not in _flags):
                _flags.add("sex")
                _acts["sex"] = max(1, max(_pos.values()))
                _fixed.append("sex<-" + "+".join(_vaginal_only or _any_pos))
        # Position counters that did not exist before (doggy / laying_down / full_nelson): rebuild them
        # from the location log, which always recorded the position. Flag with no log entry counts 1.
        _log = getattr(girl, "Sex_act_locations", None) or []
        for _k in _SEX_POSITION_KEYS:
            if _k in _flags and _acts.get(_k, 0) <= 0:
                _acts[_k] = max(1, sum(1 for _e in _log if isinstance(_e, dict) and _e.get("act") == _k))
                _fixed.append("%s=%d" % (_k, _acts[_k]))
        if _fixed:
            print("[SEX_FLAG] %s history normalized: %s" % (getattr(girl, "gid", "?"), ", ".join(_fixed)))
        return bool(_fixed)
    _ORGASM_POSITION_KEYS = ("kiss", "massage", "hj", "bj", "tj", "fj", "rj", "cowgirl", "reverse_cowgirl", "doggy", "full_nelson", "laying_down", "anal", "masturbate")
    _INITIAL_FAV_ACTS = ("kiss", "massage", "hj", "bj", "tj", "reverse_cowgirl", "cowgirl", "laying_down")
    _ACT_TO_POSE = {"tj": "titjob", "fj": "footjob", "rj": "rimjob"}

    # "mono" or "poly". Auto-switches to "poly" when any harem_accepted is populated.
    relationship_mode = "mono"

    # ============================================================
    # DEBUG FLAGS
    # ============================================================
    # When True, all girls start in the player's room at game start.
    # Set to False for normal scheduled behaviour.
    DEBUG_ALL_IN_PLAYER_ROOM = False


    # ============================================================
    # Cheating attitude levels (1..6)
    # ============================================================
    CHEAT_ATTITUDE = {
        1: "hate_cheat",       # never cheats, gets angry
        2: "soft_no_cheat",    # refuses, not angry
        3: "tempted",          # tempted but hasn't done it
        4: "first_time_ok",    # willing to cheat first time
        5: "recurring_ok",     # cheated more times
        6: "love_cheating",    # likes cheating (trait cheater starts here)
    }


    # ============================================================
    # Optional trait definitions
    # ============================================================
    TRAIT_DEFS = {
        "virgin": {"desc": "Has not had sex yet."},
        "voyeur": {"desc": "Likes watching."},
        "exhibitionist": {"desc": "Likes being watched."},
        "camera_lover": {"desc": "Loves cameras/recording. May ask the player to record during sex."},
        "camera_hater": {"desc": "Hates cameras/recording. Very resistant to being filmed."},
        "polyamorous": {"desc": "Open to sharing a partner. Easily accepts a harem."},
        "monogamous": {"desc": "Demands exclusivity. Very hard to convince into sharing."},

        # New:
        "loyal": {"desc": "Strongly resists cheating."},
        "cheater": {"desc": "Cheating is easy and enjoyable."},

        # Cum / public traits:
        "cum_slut": {"desc": "Loves cum inside, on her, in her mouth. Hates condoms."},
        "hate_cum": {"desc": "Hates cum contact. Strongly prefers condoms."},
        "public_fetish": {"desc": "Turned on by public exposure and walking around dirty."},
        "public_shy": {"desc": "Hates public exposure. Gains obedience when pushed."},
        "hardcore_sex": {"desc": "Prefers rough, fast sex. Asks to go faster during scenes."},
        "cute_sex": {"desc": "Prefers gentle, slow sex. Asks to go slower during scenes."},

        # Control (approval.rpy ACT_CONTROL):
        "femdom": {"desc": "Wants to be in charge. Accepts acts that put her in control, resists acts that put you in control."},
        "submissive": {"desc": "Likes being told what to do. Accepts acts that put you in control more easily."},

        # Relationship status:
        "married": {"desc": "She's married."},

        # Anal preference:
        "anal_lover": {"desc": "Loves anal sex. Gets more pleasure, may spontaneously ask for it."},
        "anal_hater": {"desc": "Hates/fears anal sex. Pain-focused, extremely resistant."},

        # Sexuality:
        "lesbian": {"desc": "Only attracted to women. Requires dominance or leverage for sexual acts."},

        # Economy:
        "poor": {"desc": "Financial struggles. Gifts mean more. Vulnerable to money offers."},
        "rich": {"desc": "Wealthy background. Hard to impress with gifts."},

        # Pregnancy:
        "breedable": {"desc": "Extremely fertile. Wider fertile window and higher conception chance."},
        "infertile": {"desc": "Cannot get pregnant. Zero conception chance."},
        "pregnancy_fetish": {"desc": "Wants to be bred. Refuses the pill, craves creampies."},
        "pregnancy_fear": {"desc": "Terrified of pregnancy. Always on the pill, panics if at risk."},
    }

    # Opposing trait pairs — player picks at most one per pair
    TRAIT_PAIRS = [
        {
            "category": "Camera",
            "a": "camera_lover",
            "a_label": "Camera Lover",
            "a_desc": "Loves being filmed. May ask to be recorded.",
            "b": "camera_hater",
            "b_label": "Camera Hater",
            "b_desc": "Hates cameras. Very resistant to filming.",
        },
        {
            "category": "Cum",
            "a": "cum_slut",
            "a_label": "Cum Lover",
            "a_desc": "Loves cum inside her. Hates condoms.",
            "b": "hate_cum",
            "b_label": "Cum Hater",
            "b_desc": "Hates cum contact. Demands condoms.",
        },
        {
            "category": "Public",
            "a": "public_fetish",
            "a_label": "Public Fetish",
            "a_desc": "Turned on by public exposure and risk.",
            "b": "public_shy",
            "b_label": "Public Shy",
            "b_desc": "Terrified of public exposure.",
        },
        {
            "category": "Sex Style",
            "a": "hardcore_sex",
            "a_label": "Hardcore",
            "a_desc": "Prefers rough, fast, intense sex.",
            "b": "cute_sex",
            "b_label": "Gentle",
            "b_desc": "Prefers slow, intimate, gentle sex.",
        },
        {
            "category": "Control",
            "a": "femdom",
            "a_label": "Femdom",
            "a_desc": "Wants to be in charge. Resists acts that put you in control.",
            "b": "submissive",
            "b_label": "Submissive",
            "b_desc": "Likes being told what to do. Gives in to your control easily.",
        },
        {
            "category": "Loyalty",
            "a": "cheater",
            "a_label": "Cheater",
            "a_desc": "Cheating is easy and enjoyable for her.",
            "b": "loyal",
            "b_label": "Loyal",
            "b_desc": "Strongly resists cheating. Hard to corrupt.",
        },
        {
            "category": "Anal",
            "a": "anal_lover",
            "a_label": "Anal Lover",
            "a_desc": "Loves anal. Gets more pleasure, may ask for it.",
            "b": "anal_hater",
            "b_label": "Anal Hater",
            "b_desc": "Hates/fears anal. Pain-focused, very resistant.",
        },
        {
            "category": "Economy",
            "a": "poor",
            "a_label": "Poor",
            "a_desc": "Struggles financially. Gifts mean more to her.",
            "b": "rich",
            "b_label": "Rich",
            "b_desc": "Wealthy background. Hard to impress with gifts.",
        },
        {
            "category": "Tolerance",
            "a": "heavy_drinker",
            "a_label": "Heavy Drinker",
            "a_desc": "Holds her liquor. Alcohol affects her far less.",
            "b": "lightweight",
            "b_label": "Lightweight",
            "b_desc": "Low tolerance. Gets drunk fast and sick easily.",
        },
        {
            "category": "Sharing",
            "a": "polyamorous",
            "a_label": "Polyamorous",
            "a_desc": "Open to sharing a partner. Much more willing to accept a harem.",
            "b": "monogamous",
            "b_label": "Monogamous",
            "b_desc": "Demands exclusivity. Extremely resistant to sharing.",
        },
        {
            "category": "Fertility",
            "a": "breedable",
            "a_label": "Breedable",
            "a_desc": "Extremely fertile. 1.5x conception chance and wider fertile window.",
            "b": "infertile",
            "b_label": "Infertile",
            "b_desc": "Cannot get pregnant. Zero conception chance.",
        },
        {
            "category": "Pregnancy",
            "a": "pregnancy_fetish",
            "a_label": "Pregnancy Fetish",
            "a_desc": "Wants to be bred. Refuses the pill, craves creampies.",
            "b": "pregnancy_fear",
            "b_label": "Pregnancy Fear",
            "b_desc": "Terrified of pregnancy. Always on the pill, never forgets.",
        },
    ]

    # Independent system traits — yes/no toggle (not opposing pairs)
    SYSTEM_TRAITS = [
        {
            "id": "naive",
            "label": "Naive",
            "desc": "Has never done anything sexual. No history at all. Forces Virgin.",
            "on_add": "set_naive",
            "conflicts": ["experienced"],
        },
        {
            "id": "virgin",
            "label": "Virgin",
            "desc": "Has not had sex yet.",
            "conflicts": ["experienced"],
        },
        {
            "id": "experienced",
            "label": "Experienced",
            "desc": "Has done everything before with someone else. Not a virgin, knows what she's doing.",
            "on_add": "set_experienced",
            "conflicts": ["virgin", "naive"],
        },
        {
            "id": "voyeur",
            "label": "Voyeur",
            "desc": "Likes watching others.",
        },
        {
            "id": "exhibitionist",
            "label": "Exhibitionist",
            "desc": "Likes being watched.",
        },
        {
            "id": "nerd",
            "label": "Nerd",
            "desc": "Academically obsessed. Earns double study points and reacts strongly to class disruptions.",
            "conflicts": ["gym_rat"],
        },
        {
            "id": "gym_rat",
            "label": "Gym Rat",
            "desc": "Lives at the gym. Respects strength, despises weakness.",
            "conflicts": ["nerd"],
        },
        {
            "id": "lesbian",
            "label": "Lesbian",
            "desc": "Only attracted to women. Requires dominance or leverage for sexual acts.",
            "conflicts": ["has_boyfriend", "bisexual"],
        },
        {
            "id": "bisexual",
            "label": "Bisexual",
            "desc": "Attracted to both men and women. Can have a boyfriend or girlfriend. Uses normal mechanics.",
            "conflicts": ["lesbian"],
        },
        {
            "id": "has_boyfriend",
            "label": "Has a Boyfriend",
            "desc": "She already has an NPC boyfriend at game start. The boyfriend will be present in the game.",
            "on_add": "set_npc_partner",
            "conflicts": ["has_girlfriend", "lesbian", "married"],
        },
        {
            "id": "has_girlfriend",
            "label": "Has a Girlfriend",
            "desc": "She already has an NPC girlfriend at game start. The girlfriend will be present in the game.",
            "on_add": "set_npc_partner_female",
            "conflicts": ["has_boyfriend", "married"],
        },
        {
            # No NPC husband yet: Shion's husband is the player's father (a family contact, never an NPCPartner).
            # A married teacher will get one through the partner system, with "husband" as the partner label.
            "id": "married",
            "label": "Married",
            "desc": "She's married.",
            "conflicts": ["has_boyfriend", "has_girlfriend"],
        },
    ]

    # Which girl types can have a trait (GIRLS_CONFIG "type": student / teacher / family). A trait missing here
    # fits every type. Story exceptions for one girl go in her own GIRLS_CONFIG "blocked_traits".
    TRAIT_GIRL_TYPES = {
        "nerd":           ("student",),
        "gym_rat":        ("student",),
        "has_boyfriend":  ("student", "teacher"),
        "has_girlfriend": ("student", "teacher"),
        "married":        ("teacher", "family"),
    }

    _TRAIT_TABS = [
        {
            "label": "Preferences",
            "sections": [
                {"header": "Sex Style", "pairs": ["Sex Style"]},
                {"header": "Control", "pairs": ["Control"]},
                {"header": "Cum", "pairs": ["Cum"]},
                {"header": "Anal", "pairs": ["Anal"]},
                {"header": "Fertility", "pairs": ["Fertility", "Pregnancy"]},
                {"header": "Experience", "toggles": ["naive", "virgin", "experienced"]},
            ],
        },
        {
            "label": "Personality",
            "sections": [
                {"header": "Camera", "pairs": ["Camera"]},
                {"header": "Public", "pairs": ["Public"]},
                {"header": "Lifestyle", "pairs": ["Economy", "Tolerance"]},
                {"header": "Hobbies", "toggles": ["nerd", "gym_rat"]},
                {"header": "Kinks", "toggles": ["voyeur", "exhibitionist"]},
            ],
        },
        {
            "label": "Relationships",
            "sections": [
                {"header": "Loyalty", "pairs": ["Loyalty", "Sharing"]},
                {"header": "Orientation", "toggles": ["lesbian", "bisexual"]},
                {"header": "Partner", "toggles": ["has_boyfriend", "has_girlfriend", "married"]},
            ],
        },
    ]

    _PAIRS_BY_CAT = {}
    for _p in TRAIT_PAIRS:
        _PAIRS_BY_CAT[_p["category"]] = _p

    _SYS_BY_ID = {}
    for _s in SYSTEM_TRAITS:
        _SYS_BY_ID[_s["id"]] = _s

    _TRAIT_OPPOSITE = {}
    for _p in TRAIT_PAIRS:
        _TRAIT_OPPOSITE[_p["a"]] = _p["b"]
        _TRAIT_OPPOSITE[_p["b"]] = _p["a"]

    # ---------- Trait eligibility and canon (read from GIRLS_CONFIG, so old saves follow it too) ----------

    def girl_type(girl):
        return GIRLS_CONFIG.get(girl.gid, {}).get("type", "student")

    def girl_canon_traits(girl):
        """Her canon traits (GIRLS_CONFIG "traits") MINUS the ones she lost through their designed break
        (girl._canon_lost, written by check_corruption when a CANON_BREAK_RULES gate let one go). Every canon
        reader uses this, so a broken canon stays broken: enforce_canon_traits never gives it back, load included."""
        _canon = GIRLS_CONFIG.get(getattr(girl, "gid", None), {}).get("traits", [])
        _lost = getattr(girl, "_canon_lost", None) or ()
        return [_t for _t in _canon if _t not in _lost]

    def trait_blocked_for(girl, tid):
        """Why this girl can never have this trait (her girl type or her own "blocked_traits"), else None.
        Conflicts with what she already has are a different thing: the picker shows those on its own."""
        _cfg = GIRLS_CONFIG.get(girl.gid, {})
        if tid in girl_canon_traits(girl):
            return None
        _types = TRAIT_GIRL_TYPES.get(tid)
        if tid in _cfg.get("blocked_traits", []) or (_types is not None and girl_type(girl) not in _types):
            return _tl_fmt(_("(not for %s)"), girl.Name)
        return None

    def _trait_conflicts_with(tid, other):
        return (_TRAIT_OPPOSITE.get(tid) == other
                or other in _SYS_BY_ID.get(tid, {}).get("conflicts", [])
                or tid in _SYS_BY_ID.get(other, {}).get("conflicts", []))

    def trait_possible_for(girl, tid, ignoring=None):
        """True if the girl can ever have this trait: not blocked for her and no clash with a canon trait of hers.
        `ignoring` = a canon trait about to be removed in the same corruption stage (check_corruption): the clash
        with IT doesn't count (femdom -> submissive in one stage)."""
        if trait_blocked_for(girl, tid):
            return False
        _canon = [_t for _t in girl_canon_traits(girl) if _t != ignoring]
        return tid in _canon or not any(_trait_conflicts_with(tid, _ct) for _ct in _canon)

    # A canon trait with a designed way OUT: the rule says WHEN the canon lock opens for it (check_corruption;
    # corruption_enabled still gates the whole system). Before the gate nothing the player does can take it
    # (author 2026-10-03: "antes do degrau final ela NUNCA perde"). story_last_step is -1 without a story.
    CANON_BREAK_RULES = {
        "femdom": lambda g: story_last_step(g) >= 1 and story_step(g) >= story_last_step(g),
    }

    def trait_canon_breakable(girl, tid):
        """Her gate for losing this CANON trait is open (CANON_BREAK_RULES)."""
        _rule = CANON_BREAK_RULES.get(tid)
        if _rule is None:
            return False
        try:
            return bool(_rule(girl))
        except Exception as _e:
            print("[CORRUPTION] canon break rule for %s failed: %r" % (tid, _e))
            return False

    def enforce_canon_traits(girl, why, fresh=False):
        """Make her traits obey her GIRLS_CONFIG: every canon trait present, every trait she can't have gone
        (girl type, "blocked_traits", conflict or opposite of a canon trait). Idempotent: it runs after every
        roll / pick and on every load. A canon Experienced without its history gets it: fresh=True (only while a
        new game is being set up) runs the full _apply_experienced; mid-game it only writes the NPC history and
        never touches what she did with the player."""
        _cfg = GIRLS_CONFIG.get(girl.gid, {})
        _canon = list(girl_canon_traits(girl))   # a canon she broke (CANON_BREAK_RULES) stays broken
        _removed = []
        for _tid in sorted(girl.traits):
            if _tid not in _canon and not trait_possible_for(girl, _tid):
                girl.remove_trait(_tid)
                _removed.append(_tid)
        if "virgin" in _removed:
            girl.set_flag("virgin", False)
        if ("has_boyfriend" in _removed or "has_girlfriend" in _removed) and girl.has_npc_partner():
            girl.clear_npc_partner()
        if "lesbian" in _removed:
            girl.sexuality_spectrum = 50 if girl.has_trait("bisexual") else 0
        if "gym_rat" in _removed and "schedule" in _cfg:
            girl.schedule = [list(_row) for _row in _cfg["schedule"]]
        _added = []
        for _ct in _canon:
            if not girl.has_trait(_ct):
                girl.add_trait(_ct)
                _added.append(_ct)
        # A canon Experienced needs her history with someone else too: the GIRLS_CONFIG loop only adds the trait.
        # Both histories _apply_experienced writes have "kiss", the empty default doesn't.
        if "experienced" in _canon and not (getattr(girl, "bf_history", None) or {}).get("kiss"):
            _added.append("experienced_history")
            if fresh:
                _apply_experienced(girl)
            else:
                girl.set_flag("virgin", False)
                _hist = dict(getattr(girl, "bf_history", None) or {})
                _hist.update({"kiss": True, "masturbate": True} if girl.has_trait("lesbian") else {
                    "kiss": True, "hj": True, "masturbate": True, "tj": True, "bj": True, "rub": True,
                    "tip": True, "cowgirl": True, "reverse_cowgirl": True, "doggy": True,
                    "sex": True, "sex_raw": True, "anal": True, "creampie": True})
                girl.bf_history = _hist
        if _removed or _added:
            print("[CANON] %s (%s): removed=%s added=%s fresh=%s" % (girl.gid, why, _removed, _added, fresh))
            _sync_girl(girl)
        return _removed, _added

    _tp_frozen_dbg_done = set()

    def _tp_btn_state(tid, selected, opposites, girl, frozen=None):
        _canon = girl_canon_traits(girl)
        if tid in _canon:
            return "canon", None
        _blocked_why = trait_blocked_for(girl, tid)
        if _blocked_why:
            return "blocked", _blocked_why
        if frozen is not None and tid in frozen:
            _fkey = (girl.gid, tid)
            if _fkey not in _tp_frozen_dbg_done:
                _tp_frozen_dbg_done.add(_fkey)
                print("[BTN-STATE] %s/%s -> frozen (frozen type=%s, frozen=%r)" % (girl.gid, tid, type(frozen).__name__, frozen))
            return "frozen", None
        if frozen is not None and tid not in frozen:
            _fkey2 = (girl.gid, tid, "avail")
            if _fkey2 not in _tp_frozen_dbg_done:
                _tp_frozen_dbg_done.add(_fkey2)
                print("[BTN-STATE] %s/%s -> NOT frozen (available)" % (girl.gid, tid))
            if tid == "lesbian" and girl.has_trait("cum_slut") and "pregnancy_fetish" not in selected:
                return "blocked", _tl(_("(conflicts with %s's traits)")) % girl.Name
            if tid == "pregnancy_fetish" and girl.has_trait("hate_cum"):
                return "blocked", _tl(_("(conflicts with %s's traits)")) % girl.Name
        if tid == "cum_slut" and "pregnancy_fetish" in selected:
            return "locked_sel", "(locked: pregnancy fetish)"
        if tid == "cum_slut" and "lesbian" in selected:
            return "locked", "(locked: lesbian)"
        if tid == "hate_cum" and "lesbian" in selected and tid in selected and "pregnancy_fetish" not in selected:
            return "locked_sel", "(locked: lesbian)"
        if tid == "virgin" and "naive" in selected and tid in selected:
            return "locked_sel", "(locked: naive)"
        opp = opposites.get(tid, "")
        if opp in selected and tid not in selected:
            return "blocked", "(opposite selected)"
        _st_m = _SYS_BY_ID.get(tid)
        if _st_m:
            _cf = _st_m.get("conflicts", [])
            if any(c in selected for c in _cf) or any(tid in _get_system_conflicts(s) for s in selected):
                if tid not in selected:
                    return "blocked", "(conflict)"
        if tid in selected:
            return "selected", None
        return "normal", None

    # ---------- Sexuality Spectrum helpers ----------

    def _effective_spectrum(girl):
        base = getattr(girl, "sexuality_spectrum", 0)
        shift = getattr(girl, "_spectrum_temp_shift", 0)
        if base > 50:
            return max(50, base - shift)
        elif base < 50:
            return min(50, base + shift)
        return 50

    def shift_spectrum(girl, amount):
        if store.sexuality_locked:
            return
        s = getattr(girl, "sexuality_spectrum", 0)
        if s == 50:
            return
        if s > 50:
            s = max(50, s - abs(amount))
        else:
            s = min(50, s + abs(amount))
        girl.sexuality_spectrum = s
        if s == 50 and not girl.has_trait("bisexual"):
            girl.traits.add("bisexual")
            if girl.has_trait("lesbian"):
                girl.traits.discard("lesbian")
            debug_log("[SPECTRUM] %s reached 50 -> bisexual locked" % girl.gid)
            if callable(globals().get("unlock_achievement")):
                unlock_achievement("playing_both_sides")

    def lesbian_openness(girl):
        s = _effective_spectrum(girl)
        if s <= 50:
            return 100
        return max(0, int((100 - s) * 2))

    def lesbian_resistance(girl):
        s = _effective_spectrum(girl)
        if s <= 50:
            return 0
        return min(100, int((s - 50) * 2))

    def hetero_openness(girl):
        s = _effective_spectrum(girl)
        if s >= 50:
            return 100
        return max(0, s * 2)

    def spectrum_label(girl):
        s = getattr(girl, "sexuality_spectrum", 0)
        if s <= 25: return _tr("Straight")
        if s <= 40: return _tr("Party Bi")
        if s <= 49: return _tr("Curious")
        if s == 50: return _tr("Bisexual")
        if s <= 60: return _tr("Curious")
        if s <= 75: return _tr("Party Bi")
        return _tr("Lesbian")

    def _clear_girl_traits(girl):
        """Wipe all traits, trait-synced flags, and NPC partner so the
        girl is ready for a fresh trait assignment."""
        girl.traits.clear()
        girl.flags["virgin"] = False
        girl.flags["likes_camera"] = False
        girl.flags["hates_camera"] = False
        girl.flags["has_npc_partner"] = False
        girl.flags["partner_is_female"] = False
        girl.npc_partner_id = None
        # Intentional clear (trait picker / Rod's Choice / randomize): tell the rollback recovery in
        # _refresh_girl_save, or the next interaction would bring the old partner back from the snapshot.
        store._npc_partner_cleared = set(getattr(store, "_npc_partner_cleared", set())) | {girl.gid}
        girl._npc_partner_name = None
        girl._npc_guest_number = None
        girl.bf_max_tier = 0
        girl.bf_history = {
            "hj": False, "masturbate": False, "tj": False,
            "bj": False, "sex": False, "sex_raw": False, "creampie": False,
        }
        girl.sexuality_spectrum = 0
        girl._spectrum_temp_shift = 0

    def _track_raw_sex_start(girl):
        _was_first = getattr(girl, "raw_sex_count", 0) == 0
        girl.raw_sex_count = getattr(girl, "raw_sex_count", 0) + 1
        if _was_first and hasattr(girl, "mark_player_first") and not girl.bf_has_done("sex_raw"):
            girl.mark_player_first("sex_raw")
        # the day raw sex with him started, recorded once ("for weeks" lines). A save that went raw before
        # this stamp existed keeps None: its readers fall back on what else they have.
        if _was_first and getattr(girl, "_first_raw_day", None) is None:
            girl._first_raw_day = store.Day
        print("[RAW_SEX_TRACK] %s count=%d first=%s first_raw_day=%s" % (
            girl.gid, girl.raw_sex_count, _was_first, getattr(girl, "_first_raw_day", None)))

    def _apply_gym_rat_schedule(girl):
        """If girl has gym_rat trait, shift her schedule: classroom→gym."""
        if not girl.has_trait("gym_rat"):
            return
        sched = getattr(girl, "schedule", None)
        if sched is None:
            return
        new_sched = [list(row) for row in sched]
        for d in range(7):
            for t in range(3):
                if new_sched[d][t] == "classroom":
                    new_sched[d][t] = "gym"
        girl.schedule = new_sched

    def randomize_traits_for(girl, max_traits=None):
        """Randomly assign 3-5 traits.
        Never assigns both sides of an opposing pair."""
        _clear_girl_traits(girl)

        if max_traits is None:
            max_traits = renpy.random.randint(3, 5)

        candidates = []

        for pair in TRAIT_PAIRS:
            roll = renpy.random.random()
            if pair["category"] == "Sharing":
                # 20% polyamorous, 50% monogamous, 30% neither
                if roll < 0.20:
                    candidates.append(("trait", pair["a"]))
                elif roll < 0.70:
                    candidates.append(("trait", pair["b"]))
            else:
                if roll < 0.333:
                    candidates.append(("trait", pair["a"]))
                elif roll < 0.666:
                    candidates.append(("trait", pair["b"]))

        for st in SYSTEM_TRAITS:
            _chance = 0.333
            if girl.gid == "ntw" and st["id"] in ("lesbian", "has_girlfriend"):
                _chance = 0.60
            if renpy.random.random() < _chance:
                candidates.append(("system", st))

        renpy.random.shuffle(candidates)

        _sys_conflicts = {}
        for _st in SYSTEM_TRAITS:
            _sys_conflicts[_st["id"]] = set(_st.get("conflicts", []))

        # Phase 1: Select traits (conflict resolution only, no application). Her canon traits go in first and
        # don't count toward max_traits: every roll has to fit around them.
        count = 0
        _chosen_ids = set()
        _chosen = []
        for _ct in girl_canon_traits(girl):   # a broken canon (CANON_BREAK_RULES) never rolls back in
            _chosen_ids.add(_ct)
            _chosen.append(("system", _SYS_BY_ID[_ct]) if _ct in _SYS_BY_ID else ("trait", _ct))
        for kind, val in candidates:
            if count >= max_traits:
                break
            _tid = val["id"] if kind == "system" else val
            if _tid in _chosen_ids:
                continue
            if trait_blocked_for(girl, _tid) or _TRAIT_OPPOSITE.get(_tid) in _chosen_ids:
                continue
            _skip = False
            for _cid in _chosen_ids:
                if _tid in _sys_conflicts.get(_cid, set()) or _cid in _sys_conflicts.get(_tid, set()):
                    _skip = True
                    break
            if _skip:
                continue
            _chosen_ids.add(_tid)
            _chosen.append((kind, val))
            count += 1

        # Phase 2: Apply in correct order (simple first, then partner, then experienced/naive last)
        def _apply_order(item):
            _k, _v = item
            if _k == "system":
                _oa = _v.get("on_add", "")
                if _oa in ("set_experienced", "set_naive"):
                    return 2
                elif _oa in ("set_npc_partner", "set_npc_partner_female"):
                    return 1
            return 0

        for kind, val in sorted(_chosen, key=_apply_order):
            if kind == "system":
                girl.add_trait(val["id"])
                if val.get("on_add") == "set_npc_partner":
                    girl.set_npc_partner("npc_bf_%s" % girl.gid)
                elif val.get("on_add") == "set_npc_partner_female":
                    girl.set_npc_partner_female("npc_gf_%s" % girl.gid)
                elif val.get("on_add") == "set_experienced":
                    _apply_experienced(girl)
                elif val.get("on_add") == "set_naive":
                    _apply_naive(girl)
            else:
                girl.add_trait(val)

        # has_girlfriend forces lesbian (unless bisexual)
        if girl.has_npc_partner() and girl.get_flag("partner_is_female"):
            if not girl.has_trait("lesbian") and not girl.has_trait("bisexual"):
                girl.add_trait("lesbian")

        # Lesbian co-traits: force hate_cum, high chance of virgin
        if girl.has_trait("lesbian"):
            girl.remove_trait("cum_slut")
            if not girl.has_trait("hate_cum"):
                girl.add_trait("hate_cum")
            if not girl.has_trait("virgin") and not girl.has_trait("experienced") and renpy.random.random() < 0.80:
                girl.add_trait("virgin")
            # Lesbian partners are female
            if girl.has_npc_partner():
                girl.set_flag("partner_is_female", True)
                bf_history_drop_male_acts(girl)

        # Canon traits from config are always guaranteed (safety net: the selection above already honors them)
        enforce_canon_traits(girl, "randomize", fresh=True)

        # Gym Rat: shift schedule toward gym
        _apply_gym_rat_schedule(girl)

        # Naive safety net: ensure zero history regardless of trait application order
        if girl.has_trait("naive"):
            girl.bf_max_tier = 0
            girl.bf_history = {
                "hj": False, "masturbate": False, "tj": False,
                "bj": False, "sex": False, "sex_raw": False, "creampie": False,
            }
            girl.Sex_acts = {k: 0 for k in _SEX_ACT_KEYS}
            girl.player_firsts = {}
            if not girl.has_trait("virgin"):
                girl.add_trait("virgin")

    # ── Corruption rules ────────────────────────────────────
    # Data-driven trait evolution. Each category has stages
    # checked high-to-low; first match fires and breaks.
    CORRUPTION_RULES = {
        "cum": {
            "counter": lambda g: getattr(g, "CreampieCounts", 0) + getattr(g, "ForcedSwallowCounts", 0) + getattr(g, "MouthCumCounts", 0),
            "stages": [
                {
                    "threshold": 15, "blocks": "cum_slut",
                    "remove": "hate_cum", "add": "cum_slut",
                    "banner": _("Trait evolved: Cum Slut"),
                    "narration": _("Looks like %s doesn't just tolerate it anymore... she's starting to {b}crave{/b} it."),
                },
                {
                    "threshold": 5, "requires": "hate_cum",
                    "remove": "hate_cum",
                    "banner": _("Trait lost: Hate Cum"),
                    "narration": _("Looks like %s doesn't hate cum that much anymore..."),
                },
            ],
        },
        "camera": {
            "stages": [
                {
                    "threshold": 14, "blocks": "camera_lover",
                    "counter": lambda g: getattr(g, "CorruptionVideosSentCount", 0),
                    "remove": "camera_hater", "add": "camera_lover",
                    "banner": _("Trait evolved: Camera Lover"),
                    "narration": _("%s has seen so many videos she's actually starting to {b}enjoy{/b} being on camera."),
                },
                {
                    "threshold": 7, "requires": "camera_hater",
                    "counter": lambda g: len(getattr(g, "CorruptionVideoTypesSent", set())),
                    "remove": "camera_hater",
                    "banner": _("Trait lost: Camera Hater"),
                    "narration": _("Looks like %s doesn't hate cameras that much anymore..."),
                },
            ],
        },
        "public": {
            "counter": lambda g: getattr(g, "CorruptionPublicHeavyActs", 0),
            "stages": [
                {
                    "threshold": 20, "blocks": "public_fetish",
                    "remove": "public_shy", "add": "public_fetish",
                    "banner": _("Trait evolved: Public Fetish"),
                    "narration": _("%s isn't just comfortable in public anymore... she's getting {b}turned on{/b} by it."),
                },
                {
                    "threshold": 10, "requires": "public_shy",
                    "remove": "public_shy",
                    "banner": _("Trait lost: Public Shy"),
                    "narration": _("Looks like %s isn't so shy about doing things in public anymore..."),
                },
            ],
        },
        "pace": {
            "counter": lambda g: getattr(g, "CorruptionPaceIgnoredTotal", 0),
            "stages": [{
                "threshold": 5, "requires": "cute_sex",
                "remove": "cute_sex", "add": "hardcore_sex",
                "banner": _("Trait evolved: Hardcore"),
                "narration": _("%s stopped asking you to be gentle. Looks like she's learned to {b}like it rough{/b}."),
            }],
        },
        # docs/plan_femdom.md D5: a femdom girl whose requests he keeps refusing stops giving orders (femdom -> no
        # control trait) and, if he keeps at it, learns to follow his (-> submissive). The counter only grows on that
        # path (femdom_request_refused).
        "control": {
            "counter": lambda g: getattr(g, "CorruptionFemdomRefused", 0),
            "stages": [
                {
                    "threshold": 30, "blocks": "submissive",
                    "remove": "femdom", "add": "submissive",
                    # the flag makes the Submissive chip show on her card (PERSONALITY reads discovered_trait_*)
                    "discover": "discovered_trait_submissive",
                    "achievement": "the_queen_falls",
                    "banner": _("Trait evolved: Submissive"),
                    "narration": _("%s stopped giving you orders a while ago. Now she {b}waits for yours{/b}."),
                },
                {
                    "threshold": 15, "requires": "femdom",
                    "remove": "femdom",
                    "achievement": "the_queen_falls",
                    "banner": _("Trait lost: Femdom"),
                    "narration": _("%s gave up trying to boss you around. She {b}doesn't give the orders anymore{/b}."),
                },
            ],
        },
        "loyal": {
            "counter": lambda g: getattr(g, "GirlCheatCount", 0),
            "stages": [
                {
                    "threshold": 25, "blocks": "cheater",
                    "remove": "loyal", "add": "cheater",
                    "banner": _("Trait evolved: Cheater"),
                    "narration": _("At this point, %s doesn't even feel guilty anymore. Cheating has become {b}second nature{/b} to her."),
                },
                {
                    "threshold": 10, "requires": "loyal",
                    "remove": "loyal",
                    "banner": _("Trait lost: Loyal"),
                    "narration": _("After everything she's done behind her partner's back, %s can't really call herself {b}loyal{/b} anymore."),
                },
            ],
        },
        "spank": {
            "counter": lambda g: getattr(g, "CorruptionHeavySpanks", 0),
            "stages": [
                {
                    "threshold": 5, "requires": "cute_sex",
                    "remove": "cute_sex", "add": "hardcore_sex",
                    "banner": _("Trait evolved: Hardcore"),
                    "narration": _("After all those spanks, %s doesn't flinch anymore. She's starting to {b}like the pain{/b}."),
                },
                {
                    "counter": lambda g: 0 if g.has_trait("cute_sex") else getattr(g, "CorruptionHeavySpankDays", 0),
                    "threshold": 8, "blocks": "hardcore_sex",
                    "add": "hardcore_sex",
                    "banner": _("New trait: Hardcore"),
                    "narration": _("Day after day, you've pushed %s harder and harder. She doesn't cry out anymore... she {b}asks for it{/b}."),
                },
            ],
        },
        "exhibitionist": {
            "counter": lambda g: getattr(g, "CorruptionPublicHeavyActs", 0),
            "stages": [{
                "threshold": 30, "requires": "public_fetish", "blocks": "exhibitionist",
                "add": "exhibitionist",
                "banner": _("Trait gained: Exhibitionist"),
                "narration": _("%s doesn't just enjoy public risk anymore... she {b}wants{/b} to be seen."),
            }],
        },
        "anal": {
            "counter": lambda g: (getattr(g, "Sex_acts", None) or {}).get("anal", 0),
            "stages": [
                {
                    "threshold": 15, "blocks": "anal_lover",
                    "remove": "anal_hater", "add": "anal_lover",
                    "discover": "discovered_trait_anal_lover",
                    "banner": _("Trait evolved: Anal Lover"),
                    "narration": _("%s has taken it in the ass so many times... she's starting to {b}love{/b} it."),
                },
                {
                    "threshold": 7, "requires": "anal_hater",
                    "remove": "anal_hater",
                    "banner": _("Trait lost: Anal Hater"),
                    "narration": _("After all those times, %s doesn't dread anal that much anymore..."),
                },
            ],
        },
        "sharing": {
            "counter": lambda g: len(getattr(g, "harem_accepted", set()) or set()),
            "stages": [
                {
                    "threshold": 2, "requires": "monogamous",
                    "remove": "monogamous",
                    "banner": _("Trait lost: Monogamous"),
                    "narration": _("After accepting multiple girls into the harem, %s can't really call herself {b}monogamous{/b} anymore."),
                },
            ],
        },
    }

    _COLLAR_GIRLS = frozenset({"gwen", "rogue", "tenny"})

    # ── Ex Reconciliation Config (central) ──
    EX_RECON_CONFIG = {
        "cheating_trust_days":  28,
        "normal_trust_days":    14,
        "cheating_love_min":    800,
        "cheating_obed_min":    500,
        "cheating_score_min":   1500,
        "cheating_days_min":    7,
        "normal_love_angry":    600,
        "normal_love_sad":      550,
        "normal_obed_min":      500,
        "normal_score_angry":   1000,
        "normal_score_sad":     900,
        "ex2_love_bonus":       150,
        "ex2_score_bonus":      300,
        "recatch_love_per":     200,
        "recatch_obed_per":     200,
        "love_cap":             1000,
        "obed_cap":             900,
        "normal_days_min":      3,
        "cheating_jealousy_mult": 1.5,
        "cheating_bf_loyalty_loss": 200,
        "trust_mult_high":      2.0,
        "trust_mult_low":       1.5,
    }

    # ── Girl-Initiated Confession Config (central) ──
    CONFESSION_CONFIG = {
        "love_min":           950,
        "obed_single_min":    400,
        "obed_harem_min":     500,
        "cooldown_days":      7,
        "max_gentle_rejects": 3,
        "min_kiss":           1,
        "min_sex":            3,
    }

    if "Girl" not in globals():

        class Girl(object):
            def __reduce__(self):
                # Pickle: store only the gid; on unpickle, return the
                # canonical instance from GIRL_BY_ID (same object as ALL_GIRLS).
                return (_lookup_girl, (self.Id,))

            def __init__(self, gid, Name, default_pose="standing", color="#ffffff", body_type="medium", bust="medium"):
                # Basic identity
                self.Id = gid
                self.Name = Name
                self.color = color
                self.body_type = body_type  # "petite", "medium", "tall"
                self.bust = bust  # "small", "medium", "large"

                # ---------- Core stats 0–1000 ----------
                self.Love = 0
                self.Obed = 0
                self.Inbt = 0

                # ---------- Current state ----------
                self.Lust = 0      # 0–100
                self.Stamina = 10  # 0–10

                # ---------- Temptation 0–10 ----------
                self.Temptation = 0

                self.default_pose = default_pose
                self.mast_pose = "cowgirl"
                self.current_expression = None

                # ---------- Traits & flags ----------
                self.traits = set()

                self.flags = {
                    "virgin": False,

                    # Commitments:
                    "has_npc_partner": False,
                    "has_girl_partner": False,
                    "partner_is_female": False,

                    # Camera:
                    "likes_camera": False,
                    "hates_camera": False,

                    # Story:
                    "caught_cheating": False,
                }

                # ---------- Sexuality spectrum ----------
                # 0=hetero, 50=bi(locked), 100=lesbian
                self.sexuality_spectrum = 0
                self._spectrum_temp_shift = 0
                self._lesbian_sex_stage = 0  # 0=nothing, 1=did rub/hj, 2=did tip, 3=did sex, 4=did anal

                # ---------- Hangout / ToD ----------
                self._hangout_alcohol = 0.0  # drunkenness meter (event-only; persists via _girl_save)
                self._blackmail_leverage = 0
                self._financial_times = 0
                self._financial_attitude = 0  # 0=Reluctant, 1=Resigned, 2=Transactional, 3=Dependent
                self._total_gifts_value = 0
                self._financial_total_paid = 0  # lifetime $ paid to her via financial coercion (refunds subtract)
                self._coercion_path = None  # None, "blackmail", "financial", "alcohol"
                self._anal_preference = 0  # 0=Normal, 1=Curious, 2=Preferring, 3=Addicted
                # How each act was obtained: {act: {"first": method, "counts": {method: n}}}
                # method: "willing" | "paid" | "blackmail"
                self.Sex_act_methods = {}

                # ---------- Relationship with player ----------
                # "none" | "dating" | "exclusive" | "ex"
                self.Player_status = "none"
                # Ex history: filled when player breaks up
                # { "breakup_mood": "angry"|"sad", "love_at_breakup": int,
                #   "times_dated": int, "breakup_day": int }
                self.ex_player_history = None

                # Witness history: list of dicts recording what she saw
                # [{ "girl": gid, "act": str, "day": int,
                #    "location": str, "is_public": bool,
                #    "saw_cheating_player": bool, "saw_cheating_girl": bool,
                #    "cheating_type": "none"|"witness_was_cheated_on"|"witness_saw_girl_cheat"|"witness_saw_both_cheat" }]
                self.witness_history = []

                # Video seen history: list of dicts for every video she received/saw
                # [{ "girl_gid": str, "type": str, "location": str,
                #    "condom": bool|None, "consensual": bool, "subject": str,
                #    "day": int }]
                self.video_seen_history = []

                # Pending breakup flag (set by witness caught-cheating)
                self._breakup_pending = False
                self._breakup_reason = None

                # Suspicion: grows when GF suspects cheating (0-100)
                self.suspicion = 0

                # Virginity knowledge: what this girl believes about others
                # { gid: True }  means she thinks that girl is/was a virgin
                self.knows_virgin = {}

                # ---------- Girl partnerships ----------
                # NPC partner is just a status reference (not an in-world entity).
                self.npc_partner_id = None      # e.g. "npc_bf_1"
                # Partner that IS another in-world girl.
                self.girl_partner_id = None     # e.g. "rogue"

                # ---------- BF sexual history ----------
                # What she has done with her boyfriend (randomly generated).
                # bf_max_tier: 0=nothing, 1=hj/masturbate, 2=tj, 3=bj, 4=sex, 5=raw, 6=creampie
                # If bf_max_tier < 4, she's a virgin (no penetration).
                self.bf_max_tier = 0
                self.bf_history = {
                    "hj": False, "masturbate": False, "tj": False,
                    "bj": False, "sex": False, "sex_raw": False, "creampie": False,
                }
                # Player "firsts" — set True when player does something she hasn't done with BF
                self.player_firsts = {
                    "kiss": False, "hj": False, "masturbate": False, "tj": False,
                    "bj": False, "sex": False, "sex_raw": False, "creampie": False,
                }

                # ---------- BF Loyalty ----------
                # How much she values her NPC boyfriend (0-1000).
                # High = loves him, hard to steal.  Low = she's over him.
                # Starts 750 ("she likes him a lot") when set_npc_partner is called.
                self.bf_loyalty = 750

                # ---------- Hardcore Relationship tracking ----------
                self._hc_bf_next_escalation_day = 0
                self._hc_last_interaction_day = 0
                self._hc_love_maxed_notified = False
                self._hc_virginity_uncertain = False
                self._hc_single_warned = 0
                self._hc_partner_spawn_day = 0
                self._hc_was_abandoned = False

                # ---------- Trait evolution memory ----------
                # Tracks traits lost/gained via corruption for dialogue awareness
                # e.g. {"hate_cum": "cum_slut", "cute_sex": "hardcore_sex"}
                self.evolved_traits = {}
                # Canon traits she LOST through their designed break (CANON_BREAK_RULES, check_corruption):
                # girl_canon_traits skips these, so enforce_canon_traits never gives one back (load included)
                self._canon_lost = set()
                # Her canon femdom gate opened once (the final story step): the control count started fresh there
                self._femdom_gate_opened = False
                # Orders of his she obeyed (subm_note_obeyed): the submissive discovery domain ("subm")
                self._subm_obeyed = 0

                # ---------- Trust ----------
                self.cheat_tolerance = 500
                self.distrust_level = 0

                # ---------- Actions tracking ----------
                self.Daily_Actions = []
                self.Recent_Actions = []
                self.Slaps = 0
                self.study_level = 0
                self.grade_history = []
                self._nerd_f_count = 0
                self.intimacy_flags = set()  # tracks completed intimate acts: "kiss","hj","tj","bj","sex","anal"

                # ---------- Harem ----------
                # GIDs the girl has accepted as co-partners (poly/harem).
                # If a girl's gid is in this set, sending her videos with that girl is NOT cheating.
                self.harem_accepted = set()
                self._harem_forced_by = set()

                # ---------- Jealousy ----------
                self.Jealousy = 0

                # ---------- Harem pending ----------
                self._harem_ask_pending = False
                self._harem_caught_with_gid = None
                self._harem_caught_act = None
                self._harem_caught_suggests_add = False

                # ---------- Harem consent ----------
                self._open_relationship_consent = False
                self._open_rel_declined_day = -999
                self._gf_open_rel_trigger = None

                # ---------- Memory ----------
                self.Memory = []
                self.MemoryIndex = None

                # ---------- Legacy counters (still usable) ----------
                self.Exposure = {
                    "saw_boobs": 0,
                    "saw_pussy": 0,
                    "touch_boobs": 0,
                    "lick_boobs": 0,
                    "touch_ass": 0,
                    "touch_pussy": 0,
                    "lick_pussy": 0,
                    "finger_pussy": 0,
                    "finger_ass": 0,
                    "saw_penis": 0,
                }
                self.Sex_acts = {k: 0 for k in _SEX_ACT_KEYS}
                self.virginity_taken_by_player = False
                self.virginity_context = None

                # Location-aware sex history: [{"act": "bj", "location": "pool", "day": 5}, ...]
                self.Sex_act_locations = []

                self.raw_sex_count = 0  # times had sex without condom
                self._first_raw_day = None  # Day of her first raw sex with him (_track_raw_sex_start); None = never, or before the stamp
                self.CreampieCounts = 0  # times cum inside without condom
                self.ConsentedCreampies = 0  # times she agreed to creampie
                # Most creampies in one time slot (process_cum; Truth or Dare's "same night"): the slot of her last
                # one (Day * 10 + TimeIndex), how many she took in it and her record
                self._creampie_last_slot = -1
                self._creampie_slot_count = 0
                self._creampie_slot_max = 0
                self.CumLog = {}  # {"face": 3, "inside": 5, ...}
                self._atm_count = 0
                self._atp_count = 0
                self._dick_pic_last_day = None
                self._dick_pics_received = 0
                self.Firsts = {}
                self.MouthCumCounts = 0
                self.ForcedSwallowCounts = 0
                self._cumslut_denied_inside = False
                self._creampie_photo_pending = None
                self._ld_after_pussy = False
                self._ld_after_anal = False

                self.Orgasms = {k: 0 for k in _ORGASM_POSITION_KEYS}

                self.HardOrgasms = 0

                # ---------- Favorite act ----------
                # Initial random preference + threshold (overridden per-girl at init)
                self.FavoriteAct = None
                self.FavoriteActThreshold = 0
                self._favorite_act_unlocked = False  # True after orgasms surpass initial threshold

                # ---------- Tastes (food & drink preferences) ----------
                # Discovery-gated on the phone (discovered_fav_dish / discovered_fav_drink).
                # Rolled per-girl at new game (see girl init loop + _reset_all_girls).
                self.FavoriteDish = None            # "steak"|"pasta"|"chicken"|"salad"
                self.HatedDish = None
                self.FavoriteDrink = None           # "low"|"med"|"high" (generic tier)
                self.FavoriteBrand = None           # specific drink id within that tier
                self.HatedDrink = None              # a different tier she dislikes

                # ---------- Petnames ----------
                self.petname_from_player = None
                self.petname_for_player = None
                self.petname_for_player_auto = True
                self._petname_pending_change = None
                self._petname_rejected = set()
                self._petname_last_ask_day = -99

                # ---------- Question / phone thresholds ----------
                # Randomized per-girl at creation time (see girl init loop below)
                self.phone_threshold = 0        # min Love to give phone number
                self.q_threshold_virgin = 0     # min stat to answer virgin question
                self.q_threshold_fav_act = 0    # min stat to answer favorite act question

                self.ActionLog = {
                    # -- Player saw girl's body --
                    "player_saw_boobs": 0,
                    "player_saw_pussy": 0,
                    "player_saw_ass": 0,
                    # -- Girl saw player's body --
                    "girl_saw_penis": 0,
                    "girl_saw_penis_sex": 0,
                    # -- Player touched/interacted --
                    "player_touch_boobs": 0,
                    "player_touch_pussy": 0,
                    "player_touch_ass": 0,
                    "player_lick_boobs": 0,
                    "player_lick_pussy": 0,
                    "player_finger_pussy": 0,
                    "player_finger_ass": 0,
                    # -- Acts/moments --
                    "player_caught_masturbating": 0,
                    "girl_caught_masturbating": 0,
                    "kiss": 0,
                    "flirt": 0,
                    # -- Sex acts --
                    "hj": 0,
                    "bj": 0,
                    "tj": 0,
                    "cowgirl": 0,
                    "reverse_cowgirl": 0,
                    "masturbate": 0,
                }

                self.Cum = [] # ["Face1", "Tits2", etc]
                self._mouth_cum_persist = False
                # ============================================================
                # NEW: Cheating counters (per girl, per victim/partner)
                # Requirement:
                # - If player cheats on girlfriend X with girl A, it only makes it easier with girl A.
                # - Separate when player is cheating vs when the girl is cheating on her partner.
                # ============================================================
                # player_cheat: counts when player has a girlfriend (NOT this girl) and does action with THIS girl.
                # Keyed by cheated-on girlfriend id for reporting, but the "ease" applies only to THIS girl anyway.
                self.PlayerCheatCountByVictim = defaultdict(int)

                # girl_cheat: counts when THIS girl has a partner (npc or girl) and does action outside it.
                # Keyed by partner id ("npc:<id>" or "girl:<id>")
                self.GirlCheatCountByPartner = defaultdict(int)

                # Aggregate cached counts (fast reads)
                self.PlayerCheatCount = 0
                self.GirlCheatCount = 0

                # ============================================================
                # NEW: Cheating preference state
                # - Stored, but also easy to compute if you want.
                # ============================================================
                self.CheatAttitude = 3  # default "tempted" (tunable per girl in config if you want)
                self.CheatMaxTier = 0  # highest cheating tier she has done (0=none, 1=kiss/touch, 2=hj/tj, 3=bj, 4=sex/anal)

                # Per-act cheat counters
                self.CheatActs = {
                    "kiss": 0, "touch": 0,
                    "hj": 0, "tj": 0,
                    "bj": 0, "sex": 0, "anal": 0,
                }

                # ---------- Temporary statuses ----------
                # dict of { "status_name": expire_day }
                # e.g. {"angry": 3} means angry until end of day 3
                self.temp_statuses = {}
                self.temp_status_reasons = {}

                # ---------- Cheat path ----------
                self._cheat_sex_stage = 0
                self._cheat_escalation_path = None
                self._cheat_broke = False
                self._cheat_heat = 0
                self._cheat_heat_peak = 0
                self._cheat_bf_call_triggered = False
                self._cheat_spank_mark_triggered = False
                self._cheat_condom_sex_count = 0
                self._cheat_afterscene_shown = set()

                # ---------- NPC partner ----------
                # Per-partner mirrors: neutral values + reset live in Girl._NPC_PARTNER_MIRRORS
                # (None = create_npc_partner rolls it). Keep both in sync when adding one.
                self._npc_partner_name = None
                self._npc_partner_traits = None
                self._npc_partner_schedule = None
                self._npc_guest_number = None
                # NPCPartner stats, mirrored here by NPCPartner.change_friendship / change_love and by the
                # save snapshot (same defaults as NPCPartner.__init__)
                self._npc_friendship = 200
                self._npc_love = 750
                self._npc_suspicion = 0
                self._npc_gifts_given = set()
                self._npc_partner_received_nerd_gift = False
                self._npc_ex_names = []   # names of her previous NPC partners: a NEW partner never reuses one

                # ---------- NTR boundary system ----------
                self._ntr_active = False
                self._ntr_boundary_level = None
                self._ntr_boundary_bar = 0
                self._ntr_boundary_discovered = False
                self._ntr_trust_discovered = False
                self._ntr_levelup_pending = False
                self._ntr_activation_pending = False
                self._ntr_activation_msg_pending = False
                self._ntr_activation_msg_list = []
                self._ntr_activation_msg_npc_id = None
                self._ntr_discovery_pending = False
                self._ntr_discovery_npc_id = None
                self._ntr_discovery_was_violation = False
                self._ntr_discovery_violation_act = None
                self._ntr_violation_pending = False
                self._npc_video_pending = False
                self._ntr_video_seen_pending = False   # NTR-known partner watched a video: she texts about it next day
                self._npc_secret_vid_angry = False
                self._ntr_afterscene_shown = set()

                # ---------- NPC catch / suspicion ----------
                self._npc_catch_pending = False
                self._npc_catch_pending_day = 0
                self._npc_catch_pending_ti = 0
                self._npc_catch_count = 0
                self._npc_catch_msg_pending = False
                self._npc_catch_msg_list = []
                self._npc_catch_msg_broke_up = False
                self._npc_catch_msg_reason = None
                self._npc_breakup_result = None
                self._npc_suspicion_pending = False
                self._will_break_up_with_partner = False
                # True once she dumped her NPC partner because of the player (NHIE "stolen_partner")
                self._left_partner_for_player = False
                # Times the player removed the condom without her noticing (NHIE "lied_protection")
                self._stealth_condom_count = 0

                # ---------- Girl knowledge ----------
                self.knows_acts = {}
                self.knows_cheating = {}
                self.knows_has_bf = {}
                self.knows_with_player = {}
                self.knows_lesbian = {}
                self.knows_player_bust_pref = None  # "small"/"medium"/"large" or None

                # ---------- Activity Buddy ----------
                self._buddy_activity_count = {}
                self._buddy_last_invite_day = 0
                self._buddy_accepted_count = 0

                # ---------- TJ Bust Rejection ----------
                self._tj_rejection_count = 0

                # ---------- Photo / video day cooldowns ----------
                self._mast_photo_day = None
                self._tease_photo_day = None
                self._spank_photo_day = None
                self._cream_photo_day = None
                self._bikini_photo_sent = False
                self._camtease_photo_day = None
                self._piercing_photo_sent = False
                self._photo_text_day = None   # her last photo text of her own accord, any kind (PHOTO_TEXT_GAP, system_time.rpy)

                # ---------- Relationship / ex ----------
                self._ex_confrontation_done = False
                self._cheating_ex_resolved = False
                self._date_afterglow = 0

                # ---------- Ex reconciliation ----------
                self._ex_trust = 0
                self._ex_trust_max = 0
                self._cheating_ex_reconciled = False
                self._cheating_ex_recatch = 0
                self._jealousy_gain_mult = 1.0

                # ---------- Girl-initiated confession ----------
                self._confess_cooldown_day = 0
                self._confess_reject_count = 0
                self._confess_permanent_stop = False

                # ---------- Scene state (transient but must reset) ----------
                self.escalation_history = []
                self._prev_pose = "standing"
                self._prev_slot = None
                self._massage_prev_pose = "standing"
                self._massage_prev_slot = None
                self._kiss_prev_pose = "standing"
                self._kiss_prev_slot = None
                self._ignored_pace_requests = 0
                self._pos_change_requests = 0
                self._denial_slot = None
                self._denial_actions = set()
                self.shower_state = None
                self.shower_outfit = None
                self._saved_outfit = None
                self._shower_just_declined = False
                self._slept_with_player_tonight = False
                self._hangout_alcohol = 0

                # ---------- Misc persistent ----------
                self.LastApprovalResult = None
                self.LastSafeFlirtDecision = None
                self.Mood = None
                self.player_fav_position = None
                self._last_massage_day = None
                self._lewd_flirt_slot = None
                self._lewd_flirt_count = 0
                self._blackmail_times = 0
                self._blackmail_refused = 0  # his blackmails she refused (blackmail_note_refused); _blackmail_times = gave in
                self._story_evidence_used = 0     # of those, the ones with her story's proof she gave in to...
                self._story_evidence_refused = 0  # ...and refused (story_evidence_blackmail): the rest were sex videos
                self._heavy_spank_yesterday = False
                self._heavy_spank_count = 0
                self._piercing_pending = False
                self._piercing_received = False
                self._piercing_remove_pending = False
                self._hc_bf_dumped_day = 0
                self._hc_bf_dumped_npc = None
                self.FavoriteDish = None
                self.HatedDish = None

                # ---------- Corruption counters ----------
                self.CorruptionVideosSentCount = 0      # total videos sent to this girl
                self.CorruptionVideoTypesSent = set()    # unique video types sent (hj, bj, tj, etc)
                self.CorruptionPublicHeavyActs = 0       # heavy sex acts done in public (hj, bj, tj, sex)
                self.CorruptionPaceIgnoredTotal = 0      # total pace requests ignored (permanent)
                self.CorruptionHeavySpanks = 0           # times spanked at level 7+ (for cute_sex corruption)
                self.CorruptionHeavySpankDays = 0       # distinct days with heavy spanks (for no-trait corruption)
                self._heavy_spank_last_day = -1         # last Day a heavy spank was counted

                # ---------- Spanking ----------
                self.SpankLevel = 0                      # 0-10, current intensity of the ASS spanks
                self.SlapLevel = 0                       # 0-10, the same for the FACE slaps of SpankHer (cowgirl)
                # Every ass spank she took (SubEvents.rpy spank_note): {"taken", "by_player", "enjoyed"}. None = not
                # started yet: the legacy reading (her heavy spank days) until spank_log_ensure starts it
                self.SpankLog = None

                # ============================================================
                # NEW: Girl-to-girl affinity + per-girl history
                # ============================================================
                self.Girl_like = {}  # { other_id: 0..1000 }
                self.Girl_history = defaultdict(_make_int_defaultdict)
                # Example:
                # self.Girl_history["rogue"]["kiss"] += 1
                # self.Girl_history["rogue"]["threesome"] += 1

                # ── Pregnancy ──
                self._pregnant = False
                self._pregnancy_day = 0
                self._pregnancy_stage = 0
                self._pregnancy_known = False
                self._pregnancy_discovery_day = 0
                self._pregnancy_count = 0
                self._pregnancy_cooldown = 0
                self._player_pregnancy_response = None
                self._npc_paternity_claimed = False
                self._npc_pregnancy_confrontation_pending = False
                self._npc_pregnancy_save_attempt = False
                self._npc_pregnancy_confronted = False    # her partner confronted the player: he KNOWS (pregnancy.rpy preg_partner_knows)
                self._pregnancy_told_day = 0              # Day she TOLD him (discovery event). 0 = never / old save
                self._preg_body_moments_done = ()         # body moments already played this pregnancy (pregnancy_body.rpy)

                self._giving_birth = False
                self._birth_return_day = 0
                self._postpartum = False
                self._children_count = 0
                self._children = []                       # one plain record per child, frozen at birth (children.rpy)
                self._father_involvement = None           # 0..100 once moved; None = his discovery answer speaks (children.rpy father_involvement)
                self._baby_lines_seen = []                # baby lines he already heard from her (children.rpy baby_line_pick)
                self._baby_asked_day = 0                  # Day he last asked "How's the baby?" (children.rpy child_ask_resolve)
                self._child_forgotten = False             # Baby Eraser used on her: HE remembers a child she never had
                self._child_event_next = {}               # {event: first Day it may play again} (children.rpy children_morning_pick)
                self._away_text_sent = False              # the one text of her birth week already went out
                self._birth_procedure = False             # IUD inserted after last birth (pregnancy.rpy, "THE PROCEDURE")
                self._birth_procedure_removed = ()        # traits the procedure took away; the undo gives them back

                self._on_pill = False
                self._on_placebo = False
                self._pill_missed = 0
                self._pill_days_active = 0
                self._morning_after_uses = 0
                self._morning_after_regen_day = None   # Day the plan B regen clock started (None = not running)
                self._last_inside_day = None           # last Day he finished inside her raw, as far as she knows (plan B window)

                self._cycle_offset = 0


                # ---------- Weekly schedule (7 days x 4 time slots) ----------
                self.schedule = [
                    ["campus", "campus", "campus", "room"],
                    ["campus", "campus", "pool",   "room"],
                    ["campus", "campus", "campus", "room"],
                    ["campus", "campus", "pool",   "room"],
                    ["campus", "campus", "campus", "room"],
                    ["campus", "pool",   "pool",   "room"],
                    ["campus", "campus", "pool",   "room"],
                ]

                # Location
                self.home = "room"
                self.loc = self.home
                self._prev_scheduled_loc = None
                self.loc_override = None
                self.SpriteLoc = None

                # ==================================================
                # CLOTHING STATE — unified dict model
                # ==================================================
                self.clothes = {
                    "over": None, "mid": None, "chest": None, "skirt": None,
                    "panties": None, "shoes": None,
                }
                self.clothes_state = {
                    "over": "full", "mid": "full", "chest": "full", "skirt": "full",
                    "panties": "full", "shoes": "full",
                }

                self.Collar = self.Id in _COLLAR_GIRLS
                self.Piercing = False
                self._bikini_unlocked = False
                self.CurrentOutfitPreset = None

                # Legacy compat — old code uses girl.Over, girl.OverUp etc.
                # These now read/write from self.clothes / self.clothes_state
    # --- Legacy property shims (defined after class) ---


            # ------------------------------
            # Traits & Flags
            # ------------------------------
            def has_trait(self, trait_name):
                return trait_name in self.traits

            def add_trait(self, trait_name):
                if not trait_name:
                    return
                self.traits.add(trait_name)

                # Sync common flags
                if trait_name == "virgin":
                    self.flags["virgin"] = True
                elif trait_name == "camera_lover":
                    self.flags["likes_camera"] = True
                elif trait_name == "camera_hater":
                    self.flags["hates_camera"] = True
                elif trait_name == "cheater":
                    # Cheater starts at love_cheating
                    self.CheatAttitude = 6
                elif trait_name == "loyal":
                    # Loyal starts at hate_cheat unless overridden by config
                    if self.CheatAttitude < 2:
                        self.CheatAttitude = 1
                    else:
                        self.CheatAttitude = min(self.CheatAttitude, 2)
                elif trait_name == "lesbian":
                    self.sexuality_spectrum = 100
                elif trait_name == "bisexual":
                    self.sexuality_spectrum = 50
                elif trait_name == "pregnancy_fetish":
                    if "cum_slut" not in self.traits:
                        self.add_trait("cum_slut")

            def remove_trait(self, trait_name):
                if not trait_name:
                    return
                self.traits.discard(trait_name)
                # Sync flags on removal
                if trait_name == "camera_hater":
                    self.flags["hates_camera"] = False
                elif trait_name == "camera_lover":
                    self.flags["likes_camera"] = False

            def _corruption_notify(self, banner_text, narration):
                """Play sound, show discovery banner, and narrate a corruption event."""
                _bj_paused = False
                _bj = getattr(store, '_bj_girl', None)
                if _bj is self and not getattr(store, '_bj_head_normal', False):
                    _bj_paused = _bj_pause_for_narration(self)

                renpy.music.play("audio/Information.mp3", channel="notify_sfx", loop=False)
                renpy.show_screen("discovery_banner", girl_name=self.Name, info_text=banner_text)
                renpy.say(None, narration)

                if _bj_paused:
                    _bj_resume_from_narration(self)

            def check_corruption(self, category=None):
                """Check corruption thresholds and swap traits via CORRUPTION_RULES."""
                if not getattr(store, "corruption_enabled", False):
                    return
                cats = [category] if category else list(CORRUPTION_RULES.keys())
                for cat in cats:
                    rule = CORRUPTION_RULES.get(cat)
                    if not rule:
                        continue
                    _default_counter = rule.get("counter")
                    for stage in rule["stages"]:
                        _counter_fn = stage.get("counter", _default_counter)
                        if _counter_fn is None:
                            continue
                        _count_val = _counter_fn(self)
                        _threshold = stage["threshold"]
                        if _count_val < _threshold:
                            print("[CORRUPTION] %s cat=%s: count=%d < threshold=%d, skip" % (self.gid, cat, _count_val, _threshold))
                            continue
                        if stage.get("requires") and not self.has_trait(stage["requires"]):
                            print("[CORRUPTION] %s cat=%s: count=%d >= %d but missing required trait '%s'" % (self.gid, cat, _count_val, _threshold, stage["requires"]))
                            continue
                        if stage.get("blocks") and self.has_trait(stage["blocks"]):
                            print("[CORRUPTION] %s cat=%s: count=%d >= %d but blocked by trait '%s'" % (self.gid, cat, _count_val, _threshold, stage["blocks"]))
                            continue
                        # Canon lock: a canon trait never goes, a trait she can never have never comes (enforce_canon_traits
                        # would undo it on the next load anyway). A canon whose break gate is open (CANON_BREAK_RULES,
                        # e.g. femdom after her final story step) passes; its opposite may come in the same stage.
                        _rm = stage.get("remove")
                        _rm_canon = _rm in girl_canon_traits(self) if _rm else False
                        _rm_locked = _rm_canon and not trait_canon_breakable(self, _rm)
                        if _rm_locked or (
                                stage.get("add") and not trait_possible_for(
                                    self, stage["add"], ignoring=(_rm if (_rm_canon and not _rm_locked) else None))):
                            print("[CORRUPTION] %s cat=%s: count=%d >= %d but her canon / girl type forbids it (remove=%s add=%s)" % (
                                self.gid, cat, _count_val, _threshold, stage.get("remove"), stage.get("add")))
                            continue
                        print("[CORRUPTION] %s cat=%s: FIRING stage (count=%d >= %d, add=%s remove=%s)" % (self.gid, cat, _count_val, _threshold, stage.get("add"), stage.get("remove")))
                        _had = False
                        if _rm:
                            _had = self.has_trait(_rm)
                            self.remove_trait(_rm)
                            if _rm_canon:
                                # the broken canon stays broken: girl_canon_traits skips it from now on
                                self._canon_lost = set(getattr(self, "_canon_lost", None) or ()) | {_rm}
                                print("[CORRUPTION] %s: canon trait %s broken for good (_canon_lost=%s)" % (
                                    self.gid, _rm, sorted(self._canon_lost)))
                        _add = stage.get("add")
                        if _add:
                            self.add_trait(_add)
                        if _had or (_rm and _rm in self.evolved_traits):
                            # the later stage of a chain updates the mapping (femdom: None at 15 -> submissive at 30)
                            self.evolved_traits[_rm] = _add
                        if stage.get("discover"):
                            self.discover(stage["discover"])
                        if stage.get("achievement"):
                            unlock_achievement(stage["achievement"])
                        self._corruption_notify(_tl(stage["banner"]), _tl_fmt(stage["narration"], self.Name))
                        break

            def set_flag(self, key, value=True):
                self.flags[str(key)] = bool(value)

            def get_flag(self, key, default=False):
                return bool(self.flags.get(str(key), default))

            def clear_flag(self, key):
                """Remove a flag entirely (get_flag then returns its default)."""
                self.flags.pop(str(key), None)

            def discover(self, key):
                """Set a discovery flag. Plays notification sound and shows banner if new."""
                k = str(key)
                if not self.flags.get(k, False):
                    self.flags[k] = True

                    # The two virginity keys stay in sync (one banner only): "discovered_virgin" = her status is
                    # known (the card's Virginity row, context banner below), "discovered_trait_virgin" = the
                    # Virgin chip. Half the game wrote one, half the other, and the chip never lit up.
                    if k == "discovered_virgin" and self.has_trait("virgin"):
                        self.flags["discovered_trait_virgin"] = True
                    elif k == "discovered_trait_virgin":
                        self.flags["discovered_virgin"] = True

                    # Map known discovery keys to readable banner text
                    _banner_map = {
                        "discovered_has_partner": _tr("She is dating someone"),
                        "discovered_single": _tr("She has no boyfriend"),
                        "discovered_study_level": _tr("Study habits discovered"),
                        "discovered_fav_act": _tr("Favorite act discovered"),
                        "discovered_fav_dish": _tr("Favorite food discovered"),
                        "discovered_fav_drink": _tr("Favorite drink discovered"),
                        "discovered_fav_brand": _tr("Favorite brand discovered"),
                        "discovered_petname_given": _tr("She accepted your petname"),
                        "discovered_petname_for_player": _tr("She has a name for you"),
                        "player_first_kiss": _tr("Her first kiss"),
                        "player_first_hj": _tr("You're her first handjob"),
                        "player_first_tj": _tr("You're her first titjob"),
                        "player_first_bj": _tr("You're her first blowjob"),
                        "player_first_masturbate": _tr("She's never done this for anyone"),
                        "player_first_sex": _tr("You took her virginity"),
                        "player_first_anal": _tr("You're her first anal"),
                        "player_first_sex_raw": _tr("First time raw"),
                        "player_first_creampie": _tr("First creampie"),
                        "player_first_pregnancy": _tr("You got her pregnant"),
                        "discovered_trait_poor": _tr("She struggles with money"),
                        "discovered_trait_rich": _tr("She comes from money"),
                        "discovered_pill": _tr("Birth control status discovered") + "\n" + _tr("Check Fertility in her contact"),
                        "discovered_cycle": _tr("Fertility cycle discovered") + "\n" + _tr("Check Fertility in her contact"),
                    }
                    _text = _banner_map.get(k, None)

                    # Virginity — context-aware text
                    if k == "discovered_virgin":
                        if getattr(self, "virginity_taken_by_player", False):
                            _text = _tr("You took her virginity")
                        elif self.has_trait("virgin"):
                            _text = _tr("She's a virgin")
                        else:
                            _text = _tr("She's not a virgin")

                    # BF history discoveries
                    if _text is None and k.startswith("discovered_bf_never_"):
                        _act = k.replace("discovered_bf_never_", "")
                        _act_labels = {
                            "hj": "handjob", "tj": "titjob", "bj": "blowjob",
                            "masturbate": "masturbation", "sex": "sex",
                            "sex_raw": "raw sex", "creampie": "creampie",
                            "anal": "anal",
                        }
                        _act_name = _tl(_act_labels.get(_act, _act))
                        _p_label = _tr("GF") if self.get_flag("partner_is_female") else _tr("BF")
                        _text = "%s %s: %s" % (_p_label, _tr("never did"), _act_name)
                    if _text is None and k.startswith("discovered_bf_done_"):
                        _act = k.replace("discovered_bf_done_", "")
                        _act_labels = {
                            "hj": "handjob", "tj": "titjob", "bj": "blowjob",
                            "masturbate": "masturbation", "sex": "sex",
                            "sex_raw": "raw sex", "creampie": "creampie",
                            "anal": "anal",
                        }
                        _act_name = _tl(_act_labels.get(_act, _act))
                        _p_label = _tr("GF") if self.get_flag("partner_is_female") else _tr("BF")
                        _text = "%s %s: %s" % (_p_label, _tr("has done"), _act_name)

                    # Trait discoveries
                    if _text is None and k.startswith("discovered_trait_"):
                        _trait_key = k.replace("discovered_trait_", "")
                        _trait_descriptions = {
                            "camera_lover": "She loves being on camera",
                            "camera_hater": "She hates cameras",
                            "cum_slut": "She loves cum",
                            "hate_cum": "She hates cum",
                            "hardcore_sex": "She likes it rough",
                            "cute_sex": "She likes it gentle",
                            "femdom": "She likes to be in charge",
                            "submissive": "She likes being told what to do",
                            "virgin": "She's a virgin",
                            "cheater": "She's open to cheating",
                            "loyal": "She's very loyal",
                            "public_fetish": "She likes doing it in public",
                            "public_shy": "She's terrified of public exposure",
                            "exhibitionist": "She likes being watched",
                            "voyeur": "She likes watching others",
                            "polyamorous": "She's open to sharing her partner",
                            "monogamous": "She demands exclusivity",
                            "anal_lover": "She loves anal",
                            "anal_hater": "She hates anal",
                            "lesbian": "She's only attracted to women",
                            "bisexual": "She's attracted to both men and women",
                            "experienced": "She has done everything with her partner",
                            "has_boyfriend": "She already has a boyfriend",
                            "has_girlfriend": "She already has a girlfriend",
                            "married": "She's married",
                            "poor": "She struggles financially",
                            "rich": "She comes from a wealthy background",
                            "heavy_drinker": "She can hold her liquor",
                            "lightweight": "She can't handle her drinks",
                            "nerd": "She's a total bookworm",
                            "gym_rat": "She lives at the gym",
                            "breedable": "Extra breedable",
                            "infertile": "Infertile",
                            "pregnancy_fetish": "She has a pregnancy fetish",
                            "pregnancy_fear": "She's terrified of getting pregnant",
                        }
                        _trait_desc = _trait_descriptions.get(_trait_key, None)
                        if _trait_desc:
                            _text = _tr("New Trait Discovered") + "\n" + _tr(_trait_desc)
                        else:
                            _text = None

                    # Her taste in a gift (shop.rpy gift_taste_aside)
                    if _text is None and k.startswith("discovered_gift_taste_"):
                        _text = _tr("Her taste in gifts discovered")

                    # Skip banner for generic relationship discovery and unknown keys
                    if k == "discovered_relationship":
                        _text = None

                    if _text is not None:
                        renpy.music.play("audio/Information.mp3", channel="notify_sfx", loop=False)
                        renpy.show_screen("discovery_banner", girl_name=self.Name, info_text=_text, name_color=self.color)


            # ------------------------------
            # Commitment helpers
            # ------------------------------
            def has_npc_partner(self):
                return self.get_flag("has_npc_partner") and (self.npc_partner_id is not None)

            def has_npc_girlfriend(self):
                return self.has_npc_partner() and self.get_flag("partner_is_female")

            def partner_label(self):
                if self.get_flag("partner_is_female"):
                    return _tr("girlfriend")
                return _tr("boyfriend")

            def partner_name(self):
                try:
                    npc = get_npc_partner_for(self)
                    if npc and getattr(npc, "name", None):
                        return npc.name
                except Exception:
                    pass
                gp_id = getattr(self, "girl_partner_id", None)
                if gp_id:
                    gp = GIRL_BY_ID.get(gp_id)
                    if gp:
                        return gp.Name
                return self.partner_label()

            # Read-only alias of partner_name() for Ren'Py text: "[girl.npc_partner_name]" cannot call a
            # method. pregnancy_discovery.rpy interpolates it in two menu captions; the attribute never
            # existed (only _npc_partner_name), so those menus raised AttributeError when displayed.
            npc_partner_name = property(lambda self: self.partner_name())

            def has_girl_partner(self):
                return self.get_flag("has_girl_partner") and (self.girl_partner_id is not None)

            # ---------- NPC partner assignment (CENTRAL) ----------
            # create_npc_partner() registers the NPC under one of these ids and get_npc_partner_for()
            # looks it up by self.npc_partner_id: the id, the partner_is_female flag and NPCPartner.gender
            # must always agree. EVERY assign / restore goes through set_npc_partner(), never the raw fields.
            _NPC_PARTNER_ID_PREFIX = {"male": "npc_bf_", "female": "npc_gf_"}

            def npc_partner_canonical_id(self, gender):
                return self._NPC_PARTNER_ID_PREFIX[gender] + (getattr(self, "gid", None) or self.Id)

            def resolve_npc_partner_gender(self, npc_id=None, gender=None):
                """Gender of a partner being assigned or restored. Order: explicit gender, canonical id
                prefix (npc_gf_ / npc_bf_), her orientation (lesbian / has_girlfriend = female), male."""
                if gender in self._NPC_PARTNER_ID_PREFIX:
                    return gender
                _id = str(npc_id or "")
                for _g, _prefix in self._NPC_PARTNER_ID_PREFIX.items():
                    if _id.startswith(_prefix):
                        return _g
                if self.has_trait("lesbian") or self.has_trait("has_girlfriend"):
                    return "female"
                return "male"

            # ---------- Per-partner state mirrored on the girl (CENTRAL) ----------
            # Girls are init-time objects and NPC_PARTNERS is rebuilt from the GIRL (only _girl_save reaches
            # the save file), so everything that describes ONE partner lives on her. Value = neutral state;
            # None on an identity key makes create_npc_partner() / NPCPartner.__init__ roll it again.
            # Applied by _reset_npc_partner_mirrors() when a NEW person becomes her partner, NEVER when the
            # same ex comes back (restore_ex_npc_partner). A new per-partner attribute goes HERE.
            # Left out on purpose: _npc_catch_msg_* (HER texts about the breakup, still to be delivered),
            # _npc_paternity_* / _npc_pregnancy_* (pregnancy.rpy _PREG_SCOPED_FLAGS, scope "partner", wiped by
            # clear_npc_partner), bf_history / bf_max_tier / bf_loyalty (re-rolled by set_npc_partner) and her
            # own cheating progression (_cheat_*, CheatAttitude: that is HER, not the partner).
            _NPC_PARTNER_MIRRORS = {
                # identity
                "_npc_partner_name": None,
                "_npc_guest_number": None,
                "_npc_partner_schedule": None,
                "_npc_partner_traits": None,
                # relationship stats (NPCPartner defaults)
                "_npc_friendship": 200,
                "_npc_love": 750,
                "_npc_suspicion": 0,
                # NTR arrangement + what the player discovered about it
                "_ntr_active": False,
                "_ntr_boundary_level": None,
                "_ntr_boundary_bar": 0,
                "_ntr_boundary_discovered": False,
                "_ntr_trust_discovered": False,
                # next-day queues that belong to the previous partner
                "_ntr_levelup_pending": False,
                "_ntr_activation_pending": False,
                "_ntr_activation_msg_pending": False,
                "_ntr_activation_msg_list": [],
                "_ntr_activation_msg_npc_id": None,
                "_ntr_discovery_pending": False,
                "_ntr_discovery_npc_id": None,
                "_ntr_discovery_was_violation": False,
                "_ntr_discovery_violation_act": None,
                "_ntr_violation_pending": False,
                "_ntr_video_seen_pending": False,
                "_npc_video_pending": False,
                "_npc_secret_vid_angry": False,
                "_npc_catch_pending": False,
                "_npc_catch_pending_day": 0,
                "_npc_catch_pending_ti": 0,
                "_npc_suspicion_pending": False,
                # history with that partner
                "_npc_catch_count": 0,
                "_npc_gifts_given": set(),
                "_npc_partner_received_nerd_gift": False,
                "_will_break_up_with_partner": False,
                # hardcore: the ex she could go back to, and the partner's act escalation clock
                "_hc_bf_dumped_day": 0,
                "_hc_bf_dumped_npc": None,
                "_hc_bf_next_escalation_day": 0,
            }
            # Families created on the fly, one attribute / flag per act
            _NPC_PARTNER_ATTR_PREFIXES = ("_ntr_afterscene_shown_",)
            _NPC_PARTNER_FLAG_PREFIXES = ("discovered_bf_never_", "discovered_bf_done_")
            _NPC_PARTNER_FLAGS = ("discovered_single",)

            def _reset_npc_partner_mirrors(self, reason=""):
                """A NEW person becomes her NPC partner: wipe what described the previous one, so
                create_npc_partner() / NPCPartner.__init__ roll everything again. Single writer of that wipe,
                driven by _NPC_PARTNER_MIRRORS + the prefix / flag families above. Called by set_npc_partner()
                only, and never with keep_history=True (the same ex coming back keeps every mirror)."""
                import copy as _copy
                _gid = getattr(self, "gid", None) or self.Id
                _old_name = getattr(self, "_npc_partner_name", None)
                _ex_names = getattr(self, "_npc_ex_names", None)
                if _ex_names is None:
                    _ex_names = self._npc_ex_names = []
                if _old_name and _old_name not in _ex_names:
                    _ex_names.append(_old_name)   # NPCPartner.__init__ never gives an ex's name to a new partner
                _changed = []
                for _attr, _neutral in self._NPC_PARTNER_MIRRORS.items():
                    if getattr(self, _attr, _neutral) != _neutral:
                        _changed.append(_attr)
                    setattr(self, _attr, _copy.deepcopy(_neutral))
                for _attr in [_a for _a in vars(self) if _a.startswith(self._NPC_PARTNER_ATTR_PREFIXES)]:
                    delattr(self, _attr)
                    _changed.append(_attr)
                _flags = getattr(self, "flags", None) or {}
                for _flag in [_f for _f in _flags if _f in self._NPC_PARTNER_FLAGS or _f.startswith(self._NPC_PARTNER_FLAG_PREFIXES)]:
                    self.clear_flag(_flag)
                    _changed.append("flag:" + _flag)
                print("[NPC_PARTNER] %s: per-partner mirrors reset (%s). Previous partner: %s. Exes: %s. Cleared: %s" % (
                    _gid, reason, _old_name, _ex_names, ", ".join(_changed) or "nothing"))

            def set_npc_partner(self, npc_id, gender=None, keep_history=False):
                """Give her an NPC partner. gender None = derived by resolve_npc_partner_gender().
                Default = a NEW person: the slot is emptied (clear_npc_partner), every per-partner mirror is
                wiped (_reset_npc_partner_mirrors) so create_npc_partner() rolls name, sprite, traits, schedule,
                stats and NTR state again, and what the player holds under the reused id (number, thread,
                groups) is forgotten (npc_partner_forget_identity).
                keep_history=True: the SAME person comes back (hardcore ex return): nothing is re-rolled,
                neither the mirrors nor what she did with him / her. The stored id is always the canonical
                one for that gender."""
                if not npc_id:
                    self.clear_npc_partner()
                    return
                _gender = self.resolve_npc_partner_gender(npc_id, gender)
                _canon_id = self.npc_partner_canonical_id(_gender)
                if not keep_history:
                    self.clear_npc_partner()   # a new person always starts from an empty slot (registry + pregnancy partner flags)
                    self._reset_npc_partner_mirrors("new partner %s" % _canon_id)
                    if callable(globals().get("npc_partner_forget_identity", None)):
                        # ids are canonical per girl + gender: whoever comes next reuses them, whatever the ex's gender was
                        for _g in sorted(self._NPC_PARTNER_ID_PREFIX):
                            npc_partner_forget_identity(self.npc_partner_canonical_id(_g), "new partner of %s" % (getattr(self, "gid", None) or self.Id))
                self.npc_partner_id = _canon_id
                self.set_flag("has_npc_partner", True)
                self.set_flag("partner_is_female", _gender == "female")
                if not keep_history:
                    self._generate_bf_history()
                base = 750
                if self.has_trait("loyal"):
                    base = 900
                elif self.has_trait("cheater"):
                    base = 500
                self.bf_loyalty = base
                self._ensure_npc_partner_visual()
                store._npc_partner_cleared = set(getattr(store, "_npc_partner_cleared", set())) - {self.gid}
                print("[NPC_PARTNER] %s: partner set id=%s (asked %s) gender=%s keep_history=%s" % (
                    self.Id, _canon_id, npc_id, _gender, keep_history))

            def set_npc_partner_female(self, npc_id):
                self.set_npc_partner(npc_id, gender="female")

            def restore_ex_npc_partner(self):
                """Hardcore "she goes back to her ex" (_hc_bf_return_event). The ex is the SAME person: name,
                sprite number, traits, schedule, friendship / love / suspicion and the NTR state are still
                mirrored on the girl (clear_npc_partner never wipes them), so only the id and the gender
                have to come back. Gender is read from the id saved at the breakup; a save without one
                falls back to her orientation."""
                _saved = getattr(self, "_hc_bf_dumped_npc", None)
                _gender = self.resolve_npc_partner_gender(_saved)
                self.set_npc_partner(self.npc_partner_canonical_id(_gender), gender=_gender, keep_history=True)
                print("[HC_RETURN] %s: back with her ex, saved id=%s gender=%s name=%s" % (
                    self.gid, _saved, _gender, getattr(self, "_npc_partner_name", None)))

            def clear_npc_partner(self):
                old_id = self.npc_partner_id
                if "NPC_PARTNERS" in dir(store):
                    # By owner, not by id: an id that never matched the registry key must not leave her NPC behind
                    _own_gid = getattr(self, "gid", None) or self.Id
                    for _pid in [_p for _p, _n in store.NPC_PARTNERS.items() if getattr(_n, "girl_gid", None) == _own_gid]:
                        store.NPC_PARTNERS[_pid].hide_sprite()
                        del store.NPC_PARTNERS[_pid]
                        debug_log("[NPC_PARTNER] Removed %s (girl id was %s)" % (_pid, old_id))
                self.npc_partner_id = None
                self.set_flag("has_npc_partner", False)
                self.set_flag("partner_is_female", False)
                # Pregnancy flags that describe THIS partner (paternity claim, queued confrontation,
                # save attempt) end with him: the next partner must not inherit "I'm gonna be a dad".
                if callable(globals().get("_pregnancy_reset_flags", None)):
                    _pregnancy_reset_flags(self, "partner", "clear_npc_partner old=%s" % old_id)
                store._npc_partner_cleared = set(getattr(store, "_npc_partner_cleared", set())) | {self.gid}

            def _ensure_npc_partner_visual(self):
                if not self.has_npc_partner():
                    return
                if not callable(globals().get("create_npc_partner", None)):
                    return
                gender = "female" if self.get_flag("partner_is_female") else "male"
                create_npc_partner(self, gender=gender)

            # ---------- Lesbian helpers ----------

            def gain_blackmail_leverage(self, amount=1):
                if not self.has_trait("lesbian") and not self.has_npc_partner():
                    return
                old = getattr(self, "_blackmail_leverage", 0)
                self._blackmail_leverage = min(3, old + int(amount))
                debug_log("[DEBUG] %s blackmail_leverage: +%d = %d" % (self.gid, amount, self._blackmail_leverage))

            def apply_spectrum_temp_shift(self, amount):
                old = getattr(self, "_spectrum_temp_shift", 0)
                self._spectrum_temp_shift = min(50, old + int(amount))
                debug_log("[DEBUG] %s spectrum_temp_shift: +%d = %d" % (self.gid, amount, self._spectrum_temp_shift))

            # ---------- BF Loyalty helpers ----------

            def change_bf_loyalty(self, amount):
                """Change bf_loyalty by amount, clamped to 0-1000."""
                if not hasattr(self, "bf_loyalty"):
                    self.bf_loyalty = 750
                old = self.bf_loyalty
                self.bf_loyalty = max(0, min(1000, self.bf_loyalty + int(amount)))
                return self.bf_loyalty - old

            def bf_loyalty_tier(self):
                """Return tier string based on bf_loyalty value.
                0-250: miserable, 250-500: strained, 500-750: normal, 750-1000: in_love"""
                v = int(getattr(self, "bf_loyalty", 750))
                if v < 250:
                    return "miserable"
                elif v < 500:
                    return "strained"
                elif v < 750:
                    return "normal"
                else:
                    return "in_love"

            def bf_loyalty_label(self):
                """Human-readable label for phone screen (English, _() = marker: the status chip shows it as a
                whole string, which translates it)."""
                if self.get_flag("partner_is_female"):
                    _LABELS = {
                        "miserable": _("Thinks she's boring"),
                        "strained": _("Losing interest"),
                        "normal": _("Likes her GF"),
                        "in_love": _("Loves her GF"),
                    }
                else:
                    _LABELS = {
                        "miserable": _("Thinks he's boring"),
                        "strained": _("Losing interest"),
                        "normal": _("Likes her BF"),
                        "in_love": _("Loves her BF"),
                    }
                return _LABELS.get(self.bf_loyalty_tier(), "???")

            def bf_loyalty_color(self):
                """Color for phone screen display."""
                _COLORS = {
                    "miserable": "#4ade80",   # green = good for player
                    "strained": "#facc15",    # yellow
                    "normal": "#fb923c",      # orange
                    "in_love": "#f87171",     # red = hard to steal
                }
                return _COLORS.get(self.bf_loyalty_tier(), "#8ca0b4")

            def bf_loyalty_daily_regen(self):
                """Called once per day. Loyalty slowly recovers toward 750 if player
                didn't interact. Loyal girls recover faster, cheaters slower."""
                if not self.has_npc_partner():
                    return
                if not hasattr(self, "bf_loyalty"):
                    self.bf_loyalty = 750
                # Only regen if no player interaction today
                _today_actions = getattr(self, "Daily_Actions", [])
                _had_player_contact = any(a for a in _today_actions if a.startswith("flirt_") or a.startswith("sex_") or a == "gift_given")
                if _had_player_contact:
                    return
                # Regen amount
                regen = 8
                if self.has_trait("loyal"):
                    regen = 15
                elif self.has_trait("cheater"):
                    regen = 3
                # Don't regen above 750 (cap at "normal" without effort)
                cap = 750
                if self.has_trait("loyal"):
                    cap = 900
                if self.bf_loyalty < cap:
                    self.bf_loyalty = min(cap, self.bf_loyalty + regen)

            # ----------------------------------------------------------
            # Hardcore Relationship Mode — daily tick + BF escalation
            # ----------------------------------------------------------
            def hardcore_relationship_tick(self):
                """Called once per day when hardcore_relationship is enabled.
                Phase 1: bf_loyalty boost + Love decay when player neglects.
                Phase 2: BF act escalation when bf_loyalty >= 1000."""
                _day = getattr(store, "Day", 1)
                if girl_is_away(self):
                    self._hc_last_interaction_day = _day
                    print("[HC_TICK] %s day=%d: away, clock frozen" % (self.gid, _day))
                    return
                if not self.has_npc_partner():
                    self._hc_single_neglect_tick()
                    return

                if _day <= 10:
                    return

                if self.Love >= 1000:
                    if not getattr(self, "_hc_love_maxed_notified", False):
                        self._hc_love_maxed_notified = True
                        _platonic = getattr(store, "_hc_platonic", [])
                        _npc_p = get_npc_partner_for(self) if self.has_npc_partner() else None
                        _fem_p = _npc_p.gender == "female" if _npc_p else False
                        _platonic.append((self.Name, _fem_p))
                        store._hc_platonic = _platonic
                    print("[HC_TICK] %s day=%d: Love=%d >= 1000, drift stopped" % (self.gid, _day, self.Love))
                    return

                _last = getattr(self, "_hc_last_interaction_day", 0)
                if _last >= _day - 1:
                    print("[HC_TICK] %s day=%d: last_interaction=%d (recent), skip" % (self.gid, _day, _last))
                    return
                print("[HC_TICK] %s day=%d: last_interaction=%d, neglect=%d days, loyalty=%d" % (self.gid, _day, _last, _day - _last, self.bf_loyalty))

                # --- Phase 1: daily drift when neglected ---
                self.hc_drift_one_day("neglected")

                # Queue warning if 2+ days without contact
                _days_since = _day - _last
                if _days_since >= 2 and _last > 0:
                    _warns = getattr(store, "_hc_warnings", [])
                    _warns.append((self.Name, self.get_flag("partner_is_female")))
                    store._hc_warnings = _warns

                # --- Phase 2: BF act escalation at max loyalty ---
                if self.bf_loyalty >= 1000:
                    _next = getattr(self, "_hc_bf_next_escalation_day", 0)
                    if _next == 0:
                        self._hc_bf_next_escalation_day = _day + renpy.random.randint(1, 3)
                        print("[HC_TICK] %s Phase2: loyalty=%d, first escalation scheduled day=%d" % (self.gid, self.bf_loyalty, self._hc_bf_next_escalation_day))
                    elif _next > 0 and _day >= _next:
                        _act = self._hc_escalate_bf_act()
                        if _act:
                            self._hc_bf_next_escalation_day = _day + renpy.random.randint(1, 3)
                            _escs = getattr(store, "_hc_escalations", [])
                            _escs.append((self.Name, self.get_flag("partner_is_female")))
                            store._hc_escalations = _escs
                            print("[HC_TICK] %s Phase2: ESCALATED bf_history=%s next=%d" % (self.gid, getattr(self, "bf_history", {}), self._hc_bf_next_escalation_day))
                        else:
                            self._hc_bf_next_escalation_day = -1
                            print("[HC_TICK] %s Phase2: all tiers done" % self.gid)
                    elif _next > 0:
                        print("[HC_TICK] %s Phase2: waiting (next=%d, today=%d)" % (self.gid, _next, _day))

            def hc_drift_one_day(self, why):
                """Hardcore: one day away from him pulls her toward her partner (bf_loyalty up, Love down; low Obed
                = faster). The neglect tick.
                Never through Change_Status: that counts as an interaction (_hc_last_interaction_day)."""
                _bonus = 50
                if self.has_trait("loyal"):
                    _bonus = 80
                elif self.has_trait("cheater"):
                    _bonus = 20
                self.change_bf_loyalty(_bonus)

                # Love decay: low Obed = faster decay
                _base = -4
                _obed_factor = 1.0 + (1000 - self.Obed) / 1000.0
                _love_loss = int(_base * _obed_factor)
                self.Love = max(0, self.Love + _love_loss)
                _sync_girl(self)
                print("[HC_TICK] %s drifts one day (%s): bf_loyalty +%d -> %d, Love %d -> %d" % (
                    self.gid, why, _bonus, self.bf_loyalty, self.Love - _love_loss, self.Love))

            def _hc_escalate_bf_act(self):
                """Unlock the next BF sexual act. Returns True if escalated."""
                if self.has_trait("lesbian"):
                    return None
                if self.has_trait("bisexual") and self.get_flag("partner_is_female"):
                    return None
                _ORDER = [
                    (0, ["kiss"]),
                    (1, ["hj", "masturbate"]),
                    (2, ["tj"]),
                    (3, ["bj"]),
                    (4, ["sex"]),
                    (5, ["sex_raw"]),
                    (6, ["creampie"]),
                ]
                if not hasattr(self, "bf_history"):
                    self.bf_history = {
                        "kiss": False,
                        "hj": False, "masturbate": False, "tj": False,
                        "bj": False, "sex": False, "sex_raw": False, "creampie": False,
                    }
                if "kiss" not in self.bf_history:
                    self.bf_history["kiss"] = False
                for tier, acts in _ORDER:
                    if not all(self.bf_history.get(a, False) for a in acts):
                        for a in acts:
                            self.bf_history[a] = True
                            # Clear stale "never" discovery so player can re-discover
                            if self.get_flag("discovered_bf_never_%s" % a):
                                self.set_flag("discovered_bf_never_%s" % a, False)
                        self.bf_max_tier = max(getattr(self, "bf_max_tier", 0), tier)
                        # If she was known virgin and BF escalates to sex,
                        # mark virginity as uncertain (not confirmed lost)
                        if tier == 4 and self.has_trait("virgin"):
                            self.remove_trait("virgin")
                            self.set_flag("virgin", False)
                            self._hc_virginity_uncertain = True
                            # Clear virginity discovery so player can re-discover (both keys: row and chip)
                            if self.get_flag("discovered_virgin"):
                                self.set_flag("discovered_virgin", False)
                            if self.get_flag("discovered_trait_virgin"):
                                self.set_flag("discovered_trait_virgin", False)
                        _sync_girl(self)
                        return True
                return None

            def _hc_single_neglect_tick(self):
                """Hardcore mode: track neglect for single (partnerless) girls.
                Day 5 warning, day 10 warning, day 15-20 partner spawn."""
                _day = getattr(store, "Day", 1)
                if _day <= 10:
                    return
                # A girl who can never have a boyfriend or girlfriend (married, girl type) never finds one here
                if not trait_possible_for(self, "has_boyfriend") and not trait_possible_for(self, "has_girlfriend"):
                    return

                _last = getattr(self, "_hc_last_interaction_day", 0)
                if _last == 0:
                    return
                if _last >= _day - 1:
                    return

                _days_since = _day - _last

                # Check if spawn day reached (before warnings, so it fires on the right day)
                _spawn = getattr(self, "_hc_partner_spawn_day", 0)
                if _spawn > 0 and _day >= _spawn:
                    self._hc_spawn_neglect_partner()
                    return

                if _days_since >= 10 and getattr(self, "_hc_single_warned", 0) < 2:
                    self._hc_single_warned = 2
                    _warns = getattr(store, "_hc_single_warnings", [])
                    _warns.append((self.Name, 2))
                    store._hc_single_warnings = _warns
                    _loss = max(50, int(self.Love * 0.25))
                    self.Love = max(0, self.Love - _loss)
                    self._hc_partner_spawn_day = _last + renpy.random.randint(15, 20)
                    _sync_girl(self)
                    print("[HC_SINGLE] %s day-10 warning. Love -%d. Spawn day: %d" % (self.gid, _loss, self._hc_partner_spawn_day))

                elif _days_since >= 5 and getattr(self, "_hc_single_warned", 0) < 1:
                    self._hc_single_warned = 1
                    _warns = getattr(store, "_hc_single_warnings", [])
                    _warns.append((self.Name, 1))
                    store._hc_single_warnings = _warns
                    _loss = max(25, int(self.Love * 0.10))
                    self.Love = max(0, self.Love - _loss)
                    _sync_girl(self)
                    print("[HC_SINGLE] %s day-5 warning. Love -%d" % (self.gid, _loss))

            def _hc_spawn_neglect_partner(self):
                """Spawn a partner for a neglected single girl."""
                if self.has_trait("lesbian"):
                    _gender = "female"
                elif self.has_trait("bisexual"):
                    _gender = renpy.random.choice(["male", "female"])
                else:
                    _gender = "male"

                # NEW person: set_npc_partner() wipes the per-partner mirrors and creates the NPC itself.
                # (The second create_npc_partner() that used to sit here was the only reason the new partner
                # got a new name: the first NPC was still registered, so the saved name counted as "taken".)
                self.set_npc_partner(self.npc_partner_canonical_id(_gender), gender=_gender)
                _npc = get_npc_partner_for(self)

                _flags = getattr(self, "intimacy_flags", set()) or set()
                if bool(_flags):
                    self._hc_was_abandoned = True

                _loss = max(100, int(self.Love * 0.50))
                self.Love = max(0, self.Love - _loss)
                self.bf_loyalty = 800
                self._hc_partner_spawn_day = 0
                _sync_girl(self)

                _npc_name = _npc.Name if _npc else "someone"
                _notifs = getattr(store, "_hc_new_partner", [])
                _notifs.append((self.Name, _npc_name))
                store._hc_new_partner = _notifs
                print("[HC_SINGLE] %s got a %s partner: %s. Abandoned=%s, Love -%d" % (self.gid, _gender, _npc_name, self._hc_was_abandoned, _loss))

            def gf_like_tier(self, gf_gid):
                """How much she likes the player's GF — determines tone when helping player cheat.
                Uses Girl_like[gf_gid] (0-1000). Higher = harder to help cheat.
                Returns: close / friendly / distant / hostile"""
                v = int(self.Girl_like.get(gf_gid, 500))
                if v >= 750:
                    return "close"
                elif v >= 500:
                    return "friendly"
                elif v >= 250:
                    return "distant"
                else:
                    return "hostile"

            def set_girl_partner(self, girl_id):
                self.girl_partner_id = girl_id
                self.set_flag("has_girl_partner", bool(girl_id))

            def clear_girl_partner(self):
                self.girl_partner_id = None
                self.set_flag("has_girl_partner", False)

            def _reset_partner_firsts(self):
                """New NPC partner: the "player did it before her partner" keys start over (his history was just
                re-rolled). Every other key is the player's own milestone (first_pregnancy, force_throat...): kept."""
                _partner_keys = ("kiss", "hj", "masturbate", "tj", "bj", "sex", "anal", "sex_raw", "creampie")
                _keep = dict((_k, _v) for _k, _v in (getattr(self, "player_firsts", None) or {}).items() if _k not in _partner_keys)
                self.player_firsts = dict((_k, False) for _k in _partner_keys)
                self.player_firsts.update(_keep)
                print("[BF_HISTORY] %s: partner-relative player_firsts reset, kept: %s" % (getattr(self, "gid", "?"), sorted(_keep) or "nothing"))

            def _generate_bf_history(self):
                """Randomly generate what she has done with her boyfriend.
                Escalation tiers:
                  0 = nothing sexual
                  1 = hj / masturbate
                  2 = tj
                  3 = bj
                  4 = sex (with condom)
                  5 = raw sex
                  6 = creampie
                If tier < 4, auto-sets virgin trait."""
                if self.has_trait("naive"):
                    self.bf_max_tier = 0
                    self.bf_history = {
                        "hj": False, "masturbate": False, "tj": False,
                        "bj": False, "sex": False, "sex_raw": False, "creampie": False,
                    }
                    self._reset_partner_firsts()
                    if not self.has_trait("virgin") and not self._already_deflowered():
                        self.add_trait("virgin")
                    return
                # Weighted random: favors lower tiers for more player-first opportunities
                weights = [
                    (0, 25), (1, 17), (2, 13), (3, 17),
                    (4, 13), (5, 8), (6, 7),
                ]
                total = sum(w for _tier, w in weights)
                roll = renpy.random.randint(1, total)
                cumul = 0
                tier = 0
                for t, w in weights:
                    cumul += w
                    if roll <= cumul:
                        tier = t
                        break

                # cum_slut + not virgin: boost toward raw/creampie tiers
                if self.has_trait("cum_slut") and not self.has_trait("virgin"):
                    if tier == 4:
                        # Had sex with condom → 60% chance she also went raw
                        if renpy.random.random() < 0.60:
                            tier = 5
                    if tier == 5:
                        # Had raw sex → 50% chance she also took a creampie
                        if renpy.random.random() < 0.50:
                            tier = 6

                self.bf_max_tier = tier

                # Tier mapping: everything at or below the tier is True
                tier_map = {
                    1: ["hj", "masturbate"],
                    2: ["hj", "masturbate", "tj"],
                    3: ["hj", "masturbate", "tj", "bj"],
                    4: ["hj", "masturbate", "tj", "bj", "sex"],
                    5: ["hj", "masturbate", "tj", "bj", "sex", "sex_raw"],
                    6: ["hj", "masturbate", "tj", "bj", "sex", "sex_raw", "creampie"],
                }
                acts = tier_map.get(tier, [])
                if not hasattr(self, "bf_history"):
                    self.bf_history = {
                        "hj": False, "masturbate": False, "tj": False,
                        "bj": False, "sex": False, "sex_raw": False, "creampie": False,
                    }
                for k in self.bf_history:
                    self.bf_history[k] = (k in acts)
                bf_history_drop_male_acts(self)

                self._reset_partner_firsts()

                # Auto-set virgin if BF never had sex with her
                if not self.bf_history.get("sex", False) and not self.has_trait("experienced"):
                    if not self.has_trait("virgin") and not self._already_deflowered():
                        self.add_trait("virgin")

            def _already_deflowered(self):
                """A partner history rolled MID-GAME (new partner after a breakup) must never give the virgin
                trait back to a girl the player already had sex with / deflowered."""
                _yes = girl_had_sex(self) or bool(getattr(self, "virginity_taken_by_player", False))
                if _yes:
                    print("[BF_HISTORY] %s: new partner history has no sex, but she is not a virgin any more: trait NOT re-added" % getattr(self, "gid", "?"))
                return _yes

            def bf_has_done(self, act):
                """Check if she has done this act with her BF."""
                h = getattr(self, "bf_history", {})
                return h.get(str(act), False)

            def mark_player_first(self, act):
                """Mark that the player was the first to do this act (BF hasn't).
                Triggers a discovery banner notification."""
                a = str(act)
                if not hasattr(self, "player_firsts"):
                    self.player_firsts = {
                        "kiss": False, "hj": False, "masturbate": False, "tj": False,
                        "bj": False, "sex": False, "anal": False,
                        "sex_raw": False, "creampie": False,
                    }
                # Backfill missing keys for old saves or empty dicts
                for _k in ("kiss", "hj", "masturbate", "tj", "bj", "sex", "anal", "sex_raw", "creampie"):
                    if _k not in self.player_firsts:
                        self.player_firsts[_k] = False
                if a in self.player_firsts and not self.player_firsts[a]:
                    self.player_firsts[a] = True
                    self.discover("player_first_%s" % a)


            # ------------------------------
            # Temptation (0–10)
            # ------------------------------
            def add_temptation(self, amount):
                Change_Status(self, "Temptation", amount, max_val=10)

            def set_temptation(self, value):
                self.Temptation = max(0, min(10, int(value)))

            def reset_temptation(self):
                self.Temptation = 0


            # ------------------------------
            # Cheating counters (per-girl)
            # ------------------------------
            def inc_player_cheat(self, victim_girl_id):
                """
                Player cheated on victim_girl_id with THIS girl.
                """
                if victim_girl_id is None:
                    victim_girl_id = "unknown"
                self.PlayerCheatCountByVictim[str(victim_girl_id)] += 1
                self.PlayerCheatCount += 1

                # Escalate attitude gradually (unless loyal hard locks it)
                if self.has_trait("cheater"):
                    self.CheatAttitude = 6
                elif self.has_trait("loyal"):
                    # Loyal can still be tempted over time, but much slower.
                    if self.PlayerCheatCount >= 5:
                        self.CheatAttitude = max(self.CheatAttitude, 3)
                else:
                    if self.PlayerCheatCount >= 3:
                        self.CheatAttitude = max(self.CheatAttitude, 4)
                    elif self.PlayerCheatCount >= 6:
                        self.CheatAttitude = max(self.CheatAttitude, 5)

            def inc_girl_cheat(self, partner_key):
                """Counting only — attitude evolution is handled by inc_cheat_act()."""
                if partner_key is None:
                    partner_key = "unknown"
                self.GirlCheatCountByPartner[str(partner_key)] += 1
                self.GirlCheatCount += 1
                self.check_corruption("loyal")


            def inc_cheat_act(self, action):
                """Increment per-act cheat counter and evolve CheatAttitude."""
                a = str(action)
                if a in self.CheatActs:
                    self.CheatActs[a] += 1

                # Update max tier (heaviest action she's done)
                tier = _cheat_action_tier(a) if callable(_cheat_action_tier) else 0
                if not hasattr(self, "CheatMaxTier"):
                    self.CheatMaxTier = 0
                if tier > self.CheatMaxTier:
                    self.CheatMaxTier = tier

                # BF loyalty erosion on sex acts
                _is_first = hasattr(self, "player_firsts") and self.player_firsts.get(a, False)
                _erode_bf_loyalty(self, "sex", a, is_first=_is_first)

                # Also bump the generic counter
                partner_key = None
                if self.has_npc_partner():
                    partner_key = "npc:%s" % str(self.npc_partner_id)
                elif self.has_girl_partner():
                    partner_key = "girl:%s" % str(self.girl_partner_id)
                if partner_key:
                    self.inc_girl_cheat(partner_key)

                if self.has_trait("cheater"):
                    return

                total = sum(self.CheatActs.values())

                if total >= 8:
                    self.CheatAttitude = max(self.CheatAttitude, 5)
                elif total >= 3:
                    self.CheatAttitude = max(self.CheatAttitude, 4)


            # ------------------------------
            # Girl-to-girl affinity + history
            # ------------------------------
            def set_like_for(self, other_id, value):
                value = max(0, min(MAX_STAT, int(value)))
                self.Girl_like[str(other_id)] = value

            def add_like_for(self, other_id, amount):
                key = str(other_id)
                cur = int(self.Girl_like.get(key, 0))
                self.set_like_for(key, cur + _persona_like_gain(self, key, int(amount)))

            def get_like_for(self, other_id):
                return int(self.Girl_like.get(str(other_id), 0))

            def inc_history_with(self, other_id, key, amount=1):
                """
                key examples: "kiss", "shared_player", "threesome", "saw_nude", ...
                """
                oid = str(other_id)
                self.Girl_history[oid][str(key)] += int(amount)

            def get_history_with(self, other_id, key):
                return int(self.Girl_history.get(str(other_id), {}).get(str(key), 0))


            # ------------------------------
            # Schedule helpers
            # ------------------------------
            def get_scheduled_location(self, day, time_index):
                if girl_away_reason(self):
                    return GIRL_AWAY_LOC   # schedule suspended, same lever as get_scheduled_location_for
                weekday = (max(1, int(day)) - 1) % 7
                ti = max(0, min(3, int(time_index)))
                return self.schedule[weekday][ti]

            def update_location_for_time(self, day, time_index):
                if self.loc_override is not None:
                    self.loc = self.loc_override
                else:
                    self.loc = self.get_scheduled_location(day, time_index)

            def set_location_override(self, location_code):
                self.loc_override = location_code
                self.loc = location_code

            def clear_location_override(self):
                self.loc_override = None


            # ------------------------------
            # Numeric stat helper
            # ------------------------------
            def add_stat(self, attr, amount, max_val=MAX_STAT):
                if not hasattr(self, attr):
                    return
                value = getattr(self, attr) + int(amount)
                if value < 0:
                    value = 0
                if value > int(max_val):
                    value = int(max_val)
                setattr(self, attr, value)

            def add_love(self, amount):
                self.add_stat("Love", amount)

            def add_Obed(self, amount):
                self.add_stat("Obed", amount)

            def add_Inbt(self, amount):
                self.add_stat("Inbt", amount)

            def add_Lust(self, amount):
                self.add_stat("Lust", amount, max_val=100)

            def add_stamina(self, amount):
                self.add_stat("Stamina", amount, max_val=10)


            # ------------------------------
            # Relationship helpers (player)
            # ------------------------------
            def is_dating_player(self):
                return self.Player_status in ("dating", "exclusive")

            def is_exclusive_with_player(self):
                return self.Player_status == "exclusive"

            def is_ex_of_player(self):
                return self.Player_status == "ex"

            def break_up_with_player(self, reason="generic", mood="angry", via="face"):
                """End dating relationship. Girl becomes ex. times_dated counts every time she dated him (the
                old history + this one: the "dumped again" lines read it). via: "face" / "text"."""
                if not self.is_dating_player():
                    return
                _old = getattr(self, "ex_player_history", None)
                _times = (_old.get("times_dated", 0) if isinstance(_old, dict) else 0) + 1
                self.ex_player_history = {
                    "breakup_mood": mood,
                    "love_at_breakup": int(getattr(self, "Love", 0)),
                    "times_dated": _times,
                    "breakup_day": store.Day,
                    "reason": reason,
                    "via": via,
                }
                self.Player_status = "ex"
                self._breakup_pending = False
                self._breakup_reason = None
                self.suspicion = 0
                _harem_cleanup_on_breakup(self)

            # ------------------------------
            # Temporary statuses (day-based)
            # ------------------------------
            def set_temp_status(self, status, days=1, reason=None):
                """Set a temporary status that expires after N days.
                Optional reason string stored for narration context."""
                if not hasattr(self, "temp_statuses"):
                    self.temp_statuses = {}
                if not hasattr(self, "temp_status_reasons"):
                    self.temp_status_reasons = {}
                days = _persona_mood_days(self, status, days, reason)
                self.temp_statuses[status] = store.Day + days - 1
                if reason:
                    self.temp_status_reasons[status] = reason
                elif status in self.temp_status_reasons:
                    del self.temp_status_reasons[status]

            def has_temp_status(self, status):
                """Check if a temporary status is currently active."""
                if not hasattr(self, "temp_statuses"):
                    self.temp_statuses = {}
                    return False
                expire = self.temp_statuses.get(status)
                if expire is None:
                    return False
                if store.Day > expire:
                    del self.temp_statuses[status]
                    if hasattr(self, "temp_status_reasons") and status in self.temp_status_reasons:
                        del self.temp_status_reasons[status]
                    return False
                return True

            def get_temp_status_reason(self, status):
                """Return the reason string for a temp status, or None."""
                if not hasattr(self, "temp_status_reasons"):
                    self.temp_status_reasons = {}
                    return None
                return self.temp_status_reasons.get(status, None)

            def clear_expired_statuses(self):
                """Remove all expired temporary statuses."""
                if not hasattr(self, "temp_statuses"):
                    self.temp_statuses = {}
                    return
                if not hasattr(self, "temp_status_reasons"):
                    self.temp_status_reasons = {}
                expired = [k for k, v in self.temp_statuses.items() if store.Day > v]
                for k in expired:
                    del self.temp_statuses[k]
                    if k in self.temp_status_reasons:
                        del self.temp_status_reasons[k]


    # ==================================================================
    # Legacy property shims: girl.Over -> girl.clothes["over"] etc.
    # ==================================================================
    def _cloth_getter(slot):
        def _get(self):
            c = getattr(self, "clothes", None)
            if c is None:
                return None
            return c.get(slot)
        return _get

    def _sync_shower_towel(girl):
        """Single source of truth: while in the showers, shower_state follows the towel ITEM.
        Runs on every write to the over slot (property setter, Outfit_Change, RestoreOutfit). The rule
        used to live only inside Outfit_Change, so DressUp_Sequence putting the towel back with
        `girl.Over = "towel"` left shower_state == "nude": the clothing builder then rendered over_none
        (+ towel_arm_left_none) while the arm builder rendered towel_arm_left_N -> Ren'Py conflict crash."""
        if getattr(store, "CurrentLocation", "") not in SHOWER_SPOTS:
            return
        _sh = getattr(girl, "shower_state", None)
        _over = (getattr(girl, "clothes", None) or {}).get("over")
        if _over == "towel" and _sh != "towel":
            print("[TOWEL_SYNC] %s: over=towel, shower_state %s -> towel" % (getattr(girl, "gid", "?"), _sh))
            girl.shower_state = "towel"
        elif _over is None and _sh == "towel":
            print("[TOWEL_SYNC] %s: towel removed, shower_state towel -> nude" % getattr(girl, "gid", "?"))
            girl.shower_state = "nude"

    def _cloth_setter(slot):
        def _set(self, val):
            c = getattr(self, "clothes", None)
            if c is None:
                self.clothes = {"over": None, "mid": None, "chest": None, "skirt": None, "panties": None, "shoes": None}
                c = self.clothes
            c[slot] = val
            if slot == "over":
                _sync_shower_towel(self)
        return _set

    def _state_getter(slot, flag_val):
        """Returns True when clothes_state[slot] == flag_val."""
        def _get(self):
            cs = getattr(self, "clothes_state", None)
            if cs is None:
                return False
            return cs.get(slot) == flag_val
        return _get

    def _state_setter(slot, flag_val):
        """Sets clothes_state[slot] to flag_val if True, else 'full'."""
        def _set(self, val):
            cs = getattr(self, "clothes_state", None)
            if cs is None:
                self.clothes_state = {"over": "full", "mid": "full", "chest": "full", "skirt": "full", "panties": "full", "shoes": "full"}
                cs = self.clothes_state
            cs[slot] = flag_val if val else "full"
        return _set

    Girl.Over     = property(_cloth_getter("over"),    _cloth_setter("over"))
    Girl.OverUp   = property(_state_getter("over", "up"), _state_setter("over", "up"))
    Girl.Mid      = property(_cloth_getter("mid"),     _cloth_setter("mid"))
    Girl.MidUp    = property(_state_getter("mid", "up"), _state_setter("mid", "up"))
    Girl.Chest    = property(_cloth_getter("chest"),   _cloth_setter("chest"))
    Girl.ChestUp  = property(_state_getter("chest", "up"), _state_setter("chest", "up"))
    Girl.Legs     = property(_cloth_getter("skirt"),   _cloth_setter("skirt"))
    Girl.LegsDown = property(_state_getter("skirt", "up"), _state_setter("skirt", "up"))
    Girl.Panties  = property(_cloth_getter("panties"), _cloth_setter("panties"))
    Girl.PantiesDown = property(_state_getter("panties", "down"), _state_setter("panties", "down"))
    Girl.PantiesSide = property(_state_getter("panties", "side"), _state_setter("panties", "side"))
    Girl.Shoes    = property(_cloth_getter("shoes"),   _cloth_setter("shoes"))


    # ── C. Johnson intel label resolver (used by Player.discover + Status screen) ──
    _JOHNSON_INTEL_STATIC = {
        "johnson_hotdog_energy": "Hotdogs recover energy",
        "johnson_npc_suspicious": "People are gossiping",
        "johnson_breakup": "Your breakup is known",
        "johnson_caught_public": "Professors noticed you",
        "johnson_attractive": "Girls find you handsome",
        "johnson_unattractive": "You... You are ugly :c",
        "johnson_financial_gifts": "Give gifts to pay for sex",
        "johnson_father_one": "A baby costs money: work",
        "johnson_father_many": "Many babies, many bills: work",
    }

    def _johnson_intel_label(key):
        if key in _JOHNSON_INTEL_STATIC:
            return _tr(_JOHNSON_INTEL_STATIC[key])
        if key.startswith("johnson_lesbian_"):
            _gobj = GIRL_BY_ID.get(key.replace("johnson_lesbian_", ""))
            if _gobj:
                return _tr("%s is changing") % _gobj.Name
        elif key.startswith("johnson_npc_hostile_"):
            _gobj = GIRL_BY_ID.get(key.replace("johnson_npc_hostile_", ""))
            if _gobj:
                _npc = get_npc_partner_for(_gobj)
                if _npc:
                    return _tr("%s is hostile to you") % _npc.Name
        elif key.startswith("johnson_npc_ntr_"):
            _gobj = GIRL_BY_ID.get(key.replace("johnson_npc_ntr_", ""))
            if _gobj:
                _npc = get_npc_partner_for(_gobj)
                if _npc:
                    return _tr("%s is not jealous") % _npc.Name
        elif key.startswith("johnson_npc_proud_"):
            _gobj = GIRL_BY_ID.get(key.replace("johnson_npc_proud_", ""))
            if _gobj:
                _npc = get_npc_partner_for(_gobj)
                if _npc:
                    return _tr("%s is jealous") % _npc.Name
        return None


    class PlayerData(object):
        def __init__(self, cash=100, energy=2, focus=0, Name="You"):
            self.cash = max(0, int(cash))
            self.energy_max = 2           # raised by gym (cap 5)
            self.energy = self._clamp_int(energy, 0, self.energy_max)
            self.Focus = self._clamp_int(focus, 0, 100)
            self.Name = Name
            self.skin = "White"
            self.inventory = {}   # { "item_id": quantity }
            self.study_level = 0
            self.grade_history = []
            self.phone_contacts = set()       # gids of girls whose number we have
            self.phone_npc_contacts = set()   # partner_ids of NPC partners whose number we have
            self.recorded_videos = []     # list of recorded video dicts
            self.received_photos = []     # list of photo dicts from girls
            self.campus_gossip = set()    # girl gids whose face-exposed videos were shared with non-partner NPCs
            self.bigfans_requests = []    # active BigFans fan requests
            self.bigfans_next_id = 1      # auto-increment for request ids
            self.phone_messages = {}      # {girl_gid: [msg_dicts]} chat history
            # Workout / energy tracking
            self.weekly_workouts = 0      # workouts done this week (resets Sunday)
            self.total_workouts = 0       # lifetime counter
            self._workouts_toward_energy = 0  # workouts toward next energy_max increase (resets on gain)
            self._workout_streak = 0     # consecutive 5-workout weeks
            # Swimming (register_swim, swimming.rpy): the first swim of a day counts; half a workout, and Breath
            self.total_swims = 0
            self._swim_last_day = -1
            self._swims_toward_workout = 0
            self._swims_toward_breath = 0
            self.breath = 0               # 0..BREATH_MAX: his arousal builds slower in scenes (add_player_focus)
            # Hidden attractiveness (0-100, set once at game start, never changes)
            self.attractiveness = renpy.random.randint(0, 100)
            # Discovery flags (mirror of Girl.flags for player-specific info)
            self.discoveries = {}
            # Never Have I Ever: times he lied (didn't drink but did it), got caught, or bluffed
            self._nhie_lies = 0
            self._nhie_lies_caught = 0
            self._nhie_bluffs = 0

        def discover(self, key):
            """Set a player discovery flag. Plays notification and shows banner if new."""
            k = str(key)
            if not hasattr(self, "discoveries"):
                self.discoveries = {}
            if self.discoveries.get(k, False):
                return
            self.discoveries[k] = True
            renpy.music.play("audio/Information.mp3", channel="notify_sfx", loop=False)
            _banner_map = {
                "first_kiss": _tr("Your first kiss"),
                "first_hj": _tr("Your first handjob"),
                "first_tj": _tr("Your first titjob"),
                "first_bj": _tr("Your first blowjob"),
                "first_sex": _tr("Lost your virginity"),
                "first_anal": _tr("Your first anal"),
                "first_creampie": _tr("Your first creampie"),
                "first_raw": _tr("First time going raw"),
                "took_virginity": _tr("You took someone's virginity"),
                "first_girlfriend": _tr("You got your first girlfriend"),
                "max_energy": _tr("Peak physical condition"),
            }
            _text = _banner_map.get(k, None)
            if _text is None and k.startswith("johnson_"):
                _text = _johnson_intel_label(k) or _tr("New intel acquired")
            if _text is not None:
                renpy.show_screen("discovery_banner", girl_name=self.Name, info_text=_text, name_color="#38bdf8")

        def has_discovery(self, key):
            if not hasattr(self, "discoveries"):
                self.discoveries = {}
            return self.discoveries.get(str(key), False)

        def _clamp_int(self, value, minimum, maximum):
            v = int(value)
            if v < int(minimum):
                return int(minimum)
            if v > int(maximum):
                return int(maximum)
            return v

        def add_cash(self, amount):
            a = int(amount)
            if a > 0:
                self.cash += a

        def spend_cash(self, amount):
            a = int(amount)
            if a <= 0:
                return False
            if a > self.cash:
                return False
            self.cash -= a
            return True

        def _get_energy_max(self):
            return max(1, int(getattr(self, "energy_max", 2)))

        def change_energy(self, delta):
            self.energy = self._clamp_int(self.energy + int(delta), 0, self._get_energy_max())

        def set_energy(self, value):
            self.energy = self._clamp_int(value, 0, self._get_energy_max())

        def recharge_energy(self):
            """Restore energy to max. Call on sleep."""
            self.energy = self._get_energy_max()

        def register_workout(self):
            """Call after each gym workout. Every 5 workouts raises energy_max (cap 5).
            Returns True if energy_max was raised."""
            self.weekly_workouts = getattr(self, "weekly_workouts", 0) + 1
            self.total_workouts = getattr(self, "total_workouts", 0) + 1
            self._last_workout_day = store.Day
            self._workouts_toward_energy = getattr(self, "_workouts_toward_energy", 0) + 1
            emax = self._get_energy_max()
            if self._workouts_toward_energy >= 5 and emax < 5:
                self.energy_max = emax + 1
                self._workouts_toward_energy = 0
                if self.energy_max >= 5:
                    self.discover("max_energy")
                return True
            return False

        def register_swim(self):
            """Call after each swim (the pool action and the breath-holding bet). Only the first swim of a day
            counts: a swim costs a third of a time slot, a workout the whole slot. Every SWIM_DAYS_PER_WORKOUT
            counted days = one gym workout (register_workout: Max Energy progress AND the weekly minimum); every
            SWIM_DAYS_PER_BREATH counted days = +1 Breath (cap BREATH_MAX).
            Returns (counted, energy_up, breath_up)."""
            if getattr(self, "_swim_last_day", -1) == store.Day:
                return (False, False, False)
            self._swim_last_day = store.Day
            self.total_swims = getattr(self, "total_swims", 0) + 1
            _energy_up = False
            self._swims_toward_workout = getattr(self, "_swims_toward_workout", 0) + 1
            if self._swims_toward_workout >= SWIM_DAYS_PER_WORKOUT:
                self._swims_toward_workout = 0
                _energy_up = self.register_workout()
            _breath_up = False
            if getattr(self, "breath", 0) < BREATH_MAX:
                self._swims_toward_breath = getattr(self, "_swims_toward_breath", 0) + 1
                if self._swims_toward_breath >= SWIM_DAYS_PER_BREATH:
                    self._swims_toward_breath = 0
                    self.breath = getattr(self, "breath", 0) + 1
                    _breath_up = True
            print("[SWIM] day %d counted: swims=%d toward_workout=%d energy_up=%s breath=%d breath_up=%s" % (
                store.Day, self.total_swims, self._swims_toward_workout, _energy_up, getattr(self, "breath", 0), _breath_up))
            return (True, _energy_up, _breath_up)

        def weekly_workout_check(self):
            """Call once per week (Sunday). Penalize if < 3 workouts last week.
            Sets _weekly_energy_lost flag for UI feedback."""
            wk = getattr(self, "weekly_workouts", 0)
            emax = self._get_energy_max()
            if wk < 3 and emax > 1:
                self.energy_max = emax - 1
                # Current energy can't exceed new max
                if self.energy > self.energy_max:
                    self.energy = self.energy_max
                store._weekly_energy_lost = True
            else:
                store._weekly_energy_lost = False
            self.weekly_workouts = 0

        def change_focus(self, delta):
            self.Focus = self._clamp_int(self.Focus + int(delta), 0, 100)

        def set_focus(self, value):
            self.Focus = self._clamp_int(value, 0, 100)

        def add_item(self, item_id, qty=1):
            key = str(item_id)
            self.inventory[key] = self.inventory.get(key, 0) + max(1, int(qty))

        def remove_item(self, item_id, qty=1):
            key = str(item_id)
            current = self.inventory.get(key, 0)
            if current < int(qty):
                return False
            self.inventory[key] = current - int(qty)
            if self.inventory[key] <= 0:
                del self.inventory[key]
            return True

        def get_item_count(self, item_id):
            return self.inventory.get(str(item_id), 0)

        def has_item(self, item_id, qty=1):
            return self.get_item_count(item_id) >= int(qty)


    # ------------------------------
    # Player relationship helpers (mono)
    # ------------------------------
    def get_player_girlfriends(girl_list):
        return [g for g in (girl_list or []) if g and g.is_dating_player()]

    def get_player_girlfriend(girl_list):
        gfs = get_player_girlfriends(girl_list)
        return gfs[0] if gfs else None

    def player_has_girlfriend(girl_list):
        return get_player_girlfriend(girl_list) is not None

    # --- NPC partner discovery helpers ---
    _PARTNER_DISCOVERY_KEY = "discovered_has_partner"

    def _discover_partner(girl):
        girl.discover(_PARTNER_DISCOVERY_KEY)

    def _partner_discovered(girl):
        return girl.get_flag(_PARTNER_DISCOVERY_KEY) or girl.get_flag("discovered_has_boyfriend")

    def can_start_new_relationship(new_girl, girl_list):
        if get_player_girlfriend(girl_list) is None:
            return True
        return getattr(store, "relationship_mode", "mono") == "poly" or is_player_harem_exempt(new_girl)

    # ------------------------------
    # Harem / Poly helpers
    # ------------------------------
    def _update_relationship_mode():
        for g in (ALL_GIRLS or []):
            if getattr(g, "harem_accepted", None):
                store.relationship_mode = "poly"
                return
        store.relationship_mode = "mono"

    def harem_acceptance_check(girl):
        _love = getattr(girl, "Love", 0)
        _obed = getattr(girl, "Obed", 0)
        _inbt = getattr(girl, "Inbt", 0)

        if girl.has_trait("polyamorous"):
            print("[HAREM] %s: polyamorous -> accept" % girl.gid)
            return ("accept", 9999)

        if girl.has_trait("monogamous"):
            if _love >= 900 and _obed >= 700:
                print("[HAREM] %s: monogamous BUT Love=%d Obed=%d -> grudging accept" % (girl.gid, _love, _obed))
                return ("accept", _love + _obed)
            print("[HAREM] %s: monogamous -> reject (L=%d O=%d)" % (girl.gid, _love, _obed))
            return ("reject", 0)

        _score = _love + (_obed // 2) + (_inbt // 2)
        _HAREM_SCORE_MIN = 700
        if _score >= _HAREM_SCORE_MIN:
            print("[HAREM] %s: no trait, score=%d >= %d -> accept" % (girl.gid, _score, _HAREM_SCORE_MIN))
            return ("accept", _score)
        print("[HAREM] %s: no trait, score=%d < %d -> reject" % (girl.gid, _score, _HAREM_SCORE_MIN))
        return ("reject", _score)

    def harem_vote_on_girl(voter, target):
        """Vote on whether to accept a specific girl into the harem.
        Returns (result, score, reason_key)."""
        base_result, base_score = harem_acceptance_check(voter)

        if voter.has_trait("polyamorous"):
            print("[HAREM_VOTE] %s votes accept for %s (poly trait)" % (voter.gid, target.gid))
            return ("accept", 9999, "poly")

        if base_result == "reject" and base_score < 100:
            print("[HAREM_VOTE] %s votes reject for %s (unwilling, base=%d)" % (voter.gid, target.gid, base_score))
            return ("reject", 0, "unwilling")

        _girl_like = voter.get_like_for(target.gid)
        _adjusted = base_score + (_girl_like - 500) // 2

        if _adjusted >= 700:
            if _girl_like < 250:
                _obed = getattr(voter, "Obed", 0)
                if _obed >= 800:
                    print("[HAREM_VOTE] %s votes FORCED accept for %s (hostile but Obed=%d, like=%d)" % (voter.gid, target.gid, _obed, _girl_like))
                    return ("accept", _adjusted, "forced")
                print("[HAREM_VOTE] %s votes reject for %s (hostile, like=%d, Obed=%d < 800)" % (voter.gid, target.gid, _girl_like, _obed))
                return ("reject", _adjusted, "hostile")
            print("[HAREM_VOTE] %s votes accept for %s (willing, adj=%d like=%d)" % (voter.gid, target.gid, _adjusted, _girl_like))
            return ("accept", _adjusted, "willing")

        if _girl_like >= 750 and _adjusted >= 500:
            print("[HAREM_VOTE] %s votes accept for %s (likes_her, adj=%d like=%d)" % (voter.gid, target.gid, _adjusted, _girl_like))
            return ("accept", _adjusted, "likes_her")

        print("[HAREM_VOTE] %s votes reject for %s (unwilling, adj=%d like=%d)" % (voter.gid, target.gid, _adjusted, _girl_like))
        return ("reject", _adjusted, "unwilling")

    def add_to_harem(girl, other_gid):
        if not hasattr(girl, "harem_accepted"):
            girl.harem_accepted = set()
        girl.harem_accepted.add(other_gid)
        _update_relationship_mode()
        print("[HAREM] %s now accepts %s (harem=%s)" % (girl.gid, other_gid, girl.harem_accepted))

    def remove_from_harem(girl, other_gid):
        if hasattr(girl, "harem_accepted"):
            girl.harem_accepted.discard(other_gid)
        _update_relationship_mode()
        print("[HAREM] %s removed %s (harem=%s)" % (girl.gid, other_gid, girl.harem_accepted))

    def is_harem_exempt(witness, active_girl):
        _w_harem = getattr(witness, "harem_accepted", None) or set()
        return active_girl.gid in _w_harem

    def is_player_harem_exempt(girl):
        """True if ALL of the player's GFs have this girl in their harem_accepted.
        Returns False if girl IS one of the GFs, or if there are no GFs."""
        if girl is None:
            return False
        if hasattr(girl, "is_dating_player") and girl.is_dating_player():
            return False
        _gfs = get_player_girlfriends(ALL_GIRLS) if hasattr(store, "ALL_GIRLS") else []
        if not _gfs:
            return False
        for _gf in _gfs:
            if not is_harem_exempt(_gf, girl):
                return False
        return True

    def _harem_cleanup_on_breakup(girl):
        """Remove girl from all harem_accepted sets, harem group, and clear her own set."""
        _gid = girl.gid
        for _g in (ALL_GIRLS or []):
            if _g is girl:
                continue
            if hasattr(_g, "harem_accepted") and _gid in _g.harem_accepted:
                _g.harem_accepted.discard(_gid)
                print("[HAREM] cleanup: removed %s from %s.harem_accepted" % (_gid, _g.gid))
            _gfb = getattr(_g, "_harem_forced_by", None)
            if _gfb and _gid in _gfb:
                _gfb.discard(_gid)
                print("[HAREM] cleanup: removed %s from %s._harem_forced_by" % (_gid, _g.gid))
        if hasattr(girl, "harem_accepted"):
            girl.harem_accepted.clear()
        _girl_fb = getattr(girl, "_harem_forced_by", None)
        if _girl_fb:
            _girl_fb.clear()
        girl._harem_ask_pending = False
        girl._harem_caught_with_gid = None
        girl._harem_caught_act = None
        girl._harem_caught_suggests_add = False
        girl._open_relationship_consent = False

        _hg = _get_harem_group()
        if _hg and _gid in _hg["members"]:
            _hg["members"].remove(_gid)
            phone_group_add_msg(_hg["id"], "system", _tl(_("%s left the group.")) % girl.Name, "system")
            print("[HAREM] cleanup: removed %s from harem group %s" % (_gid, _hg["id"]))
            if len(_hg["members"]) < 2:
                store.Player.phone_groups = [g for g in store.Player.phone_groups if g["id"] != _hg["id"]]
                store._harem_group_id = None
                print("[HAREM] cleanup: dissolved harem group")

        _update_relationship_mode()


    # ------------------------------
    # UI helpers (kept)
    # ------------------------------
    def show_stat_popup(value, color="#ffffff", xpos=0.75):
        v = int(value)
        if v == 0:
            return
        txt = ("+%d" % v) if v > 0 else ("%d" % v)
        renpy.show_screen("stat_popup", txt, color, xpos)

    # ---------------------------------------------------------------- PERSONALITY (the numbers)
    # docs/Personality.md, plan docs/plan_personality_mechanics.md (approved 2026-09-19). A girl missing from a table
    # behaves like everybody; a new girl needs no entry.
    #
    # How fast she gains a stat. EVERY gain from every source (chit-chat, flirts, gifts, acts, events) goes through
    # it; losses, starting values and raw=True calls (the stat cheats promise a number) never do. The fraction a gain
    # loses to the rounding waits in store._stat_gain_carry ("gid.Stat") and joins her next gain: exact in the long run.
    GIRL_STAT_GAIN_MULT = {
        "ntw":   {"Obed": 0.70, "Love": 0.85},                   # obeys nobody, slow to open up
        "tenny": {"Love": 1.20, "Obed": 1.10, "Inbt": 0.85},     # gets attached fast, follows rules, shy
        "rogue": {"Love": 1.10, "Inbt": 0.85},                   # warm, careful with her body
        "gwen":  {"Obed": 0.85, "Inbt": 1.10, "Jealousy": 1.30}, # sceptical of orders, alternative, love triangles
        "shion": {"Obed": 0.50, "Love": 0.80},                   # used to getting her way; affection is earned (x femdom 0.6)
    }

    # How fast a TRAIT makes her gain a stat, multiplied into her personality's number above (same rules: gains only,
    # the carry keeps it exact). docs/plan_femdom.md D6.
    TRAIT_STAT_GAIN_MULT = {
        "femdom": {"Obed": 0.6},       # she is the one giving the orders
        "submissive": {"Obed": 1.4},   # the mirror: she wants to be told what to do, obeys faster
    }

    # A Love LOSS from being bossed, degraded, spanked or used (docs/plan_submissive_pass.md S3): a submissive loses
    # nothing (it is what she wanted), an unbroken femdom loses more. Read at the sites that hand out the loss
    # (the degrading teases, the ass spanks, the massage and flirt ass slaps, his "stop anyway"). The FACE slap
    # stays insulting for everyone (project_spank_vs_face_slap).
    TRAIT_LOVE_LOSS_MULT = {
        "submissive": 0.0,
        "femdom": 1.5,
    }

    def trait_love_loss(girl, amount, face=False):
        """`amount` (a Love change) read through her Control trait. A gain, a face slap or a girl without the trait
        come back unchanged."""
        if amount >= 0 or face or not hasattr(girl, "has_trait"):
            return amount
        for _tid, _m in TRAIT_LOVE_LOSS_MULT.items():
            if girl.has_trait(_tid):
                _out = int(round(amount * _m))
                print("[LOVE_LOSS] %s %s: %d -> %d" % (girl.gid, _tid, amount, _out))
                return _out
        return amount

    def _persona_gain(target, flavor, amount):
        """Her gain of `flavor` after her personality multiplier and her traits' (amount > 0)."""
        if amount <= 0:
            return amount
        _gid = getattr(target, "gid", None)
        _mult = GIRL_STAT_GAIN_MULT.get(_gid, {}).get(flavor)
        if _gid and hasattr(target, "has_trait"):
            for _tid, _by_stat in TRAIT_STAT_GAIN_MULT.items():
                if flavor in _by_stat and target.has_trait(_tid):
                    _mult = (1.0 if _mult is None else _mult) * _by_stat[flavor]
        if _mult is None:
            return amount
        _carry = getattr(store, "_stat_gain_carry", None)
        if _carry is None:
            store._stat_gain_carry = _carry = {}
        _key = "%s.%s" % (target.gid, flavor)
        _exact = amount * _mult + _carry.get(_key, 0.0)
        _gain = int(_exact + 1e-9)          # 1.15 * 20 = 22.999999...: a float must not eat a point
        _carry[_key] = _exact - _gain
        print("[PERSONA] %s %s +%d x%.2f -> +%d (carry %.2f)" % (target.gid, flavor, amount, _mult, _gain, _carry[_key]))
        return _gain

    # Her temper: days added to a mood she gets (never under 1). A "breakup" mood is tuned to the reconciliation
    # cooldown (EX_RECON_CONFIG["normal_days_min"]: a shorter one reopens the gap where he can talk to her): untouched.
    GIRL_MOOD_DAYS = {
        "ntw":   {"angry": -1},     # explodes, and it passes
        "rogue": {"sad": 1},        # takes being left aside to heart
        "shion": {"angry": 1},      # holds a grudge
    }
    _MOOD_DAYS_EXEMPT_REASONS = frozenset(("breakup",))

    def _persona_mood_days(girl, status, days, reason=None):
        """How many days her `status` lasts after her temper (set_temp_status)."""
        _d = GIRL_MOOD_DAYS.get(getattr(girl, "gid", None), {}).get(status)
        if not _d or reason in _MOOD_DAYS_EXEMPT_REASONS:
            return days
        _new = max(1, int(days) + _d)
        if _new != days:
            print("[PERSONA] %s %s: %d day(s) -> %d (her temper)" % (girl.gid, status, days, _new))
        return _new

    # How fast she warms up to another girl (friendship GAINS only): NTW slow (half with eager Tenny), Gwen cautious,
    # Rogue warm. Where each friendship starts: GIRL_LIKE_START (roll_girl_likes).
    GIRL_LIKE_GAIN_MULT = {
        "ntw":   {"_all": 0.75, "tenny": 0.5},
        "gwen":  {"_all": 0.85},
        "rogue": {"_all": 1.2},
    }

    def _persona_like_gain(girl, other_id, amount):
        """Her friendship gain toward `other_id` after her personality (add_like_for)."""
        if amount <= 0:
            return amount
        _m = GIRL_LIKE_GAIN_MULT.get(getattr(girl, "gid", None))
        if not _m:
            return amount
        _f = _m.get(str(other_id), _m.get("_all", 1.0))
        return max(1, int(round(amount * _f)))

    def Change_Status(target, flavor, amount, max_val=MAX_STAT, xpos=None, show_popup=True, raw=False):
        """raw=True: the amount exactly as given, no personality (the stat cheats)."""
        if (target is None) or (not hasattr(target, flavor)):
            return

        old_value = getattr(target, flavor, 0)
        _amt = int(amount)
        if flavor == "Jealousy" and _amt > 0:
            _amt = int(_amt * getattr(target, "_jealousy_gain_mult", 1.0))
        if _amt > 0 and not raw:
            _amt = _persona_gain(target, flavor, _amt)
            # her story step's ceiling (story_steps.rpy): past it, the gain rises slowly
            _amt = story_stat_gain(target, flavor, old_value, _amt)
        new_value = old_value + _amt

        if new_value > int(max_val):
            new_value = int(max_val)
        if new_value < 0:
            new_value = 0

        delta = new_value - old_value
        setattr(target, flavor, new_value)

        # Keep save snapshot in sync
        _sync_girl(target)

        # Track last player interaction day for Hardcore Relationship Mode
        if hasattr(target, "_hc_last_interaction_day"):
            target._hc_last_interaction_day = getattr(store, "Day", 1)
            if getattr(target, "_hc_single_warned", 0) > 0:
                target._hc_single_warned = 0
                target._hc_partner_spawn_day = 0

        # Love at the top with a partner = she will leave him for the player. BEFORE the early returns: a silent gain
        # (show_popup=False: NHIE, the night hangout) or a capped one (delta 0, already at 1000) used to skip it,
        # and the breakup + homewrecker never fired
        if flavor == "Love" and new_value >= 1000 and hasattr(target, "has_npc_partner") and target.has_npc_partner():
            if not getattr(target, "_will_break_up_with_partner", False):
                target._will_break_up_with_partner = True
                unlock_achievement("homewrecker")
                debug_log("[NPC_BREAKUP] %s Love=1000 -> will_break_up_with_partner set" % getattr(target, "gid", "?"))

        if delta == 0:
            return

        if not show_popup:
            return

        STAT_COLORS = {
            "Love": STAT_POPUP_LOVE,
            "Obed": STAT_POPUP_OBED,
            "Inbt": STAT_POPUP_INBT,
            "Lust": STAT_POPUP_LUST,
            "Temptation": STAT_POPUP_TEMPTATION,
            "Jealousy": STAT_POPUP_JEALOUSY,
        }
        STAT_YPOS = {
            "Love": 0.18,
            "Obed": 0.23,
            "Inbt": 0.28,
            "Lust": 0.33,
            "Temptation": 0.38,
            "Jealousy": 0.43,
        }
        color = STAT_COLORS.get(flavor, "#ffffff")
        ypos = STAT_YPOS.get(flavor, 0.25)

        prefix = "+" if delta > 0 else "-"
        value_for_popup = abs(int(delta))

        if xpos is None:
            _loc = getattr(target, "SpriteLoc", None)
            xpos = (_loc if _loc is not None else 0.75) - 0.15

        STAT_LABELS = {
            "Jealousy": "Jeal",
        }
        tag = "stat_%s" % flavor
        renpy.show_screen(
            "StatHolder",
            value=value_for_popup,
            prefix=prefix,
            color=color,
            xpos=xpos,
            ypos=ypos,
            label_text=STAT_LABELS.get(flavor, flavor),
            hide_tag=tag,
            _tag=tag,
        )

    # Girl-to-girl friendship popups: sits below the per-girl stat column (Love 0.18 ... Jealousy 0.43)
    # and the NPC column (0.43-0.53). Popups fired close together stack downward instead of overlapping.
    _GIRL_LIKE_POPUP_YPOS = 0.58
    _GIRL_LIKE_POPUP_STEP = 0.05
    _GIRL_LIKE_POPUP_SLOTS = 4
    _GIRL_LIKE_POPUP_WINDOW = 3.5   # seconds a StatHolder stays on screen
    _girl_like_popup_state = {"t": 0.0, "slot": 0}

    def _show_girl_like_popup(label_text, delta, xpos):
        import time
        _now = time.time()
        if _now - _girl_like_popup_state["t"] < _GIRL_LIKE_POPUP_WINDOW:
            _slot = (_girl_like_popup_state["slot"] + 1) % _GIRL_LIKE_POPUP_SLOTS
        else:
            _slot = 0
        _girl_like_popup_state["t"] = _now
        _girl_like_popup_state["slot"] = _slot

        tag = "stat_girl_like_%d" % _slot
        renpy.show_screen(
            "StatHolder",
            value=abs(int(delta)),
            prefix="+" if delta > 0 else "-",
            color=STAT_POPUP_GIRL_FRIENDSHIP,
            xpos=xpos,
            ypos=_GIRL_LIKE_POPUP_YPOS + _GIRL_LIKE_POPUP_STEP * _slot,
            label_text=label_text,
            hide_tag=tag,
            _tag=tag,
        )

    def Change_Girl_Like(girl_a, girl_b, amount, amount_b=None, mutual=True, xpos=None, show_popup=True):
        """Central girl-to-girl friendship (Girl_like) change + HUD popup.
        amount  : change in how girl_a feels about girl_b (positive or negative).
        mutual  : also change how girl_b feels about girl_a, by amount_b (defaults to amount).
        Popup   : "A | B Friendship +N" when both sides moved by the same value,
                  otherwise one "A > B Friendship +N" line per side that actually moved.
        Returns (delta_a, delta_b) after clamping to 0..MAX_STAT."""
        if girl_a is None or girl_b is None or girl_a is girl_b:
            return (0, 0)

        _old_a = girl_a.get_like_for(girl_b.gid)
        girl_a.add_like_for(girl_b.gid, amount)
        delta_a = girl_a.get_like_for(girl_b.gid) - _old_a
        _sync_girl(girl_a)

        delta_b = 0
        if mutual:
            _amt_b = amount if amount_b is None else amount_b
            _old_b = girl_b.get_like_for(girl_a.gid)
            girl_b.add_like_for(girl_a.gid, _amt_b)
            delta_b = girl_b.get_like_for(girl_a.gid) - _old_b
            _sync_girl(girl_b)

        print("[GIRL_LIKE] %s -> %s: %+d (now %d) | %s -> %s: %+d (now %d) mutual=%s" % (
            girl_a.gid, girl_b.gid, delta_a, girl_a.get_like_for(girl_b.gid),
            girl_b.gid, girl_a.gid, delta_b, girl_b.get_like_for(girl_a.gid), mutual))

        if not show_popup:
            return (delta_a, delta_b)

        if xpos is None:
            _loc = getattr(girl_a, "SpriteLoc", None)
            xpos = (_loc if _loc is not None else 0.75) - 0.15

        _lbl = _tr("Friendship")
        if mutual and delta_a == delta_b:
            if delta_a != 0:
                _show_girl_like_popup("%s | %s %s" % (girl_a.Name, girl_b.Name, _lbl), delta_a, xpos)
        else:
            if delta_a != 0:
                _show_girl_like_popup("%s > %s %s" % (girl_a.Name, girl_b.Name, _lbl), delta_a, xpos)
            if delta_b != 0:
                _show_girl_like_popup("%s > %s %s" % (girl_b.Name, girl_a.Name, _lbl), delta_b, xpos)

        return (delta_a, delta_b)


# ============================================================
# GIRLS CONFIG + SPRITE / CLOTHING SYSTEM
# ============================================================

init python:
    import random as _random
    from collections import defaultdict

    # ----------------------------------------------
    # Global sprite state (expressions, etc.)
    # ----------------------------------------------
    sprite_state = {}  # key = girl.Id (e.g. "gwen")

    import time as _time_mod

    def _kill_scene_threads(keep_watchers=False):
        """Signal ALL background sex-scene threads to stop.
        Call at the top of every *_Launch label so entry is clean
        whether arriving fresh or after a rollback.
        keep_watchers: True on a mid-scene position switch. The NTR partner keeps
        watching (no scene-end bonus yet). The NTR bet event also manages its own
        watcher state (_bet_cleanup), so it is never ended here."""
        store._hj_girl       = None
        store._bj_girl       = None
        store._cowgirl_girl  = None
        store._rcg_girl      = None
        store._fn_girl       = None
        store._titjob_girl   = None
        store._doggy_girl    = None
        store._laying_girl   = None
        store._ft_girl       = None
        store._rj_girl       = None
        _keep = keep_watchers or getattr(store, "_bet_event_active", False)
        if _keep:
            debug_log("[KILL_THREADS] keeping NTR watcher (switch=%s bet=%s) watching=%s" % (keep_watchers, getattr(store, "_bet_event_active", False), store._ntr_partner_watching))
        else:
            # Every "partner leaves" site clears the watcher BEFORE the scene ends, so reaching here with
            # watching=True means he watched to the end and is still in the room. The detection tick
            # cannot re-arm him this session (_npc_witness_check_done), so remember it for the creampie rule.
            if store._ntr_partner_watching and store._ntr_watching_npc is not None:
                store._ntr_session_watcher_gid = getattr(store._ntr_watching_npc, "girl_gid", None)
                print("[NTR_WATCH] scene ended with %s still watching -> session watcher gid=%s" % (getattr(store._ntr_watching_npc, "name", "?"), store._ntr_session_watcher_gid))
            if store._ntr_partner_watching and callable(globals().get("_ntr_scene_end_bonus", None)):
                _ntr_scene_end_bonus()
            store._ntr_partner_watching = False
            store._ntr_watching_npc = None
        store._bj_cheeks_running = False
        store._bj_blink_running  = False
        # Give threads time to notice the sentinel and exit
        _time_mod.sleep(0.20)
        # Preserve recording watcher and threesome witness sprite_state across position switches
        _preserve_ids = set()
        _rec_gid = getattr(store, "_recording_watcher_gid", None)
        _rec_g = GIRL_BY_ID.get(_rec_gid) if _rec_gid else None
        if _rec_g:
            _preserve_ids.add(_rec_g.Id)
        _wit_g = getattr(store, "_witness_girl", None) if getattr(store, "_threesome_mode", False) else None
        if _wit_g and hasattr(_wit_g, "Id"):
            _preserve_ids.add(_wit_g.Id)
        _preserved = {}
        for _pid in _preserve_ids:
            _ss = sprite_state.get(_pid)
            if _ss:
                _preserved[_pid] = dict(_ss)
        # Wipe stale expression state so the new scene starts fresh
        sprite_state.clear()
        for _pid, _ss in _preserved.items():
            sprite_state[_pid] = _ss
        if _preserved:
            print("[KILL_THREADS] preserved sprite_state for %s" % list(_preserved.keys()))

    # ----------------------------------------------
    # Simple config for girls (stats + schedule)
    # ----------------------------------------------
    GIRLS_CONFIG = {
        "gwen": {
            "Name": "Gwen",
            "color": "#45b4c7",
            # student / teacher / family: which traits she can have (TRAIT_GIRL_TYPES)
            "type": "student",
            "bust": "large",
            "home": "gwen_room",
            "schedule": [
                # Morning        Noon          Evening      Night
                ["gwen_room", "gym",        "campus",    "gwen_room"],  # Sunday
                ["gwen_room", "classroom",  "campus",    "gwen_room"],  # Monday
                ["gwen_room", "pool",       "gym",       "gwen_room"],  # Tuesday
                ["gwen_room", "classroom",  "mall",      "gwen_room"],  # Wednesday (evening mall)
                ["gym",       "classroom",  "pool",      "gwen_room"],  # Thursday
                ["gwen_room", "classroom",  "campus",    "gwen_room"],  # Friday
                ["gwen_room", "mall",       "pool",      "gwen_room"],  # Saturday (weekend mall)
            ],
            "Love": 100,
            "Obed": 15,
            "Inbt": 10,
            "Lust": 5,
        },

        "rogue": {
            "Name": "Rogue",
            "color": "#c45b7c",
            "type": "student",
            "enabled": True,
            "bust": "medium",
            "home": "rogue_room",
            "schedule": [
                # Morning           Noon          Evening       Night
                ["rogue_room", "mall",       "pool",      "rogue_room"],  # Sunday (weekend mall)
                ["rogue_room", "classroom",  "campus",    "rogue_room"],  # Monday
                ["rogue_room", "campus",     "mall",      "rogue_room"],  # Tuesday (evening mall)
                ["rogue_room", "classroom",  "campus",    "rogue_room"],  # Wednesday
                ["gym",        "classroom",  "campus",    "rogue_room"],  # Thursday
                ["rogue_room", "classroom",  "pool",      "rogue_room"],  # Friday
                ["rogue_room", "gym",        "campus",    "rogue_room"],  # Saturday
            ],
            "Love": 50,
            "Obed": 15,
            "Inbt": 10,
            "Lust": 5,
        },

        "ntw": {
            "Name": "Negasonic",
            "color": "#f5c842",
            "type": "student",
            "enabled": True,
            "body_type": "petite",
            "bust": "small",
            "home": "ntw_room",
            "schedule": [
                # Morning        Noon          Evening      Night
                ["ntw_room", "campus",     "pool",      "ntw_room"],  # Sunday  (Gwen: gym/campus, Rogue: mall/pool)
                ["ntw_room", "gym",        "pool",      "ntw_room"],  # Monday  (Gwen+Rogue: classroom/campus — NTW at gym/pool)
                ["ntw_room", "classroom",  "campus",    "ntw_room"],  # Tuesday (Gwen: pool/gym, Rogue: campus/mall — NTW avoids gym)
                ["ntw_room", "campus",     "gym",       "ntw_room"],  # Wednesday (Gwen: classroom/mall, Rogue: classroom — NTW at campus)
                ["ntw_room", "campus",     "mall",      "ntw_room"],  # Thursday (evening mall)
                ["gym",      "campus",     "campus",    "ntw_room"],  # Friday  (Gwen+Rogue: classroom — NTW at campus)
                ["ntw_room", "pool",       "mall",      "ntw_room"],  # Saturday (weekend mall)
            ],
            "Love": 30,
            "Obed": 10,
            "Inbt": 5,
            "Lust": 5,
        },

        "tenny": {
            "Name": "Tenny",
            "color": "#7ecb8f",
            "type": "student",
            "enabled": True,
            "body_type": "medium",
            "bust": "small",
            "mast_pose": "laying_down",
            "home": "tenny_room",
            "traits": ["nerd"],
            "schedule": [
                # Morning          Noon            Evening       Night
                ["classroom",  "pool",        "gym",        "tenny_room"],  # Sunday
                ["classroom",  "classroom",   "pool",       "tenny_room"],  # Monday
                ["classroom",  "classroom",   "gym",        "tenny_room"],  # Tuesday
                ["tenny_room", "classroom",   "gym",        "tenny_room"],  # Wednesday
                ["classroom",  "classroom",   "gym",        "tenny_room"],  # Thursday
                ["classroom",  "classroom",   "pool",       "tenny_room"],  # Friday
                ["tenny_room", "pool",        "campus",     "tenny_room"],  # Saturday
            ],
            "Love": 30,
            "Obed": 10,
            "Inbt": 5,
            "Lust": 5,
        },

        "shion": {
            "Name": "Shion",
            "color": "#c084fc",
            # The player's stepmother, married to his father (docs/plan_shion.md)
            "type": "family",
            "traits": ["experienced", "femdom", "married", "rich"],
            # cute_sex: her canon is sadistic ("Hit me harder... make me hurt"); she rolls hardcore or neither (author,
            # 2026-09-30)
            "blocked_traits": ["lesbian", "cute_sex"],
            "enabled": True,
            "body_type": "medium",
            "bust": "medium",
            # her solo scene is in the doggy pose (DG_MASTURBATE_*): the riding pose is off for her for now
            "mast_pose": "doggy",
            # Lives off campus, in the father's apartment (APARTMENT_ROOMS), and goes to the mall: campus pickers
            # never pick her (girl_off_campus) and "going home" is her bedroom there (girl_home_loc)
            "off_campus": True,
            # Her whole route is OPTIONAL: a new game asks (_stepmom_setup), an old save turns it on by default.
            # Off = she is "route_off" away forever (girl_route_enabled), her husband and the apartment with her.
            "route_flag": "_stepmom_route",
            "role": "stepmom",         # her role's line pools (rod_lines["role:stepmom"], girl_role)
            "husband": "Dad",          # her husband: the FamilyContact she lies to (shion_netori.rpy, girl_husband)
            "husband_love": 400,       # her love for him at the start (wife_love, family_father.rpy)
            "meets_at_home": True,     # she stays home until he meets her there (her intro: _apartment_intro)
            "home": "apartment_room",
            "leave_to": "apartment",   # walking out of her bedroom: the living room (girl_home_exit)
            "pill_own": True,          # her own pill, he has no say in it until her turn (girl_holds_her_pill)
            "no_photos": True,         # she NEVER texts him a photo, asked or not: no evidence (girl_sends_photos; author 2026-10-10)
            "anal_untouched": True,    # nobody ever had her ass, the player is the first (_anal_first_story_beat; author 2026-10-10)
            "phone_threshold": 400,    # a CEO does not hand her number to the boy: Love or Obed 400, and only past her cold step
            "schedule": [
                # Morning            Noon          Evening              Night
                ["apartment_room",   "mall",       "apartment",         "apartment_room"],    # Sunday
                ["apartment_shower", "apartment",  "apartment",         "apartment_room"],    # Monday
                ["apartment",        "mall",       "apartment_shower",  "apartment_room"],    # Tuesday
                ["apartment_shower", "apartment",  "mall",              "apartment_room"],    # Wednesday
                ["apartment",        "mall",       "apartment",         "apartment_shower"],  # Thursday
                ["apartment_shower", "apartment",  "apartment",         "apartment_room"],    # Friday
                ["apartment_room",   "mall",       "mall",              "apartment_room"],    # Saturday
            ],
            # docs/plan_shion.md Fase 2: family, so a little warmer than a stranger; obeys nobody; an experienced
            # adult, far less inhibited than the students
            "Love": 60,
            "Obed": 0,
            "Inbt": 150,
            "Lust": 5,
        },

    }

    _GIRL_ASSET_FOLDER = {gid: cfg["Name"] for gid, cfg in GIRLS_CONFIG.items()}

    def girl_asset_folder(girl):
        return _GIRL_ASSET_FOLDER.get(girl.gid if hasattr(girl, "gid") else girl.Id, girl.Name)

    ALL_GIRLS = []
    GIRL_BY_ID = {}

    # ----------------------------------------------
    # Outfit presets per girl
    # ----------------------------------------------
    OUTFIT_PRESETS = {
        "gwen": {
            "casual": {
                "over": "long_shirt",
                "chest": "corset",
                "legs": "blue_skirt",
                "panties": "purple",
                "shoes": "thigh_highs",
            },
            "pool": {
                "over": None,
                "chest": "bikini_top",
                "legs": None,
                "panties": "bikini_panties",
                "shoes": None,
            },
            "shower": {
                "over": None,
                "chest": None,
                "legs": None,
                "panties": None,
                "shoes": None,
            },
        },
        "rogue": {
            "casual": {
                "over": "long_shirt",
                "chest": "crop_top",
                "legs": "blue_skirt",
                "panties": "purple",
                "shoes": "thigh_highs",
            },
            "pool": {
                "over": None,
                "chest": "bikini_top",
                "legs": None,
                "panties": "bikini_panties",
                "shoes": None,
            },
            "shower": {
                "over": None,
                "chest": None,
                "legs": None,
                "panties": None,
                "shoes": None,
            },
        },
        "ntw": {
            "casual": {
                "over": "yellow_jacket",
                "chest": "yellow_bra",
                "legs": None,
                "panties": "yellow_panties",
                "shoes": None,
            },
            "pool": {
                "over": None,
                "chest": "bikini_top",
                "legs": None,
                "panties": "bikini_panties",
                "shoes": None,
            },
            "shower": {
                "over": None,
                "chest": None,
                "legs": None,
                "panties": None,
                "shoes": None,
            },
        },
        "tenny": {
            "casual": {
                "over": "blue_jacket",
                "mid": "blue_shirt",
                "chest": "white_bra",
                "legs": "white_legs",
                "panties": "striped_panties",
                "shoes": "thigh_highs",
            },
            "pool": {
                "over": None,
                "mid": None,
                "chest": "blue_bikini_top",
                "legs": None,
                "panties": "blue_bikini_bottom",
                "shoes": None,
            },
            "shower": {
                "over": None,
                "mid": None,
                "chest": None,
                "legs": None,
                "panties": None,
                "shoes": None,
            },
        },
        "shion": {
            "casual": {
                "over": "jacket",
                "mid": "vest",
                "chest": "bra",
                "panties": "panties",
                "skirt": "pants",
            },
            "pool": {
                "over": None,
                "mid": None,
                "chest": "bikini_top",
                "panties": "bikini_bottom",
            },
            "shower": {
                "over": None,
                "mid": None,
                "chest": None,
                "panties": None,
            },
        },
    }

    # ----------------------------------------------
    # Inbt requirements per piece (0–1000)
    # ----------------------------------------------
    CLOTHING_INBT_REQ = {
        "gwen": {
            "over": {
                "long_shirt": 0,
            },
            "chest": {
                "corset": 0,
                "bikini_top": 0,
            },
            "legs": {
                "blue_skirt": 0,
            },
            "panties": {
                "purple": 0,
                "bikini_panties": 0,
            },
            "shoes": {
                "thigh_highs": 0,
            },
        },
        "rogue": {
            "over": {
                "long_shirt": 0,
            },
            "chest": {
                "crop_top": 0,
                "bikini_top": 0,
            },
            "legs": {
                "blue_skirt": 0,
            },
            "panties": {
                "purple": 0,
                "bikini_panties": 0,
            },
            "shoes": {
                "thigh_highs": 0,
            },
        },
        "ntw": {
            "over": {
                "yellow_jacket": 0,
            },
            "chest": {
                "yellow_bra": 0,
                "bikini_top": 0,
            },
            "panties": {
                "yellow_panties": 0,
                "bikini_panties": 0,
            },
        },
        "tenny": {
            "over": {
                "blue_jacket": 0,
            },
            "mid": {
                "blue_shirt": 0,
            },
            "chest": {
                "white_bra": 0,
                "blue_bikini_top": 0,
            },
            "legs": {
                "white_legs": 0,
            },
            "panties": {
                "striped_panties": 0,
                "blue_bikini_bottom": 0,
            },
            "shoes": {
                "thigh_highs": 0,
            },
        },
        "shion": {
            "over": {
                "jacket": 0,
            },
            "mid": {
                "vest": 0,
            },
            "chest": {
                "bra": 0,
                "bikini_top": 0,
            },
            "panties": {
                "panties": 0,
                "bikini_bottom": 0,
            },
        },
    }

    # ----------------------------------------------
    # Clothing -> layeredimage attributes per girl
    # ----------------------------------------------
    CLOTHING_ATTRS = {
        "gwen": {
            "over": {
                "long_shirt": {"flag_false": "over_long_shirt", "flag_true": None},
            },
            "chest": {
                "corset": {"flag_false": "chest_corset", "flag_true": "chest_corset_down"},
            },
            "legs": {
                "blue_skirt": {"flag_false": "legs_blue_skirt", "flag_true": None},
            },
            "panties": {
                "purple": {"flag_false": "panties_purple", "flag_true": "panties_purple_down"},
            },
            "shoes": {
                "thigh_highs": {"flag_false": "shoes_thigh_highs", "flag_true": None},
            },
        },

        "rogue": {
            "over": {
                "long_shirt": {"flag_false": "over_long_shirt", "flag_true": None},
            },
            "chest": {
                "crop_top": {"flag_false": "chest_corset", "flag_true": "chest_corset_down"},
            },
            "legs": {
                "blue_skirt": {"flag_false": "legs_blue_skirt", "flag_true": None},
            },
            "panties": {
                "purple": {"flag_false": "panties_purple", "flag_true": "panties_purple_down"},
            },
            "shoes": {
                "thigh_highs": {"flag_false": "shoes_thigh_highs", "flag_true": None},
            },
        },

        "tenny": {
            "over": {
                "blue_jacket": {"flag_false": "over_blue_jacket", "flag_true": "over_blue_jacket_up"},
            },
            "mid": {
                "blue_shirt": {"flag_false": "mid_blue_shirt", "flag_true": "mid_blue_shirt_up"},
            },
            "chest": {
                "white_bra": {"flag_false": "chest_white_bra", "flag_true": "chest_white_bra_up"},
                "blue_bikini_top": {"flag_false": "chest_blue_bikini_top", "flag_true": "chest_blue_bikini_top_up"},
            },
            "legs": {
                "white_legs": {"flag_false": "legs_white_legs", "flag_true": None},
            },
            "panties": {
                "striped_panties": {"flag_false": "panties_striped", "flag_true": "panties_striped_down"},
                "blue_bikini_bottom": {"flag_false": "panties_blue_bikini", "flag_true": "panties_blue_bikini_down"},
            },
            "shoes": {
                "thigh_highs": {"flag_false": "shoes_thigh_highs", "flag_true": None},
            },
        },

        "ntw": {
            "over": {
                "yellow_jacket": {"flag_false": "over_long_shirt", "flag_true": None},
            },
            "chest": {
                "yellow_bra": {"flag_false": "chest_corset", "flag_true": "chest_clothes_none"},
            },
            "panties": {
                "yellow_panties": {"flag_false": "panties_purple", "flag_true": None},
            },
        },

    }
    # ----------------------------------------------
    # Clothing -> BJ layeredimage attributes per girl
    # ----------------------------------------------
    BJ_CLOTHING_ATTRS = {
        "gwen": {
            "over": {
                "long_shirt": {"flag_false": ["over_long_shirt"], "flag_true": []},
            },
            "chest": {
                "corset": {"flag_false": ["chest_corset", "corset", "boobs_clothes_1"], "flag_true": []},
            },
            "legs": {
                "blue_skirt": {"flag_false": ["legs_blue_skirt"], "flag_true": []},
            },
            "panties": {
                "purple": {"flag_false": ["panties_purple"], "flag_true": []},
            },
            "shoes": {
                "thigh_highs": {"flag_false": ["legs_thigh_highs"], "flag_true": []},
            },
        },
        "rogue": {
            "over": {
                "long_shirt": {"flag_false": ["over_long_shirt"], "flag_true": []},
            },
            "chest": {
                # flag_false = crop-top no lugar (mostrar tudo)
                # flag_true  = crop-top puxado (ChestUp=True, seios expostos)
                "crop_top": {
                    "flag_false": ["boobs_clothed", "crop_top_bottom", "crop_top_braces", "crop_top_top"],
                    "flag_true":  [],
                },
            },
            "legs": {
                "blue_skirt": {"flag_false": ["legs_blue_skirt"], "flag_true": []},
            },
            "panties": {
                "purple": {"flag_false": ["panties_purple"], "flag_true": ["panties_purple_down"]},
            },
            "shoes": {
                "thigh_highs": {"flag_false": ["shoes_thigh_highs"], "flag_true": []},
            },
        },
    }

    # ----------------------------------------------
    # Clothing -> RCG layeredimage attributes per girl
    # ----------------------------------------------
    RCG_CLOTHING_ATTRS = {
        "gwen": {
            "over": {
                "long_shirt": {"flag_false": ["torso_over_long_shirt"], "flag_true": []},
            },
            "chest": {
                "corset": {"flag_false": ["torso_chest_corset"], "flag_true": []},
            },
            "legs": {
                "blue_skirt": {"flag_false": ["skirt_on"], "flag_true": []},
            },
            "panties": {
                "purple": {"flag_false": ["panties_1"], "flag_true": []},
            },
            "shoes": {
                "thigh_highs": {"flag_false": ["thigh_highs_on"], "flag_true": []},
            },
        },
        "rogue": {
            "over": {
                "long_shirt": {"flag_false": ["torso_over_long_shirt"], "flag_true": []},
            },
            "chest": {
                "corset": {"flag_false": ["torso_chest_corset"], "flag_true": []},
            },
            "legs": {
                "blue_skirt": {"flag_false": ["skirt_on"], "flag_true": []},
            },
            "panties": {
                "purple": {"flag_false": ["panties_1"], "flag_true": []},
            },
            "shoes": {
                "thigh_highs": {"flag_false": ["thigh_highs_on"], "flag_true": []},
            },
        },
    }

    # ----------------------------------------------
    # Clothing -> COWGIRL layeredimage attributes per girl
    # ----------------------------------------------
    COWGIRL_CLOTHING_ATTRS = {
        "gwen": {
            "over": {
                "long_shirt": {"flag_false": ["torso_over_long_shirt"], "flag_true": []},
            },
            "chest": {
                "corset": {"flag_false": [], "flag_true": []},
            },
            "panties": {
                "purple": {"flag_false": ["panties_top_1", "panties_bottom_1"], "flag_true": ["panties_top_2", "panties_bottom_none"]},
            },
            "shoes": {
                "thigh_highs": {"flag_false": ["thigh_highs_on"], "flag_true": []},
            },
        },
        "rogue": {
            "over": {
                "long_shirt": {"flag_false": ["torso_over_long_shirt"], "flag_true": []},
            },
            "chest": {
                "corset": {"flag_false": ["torso_clothing_corset"], "flag_true": ["torso_clothing_corset_up"]},
            },
            "panties": {
                "purple": {"flag_false": ["panties_top_1", "panties_bottom_1"], "flag_true": ["panties_top_2", "panties_bottom_none"]},
            },
            "shoes": {
                "thigh_highs": {"flag_false": ["thigh_highs_on"], "flag_true": []},
            },
        },
    }

    # ----------------------------------------------
    # Tastes and friendships of a new game: the ONE roll of each
    # ----------------------------------------------
    # Tastes: girl creation, _reset_all_girls, and restaurant_date for an old save that never rolled them.
    # GIRL_DISH_WEIGHTS: her story can tilt her favorite dish (Rogue: fried chicken, the South).
    GIRL_DISHES = ("steak", "pasta", "chicken", "salad")
    GIRL_DISH_WEIGHTS = {"rogue": {"chicken": 3}}

    def roll_girl_tastes(girl, drink=True):
        """Favorite / hated dish (weighted by her story) and, with drink=True, favorite / hated drink tier + brand."""
        _w = GIRL_DISH_WEIGHTS.get(girl.gid, {})
        _pool = []
        for _d in GIRL_DISHES:
            _pool += [_d] * _w.get(_d, 1)
        girl.FavoriteDish = renpy.random.choice(_pool)
        girl.HatedDish = renpy.random.choice([_d for _d in GIRL_DISHES if _d != girl.FavoriteDish])
        if drink:
            girl.FavoriteDrink = renpy.random.choice(["low", "med", "high"])
            girl.HatedDrink = renpy.random.choice([_t for _t in ("low", "med", "high") if _t != girl.FavoriteDrink])
            # alcohol.rpy may load after the girls: _reset_all_girls rolls it again at label start
            girl.FavoriteBrand = renpy.random.choice(drinks_of_tier(girl.FavoriteDrink)) if callable(globals().get("drinks_of_tier")) else None

    # Friendships between the girls start at 400-600, shifted by her personality: Rogue warm with everyone (a chosen
    # family), NTW cool (cooler with eager Tenny), Gwen cautious. How fast they grow: GIRL_LIKE_GAIN_MULT.
    GIRL_LIKE_START = {
        "rogue": {"_all": 100, "shion": -350},
        "ntw":   {"_all": -50, "tenny": -100, "shion": -350},
        "gwen":  {"_all": -50, "shion": -350},
        "tenny": {"shion": -350},
        "shion": {"_all": -350},    # she doesn't know the students and they don't know her
    }

    def roll_girl_likes():
        """Every girl's starting friendship with every other one (game launch and _reset_all_girls)."""
        for _g in ALL_GIRLS:
            _shift = GIRL_LIKE_START.get(_g.gid, {})
            for _other in ALL_GIRLS:
                if _g.gid != _other.gid:
                    _g.set_like_for(_other.gid, renpy.random.randint(400, 600) + _shift.get(_other.gid, _shift.get("_all", 0)))

    # ----------------------------------------------
    # Create girls from config + default clothing state
    # ----------------------------------------------
    for gid, cfg in GIRLS_CONFIG.items():
        name = cfg.get("Name", gid.capitalize())
        color = cfg.get("color", "#ffffff")

        girl = Girl(gid, name, color=color, body_type=cfg.get("body_type", "medium"), bust=cfg.get("bust", "medium"))

        # schedule
        if "schedule" in cfg:
            girl.schedule = cfg["schedule"]

        # base stats — use config values, fallback to defaults
        girl.Love = int(cfg.get("Love", 50))
        girl.Obed = int(cfg.get("Obed", 15))
        girl.Inbt = int(cfg.get("Inbt", 10))
        girl.Lust = int(cfg.get("Lust", 5))

        # Optional: traits and cheat attitude defaults
        for tr in cfg.get("traits", []):
            girl.add_trait(tr)

        if "cheat_attitude" in cfg:
            girl.CheatAttitude = int(cfg["cheat_attitude"])

        _npc = cfg.get("npc_partner")
        if _npc:
            girl.set_npc_partner(_npc)

        girl.gid = gid
        girl.mast_pose = cfg.get("mast_pose", "cowgirl")

        # Set each girl's home to her own room (defined in config)
        girl.home = cfg.get("home", "room")

        # Starting location: debug override or scheduled slot for Day 1 / Morning
        if DEBUG_ALL_IN_PLAYER_ROOM:
            girl.loc = "room"
        else:
            girl.loc = girl.get_scheduled_location(1, 0)

        # expression
        girl.current_expression = "normal"

        # clothing state defaults (internal codes, not attribute names)
        girl.Over = None
        girl.Chest = None
        girl.Legs = None
        girl.Panties = None
        girl.Shoes = None

        girl.OverUp = False
        girl.ChestUp = False
        girl.LegsDown = False
        girl.PantiesDown = False

        girl.CurrentOutfitPreset = None

        # Favorite act: random initial preference + threshold (1-5 orgasms)
        # Virgins can only start with kiss or massage
        if girl.has_trait("virgin"):
            _fav_acts = ["kiss", "massage"]
        else:
            _fav_acts = [a for a in _INITIAL_FAV_ACTS if girl_has_pose(girl, _ACT_TO_POSE.get(a, a))]
        girl.FavoriteAct = renpy.random.choice(_fav_acts)          # an act KEY (never a translated text)
        girl.FavoriteActThreshold = renpy.random.randint(1, 5)
        girl._favorite_act_unlocked = False

        # Tastes: favorite / hated dish and drink (the ONE roll, persists in the save)
        roll_girl_tastes(girl)

        # Per-girl randomized thresholds for questions / phone (a girl with no reason to hand her
        # number out pins it high in GIRLS_CONFIG "phone_threshold")
        girl.phone_threshold = cfg.get("phone_threshold") or renpy.random.randint(50, 150)
        girl.q_threshold_virgin = renpy.random.randint(200, 400)
        girl.q_threshold_fav_act = renpy.random.randint(150, 350)

        GIRL_BY_ID[gid] = girl
        if cfg.get("enabled", True):
            ALL_GIRLS.append(girl)

    Gwen = GIRL_BY_ID["gwen"]
    Rogue = GIRL_BY_ID["rogue"]
    NTW = GIRL_BY_ID["ntw"]
    Tenny = GIRL_BY_ID["tenny"]
    Shion = GIRL_BY_ID["shion"]

    # Girl-to-girl friendships (the ONE roll)
    roll_girl_likes()

    # ----------------------------------------------
    # New-game reset: restore girls to GIRLS_CONFIG defaults
    # (init python only runs on app launch; label start needs this
    #  so that Main Menu → New Game properly wipes old state)
    # ----------------------------------------------
    def _reset_all_girls():
        """Reset every girl to her GIRLS_CONFIG defaults for a new game."""
        _tmpl = Girl("_tmpl", "_Template")
        _template_keys = set(vars(_tmpl).keys())
        for gid, cfg in GIRLS_CONFIG.items():
            girl = GIRL_BY_ID.get(gid)
            if not girl:
                continue

            # Re-run __init__ to wipe ALL attributes back to defaults
            Girl.__init__(girl, girl.Id, girl.Name, color=girl.color, body_type=cfg.get("body_type", "medium"), bust=cfg.get("bust", "medium"))
            girl.gid = gid  # not set by __init__
            girl.mast_pose = cfg.get("mast_pose", "cowgirl")

            # Remove ad-hoc attributes that __init__ doesn't declare
            for _stale in list(vars(girl).keys()):
                if _stale not in _template_keys and _stale != "gid":
                    delattr(girl, _stale)

            # Re-apply per-girl config (mirrors the creation loop above)
            if "schedule" in cfg:
                girl.schedule = cfg["schedule"]

            girl.Love = int(cfg.get("Love", 50))
            girl.Obed = int(cfg.get("Obed", 15))
            girl.Inbt = int(cfg.get("Inbt", 10))
            girl.Lust = int(cfg.get("Lust", 5))

            for tr in cfg.get("traits", []):
                girl.add_trait(tr)

            if "cheat_attitude" in cfg:
                girl.CheatAttitude = int(cfg["cheat_attitude"])

            _npc = cfg.get("npc_partner")
            if _npc:
                girl.set_npc_partner(_npc)

            girl.home = cfg.get("home", "room")

            if DEBUG_ALL_IN_PLAYER_ROOM:
                girl.loc = "room"
            else:
                girl.loc = girl.get_scheduled_location(1, 0)

            girl.current_expression = "normal"

            # Favorite act: random initial preference
            if girl.has_trait("virgin"):
                _fav_acts = ["kiss", "massage"]
            else:
                _fav_acts = [a for a in _INITIAL_FAV_ACTS if girl_has_pose(girl, _ACT_TO_POSE.get(a, a))]
            girl.FavoriteAct = renpy.random.choice(_fav_acts)      # an act KEY (never a translated text)
            girl.FavoriteActThreshold = renpy.random.randint(1, 5)
            girl._favorite_act_unlocked = False

            # Tastes of the new game (the ONE roll)
            roll_girl_tastes(girl)

            girl.phone_threshold = GIRLS_CONFIG.get(gid, {}).get("phone_threshold") or renpy.random.randint(50, 150)
            girl.q_threshold_virgin = renpy.random.randint(200, 400)
            girl.q_threshold_fav_act = renpy.random.randint(150, 350)

            # Re-apply default casual outfit
            if gid in OUTFIT_PRESETS and "casual" in OUTFIT_PRESETS[gid]:
                girl.WearPreset("casual", apply_now=False)

        # Randomize fertility cycle offsets. The initial PILL state is rolled at label _after_rods_choice
        # (script.rpy): it needs the pregnancy mode and the final traits, and neither exists yet here.
        for _g in ALL_GIRLS:
            _g._cycle_offset = renpy.random.randint(0, 27)

        # Re-initialize girl-to-girl friendships (the ONE roll)
        roll_girl_likes()

        # Girls are init-time objects: the main menu snapshotted the PREVIOUS game's girls into _girl_save.
        # Left as is, the rollback recovery in _refresh_girl_save sees "partner in the snapshot, none on the girl,
        # no breakup marker" and brings that game's girls back at the first interaction of this one.
        store._npc_partner_cleared = set()
        store._girl_save = _snapshot_girls()
        print("[NEW_GAME] girl snapshot and partner-cleared marker reset for the new game")

    # ----------------------------------------------
    # Save/Load: snapshot & restore mutable girl state
    # Girls are created in init python (needed by layeredimage etc.)
    # but init runs on every launch, resetting stats.
    # We snapshot __dict__ into a default variable before each save
    # opportunity, and restore from it in after_load.
    # ----------------------------------------------
    def _snap_one_girl(g):
        """Snapshot a single girl's __dict__ (sets→tagged lists)."""
        gd = {}
        for k, v in g.__dict__.items():
            if isinstance(v, set):
                gd[k] = ("__set__", list(v))
            elif isinstance(v, dict):
                gd[k] = dict(v)
            elif isinstance(v, list):
                gd[k] = list(v)
            else:
                gd[k] = v
        return gd

    def _snapshot_girls():
        """Return a dict of all girl states for persistence."""
        d = {}
        for g in ALL_GIRLS:
            d[g.gid] = _snap_one_girl(g)
        return d

    def _sync_girl(girl):
        """Update _girl_save for one girl immediately (called after stat changes)."""
        d = getattr(store, "_girl_save", None)
        if d is None:
            return
        gid = getattr(girl, "gid", None)
        if gid:
            d[gid] = _snap_one_girl(girl)

    # Identity mirrors whose "unset" value (None) means NEW partner, roll him / her (create_npc_partner).
    # A save older than the mirror has no such key: her partner of that save is NOT new, so he / she keeps
    # what that version gave everybody instead of being rolled on the first load.
    _NPC_PARTNER_LEGACY_MIRRORS = {"_npc_partner_traits": set(), "_ntr_boundary_level": 1}

    # {gid: deep copy of her __dict__ at the END of init} = the state a fresh launch has. Filled once by the
    # init 999 block at the end of this file; init-time, never saved.
    _GIRL_INIT_BASELINE = {}
    _GIRL_INIT_KEYS = {}        # {gid: every attribute name she has at the end of init} (copyable or not)

    def _girl_baseline_capture():
        import copy as _copy
        for _g in ALL_GIRLS:
            _base = {}
            for _k, _v in _g.__dict__.items():
                try:
                    _base[_k] = _copy.deepcopy(_v)
                except Exception as _e:
                    # never block the startup: a value that cannot be copied is simply never reset
                    print("[SAVE] %s.%s left out of the init baseline (%r)" % (_g.gid, _k, _e))
            _GIRL_INIT_BASELINE[_g.gid] = _base
            _GIRL_INIT_KEYS[_g.gid] = set(_g.__dict__.keys())
        print("[SAVE] init baseline captured for %d girl(s)" % len(_GIRL_INIT_BASELINE))

    def _restore_girls(saved, partial=False):
        """Restore mutable girl state from snapshot dict after load.
        partial=True (rollback recovery): only the girls present in `saved` are touched. A load passes every
        girl, so a girl missing from it is reset to her init state; a partial dict must never do that."""
        import copy as _copy
        if not saved:
            return
        for g in ALL_GIRLS:
            if partial and g.gid not in saved:
                continue
            gd = saved.get(g.gid) or {}
            # Girls are init-time objects: they SURVIVE a load inside the same session. Whatever this save does
            # not carry (an attribute newer than the save, a girl newer than the save) must look like a fresh
            # launch, not like the game that was open before: it used to keep that game's value (new game,
            # Gwen pregnant, load an older save: Gwen pregnant there too, and the next snapshot saved it).
            _base = _GIRL_INIT_BASELINE.get(g.gid)
            if _base is not None:
                _reset = [k for k in _base if k not in gd]
                for k in _reset:
                    setattr(g, k, _copy.deepcopy(_base[k]))
                # attributes another game of this session created ad hoc (not declared at init, not in this save)
                _init_keys = _GIRL_INIT_KEYS.get(g.gid, ())
                _stale = [k for k in list(vars(g).keys()) if k not in gd and k not in _init_keys]
                for k in _stale:
                    delattr(g, k)
                if _reset or _stale:
                    print("[SAVE] %s: %d attr(s) not in this save back to their init value, %d ad hoc dropped: %s" % (
                        g.gid, len(_reset), len(_stale), ", ".join(sorted(_reset + _stale)[:12])))
            if not gd:
                continue
            for k, v in gd.items():
                if isinstance(v, tuple) and len(v) == 2 and v[0] == "__set__":
                    setattr(g, k, set(v[1]))
                else:
                    setattr(g, k, v)
            if g.has_npc_partner():
                _legacy = [k for k in _NPC_PARTNER_LEGACY_MIRRORS if k not in gd]
                for k in _legacy:
                    setattr(g, k, _copy.deepcopy(_NPC_PARTNER_LEGACY_MIRRORS[k]))
                if _legacy:
                    print("[MIGRATE] %s: old save without %s, existing partner kept as he / she was (no roll)" % (g.gid, ", ".join(_legacy)))

    def _backfill_girl_attrs():
        """Ensure every Girl has all current attributes.
        Creates a template Girl with __init__ defaults and copies
        any missing attribute to each real girl. Called in after_load
        so old saves get new attributes without losing existing stats."""
        import copy as _copy
        _tmpl = Girl("_tmpl", "_Template")
        _patched = {}
        for g in ALL_GIRLS:
            _missing = []
            for k, v in _tmpl.__dict__.items():
                if k in ("Id", "Name", "color", "body_type", "bust", "default_pose", "gid"):
                    continue
                if not hasattr(g, k):
                    setattr(g, k, _copy.deepcopy(v))
                    _missing.append(k)
            if _missing:
                _patched[g.gid] = _missing
                debug_log("[MIGRATE] %s: backfilled %d attrs: %s" % (g.gid, len(_missing), ", ".join(_missing)))
            # Old saves: some paths recorded a position without the "sex" act (anniversary gift, NTR bet,
            # anal -> vaginal switch). Every reader now checks the act, so give it back to her.
            girl_history_normalize(g)
            _backfill_girl_knowledge(g)
            # Old saves: the hardcore "goes back to her ex" restore brought an ex-girlfriend back flagged male
            _repair_npc_partner_gender(g)
            # Old saves: a girlfriend's rolled history could hold a boyfriend's acts (raw sex, creampie)
            bf_history_drop_male_acts(g)
            # v0.12 saves: undo the sterilization her birth forced (the birth limit is gone)
            pregnancy_procedure_backfill(g)
            # Old saves: a child counted before the child record existed (children.rpy)
            children_sync(g)
        return _patched

    def _backfill_girl_knowledge(girl):
        """Old saves: knowledge learned from a position video only holds the position. Add the act."""
        for _attr in ("knows_acts", "knows_with_player"):
            for _gid, _known in (getattr(girl, _attr, None) or {}).items():
                if isinstance(_known, set):
                    _known.update([scene_type_act(_a) for _a in list(_known)])

    # Partner-history acts only a boyfriend can have done to her, and the tier they start at (_generate_bf_history:
    # 5 = raw sex, 6 = creampie). A girlfriend's history stops at "sex".
    BF_MALE_ONLY_ACTS = ("sex_raw", "creampie")
    BF_FEMALE_MAX_TIER = 4

    def bf_history_from_men(girl):
        """Whether her partner history (bf_history) may hold BF_MALE_ONLY_ACTS: it is a boyfriend's, or she is an
        experienced non-lesbian, whose history is her past with men (_apply_experienced writes it after the partner
        roll, whoever her partner is)."""
        return not girl.has_npc_girlfriend() or (girl.has_trait("experienced") and not girl.has_trait("lesbian"))

    def bf_history_drop_male_acts(girl):
        """Her history is a girlfriend's (bf_history_from_men False): no BF_MALE_ONLY_ACTS in it, tier capped at
        "sex". Runs where a history is rolled, where randomize flags the partner female, and on load."""
        if bf_history_from_men(girl):
            return False
        _h = getattr(girl, "bf_history", None) or {}
        _dropped = [_a for _a in BF_MALE_ONLY_ACTS if _h.get(_a)]
        for _a in _dropped:
            _h[_a] = False
        _capped = (getattr(girl, "bf_max_tier", 0) or 0) > BF_FEMALE_MAX_TIER
        if _capped:
            girl.bf_max_tier = BF_FEMALE_MAX_TIER
        if _dropped or _capped:
            print("[BF_HISTORY] %s: girlfriend partner, dropped %s from her history, tier capped: %s" % (
                girl.gid, _dropped, _capped))
        return bool(_dropped or _capped)

    def _repair_npc_partner_gender(girl):
        """Old saves: the hardcore "goes back to her ex" restore ran after clear_npc_partner() had wiped
        partner_is_female, so an ex-girlfriend came back flagged male, and a save without a saved id got
        "bf_<gid>", an id the registry never uses (get_npc_partner_for returned None).
        Fires on those two signatures only: no healthy path writes an "npc_gf_" id with a male flag, or a
        non-canonical id. Runs before rebuild_npc_partners(), which then recreates her partner with the
        right gender and the name still saved on the girl. Returns True when something was fixed."""
        if not girl.has_npc_partner():
            return False
        _prefixes = Girl._NPC_PARTNER_ID_PREFIX
        _old_id = str(girl.npc_partner_id)
        _old_f = girl.get_flag("partner_is_female")
        _canonical = any(_old_id.startswith(_p) for _p in _prefixes.values())
        if _canonical and (_old_f or not _old_id.startswith(_prefixes["female"])):
            return False   # healthy, or "npc_bf_" + female flag (never produced, ambiguous): leave it
        _gender = girl.resolve_npc_partner_gender(_old_id, "female" if _old_f else None)
        girl.npc_partner_id = girl.npc_partner_canonical_id(_gender)
        girl.set_flag("partner_is_female", _gender == "female")
        print("[MIGRATE] %s: NPC partner repaired: id %s -> %s, partner_is_female %s -> %s" % (
            girl.gid, _old_id, girl.npc_partner_id, _old_f, _gender == "female"))
        return True

    def _backfill_player_attrs():
        """Ensure Player has all current PlayerData attributes."""
        import copy as _copy
        _tmpl = PlayerData()
        _missing = []
        _player = store.Player
        for k, v in _tmpl.__dict__.items():
            if k in ("Name", "cash", "energy"):
                continue
            if not hasattr(_player, k):
                setattr(_player, k, _copy.deepcopy(v))
                _missing.append(k)
        if _missing:
            debug_log("[MIGRATE] Player: backfilled %d attrs: %s" % (len(_missing), ", ".join(_missing)))
        return _missing

    def _refresh_girl_save():
        """Keep the saved snapshot current. Girls are init-time objects, so only _girl_save
        reaches the save file. Ren'Py pickles the store BEFORE config.save_json_callbacks run
        (renpy/loadsave.py: dump() first, callbacks later), so a snapshot taken in the pre-save
        callback only lands in the NEXT save. Refreshing at the start of every interaction makes
        each save carry every girl change made so far (flags from discover(), clothes, lust...).

        Rollback recovery: _girl_save is a default var (rollback-safe), but Girl objects are
        init-time (not rollback-safe). After a breakup rollback, _girl_save reverts to having
        the partner while the Girl stays mutated. _npc_partner_cleared is also rollback-safe,
        so its marker disappears after rollback, letting us detect the inconsistency."""
        try:
            _saved = getattr(store, "_girl_save", None)
            if _saved:
                _cleared = getattr(store, "_npc_partner_cleared", set()) or set()
                _to_restore = {}
                for _psg in ALL_GIRLS:
                    _sg = _saved.get(_psg.gid) or {}
                    if _sg.get("npc_partner_id") and not _psg.npc_partner_id and _psg.gid not in _cleared:
                        _to_restore[_psg.gid] = _sg
                        print("[ROLLBACK] %s: NPC partner %s lost but breakup marker absent, restoring" % (_psg.gid, _sg["npc_partner_id"]))
                if _to_restore:
                    _restore_girls(_to_restore, partial=True)
                    rebuild_npc_partners()
                    print("[ROLLBACK] %d girl(s) + NPC partners restored" % len(_to_restore))

            for _psg in ALL_GIRLS:
                if _psg.has_npc_partner():
                    _psnpc = NPC_PARTNERS.get(_psg.npc_partner_id)
                    if _psnpc:
                        _psg._npc_friendship = getattr(_psnpc, "friendship_with_player", 200)
                        _psg._npc_love = getattr(_psnpc, "love_for_girl", 750)
                        _psg._npc_suspicion = getattr(_psnpc, "suspicion", 0)
            store._girl_save = _snapshot_girls()
        except Exception as _e:
            print("[GIRL_SAVE] refresh failed: %r" % (_e,))
    config.interact_callbacks.append(_refresh_girl_save)

    # Pre-save: same refresh (covers autosaves triggered outside an interaction) + debug dump.
    def _pre_save_snapshot(d):
        _refresh_girl_save()
        debug_log("[PRE_SAVE] bk_in_store=%s  bk_current_bg=%s  CurrentLocation=%s" % (
            getattr(store, "bk_in_store", "MISSING"),
            getattr(store, "bk_current_bg", "MISSING"),
            getattr(store, "CurrentLocation", "MISSING")))
        for _psg in ALL_GIRLS:
            _psc = getattr(_psg, "clothes", {})
            debug_log("[PRE_SAVE] gid=%s loc=%s clothes=%s" % (_psg.gid, getattr(_psg, "loc", "?"), str(_psc)))
    config.save_json_callbacks.append(_pre_save_snapshot)

    # ============================================================
    # SCENE ESCALATION (centralized)
    # Called when a scene escalates from rub/tip to full sex/anal.
    # Replaces inline mark_intimacy + Change_Status + cheat blocks.
    # ============================================================
    def _anal_first_story_beat(girl):
        """Her FIRST anal ever, said out loud, for the girl whose config swears nobody came before
        (GIRLS_CONFIG "anal_untouched"; the author 2026-10-10: Shion never did it, the player is the
        first; her husband never dared to ask). The experienced trait made the voice read like routine
        (tester 2026-10-10). Plays once, at the moment anal becomes real, from both doors (start_scene
        and the rub/tip escalation)."""
        if not GIRLS_CONFIG.get(getattr(girl, "gid", None), {}).get("anal_untouched"):
            return
        if getattr(girl, "_anal_first_beat_done", False) or (getattr(girl, "Sex_acts", {}) or {}).get("anal", 0) > 0:
            return
        girl._anal_first_beat_done = True
        set_scene_expression(girl, "shy")
        Say_Line(girl, rod_pick_line(girl, "anal_her_first"))
        Say_Line(girl, rod_pick_line(girl, "anal_her_first_2"))
        print("[STORY] %s: her first anal ever, the scripted beat played" % girl.gid)

    def _scene_escalation(girl, to_action, position):
        """Called when a scene escalates from rub/tip to full sex/anal."""
        debug_log("[ESCALATION] %s escalating to %s (%s)" % (girl.gid, to_action, position))
        # Act first, position second: the position reads the act to know which hole this scene is.
        _esc_act = "anal" if to_action == "anal" else "sex"
        if _esc_act == "anal":
            _anal_first_story_beat(girl)
        _esc_again = _scene_act_marked(girl, _esc_act)
        mark_intimacy(girl, _esc_act)
        mark_intimacy(girl, position)
        if _esc_again:
            # De-escalated and came back in the same scene: counters and stats were already given
            debug_log("[ESCALATION] %s re-escalation in the same scene: no new counters / stats" % girl.gid)
            return
        if to_action == "anal":
            Change_Status(girl, "Love", 10)
            Change_Status(girl, "Inbt", 15)
            Change_Status(girl, "Obed", 12)
        else:
            Change_Status(girl, "Love", 15)
            Change_Status(girl, "Inbt", 10)
            Change_Status(girl, "Obed", 5)
        sex_accept_with_temptation(girl, "sex")
        _notify_cheat_heat(girl, "scene_%s" % to_action)
        if _is_on_cheat_path(girl):
            _advance_cheat_stage(girl, 3)
        if getattr(store, "_crowd_level", 0) > 0:
            girl.CorruptionPublicHeavyActs = getattr(girl, "CorruptionPublicHeavyActs", 0) + 1
            girl.check_corruption("public")

    # ── Girl-initiated escalation (shared logic) ──────────────

    def _girl_esc_roll(girl):
        """Calculate and roll girl-initiated escalation chance. Returns True if triggered."""
        lust = getattr(girl, "Lust", 0)
        chance = 0
        if lust >= 90:
            chance = 35
        elif lust >= 70:
            chance = 20
        elif lust >= 50:
            chance = 8
        if girl.has_trait("hardcore_sex"):
            chance += 15
        if girl.has_trait("cum_slut"):
            chance += 10
        if getattr(girl, "Inbt", 0) >= 800:
            chance += 10
        chance += int(15 * femdom_intensity(girl))   # femdom: she decides when it goes further (Actions/femdom.rpy)
        roll = renpy.random.randint(1, 100)
        debug_log("[GIRL_ESC] lust=%d chance=%d roll=%d triggered=%s" % (lust, chance, roll, roll <= chance))
        return roll <= chance

    _GIRL_ESC_RUB_TO_TIP = {
        "virgin": [
            _("I... I want to feel it... just the tip... please..."),
            _("Can you... put it in? Just a little? I want to know what it feels like..."),
            _("I can't take it anymore... just the tip... I need to feel it inside..."),
        ],
        "boyfriend": [
            _("My boyfriend never does this to me... put it in, just the tip..."),
            _("I shouldn't want this but... just the tip... he'll never know..."),
            _("I can feel you right there... just put it in a little... I won't tell anyone..."),
        ],
        "femdom": [
            _("Enough rubbing. Put the tip in. That's not a request."),
            _("I've decided you've waited long enough. The tip. Now."),
            _("Stop teasing me and push the tip in. I'll tell you when you get more."),
        ],
        "hardcore": [
            _("Stop teasing me. Put it in. At least the tip."),
            _("I'm tired of rubbing. Give me the tip. NOW."),
            _("Enough with the foreplay. Tip. Now."),
        ],
        "cute": [
            _("I... mmm... can you put just the tip in...? Just to see how it feels..."),
            _("This feels really good but... I want a little more... just the tip?"),
            _("D-don't laugh but... I want you to put it in... just a tiny bit..."),
        ],
        "default": [
            _("Mmm... put it in. Just the tip."),
            _("I want to feel it inside... just a little."),
            _("Stop teasing and give me the tip already..."),
        ],
    }

    _GIRL_ESC_TIP_TO_SEX = {
        "virgin": [
            _("I know I said just the tip but... push it in... all of it... I want my first time to be now..."),
            _("I can't... I can't hold back... put it all in... I don't care about the tip anymore..."),
            _("It feels too good to stop... go deeper... take me..."),
        ],
        "boyfriend": [
            _("Fuck the tip... put it all in. I don't care about him right now."),
            _("I can't believe I'm saying this but... go all the way. He never makes me feel like this."),
            _("Deeper... forget about 'just the tip'... I want all of you inside me..."),
        ],
        "femdom": [
            _("The tip was my idea. So is this. All the way in."),
            _("I'm done with the tip. Give me all of it, right now."),
            _("You wait until I say, and I'm saying it. Deeper."),
        ],
        "hardcore": [
            _("Fuck the tip. Go ALL the way in. NOW."),
            _("I'm done with this tip bullshit. FUCK ME."),
            _("Deeper. All the way. Stop holding back!"),
        ],
        "cum_slut": [
            _("Push it deeper... I want to feel you cum inside me..."),
            _("Forget the tip... I need all of it... I need you to fill me up..."),
            _("More... I need more... go all the way and don't pull out..."),
        ],
        "cute": [
            _("I... I want more... is that okay? Go deeper..."),
            _("The tip isn't enough anymore... I need all of it..."),
            _("Please... don't stop at the tip... I want to feel everything..."),
        ],
        "default": [
            _("Forget the tip... go all the way in."),
            _("Deeper. I want all of it."),
            _("Stop teasing me and fuck me properly."),
        ],
    }

    _GIRL_ESC_ACCEPT_SEX_VIRGIN = [
        _("W-wait... all of it? I... okay... just be gentle..."),
        _("Oh god... it's going deeper... I've never... just go slow..."),
        _("I'm scared but... I want this. All of it. Just... careful..."),
    ]

    _GIRL_ESC_ACCEPT_SEX_NORMAL = [
        _("Yes... YES! That's it!"),
        _("Oh god... finally... don't stop!"),
        _("Mmm... so much better than just the tip..."),
    ]

    _GIRL_ESC_DENY_RUB = [
        _("Mmm... fine. But you're missing out."),
        _("Ugh... okay. Keep rubbing then."),
        _("You're such a tease..."),
    ]

    _GIRL_ESC_DENY_TIP = [
        _("Ugh... you're killing me. Fine."),
        _("You're really going to make me beg, aren't you?"),
        _("I hate you right now... but fine."),
    ]

    _GIRL_ESC_TIP_TO_ANAL = {
        "femdom": [
            _("Now my ass. I decided. Put it in."),
            _("Out of my pussy and into my ass. Don't make me repeat it."),
            _("You're going in my ass next. I'm not asking."),
        ],
        "hardcore": [
            _("I don't want it there. Put it in my ass. NOW."),
            _("Stop playing around. You know where I want it. My ass. Do it."),
            _("Forget my pussy. Shove it in my ass already."),
        ],
        "cum_slut": [
            _("Mmm... you know what would feel even better? My ass. Come on..."),
            _("I want to feel you back there... put it in my ass, please..."),
            _("My ass is so empty right now... fix that for me..."),
        ],
        "cute": [
            _("I... um... can you put it... in the other hole? Please..."),
            _("I know this is weird but... I really want it in my... you know..."),
            _("Don't laugh but... I kind of want it in my butt... is that okay?"),
        ],
        "addicted": [
            _("You KNOW where I want it. Stop wasting time with my pussy."),
            _("My ass is literally aching for you. Put it in already!"),
            _("I swear if you don't put it in my ass right now I'm going to lose it."),
        ],
        "default": [
            _("I want you in my ass instead... go deeper back there."),
            _("Forget the tip... put it in my ass. I need it."),
            _("My ass wants all of you. Don't make me beg."),
        ],
    }

    _GIRL_ESC_ACCEPT_ANAL = [
        _("Oh god... yes... right where I need it..."),
        _("Finally... that's so much better..."),
        _("Mmm... thank you... that's exactly what I wanted..."),
    ]

    def _girl_esc_pick_key(girl):
        """Pick the dialogue key based on girl traits."""
        if girl.has_trait("virgin"):
            return "virgin"
        if hasattr(girl, "has_npc_partner") and girl.has_npc_partner():
            return "boyfriend"
        if girl.has_trait("femdom"):
            return "femdom"
        if girl.has_trait("hardcore_sex"):
            return "hardcore"
        if girl.has_trait("cum_slut"):
            return "cum_slut"
        if girl.has_trait("cute_sex"):
            return "cute"
        return "default"

    def _girl_esc_get_lines(girl, mode):
        """Get trait-aware request dialogue lines for escalation."""
        key = _girl_esc_pick_key(girl)
        if mode == "rub":
            pool = _GIRL_ESC_RUB_TO_TIP
        elif mode == "tip_to_anal":
            pool = _GIRL_ESC_TIP_TO_ANAL
            if getattr(girl, "_anal_preference", 0) >= 3 and "addicted" in pool:
                key = "addicted"
        else:
            pool = _GIRL_ESC_TIP_TO_SEX
        return pool.get(key, pool["default"])

    def _girl_esc_say_line(girl, line):
        """Her escalation line, translated: a "boyfriend" line talks about HER partner, so it goes through _cheat_line
        (a girlfriend: the words swapped in EN / PT / ES, the partner keys of the translation filled)."""
        if any(line in _p.get("boyfriend", ()) for _p in (_GIRL_ESC_RUB_TO_TIP, _GIRL_ESC_TIP_TO_SEX, _GIRL_ESC_TIP_TO_ANAL)):
            return _cheat_line(girl, line)
        return _tl(line)

    def _scene_position_switch(girl, from_pos, to_pos, anal=False):
        """Called when switching positions (or holes) mid-scene.
        "anal" is an ACT, not a position: to_pos == "anal" (or anal=True) counts the anal act.
        Any other target is vaginal, so it counts "sex" (once per scene, mark_intimacy dedupes):
        that is what makes an anal -> vaginal switch count as sex."""
        debug_log("[POS_SWITCH] %s: %s -> %s anal=%s phase=%s" % (girl.gid, from_pos, to_pos, anal, getattr(store, "_scene_phase", None)))
        if getattr(store, "_scene_phase", None) in _NON_PENETRATION_PHASES:
            pass   # still rubbing / just the tip: nothing to count but the position
        elif to_pos == "anal" or anal:
            mark_intimacy(girl, "anal")
        else:
            mark_intimacy(girl, "sex")
        if to_pos != "anal":
            mark_intimacy(girl, to_pos)

    # ============================================================
    # Favorite act system
    # ============================================================
    # ============================================================
    # Virginity loss
    # ============================================================
    def lose_virginity(girl, position=None):
        """
        Removes the virgin trait + flag and unlocks the full FavoriteAct pool.
        Call once when the girl has penetrative sex for the first time.
        Saves full context in girl.virginity_context for later reference.
        """
        debug_log("[DEBUG] lose_virginity() called for %s position=%s" % (girl.gid, position))
        girl.virginity_taken_by_player = True
        girl.remove_trait("virgin")
        girl.set_flag("virgin", False)
        girl.discover("discovered_virgin")
        Player.discover("took_virginity")

        _loc = getattr(store, "CurrentLocation", "room")
        _is_cheat = _is_on_cheat_path(girl) if callable(_is_on_cheat_path) else False
        _has_bf = girl.has_npc_partner() if hasattr(girl, "has_npc_partner") else False
        _dating_player = girl.is_dating_player() if hasattr(girl, "is_dating_player") else False
        girl.virginity_context = {
            "location": _loc,
            "position": position,
            "day": getattr(store, "Day", 1),
            "is_cheating": _is_cheat,
            "has_npc_partner": _has_bf,
            "is_dating_player": _dating_player,
            "is_public": getattr(store, "_crowd_level", 0) > 0,
            "was_recorded": getattr(store, "_recording_active", False),
            "condom": getattr(store, "condom_active", False),
            "scene_restricted": getattr(store, "_scene_restricted", False),
        }
        debug_log("[VIRGINITY] context saved: %s" % str(girl.virginity_context))

        store._lost_virginity_this_scene = True

        # Unlock all possible favorite acts (she now knows what sex is)
        all_acts = [a for a in _ORGASM_POSITION_KEYS if girl_has_pose(girl, _ACT_TO_POSE.get(a, a))]
        if not girl._favorite_act_unlocked:
            girl.FavoriteAct = renpy.random.choice(all_acts)
            girl._favorite_act_unlocked = True

    # ── Virginity knowledge helpers ──

    def girl_learns_virgin(learner, target):
        """Record that 'learner' now believes 'target' is a virgin.
        Only records if target currently HAS the virgin trait.
        Once virginity is lost, no new knowledge is propagated."""
        if learner.gid == target.gid:
            return
        # Only learn about CURRENT virgins — not girls who already lost it
        if not (hasattr(target, "has_trait") and target.has_trait("virgin")):
            return
        if not hasattr(learner, "knows_virgin"):
            learner.knows_virgin = {}
        if target.gid not in learner.knows_virgin:
            learner.knows_virgin[target.gid] = True

    def girl_thinks_virgin(learner, target):
        """Return True if 'learner' believes 'target' is/was a virgin."""
        if not hasattr(learner, "knows_virgin"):
            learner.knows_virgin = {}
            return False
        return learner.knows_virgin.get(target.gid, False)

    def sync_knowledge_by_friendship():
        """If two girls have friendship > 700, they share knowledge.
        Called once per day (e.g. from daily refresh)."""
        for g in ALL_GIRLS:
            _ensure_girl_knowledge(g)
            for other in ALL_GIRLS:
                if g.gid == other.gid:
                    continue
                friendship = g.Girl_like.get(other.gid, 0)
                if friendship > 700:
                    # Virginity
                    if other.has_trait("virgin"):
                        girl_learns_virgin(g, other)
                    # BF knowledge (friends know if each other has a boyfriend)
                    if hasattr(other, "has_npc_partner") and other.has_npc_partner():
                        girl_learns_has_bf(g, other)
                    # Lesbian knowledge (close friends know orientation)
                    if other.has_trait("lesbian"):
                        girl_learns_lesbian(g, other)

    # Keep old name as alias for compatibility
    sync_virginity_by_friendship = sync_knowledge_by_friendship

    def check_virgin_shock(viewer, vid_girl):
        """Return True if viewer thought vid_girl was a virgin but she's in a sex video.
        Also clears the belief (she now knows the truth)."""
        if not hasattr(viewer, "knows_virgin"):
            viewer.knows_virgin = {}
            return False
        if viewer.knows_virgin.get(vid_girl.gid, False):
            # She thought she was a virgin, but this video proves otherwise
            del viewer.knows_virgin[vid_girl.gid]
            return True
        return False

    # ============================================================
    # INTER-GIRL KNOWLEDGE SYSTEM
    # Tracks what girls know about each other from witnessing
    # acts, seeing videos, or through friendship/gossip.
    # ============================================================

    def _ensure_girl_knowledge(girl):
        """Initialize knowledge dicts if missing."""
        if not hasattr(girl, "knows_virgin"):
            girl.knows_virgin = {}
        if not hasattr(girl, "knows_acts"):
            girl.knows_acts = {}      # {gid: set("hj", "bj", ...)}
        if not hasattr(girl, "knows_cheating"):
            girl.knows_cheating = {}  # {gid: True}
        if not hasattr(girl, "knows_has_bf"):
            girl.knows_has_bf = {}    # {gid: True}
        if not hasattr(girl, "knows_with_player"):
            girl.knows_with_player = {}  # {gid: set("hj", "bj", ...)} - acts she knows target did WITH the player

    def girl_learns_act(learner, target, act, with_player=False):
        """Record that learner now knows target did a specific act.
        with_player=True means she knows it was with the player specifically."""
        if learner.gid == target.gid:
            return
        _ensure_girl_knowledge(learner)
        # `act` may be a video / witnessed scene type: a position she saw IS the "sex" act
        # ("doggy" video -> she knows "doggy" AND "sex"; "laying_anal" -> "anal"). Readers check the act.
        _learned = set((act, scene_type_act(act)))
        if target.gid not in learner.knows_acts:
            learner.knows_acts[target.gid] = set()
        learner.knows_acts[target.gid].update(_learned)
        # Also track if it was with the player
        if with_player:
            if target.gid not in learner.knows_with_player:
                learner.knows_with_player[target.gid] = set()
            learner.knows_with_player[target.gid].update(_learned)
        # If she sees penetration, she knows the virgin claim is gone
        if act == "creampie" or _learned & set(_SEX_PENETRATION_ACTS):
            if learner.knows_virgin.get(target.gid, False):
                del learner.knows_virgin[target.gid]

    def girl_learns_cheating(learner, cheater):
        """Record that learner saw cheater being unfaithful."""
        if learner.gid == cheater.gid:
            return
        _ensure_girl_knowledge(learner)
        learner.knows_cheating[cheater.gid] = True

    def girl_learns_has_bf(learner, target):
        """Record that learner now knows target has a boyfriend."""
        if learner.gid == target.gid:
            return
        _ensure_girl_knowledge(learner)
        learner.knows_has_bf[target.gid] = True

    def girl_learns_lesbian(learner, target):
        if not hasattr(target, "has_trait") or not target.has_trait("lesbian"):
            return
        if learner.gid == target.gid:
            return
        _ensure_girl_knowledge(learner)
        if not hasattr(learner, "knows_lesbian"):
            learner.knows_lesbian = {}
        learner.knows_lesbian[target.gid] = True

    def girl_knows_lesbian(knower, target):
        _kl = getattr(knower, "knows_lesbian", {})
        return _kl.get(target.gid, False)

    def check_lesbian_shock(viewer, vid_girl):
        if not hasattr(vid_girl, "has_trait") or not vid_girl.has_trait("lesbian"):
            return False
        if not girl_knows_lesbian(viewer, vid_girl):
            return False
        _key = "_lesbian_shock_%s" % vid_girl.gid
        if getattr(viewer, _key, False):
            return False
        setattr(viewer, _key, True)
        return True

    def girl_knows_act(learner, target, act=None):
        """Check if learner knows target did a specific act (or any act if act=None)."""
        _ensure_girl_knowledge(learner)
        acts = learner.knows_acts.get(target.gid, set())
        if act is None:
            return len(acts) > 0
        return act in acts

    def girl_knows_cheating(learner, target):
        """Check if learner knows target cheated."""
        _ensure_girl_knowledge(learner)
        return learner.knows_cheating.get(target.gid, False)

    def girl_knows_with_player(learner, target, act=None):
        """Check if learner knows target did acts with the player."""
        _ensure_girl_knowledge(learner)
        acts = learner.knows_with_player.get(target.gid, set())
        if act is None:
            return len(acts) > 0
        return act in acts

    def _update_anal_preference(girl):
        _ap = getattr(girl, "_anal_preference", 0)
        if girl.has_trait("anal_hater") or _ap >= 3:
            return
        anal_count = girl.Orgasms.get("anal", 0)
        _is_al = girl.has_trait("anal_lover")
        _thresholds = [(3, 1), (8, 2), (18, 3)] if _is_al else [(5, 1), (12, 2), (25, 3)]
        # An anal_lover still discovering it (trait_is_new: her first 3 anal scenes) stays "Curious" at most, a
        # first-timer never complains about the vaginal. Her orgasms keep counting: the stage catches up right after.
        _cap = 1 if _is_al and trait_is_new(girl, "anal_lover") else 3
        for req, stage in _thresholds:
            if anal_count >= req and _ap < stage:
                if stage > _cap:
                    print("[ANAL_PREF] %s: stage %d held at %d while she is still discovering anal (anal_orgasms=%d)" % (
                        girl.gid, stage, _cap, anal_count))
                    break
                girl._anal_preference = stage
                print("[ANAL_PREF] %s -> stage %d (anal_orgasms=%d)" % (girl.gid, stage, anal_count))

    def _update_favorite_act(girl):
        """
        Called after each orgasm. Two phases:
        1) Before unlock: keeps initial FavoriteAct until any act's orgasm
        count surpasses FavoriteActThreshold → that act becomes the new
        favorite and the system unlocks.
        2) After unlock: whichever act has the most orgasms is the favorite.
        Then updates anal preference and overrides FavoriteAct if stage >= 2.
        """
        orgasms = getattr(girl, "Orgasms", {})
        _valid_acts = [a for a in _ORGASM_POSITION_KEYS if girl_has_pose(girl, _ACT_TO_POSE.get(a, a))]

        if not girl._favorite_act_unlocked:
            for act in _valid_acts:
                if orgasms.get(act, 0) > girl.FavoriteActThreshold:
                    girl.FavoriteAct = act
                    girl._favorite_act_unlocked = True
                    _update_anal_preference(girl)
                    if getattr(girl, "_anal_preference", 0) >= 2:
                        girl.FavoriteAct = "anal"
                    return
        else:
            best_act = girl.FavoriteAct
            best_count = orgasms.get(best_act, 0)
            for act in _valid_acts:
                c = orgasms.get(act, 0)
                if c > best_count:
                    best_act = act
                    best_count = c
            girl.FavoriteAct = best_act

        _update_anal_preference(girl)
        if getattr(girl, "_anal_preference", 0) >= 2:
            girl.FavoriteAct = "anal"

    Girl.UpdateFavoriteAct = _update_favorite_act

    # ============================================================
    # Helpers – girl resolving / expressions / clothing
    # ============================================================

    def _resolve_girl(girl_or_id):
        if isinstance(girl_or_id, Girl):
            return girl_or_id
        return GIRL_BY_ID.get(girl_or_id)

    # ------------------------------------------------------------
    # Expression presets (head/face)
    # ------------------------------------------------------------
    # Per-girl per-pose expression overrides (checked before POSE_EXPRESSIONS)
    # Key: girl_id -> pose -> expression_name -> {eyes, mouth, brows}
    GIRL_POSE_EXPRESSIONS = {
        "gwen": {
            # ── STANDING ──
            "standing": {
                "happy":     {"eyes": "eyes_normal",    "mouth": "mouth_laugh",      "brows": "brows_normal"},
                "kissing":   {"eyes": "eyes_squint",    "mouth": "mouth_kissing",    "brows": "brows_normal"},
                "scared":    {"eyes": "eyes_surprised", "mouth": "mouth_surprised",  "brows": "brows_normal"},
                "angry":     {"eyes": "eyes_normal",    "mouth": "mouth_serious",    "brows": "brows_surprised"},
                "sad":       {"eyes": "eyes_normal",    "mouth": "mouth_serious",    "brows": "brows_confused"},
                "surprised": {"eyes": "eyes_surprised", "mouth": "mouth_surprised",  "brows": "brows_normal"},
                "normal":    {"eyes": "eyes_normal",    "mouth": "mouth_normal",     "brows": "brows_normal"},
                "sexy":      {"eyes": "eyes_normal",    "mouth": "mouth_smile",      "brows": "brows_normal"},
            },
            # ── HANDJOB ──
            "handjob": {
                "happy":     {"eyes": "eyes_normal",    "mouth": "mouth_laugh",      "brows": "brows_normal"},
                "kissing":   {"eyes": "eyes_closed",    "mouth": "mouth_smile",      "brows": "brows_normal"},
                "scared":    {"eyes": "eyes_surprised", "mouth": "mouth_surprised",  "brows": "brows_normal"},
                "angry":     {"eyes": "eyes_normal",    "mouth": "mouth_serious",    "brows": "brows_surprised"},
                "sad":       {"eyes": "eyes_normal",    "mouth": "mouth_serious",    "brows": "brows_sad"},
                "surprised": {"eyes": "eyes_surprised", "mouth": "mouth_surprised",  "brows": "brows_normal"},
                "normal":    {"eyes": "eyes_normal",    "mouth": "mouth_normal",     "brows": "brows_normal"},
                "sexy":      {"eyes": "eyes_normal",    "mouth": "mouth_smile",      "brows": "brows_normal"},
                "cumming":   {"eyes": "eyes_closed",    "mouth": "mouth_tongue",     "brows": "brows_sad"},
            },
            # ── BLOWJOB ──
            "blowjob": {
                "happy":     {"eyes": "eyes_normal",      "mouth": "mouth_happy",      "brows": "brows_normal"},
                "kissing":   {"eyes": "eyes_closed_happy","mouth": "mouth_lipbite",    "brows": "brows_normal"},
                "scared":    {"eyes": "eyes_surprised",   "mouth": "mouth_scared",     "brows": "brows_normal"},
                "angry":     {"eyes": "eyes_normal",      "mouth": "mouth_angry",      "brows": "brows_surprised"},
                "sad":       {"eyes": "eyes_normal",      "mouth": "mouth_sad",        "brows": "brows_normal"},
                "surprised": {"eyes": "eyes_surprised",   "mouth": "mouth_surprised",  "brows": "brows_normal"},
                "normal":    {"eyes": "eyes_normal",      "mouth": "mouth_tongue",     "brows": "brows_normal"},
                "sexy":      {"eyes": "eyes_normal",      "mouth": "mouth_lipbite",    "brows": "brows_normal"},
                "cumming":   {"eyes": "eyes_closed_happy","mouth": "mouth_tongue",     "brows": "brows_normal"},
                "ahegao":    {"eyes": "eyes_ahegao",      "mouth": "mouth_tongue",     "brows": "brows_normal"},
                "ahegao_2":  {"eyes": "eyes_ahegao_2",    "mouth": "mouth_tongue",     "brows": "brows_normal"},
            },
            # ── TITJOB ──
            "titjob": {
                "happy":     {"eyes": "eyes_normal",    "mouth": "mouth_laugh",      "brows": "brows_normal"},
                "kissing":   {"eyes": "eyes_closed",    "mouth": "mouth_kiss",       "brows": "brows_normal"},
                "scared":    {"eyes": "eyes_squint",    "mouth": "mouth_surprised",  "brows": "brows_confused"},
                "angry":     {"eyes": "eyes_normal",    "mouth": "mouth_sad",        "brows": "brows_challenging"},
                "sad":       {"eyes": "eyes_normal",    "mouth": "mouth_sad",        "brows": "brows_sad"},
                "surprised": {"eyes": "eyes_sexy",      "mouth": "mouth_surprised",  "brows": "brows_normal"},
                "normal":    {"eyes": "eyes_normal",    "mouth": "mouth_normal",     "brows": "brows_normal"},
                "sexy":      {"eyes": "eyes_sexy",      "mouth": "mouth_lipbite",    "brows": "brows_normal"},
                "cumming":   {"eyes": "eyes_closed",    "mouth": "mouth_ahegao",     "brows": "brows_sad"},
                "ahegao":    {"eyes": "eyes_squint",    "mouth": "mouth_ahegao",     "brows": "brows_sad"},
                "ahegao_2":  {"eyes": "eyes_closed",    "mouth": "mouth_ahegao",     "brows": "brows_sad"},
            },
            # ── RCG ──
            "reverse_cowgirl": {
                "happy":     {"eyes": "eyes_normal",        "mouth": "mouth_smile",      "brows": "brows_normal"},
                "kissing":   {"eyes": "eyes_closed",        "mouth": "mouth_kiss",       "brows": "brows_normal"},
                "scared":    {"eyes": "eyes_surprised",     "mouth": "mouth_scared",     "brows": "brows_surprised"},
                "angry":     {"eyes": "eyes_looking_to_player", "mouth": "mouth_scared", "brows": "brows_surprised"},
                "sad":       {"eyes": "eyes_normal",        "mouth": "mouth_serious",    "brows": "brows_sad"},
                "surprised": {"eyes": "eyes_surprised",     "mouth": "mouth_surprised",  "brows": "brows_surprised"},
                "normal":    {"eyes": "eyes_normal",        "mouth": "mouth_normal",     "brows": "brows_normal"},
                "sexy":      {"eyes": "eyes_looking_to_player", "mouth": "mouth_lipbite","brows": "brows_horny"},
                "cumming":   {"eyes": "eyes_closed",        "mouth": "mouth_tongue",     "brows": "brows_horny"},
                "ahegao":    {"eyes": "eyes_surprised",     "mouth": "mouth_tongue",     "brows": "brows_up"},
                "ahegao_2":  {"eyes": "eyes_squint_2",      "mouth": "mouth_tongue",     "brows": "brows_up"},
                "moaning":   {"eyes": "eyes_squint",        "mouth": "mouth_surprised",  "brows": "brows_horny"},
                "pleasure":  {"eyes": "eyes_looking_up",    "mouth": "mouth_tongue",     "brows": "brows_horny"},
            },
            # ── COWGIRL ──
            "cowgirl": {
                "happy":     {"eyes": "eyes_normal",    "mouth": "mouth_smile",      "brows": "brows_normal"},
                "kissing":   {"eyes": "eyes_closed",    "mouth": "mouth_smile",      "brows": "brows_normal"},
                "scared":    {"eyes": "eyes_surprised", "mouth": "mouth_surprised",  "brows": "brows_surprised"},
                "angry":     {"eyes": "eyes_squint",    "mouth": "mouth_serious",    "brows": "brows_surprised"},
                "sad":       {"eyes": "eyes_normal",    "mouth": "mouth_serious",    "brows": "brows_confused"},
                "surprised": {"eyes": "eyes_surprised", "mouth": "mouth_surprised",  "brows": "brows_normal"},
                "normal":    {"eyes": "eyes_normal",    "mouth": "mouth_normal",     "brows": "brows_normal"},
                "sexy":      {"eyes": "eyes_normal",    "mouth": "mouth_tongue",     "brows": "brows_horny"},
                "cumming":   {"eyes": "eyes_closed",    "mouth": "mouth_tongue",     "brows": "brows_horny"},
                "ahegao":    {"eyes": "eyes_surprised", "mouth": "mouth_tongue",     "brows": "brows_horny"},
                "ahegao_2":  {"eyes": "eyes_squint_big","mouth": "mouth_tongue",     "brows": "brows_horny"},
                "moaning":   {"eyes": "eyes_squint",    "mouth": "mouth_surprised",  "brows": "brows_horny"},
            },
            # ── DOGGY ──
            "doggy": {
                "happy":     {"eyes": "eyes_looking_to_player", "mouth": "mouth_smile",     "brows": "brows_normal"},
                "kissing":   {"eyes": "eyes_closed",            "mouth": "mouth_kiss",      "brows": "brows_normal"},
                "scared":    {"eyes": "eyes_looking_to_player", "mouth": "mouth_scared",    "brows": "brows_surprised"},
                "angry":     {"eyes": "eyes_squint",            "mouth": "mouth_serious",   "brows": "brows_confused"},
                "sad":       {"eyes": "eyes_squint",            "mouth": "mouth_scared",    "brows": "brows_sad"},
                "surprised": {"eyes": "eyes_looking_to_player", "mouth": "mouth_surprised", "brows": "brows_surprised"},
                "normal":    {"eyes": "eyes_normal",            "mouth": "mouth_normal",    "brows": "brows_normal"},
                "sexy":      {"eyes": "eyes_looking_to_player", "mouth": "mouth_lipbite",   "brows": "brows_horny"},
                "cumming":   {"eyes": "eyes_closed",            "mouth": "mouth_tongue",    "brows": "brows_horny"},
                "ahegao":    {"eyes": "eyes_surprised",         "mouth": "mouth_tongue",    "brows": "brows_surprised"},
                "ahegao_2":  {"eyes": "eyes_squint",            "mouth": "mouth_tongue",    "brows": "brows_horny"},
                "moaning":   {"eyes": "eyes_squint",            "mouth": "mouth_surprised", "brows": "brows_horny"},
                "pleasure":  {"eyes": "eyes_looking_up",        "mouth": "mouth_tongue",    "brows": "brows_horny"},
            },
        },

        "tenny": {
            "standing": {
                "happy":     {"eyes": "eyes_normal",    "mouth": "mouth_laugh",      "brows": "brows_normal"},
                "kissing":   {"eyes": "eyes_squint",    "mouth": "mouth_kissing",    "brows": "brows_normal"},
                "scared":    {"eyes": "eyes_surprised", "mouth": "mouth_surprised",  "brows": "brows_normal"},
                "angry":     {"eyes": "eyes_normal",    "mouth": "mouth_serious",    "brows": "brows_surprised"},
                "sad":       {"eyes": "eyes_normal",    "mouth": "mouth_serious",    "brows": "brows_confused"},
                "surprised": {"eyes": "eyes_surprised", "mouth": "mouth_surprised",  "brows": "brows_normal"},
                "normal":    {"eyes": "eyes_normal",    "mouth": "mouth_normal",     "brows": "brows_normal"},
                "sexy":      {"eyes": "eyes_normal",    "mouth": "mouth_smile",      "brows": "brows_normal"},
            },
            "handjob": {
                "happy":     {"eyes": "eyes_normal",       "mouth": "mouth_laugh",      "brows": "brows_normal"},
                "kissing":   {"eyes": "eyes_closed_happy", "mouth": "mouth_lipbite",    "brows": "brows_normal"},
                "scared":    {"eyes": "eyes_surprised",    "mouth": "mouth_surprised",  "brows": "brows_surprised"},
                "angry":     {"eyes": "eyes_squint",       "mouth": "mouth_serious",    "brows": "brows_surprised"},
                "sad":       {"eyes": "eyes_side",         "mouth": "mouth_sad",        "brows": "brows_sad"},
                "surprised": {"eyes": "eyes_surprised",    "mouth": "mouth_surprised",  "brows": "brows_normal"},
                "normal":    {"eyes": "eyes_normal",       "mouth": "mouth_normal",     "brows": "brows_normal"},
                "sexy":      {"eyes": "eyes_squint",       "mouth": "mouth_smile",      "brows": "brows_normal"},
                "cumming":   {"eyes": "eyes_closed",       "mouth": "mouth_tongue",     "brows": "brows_sad"},
            },
            "blowjob": {
                "happy":     {"eyes": "eyes_normal",       "mouth": "mouth_happy",      "brows": "brows_normal"},
                "kissing":   {"eyes": "eyes_closed_happy", "mouth": "mouth_lipbite",    "brows": "brows_normal"},
                "scared":    {"eyes": "eyes_surprised",    "mouth": "mouth_scared",     "brows": "brows_scared"},
                "angry":     {"eyes": "eyes_normal",       "mouth": "mouth_angry",      "brows": "brows_angry"},
                "sad":       {"eyes": "eyes_looking_down", "mouth": "mouth_sad",        "brows": "brows_sad"},
                "surprised": {"eyes": "eyes_surprised",    "mouth": "mouth_surprised",  "brows": "brows_confused"},
                "normal":    {"eyes": "eyes_normal",       "mouth": "mouth_tongue",     "brows": "brows_normal"},
                "sexy":      {"eyes": "eyes_squint",       "mouth": "mouth_lipbite",    "brows": "brows_normal"},
                "cumming":   {"eyes": "eyes_closed_happy", "mouth": "mouth_tongue",     "brows": "brows_sad"},
                "ahegao":    {"eyes": "eyes_ahegao",       "mouth": "mouth_tongue",     "brows": "brows_confused"},
                "ahegao_2":  {"eyes": "eyes_ahegao_2",     "mouth": "mouth_tongue",     "brows": "brows_sad"},
            },
        },

        "rogue": {
            # -- STANDING --
            "standing": {
                "happy":     {"eyes": "eyes_normal",      "mouth": "mouth_laugh",      "brows": "brows_normal"},
                "kissing":   {"eyes": "eyes_closed",      "mouth": "mouth_kissing",    "brows": "brows_normal"},
                "scared":    {"eyes": "eyes_surprised",   "mouth": "mouth_surprised",  "brows": "brows_surprised"},
                "angry":     {"eyes": "eyes_side_squint", "mouth": "mouth_serious",    "brows": "brows_surprised"},
                "sad":       {"eyes": "eyes_side",        "mouth": "mouth_sad",        "brows": "brows_sad"},
                "surprised": {"eyes": "eyes_surprised",   "mouth": "mouth_surprised",  "brows": "brows_surprised"},
                "normal":    {"eyes": "eyes_normal",      "mouth": "mouth_normal",     "brows": "brows_normal"},
                "sexy":      {"eyes": "eyes_side",        "mouth": "mouth_smile",      "brows": "brows_normal"},
                "sly":       {"eyes": "eyes_sexy",       "mouth": "mouth_smile",      "brows": "brows_normal"},
                "confused":  {"eyes": "eyes_side",       "mouth": "mouth_serious",    "brows": "brows_confused"},
                "embarrassed": {"eyes": "eyes_side",     "mouth": "mouth_sad",        "brows": "brows_confused"},
                "lusty":     {"eyes": "eyes_sexy",       "mouth": "mouth_smile",      "brows": "brows_normal"},
                "smirk":     {"eyes": "eyes_side_squint","mouth": "mouth_smile",      "brows": "brows_normal"},
                "startled":  {"eyes": "eyes_surprised",  "mouth": "mouth_surprised",  "brows": "brows_surprised"},
                "worried":   {"eyes": "eyes_side",       "mouth": "mouth_serious",    "brows": "brows_sad"},
                "grimace":   {"eyes": "eyes_normal",     "mouth": "mouth_serious",    "brows": "brows_normal"},
            },
            # -- HANDJOB --
            "handjob": {
                "happy":     {"eyes": "eyes_normal",    "mouth": "mouth_smile",      "brows": "brows_normal"},
                "kissing":   {"eyes": "eyes_closed",    "mouth": "mouth_smile",      "brows": "brows_normal"},
                "scared":    {"eyes": "eyes_surprised", "mouth": "mouth_surprised",  "brows": "brows_surprised"},
                "angry":     {"eyes": "eyes_squint",    "mouth": "mouth_serious",    "brows": "brows_surprised"},
                "sad":       {"eyes": "eyes_normal",    "mouth": "mouth_sad",        "brows": "brows_sad"},
                "surprised": {"eyes": "eyes_surprised", "mouth": "mouth_surprised",  "brows": "brows_normal"},
                "normal":    {"eyes": "eyes_normal",    "mouth": "mouth_normal",     "brows": "brows_normal"},
                "sexy":      {"eyes": "eyes_squint",    "mouth": "mouth_smile",      "brows": "brows_normal"},
                "cumming":   {"eyes": "eyes_closed",    "mouth": "mouth_tongue",     "brows": "brows_sad"},
            },
            # -- BLOWJOB --
            "blowjob": {
                "happy":     {"eyes": "eyes_normal",    "mouth": "mouth_happy",      "brows": "brows_normal"},
                "kissing":   {"eyes": "eyes_squint_2",  "mouth": "mouth_lipbite",    "brows": "brows_normal"},
                "scared":    {"eyes": "eyes_normal",    "mouth": "mouth_surprised",  "brows": "brows_sad"},
                "angry":     {"eyes": "eyes_normal",    "mouth": "mouth_angry",      "brows": "brows_surprised"},
                "sad":       {"eyes": "eyes_normal",    "mouth": "mouth_sad",        "brows": "brows_normal"},
                "surprised": {"eyes": "eyes_normal",    "mouth": "mouth_surprised",  "brows": "brows_surprised"},
                "normal":    {"eyes": "eyes_normal",    "mouth": "mouth_tongue",     "brows": "brows_normal"},
                "sexy":      {"eyes": "eyes_squint",    "mouth": "mouth_lipbite",    "brows": "brows_normal"},
                "cumming":   {"eyes": "eyes_squint_2",  "mouth": "mouth_tongue",     "brows": "brows_normal"},
                "ahegao":    {"eyes": "eyes_squint_2",  "mouth": "mouth_tongue",     "brows": "brows_surprised"},
                "ahegao_2":  {"eyes": "eyes_squint",    "mouth": "mouth_tongue",     "brows": "brows_surprised"},
            },
            # -- TITJOB --
            "titjob": {
                "happy":     {"eyes": "eyes_normal",    "mouth": "mouth_laugh",      "brows": "brows_normal"},
                "kissing":   {"eyes": "eyes_closed",    "mouth": "mouth_kiss",       "brows": "brows_normal"},
                "scared":    {"eyes": "eyes_squint",    "mouth": "mouth_surprised",  "brows": "brows_confused"},
                "angry":     {"eyes": "eyes_normal",    "mouth": "mouth_sad",        "brows": "brows_challenging"},
                "sad":       {"eyes": "eyes_normal",    "mouth": "mouth_sad",        "brows": "brows_sad"},
                "surprised": {"eyes": "eyes_sexy",      "mouth": "mouth_surprised",  "brows": "brows_normal"},
                "normal":    {"eyes": "eyes_normal",    "mouth": "mouth_normal",     "brows": "brows_normal"},
                "sexy":      {"eyes": "eyes_sexy",      "mouth": "mouth_lipbite",    "brows": "brows_normal"},
                "cumming":   {"eyes": "eyes_closed",    "mouth": "mouth_ahegao",     "brows": "brows_sad"},
                "ahegao":    {"eyes": "eyes_squint",    "mouth": "mouth_ahegao",     "brows": "brows_sad"},
                "ahegao_2":  {"eyes": "eyes_closed",    "mouth": "mouth_ahegao",     "brows": "brows_sad"},
            },
            # -- RCG --
            "reverse_cowgirl": {
                "happy":     {"eyes": "eyes_normal",        "mouth": "mouth_smile",      "brows": "brows_normal"},
                "kissing":   {"eyes": "eyes_closed",        "mouth": "mouth_kiss",       "brows": "brows_normal"},
                "scared":    {"eyes": "eyes_surprised",     "mouth": "mouth_scared",     "brows": "brows_surprised"},
                "angry":     {"eyes": "eyes_looking_to_player", "mouth": "mouth_scared", "brows": "brows_surprised"},
                "sad":       {"eyes": "eyes_normal",        "mouth": "mouth_serious",    "brows": "brows_normal"},
                "surprised": {"eyes": "eyes_surprised",     "mouth": "mouth_surprised",  "brows": "brows_surprised"},
                "normal":    {"eyes": "eyes_normal",        "mouth": "mouth_normal",     "brows": "brows_normal"},
                "sexy":      {"eyes": "eyes_looking_to_player", "mouth": "mouth_lipbite","brows": "brows_horny"},
                "cumming":   {"eyes": "eyes_closed",        "mouth": "mouth_tongue",     "brows": "brows_horny"},
                "ahegao":    {"eyes": "eyes_surprised",     "mouth": "mouth_tongue",     "brows": "brows_up"},
                "ahegao_2":  {"eyes": "eyes_squint_2",      "mouth": "mouth_tongue",     "brows": "brows_up"},
                "moaning":   {"eyes": "eyes_squint",        "mouth": "mouth_surprised",  "brows": "brows_horny"},
                "pleasure":  {"eyes": "eyes_looking_up",    "mouth": "mouth_tongue",     "brows": "brows_horny"},
            },
            # -- COWGIRL --
            "cowgirl": {
                "happy":     {"eyes": "eyes_normal",    "mouth": "mouth_smile",      "brows": "brows_normal"},
                "kissing":   {"eyes": "eyes_closed",    "mouth": "mouth_smile",      "brows": "brows_normal"},
                "scared":    {"eyes": "eyes_surprised", "mouth": "mouth_surprised",  "brows": "brows_surprised"},
                "angry":     {"eyes": "eyes_squint",    "mouth": "mouth_serious",    "brows": "brows_surprised"},
                "sad":       {"eyes": "eyes_normal",    "mouth": "mouth_serious",    "brows": "brows_confused"},
                "surprised": {"eyes": "eyes_surprised", "mouth": "mouth_surprised",  "brows": "brows_normal"},
                "normal":    {"eyes": "eyes_normal",    "mouth": "mouth_normal",     "brows": "brows_normal"},
                "sexy":      {"eyes": "eyes_normal",    "mouth": "mouth_tongue",     "brows": "brows_horny"},
                "cumming":   {"eyes": "eyes_closed",    "mouth": "mouth_tongue",     "brows": "brows_horny"},
                "ahegao":    {"eyes": "eyes_surprised", "mouth": "mouth_tongue",     "brows": "brows_horny"},
                "ahegao_2":  {"eyes": "eyes_squint_big","mouth": "mouth_tongue",     "brows": "brows_horny"},
                "moaning":   {"eyes": "eyes_squint",    "mouth": "mouth_surprised",  "brows": "brows_horny"},
            },
            # -- DOGGY --
            "doggy": {
                "happy":     {"eyes": "eyes_looking_to_player", "mouth": "mouth_smile",     "brows": "brows_normal"},
                "kissing":   {"eyes": "eyes_closed",            "mouth": "mouth_kiss",      "brows": "brows_normal"},
                "scared":    {"eyes": "eyes_looking_to_player", "mouth": "mouth_scared",    "brows": "brows_surprised"},
                "angry":     {"eyes": "eyes_squint",            "mouth": "mouth_serious",   "brows": "brows_confused"},
                "sad":       {"eyes": "eyes_squint",            "mouth": "mouth_scared",    "brows": "brows_sad"},
                "surprised": {"eyes": "eyes_looking_to_player", "mouth": "mouth_surprised", "brows": "brows_surprised"},
                "normal":    {"eyes": "eyes_normal",            "mouth": "mouth_normal",    "brows": "brows_normal"},
                "sexy":      {"eyes": "eyes_looking_to_player", "mouth": "mouth_lipbite",   "brows": "brows_horny"},
                "cumming":   {"eyes": "eyes_closed",            "mouth": "mouth_tongue",    "brows": "brows_horny"},
                "ahegao":    {"eyes": "eyes_surprised",         "mouth": "mouth_tongue",    "brows": "brows_surprised"},
                "ahegao_2":  {"eyes": "eyes_squint",            "mouth": "mouth_tongue",    "brows": "brows_horny"},
                "moaning":   {"eyes": "eyes_squint",            "mouth": "mouth_surprised", "brows": "brows_horny"},
                "pleasure":  {"eyes": "eyes_looking_up",        "mouth": "mouth_tongue",    "brows": "brows_horny"},
            },
        },

        "ntw": {
            # -- STANDING --
            "standing": {
                "happy":     {"eyes": "eyes_normal",      "mouth": "mouth_laugh",      "brows": "brows_normal"},
                "kissing":   {"eyes": "eyes_closed_happy", "mouth": "mouth_kissing",   "brows": "brows_normal"},
                "scared":    {"eyes": "eyes_scared",       "mouth": "mouth_surprised",  "brows": "brows_surprised"},
                "angry":     {"eyes": "eyes_side_squint",  "mouth": "mouth_sad",        "brows": "brows_surprised"},
                "sad":       {"eyes": "eyes_looking_down", "mouth": "mouth_sad",        "brows": "brows_sad"},
                "surprised": {"eyes": "eyes_surprised",    "mouth": "mouth_surprised",  "brows": "brows_surprised"},
                "normal":    {"eyes": "eyes_normal",       "mouth": "mouth_normal",     "brows": "brows_normal"},
                "sexy":      {"eyes": "eyes_squint",       "mouth": "mouth_lipbite",    "brows": "brows_normal"},
                "smile":     {"eyes": "eyes_normal",       "mouth": "mouth_laugh",      "brows": "brows_normal"},
                "sly":       {"eyes": "eyes_squint",       "mouth": "mouth_lipbite",    "brows": "brows_normal"},
                "confused":  {"eyes": "eyes_normal",       "mouth": "mouth_sad",        "brows": "brows_confused"},
                "embarrassed": {"eyes": "eyes_side",       "mouth": "mouth_laugh",      "brows": "brows_confused"},
                "smirk":     {"eyes": "eyes_normal",       "mouth": "mouth_lipbite",    "brows": "brows_confused"},
                "startled":  {"eyes": "eyes_surprised",    "mouth": "mouth_surprised",  "brows": "brows_surprised"},
                "worried":   {"eyes": "eyes_side",         "mouth": "mouth_sad",        "brows": "brows_sad"},
                "grimace":   {"eyes": "eyes_normal",       "mouth": "mouth_sad",        "brows": "brows_normal"},
            },
            # -- HANDJOB --
            "handjob": {
                "happy":     {"eyes": "eyes_normal",    "mouth": "mouth_laugh",      "brows": "brows_normal"},
                "kissing":   {"eyes": "eyes_closed",    "mouth": "mouth_smile",      "brows": "brows_normal"},
                "scared":    {"eyes": "eyes_surprised", "mouth": "mouth_surprised",  "brows": "brows_surprised"},
                "angry":     {"eyes": "eyes_normal",    "mouth": "mouth_sad",        "brows": "brows_surprised"},
                "sad":       {"eyes": "eyes_normal",    "mouth": "mouth_sad",        "brows": "brows_sad"},
                "surprised": {"eyes": "eyes_surprised", "mouth": "mouth_surprised",  "brows": "brows_normal"},
                "normal":    {"eyes": "eyes_normal",    "mouth": "mouth_normal",     "brows": "brows_normal"},
                "sexy":      {"eyes": "eyes_squint",    "mouth": "mouth_smile",      "brows": "brows_normal"},
                "cumming":   {"eyes": "eyes_closed",    "mouth": "mouth_tongue",     "brows": "brows_sad"},
                "looking_down": {"eyes": "eyes_looking_down","mouth": "mouth_normal", "brows": "brows_normal"},
            },
            # -- TITJOB --
            "titjob": {
                "happy":     {"eyes": "eyes_normal",    "mouth": "mouth_laugh",      "brows": "brows_normal"},
                "kissing":   {"eyes": "eyes_closed",    "mouth": "mouth_kiss",       "brows": "brows_normal"},
                "scared":    {"eyes": "eyes_squint",    "mouth": "mouth_surprised",  "brows": "brows_confused"},
                "angry":     {"eyes": "eyes_normal",    "mouth": "mouth_sad",        "brows": "brows_surprised"},
                "sad":       {"eyes": "eyes_normal",    "mouth": "mouth_sad",        "brows": "brows_sad"},
                "surprised": {"eyes": "eyes_normal",    "mouth": "mouth_surprised",  "brows": "brows_normal"},
                "normal":    {"eyes": "eyes_normal",    "mouth": "mouth_normal",     "brows": "brows_normal"},
                "sexy":      {"eyes": "eyes_squint",    "mouth": "mouth_lipbite",    "brows": "brows_normal"},
                "cumming":   {"eyes": "eyes_closed",    "mouth": "mouth_tongue",     "brows": "brows_sad"},
                "ahegao":    {"eyes": "eyes_squint",    "mouth": "mouth_tongue",     "brows": "brows_sad"},
                "ahegao_2":  {"eyes": "eyes_closed",    "mouth": "mouth_tongue",     "brows": "brows_sad"},
            },
            # -- BLOWJOB --
            "blowjob": {
                "happy":     {"eyes": "eyes_normal",    "mouth": "mouth_happy",      "brows": "brows_normal"},
                "kissing":   {"eyes": "eyes_closed_happy","mouth": "mouth_lipbite",  "brows": "brows_normal"},
                "scared":    {"eyes": "eyes_surprised", "mouth": "mouth_scared",     "brows": "brows_surprised"},
                "angry":     {"eyes": "eyes_squint",    "mouth": "mouth_angry",      "brows": "brows_surprised"},
                "sad":       {"eyes": "eyes_normal",    "mouth": "mouth_sad",        "brows": "brows_sad"},
                "surprised": {"eyes": "eyes_surprised", "mouth": "mouth_surprised",  "brows": "brows_surprised"},
                "normal":    {"eyes": "eyes_normal",    "mouth": "mouth_tongue",     "brows": "brows_normal"},
                "sexy":      {"eyes": "eyes_squint",    "mouth": "mouth_lipbite",    "brows": "brows_normal"},
                "cumming":   {"eyes": "eyes_closed_happy","mouth": "mouth_tongue",   "brows": "brows_normal"},
                "looking_down": {"eyes": "eyes_looking_down","mouth": "mouth_smile",  "brows": "brows_normal"},
            },
            # -- COWGIRL --
            "cowgirl": {
                "happy":     {"eyes": "eyes_normal",    "mouth": "mouth_smile",      "brows": "brows_normal"},
                "kissing":   {"eyes": "eyes_closed",    "mouth": "mouth_kissing",    "brows": "brows_normal"},
                "scared":    {"eyes": "eyes_surprised", "mouth": "mouth_surprised",  "brows": "brows_surprised"},
                "angry":     {"eyes": "eyes_squint",    "mouth": "mouth_serious",    "brows": "brows_surprised"},
                "sad":       {"eyes": "eyes_normal",    "mouth": "mouth_serious",    "brows": "brows_confused"},
                "surprised": {"eyes": "eyes_surprised", "mouth": "mouth_surprised",  "brows": "brows_surprised"},
                "normal":    {"eyes": "eyes_normal",    "mouth": "mouth_normal",     "brows": "brows_normal"},
                "sexy":      {"eyes": "eyes_normal",    "mouth": "mouth_tongue",     "brows": "brows_horny"},
                "cumming":   {"eyes": "eyes_closed",    "mouth": "mouth_tongue",     "brows": "brows_horny"},
                "ahegao":    {"eyes": "eyes_ahegao",   "mouth": "mouth_tongue",     "brows": "brows_horny"},
                "ahegao_2":  {"eyes": "eyes_ahegao_2", "mouth": "mouth_tongue",     "brows": "brows_horny"},
                "moaning":   {"eyes": "eyes_squint",    "mouth": "mouth_surprised",  "brows": "brows_horny"},
            },
            # -- RCG --
            "reverse_cowgirl": {
                "happy":     {"eyes": "eyes_looking_to_player", "mouth": "mouth_smile",     "brows": "brows_normal"},
                "kissing":   {"eyes": "eyes_closed",            "mouth": "mouth_kiss",      "brows": "brows_normal"},
                "scared":    {"eyes": "eyes_surprised",         "mouth": "mouth_scared",    "brows": "brows_surprised"},
                "angry":     {"eyes": "eyes_looking_to_player", "mouth": "mouth_scared",    "brows": "brows_surprised"},
                "sad":       {"eyes": "eyes_normal",            "mouth": "mouth_serious",   "brows": "brows_sad"},
                "surprised": {"eyes": "eyes_surprised",         "mouth": "mouth_surprised", "brows": "brows_surprised"},
                "normal":    {"eyes": "eyes_normal",            "mouth": "mouth_normal",    "brows": "brows_normal"},
                "sexy":      {"eyes": "eyes_looking_to_player", "mouth": "mouth_lipbite",   "brows": "brows_horny"},
                "cumming":   {"eyes": "eyes_closed",            "mouth": "mouth_tongue",    "brows": "brows_horny"},
                "ahegao":    {"eyes": "eyes_surprised",         "mouth": "mouth_tongue",    "brows": "brows_surprised"},
                "ahegao_2":  {"eyes": "eyes_squint_2",          "mouth": "mouth_tongue",    "brows": "brows_surprised"},
                "moaning":   {"eyes": "eyes_squint",            "mouth": "mouth_surprised", "brows": "brows_horny"},
                "pleasure":  {"eyes": "eyes_looking_up",        "mouth": "mouth_tongue",    "brows": "brows_horny"},
            },
            # -- DOGGY --
            "doggy": {
                "happy":     {"eyes": "eyes_looking_to_player", "mouth": "mouth_smile",     "brows": "brows_normal"},
                "kissing":   {"eyes": "eyes_closed",            "mouth": "mouth_kiss",      "brows": "brows_normal"},
                "scared":    {"eyes": "eyes_looking_to_player", "mouth": "mouth_scared",    "brows": "brows_surprised"},
                "angry":     {"eyes": "eyes_squint",            "mouth": "mouth_serious",   "brows": "brows_confused"},
                "sad":       {"eyes": "eyes_squint",            "mouth": "mouth_scared",    "brows": "brows_sad"},
                "surprised": {"eyes": "eyes_looking_to_player", "mouth": "mouth_surprised", "brows": "brows_surprised"},
                "normal":    {"eyes": "eyes_normal",            "mouth": "mouth_normal",    "brows": "brows_normal"},
                "sexy":      {"eyes": "eyes_looking_to_player", "mouth": "mouth_lipbite",   "brows": "brows_horny"},
                "cumming":   {"eyes": "eyes_closed",            "mouth": "mouth_tongue",    "brows": "brows_horny"},
                "ahegao":    {"eyes": "eyes_surprised",         "mouth": "mouth_tongue",    "brows": "brows_surprised"},
                "ahegao_2":  {"eyes": "eyes_squint",            "mouth": "mouth_tongue",    "brows": "brows_horny"},
                "moaning":   {"eyes": "eyes_squint",            "mouth": "mouth_surprised", "brows": "brows_horny"},
                "pleasure":  {"eyes": "eyes_looking_up",        "mouth": "mouth_tongue",    "brows": "brows_horny"},
            },
        },

        "shion": {
            # -- STANDING --
            "standing": {
                "happy":     {"eyes": "eyes_normal",       "mouth": "mouth_laugh",     "brows": "brows_normal"},
                "kissing":   {"eyes": "eyes_closed",       "mouth": "mouth_kissing",   "brows": "brows_normal"},
                "scared":    {"eyes": "eyes_scared",       "mouth": "mouth_surprised", "brows": "brows_surprised"},
                "angry":     {"eyes": "eyes_squint",       "mouth": "mouth_open_teeth", "brows": "brows_angry"},
                "sad":       {"eyes": "eyes_side",         "mouth": "mouth_sad",       "brows": "brows_sad"},
                "surprised": {"eyes": "eyes_surprised",    "mouth": "mouth_surprised", "brows": "brows_surprised"},
                "normal":    {"eyes": "eyes_normal",       "mouth": "mouth_normal",    "brows": "brows_normal"},
                "sexy":      {"eyes": "eyes_sexy",         "mouth": "mouth_lipbite",   "brows": "brows_normal"},
                # her own faces (docs/plan_shion.md Fase 2 item 9): her "serious" / "disgusted" mouth is the sad one
                "smirk":       {"eyes": "eyes_sexy",         "mouth": "mouth_smile",   "brows": "brows_confused_2"},
                "smug":        {"eyes": "eyes_squint_2",     "mouth": "mouth_lipbite", "brows": "brows_maniac"},
                "serious":     {"eyes": "eyes_squint",       "mouth": "mouth_normal",  "brows": "brows_angry"},
                "annoyed":     {"eyes": "eyes_side_squint",  "mouth": "mouth_normal",  "brows": "brows_confused"},
                "disgusted":   {"eyes": "eyes_side_squint",  "mouth": "mouth_sad",     "brows": "brows_angry"},
                "embarrassed": {"eyes": "eyes_looking_down", "mouth": "mouth_normal",  "brows": "brows_confused_2"},
            },
            # -- HANDJOB --
            "handjob": {
                "happy":     {"eyes": "eyes_normal",       "mouth": "mouth_laugh",     "brows": "brows_normal"},
                "kissing":   {"eyes": "eyes_closed_happy", "mouth": "mouth_smile",     "brows": "brows_normal"},
                "scared":    {"eyes": "eyes_surprised",    "mouth": "mouth_surprised", "brows": "brows_surprised"},
                "angry":     {"eyes": "eyes_squint",       "mouth": "mouth_serious",   "brows": "brows_surprised"},
                "sad":       {"eyes": "eyes_side",         "mouth": "mouth_sad",       "brows": "brows_sad"},
                "surprised": {"eyes": "eyes_surprised",    "mouth": "mouth_surprised", "brows": "brows_normal"},
                "normal":    {"eyes": "eyes_normal",       "mouth": "mouth_normal",    "brows": "brows_normal"},
                "sexy":      {"eyes": "eyes_squint",       "mouth": "mouth_lipbite",   "brows": "brows_normal"},
                "cumming":   {"eyes": "eyes_closed",       "mouth": "mouth_tongue",    "brows": "brows_sad"},
            },
            # -- BLOWJOB --
            "blowjob": {
                "happy":     {"eyes": "eyes_normal",       "mouth": "mouth_happy",     "brows": "brows_normal"},
                "kissing":   {"eyes": "eyes_closed_happy", "mouth": "mouth_lipbite",   "brows": "brows_normal"},
                "scared":    {"eyes": "eyes_surprised",    "mouth": "mouth_scared",    "brows": "brows_worried"},
                "angry":     {"eyes": "eyes_squint",       "mouth": "mouth_angry",     "brows": "brows_angry"},
                "sad":       {"eyes": "eyes_looking_down", "mouth": "mouth_sad",       "brows": "brows_sad"},
                "surprised": {"eyes": "eyes_surprised",    "mouth": "mouth_surprised", "brows": "brows_confused"},
                "normal":    {"eyes": "eyes_normal",       "mouth": "mouth_tongue",    "brows": "brows_normal"},
                "sexy":      {"eyes": "eyes_squint",       "mouth": "mouth_lipbite",   "brows": "brows_normal"},
                "cumming":   {"eyes": "eyes_closed_happy", "mouth": "mouth_tongue",    "brows": "brows_sad"},
                "ahegao":    {"eyes": "eyes_ahegao",       "mouth": "mouth_tongue",    "brows": "brows_confused"},
                "ahegao_2":  {"eyes": "eyes_ahegao_2",     "mouth": "mouth_tongue",    "brows": "brows_sad"},
            },
            # -- TITJOB --
            "titjob": {
                "happy":     {"eyes": "eyes_normal",       "mouth": "mouth_laugh",     "brows": "brows_normal"},
                "kissing":   {"eyes": "eyes_closed",       "mouth": "mouth_kiss",      "brows": "brows_normal"},
                "scared":    {"eyes": "eyes_squint",       "mouth": "mouth_surprised", "brows": "brows_confused"},
                "angry":     {"eyes": "eyes_normal",       "mouth": "mouth_angry",     "brows": "brows_challenging"},
                "sad":       {"eyes": "eyes_normal",       "mouth": "mouth_sad",       "brows": "brows_sad"},
                "surprised": {"eyes": "eyes_surprised",    "mouth": "mouth_surprised", "brows": "brows_normal"},
                "normal":    {"eyes": "eyes_normal",       "mouth": "mouth_normal",    "brows": "brows_normal"},
                "sexy":      {"eyes": "eyes_sexy",         "mouth": "mouth_lipbite",   "brows": "brows_normal"},
                "cumming":   {"eyes": "eyes_closed",       "mouth": "mouth_ahegao",    "brows": "brows_sad"},
                "ahegao":    {"eyes": "eyes_ahegao",       "mouth": "mouth_ahegao",    "brows": "brows_sad"},
                "ahegao_2":  {"eyes": "eyes_ahegao_2",     "mouth": "mouth_ahegao",    "brows": "brows_sad"},
            },
            # -- COWGIRL --
            "cowgirl": {
                "happy":     {"eyes": "eyes_closed_happy", "mouth": "mouth_smile",     "brows": "brows_normal"},
                "kissing":   {"eyes": "eyes_closed",       "mouth": "mouth_kiss",      "brows": "brows_normal"},
                "scared":    {"eyes": "eyes_surprised",    "mouth": "mouth_scared",    "brows": "brows_scared"},
                "angry":     {"eyes": "eyes_squint",       "mouth": "mouth_angry",     "brows": "brows_angry"},
                "sad":       {"eyes": "eyes_away",         "mouth": "mouth_sad",       "brows": "brows_sad"},
                "surprised": {"eyes": "eyes_surprised",    "mouth": "mouth_surprised", "brows": "brows_surprised"},
                "normal":    {"eyes": "eyes_normal",       "mouth": "mouth_normal",    "brows": "brows_normal"},
                "sexy":      {"eyes": "eyes_sexy",         "mouth": "mouth_lipbite",   "brows": "brows_normal"},
                "cumming":   {"eyes": "eyes_closed",       "mouth": "mouth_tongue",    "brows": "brows_sad"},
                "ahegao":    {"eyes": "eyes_ahegao",       "mouth": "mouth_tongue",    "brows": "brows_surprised"},
                "ahegao_2":  {"eyes": "eyes_ahegao_2",     "mouth": "mouth_tongue",    "brows": "brows_surprised"},
                "moaning":   {"eyes": "eyes_squint",       "mouth": "mouth_moaning",   "brows": "brows_sad"},
            },
            # -- RCG --
            "reverse_cowgirl": {
                "happy":     {"eyes": "eyes_happy",            "mouth": "mouth_smile",     "brows": "brows_normal"},
                "kissing":   {"eyes": "eyes_closed",           "mouth": "mouth_kiss",      "brows": "brows_normal"},
                "scared":    {"eyes": "eyes_surprised",        "mouth": "mouth_scared",    "brows": "brows_surprised"},
                "angry":     {"eyes": "eyes_looking_to_player","mouth": "mouth_scared",    "brows": "brows_angry"},
                "sad":       {"eyes": "eyes_side",             "mouth": "mouth_sad",       "brows": "brows_sad"},
                "surprised": {"eyes": "eyes_surprised",        "mouth": "mouth_surprised", "brows": "brows_surprised"},
                "normal":    {"eyes": "eyes_normal",           "mouth": "mouth_normal",    "brows": "brows_normal"},
                "sexy":      {"eyes": "eyes_sexy",             "mouth": "mouth_lipbite",   "brows": "brows_horny"},
                "cumming":   {"eyes": "eyes_closed",           "mouth": "mouth_tongue",    "brows": "brows_horny"},
                "ahegao":    {"eyes": "eyes_ahegao",           "mouth": "mouth_tongue",    "brows": "brows_up"},
                "ahegao_2":  {"eyes": "eyes_ahegao_2",         "mouth": "mouth_tongue",    "brows": "brows_up"},
                "moaning":   {"eyes": "eyes_blinking",         "mouth": "mouth_moaning",   "brows": "brows_horny"},
                "pleasure":  {"eyes": "eyes_looking_up",       "mouth": "mouth_tongue",    "brows": "brows_horny"},
            },
            # -- DOGGY --
            "doggy": {
                "happy":     {"eyes": "eyes_looking_to_player","mouth": "mouth_happy",     "brows": "brows_happy"},
                "kissing":   {"eyes": "eyes_closed",           "mouth": "mouth_kiss",      "brows": "brows_normal"},
                "scared":    {"eyes": "eyes_looking_to_player","mouth": "mouth_scared",    "brows": "brows_worried"},
                "angry":     {"eyes": "eyes_looking_to_player","mouth": "mouth_sad",       "brows": "brows_angry"},
                "sad":       {"eyes": "eyes_looking_left",     "mouth": "mouth_sad",       "brows": "brows_sad"},
                "surprised": {"eyes": "eyes_surprised",        "mouth": "mouth_surprised", "brows": "brows_surprised"},
                "normal":    {"eyes": "eyes_normal",           "mouth": "mouth_normal",    "brows": "brows_normal"},
                "sexy":      {"eyes": "eyes_sexy",             "mouth": "mouth_lipbite",   "brows": "brows_horny"},
                "cumming":   {"eyes": "eyes_closed",           "mouth": "mouth_tongue",    "brows": "brows_horny"},
                "ahegao":    {"eyes": "eyes_ahegao",           "mouth": "mouth_tongue",    "brows": "brows_surprised"},
                "ahegao_2":  {"eyes": "eyes_ahegao_2",         "mouth": "mouth_tongue",    "brows": "brows_horny"},
                "moaning":   {"eyes": "eyes_blinking",         "mouth": "mouth_moaning",   "brows": "brows_horny"},
                "pleasure":  {"eyes": "eyes_looking_up",       "mouth": "mouth_tongue",    "brows": "brows_horny"},
            },
        },
    }



    # ------------------------------------------------------------
    # Clothing map helper
    # ------------------------------------------------------------
    def _get_clothing_info(girl, slot, code):
        """
        slot: "over" | "chest" | "legs" | "panties" | "shoes"
        code: internal clothing code stored on Girl (e.g. "hoodie")
        Returns a dict with flag_false/flag_true or None.
        """
        if not code:
            return None
        per_girl = CLOTHING_ATTRS.get(girl.Id, {})
        slot_map = per_girl.get(slot, {})
        return slot_map.get(code, None)

    # ------------------------------------------------------------
    # Convert clothing state -> layeredimage attribute
    # ------------------------------------------------------------
    def _attr_for_over(girl):
        if not girl.Over:
            return "over_none"
        info = _get_clothing_info(girl, "over", girl.Over)
        if not info:
            return "over_%s" % girl.Over if not girl.OverUp else "over_%s_up" % girl.Over
        if girl.OverUp:
            return info.get("flag_true") or info.get("flag_false") or "over_none"
        return info.get("flag_false") or "over_none"

    def _attr_for_shoes(girl):
        if not getattr(girl, "Shoes", None):
            return "shoes_none"
        info = _get_clothing_info(girl, "shoes", girl.Shoes)
        if not info:
            return "shoes_%s" % girl.Shoes
        return info.get("flag_false") or "shoes_none"

    def _attr_for_chest(girl):
        if not girl.Chest:
            if getattr(girl, "Piercing", False):
                return "chest_piercing"
            return "chest_none"
        info = _get_clothing_info(girl, "chest", girl.Chest)
        if not info:
            return "chest_%s" % girl.Chest if not girl.ChestUp else "chest_%s_up" % girl.Chest
        if girl.ChestUp:
            return info.get("flag_true") or info.get("flag_false") or "chest_none"
        return info.get("flag_false") or "chest_none"

    def _attr_for_legs(girl):
        if not girl.Legs:
            return "legs_none"
        info = _get_clothing_info(girl, "legs", girl.Legs)
        if not info:
            return "legs_%s" % girl.Legs if not girl.LegsDown else "legs_%s_up" % girl.Legs
        if girl.LegsDown:
            return info.get("flag_true") or info.get("flag_false") or "legs_none"
        return info.get("flag_false") or "legs_none"

    def _attr_for_panties(girl):
        if not girl.Panties:
            return "panties_none"
        info = _get_clothing_info(girl, "panties", girl.Panties)
        if not info:
            return "panties_%s" % girl.Panties if not girl.PantiesDown else "panties_%s_down" % girl.Panties
        if girl.PantiesDown:
            return info.get("flag_true") or "panties_none"
        return info.get("flag_false") or "panties_none"

    def _attr_for_collar(girl):
        return "collar_on" if getattr(girl, "Collar", False) else "collar_none"

    def _bj_attrs_for_slot(girl, slot, code, flag=False):
        if not code:
            return []
        per_girl = BJ_CLOTHING_ATTRS.get(girl.Id, {})
        slot_map = per_girl.get(slot, {})
        info = slot_map.get(code)
        if not info:
            return []
        if flag:
            return list(info.get("flag_true", []))
        return list(info.get("flag_false", []))

    def _rcg_attrs_for_slot(girl, slot, code, flag=False):
        if not code:
            return []
        per_girl = RCG_CLOTHING_ATTRS.get(girl.Id, {})
        slot_map = per_girl.get(slot, {})
        info = slot_map.get(code)
        if not info:
            return []
        if flag:
            return list(info.get("flag_true", []))
        return list(info.get("flag_false", []))

    def _cowgirl_attrs_for_slot(girl, slot, code, flag=False):
        if not code:
            return []
        per_girl = COWGIRL_CLOTHING_ATTRS.get(girl.Id, {})
        slot_map = per_girl.get(slot, {})
        info = slot_map.get(code)
        if not info:
            return []
        if flag:
            return list(info.get("flag_true", []))
        return list(info.get("flag_false", []))

    def _build_blowjob_attributes(girl):
        # Use unified clothing registry
        attrs = list(_build_clothing_attributes(girl, "blowjob"))

        _has_chest_attr = any(a in ("chest_none", "chest_piercing", "chest_hidden") for a in attrs)
        _chest_exposed = (not girl.Chest or girl.ChestUp)

        if _chest_exposed and not _has_chest_attr:
            if getattr(girl, "Piercing", False):
                attrs.append("chest_piercing")
            else:
                attrs.append("chest_none")
        elif _chest_exposed and getattr(girl, "Piercing", False):
            if "chest_hidden" not in attrs and "chest_piercing" not in attrs:
                if "chest_none" in attrs:
                    attrs.remove("chest_none")
                attrs.append("chest_piercing")

        return attrs

    def _build_rcg_attributes(girl):
        state = sprite_state.setdefault(girl.Id, {})

        # In active sex scenes, butt_bottom is a standalone animated layer (ApplySpeed).
        # Outside sex scenes (debug, static), show it inside the layeredimage.
        _in_scene = getattr(store, "rcg_started", False) or getattr(store, "rcg_rub_mode", False)
        _butt_attr = "butt_bottom_none" if _in_scene else "butt_bottom_base"
        _butt_top = "butt_top_none" if _in_scene else "butt_top_1"

        # ConditionSwitch girls: face is driven by sprite_state, not attributes
        _cs_girls = getattr(store, "_RCG_CS_GIRLS", set())
        if girl.gid in _cs_girls:
            attrs = [_butt_attr, "butt_safe_on", _butt_top, "thigh_highs_none"]
        else:
            brows = _rcg_safe(state.get("brows", "brows_normal"))
            eyes = _rcg_safe(state.get("eyes", "eyes_normal"))
            mouth = _rcg_safe(state.get("mouth", "mouth_normal"))
            attrs = [brows, eyes, mouth, _butt_attr, "butt_safe_on", _butt_top, "thigh_highs_none"]
        attrs.append("collar_none")

        # Arms: pose 1 inside layeredimage, pose 2 shown externally
        # Rogue: arms_2 body stays in layeredimage (below butt), only hands go standalone
        arms_pose = getattr(store, "rcg_arms_pose", 1)
        _gid = getattr(girl, "gid", "")
        if arms_pose == 1:
            if has_clothing_layer(girl, "over", "reverse_cowgirl", "arms_1"):
                attrs.append("arms_ls_1")
            else:
                attrs.append("arms_1")
        elif _gsc(_gid, "arms_2_in_li", False, "rcg"):
            attrs.append("arms_2")
        else:
            attrs.append("arms_none")

        # Skirt: in sex scenes shown as standalone layer (ApplySpeed) for butt sync.
        # Outside sex scenes (debug), show inside the layeredimage.
        if _in_scene:
            attrs.append("skirt_none")
        else:
            _dg_skirt = [a for a in _build_clothing_attributes(girl, "reverse_cowgirl") if "skirt" in a]
            attrs.extend(_dg_skirt if _dg_skirt else ["skirt_none"])

        # Panties: in ANY scene shown as standalone for butt sync.
        # Outside scenes (debug/static), show inside layeredimage.
        if _in_scene:
            attrs.append("panties_none")
        else:
            _dg_clothing = _build_clothing_attributes(girl, "reverse_cowgirl")
            _dg_panties = [a for a in _dg_clothing if "panties" in a]
            if _dg_panties:
                attrs.extend(_dg_panties)
            else:
                attrs.append("panties_none")

        # Over + Chest via registry
        _dg_clothing = _build_clothing_attributes(girl, "reverse_cowgirl")
        _got_over = False
        _got_chest = False
        for a in _dg_clothing:
            if "torso_over" in a and a not in attrs:
                attrs.append(a)
                _got_over = True
            elif "torso_chest" in a and a not in attrs:
                attrs.append(a)
                _got_chest = True
        if not _got_over:
            attrs.append("torso_over_none")
        if not _got_chest:
            attrs.append("torso_chest_none")

        print("[RCG_BUILD] gid=%s in_scene=%s Over=%s clothes=%s clothing_attrs=%s final=%s" % (
            girl.gid, _in_scene, getattr(girl, "Over", None),
            str(girl.clothes), str(_dg_clothing), str(attrs)))
        return attrs

    def _build_doggy_attributes(girl):
        """Build attributes for the doggy layeredimage."""
        _in_scene = getattr(store, "doggy_started", False)
        _in_rub = getattr(store, "doggy_rub_mode", False)
        _butt_gap = "butt_gap_none" if (_in_scene or _in_rub) else "butt_gap_base"
        _butt_top = "butt_top_none" if (_in_scene or _in_rub) else "butt_top_base"
        attrs = [_butt_gap, _butt_top]

        # Collar
        attrs.append("collar_on" if getattr(girl, "Collar", False) else "collar_none")

        # Over + Chest via registry
        _dg_clothing = _build_clothing_attributes(girl, "doggy")
        debug_log("[DG_ATTRS] registry returned: %s | clothes=%s" % (str(_dg_clothing), str(girl.clothes)))
        _got_over = False
        _got_chest = False
        for a in _dg_clothing:
            if "torso_over" in a and a not in attrs:
                attrs.append(a)
                _got_over = True
            elif "torso_chest" in a and a not in attrs:
                attrs.append(a)
                _got_chest = True
        if not _got_over:
            attrs.append("torso_over_none")
        if not _got_chest:
            attrs.append("torso_chest_none")

        debug_log("[DG_ATTRS] final: %s" % str(attrs))
        return attrs

    _TITJOB_FALLBACK = {
        "brows_surprised": "brows_confused",
        "brows_horny":     "brows_normal",
        "brows_up":        "brows_confused",
        "eyes_squint_big": "eyes_squint",
        "eyes_squint_2":   "eyes_squint",
        "eyes_surprised":  "eyes_normal",
        "eyes_surprised_2":"eyes_normal",
        "eyes_side":       "eyes_looking_left",
        "eyes_side_2":     "eyes_looking_right",
        "eyes_looking_to_player": "eyes_looking_left",
        "eyes_looking_up": "eyes_normal",
        "eyes_left_closed":"eyes_closed",
        "eyes_right_closed":"eyes_closed",
        "mouth_normal":    "mouth_normal",
        "mouth_smile":     "mouth_laugh",
        "mouth_tongue":    "mouth_open",
        "mouth_disgusted": "mouth_sad",
        "mouth_open_teeth":"mouth_open",
        "mouth_sch":       "mouth_normal",
        "mouth_serious":   "mouth_normal",
        "mouth_scared":    "mouth_surprised",
        "mouth_kissing":   "mouth_kiss",
    }

    def _titjob_safe(attr):
        return _TITJOB_FALLBACK.get(attr, attr)

    # ── RCG fallback ──
    # Attrs defined in DG layeredimage: brows_(normal,confused,surprised,horny,sad,up)
    #   eyes_(normal,side,side_2,squint,squint_big,surprised,surprised_2,closed,
    #         left_closed,right_closed,squint_2,looking_to_player,looking_up)
    #   mouth_(normal,smile,laugh,surprised,tongue,disgusted,open_teeth,sch,serious,
    #          lipbite,kiss,scared)
    _RCG_FALLBACK = {
        # Brows not in DG
        "brows_challenging":  "brows_horny",
        "brows_confused_2":   "brows_confused",
        # Eyes not in DG
        "eyes_sexy":          "eyes_looking_to_player",
        "eyes_side_squint":   "eyes_squint",
        "eyes_blink_left":    "eyes_squint",
        "eyes_blink_right":   "eyes_squint",
        "eyes_looking_left":  "eyes_side",
        "eyes_looking_right": "eyes_side_2",
        # Mouth not in DG
        "mouth_happy":        "mouth_smile",
        "mouth_angry":        "mouth_scared",
        "mouth_screaming":    "mouth_surprised",
        "mouth_sucking":      "mouth_surprised",
        "mouth_ahegao":       "mouth_tongue",
        "mouth_open":         "mouth_surprised",
        "mouth_sad":          "mouth_serious",
        "mouth_kissing":      "mouth_kiss",
    }

    def _rcg_safe(attr):
        return _RCG_FALLBACK.get(attr, attr)

    # ── COWGIRL fallback ──
    # Attrs defined in CG layeredimage: brows_(normal,confused,surprised,horny)
    #   eyes_(normal,side,side_2,squint,squint_big,surprised,surprised_2,closed,
    #         left_closed,right_closed,squint_2)
    #   mouth_(normal,disgusted,laugh,open_teeth,sch,serious,smile,surprised,tongue)
    _COWGIRL_FALLBACK = {
        # Brows not in CG
        "brows_sad":          "brows_confused",
        "brows_up":           "brows_surprised",
        "brows_challenging":  "brows_horny",
        "brows_confused_2":   "brows_confused",
        # Eyes not in CG
        "eyes_looking_to_player": "eyes_side",
        "eyes_looking_up":        "eyes_surprised",
        "eyes_sexy":              "eyes_surprised_2",
        "eyes_side_squint":       "eyes_squint",
        "eyes_side_squint_2":     "eyes_squint_2",
        "eyes_blink_left":        "eyes_squint",
        "eyes_blink_right":       "eyes_squint",
        "eyes_looking_left":      "eyes_side",
        "eyes_looking_right":     "eyes_side_2",
        # Mouth not in CG
        "mouth_kiss":         "mouth_smile",
        "mouth_scared":       "mouth_surprised",
        "mouth_lipbite":      "mouth_smile",
        "mouth_tongue":       "mouth_sch",
        "mouth_ahegao":       "mouth_open_teeth",
        "mouth_happy":        "mouth_smile",
        "mouth_angry":        "mouth_serious",
        "mouth_screaming":    "mouth_surprised",
        "mouth_sucking":      "mouth_surprised",
        "mouth_sad":          "mouth_disgusted",
        "mouth_kissing":      "mouth_smile",
        "mouth_open":         "mouth_open_teeth",
    }

    def _cowgirl_safe(attr):
        return _COWGIRL_FALLBACK.get(attr, attr)

    def _build_titjob_attributes(girl):
        state = sprite_state.setdefault(girl.Id, {})

        brows = _titjob_safe(state.get("brows", "brows_normal"))
        eyes = _titjob_safe(state.get("eyes", "eyes_normal"))
        mouth = _titjob_safe(state.get("mouth", "mouth_normal"))

        attrs = [brows, eyes, mouth]

        # Arms: long shirt variants if over has them
        arms_pose = getattr(store, "titjob_arms_pose", 1)
        _arm_key = "arms_%d" % arms_pose
        if has_clothing_layer(girl, "over", "titjob", _arm_key):
            arms_map = {1: "arms_ls_1", 2: "arms_ls_2", 3: "arms_ls_3"}
            attrs.append(arms_map.get(arms_pose, "arms_ls_1"))
        else:
            arms_map = {1: "arms_1", 2: "arms_2", 3: "arms_3"}
            attrs.append(arms_map.get(arms_pose, "arms_1"))

        # Chest via registry
        _tj_clothing = _build_clothing_attributes(girl, "titjob")
        if _tj_clothing:
            attrs.extend(_tj_clothing)
        else:
            attrs.append("chest_base_none")
            attrs.append("corset_up_none")

        attrs.append("penis_none")
        attrs.append("boobs_naked")

        return attrs

    def _build_cowgirl_attributes(girl):
        state = sprite_state.setdefault(girl.Id, {})

        brows = _cowgirl_safe(state.get("brows", "brows_normal"))
        eyes = _cowgirl_safe(state.get("eyes", "eyes_normal"))
        mouth = _cowgirl_safe(state.get("mouth", "mouth_normal"))

        cowgirl_speed = getattr(store, "cowgirl_speed", 0)

        attrs = [brows, eyes, mouth]

        attrs.append("head_base_bob" if cowgirl_speed >= 1 else "head_base")

        arms_pose = getattr(store, "cowgirl_arms_pose", 1)
        cowgirl_speed = getattr(store, "cowgirl_speed", 0)
        if getattr(store, "cowgirl_masturbating", False):
            if _gsc(girl.gid, "mast_arm_separate", False, "cowgirl"):
                if getattr(store, "_oral_active", False):
                    attrs.append("arms_low_2")
                else:
                    attrs.append("arms_low_none")
                attrs.append("arms_high_none")
                attrs.append("masturbate_hand_none")
            elif getattr(store, "_oral_active", False):
                attrs.append("arms_low_2")
                attrs.append("arms_high_none")
                attrs.append("masturbate_hand_none")
            else:
                attrs.append("arms_low_none")
                attrs.append("arms_high_masturbate")
                attrs.append("masturbate_hand_on")
        elif arms_pose == 2:
            attrs.append("arms_low_2")
            attrs.append("arms_high_none")
            attrs.append("masturbate_hand_none")
        else:
            attrs.append("arms_low_none")
            attrs.append("arms_high_1")
            attrs.append("masturbate_hand_none")

        if _gsc(girl.gid, "has_shoulders", False, "cowgirl"):
            attrs.append("shoulder_right_on")
            attrs.append("shoulder_left_on")

        _cg_touch = getattr(store, "cowgirl_guy_touch", None)
        if getattr(store, "cowgirl_masturbating", False):
            attrs.append("guy_arms_none")
        elif _cg_touch == "grab_tits":
            attrs.append("guy_arms_none")
        elif _cg_touch == "push_down":
            # Use guy_arms_none when split left/right images exist (shown standalone by ApplySpeed)
            _arm_l = "%s cowgirl_guy_arms_left" % girl.gid
            if renpy.has_image(_arm_l):
                attrs.append("guy_arms_none")
            else:
                attrs.append("guy_arms_on")
        else:
            attrs.append("guy_arms_none")

        attrs.append("penis_top_none")

        attrs.append("guy_none")

        attrs.append("legs_bottom_none")

        # Clothing via registry
        _cg_clothing = _build_clothing_attributes(girl, "cowgirl")
        _has_panties = any("panties" in a for a in _cg_clothing)
        _has_over = any("torso_over" in a for a in _cg_clothing)
        _has_skirt = any("skirt" in a for a in _cg_clothing)
        _has_shoes = any("thigh_highs" in a for a in _cg_clothing)

        if _has_panties:
            attrs.extend([a for a in _cg_clothing if "panties" in a])
        else:
            attrs.append("panties_top_none")
            attrs.append("panties_bottom_none")

        if _has_skirt:
            attrs.extend([a for a in _cg_clothing if "skirt" in a])
        else:
            attrs.append("skirt_none")

        if _has_over:
            attrs.extend([a for a in _cg_clothing if "torso_over" in a])
        else:
            attrs.append("torso_over_none")

        if _gsc(girl.gid, "chest_always_hidden", False, "cowgirl"):
            attrs.append("torso_clothing_none")
            attrs.append("boobs_none")
        else:
            if girl.Chest:
                attrs.append("torso_clothing_none")
                attrs.append("boobs_none")
            else:
                if not girl.Over:
                    attrs.append("torso_clothing_none")
                attrs.append("boobs_none")

        if _has_shoes:
            attrs.extend([a for a in _cg_clothing if "thigh_highs" in a])
        else:
            attrs.append("thigh_highs_none")

        return attrs

    # ------------------------------------------------------------
    # Fallback map: attribute names that don't exist in standing → safe replacement
    _STANDING_FALLBACK = {
        # Eyes from other poses → standing equivalents
        "eyes_looking_to_player": "eyes_side",
        "eyes_looking_up":       "eyes_surprised",
        "eyes_looking_left":     "eyes_side",
        "eyes_left_closed":      "eyes_closed",
        "eyes_right_closed":     "eyes_closed",
        "eyes_squint_2":         "eyes_squint",
        "eyes_squinted_big":     "eyes_squint_big",
        "eyes_sexy":             "eyes_side",
        "eyes_blink_left":       "eyes_squint",
        "eyes_blink_right":      "eyes_squint",
        "eyes_ahegao":           "eyes_surprised",
        "eyes_ahegao_2":         "eyes_surprised_2",
        "eyes_away":             "eyes_side",
        "eyes_bliss":            "eyes_closed_happy",
        "eyes_up":               "eyes_surprised",
        "eyes_closed_left":      "eyes_closed",
        "eyes_closed_right":     "eyes_closed",
        "eyes_up_closed_left":   "eyes_closed",
        # Mouth from other poses → standing equivalents
        "mouth_kiss":            "mouth_kissing",
        "mouth_scared":          "mouth_surprised",
        "mouth_sad":             "mouth_serious",
        "mouth_angry":           "mouth_serious",
        "mouth_screaming":       "mouth_surprised",
        "mouth_sucking":         "mouth_surprised",
        "mouth_happy":           "mouth_smile",
        "mouth_ahegao":          "mouth_surprised",
        "mouth_open":            "mouth_open_teeth",
        # Brows from other poses → standing equivalents
        "brows_horny":           "brows_normal",
        "brows_sad":             "brows_confused",
        "brows_up":              "brows_surprised",
        "brows_challenging":     "brows_normal",
        "brows_confused_2":      "brows_confused",
        "brows_scared":          "brows_sad",
        # Mouth moaning variants (FN/other poses)
        "mouth_moaning":         "mouth_surprised",
        "mouth_moaning_2":       "mouth_surprised",
        "mouth_moaning_3":       "mouth_surprised",
    }

    def _standing_safe(attr):
        """Return a standing-safe attribute, using fallback if needed."""
        return _STANDING_FALLBACK.get(attr, attr)

    # Build attribute list for a girl
    # ------------------------------------------------------------
    def _build_attributes_for_girl(girl, pose="standing"):
        """
        Returns a list of attribute strings for the layeredimage.
        Uses unified CLOTHING_REGISTRY for clothing attrs across all poses.
        """
        state = sprite_state.setdefault(girl.Id, {})

        brows = state.get("brows", "brows_normal")
        eyes = state.get("eyes", "eyes_normal")
        mouth = state.get("mouth", "mouth_normal")

        # Apply fallbacks for standing/handjob (shared layeredimage base)
        if pose in ("standing", "handjob"):
            brows = _standing_safe(brows)
            eyes = _standing_safe(eyes)
            mouth = _standing_safe(mouth)

        # Face attrs (BJ/RCG/cowgirl/titjob/doggy handle face in their own builders)
        if pose in ("blowjob", "reverse_cowgirl", "reverse_cowgirl_anal", "titjob", "cowgirl", "doggy", "laying_down", "laying_anal", "full_nelson", "full_nelson_anal"):
            return _build_pose_attributes(girl, pose)

        # Standing / Handjob: face + clothing + extras
        attrs = [brows, eyes, mouth]

        # Clothing via unified registry (handles shower override too)
        attrs.extend(_build_clothing_attributes(girl, pose))

        # Chest body: switch between nude/piercing/clothed chest shape
        if pose in ("standing", "handjob"):
            _chest_exposed = (not girl.Chest) or girl.ChestUp
            _mid_covers = girl.Mid and not girl.MidUp
            if _chest_exposed and not _mid_covers and getattr(girl, "Piercing", False):
                if "chest_none" in attrs:
                    attrs.remove("chest_none")
                attrs.append("chest_piercing")
            elif (not _chest_exposed or _mid_covers) and _gsc(girl.gid, "has_chest_clothes_body", False, pose):
                attrs.append("chest_clothes")
            elif _chest_exposed and "chest_none" not in attrs:
                attrs.append("chest_none")

        debug_log("[DEBUG] _build_attributes: gid=%s pose=%s chest=%s chestUp=%s attrs=%s" % (
            getattr(girl, "gid", "?"), pose, str(getattr(girl, "Chest", None)),
            str(getattr(girl, "ChestUp", False)), str(attrs)))

        # Pose-specific extras
        if pose == "standing":
            _arm_pos = state.get("arm_pos", 0)
            if _arm_pos == 0:
                _arm_pos = renpy.random.choice([1, 1, 4, 4, 4])
                state["arm_pos"] = _arm_pos
            if hasattr(girl, "has_temp_status") and girl.has_temp_status("angry") and not _girl_in_sex_scene(girl):
                _arm_pos = 2
            _chest_item = getattr(girl, "clothes", {}).get("chest", None)
            _is_bikini = _chest_item and "bikini" in str(_chest_item)
            if _arm_pos == 1 and _is_bikini:
                _arm_pos = 4
            # Author's rule (2026-09-22): from visual pregnancy stage 1 on, a girl does not cross her arms standing
            # (arm pose 1), unless her crossed-arms pregnancy art is wired ("preg_crossed_arms", scene_config: Shion,
            # whose crossed arms are pose 4 and whose "Jacket Preg Crossed" is in PREG_ART). Gwen's "Cover Crossed
            # Arms" and Tenny's "Blue Shirt Arms Crossed" stay in the image folders, unwired.
            if (_arm_pos == 1 and not _gsc(girl.gid, "preg_crossed_arms", False, "standing")
                    and callable(globals().get("preg_vstage", None)) and preg_vstage(girl.gid) >= 1):
                _arm_pos = 4
            # Towel arms follow the towel LAYER the clothing builder actually emitted, not girl.clothes:
            # the shower override can render over_none (+ towel_arm_left_none) while clothes["over"] is
            # still "towel", and a second attribute of group towel_left_arm makes Ren'Py raise.
            _is_towel = any(_a.startswith("over_towel") for _a in attrs)
            _clothes_towel = getattr(girl, "clothes", {}).get("over") == "towel"
            if _is_towel != _clothes_towel:
                print("[TOWEL_SYNC] %s: towel layer=%s but clothes.over=%s shower_state=%s" % (girl.gid, _is_towel, getattr(girl, "clothes", {}).get("over"), getattr(girl, "shower_state", None)))

            _has_af = _gsc(girl.gid, "has_arms_front", False, "standing")
            if _is_towel and _has_af:
                attrs.append("left_arm_none")
                attrs.append("arms_front_none")
                if girl.gid in ("tenny", "shion"):
                    attrs.append("arm_right_%d" % _arm_pos)
                    attrs.append("towel_arm_left_%d" % _arm_pos)
                elif _arm_pos == 1:
                    attrs.append("arm_right_none")
                    attrs.append("towel_arm_right_1")
                    attrs.append("towel_arm_left_1")
                    attrs.append("towel_arms_front_1")
                else:
                    attrs.append("arm_right_%d" % _arm_pos)
                    attrs.append("towel_arm_right_none")
                    attrs.append("towel_arm_left_%d" % _arm_pos)
                    attrs.append("towel_arms_front_none")
            else:
                attrs.append("arm_right_%d" % _arm_pos)
                if _has_af:
                    attrs.append("left_arm_%d" % _arm_pos)
                    if _arm_pos == 1:
                        attrs.append("arms_front_1")
                    else:
                        attrs.append("arms_front_none")
                print("[STANDING_ARMS] gid=%s arm_pos=%d has_af=%s towel=%s attrs_added=%s" % (girl.gid, _arm_pos, _has_af, _is_towel, str([a for a in attrs if 'arm' in a or 'front' in a])))

            if _is_towel:
                # Nothing under the towel keeps its own arms: a vest / jacket BODY composite still on
                # (the towel wrapped over her clothes, _shower_story_caught's cover) drew her arms
                # UNDER the towel. Shion's crossed arms vanished beneath "Towell.png" that way
                # (author 2026-10-11): the towel re-render groups above the towel are the only arms
                # of a towel sprite, so the body composites go out with the towel on.
                for _i, _a in enumerate(attrs):
                    if _a.startswith("mid_body_") and _a != "mid_body_none":
                        attrs[_i] = "mid_body_none"
                        print("[STANDING_ARMS] %s: towel on, %s -> mid_body_none" % (girl.gid, _a))
                    elif _a.startswith("over_body_") and _a != "over_body_none":
                        attrs[_i] = "over_body_none"
                        print("[STANDING_ARMS] %s: towel on, %s -> over_body_none" % (girl.gid, _a))

            if _arm_pos in (2, 3, 4):
                _arm_composite_items = ("over_long_shirt", "over_blue_jacket", "mid_blue_shirt", "mid_blue_shirt_up", "mid_body_vest", "over_body_jacket")
                for _i, _a in enumerate(attrs):
                    if _a in _arm_composite_items:
                        attrs[_i] = "%s_arm%d" % (_a, _arm_pos)
                # Arms 2/3/4 over composites include the jacket body,
                # so hide the separate over_body to avoid double-render
                for _i, _a in enumerate(attrs):
                    if _a == "over_body_blue_jacket":
                        attrs[_i] = "over_body_none"
                        break
                if _is_towel and girl.gid == "tenny":
                    for _i, _a in enumerate(attrs):
                        if _a == "over_towel":
                            attrs[_i] = "over_towel_arm23" if _arm_pos in (2, 3) else "over_towel_arm4"
                            break

            _girl_clothes = getattr(girl, "clothes", {})
            _over_code = _girl_clothes.get("over")

            # chest_above re-render removed: arms always render above chest clothing

            # Over sleeve split: left sleeve or body above chest_above_arms
            if _over_code and _over_code != "towel":
                if girl.gid in ("gwen", "ntw"):
                    attrs.append("over_left_%d" % _arm_pos)
                elif girl.gid == "rogue":
                    if _arm_pos == 1:
                        attrs.append("over_body_mesh")
                    else:
                        for _i, _a in enumerate(attrs):
                            if _a.startswith("over_long_shirt_arm"):
                                attrs[_i] = "over_none"
                                break
                        attrs.append("over_body_mesh_arm%d" % _arm_pos)

            if girl.gid == "tenny":
                _over_item = getattr(girl, "clothes", {}).get("over")
                if _over_item != "blue_jacket":
                    attrs.append("over_body_none")
                _mid_item = getattr(girl, "clothes", {}).get("mid")
                if _mid_item != "blue_shirt":
                    attrs.append("mid_body_none")

            attrs.extend(_cum_attrs_for_standing(girl))
            attrs.append(_attr_for_collar(girl))
            attrs.append(_attr_for_blush(girl))
            attrs.extend(_cum_face_attrs_for_standing(girl))

        elif pose == "handjob":
            attrs.extend(_cum_attrs_for_hj(girl))
            attrs.append(_attr_for_collar(girl))
            attrs.append(_attr_for_blush(girl))
            attrs.extend(_cum_face_attrs_for_hj(girl))

        return attrs

    def _build_pose_attributes(girl, pose):
        """Build attrs for sex scene poses (BJ, RCG, cowgirl, titjob).
        Delegates to the existing per-pose builders for face/expression/cum,
        but uses unified _build_clothing_attributes for clothing."""
        # Use existing builders for now — they handle face, cum, and pose-specific logic.
        # The clothing part will be gradually migrated.
        if pose == "blowjob":
            return _build_blowjob_attributes(girl)
        if pose == "reverse_cowgirl":
            return _build_rcg_attributes(girl)
        if pose == "titjob":
            return _build_titjob_attributes(girl)
        if pose == "cowgirl":
            return _build_cowgirl_attributes(girl)
        if pose == "doggy":
            return _build_doggy_attributes(girl)
        return []

    # ------------------------------------------------------------
    # set_girl_sprite – show layeredimage using current state
    # ------------------------------------------------------------
    # Girls whose sprites are suppressed (e.g. during phone calls)
    _sprite_suppressed = set()

    _recording_active = False
    _recording_girl = None

    # ----------------------------------------------------------
    # STANDING BLINK (background thread per girl)
    # ----------------------------------------------------------
    _standing_blink_girls = set()  # track active blink threads
    _standing_blink_gen = {}  # generation counter per gid to kill stale threads

    def _blink_gen_alive(gid, my_gen):
        return gid in store._standing_blink_girls and store._standing_blink_gen.get(gid, -1) == my_gen

    def _standing_blink_loop(girl, my_gen):
        import time as _time, random as _random
        gid = getattr(girl, "gid", girl.Id)
        _eyes_were_closed = False
        _saved_eyes = "eyes_normal"
        try:
            while _blink_gen_alive(gid, my_gen):
                _time.sleep(_random.uniform(3.0, 7.0))
                if not _blink_gen_alive(gid, my_gen):
                    break
                state = sprite_state.get(girl.Id, {})
                if state.get("pose") != "standing" or _girl_in_sex_scene(girl):
                    continue
                if not renpy.showing(girl.Id):
                    continue
                current_eyes = state.get("eyes", "eyes_normal")
                if current_eyes in ("eyes_closed", "eyes_squint_big"):
                    continue
                try:
                    if not renpy.showing(girl.Id) or not _blink_gen_alive(gid, my_gen):
                        continue
                    _blink_at = state.get("_last_at_list")
                    if not _blink_at:
                        _saved_slot = getattr(girl, "SpriteLoc", StageCenter)
                        _BLINK_SLOT_MAP = {
                            StageLeft: [slot_left],
                            StageCenterLeft: [slot_center_left],
                            StageCenterRight: [slot_center_right],
                            StageRight: [slot_right],
                        }
                        _blink_at = _BLINK_SLOT_MAP.get(_saved_slot, [slot_center])
                    _saved_eyes = current_eyes
                    state["eyes"] = "eyes_closed"
                    _eyes_were_closed = True
                    if state.get("pose") != "standing":
                        state["eyes"] = _saved_eyes
                        _eyes_were_closed = False
                        continue
                    attrs = _build_attributes_for_girl(girl, "standing")
                    img_name = "%s standing" % girl.Id
                    if attrs:
                        img_name += " " + " ".join(attrs)
                    _blink_z = state.get("_zorder", 0)
                    _blink_show_kw = {"tag": girl.Id, "at_list": _blink_at}
                    if _blink_z:
                        _blink_show_kw["zorder"] = _blink_z
                    if gid == "tenny":
                        print("[TENNY_TRACE] blink CLOSE: showing '%s' gen=%d alive=%s" % (img_name, my_gen, _blink_gen_alive(gid, my_gen)))
                    renpy.show(img_name, **_blink_show_kw)
                    renpy.restart_interaction()
                    if not _blink_gen_alive(gid, my_gen):
                        _eyes_were_closed = False
                        break
                    _time.sleep(_random.uniform(0.10, 0.18))
                    state["eyes"] = _saved_eyes
                    _eyes_were_closed = False
                    if not _blink_gen_alive(gid, my_gen):
                        break
                    if state.get("pose") != "standing":
                        continue
                    attrs = _build_attributes_for_girl(girl, "standing")
                    img_name = "%s standing" % girl.Id
                    if attrs:
                        img_name += " " + " ".join(attrs)
                    _blink_z = state.get("_zorder", 0)
                    _blink_show_kw = {"tag": girl.Id, "at_list": _blink_at}
                    if _blink_z:
                        _blink_show_kw["zorder"] = _blink_z
                    if gid == "tenny":
                        print("[TENNY_TRACE] blink OPEN: showing '%s' gen=%d alive=%s" % (img_name, my_gen, _blink_gen_alive(gid, my_gen)))
                    renpy.show(img_name, **_blink_show_kw)
                    renpy.restart_interaction()
                    if not _blink_gen_alive(gid, my_gen):
                        break
                except:
                    state["eyes"] = _saved_eyes
                    _eyes_were_closed = False
        finally:
            if _eyes_were_closed:
                try:
                    state = sprite_state.get(girl.Id, {})
                    state["eyes"] = _saved_eyes
                    if renpy.showing(girl.Id) and state.get("pose") == "standing":
                        attrs = _build_attributes_for_girl(girl, "standing")
                        img_name = "%s standing" % girl.Id
                        if attrs:
                            img_name += " " + " ".join(attrs)
                        _blink_at = state.get("_last_at_list")
                        if not _blink_at:
                            _fs = getattr(girl, "SpriteLoc", StageCenter)
                            _FS_MAP = {
                                StageLeft: [slot_left],
                                StageCenterLeft: [slot_center_left],
                                StageCenterRight: [slot_center_right],
                                StageRight: [slot_right],
                            }
                            _blink_at = _FS_MAP.get(_fs, [slot_center])
                        _blink_z = state.get("_zorder", 0)
                        _blink_show_kw = {"tag": girl.Id, "at_list": _blink_at}
                        if _blink_z:
                            _blink_show_kw["zorder"] = _blink_z
                        if gid == "tenny":
                            print("[TENNY_TRACE] blink FINALLY: re-showing '%s'" % img_name)
                        renpy.show(img_name, **_blink_show_kw)
                        renpy.restart_interaction()
                except:
                    pass

    def start_standing_blink(girl):
        gid = getattr(girl, "gid", girl.Id)
        _gen = store._standing_blink_gen.get(gid, 0) + 1
        store._standing_blink_gen[gid] = _gen
        store._standing_blink_girls.add(gid)
        renpy.invoke_in_thread(_standing_blink_loop, girl, _gen)

    def stop_standing_blink(girl):
        gid = getattr(girl, "gid", girl.Id)
        store._standing_blink_girls.discard(gid)

    def hide_girl_sprite(girl_or_gid):
        """Hide a girl and stop her standing blink thread so she
        doesn't reappear from a background blink cycle."""
        if isinstance(girl_or_gid, str):
            gid = girl_or_gid
            _girl_id = gid
        else:
            gid = getattr(girl_or_gid, "gid", girl_or_gid.Id)
            _girl_id = girl_or_gid.Id if hasattr(girl_or_gid, "Id") else gid
        print("[HIDE_GIRL] hiding %s (was_showing=%s)" % (gid, renpy.showing(gid)))
        if gid == "tenny":
            import traceback as _tb_h
            _stack_h = "".join(_tb_h.format_stack()[-5:])
            print("[TENNY_TRACE] hide_girl_sprite: sprite_state=%s blink_set=%s\n%s" % (
                sprite_state.get(_girl_id), gid in store._standing_blink_girls, _stack_h))
        store._standing_blink_girls.discard(gid)
        _hs = sprite_state.get(_girl_id)
        if _hs:
            _hs["pose"] = "hidden"
            _hs.pop("_zorder", None)
        renpy.hide(gid)

    def _dedupe_layered_attrs(img_name, attrs):
        """Keep one attribute per layeredimage group (the LAST one wins). Ren'Py raises "The specified
        attributes for X conflict" when two attributes of the same group are shown together.
        Uses the layeredimage's own group table; `multiple` groups have no group there, so they are
        never touched. No-op when the image is not a layeredimage."""
        if not attrs:
            return attrs
        _a2g = getattr(renpy.get_registered_image(img_name), "attribute_to_groups", None)
        if not _a2g:
            return attrs
        _seen = set()
        _out = []
        for _a in reversed(attrs):
            if _a in _out:
                continue   # the same attribute listed twice is not a conflict
            _groups = _a2g.get(_a, ())
            if any(_g in _seen for _g in _groups):
                print("[ATTR_CONFLICT] %s: dropped '%s' (group %s already set by a later attr) full=%s" % (img_name, _a, list(_groups), str(attrs)))
                continue
            _seen.update(_groups)
            _out.append(_a)
        _out.reverse()
        return _out

    def set_girl_sprite(girl_or_id, pose="standing", at_list=None, zorder=None, **face_parts):
        girl = _resolve_girl(girl_or_id)
        if not girl:
            return

        if getattr(girl, "gid", "") == "tenny":
            import traceback as _tb_t
            _stack_t = "".join(_tb_t.format_stack()[-6:])
            print("[TENNY_TRACE] set_girl_sprite called for TENNY pose=%s at_list=%s zorder=%s\n%s" % (pose, at_list, zorder, _stack_t))

        if pose == "standing" and _girl_in_sex_scene(girl):
            import traceback as _tb
            _stack = "".join(_tb.format_stack())
            print("[BUG_TRACE] set_girl_sprite called with pose=standing for %s while in sex scene!\n%s" % (girl.Id, _stack))

        if pose in ("laying_down", "laying_anal") and not _girl_in_sex_scene(girl):
            import traceback as _tb
            _stack = "".join(_tb.format_stack())
            print("[BUG_TRACE] set_girl_sprite called with pose=%s for %s OUTSIDE sex scene!\n%s" % (pose, girl.Id, _stack))

        state = sprite_state.setdefault(girl.Id, {})
        state["pose"] = pose

        for key in ("hair", "brows", "eyes", "mouth"):
            val = face_parts.get(key, None)
            if val is not None:
                state[key] = val

        # Override expression if girl is angry or sad (temp status)
        if pose == "standing" and not _girl_in_sex_scene(girl):
            if hasattr(girl, "has_temp_status") and girl.has_temp_status("angry"):
                _angry_expr = GIRL_POSE_EXPRESSIONS.get(girl.Id, {}).get("standing", {}).get("angry", {})
                if _angry_expr:
                    for _k, _v in _angry_expr.items():
                        state[_k] = _v
            elif hasattr(girl, "has_temp_status") and girl.has_temp_status("sad"):
                _sad_expr = GIRL_POSE_EXPRESSIONS.get(girl.Id, {}).get("standing", {}).get("sad", {})
                if _sad_expr:
                    for _k, _v in _sad_expr.items():
                        state[_k] = _v

        # Skip rendering if suppressed (phone call etc.)
        if girl.Id in _sprite_suppressed:
            return

        attrs = _build_attributes_for_girl(girl, pose)

        if pose == "standing":
            _arm_attrs = [a for a in attrs if a.startswith("arm") or a.startswith("over_")]
            print("[SET_SPRITE] %s standing arm/over attrs=%s" % (girl.Id, str(_arm_attrs)))
            _full_img = "%s standing" % girl.Id
            if attrs:
                _full_img += " " + " ".join(attrs)
            print("[SHOW_CMD] %s" % _full_img)

        # Cache attrs for HJ so the expression cycle can reuse them
        if pose == "handjob":
            store._hj_attrs = list(attrs)

        # Map pose string to layeredimage name (e.g. reverse_cowgirl → rcg)
        _pose_img = {"reverse_cowgirl": "rcg", "reverse_cowgirl_anal": "rcg", "doggy": "doggy", "full_nelson": "fn", "full_nelson_anal": "fn", "anal": "doggy", "laying_down": "laying", "laying_anal": "laying"}.get(pose, pose)
        img_name = "%s %s" % (girl.Id, _pose_img)
        # Safety net: one attribute per layeredimage group, so a builder mistake is a log line
        # ([ATTR_CONFLICT]) instead of Ren'Py's game-ending "attributes ... conflict" exception
        attrs = _dedupe_layered_attrs(img_name, attrs)
        if attrs:
            img_name += " " + " ".join(attrs)

        _show_kw = {"tag": girl.Id}
        if at_list is not None:
            _show_kw["at_list"] = at_list
        elif pose == "standing" and not _girl_in_sex_scene(girl):
            _saved_at = state.get("_last_at_list")
            if _saved_at:
                _show_kw["at_list"] = _saved_at
            else:
                _saved_slot = getattr(girl, "SpriteLoc", StageCenter)
                _SLOT_TF_MAP = {
                    StageLeft: [slot_left],
                    StageCenterLeft: [slot_center_left],
                    StageCenterRight: [slot_center_right],
                    StageRight: [slot_right],
                }
                _show_kw["at_list"] = _SLOT_TF_MAP.get(_saved_slot, [slot_center])
        if zorder is not None:
            _show_kw["zorder"] = zorder
            state["_zorder"] = zorder
        elif state.get("_zorder", 0) != 0:
            _show_kw["zorder"] = state["_zorder"]
        if pose == "standing":
            print("[ACTUAL_SHOW] %s  kw=%s" % (img_name, {k: str(v) for k, v in _show_kw.items()}))
            renpy.hide(girl.Id)
        renpy.show(img_name, **_show_kw)
        if "at_list" in _show_kw:
            state["_last_at_list"] = _show_kw["at_list"]
        renpy.restart_interaction()

        # Auto-start/stop standing blink
        if pose == "standing":
            start_standing_blink(girl)
        else:
            stop_standing_blink(girl)

    # ------------------------------------------------------------
    # Standing Arm Position
    # ------------------------------------------------------------
    def _set_standing_arm(girl_or_id, pos):
        girl = _resolve_girl(girl_or_id)
        if not girl:
            return
        pos = int(pos)
        if pos not in (0, 1, 2, 3, 4):
            pos = 1
        state = sprite_state.setdefault(girl.Id, {})
        old = state.get("arm_pos", 0)
        if old != pos and state.get("pose") == "standing":
            stop_standing_blink(girl)
            state["arm_pos"] = pos
            set_girl_sprite(girl, pose="standing")
            print("[STANDING_ARM] %s -> arm %d" % (girl.gid, pos))
        else:
            state["arm_pos"] = pos

    # ------------------------------------------------------------
    # Expression helpers (blush, cum attrs)
    # ------------------------------------------------------------
    def _normalize_blush_value(value):
        if value is None:
            return 0

        if isinstance(value, int):
            return max(0, min(value, 2))

        s = str(value).strip().lower()
        if s.startswith("blush"):
            s = s.replace("blush", "").replace("_", "")
        if s.isdigit():
            return max(0, min(int(s), 2))

        return 0

    def _attr_for_blush(girl):
        state = sprite_state.get(girl.Id, {})
        idx = state.get("blush", 0)
        if idx == 1:
            return "blush_1"
        elif idx == 2:
            return "blush_2"
        return "blush_0"

    # -- Cum helpers for standing --
    CUM_STANDING_MAP = {
        "body":     "cum_body_on",
        "boobs":    "cum_boobs_on",
        "legs":     "cum_legs_on",
        "dripping": "cum_dripping_on",
        "hand":     "cum_hand_on",
    }

    CUM_FACE_MAP = {
        "face": "cum_face_on",
        "mouth": "cum_mouth_on",
    }

    CUM_STANDING_ALIASES = {
        "back": "body",
    }

    def _cum_attrs_for_standing(girl):
        cum = set(t.lower() for t in getattr(girl, "Cum", []))
        for alias, canonical in CUM_STANDING_ALIASES.items():
            if alias in cum:
                cum.add(canonical)
        attrs = []
        for tag, attr_on in CUM_STANDING_MAP.items():
            if tag in cum:
                attrs.append(attr_on)
            else:
                attrs.append(attr_on.replace("_on", "_none"))
        return attrs

    def _cum_face_attrs_for_standing(girl):
        cum = [t.lower() for t in getattr(girl, "Cum", [])]
        attrs = []
        for tag, attr_on in CUM_FACE_MAP.items():
            if tag in cum:
                attrs.append(attr_on)
            else:
                attrs.append(attr_on.replace("_on", "_none"))
        return attrs

    # -- Cum helpers for handjob --
    CUM_HJ_BODY_MAP = {
        "boobs": "cum_boobs_on",
    }

    CUM_HJ_FACE_MAP = {
        "face": "cum_face_on",
    }

    def _cum_attrs_for_hj(girl):
        cum = [t.lower() for t in getattr(girl, "Cum", [])]
        attrs = []
        for tag, attr_on in CUM_HJ_BODY_MAP.items():
            if tag in cum:
                attrs.append(attr_on)
            else:
                attrs.append(attr_on.replace("_on", "_none"))
        return attrs

    def _cum_face_attrs_for_hj(girl):
        cum = [t.lower() for t in getattr(girl, "Cum", [])]
        attrs = []
        for tag, attr_on in CUM_HJ_FACE_MAP.items():
            if tag in cum:
                attrs.append(attr_on)
            else:
                attrs.append(attr_on.replace("_on", "_none"))
        return attrs

    # The store vars that hold the girl of each sex scene (the exclusive acts too: footjob, rimjob)
    SCENE_GIRL_VARS = ("_hj_girl", "_bj_girl", "_titjob_girl", "_cowgirl_girl", "_rcg_girl", "_doggy_girl", "_fn_girl",
                       "_laying_girl", "_scg_girl", "_srcg_girl", "_sdg_girl", "_ft_girl", "_rj_girl")

    def player_in_sex_scene():
        """A sex scene is on (any scene, any girl): the HUD and the campus overlays stay out of it."""
        return any(getattr(store, _v, None) is not None for _v in SCENE_GIRL_VARS)

    def _girl_in_sex_scene(girl):
        """Return True if girl is currently in any sex scene (sprites managed externally)."""
        gid = getattr(girl, "gid", None) or getattr(girl, "Id", None)
        if not gid:
            return False
        for var in SCENE_GIRL_VARS:
            ref = getattr(store, var, None)
            if ref is not None and (ref is girl or getattr(ref, "gid", None) == gid or getattr(ref, "Id", None) == gid):
                return True
        return False


    # ------------------------------------------------------------
    # Parser to accept both codes and attribute-style strings
    # ------------------------------------------------------------
    def _parse_clothing_input(code, slot):
        """
        slot: "over" | "chest" | "legs" | "panties" | "shoes"
        Accepts:
            "hoodie"                -> ( "hoodie", False )
            "over_hoodie"           -> ( "hoodie", False )
            "over_hoodie_up"        -> ( "hoodie", True )
            "panties_normal_down"   -> ( "normal", True )
            "none"/"off"/"null"     -> ( None, False )
        """
        if code is None:
            return None, False

        s = str(code).strip().lower()
        if s in ("none", "off", "null"):
            return None, False

        if "_" not in s:
            return s, False

        prefix, rest = s.split("_", 1)
        if prefix != slot:
            return s, False

        flag = False
        base = rest

        if slot in ("over", "chest", "legs") and rest.endswith("_up"):
            base = rest[:-3]
            flag = True
        elif slot == "panties" and rest.endswith("_down"):
            base = rest[:-5]
            flag = True

        if base in ("none", "", None):
            return None, False

        return base, flag

    # ------------------------------------------------------------
    # Outfit_Change – high-level clothing API
    # ------------------------------------------------------------
    def Outfit_Change(self, over=None, mid=None, chest=None, legs=None, panties=None, over_up=None, mid_up=None, chest_up=None, shoes=None, legs_down=None, panties_down=None, pose=None, refresh=True):
        debug_log("[DEBUG] Outfit_Change: gid=%s over=%s mid=%s chest=%s legs=%s panties=%s shoes=%s pose=%s refresh=%s" % (getattr(self, "gid", "?"), str(over), str(mid), str(chest), str(legs), str(panties), str(shoes), str(pose), str(refresh)))
        # -------- over --------
        if over is not None:
            base, flag = _parse_clothing_input(over, "over")
            self.Over = base   # the property setter keeps shower_state in sync with the towel (_sync_shower_towel)
            self.OverUp = bool(flag) if base else False

        # -------- mid --------
        if mid is not None:
            base, flag = _parse_clothing_input(mid, "mid")
            self.Mid = base
            self.MidUp = bool(flag) if base else False

        # -------- chest --------
        if chest is not None:
            base, flag = _parse_clothing_input(chest, "chest")
            self.Chest = base
            self.ChestUp = bool(flag) if base else False

        # -------- legs --------
        if legs is not None:
            base, flag = _parse_clothing_input(legs, "legs")
            self.Legs = base
            self.LegsDown = bool(flag) if base else False

        # -------- shoes --------
        if shoes is not None:
            base, flag = _parse_clothing_input(shoes, "shoes")
            self.Shoes = base

        # -------- panties --------
        if panties is not None:
            base, flag = _parse_clothing_input(panties, "panties")
            self.Panties = base
            self.PantiesDown = bool(flag) if base else False

        # explicit flag overrides
        if over_up is not None:
            self.OverUp = bool(over_up) if self.Over else False
        if mid_up is not None:
            self.MidUp = bool(mid_up) if self.Mid else False
        if chest_up is not None:
            self.ChestUp = bool(chest_up) if self.Chest else False
        if legs_down is not None:
            self.LegsDown = bool(legs_down) if self.Legs else False
        if panties_down is not None:
            self.PantiesDown = bool(panties_down) if self.Panties else False

        # Sync changed slots to clothes dict (builder reads clothes dict)
        if over is not None or over_up is not None:
            self.clothes["over"] = self.Over
            self.clothes_state["over"] = "up" if self.OverUp else "full"
        if mid is not None or mid_up is not None:
            self.clothes["mid"] = self.Mid
            self.clothes_state["mid"] = "up" if self.MidUp else "full"
        if chest is not None or chest_up is not None:
            self.clothes["chest"] = self.Chest
            self.clothes_state["chest"] = "up" if self.ChestUp else "full"
        if legs is not None or legs_down is not None:
            self.clothes["skirt"] = self.Legs
            self.clothes_state["skirt"] = "up" if self.LegsDown else "full"
        if panties is not None or panties_down is not None:
            self.clothes["panties"] = self.Panties
            self.clothes_state["panties"] = "down" if self.PantiesDown else "full"
        if shoes is not None:
            self.clothes["shoes"] = self.Shoes

        _sync_girl(self)

        if refresh and not _girl_in_sex_scene(self):
            pose = pose or getattr(self, "default_pose", "standing")
            # Preserve current slot position when refreshing clothes
            _slot = getattr(self, "SpriteLoc", None)
            if _slot == StageLeft:
                set_girl_sprite(self, pose=pose, at_list=[slot_left])
            elif _slot == StageRight:
                set_girl_sprite(self, pose=pose, at_list=[slot_right])
            elif _slot == StageCenter:
                set_girl_sprite(self, pose=pose, at_list=[slot_center])
            else:
                set_girl_sprite(self, pose=pose)

    # ------------------------------------------------------------
    # WearPreset
    # ------------------------------------------------------------
    def WearPreset(self, preset_name, apply_now=True, pose=None):
        # Don't override shower outfit when in showers
        _sh = getattr(self, "shower_state", None)
        if _sh and _sh != "dressed" and getattr(store, "CurrentLocation", "") in SHOWER_SPOTS:
            debug_log("[DEBUG] WearPreset: BLOCKED - gid=%s preset=%s (shower_state=%s)" % (getattr(self, "gid", "?"), preset_name, _sh))
            return
        debug_log("[DEBUG] WearPreset: gid=%s preset=%s apply_now=%s" % (getattr(self, "gid", "?"), preset_name, str(apply_now)))
        presets = OUTFIT_PRESETS.get(self.Id, {})
        cfg = presets.get(preset_name)
        if not cfg:
            return

        self.clothes["over"]    = cfg.get("over",    None)
        self.clothes["mid"]     = cfg.get("mid",     None)
        self.clothes["chest"]   = cfg.get("chest",   None)
        self.clothes["skirt"]   = cfg.get("legs", cfg.get("skirt", None))
        self.clothes["panties"] = cfg.get("panties", None)
        self.clothes["shoes"]   = cfg.get("shoes",   None)

        for k in self.clothes_state:
            self.clothes_state[k] = "full"

        # Sync legacy properties from clothes dict
        self.Over     = self.clothes.get("over")
        self.Mid      = self.clothes.get("mid")
        self.Chest    = self.clothes.get("chest")
        self.Legs     = self.clothes.get("skirt")
        self.Panties  = self.clothes.get("panties")
        self.Shoes    = self.clothes.get("shoes")
        self.OverUp     = False
        self.MidUp      = False
        self.ChestUp    = False
        self.LegsDown   = False
        self.PantiesDown = False

        self.CurrentOutfitPreset = preset_name
        _sync_girl(self)

        if apply_now:
            pose = pose or getattr(self, "default_pose", "standing")
            set_girl_sprite(self, pose=pose)

    def CanWear(self, slot, item_code):
        req = CLOTHING_INBT_REQ.get(self.Id, {}).get(slot, {}).get(item_code, 0)
        return self.Inbt >= req

    def RefreshSprite(self, pose=None, at_list=None):
        pose = pose or getattr(self, "default_pose", "standing")
        if pose in ("laying_down", "laying_anal"):
            import traceback as _tb_rs
            print("[BUG_TRACE] RefreshSprite called with pose=%s for %s" % (pose, getattr(self, "Id", "?")))
            _tb_rs.print_stack()
        set_girl_sprite(self, pose=pose, at_list=at_list)

    def ResetVisuals(self, pose="standing", at_list=None):
        if _girl_in_sex_scene(self):
            import traceback as _tb
            _stack = "".join(_tb.format_stack())
            print("[BUG_TRACE] ResetVisuals called for %s while in sex scene!\n%s" % (getattr(self, "Id", "?"), _stack))
        gid = getattr(self, "gid", self.Id)
        stop_standing_blink(self)
        renpy.hide("bj_penis")
        renpy.hide("%s_bj_head" % gid)
        renpy.hide("%s_bj_jaw" % gid)
        renpy.hide("%s blowjob" % gid)
        renpy.hide(gid)
        _hide_all_scene_layers(self)

        pose = pose or getattr(self, "default_pose", "standing")
        set_girl_sprite(self, pose=pose, at_list=at_list)

    def SetPantiesDown(self, down=True, pose=None, at_list=None):
        self.PantiesDown = bool(down) and bool(self.Panties)
        pose = pose or getattr(self, "default_pose", "standing")
        set_girl_sprite(self, pose=pose, at_list=at_list)

    def SetPantiesSide(self, side=True, pose=None, at_list=None):
        self.PantiesSide = bool(side) and bool(self.Panties)
        pose = pose or getattr(self, "default_pose", "standing")
        set_girl_sprite(self, pose=pose, at_list=at_list)

    def DisplacePanties(self, pose=None, at_list=None, refresh=True):
        """Rotate panties state: full -> side -> down.
        Skips 'side' if visually identical to 'full' in current pose.
        Pass refresh=False when caller manages sprite refresh (e.g. sex scenes)."""
        if not self.Panties:
            return
        current = self.clothes_state.get("panties", "full")
        gid = getattr(self, "gid", self.Id)
        item_cfg = CLOTHING_REGISTRY.get(gid, {}).get(self.Panties, {})
        supported = item_cfg.get("states", ["full"])

        # Check pose to detect visually identical states
        _pose = sprite_state.get(self.Id, {}).get("pose", "standing")
        pose_map = item_cfg.get("poses", {}).get(_pose, {})

        if current == "full":
            if "side" in supported:
                # Skip side if same visual as full in this pose
                if pose_map.get("full", []) == pose_map.get("side", []):
                    if "down" in supported:
                        self.clothes_state["panties"] = "down"
                else:
                    self.clothes_state["panties"] = "side"
            elif "down" in supported:
                self.clothes_state["panties"] = "down"
        elif current == "side":
            if "down" in supported:
                self.clothes_state["panties"] = "down"
        # "down" is max displacement — no further action

        if refresh and not _girl_in_sex_scene(self):
            pose = pose or getattr(self, "default_pose", "standing")
            set_girl_sprite(self, pose=pose, at_list=at_list)

    def SetOverUp(self, up=True, pose=None, at_list=None):
        self.OverUp = bool(up) and bool(self.Over)
        pose = pose or getattr(self, "default_pose", "standing")
        set_girl_sprite(self, pose=pose, at_list=at_list)

    def SetMidUp(self, up=True, pose=None, at_list=None):
        self.MidUp = bool(up) and bool(self.Mid)
        pose = pose or getattr(self, "default_pose", "standing")
        set_girl_sprite(self, pose=pose, at_list=at_list)

    def SetChestUp(self, up=True, pose=None, at_list=None):
        self.ChestUp = bool(up) and bool(self.Chest)
        pose = pose or getattr(self, "default_pose", "standing")
        set_girl_sprite(self, pose=pose, at_list=at_list)

    def SetLegsDown(self, down=True, pose=None, at_list=None):
        self.LegsDown = bool(down) and bool(self.Legs)
        pose = pose or getattr(self, "default_pose", "standing")
        set_girl_sprite(self, pose=pose, at_list=at_list)

    def has_collar_art(self):
        return getattr(self, "gid", "") in _COLLAR_GIRLS

    def SetCollar(self, on=True, pose=None, at_list=None):
        self.Collar = bool(on) and self.has_collar_art()
        pose = pose or getattr(self, "default_pose", "standing")
        set_girl_sprite(self, pose=pose, at_list=at_list)

    def SaveOutfit(self):
        debug_log("[DEBUG] SaveOutfit: gid=%s clothes=%s" % (getattr(self, "gid", "?"), str(self.clothes)))
        self._saved_outfit = {
            "clothes": dict(self.clothes),
            "clothes_state": dict(self.clothes_state),
            "Collar": self.Collar,
            # Legacy keys for DressUp_Sequence compatibility
            "Over": self.Over, "OverUp": self.OverUp,
            "Mid": self.Mid, "MidUp": self.MidUp,
            "Chest": self.Chest, "ChestUp": self.ChestUp,
            "Legs": self.Legs, "LegsDown": self.LegsDown,
            "Panties": self.Panties, "PantiesDown": self.PantiesDown,
            "Shoes": self.Shoes,
        }

    def RestoreOutfit(self, clear_saved=False):
        saved = getattr(self, "_saved_outfit", None)
        debug_log("[DEBUG] RestoreOutfit: gid=%s saved=%s current_clothes=%s" % (getattr(self, "gid", "?"), str(saved.get("clothes") if saved else None), str(self.clothes)))
        if not saved:
            return
        if "clothes" in saved:
            self.clothes = dict(saved["clothes"])
            self.clothes_state = {"over": "full", "mid": "full", "chest": "full", "skirt": "full", "panties": "full", "shoes": "full"}
            _sync_shower_towel(self)   # the dict was replaced wholesale, bypassing the over setter
        else:
            self.Over = saved.get("Over")
            self.Mid = saved.get("Mid")
            self.Chest = saved.get("Chest")
            self.Legs = saved.get("Legs")
            self.Panties = saved.get("Panties")
            self.Shoes = saved.get("Shoes")
            for k in self.clothes_state:
                self.clothes_state[k] = "full"
        self.Collar = saved.get("Collar", self.has_collar_art())
        if clear_saved:
            self._saved_outfit = None

    # Bind methods to Girl
    Girl.Outfit_Change  = Outfit_Change
    Girl.WearPreset     = WearPreset
    Girl.CanWear        = CanWear
    Girl.RefreshSprite  = RefreshSprite
    Girl.SetPantiesDown  = SetPantiesDown
    Girl.SetPantiesSide  = SetPantiesSide
    Girl.DisplacePanties = DisplacePanties
    Girl.SetOverUp      = SetOverUp
    Girl.SetMidUp       = SetMidUp
    Girl.SetChestUp     = SetChestUp
    Girl.SetLegsDown    = SetLegsDown
    Girl.has_collar_art = has_collar_art
    Girl.SetCollar      = SetCollar
    Girl.ResetVisuals   = ResetVisuals
    Girl.SaveOutfit     = SaveOutfit
    Girl.RestoreOutfit  = RestoreOutfit

    # ----------------------------------------------
    # Towel / shower outfit cleanup (single source of truth)
    # ----------------------------------------------
    def _clear_shower_outfit(girl):
        """Strip towel and shower state from a girl who is no longer in showers.
        Returns True if anything was cleaned."""
        _had_state = bool(getattr(girl, "shower_state", None))
        _had_towel = getattr(girl, "clothes", {}).get("over") == "towel"
        if not _had_state and not _had_towel:
            return False
        girl.shower_state = None
        girl.shower_outfit = None
        girl.Collar = girl.has_collar_art()
        if _had_towel:
            girl.WearPreset("casual", apply_now=False)
        debug_log("[TOWEL_CLEANUP] %s: cleared (had_state=%s had_towel=%s)" % (getattr(girl, "gid", "?"), _had_state, _had_towel))
        return True

    def _prepare_shower_leave(girl):
        """Save casual outfit to _saved_outfit, strip girl nude, clear shower state.
        Returns True if DressUp_Sequence should follow."""
        _sh = getattr(girl, "shower_state", None)
        if not _sh or _sh == "dressed":
            return False
        _preset = OUTFIT_PRESETS.get(girl.gid, {}).get("casual", {})
        if not _preset:
            _clear_shower_outfit(girl)
            return False
        girl._saved_outfit = {
            "clothes": {
                "over": _preset.get("over"),
                "mid": _preset.get("mid"),
                "chest": _preset.get("chest"),
                "skirt": _preset.get("legs", _preset.get("skirt")),
                "panties": _preset.get("panties"),
                "shoes": _preset.get("shoes"),
            },
            "clothes_state": {"over": "full", "mid": "full", "chest": "full", "skirt": "full", "panties": "full", "shoes": "full"},
            "Collar": girl.has_collar_art(),
            "Over": _preset.get("over"),
            "Mid": _preset.get("mid"),
            "Chest": _preset.get("chest"),
            "Legs": _preset.get("legs", _preset.get("skirt")),
            "Panties": _preset.get("panties"),
            "Shoes": _preset.get("shoes"),
        }
        girl.shower_state = None
        girl.shower_outfit = None
        girl.Collar = False
        girl.Outfit_Change(over="none", mid="none", chest="none", legs="none", panties="none", shoes="none")
        debug_log("[SHOWER_LEAVE] %s: stripped nude, _saved_outfit set for DressUp" % getattr(girl, "gid", "?"))
        return True

    # ----------------------------------------------
    # Location outfit enforcement (called by Set_Scene)
    # ----------------------------------------------
    def _enforce_location_outfit(girl):
        """Force the correct outfit for the current location.
        Showers: untouched (shower system manages).
        Pool: bikini if unlocked, casual otherwise.
        Everything else: casual."""
        loc = getattr(store, "CurrentLocation", "")
        gid = getattr(girl, "gid", getattr(girl, "Id", ""))
        debug_log("[ENFORCE_OUTFIT] called for %s  loc=%s  _bk_in_store=%s  clothes=%s" % (
            gid, loc, getattr(store, "bk_in_store", "MISSING"), str(getattr(girl, "clothes", {}))))

        if loc in SHOWER_SPOTS:
            debug_log("[ENFORCE_OUTFIT] %s: skipped (showers)" % gid)
            return

        if getattr(store, "bk_in_store", False):
            debug_log("[ENFORCE_OUTFIT] %s: skipped (_bk_in_store)" % gid)
            return

        # Clear stale scene save — girl is outside any scene at location transition
        girl._saved_outfit = None

        if getattr(girl, "shower_state", None):
            girl.shower_state = None
            girl.shower_outfit = None

        if loc == "pool":
            if getattr(girl, "_bikini_unlocked", False) and gid in OUTFIT_PRESETS and "pool" in OUTFIT_PRESETS[gid]:
                girl.WearPreset("pool", apply_now=False)
            else:
                girl.WearPreset("casual", apply_now=False)
            return

        girl.WearPreset("casual", apply_now=False)

    # ----------------------------------------------
    # Default outfits at startup: every girl with a casual preset. This is also the state a girl NEWER than a save
    # comes back to when it loads (_restore_girls resets her to the init baseline, _girl_baseline_capture), so she
    # has to arrive dressed. It used to name Gwen, Rogue and Tenny only: a 0.12.1 save loaded without Shion showed
    # her naked at her intro (author, 2026-10-06), and NTW started undressed too.
    # ----------------------------------------------
    for _g_startup in ALL_GIRLS:
        if "casual" in OUTFIT_PRESETS.get(_g_startup.Id, {}):
            _g_startup.WearPreset("casual", apply_now=False)
    del _g_startup


# ============================================================
# DressUp_Sequence – veste a garota peça por peça após cena
# ============================================================
label DressUp_Sequence(girl):

    $ _dress_saved = getattr(girl, "_saved_outfit", None)
    if _dress_saved is None:
        $ print("[DRESSUP] _saved_outfit is None for %s, returning" % getattr(girl, "gid", "?"))
        return

    python:
        _du_state = sprite_state.get(girl.Id, {})
        print("[DRESSUP] START girl=%s pose_in_state=%s showing=%s" % (
            girl.gid, _du_state.get("pose", "??"), renpy.showing(girl.Id)))
        print("[DRESSUP] _saved_outfit=%s current_clothes=%s" % (
            str({k: v for k, v in _dress_saved.items() if v}),
            str({k: v for k, v in girl.clothes.items() if v})))
        __import__("traceback").print_stack()

    # Check if any clothing was removed OR displaced during the scene
    python:
        _clothing_changed = False
        for _ck in ("Over", "Mid", "Chest", "Legs", "Panties", "Shoes"):
            if _dress_saved.get(_ck) and not getattr(girl, _ck, None):
                _clothing_changed = True
                break
        # Also check if any state was displaced (side/down/up)
        for _sk, _sv in girl.clothes_state.items():
            if _sv != "full" and girl.clothes.get(_sk):
                _clothing_changed = True
                break

    # Dressup dialogue — only if clothing was actually removed
    if _clothing_changed:
        $ _du_line = scene_pick_line("dressup", girl=girl)
        if _du_line:
            $ Say_Line(girl, _du_line)

    $ _dress_pose = getattr(girl, "default_pose", "standing")

    # 1) Panties (removed or displaced)
    if _dress_saved["Panties"] and (not girl.Panties or girl.clothes_state.get("panties") != "full"):
        python:
            girl.Panties = _dress_saved["Panties"]
            girl.clothes_state["panties"] = "full"
            girl.RefreshSprite(pose=_dress_pose)
        with dissolve
        pause 0.3

    # 2) Legs / skirt (removed or displaced)
    if _dress_saved["Legs"] and (not girl.Legs or girl.clothes_state.get("skirt") != "full"):
        python:
            girl.Legs = _dress_saved["Legs"]
            girl.clothes_state["skirt"] = "full"
            girl.RefreshSprite(pose=_dress_pose)
        with dissolve
        pause 0.3

    # 3) Chest (removed or displaced)
    if _dress_saved["Chest"] and (not girl.Chest or girl.clothes_state.get("chest") != "full"):
        python:
            girl.Chest = _dress_saved["Chest"]
            girl.clothes_state["chest"] = "full"
            girl.RefreshSprite(pose=_dress_pose)
        with dissolve
        pause 0.3

    # 3.5) Mid (removed or displaced)
    if _dress_saved.get("Mid") and (not girl.Mid or girl.clothes_state.get("mid") != "full"):
        python:
            girl.Mid = _dress_saved["Mid"]
            girl.clothes_state["mid"] = "full"
            girl.RefreshSprite(pose=_dress_pose)
        with dissolve
        pause 0.3

    # 4) Over (removed or displaced)
    if _dress_saved["Over"] and (not girl.Over or girl.clothes_state.get("over") != "full"):
        python:
            girl.Over = _dress_saved["Over"]
            girl.clothes_state["over"] = "full"
            girl.RefreshSprite(pose=_dress_pose)
        with dissolve
        pause 0.3

    # 5) Shoes
    if _dress_saved["Shoes"] and not girl.Shoes:
        python:
            girl.Shoes = _dress_saved["Shoes"]
            girl.RefreshSprite(pose=_dress_pose)
        with dissolve
        pause 0.3

    # Safety net: force-restore any clothing that should have been
    # restored but wasn't (guards against Ren'Py interaction-point
    # issues that can lose attribute changes between dissolve/pause).
    python:
        _any_missing = False
        for _sk in ("Over", "Mid", "Chest", "Legs", "Panties", "Shoes"):
            _sv = _dress_saved.get(_sk)
            if _sv and not getattr(girl, _sk, None):
                setattr(girl, _sk, _sv)
                _any_missing = True

        girl.Collar = _dress_saved.get("Collar", False)
        if girl.Panties:
            girl.PantiesDown = _dress_saved.get("PantiesDown", False)
        if girl.Over:
            girl.OverUp = _dress_saved.get("OverUp", False)
        if girl.Mid:
            girl.MidUp = _dress_saved.get("MidUp", False)
        if girl.Chest:
            girl.ChestUp = _dress_saved.get("ChestUp", False)
        if girl.Legs:
            girl.LegsDown = _dress_saved.get("LegsDown", False)

        if _any_missing:
            girl.RefreshSprite(pose=_dress_pose)

        girl._saved_outfit = None

    return


# ============================================================
# GirlCumming – visual orgasm event when girl.Lust reaches 100
# Intensity tiers: 1 (light), 2 (normal), 3 (hard)
# ============================================================
label GirlCumming(girl, act_type, pose, scene_override=None):

    $ pose = {"full_nelson_anal": "full_nelson", "anal": "doggy", "laying_anal": "laying_down", "reverse_cowgirl_anal": "reverse_cowgirl"}.get(pose, pose)
    $ _gc_tier = _calc_orgasm_intensity(girl, act_type)
    $ _gc_hard = (_gc_tier == 3)
    $ debug_log("[DEBUG] GirlCumming: %s %s tier=%d pose=%s stamina=%d" % (girl.gid, act_type, _gc_tier, pose, getattr(girl, "Stamina", 10)))
    # The turn of a canon femdom (femdom_turn.rpy): she came while HE was in control (his act, or his position in sex)
    if (scene_control(act_type) or (scene_control(pose) if act_type == "sex" else None)) == "him":
        $ femdom_turn_note(girl, "her_cum_his_act", act_type)

    # Freeze LD animation during orgasm (head uses laying_speed for transform)
    if pose == "laying_down":
        $ store._gc_prev_laying_speed = getattr(store, "laying_speed", 0)
        $ store.laying_speed = 0

    # 1) Screen shake — tier-scaled
    if _gc_tier == 3:
        call OrgasmPunch_hard from _call_OrgasmPunch_hard_gc
    elif _gc_tier == 2:
        call OrgasmPunch from _call_OrgasmPunch_gc
    else:
        call OrgasmPunch_light from _call_OrgasmPunch_light_gc

    # 2) Orgasm expression
    if _gc_hard:
        $ set_scene_expression(girl, renpy.random.choice(["ahegao", "ahegao_2"]), pose=pose, blush="3")
    else:
        $ set_scene_expression(girl, "cumming", pose=pose, blush="3")

    # 2b) O-face hold — let the expression register before dialogue
    if _gc_tier == 3:
        pause 1.5
    elif _gc_tier == 2:
        pause 1.2
    else:
        pause 0.8

    # 3) Orgasm dialogue — tier cascades: hard -> intense -> base
    $ _gc_scene = scene_override if scene_override else act_type
    if _gc_tier == 3:
        $ _gc_line = scene_pick_line("girl_cum_hard", scene=_gc_scene, girl=girl)
        if not _gc_line:
            $ _gc_line = scene_pick_line("girl_cum_intense", scene=_gc_scene, girl=girl)
        if not _gc_line:
            $ _gc_line = scene_pick_line("girl_cum", scene=_gc_scene, girl=girl)
    elif _gc_tier == 2:
        $ _gc_line = scene_pick_line("girl_cum_intense", scene=_gc_scene, girl=girl)
        if not _gc_line:
            $ _gc_line = scene_pick_line("girl_cum", scene=_gc_scene, girl=girl)
    else:
        $ _gc_line = scene_pick_line("girl_cum", scene=_gc_scene, girl=girl)
    if _gc_line:
        call _moan_say(girl, _gc_line) from _call_ms_gc_orgasm
    else:
        pause 1.5

    # 3b) Post-dialogue recovery pause
    if _gc_tier == 3:
        pause 1.0
    elif _gc_tier == 2:
        pause 0.8
    else:
        pause 0.5

    # If eyes were locked (caught masturbating), unlock and open eyes
    if store._cg_eyes_locked:
        $ _mast_presence_break(girl)
        $ Say_Line(girl, _("W-What?! You were watching me?!"))

    # 4) Lust floor (fatigue) + consume flags
    $ girl.Lust = _orgasm_lust_floor(girl)
    $ girl.add_stamina(-2 if _gc_hard else -1)
    if store._hard_cum_ready:
        $ store._hard_cum_ready = False
    $ store._edge_denial_count = 0

    # 5) Increment orgasm counter
    $ girl.Orgasms[act_type] = girl.Orgasms.get(act_type, 0) + 1
    $ store._session_girl_orgasms += 1
    $ store._session_orgasms_by_girl[girl.gid] = store._session_orgasms_by_girl.get(girl.gid, 0) + 1
    $ print("[SESSION_ORGASM] %s -> %d this session (by_girl=%s) stamina=%d lust_floor=%d" % (girl.gid, store._session_orgasms_by_girl[girl.gid], store._session_orgasms_by_girl, getattr(girl, "Stamina", 10), girl.Lust))
    $ count_slaps_orgasm(girl)   # "Make her count" (count_slaps.rpy): she loses the number
    if _gc_hard:
        $ girl.HardOrgasms = getattr(girl, "HardOrgasms", 0) + 1

    # 5c) Sugar mommy (Actions/sugar_mommy.rpy): her orgasm pays him, capped per scene. Silent popup, no say.
    $ sugar_payout_orgasm(girl, _gc_hard)

    # 5b) Sexuality spectrum shift: orgasm moves toward bi
    if girl.has_trait("lesbian") or girl.has_trait("bisexual"):
        python:
            _spec_shift = 3
            if _gc_hard:
                _spec_shift += 2
            if act_type == "anal":
                _spec_shift += 3
            shift_spectrum(girl, _spec_shift)
            girl.apply_spectrum_temp_shift(10)
            debug_log("[DEBUG] spectrum shift: -%d = %d (lesbian orgasm)" % (_spec_shift, girl.sexuality_spectrum))

    # 6) Update favorite act
    $ girl.UpdateFavoriteAct()

    # 7) Post-orgasm dialogue — tier cascades
    if _gc_tier == 3:
        $ _gpc_line = scene_pick_line("girl_post_cum_hard", scene=_gc_scene, girl=girl)
        if not _gpc_line:
            $ _gpc_line = scene_pick_line("girl_post_cum_intense", scene=_gc_scene, girl=girl)
        if not _gpc_line:
            $ _gpc_line = scene_pick_line("girl_post_cum", scene=_gc_scene, girl=girl)
    elif _gc_tier == 2:
        $ _gpc_line = scene_pick_line("girl_post_cum_intense", scene=_gc_scene, girl=girl)
        if not _gpc_line:
            $ _gpc_line = scene_pick_line("girl_post_cum", scene=_gc_scene, girl=girl)
    else:
        $ _gpc_line = scene_pick_line("girl_post_cum", scene=_gc_scene, girl=girl)
    if _gpc_line:
        call _moan_say(girl, _gpc_line) from _call_ms_gc_post

    # 7b) Fatigue effects based on remaining Stamina
    $ _gc_stam = getattr(girl, "Stamina", 10)
    if _gc_stam <= 1:
        $ set_scene_expression(girl, "pleasure_intense", pose=pose, blush="3")
        $ _fat_line = scene_pick_line("girl_orgasm_exhausted", scene=_gc_scene, girl=girl)
        if _fat_line:
            call _moan_say(girl, _fat_line) from _call_ms_gc_exhausted
        menu:
            "Keep going":
                pass
            "Let her rest":
                $ Change_Status(girl, "Love", 10)
                $ store._scene_force_end = True
                $ debug_log("[FATIGUE] player let %s rest, Love +10" % girl.gid)
    elif _gc_stam <= 3:
        $ set_scene_expression(girl, "pleasure_intense", pose=pose, blush="3")
        $ _fat_line = scene_pick_line("girl_orgasm_dazed", scene=_gc_scene, girl=girl)
        if _fat_line:
            call _moan_say(girl, _fat_line) from _call_ms_gc_dazed
    elif _gc_stam <= 5:
        $ set_scene_expression(girl, "pleasure", pose=pose, blush="2")

    $ _watcher_scene_comment("girl_orgasm")

    # 8) Forced creampie — she finishes, THEN ends the scene furious
    if store._forced_creampie_end_after_orgasm:
        $ store._forced_creampie_end_after_orgasm = False
        call _post_orgasm_forced_creampie_end(girl, act_type) from _call__post_orgasm_forced_creampie_end

    # Restore LD speed so resumed masturbation can re-animate
    if pose == "laying_down" and hasattr(store, "_gc_prev_laying_speed"):
        $ store.laying_speed = store._gc_prev_laying_speed

    return


# ════════════════════════════════════════════════════════════
# GIRL-INITIATED ESCALATION (centralized)
# Called from rub/tip ticks in all positions.
# Sets store._girl_esc_accepted = True if player accepts.
# ════════════════════════════════════════════════════════════

label _girl_escalation_check(girl, current_mode):
    $ store._girl_esc_accepted = False
    $ store._girl_esc_wants_anal = False

    if _is_on_cheat_path(girl):
        if current_mode == "rub" and (getattr(store, "_cheat_rub_just_done", False) or not _cheat_can_tip(girl)):
            $ debug_log("[GIRL_ESC] BLOCKED: rub->tip cheat path")
            return
        if current_mode == "tip" and (getattr(store, "_cheat_tip_just_done", False) or not _cheat_can_sex(girl)):
            $ debug_log("[GIRL_ESC] BLOCKED: tip->sex cheat path")
            return

    if not _girl_esc_roll(girl):
        return

    if current_mode == "rub":
        $ _gesc_check = tip_check(girl, skip_insistence=True)
        if not _gesc_check["accepted"]:
            return
    elif current_mode == "tip":
        python:
            _gesc_ap = getattr(girl, "_anal_preference", 0)
            _gesc_pos_anal = False
            if _gesc_ap >= 2:
                if getattr(store, "_doggy_girl", None) is girl and not getattr(store, "doggy_anal", False):
                    _gesc_pos_anal = True
                elif getattr(store, "_fn_girl", None) is girl and not getattr(store, "fn_anal", False):
                    _gesc_pos_anal = True
                elif getattr(store, "_laying_girl", None) is girl and not getattr(store, "laying_anal", False):
                    _gesc_pos_anal = True
            _gesc_want_anal = _gesc_pos_anal and (_gesc_ap >= 3 or renpy.random.random() < 0.6)
        if _gesc_want_anal:
            $ _gesc_check = anal_penetration_check(girl)
            if not _gesc_check["accepted"]:
                $ _gesc_check = sex_penetration_check(girl, skip_insistence=True)
                if not _gesc_check["accepted"]:
                    return
                $ _gesc_want_anal = False
            else:
                $ store._girl_esc_wants_anal = True
                $ debug_log("[GIRL_ESC] anal preference %d -> requesting anal" % _gesc_ap)
        else:
            $ _gesc_check = sex_penetration_check(girl, skip_insistence=True)
            if not _gesc_check["accepted"]:
                return

    # NPC watching: girl directs request to NPC
    $ _gesc_ntr = store._ntr_partner_watching and store._ntr_watching_npc
    if _gesc_ntr:
        $ _gesc_req_type = "penetration" if current_mode == "rub" else ("anal" if store._girl_esc_wants_anal else "full_sex")
        call _ntr_girl_ask_npc(girl, store._ntr_watching_npc, _gesc_req_type) from _call_ntr_ask_npc_esc
    else:
        $ set_scene_expression(girl, "lusty", blush="2")
        $ _gesc_lines = _girl_esc_get_lines(girl, "tip_to_anal" if store._girl_esc_wants_anal else current_mode)
        $ Say_Line(girl, _girl_esc_say_line(girl, renpy.random.choice(_gesc_lines)))

    if current_mode == "rub":
        if _gesc_ntr and store._ntr_npc_authorized:
            menu:
                "Insert the tip":
                    $ store._girl_esc_accepted = True
                    $ Say_Player(_("As you wish..."))
                    $ mark_intimacy(girl, "tip")
                    $ Change_Status(girl, "Obed", 5)
                    $ Change_Status(girl, "Inbt", 5)
                    python:
                        if not hasattr(girl, "escalation_history"):
                            girl.escalation_history = []
                        girl.escalation_history.append({"from": "rub", "to": "tip", "initiated_by": "girl"})
                        if not girl.flags.get("escalated_rub_to_tip", False):
                            girl.discover("escalated_rub_to_tip")
                        unlock_achievement("just_the_tip")
                    call _ntr_authorized_done(girl, store._ntr_watching_npc, "penetration") from _call_ntr_auth_done_esc_rub
                "Keep rubbing":
                    $ Say_Line(girl, _format_npc_line(store._ntr_watching_npc, renpy.random.choice([_("But... %(pp)s said it was okay..."), _("Why not? %(Pp)s already agreed...")])))
        elif _gesc_ntr and not store._ntr_npc_authorized:
            menu:
                "Insert the tip anyway":
                    $ store._girl_esc_accepted = True
                    $ mark_intimacy(girl, "tip")
                    $ Change_Status(girl, "Obed", 5)
                    $ Change_Status(girl, "Inbt", 5)
                    python:
                        if not hasattr(girl, "escalation_history"):
                            girl.escalation_history = []
                        girl.escalation_history.append({"from": "rub", "to": "tip", "initiated_by": "girl"})
                    call _ntr_agreement_broken(girl, store._ntr_watching_npc, "penetration") from _call_ntr_broken_esc_rub
                "Respect [_ntr_npc_poss] decision":
                    call _ntr_boundary_respected(girl, store._ntr_watching_npc) from _call_ntr_respected_esc_rub
        else:
            menu:
                "Insert the tip":
                    if _is_on_cheat_path(girl) and not _cheat_can_tip(girl):
                        $ _notify_cheat_heat(girl, "gate_tip", False)
                        $ Say_Line(girl, _("No... no, that's enough for today. We shouldn't go further right now..."))
                    else:
                        $ store._girl_esc_accepted = True
                        $ Say_Player(_("As you wish..."))
                        $ mark_intimacy(girl, "tip")
                        if _is_on_cheat_path(girl):
                            $ _advance_cheat_stage(girl, 2)
                        $ Change_Status(girl, "Obed", 5)
                        $ Change_Status(girl, "Inbt", 5)
                        python:
                            if not hasattr(girl, "escalation_history"):
                                girl.escalation_history = []
                            girl.escalation_history.append({"from": "rub", "to": "tip", "initiated_by": "girl"})
                            if not girl.flags.get("escalated_rub_to_tip", False):
                                girl.discover("escalated_rub_to_tip")
                            unlock_achievement("just_the_tip")
                # a sugar girl (sugar_mommy.rpy) pays for what SHE is asking: the mirror of the SubEvents charge
                "Charge her for it ($[_se_charge_now])" if sugar_active(girl) and not (_is_on_cheat_path(girl) and not _cheat_can_tip(girl)) and sugar_charge_quote(girl, "tip"):
                    $ Say_Player(_tl(_("You want more? That costs. $%d.")) % store._se_charge_now)
                    if sugar_charge_accepts(girl):
                        $ sugar_charge_paid(girl, "rub_tip")
                        $ Say_Line(girl, _("...Sent. You're terrible. Now DO it."))
                        $ store._girl_esc_accepted = True
                        $ mark_intimacy(girl, "tip")
                        if _is_on_cheat_path(girl):
                            $ _advance_cheat_stage(girl, 2)
                        $ Change_Status(girl, "Obed", 5)
                        $ Change_Status(girl, "Inbt", 5)
                        python:
                            if not hasattr(girl, "escalation_history"):
                                girl.escalation_history = []
                            girl.escalation_history.append({"from": "rub", "to": "tip", "initiated_by": "girl"})
                            if not girl.flags.get("escalated_rub_to_tip", False):
                                girl.discover("escalated_rub_to_tip")
                            unlock_achievement("just_the_tip")
                    else:
                        $ Say_Line(girl, _("...Not tonight. Don't push it."))
                "Keep rubbing":
                    call _femdom_refused_react(girl, "escalation") from _call_fdr_esc_rub
                    if not store._femdom_refused:
                        $ Say_Line(girl, _tl(renpy.random.choice(_GIRL_ESC_DENY_RUB)))

    elif current_mode == "tip":
        if _gesc_ntr and store._ntr_npc_authorized:
            menu:
                "Go all the way":
                    $ store._girl_esc_accepted = True
                "Stay at the tip":
                    $ Say_Line(girl, _format_npc_line(store._ntr_watching_npc, renpy.random.choice([_("But... %(pp)s said it was okay..."), _("Why not? %(Pp)s already agreed...")])))
                    $ Change_Status(girl, "Lust", 10)
        elif _gesc_ntr and not store._ntr_npc_authorized:
            menu:
                "Go all the way anyway":
                    $ store._girl_esc_accepted = True
                "Respect [_ntr_npc_poss] decision":
                    call _ntr_boundary_respected(girl, store._ntr_watching_npc) from _call_ntr_respected_esc_tip
        else:
            menu:
                "Go all the way":
                    $ store._girl_esc_accepted = True
                "Charge her for it ($[_se_charge_now])" if sugar_active(girl) and sugar_charge_quote(girl, ("anal" if getattr(store, "_girl_esc_wants_anal", False) else "sex")):
                    $ Say_Player(_tl(_("All the way? That costs. $%d.")) % store._se_charge_now)
                    if sugar_charge_accepts(girl):
                        $ sugar_charge_paid(girl, "escalation")
                        $ Say_Line(girl, _("...Done. Sent. Now stop making me wait."))
                        $ store._girl_esc_accepted = True
                    else:
                        $ Say_Line(girl, _("...Not tonight. Don't push it."))
                "Stay at the tip":
                    call _femdom_refused_react(girl, "escalation") from _call_fdr_esc_tip
                    if not store._femdom_refused:
                        $ Say_Line(girl, _tl(renpy.random.choice(_GIRL_ESC_DENY_TIP)))
                    $ Change_Status(girl, "Lust", 10)

    return


# Called by each position after _girl_escalation_check sets _girl_esc_accepted for tip->sex (or tip->anal).
# Handles condom check, accept dialogue, _scene_escalation, virgin, tracking.
# Sets store._girl_esc_condom_denied if cheat path condom refused.
# If store._girl_esc_wants_anal, escalates to anal instead of sex.
label _girl_esc_accept_sex(girl, position):
    $ store._girl_esc_condom_denied = False
    python:
        _gesc_is_virgin = girl.has_trait("virgin")
        _gesc_has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        _gesc_to_anal = getattr(store, "_girl_esc_wants_anal", False)
        _gesc_act = "anal" if _gesc_to_anal else "sex"

    if _gesc_to_anal:
        $ Say_Line(girl, _tl(renpy.random.choice(_GIRL_ESC_ACCEPT_ANAL)))
        $ _scene_escalation(girl, "anal", position)
    elif _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False):
        call condom_check(girl, True, "hard_deny") from _call_condom_check_girl_esc
        if store.condom_denied:
            $ store._girl_esc_condom_denied = True
            return
        $ Say_Line(girl, _tl(renpy.random.choice(_GIRL_ESC_ACCEPT_SEX_VIRGIN if _gesc_is_virgin else _GIRL_ESC_ACCEPT_SEX_NORMAL)))
        $ _scene_escalation(girl, "sex", position)
        if _gesc_is_virgin:
            call virgin_first_time(girl, position) from _call_virgin_first_time_girl_esc_cheat
    elif story_act_locked(girl, "raw"):
        # Her own ask never opens raw before her step does (the act "raw" = her surrender step,
        # feedback_story_lock_all_paths): rub/tip + her beg entered bare sex at step 2, skipping the
        # etiquette every other sex entry obeys (tester 2026-10-10). She asked for sex, and she is also
        # the one with the rule: same condom_check as the cheat branch (_condom_story_locked knows her
        # story), no condom around = no sex.
        call condom_check(girl, True, "hard_deny") from _call_condom_check_girl_esc_story
        if store.condom_denied:
            $ store._girl_esc_condom_denied = True
            return
        $ Say_Line(girl, _tl(renpy.random.choice(_GIRL_ESC_ACCEPT_SEX_VIRGIN if _gesc_is_virgin else _GIRL_ESC_ACCEPT_SEX_NORMAL)))
        $ _scene_escalation(girl, "sex", position)
        if _gesc_is_virgin:
            call virgin_first_time(girl, position) from _call_virgin_first_time_girl_esc_story
    else:
        $ Say_Line(girl, _tl(renpy.random.choice(_GIRL_ESC_ACCEPT_SEX_VIRGIN if _gesc_is_virgin else _GIRL_ESC_ACCEPT_SEX_NORMAL)))
        $ store._creampie_consent = "allowed"
        $ _scene_escalation(girl, "sex", position)
        if _gesc_is_virgin:
            call virgin_first_time(girl, position) from _call_virgin_first_time_girl_esc
        $ _track_raw_sex_start(girl)

    python:
        if not hasattr(girl, "escalation_history"):
            girl.escalation_history = []
        _esc_entry = {"from": "tip", "to": _gesc_act, "initiated_by": "girl"}
        if not _gesc_to_anal and _gesc_is_virgin:
            _esc_entry["lost_virginity"] = True
            girl.discover("escalated_lost_virginity")
        if _gesc_has_bf:
            _esc_entry["cheated"] = True
            girl.discover("escalated_cheated_bf")
        girl.escalation_history.append(_esc_entry)
        if not girl.flags.get("escalated_tip_to_sex", False):
            girl.discover("escalated_tip_to_sex")
        unlock_achievement("she_wants_it")
        girl.add_temptation(3)

    # NTR outcome for tip->sex escalation
    if store._ntr_partner_watching and store._ntr_watching_npc:
        if store._ntr_npc_authorized:
            call _ntr_authorized_done(girl, store._ntr_watching_npc, "full_sex") from _call_ntr_auth_done_esc_tip
        else:
            call _ntr_agreement_broken(girl, store._ntr_watching_npc, "full_sex") from _call_ntr_broken_esc_tip
    return

init 999 python:
    # End of init: every file has configured the girls. This is what a fresh launch looks like (_restore_girls).
    _girl_baseline_capture()
