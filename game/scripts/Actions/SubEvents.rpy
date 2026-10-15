# ============================================================
# SubEvents.rpy... Girl-initiated sub-events during sex scenes
# ============================================================
# Dialogue is in scene_lines.rpy (SCENE_LINES dict).
# This file: defaults, condition checks, dispatcher, handlers.
# ============================================================

default _recording_seconds = 0.0

default _sub_event_cooldown = 0
default _sub_event_actions_taken = 0
default _sub_event_condom_fired = False
default _sub_event_creampie_fired = False
default _sub_event_position_fired = False
default _sub_event_position_switched = False
default _girl_requested_creampie = False
default _sub_event_recording_fired = False
default _cum_warning_done = False
default _virgin_nervous_done = False
default _public_panic_done = False
default _sub_event_watcher_condom_fired = False
default _sub_event_anal_request_fired = False
default _sub_event_pillow_fired = False
default _sub_event_atm_initiative_fired = False

init python:

    # ============================================================
    # CHARGE HER — player charges girl $100 for her request
    # ============================================================
    _SE_CHARGE_PRICE = 100

    def _se_can_charge(girl):
        # a sugar girl (sugar_mommy.rpy) can always be charged: paying him IS the arrangement
        if sugar_active(girl):
            return True
        return getattr(girl, "_financial_times", 0) >= 1

    def _se_charge_accepts(girl):
        obed = getattr(girl, "Obed", 0)
        base_chance = min(0.70, 0.15 + obed / 2000.0)
        if girl.has_trait("rich"):
            base_chance += 0.25
        elif girl.has_trait("poor"):
            base_chance -= 0.20
        return renpy.random.random() <= max(0.05, min(0.90, base_chance))

    # ============================================================
    # CONDITION CHECKS
    # ============================================================

    def _se_can_condom_force(girl):
        """Girl forcefully removes condom... high Inbt + experienced."""
        if not store.condom_active:
            return False
        if store._sub_event_condom_fired:
            return False
        if girl.has_trait("hate_cum"):
            return False
        raw = getattr(girl, "raw_sex_count", 0)
        inbt = getattr(girl, "Inbt", 0)
        obed = getattr(girl, "Obed", 0)
        if raw < 5:
            return False
        if inbt < 600:
            return False
        if obed < 300 and not girl.has_trait("cum_slut"):
            return False
        return True

    def _se_can_condom_ask(girl):
        """Girl asks to remove condom... moderate Inbt."""
        if not store.condom_active:
            return False
        if store._sub_event_condom_fired:
            return False
        if girl.has_trait("hate_cum"):
            return False
        raw = getattr(girl, "raw_sex_count", 0)
        inbt = getattr(girl, "Inbt", 0)
        if raw < 2:
            return False
        if inbt < 400 and not girl.has_trait("cum_slut"):
            return False
        return True

    def _se_can_condom_hate_cum(girl):
        """hate_cum girl removes condom herself if experienced enough.
        She wants raw but still blocks creampie. Requires high raw count
        since she genuinely dislikes cum — it takes a lot to get her here."""
        if not store.condom_active:
            return False
        if store._sub_event_condom_fired:
            return False
        if not girl.has_trait("hate_cum"):
            return False
        cream = getattr(girl, "CreampieCounts", 0)
        raw = getattr(girl, "raw_sex_count", 0)
        if cream >= 6 or raw >= 12:
            return True
        return False

    def _se_can_creampie_request(girl):
        """Girl expresses desire for creampie."""
        if store.condom_active:
            return False
        if store._sub_event_creampie_fired:
            return False
        if not girl.has_trait("cum_slut"):
            return False
        cream = getattr(girl, "CreampieCounts", 0)
        inbt = getattr(girl, "Inbt", 0)
        if cream < 3:
            return False
        if inbt < 400:
            return False
        return True

    def _se_can_position_change(girl, scene_type):
        """Girl suggests switching to her FavoriteAct. Only during full sex, not rub/tip."""
        if store._sub_event_position_fired:
            return False
        if store._sub_event_actions_taken < 8:
            return False
        # No position switch during anal (cowgirl/RCG don't support anal)
        if scene_type in _ANAL_SCENE_TYPES:
            return False
        if _any_rub_or_tip_active():
            return False
        fav = getattr(girl, "FavoriteAct", None)
        if fav not in ("cowgirl", "reverse_cowgirl", "doggy", "laying_down"):
            return False
        if fav == scene_type:
            return False
        if fav == "doggy" and scene_type in ("doggy", "anal"):
            return False
        if fav == "laying_down" and scene_type in ("laying_down", "laying_anal"):
            return False
        if not girl_has_pose(girl, fav):
            return False
        return True

    def _se_can_pace_request(girl, scene_type):
        """Girl asks for pace change based on personality."""
        _tv = _cum_cfg(scene_type, "tip_mode_var")
        if _tv and getattr(store, _tv, False):
            return False
        _sv = _cum_cfg(scene_type, "speed_var")
        if not _sv:
            return False
        speed = getattr(store, _sv, 0)
        if girl.has_trait("hardcore_sex"):
            return speed < _cum_cfg(scene_type, "max_speed", 3)
        if girl.has_trait("cute_sex"):
            return speed >= 2
        return False

    def _se_can_recording_request(girl, scene_type):
        """camera_lover girl asks player to start recording.
        Only triggers after enough sex acts without being recorded --
        she won't mention cameras unprompted until then."""
        if store._sub_event_recording_fired:
            return False
        if store._recording_active:
            return False
        if store._fn_girl is not None and not Player.has_item("tripod"):
            return False
        if not girl.has_trait("camera_lover"):
            return False
        # Need at least 3 sex acts before she starts asking
        sa = getattr(girl, "Sex_acts", {}) or {}
        _total_sex = sum(sa.get(k, 0) for k in ("hj", "bj", "tj", "sex", "anal"))   # acts only: a position would count the scene twice
        if _total_sex < SEX_HISTORY_THRESHOLDS["recording_request_acts"]:
            return False
        # She only asks if she has NEVER been recorded before
        _ever_recorded = any(
            v.get("girl_gid") == girl.gid
            for v in getattr(store.Player, "recorded_videos", [])
        )
        if _ever_recorded:
            return False
        inbt = getattr(girl, "Inbt", 0)
        if inbt < 300:
            return False
        return True

    # ── hate_cum: girl warns about cum ──
    def _should_trigger_cum_warning(girl, scene):
        """hate_cum girl warns player not to cum on/inside her."""
        if not girl.has_trait("hate_cum"):
            return False
        sa = getattr(store, "scene_actions", 0)
        if sa < 5:
            return False
        # Only trigger once per scene
        if getattr(store, "_cum_warning_done", False):
            return False
        return renpy.random.randint(1, 100) <= 30

    # ── virgin nervousness: virgin panics mid-scene ──
    # Every vaginal position is the "sex" act: "is this her first time?" never reads a position counter
    _SCENE_TO_ACT = {
        "cowgirl": "sex", "reverse_cowgirl": "sex",
        "doggy": "sex", "laying_down": "sex",
        "bj": "bj", "hj": "hj", "tj": "tj",
        "anal": "anal", "full_nelson": "sex",
        "full_nelson_anal": "anal", "laying_anal": "anal",
        "reverse_cowgirl_anal": "anal",
    }

    def _should_trigger_virgin_nervous(girl, scene):
        """Virgin girl gets nervous during her first time."""
        if not girl.has_trait("virgin"):
            return False
        if _any_rub_or_tip_active():
            return False
        act = _SCENE_TO_ACT.get(scene, "")
        if not act:
            return False
        acts = getattr(girl, "Sex_acts", {})
        if acts.get(act, 0) > 1:
            return False
        if getattr(store, "_virgin_nervous_done", False):
            return False
        return renpy.random.randint(1, 100) <= 40

    # ── public panic: public_shy girl panics ──
    def _should_trigger_public_panic(girl, scene):
        """public_shy girl panics about being seen in public."""
        if not girl.has_trait("public_shy"):
            return False
        _loc = getattr(store, "CurrentLocation", "room")
        if _loc not in ("classroom", "campus", "party", "gym", "street", "mall", "pool", "showers", "shower"):
            return False
        if getattr(store, "_public_panic_done", False):
            return False
        return renpy.random.randint(1, 100) <= 35

    # ── ATM initiative: girl with all positive traits asks for ATM ──
    def _se_can_atm_initiative(girl, scene_type):
        """Girl with anal_lover+cum_slut+hardcore who has done ATM 3+ times asks for it."""
        if getattr(store, "_sub_event_atm_initiative_fired", False):
            return False
        if scene_type not in _ANAL_SCENE_TYPES:
            return False
        if not any(getattr(store, _af, False) for _af in _ANAL_FLAGS.values()):
            return False
        if not (girl.has_trait("anal_lover") and girl.has_trait("cum_slut") and girl.has_trait("hardcore_sex")):
            return False
        if getattr(girl, "_atm_count", 0) < 3:
            return False
        # the scene's own speed (CUM_POSITION_CONFIG speed_var): it used to read a "dg_speed" that never existed, so
        # the doggy's ATM initiative could never fire; the laying down and the reverse cowgirl never had a branch
        _spd = _cum_get_speed(scene_type)
        if _spd < 2:
            return False
        return True

    # ── anal request: anal_lover girl asks for anal ──
    # What "now it is anal" means in each position the request runs in: that scene's own flags (its hole
    # transition, _cum_dispatch_hole_transition, does the animation; FN_HoleTransition also sets fn_anal and
    # _fn_had_anal). A position missing here falls back to doggy.
    _SE_ANAL_SWITCH = {
        "doggy":       {"_dg_had_anal": True, "_dg_scene_type": "anal"},
        "laying_down": {"_ld_had_anal": True, "_ld_scene_type": "laying_anal"},
        "full_nelson": {"_fn_scene_type": "full_nelson_anal"},
        # the reverse cowgirl keeps nothing of its own: RCG_HoleTransition sets rcg_anal, RCG_ApplySpeed _rcg_had_anal
        "reverse_cowgirl": {},
    }

    def _se_switch_to_anal(girl, scene_type):
        """The anal request's switch, every answer that says yes: the position's flags, the act, no condom."""
        for _var, _val in _SE_ANAL_SWITCH.get(scene_type, _SE_ANAL_SWITCH["doggy"]).items():
            setattr(store, _var, _val)
        mark_intimacy(girl, "anal")
        store.condom_active = False
        store.condom_denied = False
        print("[SUBEVENT_ANAL] %s: switching to anal, scene_type=%s" % (girl.gid, scene_type))

    def _se_can_anal_request(girl, scene_type):
        """anal_lover / anal_preference girl asks player to switch to anal during vaginal sex."""
        if getattr(store, "_sub_event_anal_request_fired", False):
            if getattr(girl, "_anal_preference", 0) < 3:
                return False
            # Stage 3 (addicted): can fire again after switching back to vaginal
            pass
        if any(getattr(store, _af, False) for _af in _ANAL_FLAGS.values()):
            return False
        if not girl.has_trait("anal_lover") and getattr(girl, "_anal_preference", 0) < 1:
            return False
        if scene_type not in _SE_ANAL_SWITCH:
            return False
        # the reverse cowgirl: only a girl whose own art has anal in that pose (Core_RCG rcg_has_anal)
        if scene_type == "reverse_cowgirl" and not rcg_has_anal(girl):
            return False
        # while he is inside her only: the rub / tip menus tick sub-events too, and a switch from there would leave
        # the position in rub or tip mode (the position's own escalation is the way out of those)
        if getattr(store, "_scene_phase", None) in _NON_PENETRATION_PHASES:
            return False
        # Vaginal sex scenes = the "sex" act. Positions are preferences (and doggy/laying_down are not Sex_acts keys)
        _total = girl_sex_count(girl)
        if _total < SEX_HISTORY_THRESHOLDS["anal_request_sex"]:
            return False
        if getattr(girl, "Inbt", 0) < 250:
            return False
        return True

    def _se_can_ntr_request_raw(girl):
        if not store.condom_active:
            return False
        if getattr(store, "_sub_event_ntr_raw_fired", False):
            return False
        if getattr(store, "_sub_event_condom_fired", False):
            return False
        if getattr(store, "_ntr_partner_watching", False):
            return False
        if not hasattr(girl, "has_npc_partner") or not girl.has_npc_partner():
            return False
        _npc = get_npc_partner_for(girl)
        if not _npc or not getattr(_npc, "_ntr_active", False):
            return False
        if getattr(_npc, "_ntr_boundary_level", 1) != 2:
            return False
        if girl.has_trait("cheater"):
            return False
        if girl.has_trait("hate_cum"):
            return False   # she demands condoms: never the one asking to go raw (same rule as the NTR gate)
        _obed = getattr(girl, "Obed", 0)
        _lust = getattr(girl, "Lust", 0)
        _love = getattr(girl, "Love", 0)
        if girl.has_trait("cum_slut"):
            return _obed >= 500 or (_lust >= 70 and _love >= 400)
        return _obed >= 700 or (_lust >= 80 and _love >= 600)

    def _se_can_ntr_request_creampie(girl):
        if store.condom_active:
            return False
        if getattr(store, "_sub_event_ntr_creampie_fired", False):
            return False
        if getattr(store, "_sub_event_creampie_fired", False):
            return False
        if getattr(store, "_ntr_partner_watching", False):
            return False
        if not hasattr(girl, "has_npc_partner") or not girl.has_npc_partner():
            return False
        _npc = get_npc_partner_for(girl)
        if not _npc or not getattr(_npc, "_ntr_active", False):
            return False
        if getattr(_npc, "_ntr_boundary_level", 1) != 3:
            return False
        if girl.has_trait("cheater"):
            return False
        _obed = getattr(girl, "Obed", 0)
        _lust = getattr(girl, "Lust", 0)
        _love = getattr(girl, "Love", 0)
        if girl.has_trait("cum_slut"):
            return _obed >= 400 or (_lust >= 60 and _love >= 300)
        return _obed >= 700 or (_lust >= 80 and _love >= 600)

    def _se_can_watcher_condom_remove(girl, scene_type):
        """Watcher girl removes condom during threesome."""
        if not store.condom_active:
            return False
        if getattr(store, "_sub_event_condom_fired", False):
            return False
        if getattr(store, "_sub_event_watcher_condom_fired", False):
            return False
        if not getattr(store, "_witness_watching", False):
            return False
        if getattr(store, "_ntr_partner_watching", False) and getattr(store, "_ntr_watching_npc", None):
            _wc_npc = store._ntr_watching_npc
            if getattr(_wc_npc, "_ntr_boundary_level", 1) <= 2:
                print("[SE_WATCHER_CONDOM] BLOCKED: NTR partner %s watching at level %d" % (_wc_npc.name, _wc_npc._ntr_boundary_level))
                return False
        _watcher = getattr(store, "_witness_girl", None)
        if _watcher is None:
            return False
        if _watcher.is_dating_player():
            if girl.is_dating_player():
                if not is_harem_exempt(_watcher, girl):
                    print("[SE_WATCHER_CONDOM] BLOCKED: watcher %s hasn't accepted %s in harem" % (_watcher.gid, girl.gid))
                    return False
            else:
                if not is_player_harem_exempt(girl):
                    print("[SE_WATCHER_CONDOM] BLOCKED: %s not harem-exempt" % girl.gid)
                    return False
        _raw = getattr(_watcher, "raw_sex_count", 0)
        if _raw <= 3 and not _watcher.has_trait("cum_slut"):
            print("[SE_WATCHER_CONDOM] BLOCKED: watcher %s raw=%d cum_slut=%s" % (_watcher.gid, _raw, _watcher.has_trait("cum_slut")))
            return False
        print("[SE_WATCHER_CONDOM] ELIGIBLE: watcher=%s active=%s condom=%s raw=%d cum_slut=%s" % (_watcher.gid, girl.gid, store.condom_active, _raw, _watcher.has_trait("cum_slut")))
        return True

    def _se_can_pillow_request(girl, scene_type):
        if scene_type not in ("laying_down", "laying_anal"):
            return False
        if getattr(store, "_sub_event_pillow_fired", False):
            return False
        if getattr(store, "_ld_pillow_active", False):
            return False
        _loc = getattr(store, "CurrentLocation", "room")
        if _loc not in ("room", GIRL_ROOMS.get(girl.gid, "")):
            return False
        if girl.gid != "tenny":
            return False
        return True

    def _se_pillow_weight(girl):
        w = 15
        if girl.has_trait("cute_sex"):
            w += 15
        if getattr(store, "laying_anal", False) or getattr(store, "laying_speed", 0) >= 3:
            w += 10
        return w

    # ============================================================
    # DISPATCHER
    # ============================================================

    def sub_event_dispatch(girl, scene_type):
        """Pick which sub-event fires (or None). condom_force is deterministic.
        A scene whose CUM_POSITION_CONFIG lists "sub_events" (hj / bj / tj / fj) only rolls those."""
        if getattr(store, "_bet_event_active", False):
            return None
        _allowed = CUM_POSITION_CONFIG.get(scene_type, {}).get("sub_events")

        # Highest priority: deterministic forced condom removal (her step first, like every other candidate)
        if ((_allowed is None or "condom_force" in _allowed) and _se_can_condom_force(girl)
                and not story_act_locked(girl, STORY_SUBEVENT_ACT.get("condom_force"))):
            return "condom_force"

        # Build weighted pool of eligible events
        candidates = []
        if _se_can_condom_hate_cum(girl):
            candidates.append(("condom_hate_cum", 35))
        if _se_can_condom_ask(girl):
            candidates.append(("condom_ask", 40))
        if _se_can_creampie_request(girl):
            candidates.append(("creampie", 30))
        if _se_can_position_change(girl, scene_type):
            candidates.append(("position", 20))
        if _se_can_pace_request(girl, scene_type):
            candidates.append(("pace", 15))
        if _se_can_recording_request(girl, scene_type):
            candidates.append(("recording_request", 25))
        if _should_trigger_cum_warning(girl, scene_type):
            candidates.append(("cum_warning", 30))
        if _should_trigger_virgin_nervous(girl, scene_type):
            candidates.append(("virgin_nervous", 35))
        if _should_trigger_public_panic(girl, scene_type):
            candidates.append(("public_panic", 30))
        if _se_can_atm_initiative(girl, scene_type):
            candidates.append(("atm_initiative", 20))
        if _se_can_anal_request(girl, scene_type):
            _se_anal_w = 25 + getattr(girl, "_anal_preference", 0) * 15
            candidates.append(("anal_request", _se_anal_w))
        if _se_can_ntr_request_raw(girl):
            candidates.append(("ntr_request_raw", 30))
        if _se_can_ntr_request_creampie(girl):
            candidates.append(("ntr_request_creampie", 30))
        if _se_can_watcher_condom_remove(girl, scene_type):
            candidates.append(("watcher_condom_remove", 35))
        if _se_can_pillow_request(girl, scene_type):
            candidates.append(("pillow_request", _se_pillow_weight(girl)))
        # a married girl calls her husband while he is inside her (shion_netori.rpy)
        if _se_can_netori_call(girl, scene_type):
            candidates.append(("netori_call", NETORI_CALL_WEIGHT))
        # Her orders, femdom only (Actions/femdom.rpy): they join only some rolls, capped per session
        candidates.extend(femdom_order_candidates(girl, scene_type))
        # Her asks for HIS direction, submissive only (the mirror, Actions/femdom.rpy subm_candidates)
        candidates.extend(subm_candidates(girl, scene_type))

        if _allowed is not None:
            candidates = [c for c in candidates if c[0] in _allowed]
        # her step (story_steps.rpy): nothing of hers above it
        candidates = [c for c in candidates if not story_act_locked(girl, STORY_SUBEVENT_ACT.get(c[0]))]

        if not candidates:
            return None

        # Weighted random selection
        total = sum(w for _cand, w in candidates)
        roll = renpy.random.randint(1, total)
        cumulative = 0
        for event_name, weight in candidates:
            cumulative += weight
            if roll <= cumulative:
                return event_name
        return candidates[-1][0]

    def sub_event_tick(girl, scene_type):
        """Called each action tick. Returns event name or None."""
        store._sub_event_actions_taken += 1
        store._sub_event_cooldown -= 1

        # Femdom: he held it as long as she told him to ("femdom_release" skips the cooldown: it is her answer)
        _fd = femdom_tick(girl)
        if _fd:
            return _fd

        # Her story (story_steps.rpy, "sex"): an event of her step that happens during sex (her husband calls)
        _st = story_event_now("sex", girl)
        if _st is not None:
            store._story_sex_event = _st[1]
            store._sub_event_cooldown = renpy.random.randint(3, 5)
            return "story"

        if store._sub_event_cooldown > 0:
            return None

        event = sub_event_dispatch(girl, scene_type)
        if event:
            # Reset cooldown after firing
            store._sub_event_cooldown = renpy.random.randint(3, 5)
        else:
            # No event eligible, try again in 1-2 ticks
            store._sub_event_cooldown = renpy.random.randint(1, 2)
        return event

    def sub_event_reset(girl=None):
        """Reset all sub-event state for a new scene. Every scene launch calls it (a position switch
        launches too): nothing from the last scene may keep a request from firing in this one."""
        if girl is not None:
            girl._ignored_pace_requests = 0
        store._sub_event_atm_initiative_fired = False
        store._sub_event_cooldown = renpy.random.randint(2, 4)
        store._sub_event_actions_taken = 0
        store._sub_event_condom_fired = False
        store._subm_asks_done = 0
        store._sugar_scene_paid = 0
        count_slaps_reset("scene launch")
        store._sub_event_creampie_fired = False
        store._sub_event_position_fired = False
        store._sub_event_position_switched = False
        store._girl_requested_creampie = False
        store._sub_event_recording_fired = False
        store._cum_warning_done = False
        store._virgin_nervous_done = False
        store._public_panic_done = False
        store._sub_event_anal_request_fired = False
        store._moan_cooldown = 0
        store._lesbian_coldness_done = False
        store._sub_event_ntr_raw_fired = False
        store._sub_event_ntr_creampie_fired = False
        store._sub_event_watcher_condom_fired = False
        store._sub_event_pillow_fired = False

