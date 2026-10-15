# ============================================================
# CORE COWGIRL SYSTEM
# ============================================================

default cowgirl_speed = 0
default cg_blink = False
default cg_eyes_img = ""
default cg_brows_img = ""
default cg_closed_eye_img = ""
default cowgirl_started = False
default cowgirl_arms_pose = 1
default cowgirl_masturbating = False
default cowgirl_rub_mode = False
default cowgirl_tip_mode = False
default _cowgirl_escalated = False
default cowgirl_guy_arms_visible = True
default cowgirl_guy_touch = None
default _slap_hide_hand = None
default _player_hand_disabled = None
default _cowgirl_girl = None
default _cg_anim_origin = 0.0
default _cg_eyes_locked = False
default _cg_force_static = False
default _cg_impact_active = False
default condom_active = False
default condom_denied = False
default _condom_last_trait = frozenset()
default _condom_removal_denied = False
default _creampie_warned = False
default _creampie_consent = "denied"
default _scene_condom_break = False
default _scene_condom_break_believed = False
default _financial_scene_active = False
default _financial_extras_paid = {}
default _financial_is_anal = False
default _recorded_during_coercion = False   # a video was recorded during THIS coerced scene (_tag_coercion_on_vid)
default _cowgirl_face_ordered_shown = False

image cowgirl_condom = "images/characters/Player/Cowgirl Condom.png"
image cowgirl_condom_broken = "images/characters/Player/Broken Cowgirl Condom.png"

init python:
    import math
    import time as _time

    # ==========================================================
    # SHARED YOFFSET — uses ABSOLUTE time so every layer
    # always computes the exact same value in every frame,
    # even if Ren'Py resets a transform's shown-time (st).
    # ==========================================================
    def _cg_ease(t):
        return 0.5 - 0.5 * math.cos(math.pi * t)

    def _cg_easein(t):
        return t * t

    # ==========================================================
    # ZOOM per speed — subtle pulse synced with the bounce.
    # Returns zoom value (1.0 = no zoom).
    # Higher yoffset (girl lower / deeper) = slight zoom in.
    # ==========================================================
    _CG_ZOOM_PARAMS = {
        0: (1.0, 0.015),      # idle: visible breathing
        1: (1.0, 0.020),      # slow: clear pulse
        2: (1.0, 0.025),      # standard: moderate
        3: (1.0, 0.035),      # fast: strong
        4: (1.02, 0.015),     # cumming: slightly zoomed in + pulse
    }

    def _cg_calc_zoom(yoffset, speed):
        base_zoom, amplitude = _CG_ZOOM_PARAMS.get(speed, (1.0, 0.0))
        if speed == 0 or speed == 4:
            # Time-based breathing zoom — independent of Y
            freq = 0.7 if speed == 0 else 2.5  # cumming: faster pulse
            t = _time.time()
            breath = 0.5 + 0.5 * math.sin(t * freq)
            return base_zoom + amplitude * breath
        idle_base = 30.0
        peak = {1: 105.0, 2: 125.0, 3: 190.0}.get(speed, 105.0)
        if peak == idle_base:
            return base_zoom
        # Normalize displacement 0..1 where 1 = deepest
        t = max(0.0, min(1.0, (yoffset - idle_base) / (peak - idle_base)))
        return base_zoom + amplitude * t

    # ==========================================================
    # BODY SWAY — gentle rotation using absolute clock.
    # Two sine waves for organic feel (different from head sway).
    # ==========================================================
    _CG_SWAY_PARAMS = {
        0: (1.8, 0.25, 1.0, 0.17),    # idle: visible sway
        1: (1.2, 0.30, 0.8, 0.21),    # slow
        2: (1.5, 0.38, 1.0, 0.26),    # standard
        3: (1.8, 0.45, 1.2, 0.31),    # fast
        4: (0.8, 0.50, 0.5, 0.35),    # cumming: tight trembling sway
    }

    def _cg_calc_sway(speed):
        a1, f1, a2, f2 = _CG_SWAY_PARAMS.get(speed, (1.0, 0.25, 0.6, 0.17))
        t = _time.time()
        return a1 * math.sin(t * f1) + a2 * math.sin(t * f2)

    def _cg_calc_yoffset(elapsed, speed):
        base = 30.0
        if speed == 0:
            # Micro-bounce instead of fully static — just the tip
            cycle = 3.0
            t = elapsed % cycle
            norm = 0.5 - 0.5 * math.cos(2.0 * math.pi * t / cycle)
            return 104.0 + 1.5 * norm   # 104..105.5 range — barely moves down

        # Inverted: starts at peak (bottom), rises to base first, then drops back
        if speed == 1:
            cycle = 2.0
            peak = 105.0
            t = elapsed % cycle
            if t < 1.20:
                return peak + (base - peak) * _cg_ease(t / 1.20)
            t -= 1.20
            if t < 0.35:
                return base
            t -= 0.35
            if t < 0.20:
                return base + (peak - base) * _cg_ease(t / 0.20)
            t -= 0.20
            return peak

        elif speed == 2:
            cycle = 1.31
            peak = 125.0
            t = elapsed % cycle
            if t < 0.75:
                return peak + (base - peak) * _cg_easein(t / 0.75)
            t -= 0.75
            if t < 0.22:
                return base
            t -= 0.22
            if t < 0.16:
                return base + (peak - base) * _cg_ease(t / 0.16)
            t -= 0.16
            return peak

        elif speed == 3:
            cycle = 0.40
            peak = 190.0
            top = 10.0    # goes higher than base
            t = elapsed % cycle
            if t < 0.20:
                return peak + (top - peak) * _cg_easein(t / 0.20)
            t -= 0.20
            return top + (peak - top) * _cg_ease(t / 0.20)

        else:
            # Speed 4 = cumming inside: deep position, short fast bounces
            cycle = 0.35
            deep = 165.0
            t = elapsed % cycle
            norm = 0.5 - 0.5 * math.cos(2.0 * math.pi * t / cycle)
            return deep - 25.0 * norm   # 140..165 range

    # ==========================================================
    # THE LANDING: life on the ride, on the same clock as the bounce. When she comes down on him: every layer of
    # hers settles around the penetration point (a squash, wider and lower, that springs back past rest), her head
    # nods to one side, then the other on the next landing, her boobs follow a beat late, and his hips sink a few px
    # under her weight (the penis with them). It starts easing in just before the drop ends, so nothing pops.
    # ==========================================================
    _CG_CYCLE = {1: 2.0, 2: 1.31, 3: 0.40, 4: 0.35}       # _cg_calc_yoffset's cycle per speed
    _CG_LAND_AT = {1: 1.75, 2: 1.13, 3: 0.0, 4: 0.0}       # when the drop ends in that cycle (she sits deepest)
    # speed -> (squash at the landing, ease-in s before it, s the spring takes to fade, head nod degrees)
    _CG_LAND_PARAMS = {
        1: (0.012, 0.10, 0.30, 1.4),
        2: (0.016, 0.08, 0.24, 1.8),
        3: (0.018, 0.06, 0.09, 1.2),
        4: (0.010, 0.05, 0.08, 0.6),
    }
    # The penetration point on the cowgirl canvas (px): Gwen / Rogue / Negasonic share it (her pussy, the penis at
    # 1251-1354 x 763-1080), so the squash never moves her off the penis. Art drawn elsewhere passes its own (Shion's
    # seated art: _SCG_SEAT).
    _CG_SEAT = (1306, 900)
    _CG_MATRIX_ANCHOR = (960, 750)                        # the anchor of every girl layer's matrixtransform
    # s her boobs' own bounce trails the body (it keeps falling after she lands, keeps rising after she rises)
    _CG_BOOBS_LAG = {1: 0.10, 2: 0.08, 3: 0.05, 4: 0.04}
    # px his hips sink under her when she sits deepest (they rise back with her); the penis rides _cg_guy_func
    _CG_GUY_PRESS = {1: 8.0, 2: 10.0, 3: 12.0, 4: 8.0}
    _CG_DEPTH_RANGE = {1: (30.0, 105.0), 2: (30.0, 125.0), 3: (10.0, 190.0), 4: (140.0, 165.0)}

    def _cg_landing(elapsed, speed):
        """(impulse, landing count): 0 between landings, rising to 1 as she lands, then a damped spring (a small
        negative = the rebound). The count flips the side of the head's nod at each landing."""
        _cyc = _CG_CYCLE.get(speed)
        # no landing while frozen, or while she masturbates / he eats her out (they reuse the speed, she does not ride)
        if (not _cyc or getattr(store, "_cg_force_static", False) or getattr(store, "cowgirl_masturbating", False)
                or getattr(store, "_oral_active", False)):
            return 0.0, 0
        _amp, _ramp, _decay, _nod = _CG_LAND_PARAMS[speed]
        _t = elapsed - _CG_LAND_AT[speed]
        _n = int(math.floor(_t / _cyc))
        _after = _t - _n * _cyc                    # s since the last landing
        _before = _cyc - _after                    # s to the next one
        _val = math.exp(-_after / _decay) * math.cos(math.pi * _after / (_decay * 2.5))
        if _before < _ramp:                        # easing into the next landing
            _val += math.sin(0.5 * math.pi * (1.0 - _before / _ramp)) ** 2
            _n += 1
        return _val, _n

    def _cg_squash_matrix(elapsed, speed, seat=None):
        """Her squash around her penetration point (seat, default _CG_SEAT; relative to the layers' matrixanchor), for
        the landing."""
        _val, _n = _cg_landing(elapsed, speed)
        if not _val:
            return ScaleMatrix(1.0, 1.0, 1.0)
        _amp = _CG_LAND_PARAMS[speed][0]
        _seat = seat or _CG_SEAT
        _px, _py = _seat[0] - _CG_MATRIX_ANCHOR[0], _seat[1] - _CG_MATRIX_ANCHOR[1]
        return (OffsetMatrix(_px, _py, 0) * ScaleMatrix(1.0 + 0.6 * _amp * _val, 1.0 - _amp * _val, 1.0)
                * OffsetMatrix(-_px, -_py, 0))

    def _cg_guy_press(elapsed, speed):
        """px his hips are pressed into the bed: with her depth, 0 at the top of her bounce."""
        _press = _CG_GUY_PRESS.get(speed, 0.0)
        if not _press:
            return 0.0
        _lo, _hi = _CG_DEPTH_RANGE[speed]
        return _press * max(0.0, min(1.0, (_cg_calc_yoffset(elapsed, speed) - _lo) / (_hi - _lo)))

    def _cg_guy_func(trans, st, at):
        """The penis, the condom and the cum on it (cowgirl_guy_static): 30 px, plus the press of her weight while
        she rides (it used to bob on its own 1.2 s, out of step with her). Still while frozen."""
        trans.yoffset = 30.0 + _cg_guy_now()
        return 0

    def _cg_guy_now():
        """px his hips are pressed down right now (0 when she is still, frozen, or masturbating)."""
        _speed = store.cowgirl_speed
        if _speed < 1 or store._cg_force_static or getattr(store, "cowgirl_masturbating", False):
            return 0.0
        return _cg_guy_press(_time.time() - store._cg_anim_origin, _speed)

    # ----------------------------------------------------------
    # Single transform function — ALL girl layers use this.
    # Uses absolute clock (time.time() - origin) instead of st.
    # ----------------------------------------------------------
    def _cg_slot_func(trans, st, at, seat=None):
        elapsed = _time.time() - store._cg_anim_origin
        speed = store.cowgirl_speed
        yoff = _cg_calc_yoffset(elapsed, speed)
        trans.yoffset = yoff
        sway = _cg_calc_sway(speed)
        zoom = _cg_calc_zoom(yoff, speed)
        trans.matrixanchor = _CG_MATRIX_ANCHOR
        trans.matrixtransform = ScaleMatrix(zoom, zoom, 1.0) * RotateMatrix(0, 0, sway) * _cg_squash_matrix(elapsed, speed, seat)
        return 0

    # ----------------------------------------------------------
    # Boobs transform — same cycle but with extra amplitude.
    # Amplifies the displacement from idle so boobs bounce more.
    # ----------------------------------------------------------
    _CG_BOOBS_EXTRA = {0: 0.0, 1: 0.20, 2: 0.28, 3: 0.32}
    _CG_BOOBS_EXTRA_CLOTHED = {0: 0.0, 1: 0.10, 2: 0.15, 3: 0.18}
    _CG_BOOBS_EXTRA_PETITE = {0: 0.0, 1: -0.10, 2: -0.15, 3: -0.20}
    _CG_BOOBS_EXTRA_PETITE_CLOTHED = {0: 0.0, 1: -0.15, 2: -0.22, 3: -0.30}

    def _cg_boobs_func(trans, st, at, seat=None):
        elapsed = _time.time() - store._cg_anim_origin
        speed = store.cowgirl_speed
        yoffset = _cg_calc_yoffset(elapsed, speed)
        idle_base = 30.0
        # their extra bounce trails the body (_CG_BOOBS_LAG): same size as before, only later
        _lag = _CG_BOOBS_LAG.get(speed, 0.0)
        displacement = (_cg_calc_yoffset(elapsed - _lag, speed) if _lag else yoffset) - idle_base
        _girl = store._cowgirl_girl
        _has_chest = _girl and getattr(_girl, "Chest", None) and not getattr(_girl, "ChestUp", False)
        _is_petite = _girl and getattr(_girl, "body_type", "medium") == "petite"
        if _is_petite:
            _extra_map = _CG_BOOBS_EXTRA_PETITE_CLOTHED if _has_chest else _CG_BOOBS_EXTRA_PETITE
        else:
            _extra_map = _CG_BOOBS_EXTRA_CLOTHED if _has_chest else _CG_BOOBS_EXTRA
        extra = displacement * _extra_map.get(speed, 0.0)
        final_yoff = yoffset + extra
        if not hasattr(store, "_cg_boob_dbg_t"):
            store._cg_boob_dbg_t = 0
        _now = _time.time()
        if _now - store._cg_boob_dbg_t > 3.0:
            store._cg_boob_dbg_t = _now
            print("[CG_BOOB] gid=%s body_type=%s petite=%s chest=%s speed=%s extra_map=%s disp=%.1f extra=%.1f final=%.1f" % (getattr(_girl, "gid", "?"), getattr(_girl, "body_type", "?"), _is_petite, _has_chest, speed, _extra_map, displacement, extra, final_yoff))
        trans.yoffset = final_yoff
        sway = _cg_calc_sway(speed)
        zoom = _cg_calc_zoom(final_yoff, speed)
        trans.matrixanchor = _CG_MATRIX_ANCHOR
        trans.matrixtransform = ScaleMatrix(zoom, zoom, 1.0) * RotateMatrix(0, 0, sway) * _cg_squash_matrix(elapsed, speed, seat)
        return 0

    # ----------------------------------------------------------
    # Head rotation — subtle sway using absolute clock.
    # Two overlapping sine waves for organic movement.
    # ----------------------------------------------------------
    # ----------------------------------------------------------
    # Static slot — no bounce but still has sway + breathing zoom.
    # Used during masturbation / force_static moments.
    # ----------------------------------------------------------
    # Oral gasp: (amplitude_px, angular_freq, phase_offset) per speed
    # Tongue cycles: s1=1.2s, s2=0.8s, s3=0.5s
    # Phase 2.5: body starts rising at ~40% of cycle, just before tongue apex (50%)
    _CG_ORAL_GASP = {
        1: (4.0, 5.236, 2.5),
        2: (5.0, 7.854, 2.5),
        3: (6.0, 12.566, 2.5),
    }

    def _cg_static_func(trans, st, at):
        t = _time.time()
        breath = 1.0 + 0.003 * (0.5 + 0.5 * math.sin(t * 0.8))
        trans.zoom = breath
        if getattr(store, "_oral_active", False):
            amp, freq, phase = _CG_ORAL_GASP.get(store.cowgirl_speed, (0.0, 0.0, 0.0))
            gasp = amp * max(0.0, math.sin(t * freq - phase))
            trans.yoffset = 104.0 - gasp
        else:
            trans.yoffset = 104.0
        return 0

    def _cg_head_rot_func(trans, st, at):
        # Uses raw clock — NOT tied to _cg_anim_origin so it never
        # resets when speed changes.
        t = _time.time()
        angle = 2.5 * math.sin(t * 0.4) + 1.5 * math.sin(t * 0.27)
        # her nod at each landing (_cg_landing, on the bounce's clock), to one side then the other
        _speed = getattr(store, "cowgirl_speed", 0)
        if _speed in _CG_LAND_PARAMS:
            _val, _n = _cg_landing(t - store._cg_anim_origin, _speed)
            angle += _CG_LAND_PARAMS[_speed][3] * _val * (1 if _n % 2 else -1)
        trans.matrixanchor = (1304, 288)
        trans.matrixtransform = RotateMatrix(0, 0, angle)
        return 0

    # ----------------------------------------------------------
    # Hand rotation — speed-dependent rubbing motion.
    # Anchor at (1239, 767) — pivot at wrist/palm area.
    # ----------------------------------------------------------
    _CG_HAND_ROT_PARAMS = {
        0: (0.0, 0.0, 0.0, 0.0),
        1: (5.0, 10.0, 3.0, 7.0),
        2: (5.0, 18.0, 3.0, 12.0),
        3: (5.0, 28.0, 3.0, 19.0),
    }

    def _cg_hand_rot_func(trans, st, at):
        speed = store.cowgirl_speed
        a1, f1, a2, f2 = _CG_HAND_ROT_PARAMS.get(speed, (0.0, 0.0, 0.0, 0.0))
        if a1 == 0.0:
            trans.matrixtransform = RotateMatrix(0, 0, 0)
            return 0
        t = _time.time()
        angle = a1 * math.sin(t * f1) + a2 * math.sin(t * f2)
        trans.matrixanchor = (1239, 767)
        trans.matrixtransform = RotateMatrix(0, 0, angle)
        return 0

    # ----------------------------------------------------------
    # Guy transform helper (unchanged — guy moves independently)
    # ----------------------------------------------------------
    def cowgirl_get_guy_transform(speed):
        return cowgirl_guy_static if speed >= 1 else cowgirl_guy_idle

    # ----------------------------------------------------------
    # EXPRESSION POOLS (by speed)
    # ----------------------------------------------------------
    _CG_EYES_BY_SPEED = {
        0: ["eyes_normal", "eyes_side", "eyes_side_2"],
        1: ["eyes_normal", "eyes_squint", "eyes_side", "eyes_side_2"],
        2: ["eyes_squint", "eyes_squint_big", "eyes_surprised", "eyes_squint_2"],
        3: ["eyes_squint_big", "eyes_surprised", "eyes_surprised_2", "eyes_squint_2"],
    }

    _CG_BROWS_BY_SPEED = {
        0: ["brows_normal"],
        1: ["brows_normal", "brows_horny"],
        2: ["brows_horny", "brows_surprised", "brows_confused"],
        3: ["brows_horny", "brows_surprised"],
    }

    _CG_MOUTH_BY_SPEED = {
        0: ["mouth_normal", "mouth_disgusted"],
        1: ["mouth_normal", "mouth_laugh", "mouth_disgusted"],
        2: ["mouth_open_teeth", "mouth_sch", "mouth_tongue", "mouth_surprised"],
        3: ["mouth_open_teeth", "mouth_sch", "mouth_tongue", "mouth_serious"],
    }

    # ----------------------------------------------------------
    # EXPRESSION CYCLE (background thread)
    # ----------------------------------------------------------
    def _cg_expression_guard(girl):
        return not getattr(store, '_cg_impact_active', False)

    def _cg_pool_override(girl, speed, eyes_pool, brows_pool, mouth_pool):
        if getattr(store, "_cg_eyes_locked", False):
            cur_eyes = sprite_state.get(girl.Id, {}).get("eyes", "eyes_normal")
            return ([cur_eyes], brows_pool, mouth_pool)
        return (eyes_pool, brows_pool, mouth_pool)

    def _cg_expression_refresh(girl, state):
        if getattr(store, "hiding_face", False):
            state["eyes"] = "eyes_closed"
        attrs = _build_cowgirl_attributes(girl)
        if getattr(store, "hiding_face", False):
            _hr_attrs = []
            for _a in attrs:
                if _a.startswith("eyes_"):
                    _hr_attrs.append("eyes_closed")
                elif _a.startswith("arms_high_") and _a != "arms_high_none":
                    _hr_attrs.append("arms_high_none")
                elif _a.startswith("arms_low_") and _a != "arms_low_none":
                    _hr_attrs.append("arms_low_none")
                elif _a == "shoulder_left_on":
                    _hr_attrs.append("shoulder_left_none")
                elif _a.startswith("masturbate_"):
                    _hr_attrs.append("masturbate_hand_none")
                else:
                    _hr_attrs.append(_a)
            attrs = _hr_attrs
        img_name = "%s cowgirl" % girl.gid
        if attrs:
            img_name += " " + " ".join(attrs)
        if store.cowgirl_masturbating or store._cg_force_static or getattr(store, "cowgirl_speed", 0) == 0:
            renpy.show(img_name, tag=girl.gid, at_list=[cowgirl_slot_static], zorder=9980)
        else:
            renpy.show(img_name, tag=girl.gid, at_list=[cowgirl_slot_synced], zorder=9980)
        renpy.restart_interaction()

    def _cg_expression_cycle(girl):
        _scene_expression_cycle(girl, "_cowgirl_girl", "cowgirl_speed",
            _CG_EYES_BY_SPEED, _CG_BROWS_BY_SPEED, _CG_MOUTH_BY_SPEED,
            sleep_range=(4.0, 9.0), guard_fn=_cg_expression_guard,
            pool_override_fn=_cg_pool_override, refresh_fn=_cg_expression_refresh)

    def _scg_expression_cycle(girl):
        """Shion cowgirl expression cycle — no refresh_fn (ConditionSwitch reads sprite_state directly)."""
        _scene_expression_cycle(girl, "_cowgirl_girl", "cowgirl_speed",
            _CG_EYES_BY_SPEED, _CG_BROWS_BY_SPEED, _CG_MOUTH_BY_SPEED,
            sleep_range=(4.0, 9.0), guard_fn=_cg_expression_guard,
            pool_override_fn=_cg_pool_override)

    # ----------------------------------------------------------
    # THE MASTURBATION POSES (girl.mast_pose, GIRLS_CONFIG): "cowgirl" (the riding scene, this file),
    # "laying_down" (Tenny, Core_LayingDown) and "doggy" (Shion, Core_Doggy). The MASTURBATE_* labels below
    # redirect by it; these helpers are the one place for what the caught-masturbating flows (shower, her room,
    # GirlCumming) do to her when she notices him and when he keeps watching.
    # ----------------------------------------------------------
    _MAST_SPEED_VAR = {"cowgirl": "cowgirl_speed", "laying_down": "laying_speed", "doggy": "doggy_speed"}
    _MAST_ORAL_POSES = ("cowgirl", "laying_down")     # cunnilingus art exists in these (the doggy one has none)

    def _mast_speed(girl):
        """Her current masturbation speed, whatever the pose's speed variable."""
        return getattr(store, _MAST_SPEED_VAR.get(getattr(girl, "mast_pose", "cowgirl"), "cowgirl_speed"), 0)

    def _mast_oral_ok(girl):
        return getattr(girl, "mast_pose", "cowgirl") in _MAST_ORAL_POSES

    def _mast_presence_break(girl):
        """She notices him: her hand comes off, a surprised face, the body back at rest (eyes unlocked)."""
        store._cg_eyes_locked = False
        _mpose = getattr(girl, "mast_pose", "cowgirl")
        if _mpose == "laying_down":
            store._ld_masturbating = False
            store.laying_speed = 0
            if hasattr(store, "_gc_prev_laying_speed"):
                del store._gc_prev_laying_speed
            set_scene_expression(girl, "surprised")
        elif _mpose == "doggy":
            store._dg_masturbating = False
            store.doggy_speed = 0
            set_scene_expression(girl, "surprised")
            if store._sdg_girl is girl and callable(globals().get("_sdg_apply_speed")):
                _sdg_apply_speed(girl, 0)
        else:
            store.cowgirl_masturbating = False
            store.cowgirl_arms_pose = 1
            renpy.hide("cowgirl_masturbate_arm")
            renpy.hide("cowgirl_masturbate_hand")
            state = sprite_state.setdefault(girl.Id, {})
            state["eyes"] = "eyes_surprised"
            state["mouth"] = "mouth_surprised"
            state["brows"] = "brows_surprised"
            attrs = _build_cowgirl_attributes(girl)
            img_name = "%s cowgirl" % girl.gid
            if attrs:
                img_name += " " + " ".join(attrs)
            renpy.show(img_name, tag=girl.gid, at_list=[cowgirl_slot_static], zorder=9980)
        print("[MAST] presence break: %s pose=%s" % (girl.gid, _mpose))

    def _mast_presence_resume(girl):
        """He may keep watching: her hand goes back (the caller re-applies the speed, MASTURBATE_ApplySpeed)."""
        _mpose = getattr(girl, "mast_pose", "cowgirl")
        if _mpose == "laying_down":
            store._ld_masturbating = True
        elif _mpose == "doggy":
            store._dg_masturbating = True
        else:
            store.cowgirl_masturbating = True
            store.cowgirl_arms_pose = 2
            attrs = _build_cowgirl_attributes(girl)
            img_name = "%s cowgirl" % girl.gid
            if attrs:
                img_name += " " + " ".join(attrs)
            renpy.show(img_name, tag=girl.gid, at_list=[cowgirl_slot_static], zorder=9980)
        print("[MAST] presence resume: %s pose=%s speed=%s" % (girl.gid, _mpose, _mast_speed(girl)))

