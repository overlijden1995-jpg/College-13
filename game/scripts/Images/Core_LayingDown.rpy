# Core_LayingDown.rpy — Laying Down pose core logic
# EXCLUSIVE to Tenny. Supports: rub, tip, vaginal, anal.

image ld_condom = "images/characters/Player/LD Condom.png"
image ld_condom_broken = "images/characters/Player/LD Condom Broken.png"

default laying_speed = 0
default laying_started = False
default laying_anal = False
default _laying_girl = None
default laying_blink = False
default laying_rub_mode = False
default laying_tip_mode = False
default laying_grab = False
default _ld_had_pussy = False
default _ld_had_anal = False
default _ld_torso_variant = 1
default _ld_arm_variant = 2
default _ld_pillow_active = False
default _ld_masturbating = False
default _ld_mast_t0 = None
default _ld_mast_speed = 1
default _ld_blood_active = False
default _ld_cum_dick_level = 0
default _ld_scene_type = "laying_down"   # LD_ControlMenu assigns it at entry; safety net for old saves

init python:

    # ── Turn head (hide face / look back) ──
    _LD_TURN_OBED_T = 400

    _LD_TURN_REFUSE_LINES = {
        "cum_slut": [
            _("No way, I want to see your face while you do me."),
            _("I like watching you... don't take that away from me."),
        ],
        # who gives the orders is femdom (docs/plan_femdom.md D3): hardcore keeps only the rough reasons
        "femdom": [
            _("I'll look wherever I want."),
            _("No. I want to see your face. That's not up for discussion."),
            _("You don't get to tell me where to look. Keep going."),
        ],
        "hardcore_sex": [
            _("Nah. I like the view from here."),
            _("No. I want to watch you while you fuck me hard."),
        ],
        "cute_sex": [
            _("I want to keep looking at you... is that okay?"),
            _("Please, I like being able to see you..."),
        ],
        "camera_hater": [
            _("Why? So you can record me? No."),
            _("I don't trust you enough for that."),
        ],
        "lesbian": [
            _("At least let me pretend you're someone else."),
            _("If I can't see you, this gets even weirder for me."),
        ],
        "_default": [
            _("No, I want to keep looking at you."),
            _("I'd rather keep my eyes on you."),
        ],
    }

    _LD_TURN_ACCEPT_LINES = {
        "cum_slut": [
            _("Fine... but you better not finish without warning me."),
            _("Okay, but I'll be turning back soon."),
        ],
        "hardcore_sex": [
            _("Whatever. Just keep going."),
            _("Fine. But don't get any ideas back there."),
        ],
        "cute_sex": [
            _("O-okay... if that's what you want..."),
            _("It feels weird not seeing you, but... fine."),
        ],
        "_default": [
            _("Alright... if that's what you want."),
            _("Fine... this feels a bit strange though."),
            _("Okay... just tell me when I can look back."),
        ],
    }

    def _ld_turn_trait_key(girl):
        for _tk in ("cum_slut", "femdom", "hardcore_sex", "cute_sex", "camera_hater", "lesbian"):
            if girl.has_trait(_tk):
                return _tk
        return "_default"

    def _ld_turn_check(girl):
        obed = getattr(girl, "Obed", 0)
        bonus = 0
        if girl.has_trait("hardcore_sex"):
            bonus -= 100
        if girl.has_trait("cute_sex"):
            bonus -= 50
        if girl.has_trait("camera_hater"):
            bonus -= 150
        if girl.has_trait("camera_lover"):
            bonus += 200
        # an order about where she looks: a submissive takes it sooner, a femdom later (plan_submissive_pass S2)
        if girl.has_trait("submissive"):
            bonus += 100
        if girl.has_trait("femdom"):
            bonus -= 100
        return (obed + bonus) >= _LD_TURN_OBED_T

    # ── Expression pools ──
    _LD_EYES_BY_SPEED = {
        0: ["eyes_normal", "eyes_side", "eyes_closed"],
        1: ["eyes_normal", "eyes_side", "eyes_squint"],
        2: ["eyes_squint", "eyes_closed", "eyes_squint_2"],
        3: ["eyes_squint_2", "eyes_closed", "eyes_surprised"],
        4: ["eyes_closed", "eyes_ahegao"],
    }
    _LD_BROWS_BY_SPEED = {
        0: ["brows_normal"],
        1: ["brows_normal", "brows_confused"],
        2: ["brows_confused", "brows_surprised"],
        3: ["brows_surprised", "brows_horny"],
        4: ["brows_horny", "brows_surprised"],
    }
    _LD_MOUTH_BY_SPEED = {
        0: ["mouth_normal", "mouth_smile"],
        1: ["mouth_normal", "mouth_smile", "mouth_lipbite"],
        2: ["mouth_surprised", "mouth_moaning", "mouth_moaning_2"],
        3: ["mouth_tongue", "mouth_surprised", "mouth_moaning_3"],
        4: ["mouth_tongue", "mouth_ahegao"],
    }

    def _ld_refresh_expression(girl, state):
        _eyes = _laying_safe(state.get("eyes", "eyes_normal"))
        _brows = _laying_safe(state.get("brows", "brows_normal"))
        _mouth = _laying_safe(state.get("mouth", "mouth_normal"))
        _blush = _attr_for_blush(girl)
        _speed = getattr(store, "laying_speed", 0)
        _slot_at = [ld_get_slot_transform(_speed)]
        _img = "tenny laying %s %s %s %s" % (_eyes, _brows, _mouth, _blush)
        renpy.show(_img, tag="tenny", at_list=_slot_at, zorder=_LD_Z_HEAD)
        if "face" in getattr(girl, "Cum", []):
            renpy.show("tenny laying_cum_face", tag="ld_cum_face", at_list=_slot_at, zorder=_LD_Z_CUM + 3)
        renpy.restart_interaction()

    def _ld_blink_loop(girl):
        import time as _time, random as _random
        def _is_active():
            return getattr(store, "_laying_girl") is girl
        try:
            while _is_active():
                _time.sleep(_random.uniform(3.0, 6.0))
                if not _is_active():
                    break
                _st = sprite_state.get(girl.Id, {})
                _prev_eyes = _st.get("eyes", "eyes_normal")
                _st["eyes"] = "eyes_closed"
                _ld_refresh_expression(girl, _st)
                _time.sleep(_random.uniform(0.12, 0.22))
                if not _is_active():
                    break
                _st["eyes"] = _prev_eyes
                _ld_refresh_expression(girl, _st)
        finally:
            _st = sprite_state.get(girl.Id, {})
            if _st.get("eyes") == "eyes_closed":
                _st["eyes"] = _st.get("_prev_eyes", "eyes_normal")

    def _ld_pool_override(girl, speed, eyes_pool, brows_pool, mouth_pool):
        if getattr(store, "_cg_eyes_locked", False):
            cur_eyes = sprite_state.get(girl.Id, {}).get("eyes", "eyes_closed")
            return ([cur_eyes], brows_pool, mouth_pool)
        return (eyes_pool, brows_pool, mouth_pool)

    def _laying_expression_cycle(girl):
        _scene_expression_cycle(girl, "_laying_girl", "laying_speed",
            _LD_EYES_BY_SPEED, _LD_BROWS_BY_SPEED, _LD_MOUTH_BY_SPEED,
            sleep_range=(5.0, 10.0), refresh_fn=_ld_refresh_expression,
            pool_override_fn=_ld_pool_override)

    # ── Z-order constants ──
    _LD_Z_PILLOW          = 9800
    _LD_Z_LEGS            = 9810
    _LD_Z_PANTIES_DOWN    = 9812
    _LD_Z_PANTS_DOWN      = 9815
    _LD_Z_GUY_CALF_2     = 9816
    _LD_Z_GUY_CALF_1     = 9817
    _LD_Z_GUY_LEGS_2     = 9818
    _LD_Z_GUY_LEGS_1     = 9819
    _LD_Z_PELVIS          = 9822
    _LD_Z_GUY_PELVIS      = 9823
    _LD_Z_GUY_PELVIS_SAFE = 9824
    _LD_Z_BEFORE_PUSSY    = 9825
    _LD_Z_TONGUE          = 9827
    _LD_Z_MAST_BELOW      = 9830
    _LD_Z_DURING_BELOW    = 9833
    _LD_Z_DURING          = 9835
    _LD_Z_DURING_MAST     = 9836
    _LD_Z_CUM_VAGINAL     = 9838
    _LD_Z_PENIS_VAG       = 9840
    _LD_Z_DURING_SAFE     = 9842
    _LD_Z_BEFORE_ASS      = 9844
    _LD_Z_DURING_ANAL_BL  = 9846
    _LD_Z_PENIS_ANAL      = 9847
    _LD_Z_ARMS_BELOW      = 9848
    _LD_Z_TORSO           = 9850
    _LD_Z_CHEST           = 9851
    _LD_Z_MID             = 9852
    _LD_Z_MID_SLEEVE      = 9853
    _LD_Z_OVER            = 9854
    _LD_Z_OVER_SLEEVE     = 9855
    _LD_Z_PENIS_RUB       = 9882
    _LD_Z_DURING_ANAL_SF  = 9859
    _LD_Z_ASS             = 9860
    _LD_Z_BUTT_BLUSH      = 9865
    _LD_Z_DURING_ANAL     = 9868
    _LD_Z_PANTIES         = 9880
    _LD_Z_MAST_OVER       = 9885
    _LD_Z_TOP             = 9890
    _LD_Z_GUY_CUM         = 9900
    _LD_Z_HEAD            = 9910
    _LD_Z_CUM             = 9920
    _LD_Z_CUM_GIRL        = 9980

    # ── Z-order helpers ──
    def _ld_pen_z():
        if getattr(store, "laying_rub_mode", False) and not store.laying_started:
            return _LD_Z_PENIS_RUB
        if getattr(store, "laying_anal", False):
            return _LD_Z_PENIS_ANAL
        return _LD_Z_PENIS_VAG

    def _ld_cum_z():
        return _LD_Z_CUM

    def _ld_cum_frame_anim(st, at, folder, n_frames, frame_dur=0.042):
        idx = min(int(st / frame_dur), n_frames - 1)
        path = "images/characters/Tenny/Laying Down/Cum/%s/%d.png" % (folder, idx + 1)
        d = renpy.displayable(path)
        if idx < n_frames - 1:
            return d, frame_dur - (st % frame_dur)
        return d, None

    _MAST_FRAME_DURS = {1: 0.042, 2: 0.032, 3: 0.024}

    def _ld_mast_frame_anim(st, at, folder, base_dur=None):
        import time as _time
        _t0 = getattr(store, "_ld_mast_t0", None)
        n_frames = 31
        if base_dur is not None:
            frame_dur = base_dur
        else:
            frame_dur = _MAST_FRAME_DURS.get(getattr(store, "_ld_mast_speed", 1), 0.042)
        if _t0 is None:
            return renpy.displayable("images/characters/Tenny/Laying Down/Effects/Masturbate/%s/01.png" % folder), 0.1
        elapsed = _time.time() - _t0
        cycle_len = (n_frames * 2) - 2
        cycle_pos = int(elapsed / frame_dur) % cycle_len
        if cycle_pos < n_frames:
            frame = cycle_pos + 1
        else:
            frame = cycle_len - cycle_pos + 1
        path = "images/characters/Tenny/Laying Down/Effects/Masturbate/%s/%02d.png" % (folder, frame)
        d = renpy.displayable(path)
        return d, frame_dur - (elapsed % frame_dur)

    # ── Transform helpers ──
    def ld_get_slot_transform(speed):
        m = {0: ld_slot_speed0, 1: ld_slot_speed1, 2: ld_slot_speed2, 3: ld_slot_speed3, 4: ld_slot_speed4}
        return m.get(speed, m[1])

    def ld_get_wave_transform(speed):
        m = {0: ld_wave_speed0, 1: ld_wave_speed1, 2: ld_wave_speed2, 3: ld_wave_speed3, 4: ld_wave_speed4}
        return m.get(speed, ld_wave_speed0)

    def ld_get_ass_transform(speed):
        m = {0: ld_ass_speed0, 1: ld_ass_speed1, 2: ld_ass_speed2, 3: ld_ass_speed3, 4: ld_ass_speed4}
        return m.get(speed, m[0])

    def ld_get_penis_transform(speed):
        m = {0: ld_penis_speed0, 1: ld_penis_speed1, 2: ld_penis_speed2, 3: ld_penis_speed3, 4: ld_penis_speed4}
        return m.get(speed, m[1])

    def lda_get_penis_transform(speed):
        m = {0: lda_penis_speed0, 1: lda_penis_speed1, 2: lda_penis_speed2, 3: lda_penis_speed3, 4: lda_penis_speed4}
        return m.get(speed, m[1])

    def ld_get_legs_thrust_transform(speed):
        m = {0: ld_legs_thrust_speed0, 1: ld_legs_thrust_speed1, 2: ld_legs_thrust_speed2, 3: ld_legs_thrust_speed3, 4: ld_legs_thrust_speed4}
        return m.get(speed, m[0])

    # ── Thigh/Calf rotation pivots (canvas pixel coords) ──
    _LD_THIGH_1_PIVOT = (1050, 825)
    _LD_THIGH_2_PIVOT = (1220, 825)
    _LD_CALF_1_PIVOT  = (890, 875)
    _LD_CALF_2_PIVOT  = (1380, 875)

    def ld_get_thigh_1_transform(speed):
        px, py = _LD_THIGH_1_PIVOT
        m = {0: ld_slot_speed0, 1: ld_rot_1(px, py, -1.5), 2: ld_rot_2(px, py, -2.5), 3: ld_rot_3(px, py, -3.5), 4: ld_rot_4(px, py, -4.0)}
        return m.get(speed, m[0])

    def ld_get_thigh_2_transform(speed):
        px, py = _LD_THIGH_2_PIVOT
        m = {0: ld_slot_speed0, 1: ld_rot_1(px, py, 1.5), 2: ld_rot_2(px, py, 2.5), 3: ld_rot_3(px, py, 3.5), 4: ld_rot_4(px, py, 4.0)}
        return m.get(speed, m[0])

    def ld_get_calf_1_transform(speed):
        px, py = _LD_CALF_1_PIVOT
        m = {0: ld_slot_speed0, 1: ld_rot_1(px, py, 2.0), 2: ld_rot_2(px, py, 3.5), 3: ld_rot_3(px, py, 5.0), 4: ld_rot_4(px, py, 6.0)}
        return m.get(speed, m[0])

    def ld_get_calf_2_transform(speed):
        px, py = _LD_CALF_2_PIVOT
        m = {0: ld_slot_speed0, 1: ld_rot_1(px, py, -2.0), 2: ld_rot_2(px, py, -3.5), 3: ld_rot_3(px, py, -5.0), 4: ld_rot_4(px, py, -6.0)}
        return m.get(speed, m[0])

    def ld_get_guy_pelvis_transform(speed):
        m = {0: ld_guy_pelvis_speed0, 1: ld_guy_pelvis_speed1, 2: ld_guy_pelvis_speed2, 3: ld_guy_pelvis_speed3, 4: ld_guy_pelvis_speed4}
        return m.get(speed, m[0])

    def lda_get_guy_pelvis_transform(speed):
        m = {0: lda_guy_pelvis_speed0, 1: lda_guy_pelvis_speed1, 2: lda_guy_pelvis_speed2, 3: lda_guy_pelvis_speed3, 4: lda_guy_pelvis_speed4}
        return m.get(speed, m[0])

    # ── Layer helpers ──
    def _ld_hide_all_layers():
        _hide_scene_layers("laying_down")

    def _ld_hide_panties():
        renpy.hide("ld_panties")

    def _ld_show_rear_preview(girl):
        """Show LD body layers for non-sex-scene rear view (dare spank, lap, etc).
        Assumes set_girl_sprite(pose='laying_down') was NOT called — this handles everything."""
        store._ld_torso_variant = 1
        store._ld_arm_variant = 2

        slot_at = [ld_slot_speed0]
        ass_at = [ld_ass_speed0]

        renpy.show("tenny laying_legs_left", tag="ld_legs_left", at_list=slot_at, zorder=_LD_Z_LEGS)
        renpy.show("tenny laying_legs_right", tag="ld_legs_right", at_list=slot_at, zorder=_LD_Z_LEGS + 1)

        renpy.show("tenny laying_pelvis", tag="ld_pelvis", at_list=ass_at, zorder=_LD_Z_PELVIS)

        _ld_show_torso(girl, slot_at)
        _ld_show_clothing(girl, slot_at)

        renpy.show("tenny laying_ass_base_left", tag="ld_ass_left", at_list=ass_at, zorder=_LD_Z_ASS)
        renpy.show("tenny laying_ass_base_right", tag="ld_ass_right", at_list=ass_at, zorder=_LD_Z_ASS + 1)
        renpy.show("tenny laying_before_pussy", tag="ld_before_pussy", at_list=ass_at, zorder=_LD_Z_BEFORE_PUSSY)
        renpy.show("tenny laying_before_ass", tag="ld_before_ass", at_list=ass_at, zorder=_LD_Z_BEFORE_ASS)
        renpy.show("tenny laying_before_ass_2", tag="ld_before_ass_2", at_list=ass_at, zorder=_LD_Z_BEFORE_ASS + 1)

        renpy.show("tenny laying_butt_blush", tag="ld_butt_blush", at_list=ass_at, zorder=_LD_Z_BUTT_BLUSH)

        _pan_item = girl.Panties
        _legs_state = girl.clothes_state.get("skirt", "full") if girl.Legs else None
        if _pan_item and (not girl.Legs or _legs_state == "up"):
            _pan_state = girl.clothes_state.get("panties", "full")
            _pan_z = _LD_Z_PANTIES_DOWN if _pan_state == "down" else _LD_Z_PANTIES
            _pan_img = "tenny laying_panties_%s_%s" % (_pan_item, _pan_state)
            if renpy.has_image(_pan_img, exact=True):
                renpy.show(_pan_img, tag="ld_panties", at_list=ass_at, zorder=_pan_z)
            else:
                _ld_hide_panties()
        else:
            _ld_hide_panties()

        _ld_show_pants(girl, slot_at, ass_at)

        _eyes = _laying_safe(sprite_state.get(girl.Id, {}).get("eyes", "eyes_normal"))
        _brows = _laying_safe(sprite_state.get(girl.Id, {}).get("brows", "brows_normal"))
        _mouth = _laying_safe(sprite_state.get(girl.Id, {}).get("mouth", "mouth_normal"))
        _blush = _attr_for_blush(girl)
        _head_img = "tenny laying %s %s %s %s" % (_eyes, _brows, _mouth, _blush)
        renpy.show(_head_img, tag="tenny", at_list=slot_at, zorder=_LD_Z_HEAD)

        print("[LD_REAR_PREVIEW] showing rear preview for %s" % girl.gid)

    def _ld_show_pants(girl, slot_at, ass_at):
        _all_pants_tags = ("ld_pants_left", "ld_pants_right", "ld_pants_pelvis",
                           "ld_pants_ass_l", "ld_pants_ass_r", "ld_pants_torso",
                           "ld_pants_down_l", "ld_pants_down_r")
        _legs = girl.Legs
        if not _legs or getattr(store, "_ld_masturbating", False):
            for _t in _all_pants_tags:
                renpy.hide(_t)
            return

        _state = girl.clothes_state.get("skirt", "full")
        if _state == "up":
            for _t in ("ld_pants_left", "ld_pants_right", "ld_pants_pelvis",
                        "ld_pants_ass_l", "ld_pants_ass_r", "ld_pants_torso"):
                renpy.hide(_t)
            renpy.show("tenny laying_pants_down_left", tag="ld_pants_down_l", at_list=slot_at, zorder=_LD_Z_PANTS_DOWN)
            renpy.show("tenny laying_pants_down_right", tag="ld_pants_down_r", at_list=slot_at, zorder=_LD_Z_PANTS_DOWN)
        else:
            for _t in ("ld_pants_down_l", "ld_pants_down_r"):
                renpy.hide(_t)
            tv = getattr(store, "_ld_torso_variant", 2)
            renpy.show("tenny laying_pants_left", tag="ld_pants_left", at_list=slot_at, zorder=_LD_Z_LEGS + 3)
            renpy.show("tenny laying_pants_right", tag="ld_pants_right", at_list=slot_at, zorder=_LD_Z_LEGS + 4)
            renpy.show("tenny laying_pants_pelvis", tag="ld_pants_pelvis", at_list=ass_at, zorder=_LD_Z_BEFORE_ASS + 2)
            renpy.show("tenny laying_pants_ass_left", tag="ld_pants_ass_l", at_list=ass_at, zorder=_LD_Z_ASS + 2)
            renpy.show("tenny laying_pants_ass_right", tag="ld_pants_ass_r", at_list=ass_at, zorder=_LD_Z_ASS + 3)
            _t_img = "tenny laying_pants_torso_%d" % tv
            if renpy.has_image(_t_img, exact=True):
                renpy.show(_t_img, tag="ld_pants_torso", at_list=slot_at, zorder=_LD_Z_TORSO + 1)
            _ld_hide_panties()

    def _ld_show_torso(girl, slot_at):
        tv = getattr(store, "_ld_torso_variant", 1)
        av = getattr(store, "_ld_arm_variant", 2)
        if tv == 2:
            renpy.show("tenny laying_torso_2", tag="ld_torso", at_list=slot_at, zorder=_LD_Z_TORSO)
            _arm_img = "tenny laying_t2_arm_left_%d" % av
            if renpy.has_image(_arm_img, exact=True):
                renpy.show(_arm_img, tag="ld_arm_left", at_list=slot_at, zorder=_LD_Z_ARMS_BELOW)
            else:
                renpy.show("tenny laying_t2_arm_left_1", tag="ld_arm_left", at_list=slot_at, zorder=_LD_Z_ARMS_BELOW)
            renpy.hide("ld_arm_right")
        else:
            renpy.show("tenny laying_torso_1", tag="ld_torso", at_list=slot_at, zorder=_LD_Z_TORSO)
            _arm_l = "tenny laying_arm_left_%d" % av
            _arm_r = "tenny laying_arm_right_%d" % av
            if renpy.has_image(_arm_l, exact=True):
                renpy.show(_arm_l, tag="ld_arm_left", at_list=slot_at, zorder=_LD_Z_ARMS_BELOW)
            else:
                renpy.show("tenny laying_arm_left_1", tag="ld_arm_left", at_list=slot_at, zorder=_LD_Z_ARMS_BELOW)
            if renpy.has_image(_arm_r, exact=True):
                renpy.show(_arm_r, tag="ld_arm_right", at_list=slot_at, zorder=_LD_Z_ARMS_BELOW)
            else:
                renpy.show("tenny laying_arm_right_1", tag="ld_arm_right", at_list=slot_at, zorder=_LD_Z_ARMS_BELOW)

    def _ld_show_clothing(girl, slot_at):
        tv = getattr(store, "_ld_torso_variant", 1)
        av = getattr(store, "_ld_arm_variant", 2)
        _t = "t%d" % tv

        # ── Chest (bikini top, white top) ──
        _chest_item = girl.clothes.get("chest")
        if _chest_item:
            _img = "tenny laying_chest_%s_%s" % (_chest_item, _t)
            if renpy.has_image(_img, exact=True):
                renpy.show(_img, tag="ld_chest", at_list=slot_at, zorder=_LD_Z_CHEST)
            else:
                renpy.hide("ld_chest")
        else:
            renpy.hide("ld_chest")

        # ── Mid (shirt body + sleeves) ──
        _mid_item = girl.clothes.get("mid")
        if _mid_item:
            _body = "tenny laying_mid_%s_%s" % (_mid_item, _t)
            if renpy.has_image(_body, exact=True):
                renpy.show(_body, tag="ld_mid", at_list=slot_at, zorder=_LD_Z_MID)
            else:
                renpy.hide("ld_mid")
            if tv == 1:
                _arm_key = "12" if av in (1, 2) else str(av)
                _sl_l = "tenny laying_mid_%s_t1_sl_l%s" % (_mid_item, _arm_key)
                _sl_r = "tenny laying_mid_%s_t1_sl_r%s" % (_mid_item, _arm_key)
                if renpy.has_image(_sl_l, exact=True):
                    renpy.show(_sl_l, tag="ld_mid_sl_l", at_list=slot_at, zorder=_LD_Z_MID_SLEEVE)
                else:
                    renpy.hide("ld_mid_sl_l")
                if renpy.has_image(_sl_r, exact=True):
                    renpy.show(_sl_r, tag="ld_mid_sl_r", at_list=slot_at, zorder=_LD_Z_MID_SLEEVE)
                else:
                    renpy.hide("ld_mid_sl_r")
            else:
                _arm_img = "tenny laying_mid_%s_t2_arm%d" % (_mid_item, av)
                if renpy.has_image(_arm_img, exact=True):
                    renpy.show(_arm_img, tag="ld_mid_sl_l", at_list=slot_at, zorder=_LD_Z_MID_SLEEVE)
                else:
                    renpy.hide("ld_mid_sl_l")
                _mast_r = "tenny laying_mid_%s_t2_arm_mast" % _mid_item
                if getattr(store, "_ld_masturbating", False) and renpy.has_image(_mast_r, exact=True):
                    renpy.show(_mast_r, tag="ld_mid_sl_r", at_list=slot_at, zorder=_LD_Z_MID_SLEEVE)
                else:
                    renpy.hide("ld_mid_sl_r")
        else:
            for _t_tag in ("ld_mid", "ld_mid_sl_l", "ld_mid_sl_r"):
                renpy.hide(_t_tag)

        # ── Over (jacket body + sleeves) ──
        _over_item = girl.clothes.get("over")
        if _over_item:
            _body = "tenny laying_over_%s_%s" % (_over_item, _t)
            if renpy.has_image(_body, exact=True):
                renpy.show(_body, tag="ld_over", at_list=slot_at, zorder=_LD_Z_OVER)
            else:
                renpy.hide("ld_over")
            if tv == 1:
                _arm_key = "12" if av in (1, 2) else str(av)
                _sl_l = "tenny laying_over_%s_t1_sl_l%s" % (_over_item, _arm_key)
                _sl_r = "tenny laying_over_%s_t1_sl_r%s" % (_over_item, _arm_key)
                if renpy.has_image(_sl_l, exact=True):
                    renpy.show(_sl_l, tag="ld_over_sl_l", at_list=slot_at, zorder=_LD_Z_OVER_SLEEVE)
                else:
                    renpy.hide("ld_over_sl_l")
                if renpy.has_image(_sl_r, exact=True):
                    renpy.show(_sl_r, tag="ld_over_sl_r", at_list=slot_at, zorder=_LD_Z_OVER_SLEEVE)
                else:
                    renpy.hide("ld_over_sl_r")
            else:
                _arm_img = "tenny laying_over_%s_t2_arm%d" % (_over_item, av)
                if renpy.has_image(_arm_img, exact=True):
                    renpy.show(_arm_img, tag="ld_over_sl_l", at_list=slot_at, zorder=_LD_Z_OVER_SLEEVE)
                else:
                    renpy.hide("ld_over_sl_l")
                _mast_r = "tenny laying_over_%s_t2_arm_mast" % _over_item
                if getattr(store, "_ld_masturbating", False) and renpy.has_image(_mast_r, exact=True):
                    renpy.show(_mast_r, tag="ld_over_sl_r", at_list=slot_at, zorder=_LD_Z_OVER_SLEEVE)
                else:
                    renpy.hide("ld_over_sl_r")
        else:
            for _t_tag in ("ld_over", "ld_over_sl_l", "ld_over_sl_r"):
                renpy.hide(_t_tag)

    def _ld_show_ass_layers(girl, speed, ass_at):
        _had_p = getattr(store, "_ld_had_pussy", False)
        _had_a = getattr(store, "_ld_had_anal", False)
        _pussy_img = "tenny laying_after_pussy" if getattr(girl, "_ld_after_pussy", False) else "tenny laying_before_pussy"
        _after_anal = getattr(girl, "_ld_after_anal", False)
        print("[LD_ASS] after_pussy=%s after_anal=%s started=%s anal=%s pussy_img=%s" % (getattr(girl, "_ld_after_pussy", False), _after_anal, store.laying_started, store.laying_anal, _pussy_img))

        if not store.laying_started:
            renpy.show("tenny laying_ass_base_left", tag="ld_ass_left", at_list=ass_at, zorder=_LD_Z_ASS)
            renpy.show("tenny laying_ass_base_right", tag="ld_ass_right", at_list=ass_at, zorder=_LD_Z_ASS + 1)
            renpy.show(_pussy_img, tag="ld_before_pussy", at_list=ass_at, zorder=_LD_Z_BEFORE_PUSSY)
            if _after_anal:
                renpy.show("tenny laying_after_ass", tag="ld_before_ass", at_list=ass_at, zorder=_LD_Z_BEFORE_ASS)
                renpy.hide("ld_before_ass_2")
            else:
                renpy.show("tenny laying_before_ass", tag="ld_before_ass", at_list=ass_at, zorder=_LD_Z_BEFORE_ASS)
                renpy.show("tenny laying_before_ass_2", tag="ld_before_ass_2", at_list=ass_at, zorder=_LD_Z_BEFORE_ASS + 1)
            renpy.hide("ld_during")
            renpy.hide("ld_during_below")
            renpy.hide("ld_during_safe")
            return

        if store.laying_anal:
            renpy.show("tenny laying_ass_anal_left", tag="ld_ass_left", at_list=ass_at, zorder=_LD_Z_ASS)
            renpy.show("tenny laying_ass_anal_right", tag="ld_ass_right", at_list=ass_at, zorder=_LD_Z_ASS + 1)
            renpy.show(_pussy_img, tag="ld_before_pussy", at_list=ass_at, zorder=_LD_Z_BEFORE_PUSSY)
            renpy.show("tenny laying_during_anal_below", tag="ld_during_below", at_list=ass_at, zorder=_LD_Z_DURING_ANAL_BL)
            _anal_img = "tenny laying_during_anal_fast" if speed >= 3 else "tenny laying_during_anal"
            renpy.show(_anal_img, tag="ld_during", at_list=ass_at, zorder=_LD_Z_DURING_ANAL)
            renpy.show("tenny laying_during_anal_safe", tag="ld_during_safe", at_list=ass_at, zorder=_LD_Z_DURING_ANAL_SF)
            renpy.hide("ld_before_ass")
            renpy.hide("ld_before_ass_2")
        else:
            renpy.show("tenny laying_ass_vaginal_left", tag="ld_ass_left", at_list=ass_at, zorder=_LD_Z_ASS)
            renpy.show("tenny laying_ass_vaginal_right", tag="ld_ass_right", at_list=ass_at, zorder=_LD_Z_ASS + 1)
            renpy.show("tenny laying_during_pussy_below", tag="ld_during_below", at_list=ass_at, zorder=_LD_Z_DURING_BELOW)
            renpy.show("tenny laying_during_pussy", tag="ld_during", at_list=ass_at, zorder=_LD_Z_DURING)
            renpy.show("tenny laying_during_pussy_safe", tag="ld_during_safe", at_list=ass_at, zorder=_LD_Z_DURING_SAFE)
            renpy.hide("ld_before_pussy")
            if _after_anal:
                renpy.show("tenny laying_after_ass", tag="ld_before_ass", at_list=ass_at, zorder=_LD_Z_BEFORE_ASS)
                renpy.hide("ld_before_ass_2")
            else:
                renpy.show("tenny laying_before_ass", tag="ld_before_ass", at_list=ass_at, zorder=_LD_Z_BEFORE_ASS)
                renpy.show("tenny laying_before_ass_2", tag="ld_before_ass_2", at_list=ass_at, zorder=_LD_Z_BEFORE_ASS + 1)

    def _ld_show_preview(girl):
        _slot = ld_get_slot_transform(0)
        _slot_at = [_slot]
        _ass_at = [ld_get_ass_transform(0)]

        # Head (layeredimage — read from sprite_state)
        _st = sprite_state.get(girl.Id, {})
        _ld_eyes = _laying_safe(_st.get("eyes", "eyes_normal"))
        _ld_brows = _laying_safe(_st.get("brows", "brows_normal"))
        _ld_mouth = _laying_safe(_st.get("mouth", "mouth_normal"))
        _ld_blush = _attr_for_blush(girl)
        renpy.show("tenny laying %s %s %s %s" % (_ld_eyes, _ld_brows, _ld_mouth, _ld_blush), tag="tenny", at_list=_slot_at, zorder=_LD_Z_HEAD)

        # Girl legs
        renpy.show("tenny laying_legs_left", tag="ld_legs_left", at_list=_slot_at, zorder=_LD_Z_LEGS)
        renpy.show("tenny laying_legs_right", tag="ld_legs_right", at_list=_slot_at, zorder=_LD_Z_LEGS + 1)

        # Girl pelvis
        renpy.show("tenny laying_pelvis", tag="ld_pelvis", at_list=_ass_at, zorder=_LD_Z_PELVIS)

        # Torso + arms + clothing
        _ld_show_torso(girl, _slot_at)
        _ld_show_clothing(girl, _slot_at)

        # Ass layers (preview)
        _ld_show_ass_layers(girl, 0, _ass_at)

        # Butt blush (above ass, below panties)
        renpy.show("tenny laying_butt_blush", tag="ld_butt_blush", at_list=_ass_at, zorder=_LD_Z_BUTT_BLUSH)

        # Panties
        _pan_item = girl.Panties
        _legs_state = girl.clothes_state.get("skirt", "full") if girl.Legs else None
        if _pan_item and (not girl.Legs or _legs_state == "up"):
            _pan_state = girl.clothes_state.get("panties", "full")
            _pan_z = _LD_Z_PANTIES_DOWN if _pan_state == "down" else _LD_Z_PANTIES
            _pan_img = "tenny laying_panties_%s_%s" % (_pan_item, _pan_state)
            if renpy.has_image(_pan_img, exact=True):
                renpy.show(_pan_img, tag="ld_panties", at_list=_ass_at, zorder=_pan_z)
            else:
                _ld_hide_panties()
        else:
            _ld_hide_panties()

        # Pants
        _ld_show_pants(girl, _slot_at, _ass_at)

        # Cum layers (auto-update via ConditionSwitch)
        renpy.show("tenny laying_cum_vaginal", tag="ld_cum_vaginal", at_list=_ass_at, zorder=_LD_Z_CUM)
        renpy.show("tenny laying_cum_anal", tag="ld_cum_anal", at_list=_ass_at, zorder=_LD_Z_CUM)
        renpy.show("tenny laying_cum_ass", tag="ld_cum_ass", at_list=_slot_at, zorder=_LD_Z_CUM + 1)
        renpy.show("tenny laying_cum_body", tag="ld_cum_body", at_list=_slot_at, zorder=_LD_Z_CUM + 2)
        renpy.show("tenny laying_cum_face", tag="ld_cum_face", at_list=_slot_at, zorder=_LD_Z_CUM + 3)
        renpy.show("tenny laying_cum_mouth", tag="ld_cum_mouth", at_list=_slot_at, zorder=_LD_Z_CUM + 3)
        _cum = getattr(girl, "Cum", [])
        if "dripping" in _cum or "dripping_ass" in _cum:
            renpy.show("tenny laying_cum_girl", tag="ld_cum_girl", at_list=_ass_at, zorder=_LD_Z_CUM_GIRL)

        # Hide sex-specific layers
        for _t in ("ld_penis", "ld_condom",
                    "ld_guy_legs_1", "ld_guy_legs_2",
                    "ld_guy_calf_1", "ld_guy_calf_2",
                    "ld_guy_pelvis", "ld_guy_pelvis_safe",
                    "ld_mast_anim",
                    "ld_during", "ld_during_below"):
            renpy.hide(_t)