# ============================================================
# TICK FOR THE SCENES WHERE HE IS NOT INSIDE HER (hj / bj / tj / fj)
# Only what the scene's CUM_POSITION_CONFIG "sub_events" lists. In a BJ her mouth is busy:
# the animation pauses while she talks (same as _moan_say). The caller ends the scene when
# store._sst_result comes back "abort" (the pace request's "Charge her" can end it).
# ============================================================
label _sub_event_tick_nonpen(girl, scene_type):
    $ store._sst_result = "continue"
    $ _se_np = sub_event_tick(girl, scene_type)
    if not _se_np:
        return
    $ print("[SUBEVENT] %s: %s in %s" % (girl.gid, _se_np, scene_type))
    $ _se_np_bj_speed = getattr(store, "bj_speed", 0) if getattr(store, "_bj_girl", None) is girl else 0
    if _se_np_bj_speed > 0:
        $ _se_np_force = _bj_pause_forcing()
        call BJ_ApplySpeed(girl, 0) from _call_se_np_bj_pause
    call SubEvent_Handle(girl, scene_type, _se_np) from _call_SubEvent_Handle_np
    if _se_np_bj_speed > 0:
        $ _bj_resume_forcing(_se_np_force)
        call BJ_ApplySpeed(girl, _se_np_bj_speed) from _call_se_np_bj_resume
    return

# ============================================================
# HANDLER ROUTER
# ============================================================
label SubEvent_Handle(girl, scene_type, event_name):
    if event_name == "condom_force":
        call SubEvent_CondomForceRemove(girl, scene_type) from _call_SubEvent_CondomForceRemove
    elif event_name == "condom_ask":
        call SubEvent_CondomAskRemove(girl, scene_type) from _call_SubEvent_CondomAskRemove
    elif event_name == "condom_hate_cum":
        call SubEvent_CondomHateCumRemove(girl, scene_type) from _call_SubEvent_CondomHateCumRemove
    elif event_name == "creampie":
        call SubEvent_CreampieRequest(girl, scene_type) from _call_SubEvent_CreampieRequest
    elif event_name == "position":
        call SubEvent_PositionChange(girl, scene_type) from _call_SubEvent_PositionChange
    elif event_name == "pace":
        call SubEvent_PaceRequest(girl, scene_type) from _call_SubEvent_PaceRequest
    elif event_name == "recording_request":
        call SubEvent_RecordingRequest(girl, scene_type) from _call_SubEvent_RecordingRequest
    elif event_name == "cum_warning":
        call sub_cum_warning(girl) from _call_sub_cum_warning
    elif event_name == "virgin_nervous":
        call sub_virgin_nervous(girl) from _call_sub_virgin_nervous
    elif event_name == "public_panic":
        call sub_public_panic(girl) from _call_sub_public_panic
    elif event_name == "anal_request":
        call SubEvent_AnalRequest(girl, scene_type) from _call_SubEvent_AnalRequest
    elif event_name == "atm_initiative":
        call SubEvent_ATMInitiative(girl, scene_type) from _call_SubEvent_ATMInitiative
    elif event_name == "ntr_request_raw":
        call SubEvent_NTRRequestRaw(girl, scene_type) from _call_SubEvent_NTRRequestRaw
    elif event_name == "ntr_request_creampie":
        call SubEvent_NTRRequestCreampie(girl, scene_type) from _call_SubEvent_NTRRequestCreampie
    elif event_name == "watcher_condom_remove":
        call SubEvent_WatcherCondomRemove(girl, scene_type) from _call_SubEvent_WatcherCondomRemove
    elif event_name == "pillow_request":
        call SubEvent_PillowRequest(girl, scene_type) from _call_SubEvent_PillowRequest
    elif event_name == "netori_call":
        call SubEvent_NetoriCall(girl, scene_type) from _call_SubEvent_NetoriCall
    elif event_name == "story":
        call story_event_play(girl, store._story_sex_event) from _call_story_event_sex
    elif event_name == "femdom_release":
        call _femdom_edge_release(girl, scene_type) from _call_femdom_edge_release
    elif event_name.startswith("femdom_"):
        call SubEvent_FemdomOrder(girl, scene_type, event_name) from _call_SubEvent_FemdomOrder
    elif event_name.startswith("subm_"):
        # the submissive mirror: she asks HIM to direct her (Actions/femdom.rpy)
        call SubEvent_SubmAsk(girl, scene_type, event_name) from _call_SubEvent_SubmAsk
    return

# ============================================================
# CONDOM FORCE REMOVE
# ============================================================
label SubEvent_CondomForceRemove(girl, scene_type):
    # All cheat paths: condom stays until breaking point
    if _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False):
        return

    # NPC watching: can't force — redirect to ask-NPC flow
    if store._ntr_partner_watching and store._ntr_watching_npc:
        call _ntr_girl_ask_npc(girl, store._ntr_watching_npc, "condom_remove") from _call_ntr_ask_npc_condom_force
        $ store._sub_event_condom_fired = True
        if store._ntr_npc_authorized:
            menu:
                "Remove the condom":
                    $ set_scene_expression(girl, "lewd", blush="2")
                    "You nod and pull the condom off."
                    $ _on_condom_removed(girl, skip_hide=_cum_skip_hide(scene_type))
                    $ apply_cum_bonuses(girl, "condom_removed_allowed")
                    $ store._creampie_consent = "allowed"
                    call _ntr_authorized_done(girl, store._ntr_watching_npc, "condom_remove") from _call_ntr_auth_done_cf
                "Keep it on":
                    $ set_scene_expression(girl, "sad")
                    $ Say_Line(girl, _format_npc_line(store._ntr_watching_npc, renpy.random.choice([_("But... %(pp)s said it was okay..."), _("Why not? %(Pp)s already agreed...")])))
                    $ Change_Status(girl, "Love", -3)
        else:
            menu:
                "Remove it anyway":
                    $ set_scene_expression(girl, "pleasure_intense", blush="2")
                    $ renpy.say(None, _tl_fmt(_("You pull the condom off despite %s objection."), _npc_poss(store._ntr_watching_npc)))
                    $ _on_condom_removed(girl, skip_hide=_cum_skip_hide(scene_type))
                    $ apply_cum_bonuses(girl, "condom_removed_allowed")
                    $ store._creampie_consent = "allowed"
                    call _ntr_agreement_broken(girl, store._ntr_watching_npc, "condom_remove") from _call_ntr_broken_cf
                "Respect [_ntr_npc_poss] decision":
                    call _ntr_boundary_respected(girl, store._ntr_watching_npc) from _call_ntr_respected_cf
        if not store.condom_active:
            call _sex_scene_condom_rip_visual(girl, scene_type) from _call_crv_ntr_force
        return

    $ store._sub_event_condom_fired = True
    $ _line = scene_pick_line("condom_force", scene=scene_type, girl=girl)
    $ Say_Line(girl, _line)
    "She reaches down and pulls the condom off before you can react."
    $ _on_condom_removed(girl, skip_hide=_cum_skip_hide(scene_type))
    $ apply_cum_bonuses(girl, "condom_removed_allowed")
    $ store._creampie_consent = "allowed"

    call _sex_scene_condom_rip_visual(girl, scene_type) from _call_crv_sub_force
    return