# ==========================================================
# SINGLE GIRL TRANSFORM — every girl layer uses this one.
# ==========================================================
transform cowgirl_slot_synced:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    function _cg_slot_func

# Boobs — same sync but extra bounce when naked
transform cowgirl_boobs_synced:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    function _cg_boobs_func

# Head — subtle rotation around (1304, 288)
transform cg_head_rot:
    subpixel True
    function _cg_head_rot_func

# Hand — speed-dependent rotation around (1239, 767)
transform cg_hand_rot:
    subpixel True
    function _cg_hand_rot_func

# Static girl position — sway + breathing zoom, no bounce
transform cowgirl_slot_static:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    function _cg_static_func

# Static boobs — same as static slot
transform cowgirl_boobs_static:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    function _cg_static_func

# Masturbation hand — static position + rotation
transform cowgirl_hand_masturbate:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 104
    function _cg_hand_rot_func

# ==========================================================
# ORAL TONGUE ANIMATION — frame-by-frame licking
# ==========================================================

image player_tongue_s1:
    "images/characters/Player/Tongue/Guy Tongue 1.png"
    pause 0.12
    "images/characters/Player/Tongue/Guy Tongue 2.png"
    pause 0.12
    "images/characters/Player/Tongue/Guy Tongue 3.png"
    pause 0.12
    "images/characters/Player/Tongue/Guy Tongue 4.png"
    pause 0.12
    "images/characters/Player/Tongue/Guy Tongue 5.png"
    pause 0.12
    "images/characters/Player/Tongue/Guy Tongue 6.png"
    pause 0.12
    "images/characters/Player/Tongue/Guy Tongue 7.png"
    pause 0.12
    "images/characters/Player/Tongue/Guy Tongue 8.png"
    pause 0.12
    "images/characters/Player/Tongue/Guy Tongue 9.png"
    pause 0.12
    "images/characters/Player/Tongue/Guy Tongue 10.png"
    pause 0.12
    repeat

image player_tongue_s2:
    "images/characters/Player/Tongue/Guy Tongue 1.png"
    pause 0.08
    "images/characters/Player/Tongue/Guy Tongue 2.png"
    pause 0.08
    "images/characters/Player/Tongue/Guy Tongue 3.png"
    pause 0.08
    "images/characters/Player/Tongue/Guy Tongue 4.png"
    pause 0.08
    "images/characters/Player/Tongue/Guy Tongue 5.png"
    pause 0.08
    "images/characters/Player/Tongue/Guy Tongue 6.png"
    pause 0.08
    "images/characters/Player/Tongue/Guy Tongue 7.png"
    pause 0.08
    "images/characters/Player/Tongue/Guy Tongue 8.png"
    pause 0.08
    "images/characters/Player/Tongue/Guy Tongue 9.png"
    pause 0.08
    "images/characters/Player/Tongue/Guy Tongue 10.png"
    pause 0.08
    repeat

image player_tongue_s3:
    "images/characters/Player/Tongue/Guy Tongue 1.png"
    pause 0.05
    "images/characters/Player/Tongue/Guy Tongue 2.png"
    pause 0.05
    "images/characters/Player/Tongue/Guy Tongue 3.png"
    pause 0.05
    "images/characters/Player/Tongue/Guy Tongue 4.png"
    pause 0.05
    "images/characters/Player/Tongue/Guy Tongue 5.png"
    pause 0.05
    "images/characters/Player/Tongue/Guy Tongue 6.png"
    pause 0.05
    "images/characters/Player/Tongue/Guy Tongue 7.png"
    pause 0.05
    "images/characters/Player/Tongue/Guy Tongue 8.png"
    pause 0.05
    "images/characters/Player/Tongue/Guy Tongue 9.png"
    pause 0.05
    "images/characters/Player/Tongue/Guy Tongue 10.png"
    pause 0.05
    repeat

transform mast_tongue_pos_gwen:
    pos (1257, 979)

transform mast_tongue_pos_rogue:
    pos (1257, 972)

transform mast_tongue_pos_ntw:
    pos (1257, 972)

# ==========================================================
# GUY / PENIS TRANSFORMS
# ==========================================================
# The penis while she rides (the name is old): on the bounce's clock, pressed down with her weight (_cg_guy_func)
transform cowgirl_guy_static:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    function _cg_guy_func

transform cowgirl_guy_idle:
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 30

transform cowgirl_penis_speed0:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    xoffset 0
    yoffset 0
    block:
        ease 0.60 yoffset 2
        ease 0.60 yoffset 0
        repeat

transform cowgirl_penis_speed1:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    xoffset 0
    yoffset 16
    block:
        ease 1.20 yoffset 0
        pause 0.35
        ease 0.20 yoffset 16
        pause 0.25
        repeat

transform cowgirl_penis_speed2:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    xoffset 0
    yoffset 20
    block:
        easein 0.75 yoffset 0
        pause 0.22
        ease 0.16 yoffset 20
        pause 0.18
        repeat

transform cowgirl_penis_speed3:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    xoffset 0
    yoffset 24
    block:
        easein 0.20 yoffset 0
        ease 0.20 yoffset 24
        repeat

# Penis slide-in — slides up from below into position
transform cowgirl_penis_slide_in:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    alpha 1.0
    yoffset 400
    easein 0.5 yoffset 30

# Penis slide-out — slides down off screen
transform cowgirl_penis_slide_out:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    alpha 1.0
    yoffset 30
    easeout 0.5 yoffset 400

# Slap hand transforms (cowgirl perspective — hand comes from sides)
transform cowgirl_slap_right_in:
    subpixel True
    anchor (0.5, 0.5)
    xpos 1.3
    ypos 0.60
    alpha 1.0
    easein 0.08 xpos 0.55
    pause 0.15
    easeout 0.25 xpos -0.3 alpha 0.0

transform cowgirl_slap_left_in:
    subpixel True
    anchor (0.5, 0.5)
    xpos -0.3
    ypos 0.60
    alpha 1.0
    easein 0.08 xpos 0.45
    pause 0.15
    easeout 0.25 xpos 1.3 alpha 0.0

# ============================================================
# Apply speed
# ============================================================
label COWGIRL_ApplySpeed(girl, speed=1):
    $ print("[CG_APPLY] ENTER gid=%s speed=%d" % (girl.gid, speed))

    python:
        # When called with speed >= 1, always clear force_static (resume animation)
        if speed >= 1:
            store._cg_force_static = False
        # Set the absolute time origin so all layers share the same clock (Shion's own layers ride it too)
        if not store._cg_force_static:
            store._cg_anim_origin = _time.time()

        if speed >= 1 and getattr(girl, "Panties", None):
            if not girl.PantiesDown:
                girl.PantiesDown = True
                _gid_pan = getattr(girl, "gid", "")
                _pan_cfg = CLOTHING_REGISTRY.get(_gid_pan, {}).get(girl.Panties, {})
                _pan_states = _pan_cfg.get("states", ["full"])
                girl.clothes_state["panties"] = "side" if "side" in _pan_states else "down"

    if girl.gid == "shion":
        $ _scg_apply_speed(girl, speed)
        return

    $ penis_img = "%s cowgirl_penis" % girl.gid
    $ penis_side_img = "%s cowgirl_penis_top" % girl.gid

    python:
        guy_transform = cowgirl_get_guy_transform(speed)
        if "_build_cowgirl_attributes" in globals():
            attrs = _build_cowgirl_attributes(girl)
        else:
            attrs = _build_attributes_for_girl(girl, pose="cowgirl")
        if store.hiding_face:
            _hide_attrs = []
            for _a in attrs:
                if _a.startswith("eyes_"):
                    _hide_attrs.append("eyes_closed")
                elif _a.startswith("arms_high_") and _a != "arms_high_none":
                    _hide_attrs.append("arms_high_none")
                elif _a.startswith("arms_low_") and _a != "arms_low_none":
                    _hide_attrs.append("arms_low_none")
                elif _a == "shoulder_left_on":
                    _hide_attrs.append("shoulder_left_none")
                elif _a.startswith("masturbate_"):
                    _hide_attrs.append("masturbate_hand_none")
                else:
                    _hide_attrs.append(_a)
            attrs = _hide_attrs
            state = sprite_state.setdefault(girl.Id, {})
            state["eyes"] = "eyes_closed"

        img_name = "%s cowgirl" % girl.gid
        if attrs:
            img_name += " " + " ".join(attrs)

        debug_log("[CG_APPLY] img_name=%s" % img_name)
        debug_log("[CG_APPLY] attrs=%s" % str(attrs))
        debug_log("[CG_APPLY] Chest=%s ChestUp=%s Panties=%s PantiesDown=%s Over=%s" % (girl.Chest, girl.ChestUp, girl.Panties, girl.PantiesDown, girl.Over))
        debug_log("[CG_APPLY] clothes=%s states=%s" % (str(girl.clothes), str(girl.clothes_state)))
        debug_log("[CG_APPLY] cowgirl_started=%s rub_mode=%s tip_mode=%s mast=%s speed=%s" % (store.cowgirl_started, getattr(store, "cowgirl_rub_mode", False), getattr(store, "cowgirl_tip_mode", False), getattr(store, "cowgirl_masturbating", False), speed))

        # Pick synced or static transforms based on force_static flag
        _fs = store._cg_force_static
        _slot_tf = cowgirl_slot_static if _fs else cowgirl_slot_synced
        _boob_tf = cowgirl_boobs_static if _fs else cowgirl_boobs_synced
        _guy_tf  = cowgirl_guy_idle if _fs else guy_transform

        debug_log("[CG_APPLY] force_static=%s" % _fs)

        # Validate: check each attr exists in the layeredimage
        for _a in attrs:
            _test_img = "%s cowgirl %s" % (girl.gid, _a)
            if not renpy.has_image(_test_img):
                debug_log("[CG_APPLY] WARNING: invalid attr '%s' — not in cowgirl layeredimage!" % _a)

        # -- All girl layers --
        try:
            renpy.show(img_name, tag=girl.gid, at_list=[_slot_tf], zorder=9980)
        except Exception as _cg_err:
            debug_log("[CG_APPLY] ERROR showing layeredimage: %s" % str(_cg_err))

        # -- Hide arm layers (girl covering face during recording) --
        # Right arm behind body, Left 2 below Left 1
        _CG_HIDE_ARM_Z = {"hide_arm_right": 9975, "hide_arm_left_2": 9977, "hide_arm_left_1": 9995, "hide_arm_left_2_over": 9996}
        if store.hiding_face:
            for _ha_suffix, _ha_z in _CG_HIDE_ARM_Z.items():
                _ha_img = "%s cowgirl_%s" % (girl.gid, _ha_suffix)
                _ha_tag = "cowgirl_%s" % _ha_suffix
                if renpy.has_image(_ha_img):
                    renpy.show(_ha_img, tag=_ha_tag, at_list=[_slot_tf], zorder=_ha_z)
                else:
                    renpy.hide(_ha_tag)
        else:
            for _ha_suffix in _CG_HIDE_ARM_Z:
                renpy.hide("cowgirl_%s" % _ha_suffix)

        # Skirt bottom (below everything)
        _skirt_bottom_img = "%s cowgirl_skirt_bottom" % girl.gid
        if girl.Legs and renpy.has_image(_skirt_bottom_img):
            renpy.show(_skirt_bottom_img, tag="cowgirl_skirt_bottom", at_list=[_slot_tf], zorder=9960)
        else:
            renpy.hide("cowgirl_skirt_bottom")

        _lb_img = "%s cowgirl_legs_bottom" % girl.gid
        _lb_exists = renpy.has_image(_lb_img)
        debug_log("[CG_APPLY] legs_bottom: img=%s exists=%s" % (_lb_img, _lb_exists))
        if _lb_exists:
            renpy.show(_lb_img, tag="cowgirl_legs_bottom", at_list=[_slot_tf], zorder=9965)
        else:
            renpy.hide("cowgirl_legs_bottom")

        # Panties side bottom standalone (displaced panties piece between legs)
        _pan_item = getattr(girl, "Panties", None)
        _pan_state = girl.clothes_state.get("panties", "full") if hasattr(girl, "clothes_state") else "full"
        _pan_displaced = _pan_state == "side"
        print("[CG_APPLY] panties_side_bottom: item=%s state=%s displaced=%s" % (_pan_item, _pan_state, _pan_displaced))
        if _pan_displaced:
            if _pan_item == "bikini_panties":
                _psb_img = "%s cowgirl_bikini_panties_side_bottom" % girl.gid
            else:
                _psb_img = "%s cowgirl_panties_side_bottom" % girl.gid
            _psb_exists = renpy.has_image(_psb_img)
            print("[CG_APPLY] panties_side_bottom: img=%s exists=%s" % (_psb_img, _psb_exists))
            if _psb_exists:
                renpy.show(_psb_img, tag="cowgirl_panties_side_bottom", at_list=[_slot_tf], zorder=9978)
            else:
                renpy.hide("cowgirl_panties_side_bottom")
        else:
            renpy.hide("cowgirl_panties_side_bottom")

        # -- Chest clothing --
        _chest_item = girl.Chest
        _chest_has_cg = False
        if _chest_item:
            _gid = getattr(girl, "gid", girl.Id)
            _chest_cfg = CLOTHING_REGISTRY.get(_gid, {}).get(_chest_item, {})
            _chest_has_cg = "cowgirl" in _chest_cfg.get("poses", {})

        # Fixed layer: e.g. bikini band that sits between torso and boobs
        _ct_fixed_img = "%s cowgirl_%s_fixed" % (girl.gid, _chest_item) if _chest_item else None
        _ct_fixed_z = 9984 if girl.gid == "ntw" else 9981

        if _chest_item == "corset" and _chest_has_cg and not girl.ChestUp:
            # Corset: hardcoded standalone sprites (unchanged)
            renpy.show("%s cowgirl_corset" % girl.gid, tag="cowgirl_corset", at_list=[_boob_tf], zorder=9985)
            renpy.show("%s cowgirl_corset_up" % girl.gid, tag="cowgirl_corset_up", at_list=[_slot_tf], zorder=9984)
            renpy.hide("cowgirl_chest_top")
            renpy.hide("cowgirl_chest_fixed")
            renpy.show("%s cowgirl_boobs_naked" % girl.gid, tag="cowgirl_boobs", at_list=[_boob_tf], zorder=9982)
            renpy.show("%s cowgirl_nipples" % girl.gid, tag="cowgirl_nipples", at_list=[_boob_tf], zorder=9983)
        elif _chest_item == "corset" and _chest_has_cg and girl.ChestUp:
            renpy.hide("cowgirl_corset")
            renpy.show("%s cowgirl_corset_up" % girl.gid, tag="cowgirl_corset_up", at_list=[_slot_tf], zorder=9985)
            renpy.hide("cowgirl_chest_top")
            renpy.hide("cowgirl_chest_fixed")
            renpy.show("%s cowgirl_boobs_naked" % girl.gid, tag="cowgirl_boobs", at_list=[_boob_tf], zorder=9986)
            renpy.show("%s cowgirl_nipples" % girl.gid, tag="cowgirl_nipples", at_list=[_boob_tf], zorder=9987)
        elif _chest_has_cg and not girl.ChestUp:
            # Generic chest item (bikini etc): standalone image by naming convention
            _ct_img = "%s cowgirl_%s" % (girl.gid, _chest_item)
            renpy.hide("cowgirl_corset")
            renpy.hide("cowgirl_corset_up")
            if renpy.has_image(_ct_img):
                renpy.show(_ct_img, tag="cowgirl_chest_top", at_list=[_boob_tf], zorder=9985)
            else:
                renpy.hide("cowgirl_chest_top")
            # Fixed layer: between torso and boobs (or above for NTW)
            if _ct_fixed_img and renpy.has_image(_ct_fixed_img):
                renpy.show(_ct_fixed_img, tag="cowgirl_chest_fixed", at_list=[_slot_tf], zorder=_ct_fixed_z)
            else:
                renpy.hide("cowgirl_chest_fixed")
            renpy.show("%s cowgirl_boobs_naked" % girl.gid, tag="cowgirl_boobs", at_list=[_boob_tf], zorder=9982)
            renpy.show("%s cowgirl_nipples" % girl.gid, tag="cowgirl_nipples", at_list=[_boob_tf], zorder=9983)
        elif _chest_has_cg and girl.ChestUp:
            # Generic chest pulled up: standalone "up" image
            _ct_up_img = "%s cowgirl_%s_up" % (girl.gid, _chest_item)
            renpy.hide("cowgirl_corset")
            renpy.hide("cowgirl_corset_up")
            # Fixed layer stays visible when chest is pulled up (band still on)
            if _ct_fixed_img and renpy.has_image(_ct_fixed_img):
                renpy.show(_ct_fixed_img, tag="cowgirl_chest_fixed", at_list=[_slot_tf], zorder=_ct_fixed_z)
            else:
                renpy.hide("cowgirl_chest_fixed")
            # Chest up: above boobs, follows boob bounce
            if renpy.has_image(_ct_up_img):
                renpy.show(_ct_up_img, tag="cowgirl_chest_top", at_list=[_boob_tf], zorder=9988)
            else:
                renpy.hide("cowgirl_chest_top")
            renpy.show("%s cowgirl_boobs_naked" % girl.gid, tag="cowgirl_boobs", at_list=[_boob_tf], zorder=9986)
            renpy.show("%s cowgirl_nipples" % girl.gid, tag="cowgirl_nipples", at_list=[_boob_tf], zorder=9987)
        else:
            # No chest clothing — nude
            renpy.hide("cowgirl_corset")
            renpy.hide("cowgirl_corset_up")
            renpy.hide("cowgirl_chest_top")
            renpy.hide("cowgirl_chest_fixed")
            renpy.show("%s cowgirl_boobs_naked" % girl.gid, tag="cowgirl_boobs", at_list=[_boob_tf], zorder=9986)
            renpy.show("%s cowgirl_nipples" % girl.gid, tag="cowgirl_nipples", at_list=[_boob_tf], zorder=9987)

        # -- Guy --
        _guy_z = _gsc(girl.gid, "guy_z", 9970, "cowgirl")
        _guy_synced = _gsc(girl.gid, "guy_synced", False, "cowgirl")
        _guy_at = [_slot_tf] if _guy_synced else [_guy_tf]
        renpy.hide("cowgirl_guy")

        # -- Cum layers (ConditionSwitch — auto-toggle via girl.Cum) --
        renpy.show(
            "%s cowgirl_tummy_cum" % girl.gid,
            tag="cowgirl_tummy_cum",
            at_list=[_slot_tf],
            zorder=9988
        )
        renpy.show(
            "%s cowgirl_penis_cum" % girl.gid,
            tag="cowgirl_penis_cum",
            at_list=[_guy_tf],
            zorder=9978
        )
        renpy.show(
            "%s cowgirl_cum_face" % girl.gid,
            tag="cowgirl_cum_face",
            at_list=[_slot_tf],
            zorder=9992
        )
        # legs_cum: handled inside the layeredimage (cum_legs group)
        if speed <= 0 or _fs:
            _drip_tf = cowgirl_slot_static if _fs else cowgirl_slot_synced
            renpy.show(
                "%s cowgirl_dripping_cum" % girl.gid,
                tag="cowgirl_dripping_cum",
                at_list=[_drip_tf],
                zorder=9982
            )
        else:
            renpy.hide("cowgirl_dripping_cum")

        # -- Guy touch: hands (above everything), left/right independent --
        _hand_disabled = getattr(store, "_player_hand_disabled", None)
        _slap_hide = getattr(store, "_slap_hide_hand", None)
        _cg_touch = getattr(store, "cowgirl_guy_touch", None)

        if _cg_touch == "grab_tits":
            _sq_left = "%s cowgirl_guy_squeeze_left" % girl.gid
            if renpy.has_image(_sq_left):
                # Split left/right assets
                for _side in ("left", "right"):
                    _sq_img = "%s cowgirl_guy_squeeze_%s" % (girl.gid, _side)
                    _sq_tag = "cowgirl_guy_squeeze_%s" % _side
                    if _hand_disabled != _side and _slap_hide != _side and renpy.has_image(_sq_img):
                        renpy.show(_sq_img, tag=_sq_tag, at_list=[_boob_tf], zorder=10050)
                    else:
                        renpy.hide(_sq_tag)
            else:
                # Fallback: single combined image (Rogue, etc.)
                _sq_img = "%s cowgirl_guy_squeeze" % girl.gid
                if renpy.has_image(_sq_img):
                    renpy.show(_sq_img, tag="cowgirl_guy_squeeze_left", at_list=[_boob_tf], zorder=10050)
                renpy.hide("cowgirl_guy_squeeze_right")
        else:
            renpy.hide("cowgirl_guy_squeeze_left")
            renpy.hide("cowgirl_guy_squeeze_right")

        if _cg_touch == "push_down":
            _arm_left = "%s cowgirl_guy_arms_left" % girl.gid
            if renpy.has_image(_arm_left):
                # Split left/right assets — use _slot_tf to sync with girl's legs/body
                for _side in ("left", "right"):
                    _arm_img = "%s cowgirl_guy_arms_%s" % (girl.gid, _side)
                    _arm_tag = "cowgirl_guy_arms_%s" % _side
                    if _hand_disabled != _side and _slap_hide != _side and renpy.has_image(_arm_img):
                        renpy.show(_arm_img, tag=_arm_tag, at_list=[_slot_tf], zorder=9981)
                    else:
                        renpy.hide(_arm_tag)
            else:
                renpy.hide("cowgirl_guy_arms_left")
                renpy.hide("cowgirl_guy_arms_right")
        else:
            renpy.hide("cowgirl_guy_arms_left")
            renpy.hide("cowgirl_guy_arms_right")

    if store._cg_force_static:
        # Frozen state — hide all penis layers (caller manages penis override)
        hide cowgirl_penis
        hide cowgirl_penis_side
        hide cowgirl_condom
        hide cowgirl_condom_broken
    elif speed >= 1:
        # Rub mode: penis above everything (like RCG)
        $ _cg_penis_z = 10060 if store.cowgirl_rub_mode else 9979
        show expression penis_img as cowgirl_penis at cowgirl_guy_static zorder _cg_penis_z
        hide cowgirl_penis_side
        if store.condom_active:
            if store._condom_broken:
                show cowgirl_condom_broken at cowgirl_guy_static zorder _cg_penis_z
                hide cowgirl_condom
            else:
                show cowgirl_condom at cowgirl_guy_static zorder _cg_penis_z
                hide cowgirl_condom_broken
        else:
            hide cowgirl_condom
            hide cowgirl_condom_broken
    else:
        # Speed 0: penis_side above everything (not penetrating yet)
        hide cowgirl_penis
        hide cowgirl_condom
        hide cowgirl_condom_broken
        show expression penis_side_img as cowgirl_penis_side at cowgirl_guy_idle zorder 10060

    return