# ═══════════════════════════════════════════════════════════
# TRANSFORMS — Slot (body sway, smaller than Doggy since she's supported by bed)
# ═══════════════════════════════════════════════════════════

transform ld_cum_alpha:
    alpha 0.7

transform ld_cum_anal_offset:
    alpha 0.7
    yoffset -10

transform ld_cum_shake:
    xoffset 0 yoffset 0
    easein 0.03 xoffset 10 yoffset -6
    easeout 0.03 xoffset -8 yoffset 5
    easein 0.03 xoffset 6 yoffset -4
    easeout 0.03 xoffset -4 yoffset 2
    easein 0.02 xoffset 2 yoffset -1
    easeout 0.02 xoffset 0 yoffset 0

transform ld_slot_speed0:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 0 zoom 1.0

transform ld_slot_speed1:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 0
    block:
        pause 0.35
        ease 0.20 yoffset -1
        pause 0.25
        ease 1.20 yoffset 0
        repeat

transform ld_slot_speed2:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 0
    block:
        pause 0.08
        ease 0.10 yoffset -2
        pause 0.06
        easein 0.30 yoffset 0
        repeat

transform ld_slot_speed3:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 0
    block:
        ease 0.12 yoffset -3
        easein 0.12 yoffset 0
        repeat

transform ld_slot_speed4:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 0
    block:
        ease 0.17 yoffset -3
        easein 0.17 yoffset 0
        repeat


# ═══════════════════════════════════════════════════════════
# TRANSFORMS — Ass reaction (self-contained, synced with penis, opposite Y)
# Same cycle duration as penis transforms to stay in sync after repeat.
# ═══════════════════════════════════════════════════════════

transform ld_tongue_pos:
    pos (1100, 830)

transform ld_ass_speed0:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 0 yzoom 1.0

transform ld_ass_rub:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 0 yzoom 1.0
    block:
        pause 0.12
        ease 0.18 yoffset 12 yzoom 1.006
        pause 0.10
        easein 0.50 yoffset 0 yzoom 1.0
        repeat

transform ld_ass_speed1:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 0 yzoom 1.0
    block:
        pause 0.35
        ease 0.20 yoffset 18 yzoom 1.008
        pause 0.25
        ease 1.20 yoffset 0 yzoom 1.0
        repeat

transform ld_ass_speed2:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 0 yzoom 1.0
    block:
        pause 0.08
        ease 0.12 yoffset 32 yzoom 1.015
        pause 0.06
        easein 0.28 yoffset 0 yzoom 1.0
        repeat

transform ld_ass_speed3:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 0 yzoom 1.0
    block:
        ease 0.14 yoffset 42 yzoom 1.02
        easein 0.14 yoffset 0 yzoom 1.0
        repeat

transform ld_ass_speed4:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 0 yzoom 1.0
    block:
        ease 0.17 yoffset 50 yzoom 1.025
        easein 0.17 yoffset 0 yzoom 1.0
        repeat


# ═══════════════════════════════════════════════════════════
# TRANSFORMS — Wave test (appears on impact, travels up, fades out)
# Cycle matches penis so repeat stays synced.
# ═══════════════════════════════════════════════════════════

transform ld_wave_speed0:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 0 alpha 0.0

transform ld_wave_speed1:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 0 alpha 0.0
    block:
        pause 0.55
        alpha 1.0
        ease 0.50 yoffset -50 alpha 0.0
        yoffset 0
        pause 0.95
        repeat

transform ld_wave_speed2:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 0 alpha 0.0
    block:
        pause 0.20
        alpha 1.0
        ease 0.28 yoffset -50 alpha 0.0
        yoffset 0
        pause 0.06
        repeat

transform ld_wave_speed3:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 0 alpha 0.0
    block:
        pause 0.14
        alpha 1.0
        ease 0.14 yoffset -50 alpha 0.0
        yoffset 0
        repeat

transform ld_wave_speed4:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 0 alpha 0.0
    block:
        pause 0.17
        alpha 1.0
        ease 0.17 yoffset -50 alpha 0.0
        yoffset 0
        repeat


# ═══════════════════════════════════════════════════════════
# TRANSFORMS — Slap wave (appears on impact, travels horizontally, fades out)
# Left wave = slap came from left, wave travels left→right (positive xoffset)
# Right wave = slap came from right, wave travels right→left (negative xoffset)
# ═══════════════════════════════════════════════════════════

transform ld_slap_wave_left_in:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    xoffset 0 alpha 0.0
    pause 0.12
    alpha 1.0
    ease 0.45 xoffset 60 alpha 0.0

transform ld_slap_wave_right_in:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    xoffset 0 alpha 0.0
    pause 0.12
    alpha 1.0
    ease 0.45 xoffset -60 alpha 0.0


# ═══════════════════════════════════════════════════════════
# TRANSFORMS — Slap (hand flies in from side, pauses, flies out)
# ═══════════════════════════════════════════════════════════

transform ld_slap_right_in:
    subpixel True
    anchor (0.5, 0.5)
    xpos 1.3
    ypos 0.48
    alpha 1.0
    easein 0.08 xpos 0.52
    pause 0.15
    easeout 0.25 xpos -0.3 alpha 0.0

transform ld_slap_left_in:
    subpixel True
    anchor (0.5, 0.5)
    xpos -0.3
    ypos 0.48
    alpha 1.0
    easein 0.08 xpos 0.48
    pause 0.15
    easeout 0.25 xpos 1.3 alpha 0.0


# ═══════════════════════════════════════════════════════════
# TRANSFORMS — Penis rub (speed ~2 pace)
# ═══════════════════════════════════════════════════════════

transform ld_penis_rub:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5 ypos 1.0
    xoffset 0 yoffset 75
    block:
        pause 0.12
        ease 0.18 yoffset -15
        pause 0.10
        easein 0.50 yoffset 75
        repeat


# ═══════════════════════════════════════════════════════════
# TRANSFORMS — Penis thrust (vaginal)
# ═══════════════════════════════════════════════════════════

transform ld_penis_speed0:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5 ypos 1.0
    xoffset 0 yoffset 75

transform ld_penis_speed1:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5 ypos 1.0
    xoffset 0 yoffset 75
    block:
        pause 0.35
        ease 0.20 yoffset 45
        pause 0.25
        ease 1.20 yoffset 75
        repeat

transform ld_penis_speed2:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5 ypos 1.0
    xoffset 0 yoffset 75
    block:
        pause 0.08
        ease 0.12 yoffset -15
        pause 0.06
        easein 0.28 yoffset 75
        repeat

transform ld_penis_speed3:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5 ypos 1.0
    xoffset 0 yoffset 75
    block:
        ease 0.14 yoffset -55
        easein 0.14 yoffset 75
        repeat

transform ld_penis_speed4:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5 ypos 1.0
    xoffset 0 yoffset 30
    block:
        ease 0.17 yoffset -70
        easein 0.17 yoffset 30
        repeat

transform ld_penis_virgin_hold:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5 ypos 1.0
    xoffset 0 yoffset -15

transform ld_penis_virgin_resume:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5 ypos 1.0
    xoffset 0 yoffset -15
    easein 0.5 yoffset 75
    block:
        pause 0.08
        ease 0.12 yoffset -15
        pause 0.06
        easein 0.28 yoffset 75
        repeat


# ═══════════════════════════════════════════════════════════
# TRANSFORMS — Penis thrust (anal, slightly different offset)
# ═══════════════════════════════════════════════════════════

transform lda_penis_speed0:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5 ypos 1.0
    xoffset 0 yoffset -10

transform lda_penis_speed1:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5 ypos 1.0
    xoffset 0 yoffset -10
    block:
        pause 0.35
        ease 0.20 yoffset -40
        pause 0.25
        ease 1.20 yoffset -10
        repeat

transform lda_penis_speed2:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5 ypos 1.0
    xoffset 0 yoffset -10
    block:
        pause 0.08
        ease 0.10 yoffset -50
        pause 0.06
        easein 0.30 yoffset -10
        repeat

transform lda_penis_speed3:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5 ypos 1.0
    xoffset 0 yoffset -10
    block:
        ease 0.12 yoffset -55
        easein 0.12 yoffset -10
        repeat

transform lda_penis_speed4:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5 ypos 1.0
    xoffset 0 yoffset -25
    block:
        ease 0.17 yoffset -45
        easein 0.17 yoffset -25
        repeat


# ═══════════════════════════════════════════════════════════
# TRANSFORMS — Penis slide in/out
# ═══════════════════════════════════════════════════════════

transform ld_penis_slide_in:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5 ypos 1.0
    xoffset 0 yoffset 200
    easein 0.55 yoffset 75

transform ld_penis_slide_out:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5 ypos 1.0
    xoffset 0 yoffset 75
    easeout 0.55 yoffset 200

transform lda_penis_slide_in:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5 ypos 1.0
    xoffset 0 yoffset 100
    easein 0.55 yoffset -10

transform lda_penis_slide_out:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5 ypos 1.0
    xoffset 0 yoffset -10
    easeout 0.55 yoffset 100


# ═══════════════════════════════════════════════════════════
# TRANSFORMS — Penis cum pulse
# ═══════════════════════════════════════════════════════════

transform ld_penis_cum_pulse():
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5 ypos 1.0
    xoffset 0 yoffset 30
    yzoom 1.0
    ease 0.12 yoffset 10
    pause 0.33
    ease 0.08 yzoom 1.06
    ease 0.15 yzoom 1.0
    pause 0.27
    ease 0.08 yzoom 1.06
    ease 0.15 yzoom 1.0

transform lda_penis_cum_pulse():
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5 ypos 1.0
    xoffset 0 yoffset -10
    yzoom 1.0
    pause 0.45
    ease 0.08 yzoom 1.06
    ease 0.15 yzoom 1.0
    pause 0.27
    ease 0.08 yzoom 1.06
    ease 0.15 yzoom 1.0

# Smooth thrust to deep position during cum inside
transform ld_penis_cum_deep_thrust:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5 ypos 1.0
    xoffset 0 yoffset 10
    easein 0.3 yoffset -15

transform lda_penis_cum_deep_thrust:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5 ypos 1.0
    xoffset 0 yoffset -10
    easein 0.3 yoffset -45

# Static deep position after cum inside (penis stays buried)
transform ld_penis_cum_freeze:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5 ypos 1.0
    xoffset 0 yoffset -15

transform lda_penis_cum_freeze:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5 ypos 1.0
    xoffset 0 yoffset -45

# ═══════════════════════════════════════════════════════════
# TRANSFORMS — Player legs thrust (legs_2 yoffset synced with penis)
# ═══════════════════════════════════════════════════════════

transform ld_legs_thrust_speed0:
    yoffset 0

transform ld_legs_thrust_speed1:
    yoffset 0
    block:
        pause 0.35
        ease 0.20 yoffset -4
        pause 0.25
        ease 1.20 yoffset 0
        repeat

transform ld_legs_thrust_speed2:
    yoffset 0
    block:
        pause 0.12
        ease 0.12 yoffset -6
        pause 0.10
        easein 0.45 yoffset 0
        repeat

transform ld_legs_thrust_speed3:
    yoffset 0
    block:
        ease 0.18 yoffset -8
        easein 0.18 yoffset 0
        repeat

transform ld_legs_thrust_speed4:
    yoffset -2
    block:
        ease 0.17 yoffset -6
        easein 0.17 yoffset -2
        repeat


# ═══════════════════════════════════════════════════════════
# TRANSFORMS — Callable rotation (thigh/calf, per speed)
# ═══════════════════════════════════════════════════════════

transform ld_rot_1(px, py, a):
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    matrixanchor (px, py)
    matrixtransform RotateMatrix(0, 0, 0)
    block:
        pause 0.35
        ease 0.20 matrixtransform RotateMatrix(0, 0, a)
        pause 0.25
        ease 1.20 matrixtransform RotateMatrix(0, 0, 0)
        repeat

transform ld_rot_2(px, py, a):
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    matrixanchor (px, py)
    matrixtransform RotateMatrix(0, 0, 0)
    block:
        pause 0.08
        ease 0.12 matrixtransform RotateMatrix(0, 0, a)
        pause 0.06
        easein 0.28 matrixtransform RotateMatrix(0, 0, 0)
        repeat

