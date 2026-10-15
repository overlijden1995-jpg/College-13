# ============================================================
# NPC Partner Visual Presence System
# Boyfriend/girlfriend NPCs that appear at locations
# ============================================================

default _npc_on_scene = None
default _npc_witness_check_done = False
default _npc_witness_npc = None
default _npc_witness_detected = False
default _npc_witness_scene_aborted = False

default npc_talk_girl = None
default npc_talk_cd = False
default npc_talk_fem = False

default _ntr_partner_watching = False
default _ntr_watching_npc = None
default _ntr_discovery_kick = False
default _ntr_tip_accepted = False
# Creampie confrontation needs the partner PHYSICALLY on scene. Both live as long as _session_cum.
default _ntr_spontaneous_raw_asked = False    # once per sex session: girl already asked NPC to go raw
default _ntr_creampie_witnessed_gid = None   # gid of the girl whose NTR partner was on scene for a forbidden creampie
default _ntr_session_watcher_gid = None      # girl_gid of the NTR partner who watched a scene of this sex session to its END (still in the room)
default _witness_watching = False
default _witness_girl = None
default _witness_join_available = False
default _gf_permission_accepted = False
default _gf_permission_mode = None
default _gf_permission_gf = None

init -998 python:

    NPC_PARTNERS = {}
    NPC_APPEAR_CHANCE = 1.0

    NPC_SPRITE_HEIGHT = 960     # the guest sprites' height; other NPC art is shown at it (FAMILY_SPRITES)

    for _i in range(1, 12):
        renpy.image("npc_male_%d" % _i, "images/characters/NPCs/Man/guest %d.png" % _i)
        renpy.image("npc_female_%d" % _i, "images/characters/NPCs/Woman/guest %d.png" % _i)

    _NPC_NAMES_MALE = [
        "James", "Ethan", "Lucas", "Noah", "Liam", "Mason",
        "Logan", "Alex", "Ryan", "Tyler", "Jake", "Dylan",
        "Kyle", "Marcus", "Derek", "Brandon", "Trevor", "Kevin",
        "Chad", "Brad", "Nathan", "Connor", "Owen", "Hunter",
    ]

    _NPC_NAMES_FEMALE = [
        "Emma", "Olivia", "Sophia", "Ava", "Mia", "Chloe",
        "Lily", "Zoe", "Hannah", "Ella", "Nora", "Grace",
        "Riley", "Aria", "Luna", "Hazel", "Ivy", "Stella",
        "Maya", "Ruby", "Violet", "Willow", "Jade", "Amber",
    ]

    # Canon partner names, keyed by (girl gid, partner gender). Used unless that person is already her ex.
    _NPC_CANON_NAMES = {("ntw", "female"): "Yukio"}

    # A random guest sprite for a new NPC partner (the family wears its own art, FAMILY_SPRITES: every guest is free)
    def npc_random_guest(gender="male"):
        return renpy.random.randint(1, 11)

    # Fixed guest sprite per girl — consistent partner appearance.
    _NPC_DEFAULT_GUEST = {"gwen": 6, "rogue": 3, "ntw": 10, "tenny": 8}

    class NPCPartner(object):

        def __init__(self, partner_id, girl_gid, gender="male", guest_number=None):
            self.partner_id = partner_id
            self.girl_gid = girl_gid
            self.gender = gender

            if guest_number is None:
                guest_number = npc_random_guest(gender)
            self.guest_number = guest_number

            girl = GIRL_BY_ID.get(girl_gid)
            _saved_name = getattr(girl, "_npc_partner_name", None) if girl else None
            # Her exes (Girl._reset_npc_partner_mirrors records them): a NEW partner never gets one of their names
            _ex_names = set(getattr(girl, "_npc_ex_names", None) or []) if girl else set()
            _canon_name = _NPC_CANON_NAMES.get((girl_gid, gender))
            _used = set()
            for _np in NPC_PARTNERS.values():
                # her own registered NPC is not "someone else": a second create for the same girl keeps the name
                if getattr(_np, "girl_gid", None) != girl_gid:
                    _used.add(_np.name)
            if _canon_name and (_saved_name == _canon_name or _canon_name not in _ex_names):
                self.name = _canon_name
                if girl:
                    girl._npc_partner_name = self.name
            elif _saved_name and _saved_name not in _used:
                self.name = _saved_name
            else:
                _pool = _NPC_NAMES_FEMALE if gender == "female" else _NPC_NAMES_MALE
                for _ag in ALL_GIRLS:
                    _sn = getattr(_ag, "_npc_partner_name", None)
                    if _sn and _ag.gid != girl_gid:
                        _used.add(_sn)
                _avail = [n for n in _pool if n not in _used and n not in _ex_names]
                if not _avail:
                    _avail = [n for n in _pool if n not in _ex_names] or list(_pool)
                self.name = _tl(_random.choice(_avail))
                if girl:
                    girl._npc_partner_name = self.name
                if _saved_name:
                    print("[NPC_PARTNER] %s had duplicate name '%s', reassigned to '%s'" % (girl_gid, _saved_name, self.name))
            self.Name = self.name
            self.gid = self.partner_id
            self.color = "#b0bec5"
            self.petname_for_player = None

            self.friendship_with_player = 200
            self.love_for_girl = 750
            self.suspicion = 0

            _saved_sched = getattr(girl, "_npc_partner_schedule", None) if girl else None
            if _saved_sched:
                self.schedule = _saved_sched
            else:
                self.schedule = self._generate_schedule()
                if girl:
                    girl._npc_partner_schedule = self.schedule

            _day = getattr(store, "Day", 1)
            _ti = getattr(store, "TimeIndex", 0)
            self.loc = self.get_scheduled_location(_day, _ti)

            self.traits = set()

            # Physical preference (used by ToD truths)
            _gf = GIRL_BY_ID.get(girl_gid)
            _gf_bust = getattr(_gf, "bust", "medium") if _gf else "medium"
            if _random.random() < 0.6:
                self.bust_pref = _gf_bust
            else:
                self.bust_pref = _random.choice(["small", "medium", "large"])

            debug_log("[NPC_PARTNER] Created %s: guest=%d gender=%s bust_pref=%s" % (
                self.partner_id, self.guest_number, self.gender, self.bust_pref))

        def _generate_schedule(self):
            girl = GIRL_BY_ID.get(self.girl_gid)
            if not girl or not hasattr(girl, "schedule"):
                return [["campus"] * 4 for _ in range(7)]

            _PUBLIC = ["campus", "pool", "gym", "classroom", "mall", "restaurant_restroom"]
            g_sched = girl.schedule
            npc_sched = []

            for day in range(7):
                row = []
                for ti in range(4):
                    g_loc = g_sched[day][ti]

                    if ti == 3:
                        if g_loc == getattr(girl, "home", "room") and renpy.random.random() < 0.70:
                            row.append(g_loc)
                        else:
                            row.append("campus")
                    elif g_loc in ("room", "showers"):
                        row.append(renpy.random.choice(_PUBLIC))
                    elif renpy.random.random() < 0.55:
                        row.append(g_loc)
                    else:
                        row.append(renpy.random.choice(_PUBLIC))
                npc_sched.append(row)

            return npc_sched

        def get_scheduled_location(self, day, time_index):
            weekday = (max(1, int(day)) - 1) % 7
            ti = max(0, min(3, int(time_index)))
            return self.schedule[weekday][ti]

        def update_location_for_time(self, day, time_index):
            _girl = GIRL_BY_ID.get(self.girl_gid)
            if _girl is not None and getattr(_girl, "_arguing_in_room", 0) == day:
                # She was caught today: both argue in HER room until the day ends. Read from the girl: NPC objects
                # are rebuilt on every load and never saved, only she is (_girl_save).
                self.loc = girl_home_loc(self.girl_gid)
                return
            _loc = self.get_scheduled_location(day, time_index)
            if _girl is not None and girl_is_away(_girl):
                # She is with her family giving birth. The partner who stands as the father (fooled, or the NTR
                # partner who said "I'll raise the kid") is there with her: the birth event has him texting
                # that he is heading to the hospital. Any other partner keeps his life, but never waits in her
                # EMPTY room (his schedule puts him there on most nights).
                if getattr(_girl, "_npc_paternity_claimed", False):
                    _loc = GIRL_AWAY_LOC
                elif _loc == getattr(_girl, "home", None):
                    _loc = "campus"
            self.loc = _loc

        def image_tag(self):
            return "npc_%s" % self.partner_id

        def image_name(self):
            prefix = "npc_female" if self.gender == "female" else "npc_male"
            return "%s_%d" % (prefix, self.guest_number)

        def show_sprite(self, transform):
            renpy.show(self.image_name(), tag=self.image_tag(), at_list=[transform], zorder=5)
            debug_log("[NPC_PARTNER] Showing %s (%s)" % (self.name, self.image_name()))

        def hide_sprite(self):
            renpy.hide(self.image_tag())

        def has_trait(self, trait_id):
            return trait_id in self.traits

        def add_trait(self, trait_id):
            self.traits.add(trait_id)

        def remove_trait(self, trait_id):
            self.traits.discard(trait_id)

        def change_friendship(self, amount):
            self.friendship_with_player = max(0, min(1000, self.friendship_with_player + int(amount)))
            _g = GIRL_BY_ID.get(self.girl_gid) if hasattr(self, "girl_gid") else None
            if _g:
                _g._npc_friendship = self.friendship_with_player

        def change_love(self, amount):
            self.love_for_girl = max(0, min(1000, self.love_for_girl + int(amount)))
            _g = GIRL_BY_ID.get(self.girl_gid) if hasattr(self, "girl_gid") else None
            if _g:
                _g._npc_love = self.love_for_girl

        def is_hostile(self):
            return self.friendship_with_player < 200

        def is_friendly(self):
            return self.friendship_with_player >= 500

    # ── Creation / Registry ──

    # Disposition of a random NPC partner: cumulative chance, first hit wins, no hit = neutral
    _NPC_DISPOSITION_ROLL = (("ntr", 0.25), ("proud", 0.50))

    def _npc_roll_partner_traits():
        """Random disposition + sub traits of a NEW NPC partner. Single source for create_npc_partner()
        (mirror unset) and the Randomize button of the NPC trait picker (script.rpy)."""
        _roll = renpy.random.random()
        _disp = next((_t for _t, _limit in _NPC_DISPOSITION_ROLL if _roll < _limit), None)
        _traits = set([_disp]) if _disp else set()
        _traits.update(_ntr_roll_sub_traits())
        return _traits

    def create_npc_partner(girl, gender="male"):
        partner_id = "npc_%s_%s" % ("gf" if gender == "female" else "bf", girl.gid)

        existing_num = getattr(girl, "_npc_guest_number", None)
        if existing_num is not None:
            guest_num = existing_num
        else:
            guest_num = _NPC_DEFAULT_GUEST.get(girl.gid) or npc_random_guest(gender)
            girl._npc_guest_number = guest_num

        npc = NPCPartner(partner_id, girl.gid, gender=gender, guest_number=guest_num)

        npc.friendship_with_player = getattr(girl, "_npc_friendship", 200)
        npc.love_for_girl = getattr(girl, "_npc_love", 750)
        npc.suspicion = getattr(girl, "_npc_suspicion", 0)

        _existing_traits = getattr(girl, "_npc_partner_traits", None)
        if _existing_traits is not None:
            npc.traits = set(_existing_traits)
        else:
            # unset = NEW partner (Girl._reset_npc_partner_mirrors): roll him / her
            npc.traits = _npc_roll_partner_traits()
            girl._npc_partner_traits = set(npc.traits)
            print("[NPC_PARTNER] %s (%s): rolled traits %s" % (npc.name, girl.gid, sorted(npc.traits)))

        # NTR boundary system attributes
        npc._ntr_active = getattr(girl, "_ntr_active", False)
        _bl = getattr(girl, "_ntr_boundary_level", None)
        if _bl is None:
            # unset = NEW partner: an NTR-born one rolls his limit (never for a lesbian's girlfriend, same
            # rule as the trait picker and _ntr_activate), anyone else starts at 1. Mirrored at once, or the
            # next rebuild (every load) would roll another level.
            _bl = _ntr_roll_boundary_level(gender) if (npc.has_trait("ntr") and not girl.has_trait("lesbian")) else 1
            girl._ntr_boundary_level = _bl
            print("[NPC_PARTNER] %s (%s): boundary level set to %d" % (npc.name, girl.gid, _bl))
        npc._ntr_boundary_level = _bl
        npc._ntr_boundary_bar = getattr(girl, "_ntr_boundary_bar", 0)

        NPC_PARTNERS[partner_id] = npc
        return npc

    def get_npc_partner_for(girl):
        if not girl.has_npc_partner():
            return None
        if not NPC_PARTNERS:
            rebuild_npc_partners()
        return NPC_PARTNERS.get(girl.npc_partner_id)

    def rebuild_npc_partners():
        NPC_PARTNERS.clear()
        for girl in ALL_GIRLS:
            _default_gn = _NPC_DEFAULT_GUEST.get(girl.gid)
            if _default_gn is not None and getattr(girl, "_npc_guest_number", None) != _default_gn:
                girl._npc_guest_number = _default_gn
            if girl.has_npc_partner():
                gender = "female" if girl.get_flag("partner_is_female") else "male"
                create_npc_partner(girl, gender=gender)
        debug_log("[NPC_PARTNER] rebuild: %d partners active" % len(NPC_PARTNERS))

    def update_all_npc_locations(day, time_index):
        for npc in NPC_PARTNERS.values():
            npc.update_location_for_time(day, time_index)

    def _npc_suspicion_daily_decay():
        for npc in NPC_PARTNERS.values():
            if getattr(npc, "_ntr_active", False):
                continue
            if getattr(npc, "suspicion", 0) > 0:
                npc.suspicion = max(0, npc.suspicion - 5)
                debug_log("[NPC_SUSPICION] %s decay -5 → %d" % (npc.name, npc.suspicion))

    def npc_debug(girl_or_gid=None):
        """Console helper: npc_debug(Gwen) or npc_debug("gwen") prints all NPC stats."""
        if girl_or_gid is None:
            for npc in NPC_PARTNERS.values():
                npc_debug(npc.girl_gid)
            if not NPC_PARTNERS:
                print("No NPC partners active.")
            return

        if isinstance(girl_or_gid, str):
            girl = GIRL_BY_ID.get(girl_or_gid.lower())
        else:
            girl = girl_or_gid
        if not girl:
            print("Girl not found: %s" % girl_or_gid)
            return

        npc = get_npc_partner_for(girl)
        if not npc:
            print("%s has no NPC partner." % girl.Name)
            return

        _fr = npc.friendship_with_player
        _fr_tier = "hostile" if _fr < 200 else "neutral" if _fr < 500 else "friendly"
        _lv = npc.love_for_girl
        _lv_tier = "low" if _lv < 400 else "medium" if _lv < 700 else "high"
        _ntr = getattr(npc, "_ntr_active", False)
        _bl = getattr(npc, "_ntr_boundary_level", 1)
        _bar = getattr(npc, "_ntr_boundary_bar", 0)
        _disc = getattr(girl, "_ntr_boundary_discovered", False)
        _susp = getattr(npc, "suspicion", 0)
        _catch = getattr(girl, "_npc_catch_pending", False)
        _fin_t = getattr(girl, "_financial_times", 0)
        _fin_a = getattr(girl, "_financial_attitude", 0) if callable(globals().get("_financial_attitude_stage")) else "?"

        lines = [
            "===== NPC DEBUG: %s (%s) =====" % (npc.Name, npc.partner_id),
            "Girl: %s | Gender: %s | Guest#: %d" % (girl.Name, npc.gender, npc.guest_number),
            "Location: %s" % npc.loc,
            "Traits: %s" % (", ".join(npc.traits) if npc.traits else "none"),
            "--- Stats ---",
            "Friendship: %d (%s)" % (_fr, _fr_tier),
            "Love for girl: %d (%s)" % (_lv, _lv_tier),
            "Suspicion: %d" % _susp,
            "--- NTR ---",
            "NTR active: %s | Boundary level: %d | Bar: %d" % (_ntr, _bl, _bar),
            "Girl discovered NTR: %s" % _disc,
            "--- Girl-side ---",
            "Catch pending: %s" % _catch,
            "Financial times: %d | Attitude stage: %s" % (_fin_t, _fin_a),
            "bf_loyalty: %d" % getattr(girl, "bf_loyalty", 0),
            "CheatAttitude: %d | CheatMaxTier: %d" % (getattr(girl, "CheatAttitude", 0), getattr(girl, "CheatMaxTier", 0)),
            "Cheat stage: %d | Heat: %d | Path: %d" % (getattr(girl, "_cheat_sex_stage", 0), getattr(girl, "_cheat_heat", 0), getattr(girl, "_cheat_escalation_path", 0)),
            "=============================",
        ]
        for l in lines:
            print(l)

    # ── NTR Boundary System ──

    _NTR_NON_PENETRATION = ("hj", "tj", "bj", "fj", "rj", "kiss", "rub", "masturbate")

    def _ntr_roll_boundary_level(gender):
        _r = renpy.random.randint(1, 100)
        if gender == "female":
            if _r <= 75:
                return 1
            if _r <= 90:
                return 2
            if _r <= 95:
                return 3
            return 4
        else:
            if _r <= 50:
                return 1
            if _r <= 75:
                return 2
            if _r <= 90:
                return 3
            return 4

    def _ntr_roll_sub_traits():
        _result = set()
        if renpy.random.random() < 0.30:
            _result.add("voyeur")
        if renpy.random.random() < 0.30:
            _result.add("camera_lover")
        return _result

    def _ntr_is_tip_mode():
        for _cfg in CUM_POSITION_CONFIG.values():
            _tv = _cfg.get("tip_mode_var")
            if _tv and getattr(store, _tv, False):
                return True
        return False

    def _ntr_act_within_boundary(position, boundary_level, condom_active=False, is_anal=False):
        if boundary_level >= 4:
            return True
        if position in _NTR_NON_PENETRATION:
            return True
        if _ntr_is_tip_mode():
            if getattr(store, "_ntr_tip_accepted", False):
                return True
            return boundary_level >= 2
        if boundary_level == 1:
            return False
        if is_anal:
            return False
        if boundary_level == 2:
            return condom_active
        if boundary_level == 3:
            return True
        return False

    def _ntr_boundary_level_label(level):
        if level == 1:
            return _tr("Non-penetration only")
        if level == 2:
            return _tr("Condom-protected sex")
        if level == 3:
            return _tr("Raw sex, no creampie or anal")
        return _tr("No limits")

    def _ntr_friendship_multiplier(npc):
        f = getattr(npc, "friendship_with_player", 200)
        if f >= 750:
            return 2.0
        if f >= 500:
            return 1.5
        if f >= 200:
            return 1.0
        if getattr(npc, "_ntr_active", False):
            return 2.0
        return 0.5

    def _ntr_is_hostile_mode(npc):
        return (getattr(npc, "_ntr_active", False) and
                getattr(npc, "friendship_with_player", 200) < 200)

    def _ntr_increase_boundary_bar(npc, girl, amount):
        if getattr(npc, "_ntr_boundary_level", 1) >= 4:
            return False
        _session_gain = getattr(npc, "_ntr_bar_session_gain", 0)
        _SESSION_CAP = 30
        if _session_gain >= _SESSION_CAP:
            debug_log("[NTR_BOUNDARY] %s session cap reached (%d/%d), ignoring +%d" % (npc.name, _session_gain, _SESSION_CAP, amount))
            return False
        _mult = _ntr_friendship_multiplier(npc)
        _final = int(amount * _mult)
        _final = min(_final, _SESSION_CAP - _session_gain)
        npc._ntr_bar_session_gain = _session_gain + _final
        npc._ntr_boundary_bar = getattr(npc, "_ntr_boundary_bar", 0) + _final
        if not getattr(girl, "_ntr_trust_discovered", False):
            girl._ntr_trust_discovered = True
            debug_log("[NTR_BOUNDARY] %s trust bar discovered by player" % girl.gid)
        debug_log("[NTR_BOUNDARY] %s bar +%d (base %d x%.1f) → %d" % (npc.name, _final, amount, _mult, npc._ntr_boundary_bar))
        if npc._ntr_boundary_bar >= 100:
            npc._ntr_boundary_level = min(4, getattr(npc, "_ntr_boundary_level", 1) + 1)
            npc._ntr_boundary_bar = 0
            girl._ntr_boundary_level = npc._ntr_boundary_level
            girl._ntr_boundary_bar = 0
            girl._ntr_levelup_pending = True
            if npc._ntr_boundary_level == 4:
                unlock_achievement("full_access")
            debug_log("[NTR_BOUNDARY] %s level up → %d" % (npc.name, npc._ntr_boundary_level))
            return True
        girl._ntr_boundary_bar = npc._ntr_boundary_bar
        return False

    def _ntr_girl_boundary_check(girl, violation_type):
        npc = get_npc_partner_for(girl)
        if npc is None or not getattr(npc, "_ntr_active", False):
            return {"outcome": "eager_allow", "score": 9999, "threshold": 0, "violation_type": violation_type}

        if girl.has_trait("cheater"):
            print("[NTR_GIRL_CHECK] %s cheater -> auto eager_allow" % girl.gid)
            return {"outcome": "eager_allow", "score": 9999, "threshold": 0, "violation_type": violation_type}

        _obed = getattr(girl, "Obed", 0)
        _lust = getattr(girl, "Lust", 0)
        _love = getattr(girl, "Love", 0)
        _npc_love = getattr(npc, "love_for_girl", 750)
        _bf_loyalty = getattr(girl, "bf_loyalty", 750)

        love_delta = _love - (_npc_love * 0.8)
        score = (_obed * 0.6) + (_lust * 3) + (love_delta * 0.3) - (_bf_loyalty * 0.2)

        if girl.has_trait("loyal"):
            score *= 0.5
        if girl.has_trait("cum_slut") and violation_type == "creampie":
            score += 150
        if girl.has_trait("hardcore_sex"):
            score += 80
        if girl.has_trait("cute_sex"):
            score -= 60

        _THRESHOLDS = {
            "penetration": 600,
            "raw_sex": 500,
            "creampie": 450,
            "anal": 650,
        }
        T = _THRESHOLDS.get(violation_type, 500)

        if score < T:
            outcome = "respect"
        elif score < T + 100:
            outcome = "guilty_allow"
        else:
            outcome = "eager_allow"

        print("[NTR_GIRL_CHECK] %s type=%s score=%.0f T=%d outcome=%s obed=%d lust=%d love=%d npc_love=%d loyalty=%d" % (
            girl.gid, violation_type, score, T, outcome, _obed, _lust, _love, _npc_love, _bf_loyalty))

        return {"outcome": outcome, "score": int(score), "threshold": T, "violation_type": violation_type}

    def _ntr_condom_rule_holds(girl):
        """Her partner's level-2 rule (condom required) keeps the condom on right now: he is watching at level 2,
        or she knows the rule (_ntr_active_discovered) and respects it (the raw_sex check condom_check made her
        pass before the scene). Read where the condom could come off without condom_check: her own rip attempt
        (_sex_scene_tick) and the post-cum "Ask to go raw" choice (_post_cum_condom_menu)."""
        _watch_npc = getattr(store, "_ntr_watching_npc", None)
        if getattr(store, "_ntr_partner_watching", False) and _watch_npc is not None and getattr(_watch_npc, "_ntr_boundary_level", 1) == 2:
            return True
        if _ntr_active_discovered(girl) and getattr(get_npc_partner_for(girl), "_ntr_boundary_level", 1) == 2:
            return _ntr_girl_boundary_check(girl, "raw_sex")["outcome"] == "respect"
        return False

    _NTR_GIRL_LINE_TRAITS = ("anal_lover", "cum_slut", "hate_cum", "femdom", "submissive", "hardcore_sex", "cute_sex", "loyal")

    def _ntr_girl_line(pool, girl):
        """Her line from a trait-keyed NTR pool: the first trait she has that the pool speaks for (an eager trait
        she is still discovering only through its discovery key: trait_line_keys), else "_default"."""
        for t in _NTR_GIRL_LINE_TRAITS:
            if girl.has_trait(t):
                for _k in trait_line_keys(girl, t):
                    if _k in pool:
                        return _tl(renpy.random.choice(pool[_k]))
        return _tl(renpy.random.choice(pool.get("_default", ["..."])))

    def _ntr_say_boundary_line(girl, pool):
        _line = _ntr_girl_line(pool, girl)
        Say_Line(girl, _format_partner_line(girl, _line))

    def _ntr_save_state(npc, girl):
        girl._ntr_active = getattr(npc, "_ntr_active", False)
        girl._ntr_boundary_level = getattr(npc, "_ntr_boundary_level", 1)
        girl._ntr_boundary_bar = getattr(npc, "_ntr_boundary_bar", 0)
        girl._npc_friendship = getattr(npc, "friendship_with_player", 200)
        girl._npc_love = getattr(npc, "love_for_girl", 750)
        girl._npc_suspicion = getattr(npc, "suspicion", 0)

    def _ntr_get_scene_state():
        _girl = None
        _pos = None
        _anal = False
        _condom = False
        for _prefix, _var, _pname in [
            ("dg_", "_doggy_girl", "doggy"),
            ("cowgirl_", "_cowgirl_girl", "cowgirl"),
            ("rcg_", "_rcg_girl", "reverse_cowgirl"),
            ("fn_", "_fn_girl", "full_nelson"),
            ("ld_", "_laying_girl", "laying_down"),
            ("hj_", "_hj_girl", "hj"),
            ("bj_", "_bj_girl", "bj"),
            ("titjob_", "_titjob_girl", "tj"),
            ("ft_", "_ft_girl", "fj"),
            ("rj_", "_rj_girl", "rj"),
        ]:
            _g = getattr(store, _var, None)
            if _g is not None:
                _girl = _g
                _pos = _pname
                break
        if _pos == "doggy" and getattr(store, "doggy_anal", False):
            _anal = True
            _pos = "anal"
        elif _pos == "full_nelson" and getattr(store, "fn_anal", False):
            _anal = True
        elif _pos == "laying_down" and getattr(store, "laying_anal", False):
            _anal = True
        elif _pos == "reverse_cowgirl" and getattr(store, "rcg_anal", False):
            _anal = True
        _condom = getattr(store, "condom_active", False)
        return _girl, _pos, _anal, _condom

    def _ntr_scene_end_bonus():
        if not store._ntr_partner_watching:
            return
        _npc = store._ntr_watching_npc
        if _npc is None:
            return
        _girl = GIRL_BY_ID.get(getattr(_npc, "girl_gid", ""))
        if _girl is None:
            return
        _base = 15 if _npc.has_trait("voyeur") else 10
        _ntr_increase_boundary_bar(_npc, _girl, _base)
        unlock_achievement("cuckold_show")
        debug_log("[NTR_SCENE_END] %s watched full scene, bar +%d (base, before mult)" % (_npc.name, _base))

    def _ntr_npc_leaves_scene(npc, girl):
        """Clear ALL watcher state when NPC leaves the scene via any NTR exit path.
        Called from: discovery (within/violation), boundary violation (stop/continue),
        tease degrade storm-out, creampie violation (bl==3)."""
        store._ntr_partner_watching = False
        store._ntr_watching_npc = None
        store._ntr_session_watcher_gid = None
        store._npc_witness_check_done = False
        store._npc_on_scene = None
        npc._ntr_bar_session_gain = 0
        npc.loc = "away" if girl.home == store.CurrentLocation else girl.home
        print("[NTR_EXIT] %s left scene, watcher state cleared" % npc.name)

    # ── Girl Ask NPC (partner watching) ──

    _NTR_ASK_BAR_GAIN = {
        "condom_remove": 10,
        "creampie": 12,
        "penetration": 8,
        "full_sex": 8,
        "anal": 15,
    }

    _NTR_ASK_REQUIRED_LEVEL = {
        "condom_remove": 3,
        "creampie": 4,
        "penetration": 2,
        "full_sex": 2,
        "anal": 4,
        "condom_remove": 3,
    }

    def _npc_calc_authorize_chance(npc, request_type):
        _level = getattr(npc, "_ntr_boundary_level", 1)
        _req = _NTR_ASK_REQUIRED_LEVEL.get(request_type, _level + 1)

        if _level >= _req:
            return 100
        if _req > _level + 1:
            return 0

        _bar = getattr(npc, "_ntr_boundary_bar", 0)
        _base = _bar * 0.6

        if npc.has_trait("voyeur"):
            _base += 20
        _f = getattr(npc, "friendship_with_player", 200)
        if _f >= 500:
            _base += 10
        elif _f < 200:
            if _ntr_is_hostile_mode(npc):
                _base -= 5
            else:
                _base -= 20

        return min(90, max(5, int(_base)))

    def _npc_authorize_roll(npc, request_type):
        _chance = _npc_calc_authorize_chance(npc, request_type)
        _roll = renpy.random.randint(1, 100)
        _result = _roll <= _chance
        debug_log("[NTR_ASK_NPC] %s authorize roll: chance=%d%% roll=%d result=%s request=%s" % (
            npc.name, _chance, _roll, _result, request_type))
        return _result

    def _npc_say_response(npc, girl, pool, request_type):
        _f = getattr(npc, "friendship_with_player", 200)
        if _f >= 500:
            _tier = "friendly"
        elif _f >= 200:
            _tier = "neutral"
        elif _ntr_is_hostile_mode(npc):
            _tier = "hostile_ntr"
        else:
            _tier = "hostile"
        _key = (request_type, _tier)
        _lines = pool.get(_key, pool.get((request_type, "hostile"), pool.get((request_type, "neutral"), [_("...")])))
        _line = _tl(renpy.random.choice(_lines))
        _line = _format_npc_line(npc, _line, girl)
        _npc_char = Character(npc.Name, who_color=getattr(npc, "color", "#b0bec5"))
        renpy.say(_npc_char, _line)

    def _npc_poss(npc):
        return _tr("her_poss") if getattr(npc, "gender", "male") == "female" else _tr("his")

    def _npc_pp(npc):
        return _tr("she") if getattr(npc, "gender", "male") == "female" else _tr("he")

    def _npc_Pp(npc):
        return _tr("She") if getattr(npc, "gender", "male") == "female" else _tr("He")

    # Menu captions about an NPC partner, by gender. WHOLE captions instead of a pronoun spliced in:
    # each language keeps its own word order (ES "Ignorarlo" / "Ignorarla") and both English strings
    # are already translated, so never add an old/new pair for them (duplicate `old` crashes Ren'Py).
    _NPC_MENU_CAPTIONS = {
        "ignore": {"male": _("Ignore him"), "female": _("Ignore her")},
    }

    def _npc_menu_caption(npc, key):
        """Translated menu caption about this NPC partner, picked by npc.gender."""
        _g = getattr(npc, "gender", "male")
        _by_gender = _NPC_MENU_CAPTIONS.get(key, {})
        _cap = _by_gender.get(_g, _by_gender.get("male", key))
        print("[NPC-CAPTION] key=%s npc=%s gender=%s -> %s" % (key, getattr(npc, "Name", "?"), _g, _cap))
        return _tl(_cap)

    # ── Gossip System ──

    def _npc_friendship_tier(npc):
        f = npc.friendship_with_player
        if f < 200:
            return "hostile"
        if f < 500:
            return "neutral"
        return "friendly"

    def _npc_love_tier(npc):
        l = npc.love_for_girl
        if l < 400:
            return "low"
        if l < 700:
            return "medium"
        return "high"

    NPC_GOSSIP_REACTIONS = {
        # ── PRAISE ──
        ("praise", "hostile", "low"): {
            "mood": "neutral",
            "lines": [
                _("Yeah, cool."),
                _("Sure, whatever."),
            ],
            "friendship": 5, "love": 5,
        },
        ("praise", "hostile", "medium"): {
            "mood": "angry",
            "lines": [
                _("Why do you care so much about %s?"),
                _("What's your angle here?"),
            ],
            "friendship": 10, "love": 5,
        },
        ("praise", "hostile", "high"): {
            "mood": "angry",
            "lines": [
                _("Yeah... %s is great. What's it to you?"),
                _("I know %s is. I don't need YOU to tell me that."),
            ],
            "friendship": 10, "love": 10,
        },
        ("praise", "neutral", "low"): {
            "mood": "neutral",
            "lines": [
                _("Cool, I guess."),
                _("Yeah, %s is alright."),
            ],
            "friendship": 10, "love": 10,
        },
        ("praise", "neutral", "medium"): {
            "mood": "smile",
            "lines": [
                _("Thanks, I'll let %s know you said that."),
                _("That's nice of you to say."),
            ],
            "friendship": 15, "love": 15,
        },
        ("praise", "neutral", "high"): {
            "mood": "smile",
            "lines": [
                _("That's really nice of you. %s will be happy to hear that."),
                _("You're a good friend. I'll tell %s."),
            ],
            "friendship": 20, "love": 15,
        },
        ("praise", "friendly", "low"): {
            "mood": "sad",
            "lines": [
                _("Yeah... things have been weird between us though."),
                _("I appreciate that, but honestly, I don't know where we stand."),
            ],
            "friendship": 10, "love": 15,
        },
        ("praise", "friendly", "medium"): {
            "mood": "smile",
            "lines": [
                _("Hey, thanks man. That means a lot."),
                _("%s talks about you too, you know. Says you're a good guy."),
            ],
            "friendship": 20, "love": 20,
        },
        ("praise", "friendly", "high"): {
            "mood": "happy",
            "lines": [
                _("%s really is amazing, isn't she? I'm lucky."),
                _("I know, right? I don't know what I did to deserve %s."),
            ],
            "friendship": 25, "love": 20,
        },
        # ── SABOTAGE ──
        ("sabotage", "hostile", "low"): {
            "mood": "angry",
            "lines": [
                _("Are you trying to start something?"),
                _("Get the hell out of my face."),
            ],
            "friendship": -30, "love": -10,
        },
        ("sabotage", "hostile", "medium"): {
            "mood": "angry",
            "lines": [
                _("What the hell are you implying?"),
                _("You think I'm stupid? I see what you're doing."),
            ],
            "friendship": -40, "love": -15,
        },
        ("sabotage", "hostile", "high"): {
            "mood": "angry",
            "lines": [
                _("Stay the fuck away from %s."),
                _("If I catch you near %s again, we're going to have a problem."),
            ],
            "friendship": -50, "love": -10,
        },
        ("sabotage", "neutral", "low"): {
            "mood": "angry",
            "lines": [
                _("That's... none of your business."),
                _("Why are you telling me this?"),
            ],
            "friendship": -15, "love": -15,
        },
        ("sabotage", "neutral", "medium"): {
            "mood": "worried",
            "lines": [
                _("Wait, what? %s was at your place?"),
                _("That's... weird. %s didn't mention that."),
            ],
            "friendship": -15, "love": -25,
        },
        ("sabotage", "neutral", "high"): {
            "mood": "sad",
            "lines": [
                _("%s... forgot a shirt at your room? Why was %s there?"),
                _("I don't... that doesn't make sense. %s wouldn't do that."),
            ],
            "friendship": -10, "love": -30,
        },
        ("sabotage", "friendly", "low"): {
            "mood": "worried",
            "lines": [
                _("That's a weird thing to say, dude."),
                _("I don't really want to hear about that."),
            ],
            "friendship": -20, "love": -10,
        },
        ("sabotage", "friendly", "medium"): {
            "mood": "sad",
            "lines": [
                _("Huh... that doesn't sound like %s. Does it?"),
                _("You're messing with me, right? ...Right?"),
            ],
            "friendship": -20, "love": -30,
        },
        ("sabotage", "friendly", "high"): {
            "mood": "sad",
            "lines": [
                _("I thought you were cool, man. Why are you telling me this?"),
                _("...%s would never... but you wouldn't lie to me, would you?"),
            ],
            "friendship": -25, "love": -35,
        },
    }

    def npc_gossip_get_reaction(npc, gossip_type):
        f_tier = _npc_friendship_tier(npc)
        l_tier = _npc_love_tier(npc)
        key = (gossip_type, f_tier, l_tier)
        return NPC_GOSSIP_REACTIONS.get(key)

    def npc_gossip_format_line(line, girl_name):
        try:
            translated = _tl(line)
            return translated % tuple([girl_name] * translated.count("%s"))
        except Exception:
            return _tl(line)

    _NPC_STAT_COLORS = {
        "friendship_with_player": "#7ecbff",
        "love_for_girl": "#ff9e5e",
        "suspicion": "#ff5555",
    }
    _NPC_STAT_LABELS = {
        "friendship_with_player": "Friendship",
        "love_for_girl": "NPC Love",
        "suspicion": "Suspicion",
    }
    _NPC_STAT_YPOS = {
        "friendship_with_player": 0.43,
        "love_for_girl": 0.48,
        "suspicion": 0.53,
    }

    def Change_NPC_Status(npc, flavor, amount, xpos=None):
        old_value = getattr(npc, flavor, 0)
        if flavor == "friendship_with_player":
            npc.change_friendship(amount)
        elif flavor == "love_for_girl":
            npc.change_love(amount)
        elif flavor == "suspicion":
            _ntr_girl = GIRL_BY_ID.get(getattr(npc, "girl_gid", "")) if hasattr(npc, "girl_gid") else None
            if getattr(npc, "_ntr_active", False) and _ntr_girl and getattr(_ntr_girl, "_ntr_boundary_discovered", False):
                debug_log("[NPC_STATUS] %s suspicion change skipped (NTR discovered)" % npc.name)
                return
            npc.suspicion = max(0, min(100, old_value + amount))
        else:
            return
        new_value = getattr(npc, flavor, 0)
        delta = new_value - old_value
        if delta == 0:
            return
        color = _NPC_STAT_COLORS.get(flavor, "#ffffff")
        ypos = _NPC_STAT_YPOS.get(flavor, 0.45)
        label_text = _tr(_NPC_STAT_LABELS.get(flavor, flavor))
        prefix = "+" if delta > 0 else "-"
        value_for_popup = abs(int(delta))
        if xpos is None:
            xpos = 0.50
        tag = "stat_npc_%s" % flavor
        renpy.show_screen(
            "StatHolder",
            value=value_for_popup,
            prefix=prefix,
            color=color,
            xpos=xpos,
            ypos=ypos,
            label_text=label_text,
            hide_tag=tag,
            _tag=tag,
        )

    def npc_gossip_on_cooldown(npc):
        day = getattr(store, "Day", 1)
        return getattr(npc, "_gossip_cooldown_day", -1) == day

    def npc_gossip_set_cooldown(npc):
        npc._gossip_cooldown_day = getattr(store, "Day", 1)

    # ── NPC Confide Suspicion ──

    def _npc_can_confide(npc):
        if getattr(npc, "_confided_suspicion", False):
            return False
        if getattr(npc, "_ntr_active", False):
            return False
        if npc.friendship_with_player < 500:
            return False
        girl = GIRL_BY_ID.get(npc.girl_gid)
        if not girl:
            return False
        if girl_is_away(girl):   # not the week to confide that he thinks she is cheating
            return False
        if getattr(girl, "GirlCheatCount", 0) < 3:
            return False
        if npc.suspicion >= 60:
            return False
        _current_loc = getattr(store, "CurrentLocation", None)
        if _current_loc and getattr(girl, "loc", None) == _current_loc:
            return False
        return True

    NPC_CONFIDE_LINES = {
        "high": [
            _("Hey... can I ask you something? %s has been... distant lately. I don't know if I'm doing something wrong."),
            _("I need to talk to someone. %s barely looks at me anymore. Do you think something's going on?"),
            _("You're friends with %s, right? She's been acting different. Avoiding me. I don't know what to think."),
        ],
        "medium": [
            _("Something's off with %s. I can feel it. She's hiding something, I just can't figure out what."),
            _("I'm not stupid, man. %s has been coming home late, dodging my questions. What the hell is going on?"),
            _("Be honest with me. Have you noticed anything weird about %s lately?"),
        ],
        "low": [
            _("I think %s is seeing someone. I don't even care that much anymore, I just want to know."),
            _("Pretty sure %s is cheating on me. At this point I'm more tired than mad about it."),
            _("Look, I know things between me and %s haven't been great. But if she's messing around, I'd rather just know."),
        ],
    }

    NPC_CONFIDE_REASSURE_LINES = {
        "high": [
            _("Yeah... you're probably right. Thanks, man. I needed to hear that."),
            _("I hope so. I just love her, you know? I don't want to lose her."),
        ],
        "medium": [
            _("Maybe. I don't know. But thanks for hearing me out."),
            _("I guess you could be right. I'll try not to overthink it."),
        ],
        "low": [
            _("If you say so. Doesn't feel like nothing, though."),
            _("Sure. Whatever you say."),
        ],
    }

    NPC_CONFIDE_STOKE_LINES = {
        "high": [
            _("What? What do you mean? You've seen something?"),
            _("Wait, you noticed too? Oh god... what did you see?"),
        ],
        "medium": [
            _("I knew it. I KNEW something was off. What have you seen?"),
            _("Damn it. So it's not just in my head then."),
        ],
        "low": [
            _("Figures. At least I'm not crazy."),
            _("Yeah, that's what I thought. Whatever."),
        ],
    }

    NPC_CONFIDE_CONFESS_LINES = {
        "friendly": [
            _("You... what? You're joking, right? Tell me you're joking."),
            _("I... I trusted you. I actually trusted you. Get the hell away from me."),
        ],
        "neutral": [
            _("You son of a... I should've known. Get the FUCK away from me."),
            _("Are you serious right now? You have the nerve to tell me this to my face?"),
        ],
    }

    # ── NPC Chat Conversations (Phone) ──
    # Each entry: dict with "p" (player msg), "n" (npc msg), optional "p2"/"n2" (follow-up)
    # %(girl)s = girlfriend name

    _NPC_PHONE_CONVOS = {
        "hostile": [
            {"p": _("Hey"), "n": _("What?")},
            {"p": _("How's it going?"), "n": _("Busy.")},
            {"p": _("You around campus?"), "n": _("Why do you want to know?")},
            {"p": _("What's up"), "n": _("Don't text me.")},
            {"p": _("Hey, just wanted to chat"), "n": _("About what exactly?")},
        ],
        "neutral": [
            {
                "p": _("Hey, what are you up to?"), "n": _("Just studying. Nothing exciting."),
                "p2": _("Same. Campus is dead today."), "n2": _("Tell me about it."),
            },
            {
                "p": _("How's it going?"), "n": _("Not bad. Just got out of class."),
                "p2": _("Which one? The boring one?"), "n2": _("They're ALL boring haha"),
            },
            {
                "p": _("Doing anything this weekend?"), "n": _("Maybe hanging out with %(girl)s."),
            },
            {
                "p": _("Hey"), "n": _("Hey. What's going on?"),
                "p2": _("Just bored."), "n2": _("Same lol"),
            },
            {
                "p": _("Did you see what happened at the cafeteria?"), "n": _("No, what?"),
                "p2": _("Someone dropped a whole tray in front of everyone."), "n2": _("Haha classic"),
            },
        ],
        "friendly": [
            {
                "p": _("Yo!"), "n": _("Hey man! What's good?"),
                "p2": _("Wanna grab food later?"), "n2": _("Down! Hit me up when you're ready."),
            },
            {
                "p": _("Bro"), "n": _("What's up?"),
                "p2": _("Nothing, just saying what's up haha"), "n2": _("Haha you're dumb. But same, bored as hell"),
            },
            {
                "p": _("How's %(girl)s doing?"), "n": _("She's good, man. Thanks for asking!"),
                "p2": _("Tell her I said hi"), "n2": _("Will do! She'll appreciate that."),
            },
            {
                "p": _("Dude, tried that new place near campus?"), "n": _("Not yet! Is it any good?"),
                "p2": _("Yeah, the food is great."), "n2": _("We should go together sometime!"),
            },
            {
                "p": _("Hey, quick question"), "n": _("Shoot!"),
                "p2": _("What time is that thing on Friday?"), "n2": _("8 PM. Don't be late this time haha"),
            },
            {
                "p": _("Just got out of the gym"), "n": _("Nice! How was it?"),
                "p2": _("Brutal. I can barely move."), "n2": _("Haha, we should work out together sometime"),
            },
        ],
    }

    # ── NPC Chat Conversations (In-Person) ──
    # Each entry: dict with "p" (player narration), "n" (npc speaks), "a" (after narration, optional)
    # %(girl)s = girlfriend name, %(npc)s = npc name
    # %(Pp)s = He/She, %(pp)s = him/her

    _NPC_INPERSON_CONVOS = {
        "hostile": [
            {
                "p": _("You try to make small talk."),
                "n": _("What do you want? I see you around here all the time."),
                "a": _("%(Pp)s doesn't seem to trust you."),
            },
            {
                "p": _("You say hi and try to be friendly."),
                "n": _("...Hi. Did you need something?"),
                "a": _("%(Pp)s clearly wants you to leave."),
            },
            {
                "p": _("You make a comment about campus."),
                "n": _("Yeah, cool. Look, I have stuff to do."),
                "a": _("That went nowhere."),
            },
            {
                "p": _("You ask how things are going."),
                "n": _("Fine. Everything's fine. Why?"),
                "a": _("There's an edge to %(npc)s's words."),
            },
            {
                "p": _("You try to compliment something."),
                "n": _("Thanks... I guess? What are you after?"),
                "a": _("%(Pp)s watches you as you walk away."),
            },
        ],
        "neutral": [
            {
                "p": _("You ask about the classes."),
                "n": _("Boring as always. Can't wait for the weekend."),
                "a": _("You chat for a bit about campus life."),
            },
            {
                "p": _("You mention something that happened on campus."),
                "n": _("Ha, I heard about that too. This place is crazy sometimes."),
                "a": _("%(Pp)s seems to relax a little."),
            },
            {
                "p": _("You ask about %(girl)s."),
                "n": _("%(girl)s? She's good. Busy with her stuff as usual."),
                "a": _("A normal enough conversation."),
            },
            {
                "p": _("You ask if there's anything fun happening this weekend."),
                "n": _("Not sure yet. Might do something with %(girl)s."),
                "a": _("You nod and say goodbye."),
            },
            {
                "p": _("You complain about the campus food."),
                "n": _("Yeah, it's terrible. I miss actual cooking."),
                "a": _("You bond a little over shared complaints."),
            },
        ],
        "friendly": [
            {
                "p": _("You greet %(npc)s with a fist bump."),
                "n": _("Hey! Good to see you, man."),
                "a": _("You chat for a while. It feels like a genuine friendship."),
            },
            {
                "p": _("You ask what %(npc)s has been up to."),
                "n": _("%(girl)s and I went out last night. It was fun."),
                "a": _("%(Pp)s seems happy to share."),
            },
            {
                "p": _("You mention a new place that opened near campus."),
                "n": _("Oh yeah? We should check it out together!"),
                "a": _("%(Pp)s seems genuinely interested."),
            },
            {
                "p": _("You joke about something that happened in class."),
                "n": _("Ha! No way, I missed that? That's hilarious!"),
                "a": _("You both laugh about it for a while."),
            },
            {
                "p": _("You ask %(npc)s how things are with %(girl)s."),
                "n": _("She's great, man. I'm lucky to have her. Don't tell her I said that though."),
                "a": _("%(Pp)s grins."),
            },
            {
                "p": _("You ask %(npc)s if he wants to grab food."),
                "n": _("I'm starving! Let's go."),
                "a": _("You spend some time together."),
            },
        ],
    }

    # He is away WITH her (update_location_for_time put him at GIRL_AWAY_LOC): phone only, and no campus
    # small talk ("Campus is dead today", "Wanna grab food later?").
    _NPC_PHONE_CONVOS_WITH_HER = [
        {
            "p": _("Hey, how is it going over there?"),
            "n": _("Can't talk much. I'm with %(girl)s and the baby. It's a lot."),
        },
        {
            "p": _("Everything okay?"),
            "n": _("Yeah. %(girl)s is resting. I'll be back on campus in a few days."),
        },
    ]

    # Small talk about the baby with the partner who STANDS AS THE FATHER (child_npc_is_father: fooled by
    # Choice 4, or the NTR boundary 4 partner who said "I'll raise the kid"). medium -> state -> who can say it:
    # "any" = every such partner (can be a woman: no "dad"), "fooled" = only the man who BELIEVES the child is
    # his. Same shape as the convos above: phone p = what the player types, in person p = narration.
    _NPC_BABY_CONVOS = {
        "phone": {
            "expecting": {
                "any": [
                    {"p": _("How's %(girl)s holding up?"), "n": _("Tired, hungry, and beautiful. I'm learning to cook. Badly.")},
                    {"p": _("Ready for the baby?"), "n": _("Not even close. But we bought a crib, so that's something.")},
                ],
                "fooled": [
                    {"p": _("So, a dad soon, huh?"), "n": _("Can you believe it? Me, a dad. I keep saying it out loud.")},
                ],
            },
            "born": {
                "any": [
                    {"p": _("How's the little one doing?"), "n": _("Perfect. Loud, but perfect. %(girl)s's family sends pictures every day.")},
                    {"p": _("Do you get to see the baby much?"), "n": _("Every chance we get. I never want to leave.")},
                ],
                "fooled": [
                    {"p": _("Does the baby look like you?"), "n": _("Everyone says so. Same nose, same stubborn face.")},
                ],
            },
        },
        "inperson": {
            "expecting": {
                "any": [
                    {"p": _("You ask %(npc)s how %(girl)s is doing."), "n": _("She's doing great. I'm the nervous one, honestly."), "a": _("%(Pp)s laughs, a little too fast.")},
                    {"p": _("You ask if everything is ready for the baby."), "n": _("We're getting there. There's so much stuff to buy. Who knew?")},
                ],
                "fooled": [
                    {"p": _("You congratulate %(npc)s on the baby."), "n": _("Thanks, man. Best news of my life."), "a": _("%(Pp)s beams. You say nothing.")},
                ],
            },
            "born": {
                "any": [
                    {"p": _("You ask %(npc)s about the baby."), "n": _("Growing fast. %(girl)s and I go to visit every chance we get."), "a": _("%(Pp)s shows you a picture before you can say no.")},
                    {"p": _("You ask how %(girl)s is handling everything."), "n": _("Better than me. She's a natural.")},
                ],
                "fooled": [
                    {"p": _("You ask %(npc)s if fatherhood suits him."), "n": _("More than I ever thought. That kid is my whole world."), "a": _("You nod and keep your mouth shut.")},
                ],
            },
        },
    }
    _NPC_BABY_CONVO_CHANCE = 0.5      # the rest of the time he makes his usual small talk

    _NPC_BABY_CONVOS_MULTI = {
        "phone": {
            "any": [
                {"p": _("How are the kids doing?"), "n": _("Growing like weeds. %(girl)s's family has their hands full.")},
                {"p": _("Must be wild with more than one."), "n": _("You have no idea. But I wouldn't trade it.")},
            ],
        },
        "inperson": {
            "any": [
                {"p": _("You ask %(npc)s about the kids."), "n": _("They keep each other busy. I barely have to do anything."), "a": _("%(Pp)s grins, clearly exhausted.")},
            ],
        },
    }

    def _npc_baby_convos(npc, girl, medium):
        """Convos about the baby this partner can have right now, or []."""
        if girl is None or not child_npc_is_father(girl):
            return []
        if girl_is_mother(girl):
            _state = "born"
        elif (getattr(girl, "_pregnant", False) and getattr(girl, "_pregnancy_known", False)
              and getattr(girl, "_pregnancy_stage", 0) >= 2 and not getattr(girl, "_giving_birth", False)):
            _state = "expecting"
        else:
            return []
        _table = _NPC_BABY_CONVOS[medium][_state]
        _out = list(_table["any"])
        if child_father_fooled(girl) and getattr(npc, "gender", "male") == "male":
            _out += _table["fooled"]
        if _state == "born" and getattr(girl, "_children_count", 0) >= 2 and medium in _NPC_BABY_CONVOS_MULTI:
            _out += _NPC_BABY_CONVOS_MULTI[medium].get("any", [])
        return _out

    def _npc_convo_pool(npc, pool, medium="phone"):
        """While his girl is away (giving birth) he does not talk about her as if she were around ("We went
        out last night", "She's good, busy as usual"): convos that name her are dropped. The full pool comes
        back if nothing else is left. The partner who is away WITH her has a pool of his own.
        The partner who stands as the father talks about the baby half of the time (never a hostile one)."""
        _girl = GIRL_BY_ID.get(getattr(npc, "girl_gid", None))
        if _girl is not None and not girl_is_away(_girl) and _npc_friendship_tier(npc) != "hostile":
            _baby = _npc_baby_convos(npc, _girl, medium)
            if _baby and renpy.random.random() < _NPC_BABY_CONVO_CHANCE:
                print("[NPC_PARTNER] %s: small talk about the baby (%s, %d convos)" % (npc.name, medium, len(_baby)))
                return _baby
        if _girl is None or not girl_is_away(_girl):
            return pool
        if getattr(npc, "loc", None) == GIRL_AWAY_LOC:
            print("[NPC_PARTNER] %s: away with %s, small talk from there" % (npc.name, _girl.gid))
            return _NPC_PHONE_CONVOS_WITH_HER
        _quiet = [_c for _c in pool if not any("%(girl)s" in (_v or "") for _v in _c.values())]
        print("[NPC_PARTNER] %s: %s is away, %d of %d convos do not name her" % (npc.name, _girl.gid, len(_quiet), len(pool)))
        return _quiet or pool

    def _npc_pick_phone_convo(npc, girl_name):
        tier = _npc_friendship_tier(npc)
        pool = _npc_convo_pool(npc, _NPC_PHONE_CONVOS.get(tier, _NPC_PHONE_CONVOS["neutral"]), "phone")
        convo = renpy.random.choice(pool)
        result = {}
        for key in ("p", "n", "p2", "n2"):
            val = convo.get(key)
            if val:
                text = _tl(val)
                if "%(girl)s" in text:
                    text = text % {"girl": girl_name}
                result[key] = text
            else:
                result[key] = None
        return result

    def _npc_pick_inperson_convo(npc, girl_name, is_fem):
        tier = _npc_friendship_tier(npc)
        pool = _npc_convo_pool(npc, _NPC_INPERSON_CONVOS.get(tier, _NPC_INPERSON_CONVOS["neutral"]), "inperson")
        convo = renpy.random.choice(pool)
        # here %(pp)s is the OBJECT pronoun (him / her), %(Pp)s the subject
        fmt = gender_fmt(is_fem)
        fmt.update({"girl": girl_name, "npc": npc.name, "pp": fmt["po"]})
        result = {}
        for key in ("p", "n", "a"):
            val = convo.get(key)
            if val:
                text = _tl(val)
                if "%(" in text:
                    text = text % fmt
                result[key] = text
            else:
                result[key] = None
        return result

    def _npc_chat_friendship_gain(tier):
        if tier == "hostile":
            return 5
        elif tier == "neutral":
            return renpy.random.randint(10, 15)
        else:
            return renpy.random.randint(20, 25)

    def npc_phone_chat_on_cooldown(npc):
        day = getattr(store, "Day", 1)
        return getattr(npc, "_phone_chat_cooldown_day", -1) == day

    def npc_phone_chat_set_cooldown(npc):
        npc._phone_chat_cooldown_day = getattr(store, "Day", 1)

    def npc_phone_text(npc, text, msg_type="text"):
        """The NPC partner texts the PLAYER. NPC texts always live in the NPC's OWN thread (key =
        npc.gid == npc.partner_id) with sender = npc.gid, same as _ask_npc_phone_number and
        _ntr_activation_message_event. Never post an NPC line into the girl's thread: phone_chat_screen
        draws every non-player sender of a thread as that contact's bubble, so it reads as HER talking.
        Registers the contact so the thread can be opened from the phone."""
        _contacts = getattr(store.Player, "phone_npc_contacts", None)
        if _contacts is None:
            store.Player.phone_npc_contacts = set()
            _contacts = store.Player.phone_npc_contacts
        if npc.partner_id not in _contacts:
            _contacts.add(npc.partner_id)
            print("[NPC_PHONE] %s added to contacts (texted the player first)" % npc.Name)
        phone_add_msg(npc.gid, npc.gid, text, msg_type)
        print("[NPC_PHONE] %s -> player (thread=%s, type=%s)" % (npc.Name, npc.gid, msg_type))

    # PlayerData containers keyed by the NPC partner id (set = membership, dict = per-id data).
    # A future per-NPC store on the player goes HERE so a new partner never inherits it.
    _NPC_ID_KEYED_PLAYER_STORES = ("phone_npc_contacts", "phone_messages")

    def npc_partner_forget_identity(npc_id, reason=""):
        """A NEW person is taking this NPC partner id (ids are canonical per girl + gender, so a new
        boyfriend reuses the ex's id). What the PLAYER holds under that id belongs to the ex and must not
        show up under the new name: his number, his 1:1 thread, the girl + partner groups he was in, and
        the 'recorded by' tag of the videos he filmed. Called by Girl.set_npc_partner() for a new person
        only, never when the same ex comes back (Girl.restore_ex_npc_partner)."""
        _player = getattr(store, "Player", None)
        if _player is None or not npc_id:
            return
        _done = []
        for _name in _NPC_ID_KEYED_PLAYER_STORES:
            _box = getattr(_player, _name, None)
            if _box and npc_id in _box:
                if isinstance(_box, dict):
                    _box.pop(npc_id, None)
                else:
                    _box.discard(npc_id)
                _done.append(_name)
        _groups = getattr(_player, "phone_groups", None) or []
        _dead = [_g.get("id") for _g in _groups if npc_id in _g.get("members", [])]
        if _dead:
            _player.phone_groups = [_g for _g in _groups if _g.get("id") not in _dead]
            _gmsgs = getattr(_player, "phone_group_messages", None) or {}
            for _gid in _dead:
                _gmsgs.pop(_gid, None)
            _done.append("groups %s" % _dead)
        _retagged = 0
        for _vid in (getattr(_player, "recorded_videos", None) or []):
            if _vid.get("recorder_gid") == npc_id:
                _vid["recorder_gid"] = "ex_%s" % npc_id   # recorder_name keeps the ex's name; the new partner is NOT the recorder
                _retagged += 1
        if _retagged:
            _done.append("%d video recorder tag(s)" % _retagged)
        print("[NPC_PARTNER] forget identity %s (%s): %s" % (npc_id, reason, ", ".join(_done) or "nothing to forget"))

    # ── NPC Video Response Pools ──

    _NPC_VIDEO_UNRELATED = {
        ("hostile", "neutral"): [
            _("Why are you sending me this?"),
            _("I don't want to see this."),
            _("What the hell, man?"),
        ],
        ("hostile", "proud"): [
            _("Why are you sending me this?"),
            _("Keep your filth to yourself."),
        ],
        ("hostile", "ntr"): [
            _("Why are you sending me this?"),
            _("I didn't ask for this."),
        ],
        ("neutral", "neutral"): [
            _("Uh... okay? Not sure why you sent me this."),
            _("That's... something. Thanks, I guess?"),
            _("Interesting choice to share that."),
        ],
        ("neutral", "proud"): [
            _("Alright, cool. Not really my thing to share though."),
            _("A gentleman doesn't film these things, but you do you."),
        ],
        ("neutral", "ntr"): [
            _("Heh, nice. Where did you find a girl like that?"),
            _("Not bad. She looks like she's enjoying it."),
        ],
        ("friendly", "neutral"): [
            _("Damn, nice one! She's hot."),
            _("Ha, you dog. Good for you."),
            _("Wish I could film my girl like that. She'd kill me though."),
        ],
        ("friendly", "proud"): [
            _("Nice, man. I'd never film mine though, that's private."),
            _("Ha, not bad. My girl would murder me if I tried that."),
        ],
        ("friendly", "ntr"): [
            _("Holy shit, that's hot! I wish my girl would let me film her."),
            _("Damn... I'm jealous. My girl would never do something like that for me."),
            _("Bro, that's amazing. She really goes for it huh?"),
        ],
    }

    _NPC_VIDEO_PARTNER_HIDDEN = {
        ("low", "neutral"): [
            _("Haha nice. That hair reminds me of someone, small world."),
            _("Pretty hot video. Something about her looks familiar though..."),
        ],
        ("low", "proud"): [
            _("Heh. She kind of reminds me of someone, but my girl would never do something like this."),
            _("Nice I guess. Funny, she has similar hair to my girlfriend."),
        ],
        ("low", "ntr"): [
            _("Damn, she reminds me of someone... that'd be wild though."),
            _("Wait, she looks a bit like... nah, can't be. Hot though."),
        ],
        ("medium", "neutral"): [
            _("Wait... something about this feels familiar. Weird."),
            _("I don't know why, but this is making me uncomfortable."),
        ],
        ("medium", "proud"): [
            _("Something about this girl... no, it can't be. My girl would never."),
            _("This is... unsettling. She moves just like someone I know."),
        ],
        ("medium", "ntr"): [
            _("There's something about her that I can't put my finger on..."),
            _("She really reminds me of someone. Part of me hopes it is, honestly."),
        ],
        ("high", "neutral"): [
            _("Is that...? No, it can't be. Why did you send me this?"),
            _("I'm getting a really bad feeling about this video."),
        ],
        ("high", "proud"): [
            _("This better not be who I think it is. I swear to God."),
            _("Delete this. I don't want to see this. Something isn't right."),
        ],
        ("high", "ntr"): [
            _("I keep staring at this... she looks SO much like my girl. That'd be crazy though..."),
            _("Is that... no way. But if it was... damn."),
        ],
    }

    _NPC_VIDEO_PARTNER_EXPOSED = {
        "proud": [
            _("THAT'S MY GIRLFRIEND! What the fuck is wrong with you?! You're dead!"),
            _("Is that %s?! I'm going to fucking KILL you!"),
        ],
        "neutral": [
            _("What the fuck?! Is that %s?! What did you do?!"),
            _("Oh my god... that's %s. How could you send me this?!"),
        ],
        "ntr": {
            "_default": [
                _("Wait... is that %s? When was this? Tell me more."),
                _("That's... that's %s, isn't it? I should be angry but... when did this happen?"),
            ],
            "hj": [
                _("That's... %s giving you a handjob? Well... at least she's using her hands on someone."),
                _("Is that %s? A handjob, huh... I'm not even that mad. When did this happen?"),
            ],
            "bj": [
                _("Is that %s with your... in her mouth? Wow. I... wow. How long has this been going on?"),
                _("That's %s sucking you off? I should be furious but... part of me wants to know more."),
            ],
            "tj": [
                _("That's %s using her tits on you? I always wondered what that looked like..."),
                _("Is that... a titjob? From %s? Okay... I have questions."),
            ],
            "cowgirl": [
                _("She's riding you?! That's... that's %s on top of you. I can't stop watching this."),
                _("Is that %s riding you? The way she moves... I've never seen her like that."),
            ],
            "reverse_cowgirl": [
                _("That's %s riding you backwards? That's... actually a really hot angle."),
                _("Is that %s? Reverse cowgirl... she never does that with me. When was this?"),
            ],
            "doggy": [
                _("You're fucking %s from behind? I can see her face... she's enjoying it."),
                _("That's %s getting it from behind. The sounds she makes... damn."),
            ],
            "full_nelson": [
                _("You're holding %s up like that?! That's intense... she looks completely helpless."),
                _("Is that a full nelson? With %s?! She's... she's really taking it."),
            ],
            "anal": [
                _("That's... that's %s taking it in the ass? She never lets me anywhere near there."),
                _("Is that anal? With %s? I can't believe she's letting you do that."),
            ],
            "full_nelson_anal": [
                _("You're holding %s up and fucking her ass?! That's... I don't even know what to say."),
                _("Full nelson anal with %s? She looks like she can barely handle it... but she's not stopping you."),
            ],
            "reverse_cowgirl_anal": [
                _("That's %s riding you backwards... with it in her ass?! She never lets me anywhere near there."),
                _("Reverse cowgirl, and it's going in her ass? %s... I can't believe she's doing that for you."),
            ],
            "laying_down": [
                _("That's %s just laying there and taking it? She looks... completely into it."),
                _("Is that %s on her back? The way she's looking at you... she never looks at me like that."),
            ],
            "laying_anal": [
                _("She's taking it in the ass while laying down?! %s never let me try anything like that."),
                _("That's %s getting anal while just laying there? She looks like she's actually enjoying it."),
            ],
            "creampie": [
                _("Did you cum inside %s?! That's... that's insane. Does she know you're showing me this?"),
                _("A creampie?! Inside %s?! Part of me is furious... and part of me can't look away."),
            ],
            "masturbate": [
                _("Is that %s touching herself? For you? She never does that for me..."),
                _("That's %s masturbating? When did she become comfortable enough to do that with you?"),
            ],
        },
    }

    def _npc_suspicion_tier(npc):
        s = npc.suspicion
        if s < 30:
            return "low"
        if s <= 60:
            return "medium"
        return "high"

    def _npc_trait_key(npc):
        if npc.has_trait("proud"):
            return "proud"
        if npc.has_trait("ntr"):
            return "ntr"
        return "neutral"

    _NTR_VIDEO_WITHIN_LINES = [
        _("Nice. Keep it up."),
        _("I appreciate you sharing this."),
        _("Heh... not bad."),
        _("Thanks for keeping me in the loop."),
        _("Damn, she's really getting into it, huh?"),
        _("More of this, man. I like knowing what goes on."),
    ]

    _NTR_VIDEO_WITHIN_HIDDEN_LINES = [
        _("Cool video. Would be even better if I could see her face though."),
        _("Not bad. Can't really see her reaction, but I get the picture."),
        _("Thanks for sharing. Next time try to get her face in the shot."),
    ]

    _NTR_VIDEO_WITHIN_CAMERA_LINES = [
        _("Now THAT'S what I'm talking about. Send more."),
        _("Perfect angle. You're getting good at this."),
        _("I love these. Keep them coming."),
        _("Incredible shot. You really know how to film her."),
        _("That angle is perfect... I can see everything."),
    ]

    _NTR_VIDEO_WITHIN_CAMERA_HIDDEN_LINES = [
        _("Hot video... but I can't see her face. Show me her expression next time."),
        _("This is good, but film her face. The reaction is the best part."),
        _("Nice, but you're hiding the best part. I want to see her face when she moans."),
        _("Good stuff. But seriously, get her face in the shot next time."),
    ]

    _NTR_VIDEO_WITHIN_VOYEUR_LINES = [
        _("Damn... this makes me want to be in the room, not watching a screen."),
        _("Videos are cool but... you ever thought about letting me watch live?"),
        _("I keep replaying this. Would be way better in person though."),
        _("This is hot, but imagine how much better it'd be if I was right there watching."),
    ]

    _NTR_VIDEO_OUTSIDE_LINES = [
        _("What the hell? That's NOT what we agreed on!"),
        _("You crossed the line. We had a deal."),
        _("I trusted you. This was outside our agreement."),
        _("Are you serious right now? This is way beyond what I'm okay with."),
        _("You went too far. We're going to have a problem."),
    ]

    # ── Hostile NTR: Video reaction pools (mental confusion) ──

    _NTR_VIDEO_HOSTILE_WITHIN_LINES = [
        _("I watched it again. I hate myself for it."),
        _("Why do you keep sending me these? ...Don't stop."),
        _("I stared at this for twenty minutes. I'm losing my mind."),
        _("Every time I open one of these I want to smash my phone. And then I watch it again."),
        _("I don't want to see this. ...Send another one."),
    ]

    _NTR_VIDEO_HOSTILE_WITHIN_HIDDEN_LINES = [
        _("Can't even see her face and I'm still watching this on repeat. What's wrong with me?"),
        _("Show her face next time. ...I mean, don't send these at all. ...But if you do, show her face."),
        _("I can tell it's her even without seeing her face. I've memorized every inch of her body. ...God."),
    ]

    _NTR_VIDEO_HOSTILE_WITHIN_CAMERA_LINES = [
        _("Perfect angle. ...I mean, this is disgusting. ...But the angle is perfect."),
        _("I've watched this twelve times. I hate you. Send more."),
        _("This footage is... really good quality. ...I'm going to kill you. ...After I watch it one more time."),
    ]

    _NTR_VIDEO_HOSTILE_WITHIN_VOYEUR_LINES = [
        _("Seeing it on video isn't enough. I need to be there. ...I mean, I DON'T need to be there. ...Shit."),
        _("A video can't capture what it's like being in the room. Not that I'd want to be. ...Would I?"),
        _("I keep imagining being there, watching this live. Then I want to throw up. Then I watch the video again."),
    ]

    _NTR_VIDEO_HOSTILE_OUTSIDE_LINES = [
        _("You crossed the line! I should end this! ...But I won't. Just don't do it again. PLEASE."),
        _("That was too far. Way too far. ...Why did I watch the whole thing?"),
        _("I trusted you with rules and you broke them. ...I still watched all of it. What's wrong with me?"),
    ]

    # ── NTR known: next day she hears that her partner watched a video the player sent him ──
    # The partner is in on it (NTR active + boundary discovered), and camera_lover partners ASK for these:
    # no suspicion, no breakup processing, no "are you out of your mind?!". Context of the partner:
    #   "requested" = camera_lover (he asks for videos), "known" = he knows and set rules, "hostile" = hostile NTR
    _NTR_VIDEO_SEEN_STATS = {
        "requested": {"Inbt": 3},
        "known":     {"Love": -3, "Inbt": 3},
        "hostile":   {"Obed": 3, "Inbt": 3},
    }
    # ctx -> her trait ("cheater" / "loyal" / "_default") -> [(first text, second text), ...]
    _NTR_VIDEO_SEEN_GIRL_MSGS = {
        "requested": {
            "_default": [(_("%(pn)s showed me the video you sent %(po)s. %(Pp)s told me %(pp)s asked you for it."),
                          _("It's still strange knowing %(pp)s watches us. But I'm not mad. A deal is a deal."))],
            "cheater":  [(_("So %(pn)s got the video %(pp)s wanted. %(Pp)s watched it right next to me~"),
                          _("Keep sending them. %(Pp)s likes the show, and honestly, so do I."))],
            "loyal":    [(_("%(pn)s showed me the video. %(Pp)s said %(pp)s asked you to send it."),
                          _("I don't know how to feel about it yet. But it's what %(pp)s wants, so I won't blame you."))],
        },
        "known": {
            "_default": [(_("%(pn)s showed me the video you sent %(po)s."),
                          _("%(Pp)s already knows about us, so it's not the end of the world. Just warn me next time, okay?"))],
            "cheater":  [(_("%(pn)s showed me your video. %(Pp)s knows everything anyway, so whatever~"),
                          _("Next time pick a better angle of me."))],
            "loyal":    [(_("%(pn)s showed me the video. %(Pp)s knows about us, but seeing it is different."),
                          _("I'm not angry. Just give me a heads up before you send %(po)s something like that."))],
        },
        "hostile": {
            "_default": [(_("%(pn)s watched the video you sent. %(Pp)s looked like %(pp)s wanted to smash the phone."),
                          _("But %(pp)s didn't delete it. %(Pp)s never does."))],
        },
    }

    def _ntr_video_ctx(npc):
        """How an NTR-known partner relates to videos of his girl. Shared by the next-day texts and the group pool."""
        if _ntr_is_hostile_mode(npc):
            return "hostile"
        return "requested" if npc.has_trait("camera_lover") else "known"

    def _ntr_video_seen_next_day(girl):
        """She texts about the video her NTR-known partner watched. False when NTR is not active + known."""
        npc = get_npc_partner_for(girl)
        if npc is None or not _ntr_active_discovered(girl):
            return False
        _ctx = _ntr_video_ctx(npc)
        _pool = _NTR_VIDEO_SEEN_GIRL_MSGS[_ctx]
        _key = next((_t for _t in ("cheater", "loyal") if girl.has_trait(_t) and _t in _pool), "_default")
        for _st, _val in _NTR_VIDEO_SEEN_STATS.get(_ctx, {}).items():
            Change_Status(girl, _st, _val)
        if girl.gid in getattr(store.Player, "phone_contacts", set()):
            for _m in renpy.random.choice(_pool[_key]):
                phone_add_msg(girl.gid, girl.gid, _format_partner_line(girl, _m), "text")
        print("[NTR_VIDEO_SEEN] %s ctx=%s trait=%s" % (girl.gid, _ctx, _key))
        return True

    # ── Hostile NTR: Mini-dialogue exchanges during scenes ──

    def _ntr_act_to_category(act_type):
        if act_type in ("bj",):
            return "oral"
        if act_type in ("hj", "tj"):
            return "manual"
        return "penetration"

    def _ntr_get_current_speed():
        for attr in ("doggy_speed", "cowgirl_speed", "rcg_speed", "fn_speed",
                     "bj_speed", "hj_speed", "titjob_speed"):
            v = getattr(store, attr, 0)
            if v > 0:
                return v
        return 1

    _NTR_HOSTILE_MINI_DIALOGUES = {
        # ── Penetration (doggy, cowgirl, rcg, full_nelson) ──
        ("slow", "penetration"): {
            "npc": [
                _("Why are you doing this with me, babe? Stop it!"),
                _("Babe... please... I'm right here... don't do this..."),
                _("I can't believe you're letting him... please, stop..."),
            ],
            "girl": {
                "cum_slut": [
                    _("I'm sorry, his cock is too good, I can't stop this..."),
                    _("Baby, I'll make it up to you... just... not now..."),
                ],
                "hardcore": [
                    _("Then look away. But we both know you won't."),
                    _("If it bothers you so much, leave. ...Yeah, I didn't think so."),
                ],
                "cute": [
                    _("I'm sorry, baby... I really am... but it feels so good..."),
                    _("I don't want to hurt you... but I can't stop..."),
                ],
                "_default": [
                    _("I'm sorry... I just... I can't explain what this feels like..."),
                    _("You said it was okay... remember? You said okay..."),
                ],
            },
        },
        ("medium", "penetration"): {
            "npc": [
                _("Stop moaning like that! You never moan like that with me!"),
                _("Why are you enjoying this so much?! It's killing me!"),
                _("Babe, please... at least don't look at him like that..."),
            ],
            "girl": {
                "cum_slut": [
                    _("I can't help it... he hits spots you never... mmm..."),
                    _("Maybe if you watched more, you'd learn something..."),
                ],
                "submissive": [
                    _("Then fuck me better next time. Until then, he's in charge."),
                    _("I'm sorry, babe... when he takes me like this, I just do whatever he wants..."),
                    _("Don't blame me. He tells me to moan, so I moan. I'm his right now."),
                ],
                "hardcore": [
                    _("Not my fault he knows what he's doing..."),
                    _("Then fuck me this hard and maybe I'll moan like this for you too..."),
                ],
                "cute": [
                    _("I'm trying to be quiet... but he... oh god... I'm sorry..."),
                    _("Please don't hate me... my body won't listen to me anymore..."),
                ],
                "_default": [
                    _("I'm not... I'm not enjoying... oh... oh god..."),
                    _("It's just physical... it doesn't mean anything... mmm..."),
                ],
            },
        },
        ("fast", "penetration"): {
            "npc": [
                _("STOP! This is too much! I can't watch this!"),
                _("You're screaming for him! Right in front of me!"),
                _("I hate this... I hate this... why can't I leave..."),
            ],
            "girl": {
                "cum_slut": [
                    _("THEN DON'T WATCH! But we both know you will!"),
                    _("HIS COCK IS BREAKING ME AND I LOVE IT! DEAL WITH IT!"),
                ],
                "femdom": [
                    _("SHUT UP AND WATCH! THIS IS WHAT A REAL FUCK LOOKS LIKE!"),
                    _("YOU STAY RIGHT THERE! I DIDN'T SAY YOU COULD LEAVE!"),
                    _("EYES ON ME! YOU'RE GOING TO WATCH EVERY SECOND OF THIS!"),
                ],
                "hardcore": [
                    _("YOU CAN'T LEAVE BECAUSE YOU LOVE IT TOO!"),
                    _("HE'S FUCKING ME SO HARD I CAN'T EVEN SEE STRAIGHT!"),
                ],
                "cute": [
                    _("I'M SORRY! I'M SO SORRY! BUT I CAN'T... I CAN'T STOP!"),
                    _("DON'T LOOK AT ME LIKE THAT! I FEEL BAD ENOUGH ALREADY!"),
                ],
                "_default": [
                    _("I KNOW! I KNOW! BUT HE'S... OH GOD... I CAN'T THINK!"),
                    _("STOP YELLING AT ME! YOU'RE THE ONE WHO WON'T LEAVE!"),
                ],
            },
        },
        # ── Oral (blowjob) ──
        ("slow", "oral"): {
            "npc": [
                _("You're really going to suck him off right in front of me...?"),
                _("Babe... your mouth is... that's... please stop..."),
                _("I can't believe what I'm watching right now..."),
            ],
            "girl": {
                "cum_slut": [
                    _("Mmm... I love this cock in my mouth... sorry baby..."),
                    _("Want me to stop? ...I don't think I can..."),
                ],
                "hardcore": [
                    _("Jealous? Maybe you should take notes."),
                    _("This is what enthusiasm looks like. Watch and learn."),
                ],
                "cute": [
                    _("I know... I'm sorry... but he asked me to..."),
                    _("Don't look... please... this is embarrassing enough..."),
                ],
                "_default": [
                    _("I... I can't talk right now..."),
                    _("Just... give me a minute... please..."),
                ],
            },
        },
        ("medium", "oral"): {
            "npc": [
                _("You never did THAT with me! Why are you trying so hard for him?!"),
                _("Stop looking at me while you... just... stop looking at me!"),
                _("The sounds you're making... you never made those sounds for me..."),
            ],
            "girl": {
                "cum_slut": [
                    _("Because his cock deserves it... mmm... sorry babe..."),
                    _("I can't help how much I love sucking him..."),
                ],
                "hardcore": [
                    _("Because he EARNS it. Maybe step up your game."),
                    _("I try harder because he fucks harder. Simple."),
                ],
                "cute": [
                    _("I'm not trying harder... it just... happens... I'm sorry..."),
                    _("I can't explain it... my body just responds to him..."),
                ],
                "_default": [
                    _("I don't know why it's different... it just is..."),
                    _("Please stop comparing... this isn't about you..."),
                ],
            },
        },
        ("fast", "oral"): {
            "npc": [
                _("You're choking on it and you WON'T STOP?! What happened to you?!"),
                _("I CAN'T WATCH THIS! ...But I can't leave either!"),
                _("STOP! Just STOP! ...Why am I still here..."),
            ],
            "girl": {
                "cum_slut": [
                    _("I WANT HIM TO CUM IN MY MOUTH! DEAL WITH IT!"),
                    _("THIS COCK! MMM! I'M NOT STOPPING!"),
                ],
                "femdom": [
                    _("THEN LEAVE! OR SHUT UP AND WATCH!"),
                    _("YOU DON'T LEAVE UNTIL I SAY SO! SIT DOWN!"),
                    _("KEEP WATCHING! I WANT YOU TO SEE ALL OF IT!"),
                ],
                "hardcore": [
                    _("I'LL SUCK WHOEVER I WANT HOWEVER I WANT!"),
                    _("HE'S FUCKING MY THROAT AND I'M LOVING EVERY SECOND!"),
                ],
                "cute": [
                    _("I CAN'T STOP! HE'S... HE'S MAKING ME... I'M SORRY!"),
                    _("PLEASE FORGIVE ME! I DON'T KNOW WHAT'S WRONG WITH ME!"),
                ],
                "_default": [
                    _("I CAN'T THINK! JUST... GIVE ME A SECOND..."),
                    _("STOP WATCHING IF YOU CAN'T HANDLE IT!"),
                ],
            },
        },
        # ── Manual (handjob, titjob) ──
        ("slow", "manual"): {
            "npc": [
                _("You're touching him... right in front of me..."),
                _("Babe... your hands... please... that's enough..."),
                _("I can see everything you're doing to him..."),
            ],
            "girl": {
                "cum_slut": [
                    _("It's just my hands, relax... for now..."),
                    _("You should see how hard he gets for me..."),
                ],
                "hardcore": [
                    _("It's just a handjob. Stop being dramatic."),
                    _("You agreed to this. Don't whine now."),
                ],
                "cute": [
                    _("It's just touching... it could be worse... right?"),
                    _("I'm sorry... I'll try to be quick..."),
                ],
                "_default": [
                    _("It's not that big a deal... it's just touching..."),
                    _("Relax... this is nothing compared to what we could be doing..."),
                ],
            },
        },
        ("medium", "manual"): {
            "npc": [
                _("You're really getting into it... I can tell by your face..."),
                _("Why do you look like you're enjoying this so much?!"),
                _("Your hands are all over him... this is killing me..."),
            ],
            "girl": {
                "cum_slut": [
                    _("I love feeling him throb in my hands... mmm..."),
                    _("His reactions are so hot... I can't help it..."),
                ],
                "hardcore": [
                    _("Because I AM enjoying it. Problem?"),
                    _("I like making him feel good. Get over it."),
                ],
                "cute": [
                    _("I'm not... I'm just... it's complicated... I'm sorry..."),
                    _("I wish you wouldn't watch me do this..."),
                ],
                "_default": [
                    _("I... I didn't think it would feel like this..."),
                    _("Please look away... this is hard enough..."),
                ],
            },
        },
        ("fast", "manual"): {
            "npc": [
                _("SLOW DOWN! You're going to make him... right in front of me?!"),
                _("You're jerking him off like your life depends on it! STOP!"),
                _("I CAN'T TAKE THIS! Your hands... the way you're moving..."),
            ],
            "girl": {
                "cum_slut": [
                    _("I WANT HIM TO CUM! I WANT TO SEE IT!"),
                    _("ALMOST THERE! I CAN FEEL HIM THROBBING!"),
                ],
                "hardcore": [
                    _("I'LL GO AS FAST AS I WANT! WATCH OR LEAVE!"),
                    _("HE'S ABOUT TO FINISH AND I'M GOING TO MAKE SURE HE DOES!"),
                ],
                "cute": [
                    _("I'M SORRY! HE TOLD ME TO GO FASTER! I COULDN'T SAY NO!"),
                    _("PLEASE DON'T BE MAD! I JUST... I CAN'T SLOW DOWN!"),
                ],
                "_default": [
                    _("I'M NOT STOPPING NOW! NOT WHEN HE'S THIS CLOSE!"),
                    _("JUST LOOK AWAY! I'LL BE DONE SOON!"),
                ],
            },
        },
    }

    # ── Hostile NTR: Surrender event (NPC stops begging, starts directing) ──

    _NTR_HOSTILE_SURRENDER = {
        "npc_transition": [
            _("Stop... please sto... ...harder."),
            _("Don't do this to h... ...don't stop."),
            _("I can't watch thi... ...turn her around. I want to see her face."),
        ],
        "npc_directing": [
            _("Harder. Make her feel it."),
            _("Pull her hair. She likes that... I know she does."),
            _("Don't stop. Whatever you do, don't stop."),
            _("Faster. She's close. I can tell."),
        ],
        "girl": {
            "cum_slut": [
                _("Baby...? Did you just... oh god, that's so hot..."),
                _("Wait... are you telling him to go HARDER? ...Keep talking..."),
            ],
            "hardcore": [
                _("Finally. Took you long enough to stop pretending."),
                _("There it is. I knew you'd break eventually."),
            ],
            "cute": [
                _("Baby...? Are you... are you ENJOYING this...?"),
                _("W-wait... did you just tell him to... oh god..."),
            ],
            "_default": [
                _("Did you just... tell him to go harder...?"),
                _("Are you... directing him? What's happening to you...?"),
            ],
        },
        "npc_aftermath": [
            _("...I don't know who I am anymore. But don't stop."),
            _("...I hate myself. But I need this. Don't you dare stop."),
            _("...Something broke inside me. And I don't want to fix it."),
        ],
    }

    # ── Post-surrender: NPC directs instead of begging ──

    _NTR_HOSTILE_POST_SURRENDER = {
        "npc": [
            _("Harder. She can take it."),
            _("Slow down. Make her feel every inch."),
            _("Good. Just like that. Don't stop."),
            _("Grab her hips. Hold her in place."),
            _("Make her look at me while you do it."),
        ],
        "girl": {
            "cum_slut": [
                _("Yes... do what he says..."),
                _("He knows what I like... listen to him..."),
            ],
            "hardcore": [
                _("Look at him. Giving orders now. I like this version better."),
                _("About time you owned it. Keep talking."),
            ],
            "cute": [
                _("He's... watching again... telling you what to do..."),
                _("I can't believe he's okay with this now..."),
            ],
            "_default": [
                _("He's different now. More intense..."),
                _("I don't know if this is better or worse..."),
            ],
        },
    }

    _NPC_SECRET_MASTURBATION_LINES = [
        _("You filmed her WITHOUT her knowing?! What the hell is wrong with you?"),
        _("She didn't even know she was being recorded! That's disgusting. I'm telling her."),
        _("You secretly recorded my girlfriend?! She deserves to know about this."),
    ]

    _NPC_SECRET_MASTURBATION_GENERIC = [
        _("That's clearly someone being filmed without knowing. That's messed up, dude."),
        _("You recorded someone without their consent? What's wrong with you?"),
        _("Whoever she is, she clearly didn't know she was being filmed. That's not okay."),
    ]

    # ── NTR partner reacts to video of lesbian girlfriend with a man ──
    _NTR_VIDEO_LESBIAN_EXPOSED = {
        "_default": [
            _("That's %s... with a guy? But she's... what? How did you get her to do that?"),
            _("Is that my girlfriend?! With a MAN?! She told me she would never... how?"),
        ],
        "hj": [
            _("She's giving you a handjob? My girlfriend who says she hates men... is touching YOUR dick?"),
            _("That's %s jerking you off? She told me she'd never touch a man like that."),
        ],
        "bj": [
            _("My lesbian girlfriend is sucking YOUR dick?! What the hell did you do to her?"),
            _("She's... she's blowing you? %s swore she'd never put a man in her mouth."),
        ],
        "cowgirl": [
            _("She's RIDING you?! A man?! %s told me men disgusted her!"),
            _("That's %s on top of a guy... willingly? I can't believe what I'm seeing."),
        ],
        "doggy": [
            _("You're fucking her from behind?! She said she'd never let a man do that!"),
            _("That's %s... letting a guy take her from behind. What happened to 'I'm a lesbian'?"),
        ],
        "full_nelson": [
            _("You're HOLDING her up and fucking her?! She can't even fight back! What the hell?!"),
            _("Is that %s?! A man has her in a full nelson?! She looks... she's not even resisting?!"),
        ],
        "anal": [
            _("She's letting you do ANAL?! She won't even let ME near there! What is going on?!"),
            _("My girlfriend is taking it in the ass from a man?! She said that was off limits for EVERYONE!"),
        ],
        "full_nelson_anal": [
            _("You're holding her up and fucking her ass?! She's my GIRLFRIEND! She's LESBIAN! HOW?!"),
            _("Full nelson anal?! With MY girlfriend?! She can't even move! What did you do to her?!"),
        ],
        "reverse_cowgirl_anal": [
            _("She's riding a MAN... and taking it in the ass?! %s said that was off limits for EVERYONE!"),
            _("My lesbian girlfriend, on top of a guy, with it in her ass?! What did you DO to her?!"),
        ],
        "laying_down": [
            _("She's just laying there letting you fuck her?! My LESBIAN girlfriend?! What is happening?!"),
            _("That's %s on her back with a MAN on top?! She told me she'd NEVER let a guy be on top!"),
        ],
        "laying_anal": [
            _("She's laying there taking it in the ass from a GUY?! She won't even let ME near there!"),
            _("Anal while laying down?! With MY girlfriend?! She said that was off limits for EVERYONE!"),
        ],
        "creampie": [
            _("You came INSIDE my girlfriend?! A MAN came inside my LESBIAN girlfriend?!"),
            _("A creampie?! Inside %s?! She hates men! How did you get her to let you do that?!"),
        ],
        "masturbate": [
            _("She's touching herself... for a guy? She told me she only does that thinking about women."),
            _("That's %s masturbating for you? She would never do that for a man... or so she told me."),
        ],
    }

    # ── Cuckold/Threesome video reaction pools ──

    # NPC was the RECORDER (player sends him back his own footage)
    _NPC_CUCKOLD_SELF_LEVEL0 = [
        _("Why are you sending me this? I was there... I know what I did. Stop reminding me."),
        _("I already can't sleep thinking about it. You don't need to rub it in with the video."),
        _("I held your phone while you... just delete it. Please. I don't want proof this happened."),
    ]
    _NPC_CUCKOLD_SELF_LEVEL2 = [
        _("Yeah... I remember. I held your phone the whole time. I know what I saw."),
        _("You're sending me the video I recorded for you? Fine. I know what happened. It is what it is."),
        _("I was there. I filmed it. Watching it back doesn't change anything. It already happened."),
    ]
    _NPC_CUCKOLD_SELF_LEVEL3 = [
        _("Fuck... I'm watching it again. I can't stop. The angles I got were perfect."),
        _("Dude, send me more like this. I got amazing footage. When's the next time?"),
        _("I keep rewatching this. My own camerawork. I'm weirdly proud of what I captured."),
    ]
    _NPC_CUCKOLD_SELF_HOSTILE = [
        _("I hate that I can't stop replaying this. I hate that I held the camera. I hate all of it."),
        _("Why did you send me this? I was there, I know what I did. And I hate myself for it."),
        _("Watching this back makes me want to punch something. I recorded my own humiliation."),
    ]

    # NPC was NOT involved (video of different couple being cucked)
    _NPC_CUCKOLD_OTHER_NTR = [
        _("Her boyfriend was watching? I... yeah. I know what that's like. It's complicated."),
        _("You're showing me this because you know I... never mind. That guy went through something."),
        _("Watching someone else go through it... I can't tell if it makes me feel better or worse."),
    ]
    _NPC_CUCKOLD_OTHER_DEFAULT = [
        _("Why are you showing me this? Her boyfriend was there? That's messed up, dude."),
        _("Bro, what? Her boyfriend WATCHED? That's the weirdest thing I've seen today."),
        _("I don't know why you're sending me videos of other people's relationship problems."),
    ]
    _NPC_CUCKOLD_OTHER_FRIENDLY = [
        _("Damn, that's wild. Her boyfriend just watched? Respect for the power move, I guess."),
        _("That's insane, bro. His girlfriend getting railed while he records? What a world."),
    ]

    # Threesome: His GF is the SUBJECT (another girl recorded her getting fucked)
    _NPC_THREESOME_GF_SUBJECT_NTR_IN = [
        _("She was being filmed by another girl? While you fucked her? How many people are in on this?"),
        _("Another girl was THERE? Watching? This is getting more complicated than I agreed to."),
        _("I knew about you two, but another person seeing it? That wasn't part of the deal."),
    ]
    _NPC_THREESOME_GF_SUBJECT_NO_NTR = [
        _("My girlfriend... getting fucked... with ANOTHER girl watching?! What the hell is going on?!"),
        _("She let another girl WATCH?! And RECORD?! Who else knows about this?!"),
        _("There was someone ELSE there?! Another girl SAW my girlfriend doing... THAT?!"),
    ]

    # Threesome: His GF was the RECORDER (she held the camera)
    _NPC_THREESOME_GF_RECORDER_LOW = [
        _("My girlfriend was THERE? Filming another girl having sex? What the hell?!"),
        _("She WATCHED another girl get fucked? And held the camera?! Why would she do that?!"),
        _("Why was my girlfriend in the room?! She filmed you two?! I don't understand!"),
    ]
    _NPC_THREESOME_GF_RECORDER_HIGH = [
        _("She watched? And recorded? Did she... enjoy it? I'm not sure how to feel about that."),
        _("My girlfriend was the camerawoman? Interesting. Did she just watch or... participate?"),
        _("She chose to be there and film. That's... honestly kind of intriguing."),
    ]
    _NPC_THREESOME_GF_RECORDER_HOSTILE = [
        _("She chose to be there. She watched another girl get fucked. And she FILMED it."),
        _("My girlfriend held the camera while you... she wasn't forced. She chose to watch."),
        _("She voluntarily recorded this. She wanted to be there. I don't know what to do with that."),
    ]

    # ── NTR Girl Boundary-Aware Dialogue Pools ──

    _NTR_GIRL_DENY_RAW = {
        "cum_slut": [
            _("I want to... but %(pp)s said we have to use a condom. I can't."),
            _("Ugh, I hate this. %(Pp)s made me promise we'd use protection."),
            _("%(Pp)s said no raw... and as much as I want to feel you, I can't break that promise."),
        ],
        "hardcore_sex": [
            _("I'd go raw in a heartbeat, but %(pp)s set the rules. Condom stays."),
            _("Don't tempt me. %(Pp)s said condom or nothing. That's the deal."),
        ],
        "cute_sex": [
            _("N-no... %(pp)s said we can only do it with a condom... I'd feel too guilty..."),
            _("We can't... not without protection. %(Pp)s trusted me with that one rule..."),
            _("Please don't ask me that... %(pp)s would be so hurt if we broke that promise..."),
        ],
        "loyal": [
            _("No. %(Pp)s said condom only, and I'm keeping my word. That's final."),
            _("I already feel terrible doing this. I'm not breaking %(poss)s one rule too."),
        ],
        "_default": [
            _("No, %(pp)s said we can only do it with a condom. That would be cheating."),
            _("We can't go raw... %(pp)s set that boundary and I need to respect it."),
            _("I'm already doing this behind %(poss)s back. The least I can do is use protection."),
        ],
    }

    _NTR_GIRL_DENY_CREAMPIE = {
        "cum_slut": [
            _("I want it so bad... but %(pp)s said no cumming inside. That was the one rule."),
            _("Please don't make this harder... I want every drop but %(pp)s would never forgive me."),
        ],
        "hardcore_sex": [
            _("As much as I'd love that, %(pp)s drew the line at creampies. No."),
            _("Don't. %(Pp)s said anything but inside. I'm not crossing that line."),
        ],
        "cute_sex": [
            _("No! You can't cum inside me... %(pp)s said that was the one thing we couldn't do..."),
            _("Please... not inside... %(pp)s trusted us with that rule and I can't break it..."),
        ],
        "loyal": [
            _("Absolutely not. %(Pp)s said no finishing inside, and I'm keeping that promise."),
            _("No. That's the one thing %(pp)s asked me not to do. I won't betray that trust."),
        ],
        "_default": [
            _("No! You can't cum inside me, %(pp)s said that was the one rule!"),
            _("Not inside... %(pp)s told me that was off limits. Please."),
            _("Pull out. %(Pp)s said anything but inside and I'm keeping my word."),
        ],
    }

    _NTR_GIRL_DENY_PENETRATION = {
        "cum_slut": [
            _("I want to so bad... but %(pp)s said no penetration. Only hands and mouth."),
            _("As much as I'd love to feel you inside me, %(pp)s drew the line there."),
        ],
        "hardcore_sex": [
            _("%(Pp)s said no fucking. Just hands and mouth. Those are the rules."),
            _("I'd ride you right now if I could, but %(pp)s said no penetration."),
        ],
        "cute_sex": [
            _("We can't do that... %(pp)s said no penetration... I'd feel so guilty..."),
            _("N-no... that's too far... %(pp)s said only touching and... you know... mouth stuff..."),
        ],
        "loyal": [
            _("No. %(Pp)s said no penetration and I gave my word. I'm not breaking it."),
            _("That's crossing a line. %(Pp)s was clear. No actual sex."),
        ],
        "_default": [
            _("No... %(pp)s said we can only do stuff without actual sex. No penetration."),
            _("We can't go that far... %(pp)s set the boundary at non-penetration only."),
            _("I can use my hands, my mouth, but... %(pp)s said no actual sex."),
        ],
    }

    _NTR_GIRL_DENY_ANAL = {
        "cum_slut": [
            _("Not there... %(pp)s said anal was off the table completely."),
        ],
        "hardcore_sex": [
            _("Anal is a hard no. %(Pp)s made that crystal clear."),
        ],
        "cute_sex": [
            _("N-not there! %(Pp)s said absolutely no anal... please..."),
            _("That's... no. %(Pp)s specifically said that was not okay..."),
        ],
        "loyal": [
            _("No. %(Pp)s was very specific about that. Anal is completely off limits."),
        ],
        "_default": [
            _("Not there... %(pp)s said no anal. That's a hard line."),
            _("No... %(pp)s made it clear. Anal is not something I can do with you."),
        ],
    }

    _NTR_GIRL_GUILTY_RAW = {
        "cum_slut": [
            _("...fuck it. Take it off. %(Pp)s doesn't have to know we did this without a condom."),
            _("I shouldn't... but I need to feel you. %(Pp)s can never find out."),
        ],
        "hardcore_sex": [
            _("...okay, raw. But %(pp)s can NEVER know. Got it?"),
            _("Screw it. Take it off. But this stays between us."),
        ],
        "cute_sex": [
            _("...okay, but %(pp)s can never find out we did this without a condom..."),
            _("I feel so bad... but... okay. Just this once. %(Pp)s would be devastated..."),
        ],
        "_default": [
            _("...okay, but %(pp)s can never find out we did this without a condom."),
            _("Fine... but if %(pp)s ever finds out, I'll deny everything."),
            _("I'm going to regret this... but take it off. %(Pp)s doesn't need to know."),
        ],
    }

    _NTR_GIRL_GUILTY_CREAMPIE = {
        "cum_slut": [
            _("...okay, just this once. %(Pp)s won't know you came inside me..."),
            _("I want it so bad I can't say no... but %(pp)s can never find out."),
        ],
        "hardcore_sex": [
            _("...do it. But %(pp)s finds out and I'll say you forced me."),
        ],
        "cute_sex": [
            _("...I shouldn't let you... but... okay... just don't tell %(po)s... please..."),
        ],
        "_default": [
            _("...fine, just this once. But %(pp)s can never find out you came inside me."),
            _("I can't believe I'm saying this... but do it. %(Pp)s can never know."),
        ],
    }

    _NTR_GIRL_GUILTY_PENETRATION = {
        "cum_slut": [
            _("...%(pp)s said no penetration but... I need you inside me. %(Pp)s won't know."),
        ],
        "hardcore_sex": [
            _("...screw the rules. Put it in. But %(pp)s can NEVER find out."),
        ],
        "cute_sex": [
            _("...I know I shouldn't... but I want you... %(pp)s can't find out about this..."),
        ],
        "_default": [
            _("...okay... just... %(pp)s can never know we went this far..."),
            _("I shouldn't... but I want it. %(Pp)s doesn't have to know everything."),
        ],
    }

    _NTR_GIRL_REQUEST_RAW = {
        "cum_slut": [
            _("Take it off... I know %(pp)s said use a condom but I can't take it anymore... I need to feel you."),
            _("I don't care what %(pp)s said. Take the condom off. I need you raw."),
        ],
        "hardcore_sex": [
            _("Fuck the condom. %(Pp)s isn't here. Take it off and give it to me properly."),
        ],
        "_default": [
            _("Take the condom off... I want to feel you. %(Pp)s doesn't have to know."),
            _("Can we... skip the condom? Just this once? %(Pp)s won't find out."),
        ],
    }

    _NTR_GIRL_REQUEST_CREAMPIE = {
        "cum_slut": [
            _("Cum inside me... %(pp)s doesn't have to know. I want every drop."),
            _("I don't care what %(pp)s said... I need you to fill me up."),
        ],
        "hardcore_sex": [
            _("Cum inside. %(Pp)s set the rules but %(pp)s isn't here right now."),
        ],
        "_default": [
            _("Cum inside me... it'll be our secret. I won't tell %(po)s."),
            _("Don't pull out... I want to feel you finish inside me. %(Pp)s doesn't have to know."),
        ],
    }

    # ── Girl asks NPC directly (partner watching) ──

    _NTR_GIRL_ASK_NPC_CONDOM = {
        "cum_slut": [
            _("Babe, please... let him take the condom off. I need to feel him raw... I'd cum so much harder."),
            _("%(name)s, please... tell him he can take it off. I can't cum like this."),
        ],
        "hardcore_sex": [
            _("Babe, let him take the condom off already. I want to feel him for real."),
            _("%(name)s, tell him to lose the condom. I want it raw."),
        ],
        "cute_sex": [
            _("B-babe... can he... take it off? The condom, I mean... it would feel so much better..."),
            _("%(name)s... would it be okay if... he took the condom off? Please..."),
        ],
        "loyal": [
            _("I know you said condom only, but... please? Just this once? I need it..."),
        ],
        "_default": [
            _("Babe, please, let him take the condom off... I'd cum so much better without it..."),
            _("%(name)s... can he take it off? I want to feel him... please..."),
            _("Babe, please... let him take the condom off. I need to feel him raw..."),
        ],
    }

    _NTR_GIRL_ASK_NPC_CREAMPIE = {
        "cum_slut": [
            _("Please, %(name)s, let him cum inside me... I need to feel it. Every single drop."),
            _("Babe, tell him he can cum inside... I want him to fill me up. Please."),
        ],
        "hardcore_sex": [
            _("%(name)s, let him finish inside. I want to feel him cum in me."),
            _("Babe, I want him to cum inside me. Tell him it's okay."),
        ],
        "cute_sex": [
            _("%(name)s... c-can he... finish inside? I know it's a lot to ask but... please..."),
        ],
        "loyal": [
            _("I know this is past what you agreed to, but... can he cum inside? Just this once..."),
        ],
        "_default": [
            _("Please, %(name)s... let him cum inside me. I want to feel it..."),
            _("Babe, can he finish inside me? I want it so bad..."),
        ],
    }

    _NTR_GIRL_ASK_NPC_PENETRATION = {
        "cum_slut": [
            _("Babe, let him put it in... just the tip. I need to feel a cock inside me."),
            _("%(name)s, please, tell him he can put it in... even just the tip... I'm going crazy."),
        ],
        "hardcore_sex": [
            _("%(name)s, let him put it in. I can't take the teasing anymore."),
            _("Babe, tell him to stop rubbing and put it inside. Just the tip at least."),
        ],
        "cute_sex": [
            _("%(name)s... can he... put it in? Just a little? I... I want to know how it feels..."),
        ],
        "loyal": [
            _("I know you said no penetration, but... babe, please... I need to feel him inside me..."),
        ],
        "_default": [
            _("Babe, let him put it in... just the tip... please, I need it..."),
            _("%(name)s, can he put it inside? I promise it'll just be the tip..."),
        ],
    }

    _NTR_GIRL_ASK_NPC_FULLSEX = {
        "cum_slut": [
            _("%(name)s, tell him to put it all the way in... I can't take just the tip anymore, I NEED it."),
            _("Babe, please... let him go all the way. I need his whole cock inside me."),
        ],
        "hardcore_sex": [
            _("%(name)s, let him put it all in. I'm done with this teasing."),
            _("Babe, tell him to stop holding back and fuck me properly."),
        ],
        "cute_sex": [
            _("%(name)s... c-can he... go deeper? I... I want to feel all of it... please..."),
        ],
        "loyal": [
            _("Babe, I know this is a lot... but please, let him go all the way in... I need it..."),
        ],
        "_default": [
            _("%(name)s, please... let him go all the way... I can't take just the tip anymore..."),
            _("Babe, let him put it all in... I need to feel everything..."),
        ],
    }

    _NTR_GIRL_ASK_NPC_ANAL = {
        "anal_lover": [   # was keyed "cum_slut": any cum lover claimed to love anal
            _("%(name)s, let him try my ass... please, I want it so bad. You know how much I love it."),
            _("Babe, tell him he can fuck my ass... I need it. Please."),
        ],
        "hardcore_sex": [
            _("%(name)s, let him do my ass. I want it rough back there."),
        ],
        "cute_sex": [
            _("%(name)s... would it be okay if he... tried my... other hole? I... I'm curious..."),
        ],
        "_default": [
            _("Babe... let him try my ass... please... I want it so bad..."),
            _("%(name)s, can he... go back there? I need to feel him in my ass..."),
        ],
    }

    _NTR_GIRL_ASK_NPC_POOLS = {
        "condom_remove": _NTR_GIRL_ASK_NPC_CONDOM,
        "creampie": _NTR_GIRL_ASK_NPC_CREAMPIE,
        "penetration": _NTR_GIRL_ASK_NPC_PENETRATION,
        "full_sex": _NTR_GIRL_ASK_NPC_FULLSEX,
        "anal": _NTR_GIRL_ASK_NPC_ANAL,
    }

    _NPC_AUTHORIZE_RESPONSE = {
        ("condom_remove", "friendly"): [
            _("...fine. If that's what you want, baby."),
            _("...alright. He can take it off. But only because you asked."),
        ],
        ("condom_remove", "neutral"): [
            _("...I guess. But just this once."),
            _("...whatever. If that's what you need."),
        ],
        ("condom_remove", "hostile"): [
            _("...fine. Do whatever you want. You clearly don't care what I think."),
        ],
        ("creampie", "friendly"): [
            _("...go ahead. Let him finish inside you."),
            _("...okay, baby. If that's what you want."),
        ],
        ("creampie", "neutral"): [
            _("...whatever. Just... don't make a big deal of it."),
        ],
        ("creampie", "hostile"): [
            _("...sure. Why not. Nothing matters at this point."),
        ],
        ("penetration", "friendly"): [
            _("...alright. If you need it that bad."),
            _("...okay. He can put it in. But be careful."),
        ],
        ("penetration", "neutral"): [
            _("...do what you want."),
            _("...I guess I can't stop you."),
        ],
        ("penetration", "hostile"): [
            _("...go ahead. Ruin everything."),
        ],
        ("full_sex", "friendly"): [
            _("...okay, baby. Let him go all the way. I trust you."),
            _("...fine. If that's what makes you happy."),
        ],
        ("full_sex", "neutral"): [
            _("...I can't believe this. Fine."),
        ],
        ("full_sex", "hostile"): [
            _("...whatever. You've already gone this far."),
        ],
        ("anal", "friendly"): [
            _("...Jesus. Fine. If you really want that."),
            _("...okay. But... just be careful."),
        ],
        ("anal", "neutral"): [
            _("...I can't believe I'm saying yes to this."),
        ],
        ("anal", "hostile"): [
            _("...sure. Go ahead. What's one more line to cross."),
        ],
        # ── Hostile NTR: self-loathing permission ──
        ("condom_remove", "hostile_ntr"): [
            _("...I hate this. I hate you. ...Fine. Take it off. I don't care anymore. ...I care. But fine."),
            _("...Why am I saying yes...? Just... just do it. Before I change my mind."),
        ],
        ("creampie", "hostile_ntr"): [
            _("...Inside her? You want to... I should say no. I WANT to say no. ...Do it."),
            _("...Go ahead. Finish inside. I'll hate myself for saying this. But do it."),
        ],
        ("penetration", "hostile_ntr"): [
            _("...Put it in. I can't believe I'm saying this. ...Just do it before I lose it."),
            _("...Fine. Go ahead. Penetrate her. I'll... I'll just... stand here. Watching. Like always."),
        ],
        ("full_sex", "hostile_ntr"): [
            _("...Whatever. Fuck her. Properly. I don't even know who I am anymore."),
            _("...Do it. All the way. I've stopped recognizing myself anyway."),
        ],
        ("anal", "hostile_ntr"): [
            _("...Her ass too? You're a monster. ...I'm worse for saying yes. Do it."),
            _("...That's... that's too much. ...But I'll say yes anyway. What's wrong with me?"),
        ],
    }

    _NPC_DENY_RESPONSE = {
        ("condom_remove", "friendly"): [
            _("No, baby. The condom stays on. That was our deal."),
            _("I'm sorry, but no. That's my one rule. Please."),
        ],
        ("condom_remove", "neutral"): [
            _("No. The condom stays on."),
            _("Absolutely not. That was the deal."),
        ],
        ("condom_remove", "hostile"): [
            _("Are you kidding me? No. The condom stays."),
        ],
        ("creampie", "friendly"): [
            _("No, baby. He can't finish inside you. That's too far."),
            _("I love you, but no. He's not cumming inside you."),
        ],
        ("creampie", "neutral"): [
            _("No way. He's not cumming inside you."),
        ],
        ("creampie", "hostile"): [
            _("The fuck? No. Absolutely not."),
        ],
        ("penetration", "friendly"): [
            _("No. I said no penetration, and I meant it. Please don't ask again."),
        ],
        ("penetration", "neutral"): [
            _("No. I said no penetration and I meant it."),
        ],
        ("penetration", "hostile"): [
            _("Are you serious right now? No."),
        ],
        ("full_sex", "friendly"): [
            _("No, baby. The tip was already a lot. I can't handle more than that."),
        ],
        ("full_sex", "neutral"): [
            _("No. You already got the tip. Don't push it."),
        ],
        ("full_sex", "hostile"): [
            _("Are you insane? No way."),
        ],
        ("anal", "friendly"): [
            _("No. That's way too far, baby. I can't watch that."),
        ],
        ("anal", "neutral"): [
            _("No. That's too far."),
        ],
        ("anal", "hostile"): [
            _("You've lost your mind. No."),
        ],
        # ── Hostile NTR: begging denial ──
        ("condom_remove", "hostile_ntr"): [
            _("No... please... the condom stays. That's all I have left. Please don't take that from me..."),
            _("Please... just... keep the condom on. I need that. I need SOMETHING to hold on to."),
        ],
        ("creampie", "hostile_ntr"): [
            _("Please... don't cum inside her... that's the one thing I can't watch... please..."),
            _("Not inside... please... I know I've agreed to a lot but... not that. I'm begging you."),
        ],
        ("penetration", "hostile_ntr"): [
            _("No penetration... please... I know I agreed to things but not that... not yet... please..."),
            _("Please... don't put it in... touching is one thing but... this is different. Please."),
        ],
        ("full_sex", "hostile_ntr"): [
            _("Just the tip was already too much... please... I can't handle more than that..."),
            _("No... going all the way would break me... please... I'm barely holding together as it is..."),
        ],
        ("anal", "hostile_ntr"): [
            _("Not that... anything but that... please... I'm begging you..."),
            _("Her ass...? No... that's... I can't. I physically cannot watch that. Please."),
        ],
    }

    _NTR_GIRL_NPC_AUTHORIZED = {
        "cum_slut": [
            _("Yes! Thank you, babe... you won't regret this..."),
            _("Thank you, %(name)s... I promise it'll be worth watching..."),
        ],
        "femdom": [
            _("That's what I thought. Now watch."),
            _("Good. Now sit back and watch, %(name)s."),
            _("Smart answer. Stay right there, %(name)s, and don't look away."),
        ],
        "hardcore_sex": [
            _("Good. Because he's about to fuck me hard, and I didn't want to wait."),
            _("Finally. I've been dying for him to go rough on me, %(name)s."),
        ],
        "cute_sex": [
            _("Thank you, baby... I promise it'll be worth it..."),
            _("R-really? Thank you, %(name)s..."),
        ],
        "loyal": [
            _("Thank you for trusting me, %(name)s... I love you."),
        ],
        "_default": [
            _("Thank you, babe... you don't know how much I needed this..."),
            _("Thank you, %(name)s... I'll make it up to you..."),
        ],
    }

    _NTR_GIRL_NPC_DENIED = {
        "cum_slut": [
            _("Please? Just this once? I need it so bad, %(name)s..."),
            _("Ugh... fine. But you're killing me, babe..."),
        ],
        "hardcore_sex": [
            _("Ugh, whatever... it's your loss, %(name)s."),
            _("Fine. But don't expect me to be happy about it."),
        ],
        "cute_sex": [
            _("O-okay... I understand, %(name)s..."),
            _("You're right... I'm sorry I asked..."),
        ],
        "loyal": [
            _("You're right. I'm sorry, %(name)s. I shouldn't have asked."),
        ],
        "_default": [
            _("Fine... I understand, %(name)s."),
            _("Okay... if that's what you want, babe..."),
        ],
    }

    _NPC_PLAYER_OBEYED = {
        "voyeur": [
            _("That was... fuck. That was something."),
            _("...I can't believe how hot that was."),
        ],
        "friendly": [
            _("...I can't believe I just watched that. But... okay."),
            _("...just... don't take advantage of this."),
        ],
        "neutral": [
            _("...don't make me regret this."),
        ],
        "hostile": [
            _("...you got what you wanted. Don't expect this again."),
        ],
    }

    _NPC_PLAYER_DEFIED = {
        "friendly": [
            _("What the fuck?! I said NO! We had a deal!"),
            _("Are you kidding me?! I trusted you and you just... you just did it anyway?!"),
        ],
        "neutral": [
            _("You son of a bitch. I said no. What part of 'no' don't you understand?!"),
            _("You piece of shit... I told you not to do that!"),
        ],
        "hostile": [
            _("You piece of shit... I KNEW I couldn't trust you!"),
            _("I'm done. I'm fucking done with both of you."),
        ],
    }

    _NTR_GIRL_CBREAK_PANIC = {
        "cum_slut": [
            _("Oh no... the condom was the ONE thing keeping %(pp)s from losing it..."),
            _("%(Pp)s said condom only... and now it's broken. This is bad."),
        ],
        "hate_cum": [
            _("THE CONDOM BROKE?! %(Pp)s said we HAD to use one! This is a disaster!"),
        ],
        "cute_sex": [
            _("Oh no oh no oh no... %(pp)s said we had to use protection... what do we do?!"),
        ],
        "_default": [
            _("Oh god... %(pp)s said condom only and now it's broken... this is really bad."),
            _("The one rule %(pp)s set was use a condom... and now it broke. Perfect."),
        ],
    }

    _NTR_GIRL_CBREAK_EXCITED = {
        "cum_slut": [
            _("It broke? Oh well... guess %(pp)s can't blame us for an accident, right?"),
            _("The condom broke... I should be worried but honestly? I'm glad."),
        ],
        "hardcore_sex": [
            _("Broke? Good. %(Pp)s should have never set that rule anyway. Keep going."),
        ],
        "_default": [
            _("It broke... maybe this is a sign. %(Pp)s doesn't have to know, right?"),
            _("Oh... it broke. Well... it's not like we planned it. %(Pp)s can't blame us."),
        ],
    }

    # ── NPC watching condom break: NPC lines (partner's POV) ──
    # In these lines "she / her" is ALWAYS the girl and "he / him" is ALWAYS the player, so they are plain words:
    # %(pp)s / %(po)s are the PARTNER's own pronouns in both formatters and must never stand for them (the old
    # pools did, so a boyfriend said "he's not stopping him"). Only %(girl_name)s is filled, by
    # _format_npc_line(npc, line, girl). Pools are keyed hostile / voyeur / _default.

    _NTR_NPC_CBREAK_TOLD = {      # spoken out loud: she knows it broke and kept going raw
        "_default": [
            _("The condom broke? And %(girl_name)s is letting him keep going raw? ...I didn't expect to like this so much."),
            _("I can see the torn condom from here. %(girl_name)s knows... and she's not stopping him. That's so hot."),
            _("It broke and %(girl_name)s is still going? No protection, nothing... god, I can't look away."),
        ],
        "hostile": [
            _("It tore... and %(girl_name)s is still letting him? Bare? ...Why can't I make myself stop this?"),
            _("That condom was the one thing I asked for, %(girl_name)s. And you're not even slowing down..."),
            _("She knows it broke and she's taking him raw anyway... and I'm still standing here watching. God, I hate this."),
        ],
    }

    _NTR_NPC_CBREAK_HIDDEN = {    # THOUGHT, never spoken (Thinking()): only he and the player know
        "_default": [
            _("Wait... is that condom torn? %(girl_name)s doesn't even know... he's going in raw and she has no idea."),
            _("The condom is broken and %(girl_name)s can't tell. She thinks she's protected... this is unreal."),
            _("I can see it from here... the condom ripped. Every thrust is raw and she doesn't know."),
            _("I should say something. One word and it stops... so why am I keeping my mouth shut?"),
            _("That was my one rule. It just tore right in front of me... and I'm not going to tell her. What is wrong with me?"),
            _("He felt it rip and he kept going. He knows. I know. %(girl_name)s is the only one who doesn't... and my heart won't slow down."),
        ],
        "voyeur": [
            _("It ripped. She's taking him bare and only the two of us know... I've never been this turned on in my life."),
            _("Don't say a word. Don't ruin it. Just watch %(girl_name)s take him raw without knowing."),
            _("The condom is gone and she has no clue... this is better than anything I pictured."),
            _("Look at her... she thinks there's still something between them. There isn't. And I'm not telling."),
        ],
        "hostile": [
            _("The condom tore. He's inside %(girl_name)s with nothing on and she doesn't know... say something. Say something, you coward."),
            _("That bastard felt it break and kept going. And I'm just standing here. Again."),
            _("My one rule, torn open right in front of me... and my mouth won't open. I hate this. I hate myself."),
            _("She has no idea. One word from me and it stops... so why is part of me hoping he doesn't pull out?"),
        ],
    }

    _NTR_NPC_CBREAK_KNEW = {      # spoken: she has just found out, he had noticed long before
        "_default": [
            _("I saw it tear a while ago, %(girl_name)s. I should have said something... I didn't want to."),
            _("Don't look at me like that, %(girl_name)s. I noticed before you did. And I let him keep going."),
            _("I knew. I watched him take you raw and I kept my mouth shut... forget the condom rule. It's done."),
        ],
        "hostile": [
            _("I saw it rip, %(girl_name)s. I saw it and I couldn't say a word... what does that make me?"),
            _("I knew. I stood here and let it happen. Don't ask me why. I don't know why."),
        ],
    }

    _NTR_NPC_CBREAK_NARR = {      # narrator beats; the NPC pronouns (%(pp)s etc.) are correct HERE: they describe the partner
        "notice": {               # before the thought: the PLAYER sees him notice, she does not
            "_default": [
                _("%(name)s's eyes drop to where you and %(girl_name)s are joined... and freeze. %(Pp)s saw the tear. %(girl_name)s, lost in the moment, notices nothing."),
                _("You catch %(name)s staring at the torn condom. %(Poss)s mouth opens... then closes again. %(girl_name)s has no idea."),
                _("%(name)s leans in, squinting. %(Pp)s just noticed what %(girl_name)s hasn't: the condom is ripped."),
            ],
            "hostile": [
                _("%(name)s goes rigid, eyes locked on the torn condom. %(Pp)s looks at you, then at %(girl_name)s, who hasn't noticed a thing."),
                _("The color drains from %(name)s's face. %(Pp)s saw the condom rip. %(Poss)s lips move, but no sound comes out."),
            ],
        },
        "close_silent": {         # after the silent level-up
            "_default": [
                _("%(name)s says nothing. No warning, no protest. Whatever rule %(pp)s had about condoms just died in silence."),
                _("%(name)s keeps quiet and keeps watching, breathing harder than before. The broken condom pushed %(po)s to accept raw sex, and %(girl_name)s doesn't even know it happened."),
            ],
            "hostile": [
                _("%(name)s swallows whatever %(pp)s was about to say. That rule was %(poss)s last line of defense, and %(pp)s just let it go without a fight."),
            ],
        },
        "close_spoken": {         # told / knew. _default is the EXISTING string (its PT / ES pair stays valid)
            "_default": [
                _("%(name)s doesn't look upset. If anything, %(pp)s seems more excited than before. The broken condom pushed %(po)s to accept raw sex."),
            ],
            "hostile": [
                _("%(name)s looks wrecked, but %(pp)s doesn't ask for the condom back. The broken condom pushed %(po)s to accept raw sex."),
            ],
        },
    }

    # mode -> how the watching partner plays it. silent True = THOUGHT through Thinking() (she cannot hear it).
    # intro / close = _NTR_NPC_CBREAK_NARR keys. saw = value written to store._condom_break_partner_saw.
    _NTR_CBREAK_WATCH_MODES = {
        "told":   {"pool": _NTR_NPC_CBREAK_TOLD,   "silent": False, "intro": None,     "close": "close_spoken", "saw": "spoken"},
        "hidden": {"pool": _NTR_NPC_CBREAK_HIDDEN, "silent": True,  "intro": "notice", "close": "close_silent", "saw": "silent"},
        "knew":   {"pool": _NTR_NPC_CBREAK_KNEW,   "silent": False, "intro": None,     "close": "close_spoken", "saw": "spoken"},
    }

    # Chance that a WATCHING partner spots a hidden tear before she does. Only things the code already exposes.
    NTR_CBREAK_NOTICE = {
        "levels": (2,),            # boundary levels where the condom is HIS rule, so a tear matters to him
        "first_look": 0.35,        # his first watching tick after the tear (the tick it breaks, or his first tick if he walked in later)
        "per_tick": 0.12,          # every later watching tick while she still has not found out
        "npc_traits": {"voyeur": 0.20, "camera_lover": 0.10},   # additive, NPC partner traits
        "hostile": 0.10,           # hostile NTR mode: he studies every detail, looking for a reason to stop it
        "max": 0.90,
    }

    def _ntr_cbreak_line(npc, girl, pools):
        """Random line from a condom-break pool dict keyed hostile / voyeur / _default (same split as the watching
        narration in _npc_partner_detection_tick), translated and formatted in the NPC's voice."""
        _key = "hostile" if _ntr_is_hostile_mode(npc) else ("voyeur" if npc.has_trait("voyeur") else "_default")
        _pool = pools.get(_key) or pools["_default"]
        return _format_npc_line(npc, renpy.random.choice(_pool), girl)

    def _ntr_cbreak_watch_mode():
        """Which condom-break beat the watching partner plays. Single source for the label and the tick.
        hidden = the torn condom is still on and only the player knows | knew = she found out, he had silently
        noticed before | told = she knows and he reacts to it for the first time."""
        _hidden = store._condom_broken_hidden
        if _hidden and store.condom_active:
            return "hidden"
        if not _hidden and getattr(store, "_condom_break_partner_saw", None) == "silent":
            return "knew"
        return "told"

    def _ntr_cbreak_notice_chance(npc, looks):
        _cfg = NTR_CBREAK_NOTICE
        _chance = _cfg["first_look"] if looks == 0 else _cfg["per_tick"]
        for _t, _bonus in _cfg["npc_traits"].items():
            if npc.has_trait(_t):
                _chance += _bonus
        if _ntr_is_hostile_mode(npc):
            _chance += _cfg["hostile"]
        return min(_cfg["max"], _chance)

    def _ntr_cbreak_tick_fires(girl, npc, within):
        """Watching tick, WITHIN bounds only (the violation flow owns every other tick). True when the partner
        plays a condom-break beat now: 'knew' (one spoken follow-up after she found out) or 'hidden' (notice
        roll, NTR_CBREAK_NOTICE). He must be able to SEE: _tease_partner_watching() is False while he faces
        away in the bet event."""
        if not within or npc is None or not store._condom_broken:
            return False
        if not getattr(npc, "_ntr_active", False) or not _npc_witness_is_girls_partner(npc, girl):
            return False
        if not _tease_partner_watching():
            print("[NTR_CBREAK_NOTICE] %s cannot see the scene (facing away): no roll" % npc.name)
            return False
        _saw = getattr(store, "_condom_break_partner_saw", None)
        _mode = _ntr_cbreak_watch_mode()
        if _mode == "knew":
            print("[NTR_CBREAK_NOTICE] %s had noticed before %s found out -> follow-up beat" % (npc.name, girl.gid))
            return True
        if _mode != "hidden" or _saw is not None:
            return False
        if getattr(npc, "_ntr_boundary_level", 1) not in NTR_CBREAK_NOTICE["levels"]:
            return False
        _looks = getattr(store, "_condom_break_notice_looks", 0)
        _chance = _ntr_cbreak_notice_chance(npc, _looks)
        _roll = renpy.random.random()
        store._condom_break_notice_looks = _looks + 1
        print("[NTR_CBREAK_NOTICE] npc=%s girl=%s look=%d chance=%.2f roll=%.4f noticed=%s" % (
            npc.name, girl.gid, _looks + 1, _chance, _roll, _roll < _chance))
        return _roll < _chance

    # ── Girl discovers hidden break — NTR-specific harsher pools ──

    _NTR_GIRL_CBREAK_HIDDEN_DISCOVER = {
        "cum_slut": [
            _("The condom broke and you KNEW?! %(Pp)s said we had to use one! ...Okay, it felt amazing, but still!"),
            _("You hid this from me?! %(pl)s trusted us to use protection! ...Fine, I liked it, but that's not the point!"),
        ],
        "hate_cum": [
            _("THE CONDOM WAS BROKEN THIS WHOLE TIME?! %(pl)s said CONDOM ONLY! You betrayed BOTH of us!"),
            _("You KNEW it broke and kept going?! %(Pp)s trusted us! I trusted YOU! This is unforgivable!"),
        ],
        "hardcore_sex": [
            _("It broke and you didn't tell me? %(pl)s set that rule for a reason. That's messed up."),
            _("You hid the break? I don't care about the sex, but %(pl)s trusted us. That's a shitty move."),
        ],
        "cute_sex": [
            _("You... you knew the condom broke and didn't tell me? %(pl)s trusted us! I trusted you! How could you?!"),
            _("The condom was broken this whole time? %(Pp)s said we needed protection! You lied to BOTH of us!"),
        ],
        "cheater": [
            _("The condom broke? ...Honestly I don't care about that. But you HID it from me. That's the problem."),
            _("Look, %(pl)s's rule doesn't bother me. But lying to MY face? That's not cool."),
        ],
        "_default": [
            _("You KNEW the condom was broken?! %(pl)s said condom only! You broke %(poss)s trust AND mine!"),
            _("The condom tore and you hid it?! %(Pp)s trusted us to follow the rules! I can't believe you did this!"),
        ],
    }

    _NTR_GIRL_CBREAK_HIDDEN_EXCUSE = {
        "didnt_notice": {
            "cum_slut": [
                _("You 'didn't notice'? ...Fine. But %(pl)s is going to notice I'm dripping."),
                _("Didn't notice? ...I mean, it DID feel better. But %(pl)s is going to freak out."),
            ],
            "hate_cum": [
                _("Didn't NOTICE?! You were inside me RAW! %(pl)s trusted us! How do you NOT notice?!"),
                _("You didn't NOTICE?! There's cum inside me RIGHT NOW! %(pl)s said condom only! This is disgusting!"),
            ],
            "hardcore_sex": [
                _("Didn't notice? Whatever, the sex was fine. But %(pl)s trusted us. That's on you."),
                _("You didn't notice? ...I don't buy it. But even if true, %(pl)s is still going to be pissed."),
            ],
            "cute_sex": [
                _("You didn't notice? How?! %(pl)s trusted us! I feel so guilty right now..."),
                _("Didn't notice?! %(Pp)s set one rule and you couldn't even pay attention?! I feel terrible!"),
            ],
            "cheater": [
                _("Didn't notice? Sure. The condom I don't care about, but don't lie to me."),
                _("You 'didn't notice'? ...Whatever, %(pl)s's rule was dumb anyway. Just don't hide stuff from ME."),
            ],
            "_default": [
                _("You didn't notice? %(pl)s set ONE rule and you couldn't even check?! That's so irresponsible!"),
                _("How do you not notice?! %(Pp)s is going to be devastated if %(pp)s finds out!"),
            ],
        },
        "felt_too_good": {
            "cum_slut": [
                _("It felt too good? ...Yeah, it did. But %(pl)s is going to lose it if %(pp)s finds out."),
                _("Too good to stop? ...I get it, honestly. But %(pl)s had ONE rule and you broke it."),
            ],
            "hate_cum": [
                _("FELT TOO GOOD?! You chose how it FELT over %(pl)s's trust?! Over MY trust?! You're disgusting!"),
                _("Too good?! You had your cum inside me without protection! %(pl)s trusted us! I'm going to be sick!"),
            ],
            "hardcore_sex": [
                _("Felt too good? I get it, but %(pl)s trusted us. You should've said something."),
                _("Too good to stop? ...Fair. But hiding it was the wrong call. %(pl)s deserved better."),
            ],
            "cute_sex": [
                _("It felt too good?! That's your excuse?! %(pl)s trusted us and you just... didn't care?!"),
                _("Too good to stop?! %(Pp)s had ONE boundary! You could have at least TOLD me!"),
            ],
            "cheater": [
                _("Felt too good? Can't argue with that. But next time just tell me, I don't care about %(pl)s's rules."),
                _("Too good? Yeah, raw is better. Just don't hide it from ME next time, %(pl)s can deal with it."),
            ],
            "_default": [
                _("It felt too good?! So your pleasure was more important than %(pl)s's one rule?! And my consent?!"),
                _("You kept going because it felt good?! %(Pp)s trusted us! I trusted you! This is so selfish!"),
            ],
        },
        "moaned_louder": {
            "cum_slut": [
                _("Don't you DARE use my reactions to justify this! %(pl)s had ONE boundary!"),
                _("I moaned louder because it felt good, not because I wanted you to HIDE it! %(pl)s trusted us!"),
            ],
            "hate_cum": [
                _("My moaning?! You're blaming ME?! %(pl)s said condom only and you filled me with cum! YOU did this!"),
                _("Don't you DARE blame my reactions! I moaned because I didn't KNOW! %(pl)s is going to be furious!"),
            ],
            "hardcore_sex": [
                _("Don't blame me for your bad call. I was into it, sure. But %(pl)s's trust isn't a joke."),
                _("My reactions aren't your excuse. %(pl)s had ONE rule. Own what you did."),
            ],
            "cute_sex": [
                _("Don't blame MY reactions! I didn't know the condom was broken! %(pl)s trusted us!"),
                _("You're using my moaning as an excuse?! I feel so betrayed right now! %(Pp)s trusted us!"),
            ],
            "cheater": [
                _("I mean, yeah, it was hot. But blaming me? Just own it. I would've been fine with it anyway."),
                _("Don't need to justify it to me. I liked it raw. Just don't hide things, that's all I ask."),
            ],
            "_default": [
                _("Don't turn this on ME! %(pl)s set a boundary and you broke it behind BOTH our backs!"),
                _("My moaning doesn't give you permission to hide it! %(Pp)s trusted us and you threw that away!"),
            ],
        },
    }

    def _npc_video_reaction(npc, vid, girl_present=False):
        # girl_present: the video was posted in a group chat SHE is in. She already reacted live there,
        # so no next-day "he showed me the video" text.
        _girl_gid = vid.get("girl_gid", "")
        _face_hidden = vid.get("face_hidden", True)
        _is_partner_girl = (_girl_gid == npc.girl_gid)
        _trait = _npc_trait_key(npc)
        _girl = GIRL_BY_ID.get(_girl_gid)
        _girl_name = _girl.Name if _girl else "her"

        _vid_consensual = vid.get("consensual", True)
        _vid_type = vid.get("type", "unknown")

        if not _vid_consensual and _vid_type == "masturbate":
            if _is_partner_girl and not _face_hidden:
                _line = _tl(renpy.random.choice(_NPC_SECRET_MASTURBATION_LINES))
                Change_NPC_Status(npc, "friendship_with_player", -200)
                if _girl:
                    Change_Status(_girl, "Love", -50)
                    Change_Status(_girl, "Obed", -20)
                    Change_Status(_girl, "Inbt", 30)
                    _girl._npc_secret_vid_angry = True
                debug_log("[NPC_VIDEO] %s: SECRET masturbation vid of partner %s (face visible)! friend -200, girl stats changed" % (
                    npc.name, _girl_gid))
            else:
                _line = _tl(renpy.random.choice(_NPC_SECRET_MASTURBATION_GENERIC))
                Change_NPC_Status(npc, "friendship_with_player", -100)
                debug_log("[NPC_VIDEO] %s: SECRET masturbation vid (partner=%s fh=%s) of %s, friend -100" % (
                    npc.name, _is_partner_girl, _face_hidden, _girl_gid))
            return _line

        # ── Cuckold / Threesome video reactions ──
        _is_cuckold_vid = vid.get("cuckold", False)
        _is_threesome_vid = vid.get("threesome", False)
        if _is_cuckold_vid or _is_threesome_vid:
            _recorder_gid = vid.get("recorder_gid", "")
            _npc_was_recorder = (_recorder_gid == getattr(npc, "partner_id", ""))
            _npc_gf_is_subject = _is_partner_girl
            _npc_gf_is_recorder = (_recorder_gid == npc.girl_gid)
            _is_hostile_ntr = _ntr_is_hostile_mode(npc)
            _bl = getattr(npc, "_ntr_boundary_level", 1)

            if _is_cuckold_vid and _npc_was_recorder:
                # Player sends back the video HE recorded
                if _is_hostile_ntr:
                    _pool = _NPC_CUCKOLD_SELF_HOSTILE
                    _ntr_increase_boundary_bar(npc, _girl, 15) if _girl else None
                    Change_NPC_Status(npc, "friendship_with_player", -30)
                elif _bl >= 3:
                    _pool = _NPC_CUCKOLD_SELF_LEVEL3
                    _ntr_increase_boundary_bar(npc, _girl, 12) if _girl else None
                    Change_NPC_Status(npc, "friendship_with_player", 5)
                elif _bl >= 2:
                    _pool = _NPC_CUCKOLD_SELF_LEVEL2
                    _ntr_increase_boundary_bar(npc, _girl, 8) if _girl else None
                    Change_NPC_Status(npc, "friendship_with_player", -10)
                else:
                    _pool = _NPC_CUCKOLD_SELF_LEVEL0
                    _ntr_increase_boundary_bar(npc, _girl, 5) if _girl else None
                    Change_NPC_Status(npc, "friendship_with_player", -20)
                _line = _tl(renpy.random.choice(_pool))
                debug_log("[NPC_VIDEO] %s: CUCKOLD self-recorder vid, hostile=%s bl=%d" % (npc.name, _is_hostile_ntr, _bl))
                return _line

            elif _is_cuckold_vid and not _npc_was_recorder and not _npc_gf_is_subject:
                # NPC sees a cuckold video he wasn't involved in
                _ftier = _npc_friendship_tier(npc)
                _has_ntr = getattr(npc, "_ntr_active", False)
                if _has_ntr:
                    _pool = _NPC_CUCKOLD_OTHER_NTR
                elif _ftier == "friendly":
                    _pool = _NPC_CUCKOLD_OTHER_FRIENDLY
                else:
                    _pool = _NPC_CUCKOLD_OTHER_DEFAULT
                _line = _tl(renpy.random.choice(_pool))
                debug_log("[NPC_VIDEO] %s: CUCKOLD other vid, ntr=%s ftier=%s" % (npc.name, _has_ntr, _ftier))
                return _line

            elif _is_threesome_vid and _npc_gf_is_subject and not _face_hidden:
                # His GF is the subject (another girl recorded her getting fucked)
                _ntr_active = getattr(npc, "_ntr_active", False)
                if _ntr_active:
                    _vid_pos = vid.get("type", "unknown")
                    _vid_is_anal = _vid_pos in ("anal",) or (vid.get("is_anal", False))
                    _vid_condom = vid.get("condom", False)
                    _within = _ntr_act_within_boundary(_vid_pos, _bl, condom_active=_vid_condom, is_anal=_vid_is_anal)
                    if _within:
                        _pool = _NPC_THREESOME_GF_SUBJECT_NTR_IN
                        _ntr_increase_boundary_bar(npc, _girl, 10) if _girl else None
                    else:
                        _pool = _NPC_THREESOME_GF_SUBJECT_NO_NTR
                        Change_NPC_Status(npc, "friendship_with_player", -50)
                        if _girl:
                            _girl._ntr_violation_pending = True
                else:
                    _pool = _NPC_THREESOME_GF_SUBJECT_NO_NTR
                    Change_NPC_Status(npc, "friendship_with_player", -50)
                    npc.suspicion = min(100, npc.suspicion + 25)
                    if npc.suspicion >= 100 and _girl:
                        _girl._npc_video_pending = True
                _line = _tl(renpy.random.choice(_pool))
                debug_log("[NPC_VIDEO] %s: THREESOME gf_subject vid, ntr=%s bl=%d" % (npc.name, _ntr_active, _bl))
                return _line

            elif _is_threesome_vid and _npc_gf_is_recorder:
                # His GF held the camera while another girl got fucked
                if _is_hostile_ntr:
                    _pool = _NPC_THREESOME_GF_RECORDER_HOSTILE
                    Change_NPC_Status(npc, "friendship_with_player", -15)
                    npc.suspicion = min(100, npc.suspicion + 15)
                elif _bl >= 2:
                    _pool = _NPC_THREESOME_GF_RECORDER_HIGH
                    _ntr_increase_boundary_bar(npc, _girl, 5) if _girl else None
                    npc.suspicion = min(100, npc.suspicion + 10)
                else:
                    _pool = _NPC_THREESOME_GF_RECORDER_LOW
                    Change_NPC_Status(npc, "friendship_with_player", -15)
                    npc.suspicion = min(100, npc.suspicion + 25)
                _line = _tl(renpy.random.choice(_pool))
                debug_log("[NPC_VIDEO] %s: THREESOME gf_recorder vid, hostile=%s bl=%d" % (npc.name, _is_hostile_ntr, _bl))
                return _line

            elif _is_cuckold_vid and _npc_gf_is_subject and not _npc_was_recorder and not _face_hidden:
                # His GF is in a cuckold video but a DIFFERENT NPC recorded
                _ntr_active = getattr(npc, "_ntr_active", False)
                if _ntr_active:
                    _pool = _NPC_THREESOME_GF_SUBJECT_NTR_IN
                    _ntr_increase_boundary_bar(npc, _girl, 10) if _girl else None
                else:
                    _pool = _NPC_THREESOME_GF_SUBJECT_NO_NTR
                    Change_NPC_Status(npc, "friendship_with_player", -50)
                    npc.suspicion = min(100, npc.suspicion + 25)
                    if npc.suspicion >= 100 and _girl:
                        _girl._npc_video_pending = True
                _line = _tl(renpy.random.choice(_pool))
                debug_log("[NPC_VIDEO] %s: CUCKOLD gf_subject (diff recorder) vid, ntr=%s" % (npc.name, _ntr_active))
                return _line

        # NTR-active partner: classify video by boundary level + traits
        _ntr_active_check = getattr(npc, "_ntr_active", False)
        _ntr_just_activated = False
        if _is_partner_girl and not _face_hidden and not _ntr_active_check and npc.has_trait("ntr") and _girl and not _girl.has_trait("lesbian"):
            _ntr_activate(_girl, npc)
            _ntr_active_check = True
            _ntr_just_activated = True
            debug_log("[NPC_VIDEO] %s: auto-activated NTR for partner vid (trait present, _ntr_active was False)" % npc.name)
        if _is_partner_girl and _ntr_active_check and not _ntr_just_activated and _girl and not _girl.has_trait("lesbian") and getattr(_girl, "_ntr_boundary_discovered", False):
            _vid_pos = vid.get("type", "unknown")
            _vid_is_anal = _vid_pos in ("anal",) or (vid.get("is_anal", False))
            _vid_condom = vid.get("condom", False)
            _bl = getattr(npc, "_ntr_boundary_level", 1)
            _within = _ntr_act_within_boundary(_vid_pos, _bl, condom_active=_vid_condom, is_anal=_vid_is_anal)
            _is_cam = npc.has_trait("camera_lover")
            _is_voyeur = npc.has_trait("voyeur")

            _is_hostile_ntr = _ntr_is_hostile_mode(npc)
            if _within:
                if _is_hostile_ntr:
                    if _is_cam and _face_hidden:
                        _line = _tl(renpy.random.choice(_NTR_VIDEO_HOSTILE_WITHIN_HIDDEN_LINES))
                        _bar_gain = 14
                    elif _is_cam:
                        _line = _tl(renpy.random.choice(_NTR_VIDEO_HOSTILE_WITHIN_CAMERA_LINES))
                        _bar_gain = 18
                    elif _is_voyeur:
                        _line = _tl(renpy.random.choice(_NTR_VIDEO_HOSTILE_WITHIN_VOYEUR_LINES))
                        _bar_gain = 14
                    elif _face_hidden:
                        _line = _tl(renpy.random.choice(_NTR_VIDEO_HOSTILE_WITHIN_HIDDEN_LINES))
                        _bar_gain = 10
                    else:
                        _line = _tl(renpy.random.choice(_NTR_VIDEO_HOSTILE_WITHIN_LINES))
                        _bar_gain = 12
                elif _is_cam and _face_hidden:
                    _line = _tl(renpy.random.choice(_NTR_VIDEO_WITHIN_CAMERA_HIDDEN_LINES))
                    _bar_gain = 12
                elif _is_cam:
                    _line = _tl(renpy.random.choice(_NTR_VIDEO_WITHIN_CAMERA_LINES))
                    _bar_gain = 15
                elif _is_voyeur:
                    _line = _tl(renpy.random.choice(_NTR_VIDEO_WITHIN_VOYEUR_LINES))
                    _bar_gain = 12
                elif _face_hidden:
                    _line = _tl(renpy.random.choice(_NTR_VIDEO_WITHIN_HIDDEN_LINES))
                    _bar_gain = 8
                else:
                    _line = _tl(renpy.random.choice(_NTR_VIDEO_WITHIN_LINES))
                    _bar_gain = 10
                _ntr_increase_boundary_bar(npc, _girl, _bar_gain)
                debug_log("[NTR_VIDEO] %s: vid of %s WITHIN bounds (pos=%s bl=%d cam=%s voy=%s fh=%s hostile=%s), bar +%d" % (
                    npc.name, _girl_gid, _vid_pos, _bl, _is_cam, _is_voyeur, _face_hidden, _is_hostile_ntr, _bar_gain))
            else:
                if _is_hostile_ntr:
                    _line = _tl(renpy.random.choice(_NTR_VIDEO_HOSTILE_OUTSIDE_LINES))
                    Change_NPC_Status(npc, "friendship_with_player", -30)
                    _old_bar = getattr(npc, "_ntr_boundary_bar", 0)
                    npc._ntr_boundary_bar = max(0, _old_bar - 10)
                    debug_log("[NTR_VIDEO] %s: vid of %s OUTSIDE bounds HOSTILE (pos=%s bl=%d), friend -30, bar -10" % (
                        npc.name, _girl_gid, _vid_pos, _bl))
                else:
                    _line = _tl(renpy.random.choice(_NTR_VIDEO_OUTSIDE_LINES))
                    Change_NPC_Status(npc, "friendship_with_player", -50)
                    _old_bar = getattr(npc, "_ntr_boundary_bar", 0)
                    npc._ntr_boundary_bar = max(0, _old_bar - 20)
                    debug_log("[NTR_VIDEO] %s: vid of %s OUTSIDE bounds (pos=%s bl=%d), friend -50, bar -20" % (
                        npc.name, _girl_gid, _vid_pos, _bl))
                _girl._ntr_boundary_bar = npc._ntr_boundary_bar
                _girl._ntr_violation_pending = True
            if not _face_hidden:
                # This branch is NTR active + boundary discovered: the partner is in on it. No suspicion (it
                # is frozen once NTR is discovered anyway), no breakup processing, no group dissolve.
                # Outside-bounds videos are already handled by _ntr_violation_pending above.
                if _within and not girl_present:
                    _girl._ntr_video_seen_pending = True
                debug_log("[NPC_VIDEO] %s: face-visible NTR vid of %s within=%s girl_present=%s -> seen_pending=%s" % (npc.name, _girl_gid, _within, girl_present, _within and not girl_present))
            return _line

        if _is_partner_girl and not _face_hidden:
            _exposed_pool = _NPC_VIDEO_PARTNER_EXPOSED.get(_trait, _NPC_VIDEO_PARTNER_EXPOSED["neutral"])
            if _girl and _girl.has_trait("lesbian") and _trait == "ntr":
                _exposed_pool = _NTR_VIDEO_LESBIAN_EXPOSED
            if isinstance(_exposed_pool, dict):
                pool = _exposed_pool.get(_vid_type, _exposed_pool.get("_default", [_("Wait... is that %s? Tell me more.")]))
            else:
                pool = _exposed_pool
            _line = _tl(renpy.random.choice(pool))
            if "%s" in _line:
                _line = _line % _girl_name

            if _trait == "proud":
                Change_NPC_Status(npc, "friendship_with_player", -200)
                npc.suspicion = 100
            elif _trait == "ntr":
                Change_NPC_Status(npc, "friendship_with_player", -20)
                npc.suspicion = 100
            else:
                Change_NPC_Status(npc, "friendship_with_player", -100)
                npc.suspicion = 100

            if npc.suspicion >= 100:
                _girl._npc_video_pending = True

            debug_log("[NPC_VIDEO] %s: EXPOSED face of %s! trait=%s susp=%d friend=%d" % (
                npc.name, _girl_gid, _trait, npc.suspicion, npc.friendship_with_player))
            return _line

        elif _is_partner_girl and _face_hidden:
            _susp_tier = _npc_suspicion_tier(npc)
            pool = _NPC_VIDEO_PARTNER_HIDDEN.get((_susp_tier, _trait), _NPC_VIDEO_PARTNER_HIDDEN[("low", "neutral")])
            _line = _tl(renpy.random.choice(pool))
            Change_NPC_Status(npc, "suspicion", 10)
            debug_log("[NPC_VIDEO] %s: hidden face of partner %s, susp_tier=%s +10 susp (now %d)" % (
                npc.name, _girl_gid, _susp_tier, npc.suspicion))
            return _line

        else:
            _ftier = _npc_friendship_tier(npc)
            pool = _NPC_VIDEO_UNRELATED.get((_ftier, _trait), _NPC_VIDEO_UNRELATED[("neutral", "neutral")])
            _line = _tl(renpy.random.choice(pool))

            if not _face_hidden and _girl:
                _gossip = getattr(store.Player, "campus_gossip", set())
                if not hasattr(store.Player, "campus_gossip"):
                    store.Player.campus_gossip = set()
                store.Player.campus_gossip.add(_girl_gid)
                _partner_npc = get_npc_partner_for(_girl)
                if _partner_npc:
                    Change_NPC_Status(_partner_npc, "suspicion", 10)
                    debug_log("[NPC_VIDEO] %s: unrelated face-visible vid of %s, +10 susp on partner %s (now %d)" % (
                        npc.name, _girl_gid, _partner_npc.name, _partner_npc.suspicion))

            debug_log("[NPC_VIDEO] %s: unrelated vid of %s, friendship=%s trait=%s face_hidden=%s" % (
                npc.name, _girl_gid, _ftier, _trait, _face_hidden))
            return _line

    # ── Scene rendering ──

    def resolve_npc_for_location(location):
        """Determine which NPC (if any) should appear at this location.
        Sets store._npc_on_scene. Does NOT render -- Set_Scene handles slots."""
        store._npc_on_scene = None

        for npc in NPC_PARTNERS.values():
            npc.hide_sprite()

        if getattr(store, "_in_event", False) or getattr(store, "_in_intro", False):
            return

        candidates = []
        girls_here = [g for g in ALL_GIRLS if g.loc == location]
        for g in girls_here:
            npc = get_npc_partner_for(g)
            if npc and npc.loc == location:
                candidates.append(npc)

        for npc in NPC_PARTNERS.values():
            if npc.loc == location and npc not in candidates:
                candidates.append(npc)

        if not candidates:
            return

        npc = candidates[0]

        if renpy.random.random() > NPC_APPEAR_CHANCE:
            return

        store._npc_on_scene = npc
        debug_log("[NPC_PARTNER] %s resolved at %s" % (npc.name, location))

    # ── NPC Witness Detection ──

    _NPC_DETECT_BASE = {
        "kiss":            {"room": 50, "public": 15},
        "rub":             {"room": 40, "public": 10},
        "hj":              {"room": 90, "public": 40},
        "bj":              {"room": 90, "public": 40},
        "tj":              {"room": 90, "public": 40},
        "sex":             {"room": 95, "public": 45},
        "cowgirl":         {"room": 95, "public": 45},
        "reverse_cowgirl": {"room": 95, "public": 45},
        "doggy":           {"room": 95, "public": 45},
        "anal":            {"room": 95, "public": 45},
        "massage":         {"room": 0,  "public": 0},
    }

    _NPC_ROOM_LOCATIONS = {"room", "gwen_room", "rogue_room", "ntw_room", "tenny_room"}

    def _npc_crowd_detect_mod():
        """Convert crowd level 0-100 to detection modifier (-20 to +10)."""
        cl = getattr(store, "_crowd_level", 0)
        if cl <= 0:
            return -20
        if cl <= 20:
            return -10
        if cl <= 50:
            return 0
        return 10

    def npc_partner_detection_roll(npc, girl, act_type):
        if act_type == "massage":
            return False

        loc = getattr(store, "CurrentLocation", "room")
        is_room = _is_room_location(loc)
        loc_key = "room" if is_room else "public"

        act_data = _NPC_DETECT_BASE.get(act_type, _NPC_DETECT_BASE.get("sex"))
        base = act_data.get(loc_key, 40)

        # NPC already in the room — guaranteed detection
        if npc is getattr(store, "_npc_on_scene", None) and is_room:
            debug_log("[NPC_DETECT] %s is ON SCENE in room -> auto-detect" % npc.name)
            return True
        elif not is_room:
            base += _npc_crowd_detect_mod()
        elif is_room and not _is_door_open(loc):
            base -= 30

        if getattr(npc, "_ntr_active", False) and npc.has_trait("voyeur"):
            base += 20

        base = max(0, min(100, base))
        roll = renpy.random.randint(1, 100)
        detected = roll <= base

        debug_log("[NPC_DETECT] %s act=%s loc=%s base=%d roll=%d -> %s" % (
            npc.name, act_type, loc, base, roll, "DETECTED" if detected else "missed"))
        return detected

    def npc_partner_witness_check(girl, act_type):
        if getattr(store, "_scene_restricted", False):
            return None
        if getattr(store, "_npc_witness_check_done", False):
            return None
        if getattr(store, "_hangout_running", False):
            # a RUNNING hangout has no partner walk-ins (the scheduled list used to sit here
            # and silently disabled every catch for the rest of the invite day)
            return None
        if getattr(girl, "_npc_catch_pending", False):
            # already caught today: the partner is dealing with it, never a second catch
            return None
        if not girl.has_npc_partner():
            return None
        npc = get_npc_partner_for(girl)
        if npc is None:
            return None
        loc = getattr(store, "CurrentLocation", "room")
        if npc.loc != loc:
            return None
        if store.door_locked:
            debug_log("[NPC_DETECT] Door locked, %s cannot walk in" % npc.name)
            return None
        if not npc_partner_detection_roll(npc, girl, act_type):
            return None

        store._npc_witness_check_done = True
        store._npc_witness_npc = npc
        store._npc_witness_detected = True
        return npc

    def _npc_witness_is_girls_partner(npc, girl):
        return npc.girl_gid == girl.gid

    # ── Act Severity System ──
    _NPC_ACT_SEVERITY = {
        "kiss": "mild", "rub": "mild", "massage": "mild", "tip": "mild",
        "hj": "moderate", "bj": "moderate", "tj": "moderate",
        "sex": "severe", "cowgirl": "severe", "reverse_cowgirl": "severe",
        "doggy": "severe", "full_nelson": "severe",
        "anal": "extreme", "doggy_anal": "extreme", "full_nelson_anal": "extreme",
        "laying_down": "severe", "laying_anal": "extreme",
        "reverse_cowgirl_anal": "extreme",
    }
    _NPC_SEVERITY_F_SHIFT = {"mild": 100, "moderate": 0, "severe": -100, "extreme": -200}
    _NPC_SEVERITY_STAT_MULT = {"mild": 0.5, "moderate": 1.0, "severe": 1.5, "extreme": 2.0}

    def _npc_act_severity(act_type):
        return _NPC_ACT_SEVERITY.get(act_type, "moderate")

    def _npc_witness_reaction_type(npc, girl, act_type=None):
        if not _npc_witness_is_girls_partner(npc, girl):
            return "public_boost"
        sev = _npc_act_severity(act_type) if act_type else "moderate"
        f = npc.friendship_with_player + _NPC_SEVERITY_F_SHIFT.get(sev, 0)
        l = npc.love_for_girl
        if f < 200:
            return "furious"
        elif f < 400:
            return "angry"
        elif l >= 700:
            return "sad"
        else:
            return "confused"

    # ── Severity-Specific Witness Dialogue Pools ──
    _NPC_WITNESS_LINES = {
        ("furious", "mild"): [
            _("Keep your hands off %(girl_name)s! Who the hell do you think you are?!"),
            _("You think you can just touch my %(pl)s like that?! Get the fuck away from her!"),
            _("I saw that! Don't you DARE put your hands on %(girl_name)s again!"),
        ],
        ("angry", "mild"): [
            _("Really, %(girl_name)s? That's what you're doing behind my back?"),
            _("I saw that. Don't try to deny it, %(girl_name)s. We need to talk."),
            _("So you're just going to fool around with this guy? How long, %(girl_name)s?"),
        ],
        ("sad", "mild"): [
            _("I saw you two... the kiss. I thought we had something real, %(girl_name)s."),
            _("%(girl_name)s... you were kissing him. Do I mean that little to you?"),
            _("That kiss meant something, didn't it? Don't lie to me, %(girl_name)s..."),
        ],
        ("confused", "mild"): [
            _("Wait... was that... were you two just...? %(girl_name)s?"),
            _("Did I just see what I think I saw? %(girl_name)s, care to explain?"),
            _("Hold on. Were you... kissing him? I must be seeing things."),
        ],
        ("furious", "moderate"): [
            _("%(girl_name)s?! What are you DOING?! I can't believe this!"),
            _("What the FUCK?! %(girl_name)s?! With HIM?! We're DONE!"),
            _("Are you kidding me right now?! That's MY %(pl)s!"),
        ],
        ("angry", "moderate"): [
            _("%(girl_name)s... what is this? I can't believe what I'm seeing."),
            _("So this is what you do when I'm not around? How long, %(girl_name)s?"),
            _("I can't believe what I'm seeing right now... %(girl_name)s, we need to talk."),
        ],
        ("sad", "moderate"): [
            _("I... I thought we had something special, %(girl_name)s..."),
            _("%(girl_name)s... why? I thought you loved me..."),
            _("You're really doing this to me? To us? I don't understand..."),
        ],
        ("confused", "moderate"): [
            _("Wait... %(girl_name)s? What's happening here?"),
            _("Hold on... is this what I think it is? %(girl_name)s?"),
            _("I... what? %(girl_name)s, what are you doing?"),
        ],
        ("furious", "severe"): [
            _("You're FUCKING him?! Right here?! We're done, %(girl_name)s! DONE!"),
            _("I'm watching my %(pl)s get FUCKED and you don't even care?! I'll kill you both!"),
            _("%(girl_name)s is having SEX with this guy?! Are you fucking SERIOUS right now?!"),
        ],
        ("angry", "severe"): [
            _("You're having SEX with him?! How could you do this to me, %(girl_name)s?!"),
            _("You're actually... sleeping with him. I can't even process this right now."),
            _("%(girl_name)s, you're literally fucking another person! Do I mean NOTHING to you?!"),
        ],
        ("sad", "severe"): [
            _("You're... sleeping with someone else... I don't even know what to say, %(girl_name)s."),
            _("I loved you, %(girl_name)s. And this is what I walk in on... you having sex with him."),
            _("I can see everything... I wish I could unsee it. Why, %(girl_name)s?"),
        ],
        ("confused", "severe"): [
            _("Wait... are you two actually... having sex? %(girl_name)s, what the hell?"),
            _("I... is this really happening? %(girl_name)s, are you seriously doing this?"),
            _("Am I dreaming? That's... my %(pl)s. With another guy. Inside her."),
        ],
        ("furious", "extreme"): [
            _("You're letting him fuck your ASS?! You never even let ME do that!! We're DONE!"),
            _("ANAL?! With HIM?! I can't believe what I'm seeing, %(girl_name)s!!"),
            _("That's IT!! %(girl_name)s takes it in the ass for some random guy?! I'm DONE!!"),
        ],
        ("angry", "extreme"): [
            _("You're doing... THAT... with him? %(girl_name)s, this is beyond anything I expected."),
            _("Anal? Really, %(girl_name)s? With this guy? I don't even know who you are anymore."),
            _("I never thought you'd... %(girl_name)s, you crossed every line there is."),
        ],
        ("sad", "extreme"): [
            _("You're letting him do that to you... I'll never get this image out of my head, %(girl_name)s."),
            _("I always respected your limits. And here you are... letting someone else cross them all."),
            _("%(girl_name)s... seeing you like this... with him... I have no words."),
        ],
        ("confused", "extreme"): [
            _("Is that... wait... are you doing... that? %(girl_name)s, I don't understand."),
            _("Did I just see... %(girl_name)s, what are you... I can't even say it."),
            _("I... that's... what? %(girl_name)s, I need to sit down."),
        ],
    }

    def _format_npc_line(npc, line, girl=None):
        """Translate a line about an NPC (or said to him) and fill its keys: he / she of the NPC (gender_fmt; %(ga)s =
        the PT / ES ending about HIM / HER, "relajad%(ga)s" in the ES pools of hangout_tod_bf), his name, "girlfriend"
        = the girl (partner_label_fmt). The translation decides, as in _format_partner_line."""
        if not line:
            return line
        _t = _tl(line)
        if "%(" not in _t:
            return _t
        _is_f = getattr(npc, "gender", "male") == "female"
        _d = gender_fmt(_is_f)
        _d.update(partner_label_fmt(True, _tr("girlfriend")))
        _d["name"] = getattr(npc, "Name", "")
        _d["pub_desc"] = _tr("A girl") if _is_f else _tr("A guy")
        if girl:
            _d["girl_name"] = girl.Name
        return fmt_safe(_t, _d, line)

    def _girl_accepts_npc_witness(girl, npc):
        if girl.has_trait("loyal"):
            return False
        if girl.has_trait("cheater"):
            return True
        if girl.Love >= 800:
            return True
        if getattr(girl, "bf_loyalty", 750) < 300:
            return True
        if girl.has_trait("exhibitionist"):
            return True
        if girl.Obed >= 700:
            return True
        return False

    def _girl_continues_after_catch(girl):
        if girl.has_trait("lesbian"):
            return False
        if girl.has_trait("loyal"):
            return False
        if girl.has_trait("cheater"):
            return True
        if girl.has_trait("exhibitionist"):
            return True
        if (girl.Obed + girl.Inbt) / 2 >= 500:
            return True
        return False

    def _npc_breakup_decision(girl, npc):
        if npc.has_trait("proud"):
            debug_log("[NPC_BREAKUP] %s proud -> breakup" % npc.name)
            return True
        if npc.has_trait("ntr") or getattr(npc, "_ntr_active", False):
            if not getattr(npc, "_ntr_active", False) and not girl.has_trait("lesbian"):
                _ntr_activate(girl, npc)
            elif getattr(npc, "_ntr_active", False) and not getattr(girl, "_ntr_boundary_discovered", False) and not girl.has_trait("lesbian"):
                girl._ntr_activation_pending = True
                debug_log("[NTR_ACTIVATE] %s born-NTR, queuing activation message" % npc.name)
            debug_log("[NPC_BREAKUP] %s ntr -> stays" % npc.name)
            return False

        count = getattr(girl, "_npc_catch_count", 1)

        # Lesbian GF: much harder to break up. She rationalizes, denies, forgives.
        if girl.has_trait("lesbian"):
            if count < 3:
                debug_log("[NPC_BREAKUP] %s lesbian GF catch #%d -> stays (needs 3+)" % (npc.name, count))
                return False
            if count >= 5 and not npc.has_trait("ntr"):
                npc.add_trait("ntr")
                girl._npc_partner_traits = set(npc.traits)
                debug_log("[NPC_BREAKUP] %s lesbian 5+ catches -> gained ntr, stays" % npc.name)
                return False
            chances_les = {3: 0.15, 4: 0.30, 5: 0.50}
            chance = chances_les.get(count, 0.50)
            result = renpy.random.random() < chance
            debug_log("[NPC_BREAKUP] %s lesbian count=%d chance=%.0f%% -> %s" % (npc.name, count, chance*100, "breakup" if result else "stays"))
            return result

        if count >= 3 and not npc.has_trait("ntr"):
            npc.add_trait("ntr")
            girl._npc_partner_traits = set(npc.traits)
            debug_log("[NPC_BREAKUP] %s 3+ catches -> gained ntr, stays" % npc.name)
            return False

        chances = {1: 0.30, 2: 0.55, 3: 0.80}
        chance = chances.get(count, 0.80)
        result = renpy.random.random() < chance
        debug_log("[NPC_BREAKUP] %s count=%d chance=%.0f%% -> %s" % (npc.name, count, chance*100, "breakup" if result else "stays"))
        return result

    # ── Pregnancy: does he forgive her? ──
    # He found out the baby is not his and she asked him to stay (label _npc_pregnancy_breakup, "Try to work
    # things out" also costs him 200 love for her). The next morning he decides (author, 2026-09-19): his love
    # for her sets the chance he walks out; an NTR partner she has not caught on to yet (born NTR, or active and
    # undiscovered; never a lesbian's partner) is more forgiving the higher his boundary level, and at the top
    # level he stays AND raises the child as his (_npc_paternity_claimed, the "I'll raise the kid" of the NTR
    # partner who already knew). A proud partner never gets here (he leaves on the spot).
    NPC_PREGNANCY_LEAVE_CHANCE = ((700, 0.35), (400, 0.60), (0, 0.85))   # (his love for her at least, chance he leaves)
    NPC_PREGNANCY_NTR_LEAVE_MULT = {1: 0.75, 2: 0.50, 3: 0.25}           # x that chance, by NTR boundary level
    NPC_PREGNANCY_RAISE_LEVEL = 4                                          # "No limits": he raises the child
    # Her texts the morning after, in order. %(pn)s / %(Pn)s = his name, %(pp)s %(Pp)s %(po)s %(poss)s = his
    # pronouns (_format_partner_line: a girlfriend reads she / her). "lesbian" = her own words, else "_default".
    NPC_PREGNANCY_VERDICT_MSGS = {
        "left": {
            "_default": [
                _("I told %(pn)s the truth. All of it. %(Pp)s packed a bag before I even finished."),
                _("%(Pp)s said %(pp)s can't raise another man's baby. I don't even know how to argue with that."),
            ],
            "lesbian": [
                _("I told %(pn)s everything. %(Pp)s said %(pp)s can't stay with me while I carry a man's baby."),
                _("So that's it. I lost %(po)s. Over you. Over this."),
            ],
        },
        "forgave": {
            "_default": [
                _("I talked to %(pn)s all night. %(Pp)s is staying. I still don't understand why."),
                _("%(Pp)s knows the baby isn't %(poss)s. We're going to try anyway. Please don't make this harder."),
            ],
            "lesbian": [
                _("%(Pn)s is staying. We both cried all night, and somehow %(pp)s still wants me."),
                _("%(Pp)s knows it's yours. Please give us some space for a while."),
            ],
        },
        "raise": {
            "_default": [
                _("%(Pn)s isn't leaving. And it gets stranger."),
                _("%(Pp)s said %(pp)s'll raise the baby as %(poss)s own. %(Pp)s didn't even sound angry. More like... excited."),
                _("I don't know what to feel. But this baby won't grow up without a family."),
            ],
        },
    }

    def _npc_pregnancy_verdict(girl, npc):
        """His answer, the morning after she asked him to stay: "left", "forgave" or "raise" (he stays and raises
        the child). Logged with every number that decided it."""
        if npc.has_trait("proud"):
            print("[NPC_BREAKUP] %s pregnancy verdict: proud -> left" % npc.name)
            return "left"
        _love = npc.love_for_girl
        _chance = next(_c for _min, _c in NPC_PREGNANCY_LEAVE_CHANCE if _love >= _min)
        _ntr = (npc.has_trait("ntr") or getattr(npc, "_ntr_active", False)) and not girl.has_trait("lesbian")
        _lvl = getattr(npc, "_ntr_boundary_level", 1)
        if _ntr and _lvl >= NPC_PREGNANCY_RAISE_LEVEL:
            print("[NPC_BREAKUP] %s pregnancy verdict: love=%d NTR level %d -> raise" % (npc.name, _love, _lvl))
            return "raise"
        if _ntr:
            _chance *= NPC_PREGNANCY_NTR_LEAVE_MULT.get(_lvl, 1.0)
        _roll = renpy.random.random()
        _verdict = "left" if _roll < _chance else "forgave"
        print("[NPC_BREAKUP] %s pregnancy verdict: love=%d ntr=%s level=%d chance=%.0f%% roll=%.2f -> %s" % (
            npc.name, _love, _ntr, _lvl, _chance * 100, _roll, _verdict))
        return _verdict

    def _npc_raises_child(girl, npc, why):
        """He takes the baby on as his own KNOWING it is the player's (NTR, "No limits"): he stands as the father
        from now on (child_npc_is_father: no child support from the player). Both ways in: the NTR partner who
        already knew (label _npc_pregnancy_breakup) and the morning-after verdict "raise"."""
        girl._npc_paternity_claimed = True
        unlock_achievement("eyes_wide_open")
        print("[NPC_BREAKUP] %s raises %s's baby as his own, knowing it is the player's (%s)" % (npc.name, girl.gid, why))

    def _npc_pregnancy_verdict_msgs(girl, verdict):
        _pool = NPC_PREGNANCY_VERDICT_MSGS[verdict]
        _lines = _pool["lesbian"] if girl.has_trait("lesbian") and "lesbian" in _pool else _pool["_default"]
        return [_format_partner_line(girl, _l) for _l in _lines]

    def _npc_ntr_learns(girl, npc, reason):
        """An NTR partner (born or active) who just learned about the player and stays: a born one wakes up
        (_ntr_activate), an active one she has not caught on to yet tells her he knows (activation message).
        Never for a lesbian (the NTR boundary system does not apply to her)."""
        if girl.has_trait("lesbian"):
            return
        if not getattr(npc, "_ntr_active", False):
            if npc.has_trait("ntr"):
                _ntr_activate(girl, npc)
        elif not getattr(girl, "_ntr_boundary_discovered", False):
            girl._ntr_activation_pending = True
            debug_log("[NTR_ACTIVATE] %s born-NTR, queuing activation message (reason=%s)" % (npc.name, reason))

    def _npc_process_breakup(girl, reason):
        """
        Unified NPC breakup processing. Called next day after the event.
        reason: "caught" (NPC witnessed), "suspicion" (suspicion reached 100), "video" (face-visible video sent)
        or "pregnancy" (he found out the baby is not his and she asked him to stay: _npc_pregnancy_verdict)
        """
        npc = get_npc_partner_for(girl)
        if npc is None:
            debug_log("[NPC_BREAKUP] %s: no NPC partner found, aborting (reason=%s)" % (girl.gid, reason))
            return

        if reason == "video" and _ntr_active_discovered(girl):
            # Flag queued by older builds for an NTR-known partner. He already knows: skip the breakup /
            # "are you out of your mind?!" path. An outside-bounds video gets its own fight text instead.
            if not getattr(girl, "_ntr_violation_pending", False):
                _ntr_video_seen_next_day(girl)
            print("[NPC_BREAKUP] %s: video reason ignored, NTR known" % girl.gid)
            return

        debug_log("[NPC_BREAKUP] Processing %s reason=%s" % (girl.gid, reason))

        _contacts = getattr(store.Player, "phone_contacts", set())
        if girl.gid not in _contacts:
            store.Player.phone_contacts.add(girl.gid)
            phone_add_msg(girl.gid, girl.gid, _tl_fmt(_("Hey, it's %s. I got your number from the class group."), girl.Name), "text")

        _plabel = girl.partner_label()
        _pp = _tr("she") if girl.get_flag("partner_is_female") else _tr("he")
        _Pp = _tr("She") if girl.get_flag("partner_is_female") else _tr("He")
        _po = _tr("her_obj") if girl.get_flag("partner_is_female") else _tr("him")
        _npc_name = npc.Name if hasattr(npc, "Name") else _plabel
        _is_lesbian = girl.has_trait("lesbian")
        _is_cheater = girl.has_trait("cheater")
        _is_loyal = girl.has_trait("loyal")
        # acts only: positions are preferences, a cowgirl scene would count twice
        _total_acts = sum(_v for _k, _v in getattr(girl, "Sex_acts", {}).items() if _k not in _SEX_POSITION_KEYS)
        _catch_count = getattr(girl, "_npc_catch_count", 1)
        _bf_loyalty = getattr(girl, "bf_loyalty", 500)

        # ── Decision ──
        _preg_verdict = None
        if reason == "caught":
            broke_up = _npc_breakup_decision(girl, npc)
        elif reason == "pregnancy":
            _preg_verdict = _npc_pregnancy_verdict(girl, npc)
            broke_up = _preg_verdict == "left"
            if not broke_up and (npc.has_trait("ntr") or getattr(npc, "_ntr_active", False)):
                _npc_ntr_learns(girl, npc, reason)
        else:
            if npc.has_trait("proud"):
                broke_up = True
            elif npc.has_trait("ntr") or getattr(npc, "_ntr_active", False):
                broke_up = False
                _npc_ntr_learns(girl, npc, reason)
            else:
                _love = npc.love_for_girl
                if _love >= 700:
                    chance = 0.20
                elif _love >= 400:
                    chance = 0.40
                else:
                    chance = 0.70
                broke_up = renpy.random.random() < chance
                debug_log("[NPC_BREAKUP] %s suspicion: love=%d chance=%.0f%% -> %s" % (npc.name, _love, chance*100, "breakup" if broke_up else "stays"))

        # ── Messages ──
        _pending_msgs = []

        if broke_up:
            if reason == "caught":
                if _is_lesbian:
                    _pending_msgs.append(_tl_fmt(_("I talked to %s. We broke up. %s couldn't handle finding me with a man."), _npc_name, _Pp))
                    if _total_acts >= SEX_HISTORY_THRESHOLDS["breakup_lesbian_identity_acts"]:
                        _pending_msgs.append(_("I don't even know what I am anymore. I keep doing things with you that I shouldn't want. But I do."))
                    else:
                        _pending_msgs.append(_("I'm a lesbian who lost her girlfriend because of a guy. I hope you're happy."))
                elif _is_cheater:
                    _pending_msgs.append(_tl_fmt(_("So... %s and I are done. %s found out and honestly? I'm relieved."), _npc_name, _Pp))
                    _pending_msgs.append(_("Now we don't have to sneak around. Come find me whenever you want."))
                elif _bf_loyalty < 300 or _total_acts >= SEX_HISTORY_THRESHOLDS["breakup_heavy_history_acts"]:
                    _pending_msgs.append(_tl_fmt(_("I talked to %s. It's over. Things weren't good between us anyway."), _npc_name))
                    _pending_msgs.append(_("Honestly, it was a matter of time. What we did just sped things up."))
                elif _is_loyal:
                    _pending_msgs.append(_tl_fmt(_("I talked to %s. We're done. %s couldn't forgive me and I don't blame %s."), _npc_name, _Pp, _po))
                    _pending_msgs.append(_("I hope you understand how much this cost me. Please don't contact me for a while."))
                else:
                    _pending_msgs.append(_tl_fmt(_("Hey... I talked to %s. We broke up. Because of what happened."), _npc_name))
                    _pending_msgs.append(_("I hope you're happy. You ruined my relationship."))
            elif reason == "video":
                _girl_love = getattr(girl, "Love", 0)
                if _girl_love >= 600:
                    _pending_msgs.append(_tl_fmt(_("You sent a video of us to %s? What were you thinking?"), _npc_name))
                    _pending_msgs.append(_tl_fmt(_("%s showed it to me. I couldn't even deny it."), _Pp))
                    _pending_msgs.append(_("We broke up. I need some time to process this."))
                    Change_Status(girl, "Love", -10)
                    girl.set_temp_status("sad", 1)
                elif _girl_love >= 300:
                    _pending_msgs.append(_tl_fmt(_("Are you insane?! You sent %s a video of us?!"), _npc_name))
                    _pending_msgs.append(_("My relationship is over because YOU decided to show off!"))
                    _pending_msgs.append(_("I can't believe I trusted you."))
                    Change_Status(girl, "Love", -25)
                    girl.set_temp_status("angry", 1)
                else:
                    _pending_msgs.append(_tl_fmt(_("%s broke up with me because of YOUR video!"), _npc_name))
                    _pending_msgs.append(_("You ruined everything! I never want to see your face again!"))
                    Change_Status(girl, "Love", -50)
                    girl.set_temp_status("angry", 2)
            elif reason == "pregnancy":
                _pending_msgs.extend(_npc_pregnancy_verdict_msgs(girl, "left"))
            else:
                if _is_lesbian:
                    _pending_msgs.append(_tl_fmt(_("%s sat me down last night. %s said %s had been watching, noticing things."), _npc_name, _Pp, _pp))
                    _pending_msgs.append(_tl_fmt(_("%s asked if I had feelings for you. I couldn't even look %s in the eye."), _Pp, _po))
                    _pending_msgs.append(_tl_fmt(_("We're done. %s said %s deserves someone who isn't confused."), _Pp, _pp))
                elif _is_cheater:
                    _pending_msgs.append(_tl_fmt(_("So %s finally snapped. Cornered me and started asking questions I couldn't answer."), _npc_name))
                    _pending_msgs.append(_tl_fmt(_("I tried to play dumb but %s wasn't buying it. We broke up."), _pp))
                    _pending_msgs.append(_("Honestly? I'm relieved. No more sneaking around."))
                elif _bf_loyalty < 300 or _total_acts >= SEX_HISTORY_THRESHOLDS["breakup_heavy_history_acts"]:
                    _pending_msgs.append(_tl_fmt(_("%s said %s noticed I've been different lately. Distant, distracted."), _npc_name, _pp))
                    _pending_msgs.append(_tl_fmt(_("%s didn't accuse me of anything specific, but %s said %s couldn't keep pretending everything was fine."), _Pp, _pp, _pp))
                    _pending_msgs.append(_("Things were already falling apart. This just made it official."))
                elif _is_loyal:
                    _pending_msgs.append(_tl_fmt(_("%s confronted me last night. %s said things haven't been right between us for a while."), _npc_name, _Pp))
                    _pending_msgs.append(_tl_fmt(_("I tried to deny everything but %s kept pushing. %s said %s could feel it."), _pp, _Pp, _pp))
                    _pending_msgs.append(_("I couldn't lie anymore. It's over. And it's my fault."))
                else:
                    _pending_msgs.append(_tl_fmt(_("Hey... %s broke up with me. %s said %s could tell something was off."), _npc_name, _Pp, _pp))
                    _pending_msgs.append(_tl_fmt(_("%s mentioned your name. More than once. %s connected the dots."), _Pp, _Pp))
                    _pending_msgs.append(_("I guess we weren't as careful as we thought."))

            if girl.has_trait("has_boyfriend"):
                girl.remove_trait("has_boyfriend")
            elif girl.has_trait("has_girlfriend"):
                girl.remove_trait("has_girlfriend")
            girl.clear_npc_partner()
            girl._npc_breakup_result = "broke_up"
            debug_log("[NPC_BREAKUP] %s broke up (reason=%s)" % (girl.gid, reason))

        else:
            if reason == "caught":
                if _is_lesbian:
                    _pending_msgs.append(_tl_fmt(_("I talked to %s. %s forgave me... somehow. %s thinks I was confused."), _npc_name, _Pp, _Pp))
                    if _catch_count >= 3:
                        _pending_msgs.append(_tl_fmt(_("But %s is running out of patience. We need to be more careful. Or stop. We should probably stop."), _pp))
                    else:
                        _pending_msgs.append(_tl_fmt(_("I told %s it was a one-time thing and it would never happen again. Please don't make me a liar."), _po))
                elif _is_cheater:
                    _pending_msgs.append(_tl_fmt(_("Talked to %s. We're still together. %s bought my excuse."), _npc_name, _Pp))
                    _pending_msgs.append(_("We just need to be more careful next time ;)"))
                elif npc.has_trait("ntr"):
                    _pending_msgs.append(_tl_fmt(_("So I talked to %s... and %s didn't really mind? %s seemed almost... into it?"), _npc_name, _pp, _Pp))
                    _pending_msgs.append(_("I don't know what to think about that. We're still together though."))
                elif _bf_loyalty < 300 or _total_acts >= SEX_HISTORY_THRESHOLDS["breakup_heavy_history_acts"]:
                    _pending_msgs.append(_tl_fmt(_("I talked to %s. We're still together, but honestly, things were already bad."), _npc_name))
                    _pending_msgs.append(_("I don't know how long we'll last. But please don't push it."))
                elif _is_loyal:
                    _pending_msgs.append(_tl_fmt(_("I talked to %s. %s forgave me. I don't deserve %s."), _npc_name, _Pp, _po))
                    _pending_msgs.append(_("What we did can NEVER happen again. I mean it. Please respect that."))
                else:
                    _pending_msgs.append(_tl_fmt(_("Hey... I talked to my %s. %s forgave me, but it was close."), _plabel, _Pp))
                    _pending_msgs.append(_tl_fmt(_("We can't do that again. At least not where %s can find out."), _pp))
            elif reason == "video":
                npc.suspicion = 30
                if npc.has_trait("ntr"):
                    _pending_msgs.append(_tl_fmt(_("%s showed me a video you sent %s. A video of US."), _npc_name, _po))
                    _pending_msgs.append(_tl_fmt(_("The weird part? %s didn't seem that upset. More... curious about it."), _Pp))
                    _pending_msgs.append(_("We're still together, but... are you out of your mind?!"))
                elif _is_cheater:
                    _pending_msgs.append(_tl_fmt(_("%s showed me the video. I can't believe you sent that."), _npc_name))
                    _pending_msgs.append(_tl_fmt(_("I told %s it wasn't me. %s bought it, barely."), _po, _Pp))
                    _pending_msgs.append(_("We're still together. But seriously, what is wrong with you?"))
                elif _is_loyal:
                    _pending_msgs.append(_tl_fmt(_("%s showed me something on the phone. It was a video. Of me. With you."), _npc_name))
                    _pending_msgs.append(_tl_fmt(_("I told %s it was someone who looked like me. I don't think %s believed me."), _po, _pp))
                    _pending_msgs.append(_("We're still together but I've never been so scared. NEVER do that again."))
                else:
                    _pending_msgs.append(_tl_fmt(_("%s showed me a video you sent. A video of US. Are you out of your mind?!"), _npc_name))
                    _pending_msgs.append(_tl_fmt(_("I told %s it wasn't me. I don't think %s believes me but we're still together."), _po, _pp))
                    _pending_msgs.append(_("If you EVER do something like that again, I'm done with you."))
                Change_Status(girl, "Love", -15)
            elif reason == "pregnancy":
                if _preg_verdict == "raise":
                    _npc_raises_child(girl, npc, "verdict")
                else:
                    unlock_achievement("against_all_odds")
                _pending_msgs.extend(_npc_pregnancy_verdict_msgs(girl, _preg_verdict))
            else:
                npc.suspicion = 30
                if _is_lesbian:
                    _pending_msgs.append(_tl_fmt(_("%s confronted me today. %s asked if something was going on with you."), _npc_name, _Pp))
                    _pending_msgs.append(_("I denied everything. Said you were just a classmate who helped me study."))
                    _pending_msgs.append(_tl_fmt(_("%s believed me... I think. But %s is watching closely now."), _Pp, _pp))
                elif _is_cheater:
                    _pending_msgs.append(_tl_fmt(_("%s was acting all suspicious today, asking weird questions about you."), _npc_name))
                    _pending_msgs.append(_tl_fmt(_("I played dumb. Told %s you were nobody. %s bought it."), _po, _Pp))
                    _pending_msgs.append(_tl_fmt(_("We're fine. But maybe cool it for a bit? %s has eyes on me now."), _Pp))
                elif npc.has_trait("ntr"):
                    _pending_msgs.append(_tl_fmt(_("So %s brought up your name today. Asked if we were close."), _npc_name))
                    _pending_msgs.append(_tl_fmt(_("The weird thing? %s didn't seem angry. More like... curious?"), _Pp))
                    _pending_msgs.append(_("I don't know what to make of that. We're still together though."))
                elif _is_loyal:
                    _pending_msgs.append(_tl_fmt(_("%s sat me down and asked me directly if something was happening between us."), _npc_name))
                    _pending_msgs.append(_("My heart almost stopped. I swore nothing was going on."))
                    _pending_msgs.append(_tl_fmt(_("%s believed me, but %s said if %s ever finds out I lied, that's it. No second chances."), _Pp, _pp, _pp))
                else:
                    _pending_msgs.append(_tl_fmt(_("%s asked me some really uncomfortable questions today. About you."), _npc_name))
                    _pending_msgs.append(_tl_fmt(_("I told %s nothing is going on. %s seemed to buy it, but barely."), _po, _Pp))
                    _pending_msgs.append(_tl_fmt(_("We need to be careful. %s is suspicious and %s won't let this go easily."), _Pp, _pp))

            girl._npc_breakup_result = "stayed"
            debug_log("[NPC_BREAKUP] %s stayed (reason=%s)" % (girl.gid, reason))

        girl._npc_catch_msg_pending = True
        girl._npc_catch_msg_list = list(_pending_msgs)
        girl._npc_catch_msg_broke_up = broke_up
        girl._npc_catch_msg_reason = reason
        girl.clear_expired_statuses()
        if reason == "caught":
            girl.loc = girl.get_scheduled_location(store.Day, store.TimeIndex)

    def npc_next_day_process(girl):
        """Every flag-driven "the morning after" resolution between a girl and her NPC partner, in order.
        ONE list: _per_day_cleanup runs it for the girls who are reachable, _pregnancy_return for the girl
        who just came back (her flags waited for her; resolving them a day later kept her room locked)."""
        _npc_process_catch_next_day(girl)
        _npc_process_suspicion_next_day(girl)
        _npc_process_video_next_day(girl)
        _npc_process_pregnancy_verdict_next_day(girl)
        _ntr_process_discovery_next_day(girl)
        _ntr_process_activation_next_day(girl)
        _ntr_process_levelup_next_day(girl)
        _ntr_process_violation_next_day(girl)
        _npc_process_secret_vid_angry(girl)

    def _npc_process_catch_next_day(girl):
        if not getattr(girl, "_npc_catch_pending", False):
            return
        girl._npc_catch_pending = False
        _npc_process_breakup(girl, "caught")

    def _npc_process_suspicion_next_day(girl):
        if not getattr(girl, "_npc_suspicion_pending", False):
            return
        girl._npc_suspicion_pending = False
        _npc_process_breakup(girl, "suspicion")

    def _npc_process_pregnancy_verdict_next_day(girl):
        """She asked him to stay after he found out the baby is not his: his answer (_npc_pregnancy_verdict).
        A save from before this answer existed, whose baby is already born, just drops the old flag."""
        if not getattr(girl, "_npc_pregnancy_save_attempt", False):
            return
        girl._npc_pregnancy_save_attempt = False
        if not getattr(girl, "_pregnant", False) or not girl.has_npc_partner():
            print("[NPC_BREAKUP] %s: pregnancy save attempt dropped (pregnant=%s partner=%s)" % (
                girl.gid, getattr(girl, "_pregnant", False), girl.has_npc_partner()))
            return
        _npc_process_breakup(girl, "pregnancy")

    def _ntr_activate(girl, npc):
        if girl.has_trait("lesbian"):
            debug_log("[NTR_ACTIVATE] %s is lesbian, NTR boundary system not applicable" % girl.gid)
            return
        npc._ntr_active = True
        _bl = getattr(girl, "_ntr_boundary_level", None)
        if _bl is not None:
            npc._ntr_boundary_level = _bl
        else:
            _g = getattr(npc, "gender", "male")
            npc._ntr_boundary_level = _ntr_roll_boundary_level(_g)
            girl._ntr_boundary_level = npc._ntr_boundary_level
        npc._ntr_boundary_bar = 0
        girl._ntr_boundary_bar = 0
        _ntr_save_state(npc, girl)
        girl._ntr_activation_pending = True
        debug_log("[NTR_ACTIVATE] %s activated! boundary_level=%d traits=%s" % (
            npc.name, npc._ntr_boundary_level, npc.traits))

    def _ntr_process_activation_next_day(girl):
        if not getattr(girl, "_ntr_activation_pending", False):
            return
        girl._ntr_activation_pending = False
        npc = get_npc_partner_for(girl)
        if npc is None:
            return
        _girl_name = girl.Name
        _bl = getattr(npc, "_ntr_boundary_level", 1)
        _was_caught = getattr(girl, "_npc_catch_count", 0) > 0
        _msgs = []
        if _ntr_is_hostile_mode(npc):
            if _was_caught:
                _msgs.append(_("About yesterday... I saw everything. Don't think for a second I'm okay with this."))
            else:
                _msgs.append(_tl_fmt(_("I know what you've been doing with %s. Don't think for a second I'm okay with this."), _girl_name))
            if _bl == 1:
                _msgs.append(_("If you HAVE to do anything... keep it simple. No penetration. I swear, if you cross that line..."))
            elif _bl == 2:
                _msgs.append(_("Fine. Do whatever you want. But use a damn condom. I don't want to think about what happens if you don't."))
            elif _bl == 3:
                _msgs.append(_("I can't believe I'm saying this. Do what you want, but don't finish inside and don't touch her ass. That's where I draw the line."))
            else:
                _msgs.append(_("Whatever. Do whatever you want with her. I don't even know why I care anymore."))
            if _bl < 4:
                _msgs.append(_("I hate that I'm even having this conversation. Just... follow the rules."))
            if npc.has_trait("camera_lover"):
                _msgs.append(_("And send me the videos. Don't ask me why. Just do it."))
        else:
            if _was_caught:
                _msgs.append(_("About what happened yesterday... I've been thinking all night. And honestly? I don't mind."))
            else:
                _msgs.append(_tl_fmt(_("Hey, I know you've been getting close to %s. And honestly? I don't mind."), _girl_name))
            if _bl == 1:
                _msgs.append(_("It's fine to do simple things, but NO penetration!"))
            elif _bl == 2:
                _msgs.append(_("It's fine if you two go all the way, but you NEED to use protection."))
            elif _bl == 3:
                _msgs.append(_("I... I think it's fine if you do whatever you want, but please be careful, no finishing inside or anal, it could be too risky."))
            else:
                _msgs.append(_("You know, I really just want her to be happy. You can do whatever you want with her..."))
            if _bl < 4:
                _msgs.append(_("Just respect that, and we're cool."))
            if npc.has_trait("camera_lover"):
                if _bl >= 4:
                    _msgs.append(_("My only condition? I want to see videos of whatever happens."))
                else:
                    _msgs.append(_("Oh, and one more thing. I want to see videos of whatever happens."))
        girl._ntr_activation_msg_pending = True
        girl._ntr_activation_msg_list = list(_msgs)
        girl._ntr_activation_msg_npc_id = npc.partner_id
        debug_log("[NTR_ACTIVATE] %s activation messages queued (%d msgs)" % (npc.name, len(_msgs)))

    def _ntr_process_discovery_next_day(girl):
        if not getattr(girl, "_ntr_discovery_pending", False):
            return
        girl._ntr_discovery_pending = False
        _npc_id = getattr(girl, "_ntr_discovery_npc_id", None)
        npc = NPC_PARTNERS.get(_npc_id) if _npc_id else get_npc_partner_for(girl)
        if npc is None:
            return
        _was_violation = getattr(girl, "_ntr_discovery_was_violation", False)
        _girl_name = girl.Name
        _bl = getattr(npc, "_ntr_boundary_level", 1)
        _msgs = []
        _is_hostile = _ntr_is_hostile_mode(npc)
        if _was_violation:
            _viol_act = getattr(girl, "_ntr_discovery_violation_act", "sex")
            if _is_hostile:
                _msgs.append(_tl_fmt(_("I SAW what you did with %s. You think I'm BLIND?!"), _girl_name))
                if _bl == 1:
                    _msgs.append(_("You went way too far. Touching is one thing. What you did? That's something else entirely."))
                elif _bl == 2:
                    _msgs.append(_("No protection?! Are you insane?! ...I'm setting rules. And you WILL follow them."))
                elif _bl == 3:
                    _msgs.append(_("Finishing inside?! Anal?! I should end everything right now. ...But I won't. God help me, I won't."))
                _msgs.append(_tl_fmt(_("You want to keep going with %s? Fine. I can't stop it. But there ARE limits."), _girl_name))
                if npc.has_trait("camera_lover"):
                    _msgs.append(_("And I want to see everything on video. Don't ask why."))
            else:
                _msgs.append(_tl_fmt(_("I saw what you did with %s. That was NOT okay."), _girl_name))
                if _bl == 1:
                    _msgs.append(_("Look... I've thought about it. I could accept simple stuff, touching, hands. But what you did crossed the line."))
                elif _bl == 2:
                    _msgs.append(_("I could have accepted it if you at least used protection. But you didn't even do that."))
                elif _bl == 3:
                    _msgs.append(_("There were things I could tolerate, but finishing inside or anal? That's where I draw the line."))
                _msgs.append(_tl_fmt(_("If you want to keep doing things with %s, fine. But there are RULES."), _girl_name))
                if npc.has_trait("camera_lover"):
                    _msgs.append(_("And I want every moment on video."))
        else:
            if _is_hostile:
                _msgs.append(_("I haven't slept. I can't stop thinking about what I saw."))
                _msgs.append(_tl_fmt(_("I saw you with %s. I should be furious. I AM furious. But..."), _girl_name))
                if _bl == 1:
                    _msgs.append(_("Simple stuff. Touching. Hands. That's ALL. No penetration. I mean it."))
                elif _bl == 2:
                    _msgs.append(_("If you're going to do... more... use a condom. At LEAST give me that."))
                elif _bl == 3:
                    _msgs.append(_("Do whatever. Just don't finish inside and stay away from... that other thing. I can't watch that."))
                else:
                    _msgs.append(_("...Do whatever you want. I've lost the will to fight this. What's wrong with me?"))
                if _bl < 4:
                    _msgs.append(_("Follow the rules. Or don't. I don't know why I think you'll listen."))
                if npc.has_trait("camera_lover"):
                    _msgs.append(_("Send me the videos. I don't want to explain why. Just send them."))
            else:
                _msgs.append(_("About yesterday... I've been thinking all night."))
                _msgs.append(_tl_fmt(_("I saw you with %s. And honestly? I'm not as upset as I thought I'd be."), _girl_name))
                if _bl == 1:
                    _msgs.append(_("Simple stuff is fine. Touching, hands, whatever. But NO penetration. That's my line."))
                elif _bl == 2:
                    _msgs.append(_("You two can go further if you want, but you NEED to use protection. Non-negotiable."))
                elif _bl == 3:
                    _msgs.append(_("Do what you want, but be careful. No finishing inside or anal."))
                else:
                    _msgs.append(_("Honestly? Do whatever you want with her. I just want her to be happy."))
                if _bl < 4:
                    _msgs.append(_("Respect that, and we're fine."))
                if npc.has_trait("camera_lover"):
                    if _bl >= 4:
                        _msgs.append(_("My only condition? I want to see videos of whatever happens."))
                    else:
                        _msgs.append(_("Oh, and one more thing. I want to see videos of whatever happens."))
        girl._ntr_activation_msg_pending = True
        girl._ntr_activation_msg_list = list(_msgs)
        girl._ntr_activation_msg_npc_id = npc.partner_id
        girl._ntr_discovery_was_violation = False
        girl._ntr_discovery_violation_act = None
        girl._ntr_discovery_npc_id = None
        debug_log("[NTR_DISCOVERY_NEXT_DAY] %s discovery msgs queued, violation=%s level=%d hostile=%s" % (npc.name, _was_violation, _bl, _is_hostile))

    def _ntr_process_levelup_next_day(girl):
        if not getattr(girl, "_ntr_levelup_pending", False):
            return
        girl._ntr_levelup_pending = False
        npc = get_npc_partner_for(girl)
        if npc is None:
            return
        _girl_name = girl.Name
        _bl = getattr(npc, "_ntr_boundary_level", 1)
        _msgs = []
        if _ntr_is_hostile_mode(npc):
            if _bl == 2:
                _msgs.append(_tl_fmt(_("I don't know what's wrong with me. Go ahead. Fuck %s. But use protection. ...God, I hate myself."), _girl_name))
            elif _bl == 3:
                _msgs.append(_("Take the condom off. I don't care anymore. Just... don't finish inside. I still have SOME limits left."))
            elif _bl == 4:
                _msgs.append(_("Do whatever you want. I've stopped caring. ...That's a lie. I haven't. But do it anyway."))
            if _msgs and npc.has_trait("camera_lover"):
                _msgs.append(_("Keep sending videos. I still don't know why I watch them. But I do."))
        else:
            if _bl == 2:
                _msgs.append(_tl_fmt(_("I've been thinking... I trust you enough now. You can go further with %s, just use protection."), _girl_name))
            elif _bl == 3:
                _msgs.append(_("Look, I know you two have something. You don't need the condom anymore. Just... be careful, don't finish inside."))
            elif _bl == 4:
                _msgs.append(_tl_fmt(_("I... I just want %s to be happy. Do whatever you want with her."), _girl_name))
            if _msgs and npc.has_trait("camera_lover"):
                if _bl >= 4:
                    _msgs.append(_("My only condition? I want to see videos of whatever happens."))
                else:
                    _msgs.append(_("Oh, and I still want to see videos of whatever happens."))
        if _msgs:
            girl._ntr_activation_msg_pending = True
            girl._ntr_activation_msg_list = list(_msgs)
            girl._ntr_activation_msg_npc_id = npc.partner_id
            debug_log("[NTR_LEVELUP] %s level-up messages queued, new level=%d" % (npc.name, _bl))

    def _ntr_process_violation_next_day(girl):
        if not getattr(girl, "_ntr_violation_pending", False):
            return
        girl._ntr_violation_pending = False
        npc = get_npc_partner_for(girl)
        if npc is None:
            return
        _contacts = getattr(store.Player, "phone_contacts", set())
        if girl.gid in _contacts:
            _npc_name = npc.Name if hasattr(npc, "Name") else "my partner"
            _msgs = []
            _msgs.append(_tl_fmt(_("%s and I had a huge fight last night because of what you did."), _npc_name))
            _msgs.append(_("Things are really tense. Please be more careful."))
            phone_add_msg(girl.gid, girl.gid, _tl(_msgs[0]), "text")
            phone_add_msg(girl.gid, girl.gid, _tl(_msgs[1]), "text")
        Change_Status(girl, "Love", -15)
        Change_Status(girl, "Obed", 5)
        Change_Status(girl, "Inbt", 5)
        debug_log("[NTR_VIOLATION] %s fight aftermath: Love -15, Obed +5, Inbt +5" % girl.gid)

    def _npc_process_video_next_day(girl):
        _seen_done = False
        if getattr(girl, "_ntr_video_seen_pending", False):
            girl._ntr_video_seen_pending = False
            _seen_done = _ntr_video_seen_next_day(girl)
        if not getattr(girl, "_npc_video_pending", False):
            return
        girl._npc_video_pending = False
        if _seen_done:
            return   # legacy flag (older build) for the same NTR-known partner: the texts already went out
        _npc_process_breakup(girl, "video")

    def _npc_process_secret_vid_angry(girl):
        if not getattr(girl, "_npc_secret_vid_angry", False):
            return
        girl._npc_secret_vid_angry = False
        _girl_name = girl.Name
        _npc = get_npc_partner_for(girl)
        _npc_name = _npc.Name if _npc else _tl(_("Someone"))
        _msgs = [
            _("%s told me you secretly filmed me. What is wrong with you?!"),
            _("I can't believe you did that. %s showed me the proof."),
            _("You recorded me without my consent?! %s told me everything."),
        ]
        _msg = _tl(renpy.random.choice(_msgs)) % _npc_name
        phone_add_msg(girl.gid, girl.gid, _msg, "text")
        girl.set_temp_status("angry", 3, "secret_recording")
        debug_log("[NPC_SECRET_VID] %s angry 3 days: NPC told her about secret recording" % girl.gid)

    def _chitchat_breakup_suggestion(girl, loc, t_index):
        renpy.call("_npc_breakup_suggestion_chat", girl)

    def _ntr_creampie_check(girl):
        """Check if NPC partner should detect creampie. Returns True if detection should fire.
        He must have been PHYSICALLY on scene (process_cum records it in store._ntr_creampie_witnessed_gid:
        the watcher state is already wiped by scene_full_cleanup when this runs). Partner absent = it
        stays a secret now; at level 3 _ntr_violation_pending brings the next-day fight."""
        if not getattr(girl, "_ntr_boundary_discovered", False):
            return False
        npc = get_npc_partner_for(girl)
        if npc is None:
            return False
        if not getattr(npc, "_ntr_active", False):
            return False
        bl = getattr(npc, "_ntr_boundary_level", 1)
        # Levels 1-3 don't allow creampie. Level 4 = no limits
        if bl >= 4:
            return False
        # The witnessed flag IS the evidence: only an inside / condom_removed_inside process_cum of this
        # session sets it, and session_cum_reset() clears it together with _session_cum. (_session_cum is
        # not tested any more: the laying down "Clean up" option wipes it in the middle of the scene.)
        _sc = store._session_cum
        if getattr(store, "_ntr_creampie_witnessed_gid", None) != girl.gid:
            debug_log("[NTR_CREAMPIE] %s: creampie NOT witnessed (partner absent, bl=%d) -> no confrontation, violation_pending=%s" % (girl.gid, bl, getattr(girl, "_ntr_violation_pending", False)))
            return False
        debug_log("[NTR_CREAMPIE] Check PASSED for %s (bl=%d, session_cum=%s)" % (girl.gid, bl, _sc))
        return True