# ============================================================
# Launch
# ============================================================
label COWGIRL_Launch(girl, from_switch=False):
    $ debug_log("[DEBUG] COWGIRL_Launch: entered, from_switch=%s" % str(from_switch))
    $ _kill_scene_threads(keep_watchers=from_switch)
    $ stop_standing_blink(girl)

    if not from_switch:
        $ public_attention_reset()
        call PlayerExposure(girl) from _call_PlayerExposure_1

    $ girl._prev_pose = getattr(girl, "default_pose", "standing")
    $ girl._prev_slot = getattr(girl, "SpriteLoc", StageCenter)
    if not getattr(girl, "_saved_outfit", None):
        $ girl.SaveOutfit()

    python:
        # Clear other scene refs so set_scene_expression doesn't cross-contaminate
        _clear_scene_refs("cowgirl")
        store.doggy_started = False
        _hide_all_scene_layers(girl)

        _hide_non_scene_girls(girl)

        # Her standing sprite: a pose drawn under her own tag replaces it, layers with tags of their own (Shion's
        # scg_*) do not, and an End right before this (a position switch, the mouth finish) re-showed it
        # (scene_full_cleanup ResetVisuals). Hidden for every girl, as COWGIRL_RubLaunch does
        hide_girl_sprite(girl)

        store._cowgirl_girl = girl
        sprite_state.setdefault(girl.Id, {})["pose"] = "cowgirl"
        store.cowgirl_started = False
        store.cowgirl_rub_mode = False
        store.cowgirl_tip_mode = False
        store.cowgirl_masturbating = False
        store.cowgirl_arms_pose = 1
        store.hiding_face = False
        store._cowgirl_face_ordered_shown = False
        store.cowgirl_guy_arms_visible = True
        store.cowgirl_guy_touch = None
        store._cg_force_static = False
        store._cg_anim_origin = _time.time()

        # Shion custom cowgirl: set her scene ref, init arms variant
        if girl.gid == "shion":
            store._scg_girl = girl
            store._scg_arms_variant = 1

        # Auto-strip items that don't support cowgirl pose
        _gid = getattr(girl, "gid", getattr(girl, "Id", ""))
        _reg = CLOTHING_REGISTRY.get(_gid, {})
        for _slot_name, _slot_attr in [("over", "Over"), ("chest", "Chest")]:
            _item = getattr(girl, _slot_attr, None)
            if not _item:
                _item = girl.clothes.get(_slot_name if _slot_name != "chest" else "chest")
            if _item:
                _item_cfg = _reg.get(_item, {})
                if "cowgirl" not in _item_cfg.get("poses", {}):
                    girl.Outfit_Change(**{_slot_name: "none"}, refresh=False)

        if girl.gid == "shion":
            store._scg_girl = girl
            store._scg_arms_variant = 1
            renpy.invoke_in_thread(_scene_cs_blink_loop, girl, "_cowgirl_girl")
            renpy.invoke_in_thread(_scg_expression_cycle, girl)
        else:
            renpy.invoke_in_thread(_scene_blink_loop, girl, "_cowgirl_girl", "cg_blink")
            renpy.invoke_in_thread(_cg_expression_cycle, girl)

    if "cowgirl_speed" not in globals():
        $ cowgirl_speed = 0

    $ sub_event_reset(girl)
    call COWGIRL_ApplySpeed(girl, cowgirl_speed) from _call_COWGIRL_ApplySpeed_5
    if from_switch:
        with dissolve
    else:
        with fade

    if from_switch:
        # Reset skirt state from previous position
        if girl.clothes_state.get("skirt") == "up":
            $ girl.clothes_state["skirt"] = "full"
        # Coming from another position: panties already handled, just strip
        if girl.Panties is not None:
            $ girl.Outfit_Change(panties="none", pose="cowgirl")
            call COWGIRL_ApplySpeed(girl, cowgirl_speed) from _call_COWGIRL_ApplySpeed_sw1
    else:
        if girl.Legs is not None or girl.Panties is not None:
            $ Say_Line(girl, _("Here... let me give you a better view."))

        # --- BOTTOM (skirt pulled up > panties > bare) ---
        if girl.Legs is not None:
            pause 0.8
            $ girl.Outfit_Change(legs_down=True, pose="cowgirl")
            call COWGIRL_ApplySpeed(girl, cowgirl_speed) from _call_COWGIRL_ApplySpeed_6

        if girl.Panties is not None:
            pause 0.15
            menu:
                "Remove panties":
                    $ girl.Outfit_Change(panties="none", pose="cowgirl")
                    call COWGIRL_ApplySpeed(girl, cowgirl_speed) from _call_COWGIRL_ApplySpeed_7

                "Pull panties to the side" if _item_has_state(girl, "panties", "side"):
                    $ girl.clothes_state["panties"] = "side"
                    call COWGIRL_ApplySpeed(girl, cowgirl_speed) from _call_COWGIRL_ApplySpeed_8

                "Pull panties down" if _item_has_state(girl, "panties", "down"):
                    $ girl.clothes_state["panties"] = "down"
                    call COWGIRL_ApplySpeed(girl, cowgirl_speed) from _call_COWGIRL_ApplySpeed_8b

    # Register exposure after strip (both options count as seeing pussy)
    $ _exp = girl.RegisterAction("player_saw_pussy")
    if _exp["first_time"]:
        call FirstExposureReaction(girl, "pussy") from _call_FirstExposureReaction_6

    return

# ============================================================
# Control Menu
# ============================================================
label COWGIRL_ControlMenu(girl):
    $ debug_log("[DEBUG] COWGIRL_ControlMenu: entered")
    $ store._player_exhausted = False
    $ store._scene_phase = "sex"
    if "cowgirl_speed" not in globals():
        $ cowgirl_speed = 1

    # Reset position switch flag on entry
    $ store._sub_event_position_switched = False
    $ store._cheat_shower_max_act = "sex"

    while True:

        # Position-switch escape: if a sub-event switched us here, return
        if store._sub_event_position_switched:
            $ store._sub_event_position_switched = False
            return

        if Round >= 100:
            $ Say_Line(girl, _scene_time_up_line())
            call COWGIRL_End(girl, dress_up=False) from _call_COWGIRL_End_timeout
            return

        menu:
            "Keep going" if cowgirl_speed >= 1:
                call _sex_scene_tick(girl, "cowgirl", cowgirl_speed) from _call_sst_cg_kg

                if store._sst_result == "condom_ripped":
                    call CG_CondomRemoveAnim(girl) from _call_CG_CondomRemoveAnim_sst_kg
                    call COWGIRL_ApplySpeed(girl, cowgirl_speed) from _call_CG_ApplySpeed_sst_rip

                if store._sst_result == "abort":
                    if store._sst_abort_reason == "post_cum":
                        $ _set_post_cum("cowgirl", "sex")
                        return
                    call _sex_scene_handle_abort(girl, "cowgirl") from _call_sst_abort_cg_kg
                    return

            "Speed up" if cowgirl_speed < 3:
                $ advance_round(TIME_COSTS["sex_tick"])
                $ Say_Player(_("Faster..."))
                $ _was_tip = (cowgirl_speed == 0)
                $ cowgirl_started = True
                $ cowgirl_speed += 1
                if _was_tip:
                    call CG_PenisEnterAnim(girl) from _call_CG_PenisEnterAnim_speedup
                call COWGIRL_ApplySpeed(girl, cowgirl_speed) from _call_COWGIRL_ApplySpeed_9
                call _speed_change_tick(girl, "cowgirl", 1) from _call_sct_cg_su
                if _scene_should_exit():
                    return
                if cowgirl_speed >= 3:
                    $ _watcher_scene_comment("speed_max")
                $ Narration(_("She speeds up her movements."))

            "Speed down" if cowgirl_speed > 0:
                $ advance_round(1)
                $ cowgirl_speed -= 1
                call COWGIRL_ApplySpeed(girl, cowgirl_speed) from _call_COWGIRL_ApplySpeed_10
                call _speed_change_tick(girl, "cowgirl", -1) from _call_sct_cg_sd
                if store._sub_event_position_switched:
                    return
                $ _watcher_scene_comment("speed_down")
                $ Narration(_("She slows her movements."))

            "{color=#fbbf24}Cum{/color}" if player_is_cumming():
                call PlayerCumMenu(girl, "cowgirl") from _call_PlayerCumMenu_voluntary_cg
                $ _handle_post_cum_exit("cowgirl", "sex")
                return

            "Slap her face" if not getattr(store, "hiding_face", False):
                $ advance_round(1)
                call SpankHer(girl, "cowgirl") from _call_SpankHer_cowgirl

            "Tease her..." if cowgirl_speed > 0:
                $ advance_round(1)
                call _tease_menu(girl, "cowgirl") from _call_tease_menu_cg

            "Strip her" if not getattr(store, "_scene_restricted", False):
                $ advance_round(1)
                call COWGIRL_StripMenu(girl) from _call_COWGIRL_StripMenu

            "Touch her..." if not store.cowgirl_guy_touch:
                menu:
                    "Push her down":
                        $ advance_round(1)
                        $ store.cowgirl_guy_touch = "push_down"
                        $ store.cowgirl_guy_arms_visible = True
                        call COWGIRL_ApplySpeed(girl, cowgirl_speed) from _call_COWGIRL_ApplySpeed_11
                    "Grab her tits":
                        $ advance_round(1)
                        $ store.cowgirl_guy_touch = "grab_tits"
                        call COWGIRL_ApplySpeed(girl, cowgirl_speed) from _call_COWGIRL_ApplySpeed_12
                    "Back":
                        pass

            "Let her go" if store.cowgirl_guy_touch:
                $ advance_round(1)
                $ store.cowgirl_guy_touch = None
                $ store.cowgirl_guy_arms_visible = False
                call COWGIRL_ApplySpeed(girl, cowgirl_speed) from _call_COWGIRL_ApplySpeed_letgo

            "Switch arm pose" if not getattr(store, "hiding_face", False):
                $ cowgirl_arms_pose = 2 if cowgirl_arms_pose == 1 else 1
                call COWGIRL_ApplySpeed(girl, cowgirl_speed) from _call_COWGIRL_ApplySpeed_13

            "Record Options..." if not getattr(store, "_recording_active", False) or getattr(store, "_recording_girl", None) == girl:
                menu:
                    "Record her" if not getattr(store, "_recording_active", False):
                        call _sex_phone_menu(girl, "cowgirl") from _call__sex_phone_menu_2
                    "Ask [store._ntr_watching_npc.Name] to record" if store._ntr_partner_watching and not getattr(store, "_recording_active", False):
                        call _watcher_record_start(girl, "cowgirl") from _call_watcher_rec_start_cg_npc
                    "Ask [store._witness_girl.Name] to record" if getattr(store, "_witness_watching", False) and getattr(store, "_witness_girl", None) is not None and not store._ntr_partner_watching and not getattr(store, "_recording_active", False):
                        call _watcher_record_start(girl, "cowgirl") from _call_watcher_rec_start_cg_girl
                    "Stop recording" if getattr(store, "_recording_active", False) and getattr(store, "_recording_girl", None) == girl:
                        $ _rec_stop_name = _get_recording_stopper_name()
                        $ finalize_recording()
                        if store.hiding_face:
                            $ store.hiding_face = False
                        if _rec_stop_name:
                            $ _rec_stop_text = _tl(_("%s stopped the recording.")) % _rec_stop_name
                            $ Narration(_rec_stop_text)
                        else:
                            $ Narration(_("You stop recording."))
                    "Order her to show her face" if getattr(store, "hiding_face", False) and getattr(store, "_recording_active", False) and not getattr(store, "_recording_face_locked", False):
                        $ store.hiding_face = False
                        $ store._cowgirl_face_ordered_shown = True
                        $ Narration(_("You tell her to show her face."))
                    "Back":
                        pass
                call COWGIRL_ApplySpeed(girl, cowgirl_speed) from _call_COWGIRL_ApplySpeed_rec_opts

            "Condom..." if store.condom_active:
                call CondomMidsceneMenu(girl, "cowgirl") from _call_CondomMidsceneMenu
                if not store.condom_active:
                    call CG_CondomRemoveAnim(girl) from _call_CG_CondomRemoveAnim_mid
                    call COWGIRL_ApplySpeed(girl, cowgirl_speed) from _call_COWGIRL_ApplySpeed_14

            "Switch position..." if cowgirl_started and not getattr(store, "_scene_restricted", False):
                if store._condom_broken_hidden:
                    call CondomBreakDiscovery(girl, "cowgirl") from _call_CondomBreakDisc_cg
                if store._stealth_condom_removed:
                    call StealthCondomDiscovery(girl, "cowgirl") from _call_StealthDisc_cg
                menu:
                    "Reverse Cowgirl" if girl_has_pose(girl, "reverse_cowgirl"):
                        $ Say_Player(_("Turn around..."))
                        python:
                            _switch_lines = [
                                _("Mmm, you want me facing away?"),

                                _("Alright, let me turn around for you."),

                                _("Sure... let me switch it up."),

                            ]
                        $ Say_Line(girl, _tl(renpy.random.choice(_switch_lines)))

                        $ _saved_condom = condom_carry_save()
                        $ _saved_clothes = dict(girl.clothes)
                        $ _saved_clothes_state = dict(girl.clothes_state)
                        $ _saved_outfit_ref = getattr(girl, "_saved_outfit", None)
                        call COWGIRL_End(girl, dress_up=False) from _call_COWGIRL_End_switch_rcg
                        $ condom_carry_restore(_saved_condom)
                        $ girl.clothes = _saved_clothes
                        $ girl.clothes_state = _saved_clothes_state
                        $ girl._saved_outfit = _saved_outfit_ref

                        $ rcg_speed = 0
                        $ _scene_position_switch(girl, "cowgirl", "reverse_cowgirl", anal=False)   # player switch: count the new position (and sex, if it is vaginal now)
                        call RCG_Launch(girl, from_switch=True) from _call_RCG_Launch_switch
                        call RCG_ControlMenu(girl) from _call_RCG_ControlMenu_switch

                        $ store._sub_event_position_switched = True

                    "Doggy" if girl_has_pose(girl, "doggy"):
                        $ Say_Player(_("Get on all fours..."))
                        call _femdom_position_gate(girl, "cowgirl", "doggy") from _call_fpg_cg_dg
                        if store._femdom_gate_ok:
                            python:
                                _switch_lines = [
                                    _("You want me from behind? Okay..."),

                                    _("Mmm, doggy style? I like that."),

                                    _("Sure... let me get on all fours."),

                                ]
                            $ Say_Line(girl, _tl(renpy.random.choice(_switch_lines)))

                            $ _saved_condom = condom_carry_save()
                            $ _saved_clothes = dict(girl.clothes)
                            $ _saved_clothes_state = dict(girl.clothes_state)
                            $ _saved_outfit_ref = getattr(girl, "_saved_outfit", None)
                            call COWGIRL_End(girl, dress_up=False) from _call_COWGIRL_End_switch_dg
                            $ condom_carry_restore(_saved_condom)
                            $ girl.clothes = _saved_clothes
                            $ girl.clothes_state = _saved_clothes_state
                            $ girl._saved_outfit = _saved_outfit_ref

                            $ doggy_speed = 0
                            $ _scene_position_switch(girl, "cowgirl", "doggy", anal=getattr(store, "doggy_anal", False))   # player switch: count the new position (and sex, if it is vaginal now)
                            call DG_Launch(girl, from_switch=True) from _call_DG_Launch_cg_switch
                            call DG_ControlMenu(girl) from _call_DG_ControlMenu_cg_switch

                            $ store._sub_event_position_switched = True

                    "Full Nelson" if girl_has_pose(girl, "full_nelson"):
                        $ Say_Player(_("Come here..."))
                        call _femdom_position_gate(girl, "cowgirl", "full_nelson") from _call_fpg_cg_fn
                        if store._femdom_gate_ok:
                            python:
                                _switch_lines = [
                                    _("What are you... oh!"),

                                    _("You're picking me up...?!"),

                                    _("Whoa... okay...!"),

                                ]
                            $ Say_Line(girl, _tl(renpy.random.choice(_switch_lines)))

                            $ _saved_condom = condom_carry_save()
                            $ _saved_clothes = dict(girl.clothes)
                            $ _saved_clothes_state = dict(girl.clothes_state)
                            $ _saved_outfit_ref = getattr(girl, "_saved_outfit", None)
                            call COWGIRL_End(girl, dress_up=False) from _call_COWGIRL_End_switch_fn
                            $ condom_carry_restore(_saved_condom)
                            $ girl.clothes = _saved_clothes
                            $ girl.clothes_state = _saved_clothes_state
                            $ girl._saved_outfit = _saved_outfit_ref

                            $ fn_speed = 0
                            $ _scene_position_switch(girl, "cowgirl", "full_nelson", anal=getattr(store, "fn_anal", False))   # player switch: count the new position (and sex, if it is vaginal now)
                            call FN_Launch(girl, from_switch=True) from _call_FN_Launch_cg_switch
                            call FN_ControlMenu(girl) from _call_FN_ControlMenu_cg_switch

                            $ store._sub_event_position_switched = True

                    "Back":
                        pass

            "Stop now":
                if store._forced_creampie_end_after_orgasm:
                    call _player_stops_after_forced_creampie(girl, "cowgirl") from _call__player_stops_forced_cg
                elif cowgirl_speed >= 1:
                    $ debug_log("[DEBUG] Ask her to stop (CG): Lust=%d speed=%d" % (girl.Lust, cowgirl_speed))
                    $ store._edge_lust_check = (girl.Lust >= 80)
                    if store._edge_lust_check:
                        $ debug_log("[DEBUG] Lust >= 80, entering EdgeDenial")
                        # She begs with him still in her: the scene stays exactly as it is until the action really stops.
                        # "Keep going" goes on at the same speed, her "No, stop." is the same stop as below (author,
                        # 2026-10-09)
                        call EdgeDenial(girl, "cowgirl") from _call_EdgeDenial_cg
                        if girl.Lust >= 100:
                            call GirlCumming(girl, "cowgirl", "cowgirl") from _call_GirlCumming_cg_edge
                        if store._edge_scene_ended:
                            $ store._edge_scene_ended = False
                            call _cum_dispatch_aftermath(girl, "cowgirl") from _call_ca_dispatch_cg_edge_stop
                            return
                    else:
                        $ debug_log("[DEBUG] Lust < 80, ending scene normally")
                        call _cum_dispatch_aftermath(girl, "cowgirl") from _call_ca_dispatch_cg_stop_main
                        return
                else:
                    $ Say_Line(girl, _pick_stop_line(girl))
                    call _cum_dispatch_aftermath(girl, "cowgirl") from _call_ca_dispatch_cg_stop
                    return