transform ld_rot_3(px, py, a):
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    matrixanchor (px, py)
    matrixtransform RotateMatrix(0, 0, 0)
    block:
        ease 0.14 matrixtransform RotateMatrix(0, 0, a)
        easein 0.14 matrixtransform RotateMatrix(0, 0, 0)
        repeat

transform ld_rot_4(px, py, a):
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    matrixanchor (px, py)
    matrixtransform RotateMatrix(0, 0, 0)
    block:
        ease 0.17 matrixtransform RotateMatrix(0, 0, a)
        easein 0.17 matrixtransform RotateMatrix(0, 0, 0)
        repeat


# ═══════════════════════════════════════════════════════════
# TRANSFORMS — Guy pelvis thrust (vaginal, ~60% of penis amplitude)
# ═══════════════════════════════════════════════════════════

transform ld_guy_pelvis_speed0:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 45

transform ld_guy_pelvis_speed1:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 45
    block:
        pause 0.35
        ease 0.20 yoffset 27
        pause 0.25
        ease 1.20 yoffset 45
        repeat

transform ld_guy_pelvis_speed2:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 45
    block:
        pause 0.08
        ease 0.12 yoffset -9
        pause 0.06
        easein 0.28 yoffset 45
        repeat

transform ld_guy_pelvis_speed3:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 45
    block:
        ease 0.14 yoffset -33
        easein 0.14 yoffset 45
        repeat

transform ld_guy_pelvis_speed4:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 18
    block:
        ease 0.17 yoffset -42
        easein 0.17 yoffset 18
        repeat


# ═══════════════════════════════════════════════════════════
# TRANSFORMS — Guy pelvis thrust (anal)
# ═══════════════════════════════════════════════════════════

transform lda_guy_pelvis_speed0:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset -6

transform lda_guy_pelvis_speed1:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset -6
    block:
        pause 0.35
        ease 0.20 yoffset -24
        pause 0.25
        ease 1.20 yoffset -6
        repeat

transform lda_guy_pelvis_speed2:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset -6
    block:
        pause 0.08
        ease 0.10 yoffset -30
        pause 0.06
        easein 0.30 yoffset -6
        repeat

transform lda_guy_pelvis_speed3:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset -6
    block:
        ease 0.12 yoffset -33
        easein 0.12 yoffset -6
        repeat

transform lda_guy_pelvis_speed4:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset -15
    block:
        ease 0.17 yoffset -27
        easein 0.17 yoffset -15
        repeat


# ═══════════════════════════════════════════════════════════
# TRANSFORMS — Guy pelvis rub / slide / cum pulse
# ═══════════════════════════════════════════════════════════

transform ld_guy_pelvis_rub:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 45
    block:
        pause 0.12
        ease 0.18 yoffset -9
        pause 0.10
        easein 0.50 yoffset 45
        repeat

transform ld_guy_pelvis_slide_in:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 120
    easein 0.55 yoffset 45

transform ld_guy_pelvis_slide_out:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 45
    easeout 0.55 yoffset 120

transform lda_guy_pelvis_slide_in:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 60
    easein 0.55 yoffset -6

transform lda_guy_pelvis_slide_out:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset -6
    easeout 0.55 yoffset 60

transform ld_guy_legs_slide_in:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 100
    easein 0.55 yoffset 0

transform ld_guy_legs_slide_out:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 0
    easeout 0.55 yoffset 100

transform ld_guy_pelvis_cum_pulse:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 18
    ease 0.12 yoffset 5
    pause 0.33
    ease 0.08 yoffset 0
    ease 0.15 yoffset 18
    pause 0.27
    ease 0.08 yoffset 0
    ease 0.15 yoffset 18

transform lda_guy_pelvis_cum_pulse:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset -6
    pause 0.45
    ease 0.08 yoffset -16
    ease 0.15 yoffset -6
    pause 0.27
    ease 0.08 yoffset -16
    ease 0.15 yoffset -6

# Static deep position after cum inside (pelvis stays pressed)
transform ld_guy_pelvis_cum_freeze:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset -42

transform lda_guy_pelvis_cum_freeze:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset -27





# ═══════════════════════════════════════════════════════════
# LD_ApplySpeed — master display function
# ═══════════════════════════════════════════════════════════

label LD_ApplySpeed(girl, speed=1):

    python:
        _hide_scene_layers("laying_down")

        _is_anal = store.laying_anal
        _rub_mode = getattr(store, "laying_rub_mode", False) and not store.laying_started

        if speed >= 3 or _is_anal:
            store._ld_arm_variant = 1
        elif store._ld_pillow_active:
            store._ld_arm_variant = 3
        else:
            store._ld_arm_variant = 2

        slot_transform = ld_get_slot_transform(speed)
        if _rub_mode:
            ass_transform = ld_ass_rub
        else:
            ass_transform = ld_get_ass_transform(speed)

        _static_at = [ld_get_slot_transform(0)]
        slot_at_list = [slot_transform]
        ass_at_list = [ass_transform]

        # ── Player legs (calves, thighs — only when scene active) ──
        _show_guy_legs = store.laying_started or _rub_mode
        if _show_guy_legs:
            renpy.show("tenny laying_guy_calf_1", tag="ld_guy_calf_1", at_list=[ld_get_calf_1_transform(speed)], zorder=_LD_Z_GUY_CALF_1)
            renpy.show("tenny laying_guy_calf_2", tag="ld_guy_calf_2", at_list=[ld_get_calf_2_transform(speed)], zorder=_LD_Z_GUY_CALF_2)
            renpy.show("tenny laying_guy_legs_1", tag="ld_guy_legs_1", at_list=[ld_get_thigh_1_transform(speed)], zorder=_LD_Z_GUY_LEGS_1)
            renpy.show("tenny laying_guy_legs_2", tag="ld_guy_legs_2", at_list=[ld_get_thigh_2_transform(speed)], zorder=_LD_Z_GUY_LEGS_2)
            renpy.show("tenny laying_guy_pelvis_safe", tag="ld_guy_pelvis_safe", at_list=_static_at, zorder=_LD_Z_GUY_PELVIS_SAFE)

        # ── Girl legs (closed) ──
        renpy.show("tenny laying_legs_left", tag="ld_legs_left", at_list=slot_at_list, zorder=_LD_Z_LEGS)
        renpy.show("tenny laying_legs_right", tag="ld_legs_right", at_list=slot_at_list, zorder=_LD_Z_LEGS + 1)

        # ── Pelvis ──
        renpy.show("tenny laying_pelvis", tag="ld_pelvis", at_list=ass_at_list, zorder=_LD_Z_PELVIS)

        # ── Torso + Arms + Clothing ──
        _ld_show_torso(girl, slot_at_list)
        _ld_show_clothing(girl, slot_at_list)

        # ── Pillow (below head, Tenny only) ──
        if store._ld_pillow_active:
            renpy.show("tenny laying_green_pillow", tag="ld_pillow", at_list=slot_at_list, zorder=_LD_Z_PILLOW)
        else:
            renpy.hide("ld_pillow")

        # ── Ass layers ──
        _ld_show_ass_layers(girl, speed, ass_at_list)

        # ── Grab layers (above ass) ──
        _hand_disabled = getattr(store, "_player_hand_disabled", None)
        if _hand_disabled and not getattr(store, "_recording_active", False):
            store._player_hand_disabled = None
            _hand_disabled = None
        _slap_hide = getattr(store, "_slap_hide_hand", None)
        if store.laying_grab:
            for _side in ("left", "right"):
                _gb_img = "tenny laying_grab_%s" % _side
                _gb_tag = "ld_grab_%s" % _side
                if _hand_disabled != _side and _slap_hide != _side:
                    renpy.show(_gb_img, tag=_gb_tag, at_list=ass_at_list, zorder=_LD_Z_PANTIES + 5)
                else:
                    renpy.hide(_gb_tag)
        else:
            renpy.hide("ld_grab_left")
            renpy.hide("ld_grab_right")

        # ── Wave test (opposite Y of ass) ──
        if store.laying_started and speed >= 2:
            _wave_tf = ld_get_wave_transform(speed)
            renpy.show("tenny laying_wave_left", tag="ld_wave_left", at_list=[_wave_tf], zorder=_LD_Z_ASS + 2)
            renpy.show("tenny laying_wave_right", tag="ld_wave_right", at_list=[_wave_tf], zorder=_LD_Z_ASS + 2)
        else:
            renpy.hide("ld_wave_left")
            renpy.hide("ld_wave_right")

        # ── Butt blush (above ass, below panties — visible after spanks) ──
        renpy.show("tenny laying_butt_blush", tag="ld_butt_blush", at_list=ass_at_list, zorder=_LD_Z_BUTT_BLUSH)

        # ── Panties ──
        _pan_item = girl.Panties
        _legs_state = girl.clothes_state.get("skirt", "full") if girl.Legs else None
        if _pan_item and (not girl.Legs or _legs_state == "up"):
            _pan_state = girl.clothes_state.get("panties", "full")
            if store.laying_started and _pan_state == "full":
                _ld_hide_panties()
            else:
                _pan_z = _LD_Z_PANTIES_DOWN if _pan_state == "down" else _LD_Z_PANTIES
                _pan_img = "tenny laying_panties_%s_%s" % (_pan_item, _pan_state)
                if renpy.has_image(_pan_img, exact=True):
                    renpy.show(_pan_img, tag="ld_panties", at_list=ass_at_list, zorder=_pan_z)
                else:
                    _ld_hide_panties()
        else:
            _ld_hide_panties()

        # ── Pants ──
        _ld_show_pants(girl, slot_at_list, ass_at_list)

        # ── Penis + Guy pelvis ──
        _show_penis = store.laying_started or _rub_mode
        _pen_z = _ld_pen_z()
        if _show_penis:
            if _rub_mode:
                _penis_tf = ld_penis_rub
                _pelvis_tf = ld_guy_pelvis_rub
            elif _is_anal:
                _penis_tf = lda_get_penis_transform(speed)
                _pelvis_tf = lda_get_guy_pelvis_transform(speed)
            else:
                _penis_tf = ld_get_penis_transform(speed)
                _pelvis_tf = ld_get_guy_pelvis_transform(speed)

            _pen_img = "tenny laying_penis"
            if store.condom_active:
                _condom_img = _condom_img_tag("ld_condom")
                _penis_w = Fixed(
                    renpy.displayable(_pen_img),
                    renpy.displayable(_condom_img),
                    fit_first=True,
                )
                renpy.show("ld_penis_combined", what=_penis_w, tag="ld_penis", at_list=[_penis_tf], zorder=_pen_z)
            else:
                renpy.show(_pen_img, tag="ld_penis", at_list=[_penis_tf], zorder=_pen_z)
            renpy.hide("ld_condom")
            renpy.show("tenny laying_guy_pelvis", tag="ld_guy_pelvis", at_list=[_pelvis_tf], zorder=_LD_Z_GUY_PELVIS)
        else:
            renpy.hide("ld_penis")
            renpy.hide("ld_condom")
            renpy.hide("ld_guy_pelvis")

        # ── Head + Expressions (layeredimage — read from sprite_state) ──
        _st = sprite_state.get(girl.Id, {})
        _ld_eyes = _laying_safe(_st.get("eyes", "eyes_normal"))
        _ld_brows = _laying_safe(_st.get("brows", "brows_normal"))
        _ld_mouth = _laying_safe(_st.get("mouth", "mouth_normal"))
        _ld_blush = _attr_for_blush(girl)
        renpy.show("tenny laying %s %s %s %s" % (_ld_eyes, _ld_brows, _ld_mouth, _ld_blush), tag="tenny", at_list=slot_at_list, zorder=_LD_Z_HEAD)

        # ── Cum layers ──
        # During rub, penis is at _LD_Z_PENIS_RUB (9882) — cum on body/ass must be below it
        if _rub_mode:
            _cum_z_base = _LD_Z_PENIS_RUB - 5
        else:
            _cum_z_base = _LD_Z_CUM
        renpy.show("tenny laying_cum_vaginal", tag="ld_cum_vaginal", at_list=ass_at_list, zorder=_LD_Z_CUM_VAGINAL)
        renpy.show("tenny laying_cum_anal", tag="ld_cum_anal", at_list=ass_at_list, zorder=_cum_z_base)
        renpy.show("tenny laying_cum_ass", tag="ld_cum_ass", at_list=ass_at_list, zorder=_cum_z_base + 1)
        renpy.show("tenny laying_cum_body", tag="ld_cum_body", at_list=slot_at_list, zorder=_cum_z_base + 2)
        renpy.show("tenny laying_cum_face", tag="ld_cum_face", at_list=slot_at_list, zorder=_LD_Z_CUM + 3)
        renpy.show("tenny laying_cum_mouth", tag="ld_cum_mouth", at_list=slot_at_list, zorder=_LD_Z_CUM + 3)
        _cum = getattr(girl, "Cum", [])
        if _is_anal:
            _cum_girl_z = _LD_Z_CUM_VAGINAL
        elif _show_penis:
            _cum_girl_z = _pen_z - 1
        else:
            _cum_girl_z = _LD_Z_CUM_GIRL
        if "dripping" in _cum:
            renpy.show("tenny laying_cum_girl", tag="ld_cum_girl", at_list=ass_at_list, zorder=_cum_girl_z)

        # ── Virginity blood on penis (stays after defloration) ──
        if store._ld_blood_active and _show_penis:
            _bl_img = girl.gid + " laying_blood_penis"
            if renpy.has_image(_bl_img, exact=True):
                renpy.show(_bl_img, tag="ld_blood_penis", at_list=[_penis_tf], zorder=_pen_z + 1)

        # ── Cum layers (only without condom, or broken condom) ──
        _raw_cum = not store.condom_active or store._condom_broken
        if _raw_cum:
            _sc_inside = store._session_cum.get("inside", 0)
            if _sc_inside >= 3:
                store._ld_cum_dick_level = 2
            elif _sc_inside >= 2:
                store._ld_cum_dick_level = 1
            if store._ld_cum_dick_level > 0 and _show_penis:
                _cd_suffix = "2" if store._ld_cum_dick_level >= 2 else "1"
                _cd_img = girl.gid + " laying_cum_dick_" + _cd_suffix
                if renpy.has_image(_cd_img, exact=True):
                    renpy.show(_cd_img, tag="ld_cum_dick", at_list=[_penis_tf], zorder=_pen_z + 1)

            if "dripping" in _cum:
                _ass_at = [ld_get_ass_transform(speed)]
                renpy.show("tenny laying_cum_girl", tag="ld_cum_girl", at_list=_ass_at, zorder=_cum_girl_z)

            if store._ld_cum_dick_level >= 1 and _show_penis:
                _cc2_img = girl.gid + " laying_cum_creampie_2"
                if renpy.has_image(_cc2_img, exact=True):
                    renpy.show(_cc2_img, tag="ld_cum_creampie_2", at_list=[_penis_tf], zorder=_pen_z + 1)
            if store._ld_cum_dick_level >= 2 and _show_penis:
                _cc3_img = girl.gid + " laying_cum_creampie_3"
                if renpy.has_image(_cc3_img, exact=True):
                    renpy.show(_cc3_img, tag="ld_cum_creampie_3", at_list=[_penis_tf], zorder=_pen_z + 1)

        debug_log("[LD_APPLY] speed=%d started=%s anal=%s rub=%s" % (speed, store.laying_started, _is_anal, _rub_mode))

    return


# ═══════════════════════════════════════════════════════════
# LD_Launch — scene setup
# ═══════════════════════════════════════════════════════════

label LD_Launch(girl, from_switch=False):
    $ sub_event_reset(girl)
    $ _kill_scene_threads(keep_watchers=from_switch)
    $ stop_standing_blink(girl)

    if not from_switch:
        $ public_attention_reset()

    python:
        _hide_all_scene_layers(girl)

        _hide_non_scene_girls(girl)

        store.hiding_face = False
        store._laying_girl = girl
        if not from_switch:
            girl._prev_pose = sprite_state.get(girl.Id, {}).get("pose", "standing")
            girl._prev_slot = getattr(girl, "_current_slot", StageCenter)
        sprite_state.setdefault(girl.Id, {})["pose"] = "laying_down"
        store.laying_speed = 0
        store.laying_started = False
        store.laying_grab = False
        store._ld_had_pussy = False
        store._ld_had_anal = False
        store._ld_blood_active = False
        store._ld_cum_dick_level = 0
        store._ld_torso_variant = 1
        store._ld_arm_variant = 2
        store._ld_pillow_active = False

        renpy.start_predict(
            "tenny laying_pelvis",
            "tenny laying_ass_base_left",
            "tenny laying_ass_base_right",
            "tenny laying_ass_vaginal_left",
            "tenny laying_ass_vaginal_right",
            "tenny laying_before_pussy",
            "tenny laying_after_pussy",
            "tenny laying_before_ass",
            "tenny laying_after_ass",
            "tenny laying_during_pussy",
            "tenny laying_during_pussy_below",
            "tenny laying_during_anal",
            "tenny laying_during_anal_below",
            "tenny laying_penis",
        )

    if from_switch:
        if girl.Panties is not None:
            $ girl.Outfit_Change(panties="none", pose="laying_down")
        call LD_ApplySpeed(girl, 0) from _call_LD_ApplySpeed_launch_switch
        with dissolve
    else:
        $ set_girl_sprite(girl, pose="laying_down")
        $ _ld_show_preview(girl)
        with fade

        call _ld_bottom_clothes_menu(girl) from _call_ld_bottom_menu_launch

        call LD_ApplySpeed(girl, 0) from _call_LD_ApplySpeed_launch_init

    python:
        renpy.invoke_in_thread(_ld_blink_loop, girl)
        renpy.invoke_in_thread(_laying_expression_cycle, girl)
    return


# ═══════════════════════════════════════════════════════════
# LD_ControlMenu — main sex loop
# ═══════════════════════════════════════════════════════════

