# ============================================================
# SHARED SEX SCENE TICK + LAYER CLEANUP
# Centralizes the "keep going" logic for all penetration scenes
# and provides automatic layer cleanup by tag prefix.
# ============================================================

# A restricted scene that does NOT end with his finish (scene_ends_on_cum): set with _scene_restricted by a girl's story
# scenes, cleared with it
default _scene_cum_continues = False
# He had a condom on when his finish started (PlayerCumMenu / ForcedCumOverdue): his finish outside pulls it off, the
# next round still asks for one (_set_post_cum)
default _finish_had_condom = False

init python:

    def scene_ends_on_cum():
        """The scene ends with his first finish, no post-cum menu: a restricted event scene (_scene_restricted). A
        girl's story scenes are restricted too but go on like any scene (_scene_cum_continues: story_restricted_scene,
        her final-step dinner); of her story only the marital bed ends on it (author, 2026-10-09)."""
        return bool(getattr(store, "_scene_restricted", False)) and not getattr(store, "_scene_cum_continues", False)

    _SCENE_TAG_PREFIXES = {
        "doggy":           ("dg_", "sdg_"),
        "anal":            ("dg_", "sdg_"),
        "cowgirl":         ("cowgirl_", "scg_"),
        "reverse_cowgirl": ("rcg_", "srcg_"),
        "reverse_cowgirl_anal": ("rcg_", "srcg_"),
        "full_nelson":     ("fn_",),
        "full_nelson_anal": ("fn_",),
        "hj":              ("hj_",),
        "bj":              ("bj_",),
        "tj":              ("titjob_",),
        "laying_down":     ("ld_",),
        "laying_anal":     ("ld_",),
        "fj":              ("ft_",),
        "rj":              ("rj_",),
    }

    _ALL_SCENE_PREFIXES = ("dg_", "sdg_", "cowgirl_", "scg_", "rcg_", "srcg_", "fn_", "hj_", "bj_", "titjob_", "ld_", "ft_", "rj_")

    def _hide_scene_layers(position, girl=None):
        """Hide ALL standalone layers for a position by tag prefix.
        Automatically finds every shown image with the position's prefix
        so new clothing items never need manual cleanup updates."""
        prefixes = _SCENE_TAG_PREFIXES.get(position, ())
        showing = list(renpy.get_showing_tags("master"))
        _hidden = []
        _remaining = []
        for tag in showing:
            _matched = False
            for p in prefixes:
                if tag.startswith(p):
                    renpy.hide(tag)
                    _hidden.append(tag)
                    _matched = True
                    break
            if not _matched:
                _remaining.append(tag)
        print("[HIDE_SCENE_LAYERS] position=%s prefixes=%s hidden=%s remaining=%s" % (position, prefixes, _hidden, _remaining))
        if position == "bj" and girl:
            gid = girl.gid
            for tag in showing:
                if tag.startswith(gid + "_bj_"):
                    renpy.hide(tag)

    def _hide_all_scene_layers(girl=None):
        """Nuclear cleanup: hide ALL sex scene layers across ALL positions.
        Call at the start of any Launch to guarantee a clean slate."""
        showing = list(renpy.get_showing_tags("master"))
        _tenny_tags = [t for t in showing if "tenny" in str(t)]
        if _tenny_tags:
            print("[TENNY_TRACE] _hide_all_scene_layers ENTRY: tenny-related tags=%s all_tags=%s" % (_tenny_tags, showing))
        for tag in showing:
            for p in _ALL_SCENE_PREFIXES:
                if tag.startswith(p):
                    renpy.hide(tag)
                    break
        _known_gids = set(getattr(store, "GIRL_BY_ID", {}).keys())
        if girl:
            _known_gids.add(girl.gid)
        for tag in showing:
            for _gid in _known_gids:
                if tag.startswith(_gid + "_bj_") or tag.startswith(_gid + "_hj_"):
                    renpy.hide(tag)
                    break
        _remaining = list(renpy.get_showing_tags("master"))
        _tenny_remain = [t for t in _remaining if "tenny" in str(t)]
        if _tenny_remain:
            print("[TENNY_TRACE] _hide_all_scene_layers EXIT: tenny STILL showing=%s" % _tenny_remain)

    def _sex_lust_for_speed(speed):
        if speed <= 1:
            return 3
        elif speed == 2:
            return 5
        return 8

    _POST_CUM_MENU_MAP = {
        "sex": {
            "laying_down": "LD_ControlMenu", "laying_anal": "LD_ControlMenu",
            "doggy": "DG_ControlMenu", "anal": "DG_ControlMenu",
            "full_nelson": "FN_ControlMenu", "full_nelson_anal": "FN_ControlMenu",
            "cowgirl": "COWGIRL_ControlMenu",
            "reverse_cowgirl": "RCG_ControlMenu", "reverse_cowgirl_anal": "RCG_ControlMenu",
            "bj": "BJ_ActionMenu",
            "hj": "HJ_ControlMenu",
            "tj": "TITJOB_ControlMenu",
            "fj": "FT_ControlMenu",
            "rj": "RJ_ControlMenu",
        },
        "rub": {
            "doggy": "DG_RubControlMenu", "laying_down": "LD_RubControlMenu",
            "full_nelson": "FN_RubControlMenu",
            "cowgirl": "COWGIRL_RubControlMenu",
            "reverse_cowgirl": "RCG_RubControlMenu",
        },
        "tip": {
            "doggy": "DG_TipControlMenu", "laying_down": "LD_TipControlMenu",
            # FN is the one position that reports its anal name in tip mode (doggy / RCG pass the base name):
            # without this row "Keep going" after his cum ended the anal tip scene (tester 2026-10-11)
            "full_nelson": "FN_TipControlMenu", "full_nelson_anal": "FN_TipControlMenu",
            "cowgirl": "COWGIRL_TipControlMenu",
            "reverse_cowgirl": "RCG_TipControlMenu",
        },
    }

    def _scene_should_exit():
        return (
            store._player_exhausted
            or store._post_cum_pending
            or store._sub_event_position_switched
            or getattr(store, "_scene_force_end", False)
            or store._hate_cum_scene_aborted
        )

    def scene_flow_state():
        """Everything that decides whether a scene goes on after his cum, on one line: the [SCENE_FLOW] logs (search
        log.txt for [SCENE_FLOW] to follow a scene from his cum to its end)."""
        return ("energy=%s exhausted=%s post_cum_pending=%s pos_switched=%s force_end=%s hate_abort=%s npc_abort=%s "
                "restricted=%s cum_continues=%s condom=%s Round=%s stack=%s") % (
            getattr(store.Player, "energy", "?"), store._player_exhausted, store._post_cum_pending,
            store._sub_event_position_switched, getattr(store, "_scene_force_end", False), store._hate_cum_scene_aborted,
            getattr(store, "_npc_witness_scene_aborted", False), getattr(store, "_scene_restricted", False),
            getattr(store, "_scene_cum_continues", False), getattr(store, "condom_active", False),
            getattr(store, "Round", "?"), [str(_n) for _n in renpy.get_return_stack()[-6:]])

    def _scene_exit_flags_reset():
        """Clear every flag _scene_should_exit() reads. sex_menu clears these on
        entry; scenes launched OUTSIDE sex_menu (ToD dares, secret-party BJ) MUST
        call this before launching. Otherwise a flag left True by a previous
        scene's cum (_post_cum_pending, set by _handle_post_cum_exit) makes the
        next scene's ControlMenu exit on the first tick — the scene ends with no
        player input."""
        store._player_exhausted = False
        store._post_cum_pending = False
        store._finish_had_condom = False
        store._sub_event_position_switched = False
        store._scene_force_end = False
        store._hate_cum_scene_aborted = False
        # a catch-STOP outside start_scene (e.g. _virgin_anal_launch) left this True and the
        # NEXT scene ended on its first Keep going with "rushes out" and no partner on scene
        store._npc_witness_scene_aborted = False
        store._edge_end_said = None        # her "left on the edge" line may play once in the new session
        femdom_session_reset("bypass launch")
        print("[SCENE] _scene_exit_flags_reset: cleared exit flags before bypass launch")

    def _slot_to_transform(slot):
        if slot == StageLeft:
            return slot_left
        elif slot == StageRight:
            return slot_right
        return slot_center

    def _reset_expression_state(girl):
        state = sprite_state.setdefault(girl.Id, {})
        state["brows"] = "brows_normal"
        state["eyes"] = "eyes_normal"
        state["mouth"] = "mouth_normal"

    def _set_post_cum(scene_type, sub_mode="sex"):
        store._post_cum_pending = True
        store._post_cum_scene_type = scene_type
        store._post_cum_sub_mode = sub_mode
        store._post_cum_menu = _POST_CUM_MENU_MAP.get(sub_mode, {}).get(scene_type)
        # Read right after THIS cum. Only the cum-outside menu used to set it and nothing cleared it, so after
        # cumming INSIDE the condom the round went on with the same used condom (never rolled again) or not,
        # depending on an older scene. With a condom on for this finish _post_cum_central always asks: a fresh
        # condom / ask to go raw / stop. "On for this finish" includes the one he pulled off to cum outside
        # (_finish_had_condom): the next round is never raw without her answer.
        store._post_cum_had_condom = _girl_thinks_condom_on() or bool(getattr(store, "_finish_had_condom", False))
        print("[POST_CUM] set: scene=%s sub=%s had_condom=%s (condom_active=%s stealth=%s finish_had_condom=%s)" % (
            scene_type, sub_mode, store._post_cum_had_condom, store.condom_active, getattr(store, "_stealth_condom_removed", False),
            getattr(store, "_finish_had_condom", False)))
        print("[SCENE_FLOW] post-cum set: scene=%s sub=%s resume_menu=%s | %s" % (scene_type, sub_mode, store._post_cum_menu, scene_flow_state()))
        store._finish_had_condom = False

    def _handle_post_cum_exit(scene_type, sub_mode="sex"):
        print("[POST_CUM_EXIT] scene=%s sub=%s force_end=%s hate_abort=%s exhausted=%s" % (
            scene_type, sub_mode,
            getattr(store, "_scene_force_end", False),
            store._hate_cum_scene_aborted,
            store._player_exhausted))
        if getattr(store, "_scene_force_end", False):
            print("[SCENE_FLOW] after his cum: FORCE END (the scene ends, no post-cum menu) | %s" % scene_flow_state())
            return "force_end"
        if store._hate_cum_scene_aborted:
            store._hate_cum_scene_aborted = False
            print("[SCENE_FLOW] after his cum: HATE_CUM ABORT (the scene ends) | %s" % scene_flow_state())
            return "hate_abort"
        _set_post_cum(scene_type, sub_mode)
        return "post_cum"

    def _anal_lust_for_speed(girl, speed):
        if girl.has_trait("anal_lover"):
            return _sex_lust_for_speed(speed)
        elif girl.has_trait("anal_hater") and girl.has_trait("hardcore_sex"):
            return 2 if speed == 1 else 3 if speed == 2 else 5
        elif girl.has_trait("anal_hater"):
            return 0 if speed == 1 else 1 if speed == 2 else 1
        else:
            return 1 if speed == 1 else 2 if speed == 2 else 3

    def _apply_anal_lust_cap(girl, is_anal):
        if is_anal and girl.has_trait("anal_hater") and not girl.has_trait("hardcore_sex"):
            girl.Lust = min(girl.Lust, 50)

    def _anal_tip_lust(girl):
        """Her Lust per tick of an ANAL tip (the doggy's rule: a lover 2, a hater nothing, 1 otherwise)."""
        if girl.has_trait("anal_lover"):
            return 2
        if girl.has_trait("anal_hater"):
            return 0
        return 1

    def _count_anal_tip(girl, is_anal):
        if is_anal and not store._anal_tip_counted:
            store._anal_tip_counted = True
            _acts = getattr(girl, "Sex_acts", {}) or {}
            _acts["anal_tip"] = _acts.get("anal_tip", 0) + 1
            girl.Sex_acts = _acts
            mark_intimacy(girl, "anal_tip")

    # ── Trait mini-script dialogue pools ──

    _CUM_SLUT_RAW_CREAM_LINES = [
        _("Oh god yes... I can feel it all inside me..."),
        _("Mmm... fill me up... every last drop..."),
        _("Don't pull out yet... I want to feel you throb inside me..."),
        _("That's what I needed... your cum deep inside me..."),
    ]

    _GENTLE_SPEED_COMPLAINT_LINES = [
        _("Slow down... you're going too fast..."),
        _("Not so rough... please..."),
        _("That's too fast for me... can you be gentler...?"),
        _("Easy... you're hurting me a little..."),
        _("Please slow down... I like it gentle..."),
    ]

    _EXHIB_PUBLIC_LINES = [
        _("Someone might see us... that makes it even better..."),
        _("The thought of getting caught is driving me crazy..."),
        _("Anyone could walk by right now... oh god..."),
        _("I love doing this where people might see..."),
        _("Being out in the open like this... it's so exciting..."),
    ]

    # ── Girl tries to remove condom ──
    _CONDOM_RIP_ATTEMPT_LINES = {
        "cum_slut": [
            _("I can't take this stupid condom anymore... I NEED to feel you!"),
            _("No more condom! I want it RAW inside me!"),
            _("Take it OFF! I want to feel every inch without this thing!"),
        ],
        # still discovering it (trait_is_new, read through trait_pool_key): she wants it, she does not rage at it
        "cum_slut_new": [
            _("I want to feel you without this... is that crazy?"),
            _("Can we take this off? I... I want to feel you."),
        ],
        "hardcore_sex": [
            _("Enough with this thing... I want the real deal."),
            _("This condom is ruining it. Let me take it off."),
        ],
        "breedable": [
            _("I want to feel you... all of you... let me take this off..."),
            _("This thing is in the way... I need you inside me for real..."),
        ],
        "_default": [
            _("I... I want to feel you without this..."),
            _("Can we just... take this off already?"),
            _("I don't want this between us anymore..."),
        ],
    }
    _CONDOM_RIP_STOPPED_OBEY = [
        _("...Fine. But I don't like it."),
        _("Ugh... okay. It stays."),
        _("...You're no fun. Okay."),
    ]
    _CONDOM_RIP_STOPPED_IGNORE = [
        _("I don't care what you think!"),
        _("You don't get to tell me what to do!"),
        _("Too bad! I'm doing it anyway!"),
    ]
    _CONDOM_RIP_ALLOWED = [
        _("Mmm... MUCH better... now fuck me properly!"),
        _("Finally... that's so much better..."),
        _("Yes... I needed this... keep going..."),
    ]
    _CONDOM_RIP_OBED_THRESHOLD = 400

    def _condom_rip_chance(girl):
        _inbt = getattr(girl, "Inbt", 0)
        _chance = _inbt * 0.00015
        if trait_is_veteran(girl, "cum_slut"):   # still discovering it: she tries no more than anyone with her Inbt
            _chance += 0.12
        if girl.has_trait("hardcore_sex"):
            _chance += 0.04
        if girl.has_trait("breedable") or girl.has_trait("pregnancy_fetish"):
            _chance += 0.05
        if girl.has_trait("hate_cum") or girl.has_trait("pregnancy_fear"):
            _chance = 0.0
        return min(_chance, 0.35)

    def _condom_rip_line(girl):
        for _t in ("cum_slut", "hardcore_sex", "breedable"):
            if girl.has_trait(_t) and _t in _CONDOM_RIP_ATTEMPT_LINES:
                return renpy.random.choice(_CONDOM_RIP_ATTEMPT_LINES[trait_pool_key(girl, _t, _CONDOM_RIP_ATTEMPT_LINES)])
        return renpy.random.choice(_CONDOM_RIP_ATTEMPT_LINES["_default"])