label COWGIRL_StripMenu(girl):
    while True:
        $ _legs_label = _("Remove pants") if _strip_name_for_slot(girl, "skirt") == "pants" else _("Remove skirt")
        menu:
            "Remove top" if girl.Over:
                call _strip_approval(girl, ["over"]) from _call__strip_approval_9
                if store._strip_approved:
                    $ girl.Outfit_Change(over="none", pose="cowgirl")
                    if _cowgirl_girl == girl:
                        call COWGIRL_ApplySpeed(girl, cowgirl_speed) from _call_COWGIRL_ApplySpeed_17
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_9

            "Pull chest up" if girl.Chest and girl.clothes_state.get("chest") != "up" and _item_has_state(girl, "chest", "up"):
                call _strip_approval(girl, ["chest"]) from _call__strip_approval_cg_chest_up
                if store._strip_approved:
                    $ girl.Outfit_Change(chest_up=True, pose="cowgirl")
                    if _cowgirl_girl == girl:
                        call COWGIRL_ApplySpeed(girl, cowgirl_speed) from _call_COWGIRL_ApplySpeed_chest_up
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_cg_chest_up

            "Remove chest" if girl.Chest:
                call _strip_approval(girl, _get_strip_slots(girl, "chest")) from _call__strip_approval_10
                if store._strip_approved:
                    $ _do_strip_change(girl, "chest", "cowgirl")
                    if _cowgirl_girl == girl:
                        call COWGIRL_ApplySpeed(girl, cowgirl_speed) from _call_COWGIRL_ApplySpeed_18
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_10

            "Chest down" if girl.Chest and girl.ChestUp:
                $ girl.SetChestUp(False, pose="cowgirl")
                if _cowgirl_girl == girl:
                    call COWGIRL_ApplySpeed(girl, cowgirl_speed) from _call_COWGIRL_ApplySpeed_19

            "[_legs_label]" if girl.Legs:
                call _strip_approval(girl, ["legs"]) from _call__strip_approval_12
                if store._strip_approved:
                    $ girl.Outfit_Change(legs="none", pose="cowgirl")
                    if _cowgirl_girl == girl:
                        call COWGIRL_ApplySpeed(girl, cowgirl_speed) from _call_COWGIRL_ApplySpeed_20
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_11

            "Pull panties to the side" if girl.Panties and girl.clothes_state.get("panties") != "side" and _item_has_state(girl, "panties", "side"):
                call _strip_approval(girl, ["panties"]) from _call__strip_approval_cg_pan_side
                if store._strip_approved:
                    $ girl.clothes_state["panties"] = "side"
                    call COWGIRL_ApplySpeed(girl, cowgirl_speed) from _call_COWGIRL_ApplySpeed_pan_side
                    call CheckExposure(girl) from _call_CheckExposure_cg_pan_side

            "Pull panties down" if girl.Panties and girl.clothes_state.get("panties") != "down" and _item_has_state(girl, "panties", "down"):
                call _strip_approval(girl, ["panties"]) from _call__strip_approval_cg_pan_down
                if store._strip_approved:
                    $ girl.clothes_state["panties"] = "down"
                    call COWGIRL_ApplySpeed(girl, cowgirl_speed) from _call_COWGIRL_ApplySpeed_pan_down
                    call CheckExposure(girl) from _call_CheckExposure_cg_pan_down

            "Remove panties" if girl.Panties:
                call _strip_approval(girl, ["panties"]) from _call__strip_approval_13
                if store._strip_approved:
                    $ girl.Outfit_Change(panties="none", pose="cowgirl")
                    if _cowgirl_girl == girl:
                        call COWGIRL_ApplySpeed(girl, cowgirl_speed) from _call_COWGIRL_ApplySpeed_21
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_12

            "Remove shoes" if getattr(girl, "Shoes", None):
                $ girl.Outfit_Change(shoes="none", pose="cowgirl")
                if _cowgirl_girl == girl:
                    call COWGIRL_ApplySpeed(girl, cowgirl_speed) from _call_COWGIRL_ApplySpeed_22

            "Back":
                return

# ============================================================
# End
# ============================================================
label COWGIRL_End(girl, dress_up=True, was_secret=False):
    $ debug_log("[DEBUG] COWGIRL_End: entered, dress_up=%s was_secret=%s" % (str(dress_up), str(was_secret)))
    $ scene_full_cleanup(girl, was_secret=was_secret)
    $ finalize_recording()
    $ _player_cleanup(girl)

    $ pose = getattr(girl, "_prev_pose", "standing")
    $ slot = _safe_restore_slot(getattr(girl, "_prev_slot", StageCenter))

    python:
        slot_transform = _slot_to_transform(slot)
        _reset_expression_state(girl)

        store._cowgirl_girl = None
        store._scg_girl = None
        store.cowgirl_started = False
        store.cowgirl_masturbating = False
        store._oral_active = False
        renpy.hide("mast_tongue")
        renpy.hide("mast_pussy")
        store.cg_blink = False
        store._cg_eyes_locked = False
        store._cg_force_static = False
        store.hiding_face = False
        girl.ResetVisuals(pose=pose, at_list=[slot_transform])
        _hide_scene_layers("cowgirl")
        if callable(globals().get("_scg_hide_all")):
            _scg_hide_all()
        store.condom_active = False
        store.cowgirl_rub_mode = False
        store.cowgirl_tip_mode = False
        store.cowgirl_guy_touch = None

    if dress_up:
        call DressUp_Sequence(girl) from _call_DressUp_Sequence_3
    $ debug_log("[DEBUG] COWGIRL_End: returning")
    return

# ============================================================
# Cum Animation (inside — pulse + shake, guy arms forced)
# ============================================================
transform cowgirl_penis_cum_pulse():
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    xoffset 0
    yoffset 0
    yzoom 1.0
    pause 0.45
    ease 0.08 yzoom 1.06
    ease 0.15 yzoom 1.0
    pause 0.27
    ease 0.08 yzoom 1.06
    ease 0.15 yzoom 1.0

label CG_CumAnim(girl):
    if girl.gid == "shion":
        $ _apply_cum_expression(girl, "cowgirl", "inside")
        $ store.cowgirl_speed = 4
        call COWGIRL_ApplySpeed(girl, 4) from _call_COWGIRL_ApplySpeed_cum_shion
        call _cum_punch_pair("oral") from _call_cum_punch_cg_cum_shion
        $ store._cg_force_static = True
        $ store.cowgirl_speed = 0
        call COWGIRL_ApplySpeed(girl, 0) from _call_COWGIRL_ApplySpeed_cum_freeze_shion
        python:
            renpy.hide("scg_penis")
            renpy.hide("scg_condom")
        return
    # Cum expression: intense orgasm face + force guy arms
    python:
        _apply_cum_expression(girl, "cowgirl", "inside")
        store.cowgirl_guy_arms_visible = True

    # Speed 4 = cumming inside: deep position, tiny fast bounces
    $ store.cowgirl_speed = 4
    call COWGIRL_ApplySpeed(girl, 4) from _call_COWGIRL_ApplySpeed_cum_grab

    # Penis pulse (+ condom if active)
    $ renpy.show("%s cowgirl_penis" % girl.gid, tag="cowgirl_penis", at_list=[cowgirl_penis_cum_pulse()], zorder=9979)
    if store.condom_active:
        $ _cb_cimg = _condom_img_tag("cowgirl_condom")
        $ renpy.show(_cb_cimg, at_list=[cowgirl_penis_cum_pulse()], zorder=9979)

    call _cum_punch_pair("oral") from _call_cum_punch_cg_cum

    # Freeze into aftermath pose (static, no penis, dripping visible)
    $ store._cg_force_static = True
    $ store.cowgirl_speed = 0
    call COWGIRL_ApplySpeed(girl, 0) from _call_COWGIRL_ApplySpeed_cum_aftermath

    # Slide penis down off screen
    python:
        _pen_img = "%s cowgirl_penis" % girl.gid
        renpy.show(_pen_img, tag="cowgirl_penis", at_list=[cowgirl_penis_slide_out], zorder=9979)
        renpy.hide("cowgirl_penis_side")
        if store._condom_broken:
            renpy.show("cowgirl_condom_broken", at_list=[cowgirl_penis_slide_out], zorder=9979)
            renpy.hide("cowgirl_condom")
        else:
            renpy.hide("cowgirl_condom")
            renpy.hide("cowgirl_condom_broken")
    $ renpy.pause(0.55)
    python:
        renpy.hide("cowgirl_penis")
        renpy.hide("cowgirl_condom_broken")

    return

# ============================================================
# Cum Outside Freeze (pull out, penis on top, cum layers)
# ============================================================
label CG_CumOutsideFreeze(girl):
    if girl.gid == "shion":
        python:
            store.condom_active = False
            store._cg_force_static = True
            _apply_cum_expression(girl, "cowgirl", "outside")
        call COWGIRL_ApplySpeed(girl, 0) from _call_COWGIRL_ApplySpeed_cum_outside_shion
        python:
            renpy.show("shion scg_penis", tag="scg_penis", at_list=[scg_guy], zorder=10060)
        call _cum_punch_pair("oral") from _call_cum_punch_cg_outside_shion
        python:
            renpy.show("shion scg_penis", tag="scg_penis", at_list=[scg_guy], zorder=10060)
            for _ct in ("scg_cum_ass", "scg_cum_legs", "scg_cum_pussy", "scg_cum_tummy"):
                _ci = "shion %s" % _ct
                if renpy.has_image(_ci, exact=True):
                    renpy.show(_ci, tag=_ct, at_list=_scg_girl_at(), zorder=10003)
        return
    $ _had_condom = store.condom_active
    python:
        store.condom_active = False
        store._cg_force_static = True
        _apply_cum_expression(girl, "cowgirl", "outside")
        store.cowgirl_guy_arms_visible = True

    # Let ApplySpeed handle ALL layers with static transforms (via _cg_force_static)
    call COWGIRL_ApplySpeed(girl, 0) from _call_COWGIRL_ApplySpeed_cum_freeze

    python:
        _pen_img = "%s cowgirl_penis" % girl.gid
        _was_rub = getattr(store, "cowgirl_rub_mode", False)

    if _was_rub:
        # Rub: penis was never inside, just show it on top directly
        python:
            renpy.hide("cowgirl_penis_side")
            renpy.show(_pen_img, tag="cowgirl_penis", at_list=[cowgirl_guy_static], zorder=10060)
    else:
        # Sex/tip: slide penis out (with condom if had one), then back in on top
        python:
            if _had_condom:
                _cb_cimg = _condom_img_tag("cowgirl_condom")
                renpy.show(_cb_cimg, at_list=[cowgirl_penis_slide_out], zorder=9979)
            renpy.show(_pen_img, tag="cowgirl_penis", at_list=[cowgirl_penis_slide_out], zorder=9979)
            renpy.hide("cowgirl_penis_side")
        $ renpy.pause(0.6)
        # Back in without condom, on top of everything
        python:
            renpy.hide("cowgirl_condom")
            renpy.hide("cowgirl_condom_broken")
            renpy.hide("cowgirl_penis")
            renpy.show(_pen_img, tag="cowgirl_penis", at_list=[cowgirl_penis_slide_in], zorder=10060)
        $ renpy.pause(0.6)

    # Override with cum pulse on top
    $ renpy.show("%s cowgirl_penis" % girl.gid, tag="cowgirl_penis", at_list=[cowgirl_penis_cum_pulse()], zorder=10060)

    # Hide cum layers (fresh cum appears after punches)
    python:
        renpy.hide("cowgirl_tummy_cum")
        renpy.hide("cowgirl_penis_cum")
        renpy.hide("cowgirl_dripping_cum")
        renpy.hide("cowgirl_cum_face")

    call _cum_punch_pair("oral") from _call_cum_punch_cg_outside

    # After punches: penis static
    python:
        renpy.hide("cowgirl_penis")
        renpy.show(
            "%s cowgirl_penis" % girl.gid,
            tag="cowgirl_penis",
            at_list=[cowgirl_guy_idle],
            zorder=10060
        )

    return

# ============================================================
# Penis Entry Animation (slide in from below)
# ============================================================
label CG_PenisEnterAnim(girl):
    if girl.gid == "shion":
        python:
            renpy.show("shion scg_penis", tag="scg_penis", at_list=[scg_guy], zorder=9964)
            if store.condom_active:
                renpy.show("shion scg_condom", tag="scg_condom", at_list=[scg_guy], zorder=9965)
        $ renpy.pause(0.3)
        return
    # Hide penis_side first so it doesn't linger
    python:
        renpy.hide("cowgirl_penis_side")
        renpy.hide("cowgirl_penis")
        renpy.hide("cowgirl_condom")
        renpy.hide("cowgirl_condom_broken")
        _pen_img = "%s cowgirl_penis" % girl.gid
        _pen_z = 10060 if store.cowgirl_rub_mode else 9979
        renpy.show(_pen_img, tag="cowgirl_penis", at_list=[cowgirl_penis_slide_in], zorder=_pen_z)
        if store.condom_active:
            _cb_cimg = _condom_img_tag("cowgirl_condom")
            renpy.show(_cb_cimg, at_list=[cowgirl_penis_slide_in], zorder=_pen_z)
    $ renpy.pause(0.55)
    return

# ============================================================
# Condom Remove Animation (slide out with condom, slide back in raw)
# Called AFTER _on_condom_removed already ran (condom layer hidden).
# We re-show the condom image so it slides out visibly.
# ============================================================
label CG_CondomRemoveAnim(girl):
    if girl.gid == "shion":
        $ renpy.hide("scg_condom")
        $ renpy.pause(0.3)
        $ renpy.show("shion scg_penis", tag="scg_penis", at_list=[scg_guy], zorder=9964)
        $ renpy.pause(0.3)
        return
    python:
        _pen_img = "%s cowgirl_penis" % girl.gid
        _pen_z = 10060 if store.cowgirl_rub_mode else 9979
        # Slide penis + condom out together
        _cg_condom_tag = _condom_img_tag("cowgirl_condom")
        renpy.show(_pen_img, tag="cowgirl_penis", at_list=[cowgirl_penis_slide_out], zorder=_pen_z)
        renpy.show(_cg_condom_tag, at_list=[cowgirl_penis_slide_out], zorder=_pen_z)
    $ renpy.pause(0.6)
    # Everything off screen now — hide condom, slide penis back in raw
    python:
        renpy.hide("cowgirl_condom")
        renpy.hide("cowgirl_condom_broken")
        renpy.hide("cowgirl_penis")
        _pen_img = "%s cowgirl_penis" % girl.gid
        _pen_z = 10060 if store.cowgirl_rub_mode else 9979
        renpy.show(_pen_img, tag="cowgirl_penis", at_list=[cowgirl_penis_slide_in], zorder=_pen_z)
    $ renpy.pause(0.6)
    return

# ============================================================
# Creampie Aftermath (static pose before ending)
# ============================================================
label COWGIRL_CreampieAftermath(girl):
    if girl.gid == "shion":
        $ store._cg_force_static = True
        call COWGIRL_ApplySpeed(girl, 0) from _call_COWGIRL_ApplySpeed_creampie_shion
        python:
            renpy.hide("scg_penis")
            renpy.hide("scg_condom")
        return
    # Show static: guy arms forced on, no penis, cum dripping visible
    python:
        store.cowgirl_guy_arms_visible = True
        store._cg_force_static = True

    call COWGIRL_ApplySpeed(girl, 0) from _call_COWGIRL_ApplySpeed_creampie_aftermath

    # Hide penis/condom
    python:
        renpy.hide("cowgirl_penis")
        renpy.hide("cowgirl_penis_side")
        renpy.hide("cowgirl_condom")
        renpy.hide("cowgirl_condom_broken")

    return