label LD_ControlMenu(girl, from_escalation=False):

    $ store._player_exhausted = False
    $ store._scene_phase = "sex"
    $ store._cheat_shower_max_act = "sex"
    $ _ld_scene_type = "laying_anal" if store.laying_anal else "laying_down"

    if not from_escalation and not store.laying_started:
        $ laying_speed = 0

    while True:
        $ _ld_scene_type = "laying_anal" if store.laying_anal else "laying_down"
        $ print("[LD_LOOP] top: energy=%d exhausted=%s Focus=%d laying_started=%s post_cum=%s pos_switched=%s Round=%d" % (Player.energy, store._player_exhausted, Player.Focus, store.laying_started, store._post_cum_pending, getattr(store, "_sub_event_position_switched", False), Round))
        if store._post_cum_pending:
            $ print("[LD_LOOP] EXIT: _post_cum_pending=True")
            return

        if getattr(store, "_sub_event_position_switched", False):
            $ print("[LD_LOOP] EXIT: _sub_event_position_switched=True")
            $ store._sub_event_position_switched = False
            return

        # Scene ended or forced out by a sub-call (force_scene_reset, hate_cum, exhaustion...)
        if _scene_should_exit() or store._laying_girl is None:
            $ print("[LD_LOOP] EXIT: scene_should_exit=%s laying_girl_none=%s" % (_scene_should_exit(), store._laying_girl is None))
            return

        if Round >= 100:
            $ Say_Line(girl, _scene_time_up_line())
            call LD_End(girl, dress_up=False) from _call_LD_End_timeout
            return

        menu:
            "Keep going" if store.laying_started:
                $ _ld_lust = _anal_lust_for_speed(girl, laying_speed) if store.laying_anal else -1

                call _sex_scene_tick(girl, _ld_scene_type, laying_speed, girl_lust=_ld_lust) from _call_sst_ld_kg

                $ _apply_anal_lust_cap(girl, store.laying_anal)

                if store._sst_result == "condom_ripped":
                    call LD_CondomRemoveAnim(girl) from _call_LD_CondomRemoveAnim_sst_kg
                    call LD_ApplySpeed(girl, laying_speed) from _call_LD_ApplySpeed_sst_rip

                if store._sst_result == "abort":
                    if store._sst_abort_reason == "post_cum":
                        $ _set_post_cum("laying_anal" if store.laying_anal else "laying_down", "sex")
                        return
                    if store._sst_abort_reason == "position_switch":
                        return
                    else:
                        call _sex_scene_handle_abort(girl, _ld_scene_type) from _call_sst_abort_ld_kg
                        return

            "Speed up" if laying_speed < 3:
                $ advance_round(TIME_COSTS["sex_tick"])
                $ laying_speed += 1
                call LD_HoleTransition(girl, store.laying_anal) from _call_LD_HoleTransition_su
                $ _moan = scene_moan_tick(girl, _ld_scene_type, laying_speed)
                if _moan:
                    call _moan_say(girl, _moan) from _call_ms_ld_kg
                if laying_speed >= 3:
                    $ set_scene_expression(girl, "pleasure_intense")
                else:
                    $ set_scene_expression(girl, "surprised")
                call LD_ApplySpeed(girl, laying_speed) from _call_LD_ApplySpeed_su
                call _speed_change_tick(girl, _ld_scene_type, 1) from _call_sct_ld_su
                if _scene_should_exit():
                    return
                if laying_speed >= 3:
                    $ _watcher_scene_comment("speed_max")

            "Slow down" if laying_speed > 1:
                $ advance_round(1)
                $ laying_speed -= 1
                $ set_scene_expression(girl, "pleasure_mild")
                call LD_ApplySpeed(girl, laying_speed) from _call_LD_ApplySpeed_sd
                call _speed_change_tick(girl, _ld_scene_type, -1) from _call_sct_ld_sd
                if store._sub_event_position_switched:
                    return
                $ _watcher_scene_comment("speed_down")

            "Penetration..." if store.laying_started:
                $ _es_from = "anal" if store.laying_anal else "sex"
                call _escalation_menu(girl, "laying_down") from _call_esc_menu_ld_sex
                if store._esc_result == "accepted":
                    call _ld_esc_dispatch(girl, _es_from, laying_speed) from _call_esc_disp_ld_sex
                    # Dispatch may have ended the scene (e.g. cheat condom breakdown on anal->pussy): LD_End clears _laying_girl
                    if store._esc_is_deescalation or store._laying_girl is None:
                        $ debug_log("[LD_LOOP] EXIT after escalation: deesc=%s scene_ended=%s" % (store._esc_is_deescalation, store._laying_girl is None))
                        return
                elif store._esc_result == "scene_ended":
                    call LD_End(girl, dress_up=False) from _call_LD_End_esc_sex
                    return

            "Grab her ass" if store.laying_started and not store.laying_grab:
                $ advance_round(1)
                $ store.laying_grab = True
                call LD_ApplySpeed(girl, laying_speed) from _call_LD_ApplySpeed_grab
                python:
                    _grab_react = renpy.random.choice(["mouth_surprised", "mouth_tongue", "mouth_kiss"])
                    set_scene_expression(girl, None, mouth=_grab_react)
                call LD_ApplySpeed(girl, laying_speed) from _call_LD_ApplySpeed_grab_react

            "Let go" if store.laying_grab:
                $ advance_round(1)
                $ store.laying_grab = False
                call LD_ApplySpeed(girl, laying_speed) from _call_LD_ApplySpeed_letgo

            "Give her a pillow" if girl.gid == "tenny" and store.laying_started and not store._ld_pillow_active and CurrentLocation in ("room", GIRL_ROOMS.get(girl.gid, "")):
                $ store._ld_pillow_active = True
                call LD_ApplySpeed(girl, laying_speed) from _call_LD_ApplySpeed_pillow_on

            "Remove pillow" if store._ld_pillow_active:
                $ store._ld_pillow_active = False
                call LD_ApplySpeed(girl, laying_speed) from _call_LD_ApplySpeed_pillow_off

            "Spank her" if store.laying_started:
                $ advance_round(1)
                call SpankHer(girl, "laying_down") from _call_SpankHer_ld

            "Tease her..." if store.laying_started and laying_speed > 0:
                $ advance_round(1)
                call _tease_menu(girl, _ld_scene_type) from _call_tease_menu_ld

            "Ask to hide her face" if store.laying_started and not store.hiding_face and not getattr(store, "_recording_active", False):
                call _ld_turn_head(girl) from _call_ld_turn_head_fwd
                call LD_ApplySpeed(girl, laying_speed) from _call_LD_ApplySpeed_turn_fwd

            "Tell her to look back" if store.hiding_face and not getattr(store, "_recording_active", False):
                $ store.hiding_face = False
                call LD_ApplySpeed(girl, laying_speed) from _call_LD_ApplySpeed_turn_back
                $ _turn_txt = _tl(_("She turns her head back to face you."))
                $ Narration(_turn_txt)
                if store._stealth_condom_removed:
                    call StealthCondomDiscovery(girl, _ld_scene_type) from _call_StealthDisc_ld_lookback

            "Record Options..." if (store.laying_started and not getattr(store, "_recording_active", False)) or (getattr(store, "_recording_active", False) and getattr(store, "_recording_girl", None) == girl):
                menu:
                    "Record her..." if not getattr(store, "_recording_active", False) and not store.hiding_face:
                        call _sex_phone_menu(girl, "laying_down") from _call__sex_phone_menu_ld
                    "Record her..." if not getattr(store, "_recording_active", False) and store.hiding_face:
                        call _sex_phone_menu(girl, "laying_down") from _call__sex_phone_menu_ld_hf
                    "Record without telling her" if not getattr(store, "_recording_active", False) and store.hiding_face:
                        call _ld_secret_recording(girl) from _call_ld_secret_recording
                    "Ask [store._ntr_watching_npc.Name] to record" if store._ntr_partner_watching and not getattr(store, "_recording_active", False):
                        call _watcher_record_start(girl, "laying_down") from _call_watcher_rec_start_ld_npc
                    "Ask [store._witness_girl.Name] to record" if getattr(store, "_witness_watching", False) and getattr(store, "_witness_girl", None) is not None and not store._ntr_partner_watching and not getattr(store, "_recording_active", False):
                        call _watcher_record_start(girl, "laying_down") from _call_watcher_rec_start_ld_girl
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
                    "Order her to look back" if getattr(store, "hiding_face", False) and getattr(store, "_recording_active", False) and not getattr(store, "_recording_face_locked", False):
                        $ store.hiding_face = False
                        call _ld_look_back_during_recording(girl) from _call_ld_look_back_rec
                    "Back":
                        pass
                if getattr(store, "_ld_secret_caught_end", False):
                    $ store._ld_secret_caught_end = False
                    call LD_End(girl, dress_up=False) from _call_LD_End_secret_caught
                    return
                call LD_ApplySpeed(girl, laying_speed) from _call_LD_ApplySpeed_rec_opts

            "Condom..." if store.condom_active and store.laying_started:
                call CondomMidsceneMenu(girl, _ld_scene_type) from _call_CondomMidsceneMenu_ld
                if not store.condom_active:
                    call LD_CondomRemoveAnim(girl) from _call_LD_CondomRemoveAnim_mid
                    call LD_ApplySpeed(girl, laying_speed) from _call_LD_ApplySpeed_condom_rm

            "Switch position..." if store.laying_started and not getattr(store, "_scene_restricted", False):
                if store._condom_broken_hidden:
                    call CondomBreakDiscovery(girl, _ld_scene_type) from _call_CondomBreakDisc_ld
                if store._stealth_condom_removed:
                    call StealthCondomDiscovery(girl, _ld_scene_type) from _call_StealthDisc_ld
                # Discovery may have ended the scene (force_scene_reset): don't offer the switch
                if _scene_should_exit() or store._laying_girl is None:
                    return
                menu:
                    "Full Nelson" if girl_has_pose(girl, "full_nelson"):
                        $ Say_Player(_("Let me pick you up..."))
                        # Carry the current hole into the next pose (anal stays anal)
                        $ _switch_anal = store.laying_anal
                        python:
                            _switch_lines = [
                                _("You're picking me up? Okay...!"),

                                _("Mmm, hold me up then."),

                                _("Sure... lift me."),

                            ]
                        $ Say_Line(girl, _tl(renpy.random.choice(_switch_lines)))

                        $ _saved_condom = condom_carry_save()
                        python:
                            store._laying_girl = None
                            store.laying_started = False
                            store.laying_anal = False
                            store.laying_rub_mode = False
                            store.laying_tip_mode = False
                            store.laying_grab = False
                            store._ld_masturbating = False
                            store._ld_mast_t0 = None
                            store.hiding_face = False
                            _ld_hide_all_layers()
                            hide_girl_sprite(girl)
                            store.condom_active = False
                        $ condom_carry_restore(_saved_condom)

                        $ fn_speed = 0
                        $ store.fn_anal = _switch_anal
                        $ debug_log("[SWITCH] LD->FN carry anal=%s" % store.fn_anal)
                        $ _scene_position_switch(girl, "laying_down", "full_nelson", anal=getattr(store, "fn_anal", False))   # player switch: count the new position (and sex, if it is vaginal now)
                        call FN_Launch(girl, from_switch=True) from _call_FN_Launch_ld_switch
                        call FN_ControlMenu(girl) from _call_FN_ControlMenu_ld_switch

                        $ store._sub_event_position_switched = True

                    "Back":
                        pass

            "Strip her..." if not getattr(store, "_scene_restricted", False):
                call _ld_strip_menu(girl) from _call_ld_strip_sex
                call LD_ApplySpeed(girl, laying_speed) from _call_LD_ApplySpeed_strip

            "Clean up" if store._ld_blood_active or getattr(girl, "Cum", []):
                python:
                    print("[LD_CLEANUP] before: blood=%s cum=%s dick_level=%d session_cum=%s" % (store._ld_blood_active, getattr(girl, "Cum", []), store._ld_cum_dick_level, store._session_cum))
                    girl.Cum = []
                    girl._mouth_cum_persist = False
                    store._ld_blood_active = False
                    store._ld_cum_dick_level = 0
                    store._forced_creampie_count = 0
                    store._session_cum = {}
                call LD_ApplySpeed(girl, laying_speed) from _call_LD_ApplySpeed_cleanup

            "{color=#fbbf24}Cum{/color}" if player_is_cumming():
                call PlayerCumMenu(girl, _ld_scene_type) from _call_PlayerCumMenu_voluntary_ld
                $ _handle_post_cum_exit("laying_anal" if store.laying_anal else "laying_down", "sex")
                return

            "Stop now" if store.laying_started:
                if store._forced_creampie_end_after_orgasm:
                    call _player_stops_after_forced_creampie(girl, _ld_scene_type) from _call__player_stops_forced_ld
                $ debug_log("[DEBUG] Ask her to stop (LD): Lust=%d speed=%d" % (girl.Lust, laying_speed))
                $ store._edge_lust_check = (girl.Lust >= 80)
                if store._edge_lust_check:
                    $ debug_log("[DEBUG] Lust >= 80, entering EdgeDenial")
                    # She begs with him still in her: the scene stays exactly as it is until the action really stops.
                    # "Keep going" goes on at the same speed, her "No, stop." is the same stop as below (the freeze
                    # comes then) (author, 2026-10-09)
                    call EdgeDenial(girl, _ld_scene_type) from _call_EdgeDenial_ld
                    if girl.Lust >= 100:
                        call GirlCumming(girl, _ld_scene_type, _ld_scene_type) from _call_GirlCumming_ld_edge
                    if store._edge_scene_ended:
                        $ store._edge_scene_ended = False
                        $ laying_speed = 0
                        call LD_ApplySpeed(girl, 0) from _call_LD_ApplySpeed_edge
                        $ Say_Line(girl, _tl(_("Alright...")))
                        $ print("[LD_FLOW] EDGE STOP path, Cum=%s" % getattr(girl, "Cum", []))
                        call _cum_dispatch_aftermath(girl, "laying_anal" if store.laying_anal else "laying_down") from _call_ca_dispatch_ld_edge_stop
                        return
                else:
                    $ debug_log("[DEBUG] Lust < 80, ending scene normally")
                    $ laying_speed = 0
                    call LD_ApplySpeed(girl, 0) from _call_LD_ApplySpeed_stop_freeze
                    $ Say_Line(girl, _tl(_("Alright...")))
                    $ print("[LD_FLOW] NORMAL STOP path, Cum=%s" % getattr(girl, "Cum", []))
                    call _cum_dispatch_aftermath(girl, "laying_anal" if store.laying_anal else "laying_down") from _call_ca_dispatch_ld_stop
                    return


# ═══════════════════════════════════════════════════════════
# LD_StripMenu — clothing removal during sex
# ═══════════════════════════════════════════════════════════

label _ld_bottom_clothes_menu(girl):
    python:
        _has_pants = girl.Legs is not None
        _has_panties = girl.Panties is not None and girl.clothes_state.get("panties") == "full"
        print("[LD_BOTTOM_MENU] ENTER gid=%s has_pants=%s has_panties=%s panties_state=%s restricted=%s" % (girl.gid, _has_pants, _has_panties, girl.clothes_state.get("panties", "??"), getattr(store, "_scene_restricted", False)))

    if not _has_pants and not _has_panties:
        $ print("[LD_BOTTOM_MENU] SKIP: no pants, no panties")
        return

    python:
        # "sex" + "anal" scenes. The old read was always 0: "sex_acts" is not an attribute (it is Sex_acts)
        # and "laying_down" is a position, never a Sex_acts key.
        _total_sex = girl_act_counts(girl)[0]
        _is_virgin = girl.has_trait("virgin")

        if _is_virgin:
            set_scene_expression(girl, "scared", pose="laying_down", blush=2)
            _ready_lines = [
                _("I... I've never done this before. Be gentle, okay?"),
                _("My heart is pounding... just... go slow."),
                _("I'm nervous... but I trust you."),
            ]
        elif _total_sex <= SEX_HISTORY_THRESHOLDS["ld_inexperienced_sex"]:
            set_scene_expression(girl, "embarrassed", pose="laying_down", blush=1)
            _ready_lines = [
                _("Here... let me get ready for you."),
                _("Hold on... let me fix this first."),
                _("Just a second..."),
            ]
        elif girl.has_trait("hardcore_sex"):
            set_scene_expression(girl, "lusty", pose="laying_down")
            _ready_lines = [
                _("Hurry up already."),
                _("Stop stalling and get to it."),
                _("Come on. We both know what we want."),
            ]
        elif girl.has_trait("cum_slut"):
            set_scene_expression(girl, "sexy", pose="laying_down", blush=1)
            _ready_lines = [
                _("Mmm... I've been thinking about this."),
                _("I can already feel my heart racing..."),
                _("Don't keep me waiting..."),
            ]
        elif girl.has_trait("cute_sex"):
            set_scene_expression(girl, "smile", pose="laying_down", blush=1)
            _ready_lines = [
                _("Take your time... there's no rush."),
                _("Come closer... I want to feel you near me."),
                _("Be sweet to me, okay?"),
            ]
        else:
            _expr = renpy.random.choice(["shy", "smile", "embarrassed"])
            set_scene_expression(girl, _expr, pose="laying_down")
            _ready_lines = [
                _("Here... let me get ready for you."),
                _("Hold on... let me fix this first."),
                _("Just a second..."),
                _("Ready when you are."),
                _("Okay... let's do this."),
            ]
    $ Say_Line(girl, _tl(renpy.random.choice(_ready_lines)))

    if _has_pants:
        menu:
            "Remove pants":
                $ girl.clothes["skirt"] = None
                $ girl.clothes_state["skirt"] = "full"
            "Pull pants down":
                $ girl.clothes_state["skirt"] = "up"
        call LD_ApplySpeed(girl, laying_speed) from _call_LD_ApplySpeed_btm_pants
        pause 0.3

    python:
        _pants_down = girl.Legs and girl.clothes_state.get("skirt") == "up"
        _has_panties = girl.Panties is not None and girl.clothes_state.get("panties") == "full"
    if _has_panties and (not girl.Legs or _pants_down):
        menu:
            "Pull panties to the side":
                $ girl.clothes_state["panties"] = "side"
                $ print("[LD_BOTTOM_MENU] Selected: panties to the side")
            "Pull panties down":
                $ girl.clothes_state["panties"] = "down"
                $ print("[LD_BOTTOM_MENU] Selected: panties down")
            "Remove panties" if not _pants_down:
                $ girl.clothes["panties"] = None
                $ girl.clothes_state["panties"] = "full"
                $ print("[LD_BOTTOM_MENU] Selected: remove panties")
        call LD_ApplySpeed(girl, laying_speed) from _call_LD_ApplySpeed_btm_panties

    $ print("[LD_BOTTOM_MENU] EXIT: panties_state=%s exhausted=%s post_cum=%s" % (girl.clothes_state.get("panties", "??"), store._player_exhausted, store._post_cum_pending))
    call CheckExposure(girl) from _call_CheckExposure_btm_ld
    return

label _ld_strip_top_menu(girl):
    menu:
        "Remove jacket" if girl.clothes.get("over"):
            $ girl.clothes["over"] = None
        "Remove shirt" if girl.clothes.get("mid"):
            $ girl.clothes["mid"] = None
        "Remove top" if girl.clothes.get("chest"):
            $ girl.clothes["chest"] = None
        "Never mind":
            pass
    return

label _ld_strip_menu(girl):
    python:
        _has_over = girl.clothes.get("over") is not None
        _has_mid = girl.clothes.get("mid") is not None and not _has_over
        _has_chest = girl.clothes.get("chest") is not None and not _has_over and not girl.clothes.get("mid")
        _masting = getattr(store, "_ld_masturbating", False)
        _has_pants_full = not _masting and girl.Legs is not None and girl.clothes_state.get("skirt", "full") == "full"
        _has_pants_down = not _masting and girl.Legs is not None and girl.clothes_state.get("skirt") == "up"
        _pan_state = girl.clothes_state.get("panties", "full")
        _panties_accessible = _masting or not girl.Legs or _has_pants_down or girl.clothes_state.get("skirt") != "full"
        _has_panties_full = girl.Panties is not None and _pan_state == "full" and _panties_accessible
        _has_panties_moved = girl.Panties is not None and _pan_state in ("side", "down") and _panties_accessible
        _can_remove_panties = girl.Panties is not None and _panties_accessible
        print("[LD_STRIP_MENU] ENTER gid=%s over=%s mid=%s chest=%s pants_full=%s pants_down=%s panties_full=%s panties_moved=%s restricted=%s" % (girl.gid, _has_over, _has_mid, _has_chest, _has_pants_full, _has_pants_down, _has_panties_full, _has_panties_moved, getattr(store, "_scene_restricted", False)))

    menu:
        "Remove jacket" if _has_over:
            $ girl.clothes["over"] = None
        "Remove shirt" if _has_mid:
            $ girl.clothes["mid"] = None
        "Remove top" if _has_chest:
            $ girl.clothes["chest"] = None
        "Remove pants" if _has_pants_full or _has_pants_down:
            $ girl.clothes["skirt"] = None
            $ girl.clothes_state["skirt"] = "full"
        "Pull pants down" if _has_pants_full:
            $ girl.clothes_state["skirt"] = "up"
        "Pull panties to the side" if _has_panties_full:
            $ girl.clothes_state["panties"] = "side"
            $ print("[LD_STRIP_MENU] Selected: panties to the side")
        "Pull panties down" if _has_panties_full:
            $ girl.clothes_state["panties"] = "down"
            $ print("[LD_STRIP_MENU] Selected: panties down")
        "Remove panties" if _can_remove_panties:
            $ girl.clothes["panties"] = None
            $ girl.clothes_state["panties"] = "full"
            $ print("[LD_STRIP_MENU] Selected: remove panties")
        "Back":
            $ print("[LD_STRIP_MENU] Selected: Back")
            return

    $ print("[LD_STRIP_MENU] EXIT: panties_state=%s exhausted=%s post_cum=%s" % (girl.clothes_state.get("panties", "??"), store._player_exhausted, store._post_cum_pending))
    call LD_ApplySpeed(girl, laying_speed) from _call_LD_ApplySpeed_strip_refresh
    call CheckExposure(girl) from _call_CheckExposure_strip_ld
    return


# ═══════════════════════════════════════════════════════════
# _ld_virgin_blood_postscene — blood animation after first virginity loss
# ═══════════════════════════════════════════════════════════

label _ld_virgin_blood_postscene(girl):
    if not getattr(store, "_virgin_blood_postscene", False):
        return
    $ store._virgin_blood_postscene = False
    $ laying_speed = 0
    call LD_ApplySpeed(girl, 0) from _call_LD_ApplySpeed_blood_post_lbl
    python:
        for _tag in ("ld_penis", "ld_condom", "ld_guy_pelvis", "ld_guy_pelvis_safe",
                     "ld_guy_calf_1", "ld_guy_calf_2", "ld_guy_legs_1", "ld_guy_legs_2",
                     "ld_blood_penis", "ld_grab_left", "ld_grab_right",
                     "ld_cum_dick", "ld_cum_creampie_2", "ld_cum_creampie_3",
                     "ld_during", "ld_during_below", "ld_during_safe"):
            renpy.hide(_tag)
        _ass_at = [ld_get_ass_transform(0)]
        if store.laying_anal:
            renpy.show("tenny laying_ass_base_left", tag="ld_ass_left", at_list=_ass_at, zorder=_LD_Z_ASS)
            renpy.show("tenny laying_ass_base_right", tag="ld_ass_right", at_list=_ass_at, zorder=_LD_Z_ASS + 1)
            renpy.show("tenny laying_after_ass", tag="ld_before_ass", at_list=_ass_at, zorder=_LD_Z_BEFORE_ASS)
            renpy.hide("ld_before_ass_2")
        else:
            renpy.show("tenny laying_after_pussy", tag="ld_before_pussy", at_list=_ass_at, zorder=_LD_Z_BEFORE_PUSSY)
        _cum = getattr(girl, "Cum", [])
        _cum_at = _ass_at + [ld_cum_alpha]
        if "dripping_ass" in _cum:
            _cum_anal_at = _ass_at + [ld_cum_anal_offset]
            renpy.show("tenny laying_cum_anal", tag="ld_cum_anal", at_list=_cum_anal_at, zorder=_LD_Z_CUM)
        if "dripping" in _cum:
            renpy.show("tenny laying_cum_vaginal", tag="ld_cum_vaginal", at_list=_cum_at, zorder=_LD_Z_CUM_VAGINAL)
            renpy.show("tenny laying_cum_girl", tag="ld_cum_girl", at_list=_cum_at, zorder=_LD_Z_CUM_GIRL)
        _blood_img = girl.gid + " laying_blood_anim"
        if renpy.has_image(_blood_img, exact=True):
            renpy.show(_blood_img, tag="ld_blood_anim", at_list=_ass_at, zorder=_LD_Z_PENIS_VAG + 1)
    $ renpy.pause(3.0, hard=True)
    return


# LD_End — cleanup
# ═══════════════════════════════════════════════════════════

label LD_End(girl, dress_up=True):
    $ debug_log("[DEBUG] LD_End: entered, dress_up=%s" % str(dress_up))
    $ store._last_scene_was_anal = store.laying_anal
    if store.laying_anal:
        $ store._atm_source_gid = girl.gid
    $ scene_full_cleanup(girl)
    $ finalize_recording()
    $ _player_cleanup(girl)

    $ pose = getattr(girl, "_prev_pose", "standing")
    $ slot = _safe_restore_slot(getattr(girl, "_prev_slot", StageCenter))

    python:
        slot_transform = _slot_to_transform(slot)
        _reset_expression_state(girl)

        store._laying_girl = None
        store.laying_blink = False
        store.laying_started = False
        store.laying_anal = False
        store.laying_rub_mode = False
        store.laying_tip_mode = False
        store.laying_grab = False
        store._ld_masturbating = False
        store._ld_mast_t0 = None
        store.hiding_face = False
        girl.ResetVisuals(pose=pose, at_list=[slot_transform])
        _ld_hide_all_layers()
        store.condom_active = False

    if dress_up:
        call DressUp_Sequence(girl) from _call_DressUp_Sequence_ld
    return


# ═══════════════════════════════════════════════════════════
# LD_RubLaunch — rub mode (penis visible, no penetration)
# ═══════════════════════════════════════════════════════════

label LD_RubLaunch(girl):
    $ sub_event_reset(girl)

    $ public_attention_reset()
    call PlayerExposure(girl) from _call_PlayerExposure_ld_rub

    $ girl._prev_pose = getattr(girl, "default_pose", "standing")
    $ girl._prev_slot = getattr(girl, "SpriteLoc", StageCenter)
    if not getattr(girl, "_saved_outfit", None):
        $ girl.SaveOutfit()

    python:
        _kill_scene_threads()
        stop_standing_blink(girl)

        _hide_all_scene_layers(girl)

        _hide_non_scene_girls(girl)

        store._laying_girl = girl
        sprite_state.setdefault(girl.Id, {})["pose"] = "laying_down"
        store.laying_speed = 0
        store.laying_started = False
        store.laying_grab = False
        store.laying_rub_mode = True
        store.laying_tip_mode = False
        store.laying_anal = False
        store._ld_had_pussy = False
        store._ld_had_anal = False
        store._ld_blood_active = False
        store._ld_cum_dick_level = 0
        store._ld_torso_variant = 1
        store._ld_arm_variant = 2
        store._ld_pillow_active = False

    $ set_girl_sprite(girl, pose="laying_down")
    $ _ld_show_preview(girl)
    with fade

    python:
        _total_sex = girl_act_counts(girl)[0]   # "sex" + "anal" scenes (old read of "sex_acts"/"laying_down" was always 0)
        if girl.has_trait("virgin"):
            set_scene_expression(girl, "nervous", pose="laying_down", blush=1)
        elif _total_sex <= SEX_HISTORY_THRESHOLDS["ld_inexperienced_sex"]:
            set_scene_expression(girl, "shy", pose="laying_down")
        elif girl.has_trait("hardcore_sex"):
            set_scene_expression(girl, "lusty", pose="laying_down")
        elif girl.has_trait("cum_slut"):
            set_scene_expression(girl, "sexy", pose="laying_down", blush=1)
        else:
            set_scene_expression(girl, renpy.random.choice(["shy", "smile", "embarrassed"]), pose="laying_down")

    python:
        renpy.invoke_in_thread(_ld_blink_loop, girl)
        renpy.invoke_in_thread(_laying_expression_cycle, girl)
    return


