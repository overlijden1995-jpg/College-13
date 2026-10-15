# ============================================================
# Cum.rpy... Player cum / creampie system
# ============================================================

default _session_cum = {}
default _session_loads_by_girl = {}   # gid -> loads that touched her this session (trait_is_first reads it)
default _atm_session_count = 0
default _atm_cum_in_mouth = False
default _edge_end_said = None          # gid whose "left on the edge" line this session already played (scene_full_cleanup)
default _atm_source_gid = None
default _recording_had_atm = False
default _hate_cum_scene_aborted = False
default _forced_creampie_count = 0
default _focus_overdue_count = 0
default _focus_warning_shown = False
default _forced_creampie_end_after_orgasm = False
default _player_exhausted = False
default _scene_force_end = False
default _session_girl_orgasms = 0
default _session_orgasms_by_girl = {}
default _session_spanked_girls = set()
default _hard_cum_ready = False
default _pcc_choice = None
default _pcc_raw_allowed = False
default _resist_result = ""
default _bj_prev_speed = 1
default _bj_prev_action = "suck"
default _threesome_mode = False
default _threesome_participants = set()
default _sex_menu_active = False
default _post_cum_pending = False
default _post_cum_result = "stop"
default _post_cum_had_condom = False
default _post_cum_sub_mode = "sex"
default _post_cum_scene_type = ""
default _post_cum_menu = None
default _via_bj_post_cum_choice = None

init python:

    # The raw-lock condom etiquette (another condom / ask to go raw) only belongs where going back in
    # BARE is a thing. A hand, mouth, chest or feet scene has nothing raw to return to: the menu there
    # read as "the game thinks we had sex" (tester 2026-10-10/11, story HJ and BJ scenes).
    _NONPENETRATIVE_SCENES = ("hj", "tj", "fj", "bj", "rj", "masturbate")
    def _scene_is_penetrative(scene_type):
        return scene_type not in _NONPENETRATIVE_SCENES

    # ---------------------------------------------------------
    # Cum image helper (existing)
    # ---------------------------------------------------------
    def get_cum_image(girl, pose, tag):
        """
        girl: objeto Girl
        pose: "Handjob", "BJ", "Reverse Cowgirl", etc
        tag: "Face1", "Tits2", "Mouth1" etc
        """
        path = "images/characters/{}/{}/Cum/{}.png".format(
            girl.Name,
            pose,
            tag.replace(" ", "")
        )
        if renpy.loadable(path):
            return path
        return Null()

    # =========================================================
    # 1. CONFIG MAPPINGS
    # =========================================================

    # Lust gain per "Keep going" / "Speed up" tick: {scene: {speed: gain}}
    PLAYER_LUST_GAINS = {
        "hj":       {1: 5, 2: 10},
        "bj_lick":  {1: 3},
        "bj_suck":  {1: 5, 2: 8, 3: 12},
        "tj":       {1: 4, 2: 8, 3: 12},
        "fj":       {1: 4, 2: 8, 3: 12},
        "rj":       {1: 6, 2: 10, 3: 15},
        "cowgirl":  {1: 5, 2: 8, 3: 15},
        "reverse_cowgirl":    {1: 5, 2: 8, 3: 15},
        "reverse_cowgirl_anal": {1: 6, 2: 10, 3: 18},
        "doggy":              {1: 5, 2: 8, 3: 15},
        "anal":               {1: 6, 2: 10, 3: 18},
        "full_nelson":        {1: 5, 2: 8, 3: 15},
        "full_nelson_anal":   {1: 6, 2: 10, 3: 18},
        "laying_down":        {1: 5, 2: 8, 3: 15},
        "laying_anal":        {1: 6, 2: 10, 3: 18},
        "tip":                {1: 3},
        "rub":                {1: 2},
    }

    # ── Position dispatch config ────────────────────────────
    # Replaces ~30 if/elif chains with a single dict lookup.
    # To add a new pose: add one entry here, all Cum.rpy dispatch works automatically.
    # "sub_events": the girl-initiated sub-events that scene can roll (SubEvents.rpy sub_event_dispatch); missing =
    # all of them (the positions). Scenes where he is not inside her only get the ones where she just talks or asks.
    # "max_speed": the scene's top speed when it is not 3 (a pace request never goes past it).
    CUM_POSITION_CONFIG = {
        "bj": {
            "cum_anim":           "BJ_CumAnim",
            "fire_away_anim":     "BJ_CumAnim",
            "outside_freeze":     None,
            "condom_remove_anim": None,
            "creampie_aftermath": None,
            "end_label":          "BJ_End",
            "skip_condom_hide":   False,
            "apply_speed_label":  "BJ_ApplySpeed",
            "speed_var":          "bj_speed",
            "condom_img_prefix":  None,
            "tip_mode_var":       None,
            "rub_mode_var":       None,
            "hole_transition_label": None,
            # no pace (licking has one speed) and no recording request (BJ only records while she sucks)
            "sub_events":         ("cum_warning", "virgin_nervous", "public_panic", "femdom_no_cum", "femdom_cum_demand", "subm_cum_where"),
        },
        "hj": {
            "cum_anim":           "HJ_CumAnim",
            "fire_away_anim":     "HJ_CumAnim",
            "outside_freeze":     None,
            "condom_remove_anim": None,
            "creampie_aftermath": None,
            "end_label":          "HJ_End",
            "skip_condom_hide":   False,
            "apply_speed_label":  "HJ_ApplySpeed",
            "speed_var":          "hj_speed",
            "condom_img_prefix":  None,
            "tip_mode_var":       None,
            "rub_mode_var":       None,
            "hole_transition_label": None,
            # she is the one moving here: of her orders only "don't cum yet" fits (no pace / challenge for him)
            "sub_events":         ("pace", "recording_request", "cum_warning", "virgin_nervous", "public_panic", "femdom_no_cum", "netori_call", "subm_orders", "subm_cum_where"),
            "max_speed":          2,
        },
        "tj": {
            "cum_anim":           "TJ_CumAnim",
            "fire_away_anim":     "TJ_FireAwayCumAnim",
            "outside_freeze":     None,
            "condom_remove_anim": None,
            "creampie_aftermath": None,
            "end_label":          "TITJOB_End",
            "skip_condom_hide":   False,
            "apply_speed_label":  "TITJOB_ApplySpeed",
            "speed_var":          "titjob_speed",
            "condom_img_prefix":  None,
            "tip_mode_var":       None,
            "rub_mode_var":       None,
            "hole_transition_label": None,
            # she is the one moving here: of her orders only "don't cum yet" fits (no pace / challenge for him)
            "sub_events":         ("pace", "recording_request", "cum_warning", "virgin_nervous", "public_panic", "femdom_no_cum", "netori_call", "subm_orders", "subm_cum_where"),
        },
        "fj": {
            "cum_anim":           "FT_CumAnim",
            "fire_away_anim":     None,
            "outside_freeze":     None,
            "condom_remove_anim": None,
            "creampie_aftermath": None,
            "end_label":          "FT_End",
            "skip_condom_hide":   False,
            "apply_speed_label":  "FT_ApplySpeed",
            "speed_var":          "_ft_speed",
            "condom_img_prefix":  None,
            "tip_mode_var":       None,
            "rub_mode_var":       None,
            "hole_transition_label": None,
            # she is the one moving here: of her orders only "don't cum yet" fits (no pace / challenge for him)
            "sub_events":         ("pace", "recording_request", "cum_warning", "virgin_nervous", "public_panic", "femdom_no_cum", "subm_orders", "subm_cum_where"),
        },
        # Rimjob (Core_Rimjob.rpy): her hand is the only place he can reach ("cum_menu": PlayerCumMenu_Hand)
        "rj": {
            "cum_anim":           "RJ_CumAnim",
            "fire_away_anim":     "RJ_FireAwayAnim",
            "outside_freeze":     None,
            "condom_remove_anim": None,
            "creampie_aftermath": None,
            "end_label":          "RJ_End",
            "skip_condom_hide":   False,
            "apply_speed_label":  "RJ_ApplySpeed",
            "speed_var":          "_rj_speed",
            "condom_img_prefix":  None,
            "tip_mode_var":       None,
            "rub_mode_var":       None,
            "hole_transition_label": None,
            "cum_menu":           "PlayerCumMenu_Hand",
            # he is the one in control, her mouth is busy: only "don't cum yet", a camera, being seen
            "sub_events":         ("recording_request", "public_panic", "femdom_no_cum"),
        },
        "reverse_cowgirl": {
            "cum_anim":           "RCG_CumAnim",
            "fire_away_anim":     "RCG_CumAnim",
            "outside_freeze":     "RCG_CumOutsideFreeze",
            "condom_remove_anim": "RCG_CondomRemoveAnim",
            "creampie_aftermath": "RCG_CreampieAftermath",
            "end_label":          "RCG_End",
            "skip_condom_hide":   True,
            "apply_speed_label":  "RCG_ApplySpeed",
            "speed_var":          "rcg_speed",
            "condom_img_prefix":  "rcg_condom",
            "tip_mode_var":       "rcg_tip_mode",
            "rub_mode_var":       "rcg_rub_mode",
            "hole_transition_label": "RCG_HoleTransition",   # her anal request (SubEvents) switches holes through it
            "tip_outside_cum_type": "ass",
            "tip_outside_visual": "RCG_TipDeniedCumVisual",
        },
        # her ass in the reverse cowgirl (a girl whose art has it: Core_RCG rcg_has_anal): the same labels, which read
        # store.rcg_anal; its own type so his cum inside counts as anal (never a creampie) like every anal variant
        "reverse_cowgirl_anal": {
            "cum_anim":           "RCG_CumAnim",
            "fire_away_anim":     "RCG_CumAnim",
            "outside_freeze":     "RCG_CumOutsideFreeze",
            "condom_remove_anim": "RCG_CondomRemoveAnim",
            "creampie_aftermath": "RCG_CreampieAftermath",
            "end_label":          "RCG_End",
            "skip_condom_hide":   True,
            "apply_speed_label":  "RCG_ApplySpeed",
            "speed_var":          "rcg_speed",
            "condom_img_prefix":  "rcg_condom",
            "tip_mode_var":       "rcg_tip_mode",
            "rub_mode_var":       "rcg_rub_mode",
            "hole_transition_label": "RCG_HoleTransition",
            "tip_outside_cum_type": "ass",
            "tip_outside_visual": "RCG_TipDeniedCumVisual",
        },
        "cowgirl": {
            "cum_anim":           "CG_CumAnim",
            "fire_away_anim":     "CG_CumAnim",
            "outside_freeze":     "CG_CumOutsideFreeze",
            "condom_remove_anim": "CG_CondomRemoveAnim",
            "creampie_aftermath": "COWGIRL_CreampieAftermath",
            "end_label":          "COWGIRL_End",
            "skip_condom_hide":   True,
            "apply_speed_label":  "COWGIRL_ApplySpeed",
            "speed_var":          "cowgirl_speed",
            "condom_img_prefix":  "cowgirl_condom",
            "tip_mode_var":       "cowgirl_tip_mode",
            "rub_mode_var":       "cowgirl_rub_mode",
            "hole_transition_label": None,
            "tip_outside_cum_type": "outside",
            "tip_outside_visual": "CG_TipDeniedCumVisual",
        },
        "doggy": {
            "cum_anim":           "DG_CumAnim",
            "fire_away_anim":     "DG_CumAnim",
            "outside_freeze":     "DG_CumOutsideFreeze",
            "condom_remove_anim": "DG_CondomRemoveAnim",
            "creampie_aftermath": "DG_CreampieAftermath",
            "end_label":          "DG_End",
            "skip_condom_hide":   True,
            "apply_speed_label":  "DG_ApplySpeed",
            "speed_var":          "doggy_speed",
            "condom_img_prefix":  "dg_condom",
            "tip_mode_var":       "doggy_tip_mode",
            "rub_mode_var":       "doggy_rub_mode",
            "hole_transition_label": "DG_HoleTransition",
            "tip_outside_cum_type": "ass",
            "tip_outside_visual": "DG_TipDeniedCumVisual",
        },
        "anal": {
            "cum_anim":           "DG_CumAnim",
            "fire_away_anim":     "DG_CumAnim",
            "outside_freeze":     "DG_CumOutsideFreeze",
            "condom_remove_anim": "DG_CondomRemoveAnim",
            "creampie_aftermath": "DG_CreampieAftermath",
            "end_label":          "DG_End",
            "skip_condom_hide":   True,
            "apply_speed_label":  "DG_ApplySpeed",
            "speed_var":          "doggy_speed",
            "condom_img_prefix":  "dg_condom",
            "tip_mode_var":       "doggy_tip_mode",
            "rub_mode_var":       "doggy_rub_mode",
            "hole_transition_label": "DG_HoleTransition",
            "tip_outside_cum_type": "ass",
            "tip_outside_visual": "DG_TipDeniedCumVisual",
        },
        "full_nelson": {
            "cum_anim":           "FN_CumAnim",
            "fire_away_anim":     "FN_CumAnim",
            "outside_freeze":     "FN_CumOutsideFreeze",
            "condom_remove_anim": "FN_CondomRemoveAnim",
            "creampie_aftermath": "FN_CreampieAftermath",
            "end_label":          "FN_End",
            "skip_condom_hide":   True,
            "apply_speed_label":  "FN_ApplySpeed",
            "speed_var":          "fn_speed",
            "condom_img_prefix":  "fn_condom",
            "tip_mode_var":       "fn_tip_mode",
            "rub_mode_var":       "fn_rub_mode",
            "hole_transition_label": "FN_HoleTransition",
            "tip_outside_cum_type": "ass",      # FN draws ass / boobs / face cum, never "body" (the "outside" default)
        },
        "full_nelson_anal": {
            "cum_anim":           "FN_CumAnim",
            "fire_away_anim":     "FN_CumAnim",
            "outside_freeze":     "FN_CumOutsideFreeze",
            "condom_remove_anim": "FN_CondomRemoveAnim",
            "creampie_aftermath": "FN_CreampieAftermath",
            "end_label":          "FN_End",
            "skip_condom_hide":   True,
            "apply_speed_label":  "FN_ApplySpeed",
            "speed_var":          "fn_speed",
            "condom_img_prefix":  "fn_condom",
            "tip_mode_var":       "fn_tip_mode",
            "rub_mode_var":       "fn_rub_mode",
            "hole_transition_label": "FN_HoleTransition",
            "tip_outside_cum_type": "ass",
        },
        "laying_down": {
            "cum_anim":           "LD_CumAnim",
            "fire_away_anim":     "LD_CumAnim",
            "outside_freeze":     "LD_CumOutsideFreeze",
            "condom_remove_anim": "LD_CondomRemoveAnim",
            "creampie_aftermath": "LD_CreampieAftermath",
            "end_label":          "LD_End",
            "skip_condom_hide":   True,
            "apply_speed_label":  "LD_ApplySpeed",
            "speed_var":          "laying_speed",
            "condom_img_prefix":  "ld_condom",
            "tip_mode_var":       "laying_tip_mode",
            "rub_mode_var":       "laying_rub_mode",
            "hole_transition_label": "LD_HoleTransition",
        },
        "laying_anal": {
            "cum_anim":           "LD_CumAnim",
            "fire_away_anim":     "LD_CumAnim",
            "outside_freeze":     "LD_CumOutsideFreeze",
            "condom_remove_anim": "LD_CondomRemoveAnim",
            "creampie_aftermath": "LD_CreampieAftermath",
            "end_label":          "LD_End",
            "skip_condom_hide":   True,
            "apply_speed_label":  "LD_ApplySpeed",
            "speed_var":          "laying_speed",
            "condom_img_prefix":  "ld_condom",
            "tip_mode_var":       "laying_tip_mode",
            "rub_mode_var":       "laying_rub_mode",
            "hole_transition_label": "LD_HoleTransition",
        },
    }

    def _cum_cfg(scene_type, key, default=None):
        """Lookup CUM_POSITION_CONFIG for a scene_type + key."""
        cfg = CUM_POSITION_CONFIG.get(scene_type)
        if cfg is None:
            print("[WARN] CUM_POSITION_CONFIG: unknown scene_type '%s'" % scene_type)
            return default
        return cfg.get(key, default)

    def _cum_skip_hide(scene_type):
        """True when condom layer should NOT be hidden (pose handles it via anim)."""
        return CUM_POSITION_CONFIG.get(scene_type, {}).get("skip_condom_hide", False)

    def _condom_img_tag(prefix):
        """Return broken or intact condom image tag for the given prefix."""
        return (prefix + "_broken") if store._condom_broken else prefix

    def _cum_get_speed(scene_type):
        """Return current speed for a scene_type via config lookup."""
        _sv = _cum_cfg(scene_type, "speed_var")
        return getattr(store, _sv, 0) if _sv else 0

    def _any_rub_or_tip_active():
        """True if any position is currently in rub or tip mode."""
        for _st, _cfg in CUM_POSITION_CONFIG.items():
            _rm = _cfg.get("rub_mode_var")
            _tm = _cfg.get("tip_mode_var")
            if _rm and getattr(store, _rm, False):
                return True
            if _tm and getattr(store, _tm, False):
                return True
        return False

    def _se_adjust_pace(scene_type, delta):
        """Adjust current speed variable by delta (clamped 0 to the scene's max_speed, 3 by default) using config lookup."""
        _sv = _cum_cfg(scene_type, "speed_var")
        if _sv:
            _cur = getattr(store, _sv, 0)
            setattr(store, _sv, max(0, min(_cum_cfg(scene_type, "max_speed", 3), _cur + delta)))

    # ---------------------------------------------------------
    # Creampie Aftermath — centralized expression mapping
    # ---------------------------------------------------------
    CREAMPIE_AFTERMATH_EXPRESSIONS = {
        (False, "cum_slut"):     ("ahegao", {"blush": "3"}),
        (False, "anal_lover"):   ("ahegao", {"blush": "3"}),
        (False, "anal_hater"):   ("scared", {"blush": "2"}),
        (False, "hardcore_sex"): ("surprised", {}),
        (False, "cute_sex"):     ("sad", {}),
        (False, "default"):      ("scared", {}),
        # Condom break context overrides (checked first in resolver)
        (False, "condom_break"):          ("angry", {}),
        (False, "condom_break_believed"): ("worried", {}),
        (False, "condom_break_cum_slut"): ("lewd", {"blush": "2"}),
        (True, "cum_slut"):      ("ahegao", {"blush": "3"}),
        (True, "anal_lover"):    ("ahegao", {"blush": "3"}),
        (True, "anal_hater"):    ("uncomfortable", {}),
        (True, "hardcore_sex"):  ("lewd", {}),
        (True, "cute_sex"):      ("shy", {}),
        (True, "default"):       ("happy", {}),
    }

    # ---------------------------------------------------------
    # First creampie + partner — stat impact (migrated from
    # _first_creampie_bf_reaction, applied in Central)
    # ---------------------------------------------------------
    FIRST_CREAMPIE_PARTNER_STATS = {
        "cum_slut":  {"Inbt": 20, "Lust": 15},
        "cheater":   {"Inbt": 20, "Lust": 15},
        "loyal":     {"Love": -20, "Obed": 10, "Inbt": 10},
        "neutral":   {"Love": -5, "Inbt": 10},
    }

    def _resolve_first_creampie_category(girl):
        if girl.has_trait("cum_slut"):
            return "cum_slut"
        _att = get_effective_cheat_attitude(girl) if callable(get_effective_cheat_attitude) else int(getattr(girl, "CheatAttitude", 3))
        if girl.has_trait("cheater") or _att >= 6:
            return "cheater"
        if girl.has_trait("loyal") or _att <= 2:
            return "loyal"
        return "neutral"

    def _ca_resolve_expression(girl, consented, is_anal):
        """Pick expression for creampie aftermath. Data-driven, priority-ordered."""
        # Condom break override (highest priority when not consented)
        if not consented and getattr(store, "_scene_condom_break", False):
            if girl.has_trait("cum_slut"):
                return CREAMPIE_AFTERMATH_EXPRESSIONS.get((False, "condom_break_cum_slut"), ("lewd", {"blush": "2"}))
            if getattr(store, "_scene_condom_break_believed", False):
                return CREAMPIE_AFTERMATH_EXPRESSIONS.get((False, "condom_break_believed"), ("worried", {}))
            return CREAMPIE_AFTERMATH_EXPRESSIONS.get((False, "condom_break"), ("angry", {}))
        _cs = girl.has_trait("cum_slut")
        _al = is_anal and girl.has_trait("anal_lover")
        _ah = is_anal and girl.has_trait("anal_hater")
        _hc = girl.has_trait("hardcore_sex")
        _cu = girl.has_trait("cute_sex")
        if _cs or _al:
            _tk = "cum_slut" if _cs else "anal_lover"
        elif _ah:
            _tk = "anal_hater"
        elif _hc:
            _tk = "hardcore_sex"
        elif _cu:
            _tk = "cute_sex"
        else:
            _tk = "default"
        _expr, _ov = CREAMPIE_AFTERMATH_EXPRESSIONS[(consented, _tk)]
        if _expr == "ahegao":
            _expr = renpy.random.choice(["ahegao", "ahegao_2"])
        return _expr, _ov

    # Permission rules... same schema as APPROVAL_ACTION_RULES
    CUM_PERMISSION_RULES = {
        "_default": {
            "cum_in_mouth_ask":     {"T": 800,  "Type": "LOI", "Spread": 160, "Variation": 40},
            "cum_inside_ask":       {"T": 1250, "Type": "LOI", "Spread": 160, "Variation": 40},
            "cum_inside_anal_ask":  {"T": 1100, "Type": "OI",  "Spread": 160, "Variation": 40},
            "cum_in_mouth_from_anal_ask": {"T": 1200, "Type": "OI", "Spread": 160, "Variation": 40},
            "cum_remove_condom_ask":{"T": 1300, "Type": "LOI", "Spread": 180, "Variation": 50},
            "condom_remove_midscene":{"T": 900, "Type": "LOI", "Spread": 180, "Variation": 50},
        },
    }

    # Penalties when forced without permission
    CUM_PENALTY_RULES = {
        "cum_in_mouth_forced":    {"Love": -30,  "Obed": -15, "Inbt": 15},
        "cum_inside_forced":      {"Love": -80,  "Obed": 20, "Inbt": 30},
        "condom_removed_forced":  {"Love": -150, "Obed": 30, "Inbt": 40},
    }

    # Bonuses when consensual
    CUM_BONUS_RULES = {
        "cum_outside":            {"Love": 5,   "Obed": 5,  "Inbt": 10},
        "cum_in_mouth_allowed":   {"Love": 10,  "Obed": 10, "Inbt": 15},
        "cum_inside_allowed":     {"Love": 20,  "Obed": 15, "Inbt": 25},
        "condom_removed_allowed": {"Love": 15,  "Obed": 20, "Inbt": 30},
    }

    # Display names for cum locations (UI label)
    CUM_DISPLAY_NAMES = {
        "inside":                 "Creampie",
        "condom_removed_inside":  "Creampie",
        "face":                   "Face",
        "mouth":                  "Mouth",
        "tits":                   "Tits",
        "ass":                    "Ass",
        "back":                   "Back",
        "belly":                  "Belly",
        "outside":                "Body",
        "condom":                 "Condom",
        "away":                   None,
    }

    # Cleanup permission thresholds
    # "eat": needs Obed + Inbt
    # "leave": needs Inbt, bonus from public exposure acts
    CUM_CLEANUP_RULES = {
        "eat":   {"T": 500, "Type": "OI",  "Spread": 140, "Variation": 30},
        "leave": {"T": 600, "Type": "LOI", "Spread": 160, "Variation": 40},
    }

    # =========================================================
    # POST-CUM CONDOM/RAW DECISION LINES (shared by all positions)
    # =========================================================

    _POST_CUM_RAW_SUGGEST = [
        _("You know... you don't have to put another one on. I can take it raw."),
        _("Forget the condom... I want to feel you this time."),
        _("Do we really need another one? Just put it in... like this."),
    ]

    _POST_CUM_RAW_ACCEPT = [
        _("Mmm... that's more like it. I can feel everything now."),
        _("Yes... so much better without it."),
        _("Finally... now give it to me for real."),
    ]

    # =========================================================
    # RESIST FORCED CUM CONFIG
    # =========================================================

    RESIST_POSITION_TYPE = {
        "cowgirl": "on_top", "reverse_cowgirl": "on_top", "reverse_cowgirl_anal": "on_top",
        "doggy": "neutral", "anal": "neutral", "full_nelson": "neutral", "full_nelson_anal": "neutral",
        "laying_down": "neutral", "laying_anal": "neutral",
        "bj": "oral", "hj": "oral", "tj": "oral",
    }

    RESIST_STRENGTH_TABLE = {
        5: {"on_top": True,  "neutral": True,  "oral": True},
        4: {"on_top": True,  "neutral": True,  "oral": True},
        3: {"on_top": False, "neutral": True,  "oral": True},
        2: {"on_top": False, "neutral": False, "oral": False},
        1: {"on_top": False, "neutral": False, "oral": False},
    }

    RESIST_OBED_BASE = {"cum_slut": 600, "default": 500}
    RESIST_OBED_PER_LEVEL = 100

    RESIST_NARRATION = {
        "on_top": {
            "attempt": [
                _("She's on top of you, pinning you down. You try to lift her off..."),
                _("You grab her hips and try to push her up, but she bears down with all her weight..."),
            ],
            "success": [
                _("With a surge of strength, you manage to lift her off just in time."),
                _("You grip her waist and force her up. She yelps as you overpower her."),
            ],
            "fail": [
                _("She's too heavy from this angle. She slams down harder and you can't stop it."),
                _("You try to lift her but she locks her legs. There's no escaping from underneath."),
            ],
        },
        "neutral": {
            "attempt": [
                _("You grab her hips trying to pull out, but she pushes back against you..."),
                _("You try to pull away but she braces herself and pushes back..."),
            ],
            "success": [
                _("You manage to pull out just in time, overpowering her grip."),
                _("With your strength, you yank her hips forward and pull free."),
            ],
            "fail": [
                _("She's too determined. She pushes back hard and you can't pull out in time."),
                _("She throws herself back against you before you can react. It's too late."),
            ],
        },
        "oral": {
            "attempt": [
                _("You try to pull away but she grips your hips tighter..."),
                _("You grab the back of her head trying to push away, but she holds on..."),
            ],
            "success": [
                _("You manage to pull free from her grip at the last second."),
                _("With enough force, you push her head back and pull out of her mouth."),
            ],
            "fail": [
                _("She grips too tight. Her hands lock behind you and she pulls you deeper."),
                _("She won't let go. Her grip is iron and she forces every drop into her mouth."),
            ],
        },
    }

    RESIST_GIRL_SHOCK = [
        _("Wh... what?! How are you so strong?!"),
        _("No! I almost had you! That's not fair!"),
        _("You... you overpowered me... ugh, fine!"),
    ]

    _FORCED_CUM_COOLDOWN_DAYS = 3

    def _forced_cum_on_cooldown(girl):
        _last = getattr(girl, "_forced_cum_last_day", -999)
        return (store.Day - _last) < _FORCED_CUM_COOLDOWN_DAYS

    RESIST_AUTO_OBED_GIRL = {
        "revenge": [
            _("I'm going to... I'll make you... I..."),
            _("You're cumming inside this time! I'll... I..."),
            _("I won't let you pull out! I'll just... I..."),
        ],
        "auto": [
            _("Inside! Cum inside me! I'll make you... I..."),
            _("Don't you dare pull out! I'll hold you... I..."),
            _("I need it! I'll force you to... I..."),
        ],
        "bj": [
            _("Give it to me! I'm not letting go! I'll... I..."),
            _("It's mine! I'll hold you there until... I..."),
        ],
        "femdom": [
            _("Stay under me. You're finishing where I say... I... ugh."),
            _("Don't you dare move. I decide where you... I..."),
            _("You're not pulling out. I'm on top, I make the... I..."),
        ],
    }

    RESIST_AUTO_OBED_NARR = [
        _("She tries to take control, but her body hesitates. She can't bring herself to defy you."),
        _("She wants to force it, but something stops her. Your dominance over her is too strong."),
        _("She reaches for you but freezes. Even in her desperation, she can't override your authority."),
    ]

    RESIST_AUTO_OBED_GIRL_AFTER = [
        _("I... I can't... just... please..."),
        _("Why can't I just... ugh... fine, you decide..."),
        _("I want it so bad but I... I can't make you..."),
    ]

    RESIST_AUTO_STRENGTH_GIRL = {
        "revenge": [
            _("You're NOT pulling out this time!"),
            _("I won't let you! Stay inside!"),
        ],
        "auto": [
            _("Cum inside me! I'll MAKE you!"),
            _("You're not going anywhere!"),
        ],
        "bj": [
            _("You're cumming in my mouth! Don't move!"),
            _("I'm not letting go!"),
        ],
        "femdom": [
            _("Stay right there. You finish inside me because I say so."),
            _("You're not going anywhere. I'm on top, I decide."),
        ],
    }

    RESIST_AUTO_STRENGTH_NARR = {
        "on_top": [
            _("She tries to slam down and lock her legs, but you grab her hips and lift her like she weighs nothing."),
            _("She bears down with all her weight, but your grip is iron. You hold her in place effortlessly."),
        ],
        "neutral": [
            _("She pushes back trying to trap you inside, but you're far stronger. You hold her still with one hand."),
            _("She braces herself and pushes back, but you overpower her easily. She can't match your strength."),
        ],
        "oral": [
            _("She grabs your hips and tries to pull you deeper, but you push her head back without effort."),
            _("She grips tighter, desperate to hold you in place, but you pry her hands away easily."),
        ],
    }

    RESIST_AUTO_STRENGTH_GIRL_AFTER = [
        _("You're... too strong... I can't hold you..."),
        _("How are you this strong?! I can't... ugh, fine!"),
        _("Let go of me! I almost... no, I can't overpower you..."),
    ]

    # =========================================================
    # 2. PYTHON FUNCTIONS
    # =========================================================

    def _get_auto_resist_reason(girl):
        """Returns why player auto-resists: 'strength', 'obed', or None."""
        _is_athlete = getattr(Player, "player_trait", "") == "athlete"
        _p_energy = getattr(Player, "energy_max", 2)
        if _is_athlete or _p_energy >= 5:
            debug_log("[RESIST] auto: strength (athlete=%s energy=%d)" % (_is_athlete, _p_energy))
            return "strength"
        base = RESIST_OBED_BASE["cum_slut" if girl.has_trait("cum_slut") else "default"]
        reduction = max(0, (_p_energy - 2)) * RESIST_OBED_PER_LEVEL
        threshold = base - reduction
        if girl.Obed >= threshold:
            debug_log("[RESIST] auto: obed (girl.Obed=%d >= threshold=%d)" % (girl.Obed, threshold))
            return "obed"
        debug_log("[RESIST] no auto-resist (Obed=%d < threshold=%d, energy=%d)" % (girl.Obed, threshold, _p_energy))
        return None

    def _resist_physical_check(scene_type):
        """True = player overpowers her in menu resist attempt."""
        e = 5 if getattr(Player, "player_trait", "") == "athlete" else getattr(Player, "energy_max", 2)
        pos_type = RESIST_POSITION_TYPE.get(scene_type, "neutral")
        result = RESIST_STRENGTH_TABLE.get(e, RESIST_STRENGTH_TABLE[2]).get(pos_type, False)
        debug_log("[RESIST] physical check: energy=%d scene=%s pos_type=%s result=%s" % (e, scene_type, pos_type, result))
        return result

    def _resist_narration(scene_type, phase):
        """Get random narration line for menu resist sequence."""
        pos_type = RESIST_POSITION_TYPE.get(scene_type, "neutral")
        pool = RESIST_NARRATION.get(pos_type, RESIST_NARRATION["neutral"]).get(phase, [])
        return _tl(renpy.random.choice(pool)) if pool else "..."

    def get_player_lust_gain(scene_type, speed):
        """Lookup focus gain from PLAYER_LUST_GAINS config."""
        scene = PLAYER_LUST_GAINS.get(scene_type, {})
        return scene.get(speed, 0)

    def player_is_cumming():
        """True when Player.Focus has reached the cum threshold."""
        return getattr(Player, "Focus", 0) >= 100

    # ── Focus Overdue system ──
    # When Focus reaches 100, player can choose "Cum" or keep going.
    # Each action past 100 rolls for forced cum: P = 1 - 0.5^n

    _FORCED_CUM_MAP = {
        "doggy": "inside", "cowgirl": "inside", "reverse_cowgirl": "inside",
        "full_nelson": "inside", "anal": "inside_anal", "full_nelson_anal": "inside_anal",
        "laying_down": "inside", "laying_anal": "inside_anal", "reverse_cowgirl_anal": "inside_anal",
        "bj": "mouth", "tj": "tits", "hj": "outside", "fj": "feet", "rj": "hand",
    }
    # Overdue cum types that land OUTSIDE her on one spot of their own (recorded as that spot, not "outside")
    _FORCED_CUM_OUTSIDE_SPOTS = ("feet", "hand")

    _FORCED_OVERDUE_LINES = {
        "inside": [
            _("You can't hold back anymore and cum deep inside her."),
            _("Your body gives in... you lose control and cum inside her."),
            _("You try to pull out, but it's too late... you cum deep inside her."),
        ],
        "inside_anal": [
            _("You can't hold back anymore and cum deep inside her ass."),
            _("Your body gives in... you lose control and cum inside her ass."),
            _("You try to pull out, but it's too late... you cum deep in her ass."),
        ],
        "condom": [
            _("You can't hold back anymore and cum inside the condom."),
            _("Your body gives in... you lose control and fill the condom."),
            _("You try to hold on, but it's no use... you cum inside the condom."),
        ],
        "mouth": [
            _("You can't hold back and cum in her mouth before she can react."),
            _("Your body gives in... you release in her mouth without warning."),
            _("You try to warn her, but it's too late... you cum in her mouth."),
        ],
        "tits": [
            _("You can't hold back anymore and cum all over her chest."),
            _("Your body gives in... you lose control and cum all over her tits."),
            _("You try to hold on, but it's no use... you cum all over her breasts."),
        ],
        "outside": [
            _("You can't hold back anymore and cum on her."),
            _("Your body gives in... you lose control and cum all over her."),
            _("You try to hold on, but it's no use... you pull out and cum on her."),
        ],
        "rub": [
            _("You can't hold back anymore and cum all over her."),
            _("Your body gives in... you lose control and cum on her."),
            _("You try to hold on, but it's no use... you cum all over her."),
        ],
        "hand": [
            _("You can't hold back anymore and cum all over her hand."),
            _("Your body gives in... her hand keeps stroking you through it."),
            _("You try to hold on, but her tongue and her hand push you over the edge."),
        ],
        "feet": [
            _("You can't hold back anymore and cum all over her feet."),
            _("Your body gives in... you lose control and cum between her toes."),
            _("You try to hold on, but her feet push you over the edge."),
        ],
    }

    def focus_overdue_roll():
        n = store._focus_overdue_count
        if n <= 1:
            return False
        emax = getattr(store.Player, "energy_max", 2)
        base = min(0.70, max(0.40, 0.40 + emax * 0.05))
        p = 1.0 - (base ** n)
        roll = renpy.random.random()
        result = roll < p
        debug_log("[FOCUS_OVERDUE] n=%d emax=%d base=%.2f P=%.4f roll=%.4f triggered=%s" % (n, emax, base, p, roll, result))
        if not result and n >= 3:
            unlock_achievement("hold_steady")
        return result

    def focus_overdue_tick():
        store._focus_overdue_count += 1
        debug_log("[FOCUS_OVERDUE] tick: count now %d" % store._focus_overdue_count)
        return focus_overdue_roll()

    def _forced_cum_type(scene_type):
        phase = getattr(store, "_scene_phase", "sex")
        if phase == "rub":
            return "outside"
        base = _FORCED_CUM_MAP.get(scene_type, "outside")
        if base in ("inside", "inside_anal") and store.condom_active:
            return "condom"
        return base

    # DEPRECATED: use girl.has_trait("trait") instead
    def _girl_has_trait(girl, name):
        traits = getattr(girl, "traits", set())
        return str(name).lower() in set(str(x).lower() for x in traits)

    def _girl_lust_gain(girl, base, speed=None):
        """Apply girl lust gain with trait bonuses.
        speed: current scene speed (0-3). Pass explicitly from Core files.
        - exhibitionist + public: +50% lust
        - public_fetish + public: +1 lust
        - hardcore_sex + speed 3: +2 lust
        - cute_sex + speed 1: +2 lust
        - camera_lover + recording: +2 lust
        """
        bonus = 0

        # Exhibitionist in public: +50%
        if girl.has_trait("exhibitionist") and _is_public_location():
            bonus += max(1, base // 2)

        # Public fetish in public: flat +1
        if girl.has_trait("public_fetish") and _is_public_location():
            bonus += 1

        # Hardcore at max speed: +2
        if speed is not None and girl.has_trait("hardcore_sex") and speed >= 3:
            bonus += 2

        # Cute at slow speed: +2
        if speed is not None and girl.has_trait("cute_sex") and speed == 1:
            bonus += 2

        # Camera lover while being recorded: +2
        if girl.has_trait("camera_lover") and getattr(store, "_recording_active", False):
            bonus += 2

        girl.Lust = min(100, girl.Lust + base + bonus)

    def _calc_orgasm_intensity(girl, act_type=None):
        intensity = 1
        org_count = store._session_orgasms_by_girl.get(girl.gid, 0)
        denial = getattr(store, "_edge_denial_count", 0)

        if store._hard_cum_ready:
            intensity = 3
        elif denial >= 2:
            intensity = max(intensity, 3)
        elif denial >= 1:
            intensity = max(intensity, 2)

        if org_count >= 2:
            intensity = max(intensity, 3)
        elif org_count >= 1:
            intensity = max(intensity, 2)

        if act_type and getattr(girl, "FavoriteAct", None) == act_type:
            intensity = min(3, intensity + 1)

        if girl.has_trait("cum_slut"):
            intensity = min(3, intensity + 1)
        if girl.has_trait("exhibitionist") and _is_public_location():
            intensity = min(3, intensity + 1)

        stamina = getattr(girl, "Stamina", 10)
        if stamina <= 2:
            intensity = min(3, intensity + 1)

        print("[ORGASM_INTENSITY] %s tier=%d act=%s org_count=%d denial=%d hard=%s stamina=%d" % (girl.gid, intensity, act_type, org_count, denial, store._hard_cum_ready, stamina))
        return intensity

    def _orgasm_lust_floor(girl):
        org_count = store._session_orgasms_by_girl.get(girl.gid, 0)
        stamina = getattr(girl, "Stamina", 10)
        floor = (org_count * 10) + max(0, (5 - stamina) * 5)
        floor = min(50, max(0, floor))
        print("[ORGASM_FLOOR] %s org_count=%d stamina=%d floor=%d" % (girl.gid, org_count, stamina, floor))
        return floor

    def _should_trigger_nonscene_orgasm(girl):
        if girl.Lust < 100:
            return False
        if _girl_in_sex_scene(girl):
            return False
        return True

    # Personality: a bonus / penalty on her consent to be filmed (Gwen was filmed day and night once). Never for a
    # camera_lover; a camera_hater adds it to her own -700. The NTW does NOT notice hidden cameras (author).
    GIRL_RECORDING_BONUS = {"gwen": -150, "shion": -300}   # Shion: one video would end a CEO

    def recording_consent_check(girl, position=None):
        """
        Tiered consent check for recording.
        Returns dict with:
          - "accepted": True if any tier passed (backward compat)
          - "result": "accepted" | "face_hidden_only" | "denied"
          - "face_hidden": False (full) | True (forced) | None (denied)
        Tier 1 (T=800): full face recording
        Tier 2 (T=600): she agrees only if face is hidden
        """
        bonus = 0

        if girl.has_trait("camera_lover"):
            bonus += 500

        if girl.has_trait("camera_hater"):
            bonus -= 700

        _rec_persona = GIRL_RECORDING_BONUS.get(getattr(girl, "gid", None), 0)
        if _rec_persona and not girl.has_trait("camera_lover"):
            bonus += _rec_persona
            print("[PERSONA] %s recording consent %+d (her story with cameras)" % (girl.gid, _rec_persona))

        if position in _ANAL_SCENE_TYPES:
            bonus -= 150

        if girl.has_trait("lesbian"):
            bonus -= 500

        vids = getattr(store.Player, "recorded_videos", [])
        prev_consensual = sum(1 for v in vids if v.get("girl_gid") == girl.gid and v.get("consensual", False))
        bonus += min(125, prev_consensual * 25)

        _full = ApprovalCheck(
            girl=girl, T=800, Type="LOI",
            Spread=160, Bonus=bonus, Variation=40, ReturnData=True,
        )
        if _full["accepted"]:
            _full["result"] = "accepted"
            _full["face_hidden"] = False
            return _full

        _no_hide_positions = ("tj", "fj", "rj")   # no hide-face art
        _pose_map = {"bj": "blowjob", "hj": "handjob", "masturbate": "laying_down"}
        _can_hide = scene_has_hide_face(girl.gid, _pose_map.get(position, position))
        if position not in _no_hide_positions and _can_hide:
            _hidden = ApprovalCheck(
                girl=girl, T=600, Type="LOI",
                Spread=160, Bonus=bonus, Variation=40, ReturnData=True,
            )
            if _hidden["accepted"]:
                _hidden["result"] = "face_hidden_only"
                _hidden["face_hidden"] = True
                return _hidden

        _full["result"] = "denied"
        _full["face_hidden"] = None
        return _full

    def _tag_coercion_on_vid(vid):
        _ct = getattr(store, "_coercion_type", None)
        if _ct in ("blackmail", "financial"):
            vid["coerced"] = _ct
            store._recorded_during_coercion = True
            print("[REC_COERCE] tagged vid: girl=%s type=%s coerced=%s" % (vid.get("girl_gid"), vid.get("type"), _ct))

    def _add_creampie_video(girl):
        """Add a separate creampie video entry alongside the original sex video.
        Reads store._creampie_consent and store._girl_requested_creampie to
        determine the girl's reaction:
            'loved'    - she begged for it
            'accepted' - she consented
            'angry'    - forced / she didn't want it
        Also marks anal_creampie=True when the original scene was anal.
        """
        vids = getattr(store.Player, "recorded_videos", [])
        # Find the original recording to copy its metadata
        for v in reversed(vids):
            if v.get("girl_gid") == girl.gid and v.get("type") in ("cowgirl", "reverse_cowgirl", "reverse_cowgirl_anal", "doggy", "anal", "laying_down", "laying_anal", "full_nelson", "full_nelson_anal"):
                # Determine reaction from session state
                _requested = getattr(store, "_girl_requested_creampie", False)
                _consent = getattr(store, "_creampie_consent", "denied")
                if _requested:
                    _reaction = "loved"
                elif _consent in ("allowed", "changed_mind"):
                    _reaction = "accepted"
                else:
                    _reaction = "angry"

                creampie_vid = {
                    "girl_gid": v["girl_gid"],
                    "type": "creampie",
                    "location": v.get("location", CurrentLocation),
                    "committed": v.get("committed", False),
                    "consensual": v.get("consensual", True),
                    "reaction": _reaction,
                    "hd": v.get("hd", False),
                    "face_hidden": v.get("face_hidden", True),
                    # her discovery stage as the load lands (the recording's was taken before it)
                    "snapshot": dict(v.get("snapshot", {}), discovering=trait_discovery_state(girl)),
                }
                # Mark anal creampies for distinct video reactions (any anal position: FN / laying anal too)
                if v.get("type") in _ANAL_SCENE_TYPES:
                    creampie_vid["anal_creampie"] = True
                vids.append(creampie_vid)
                break

    def CumPermissionCheck(girl, action):
        """
        Check if girl allows the cum action.
        Uses ApprovalCheck with CUM_PERMISSION_RULES + dynamic bonuses
        from raw_sex_count and CreampieCounts.
        Traits: cum_slut gets huge bonus for inside/mouth, hate_cum gets penalty.
        Returns ApprovalCheck result dict (ReturnData=True).
        """
        # her step locks it (story_steps.rpy): she refuses whatever her stats
        _story_lock = story_lock_result(girl, action)
        if _story_lock:
            store._ntr_creampie_gate_result = None
            return _story_lock
        cfg = {"T": 900, "Type": "LOI", "Spread": 180, "Variation": 50}
        default_block = CUM_PERMISSION_RULES.get("_default", {})
        if action in default_block:
            cfg.update(default_block[action])

        gid = getattr(girl, "gid", None) or getattr(girl, "Id", None)
        if gid:
            girl_block = CUM_PERMISSION_RULES.get(str(gid).lower(), {})
            if girl_block and action in girl_block:
                cfg.update(girl_block[action])

        _raw_count = getattr(girl, "raw_sex_count", 0)
        _cream_count = getattr(girl, "CreampieCounts", 0)

        # Progressive trust from raw sex history (slow ramp)
        raw_bonus = min(200, _raw_count * 20)
        cream_bonus = min(200, _cream_count * 40)
        total_bonus = raw_bonus + cream_bonus

        # --- No raw history penalty ---
        # If she's never had raw sex with the player, she's far less likely
        # to accept cum inside / condom removal on first try
        # (anal_ask uses its own OI formula, but still penalizes first-timers)
        if action in ("cum_inside_ask", "cum_inside_anal_ask", "cum_remove_condom_ask", "condom_remove_midscene"):
            if _raw_count == 0:
                total_bonus -= 350  # huge barrier... never gone raw
            elif _raw_count < 3:
                total_bonus -= 150  # still hesitant... only done it a few times

        # --- ATM extra penalty: cum in mouth coming from anal is much harder ---
        if action == "cum_in_mouth_from_anal_ask":
            _atm_count = getattr(girl, "_atm_count", 0)
            if _atm_count == 0:
                total_bonus -= 300  # first ATM ever: huge disgust barrier
            elif _atm_count < 3:
                total_bonus -= 100  # still not used to it
            # Experience ramp
            total_bonus += min(_atm_count * 60, 250)

        # --- Trait: cum_slut ---
        # Loves cum inside/mouth, hates condoms
        if girl.has_trait("cum_slut"):
            if action == "cum_in_mouth_from_anal_ask":
                total_bonus += 400  # loves it, ATM is kinky to her
            elif action in ("cum_inside_ask", "cum_inside_anal_ask", "cum_in_mouth_ask"):
                total_bonus += 500  # massive bonus... wants it (offsets no-raw penalty)
            elif action in ("cum_remove_condom_ask", "condom_remove_midscene"):
                total_bonus += 450  # hates condoms, happy to remove

        # --- Trait: hardcore_sex ---
        # More willing to accept cum inside, but not an auto-override
        if girl.has_trait("hardcore_sex"):
            if action == "cum_in_mouth_from_anal_ask":
                total_bonus += 300  # kinky enough to accept ATM
            elif action in ("cum_inside_ask", "cum_inside_anal_ask", "cum_in_mouth_ask"):
                total_bonus += 200  # comfortable with it but still needs trust
            elif action in ("cum_remove_condom_ask", "condom_remove_midscene"):
                total_bonus += 150

        # --- Trait: cute_sex ---
        # Disgusted by ATM specifically
        if girl.has_trait("cute_sex"):
            if action == "cum_in_mouth_from_anal_ask":
                total_bonus -= 300  # absolutely disgusted

        # --- Trait: hate_cum ---
        # Hates cum contact, strongly prefers condoms.
        # Progressive raw/cream bonuses are capped for hate_cum so she never
        # "gets used to it" — the penalty stays dominant regardless of history.
        if girl.has_trait("hate_cum"):
            if action == "cum_in_mouth_from_anal_ask":
                total_bonus -= 500  # disgusting + hates cum = nuclear rejection
            elif action in ("cum_inside_ask", "cum_inside_anal_ask", "cum_in_mouth_ask"):
                total_bonus -= 400  # really doesn't want it
            elif action in ("cum_remove_condom_ask", "condom_remove_midscene"):
                total_bonus -= 500  # absolutely wants the condom on
            # Clamp progressive bonuses so they never overcome the hate_cum penalty
            _max_prog = 150  # raw + cream combined can add at most 150 for hate_cum
            _current_prog = raw_bonus + cream_bonus
            if _current_prog > _max_prog:
                total_bonus -= (_current_prog - _max_prog)

        # --- Condom broke, she can see the evidence ---
        if action == "condom_break_accept":
            total_bonus += 100
            if girl.has_trait("cum_slut"):
                total_bonus += 450
            elif girl.has_trait("hardcore_sex"):
                total_bonus += 200
            elif girl.has_trait("hate_cum"):
                total_bonus -= 300
            elif girl.has_trait("cute_sex"):
                total_bonus -= 100

        # --- Trait: anal_lover ---
        if girl.has_trait("anal_lover"):
            if action == "cum_inside_anal_ask":
                total_bonus += 300
            elif action == "cum_in_mouth_from_anal_ask":
                total_bonus += 200

        # --- Trait: anal_hater ---
        if girl.has_trait("anal_hater"):
            if action == "cum_inside_anal_ask":
                total_bonus -= 200
            elif action == "cum_in_mouth_from_anal_ask":
                total_bonus -= 200

        # --- Pregnancy: pill / pregnancy traits / already pregnant (values live in pregnancy.rpy) ---
        if callable(globals().get("fert_cum_permission_bonus", None)):
            total_bonus += fert_cum_permission_bonus(girl, action)

        # --- NTR Boundary: creampie gate (levels 1-3 forbid creampie) ---
        store._ntr_creampie_gate_result = None
        if action in ("cum_inside_ask", "cum_inside_anal_ask"):
            if hasattr(girl, "has_npc_partner") and girl.has_npc_partner():
                _npc_cum = get_npc_partner_for(girl)
                if _npc_cum and getattr(_npc_cum, "_ntr_active", False) and getattr(girl, "_ntr_boundary_discovered", False):
                    _bl_cum = getattr(_npc_cum, "_ntr_boundary_level", 1)
                    if _bl_cum <= 3:
                        _ntr_cum_check = _ntr_girl_boundary_check(girl, "creampie")
                        if _ntr_cum_check["outcome"] == "respect":
                            total_bonus -= 800
                            store._ntr_creampie_gate_result = "respect"
                        elif _ntr_cum_check["outcome"] == "guilty_allow":
                            total_bonus -= 200
                            store._ntr_creampie_gate_result = "guilty_allow"
                        else:
                            total_bonus += 100
                            store._ntr_creampie_gate_result = "eager_allow"
                        print("[NTR_CUM_GATE] %s action=%s bl=%d check=%s bonus_mod applied" % (
                            girl.gid, action, _bl_cum, _ntr_cum_check["outcome"]))

        return ApprovalCheck(
            girl=girl,
            T=cfg["T"],
            Type=cfg["Type"],
            Spread=cfg["Spread"],
            Bonus=total_bonus,
            Variation=cfg.get("Variation", 0),
            ReturnData=True,
        )

    def apply_cum_penalties(girl, rule_name, scene_type=None):
        """Apply stat penalties from CUM_PENALTY_RULES via Change_Status.
        hate_cum: extra Love loss, extra Obed gain (submits but hates it).
        cum_slut: reduced penalties (she secretly liked it).
        anal_lover + anal scene: no Love penalty (she wanted cum in her ass).
        """
        rule = CUM_PENALTY_RULES.get(rule_name, {})
        _is_anal_scene = scene_type in _ANAL_SCENE_TYPES
        _anal_lover_anal = _is_anal_scene and girl.has_trait("anal_lover") and rule_name == "cum_inside_forced"
        for stat, amount in rule.items():
            mod = amount
            if girl.has_trait("hate_cum"):
                if stat == "Love":
                    mod = int(amount * 1.5)  # extra Love loss
                elif stat == "Obed":
                    mod = int(abs(amount) * 0.5)  # gains Obed instead of losing it
            elif _anal_lover_anal:
                if stat == "Love":
                    mod = 0  # she wanted it, no Love penalty
                elif stat == "Obed":
                    mod = abs(amount)
            elif girl.has_trait("cum_slut"):
                if stat == "Love":
                    mod = int(amount * 0.3)  # barely upset
                elif stat == "Obed":
                    mod = abs(amount)  # no penalty, slight gain
            Change_Status(girl, stat, mod)
        # hate_cum: bonus Obed for being forced into it
        if girl.has_trait("hate_cum"):
            Change_Status(girl, "Obed", 25)

    def apply_cum_bonuses(girl, rule_name):
        """Apply stat bonuses from CUM_BONUS_RULES via Change_Status.
        cum_slut: extra Lust and Inbt from cum events.
        """
        rule = CUM_BONUS_RULES.get(rule_name, {})
        for stat, amount in rule.items():
            mod = amount
            if girl.has_trait("cum_slut"):
                if stat == "Inbt":
                    mod = int(amount * 1.8)  # loves it
            Change_Status(girl, stat, mod)
        # Track consented creampies separately
        if rule_name in ("cum_inside_allowed", "condom_removed_allowed"):
            girl.ConsentedCreampies = getattr(girl, "ConsentedCreampies", 0) + 1
        # cum_slut: gains Lust from cum events
        if girl.has_trait("cum_slut"):
            if rule_name in ("cum_inside_allowed", "condom_removed_allowed", "cum_in_mouth_allowed"):
                girl.Lust = min(100, getattr(girl, "Lust", 0) + 20)
            else:
                girl.Lust = min(100, getattr(girl, "Lust", 0) + 8)

    # ---------------------------------------------------------
    # Angry reason narration... context hints for the player
    # ---------------------------------------------------------
    ANGRY_NARRATION = {
        "forced_creampie": [
            _("Maybe you shouldn't have cum inside her... Or maybe you should try again once she calms down?"),
            _("She's furious about what you did. Give her some time... she might forgive you eventually."),
            _("Forcing yourself inside someone who hates it tends to have consequences. Wait it out."),
        ],
        "marital_bed_no_energy": [
            _("She expected more from you. A lot more. Maybe hit the gym before next time."),
        ],
    }

    def get_angry_narration(girl):
        """Return a narration hint based on the girl's angry reason."""
        reason = girl.get_temp_status_reason("angry") if hasattr(girl, "get_temp_status_reason") else None
        if reason and reason in ANGRY_NARRATION:
            # translated here: every caller shows it as is ("[_angry_narr]", renpy.say)
            return _tl(renpy.random.choice(ANGRY_NARRATION[reason]))
        return None

    def _hide_condom_layer():
        """Hide condom visual layer for all scene types."""
        renpy.hide("cowgirl_condom")
        renpy.hide("cowgirl_condom_broken")
        renpy.hide("rcg_condom")
        renpy.hide("dg_condom")
        renpy.hide("fn_condom")
        renpy.hide("ld_condom")

    def _cheat_lets_condom_go(girl):
        """Cheat path before her breaking point: the condom only comes off past this stat gate (same gate as
        CondomMidsceneMenu). Off the cheat path, or once she broke, it always may.
        Read by _on_condom_removed and by the post-cum "Ask to go raw" choice (_post_cum_condom_menu)."""
        if not _is_on_cheat_path(girl) or getattr(girl, "_cheat_broke", False):
            return True
        _heat = getattr(girl, "_cheat_heat", 0)
        return (
            (_heat >= 80 and getattr(girl, "Obed", 0) >= 500 and getattr(girl, "Inbt", 0) >= 300)
            or (_heat >= 90 and getattr(girl, "Lust", 0) >= 80)
            or girl.has_trait("cum_slut")
        )

    def _on_condom_removed(girl, skip_hide=False, force=False):
        """Called when condom is successfully removed mid-scene.
        Returns True if blocked (her story step, cheat path), False if removal proceeded.
        force=True skips the cheat path block (girl-initiated removal), never her story step."""
        # Her step locks going raw (story_steps.rpy "raw"): every way here asks it first, this only catches a path
        # that did not (the condom stays on whoever asked, she says no)
        if story_act_locked(girl, "raw"):
            print("[STORY] condom removal BLOCKED: %s's step %d locks raw (a caller that skipped the step gate)" % (
                girl.gid, story_step(girl)))
            set_scene_expression(girl, "angry")
            Say_Line(girl, story_locked_line(girl, "raw"))
            return True
        # All cheat paths: condom removal blocked until breaking point
        # UNLESS stats are high enough (_cheat_lets_condom_go)
        if not force and _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False):
            if not _cheat_lets_condom_go(girl):
                _cep = getattr(girl, "_cheat_escalation_path", 0)
                if _cep == 1:
                    Say_Line(girl, _cheat_line(girl, renpy.random.choice(_PATH1_CONDOM_BLOCK)))
                elif _cep == 2:
                    _p2_block = [
                        _("No! I'm still in control! The condom STAYS on!"),
                        _("Don't you DARE! I decide when it comes off! Not you!"),
                        _("I said condom STAYS! I'm not losing control like that!"),
                    ]
                    Say_Line(girl, _cheat_line(girl, renpy.random.choice(_p2_block)))
                else:
                    _p3_block = [
                        _("No! I'm getting revenge, not being RECKLESS!"),
                        _("The condom stays! He doesn't deserve the full betrayal yet!"),
                        _("Keep it ON! I'm mad at him, not suicidal!"),
                    ]
                    Say_Line(girl, _cheat_line(girl, renpy.random.choice(_p3_block)))
                return True
        store.condom_active = False
        if not skip_hide:
            _hide_condom_layer()
        # Save blood/cum state for position-specific CondomRemoveAnim
        store._cr_had_blood = store._ld_blood_active
        store._cr_had_cum = store._ld_cum_dick_level
        if store._cr_had_blood or store._cr_had_cum:
            print("[CONDOM_REMOVE] cleanup pending: blood=%s cum_level=%d inside=%d condom=%d" % (store._cr_had_blood, store._cr_had_cum, store._session_cum.get("inside", 0), store._session_cum.get("condom", 0)))
        # Reset state flags (LD_ApplySpeed won't re-show after anim)
        store._ld_blood_active = False
        store._ld_cum_dick_level = 0
        store._session_cum.pop("inside", None)
        store._session_cum.pop("condom", None)
        store._forced_creampie_count = 0
        # No position-specific anim: hide layers directly
        if not skip_hide:
            renpy.hide("ld_blood_penis")
            renpy.hide("ld_blood_anim")
            renpy.hide("ld_blood_static")
            renpy.hide("ld_cum_dick")
            renpy.hide("ld_cum_creampie_2")
            renpy.hide("ld_cum_creampie_3")
        _track_raw_sex_start(girl)
        store._condom_removed_midscene = True
        # Split recording: condom video stays, new raw video starts
        if getattr(store, "_recording_active", False) and getattr(store, "_recording_girl", None) is girl:
            _vids = getattr(store.Player, "recorded_videos", [])
            for _v in reversed(_vids):
                if _v.get("girl_gid") == girl.gid and _v.get("condom", False):
                    _raw_vid = dict(_v)
                    _raw_vid["condom"] = False
                    _vids.append(_raw_vid)
                    break

    # ---------------------------------------------------------
    # Session cum tracker
    # ---------------------------------------------------------
    def session_cum_reset():
        """Reset session cum tracker. Call when entering sex_menu."""
        store._session_cum = {}
        store._session_loads_by_girl = {}
        # NTR creampie presence flags share the lifetime of _session_cum (_ntr_creampie_check reads both)
        store._ntr_creampie_witnessed_gid = None
        store._ntr_session_watcher_gid = None
        # Safety net: scenes that end without CumCleanupMenu (angry ends via force_scene_reset,
        # events, dares) used to drop their pregnancy risks here without ever rolling them.
        if getattr(store, "_scene_pregnancy_risks", None) and callable(globals().get("_process_pregnancy_rolls", None)):
            print("[PREGNANCY] session_cum_reset: %d unprocessed risk(s), rolling now" % len(store._scene_pregnancy_risks))
            _process_pregnancy_rolls()
        store._scene_pregnancy_risks = []
        if callable(globals().get("_scene_marks_reset", None)):
            _scene_marks_reset()   # new sex session: act / position counters may go up again
        store._forced_creampie_count = 0
        store._forced_creampie_end_after_orgasm = False
        store._atm_session_count = 0
        store._atm_tease_played = False
        store._atm_cum_in_mouth = False
        store._atm_source_gid = None
        store._edge_denial_count = 0
        store._hard_cum_ready = False
        store._stop_continue_count = 0
        store._cheat_gate_heat_given = set()
        store._ntr_tip_accepted = False
        store._condom_rip_attempted = False

    # ---------------------------------------------------------
    # ATM (ass to mouth): the ONE registration point
    # ---------------------------------------------------------
    def atm_register(girl, source_gid=None, where="?"):
        """She takes it in her mouth right after it was in an ass. EVERY ATM path calls this and nothing else
        touches the ATM counters (cum menu, doggy tip menu, sex_menu "Blowjob" after anal).
          girl       = the girl whose MOUTH it goes into. Only HER history moves: _atm_count, Firsts["atm"].
          source_gid = whose ass it was in. None or her own gid = same-girl ATM. Another gid = threesome cross
                       ATM: that girl only had anal (mark_intimacy already counted it), nothing moves for her.
        Opens the ATM context (_atm_cum_in_mouth / _atm_source_gid) and counts ONCE per scene: the mark lives in
        _scene_marks() (same bookkeeping as "sex" / "anal"), wiped by scene_full_cleanup() and
        session_cum_reset(). A second call inside the same scene is a no-op, the next scene counts again.
        Firsts["cum_mouth"] is NOT written here: process_cum() does it when the cum really lands in her mouth.
        Returns True when this call counted."""
        if girl is None:
            return False
        _src = source_gid or girl.gid
        _cross = (_src != girl.gid)
        store._atm_cum_in_mouth = True
        store._atm_source_gid = _src
        if _scene_act_marked(girl, "atm"):
            print("[ATM] register %s (where=%s): already counted this scene, skipped" % (girl.gid, where))
            return False
        _scene_marks().add((girl.gid, "atm"))
        girl._atm_count = getattr(girl, "_atm_count", 0) + 1
        store._atm_session_count = getattr(store, "_atm_session_count", 0) + 1
        _firsts = getattr(girl, "Firsts", None)
        if _firsts is None:
            girl.Firsts = {}
            _firsts = girl.Firsts
        if "atm" not in _firsts:
            _firsts["atm"] = "before_kiss" if "kiss" not in getattr(girl, "intimacy_flags", set()) else "normal"
        # Video tag: every reader of vid["atm"] (BigFans captions, video reactions) says it was HER OWN ass
        if not _cross:
            store._recording_had_atm = True
        unlock_achievement("acquired_taste")
        print("[ATM] register %s (where=%s): src=%s cross=%s count=%d session=%d firsts_atm=%s rec_pending=%s" % (
            girl.gid, where, _src, _cross, girl._atm_count, store._atm_session_count,
            _firsts.get("atm"), getattr(store, "_recording_had_atm", False)))
        _watcher_scene_comment("atm")
        return True

    def _threesome_switch_cleanup(girl):
        """Light cleanup for threesome girl switch.
        Hides scene layers and resets position state, but does NOT
        restore outfit, clear cum, or wipe sprite_state globally."""
        debug_log("[THREESOME] switch_cleanup: hiding scene for %s" % girl.gid)

        # Clear scene-girl refs so _girl_in_sex_scene returns False
        for var in SCENE_GIRL_VARS:
            ref = getattr(store, var, None)
            if ref is not None and (ref is girl or getattr(ref, "gid", None) == girl.gid):
                setattr(store, var, None)

        # Stop blink/expression threads
        store._bj_cheeks_running = False
        store._bj_blink_running = False

        # Hide all sex scene overlay layers
        _hide_all_scene_layers(girl)
        for _extra in ("spank_hand", "bj_slap", "touch_zoom"):
            renpy.hide(_extra)

        # Reset position-specific state
        store.rcg_rub_mode = False
        store.rcg_tip_mode = False
        store.rcg_grab = False
        store.rcg_started = False
        store.rcg_arms_pose = 1
        store.cowgirl_rub_mode = False
        store.cowgirl_tip_mode = False
        store.cowgirl_started = False
        store.condom_active = False
        condom_break_reset()
        stealth_condom_reset()
        store.titjob_started = False
        store.titjob_arms_pose = 1
        store.doggy_blink = False
        store.doggy_started = False
        store.doggy_anal = False
        store.doggy_rub_mode = False
        store.doggy_tip_mode = False
        store.doggy_grab = False

    def _threesome_cleanup_watcher(watcher):
        """Cleanup for a threesome watching girl on session exit.
        Restores outfit, clears cum, refreshes standing sprite.
        Does NOT hide or relocate -- caller handles that."""
        debug_log("[THREESOME] cleanup_watcher: %s" % watcher.gid)
        if hasattr(watcher, "Cum"):
            watcher.Cum = []
            watcher._mouth_cum_persist = False
        if getattr(watcher, "_saved_outfit", None):
            watcher.RestoreOutfit(clear_saved=True)
        set_girl_sprite(watcher.gid, pose="standing", at_list=[slot_right])

    def _record_threesome_history():
        """Record Girl_history for all threesome participants. Call once on session exit."""
        _ts_parts = list(getattr(store, "_threesome_participants", set()))
        if len(_ts_parts) < 2:
            store._threesome_participants = set()
            return
        for _i, _gid_a in enumerate(_ts_parts):
            for _gid_b in _ts_parts[_i+1:]:
                _ga = _resolve_girl(_gid_a)
                _gb = _resolve_girl(_gid_b)
                if _ga and _gb:
                    record_girl_interaction(_ga, _gb, "threesome", shared_player=True)
                    debug_log("[THREESOME] Recorded history: %s <-> %s" % (_gid_a, _gid_b))
        store._threesome_participants = set()

    def _active_girl_allows_threesome(active_girl, watcher):
        """Check if the active girl is open to a threesome with the watcher.
        Returns 'allow', 'watch_only', or 'refuse'."""
        if active_girl.has_trait("polyamorous"):
            debug_log("[THREESOME] active_girl %s auto-allow (poly/polyamorous)" % active_girl.gid)
            return "allow"
        if active_girl.has_trait("virgin"):
            debug_log("[THREESOME] active_girl %s auto-refuse (virgin)" % active_girl.gid)
            return "refuse"

        _score = 0

        if active_girl.has_trait("exhibitionist"):
            _score += 200
        if active_girl.has_trait("cheater"):
            _score += 150
        if active_girl.has_trait("hardcore_sex"):
            _score += 150
        if active_girl.has_trait("cum_slut"):
            _score += 100
        if active_girl.has_trait("voyeur"):
            _score += 50
        if active_girl.has_trait("loyal"):
            _score -= 200
        if active_girl.has_trait("cute_sex"):
            _score -= 150
        if active_girl.has_trait("public_shy"):
            _score -= 100

        _like = active_girl.get_like_for(watcher.gid)
        if _like >= 700:
            _score += 150
        elif _like >= 500:
            _score += 50
        elif _like < 200:
            _score -= 200

        _lust = getattr(active_girl, "Lust", 0)
        _score += int(_lust * 3)

        if active_girl.is_dating_player() and not is_harem_exempt(active_girl, watcher):
            _score -= 250

        debug_log("[THREESOME] active_girl_allows: %s score=%d (like=%d lust=%d dating=%s harem_exempt=%s)" % (active_girl.gid, _score, _like, _lust, active_girl.is_dating_player(), is_harem_exempt(active_girl, watcher) if active_girl.is_dating_player() else "n/a"))

        if _score >= 300:
            return "allow"
        elif _score >= 0:
            return "watch_only"
        else:
            return "refuse"

    _AG_THREESOME_LINES = {
        "allow": {
            "exhibitionist": [
                _("Mmm, an audience? I'm not complaining."),
                _("Let her watch. I like being seen."),
            ],
            "cheater": [
                _("She can stay. Makes things more interesting."),
            ],
            "hardcore_sex": [
                _("Fine. Let her watch."),
            ],
            "polyamorous": [
                _("The more the merrier~"),
            ],
            "cum_slut": [
                _("Let her watch. I don't care who sees."),
            ],
            "_default": [
                _("I guess it's fine if she stays."),
                _("Whatever... she can stay."),
            ],
        },
        "watch_only": {
            "loyal": [
                _("Don't even think about it. This is between us."),
            ],
            "cute_sex": [
                _("Please, no... this is already embarrassing enough..."),
            ],
            "public_shy": [
                _("I can't... not with someone watching like that."),
            ],
            "_dating": [
                _("She can watch, but you're mine. Got it?"),
            ],
            "_default": [
                _("She can watch, I guess. But nothing more."),
            ],
        },
        "refuse": {
            "loyal": [
                _("This is private. Tell her to leave. Now."),
            ],
            "cute_sex": [
                _("I can't do this with her here... please make her go!"),
            ],
            "public_shy": [
                _("No! Get her out! I can't have anyone see this!"),
            ],
            "_dating": [
                _("Get her out of here. You're mine, and she's not watching."),
            ],
            "_default": [
                _("I don't want her here. Ask her to leave."),
            ],
        },
    }

    _AG_THREESOME_WATCHER_KICKED = [
        _("Fine... I'll go."),
        _("Okay, okay. I'm leaving."),
        _("Sorry. I didn't mean to intrude."),
    ]

    # ── Threesome: jealous watcher commentary (fires during the scene) ──
    # scene_type (as passed to scene_moan_tick) -> line group
    _TS_JEAL_SCENE_MAP = {
        "hj": "hj",
        "bj": "bj",
        "tj": "tj",
        "rub": "rub",
        "cowgirl": "ride",
        "reverse_cowgirl": "ride",
        "doggy": "fuck",
        "full_nelson": "fuck",
        "anal": "anal",
        "full_nelson_anal": "anal",
        "laying_down": "laying_down",
        "laying_anal": "anal",
        "reverse_cowgirl_anal": "anal",
    }

    # Jealousy 300-599: she wants a turn (envious)
    _TS_JEAL_WANT_LINES = {
        "hj": [
            _("Look at how she strokes you... I want my hands on you too..."),
            _("My hands are getting restless just from watching... save some for me."),
            _("I keep imagining it's MY hand on you right now..."),
        ],
        "bj": [
            _("I want to taste you too... don't you dare finish in her mouth."),
            _("My mouth is watering just from watching this..."),
            _("She gets your cock and I just get to watch? I want a turn..."),
        ],
        "tj": [
            _("I want you between MY tits too..."),
            _("Watching her use her chest like that... come here, I want that too."),
            _("My turn next... I want to feel you sliding between mine."),
        ],
        "rub": [
            _("Stop teasing her and come tease ME..."),
            _("Even watching this is driving me crazy... I want that too."),
            _("You better have some energy left for me..."),
        ],
        "ride": [
            _("I want to ride you too... don't let her wear you out."),
            _("Watching her bounce on you like that... I can't stand it, I want my turn."),
            _("Save some of that for me... I want to be on top of you too."),
        ],
        "fuck": [
            _("I want you inside me too... hurry up..."),
            _("Watching you take her like that... I need that too. I NEED it."),
            _("Don't you dare finish before I get mine..."),
        ],
        "anal": [
            _("You're doing THAT with her?... I want to try it too..."),
            _("I can't believe I'm jealous of her ass... you're coming to me after this."),
            _("If she gets that, then I get that too. Understood?"),
        ],
    }

    # Jealousy 600+: she claims she does it better than the active girl
    _TS_JEAL_BETTER_LINES = {
        "hj": [
            _("Her hands? Please. Mine would have you shaking by now."),
            _("%s strokes you like she's scared of it. Give it here, I'll show her how it's done."),
            _("I know exactly how you like it. Better than SHE ever will."),
        ],
        "bj": [
            _("That's how %s sucks you? Cute. I can do things she's never even heard of."),
            _("Look at your face... that's not even close to what MY mouth does to you."),
            _("When she's done playing, I'll show you what a real blowjob feels like."),
        ],
        "tj": [
            _("Hers? Really? Mine feel ten times better and you know it."),
            _("%s is trying so hard... I don't even have to try to beat that."),
            _("Come put it between mine and then tell me who does it better."),
        ],
        "rub": [
            _("She calls that teasing? I'd have you begging in half the time."),
            _("Watch and learn, %s. Actually no... MY turn, YOU watch."),
            _("You're wasting your energy on an amateur..."),
        ],
        "ride": [
            _("%s rides you like it's her first time. I'd have you finished already."),
            _("Is that as fast as she can go? Pathetic. Put me on top."),
            _("You always moan louder when I ride you. Don't think I haven't noticed."),
        ],
        "fuck": [
            _("She just lies there and takes it. I actually move. Big difference."),
            _("%s can barely handle you at that speed. I'd be begging for MORE."),
            _("When you're done with her, come fuck a REAL woman."),
        ],
        "anal": [
            _("Her ass has got NOTHING on mine and we both know it."),
            _("%s can barely take it. I was built for that."),
            _("Enjoy the appetizer. The main course is sitting right here."),
        ],
    }

    def _ts_watcher_jealousy_tick(active_girl, scene_type):
        """During a threesome, a jealous GF watching her turn throws envious lines.
        Jealousy >= 300: she wants a turn. >= 600: she claims she does it better.
        Called from scene_moan_tick (universal per-tick hook in every position loop).
        Returns True if a line fired (caller skips this tick's moan)."""
        if not getattr(store, "_threesome_mode", False):
            return False
        if not getattr(store, "_witness_watching", False):
            return False
        _w = getattr(store, "_witness_girl", None)
        if _w is None or active_girl is None or _w.gid == active_girl.gid:
            return False
        if not (hasattr(_w, "is_dating_player") and _w.is_dating_player()):
            return False
        _jeal = getattr(_w, "Jealousy", 0)
        if _jeal < 300:
            return False
        _group = _TS_JEAL_SCENE_MAP.get(scene_type)
        if _group is None:
            return False
        store._ts_jeal_comment_cd = max(0, getattr(store, "_ts_jeal_comment_cd", 0) - 1)
        if store._ts_jeal_comment_cd > 0:
            return False
        if renpy.random.random() >= 0.20:
            return False
        # 600+: mostly competitive "I do it better"; otherwise envious wanting
        if _jeal >= 600 and renpy.random.random() < 0.70:
            _pool = _TS_JEAL_BETTER_LINES.get(_group)
            _expr = "angry"
            _tier = "better"
        else:
            _pool = _TS_JEAL_WANT_LINES.get(_group)
            _expr = "lipbite"
            _tier = "want"
        if not _pool:
            return False
        _line = _tl(renpy.random.choice(_pool))
        if "%s" in _line:
            _line = _line % active_girl.Name
        set_scene_expression(_w, _expr)
        Say_Line(_w, _line)
        store._ts_jeal_comment_cd = 5
        print("[TS_JEALOUSY] watcher %s commented on %s (jeal=%d group=%s tier=%s)" % (_w.gid, active_girl.gid, _jeal, _group, _tier))
        return True

    # ── Threesome: end-of-session satisfaction reaction (only one girl came) ──
    _TS_UNSAT_LINES = {
        "hardcore_sex": [
            _("Are you SERIOUS?! You made %s cum and I get NOTHING?!"),
            _("%s got hers and I'm just supposed to smile about it? Screw you."),
            _("Unbelievable. Next time SHE watches and I get the attention."),
        ],
        "cum_slut": [
            _("%s came and I didn't?! That's the cruelest thing you've ever done to me!"),
            _("I NEEDED that! You gave everything to %s and left me EMPTY!"),
            _("This is torture... she gets to cum and I'm left aching like this?!"),
        ],
        "cute_sex": [
            _("So... only %s gets to finish? I thought... I thought you cared about me too..."),
            _("I'm happy for %s, really, but... what about me?"),
            _("It's fine... it's fine. It's not fine. You didn't even try for me..."),
        ],
        "_default": [
            _("Wow. %s gets everything and I get to watch? Noted."),
            _("You made her cum and just... forgot about me?"),
            _("Next time it's MY turn first. I mean it."),
        ],
    }

    _TS_RIVALRY_COMEBACK_LINES = [
        _("Not my fault I'm his favorite."),
        _("Maybe if you tried harder, he'd actually notice you."),
        _("Aww, jealous? Don't worry, I'll put in a good word for you."),
        _("Some of us just know how to keep his attention."),
        _("He chose me for a reason, sweetie. Take notes."),
        _("Don't look at me like that. You wanted to share, remember?"),
    ]

    # ── Threesome: watcher commentary during sex scene events ──

    _TS_WATCHER_LINES = {
        "speed_max": {
            "cute_sex": [
                _("Oh my God... he's going that fast?! That looks like it hurts!"),
                _("I can't even watch... he's being so rough with her!"),
                _("Is she okay?! That's way too intense!"),
            ],
            "hardcore_sex": [
                _("YES! That's what I'm talking about! Don't you dare slow down!"),
                _("Now THAT'S the speed I want when it's my turn!"),
                _("Finally going all out! That's how you do it!"),
            ],
            "voyeur": [
                _("Oh wow... I can't look away from this..."),
                _("This is... I shouldn't be this turned on just watching..."),
            ],
            "virgin": [
                _("How does she take it that fast?! That looks insane!"),
                _("I could never handle that... he's going so hard!"),
            ],
            "_default": [
                _("Damn... he's really not holding back."),
                _("That's... pretty intense."),
            ],
        },
        "speed_down": {
            "hardcore_sex": [
                _("Why are you slowing down? She can handle more than that."),
                _("Come on, don't go easy on her. Pick it back up."),
                _("Boring... speed it up already."),
            ],
            "cute_sex": [
                _("Good... slow down a little. Be gentle with her."),
                _("That's better. No need to go that hard."),
            ],
        },
        "spank": {
            "cute_sex": [
                _("Did you just HIT her?! What is wrong with you?!"),
                _("Stop that! You're hurting her!"),
                _("I flinched just watching that..."),
            ],
            "hardcore_sex": [
                _("Ooh, nice one! Do it harder next time!"),
                _("She loved that, I can tell. Do it again!"),
                _("Spank ME next when it's my turn!"),
            ],
            "voyeur": [
                _("Oh... that sound... I felt that from here."),
                _("The way she reacted to that slap..."),
            ],
            "virgin": [
                _("Oh God, he hit her! Is that... normal?!"),
                _("She doesn't seem upset about it... people do this?!"),
            ],
            "_default": [
                _("Whoa... didn't expect that."),
                _("That was... intense."),
            ],
        },
        "cum_on_girl": {
            "cum_slut": [
                _("That should've been MINE! I wanted every drop!"),
                _("Seriously?! You waste it all on HER?! I'm right here!"),
                _("I can't believe you... I would've taken all of it!"),
            ],
            "hate_cum": [
                _("Ugh... how can she just let him do that?"),
                _("I'm SO glad that wasn't me. That's disgusting."),
            ],
            "cute_sex": [
                _("Oh my... that's... a lot."),
                _("Is she okay with that? That's so messy..."),
            ],
            "_default": [
                _("Well... he made his choice, I guess."),
                _("Guess it's pretty clear who he was focused on tonight."),
            ],
        },
        "creampie": {
            "cum_slut": [
                _("Inside HER?! That should've been me!"),
                _("He came inside her and not me?! That's NOT fair!"),
                _("I would've taken every single drop! Why HER?!"),
                _("You better have some left for me after all that..."),
            ],
            "hate_cum": [
                _("He just... INSIDE?! Oh my God, that's terrifying!"),
                _("Thank GOD that wasn't me... are you insane?!"),
                _("Without pulling out?! What is WRONG with you?!"),
            ],
            "cute_sex": [
                _("He finished... inside her? That's so intimate..."),
                _("Inside?! Isn't that... really dangerous?"),
            ],
            "virgin": [
                _("He came INSIDE?! Is that even safe?!"),
                _("Oh my God... he actually did it inside her..."),
            ],
            "_default": [
                _("Inside her, huh... noted."),
                _("Well, no going back from that one."),
            ],
        },
        "girl_orgasm": {
            "cum_slut": [
                _("She came and I'm just standing here watching?! This isn't fair!"),
                _("Must be nice... finishing while I don't get anything."),
            ],
            "hardcore_sex": [
                _("About time she finished! Now make ME cum."),
                _("Good for her. Now don't forget about MY turn."),
            ],
            "cute_sex": [
                _("That looked... really nice. I wish that was me..."),
                _("She seems so happy... when is it my turn?"),
            ],
            "voyeur": [
                _("Oh wow... watching her cum like that is... incredible."),
                _("The face she makes when she finishes..."),
            ],
            "_default": [
                _("She got hers... so what about me?"),
                _("Lucky her."),
            ],
        },
        "anal_enter": {
            "anal_lover": [
                _("Oh, her ass... lucky girl. I love that feeling..."),
                _("Mmm, go deeper... I wish that was me..."),
                _("Her ass is going to feel so good around you... I'm jealous."),
            ],
            "anal_hater": [
                _("In her... there? I can't even watch this..."),
                _("That looks so painful... I could never do that..."),
                _("How can she take that?! That must hurt so much..."),
            ],
            "cute_sex": [
                _("Careful... that has to hurt her... go slow..."),
                _("Are you sure about this? She looks uncomfortable..."),
                _("Be gentle... that's a really sensitive spot..."),
            ],
            "hardcore_sex": [
                _("Fuck her ass! Don't hold back!"),
                _("Push it all the way in! She can take it!"),
                _("That's right, claim that ass. Hard."),
            ],
            "_default": [
                _("Oh, you're going there... wow..."),
                _("That's bold... she seems to be handling it though."),
                _("Her ass? That's... something else."),
            ],
        },
        "atm": {
            "cum_slut": [
                _("Straight from her ass to her mouth... that's so filthy... I love it."),
                _("She actually took it in her mouth after THAT?! Oh my god..."),
                _("That's so dirty... and so hot... I can't look away..."),
            ],
            "hate_cum": [
                _("From her ASS to her MOUTH?! I'm going to throw up..."),
                _("That is the most disgusting thing I've ever seen..."),
                _("How can she put that in her mouth after... oh god no..."),
            ],
            "cute_sex": [
                _("Wait, that was just in her... oh no... spit it out!"),
                _("That's so unsanitary! How can you make her do that?!"),
                _("I can't watch this... that's so wrong..."),
            ],
            "hardcore_sex": [
                _("Ass to mouth? Now THAT'S what I call committed."),
                _("She took it like a pro. Respect."),
                _("Straight from her ass... and she didn't even flinch. Impressive."),
            ],
            "_default": [
                _("Did that just go from her... to her...? Oh my god."),
                _("That's... wow. I don't even know what to say."),
                _("I've never seen anyone do that before... she's something else."),
            ],
        },
        "recording": {
            "camera_lover": [
                _("Ooh, filming? Make sure you get my good side too!"),
                _("Are you going to film ME next? I want to be on camera!"),
                _("Recording this? Smart. Let me pose in the background..."),
            ],
            "camera_hater": [
                _("Put that camera away! What if someone sees this?!"),
                _("You're RECORDING?! I don't want to be in that video!"),
                _("Delete that! I don't want any part of this on camera!"),
            ],
            "exhibitionist": [
                _("Filming a threesome? This is going to be so hot to watch later..."),
                _("Make sure you capture everything... every angle..."),
                _("I hope someone sees this... the thought makes me so excited..."),
            ],
            "public_shy": [
                _("Oh no, not a camera... please don't point it at me..."),
                _("Can you at least keep me out of the shot?! Please?!"),
                _("If anyone ever sees this, I will literally die..."),
            ],
            "_default": [
                _("You're filming this? Really?"),
                _("A camera? I didn't agree to be in a video..."),
                _("Just... make sure my face isn't in it, okay?"),
            ],
        },
        # The WATCHER talks about the ACTIVE girl's partner: "her %(pl)s" (a bare %(pl)s reads "boyfriend is...")
        "ntr_watching": {
            "loyal": [
                _("Her %(pl)s is RIGHT THERE watching... this is so wrong..."),
                _("I feel so bad... her %(pl)s can see everything..."),
                _("How can you do this with her %(pl)s watching? Have you no shame?"),
            ],
            "cheater": [
                _("The look on %(poss)s face... this is thrilling..."),
                _("Her %(pl)s is watching... and honestly? That makes it hotter..."),
                _("Let %(po)s watch. %(Pp)s should see what %(pp)s is missing."),
            ],
            "cute_sex": [
                _("This feels so wrong with her %(pl)s here... I can't look at %(po)s..."),
                _("Her poor %(pl)s... %(pp)s shouldn't have to see this..."),
                _("Can we... not do this while %(pp)s is watching? Please?"),
            ],
            "_default": [
                _("Her %(pl)s is right there... this is so awkward..."),
                _("I keep making eye contact with her %(pl)s... this is weird..."),
                _("With her %(pl)s watching... I don't know how to feel about this."),
            ],
        },
    }

    _TS_WATCHER_CONTEXT = {
        "spank_was_spanked": {
            "cute_sex": [
                _("I know how that feels... my butt is still stinging."),
                _("Ouch... she'll feel that later. Trust me, I know."),
            ],
            "virgin": [
                _("He did the same thing to me... I guess he likes doing that."),
                _("Again? He really likes spanking, doesn't he..."),
            ],
            "_default": [
                _("Same thing he did to me..."),
                _("Yep... I know exactly how that feels."),
            ],
        },
        "girl_orgasm_already_came": {
            "cum_slut": [
                _("Good for her! ...Now I want to go again."),
                _("She came too? I still came harder though!"),
            ],
            "hardcore_sex": [
                _("Now we're even. But I bet I was louder."),
                _("Finally caught up! Took her long enough."),
            ],
            "cute_sex": [
                _("She looks so relieved... I'm glad she got to finish too."),
                _("That's nice... now we both got ours."),
            ],
            "_default": [
                _("Good... now we're even."),
                _("At least she got hers too."),
            ],
        },
        # 2nd+ creampie of the girl he is with this session (_watcher_scene_comment): "again" is true only now
        "creampie_again": {
            "cum_slut": [
                _("Again?! How many times are you going to fill HER up and not me?!"),
                _("I'm literally right here... and you keep choosing her?!"),
            ],
        },
    }

    # A watcher still discovering an eager trait speaks through "<trait>_new" (trait_line_keys); without one
    # the next trait of hers speaks. These veteran pools hold nothing she has to have lived (plain wanting /
    # jealousy / cheering), so they are her discovery pools too. Left out on purpose: the veteran lectures
    # (speed_max / speed_down hardcore_sex) and anal_enter anal_lover ("I love that feeling").
    _TS_WATCHER_LINES["anal_enter"]["anal_lover_new"] = [
        _("Mmm, go deeper... I wish that was me..."),
        _("Her ass is going to feel so good around you... I'm jealous."),
    ]
    _TS_WATCHER_LINES["spank"]["hardcore_sex_new"] = [
        _("Oh... that sound... why do I want him to do that to me?"),
        _("She liked that... I think I would too."),
    ]
    for _tsw_table, _tsw_event, _tsw_trait in (
            (_TS_WATCHER_LINES, "cum_on_girl", "cum_slut"), (_TS_WATCHER_LINES, "creampie", "cum_slut"),
            (_TS_WATCHER_LINES, "girl_orgasm", "cum_slut"), (_TS_WATCHER_LINES, "girl_orgasm", "hardcore_sex"),
            (_TS_WATCHER_LINES, "anal_enter", "hardcore_sex"), (_TS_WATCHER_LINES, "atm", "cum_slut"),
            (_TS_WATCHER_LINES, "atm", "hardcore_sex"),
            (_TS_WATCHER_CONTEXT, "girl_orgasm_already_came", "cum_slut"),
            (_TS_WATCHER_CONTEXT, "girl_orgasm_already_came", "hardcore_sex"),
            (_TS_WATCHER_CONTEXT, "creampie_again", "cum_slut")):
        _tsw_table[_tsw_event][_tsw_trait + "_new"] = _tsw_table[_tsw_event][_tsw_trait]

    _WATCHER_EVENT_EXPR = {
        "speed_max": {"cute_sex": "scared", "hardcore_sex": "smug", "voyeur": "lipbite", "_default": "surprised"},
        "speed_down": {"hardcore_sex": "angry", "cute_sex": "happy", "_default": "normal"},
        "spank": {"cute_sex": "scared", "hardcore_sex": "smug", "voyeur": "lipbite", "_default": "surprised"},
        "cum_on_girl": {"cum_slut": "angry", "hate_cum": "angry", "_default": "surprised"},
        "creampie": {"cum_slut": "angry", "hate_cum": "scared", "_default": "surprised"},
        "girl_orgasm": {"cum_slut": "angry", "hardcore_sex": "smug", "voyeur": "lipbite", "cute_sex": "sad", "_default": "sad"},
        "anal_enter": {"anal_lover": "lipbite", "anal_hater": "uncomfortable", "cute_sex": "worried", "hardcore_sex": "smug", "_default": "surprised"},
        "atm": {"cum_slut": "lipbite", "hate_cum": "disgusted", "cute_sex": "scared", "hardcore_sex": "smug", "_default": "surprised"},
        "recording": {"camera_lover": "happy", "camera_hater": "angry", "exhibitionist": "happy", "public_shy": "scared", "_default": "worried"},
        "ntr_watching": {"loyal": "uncomfortable", "cheater": "lipbite", "cute_sex": "worried", "_default": "uncomfortable"},
    }

    # A FACE slap (SpankHer in cowgirl, SPANK_FACE_SCENES): the spank pool without the lines only an ass spank fits,
    # and never the "spank_was_spanked" context (that one is for an event "spank")
    _TS_WATCHER_SPANK_ONLY = (_("Spank ME next when it's my turn!"),)
    _TS_WATCHER_LINES["slap"] = {_k: [_l for _l in _v if _l not in _TS_WATCHER_SPANK_ONLY]
                                 for _k, _v in _TS_WATCHER_LINES["spank"].items()}
    _WATCHER_EVENT_EXPR["slap"] = _WATCHER_EVENT_EXPR["spank"]

    _WATCHER_TRAIT_ORDER = [
        "cum_slut", "hate_cum",
        "anal_lover", "anal_hater",
        "camera_lover", "camera_hater",
        "exhibitionist", "public_shy",
        "hardcore_sex", "cute_sex",
        "loyal", "cheater",
        "voyeur", "virgin",
    ]

    def _watcher_scene_comment(event_type, active_girl=None):
        """Watcher comments on specific events during threesome scenes.
        Returns True if a line was spoken."""
        if not getattr(store, "_threesome_mode", False):
            return
        if not getattr(store, "_witness_watching", False):
            return
        _w = getattr(store, "_witness_girl", None)
        if _w is None:
            return
        _pool_dict = _TS_WATCHER_LINES.get(event_type)
        if not _pool_dict:
            return
        # first trait of hers the event speaks for; an eager trait she is still discovering only through its
        # discovery key (trait_line_keys). _matched_key is the pool key, _matched_trait the trait (expression)
        _matched_trait = _matched_key = "_default"
        for _t in _WATCHER_TRAIT_ORDER:
            if not _w.has_trait(_t):
                continue
            _k = next((_tk for _tk in trait_line_keys(_w, _t) if _tk in _pool_dict), None)
            if _k:
                _matched_trait, _matched_key = _t, _k
                break
        _pool = _pool_dict.get(_matched_key)
        if not _pool:
            return

        _ctx_key = None
        if event_type == "spank" and _w.gid in getattr(store, "_session_spanked_girls", set()):
            _ctx_key = "spank_was_spanked"
        elif event_type == "girl_orgasm" and getattr(store, "_session_orgasms_by_girl", {}).get(_w.gid, 0) > 0:
            _ctx_key = "girl_orgasm_already_came"
        elif event_type == "creampie":
            # creampies of the girl he is with, this one included (process_cum counts it before the comment).
            # The counter restarts at every sex_menu entry, a threesome switch too: it can miss one, never add one
            _cream_n = getattr(store, "_session_cum", {}).get("inside", 0)
            print("[TS_WATCHER] creampie #%d this session (2+ = again)" % _cream_n)
            if _cream_n >= 2:
                _ctx_key = "creampie_again"
        if _ctx_key:
            _ctx_dict = _TS_WATCHER_CONTEXT.get(_ctx_key)
            if _ctx_dict:
                _ctx_pool = _ctx_dict.get(_matched_key, _ctx_dict.get("_default"))
                if _ctx_pool:
                    _pool = _ctx_pool
                    print("[TS_WATCHER] context override: %s -> %s" % (_ctx_key, _matched_trait))

        _line = _tl(renpy.random.choice(_pool))
        if event_type == "ntr_watching" and active_girl and callable(globals().get("_format_partner_line", None)):
            _line = _format_partner_line(active_girl, _line)
        _expr_map = _WATCHER_EVENT_EXPR.get(event_type, {})
        _expr = _expr_map.get(_matched_trait, _expr_map.get("_default", "normal"))
        set_scene_expression(_w, _expr)
        Say_Line(_w, _line)
        print("[TS_WATCHER] %s (%s) reacted to %s" % (_w.gid, _matched_key, event_type))
        return True

    def _threesome_satisfaction_check(silent=False):
        """At threesome session end: BOTH girls expect to be satisfied.
        If only one came, the other(s) gain Jealousy and complain (unless silent).
        Achievement: one girl came 2+ times while the other got zero."""
        _ts_org = getattr(store, "_session_orgasms_by_girl", {}) or {}
        _ts_group = set(getattr(store, "_threesome_participants", set()) or set())
        _wg = getattr(store, "_witness_girl", None)
        print("[TS_SAT] START: orgasms=%s participants=%s witness=%s join_avail=%s silent=%s" % (_ts_org, _ts_group, _wg.gid if _wg else None, getattr(store, "_witness_join_available", False), silent))
        if _wg is not None and getattr(store, "_witness_join_available", False):
            _ts_group.add(_wg.gid)
        _ts_girls = [_g for _g in [_resolve_girl(_gid) for _gid in _ts_group] if _g is not None]
        if len(_ts_girls) < 2:
            print("[TS_SAT] ABORT: less than 2 girls in group (%s)" % [_g.gid for _g in _ts_girls])
            return
        _ts_counts = dict((_g.gid, _ts_org.get(_g.gid, 0)) for _g in _ts_girls)
        _ts_sat = [_g for _g in _ts_girls if _ts_counts[_g.gid] > 0]
        _ts_unsat = [_g for _g in _ts_girls if _ts_counts[_g.gid] == 0]
        print("[TS_SAT] counts=%s sat=%s unsat=%s" % (_ts_counts, [g.gid for g in _ts_sat], [g.gid for g in _ts_unsat]))
        debug_log("[THREESOME] satisfaction check: %s (silent=%s)" % (_ts_counts, silent))
        if not _ts_sat or not _ts_unsat:
            return
        # Achievement: exactly one satisfied with 2+ orgasms, everyone else zero
        if len(_ts_sat) == 1 and _ts_counts[_ts_sat[0].gid] >= 2:
            unlock_achievement("shes_my_favorite")
        _fav = _ts_sat[0]
        for _ug in _ts_unsat:
            Change_Status(_ug, "Jealousy", 80, max_val=1000)
            print("[TS_JEALOUSY] %s left unsatisfied (favorite=%s, counts=%s) -> Jealousy +80" % (_ug.gid, _fav.gid, _ts_counts))
            if silent:
                continue
            _ts_unsat_pool = None
            for _t in ("hardcore_sex", "cum_slut", "cute_sex"):
                if _ug.has_trait(_t):
                    _ts_unsat_pool = _TS_UNSAT_LINES[_t]
                    break
            if _ts_unsat_pool is None:
                _ts_unsat_pool = _TS_UNSAT_LINES["_default"]
            _ts_unsat_line = _tl(renpy.random.choice(_ts_unsat_pool))
            if "%s" in _ts_unsat_line:
                _ts_unsat_line = _ts_unsat_line % _fav.Name
            set_girl_sprite(_ug, pose="standing", at_list=[slot_center_right])
            set_girl_sprite(_fav, pose="standing", at_list=[slot_center_left])
            set_scene_expression(_ug, "sad" if _ug.has_trait("cute_sex") else "angry")
            Say_Line(_ug, _ts_unsat_line)
            _has_rivalry = (_fav.gid in getattr(_ug, "_harem_forced_by", set())) or (_ug.gid in getattr(_fav, "_harem_forced_by", set()))
            if _has_rivalry:
                _rivalry_line = _tl(renpy.random.choice(_TS_RIVALRY_COMEBACK_LINES))
                set_scene_expression(_fav, "smug")
                Say_Line(_fav, _rivalry_line)
                print("[TS_RIVALRY] %s fired back at %s" % (_fav.gid, _ug.gid))

    def _show_active_girl_threesome_reaction(active_girl, watcher, decision):
        """Show active girl's reaction to a witness staying/being kicked out."""
        _pool = _AG_THREESOME_LINES.get(decision, {})
        _line = None
        if decision in ("watch_only", "refuse") and active_girl.is_dating_player():
            _line = renpy.random.choice(_pool.get("_dating", _pool["_default"]))
        else:
            for _t in ("exhibitionist", "cheater", "hardcore_sex", "polyamorous", "cum_slut", "loyal", "cute_sex", "public_shy"):
                if active_girl.has_trait(_t) and _t in _pool:
                    _line = renpy.random.choice(_pool[_t])
                    break
        if _line is None:
            _line = renpy.random.choice(_pool.get("_default", [""]))
        Say_Line(active_girl, _tl(_line))

        if decision == "refuse":
            Say_Line(watcher, _tl(renpy.random.choice(_AG_THREESOME_WATCHER_KICKED)))

    def _witness_decides_to_stay(watcher, active_girl, force_join=False):
        """Central handler when a witness/walk-in girl decides to stay during sex.
        Checks active girl's opinion. Returns 'threesome', 'watch_only', or 'refuse'.
        force_join=True: skips active girl check (she already agreed via menu)."""
        if not getattr(watcher, "_saved_outfit", None):
            watcher.SaveOutfit()

        if force_join:
            _ag_decision = "allow"
        else:
            _ag_decision = _active_girl_allows_threesome(active_girl, watcher)

        store._witness_stay_result = _ag_decision if _ag_decision != "allow" else "threesome"
        _show_active_girl_threesome_reaction(active_girl, watcher, _ag_decision)

        if _ag_decision == "refuse":
            watcher.loc = girl_home_loc(watcher)
            hide_girl_sprite(watcher)
            debug_log("[THREESOME] witness_decides_to_stay: %s REFUSED by %s, watcher sent home" % (watcher.gid, active_girl.gid))
            return "refuse"

        store._witness_girl = watcher
        store._witness_watching = True
        store._witness_check_done = True

        if _ag_decision == "watch_only":
            debug_log("[THREESOME] witness_decides_to_stay: %s watch_only (active %s tolerates)" % (watcher.gid, active_girl.gid))
            return "watch_only"

        store._threesome_mode = True
        store._threesome_participants = set([active_girl.gid])
        unlock_achievement("the_3_way")

        if force_join:
            store._witness_join_available = True
        elif _witness_wants_to_join(watcher, active_girl):
            store._witness_join_available = True

        debug_log("[THREESOME] witness_decides_to_stay: %s THREESOME (active=%s force_join=%s join_available=%s)" % (watcher.gid, active_girl.gid, force_join, store._witness_join_available))
        return "threesome"

    def _threesome_invite_check(inv_girl, active_girl):
        """Check if watching girl accepts a threesome invitation.
        Returns "accept", "watch" (decline but stay), or "leave" (decline and go)."""

        # Lesbian block: lesbians only watch, never join
        if inv_girl.has_trait("lesbian"):
            debug_log("[THREESOME] invite BLOCKED: %s is lesbian, can only watch" % inv_girl.gid)
            return "watch"

        # GF block: a girlfriend refuses to share UNLESS she's polyamorous (the trait
        # is literally "open to sharing a partner") or the two are harem-mutual. Only a
        # DATING girl who is NOT poly (and not harem-mutual) forces the threesome to
        # break off — a poly GF falls through to the normal willingness check below.
        if inv_girl.is_dating_player() or active_girl.is_dating_player():
            _harem_mutual = is_harem_exempt(inv_girl, active_girl) and is_harem_exempt(active_girl, inv_girl)
            _inv_blocks = inv_girl.is_dating_player() and not inv_girl.has_trait("polyamorous")
            _active_blocks = active_girl.is_dating_player() and not active_girl.has_trait("polyamorous")
            if not _harem_mutual and (_inv_blocks or _active_blocks):
                debug_log("[THREESOME] invite BLOCKED: non-poly girlfriend present (inv=%s dating=%s poly=%s, active=%s dating=%s poly=%s)" % (inv_girl.gid, inv_girl.is_dating_player(), inv_girl.has_trait("polyamorous"), active_girl.gid, active_girl.is_dating_player(), active_girl.has_trait("polyamorous")))
                return "leave"
            debug_log("[THREESOME] GF present but poly/harem-mutual, allowing")

        like = int(inv_girl.get_like_for(active_girl.gid))
        love = int(getattr(inv_girl, "Love", 0))
        lust = int(getattr(inv_girl, "Lust", 0))
        obed = int(getattr(inv_girl, "Obed", 0))

        # Very low Girl_like = she leaves
        if like < 200:
            debug_log("[THREESOME] invite LEAVE: %s Girl_like for %s = %d (< 200)" % (inv_girl.gid, active_girl.gid, like))
            return "leave"

        threshold = 500

        if inv_girl.has_trait("exhibitionist") or inv_girl.has_trait("voyeur"):
            threshold -= 150
        if inv_girl.has_trait("hardcore_sex") or inv_girl.has_trait("cheater"):
            threshold -= 100
        if inv_girl.has_trait("public_shy"):
            threshold += 100
        if inv_girl.has_trait("loyal") and inv_girl.has_npc_partner():
            threshold += 200

        if like >= 700:
            threshold -= 50

        pool = love + (lust * 5) + obed
        debug_log("[THREESOME] invite check %s: pool=%d (L%d+Lust%dx5+O%d) vs T=%d like=%d" % (inv_girl.gid, pool, love, lust, obed, threshold, like))

        if pool >= threshold and like >= 300:
            return "accept"

        # Low like or low pool with shy/loyal = leave
        if like < 300 or inv_girl.has_trait("public_shy") or (inv_girl.has_trait("loyal") and inv_girl.has_npc_partner()):
            return "leave"

        return "watch"

    def scene_full_cleanup(girl, keep_outfit_for_dressup=False, was_secret=False):
        """Centralized cleanup after ANY sex scene exit.
        Restores outfit, clears cum, hides HUD, resets flags.
        Also hides ALL sex scene layers as safety net.
        keep_outfit_for_dressup: if True, don't restore outfit — let DressUp_Sequence animate it."""
        debug_log("[DEBUG] scene_full_cleanup: entered for girl=%s keep_outfit=%s" % (getattr(girl, 'gid', str(girl)), keep_outfit_for_dressup))

        # a sex-bubble line nobody clicked yet (the "Stop now" narration, a farewell of hers) is read BEFORE
        # the teardown wipes it (player report, 2026-10-09: "after stopping sex... moved in about a second").
        # Only with the bubble REALLY on screen: the flag alone can come stale out of a save.
        # The wait is _sex_bubble_wait_click (Talk.rpy): a rollback / load during it MUST propagate
        # (a bare `except Exception` here swallowed it: NameError on the caller's next line, 2026-10-11).
        if getattr(store, "_sex_bubble_pending", False) and renpy.get_screen("sex_bubble"):
            _sex_bubble_wait_click()
            _force_dismiss_sex_bubble()
        store._sex_bubble_pending = False

        # Left ON THE EDGE (tester suggestion, the author's yes 2026-10-10): the scene ends with her
        # Lust at the top and not one orgasm. Before the teardown, while she is still on screen: a warm
        # relationship drops the mask and demands the finish (edge_end_beg), a cold one rebuilds her
        # composure (edge_end_hide). Never on an angry abort, never inside a scripted story scene.
        # ONCE per session (_edge_end_said, reset by _scene_exit_flags_reset at every start_scene): the stop path
        # runs this cleanup up to three times (the position's End label, start_scene, after the CumCleanupMenu)
        # and she said it twice, in the bubble and again in the text box (tester 2026-10-11).
        if (getattr(girl, "Lust", 0) >= 85
                and store._session_orgasms_by_girl.get(getattr(girl, "gid", None), 0) == 0
                and getattr(store, "_edge_end_said", None) != getattr(girl, "gid", None)
                and not getattr(store, "_scene_angry_abort", False)
                and not getattr(store, "_scene_restricted", False)
                and not (hasattr(girl, "has_temp_status") and girl.has_temp_status("angry"))):
            _edge_warm = (hasattr(girl, "is_dating_player") and girl.is_dating_player()) or getattr(girl, "Love", 0) >= 600
            print("[EDGE_END] %s left on the edge (Lust %d, warm=%s)" % (girl.gid, girl.Lust, _edge_warm))
            store._edge_end_said = girl.gid
            Say_Line(girl, rod_pick_line(girl, "edge_end_beg" if _edge_warm else "edge_end_hide"))

        _intimacy = getattr(girl, "intimacy_flags", set()) or set()
        _had_penetrative = any(k in _intimacy for k in ("sex", "anal"))   # penetration ACTS only, never position flags
        _player_gf_list = [g for g in store.ALL_GIRLS if g.is_dating_player() and g != girl]
        debug_log("[ACHIEVEMENT] double_betrayal cleanup check: gf=%s bf=%s had_sex=%s" % ([g.gid for g in _player_gf_list], girl.has_npc_partner(), _had_penetrative))
        if _player_gf_list and girl.has_npc_partner() and _had_penetrative:
            unlock_achievement("double_betrayal")

        # _last_scene_was_anal: preserved here — DG_End sets it, sex_menu clears it on entry
        store.doggy_anal = False
        store.laying_anal = False
        store.rcg_anal = False

        # Hide HUD
        pass  # cum_tracker_hud disabled

        # Preserve watcher gid BEFORE finalize_recording clears it,
        # so _kill_scene_threads can protect the watcher's sprite_state.
        _pre_rec_watcher = getattr(store, "_recording_watcher_gid", None)
        _wg_trace = getattr(store, "_witness_girl", None)
        _wg_trace_gid = getattr(_wg_trace, "gid", None) if _wg_trace else None
        if _wg_trace_gid:
            print("[CLEANUP_TRACE] PRE finalize_recording: witness=%s showing=%s rec_watcher=%s" % (
                _wg_trace_gid, renpy.showing(_wg_trace_gid), _pre_rec_watcher))

        # Stop recording if active
        finalize_recording()

        if _wg_trace_gid:
            print("[CLEANUP_TRACE] POST finalize_recording: witness=%s showing=%s" % (
                _wg_trace_gid, renpy.showing(_wg_trace_gid)))

        # Restore gid so _kill_scene_threads can preserve watcher sprite_state
        if _pre_rec_watcher and not getattr(store, "_recording_watcher_gid", None):
            store._recording_watcher_gid = _pre_rec_watcher

        # Reset session state (session_cum preserved for CumCleanupMenu)
        # NOTE: door_locked is NOT reset here — it persists across mid-session
        # transitions (HJ→BJ, cum-in-mouth, position switches). It is cleared
        # by interactions.rpy at real session end and by navigation on location change.
        if not scene_ends_on_cum():
            store._player_exhausted = False
        else:
            debug_log("[CLEANUP] scene_full_cleanup: preserving _player_exhausted=%s (scene ends on his cum)" % store._player_exhausted)
        store._mast_threads_running = False
        store._oral_active = False
        store._financial_scene_active = False
        store._financial_extras_paid = {}
        store._focus_overdue_count = 0
        store._focus_warning_shown = False
        store._cum_forced_surprise = False
        store._force_creampie = False
        store._virgin_blood_postscene = False
        _esc_session_reset()
        count_slaps_reset("scene cleanup")

        # Kill background threads (blink, expression cycle) so they stop
        # re-showing images after renpy.scene() clears the display
        _kill_scene_threads()
        # Clear watcher gid after _kill_scene_threads preserved sprite_state
        store._recording_watcher_gid = None

        if _wg_trace_gid:
            print("[CLEANUP_TRACE] POST _kill_scene_threads: witness=%s showing=%s sprite_state=%s" % (
                _wg_trace_gid, renpy.showing(_wg_trace_gid), bool(sprite_state.get(_wg_trace_gid))))

        _mid_session = getattr(store, "_sex_menu_active", False)

        # Clear cum from body (skip mid-session — cum persists between scenes)
        # Mouth cum persists through scene end for standing sprite
        # _cum_left_on: player chose "Leave it" in CumCleanupMenu — preserve cum
        if not _mid_session and hasattr(girl, "Cum"):
            if getattr(girl, "_cum_left_on", False):
                debug_log("[CLEANUP] cum left on by player choice, preserving for %s" % getattr(girl, 'gid', str(girl)))
                girl._cum_left_on = False
            else:
                _persist_mouth = getattr(girl, "_mouth_cum_persist", False)
                girl.Cum = []
                girl._mouth_cum_persist = False
                if _persist_mouth:
                    girl.Cum.append("mouth")
                    debug_log("[CLEANUP] mouth cum preserved on standing sprite for %s" % getattr(girl, 'gid', str(girl)))
        elif _mid_session and getattr(girl, "_mouth_cum_persist", False):
            _mcl = getattr(girl, "Cum", [])
            if "mouth" not in _mcl:
                _mcl.append("mouth")
                girl.Cum = _mcl
                debug_log("[CLEANUP] mouth cum re-added mid-session for %s" % getattr(girl, 'gid', str(girl)))

        # Hide ALL sex scene layers (dynamic scan by prefix)
        _hide_all_scene_layers(girl)
        for _extra in ("spank_hand", "bj_slap", "touch_zoom"):
            renpy.hide(_extra)

        # Reset RCG/cowgirl state
        store.rcg_rub_mode = False
        store.rcg_tip_mode = False
        store.rcg_grab = False
        store.rcg_started = False
        store.rcg_arms_pose = 1
        store.cowgirl_rub_mode = False
        store.cowgirl_tip_mode = False
        store.cowgirl_started = False
        store.condom_active = False
        condom_break_reset()
        stealth_condom_reset()

        if renpy.showing("impregnation_anim"):
            renpy.hide("impregnation_anim")

        # Reset titjob state
        store.titjob_started = False
        store.titjob_arms_pose = 1

        # Reset doggy state
        store._doggy_girl = None
        store.doggy_blink = False
        store.doggy_started = False
        store.doggy_anal = False
        store.doggy_rub_mode = False
        store.doggy_tip_mode = False
        store.doggy_grab = False
        store._dg_masturbating = False
        # the session's hole history (the gaping "After" patches of her doggy, Shion's RCG anus): a position switch
        # carries it on, a scene end drops it
        store._dg_had_pussy = False
        store._dg_had_anal = False
        store._rcg_had_anal = False

        # Reset laying_down state
        store._laying_girl = None
        store.laying_speed = 0
        store.laying_blink = False
        store.laying_started = False
        store.laying_rub_mode = False
        store.laying_tip_mode = False
        store._ld_masturbating = False
        store._ld_blood_active = False
        store._ld_cum_dick_level = 0

        # Restore saved outfit (skip mid-session — girl stays stripped between scenes)
        if _mid_session:
            debug_log("[DEBUG] scene_full_cleanup: mid-session, keeping current outfit + cum")
        elif not keep_outfit_for_dressup and getattr(girl, "_saved_outfit", None):
            girl.RestoreOutfit(clear_saved=True)
        elif keep_outfit_for_dressup and getattr(girl, "_saved_outfit", None):
            debug_log("[DEBUG] scene_full_cleanup: DressUp didn't run, forcing RestoreOutfit")
            girl.RestoreOutfit(clear_saved=True)

        # Safety net: if RestoreOutfit put the towel back, or shower state lingered, force casual
        if getattr(girl, "shower_state", None) in ("towel", "nude") or getattr(girl, "clothes", {}).get("over") == "towel":
            girl.WearPreset("casual", apply_now=False)
            if getattr(girl, "shower_state", None) not in (None, "dressed"):
                girl.shower_state = "dressed"

        # Reset to standing pose with clean transforms (kills sex animations)
        pose = getattr(girl, "default_pose", "standing")
        _slot = _safe_restore_slot(getattr(girl, "_prev_slot", StageCenter))
        if _slot == StageLeft:
            _slot_tf = slot_left
        elif _slot == StageRight:
            _slot_tf = slot_right
        else:
            _slot_tf = slot_center
        girl.ResetVisuals(pose=pose, at_list=[_slot_tf])

        # Lesbian post-scene coldness (skip if player left unnoticed or already fired)
        if not was_secret and girl.has_trait("lesbian") and not getattr(store, "_lesbian_coldness_done", False):
            store._lesbian_coldness_done = True
            _proof = lesbian_openness(girl)
            if _proof < 26:
                _cold_pen = 30
            elif _proof < 51:
                _cold_pen = 20
            elif _proof < 76:
                _cold_pen = 10
            else:
                _cold_pen = 0
            if _cold_pen > 0:
                girl.set_temp_status("cold", 1)
                Change_Status(girl, "Love", -_cold_pen)
                debug_log("[DEBUG] lesbian coldness: proof=%d penalty=%d" % (_proof, _cold_pen))
                if _proof < 26:
                    _cold_lines = [
                        _("Shit... I should not be doing that with a man. Don't get any ideas."),
                        _("This doesn't mean anything. I'm still not into guys."),
                        _("That was a mistake. Don't think this changes anything."),
                    ]
                    set_scene_expression(girl, "angry")
                elif _proof < 51:
                    _cold_lines = [
                        _("I don't know why I keep letting this happen..."),
                        _("This is so confusing... just leave me alone for a bit."),
                        _("I need a minute. Don't talk to me right now."),
                    ]
                    set_scene_expression(girl, "sad")
                else:
                    _cold_lines = [
                        _("I... I don't want to think about what this means."),
                        _("Can we just pretend this didn't happen? Again?"),
                    ]
                    set_scene_expression(girl, "sad")
                Say_Line(girl, _tl(renpy.random.choice(_cold_lines)))

        # Watcher/threesome cleanup is handled by _sex_menu_exit_cleanup(),
        # called only when the player truly exits sex_menu.
        # scene_full_cleanup does NOT touch witness/threesome state.

        # NTR discovery kick fallback (standalone scenes outside sex_menu)
        if not _mid_session and getattr(store, "_ntr_discovery_kick", False):
            store._ntr_discovery_kick = False
            _kick_npc = get_npc_partner_for(girl)
            # no NPC to name: a pronoun of the language (Russian: "ними", it fits "поговорить с ...")
            _kick_npc_name = _kick_npc.Name if _kick_npc else _tl(_("them"))
            _kick_line = _tl(_("Look, that was good, but I need to talk to %s now. We'll talk tomorrow, okay?")) % _kick_npc_name
            Say_Line(girl, _kick_line)
            store.CurrentLocation = "room"
            debug_log("[NTR_DISCOVERY] Post-scene kick (standalone): player sent to room")

        debug_log("[DEBUG] scene_full_cleanup: finished for girl=%s" % getattr(girl, 'gid', str(girl)))

    def _sex_menu_exit_cleanup(silent=False):
        """Centralized cleanup for ALL sex_menu exit paths.
        Handles threesome history/watcher cleanup, witness reset, and session flag.
        Call this once when the player truly leaves sex_menu (not between scenes).
        silent=True: skip spoken reactions (kick-out / hard-reset exit paths)."""
        store._sex_menu_active = False
        store._via_bj_post_cum_choice = None

        print("[EXIT_CLEANUP] threesome_mode=%s participants=%s witness=%s" % (getattr(store, "_threesome_mode", False), getattr(store, "_threesome_participants", set()), getattr(store, "_witness_girl", None)))
        if getattr(store, "_threesome_mode", False):
            _wg = getattr(store, "_witness_girl", None)
            _ts_parts = set(getattr(store, "_threesome_participants", set()))
            if _wg is not None and getattr(store, "_witness_watching", False) and _wg.gid not in _ts_parts:
                for _p_gid in _ts_parts:
                    _wg.inc_history_with(_p_gid, "threesome_watched", 1)
                debug_log("[THREESOME] Recorded watch history for %s with %s" % (_wg.gid, list(_ts_parts)))
            # Satisfaction: in a threesome BOTH girls expect to cum (must run BEFORE _record_threesome_history clears participants)
            _threesome_satisfaction_check(silent=silent)
            _record_threesome_history()
            # Harem trigger: if a GF participated in threesome, set open-rel trigger with the other girl
            for _tgid in _ts_parts:
                _tg = _resolve_girl(_tgid)
                if _tg and _tg.is_dating_player() and not getattr(_tg, "_open_relationship_consent", False):
                    for _togid in _ts_parts:
                        _tog = GIRL_BY_ID.get(_togid)
                        if _togid != _tgid and _tog and not is_harem_exempt(_tg, _tog):
                            _tg._gf_open_rel_trigger = {"other_gid": _togid, "reason": "threesome"}
                            print("[HAREM_TRIGGER] %s threesome with %s, trigger set" % (_tgid, _togid))
                            break
            if _wg is not None and getattr(store, "_witness_watching", False):
                _threesome_cleanup_watcher(_wg)
            debug_log("[THREESOME] _sex_menu_exit_cleanup: full watcher cleanup done")
        else:
            _wg = getattr(store, "_witness_girl", None)
            if _wg is not None and getattr(store, "_witness_watching", False):
                _wg.loc = getattr(store, "_ig_original_loc", _wg.loc)
                hide_girl_sprite(_wg)

        print("[WITNESS_RESET] _sex_menu_exit_cleanup clearing witness: was_watching=%s was_girl=%s threesome=%s" % (getattr(store, "_witness_watching", False), getattr(getattr(store, "_witness_girl", None), "gid", None), getattr(store, "_threesome_mode", False)))
        store._witness_girl = None
        store._witness_watching = False
        store._witness_join_available = False
        store._witness_scene_aborted = False
        store._threesome_mode = False
        store._threesome_participants = set()
        store._atm_cum_in_mouth = False
        store._atm_source_gid = None
        store._npc_witness_check_done = False
        store._npc_witness_npc = None
        store._npc_witness_detected = False
        store._ntr_spontaneous_raw_asked = False

    def session_cum_add(cum_type):
        """Add a cum event to the session tracker."""
        # Merge creampie variants into one display key
        display_key = cum_type
        if cum_type == "condom_removed_inside":
            display_key = "inside"
        sc = store._session_cum
        sc[display_key] = sc.get(display_key, 0) + 1
        store._session_cum = sc

    def session_cum_has_any():
        """True if any cum was deposited this session (excluding condom)."""
        for k, v in store._session_cum.items():
            if k not in ("condom", "away") and v > 0:
                return True
        return False

    def _rebuild_cum_from_session(girl):
        """Rebuild girl.Cum visual tags from _session_cum data.
        scene_full_cleanup clears girl.Cum before CumCleanupMenu runs,
        so "Leave it" must reconstruct it from the session tracker."""
        _map = {
            "face": "face", "tits": "boobs", "outside": "body",
            "inside": "dripping", "head": "head", "mouth": "mouth",
            "shoulders": "shoulders", "ass": "ass", "back": "back",
        }
        cum_list = []
        for k, v in store._session_cum.items():
            if k in ("condom", "away", "anal_inside") or v <= 0:
                continue
            tag = _map.get(k)
            if tag and tag not in cum_list:
                cum_list.append(tag)
        if store._session_cum.get("anal_inside", 0) > 0:
            if "dripping_ass" not in cum_list:
                cum_list.append("dripping_ass")
        girl.Cum = cum_list
        girl._cum_left_on = True
        girl.RefreshSprite()
        print("[CUM_LEAVE] rebuilt cum from session: %s" % cum_list)

    def session_cum_visible_items():
        """Return list of (display_name, count) for the HUD, excluding condom."""
        items = []
        for key, count in store._session_cum.items():
            if key in ("condom", "away") or count <= 0:
                continue
            name = CUM_DISPLAY_NAMES.get(key, key.capitalize())
            items.append((name, count))
        return sorted(items, key=lambda x: x[0])

    # ---------------------------------------------------------
    # Multiple consented creampie lines (same session)
    # ---------------------------------------------------------
    _MULTI_CREAM_LINES = {
        "cum_slut": [
            _("Again...~ You really can't get enough of me, can you?"),
            _("More? Yes please... fill me up until I'm overflowing~"),
            _("Keep going... I want every last drop inside me~"),
            _("Mmm... I lost count. Don't stop."),
            _("Yesss, again! Let it all out inside me... I want to be dripping~"),
            _("More, more, more! I want so much cum inside me it leaks out~"),
            _("Fill me up again! I want to feel it running down my thighs~"),
            _("Don't stop cumming inside me... I want to be completely full~"),
        ],
        # still discovering it (trait_is_new): a 2nd load this session, "again" is true, the addiction is not yet
        "cum_slut_new": [
            _("Again...? I can't believe how much I want this..."),
            _("Twice... and I still want more. What's happening to me?"),
            _("You came inside me again... how does it keep getting better?"),
            _("More...? Yes... I don't understand it, but yes."),
        ],
        "hate_cum": [
            _("Again?! I already told you... ugh, fine. But this is the LAST time."),
            _("You already came inside me once... why do I keep letting you do this..."),
            _("I swear, if you do it AGAIN after this... we're done."),
            _("How many times are you going to... ugh. I can feel it all inside me already."),
        ],
        "hardcore_sex": [
            _("Again? Good. Don't hold back."),
            _("More. I can take it. Give me everything."),
            _("You're not done yet? Perfect. Neither am I."),
            _("Keep filling me up. I want to feel it dripping out of me."),
            _("Again! Harder this time! Make me feel every drop!"),
            _("Don't stop until you have nothing left to give me."),
        ],
        "cute_sex": [
            _("Again...? That's a lot... but it feels so warm and close..."),
            _("You really wanted to, huh? It's okay... I like feeling connected to you."),
            _("I'm so full already... but I don't want you to stop..."),
            _("It's so warm inside me... I can feel it all... is that okay?"),
            _("You keep filling me up... I feel so close to you right now..."),
        ],
        "cheater": [
            _("Twice inside me... your girlfriend would die if she knew~"),
            _("More? She's never getting this from you, is she?"),
            _("Keep cumming inside me. I want her to smell me on you."),
            _("Again! Your girlfriend doesn't get you like this, does she?"),
            _("Mmm, one more load inside me... your girlfriend can have what's left~"),
        ],
        "loyal": [
            _("You came inside me again... my %(pl)s can never find out about any of this."),
            _("Twice... I'm in so deep now. There's no going back."),
            _("How many times are you going to do this to me... and why can't I say no?"),
            _("Again... %(pp)s doesn't know I'm full of another man's cum right now..."),
            _("I'm going home to %(po)s like this... with your cum still dripping out of me..."),
            _("My %(pl)s would lose %(poss)s mind... and you keep doing it... and I keep letting you..."),
        ],
        "camera_lover": [
            _("Again? I hope you're recording this... it's going to look amazing."),
            _("Twice inside... the footage is going to be incredible~"),
            _("Keep the camera on! I want them to see every drop going inside me~"),
        ],
        "exhibitionist": [
            _("Again... right here. Anyone could walk in. I don't even care anymore."),
            _("More? The thought of someone catching us like this..."),
            _("Fill me up again... I want someone to see me dripping on the way out."),
        ],
        "public_fetish": [
            _("Again... right here where anyone could catch us dripping. The thrill doubles each time."),
            _("Another load inside me... in public... if someone walks by now the evidence is OBVIOUS."),
            _("More cum inside me where people could see? My heart is racing and I love it."),
        ],
        "camera_hater": [
            _("Again?! Please tell me you didn't film the FIRST one either!"),
            _("Twice inside me... and you better not have evidence of EITHER time."),
            _("More?! If anyone ever finds out about even ONE of these creampies..."),
        ],
        "public_shy": [
            _("Again?! It's already going to be impossible to walk out of here without anyone noticing..."),
            _("Twice inside me... if someone sees me leaking... I can't even think about it."),
            _("More cum... in public... I'm going to be dripping all the way home. Someone WILL notice."),
        ],
        "virgin": [
            _("You came inside me again... I just lost my virginity and I'm already full of your cum..."),
            _("My first time ever and you've already cum inside me twice... I can't believe this is happening."),
            _("More... I went from virgin to this in one session... what have I become?"),
        ],
        # --- BF context (not a trait -- checked separately) ---
        "_bf": [
            _("Again... you keep cumming inside me while my %(pl)s has no idea..."),
            _("More inside me... %(pp)s thinks I'm being faithful and I'm here dripping with your cum..."),
            _("You already came inside me once... my %(pl)s never even gets to do this... and you just keep going..."),
            _("I'm so full of your cum... and none of it is my %(pl)s's... god, what am I doing..."),
            _("Again... if %(pp)s knew how many times you came inside me today %(pp)s would lose %(poss)s mind..."),
            _("Keep filling me up... I'll go home to %(po)s like this and %(pp)s won't suspect a thing..."),
        ],
        "_default": [
            _("Again...? You really couldn't hold back, huh?"),
            _("Twice inside me in one session... that's a lot."),
            _("More...? Okay... just be careful."),
            _("You already came inside once... but fine. I trust you."),
            _("Yesss, again... let it all out inside me..."),
            _("More... I can feel it all inside me already... don't stop..."),
            _("Fill me up again... I want to feel it overflowing..."),
        ],
    }

    def _multi_cream_line(girl):
        """Pick a trait-aware line for 2nd+ consented creampie in same session."""
        _has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        for t in ("cum_slut", "hate_cum", "hardcore_sex", "cute_sex", "cheater",
                  "loyal", "camera_lover", "exhibitionist", "public_fetish",
                  "camera_hater", "public_shy", "virgin"):
            if not girl.has_trait(t):
                continue
            if t == "loyal" and not _has_bf:
                continue
            if t == "cheater" and not (player_has_girlfriend(ALL_GIRLS) and not girl.is_dating_player()):
                continue
            t = trait_pool_key(girl, t, _MULTI_CREAM_LINES)   # "cum_slut_new" while discovering it (a 2nd load is never her first)
            _line = renpy.random.choice(_MULTI_CREAM_LINES[t])
            return _format_partner_line(girl, _line)
        # BF context (not a trait)
        if _has_bf:
            return _format_partner_line(girl, renpy.random.choice(_MULTI_CREAM_LINES["_bf"]))
        return renpy.random.choice(_MULTI_CREAM_LINES["_default"])

    def _creampie_was_refused():
        """True when she TOLD him not to finish inside during this scene (the raw-sex talk, or a refusal since).
        The default "denied" only means nobody brought it up, so it is not a refusal."""
        return store._creampie_consent == "blocked" or (store._creampie_consent == "denied" and bool(store._creampie_warned))

    def _cream_liked_line(girl, scene_type, refused):
        """Her line after a creampie nobody cleared with her that she loves anyway (cum_slut anywhere, anal_lover
        in anal). A cum_slut only gets the forced pool ("I said no but...") when she really HAD said no
        (`refused`); when nobody asked, it is a regular creampie reaction (her traits and the pregnancy layer
        pick it: a breeding kink answers "please let this one take"). The anal_lover lines of the forced pool
        never claim a refusal ("without asking? ...Good.")."""
        if girl.has_trait("cum_slut"):
            _key, _fallback = (("cum_inside_forced", _("I said no but... okay, I liked it.")) if refused
                               else ("cum_inside", _("You could have just asked... but I liked it.")))
        else:
            _key, _fallback = "cum_inside_forced", _("You came inside my ass... good.")
        print("[CUM] liked-it-anyway line: %s pool=%s refused=%s scene=%s consent=%s warned=%s" % (
            girl.gid, _key, refused, scene_type, store._creampie_consent, store._creampie_warned))
        return scene_pick_line(_key, scene=scene_type, girl=girl) or _tl(_fallback)

    def _consented_cream_line(girl, scene_type):
        """Pick consented creampie line — multi-cream aware.
        Uses session tracker: if inside >= 2 at this point, it's a repeat."""
        _sc = store._session_cum.get("inside", 0)
        if _sc >= 2:
            return _multi_cream_line(girl)
        return scene_pick_line("cum_inside_consented", scene=scene_type, girl=girl) or _("I can't believe I let you do that...")

    # ---------------------------------------------------------
    # Cum tracking (permanent + session)
    # ---------------------------------------------------------
    def process_cum(girl, scene_type, cum_type, visual_tags=None):
        """
        Central tracking after cum event.
        cum_type: "outside", "face", "tits", "mouth", "inside",
                  "condom", "condom_removed_inside"
        visual_tags: optional list of explicit visual tags (e.g. ["face","boobs","head"])
                     when cum lands on multiple places at once. Overrides _CUM_VISUAL_MAP.
        Returns {"first_time": bool, "total": int}
        """
        # Permanent log
        cum_log = getattr(girl, "CumLog", {})
        prev = cum_log.get(cum_type, 0)
        cum_log[cum_type] = prev + 1
        girl.CumLog = cum_log
        if cum_type != "condom":   # same rule as girl_cum_loads(): a condom's load never touched her
            _slg = store._session_loads_by_girl
            _slg[girl.gid] = _slg.get(girl.gid, 0) + 1
            store._session_loads_by_girl = _slg
            print("[CUM] %s load #%d (%d this session), cum_slut discovery=%s" % (
                girl.gid, girl_cum_loads(girl), _slg[girl.gid],
                trait_discovery_keys(girl, "cum_slut") if girl.has_trait("cum_slut") else "-"))

        if cum_type in ("inside", "condom_removed_inside"):
            _was_first_cream = getattr(girl, "CreampieCounts", 0) == 0
            girl.CreampieCounts = getattr(girl, "CreampieCounts", 0) + 1
            # Creampies per time slot (one night = one slot: a morning one and a night one are not "the same night"):
            # the slot of her last one, how many she took in it and the most she ever took in one slot. Truth or Dare
            # reads the most ("more than once in the same night"); 0 = no record yet (a save older than it), where the
            # reader keeps its proof from the counts.
            _cslot = store.Day * 10 + getattr(store, "TimeIndex", 0)
            girl._creampie_slot_count = ((getattr(girl, "_creampie_slot_count", 0) or 0) + 1
                                         if getattr(girl, "_creampie_last_slot", -1) == _cslot else 1)
            girl._creampie_last_slot = _cslot
            girl._creampie_slot_max = max(getattr(girl, "_creampie_slot_max", 0) or 0, girl._creampie_slot_count)
            print("[CUM] %s creampie #%d, slot record: slot=%d in_this_slot=%d most_in_one_slot=%d" % (
                girl.gid, girl.CreampieCounts, _cslot, girl._creampie_slot_count, girl._creampie_slot_max))
            # Player global first creampie (shown first so girl banner replaces it)
            if not Player.has_discovery("first_creampie"):
                Player.discover("first_creampie")
            # Girl-specific first creampie (shown last, stays on screen)
            if _was_first_cream and hasattr(girl, "mark_player_first") and not girl.bf_has_done("creampie"):
                girl.mark_player_first("creampie")
            if hasattr(girl, "has_trait") and girl.has_trait("hate_cum"):
                unlock_achievement("unwanted_gift")

            # Add separate creampie video alongside the original
            if store._recording_active and store._recording_girl == girl:
                _add_creampie_video(girl)

            # Pregnancy risk registration (pregnancy.rpy ignores anal / non-penetrative scenes)
            if callable(globals().get("_register_pregnancy_risk", None)):
                _register_pregnancy_risk(girl, cum_type, scene_type)

        # Visual cum persistence
        cum_list = getattr(girl, "Cum", [])
        if visual_tags is not None:
            for _vt in visual_tags:
                if _vt not in cum_list:
                    cum_list.append(_vt)
            print("[PROCESS_CUM] scene_type=%s cum_type=%s visual_tags=%s" % (scene_type, cum_type, visual_tags))
        else:
            _CUM_VISUAL_MAP = {
                "face":    "face",
                "tits":    "boobs",
                "outside": "body",
                "inside":  "dripping",
                "condom_removed_inside": "dripping",
                "head":    "head",
                "mouth":   "mouth",
                "shoulders": "shoulders",
                "ass":     "ass",
                "back":    "back",
            }
            visual_tag = _CUM_VISUAL_MAP.get(cum_type)
            print("[PROCESS_CUM] scene_type=%s cum_type=%s visual_tag=%s" % (scene_type, cum_type, visual_tag))
            if visual_tag == "dripping" and scene_type in _ANAL_SCENE_TYPES:
                visual_tag = None
                print("[PROCESS_CUM] ANAL: suppressed dripping visual_tag")
            if visual_tag and visual_tag not in cum_list:
                cum_list.append(visual_tag)

        # Anal creampie: add separate dripping_ass tag (distinct from vaginal dripping)
        if scene_type in _ANAL_SCENE_TYPES and cum_type in ("inside", "condom_removed_inside"):
            if "dripping_ass" not in cum_list:
                cum_list.append("dripping_ass")
            print("[PROCESS_CUM] ANAL INSIDE: added dripping_ass, cum_list=%s" % cum_list)
            _ac = store._session_cum
            _ac["anal_inside"] = _ac.get("anal_inside", 0) + 1
            store._session_cum = _ac

        # Firsts tracking: first cum in mouth. ATM-aware: the ATM context (_atm_cum_in_mouth, opened by
        # atm_register) is still open here, _bj_mouth_cum_reaction only closes it AFTER process_cum.
        if cum_type == "mouth":
            _firsts = getattr(girl, "Firsts", None)
            if _firsts is None:
                girl.Firsts = {}
                _firsts = girl.Firsts
            if "cum_mouth" not in _firsts:
                _firsts["cum_mouth"] = "from_anal" if getattr(store, "_atm_cum_in_mouth", False) else "normal"
                print("[ATM] %s Firsts[cum_mouth]=%s" % (girl.gid, _firsts["cum_mouth"]))
            # Track mouth cum count for corruption (parallel to CreampieCounts)
            girl.MouthCumCounts = getattr(girl, "MouthCumCounts", 0) + 1
            girl._mouth_cum_persist = True
            debug_log("[CUM] mouth cum persist flag set for %s" % girl.gid)

        # HJ/BJ scene: always add penis cum on player cum
        if store._hj_girl is not None and store._hj_girl is girl:
            if "penis" not in cum_list:
                cum_list.append("penis")
        elif store._bj_girl is not None and store._bj_girl is girl:
            if "penis" not in cum_list:
                cum_list.append("penis")

        girl.Cum = cum_list

        # Auto-refresh scene visuals
        _refresh_scene_cum(girl)

        # Session log (for HUD display)
        session_cum_add(cum_type)

        # Corruption check: creampie + mouth cum threshold
        if cum_type in ("inside", "condom_removed_inside", "mouth"):
            girl.check_corruption("cum")

        # Reset player focus after cumming
        store.Player.Focus = 0
        store._focus_overdue_count = 0
        store._focus_warning_shown = False

        # Drain energy on cum
        store.Player.change_energy(-1)
        if store.Player.energy <= 0:
            store._player_exhausted = True

        if scene_ends_on_cum():
            store._player_exhausted = True
            debug_log("[CUM] scene ends on his cum: forcing _player_exhausted=True for auto-end")
        print("[SCENE_FLOW] he came: %s %s/%s (energy after this cum; exhausted=True here = out of energy or a scene that "
              "ends on his cum) | %s" % (girl.gid, scene_type, cum_type, scene_flow_state()))

        # NTR creampie violation. PRESENCE is decided here: scene_full_cleanup wipes the watcher state
        # before start_scene runs _ntr_creampie_check, so it cannot be tested later. "< 4" and not "== 3":
        # a watched tip creampie at level 1 / 2 must confront too.
        if cum_type in ("inside", "condom_removed_inside"):
            _ntr_npc_w = getattr(store, "_ntr_watching_npc", None)
            if _ntr_npc_w is not None and getattr(_ntr_npc_w, "_ntr_active", False):
                _ntr_bl = getattr(_ntr_npc_w, "_ntr_boundary_level", 1)
                if _ntr_bl < 4 and _npc_witness_is_girls_partner(_ntr_npc_w, girl):
                    store._ntr_creampie_witnessed_gid = girl.gid
                    girl._ntr_violation_pending = True   # angry ends are gated on this flag (level 1 / 2 included)
                    print("[NTR_CUM] creampie WITNESSED by %s (bl=%d) -> confrontation allowed" % (_ntr_npc_w.name, _ntr_bl))
                if _ntr_bl == 3:
                    girl._ntr_violation_pending = True
                    _ntr_npc_leaves_scene(_ntr_npc_w, girl)
                    debug_log("[NTR_CUM] Creampie violation flagged for %s (penalty deferred to _ntr_creampie_confrontation)" % _ntr_npc_w.name)
            elif not girl.has_trait("lesbian") and girl.has_npc_partner():
                _npc_check = get_npc_partner_for(girl)
                if _npc_check and getattr(_npc_check, "_ntr_active", False):
                    _ntr_bl_abs = getattr(_npc_check, "_ntr_boundary_level", 1)
                    if _ntr_bl_abs < 4 and getattr(store, "_ntr_session_watcher_gid", None) == girl.gid and not store.door_locked:
                        # he watched an earlier scene of this session to its end and never left the room
                        store._ntr_creampie_witnessed_gid = girl.gid
                        girl._ntr_violation_pending = True
                        print("[NTR_CUM] creampie with %s still in the room (watched an earlier scene, bl=%d) -> confrontation allowed" % (_npc_check.name, _ntr_bl_abs))
                    else:
                        print("[NTR_CUM] creampie with partner ABSENT for %s (bl=%d): no confrontation, next-day fallout only at level 3" % (girl.gid, _ntr_bl_abs))
                    if _ntr_bl_abs == 3:
                        girl._ntr_violation_pending = True
                        debug_log("[NTR_CUM] Creampie violation (not watching), next-day consequences for %s" % girl.gid)

        if scene_type not in ("bj", "hj", "tj", "fj", "rj") and girl.has_npc_partner():
            _wm_npc = get_npc_partner_for(girl)
            if _wm_npc and getattr(_wm_npc, "friendship_with_player", 0) >= 500:
                unlock_achievement("wingman")

        store._last_cum_type = cum_type

        if cum_type in ("inside", "condom_removed_inside"):
            _watcher_scene_comment("creampie")
        elif cum_type not in ("condom", "outside"):
            _watcher_scene_comment("cum_on_girl")
        elif visual_tags:
            _watcher_scene_comment("cum_on_girl")

        # Pregnancy: pull-out risk (1%). pregnancy.rpy filters out anal / non-penetrative scenes.
        if cum_type == "outside":
            if callable(globals().get("_register_pregnancy_risk", None)):
                _register_pregnancy_risk(girl, "outside", scene_type)

        # Femdom: did he keep her orders (hold it, where to cum, her first)? Judged now, said after (_post_cum_central)
        femdom_note_cum(girl, scene_type, cum_type)

        return {"first_time": prev == 0, "total": cum_log[cum_type]}

    def _cum_say_line(girl, cum_type, scene_type):
        _line = scene_pick_line("cum_%s" % cum_type, scene=scene_type, girl=girl)
        if _line:
            Say_Line(girl, _line)

    def _pcr_reset_speed(scene_type):
        _sv = _cum_cfg(scene_type, "speed_var")
        if _sv:
            setattr(store, _sv, 1)
        if scene_type == "cowgirl":
            store._cg_force_static = False
        print("[PCR_RESET_SPEED] scene=%s" % scene_type)

    def _refresh_scene_cum(girl):
        """Refresh current scene visuals after cum was added to girl.Cum."""
        gid = getattr(girl, "gid", girl.Id)

        # HJ scene
        if store._hj_girl is not None and store._hj_girl is girl:
            _hj_update_attrs(girl)
            _hj_show_sprite(girl)
            _hj_cum = getattr(girl, "Cum", [])
            _hj_slot_tf = hj_get_slot_transform(store.hj_speed)
            _hj_pov = _gsc(gid, 'pov_overlay', False, pose='handjob')
            for _suffix, _z_normal, _z_pov in [("hj_cum_face", 10002, 10057), ("hj_cum_mouth", 10003, 10058)]:
                _hj_cum_img = "%s %s" % (gid, _suffix)
                _hj_cum_z = _z_pov if _hj_pov else _z_normal
                if renpy.has_image(_hj_cum_img):
                    renpy.show(_hj_cum_img, tag="%s_%s" % (gid, _suffix), at_list=[_hj_slot_tf], zorder=_hj_cum_z)
            hj_show_hand_cum(girl, store.hj_speed, _hj_pov)
            renpy.restart_interaction()
            print("[HJ_REFRESH_CUM] gid=%s Cum=%s pov=%s" % (gid, _hj_cum, _hj_pov))

        # BJ scene (cum layers use ConditionSwitch, just restart interaction)
        elif store._bj_girl is not None and store._bj_girl is girl:
            renpy.restart_interaction()

        # TJ scene (cum layers use ConditionSwitch, just restart interaction)
        elif store._titjob_girl is not None and store._titjob_girl is girl:
            renpy.restart_interaction()

        # RCG scene (cum layers use ConditionSwitch, just restart interaction)
        elif store._rcg_girl is not None and store._rcg_girl is girl:
            renpy.restart_interaction()

        # Cowgirl scene (cum layers use ConditionSwitch, just restart interaction)
        elif store._cowgirl_girl is not None and store._cowgirl_girl is girl:
            renpy.restart_interaction()

        # Doggy scene (cum layers use ConditionSwitch, just restart interaction)
        elif store._doggy_girl is not None and store._doggy_girl is girl:
            renpy.restart_interaction()

        # LD scene (cum layers use ConditionSwitch, just restart interaction)
        elif store._laying_girl is not None and store._laying_girl is girl:
            renpy.restart_interaction()

        # FN scene — must re-show cum layers explicitly (not ConditionSwitch)
        elif store._fn_girl is not None and store._fn_girl is girl:
            _fn_gid = gid
            _fn_cum = getattr(girl, "Cum", [])
            _fn_slot_tf = fn_get_slot_transform(0, anal=store.fn_anal)
            if "ass" in _fn_cum:
                renpy.show("%s fn_cum_ass" % _fn_gid, tag="fn_cum_ass", at_list=[_fn_slot_tf], zorder=9965)
            if "boobs" in _fn_cum:
                _fn_has_top = girl.clothes.get("chest") is not None and girl.clothes_state.get("chest") not in ("down", None)
                _fn_cum_boobs_at = [_fn_slot_tf] if _fn_has_top else [_fn_slot_tf, fn_get_chest_transform(0, anal=store.fn_anal)]
                renpy.show("%s fn_cum_boobs" % _fn_gid, tag="fn_cum_boobs", at_list=_fn_cum_boobs_at, zorder=9996)
            if "dripping_ass" in _fn_cum and not store.fn_anal:
                if _fn_gid == "tenny":
                    renpy.show("tenny fn_after_ass_anim", tag="fn_after_ass", at_list=[_fn_slot_tf], zorder=9991)
                else:
                    renpy.show("%s fn_cum_ass_inside" % _fn_gid, tag="fn_cum_ass_inside", at_list=[_fn_slot_tf], zorder=9991)
            if "dripping" in _fn_cum:
                # anal: above the torso (9990) but below the anal action art (9994), never over the
                # visible penetration (author 2026-10-11); vaginal: below the penis (9988)
                _cp2_z = 9991 if store.fn_anal else 9987
                if _fn_gid == "tenny":
                    renpy.show("tenny fn_after_pussy_anim", tag="fn_after_pussy", at_list=[_fn_slot_tf], zorder=_cp2_z)
                else:
                    renpy.show("%s fn_cum_inside_pussy_2" % _fn_gid, tag="fn_cum_inside_pussy_2", at_list=[_fn_slot_tf], zorder=_cp2_z)
            if "dripping" in _fn_cum or "dripping_ass" in _fn_cum:
                _fn_pen_tf = fn_get_penis_transform(0, anal=store.fn_anal)
                renpy.show("%s fn_cum_penis" % _fn_gid, tag="fn_cum_penis", at_list=[_fn_pen_tf], zorder=9988)
            if "face" in _fn_cum:
                _fn_head_tf = [_fn_slot_tf, fn_get_head_transform(0)]
                renpy.show("%s fn_cum_face" % _fn_gid, tag="fn_cum_face", at_list=_fn_head_tf, zorder=10000)
            renpy.restart_interaction()
            print("[FN_REFRESH_CUM] showed cum layers: %s" % _fn_cum)

    def _girl_angry_abort(girl, days=1, reason=None, love_penalty=0):
        """Set girl angry for N days and abort the scene.
        Call force_scene_reset + jump main_loop from the label side."""
        if love_penalty:
            Change_Status(girl, "Love", love_penalty)
        girl.set_temp_status("angry", days, reason=reason)

    # ---------------------------------------------------------
    # Shared slap system — expression per trait per scene
    # Returns (eyes, mouth, brows)
    # ---------------------------------------------------------
    SLAP_EXPR_BJ = {
        "hardcore_sex": {
            "eyes":  ["ahegao", "ahegao_2", "up_right_closed", "up_left_closed"],
            "mouth": ["mouth_happy", "mouth_lipbite", "mouth_tongue"],
            "brows": [1, 2],
        },
        "cute_sex": {
            "eyes":  ["looking_right", "looking_left", "closed_happy"],
            "mouth": ["mouth_sad", "mouth_surprised"],
            "brows": [3, 4],
        },
        "_default": {
            "eyes":  ["squint", "squint_2", "closed_happy"],
            "mouth": ["mouth_surprised", "mouth_smile"],
            "brows": [1, 2, 3],
        },
    }

    SLAP_EXPR_HJ = {
        "hardcore_sex": {
            "eyes":  ["eyes_squint_big", "eyes_surprised_2", "eyes_left_closed"],
            "mouth": ["mouth_smile", "mouth_tongue", "mouth_laugh"],
            "brows": ["brows_normal", "brows_surprised"],
        },
        "cute_sex": {
            "eyes":  ["eyes_side", "eyes_side_2", "eyes_closed"],
            "mouth": ["mouth_sad", "mouth_surprised"],
            "brows": ["brows_confused", "brows_sad"],
        },
        "_default": {
            "eyes":  ["eyes_squint", "eyes_squint_2", "eyes_surprised"],
            "mouth": ["mouth_surprised", "mouth_normal"],
            "brows": ["brows_normal", "brows_confused"],
        },
    }

    def _slap_pick_expression(girl, scene_type="bj"):
        """Returns (eyes, mouth, brows) for slap reaction."""
        pool = SLAP_EXPR_BJ if scene_type == "bj" else SLAP_EXPR_HJ
        # a cum_slut begs for slaps like a hardcore girl (same precedence as SpankHer): she gets the horny faces
        for t in ("hardcore_sex", "cum_slut", "cute_sex"):
            if girl.has_trait(t):
                p = pool["hardcore_sex" if t == "cum_slut" else t]
                return (renpy.random.choice(p["eyes"]), renpy.random.choice(p["mouth"]), renpy.random.choice(p["brows"]))
        p = pool["_default"]
        return (renpy.random.choice(p["eyes"]), renpy.random.choice(p["mouth"]), renpy.random.choice(p["brows"]))

    def _player_cleanup(girl):
        """Remove penis cum from girl and restart interaction."""
        cum = getattr(girl, "Cum", [])
        if "penis" in cum:
            cum.remove("penis")
            girl.Cum = cum
        renpy.restart_interaction()

    def _remove_cum_tag(girl, tag):
        """Remove a specific cum tag from girl.Cum and refresh visuals."""
        cum = getattr(girl, "Cum", [])
        if tag in cum:
            cum.remove(tag)
            girl.Cum = cum
        gid = girl.gid
        if tag == "mouth":
            girl._mouth_cum_persist = False
            renpy.hide("%s_bj_cum_mouth" % gid)
            renpy.hide("%s_hj_cum_mouth" % gid)
        renpy.restart_interaction()

    # ---------------------------------------------------------
    # Cleanup permission check
    # ---------------------------------------------------------
    def CumCleanupCheck(girl, action):
        """
        Check if girl will accept a cleanup action ("eat" or "leave").
        Traits:
          cum_slut: always allows eat, bonus for leave
          hate_cum: never allows eat or leave
          public_fetish: big bonus for leave
          public_shy: penalty for leave, but gains Obed if forced
        Returns ApprovalCheck result dict.
        """
        cfg = CUM_CLEANUP_RULES.get(action, {"T": 600, "Type": "LOI", "Spread": 160, "Variation": 40})

        # cum_slut: auto-accept eat, big bonus for leave
        if girl.has_trait("cum_slut"):
            if action == "eat":
                return {"accepted": True, "outcome": "hard_allow", "score": 9999, "tier": 4, "reasons": ["cum_slut"]}
            elif action == "leave":
                return ApprovalCheck(girl=girl, T=cfg["T"], Type=cfg["Type"],
                    Spread=cfg["Spread"], Bonus=300, Variation=cfg.get("Variation", 0), ReturnData=True)

        # hate_cum: auto-deny eat and leave
        if girl.has_trait("hate_cum"):
            if action in ("eat", "leave"):
                return {"accepted": False, "outcome": "hard_deny", "score": 0, "tier": 0, "reasons": ["hate_cum"]}

        bonus = 0
        if action == "leave":
            # Bonus from public exposure / exhibitionist acts
            action_log = getattr(girl, "ActionLog", {})
            public_acts = 0
            for k, v in action_log.items():
                if "saw" in k or "caught" in k or "expose" in k:
                    public_acts += v
            bonus = min(300, public_acts * 25)

            # public_fetish: big bonus for leaving cum on body
            if girl.has_trait("public_fetish"):
                bonus += 350

            # exhibitionist: loves walking around dirty, bonus for leave
            if girl.has_trait("exhibitionist"):
                bonus += 400

            # public_shy: penalty for leaving cum on body
            if girl.has_trait("public_shy"):
                bonus -= 250

        return ApprovalCheck(
            girl=girl,
            T=cfg["T"],
            Type=cfg["Type"],
            Spread=cfg["Spread"],
            Bonus=bonus,
            Variation=cfg.get("Variation", 0),
            ReturnData=True,
        )

# ============================================================
# 3. REN'PY LABELS
# ============================================================

# ------------------------------------------------------------
# Non-scene orgasm — triggers when Lust >= 100 outside sex scenes
# ------------------------------------------------------------
label _nonscene_orgasm(girl):
    $ debug_log("[NONSCENE_ORGASM] %s Lust=%d" % (girl.gid, girl.Lust))
    call GirlCumming(girl, "touch", "standing") from _call_GirlCumming_nonscene

    $ _ns_line = scene_pick_line("girl_nonscene_orgasm", scene="touch", girl=girl)
    if _ns_line:
        $ Say_Line(girl, _ns_line)

    return

# ------------------------------------------------------------
# Dispatch labels — route to position-specific labels via config
# ------------------------------------------------------------
label _cum_dispatch_anim(girl, scene_type):
    $ _lbl = _cum_cfg(scene_type, "cum_anim")
    if _lbl:
        call expression _lbl pass (girl) from _call__cum_dispatch_anim_inner
    return

label _cum_dispatch_fire_away(girl, scene_type):
    $ _lbl = _cum_cfg(scene_type, "fire_away_anim")
    if _lbl:
        call expression _lbl pass (girl) from _call__cum_dispatch_fire_inner
    return

label _cum_dispatch_outside_freeze(girl, scene_type):
    $ _lbl = _cum_cfg(scene_type, "outside_freeze")
    if _lbl:
        call expression _lbl pass (girl) from _call__cum_dispatch_freeze_inner
    return

label _cum_dispatch_condom_remove(girl, scene_type):
    $ _lbl = _cum_cfg(scene_type, "condom_remove_anim")
    if _lbl:
        call expression _lbl pass (girl) from _call__cum_dispatch_condom_inner
    return

label _cum_dispatch_apply_speed(girl, scene_type, speed=None):
    python:
        _as_lbl = _cum_cfg(scene_type, "apply_speed_label")
        if speed is not None:
            _as_spd = speed
        else:
            _as_var = _cum_cfg(scene_type, "speed_var")
            _as_spd = getattr(store, _as_var, 0) if _as_var else 0
    if _as_lbl:
        call expression _as_lbl pass (girl, _as_spd) from _call__cum_as_dispatch
    return

label _cum_dispatch_condom_visual(girl, scene_type):
    call _cum_dispatch_condom_remove(girl, scene_type) from _call__cdcv_remove
    call _cum_dispatch_apply_speed(girl, scene_type) from _call__cdcv_speed
    return

label _cum_dispatch_hole_transition(girl, scene_type, to_anal=True):
    $ _ht_lbl = _cum_cfg(scene_type, "hole_transition_label")
    if _ht_lbl:
        call expression _ht_lbl pass (girl, to_anal) from _call__cum_ht_dispatch
    return

label _cum_dispatch_end(girl, scene_type, dress_up=False):
    $ _lbl = _cum_cfg(scene_type, "end_label")
    if _lbl:
        call expression _lbl pass (girl, dress_up=dress_up) from _call__cum_dispatch_end_inner
    return

label _cum_dispatch_aftermath(girl, scene_type, drip_check=True, consented=None):
    python:
        if consented is None:
            consented = store._creampie_consent in ("allowed", "changed_mind")
    $ _lbl = _cum_cfg(scene_type, "creampie_aftermath")
    if not _lbl:
        return
    if drip_check and "dripping" not in getattr(girl, "Cum", []) and "dripping_ass" not in getattr(girl, "Cum", []):
        return
    call CreampieAftermath_Central(girl, scene_type, consented=consented) from _call_ca_central_dispatch
    return

# ============================================================
# Tip-Outside — centralized "Ask to cum inside" / force flows
# ============================================================
label _tip_ask_cum_inside(girl, scene_type):
    $ print("[TIP_CUM] ask_inside scene=%s girl=%s" % (scene_type, girl.gid))
    $ _cum_check = CumPermissionCheck(girl, "cum_inside_ask")
    if _cum_check["accepted"]:
        $ Say_Line(girl, scene_pick_line("cum_inside_accepted", scene=scene_type, girl=girl) or _("Okay... do it. Cum inside."))
        $ store._creampie_consent = "allowed"
        call _cum_dispatch_anim(girl, scene_type) from _call_tip_ask_anim
        "You push deeper and cum inside her."
        $ process_cum(girl, scene_type, "inside")
        $ apply_cum_bonuses(girl, "cum_inside_allowed")
    else:
        $ Say_Line(girl, scene_pick_line("cum_inside_denied", scene=scene_type, girl=girl) or _("No! Pull out!"))
        call _cum_dispatch_outside_freeze(girl, scene_type) from _call_tip_ask_freeze
        $ _tip_cum_type = _cum_cfg(scene_type, "tip_outside_cum_type", "outside")
        if _tip_cum_type == "ass":
            "You pull out and cum on her ass."
        else:
            "You pull out and cum on her."
        $ process_cum(girl, scene_type, _tip_cum_type)
        $ _tip_vis = _cum_cfg(scene_type, "tip_outside_visual")
        if _tip_vis:
            call expression _tip_vis pass (girl) from _call_tip_ask_vis
        $ apply_cum_bonuses(girl, "cum_outside")
    return

label _tip_force_cum_inside(girl, scene_type):
    $ print("[TIP_CUM] force_inside scene=%s girl=%s" % (scene_type, girl.gid))
    $ store._cum_forced_surprise = not (girl.has_trait("cum_slut") or girl.has_trait("hardcore_sex"))
    call _cum_dispatch_anim(girl, scene_type) from _call_tip_force_anim
    "You push all the way in and cum deep inside her."
    $ process_cum(girl, scene_type, "inside")
    $ _cum_check = CumPermissionCheck(girl, "cum_inside_ask")
    if _cum_check["accepted"]:
        $ store._creampie_consent = "allowed"
        $ apply_cum_bonuses(girl, "cum_inside_allowed")
        $ _ci_line = scene_pick_line("cum_inside_accepted", scene=scene_type, girl=girl) or _("Mmm... I felt that.")
        $ Say_Line(girl, _ci_line)
    else:
        # Forced creampie — same handling as PlayerCumMenu_Penetration_Raw
        python:
            _is_hate_cum = girl.has_trait("hate_cum")
            _is_cum_slut = girl.has_trait("cum_slut")
            _ci_anal_lover_anal = scene_type in _ANAL_SCENE_TYPES and girl.has_trait("anal_lover")
            _ci_lust = getattr(girl, "Lust", 0)
        $ store._creampie_consent = "denied"
        $ store._forced_creampie_count += 1
        if not _is_cum_slut and not _ci_anal_lover_anal:
            $ apply_cum_penalties(girl, "cum_inside_forced", scene_type)

        if _is_hate_cum:
            $ store._witness_expression_lock = True
            $ set_scene_expression(girl, "angry", brows="brows_maniac")
            $ _cf_line = scene_pick_line("cum_inside_forced", scene=scene_type, girl=girl) or _("What?! I told you not to! You came inside me?!")
            $ Say_Line(girl, _cf_line)
            call _hate_cum_angry_end(girl, scene_type) from _call_hate_cum_tip_force

        elif _is_cum_slut or _ci_anal_lover_anal:
            $ _ci_refused = _creampie_was_refused()
            $ store._creampie_consent = "allowed"
            $ apply_cum_bonuses(girl, "cum_inside_allowed")
            $ _ci_line = _cream_liked_line(girl, scene_type, _ci_refused)
            $ Say_Line(girl, _ci_line)

        elif _ci_lust >= 90:
            python:
                _lust_lines = [
                    _("Son of a bitch! I can't stop nowww, I'm almost cumming...!"),
                    _("You asshole! I told you not to... ngh... but I'm so close... fuck!"),
                    _("Are you serious?! I... ahhh... god damn it, I can't stop now...!"),
                    _("You came inside me?! I'm gonna... nnh... I hate you... but don't stop...!"),
                ]
            $ Say_Line(girl, _tl(renpy.random.choice(_lust_lines)))
            $ Change_Status(girl, "Love", -30)
            $ store._forced_creampie_end_after_orgasm = True

        else:
            $ store._witness_expression_lock = True
            $ set_scene_expression(girl, "angry", brows="brows_maniac")
            $ _cf_line = scene_pick_line("cum_inside_forced", scene=scene_type, girl=girl) or _("What?! I told you not to! You came inside me?!")
            $ Say_Line(girl, _cf_line)
            call _forced_creampie_angry_end(girl, scene_type) from _call_forced_cream_tip_force

    return

# ============================================================
# CreampieAftermath_Central — expression + visual + dialogue
# ============================================================
label CreampieAftermath_Central(girl, scene_type, consented=True):
    python:
        _ca_is_anal = scene_type in _ANAL_SCENE_TYPES
        _ca_expr, _ca_ov = _ca_resolve_expression(girl, consented, _ca_is_anal)
        set_scene_expression(girl, _ca_expr, blush=_ca_ov.get("blush"))

    $ _ca_vis = _cum_cfg(scene_type, "creampie_aftermath")
    if _ca_vis:
        call expression _ca_vis pass (girl) from _call_ca_visual

    python:
        _ca_key = "creampie_aftermath_forced" if not consented else "creampie_aftermath"
        _ca_line = scene_pick_line(_ca_key, scene=scene_type, girl=girl)
        if _ca_line:
            _ca_line = _format_partner_line(girl, _ca_line)
        print("[CREAM_CENTRAL] key=%s scene=%s consented=%s line=%s" % (_ca_key, scene_type, consented, _ca_line[:40] if _ca_line else "None"))
    if _ca_line:
        $ Say_Line(girl, _ca_line)

    # First creampie + partner stats (migrated from _first_creampie_bf_reaction)
    python:
        _fc_cc = getattr(girl, "CreampieCounts", 0)
        _fc_session = getattr(store, "_session_cum", {}).get("inside", 0)
        _fc_has_partner = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        if _fc_cc == 1 and _fc_session >= 1 and _fc_has_partner:
            _fc_cat = _resolve_first_creampie_category(girl)
            _fc_stats = FIRST_CREAMPIE_PARTNER_STATS.get(_fc_cat, FIRST_CREAMPIE_PARTNER_STATS["neutral"])
            for _fc_stat, _fc_val in _fc_stats.items():
                if _fc_stat == "Lust":
                    girl.Lust = min(100, getattr(girl, "Lust", 0) + _fc_val)
                else:
                    Change_Status(girl, _fc_stat, _fc_val)
            if not girl.get_flag("partner_is_female"):
                girl.discover("discovered_bf_never_creampie")
            _discover_partner(girl)
            print("[CREAM_CENTRAL] first_creampie partner stats: cat=%s" % _fc_cat)

    $ renpy.pause(0.5)
    return

# ------------------------------------------------------------
# CondomMidsceneMenu... remove condom during sex (control menu)
# ------------------------------------------------------------
label CondomMidsceneMenu(girl, scene_type):

    # Restricted scene gate: she demanded the condom, it stays (marital bed, etc.)
    if getattr(store, "_scene_restricted", False):
        python:
            _restr_condom_deny = [
                _("Don't touch the condom. I told you how this works."),
                _("The condom stays on. I'm in charge here, remember?"),
                _("No. You don't get to decide that. Not tonight."),
            ]
        $ Say_Line(girl, _tl(renpy.random.choice(_restr_condom_deny)))
        return

    # NTR gate: if partner watching and boundary requires condom, block removal
    if store._ntr_partner_watching and store._ntr_watching_npc:
        call _ntr_escalation_gate(girl, "condom_remove") from _call_ntr_gate_condom_mid
        if not store._ntr_gate_passed:
            return

    # Story step gate: her step locks going raw = condom stays, no discussion
    if story_act_locked(girl, "raw"):
        python:
            _story_condom_deny = [
                _("The condom stays on. That's not up for discussion."),
                _("Don't touch the condom. I said we use protection, and I meant it."),
                _("No. The condom stays. I'm not negotiating this."),
            ]
        $ set_scene_expression(girl, "angry")
        $ Say_Line(girl, _tl(renpy.random.choice(_story_condom_deny)))
        return

    # Cheat path gate: condom stays unless heat + stats are high enough
    if _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False):
        python:
            _heat = getattr(girl, "_cheat_heat", 0)
            _cm_obed_cheat = getattr(girl, "Obed", 0)
            _cm_inbt_cheat = getattr(girl, "Inbt", 0)
            _cm_lust_cheat = getattr(girl, "Lust", 0)
            # High heat + high stats: she can be convinced (difficult but possible)
            _cheat_raw_ok = (
                _heat >= 80 and _cm_obed_cheat >= 500 and _cm_inbt_cheat >= 300
            ) or (
                _heat >= 90 and _cm_lust_cheat >= 80
            ) or girl.has_trait("cum_slut")
        if not _cheat_raw_ok:
            python:
                _deny_lines = [
                    _("Don't even think about it. The condom stays on."),
                    _("No. I told you, that's the deal. Keep it on."),
                    _("Are you serious? It stays on. End of discussion."),
                    _("I already told you my conditions. The condom stays."),
                ]
            $ Say_Line(girl, _tl(renpy.random.choice(_deny_lines)))
            return

    python:
        _cm_inbt = getattr(girl, "Inbt", 0)
        _cm_obed = getattr(girl, "Obed", 0)
        _cm_lust = getattr(girl, "Lust", 0)
        _cm_raw = getattr(girl, "raw_sex_count", 0)
        _cm_is_first_raw = _cm_raw == 0
        _cm_has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        _cm_is_cum_slut = girl.has_trait("cum_slut")
        _cm_is_hate_cum = girl.has_trait("hate_cum")
        _cm_is_cheater = girl.has_trait("cheater") or getattr(girl, "CheatAttitude", 0) >= 5
        _cm_player_has_gf = player_has_girlfriend(ALL_GIRLS) and not girl.is_dating_player() and not is_player_harem_exempt(girl)

    menu:
        "Ask her to remove it":
            call _condom_ask_remove(girl, scene_type) from _call__condom_ask_remove

        "Just remove it":
            call _condom_force_remove(girl, scene_type) from _call__condom_force_remove

        "Never mind":
            pass

    return

# ── Ask Her to Remove Condom ─────────────────────────────────
label _condom_ask_remove(girl, scene_type):

    python:
        _cm_inbt = getattr(girl, "Inbt", 0)
        _cm_obed = getattr(girl, "Obed", 0)
        _cm_lust = getattr(girl, "Lust", 0)
        _cm_raw = getattr(girl, "raw_sex_count", 0)
        _cm_is_first_raw = _cm_raw == 0
        _cm_has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        _cm_is_f = girl.get_flag("partner_is_female") if _cm_has_bf else False
        _cm_bf_f = partner_fmt(girl)
        _cm_is_cum_slut = girl.has_trait("cum_slut")
        _cm_is_hate_cum = girl.has_trait("hate_cum")
        _cm_is_cute = girl.has_trait("cute_sex")
        _cm_is_hardcore = girl.has_trait("hardcore_sex")
        _cm_is_cheater = girl.has_trait("cheater") or getattr(girl, "CheatAttitude", 0) >= 5
        _cm_player_has_gf = player_has_girlfriend(ALL_GIRLS) and not girl.is_dating_player() and not is_player_harem_exempt(girl)
        _cm_recording = getattr(store, "_recording_active", False) and getattr(store, "_recording_girl", None) == girl
        _cm_is_dating = girl.is_dating_player()
        _cm_bf_did_sex = _cm_has_bf and hasattr(girl, "bf_has_done") and girl.bf_has_done("sex")

        # ── Determine outcome ──
        _cm_result = "deny"

        if _cm_is_hate_cum:
            _cm_cream = getattr(girl, "CreampieCounts", 0)
            if _cm_cream >= 1 or _cm_raw >= 3:
                _cm_result = "accept_hate_cum"
            else:
                _cm_result = "hard_deny"
        elif _cm_is_cum_slut and _cm_inbt >= 200:
            _cm_result = "accept"
        elif _cm_is_cum_slut and _cm_inbt < 200:
            _cm_result = "soft_deny"
        elif _cm_obed >= 600 and _cm_inbt >= 300:
            _cm_result = "accept"
        elif _cm_lust >= 80 and _cm_inbt >= 400 and _cm_raw >= 3:
            _cm_result = "accept"
        elif _cm_lust >= 70 and _cm_raw >= 5:
            _cm_result = "accept"
        elif _cm_lust >= 60 and _cm_inbt >= 300:
            _cm_result = "soft_deny"
        else:
            _cm_result = "deny"

    # ── ACCEPT (hate_cum exception) ──
    if _cm_result == "accept_hate_cum":
        $ set_scene_expression(girl, "worried")
        python:
            if _cm_has_bf:
                _hc_lines = [
                    _("Fine... take it off. But do NOT cum inside me. I mean it. Not a single drop."),
                    _("Okay... raw. But if you finish inside me, we're done. I'm not joking."),
                    _("I'll let you take it off... but you pull out. No exceptions. My %(pl)s would kill us both."),
                ]
            elif _cm_player_has_gf:
                _hc_lines = [
                    _("Take it off. But you're pulling out. Your girlfriend can deal with your mess, not me."),
                    _("Fine... but NOT inside me. I don't care how good it feels. Pull. Out."),
                ]
            else:
                _hc_lines = [
                    _("Fine... take it off. But you are NOT finishing inside me. Understood?"),
                    _("Okay. But pull out. I'm serious. Don't you dare cum inside me."),
                    _("I'll let you go raw... but the second you're close, you pull out. No discussion."),
                    _("Take it off... but if I feel even a drop inside me, I swear to god..."),
                ]
            _hc_line = _tl(renpy.random.choice(_hc_lines)) % _cm_bf_f

        $ Say_Line(girl, _hc_line)
        $ set_scene_expression(girl, "angry")
        $ _cr_blocked = _on_condom_removed(girl, skip_hide=_cum_skip_hide(scene_type))
        if not _cr_blocked:
            $ apply_cum_bonuses(girl, "condom_removed_allowed")
            $ girl.discover("discovered_trait_hate_cum")
            $ store._creampie_consent = "blocked"
            "She lets you remove the condom, but makes it clear: no finishing inside."
            $ set_scene_expression(girl, "normal")

    # ── ACCEPT ──
    elif _cm_result == "accept":
        python:
            _cm_line_trait = None   # set by the trait branches: only the pool that SPOKE discovers
            # Priority order: most specific context first
            # 1. First raw + cheater bf + player has gf (triple betrayal)
            if _cm_is_first_raw and _cm_has_bf and _cm_is_cheater and _cm_player_has_gf:
                _ask_lines = [
                    _("First time raw... behind my %(pl)s's back AND yours? God, this is so wrong. Take it off."),
                    _("Neither of them will ever know... your girlfriend, my %(pl)s... take it off. I want this."),
                ]
                if _cm_bf_did_sex:
                    _ask_lines.append(_("My %(pl)s always wraps it. Your girlfriend probably thinks you do too. Let's both be terrible. Take it off."))
            # 2. First raw + has boyfriend
            elif _cm_is_first_raw and _cm_has_bf:
                _ask_lines = [
                    _("I've never gone raw with anyone... not even %(po)s. You'll be the first. Take it off."),
                    _("My %(pl)s would lose %(poss)s mind if %(pp)s knew I'm letting you do this. Take it off."),
                ]
                if _cm_bf_did_sex:
                    _ask_lines.extend([
                        _("My %(pl)s always uses a condom... but okay. Take it off. I want to feel what it's like without one."),
                        _("%(Pp)s always wraps it. Always. But with you... I want to know what I've been missing."),
                    ])
            # 3. First raw + player has gf
            elif _cm_is_first_raw and _cm_player_has_gf:
                _ask_lines = [
                    _("My first time raw... and it's with someone who has a girlfriend. What am I doing? ...Take it off."),
                    _("I've never done it without one. Does your girlfriend let you go raw? ...Forget it. Take it off."),
                    _("First time without a condom and you're cheating on your girlfriend to do it... just take it off."),
                ]
            # 4. First raw (no bf, no player gf)
            elif _cm_is_first_raw and _cm_is_cute:
                _ask_lines = [
                    _("I've never... without one... I'm really nervous. But I trust you. Please be gentle. Take it off."),
                    _("This is my first time raw... my heart is pounding. But I want to feel close to you. Take it off."),
                    _("No one's ever been inside me without a condom... promise me you'll be careful? ...Okay. Take it off."),
                ]
            elif _cm_is_first_raw and _cm_is_hardcore:
                _ask_lines = [
                    _("First time raw? Let's fucking do it. Take it off. I want to feel everything."),
                    _("I've been saving this. No more plastic between us. Rip it off."),
                    _("About time someone asked. Take it off and don't hold back."),
                ]
            elif _cm_is_first_raw:
                _ask_lines = [
                    _("I've never done it without one before... but okay. I trust you. Take it off."),
                    _("This is my first time raw... I'm nervous. But I want it."),
                    _("I've always been careful... but something about you makes me want to throw caution away."),
                    _("No one's ever been inside me without a condom. You'll be the first."),
                ]
            # 5. Cheater + has bf (not first raw)
            elif _cm_is_cheater and _cm_has_bf:
                _ask_lines = [
                    _("My %(pl)s and I always use one. But I don't want that with you. Take it off."),
                    _("%(Pp)s wraps it every time. So obedient. You? I want to feel you raw. Take it off."),
                    _("The thrill of going raw behind %(poss)s back... I can't resist. Do it."),
                    _("My %(pl)s doesn't know how good raw feels... because I never let %(po)s. You though? Take it off."),
                ]
            # 6. Has bf (not cheater, not first raw)
            elif _cm_has_bf:
                _ask_lines = [
                    _("My %(pl)s doesn't even know I do this with you... let alone raw. Go ahead."),
                    _("%(Pp)s always uses protection. With you? I don't want any barriers."),
                    _("If %(pp)s knew I was letting you go raw... take it off. I can't resist you."),
                ]
            # 7. Cheater + player has gf (taunting)
            elif _cm_is_cheater and _cm_player_has_gf:
                _ask_lines = [
                    _("Your girlfriend would be so angry if she saw you fucking me raw... take it off."),
                    _("Does your girlfriend let you go raw? Because I will. Take it off."),
                    _("She probably thinks you're being faithful right now... take the condom off and prove her wrong."),
                    _("Raw? Behind your girlfriend's back? God, that's hot. Do it."),
                    _("I wonder if she'd cry or scream if she found out. Either way... take it off."),
                ]
            # 8. Player has gf (not cheater)
            elif _cm_player_has_gf:
                _ask_lines = [
                    _("You have a girlfriend and you want to go raw with me...? Fine. Take it off."),
                    _("Your girlfriend would hate this... but okay. I want to feel you."),
                    _("This feels wrong knowing you're with someone... but I want it. Take it off."),
                ]
            # 9. Recording active
            elif _cm_recording:
                _ask_lines = [
                    _("You're recording this AND asking me to go raw? ...Fine. Make it a good video. Take it off."),
                    _("On camera, without a condom? You're insane. ...Okay. Take it off."),
                    _("You want to film me taking it raw? ...I can't believe I'm saying yes. Do it."),
                ]
            # 10. Trait-specific (no special context). Not her first raw: a cum_slut still discovering it wants it, no hate yet
            elif _cm_is_cum_slut and not trait_is_veteran(girl, "cum_slut"):
                _cm_line_trait = "cum_slut"
                _ask_lines = [
                    _("Take it off... I keep thinking about how it felt without it."),
                    _("Yes... take it off. I want to feel you again."),
                    _("Okay... I won't pretend I didn't want you to ask."),
                ]
            elif _cm_is_cum_slut:
                _cm_line_trait = "cum_slut"
                _ask_lines = [
                    _("Finally! Take that thing off! I need to feel you raw!"),
                    _("YES! Get rid of it! I want every inch!"),
                    _("About time you asked... I've been dying to feel you bare."),
                    _("I HATE condoms. Take it off and give me everything."),
                ]
            elif _cm_is_cute:
                _cm_line_trait = "cute_sex"
                _ask_lines = [
                    _("Okay... I want to feel closer to you. Take it off. Just be gentle."),
                    _("I trust you... take it off. I want it to be just us, nothing between us."),
                    _("Take it off... I want to feel every part of you inside me."),
                ]
            elif _cm_is_hardcore:
                _cm_line_trait = "hardcore_sex"
                _ask_lines = [
                    _("Take it off. I want the real thing. Raw. Now."),
                    _("Rip it off. I don't want anything between us."),
                    _("Finally. Get rid of it and fuck me properly."),
                ]
            # 11. Default
            else:
                _ask_lines = [
                    _("Okay... take it off. I want to feel you."),
                    _("Go ahead... I want you inside me properly."),
                    _("Take it off... I need to feel the real thing."),
                    _("Alright. I want to feel you without it. Take it off."),
                ]

            _ask_line = _tl(renpy.random.choice(_ask_lines)) % _cm_bf_f

        $ Say_Line(girl, _ask_line)
        $ _cr_blocked = _on_condom_removed(girl, skip_hide=_cum_skip_hide(scene_type))
        if _cr_blocked:
            return
        $ apply_cum_bonuses(girl, "condom_removed_allowed")
        # She accepted removal -- cum inside is implicitly allowed
        $ store._creampie_consent = "allowed"
        $ store._creampie_warned = True
        # Discovery flags: the trait whose pool spoke; cheating is the DEED (she has a partner and accepted)
        if _cm_line_trait:
            $ girl.discover("discovered_trait_%s" % _cm_line_trait)
        if girl.has_trait("cheater") and _cm_has_bf:
            $ girl.discover("discovered_trait_cheater")
        if _cm_has_bf:
            $ _discover_partner(girl)
            $ girl.discover("discovered_bf_never_sex_raw")
            if _cm_is_first_raw:
                $ girl.discover("discovered_bf_done_sex")
        "She lets you remove the condom."

    # ── SOFT DENY ──
    elif _cm_result == "soft_deny":
        python:
            if _cm_is_cum_slut:
                _soft_lines = [
                    _("I... I want to, but... it's embarrassing to admit. Can we keep it on for now?"),
                    _("Part of me really wants to say yes... but I'm not ready to go there yet."),
                ]
            elif _cm_has_bf and _cm_player_has_gf:
                _soft_lines = [
                    _("We're both cheating on someone... and you want to go raw too? That's... a lot. Not yet."),
                    _("I have a %(pl)s, you have a girlfriend... the condom is the last bit of sanity here."),
                ]
            elif _cm_has_bf:
                _soft_lines = [
                    _("I'm already cheating on %(po)s... going raw feels like another line I shouldn't cross."),
                    _("This is already bad enough with a condom on... without one? I don't know..."),
                ]
                if _cm_bf_did_sex:
                    _soft_lines.append(_("My %(pl)s and I always use protection. I can't... not yet."))
                else:
                    _soft_lines.append(_("I have a %(pl)s... I should not go raw..."))
            elif _cm_player_has_gf:
                _soft_lines = [
                    _("You have a girlfriend... and you want to go raw with me? That's... I need to think about it."),
                    _("Going raw with someone who has a girlfriend... I'm not sure I can do that. Not yet."),
                ]
            elif _cm_is_cute:
                _soft_lines = [
                    _("I... I want to feel closer to you, but... I'm scared. Can we keep it on for now?"),
                    _("Maybe someday... but not today. I'm not ready. I'm sorry..."),
                    _("My heart says yes but my head says no... can we keep it on? Please?"),
                ]
            elif girl.has_trait("femdom"):
                _soft_lines = [
                    _("Tch... I want to, but not yet. Earn it first."),
                    _("Not yet. I'll tell you when you've earned it. Until then, it stays on."),
                    _("Ask nicely enough and maybe one day I'll say yes. Today the condom stays."),
                ]
            elif _cm_is_hardcore:
                _soft_lines = [
                    _("Ask me again when I trust you more. For now, the condom stays."),
                    _("Not raw, not yet. Keep it on and just fuck me harder instead."),
                ]
            else:
                _soft_lines = [
                    _("I... I'm not sure. Can we keep it on for now?"),
                    _("That's a big ask mid-session... I don't think I'm ready."),
                    _("Maybe next time? I want to, but not today."),
                ]
            _soft_line = _tl(renpy.random.choice(_soft_lines)) % _cm_bf_f

        $ Say_Line(girl, _soft_line)
        $ store._condom_removal_denied = True

    # ── HARD DENY (hate_cum) ──
    elif _cm_result == "hard_deny":
        $ set_scene_expression(girl, "angry")
        python:
            if _cm_recording:
                _hard_lines = [
                    _("You're recording AND asking to go raw?! Absolutely NOT! Are you trying to ruin my life?!"),
                    _("No! The condom stays on! Especially while that camera is running!"),
                ]
            elif _cm_has_bf:
                _hard_lines = [
                    _("Absolutely not. I have a %(pl)s and the condom stays on. Don't push it."),
                    _("No! I'm already doing something terrible. The condom is non-negotiable."),
                ]
            else:
                _hard_lines = [
                    _("Absolutely not. The condom stays on. Don't ask again."),
                    _("Are you insane? No. That's not happening."),
                    _("The condom stays. End of discussion."),
                    _("Don't even think about it. I said no."),
                ]
            _hard_line = _tl(renpy.random.choice(_hard_lines)) % _cm_bf_f

        $ Say_Line(girl, _hard_line)
        $ Change_Status(girl, "Love", -10)
        $ Change_Status(girl, "Obed", -5)
        $ store._creampie_consent = "blocked"
        $ store._condom_removal_denied = True
        $ set_scene_expression(girl, "normal")

    # ── DENY ──
    else:
        python:
            if _cm_has_bf and _cm_player_has_gf:
                _deny_lines = [
                    _("No. We both have partners. The condom is the bare minimum."),
                    _("Your girlfriend, my %(pl)s... and you want to go raw? No way."),
                ]
            elif _cm_has_bf:
                _deny_lines = [
                    _("No. I'm already doing enough behind %(poss)s back. The condom stays on."),
                    _("You want me to cheat on %(po)s AND go raw? That's too much."),
                    _("I have a %(pl)s. The condom is the least you can do."),
                ]
            elif _cm_player_has_gf:
                _deny_lines = [
                    _("You have a girlfriend. The condom stays. I'm not doing that."),
                    _("No. You're already cheating on her. Going raw is where I draw the line."),
                ]
            elif _cm_is_cute:
                _deny_lines = [
                    _("N-no... I'm not ready for that. Please don't be mad..."),
                    _("I can't... I'm sorry. I want the condom on. Please?"),
                ]
            elif girl.has_trait("femdom"):
                _deny_lines = [
                    _("No. You haven't earned that yet. Maybe if you impress me."),
                    _("Not happening. Show me you deserve it first."),
                    _("No. I decide when you get me raw, and today isn't that day."),
                ]
            elif _cm_is_hardcore:
                _deny_lines = [
                    _("No. Rough, sure. Raw, no. Keep it on."),
                    _("Not happening. Keep it on and fuck me like you mean it."),
                ]
            elif _cm_recording:
                _deny_lines = [
                    _("No! Especially not while you're recording! Keep the condom on!"),
                    _("Are you crazy? On camera AND raw? Absolutely not."),
                ]
            else:
                _deny_lines = [
                    _("No... keep it on, please."),
                    _("I'm not comfortable with that. Keep the condom."),
                    _("Not happening. I want it to stay on."),
                ]
            _deny_line = _tl(renpy.random.choice(_deny_lines)) % _cm_bf_f

        $ Say_Line(girl, _deny_line)
        $ Change_Status(girl, "Love", -5)
        $ store._condom_removal_denied = True

    return

# ── Force Remove Condom (without asking) ─────────────────────
label _condom_force_remove(girl, scene_type):

    # Stealth check: if she can't see, try to remove without her noticing
    # Cheat path girls are too vigilant about the condom for stealth
    if _can_stealth_remove(scene_type) and not (_is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False)):
        python:
            _stealth_chance = _stealth_condom_detect_chance(girl, scene_type)
            _stealth_detected = renpy.random.random() < _stealth_chance
            print("[STEALTH_CONDOM] attempt: chance=%.2f detected=%s" % (_stealth_chance, _stealth_detected))
        if not _stealth_detected:
            call _condom_stealth_success(girl, scene_type) from _call_stealth_success
            return
        python:
            _stealth_detect_narr = _tl(renpy.random.choice(_STEALTH_DETECT_NARR))
        "[_stealth_detect_narr]"

    python:
        _cm_inbt = getattr(girl, "Inbt", 0)
        _cm_obed = getattr(girl, "Obed", 0)
        _cm_lust = getattr(girl, "Lust", 0)
        _cm_raw = getattr(girl, "raw_sex_count", 0)
        _cm_is_first_raw = _cm_raw == 0
        _cm_has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        _cm_is_f = girl.get_flag("partner_is_female") if _cm_has_bf else False
        _cm_bf_f = partner_fmt(girl)
        _cm_is_cum_slut = girl.has_trait("cum_slut")
        _cm_is_hate_cum = girl.has_trait("hate_cum")
        _cm_is_cute = girl.has_trait("cute_sex")
        _cm_is_hardcore = girl.has_trait("hardcore_sex")
        _cm_is_cheater = girl.has_trait("cheater") or getattr(girl, "CheatAttitude", 0) >= 5
        _cm_player_has_gf = player_has_girlfriend(ALL_GIRLS) and not girl.is_dating_player() and not is_player_harem_exempt(girl)
        _cm_recording = getattr(store, "_recording_active", False) and getattr(store, "_recording_girl", None) == girl
        _cm_is_dating = girl.is_dating_player()
        _cm_bf_did_sex = _cm_has_bf and hasattr(girl, "bf_has_done") and girl.bf_has_done("sex")

        # ── Determine outcome ──
        _cm_result = "angry"  # default

        if _cm_is_hate_cum:
            _cm_result = "furious"
        elif _cm_is_cum_slut and _cm_obed >= 300:
            _cm_result = "accept"
        elif _cm_is_cum_slut and _cm_obed < 300:
            _cm_result = "shocked_accept"
        elif _cm_obed >= 700 and _cm_inbt >= 400:
            _cm_result = "accept"
        elif _cm_obed >= 500 and _cm_lust >= 80 and _cm_raw >= 3:
            _cm_result = "accept"
        elif _cm_lust >= 90 and _cm_raw >= 5:
            _cm_result = "accept"
        elif _cm_obed >= 400 and _cm_lust >= 70:
            _cm_result = "angry_continue"
        else:
            _cm_result = "angry"

    "You pull the condom off."

    # ── FURIOUS (hate_cum... condom stays, creampie blocked) ──
    if _cm_result == "furious":
        $ set_scene_expression(girl, "angry")
        python:
            if _cm_recording:
                _fury_lines = [
                    _("WHAT THE HELL?! You're RECORDING and trying to go raw?! PUT IT BACK ON!"),
                    _("Are you INSANE?! On camera AND without a condom?! PUT IT BACK RIGHT NOW!"),
                ]
            elif _cm_has_bf:
                _fury_lines = [
                    _("WHAT THE HELL?! My %(pl)s would NEVER do this! PUT IT BACK ON!"),
                    _("Are you INSANE?! I have a %(PL)s and you just... PUT IT BACK!"),
                ]
            else:
                _fury_lines = [
                    _("WHAT THE HELL?! PUT IT BACK ON RIGHT NOW!"),
                    _("Are you INSANE?! Don't you DARE touch me without that on!"),
                    _("You disgusting... put it back on or I'm DONE!"),
                    _("NO! What is WRONG with you?! Put it back on!"),
                ]
        $ Say_Line(girl, _tl(renpy.random.choice(_fury_lines)) % _cm_bf_f)
        $ Change_Status(girl, "Love", -30)
        $ Change_Status(girl, "Obed", -20)
        $ store._creampie_consent = "blocked"
        "You failed to remove the condom. She's furious."
        $ store._condom_removal_denied = True
        $ set_scene_expression(girl, "normal")
        return

    # ── ACCEPT (submissive / experienced) ──
    if _cm_result == "accept":
        python:
            _cm_line_trait = None   # set by the trait branches: only the pool that SPOKE discovers
            # cum_slut ALWAYS gets ironic lines (highest priority). Still discovering it (trait_is_new): no irony yet,
            # the first-raw / context lines below fit her
            if _cm_is_cum_slut and trait_is_veteran(girl, "cum_slut"):
                _cm_line_trait = "cum_slut"
                _fa_lines = [
                    _("Oh no... I feel so vulnerable now... what if you decide to fill up my poor little pussy?"),
                    _("Mmm... no condom? Whatever will I do if you cum inside me... oh wait, I WANT that."),
                    _("Finally! Now there's nothing between us... and nothing stopping you from filling me up."),
                    _("Oh no, the condom is gone! I'm SO scared of you cumming inside me... just kidding. DO IT."),
                ]
            # Most specific context first
            elif _cm_is_first_raw and _cm_has_bf and _cm_is_cheater and _cm_player_has_gf:
                _fa_lines = [
                    _("First time raw... behind both our partners' backs... you didn't even ask. That's so hot."),
                ]
                if _cm_bf_did_sex:
                    _fa_lines.append(_("You just... my %(pl)s always uses one. Your girlfriend doesn't know you're here. And now you're raw inside me... god."))
                else:
                    _fa_lines.append(_("You just... your girlfriend doesn't know you're here. My %(pl)s doesn't know either. And now we're raw... god."))
            elif _cm_is_first_raw and _cm_has_bf:
                _fa_lines = [
                    _("You just... I never even did this with %(po)s. And you just took it off like it's nothing..."),
                ]
                if _cm_bf_did_sex:
                    _fa_lines.extend([
                        _("Wait... you... oh god. My %(pl)s always uses one. You're the first to... mmm..."),
                        _("%(Pp)s always wears one. Always. And you just... oh... I can feel everything..."),
                    ])
                else:
                    _fa_lines.extend([
                        _("Wait... you... oh god. You just took it off... I can feel everything..."),
                        _("My %(pl)s would kill me if %(pp)s knew... and you just... oh..."),
                    ])
            elif _cm_is_first_raw and _cm_player_has_gf:
                _fa_lines = [
                    _("You just took it off... my first time raw and it's with someone who has a girlfriend... oh god..."),
                    _("First time without a condom and you didn't even ask... does your girlfriend know you do this?"),
                ]
            elif _cm_is_first_raw and _cm_is_cute:
                _cm_line_trait = "cute_sex"
                _fa_lines = [
                    _("Y-you just... that was my first time without... oh... it feels so different... so warm..."),
                    _("I've never... without one... you didn't even ask me... but... it feels incredible..."),
                ]
            elif _cm_is_first_raw and _cm_is_hardcore:
                _cm_line_trait = "hardcore_sex"
                _fa_lines = [
                    _("You just ripped it off... first time raw and you didn't even ask. I respect that. Keep going."),
                    _("Bold as fuck. First time without one and you just went for it. Don't stop."),
                ]
            elif _cm_is_first_raw:
                _fa_lines = [
                    _("You just... that's my first time without one. Oh... it feels so different..."),
                    _("I've never felt it raw before... you didn't even ask... but it feels incredible."),
                    _("That was bold... no one's ever gone bare inside me before. Don't stop."),
                ]
            elif _cm_is_cheater and _cm_has_bf and _cm_player_has_gf:
                _fa_lines = [
                    _("You ripped it off... both cheating on our partners AND going raw. We're terrible. Don't stop."),
                    _("My %(pl)s, your girlfriend... neither of them would believe this. Keep going."),
                ]
            elif _cm_is_cheater and _cm_has_bf:
                _fa_lines = [
                    _("Behind %(poss)s back AND raw? You're a worse person than me. Keep going."),
                    _("You just ripped it off without even asking... my %(pl)s would NEVER. I love that about you."),
                    _("You're fucking me raw behind %(poss)s back and you didn't even hesitate. God that's hot."),
                ]
                if _cm_bf_did_sex:
                    _fa_lines.extend([
                        _("You just took it off... my %(pl)s always wraps it. You don't even bother. I love it."),
                        _("%(Pp)s asks permission. You just take it. That's why I keep coming back to you."),
                    ])
                else:
                    _fa_lines.extend([
                        _("You just took it off... behind my %(pl)s's back. I love it."),
                        _("My %(pl)s doesn't even get this... and you just rip it off like you own me."),
                    ])
            elif _cm_has_bf:
                _fa_lines = [
                    _("No condom... if %(pp)s ever found out... mmm, I can't help myself."),
                    _("You're inside me raw without even asking... I should be furious but it feels too good..."),
                    _("You just... took it off... my %(pl)s would kill us both and I don't even care right now..."),
                ]
                if _cm_bf_did_sex:
                    _fa_lines.extend([
                        _("You just took it off... my %(pl)s would never do that. Keep going."),
                        _("%(Pp)s always wears one. You just... didn't even hesitate. Oh god..."),
                        _("My %(pl)s asks every time. You didn't even blink. Why does that turn me on so much..."),
                    ])
                else:
                    _fa_lines.extend([
                        _("You just took it off... my %(pl)s can never know about this. Keep going."),
                        _("Raw... behind %(poss)s back... oh god..."),
                        _("I have a %(pl)s and you're raw inside me without even asking... what is wrong with me..."),
                    ])
            elif _cm_is_cheater and _cm_player_has_gf:
                _fa_lines = [
                    _("You ripped it off... your girlfriend would die if she saw this. Keep going."),
                    _("Raw behind your girlfriend's back? You're even worse than me. I love it."),
                    _("Does she know you go raw with other girls? Because this is so much hotter without it."),
                    _("Your girlfriend thinks you're faithful... and here you are, raw inside me. Don't stop."),
                ]
            elif _cm_player_has_gf:
                _fa_lines = [
                    _("You took it off... does your girlfriend know you do this? ...Don't answer that."),
                    _("Raw with someone who isn't your girlfriend... you're bold. Keep going."),
                ]
            elif _cm_recording:
                _fa_lines = [
                    _("You took it off while recording... if anyone sees this... oh god. Don't stop."),
                    _("On camera AND raw? You're insane. ...Keep going. Make it a good video."),
                ]
            elif _cm_is_cum_slut:
                # only a cum_slut still discovering it gets here (the veteran one took the ironic lines at the top)
                _cm_line_trait = "cum_slut"
                _fa_lines = [
                    _("You took it off... I... I kind of hoped you would."),
                    _("No condom... oh. I can feel you so much better... don't stop."),
                    _("You didn't even ask... and I don't want you to put it back."),
                ]
            elif _cm_is_cute:
                _cm_line_trait = "cute_sex"
                _fa_lines = [
                    _("Y-you took it off... I can feel... everything... oh my god..."),
                    _("You didn't ask... but... oh... it feels so much warmer... so close..."),
                    _("That was sudden... but I... I don't want you to put it back. Keep going..."),
                ]
            elif _cm_is_hardcore:
                _cm_line_trait = "hardcore_sex"
                _fa_lines = [
                    _("You just ripped it off. Good. I like someone who takes what they want."),
                    _("About damn time. Condoms are for people who aren't serious. Don't stop."),
                    _("That's more like it. Raw. The way it should be."),
                ]
            else:
                _fa_lines = [
                    _("You just... mmm... that feels different. Better. Don't stop."),
                    _("Oh... you took it off. I... okay. It does feel better."),
                    _("Bold move... but I'm not complaining. Keep going."),
                ]

            _fa_line = _tl(renpy.random.choice(_fa_lines)) % _cm_bf_f

        $ _cr_blocked = _on_condom_removed(girl, skip_hide=_cum_skip_hide(scene_type))
        if _cr_blocked:
            return
        $ Say_Line(girl, _fa_line)
        $ apply_cum_bonuses(girl, "condom_removed_allowed")
        # She accepted the removal -- cum inside is implicitly allowed
        $ store._creampie_consent = "allowed"
        $ store._creampie_warned = True
        # Discovery flags: the trait whose pool spoke; cheating is the DEED (she has a partner and accepted)
        if _cm_line_trait:
            $ girl.discover("discovered_trait_%s" % _cm_line_trait)
        if girl.has_trait("cheater") and _cm_has_bf:
            $ girl.discover("discovered_trait_cheater")
        if _cm_has_bf:
            $ _discover_partner(girl)
            if _cm_bf_did_sex:
                $ girl.discover("discovered_bf_never_sex_raw")
                if _cm_is_first_raw:
                    $ girl.discover("discovered_bf_done_sex")
        return

    # ── SHOCKED ACCEPT (likes it but upset you didn't ask) ──
    if _cm_result == "shocked_accept":
        python:
            # cum_slut: always ironic, never upset (once she is past discovering it; before, the lines below fit her)
            _cm_line_trait = None   # only the ironic pool below evidences the trait
            if _cm_is_cum_slut and trait_is_veteran(girl, "cum_slut"):
                _cm_line_trait = "cum_slut"
                _sa_lines = [
                    _("Oh no... I feel so vulnerable now... what if you decide to fill up my poor little pussy?"),
                    _("Mmm... no condom? Whatever will I do if you cum inside me... oh wait, I WANT that."),
                    _("Finally! Now there's nothing between us... and nothing stopping you from filling me up."),
                    _("Oh no, the condom is gone! I'm SO scared of you cumming inside me... just kidding. DO IT."),
                ]
            elif _cm_is_first_raw and _cm_has_bf:
                if _cm_bf_did_sex:
                    _sa_lines = [
                        _("Hey! My first time raw and you didn't even ask?! ...My %(pl)s always asks. But fine... it's better without it."),
                        _("You could have asked! My %(pl)s always uses one... and now you just... ugh. It does feel amazing though."),
                    ]
                else:
                    _sa_lines = [
                        _("Hey! My first time raw and you didn't even ask?! ...I have a %(pl)s! But fine... it's better without it."),
                        _("You could have asked! I've never done this without one... ugh. It does feel amazing though."),
                    ]
            elif _cm_is_first_raw:
                _sa_lines = [
                    _("That was my FIRST time without one and you didn't even ASK?! ...But oh god it feels so much better."),
                    _("You just took my raw virginity without warning! ...Fine. Don't put it back. But WARN me next time!"),
                ]
            elif _cm_player_has_gf and _cm_is_cheater:
                _sa_lines = [
                    _("Hey! You could have asked! ...But your girlfriend would HATE this, so I'll allow it."),
                    _("Rude! ...But also... raw behind her back? Fine. Keep going."),
                ]
            elif _cm_has_bf:
                if _cm_bf_did_sex:
                    _sa_lines = [
                        _("You could have asked! ...My %(pl)s always asks. But fine... it feels better without it."),
                        _("Don't just... ugh. At least it feels amazing. My %(pl)s never goes raw."),
                    ]
                else:
                    _sa_lines = [
                        _("You could have asked! ...I have a %(pl)s, you know! But fine... it feels better without it."),
                        _("Don't just... ugh. At least it feels amazing. But you should have ASKED."),
                    ]
            elif _cm_player_has_gf:
                _sa_lines = [
                    _("Hey! You could've asked! Does your girlfriend know you just do this?! ...Fine. It feels better."),
                    _("Rude! ...Your poor girlfriend. But I'm not complaining. Keep going."),
                ]
            elif _cm_recording:
                _sa_lines = [
                    _("You took it off while RECORDING?! Without ASKING?! ...Ugh, it does feel better. But you owe me."),
                    _("On camera AND you just rip it off?! ...Fine. But if that video leaks, you're dead."),
                ]
            else:
                _sa_lines = [
                    _("Hey! You could have asked first! ...But god, it feels so much better without it."),
                    _("Rude! ...But also... don't put it back on. Please."),
                    _("You didn't even ask! ...Fine. It feels better this way. But WARN me next time!"),
                ]
            _sa_line = _tl(renpy.random.choice(_sa_lines)) % _cm_bf_f

        $ _cr_blocked = _on_condom_removed(girl, skip_hide=_cum_skip_hide(scene_type))
        if _cr_blocked:
            return
        $ Say_Line(girl, _sa_line)
        if not _cm_is_cum_slut:
            $ Change_Status(girl, "Love", -5)
        else:
            $ Change_Status(girl, "Love", 5)
        if _cm_line_trait:
            $ girl.discover("discovered_trait_%s" % _cm_line_trait)
        $ apply_cum_bonuses(girl, "condom_removed_allowed")
        # She accepted (shocked but ok) -- cum inside is implicitly allowed
        $ store._creampie_consent = "allowed"
        $ store._creampie_warned = True
        return

    # ── ANGRY BUT CONTINUES (moderate Obed + high Lust... condom stays, creampie blocked) ──
    if _cm_result == "angry_continue":
        $ set_scene_expression(girl, "angry")
        python:
            if _cm_has_bf and _cm_player_has_gf:
                _ac_lines = [
                    _("What the... We both have partners and you just rip the condom off?! Put it BACK!"),
                    _("My %(pl)s, your girlfriend, and now THIS?! Put the condom back on RIGHT NOW!"),
                ]
            elif _cm_has_bf:
                if _cm_bf_did_sex:
                    _ac_lines = [
                        _("What the... Don't you EVER do that without asking! My %(pl)s at least has the decency to ask! Put it back on!"),
                        _("Are you serious right now?! %(Pp)s would NEVER pull something like this! Put the condom back!"),
                    ]
                else:
                    _ac_lines = [
                        _("What the... Don't you EVER do that without asking! I have a %(PL)s! Put it back on!"),
                        _("Are you serious right now?! Put the condom back! NOW!"),
                    ]
            elif _cm_player_has_gf:
                _ac_lines = [
                    _("Excuse me?! Does your girlfriend let you pull stunts like this?! Put it back on!"),
                    _("You have a girlfriend and you just... god. Put it back on. Now."),
                ]
            elif _cm_recording:
                _ac_lines = [
                    _("You're RECORDING and you just took it off?! Put it BACK! Are you insane?!"),
                    _("On camera AND without asking?! Put the condom back on before I end this!"),
                ]
            elif _cm_is_cute:
                _ac_lines = [
                    _("W-what?! You can't just DO that! Put it back on! Please! That scared me!"),
                    _("Why did you do that without asking?! I'm not... put it back on! Now!"),
                ]
            elif girl.has_trait("femdom"):
                _ac_lines = [
                    _("Bold move, but you crossed a line. Put it back on. You haven't earned raw yet."),
                    _("You don't take things from me. You wait until I give them. Put it back on."),
                    _("Did I give you permission? No. Put it back on and remember who decides here."),
                ]
            elif _cm_is_hardcore:
                _ac_lines = [
                    _("I respect the balls, but no. Put it back on. Ask next time."),
                    _("Nice try. Condom back on, now. Then keep going, and don't go soft on me."),
                ]
            else:
                _ac_lines = [
                    _("Don't you EVER do that without asking me! Put it back on!"),
                    _("What the hell?! You can't just... put the condom back on. NOW!"),
                    _("Are you insane?! Don't ever pull that again! Put it back!"),
                ]
            _ac_line = _tl(renpy.random.choice(_ac_lines)) % _cm_bf_f

        $ Say_Line(girl, _ac_line)
        $ Change_Status(girl, "Love", -10)
        $ Change_Status(girl, "Obed", -5)
        $ store._creampie_consent = "blocked"
        "You put the condom back on. She's not happy about what you tried."
        $ store._condom_removal_denied = True
        $ set_scene_expression(girl, "normal")
        return

    # ── ANGRY (refuses... condom stays on, creampie blocked) ──
    $ set_scene_expression(girl, "angry")
    python:
        if _cm_has_bf and _cm_player_has_gf:
            _ang_lines = [
                _("We both have partners and you try THIS?! Put it back on! NOW!"),
                _("My %(pl)s, your girlfriend... and you rip the condom off?! What is WRONG with you?!"),
            ]
        elif _cm_has_bf:
            _ang_lines = [
                _("What the HELL?! Put it back on! Not even my %(pl)s pulls shit like this!"),
                _("Are you insane?! I have a %(PL)s and you just... put the condom back on. NOW."),
                _("Do you have ANY respect?! My %(pl)s would never do something this disgusting!"),
            ]
        elif _cm_player_has_gf:
            _ang_lines = [
                _("You have a GIRLFRIEND and you're trying to go raw with ME?! Put it back on!"),
                _("Does your girlfriend know you do things like this?! Put. It. Back. On!"),
            ]
        elif _cm_recording:
            _ang_lines = [
                _("You're RECORDING and you just took the condom off?! Put it back on or I'm DONE!"),
                _("On camera?! Without a condom?! Are you trying to RUIN me?! PUT IT BACK!"),
            ]
        elif _cm_is_cute:
            _ang_lines = [
                _("W-why would you do that?! That's so scary! Put it back on! Please!"),
                _("Don't do that to me! I trusted you! Put the condom back on right now!"),
                _("I can't believe you just... please put it back on. I'm really upset."),
            ]
        elif _cm_is_hardcore:
            _ang_lines = [
                _("You've got nerve. But I didn't say yes. Put it back on. Now."),
                _("Don't EVER pull that shit without asking. Put it back on or we're done here."),
            ]
        else:
            _ang_lines = [
                _("What the hell?! Put it back on RIGHT NOW!"),
                _("Did you seriously just do that?! I didn't say you could take it off!"),
                _("Are you out of your mind?! Put the condom back on or we're done!"),
                _("Don't you DARE! Put it back on this instant!"),
            ]
        _ang_line = _tl(renpy.random.choice(_ang_lines)) % _cm_bf_f

    $ Say_Line(girl, _ang_line)
    $ Change_Status(girl, "Love", -15)
    $ Change_Status(girl, "Obed", -10)
    $ Change_Status(girl, "Inbt", -10)
    $ store._creampie_consent = "blocked"
    "You put the condom back on. She's visibly upset."
    $ store._condom_removal_denied = True
    $ set_scene_expression(girl, "normal")

    return

# ------------------------------------------------------------
# ForcedCumOverdue... forced cum when player delays past Focus 100
# ------------------------------------------------------------
label ForcedCumOverdue(girl, scene_type):
    $ debug_log("[FORCED_OVERDUE] triggered: scene=%s condom=%s stealth=%s overdue_n=%d phase=%s" % (scene_type, store.condom_active, store._stealth_condom_removed, store._focus_overdue_count, getattr(store, "_scene_phase", "sex")))

    $ store._scene_force_end = False
    # a condom on as his finish starts (the post-cum condom menu reads it after a finish that pulled it off)
    $ store._finish_had_condom = _girl_thinks_condom_on()
    $ _fo_cum_type = _forced_cum_type(scene_type)
    $ debug_log("[FORCED_OVERDUE] cum_type=%s" % _fo_cum_type)

    python:
        _fo_narr_key = _fo_cum_type
        if _fo_narr_key == "outside" and getattr(store, "_scene_phase", "sex") == "rub":
            _fo_narr_key = "rub"
        _fo_narr = _tl(renpy.random.choice(_FORCED_OVERDUE_LINES.get(_fo_narr_key, _FORCED_OVERDUE_LINES["outside"])))

    if _fo_cum_type == "condom":
        call _cum_dispatch_anim(girl, scene_type) from _call__cum_anim_fo_condom
        "[_fo_narr]"
        $ process_cum(girl, scene_type, "condom")
        $ apply_cum_bonuses(girl, "cum_outside")

    elif _fo_cum_type in ("inside", "inside_anal"):
        $ _fo_is_cum_slut = girl.has_trait("cum_slut")
        $ _fo_is_hate_cum = girl.has_trait("hate_cum")
        $ _fo_has_consent = store._creampie_consent in ("allowed", "changed_mind") or getattr(store, "_girl_requested_creampie", False)
        $ debug_log("[FORCED_OVERDUE] inside: cum_slut=%s hate_cum=%s has_consent=%s" % (_fo_is_cum_slut, _fo_is_hate_cum, _fo_has_consent))

        $ _fo_anal_lover_anal = scene_type in _ANAL_SCENE_TYPES and girl.has_trait("anal_lover")
        if _fo_is_cum_slut or _fo_anal_lover_anal:
            $ set_scene_expression(girl, renpy.random.choice(["ahegao", "ahegao_2"]), blush="3")
        elif not _fo_has_consent:
            $ store._cum_forced_surprise = True

        call _cum_dispatch_anim(girl, scene_type) from _call__cum_anim_fo_inside
        "[_fo_narr]"
        $ process_cum(girl, scene_type, "inside")

        if store._stealth_condom_removed:
            $ debug_log("[FORCED_OVERDUE] stealth condom detected, routing to stealth realization")
            call _stealth_cream_realization(girl, scene_type) from _call_stealth_cream_real_fo
            return

        if _fo_has_consent:
            # She had said yes (or asked for it): a creampie she wanted, whatever her traits. This used to come
            # AFTER the cum_slut check, so a cum_slut who had said "finish inside me" answered "I said no but..."
            $ apply_cum_bonuses(girl, "cum_inside_allowed")
            $ _fo_line = _consented_cream_line(girl, scene_type)
            $ Say_Line(girl, _fo_line)
        elif _fo_is_cum_slut or _fo_anal_lover_anal:
            # Nobody cleared it with her and she loves it anyway: the outcome of the manual "Cum inside"
            $ store._forced_creampie_count += 1
            $ _fo_refused = _creampie_was_refused()
            $ store._creampie_consent = "allowed"
            $ apply_cum_bonuses(girl, "cum_inside_allowed")
            $ _fo_line = _cream_liked_line(girl, scene_type, _fo_refused)
            $ Say_Line(girl, _fo_line)
        else:
            $ apply_cum_penalties(girl, "cum_inside_forced", scene_type)
            $ store._witness_expression_lock = True
            $ set_scene_expression(girl, "angry", brows="brows_maniac")
            $ store._forced_creampie_count += 1

            $ _fo_line = scene_pick_line("cum_inside_forced", scene=scene_type, girl=girl) or _("What?! You came inside me?!")
            $ Say_Line(girl, _fo_line)

            if _fo_is_hate_cum:
                call _hate_cum_angry_end(girl, scene_type) from _call__hate_cum_angry_end_fo
                $ store._scene_force_end = True
                return

            if store._forced_creampie_count >= 2:
                call _forced_creampie_angry_end(girl, scene_type) from _call__forced_creampie_angry_end_fo
                $ store._scene_force_end = True
                return

        if not _fo_is_cum_slut and not _fo_anal_lover_anal:
            $ store._witness_expression_lock = False
            $ set_scene_expression(girl, "normal")

    elif _fo_cum_type == "mouth":
        $ store._cum_forced_surprise = not (girl.has_trait("cum_slut") or girl.has_trait("hardcore_sex"))
        if scene_type == "bj" and getattr(store, "bj_forcing", False):
            call BJ_CumAnim(girl, forced=True) from _call__cum_anim_fo_mouth_forced
        else:
            call _cum_dispatch_anim(girl, scene_type) from _call__cum_anim_fo_mouth
        "[_fo_narr]"
        $ _fo_mouth_check = CumPermissionCheck(girl, "cum_in_mouth_ask")
        $ process_cum(girl, scene_type, "mouth")
        if _fo_mouth_check["accepted"]:
            $ apply_cum_bonuses(girl, "cum_in_mouth_allowed")
        else:
            $ apply_cum_penalties(girl, "cum_in_mouth_forced")
        call _bj_mouth_cum_reaction(girl, not _fo_mouth_check["accepted"]) from _call__bj_mcr_fo

    elif _fo_cum_type == "tits":
        call _cum_dispatch_anim(girl, scene_type) from _call__cum_anim_fo_tits
        "[_fo_narr]"
        $ process_cum(girl, scene_type, "tits")
        $ apply_cum_bonuses(girl, "cum_outside")

    else:
        # Use outside_freeze for rub/tip (penis not inside); fall back to cum_anim (HJ etc.)
        $ _fo_outside_lbl = _cum_cfg(scene_type, "outside_freeze")
        if _fo_outside_lbl:
            call _cum_dispatch_outside_freeze(girl, scene_type) from _call__cum_freeze_fo_outside
        else:
            call _cum_dispatch_anim(girl, scene_type) from _call__cum_anim_fo_outside
        "[_fo_narr]"
        $ process_cum(girl, scene_type, _fo_cum_type if _fo_cum_type in _FORCED_CUM_OUTSIDE_SPOTS else "outside")
        $ apply_cum_bonuses(girl, "cum_outside")

    $ Player.Focus = 0

    return

# ------------------------------------------------------------
# PlayerCumMenu... main dispatcher
# ------------------------------------------------------------
label PlayerCumMenu(girl, scene_type):
    $ store._scene_force_end = False
    # a condom on as his finish starts (the post-cum condom menu reads it after a finish that pulled it off)
    $ store._finish_had_condom = _girl_thinks_condom_on()

    "You feel yourself getting close..."

    $ _pcm_own = _cum_cfg(scene_type, "cum_menu")
    if _pcm_own:
        call expression _pcm_own pass (girl, scene_type) from _call_PlayerCumMenu_own
    elif scene_type in ("hj", "bj", "tj", "fj"):
        call PlayerCumMenu_Oral(girl, scene_type) from _call_PlayerCumMenu_Oral
    else:
        call PlayerCumMenu_Penetration(girl, scene_type) from _call_PlayerCumMenu_Penetration

    $ Player.Focus = 0

    return

# ------------------------------------------------------------
# _cum_in_mouth_via_bj... reusable switch to BJ for mouth cum
# Works for any non-BJ oral scene (HJ, TJ, etc.)
# ------------------------------------------------------------
label _cum_in_mouth_via_bj(girl, orig_scene):
    $ debug_log("[DEBUG] _cum_in_mouth_via_bj START orig_scene=%s" % orig_scene)
    # If hiding face during recording, stop recording (face visible in BJ transition)
    python:
        _hiding_active = getattr(store, "hiding_face", False)
        if _hiding_active and getattr(store, "_recording_active", False):
            store._recording_active = False
            store._recording_girl = None
            store.hiding_face = False
            if renpy.get_screen("recording_overlay"):
                renpy.hide_screen("recording_overlay")
    # Preserve exhaustion state (scene_full_cleanup resets it)
    $ _saved_exhausted = store._player_exhausted
    # A condom on for this finish (it comes off for her mouth; the End below resets it): the menu after it is the
    # condom menu, as after every finish with one
    $ _vbj_had_condom = _girl_thinks_condom_on() or bool(getattr(store, "_finish_had_condom", False))
    $ _vbj_condom_snap = None
    # Preserve tip/rub mode state for return-to-scene
    $ _saved_tip_mode = getattr(store, "doggy_tip_mode", False)
    $ _saved_fn_tip_mode = getattr(store, "fn_tip_mode", False)
    $ _saved_fn_anal = getattr(store, "fn_anal", False)
    $ _saved_ld_tip_mode = getattr(store, "laying_tip_mode", False)
    $ _saved_ld_rub_mode = getattr(store, "laying_rub_mode", False)
    $ _saved_ld_anal = getattr(store, "laying_anal", False)
    $ _saved_rcg_anal = getattr(store, "rcg_anal", False)
    # Preserve recording state across scene transition
    $ _saved_recording = getattr(store, "_recording_active", False)
    $ _saved_recording_girl = getattr(store, "_recording_girl", None)
    $ _saved_hand_disabled = getattr(store, "_player_hand_disabled", None)
    $ _saved_rec_seconds = getattr(store, "_recording_seconds", 0.0)
    $ _saved_rec_rate = getattr(store, "_recording_sec_rate", 0.0)
    # Preserve NTR watching state (killed by _kill_scene_threads in End/Launch)
    $ _saved_ntr_watching = getattr(store, "_ntr_partner_watching", False)
    $ _saved_ntr_npc = getattr(store, "_ntr_watching_npc", None)
    $ _saved_ntr_sess_watcher = getattr(store, "_ntr_session_watcher_gid", None)   # the scene end below is only a transition
    # Preserve stripped clothes state (scene End restores outfit via cleanup)
    $ _saved_clothes = dict(girl.clothes)
    $ _saved_clothes_state = dict(girl.clothes_state)
    # Preserve original outfit reference so final End can still restore to pre-scene state
    $ _saved_outfit_ref = getattr(girl, "_saved_outfit", None)
    # Suppress lesbian coldness during mid-scene transition (fires at real scene end)
    $ _saved_lesbian_cd = getattr(store, "_lesbian_coldness_done", False)
    $ store._lesbian_coldness_done = True

    # End current scene
    $ debug_log("[DEBUG] calling %s End from mouth_via_bj" % orig_scene)
    call _cum_dispatch_end(girl, orig_scene) from _call__cum_dispatch_end_mouth_via_bj
    $ debug_log("[DEBUG] End returned from mouth_via_bj")
    $ store._lesbian_coldness_done = _saved_lesbian_cd

    # Restore stripped clothes (scene_full_cleanup restored the saved outfit)
    $ girl.clothes = _saved_clothes
    $ girl.clothes_state = _saved_clothes_state
    # Keep original outfit ref so the real scene end restores properly
    $ girl._saved_outfit = _saved_outfit_ref
    $ debug_log("[DEBUG] _cum_in_mouth_via_bj: clothes preserved=%s" % str(_saved_clothes))

    # Restore recording state (scene End may have cleared it)
    $ store._recording_active = _saved_recording
    $ store._recording_girl = _saved_recording_girl
    $ store._player_hand_disabled = _saved_hand_disabled
    $ store._recording_seconds = _saved_rec_seconds
    $ store._recording_sec_rate = _saved_rec_rate
    if _saved_recording and not renpy.get_screen("recording_overlay"):
        $ renpy.show_screen("recording_overlay")
    $ debug_log("[DEBUG] _cum_in_mouth_via_bj: recording preserved=%s secs=%.1f hand=%s" % (_saved_recording, _saved_rec_seconds, _saved_hand_disabled))

    # Restore NTR watching state (cleared by _kill_scene_threads during transitions)
    $ store._ntr_partner_watching = _saved_ntr_watching
    $ store._ntr_watching_npc = _saved_ntr_npc
    $ store._ntr_session_watcher_gid = _saved_ntr_sess_watcher

    # Player is already exposed from the prior scene — skip "drop your pants"
    $ store._player_exposed_this_session = True

    # Strip towel if in shower (towel has no BJ layer)
    if getattr(girl, "shower_state", None) and girl.clothes.get("over") == "towel":
        $ girl.Outfit_Change(over="none")

    # Launch BJ (fade transition, head at speed 0 = still)
    call BJ_Launch(girl) from _call_BJ_Launch_mouth_via_bj
    $ mark_intimacy(girl, "bj")

    python:
        store.bj_idle_mouth = "mouth_tongue"
        store.bj_torso_type = _gsc(girl.gid, 'default_torso_type', 1, pose='blowjob')
        store.bj_action = "suck"

    # ATM: she acknowledges what she's about to do (still at speed 0 so arms are static)
    if getattr(store, "_atm_cum_in_mouth", False):
        call BJ_ApplySpeed(girl, 0) from _call_BJ_ApplySpeed_atm_still
        python:
            _atm_entry = None
            _has_hc = girl.has_trait("hardcore_sex")
            _has_ah_entry = girl.has_trait("anal_hater")
            _has_hc_cum_entry = girl.has_trait("hate_cum")

            if girl.has_trait("cum_slut") and (trait_is_new(girl, "cum_slut") or (girl.has_trait("anal_lover") and trait_is_new(girl, "anal_lover"))):
                # still discovering the cum or the anal: she wants it, and can't believe she does
                _atm_entry = renpy.random.choice([
                    _("It was just in my... and I'm going to... oh god. Why do I want to?"),
                    _("Straight from my ass... that's so dirty. Why am I not saying no?"),
                ])
            elif girl.has_trait("cum_slut"):
                _atm_entry = renpy.random.choice([
                    _("Mmm... I know where it's been. I want to taste it for you. Treat me right..."),
                    _("Straight from my ass... god, that's so dirty. I love it."),
                ])
            elif girl.has_trait("submissive") and _has_ah_entry and _has_hc_cum_entry:
                _atm_entry = renpy.random.choice([
                    _("Here I am about to taste your cum, my ass or both and I'm still going to open my mouth for you... Go ahead. It's yours. I've earned whatever you give me here."),
                    _("I hate the taste of cum. I hate the taste of my ass. But you want my mouth, so it's yours. Just tell me when."),
                    _("Where do you want it? ...No, don't answer. Wherever you put it, I'll take it. That's what I'm here for."),
                ])
            elif _has_hc and _has_ah_entry and _has_hc_cum_entry:
                _atm_entry = renpy.random.choice([
                    _("Shoot from a distance and my mouth's full of cum. Force it past my tongue first and I'll have a mouth full of my ass. Or you could entirely fuck me and park both right on my tongue. That'd be what I deserve for saying yes to this."),
                    _("I hate the taste of cum and I hate the taste of my ass. So shove it deep and finish fast, before I can taste either one."),
                ])
            elif _has_hc and _has_ah_entry:
                _atm_entry = renpy.random.choice([
                    _("You best keep that thing a safe distance away. You can cum in my mouth, but I don't wanna taste my ass. Though I wouldn't have much choice if you took control..."),
                    _("Here, shoot for my mouth. Though I'll have it open... And your cock will be right there... Fresh from my ass... If you make me... Well I guess that'd be on me..."),
                ])
            elif _has_hc and _has_hc_cum_entry:
                _atm_entry = renpy.random.choice([
                    _("Please, shove that thing in as deep as you can first. I won't have to feel it or taste it that way."),
                    _("Do me a favor and force me all the way down first? I'll gag a bit, but I'll gag worse if I have to taste cum."),
                ])
            elif _has_hc:
                _atm_entry = renpy.random.choice([
                    _("You're really making me do this, huh? ...Fine. Open wide."),
                    _("Right from my ass to my mouth. You're filthy. Don't stop."),
                ])
            elif girl.has_trait("cute_sex"):
                _atm_entry = renpy.random.choice([
                    _("I can't believe you're making me do this... don't you care how I feel?"),
                    _("This is so wrong... why do you want me to do this?"),
                ])
            else:
                _atm_entry = renpy.random.choice([
                    _("You know where that just was, right? ...Fine."),
                    _("Straight from my ass... you're really something else."),
                ])
            _atm_entry = atm_cross_override(girl, "entry", _atm_entry)   # threesome: it was in the OTHER girl's ass
            if _atm_entry:
                Say_Line(girl, _atm_entry)

    call BJ_ApplySpeed(girl, 3) from _call_BJ_ApplySpeed_mouth_via_bj

    menu:
        "Cum in her mouth":
            $ store.bj_torso_type = 2
            call BJ_CumAnim(girl, False) from _call_BJ_CumAnim_mouth_via_bj
            $ process_cum(girl, "bj", "mouth")
            $ apply_cum_bonuses(girl, "cum_in_mouth_allowed")
            call _bj_mouth_cum_reaction(girl, False, skip_post_menu=True) from _call__bj_mcr_mouth_via_bj

        "Force her down":
            # Force speed 3 + forcing hands + cum (hide arm/hand — arms_1 default shows)
            $ store.bj_torso_type = 1
            $ store.bj_forcing = True
            $ store._bj_use_half_penis = (girl.gid == "tenny")
            $ store.bj_speed = 3
            $ store.bj_action = "suck"
            call BJ_ApplySpeed(girl, 3) from _call_BJ_ApplySpeed_force_cum_via_bj

            # Show forcing hands (same logic as BJ_PlayerCum forced)
            python:
                _gid = girl.gid
                _hand_disabled = getattr(store, "_player_hand_disabled", None)
                _force_tf = bj_get_head_transform(3)
                _is_pov = _gsc(_gid, 'pov_overlay', False, pose='blowjob')
                _forcing_z = 10100 if _is_pov else 10080
                _f_left = "%s bj_forcing_hands_left" % _gid
                if renpy.has_image(_f_left):
                    for _side in ("left", "right"):
                        _f_img = "%s bj_forcing_hands_%s" % (_gid, _side)
                        _f_tag = "%s_bj_forcing_%s" % (_gid, _side)
                        if _hand_disabled != _side and renpy.has_image(_f_img):
                            renpy.show(_f_img, tag=_f_tag, at_list=[_force_tf], zorder=_forcing_z)
                        else:
                            renpy.hide(_f_tag)
                else:
                    _f_img = "%s bj_forcing_hands" % _gid
                    if renpy.has_image(_f_img):
                        renpy.show(_f_img, tag="%s_bj_forcing_left" % _gid, at_list=[_force_tf], zorder=_forcing_z)
                    renpy.hide("%s_bj_forcing_right" % _gid)

            "You grab her head and force it down."

            # Head grab rejection: only during ATM, only with 2+ negative traits, only if Obed is low enough
            # Hardcore girls never resist — being forced is what they want
            python:
                _hg_is_atm = getattr(store, "_atm_cum_in_mouth", False)
                _hg_reject = False
                if _hg_is_atm and not girl.has_trait("hardcore_sex"):
                    _hg_neg_count = 0
                    if girl.has_trait("cute_sex"):
                        _hg_neg_count += 1
                    if girl.has_trait("anal_hater"):
                        _hg_neg_count += 1
                    if girl.has_trait("hate_cum"):
                        _hg_neg_count += 1
                    if _hg_neg_count >= 2 and getattr(girl, "Obed", 0) < 600:
                        _hg_reject = True
                        debug_log("[DEBUG] Head grab rejection: neg_traits=%d, Obed=%d" % (_hg_neg_count, getattr(girl, "Obed", 0)))

            if _hg_reject:
                # She physically resists — pulls away
                python:
                    if _hg_neg_count >= 3:
                        _hg_line = renpy.random.choice([
                            _("NO! GET OFF ME! I'm NOT swallowing that! Not after where it's been!"),
                            _("STOP! I hate this! I hate cum, I hate anal, and I am NOT doing this!"),
                        ])
                    else:
                        _hg_line = renpy.random.choice([
                            _("No! I said I'd try but I can't! Not like this!"),
                            _("Stop! You're forcing me! I can't do it, please!"),
                        ])
                    set_scene_expression(girl, "angry")
                    Say_Line(girl, _hg_line)
                    Change_Status(girl, "Love", -10)
                    Change_Status(girl, "Obed", -5)

                "She jerks her head away at the last second."
                # Forced facial instead of mouth
                $ _pov_rej = _gsc(girl.gid, 'pov_overlay', False, pose='blowjob')
                $ renpy.show("%s bj_penis" % girl.gid, tag="bj_penis", at_list=[_bj_get_penis_cum_tf(girl)], zorder=10055 if _pov_rej else 10020)

                $ renpy.pause(0.50)
                show layer master at bj_slap_shake
                $ renpy.pause(0.20)
                show layer master

                $ process_cum(girl, "bj", "face")
                python:
                    _hg_after = renpy.random.choice([
                        _("Don't EVER try that again!"),
                        _("I told you I couldn't do it... why would you force me?"),
                    ])
                    set_scene_expression(girl, "angry")
                    Say_Line(girl, _hg_after)

                # Skip normal force flow — clean up BJ before returning
                $ store.bj_forcing = False
                $ store._bj_use_half_penis = False
                call BJ_End(girl, dress_up=False) from _call_BJ_End_hg_reject
                return

            # Let forcing animation play before cum
            $ renpy.pause(1.5)

            # Penis pulse — standard below head(10015); POV below guy(10050)
            $ _pov_force = _gsc(girl.gid, 'pov_overlay', False, pose='blowjob')
            $ renpy.show("%s bj_penis" % girl.gid, tag="bj_penis", at_list=[_bj_get_penis_cum_tf(girl)], zorder=10055 if _pov_force else 9990)

            # Punch 1
            $ renpy.pause(0.50)
            show layer master at bj_slap_shake
            $ renpy.pause(0.20)
            show layer master

            # Punch 2
            $ renpy.pause(0.50)
            show layer master at bj_slap_shake
            $ renpy.pause(0.20)
            show layer master

            $ process_cum(girl, "bj", "mouth")

            # Pre-compute acceptance (used for expression + menu)
            python:
                _fc_obed = getattr(girl, "Obed", 0)
                _fc_inbt = getattr(girl, "Inbt", 0)
                _fc_has_hc = girl.has_trait("hate_cum")
                _fc_has_hardcore = girl.has_trait("hardcore_sex")
                _fc_has_al = girl.has_trait("anal_lover")

                if girl.has_trait("cum_slut"):
                    _fc_accepted = True
                elif _fc_has_hc:
                    if _fc_has_hardcore and _fc_has_al:
                        _fc_accepted = (_fc_obed >= 300 or _fc_inbt >= 300)
                    elif _fc_has_hardcore:
                        _fc_accepted = (_fc_obed >= 500 or _fc_inbt >= 500)
                    elif _fc_has_al:
                        _fc_accepted = (_fc_obed >= 400 or _fc_inbt >= 400)
                    else:
                        _fc_accepted = False
                    debug_log("[DEBUG] forced_swallow: hate_cum + hc=%s al=%s obed=%d inbt=%d -> accepted=%s" % (_fc_has_hardcore, _fc_has_al, _fc_obed, _fc_inbt, _fc_accepted))
                elif _fc_has_hardcore:
                    _fc_accepted = (_fc_obed >= 300 or _fc_inbt >= 300)
                elif girl.has_trait("cute_sex"):
                    _fc_accepted = (_fc_obed >= 700 and _fc_inbt >= 500)
                else:
                    _fc_accepted = (_fc_obed >= 500 or (_fc_obed >= 300 and _fc_inbt >= 400))

            # Show mouth cum expression — trait + acceptance aware
            python:
                _frc_brows = None
                if girl.has_trait("cum_slut"):
                    _frc_eyes = "eyes_" + renpy.random.choice(["ahegao", "ahegao_2"])
                elif girl.has_trait("hardcore_sex"):
                    if _fc_accepted:
                        _frc_eyes = "eyes_" + renpy.random.choice(["ahegao", "ahegao_2"])
                    else:
                        _frc_eyes = "eyes_left_closed"
                        _frc_brows = "brows_maniac"
                elif girl.has_trait("hate_cum"):
                    _frc_eyes = "eyes_squint"
                    _frc_brows = "brows_surprised"
                elif girl.has_trait("cute_sex"):
                    _frc_eyes = "eyes_" + renpy.random.choice(["surprised", "right_closed", "closed", "left_closed"])
                    _frc_brows = "brows_confused"
                else:
                    _frc_eyes = "eyes_" + renpy.random.choice(["squint", "squint_2", "left_closed", "right_closed"])
                set_scene_expression(girl, None, eyes=_frc_eyes, brows=_frc_brows, mouth="mouth_tongue")

            # Trait reactions to being forced
            if girl.has_trait("cum_slut"):
                $ Change_Status(girl, "Inbt", 15)
                $ Change_Status(girl, "Obed", 10)
                $ girl.Lust = min(100, getattr(girl, "Lust", 0) + 10)
            elif girl.has_trait("hate_cum"):
                $ Change_Status(girl, "Love", -15)
                $ Change_Status(girl, "Obed", -5)
            elif girl.has_trait("cute_sex"):
                $ Change_Status(girl, "Love", -10)
            elif girl.has_trait("hardcore_sex"):
                $ Change_Status(girl, "Obed", 10)
                $ girl.Lust = min(100, getattr(girl, "Lust", 0) + 5)
            elif girl.has_trait("cute_sex"):
                $ Change_Status(girl, "Love", -5)
                $ Change_Status(girl, "Inbt", 5)

            # Stay at force speed 3 — player chooses next action
            menu:
                "Hold her down and tell her to swallow":

                    if _fc_accepted:
                        # Player commands her to swallow
                        python:
                            _is_atm_force = getattr(store, "_atm_cum_in_mouth", False)
                            if _is_atm_force:
                                _fc_cmd_pool = [
                                    _("Swallow it. All of it. I don't care where it's been."),
                                    _("You're going to swallow every drop. I'll let go when you do."),
                                    _("Don't you dare spit it out. Swallow. Now."),
                                ]
                            else:
                                _fc_cmd_pool = [
                                    _("Swallow. I'm telling you."),
                                    _("I'll let you go when you swallow. Come on."),
                                    _("Don't leave a drop, swallow it all."),
                                ]
                        $ Say_Player(_tl(renpy.random.choice(_fc_cmd_pool)))
                        # She responds with muffled sounds only (mouth is full)
                        python:
                            if girl.has_trait("cum_slut"):
                                _fc_sw_pool = [
                                    _("Mmph... mmmm..."),
                                    _("Mmm... mmph... mmm..."),
                                ]
                            elif girl.has_trait("hate_cum") and girl.has_trait("hardcore_sex"):
                                _fc_sw_pool = [
                                    _("Mmgh...! ...Mm... tch..."),
                                    _("Ugh... mmph... hnn..."),
                                ]
                            elif girl.has_trait("cute_sex"):
                                _fc_sw_pool = [
                                    _("Mm... mmh... mm..."),
                                    _("Mmh... nn... mm..."),
                                    _("Mm... hm... mmh..."),
                                ]
                            elif girl.has_trait("cute_sex"):
                                _fc_sw_pool = [
                                    _("Mmph...! Mmgh... mm..."),
                                    _("Mmhh... mmph... mm..."),
                                    _("Mmgh...! ...Mm... mmph..."),
                                ]
                            elif girl.has_trait("hardcore_sex"):
                                _fc_sw_pool = [
                                    _("Mmgh...! ...Mmph."),
                                    _("Mmph... tch... mmgh."),
                                    _("Ugh... mmph... mm."),
                                ]
                            else:
                                _fc_sw_pool = [
                                    _("Mmgh... mmph... mm..."),
                                    _("Mmph... mm... mmgh..."),
                                    _("Mm... mmph... mmgh..."),
                                ]
                        $ Say_Line(girl, _tl(renpy.random.choice(_fc_sw_pool)))
                        # Swallow while still at force depth
                        $ set_scene_expression(girl, "closed_happy")
                        if girl.gid == "tenny":
                            python:
                                _ht = bj_get_head_transform(store.bj_speed)
                                _pov = _gsc("tenny", 'pov_overlay', False, pose='blowjob')
                                renpy.show("tenny blowjob_head head_base", tag="tenny_bj_head", at_list=[_ht], zorder=10058 if _pov else 10015)
                                renpy.show("tenny blowjob_jaw jaw_1", tag="tenny_bj_jaw", at_list=[_ht], zorder=9984)
                        $ _remove_cum_tag(girl, "mouth")
                        $ renpy.pause(0.8)
                        $ apply_cum_bonuses(girl, "cum_in_mouth_allowed")
                        $ Change_Status(girl, "Obed", 25)
                        $ Change_Status(girl, "Inbt", 20)
                        $ girl.ForcedSwallowCounts = getattr(girl, "ForcedSwallowCounts", 0) + 1
                        $ girl.check_corruption("cum")
                        $ unlock_achievement("until_the_end")

                        # Release forcing hands
                        $ renpy.hide("%s_bj_forcing_left" % girl.gid)
                        $ renpy.hide("%s_bj_forcing_right" % girl.gid)
                        $ store.bj_forcing = False

                        # Slow rise from force depth to idle
                        if girl.gid == "tenny":
                            $ _tenny_bj_force_rise_anim(girl, show_cum=True)
                        else:
                            python:
                                _gid = girl.gid
                                _is_pov = _gsc(_gid, 'pov_overlay', False, pose='blowjob')
                                store.bj_idle_mouth = "mouth_tongue"
                                store.bj_action = "lick"
                                store.bj_speed = 0
                                _head_rise = getattr(renpy.store, "%s_bj_head_force_rise" % _gid, bj_head_force_rise)
                                _slot_rise = getattr(renpy.store, "%s_bj_slot_force_rise" % _gid, bj_slot_force_rise)
                                _rise_penis_z = 10055 if _is_pov else 9990
                                renpy.show("%s bj_penis" % _gid, tag="bj_penis", at_list=[_bj_get_penis_tf(girl)], zorder=_rise_penis_z)
                                if bj_has_sucking_mouth(girl):
                                    renpy.show("%s bj_sucking_mouth" % _gid, tag="%s_bj_sucking_mouth" % _gid, at_list=[_head_rise], zorder=10030)
                                _below_img = "%s bj_sucking_below" % _gid
                                if renpy.has_image(_below_img):
                                    renpy.show(_below_img, tag="%s_bj_sucking_below" % _gid, at_list=[_head_rise], zorder=9985)
                                _fc_head = "%s blowjob_head mouth_sucking" % _gid
                                renpy.show(_fc_head, tag="%s_bj_head" % _gid, at_list=[_head_rise], zorder=10058 if _is_pov else 10015)
                                renpy.show("%s blowjob_jaw jaw_1" % _gid, tag="%s_bj_jaw" % _gid, at_list=[_head_rise], zorder=9984)
                                _attrs = _build_attributes_for_girl(girl, pose="blowjob")
                                _body_img = "%s blowjob" % _gid
                                if _attrs:
                                    _body_img += " " + " ".join(_attrs)
                                renpy.show(_body_img, tag=_gid, at_list=[_slot_rise], zorder=9980)
                                renpy.hide("%s_bj_right_arm" % _gid)
                                renpy.hide("%s_bj_arm" % _gid)
                                renpy.hide("%s_bj_hand" % _gid)
                                for _suffix, _z in [("bj_cum_face", 10025), ("bj_cum_face_under", 9986), ("bj_cum_mouth", 9988)]:
                                    _img = "%s %s" % (_gid, _suffix)
                                    if renpy.has_image(_img):
                                        renpy.show(_img, tag="%s_%s" % (_gid, _suffix), at_list=[_head_rise], zorder=_z)
                        $ renpy.pause(0.8)

                        # Cleanup rise layers before BJ_ApplySpeed resets everything
                        $ renpy.hide("%s_bj_sucking_mouth" % girl.gid)
                        $ renpy.hide("%s_bj_sucking_below" % girl.gid)
                        $ renpy.hide("%s_bj_cum_mouth" % girl.gid)

                        # Finalize at idle position with back arms
                        $ store.bj_speed = 0
                        $ store.bj_action = "lick"
                        python:
                            _has_ba = bj_has_back_arms(girl)
                            if _has_ba:
                                store.bj_torso_type = 4
                                store.bj_idle_mouth = "mouth_sad"
                            else:
                                store.bj_torso_type = getattr(store, '_bj_pre_force_torso', _gsc(girl.gid, 'default_torso_type', 2, pose='blowjob'))
                            print("[CUM_FORCE_RISE] pre-ApplySpeed: bj_torso_type=%d has_back_arms=%s idle_mouth=%s" % (store.bj_torso_type, _has_ba, store.bj_idle_mouth))
                        call BJ_ApplySpeed(girl, 0) from _call_BJ_ApplySpeed_force_hold_ok
                        $ _tenny_bj_post_apply_correct(girl, 0) if girl.gid == "tenny" else None

                        # Switch to speaking face for post-swallow dialogue
                        python:
                            if _gsc(girl.gid, 'has_head_normal', False, pose='blowjob'):
                                store._bj_head_normal = True
                            renpy.hide("%s_bj_cum_mouth" % girl.gid)
                            if store._bj_head_normal:
                                _ht = bj_get_head_transform(0)
                                _pov = _gsc(girl.gid, 'pov_overlay', False, pose='blowjob')
                                renpy.show("%s blowjob_head head_normal" % girl.gid, tag="%s_bj_head" % girl.gid, at_list=[_ht], zorder=10058 if _pov else 10015)

                        # Trait-specific reaction after rising
                        if trait_is_veteran(girl, "cum_slut"):
                            $ set_scene_expression(girl, None, eyes="eyes_" + renpy.random.choice(["ahegao", "ahegao_2"]), mouth="mouth_happy")
                            $ Say_Line(girl, _("Straight from the source to deep down my throat. I loved that..."))
                        elif girl.has_trait("cum_slut"):
                            # still discovering it: surprised at herself, not a connoisseur (the virgin line below still fits)
                            $ set_scene_expression(girl, "surprised")
                            $ Say_Line(girl, renpy.random.choice([
                                _("That was... so deep... I can't believe I liked that."),
                                _("You held me down and I... I didn't want you to stop. What is wrong with me?"),
                            ]))
                        elif girl.has_trait("hate_cum") and girl.has_trait("hardcore_sex"):
                            $ set_scene_expression(girl, None, eyes="eyes_squint", mouth="mouth_smile")
                            $ Say_Line(girl, renpy.random.choice([
                                _("That was disgusting... but you holding me down like that..."),
                                _("I hated every second of that taste... but the rest? Don't stop being rough."),
                            ]))
                        elif girl.has_trait("submissive") and not girl.has_trait("cute_sex"):
                            # a gentle girl still minds being forced (her branch below, with its Love loss)
                            $ set_scene_expression(girl, None, eyes="eyes_normal", mouth="mouth_smile")
                            $ Say_Line(girl, renpy.random.choice([
                                _("I can go even deeper if you train me more like that..."),
                                _("You held me down and I didn't fight it once. Use my throat like that whenever you want."),
                                _("That's how you want me? Held down and swallowing? ...Then that's how I'll be."),
                            ]))
                        elif girl.has_trait("hardcore_sex"):
                            $ set_scene_expression(girl, None, eyes="eyes_normal", mouth="mouth_smile")
                            $ Say_Line(girl, _("Fuck... that was deep. Next time go even rougher."))
                        elif girl.has_trait("cute_sex"):
                            $ set_scene_expression(girl, None, eyes="eyes_" + renpy.random.choice(["closed", "left_closed"]), mouth="mouth_sad")
                            $ Say_Line(girl, renpy.random.choice([
                                _("You could have just asked me... you didn't need to force it."),
                                _("Why did you do that? I couldn't even breathe..."),
                            ]))
                            $ Change_Status(girl, "Love", -5)
                        else:
                            $ set_scene_expression(girl, None, eyes="eyes_squint", mouth="mouth_sad")
                            $ Say_Line(girl, _("Don't do that again without warning me first..."))

                        # Context-aware follow-up lines
                        if girl.has_trait("virgin") and not girl.player_firsts.get("force_throat"):
                            $ girl.player_firsts["force_throat"] = True
                            $ Say_Line(girl, _("I've never... no one has ever done that to me before."))
                        if girl.has_npc_partner():
                            if girl.has_trait("loyal"):
                                $ Say_Line(girl, _format_partner_line(girl, _("%(Pp)s would never do something like that to me... what am I doing?")))
                            elif girl.has_trait("cheater") and getattr(girl, "CheatAttitude", 1) >= 5:
                                $ Say_Line(girl, _format_partner_line(girl, _("It's not like %(pl)s has the guts to do that anyway...")))
                        if getattr(store, "_recording_active", False):
                            if girl.has_trait("camera_lover"):
                                $ Say_Line(girl, _("Wait, is that still recording? ...Good."))
                            elif girl.has_trait("camera_hater"):
                                $ set_scene_expression(girl, "angry")
                                $ Say_Line(girl, _("Tell me you didn't just record that."))
                        if _is_public_location():
                            if girl.has_trait("public_fetish"):
                                $ Say_Line(girl, _("Did anyone see that? ...I kind of hope they did."))
                            elif girl.has_trait("public_shy"):
                                $ set_scene_expression(girl, None, eyes="eyes_left_closed", brows="brows_confused")
                                $ Say_Line(girl, _("Oh god, what if someone saw that..."))

                        if _is_atm_force:
                            call _post_atm_swallow_reaction(girl) from _call_post_atm_sw_force

                        # Skip continue/stop — centralized handler decides after return

                    else:
                        # She BITES
                        "You feel her teeth pressing down on you. Hard."
                        python:
                            if girl.has_trait("hate_cum"):
                                _bite_pool = [
                                    _("You feel THAT?! Try that again and I'll bite it OFF! Get away from me!"),
                                    _("I will BITE through it if you don't let go RIGHT NOW!"),
                                ]
                            elif girl.has_trait("cute_sex"):
                                _bite_pool = [
                                    _("I trusted you... and you did this to me? Let go. Now."),
                                    _("How could you do that? I would have done it if you just asked..."),
                                ]
                            elif girl.has_trait("cute_sex"):
                                _bite_pool = [
                                    _("Mmph!! L-let go!! I can't... I'll bite harder! I mean it!"),
                                    _("S-stop!! You're hurting me! Let go or I'll... I'll really bite!"),
                                ]
                            else:
                                _bite_pool = [
                                    _("What the fuck was that?! Don't EVER do that again!"),
                                    _("Are you insane?! Next time I won't hold back."),
                                    _("You feel that? That's a warning. Push your luck and I bite for real."),
                                ]
                        $ set_scene_expression(girl, "angry", brows="brows_maniac")
                        $ Say_Line(girl, _tl(renpy.random.choice(_bite_pool)))
                        $ Change_Status(girl, "Love", -20)
                        $ Change_Status(girl, "Obed", -10)
                        if girl.has_trait("hate_cum"):
                            $ Change_Status(girl, "Love", -20)
                            $ Change_Status(girl, "Obed", -10)
                            $ store._hate_cum_scene_aborted = True
                        elif girl.has_trait("cute_sex"):
                            $ Change_Status(girl, "Love", -15)
                            $ Change_Status(girl, "Obed", -5)

                        # Release her head
                        $ renpy.hide("%s_bj_forcing_left" % girl.gid)
                        $ renpy.hide("%s_bj_forcing_right" % girl.gid)
                        $ store.bj_forcing = False
                        "You release her head."

                        # Slow rise from force depth to idle
                        if girl.gid == "tenny":
                            $ _tenny_bj_force_rise_anim(girl, show_cum=False)
                        else:
                            python:
                                _gid = girl.gid
                                _is_pov = _gsc(_gid, 'pov_overlay', False, pose='blowjob')
                                store.bj_idle_mouth = "mouth_tongue"
                                store.bj_action = "lick"
                                store.bj_speed = 0
                                _head_rise = getattr(renpy.store, "%s_bj_head_force_rise" % _gid, bj_head_force_rise)
                                _slot_rise = getattr(renpy.store, "%s_bj_slot_force_rise" % _gid, bj_slot_force_rise)
                                _rise_penis_z = 10055 if _is_pov else 9990
                                renpy.show("%s bj_penis" % _gid, tag="bj_penis", at_list=[_bj_get_penis_tf(girl)], zorder=_rise_penis_z)
                                if bj_has_sucking_mouth(girl):
                                    renpy.show("%s bj_sucking_mouth" % _gid, tag="%s_bj_sucking_mouth" % _gid, at_list=[_head_rise], zorder=10030)
                                else:
                                    renpy.hide("%s_bj_sucking_mouth" % _gid)
                                _below_img = "%s bj_sucking_below" % _gid
                                if renpy.has_image(_below_img):
                                    renpy.show(_below_img, tag="%s_bj_sucking_below" % _gid, at_list=[_head_rise], zorder=9985)
                                if _gid == "tenny":
                                    _rej_head = "%s blowjob_head head_deepthroat mouth_sad" % _gid
                                else:
                                    _rej_head = "%s blowjob_head mouth_sucking" % _gid
                                renpy.show(_rej_head, tag="%s_bj_head" % _gid, at_list=[_head_rise], zorder=10058 if _is_pov else 10015)
                                renpy.show("%s blowjob_jaw jaw_1" % _gid, tag="%s_bj_jaw" % _gid, at_list=[_head_rise], zorder=9984)
                                _attrs = _build_attributes_for_girl(girl, pose="blowjob")
                                _body_img = "%s blowjob" % _gid
                                if _attrs:
                                    _body_img += " " + " ".join(_attrs)
                                renpy.show(_body_img, tag=_gid, at_list=[_slot_rise], zorder=9980)
                                renpy.hide("%s_bj_right_arm" % _gid)
                                renpy.hide("%s_bj_arm" % _gid)
                                renpy.hide("%s_bj_hand" % _gid)
                                if renpy.has_image("%s bj_back_arm_left" % _gid):
                                    renpy.show("%s bj_back_arm_left" % _gid, tag="%s_bj_back_arm_left" % _gid, at_list=[_slot_rise], zorder=9970)
                                if renpy.has_image("%s bj_back_arm_right" % _gid):
                                    renpy.show("%s bj_back_arm_right" % _gid, tag="%s_bj_back_arm_right" % _gid, at_list=[_slot_rise], zorder=9970)
                        $ renpy.pause(0.8)

                        # Cleanup rise layers
                        $ renpy.hide("%s_bj_sucking_mouth" % girl.gid)
                        $ renpy.hide("%s_bj_sucking_below" % girl.gid)

                        # Finalize at idle
                        python:
                            _has_ba = bj_has_back_arms(girl)
                            if _has_ba:
                                store.bj_torso_type = 4
                                store.bj_idle_mouth = "mouth_sad"
                            else:
                                store.bj_torso_type = getattr(store, '_bj_pre_force_torso', _gsc(girl.gid, 'default_torso_type', 2, pose='blowjob'))
                        call BJ_ApplySpeed(girl, 0) from _call_BJ_ApplySpeed_force_hold_bite
                        $ _tenny_bj_post_apply_correct(girl, 0, mouth=None) if girl.gid == "tenny" else None

                        # Switch to speaking face for post-bite dialogue
                        python:
                            if _gsc(girl.gid, 'has_head_normal', False, pose='blowjob'):
                                store._bj_head_normal = True
                            if girl.gid == "tenny":
                                _ht = bj_get_head_transform(0)
                                _pov = _gsc("tenny", 'pov_overlay', False, pose='blowjob')
                                renpy.show("tenny blowjob_head head_normal", tag="tenny_bj_head", at_list=[_ht], zorder=10058 if _pov else 10015)

                        # She spits it out violently
                        $ set_scene_expression(girl, "angry", brows="brows_maniac")
                        "She spits it out."
                        $ _remove_cum_tag(girl, "mouth")

                        # Angry post-bite dialogue
                        python:
                            if girl.has_trait("hate_cum"):
                                _bite_after_pool = [
                                    _("Get AWAY from me! I can't believe you tried that!"),
                                    _("We're DONE! You think you can just force that on me?!"),
                                ]
                            elif girl.has_trait("cute_sex"):
                                _bite_after_pool = [
                                    _("How could you do that to me?! I trusted you!"),
                                    _("I had to BITE you to make you stop! What is wrong with you?!"),
                                ]
                            else:
                                _bite_after_pool = [
                                    _("You're lucky I didn't bite harder. Don't EVER try that again."),
                                    _("Next time I won't give a warning. Understand?"),
                                ]
                        $ Say_Line(girl, _tl(renpy.random.choice(_bite_after_pool)))

                        if store._hate_cum_scene_aborted:
                            # hate_cum: scene ends with redress
                            $ debug_log("[DEBUG] bite: hate_cum abort, running BJ_End + DressUp")
                            call BJ_End(girl, dress_up=False) from _call_BJ_End_bite_abort
                            call DressUp_Sequence(girl) from _call_DressUp_bite_abort
                            if getattr(store, "_coercion_type", None):
                                $ debug_log("[DEBUG] bite abort: coercion post-scene (%s)" % store._coercion_type)
                                $ store._coercion_type_for_post = store._coercion_type
                                $ store._coercion_type = None
                                call _coercion_post_scene(girl, store._coercion_type_for_post) from _call_coerce_post_bite
                            python:
                                scene_full_cleanup(girl)
                                _loc_loops = _LOC_LOOPS   # central map (navigation.rpy); the local copy had no "tenny_room"
                                _target = _loc_loops.get(store.CurrentLocation, "Campus_Loop")
                                renpy.jump(_target)
                        else:
                            # First kiss aftermath (if ATM before first kiss)
                            if getattr(store, "_atm_cum_in_mouth", False):
                                call _post_atm_first_kiss_reaction(girl) from _call_post_atm_fk_bite

                            # Skip continue/stop — centralized handler decides after return

                "Let go":
                    # Release forcing hands
                    $ renpy.hide("%s_bj_forcing_left" % girl.gid)
                    $ renpy.hide("%s_bj_forcing_right" % girl.gid)
                    $ store.bj_forcing = False

                    # Slow rise from force depth to idle (keep mouth cum visible)
                    if girl.gid == "tenny":
                        $ _tenny_bj_force_rise_anim(girl, show_cum=True)
                    else:
                        python:
                            _gid = girl.gid
                            _is_pov = _gsc(_gid, 'pov_overlay', False, pose='blowjob')
                            store.bj_idle_mouth = "mouth_tongue"
                            store.bj_action = "lick"
                            store.bj_speed = 0
                            _head_rise = getattr(renpy.store, "%s_bj_head_force_rise" % _gid, bj_head_force_rise)
                            _slot_rise = getattr(renpy.store, "%s_bj_slot_force_rise" % _gid, bj_slot_force_rise)
                            _rise_penis_z = 10055 if _is_pov else 9990
                            renpy.show("%s bj_penis" % _gid, tag="bj_penis", at_list=[_bj_get_penis_tf(girl)], zorder=_rise_penis_z)
                            if bj_has_sucking_mouth(girl):
                                renpy.show("%s bj_sucking_mouth" % _gid, tag="%s_bj_sucking_mouth" % _gid, at_list=[_head_rise], zorder=10030)
                            else:
                                renpy.hide("%s_bj_sucking_mouth" % _gid)
                            _below_img = "%s bj_sucking_below" % _gid
                            if renpy.has_image(_below_img):
                                renpy.show(_below_img, tag="%s_bj_sucking_below" % _gid, at_list=[_head_rise], zorder=9985)
                            _lg_head = "%s blowjob_head mouth_sucking" % _gid
                            renpy.show(_lg_head, tag="%s_bj_head" % _gid, at_list=[_head_rise], zorder=10058 if _is_pov else 10015)
                            renpy.show("%s blowjob_jaw jaw_1" % _gid, tag="%s_bj_jaw" % _gid, at_list=[_head_rise], zorder=9984)
                            _attrs = _build_attributes_for_girl(girl, pose="blowjob")
                            _body_img = "%s blowjob" % _gid
                            if _attrs:
                                _body_img += " " + " ".join(_attrs)
                            renpy.show(_body_img, tag=_gid, at_list=[_slot_rise], zorder=9980)
                            renpy.hide("%s_bj_right_arm" % _gid)
                            renpy.hide("%s_bj_arm" % _gid)
                            renpy.hide("%s_bj_hand" % _gid)
                            for _suffix, _z in [("bj_cum_face", 10025), ("bj_cum_face_under", 9986), ("bj_cum_mouth", 9988)]:
                                _img = "%s %s" % (_gid, _suffix)
                                if renpy.has_image(_img):
                                    renpy.show(_img, tag="%s_%s" % (_gid, _suffix), at_list=[_head_rise], zorder=_z)
                    $ renpy.pause(0.8)

                    # Cleanup rise layers
                    $ renpy.hide("%s_bj_sucking_mouth" % girl.gid)
                    $ renpy.hide("%s_bj_sucking_below" % girl.gid)

                    # Finalize at idle position + restore arms
                    $ store.bj_speed = 0
                    $ store.bj_action = "lick"
                    python:
                        _has_ba = bj_has_back_arms(girl)
                        if _has_ba:
                            store.bj_torso_type = 4
                            store.bj_idle_mouth = "mouth_sad"
                        else:
                            store.bj_torso_type = getattr(store, '_bj_pre_force_torso', _gsc(girl.gid, 'default_torso_type', 2, pose='blowjob'))
                        print("[CUM_LETGO_RISE] pre-ApplySpeed: torso_type=%d has_back_arms=%s idle_mouth=%s" % (store.bj_torso_type, _has_ba, store.bj_idle_mouth))
                    call BJ_ApplySpeed(girl, 0) from _call_BJ_ApplySpeed_force_let_go
                    $ _tenny_bj_post_apply_correct(girl, 0) if girl.gid == "tenny" else None

                    # Re-show mouth cum above head (10017) so it's visible during reaction menu
                    python:
                        _cm_img = "%s bj_cum_mouth" % girl.gid
                        if renpy.has_image(_cm_img):
                            _ht = bj_get_head_transform(0)
                            renpy.show(_cm_img, tag="%s_bj_cum_mouth" % girl.gid, at_list=[_ht], zorder=10017)

                    $ apply_cum_bonuses(girl, "cum_in_mouth_allowed")
                    call _bj_mouth_cum_reaction(girl, False, skip_post_menu=True) from _call__bj_mcr_force_mouth_via_bj
    $ debug_log("[DEBUG] _bj_mouth_cum_reaction returned, _hate_cum_scene_aborted=%s" % str(store._hate_cum_scene_aborted))

    # Continue/stop menu while still in BJ pose (before returning to original scene)
    # Skipped if reaction already decided (hate_cum abort, forced jump, etc.)
    $ store._via_bj_post_cum_choice = None
    if not store._hate_cum_scene_aborted:
        if store._player_exhausted:
            $ store._via_bj_post_cum_choice = "stop"
            $ debug_log("[DEBUG] via_bj menu: auto-stop (exhausted)")
        elif _vbj_had_condom or (story_act_locked(girl, "raw") and _scene_is_penetrative(orig_scene)):
            # He had a condom on, or her step locks raw AND the scene he goes back to penetrates: another
            # condom / ask to go raw / stop, never a bare "Keep going" that would put him back in her with
            # nothing on. From a HAND scene (hj/tj/fj) there is nothing raw to return to: the condom menu
            # after a handjob mouth finish read as "the game thinks we had sex" (tester 2026-10-10)
            call _post_cum_condom_menu(girl) from _call_pcc_via_bj
            $ store._via_bj_post_cum_choice = "stop" if store._pcc_choice == "stop" else "continue"
            if store._pcc_choice == "condom":
                # BJ_End and the relaunch reset the condom (scene_full_cleanup): put back after them
                $ _vbj_condom_snap = condom_carry_save()
            $ print("[SCENE_FLOW] mouth finish (BJ pose, he had a condom=%s): condom menu -> %s" % (_vbj_had_condom, store._pcc_choice))
        else:
            menu:
                "Keep going":
                    $ store._via_bj_post_cum_choice = "continue"
                    $ debug_log("[DEBUG] via_bj menu: player chose CONTINUE")
                "Stop now":
                    $ store._via_bj_post_cum_choice = "stop"
                    $ debug_log("[DEBUG] via_bj menu: player chose STOP")

    # Return to original scene
    # Preserve recording state across BJ_End (finalize_recording destroys it)
    $ _saved_rec_bj = getattr(store, "_recording_active", False)
    $ _saved_rec_girl_bj = getattr(store, "_recording_girl", None)
    $ _saved_hand_bj = getattr(store, "_player_hand_disabled", None)
    $ _saved_rec_seconds_bj = getattr(store, "_recording_seconds", 0.0)
    $ _saved_rec_rate_bj = getattr(store, "_recording_sec_rate", 0.0)
    # Preserve stripped clothes across BJ_End (scene_full_cleanup would restore)
    $ _saved_clothes_bj = dict(girl.clothes)
    $ _saved_clothes_state_bj = dict(girl.clothes_state)
    $ _saved_outfit_ref_bj = getattr(girl, "_saved_outfit", None)
    $ debug_log("[DEBUG] calling BJ_End, saving recording=%s girl=%s" % (_saved_rec_bj, _saved_rec_girl_bj))
    call BJ_End(girl, dress_up=False) from _call_BJ_End_mouth_via_bj
    # Restore recording state after BJ_End
    $ store._recording_active = _saved_rec_bj
    $ store._recording_girl = _saved_rec_girl_bj
    $ store._player_hand_disabled = _saved_hand_bj
    $ store._recording_seconds = _saved_rec_seconds_bj
    $ store._recording_sec_rate = _saved_rec_rate_bj
    if _saved_rec_bj and not renpy.get_screen("recording_overlay"):
        $ renpy.show_screen("recording_overlay")
        $ debug_log("[DEBUG] BJ_End: recording overlay re-shown")
    # Restore stripped clothes after BJ_End
    $ girl.clothes = _saved_clothes_bj
    $ girl.clothes_state = _saved_clothes_state_bj
    $ girl._saved_outfit = _saved_outfit_ref_bj
    $ debug_log("[DEBUG] BJ_End returned, recording restored=%s, aborted=%s orig_scene=%s" % (_saved_rec_bj, str(store._hate_cum_scene_aborted), orig_scene))

    if store._hate_cum_scene_aborted:
        $ debug_log("[DEBUG] ABORTED - returning to original scene as exhausted")
        $ store._hate_cum_scene_aborted = False
        $ store._player_exhausted = True
        if getattr(store, "_coercion_type", None):
            $ debug_log("[DEBUG] abort: coercion post-scene (%s)" % store._coercion_type)
            $ store._coercion_type_for_post = store._coercion_type
            $ store._coercion_type = None
            call _coercion_post_scene(girl, store._coercion_type_for_post) from _call_coerce_post_bjstop

    # Skip relaunch if player chose stop in BJ menu or scene was force-ended
    $ _skip_relaunch = store._scene_force_end or (store._via_bj_post_cum_choice == "stop") or store._player_exhausted
    if not _skip_relaunch:
        if orig_scene == "hj":
            call HJ_Launch(girl) from _call_HJ_Launch_mouth_via_bj
        elif orig_scene == "tj":
            call TITJOB_Launch(girl) from _call_TITJOB_Launch_mouth_via_bj
        elif orig_scene == "fj":
            call FT_Launch(girl) from _call_FT_Launch_mouth_via_bj
        elif orig_scene in ("reverse_cowgirl", "reverse_cowgirl_anal"):
            $ debug_log("[DEBUG] calling RCG_Launch to return to RCG (anal=%s)" % _saved_rcg_anal)
            $ _saved_skirt_state = girl.clothes_state.get("skirt")
            $ rcg_speed = 2
            $ store.rcg_anal = _saved_rcg_anal
            call RCG_Launch(girl, from_switch=True) from _call_RCG_Launch_mouth_via_bj
            # RCG_Launch resets skirt "up"->"full" for position switches,
            # but returning from mouth cum should preserve original state
            if _saved_skirt_state is not None and _saved_skirt_state != girl.clothes_state.get("skirt"):
                $ girl.clothes_state["skirt"] = _saved_skirt_state
            # he is back in her (the hole the scene had): the layers drew her hovering at speed 0 above
            $ store.rcg_started = True
            $ renpy.with_statement(None)
            call RCG_ApplySpeed(girl, rcg_speed) from _call_RCG_ApplySpeed_mouth_via_bj
        elif orig_scene == "cowgirl":
            call COWGIRL_Launch(girl, from_switch=True) from _call_COWGIRL_Launch_mouth_via_bj
            $ store.cowgirl_started = True
            $ renpy.with_statement(None)
            call COWGIRL_ApplySpeed(girl, 2) from _call_COWGIRL_ApplySpeed_mouth_via_bj
        elif orig_scene in ("doggy", "anal"):
            $ store.doggy_anal = (orig_scene == "anal")
            call DG_Launch(girl, from_switch=True) from _call_DG_Launch_mouth_via_bj
            if _saved_tip_mode:
                $ store.doggy_tip_mode = True
                call DG_HoleTransition(girl, store.doggy_anal) from _call_DG_HoleTransition_mouth_via_bj
                call DG_ApplySpeed(girl, 1) from _call_DG_ApplySpeed_mouth_via_bj_tip
            else:
                $ store.doggy_started = True
                $ store._dg_had_anal = (orig_scene == "anal")
                $ store._dg_had_pussy = (orig_scene == "doggy")
                $ renpy.with_statement(None)
                call DG_ApplySpeed(girl, 2) from _call_DG_ApplySpeed_mouth_via_bj
        elif orig_scene in ("full_nelson", "full_nelson_anal"):
            $ store.fn_anal = _saved_fn_anal
            call FN_Launch(girl, from_switch=True) from _call_FN_Launch_mouth_via_bj
            if _saved_fn_tip_mode:
                $ store.fn_tip_mode = True
                call FN_HoleTransition(girl, store.fn_anal) from _call_FN_HoleTransition_mouth_via_bj
                call FN_ApplySpeed(girl, 1) from _call_FN_ApplySpeed_mouth_via_bj_tip
            else:
                $ store.fn_started = True
                $ store._fn_had_anal = (orig_scene == "full_nelson_anal")
                $ store._fn_had_pussy = (orig_scene == "full_nelson")
                $ renpy.with_statement(None)
                call FN_ApplySpeed(girl, 2) from _call_FN_ApplySpeed_mouth_via_bj
        elif orig_scene in ("laying_down", "laying_anal"):
            $ store.laying_anal = _saved_ld_anal
            call LD_Launch(girl, from_switch=True) from _call_LD_Launch_mouth_via_bj
            if _saved_ld_tip_mode:
                $ store.laying_tip_mode = True
                call LD_HoleTransition(girl, store.laying_anal) from _call_LD_HoleTransition_mouth_via_bj
                call LD_ApplySpeed(girl, 1) from _call_LD_ApplySpeed_mouth_via_bj_tip
            elif _saved_ld_rub_mode:
                $ store.laying_rub_mode = True
                call LD_ApplySpeed(girl, 0) from _call_LD_ApplySpeed_mouth_via_bj_rub
            else:
                $ store.laying_started = True
                $ store._ld_had_anal = (orig_scene == "laying_anal")
                $ store._ld_had_pussy = (orig_scene == "laying_down")
                if orig_scene == "laying_down":
                    $ girl._ld_after_pussy = True
                if orig_scene == "laying_anal":
                    $ girl._ld_after_anal = True
                $ renpy.with_statement(None)
                call LD_ApplySpeed(girl, 2) from _call_LD_ApplySpeed_mouth_via_bj

    # Restore NTR watching state after scene relaunch (Launch calls _kill_scene_threads again)
    $ store._ntr_partner_watching = _saved_ntr_watching
    $ store._ntr_watching_npc = _saved_ntr_npc
    $ store._ntr_session_watcher_gid = _saved_ntr_sess_watcher
    # The fresh condom he put on in the BJ pose, back on him in the relaunched scene
    if _vbj_condom_snap and not _skip_relaunch:
        $ condom_carry_restore(_vbj_condom_snap)
    # Restore exhaustion (scene_full_cleanup reset it, but energy is still 0)
    if _skip_relaunch:
        $ store._player_exhausted = True
    else:
        $ store._player_exhausted = _saved_exhausted or (store.Player.energy <= 0)
    $ print("[SCENE_FLOW] mouth finish done: relaunched=%s choice=%s | %s" % (not _skip_relaunch, store._via_bj_post_cum_choice, scene_flow_state()))
    $ debug_log("[DEBUG] _cum_in_mouth_via_bj END, ntr_watching=%s exhausted=%s skip_relaunch=%s returning" % (_saved_ntr_watching, store._player_exhausted, _skip_relaunch))
    return

# ------------------------------------------------------------
# PlayerCumMenu_Oral... HJ / BJ / TJ
# ------------------------------------------------------------
label PlayerCumMenu_Oral(girl, scene_type):
    $ debug_log("[DEBUG] PlayerCumMenu_Oral: entered, scene_type=%s" % scene_type)
    $ _is_cum_slut_oral = girl.has_trait("cum_slut")
    $ _cs_forces_oral = trait_is_veteran(girl, "cum_slut")   # still discovering it: she wants it, never forces it
    $ _is_hate_cum_oral = girl.has_trait("hate_cum")
    $ _cumslut_cream_oral = getattr(girl, "CreampieCounts", 0)

    # ── cum_slut during BJ: she forces it in her mouth (resist-gated) ──
    # Skip when bj_forcing: player is already forcing her head down, she can't wrestle for control
    if _cs_forces_oral and scene_type == "bj" and not _forced_cum_on_cooldown(girl) and not getattr(store, "bj_forcing", False):
        $ _auto_resist_reason = _get_auto_resist_reason(girl)
        $ _bj_resist_saved_speed = store.bj_speed
        $ store.bj_speed = 0
        call BJ_ApplySpeed(girl, 0) from _call_BJ_ApplySpeed_resist_freeze

        if _auto_resist_reason:
            # ── AUTO-RESIST BJ: she tries but FAILS ──
            python:
                _intent_pool = RESIST_AUTO_OBED_GIRL["bj"] if _auto_resist_reason == "obed" else RESIST_AUTO_STRENGTH_GIRL["bj"]
            $ Say_Line(girl, _tl(renpy.random.choice(_intent_pool)))

            if _auto_resist_reason == "obed":
                $ _narr = _tl(renpy.random.choice(RESIST_AUTO_OBED_NARR))
                "[_narr]"
                $ Say_Line(girl, _tl(renpy.random.choice(RESIST_AUTO_OBED_GIRL_AFTER)))
            else:
                python:
                    _narr = _tl(renpy.random.choice(RESIST_AUTO_STRENGTH_NARR["oral"]))
                "[_narr]"
                $ Say_Line(girl, _tl(renpy.random.choice(RESIST_AUTO_STRENGTH_GIRL_AFTER)))
                # "She tried, but you're stronger": the automatic strength resist IS that (Athlete / Max Energy 5)
                $ unlock_achievement("iron_will")

            $ Change_Status(girl, "Obed", 10)
            $ store.bj_speed = _bj_resist_saved_speed
            call BJ_ApplySpeed(girl, _bj_resist_saved_speed) from _call_BJ_ApplySpeed_resist_restore
            # fall through to normal oral menu

        else:
            # ── CAN'T AUTO-RESIST BJ: last-moment menu ──
            python:
                _cs_force_lines = [
                    _("NO NO NO! I WANT IT!"),
                    _("DON'T YOU DARE PULL OUT! GIVE IT TO ME!"),
                    _("IT'S MINE! CUM IN MY MOUTH!"),
                ]
            $ Say_Line(girl, _tl(renpy.random.choice(_cs_force_lines)))

            call _player_resist_forced_cum(girl, "bj") from _call_resist_bj

            if store._resist_result == "resisted":
                $ Change_Status(girl, "Obed", 10)
                $ store.bj_speed = _bj_resist_saved_speed
                call BJ_ApplySpeed(girl, _bj_resist_saved_speed) from _call_BJ_ApplySpeed_resist_restore2
                # fall through to normal oral menu
            else:
                # Player accepted or failed — forced BJ cum. BJ_CumAnim snapshots bj_speed as her speed to resume
                # at: give it back the real one (the resist freeze left 0 there), it re-freezes by itself.
                $ store.bj_speed = _bj_resist_saved_speed
                call BJ_CumAnim(girl) from _call_BJ_CumAnim_cs_force
                $ process_cum(girl, scene_type, "mouth")
                $ apply_cum_bonuses(girl, "cum_in_mouth_allowed")
                call _bj_mouth_cum_reaction(girl, False) from _call__bj_mcr_cs_force
                return

    # ── cum_slut 3+ creampies: she begs before the menu ──
    if _is_cum_slut_oral and _cumslut_cream_oral >= 3:
        python:
            _beg_oral = [
                _("Wait... can't you put it inside me instead? Please... I want to feel you cum inside..."),
                _("Don't cum like this... I want it inside me... please..."),
                _("Wouldn't you rather cum inside me? Please... I need it..."),
            ]
        $ Say_Line(girl, _tl(renpy.random.choice(_beg_oral)))

    menu:
        "Fire away":
            # cum_slut intercept: she's desperate
            if _cs_forces_oral:
                python:
                    _cs_fire_despair = [
                        _("No! Don't waste it! Please, at least let me swallow it!"),
                        _("You're just going to fire it into the air?! That's MY cum! Don't waste it!"),
                        _("Stop! At least aim it at me! I need every drop!"),
                        _("Are you serious?! That cum belongs INSIDE me, not on the floor!"),
                    ]
                $ Say_Line(girl, _tl(renpy.random.choice(_cs_fire_despair)))
                $ Change_Status(girl, "Love", -3)
                $ girl._cumslut_denied_inside = True
            elif _is_cum_slut_oral:
                # still discovering it: a little disappointed, no fight (and no revenge creampie later)
                python:
                    _cs_fire_curious = [
                        _("Oh... okay. I kind of wanted to feel it, though..."),
                        _("Wait... I wanted it... never mind."),
                        _("Aw... I was hoping you'd let me have it."),
                    ]
                $ Say_Line(girl, _tl(renpy.random.choice(_cs_fire_curious)))

            call _cum_dispatch_fire_away(girl, scene_type) from _call__cum_dispatch_fire_away_oral
            $ process_cum(girl, scene_type, "away")
            $ apply_cum_bonuses(girl, "cum_outside")
            if _is_hate_cum_oral:
                $ Change_Status(girl, "Love", -5)
            $ Change_Status(girl, "Obed", 1)

            # TJ fire away: frozen state, player decides to continue or stop
            if scene_type == "tj":
                if store._player_exhausted:
                    pass
                else:
                    menu:
                        "Continue":
                            call TITJOB_ApplySpeed(girl, titjob_speed) from _call_TITJOB_ApplySpeed_fire_cont
                        "Stop":
                            call TITJOB_End(girl, dress_up=False) from _call_TITJOB_End_fire_stop
                            $ store._player_exhausted = True

            # FJ fire away: same pattern as TJ
            if scene_type == "fj":
                if store._player_exhausted:
                    pass
                else:
                    menu:
                        "Continue":
                            call FT_ApplySpeed(girl, _ft_speed) from _call_FT_ApplySpeed_fire_cont
                        "Stop":
                            call FT_End(girl, dress_up=False) from _call_FT_End_fire_stop
                            $ store._player_exhausted = True

        "Cum outside":
            # cum_slut intercept: covering her is not enough
            if _cs_forces_oral:
                python:
                    _cs_outside_despair = [
                        _("No... covering me is not enough... I need it INSIDE me..."),
                        _("Outside?! Why would you waste it on my skin when you could fill me up?!"),
                        _("Please... don't cum outside... I want to feel it deep inside..."),
                        _("On me? That's not where it belongs! It belongs INSIDE me!"),
                    ]
                $ Say_Line(girl, _tl(renpy.random.choice(_cs_outside_despair)))
                $ Change_Status(girl, "Love", -3)
                $ girl._cumslut_denied_inside = True
            # still discovering it: no fight here, her "cum_<where>" reaction (cum_slut_first / _new) says the rest

            python:
                _cum_outside_warns = [
                    _("[girl.Name], I'm close..."),
                    _("[girl.Name], I'm gonna cum..."),
                    _("I... I'm cumming..."),
                ]
            $ Say_Player(_tl(renpy.random.choice(_cum_outside_warns)))
            if _is_hate_cum_oral:
                $ Change_Status(girl, "Love", -5)
            call PlayerCumMenu_Outside_Oral(girl, scene_type) from _call_PlayerCumMenu_Outside_Oral
            $ Change_Status(girl, "Obed", 1)

        "Warn her":
            call _cum_warn_her_oral(girl, scene_type) from _call__cum_warn_her_oral
            $ Change_Status(girl, "Obed", 1)

        "Ask to cum inside her mouth":
            $ _cum_check = CumPermissionCheck(girl, "cum_in_mouth_ask")
            if scene_type == "bj" and getattr(store, "hiding_face", False):
                $ store.hiding_face = False
                call BJ_ApplySpeed(girl, 0) from _call_BJ_ApplySpeed_unhide_mouth_ask
                if getattr(store, "_recording_active", False):
                    $ Say_Line(girl, _("Wait, stop recording!"))
                    $ finalize_recording()
            if _cum_check["accepted"]:
                $ Say_Line(girl, scene_pick_line("cum_mouth_accepted", scene=scene_type, girl=girl) or _("Go ahead... do it."))
                if scene_type == "bj":
                    call BJ_CumAnim(girl) from _call_BJ_CumAnim_ask_ok
                    $ process_cum(girl, scene_type, "mouth")
                    $ apply_cum_bonuses(girl, "cum_in_mouth_allowed")
                    call _bj_mouth_cum_reaction(girl, False) from _call__bj_mcr_ask
                elif scene_type in ("hj", "tj", "fj", "reverse_cowgirl", "cowgirl"):
                    call _cum_in_mouth_via_bj(girl, scene_type) from _call__cum_in_mouth_via_bj_ask
                else:
                    $ process_cum(girl, scene_type, "mouth")
                    $ apply_cum_bonuses(girl, "cum_in_mouth_allowed")
                    $ Say_Line(girl, scene_pick_line("cum_mouth", scene=scene_type, girl=girl) or _("She swallows it all."))
            else:
                $ set_scene_expression(girl, "angry")
                $ Say_Line(girl, scene_pick_line("cum_mouth_denied", scene=scene_type, girl=girl) or _("No way... not in my mouth."))
                $ _deny_lbl = _cum_cfg(scene_type, "outside_freeze") or _cum_cfg(scene_type, "cum_anim")
                if _deny_lbl:
                    call expression _deny_lbl pass (girl) from _call__cum_mouth_deny_dispatch
                $ process_cum(girl, scene_type, "outside")
                $ apply_cum_bonuses(girl, "cum_outside")
            if _is_hate_cum_oral:
                $ Change_Status(girl, "Love", -10)
            $ Change_Status(girl, "Obed", 1)

        "Cum in her mouth" if scene_type == "bj":
            $ _cum_check = CumPermissionCheck(girl, "cum_in_mouth_ask")
            call BJ_CumAnim(girl, True) from _call_BJ_CumAnim_forced
            $ process_cum(girl, scene_type, "mouth")
            if _cum_check["accepted"]:
                $ apply_cum_bonuses(girl, "cum_in_mouth_allowed")
                call _bj_mouth_cum_reaction(girl, False) from _call__bj_mcr_force_ok
            else:
                $ apply_cum_penalties(girl, "cum_in_mouth_forced")
                call _bj_mouth_cum_reaction(girl, True) from _call__bj_mcr_force_bad
            if _is_hate_cum_oral:
                $ Change_Status(girl, "Love", -15)
            $ Change_Status(girl, "Obed", 1)

    return

# ------------------------------------------------------------
# PlayerCumMenu_Outside_Oral... submenu for oral cum-outside
# ------------------------------------------------------------
label PlayerCumMenu_Outside_Oral(girl, scene_type):

    menu:
        "All over her":
            call _cum_dispatch_anim(girl, scene_type) from _call__cum_dispatch_anim_allover
            if scene_type == "tj":
                $ process_cum(girl, scene_type, "outside", ["face", "boobs", "head", "shoulders"])
            elif scene_type == "fj":
                # the footjob has its own overlay art for each spot (_ft_add_cum, Tenny/Footjob.rpy)
                $ _ft_add_cum("face", "boobs", "belly")
                $ process_cum(girl, scene_type, "outside", ["face", "boobs", "belly"])
            else:
                $ process_cum(girl, scene_type, "outside", ["face", "boobs", "head"])
            $ apply_cum_bonuses(girl, "cum_outside")
            $ _cum_say_line(girl, "outside", scene_type)

        "On her face":
            call _cum_dispatch_anim(girl, scene_type) from _call__cum_dispatch_anim_face
            if scene_type == "fj":
                $ _ft_add_cum("face")
            $ process_cum(girl, scene_type, "face")
            $ apply_cum_bonuses(girl, "cum_outside")
            $ _cum_say_line(girl, "face", scene_type)

        "On her tits":
            call _cum_dispatch_anim(girl, scene_type) from _call__cum_dispatch_anim_tits
            if scene_type == "fj":
                $ _ft_add_cum("boobs")
            $ process_cum(girl, scene_type, "tits")
            $ apply_cum_bonuses(girl, "cum_outside")
            $ _cum_say_line(girl, "tits", scene_type)

        "On her wedding ring" if scene_type == "hj" and girl_wears_ring(girl):
            call _netori_ring_cum(girl, scene_type) from _call__netori_ring_cum_hj

        "On her belly" if scene_type == "fj":
            call _cum_dispatch_anim(girl, scene_type) from _call__cum_dispatch_anim_belly_fj
            $ _ft_add_cum("belly")
            $ process_cum(girl, scene_type, "belly")
            $ apply_cum_bonuses(girl, "cum_outside")
            $ _cum_say_line(girl, "belly", scene_type)

        "On her feet" if scene_type == "fj":
            call _cum_dispatch_anim(girl, scene_type) from _call__cum_dispatch_anim_feet
            $ process_cum(girl, scene_type, "feet")
            $ apply_cum_bonuses(girl, "cum_outside")
            $ _cum_say_line(girl, "feet", scene_type)

    return

# ------------------------------------------------------------
# BJ mouth cum reaction — swallow / spit
# forced=True when player came in her mouth without permission
# ------------------------------------------------------------
label _bj_mouth_cum_reaction(girl, forced=False, skip_post_menu=False):

    $ store._bj_mouth_cum_continued = False

    # Promote penis above head and cum_mouth above mouth expression
    # so the cum layer is visible during the swallow/spit menu.
    # Standard: penis 10020 > cum_mouth 10017 > head 10015
    # POV:      penis(10059) > head(10058) > cum_mouth(10040)
    python:
        _gid = girl.gid
        _ht = bj_get_head_transform(0)
        _pov_mcr = _gsc(_gid, 'pov_overlay', False, pose='blowjob')
        _mcr_penis_z = 10059 if _pov_mcr else 10020
        _mcr_cum_mouth_z = 10040 if _pov_mcr else 10017
        print("[BJ_MOUTH_CUM_REACT] pov=%s, penis z=%d, cum_mouth z=%d" % (_pov_mcr, _mcr_penis_z, _mcr_cum_mouth_z))
        if _gsc(_gid, 'has_head_normal', False, pose='blowjob'):
            store._bj_head_normal = True
            renpy.show("%s blowjob_head head_normal mouth_tongue" % _gid, tag="%s_bj_head" % _gid, at_list=[_ht], zorder=10058 if _pov_mcr else 10015)
            if renpy.has_image("%s blowjob_jaw" % _gid):
                renpy.show("%s blowjob_jaw jaw_1" % _gid, tag="%s_bj_jaw" % _gid, at_list=[_ht], zorder=9984)
            _mcr_cum_mouth_z = 10059 if _pov_mcr else 10017
            print("[BJ_MOUTH_CUM_REACT] %s: head_normal + jaw, cum_mouth z=%d" % (_gid, _mcr_cum_mouth_z))
        renpy.show(
            "%s bj_penis" % _gid,
            tag="bj_penis",
            at_list=[_bj_get_penis_tf(girl)],
            zorder=_mcr_penis_z
        )
        _cm_img = "%s bj_cum_mouth" % _gid
        if renpy.has_image(_cm_img):
            renpy.show(_cm_img, tag="%s_bj_cum_mouth" % _gid, at_list=[_ht], zorder=_mcr_cum_mouth_z)
        if _pov_mcr:
            _mcr_slot = bj_get_slot_transform(0)
            if store.bj_torso_type == 4:
                renpy.hide("%s_bj_right_arm" % _gid)
                renpy.hide("%s_bj_arm" % _gid)
                renpy.hide("%s_bj_hand" % _gid)
                _ba_l = "%s bj_back_arm_left" % _gid
                _ba_r = "%s bj_back_arm_right" % _gid
                if renpy.has_image(_ba_l):
                    renpy.show(_ba_l, tag="%s_bj_back_arm_left" % _gid, at_list=[_mcr_slot], zorder=9970)
                if renpy.has_image(_ba_r):
                    renpy.show(_ba_r, tag="%s_bj_back_arm_right" % _gid, at_list=[_mcr_slot], zorder=9970)
                print("[BJ_MOUTH_CUM_REACT] POV torso_type==4: back arms, hid front arms")
            else:
                if renpy.has_image("%s bj_right_arm" % _gid):
                    renpy.show("%s bj_right_arm" % _gid, tag="%s_bj_right_arm" % _gid, at_list=[_mcr_slot, hj_pov_arm_right_speed0()], zorder=10051)
                if renpy.has_image("%s bj_arm" % _gid):
                    renpy.show("%s bj_arm" % _gid, tag="%s_bj_arm" % _gid, at_list=[_mcr_slot, hj_pov_arm_left_speed0()], zorder=10052)
                renpy.show("%s bj_hand" % _gid, tag="%s_bj_hand" % _gid, at_list=[bj_cum_hand_static], zorder=10060)
                print("[BJ_MOUTH_CUM_REACT] POV: front arms+hand stopped at speed 0")

    # Random eyes for showing mouth cum (normal girls)
    $ _mcr_show_eyes = "eyes_" + renpy.random.choice(["left_closed", "right_closed", "squint", "squint_2"])

    # ── cum_slut: auto-swallow, immediate ──
    if girl.has_trait("cum_slut"):
        $ _cs_mcr_veteran = trait_is_veteran(girl, "cum_slut")
        if _cs_mcr_veteran:
            # Show mouth cum with ahegao eyes
            $ set_scene_expression(girl, None, eyes="eyes_" + renpy.random.choice(["ahegao", "ahegao_2"]), mouth="mouth_tongue")
            $ renpy.pause(0.6)
        else:
            # Still discovering it (trait_is_new): she tastes it first, surprised by how much she likes it
            $ set_scene_expression(girl, "surprised", mouth="mouth_tongue")
            $ renpy.pause(0.6)
            $ _cs_mcr_line = scene_pick_line("cum_mouth", scene="bj", girl=girl)
            $ print("[CUM] %s mouth load while discovering cum_slut: %s" % (girl.gid, _cs_mcr_line))
            if _cs_mcr_line:
                $ Say_Line(girl, _cs_mcr_line)
        # Swallow: closed happy + lipbite, remove cum layer
        $ set_scene_expression(girl, "closed_happy")
        # Tenny: switch from deepthroat to regular head on swallow
        if girl.gid == "tenny":
            python:
                _ht = bj_get_head_transform(0)
                _pov = _gsc("tenny", 'pov_overlay', False, pose='blowjob')
                renpy.show("tenny blowjob_head head_normal", tag="tenny_bj_head", at_list=[_ht], zorder=10058 if _pov else 10015)
        $ _remove_cum_tag(girl, "mouth")
        $ renpy.pause(0.6)
        # Post-swallow: open eyes, happy
        if _cs_mcr_veteran:
            $ set_scene_expression(girl, "happy")
            "She doesn't seem satisfied with just that."
        else:
            $ set_scene_expression(girl, "embarrassed")
            "She blushes, a little surprised at how much she liked that."
        $ Change_Status(girl, "Obed", 20)
        $ Change_Status(girl, "Inbt", 25)
        $ girl.Lust = min(100, getattr(girl, "Lust", 0) + 15)
        # Resume BJ immediately (exhaustion still checked by BJ_ActionMenu on return)
        $ store.bj_speed = store._bj_prev_speed
        $ store.bj_action = store._bj_prev_action
        call BJ_ApplySpeed(girl, store.bj_speed) from _call_BJ_ApplySpeed_cs_resume
        return

    # ── hate_cum + forced: spit, angry for 1 day, abort scene ──
    if girl.has_trait("hate_cum") and forced:
        # Show briefly with random eyes + tongue
        $ set_scene_expression(girl, None, eyes=_mcr_show_eyes, mouth="mouth_tongue")
        "She spits it out in disgust."
        $ _remove_cum_tag(girl, "mouth")
        # Angry face
        $ store._witness_expression_lock = True
        $ set_scene_expression(girl, "angry", brows="brows_maniac")
        $ Say_Line(girl, _("I told you to warn me!"))
        $ Change_Status(girl, "Love", -30)
        $ Change_Status(girl, "Obed", -10)

        if getattr(store, "_scene_restricted", False):
            $ store._witness_expression_lock = False
            $ store._scene_angry_abort = True
            $ store._player_exhausted = True
            return

        python:
            _in_her_room = (store.CurrentLocation == GIRL_ROOMS.get(girl.gid, ""))
        if _in_her_room:
            "She pushes you out and locks the door behind you."
        else:
            "She gets angry and storms off."
        $ store._witness_expression_lock = False
        if getattr(girl, '_ntr_violation_pending', False):
            call _angry_end_ntr_confrontation(girl) from _call_aend_ntr_bj_hate
        $ force_scene_reset(girl, angry_days=1, reason="forced_cum_mouth")
        jump main_loop

    # ── hate_cum + accepted: spit with disgust but no anger (she agreed) ──
    if girl.has_trait("hate_cum") and not forced:
        $ set_scene_expression(girl, None, eyes=_mcr_show_eyes, mouth="mouth_tongue")
        $ renpy.pause(0.4)
        "She immediately spits it out."
        $ _remove_cum_tag(girl, "mouth")
        $ set_scene_expression(girl, "disgusted")
        python:
            _hc_spit_lines = [
                _("Ugh... I knew I'd hate it. At least you warned me."),
                _("That was disgusting... but I let you, so..."),
                _("Never again... At least that's what I keep telling myself."),
            ]
        $ Say_Line(girl, _tl(renpy.random.choice(_hc_spit_lines)))
        $ Change_Status(girl, "Obed", 10)

        $ _hc_had_condom = _girl_thinks_condom_on()
        $ debug_log("[DEBUG] hc_spit post-cum: _hc_had_condom=%s" % _hc_had_condom)
        if _hc_had_condom:
            call _post_cum_condom_menu(girl) from _call_pcc_bj_hc
            if store._pcc_choice in ("condom", "raw"):
                $ store.bj_speed = store._bj_prev_speed
                $ store.bj_action = store._bj_prev_action
                call BJ_ApplySpeed(girl, store.bj_speed) from _call_BJ_ApplySpeed_pcc_hc_resume
            else:
                $ Say_Line(girl, _("Good. I need a break from... that."))
                $ store._hate_cum_scene_aborted = True
        else:
            if store._player_exhausted:
                $ store._hate_cum_scene_aborted = True
            else:
                menu:
                    "Keep going":
                        $ store.bj_speed = store._bj_prev_speed
                        $ store.bj_action = store._bj_prev_action
                        call BJ_ApplySpeed(girl, store.bj_speed) from _call_BJ_ApplySpeed_hc_spit_resume
                    "Stop now":
                        $ Say_Line(girl, _("Good. I need a break from... that."))
                        $ store._hate_cum_scene_aborted = True
        return

    # ── Forced (player came without permission): spit, angry, abort scene ──
    if forced:
        # Show briefly with random eyes + tongue
        $ set_scene_expression(girl, None, eyes=_mcr_show_eyes, mouth="mouth_tongue")
        "She spits it out, furious."
        $ _remove_cum_tag(girl, "mouth")
        # Angry face
        $ store._witness_expression_lock = True
        $ set_scene_expression(girl, "angry", brows="brows_maniac")
        $ Say_Line(girl, _("I told you to warn me!"))
        $ Change_Status(girl, "Love", -15)

        if getattr(store, "_scene_restricted", False):
            $ store._witness_expression_lock = False
            $ store._scene_angry_abort = True
            $ store._player_exhausted = True
            return

        python:
            _in_her_room = (store.CurrentLocation == GIRL_ROOMS.get(girl.gid, ""))
        if _in_her_room:
            "She pushes you out and locks the door behind you."
        else:
            "She gets angry and storms off."
        $ store._witness_expression_lock = False
        if getattr(girl, '_ntr_violation_pending', False):
            call _angry_end_ntr_confrontation(girl) from _call_aend_ntr_bj_forced
        $ force_scene_reset(girl, angry_days=1, reason="forced_cum_mouth")
        jump main_loop

    # ── Normal: show mouth cum with random eyes + tongue, then player chooses ──
    $ set_scene_expression(girl, None, eyes=_mcr_show_eyes, mouth="mouth_tongue")

    # Capture ATM context and reset flag
    python:
        _is_atm_swallow = getattr(store, "_atm_cum_in_mouth", False)
        store._atm_cum_in_mouth = False
        store._atm_tease_played = False

    menu:
        "Tell her to swallow":
            if _is_atm_swallow:
                # ATM swallow: harder check (T=850 vs 600)
                $ _swallow_check = ApprovalCheck(girl=girl, T=850, Type="OI", Spread=140, Variation=30, ReturnData=True)
                if _swallow_check["accepted"]:
                    python:
                        if girl.has_trait("hardcore_sex"):
                            _atm_sw_pool = [
                                _("It was in my ass and you want me to swallow? ...Fuck. That's disgusting. ...I'll do it."),
                                _("From my ass, and now down my throat? ...Fine. Watch me."),
                                _("That was just in my ass... God, you're filthy. ...Okay. I'm swallowing it."),
                            ]
                        elif girl.has_trait("cute_sex"):
                            _atm_sw_pool = [
                                _("S-swallow it...? But it was... in my butt... I... o-okay..."),
                                _("You want me to swallow...? After it was in my... oh god... f-fine..."),
                                _("It was in my b-butt and you want me to... I can't believe I'm doing this..."),
                            ]
                        else:
                            _atm_sw_pool = [
                                _("Swallow after it was in my ass? ...I can't believe I'm saying okay."),
                                _("Swallow it...? It was in my ass. ...God. Fine. I'll do it."),
                                _("It was in my ass and now you want me to... ugh. Okay. Don't make this a habit."),
                            ]
                    $ Say_Line(girl, atm_cross_override(girl, "swallow_ok", _tl(renpy.random.choice(_atm_sw_pool))))
                    # Swallow: closed happy + lipbite
                    $ set_scene_expression(girl, "closed_happy")
                    if _gsc(girl.gid, 'has_head_normal', False, pose='blowjob'):
                        python:
                            _ht = bj_get_head_transform(0)
                            _pov = _gsc(girl.gid, 'pov_overlay', False, pose='blowjob')
                            renpy.show("%s blowjob_head head_normal" % girl.gid, tag="%s_bj_head" % girl.gid, at_list=[_ht], zorder=10058 if _pov else 10015)
                    $ _remove_cum_tag(girl, "mouth")
                    $ renpy.pause(0.6)
                    # Post-swallow: smile
                    $ set_scene_expression(girl, None, eyes="eyes_normal", mouth="mouth_smile")
                    $ Change_Status(girl, "Obed", 20)
                    $ Change_Status(girl, "Inbt", 20)
                    call _post_atm_swallow_reaction(girl) from _call_post_atm_sw_tell
                else:
                    python:
                        if girl.has_trait("cute_sex"):
                            _atm_deny_pool = [
                                _("No! It was in my butt! I'm not swallowing that!"),
                                _("I can't... it was just in my... no way! That's too much!"),
                                _("Swallow THAT? After where it's been? N-no!"),
                            ]
                        elif girl.has_trait("hardcore_sex"):
                            _atm_deny_pool = [
                                _("Even I have limits. It was in my ass. I'm not swallowing that."),
                                _("Okay, that's too far. From my ass to my stomach? No."),
                                _("I'll do a lot of things, but swallowing after it was in my ass? No way."),
                            ]
                        else:
                            _atm_deny_pool = [
                                _("Swallow it? After it was in my ass? Absolutely not."),
                                _("It was literally in my ass. I'm not swallowing that."),
                                _("I agreed to the blowjob, not to swallowing after it was in my ass."),
                            ]
                    $ Say_Line(girl, atm_cross_override(girl, "swallow_no", _tl(renpy.random.choice(_atm_deny_pool))))
                    "She turns away and spits it out."
                    $ _remove_cum_tag(girl, "mouth")
                    $ set_scene_expression(girl, None, mouth="mouth_sad")
                    $ Change_Status(girl, "Love", -10)
            else:
                # Normal swallow check
                $ _swallow_check = ApprovalCheck(girl=girl, T=600, Type="OI", Spread=140, Variation=30, ReturnData=True)
                if _swallow_check["accepted"]:
                    if not girl.has_trait("femdom"):
                        $ Say_Line(girl, _("...fine."))
                    # Swallow: closed happy + lipbite
                    $ set_scene_expression(girl, "closed_happy")
                    if _gsc(girl.gid, 'has_head_normal', False, pose='blowjob'):
                        python:
                            _ht = bj_get_head_transform(0)
                            _pov = _gsc(girl.gid, 'pov_overlay', False, pose='blowjob')
                            renpy.show("%s blowjob_head head_normal" % girl.gid, tag="%s_bj_head" % girl.gid, at_list=[_ht], zorder=10058 if _pov else 10015)
                    $ _remove_cum_tag(girl, "mouth")
                    $ renpy.pause(0.6)
                    # Post-swallow: smile
                    $ set_scene_expression(girl, None, eyes="eyes_normal", mouth="mouth_smile")
                    if girl.has_trait("femdom"):
                        $ set_scene_expression(girl, "smug")
                        $ Say_Line(girl, _("I swallowed because I wanted to, not because you told me."))
                        $ Say_Line(girl, _("Your cum is all mine, you understand? You'll cum in my mouth whenever I want."))
                    $ Change_Status(girl, "Obed", 15)
                    $ Change_Status(girl, "Inbt", 15)
                else:
                    $ Say_Line(girl, _("No way."))
                    "She turns away and spits it out."
                    $ _remove_cum_tag(girl, "mouth")
                    $ set_scene_expression(girl, None, mouth="mouth_sad")
                    $ Change_Status(girl, "Love", -10)

        "Say nothing":
            python:
                _sn_obed = getattr(girl, "Obed", 0)
                _sn_inbt = getattr(girl, "Inbt", 0)
            if _is_atm_swallow:
                # ATM: much harder to swallow on her own
                if _sn_obed >= 600 or _sn_inbt >= 700:
                    $ set_scene_expression(girl, "closed_happy")
                    if _gsc(girl.gid, 'has_head_normal', False, pose='blowjob'):
                        python:
                            _ht = bj_get_head_transform(0)
                            _pov = _gsc(girl.gid, 'pov_overlay', False, pose='blowjob')
                            renpy.show("%s blowjob_head head_normal" % girl.gid, tag="%s_bj_head" % girl.gid, at_list=[_ht], zorder=10058 if _pov else 10015)
                    $ _remove_cum_tag(girl, "mouth")
                    $ renpy.pause(0.6)
                    $ set_scene_expression(girl, None, eyes="eyes_normal", mouth="mouth_smile")
                    "She hesitates... looks at you... and swallows."
                    $ Change_Status(girl, "Obed", 15)
                    call _post_atm_swallow_reaction(girl) from _call_post_atm_sw_silent
                else:
                    "She immediately spits it out."
                    $ _remove_cum_tag(girl, "mouth")
                    $ set_scene_expression(girl, None, mouth="mouth_sad")
            elif _sn_obed >= 300 or _sn_inbt >= 400:
                # Swallow: closed happy + lipbite
                $ set_scene_expression(girl, "closed_happy")
                if _gsc(girl.gid, 'has_head_normal', False, pose='blowjob'):
                    python:
                        _ht = bj_get_head_transform(0)
                        _pov = _gsc(girl.gid, 'pov_overlay', False, pose='blowjob')
                        renpy.show("%s blowjob_head head_normal" % girl.gid, tag="%s_bj_head" % girl.gid, at_list=[_ht], zorder=10058 if _pov else 10015)
                $ _remove_cum_tag(girl, "mouth")
                $ renpy.pause(0.6)
                $ set_scene_expression(girl, None, eyes="eyes_normal", mouth="mouth_smile")
                "She looks at you for a moment, then swallows."
                $ Change_Status(girl, "Obed", 10)
            else:
                "She turns away and spits it out."
                $ _remove_cum_tag(girl, "mouth")
                $ set_scene_expression(girl, None, mouth="mouth_sad")

    # After swallow/spit: condom/raw menu if she thinks condom is on, else simple keep/stop
    # skip_post_menu=True when called from _cum_in_mouth_via_bj — centralized handler decides
    if not skip_post_menu:
        $ _mcr_had_condom = _girl_thinks_condom_on()
        $ debug_log("[DEBUG] mouth_cum_reaction post-cum: _mcr_had_condom=%s (condom_active=%s stealth=%s)" % (_mcr_had_condom, store.condom_active, store._stealth_condom_removed))
        if store._player_exhausted:
            pass
        elif _mcr_had_condom:
            call _post_cum_condom_menu(girl) from _call_pcc_bj_mcr
            if store._pcc_choice in ("condom", "raw"):
                $ store._bj_mouth_cum_continued = True
                $ store.bj_speed = store._bj_prev_speed
                $ store.bj_action = store._bj_prev_action
                call BJ_ApplySpeed(girl, store.bj_speed) from _call_BJ_ApplySpeed_pcc_mcr_resume
            else:
                $ debug_log("[DEBUG] mouth_cum_reaction: player chose STOP")
                $ Say_Line(girl, _("Alright..."))
                $ store._hate_cum_scene_aborted = True
        else:
            menu:
                "Keep going":
                    $ store._bj_mouth_cum_continued = True
                    $ store.bj_speed = store._bj_prev_speed
                    $ store.bj_action = store._bj_prev_action
                    call BJ_ApplySpeed(girl, store.bj_speed) from _call_BJ_ApplySpeed_mcr_resume

                "Stop now":
                    $ debug_log("[DEBUG] mouth_cum_reaction: player chose ASK HER TO STOP")
                    $ Say_Line(girl, _("Alright..."))
                    $ store._hate_cum_scene_aborted = True
                    $ debug_log("[DEBUG] _hate_cum_scene_aborted set to True")

    $ debug_log("[DEBUG] _bj_mouth_cum_reaction returning, aborted=%s continued=%s" % (store._hate_cum_scene_aborted, store._bj_mouth_cum_continued))
    return

# ------------------------------------------------------------
# Post-cum condom decision (centralized)
# Used after any finish with a condom on (in her eyes, or the one he pulled off to cum outside: _post_cum_had_condom).
# Sets store._pcc_choice ("condom"/"raw"/"stop") and
# store._pcc_raw_allowed (bool) for caller narration.
# Caller handles position-specific speed resume after return.
# ------------------------------------------------------------
label _post_cum_condom_menu(girl):
    $ _has_condoms = (Player.get_item_count("condom") + Player.get_item_count("japanese_condom")) > 0
    $ debug_log("[PCC_MENU] entered: has_condoms=%s (reg=%d jp=%d), stealth=%s, condom_active=%s" % (_has_condoms, Player.get_item_count("condom"), Player.get_item_count("japanese_condom"), store._stealth_condom_removed, store.condom_active))
    $ _raw_check = CumPermissionCheck(girl, "cum_remove_condom_ask")
    # Approval alone is not enough: the cheat path before her breaking point and her partner's condom rule
    # (NTR level 2) keep the condom on here too, as they do everywhere else it could come off. Her story step too:
    # "cum_remove_condom_ask" is the act "raw" (story_steps.rpy), so CumPermissionCheck refuses it below step 4
    $ _pcc_rule_keeps_condom = (not _cheat_lets_condom_go(girl)) or _ntr_condom_rule_holds(girl)
    $ _would_allow_raw = _raw_check["accepted"] and not _pcc_rule_keeps_condom
    $ store._pcc_raw_allowed = _would_allow_raw
    $ debug_log("[PCC_MENU] raw: approval=%s rule_keeps_condom=%s -> she says yes=%s" % (_raw_check["accepted"], _pcc_rule_keeps_condom, _would_allow_raw))

    if _would_allow_raw:
        $ Say_Line(girl, _tl(renpy.random.choice(_POST_CUM_RAW_SUGGEST)))

label ._pcc_choose:
    # the three answers are always on the menu: "Ask to go raw" gets her yes or her no (never a hidden button)
    menu:
        "Grab another condom" if _has_condoms:
            # Same as the first one: pick the type if you carry both, use up THAT one, roll ITS break chance
            call _apply_condom(girl) from _call_apply_condom_pcc
            $ store._pcc_choice = "condom"
            if _would_allow_raw:
                $ Change_Status(girl, "Love", -3)

        "!disabled!Grab another condom - You don't have one" if not _has_condoms:
            pass

        "Ask to go raw":
            if not _would_allow_raw:
                # her no, in the voice of what holds her: her story step, her partner's rule, else her own
                if story_act_locked(girl, "raw"):
                    $ set_scene_expression(girl, "angry")
                    $ Say_Line(girl, story_locked_line(girl, "raw"))
                elif _ntr_condom_rule_holds(girl):
                    $ _ntr_say_boundary_line(girl, _NTR_GIRL_DENY_RAW)
                else:
                    $ Say_Line(girl, _condom_deny_line(girl))
                $ debug_log("[PCC_MENU] ask to go raw: she says no")
                jump ._pcc_choose
            $ Say_Line(girl, _tl(renpy.random.choice(_POST_CUM_RAW_ACCEPT)))
            # The rest of this scene is raw: count it like any mid-scene removal (raw_sex_count, her first raw,
            # the cheat "sex_raw" afterscene), the condom used up or pulled off for his finish outside alike. A stealth
            # removal already counted it in _on_condom_removed.
            if not getattr(store, "_stealth_condom_removed", False):
                $ _track_raw_sex_start(girl)
            $ store._condom_removed_midscene = True
            $ stealth_condom_reset()
            $ store.condom_active = False
            $ store._creampie_consent = "allowed"
            $ Change_Status(girl, "Obed", 3)
            $ Change_Status(girl, "Inbt", 2)
            $ store._pcc_choice = "raw"

        "Stop now":
            $ stealth_condom_reset()
            if _would_allow_raw:
                $ Change_Status(girl, "Love", -3)
            $ store._pcc_choice = "stop"

    $ print("[SCENE_FLOW] condom menu: he chose %s (condoms left before=%s, her yes to raw=%s)" % (store._pcc_choice, _has_condoms, _would_allow_raw))
    return

# ------------------------------------------------------------
# DEPRECATED: replaced by _post_cum_central (v0.10.4)
# Kept for safety; no callers after refactor.
# ------------------------------------------------------------
label _post_cum_resume(girl, scene_type, had_condom):
    if had_condom and not store._player_exhausted:
        call _post_cum_condom_menu(girl) from _call_pcc_pcr
        if store._pcc_choice in ("condom", "raw"):
            $ _pcr_reset_speed(scene_type)
            call _pcr_apply_speed(girl, scene_type) from _call_pcr_as_1
            if store._pcc_choice == "condom":
                if store._pcc_raw_allowed:
                    "You put on a fresh condom. She looks a little disappointed."
                else:
                    "You put on a fresh condom and continue."
        else:
            $ store._player_exhausted = True

    elif not store._player_exhausted:
        menu:
            "Keep going":
                $ _pcr_reset_speed(scene_type)
                call _pcr_apply_speed(girl, scene_type) from _call_pcr_as_2
            "Stop":
                $ store._player_exhausted = True
    return

label _pcr_apply_speed(girl, scene_type):
    call _cum_dispatch_apply_speed(girl, scene_type, speed=1) from _call_pcr_as_delegate
    return

# ============================================================
# CENTRALIZED POST-CUM HANDLER
# Called from start_scene after the End label transitions to standing.
# Replaces the inconsistent per-position PlayerExhausted + inline menu pattern.
# All reactions and keep-going decisions happen in standing pose.
# ============================================================
label _post_cum_central(girl, scene_type):
    $ store._post_cum_pending = False
    $ print("[POST_CUM_CENTRAL] scene_type=%s exhausted=%s girl_orgasms=%s had_condom=%s sub_mode=%s restricted=%s continues=%s" % (scene_type, store._player_exhausted, store._session_girl_orgasms, store._post_cum_had_condom, store._post_cum_sub_mode, getattr(store, "_scene_restricted", False), getattr(store, "_scene_cum_continues", False)))

    # Femdom: what she thinks of the orders he just kept / broke (femdom_note_cum), before anything else
    $ femdom_play_verdicts(girl, scene_type)

    if scene_ends_on_cum():
        $ store._post_cum_result = "stop"
        $ print("[SCENE_FLOW] post-cum -> STOP: this scene ends on his cum (restricted, no cum_continues) | %s" % scene_flow_state())
        return

    # Pre-filled choice from _cum_in_mouth_via_bj (menu was shown in BJ pose)
    if getattr(store, "_via_bj_post_cum_choice", None):
        $ store._post_cum_result = store._via_bj_post_cum_choice
        $ store._via_bj_post_cum_choice = None
        $ Player.set_focus(0)
        $ print("[POST_CUM_CENTRAL] via_bj pre-filled: %s" % store._post_cum_result)
        $ print("[SCENE_FLOW] post-cum -> %s: chosen on the menu after the mouth finish (BJ pose) | %s" % (store._post_cum_result.upper(), scene_flow_state()))
        return

    $ Player.set_focus(0)

    if store._forced_creampie_end_after_orgasm:
        if store._player_exhausted:
            $ store._forced_creampie_end_after_orgasm = False
            call _player_didnt_finish_after_forced_creampie(girl, scene_type) from _call_pcc_forced_cream
            $ store._post_cum_result = "stop"
            $ print("[SCENE_FLOW] post-cum -> STOP: forced creampie and he is exhausted | %s" % scene_flow_state())
            return
        $ store._post_cum_result = "continue"
        $ print("[POST_CUM_CENTRAL] forced_creampie: player has energy, auto-continue (flag stays for GirlCumming)")
        $ print("[SCENE_FLOW] post-cum -> CONTINUE: forced creampie, he has energy | %s" % scene_flow_state())
        return

    python:
        _girl_came = store._session_girl_orgasms > 0
        _has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        _ex_is_cheater = hasattr(girl, "has_trait") and girl.has_trait("cheater")

        _exhaust_narr = [
            _("Your body gives out. You can't keep going."),
            _("You feel completely drained. There's nothing left."),
            _("Your legs feel like lead. You're done."),
        ]

        _girl_satisfied = {
            "hardcore_sex": [
                _("That's it? Hmph. At least I got mine."),
                _("You're done already? Well, I can't complain... I got what I needed."),
                _("Tch. Could've gone longer. But at least you made me finish first."),
            ],
            "cute_sex": [
                _("Hey... it's okay. You made me feel amazing. Rest now."),
                _("Don't worry about it. I'm happy. You were wonderful."),
                _("That was perfect. You don't need to push yourself for me."),
            ],
            "cum_slut": [
                _("Aww, already? I wanted more... but at least I came."),
                _("Done already? Hmm... well, you did make me cum, so I'll forgive you."),
                _("I wanted to keep going... but fine. You earned your rest."),
            ],
            "hate_cum": [
                _("Good. We're done then. At least it wasn't a waste."),
                _("Fine by me. I'm satisfied anyway."),
                _("That's enough then. It was... fine."),
            ],
            "_bf": [
                _("I can't believe I just did that... but at least it felt good."),
                _("My %(pl)s would be devastated if %(pp)s knew... but you did make me feel things %(pp)s doesn't."),
                _("This was a mistake... a really good mistake. But still a mistake."),
            ],
            "_default": [
                _("It's okay. I'm satisfied. You did good."),
                _("Don't worry about it. I had fun."),
                _("That was great. Rest up, okay?"),
            ],
        }

        _girl_unsatisfied = {
            "hardcore_sex": [
                _("Are you serious?! That's it? You didn't even make me cum!"),
                _("Wow. I can't believe this. All that and I didn't even finish."),
                _("Pathetic. You couldn't even get me off?"),
                _("Don't tell me you're done. I didn't even get CLOSE."),
            ],
            "cute_sex": [
                _("Oh... you're done? I... it's okay, I guess. These things happen."),
                _("I was hoping to finish too, but... it's fine. Don't worry about it."),
                _("It's alright. Maybe next time you can last a little longer?"),
                _("I'm not upset... just a little disappointed. But it's okay, really."),
            ],
            "cum_slut": [
                _("Wait, WHAT? You're done?! But I didn't even get to cum!"),
                _("Are you kidding me?! I was SO close! This is so unfair!"),
                _("Noooo! I needed more! You can't just leave me like this!"),
            ],
            "hate_cum": [
                _("So you finished and I didn't? Typical."),
                _("Of course. You got what you wanted and I got nothing."),
                _("Great. You're done and I'm left unsatisfied. Fantastic."),
            ],
            "_bf": [
                _("I cheated on my %(pl)s for THIS? You didn't even make me cum!"),
                _("I can't believe I fell for this... and I didn't even get to finish."),
                _("I risked everything for nothing. Not even an orgasm."),
                _("My %(pl)s would've at least tried to make me finish..."),
            ],
            "_bf_cheater": [
                _("Seriously? I left my %(pl)s hanging for this?"),
                _("Well that was a waste. At least my %(pl)s makes me cum."),
                _("I snuck around for nothing. You didn't even finish the job."),
            ],
            "_default": [
                _("Wait... you're done? But I didn't..."),
                _("Oh. That's it? I was hoping to finish too..."),
                _("I'm a little disappointed, honestly. I didn't get to cum."),
                _("You're stopping? But I wasn't done..."),
            ],
        }

        if _girl_came:
            _pool = _girl_satisfied
        else:
            _pool = _girl_unsatisfied

        _picked_line = None
        _ex_bf_f = None
        if _has_bf:
            _ex_bf_f = partner_fmt(girl)
        if _has_bf and not _ex_is_cheater and not _girl_came:
            _picked_line = _tl(renpy.random.choice(_pool["_bf"])) % _ex_bf_f
        elif _has_bf and _ex_is_cheater and not _girl_came:
            _picked_line = _tl(renpy.random.choice(_pool["_bf_cheater"])) % _ex_bf_f
        elif _has_bf and not _ex_is_cheater and _girl_came:
            _picked_line = _tl(renpy.random.choice(_pool["_bf"])) % _ex_bf_f
        if _picked_line is None:
            for _t in ("hardcore_sex", "cute_sex", "cum_slut", "hate_cum"):
                if girl.has_trait(_t):
                    _picked_line = renpy.random.choice(_pool[_t])
                    break
        if _picked_line is None:
            _picked_line = renpy.random.choice(_pool["_default"])

    if store._player_exhausted:
        "[_tl(renpy.random.choice(_exhaust_narr))]"
        $ Say_Line(girl, _picked_line)
        if not _girl_came:
            $ Change_Status(girl, "Obed", -10)
            $ Change_Status(girl, "Love", -5)
            if girl.has_trait("hardcore_sex"):
                "She looks genuinely angry. You can tell this won't be easily forgiven."
            elif girl.has_trait("cute_sex"):
                "She hides it well, but you can see the disappointment in her eyes."
            elif _has_bf and not _ex_is_cheater:
                "The regret is written all over her face."
            else:
                "She clearly expected more from you."
        else:
            "At least she seems satisfied."
        # gym tip only while training can still raise it (5 = cap): at 5/5 it just nags
        if Player.energy_max < 5:
            "You need to build your stamina if you want to last longer. {b}Working out at the gym{/b} will raise your max energy over time."
            "Your current max energy: {b}[Player.energy_max]/5{/b}. Train consistently to push your limits."
        $ store._post_cum_result = "stop"
        $ print("[POST_CUM_CENTRAL] exhausted -> stop")
        $ print("[SCENE_FLOW] post-cum -> STOP: he is exhausted (energy 0, or a flag set before this) | %s" % scene_flow_state())
        return

    # a condom on for this finish (_post_cum_had_condom: the one he pulled off to cum outside included): a fresh one / ask
    # to go raw / stop. Her step locking raw asks the same whatever happened (never a bare "Keep going"),
    # but ONLY in a scene that can go back in bare (_scene_is_penetrative: no condom talk after a handjob)
    if store._post_cum_sub_mode == "sex" and (store._post_cum_had_condom or (story_act_locked(girl, "raw") and _scene_is_penetrative(store._post_cum_scene_type))):
        call _post_cum_condom_menu(girl) from _call_pcc_condom
        if store._pcc_choice == "stop":
            $ store._post_cum_result = "stop"
        else:
            $ store._post_cum_result = store._pcc_choice
    else:
        menu:
            "Keep going":
                $ store._post_cum_result = "continue"
            "Stop":
                $ store._post_cum_result = "stop"
        if store._post_cum_result == "stop":
            # she is still on the edge: a submissive pleads, a femdom demands (edge_denial.rpy)
            call _post_cum_stop_plea(girl, store._post_cum_scene_type) from _call_post_cum_stop_plea

    if store._post_cum_result == "raw":
        $ store.condom_active = False
    elif store._post_cum_result == "condom":
        $ store.condom_active = True

    $ print("[POST_CUM_CENTRAL] result=%s" % store._post_cum_result)
    $ print("[SCENE_FLOW] post-cum -> %s: his choice on the post-cum menu (%s) | %s" % (
        store._post_cum_result.upper(),
        "condom menu" if (store._post_cum_sub_mode == "sex" and (store._post_cum_had_condom or (story_act_locked(girl, "raw") and _scene_is_penetrative(store._post_cum_scene_type)))) else "keep going / stop",
        scene_flow_state()))
    return

# ------------------------------------------------------------
# Post-ATM swallow reactions + camera acknowledge
# Called after any ATM swallow (tell, force, say nothing)
# ------------------------------------------------------------
label _post_atm_swallow_reaction(girl):
    python:
        _has_al = girl.has_trait("anal_lover")
        _has_ah = girl.has_trait("anal_hater")
        _has_cs = girl.has_trait("cum_slut")
        _has_hc_cum = girl.has_trait("hate_cum")
        _has_hc = girl.has_trait("hardcore_sex")
        _has_sub = girl.has_trait("submissive")
        _has_cute = girl.has_trait("cute_sex")
        # still discovering it (trait_is_new): she can't believe she liked it, no "addicted" / "anything you give me" yet
        _cs_disc = _has_cs and trait_is_new(girl, "cum_slut")
        _al_disc = _has_al and trait_is_new(girl, "anal_lover")

        _atm_react = None

        # Recursion: 2nd+ ATM swallow this session, her trait's own voice (Dialogs/atm_repeat_lines.rpy)
        _atm_sc = store._atm_session_count
        if _atm_sc >= 2:
            _atm_react = atm_repeat_line(girl, "post", _atm_sc)

        elif _has_al and _has_cs and (_cs_disc or _al_disc):
            _atm_react = renpy.random.choice([
                _("I just... swallowed it. After it was in my ass. And I liked it? What is happening to me?"),
                _("That should have been gross... why wasn't it gross?"),
                _("I can taste where it's been... and I don't want to stop. That scares me a little."),
            ])
        elif _has_al and _has_cs:
            _atm_react = renpy.random.choice([
                _("I can taste my own ass on it... and I want more."),
                _("That flavor... straight from my ass. God, I'm addicted."),
                _("Ass to mouth and I swallowed every drop. I'm disgusting and I love it."),
            ])
        elif _has_al and _has_hc_cum:
            _atm_react = renpy.random.choice([
                _("I hate the taste of cum... but knowing where it's been makes it weirdly exciting."),
                _("Disgusting... but the fact it was in my ass first... I don't know how to feel."),
            ])
        elif _has_ah and _has_cs and _cs_disc:
            _atm_react = renpy.random.choice([
                _("Swallowing was... more than okay, actually. But tasting my own ass? That's a lot."),
                _("The cum part... I didn't expect to like that. The ass part... I'll need a minute."),
            ])
        elif _has_ah and _has_cs:
            _atm_react = renpy.random.choice([
                _("I love swallowing... but tasting my own ass? That's a lot."),
                _("The cum part was fine. The ass part... I'll need a minute."),
            ])
        elif _has_ah and _has_hc_cum and _has_sub:
            _atm_react = renpy.random.choice([
                _("Every part of that was awful. And you knew I'd do it anyway, didn't you?"),
                _("Revolting. The cum, the taste of my ass, all of it... and I swallowed without being told."),
                _("I hate cum. I hate my ass on your cock. And I still swallowed it all, because you wanted me to."),
            ])
        elif _has_ah and _has_hc_cum and _has_hc:
            _atm_react = renpy.random.choice([
                _("I hate cum. I hate anal. And somehow I'm on my knees swallowing both. ...What is wrong with me?"),
                _("Everything about that was vile... and the worst part is you made me feel something doing it."),
                _("I hate cum. I hate the taste of my ass. You made me take both... and I let you."),
            ])
        elif _has_ah and _has_hc_cum:
            _atm_react = renpy.random.choice([
                _("I hate cum. I hate anal. And you made me combine both. I have no words."),
                _("That was the worst thing I've ever tasted. I hate everything about this."),
            ])
        elif _has_sub and _has_ah:
            _atm_react = renpy.random.choice([
                _("I hated every second of that... and I'd do it again if you told me to. What's wrong with me?"),
                _("My ass on your cock, in my mouth. I despise it. Tell me to do it again."),
                _("That was in my ass and I still swallowed it for you. I'll do whatever you tell me, won't I?"),
            ])
        elif _has_hc and _has_ah:
            _atm_react = renpy.random.choice([
                _("That was disgusting. I hated it. And the fact you made me... god."),
                _("I hate anything back there... but you fucked my ass and then my throat that hard? My whole body is still shaking."),
                _("Disgusting. Vile. And so fucking rough I can't even stay mad about it."),
            ])
        elif _has_sub and _has_hc_cum:
            _atm_react = renpy.random.choice([
                _("I hate cum... and you made me swallow it because you told me to. That's all it takes."),
                _("Disgusting. But you wanted it, so I did it. That's how this works."),
                _("I hate the taste. I swallowed anyway. You say it, I do it... that's just how it is with you."),
            ])
        elif _has_hc and _has_hc_cum:
            _atm_react = renpy.random.choice([
                _("I hate cum, you know that. But you went so fast and deep I barely tasted it. ...Almost worth it."),
                _("Disgusting. I hate the taste. But the way you pounded my ass first? That part I'd take again."),
            ])
        elif _has_cs and _cs_disc:
            _atm_react = renpy.random.choice([
                _("I swallowed it... even after it was in my ass. Who am I right now?"),
                _("Mmm... that was so dirty. And I didn't even hesitate."),
            ])
        elif _has_cs:
            _atm_react = renpy.random.choice([
                _("I'll swallow anything you give me... even after it's been in my ass."),
                _("Mmm... it tastes different after being inside me back there."),
            ])
        elif _has_hc_cum:
            _atm_react = renpy.random.choice([
                _("I already hate cum... and this tastes even worse than normal."),
                _("You made me swallow cum that was in my ass. I feel sick."),
            ])
        elif _has_hc:
            _atm_react = renpy.random.choice([
                _("Filthy. My own ass. I swallowed it. ...Do it again."),
                _("That tasted exactly like you'd expect. And I didn't flinch."),
                _("Ass to mouth. Swallowed. What else do you want from me?"),
            ])
        elif _has_cute:
            _atm_react = renpy.random.choice([
                _("I can't believe you made me do that... how could you?"),
                _("I feel so used right now... that was horrible..."),
                _("Why would you do that to me? I can still taste it... I feel sick..."),
            ])
        elif _has_al:
            _atm_react = renpy.random.choice([
                _("Tasting my own ass on it is... strangely intimate."),
                _("I could taste where it's been. And honestly? I didn't hate it."),
            ])
        else:
            _atm_react = renpy.random.choice([
                _("I can't believe I just did that... it was in my ass..."),
                _("The taste... I know exactly where that was. God."),
                _("I just swallowed cum that was in my ass. Let that sink in."),
            ])

        if _atm_sc < 2:   # first ATM swallow of the session; the 2nd+ "getting used to it" lines stay as they are
            _atm_react = atm_cross_override(girl, "after_swallow", _atm_react)   # threesome: it was in the OTHER girl's ass
        if _atm_react:
            Say_Line(girl, _atm_react)

    # Camera acknowledge — she notices after swallowing
    if getattr(store, "_recording_active", False):
        python:
            _cam_react = None
            if girl.has_trait("camera_lover"):
                _cam_react = renpy.random.choice([
                    _("Wait... you filmed all of that?! ...Good. I want to watch it later."),
                    _("Is that camera still on? Tell me you got that on video."),
                    _("You recorded me swallowing after ass to mouth? ...Play it back for me later."),
                ])
            elif girl.has_trait("camera_hater"):
                _cam_react = renpy.random.choice([
                    _("Is that... a CAMERA?! You recorded me doing THAT?! DELETE IT!"),
                    _("You filmed me?! Swallowing THAT?! I swear to god, delete it NOW!"),
                    _("YOU RECORDED THIS?! After what I just did?! Give me that phone!"),
                ])
            else:
                _cam_react = renpy.random.choice([
                    _("Wait... was that recording this whole time? Oh my god..."),
                    _("You... you filmed me doing that? With your phone? ...Oh no."),
                    _("Tell me you didn't just record me swallowing after... oh god."),
                ])
            if _cam_react:
                Say_Line(girl, _cam_react)

            if girl.has_trait("camera_hater"):
                Change_Status(girl, "Love", -20)
                Change_Status(girl, "Obed", -10)
            elif girl.has_trait("camera_lover"):
                Change_Status(girl, "Inbt", 15)

    # First kiss aftermath (if ATM was before first kiss)
    $ debug_log("[ATM_FK] About to call _post_atm_first_kiss_reaction from _post_atm_swallow_reaction")
    call _post_atm_first_kiss_reaction(girl) from _call_post_atm_fk_react

    return

# ------------------------------------------------------------
# Post-ATM first kiss reaction — "does this count as my first kiss?"
# Called at the end of _post_atm_swallow_reaction
# ------------------------------------------------------------
label _post_atm_first_kiss_reaction(girl):
    python:
        _nk = getattr(store, "_never_kissed_before_atm", False)
        debug_log("[ATM_FK] CHECK _never_kissed_before_atm=%s" % _nk)
        store._never_kissed_before_atm = False
    if not _nk:
        $ debug_log("[ATM_FK] SKIPPING first kiss popup (flag was False)")
        return

    $ unlock_achievement("worst_first_kiss")

    python:
        _has_cute = girl.has_trait("cute_sex")
        _has_hc = girl.has_trait("hardcore_sex")

        if _has_cute:
            _fk_line = renpy.random.choice([
                _("I... I put my mouth on you. That was... my lips touched you there. Before they've touched anyone anywhere. Do you think... does that count? As a kiss? It can't count... right?"),
                _("I did it. For you. Are you happy? I tasted your... stuff. I tasted myself... I had my lips on your cock. My lips were on you... Hey, do you think that counts as my first kiss? It can't, right?"),
            ])
        elif _has_hc:
            _fk_line = renpy.random.choice([
                _("So my first kiss was on your cock. After it was in my ass. ...That's kind of metal, actually. Does it count?"),
                _("My lips have been on your cock before they've been on your mouth. From my ass. ...Does that count as a first kiss or what?"),
            ])
        else:
            _fk_line = renpy.random.choice([
                _("You know... my lips were on you before we've ever kissed. After it was... back there. Do you think that counts?"),
                _("I had your cock in my mouth before I've ever been kissed. Straight from my ass. ...Does that count as my first kiss?"),
            ])
    $ set_scene_expression(girl, "shy")
    $ Say_Line(girl, _fk_line)

    menu:
        "It doesn't count":
            python:
                if _has_cute:
                    _no_pool = [
                        _("That's right. Good. We can still do that. I can still have that. This wasn't wrong. I just know what your cock tastes like. And your cum. And my... I know what my asshole tastes like now. And not your lips. You wanted it like this. You liked it. That's good. You can still kiss me later."),
                        _("Good. That's what I thought. That wasn't a kiss. That was... something else entirely. My first kiss is still out there. Waiting. For something real."),
                    ]
                elif _has_hc:
                    _no_pool = [
                        _("Fair enough. That was just... a warm-up. The real first kiss better be worth it after all that."),
                        _("Good. 'Cause that would've been a really fucked up first kiss. Even for me."),
                    ]
                else:
                    _no_pool = [
                        _("Right. Of course it doesn't count. That was... that was something else. My first real kiss is still ahead of me."),
                        _("Good. I didn't think so either. That wasn't a kiss. That was... I don't even know what that was."),
                    ]
            $ set_scene_expression(girl, "smile")
            $ Say_Line(girl, _tl(renpy.random.choice(_no_pool)))

        "It does count":
            python:
                if _has_cute:
                    _yes_pool = [
                        _("Oh. You're right... of course it counts. This was it. My perfect first kiss... was given to your cock. After it had been in my ass. So you could cum in my mouth. I'll always remember this. I'll always remember this taste. What have I done..."),
                        _("It counts?! That... THAT was my first kiss?! I'll never get that back! You... I can't believe you!"),
                    ]
                elif _has_hc:
                    _yes_pool = [
                        _("Ha! My first kiss was ass to mouth. That's actually kind of badass. Most people don't even get a good story out of theirs."),
                        _("Damn. My first kiss was on a cock fresh out of my ass. That's going to be a hell of a thing to remember forever."),
                    ]
                else:
                    _yes_pool = [
                        _("You think so? My first kiss was... that. On your... after it was in my... I'm going to be thinking about that for a long time."),
                        _("Great. My first kiss. A cock straight from my ass. That's what I'll remember forever. ...Thanks for that."),
                    ]
            if _has_cute:
                $ set_scene_expression(girl, "scared")
            elif _has_hc:
                $ set_scene_expression(girl, "smug")
            else:
                $ set_scene_expression(girl, "uncomfortable")
            $ Say_Line(girl, _tl(renpy.random.choice(_yes_pool)))
            $ mark_intimacy(girl, "kiss", skip_player_first=True)
            $ girl.mark_player_first("kiss")
            $ Change_Status(girl, "Inbt", 15)
            if _has_cute:
                $ Change_Status(girl, "Love", -10)
            $ debug_log("[DEBUG] ATM first kiss: player said it counts, kiss marked")

    return

# ------------------------------------------------------------
# PlayerCumMenu_Penetration... RCG / Cowgirl
# ------------------------------------------------------------
label PlayerCumMenu_Penetration(girl, scene_type):
    $ debug_log("[CUM_ROUTE] PlayerCumMenu_Penetration: scene=%s condom=%s stealth=%s midscene_removed=%s broken_hidden=%s" % (scene_type, store.condom_active, getattr(store, "_stealth_condom_removed", False), getattr(store, "_condom_removed_midscene", False), getattr(store, "_condom_broken_hidden", False)))

    if store.condom_active:
        $ debug_log("[CUM_ROUTE] -> routing to CONDOM menu")
        call PlayerCumMenu_Penetration_Condom(girl, scene_type) from _call_PlayerCumMenu_Penetration_Condom
    else:
        $ debug_log("[CUM_ROUTE] -> routing to RAW menu")
        call PlayerCumMenu_Penetration_Raw(girl, scene_type) from _call_PlayerCumMenu_Penetration_Raw

    return

# ------------------------------------------------------------
# With condom active
# ------------------------------------------------------------
label PlayerCumMenu_Penetration_Condom(girl, scene_type):

    $ debug_log("[CUM_ROUTE] Penetration_Condom: cheat=%s broke=%s broken_hidden=%s midscene_removed=%s cumslut=%s cream=%s" % (_is_on_cheat_path(girl), getattr(girl, "_cheat_broke", False), getattr(store, "_condom_broken_hidden", False), getattr(store, "_condom_removed_midscene", False), girl.has_trait("cum_slut"), getattr(girl, "CreampieCounts", 0)))

    # Track condom sex for cheat path breaking point (any path)
    if _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False):
        $ girl._cheat_condom_sex_count = getattr(girl, "_cheat_condom_sex_count", 0) + 1
        $ debug_log("[CUM_ROUTE] cheat path condom_sex_count=%s" % girl._cheat_condom_sex_count)

    # Hidden broken condom: special cum menu
    if store._condom_broken_hidden:
        $ debug_log("[CUM_ROUTE] -> CondomBreakCumMenu (broken hidden)")
        call CondomBreakCumMenu(girl, scene_type) from _call_CondomBreakCumMenu
        return

    # All cheat paths: condom stays until breaking point. Player chooses where to cum.
    if _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False):
        $ debug_log("[CUM_ROUTE] -> cheat path condom menu")
        menu:
            "Warn her":
                python:
                    _cep = getattr(girl, "_cheat_escalation_path", 0)
                    if _cep == 1:
                        _cum_condom_line = _cheat_line(girl, renpy.random.choice(_PATH1_CONDOM_BLOCK))
                    elif _cep == 2:
                        _cum_condom_line = _cheat_line(girl, renpy.random.choice([
                            _("Don't even THINK about taking it off! I'm still in control!"),
                            _("Condom stays ON! I decide when... and it's NOT now!"),
                            _("Keep it on! I'm not losing control like that!"),
                        ]))
                    else:
                        _cum_condom_line = _cheat_line(girl, renpy.random.choice([
                            _("Condom STAYS! I'm getting revenge, not being stupid!"),
                            _("Keep it on! He doesn't deserve the full betrayal... not yet!"),
                            _("The condom stays! I'm mad, not reckless!"),
                        ]))
                $ Say_Line(girl, _cum_condom_line)
                "You cum inside the condom."
                $ process_cum(girl, scene_type, "condom")
                $ apply_cum_bonuses(girl, "cum_outside")

            "Cum in her mouth":
                $ _cum_check_mouth = CumPermissionCheck(girl, "cum_in_mouth_ask")
                if _cum_check_mouth["accepted"]:
                    $ Say_Line(girl, scene_pick_line("cum_mouth_accepted", scene=scene_type, girl=girl) or _("Go ahead... do it."))
                    call _cum_in_mouth_via_bj(girl, scene_type) from _call__cum_in_mouth_via_bj_cheat_condom
                else:
                    $ Say_Line(girl, scene_pick_line("cum_mouth_denied", scene=scene_type, girl=girl) or _("No way... not in my mouth."))
                    "You finish inside the condom instead."
                    $ process_cum(girl, scene_type, "condom")
                    $ apply_cum_bonuses(girl, "cum_outside")

            "Cum outside":
                call PlayerCumMenu_Outside_Penetration(girl, scene_type) from _call_PlayerCumMenu_Outside_Penetration_cheat_condom

            "Cum in the condom":
                call _cum_dispatch_anim(girl, scene_type) from _call__cum_anim_cheat_condom
                "You finish inside the condom."
                $ process_cum(girl, scene_type, "condom")
                $ apply_cum_bonuses(girl, "cum_outside")
                $ _cum_say_line(girl, "condom", scene_type)

            "Ask to remove":
                python:
                    _cep = getattr(girl, "_cheat_escalation_path", 0)
                    if _cep == 1:
                        _cum_condom_line = _cheat_line(girl, renpy.random.choice(_PATH1_CONDOM_BLOCK))
                    elif _cep == 2:
                        _cum_condom_line = _cheat_line(girl, renpy.random.choice([
                            _("Don't even THINK about taking it off! I'm still in control!"),
                            _("Condom stays ON! I decide when... and it's NOT now!"),
                            _("Keep it on! I'm not losing control like that!"),
                        ]))
                    else:
                        _cum_condom_line = _cheat_line(girl, renpy.random.choice([
                            _("Condom STAYS! I'm getting revenge, not being stupid!"),
                            _("Keep it on! He doesn't deserve the full betrayal... not yet!"),
                            _("The condom stays! I'm mad, not reckless!"),
                        ]))
                $ Say_Line(girl, _cum_condom_line)
                "She won't allow it. You finish inside the condom."
                $ process_cum(girl, scene_type, "condom")
                $ apply_cum_bonuses(girl, "cum_outside")

        call _cheat_condom_corruption(girl) from _call_cheat_condom_corr_p1
        return

    # Restricted scene gate: condom stays, no removal (marital bed, etc.)
    if getattr(store, "_scene_restricted", False):
        $ debug_log("[CUM_ROUTE] -> scene_restricted: condom stays, limited menu")
        menu:
            "Cum in the condom":
                call _cum_dispatch_anim(girl, scene_type) from _call__cum_anim_condom_restricted
                "You finish inside the condom."
                $ process_cum(girl, scene_type, "condom")
                $ apply_cum_bonuses(girl, "cum_outside")
                $ _cum_say_line(girl, "condom", scene_type)

            "Cum outside":
                call PlayerCumMenu_Outside_Penetration(girl, scene_type) from _call_PlayerCumMenu_Outside_restricted

            "Ask to remove and cum inside":
                python:
                    _restr_cum_deny = [
                        _("Are you out of your mind? The condom stays on."),
                        _("No. You don't get to make that call. Not here."),
                        _("I said we use protection. That's final."),
                    ]
                $ set_scene_expression(girl, "angry")
                $ Say_Line(girl, _tl(renpy.random.choice(_restr_cum_deny)))
                call _cum_dispatch_anim(girl, scene_type) from _call__cum_anim_condom_restricted_deny
                $ set_scene_expression(girl, "serious")
                $ Say_Line(girl, _tl(_("You finish in the condom. End of story.")))
                $ process_cum(girl, scene_type, "condom")
                $ apply_cum_bonuses(girl, "cum_outside")
        return

    # Story step gate: her step locks going raw or a creampie = condom cannot come off, limited cum menu
    if story_act_locked(girl, "raw") or story_act_locked(girl, "cum_inside"):
        $ debug_log("[CUM_ROUTE] -> story-locked raw / cum_inside: condom stays, limited menu")
        menu:
            "Cum in the condom":
                call _cum_dispatch_anim(girl, scene_type) from _call__cum_anim_condom_story
                "You finish inside the condom."
                $ process_cum(girl, scene_type, "condom")
                $ apply_cum_bonuses(girl, "cum_outside")
                $ _cum_say_line(girl, "condom", scene_type)

            "Cum outside":
                call PlayerCumMenu_Outside_Penetration(girl, scene_type) from _call_PlayerCumMenu_Outside_story

            "Ask to remove and cum inside":
                $ set_scene_expression(girl, "angry")
                $ Say_Line(girl, story_locked_line(girl, "raw" if story_act_locked(girl, "raw") else "cum_inside"))
                call _cum_dispatch_anim(girl, scene_type) from _call__cum_anim_condom_story_deny
                "You finish inside the condom."
                $ process_cum(girl, scene_type, "condom")
                $ apply_cum_bonuses(girl, "cum_outside")

            "Ask to cum in her mouth":
                $ _cum_check_mouth = CumPermissionCheck(girl, "cum_in_mouth_ask")
                if _cum_check_mouth["accepted"]:
                    $ Say_Line(girl, scene_pick_line("cum_mouth_accepted", scene=scene_type, girl=girl) or _("Go ahead... do it."))
                    call _cum_in_mouth_via_bj(girl, scene_type) from _call__cum_in_mouth_via_bj_condom_story
                else:
                    $ Say_Line(girl, scene_pick_line("cum_mouth_denied", scene=scene_type, girl=girl) or _("No way... not in my mouth."))
                    "You finish inside the condom instead."
                    $ process_cum(girl, scene_type, "condom")
                    $ apply_cum_bonuses(girl, "cum_outside")
        return

    $ _condom_was_removed = getattr(store, "_condom_removed_midscene", False)
    $ debug_log("[CUM_ROUTE] past cheat check: _condom_removed_midscene=%s" % _condom_was_removed)

    if _condom_was_removed:
        $ debug_log("[CUM_ROUTE] -> redirecting to RAW menu (condom removed midscene but condom_active still True)")
        call PlayerCumMenu_Penetration_Raw(girl, scene_type) from _call_PlayerCumMenu_Penetration_Raw_midremove
        return

    $ _is_cum_slut_condom = girl.has_trait("cum_slut")
    $ _cumslut_cream_count_condom = getattr(girl, "CreampieCounts", 0)

    # ── cum_slut 5+ creampies: AUTO removes condom + creampie ──
    if _is_cum_slut_condom and _cumslut_cream_count_condom >= 5:
        $ debug_log("[CUM_ROUTE] -> cum_slut AUTO rip (5+ creampies)")
        python:
            _auto_rip = [
                _("Take it OFF! Rip it off and cum inside me! NOW!"),
                _("I don't CARE about the condom! Take it off! I NEED you inside me!"),
                _("NO condom! I want to FEEL it! Take it off and fill me up!"),
            ]
            _auto_rip2 = [
                _("YES! GIVE IT TO ME! ALL OF IT INSIDE!"),
                _("DEEPER! I want every drop! Don't hold back!"),
                _("Oh GOD yes! FILL ME!"),
            ]
        $ Say_Line(girl, _tl(renpy.random.choice(_auto_rip)))
        "She reaches down and rips the condom off herself."
        $ _on_condom_removed(girl, skip_hide=_cum_skip_hide(scene_type))
        call _cum_dispatch_condom_remove(girl, scene_type) from _call__cum_condom_remove_cumslut_auto
        $ set_scene_expression(girl, renpy.random.choice(["ahegao", "ahegao_2"]), blush="3")
        $ Say_Line(girl, _tl(renpy.random.choice(_auto_rip2)))
        if scene_type == "cowgirl":
            "She slams down on you with all her weight, grinding harder and faster. You couldn't push her off even if you tried."
        else:
            "She throws herself back against you at full speed, her whole body shaking. Your mind goes completely blank."
        call _cum_dispatch_anim(girl, scene_type) from _call__cum_anim_cumslut_auto
        "You cum deep inside her."
        $ process_cum(girl, scene_type, "condom_removed_inside")
        $ apply_cum_bonuses(girl, "condom_removed_allowed")
        $ _cr_line = _consented_cream_line(girl, scene_type)
        $ Say_Line(girl, _cr_line)
        return

    # ── cum_slut 3+ creampies: she BEGS before the menu ──
    if _is_cum_slut_condom and _cumslut_cream_count_condom >= 3:
        python:
            _beg_condom = [
                _("Take the condom off... please, I want to feel you cum inside..."),
                _("I don't want the condom... please, take it off and cum inside me..."),
                _("Can you please take it off? I need to feel it inside..."),
            ]
        $ Say_Line(girl, _tl(renpy.random.choice(_beg_condom)))

    $ debug_log("[CUM_ROUTE] -> showing NORMAL condom menu (Cum in the condom + Cum outside + Warn her + Ask to remove)")
    menu:
        "Cum in the condom":
            call _cum_dispatch_anim(girl, scene_type) from _call__cum_anim_condom
            # ── cum_slut 3+ begging intercept ──
            if _is_cum_slut_condom and _cumslut_cream_count_condom >= 3:
                python:
                    _despair_condom = [
                        _("No! Take it off! PLEASE! I need to feel you inside me!"),
                        _("Don't cum in the condom! Please, take it off! I'm BEGGING you!"),
                        _("Please reconsider! I want it RAW... I need it inside me!"),
                    ]
                $ Say_Line(girl, _tl(renpy.random.choice(_despair_condom)))
                menu:
                    "Reconsider (remove condom, cum inside)":
                        python:
                            _relief_condom = [
                                _("Yes! Thank you! Take it off, take it off!"),
                                _("Oh god, yes! I need to feel you!"),
                            ]
                        $ Say_Line(girl, _tl(renpy.random.choice(_relief_condom)))
                        $ set_scene_expression(girl, renpy.random.choice(["ahegao", "ahegao_2"]), blush="3")
                        $ _on_condom_removed(girl, skip_hide=_cum_skip_hide(scene_type))
                        call _cum_dispatch_condom_remove(girl, scene_type) from _call__cum_condom_remove_reconsider
                        call _cum_dispatch_anim(girl, scene_type) from _call__cum_anim_reconsider
                        "You rip the condom off and cum deep inside her."
                        $ process_cum(girl, scene_type, "condom_removed_inside")
                        $ apply_cum_bonuses(girl, "condom_removed_allowed")
                        $ _cr_line = _consented_cream_line(girl, scene_type)
                        $ Say_Line(girl, _cr_line)
                    "Ignore her":
                        "You finish inside the condom despite her pleas."
                        $ process_cum(girl, scene_type, "condom")
                        $ apply_cum_bonuses(girl, "cum_outside")
                        $ _cum_say_line(girl, "condom", scene_type)
            else:
                "You finish inside the condom."
                $ process_cum(girl, scene_type, "condom")
                $ apply_cum_bonuses(girl, "cum_outside")
                $ _cum_say_line(girl, "condom", scene_type)

        "Cum outside":
            # ── cum_slut 3+ begging intercept ──
            if _is_cum_slut_condom and _cumslut_cream_count_condom >= 3:
                python:
                    _despair_condom_out = [
                        _("No! Don't pull out! Take the condom off and cum INSIDE!"),
                        _("WAIT! Please! Remove it and give it to me inside!"),
                        _("Don't waste it outside! I NEED it in me! Please!"),
                    ]
                $ Say_Line(girl, _tl(renpy.random.choice(_despair_condom_out)))
                menu:
                    "Reconsider (remove condom, cum inside)":
                        python:
                            _relief_condom2 = [
                                _("YES! Take it off! Give it ALL to me!"),
                                _("Thank you! I need every drop inside!"),
                            ]
                        $ Say_Line(girl, _tl(renpy.random.choice(_relief_condom2)))
                        $ set_scene_expression(girl, renpy.random.choice(["ahegao", "ahegao_2"]), blush="3")
                        $ _on_condom_removed(girl, skip_hide=_cum_skip_hide(scene_type))
                        call _cum_dispatch_condom_remove(girl, scene_type) from _call__cum_condom_remove_reconsider2
                        call _cum_dispatch_anim(girl, scene_type) from _call__cum_anim_reconsider2
                        "You rip the condom off and cum deep inside her."
                        $ process_cum(girl, scene_type, "condom_removed_inside")
                        $ apply_cum_bonuses(girl, "condom_removed_allowed")
                        $ _cr_line = _consented_cream_line(girl, scene_type)
                        $ Say_Line(girl, _cr_line)
                    "Ignore her":
                        "You pull out despite her pleas."
                        call PlayerCumMenu_Outside_Penetration(girl, scene_type) from _call_PlayerCumMenu_Outside_Penetration_condom_ignore
            else:
                call PlayerCumMenu_Outside_Penetration(girl, scene_type) from _call_PlayerCumMenu_Outside_Penetration

        "Ask to cum in her mouth":
            $ _cum_check_mouth = CumPermissionCheck(girl, "cum_in_mouth_ask")
            if _cum_check_mouth["accepted"]:
                $ Say_Line(girl, scene_pick_line("cum_mouth_accepted", scene=scene_type, girl=girl) or _("Go ahead... do it."))
                call _cum_in_mouth_via_bj(girl, scene_type) from _call__cum_in_mouth_via_bj_condom_mouth
            else:
                $ Say_Line(girl, scene_pick_line("cum_mouth_denied", scene=scene_type, girl=girl) or _("No way... not in my mouth."))
                "You finish inside the condom instead."
                $ process_cum(girl, scene_type, "condom")
                $ apply_cum_bonuses(girl, "cum_outside")

        "Warn her":
            call _cum_warn_her_condom(girl, scene_type) from _call__cum_warn_her_condom

        "Ask to remove and cum inside":
            $ _cum_check = CumPermissionCheck(girl, "cum_remove_condom_ask")
            if _cum_check["accepted"]:
                $ _cr_line = scene_pick_line("cum_inside_accepted", scene=scene_type, girl=girl) or _("Okay... take it off. I want to feel you.")
                $ Say_Line(girl, _cr_line)
                $ _on_condom_removed(girl, skip_hide=_cum_skip_hide(scene_type))
                $ store._creampie_consent = "allowed"
                if _is_cum_slut_condom:
                    $ set_scene_expression(girl, renpy.random.choice(["ahegao", "ahegao_2"]), blush="3")
                call _cum_dispatch_condom_remove(girl, scene_type) from _call__cum_condom_remove_ask_remove
                call _cum_dispatch_anim(girl, scene_type) from _call__cum_anim_ask_remove_ok
                "You rip the condom off and cum deep inside her."
                $ process_cum(girl, scene_type, "condom_removed_inside")
                $ apply_cum_bonuses(girl, "condom_removed_allowed")
                $ _cr_line = _consented_cream_line(girl, scene_type)
                $ Say_Line(girl, _cr_line)
            else:
                if _cum_check["outcome"] == "hard_deny":
                    $ _cr_line = scene_pick_line("cum_inside_denied", scene=scene_type, girl=girl) or _("Absolutely not. Don't even think about it.")
                    $ Say_Line(girl, _cr_line)
                    "She grabs the condom to make sure it stays on."
                else:
                    $ _cr_line = scene_pick_line("cum_inside_denied", scene=scene_type, girl=girl) or _("No! Keep the condom on.")
                    $ Say_Line(girl, _cr_line)
                python:
                    _fin_combo_ok = _can_financial_extra(girl, "creampie")
                    _fin_combo_price = _calc_financial_extra_price(girl, "condom_remove") + _calc_financial_extra_price(girl, "creampie") if _fin_combo_ok else 0
                    import math
                    _fin_combo_price = max(50, int(math.ceil(_fin_combo_price / 50.0) * 50)) if _fin_combo_ok else 0
                    _fin_combo_afford = _fin_combo_ok and store.Player.cash >= _fin_combo_price
                if _fin_combo_afford:
                    menu:
                        "Offer extra to go raw and cum inside":
                            $ set_scene_expression(girl, "surprised")
                            $ Say_Player(_("What if I pay you to take the condom off and let me cum inside?"))
                            python:
                                _pp_here = _is_partner_present(girl)[0] if hasattr(girl, "has_npc_partner") and girl.has_npc_partner() else False
                                if _pp_here:
                                    set_scene_expression(girl, None, eyes="eyes_side", brows="brows_confused", mouth="mouth_serious")
                                else:
                                    set_scene_expression(girl, "worried")
                            $ Say_Line(girl, _fin_line(girl, "midscene_combo_paid", fmt={"price": _fin_combo_price}))
                            menu:
                                "Pay $[_fin_combo_price]":
                                    $ _financial_pay(girl, _fin_combo_price)
                                    $ store._financial_extras_paid["condom_remove"] = True
                                    $ store._financial_extras_paid["creampie"] = True
                                    $ set_scene_expression(girl, "sad")
                                    $ _on_condom_removed(girl, skip_hide=_cum_skip_hide(scene_type))
                                    $ store._creampie_consent = "allowed"
                                    if getattr(store, "_recording_active", False):
                                        $ unlock_achievement("expensive_pie")
                                    call _cum_dispatch_condom_remove(girl, scene_type) from _call__cum_condom_remove_fin
                                    call _cum_dispatch_anim(girl, scene_type) from _call__cum_anim_condom_fin
                                    "You rip the condom off and cum inside her."
                                    $ process_cum(girl, scene_type, "condom_removed_inside")
                                    $ apply_cum_bonuses(girl, "condom_removed_allowed")
                                "Never mind":
                                    $ set_scene_expression(girl, "normal")
                                    "You finish inside the condom."
                                    $ process_cum(girl, scene_type, "condom")
                                    $ apply_cum_bonuses(girl, "cum_outside")
                        "Finish in condom":
                            "She won't allow it. You finish inside the condom."
                            $ process_cum(girl, scene_type, "condom")
                            $ apply_cum_bonuses(girl, "cum_outside")
                else:
                    "She won't allow it. You finish inside the condom."
                    $ process_cum(girl, scene_type, "condom")
                    $ apply_cum_bonuses(girl, "cum_outside")

        "Remove condom and cum inside":
            $ _cum_check = CumPermissionCheck(girl, "cum_remove_condom_ask")
            $ _on_condom_removed(girl, skip_hide=_cum_skip_hide(scene_type))
            if not (girl.has_trait("cum_slut") or girl.has_trait("hardcore_sex")):
                $ store._cum_forced_surprise = True
            call _cum_dispatch_condom_remove(girl, scene_type) from _call__cum_condom_remove_force_remove
            call _cum_dispatch_anim(girl, scene_type) from _call__cum_anim_force_remove
            "You rip the condom off and cum deep inside her."
            $ process_cum(girl, scene_type, "condom_removed_inside")
            if _cum_check["accepted"]:
                # She would have said yes -- surprised but accepts
                python:
                    _rc_lines = {
                        "cum_slut": [
                            _("You ripped it off AND came inside?! ...God, that's perfect. Do it every time."),
                            _("No condom, no warning, straight inside me... you're my kind of man."),
                            _("You didn't even ask... just ripped it off and filled me up. I'm in love."),
                        ],
                        "cum_slut_first": [
                            _("You took it off and... inside?! Oh my god... so that's what it feels like..."),
                            _("Wait, you... inside me? I didn't know it would feel like this..."),
                            _("No condom... and you finished inside... I can feel all of it. Wow..."),
                        ],
                        "cum_slut_new": [
                            _("You ripped it off and came inside?! ...I should be mad. I'm really not."),
                            _("No condom, no warning... and I loved it. What's wrong with me?"),
                            _("You didn't even ask... and I can't stop smiling."),
                        ],
                        "hardcore_sex": [
                            _("You ripped it off and came inside without a word. Respect."),
                            _("No asking, no hesitation... just raw cum inside me. That's how it should be."),
                            _("You just took what you wanted. Good. Don't ever ask next time either."),
                        ],
                        "cute_sex": [
                            _("Y-you took it off AND came inside?! That's so... I felt everything... it was warm..."),
                            _("You... you could have asked first... but... I felt so close to you just now..."),
                            _("I wasn't ready for that... but it felt really nice... all warm inside..."),
                        ],
                        "_bf": [
                            _("You're cumming inside me without the condom AND without asking... I should kill you, but your cum feels so good..."),
                            _("You ripped it off and came inside %(poss)s girlfriend without a word... and I love every second of it..."),
                            _("My %(pl)s asks permission for everything. You just rip the condom off and cum inside me like you own me..."),
                            _("No condom, no warning... you just came inside someone else's girlfriend. And I want more..."),
                            _("%(Pp)s would never do this to me... rip it off and just finish inside... but you did. And I'm not even mad..."),
                        ],
                        "_default": [
                            _("You could have just asked... but honestly? I liked it better this way."),
                            _("You ripped it off and came inside without a word... bold. But I'm not mad."),
                            _("No warning, no condom... you just went for it. I'll let it slide."),
                            _("That was... intense. You didn't ask at all. But it felt good."),
                        ],
                    }
                    _rc_sl = None
                    if girl.has_trait("cum_slut"):
                        _rc_sl = renpy.random.choice(_rc_lines[trait_pool_key(girl, "cum_slut", _rc_lines)])
                    else:
                        for _t in ("hardcore_sex", "cute_sex"):
                            if girl.has_trait(_t):
                                _rc_sl = renpy.random.choice(_rc_lines[_t])
                                break
                    if _rc_sl is None and hasattr(girl, "has_npc_partner") and girl.has_npc_partner():
                        _rc_sl = _format_partner_line(girl, renpy.random.choice(_rc_lines["_bf"]))
                    if _rc_sl is None:
                        _rc_sl = renpy.random.choice(_rc_lines["_default"])
                $ Say_Line(girl, _rc_sl)
                $ apply_cum_bonuses(girl, "condom_removed_allowed")
                $ store._creampie_consent = "allowed"
            else:
                # Forced condom removal + creampie... very aggressive
                $ apply_cum_penalties(girl, "condom_removed_forced")
                $ store._forced_creampie_count += 1

                if girl.has_trait("cum_slut"):
                    $ _cr_line = scene_pick_line("cum_inside", scene=scene_type, girl=girl) or _("You ripped it off?! ...Okay, I actually love this.")
                    $ Say_Line(girl, _cr_line)
                elif getattr(girl, "Lust", 0) >= 90:
                    $ _lust_lines = [ \
                        _("You took the condom OFF?! I... ngh... I'm too close to stop... you bastard...!"), \
                        _("Are you INSANE?! The condom... ahhh... f-fuck, I can't think straight...!"), \
                    ]
                    $ Say_Line(girl, _tl(renpy.random.choice(_lust_lines)))
                    $ Change_Status(girl, "Love", -40)
                    $ store._forced_creampie_end_after_orgasm = True
                    # Force speed 3 — she's overwhelmed
                    python:
                        _sv = _cum_cfg(scene_type, "speed_var")
                        if _sv:
                            setattr(store, _sv, 3)
                    call _cum_dispatch_apply_speed(girl, scene_type, speed=3) from _call_as_forced_condom_off
                else:
                    if girl.has_trait("hate_cum"):
                        call _hate_cum_angry_end(girl, scene_type) from _call__hate_cum_angry_end_2
                    else:
                        call _forced_condom_removal_angry_end(girl, scene_type) from _call__forced_condom_removal_angry_end

    return

# ------------------------------------------------------------
# Without condom (raw)... respects _creampie_consent flag
# "allowed" / "changed_mind" = she's okay with it
# "denied" = she said no (force = penalties)
# ------------------------------------------------------------
label PlayerCumMenu_Penetration_Raw(girl, scene_type):

    # ── Forced creampie (story event: she commands it, no choice) ──
    if getattr(store, "_force_creampie", False):
        $ set_scene_expression(girl, "lusty", blush="2")
        $ Say_Line(girl, _tl(_("Inside. All of it. Don't even think about pulling out.")))
        menu:
            "Cum inside her":
                pass
            "Try to pull out":
                $ set_scene_expression(girl, "angry")
                $ Say_Line(girl, _tl(_("I said INSIDE.")))
                "She pushes back hard, locking you in place."
        call _cum_dispatch_anim(girl, scene_type) from _call__cum_anim_force_creampie
        $ set_scene_expression(girl, renpy.random.choice(["ahegao", "ahegao_2"]), blush="3")
        "You cum deep inside her."
        $ process_cum(girl, scene_type, "inside")
        $ apply_cum_bonuses(girl, "cum_inside_allowed")
        $ Say_Line(girl, _tl(_("Good boy.")))
        return

    $ _consent = store._creampie_consent
    $ _girl_requested = getattr(store, "_girl_requested_creampie", False)

    # "blocked" = she's angry about forced condom removal... cannot be overridden
    # If she explicitly requested it via SubEvent, override to allowed (unless blocked)
    if _girl_requested and _consent != "blocked":
        $ _consent = "allowed"

    $ _is_hate_cum = girl.has_trait("hate_cum")
    $ _is_cum_slut = girl.has_trait("cum_slut")
    $ _first_creampie = (getattr(girl, "CreampieCounts", 0) == 0)
    $ _cumslut_cream_count = getattr(girl, "CreampieCounts", 0)

    # ── Determine if a forced cum scenario would trigger ──
    $ _force_type = None
    $ _on_forced_cd = _forced_cum_on_cooldown(girl)
    if _is_cum_slut and not trait_is_veteran(girl, "cum_slut") and getattr(girl, "_cumslut_denied_inside", False):
        # still discovering it: she never forces it (a revenge left pending from an older save is dropped)
        $ girl._cumslut_denied_inside = False
        $ print("[CUM] %s still discovering cum_slut: pending revenge creampie dropped" % girl.gid)
    if _is_cum_slut and trait_is_veteran(girl, "cum_slut"):
        if getattr(girl, "_cumslut_denied_inside", False):
            $ _force_type = "revenge"
        elif _cumslut_cream_count >= 5 and not _on_forced_cd:
            $ _force_type = "auto"

    # pregnancy_fetish: she will not let him pull out, and starts earlier than plain cum_slut
    # (pregnancy.rpy, plan section 17). A pending revenge keeps priority.
    if _force_type != "revenge" and not _on_forced_cd and callable(globals().get("fert_breed_force_type", None)):
        $ _force_type = fert_breed_force_type(girl, scene_type) or _force_type

    # femdom veteran on top: she decides where he finishes (Actions/femdom.rpy)
    if not _force_type and not _on_forced_cd:
        $ _force_type = femdom_force_type(girl, scene_type, _consent)

    # ── RESIST GATE: check if player can block the forced scenario ──
    if _force_type:
        $ _auto_resist_reason = _get_auto_resist_reason(girl)

        if _auto_resist_reason:
            # ── AUTO-RESIST: she tries but FAILS ──
            python:
                _intent_pool = RESIST_AUTO_OBED_GIRL[_force_type] if _auto_resist_reason == "obed" else RESIST_AUTO_STRENGTH_GIRL[_force_type]
            $ Say_Line(girl, _tl(renpy.random.choice(_intent_pool)))

            if _auto_resist_reason == "obed":
                $ _narr = _tl(renpy.random.choice(RESIST_AUTO_OBED_NARR))
                "[_narr]"
                $ Say_Line(girl, _tl(renpy.random.choice(RESIST_AUTO_OBED_GIRL_AFTER)))
            else:
                python:
                    _pos_type = RESIST_POSITION_TYPE.get(scene_type, "neutral")
                    _narr = _tl(renpy.random.choice(RESIST_AUTO_STRENGTH_NARR[_pos_type]))
                "[_narr]"
                $ Say_Line(girl, _tl(renpy.random.choice(RESIST_AUTO_STRENGTH_GIRL_AFTER)))
                # "She tried, but you're stronger": the automatic strength resist IS that (Athlete / Max Energy 5)
                $ unlock_achievement("iron_will")

            if _force_type == "revenge":
                $ girl._cumslut_denied_inside = False
            $ Change_Status(girl, "Obed", 10)
            $ _force_type = None

        else:
            # ── CAN'T AUTO-RESIST: last-moment menu ──
            python:
                _intent_pool = RESIST_AUTO_STRENGTH_GIRL[_force_type]
            $ Say_Line(girl, _tl(renpy.random.choice(_intent_pool)))

            call _player_resist_forced_cum(girl, scene_type) from _call_resist_penetration

            if store._resist_result == "resisted":
                if _force_type == "revenge":
                    $ girl._cumslut_denied_inside = False
                $ Change_Status(girl, "Obed", 10)
                $ _force_type = None

    # ── FORCED: REVENGE path (player accepted or failed to resist) ──
    if _force_type == "revenge":
        $ unlock_achievement("no_choice")
        $ girl._cumslut_denied_inside = False
        $ store._hard_cum_ready = True
        python:
            _revenge_followup = [
                _("YES! YES! YESSS! That's what I NEEDED!"),
                _("Oh GOD! Finally! Don't you EVER deny me again!"),
                _("See? Was that so hard? Now fill me up COMPLETELY!"),
            ]
        $ set_scene_expression(girl, renpy.random.choice(["ahegao", "ahegao_2"]), blush="3")
        if scene_type == "cowgirl":
            "She locks her legs around you and slams down with terrifying force. You have zero control."
        else:
            "She throws herself back against you, slamming at maximum speed. Before you can even think about pulling out, it's too late."
        call _cum_dispatch_anim(girl, scene_type) from _call__cum_anim_cumslut_revenge
        $ Say_Line(girl, _tl(renpy.random.choice(_revenge_followup)))
        "You cum deep inside her. She doesn't let go until she's sure every drop is inside."
        $ process_cum(girl, scene_type, "inside")
        $ apply_cum_bonuses(girl, "cum_inside_allowed")
        $ girl.discover("discovered_trait_cum_slut") if girl.has_trait("cum_slut") else None
        $ Change_Status(girl, "Obed", 15)
        $ Change_Status(girl, "Inbt", 10)
        return

    # ── FORCED: FEMDOM path (a veteran femdom on top keeps him inside; he accepted or failed to resist) ──
    if _force_type == "femdom":
        $ unlock_achievement("no_choice")
        $ set_scene_expression(girl, "lusty", blush="2")
        $ Say_Line(girl, scene_pick_line("femdom_force_cum", scene=scene_type, girl=girl))
        $ girl.discover("discovered_trait_femdom") if girl.has_trait("femdom") else None
        "She pins your wrists down and rides you through it. Where you finish is not your call."
        "You cum deep inside her."
        $ process_cum(girl, scene_type, "inside")
        $ apply_cum_bonuses(girl, "cum_inside_allowed")
        $ Say_Line(girl, scene_pick_line("femdom_force_cum_after", scene=scene_type, girl=girl))
        return

    # ── FORCED: AUTO-CREAMPIE path (player accepted or failed to resist) ──
    # "breed" = same flow driven by her breeding kink, with breeding lines (pregnancy.rpy)
    if _force_type in ("auto", "breed"):
        $ unlock_achievement("no_choice")
        python:
            _auto_followup = [
                _("YES! YES! YESSS! Don't stop!"),
                _("GIVE IT TO ME! ALL OF IT!"),
                _("DEEPER! I want every last drop!"),
                _("Oh GOD yes! FILL ME UP!"),
            ]
            if callable(globals().get("fert_breed_pool", None)):
                _auto_followup = fert_breed_pool(girl, scene_type, "followup", _auto_followup)
        $ set_scene_expression(girl, renpy.random.choice(["ahegao", "ahegao_2"]), blush="3")
        $ Say_Line(girl, _tl(renpy.random.choice(_auto_followup)))
        # the "auto" force is her cum_slut veteran taking the creampie ("FILL ME UP!");
        # "breed" speaks from the breeding pools and discovers through them (pregnancy.rpy)
        $ girl.discover("discovered_trait_cum_slut") if (_force_type == "auto" and girl.has_trait("cum_slut")) else None
        if scene_type == "cowgirl":
            "She slams down on you even harder and faster, pinning you underneath her with all her weight. There's no way to lift her off."
        else:
            "She picks up the pace to the max, grinding back against you with everything she has. Your mind goes blank and you can't even think about where to cum."
        "You cum deep inside her."
        $ process_cum(girl, scene_type, "inside")
        $ apply_cum_bonuses(girl, "cum_inside_allowed")
        $ _cr_line = _consented_cream_line(girl, scene_type)
        $ Say_Line(girl, _cr_line)
        return

    # ── cum_slut 3+ creampies: she BEGS before the menu ──
    if _is_cum_slut and _cumslut_cream_count >= 3:
        python:
            _beg_lines = [
                _("Please... cum inside me. I need to feel it..."),
                _("You're close, right? Do it inside... please..."),
                _("Don't pull out... I want it all inside me..."),
                _("Promise me you'll cum inside... I need it so bad..."),
            ]
            if callable(globals().get("fert_breed_pool", None)):
                _beg_lines = fert_breed_pool(girl, scene_type, "beg", _beg_lines)
        $ Say_Line(girl, _tl(renpy.random.choice(_beg_lines)))

    menu:
        "Cum outside":
            # ── cum_slut intercept (always, not just 3+). Still discovering it: no begging, the choice stays
            #    his and her "cum_outside" reaction (cum_slut_first / _new) says she wanted it ──
            if _is_cum_slut and trait_is_veteran(girl, "cum_slut"):
                python:
                    _despair_lines = [
                        _("No! No no no! Please don't! I NEED it inside me!"),
                        _("Wait! Please reconsider! I'm begging you, cum inside!"),
                        _("Don't waste it! Please... I'll do anything, just cum inside me!"),
                        _("NO! You can't! I need to feel you cum inside me, PLEASE!"),
                    ]
                    if callable(globals().get("fert_breed_pool", None)):
                        _despair_lines = fert_breed_pool(girl, scene_type, "despair", _despair_lines)
                $ Say_Line(girl, _tl(renpy.random.choice(_despair_lines)))
                menu:
                    "Reconsider (cum inside)":
                        python:
                            _relief_lines = [
                                _("Yes! Thank you! Give it all to me!"),
                                _("Oh god, yes! I knew you wouldn't deny me!"),
                                _("YES! Inside! All of it!"),
                            ]
                            if callable(globals().get("fert_breed_pool", None)):
                                _relief_lines = fert_breed_pool(girl, scene_type, "relief", _relief_lines)
                        $ Say_Line(girl, _tl(renpy.random.choice(_relief_lines)))
                        $ set_scene_expression(girl, renpy.random.choice(["ahegao", "ahegao_2"]), blush="3")
                        "You thrust deep and cum inside her."
                        $ process_cum(girl, scene_type, "inside")
                        $ apply_cum_bonuses(girl, "cum_inside_allowed")
                        $ _cr_line = _consented_cream_line(girl, scene_type)
                        $ Say_Line(girl, _cr_line)
                    "Ignore her":
                        "You pull out despite her pleas."
                        call PlayerCumMenu_Outside_Penetration(girl, scene_type) from _call_PlayerCumMenu_Outside_Penetration_cumslut_ignore
                        python:
                            _ignored = [
                                _("You... you pulled out...? I can't believe you..."),
                                _("No... all that cum... wasted... why would you do that to me..."),
                                _("I begged you... I BEGGED you and you still pulled out..."),
                            ]
                            if callable(globals().get("fert_breed_pool", None)):
                                _ignored = fert_breed_pool(girl, scene_type, "ignored", _ignored)
                        $ Say_Line(girl, _tl(renpy.random.choice(_ignored)))
                        $ Change_Status(girl, "Love", -8)
                        $ Change_Status(girl, "Obed", 8)
                        $ girl._cumslut_denied_inside = True
            else:
                call PlayerCumMenu_Outside_Penetration(girl, scene_type) from _call_PlayerCumMenu_Outside_Penetration_1

        "Ask to cum inside her mouth" if not store._stealth_condom_removed:
            if scene_type in _ANAL_SCENE_TYPES:
                # ATM path: much harder, pre-reaction dialogue
                $ _cum_check = CumPermissionCheck(girl, "cum_in_mouth_from_anal_ask")

                # Virgin / first kiss / first BJ callout — plays before accept or reject
                python:
                    _iflags = getattr(girl, "intimacy_flags", set())
                    _is_virgin = girl.has_trait("virgin")
                    _never_kissed = "kiss" not in _iflags
                    _never_bj = "bj" not in _iflags
                    _atm_callout = None

                    if _is_virgin and _never_kissed and _never_bj:
                        _atm_callout = renpy.random.choice([
                            _("I've never had it in my mouth before... you haven't even kissed me yet... I've never been kissed at all. And you want me to taste... that?!"),
                            _("You haven't even kissed me... you haven't put it in my mouth once... you skipped everything and now THIS?"),
                        ])
                    elif _is_virgin and _never_bj:
                        _atm_callout = renpy.random.choice([
                            _("You skipped my... you went straight to my ass and now you want it in my mouth? I've never even done that before!"),
                            _("You ignored everything else... went for my ass first... and now my mouth? Before I've even tried it normally?"),
                        ])
                    elif _is_virgin:
                        _atm_callout = renpy.random.choice([
                            _("You've been everywhere except... you know. And now you want it from THERE to my mouth?"),
                            _("You've done everything BUT the normal thing... and now you want me to taste where it's been?"),
                        ])
                    elif _never_kissed:
                        _atm_callout = renpy.random.choice([
                            _("You haven't even kissed me yet and you want me to put THAT in my mouth?"),
                            _("We haven't even kissed... and my first taste of you is going to be... that?"),
                        ])
                    elif _never_bj:
                        _atm_callout = renpy.random.choice([
                            _("I've never even had it in my mouth before and you want the first time to be from THERE?"),
                            _("My first time putting it in my mouth... and it's coming straight from my ass?"),
                        ])

                    if _atm_callout:
                        Say_Line(girl, _atm_callout)
                        debug_log("[DEBUG] ATM virgin/first callout played: virgin=%s kissed=%s bj=%s" % (_is_virgin, not _never_kissed, not _never_bj))

                    # Pre-ATM: she hasn't even cum yet and he's already asking for ATM
                    _girl_orgasms = getattr(girl, "Orgasms", {})
                    _scene_orgasms = _girl_orgasms.get(scene_type, 0) + store._session_girl_orgasms
                    if _scene_orgasms == 0 and girl.Lust < 100:
                        _no_cum_line = renpy.random.choice([
                            _("You haven't even let me finish yet and you want me to do THAT?"),
                            _("I haven't even cum once and you're already asking for this?"),
                            _("You didn't even bother making me feel good first... and now you want this."),
                        ])
                        Say_Line(girl, _no_cum_line)
                        debug_log("[DEBUG] ATM pre-orgasm callout: girl hasn't cum this session")

                $ store._never_kissed_before_atm = _never_kissed
                $ debug_log("[ATM_FK] SET _never_kissed_before_atm=%s (PlayerCumMenu path)" % _never_kissed)

                if _cum_check["accepted"]:
                    # Pre-reaction: she knows where it's been
                    python:
                        _atm_pre = None
                        _has_hc = girl.has_trait("hardcore_sex")
                        _has_ah = girl.has_trait("anal_hater")
                        _has_al = girl.has_trait("anal_lover")
                        _has_hc_cum = girl.has_trait("hate_cum")
                        _has_sub = girl.has_trait("submissive")
                        # still discovering the cum or the anal (trait_is_new): she wants it and can't believe it
                        _al_atm_disc = _has_al and trait_is_new(girl, "anal_lover")

                        if girl.has_trait("cum_slut") and (trait_is_new(girl, "cum_slut") or _al_atm_disc):
                            _atm_pre_pool = [
                                _("From my ass to my mouth? That's so filthy... why does that make me want it?"),
                                _("You want me to taste... after it was there? ...Okay. I want to."),
                                _("I shouldn't want this... but yes. Give it to me."),
                            ]
                        elif girl.has_trait("cum_slut"):
                            _atm_pre_pool = [
                                _("Straight from my ass to my mouth? God, that's filthy... I love it."),
                                _("You want me to taste my own ass? God, please..."),
                                _("Right from my ass? Mmm... give it to me."),
                            ]
                        elif _has_al and _has_hc and _al_atm_disc:
                            _atm_pre_pool = [
                                _("Ass to mouth? ...Okay. Don't go easy on me."),
                                _("From my ass to my mouth... god, why am I into this?"),
                            ]
                        elif _has_al and _has_sub and not _al_atm_disc:
                            _atm_pre_pool = [
                                _("Your plan here better be to make me taste everything. I'll be mad if you don't make me the dirtiest possible slut by the end of this."),
                                _("From my ass to my mouth... god yes. Make me earn it."),
                                _("Straight from my ass to my mouth? Yes. Use me however you like, both ends are yours."),
                            ]
                        elif _has_al and _has_hc:
                            _atm_pre_pool = [
                                _("Ass to mouth? You'd better not hold back. I want it filthy."),
                                _("Straight from my ass to my mouth? Yes. Shove it in deep and don't be gentle."),
                                _("From my ass to my throat, fast and rough. That's exactly how I want it."),
                            ]
                        elif _has_sub and _has_ah and _has_hc_cum:
                            _atm_pre_pool = [
                                _("That's disgusting on two levels... and you know I'll do it anyway because you told me to."),
                                _("I hate cum and I hate where that's been... but you want it in my mouth, so I'll open up."),
                                _("Two things I hate, and you want both on my tongue. ...Okay. I'm not going to say no to you."),
                            ]
                        elif _has_hc and _has_ah and _has_hc_cum:
                            _atm_pre_pool = [
                                _("Cum from my ass? I hate both of those things... but you making me? ...Fine."),
                                _("I hate everything about this... and that's exactly why you want me to, right? ...Okay."),
                            ]
                        elif _has_hc and _has_ah:
                            _atm_pre_pool = [
                                _("From my ass? I hate that... but the fact you'd make me do it... fine."),
                                _("That's repulsive... and you know I hate it. That's why you're asking, isn't it? ...Do it."),
                                _("I despise where that's been... but something about how wrong this is... just do it."),
                            ]
                        elif _has_sub and _has_hc_cum:
                            _atm_pre_pool = [
                                _("I hate the taste of cum... but if you're telling me to do it, I'll do it."),
                                _("You know I hate cum. But you want it in my mouth anyway? ...Fine. You're the boss."),
                                _("I'd never let anyone else do this. But you want my mouth, so... it's yours."),
                            ]
                        elif _has_hc and _has_hc_cum:
                            _atm_pre_pool = [
                                _("I hate the taste of cum... so shove it deep and cum fast. Don't give me time to think."),
                                _("You know I hate cum. Fine. Just make it rough so I'm not thinking about the taste."),
                            ]
                        elif _has_hc:
                            _atm_pre_pool = [
                                _("From my ass to my mouth? ...You're nasty. Fine, do it."),
                                _("You know where that's been, right? ...Whatever, I can handle it."),
                                _("That's disgusting... but kind of hot. Okay."),
                            ]
                        elif girl.has_trait("cute_sex"):
                            _atm_pre_pool = [
                                _("You want me to put that in my mouth after... Why would you ask me to do that?"),
                                _("After it was in my... Don't you care about me at all? ...Fine. If it makes you happy."),
                                _("Why would you want me to do that? Why would you want to do that to me? Why would anyone want that? And after you... do you care about me at all?"),
                            ]
                        else:
                            _atm_pre_pool = [
                                _("You know where that's been, right? ...Fine. Do it."),
                                _("From my ass to my mouth? ...I can't believe I'm saying okay."),
                                _("That's... really gross. But okay. Just do it."),
                            ]
                        # Recursion: 2nd+ ATM this session, her trait's own voice (Dialogs/atm_repeat_lines.rpy)
                        _atm_sc = store._atm_session_count
                        if _atm_sc >= 1:
                            _atm_pre_pool = [atm_repeat_line(girl, "pre", _atm_sc)]

                        _atm_pre = _tl(renpy.random.choice(_atm_pre_pool))
                    $ Say_Line(girl, _atm_pre)
                    # ONE registration point for every ATM path (atm_register, this file): counters, Firsts["atm"],
                    # recording tag, achievement and the ATM context. Firsts["cum_mouth"] is written by process_cum().
                    $ atm_register(girl, where="cum_menu_raw")
                    call _cum_in_mouth_via_bj(girl, scene_type) from _call__cum_in_mouth_via_bj_atm
                else:
                    # ATM denied: trait-specific reactions
                    python:
                        _atm_deny = None
                        if girl.has_trait("hate_cum"):
                            _atm_deny_pool = [
                                _("FROM MY ASS?! To my MOUTH?! Are you INSANE?! That's DISGUSTING!"),
                                _("You want me to put THAT in my mouth after it was in my ASS?! ABSOLUTELY NOT!"),
                                _("That is the most revolting thing anyone has ever asked me. NO!"),
                            ]
                        elif girl.has_trait("cute_sex"):
                            _atm_deny_pool = [
                                _("No! Why would you even ask me that? Don't you care about me at all?"),
                                _("After it was in my... How could you even think of asking me to do that?"),
                                _("That's... that's horrible. After everything... I thought you cared about me..."),
                            ]
                        elif girl.has_trait("anal_hater"):
                            _atm_deny_pool = [
                                _("You just put me through that, and NOW you want it in my MOUTH?! No!"),
                                _("I already hated having it back there. You want me to TASTE it too?! Absolutely not!"),
                                _("After what I just went through?! You want to shove it in my face?! NO!"),
                            ]
                        else:
                            _atm_deny_pool = [
                                _("No way. Do you know where that's been? Not in my mouth."),
                                _("Absolutely not. It was just in my ass. That's disgusting."),
                                _("Are you serious? After it was in my ass? No."),
                            ]
                        _atm_deny = _tl(renpy.random.choice(_atm_deny_pool))
                    $ Say_Line(girl, _atm_deny)
                    # hate_cum ATM denial: she's so disgusted she ends the scene
                    if girl.has_trait("hate_cum"):
                        $ Change_Status(girl, "Love", -15)
                        $ Change_Status(girl, "Obed", -5)
                        call _atm_ask_angry_end(girl, scene_type) from _call__atm_ask_angry_end
                    elif not girl.has_trait("anal_hater") and not girl.has_trait("anal_lover") and not girl.has_trait("cute_sex"):
                        # Neutral girl: wipe off compromise — cleans it and proceeds to normal BJ
                        python:
                            _wipe_line = renpy.random.choice([
                                _("Hold on... let me just... there. Okay, we're good."),
                                _("Wait. Give me a second."),
                                _("Just... hold on. Let me take care of that first."),
                            ])
                            Say_Line(girl, _wipe_line)
                        "She grabs a tissue and quickly wipes you off before continuing."
                        $ debug_log("[DEBUG] ATM wipe-off compromise: neutral girl wiped, proceeding to normal BJ")
                        call _cum_in_mouth_via_bj(girl, scene_type) from _call__cum_in_mouth_via_bj_wipeoff
                    else:
                        call PlayerCumMenu_Outside_Penetration(girl, scene_type) from _call_PlayerCumMenu_Outside_Penetration_atm_denied
            else:
                # Normal path (non-anal)
                $ _cum_check = CumPermissionCheck(girl, "cum_in_mouth_ask")
                if _cum_check["accepted"]:
                    $ Say_Line(girl, scene_pick_line("cum_mouth_accepted", scene=scene_type, girl=girl) or _("Go ahead... do it."))
                    call _cum_in_mouth_via_bj(girl, scene_type) from _call__cum_in_mouth_via_bj_penetration
                else:
                    $ Say_Line(girl, scene_pick_line("cum_mouth_denied", scene=scene_type, girl=girl) or _("No way... not in my mouth."))
                    call PlayerCumMenu_Outside_Penetration(girl, scene_type) from _call_PlayerCumMenu_Outside_Penetration_mouth_denied

        "Cum inside":
            if _is_cum_slut or (scene_type in _ANAL_SCENE_TYPES and girl.has_trait("anal_lover")):
                $ set_scene_expression(girl, renpy.random.choice(["ahegao", "ahegao_2"]), blush="3")
            elif _consent not in ("allowed", "changed_mind") and not _girl_requested:
                $ store._cum_forced_surprise = True
            call _cum_dispatch_anim(girl, scene_type) from _call__cum_anim_inside
            if scene_type in _ANAL_SCENE_TYPES:
                "You thrust deep and cum inside her ass."
            else:
                "You thrust deep and cum inside her."
            $ process_cum(girl, scene_type, "inside")

            if store._stealth_condom_removed:
                call _stealth_cream_realization(girl, scene_type) from _call_stealth_cream_real
                return

            if _consent in ("allowed", "changed_mind") or _girl_requested:
                # She consented... post-creampie reaction
                $ _ci_line = _consented_cream_line(girl, scene_type)
                $ Say_Line(girl, _ci_line)
                $ apply_cum_bonuses(girl, "cum_inside_allowed")
            else:
                # No explicit consent -- but check if she WOULD have accepted
                # (same check Warn Her uses). If yes, she's surprised but ok.
                $ _ci_lust = getattr(girl, "Lust", 0)
                if _ci_lust >= 80 and not _is_hate_cum:
                    $ _ci_implicit = CumPermissionCheck(girl, "cum_inside_anal_ask" if scene_type in _ANAL_SCENE_TYPES else "cum_inside_ask")
                else:
                    $ _ci_implicit = {"accepted": False}

                if _ci_implicit["accepted"]:
                    # She would have said yes if asked -- surprised but accepts
                    $ store._creampie_consent = "changed_mind"
                    if _is_cum_slut or (scene_type in _ANAL_SCENE_TYPES and girl.has_trait("anal_lover")):
                        $ set_scene_expression(girl, renpy.random.choice(["ahegao", "ahegao_2"]), blush="3")
                    python:
                        _ci_surprise = {
                            "cum_slut": [
                                _("You didn't even ask... I LOVE that. Do it every time."),
                                _("Mmm... just like that, no warning. Perfect."),
                                _("No warning, no permission... just raw cum inside me. You're perfect."),
                            ],
                            "cum_slut_first": [
                                _("You came inside without... oh. Oh wow. So that's what it feels like..."),
                                _("Wait, did you just... inside? I can feel it. I didn't know it would be this warm..."),
                                _("No warning at all? ...I don't even care. That felt amazing."),
                            ],
                            "cum_slut_new": [
                                _("You didn't even warn me... and I don't even care. That felt so good."),
                                _("Inside, without asking? ...I should be mad. I'm not."),
                                _("No warning... mmm... I think I liked it better that way."),
                            ],
                            "hardcore_sex": [
                                _("You just... went for it. No warning. Damn... I respect that."),
                                _("You didn't even hesitate. Good. That's how it should be."),
                                _("You came inside without a word. That's how a real man does it."),
                            ],
                            "cute_sex": [
                                _("You... you came inside? Without telling me? I... it felt really warm..."),
                                _("W-wait... you finished inside? I didn't say you could... but I don't hate it..."),
                                _("I felt it go in... all warm... you could've warned me but... it's okay..."),
                            ],
                            "_bf": [
                                _("You're cumming inside me without even asking... I should kill you, but it feels too good..."),
                                _("You just came inside someone else's girlfriend without a word... and I let you..."),
                                _("My %(pl)s asks permission for everything. You just cum inside me like you own me... and I love it..."),
                                _("You didn't even ask... you just finished inside me. My %(pl)s would never... oh god..."),
                                _("No warning, no condom, no permission... just your cum inside %(poss)s girlfriend. What is wrong with me..."),
                            ],
                            "_default": [
                                _("You could have warned me... but honestly? I didn't mind."),
                                _("You just came inside without asking? Bold... but I'm not mad."),
                                _("No warning? Really? ...Fine. I'll let it slide this time."),
                                _("You came inside without saying anything... I felt everything. It's fine."),
                            ],
                        }
                        _ci_sl = None
                        if _is_cum_slut:
                            _ci_sl = renpy.random.choice(_ci_surprise[trait_pool_key(girl, "cum_slut", _ci_surprise)])
                        else:
                            for _t in ("hardcore_sex", "cute_sex"):
                                if girl.has_trait(_t):
                                    _ci_sl = renpy.random.choice(_ci_surprise[_t])
                                    break
                        # BF context (not a trait)
                        if _ci_sl is None and hasattr(girl, "has_npc_partner") and girl.has_npc_partner():
                            _ci_sl = _format_partner_line(girl, renpy.random.choice(_ci_surprise["_bf"]))
                        if _ci_sl is None:
                            _ci_sl = renpy.random.choice(_ci_surprise["_default"])
                    $ Say_Line(girl, _ci_sl)
                    $ apply_cum_bonuses(girl, "cum_inside_allowed")

                else:
                    # She would NOT have accepted -- forced creampie
                    # cum_slut / anal_lover+anal skip penalties (handled below with bonuses)
                    $ _ci_anal_lover_anal = scene_type in _ANAL_SCENE_TYPES and girl.has_trait("anal_lover")
                    if not _is_cum_slut and not _ci_anal_lover_anal:
                        $ apply_cum_penalties(girl, "cum_inside_forced", scene_type)
                    $ store._forced_creampie_count += 1

                    if _is_hate_cum:
                        # hate_cum: always furious, immediate end
                        $ store._witness_expression_lock = True
                        $ set_scene_expression(girl, "angry", brows="brows_maniac")
                        $ _cf_line = scene_pick_line("cum_inside_forced", scene=scene_type, girl=girl) or _("What?! I told you not to! You came inside me?!")
                        $ Say_Line(girl, _cf_line)
                        call _hate_cum_angry_end(girl, scene_type) from _call__hate_cum_angry_end

                    elif _is_cum_slut or _ci_anal_lover_anal:
                        # cum_slut: secretly likes it even without consent / anal_lover in anal: she wanted cum in her ass
                        $ _ci_refused = _creampie_was_refused()
                        $ store._creampie_consent = "allowed"
                        $ apply_cum_bonuses(girl, "cum_inside_allowed")
                        $ _ci_line = _cream_liked_line(girl, scene_type, _ci_refused)
                        $ Say_Line(girl, _ci_line)

                    elif _ci_lust >= 90:
                        # High lust: too close to orgasm to stop... angry but keeps going
                        # She'll end the scene after she cums
                        $ _lust_lines = [ \
                            _("Son of a bitch! I can't stop nowww, I'm almost cumming...!"), \
                            _("You asshole! I told you not to... ngh... but I'm so close... fuck!"), \
                            _("Are you serious?! I... ahhh... god damn it, I can't stop now...!"), \
                            _("You came inside me?! I'm gonna... nnh... I hate you... but don't stop...!"), \
                        ]
                        $ Say_Line(girl, _tl(renpy.random.choice(_lust_lines)))
                        $ Change_Status(girl, "Love", -30)
                        $ store._forced_creampie_end_after_orgasm = True

                    else:
                        # Normal girl, first forced creampie... furious, scene ends
                        $ store._witness_expression_lock = True
                        $ set_scene_expression(girl, "angry", brows="brows_maniac")
                        $ _cf_line = scene_pick_line("cum_inside_forced", scene=scene_type, girl=girl) or _("What?! I told you not to! You came inside me?!")
                        $ Say_Line(girl, _cf_line)
                        call _forced_creampie_angry_end(girl, scene_type) from _call__forced_creampie_angry_end

        "Warn her" if not store._stealth_condom_removed:
            call _cum_warn_her(girl, scene_type, _consent) from _call__cum_warn_her

        "Ask to cum inside" if not store._stealth_condom_removed:
            # If she already consented, skip the check
            if _consent in ("allowed", "changed_mind") or _girl_requested:
                $ _ci_line = scene_pick_line("cum_inside_accepted", scene=scene_type, girl=girl) or _("Yes... do it inside me.")
                $ Say_Line(girl, _ci_line)
                if _is_cum_slut or (scene_type in _ANAL_SCENE_TYPES and girl.has_trait("anal_lover")):
                    $ set_scene_expression(girl, renpy.random.choice(["ahegao", "ahegao_2"]), blush="3")
                call _cum_dispatch_anim(girl, scene_type) from _call__cum_anim_ask_inside_ok
                "You thrust deep and cum inside her."
                $ process_cum(girl, scene_type, "inside")
                $ apply_cum_bonuses(girl, "cum_inside_allowed")
                $ _cr_line = _consented_cream_line(girl, scene_type)
                $ Say_Line(girl, _cr_line)
            else:
                # She said no or blocked... stat-based check
                $ _cum_check = CumPermissionCheck(girl, "cum_inside_anal_ask" if scene_type in _ANAL_SCENE_TYPES else "cum_inside_ask")
                if _cum_check["accepted"]:
                    python:
                        _ntr_cream_gate = getattr(store, "_ntr_creampie_gate_result", None)
                    if _ntr_cream_gate == "guilty_allow":
                        $ _ntr_say_boundary_line(girl, _NTR_GIRL_GUILTY_CREAMPIE)
                    $ _ci_line = scene_pick_line("cum_inside_accepted", scene=scene_type, girl=girl) or _("I... okay. Do it. Inside me.")
                    $ Say_Line(girl, _ci_line)
                    $ store._creampie_consent = "changed_mind"
                    if _is_cum_slut or (scene_type in _ANAL_SCENE_TYPES and girl.has_trait("anal_lover")):
                        $ set_scene_expression(girl, renpy.random.choice(["ahegao", "ahegao_2"]), blush="3")
                    call _cum_dispatch_anim(girl, scene_type) from _call__cum_anim_ask_inside_changed
                    "You thrust deep and cum inside her."
                    $ process_cum(girl, scene_type, "inside")
                    $ apply_cum_bonuses(girl, "cum_inside_allowed")
                    $ _cr_line = _consented_cream_line(girl, scene_type)
                    $ Say_Line(girl, _cr_line)
                else:
                    python:
                        _ntr_cream_gate = getattr(store, "_ntr_creampie_gate_result", None)
                    if _ntr_cream_gate == "respect":
                        $ _ntr_say_boundary_line(girl, _NTR_GIRL_DENY_CREAMPIE)
                    else:
                        $ _ci_line = scene_pick_line("cum_inside_denied", scene=scene_type, girl=girl) or _("No... pull out, please. I told you.")
                        $ Say_Line(girl, _ci_line)
                    python:
                        _fin_cream_ok = _can_financial_extra(girl, "creampie")
                        _fin_cream_price = _calc_financial_extra_price(girl, "creampie") if _fin_cream_ok else 0
                        _fin_cream_afford = _fin_cream_ok and store.Player.cash >= _fin_cream_price
                    menu:
                        "Offer extra for creampie" if _fin_cream_afford:
                            $ set_scene_expression(girl, "surprised")
                            $ Say_Player(_("What if I pay extra to cum inside?"))
                            python:
                                _pp_here = _is_partner_present(girl)[0] if hasattr(girl, "has_npc_partner") and girl.has_npc_partner() else False
                                if _pp_here:
                                    set_scene_expression(girl, None, eyes="eyes_side", brows="brows_confused", mouth="mouth_serious")
                                else:
                                    set_scene_expression(girl, "worried")
                            $ Say_Line(girl, _fin_line(girl, "midscene_creampie_paid", fmt={"price": _fin_cream_price}, tk=_fin_extra_trait_key(girl, "creampie")))
                            menu:
                                "Pay $[_fin_cream_price]":
                                    $ _financial_pay(girl, _fin_cream_price)
                                    $ store._financial_extras_paid["creampie"] = True
                                    $ store._creampie_consent = "allowed"
                                    if getattr(store, "_recording_active", False):
                                        $ unlock_achievement("expensive_pie")
                                    if _is_cum_slut or (scene_type in _ANAL_SCENE_TYPES and girl.has_trait("anal_lover")):
                                        $ set_scene_expression(girl, renpy.random.choice(["ahegao", "ahegao_2"]), blush="3")
                                    else:
                                        $ set_scene_expression(girl, "sad")
                                    call _cum_dispatch_anim(girl, scene_type) from _call__cum_anim_fin_creampie
                                    "You cum inside her."
                                    $ process_cum(girl, scene_type, "inside")
                                    $ apply_cum_bonuses(girl, "cum_inside_allowed")
                                "Never mind":
                                    $ set_scene_expression(girl, "normal")
                                    call _cum_dispatch_outside_freeze(girl, scene_type) from _call__cum_freeze_fin_nevermind
                                    "You pull out and cum outside."
                                    $ process_cum(girl, scene_type, "outside")
                                    $ apply_cum_bonuses(girl, "cum_outside")
                        "Pull out":
                            call _cum_dispatch_outside_freeze(girl, scene_type) from _call__cum_freeze_ask_denied
                            "You pull out and cum outside."
                            $ process_cum(girl, scene_type, "outside")
                            $ apply_cum_bonuses(girl, "cum_outside")
                        "Cum inside":
                            $ _fi_anal_lover_anal = scene_type in _ANAL_SCENE_TYPES and girl.has_trait("anal_lover")
                            if _is_cum_slut or _fi_anal_lover_anal:
                                $ set_scene_expression(girl, renpy.random.choice(["ahegao", "ahegao_2"]), blush="3")
                            else:
                                $ store._cum_forced_surprise = True
                            call _cum_dispatch_anim(girl, scene_type) from _call__cum_anim_ask_inside_force
                            "You cum inside her anyway."
                            $ process_cum(girl, scene_type, "inside")
                            if not _is_cum_slut and not _fi_anal_lover_anal:
                                $ apply_cum_penalties(girl, "cum_inside_forced", scene_type)
                            $ store._forced_creampie_count += 1

                            if _is_cum_slut:
                                # cum_slut: secretly happy even after denial (she just said no: refused=True)
                                $ _ci_line = _cream_liked_line(girl, scene_type, True)
                                $ Say_Line(girl, _ci_line)
                            elif _fi_anal_lover_anal:
                                # anal_lover in anal: she wanted cum in her ass
                                $ store._creampie_consent = "allowed"
                                $ apply_cum_bonuses(girl, "cum_inside_allowed")
                                $ _ci_line = _cream_liked_line(girl, scene_type, True)
                                $ Say_Line(girl, _ci_line)
                            elif getattr(girl, "Lust", 0) >= 90:
                                # High lust: too overwhelmed... angry but can't stop
                                $ _lust_lines = [ \
                                    _("You ASSHOLE! I said no TWICE! I... ngh... f-fuck, I'm too close...!"), \
                                    _("I can't believe you... I told you NO... but I'm about to... ahhh...!"), \
                                ]
                                $ Say_Line(girl, _tl(renpy.random.choice(_lust_lines)))
                                $ Change_Status(girl, "Love", -50)
                                $ store._forced_creampie_end_after_orgasm = True
                            else:
                                # She said no TWICE and he forced it... always furious, scene ends
                                $ store._witness_expression_lock = True
                                $ set_scene_expression(girl, "angry", brows="brows_maniac")
                                $ _cf_line = scene_pick_line("cum_inside_forced", scene=scene_type, girl=girl) or _("You came inside me?! I told you TWICE!")
                                $ Say_Line(girl, _cf_line)
                                if _is_hate_cum:
                                    call _hate_cum_angry_end(girl, scene_type) from _call__hate_cum_angry_end_1
                                else:
                                    call _forced_creampie_angry_end(girl, scene_type) from _call__forced_creampie_angry_end_1

    return

# ------------------------------------------------------------
# Warn her... player tells her he's about to cum, she decides.
# hate_cum: NEVER allows inside via warn.
# Others: needs Lust >= 80 AND CumPermissionCheck to accept.
# ------------------------------------------------------------
label _cum_warn_her(girl, scene_type, consent):

    "You tell her you're about to cum."

    $ _is_hate_cum = girl.has_trait("hate_cum")
    $ _is_cum_slut = girl.has_trait("cum_slut")
    $ _lust = getattr(girl, "Lust", 0)

    # --- hate_cum: ALWAYS says pull out, no exceptions ---
    if _is_hate_cum:
        python:
            _warn_no_hc = [
                _("Pull out! NOW! Don't even think about it!"),
                _("I told you NO! Pull out right now!"),
                _("Are you crazy?! Pull out! I mean it!"),
                _("Don't you DARE finish inside me!"),
            ]
            _wl = _tl(renpy.random.choice(_warn_no_hc))
        $ _wl = fert_override_line(girl, scene_type, "inside_no", _wl) if callable(globals().get("fert_override_line", None)) else _wl
        $ Say_Line(girl, _wl)
        call _cum_dispatch_outside_freeze(girl, scene_type) from _call__cum_freeze_warn_hate
        "You pull out and cum outside."
        $ process_cum(girl, scene_type, "outside")
        $ apply_cum_bonuses(girl, "cum_outside")

    # --- cum_slut: ALWAYS says inside (a veteran one makes the decision for both of you) ---
    elif _is_cum_slut and trait_is_veteran(girl, "cum_slut"):
        python:
            _warn_cs = [
                _("Yes! Don't you dare pull out!"),
                _("Finally! Give it all to me... inside!"),
                _("I've been waiting for this... cum inside me!"),
            ]
            _wl = _tl(renpy.random.choice(_warn_cs))
        $ _wl = fert_override_line(girl, scene_type, "inside_ok", _wl) if callable(globals().get("fert_override_line", None)) else _wl
        $ Say_Line(girl, _wl)
        python:
            _cs_narr = {
                "cowgirl": [
                    _("She speeds up, grinding harder, a satisfied smile on her face. She's not letting you go anywhere."),
                    _("Her hips slam down as she locks eyes with you, making it clear pulling out isn't an option."),
                    _("She presses herself down, taking you as deep as she can, not giving you any choice."),
                ],
                "reverse_cowgirl": [
                    _("She pushes back against you, keeping you buried deep. She looks over her shoulder with a grin."),
                    _("She reaches back and grabs your hip, pulling you closer. There's no pulling out now."),
                    _("She arches her back and tightens around you, trapping you inside with a breathless laugh."),
                ],
                "_default": [
                    _("She wraps her legs around you and pulls you deeper, smiling. She's not giving you any option."),
                    _("She locks her ankles behind you, keeping you pressed against her. You're not going anywhere."),
                    _("She grabs your hips and pulls you closer with a grin, making the decision for both of you."),
                ],
            }
            _narr_pool = _cs_narr.get(scene_position(scene_type), _cs_narr["_default"])   # the pose, in either hole
            _narr = _tl(renpy.random.choice(_narr_pool))
        "[_narr]"
        call _cum_dispatch_anim(girl, scene_type) from _call__cum_anim_warn_cs
        $ process_cum(girl, scene_type, "inside")
        $ apply_cum_bonuses(girl, "cum_inside_allowed")
        $ _cr_line = _consented_cream_line(girl, scene_type)
        $ Say_Line(girl, _cr_line)

    # --- Consent already allowed (not hate_cum, not a veteran cum_slut). A cum_slut still discovering it
    #     (trait_is_new) asks for it here instead: she wants it inside, but she does not trap him ---
    elif consent in ("allowed", "changed_mind") or _is_cum_slut:
        if _is_cum_slut:
            $ store._creampie_consent = "allowed"
        python:
            _warn_accept = {
                "cum_slut_first": [
                    _("Inside... please. I want to know what it feels like."),
                    _("Don't pull out... I want to feel it. I want to know."),
                    _("Inside me... I've been wondering about this for so long..."),
                ],
                "cum_slut_new": [
                    _("Don't pull out... I want to feel you finish inside me."),
                    _("Inside... yes. Please. I want it."),
                    _("Stay in... I want all of it."),
                ],
                "hardcore_sex": [
                    _("Grab me tight and cum deep inside me... don't you dare hold back."),
                    _("Cum and keep going. We're not stopping now. Deeper. Harder."),
                    _("Slam it all the way in and fill me up. Every. Last. Drop."),
                    _("Push it deep and don't pull out until you're completely empty inside me."),
                    _("Harder! Cum inside me and don't stop fucking me!"),
                ],
                "cute_sex": [
                    _("Push it all the way in and fill me up... I want every drop inside me..."),
                    _("Hold me tight and let it all out deep inside... don't pull away..."),
                    _("I want to feel you cum inside me... all of it... nice and deep..."),
                    _("Stay inside me... I want to feel every bit of you filling me up..."),
                    _("Go as deep as you can... I want all of you inside me..."),
                ],
                "_default": [
                    _("Deep inside... hold me tight and don't pull out until everything is inside me."),
                    _("Inside! Don't stop now, I don't want to stop!"),
                    _("All the way in... give me everything. I want to feel you fill me up."),
                    _("Cum deep inside me... don't hold back. I want it all."),
                    _("Push it in and don't pull out... I want every last drop inside me."),
                ],
            }
            _wl = None
            _wa_keys = (trait_discovery_keys(girl, "cum_slut") if _is_cum_slut else []) + [_t for _t in ("hardcore_sex", "cute_sex") if girl.has_trait(_t)]
            for _k in _wa_keys:
                if _k in _warn_accept:
                    _wl = renpy.random.choice(_warn_accept[_k])
                    break
            if _wl is None:
                _wl = renpy.random.choice(_warn_accept["_default"])
            print("[CUM] warn her (raw): %s consent=%s keys=%s" % (girl.gid, consent, _wa_keys))
        $ _wl = fert_override_line(girl, scene_type, "inside_ok", _wl) if callable(globals().get("fert_override_line", None)) else _wl
        $ Say_Line(girl, _wl)
        python:
            _ca_narr = {
                "cowgirl": [
                    _("She keeps riding, her pace steady and deliberate as you finish inside her."),
                    _("She grinds down one last time, keeping you deep as you release."),
                ],
                "reverse_cowgirl": [
                    _("She stays in place, arching her back as you thrust deep and finish inside her."),
                    _("She holds still, pressing back against you as you empty yourself inside her."),
                ],
                "_default": [
                    _("She pulls you close, holding you tight as you thrust deep and finish inside her."),
                    _("She holds onto you, her breathing heavy as you cum inside her."),
                    _("You press deep and release inside her. She holds you there, not letting go."),
                ],
            }
            _narr = _tl(renpy.random.choice(_ca_narr.get(scene_position(scene_type), _ca_narr["_default"])))  # translated when picked: a "[var]" line never translates what it interpolates
        "[_narr]"
        call _cum_dispatch_anim(girl, scene_type) from _call__cum_anim_warn_consent
        $ process_cum(girl, scene_type, "inside")
        $ apply_cum_bonuses(girl, "cum_inside_allowed")
        $ _cr_line = _consented_cream_line(girl, scene_type)
        $ Say_Line(girl, _cr_line)

    # --- Consent denied: needs high Lust AND stat check ---
    else:
        # Gate 1: Lust must be >= 80
        # Gate 2: CumPermissionCheck must pass
        if _lust >= 80:
            $ _warn_check = CumPermissionCheck(girl, "cum_inside_ask")
        else:
            $ _warn_check = {"accepted": False}

        if _warn_check["accepted"]:
            # High Lust + stats passed... she gives in
            python:
                _warn_yes = {
                    "cute_sex": [
                        _("I... I can't think straight... okay. Do it inside."),
                        _("My body is saying yes... go ahead. Inside me."),
                    ],
                    "_default": [
                        _("I... god, I'm so turned on... fine. Do it. Inside."),
                        _("Forget what I said... just finish inside me."),
                        _("I can't hold back anymore... cum inside."),
                    ],
                }
                _wl = None
                if girl.has_trait("cute_sex"):
                    _wl = renpy.random.choice(_warn_yes["cute_sex"])
                if _wl is None:
                    _wl = renpy.random.choice(_warn_yes["_default"])
            $ _wl = fert_override_line(girl, scene_type, "inside_ok", _wl) if callable(globals().get("fert_override_line", None)) else _wl
            $ Say_Line(girl, _wl)
            $ store._creampie_consent = "changed_mind"
            python:
                _cm_narr = {
                    "cowgirl": [
                        _("Her resistance fades as lust takes over. She grinds down, pulling you deeper as you finish inside her."),
                        _("She hesitates for a moment, then her hips take over, riding you through your climax."),
                    ],
                    "reverse_cowgirl": [
                        _("She grips the sheets, torn between stopping you and wanting more. Her body wins. You cum deep inside her."),
                        _("She tenses up, but doesn't pull away. You push deep and finish inside her as she gasps."),
                    ],
                    "_default": [
                        _("She hesitates, but her body betrays her. She pulls you closer as you finish deep inside her."),
                        _("For a moment she almost stops you, but then wraps herself around you, giving in completely."),
                        _("Her grip tightens as she lets go of her last resistance, holding you inside her as you cum."),
                    ],
                }
                _narr = _tl(renpy.random.choice(_cm_narr.get(scene_position(scene_type), _cm_narr["_default"])))  # translated when picked: a "[var]" line never translates what it interpolates
            "[_narr]"
            call _cum_dispatch_anim(girl, scene_type) from _call__cum_anim_warn_changed
            $ process_cum(girl, scene_type, "inside")
            $ apply_cum_bonuses(girl, "cum_inside_allowed")
            $ _cr_line = _consented_cream_line(girl, scene_type)
            $ Say_Line(girl, _cr_line)
        else:
            # Lust too low or stats not enough... she says no
            python:
                _warn_no = {
                    "cute_sex": [
                        _("No! Please pull out... I'm not ready for that!"),
                        _("Pull out, please! Not inside!"),
                    ],
                    "_default": [
                        _("Pull out! I said no!"),
                        _("Don't you dare! Pull out!"),
                        _("No! Outside! Now!"),
                    ],
                }
                _wl = None
                if girl.has_trait("cute_sex"):
                    _wl = renpy.random.choice(_warn_no["cute_sex"])
                if _wl is None:
                    _wl = renpy.random.choice(_warn_no["_default"])
            $ _wl = fert_override_line(girl, scene_type, "inside_no", _wl) if callable(globals().get("fert_override_line", None)) else _wl
            $ Say_Line(girl, _wl)
            call _cum_dispatch_outside_freeze(girl, scene_type) from _call__cum_freeze_warn_denied
            "You pull out and cum outside."
            $ process_cum(girl, scene_type, "outside")
            $ apply_cum_bonuses(girl, "cum_outside")

    return

# ------------------------------------------------------------
# Warn her... ORAL (HJ / BJ / TJ)
# Girl decides where based on traits and preferences.
# hate_cum: always outside (far away)
# cum_slut: opens mouth and swallows
# Others: mouth if high stats, outside otherwise
# ------------------------------------------------------------
label _cum_warn_her_oral(girl, scene_type):

    "You tell her you're about to cum."

    $ _is_hate_cum = girl.has_trait("hate_cum")
    $ _is_cum_slut = girl.has_trait("cum_slut")

    # BJ: pause animation for dialogue (mirror tease speed-0 pattern)
    if scene_type == "bj":
        python:
            _saved_bj_warn = {
                "bj_speed": store.bj_speed,
                "bj_eyes": store.bj_eyes,
                "bj_brows": store.bj_brows,
                "bj_idle_mouth": store.bj_idle_mouth,
            }
            _bj_pause_forcing()
            print("[BJ_WARN_ORAL] pause: saving speed=%d" % store.bj_speed)
        call BJ_ApplySpeed(girl, 0) from _call_BJ_AS_warn_oral_pause
        python:
            if _gsc(girl.gid, 'has_head_normal', False, pose='blowjob'):
                store._bj_head_normal = True
                _pov_bj = _gsc(girl.gid, 'pov_overlay', False, pose='blowjob')
                _bj_head_z = 10058 if _pov_bj else 10015
                _bj_mouth = getattr(store, 'bj_idle_mouth', 'mouth_sucking')
                if _bj_mouth in ('mouth_sucking', 'mouth_none', ''):
                    _bj_mouth = 'mouth_normal'
                renpy.show(
                    "%s blowjob_head head_normal %s" % (girl.gid, _bj_mouth),
                    tag="%s_bj_head" % girl.gid,
                    at_list=[bj_get_head_transform(0)],
                    zorder=_bj_head_z
                )

    if _is_hate_cum:
        python:
            _warn_oral_hc = [
                _("Get it away from me! Just... aim somewhere else!"),
                _("Don't point that at me! Just let it go away from my face!"),
                _("Pull away! I don't want it anywhere near me!"),
            ]
            _wl = _tl(renpy.random.choice(_warn_oral_hc))
        $ Say_Line(girl, _wl)
        if scene_type == "bj":
            $ store.bj_speed = _saved_bj_warn["bj_speed"]
            call BJ_CumAnim(girl) from _call_BJ_CumAnim_warn_hc
        elif scene_type == "tj":
            call TJ_CumAnim(girl) from _call_TJ_CumAnim_warn_hc
        $ process_cum(girl, scene_type, "away")
        $ apply_cum_bonuses(girl, "cum_outside")

    elif _is_cum_slut:
        python:
            # her choice when warned (never forced): the veteran demands it, a first-timer asks to try it
            _warn_oral_cs = {
                "cum_slut": [
                    _("In my mouth! Give it to me! I want to taste it all!"),
                    _("Don't waste it... put it in my mouth!"),
                    _("I want every last drop... cum in my mouth!"),
                ],
                "cum_slut_first": [
                    _("In my mouth... please. I want to know how it tastes."),
                    _("Can I... taste it? Please?"),
                    _("Wait... let me try. In my mouth."),
                ],
                "cum_slut_new": [
                    _("In my mouth... please. I want to taste it."),
                    _("Let me have it... in my mouth."),
                    _("Don't pull away... I want it."),
                ],
            }
            _wl = _tl(renpy.random.choice(_warn_oral_cs[trait_pool_key(girl, "cum_slut", _warn_oral_cs)]))
        $ Say_Line(girl, _wl)
        if scene_type == "bj":
            $ store.bj_speed = _saved_bj_warn["bj_speed"]
            call BJ_CumAnim(girl) from _call_BJ_CumAnim_warn_cs
            $ process_cum(girl, scene_type, "mouth")
            $ apply_cum_bonuses(girl, "cum_in_mouth_allowed")
            call _bj_mouth_cum_reaction(girl, False) from _call__bj_mcr_warn_cs
        elif scene_type in ("hj", "tj", "fj"):
            call _cum_in_mouth_via_bj(girl, scene_type) from _call__cum_in_mouth_via_bj_warn_cs
        else:
            $ process_cum(girl, scene_type, "mouth")
            $ apply_cum_bonuses(girl, "cum_in_mouth_allowed")

    else:
        # Check if she'd accept mouth via stats
        $ _mouth_check = CumPermissionCheck(girl, "cum_in_mouth_ask")
        if _mouth_check["accepted"]:
            python:
                _warn_oral_yes = {
                    "cute_sex": [
                        _("O-okay... in my mouth. I'll try to swallow..."),
                        _("I'll take it... just don't make a mess..."),
                    ],
                    "hardcore_sex": [
                        _("In my mouth. I can handle it."),
                        _("Give it to me. My mouth, now."),
                    ],
                    "camera_lover": [
                        _("Cum on my face! Make it look good!"),
                        _("Give me a facial... I want to see it!"),
                    ],
                    "_default": [
                        _("In my mouth... I guess. Just warn me next time earlier."),
                        _("Okay... do it. In my mouth."),
                        _("Go ahead... I'll take it."),
                    ],
                }
                _wl = None
                for _t in ("cute_sex", "hardcore_sex", "camera_lover"):
                    if girl.has_trait(_t):
                        _wl = renpy.random.choice(_warn_oral_yes[_t])
                        break
                if _wl is None:
                    _wl = renpy.random.choice(_warn_oral_yes["_default"])

            $ Say_Line(girl, _wl)

            # camera_lover prefers face over mouth
            if girl.has_trait("camera_lover"):
                if scene_type == "bj":
                    $ store.bj_speed = _saved_bj_warn["bj_speed"]
                    call BJ_CumAnim(girl) from _call_BJ_CumAnim_warn_face
                elif scene_type == "tj":
                    call TJ_CumAnim(girl) from _call_TJ_CumAnim_warn_face
                elif scene_type == "fj":
                    call _cum_dispatch_anim(girl, scene_type) from _call__cum_anim_warn_face_fj
                    $ _ft_add_cum("face")
                $ process_cum(girl, scene_type, "face")
                $ apply_cum_bonuses(girl, "cum_outside")
            else:
                if scene_type == "bj":
                    $ store.bj_speed = _saved_bj_warn["bj_speed"]
                    call BJ_CumAnim(girl) from _call_BJ_CumAnim_warn_mouth
                    $ process_cum(girl, scene_type, "mouth")
                    $ apply_cum_bonuses(girl, "cum_in_mouth_allowed")
                    call _bj_mouth_cum_reaction(girl, False) from _call__bj_mcr_warn_mouth
                elif scene_type in ("hj", "tj", "fj"):
                    call _cum_in_mouth_via_bj(girl, scene_type) from _call__cum_in_mouth_via_bj_warn_mouth
                else:
                    $ process_cum(girl, scene_type, "mouth")
                    $ apply_cum_bonuses(girl, "cum_in_mouth_allowed")
        else:
            python:
                _warn_oral_no = {
                    "cute_sex": [
                        _("N-not in my mouth... just... aim down, please?"),
                        _("Not my face either! Just... on my chest or something..."),
                    ],
                    "public_shy": [
                        _("Not on me! What if someone sees the mess?!"),
                        _("Just do it away from me... please!"),
                    ],
                    "_default": [
                        _("Not in my mouth! Just... anywhere else."),
                        _("Pull back! I don't want it on my face either."),
                        _("Just let it go... but not on me."),
                    ],
                }
                _wl = None
                for _t in ("cute_sex", "public_shy"):
                    if girl.has_trait(_t):
                        _wl = renpy.random.choice(_warn_oral_no[_t])
                        break
                if _wl is None:
                    _wl = renpy.random.choice(_warn_oral_no["_default"])

            $ Say_Line(girl, _wl)

            # She directs it to tits or outside based on preference
            if scene_type == "bj":
                $ store.bj_speed = _saved_bj_warn["bj_speed"]
                call BJ_CumAnim(girl) from _call_BJ_CumAnim_warn_deny
            elif scene_type == "tj":
                call TJ_CumAnim(girl) from _call_TJ_CumAnim_warn_deny
            if scene_type == "tj":
                $ process_cum(girl, scene_type, "tits")
            else:
                $ process_cum(girl, scene_type, "outside")
            $ apply_cum_bonuses(girl, "cum_outside")

    return

# ------------------------------------------------------------
# Warn her... CONDOM (Penetration with condom on)
# Girl decides based on traits. She won't feel cum directly
# so the decision is: keep condom on, or ask to remove it.
# hate_cum: always keep condom on
# cum_slut: asks to remove it and cum inside raw
# Others: keep condom unless high stats allow
# ------------------------------------------------------------
label _cum_warn_her_condom(girl, scene_type):

    "You tell her you're about to cum."

    $ _is_hate_cum = girl.has_trait("hate_cum")
    $ _is_cum_slut = girl.has_trait("cum_slut")

    if _is_hate_cum:
        python:
            _warn_cond_hc = [
                _("Good. Keep the condom on. That's what it's there for."),
                _("Don't you dare take that off. Finish in the condom."),
                _("Inside the condom. Obviously. Don't even think about removing it."),
            ]
            _wl = _tl(renpy.random.choice(_warn_cond_hc))
        $ Say_Line(girl, _wl)
        "You finish inside the condom."
        $ process_cum(girl, scene_type, "condom")
        $ apply_cum_bonuses(girl, "cum_outside")

    elif _is_cum_slut and trait_is_veteran(girl, "cum_slut"):
        python:
            _warn_cond_cs = [
                _("TAKE IT OFF! I was SO wrong about the condom! I NEED your cum inside me!"),
                _("Rip that thing off and fill me up! I can't finish with this plastic between us!"),
                _("Forget the condom! I NEED to feel you raw! Every drop INSIDE me! NOW!"),
                _("I don't care what I said before! TAKE IT OFF! I need to feel you cum inside me!"),
                _("GET RID OF IT! I was an idiot for asking! I need the real thing! CUM INSIDE ME!"),
            ]
            _wl = _tl(renpy.random.choice(_warn_cond_cs))
        $ Say_Line(girl, _wl)
        $ _on_condom_removed(girl, skip_hide=_cum_skip_hide(scene_type))
        $ store._creampie_consent = "allowed"
        call _cum_dispatch_condom_remove(girl, scene_type) from _call__cum_condom_remove_warn_cumslut
        call _cum_dispatch_anim(girl, scene_type) from _call__cum_anim_warn_cumslut
        "You rip the condom off and cum deep inside her."
        $ process_cum(girl, scene_type, "condom_removed_inside")
        $ apply_cum_bonuses(girl, "condom_removed_allowed")

    else:
        # (a cum_slut still discovering it lands here: she asks like anyone else, she does not demand)
        # If she already denied condom removal this scene, don't offer again
        $ _already_denied = getattr(store, "_condom_removal_denied", False)
        # Check if she'd allow removal via stats (skip if already denied)
        $ _rem_check = CumPermissionCheck(girl, "cum_remove_condom_ask") if not _already_denied else {"accepted": False}
        if _rem_check["accepted"]:
            python:
                _warn_cond_yes = {
                    "cum_slut_first": [
                        _("Take it off... please. I want to know what it feels like without it."),
                        _("Can we... take it off? I want to feel you finish. For real."),
                        _("Off... please. I've been wondering what it's like."),
                    ],
                    "cum_slut_new": [
                        _("Take it off... I want to feel you finish inside me."),
                        _("Please... no condom. I want it inside."),
                        _("Off... I want the real thing. Please."),
                    ],
                    "hardcore_sex": [
                        _("Fuck! Take it off! I was wrong, I need to feel you raw!"),
                        _("Rip it off! I can't take it, I need your cum inside me!"),
                        _("I don't care anymore! Take it off and cum inside me! NOW!"),
                        _("Screw the condom! I want to feel everything! TAKE IT OFF!"),
                    ],
                    "cute_sex": [
                        _("I... I changed my mind. Please take it off. I want to feel you..."),
                        _("I know I said keep it on, but... I want to feel you closer. Please..."),
                        _("Take it off... I was being silly. I want this to be real..."),
                        _("I need to feel you... for real. Please take it off..."),
                    ],
                    "_default": [
                        _("Take the condom off... I was wrong. I need to feel you finish inside me."),
                        _("I can't do this with the condom on. Take it off. I need you raw."),
                        _("Forget what I said before. Take it off. I want to feel everything."),
                        _("I changed my mind. Take it off and cum inside me. I mean it."),
                        _("God, I need you raw. Take it off. I don't care anymore."),
                    ],
                }
                _wl = None
                _wcy_keys = (trait_discovery_keys(girl, "cum_slut") if _is_cum_slut else []) + [_t for _t in ("hardcore_sex", "cute_sex") if girl.has_trait(_t)]
                for _k in _wcy_keys:
                    if _k in _warn_cond_yes:
                        _wl = renpy.random.choice(_warn_cond_yes[_k])
                        break
                if _wl is None:
                    _wl = renpy.random.choice(_warn_cond_yes["_default"])
            $ Say_Line(girl, _wl)
            $ _on_condom_removed(girl, skip_hide=_cum_skip_hide(scene_type))
            $ store._creampie_consent = "allowed"
            call _cum_dispatch_condom_remove(girl, scene_type) from _call__cum_condom_remove_warn_accept
            call _cum_dispatch_anim(girl, scene_type) from _call__cum_anim_warn_accept
            "You rip the condom off and cum deep inside her."
            $ process_cum(girl, scene_type, "condom_removed_inside")
            $ apply_cum_bonuses(girl, "condom_removed_allowed")
        else:
            python:
                _warn_cond_no = {
                    "cute_sex": [
                        _("Keep it on... please. I feel safer this way."),
                        _("Don't remove it! Just finish in the condom."),
                    ],
                    "_default": [
                        _("Keep the condom on. Finish like that."),
                        _("Don't even think about taking it off. Just cum."),
                        _("The condom stays. Go ahead and finish."),
                    ],
                }
                _wl = None
                if girl.has_trait("cute_sex"):
                    _wl = renpy.random.choice(_warn_cond_no["cute_sex"])
                if _wl is None:
                    _wl = renpy.random.choice(_warn_cond_no["_default"])
            $ Say_Line(girl, _wl)
            "You finish inside the condom."
            $ process_cum(girl, scene_type, "condom")
            $ apply_cum_bonuses(girl, "cum_outside")

    return

# ------------------------------------------------------------
# _exit_sex_pose... visually end the sex position (RCG/cowgirl/
# hj/bj/tj) and return the girl to standing. Does NOT reset
# stats or move the girl... just cleans up the visual scene.
# ------------------------------------------------------------
label _exit_sex_pose(girl, scene_type):
    $ debug_log("[DEBUG] _exit_sex_pose: entered, scene_type=%s" % scene_type)
    call _cum_dispatch_end(girl, scene_type) from _call__cum_dispatch_end_angry
    return

# ------------------------------------------------------------
# _player_stops_after_forced_creampie... player chose "Ask her
# to stop" while the forced creampie flag is active. She's
# furious: he came inside her and won't even let her finish.
# ------------------------------------------------------------
label _player_stops_after_forced_creampie(girl, scene_type):
    $ debug_log("[DEBUG] _player_stops_after_forced_creampie: entered, scene_type=%s" % scene_type)
    $ store._witness_expression_lock = True
    call _exit_sex_pose(girl, scene_type) from _call__exit_sex_pose_3

    python:
        _stop_lines = [
            _("STOP?! You came inside me without permission and now you want to STOP?! You won't even let me finish?!"),
            _("Are you SERIOUS?! You cum inside me and then just QUIT?! I didn't even get to cum! You selfish piece of shit!"),
            _("You... you came inside me. I told you not to. And now you're STOPPING?! I was almost there! You absolute ASSHOLE!"),
            _("Oh, so YOU get to finish inside me whenever you want, but I don't even get to CUM?! What kind of person ARE you?!"),
            _("You forced your cum inside me and you can't even have the DECENCY to let me finish?! Get away from me!"),
        ]
    $ Say_Line(girl, _tl(renpy.random.choice(_stop_lines)))

    $ Change_Status(girl, "Love", -100)
    $ Change_Status(girl, "Inbt", -40)
    $ Change_Status(girl, "Obed", 80)

    python:
        _in_her_room = (store.CurrentLocation == GIRL_ROOMS.get(girl.gid, ""))

    if _in_her_room:
        "She's is furious... Maybe not the best decision."
        $ Say_Line(girl, _("Get OUT. I don't ever want to see your face again."))
    else:
        "Her eyes burn with a mix of humiliation and fury you've never seen before."
        $ Say_Line(girl, _("Don't EVER touch me again. I'm done with you."))

    "She's beyond furious. You won't be able to approach her for days."

    $ store._witness_expression_lock = False

    if getattr(girl, '_ntr_violation_pending', False):
        call _angry_end_ntr_confrontation(girl) from _call_aend_ntr_stops_after

    $ force_scene_reset(girl, angry_days=3, reason="forced_creampie_and_stopped")
    jump main_loop

# ------------------------------------------------------------
# ATM ask angry end... hate_cum girl ends the scene over the ASK
# itself. NO cum happened: no aftermath pose, no cum dispatch
# (reusing _hate_cum_angry_end here played "You came inside me?!"
# and processed an orgasm that never was)
# ------------------------------------------------------------
label _atm_ask_angry_end(girl, scene_type):
    $ store._witness_expression_lock = True
    $ set_scene_expression(girl, "angry", brows="brows_maniac")

    "She shoves you off her before you can say another word."

    python:
        _atm_angry_lines = [
            _("We're DONE here. The fact that you would even ask me that..."),
            _("Get off me. Right now. I can't believe you just asked me that."),
            _("No. This is over. Don't you EVER ask me something like that again."),
        ]
        _atm_angry_line = _tl(renpy.random.choice(_atm_angry_lines))
    $ Say_Line(girl, _atm_angry_line)

    $ store._hate_cum_scene_aborted = True

    python:
        # girl_home_loc, not GIRL_ROOMS: a girl who lives off campus (Shion) has no dorm room entry
        _in_her_room = (store.CurrentLocation == girl_home_loc(girl))

    if _in_her_room:
        $ Say_Line(girl, _("Get out of my room. NOW."))
        "She pushes you toward the door."
    else:
        $ Say_Line(girl, _("I'm leaving. Don't follow me."))
        "She grabs her things and storms off."

    $ store._witness_expression_lock = False

    $ force_scene_reset(girl, angry_days=2, reason="atm_request")
    jump main_loop

# ------------------------------------------------------------
# hate_cum angry end... girl is furious, ends scene, leaves
# ------------------------------------------------------------
label _hate_cum_angry_end(girl, scene_type):
    $ store._witness_expression_lock = True
    # Show aftermath pose before angry lines
    call _cum_dispatch_aftermath(girl, scene_type, consented=False) from _call__cum_dispatch_aftermath_hate

    $ set_scene_expression(girl, "angry", brows="brows_maniac")

    python:
        _angry_lines = [
            _("What the HELL is wrong with you?! I told you NO!"),
            _("You came inside me?! After I said NOT to?! Get away from me!"),
            _("I can't believe you just did that! You're disgusting!"),
        ]
        _angry_line = _tl(renpy.random.choice(_angry_lines))
    $ Say_Line(girl, _angry_line)

    $ store._hate_cum_scene_aborted = True

    python:
        _in_her_room = (store.CurrentLocation == GIRL_ROOMS.get(girl.gid, ""))

    if _in_her_room:
        $ Say_Line(girl, _("Get out of my room. NOW."))
        "She pushes you toward the door."
    else:
        $ Say_Line(girl, _("I'm leaving. Don't follow me."))
        "She grabs her things and storms off."

    $ store._witness_expression_lock = False

    if getattr(girl, '_ntr_violation_pending', False):
        call _angry_end_ntr_confrontation(girl) from _call_aend_ntr_hate_cum

    $ force_scene_reset(girl, angry_days=2, reason="forced_creampie")
    jump main_loop

# ------------------------------------------------------------
# forced_creampie_angry_end... forced creampie, girl ends scene
# Picks lines based on how many times it happened this session
# ------------------------------------------------------------
label _forced_creampie_angry_end(girl, scene_type):
    $ store._witness_expression_lock = True
    # Show aftermath pose before angry lines
    call _cum_dispatch_aftermath(girl, scene_type, consented=False) from _call__cum_dispatch_aftermath_forced

    $ set_scene_expression(girl, "angry", brows="brows_maniac")

    python:
        _fc_count = store._forced_creampie_count
        if _fc_count >= 2:
            _angry_lines = [
                _("AGAIN?! You did it AGAIN?! What is WRONG with you?!"),
                _("Twice?! You came inside me TWICE after I said no?! We're done!"),
                _("I told you to stop and you did it AGAIN! Get away from me!"),
            ]
            _love_loss = -80
            _obed_loss = -30
            _angry_days = 2
        else:
            _love_loss = -50
            _obed_loss = -20
            _angry_days = 1

    if _fc_count >= 2:
        $ Say_Line(girl, _tl(renpy.random.choice(_angry_lines)))

    $ Change_Status(girl, "Love", _love_loss)
    $ Change_Status(girl, "Obed", _obed_loss)

    python:
        _in_her_room = (store.CurrentLocation == GIRL_ROOMS.get(girl.gid, ""))

    if _in_her_room:
        $ Say_Line(girl, _("Get out. I don't want to see you right now."))
        "She turns away from you, shaking with anger."
        scene bg Door
        with dissolve
        "The door slams shut behind you."
    else:
        $ Say_Line(girl, _("I'm done. Don't talk to me today."))
        "She grabs her clothes and leaves without looking back."

    $ store._witness_expression_lock = False

    if getattr(girl, '_ntr_violation_pending', False):
        call _angry_end_ntr_confrontation(girl) from _call_aend_ntr_forced_creampie

    $ force_scene_reset(girl, angry_days=_angry_days, reason="forced_creampie")
    jump main_loop

# ------------------------------------------------------------
# forced_condom_removal_angry_end... ripped condom off + came inside
# Specific lines about the condom removal betrayal
# ------------------------------------------------------------
label _forced_condom_removal_angry_end(girl, scene_type):
    $ store._witness_expression_lock = True
    $ set_scene_expression(girl, "angry", brows="brows_maniac")

    python:
        _angry_lines = [
            _("Why would you REMOVE it?! I asked for the condom specifically so you wouldn't cum inside!"),
            _("The condom was there for a REASON! You just ripped it off and came inside me?!"),
            _("Are you out of your MIND?! I wanted the condom ON! Now you came inside me like it's nothing?!"),
            _("I TOLD you to keep it on! You removed it and finished inside me?! Do you have any idea what you just did?!"),
        ]
        # Only true when she really is unprotected (placebo counts as the pill: she believes in it)
        if not getattr(girl, "_on_pill", False):
            _angry_lines.append(_("I'm not on the pill! What the fuck are you thinking?! You took it OFF?!"))
        _angry_line = _tl(renpy.random.choice(_angry_lines))

    $ Say_Line(girl, _angry_line)

    $ Change_Status(girl, "Love", -80)
    $ Change_Status(girl, "Obed", 30)
    $ Change_Status(girl, "Inbt", 40)

    python:
        _in_her_room = (store.CurrentLocation == GIRL_ROOMS.get(girl.gid, ""))

    if _in_her_room:
        $ Say_Line(girl, _("Get out of my room. NOW. Don't come back today."))
        "She pushes you toward the door, trembling with rage."
        scene bg Door
        with dissolve
        "The door slams shut behind you."
    else:
        $ Say_Line(girl, _("I'm leaving. Don't you DARE follow me."))
        "She grabs her clothes and storms off without looking back."

    $ store._witness_expression_lock = False

    if getattr(girl, '_ntr_violation_pending', False):
        call _angry_end_ntr_confrontation(girl) from _call_aend_ntr_condom_removal

    $ force_scene_reset(girl, angry_days=2, reason="forced_condom_removal")
    jump main_loop

# ------------------------------------------------------------
# post_orgasm_forced_creampie_end... she came despite being furious
# about the forced creampie, now the rage catches up
# ------------------------------------------------------------
label _post_orgasm_forced_creampie_end(girl, scene_type):
    $ store._witness_expression_lock = True
    # Transition out of sex pose to standing before angry dialogue
    call _exit_sex_pose(girl, scene_type) from _call__exit_sex_pose_1

    $ set_scene_expression(girl, "angry", brows="brows_maniac")

    python:
        _po_lines = [
            _("Don't you DARE think that orgasm means I forgive you. You came inside me without my permission."),
            _("Just because I came doesn't mean what you did was okay. I told you NOT to cum inside me."),
            _("I hate that I came after what you did. You still came inside me without asking. We're done."),
            _("You think just because I finished, everything is fine?! You came inside me! I said NO!"),
            _("That orgasm changes NOTHING. You violated my trust. Get away from me."),
        ]
    $ Say_Line(girl, _tl(renpy.random.choice(_po_lines)))

    $ Change_Status(girl, "Love", -60)
    $ Change_Status(girl, "Obed", 20)
    $ Change_Status(girl, "Inbt", 30)

    python:
        _in_her_room = (store.CurrentLocation == GIRL_ROOMS.get(girl.gid, ""))

    if _in_her_room:
        $ Say_Line(girl, _("Get out. I need to be alone."))
        "She turns away, still trembling from the orgasm, but her eyes are full of fury."
        scene bg Door
        with dissolve
        "The door slams shut behind you."
    else:
        $ Say_Line(girl, _("I'm leaving. Don't follow me. Don't talk to me."))
        "She gets dressed quickly, legs still shaking, and leaves without looking back."

    $ store._witness_expression_lock = False

    if getattr(girl, '_ntr_violation_pending', False):
        call _angry_end_ntr_confrontation(girl) from _call_aend_ntr_post_orgasm

    $ force_scene_reset(girl, angry_days=2, reason="forced_creampie")
    jump main_loop

# ------------------------------------------------------------
# player_didnt_finish_after_forced_creampie... he came inside her
# without permission, she stayed because Lust was high, and now
# he can't even finish / stops. Ultimate humiliation for her.
# 3 days angry, massive stat loss, but +100 Obed (broken will).
# ------------------------------------------------------------
label _player_didnt_finish_after_forced_creampie(girl, scene_type):
    $ store._witness_expression_lock = True
    # Transition out of sex pose to standing
    call _exit_sex_pose(girl, scene_type) from _call__exit_sex_pose_2

    "Your body gives out. You can't keep going."

    python:
        _rage_lines = [
            _("Are you KIDDING me?! You came inside me WITHOUT my permission, I stayed because I couldn't stop... and you can't even FINISH?!"),
            _("You... you BASTARD. You came inside me when I said no. I let it go because I was close. And now you're DONE?! You couldn't even last?!"),
            _("Let me get this straight. You came inside me. Without consent. I was too far gone to stop. And now you can't even perform?! What the hell is WRONG with you?!"),
            _("You forced yourself inside me, I stayed because my body wouldn't let me stop... and THIS is all you had?! You're pathetic AND an asshole!"),
            _("So you cum inside me without asking, I'm too close to quit, and you run out of STAMINA?! I risked everything and you couldn't even finish the job?!"),
        ]
        _rage_line = _tl(renpy.random.choice(_rage_lines))

    $ Say_Line(girl, _rage_line)

    python:
        _followup_lines = [
            _("I let you get away with the worst thing you could do to me... and you couldn't even make it worth it."),
            _("Your cum is inside me right now. And you couldn't even give me the decency of finishing properly."),
            _("I will NEVER forget this. You used me and you couldn't even commit to it."),
            _("I stayed when I should have left. And THIS is what I get for it."),
        ]

    $ Say_Line(girl, _tl(renpy.random.choice(_followup_lines)))

    # Massive stat consequences
    $ Change_Status(girl, "Love", -120)
    $ Change_Status(girl, "Inbt", -50)
    # She's emotionally broken... obedience skyrockets
    $ Change_Status(girl, "Obed", 100)

    python:
        _in_her_room = (store.CurrentLocation == GIRL_ROOMS.get(girl.gid, ""))

    if _in_her_room:
        "She stares at the ceiling, tears streaming down her face."
        $ Say_Line(girl, _("Get out of my room. Don't come back for a while."))
    else:
        "She gets dressed in silence, hands trembling with rage."
        $ Say_Line(girl, _("Don't talk to me. Don't look at me. Don't even THINK about me."))

    "She's absolutely furious. You won't be able to approach her for days."

    $ store._witness_expression_lock = False

    if getattr(girl, '_ntr_violation_pending', False):
        call _angry_end_ntr_confrontation(girl) from _call_aend_ntr_didnt_finish

    $ force_scene_reset(girl, angry_days=3, reason="forced_creampie_humiliation")
    jump main_loop

# ------------------------------------------------------------
# Player resist forced cum... last-moment menu when girl tries
# to force. Sets store._resist_result: accepted/resisted/failed
# ------------------------------------------------------------
label _player_resist_forced_cum(girl, scene_type):
    $ girl._forced_cum_last_day = store.Day
    menu:
        "Let her have her way":
            $ store._resist_result = "accepted"
        "Try to resist":
            $ _narr = _resist_narration(scene_type, "attempt")
            "[_narr]"
            if _resist_physical_check(scene_type):
                $ _narr = _resist_narration(scene_type, "success")
                "[_narr]"
                $ Say_Line(girl, _tl(renpy.random.choice(RESIST_GIRL_SHOCK)))
                $ store._resist_result = "resisted"
                $ femdom_turn_note(girl, "resisted_forced_cum", scene_type)
                $ unlock_achievement("iron_will")
            else:
                $ _narr = _resist_narration(scene_type, "fail")
                "[_narr]"
                $ store._resist_result = "failed"
    return

# ------------------------------------------------------------
# Submenu for penetration cum-outside
# ------------------------------------------------------------
label PlayerCumMenu_Outside_Penetration(girl, scene_type):
    $ _oc_type = "outside"

    # Position-specific menus (different targets per pose)
    if scene_type in ("reverse_cowgirl", "reverse_cowgirl_anal"):
        $ _oc_targets = _gsc(girl.gid, "cum_outside_targets", None, "rcg")
        if _oc_targets:
            menu:
                "On her face" if "face" in _oc_targets:
                    $ _oc_type = "face"
                "On her ass" if "ass" in _oc_targets:
                    $ _oc_type = "ass"
                "On her back" if "back" in _oc_targets:
                    $ _oc_type = "back"
                "All over her" if "outside" in _oc_targets:
                    $ _oc_type = "outside"
                "Never mind":
                    $ store._cum_menu_cancelled = True
                    return
        else:
            menu:
                "On her face":
                    $ _oc_type = "face"
                "On her ass":
                    $ _oc_type = "ass"
                "On her back":
                    $ _oc_type = "back"
                "All over her":
                    $ _oc_type = "outside"

    elif scene_type in ("doggy", "anal"):
        menu:
            "On her ass":
                $ _oc_type = "ass"
            "On her back":
                $ _oc_type = "back"
            "All over her":
                $ _oc_type = "outside"

    elif scene_type == "cowgirl":
        menu:
            "On her face":
                $ _oc_type = "face"
            "On her legs":
                $ _oc_type = "legs"
            "On her tummy":
                $ _oc_type = "body"
            "All over her":
                $ _oc_type = "outside"

    elif scene_type in ("full_nelson", "full_nelson_anal"):
        menu:
            "On her face":
                $ _oc_type = "face"
            "On her ass":
                $ _oc_type = "ass"
            "On her tits":
                $ _oc_type = "tits"
            "All over her":
                $ _oc_type = "outside"

    elif scene_type in ("laying_down", "laying_anal"):
        menu:
            "On her face":
                $ _oc_type = "face"
            "On her ass":
                $ _oc_type = "ass"
            "On her back":
                $ _oc_type = "back"
            "All over her":
                $ _oc_type = "outside"

    else:
        menu:
            "On her belly":
                $ _oc_type = "belly"
            "On her tits":
                $ _oc_type = "tits"
            "All over her":
                $ _oc_type = "outside"

    # Shared: freeze animation
    call _cum_dispatch_outside_freeze(girl, scene_type) from _call_oc_freeze

    # Face cum clears hiding_face
    if _oc_type == "face" and getattr(store, "hiding_face", False):
        $ store.hiding_face = False

    # Narrate + process cum (pull verb differs by position)
    python:
        # the verb of "You [_oc_pull] and cum on her ...": a [var] is shown as it is, so it is translated HERE
        _oc_pull = _tl(_("lift her off")) if scene_type == "cowgirl" else (_tl(_("pull her off")) if _oc_type == "face" else _tl(_("pull out")))
        _OC_ALL_EXTRAS = {
            "reverse_cowgirl": ["ass", "back", "face"], "reverse_cowgirl_anal": ["ass", "back", "face"],
            "doggy": ["ass", "back"], "anal": ["ass", "back"],
            "cowgirl": ["body", "legs", "face"],
            "full_nelson": ["ass", "boobs", "face"], "full_nelson_anal": ["ass", "boobs", "face"],
            "laying_down": ["ass", "back", "face"], "laying_anal": ["ass", "back", "face"],
        }

    if _oc_type == "face":
        "You [_oc_pull] and cum on her face."
        $ process_cum(girl, scene_type, "face")
    elif _oc_type == "ass":
        "You [_oc_pull] and cum on her ass."
        $ process_cum(girl, scene_type, "ass")
    elif _oc_type == "back":
        "You [_oc_pull] and cum on her back."
        $ process_cum(girl, scene_type, "back")
    elif _oc_type == "tits":
        "You [_oc_pull] and cum on her tits."
        $ process_cum(girl, scene_type, "tits")
    elif _oc_type == "legs":
        "You [_oc_pull] and cum on her legs."
        $ process_cum(girl, scene_type, "outside", ["legs"])
    elif _oc_type == "body":
        "You [_oc_pull] and cum on her tummy."
        $ process_cum(girl, scene_type, "outside")
    elif _oc_type == "belly":
        "You [_oc_pull] and cum on her belly."
        $ process_cum(girl, scene_type, "belly")
    else:
        "You [_oc_pull] and cum all over her."
        $ process_cum(girl, scene_type, "outside", _OC_ALL_EXTRAS.get(scene_type, []))

    # Shared: bonuses + say + resume
    $ apply_cum_bonuses(girl, "cum_outside")
    $ _cum_say_line(girl, _oc_type, scene_type)
    # _post_cum_had_condom: set for every cum by _set_post_cum (scene_tick.rpy), not here

    return

# ============================================================
# ============================================================
# SHARED SLAP — works for BJ, HJ, TJ, etc.
# scene_type: "bj", "hj", "tj" etc
# ============================================================
default _slap_count = 0

label SexScene_Slap(girl, scene_type):
    $ slap_crack()
    $ store._slap_count += 1
    # a FACE slap: never in _session_spanked_girls (the threesome watcher's "my butt is still stinging"; SpankHer
    # adds the girls whose ASS he spanked)

    # Pick random side + expression; hide grab hand on that side
    python:
        _hand_disabled = getattr(store, "_player_hand_disabled", None)
        _slap_side = ("left" if _hand_disabled == "right" else "right") if _hand_disabled else renpy.random.choice(["right", "left"])
        store._slap_hide_hand = _slap_side
        _slap_img = "%s %s_slap_%s" % (girl.gid, scene_type, _slap_side)
        if scene_type == "hj":
            _slap_tf = hj_slap_right_in if _slap_side == "right" else hj_slap_left_in
        elif scene_type == "tj":
            _slap_tf = tj_slap_right_in if _slap_side == "right" else tj_slap_left_in
            # Immediately hide the grab hand on the slap side
            if store.titjob_grab:
                renpy.hide("titjob_grab_%s" % _slap_side)
        else:
            _slap_tf = bj_slap_right_in if _slap_side == "right" else bj_slap_left_in
            # Immediately hide the forcing hand on the slap side
            if store.bj_forcing:
                renpy.hide("%s_bj_forcing_%s" % (girl.gid, _slap_side))
        _slap_eyes, _slap_mouth, _slap_brows = _slap_pick_expression(girl, scene_type)

    # Show hand flying in (above everything including guy layer)
    show expression _slap_img as bj_slap at _slap_tf zorder 10070

    # Wait for hand to reach face
    $ renpy.pause(0.08)

    # Screen shake on impact
    show layer master at bj_slap_shake

    # Blink + change expression on impact
    if scene_type == "bj":
        # BJ: blink then change eyes + brows (mouth managed by sucking/lick)
        $ store.bj_blink = True
        $ renpy.pause(0.10, hard=True)
        python:
            store.bj_blink = False
            store.bj_eyes = _slap_eyes
            store.bj_brows = _slap_brows
            renpy.restart_interaction()
    elif scene_type == "hj":
        # HJ: blink then change eyes + mouth + brows
        $ store.hj_blink = True
        $ renpy.pause(0.12, hard=True)
        python:
            store.hj_blink = False
            state = sprite_state.setdefault(girl.Id, {})
            state["eyes"] = _slap_eyes
            state["mouth"] = _slap_mouth
            state["brows"] = _slap_brows
            _hj_update_attrs(girl)
            _hj_show_sprite(girl)
            renpy.restart_interaction()
    elif scene_type == "tj":
        # TJ: blink (eyes closed) then change expression
        python:
            state = sprite_state.setdefault(girl.Id, {})
            state["eyes"] = "eyes_closed"
        call TITJOB_ApplySpeed(girl, titjob_speed) from _call_TITJOB_ApplySpeed_slap_blink
        $ renpy.pause(0.12, hard=True)
        python:
            state = sprite_state.setdefault(girl.Id, {})
            state["eyes"] = _slap_eyes
            state["mouth"] = _slap_mouth
            state["brows"] = _slap_brows
        call TITJOB_ApplySpeed(girl, titjob_speed) from _call_TITJOB_ApplySpeed_slap
    else:
        python:
            state = sprite_state.setdefault(girl.Id, {})
            state["eyes"] = _slap_eyes
            state["mouth"] = _slap_mouth
            state["brows"] = _slap_brows
            set_girl_sprite(girl, pose=scene_type)
            renpy.restart_interaction()

    # Wait for shake + hand exit
    $ renpy.pause(0.40)
    hide bj_slap
    show layer master

    # Restore hidden grab/forcing hand
    $ store._slap_hide_hand = None
    if scene_type == "tj":
        call TITJOB_ApplySpeed(girl, titjob_speed) from _call_TITJOB_ApplySpeed_slap_restore
    if scene_type == "bj" and store.bj_forcing:
        call BJ_ApplySpeed(girl, bj_speed) from _call_BJ_ApplySpeed_slap_restore

    # Blush based on slap count
    python:
        _blush = 0
        if store._slap_count >= 6:
            _blush = 2
        elif store._slap_count >= 3:
            _blush = 1
        state = sprite_state.setdefault(girl.Id, {})
        state["blush"] = _blush
        renpy.restart_interaction()

    # +1 Obed and +1 Inbt per slap (always)
    $ Change_Status(girl, "Obed", 1)
    $ Change_Status(girl, "Inbt", 1)
    # A cum_slut begs for it like a hardcore girl (SpankHer checks cum_slut first too): no Love loss, no warn / abort
    $ _slap_loves_it = girl.has_trait("hardcore_sex") or girl.has_trait("cum_slut")

    # -1 Love per slap (unless she loves it)
    if not _slap_loves_it:
        $ Change_Status(girl, "Love", -1)

    # Forced BJ: she can't speak clearly, use muffled moans only
    $ _slap_bj_forcing = (scene_type == "bj" and getattr(store, "bj_forcing", False))

    # Trait-specific reactions
    if _slap_loves_it:
        if _slap_bj_forcing:
            $ _slap_line = renpy.random.choice([_("Mmrph!"), _("Glrk!"), _("Nngh!"), _("Hrrm!"), _("Gllk!")])
            call _moan_say(girl, _slap_line, muffled=True) from _call_ms_slap_hc1
        else:
            $ _slap_line = renpy.random.choice([_("Mmh!"), _("Ung!"), _("Ahh~!"), _("Mmm...!"), _("Ngh!")])
            call _moan_say(girl, _slap_line) from _call_ms_slap_hc1b
        $ girl.Lust = min(100, getattr(girl, "Lust", 0) + 8)

        # Every 3 slaps: verbal line (muffled during forced BJ)
        if store._slap_count % 3 == 0:
            if _slap_bj_forcing:
                $ _slap_line = renpy.random.choice([_("HRRM!! MMPH!!"), _("GLLK!! NNGH!!"), _("MMRPH!!")])
                call _moan_say(girl, _slap_line, muffled=True) from _call_ms_slap_hc2
            else:
                python:
                    if store._slap_count <= 3:
                        _hc_verbal = [
                            _("I'm not made of paper, harder!"),
                            _("Harder!"),
                            _("More! More!"),
                            _("Is that all you got?!"),
                            _("Come on, hit me!"),
                        ]
                    else:
                        _hc_verbal = [
                            _("I SAID HARDER!"),
                            _("HIT ME! PUT YOUR BACK INTO IT!"),
                            _("I SAID HARDER, GIVE IT ALL YOU GOT!"),
                            _("COME ON! I BARELY FELT THAT!"),
                            _("THAT'S NOTHING! MORE!"),
                        ]
                $ _slap_line = _tl(renpy.random.choice(_hc_verbal))
                call _moan_say(girl, _slap_line) from _call_ms_slap_hc2b

    elif girl.has_trait("cute_sex"):
        if _slap_bj_forcing:
            $ _slap_line = renpy.random.choice([_("Mmph..."), _("Nnh..."), _("Glk..."), _("Hhn...")])
            call _moan_say(girl, _slap_line, muffled=True) from _call_ms_slap_cute1
        else:
            $ _slap_line = renpy.random.choice([_("Mmh..."), _("Ngh..."), _("Ah..."), _("Uhn...")])
            call _moan_say(girl, _slap_line) from _call_ms_slap_cute1b

        # 2+ slaps: verbal plea — change to sad mouth
        if store._slap_count >= 2 and store._slap_count < 6:
            if _slap_bj_forcing:
                python:
                    if store._slap_count <= 3:
                        _shy_ask_lines = [_("Mmph... nngh... mmh..."), _("Hhn... glk... nnh..."), _("Nnh... mmph... hhn...")]
                    else:
                        _shy_ask_lines = [_("MMPH... NNH... HHN..."), _("GGH... MMRPH... NNH..."), _("HHN... NNH... MMPH...")]
                $ _slap_line = _tl(renpy.random.choice(_shy_ask_lines))
                call _moan_say(girl, _slap_line, muffled=True) from _call_ms_slap_cute2
            else:
                # Sad face for verbal line
                if scene_type == "bj":
                    $ set_scene_expression(girl, None, mouth="mouth_sad")
                elif scene_type == "hj":
                    python:
                        state = sprite_state.setdefault(girl.Id, {})
                        state["mouth"] = "mouth_sad"
                        _hj_update_attrs(girl)
                        _hj_show_sprite(girl)
                python:
                    if store._slap_count <= 3:
                        _shy_ask_lines = [
                            _("Please... don't do that... it hurts..."),
                            _("Can you stop hitting me...? Please..."),
                            _("I don't like that... please stop..."),
                        ]
                    else:
                        _shy_ask_lines = [
                            _("Please... this... this hurts..."),
                            _("I... no... I don't like this..."),
                            _("Stop... you're hurting me..."),
                            _("Why do you keep doing this...?"),
                        ]
                $ _slap_line = _tl(renpy.random.choice(_shy_ask_lines))
                call _moan_say(girl, _slap_line) from _call_ms_slap_cute2b
            $ Change_Status(girl, "Love", -5)

        # 6+ slaps: she ends it, sad for the rest of the day
        if store._slap_count >= 6:
            if scene_type == "bj":
                $ set_scene_expression(girl, None, eyes="eyes_squint_2", mouth="mouth_sad")
            elif scene_type == "hj":
                python:
                    state = sprite_state.setdefault(girl.Id, {})
                    state["eyes"] = "eyes_closed"
                    state["mouth"] = "mouth_sad"
                    _hj_update_attrs(girl)
                    _hj_show_sprite(girl)
            python:
                _shy_stop_lines = [
                    _("I can't do this anymore..."),
                    _("I'm done... I can't take it..."),
                    _("Stop... just stop... please..."),
                ]
            $ _slap_line = _tl(renpy.random.choice(_shy_stop_lines))
            call _moan_say(girl, _slap_line) from _call_ms_slap_cute3
            $ Change_Status(girl, "Love", -20)
            $ girl.Mood = "sad"
            "She pulls away, unable to hold back tears."
            $ force_scene_reset(girl, angry_days=0, reason="slap_abuse")
            $ girl.Mood = "sad"
            jump main_loop

    elif girl.has_trait("femdom") and not trait_is_discovering(girl, "femdom"):
        # A woman who gives the orders does not whine at a slap (tester 2026-10-10: "she could have us
        # killed" and all she said was a mild complaint): cold fury, a priced warning from the second
        # one, and at the fifth she ends the scene on her feet. Any femdom, no role named.
        if _slap_bj_forcing:
            $ _slap_line = renpy.random.choice([_("Mmrph!"), _("Nngh!"), _("Grk...!")])
            call _moan_say(girl, _slap_line, muffled=True) from _call_ms_slap_fd1
        else:
            $ _slap_line = renpy.random.choice([_("...You dare."), _("Tch."), _("...Bold of you.")])
            call _moan_say(girl, _slap_line) from _call_ms_slap_fd1b

        # ONE is the allowance (tester 2026-10-11: a threat repeated is a threat wasted): the first slap
        # buys the warning, the second ends the scene. No re-warns.
        if store._slap_count == 1 and not _slap_bj_forcing:
            python:
                _fd_warn_lines = [
                    _("You get that one. The next will cost you."),
                    _("Careful. Remember who you belong to when this is over."),
                    _("I keep score. You do not want to see the bill."),
                ]
            $ _slap_line = _tl(renpy.random.choice(_fd_warn_lines))
            call _moan_say(girl, _slap_line) from _call_ms_slap_fd2
            $ Change_Status(girl, "Love", -3)

        if store._slap_count >= 2:
            python:
                _fd_stop_lines = [
                    _("Enough. We are done here."),
                    _("That was your last one. Get off me."),
                    _("The lesson is over. Out."),
                ]
            $ _slap_line = _tl(renpy.random.choice(_fd_stop_lines))
            call _moan_say(girl, _slap_line) from _call_ms_slap_fd3
            $ Change_Status(girl, "Love", -10)
            $ Change_Status(girl, "Obed", -5)
            "She shoves you off and stands, perfectly composed and absolutely furious."
            $ force_scene_reset(girl, angry_days=1, reason="slap_femdom")
            jump main_loop

    else:
        if _slap_bj_forcing:
            $ _slap_line = renpy.random.choice([_("Gllur!"), _("Mmrph!"), _("Glrk!"), _("Nngh!")])
            call _moan_say(girl, _slap_line, muffled=True) from _call_ms_slap_default
        else:
            $ _slap_line = renpy.random.choice([_("Ugh..."), _("Mmh..."), _("Ah!"), _("Ngh...")])
            call _moan_say(girl, _slap_line) from _call_ms_slap_defaultb

        if store._slap_count >= 4 and store._slap_count < 8:
            if _slap_bj_forcing:
                python:
                    if store._slap_count <= 5:
                        _def_warn_lines = [_("Mmph... nnh..."), _("Hhn... nngh..."), _("Glk... mmph...")]
                    else:
                        _def_warn_lines = [_("MMPH!! NNH!!"), _("HHN!! NNGH!!"), _("MMRPH!! GGH!!")]
                $ _slap_line = _tl(renpy.random.choice(_def_warn_lines))
                call _moan_say(girl, _slap_line, muffled=True) from _call_ms_slap_def_warn
            else:
                if scene_type == "bj":
                    $ set_scene_expression(girl, None, mouth="mouth_sad")
                elif scene_type == "hj":
                    python:
                        state = sprite_state.setdefault(girl.Id, {})
                        state["mouth"] = "mouth_sad"
                        _hj_update_attrs(girl)
                        _hj_show_sprite(girl)
                python:
                    if store._slap_count <= 5:
                        _def_warn_lines = [
                            _("Hey... that actually hurts..."),
                            _("Don't hit me like that..."),
                            _("Ow... can you not do that?"),
                        ]
                    else:
                        _def_warn_lines = [
                            _("Seriously, stop hitting me!"),
                            _("I said it hurts! What's wrong with you?"),
                            _("Stop it! That really hurts!"),
                        ]
                $ _slap_line = _tl(renpy.random.choice(_def_warn_lines))
                call _moan_say(girl, _slap_line) from _call_ms_slap_def_warnb
            $ Change_Status(girl, "Love", -5)
            $ Change_Status(girl, "Obed", 3)

        if store._slap_count >= 8:
            if scene_type == "bj":
                $ set_scene_expression(girl, None, eyes="eyes_squint_2", mouth="mouth_sad")
            elif scene_type == "hj":
                python:
                    state = sprite_state.setdefault(girl.Id, {})
                    state["eyes"] = "eyes_closed"
                    state["mouth"] = "mouth_sad"
                    _hj_update_attrs(girl)
                    _hj_show_sprite(girl)
            python:
                _def_stop_lines = [
                    _("We're done. I'm not letting you hit me anymore."),
                    _("That's it. I told you to stop and you didn't. We're done."),
                    _("No. I'm done. You went way too far."),
                ]
            $ _slap_line = _tl(renpy.random.choice(_def_stop_lines))
            call _moan_say(girl, _slap_line) from _call_ms_slap_def_abort
            $ Change_Status(girl, "Love", -15)
            "She pulls away, visibly shaken."
            $ force_scene_reset(girl, angry_days=1, reason="slap_abuse")
            jump main_loop

    # She counts (count_slaps.rpy): the number after the slap's moan (never with his hands on her head)
    $ count_slaps_say(girl, True)
    return

# 4. CUM CLEANUP MENU
# ============================================================

label CumCleanupMenu(girl):

    # Re-add mouth cum if flagged (removed during BJ reaction for visual transition)
    python:
        if getattr(girl, "_mouth_cum_persist", False):
            _mcl = getattr(girl, "Cum", [])
            if "mouth" not in _mcl:
                _mcl.append("mouth")
                girl.Cum = _mcl
                girl.RefreshSprite()   # drawn now, not at the next refresh ("Leave it" was the first one)
            debug_log("[CLEANUP_MENU] mouth cum re-added for %s before cleanup menu" % girl.gid)

    # Skip if no visible cum on her (condom-only doesn't count)
    if not session_cum_has_any():
        # She may blurt out her pill / cycle status after a raw creampie (reads the risk list, so before the rolls)
        if callable(globals().get("fert_scene_remark", None)):
            $ fert_scene_remark(girl)
        if callable(globals().get("_process_pregnancy_rolls", None)):
            $ _process_pregnancy_rolls()
        $ session_cum_reset()
        return

    # still discovering it (trait_is_new): she likes it and it surprises her, no "I love it" yet
    $ _cs_cl_new = girl.has_trait("cum_slut") and trait_is_new(girl, "cum_slut")
    $ _al_cl_new = girl.has_trait("anal_lover") and trait_is_new(girl, "anal_lover")

    # Trait-specific opening line + discovery
    if _cs_cl_new:
        $ Say_Line(girl, _("Look at this mess... why am I smiling?"))
        $ girl.discover("discovered_trait_cum_slut")
    elif girl.has_trait("cum_slut"):
        $ Say_Line(girl, _("Mmm... look at this mess. I love it."))
        $ girl.discover("discovered_trait_cum_slut")
    elif girl.has_trait("hate_cum"):
        $ Say_Line(girl, _("Ugh... this is disgusting. Get it off me."))
        $ girl.discover("discovered_trait_hate_cum")
    else:
        $ Say_Line(girl, _("So... what do I do about the mess?"))

    # Check what options are available
    $ _eat_check = CumCleanupCheck(girl, "eat")
    $ _leave_check = CumCleanupCheck(girl, "leave")
    $ _can_eat = _eat_check["accepted"]
    $ _can_leave = _leave_check["accepted"]

    menu:
        "Clean up.":
            if girl.has_trait("hate_cum"):
                $ Say_Line(girl, _("Thank god. Give me something to wipe with."))
            else:
                $ Say_Line(girl, _("Yeah, I figured."))
            "She cleans herself off."
            $ girl.Cum = []
            $ girl._mouth_cum_persist = False
            $ girl.RefreshSprite()
            $ Change_Status(girl, "Love", 5)

        "Eat it." if _can_eat:
            python:
                _cum_from_ass = store._session_cum.get("anal_inside", 0) > 0
            if _cum_from_ass:
                # Cum came from her ass — trait-specific acknowledgment
                if girl.has_trait("cum_slut") and (_cs_cl_new or _al_cl_new):
                    $ Say_Line(girl, _("From my ass...? ...Okay. I want to."))
                    "She hesitates for a second, then scoops it up, blushing."
                    $ Change_Status(girl, "Obed", 20)
                    $ Change_Status(girl, "Inbt", 35)
                    $ girl.Lust = min(100, getattr(girl, "Lust", 0) + 15)
                elif girl.has_trait("cum_slut"):
                    $ Say_Line(girl, _("From my ass? Even better. Give me every drop."))
                    "She eagerly scoops it all up without hesitation."
                    $ Change_Status(girl, "Obed", 20)
                    $ Change_Status(girl, "Inbt", 35)
                    $ girl.Lust = min(100, getattr(girl, "Lust", 0) + 15)
                elif _al_cl_new:
                    $ Say_Line(girl, _("It came from... back there. ...Okay."))
                    "She licks her fingers clean, her cheeks burning."
                    $ Change_Status(girl, "Obed", 15)
                    $ Change_Status(girl, "Inbt", 25)
                elif girl.has_trait("anal_lover"):
                    $ Say_Line(girl, _("Mmm... I know exactly where that came from."))
                    "She licks her fingers clean with a knowing look."
                    $ Change_Status(girl, "Obed", 15)
                    $ Change_Status(girl, "Inbt", 25)
                elif girl.has_trait("hardcore_sex"):
                    $ Say_Line(girl, _("Eating cum from my own ass. What am I even doing with my life?"))
                    "She does it anyway, without breaking eye contact."
                    $ Change_Status(girl, "Obed", 20)
                    $ Change_Status(girl, "Inbt", 25)
                elif girl.has_trait("cute_sex"):
                    $ Say_Line(girl, _("You want me to eat that after it was... back there? ...Okay..."))
                    "She reluctantly scoops it up, wincing as she swallows."
                    $ Change_Status(girl, "Obed", 20)
                    $ Change_Status(girl, "Inbt", 15)
                elif girl.has_trait("anal_hater"):
                    $ Say_Line(girl, _("That was in my ass... and now you want me to eat it? That's awful."))
                    "She forces herself through it, grimacing the whole time."
                    $ Change_Status(girl, "Obed", 20)
                    $ Change_Status(girl, "Inbt", 15)
                else:
                    $ Say_Line(girl, _("From my ass... okay. Not like this day can get any weirder."))
                    "She scoops it up and swallows with a resigned expression."
                    $ Change_Status(girl, "Obed", 15)
                    $ Change_Status(girl, "Inbt", 20)
            elif _cs_cl_new:
                $ Say_Line(girl, _("Okay... I want to."))
                "She licks it up, blushing at how much she enjoys it."
                $ Change_Status(girl, "Obed", 20)
                $ Change_Status(girl, "Inbt", 30)
                $ girl.Lust = min(100, getattr(girl, "Lust", 0) + 15)
            elif girl.has_trait("cum_slut"):
                $ Say_Line(girl, _("With pleasure~"))
                "She eagerly licks every last drop."
                $ Change_Status(girl, "Obed", 20)
                $ Change_Status(girl, "Inbt", 30)
                $ girl.Lust = min(100, getattr(girl, "Lust", 0) + 15)
            else:
                $ Say_Line(girl, _("You want me to...? Fine."))
                "She scoops it up and licks her fingers clean."
                $ Change_Status(girl, "Obed", 15)
                $ Change_Status(girl, "Inbt", 20)
            $ girl.Cum = []
            $ girl._mouth_cum_persist = False
            $ girl.RefreshSprite()

        "Don't clean it. Leave it." if _can_leave:
            # Flag for next-morning creampie photo (only if cum is actually inside)
            if store._session_cum.get("inside", 0) > 0:
                $ girl._creampie_photo_pending = True
            if girl.has_trait("public_fetish"):
                $ Say_Line(girl, _("Hehe... everyone's going to see, you know?"))
                "She grins and walks off without cleaning up."
                $ Change_Status(girl, "Inbt", 35)
                $ Change_Status(girl, "Obed", 15)
            elif girl.has_trait("public_shy"):
                $ Say_Line(girl, _("W-what?! Someone might see...!"))
                "Despite her protests, she doesn't wipe it off."
                $ Change_Status(girl, "Obed", 30)
                $ Change_Status(girl, "Inbt", 15)
            else:
                $ Say_Line(girl, _("Seriously? Walk around like this?"))
                "She hesitates, but doesn't wipe it off."
                $ Change_Status(girl, "Inbt", 25)
                $ Change_Status(girl, "Obed", 10)
            $ _rebuild_cum_from_session(girl)

        "You decide.":
            python:
                _inbt = getattr(girl, "Inbt", 0)
                _obed = getattr(girl, "Obed", 0)
                _is_cum_slut = girl.has_trait("cum_slut")
                _is_pub_fetish = girl.has_trait("public_fetish")
            # cum_slut always prefers to eat (still discovering it: she is surprised at herself)
            if _is_cum_slut and _cs_cl_new:
                $ Say_Line(girl, _("I... think I want to taste it."))
                "She licks it up, a little surprised at herself."
                $ girl.Cum = []
                $ girl._mouth_cum_persist = False
                $ girl.RefreshSprite()
                $ Change_Status(girl, "Obed", 20)
                $ Change_Status(girl, "Inbt", 25)
                $ girl.Lust = min(100, getattr(girl, "Lust", 0) + 10)
            elif _is_cum_slut:
                $ Say_Line(girl, _("Mmm... I think I'll have a taste~"))
                "She eagerly licks it all up."
                $ girl.Cum = []
                $ girl._mouth_cum_persist = False
                $ girl.RefreshSprite()
                $ Change_Status(girl, "Obed", 20)
                $ Change_Status(girl, "Inbt", 25)
                $ girl.Lust = min(100, getattr(girl, "Lust", 0) + 10)
            # public_fetish prefers to leave it
            elif _is_pub_fetish and _can_leave:
                $ Say_Line(girl, _("I'll leave it on... let them stare."))
                "She walks off with a confident smirk."
                $ Change_Status(girl, "Inbt", 30)
                $ Change_Status(girl, "Obed", 15)
                $ _rebuild_cum_from_session(girl)
            elif _can_leave and _inbt >= 400:
                $ Say_Line(girl, _("Hmm... I think I'll leave it."))
                "She smirks and doesn't bother cleaning up."
                $ Change_Status(girl, "Inbt", 20)
                $ Change_Status(girl, "Obed", 10)
                $ _rebuild_cum_from_session(girl)
            elif _can_eat and _obed >= 300:
                $ Say_Line(girl, _("Well... waste not, want not."))
                "She licks it all up without hesitation."
                $ girl.Cum = []
                $ girl._mouth_cum_persist = False
                $ girl.RefreshSprite()
                $ Change_Status(girl, "Obed", 15)
                $ Change_Status(girl, "Inbt", 15)
            else:
                $ Say_Line(girl, _("I'll just clean it, obviously."))
                "She wipes herself off."
                $ girl.Cum = []
                $ girl._mouth_cum_persist = False
                $ girl.RefreshSprite()
                $ Change_Status(girl, "Love", 5)

    $ girl._mouth_cum_persist = False

    # She may blurt out her pill / cycle status after a raw creampie (reads the risk list, so before the rolls)
    if callable(globals().get("fert_scene_remark", None)):
        $ fert_scene_remark(girl)

    # Process pregnancy rolls before resetting session
    if callable(globals().get("_process_pregnancy_rolls", None)):
        $ _process_pregnancy_rolls()

    $ session_cum_reset()

    return

# ============================================================
# 5. DEPRECATED: replaced by _post_cum_central (v0.10.4)
#    Kept for safety; no callers after refactor.
# ============================================================

label PlayerExhausted(girl, scene_type):
    # Reset player focus so he doesn't cum-loop
    $ Player.set_focus(0)

    if getattr(store, "_scene_restricted", False):
        return

    # --- Special case: player didn't finish + forced creampie pending ---
    # She was furious about the creampie but stayed because Lust was high.
    # Now the player can't even finish? She's LIVID.
    if store._forced_creampie_end_after_orgasm:
        $ store._forced_creampie_end_after_orgasm = False
        call _player_didnt_finish_after_forced_creampie(girl, scene_type) from _call__player_didnt_finish_forced
        return

    python:
        _girl_came = store._session_girl_orgasms > 0
        _has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        _ex_is_cheater = hasattr(girl, "has_trait") and girl.has_trait("cheater")

        # --- PLAYER EXHAUSTION LINES (narrator) ---
        _exhaust_narr = [
            _("Your body gives out. You can't keep going."),
            _("You feel completely drained. There's nothing left."),
            _("Your legs feel like lead. You're done."),
        ]

        # --- GIRL REACTION: she DID cum ---
        _girl_satisfied = {
            "hardcore_sex": [
                _("That's it? Hmph. At least I got mine."),
                _("You're done already? Well, I can't complain... I got what I needed."),
                _("Tch. Could've gone longer. But at least you made me finish first."),
            ],
            "cute_sex": [
                _("Hey... it's okay. You made me feel amazing. Rest now."),
                _("Don't worry about it. I'm happy. You were wonderful."),
                _("That was perfect. You don't need to push yourself for me."),
            ],
            "cum_slut": [
                _("Aww, already? I wanted more... but at least I came."),
                _("Done already? Hmm... well, you did make me cum, so I'll forgive you."),
                _("I wanted to keep going... but fine. You earned your rest."),
            ],
            "hate_cum": [
                _("Good. We're done then. At least it wasn't a waste."),
                _("Fine by me. I'm satisfied anyway."),
                _("That's enough then. It was... fine."),
            ],
            "_bf": [
                _("I can't believe I just did that... but at least it felt good."),
                _("My %(pl)s would be devastated if %(pp)s knew... but you did make me feel things %(pp)s doesn't."),
                _("This was a mistake... a really good mistake. But still a mistake."),
            ],
            "_default": [
                _("It's okay. I'm satisfied. You did good."),
                _("Don't worry about it. I had fun."),
                _("That was great. Rest up, okay?"),
            ],
        }

        # --- GIRL REACTION: she did NOT cum ---
        _girl_unsatisfied = {
            "hardcore_sex": [
                _("Are you serious?! That's it? You didn't even make me cum!"),
                _("Wow. I can't believe this. All that and I didn't even finish."),
                _("Pathetic. You couldn't even get me off?"),
                _("Don't tell me you're done. I didn't even get CLOSE."),
            ],
            "cute_sex": [
                _("Oh... you're done? I... it's okay, I guess. These things happen."),
                _("I was hoping to finish too, but... it's fine. Don't worry about it."),
                _("It's alright. Maybe next time you can last a little longer?"),
                _("I'm not upset... just a little disappointed. But it's okay, really."),
            ],
            "cum_slut": [
                _("Wait, WHAT? You're done?! But I didn't even get to cum!"),
                _("Are you kidding me?! I was SO close! This is so unfair!"),
                _("Noooo! I needed more! You can't just leave me like this!"),
            ],
            "hate_cum": [
                _("So you finished and I didn't? Typical."),
                _("Of course. You got what you wanted and I got nothing."),
                _("Great. You're done and I'm left unsatisfied. Fantastic."),
            ],
            "_bf": [
                _("I cheated on my %(pl)s for THIS? You didn't even make me cum!"),
                _("I can't believe I fell for this... and I didn't even get to finish."),
                _("I risked everything for nothing. Not even an orgasm."),
                _("My %(pl)s would've at least tried to make me finish..."),
            ],
            "_bf_cheater": [
                _("Seriously? I left my %(pl)s hanging for this?"),
                _("Well that was a waste. At least my %(pl)s makes me cum."),
                _("I snuck around for nothing. You didn't even finish the job."),
            ],
            "_default": [
                _("Wait... you're done? But I didn't..."),
                _("Oh. That's it? I was hoping to finish too..."),
                _("I'm a little disappointed, honestly. I didn't get to cum."),
                _("You're stopping? But I wasn't done..."),
            ],
        }

        # --- Pick girl reaction ---
        if _girl_came:
            _pool = _girl_satisfied
        else:
            _pool = _girl_unsatisfied

        _picked_line = None
        _ex_bf_f = None
        if _has_bf:
            _ex_bf_f = partner_fmt(girl)
        # BF lines
        if _has_bf and not _ex_is_cheater and not _girl_came:
            _picked_line = _tl(renpy.random.choice(_pool["_bf"])) % _ex_bf_f
        elif _has_bf and _ex_is_cheater and not _girl_came:
            _picked_line = _tl(renpy.random.choice(_pool["_bf_cheater"])) % _ex_bf_f
        elif _has_bf and not _ex_is_cheater and _girl_came:
            _picked_line = _tl(renpy.random.choice(_pool["_bf"])) % _ex_bf_f
        # Trait lines
        if _picked_line is None:
            for _t in ("hardcore_sex", "cute_sex", "cum_slut", "hate_cum"):
                if girl.has_trait(_t):
                    _picked_line = renpy.random.choice(_pool[_t])
                    break
        if _picked_line is None:
            _picked_line = renpy.random.choice(_pool["_default"])

    # --- Narrator: you're spent ---
    "[_tl(renpy.random.choice(_exhaust_narr))]"

    # --- Girl reaction ---
    $ Say_Line(girl, _picked_line)

    # --- Stat consequences when girl didn't cum ---
    if not _girl_came:
        $ Change_Status(girl, "Obed", -10)
        $ Change_Status(girl, "Love", -5)
        if girl.has_trait("hardcore_sex"):
            "She looks genuinely angry. You can tell this won't be easily forgiven."
        elif girl.has_trait("cute_sex"):
            "She hides it well, but you can see the disappointment in her eyes."
        elif _has_bf and not _ex_is_cheater:
            "The regret is written all over her face."
        else:
            "She clearly expected more from you."
    else:
        "At least she seems satisfied."

    # --- Narrator tip: train at the gym (only while it can still go up: 5 = cap) ---
    if Player.energy_max < 5:
        "You need to build your stamina if you want to last longer. {b}Working out at the gym{/b} will raise your max energy over time."
        "Your current max energy: {b}[Player.energy_max]/5{/b}. Train consistently to push your limits."

    return