# ============================================================
# RUB MODE - Launch
# ============================================================
label COWGIRL_RubLaunch(girl):

    $ public_attention_reset()
    call PlayerExposure(girl) from _call_PlayerExposure_cg_rub

    $ girl._prev_pose = getattr(girl, "default_pose", "standing")
    $ girl._prev_slot = getattr(girl, "SpriteLoc", StageCenter)
    if not getattr(girl, "_saved_outfit", None):
        $ girl.SaveOutfit()

    python:
        store._cowgirl_girl = girl
        store.cowgirl_started = False
        store.cowgirl_rub_mode = True
        store._cg_anim_origin = _time.time()
        if girl.gid == "shion":
            store._scg_girl = girl
            store._scg_arms_variant = 1
            renpy.invoke_in_thread(_scene_cs_blink_loop, girl, "_cowgirl_girl")
            renpy.invoke_in_thread(_scg_expression_cycle, girl)
        else:
            renpy.invoke_in_thread(_scene_blink_loop, girl, "_cowgirl_girl", "cg_blink")
            renpy.invoke_in_thread(_cg_expression_cycle, girl)
        # Clear standing sprite before showing cowgirl pose
        hide_girl_sprite(girl)

    if "cowgirl_speed" not in globals():
        $ cowgirl_speed = 0

    $ sub_event_reset(girl)
    call COWGIRL_ApplySpeed(girl, 0) from _call_COWGIRL_ApplySpeed_rub_launch
    with fade

    if girl.Legs is not None or girl.Panties is not None:
        $ Say_Line(girl, _("Here... let me give you a better view."))

    if girl.Legs is not None:
        pause 0.8
        $ girl.Outfit_Change(legs_down=True, pose="cowgirl")
        call COWGIRL_ApplySpeed(girl, 0) from _call_COWGIRL_ApplySpeed_rub_strip_legs

    if girl.Panties is not None:
        pause 0.15
        menu:
            "Remove panties":
                $ girl.Outfit_Change(panties="none", pose="cowgirl")
                call COWGIRL_ApplySpeed(girl, 0) from _call_COWGIRL_ApplySpeed_rub_strip_pan

            "Pull panties to the side" if _panties_next_state(girl) == "side":
                $ girl.DisplacePanties(pose="cowgirl", refresh=False)
                call COWGIRL_ApplySpeed(girl, 0) from _call_COWGIRL_ApplySpeed_rub_strip_side

            "Pull panties down" if _panties_next_state(girl) == "down":
                $ girl.DisplacePanties(pose="cowgirl", refresh=False)
                call COWGIRL_ApplySpeed(girl, 0) from _call_COWGIRL_ApplySpeed_rub_strip_down

    $ _exp = girl.RegisterAction("player_saw_pussy")
    if _exp["first_time"]:
        call FirstExposureReaction(girl, "pussy") from _call_FirstExposureReaction_cg_rub

    return

# ═══════════════════════════════════════════════════════════
# _cg_esc_dispatch — visual transitions after _escalation_menu
# Handles state vars, condom, visuals, and enters the next menu
# ═══════════════════════════════════════════════════════════
label _cg_esc_dispatch(girl, from_state, current_speed):
    if store._esc_result != "accepted":
        return

    # ── De-escalation ──────────────────────────────────────
    if store._esc_is_deescalation:
        if store._esc_target == "rub":
            python:
                store.cowgirl_rub_mode = True
                store.cowgirl_tip_mode = False
                store.cowgirl_started = False
            call COWGIRL_ApplySpeed(girl, 0) from _call_CG_ApplySpeed_deesc_rub
            call COWGIRL_RubControlMenu(girl) from _call_CG_RubCM_deesc
            return
        elif store._esc_target == "tip":
            $ store.cowgirl_tip_mode = True
            call COWGIRL_ApplySpeed(girl, 1) from _call_CG_ApplySpeed_deesc_tip
            call COWGIRL_TipControlMenu(girl) from _call_CG_TipCM_deesc
            return
        return

    # ── Tip (from rub) ─────────────────────────────────────
    if store._esc_target == "tip":
        if girl.Legs:
            $ girl.Outfit_Change(legs_down=True, pose="cowgirl")
        if girl.Panties:
            $ girl.Outfit_Change(panties="none", pose="cowgirl")
        python:
            store.cowgirl_rub_mode = False
            store.cowgirl_tip_mode = True
            store.cowgirl_started = True
        call CG_PenisEnterAnim(girl) from _call_CG_PenisEnterAnim_esc_tip
        call COWGIRL_ApplySpeed(girl, 1) from _call_CG_ApplySpeed_esc_tip

        if store._esc_was_forced:
            $ Say_Line(girl, _esc_pick_line(girl, _ESC_TIP_FORCE_ACCEPT))
            $ Say_Player(_("It's just the tip, I promise..."))
            $ Say_Line(girl, _tl(renpy.random.choice(_ESC_TIP_FORCE_REACT)))

        call COWGIRL_TipControlMenu(girl) from _call_CG_TipCM_esc_tip
        return

    # ── Sex (from rub or tip) ──────────────────────────────
    if store._esc_target == "sex":
        $ _from_tip = (from_state == "tip")

        if not _from_tip:
            if girl.Legs:
                $ girl.Outfit_Change(legs_down=True, pose="cowgirl")
            if girl.Panties:
                $ girl.Outfit_Change(panties="none", pose="cowgirl")

        python:
            store.cowgirl_rub_mode = False
            store.cowgirl_tip_mode = False
            store._saved_cg_started = store.cowgirl_started
            store.cowgirl_started = False
        call COWGIRL_ApplySpeed(girl, 0) from _call_CG_ApplySpeed_rest_esc_sex

        if store._esc_was_forced:
            if _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False):
                call condom_check(girl, True, "hard_deny") from _call_condom_esc_cg_sex_f_cheat
                if store.condom_denied:
                    $ store.cowgirl_started = store._saved_cg_started
                    call COWGIRL_End(girl, dress_up=False) from _call_CG_End_esc_sex_f_cond
                    call _cheat_no_condom_breakdown(girl) from _call_condom_snap_esc_cg_sex_f
                    return
            else:
                # She refuses raw: decide it NOW, before the act is counted and before a virgin loses it
                if not getattr(store, "_esc_skip_condom", False) and not _force_raw_accepts(girl):
                    call force_raw(girl) from _call_force_raw_esc_cg_sex_pre
                    if store.condom_denied:
                        $ store.cowgirl_started = store._saved_cg_started
                        call COWGIRL_End(girl, dress_up=False) from _call_CG_End_esc_sex_f_deny_pre
                        return
                # Defer force_raw until after visual transition (penis visible during dialogue)
                python:
                    store.condom_active = False
                    store.condom_denied = False
                    store._force_raw_pending = True
        else:
            if _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False):
                call condom_check(girl, True, "hard_deny") from _call_condom_esc_cg_sex_a_cheat
            else:
                $ _pen = store._esc_pen_result
                call condom_check(girl, _pen["condom_required"], _pen["raw_outcome"]) from _call_condom_esc_cg_sex_a
            if store.condom_denied:
                if _is_on_cheat_path(girl):
                    $ store.cowgirl_started = store._saved_cg_started
                    call COWGIRL_End(girl, dress_up=False) from _call_CG_End_esc_sex_a_cond
                    call _cheat_no_condom_breakdown(girl) from _call_condom_snap_esc_cg_sex_a
                    return
                python:
                    store.cowgirl_rub_mode = (from_state == "rub")
                    store.cowgirl_tip_mode = _from_tip
                    store.cowgirl_started = store._saved_cg_started
                call COWGIRL_ApplySpeed(girl, current_speed) from _call_CG_ApplySpeed_esc_sex_cond_deny
                return

        $ store.cowgirl_started = store._saved_cg_started
        if not store.condom_denied:
            $ _scene_escalation(girl, "sex", "cowgirl")
            $ _had_condom_esc = store.condom_active
            python:
                store.cowgirl_rub_mode = False
                store.cowgirl_tip_mode = False
                # Same hole as RCG: from RUB the saved cowgirl_started is False and the
                # success path never set it, so "Switch position..." stayed hidden.
                store.cowgirl_started = True
                print("[CG_ESC] sex from %s: cowgirl_started forced True" % from_state)
            call CG_PenisEnterAnim(girl) from _call_CG_PenisEnterAnim_esc_sex
            if store._esc_virgin_check:
                call virgin_first_time(girl, "cowgirl") from _call_virgin_esc_cg_sex
            $ cowgirl_speed = store._esc_speed
            call COWGIRL_ApplySpeed(girl, cowgirl_speed) from _call_CG_ApplySpeed_esc_sex_go

            # ── Deferred force_raw — penis now visible ──
            if getattr(store, "_force_raw_pending", False):
                $ store._force_raw_pending = False
                call force_raw(girl) from _call_force_raw_esc_cg_sex
                if store.condom_denied:
                    call COWGIRL_End(girl, dress_up=False) from _call_CG_End_esc_sex_f_deny
                    return

            if store._esc_was_forced and not store._esc_virgin_check:
                python:
                    _is_hc = girl.has_trait("hardcore_sex")
                    _is_cute = girl.has_trait("cute_sex")
                    if _from_tip:
                        if _is_hc:
                            _post_lines = [
                                _("You just shoved it all in? Good. Don't hold back."),
                                _("No warning? That's more like it."),
                            ]
                        elif _is_cute:
                            _post_lines = [
                                _("W-wait, you pushed it all in... oh... oh god..."),
                                _("H-hey, that's not just the tip! You didn't even... mmm..."),
                            ]
                        else:
                            _post_lines = [
                                _("You pushed it all in... just like that?"),
                                _("Hold on, you just... you didn't even ask..."),
                            ]
                    else:
                        if _is_hc:
                            _post_lines = [
                                _("Ah! You just... pushed it in... oh god..."),
                                _("Finally! Don't hold back!"),
                            ]
                        elif _is_cute:
                            _post_lines = [
                                _("Ah! You just... pushed it in... oh god..."),
                                _("W-wait! That's not rubbing anymore!"),
                            ]
                        else:
                            _post_lines = [
                                _("Ah! You just... pushed it in... oh god..."),
                                _("Hey! You said... mmm... okay, don't stop."),
                            ]
                $ Say_Line(girl, _tl(renpy.random.choice(_post_lines)))

            call COWGIRL_ControlMenu(girl) from _call_CG_CM_esc_sex
            if not _had_condom_esc and not store._condom_removed_midscene and not getattr(store, "_sub_event_position_switched", False):
                python:
                    _track_raw_sex_start(girl)
        return

    return

# ============================================================
# RUB MODE - Control Menu
# ============================================================
label COWGIRL_RubControlMenu(girl):

    $ store._scene_phase = "rub"
    if "cowgirl_speed" not in globals():
        $ cowgirl_speed = 1

    while True:

        if _scene_should_exit():
            return

        if Round >= 100:
            $ Say_Line(girl, _scene_time_up_line())
            call COWGIRL_End(girl, dress_up=False) from _call_COWGIRL_End_timeout_rub
            return

        menu:
            "Keep going" if cowgirl_speed >= 1:
                $ advance_round(TIME_COSTS["sex_tick"])
                $ add_player_focus(get_player_lust_gain("cowgirl", cowgirl_speed))
                $ _girl_lust_gain(girl, (2 if cowgirl_speed == 1 else 3 if cowgirl_speed == 2 else 5), cowgirl_speed)
                $ _moan = scene_moan_tick(girl, "rub", cowgirl_speed)
                if _moan:
                    call _moan_say(girl, _moan) from _call_ms_cg_rub

                # Path 1: first rub commentary
                if getattr(store, "_path1_rub_first_line_pending", False):
                    $ store._path1_rub_first_line_pending = False
                    $ Say_Line(girl, _cheat_rub_midline(girl))

                # Cheat path breaking point (can fire during rub too)
                if _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False):
                    if _cheat_breaking_point_ready(girl) and renpy.random.random() < 0.30:
                        call _cheat_breaking_point(girl, "cowgirl") from _call_cheat_break_cg_rub

                # Public attention
                $ _pa_caught = public_attention_tick(girl, "keep_going", cowgirl_speed)
                if _pa_caught:
                    if not _caught_keeps_going(girl):
                        call COWGIRL_End(girl, dress_up=False) from _call_COWGIRL_End_rub_pa
                    call caught_in_public(girl, "cowgirl") from _call_caught_public_cg_rub_kg
                    return

                call _sex_interruption_check(girl, "cowgirl") from _call_interrupt_cg_rub
                $ store._witness_expression_lock = False
                if store._sex_interrupted:
                    call COWGIRL_End(girl, dress_up=False) from _call_COWGIRL_End_rub_int
                    return

                call _npc_partner_detection_tick(girl, "cowgirl") from _call_npc_detect_cg_rub
                if store._npc_witness_scene_aborted:
                    call COWGIRL_End(girl, dress_up=False) from _call_COWGIRL_End_rub_npc
                    return

                $ _se = sub_event_tick(girl, "cowgirl")
                if _se:
                    call SubEvent_Handle(girl, "cowgirl", _se) from _call_SubEvent_Handle_cg_rub
                    if store._sub_event_position_switched:
                        $ store._sub_event_position_switched = False
                        return

                call _cheat_bf_call_check(girl, "cowgirl") from _call_cheat_bf_cg_rub

                # Spontaneous escalation: she wants more
                call _girl_escalation_check(girl, "rub") from _call_girl_esc_cg_rub
                if store._girl_esc_accepted:
                    if girl.Legs:
                        $ girl.Outfit_Change(legs_down=True, pose="cowgirl")
                    if girl.Panties:
                        $ girl.Outfit_Change(panties="none", pose="cowgirl")
                    $ store.cowgirl_rub_mode = False
                    $ store.cowgirl_tip_mode = True
                    $ store.cowgirl_started = True
                    call CG_PenisEnterAnim(girl) from _call_CG_PenisEnterAnim_esc_rub_tip2
                    call COWGIRL_ApplySpeed(girl, 1) from _call_COWGIRL_ApplySpeed_esc_rub_tip2
                    call COWGIRL_TipControlMenu(girl) from _call_COWGIRL_TipControlMenu_esc2
                    return

                if girl.Lust >= 100:
                    call GirlCumming(girl, "cowgirl", "cowgirl", scene_override="rub") from _call_GirlCumming_cg_rub
                if player_is_cumming():
                    if focus_overdue_tick():
                        call ForcedCumOverdue(girl, "cowgirl") from _call_ForcedCumOverdue_cg_rub
                        $ _handle_post_cum_exit("cowgirl", "rub")
                        return

            "Speed up" if cowgirl_speed < 3:
                $ advance_round(TIME_COSTS["sex_tick"])
                $ cowgirl_speed += 1
                call COWGIRL_ApplySpeed(girl, cowgirl_speed) from _call_COWGIRL_ApplySpeed_rub_su
                $ add_player_focus(get_player_lust_gain("cowgirl", cowgirl_speed))
                $ _girl_lust_gain(girl, (2 if cowgirl_speed == 1 else 3 if cowgirl_speed == 2 else 5), cowgirl_speed)
                $ Narration(_("You rub faster."))

            "Speed down" if cowgirl_speed > 0:
                $ advance_round(1)
                $ cowgirl_speed -= 1
                call COWGIRL_ApplySpeed(girl, cowgirl_speed) from _call_COWGIRL_ApplySpeed_rub_sd
                $ Narration(_("You slow down."))

            "Slap her face":
                $ advance_round(1)
                call SpankHer(girl, "cowgirl") from _call_SpankHer_cg_rub

            "Strip her" if not getattr(store, "_scene_restricted", False):
                $ advance_round(1)
                call COWGIRL_RubStripMenu(girl) from _call_COWGIRL_RubStripMenu

            "Penetration...":
                call _escalation_menu(girl, "cowgirl") from _call_esc_menu_cg_rub
                if store._esc_result == "accepted":
                    call _cg_esc_dispatch(girl, "rub", cowgirl_speed) from _call_esc_disp_cg_rub
                    return
                elif store._esc_result == "scene_ended":
                    call COWGIRL_End(girl, dress_up=False) from _call_COWGIRL_End_esc_rub
                    return

            "{color=#fbbf24}Cum{/color}" if player_is_cumming():
                call CG_PlayerCumMenu_RubOutside(girl) from _call_CG_PlayerCumMenu_RubOutside_voluntary
                $ _handle_post_cum_exit("cowgirl", "rub")
                return

            "Stop now":
                call _scene_stop_reaction(girl) from _call_stop_react_cg_rub
                if store._stop_accepted:
                    return

# ============================================================
# RUB MODE - Strip Menu
# ============================================================
label COWGIRL_RubStripMenu(girl):
    while True:
        $ _legs_label = _("Remove pants") if _strip_name_for_slot(girl, "skirt") == "pants" else _("Remove skirt")
        menu:
            "[_legs_label]" if girl.Legs:
                call _strip_approval(girl, ["legs"]) from _call__strip_approval_cg_rub_legs
                if store._strip_approved:
                    $ girl.Outfit_Change(legs="none", pose="cowgirl")
                    if _cowgirl_girl == girl:
                        call COWGIRL_ApplySpeed(girl, cowgirl_speed) from _call_COWGIRL_ApplySpeed_rub_strip_legs_2

            "Remove panties" if girl.Panties:
                call _strip_approval(girl, ["panties"]) from _call__strip_approval_cg_rub_panties
                if store._strip_approved:
                    $ girl.Outfit_Change(panties="none", pose="cowgirl")
                    if _cowgirl_girl == girl:
                        call COWGIRL_ApplySpeed(girl, cowgirl_speed) from _call_COWGIRL_ApplySpeed_rub_strip_panties

            "Remove top" if girl.Over:
                call _strip_approval(girl, ["over"]) from _call__strip_approval_cg_rub_over
                if store._strip_approved:
                    $ girl.Outfit_Change(over="none", pose="cowgirl")
                    if _cowgirl_girl == girl:
                        call COWGIRL_ApplySpeed(girl, cowgirl_speed) from _call_COWGIRL_ApplySpeed_rub_strip_over

            "Pull chest up" if girl.Chest and girl.clothes_state.get("chest") != "up" and _item_has_state(girl, "chest", "up"):
                call _strip_approval(girl, ["chest"]) from _call__strip_approval_cg_rub_chest_up
                if store._strip_approved:
                    $ girl.Outfit_Change(chest_up=True, pose="cowgirl")
                    if _cowgirl_girl == girl:
                        call COWGIRL_ApplySpeed(girl, cowgirl_speed) from _call_COWGIRL_ApplySpeed_rub_strip_chest_up

            "Remove chest" if girl.Chest:
                call _strip_approval(girl, _get_strip_slots(girl, "chest")) from _call__strip_approval_cg_rub_chest
                if store._strip_approved:
                    $ _do_strip_change(girl, "chest", "cowgirl")
                    if _cowgirl_girl == girl:
                        call COWGIRL_ApplySpeed(girl, cowgirl_speed) from _call_COWGIRL_ApplySpeed_rub_strip_chest

            "Back":
                return

# ============================================================
# JUST THE TIP - Launch
# ============================================================
label COWGIRL_TipLaunch(girl):

    $ public_attention_reset()
    call PlayerExposure(girl) from _call_PlayerExposure_cg_tip

    $ girl._prev_pose = getattr(girl, "default_pose", "standing")
    $ girl._prev_slot = getattr(girl, "SpriteLoc", StageCenter)
    if not getattr(girl, "_saved_outfit", None):
        $ girl.SaveOutfit()

    python:
        store._cowgirl_girl = girl
        store.cowgirl_started = True
        store.cowgirl_tip_mode = True
        store._cg_anim_origin = _time.time()
        # her standing sprite goes for every girl (COWGIRL_Launch): layers with tags of their own never replace it
        hide_girl_sprite(girl)
        sprite_state.setdefault(girl.Id, {})["pose"] = "cowgirl"
        if girl.gid == "shion":
            store._scg_girl = girl
            store._scg_arms_variant = 1
            renpy.invoke_in_thread(_scene_cs_blink_loop, girl, "_cowgirl_girl")
            renpy.invoke_in_thread(_scg_expression_cycle, girl)
        else:
            renpy.invoke_in_thread(_scene_blink_loop, girl, "_cowgirl_girl", "cg_blink")
            renpy.invoke_in_thread(_cg_expression_cycle, girl)

    $ cowgirl_speed = 1

    if girl.Legs:
        $ girl.Outfit_Change(legs_down=True, pose="cowgirl")
    if girl.Panties:
        $ girl.Outfit_Change(panties="none", pose="cowgirl")

    $ sub_event_reset(girl)
    call COWGIRL_ApplySpeed(girl, 1) from _call_COWGIRL_ApplySpeed_tip_launch
    with fade

    return