# ============================================================
# CONDOM ASK REMOVE
# ============================================================
label SubEvent_CondomAskRemove(girl, scene_type):
    if _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False):
        return

    # NPC watching: girl asks NPC instead of player
    if store._ntr_partner_watching and store._ntr_watching_npc:
        call _ntr_girl_ask_npc(girl, store._ntr_watching_npc, "condom_remove") from _call_ntr_ask_npc_condom_ask
        $ store._sub_event_condom_fired = True
        if store._ntr_npc_authorized:
            menu:
                "Remove the condom":
                    $ set_scene_expression(girl, renpy.random.choice(["ahegao", "ahegao_2"]), blush="2")
                    "You nod and pull the condom off."
                    $ _on_condom_removed(girl, skip_hide=_cum_skip_hide(scene_type))
                    $ apply_cum_bonuses(girl, "condom_removed_allowed")
                    $ store._creampie_consent = "allowed"
                    call _ntr_authorized_done(girl, store._ntr_watching_npc, "condom_remove") from _call_ntr_auth_done_ca
                "Keep it on":
                    $ set_scene_expression(girl, "sad")
                    $ Say_Line(girl, _format_npc_line(store._ntr_watching_npc, renpy.random.choice([_("But... %(pp)s said it was okay..."), _("Why not? %(Pp)s already agreed...")])))
                    $ Change_Status(girl, "Love", -3)
        else:
            menu:
                "Remove it anyway":
                    $ set_scene_expression(girl, renpy.random.choice(["ahegao", "ahegao_2"]), blush="2")
                    $ renpy.say(None, _tl_fmt(_("You pull the condom off despite %s objection."), _npc_poss(store._ntr_watching_npc)))
                    $ _on_condom_removed(girl, skip_hide=_cum_skip_hide(scene_type))
                    $ apply_cum_bonuses(girl, "condom_removed_allowed")
                    $ store._creampie_consent = "allowed"
                    call _ntr_agreement_broken(girl, store._ntr_watching_npc, "condom_remove") from _call_ntr_broken_ca
                "Respect [_ntr_npc_poss] decision":
                    call _ntr_boundary_respected(girl, store._ntr_watching_npc) from _call_ntr_respected_ca
        if not store.condom_active:
            call _sex_scene_condom_rip_visual(girl, scene_type) from _call_crv_ntr_ask
        return

    $ store._sub_event_condom_fired = True
    $ _line = scene_pick_line("condom_ask", scene=scene_type, girl=girl)
    $ Say_Line(girl, _line)

    menu:
        "Let her remove it":
            $ set_scene_expression(girl, renpy.random.choice(["ahegao", "ahegao_2"]), blush="2")
            "You nod and she eagerly pulls it off."
            $ _on_condom_removed(girl, skip_hide=_cum_skip_hide(scene_type))
            $ apply_cum_bonuses(girl, "condom_removed_allowed")
            $ store._creampie_consent = "allowed"
            call _sex_scene_condom_rip_visual(girl, scene_type) from _call_crv_sub_ask

        "Keep it on":
            call _femdom_refused_react(girl, "condom", scene_type) from _call_fdr_condom
            if not store._femdom_refused:
                $ set_scene_expression(girl, "sad")
                $ _line = scene_pick_line("condom_denied", scene=scene_type, girl=girl)
                $ Say_Line(girl, _line)

        "Charge her $[_se_charge_now]" if _se_can_charge(girl) and sugar_charge_quote(girl, ("anal" if _tease_is_anal_scene(scene_type) else "sex")):
            $ Say_Player(_tl(_("You want the condom off? Pay me $%d.")) % store._se_charge_now)
            $ set_scene_expression(girl, "surprised")
            python:
                _charge_ok = sugar_charge_accepts(girl)   # a sugar girl pays almost always (sugar_mommy.rpy)
            if _charge_ok:
                $ sugar_charge_paid(girl, "condom_off")
                $ set_scene_expression(girl, renpy.random.choice(["ahegao", "ahegao_2"]), blush="2")
                $ Say_Line(girl, renpy.random.choice([_("...Fine. Take the money. Now take it off."), _("I'm paying to feel you raw...? Here. Just do it."), _("You're unbelievable... take it. Now rip that thing off.")]))
                $ _on_condom_removed(girl, skip_hide=_cum_skip_hide(scene_type))
                $ apply_cum_bonuses(girl, "condom_removed_allowed")
                $ store._creampie_consent = "allowed"
                $ Change_Status(girl, "Obed", 5)
                call _sex_scene_condom_rip_visual(girl, scene_type) from _call_crv_sub_charge
            else:
                python:
                    _refuse_roll = renpy.random.random()
                if _refuse_roll < 0.3:
                    $ set_scene_expression(girl, "angry")
                    $ Say_Line(girl, renpy.random.choice([_("Pay YOU to go raw? That's it. We're done."), _("You want me to pay for that? Disgusting. Get off.")]))
                    $ Change_Status(girl, "Love", -10)
                    $ store._sst_result = "abort"
                    $ store._sst_abort_reason = "hate_cum"
                else:
                    $ set_scene_expression(girl, "angry")
                    $ Say_Line(girl, renpy.random.choice([_("No. Keep the condom on then. Whatever."), _("I'm not paying for that. Just keep going.")]))
                    $ Change_Status(girl, "Obed", 3)
    return

# ============================================================
# CONDOM HATE_CUM REMOVE — she removes it herself but forbids
# finishing inside. Fires when cream >= 3 or raw >= 7.
# ============================================================
label SubEvent_CondomHateCumRemove(girl, scene_type):
    if _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False):
        return
    $ store._sub_event_condom_fired = True

    python:
        _has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        _player_gf = player_has_girlfriend(ALL_GIRLS) and not girl.is_dating_player() and not is_player_harem_exempt(girl)

        if _has_bf and _player_gf:
            _hcr_lines = [
                _("We're already doing something horrible... take it off. But don't you DARE cum inside me."),
                _("My %(pl)s uses a condom. Your girlfriend probably makes you too. Take it off... but pull out."),
            ]
        elif _has_bf:
            _hcr_lines = [
                _("%(Pp)s always uses protection with me... but I want to feel you. Take it off. But NOT inside. Got it?"),
                _("I'm already cheating... might as well feel the real thing. Take it off. But you pull out or we're done."),
            ]
        elif _player_gf:
            _hcr_lines = [
                _("Your girlfriend lets you go raw? Whatever. Take it off. But you're pulling out. No exceptions."),
                _("Fine... take it off. But this doesn't mean you can cum inside. Save that for your girlfriend."),
            ]
        else:
            _hcr_lines = [
                _("Take it off... I want to feel you. But this does NOT mean you can finish inside me."),
                _("I want it raw... but don't get any ideas. You cum inside me and I'll kill you."),
                _("Pull it off. I want the real thing. But you pull out when it's time. I mean it."),
                _("Take it off already... but this doesn't mean you can cum inside. Don't even think about it."),
                _("Fine, I can't take it anymore... take it off. But NOT inside. I swear, not a single drop."),
            ]
        # _format_partner_line gives every partner key (pl, Pp, pp...): the PT / ES pairs use %(Pp)s, and formatting
        # with {"pl": ...} alone raised KeyError there. Without a partner the lines carry no placeholder.
        _hcr_raw = renpy.random.choice(_hcr_lines)
        _hcr_line = _format_partner_line(girl, _hcr_raw) if _has_bf else _tl(_hcr_raw)

    $ Say_Line(girl, _hcr_line)
    "She reaches down and removes the condom herself."
    $ _on_condom_removed(girl, skip_hide=_cum_skip_hide(scene_type))
    $ apply_cum_bonuses(girl, "condom_removed_allowed")
    $ girl.discover("discovered_trait_hate_cum") if girl.has_trait("hate_cum") else None
    $ unlock_achievement("change_of_heart")
    $ store._creampie_consent = "blocked"

    call _sex_scene_condom_rip_visual(girl, scene_type) from _call_crv_sub_hatecum
    return

# ============================================================
# WATCHER CONDOM REMOVE (threesome)
# ============================================================
label SubEvent_WatcherCondomRemove(girl, scene_type):
    $ store._sub_event_watcher_condom_fired = True
    $ store._sub_event_condom_fired = True
    $ _watcher = store._witness_girl

    "[_watcher.Name] moves closer to both of you."

    $ Say_Line(_watcher, _("Come on, [girl.Name], you're a big girl. Time for some real action."))

    $ set_scene_expression(girl, "surprised")
    $ Say_Line(girl, _("What? What are you..."))

    "[_watcher.Name] reaches down, pulls the condom off and guides you back inside [girl.Name]."

    $ _on_condom_removed(girl, skip_hide=_cum_skip_hide(scene_type), force=True)

    call _sex_scene_condom_rip_visual(girl, scene_type) from _call_crv_watcher

    $ set_scene_expression(girl, "ahegao", blush="2")
    $ Say_Line(girl, _("Oh my God, [_watcher.Name]... this is dangerous... Holy... this is SO GOOD! Don't stop!"))

    $ girl.Lust = min(100, girl.Lust + 20)
    $ apply_cum_bonuses(girl, "condom_removed_allowed")
    $ store._creampie_consent = "allowed"
    $ unlock_achievement("helping_hand")
    $ print("[SE_WATCHER_CONDOM] %s removed condom from %s (raw=%d, cum_slut=%s)" % (_watcher.gid, girl.gid, getattr(_watcher, "raw_sex_count", 0), _watcher.has_trait("cum_slut")))
    return

# ============================================================
# CREAMPIE REQUEST
# ============================================================
label SubEvent_CreampieRequest(girl, scene_type):
    $ store._sub_event_creampie_fired = True
    # the event only fires for a cum_slut (_se_can_creampie_request): her ask IS the trait showing
    $ girl.discover("discovered_trait_cum_slut") if girl.has_trait("cum_slut") else None

    # NPC watching: girl asks NPC for creampie permission
    if store._ntr_partner_watching and store._ntr_watching_npc:
        call _ntr_girl_ask_npc(girl, store._ntr_watching_npc, "creampie") from _call_ntr_ask_npc_creampie
        if store._ntr_npc_authorized:
            menu:
                "I'll cum inside her":
                    $ set_scene_expression(girl, renpy.random.choice(["ahegao", "ahegao_2"]), blush="3")
                    $ Change_Status(girl, "Love", 10)
                    $ Change_Status(girl, "Inbt", 15)
                    $ store._girl_requested_creampie = True
                    $ store._creampie_consent = "allowed"
                    $ Say_Line(girl, renpy.random.choice([_("Yes... give it all to me..."), _("I want every drop..."), _("Don't hold back...")]))
                    call _ntr_authorized_done(girl, store._ntr_watching_npc, "creampie") from _call_ntr_auth_done_cr
                "I'll pull out":
                    $ set_scene_expression(girl, "sad")
                    $ Say_Line(girl, _format_npc_line(store._ntr_watching_npc, renpy.random.choice([_("But... %(pp)s said it was okay..."), _("Why not? %(Pp)s already agreed...")])))
                    $ Change_Status(girl, "Love", -3)
        else:
            menu:
                "I'll cum inside her anyway":
                    $ set_scene_expression(girl, renpy.random.choice(["ahegao", "ahegao_2"]), blush="3")
                    $ Change_Status(girl, "Love", 10)
                    $ Change_Status(girl, "Inbt", 15)
                    $ store._girl_requested_creampie = True
                    $ store._creampie_consent = "allowed"
                    call _ntr_agreement_broken(girl, store._ntr_watching_npc, "creampie") from _call_ntr_broken_cr
                "Respect [_ntr_npc_poss] decision":
                    call _ntr_boundary_respected(girl, store._ntr_watching_npc) from _call_ntr_respected_cr
        return

    $ set_scene_expression(girl, "lusty")
    $ _line = scene_pick_line("creampie_req", scene=scene_type, girl=girl)
    $ Say_Line(girl, _line)

    menu:
        "I'll cum inside her":
            $ set_scene_expression(girl, renpy.random.choice(["ahegao", "ahegao_2"]), blush="3")
            $ Change_Status(girl, "Love", 10)
            $ Change_Status(girl, "Inbt", 15)
            $ store._girl_requested_creampie = True
            $ store._creampie_consent = "allowed"
            $ Say_Line(girl, renpy.random.choice([_("Yes... give it all to me..."), _("I want every drop..."), _("Don't hold back...")]))

        "I'll pull out":
            call _femdom_refused_react(girl, "creampie", scene_type) from _call_fdr_creampie
            if not store._femdom_refused:
                $ set_scene_expression(girl, "sad")
                $ Say_Line(girl, renpy.random.choice([_("Fine... pull out then..."), _("Really? I was hoping you would..."), _("Your loss...")]))
            $ Change_Status(girl, "Love", -3)

        "Charge her $[_se_charge_now]" if _se_can_charge(girl) and sugar_charge_quote(girl, ("anal" if _tease_is_anal_scene(scene_type) else "sex")):
            $ Say_Player(_tl(_("You want it inside? Pay me $%d.")) % store._se_charge_now)
            $ set_scene_expression(girl, "surprised")
            python:
                _charge_ok = sugar_charge_accepts(girl)   # a sugar girl pays almost always (sugar_mommy.rpy)
            if _charge_ok:
                $ sugar_charge_paid(girl, "creampie")
                $ set_scene_expression(girl, "sad")
                $ Say_Line(girl, renpy.random.choice([_("...I'm paying a man to cum inside me. Here."), _("You're really charging me for this...? Fine. Take it."), _("I want it that bad...? Apparently I do. Here's your money.")]))
                $ Change_Status(girl, "Love", 5)
                $ Change_Status(girl, "Obed", 5)
                $ store._girl_requested_creampie = True
                $ store._creampie_consent = "allowed"
            else:
                python:
                    _refuse_roll = renpy.random.random()
                if _refuse_roll < 0.3:
                    $ set_scene_expression(girl, "angry")
                    $ Say_Line(girl, renpy.random.choice([_("Pay YOU to cum inside ME? Are you out of your mind? We're done."), _("That's the most insulting thing anyone has ever said to me. Get off.")]))
                    $ Change_Status(girl, "Love", -10)
                    $ store._sst_result = "abort"
                    $ store._sst_abort_reason = "hate_cum"
                else:
                    $ set_scene_expression(girl, "angry")
                    $ Say_Line(girl, renpy.random.choice([_("I'm not paying for that. Just cum wherever you want."), _("No. Forget I asked. Do whatever.")]))
                    $ Change_Status(girl, "Obed", 3)
    return