init 1 python:
    register_chitchat(
        "global",
        _chitchat_breakup_suggestion,
        condition=lambda g, loc, t: getattr(g, "_will_break_up_with_partner", False) and g.has_npc_partner(),
        weight=20,
    )

# ============================================================
# NPC Witness Reaction Labels
# ============================================================

label _npc_partner_detection_tick(girl, act_type):

    python:
        if act_type not in _NTR_NON_PENETRATION:
            if (getattr(store, "doggy_rub_mode", False) or getattr(store, "cowgirl_rub_mode", False)
                    or getattr(store, "rcg_rub_mode", False) or getattr(store, "fn_rub_mode", False)
                    or getattr(store, "laying_rub_mode", False)):
                act_type = "rub"
            elif _ntr_is_tip_mode():
                act_type = "tip"

    # NTR-active partner: silent watch or violation interrupt
    if store._ntr_partner_watching:
        python:
            _ntr_w_npc = store._ntr_watching_npc
            _ntr_w_girl, _ntr_w_pos, _ntr_w_anal, _ntr_w_condom = _ntr_get_scene_state()
            # Bet event: condom removal was the agreed consequence. ONLY while the event runs, for the bet
            # girl. It used to test _bet_npc_looked alone: that flag is saved and was never cleared, so after
            # a won bet every later tick was "within bounds" forever (no condom-break level-up, no violation).
            _ntr_w_bet_ok = (getattr(store, "_bet_event_active", False)
                             and getattr(store, "_bet_npc_looked", False)
                             and getattr(store, "_bet_girl_gid", None) == girl.gid)
            _ntr_w_within = True if _ntr_w_bet_ok else _ntr_act_within_boundary(
                act_type, getattr(_ntr_w_npc, "_ntr_boundary_level", 1),
                condom_active=_ntr_w_condom, is_anal=_ntr_w_anal)
            print("[NTR_WATCH_TICK] npc=%s girl=%s act=%s level=%s condom=%s broken=%s hidden=%s anal=%s bet_ok=%s within=%s" % (
                getattr(_ntr_w_npc, "name", None), girl.gid, act_type, getattr(_ntr_w_npc, "_ntr_boundary_level", 1),
                _ntr_w_condom, store._condom_broken, store._condom_broken_hidden, _ntr_w_anal, _ntr_w_bet_ok, _ntr_w_within))

        # Condom break beats (within bounds only). HIDDEN break: he may notice before she does (roll,
        # NTR_CBREAK_NOTICE). Once she finds out, a partner who had silently noticed admits it, once.
        $ _ntr_w_cb_fires = _ntr_cbreak_tick_fires(girl, _ntr_w_npc, _ntr_w_within)
        if _ntr_w_cb_fires:
            call _ntr_condom_break_watching(girl, _ntr_w_npc) from _call_ntr_cbreak_watch_beat
            return

        if not _ntr_w_within:
            # Condom break is NOT a violation — it's an accident that triggers level up
            if store._condom_broken and getattr(_ntr_w_npc, "_ntr_boundary_level", 1) == 2 and not _ntr_w_anal:
                call _ntr_condom_break_watching(girl, _ntr_w_npc) from _call_ntr_cbreak_watch
            else:
                call _ntr_boundary_violation(girl, _ntr_w_npc, act_type) from _call_ntr_violation_watch
        else:
            # Periodic narration while NPC watches (~25% chance per tick)
            python:
                _ntr_w_roll = renpy.random.random()
            if _ntr_w_roll < 0.25:
                python:
                    _ntr_w_is_voyeur = _ntr_w_npc.has_trait("voyeur") if hasattr(_ntr_w_npc, "has_trait") else False
                    _ntr_w_name = _ntr_w_npc.Name
                    if _ntr_is_hostile_mode(_ntr_w_npc):
                        _ntr_w_react_pool = [
                            _("%s is trembling with rage, but can't tear their eyes away."),
                            _("%s's fists are clenched white, yet they haven't moved an inch."),
                            _("%s looks disgusted with themselves for watching, yet stays rooted to the spot."),
                            _("%s is breathing hard, caught between fury and something they refuse to name."),
                            _("%s's jaw is locked, eyes burning with hate... and something else."),
                            _("%s grips the doorframe so hard their knuckles crack, but their gaze stays fixed."),
                        ]
                    elif _ntr_w_is_voyeur:
                        _ntr_w_react_pool = [
                            _("%s is watching intently, completely absorbed in the scene."),
                            _("%s has one hand inside their pants, squirming shyly."),
                            _("%s is breathing heavily, unable to look away."),
                            _("%s is biting their lip, eyes locked on every movement."),
                        ]
                    else:
                        _ntr_w_react_pool = [
                            _("%s is wide-eyed, watching everything unfold."),
                            _("%s seems to have teary eyes, but can't stop looking."),
                            _("%s is frozen in place, staring with a mix of shock and fascination."),
                            _("%s swallows hard, clearly uncomfortable but unable to leave."),
                            _("%s clenches their fists, jaw tight, but stays put."),
                        ]
                    _ntr_w_react_line = _tl(renpy.random.choice(_ntr_w_react_pool)) % _ntr_w_name
                "[_ntr_w_react_line]"
            # ── Hostile NTR: surrender check or mini-dialogues ──
            python:
                _ntr_hmd_ok = _ntr_is_hostile_mode(_ntr_w_npc)
                _ntr_surr_ok = False
                if _ntr_hmd_ok:
                    _ntr_hmd_cd = getattr(store, "_ntr_hostile_mini_cd", 0) - 1
                    store._ntr_hostile_mini_cd = max(0, _ntr_hmd_cd)
                    _ntr_surr_ok = (
                        not getattr(_ntr_w_npc, "_ntr_hostile_surrendered", False)
                        and getattr(_ntr_w_npc, "_ntr_boundary_level", 1) >= 4
                        and getattr(_ntr_w_npc, "_ntr_hostile_mini_count", 0) >= 8
                        and _ntr_get_current_speed() >= 3
                    )
                    if _ntr_surr_ok:
                        _nhs_st, _nhs_pos, _nhs_a, _nhs_c = _ntr_get_scene_state()
                        _ntr_surr_ok = _nhs_pos in ("doggy", "cowgirl", "reverse_cowgirl", "full_nelson")
            if _ntr_hmd_ok and _ntr_surr_ok:
                call _ntr_hostile_surrender(girl, _ntr_w_npc) from _call_ntr_hostile_surrender
            elif _ntr_hmd_ok and store._ntr_hostile_mini_cd <= 0:
                python:
                    _ntr_hmd_roll = renpy.random.random()
                if _ntr_hmd_roll < 0.15:
                    $ store._ntr_hostile_mini_cd = 4
                    call _ntr_hostile_mini_dialogue(girl, _ntr_w_npc) from _call_ntr_hostile_mini
        return

    python:
        _npc_det = npc_partner_witness_check(girl, act_type)

    if _npc_det is not None:
        # Check if this is an NTR-active partner
        python:
            _det_is_ntr_active = (
                getattr(_npc_det, "_ntr_active", False)
                and _npc_witness_is_girls_partner(_npc_det, girl)
                and not girl.has_trait("lesbian")
            )
        if _det_is_ntr_active:
            python:
                _ntr_d_girl, _ntr_d_pos, _ntr_d_anal, _ntr_d_condom = _ntr_get_scene_state()
                _ntr_d_within = _ntr_act_within_boundary(
                    act_type, getattr(_npc_det, "_ntr_boundary_level", 1),
                    condom_active=_ntr_d_condom, is_anal=_ntr_d_anal)
                _ntr_d_discovered = getattr(girl, "_ntr_boundary_discovered", False)
            if not _ntr_d_discovered:
                # First time caught — discovery event
                call _ntr_discovery_event(girl, _npc_det, act_type) from _call_ntr_discovery
            elif _ntr_d_within:
                # Silent observation — NTR partner watches without interrupting
                python:
                    store._ntr_partner_watching = True
                    store._ntr_watching_npc = _npc_det
                    _npc_det._ntr_bar_session_gain = 0
                    _bar_gain = 8 if _npc_det.has_trait("voyeur") else 3
                    _ntr_increase_boundary_bar(_npc_det, girl, _bar_gain)
                    if _ntr_is_hostile_mode(_npc_det):
                        _ntr_watch_lines = [
                            _("%s sees what's happening. Fury flashes across their face... but they don't leave."),
                            _("%s walks in, freezes at the sight. Their hands shake, but their feet won't move."),
                            _("%s catches on. Rage fills their eyes... but they stay, unable to look away."),
                        ]
                    else:
                        _ntr_watch_lines = [
                            _("%s notices what's happening, but decides to just watch."),
                            _("%s glances over and sees everything, but stays quiet."),
                            _("%s catches on to what you're doing, but doesn't say a word."),
                        ]
                    _ntr_watch_narr = _tl(renpy.random.choice(_ntr_watch_lines)) % _npc_det.Name
                    debug_log("[NTR_WALKIN] %s silently watches %s act=%s (within bounds)" % (_npc_det.name, girl.gid, act_type))
                "[_ntr_watch_narr]"
            else:
                call _ntr_boundary_violation(girl, _npc_det, act_type) from _call_ntr_violation_walkin
        else:
            call _npc_partner_witness_reaction(girl, _npc_det, act_type) from _call_npc_witness_react
    return