# ============================================================
# JUST THE TIP - Control Menu (locked at speed 1)
# ============================================================
label COWGIRL_TipControlMenu(girl):

    $ store._scene_phase = "tip"
    $ store._cheat_shower_max_act = "tip"
    $ cowgirl_speed = 1

    while True:

        if _scene_should_exit():
            return

        if Round >= 100:
            $ Say_Line(girl, _scene_time_up_line())
            call COWGIRL_End(girl, dress_up=False) from _call_COWGIRL_End_timeout_tip
            return

        $ debug_log("[DEBUG] CG_TipControlMenu loop: path=%s stage=%s tip_just=%s can_sex=%s" % (getattr(girl, "_cheat_escalation_path", 0), getattr(girl, "_cheat_sex_stage", 0), getattr(store, "_cheat_tip_just_done", False), _cheat_can_sex(girl) if _is_on_cheat_path(girl) else "N/A"))

        menu:
            "Keep going":
                $ advance_round(TIME_COSTS["sex_tick"])
                $ add_player_focus(get_player_lust_gain("cowgirl", 1))
                $ _girl_lust_gain(girl, 2, 1)
                $ _moan = scene_moan_tick(girl, "cowgirl", 1)
                if _moan:
                    call _moan_say(girl, _moan) from _call_ms_cg_sex

                # Path 1: first tip commentary
                if getattr(store, "_path1_tip_first_line_pending", False):
                    $ store._path1_tip_first_line_pending = False
                    $ Say_Line(girl, _cheat_tip_midline(girl))

                # Cheat path breaking point (can fire during tip too)
                if _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False):
                    if _cheat_breaking_point_ready(girl) and renpy.random.random() < 0.30:
                        call _cheat_breaking_point(girl, "cowgirl") from _call_cheat_break_cg_tip

                $ _pa_caught = public_attention_tick(girl, "keep_going", 1)
                if _pa_caught:
                    if not _caught_keeps_going(girl):
                        call COWGIRL_End(girl, dress_up=False) from _call_COWGIRL_End_tip_pa
                    call caught_in_public(girl, "cowgirl") from _call_caught_public_cg_tip_kg
                    return

                call _sex_interruption_check(girl, "cowgirl") from _call_interrupt_cg_tip
                $ store._witness_expression_lock = False
                if store._sex_interrupted:
                    call COWGIRL_End(girl, dress_up=False) from _call_COWGIRL_End_tip_int
                    return

                call _npc_partner_detection_tick(girl, "cowgirl") from _call_npc_detect_cg_tip
                if store._npc_witness_scene_aborted:
                    call COWGIRL_End(girl, dress_up=False) from _call_COWGIRL_End_tip_npc
                    return

                $ _se = sub_event_tick(girl, "cowgirl")
                if _se:
                    call SubEvent_Handle(girl, "cowgirl", _se) from _call_SubEvent_Handle_cg_tip
                    if store._sub_event_position_switched:
                        $ store._sub_event_position_switched = False
                        return

                call _cheat_bf_call_check(girl, "cowgirl") from _call_cheat_bf_cg_tip

                # Spontaneous escalation: she wants all the way
                call _girl_escalation_check(girl, "tip") from _call_girl_esc_cg_tip
                if store._girl_esc_accepted:
                    $ store.cowgirl_tip_mode = False
                    call _girl_esc_accept_sex(girl, "cowgirl") from _call_girl_esc_accept_cg
                    if store._girl_esc_condom_denied:
                        call COWGIRL_End(girl, dress_up=False) from _call_COWGIRL_End_esc_condom
                        call _cheat_no_condom_breakdown(girl) from _call_condom_snap_cg_esc2
                        return
                    $ cowgirl_speed = 3
                    call COWGIRL_ApplySpeed(girl, 3) from _call_COWGIRL_ApplySpeed_esc_tip_fuck2
                    call COWGIRL_ControlMenu(girl) from _call_COWGIRL_ControlMenu_esc2
                    return

                if girl.Lust >= 100:
                    call GirlCumming(girl, "cowgirl", "cowgirl", scene_override="tip") from _call_GirlCumming_cg_tip
                if player_is_cumming():
                    if focus_overdue_tick():
                        call ForcedCumOverdue(girl, "cowgirl") from _call_ForcedCumOverdue_cg_tip
                        $ _handle_post_cum_exit("cowgirl", "tip")
                        return

            "Slap her face":
                $ advance_round(1)
                call SpankHer(girl, "cowgirl") from _call_SpankHer_cg_tip

            "Strip her" if not getattr(store, "_scene_restricted", False):
                $ advance_round(1)
                call COWGIRL_StripMenu(girl) from _call_COWGIRL_StripMenu_tip

            "Penetration...":
                call _escalation_menu(girl, "cowgirl") from _call_esc_menu_cg_tip
                if store._esc_result == "accepted":
                    call _cg_esc_dispatch(girl, "tip", cowgirl_speed) from _call_esc_disp_cg_tip
                    return
                elif store._esc_result == "scene_ended":
                    call COWGIRL_End(girl, dress_up=False) from _call_COWGIRL_End_esc_tip
                    return

            "{color=#fbbf24}Cum{/color}" if player_is_cumming():
                call CG_PlayerCumMenu_TipOutside(girl) from _call_CG_PlayerCumMenu_TipOutside_voluntary
                $ _handle_post_cum_exit("cowgirl", "tip")
                return

            "Stop now":
                call _scene_stop_reaction(girl) from _call_stop_react_cg_tip
                if store._stop_accepted:
                    return

# ============================================================
# Rub - Cum Menu (cowgirl)
# ============================================================
label CG_PlayerCumMenu_RubOutside(girl):

    "You feel yourself getting close..."

    menu:
        "Fire away":
            call CG_CumOutsideFreeze(girl) from _call_CG_CumOutsideFreeze_rub_fire
            "You cum."
            $ process_cum(girl, "cowgirl", "away")
            $ apply_cum_bonuses(girl, "cum_outside")

        "Cum outside":
            $ _cg_cum_type = "body"
            menu:
                "On her face":
                    $ _cg_cum_type = "face"
                "On her legs":
                    $ _cg_cum_type = "legs"
                "On her tummy":
                    $ _cg_cum_type = "body"
                "All over her":
                    $ _cg_cum_type = "all"

            call CG_CumOutsideFreeze(girl) from _call_CG_CumOutsideFreeze_rub_out

            if _cg_cum_type == "face":
                "You cum on her face."
                $ process_cum(girl, "cowgirl", "face")
            elif _cg_cum_type == "legs":
                "You cum on her legs."
                $ process_cum(girl, "cowgirl", "outside", ["legs"])
            elif _cg_cum_type == "body":
                "You cum on her tummy."
                $ process_cum(girl, "cowgirl", "outside")
            else:
                "You cum all over her."
                $ process_cum(girl, "cowgirl", "outside", ["body", "legs", "face"])

            python:
                if girl.gid != "shion":
                    renpy.show("%s cowgirl_tummy_cum" % girl.gid, tag="cowgirl_tummy_cum", at_list=[cowgirl_slot_static], zorder=9988)
                    renpy.show("%s cowgirl_penis_cum" % girl.gid, tag="cowgirl_penis_cum", at_list=[cowgirl_guy_idle], zorder=9978)
                    renpy.show("%s cowgirl_cum_face" % girl.gid, tag="cowgirl_cum_face", at_list=[cowgirl_slot_static], zorder=9992)
                renpy.restart_interaction()
            $ apply_cum_bonuses(girl, "cum_outside")
            $ _cum_say_line(girl, "outside", "cowgirl")

    return

# ============================================================
# CG_TipDeniedCumVisual — outside cum sprites on denied creampie
# ============================================================
label CG_TipDeniedCumVisual(girl):
    if girl.gid == "shion":
        python:
            for _ct in ("scg_cum_ass", "scg_cum_legs", "scg_cum_pussy", "scg_cum_tummy"):
                _ci = "shion %s" % _ct
                if renpy.has_image(_ci, exact=True):
                    renpy.show(_ci, tag=_ct, at_list=_scg_girl_at(), zorder=10003)
            renpy.restart_interaction()
        return
    python:
        renpy.show("%s cowgirl_tummy_cum" % girl.gid, tag="cowgirl_tummy_cum", at_list=[cowgirl_slot_static], zorder=9988)
        renpy.show("%s cowgirl_cum_face" % girl.gid, tag="cowgirl_cum_face", at_list=[cowgirl_slot_static], zorder=9992)
        renpy.restart_interaction()
    return

# ============================================================
# Just The Tip - Cum Menu (cowgirl)
# ============================================================
label CG_PlayerCumMenu_TipOutside(girl):

    "You feel yourself getting close..."

    menu:
        "Fire away":
            call CG_CumOutsideFreeze(girl) from _call_CG_CumOutsideFreeze_tip_fire
            "You pull out and cum."
            $ process_cum(girl, "cowgirl", "away")
            $ apply_cum_bonuses(girl, "cum_outside")

        "Cum outside":
            $ _cg_cum_type = "body"
            menu:
                "On her face":
                    $ _cg_cum_type = "face"
                "On her legs":
                    $ _cg_cum_type = "legs"
                "On her tummy":
                    $ _cg_cum_type = "body"
                "All over her":
                    $ _cg_cum_type = "all"

            call CG_CumOutsideFreeze(girl) from _call_CG_CumOutsideFreeze_tip_out

            if _cg_cum_type == "face":
                "You pull out and cum on her face."
                $ process_cum(girl, "cowgirl", "face")
            elif _cg_cum_type == "legs":
                "You pull out and cum on her legs."
                $ process_cum(girl, "cowgirl", "outside", ["legs"])
            elif _cg_cum_type == "body":
                "You pull out and cum on her tummy."
                $ process_cum(girl, "cowgirl", "outside")
            else:
                "You pull out and cum all over her."
                $ process_cum(girl, "cowgirl", "outside", ["body", "legs", "face"])

            python:
                if girl.gid != "shion":
                    renpy.show("%s cowgirl_tummy_cum" % girl.gid, tag="cowgirl_tummy_cum", at_list=[cowgirl_slot_static], zorder=9988)
                    renpy.show("%s cowgirl_penis_cum" % girl.gid, tag="cowgirl_penis_cum", at_list=[cowgirl_guy_idle], zorder=9978)
                    renpy.show("%s cowgirl_cum_face" % girl.gid, tag="cowgirl_cum_face", at_list=[cowgirl_slot_static], zorder=9992)
                renpy.restart_interaction()
            $ apply_cum_bonuses(girl, "cum_outside")
            $ _cum_say_line(girl, "outside", "cowgirl")

        "Ask to cum in her mouth":
            $ _cum_check = CumPermissionCheck(girl, "cum_in_mouth_ask")
            if _cum_check["accepted"]:
                $ Say_Line(girl, scene_pick_line("cum_mouth_accepted", scene="cowgirl", girl=girl) or "Go ahead... do it.")
                call _cum_in_mouth_via_bj(girl, "cowgirl") from _call__cum_in_mouth_via_bj_cg_tip
            else:
                $ Say_Line(girl, scene_pick_line("cum_mouth_denied", scene="cowgirl", girl=girl) or "No way... not in my mouth.")
                call CG_CumOutsideFreeze(girl) from _call_CG_CumOutsideFreeze_tip_mouth_denied
                "You pull out and cum on her."
                $ process_cum(girl, "cowgirl", "outside")
                python:
                    if girl.gid != "shion":
                        renpy.show("%s cowgirl_tummy_cum" % girl.gid, tag="cowgirl_tummy_cum", at_list=[cowgirl_slot_static], zorder=9988)
                        renpy.show("%s cowgirl_cum_face" % girl.gid, tag="cowgirl_cum_face", at_list=[cowgirl_slot_static], zorder=9992)
                    renpy.restart_interaction()
                $ apply_cum_bonuses(girl, "cum_outside")

        "Ask to cum inside":
            call _tip_ask_cum_inside(girl, "cowgirl") from _call_tip_ask_cg

        "Cum inside her":
            call _tip_force_cum_inside(girl, "cowgirl") from _call_tip_force_cg

    return


# (Old _cowgirl_escalation_check removed — now uses centralized _girl_escalation_check)

# ============================================================
# MASTURBATION SCENE
# Same cowgirl layers / Y — body static, hand rotation only.
# ============================================================

# ── Apply speed (masturbation variant) ──
label MASTURBATE_ApplySpeed(girl, speed=0):
    $ print("[MAST_AS] ENTER gid=%s mast_pose=%s speed=%d" % (girl.gid, getattr(girl, "mast_pose", "MISSING"), speed))
    if getattr(girl, "mast_pose", "cowgirl") == "laying_down":
        $ print("[MAST_AS] REDIRECT to LD_MASTURBATE_ApplySpeed")
        call LD_MASTURBATE_ApplySpeed(girl, speed) from _call_LD_MAST_AS_redir
        return
    if getattr(girl, "mast_pose", "cowgirl") == "doggy":
        $ print("[MAST_AS] REDIRECT to DG_MASTURBATE_ApplySpeed")
        call DG_MASTURBATE_ApplySpeed(girl, speed) from _call_DG_MAST_AS_redir
        return

    $ print("[MAST_AS] COWGIRL PATH for gid=%s" % girl.gid)
    python:
        # Only activate masturbation arms/hand at speed >= 1
        store.cowgirl_masturbating = (speed >= 1)

        # Auto-displace panties at speed >= 1 (only if still full)
        if speed >= 1 and getattr(girl, "Panties", None) and girl.clothes_state.get("panties") == "full":
            girl.DisplacePanties(pose="cowgirl", refresh=False)

        _mast_sep = _gsc(girl.gid, "mast_arm_separate", False, "cowgirl")
        debug_log("[MAST_APPLY] gid=%s speed=%d oral=%s mast_sep=%s" % (girl.gid, speed, getattr(store, "_oral_active", False), _mast_sep))

        attrs = _build_cowgirl_attributes(girl)
        if getattr(store, "hiding_face", False):
            _hide_attrs = []
            for _a in attrs:
                if _a.startswith("eyes_"):
                    _hide_attrs.append("eyes_closed")
                elif _a.startswith("arms_high_") and _a != "arms_high_none":
                    _hide_attrs.append("arms_high_none")
                elif _a.startswith("arms_low_") and _a != "arms_low_none":
                    _hide_attrs.append("arms_low_none")
                elif _a == "shoulder_left_on":
                    _hide_attrs.append("shoulder_left_none")
                elif _a.startswith("masturbate_"):
                    _hide_attrs.append("masturbate_hand_none")
                else:
                    _hide_attrs.append(_a)
            attrs = _hide_attrs
            state = sprite_state.setdefault(girl.Id, {})
            state["eyes"] = "eyes_closed"

        img_name = "%s cowgirl" % girl.gid
        if attrs:
            img_name += " " + " ".join(attrs)

        # -- Girl layers — all static (no bounce) --
        renpy.show(
            img_name,
            tag=girl.gid,
            at_list=[cowgirl_slot_static],
            zorder=9980
        )

        # -- Hide arm layers (girl covering face during recording) --
        _CG_MAST_HIDE_ARM_Z = {"hide_arm_left_2": 9977, "hide_arm_left_1": 9995}
        if getattr(store, "hiding_face", False):
            for _ha_suffix, _ha_z in _CG_MAST_HIDE_ARM_Z.items():
                _ha_img = "%s cowgirl_%s" % (girl.gid, _ha_suffix)
                _ha_tag = "cowgirl_%s" % _ha_suffix
                if renpy.has_image(_ha_img):
                    renpy.show(_ha_img, tag=_ha_tag, at_list=[cowgirl_slot_static], zorder=_ha_z)
                else:
                    renpy.hide(_ha_tag)
        else:
            for _ha_suffix in _CG_MAST_HIDE_ARM_Z:
                renpy.hide("cowgirl_%s" % _ha_suffix)

        renpy.show(
            "%s cowgirl_legs_bottom" % girl.gid,
            tag="cowgirl_legs_bottom",
            at_list=[cowgirl_slot_static],
            zorder=9965
        )

        _m_pan_item = getattr(girl, "Panties", None)
        if _m_pan_item and girl.PantiesSide:
            if _m_pan_item == "bikini_panties":
                _m_psb_img = "%s cowgirl_bikini_panties_side_bottom" % girl.gid
            else:
                _m_psb_img = "%s cowgirl_panties_side_bottom" % girl.gid
            if renpy.has_image(_m_psb_img):
                renpy.show(_m_psb_img, tag="cowgirl_panties_side_bottom", at_list=[cowgirl_slot_static], zorder=9978)
            else:
                renpy.hide("cowgirl_panties_side_bottom")
        else:
            renpy.hide("cowgirl_panties_side_bottom")

        # Chest / boobs (static) — z-orders from GIRL_SCENE_CONFIG
        _m_corset_z = _gsc(girl.gid, "mast_corset_z", 9985, "cowgirl")
        _m_boobs_cl_z = _gsc(girl.gid, "mast_boobs_clothed_z", 9982, "cowgirl")
        _m_nips_cl_z = _gsc(girl.gid, "mast_nipples_clothed_z", 9983, "cowgirl")
        _m_boobs_z = _gsc(girl.gid, "mast_boobs_z", 9986, "cowgirl")
        _m_nipples_z = _gsc(girl.gid, "mast_nipples_z", 9987, "cowgirl")
        _m_chest_z = _gsc(girl.gid, "mast_chest_z", 9988, "cowgirl")
        debug_log("[MAST_APPLY] gid=%s chest_z=%d boobs_z=%d nipples_z=%d" % (girl.gid, _m_corset_z, _m_boobs_z, _m_nipples_z))
        _m_chest_item = girl.Chest
        _m_chest_cfg = CLOTHING_REGISTRY.get(girl.gid, {}).get(_m_chest_item, {}) if _m_chest_item else {}
        _m_chest_has_cg = "cowgirl" in _m_chest_cfg.get("poses", {})

        if _m_chest_item == "corset" and _m_chest_has_cg and not girl.ChestUp:
            renpy.show("%s cowgirl_corset" % girl.gid, tag="cowgirl_corset", at_list=[cowgirl_boobs_static], zorder=_m_corset_z)
            renpy.show("%s cowgirl_corset_up" % girl.gid, tag="cowgirl_corset_up", at_list=[cowgirl_slot_static], zorder=9984)
            renpy.hide("cowgirl_chest_top")
            renpy.show("%s cowgirl_boobs_naked" % girl.gid, tag="cowgirl_boobs", at_list=[cowgirl_boobs_static], zorder=_m_boobs_cl_z)
            renpy.show("%s cowgirl_nipples" % girl.gid, tag="cowgirl_nipples", at_list=[cowgirl_boobs_static], zorder=_m_nips_cl_z)
        elif _m_chest_item == "corset" and _m_chest_has_cg and girl.ChestUp:
            renpy.hide("cowgirl_corset")
            renpy.show("%s cowgirl_corset_up" % girl.gid, tag="cowgirl_corset_up", at_list=[cowgirl_slot_static], zorder=9985)
            renpy.hide("cowgirl_chest_top")
            renpy.show("%s cowgirl_boobs_naked" % girl.gid, tag="cowgirl_boobs", at_list=[cowgirl_boobs_static], zorder=_m_boobs_z)
            renpy.show("%s cowgirl_nipples" % girl.gid, tag="cowgirl_nipples", at_list=[cowgirl_boobs_static], zorder=_m_nipples_z)
        elif _m_chest_has_cg and not girl.ChestUp:
            _m_ct_img = "%s cowgirl_%s" % (girl.gid, _m_chest_item)
            _m_ct_fixed_img = "%s cowgirl_%s_fixed" % (girl.gid, _m_chest_item)
            _m_ct_fixed_z = _m_corset_z - 1
            renpy.hide("cowgirl_corset")
            renpy.hide("cowgirl_corset_up")
            if renpy.has_image(_m_ct_img):
                renpy.show(_m_ct_img, tag="cowgirl_chest_top", at_list=[cowgirl_boobs_static], zorder=_m_corset_z)
            else:
                renpy.hide("cowgirl_chest_top")
            if renpy.has_image(_m_ct_fixed_img):
                renpy.show(_m_ct_fixed_img, tag="cowgirl_chest_fixed", at_list=[cowgirl_slot_static], zorder=_m_ct_fixed_z)
            else:
                renpy.hide("cowgirl_chest_fixed")
            renpy.show("%s cowgirl_boobs_naked" % girl.gid, tag="cowgirl_boobs", at_list=[cowgirl_boobs_static], zorder=_m_boobs_cl_z)
            renpy.show("%s cowgirl_nipples" % girl.gid, tag="cowgirl_nipples", at_list=[cowgirl_boobs_static], zorder=_m_nips_cl_z)
        elif _m_chest_has_cg and girl.ChestUp:
            _m_ct_up_img = "%s cowgirl_%s_up" % (girl.gid, _m_chest_item)
            _m_ct_fixed_img = "%s cowgirl_%s_fixed" % (girl.gid, _m_chest_item)
            _m_ct_fixed_z = _m_boobs_z - 1
            renpy.hide("cowgirl_corset")
            renpy.hide("cowgirl_corset_up")
            if renpy.has_image(_m_ct_fixed_img):
                renpy.show(_m_ct_fixed_img, tag="cowgirl_chest_fixed", at_list=[cowgirl_slot_static], zorder=_m_ct_fixed_z)
            else:
                renpy.hide("cowgirl_chest_fixed")
            renpy.show("%s cowgirl_boobs_naked" % girl.gid, tag="cowgirl_boobs", at_list=[cowgirl_boobs_static], zorder=_m_boobs_z)
            renpy.show("%s cowgirl_nipples" % girl.gid, tag="cowgirl_nipples", at_list=[cowgirl_boobs_static], zorder=_m_nipples_z)
            if renpy.has_image(_m_ct_up_img):
                renpy.show(_m_ct_up_img, tag="cowgirl_chest_top", at_list=[cowgirl_boobs_static], zorder=_m_chest_z)
            else:
                renpy.hide("cowgirl_chest_top")
        else:
            renpy.hide("cowgirl_corset")
            renpy.hide("cowgirl_corset_up")
            renpy.hide("cowgirl_chest_top")
            renpy.hide("cowgirl_chest_fixed")
            renpy.show("%s cowgirl_boobs_naked" % girl.gid, tag="cowgirl_boobs", at_list=[cowgirl_boobs_static], zorder=_m_boobs_z)
            renpy.show("%s cowgirl_nipples" % girl.gid, tag="cowgirl_nipples", at_list=[cowgirl_boobs_static], zorder=_m_nipples_z)

        renpy.hide("cowgirl_guy")

        # No penis in masturbation scene
        renpy.hide("cowgirl_penis")
        renpy.hide("cowgirl_penis_side")

        # Arm + hand OR tongue: depends on oral mode
        if speed >= 1:
            if getattr(store, "_oral_active", False):
                debug_log("[MAST_APPLY] path=ORAL: showing tongue+pussy, hiding arm/hand")
                renpy.hide("cowgirl_masturbate_arm")
                renpy.hide("cowgirl_masturbate_hand")
                _tongue_img = "player_tongue_s%d" % min(speed, 3)
                _tongue_tf = globals().get("mast_tongue_pos_%s" % girl.gid, mast_tongue_pos_gwen)
                renpy.show(_tongue_img, tag="mast_tongue", at_list=[_tongue_tf], zorder=9987)
                renpy.show("%s cowgirl_pussy" % girl.gid, tag="mast_pussy", at_list=[cowgirl_slot_static], zorder=9988)
            elif _mast_sep:
                debug_log("[MAST_APPLY] path=HANDS_SEPARATE: hiding_face=%s" % getattr(store, "hiding_face", False))
                renpy.hide("mast_tongue")
                renpy.hide("mast_pussy")
                if getattr(store, "hiding_face", False):
                    arm_img = "%s cowgirl_hide_arm_masturbate_right" % girl.gid
                else:
                    _ls_img = "%s cowgirl_masturbate_arm_ls" % girl.gid
                    if girl.Over and renpy.has_image(_ls_img, exact=True):
                        arm_img = _ls_img
                    else:
                        arm_img = "%s cowgirl_masturbate_arm" % girl.gid
                renpy.show(arm_img, tag="cowgirl_masturbate_arm", at_list=[cowgirl_slot_static], zorder=9986)
                renpy.show(
                    "%s cowgirl_masturbate_hand" % girl.gid,
                    tag="cowgirl_masturbate_hand",
                    at_list=[cowgirl_hand_masturbate],
                    zorder=9987
                )
            else:
                debug_log("[MAST_APPLY] path=HANDS_LAYERED: hiding_face=%s" % getattr(store, "hiding_face", False))
                renpy.hide("mast_tongue")
                renpy.hide("mast_pussy")
                if getattr(store, "hiding_face", False):
                    renpy.show(
                        "%s cowgirl_hide_arm_masturbate_right" % girl.gid,
                        tag="cowgirl_masturbate_arm",
                        at_list=[cowgirl_slot_static],
                        zorder=9986
                    )
                    renpy.show(
                        "%s cowgirl_masturbate_hand" % girl.gid,
                        tag="cowgirl_masturbate_hand",
                        at_list=[cowgirl_hand_masturbate],
                        zorder=9987
                    )
        else:
            renpy.hide("cowgirl_masturbate_arm")
            renpy.hide("cowgirl_masturbate_hand")
            renpy.hide("mast_tongue")
            renpy.hide("mast_pussy")

    return