# Result flags — set by _sex_scene_tick, read by caller
default _sst_result = "continue"
default _sst_abort_reason = None
default _condom_rip_attempted = False

# Auto-continue: when True, the choice screen auto-fires "Keep going" every 3s
# and Ren'Py's auto-forward advances dialogue automatically
default _auto_continue = False
default _ac_prev_afm = False
default _ac_prev_afm_time = 10

init python:
    _STOP_LINES = {
        "hardcore_sex": [
            _("Tch. Fine."),
            _("Already? I was just warming up."),
            _("You're stopping? Seriously?"),
        ],
        "cute_sex": [
            _("Okay... that was nice."),
            _("Sure, let's take a break."),
            _("That was sweet... thanks."),
        ],
        "cum_slut": [
            _("Mmm... already? Fine."),
            _("Aww, I wanted more... but okay."),
            _("Really? I was hoping we'd keep going..."),
        ],
        "hate_cum": [
            _("Good. We're done then."),
            _("Finally. That's enough."),
            _("About time."),
        ],
        "_default": [
            _("Okay... that was nice."),
            _("Mmm... already? Fine."),
            _("Sure, let's take a break."),
            _("Already? ...fine, we can stop."),
            _("Alright, let's stop here."),
        ],
    }

    _STOP_BEG_LINES = {
        # her Control trait first (_pick_stop_line): a submissive pleads, a femdom demands
        "submissive": [
            _("Can we please keep going a little bit longer? I'm... really close."),
            _("Please... not yet. I'll be good. I just need a little more. If you want."),
            _("I'm so close... please? Only if you want me to. But please."),
        ],
        "femdom": [
            _("Who said you could stop? I'm not done. Back to it."),
            _("Stop? No. I decide when we stop, and I haven't finished. Keep going."),
            _("You don't get to stop here. Finish what you started."),
        ],
        "hardcore_sex": [
            _("Wait... don't stop. I'm so close."),
            _("No, keep going! I need this!"),
            _("Don't you dare stop now. I was almost there."),
        ],
        "cute_sex": [
            _("W-wait... can we keep going? Just a little more..."),
            _("Please... I'm almost there. Don't stop yet..."),
            _("I was feeling so good... can you keep going?"),
        ],
        "cum_slut": [
            _("No no no, don't stop! I'm so close!"),
            _("Please keep going! I need to cum so bad!"),
            _("You can't stop now! I was about to...!"),
        ],
        "hate_cum": [
            _("Ugh... fine, don't stop. I'm... close."),
            _("Just... keep going. I need to finish."),
            _("Don't stop now... I hate that I need this."),
        ],
        "_default": [
            _("Wait... can we keep going? I'm almost there..."),
            _("Please... just a little more."),
            _("I was so close... don't stop now."),
        ],
    }

    def _pick_stop_line(girl, beg=False):
        pool = _STOP_BEG_LINES if beg else _STOP_LINES
        for _t in ("submissive", "femdom", "hardcore_sex", "cute_sex", "cum_slut", "hate_cum"):
            if girl.has_trait(_t):
                return _tl(renpy.random.choice(pool.get(_t, pool["_default"])))
        return _tl(renpy.random.choice(pool["_default"]))

    def _toggle_auto_continue():
        store._auto_continue = not store._auto_continue
        if store._auto_continue:
            store._ac_prev_afm = _preferences.afm_enable
            store._ac_prev_afm_time = _preferences.afm_time
            _preferences.afm_enable = True
            _preferences.afm_time = 5
        else:
            _preferences.afm_enable = store._ac_prev_afm
            _preferences.afm_time = store._ac_prev_afm_time

    def _disable_auto_continue():
        if store._auto_continue:
            store._auto_continue = False
            _preferences.afm_enable = store._ac_prev_afm
            _preferences.afm_time = store._ac_prev_afm_time