# ============================================================
# POSITION CHANGE — shared execution (called from both accept and charge paths)
# ============================================================
label _se_execute_pos_switch(girl, scene_type):
    python:
        _saved_condom = condom_carry_save()   # the whole condom: type, break roll, stealth (the End below resets it)
        _was_tip_mode = store.doggy_tip_mode or store.cowgirl_tip_mode or store.rcg_tip_mode or getattr(store, "fn_tip_mode", False) or getattr(store, "laying_tip_mode", False)
        _saved_clothes = dict(girl.clothes)
        _saved_clothes_state = dict(girl.clothes_state)
        _saved_outfit_ref = getattr(girl, "_saved_outfit", None)

    call _cum_dispatch_end(girl, scene_type) from _call_end_pos_switch

    $ condom_carry_restore(_saved_condom)
    $ girl.clothes = _saved_clothes
    $ girl.clothes_state = _saved_clothes_state
    $ girl._saved_outfit = _saved_outfit_ref

    $ debug_log("[POS_SWITCH_SE] %s: %s -> %s tip=%s virgin=%s" % (girl.gid, scene_type, _fav, _was_tip_mode, girl.has_trait("virgin")))
    $ _scene_position_switch(girl, scene_type, _fav)

    if girl.has_trait("virgin") and _fav in ("cowgirl", "reverse_cowgirl", "doggy", "laying_down"):
        if _fav == "reverse_cowgirl":
            $ rcg_speed = 0
            call RCG_Launch(girl, from_switch=True) from _call_RCG_Launch_ps_v
        elif _fav == "cowgirl":
            $ cowgirl_speed = 0
            call COWGIRL_Launch(girl, from_switch=True) from _call_CG_Launch_ps_v
        elif _fav == "doggy":
            $ doggy_speed = 0
            call DG_Launch(girl, from_switch=True) from _call_DG_Launch_ps_v
        elif _fav == "laying_down":
            $ laying_speed = 0
            call LD_Launch(girl, from_switch=True) from _call_LD_Launch_ps_v
        call virgin_first_time(girl, _fav) from _call_virgin_ps

    if _fav == "reverse_cowgirl":
        $ rcg_speed = 0
        $ store.rcg_tip_mode = _was_tip_mode
        if not girl.has_trait("virgin"):
            call RCG_Launch(girl, from_switch=True) from _call_RCG_Launch_ps
        if _was_tip_mode:
            call RCG_TipControlMenu(girl) from _call_RCG_TCM_ps
        else:
            call RCG_ControlMenu(girl) from _call_RCG_CM_ps
    elif _fav == "cowgirl":
        $ cowgirl_speed = 0
        $ store.cowgirl_tip_mode = _was_tip_mode
        if not girl.has_trait("virgin"):
            call COWGIRL_Launch(girl, from_switch=True) from _call_CG_Launch_ps
        if _was_tip_mode:
            call COWGIRL_TipControlMenu(girl) from _call_CG_TCM_ps
        else:
            call COWGIRL_ControlMenu(girl) from _call_CG_CM_ps
    elif _fav == "doggy":
        $ doggy_speed = 0
        $ store.doggy_tip_mode = _was_tip_mode
        if not girl.has_trait("virgin"):
            call DG_Launch(girl, from_switch=True) from _call_DG_Launch_ps
        if _was_tip_mode:
            call DG_TipControlMenu(girl) from _call_DG_TCM_ps
        else:
            call DG_ControlMenu(girl) from _call_DG_CM_ps
    elif _fav == "laying_down":
        $ laying_speed = 0
        if not girl.has_trait("virgin"):
            call LD_Launch(girl, from_switch=True) from _call_LD_Launch_ps
        if _was_tip_mode:
            call LD_TipControlMenu(girl) from _call_LD_TCM_ps
        else:
            call LD_ControlMenu(girl) from _call_LD_CM_ps

    # the new position's menu ran nested inside the old one's tick: it returned (his cum, an end...), unwind to start_scene
    $ print("[SCENE_FLOW] her position switch: %s -> %s, the new position's menu returned (unwinding to start_scene) | %s" % (scene_type, _fav, scene_flow_state()))
    $ store._sub_event_position_switched = True
    return

# ============================================================
# POSITION CHANGE
# ============================================================
label SubEvent_PositionChange(girl, scene_type):
    $ store._sub_event_position_fired = True
    $ _fav = getattr(girl, "FavoriteAct", None)

    if _fav == "cowgirl":
        $ _line = scene_pick_line("pos_cowgirl", girl=girl)
        $ Say_Line(girl, _line)
    elif _fav == "reverse_cowgirl":
        $ _line = scene_pick_line("pos_cowgirl", girl=girl)
        $ Say_Line(girl, _line)
    elif _fav == "doggy":
        $ _line = scene_pick_line("pos_doggy", girl=girl)
        if _line:
            $ Say_Line(girl, _line)
        else:
            python:
                _doggy_req = renpy.random.choice([
                    _("Turn me around... I want it from behind."),
                    _("Can we switch? I want you behind me..."),
                    _("Put me on all fours... please."),
                ])
                Say_Line(girl, _doggy_req)
    elif _fav == "laying_down":
        python:
            _ld_req = renpy.random.choice([
                _("Lay me down... I want to feel you on top of me."),
                _("Can we switch? I want you on top..."),
                _("Push me down... I like it that way."),
            ])
            Say_Line(girl, _ld_req)

    # Narration hint about her preference
    python:
        _pos_req_count = getattr(girl, "_pos_change_requests", 0)
        girl._pos_change_requests = _pos_req_count + 1

    if _pos_req_count == 0:
        if _fav == "cowgirl":
            "She seems eager to be on top. Maybe she prefers being in control?"
        elif _fav == "reverse_cowgirl":
            "She seems eager to be on top. Maybe she prefers being in control?"
        elif _fav == "doggy":
            "She seems eager to get on all fours. Maybe she likes it from behind?"
        elif _fav == "laying_down":
            "She seems eager to lay back and let you take over. Maybe she likes being pinned down?"
    elif _pos_req_count == 1:
        if _fav == "cowgirl":
            "She's asked to ride you before... this might be her favorite position."
        elif _fav == "reverse_cowgirl":
            "She's asked to ride you before... this might be her favorite position."
        elif _fav == "doggy":
            "She's asked to be taken from behind before... this might be her favorite position."
        elif _fav == "laying_down":
            "She's asked to lay down before... this might be her favorite position."
    else:
        if _fav == "cowgirl":
            "She always wants to ride you. Cowgirl is definitely her favorite."
        elif _fav == "reverse_cowgirl":
            "She always wants to ride you. Cowgirl is definitely her favorite."
        elif _fav == "doggy":
            "She always wants it from behind. Doggy is definitely her favorite."
        elif _fav == "laying_down":
            "She always wants to lay back. Laying down is definitely her favorite."
        $ girl.discover("discovered_fav_act")

    menu:
        "Sure, let's switch":
            if store._condom_broken_hidden:
                call CondomBreakDiscovery(girl, scene_type) from _call_CondomBreakDisc_posswitch
            call _se_execute_pos_switch(girl, scene_type) from _call_ps_accept

        "No, keep going":
            call _femdom_refused_react(girl, "position", scene_type) from _call_fdr_position
            if not store._femdom_refused:
                $ _line = scene_pick_line("pos_denied", girl=girl)
                $ Say_Line(girl, _line)
                $ Change_Status(girl, "Obed", 10)

        "Charge her $[_se_charge_now]" if _se_can_charge(girl) and sugar_charge_quote(girl, ("anal" if _tease_is_anal_scene(scene_type) else "sex")):
            $ Say_Player(_tl(_("You want to switch? Pay me $%d.")) % store._se_charge_now)
            $ set_scene_expression(girl, "surprised")
            python:
                _charge_ok = sugar_charge_accepts(girl)   # a sugar girl pays almost always (sugar_mommy.rpy)
            if _charge_ok:
                $ sugar_charge_paid(girl, "switch")
                $ set_scene_expression(girl, "sad")
                $ Say_Line(girl, renpy.random.choice([_("...Fine. Here. Now switch."), _("You're unbelievable... take the money."), _("Ugh... here. Now do what I asked.")]))
                $ Change_Status(girl, "Obed", 5)

                if store._condom_broken_hidden:
                    call CondomBreakDiscovery(girl, scene_type) from _call_CondomBreakDisc_charge
                call _se_execute_pos_switch(girl, scene_type) from _call_ps_charge
            else:
                python:
                    _refuse_roll = renpy.random.random()
                if _refuse_roll < 0.3:
                    $ set_scene_expression(girl, "angry")
                    $ Say_Line(girl, renpy.random.choice([_("Pay YOU to switch? That's disgusting. We're done."), _("You want me to PAY for a position change?! I'm out.")]))
                    $ Change_Status(girl, "Love", -10)
                    $ store._sst_result = "abort"
                    $ store._sst_abort_reason = "hate_cum"
                else:
                    $ set_scene_expression(girl, "angry")
                    $ Say_Line(girl, renpy.random.choice([_("I'm not paying you for that. Just keep going."), _("No. Forget I asked. Keep going like normal.")]))
                    $ Change_Status(girl, "Obed", 3)
    return

# ============================================================
# PACE REQUEST
# ============================================================
label SubEvent_PaceRequest(girl, scene_type):
    python:
        _wants_faster = girl.has_trait("hardcore_sex")
        _wants_slower = girl.has_trait("cute_sex")

    if _wants_faster:
        $ _line = scene_pick_line("pace_faster", scene=scene_type, girl=girl)
        $ Say_Line(girl, _line)
        $ girl.discover("discovered_trait_hardcore_sex")
    elif _wants_slower:
        $ _line = scene_pick_line("pace_slower", scene=scene_type, girl=girl)
        $ Say_Line(girl, _line)
        $ girl.discover("discovered_trait_cute_sex")

    $ _obey_text = _("Agree with her")
    $ _ignore_text = _("Ignore her")
    menu:
        "[_obey_text]":
            if _wants_faster:
                $ _se_adjust_pace(scene_type, 1)
            elif _wants_slower:
                $ _se_adjust_pace(scene_type, -1)
            call _cum_dispatch_apply_speed(girl, scene_type) from _call_cas_pace_obey

            if _wants_faster:
                $ set_scene_expression(girl, renpy.random.choice(["ahegao", "ahegao_2"]), blush="2")
            $ _line = scene_pick_line("pace_obeyed", scene=scene_type, girl=girl)
            $ Say_Line(girl, _line)
            $ Change_Status(girl, "Love", renpy.random.randint(1, 3))

        "[_ignore_text]":
            python:
                _ignored = getattr(girl, "_ignored_pace_requests", 0)
                girl._ignored_pace_requests = _ignored + 1
                # Permanent counter for corruption
                girl.CorruptionPaceIgnoredTotal = getattr(girl, "CorruptionPaceIgnoredTotal", 0) + 1
                girl.check_corruption("pace")

            call _femdom_refused_react(girl, "pace", scene_type) from _call_fdr_pace
            if store._femdom_refused:
                pass
            elif girl._ignored_pace_requests >= 2:
                $ _line = scene_pick_line("pace_ignored_2", girl=girl)
                $ Say_Line(girl, _line)
                $ Change_Status(girl, "Obed", renpy.random.randint(1, 2))
            else:
                $ _line = scene_pick_line("pace_ignored_1", girl=girl)
                $ Say_Line(girl, _line)
                $ Change_Status(girl, "Obed", renpy.random.randint(1, 2))

        "Charge her $[_se_charge_now]" if _se_can_charge(girl) and sugar_charge_quote(girl, ("anal" if _tease_is_anal_scene(scene_type) else "sex")):
            $ Say_Player(_tl(_("You want that? Pay me $%d.")) % store._se_charge_now)
            $ set_scene_expression(girl, "surprised")
            python:
                _charge_ok = sugar_charge_accepts(girl)   # a sugar girl pays almost always (sugar_mommy.rpy)
            if _charge_ok:
                $ sugar_charge_paid(girl, "pace")
                $ set_scene_expression(girl, "sad")
                $ Say_Line(girl, renpy.random.choice([_("...Fine. Here. Now do it."), _("You're charging ME? ...Whatever. Take it."), _("Ugh... here's your money. Happy?")]))
                if _wants_faster:
                    $ _se_adjust_pace(scene_type, 1)
                elif _wants_slower:
                    $ _se_adjust_pace(scene_type, -1)
                call _cum_dispatch_apply_speed(girl, scene_type) from _call_cas_pace_charge
                $ Change_Status(girl, "Obed", 5)
            else:
                python:
                    _refuse_roll = renpy.random.random()
                if _refuse_roll < 0.3:
                    $ set_scene_expression(girl, "angry")
                    $ Say_Line(girl, renpy.random.choice([_("You're charging me?! Are you serious?! We're done!"), _("Pay YOU? For something I WANT? That's it. I'm done.")]))
                    $ Change_Status(girl, "Love", -10)
                    $ store._sst_result = "abort"
                    $ store._sst_abort_reason = "hate_cum"
                else:
                    $ set_scene_expression(girl, "angry")
                    $ Say_Line(girl, renpy.random.choice([_("No way. I'm not paying you for that."), _("You wish. Keep going like normal."), _("Pay you? Please. Just keep doing what you're doing.")]))
                    $ Change_Status(girl, "Obed", 3)
    return