# ═══════════════════════════════════════════════════════════
# _ld_esc_dispatch — visual transitions after _escalation_menu
# Handles state vars, condom, visuals, and enters the next menu
# ═══════════════════════════════════════════════════════════
label _ld_esc_dispatch(girl, from_state, current_speed):
    if store._esc_result != "accepted":
        return

    # ── De-escalation ──────────────────────────────────────
    if store._esc_is_deescalation:
        if store._esc_target == "rub":
            python:
                store.laying_rub_mode = True
                store.laying_tip_mode = False
                store.laying_started = False
                store.laying_anal = False
            call LD_ApplySpeed(girl, 0) from _call_LD_ApplySpeed_deesc_rub
            call LD_RubControlMenu(girl) from _call_LD_RubCM_deesc
            return
        elif store._esc_target == "tip":
            $ store.laying_tip_mode = True
            call LD_ApplySpeed(girl, 1) from _call_LD_ApplySpeed_deesc_tip
            call LD_TipControlMenu(girl) from _call_LD_TipCM_deesc
            return
        elif store._esc_target == "sex":
            python:
                store.laying_anal = False
                store.laying_tip_mode = False
            $ _ld_scene_type = "laying_down"
            call LD_HoleTransition(girl, False) from _call_LD_HoleT_deesc_sex
            call LD_ApplySpeed(girl, current_speed) from _call_LD_ApplySpeed_deesc_sex
            return
        return

    # ── Tip (from rub) ─────────────────────────────────────
    if store._esc_target == "tip":
        $ store.laying_anal = store._esc_anal_choice
        call LD_ApplySpeed(girl, 0) from _call_LD_ApplySpeed_esc_tip_prep
        call _ld_bottom_clothes_menu(girl) from _call_ld_bottom_esc_tip
        python:
            store.laying_rub_mode = False
            store.laying_tip_mode = True
        call LD_HoleTransition(girl, store.laying_anal) from _call_LD_HoleT_esc_tip
        call LD_ApplySpeed(girl, 1) from _call_LD_ApplySpeed_esc_tip

        if store._esc_was_forced:
            $ Say_Line(girl, _esc_pick_line(girl, _ESC_TIP_FORCE_ACCEPT))
            $ Say_Player(_("It's just the tip, I promise..."))
            $ Say_Line(girl, _tl(renpy.random.choice(_ESC_TIP_FORCE_REACT)))

        call LD_TipControlMenu(girl) from _call_LD_TipCM_esc_tip
        return

    # ── Sex escalation (from rub or tip) ───────────────────
    if store._esc_target == "sex" and from_state != "anal":
        python:
            _from_tip = (from_state == "tip")
            store.laying_anal = False

        if not _from_tip:
            call _ld_bottom_clothes_menu(girl) from _call_ld_bottom_esc_sex

        python:
            store.laying_rub_mode = False
            store.laying_tip_mode = False
            store._saved_ld_started = store.laying_started
            store.laying_started = False
        call LD_ApplySpeed(girl, 0) from _call_LD_ApplySpeed_rest_esc_sex

        if store._esc_was_forced:
            if _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False):
                call condom_check(girl, True, "hard_deny") from _call_condom_esc_ld_sex_f_cheat
                if store.condom_denied:
                    $ store.laying_started = store._saved_ld_started
                    call LD_End(girl, dress_up=False) from _call_LD_End_esc_sex_f_cond
                    call _cheat_no_condom_breakdown(girl) from _call_condom_snap_esc_ld_sex_f
                    return
            else:
                # She refuses raw: decide it NOW, before the act is counted and before a virgin loses it
                if not getattr(store, "_esc_skip_condom", False) and not _force_raw_accepts(girl):
                    call force_raw(girl) from _call_force_raw_esc_ld_sex_pre
                    if store.condom_denied:
                        $ store.laying_started = store._saved_ld_started
                        call LD_End(girl, dress_up=False) from _call_LD_End_esc_sex_f_deny_pre
                        return
                # Defer force_raw until after visual transition (penis visible during dialogue)
                python:
                    store.condom_active = False
                    store.condom_denied = False
                    store._force_raw_pending = True
        else:
            if _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False):
                call condom_check(girl, True, "hard_deny") from _call_condom_esc_ld_sex_a_cheat
            else:
                $ _pen = store._esc_pen_result
                call condom_check(girl, _pen["condom_required"], _pen["raw_outcome"]) from _call_condom_esc_ld_sex_a
            if store.condom_denied:
                if _is_on_cheat_path(girl):
                    $ store.laying_started = store._saved_ld_started
                    call LD_End(girl, dress_up=False) from _call_LD_End_esc_sex_a_cond
                    call _cheat_no_condom_breakdown(girl) from _call_condom_snap_esc_ld_sex_a
                    return
                python:
                    store.laying_rub_mode = (from_state == "rub")
                    store.laying_tip_mode = _from_tip
                    store.laying_started = store._saved_ld_started
                call LD_ApplySpeed(girl, current_speed) from _call_LD_ApplySpeed_esc_sex_cond_deny
                return

        $ store.laying_started = store._saved_ld_started
        if not store.condom_denied:
            $ _scene_escalation(girl, "sex", "laying_down")
            $ _had_condom_esc = store.condom_active
            python:
                store.laying_rub_mode = False
                store.laying_tip_mode = False
            $ _ld_scene_type = "laying_down"
            call LD_HoleTransition(girl, False) from _call_LD_HoleT_esc_sex
            if store._esc_virgin_check:
                call virgin_first_time(girl, "laying_down") from _call_virgin_esc_ld_sex
            $ laying_speed = store._esc_speed
            call LD_ApplySpeed(girl, laying_speed) from _call_LD_ApplySpeed_esc_sex_go

            # ── Deferred force_raw — penis now visible ──
            if getattr(store, "_force_raw_pending", False):
                $ store._force_raw_pending = False
                call force_raw(girl) from _call_force_raw_esc_ld_sex
                if store.condom_denied:
                    call LD_End(girl, dress_up=False) from _call_LD_End_esc_sex_f_deny
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

            call LD_ControlMenu(girl, from_escalation=True) from _call_LD_CM_esc_sex
            if not _had_condom_esc and not store._condom_removed_midscene and not getattr(store, "_sub_event_position_switched", False):
                python:
                    _track_raw_sex_start(girl)
        return

    # ── Sex from anal (hole switch) ────────────────────────
    if store._esc_target == "sex" and from_state == "anal":
        python:
            _atp_outcome = store._esc_atp_result.get("outcome", "accept_raw") if store._esc_atp_result else "accept_raw"

        if _atp_outcome == "require_condom":
            if store._esc_was_forced:
                $ Say_Line(girl, _atp_switch_line(girl, forced=True))   # pools: _ATP_SWITCH_LINES (escalation.rpy)
            else:
                $ Say_Line(girl, _atp_switch_line(girl))

            $ store._saved_ld_started = store.laying_started
            $ store.laying_started = False
            call LD_ApplySpeed(girl, 0) from _call_LD_ApplySpeed_rest_sw_atp
            call condom_check(girl, True, "hard_deny") from _call_condom_sw_ld_atp
            $ store.laying_started = store._saved_ld_started
            if store.condom_denied:
                call LD_ApplySpeed(girl, current_speed) from _call_LD_ApplySpeed_sw_atp_deny
                return

        if _atp_outcome == "accept_raw" and _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False):
            $ store._saved_ld_started = store.laying_started
            $ store.laying_started = False
            call LD_ApplySpeed(girl, 0) from _call_LD_ApplySpeed_rest_sw_cheat
            call condom_check(girl, True, "hard_deny") from _call_condom_sw_ld_cheat
            $ store.laying_started = store._saved_ld_started
            if store.condom_denied:
                call LD_End(girl, dress_up=False) from _call_LD_End_sw_cheat
                call _cheat_no_condom_breakdown(girl) from _call_condom_snap_sw_ld_cheat
                return

        if store._esc_was_forced:
            $ set_scene_expression(girl, "surprised")
            python:
                _sw_pre = [
                    _("Wait, you're switching..."),
                    _("H-hey, that's a different..."),
                    _("Hold on, you're pulling out and..."),
                ]
            $ Say_Line(girl, _tl(renpy.random.choice(_sw_pre)))

        $ _scene_position_switch(girl, "anal", "laying_down")
        if store._esc_was_forced:
            $ sex_accept_with_temptation(girl, "sex")
            $ Change_Status(girl, "Obed", 3)
            $ Change_Status(girl, "Inbt", 3)
        else:
            if _is_on_cheat_path(girl) and _cheat_stage(girl) < 3:
                $ Say_Line(girl, _cheat_sex_first_line(girl))
            else:
                python:
                    if girl.has_trait("hardcore_sex"):
                        _sw_ask_pool = [
                            _("From my ass to my pussy? Dirty. I like it. Go ahead."),
                            _("You want to switch? Fine, shove it in."),
                        ]
                    elif girl.has_trait("cum_slut"):
                        _sw_ask_pool = [
                            _("Mmm, switch wherever you want... I just want you inside me."),
                            _("My pussy, my ass, I don't care... just don't stop."),
                        ]
                    else:
                        _sw_ask_pool = [
                            _("Mmm... okay. Switch to my pussy."),
                            _("You want to switch? Sure... put it in."),
                        ]
                $ Say_Line(girl, _tl(renpy.random.choice(_sw_ask_pool)))

        $ _ld_scene_type = "laying_down"
        call LD_HoleTransition(girl, False) from _call_LD_HoleT_sw_a2p
        call LD_ApplySpeed(girl, current_speed) from _call_LD_ApplySpeed_sw_a2p

        if store._esc_was_forced:
            python:
                _sw_post = [
                    _("Ah! You switched! ...mmm..."),
                    _("You could have asked... but don't stop."),
                ]
            $ Say_Line(girl, _tl(renpy.random.choice(_sw_post)))
        return

    # ── Anal escalation (from rub or tip) ──────────────────
    if store._esc_target == "anal" and from_state != "sex":
        if from_state == "rub":
            call _ld_bottom_clothes_menu(girl) from _call_ld_bottom_esc_anal
        python:
            store.laying_rub_mode = False
            store.laying_tip_mode = False
            store.laying_anal = True
            store.condom_active = False
            store.condom_denied = False
        $ _scene_escalation(girl, "anal", "laying_down")
        $ _ld_scene_type = "laying_anal"
        call LD_HoleTransition(girl, True) from _call_LD_HoleT_esc_anal
        $ laying_speed = store._esc_speed
        call LD_ApplySpeed(girl, laying_speed) from _call_LD_ApplySpeed_esc_anal

        if store._esc_was_forced:
            python:
                _post_lines = [
                    _("Ah! You just... put it in my ass... oh fuck..."),
                    _("W-wait! That's my ASS! Oh god..."),
                    _("You didn't even ask! ...ngh... it's so tight..."),
                ]
            $ Say_Line(girl, _tl(renpy.random.choice(_post_lines)))

        call LD_ControlMenu(girl, from_escalation=True) from _call_LD_CM_esc_anal
        if not getattr(store, "_sub_event_position_switched", False):
            python:
                _track_raw_sex_start(girl)
        return

    # ── Anal from sex (hole switch) ────────────────────────
    if store._esc_target == "anal" and from_state == "sex":
        if store._esc_was_forced:
            $ set_scene_expression(girl, "surprised")
            call LD_ApplySpeed(girl, current_speed) from _call_LD_ApplySpeed_sw_fa_pre
            python:
                _sw_pre = [
                    _("Wait, that's my..."),
                    _("H-hey! Wrong hole!"),
                    _("Hold on, that's not my..."),
                ]
            $ Say_Line(girl, _tl(renpy.random.choice(_sw_pre)))
            $ _scene_position_switch(girl, "laying_down", "anal")
            $ mark_intimacy(girl, "anal")
            $ sex_accept_with_temptation(girl, "anal")
        else:
            $ _scene_position_switch(girl, "laying_down", "anal")
            $ mark_intimacy(girl, "anal")

        $ Change_Status(girl, "Obed", 8)
        $ Change_Status(girl, "Inbt", 5)
        python:
            store.condom_active = False
            store.condom_denied = False
        $ _ld_scene_type = "laying_anal"
        call LD_HoleTransition(girl, True) from _call_LD_HoleT_sw_p2a
        call LD_ApplySpeed(girl, current_speed) from _call_LD_ApplySpeed_sw_p2a

        if store._esc_was_forced:
            python:
                _sw_post = [
                    _("AH! That's my ass! ...oh god..."),
                    _("You just switched holes! ...mmm..."),
                    _("Hey! That's... oh... don't stop..."),
                ]
            $ Say_Line(girl, _tl(renpy.random.choice(_sw_post)))
        return

    return


# ═══════════════════════════════════════════════════════════
# LD_RubControlMenu — rub game loop
# ═══════════════════════════════════════════════════════════

label LD_RubControlMenu(girl):

    $ store._scene_phase = "rub"
    $ laying_speed = 0
    $ print("[LD_RUB_MENU] ENTER gid=%s restricted=%s exhausted=%s energy=%d" % (girl.gid, getattr(store, "_scene_restricted", False), store._player_exhausted, Player.energy))
    call LD_ApplySpeed(girl, 0) from _call_LD_ApplySpeed_rub_entry

    while True:
        $ print("[LD_RUB_MENU] LOOP TOP: sub_event=%s exhausted=%s post_cum=%s Round=%s" % (getattr(store, "_sub_event_position_switched", False), store._player_exhausted, store._post_cum_pending, Round))
        if _scene_should_exit():
            $ print("[LD_RUB_MENU] EXIT: _scene_should_exit()")
            return

        if Round >= 100:
            $ print("[LD_RUB_MENU] EXIT: round_limit=%s" % Round)
            $ Say_Line(girl, _scene_time_up_line())
            call LD_End(girl, dress_up=False) from _call_LD_End_timeout_rub
            return

        menu:
            "Keep rubbing":
                call _sex_scene_tick(girl, "rub", 1) from _call_sst_ld_rub
                if store._sst_result == "abort":
                    call _sex_scene_handle_abort(girl, "rub") from _call_sst_abort_ld_rub
                    return

            "Strip her..." if not getattr(store, "_scene_restricted", False):
                call _ld_strip_menu(girl) from _call_ld_strip_rub
                call LD_ApplySpeed(girl, 0) from _call_LD_ApplySpeed_strip_rub

            "Penetration...":
                call _escalation_menu(girl, "laying_down") from _call_esc_menu_ld_rub
                if store._esc_result == "accepted":
                    call _ld_esc_dispatch(girl, "rub", laying_speed) from _call_esc_disp_ld_rub
                    return
                elif store._esc_result == "scene_ended":
                    call LD_End(girl, dress_up=False) from _call_LD_End_esc_rub
                    return

            "{color=#fbbf24}Cum{/color}" if player_is_cumming():
                call LD_PlayerCumMenu_RubOutside(girl) from _call_LD_PlayerCumMenu_RubOutside_voluntary
                $ _handle_post_cum_exit("laying_down", "rub")
                return

            "Stop now":
                $ print("[LD_RUB_MENU] Selected: Stop now")
                call _scene_stop_reaction(girl) from _call_stop_react_ld_rub
                if store._stop_accepted:
                    $ print("[LD_RUB_MENU] EXIT: stop accepted")
                    return


# ═══════════════════════════════════════════════════════════
# LD_TipLaunch — tip mode (speed locked at 1)
# ═══════════════════════════════════════════════════════════

label LD_TipLaunch(girl):
    $ sub_event_reset(girl)

    $ public_attention_reset()
    call PlayerExposure(girl) from _call_PlayerExposure_ld_tip

    $ girl._prev_pose = getattr(girl, "default_pose", "standing")
    $ girl._prev_slot = getattr(girl, "SpriteLoc", StageCenter)
    if not getattr(girl, "_saved_outfit", None):
        $ girl.SaveOutfit()

    python:
        _kill_scene_threads()
        stop_standing_blink(girl)

        _hide_all_scene_layers(girl)

        _hide_non_scene_girls(girl)

        store._laying_girl = girl
        sprite_state.setdefault(girl.Id, {})["pose"] = "laying_down"
        store.laying_speed = 1
        store.laying_started = False
        store.laying_grab = False
        store.laying_rub_mode = False
        store.laying_tip_mode = False
        _tip_anal = getattr(store, "laying_anal", False)
        store.laying_anal = False
        store._ld_had_pussy = False
        store._ld_had_anal = False
        store._ld_blood_active = False
        store._ld_cum_dick_level = 0
        store._ld_torso_variant = 1
        store._ld_arm_variant = 2
        store._ld_pillow_active = False

    $ set_girl_sprite(girl, pose="laying_down")
    $ _ld_show_preview(girl)
    with fade

    call _ld_bottom_clothes_menu(girl) from _call_ld_bottom_menu_tip

    $ store.laying_tip_mode = True
    call LD_HoleTransition(girl, _tip_anal) from _call_LD_HoleTransition_tip_launch
    call LD_ApplySpeed(girl, 1) from _call_LD_ApplySpeed_tip_init

    python:
        renpy.invoke_in_thread(_ld_blink_loop, girl)
        renpy.invoke_in_thread(_laying_expression_cycle, girl)
    return


# ═══════════════════════════════════════════════════════════
# LD_TipControlMenu — tip game loop (speed locked at 1)
# ═══════════════════════════════════════════════════════════

label LD_TipControlMenu(girl):

    $ store._scene_phase = "tip"
    $ store._cheat_shower_max_act = "tip"
    $ laying_speed = 1
    $ print("[LD_TIP_MENU] ENTER gid=%s restricted=%s exhausted=%s energy=%d" % (girl.gid, getattr(store, "_scene_restricted", False), store._player_exhausted, Player.energy))

    while True:
        $ print("[LD_TIP_MENU] LOOP TOP: sub_event=%s exhausted=%s post_cum=%s Round=%s" % (getattr(store, "_sub_event_position_switched", False), store._player_exhausted, store._post_cum_pending, Round))
        if _scene_should_exit():
            $ print("[LD_TIP_MENU] EXIT: _scene_should_exit()")
            return

        if Round >= 100:
            $ Say_Line(girl, _scene_time_up_line())
            call LD_End(girl, dress_up=False) from _call_LD_End_timeout_tip
            return

        menu:
            "Keep going":
                call _sex_scene_tick(girl, "tip", 1) from _call_sst_ld_tip
                if store._sst_result == "abort":
                    call _sex_scene_handle_abort(girl, "tip") from _call_sst_abort_ld_tip
                    return

            "{color=#fbbf24}Cum{/color}" if player_is_cumming():
                call LD_PlayerCumMenu_TipOutside(girl) from _call_LD_PlayerCumMenu_TipOutside_voluntary
                $ _handle_post_cum_exit("laying_down", "tip")
                return

            "Penetration...":
                call _escalation_menu(girl, "laying_down") from _call_esc_menu_ld_tip
                if store._esc_result == "accepted":
                    call _ld_esc_dispatch(girl, "tip", laying_speed) from _call_esc_disp_ld_tip
                    return
                elif store._esc_result == "scene_ended":
                    call LD_End(girl, dress_up=False) from _call_LD_End_esc_tip
                    return

            "Strip her..." if not getattr(store, "_scene_restricted", False):
                call _ld_strip_menu(girl) from _call_ld_strip_tip
                call LD_ApplySpeed(girl, 1) from _call_LD_ApplySpeed_strip_tip

            "Stop now":
                call _scene_stop_reaction(girl) from _call_stop_react_ld_tip
                if store._stop_accepted:
                    return


# ═══════════════════════════════════════════════════════════
# LD_HoleTransition — first entry / vaginal <-> anal switch
# ═══════════════════════════════════════════════════════════

label LD_HoleTransition(girl, to_anal):
    python:
        _ht_switching = store.laying_started and (store.laying_anal != to_anal)
        _ht_first = not store.laying_started
        debug_log("[LD_HT] to_anal=%s started=%s cur_anal=%s | switching=%s first=%s" % (to_anal, store.laying_started, store.laying_anal, _ht_switching, _ht_first))

    if _ht_switching:
        $ set_scene_expression(girl, "surprised")
        call LD_ApplySpeed(girl, 0) from _call_LD_ApplySpeed_ht_freeze
        python:
            if not store.laying_anal:
                _ht_ass_at = [ld_get_ass_transform(0)]
                renpy.show("tenny laying_during_pussy_below", tag="ld_during_below", at_list=_ht_ass_at, zorder=_LD_Z_DURING_BELOW)
                renpy.show("tenny laying_during_pussy", tag="ld_during", at_list=_ht_ass_at, zorder=_LD_Z_DURING)
                renpy.show("tenny laying_during_pussy_safe", tag="ld_during_safe", at_list=_ht_ass_at, zorder=_LD_Z_DURING_SAFE)
                renpy.hide("ld_before_pussy")
                _raw = not store.condom_active or store._condom_broken
                if to_anal and _raw and store._session_cum.get("inside", 0) > 0:
                    renpy.show("tenny laying_cum_girl", tag="ld_cum_girl", at_list=_ht_ass_at, zorder=_LD_Z_CUM_VAGINAL)
        call LD_PenisExitAnim(girl) from _call_LD_PenisExitAnim_ht_switch

    python:
        store.laying_anal = to_anal
        store.laying_started = True

    if _ht_first or _ht_switching:
        call LD_PenisEnterAnim(girl) from _call_LD_PenisEnterAnim_ht

    python:
        if to_anal:
            store._ld_had_anal = True
            girl._ld_after_anal = True
        else:
            store._ld_had_pussy = True
            girl._ld_after_pussy = True
        debug_log("[LD_HT] DONE anal=%s had_p=%s had_a=%s after_p=%s after_a=%s" % (store.laying_anal, store._ld_had_pussy, store._ld_had_anal, girl._ld_after_pussy, girl._ld_after_anal))
    # only when he actually goes in (first entry or pussy -> ass), not on every speed change inside the same hole
    if to_anal and (_ht_first or _ht_switching):
        $ _watcher_scene_comment("anal_enter")
    return


# ═══════════════════════════════════════════════════════════
# LD_PenisEnterAnim — slide in
# ═══════════════════════════════════════════════════════════

label LD_PenisEnterAnim(girl):
    python:
        _total_sex = girl_act_counts(girl)[0]   # "sex" + "anal" scenes (old read of "sex_acts"/"laying_down" was always 0)
        if girl.has_trait("virgin"):
            set_scene_expression(girl, "scared", blush=2)
        elif _total_sex <= SEX_HISTORY_THRESHOLDS["ld_entry_inexperienced_sex"]:
            set_scene_expression(girl, "surprised", blush=1)
        elif girl.has_trait("hardcore_sex"):
            set_scene_expression(girl, renpy.random.choice(["lusty", "pleasure_mild"]))
        elif girl.has_trait("cute_sex"):
            set_scene_expression(girl, renpy.random.choice(["nervous", "embarrassed"]), blush=1)
        else:
            set_scene_expression(girl, renpy.random.choice(["surprised", "pleasure_mild", "nervous"]))
    python:
        debug_log("[LD_ENTER] anal=%s condom=%s" % (store.laying_anal, store.condom_active))

        _slot_at0 = [ld_get_slot_transform(0)]
        _ass_at0 = [ld_get_ass_transform(0)]

        _st = sprite_state.get(girl.Id, {})
        _ld_eyes = _laying_safe(_st.get("eyes", "eyes_normal"))
        _ld_brows = _laying_safe(_st.get("brows", "brows_normal"))
        _ld_mouth = _laying_safe(_st.get("mouth", "mouth_normal"))
        _ld_blush = _attr_for_blush(girl)
        renpy.show("tenny laying %s %s %s %s" % (_ld_eyes, _ld_brows, _ld_mouth, _ld_blush), tag="tenny", at_list=_slot_at0, zorder=_LD_Z_HEAD)
        _ld_show_ass_layers(girl, 0, _ass_at0)
        renpy.show("tenny laying_butt_blush", tag="ld_butt_blush", at_list=_ass_at0, zorder=_LD_Z_BUTT_BLUSH)

        _legs_slide = ld_guy_legs_slide_in
        renpy.show("tenny laying_guy_calf_1", tag="ld_guy_calf_1", at_list=[_legs_slide], zorder=_LD_Z_GUY_CALF_1)
        renpy.show("tenny laying_guy_calf_2", tag="ld_guy_calf_2", at_list=[_legs_slide], zorder=_LD_Z_GUY_CALF_2)
        renpy.show("tenny laying_guy_legs_1", tag="ld_guy_legs_1", at_list=[_legs_slide], zorder=_LD_Z_GUY_LEGS_1)
        renpy.show("tenny laying_guy_legs_2", tag="ld_guy_legs_2", at_list=[_legs_slide], zorder=_LD_Z_GUY_LEGS_2)
        renpy.show("tenny laying_guy_pelvis_safe", tag="ld_guy_pelvis_safe", at_list=[_legs_slide], zorder=_LD_Z_GUY_PELVIS_SAFE)

        if store.laying_anal:
            renpy.show("tenny laying_during_anal_safe", tag="ld_during_safe", at_list=_ass_at0, zorder=_LD_Z_DURING_ANAL_SF)
        else:
            renpy.show("tenny laying_during_pussy_safe", tag="ld_during_safe", at_list=_ass_at0, zorder=_LD_Z_DURING_SAFE)

        renpy.hide("ld_penis")
        renpy.hide("ld_condom")
        _pen_z = _ld_pen_z()
        _slide_tf = lda_penis_slide_in if store.laying_anal else ld_penis_slide_in
        _pelvis_slide = lda_guy_pelvis_slide_in if store.laying_anal else ld_guy_pelvis_slide_in
        renpy.show("tenny laying_penis", tag="ld_penis", at_list=[_slide_tf], zorder=_pen_z)
        renpy.show("tenny laying_guy_pelvis", tag="ld_guy_pelvis", at_list=[_pelvis_slide], zorder=_LD_Z_GUY_PELVIS)
        if store.condom_active:
            _cb_cimg = _condom_img_tag("ld_condom")
            renpy.show(_cb_cimg, tag="ld_condom", at_list=[_slide_tf], zorder=_pen_z)
        if store._ld_blood_active:
            _bl_img = girl.gid + " laying_blood_penis"
            if renpy.has_image(_bl_img, exact=True):
                renpy.show(_bl_img, tag="ld_blood_penis", at_list=[_slide_tf], zorder=_pen_z + 1)
        _raw = not store.condom_active or store._condom_broken
        if _raw and store._ld_cum_dick_level > 0:
            _cd_suffix = "2" if store._ld_cum_dick_level >= 2 else "1"
            _cd_img = girl.gid + " laying_cum_dick_" + _cd_suffix
            if renpy.has_image(_cd_img, exact=True):
                renpy.show(_cd_img, tag="ld_cum_dick", at_list=[_slide_tf], zorder=_pen_z + 1)
        if _raw and store._ld_cum_dick_level >= 1:
            _cc2_img = girl.gid + " laying_cum_creampie_2"
            if renpy.has_image(_cc2_img, exact=True):
                renpy.show(_cc2_img, tag="ld_cum_creampie_2", at_list=[_slide_tf], zorder=_pen_z + 1)
        if _raw and store._ld_cum_dick_level >= 2:
            _cc3_img = girl.gid + " laying_cum_creampie_3"
            if renpy.has_image(_cc3_img, exact=True):
                renpy.show(_cc3_img, tag="ld_cum_creampie_3", at_list=[_slide_tf], zorder=_pen_z + 1)

    $ renpy.pause(0.25)

    python:
        _ass_at0 = [ld_get_ass_transform(0)]
        if store.laying_anal:
            renpy.show("tenny laying_during_anal_below", tag="ld_during_below", at_list=_ass_at0, zorder=_LD_Z_DURING_ANAL_BL)
            renpy.show("tenny laying_during_anal", tag="ld_during", at_list=_ass_at0, zorder=_LD_Z_DURING_ANAL)
        else:
            renpy.show("tenny laying_during_pussy_below", tag="ld_during_below", at_list=_ass_at0, zorder=_LD_Z_DURING_BELOW)
            renpy.show("tenny laying_during_pussy", tag="ld_during", at_list=_ass_at0, zorder=_LD_Z_DURING)
            renpy.hide("ld_before_pussy")

    $ renpy.pause(0.30)
    return