# ============================================================
# MAIN TICK — call once per "Keep going" in any penetration scene
# ============================================================
#
# girl_lust: override girl lust gain (default: auto by speed)
#            pass 0 to skip girl lust entirely (caller handles it)
#
# After return, check store._sst_result:
#   "continue"       — normal, keep looping
#   "condom_ripped"   — cum_slut ripped condom; caller must play
#                       CondomRemoveAnim + ApplySpeed for visuals
#   "condom_broken_accepted" — condom broke, she accepted raw;
#                       visuals already updated, just continue
#   "cum_resumed"     — player came but scene continues; caller
#                       should restore speed >= 1 and ApplySpeed
#   "abort"           — scene must end, call _sex_scene_handle_abort
#
label _sex_scene_tick(girl, position, speed, girl_lust=-1):
    $ store._sst_result = "continue"
    $ store._sst_abort_reason = None

    python:
        _sst_ptr = getattr(store, "_pending_tease_restore", None)
        if _sst_ptr:
            store._pending_tease_restore = None
            _sst_ptr_g = GIRL_BY_ID.get(_sst_ptr["gid"])
            if _sst_ptr_g:
                _sst_ss = sprite_state.setdefault(_sst_ptr_g.Id, {})
                for _sst_k, _sst_v in _sst_ptr["face"].items():
                    if _sst_v is not None:
                        _sst_ss[_sst_k] = _sst_v

    if _sst_ptr:
        call _sst_apply_speed_dispatch(girl, position) from _call_sst_tease_restore

    $ advance_round(TIME_COSTS["sex_tick"])
    $ add_player_focus(get_player_lust_gain(position, speed))

    if girl_lust < 0:
        $ _girl_lust_gain(girl, _sex_lust_for_speed(speed), speed)
    elif girl_lust > 0:
        $ _girl_lust_gain(girl, girl_lust, speed)

    $ _moan = scene_moan_tick(girl, position, speed)
    if _moan:
        call _moan_say(girl, _moan) from _call_ms_sst

    # ── gentle trait: complains at speed 3 ──
    if speed >= 3 and girl.has_trait("cute_sex"):
        python:
            _sst_gentle_cd = getattr(store, "_sst_gentle_cd", 0) - 1
            store._sst_gentle_cd = max(0, _sst_gentle_cd)
        if store._sst_gentle_cd <= 0 and renpy.random.random() < 0.25:
            $ store._sst_gentle_cd = 4
            $ Say_Line(girl, _tl(renpy.random.choice(_GENTLE_SPEED_COMPLAINT_LINES)))
            $ Change_Status(girl, "Obed", 1)
            $ Change_Status(girl, "Love", -1)

    # Time warnings
    if Round >= 90 and not store._time_warned_urgent:
        $ store._time_warned_urgent = True
        $ Say_Line(girl, _time_warning_line(girl, "urgent"))
    elif Round >= 80 and not store._time_warned_soon:
        $ store._time_warned_soon = True
        $ Say_Line(girl, _time_warning_line(girl, "soon"))

    # ── cheat path: first sex commentary (skip when NPC is present — lines assume NPC doesn't know) ──
    if getattr(store, "_path1_sex_first_line_pending", False) and not getattr(store, "_ntr_partner_watching", False):
        $ store._path1_sex_first_line_pending = False
        if (position in ("doggy", "anal") and store.doggy_anal) or (position != "anal" and position in _ANAL_SCENE_TYPES):
            $ Say_Line(girl, _cheat_anal_midline(girl))
        else:
            $ Say_Line(girl, _cheat_sex_midline(girl))

    # ── cheat path: breaking point (she snaps, removes condom) ──
    if _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False) and not getattr(store, "_ntr_partner_watching", False):
        if _cheat_breaking_point_ready(girl) and renpy.random.random() < 0.30:
            call _cheat_breaking_point(girl, position) from _call_cheat_break_sst

    # ── condom break check ──
    if store.condom_active and store._condom_break_will_happen and not store._condom_broken:
        if condom_break_tick():
            call CondomBreakEvent(girl, position) from _call_CondomBreakEvent_sst
            if store._sst_result == "abort":
                return

    # ── girl tries to remove condom: Inbt-based chance, player menu ──
    # Blocked while her partner's level-2 condom rule holds (_ntr_condom_rule_holds: he watches at level 2, or
    # she knows the rule and respects it)
    if store.condom_active and not store._condom_broken and speed >= 2 and not getattr(store, "_condom_rip_attempted", False):
        if story_act_locked(girl, "raw"):
            pass
        elif _ntr_condom_rule_holds(girl):
            pass
        elif not (_is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False)):
            if renpy.random.random() < _condom_rip_chance(girl):
                $ store._condom_rip_attempted = True
                $ Say_Line(girl, _tl(_condom_rip_line(girl)))
                "She reaches for the condom, trying to take it off."
                menu:
                    "Say nothing":
                        $ _on_condom_removed(girl, skip_hide=(position not in ("doggy", "anal")), force=True)
                        $ Say_Line(girl, _tl(renpy.random.choice(_CONDOM_RIP_ALLOWED)))
                        $ store._sst_result = "condom_ripped"
                    "Stop her":
                        if getattr(girl, "Obed", 0) >= _CONDOM_RIP_OBED_THRESHOLD:
                            $ set_scene_expression(girl, "annoyed")
                            $ Say_Line(girl, _tl(renpy.random.choice(_CONDOM_RIP_STOPPED_OBEY)))
                            $ set_scene_expression(girl, "normal")
                            $ Change_Status(girl, "Obed", 3)
                            $ Change_Status(girl, "Love", -2)
                        else:
                            $ set_scene_expression(girl, "angry")
                            $ Say_Line(girl, _tl(renpy.random.choice(_CONDOM_RIP_STOPPED_IGNORE)))
                            "She ignores you and pulls it off anyway."
                            $ _on_condom_removed(girl, skip_hide=(position not in ("doggy", "anal")), force=True)
                            $ Say_Line(girl, _tl(renpy.random.choice(_CONDOM_RIP_ALLOWED)))
                            $ set_scene_expression(girl, "normal")
                            $ store._sst_result = "condom_ripped"

    # ── mid-scene creampie consent change ──
    call _check_creampie_consent_change(girl) from _call_consent_change_sst

    # ── public attention ──
    if store._crowd_level > 0 and not getattr(store, "_scene_restricted", False):
        $ _pa_caught = public_attention_tick(girl, "keep_going", speed)
        if _pa_caught:
            if not _caught_keeps_going(girl):
                $ store._sst_result = "abort"
                $ store._sst_abort_reason = "caught_end"
            else:
                $ store._sst_result = "abort"
                $ store._sst_abort_reason = "caught_continue"
            return

    # ── exhibitionist in public: extra excitement ──
    if store._crowd_level > 0 and girl.has_trait("exhibitionist"):
        python:
            _sst_exhib_cd = getattr(store, "_sst_exhib_cd", 0) - 1
            store._sst_exhib_cd = max(0, _sst_exhib_cd)
        if store._sst_exhib_cd <= 0 and renpy.random.random() < 0.20:
            $ store._sst_exhib_cd = 5
            $ Say_Line(girl, _tl(renpy.random.choice(_EXHIB_PUBLIC_LINES)))
            $ _girl_lust_gain(girl, 3, speed)

    # ── random interruption check ──
    call _sex_interruption_check(girl, position) from _call_interrupt_sst
    $ store._witness_expression_lock = False
    if store._sex_interrupted:
        $ store._sst_result = "abort"
        $ store._sst_abort_reason = "interrupted"
        return

    # ── NPC partner detection ──
    call _npc_partner_detection_tick(girl, position) from _call_npc_detect_sst
    if store._npc_witness_scene_aborted:
        $ store._sst_result = "abort"
        $ store._sst_abort_reason = "npc_witness"
        return

    # ── sub events (pace request, position change, condom events, etc.) ──
    $ _se = sub_event_tick(girl, position)
    if _se:
        call SubEvent_Handle(girl, position, _se) from _call_SubEvent_Handle_sst
        if store._sub_event_position_switched:
            $ store._sub_event_position_switched = False
            $ store._sst_result = "abort"
            $ store._sst_abort_reason = "position_switch"
            return
        if store._sst_result == "abort":
            return

    # ── cheat path: BF phone call ──
    call _cheat_bf_call_check(girl, position) from _call_cheat_bf_sst

    # ── girl cumming ──
    if girl.Lust >= 100:
        call GirlCumming(girl, position, position) from _call_GirlCumming_sst

    # ── player cumming (focus overdue system) — bet event handles cum externally ──
    if player_is_cumming() and not getattr(store, "_bet_event_active", False):
        if not store._focus_warning_shown:
            $ store._focus_warning_shown = True
            "You feel like you're about to explode..."
        elif focus_overdue_tick():
            call ForcedCumOverdue(girl, position) from _call_ForcedCumOverdue_sst
            if getattr(store, "_scene_force_end", False):
                $ store._sst_result = "abort"
                $ store._sst_abort_reason = "force_end"
                return
            if store._hate_cum_scene_aborted:
                $ store._hate_cum_scene_aborted = False
                $ store._sst_result = "abort"
                $ store._sst_abort_reason = "hate_cum"
                return
            # Both exhausted and non-exhausted: route through centralized post-cum
            $ store._sst_result = "abort"
            $ store._sst_abort_reason = "post_cum"
            return

    if Player.energy <= 0:
        $ store._sst_result = "abort"
        $ store._sst_abort_reason = "post_cum"
        return

    return