# ============================================================
# RECORDING REQUEST (camera_lover asks to be recorded)
# ============================================================
label SubEvent_RecordingRequest(girl, scene_type):
    $ store._sub_event_recording_fired = True
    # camera_lover only (_se_can_recording_request): asking to be filmed reveals it, accepted or not
    $ girl.discover("discovered_trait_camera_lover") if girl.has_trait("camera_lover") else None
    $ _line = scene_pick_line("recording_request", scene=scene_type, girl=girl)
    $ Say_Line(girl, _line)

    if store._fn_girl is not None:
        menu:
            "Set up the tripod":
                call _fn_tripod_start_recording(girl, scene_type) from _call_fn_tripod_start_se
                if store._fn_tripod_result == "started":
                    $ _line = scene_pick_line("recording_request_accepted", scene=scene_type, girl=girl)
                    $ Say_Line(girl, _line)
                    $ Change_Status(girl, "Love", 10)
                    $ Change_Status(girl, "Inbt", 15)
                    $ girl.discover("discovered_trait_camera_lover")
            "Not now":
                call _femdom_refused_react(girl, "recording", scene_type) from _call_fdr_rec_tripod
                if not store._femdom_refused:
                    $ _line = scene_pick_line("recording_request_denied", scene=scene_type, girl=girl)
                    $ Say_Line(girl, _line)
        return

    menu:
        "Start recording":
            python:
                store._recording_active = True
                store._recording_girl = girl
                store._recording_seconds = 0.0
                store._player_hand_disabled = renpy.random.choice(["left", "right"])
                _pen = scene_type_is_penetration(scene_type)   # was a hand-written tuple without full nelson
                vid = {
                    "girl_gid": girl.gid,
                    "type": scene_type,
                    "location": CurrentLocation,
                    "committed": girl.has_npc_partner(),
                    "consensual": True,
                    "hd": Player.has_item("tekmix_camera"),
                    "snapshot": _make_vid_snapshot(girl),
                }
                if _pen:
                    vid["condom"] = bool(store.condom_active)
                _tag_coercion_on_vid(vid)
                store.Player.recorded_videos.append(vid)
                renpy.show_screen("recording_overlay")
            $ _line = scene_pick_line("recording_request_accepted", scene=scene_type, girl=girl)
            $ Say_Line(girl, _line)
            $ Change_Status(girl, "Love", 10)
            $ Change_Status(girl, "Inbt", 15)
            $ girl.discover("discovered_trait_camera_lover")

        "Not now":
            call _femdom_refused_react(girl, "recording", scene_type) from _call_fdr_rec
            if not store._femdom_refused:
                $ _line = scene_pick_line("recording_request_denied", scene=scene_type, girl=girl)
                $ Say_Line(girl, _line)
    return

# ============================================================
# CUM WARNING (hate_cum girl warns player)
# ============================================================
label sub_cum_warning(girl):
    $ store._cum_warning_done = True
    $ set_scene_expression(girl, "worried")
    # Anal-specific warnings take priority when in anal (every position's anal flag: doggy, full nelson, laying down)
    if any(getattr(store, _af, False) for _af in _ANAL_FLAGS.values()):
        if girl.has_trait("anal_hater"):
            $ Say_Line(girl, _("Do NOT cum in my ass! I mean it! Pull out when you're close!"))
            $ Say_Line(girl, _("My ass has been through enough already!"))
            $ girl.discover("discovered_trait_hate_cum") if girl.has_trait("hate_cum") else None
        elif girl.has_trait("cute_sex"):
            $ Say_Line(girl, _("P-please... not in my butt... please pull out before you finish..."))
            $ Say_Line(girl, _("I can't handle that back there... promise me..."))
            $ girl.discover("discovered_trait_hate_cum") if girl.has_trait("hate_cum") else None
        elif trait_is_discovering(girl, "anal_lover"):
            # still discovering anal: curious about it, not ordering him around
            $ Say_Line(girl, _("I usually hate it... but back there, I think I want to feel it."))
            $ Say_Line(girl, _("Just... don't pull out. I'm curious."))
        elif girl.has_trait("anal_lover"):
            $ Say_Line(girl, _("When you're ready... I want to feel it deep in my ass."))
            $ Say_Line(girl, _("Don't you dare pull out."))
        elif girl.has_trait("hardcore_sex"):
            $ Say_Line(girl, _("If you're going to cum, you better not waste it outside."))
            $ Say_Line(girl, _("My ass can take it. Don't be a coward."))
        else:
            $ Say_Line(girl, _("When you're close... pull out of my ass first."))
            $ Say_Line(girl, _("I don't want your cum in there. Anywhere else."))
            $ girl.discover("discovered_trait_hate_cum") if girl.has_trait("hate_cum") else None
        $ set_scene_expression(girl, "normal")
        return
    # every branch below warns him off: the trait talking
    $ girl.discover("discovered_trait_hate_cum") if girl.has_trait("hate_cum") else None
    if girl.has_trait("hardcore_sex"):
        $ Say_Line(girl, _("I swear, if you cum on me, I'll break something."))
        $ Say_Line(girl, _("Keep it away from me. I mean it."))
    elif girl.has_trait("cute_sex"):
        $ Say_Line(girl, _("P-please... when you're about to finish... don't... not on me..."))
        $ Say_Line(girl, _("I really can't handle that... please promise me..."))
    elif girl.has_trait("camera_hater"):
        $ Say_Line(girl, _("I already hate that you could be recording this..."))
        $ Say_Line(girl, _("If you finish on me on top of everything else, I swear..."))
        $ Say_Line(girl, _("Just... keep it away. I'm stressed enough."))
    elif girl.has_trait("loyal") and girl.has_npc_partner():
        $ Say_Line(girl, _("I shouldn't even be doing this... and if you finish on me..."))
        $ Say_Line(girl, _("I'll never be able to look my [girl.partner_label()] in the eye again."))
        $ Say_Line(girl, _("Please. Just... don't make this worse than it already is."))
    elif girl.has_trait("public_fetish"):
        $ Say_Line(girl, _("Look, I'm down for a lot of things, but that? No."))
        $ Say_Line(girl, _("Keep it off me. Everything else is fair game though~"))
    elif girl.has_trait("cheater"):
        $ Say_Line(girl, _("Whatever, just don't cum on me."))
        $ Say_Line(girl, _("I don't care about the rest, just not that. Gross."))
    else:
        $ Say_Line(girl, _("Hey. When you're close... aim away from me."))
        $ Say_Line(girl, _("I mean it. I hate that stuff. Keep it off me."))
    $ set_scene_expression(girl, "normal")
    return

# ============================================================
# VIRGIN NERVOUSNESS (virgin girl panics mid-scene)
# ============================================================
label sub_virgin_nervous(girl):
    $ store._virgin_nervous_done = True
    # virgin only: her nerves say it out loud (discover syncs the chip + the Virginity row)
    $ girl.discover("discovered_trait_virgin") if girl.has_trait("virgin") else None
    $ set_scene_expression(girl, "worried")
    if girl.has_trait("cute_sex"):
        $ Say_Line(girl, _("W-wait... I'm sorry... I'm just really nervous..."))
        $ Say_Line(girl, _("It's my first time doing this... is it okay if we go slow?"))
        $ Say_Line(girl, _("I trust you... just... be patient with me..."))
    elif girl.has_trait("hardcore_sex"):
        $ Say_Line(girl, _("I've never done this before. Don't you dare go easy on me though."))
        $ Say_Line(girl, _("...but maybe warn me before you do anything new."))
    elif girl.has_trait("camera_hater") and not store._recording_active:
        $ Say_Line(girl, _("This is my first time... you better not be recording this."))
        $ Say_Line(girl, _("I'm serious. If I find out there's a camera anywhere..."))
        $ Say_Line(girl, _("Just... be gentle with me, okay? I'm nervous enough."))
    elif girl.has_trait("loyal") and girl.has_npc_partner():
        $ Say_Line(girl, _("I've never done this before... and I have a [girl.partner_label()]..."))
        $ Say_Line(girl, _("What am I doing? This is so wrong..."))
        $ Say_Line(girl, _("...but I don't want to stop. Just... be careful with me."))
    elif girl.has_trait("public_fetish"):
        $ Say_Line(girl, _("My first time... and it's somewhere people could see~"))
        $ Say_Line(girl, _("That actually makes it kind of exciting..."))
        $ Say_Line(girl, _("But still... go slow? I've never actually done this."))
    elif girl.has_trait("cheater"):
        $ Say_Line(girl, _("Yeah, it's my first time. Don't make it weird."))
        $ Say_Line(girl, _("Just do your thing. I'll figure it out."))
    elif girl.has_trait("cum_slut"):
        $ Say_Line(girl, _("I've thought about this so many times... and now it's happening..."))
        $ Say_Line(girl, _("I'm nervous but honestly? I'm more excited than scared."))
        $ Say_Line(girl, _("Don't hold back too much... I want the full experience~"))
    elif girl.has_trait("hate_cum"):
        $ Say_Line(girl, _("It's my first time so... please be careful."))
        $ Say_Line(girl, _("And when you're done... don't you dare finish on me."))
        $ Say_Line(girl, _("I'm already terrified enough without worrying about that."))
    else:
        $ Say_Line(girl, _("Hey... can we slow down for a second?"))
        $ Say_Line(girl, _("I've never done this before and my heart is racing..."))
        $ Say_Line(girl, _("I'm okay. I want this. I just... need a moment."))
    $ set_scene_expression(girl, "normal")
    return

# ============================================================
# PUBLIC PANIC (public_shy girl panics about being seen)
# ============================================================
label sub_public_panic(girl):
    $ store._public_panic_done = True
    $ unlock_achievement("stage_fright")
    $ set_scene_expression(girl, "scared")
    $ Say_Line(girl, _("Wait... did you hear that?!"))
    "..."
    $ Say_Line(girl, _("I thought someone was coming..."))
    if girl.has_trait("cute_sex"):
        $ Say_Line(girl, _("Oh god, my heart almost stopped... what if someone sees us...?"))
        $ Say_Line(girl, _("I can't do this in the open like this... I'm so scared..."))
        $ girl.discover("discovered_trait_public_shy") if girl.has_trait("public_shy") else None
    elif girl.has_trait("hardcore_sex"):
        $ Say_Line(girl, _("False alarm. But seriously, if someone catches us, I'm blaming you."))
        $ Say_Line(girl, _("...let's hurry up before someone actually shows up."))
    elif girl.has_trait("camera_hater"):
        $ Say_Line(girl, _("What if someone has their phone out?! What if they recorded us?!"))
        $ Say_Line(girl, _("I can't breathe... this is a nightmare..."))
        $ Say_Line(girl, _("We need to stop... or at least move somewhere hidden!"))
        $ girl.discover("discovered_trait_public_shy") if girl.has_trait("public_shy") else None
    elif girl.has_trait("loyal") and girl.has_npc_partner():
        $ Say_Line(girl, _("If someone sees us... and word gets back to my [girl.partner_label()]..."))
        $ Say_Line(girl, _("Oh god, I'm going to be sick. This was such a bad idea."))
        $ Say_Line(girl, _("Why did I agree to this?! We need to hurry up and finish!"))
        $ girl.discover("discovered_trait_public_shy") if girl.has_trait("public_shy") else None
    elif girl.has_trait("cheater"):
        $ Say_Line(girl, _("Eh, false alarm. Who cares anyway?"))
        $ Say_Line(girl, _("Even if someone sees us, so what? Not like it matters."))
    elif girl.has_trait("cum_slut"):
        $ Say_Line(girl, _("That scared me for a second... but honestly?"))
        $ Say_Line(girl, _("My heart is pounding and it's making everything feel more intense~"))
        $ Say_Line(girl, _("Let's keep going... I don't want to stop now."))
    elif girl.has_trait("hate_cum"):
        $ Say_Line(girl, _("We almost got caught! And I swear if you panic and finish on me..."))
        $ Say_Line(girl, _("Don't even think about it. Control yourself."))
        $ Say_Line(girl, _("This is stressful enough without worrying about that too."))
        $ girl.discover("discovered_trait_public_shy") if girl.has_trait("public_shy") else None
    else:
        $ Say_Line(girl, _("That was close... we need to be more careful."))
        $ Say_Line(girl, _("If anyone sees us out here... I'd die of embarrassment."))
        $ girl.discover("discovered_trait_public_shy") if girl.has_trait("public_shy") else None
    $ set_scene_expression(girl, "normal")
    return

# ============================================================
# ANAL REQUEST (anal_lover asks to switch to anal)
# ============================================================
label SubEvent_AnalRequest(girl, scene_type):
    $ store._sub_event_anal_request_fired = True

    # NPC watching: girl asks NPC for anal permission
    if store._ntr_partner_watching and store._ntr_watching_npc:
        call _ntr_girl_ask_npc(girl, store._ntr_watching_npc, "anal") from _call_ntr_ask_npc_anal
        if store._ntr_npc_authorized:
            menu:
                "Switch to anal":
                    $ set_scene_expression(girl, "ahegao", blush="3")
                    $ _se_switch_to_anal(girl, scene_type)
                    $ girl.discover("discovered_trait_anal_lover") if girl.has_trait("anal_lover") else None   # the ask also fires from _anal_preference alone: no false banner
                    $ Change_Status(girl, "Love", 5)
                    $ Change_Status(girl, "Inbt", 5)
                    call _cum_dispatch_hole_transition(girl, scene_type, True) from _call_ht_anal_ntr_auth
                    call _cum_dispatch_apply_speed(girl, scene_type) from _call_cas_anal_ntr_auth
                    call _ntr_authorized_done(girl, store._ntr_watching_npc, "anal") from _call_ntr_auth_done_an
                "Stay in her pussy":
                    $ set_scene_expression(girl, "sad")
                    $ Say_Line(girl, _format_npc_line(store._ntr_watching_npc, renpy.random.choice([_("But... %(pp)s said it was okay..."), _("Why not? %(Pp)s already agreed...")])))
        else:
            menu:
                "Switch to anal anyway":
                    $ set_scene_expression(girl, "pleasure_intense", blush="2")
                    $ _se_switch_to_anal(girl, scene_type)
                    $ girl.discover("discovered_trait_anal_lover") if girl.has_trait("anal_lover") else None   # the ask also fires from _anal_preference alone: no false banner
                    call _cum_dispatch_hole_transition(girl, scene_type, True) from _call_ht_anal_ntr_defy
                    call _cum_dispatch_apply_speed(girl, scene_type) from _call_cas_anal_ntr_defy
                    call _ntr_agreement_broken(girl, store._ntr_watching_npc, "anal") from _call_ntr_broken_an
                "Respect [_ntr_npc_poss] decision":
                    call _ntr_boundary_respected(girl, store._ntr_watching_npc) from _call_ntr_respected_an
        return

    $ set_scene_expression(girl, "lusty")
    $ _line = scene_pick_line("anal_request", scene=scene_type, girl=girl)
    $ Say_Line(girl, _line)

    menu:
        "Switch to anal":
            $ _se_switch_to_anal(girl, scene_type)
            $ _line = scene_pick_line("anal_request_accepted", scene=scene_type, girl=girl)
            $ Say_Line(girl, _line)
            $ girl.discover("discovered_trait_anal_lover") if girl.has_trait("anal_lover") else None   # the ask also fires from _anal_preference alone: no false banner
            $ Change_Status(girl, "Love", 5)
            $ Change_Status(girl, "Inbt", 5)
            call _cum_dispatch_hole_transition(girl, scene_type, True) from _call_ht_anal_accept
            call _cum_dispatch_apply_speed(girl, scene_type) from _call_cas_anal_accept

        "Stay in her pussy":
            call _femdom_refused_react(girl, "anal", scene_type) from _call_fdr_anal
            if not store._femdom_refused:
                $ set_scene_expression(girl, "sad")
                $ _line = scene_pick_line("anal_request_declined", scene=scene_type, girl=girl)
                $ Say_Line(girl, _line)
                $ set_scene_expression(girl, "normal")

        "Charge her $[_se_charge_now]" if _se_can_charge(girl) and sugar_charge_quote(girl, ("anal" if _tease_is_anal_scene(scene_type) else "sex")):
            $ Say_Player(_tl(_("You want it in the ass? Pay me $%d.")) % store._se_charge_now)
            $ set_scene_expression(girl, "surprised")
            python:
                _charge_ok = sugar_charge_accepts(girl)   # a sugar girl pays almost always (sugar_mommy.rpy)
            if _charge_ok:
                $ sugar_charge_paid(girl, "anal")
                $ set_scene_expression(girl, "sad")
                $ Say_Line(girl, renpy.random.choice([_("...Fine. Take the money. Now put it in my ass."), _("You're really making me pay for this...? Ugh. Here."), _("I can't believe I'm paying for anal... take it.")]))
                $ _se_switch_to_anal(girl, scene_type)
                $ girl.discover("discovered_trait_anal_lover") if girl.has_trait("anal_lover") else None   # the ask also fires from _anal_preference alone: no false banner
                $ Change_Status(girl, "Love", 5)
                $ Change_Status(girl, "Obed", 5)
                call _cum_dispatch_hole_transition(girl, scene_type, True) from _call_ht_anal_charge
                call _cum_dispatch_apply_speed(girl, scene_type) from _call_cas_anal_charge
            else:
                python:
                    _refuse_roll = renpy.random.random()
                if _refuse_roll < 0.3:
                    $ set_scene_expression(girl, "angry")
                    $ Say_Line(girl, renpy.random.choice([_("Pay YOU to fuck MY ass? You're insane. We're done."), _("I'm not paying for you to use me. Get off.")]))
                    $ Change_Status(girl, "Love", -10)
                    $ store._sst_result = "abort"
                    $ store._sst_abort_reason = "hate_cum"
                else:
                    $ set_scene_expression(girl, "angry")
                    $ Say_Line(girl, renpy.random.choice([_("No way I'm paying for that. Forget I asked."), _("You're disgusting. Just keep going like normal.")]))
                    $ Change_Status(girl, "Obed", 3)
    return