label _npc_partner_witness_reaction(girl, npc, act_type):
    $ store._npc_witness_scene_aborted = False
    $ debug_log("[NPC_WITNESS] Reaction: girl=%s npc=%s act=%s Day=%d TI=%d" % (girl.gid, npc.name, act_type, store.Day, store.TimeIndex))

    python:
        _nw_is_partner = _npc_witness_is_girls_partner(npc, girl)
        _nw_reaction = _npc_witness_reaction_type(npc, girl, act_type)
        _nw_severity = _npc_act_severity(act_type)
        _nw_mult = _NPC_SEVERITY_STAT_MULT.get(_nw_severity, 1.0)

    if not _nw_is_partner:
        python:
            _pub_lines = [
                _("Someone nearby glances in your direction, but it's nobody important."),
                _("%(pub_desc)s pauses, stares for a second, then walks away shaking %(poss)s head."),
                _("You notice someone watching from a distance, but they leave quickly."),
            ]
        "[_format_npc_line(npc, renpy.random.choice(_pub_lines))]"
        $ Change_Status(girl, "Inbt", -5)
        return

    # ── NPC IS the girl's partner ──

    # Step 1: NPC entrance / realization
    python:
        _npc_was_here = (getattr(npc, "loc", None) == getattr(store, "CurrentLocation", "room"))
        _is_room = _is_room_location()
        if _npc_was_here and _is_room:
            _entrance = [
                _("%(name)s looks up from %(poss)s phone and freezes. %(Poss)s eyes go wide."),
                _("%(name)s stops scrolling through %(poss)s phone. %(Pp)s stares at the scene in front of %(po)s, unable to process what %(pp)s's seeing."),
                _("%(name)s was right there the whole time. %(Pp)s slowly takes off %(poss)s headphones, mouth hanging open."),
            ]
        elif _is_room:
            _entrance = [
                _("The door swings open. %(name)s walks in and freezes."),
                _("You hear the door handle turn. %(name)s steps inside and stops dead."),
                _("%(name)s opens the door without knocking. The silence is deafening."),
            ]
        else:
            _entrance = [
                _("%(name)s approaches from behind and sees everything."),
                _("A familiar voice gasps behind you. %(name)s is standing right there."),
                _("%(name)s rounds the corner and catches you both in the act."),
            ]
    "[_format_npc_line(npc, renpy.random.choice(_entrance))]"
    if not _npc_was_here:
        $ _show_witness_enter(npc)

    # Step 2: NPC reacts (severity-aware pools + scaled penalties) and LEAVES
    python:
        _nw_pool = _NPC_WITNESS_LINES.get((_nw_reaction, _nw_severity), _NPC_WITNESS_LINES.get((_nw_reaction, "moderate"), []))
        _npc_line = renpy.random.choice(_nw_pool) if _nw_pool else "..."
        debug_log("[NPC_WITNESS] reaction=%s severity=%s mult=%.1f act=%s" % (_nw_reaction, _nw_severity, _nw_mult, act_type))
    $ Say_Line(npc, _format_npc_line(npc, _npc_line, girl))

    if _nw_reaction == "furious":
        python:
            npc.change_friendship(int(-200 * _nw_mult))
            npc.change_love(int(-50 * _nw_mult))
            girl.change_bf_loyalty(int(-100 * _nw_mult))

    elif _nw_reaction == "angry":
        python:
            npc.change_friendship(int(-100 * _nw_mult))
            npc.change_love(int(-25 * _nw_mult))
            girl.change_bf_loyalty(int(-75 * _nw_mult))

    elif _nw_reaction == "sad":
        python:
            npc.change_friendship(int(-50 * _nw_mult))
            npc.change_love(int(-100 * _nw_mult))
            girl.change_bf_loyalty(int(-50 * _nw_mult))

    elif _nw_reaction == "confused":
        python:
            npc.change_friendship(int(-50 * _nw_mult))
            girl.change_bf_loyalty(int(-25 * _nw_mult))

    # NPC storms out
    "[npc.Name] turns around and leaves without another word."
    $ _hide_witness_exit(npc)
    $ npc.loc = "away" if girl.home == store.CurrentLocation else girl.home

    # Step 3: Girl decides to continue or stop
    python:
        _nw_continues = _girl_continues_after_catch(girl)
        debug_log("[NPC_WITNESS] Step 3: %s continues=%s lesbian=%s" % (girl.gid, _nw_continues, girl.has_trait("lesbian")))

    if _nw_continues:
        python:
            _nw_matched_trait = None
            if girl.has_trait("cheater"):
                _cont_line = renpy.random.choice([
                    _("Fuck %(name)s, we'll talk later. Keep going."),
                    _("Whatever. %(Pp)s will get over it. Where were we?"),
                    _("Let %(name)s cry about it. I'm not done with you yet."),
                ])
                _nw_matched_trait = "cheater"
            elif girl.has_trait("exhibitionist"):
                _cont_line = renpy.random.choice([
                    _("That was... intense. But keep going. I don't want to stop."),
                    _("I'll deal with %(name)s later. Right now, I want you."),
                ])
                # arousal/continuing is not being-seen evidence: no discover
            elif (girl.Obed + girl.Inbt) / 2 >= 500:
                _cont_line = renpy.random.choice([
                    _("Keep going... I'll take care of this later."),
                    _("Don't stop. %(Pp)s can wait. This can't."),
                    _("I... I'll deal with it after. Just... keep going."),
                ])
            else:
                _cont_line = renpy.random.choice([
                    _("I... I don't know what to do. But... don't stop."),
                    _("We've already been caught. Stopping now won't change anything."),
                ])
        $ Say_Line(girl, _format_npc_line(npc, _cont_line))
        if _nw_matched_trait:
            $ girl.discover("discovered_trait_%s" % _nw_matched_trait)
        $ Change_Status(girl, "Inbt", -10)
        $ store._witness_expression_lock = False
        $ debug_log("[NPC_DETECT] %s continues after catch, re-rendering scene" % girl.gid)
        call _rerender_sex_scene(girl, act_type) from _call_rerender_npc_witness_continue
    else:
        python:
            _nw_stop_trait = None
            if girl.has_trait("lesbian"):
                _stop_line = renpy.random.choice([
                    _("%(name)s just saw me with a MAN. I need to go. NOW. I have to explain... somehow."),
                    _("Oh god... %(name)s... %(pp)s saw everything... I need to talk to %(po)s before %(pp)s..."),
                    _("This is a nightmare. %(name)s caught me with a guy. I'm a lesbian and %(pp)s just... I have to go!"),
                    _("%(name)s is going to think I've been lying about being a lesbian this whole time... I need to go after %(po)s!"),
                ])
                _nw_stop_trait = "lesbian"
            elif girl.has_trait("bisexual") and girl.has_npc_partner():
                _stop_line = renpy.random.choice([
                    _("%(name)s just saw me with another guy... I need to go explain!"),
                    _("Oh god... %(name)s... %(pp)s saw everything... I need to talk to %(po)s!"),
                    _("%(name)s caught me cheating... I need to go after %(po)s before it's too late!"),
                ])
                # "saw me with another guy" says nothing about liking girls: no discover
            elif girl.has_trait("loyal"):
                _stop_line = renpy.random.choice([
                    _("I need to go. I need to talk to %(name)s. I should NEVER have done this!"),
                    _("Oh god, what have I done... I have to go after %(name)s. NOW!"),
                    _("This was a mistake! A terrible mistake! I'm going to %(name)s!"),
                ])
                _nw_stop_trait = "loyal"
            elif girl.has_trait("cute_sex"):
                _stop_line = renpy.random.choice([
                    _("N-no... %(name)s saw us... I can't... I need to go talk to %(name)s..."),
                    _("Oh god... I want to disappear... I have to go..."),
                    _("Please... I need to go after %(name)s... I'm so sorry..."),
                ])
                # "I want to disappear" is embarrassment tone, not a taste: no discover
            else:
                _stop_line = renpy.random.choice([
                    _("I need to go... %(name)s is... I have to talk to %(name)s."),
                    _("We have to stop. I can't just let %(name)s leave like that."),
                    _("This is bad... really bad. I need to go. Now."),
                ])
        $ Say_Line(girl, _format_npc_line(npc, _stop_line))
        if _nw_stop_trait:
            $ girl.discover("discovered_trait_%s" % _nw_stop_trait)
        python:
            Change_Status(girl, "Love", -20)
            Change_Status(girl, "Obed", 10)
            store._npc_witness_scene_aborted = True
            print("[NPC_DETECT] >>> _npc_witness_scene_aborted SET TO TRUE for %s <<<" % girl.gid)
        $ debug_log("[NPC_DETECT] %s stops after catch, scene aborted" % girl.gid)

    # Step 4: Set flags for both paths (resolved next day by _npc_process_catch_next_day)
    python:
        girl._npc_catch_pending = True
        girl._npc_catch_pending_day = store.Day
        girl._npc_catch_pending_ti = store.TimeIndex
        girl._npc_catch_count = getattr(girl, "_npc_catch_count", 0) + 1
        girl.set_temp_status("unavailable", 2, reason="talking_to_partner")
        debug_log("[NPC_WITNESS] Step 4: %s catch_pending=True count=%d unavailable_until=Day%d Day=%d TI=%d" % (girl.gid, girl._npc_catch_count, store.Day + 1, store.Day, store.TimeIndex))

    return