# ═══════════════════════════════════════════════════════════
# LD_PenisExitAnim — slide out
# ═══════════════════════════════════════════════════════════

label LD_PenisExitAnim(girl):
    python:
        _pen_z = _ld_pen_z()
        _slide_tf = lda_penis_slide_out if store.laying_anal else ld_penis_slide_out
        _pelvis_slide = lda_guy_pelvis_slide_out if store.laying_anal else ld_guy_pelvis_slide_out
        _legs_slide = ld_guy_legs_slide_out
        renpy.show("tenny laying_penis", tag="ld_penis", at_list=[_slide_tf], zorder=_pen_z)
        renpy.show("tenny laying_guy_pelvis", tag="ld_guy_pelvis", at_list=[_pelvis_slide], zorder=_LD_Z_GUY_PELVIS)
        renpy.show("tenny laying_guy_calf_1", tag="ld_guy_calf_1", at_list=[_legs_slide], zorder=_LD_Z_GUY_CALF_1)
        renpy.show("tenny laying_guy_calf_2", tag="ld_guy_calf_2", at_list=[_legs_slide], zorder=_LD_Z_GUY_CALF_2)
        renpy.show("tenny laying_guy_legs_1", tag="ld_guy_legs_1", at_list=[_legs_slide], zorder=_LD_Z_GUY_LEGS_1)
        renpy.show("tenny laying_guy_legs_2", tag="ld_guy_legs_2", at_list=[_legs_slide], zorder=_LD_Z_GUY_LEGS_2)
        renpy.show("tenny laying_guy_pelvis_safe", tag="ld_guy_pelvis_safe", at_list=[_legs_slide], zorder=_LD_Z_GUY_PELVIS_SAFE)
        if store.condom_active:
            _cb_cimg = _condom_img_tag("ld_condom")
            renpy.show(_cb_cimg, tag="ld_condom", at_list=[_slide_tf], zorder=_pen_z)
        if store._ld_blood_active:
            _bl_img = girl.gid + " laying_blood_penis"
            if renpy.has_image(_bl_img, exact=True):
                renpy.show(_bl_img, tag="ld_blood_penis", at_list=[_slide_tf], zorder=_pen_z + 1)
        _raw = not store.condom_active or store._condom_broken
        if _raw and store._ld_cum_dick_level > 0:
            _cd_suffix = "2" if store._ld_cum_dick_level >= 2 else "1"
            _cd_img = girl.gid + " laying_cum_dick_" + _cd_suffix
            if renpy.has_image(_cd_img, exact=True):
                renpy.show(_cd_img, tag="ld_cum_dick", at_list=[_slide_tf], zorder=_pen_z + 1)
        if _raw and store._ld_cum_dick_level >= 1:
            _cc2_img = girl.gid + " laying_cum_creampie_2"
            if renpy.has_image(_cc2_img, exact=True):
                renpy.show(_cc2_img, tag="ld_cum_creampie_2", at_list=[_slide_tf], zorder=_pen_z + 1)
        if _raw and store._ld_cum_dick_level >= 2:
            _cc3_img = girl.gid + " laying_cum_creampie_3"
            if renpy.has_image(_cc3_img, exact=True):
                renpy.show(_cc3_img, tag="ld_cum_creampie_3", at_list=[_slide_tf], zorder=_pen_z + 1)
    $ renpy.pause(0.55)
    python:
        renpy.hide("ld_penis")
        renpy.hide("ld_condom")
        renpy.hide("ld_blood_penis")
        renpy.hide("ld_cum_dick")
        renpy.hide("ld_cum_creampie_2")
        renpy.hide("ld_cum_creampie_3")
        renpy.hide("ld_guy_pelvis")
        renpy.hide("ld_guy_calf_1")
        renpy.hide("ld_guy_calf_2")
        renpy.hide("ld_guy_legs_1")
        renpy.hide("ld_guy_legs_2")
        renpy.hide("ld_guy_pelvis_safe")
    return


# ═══════════════════════════════════════════════════════════
# LD_CondomRemoveAnim — slide out with condom, back in raw
# ═══════════════════════════════════════════════════════════

label LD_CondomRemoveAnim(girl):
    python:
        _pen_z = _ld_pen_z()
        _slide_tf = lda_penis_slide_out if store.laying_anal else ld_penis_slide_out
        _pelvis_slide = lda_guy_pelvis_slide_out if store.laying_anal else ld_guy_pelvis_slide_out
        _legs_slide = ld_guy_legs_slide_out
        _ld_condom_tag = _condom_img_tag("ld_condom")
        _cr_blood = getattr(store, "_cr_had_blood", False)
        _cr_cum = getattr(store, "_cr_had_cum", 0)
        renpy.show("tenny laying_penis", tag="ld_penis", at_list=[_slide_tf], zorder=_pen_z)
        renpy.show(_ld_condom_tag, tag="ld_condom", at_list=[_slide_tf], zorder=_pen_z)
        # Blood/cum slide out with the condom
        if _cr_blood:
            _bl_img = girl.gid + " laying_blood_penis"
            if renpy.has_image(_bl_img, exact=True):
                renpy.show(_bl_img, tag="ld_blood_penis", at_list=[_slide_tf], zorder=_pen_z + 1)
        if _cr_cum > 0:
            _cd_img = girl.gid + " laying_cum_dick_" + ("2" if _cr_cum >= 2 else "1")
            if renpy.has_image(_cd_img, exact=True):
                renpy.show(_cd_img, tag="ld_cum_dick", at_list=[_slide_tf], zorder=_pen_z + 1)
            _cc2_img = girl.gid + " laying_cum_creampie_2"
            if renpy.has_image(_cc2_img, exact=True):
                renpy.show(_cc2_img, tag="ld_cum_creampie_2", at_list=[_slide_tf], zorder=_pen_z + 1)
            if _cr_cum >= 2:
                _cc3_img = girl.gid + " laying_cum_creampie_3"
                if renpy.has_image(_cc3_img, exact=True):
                    renpy.show(_cc3_img, tag="ld_cum_creampie_3", at_list=[_slide_tf], zorder=_pen_z + 1)
        renpy.show("tenny laying_guy_pelvis", tag="ld_guy_pelvis", at_list=[_pelvis_slide], zorder=_LD_Z_GUY_PELVIS)
        renpy.show("tenny laying_guy_calf_1", tag="ld_guy_calf_1", at_list=[_legs_slide], zorder=_LD_Z_GUY_CALF_1)
        renpy.show("tenny laying_guy_calf_2", tag="ld_guy_calf_2", at_list=[_legs_slide], zorder=_LD_Z_GUY_CALF_2)
        renpy.show("tenny laying_guy_legs_1", tag="ld_guy_legs_1", at_list=[_legs_slide], zorder=_LD_Z_GUY_LEGS_1)
        renpy.show("tenny laying_guy_legs_2", tag="ld_guy_legs_2", at_list=[_legs_slide], zorder=_LD_Z_GUY_LEGS_2)
        renpy.show("tenny laying_guy_pelvis_safe", tag="ld_guy_pelvis_safe", at_list=[_legs_slide], zorder=_LD_Z_GUY_PELVIS_SAFE)
    $ renpy.pause(0.6)
    python:
        renpy.hide("ld_condom")
        renpy.hide("ld_penis")
        # Blood/cum removed with the condom
        if _cr_blood:
            renpy.hide("ld_blood_penis")
            renpy.hide("ld_blood_anim")
            renpy.hide("ld_blood_static")
        if _cr_cum > 0:
            renpy.hide("ld_cum_dick")
            renpy.hide("ld_cum_creampie_2")
            renpy.hide("ld_cum_creampie_3")
        renpy.hide("ld_guy_pelvis")
        renpy.hide("ld_guy_calf_1")
        renpy.hide("ld_guy_calf_2")
        renpy.hide("ld_guy_legs_1")
        renpy.hide("ld_guy_legs_2")
        renpy.hide("ld_guy_pelvis_safe")
        _pen_z = _ld_pen_z()
        _slide_tf = lda_penis_slide_in if store.laying_anal else ld_penis_slide_in
        _pelvis_slide = lda_guy_pelvis_slide_in if store.laying_anal else ld_guy_pelvis_slide_in
        _legs_slide = ld_guy_legs_slide_in
        renpy.show("tenny laying_penis", tag="ld_penis", at_list=[_slide_tf], zorder=_pen_z)
        renpy.show("tenny laying_guy_pelvis", tag="ld_guy_pelvis", at_list=[_pelvis_slide], zorder=_LD_Z_GUY_PELVIS)
        renpy.show("tenny laying_guy_calf_1", tag="ld_guy_calf_1", at_list=[_legs_slide], zorder=_LD_Z_GUY_CALF_1)
        renpy.show("tenny laying_guy_calf_2", tag="ld_guy_calf_2", at_list=[_legs_slide], zorder=_LD_Z_GUY_CALF_2)
        renpy.show("tenny laying_guy_legs_1", tag="ld_guy_legs_1", at_list=[_legs_slide], zorder=_LD_Z_GUY_LEGS_1)
        renpy.show("tenny laying_guy_legs_2", tag="ld_guy_legs_2", at_list=[_legs_slide], zorder=_LD_Z_GUY_LEGS_2)
        renpy.show("tenny laying_guy_pelvis_safe", tag="ld_guy_pelvis_safe", at_list=[_legs_slide], zorder=_LD_Z_GUY_PELVIS_SAFE)
    $ renpy.pause(0.6)
    return


# ═══════════════════════════════════════════════════════════
# LD_CondomPutOnAnim — slide out raw, back in with condom
# ═══════════════════════════════════════════════════════════

label LD_CondomPutOnAnim(girl):
    python:
        _pen_z = _ld_pen_z()
        _slide_tf = lda_penis_slide_out if store.laying_anal else ld_penis_slide_out
        _pelvis_slide = lda_guy_pelvis_slide_out if store.laying_anal else ld_guy_pelvis_slide_out
        _legs_slide = ld_guy_legs_slide_out
        renpy.show("tenny laying_penis", tag="ld_penis", at_list=[_slide_tf], zorder=_pen_z)
        renpy.show("tenny laying_guy_pelvis", tag="ld_guy_pelvis", at_list=[_pelvis_slide], zorder=_LD_Z_GUY_PELVIS)
        renpy.show("tenny laying_guy_calf_1", tag="ld_guy_calf_1", at_list=[_legs_slide], zorder=_LD_Z_GUY_CALF_1)
        renpy.show("tenny laying_guy_calf_2", tag="ld_guy_calf_2", at_list=[_legs_slide], zorder=_LD_Z_GUY_CALF_2)
        renpy.show("tenny laying_guy_legs_1", tag="ld_guy_legs_1", at_list=[_legs_slide], zorder=_LD_Z_GUY_LEGS_1)
        renpy.show("tenny laying_guy_legs_2", tag="ld_guy_legs_2", at_list=[_legs_slide], zorder=_LD_Z_GUY_LEGS_2)
        renpy.show("tenny laying_guy_pelvis_safe", tag="ld_guy_pelvis_safe", at_list=[_legs_slide], zorder=_LD_Z_GUY_PELVIS_SAFE)
    $ renpy.pause(0.6)
    python:
        renpy.hide("ld_penis")
        renpy.hide("ld_guy_pelvis")
        renpy.hide("ld_guy_calf_1")
        renpy.hide("ld_guy_calf_2")
        renpy.hide("ld_guy_legs_1")
        renpy.hide("ld_guy_legs_2")
        renpy.hide("ld_guy_pelvis_safe")
        _pen_z = _ld_pen_z()
        _slide_tf = lda_penis_slide_in if store.laying_anal else ld_penis_slide_in
        _pelvis_slide = lda_guy_pelvis_slide_in if store.laying_anal else ld_guy_pelvis_slide_in
        _legs_slide = ld_guy_legs_slide_in
        renpy.show("tenny laying_penis", tag="ld_penis", at_list=[_slide_tf], zorder=_pen_z)
        renpy.show("tenny laying_guy_pelvis", tag="ld_guy_pelvis", at_list=[_pelvis_slide], zorder=_LD_Z_GUY_PELVIS)
        renpy.show("tenny laying_guy_calf_1", tag="ld_guy_calf_1", at_list=[_legs_slide], zorder=_LD_Z_GUY_CALF_1)
        renpy.show("tenny laying_guy_calf_2", tag="ld_guy_calf_2", at_list=[_legs_slide], zorder=_LD_Z_GUY_CALF_2)
        renpy.show("tenny laying_guy_legs_1", tag="ld_guy_legs_1", at_list=[_legs_slide], zorder=_LD_Z_GUY_LEGS_1)
        renpy.show("tenny laying_guy_legs_2", tag="ld_guy_legs_2", at_list=[_legs_slide], zorder=_LD_Z_GUY_LEGS_2)
        renpy.show("tenny laying_guy_pelvis_safe", tag="ld_guy_pelvis_safe", at_list=[_legs_slide], zorder=_LD_Z_GUY_PELVIS_SAFE)
        if store.condom_active:
            _condom_img = _condom_img_tag("ld_condom")
            renpy.show(_condom_img, tag="ld_condom", at_list=[_slide_tf], zorder=_pen_z)
    $ renpy.pause(0.6)
    return


# ═══════════════════════════════════════════════════════════
# LD_CumAnim — cum inside (speed 4 + shake)
# ═══════════════════════════════════════════════════════════

label LD_CumAnim(girl):
    $ _ld_prev_speed = store.laying_speed
    $ _apply_cum_expression(girl, "laying_down", "inside")

    $ store.laying_speed = 4
    call LD_ApplySpeed(girl, 4) from _call_LD_ApplySpeed_cum4

    python:
        _pen_z = _ld_pen_z()
        _cum_tf = lda_penis_cum_pulse() if store.laying_anal else ld_penis_cum_pulse()
        _pelvis_cum = lda_guy_pelvis_cum_pulse if store.laying_anal else ld_guy_pelvis_cum_pulse
        renpy.show("tenny laying_penis", tag="ld_penis", at_list=[_cum_tf], zorder=_pen_z)
        renpy.show("tenny laying_guy_pelvis", tag="ld_guy_pelvis", at_list=[_pelvis_cum], zorder=_LD_Z_GUY_PELVIS)
        if store.condom_active:
            _cb = _condom_img_tag("ld_condom")
            renpy.show(_cb, tag="ld_condom", at_list=[_cum_tf], zorder=_pen_z)

    $ renpy.pause(0.35)
    show layer master at ld_cum_shake
    $ renpy.pause(0.20)
    show layer master

    # Re-sync all layers so cum anim starts in phase with ass bounce
    call LD_ApplySpeed(girl, 4) from _call_LD_ApplySpeed_cum4_sync

    # Smooth thrust to deep + cum girl anim + screen shake — girl keeps moving
    python:
        _pen_z = _ld_pen_z()
        if store.laying_anal:
            _deep_tf = lda_penis_cum_deep_thrust
            _freeze_pel = lda_guy_pelvis_cum_freeze
        else:
            _deep_tf = ld_penis_cum_deep_thrust
            _freeze_pel = ld_guy_pelvis_cum_freeze
        renpy.show("tenny laying_penis", tag="ld_penis", at_list=[_deep_tf], zorder=_pen_z)
        renpy.show("tenny laying_guy_pelvis", tag="ld_guy_pelvis", at_list=[_freeze_pel], zorder=_LD_Z_GUY_PELVIS)
        if store.condom_active:
            _cb = _condom_img_tag("ld_condom")
            renpy.show(_cb, tag="ld_condom", at_list=[_deep_tf], zorder=_pen_z)
        if store._ld_blood_active:
            _bl_img = girl.gid + " laying_blood_penis"
            if renpy.has_image(_bl_img, exact=True):
                renpy.show(_bl_img, tag="ld_blood_penis", at_list=[_deep_tf], zorder=_pen_z + 1)
        _raw_cum = not store.condom_active or store._condom_broken
        _prev_inside = store._session_cum.get("inside", 0)
        if _raw_cum:
            if _prev_inside >= 2:
                _cd_img = girl.gid + " laying_cum_dick_2_anim"
                if renpy.has_image(_cd_img, exact=True):
                    renpy.show(_cd_img, tag="ld_cum_dick", at_list=[_deep_tf], zorder=_pen_z + 1)
            elif _prev_inside >= 1:
                _cd_img = girl.gid + " laying_cum_dick_1_anim"
                if renpy.has_image(_cd_img, exact=True):
                    renpy.show(_cd_img, tag="ld_cum_dick", at_list=[_deep_tf], zorder=_pen_z + 1)
        renpy.show("tenny laying_guy_calf_1", tag="ld_guy_calf_1", at_list=[ld_get_calf_1_transform(0)], zorder=_LD_Z_GUY_CALF_1)
        renpy.show("tenny laying_guy_calf_2", tag="ld_guy_calf_2", at_list=[ld_get_calf_2_transform(0)], zorder=_LD_Z_GUY_CALF_2)
        renpy.show("tenny laying_guy_legs_1", tag="ld_guy_legs_1", at_list=[ld_get_thigh_1_transform(0)], zorder=_LD_Z_GUY_LEGS_1)
        renpy.show("tenny laying_guy_legs_2", tag="ld_guy_legs_2", at_list=[ld_get_thigh_2_transform(0)], zorder=_LD_Z_GUY_LEGS_2)

        _cum_ass_at = [ld_get_ass_transform(4)]
        if _raw_cum:
            if store.laying_anal:
                if "dripping" in getattr(girl, "Cum", []):
                    renpy.show("tenny laying_cum_girl", tag="ld_cum_girl", at_list=_cum_ass_at, zorder=_LD_Z_CUM_VAGINAL)
            elif _prev_inside >= 1:
                renpy.show("tenny laying_cum_girl", tag="ld_cum_girl", at_list=_cum_ass_at, zorder=_LD_Z_CUM_GIRL)
            else:
                renpy.show("tenny laying_cum_girl_anim", tag="ld_cum_girl", at_list=_cum_ass_at, zorder=_LD_Z_CUM_GIRL)
            if store._ld_cum_dick_level >= 1:
                _cc2_img = girl.gid + " laying_cum_creampie_2"
                if renpy.has_image(_cc2_img, exact=True):
                    renpy.show(_cc2_img, tag="ld_cum_creampie_2", at_list=[_deep_tf], zorder=_pen_z + 1)
            if store._ld_cum_dick_level >= 2:
                _cc3_img = girl.gid + " laying_cum_creampie_3"
                if renpy.has_image(_cc3_img, exact=True):
                    renpy.show(_cc3_img, tag="ld_cum_creampie_3", at_list=[_deep_tf], zorder=_pen_z + 1)

    show layer master at ld_cum_shake
    $ renpy.pause(2.3, hard=True)
    show layer master

    $ store.laying_speed = 0
    call LD_ApplySpeed(girl, 0) from _call_LD_ApplySpeed_cum4_freeze

    # Keep penis at deep position + show static cum_girl + blood follows
    python:
        _pen_z = _ld_pen_z()
        if store.laying_anal:
            _freeze_tf = lda_penis_cum_freeze
            _freeze_pel = lda_guy_pelvis_cum_freeze
        else:
            _freeze_tf = ld_penis_cum_freeze
            _freeze_pel = ld_guy_pelvis_cum_freeze
        renpy.show("tenny laying_penis", tag="ld_penis", at_list=[_freeze_tf], zorder=_pen_z)
        renpy.show("tenny laying_guy_pelvis", tag="ld_guy_pelvis", at_list=[_freeze_pel], zorder=_LD_Z_GUY_PELVIS)
        if store.condom_active:
            _cb = _condom_img_tag("ld_condom")
            renpy.show(_cb, tag="ld_condom", at_list=[_freeze_tf], zorder=_pen_z)
        if store._ld_blood_active:
            _bl_img = girl.gid + " laying_blood_penis"
            if renpy.has_image(_bl_img, exact=True):
                renpy.show(_bl_img, tag="ld_blood_penis", at_list=[_freeze_tf], zorder=_pen_z + 1)
        _raw_cum = not store.condom_active or store._condom_broken
        _prev_inside = store._session_cum.get("inside", 0)
        _effective_inside = _prev_inside + 1
        if _raw_cum:
            if _effective_inside >= 3:
                store._ld_cum_dick_level = 2
            elif _effective_inside >= 2:
                store._ld_cum_dick_level = 1
            if store._ld_cum_dick_level >= 2:
                _cd_img = girl.gid + " laying_cum_dick_2"
                if renpy.has_image(_cd_img, exact=True):
                    renpy.show(_cd_img, tag="ld_cum_dick", at_list=[_freeze_tf], zorder=_pen_z + 1)
            elif store._ld_cum_dick_level >= 1:
                _cd_img = girl.gid + " laying_cum_dick_1"
                if renpy.has_image(_cd_img, exact=True):
                    renpy.show(_cd_img, tag="ld_cum_dick", at_list=[_freeze_tf], zorder=_pen_z + 1)
            _ass_at = [ld_get_ass_transform(0)]
            _cg_z = _LD_Z_CUM_VAGINAL if store.laying_anal else _LD_Z_CUM_GIRL
            _has_vaginal_drip = "dripping" in getattr(girl, "Cum", [])
            if not store.laying_anal or _has_vaginal_drip:
                renpy.show("tenny laying_cum_girl", tag="ld_cum_girl", at_list=_ass_at, zorder=_cg_z)
            if store._ld_cum_dick_level >= 1:
                _cc2_img = girl.gid + " laying_cum_creampie_2"
                if renpy.has_image(_cc2_img, exact=True):
                    renpy.show(_cc2_img, tag="ld_cum_creampie_2", at_list=[_freeze_tf], zorder=_pen_z + 1)
            if store._ld_cum_dick_level >= 2:
                _cc3_img = girl.gid + " laying_cum_creampie_3"
                if renpy.has_image(_cc3_img, exact=True):
                    renpy.show(_cc3_img, tag="ld_cum_creampie_3", at_list=[_freeze_tf], zorder=_pen_z + 1)
    return