# ============================================================
# ATM INITIATIVE (girl asks player to cum in her mouth from anal)
# ============================================================
label SubEvent_ATMInitiative(girl, scene_type):
    $ store._sub_event_atm_initiative_fired = True
    $ debug_log("[DEBUG] SubEvent_ATMInitiative: fired for %s" % girl.gid)

    python:
        _atm_init_line = renpy.random.choice([
            _("When you're ready to cum... put it in my mouth. I want to taste where it's been."),
            _("Don't cum in my ass... I want it in my mouth. Straight from back there. Please."),
            _("You know what I want when you finish... give it to me ass to mouth. I need it."),
        ])
    $ Say_Line(girl, _atm_init_line)
    python:
        # her unprompted ask ("I want to taste where it's been") names both tastes;
        # the event's gate needs hardcore too, but no line here voices roughness
        if girl.has_trait("cum_slut"):
            girl.discover("discovered_trait_cum_slut")
        if girl.has_trait("anal_lover"):
            girl.discover("discovered_trait_anal_lover")

    menu:
        "Do it":
            python:
                _accept_line = renpy.random.choice([
                    _("Yes... give me every drop. Straight from my ass."),
                    _("Mmm... I knew you'd say yes. I'll be ready."),
                ])
                Say_Line(girl, _accept_line)
                store._atm_cum_in_mouth = True
                store._atm_source_gid = girl.gid
                store._atm_girl_initiated = True
                # A PROMISE, not the act: nothing is counted here. atm_register() (Cum.rpy) counts it when he really
                # asks for her mouth at the cum menu. Counting here gave +2 for one ATM (promise + ask), +1 when he
                # ended up cumming somewhere else, and made her first ATM of the session play the "Again?" lines.
                print("[ATM] %s initiative accepted: promise only, counted at the cum menu" % girl.gid)
                debug_log("[DEBUG] ATM initiative accepted, _atm_cum_in_mouth=True")
            $ Change_Status(girl, "Love", 5)
            $ Change_Status(girl, "Inbt", 10)

        "No":
            call _femdom_refused_react(girl, "atm", scene_type) from _call_fdr_atm
            if not store._femdom_refused:
                python:
                    _decline_line = renpy.random.choice([
                        _("Really? ...Fine. But the offer stands."),
                        _("Your loss... I was looking forward to it."),
                    ])
                    Say_Line(girl, _decline_line)
            $ debug_log("[DEBUG] ATM initiative declined")
    return

# ============================================================
# NTR BOUNDARY: GIRL REQUESTS RAW (despite level 2)
# ============================================================
label SubEvent_NTRRequestRaw(girl, scene_type):
    $ store._sub_event_ntr_raw_fired = True
    $ store._sub_event_condom_fired = True
    $ print("[SUBEVENT] NTR request raw: %s scene=%s" % (girl.gid, scene_type))

    $ set_scene_expression(girl, "lusty")
    $ _ntr_say_boundary_line(girl, _NTR_GIRL_REQUEST_RAW)

    menu:
        "Take the condom off":
            $ _on_condom_removed(girl, skip_hide=_cum_skip_hide(scene_type))
            $ apply_cum_bonuses(girl, "condom_removed_allowed")
            $ store._creampie_consent = "allowed"
            $ Change_Status(girl, "Obed", 5)
            $ Change_Status(girl, "Inbt", 10)
            call _sex_scene_condom_rip_visual(girl, scene_type) from _call_crv_ntr_raw

        "Keep the condom on":
            $ set_scene_expression(girl, "sad")
            python:
                _ntr_raw_deny = renpy.random.choice([
                    _("Fine... I just wanted to feel you without it..."),
                    _("Whatever... your call."),
                ])
            $ Say_Line(girl, _ntr_raw_deny)
    return

# ============================================================
# NTR BOUNDARY: GIRL REQUESTS CREAMPIE (despite level 3)
# ============================================================
label SubEvent_NTRRequestCreampie(girl, scene_type):
    $ store._sub_event_ntr_creampie_fired = True
    $ store._sub_event_creampie_fired = True
    $ print("[SUBEVENT] NTR request creampie: %s scene=%s" % (girl.gid, scene_type))

    $ set_scene_expression(girl, "lusty")
    $ _ntr_say_boundary_line(girl, _NTR_GIRL_REQUEST_CREAMPIE)

    menu:
        "Promise to cum inside":
            $ store._girl_requested_creampie = True
            $ store._creampie_consent = "allowed"
            $ Change_Status(girl, "Love", 10)
            $ Change_Status(girl, "Inbt", 15)
            python:
                _ntr_cream_yes = renpy.random.choice([
                    _("Yes... fill me up when you're ready. Our little secret."),
                    _("I knew you would... I can't wait to feel it."),
                ])
            $ Say_Line(girl, _ntr_cream_yes)

        "Refuse":
            $ set_scene_expression(girl, "sad")
            python:
                _ntr_cream_no = renpy.random.choice([
                    _("Fine... just pull out when you're done..."),
                    _("I really wanted you to... but okay..."),
                ])
            $ Say_Line(girl, _ntr_cream_no)
    return

# ============================================================
# SPANK HER
# ============================================================
init python:
    # ── Her spank record (girl.SpankLog) ──
    # Every ASS spank she took: SpankHer (light and heavy), the Truth or Dare spank dares, the pillow refusal, his lewd
    # flirt slap. {"taken": n, "by_player": n, "enjoyed": n}, "enjoyed" = her reaction at that moment was pleasure;
    # "given" / "given_enjoyed" = the ones SHE gave (the Truth or Dare girl-on-girl dare). Read by the NHIE
    # liked_spanking. None = a save older than the record (spank_log_ensure starts it on her next spank).
    # A face slap is no spank: SpankHer in these scenes hits her FACE, never recorded (nor in the heavy spank
    # corruption counters, whose narration says "After all those spanks", nor in the next-morning spanked photo)
    SPANK_FACE_SCENES = ("cowgirl",)
    # SpankHer's reaction order (first match speaks): these beg for more at every level...
    SPANK_LOVER_TRAITS = ("cum_slut", "hardcore_sex")
    # ...these protest at every level...
    SPANK_HATER_TRAITS = ("cute_sex", "virgin")
    # ...any other girl moans at a light / medium spank and cries at a heavy one (SpankHer tier 3: this level and up)
    SPANK_HEAVY_LEVEL = 8

    # Per-girl RCG slap transforms (full-screen images whose hand is at the landing spot: xoffset animation, not xpos).
    # Values are transform names resolved at runtime (the transforms live in the character's file).
    _RCG_SLAP_TRANSFORMS = {
        "shion": {"right": "srcg_slap_right_in", "left": "srcg_slap_left_in"},
    }
    # Per-girl doggy slap with its own layer set: (image, transform name), ONE hand whatever the side (a side view)
    _DOGGY_SLAP_OVERRIDES = {
        "shion": ("shion sdg_slap", "sdg_slap_in"),
    }
    # His lewd flirt slap on her ass (Flirt_Lewd_SlapAss): the answers that liked it ("Bold move.", "You really like
    # my ass, huh?", a femdom's "Not bad"). A shy or an obedient yes only lets it slide; a no hated it
    SPANK_FLIRT_ENJOYED_MODES = ("normal_yes", "enthusiastic_yes", "commanding_yes")

    def spank_enjoyed(girl, heavy=False):
        """Does she enjoy a SpankHer spank? SpankHer's own reaction for her (SPANK_LOVER / HATER_TRAITS, then the
        level). For a heavy one ask after the corruption check: it may have just turned her hardcore. heavy=False is
        also the reading of a save older than her record: her heavy spank days came after lighter spanks."""
        if any(girl.has_trait(_t) for _t in SPANK_LOVER_TRAITS):
            return True
        if any(girl.has_trait(_t) for _t in SPANK_HATER_TRAITS):
            return False
        return not heavy

    def spank_log_ensure(girl):
        """Her spank record, started on her first recorded spank. A save older than the record starts it from what
        that save knew: her heavy spank days (all his), liked per spank_enjoyed. Call it before a spank moves
        CorruptionHeavySpankDays (SpankHer does, at its top)."""
        _log = getattr(girl, "SpankLog", None)
        if _log is None:
            _days = int(getattr(girl, "CorruptionHeavySpankDays", 0) or 0)
            _log = {"taken": _days, "by_player": _days, "enjoyed": _days if (_days and spank_enjoyed(girl)) else 0}
            girl.SpankLog = _log
            print("[SPANK] %s: spank record started %s (legacy heavy spank days %d)" % (girl.gid, _log, _days))
        return _log

    def slap_crack():
        """The crack of a slap, ANY slap: ass spank, face slap, hers on him, girl on girl. Every site
        calls this instead of carrying its own copy of the file (author 2026-10-10, "deveria ser
        globalizado"): one place owns the sound, so changing the file or channel changes every slap,
        and a new slap can never ship mute again (the ToD dares and the massage did)."""
        renpy.sound.play("audio/Slap.ogg")

    def spank_note(girl, enjoyed, source, by_player=True, given=False):
        """She just took an ASS spank (a face slap never comes here): count it, who gave it, and whether she
        enjoyed it at that moment (the reaction the caller plays for her). given=True: SHE spanked someone (by_player
        means nothing then), enjoyed = her own answer liked doing it."""
        _log = dict(spank_log_ensure(girl))
        if given:
            _log["given"] = _log.get("given", 0) + 1
            if enjoyed:
                _log["given_enjoyed"] = _log.get("given_enjoyed", 0) + 1
        else:
            _log["taken"] = _log.get("taken", 0) + 1
            if by_player:
                _log["by_player"] = _log.get("by_player", 0) + 1
            if enjoyed:
                _log["enjoyed"] = _log.get("enjoyed", 0) + 1
        girl.SpankLog = _log
        print("[SPANK] %s spank noted (%s): given=%s enjoyed=%s by_player=%s -> %s" % (
            girl.gid, source, given, bool(enjoyed), by_player, _log))