# ============================================================
# NPC Breakup Message Event — phone notification next morning
# Every reason of _npc_process_breakup: "caught", "suspicion" / "video" (the shared else), "pregnancy".
# ============================================================
label _npc_catch_message_event(girl):

    python:
        _catch_reason = getattr(girl, "_npc_catch_msg_reason", "caught")
        _catch_broke_up = getattr(girl, "_npc_catch_msg_broke_up", False)
        _catch_msgs = getattr(girl, "_npc_catch_msg_list", [])

    play sound "audio/Notification.mp3" noloop

    if _catch_reason == "caught":
        if _catch_broke_up:
            "Your phone buzzes. A long message from [girl.Name]. This doesn't look good."
        else:
            "Your phone buzzes. New message from [girl.Name]. She seems shaken."
    elif _catch_reason == "pregnancy":
        $ Narration(_tl_fmt(_("Your phone buzzes. It's %s. She had the talk she said she would."), girl.Name))
    else:
        if _catch_broke_up:
            "Your phone buzzes. [girl.Name] sent you a message. Something feels off."
        else:
            "Your phone buzzes. [girl.Name] texted you. Sounds like she needs to vent."

    while _catch_msgs:
        $ phone_add_msg(girl.gid, girl.gid, None, "typing")
        call screen phone_chat_screen(girl, auto_close=renpy.random.uniform(1.0, 1.8), choices=[])
        python:
            _t = phone_get_msgs(girl.gid)
            if _t and _t[-1].get("type") == "typing": _t.pop()
            _this_msg = _catch_msgs.pop(0)
            phone_add_msg(girl.gid, girl.gid, _tl(_this_msg))
        call screen phone_chat_screen(girl, auto_close=renpy.random.uniform(0.8, 1.2) if _catch_msgs else 0, choices=[])

    call screen phone_chat_screen(girl, choices=[])

    # Post-message narration
    if _catch_reason == "caught":
        if _catch_broke_up:
            "You stare at the screen. Her relationship is over because of you."
        else:
            "You let out a breath you didn't know you were holding. That was close."
    elif _catch_reason == "pregnancy":
        if _catch_broke_up:
            $ Narration(_("She tried to hold it together. It wasn't enough."))
        elif child_npc_is_father(girl):
            $ Narration(_format_partner_line(girl, _("A baby that isn't %(poss)s, and %(pp)s will raise it anyway. You don't know what to make of that.")))
        else:
            $ Narration(_format_partner_line(girl, _("Somehow they're still together, with a baby that isn't %(poss)s on the way.")))
    else:
        if _catch_broke_up:
            "So the suspicion finally got to them. You wonder if it was worth it."
        else:
            "Crisis averted, for now. But the clock is ticking."

    $ girl._npc_catch_msg_pending = False
    $ girl._npc_catch_msg_list = []
    $ girl._npc_catch_msg_reason = None
    return