# ═══════════════════════════════════════════════════════════
# LD_CumOutsideFreeze — cum outside (freeze + slide out)
# ═══════════════════════════════════════════════════════════

label LD_CumOutsideFreeze(girl):
    $ _apply_cum_expression(girl, "laying_down", "outside")

    $ store.laying_speed = 0
    call LD_ApplySpeed(girl, 0) from _call_LD_ApplySpeed_cumfreeze

    call LD_PenisExitAnim(girl) from _call_LD_PenisExitAnim_cumout

    # Slide everything back in together (penis, pelvis, legs — all synced)
    python:
        _pen_z = _ld_pen_z()
        _pen_slide = lda_penis_slide_in if store.laying_anal else ld_penis_slide_in
        _pel_slide = lda_guy_pelvis_slide_in if store.laying_anal else ld_guy_pelvis_slide_in
        _legs_slide_in = ld_guy_legs_slide_in
        _co_pen_z = _LD_Z_CUM_GIRL + 1
        _co_dick_z = _LD_Z_CUM_GIRL + 2
        renpy.show("tenny laying_penis", tag="ld_penis", at_list=[_pen_slide], zorder=_co_pen_z)
        renpy.show("tenny laying_guy_pelvis", tag="ld_guy_pelvis", at_list=[_pel_slide], zorder=_LD_Z_GUY_PELVIS)
        renpy.show("tenny laying_guy_calf_1", tag="ld_guy_calf_1", at_list=[_legs_slide_in], zorder=_LD_Z_GUY_CALF_1)
        renpy.show("tenny laying_guy_calf_2", tag="ld_guy_calf_2", at_list=[_legs_slide_in], zorder=_LD_Z_GUY_CALF_2)
        renpy.show("tenny laying_guy_legs_1", tag="ld_guy_legs_1", at_list=[_legs_slide_in], zorder=_LD_Z_GUY_LEGS_1)
        renpy.show("tenny laying_guy_legs_2", tag="ld_guy_legs_2", at_list=[_legs_slide_in], zorder=_LD_Z_GUY_LEGS_2)
        renpy.show("tenny laying_guy_pelvis_safe", tag="ld_guy_pelvis_safe", at_list=[_legs_slide_in], zorder=_LD_Z_GUY_PELVIS_SAFE)
        _raw = not store.condom_active or store._condom_broken
        if _raw and store._ld_cum_dick_level > 0:
            _cd_suffix = "2" if store._ld_cum_dick_level >= 2 else "1"
            _cd_img = girl.gid + " laying_cum_dick_" + _cd_suffix
            if renpy.has_image(_cd_img, exact=True):
                renpy.show(_cd_img, tag="ld_cum_dick", at_list=[_pen_slide], zorder=_co_dick_z)
        if _raw and store._ld_cum_dick_level >= 1:
            _cc2_img = girl.gid + " laying_cum_creampie_2"
            if renpy.has_image(_cc2_img, exact=True):
                renpy.show(_cc2_img, tag="ld_cum_creampie_2", at_list=[_pen_slide], zorder=_co_dick_z)
        if _raw and store._ld_cum_dick_level >= 2:
            _cc3_img = girl.gid + " laying_cum_creampie_3"
            if renpy.has_image(_cc3_img, exact=True):
                renpy.show(_cc3_img, tag="ld_cum_creampie_3", at_list=[_pen_slide], zorder=_co_dick_z)

    $ renpy.pause(0.55)

    # Cum pulse after slide completes
    python:
        _pen_z = _ld_pen_z()
        _cum_tf = lda_penis_cum_pulse() if store.laying_anal else ld_penis_cum_pulse()
        _pelvis_cum = lda_guy_pelvis_cum_pulse if store.laying_anal else ld_guy_pelvis_cum_pulse
        _co_pen_z = _LD_Z_CUM_GIRL + 1
        _co_dick_z = _LD_Z_CUM_GIRL + 2
        renpy.show("tenny laying_penis", tag="ld_penis", at_list=[_cum_tf], zorder=_co_pen_z)
        renpy.show("tenny laying_guy_pelvis", tag="ld_guy_pelvis", at_list=[_pelvis_cum], zorder=_LD_Z_GUY_PELVIS)
        _raw = not store.condom_active or store._condom_broken
        if _raw and store._ld_cum_dick_level > 0:
            _cd_suffix = "2" if store._ld_cum_dick_level >= 2 else "1"
            _cd_img = girl.gid + " laying_cum_dick_" + _cd_suffix
            if renpy.has_image(_cd_img, exact=True):
                renpy.show(_cd_img, tag="ld_cum_dick", at_list=[_cum_tf], zorder=_co_dick_z)
        if _raw and store._ld_cum_dick_level >= 1:
            _cc2_img = girl.gid + " laying_cum_creampie_2"
            if renpy.has_image(_cc2_img, exact=True):
                renpy.show(_cc2_img, tag="ld_cum_creampie_2", at_list=[_cum_tf], zorder=_co_dick_z)
        if _raw and store._ld_cum_dick_level >= 2:
            _cc3_img = girl.gid + " laying_cum_creampie_3"
            if renpy.has_image(_cc3_img, exact=True):
                renpy.show(_cc3_img, tag="ld_cum_creampie_3", at_list=[_cum_tf], zorder=_co_dick_z)

    $ renpy.pause(0.35)
    show layer master at ld_cum_shake
    $ renpy.pause(0.20)
    show layer master
    $ renpy.pause(0.50)
    return



# ═══════════════════════════════════════════════════════════
# LD_CreampieAftermath — static pose after cum inside
# ═══════════════════════════════════════════════════════════

label LD_CreampieAftermath(girl):
    python:
        store.laying_speed = 0
        print("[LD_AFTERMATH] ENTER laying_anal=%s laying_started=%s" % (store.laying_anal, store.laying_started))
        print("[LD_AFTERMATH] _ld_after_pussy=%s _ld_after_anal=%s" % (getattr(girl, "_ld_after_pussy", "MISSING"), getattr(girl, "_ld_after_anal", "MISSING")))
        print("[LD_AFTERMATH] _ld_had_pussy=%s _ld_had_anal=%s" % (getattr(store, "_ld_had_pussy", "MISSING"), getattr(store, "_ld_had_anal", "MISSING")))
        print("[LD_AFTERMATH] girl.Cum=%s" % getattr(girl, "Cum", []))
        print("[LD_AFTERMATH] _ld_cum_dick_level=%s condom_active=%s _condom_broken=%s" % (store._ld_cum_dick_level, store.condom_active, getattr(store, "_condom_broken", False)))
        print("[LD_AFTERMATH] showing_tags=%s" % [t for t in renpy.get_showing_tags("master") if t.startswith("ld_")])

        _slot_at = [ld_get_slot_transform(0)]
        _ass_at = [ld_get_ass_transform(0)]

        _st = sprite_state.get(girl.Id, {})
        _ld_eyes = _laying_safe(_st.get("eyes", "eyes_normal"))
        _ld_brows = _laying_safe(_st.get("brows", "brows_normal"))
        _ld_mouth = _laying_safe(_st.get("mouth", "mouth_normal"))
        _ld_blush = _attr_for_blush(girl)
        renpy.show("tenny laying %s %s %s %s" % (_ld_eyes, _ld_brows, _ld_mouth, _ld_blush), tag="tenny", at_list=_slot_at, zorder=_LD_Z_HEAD)
        _ld_show_torso(girl, _slot_at)
        _ld_show_clothing(girl, _slot_at)
        _ld_show_ass_layers(girl, 0, _ass_at)
        renpy.show("tenny laying_butt_blush", tag="ld_butt_blush", at_list=_ass_at, zorder=_LD_Z_BUTT_BLUSH)
        _ld_show_pants(girl, _slot_at, _ass_at)

        _pan_item = girl.Panties
        _legs_state = girl.clothes_state.get("skirt", "full") if girl.Legs else None
        if _pan_item and (not girl.Legs or _legs_state == "up"):
            _pan_state = girl.clothes_state.get("panties", "full")
            if store.laying_started and _pan_state == "full":
                _ld_hide_panties()
            else:
                _pan_z = _LD_Z_PANTIES_DOWN if _pan_state == "down" else _LD_Z_PANTIES
                _pan_img = "tenny laying_panties_%s_%s" % (_pan_item, _pan_state)
                if renpy.has_image(_pan_img, exact=True):
                    renpy.show(_pan_img, tag="ld_panties", at_list=_ass_at, zorder=_pan_z)
                else:
                    _ld_hide_panties()
        else:
            _ld_hide_panties()

        renpy.show("tenny laying_legs_left", tag="ld_legs_left", at_list=_slot_at, zorder=_LD_Z_LEGS)
        renpy.show("tenny laying_legs_right", tag="ld_legs_right", at_list=_slot_at, zorder=_LD_Z_LEGS + 1)
        renpy.show("tenny laying_pelvis", tag="ld_pelvis", at_list=_ass_at, zorder=_LD_Z_PELVIS)

        print("[LD_AFTERMATH] ANAL BRANCH: laying_anal=%s" % store.laying_anal)
        if store.laying_anal:
            print("[LD_AFTERMATH] showing base_ass, after_ass, hiding during layers")
            renpy.show("tenny laying_ass_base_left", tag="ld_ass_left", at_list=_ass_at, zorder=_LD_Z_ASS)
            renpy.show("tenny laying_ass_base_right", tag="ld_ass_right", at_list=_ass_at, zorder=_LD_Z_ASS + 1)
            renpy.show("tenny laying_after_ass", tag="ld_before_ass", at_list=_ass_at, zorder=_LD_Z_BEFORE_ASS)
            renpy.hide("ld_before_ass_2")
            renpy.hide("ld_during")
            renpy.hide("ld_during_below")
            renpy.hide("ld_during_safe")
            _ap = getattr(girl, "_ld_after_pussy", False)
            print("[LD_AFTERMATH] after_pussy check: %s" % _ap)
            if _ap:
                print("[LD_AFTERMATH] showing after_pussy at z=%d" % _LD_Z_DURING_BELOW)
                renpy.show("tenny laying_after_pussy", tag="ld_before_pussy", at_list=_ass_at, zorder=_LD_Z_DURING_BELOW)
        else:
            print("[LD_AFTERMATH] vaginal branch: showing after_pussy, during_pussy layers")
            renpy.show("tenny laying_after_pussy", tag="ld_during_below", at_list=_ass_at, zorder=_LD_Z_DURING_BELOW)
            renpy.show("tenny laying_during_pussy", tag="ld_during", at_list=_ass_at, zorder=_LD_Z_DURING)
            renpy.show("tenny laying_during_pussy_safe", tag="ld_during_safe", at_list=_ass_at, zorder=_LD_Z_DURING_SAFE)
            renpy.hide("ld_before_pussy")

        renpy.hide("ld_penis")
        renpy.hide("ld_condom")
        renpy.hide("ld_blood_penis")
        renpy.hide("ld_blood_anim")
        renpy.hide("ld_blood_static")

        _cum = getattr(girl, "Cum", [])
        _had_vaginal_cream = "dripping" in _cum
        _had_anal_cream = "dripping_ass" in _cum
        print("[LD_AFTERMATH] CUM: girl.Cum=%s vaginal_cream=%s anal_cream=%s" % (_cum, _had_vaginal_cream, _had_anal_cream))
        _cum_at = _ass_at + [ld_cum_alpha]

        renpy.hide("ld_cum_dick")
        renpy.hide("ld_cum_creampie_2")
        renpy.hide("ld_cum_creampie_3")

        _cum_anal_at = _ass_at + [ld_cum_anal_offset]
        if _had_anal_cream:
            print("[LD_AFTERMATH] showing cum_anal at 70%% with y-offset")
            renpy.show("tenny laying_cum_anal", tag="ld_cum_anal", at_list=_cum_anal_at, zorder=_LD_Z_CUM)
        else:
            print("[LD_AFTERMATH] no anal cream, hiding cum_anal")
            renpy.hide("ld_cum_anal")
        if _had_vaginal_cream:
            print("[LD_AFTERMATH] showing cum_vaginal + cum_girl at 70%%")
            renpy.show("tenny laying_cum_vaginal", tag="ld_cum_vaginal", at_list=_cum_at, zorder=_LD_Z_CUM_VAGINAL)
            renpy.show("tenny laying_cum_girl", tag="ld_cum_girl", at_list=_cum_at, zorder=_LD_Z_CUM_GIRL)
        else:
            print("[LD_AFTERMATH] no vaginal cream, hiding cum_vaginal + cum_girl")
            renpy.hide("ld_cum_vaginal")
            renpy.hide("ld_cum_girl")
        print("[LD_AFTERMATH] DONE showing_tags=%s" % [t for t in renpy.get_showing_tags("master") if t.startswith("ld_")])
        renpy.hide("ld_guy_legs_1")
        renpy.hide("ld_guy_legs_2")
        renpy.hide("ld_guy_calf_1")
        renpy.hide("ld_guy_calf_2")
        renpy.hide("ld_guy_pelvis")
        renpy.hide("ld_guy_pelvis_safe")

        _raw_cum = not store.condom_active or store._condom_broken
        if not store.laying_anal and _raw_cum:
            renpy.show("tenny laying_after_creampie_anim", tag="ld_after_creampie", at_list=_ass_at, zorder=_LD_Z_CUM_VAGINAL + 1)

    if not store.laying_anal and (not store.condom_active or store._condom_broken):
        $ renpy.pause(2.4, hard=True)
        python:
            _ass_at = [ld_get_ass_transform(0)]
            renpy.show("tenny laying_after_creampie", tag="ld_after_creampie", at_list=_ass_at, zorder=_LD_Z_CUM_VAGINAL + 1)

    return


# ═══════════════════════════════════════════════════════════
# LD_PlayerCumMenu_RubOutside — cum menu for rub mode
# ═══════════════════════════════════════════════════════════

label LD_PlayerCumMenu_RubOutside(girl):

    "You feel yourself getting close..."
    $ _ld_mouth_via_bj = False

    menu:
        "Fire away":
            call _ld_rub_cum_anim(girl) from _call_ld_rub_cum_anim_fire
            "You cum."
            $ process_cum(girl, "laying_down", "away")
            $ apply_cum_bonuses(girl, "cum_outside")

        "Cum on her":
            $ _ld_cum_type = "ass"
            menu:
                "On her ass":
                    $ _ld_cum_type = "ass"
                "On her body":
                    $ _ld_cum_type = "body"
                "On her face":
                    $ _ld_cum_type = "face"

            call _ld_rub_cum_anim(girl) from _call_ld_rub_cum_anim_on

            if _ld_cum_type == "ass":
                "You cum on her ass."
                $ process_cum(girl, "laying_down", "ass")
            elif _ld_cum_type == "body":
                "You cum on her body."
                $ process_cum(girl, "laying_down", "body")
            else:
                "You cum on her face."
                $ process_cum(girl, "laying_down", "face")

            $ apply_cum_bonuses(girl, "cum_outside")
            $ _cum_say_line(girl, _ld_cum_type, "laying_down")

        "Ask to cum in her mouth":
            $ _cum_check = CumPermissionCheck(girl, "cum_in_mouth_ask")
            if _cum_check["accepted"]:
                $ Say_Line(girl, scene_pick_line("cum_mouth_accepted", scene="laying_down", girl=girl) or _("Go ahead... do it."))
                call _cum_in_mouth_via_bj(girl, "laying_down") from _call_cum_in_mouth_via_bj_ld_rub
                $ _ld_mouth_via_bj = True
            else:
                $ set_scene_expression(girl, "angry")
                $ Say_Line(girl, scene_pick_line("cum_mouth_denied", scene="laying_down", girl=girl) or _("No way... not in my mouth."))
                call _ld_rub_cum_anim(girl) from _call_ld_rub_cum_anim_mouth_deny
                "You cum on her body instead."
                $ process_cum(girl, "laying_down", "body")
                $ apply_cum_bonuses(girl, "cum_outside")

    return


label _ld_rub_cum_anim(girl):
    $ _apply_cum_expression(girl, "laying_down", "outside")
    python:
        _pen_z = _LD_Z_PENIS_RUB
        _cum_tf = ld_penis_cum_pulse()
        renpy.show("tenny laying_penis", tag="ld_penis", at_list=[_cum_tf], zorder=_pen_z)
        renpy.show("tenny laying_guy_pelvis", tag="ld_guy_pelvis", at_list=[ld_guy_pelvis_cum_pulse], zorder=_LD_Z_GUY_PELVIS)
    $ renpy.pause(0.35)
    show layer master at ld_cum_shake
    $ renpy.pause(0.20)
    show layer master
    $ renpy.pause(0.50)
    return


# ═══════════════════════════════════════════════════════════
# LD_PlayerCumMenu_TipOutside — cum menu for tip mode
# ═══════════════════════════════════════════════════════════

label LD_PlayerCumMenu_TipOutside(girl):

    "You feel yourself getting close..."
    $ _ld_scene_type = "laying_anal" if store.laying_anal else "laying_down"
    $ _ld_mouth_via_bj = False

    menu:
        "Fire away":
            call LD_CumOutsideFreeze(girl) from _call_LD_CumOutsideFreeze_tip_fire
            "You pull out and cum."
            $ process_cum(girl, _ld_scene_type, "away")
            $ apply_cum_bonuses(girl, "cum_outside")

        "Cum on her":
            $ _ld_cum_type = "ass"
            menu:
                "On her ass":
                    $ _ld_cum_type = "ass"
                "On her body":
                    $ _ld_cum_type = "body"
                "On her face":
                    $ _ld_cum_type = "face"

            call LD_CumOutsideFreeze(girl) from _call_LD_CumOutsideFreeze_tip_on

            if _ld_cum_type == "ass":
                "You pull out and cum on her ass."
                $ process_cum(girl, _ld_scene_type, "ass")
            elif _ld_cum_type == "body":
                "You pull out and cum on her body."
                $ process_cum(girl, _ld_scene_type, "body")
            else:
                "You pull out and cum on her face."
                $ process_cum(girl, _ld_scene_type, "face")

            $ apply_cum_bonuses(girl, "cum_outside")
            $ _cum_say_line(girl, _ld_cum_type, _ld_scene_type)

        "Ask to cum in her mouth":
            $ _cum_check = CumPermissionCheck(girl, "cum_in_mouth_ask")
            if _cum_check["accepted"]:
                $ Say_Line(girl, scene_pick_line("cum_mouth_accepted", scene=_ld_scene_type, girl=girl) or _("Go ahead... do it."))
                call _cum_in_mouth_via_bj(girl, _ld_scene_type) from _call_cum_in_mouth_via_bj_ld_tip
                $ _ld_mouth_via_bj = True
            else:
                $ set_scene_expression(girl, "angry")
                $ Say_Line(girl, scene_pick_line("cum_mouth_denied", scene=_ld_scene_type, girl=girl) or _("No way... not in my mouth."))
                call LD_CumOutsideFreeze(girl) from _call_LD_CumOutsideFreeze_tip_mouth_deny
                "You pull out and cum on her body instead."
                $ process_cum(girl, _ld_scene_type, "body")
                $ apply_cum_bonuses(girl, "cum_outside")

        "Ask to cum inside":
            call _tip_ask_cum_inside(girl, _ld_scene_type) from _call_tip_ask_ld

        "Cum inside her":
            call _tip_force_cum_inside(girl, _ld_scene_type) from _call_tip_force_ld

    return


# ═══════════════════════════════════════════════════════════
# _ld_turn_head — Obed check to hide face
# ═══════════════════════════════════════════════════════════

label _ld_turn_head(girl, ask=None):
    # ask: his words, for a pose where "look away" reads wrong (the doggy: "Turn your head forward.")
    $ Say_Player(ask or _("Look away for me."))
    if _ld_turn_check(girl):
        python:
            _tk = _ld_turn_trait_key(girl)
            _lines = _LD_TURN_ACCEPT_LINES.get(_tk, _LD_TURN_ACCEPT_LINES["_default"])
            _line = renpy.random.choice(_lines)
        $ Say_Line(girl, _tl(_line))
        $ store.hiding_face = True
    else:
        python:
            _tk = _ld_turn_trait_key(girl)
            _lines = _LD_TURN_REFUSE_LINES.get(_tk, _LD_TURN_REFUSE_LINES["_default"])
            _line = renpy.random.choice(_lines)
        $ Say_Line(girl, _tl(_line))
    return


# ═══════════════════════════════════════════════════════════
# _ld_secret_recording — she's hiding face, can't see phone
# ═══════════════════════════════════════════════════════════

label _ld_secret_recording(girl, scene_type="laying_down"):
    python:
        # The type must say what was filmed: anal in this position is "laying_anal", and the
        # masturbation flow shares this label ("masturbate"). It used to be always "laying_down".
        _ld_vid_type = live_scene_type(scene_type)
        store._ld_secret_caught_end = False
        store._recording_active = True
        store._recording_girl = girl
        store._recording_face_locked = False
        store._player_hand_disabled = renpy.random.choice(["left", "right"])
        vid = {
            "girl_gid": girl.gid,
            "type": _ld_vid_type,
            "location": CurrentLocation,
            "committed": girl.has_npc_partner(),
            "consensual": False,
            "reluctant": False,
            "face_hidden": True,
            "hd": Player.has_item("tekmix_camera"),
            "snapshot": _make_vid_snapshot(girl),
        }
        if scene_type_is_penetration(_ld_vid_type):
            vid["condom"] = bool(store.condom_active)
        _tag_coercion_on_vid(vid)
        store.Player.recorded_videos.append(vid)
        print("[RECORDING] %s secret LD recording: type=%s" % (girl.gid, _ld_vid_type))
        renpy.show_screen("recording_overlay")
    $ _sec_txt = _tl(_("You quietly pull out your phone and start recording. She can't see a thing."))
    "[_sec_txt]"
    return


# ═══════════════════════════════════════════════════════════
# _ld_look_back_during_recording — discovers secret recording
# ═══════════════════════════════════════════════════════════

label _ld_look_back_during_recording(girl):
    $ store._ld_secret_caught_end = False
    python:
        _was_secret = False
        for _vid in reversed(store.Player.recorded_videos):
            if _vid.get("girl_gid") == girl.gid and not _vid.get("consensual", True) and _vid.get("face_hidden", False):
                _vid["face_hidden"] = False
                _was_secret = True
                break

    if _was_secret:
        $ _disc_txt = _tl(_("She turns her head and immediately spots your phone."))
        "[_disc_txt]"
        $ set_scene_expression(girl, "surprised", blush="1")
        if girl.has_trait("camera_hater"):
            $ Say_Line(girl, _tl(_("Are you recording me?! What the hell is wrong with you?!")))
            $ set_scene_expression(girl, "angry", blush="1")
            $ Change_Status(girl, "Love", -10)
            $ Change_Status(girl, "Inbt", 15)
            $ finalize_recording()
            $ _kick_txt = _tl(_("She pushes you off and gets up, furious."))
            "[_kick_txt]"
            $ store._ld_secret_caught_end = True
        elif girl.has_trait("camera_lover"):
            $ Say_Line(girl, _tl(_("Wait... are you filming? ...You sneaky bastard. At least get my good side.")))
            $ set_scene_expression(girl, "lusty", blush="2")
            $ Change_Status(girl, "Love", 3)
        elif girl.has_trait("cum_slut"):
            $ Say_Line(girl, _tl(_("You were recording this whole time? ...Honestly, that's kind of hot.")))
            $ set_scene_expression(girl, "lusty", blush="2")
        elif girl.has_trait("lesbian"):
            $ Say_Line(girl, _tl(_("You were filming me?! With a guy?! Are you insane?!")))
            $ set_scene_expression(girl, "angry", blush="1")
            $ Change_Status(girl, "Love", -8)
            $ Change_Status(girl, "Inbt", 10)
            $ finalize_recording()
            $ _kick_txt = _tl(_("She pushes you off and gets up, furious."))
            "[_kick_txt]"
            $ store._ld_secret_caught_end = True
        else:
            $ Say_Line(girl, _tl(_("Wait, is that... are you recording?! Since when?!")))
            $ set_scene_expression(girl, "angry", blush="1")
            $ Change_Status(girl, "Love", -5)
            $ Change_Status(girl, "Inbt", 5)
            $ finalize_recording()
            $ _kick_txt = _tl(_("She pushes you off and gets up, furious."))
            "[_kick_txt]"
            $ store._ld_secret_caught_end = True
    else:
        $ _look_txt = _tl(_("You tell her to look back at you."))
        "[_look_txt]"

    return