label SpankHer(girl, scene_type):
    $ slap_crack()
    python:
        _is_hardcore = girl.has_trait("hardcore_sex")
        _is_cute = girl.has_trait("cute_sex")
        _is_cum_slut = girl.has_trait("cum_slut")
        _is_virgin = girl.has_trait("virgin")
        # Cowgirl = face slap, any other scene = ass spank (SPANK_FACE_SCENES). A face slap is no spank: it never
        # reaches her spank record, the heavy spank corruption counters, the next-morning spanked photo, the
        # threesome watcher's "my butt is still stinging" or her butt: it climbs its own level (SlapLevel), so her ass
        # stays unmarked (butt_blush, the cheating "marks" talk read SpankLevel)
        _is_face = scene_type in SPANK_FACE_SCENES
        _level_attr = "SlapLevel" if _is_face else "SpankLevel"
        if not _is_face:
            spank_log_ensure(girl)   # before any counter below moves: an old save's record starts from them
            store._session_spanked_girls.add(girl.gid)

        # Increment the level (cap at 10)
        _spank_level = min(10, (getattr(girl, _level_attr, 0) or 0) + 1)
        setattr(girl, _level_attr, _spank_level)
        # Flag for next-morning photo if heavy spank (7+): the photo shows her spanked ass
        if _spank_level >= 7 and not _is_face:
            girl._heavy_spank_yesterday = True
        if _spank_level >= 6:
            unlock_achievement("red_handed")
        print("[SPANK] %s: %s=%d, face=%s, cute=%s hc=%s cs=%s virgin=%s, corruption_enabled=%s" % (girl.Name, _level_attr, _spank_level, _is_face, _is_cute, _is_hardcore, _is_cum_slut, _is_virgin, getattr(store, "corruption_enabled", False)))

        # Show slap hand flying in (scene-aware); hide grab hand on that side
        _hand_disabled = getattr(store, "_player_hand_disabled", None)
        _spank_side = ("left" if _hand_disabled == "right" else "right") if _hand_disabled else renpy.random.choice(["right", "left"])
        store._slap_hide_hand = _spank_side
        if scene_type == "cowgirl":
            _spank_img = "%s cowgirl_slap_%s" % (girl.gid, _spank_side)
            _spank_tf = cowgirl_slap_right_in if _spank_side == "right" else cowgirl_slap_left_in
            # Immediately hide the grab/squeeze/arms hand on the slap side
            _cg_touch = getattr(store, "cowgirl_guy_touch", None)
            if _cg_touch == "grab_tits":
                renpy.hide("cowgirl_guy_squeeze_%s" % _spank_side)
            elif _cg_touch == "push_down":
                renpy.hide("cowgirl_guy_arms_%s" % _spank_side)
        elif scene_type in ("doggy", "anal"):
            _dg_slap = _DOGGY_SLAP_OVERRIDES.get(girl.gid)
            if _dg_slap:
                _spank_img = _dg_slap[0]
                _spank_tf = getattr(store, _dg_slap[1])
            else:
                _spank_img = "%s doggy_slap_%s" % (girl.gid, _spank_side)
                _spank_tf = dg_slap_right_in if _spank_side == "right" else dg_slap_left_in
            if store.doggy_grab:
                renpy.hide("dg_grab_%s" % _spank_side)
        elif scene_type == "laying_down":
            _spank_img = "tenny laying_slap_%s" % _spank_side
            _spank_tf = ld_slap_right_in if _spank_side == "right" else ld_slap_left_in
            if store.laying_grab:
                renpy.hide("ld_grab_%s" % _spank_side)
        else:
            _spank_img = "%s rcg_slap_%s" % (girl.gid, _spank_side)
            _rcg_slap_overrides = _RCG_SLAP_TRANSFORMS.get(girl.gid)
            if _rcg_slap_overrides:
                _spank_tf = getattr(store, _rcg_slap_overrides[_spank_side])
            else:
                _spank_tf = rcg_slap_right_in if _spank_side == "right" else rcg_slap_left_in
            # Immediately hide the grab hand on the slap side
            if store.rcg_grab:
                renpy.hide("rcg_grab_%s" % _spank_side)
            # ... or the hand holding her down lets go of her thigh for the spank (Core_RCG.rpy, her own layers)
            if getattr(store, "rcg_hold", False):
                rcg_hold_redraw(girl)

    show expression _spank_img as spank_hand at _spank_tf zorder 10090

    # Slap wave (laying_down only — show immediately with the slap sound)
    if scene_type == "laying_down":
        if _spank_side == "right":
            show expression "tenny laying_slap_wave_right" as slap_wave at ld_slap_wave_right_in zorder 9862
        else:
            show expression "tenny laying_slap_wave_left" as slap_wave at ld_slap_wave_left_in zorder 9862

    $ renpy.pause(0.08)

    # Spank screen shake
    call Punch from _call_Punch_spank

    # Blink on impact + change expression
    python:
        state = sprite_state.setdefault(girl.Id, {})
        state["eyes"] = "eyes_closed"

        # Update butt blush (3+ = level 1, 6+ = level 2): ass spanks only
        if not _is_face:
            _butt_blush = 0
            if _spank_level >= 6:
                _butt_blush = 2
            elif _spank_level >= 3:
                _butt_blush = 1
            state["butt_blush"] = _butt_blush

    call _cum_dispatch_apply_speed(girl, scene_type) from _call_spank_blink
    $ renpy.pause(0.12, hard=True)

    # Open eyes with new expression
    python:
        state = sprite_state.setdefault(girl.Id, {})
        if _is_hardcore:
            state["eyes"] = renpy.random.choice(["eyes_looking_to_player", "eyes_side", _("eyes_normal")])
            state["mouth"] = renpy.random.choice(["mouth_tongue", _("mouth_lipbite"), "mouth_smile"])
            state["brows"] = "brows_horny"
        elif _is_cute:
            if _spank_level <= 3:
                state["eyes"] = renpy.random.choice(["eyes_squint", _("eyes_looking_right"), _("eyes_closed")])
                state["mouth"] = renpy.random.choice(["mouth_surprised", "mouth_scared"])
            elif _spank_level <= 7:
                state["eyes"] = renpy.random.choice(["eyes_squint", _("eyes_looking_left"), _("eyes_looking_right"), _("eyes_closed")])
                state["mouth"] = renpy.random.choice(["mouth_scared", _("mouth_sad")])
            else:
                state["eyes"] = renpy.random.choice([_("eyes_looking_left"), _("eyes_looking_right"), _("eyes_closed")])
                state["mouth"] = "mouth_sad"
            state["brows"] = "brows_sad"
        else:
            state["eyes"] = renpy.random.choice(["eyes_looking_to_player", "eyes_squint", _("eyes_normal")])
            state["mouth"] = renpy.random.choice(["mouth_surprised", _("mouth_lipbite"), "mouth_tongue"])
            state["brows"] = renpy.random.choice([_("brows_surprised"), _("brows_horny")])

    call _cum_dispatch_apply_speed(girl, scene_type) from _call_spank_expr

    $ renpy.pause(0.20)
    hide spank_hand

    # Restore hidden grab hand
    $ store._slap_hide_hand = None
    call _cum_dispatch_apply_speed(girl, scene_type) from _call_spank_restore

    # Her spank record: a light / medium ass spank is noted here, with the reaction the tiers below play for her
    # (spank_enjoyed). A heavy one is noted inside its tier, after the corruption check that may turn her hardcore
    if not _is_face and _spank_level < SPANK_HEAVY_LEVEL:
        $ spank_note(girl, spank_enjoyed(girl), "spank_her")

    # She counts (count_slaps.rpy, the "Make her count" tease): her number replaces the reaction line of the tiers
    # below (the abort lines of a heavy spank still play)
    $ _spank_counted = count_slaps_say(girl, _is_face)

    # ── TIER 1: light (0-3) ──
    if _spank_level <= 3:
        if _is_cum_slut:
            python:
                if _is_face:
                    _spank_lines = [
                        _("Mmm! Yes! Slap my face!"),
                        _("Harder! I love it when you're rough with me!"),
                        _("Again! Slap me! Don't stop!"),
                    ]
                else:
                    _spank_lines = [
                        _("Mmm! Yes! Spank that ass!"),
                        _("Harder! I love it when you're rough!"),
                        _("Again! Don't stop!"),
                    ]
            $ _spank_counted or Say_Line(girl, _tl(renpy.random.choice(_spank_lines)))
            $ girl.discover("discovered_trait_cum_slut")
            $ Change_Status(girl, "Obed", 4)
            $ Change_Status(girl, "Inbt", 3)
            $ girl.Lust = min(100, getattr(girl, "Lust", 0) + 5)
        elif _is_hardcore:
            python:
                if _is_face:
                    _spank_lines = [
                        _("Mmm, that's it. Slap me harder."),
                        _("Is that all you got? Hit my face for real."),
                        _("Yes! Slap me again. Don't be shy."),
                    ]
                else:
                    _spank_lines = [
                        _("Mmm, that's it. Spank me harder."),
                        _("Is that all you got? Come on, hit me for real."),
                        _("Yes! Again. Don't be shy."),
                    ]
            $ _spank_counted or Say_Line(girl, _tl(renpy.random.choice(_spank_lines)))
            $ girl.discover("discovered_trait_hardcore_sex")
            $ Change_Status(girl, "Obed", 3)
            $ Change_Status(girl, "Inbt", 2)
        elif _is_cute:
            python:
                if _is_face:
                    _spank_lines = [
                        _("Ah! You slapped my face?!"),
                        _("Ouch! Why did you hit my face?!"),
                        _("Hey! Don't slap me!"),
                    ]
                else:
                    _spank_lines = [
                        _("Ah! W-what was that for?!"),
                        _("Ouch! That surprised me..."),
                        _("Hey! Be gentle with me..."),
                    ]
            $ _spank_counted or Say_Line(girl, _tl(renpy.random.choice(_spank_lines)))
            $ Change_Status(girl, "Obed", 1)
            $ Change_Status(girl, "Love", trait_love_loss(girl, -1, face=_is_face))
        elif _is_virgin:
            python:
                if _is_face:
                    _spank_lines = [
                        _("AH! You hit my FACE?!"),
                        _("Ouch! Nobody has ever slapped my face before!"),
                        _("H-hey! Don't slap me like that!"),
                    ]
                else:
                    _spank_lines = [
                        _("AH! W-why did you do that?!"),
                        _("Ouch! Nobody has ever... that hurt!"),
                        _("H-hey! Don't spank me like that!"),
                    ]
            $ _spank_counted or Say_Line(girl, _tl(renpy.random.choice(_spank_lines)))
            $ girl.discover("discovered_trait_virgin")
            $ Change_Status(girl, "Obed", 1)
        else:
            python:
                if _is_face:
                    _spank_lines = [
                        _("Mmm, slap my face like that..."),
                        _("Oh! Do that again..."),
                        _("Mmm... I kind of like when you slap me."),
                    ]
                else:
                    _spank_lines = [
                        _("Hmm, yes, spank my ass."),
                        _("Oh! Do that again..."),
                        _("Mmm... I kind of like that."),
                    ]
            $ _spank_counted or Say_Line(girl, _tl(renpy.random.choice(_spank_lines)))
            if _is_face:
                "She recoils from the slap but bites her lip."
            else:
                "She flinches from the slap but lets out a soft moan of pleasure."
            $ Change_Status(girl, "Obed", 2)

    # ── TIER 2: medium (4-7) ──
    elif _spank_level < SPANK_HEAVY_LEVEL:
        if _is_cum_slut:
            python:
                if _is_face:
                    _spank_lines = [
                        _("Yes! Harder! Make my cheek red!"),
                        _("Slap me! I love it! Don't hold back!"),
                        _("More! Slap my face! Harder!"),
                    ]
                else:
                    _spank_lines = [
                        _("Yes! Harder! Make my ass red!"),
                        _("Spank me! I love it! Don't hold back!"),
                        _("More! My ass can take it! Harder!"),
                    ]
            $ _spank_counted or Say_Line(girl, _tl(renpy.random.choice(_spank_lines)))
            $ girl.discover("discovered_trait_cum_slut")
            $ Change_Status(girl, "Obed", 6)
            $ Change_Status(girl, "Inbt", 4)
            $ girl.Lust = min(100, getattr(girl, "Lust", 0) + 8)
        elif _is_hardcore:
            python:
                if _is_face:
                    _spank_lines = [
                        _("YES! Mark my face! Slap me harder!"),
                        _("Harder! I want my cheek burning tomorrow!"),
                        _("That's more like it! Slap me! Don't stop!"),
                        _("I want bruises on my face. Hit me like you mean it."),
                    ]
                else:
                    _spank_lines = [
                        _("Harder! I want to feel it tomorrow!"),
                        _("That's more like it! Don't stop!"),
                        _("I want bruises. Hit me like you mean it."),
                    ]
                    # being marked as his is submissive, not hardcore (docs/plan_femdom.md D3): only a girl who is
                    # both says it (this branch keeps the hardcore stats; the generic branch has its own "mark me")
                    if girl.has_trait("submissive"):
                        _spank_lines.append(_("YES! Mark me as yours! Spank me harder!"))
                _spank_pick = renpy.random.choice(_spank_lines)
            $ _spank_counted or Say_Line(girl, _tl(_spank_pick))
            python:
                girl.discover("discovered_trait_hardcore_sex")
                # "Mark me as yours" is her submissive voice: only when that exact line spoke
                if _spank_pick == "YES! Mark me as yours! Spank me harder!" and girl.has_trait("submissive"):
                    girl.discover("discovered_trait_submissive")
            $ Change_Status(girl, "Obed", 5)
            $ Change_Status(girl, "Inbt", 3)
        elif _is_cute:
            python:
                _spank_lines = [
                    _("Ow! That really hurts! Please stop..."),
                    _("You're being too rough! I don't like this..."),
                    _("It's too much... please, be gentle..."),
                ]
            $ _spank_counted or Say_Line(girl, _tl(renpy.random.choice(_spank_lines)))
            "Her eyes start to water from the sting."
            $ Change_Status(girl, "Love", trait_love_loss(girl, -3, face=_is_face))
            $ Change_Status(girl, "Obed", 2)
        elif _is_virgin:
            python:
                _spank_lines = [
                    _("Stop it! That HURTS! Why are you being so rough?!"),
                    _("Please... I've never been hit like this before..."),
                    _("OW! You're scaring me... please stop..."),
                ]
            $ _spank_counted or Say_Line(girl, _tl(renpy.random.choice(_spank_lines)))
            $ girl.discover("discovered_trait_virgin")
            $ Change_Status(girl, "Love", trait_love_loss(girl, -2, face=_is_face))
            $ Change_Status(girl, "Obed", 2)
        else:
            python:
                if _is_face:
                    _spank_lines = [
                        _("Yes, slap my face! Mark me!"),
                        _("Mmm! My cheek is burning..."),
                        _("Harder... I can take it."),
                    ]
                else:
                    _spank_lines = [
                        _("Yes, mark me as yours, spank me!"),
                        _("Mmm! My ass is on fire..."),
                        _("Harder... I can take it."),
                    ]
            $ _spank_counted or Say_Line(girl, _tl(renpy.random.choice(_spank_lines)))
            if _is_face:
                "You can see her cheek turning red from your slaps."
            else:
                "You can see her ass turning red from your slaps."
            $ Change_Status(girl, "Obed", 3)
            $ Change_Status(girl, "Inbt", 2)

    # ── TIER 3: heavy (8-10) ──
    else:
        python:
            _corruption_narr = None
            # no "she is breaking" narration for a cum_slut: her branch below always begs for more, she never protests
            _corruption_on = getattr(store, "corruption_enabled", False) and not girl.has_trait("hardcore_sex") and not _is_cum_slut
            _is_cute_corr = girl.has_trait("cute_sex")
            print("[SPANK] %s TIER 3 — CorruptionHeavySpanks=%d, CorruptionHeavySpankDays=%d, corruption_enabled=%s, traits=%s" % (girl.Name, getattr(girl, "CorruptionHeavySpanks", 0), getattr(girl, "CorruptionHeavySpankDays", 0), getattr(store, "corruption_enabled", False), girl.traits))

            # a face slap is no spank (SPANK_FACE_SCENES): neither heavy spank counter moves, their narrations and
            # banners ("After all those spanks") speak of spanks
            if _is_cute_corr and not _is_face:
                girl.CorruptionHeavySpanks = getattr(girl, "CorruptionHeavySpanks", 0) + 1
                print("[CORRUPTION] %s cute_sex heavy spank #%d" % (girl.Name, girl.CorruptionHeavySpanks))
                if _corruption_on:
                    _corruption_narr = {
                        1: _("She winces, but you catch a flicker of something else in her eyes."),
                        2: _("Her cries sound different now... less fear, more excitement."),
                        3: _("She's biting her lip. The pain is turning into something else for her."),
                        4: _("She barely fights back anymore. Her body trembles, but not just from fear."),
                    }.get(girl.CorruptionHeavySpanks)
            else:
                print("[CORRUPTION] %s no cute_sex or a face slap (face=%s), CorruptionHeavySpanks skipped" % (girl.Name, _is_face))

            _cur_day = store.Day
            _last_day = getattr(girl, "_heavy_spank_last_day", -1)
            if _is_face:
                print("[CORRUPTION] %s face slap, CorruptionHeavySpankDays stays at %d" % (girl.Name, getattr(girl, "CorruptionHeavySpankDays", 0)))
            elif _last_day != _cur_day:
                girl.CorruptionHeavySpankDays = getattr(girl, "CorruptionHeavySpankDays", 0) + 1
                girl._heavy_spank_last_day = _cur_day
                print("[CORRUPTION] %s heavy spank day %d (game day %d)" % (girl.Name, girl.CorruptionHeavySpankDays, _cur_day))
                # a virgin (non-cute) takes the virgin branch below, which protests and ends the scene every time
                if _corruption_on and not _is_cute_corr and not _is_virgin:
                    _corruption_narr = {
                        1: _("You notice something... she didn't flinch as much this time."),
                        2: _("She seems to be getting used to the rough treatment."),
                        3: _("There's something different in her eyes... she's not just enduring it anymore."),
                        4: _("Her protests are getting weaker. Is she starting to enjoy this?"),
                        5: _("She barely complains now. The pain seems to excite her more than she'd admit."),
                        6: _("You can tell she's fighting it, but her body responds to the roughness."),
                        7: _("She's almost there. One more push and she won't be able to deny it."),
                    }.get(girl.CorruptionHeavySpankDays)
                    _corruption_narr = _tl(_corruption_narr) if _corruption_narr else None  # translated when picked: a "[var]" line never translates what it interpolates
            else:
                print("[CORRUPTION] %s same day=%d, CorruptionHeavySpankDays stays at %d" % (girl.Name, _cur_day, getattr(girl, "CorruptionHeavySpankDays", 0)))

            girl.check_corruption("spank")
            # The evolution above may have swapped cute_sex -> hardcore_sex (or added hardcore_sex): the reaction
            # below must match the banner she just got, not the trait she had before this spank.
            _is_hardcore = girl.has_trait("hardcore_sex")
            _is_cute = girl.has_trait("cute_sex")
            # her spank record, with the reaction the branches below play (spank_enjoyed, after the evolution)
            if not _is_face:
                spank_note(girl, spank_enjoyed(girl, heavy=True), "spank_her_heavy")

        if _corruption_narr:
            "[_corruption_narr]"

        if _is_cum_slut:
            python:
                if _is_face:
                    _spank_lines = [
                        _("FUCK! YES! SLAP MY FACE! I LOVE IT!"),
                        _("HARDER! SLAP ME UNTIL MY CHEEK IS SWOLLEN!"),
                        _("DON'T STOP SLAPPING ME! I'M SO WET FROM THIS!"),
                    ]
                else:
                    _spank_lines = [
                        _("FUCK! YES! DESTROY MY ASS! I LOVE IT!"),
                        _("HARDER! MAKE ME YOURS! SPANK ME UNTIL I CAN'T SIT!"),
                        _("DON'T STOP! I'M SO WET FROM THIS!"),
                    ]
            $ _spank_counted or Say_Line(girl, _tl(renpy.random.choice(_spank_lines)))
            $ girl.discover("discovered_trait_cum_slut")
            if _is_face:
                "She's moaning loudly, turning her face toward you for more."
            else:
                "She's moaning loudly, pushing her ass back for more."
            $ Change_Status(girl, "Obed", 10)
            $ Change_Status(girl, "Inbt", 6)
            $ girl.Lust = min(100, getattr(girl, "Lust", 0) + 12)
        elif _is_hardcore:
            python:
                _spank_lines = [
                    _("FUCK YES! MORE! I can take ANYTHING you give me!"),
                    _("Is THAT all?! HIT ME HARDER! Make me SCREAM!"),
                    _("HARDER! Break me! I want to feel this for DAYS!"),
                ]
                # begging for punishment is submissive, not hardcore (docs/plan_femdom.md D3): only a girl who is both
                if girl.has_trait("submissive"):
                    _spank_lines.append(_("YES! PUNISH ME! I love it! Don't you DARE stop!"))
                _spank_pick = renpy.random.choice(_spank_lines)
            $ _spank_counted or Say_Line(girl, _tl(_spank_pick))
            python:
                girl.discover("discovered_trait_hardcore_sex")
                # begging for punishment is her submissive voice: only when that exact line spoke
                if _spank_pick == "YES! PUNISH ME! I love it! Don't you DARE stop!" and girl.has_trait("submissive"):
                    girl.discover("discovered_trait_submissive")
            if _is_face:
                "She leans her face into your hand, begging for more."
            else:
                "She pushes her ass back into your hand, begging for more."
            $ Change_Status(girl, "Obed", 8)
            $ Change_Status(girl, "Inbt", 5)
        elif _is_cute:
            python:
                _spank_lines = [
                    _("P-please... stop... you're going to leave me bruised..."),
                    _("I can't... it hurts so much... please, no more..."),
                    _("Ouch! You're going to leave marks! Please stop!"),
                ]
            $ _spank_counted or Say_Line(girl, _tl(renpy.random.choice(_spank_lines)))
            "Her eyes are full of tears from the pain of your slaps."
            $ Change_Status(girl, "Love", trait_love_loss(girl, -8, face=_is_face))
            $ Change_Status(girl, "Obed", 3)

            # She's had enough — abort the scene
            python:
                _spank_abort_lines = [
                    _("STOP! I said STOP! I can't take any more!"),
                    _("That's it! I'm DONE! You went WAY too far!"),
                    _("No more! You're hurting me! We're finished here!"),
                ]
            $ Say_Line(girl, _tl(renpy.random.choice(_spank_abort_lines)))
            $ Change_Status(girl, "Love", trait_love_loss(girl, -20, face=_is_face))

            python:
                _in_her_room = (store.CurrentLocation == GIRL_ROOMS.get(girl.gid, ""))
            if _in_her_room:
                python:
                    _narr = _tl(renpy.random.choice([
                        _("She pushes you toward the door, tears streaming down her face."),
                        _("With trembling hands and watery eyes, she shoves you out of her room."),
                        _("She can barely look at you. Eyes red and full of tears, she points at the door."),
                    ]))
                "[_narr]"
            else:
                python:
                    _narr = _tl(renpy.random.choice([
                        _("She grabs her things and runs off, wiping tears from her eyes."),
                        _("Without another word, she turns away and leaves, sobbing quietly."),
                        _("She pulls away from you and storms off, her eyes glistening with tears."),
                    ]))
                "[_narr]"

            if _is_face:
                PlayerChar "Looks like she needs more... training. Maybe a few more slaps once she calms down will help her get used to it."
            else:
                PlayerChar "Looks like she needs more... training. Maybe more spanking once she calms down will help her get used to it."

            $ girl.set_temp_status("sad", days=1, reason="excessive_spanking")
            $ force_scene_reset(girl, angry_days=0, reason="excessive_spanking")
            jump main_loop

        elif _is_virgin:
            python:
                _spank_lines = [
                    _("STOP! PLEASE! I've never... this is too much! You're HURTING me!"),
                    _("Why are you doing this?! I can't take it! STOP!"),
                    _("PLEASE STOP! I'm begging you! It hurts so much!"),
                ]
            $ _spank_counted or Say_Line(girl, _tl(renpy.random.choice(_spank_lines)))
            if _is_face:
                "She's trembling and crying from the heavy slaps."
            else:
                "She's trembling and crying from the heavy spanking."
            $ Change_Status(girl, "Love", trait_love_loss(girl, -10, face=_is_face))
            $ Change_Status(girl, "Obed", 5)

            python:
                _spank_abort_lines = [
                    _("I can't do this anymore! Stop! PLEASE!"),
                    _("That's enough! I'm done! You're scaring me!"),
                    _("No more! I can't take any more of this!"),
                ]
            $ Say_Line(girl, _tl(renpy.random.choice(_spank_abort_lines)))
            $ Change_Status(girl, "Love", trait_love_loss(girl, -15, face=_is_face))

            python:
                _in_her_room = (store.CurrentLocation == GIRL_ROOMS.get(girl.gid, ""))
            if _in_her_room:
                "She curls up on her bed, shaking. She won't even look at you."
            else:
                "She pulls away from you and stumbles off, tears running down her face."

            $ girl.set_temp_status("sad", days=1, reason="excessive_spanking")
            $ force_scene_reset(girl, angry_days=0, reason="excessive_spanking")
            jump main_loop

        else:
            python:
                girl._heavy_spank_count = getattr(girl, "_heavy_spank_count", 0) + 1

            if girl._heavy_spank_count <= 2:
                python:
                    _spank_lines = [
                        _("Ouch! You're going to leave me purple!"),
                        _("Ow ow ow! Okay, that's really starting to hurt!"),
                    ]
                    # a face slap (cowgirl) never talks about her ass
                    if not _is_face:
                        _spank_lines.append(_("My ass... I won't be able to sit down after this!"))
                $ _spank_counted or Say_Line(girl, _tl(renpy.random.choice(_spank_lines)))
                "Her eyes start to tear up from the pain of your slaps."
                $ Change_Status(girl, "Obed", 5)
                $ Change_Status(girl, "Inbt", 3)
            else:
                python:
                    _spank_lines = [
                        _("ENOUGH! I said enough! You're going way too far!"),
                        _("STOP IT! What is wrong with you?! That HURTS!"),
                        _("I'm DONE! You crossed the line! We're finished!"),
                    ]
                $ _spank_counted or Say_Line(girl, _tl(renpy.random.choice(_spank_lines)))
                $ Change_Status(girl, "Love", trait_love_loss(girl, -12, face=_is_face))
                $ Change_Status(girl, "Obed", 5)

                python:
                    _in_her_room = (store.CurrentLocation == GIRL_ROOMS.get(girl.gid, ""))
                if _in_her_room:
                    "She shoves you away, rubbing the tears from her eyes."
                else:
                    "She pushes past you and storms off, furious and in pain."

                $ girl._heavy_spank_count = 0
                $ girl.set_temp_status("angry", days=1, reason="excessive_spanking")
                $ force_scene_reset(girl, angry_days=1, reason="excessive_spanking")
                jump main_loop

    $ _girl_lust_gain(girl, 2)
    if _should_trigger_nonscene_orgasm(girl):
        call _nonscene_orgasm(girl) from _call_nonscene_orgasm_spank
    elif girl.Lust >= 100 and not _is_face and _girl_in_sex_scene(girl):
        # Inside a scene the nonscene hook above refuses by design, so the spank that topped her off
        # never fired ANY orgasm (tester 2026-10-10: "even hardcore girls do not cum while being
        # spanked"): the scene's own climax plays, like any other tick that fills her up.
        call GirlCumming(girl, "spank", scene_type) from _call_GirlCumming_spank
    $ _watcher_scene_comment("slap" if _is_face else "spank")
    return