# ── Launch ──
label ORAL_Launch(girl):
    # Cunnilingus = the masturbate pose in oral mode (start_scene "oral" comes through here)
    $ store._oral_active = True
    call MASTURBATE_Launch(girl) from _call_MASTURBATE_Launch_oral_orch
    $ store._scene_phase = "oral"
    return

label MASTURBATE_Launch(girl):
    $ print("[MAST_LAUNCH] ENTER gid=%s mast_pose=%s" % (girl.gid, getattr(girl, "mast_pose", "MISSING")))
    if getattr(girl, "mast_pose", "cowgirl") == "laying_down":
        $ print("[MAST_LAUNCH] REDIRECT to LD")
        call LD_MASTURBATE_Launch(girl) from _call_LD_MAST_Launch_redir
        return
    if getattr(girl, "mast_pose", "cowgirl") == "doggy":
        $ print("[MAST_LAUNCH] REDIRECT to DG")
        call DG_MASTURBATE_Launch(girl) from _call_DG_MAST_Launch_redir
        return
    $ print("[MAST_LAUNCH] COWGIRL PATH")
    $ _kill_scene_threads()
    $ _hide_all_scene_layers(girl)

    $ girl._prev_pose = getattr(girl, "default_pose", "standing")
    $ girl._prev_slot = getattr(girl, "SpriteLoc", StageCenter)
    if not getattr(girl, "_saved_outfit", None):
        $ girl.SaveOutfit()

    python:
        store._cowgirl_girl = girl
        store.cowgirl_started = False
        store.cowgirl_masturbating = False
        store._oral_active = getattr(store, "_oral_active", False)
        store.cowgirl_arms_pose = 2
        store.cowgirl_guy_arms_visible = False
        store._cg_anim_origin = _time.time()
        store._cg_force_static = True
        sprite_state.setdefault(girl.Id, {})["pose"] = "cowgirl"
        renpy.invoke_in_thread(_scene_blink_loop, girl, "_cowgirl_girl", "cg_blink")
        renpy.invoke_in_thread(_cg_expression_cycle, girl)

    if "cowgirl_speed" not in globals():
        $ cowgirl_speed = 0

    call MASTURBATE_ApplySpeed(girl, 0) from _call_MASTURBATE_ApplySpeed_1
    with fade

    if girl.Legs is not None or girl.Panties is not None:
        $ Say_Line(girl, _("Here... let me give you a better view."))

    # --- BOTTOM (skirt pulled up > panties > bare) ---
    if girl.Legs is not None:
        pause 0.8
        $ girl.Outfit_Change(legs_down=True, pose="cowgirl")
        call MASTURBATE_ApplySpeed(girl, cowgirl_speed) from _call_MASTURBATE_ApplySpeed_2

    if girl.Panties is not None:
        pause 0.15
        menu:
            "Remove panties":
                $ girl.Outfit_Change(panties="none", pose="cowgirl")
                call MASTURBATE_ApplySpeed(girl, cowgirl_speed) from _call_MASTURBATE_ApplySpeed_3

            "Pull panties to the side" if _item_has_state(girl, "panties", "side"):
                $ girl.clothes_state["panties"] = "side"
                call MASTURBATE_ApplySpeed(girl, cowgirl_speed) from _call_MASTURBATE_ApplySpeed_4

            "Pull panties down" if _item_has_state(girl, "panties", "down"):
                $ girl.clothes_state["panties"] = "down"
                call MASTURBATE_ApplySpeed(girl, cowgirl_speed) from _call_MASTURBATE_ApplySpeed_4b

    # Register exposure after strip (both options count as seeing pussy)
    $ _exp = girl.RegisterAction("player_saw_pussy")
    if _exp["first_time"]:
        call FirstExposureReaction(girl, "pussy") from _call_FirstExposureReaction_7

    return

# ── Launch (caught variant — no strip, no dialogue, no exposure) ──
label MASTURBATE_Launch_Caught(girl):
    if getattr(girl, "mast_pose", "cowgirl") == "laying_down":
        call LD_MASTURBATE_Launch_Caught(girl) from _call_LD_MAST_LC_redir
        return
    if getattr(girl, "mast_pose", "cowgirl") == "doggy":
        call DG_MASTURBATE_Launch_Caught(girl) from _call_DG_MAST_LC_redir
        return

    $ girl._prev_pose = getattr(girl, "default_pose", "standing")
    $ girl._prev_slot = getattr(girl, "SpriteLoc", StageCenter)
    if not getattr(girl, "_saved_outfit", None):
        $ girl.SaveOutfit()

    python:
        store._cowgirl_girl = girl
        store.cowgirl_started = False
        store.cowgirl_masturbating = False
        store._oral_active = False
        store.cowgirl_arms_pose = 2
        store.cowgirl_guy_arms_visible = False
        store._cg_anim_origin = _time.time()
        renpy.invoke_in_thread(_scene_blink_loop, girl, "_cowgirl_girl", "cg_blink")
        renpy.invoke_in_thread(_cg_expression_cycle, girl)

    call MASTURBATE_ApplySpeed(girl, cowgirl_speed) from _call_MASTURBATE_ApplySpeed_5

    $ renpy.hide("cowgirl_guy")

    with fade

    return

# ── Control Menu ──
label MASTURBATE_ControlMenu(girl):
    if getattr(girl, "mast_pose", "cowgirl") == "laying_down":
        call LD_MASTURBATE_ControlMenu(girl) from _call_LD_MAST_CM_redir
        return
    if getattr(girl, "mast_pose", "cowgirl") == "doggy":
        call DG_MASTURBATE_ControlMenu(girl) from _call_DG_MAST_CM_redir
        return

    $ store._scene_phase = "masturbate"
    if "cowgirl_speed" not in globals():
        $ cowgirl_speed = 0
    $ store._mast_stop_asked = 0
    $ store._mast_sex_asks = 0

    while True:

        if Round >= 100:
            $ Say_Line(girl, _scene_time_up_line())
            call COWGIRL_End(girl, dress_up=False) from _call_COWGIRL_End_timeout_mast
            return

        menu:
            "Keep going" if cowgirl_speed >= 1:
                $ advance_round(TIME_COSTS["sex_tick"])
                python:
                    _mast_phase = "oral" if getattr(store, "_oral_active", False) else "masturbate"
                    if _mast_phase == "oral":
                        _mast_lust = 4 if cowgirl_speed == 1 else 7 if cowgirl_speed == 2 else 10
                    else:
                        _mast_lust = 2 if cowgirl_speed == 1 else 4 if cowgirl_speed == 2 else 6
                $ _girl_lust_gain(girl, _mast_lust, cowgirl_speed)
                $ _moan = scene_moan_tick(girl, _mast_phase, cowgirl_speed)
                if _moan:
                    call _moan_say(girl, _moan) from _call_ms_cg_mast
                if girl.Lust >= 100:
                    call GirlCumming(girl, _mast_phase, "cowgirl") from _call_GirlCumming_6

                # --- Sex escalation: girl asks for the real thing (up to 3 times) ---
                python:
                    _flags = getattr(girl, "intimacy_flags", set()) or set()
                    _has_sex_history = bool(_flags & {"sex", "bj", "hj", "tj"})
                    _is_lesbian = girl.has_trait("lesbian")
                    _msa = getattr(store, "_mast_sex_asks", 0)
                    _escalate_chance = 0
                    if getattr(store, "_oral_active", False):
                        _escalate_chance = 0
                    elif girl.Lust >= 55 and _has_sex_history and _msa < 3 and not _is_lesbian:
                        _escalate_chance = min(15 + (girl.Lust - 55) + _msa * 12, 50)
                    _wants_sex = _escalate_chance > 0 and renpy.random.randint(1, 100) <= _escalate_chance
                if _wants_sex:
                    python:
                        store._mast_sex_asks += 1
                        _n = store._mast_sex_asks
                    if _n <= 2:
                        # --- Asks 1 and 2: simple request ---
                        if _n == 1:
                            $ Say_Line(girl, _("I need the real thing... please."))
                        else:
                            $ Say_Line(girl, _("Please... my fingers aren't enough anymore... I need you."))
                        menu:
                            "Give her what she wants":
                                # Cheat path gate
                                if _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False) and _cheat_stage(girl) < 2:
                                    python:
                                        _cep = getattr(girl, "_cheat_escalation_path", 0)
                                        if _cep == 1:
                                            _mg_deny = "I want you so badly... but I have a {hint}boyfriend{/hint}! We can't! Not like this!"
                                        elif _cep == 2:
                                            _mg_deny = _("I want to but... I'm not ready. Not yet. I need to be in control of when this happens.")
                                        else:
                                            _mg_deny = _("God I want you... but not now. Somewhere more private, on my terms.")
                                    $ Say_Line(girl, _mg_deny)
                                    $ Change_Status(girl, "Inbt", 5)
                                else:
                                    $ Change_Status(girl, "Love", 5)
                                    call COWGIRL_End(girl, dress_up=False) from _call_COWGIRL_End_mastesc
                                    if CurrentLocation in SHOWER_SPOTS:
                                        $ girl.Collar = False
                                        $ girl.Outfit_Change(over="none", mid="none", chest="none", legs="none", panties="none", shoes="none")
                                        $ girl._saved_outfit = None
                                    call sex_menu(girl, CurrentLocation, store.TimeIndex) from _call_sex_menu_mastesc
                                    return
                            "Not now":
                                $ Change_Status(girl, "Obed", 3)
                                $ girl.Lust = max(girl.Lust - 50, 0)
                                "Frustrated, she clearly loses focus from the rejection."
                                if _n == 1:
                                    $ Say_Line(girl, _("You're really going to leave me like this...?"))
                                else:
                                    $ Say_Line(girl, _("I can't believe you're doing this to me..."))
                    else:
                        # --- Ask 3: desperate negotiation ---
                        call _mast_desperate_negotiation(girl) from _call_mast_desp_neg
                        if store._mast_desp_result == "sex":
                            return
                        if store._mast_desp_result == "kicked":
                            # She already told him to leave: silent redress, then the
                            # centralized angry kick-out (expression, angry status, narration, campus).
                            $ print("[MAST_DESP] kicked: %s rejected 3rd ask -> angry kick-out (cowgirl)" % girl.gid)
                            call COWGIRL_End(girl, dress_up=False) from _call_COWGIRL_End_desp_kicked
                            call _scene_kick_to_campus(girl, mood="angry") from _call_kick_mast_desp_cg
                            return

            "Start" if cowgirl_speed == 0:
                if getattr(store, "_oral_active", False):
                    $ cowgirl_speed = 1
                    call MASTURBATE_ApplySpeed(girl, cowgirl_speed) from _call_MASTURBATE_ApplySpeed_6
                    $ _girl_lust_gain(girl, 4, cowgirl_speed)
                    $ _moan = scene_moan_tick(girl, "oral", cowgirl_speed)
                    if _moan:
                        call _moan_say(girl, _moan) from _call_ms_cg_oral
                    if girl.Lust >= 100:
                        call GirlCumming(girl, "oral", "cowgirl") from _call_GirlCumming_7
                    $ Narration(_("You lean in and start."))
                else:
                    $ Say_Player(_("Go ahead... start touching yourself."))
                    $ cowgirl_speed = 1
                    call MASTURBATE_ApplySpeed(girl, cowgirl_speed) from _call_MASTURBATE_ApplySpeed_6b
                    $ _girl_lust_gain(girl, 2, cowgirl_speed)
                    $ _moan = scene_moan_tick(girl, "masturbate", cowgirl_speed)
                    if _moan:
                        call _moan_say(girl, _moan) from _call_ms_cg_mast2
                    if girl.Lust >= 100:
                        call GirlCumming(girl, "masturbate", "cowgirl") from _call_GirlCumming_7b
                    $ Narration(_("She begins to touch herself."))

            "Speed up" if cowgirl_speed >= 1 and cowgirl_speed < 3:
                $ advance_round(TIME_COSTS["sex_tick"])
                $ Say_Player(_("Faster..."))
                $ cowgirl_speed += 1
                call MASTURBATE_ApplySpeed(girl, cowgirl_speed) from _call_MASTURBATE_ApplySpeed_7
                python:
                    _mast_phase_su = "oral" if getattr(store, "_oral_active", False) else "masturbate"
                    if _mast_phase_su == "oral":
                        _mast_lust_su = 4 if cowgirl_speed == 1 else 7 if cowgirl_speed == 2 else 10
                    else:
                        _mast_lust_su = 2 if cowgirl_speed == 1 else 4 if cowgirl_speed == 2 else 6
                $ _girl_lust_gain(girl, _mast_lust_su, cowgirl_speed)
                $ _moan = scene_moan_tick(girl, _mast_phase_su, cowgirl_speed)
                if _moan:
                    call _moan_say(girl, _moan) from _call_ms_cg_mast_su
                if girl.Lust >= 100:
                    call GirlCumming(girl, _mast_phase_su, "cowgirl") from _call_GirlCumming_8
                if getattr(store, "_oral_active", False):
                    $ Narration(_("You speed up."))
                else:
                    $ Narration(_("She speeds up her movements."))

            "Speed down" if cowgirl_speed > 0:
                $ advance_round(1)
                $ cowgirl_speed -= 1
                call MASTURBATE_ApplySpeed(girl, cowgirl_speed) from _call_MASTURBATE_ApplySpeed_8
                if getattr(store, "_oral_active", False):
                    $ Narration(_("You slow down."))
                else:
                    $ Narration(_("She slows down."))

            "Eat her out" if cowgirl_speed >= 1 and not getattr(store, "_oral_active", False) and not getattr(store, "hiding_face", False):
                $ _oral_appr = sex_action_check(girl, "oral")
                if _oral_appr["accepted"]:
                    $ store._oral_active = True
                    $ store._scene_phase = "oral"
                    $ girl.Sex_acts["oral"] = girl.Sex_acts.get("oral", 0) + 1
                    $ set_scene_expression(girl, "pleasure_mild")
                    call MASTURBATE_ApplySpeed(girl, cowgirl_speed) from _call_MASTURBATE_ApplySpeed_oral_on
                    $ Say_Line(girl, sex_line_for(girl, "oral", True))
                else:
                    $ Say_Line(girl, sex_line_for(girl, "oral", False))

            "Let her use her hands" if getattr(store, "_oral_active", False):
                $ store._oral_active = False
                $ store._scene_phase = "masturbate"
                call MASTURBATE_ApplySpeed(girl, cowgirl_speed) from _call_MASTURBATE_ApplySpeed_oral_off
                $ Narration(_("She starts touching herself again."))

            "Strip her" if not getattr(store, "_scene_restricted", False):
                $ advance_round(1)
                call MASTURBATE_StripMenu(girl) from _call_MASTURBATE_StripMenu

            "Record Options..." if not getattr(store, "_oral_active", False) and (not getattr(store, "_recording_active", False) or getattr(store, "_recording_girl", None) == girl):
                menu:
                    "Record her" if not getattr(store, "_recording_active", False):
                        call _sex_phone_menu(girl, "masturbate") from _call__sex_phone_menu_3
                    "Ask [store._ntr_watching_npc.Name] to record" if store._ntr_partner_watching and not getattr(store, "_recording_active", False):
                        call _watcher_record_start(girl, "masturbate") from _call_watcher_rec_start_mast_npc
                    "Ask [store._witness_girl.Name] to record" if getattr(store, "_witness_watching", False) and getattr(store, "_witness_girl", None) is not None and not store._ntr_partner_watching and not getattr(store, "_recording_active", False):
                        call _watcher_record_start(girl, "masturbate") from _call_watcher_rec_start_mast_girl
                    "Stop recording" if getattr(store, "_recording_active", False) and getattr(store, "_recording_girl", None) == girl:
                        $ _rec_stop_name = _get_recording_stopper_name()
                        $ finalize_recording()
                        if store.hiding_face:
                            $ store.hiding_face = False
                        if _rec_stop_name:
                            $ _rec_stop_text = _tl(_("%s stopped the recording.")) % _rec_stop_name
                            $ Narration(_rec_stop_text)
                        else:
                            $ Narration(_("You stop recording."))
                    "Back":
                        pass
                call MASTURBATE_ApplySpeed(girl, cowgirl_speed) from _call_MASTURBATE_ApplySpeed_rec_opts

            "Stop now":
                # If Lust is high and she hasn't cum yet, she begs to continue
                if girl.Lust >= 70 and not getattr(store, "_mast_stop_asked", 0) >= 3:
                    python:
                        _stop_n = getattr(store, "_mast_stop_asked", 0)
                        store._mast_stop_asked = _stop_n + 1
                        if _stop_n == 0:
                            _beg_line = _("Please... just a little more, I'm so close...")
                        elif _stop_n == 1:
                            _beg_line = _("No, please... I can't stop now, I need this so bad...")
                        else:
                            _beg_line = _("I'm begging you... don't make me stop... I'll do anything...")
                    $ Say_Line(girl, _beg_line)
                    menu:
                        "Let her continue":
                            $ Change_Status(girl, "Love", 5)
                        "No, stop now.":
                            $ Change_Status(girl, "Obed", 5)
                            $ Change_Status(girl, "Love", trait_love_loss(girl, -3))   # denied: a submissive minds nothing
                            $ Say_Line(girl, _("...Fine."))
                            call COWGIRL_End(girl, dress_up=False) from _call_COWGIRL_End_11
                            $ store._mast_stop_asked = 0
                            return
                else:
                    $ Say_Line(girl, _("Alright..."))
                    call COWGIRL_End(girl, dress_up=False) from _call_COWGIRL_End_11b
                    $ store._mast_stop_asked = 0
                    return