# ============================================================
# ABORT HANDLER — dispatches to position-specific End/Creampie
# Call this when _sst_result == "abort"
# ============================================================
label _sex_scene_handle_abort(girl, position):
    if store._sst_abort_reason == "condom_break_denied":
        call _sst_end_dispatch(girl, position, False) from _call_sst_end_cbreak
        return

    if store._sst_abort_reason in ("caught_end", "caught_continue"):
        if store._sst_abort_reason == "caught_end":
            call _sst_end_dispatch(girl, position, False) from _call_sst_end_caught
        call caught_in_public(girl, position) from _call_caught_sst
        return

    if store._sst_abort_reason in ("interrupted", "npc_witness"):
        $ print("[SST_ABORT] reason=%s, calling _sst_end_dispatch. _npc_witness_scene_aborted=%s" % (store._sst_abort_reason, getattr(store, "_npc_witness_scene_aborted", False)))
        call _sst_end_dispatch(girl, position, False) from _call_sst_end_int
        $ print("[SST_ABORT] after _sst_end_dispatch. _npc_witness_scene_aborted=%s" % getattr(store, "_npc_witness_scene_aborted", False))
        return

    # "post_cum" is handled by ControlMenu caller via _post_cum_pending
    # hate_cum, position_switch: just return (caller handles)
    return