# ============================================================
# PILLOW REQUEST
# ============================================================
label SubEvent_PillowRequest(girl, scene_type):
    $ store._sub_event_pillow_fired = True
    $ set_scene_expression(girl, "sad")

    if getattr(store, "laying_anal", False):
        $ Say_Line(girl, _("Can you get me a pillow? This position is killing my neck..."))
    elif getattr(store, "laying_speed", 0) >= 3:
        $ Say_Line(girl, _("Wait, let me grab a pillow... you're going so hard..."))
    else:
        $ Say_Line(girl, _("Can you hand me that pillow? I want to get comfortable."))

    menu:
        "Give her the pillow":
            $ store._ld_pillow_active = True
            $ set_scene_expression(girl, "happy")
            $ Say_Line(girl, _("Thanks... much better."))
            $ Change_Status(girl, "Love", renpy.random.randint(2, 5))
            call LD_ApplySpeed(girl, laying_speed) from _call_LD_ApplySpeed_pillow_se

        "No":
            $ Say_Player(_("No, stay like that!"))
            $ Change_Status(girl, "Love", -renpy.random.randint(2, 4))
            $ Change_Status(girl, "Obed", renpy.random.randint(2, 4))

            # Visual-only spank (no SpankLevel, no butt_blush, no stat escalation)
            $ slap_crack()
            python:
                _hand_disabled = getattr(store, "_player_hand_disabled", None)
                _spank_side = ("left" if _hand_disabled == "right" else "right") if _hand_disabled else renpy.random.choice(["right", "left"])
                store._slap_hide_hand = _spank_side
                _spank_img = "tenny laying_slap_%s" % _spank_side
                _spank_tf = ld_slap_right_in if _spank_side == "right" else ld_slap_left_in
                if store.laying_grab:
                    renpy.hide("ld_grab_%s" % _spank_side)

            show expression _spank_img as spank_hand at _spank_tf zorder 10090

            if _spank_side == "right":
                show expression "tenny laying_slap_wave_right" as slap_wave at ld_slap_wave_right_in zorder 9862
            else:
                show expression "tenny laying_slap_wave_left" as slap_wave at ld_slap_wave_left_in zorder 9862

            $ renpy.pause(0.08)
            call Punch from _call_Punch_pillow_spank

            python:
                state = sprite_state.setdefault(girl.Id, {})
                state["eyes"] = "eyes_closed"
            call LD_ApplySpeed(girl, laying_speed) from _call_LD_ApplySpeed_pillow_spank_blink
            $ renpy.pause(0.12, hard=True)

            $ set_scene_expression(girl, "scared")
            call LD_ApplySpeed(girl, laying_speed) from _call_LD_ApplySpeed_pillow_spank_expr
            $ renpy.pause(0.20)

            hide spank_hand
            $ store._slap_hide_hand = None
            call LD_ApplySpeed(girl, laying_speed) from _call_LD_ApplySpeed_pillow_spank_restore

            # still a spank on her ass (her spank record), taken scared: not enjoyed
            $ spank_note(girl, False, "pillow_refused")
            $ Say_Line(girl, _("Fine..."))

    return