# ============================================================
# DESPERATE NEGOTIATION — 3rd sex ask during masturbation
# Player leverages her desperation for raw / creampie
# ============================================================
label _mast_desperate_negotiation(girl):

    $ store._mast_desp_result = "denied"

    # Cheat path: she won't go further than her current stage allows
    if _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False):
        python:
            _cep = getattr(girl, "_cheat_escalation_path", 0)
            if _cep == 1:
                _desp_deny = "I'll do anything... EXCEPT that. I have a {hint}boyfriend{/hint}! Please... just... not THAT."
            elif _cep == 2:
                _desp_deny = _("I want you so badly but... I'm not ready to go that far. Not like this. I need to be in control.")
            else:
                _desp_deny = _("I'm desperate but not THAT desperate... he doesn't deserve the full betrayal. Not yet.")
        $ Say_Line(girl, _desp_deny)
        $ Change_Status(girl, "Inbt", 8)
        $ Change_Status(girl, "Lust", 15)
        $ store._mast_desp_result = "denied"
        return

    $ Say_Line(girl, _("Please... I'll do anything, let you do whatever you want with me..."))

    menu:
        "Give her what she wants":
            $ Change_Status(girl, "Love", 5)
            call COWGIRL_End(girl, dress_up=False) from _call_COWGIRL_End_desp_norm
            if CurrentLocation in SHOWER_SPOTS:
                $ girl.Collar = False
                $ girl.Outfit_Change(over="none", mid="none", chest="none", legs="none", panties="none", shoes="none")
                $ girl._saved_outfit = None
            call sex_menu(girl, CurrentLocation, store.TimeIndex) from _call_sex_menu_desp_norm
            $ store._mast_desp_result = "sex"
            return

        "Only if we do it raw":
            $ Say_Player(_("Only if we do it raw."))
            jump ._negotiate_raw

        "Not now":
            $ Change_Status(girl, "Obed", 3)
            $ girl.Lust = max(girl.Lust - 50, 0)
            "Frustrated, she clearly loses focus from the rejection."
            $ set_scene_expression(girl, "angry")
            $ Say_Line(girl, _("Then just... go. Leave me alone."))
            $ store._mast_desp_result = "kicked"
            return

label ._negotiate_raw:

    # her step locks going raw (story_steps.rpy "raw"): desperate or not, never bare
    if story_act_locked(girl, "raw"):
        $ set_scene_expression(girl, "angry")
        $ Say_Line(girl, story_locked_line(girl, "raw"))
        $ girl.Lust = max(girl.Lust - 50, 0)
        "Frustrated, she clearly loses focus from the rejection."
        $ store._mast_desp_result = "denied"
        return

    # Desperation approval: sex threshold (1100) with +200 bonus = effectively 900
    python:
        _desp_rule = ApprovalRuleFor(girl, "sex", "sex")
        _desp_rule["Bonus"] = _desp_rule.get("Bonus", 0) + 200
        _desp_raw_result = ApprovalCheck(girl, ReturnData=True, **_desp_rule)
        _accepts_raw = _desp_raw_result["accepted"]

    if not _accepts_raw:
        # Trait-aware denial
        if girl.has_trait("cum_slut"):
            $ Say_Line(girl, renpy.random.choice([_("I want it so bad but... no, not without protection. I can't think straight."), _("God, I want to feel you raw... but no. I'm not THAT desperate. ...Am I?")]))
        elif girl.has_trait("hate_cum"):
            $ Say_Line(girl, renpy.random.choice([_("Raw?! Are you insane?! I'd rather use my fingers forever than risk THAT."), _("Absolutely not. I hate that stuff anywhere near me. I'll finish on my own.")]))
        else:
            $ Say_Line(girl, renpy.random.choice([_("No... that's too much. I... I'll handle it myself."), _("I can't agree to that... not like this. I'll finish with my fingers.")]))
        $ girl.Lust = max(girl.Lust - 50, 0)
        "Frustrated, she clearly loses focus from the rejection."
        $ store._mast_desp_result = "denied"
        return

    # Trait-aware acceptance
    if girl.has_trait("cum_slut"):
        $ Say_Line(girl, renpy.random.choice([_("Raw? God yes... I want to feel everything. NOW."), _("No condom? Even better... I want every inch of you right now.")]))
    elif girl.has_trait("hate_cum"):
        $ Say_Line(girl, renpy.random.choice([_("Fine... raw. But if you even THINK about finishing inside me..."), _("Ok... no condom. But you pull out. You PULL OUT. Understood?")]))
    else:
        $ Say_Line(girl, renpy.random.choice([_("Ok... raw. Fine. But NOW."), _("No condom...? I... fine. Just hurry up before I change my mind.")]))

    menu:
        "Deal.":
            jump ._launch_desperate_sex

        "...and I want to cum inside.":
            $ Say_Player(_("...and I want to cum inside."))
            jump ._negotiate_creampie

label ._negotiate_creampie:

    # Trait bonus/penalty for creampie negotiation
    # cum_slut: +150 extra (she wants it), hate_cum: -200 (she hates it)
    python:
        _desp_rule2 = ApprovalRuleFor(girl, "sex", "sex")
        _cream_trait_bonus = 300
        if hasattr(girl, "has_trait"):
            if girl.has_trait("cum_slut"):
                _cream_trait_bonus += 150
            elif girl.has_trait("hate_cum"):
                _cream_trait_bonus -= 200
        _desp_rule2["Bonus"] = _desp_rule2.get("Bonus", 0) + _cream_trait_bonus
        _desp_cream_result = ApprovalCheck(girl, ReturnData=True, **_desp_rule2)
        _accepts_cream = _desp_cream_result["accepted"] and not story_act_locked(girl, "cum_inside")

    if not _accepts_cream:
        # Trait-aware denial
        if girl.has_trait("cum_slut"):
            $ Say_Line(girl, renpy.random.choice([_("I want it so bad... but not inside. Not yet. Just fuck me raw and pull out."), _("Mmm... I want your cum but... not inside me right now. Just give it to me raw.")]))
        elif girl.has_trait("hate_cum"):
            $ Say_Line(girl, renpy.random.choice([_("Inside?! HELL no! I already said yes to raw, don't push it! Pull out or forget it!"), _("You want to cum INSIDE me?! That's disgusting! Raw is the limit. Take it or leave it!")]))
        else:
            $ Say_Line(girl, renpy.random.choice([_("Please... fuck me raw, but pull out. That's as far as I'll go."), _("Inside is too much... just pull out. That's my condition.")]))

        menu:
            "Fine, deal.":
                jump ._launch_desperate_sex

            "Then forget it.":
                if girl.has_trait("cum_slut"):
                    $ Say_Line(girl, _("You're really going to leave me empty over this...? Fine. I'll do it myself."))
                elif girl.has_trait("hate_cum"):
                    $ Say_Line(girl, _("Good riddance. I was never going to let you do that anyway."))
                else:
                    $ Say_Line(girl, _("...Fine. I'll finish with my fingers then."))
                $ girl.Lust = max(girl.Lust - 50, 0)
                "Frustrated, she clearly loses focus from the rejection."
                $ store._mast_desp_result = "denied"
                return
    else:
        # Trait-aware acceptance (a cum_slut still discovering it wants it, she does not need it yet)
        if girl.has_trait("cum_slut") and trait_is_new(girl, "cum_slut"):
            $ Say_Line(girl, renpy.random.choice([_("Inside...? Yes... I want to feel it. Please, now."), _("Cum inside me, please... I want to feel all of it. Don't hold anything back!")]))
        elif girl.has_trait("cum_slut"):
            $ Say_Line(girl, renpy.random.choice([_("Yes... fill me up, every last drop! I NEED it inside me!"), _("Cum inside me, please... I want to feel all of it. Don't hold anything back!")]))
        elif girl.has_trait("hate_cum"):
            $ Say_Line(girl, renpy.random.choice([_("I can't believe I'm saying this... fine. Inside. Just... just do it before I come to my senses."), _("God...You motherfu... okay. Inside. But this is the desperation talking, not me. Remember that.")]))
        else:
            $ Say_Line(girl, renpy.random.choice([_("Fill me up... just do it now, I need it!"), _("Inside... fine. I don't care anymore. Just fuck me NOW.")]))
        $ store._desperation_accepted_creampie = True
        $ unlock_achievement("persistence_pays")
        jump ._launch_desperate_sex

label ._launch_desperate_sex:

    # End masturbation scene (detect origin by active scene girl)
    if getattr(store, "_laying_girl", None) is girl:
        call LD_End(girl, dress_up=False) from _call_LD_End_desp_launch
    else:
        call COWGIRL_End(girl, dress_up=False) from _call_COWGIRL_End_desp_launch

    # In showers, girl was nude — End restored clothes, strip again
    if CurrentLocation in SHOWER_SPOTS:
        $ girl.Collar = False
        $ girl.Outfit_Change(over="none", mid="none", chest="none", legs="none", panties="none", shoes="none")
        $ girl._saved_outfit = None

    # Set up sex session flags
    python:
        session_cum_reset()
        store._lost_virginity_this_scene = False
        store._condom_removed_midscene = False
        store._sub_event_position_switched = False
        store._player_exposed_this_session = False
        store._creampie_warned = False
        store._sex_menu_deny_count = 0
        store._deny_kick = False
        store._player_exhausted = False
        store._session_girl_orgasms = 0
        store._session_orgasms_by_girl = {}
        store._session_spanked_girls = set()
        store._hard_cum_ready = False
        store._witness_girl = None
        store._witness_watching = False
        store._witness_join_available = False
        store._witness_scene_aborted = False
        store._witness_check_done = False
        store._interruption_happened = False
        store._interrupt_rolls_ready = False

        # RAW — no condom
        store.condom_active = False
        store.condom_denied = False
        store._condom_removal_denied = False

        # Desperation flags
        store._desperation_accepted_raw = True
        if not getattr(store, "_desperation_accepted_creampie", False):
            store._creampie_consent = "denied"
            store._desperation_accepted_creampie = False
        else:
            store._creampie_consent = "allowed"

        pass
        if not getattr(girl, "_saved_outfit", None):
            girl.SaveOutfit()

        # Mark intimacy + stats
        mark_intimacy(girl, "sex")
        sex_accept_with_temptation(girl, "sex")
        Change_Status(girl, "Love", 15)
        Change_Status(girl, "Inbt", 10)
        Change_Status(girl, "Obed", 8)

    # Position choice
    menu:
        "Riding" if girl_has_pose(girl, "cowgirl"):
            "She climbs on top of you."
            $ cowgirl_speed = 0
            call COWGIRL_Launch(girl) from _call_COWGIRL_Launch_desp
            if girl.has_trait("virgin"):
                call virgin_first_time(girl, "cowgirl") from _call_virgin_first_time_desp_cg
                $ print("[VIRGIN] CG desp: virgin_first_time returned, continuing to ControlMenu")
            $ mark_intimacy(girl, "cowgirl")
            $ _had_condom_before_scene = store.condom_active
            call COWGIRL_ControlMenu(girl) from _call_COWGIRL_ControlMenu_desp
            if not _had_condom_before_scene and not store._condom_removed_midscene and not getattr(store, "_sub_event_position_switched", False):
                python:
                    _track_raw_sex_start(girl)

        "Reverse Cowgirl" if girl_has_pose(girl, "reverse_cowgirl"):
            "She gets into position for you."
            $ rcg_speed = 0
            call RCG_Launch(girl) from _call_RCG_Launch_desp
            if girl.has_trait("virgin"):
                call virgin_first_time(girl, "reverse_cowgirl") from _call_virgin_first_time_desp_rcg
            $ mark_intimacy(girl, "reverse_cowgirl")
            $ _had_condom_before_scene = store.condom_active
            call RCG_ControlMenu(girl) from _call_RCG_ControlMenu_desp
            if not _had_condom_before_scene and not store._condom_removed_midscene and not getattr(store, "_sub_event_position_switched", False):
                python:
                    _track_raw_sex_start(girl)

        "Doggy" if girl_has_pose(girl, "doggy"):
            "She turns around and bends over."
            $ doggy_speed = 0
            call DG_Launch(girl) from _call_DG_Launch_desp
            if girl.has_trait("virgin"):
                call virgin_first_time(girl, "doggy") from _call_virgin_first_time_desp_dg
            $ mark_intimacy(girl, "doggy")
            $ _had_condom_before_scene = store.condom_active
            call DG_ControlMenu(girl) from _call_DG_ControlMenu_desp
            if not _had_condom_before_scene and not store._condom_removed_midscene and not getattr(store, "_sub_event_position_switched", False):
                python:
                    _track_raw_sex_start(girl)

        "Full Nelson" if girl_has_pose(girl, "full_nelson"):
            "You lift her up and get into position."
            $ fn_speed = 0
            call FN_Launch(girl) from _call_FN_Launch_desp
            if girl.has_trait("virgin"):
                call virgin_first_time(girl, "full_nelson") from _call_virgin_first_time_desp_fn
            $ mark_intimacy(girl, "full_nelson")
            $ _had_condom_before_scene = store.condom_active
            call FN_ControlMenu(girl) from _call_FN_ControlMenu_desp
            if not _had_condom_before_scene and not store._condom_removed_midscene and not getattr(store, "_sub_event_position_switched", False):
                python:
                    _track_raw_sex_start(girl)

        "Laying Down" if girl_has_pose(girl, "laying_down"):
            "She lies back and spreads her legs for you."
            $ laying_speed = 0
            call LD_Launch(girl) from _call_LD_Launch_desp
            if girl.has_trait("virgin"):
                call virgin_first_time(girl, "laying_down") from _call_virgin_first_time_desp_ld
            $ mark_intimacy(girl, "laying_down")
            $ _had_condom_before_scene = store.condom_active
            call LD_ControlMenu(girl) from _call_LD_ControlMenu_desp
            if not _had_condom_before_scene and not store._condom_removed_midscene and not getattr(store, "_sub_event_position_switched", False):
                python:
                    _track_raw_sex_start(girl)

    # Post-sex: desperation regret if she accepted creampie under pressure
    if getattr(store, "_desperation_accepted_creampie", False):
        $ girl.RegisterAction("desperation_creampie_regret")
        $ Change_Status(girl, "Love", -10)
        $ Say_Line(girl, _("I can't believe I let you do that... I was so desperate I couldn't think straight."))

    if getattr(store, "_desperation_accepted_raw", False):
        $ girl.RegisterAction("desperation_raw_accepted")

    # Clean up desperation flags + full scene cleanup
    python:
        store._desperation_accepted_raw = False
        store._desperation_accepted_creampie = False
        scene_full_cleanup(girl)

    $ store._mast_desp_result = "sex"
    return

label MASTURBATE_StripMenu(girl):
    while True:
        python:
            print("[MAST_STRIP_MENU] gid=%s Panties=%s state=%s pose=%s has_side=%s has_down=%s" % (girl.gid, girl.Panties, girl.clothes_state.get("panties"), sprite_state.get(girl.Id, {}).get("pose", "?"), _item_has_state(girl, "panties", "side"), _item_has_state(girl, "panties", "down")))
            _sm_over = clothing_item_name(girl, "over")
            _sm_chest = clothing_item_name(girl, "chest")
            _sm_legs = clothing_item_name(girl, "skirt")
            _sm_panties = clothing_item_name(girl, "panties")
            _sm_shoes = clothing_item_name(girl, "shoes")
        menu:
            "Remove [_sm_over]" if girl.Over:
                call _strip_approval(girl, ["over"]) from _call__strip_approval_15
                if store._strip_approved:
                    $ girl.Outfit_Change(over="none", pose="cowgirl")
                    call MASTURBATE_ApplySpeed(girl, cowgirl_speed) from _call_MASTURBATE_ApplySpeed_11
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_14

            "Pull [_sm_chest] up" if girl.Chest and girl.clothes_state.get("chest") != "up" and _item_has_state(girl, "chest", "up"):
                call _strip_approval(girl, ["chest"]) from _call__strip_approval_mast_chest_up
                if store._strip_approved:
                    $ girl.Outfit_Change(chest_up=True, pose="cowgirl")
                    call MASTURBATE_ApplySpeed(girl, cowgirl_speed) from _call_MASTURBATE_ApplySpeed_chest_up
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_mast_chest_up

            "Pull [_sm_chest] down" if girl.Chest and girl.ChestUp:
                $ girl.SetChestUp(False, pose="cowgirl")
                call MASTURBATE_ApplySpeed(girl, cowgirl_speed) from _call_MASTURBATE_ApplySpeed_13

            "Remove [_sm_chest]" if girl.Chest:
                python:
                    _mast_strip_slots = ["chest"]
                    if girl.Over:
                        _mast_strip_slots.append("over")
                call _strip_approval(girl, _mast_strip_slots) from _call__strip_approval_16
                if store._strip_approved:
                    python:
                        _mast_strip_kw = {"chest": "none", "pose": "cowgirl"}
                        if girl.Over:
                            _mast_strip_kw["over"] = "none"
                        girl.Outfit_Change(**_mast_strip_kw)
                    call MASTURBATE_ApplySpeed(girl, cowgirl_speed) from _call_MASTURBATE_ApplySpeed_12
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_15

            "Remove [_sm_legs]" if girl.Legs:
                call _strip_approval(girl, ["legs"]) from _call__strip_approval_18
                if store._strip_approved:
                    $ girl.Outfit_Change(legs="none", pose="cowgirl")
                    call MASTURBATE_ApplySpeed(girl, cowgirl_speed) from _call_MASTURBATE_ApplySpeed_14
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_16

            "Pull [_sm_panties] to the side" if girl.Panties and girl.clothes_state.get("panties") == "full" and _item_has_state(girl, "panties", "side"):
                call _strip_approval(girl, ["panties"]) from _call__strip_approval_mast_pan_side
                if store._strip_approved:
                    $ girl.clothes_state["panties"] = "side"
                    call MASTURBATE_ApplySpeed(girl, cowgirl_speed) from _call_MASTURBATE_ApplySpeed_pan_side
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_mast_pan_side

            "Pull [_sm_panties] down" if girl.Panties and girl.clothes_state.get("panties") != "down" and _item_has_state(girl, "panties", "down"):
                $ print("[MAST_STRIP] Pull panties down selected! current_state=%s" % girl.clothes_state.get("panties"))
                call _strip_approval(girl, ["panties"]) from _call__strip_approval_mast_pan_down
                if store._strip_approved:
                    $ girl.clothes_state["panties"] = "down"
                    call MASTURBATE_ApplySpeed(girl, cowgirl_speed) from _call_MASTURBATE_ApplySpeed_pan_down
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_mast_pan_down

            "Remove [_sm_panties]" if girl.Panties:
                call _strip_approval(girl, ["panties"]) from _call__strip_approval_19
                if store._strip_approved:
                    $ girl.Outfit_Change(panties="none", pose="cowgirl")
                    call MASTURBATE_ApplySpeed(girl, cowgirl_speed) from _call_MASTURBATE_ApplySpeed_15
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_17

            "Remove [_sm_shoes]" if getattr(girl, "Shoes", None):
                $ girl.Outfit_Change(shoes="none", pose="cowgirl")
                call MASTURBATE_ApplySpeed(girl, cowgirl_speed) from _call_MASTURBATE_ApplySpeed_16

            "Back":
                return