# ============================================================
# CONDOM RIP HANDLER — dispatches to position CondomRemoveAnim
# Call when _sst_result == "condom_ripped"
# ============================================================
label _sex_scene_condom_rip_visual(girl, position):
    call _cum_dispatch_condom_visual(girl, position) from _call__crv_delegate
    return


# ============================================================
# DISPATCH HELPERS
# ============================================================
label _sst_end_dispatch(girl, position, dress_up=False):
    call _cum_dispatch_end(girl, position, dress_up=dress_up) from _call__cum_dispatch_end_sst
    return

label _sst_creampie_dispatch(girl, position, consensual):
    call _cum_dispatch_aftermath(girl, position, drip_check=False, consented=consensual) from _call__cum_dispatch_aftermath_sst
    return

label _sst_apply_speed_dispatch(girl, position):
    call _cum_dispatch_apply_speed(girl, position) from _call__sst_as_delegate
    return

# ============================================================
# Centralized speed change stat tick — shared by all positions
# direction: 1 = speed up, -1 = speed down
# Called AFTER the position already adjusted its speed var and called ApplySpeed
# ============================================================
label _speed_change_tick(girl, position, direction=1):
    python:
        _sv = _cum_cfg(position, "speed_var")
        _spd = getattr(store, _sv, 0) if _sv else 0

    if direction >= 1:
        $ add_player_focus(get_player_lust_gain(position, _spd))
        $ _girl_lust_gain(girl, _sex_lust_for_speed(_spd), _spd)

        $ _pa_caught = public_attention_tick(girl, "speed_up", _spd)
        if _pa_caught:
            if not _caught_keeps_going(girl):
                call _cum_dispatch_end(girl, position) from _call_end_pa_sct
            call caught_in_public(girl, position) from _call_caught_sct
            return

        $ _se = sub_event_tick(girl, position)
        if _se:
            call SubEvent_Handle(girl, position, _se) from _call_se_sct
            if store._sub_event_position_switched:
                return

        if girl.Lust >= 100:
            call GirlCumming(girl, position, position) from _call_gc_sct
        if player_is_cumming() and not getattr(store, "_bet_event_active", False):
            if focus_overdue_tick():
                call ForcedCumOverdue(girl, position) from _call_fco_sct
                if getattr(store, "_scene_force_end", False):
                    return
                if store._hate_cum_scene_aborted:
                    $ store._hate_cum_scene_aborted = False
                    return
                # Route through centralized post-cum handler
                $ _set_post_cum(position, "sex")
                return
    else:
        $ add_player_focus(10 if _spd == 1 else 20 if _spd >= 2 else 0)

        $ _se = sub_event_tick(girl, position)
        if _se:
            call SubEvent_Handle(girl, position, _se) from _call_se_sct_sd
            if store._sub_event_position_switched:
                return
    return