# ============================================================
# NTR Activation / Level-Up Message Event
# ============================================================

label _ntr_activation_message_event(girl):

    python:
        _ntr_msgs = getattr(girl, "_ntr_activation_msg_list", [])
        _ntr_npc_id = getattr(girl, "_ntr_activation_msg_npc_id", None)
        _ntr_npc = NPC_PARTNERS.get(_ntr_npc_id) if _ntr_npc_id else None

    if _ntr_npc is None:
        $ girl._ntr_activation_msg_pending = False
        return

    play sound "audio/Notification.mp3" noloop

    python:
        _ntr_npc_name = _ntr_npc.Name if hasattr(_ntr_npc, "Name") else "Someone"
        _npc_contacts = getattr(store.Player, "phone_npc_contacts", set())
        if _ntr_npc.partner_id not in _npc_contacts:
            _npc_contacts.add(_ntr_npc.partner_id)

    "Your phone buzzes. New message from [_ntr_npc_name]. That's... unexpected."

    while _ntr_msgs:
        $ phone_add_msg(_ntr_npc.gid, _ntr_npc.gid, None, "typing")
        call screen phone_chat_screen(_ntr_npc, auto_close=renpy.random.uniform(1.0, 1.8), choices=[])
        python:
            _t = phone_get_msgs(_ntr_npc.gid)
            if _t and _t[-1].get("type") == "typing": _t.pop()
            _this_msg = _ntr_msgs.pop(0)
            phone_add_msg(_ntr_npc.gid, _ntr_npc.gid, _tl(_this_msg))
        call screen phone_chat_screen(_ntr_npc, auto_close=renpy.random.uniform(0.8, 1.2) if _ntr_msgs else 0, choices=[])

    call screen phone_chat_screen(_ntr_npc, choices=[])

    python:
        _npc_bl = getattr(_ntr_npc, "_ntr_boundary_level", 1)
        _npc_cam = _ntr_npc.has_trait("camera_lover") if hasattr(_ntr_npc, "has_trait") else False

    python:
        _ntr_msg_hostile = _ntr_is_hostile_mode(_ntr_npc)
    if _ntr_msg_hostile:
        if _npc_bl >= 4:
            "So [_ntr_npc_name] knows. And hates every second of it... but gave up fighting."
        else:
            "So [_ntr_npc_name] knows. And clearly hates it... but set rules instead of stopping it. Interesting."
    elif _npc_bl >= 4 and _npc_cam:
        "So [_ntr_npc_name] knows. And apparently doesn't mind... just wants to see the footage."
    elif _npc_bl >= 4:
        "So [_ntr_npc_name] knows. And doesn't mind. At all."
    elif _npc_cam:
        "So [_ntr_npc_name] knows. And apparently doesn't mind... with conditions. And wants videos on top of that."
    else:
        "So [_ntr_npc_name] knows. And apparently doesn't mind... with conditions."

    $ girl._ntr_boundary_discovered = True
    $ girl._ntr_activation_msg_pending = False
    $ girl._ntr_activation_msg_list = []
    $ girl._ntr_activation_msg_npc_id = None
    return

