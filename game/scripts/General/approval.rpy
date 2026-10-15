init python:
    import random as _random

    # =====================================================
    # CENTRAL APPROVAL MAPPING
    # - category: safe | lewd | sex (future)
    # - "_default": fallback for all girls
    # - "<girl_id>": per-girl overrides
    # =====================================================
    APPROVAL_ACTION_RULES = {
        "safe": {
            "_default": {
                "joke": {"T": 120, "Type": "L", "Spread": 120, "Bonus": 40, "Variation": 20},
                "touch_cheek": {"T": 130, "Type": "LI", "Spread": 120, "Bonus": 0, "Variation": 25},
                "hug": {"T": 180, "Type": "LO", "Spread": 130, "Bonus": 0, "Variation": 30},
                "hold_hands": {"T": 220, "Type": "LI", "Spread": 140, "Bonus": 0, "Variation": 30},
                "kiss_cheek": {"T": 270, "Type": "LI", "Spread": 150, "Bonus": 0, "Variation": 35},
                "shoulder_massage": {"T": 300, "Type": "LOI", "Spread": 160, "Bonus": 0, "Variation": 35},
                "steal_kiss": {"T": 400, "Type": "LOI", "Spread": 170, "Bonus": 0, "Variation": 40},
                # --- Compliments: EASY (always accepted at start, score ~62+ vs T=30-40) ---
                "compliment_smile":        {"T": 30,  "Type": "L",  "Spread": 80, "Bonus": 40, "Variation": 10},
                "compliment_laugh":        {"T": 30,  "Type": "L",  "Spread": 80, "Bonus": 40, "Variation": 10},
                "compliment_hair_today":   {"T": 40,  "Type": "L",  "Spread": 80, "Bonus": 30, "Variation": 10},
                "compliment_outfit_style": {"T": 40,  "Type": "L",  "Spread": 80, "Bonus": 30, "Variation": 10},
                "compliment_fragrance":    {"T": 40,  "Type": "L",  "Spread": 80, "Bonus": 30, "Variation": 10},
                "compliment_class":        {"T": 40,  "Type": "LI", "Spread": 80, "Bonus": 30, "Variation": 10},
                "compliment_class_grades": {"T": 40,  "Type": "LI", "Spread": 80, "Bonus": 30, "Variation": 10},
                # --- Compliments: MEDIUM (needs a few chats first, Love ~70-100) ---
                "compliment_dr_skill":     {"T": 80,  "Type": "LO", "Spread": 100, "Bonus": 0, "Variation": 20},
                "compliment_gym_weights":  {"T": 80,  "Type": "LO", "Spread": 100, "Bonus": 0, "Variation": 20},
                "compliment_beauty_today": {"T": 100, "Type": "LI", "Spread": 110, "Bonus": 0, "Variation": 20},
                "compliment_gorgeous":     {"T": 110, "Type": "LI", "Spread": 110, "Bonus": 0, "Variation": 25},
                "compliment_confidence":   {"T": 90,  "Type": "LI", "Spread": 100, "Bonus": 0, "Variation": 20},
                "compliment_smart":        {"T": 90,  "Type": "LI", "Spread": 100, "Bonus": 0, "Variation": 20},
                # --- Compliments: HARD (bold, needs decent stats Love ~150+) ---
                "compliment_eyes":         {"T": 150, "Type": "LI", "Spread": 120, "Bonus": 0, "Variation": 30},
                "compliment_toned_body":   {"T": 140, "Type": "LOI","Spread": 120, "Bonus": 0, "Variation": 25},
                "compliment_so_into_you":  {"T": 180, "Type": "LI", "Spread": 130, "Bonus": 0, "Variation": 30},
            },
            # Personality (docs/plan_personality_mechanics.md): the compliments she distrusts are harder to accept
            # (dialogue_bank.rpy GIRL_COMPLIMENT_TASTE: they also pay less and sting more)
            "gwen": {
                "compliment_gorgeous":     {"T": 150},
                "compliment_beauty_today": {"T": 140},
            },
            "ntw": {
                "compliment_smile":        {"T": 70},
            },
        },
        "lewd": {
            "_default": {
                "slap_ass":   {"T":  950, "Type": "OI",  "Spread": 160, "Bonus": 0, "Variation": 60},
                "pinch_ass":  {"T":  900, "Type": "OI",  "Spread": 150, "Bonus": 0, "Variation": 50},
                "grab_tits":  {"T": 1000, "Type": "LOI", "Spread": 170, "Bonus": 0, "Variation": 70},
                "grab_ass":   {"T":  950, "Type": "LOI", "Spread": 160, "Bonus": 0, "Variation": 60},
                "ask_panties":{"T": 1050, "Type": "LI",  "Spread": 180, "Bonus": 0, "Variation": 70},
                # his unasked photo on her phone (phone_messaging _dp_process_dickpic): Love AND obedience, never
                # obedience alone (a flat Obed 200 switch let a girl at Love 0 enjoy it: tester 2026-10-11)
                "dick_pic":   {"T":  520, "Type": "LO",  "Spread": 150, "Bonus": 0, "Variation": 40},
                # his text ORDER to a submissive (player_phone_order.rpy): be in his room tonight
                "phone_order":{"T":  520, "Type": "LO",  "Spread": 150, "Bonus": 0, "Variation": 40},
            },
            "tenny": {
                "slap_ass":    {"T": 1100},
                "pinch_ass":   {"T": 1050},
                "grab_tits":   {"T": 1160},
                "grab_ass":    {"T": 1100},
                "ask_panties": {"T": 1220},
            },
        },

        # -------------------------------------------------------
        # SEX category — used by sexual scene approval gates.
        # T values are raw stat sums (Love+Obed+Inbt can reach 3000)
        # plus Lust×2.5 and Temptation×22 bonuses.
        # Starting stats (Love=100,Obed=15,Inbt=10,Lust=5,Temp=0)
        # give a base LI of ~122, LOI of ~137.
        # -------------------------------------------------------
        "sex": {
            "_default": {
                "kiss":       {"T": 380,  "Type": "LI",  "Spread": 120, "Bonus": 0, "Variation": 30},
                "masturbate": {"T": 500,  "Type": "LOI", "Spread": 130, "Bonus": 0, "Variation": 35},
                "oral":       {"T": 700,  "Type": "LOI", "Spread": 145, "Bonus": 0, "Variation": 45},
                "rub":        {"T": 950,  "Type": "LOI", "Spread": 160, "Bonus": 0, "Variation": 55},
                "hj":         {"T": 600,  "Type": "LOI", "Spread": 140, "Bonus": 0, "Variation": 40},
                "fj":         {"T": 720,  "Type": "LOI", "Spread": 148, "Bonus": 0, "Variation": 48},
                "tj":         {"T": 750,  "Type": "LOI", "Spread": 150, "Bonus": 0, "Variation": 50},
                "bj":         {"T": 900,  "Type": "LOI", "Spread": 160, "Bonus": 0, "Variation": 55},
                "tip":        {"T": 1000, "Type": "LOI", "Spread": 165, "Bonus": 0, "Variation": 55},
                "sex":        {"T": 1150, "Type": "LOI", "Spread": 170, "Bonus": 0, "Variation": 60},
                "anal":       {"T": 1350, "Type": "OI",  "Spread": 180, "Bonus": 0, "Variation": 70},
                # her tongue on him: the most "his" act there is (only girls with the pose: girl_has_pose "rimjob")
                "rj":         {"T": 1400, "Type": "OI",  "Spread": 180, "Bonus": 0, "Variation": 70},
                # --- Touch actions (used by sex_touch_menu) ---
                "touch_massage":  {"T": 300,  "Type": "LO",  "Spread": 130, "Bonus": 0, "Variation": 25},
                "touch_thighs":   {"T": 380,  "Type": "LI",  "Spread": 135, "Bonus": 0, "Variation": 30},
                "touch_ass":      {"T": 450,  "Type": "LOI", "Spread": 140, "Bonus": 0, "Variation": 35},
                "touch_tits":     {"T": 530,  "Type": "LOI", "Spread": 145, "Bonus": 0, "Variation": 40},
                "touch_pussy":    {"T": 620,  "Type": "LOI", "Spread": 150, "Bonus": 0, "Variation": 45},
                # --- Strip actions (exposure approval during scenes) ---
                "strip_minor":    {"T": 200,  "Type": "LI",  "Spread": 120, "Bonus": 0, "Variation": 25},
                "strip_top":      {"T": 350,  "Type": "LI",  "Spread": 130, "Bonus": 0, "Variation": 30},
                "strip_bottom":   {"T": 500,  "Type": "LOI", "Spread": 140, "Bonus": 0, "Variation": 35},
            },
            "tenny": {
                "kiss":         {"T": 450},
                "masturbate":   {"T": 580},
                "oral":         {"T": 810},
                "rub":          {"T": 1100},
                "hj":           {"T": 700},
                "fj":           {"T": 840},
                "tj":           {"T": 870},
                "bj":           {"T": 1050},
                "tip":          {"T": 1200},
                "sex":          {"T": 1340},
                "anal":         {"T": 1570},
                "touch_thighs": {"T": 440},
                "touch_ass":    {"T": 520},
                "touch_tits":   {"T": 615},
                "touch_pussy":  {"T": 720},
                "strip_top":    {"T": 410},
                "strip_bottom": {"T": 580},
            },
        },
    }

    # Per-girl places. {"set": x} REPLACES the weight of the place (public / semi-public / private); {"mult": x}
    # multiplies it: how at ease she is there (personality, docs/plan_personality_mechanics.md), so her traits still
    # count. A place missing here = the normal rule.
    GIRL_LOCATION_MULTS = {
        "tenny": {
            "classroom":  {"set": 0.35},
            "tenny_room": {"set": 1.20},
        },
        "gwen": {
            "gwen_room":  {"mult": 1.15},     # her own space
        },
        "ntw": {
            "gym":        {"mult": 1.15},     # where she trains
        },
        "rogue": {
            "pool":       {"mult": 1.15},     # outdoors
            "campus":     {"mult": 1.10},
        },
    }

    # Who is in control of a sex act: "her" (she leads, she decides) or "him". An act missing here is neutral.
    # The position is not here: "sex" is the act, the position is picked after it.
    ACT_CONTROL = {
        "hj":   "her",
        "fj":   "her",
        "oral": "her",   # him going down on her
        "bj":   "him",
        "anal": "him",
        "rj":   "him",
    }
    # Who is in control of a position (docs/plan_femdom.md): she rides him in cowgirl / reverse cowgirl, he takes her in
    # the others. Read by the femdom orders (Actions/femdom.rpy): she takes over from "his", sets the pace in "hers",
    # and may refuse to go from hers to his.
    POSITION_CONTROL = {
        "cowgirl": "her", "reverse_cowgirl": "her", "reverse_cowgirl_anal": "her",
        "doggy": "him", "anal": "him", "full_nelson": "him", "full_nelson_anal": "him",
        "laying_down": "him", "laying_anal": "him",
    }

    def scene_control(scene_type):
        """"her" / "him" / None for a scene type: its position (POSITION_CONTROL), else its act (ACT_CONTROL)."""
        return POSITION_CONTROL.get(scene_type) or ACT_CONTROL.get(scene_type)

    # Who is in control of an ORDER outside the sex acts (lewd / safe categories): the same Control bonus applies
    # (docs/plan_submissive_pass.md S2: a submissive takes his orders sooner, a femdom later). Add a key here when its
    # check goes through ApprovalRuleFor; a key missing here is neutral.
    ORDER_CONTROL = {
        "dick_pic": "him",
        "phone_order": "him",
        # his strip commands (sex category, docs/plan_submissive_pass.md S2): his orders
        "strip_minor": "him",
        "strip_top": "him",
        "strip_bottom": "him",
    }
    # How her Control trait (characters_stats.rpy TRAIT_PAIRS "Control") READS her stats in every approval check:
    # a WEIGHT on Love and Obed, never a harder or easier bar (the old flat Bonus made a femdom "less horny" and a
    # submissive "generically slutty": tester 2026-10-11, the author's ruling). A femdom gives what she gives out of
    # love, obedience barely enters it; a submissive gives what she is told, love matters less. The side of the act
    # ("him" = he is in control, "her" = she leads; ACT_CONTROL / ORDER_CONTROL) sets how far the weights move;
    # "any" is every check with no side. The pairs are sum-neutral: a girl with even stats sees the same total.
    TRAIT_STAT_WEIGHTS = {
        "femdom":     {"him": {"L": 1.30, "O": 0.70}, "her": {"L": 1.10, "O": 0.90}, "any": {"L": 1.15, "O": 0.85}},
        "submissive": {"him": {"L": 0.70, "O": 1.30}, "her": {"L": 0.90, "O": 1.10}, "any": {"L": 0.85, "O": 1.15}},
    }

    def trait_stat_weights(girl, action=None):
        """The {"L": x, "O": y} weights of her Control trait for this action (its side from ACT_CONTROL /
        ORDER_CONTROL, else "any"), or None for a girl without one. A canon femdom on her turn minds his control
        less at every stage (femdom_turn.rpy): the "him" shift fades with FEMDOM_TURN_HIS_PENALTY."""
        if not hasattr(girl, "has_trait"):
            return None
        _side = ACT_CONTROL.get(str(action)) or ORDER_CONTROL.get(str(action)) or "any"
        for _tid, _by_side in TRAIT_STAT_WEIGHTS.items():
            if girl.has_trait(_tid):
                _w = dict(_by_side.get(_side) or _by_side["any"])
                if _tid == "femdom" and _side == "him":
                    _f = FEMDOM_TURN_HIS_PENALTY[femdom_stage(girl)]
                    _w = {_k: 1.0 + (_v - 1.0) * _f for _k, _v in _w.items()}
                return _w
        return None

    def ApprovalRuleFor(girl=None, action=None, category="safe"):
        """
        Return merged approval config for a specific (girl, action, category).
        Merge order: hardcoded default -> category default action -> girl override action,
        then (sex acts) her Control trait moves the Bonus (ACT_CONTROL / TRAIT_CONTROL_BONUS).
        """
        cfg = {"T": 380, "Type": "LI", "Spread": 140, "Bonus": 0, "Variation": 30}

        category_block = APPROVAL_ACTION_RULES.get(str(category), {})
        default_block = category_block.get("_default", {})
        action_key = str(action) if action is not None else ""

        if action_key in default_block:
            cfg.update(default_block[action_key])

        gid = None
        if girl is not None:
            gid = getattr(girl, "Id", None) or getattr(girl, "gid", None)
        if gid:
            girl_block = category_block.get(str(gid).lower(), {})
            if action_key in girl_block:
                cfg.update(girl_block[action_key])

        # her Control trait weighs her stats (TRAIT_STAT_WEIGHTS); a caller that unpacks the keys by hand still gets
        # it: ApprovalCheck recomputes from its Action when Weights is not passed
        _w = trait_stat_weights(girl, action_key)
        if _w:
            cfg["Weights"] = _w
            print("[APPROVAL] control: %s %s -> weights %s" % (gid, action_key, _w))

        return cfg

    def _count_location_occupants(girl):
        """Count other people at the player's location (excluding girl and player)."""
        count = 0
        _roster = getattr(store, "_location_roster", None)
        _loc = store.CurrentLocation
        _party = getattr(store, "Party", [])

        if _roster is not None:
            for entity in _roster.get("near", []):
                if entity is girl or entity in _party:
                    continue
                if isinstance(entity, Girl):
                    count += 1
                    if callable(globals().get("get_npc_partner_for")) and entity.has_npc_partner():
                        _enpc = get_npc_partner_for(entity)
                        if _enpc and getattr(_enpc, "loc", None) == _loc:
                            count += 1
        else:
            for g in getattr(store, "ALL_GIRLS", []):
                if g is girl or g in _party:
                    continue
                if getattr(g, "loc", None) == _loc:
                    count += 1

        if callable(globals().get("get_npc_partner_for")) and hasattr(girl, "has_npc_partner") and girl.has_npc_partner():
            _gnpc = get_npc_partner_for(girl)
            if _gnpc and getattr(_gnpc, "loc", None) == _loc:
                count += 1

        return count

    def ApprovalCheck(
        girl=None,
        T=1000,
        Type="LOI",
        Spread=150,
        Bonus=0,
        Variation=0,
        Check=False,
        ReturnData=False,
        Action=None,
        Location=None,
        IsCheating=None,
        PlayerDating=False,
        GirlDating=None,
        Remote=False,
        Weights=None
    ):
        """
        Unified approval engine.
        Remote=True: she answers on her phone, away from him (a photo, a text): the people around HIM do not count.
        Weights: {"L": x, "O": y, "I": z} multipliers on her stat pool (her Control trait, trait_stat_weights);
        None = read from her traits and the Action here.
        - Check=True returns only raw numeric score (legacy behavior).
        - ReturnData=True returns a rich dict with outcome/reasons.
        - Otherwise returns legacy tier 0..4.
        """

        def _default_result():
            return {
                "score": 0,
                "tier": 0,
                "accepted": False,
                "outcome": "hard_deny",
                "reason_primary": "no_girl",
                "reason_secondary": None,
                "reasons": ["no_girl"],
                "is_cheating": False,
                "cheating_state": "none",
                "debug": {},
            }

        if not girl:
            if Check:
                return 0
            if ReturnData:
                return _default_result()
            return 0

        # Read core stats
        L = getattr(girl, "Love", 0)
        O = getattr(girl, "Obed", 0)
        I = getattr(girl, "Inbt", 0)
        Lust = getattr(girl, "Lust", 0)
        Temptation = getattr(girl, "Temptation", 0)

        t = (Type or "LOI").upper()

        # Base stat pool by type
        love_part = 0
        obed_part = 0
        inbt_part = 0
        if t == "LOI":
            love_part = L
            obed_part = O
            inbt_part = I
        elif t == "L":
            love_part = L
        elif t == "O":
            obed_part = O
        elif t == "I":
            inbt_part = I
        elif t == "LO":
            love_part = L
            obed_part = O
        elif t == "LI":
            love_part = L
            inbt_part = I
        elif t == "OI":
            obed_part = O
            inbt_part = I
        else:
            love_part = L
            obed_part = O
            inbt_part = I

        _w = Weights if Weights is not None else trait_stat_weights(girl, Action)
        if _w:
            love_part = int(love_part * _w.get("L", 1.0))
            obed_part = int(obed_part * _w.get("O", 1.0))
            inbt_part = int(inbt_part * _w.get("I", 1.0))
        base_value = love_part + obed_part + inbt_part

        # Temporary state pressure
        lust_part = int(Lust * 2.5)
        temptation_part = int(Temptation * 22)

        value = base_value + lust_part + temptation_part + int(Bonus)

        # Dating player bonus — girlfriend is much more willing
        if hasattr(girl, "is_dating_player") and girl.is_dating_player():
            value += 300

        # Date afterglow — temporary approval boost from a good date
        if hasattr(girl, "has_temp_status") and girl.has_temp_status("date_afterglow"):
            _glow = getattr(girl, "_date_afterglow", 0)
            value += {0: 0, 1: 30, 2: 60}.get(_glow, 0)

        # Drunk — temporary approval boost while intoxicated (event-only,
        # since drunkenness is only raised inside events)
        if callable(globals().get("drunk_approval_bonus")):
            value += drunk_approval_bonus(girl)

        # Optional randomness
        variation_roll = 0
        if Variation > 0:
            variation_roll = _random.randint(-Variation, Variation)
            value += variation_roll

        # Relationship state
        if GirlDating is None:
            girl_has_partner = False
            if hasattr(girl, "has_npc_partner") and girl.has_npc_partner():
                girl_has_partner = True
            if hasattr(girl, "has_girl_partner") and girl.has_girl_partner():
                girl_has_partner = True
            GirlDating = girl_has_partner
        else:
            GirlDating = bool(GirlDating)

        # Auto-detect if player is dating someone else
        # Skip if she IS the player's GF — she's not "the other woman" in a poly setup
        if not PlayerDating:
            if not (hasattr(girl, "is_dating_player") and girl.is_dating_player()):
                _p_gf = get_player_girlfriend(store.ALL_GIRLS) if hasattr(store, "ALL_GIRLS") else None
                if _p_gf is not None and _p_gf != girl:
                    if not is_player_harem_exempt(girl):
                        PlayerDating = True

        if IsCheating is None:
            is_cheating = bool(PlayerDating) or bool(GirlDating)
        else:
            is_cheating = bool(IsCheating)

        # Location class
        loc = Location if Location is not None else getattr(girl, "loc", None)
        loc_kind = "private"
        if loc in ("classroom", "campus", "party", "gym", "street", "mall"):
            loc_kind = "public"
        elif loc in ("pool", "showers", "shower", "restaurant_restroom"):
            loc_kind = "semi_public"

        # Traits
        traits = set()
        if hasattr(girl, "traits") and girl.traits:
            traits = set([str(x).lower() for x in girl.traits])

        def has_trait(name):
            return str(name).lower() in traits

        context_mult = 1.0
        _has_public_trait = has_trait("public_fetish") or has_trait("exhibitionist")
        if loc_kind == "public":
            if _has_public_trait:
                context_mult *= 0.92  # minor penalty, she likes it
            else:
                context_mult *= 0.55  # heavy penalty, she's uncomfortable
        elif loc_kind == "semi_public":
            if _has_public_trait:
                context_mult *= 0.96
            else:
                context_mult *= 0.72

        _girl_gid = getattr(girl, "gid", None) or getattr(girl, "Id", None)
        if _girl_gid:
            _girl_loc = GIRL_LOCATION_MULTS.get(str(_girl_gid).lower(), {}).get(loc, None)
            if _girl_loc is not None:
                _was = context_mult
                context_mult = _girl_loc["set"] if "set" in _girl_loc else context_mult * _girl_loc["mult"]
                print("[APPROVAL] Per-girl place: %s at %s -> context_mult=%.2f (was %.2f, %s)" % (_girl_gid, loc, context_mult, _was, _girl_loc))

        trait_mult = 1.0
        if has_trait("lesbian") and loc_kind != "private":
            trait_mult *= 0.30
            if _has_public_trait:
                trait_mult = max(trait_mult, 0.55)
        if has_trait("shy") and loc_kind != "private":
            trait_mult *= 0.78
        if has_trait("exhibitionist") and loc_kind != "private":
            trait_mult *= 1.15  # enjoys it but doesn't fully cancel
        if has_trait("public_fetish") and loc_kind != "private":
            trait_mult *= 1.20  # gets excited, nearly cancels penalty
        # public_shy: extra penalty in public, gains Obed when pushed
        if has_trait("public_shy") and loc_kind != "private":
            trait_mult *= 0.60

        # First-time public act penalty (stacks with public penalty)
        if loc_kind != "private" and not _has_public_trait:
            _intimacy = getattr(girl, "intimacy_flags", set()) or set()
            _int_key = str(Action) if Action else ""
            # Any position means "sex": the first-time-in-public check must read the act flag
            _int_key = "sex" if _int_key == "riding" else scene_type_act(_int_key)
            if _int_key and _int_key not in _intimacy:
                context_mult *= 0.55  # 45% extra penalty for first-time public act

        # Room occupancy penalty: other people present reduce approval
        _door_locked = getattr(store, "door_locked", False)
        if not _door_locked and not Remote:
            _occ = _count_location_occupants(girl)
            if _occ > 0:
                if _has_public_trait:
                    pass
                elif has_trait("shy") or has_trait("public_shy"):
                    context_mult *= max(0.35, 1.0 - _occ * 0.24)
                elif has_trait("exhibitionist"):
                    context_mult *= max(0.55, 1.0 - _occ * 0.06)
                else:
                    context_mult *= max(0.55, 1.0 - _occ * 0.12)
                print("[APPROVAL] occupancy: %d others, door_locked=%s, context_mult=%.3f" % (_occ, _door_locked, context_mult))

        # BF loyalty modifier: only applies when the GIRL has her own partner
        if GirlDating and hasattr(girl, "bf_loyalty"):
            _bfl = int(getattr(girl, "bf_loyalty", 750))
            if _bfl >= 750:
                trait_mult *= 0.70   # loves BF — very resistant
            elif _bfl >= 500:
                trait_mult *= 0.85   # likes BF — moderate resistance
            elif _bfl >= 250:
                trait_mult *= 1.0    # strained — neutral
            else:
                trait_mult *= 1.15   # miserable — easier to seduce

        # Cheating profile
        cheating_state = "none"
        if is_cheating:
            player_cheat_count = int(getattr(girl, "PlayerCheatCount", 0))
            girl_cheat_count = int(getattr(girl, "GirlCheatCount", 0))
            total_cheat_count = player_cheat_count + girl_cheat_count

            loves_cheating = (
                has_trait("cheater") or
                int(getattr(girl, "CheatAttitude", 3)) >= 6
            )
            if loves_cheating:
                cheating_state = "love_cheating"
                trait_mult *= 1.35
            elif total_cheat_count == 0:
                cheating_state = "first_cheating"
            else:
                cheating_state = "recurring_cheating"

            if has_trait("loyal") and cheating_state != "love_cheating":
                trait_mult *= 0.60

            # Friendship with player's GF penalty (skip if harem-exempt)
            # Higher friendship = harder to accept cheating
            if not loves_cheating and not is_player_harem_exempt(girl):
                _pgf = get_player_girlfriend(getattr(store, "ALL_GIRLS", [])) if hasattr(store, "ALL_GIRLS") else None
                if _pgf and _pgf != girl and hasattr(girl, "get_like_for"):
                    _fship = girl.get_like_for(_pgf.gid)
                    if _fship >= 800:
                        trait_mult *= 0.55   # best friends -- huge penalty
                    elif _fship >= 500:
                        trait_mult *= 0.75   # friends -- significant penalty
                    elif _fship >= 250:
                        trait_mult *= 0.90   # acquaintances -- small penalty

            # Partner physically present at the same location
            _npc_here = False
            if callable(globals().get("get_npc_partner_for")):
                _ap_npc = get_npc_partner_for(girl)
                if _ap_npc and getattr(_ap_npc, "loc", None) == loc:
                    _ntr_bypass = (getattr(_ap_npc, "_ntr_active", False)
                                   and getattr(girl, "_ntr_boundary_discovered", False))
                    if not _ntr_bypass:
                        _npc_here = True
                        if loves_cheating:
                            trait_mult *= 0.65
                        elif has_trait("loyal"):
                            trait_mult *= 0.25
                        else:
                            trait_mult *= 0.40
                        print("[APPROVAL] partner_present: npc=%s loc=%s mult applied" % (_ap_npc.name, loc))

        # Reconciled ex: harder to approve until trust builds
        _etm = getattr(girl, "_ex_trust_max", 0)
        if _etm > 0:
            _ext = getattr(girl, "_ex_trust", 0)
            _rc = EX_RECON_CONFIG
            if getattr(girl, "_cheating_ex_reconciled", False):
                if _ext < _etm // 2:
                    trait_mult *= _rc["trust_mult_high"]
                elif _ext < _etm:
                    trait_mult *= _rc["trust_mult_low"]
            else:
                if _ext < _etm:
                    trait_mult *= _rc["trust_mult_low"]

        if Action == "oral":
            if has_trait("bisexual"):
                trait_mult *= 1.25
            if has_trait("cute_sex"):
                trait_mult *= 1.15

        _value_before_mult = value
        value = int(value * context_mult * trait_mult)

        _tag = "[APPROVAL_ANAL]" if Action == "anal" else "[APPROVAL]"
        if Action == "anal" or ReturnData:
            debug_log("%s base_value=%s (L=%s O=%s I=%s type=%s)" % (_tag, base_value, love_part, obed_part, inbt_part, t))
            debug_log("%s lust_part=%s tempt_part=%s bonus=%s dating=%s variation=%s" % (_tag, lust_part, temptation_part, int(Bonus), 300 if (hasattr(girl, "is_dating_player") and girl.is_dating_player()) else 0, variation_roll))
            debug_log("%s value_before_mult=%s context_mult=%.3f trait_mult=%.3f value_after=%s" % (_tag, _value_before_mult, context_mult, trait_mult, value))
            debug_log("%s T=%s Spread=%s margin=%s need_margin=%s" % (_tag, int(T), int(Spread), value - int(T), int(Spread * 0.30)))
            debug_log("%s is_cheating=%s cheating_state=%s GirlDating=%s PlayerDating=%s loc_kind=%s loc=%s" % (_tag, is_cheating, cheating_state, GirlDating, PlayerDating, loc_kind, loc))
            debug_log("%s traits=%s" % (_tag, traits))

        # Legacy raw score request
        if Check:
            return value

        margin = value - int(T)

        high_lust = Lust >= 65
        high_tempt = Temptation >= 6
        tempted = high_lust or high_tempt

        # Angry deny: moral block in cheating context.
        angry_moral_block = (
            is_cheating and
            has_trait("loyal") and
            cheating_state != "love_cheating" and
            Temptation < 7 and Lust < 75
        )

        if angry_moral_block:
            outcome = "angry_deny"
        elif margin < -int(Spread):
            outcome = "hard_deny"
        elif margin < 0:
            outcome = "tempted_deny" if tempted else "soft_deny"
        elif margin < int(Spread * 0.30):
            outcome = "neutral"
        elif margin < int(Spread):
            outcome = "tempted_allow" if tempted else "soft_allow"
        else:
            outcome = "hard_allow"

        accepted = outcome in ("tempted_allow", "soft_allow", "hard_allow")

        # Legacy tier mapping 0..4
        if outcome in ("angry_deny", "hard_deny"):
            tier = 0
        elif outcome in ("soft_deny", "tempted_deny"):
            tier = 1
        elif outcome == "neutral":
            tier = 2
        elif outcome == "tempted_allow":
            tier = 2
        elif outcome == "soft_allow":
            tier = 3
        else:
            tier = 4

        # Reason tracing
        reason_weights = {
            "love": love_part,
            "obed": obed_part,
            "inbt": inbt_part,
            "lust": lust_part,
            "temptation": temptation_part,
        }
        ranked = sorted(reason_weights.items(), key=lambda kv: kv[1], reverse=True)
        reason_primary = ranked[0][0] if ranked else "love"
        reason_secondary = ranked[1][0] if len(ranked) > 1 else None

        reasons = [reason_primary]
        if reason_secondary and reason_secondary != reason_primary:
            reasons.append(reason_secondary)
        if is_cheating:
            reasons.append("cheating")
            if cheating_state == "first_cheating":
                reasons.append("first_cheating")
            elif cheating_state == "love_cheating":
                reasons.append("love_cheating")
        if loc_kind == "public":
            reasons.append("public_pressure")
        elif loc_kind == "semi_public":
            reasons.append("semi_public_pressure")

        # Trait-driven primary reason override for explicit cheating profile
        if is_cheating and cheating_state == "love_cheating":
            reason_primary = "love_cheating"
        elif outcome == "tempted_allow":
            if temptation_part >= lust_part:
                reason_primary = "temptation"
            else:
                reason_primary = "lust"
        elif outcome == "tempted_deny":
            reason_primary = "temptation"

        result = {
            "score": value,
            "tier": tier,
            "accepted": accepted,
            "outcome": outcome,
            "reason_primary": reason_primary,
            "reason_secondary": reason_secondary,
            "reasons": reasons,
            "is_cheating": is_cheating,
            "cheating_state": cheating_state,
            "debug": {
                "love_part": love_part,
                "obed_part": obed_part,
                "inbt_part": inbt_part,
                "lust_part": lust_part,
                "temptation_part": temptation_part,
                "bonus": int(Bonus),
                "variation_roll": variation_roll,
                "context_mult": context_mult,
                "trait_mult": trait_mult,
                "location_kind": loc_kind,
                "margin": margin,
            },
        }

        # Keep last decision attached to the girl for dialogue layering.
        setattr(girl, "LastApprovalResult", result)

        if ReturnData:
            return result

        return tier
