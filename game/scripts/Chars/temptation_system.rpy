# ============================================================
# temptation_system.rpy
# Provocation (0–10), action gates, multipliers, cheating types,
# per-girl cheat counters, traits loyal/cheater, girl-girl history.
# ============================================================

init -998 python:
    # ------------------------------
    # Locations
    # ------------------------------
    PRIVATE_LOCATIONS = set(["room", "bedroom", "home", "private"])

    # ------------------------------
    # Cheating tags taxonomy (event tags)
    # ------------------------------
    CHEAT_TAGS = {
        "player_cheats_on_girl": "player_cheats_on_girl",   # player has gf and acts with a different girl
        "girl_cheats_on_npc":    "girl_cheats_on_npc",      # girl has npc partner and acts outside
        "girl_cheats_on_girl":   "girl_cheats_on_girl",     # girl has girl partner and acts outside
        "witnessed_cheating":    "witnessed_cheating",
    }

    # ------------------------------
    # Action rules
    # ------------------------------
    # min_stat    : weighted score floor  (Love×0.45 + Obed×0.25 + Inbt×0.30, max 1000)
    # min_temptation: Temptation (0–10) floor
    # temptation_gain: added to girl's Temptation after the act
    # temptation_cost: subtracted from girl's Temptation after the act
    ACTION_RULES = {
        "flirt": {"min_stat": 0, "min_temptation": 0, "temptation_gain": 1, "temptation_cost": 0},
        "kiss":  {"min_stat": 0, "min_temptation": 0, "temptation_gain": 1, "temptation_cost": 1},  # real: min_stat=300, min_temptation=2
        "touch": {"min_stat": 0, "min_temptation": 0, "temptation_gain": 1, "temptation_cost": 1},  # real: min_stat=400, min_temptation=3
        "hj":    {"min_stat": 0, "min_temptation": 0, "temptation_gain": 1, "temptation_cost": 1},  # real: min_stat=460, min_temptation=4
        "tj":    {"min_stat": 0, "min_temptation": 0, "temptation_gain": 0, "temptation_cost": 2},  # real: min_stat=520, min_temptation=4
        "bj":    {"min_stat": 0, "min_temptation": 0, "temptation_gain": 0, "temptation_cost": 2},  # real: min_stat=580, min_temptation=5
        "tip":   {"min_stat": 0, "min_temptation": 0, "temptation_gain": 1, "temptation_cost": 2},
        "sex":   {"min_stat": 0, "min_temptation": 0, "temptation_gain": 0, "temptation_cost": 3},  # real: min_stat=700, min_temptation=7
        "anal":  {"min_stat": 0, "min_temptation": 0, "temptation_gain": 0, "temptation_cost": 3},  # real: min_stat=850, min_temptation=9
    }

    # ------------------------------
    # Score model
    # ------------------------------
    def get_action_score(girl, action):
        if girl is None:
            return 0

        score = int(girl.Love * 0.45) + int(girl.Obed * 0.25) + int(girl.Inbt * 0.30)

        if hasattr(girl, "has_trait"):
            if girl.has_trait("voyeur") and action in ("kiss", "touch"):
                score += 40
            if girl.has_trait("exhibitionist") and action in ("kiss", "touch"):
                score += 40
            if girl.has_trait("camera_hater") and action in ("kiss", "touch", "hj", "tj", "bj", "sex", "anal"):
                score -= 60
            if girl.has_trait("camera_lover") and action in ("kiss", "touch"):
                score += 30

            # Loyal/cheater minor score nudge (main effect is multiplier)
            if girl.has_trait("loyal") and action in ("kiss", "touch", "hj", "tj", "bj", "sex", "anal"):
                score -= 40
            if girl.has_trait("cheater") and action in ("kiss", "touch", "hj", "tj", "bj", "sex", "anal"):
                score += 60

            if girl.has_trait("anal_lover") and action == "anal":
                score += 40
            if girl.has_trait("anal_hater") and action == "anal":
                score -= 60

        if score < 0:
            score = 0
        if score > 1000:
            score = 1000
        return score

    # ------------------------------
    # Context helpers
    # ------------------------------
    def _is_private(location):
        return (location in PRIVATE_LOCATIONS)

    def _partner_key_for_girl(girl):
        """
        Returns:
        - "npc:<id>" if npc partner exists
        - "girl:<id>" if girl partner exists
        - None
        """
        if girl is None:
            return None
        if hasattr(girl, "has_npc_partner") and girl.has_npc_partner():
            return "npc:%s" % str(girl.npc_partner_id)
        if hasattr(girl, "has_girl_partner") and girl.has_girl_partner():
            return "girl:%s" % str(girl.girl_partner_id)
        return None

    # ------------------------------
    # Cheating action tiers (severity)
    # Tier 1: light (kiss/touch/flirt)
    # Tier 2: medium (hj/tj/masturbate)
    # Tier 3: medium-heavy (bj)
    # Tier 4: heavy (sex/anal)
    # ------------------------------
    def _cheat_action_tier(action):
        a = str(action)
        if a in ("kiss", "touch", "flirt", "kiss_cheek", "steal_kiss",
                  "hold_hands", "hug", "shoulder_massage"):
            return 1
        if a in ("hj", "tj", "masturbate", "oral", "grab_tits", "grab_ass",
                  "slap_ass", "pinch_ass", "touch_cheek"):
            return 2
        if a in ("bj",):
            return 3
        if a in ("sex", "anal"):
            return 4
        return 1

    # ------------------------------
    # Cheating attitude gating (1..6)
    # Tier-aware: actions above girl's CheatMaxTier get reduced attitude.
    # ------------------------------
    def get_effective_cheat_attitude(girl, action=None):
        """
        Trait cheater forces 6. Trait loyal pushes low.
        Otherwise use girl.CheatAttitude, reduced if the action tier
        is above what she has done before (CheatMaxTier).
        """
        if girl is None:
            return 2
        if hasattr(girl, "has_trait"):
            if girl.has_trait("cheater"):
                return 6
            if girl.has_trait("loyal"):
                return min(int(getattr(girl, "CheatAttitude", 2)), 2)
        base = int(getattr(girl, "CheatAttitude", 3))

        # Tier-aware reduction: heavier acts she hasn't done yet get lower effective attitude
        if action is not None:
            action_tier = _cheat_action_tier(action)
            max_tier = int(getattr(girl, "CheatMaxTier", 0))
            tier_gap = action_tier - max_tier
            if tier_gap > 0:
                base = max(1, base - tier_gap)

        return base

    def is_cheat_refusal_angry(girl):
        # hate_cheat => angry; soft_no_cheat => not angry
        att = get_effective_cheat_attitude(girl)
        return (att == 1)

    def is_cheat_hard_block(girl):
        # hate_cheat blocks cheating always; soft_no_cheat blocks but not angry
        att = get_effective_cheat_attitude(girl)
        return (att in (1, 2))

    # ------------------------------
    # Multipliers (difficulty)
    # Higher = harder.
    # Includes:
    # - public penalty
    # - partner penalty
    # - player has gf penalty
    # - loyal/cheater
    # - per-girl cheating counters (makes it easier with THIS girl only)
    # ------------------------------
    def get_action_multiplier(girl, action, location=None, player_has_gf=False, player_gf_id=None):
        mult = 1.0
        loc = location if location is not None else getattr(girl, "loc", None)

        # Public spaces are harder
        if _is_public_location(loc):
            mult *= 2.0

        # Partner penalties (if she has a partner and is crossing lines)
        cheating_context_for_her = False
        partner_key = _partner_key_for_girl(girl)
        if partner_key and action in ("kiss", "touch", "hj", "tj", "bj", "sex", "anal"):
            cheating_context_for_her = True
            mult *= 1.8  # baseline for "she has someone"

        # Player mono cheating pressure
        cheating_context_for_player = False
        if player_has_gf and action in ("kiss", "touch", "hj", "tj", "bj", "sex", "anal"):
            cheating_context_for_player = True
            mult *= 1.5

        # Trait loyal/cheater: only really matters in cheating contexts
        if hasattr(girl, "has_trait"):
            if girl.has_trait("loyal") and (cheating_context_for_player or cheating_context_for_her):
                mult *= 2.5
            if girl.has_trait("cheater") and (cheating_context_for_player or cheating_context_for_her):
                mult *= 0.55

        # Per-girl cheat counters make future cheating easier WITH THIS GIRL ONLY
        # Player cheating with this girl (keyed by victim gf id for stats, but effect applies to this girl).
        if cheating_context_for_player and hasattr(girl, "PlayerCheatCount"):
            c = int(getattr(girl, "PlayerCheatCount", 0))
            # each cheat reduces difficulty a bit, capped
            mult *= max(0.70, 1.0 - (0.06 * c))

        # Girl cheating on her partner with this girl/player
        if cheating_context_for_her and hasattr(girl, "GirlCheatCount"):
            c2 = int(getattr(girl, "GirlCheatCount", 0))
            mult *= max(0.72, 1.0 - (0.05 * c2))

        # Attitude: higher attitude makes cheating easier (but doesn’t affect non-cheating actions)
        att = get_effective_cheat_attitude(girl, action=action)
        if (cheating_context_for_player or cheating_context_for_her) and action in ("kiss", "touch", "hj", "tj", "bj", "sex", "anal"):
            if att == 3:
                mult *= 1.0
            elif att == 4:
                mult *= 0.92
            elif att == 5:
                mult *= 0.84
            elif att == 6:
                mult *= 0.75
            elif att == 2:
                mult *= 1.35
            elif att == 1:
                mult *= 2.0

        # Clamp
        if mult < 0.45:
            mult = 0.45
        if mult > 6.0:
            mult = 6.0
        return mult

    # NTR boundary: minimum level needed for each act (pre-approval)
    _NTR_ACT_MIN_LEVEL = {
        "kiss": 1, "rub": 1, "touch": 1, "masturbate": 1,
        "hj": 1, "bj": 1, "tj": 1, "oral": 1,
        "tip": 2, "sex": 2,
        "anal": 4,
    }
    _NTR_EXCEED_GATES = {
        "sex": 9,
        "anal": 10,
    }

    # ------------------------------
    # Loyalty / temptation blocking
    # Progressive fall into temptation, PLUS attitude blocks.
    # ------------------------------
    def is_loyalty_blocked(girl, action, player_has_gf=False):
        """
        Returns (blocked: bool, reason: str)
        """
        if girl is None:
            return True, "no_girl"
        # her step locks it (story_steps.rpy): refused whatever her stats, before anything else
        if story_act_locked(girl, action):
            return True, "story_locked"
        if hasattr(girl, "has_trait") and girl.has_trait("lesbian"):
            return False, None

        t = int(getattr(girl, "Temptation", 0))
        att = get_effective_cheat_attitude(girl, action=action)

        # Determine if this action would be cheating for player or for her.
        her_partner = _partner_key_for_girl(girl)
        cheating_for_her = bool(her_partner) and action in ("kiss", "touch", "masturbate", "oral", "rub", "hj", "tj", "bj", "rj", "sex", "anal")
        cheating_for_player = bool(player_has_gf) and action in ("kiss", "touch", "masturbate", "oral", "rub", "hj", "tj", "bj", "rj", "sex", "anal")
        if cheating_for_player and is_player_harem_exempt(girl):
            cheating_for_player = False
        is_any_cheat = cheating_for_her or cheating_for_player

        # Drunk lowers her guard: adds to effective temptation for the cheat
        # path (event-only). Opens a temporary window she'd resist while sober.
        if is_any_cheat and callable(globals().get("drunk_cheat_bonus")):
            t += drunk_cheat_bonus(girl)

        # Cheat heat: contributes to effective temptation for cheat path girls
        if cheating_for_her and callable(_is_on_cheat_path) and _is_on_cheat_path(girl):
            _eff_heat = _cheat_effective_heat(girl) if callable(_cheat_effective_heat) else getattr(girl, "_cheat_heat", 0)
            t += int(_eff_heat // 10)

            # Bypass: if she's already done a cheating act at this tier or higher, skip loyalty check
            _act_tier = _cheat_action_tier(action) if callable(_cheat_action_tier) else 0
            if _act_tier > 0 and getattr(girl, "CheatMaxTier", 0) >= _act_tier:
                return False, "ok"

        # Attitude gate (no longer permanent — high temptation can overcome)
        if is_any_cheat and att == 1 and t < 5:
            return True, "hate_cheat"
        if is_any_cheat and att == 2 and t < 4:
            return True, "soft_no_cheat"

        # Cheater bypasses most loyalty blocks
        if hasattr(girl, "has_trait") and girl.has_trait("cheater"):
            # still keep virgin gate below
            pass
        else:
            # If she has partner, require higher temptation to cross lines
            if cheating_for_her:
                _ntr_npc = None
                if callable(globals().get("get_npc_partner_for")):
                    _ntr_npc = get_npc_partner_for(girl)
                    if _ntr_npc and not getattr(_ntr_npc, "_ntr_active", False):
                        _ntr_npc = None

                if _ntr_npc is not None:
                    _ntr_lvl = getattr(_ntr_npc, "_ntr_boundary_level", 1)
                    _ntr_min = _NTR_ACT_MIN_LEVEL.get(action, 4)
                    _ntr_within = _ntr_lvl >= _ntr_min

                    if not _ntr_within:
                        _ntr_same_loc = getattr(_ntr_npc, "loc", None) == getattr(store, "CurrentLocation", None)
                        if _ntr_same_loc:
                            print("[LOYALTY] NTR boundary block (nearby): %s act=%s level=%d min=%d" % (girl.gid, action, _ntr_lvl, _ntr_min))
                            return True, "ntr_boundary_nearby"
                        _need = _NTR_EXCEED_GATES.get(action, 10)
                        if _need and t < _need:
                            print("[LOYALTY] NTR boundary block: %s act=%s level=%d tempt=%d need=%d" % (girl.gid, action, _ntr_lvl, t, _need))
                            return True, "ntr_boundary"
                else:
                    _bf_gates = {
                        "kiss": 3, "touch": 3, "masturbate": 4,
                        "hj": 5, "tj": 5, "oral": 5,
                        "bj": 7, "rub": 7, "tip": 7, "sex": 8, "anal": 9,
                    }
                    _need = _bf_gates.get(action, 0)
                    if _need and t < _need:
                        return True, "partner_loyalty"

            # If player has gf, require extra temptation too (she knows it's wrong)
            # Friendship with player's GF raises the gate further
            if cheating_for_player:
                _pg_gates = {
                    "kiss": 2, "touch": 2, "masturbate": 3,
                    "hj": 4, "tj": 4, "oral": 4,
                    "bj": 5, "rub": 6, "tip": 6, "sex": 7, "anal": 8,
                }
                _need = _pg_gates.get(action, 0)

                # Friendship penalty: best friends (1000) add +3 to gate, strangers (0) add +0
                _player_gf = get_player_girlfriend(store.ALL_GIRLS)
                if _player_gf and _player_gf != girl:
                    _friendship = girl.get_like_for(_player_gf.gid)
                    _friend_extra = min(3, int(_friendship / 250))  # 0-3: 0-249=+0, 250-499=+1, 500-749=+2, 750+=+3
                    _need += _friend_extra

                if _need and t < _need:
                    return True, "player_has_gf_block"

        # Virgin gate (optional hard block unless extremely tempted)
        # Only blocks vaginal sex — anal has no virginity concept
        if hasattr(girl, "get_flag") and girl.get_flag("virgin", False):
            if action == "sex":
                if t < 8:
                    return True, "virgin_block"

        return False, "ok"

    # ------------------------------
    # Can do action?
    # ------------------------------
    def can_do_action(girl, action, location=None, player_has_gf=False, player_gf_id=None):
        rules = ACTION_RULES.get(action)
        if not rules:
            return False, "invalid_action"

        blocked, why = is_loyalty_blocked(girl, action, player_has_gf=player_has_gf)
        if blocked:
            return False, why

        score = get_action_score(girl, action)
        mult = get_action_multiplier(girl, action, location=location, player_has_gf=player_has_gf, player_gf_id=player_gf_id)

        needed_stat = int(rules["min_stat"] * mult)
        needed_tempt = int(rules["min_temptation"] * mult)

        if int(getattr(girl, "Temptation", 0)) < needed_tempt:
            return False, "not_tempted"

        if score < needed_stat:
            return False, "stats_too_low"

        return True, "ok"

    # ------------------------------
    # Build cheating tags for event logging
    # ------------------------------
    def build_cheating_tags(girl, action, player_has_gf=False):
        tags = []
        if girl is None:
            return tags

        her_partner = _partner_key_for_girl(girl)
        if her_partner and action in ("kiss", "touch", "hj", "tj", "bj", "sex", "anal"):
            if her_partner.startswith("npc:"):
                tags.append(CHEAT_TAGS["girl_cheats_on_npc"])
            elif her_partner.startswith("girl:"):
                tags.append(CHEAT_TAGS["girl_cheats_on_girl"])

        if player_has_gf and action in ("kiss", "touch", "hj", "tj", "bj", "sex", "anal"):
            tags.append(CHEAT_TAGS["player_cheats_on_girl"])

        return tags

    # ------------------------------
    # Girl-to-girl interaction helper (affinity + history)
    # ------------------------------
    def record_girl_interaction(girl_a, girl_b, action, like_delta=0, shared_player=False):
        """
        Updates:
        - a likes b
        - b likes a
        - history counters: kiss/touch/etc
        - shared_player/threesome counters
        """
        if not girl_a or not girl_b:
            return

        a_id = getattr(girl_a, "Id", str(girl_a))
        b_id = getattr(girl_b, "Id", str(girl_b))

        if like_delta:
            girl_a.add_like_for(b_id, like_delta)
            girl_b.add_like_for(a_id, like_delta)

        girl_a.inc_history_with(b_id, action, 1)
        girl_b.inc_history_with(a_id, action, 1)

        if shared_player:
            girl_a.inc_history_with(b_id, "shared_player", 1)
            girl_b.inc_history_with(a_id, "shared_player", 1)
            girl_a.inc_history_with(b_id, "threesome", 1)
            girl_b.inc_history_with(a_id, "threesome", 1)

    # ------------------------------
    # Utility: provoke (temptation step)
    # ------------------------------
    def provoke(girl, amount=1, cap=10):
        if girl is None:
            return
        girl.add_temptation(int(amount))
        if girl.Temptation > int(cap):
            girl.Temptation = int(cap)