# ============================================================
# NTR Discovery Event — first time NPC catches player mid-scene
# Two paths: within bounds (calm acceptance) vs violation (angry catch)
# ============================================================

label _ntr_discovery_event(girl, npc, act_type):
    python:
        _disc_girl, _disc_pos, _disc_anal, _disc_condom = _ntr_get_scene_state()
        _disc_within = _ntr_act_within_boundary(
            act_type, getattr(npc, "_ntr_boundary_level", 1),
            condom_active=_disc_condom, is_anal=_disc_anal)
        _disc_npc_here = (getattr(npc, "loc", None) == getattr(store, "CurrentLocation", "room"))
        _disc_is_room = _is_room_location()
        debug_log("[NTR_DISCOVERY] %s discovers %s act=%s within=%s boundary=%d" % (
            npc.name, girl.gid, act_type, _disc_within, getattr(npc, "_ntr_boundary_level", 1)))

    # Step 1: NPC entrance
    python:
        if _disc_npc_here and _disc_is_room:
            _disc_entrance = [
                _("%(name)s looks up and freezes. %(Poss)s face goes pale."),
                _("%(name)s was right there the whole time. %(Pp)s slowly looks up, eyes wide."),
            ]
        elif _disc_is_room:
            _disc_entrance = [
                _("The door opens. %(name)s walks in and stops dead in %(poss)s tracks."),
                _("You hear the door. %(name)s steps inside and the color drains from %(poss)s face."),
            ]
        else:
            _disc_entrance = [
                _("%(name)s appears nearby and sees everything."),
                _("A gasp from behind. %(name)s is standing right there, staring."),
            ]
    "[_format_npc_line(npc, renpy.random.choice(_disc_entrance))]"
    if not _disc_npc_here:
        $ _show_witness_enter(npc)

    if _disc_within:
        # ── WITHIN BOUNDS: Calm discovery ──

        # Girl's first reaction: shocked, looks at NPC
        $ set_scene_expression(girl, None, eyes="eyes_side", brows="brows_surprised", mouth="mouth_surprised")

        # NPC is shocked but will ultimately accept
        python:
            _disc_shock_line = _tl(_("%s... %s... How can... Oh my god...")) % (girl.Name, store.Player.Name)
        $ Say_Line(npc, _disc_shock_line)

        # Girl reacts (trait-aware) — looking away, embarrassed
        $ set_scene_expression(girl, None, eyes="eyes_side", brows="brows_sad", mouth="mouth_sad")
        python:
            if girl.has_trait("cheater"):
                _disc_girl_lines = [
                    _("Look, I'm sorry you found out like this, but I'm not going to pretend I'm sorry."),
                    _("I know this looks bad, but this is what I want."),
                ]
                set_scene_expression(girl, None, eyes="eyes_side", brows="brows_normal", mouth="mouth_serious")
            else:
                _disc_girl_lines = [
                    _("Oh no, sorry, sorry, sorry... I was... I don't know what I was thinking..."),
                    _("I'm so sorry... I never meant for you to see this..."),
                    _("Oh god... I... I don't know how this happened..."),
                ]
        $ Say_Line(girl, _tl(renpy.random.choice(_disc_girl_lines)))

        # NPC asks the key question — girl glances at NPC nervously
        $ set_scene_expression(girl, None, eyes="eyes_side_2", brows="brows_confused", mouth="mouth_serious")
        python:
            _disc_ask_lines = [
                _("No... It is... Are you... Are you happy like this? Do you like doing this with him?"),
                _("I... Just tell me... Is this what you want? Do you want to be with him like this?"),
            ]
        $ Say_Line(npc, _tl(renpy.random.choice(_disc_ask_lines)))

        # Girl confirms — looking down/away, conflicted
        $ set_scene_expression(girl, None, eyes="eyes_side", brows="brows_sad", mouth="mouth_sad")
        python:
            if girl.has_trait("cheater"):
                _disc_confirm_lines = [
                    _("Yes. And I'm not going to apologize for it."),
                    _("Yes. I know it's messed up, but yes."),
                ]
                set_scene_expression(girl, None, eyes="eyes_side", brows="brows_normal", mouth="mouth_serious")
            else:
                _disc_confirm_lines = [
                    _("Yes... I'm so sorry..."),
                    _("I... yes... I'm sorry, I really am..."),
                    _("Yes... I don't know what to say... I'm sorry..."),
                ]
        $ Say_Line(girl, _tl(renpy.random.choice(_disc_confirm_lines)))

        # NPC accepts reluctantly
        python:
            _disc_accept_lines = [
                _("No... It's fine... Keep going. Really. We'll talk later."),
                _("I... okay. Just... finish what you're doing. We'll talk about this later."),
            ]
        $ Say_Line(npc, _tl(renpy.random.choice(_disc_accept_lines)))

        # Girl watches NPC leave — sad, eyes follow him out
        $ set_scene_expression(girl, None, eyes="eyes_side", brows="brows_sad", mouth="mouth_serious")

        # NPC exits — he leaves them alone
        python:
            _disc_leave_line = _tl(_("%s turns away and quietly leaves the room.")) % npc.Name
        "[_disc_leave_line]"
        $ _hide_witness_exit(npc)

        # NPC left the room — clear watching flag, set kick for after scene
        python:
            _ntr_npc_leaves_scene(npc, girl)
            store._ntr_discovery_kick = True
            girl._ntr_discovery_pending = True
            girl._ntr_discovery_npc_id = npc.partner_id
            debug_log("[NTR_DISCOVERY] Within bounds: %s left room, scene continues, kick pending" % npc.name)

        # Re-render scene (NPC left, just girl + player remain)
        call _rerender_sex_scene(girl, act_type) from _call_rerender_ntr_discovery

    else:
        # ── VIOLATION: Act exceeds boundary — angry catch ──

        # Girl freezes — terrified, looking at NPC
        $ set_scene_expression(girl, None, eyes="eyes_side", brows="brows_surprised", mouth="mouth_surprised")

        python:
            _disc_fury_pool = [
                _("%s... What the HELL?! With HIM?! Like THAT?!"),
                _("Are you KIDDING me?! %s, what is this?!"),
                _("No... No, no, no! %s! What are you DOING?!"),
            ]
            _disc_fury_line = _tl(renpy.random.choice(_disc_fury_pool)) % girl.Name
        $ Say_Line(npc, _disc_fury_line)

        # Girl panics — scared, can't look at NPC
        $ set_scene_expression(girl, None, eyes="eyes_side_2", brows="brows_sad", mouth="mouth_scared")
        python:
            if girl.has_trait("cheater"):
                _disc_vpanic_lines = [
                    _("So what? You knew this was going to happen eventually."),
                    _("It's not what it looks like... okay, it is, but I don't care."),
                ]
                set_scene_expression(girl, None, eyes="eyes_squint", brows="brows_normal", mouth="mouth_serious")
            else:
                _disc_vpanic_lines = [
                    _("Wait, please, I can explain... I... I can't explain this..."),
                    _("Oh god... this isn't... I'm so sorry, I'm so sorry..."),
                    _("No, wait... please... I didn't mean for this to happen..."),
                ]
        $ Say_Line(girl, _tl(renpy.random.choice(_disc_vpanic_lines)))

        # NPC storms out — girl looks toward him leaving
        $ set_scene_expression(girl, None, eyes="eyes_side", brows="brows_sad", mouth="mouth_sad")
        python:
            _disc_storm_lines = [
                _("I can't even look at you right now. We're DONE talking until I figure this out."),
                _("Don't follow me. Don't call me. I need to think about whether this is over."),
            ]
        $ Say_Line(npc, _tl(renpy.random.choice(_disc_storm_lines)))

        # Girl watches him leave — devastated
        $ set_scene_expression(girl, "scared")
        python:
            _disc_storm_exit = _tl(_("%s storms out, slamming the door.")) % npc.Name
        "[_disc_storm_exit]"
        $ _hide_witness_exit(npc)

        # Scene aborted — NPC left
        python:
            store._npc_witness_scene_aborted = True
            _ntr_npc_leaves_scene(npc, girl)
            Change_Status(girl, "Love", -25)
            Change_Status(girl, "Obed", 15)
            npc.change_friendship(-150)
            npc.change_love(-30)
            girl.change_bf_loyalty(-80)
            girl._ntr_discovery_pending = True
            girl._ntr_discovery_npc_id = npc.partner_id
            girl._ntr_discovery_was_violation = True
            girl._ntr_discovery_violation_act = act_type
            girl.set_temp_status("unavailable", 2, reason="ntr_violation")
            debug_log("[NTR_DISCOVERY] Violation: %s furious, scene aborted, act=%s" % (npc.name, act_type))

    return