# ═══════════════════════════════════════════════════════════
# LD MASTURBATION — Tenny-exclusive laying down masturbation
# Replaces the cowgirl-based MASTURBATE_* flow for Tenny.
# Uses Torso 2, open legs, masturbation arm/hand.
# ═══════════════════════════════════════════════════════════

label LD_MASTURBATE_ApplySpeed(girl, speed=0):

    python:
        _hide_scene_layers("laying_down")

        _is_masting = (speed >= 1)

        if _is_masting and getattr(girl, "Panties", None) and girl.clothes_state.get("panties") == "full":
            girl.DisplacePanties(pose="laying_down", refresh=False)

        _is_oral = _is_masting and getattr(store, "_oral_active", False)

        if _is_oral:
            store._ld_torso_variant = 1
            store._ld_arm_variant = 2
        else:
            store._ld_torso_variant = 2
            store._ld_arm_variant = 1

        slot_at = [ld_get_slot_transform(0)]
        ass_at = [ld_get_ass_transform(0)]

        # ── Legs (open right for masturbation — both layers always visible) ──
        renpy.show("tenny laying_legs_left", tag="ld_legs_left", at_list=slot_at, zorder=_LD_Z_LEGS)
        renpy.show("tenny laying_legs_open_right", tag="ld_legs_right", at_list=slot_at, zorder=_LD_Z_LEGS + 1)
        renpy.show("tenny laying_legs_open_right_2", tag="ld_legs_right_2", at_list=slot_at, zorder=_LD_Z_LEGS + 2)

        # ── Pelvis ──
        renpy.show("tenny laying_pelvis", tag="ld_pelvis", at_list=ass_at, zorder=_LD_Z_PELVIS)

        # ── Torso + Arms (oral=T1 normal pose, masturbation=T2 + mast arm) ──
        if _is_oral:
            _ld_show_torso(girl, slot_at)
        else:
            renpy.show("tenny laying_torso_2", tag="ld_torso", at_list=slot_at, zorder=_LD_Z_TORSO)
            renpy.show("tenny laying_t2_arm_left_1", tag="ld_arm_left", at_list=slot_at, zorder=_LD_Z_ARMS_BELOW)
            renpy.hide("ld_arm_right")
            renpy.show("tenny laying_t2_arm_mast", tag="ld_mast_arm", at_list=slot_at, zorder=_LD_Z_ARMS_BELOW - 1)

        # ── Masturbation animated layers OR oral tongue ──
        if _is_masting:
            if _is_oral:
                debug_log("[LD_MAST_APPLY] path=ORAL: showing tongue, hiding hand anim")
                _tongue_img = "player_tongue_s%d" % min(speed, 3)
                renpy.show(_tongue_img, tag="ld_mast_tongue", at_list=[ld_tongue_pos], zorder=_LD_Z_TONGUE)
                renpy.hide("ld_mast_anim")
                if getattr(store, "_ld_mast_t0", None) is None:
                    import time as _time
                    store._ld_mast_t0 = _time.time()
                store._ld_mast_speed = speed
            else:
                import time as _time
                _prev_speed = getattr(store, "_ld_mast_speed", 0)
                _set_changed = (speed <= 1) != (_prev_speed <= 1) and _prev_speed > 0
                if getattr(store, "_ld_mast_t0", None) is None or _set_changed:
                    store._ld_mast_t0 = _time.time()
                elif _prev_speed != speed and speed > 1:
                    _now = _time.time()
                    _old_dur = _MAST_FRAME_DURS.get(_prev_speed, 0.042)
                    _new_dur = _MAST_FRAME_DURS.get(speed, 0.042)
                    _cpos = int((_now - store._ld_mast_t0) / _old_dur) % 60
                    store._ld_mast_t0 = _now - (_cpos * _new_dur)
                store._ld_mast_speed = speed
                _mast_img = "tenny laying_mast_pre_insert" if speed <= 1 else "tenny laying_mast_insert"
                renpy.show(_mast_img, tag="ld_mast_anim", at_list=ass_at, zorder=_LD_Z_MAST_OVER)
        else:
            store._ld_mast_t0 = None
            renpy.hide("ld_mast_anim")

        # ── Clothing (T2 variants) ──
        _ld_show_clothing(girl, slot_at)

        # ── Ass base ──
        renpy.show("tenny laying_ass_base_left", tag="ld_ass_left", at_list=ass_at, zorder=_LD_Z_ASS)
        renpy.show("tenny laying_ass_base_right", tag="ld_ass_right", at_list=ass_at, zorder=_LD_Z_ASS + 1)
        if _is_masting and not _is_oral:
            renpy.hide("ld_before_pussy")
        elif _is_masting and _is_oral and getattr(girl, "_ld_after_pussy", False):
            renpy.show("tenny laying_mast_after_anim", tag="ld_before_pussy", at_list=ass_at, zorder=_LD_Z_BEFORE_PUSSY)
        else:
            _pussy_img = "tenny laying_after_pussy" if getattr(girl, "_ld_after_pussy", False) else "tenny laying_before_pussy"
            renpy.show(_pussy_img, tag="ld_before_pussy", at_list=ass_at, zorder=_LD_Z_BEFORE_PUSSY)
        if getattr(girl, "_ld_after_anal", False):
            renpy.show("tenny laying_after_ass", tag="ld_before_ass", at_list=ass_at, zorder=_LD_Z_BEFORE_ASS)
            renpy.hide("ld_before_ass_2")
        else:
            renpy.show("tenny laying_before_ass", tag="ld_before_ass", at_list=ass_at, zorder=_LD_Z_BEFORE_ASS)
            renpy.show("tenny laying_before_ass_2", tag="ld_before_ass_2", at_list=ass_at, zorder=_LD_Z_BEFORE_ASS + 1)

        # ── Panties (during masturbation, pants are hidden so panties always render) ──
        _pan_item = girl.Panties
        _legs_state = girl.clothes_state.get("skirt", "full") if girl.Legs else None
        _masting_mode = getattr(store, "_ld_masturbating", False)
        if _pan_item and (not girl.Legs or _legs_state == "up" or _masting_mode):
            _pan_state = girl.clothes_state.get("panties", "full")
            if _is_masting and _pan_state == "full":
                _ld_hide_panties()
            else:
                _pan_z = _LD_Z_PANTIES_DOWN if _pan_state == "down" else _LD_Z_PANTIES
                _pan_img = "tenny laying_panties_%s_%s" % (_pan_item, _pan_state)
                if renpy.has_image(_pan_img, exact=True):
                    renpy.show(_pan_img, tag="ld_panties", at_list=ass_at, zorder=_pan_z)
                else:
                    _ld_hide_panties()
        else:
            _ld_hide_panties()

        # ── Pants ──
        _ld_show_pants(girl, slot_at, ass_at)

        # ── Head ──
        _st = sprite_state.get(girl.Id, {})
        _ld_eyes = _laying_safe(_st.get("eyes", "eyes_normal"))
        _ld_brows = _laying_safe(_st.get("brows", "brows_normal"))
        _ld_mouth = _laying_safe(_st.get("mouth", "mouth_normal"))
        _ld_blush = _attr_for_blush(girl)
        renpy.show("tenny laying %s %s %s %s" % (_ld_eyes, _ld_brows, _ld_mouth, _ld_blush), tag="tenny", at_list=slot_at, zorder=_LD_Z_HEAD)

        # ── Cum layers ──
        renpy.show("tenny laying_cum_vaginal", tag="ld_cum_vaginal", at_list=ass_at, zorder=_LD_Z_CUM)
        renpy.show("tenny laying_cum_anal", tag="ld_cum_anal", at_list=ass_at, zorder=_LD_Z_CUM)
        renpy.show("tenny laying_cum_ass", tag="ld_cum_ass", at_list=slot_at, zorder=_LD_Z_CUM + 1)
        renpy.show("tenny laying_cum_body", tag="ld_cum_body", at_list=slot_at, zorder=_LD_Z_CUM + 2)
        renpy.show("tenny laying_cum_face", tag="ld_cum_face", at_list=slot_at, zorder=_LD_Z_CUM + 3)
        renpy.show("tenny laying_cum_mouth", tag="ld_cum_mouth", at_list=slot_at, zorder=_LD_Z_CUM + 3)
        _cum = getattr(girl, "Cum", [])
        if "dripping" in _cum or "dripping_ass" in _cum:
            renpy.show("tenny laying_cum_girl", tag="ld_cum_girl", at_list=ass_at, zorder=_LD_Z_CUM_GIRL)

        for _t in ("ld_penis", "ld_condom", "ld_guy_legs_1", "ld_guy_legs_2",
                    "ld_guy_calf_1", "ld_guy_calf_2", "ld_guy_pelvis",
                    "ld_guy_pelvis_safe"):
            renpy.hide(_t)

        debug_log("[LD_MAST_APPLY] speed=%d masting=%s oral=%s" % (speed, _is_masting, _is_oral))

    return


# ── LD Masturbation Launch ──
label LD_MASTURBATE_Launch(girl):
    $ _kill_scene_threads()
    $ _hide_all_scene_layers(girl)

    $ girl._prev_pose = getattr(girl, "default_pose", "standing")
    $ girl._prev_slot = getattr(girl, "SpriteLoc", StageCenter)
    if not getattr(girl, "_saved_outfit", None):
        $ girl.SaveOutfit()

    python:
        store._laying_girl = girl
        store._cowgirl_girl = girl
        store.cowgirl_started = False
        store.laying_started = False
        store.laying_rub_mode = False
        store.laying_tip_mode = False
        store.laying_anal = False
        store._ld_torso_variant = 2
        store._ld_arm_variant = 1
        store._ld_masturbating = True
        store.hiding_face = False
        store._oral_active = getattr(store, "_oral_active", False)
        sprite_state.setdefault(girl.Id, {})["pose"] = "laying_down"
        renpy.invoke_in_thread(_ld_blink_loop, girl)
        renpy.invoke_in_thread(_laying_expression_cycle, girl)

    if "laying_speed" not in globals():
        $ laying_speed = 0

    call LD_MASTURBATE_ApplySpeed(girl, 0) from _call_LD_MAST_AS_launch
    with fade

    if girl.Legs is not None or girl.Panties is not None:
        $ Say_Line(girl, _("Here... let me give you a better view."))

    if girl.Legs is not None:
        pause 0.8
        $ girl.Outfit_Change(legs_down=True, pose="laying_down")
        call LD_MASTURBATE_ApplySpeed(girl, laying_speed) from _call_LD_MAST_AS_strip1

    if girl.Panties is not None:
        pause 0.15
        menu:
            "Remove panties":
                $ girl.Outfit_Change(panties="none", pose="laying_down")
                call LD_MASTURBATE_ApplySpeed(girl, laying_speed) from _call_LD_MAST_AS_strip2

            "Pull panties to the side" if _item_has_state(girl, "panties", "side"):
                $ girl.clothes_state["panties"] = "side"
                call LD_MASTURBATE_ApplySpeed(girl, laying_speed) from _call_LD_MAST_AS_strip3

            "Pull panties down" if _item_has_state(girl, "panties", "down"):
                $ girl.clothes_state["panties"] = "down"
                call LD_MASTURBATE_ApplySpeed(girl, laying_speed) from _call_LD_MAST_AS_strip4

    $ _exp = girl.RegisterAction("player_saw_pussy")
    if _exp["first_time"]:
        call FirstExposureReaction(girl, "pussy") from _call_FER_ld_mast

    return


# ── LD Masturbation Launch (caught variant) ──
label LD_MASTURBATE_Launch_Caught(girl):

    $ girl._prev_pose = getattr(girl, "default_pose", "standing")
    $ girl._prev_slot = getattr(girl, "SpriteLoc", StageCenter)
    if not getattr(girl, "_saved_outfit", None):
        $ girl.SaveOutfit()

    python:
        store._laying_girl = girl
        store._cowgirl_girl = girl
        store.cowgirl_started = False
        store.laying_started = False
        store._ld_torso_variant = 2
        store._ld_arm_variant = 1
        store._ld_masturbating = True
        sprite_state.setdefault(girl.Id, {})["pose"] = "laying_down"
        renpy.invoke_in_thread(_ld_blink_loop, girl)
        renpy.invoke_in_thread(_laying_expression_cycle, girl)

    call LD_MASTURBATE_ApplySpeed(girl, laying_speed) from _call_LD_MAST_AS_caught

    with fade

    return


# ── LD Masturbation Control Menu ──
label LD_MASTURBATE_ControlMenu(girl):

    $ store._scene_phase = "masturbate"
    if "laying_speed" not in globals():
        $ laying_speed = 0
    $ store._mast_stop_asked = 0
    $ store._mast_sex_asks = 0

    while True:

        if _scene_should_exit() or store._laying_girl is None:
            $ print("[LD_MAST_LOOP] EXIT: scene_should_exit=%s laying_girl_none=%s" % (_scene_should_exit(), store._laying_girl is None))
            return

        if Round >= 100:
            $ Say_Line(girl, _scene_time_up_line())
            call LD_End(girl, dress_up=False) from _call_LD_End_timeout_mast
            return

        menu:
            "Keep going" if laying_speed >= 1:
                $ advance_round(TIME_COSTS["sex_tick"])
                python:
                    _mast_phase = "oral" if getattr(store, "_oral_active", False) else "masturbate"
                    if _mast_phase == "oral":
                        _mast_lust = 4 if laying_speed == 1 else 7 if laying_speed == 2 else 10
                    else:
                        _mast_lust = 2 if laying_speed == 1 else 4 if laying_speed == 2 else 6
                $ _girl_lust_gain(girl, _mast_lust, laying_speed)
                $ _moan = scene_moan_tick(girl, _mast_phase, laying_speed)
                if _moan:
                    call _moan_say(girl, _moan) from _call_ms_ld_mast
                if girl.Lust >= 100:
                    call GirlCumming(girl, _mast_phase, "laying_down") from _call_GirlCumming_ld_mast

                python:
                    _flags = getattr(girl, "intimacy_flags", set()) or set()
                    _has_sex_history = bool(_flags & {"sex", "bj", "hj", "tj"})
                    _is_lesbian = girl.has_trait("lesbian")
                    _msa = getattr(store, "_mast_sex_asks", 0)
                    _escalate_chance = 0
                    if getattr(store, "_oral_active", False):
                        _escalate_chance = 0
                    elif story_act_locked(girl, "sex"):
                        # a girl with a story never begs for the act her own step refuses (tester 2026-10-10:
                        # she asked for "the real thing" and then story-declined it at the sex menu)
                        print("[LD_MAST_LOOP] escalation ask skipped: %s, her story locks sex (step %s)" % (girl.gid, story_step_id(girl)))
                    elif girl.Lust >= 55 and _has_sex_history and _msa < 3 and not _is_lesbian:
                        _escalate_chance = min(15 + (girl.Lust - 55) + _msa * 12, 50)
                    _wants_sex = _escalate_chance > 0 and renpy.random.randint(1, 100) <= _escalate_chance
                if _wants_sex:
                    python:
                        store._mast_sex_asks += 1
                        _n = store._mast_sex_asks
                    if _n <= 2:
                        if _n == 1:
                            $ Say_Line(girl, _("I need the real thing... please."))
                        else:
                            $ Say_Line(girl, _("Please... my fingers aren't enough anymore... I need you."))
                        menu:
                            "Give her what she wants":
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
                                    call LD_End(girl, dress_up=False) from _call_LD_End_mastesc
                                    call sex_menu(girl, CurrentLocation, store.TimeIndex) from _call_sex_menu_ld_mastesc
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
                        call _mast_desperate_negotiation(girl) from _call_mast_desp_neg_ld
                        if store._mast_desp_result == "sex":
                            return
                        if store._mast_desp_result == "kicked":
                            # She already told him to leave: silent redress, then the
                            # centralized angry kick-out (expression, angry status, narration, campus).
                            $ print("[MAST_DESP] kicked: %s rejected 3rd ask -> angry kick-out (laying_down)" % girl.gid)
                            call LD_End(girl, dress_up=False) from _call_LD_End_desp_kicked
                            call _scene_kick_to_campus(girl, mood="angry") from _call_kick_mast_desp_ld
                            return

            "Start" if laying_speed == 0:
                if getattr(store, "_oral_active", False):
                    $ laying_speed = 1
                    call LD_MASTURBATE_ApplySpeed(girl, laying_speed) from _call_LD_MAST_AS_start_oral
                    $ _girl_lust_gain(girl, 4, laying_speed)
                    $ _moan = scene_moan_tick(girl, "oral", laying_speed)
                    if _moan:
                        call _moan_say(girl, _moan) from _call_ms_ld_oral
                    if girl.Lust >= 100:
                        call GirlCumming(girl, "oral", "laying_down") from _call_GirlCumming_ld_mast_start_oral
                    $ Narration(_("You lean in and start."))
                else:
                    $ Say_Player(_("Go ahead... start touching yourself."))
                    $ laying_speed = 1
                    call LD_MASTURBATE_ApplySpeed(girl, laying_speed) from _call_LD_MAST_AS_start
                    $ _girl_lust_gain(girl, 2, laying_speed)
                    $ _moan = scene_moan_tick(girl, "masturbate", laying_speed)
                    if _moan:
                        call _moan_say(girl, _moan) from _call_ms_ld_mast2
                    if girl.Lust >= 100:
                        call GirlCumming(girl, "masturbate", "laying_down") from _call_GirlCumming_ld_mast_start
                    $ Narration(_("She begins to touch herself."))

            "Speed up" if laying_speed >= 1 and laying_speed < 3:
                $ advance_round(TIME_COSTS["sex_tick"])
                $ Say_Player(_("Faster..."))
                $ laying_speed += 1
                call LD_MASTURBATE_ApplySpeed(girl, laying_speed) from _call_LD_MAST_AS_speedup
                python:
                    _mast_phase_su = "oral" if getattr(store, "_oral_active", False) else "masturbate"
                    if _mast_phase_su == "oral":
                        _mast_lust_su = 4 if laying_speed == 1 else 7 if laying_speed == 2 else 10
                    else:
                        _mast_lust_su = 2 if laying_speed == 1 else 4 if laying_speed == 2 else 6
                $ _girl_lust_gain(girl, _mast_lust_su, laying_speed)
                $ _moan = scene_moan_tick(girl, _mast_phase_su, laying_speed)
                if _moan:
                    call _moan_say(girl, _moan) from _call_ms_ld_mast_su
                if girl.Lust >= 100:
                    call GirlCumming(girl, _mast_phase_su, "laying_down") from _call_GirlCumming_ld_mast_su
                if getattr(store, "_oral_active", False):
                    $ Narration(_("You speed up."))
                else:
                    $ Narration(_("She speeds up her movements."))

            "Speed down" if laying_speed > 0:
                $ advance_round(1)
                $ laying_speed -= 1
                call LD_MASTURBATE_ApplySpeed(girl, laying_speed) from _call_LD_MAST_AS_speeddown
                if getattr(store, "_oral_active", False):
                    $ Narration(_("You slow down."))
                else:
                    $ Narration(_("She slows down."))

            "Eat her out" if laying_speed >= 1 and not getattr(store, "_oral_active", False):
                $ _oral_appr = sex_action_check(girl, "oral")
                if _oral_appr["accepted"]:
                    $ store._oral_active = True
                    $ store._scene_phase = "oral"
                    $ girl.Sex_acts["oral"] = girl.Sex_acts.get("oral", 0) + 1
                    $ set_scene_expression(girl, "pleasure_mild")
                    call LD_MASTURBATE_ApplySpeed(girl, laying_speed) from _call_LD_MAST_AS_oral_on
                    $ Say_Line(girl, sex_line_for(girl, "oral", True))
                else:
                    $ Say_Line(girl, sex_line_for(girl, "oral", False))

            "Let her use her hands" if getattr(store, "_oral_active", False):
                $ store._oral_active = False
                $ store._scene_phase = "masturbate"
                call LD_MASTURBATE_ApplySpeed(girl, laying_speed) from _call_LD_MAST_AS_oral_off
                $ Narration(_("She starts touching herself again."))

            "Ask to hide her face" if laying_speed >= 1 and not store.hiding_face and not getattr(store, "_recording_active", False):
                call _ld_turn_head(girl) from _call_ld_turn_head_mast
                call LD_MASTURBATE_ApplySpeed(girl, laying_speed) from _call_LD_MAST_AS_hide

            "Tell her to look back" if store.hiding_face and not getattr(store, "_recording_active", False):
                $ store.hiding_face = False
                call LD_MASTURBATE_ApplySpeed(girl, laying_speed) from _call_LD_MAST_AS_show
                $ _turn_txt = _tl(_("She turns her head back to face you."))
                $ Narration(_turn_txt)

            "Strip her..." if not getattr(store, "_scene_restricted", False):
                $ advance_round(1)
                call _ld_strip_menu(girl) from _call_ld_strip_mast
                call LD_MASTURBATE_ApplySpeed(girl, laying_speed) from _call_LD_MAST_AS_strip

            "Record Options..." if not getattr(store, "_oral_active", False) and (not getattr(store, "_recording_active", False) or getattr(store, "_recording_girl", None) == girl):
                menu:
                    "Record her..." if not getattr(store, "_recording_active", False) and not store.hiding_face:
                        call _sex_phone_menu(girl, "masturbate") from _call__sex_phone_menu_ld_mast
                    "Record her..." if not getattr(store, "_recording_active", False) and store.hiding_face:
                        call _sex_phone_menu(girl, "masturbate") from _call__sex_phone_menu_ld_mast_hf
                    "Record without telling her" if not getattr(store, "_recording_active", False) and store.hiding_face:
                        call _ld_secret_recording(girl, "masturbate") from _call_ld_secret_recording_mast
                    "Ask [store._ntr_watching_npc.Name] to record" if store._ntr_partner_watching and not getattr(store, "_recording_active", False):
                        call _watcher_record_start(girl, "masturbate") from _call_watcher_rec_start_ld_mast_npc
                    "Ask [store._witness_girl.Name] to record" if getattr(store, "_witness_watching", False) and getattr(store, "_witness_girl", None) is not None and not store._ntr_partner_watching and not getattr(store, "_recording_active", False):
                        call _watcher_record_start(girl, "masturbate") from _call_watcher_rec_start_ld_mast_girl
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
                    "Order her to look back" if getattr(store, "hiding_face", False) and getattr(store, "_recording_active", False) and not getattr(store, "_recording_face_locked", False):
                        $ store.hiding_face = False
                        call _ld_look_back_during_recording(girl) from _call_ld_look_back_rec_mast
                    "Back":
                        pass
                if getattr(store, "_ld_secret_caught_end", False):
                    $ store._ld_secret_caught_end = False
                    call LD_End(girl, dress_up=False) from _call_LD_End_secret_caught_mast
                    return
                call LD_MASTURBATE_ApplySpeed(girl, laying_speed) from _call_LD_MAST_AS_rec

            "Stop now":
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
                            call LD_End(girl, dress_up=False) from _call_LD_End_mast_stop
                            $ store._mast_stop_asked = 0
                            return
                else:
                    $ Say_Line(girl, _("Alright..."))
                    call LD_End(girl, dress_up=False) from _call_LD_End_mast_stop2
                    $ store._mast_stop_asked = 0
                    return