# ============================================================
# MOAN SAY — pause animation, show moan line, resume speed
# Called from every position's control menu after scene_moan_tick
# returns a line string. Detects the active scene and pauses
# the appropriate ApplySpeed to 0 during dialogue.
# ============================================================
label _moan_say(girl, line, muffled=False):
    # BJ only: pause animation to speed 0 (mouth occupied, needs to stop to speak)
    # All other positions: girl speaks without stopping the animation
    # muffled=True: text appears without pausing animation or swapping BJ head
    python:
        _ms_is_bj = getattr(store, "_bj_girl", None) is girl
        _ms_speed = getattr(store, "bj_speed", 0) if _ms_is_bj else 0

    if not _ms_is_bj or _ms_speed <= 0:
        $ Say_Line(girl, line)
        return

    if muffled:
        $ renpy.say(_make_char_from_girl(girl), _tl(line))
        return

    $ _ms_saved_force = _bj_pause_forcing()

    call BJ_ApplySpeed(girl, 0) from _call_ms_pause
    $ Say_Line(girl, line)

    $ _bj_resume_forcing(_ms_saved_force)

    call BJ_ApplySpeed(girl, _ms_speed) from _call_ms_resume
    return


# ============================================================
# Centralized bottom clothes menu — strip skirt/panties before
# entering tip or sex from any position.
# ============================================================
label _scene_bottom_clothes_menu(girl, position):
    python:
        _slots_for_pos = POSE_SLOTS.get(position, [])
        _skirt_needs = ("skirt" in _slots_for_pos) and girl.Legs is not None and girl.clothes_state.get("skirt") == "full"
        _pan_needs = girl.Panties is not None and girl.clothes_state.get("panties") == "full"
        debug_log("[BOTTOM_CLOTHES] pos=%s skirt_needs=%s pan_needs=%s" % (position, _skirt_needs, _pan_needs))

    if not _skirt_needs and not _pan_needs:
        return

    python:
        _ready_lines = [
            _("Here... let me get ready for you."),
            _("Hold on... let me fix this first."),
            _("Just a second..."),
        ]
    $ Say_Line(girl, _tl(renpy.random.choice(_ready_lines)))

    if _skirt_needs:
        # the item on her legs, by name: pants have no "up" and are no skirt
        $ _sm_legs = clothing_item_name(girl, "skirt")
        menu:
            "Lift skirt up" if _item_has_state(girl, "skirt", "up"):
                $ girl.clothes_state["skirt"] = "up"
            "Remove [_sm_legs]":
                $ girl.clothes["skirt"] = None
                $ girl.clothes_state["skirt"] = "full"
        call _sst_btm_refresh(girl, position) from _call_sst_btm_skirt

    if _pan_needs:
        pause 0.3
        menu:
            "Pull panties to the side" if _item_has_state(girl, "panties", "side"):
                $ girl.clothes_state["panties"] = "side"
            "Remove panties":
                $ girl.clothes["panties"] = None
                $ girl.clothes_state["panties"] = "full"
        call _sst_btm_refresh(girl, position) from _call_sst_btm_pan

    call CheckExposure(girl) from _call_CheckExposure_btm_central
    return

label _sst_btm_refresh(girl, position):
    call _cum_dispatch_apply_speed(girl, position) from _call_btm_refresh_delegate
    return


# ============================================================
# Scene Stop Reaction — centralized stop line + beg-to-continue
# ============================================================
label _scene_stop_reaction(girl):
    $ store._stop_accepted = True
    if girl.Lust > 90:
        $ Say_Line(girl, _pick_stop_line(girl, beg=True))
        menu:
            "Let her have it":
                $ store._stop_accepted = False
                if getattr(store, "_stop_continue_count", 0) < 1:
                    $ Change_Status(girl, "Love", 5)
                $ store._stop_continue_count = getattr(store, "_stop_continue_count", 0) + 1
            "Stop anyway":
                $ Change_Status(girl, "Love", trait_love_loss(girl, -3))   # denied: a submissive minds nothing
                $ Change_Status(girl, "Obed", 5)
                if girl.has_trait("femdom"):
                    # his no to her order: counted and paid (femdom.rpy)
                    $ femdom_react_refused(girl, "stop")
    else:
        $ Say_Line(girl, _pick_stop_line(girl))
    return