# ============================================================
# NTR Girl Ask NPC (partner watching — girl directs request to NPC)
# ============================================================

label _ntr_girl_ask_npc(girl, npc, request_type):
    $ store._ntr_npc_authorized = False
    $ store._ntr_npc_request_type = request_type
    $ store._ntr_npc_poss = _npc_poss(npc)

    $ set_scene_expression(girl, "lusty", blush="2")

    python:
        _ask_pool = _NTR_GIRL_ASK_NPC_POOLS.get(request_type)
        if _ask_pool is None:
            debug_log("[NTR_ASK_NPC] Unknown request_type: %s" % request_type)
        else:
            _ask_line = _ntr_girl_line(_ask_pool, girl)
            _ask_line = _ask_line.replace("%(name)s", npc.Name)

    if _ask_pool is None:
        return

    $ Say_Line(girl, _ask_line)

    python:
        _bar_gain = _NTR_ASK_BAR_GAIN.get(request_type, 8)
        _ntr_increase_boundary_bar(npc, girl, _bar_gain)
        debug_log("[NTR_ASK_NPC] %s asked %s for '%s', bar +%d" % (girl.Name, npc.Name, request_type, _bar_gain))

        _authorized = _npc_authorize_roll(npc, request_type)
        store._ntr_npc_authorized = _authorized

    if _authorized:
        $ unlock_achievement("ask_permission")
        $ _npc_say_response(npc, girl, _NPC_AUTHORIZE_RESPONSE, request_type)

        $ set_scene_expression(girl, "ahegao", blush="3")
        python:
            _react_line = _ntr_girl_line(_NTR_GIRL_NPC_AUTHORIZED, girl)
            _react_line = _react_line.replace("%(name)s", npc.Name)
        $ Say_Line(girl, _react_line)
    else:
        $ _npc_say_response(npc, girl, _NPC_DENY_RESPONSE, request_type)

        $ set_scene_expression(girl, "sad", blush="1")
        python:
            _react_line = _ntr_girl_line(_NTR_GIRL_NPC_DENIED, girl)
            _react_line = _react_line.replace("%(name)s", npc.Name)
        $ Say_Line(girl, _react_line)

    return


label _ntr_authorized_done(girl, npc, request_type):
    python:
        Change_Status(girl, "Obed", 10)
        Change_Status(girl, "Love", 5)
        npc.friendship_with_player = min(1000, npc.friendship_with_player + 15)
        _auth_new_level = _NTR_ASK_REQUIRED_LEVEL.get(request_type, 0)
        _auth_old_level = getattr(npc, "_ntr_boundary_level", 1)
        _auth_upgraded = False
        if _auth_new_level > _auth_old_level:
            npc._ntr_boundary_level = _auth_new_level
            npc._ntr_boundary_bar = 0
            _auth_upgraded = True
            debug_log("[NTR_AUTH_DONE] %s: level up %d -> %d (authorized %s)" % (npc.name, _auth_old_level, _auth_new_level, request_type))
            # an authorization that opens his LAST level is "all limits given up" too (the bar is not the only way)
            if _auth_new_level >= 4:
                unlock_achievement("full_access")
        # NPC explicitly authorized penetration at level 2 → implicitly accepts raw
        if not _auth_upgraded and request_type in ("penetration", "full_sex") and _auth_old_level == 2:
            npc._ntr_boundary_level = 3
            npc._ntr_boundary_bar = 0
            debug_log("[NTR_AUTH_DONE] %s: level up 2 -> 3 (NPC authorized penetration, implies raw)" % npc.name)
        if _auth_upgraded or npc._ntr_boundary_level != _auth_old_level:
            _ntr_save_state(npc, girl)
        debug_log("[NTR_AUTH_DONE] %s: NPC authorized + player did it. Obed+10 Love+5 friendship+15" % request_type)

        _f = npc.friendship_with_player
        if _f >= 500:
            _obeyed_tier = "friendly"
        elif _f >= 200:
            _obeyed_tier = "neutral"
        else:
            _obeyed_tier = "hostile"
        if npc.has_trait("voyeur"):
            _obeyed_tier = "voyeur"
        _obeyed_lines = _NPC_PLAYER_OBEYED.get(_obeyed_tier, _NPC_PLAYER_OBEYED.get("neutral", ["..."]))
        _obeyed_line = _tl(renpy.random.choice(_obeyed_lines))
        _obeyed_line = _format_npc_line(npc, _obeyed_line, girl)
    $ renpy.say(Character(npc.Name, who_color=getattr(npc, "color", "#b0bec5")), _obeyed_line)
    return


label _ntr_agreement_broken(girl, npc, request_type):
    python:
        Change_Status(girl, "Obed", 15)
        Change_Status(girl, "Inbt", 10)
        _friendship_loss = 75 if request_type in ("creampie", "anal") else 50
        npc.friendship_with_player = max(0, npc.friendship_with_player - _friendship_loss)
        npc.love_for_girl = max(0, npc.love_for_girl - 20)
        _bar_loss = min(getattr(npc, "_ntr_boundary_bar", 0), 15)
        npc._ntr_boundary_bar = max(0, getattr(npc, "_ntr_boundary_bar", 0) - _bar_loss)
        girl._ntr_boundary_bar = npc._ntr_boundary_bar
        _ntr_save_state(npc, girl)
        debug_log("[NTR_BROKEN] %s: player defied NPC. friendship -%d love_for_girl -20 bar -%d" % (
            request_type, _friendship_loss, _bar_loss))

        _f = npc.friendship_with_player
        if _f >= 500:
            _def_tier = "friendly"
        elif _f >= 200:
            _def_tier = "neutral"
        else:
            _def_tier = "hostile"
        _def_lines = _NPC_PLAYER_DEFIED.get(_def_tier, _NPC_PLAYER_DEFIED.get("neutral", ["..."]))
        _def_line = _tl(renpy.random.choice(_def_lines))
        _def_line = _format_npc_line(npc, _def_line, girl)
    $ renpy.say(Character(npc.Name, who_color=getattr(npc, "color", "#b0bec5")), _def_line)
    return


label _ntr_boundary_respected(girl, npc):
    python:
        npc.friendship_with_player = min(1000, npc.friendship_with_player + 5)
        debug_log("[NTR_RESPECTED] Player respected NPC denial. friendship +5")
    return


# ============================================================
# NTR Escalation Gate (player-initiated menu pre-check)
# ============================================================

label _ntr_escalation_gate(girl, target_act):
    $ store._ntr_gate_passed = True
    if not store._ntr_partner_watching or not store._ntr_watching_npc:
        return
    python:
        _gate_npc = store._ntr_watching_npc
        _gate_level = getattr(_gate_npc, "_ntr_boundary_level", 1)
        _gate_condom = getattr(store, "condom_active", False)
        _gate_is_anal = target_act in ("anal", "anal_switch", "tip_anal")
        if target_act in ("condom_remove", "force_raw"):
            _gate_condom = False
        _gate_pos = "anal" if _gate_is_anal else "sex"
        _gate_within = _ntr_act_within_boundary(_gate_pos, _gate_level, _gate_condom, _gate_is_anal)
    if _gate_within:
        # Spontaneous raw: at level 2 + condom + high Lust, she asks NPC to go raw. Never a hate_cum girl
        # (she "demands condoms"; she can still go raw through the player's own ask, which keeps her creampie blocked)
        if _gate_level == 2 and _gate_condom and girl.Lust >= 60 and not store._ntr_spontaneous_raw_asked and not girl.has_trait("hate_cum") and target_act not in ("condom_remove", "force_raw") and not story_act_locked(girl, "raw"):
            call _ntr_spontaneous_raw_request(girl, _gate_npc) from _call_ntr_gate_spont_raw
        return
    python:
        if _gate_is_anal:
            store._ntr_gate_req = "anal"
        elif target_act in ("condom_remove", "force_raw") or (_gate_level == 2 and not _gate_condom):
            store._ntr_gate_req = "condom_remove"
        elif _gate_level == 1:
            store._ntr_gate_req = "penetration"
        else:
            store._ntr_gate_req = "full_sex"
        debug_log("[NTR_GATE] %s: target=%s level=%d condom=%s req=%s" % (girl.Name, target_act, _gate_level, _gate_condom, store._ntr_gate_req))
    call _ntr_girl_ask_npc(girl, _gate_npc, store._ntr_gate_req) from _call_ntr_gate_ask
    if store._ntr_npc_authorized:
        call _ntr_authorized_done(girl, _gate_npc, store._ntr_gate_req) from _call_ntr_gate_auth_done
        return
    menu:
        "Do it anyway":
            call _ntr_agreement_broken(girl, _gate_npc, store._ntr_gate_req) from _call_ntr_gate_broken
        "Respect [_ntr_npc_poss] decision":
            call _ntr_boundary_respected(girl, _gate_npc) from _call_ntr_gate_respected
            $ store._ntr_gate_passed = False
    return


# ============================================================
# NTR Spontaneous Raw Request
# ============================================================
# At boundary level 2 (condom rule), if the girl is aroused enough (Lust >= 60)
# she spontaneously asks her NPC partner to let the player remove the condom.
# Triggers once per sex session during any escalation that would pass with condom.

label _ntr_spontaneous_raw_request(girl, npc):
    $ store._ntr_spontaneous_raw_asked = True
    $ print("[NTR_SPONT_RAW] %s asks %s to remove condom (Lust=%d)" % (girl.Name, npc.Name, girl.Lust))

    call _ntr_girl_ask_npc(girl, npc, "condom_remove") from _call_ntr_spont_ask

    if store._ntr_npc_authorized:
        menu:
            "Remove the condom":
                $ set_scene_expression(girl, "lewd", blush="2")
                "You nod and pull the condom off."
                python:
                    _spont_pos = None
                    for _sv, _sp in [("_doggy_girl", "doggy"), ("_cowgirl_girl", "cowgirl"), ("_rcg_girl", "reverse_cowgirl"), ("_fn_girl", "full_nelson"), ("_laying_girl", "laying_down")]:
                        if getattr(store, _sv, None) is not None:
                            _spont_pos = _sp
                            break
                # She asked, he allowed: never the cheat-path block. The pose's rip animation hides the condom itself
                # (skip_hide), or it would vanish now and pop back for the slide-out below.
                $ _on_condom_removed(girl, skip_hide=_cum_skip_hide(_spont_pos), force=True)
                $ apply_cum_bonuses(girl, "condom_removed_allowed")
                $ store._creampie_consent = "allowed"
                call _ntr_authorized_done(girl, npc, "condom_remove") from _call_ntr_spont_auth
                if _spont_pos:
                    call _sex_scene_condom_rip_visual(girl, _spont_pos) from _call_crv_ntr_spont
            "Keep it on":
                $ set_scene_expression(girl, "sad")
                python:
                    _keep_line = _format_npc_line(npc, renpy.random.choice([
                        _("But... %(pp)s said it was okay..."),
                        _("Why not? %(Pp)s already agreed..."),
                    ]))
                $ Say_Line(girl, _keep_line)
                $ Change_Status(girl, "Love", -3)
    return


# ============================================================
# NTR Boundary Violation (during scene)
# ============================================================

# ── NTR Condom Break While Watching ──
# NOT a violation. The partner sees the accident, gets excited, auto-levels 2 -> 3.
# Mode (_ntr_cbreak_watch_mode): "told" = she knows, he reacts out loud | "hidden" = only the player knows, he
# noticed first and only THINKS it (she must not find out from him) | "knew" = she has just found out and he had
# noticed earlier: spoken follow-up, no second level-up.
label _ntr_condom_break_watching(girl, npc):
    python:
        _ncb_mode = _ntr_cbreak_watch_mode()
        _ncb_cfg = _NTR_CBREAK_WATCH_MODES[_ncb_mode]
        _ncb_silent = _ncb_cfg["silent"]
        _ncb_level = getattr(npc, "_ntr_boundary_level", 1)
        _ncb_npc_line = _ntr_cbreak_line(npc, girl, _ncb_cfg["pool"])
        _ncb_intro = _ntr_cbreak_line(npc, girl, _NTR_NPC_CBREAK_NARR[_ncb_cfg["intro"]]) if _ncb_cfg["intro"] else None
        _ncb_close = _ntr_cbreak_line(npc, girl, _NTR_NPC_CBREAK_NARR[_ncb_cfg["close"]])
        _ncb_saw = _ncb_cfg["saw"]
        print("[NTR_CBREAK_WATCH] npc=%s girl=%s mode=%s level=%d told=%s hidden=%s saw=%s snapshot=%s" % (
            npc.name, girl.gid, _ncb_mode, _ncb_level, store._condom_broken_told, store._condom_broken_hidden,
            getattr(store, "_condom_break_partner_saw", None), getattr(store, "_condom_break_ntr_level", None)))
        debug_log("[NTR_CBREAK_WATCH] %s sees condom break: mode=%s level=%d" % (npc.name, _ncb_mode, _ncb_level))
        _ncb_cfg = None   # it holds the pool dicts: do not leave them in the saved store

    if _ncb_intro:
        "[_ncb_intro]"

    # "hidden": a spoken line would tell her. Thinking() shows it in parentheses under his name (unspoken).
    if _ncb_silent:
        $ Thinking(npc, _ncb_npc_line)
    else:
        $ Say_Line(npc, _ncb_npc_line)

    # Auto level up 2 -> 3, once ("knew" arrives here already at 3)
    python:
        if getattr(store, "_condom_break_ntr_level", None) is None:
            store._condom_break_ntr_level = _ncb_level   # no snapshot (older save / QA): keep what SHE knows
        if _ncb_level == 2:
            npc._ntr_boundary_level = 3
            npc._ntr_boundary_bar = 0
            _ntr_save_state(npc, girl)
            girl._ntr_levelup_pending = True   # next day she texts the new rule, so the player SEES the progress
            print("[NTR_CBREAK_WATCH] %s level 2 -> 3 (mode=%s)" % (npc.name, _ncb_mode))
            debug_log("[NTR_CBREAK_WATCH] %s auto level up -> 3 (raw sex now allowed)" % npc.name)
        else:
            print("[NTR_CBREAK_WATCH] %s no level change (level=%d mode=%s)" % (npc.name, _ncb_level, _ncb_mode))
        store._condom_break_partner_saw = _ncb_saw

    "[_ncb_close]"
    return


# ============================================================
# Hostile NTR: Mini-dialogue exchanges (NPC begs girl, girl responds)
# ============================================================

label _ntr_hostile_mini_dialogue(girl, npc):
    python:
        _hmd_surrendered = getattr(npc, "_ntr_hostile_surrendered", False)
        if _hmd_surrendered:
            _hmd_npc_line = _tl(renpy.random.choice(_NTR_HOSTILE_POST_SURRENDER["npc"]))
            _hmd_girl_pool = _NTR_HOSTILE_POST_SURRENDER["girl"]
        else:
            _hmd_speed = _ntr_get_current_speed()
            _hmd_tier = "fast" if _hmd_speed >= 3 else ("medium" if _hmd_speed >= 2 else "slow")
            _hmd_girl_st, _hmd_pos, _hmd_anal, _hmd_condom = _ntr_get_scene_state()
            _hmd_cat = _ntr_act_to_category(_hmd_pos if _hmd_pos else "penetration")
            _hmd_key = (_hmd_tier, _hmd_cat)
            _hmd_entry = _NTR_HOSTILE_MINI_DIALOGUES.get(_hmd_key)
    if not _hmd_surrendered and _hmd_entry is None:
        return
    python:
        if not _hmd_surrendered:
            _hmd_npc_line = _tl(renpy.random.choice(_hmd_entry["npc"]))
            _hmd_girl_pool = _hmd_entry["girl"]
        _hmd_girl_key = "_default"
        for _hmd_t in ("cum_slut", "femdom", "submissive", "hardcore_sex", "cute_sex"):
            _hmd_tk = _hmd_t.replace("_sex", "") if "_sex" in _hmd_t else _hmd_t
            if hasattr(girl, "has_trait") and girl.has_trait(_hmd_t) and _hmd_tk in _hmd_girl_pool:
                _hmd_girl_key = _hmd_tk
                break
        _hmd_girl_line = _format_partner_line(girl, renpy.random.choice(_hmd_girl_pool.get(_hmd_girl_key, _hmd_girl_pool["_default"])))
        npc._ntr_hostile_mini_count = getattr(npc, "_ntr_hostile_mini_count", 0) + 1
        debug_log("[NTR_HOSTILE_MINI] %s -> %s: surrendered=%s trait=%s count=%d" % (npc.name, girl.gid, _hmd_surrendered, _hmd_girl_key, npc._ntr_hostile_mini_count))
    $ Say_Line(npc, _hmd_npc_line)
    $ Say_Line(girl, _hmd_girl_line)
    $ _ntr_increase_boundary_bar(npc, girl, 3)
    return


# ============================================================
# Hostile NTR: Surrender event (NPC stops begging, starts directing)
# Triggers: boundary 4 + 8 mini-dialogues + speed 3 + penetration
# ============================================================

label _ntr_hostile_surrender(girl, npc):
    python:
        _nhs_trans = _tl(renpy.random.choice(_NTR_HOSTILE_SURRENDER["npc_transition"]))
        _nhs_direct = _tl(renpy.random.choice(_NTR_HOSTILE_SURRENDER["npc_directing"]))
        _nhs_girl_pool = _NTR_HOSTILE_SURRENDER["girl"]
        _nhs_girl_key = "_default"
        for _nhs_t in ("cum_slut", "hardcore_sex", "cute_sex"):
            _nhs_tk = _nhs_t.replace("_sex", "") if "_sex" in _nhs_t else _nhs_t
            if hasattr(girl, "has_trait") and girl.has_trait(_nhs_t) and _nhs_tk in _nhs_girl_pool:
                _nhs_girl_key = _nhs_tk
                break
        _nhs_girl_line = _tl(renpy.random.choice(_nhs_girl_pool[_nhs_girl_key]))
        _nhs_after = _tl(renpy.random.choice(_NTR_HOSTILE_SURRENDER["npc_aftermath"]))
        npc._ntr_hostile_surrendered = True
        debug_log("[NTR_HOSTILE_SURRENDER] %s surrendered! girl=%s" % (npc.name, girl.gid))

    $ Say_Line(npc, _nhs_trans)

    python:
        _nhs_narr = _tl(_("Something shifts in %s's voice. The begging is gone. Replaced by something else entirely.")) % npc.Name
    "[_nhs_narr]"

    $ Say_Line(npc, _nhs_direct)
    $ Say_Line(girl, _nhs_girl_line)
    $ Say_Line(npc, _nhs_after)

    python:
        _nhs_final = _tl(_("%s's eyes are hollow but hungry. The person who walked in begging is gone. What's left is worse... and more honest.")) % npc.Name
    "[_nhs_final]"

    $ _ntr_increase_boundary_bar(npc, girl, 15)

    if Player.attractiveness <= 25:
        $ unlock_achievement("ugly_bastard")

    return


label _ntr_boundary_violation(girl, npc, act_type):
    $ store._npc_witness_scene_aborted = False
    $ debug_log("[NTR_VIOLATION] %s violated boundary! girl=%s act=%s level=%d" % (npc.name, girl.gid, act_type, getattr(npc, "_ntr_boundary_level", 1)))

    python:
        _ntr_v_bl = getattr(npc, "_ntr_boundary_level", 1)
        _ntr_v_is_anal = act_type in _ANAL_SCENE_TYPES or (act_type == "doggy" and getattr(store, "doggy_anal", False)) or (act_type == "full_nelson" and getattr(store, "fn_anal", False)) or (act_type == "laying_down" and getattr(store, "laying_anal", False)) or (act_type == "reverse_cowgirl" and getattr(store, "rcg_anal", False))
        _ntr_v_is_tip = _ntr_is_tip_mode()
        _ntr_v_hostile = _ntr_is_hostile_mode(npc)
        if _ntr_v_hostile:
            if _ntr_v_bl == 1:
                _ntr_v_warning = _tl(_("Please... please don't do that. We agreed no penetration. I'm begging you..."))
            elif _ntr_v_bl == 2:
                if _ntr_v_is_anal:
                    _ntr_v_warning = _tl(_("Not that... please... anal was not part of this. I can't handle that..."))
                else:
                    _ntr_v_warning = _tl(_("Where's the condom...? You promised... please put it back on... please..."))
            elif _ntr_v_bl == 3:
                if _ntr_v_is_anal:
                    _ntr_v_warning = _tl(_("No... not that... please... that's the one thing I can't watch... please stop..."))
                else:
                    _ntr_v_warning = _tl(_("Don't finish inside... that's all I ask... please... I'm begging you..."))
            else:
                _ntr_v_warning = _tl(_("Please stop... I know I said anything but... this is too much... please..."))
            _ntr_v_entrance = _tl(_("%s steps forward, shaking, tears in their eyes.")) % npc.Name
        else:
            if _ntr_v_bl == 1:
                _ntr_v_warning = _tl(_("Hey! We agreed no penetration! Stop right now!"))
            elif _ntr_v_bl == 2:
                if _ntr_v_is_anal:
                    _ntr_v_warning = _tl(_("Hey! Anal was NOT part of the deal! Stop!"))
                else:
                    _ntr_v_warning = _tl(_("Where's the condom?! We agreed on protection! Stop!"))
            elif _ntr_v_bl == 3:
                if _ntr_v_is_anal:
                    _ntr_v_warning = _tl(_("No anal! That was the one rule! Stop right now!"))
                else:
                    _ntr_v_warning = _tl(_("Don't you dare finish inside! We had a deal!"))
            else:
                _ntr_v_warning = _tl(_("That's too far! Stop!"))
            _ntr_v_entrance = _tl(_("%s steps forward, visibly upset.")) % npc.Name

    "[_ntr_v_entrance]"
    # Girl shocked — NPC just caught them
    $ set_scene_expression(girl, None, eyes="eyes_side", brows="brows_surprised", mouth="mouth_surprised")
    $ Say_Line(npc, _ntr_v_warning)

    # "Just the tip" negotiation: girl defends if boundary is 1 and act is tip
    if _ntr_v_bl == 1 and _ntr_v_is_tip:
        # Girl pleads with NPC — desperate, looking at him
        $ set_scene_expression(girl, None, eyes="eyes_side", brows="brows_sad", mouth="mouth_sad")
        python:
            _ntr_v_tip_girl_line = _tl(_("C'mon baby... It's just the tip, it's not fully in... it barely counts, please..."))
        $ Say_Line(girl, _ntr_v_tip_girl_line)

        # NPC decides based on love
        python:
            _ntr_v_npc_love = getattr(npc, "love_for_girl", 750)
            _ntr_v_tip_accepted = _ntr_v_npc_love >= 500
            debug_log("[NTR_VIOLATION] Tip negotiation: npc_love=%d accepted=%s" % (_ntr_v_npc_love, _ntr_v_tip_accepted))

        if _ntr_v_tip_accepted:
            # Girl relieved — grateful look
            $ set_scene_expression(girl, None, eyes="eyes_side", brows="brows_confused", mouth="mouth_surprised")
            python:
                _ntr_v_tip_accept_pool = [
                    _("...Fine. JUST the tip. But if I see anything more, we're done."),
                    _("...Okay. But only the tip. I swear, if you go any further..."),
                ]
            $ Say_Line(npc, _tl(renpy.random.choice(_ntr_v_tip_accept_pool)))
            $ Change_NPC_Status(npc, "friendship_with_player", -30)
            python:
                _ntr_increase_boundary_bar(npc, girl, 15)
                store._ntr_tip_accepted = True
                debug_log("[NTR_VIOLATION] Tip negotiation accepted! friendship -30, bar +15")
            return
        else:
            # Girl scared — NPC is firm
            $ set_scene_expression(girl, None, eyes="eyes_side_2", brows="brows_surprised", mouth="mouth_scared")
            python:
                _ntr_v_tip_deny_pool = [
                    _("No! I don't care if it's 'just the tip'. No penetration means NO penetration!"),
                    _("I said no penetration! I don't want to hear excuses!"),
                ]
            $ Say_Line(npc, _tl(renpy.random.choice(_ntr_v_tip_deny_pool)))

    # Girl reaction based on stats
    python:
        _ntr_v_girl_loves_player = girl.Love >= 600
        _ntr_v_girl_high_obed = girl.Obed >= 500
        if _ntr_v_girl_loves_player:
            _ntr_v_girl_react = _tl(_("%s looks at you, then back at %s, conflicted.")) % (girl.Name, npc.Name)
        elif _ntr_v_girl_high_obed:
            _ntr_v_girl_react = _tl(_("%s freezes, waiting to see what you decide.")) % girl.Name
        else:
            _ntr_v_girl_react = _tl(_("%s flinches, clearly uncomfortable with the situation.")) % girl.Name

    "[_ntr_v_girl_react]"

    menu:
        "Stop (respect the boundary)":
            $ Change_NPC_Status(npc, "friendship_with_player", -20)
            $ debug_log("[NTR_VIOLATION] Player stopped. friendship -20")
            # Girl looks relieved, watching NPC
            $ set_scene_expression(girl, None, eyes="eyes_side", brows="brows_sad", mouth="mouth_serious")
            if _ntr_v_hostile:
                python:
                    _ntr_v_breath = _tl(_("%s's shoulders drop. Relief and shame mix on their face.")) % npc.Name
                "[_ntr_v_breath]"
                $ Say_Line(npc, _tl(_("...Thank you. I hate that I'm grateful for this.")))
                python:
                    _ntr_v_stop_leave = _tl(_("%s wipes their eyes and stumbles out of the room.")) % npc.Name
                "[_ntr_v_stop_leave]"
            else:
                python:
                    _ntr_v_breath = _tl(_("%s takes a deep breath.")) % npc.Name
                "[_ntr_v_breath]"
                $ Say_Line(npc, _tl(_("Thank you. I appreciate you respecting our agreement.")))
                python:
                    _ntr_v_stop_leave = _tl(_("%s nods and quietly leaves the room.")) % npc.Name
                "[_ntr_v_stop_leave]"
            $ _hide_witness_exit(npc)
            $ _ntr_npc_leaves_scene(npc, girl)
            # NTR stop: end current act but stay in sex menu (don't fully exit)
            $ store._npc_witness_scene_aborted = True
            $ store._ntr_violation_stopped = True

        "Continue anyway":
            $ Change_NPC_Status(npc, "friendship_with_player", -150)
            python:
                _old_bar = getattr(npc, "_ntr_boundary_bar", 0)
                npc._ntr_boundary_bar = max(0, _old_bar - 30)
                girl._ntr_boundary_bar = npc._ntr_boundary_bar
            $ Change_Status(girl, "Obed", 15)
            $ Change_Status(girl, "Inbt", 10)
            $ debug_log("[NTR_VIOLATION] Player continues! friendship -150, bar -30, Obed +15, Inbt +10")
            # Girl looks away, conflicted
            $ set_scene_expression(girl, None, eyes="eyes_side_2", brows="brows_confused", mouth="mouth_serious")
            if _ntr_v_hostile:
                python:
                    _ntr_v_disbelief = _tl(_("%s's voice breaks. Their hands drop to their sides.")) % npc.Name
                "[_ntr_v_disbelief]"
                $ Say_Line(npc, _tl(_("You... you don't even care, do you...?")))
                $ set_scene_expression(girl, None, eyes="eyes_side", brows="brows_sad", mouth="mouth_scared")
                python:
                    _ntr_v_storm = _tl(_("You don't stop. %s stands there for a long moment, fists trembling, then stumbles out of the room.")) % npc.Name
                "[_ntr_v_storm]"
            else:
                python:
                    _ntr_v_disbelief = _tl(_("%s stares at you in disbelief.")) % npc.Name
                "[_ntr_v_disbelief]"
                $ Say_Line(npc, _tl(_("Are you serious?! We had a deal!")))
                $ set_scene_expression(girl, None, eyes="eyes_side", brows="brows_sad", mouth="mouth_scared")
                python:
                    _ntr_v_storm = _tl(_("But you don't stop. %s clenches both fists, then turns and storms out.")) % npc.Name
                "[_ntr_v_storm]"
            $ _hide_witness_exit(npc)
            $ _ntr_npc_leaves_scene(npc, girl)
            $ girl._ntr_violation_pending = True
            $ unlock_achievement("boundary_broken")

    return

# ============================================================
# ChitChat: Breakup Suggestion (Love=1000)
# ============================================================

label _npc_breakup_suggestion_chat(girl):
    $ _partner = girl.partner_label()

    if girl.has_trait("lesbian"):
        $ set_scene_expression(girl, "serious")
        $ Say_Line(girl, _("Hey... I know what we do together. But my [_partner] is everything to me."))
        $ Say_Line(girl, _("Whatever this is between us... it's not love. I hope you understand that."))
        $ Change_Status(girl, "Love", -15)
        $ girl._will_break_up_with_partner = False
        $ set_scene_expression(girl, "normal")
        return

    $ set_scene_expression(girl, "worried")
    $ Say_Line(girl, _("Hey... can I ask you something?"))
    $ Say_Line(girl, _("Do you think I should break up with my [_partner]?"))

    menu:
        "Yes, you deserve better.":
            $ set_scene_expression(girl, "sad")
            $ Say_Line(girl, _("You're right... I've been thinking about it for a while."))
            $ Say_Line(girl, _tl(_("I'll talk to %s tonight.")) % girl.partner_label())
            python:
                if girl.has_trait("has_boyfriend"):
                    girl.remove_trait("has_boyfriend")
                elif girl.has_trait("has_girlfriend"):
                    girl.remove_trait("has_girlfriend")
                girl._left_partner_for_player = True
                girl.clear_npc_partner()
                girl._will_break_up_with_partner = False
                Change_Status(girl, "Love", 50)
                debug_log("[NPC_BREAKUP] %s voluntary breakup via chitchat" % girl.gid)
            $ set_scene_expression(girl, "happy")
            $ Say_Line(girl, _("It's done. I feel... lighter already."))
            $ set_scene_expression(girl, "normal")

        "No, I think you should stay with them.":
            $ set_scene_expression(girl, "uncomfortable")
            $ Say_Line(girl, _("Really? ...Okay. Maybe you're right."))
            $ set_scene_expression(girl, "normal")
            $ girl._will_break_up_with_partner = False

        "That's your decision, not mine.":
            $ set_scene_expression(girl, "worried")
            $ Say_Line(girl, _("I know... I just needed to hear someone say it. I'll think about it."))
            $ set_scene_expression(girl, "normal")
            $ girl._will_break_up_with_partner = False

    return

# ============================================================
# NPC Phone Chat
# ============================================================

label npc_phone_open_chat(npc):

    $ store._phone_chat_exit = "back"

    label .chat_loop:

    python:
        _npc_chat_cd = npc_phone_chat_on_cooldown(npc)
        _npc_has_vids = bool(getattr(store.Player, "recorded_videos", []))
        _npc_chat_choices = []
        if _npc_chat_cd:
            _npc_chat_choices.append((_("Chit Chat") + " {size=14}(" + _("already texted today") + "){/size}", "cooldown", True))
            _npc_chat_choices.append((_("Send Video") + " {size=14}(" + _("already texted today") + "){/size}", "cooldown_vid", True))
        else:
            _npc_chat_choices.append((_("Chit Chat"), "chitchat", False))
            if _npc_has_vids:
                _npc_chat_choices.append((_("Send Video"), "send_video", False))
            else:
                _npc_chat_choices.append((_("Send Video") + " {size=14}(" + _("no videos") + "){/size}", "no_vids", True))

    call screen phone_chat_screen(npc, choices=_npc_chat_choices, can_leave=True)
    $ _npc_chat_action = _return

    if _npc_chat_action == "home":
        $ store._phone_chat_exit = "home"
        $ _phone_restore_others()
        return

    if _npc_chat_action == "chitchat":
        python:
            _npc_girl_c = GIRL_BY_ID.get(npc.girl_gid)
            _girl_name_c = _npc_girl_c.Name if _npc_girl_c else "her"
            _convo = _npc_pick_phone_convo(npc, _girl_name_c)
            phone_add_msg(npc.gid, "player", _convo["p"])
        call _phone_typing(npc, choices=[]) from _typing_npc_chat
        $ phone_add_msg(npc.gid, npc.gid, _convo["n"])
        if _convo.get("p2"):
            $ phone_add_msg(npc.gid, "player", _convo["p2"])
            call _phone_typing(npc, choices=[]) from _typing_npc_chat_2
            if _convo.get("n2"):
                $ phone_add_msg(npc.gid, npc.gid, _convo["n2"])
        python:
            _tier_c = _npc_friendship_tier(npc)
            _gain = _npc_chat_friendship_gain(_tier_c)
            Change_NPC_Status(npc, "friendship_with_player", _gain)
            if _tier_c == "hostile":
                Change_NPC_Status(npc, "suspicion", 3)
                debug_log("[NPC_PHONE] %s hostile chat +%d friendship +3 suspicion (now f=%d s=%d)" % (npc.name, _gain, npc.friendship_with_player, npc.suspicion))
            else:
                debug_log("[NPC_PHONE] %s %s chat +%d friendship (now %d)" % (npc.name, _tier_c, _gain, npc.friendship_with_player))
            npc_phone_chat_set_cooldown(npc)
        jump .chat_loop

    if _npc_chat_action == "send_video":
        call _npc_phone_send_video(npc) from _call_npc_send_video
        jump .chat_loop

    if _npc_chat_action in ("cooldown", "cooldown_vid", "no_vids"):
        jump .chat_loop

    $ store._phone_chat_exit = "back"
    return

# ============================================================
# NPC Phone — Send Video
# ============================================================

label _npc_phone_send_video(npc):

    python:
        _vids = getattr(store.Player, "recorded_videos", [])
    if not _vids:
        $ phone_add_msg(npc.gid, "system", _("You don't have any recorded videos."))
        return

    # Step 1: Pick girl from videos
    python:
        _girl_gids = sorted(set(v["girl_gid"] for v in _vids))
        _vid_girl_choices = []
        for _gid in _girl_gids:
            _cg = GIRL_BY_ID.get(_gid)
            if _cg:
                _vid_girl_choices.append((_cg.Name, _gid))
    call screen phone_chat_screen(npc, choices=_vid_girl_choices, can_leave=True)
    $ _chosen_gid = _return
    if _chosen_gid == "home":
        $ store._phone_chat_exit = "home"
        $ _phone_restore_others()
        return
    if _chosen_gid in (None, "close"):
        return

    # Step 2: Pick position (split by face_hidden)
    python:
        _gid_vids = [v for v in _vids if v["girl_gid"] == _chosen_gid]
        _combos = set()
        for _cv in _gid_vids:
            if _cv.get("special"):
                continue
            _var = "nc" if not _cv.get("consensual", True) else ("h" if _cv.get("face_hidden", True) else "v")
            _combos.add((_cv["type"], _var))
        _combos = sorted(_combos)
        _vid_pos_choices = []
        for _pos, _var in _combos:
            _label = _pk_t(VIDEO_TYPE_DISPLAY.get(_pos, _pos.replace("_", " ").title()))
            if _var == "nc":
                _label += " {size=18}(" + _tl(_("non-consensual")) + "){/size}"
            elif _var == "h":
                _label += " {size=18}(" + _tl(_("hidden face")) + "){/size}"
            else:
                _label += " {size=18}(" + _("face visible") + "){/size}"
            _vid_pos_choices.append((_label, _pos + "|" + _var))
        _has_special = any(v.get("special") for v in _gid_vids)
        if _has_special:
            _vid_pos_choices.append((_("SPECIAL"), "special"))
    call screen phone_chat_screen(npc, choices=_vid_pos_choices, can_leave=True)
    $ _chosen_pos = _return
    if _chosen_pos == "home":
        $ store._phone_chat_exit = "home"
        $ _phone_restore_others()
        return
    if _chosen_pos in (None, "close"):
        return

    # Parse variant from choice value
    python:
        _chosen_face_hidden = None
        _chosen_nonconsensual = False
        if _chosen_pos and "|" in str(_chosen_pos):
            _pparts = _chosen_pos.split("|")
            _chosen_pos = _pparts[0]
            if _pparts[1] == "nc":
                _chosen_nonconsensual = True
            elif _pparts[1] == "h":
                _chosen_face_hidden = True
            else:
                _chosen_face_hidden = False

    # Step 2b: If SPECIAL, pick the specific special type
    if _chosen_pos == "special":
        python:
            _special_types = sorted(set(v.get("special") for v in _gid_vids if v.get("special")))
            _special_choices = [(SPECIAL_VIDEO_DISPLAY.get(s, s.title()), s) for s in _special_types]
        call screen phone_chat_screen(npc, choices=_special_choices, can_leave=True)
        $ _chosen_special = _return
        if _chosen_special == "home":
            $ store._phone_chat_exit = "home"
            $ _phone_restore_others()
            return
        if _chosen_special in (None, "close"):
            return

    # Step 3: Pick location (if multiple)
    python:
        if _chosen_pos == "special":
            _matching = [v for v in _vids if v["girl_gid"] == _chosen_gid and v.get("special") == _chosen_special]
        elif _chosen_nonconsensual:
            _matching = [v for v in _vids if v["girl_gid"] == _chosen_gid and v["type"] == _chosen_pos and not v.get("special") and not v.get("consensual", True)]
        else:
            _matching = [v for v in _vids if v["girl_gid"] == _chosen_gid and v["type"] == _chosen_pos and not v.get("special") and v.get("consensual", True)]
            if _chosen_face_hidden is not None:
                _matching = [v for v in _matching if v.get("face_hidden", True) == _chosen_face_hidden]
        _locs = sorted(set(v.get("location", "unknown") for v in _matching))
    if len(_locs) > 1:
        python:
            _VID_LOC_NAMES = {
                "campus": _tr("Campus"), "pool": _tr("Pool"), "showers": _tr("Showers"), "apartment": _tr("Apartment"), "apartment_room": _tr("Apartment Bedroom"), "apartment_shower": _tr("Apartment Bathroom"),
                "room": _tr("%s's Room") % store.Player.Name,
                "gwen_room": _tr("Gwen's Room"), "rogue_room": _tr("Rogue's Room"), "ntw_room": _tr("Negasonic's Room"), "tenny_room": _tr("%s's Room") % GIRL_BY_ID["tenny"].Name,
                "classroom": _tr("Classroom"), "gym": _tr("Gym"), "hall": _tr("Hall"),
                "street": _tr("Street"), "mall": _tr("Mall"), "party": _tr("Party"),
            }
            _vid_loc_choices = [(_VID_LOC_NAMES.get(l, l.replace("_", " ").title()), l) for l in _locs]
        call screen phone_chat_screen(npc, choices=_vid_loc_choices, can_leave=True)
        $ _chosen_loc = _return
        if _chosen_loc == "home":
            $ store._phone_chat_exit = "home"
            $ _phone_restore_others()
            return
    else:
        $ _chosen_loc = _locs[0] if _locs else None

    if _chosen_loc in (None, "close"):
        return

    # Step 4: Select the video
    python:
        _loc_vids = [v for v in _matching if v.get("location", "") == _chosen_loc]
        _sent_vid = _loc_vids[-1] if _loc_vids else (_matching[-1] if _matching else {"girl_gid": _chosen_gid, "type": _chosen_pos, "location": _chosen_loc, "face_hidden": True})

    # Send player system message with video description
    python:
        _vid_girl = GIRL_BY_ID.get(_sent_vid.get("girl_gid", ""))
        _vid_name = _vid_girl.Name if _vid_girl else "her"
        _vid_pos = _sent_vid.get("type", "unknown")
        _vid_loc = _sent_vid.get("location", "")
        _vid_special = _sent_vid.get("special")
        _vid_loc_names = {
            "room": _("in your room"), "campus": _("on campus"), "pool": _("at the pool"),
            "hall": _("in the hallway"), "street": _("on the street"), "mall": _("at the mall"),
            "party": _("at the party"), "gym": _("at the gym"), "classroom": _("in the classroom"),
            "showers": _("in the showers"), "apartment": _("in the apartment"), "apartment_room": _("in the bedroom"), "apartment_shower": _("in the bathroom"), "shower": _("in the shower"), "bathroom": _("in the bathroom"),
            "gwen_room": _("in a dorm room"), "rogue_room": _("in a dorm room"), "ntw_room": _("in a dorm room"),
        }
        if _vid_loc == _sent_vid.get("girl_gid", "") + "_room":
            _vid_loc_names[_vid_loc] = _("in her room")
        _vid_loc_str = _tl(_vid_loc_names.get(_vid_loc, ""))
        _NPC_VID_SEND_DESCS = {
            "hj": renpy.random.choice([
                _("You sent a video of %s jerking you off %s"),
                _("You sent a video of %s stroking your cock %s"),
            ]),
            "bj": renpy.random.choice([
                _("You sent a video of %s sucking your dick %s"),
                _("You sent a video of %s going down on you %s"),
            ]),
            "tj": renpy.random.choice([
                _("You sent a video of %s's tits wrapped around your dick %s"),
                _("You sent a video of %s giving you a titjob %s"),
            ]),
            "cowgirl": renpy.random.choice([
                _("You sent a video of %s riding you %s"),
                _("You sent a video of %s bouncing on your cock %s"),
            ]),
            "reverse_cowgirl": renpy.random.choice([
                _("You sent a video of %s riding you in reverse %s"),
                _("You sent a video of %s on top of you facing away %s"),
            ]),
            "doggy": renpy.random.choice([
                _("You sent a video of you taking %s from behind %s"),
                _("You sent a video of you bending %s over %s"),
            ]),
            "full_nelson": renpy.random.choice([
                _("You sent a video of you pounding %s in full nelson %s"),
                _("You sent a video of %s held up and getting fucked %s"),
            ]),
            "full_nelson_anal": _("You sent a video of you doing %s's ass in full nelson %s"),
            "reverse_cowgirl_anal": _("You sent a video of %s riding you in reverse with it in her ass %s"),
            "laying_down": renpy.random.choice([
                _("You sent a video of you fucking %s while she's laying down %s"),
                _("You sent a video of %s on her back taking it %s"),
            ]),
            "laying_anal": _("You sent a video of you doing %s's ass while she lays there %s"),
            "anal": renpy.random.choice([
                _("You sent a video of you doing anal with %s %s"),
                _("You sent a video of you taking %s's ass %s"),
            ]),
            "creampie": renpy.random.choice([
                _("You sent a video of you cumming inside %s %s"),
                _("You sent a video of you finishing deep inside %s %s"),
            ]),
            "masturbate": renpy.random.choice([
                _("You sent a video of %s touching herself %s"),
                _("You sent a video of %s pleasuring herself %s"),
            ]),
            "sex": renpy.random.choice([
                _("You sent a video of you fucking %s %s"),
                _("You sent a video of you deep inside %s %s"),
            ]),
        }
        if _vid_special == "virginity":
            _vid_send_msg = _tl(_("You sent a video of %s losing her virginity %s")) % (_vid_name, _vid_loc_str)
        else:
            _vid_send_msg = _tl(_NPC_VID_SEND_DESCS.get(_vid_pos, _("You sent a video of %s %s"))) % (_vid_name, _vid_loc_str)
        _vid_send_msg = _vid_send_msg.strip()
    $ phone_add_msg(npc.gid, "player", _vid_send_msg, "system")

    # NPC typing animation
    call _phone_typing(npc, choices=[]) from _typing_npc_video

    # Process reaction
    python:
        _npc_vid_response = _npc_video_reaction(npc, _sent_vid)
        phone_add_msg(npc.gid, npc.gid, _npc_vid_response)

        _vid_face_hidden = _sent_vid.get("face_hidden", True)
        _vid_is_partner = (_sent_vid.get("girl_gid", "") == npc.girl_gid)

        if not _vid_face_hidden and not _vid_is_partner:
            _gossip_girl = GIRL_BY_ID.get(_sent_vid.get("girl_gid", ""))
            if _gossip_girl and _gossip_girl.has_npc_partner():
                _gossip_pronoun = _tr("She") if getattr(npc, "gender", "male") == "female" else _tr("He")
                phone_add_msg(npc.gid, "system", _tl(_("%s'll probably tell others about this.")) % _gossip_pronoun, "system")

        npc_phone_chat_set_cooldown(npc)
        unlock_achievement("viral_video")
        debug_log("[NPC_VIDEO] Send complete: npc=%s vid_girl=%s face_hidden=%s is_partner=%s" % (
            npc.name, _sent_vid.get("girl_gid"), _vid_face_hidden, _vid_is_partner))

    return

# ============================================================
# NTR Creampie Confrontation
# NPC partner storms in after detecting creampie
# ============================================================
label _ntr_creampie_confrontation(girl):
    python:
        _npc_cream = get_npc_partner_for(girl)
        if _npc_cream is None:
            renpy.return_statement()
        _npc_name = _npc_cream.Name if hasattr(_npc_cream, "Name") else "partner"
        debug_log("[NTR_CREAMPIE] Confrontation START for %s, npc=%s" % (girl.gid, _npc_name))

    # NPC enters
    $ _show_witness_enter(_npc_cream)

    # NPC reacts to creampie
    python:
        _cream_npc_lines = [
            _("Did you just cum inside her?! Are you serious right now?!"),

            _("You came INSIDE her?! That was the ONE thing you weren't supposed to do!"),

            _("I can see it... you came inside her. What the hell is wrong with you?!"),

        ]
    $ Say_Line(_npc_cream, _tl(renpy.random.choice(_cream_npc_lines)))

    # Girl scared reaction
    $ set_scene_expression(girl, None, eyes="eyes_scared", brows="brows_sad", mouth="mouth_scared")
    python:
        _cream_girl_lines = [
            _("It's not what it looks like..."),

            _("I-I'm sorry, it just happened..."),

            _("Please, let me explain..."),

        ]
    $ Say_Line(girl, _tl(renpy.random.choice(_cream_girl_lines)))

    # NPC final outburst
    python:
        _cream_npc_final = [
            _("We had ONE rule! ONE! And you couldn't even follow THAT?!"),

            _("I trusted you with ONE boundary and you broke it!"),

            _("This is exactly what I was afraid of. You crossed the line!"),

        ]
    $ Say_Line(_npc_cream, _tl(renpy.random.choice(_cream_npc_final)))

    # Stat changes
    python:
        Change_NPC_Status(_npc_cream, "friendship_with_player", -200)
        _old_bar = getattr(_npc_cream, "_ntr_boundary_bar", 0)
        _npc_cream._ntr_boundary_bar = max(0, _old_bar - 50)
        girl._ntr_boundary_bar = _npc_cream._ntr_boundary_bar
        girl._ntr_violation_pending = True
        store._ntr_creampie_witnessed_gid = None   # consumed (the campus abort never runs session_cum_reset)
        debug_log("[NTR_CREAMPIE] Stats: friend -200, bar %d->%d, violation pending" % (_old_bar, _npc_cream._ntr_boundary_bar))

    # NPC exits
    $ _hide_witness_exit(_npc_cream)

    # Abort scene
    $ store._npc_witness_scene_aborted = True
    $ debug_log("[NTR_CREAMPIE] Confrontation END, scene aborted")

    return

# ============================================================
# NTR Angry-End Confrontation
# NPC partner reacts during angry-end when creampie boundary
# was violated. Girl is ALREADY furious at the player.
# Called from angry-end labels BEFORE force_scene_reset.
# ============================================================
label _angry_end_ntr_confrontation(girl):
    python:
        if not getattr(girl, '_ntr_violation_pending', False):
            renpy.return_statement()
        # He must have been on scene for the creampie. Absent: keep _ntr_violation_pending so
        # _ntr_process_violation_next_day delivers the fallout, but nobody walks in out of nowhere.
        if getattr(store, "_ntr_creampie_witnessed_gid", None) != girl.gid:
            debug_log("[NTR_ANGRY_END] %s: violation pending but partner was NOT on scene -> confrontation skipped, next-day fallout kept" % girl.gid)
            renpy.return_statement()
        _aend_npc = get_npc_partner_for(girl)
        if _aend_npc is None:
            renpy.return_statement()
        _aend_npc_name = _aend_npc.Name if hasattr(_aend_npc, "Name") else "partner"
        debug_log("[NTR_ANGRY_END] Confrontation START for %s, npc=%s" % (girl.gid, _aend_npc_name))

    $ store._witness_expression_lock = True

    # NPC enters
    $ _show_witness_enter(_aend_npc)

    # NPC reacts — protective, saw the forced act
    python:
        _aend_npc_lines = [
            _("What the FUCK did you just do to her?! She told you to stop!"),

            _("You came inside her when she said NO?! I saw everything!"),

            _("I was watching the whole time. You forced yourself on her. You're done."),

        ]
    $ Say_Line(_aend_npc, _tl(renpy.random.choice(_aend_npc_lines)))

    # Girl turns to partner — shame, fear, anger at player
    $ set_scene_expression(girl, None, eyes="eyes_scared", brows="brows_sad", mouth="mouth_scared")
    python:
        _aend_girl_lines = [
            _("%(Pp)s saw... %(pp)s saw everything... I didn't want this, I swear!"),

            _("I told him no! He didn't listen! Please, take me home..."),

            _("I tried to stop him... %(pl)s, please, just get me out of here..."),

        ]
        _aend_girl_line = _format_partner_line(girl, _tl(renpy.random.choice(_aend_girl_lines)))
    $ Say_Line(girl, _aend_girl_line)

    # NPC final — direct threat to player
    python:
        _aend_npc_final = [
            _("If I EVER see you near her again, you'll regret it."),

            _("Stay away from her. I mean it. Come near her again and I'll make sure you can't."),

            _("We're done. You, me, all of this. And if she ends up pregnant from this, I'm coming for you."),

        ]
    $ Say_Line(_aend_npc, _tl(renpy.random.choice(_aend_npc_final)))

    # Penalties — same weight as normal confrontation
    python:
        Change_NPC_Status(_aend_npc, "friendship_with_player", -200)
        _aend_old_bar = getattr(_aend_npc, "_ntr_boundary_bar", 0)
        _aend_npc._ntr_boundary_bar = max(0, _aend_old_bar - 50)
        girl._ntr_boundary_bar = _aend_npc._ntr_boundary_bar
        girl._ntr_violation_pending = False
        store._ntr_creampie_witnessed_gid = None
        debug_log("[NTR_ANGRY_END] Stats: friend -200, bar %d->%d, violation CLEARED (no next-day)" % (_aend_old_bar, _aend_npc._ntr_boundary_bar))

    $ store._witness_expression_lock = False

    # NPC exits
    $ _hide_witness_exit(_aend_npc)

    $ store._npc_witness_scene_aborted = True
    $ debug_log("[NTR_ANGRY_END] Confrontation END")

    return
