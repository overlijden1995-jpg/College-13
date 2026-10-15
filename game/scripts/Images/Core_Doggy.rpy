# ============================================================
# CORE DOGGY SYSTEM (vaginal + anal, no clothing/actions)
# ============================================================

image dg_condom = "images/characters/Player/Doggy Condom.png"
image dg_condom_broken = "images/characters/Player/Broken Doggy Condom.png"

default doggy_speed = 0
default doggy_started = False
default doggy_anal = False
default _doggy_girl = None
default doggy_blink = False
default doggy_rub_mode = False
default _dg_masturbating = False   # her solo scene in this pose (mast_pose "doggy", DG_MASTURBATE_*)
default _dg_massage = False        # the solo display borrowed by the massage / sunscreen (_rear_pose_for "doggy"): no hand of hers either
default doggy_tip_mode = False
default doggy_grab = False
# Read by the rub menu before any other doggy menu may have assigned it (NameError in old saves)
default _dg_scene_type = "doggy"

init python:
    # -----------------------------
    # DOGGY BLINK + EXPRESSION CYCLE
    # -----------------------------
    # Doggy-specific expression pools (girl seen from behind)
    _DG_EYES_BY_SPEED = {
        0: ["eyes_normal", "eyes_side", "eyes_closed"],
        1: ["eyes_normal", "eyes_side", "eyes_squint"],
        2: ["eyes_squint", "eyes_closed", "eyes_squint_big"],
        3: ["eyes_squint_big", "eyes_closed", "eyes_surprised"],
        4: ["eyes_closed", "eyes_squint_big"],
    }
    _DG_BROWS_BY_SPEED = {
        0: ["brows_normal"],
        1: ["brows_normal", "brows_confused"],
        2: ["brows_confused", "brows_surprised"],
        3: ["brows_surprised", "brows_horny"],
        4: ["brows_horny", "brows_surprised"],
    }
    _DG_MOUTH_BY_SPEED = {
        0: ["mouth_normal", "mouth_smile"],
        1: ["mouth_normal", "mouth_smile", "mouth_serious"],
        2: ["mouth_surprised", "mouth_open_teeth", "mouth_sch"],
        3: ["mouth_tongue", "mouth_surprised", "mouth_open_teeth"],
        4: ["mouth_tongue", "mouth_surprised"],
    }

    def _dg_cs_girls():
        return {gid for gid in GIRL_SCENE_CONFIG if GIRL_SCENE_CONFIG[gid].get("doggy", {}).get("uses_conditionswitch")}

    def dg_has_grab(girl):
        """His hands on her ass in this pose ("Grab her ass"): a girl with that art (GIRL_SCENE_CONFIG "has_grab")."""
        return bool(_gsc(girl.gid, "has_grab", True, "doggy"))

    def dg_has_hide_face(girl):
        """Her doggy art shows her face and can turn it away (GIRL_SCENE_CONFIG "has_hide_face"). Off by default: the
        standard doggy is seen from behind, every video of it is face hidden (_dg_ask_recording)."""
        return scene_has_hide_face(girl.gid, "doggy")

    def _doggy_expression_cycle(girl):
        _scene_expression_cycle(girl, "_doggy_girl", "doggy_speed",
            _DG_EYES_BY_SPEED, _DG_BROWS_BY_SPEED, _DG_MOUTH_BY_SPEED,
            sleep_range=(2.5, 5.0), cs_girls=_dg_cs_girls())

    # -----------------------------
    # TRANSFORM HELPERS
    # -----------------------------
    def dg_get_slot_transform(speed):
        slot_map = {0: dg_slot_speed0, 1: dg_slot_speed1, 2: dg_slot_speed2, 3: dg_slot_speed3, 4: dg_slot_speed4}
        return slot_map.get(speed, slot_map[1])

    def dg_get_butt_transform(speed):
        butt_map = {0: dg_butt_wobble_speed0, 1: dg_butt_wobble_speed1, 2: dg_butt_wobble_speed2, 3: dg_butt_wobble_speed3}
        return butt_map.get(speed, butt_map[1])

    def dg_get_butt_top_zoom_transform(speed):
        zoom_map = {0: dg_butt_top_zoom_speed0, 1: dg_butt_top_zoom_speed1, 2: dg_butt_top_zoom_speed2, 3: dg_butt_top_zoom_speed3}
        return zoom_map.get(speed, zoom_map[0])

    def dg_get_butt_shrink_transform(speed):
        m = {0: dg_butt_shrink_speed0, 1: dg_butt_shrink_speed1, 2: dg_butt_shrink_speed2, 3: dg_butt_shrink_speed3}
        return m.get(speed, m[0])

    def dg_get_skirt_zoom_transform(speed):
        m = {0: dg_skirt_zoom_speed0, 1: dg_skirt_zoom_speed1, 2: dg_skirt_zoom_speed2, 3: dg_skirt_zoom_speed3}
        return m.get(speed, m[0])

    def dg_get_panties_zoom_transform(speed):
        m = {0: dg_skirt_zoom_speed0, 1: dg_skirt_zoom_speed1, 2: dg_skirt_zoom_speed2, 3: dg_skirt_zoom_speed3}
        return m.get(speed, m[0])

    def dg_get_leg_left_transform(speed):
        gid = store._doggy_girl.gid if store._doggy_girl else None
        overrides = _gsc(gid, "leg_left_transforms", None, "doggy")
        if overrides:
            tf_name = overrides.get(speed, overrides.get(0))
            return getattr(store, tf_name)()
        m = {0: dg_leg_left_speed0(), 1: dg_leg_left_speed1(), 2: dg_leg_left_speed2(), 3: dg_leg_left_speed3()}
        return m.get(speed, dg_leg_left_speed0())

    def dg_get_leg_right_transform(speed):
        gid = store._doggy_girl.gid if store._doggy_girl else None
        overrides = _gsc(gid, "leg_right_transforms", None, "doggy")
        if overrides:
            tf_name = overrides.get(speed, overrides.get(0))
            return getattr(store, tf_name)()
        m = {0: dg_leg_right_speed0(), 1: dg_leg_right_speed1(), 2: dg_leg_right_speed2(), 3: dg_leg_right_speed3()}
        return m.get(speed, dg_leg_right_speed0())

    def dg_get_penis_transform(speed):
        p_map = {0: dg_penis_speed0, 1: dg_penis_speed1, 2: dg_penis_speed2, 3: dg_penis_speed3, 4: dg_penis_speed4}
        return p_map.get(speed, p_map[1])

    def dga_get_penis_transform(speed):
        p_map = {0: dga_penis_speed0, 1: dga_penis_speed1, 2: dga_penis_speed2, 3: dga_penis_speed3, 4: dga_penis_speed4}
        return p_map.get(speed, p_map[1])

    # ---------------------------------------------------------
    # Rub-mode z-order helpers (centralized)
    # ---------------------------------------------------------
    def _dg_is_rub_mode():
        return getattr(store, "doggy_rub_mode", False) and not store.doggy_started

    def _dg_pen_z():
        if _dg_is_rub_mode():
            return 10102
        if getattr(store, "doggy_anal", False):
            return 10063
        return 10050

    def _dg_cum_z():
        return 10101 if _dg_is_rub_mode() else 10082

    # ---------------------------------------------------------
    # Base layer helpers — Clean Base (center/right/left) + overlays
    # ---------------------------------------------------------
    def _dg_show_preview_layers(girl, at_list, z):
        """Show all 5 base layers for preview/transitions/freeze.
        Center(z), Right(z+1), Left(z+2), Pussy(z+3), Ass(z+4)"""
        gid = girl.gid
        _had_p = getattr(store, "_dg_had_pussy", False)
        _had_a = getattr(store, "_dg_had_anal", False)
        _p_img = "%s doggy_ass_after_pussy" % gid if _had_p else "%s doggy_ass_before_pussy" % gid
        _a_img = "%s doggy_ass_after_ass" % gid if _had_a else "%s doggy_ass_before_ass" % gid
        renpy.show("%s doggy_ass_clean_center" % gid, tag="dg_base_center", at_list=at_list, zorder=z)
        renpy.show(_p_img, tag="dg_base_pussy", at_list=at_list, zorder=z + 1)
        renpy.show(_a_img, tag="dg_base_ass", at_list=at_list, zorder=z + 2)
        renpy.show("%s doggy_ass_clean_right" % gid, tag="dg_base_right", at_list=at_list, zorder=z + 3)
        renpy.show("%s doggy_ass_clean_left" % gid, tag="dg_base_left", at_list=at_list, zorder=z + 4)
        renpy.hide("dg_during")
        renpy.hide("dg_during_below")

    def _dg_hide_all_base():
        for tag in ("dg_base_center", "dg_base_right", "dg_base_left",
                    "dg_base_pussy", "dg_base_ass", "dg_during", "dg_during_below"):
            renpy.hide(tag)

    def _dg_hide_panties():
        renpy.hide("dg_panties")
        renpy.hide("dg_panties_right")
        renpy.hide("dg_panties_left")

    def _dg_hide_all_layers():
        _hide_scene_layers("doggy")

    # ---------------------------------------------------------
    # SIMPLE PREVIEW — used during clothes menu / before penis enters
    # Shows only: body (layeredimage) + base overlay + legs + calves
    # Hides all splits, penis, safe, anus layers.
    # ---------------------------------------------------------
    def _dg_show_preview(girl):
        _hide_scene_layers("reverse_cowgirl")

        gid = girl.gid
        _slot = dg_get_slot_transform(0)

        # Build full attributes (clothing + collar) then force butt off
        attrs = _build_doggy_attributes(girl)
        attrs = [a for a in attrs if "butt_gap" not in a and "butt_top" not in a]
        attrs.extend(["butt_gap_none", "butt_top_none"])

        # Strip chest/over from layeredimage when standalone exists
        # (over layer in layeredimage is opaque and hides corset beneath it)
        _prev_chest_key = None
        _c_val = girl.clothes.get("chest")
        _c_map = {"corset": "doggy_corset", "crop_top": "doggy_corset", "bikini_top": "doggy_bikini_top"}
        _c_key = _c_map.get(_c_val)
        if _c_key and renpy.has_image("%s %s" % (gid, _c_key), exact=True):
            attrs = [a for a in attrs if "torso_chest" not in a]
            attrs.append("torso_chest_none")
            _prev_chest_key = _c_key

        _prev_over_key = None
        _o_val = girl.clothes.get("over")
        _o_map = {"long_shirt": "doggy_mesh_top"}
        _o_key = _o_map.get(_o_val)
        if _o_key and renpy.has_image("%s %s" % (gid, _o_key), exact=True):
            attrs = [a for a in attrs if "torso_over" not in a]
            attrs.append("torso_over_none")
            _prev_over_key = _o_key

        img_name = "%s doggy %s" % (gid, " ".join(attrs))
        debug_log("[DG_PREVIEW] layeredimage: %s" % img_name)
        debug_log("[DG_PREVIEW] clothes=%s states=%s" % (str(girl.clothes), str(girl.clothes_state)))

        renpy.show("%s doggy_boobs" % gid, tag="dg_boobs", at_list=[_slot], zorder=9979)
        renpy.show(
            img_name,
            tag=gid, at_list=[_slot], zorder=9980
        )
        renpy.show("%s doggy_calves_left" % gid, tag="dg_calves_left", at_list=[dg_calves_static], zorder=9970)
        renpy.show("%s doggy_calves_right" % gid, tag="dg_calves_right", at_list=[dg_calves_static], zorder=9970)
        renpy.show("%s doggy_legs_left" % gid, tag="dg_legs_left", at_list=[dg_calves_static], zorder=9972)
        renpy.show("%s doggy_legs_right" % gid, tag="dg_legs_right", at_list=[dg_calves_static], zorder=9972)
        renpy.show("%s doggy_foot_left" % gid, tag="dg_foot_left", at_list=[dg_calves_static], zorder=9974)
        renpy.show("%s doggy_foot_right" % gid, tag="dg_foot_right", at_list=[dg_calves_static], zorder=9974)

        # All 5 base layers (center + right + left + pussy + ass)
        _dg_show_preview_layers(girl, [_slot], 9990)

        # Hide sex-specific layers
        for _t in ("dg_penis", "dg_condom",
                    "dg_grab_left", "dg_grab_right",
                    "dg_body_safe",
                    "dg_ass_safe", "dg_penis_over",
                    "dg_during", "dg_during_below"):
            renpy.hide(_t)

        # Re-show chest/over as standalones above base layers
        if _prev_chest_key:
            renpy.show("%s %s" % (gid, _prev_chest_key), tag="dg_chest_over", at_list=[_slot], zorder=10052)
        else:
            renpy.hide("dg_chest_over")
        if _prev_over_key:
            renpy.show("%s %s" % (gid, _prev_over_key), tag="dg_over_above", at_list=[_slot], zorder=10054)
            _h_img = "%s doggy_head" % gid
            if renpy.has_image(_h_img, exact=True):
                renpy.show(_h_img, tag="dg_head_above", at_list=[_slot], zorder=10055)
        else:
            renpy.hide("dg_over_above")
            renpy.hide("dg_head_above")

        # --- Clothing standalones ---
        # Thigh highs
        if getattr(girl, "Shoes", None):
            debug_log("[DG_PREVIEW] showing thigh_highs (Shoes=%s)" % girl.Shoes)
            _thc_l = "%s doggy_thigh_highs_calves_left" % gid
            if renpy.has_image(_thc_l, exact=True):
                renpy.show(_thc_l, tag="dg_thigh_highs_calves_left", at_list=[dg_calves_static], zorder=9971)
                renpy.show("%s doggy_thigh_highs_calves_right" % gid, tag="dg_thigh_highs_calves_right", at_list=[dg_calves_static], zorder=9971)
                renpy.hide("dg_thigh_highs_calves")
            else:
                renpy.show("%s doggy_thigh_highs_calves" % gid, tag="dg_thigh_highs_calves", at_list=[dg_calves_static], zorder=9971)
            _thf_l = "%s doggy_thigh_highs_foot_left" % gid
            if renpy.has_image(_thf_l, exact=True):
                renpy.show(_thf_l, tag="dg_thigh_highs_foot_left", at_list=[dg_calves_static], zorder=9975)
                renpy.show("%s doggy_thigh_highs_foot_right" % gid, tag="dg_thigh_highs_foot_right", at_list=[dg_calves_static], zorder=9975)
                renpy.hide("dg_thigh_highs_foot")
            else:
                renpy.show("%s doggy_thigh_highs_foot" % gid, tag="dg_thigh_highs_foot", at_list=[dg_calves_static], zorder=9975)
            renpy.show("%s doggy_thigh_highs_legs_left" % gid, tag="dg_thigh_highs_legs_left", at_list=[dg_calves_static], zorder=9973)
            renpy.show("%s doggy_thigh_highs_legs_right" % gid, tag="dg_thigh_highs_legs_right", at_list=[dg_calves_static], zorder=9973)
        else:
            renpy.hide("dg_thigh_highs_foot")
            renpy.hide("dg_thigh_highs_calves")
            renpy.hide("dg_thigh_highs_foot_left")
            renpy.hide("dg_thigh_highs_foot_right")
            renpy.hide("dg_thigh_highs_calves_left")
            renpy.hide("dg_thigh_highs_calves_right")
            renpy.hide("dg_thigh_highs_legs_left")
            renpy.hide("dg_thigh_highs_legs_right")

        # Panties
        _pan_item = girl.Panties
        if _pan_item:
            _pan_state = girl.clothes_state.get("panties", "full")
            if _pan_state == "side":
                _pan_r = "%s doggy_panties_%s_side_right" % (gid, _pan_item)
                _pan_l = "%s doggy_panties_%s_side_left" % (gid, _pan_item)
                if renpy.has_image(_pan_r, exact=True) and renpy.has_image(_pan_l, exact=True):
                    renpy.show(_pan_r, tag="dg_panties_right", at_list=[_slot], zorder=10071)
                    renpy.show(_pan_l, tag="dg_panties_left", at_list=[_slot], zorder=10071)
                    renpy.hide("dg_panties")
                else:
                    _pan_img = "%s doggy_panties_%s_side" % (gid, _pan_item)
                    if store.doggy_anal:
                        _pan_img_anal = "%s doggy_panties_%s_side_anal" % (gid, _pan_item)
                        if renpy.has_image(_pan_img_anal, exact=True):
                            _pan_img = _pan_img_anal
                    if renpy.has_image(_pan_img, exact=True):
                        renpy.show(_pan_img, tag="dg_panties", at_list=[_slot], zorder=10079)
                        renpy.hide("dg_panties_right")
                        renpy.hide("dg_panties_left")
                    else:
                        _dg_hide_panties()
            else:
                _pan_img = "%s doggy_panties_%s_%s" % (gid, _pan_item, _pan_state)
                debug_log("[DG_PREVIEW] panties: img=%s has=%s" % (_pan_img, renpy.has_image(_pan_img, exact=True)))
                if renpy.has_image(_pan_img, exact=True):
                    renpy.show(_pan_img, tag="dg_panties", at_list=[_slot], zorder=10079)
                    renpy.hide("dg_panties_right")
                    renpy.hide("dg_panties_left")
                else:
                    _dg_hide_panties()
        else:
            debug_log("[DG_PREVIEW] no panties")
            _dg_hide_panties()

        # Skirt (use upskirt when already started — matches DG_ApplySpeed logic)
        if girl.Legs:
            _skirt_state = girl.clothes_state.get("skirt", "full")
            if store.doggy_started or _skirt_state == "up":
                _skirt_img = "%s doggy_skirt_up" % gid
                _skirt_safe = "%s doggy_skirt_up_safe" % gid
                if renpy.has_image(_skirt_img, exact=True):
                    renpy.show(_skirt_img, tag="dg_skirt", at_list=[_slot], zorder=10080)
                else:
                    renpy.hide("dg_skirt")
                if renpy.has_image(_skirt_safe, exact=True):
                    renpy.show(_skirt_safe, tag="dg_skirt_safe", at_list=[_slot], zorder=9985)
                else:
                    renpy.hide("dg_skirt_safe")
            else:
                _skirt_img = "%s doggy_skirt" % gid
                if renpy.has_image(_skirt_img, exact=True):
                    renpy.show(_skirt_img, tag="dg_skirt", at_list=[_slot], zorder=10080)
                else:
                    renpy.hide("dg_skirt")
                renpy.hide("dg_skirt_safe")
        else:
            debug_log("[DG_PREVIEW] no skirt")
            renpy.hide("dg_skirt")
            renpy.hide("dg_skirt_safe")

        # Shirt arms (standalone — above arms layer)
        _shirt_arms = "%s doggy_shirt_arms" % gid
        if girl.clothes.get("over") and renpy.has_image(_shirt_arms, exact=True):
            renpy.show(_shirt_arms, tag="dg_shirt_arms", at_list=[_slot], zorder=9981)
        else:
            renpy.hide("dg_shirt_arms")

    # ---------------------------------------------------------
    # BUTT LAYER DISPLAY — mode-specific layer stacking
    # ---------------------------------------------------------
    def _dg_show_butt_layers(girl, speed, butt_detail_at=None):
        if butt_detail_at is None:
            butt_detail_at = [dg_get_slot_transform(speed),
                              dg_get_butt_transform(speed),
                              dg_get_butt_shrink_transform(speed)]

        if not store.doggy_started:
            debug_log("[BUTT] preview mode (not started) speed=%d" % speed)
            _dg_show_preview_layers(girl, butt_detail_at, 9990)
            renpy.hide("dg_ass_safe")
            renpy.hide("dg_penis_over")
            return

        gid = girl.gid
        debug_log("[BUTT] speed=%d anal=%s had_p=%s had_a=%s" % (speed, store.doggy_anal, getattr(store, "_dg_had_pussy", False), getattr(store, "_dg_had_anal", False)))
        _had_p = getattr(store, "_dg_had_pussy", False)
        _had_a = getattr(store, "_dg_had_anal", False)

        _shrink_at = [dg_get_slot_transform(speed),
                      dg_get_butt_transform(speed),
                      dg_get_butt_shrink_transform(speed)]

        # z-order vaginal: center(9990) < during_below(10050) < body_safe(10051)
        #   < penis(10052) < during(10053) < base_ass(10054) < right/left(10055-10056)
        # z-order anal: center(9990) < body_safe(10059) < during_below(10060)
        #   < right/left(10061-10062) < penis(10063) < during(10064) < ass_safe(10068)
        _rl_z = 10061 if store.doggy_anal else 10055
        renpy.show("%s doggy_ass_clean_center" % gid, tag="dg_base_center", at_list=_shrink_at, zorder=9990)
        renpy.show("%s doggy_ass_clean_right" % gid, tag="dg_base_right", at_list=_shrink_at, zorder=_rl_z)
        renpy.show("%s doggy_ass_clean_left" % gid, tag="dg_base_left", at_list=_shrink_at, zorder=_rl_z + 1)

        if store.doggy_anal:
            _p_img = "%s doggy_ass_after_pussy" % gid if _had_p else "%s doggy_ass_before_pussy" % gid
            renpy.show(_p_img, tag="dg_base_pussy", at_list=_shrink_at, zorder=10051)
            if speed > 0:
                renpy.show("%s doggy_ass_during_anal_below" % gid, tag="dg_during_below", at_list=_shrink_at, zorder=10060)
                renpy.show("%s doggy_ass_during_anal" % gid, tag="dg_during", at_list=_shrink_at, zorder=10064)
                renpy.hide("dg_base_ass")
            else:
                _a_img = "%s doggy_ass_after_ass" % gid if _had_a else "%s doggy_ass_before_ass" % gid
                renpy.show(_a_img, tag="dg_base_ass", at_list=_shrink_at, zorder=10058)
                renpy.hide("dg_during_below")
                renpy.hide("dg_during")
            _asl = "%s doggy_ass_safe_layer" % gid
            if renpy.has_image(_asl, exact=True):
                renpy.show(_asl, tag="dg_ass_safe", at_list=_shrink_at, zorder=10068)
            else:
                renpy.hide("dg_ass_safe")
        else:
            _a_img = "%s doggy_ass_after_ass" % gid if _had_a else "%s doggy_ass_before_ass" % gid
            renpy.show(_a_img, tag="dg_base_ass", at_list=_shrink_at, zorder=10054)
            renpy.hide("dg_ass_safe")
            if speed > 0:
                renpy.show("%s doggy_ass_during_pussy_below" % gid, tag="dg_during_below", at_list=_shrink_at, zorder=10048)
                renpy.show("%s doggy_ass_during_pussy" % gid, tag="dg_during", at_list=_shrink_at, zorder=10053)
                renpy.hide("dg_base_pussy")
            else:
                _p_img2 = "%s doggy_ass_after_pussy" % gid if _had_p else "%s doggy_ass_before_pussy" % gid
                renpy.show(_p_img2, tag="dg_base_pussy", at_list=_shrink_at, zorder=10058)
                renpy.hide("dg_during_below")
                renpy.hide("dg_during")

# ═══════════════════════════════════════════════════════════
# CALVES (completely static — planted on ground, never moves)
# ═══════════════════════════════════════════════════════════
transform dg_cum_shake:
    xoffset 0 yoffset 0
    easein 0.03 xoffset 12 yoffset -8
    easeout 0.03 xoffset -10 yoffset 6
    easein 0.03 xoffset 8 yoffset -5
    easeout 0.03 xoffset -5 yoffset 3
    easein 0.02 xoffset 3 yoffset -2
    easeout 0.02 xoffset 0 yoffset 0

transform dg_calves_static:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0

# ═══════════════════════════════════════════════════════════
# SLOT TRANSFORMS (character body movement — synced with butt direction)
# ═══════════════════════════════════════════════════════════
transform dg_slot_speed0:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 0 zoom 1.0

transform dg_slot_speed1:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 0 zoom 1.0
    block:
        pause 0.35
        ease 0.20 yoffset -10 zoom 1.001
        pause 0.25
        ease 1.20 yoffset 0 zoom 1.0
        repeat

transform dg_slot_speed2:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 0 zoom 1.0
    block:
        pause 0.12
        ease 0.12 yoffset -14 zoom 1.002
        pause 0.10
        easein 0.45 yoffset 0 zoom 1.0
        repeat

transform dg_slot_speed3:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 0 zoom 1.0
    block:
        ease 0.18 yoffset -25 zoom 1.005
        easein 0.18 yoffset 0 zoom 1.0
        repeat

transform dg_slot_speed4:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset -7
    block:
        ease 0.17 yoffset -12
        easein 0.17 yoffset -7
        repeat

# ═══════════════════════════════════════════════════════════
# BUTT WOBBLE (overlay on butt detail layers)
# ═══════════════════════════════════════════════════════════
transform dg_butt_wobble_speed0:
    yoffset 0

transform dg_butt_wobble_speed1:
    yoffset 0
    block:
        pause 0.35
        ease 0.20 yoffset -24
        pause 0.25
        ease 1.20 yoffset 0
        repeat

transform dg_butt_wobble_speed2:
    yoffset 0
    block:
        pause 0.12
        ease 0.12 yoffset -28
        pause 0.10
        easein 0.45 yoffset 0
        repeat

transform dg_butt_wobble_speed3:
    yoffset 0
    block:
        ease 0.18 yoffset -28
        easein 0.18 yoffset 0
        repeat

# ═══════════════════════════════════════════════════════════
# BUTT TOP ZOOM (yzoom pulse on butt_top layers)
# ═══════════════════════════════════════════════════════════
transform dg_butt_top_zoom_speed0:
    zoom 1.0
    yoffset 0

transform dg_butt_top_zoom_speed1:
    subpixel True
    zoom 1.0
    yoffset 0
    block:
        pause 0.35
        ease 0.20 zoom 1.014 yoffset -5
        pause 0.25
        ease 1.20 zoom 1.0 yoffset 0
        repeat

transform dg_butt_top_zoom_speed2:
    subpixel True
    zoom 1.0
    yoffset 0
    block:
        pause 0.12
        ease 0.12 zoom 1.022 yoffset -8
        pause 0.10
        easein 0.45 zoom 1.0 yoffset 0
        repeat

transform dg_butt_top_zoom_speed3:
    subpixel True
    zoom 1.0
    yoffset 0
    block:
        ease 0.18 zoom 1.032 yoffset -12
        easein 0.18 zoom 1.0 yoffset 0
        repeat

# ═══════════════════════════════════════════════════════════
# BUTT BASE SHRINK (Clean Base Right/Left — zoom decreases on thrust)
# ═══════════════════════════════════════════════════════════
transform dg_butt_shrink_speed0:
    yoffset 0

transform dg_butt_shrink_speed1:
    subpixel True
    yoffset 0
    block:
        pause 0.35
        ease 0.20 yoffset -18
        pause 0.25
        ease 1.20 yoffset 0
        repeat

transform dg_butt_shrink_speed2:
    subpixel True
    yoffset 0
    block:
        pause 0.12
        ease 0.12 yoffset -22
        pause 0.10
        easein 0.45 yoffset 0
        repeat

transform dg_butt_shrink_speed3:
    subpixel True
    yoffset 0
    block:
        ease 0.18 yoffset -22
        easein 0.18 yoffset 0
        repeat

# ═══════════════════════════════════════════════════════════
# SKIRT / PANTIES ZOOM (bigger than butt zoom, lifts upward with thrust)
# Used for skirt_up and panties_side so they visibly follow the animation
# ═══════════════════════════════════════════════════════════
transform dg_skirt_zoom_speed0:
    zoom 1.0
    yoffset 0

transform dg_skirt_zoom_speed1:
    subpixel True
    zoom 1.0
    yoffset 0
    block:
        pause 0.35
        ease 0.20 zoom 1.025 yoffset -10
        pause 0.25
        ease 1.20 zoom 1.0 yoffset 0
        repeat

transform dg_skirt_zoom_speed2:
    subpixel True
    zoom 1.0
    yoffset 0
    block:
        pause 0.12
        ease 0.12 zoom 1.038 yoffset -16
        pause 0.10
        easein 0.45 zoom 1.0 yoffset 0
        repeat

transform dg_skirt_zoom_speed3:
    subpixel True
    zoom 1.0
    yoffset 0
    block:
        ease 0.18 zoom 1.055 yoffset -22
        easein 0.18 zoom 1.0 yoffset 0
        repeat

# ═══════════════════════════════════════════════════════════
# LEG ROTATION — LEFT (anchor 815, 600)
# ═══════════════════════════════════════════════════════════
transform dg_leg_left_speed0():
    subpixel True
    matrixanchor (815, 600)

transform dg_leg_left_speed1():
    subpixel True
    matrixanchor (815, 600)
    block:
        pause 0.35
        ease 0.20 matrixtransform RotateMatrix(0, 0, -8)
        pause 0.25
        ease 1.20 matrixtransform RotateMatrix(0, 0, 0)
        repeat

transform dg_leg_left_speed2():
    subpixel True
    matrixanchor (815, 600)
    block:
        pause 0.12
        ease 0.12 matrixtransform RotateMatrix(0, 0, -12)
        pause 0.10
        easein 0.45 matrixtransform RotateMatrix(0, 0, 0)
        repeat

transform dg_leg_left_speed3():
    subpixel True
    matrixanchor (815, 600)
    block:
        ease 0.18 matrixtransform RotateMatrix(0, 0, -14)
        easein 0.18 matrixtransform RotateMatrix(0, 0, 0)
        repeat

# ═══════════════════════════════════════════════════════════
# LEG ROTATION — RIGHT (anchor 1490, 500)
# ═══════════════════════════════════════════════════════════
transform dg_leg_right_speed0():
    subpixel True
    matrixanchor (1450, 600)

transform dg_leg_right_speed1():
    subpixel True
    matrixanchor (1450, 600)
    block:
        pause 0.35
        ease 0.20 matrixtransform RotateMatrix(0, 0, 8)
        pause 0.25
        ease 1.20 matrixtransform RotateMatrix(0, 0, 0)
        repeat

transform dg_leg_right_speed2():
    subpixel True
    matrixanchor (1450, 600)
    block:
        pause 0.12
        ease 0.12 matrixtransform RotateMatrix(0, 0, 12)
        pause 0.10
        easein 0.45 matrixtransform RotateMatrix(0, 0, 0)
        repeat

transform dg_leg_right_speed3():
    subpixel True
    matrixanchor (1450, 600)
    block:
        ease 0.18 matrixtransform RotateMatrix(0, 0, 14)
        easein 0.18 matrixtransform RotateMatrix(0, 0, 0)
        repeat

# ═══════════════════════════════════════════════════════════
# PENIS TRANSFORMS
# ═══════════════════════════════════════════════════════════
transform dg_penis_speed0:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    xoffset 0
    yoffset 100

transform dg_penis_speed1:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    xoffset 0
    yoffset 125
    block:
        pause 0.35
        ease 0.20 yoffset 10
        pause 0.25
        ease 1.20 yoffset 125
        repeat

transform dg_penis_speed2:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    xoffset 0
    yoffset 95
    block:
        pause 0.12
        ease 0.12 yoffset -60
        pause 0.10
        easein 0.45 yoffset 95
        repeat

transform dg_penis_speed3:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    xoffset 0
    yoffset 98
    block:
        ease 0.18 yoffset -140
        easein 0.18 yoffset 98
        repeat

transform dg_penis_speed4:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    xoffset 0
    yoffset 85
    block:
        ease 0.17 yoffset 15
        easein 0.17 yoffset 85
        repeat

# ═══════════════════════════════════════════════════════════
# ANAL PENIS TRANSFORMS (same timing, higher on Y axis)
# ═══════════════════════════════════════════════════════════
transform dga_penis_speed0:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    xoffset 0
    yoffset 85

transform dga_penis_speed1:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    xoffset 0
    yoffset 64
    block:
        pause 0.35
        ease 0.20 yoffset -15
        pause 0.25
        ease 1.20 yoffset 64
        repeat

transform dga_penis_speed2:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    xoffset 0
    yoffset 66
    block:
        pause 0.12
        ease 0.12 yoffset -85
        pause 0.10
        easein 0.45 yoffset 66
        repeat

transform dga_penis_speed3:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    xoffset 0
    yoffset 68
    block:
        ease 0.18 yoffset -135
        easein 0.18 yoffset 68
        repeat

transform dga_penis_speed4:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    xoffset 0
    yoffset 0
    block:
        ease 0.17 yoffset -70
        easein 0.17 yoffset 0
        repeat

# Penis slide-in (vaginal)
transform dg_penis_slide_in:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    alpha 1.0
    yoffset 350
    easein 0.45 yoffset 95

# Penis slide-in (anal — higher Y)
transform dga_penis_slide_in:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    alpha 1.0
    yoffset 350
    easein 0.45 yoffset 55

# Penis slide-out (vaginal)
transform dg_penis_slide_out:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    alpha 1.0
    yoffset 95
    easeout 0.45 yoffset 350

# Penis slide-out (anal)
transform dga_penis_slide_out:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    alpha 1.0
    yoffset 55
    easeout 0.45 yoffset 350

# ═══════════════════════════════════════════════════════════
# Slap transforms (hand flies in from side, pauses, flies out)
# ═══════════════════════════════════════════════════════════
transform dg_slap_right_in:
    subpixel True
    anchor (0.5, 0.5)
    xpos 1.3
    ypos 0.55
    alpha 1.0
    easein 0.08 xpos 0.55
    pause 0.15
    easeout 0.25 xpos -0.3 alpha 0.0

transform dg_slap_left_in:
    subpixel True
    anchor (0.5, 0.5)
    xpos -0.3
    ypos 0.55
    alpha 1.0
    easein 0.08 xpos 0.45
    pause 0.15
    easeout 0.25 xpos 1.3 alpha 0.0

# ═══════════════════════════════════════════════════════════
# DG_ApplySpeed — show/refresh all layers at given speed
# ═══════════════════════════════════════════════════════════
label DG_ApplySpeed(girl, speed=1):

    if girl.gid == "shion":
        $ _sdg_apply_speed(girl, speed)
        return

    $ penis_img = "%s doggy_penis" % girl.gid

    python:
        # Kill any leftover RCG layers first
        _hide_scene_layers("reverse_cowgirl")
        # Kill creampie dripping (shown by DG_CumAnim at z10059)
        renpy.hide("dg_ca_dripping")

        _is_anal = store.doggy_anal

        if not store.doggy_started:
            store._dg_butt_state = "base"
        elif speed >= 3:
            store._dg_butt_state = "butt_top_2"
        else:
            store._dg_butt_state = "base"

        _rub_mode = getattr(store, "doggy_rub_mode", False) and not store.doggy_started
        slot_transform = dg_get_slot_transform(speed)
        butt_transform = dg_get_butt_transform(speed)
        butt_top_zoom_transform = dg_get_butt_top_zoom_transform(speed)
        attrs = _build_doggy_attributes(girl)
        attrs = [a for a in attrs if "butt_gap" not in a and "butt_top" not in a]
        attrs.extend(["butt_gap_none", "butt_top_none"])

        _will_show_penis = (store.doggy_started and speed >= 1) or getattr(store, "doggy_rub_mode", False)

        # Always strip chest/over from layeredimage when standalone exists
        # (over layer is opaque and hides corset beneath it)
        _stripped_over = False
        _o_val = girl.clothes.get("over")
        _o_map_chk = {"long_shirt": "doggy_mesh_top"}
        _o_key_chk = _o_map_chk.get(_o_val)
        if _o_key_chk and renpy.has_image("%s %s" % (girl.gid, _o_key_chk), exact=True):
            attrs = [a for a in attrs if "torso_over" not in a]
            attrs.append("torso_over_none")
            _stripped_over = True

        _stripped_chest = False
        _c_val = girl.clothes.get("chest")
        _c_map_chk = {"corset": "doggy_corset", "crop_top": "doggy_corset", "bikini_top": "doggy_bikini_top"}
        _c_key_chk = _c_map_chk.get(_c_val)
        if _c_key_chk and renpy.has_image("%s %s" % (girl.gid, _c_key_chk), exact=True):
            attrs = [a for a in attrs if "torso_chest" not in a]
            attrs.append("torso_chest_none")
            _stripped_chest = True

        img_name = "%s doggy" % girl.gid
        if attrs:
            img_name += " " + " ".join(attrs)
        debug_log("[DG_APPLY] speed=%d started=%s anal=%s | img=%s" % (speed, store.doggy_started, store.doggy_anal, img_name))
        debug_log("[DG_APPLY] clothes=%s states=%s" % (str(girl.clothes), str(girl.clothes_state)))

        leg_left_transform = dg_get_leg_left_transform(speed)
        leg_right_transform = dg_get_leg_right_transform(speed)

        slot_at_list = [slot_transform]
        butt_shrink_transform = dg_get_butt_shrink_transform(speed)
        body_at_list = [slot_transform, butt_transform, butt_shrink_transform]
        butt_at_list = [slot_transform, butt_transform]
        butt_detail_at_list = butt_at_list + [butt_top_zoom_transform]

        # Clothing follows same movement as Base Left/Right
        clothing_at_list = body_at_list

        # Boobs (below body)
        renpy.show(
            "%s doggy_boobs" % girl.gid,
            tag="dg_boobs",
            at_list=slot_at_list,
            zorder=9979,
        )

        # Layeredimage (body, arms, head, expressions)
        renpy.show(
            img_name,
            tag=girl.gid,
            at_list=slot_at_list,
            zorder=9980
        )

        # Calves (split left/right — static, planted on ground)
        renpy.show(
            "%s doggy_calves_left" % girl.gid,
            tag="dg_calves_left",
            at_list=[dg_calves_static],
            zorder=9970,
        )
        renpy.show(
            "%s doggy_calves_right" % girl.gid,
            tag="dg_calves_right",
            at_list=[dg_calves_static],
            zorder=9970,
        )

        # Legs (split left/right — static position, rotation only)
        renpy.show(
            "%s doggy_legs_left" % girl.gid,
            tag="dg_legs_left",
            at_list=[dg_calves_static, leg_left_transform],
            zorder=9972,
        )
        renpy.show(
            "%s doggy_legs_right" % girl.gid,
            tag="dg_legs_right",
            at_list=[dg_calves_static, leg_right_transform],
            zorder=9972,
        )

        # Foot (split left/right — static, above calves)
        renpy.show(
            "%s doggy_foot_left" % girl.gid,
            tag="dg_foot_left",
            at_list=[dg_calves_static],
            zorder=9974,
        )
        renpy.show(
            "%s doggy_foot_right" % girl.gid,
            tag="dg_foot_right",
            at_list=[dg_calves_static],
            zorder=9974,
        )

        # Butt layers (base + top2 splits) — delegated to config-driven function
        _dg_show_butt_layers(girl, speed, body_at_list)

        # ── Clothing standalone layers ──
        debug_log("[DG_APPLY] Shoes=%s Panties=%s Legs=%s Over=%s Chest=%s" % (getattr(girl, "Shoes", None), girl.Panties, girl.Legs, girl.clothes.get("over"), girl.clothes.get("chest")))

        # Thigh highs (two parts: over calves + over legs)
        _shoes_val = getattr(girl, "Shoes", None)
        debug_log("[DG_APPLY] Shoes=%s clothes.shoes=%s" % (_shoes_val, girl.clothes.get("shoes")))
        if _shoes_val:
            _thc_l = "%s doggy_thigh_highs_calves_left" % girl.gid
            if renpy.has_image(_thc_l, exact=True):
                renpy.show(_thc_l, tag="dg_thigh_highs_calves_left", at_list=[dg_calves_static], zorder=9971)
                renpy.show("%s doggy_thigh_highs_calves_right" % girl.gid, tag="dg_thigh_highs_calves_right", at_list=[dg_calves_static], zorder=9971)
                renpy.hide("dg_thigh_highs_calves")
            else:
                _th_calves = "%s doggy_thigh_highs_calves" % girl.gid
                debug_log("[DG_APPLY] thigh_highs: calves=%s has=%s" % (_th_calves, renpy.has_image(_th_calves, exact=True)))
                renpy.show(_th_calves, tag="dg_thigh_highs_calves", at_list=[dg_calves_static], zorder=9971)
            _thf_l = "%s doggy_thigh_highs_foot_left" % girl.gid
            if renpy.has_image(_thf_l, exact=True):
                renpy.show(_thf_l, tag="dg_thigh_highs_foot_left", at_list=[dg_calves_static], zorder=9975)
                renpy.show("%s doggy_thigh_highs_foot_right" % girl.gid, tag="dg_thigh_highs_foot_right", at_list=[dg_calves_static], zorder=9975)
                renpy.hide("dg_thigh_highs_foot")
            else:
                renpy.show("%s doggy_thigh_highs_foot" % girl.gid, tag="dg_thigh_highs_foot", at_list=[dg_calves_static], zorder=9975)
            renpy.show(
                "%s doggy_thigh_highs_legs_left" % girl.gid,
                tag="dg_thigh_highs_legs_left",
                at_list=[dg_calves_static, leg_left_transform],
                zorder=9973,
            )
            renpy.show(
                "%s doggy_thigh_highs_legs_right" % girl.gid,
                tag="dg_thigh_highs_legs_right",
                at_list=[dg_calves_static, leg_right_transform],
                zorder=9973,
            )
        else:
            renpy.hide("dg_thigh_highs_foot")
            renpy.hide("dg_thigh_highs_calves")
            renpy.hide("dg_thigh_highs_foot_left")
            renpy.hide("dg_thigh_highs_foot_right")
            renpy.hide("dg_thigh_highs_calves_left")
            renpy.hide("dg_thigh_highs_calves_right")
            renpy.hide("dg_thigh_highs_legs_left")
            renpy.hide("dg_thigh_highs_legs_right")

        # Panties (standalone — state-driven)
        # During sex: only show side/down, never full (full hides the action)
        # Side panties split into right/left halves that follow each butt cheek
        # Down panties use clothing transforms (around thighs, looser motion)
        _pan_item = girl.Panties
        if _pan_item:
            _pan_state = girl.clothes_state.get("panties", "full")
            if store.doggy_started and _pan_state == "full":
                _dg_hide_panties()
            elif _pan_state == "side":
                # Try split right/left (each follows its butt cheek)
                _pan_r = "%s doggy_panties_%s_side_right" % (girl.gid, _pan_item)
                _pan_l = "%s doggy_panties_%s_side_left" % (girl.gid, _pan_item)
                if renpy.has_image(_pan_r, exact=True) and renpy.has_image(_pan_l, exact=True):
                    renpy.show(_pan_r, tag="dg_panties_right", at_list=clothing_at_list, zorder=10071)
                    renpy.show(_pan_l, tag="dg_panties_left", at_list=clothing_at_list, zorder=10071)
                    renpy.hide("dg_panties")
                else:
                    # Fallback: single side image (or anal variant)
                    _pan_img = "%s doggy_panties_%s_side" % (girl.gid, _pan_item)
                    if store.doggy_anal:
                        _pan_img_anal = "%s doggy_panties_%s_side_anal" % (girl.gid, _pan_item)
                        if renpy.has_image(_pan_img_anal, exact=True):
                            _pan_img = _pan_img_anal
                    renpy.show(_pan_img, tag="dg_panties", at_list=clothing_at_list, zorder=10079)
                    renpy.hide("dg_panties_right")
                    renpy.hide("dg_panties_left")
            else:
                _pan_img = "%s doggy_panties_%s_%s" % (girl.gid, _pan_item, _pan_state)
                if renpy.has_image(_pan_img, exact=True):
                    renpy.show(_pan_img, tag="dg_panties", at_list=clothing_at_list, zorder=10079)
                    renpy.hide("dg_panties_right")
                    renpy.hide("dg_panties_left")
                else:
                    _dg_hide_panties()
        else:
            _dg_hide_panties()

        # Skirt (standalone — state-driven)
        # During sex: skirt_up above butt (10080), skirt_up_safe below cheeks (10054)
        if girl.Legs:
            _skirt_state = girl.clothes_state.get("skirt", "full")
            if store.doggy_started or _skirt_state == "up":
                _skirt_img = "%s doggy_skirt_up" % girl.gid
                _skirt_safe = "%s doggy_skirt_up_safe" % girl.gid
                if renpy.has_image(_skirt_img, exact=True):
                    renpy.show(_skirt_img, tag="dg_skirt", at_list=clothing_at_list, zorder=10080)
                else:
                    renpy.hide("dg_skirt")
                if renpy.has_image(_skirt_safe, exact=True):
                    renpy.show(_skirt_safe, tag="dg_skirt_safe", at_list=clothing_at_list, zorder=9985)
                else:
                    renpy.hide("dg_skirt_safe")
            else:
                _skirt_img = "%s doggy_skirt" % girl.gid
                if renpy.has_image(_skirt_img, exact=True):
                    renpy.show(_skirt_img, tag="dg_skirt", at_list=clothing_at_list, zorder=10080)
                else:
                    renpy.hide("dg_skirt")
                renpy.hide("dg_skirt_safe")
        else:
            renpy.hide("dg_skirt")
            renpy.hide("dg_skirt_safe")

        # ── Shirt arms standalone ──
        _sa = "%s doggy_shirt_arms" % girl.gid
        if girl.clothes.get("over") and renpy.has_image(_sa, exact=True):
            renpy.show(_sa, tag="dg_shirt_arms", at_list=slot_at_list, zorder=9981)
        else:
            renpy.hide("dg_shirt_arms")

        # ── Penis ──
        _penis_speed = speed
        if _is_anal:
            _penis_tf = dga_get_penis_transform(_penis_speed)
        else:
            _penis_tf = dg_get_penis_transform(_penis_speed)

        _show_penis = (store.doggy_started and speed >= 1) or getattr(store, "doggy_rub_mode", False)
        _pen_z = _dg_pen_z()
        if _show_penis:
            if store.condom_active:
                _condom_img = _condom_img_tag("dg_condom")
                _penis_with_condom = Fixed(
                    renpy.displayable(penis_img),
                    renpy.displayable(_condom_img),
                    fit_first=True,
                )
                renpy.show("dg_penis_combined", what=_penis_with_condom, tag="dg_penis", at_list=[_penis_tf], zorder=_pen_z)
            else:
                renpy.show(penis_img, tag="dg_penis", at_list=[_penis_tf], zorder=_pen_z)
            renpy.hide("dg_condom")
            if store.doggy_started:
                _bs_z = 10051 if not _is_anal else 10059
                renpy.show("%s doggy_body_safe" % girl.gid, tag="dg_body_safe", at_list=slot_at_list, zorder=_bs_z)
                _chest_over_z = _bs_z + 1
                _c_val = girl.clothes.get("chest")
                _c_map = {"corset": "doggy_corset", "crop_top": "doggy_corset", "bikini_top": "doggy_bikini_top"}
                _c_key = _c_map.get(_c_val)
                if _c_key:
                    _c_img = "%s %s" % (girl.gid, _c_key)
                    if renpy.has_image(_c_img, exact=True):
                        renpy.show(_c_img, tag="dg_chest_over", at_list=slot_at_list, zorder=_chest_over_z)
                    else:
                        renpy.hide("dg_chest_over")
                else:
                    renpy.hide("dg_chest_over")
                _over_z = 10054 if not _is_anal else 10060
                _o_val = girl.clothes.get("over")
                _o_map = {"long_shirt": "doggy_mesh_top"}
                _o_key = _o_map.get(_o_val)
                if _o_key:
                    _o_img = "%s %s" % (girl.gid, _o_key)
                    if renpy.has_image(_o_img, exact=True):
                        renpy.show(_o_img, tag="dg_over_above", at_list=slot_at_list, zorder=_over_z)
                        _h_img = "%s doggy_head" % girl.gid
                        if renpy.has_image(_h_img, exact=True):
                            renpy.show(_h_img, tag="dg_head_above", at_list=slot_at_list, zorder=_over_z + 1)
                    else:
                        renpy.hide("dg_over_above")
                        renpy.hide("dg_head_above")
                else:
                    renpy.hide("dg_over_above")
                    renpy.hide("dg_head_above")
            else:
                renpy.hide("dg_body_safe")
                if _stripped_chest:
                    renpy.show("%s %s" % (girl.gid, _c_key_chk), tag="dg_chest_over", at_list=slot_at_list, zorder=10052)
                else:
                    renpy.hide("dg_chest_over")
                if _stripped_over:
                    renpy.show("%s %s" % (girl.gid, _o_key_chk), tag="dg_over_above", at_list=slot_at_list, zorder=10054)
                    _h_img = "%s doggy_head" % girl.gid
                    if renpy.has_image(_h_img, exact=True):
                        renpy.show(_h_img, tag="dg_head_above", at_list=slot_at_list, zorder=10055)
                else:
                    renpy.hide("dg_over_above")
                    renpy.hide("dg_head_above")
        else:
            renpy.hide("dg_penis")
            renpy.hide("dg_condom")
            renpy.hide("dg_body_safe")
            if _stripped_chest:
                renpy.show("%s %s" % (girl.gid, _c_key_chk), tag="dg_chest_over", at_list=slot_at_list, zorder=10052)
            else:
                renpy.hide("dg_chest_over")
            if _stripped_over:
                renpy.show("%s %s" % (girl.gid, _o_key_chk), tag="dg_over_above", at_list=slot_at_list, zorder=10054)
                _h_img = "%s doggy_head" % girl.gid
                if renpy.has_image(_h_img, exact=True):
                    renpy.show(_h_img, tag="dg_head_above", at_list=slot_at_list, zorder=10055)
            else:
                renpy.hide("dg_over_above")
                renpy.hide("dg_head_above")

        # ── Grab layers (above butt) ──
        _hand_disabled = getattr(store, "_player_hand_disabled", None)
        if _hand_disabled and not getattr(store, "_recording_active", False):
            store._player_hand_disabled = None
            _hand_disabled = None
        _slap_hide = getattr(store, "_slap_hide_hand", None)
        if store.doggy_grab:
            for _side in ("left", "right"):
                _gb_img = "%s doggy_grab_butt_%s" % (girl.gid, _side)
                _gb_tag = "dg_grab_%s" % _side
                _has_img = renpy.has_image(_gb_img, exact=True)
                debug_log("[GRAB] side=%s img=%s has_img=%s hand_disabled=%s slap_hide=%s" % (_side, _gb_img, _has_img, _hand_disabled, _slap_hide))
                if _hand_disabled != _side and _slap_hide != _side and _has_img:
                    renpy.show(_gb_img, tag=_gb_tag, at_list=butt_detail_at_list, zorder=10090)
                else:
                    debug_log("[GRAB] HIDING %s: disabled=%s slap=%s has_img=%s" % (_side, _hand_disabled == _side, _slap_hide == _side, _has_img))
                    renpy.hide(_gb_tag)
        else:
            renpy.hide("dg_grab_left")
            renpy.hide("dg_grab_right")

        # ── Cum layers (ConditionSwitch — auto-update) ──
        _cum_z = _dg_cum_z()
        # Butt cum (on her ass, follows same movement as Base Left/Right)
        renpy.show(
            "%s doggy_butt_cum" % girl.gid,
            tag="dg_butt_cum",
            at_list=body_at_list,
            zorder=_cum_z,
        )

        # Back cum (on her back, follows body slot)
        renpy.show(
            "%s doggy_back_cum" % girl.gid,
            tag="dg_back_cum",
            at_list=slot_at_list,
            zorder=_cum_z + 1,
        )

        # Dripping cum: just below penis
        _drip_z = _dg_pen_z() - 1
        if not getattr(store, "doggy_rub_mode", False):
            renpy.show(
                "%s doggy_dripping_cum" % girl.gid,
                tag="dg_dripping_cum",
                at_list=body_at_list,
                zorder=_drip_z,
            )
            renpy.show(
                "%s doggy_dripping_ass_cum" % girl.gid,
                tag="dg_dripping_ass_cum",
                at_list=body_at_list,
                zorder=_drip_z,
            )
        else:
            renpy.hide("dg_dripping_cum")
            renpy.hide("dg_dripping_ass_cum")

    return

# ═══════════════════════════════════════════════════════════
# DG_Launch — setup and first display
# ═══════════════════════════════════════════════════════════
label DG_Launch(girl, from_switch=False):
    $ sub_event_reset(girl)
    $ _kill_scene_threads(keep_watchers=from_switch)
    $ stop_standing_blink(girl)

    if not from_switch:
        $ public_attention_reset()

    python:
        # Clear other scene refs so set_scene_expression / blink threads
        # don't accidentally show layers from another position
        _clear_scene_refs("doggy")
        store.cowgirl_started = False
        store.cowgirl_masturbating = False

        # Hide all layers from other/previous scenes
        _hide_all_scene_layers(girl)

        _hide_non_scene_girls(girl)

        store.hiding_face = False
        store._doggy_girl = girl
        if not from_switch:
            girl._prev_pose = sprite_state.get(girl.Id, {}).get("pose", "standing")
            girl._prev_slot = getattr(girl, "_current_slot", StageCenter)
        sprite_state.setdefault(girl.Id, {})["pose"] = "doggy"
        store.doggy_speed = 0
        store.doggy_started = False
        store._dg_butt_state = "base"
        store._dg_had_pussy = False
        store._dg_had_anal = False

        _gid = girl.gid

        # Shion custom doggy: set her scene ref, init head position. Her sdg_* layers have their own tags: her standing
        # sprite (the tag the others' doggy layeredimage replaces, set_girl_sprite) has to go by hand
        if _gid == "shion":
            hide_girl_sprite(girl)
            sprite_state.setdefault(girl.Id, {})["pose"] = "doggy"
            store._sdg_girl = girl
            store._sdg_head_pos = 2   # head 2: her face turned to him, with expressions (head 1 = from behind, no face)
            store._sdg_butt_state = "closed"
            store._sdg_guy_on = False
        else:
            renpy.start_predict(
                "%s doggy_ass_clean_center" % _gid,
                "%s doggy_ass_clean_right" % _gid,
                "%s doggy_ass_clean_left" % _gid,
                "%s doggy_ass_before_pussy" % _gid,
                "%s doggy_ass_before_ass" % _gid,
                "%s doggy_ass_after_pussy" % _gid,
                "%s doggy_ass_after_ass" % _gid,
                "%s doggy_ass_during_pussy" % _gid,
                "%s doggy_ass_during_pussy_below" % _gid,
                "%s doggy_ass_during_anal" % _gid,
                "%s doggy_ass_during_anal_below" % _gid,
                "%s doggy_calves_left" % _gid,
                "%s doggy_calves_right" % _gid,
                "%s doggy_legs_left" % _gid,
                "%s doggy_legs_right" % _gid,
                "%s doggy_foot_left" % _gid,
                "%s doggy_foot_right" % _gid,
            )

    if from_switch:
        # Reset skirt state from previous position
        if girl.clothes_state.get("skirt") == "up":
            $ girl.clothes_state["skirt"] = "full"
        if girl.Panties is not None:
            $ girl.Outfit_Change(panties="none", pose="doggy")
        call DG_ApplySpeed(girl, 0) from _call_DG_ApplySpeed_launch_switch
        with dissolve
    else:
        if girl.gid == "shion":
            call DG_ApplySpeed(girl, 0) from _call_DG_ApplySpeed_shion_launch
        else:
            $ set_girl_sprite(girl, pose="doggy")
        with fade

        call _dg_bottom_clothes_menu(girl) from _call_dg_bottom_menu_launch

        call DG_ApplySpeed(girl, 0) from _call_DG_ApplySpeed_launch_init

    # Start blink + expression threads
    python:
        if girl.gid == "shion":
            renpy.invoke_in_thread(_scene_cs_blink_loop, girl, "_doggy_girl", blink_timing=(0.12, 0.22))
        else:
            renpy.invoke_in_thread(_scene_blink_loop, girl, "_doggy_girl", "doggy_blink", cs_girls=_dg_cs_girls(), blink_timing=(0.12, 0.22))
        renpy.invoke_in_thread(_doggy_expression_cycle, girl)
    return

# ═══════════════════════════════════════════════════════════
# DG_ControlMenu — main sex loop
# ═══════════════════════════════════════════════════════════
label DG_ControlMenu(girl, from_escalation=False):

    $ store._player_exhausted = False
    $ store._scene_phase = "sex"
    $ store._cheat_shower_max_act = "sex"
    $ _dg_scene_type = "anal" if store.doggy_anal else "doggy"

    if not from_escalation and not store.doggy_started:
        $ doggy_speed = 0
        if girl.gid == "shion":
            call DG_ApplySpeed(girl, 0) from _call_DG_ApplySpeed_control_preview_shion
        else:
            $ _dg_show_preview(girl)
        call _dg_bottom_clothes_menu(girl) from _call_dg_bottom_control_entry

    while True:
        $ _dg_scene_type = "anal" if store.doggy_anal else "doggy"
        if store._post_cum_pending:
            return

        if getattr(store, "_sub_event_position_switched", False):
            $ store._sub_event_position_switched = False
            return

        # Scene ended or forced out by a sub-call (force_scene_reset, hate_cum, exhaustion...)
        if _scene_should_exit() or store._doggy_girl is None:
            $ debug_log("[DG_LOOP] EXIT: scene_should_exit=%s doggy_girl_none=%s" % (_scene_should_exit(), store._doggy_girl is None))
            return

        if Round >= 100:
            $ Say_Line(girl, _scene_time_up_line())
            call DG_End(girl, dress_up=False) from _call_DG_End_timeout
            return

        menu:
            "Keep going" if store.doggy_started:
                $ _dg_lust = _anal_lust_for_speed(girl, doggy_speed) if store.doggy_anal else -1

                call _sex_scene_tick(girl, _dg_scene_type, doggy_speed, girl_lust=_dg_lust) from _call_sst_dg_kg

                $ _apply_anal_lust_cap(girl, store.doggy_anal)

                # Handle condom rip visual
                if store._sst_result == "condom_ripped":
                    call DG_CondomRemoveAnim(girl) from _call_DG_CondomRemoveAnim_sst_kg
                    call DG_ApplySpeed(girl, doggy_speed) from _call_DG_ApplySpeed_sst_rip

                # Handle abort
                if store._sst_result == "abort":
                    if store._sst_abort_reason == "post_cum":
                        $ _set_post_cum("anal" if store.doggy_anal else "doggy", "sex")
                        return
                    if store._sst_abort_reason == "position_switch":
                        return
                    else:
                        call _sex_scene_handle_abort(girl, _dg_scene_type) from _call_sst_abort_dg_kg
                        return

            "Speed up" if doggy_speed < 3:
                $ advance_round(TIME_COSTS["sex_tick"])
                $ doggy_speed += 1
                call DG_HoleTransition(girl, store.doggy_anal) from _call_DG_HoleTransition_su
                $ _moan = scene_moan_tick(girl, _dg_scene_type, doggy_speed)
                if _moan:
                    call _moan_say(girl, _moan) from _call_ms_dg_kg
                call DG_ApplySpeed(girl, doggy_speed) from _call_DG_ApplySpeed_su
                call _speed_change_tick(girl, _dg_scene_type, 1) from _call_sct_dg_su
                if _scene_should_exit():
                    return
                if doggy_speed >= 3:
                    $ _watcher_scene_comment("speed_max")

            "Slow down" if doggy_speed > 1:
                $ advance_round(1)
                $ doggy_speed -= 1
                call DG_ApplySpeed(girl, doggy_speed) from _call_DG_ApplySpeed_sd
                call _speed_change_tick(girl, _dg_scene_type, -1) from _call_sct_dg_sd
                if store._sub_event_position_switched:
                    return
                $ _watcher_scene_comment("speed_down")

            "Penetration..." if store.doggy_started:
                $ _es_from = "anal" if store.doggy_anal else "sex"
                call _escalation_menu(girl, "doggy") from _call_esc_menu_dg_sex
                if store._esc_result == "accepted":
                    call _dg_esc_dispatch(girl, _es_from, doggy_speed) from _call_esc_disp_dg_sex
                    # Dispatch may have ended the scene (e.g. cheat condom breakdown on anal->pussy): DG_End clears _doggy_girl
                    if store._esc_is_deescalation or store._doggy_girl is None:
                        $ debug_log("[DG_LOOP] EXIT after escalation: deesc=%s scene_ended=%s" % (store._esc_is_deescalation, store._doggy_girl is None))
                        return
                elif store._esc_result == "scene_ended":
                    call DG_End(girl, dress_up=False) from _call_DG_End_esc_sex
                    return
                # denied/cancelled: stay in sex menu
            "Grab her ass" if store.doggy_started and not store.doggy_grab and dg_has_grab(girl):
                $ advance_round(1)
                $ store.doggy_grab = True
                call DG_ApplySpeed(girl, doggy_speed) from _call_DG_ApplySpeed_grab
                python:
                    _grab_react = renpy.random.choice(["mouth_surprised", "mouth_tongue", "mouth_kiss"])
                    set_scene_expression(girl, None, mouth=_grab_react)
                call DG_ApplySpeed(girl, doggy_speed) from _call_DG_ApplySpeed_grab_react

            "Let go" if store.doggy_grab:
                $ advance_round(1)
                $ store.doggy_grab = False
                call DG_ApplySpeed(girl, doggy_speed) from _call_DG_ApplySpeed_letgo

            "Tease her..." if store.doggy_started and doggy_speed > 0:
                $ advance_round(1)
                call _tease_menu(girl, _dg_scene_type) from _call_tease_menu_dg

            "Spank her" if store.doggy_started:
                $ advance_round(1)
                call SpankHer(girl, _dg_scene_type) from _call_SpankHer_dg

            # Her hand on herself while he is in her ass (girls with the art: self_touch_anal in GIRL_SCENE_CONFIG;
            # never in her pussy, the layers read _dg_masturbating). Her yes is the "masturbate" lewd rule, with
            # what she already gave him in this scene on top.
            "Tell her to touch herself" if store.doggy_started and store.doggy_anal and not store._dg_masturbating and _gsc(girl.gid, "self_touch_anal", False, "doggy"):
                $ advance_round(1)
                $ Say_Player(_("Touch yourself while I fuck your ass."))
                python:
                    _ts_rule = dict(ApprovalRuleFor(girl, "masturbate", "lewd"))
                    _ts_rule["Bonus"] = _ts_rule.get("Bonus", 0) + 150   # she is already taking him in the ass
                    _ts_res = ApprovalCheck(girl, ReturnData=True, Action="masturbate", **_ts_rule)
                    print("[DG_TOUCH_SELF] %s accepted=%s score=%s" % (girl.gid, _ts_res["accepted"], _ts_res.get("score")))
                if _ts_res["accepted"]:
                    $ store._dg_masturbating = True
                    $ set_scene_expression(girl, None, mouth="mouth_lipbite", eyes="eyes_closed")
                    $ Say_Line(girl, renpy.random.choice([_("Mmh... like this?"), _("God... fine. Keep going, don't stop."), _("You want a show too? Greedy...")]))
                    $ Change_Status(girl, "Lust", 5)
                    call DG_ApplySpeed(girl, doggy_speed) from _call_DG_ApplySpeed_touch_self
                else:
                    $ set_scene_expression(girl, None, mouth="mouth_sad", brows="brows_angry")
                    $ Say_Line(girl, renpy.random.choice([_("No. Do your part and I'll do mine."), _("I'm not putting on a show for you. Just move."), _("Focus on what you're doing back there.")]))

            "Tell her to stop touching herself" if store.doggy_started and store._dg_masturbating:
                $ advance_round(1)
                $ Say_Player(_("Hands off. Just take it."))
                $ store._dg_masturbating = False
                $ Say_Line(girl, renpy.random.choice([_("Tch... fine."), _("You're no fun."), _("As you wish...")]))
                call DG_ApplySpeed(girl, doggy_speed) from _call_DG_ApplySpeed_touch_self_off

            # Her face, a girl whose doggy art shows it (dg_has_hide_face): she looks forward, away from him, or back at
            # him. Hiding her face is for the camera (Record Options); here it is just where she looks (author,
            # 2026-10-11), the RCG's words. The laying pose's orders (_ld_turn_head: her yes / no and its lines), he is
            # behind her in both
            "Tell her to look forward" if store.doggy_started and dg_has_hide_face(girl) and not store.hiding_face and not getattr(store, "_recording_active", False):
                call _ld_turn_head(girl, _("Turn your head forward.")) from _call_ld_turn_head_dg
                call DG_ApplySpeed(girl, doggy_speed) from _call_DG_ApplySpeed_turn_fwd

            "Tell her to look back" if store.doggy_started and dg_has_hide_face(girl) and store.hiding_face and not getattr(store, "_recording_active", False):
                $ store.hiding_face = False
                call DG_ApplySpeed(girl, doggy_speed) from _call_DG_ApplySpeed_turn_back
                $ _turn_txt = _tl(_("She turns her head back to face you."))
                $ Narration(_turn_txt)
                if store._stealth_condom_removed:
                    call StealthCondomDiscovery(girl, _dg_scene_type) from _call_StealthDisc_dg_lookback

            "Record Options..." if (store.doggy_started and not getattr(store, "_recording_active", False)) or (getattr(store, "_recording_active", False) and getattr(store, "_recording_girl", None) == girl):
                menu:
                    # her face in the shot (dg_has_hide_face): the shared prompt, with "Ask her to hide her face"
                    "Ask to record" if not getattr(store, "_recording_active", False) and dg_has_hide_face(girl):
                        call _sex_phone_menu(girl, _dg_scene_type) from _call__sex_phone_menu_dg
                    "Ask to record" if not getattr(store, "_recording_active", False) and not dg_has_hide_face(girl):
                        call _dg_ask_recording(girl, _dg_scene_type) from _call__dg_ask_recording
                    # in secret only while she can't see him (looking away, or a pose that never shows her face)
                    "Record without telling her" if not getattr(store, "_recording_active", False) and (store.hiding_face or not dg_has_hide_face(girl)):
                        call _dg_secret_recording(girl, _dg_scene_type) from _call__dg_secret_recording
                    "Ask [store._ntr_watching_npc.Name] to record" if store._ntr_partner_watching and not getattr(store, "_recording_active", False):
                        call _watcher_record_start(girl, "doggy") from _call_watcher_rec_start_dg_npc
                    "Ask [store._witness_girl.Name] to record" if getattr(store, "_witness_watching", False) and getattr(store, "_witness_girl", None) is not None and not store._ntr_partner_watching and not getattr(store, "_recording_active", False):
                        call _watcher_record_start(girl, "doggy") from _call_watcher_rec_start_dg_girl
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
                    # the laying pose's label: a secret video she now sees (he is behind her in both)
                    "Order her to look back" if getattr(store, "hiding_face", False) and getattr(store, "_recording_active", False) and not getattr(store, "_recording_face_locked", False):
                        $ store.hiding_face = False
                        call _ld_look_back_during_recording(girl) from _call_ld_look_back_rec_dg
                    "Back":
                        pass
                if getattr(store, "_ld_secret_caught_end", False):
                    $ store._ld_secret_caught_end = False
                    call DG_End(girl, dress_up=False) from _call_DG_End_secret_caught
                    return
                call DG_ApplySpeed(girl, doggy_speed) from _call_DG_ApplySpeed_rec_opts

            "Condom..." if store.condom_active and store.doggy_started:
                call CondomMidsceneMenu(girl, _dg_scene_type) from _call_CondomMidsceneMenu_dg
                if not store.condom_active:
                    call DG_CondomRemoveAnim(girl) from _call_DG_CondomRemoveAnim_mid
                    call DG_ApplySpeed(girl, doggy_speed) from _call_DG_ApplySpeed_condom_rm

            "Switch position..." if store.doggy_started and not getattr(store, "_scene_restricted", False):
                if store._condom_broken_hidden:
                    call CondomBreakDiscovery(girl, "doggy") from _call_CondomBreakDisc_dg
                if store._stealth_condom_removed:
                    call StealthCondomDiscovery(girl, "doggy") from _call_StealthDisc_dg
                # Discovery may have ended the scene (force_scene_reset): don't offer the switch
                if _scene_should_exit() or store._doggy_girl is None:
                    return
                menu:
                    "Reverse Cowgirl" if girl_has_pose(girl, "reverse_cowgirl"):
                        $ Say_Player(_("Turn around..."))
                        # Anal scene -> vaginal-only position: same gates as "Switch to her pussy" (escalation.rpy).
                        # A girl whose RCG art has anal (rcg_has_anal) keeps the hole instead: anal stays anal.
                        $ store._switch_gate_ok = True
                        $ _sw_carry_anal = bool(store.doggy_anal) and rcg_has_anal(girl)
                        $ _sw_from_anal = bool(store.doggy_anal) and not _sw_carry_anal   # only an ANAL scene makes this switch a hole switch
                        if _sw_from_anal:
                            call _switch_to_vaginal_gate(girl, "doggy") from _call_sw_gate_sw_dg_rcg
                            if store._switch_gate_scene_ended:
                                return
                        if store._switch_gate_ok:
                            python:
                                _switch_lines = [
                                    _("You want me facing away? Okay..."),

                                    _("Mmm, let me turn around for you."),

                                    _("Sure... let me switch it up."),

                                ]
                            $ Say_Line(girl, _tl(renpy.random.choice(_switch_lines)))

                            # Clean up doggy standalones
                            $ _saved_condom = condom_carry_save()
                            python:
                                store._doggy_girl = None
                                store._sdg_girl = None   # her split doggy ref too: the switch leaked it, _in_sex never ended (tester 2026-10-10)
                                store.doggy_started = False
                                store.doggy_anal = False
                                store.doggy_rub_mode = False
                                store.doggy_tip_mode = False
                                _dg_hide_all_layers()
                                store.doggy_grab = False
                                hide_girl_sprite(girl)
                                store.condom_active = False
                            $ condom_carry_restore(_saved_condom)

                            $ rcg_speed = 0
                            $ store.rcg_anal = _sw_carry_anal
                            $ debug_log("[SWITCH] DG->RCG carry anal=%s" % store.rcg_anal)
                            $ _scene_position_switch(girl, "doggy", "reverse_cowgirl", anal=_sw_carry_anal)   # player switch: count the new position (and sex, if it is vaginal now)
                            call RCG_Launch(girl, from_switch=True) from _call_RCG_Launch_dg_switch
                            if _sw_from_anal and girl.has_trait("virgin"):
                                # she was only doing anal: this switch is her first vaginal penetration
                                call virgin_first_time(girl, "reverse_cowgirl") from _call_virgin_sw_dg_rcg
                            call RCG_ControlMenu(girl) from _call_RCG_ControlMenu_dg_switch

                            $ store._sub_event_position_switched = True

                    "Riding" if girl_has_pose(girl, "cowgirl"):
                        $ Say_Player(_("Get on top..."))
                        # Anal scene -> vaginal-only position: same gates as "Switch to her pussy" (escalation.rpy)
                        $ store._switch_gate_ok = True
                        $ _sw_from_anal = bool(store.doggy_anal)   # only an ANAL scene makes this switch a hole switch
                        if _sw_from_anal:
                            call _switch_to_vaginal_gate(girl, "doggy") from _call_sw_gate_sw_dg_cg
                            if store._switch_gate_scene_ended:
                                return
                        if store._switch_gate_ok:
                            python:
                                _switch_lines = [
                                    _("You want me on top? Okay..."),

                                    _("Mmm, let me ride you instead."),

                                    _("Sure... let me turn around."),

                                ]
                            $ Say_Line(girl, _tl(renpy.random.choice(_switch_lines)))

                            # Clean up doggy standalones
                            $ _saved_condom = condom_carry_save()
                            python:
                                store._doggy_girl = None
                                store._sdg_girl = None   # her split doggy ref too: the switch leaked it, _in_sex never ended (tester 2026-10-10)
                                store.doggy_started = False
                                store.doggy_anal = False
                                store.doggy_rub_mode = False
                                store.doggy_tip_mode = False
                                _dg_hide_all_layers()
                                store.doggy_grab = False
                                hide_girl_sprite(girl)
                                store.condom_active = False
                            $ condom_carry_restore(_saved_condom)

                            $ cowgirl_speed = 0
                            $ _scene_position_switch(girl, "doggy", "cowgirl", anal=False)   # player switch: count the new position (and sex, if it is vaginal now)
                            call COWGIRL_Launch(girl, from_switch=True) from _call_COWGIRL_Launch_dg_switch
                            if _sw_from_anal and girl.has_trait("virgin"):
                                # she was only doing anal: this switch is her first vaginal penetration
                                call virgin_first_time(girl, "cowgirl") from _call_virgin_sw_dg_cg
                            call COWGIRL_ControlMenu(girl) from _call_COWGIRL_ControlMenu_dg_switch

                            $ store._sub_event_position_switched = True

                    "Full Nelson" if girl_has_pose(girl, "full_nelson"):
                        $ Say_Player(_("Come here..."))
                        # Carry the current hole into the next pose (anal stays anal)
                        $ _switch_anal = store.doggy_anal
                        python:
                            _switch_lines = [
                                _("What are you... oh!"),

                                _("You're picking me up...?!"),

                                _("Whoa... okay...!"),

                            ]
                        $ Say_Line(girl, _tl(renpy.random.choice(_switch_lines)))

                        $ _saved_condom = condom_carry_save()
                        python:
                            store._doggy_girl = None
                            store._sdg_girl = None   # her split doggy ref too: the switch leaked it, _in_sex never ended (tester 2026-10-10)
                            store.doggy_started = False
                            store.doggy_anal = False
                            store.doggy_rub_mode = False
                            store.doggy_tip_mode = False
                            _dg_hide_all_layers()
                            store.doggy_grab = False
                            hide_girl_sprite(girl)
                            store.condom_active = False
                        $ condom_carry_restore(_saved_condom)

                        $ fn_speed = 0
                        $ store.fn_anal = _switch_anal
                        $ debug_log("[SWITCH] DG->FN carry anal=%s" % store.fn_anal)
                        $ _scene_position_switch(girl, "doggy", "full_nelson", anal=getattr(store, "fn_anal", False))   # player switch: count the new position (and sex, if it is vaginal now)
                        call FN_Launch(girl, from_switch=True) from _call_FN_Launch_dg_switch
                        call FN_ControlMenu(girl) from _call_FN_ControlMenu_dg_switch

                        $ store._sub_event_position_switched = True

                    "Back":
                        pass

            "Strip her..." if not getattr(store, "_scene_restricted", False):
                $ advance_round(1)
                call DG_StripMenu(girl) from _call_DG_StripMenu

            "{color=#fbbf24}Cum{/color}" if player_is_cumming():
                call PlayerCumMenu(girl, _dg_scene_type) from _call_PlayerCumMenu_voluntary_dg
                $ _handle_post_cum_exit("anal" if store.doggy_anal else "doggy", "sex")
                return

            "Stop now" if store.doggy_started:
                if store._forced_creampie_end_after_orgasm:
                    call _player_stops_after_forced_creampie(girl, _dg_scene_type) from _call__player_stops_forced_dg_sex
                $ debug_log("[DEBUG] Ask her to stop (DG): Lust=%d speed=%d" % (girl.Lust, doggy_speed))
                $ store._edge_lust_check = (girl.Lust >= 80)
                if store._edge_lust_check:
                    $ debug_log("[DEBUG] Lust >= 80, entering EdgeDenial")
                    # She begs with him still in her: the scene stays exactly as it is (speed 0 here drew him pulled out,
                    # the "after" layers, before anything had stopped). "Keep going" goes on at the same speed, her
                    # "No, stop." is the same stop as below (author, 2026-10-09)
                    call EdgeDenial(girl, _dg_scene_type) from _call_EdgeDenial_dg
                    if girl.Lust >= 100:
                        call GirlCumming(girl, _dg_scene_type, _dg_scene_type) from _call_GirlCumming_dg_edge
                    if store._edge_scene_ended:
                        $ store._edge_scene_ended = False
                        call _cum_dispatch_aftermath(girl, "anal" if store.doggy_anal else "doggy") from _call_ca_dispatch_dg_edge_stop
                        return
                else:
                    $ debug_log("[DEBUG] Lust < 80, ending scene normally")
                    call _cum_dispatch_aftermath(girl, "anal" if store.doggy_anal else "doggy") from _call_ca_dispatch_dg_stop
                    return

    return

# ═══════════════════════════════════════════════════════════
# DG_StripMenu — clothing removal during doggy
# ═══════════════════════════════════════════════════════════
label DG_StripMenu(girl):
    while True:
        # the item she wears on her legs, by name (her pants are no skirt)
        $ _sm_legs = clothing_item_name(girl, "skirt")
        menu:
            "Remove top" if girl.Over:
                call _strip_approval(girl, ["over"]) from _call__strip_approval_dg_over
                if store._strip_approved:
                    $ girl.Outfit_Change(over="none", pose="doggy")
                    if store._doggy_girl == girl:
                        call DG_ApplySpeed(girl, doggy_speed) from _call_DG_ApplySpeed_strip_over
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_dg_over

            "Remove chest" if girl.Chest:
                call _strip_approval(girl, _get_strip_slots(girl, "chest")) from _call__strip_approval_dg_chest_r
                if store._strip_approved:
                    $ _do_strip_change(girl, "chest", "doggy")
                    if store._doggy_girl == girl:
                        call DG_ApplySpeed(girl, doggy_speed) from _call_DG_ApplySpeed_strip_chest
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_dg_chest

            "Lift skirt up" if girl.Legs and girl.clothes_state.get("skirt") != "up" and _item_has_state(girl, "skirt", "up"):
                call _strip_approval(girl, ["legs"]) from _call__strip_approval_dgs_skirt_up
                if store._strip_approved:
                    $ girl.clothes_state["skirt"] = "up"
                    if store._doggy_girl == girl:
                        call DG_ApplySpeed(girl, doggy_speed) from _call_DG_ApplySpeed_strip_skirt_up
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_dgs_skirt_up

            "Remove [_sm_legs]" if girl.Legs:
                call _strip_approval(girl, ["legs"]) from _call__strip_approval_dg_legs
                if store._strip_approved:
                    $ girl.Outfit_Change(legs="none", pose="doggy")
                    if store._doggy_girl == girl:
                        call DG_ApplySpeed(girl, doggy_speed) from _call_DG_ApplySpeed_strip_legs
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_dg_legs

            "Remove panties" if girl.Panties:
                call _strip_approval(girl, ["panties"]) from _call__strip_approval_dg_pan
                if store._strip_approved:
                    $ girl.Outfit_Change(panties="none", pose="doggy")
                    if store._doggy_girl == girl:
                        call DG_ApplySpeed(girl, doggy_speed) from _call_DG_ApplySpeed_strip_pan
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_dg_pan

            "Pull panties to the side" if girl.Panties and _panties_next_state(girl) == "side":
                call _strip_approval(girl, ["panties"]) from _call__strip_approval_dgs_pan_side
                if store._strip_approved:
                    $ girl.clothes_state["panties"] = "side"
                    if store._doggy_girl == girl:
                        call DG_ApplySpeed(girl, doggy_speed) from _call_DG_ApplySpeed_strip_pan_side
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_dgs_pan_side

            "Remove shoes" if getattr(girl, "Shoes", None):
                $ girl.Outfit_Change(shoes="none", pose="doggy")
                if store._doggy_girl == girl:
                    call DG_ApplySpeed(girl, doggy_speed) from _call_DG_ApplySpeed_strip_shoes

            "Back":
                return


# ═══════════════════════════════════════════════════════════
# _dg_esc_dispatch — visual transitions after _escalation_menu
# Handles state vars, condom, visuals, and enters the next menu
# ═══════════════════════════════════════════════════════════
label _dg_esc_dispatch(girl, from_state, current_speed):
    if store._esc_result != "accepted":
        return

    # ── De-escalation ──────────────────────────────────────
    if store._esc_is_deescalation:
        if store._esc_target == "rub":
            python:
                store.doggy_rub_mode = True
                store.doggy_tip_mode = False
                store.doggy_started = False
                store.doggy_anal = False
            call DG_ApplySpeed(girl, 0) from _call_DG_ApplySpeed_deesc_rub
            call DG_RubControlMenu(girl) from _call_DG_RubCM_deesc
            return
        elif store._esc_target == "tip":
            $ store.doggy_tip_mode = True
            call DG_ApplySpeed(girl, 1) from _call_DG_ApplySpeed_deesc_tip
            call DG_TipControlMenu(girl) from _call_DG_TipCM_deesc
            return
        elif store._esc_target == "sex":
            python:
                store.doggy_anal = False
                store.doggy_tip_mode = False
            $ _dg_scene_type = "doggy"
            call DG_HoleTransition(girl, False) from _call_DG_HoleT_deesc_sex
            call DG_ApplySpeed(girl, current_speed) from _call_DG_ApplySpeed_deesc_sex
            return
        return

    # ── Tip (from rub) ─────────────────────────────────────
    if store._esc_target == "tip":
        $ store.doggy_anal = store._esc_anal_choice
        call DG_ApplySpeed(girl, 0) from _call_DG_ApplySpeed_esc_tip_prep
        call _dg_bottom_clothes_menu(girl) from _call_dg_bottom_esc_tip
        python:
            store.doggy_rub_mode = False
            store.doggy_tip_mode = True
        call DG_HoleTransition(girl, store.doggy_anal) from _call_DG_HoleT_esc_tip
        call DG_ApplySpeed(girl, 1) from _call_DG_ApplySpeed_esc_tip

        if store._esc_was_forced:
            $ Say_Line(girl, _esc_pick_line(girl, _ESC_TIP_FORCE_ACCEPT))
            $ Say_Player(_("It's just the tip, I promise..."))
            $ Say_Line(girl, _tl(renpy.random.choice(_ESC_TIP_FORCE_REACT)))

        call DG_TipControlMenu(girl) from _call_DG_TipCM_esc_tip
        return

    # ── Sex escalation (from rub or tip) ───────────────────
    if store._esc_target == "sex" and from_state != "anal":
        python:
            _from_tip = (from_state == "tip")
            store.doggy_anal = False

        if not _from_tip:
            call _dg_bottom_clothes_menu(girl) from _call_dg_bottom_esc_sex

        python:
            store.doggy_rub_mode = False
            store.doggy_tip_mode = False
            store._saved_dg_started = store.doggy_started
            store.doggy_started = False
        call DG_ApplySpeed(girl, 0) from _call_DG_ApplySpeed_rest_esc_sex

        if store._esc_was_forced:
            if _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False):
                call condom_check(girl, True, "hard_deny") from _call_condom_esc_sex_f_cheat
                if store.condom_denied:
                    $ store.doggy_started = store._saved_dg_started
                    call DG_End(girl, dress_up=False) from _call_DG_End_esc_sex_f_cond
                    call _cheat_no_condom_breakdown(girl) from _call_condom_snap_esc_sex_f
                    return
            else:
                # She refuses raw: decide it NOW, before the act is counted and before a virgin loses it
                if not getattr(store, "_esc_skip_condom", False) and not _force_raw_accepts(girl):
                    call force_raw(girl) from _call_force_raw_esc_dg_sex_pre
                    if store.condom_denied:
                        $ store.doggy_started = store._saved_dg_started
                        call DG_End(girl, dress_up=False) from _call_DG_End_esc_sex_f_deny_pre
                        return
                # Defer force_raw until after visual transition (penis visible during dialogue)
                python:
                    store.condom_active = False
                    store.condom_denied = False
                    store._force_raw_pending = True
        else:
            if _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False):
                call condom_check(girl, True, "hard_deny") from _call_condom_esc_sex_a_cheat
            else:
                $ _pen = store._esc_pen_result
                call condom_check(girl, _pen["condom_required"], _pen["raw_outcome"]) from _call_condom_esc_sex_a
            if store.condom_denied:
                if _is_on_cheat_path(girl):
                    $ store.doggy_started = store._saved_dg_started
                    call DG_End(girl, dress_up=False) from _call_DG_End_esc_sex_a_cond
                    call _cheat_no_condom_breakdown(girl) from _call_condom_snap_esc_sex_a
                    return
                python:
                    store.doggy_rub_mode = (from_state == "rub")
                    store.doggy_tip_mode = _from_tip
                    store.doggy_started = store._saved_dg_started
                call DG_ApplySpeed(girl, current_speed) from _call_DG_ApplySpeed_esc_sex_cond_deny
                return

        $ store.doggy_started = store._saved_dg_started
        if not store.condom_denied:
            $ _scene_escalation(girl, "sex", "doggy")
            $ _had_condom_esc = store.condom_active
            python:
                store.doggy_rub_mode = False
                store.doggy_tip_mode = False
            call DG_HoleTransition(girl, False) from _call_DG_HoleT_esc_sex
            if store._esc_virgin_check:
                call virgin_first_time(girl, "doggy") from _call_virgin_esc_sex
            $ doggy_speed = store._esc_speed
            call DG_ApplySpeed(girl, doggy_speed) from _call_DG_ApplySpeed_esc_sex_go

            # ── Deferred force_raw — penis now visible ──
            if getattr(store, "_force_raw_pending", False):
                $ store._force_raw_pending = False
                call force_raw(girl) from _call_force_raw_esc_sex
                if store.condom_denied:
                    call DG_End(girl, dress_up=False) from _call_DG_End_esc_sex_f_deny
                    return

            if store._esc_was_forced and not store._esc_virgin_check:
                python:
                    _is_hc = girl.has_trait("hardcore_sex")
                    _is_cute = girl.has_trait("cute_sex")
                    if _from_tip:
                        if _is_hc:
                            _post_lines = [
                                _("You just shoved it in raw? Good. Don't hold back."),
                                _("No condom, no warning? That's more like it."),
                            ]
                        elif _is_cute:
                            _post_lines = [
                                _("W-wait, you went in without... oh... oh god..."),
                                _("H-hey, that's raw! You didn't even... mmm..."),
                            ]
                        else:
                            _post_lines = [
                                _("You went in raw... just like that? No asking?"),
                                _("Hold on, that's bare... you didn't even put anything on..."),
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

            call DG_ControlMenu(girl, from_escalation=True) from _call_DG_CM_esc_sex
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

            $ store._saved_dg_started = store.doggy_started
            $ store.doggy_started = False
            call DG_ApplySpeed(girl, 0) from _call_DG_ApplySpeed_rest_sw_atp
            call condom_check(girl, True, "hard_deny") from _call_condom_sw_atp
            $ store.doggy_started = store._saved_dg_started
            if store.condom_denied:
                call DG_ApplySpeed(girl, current_speed) from _call_DG_ApplySpeed_sw_atp_deny
                return

        if _atp_outcome == "accept_raw" and _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False):
            $ store._saved_dg_started = store.doggy_started
            $ store.doggy_started = False
            call DG_ApplySpeed(girl, 0) from _call_DG_ApplySpeed_rest_sw_cheat
            call condom_check(girl, True, "hard_deny") from _call_condom_sw_cheat
            $ store.doggy_started = store._saved_dg_started
            if store.condom_denied:
                call DG_End(girl, dress_up=False) from _call_DG_End_sw_cheat
                call _cheat_no_condom_breakdown(girl) from _call_condom_snap_sw_cheat
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

        $ _scene_position_switch(girl, "anal", "doggy")
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

        $ _dg_scene_type = "doggy"
        call DG_HoleTransition(girl, False) from _call_DG_HoleT_sw_a2p
        call DG_ApplySpeed(girl, current_speed) from _call_DG_ApplySpeed_sw_a2p

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
            call _dg_bottom_clothes_menu(girl) from _call_dg_bottom_esc_anal
        python:
            store.doggy_rub_mode = False
            store.doggy_tip_mode = False
            store.doggy_anal = True
            store.condom_active = False
            store.condom_denied = False
        $ _scene_escalation(girl, "anal", "doggy")
        call DG_HoleTransition(girl, True) from _call_DG_HoleT_esc_anal
        $ doggy_speed = store._esc_speed
        call DG_ApplySpeed(girl, doggy_speed) from _call_DG_ApplySpeed_esc_anal

        if store._esc_was_forced:
            python:
                _post_lines = [
                    _("Ah! You just... put it in my ass... oh fuck..."),
                    _("W-wait! That's my ASS! Oh god..."),
                    _("You didn't even ask! ...ngh... it's so tight..."),
                ]
            $ Say_Line(girl, _tl(renpy.random.choice(_post_lines)))

        call DG_ControlMenu(girl, from_escalation=True) from _call_DG_CM_esc_anal
        if not getattr(store, "_sub_event_position_switched", False):
            python:
                _track_raw_sex_start(girl)
        return

    # ── Anal from sex (hole switch) ────────────────────────
    if store._esc_target == "anal" and from_state == "sex":
        if store._esc_was_forced:
            $ set_scene_expression(girl, "surprised")
            call DG_ApplySpeed(girl, current_speed) from _call_DG_ApplySpeed_sw_fa_pre
            python:
                _sw_pre = [
                    _("Wait, that's my..."),
                    _("H-hey! Wrong hole!"),
                    _("Hold on, that's not my..."),
                ]
            $ Say_Line(girl, _tl(renpy.random.choice(_sw_pre)))
            $ _scene_position_switch(girl, "doggy", "anal")
            $ mark_intimacy(girl, "anal")
            $ sex_accept_with_temptation(girl, "anal")
        else:
            $ _scene_position_switch(girl, "doggy", "anal")
            $ mark_intimacy(girl, "anal")

        $ Change_Status(girl, "Obed", 8)
        $ Change_Status(girl, "Inbt", 5)
        python:
            store.condom_active = False
            store.condom_denied = False
        $ _dg_scene_type = "anal"
        call DG_HoleTransition(girl, True) from _call_DG_HoleT_sw_p2a
        call DG_ApplySpeed(girl, current_speed) from _call_DG_ApplySpeed_sw_p2a

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
# DG_TipStripMenu — clothing removal during tip mode
# ═══════════════════════════════════════════════════════════
label DG_TipStripMenu(girl):
    while True:
        # the item she wears on her legs, by name (her pants are no skirt)
        $ _sm_legs = clothing_item_name(girl, "skirt")
        menu:
            "Remove top" if girl.Over:
                call _strip_approval(girl, ["over"]) from _call__strip_approval_dgt_over
                if store._strip_approved:
                    $ girl.Outfit_Change(over="none", pose="doggy")
                    if store._doggy_girl == girl:
                        call DG_ApplySpeed(girl, doggy_speed) from _call_DG_ApplySpeed_tstrip_over
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_dgt_over

            "Remove chest" if girl.Chest:
                call _strip_approval(girl, _get_strip_slots(girl, "chest")) from _call__strip_approval_dgt_chest_r
                if store._strip_approved:
                    $ _do_strip_change(girl, "chest", "doggy")
                    if store._doggy_girl == girl:
                        call DG_ApplySpeed(girl, doggy_speed) from _call_DG_ApplySpeed_tstrip_chest
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_dgt_chest

            "Lift skirt up" if girl.Legs and girl.clothes_state.get("skirt") != "up" and _item_has_state(girl, "skirt", "up"):
                call _strip_approval(girl, ["legs"]) from _call__strip_approval_dgt_skirt_up
                if store._strip_approved:
                    $ girl.clothes_state["skirt"] = "up"
                    if store._doggy_girl == girl:
                        call DG_ApplySpeed(girl, doggy_speed) from _call_DG_ApplySpeed_tstrip_skirt_up
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_dgt_skirt_up

            "Remove [_sm_legs]" if girl.Legs:
                call _strip_approval(girl, ["legs"]) from _call__strip_approval_dgt_legs
                if store._strip_approved:
                    $ girl.Outfit_Change(legs="none", pose="doggy")
                    if store._doggy_girl == girl:
                        call DG_ApplySpeed(girl, doggy_speed) from _call_DG_ApplySpeed_tstrip_legs
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_dgt_legs

            "Remove panties" if girl.Panties:
                call _strip_approval(girl, ["panties"]) from _call__strip_approval_dgt_pan
                if store._strip_approved:
                    $ girl.Outfit_Change(panties="none", pose="doggy")
                    if store._doggy_girl == girl:
                        call DG_ApplySpeed(girl, doggy_speed) from _call_DG_ApplySpeed_tstrip_pan
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_dgt_pan

            "Pull panties to the side" if girl.Panties and _panties_next_state(girl) == "side":
                call _strip_approval(girl, ["panties"]) from _call__strip_approval_dgt_pan_side
                if store._strip_approved:
                    $ girl.clothes_state["panties"] = "side"
                    if store._doggy_girl == girl:
                        call DG_ApplySpeed(girl, doggy_speed) from _call_DG_ApplySpeed_tstrip_pan_side
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_dgt_pan_side

            "Remove shoes" if getattr(girl, "Shoes", None):
                $ girl.Outfit_Change(shoes="none", pose="doggy")
                if store._doggy_girl == girl:
                    call DG_ApplySpeed(girl, doggy_speed) from _call_DG_ApplySpeed_tstrip_shoes

            "Back":
                return

# ═══════════════════════════════════════════════════════════
# DG_End — cleanup and restore standing sprite
# ═══════════════════════════════════════════════════════════
label DG_End(girl, dress_up=True):
    $ debug_log("[DEBUG] DG_End: entered, dress_up=%s" % str(dress_up))
    $ store._last_scene_was_anal = store.doggy_anal
    if store.doggy_anal:
        $ store._atm_source_gid = girl.gid
    $ scene_full_cleanup(girl)
    $ finalize_recording()
    $ _player_cleanup(girl)

    $ pose = getattr(girl, "_prev_pose", "standing")
    $ slot = _safe_restore_slot(getattr(girl, "_prev_slot", StageCenter))

    python:
        slot_transform = _slot_to_transform(slot)
        _reset_expression_state(girl)

        store._doggy_girl = None
        store._sdg_girl = None
        store._sdg_guy_on = False
        store._sdg_penis_out = None
        store.doggy_blink = False
        store.doggy_started = False
        store.doggy_anal = False
        store.doggy_rub_mode = False
        store.doggy_tip_mode = False
        store._dg_masturbating = False
        store._dg_massage = False
        store.hiding_face = False
        girl.ResetVisuals(pose=pose, at_list=[slot_transform])
        _dg_hide_all_layers()
        if callable(globals().get("_sdg_hide_all")):
            _sdg_hide_all()
        store.doggy_grab = False
        store.condom_active = False

    if dress_up:
        call DressUp_Sequence(girl) from _call_DressUp_Sequence_dg
    return

# ═══════════════════════════════════════════════════════════
# DG_RubLaunch — setup for rub mode (shared vaginal & anal)
# ═══════════════════════════════════════════════════════════
label DG_RubLaunch(girl):
    $ sub_event_reset(girl)

    $ public_attention_reset()
    call PlayerExposure(girl) from _call_PlayerExposure_dg_rub

    $ girl._prev_pose = getattr(girl, "default_pose", "standing")
    $ girl._prev_slot = getattr(girl, "SpriteLoc", StageCenter)
    if not getattr(girl, "_saved_outfit", None):
        $ girl.SaveOutfit()

    python:
        # Clear other scene refs
        _clear_scene_refs("doggy")

        # Hide all layers from other/previous scenes
        _hide_all_scene_layers(girl)

        _hide_non_scene_girls(girl)

        store._doggy_girl = girl
        store.doggy_started = False
        store.doggy_rub_mode = True
        store.doggy_tip_mode = False
        store.doggy_anal = False
        store._dg_butt_state = "base"
        store._dg_had_pussy = False
        store._dg_had_anal = False
        if girl.gid == "shion":
            store._sdg_girl = girl
            store._sdg_head_pos = 2   # head 2: her face turned to him, with expressions (head 1 = from behind, no face)
            store._sdg_butt_state = "closed"
            store._sdg_guy_on = False
        hide_girl_sprite(girl)

    $ doggy_speed = 0

    if girl.gid == "shion":
        call DG_ApplySpeed(girl, 0) from _call_DG_ApplySpeed_rub_shion
    else:
        $ set_girl_sprite(girl, pose="doggy")
        $ _dg_show_preview(girl)
    with fade

    python:
        if girl.gid == "shion":
            renpy.invoke_in_thread(_scene_cs_blink_loop, girl, "_doggy_girl", blink_timing=(0.12, 0.22))
        else:
            renpy.invoke_in_thread(_scene_blink_loop, girl, "_doggy_girl", "doggy_blink", cs_girls=_dg_cs_girls(), blink_timing=(0.12, 0.22))
        renpy.invoke_in_thread(_doggy_expression_cycle, girl)
    return

# ═══════════════════════════════════════════════════════════
# Masturbation in the doggy pose (mast_pose "doggy": Shion), the flow of MASTURBATE_Launch / LD_MASTURBATE_Launch
# (the riding / laying poses) with her layers: her hand between her legs, him kneeling behind her with nothing out
# (_sdg_apply_speed reads _dg_masturbating). No cunnilingus art in this pose (_MAST_ORAL_POSES, Core_Cowgirl).
# MASTURBATE_Launch / _Launch_Caught / _ApplySpeed / _ControlMenu redirect here by her mast_pose.
# ═══════════════════════════════════════════════════════════
label DG_MASTURBATE_Launch(girl):
    $ _kill_scene_threads()
    $ _hide_all_scene_layers(girl)

    $ girl._prev_pose = getattr(girl, "default_pose", "standing")
    $ girl._prev_slot = getattr(girl, "SpriteLoc", StageCenter)
    if not getattr(girl, "_saved_outfit", None):
        $ girl.SaveOutfit()

    call _dg_masturbate_setup(girl) from _call_dg_mast_setup
    call DG_MASTURBATE_ApplySpeed(girl, 0) from _call_DG_MAST_AS_launch
    with fade

    # --- BOTTOM: she can rub herself THROUGH her pants / panties in this pose (her hand is drawn over them), so
    # nothing comes off on its own. Pants have no pulled-down art here: off or on. ---
    $ _dg_mast_bare = girl.Legs is None and girl.Panties is None
    if girl.Legs is not None:
        $ Say_Line(girl, _("Do you want them off, or do you want to watch me through them?"))
        menu:
            "Take the pants off":
                $ girl.Outfit_Change(legs="none", pose="doggy")
                call DG_MASTURBATE_ApplySpeed(girl, doggy_speed) from _call_DG_MAST_AS_strip1

            "Leave them on":
                $ Say_Line(girl, _("Fine. Watch my hand, then."))

    if girl.Panties is not None and girl.Legs is None:
        $ Say_Line(girl, _("Here... let me give you a better view."))
        pause 0.15
        menu:
            "Remove panties":
                $ girl.Outfit_Change(panties="none", pose="doggy")
                call DG_MASTURBATE_ApplySpeed(girl, doggy_speed) from _call_DG_MAST_AS_strip2

            "Pull panties to the side" if _item_has_state(girl, "panties", "side"):
                $ girl.clothes_state["panties"] = "side"
                call DG_MASTURBATE_ApplySpeed(girl, doggy_speed) from _call_DG_MAST_AS_strip3

            "Pull panties down" if _item_has_state(girl, "panties", "down"):
                $ girl.clothes_state["panties"] = "down"
                call DG_MASTURBATE_ApplySpeed(girl, doggy_speed) from _call_DG_MAST_AS_strip4

            "Leave them on":
                $ Say_Line(girl, _("Through them, then. Don't blink."))

    # exposure only when her pussy is actually out (bare, or the panties moved)
    if girl.Legs is None and (girl.Panties is None or girl.clothes_state.get("panties", "full") != "full"):
        $ _exp = girl.RegisterAction("player_saw_pussy")
        if _exp["first_time"]:
            call FirstExposureReaction(girl, "pussy") from _call_FER_dg_mast

    return

# caught variant: no strip, no dialogue, no exposure (the shower / her room, like MASTURBATE_Launch_Caught)
label DG_MASTURBATE_Launch_Caught(girl):
    $ girl._prev_pose = getattr(girl, "default_pose", "standing")
    $ girl._prev_slot = getattr(girl, "SpriteLoc", StageCenter)
    if not getattr(girl, "_saved_outfit", None):
        $ girl.SaveOutfit()

    call _dg_masturbate_setup(girl) from _call_dg_mast_setup_caught
    call DG_MASTURBATE_ApplySpeed(girl, doggy_speed) from _call_DG_MAST_AS_caught
    with fade
    return

# the scene state of both launches (the doggy flags, her refs, the blink and expression threads)
label _dg_masturbate_setup(girl):
    python:
        _clear_scene_refs("doggy")
        _hide_non_scene_girls(girl)
        store._doggy_girl = girl
        store.doggy_started = False
        store.doggy_rub_mode = False
        store.doggy_tip_mode = False
        store.doggy_anal = False
        store.doggy_grab = False
        store._dg_butt_state = "base"
        store._dg_had_pussy = False
        store._dg_had_anal = False
        store._dg_masturbating = True
        store._oral_active = False
        store.hiding_face = False
        sprite_state.setdefault(girl.Id, {})["pose"] = "doggy"
        if girl.gid == "shion":
            store._sdg_girl = girl
            store._sdg_head_pos = 2   # her face turned to him, with expressions
            store._sdg_butt_state = "closed"
            store._sdg_guy_on = False
        hide_girl_sprite(girl)
        if girl.gid == "shion":
            renpy.invoke_in_thread(_scene_cs_blink_loop, girl, "_doggy_girl", blink_timing=(0.12, 0.22))
        else:
            renpy.invoke_in_thread(_scene_blink_loop, girl, "_doggy_girl", "doggy_blink", cs_girls=_dg_cs_girls(), blink_timing=(0.12, 0.22))
        renpy.invoke_in_thread(_doggy_expression_cycle, girl)
        print("[DG_MAST] setup: %s speed=%s" % (girl.gid, getattr(store, "doggy_speed", 0)))
    return

label DG_MASTURBATE_ApplySpeed(girl, speed=0):
    python:
        store._dg_masturbating = True
        store.doggy_speed = speed
        # her clothes stay as they are: dressed, she rubs herself through them (her hand over the clothes)
    call DG_ApplySpeed(girl, speed) from _call_DG_AS_mast
    return

label DG_MASTURBATE_ControlMenu(girl):

    $ store._scene_phase = "masturbate"
    $ store._mast_stop_asked = 0
    $ store._mast_sex_asks = 0

    while True:

        if _scene_should_exit() or store._doggy_girl is None:
            $ print("[DG_MAST_LOOP] EXIT: scene_should_exit=%s doggy_girl_none=%s" % (_scene_should_exit(), store._doggy_girl is None))
            return

        if Round >= 100:
            $ Say_Line(girl, _scene_time_up_line())
            call DG_End(girl, dress_up=False) from _call_DG_End_timeout_mast
            return

        menu:
            "Keep going" if doggy_speed >= 1:
                $ advance_round(TIME_COSTS["sex_tick"])
                $ _girl_lust_gain(girl, (2 if doggy_speed == 1 else 4 if doggy_speed == 2 else 6), doggy_speed)
                $ _moan = scene_moan_tick(girl, "masturbate", doggy_speed)
                if _moan:
                    call _moan_say(girl, _moan) from _call_ms_dg_mast
                if girl.Lust >= 100:
                    call GirlCumming(girl, "masturbate", "doggy") from _call_GirlCumming_dg_mast

                # --- Sex escalation: girl asks for the real thing (up to 3 times), as in the other poses ---
                python:
                    _flags = getattr(girl, "intimacy_flags", set()) or set()
                    _has_sex_history = bool(_flags & {"sex", "bj", "hj", "tj"})
                    _is_lesbian = girl.has_trait("lesbian")
                    _msa = getattr(store, "_mast_sex_asks", 0)
                    _escalate_chance = 0
                    if story_act_locked(girl, "sex"):
                        # a girl with a story never begs for the act her own step refuses (the A7 rule,
                        # Core_LayingDown; this doggy copy had the same hole: Shion's mast_pose is doggy)
                        print("[DG_MAST_LOOP] escalation ask skipped: %s, her story locks sex (step %s)" % (girl.gid, story_step_id(girl)))
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
                                    call DG_End(girl, dress_up=False) from _call_DG_End_mastesc
                                    call sex_menu(girl, CurrentLocation, store.TimeIndex) from _call_sex_menu_dg_mastesc
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
                        call _mast_desperate_negotiation(girl) from _call_mast_desp_neg_dg
                        if store._mast_desp_result == "sex":
                            return
                        if store._mast_desp_result == "kicked":
                            $ print("[MAST_DESP] kicked: %s rejected 3rd ask -> angry kick-out (doggy)" % girl.gid)
                            call DG_End(girl, dress_up=False) from _call_DG_End_desp_kicked
                            call _scene_kick_to_campus(girl, mood="angry") from _call_kick_mast_desp_dg
                            return

            "Start" if doggy_speed == 0:
                $ Say_Player(_("Go ahead... start touching yourself."))
                $ doggy_speed = 1
                call DG_MASTURBATE_ApplySpeed(girl, doggy_speed) from _call_DG_MAST_AS_start
                $ _girl_lust_gain(girl, 2, doggy_speed)
                $ _moan = scene_moan_tick(girl, "masturbate", doggy_speed)
                if _moan:
                    call _moan_say(girl, _moan) from _call_ms_dg_mast2
                if girl.Lust >= 100:
                    call GirlCumming(girl, "masturbate", "doggy") from _call_GirlCumming_dg_mast_start
                $ Narration(_("She begins to touch herself."))

            "Speed up" if doggy_speed >= 1 and doggy_speed < 3:
                $ advance_round(TIME_COSTS["sex_tick"])
                $ Say_Player(_("Faster..."))
                $ doggy_speed += 1
                call DG_MASTURBATE_ApplySpeed(girl, doggy_speed) from _call_DG_MAST_AS_speedup
                $ _girl_lust_gain(girl, (2 if doggy_speed == 1 else 4 if doggy_speed == 2 else 6), doggy_speed)
                $ _moan = scene_moan_tick(girl, "masturbate", doggy_speed)
                if _moan:
                    call _moan_say(girl, _moan) from _call_ms_dg_mast_su
                if girl.Lust >= 100:
                    call GirlCumming(girl, "masturbate", "doggy") from _call_GirlCumming_dg_mast_su
                $ Narration(_("She speeds up her movements."))

            "Speed down" if doggy_speed > 0:
                $ advance_round(1)
                $ doggy_speed -= 1
                call DG_MASTURBATE_ApplySpeed(girl, doggy_speed) from _call_DG_MAST_AS_speeddown
                $ Narration(_("She slows down."))

            "Strip her..." if not getattr(store, "_scene_restricted", False):
                $ advance_round(1)
                call DG_StripMenu(girl) from _call_dg_strip_mast
                call DG_MASTURBATE_ApplySpeed(girl, doggy_speed) from _call_DG_MAST_AS_strip

            "Record Options..." if (not getattr(store, "_recording_active", False) or getattr(store, "_recording_girl", None) == girl):
                menu:
                    "Record her" if not getattr(store, "_recording_active", False):
                        call _sex_phone_menu(girl, "masturbate") from _call__sex_phone_menu_dg_mast
                    "Ask [store._ntr_watching_npc.Name] to record" if store._ntr_partner_watching and not getattr(store, "_recording_active", False):
                        call _watcher_record_start(girl, "masturbate") from _call_watcher_rec_start_dg_mast_npc
                    "Ask [store._witness_girl.Name] to record" if getattr(store, "_witness_watching", False) and getattr(store, "_witness_girl", None) is not None and not store._ntr_partner_watching and not getattr(store, "_recording_active", False):
                        call _watcher_record_start(girl, "masturbate") from _call_watcher_rec_start_dg_mast_girl
                    "Stop recording" if getattr(store, "_recording_active", False) and getattr(store, "_recording_girl", None) == girl:
                        $ _rec_stop_name = _get_recording_stopper_name()
                        $ finalize_recording()
                        if _rec_stop_name:
                            $ _rec_stop_text = _tl(_("%s stopped the recording.")) % _rec_stop_name
                            $ Narration(_rec_stop_text)
                        else:
                            $ Narration(_("You stop recording."))
                    "Back":
                        pass
                call DG_MASTURBATE_ApplySpeed(girl, doggy_speed) from _call_DG_MAST_AS_rec

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
                            call DG_End(girl, dress_up=False) from _call_DG_End_mast_stop
                            $ store._mast_stop_asked = 0
                            return
                else:
                    $ Say_Line(girl, _("Alright..."))
                    call DG_End(girl, dress_up=False) from _call_DG_End_mast_stop2
                    $ store._mast_stop_asked = 0
                    return

# ═══════════════════════════════════════════════════════════
# DG_RubControlMenu — rub mode main loop
# ═══════════════════════════════════════════════════════════
label DG_RubControlMenu(girl):

    $ store._scene_phase = "rub"
    $ doggy_speed = 0
    # Rub is never anal. This menu was the only one reading _dg_scene_type without assigning it
    # (NameError on "Keep going" past Focus 100), and after an anal scene the stale "anal" leaked in.
    $ _dg_scene_type = "doggy"
    $ print("[DG_RUB_MENU] enter gid=%s scene_type=%s" % (girl.gid, _dg_scene_type))
    call DG_ApplySpeed(girl, doggy_speed) from _call_DG_ApplySpeed_rub_menu_init

    while True:

        if _scene_should_exit():
            return

        if Round >= 100:
            $ Say_Line(girl, _scene_time_up_line())
            call DG_End(girl, dress_up=False) from _call_DG_End_timeout_rub
            return

        menu:
            # ── keep going ──────────────────────────────
            "Keep going" if doggy_speed >= 1:
                $ advance_round(TIME_COSTS["sex_tick"])
                $ add_player_focus(get_player_lust_gain("doggy", doggy_speed))
                $ _girl_lust_gain(girl, (2 if doggy_speed == 1 else 3 if doggy_speed == 2 else 5), doggy_speed)
                $ _moan = scene_moan_tick(girl, "doggy", doggy_speed)
                if _moan:
                    call _moan_say(girl, _moan) from _call_ms_dg_su

                if getattr(store, "_path1_rub_first_line_pending", False):
                    $ store._path1_rub_first_line_pending = False
                    $ Say_Line(girl, _cheat_rub_midline(girl))

                if _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False):
                    if _cheat_breaking_point_ready(girl) and renpy.random.random() < 0.30:
                        call _cheat_breaking_point(girl, "doggy") from _call_cheat_break_dgrub

                # Public attention
                if store._crowd_level > 0:
                    $ _pa_caught = public_attention_tick(girl, "keep_going", doggy_speed)
                    if _pa_caught:
                        if not _caught_keeps_going(girl):
                            call DG_End(girl, dress_up=False) from _call_DG_End_rub_pa
                        call caught_in_public(girl, "doggy") from _call_caught_public_dg_rub
                        return

                call _sex_interruption_check(girl, "doggy") from _call_interrupt_dg_rub
                $ store._witness_expression_lock = False
                if store._sex_interrupted:
                    call DG_End(girl, dress_up=False) from _call_DG_End_rub_int
                    return

                call _npc_partner_detection_tick(girl, "doggy") from _call_npc_detect_dg_rub
                if store._npc_witness_scene_aborted:
                    call DG_End(girl, dress_up=False) from _call_DG_End_rub_npc
                    return

                $ _se = sub_event_tick(girl, "doggy")
                if _se:
                    call SubEvent_Handle(girl, "doggy", _se) from _call_SubEvent_Handle_dg_rub
                    if store._sub_event_position_switched:
                        $ store._sub_event_position_switched = False
                        return

                call _cheat_bf_call_check(girl, "doggy") from _call_cheat_bf_dg_rub

                # Spontaneous escalation: she wants more
                call _girl_escalation_check(girl, "rub") from _call_girl_esc_dg_rub
                if store._girl_esc_accepted:
                    $ store.doggy_rub_mode = False
                    $ store.doggy_tip_mode = True
                    $ store.doggy_started = True
                    call DG_ApplySpeed(girl, 0) from _call_DG_ApplySpeed_esc_strip_rub
                    call DG_HoleTransition(girl, False) from _call_DG_HoleTransition_esc_rub_tip
                    call DG_ApplySpeed(girl, 1) from _call_DG_ApplySpeed_esc_rub_tip
                    call DG_TipControlMenu(girl) from _call_DG_TipControlMenu_esc_rub
                    return

                if girl.Lust >= 100:
                    call GirlCumming(girl, "doggy", "doggy", scene_override="rub") from _call_GirlCumming_dg_rub
                if player_is_cumming():
                    if focus_overdue_tick():
                        call ForcedCumOverdue(girl, _dg_scene_type) from _call_ForcedCumOverdue_dg_rub
                        label _call_PlayerCumMenu_RubOutside_dg:
                        $ _handle_post_cum_exit("doggy", "rub")
                        return

            # ── speed up / down ──────────────��──────────
            "Speed up" if doggy_speed < 3:
                $ advance_round(TIME_COSTS["sex_tick"])
                $ doggy_speed += 1
                call DG_ApplySpeed(girl, doggy_speed) from _call_DG_ApplySpeed_rub_su
                $ add_player_focus(get_player_lust_gain("doggy", doggy_speed))
                $ _girl_lust_gain(girl, (2 if doggy_speed == 1 else 3 if doggy_speed == 2 else 5), doggy_speed)
                $ Narration(_("You rub faster."))

            "Slow down" if doggy_speed > 0:
                $ advance_round(1)
                $ doggy_speed -= 1
                call DG_ApplySpeed(girl, doggy_speed) from _call_DG_ApplySpeed_rub_sd
                $ Narration(_("You slow down."))

            "Strip her..." if not getattr(store, "_scene_restricted", False):
                $ advance_round(1)
                call DG_StripMenu(girl) from _call_DG_StripMenu_rub

            # ── Penetration submenu (centralized) ──────
            "Penetration...":
                call _escalation_menu(girl, "doggy") from _call_esc_menu_dg_rub
                if store._esc_result == "accepted":
                    call _dg_esc_dispatch(girl, "rub", doggy_speed) from _call_esc_disp_dg_rub
                    return
                elif store._esc_result == "scene_ended":
                    call DG_End(girl, dress_up=False) from _call_DG_End_esc_rub
                    return
                # denied/cancelled: stay in rub menu
            "{color=#fbbf24}Cum{/color}" if player_is_cumming():
                call DG_PlayerCumMenu_RubOutside(girl) from _call_DG_PlayerCumMenu_RubOutside_voluntary
                $ _handle_post_cum_exit("doggy", "rub")
                return

            # ── stop ────────────────────────────────────
            "Stop now":
                call _scene_stop_reaction(girl) from _call_stop_react_dg_rub
                if store._stop_accepted:
                    return

    return

# ═══════════════════════════════════════════════════════════
# DG_TipLaunch — setup for tip mode (vaginal or anal)
# ═══════════════════════════════════════════════════════════
label DG_TipLaunch(girl):
    $ sub_event_reset(girl)

    $ public_attention_reset()
    call PlayerExposure(girl) from _call_PlayerExposure_dg_tip

    $ girl._prev_pose = getattr(girl, "default_pose", "standing")
    $ girl._prev_slot = getattr(girl, "SpriteLoc", StageCenter)
    if not getattr(girl, "_saved_outfit", None):
        $ girl.SaveOutfit()

    python:
        # Clear other scene refs
        _clear_scene_refs("doggy")

        # Hide all layers from other/previous scenes
        _hide_all_scene_layers(girl)

        store._doggy_girl = girl
        store.doggy_started = False
        store.doggy_rub_mode = False
        store.doggy_tip_mode = False
        # doggy_anal is NOT reset here — caller sets it
        # (orchestrator pre_launch for anal, or explicit set before call)
        store._dg_butt_state = "base"
        store._dg_had_pussy = False
        store._dg_had_anal = False
        if girl.gid == "shion":
            hide_girl_sprite(girl)   # her sdg_* layers have their own tags (DG_Launch)
            store._sdg_girl = girl
            store._sdg_head_pos = 2   # head 2: her face turned to him, with expressions (head 1 = from behind, no face)
            store._sdg_butt_state = "closed"
            store._sdg_guy_on = False

    $ doggy_speed = 1

    if girl.gid == "shion":
        call DG_ApplySpeed(girl, 0) from _call_DG_ApplySpeed_tip_shion
    else:
        $ set_girl_sprite(girl, pose="doggy")
        $ _dg_show_preview(girl)
    with fade

    call _dg_bottom_clothes_menu(girl) from _call_dg_bottom_tip_launch

    $ store.doggy_tip_mode = True
    call DG_HoleTransition(girl, store.doggy_anal) from _call_DG_HoleTransition_tip_launch
    call DG_ApplySpeed(girl, 1) from _call_DG_ApplySpeed_tip_launch

    python:
        if girl.gid == "shion":
            renpy.invoke_in_thread(_scene_cs_blink_loop, girl, "_doggy_girl", blink_timing=(0.12, 0.22))
        else:
            renpy.invoke_in_thread(_scene_blink_loop, girl, "_doggy_girl", "doggy_blink", cs_girls=_dg_cs_girls(), blink_timing=(0.12, 0.22))
        renpy.invoke_in_thread(_doggy_expression_cycle, girl)
    return

# ═══════════════════════════════════════════════════════════
# DG_TipControlMenu — tip mode, locked at speed 1
# ═══════════════════════════════════════════════════════════
label DG_TipControlMenu(girl):

    $ store._scene_phase = "tip"
    $ store._cheat_shower_max_act = "tip"
    $ doggy_speed = 1
    $ _dg_scene_type = "anal" if store.doggy_anal else "doggy"
    $ store._anal_tip_counted = False
    $ advance_round(TIME_COSTS["sex_tick"])

    while True:

        if _scene_should_exit():
            return

        if Round >= 100:
            $ Say_Line(girl, _scene_time_up_line())
            call DG_End(girl, dress_up=False) from _call_DG_End_timeout_tip
            return

        menu:
            # ── keep going ──────────────────────────────
            "Keep going":
                $ advance_round(TIME_COSTS["sex_tick"])
                $ add_player_focus(get_player_lust_gain(_dg_scene_type, 1))
                if store.doggy_anal:
                    if girl.has_trait("anal_lover"):
                        $ _girl_lust_gain(girl, 2, 1)
                    elif girl.has_trait("anal_hater"):
                        $ _girl_lust_gain(girl, 0, 1)
                    else:
                        $ _girl_lust_gain(girl, 1, 1)
                else:
                    $ _girl_lust_gain(girl, 2, 1)
                $ _apply_anal_lust_cap(girl, store.doggy_anal)
                $ _moan = scene_moan_tick(girl, _dg_scene_type, 1)
                if _moan:
                    call _moan_say(girl, _moan) from _call_ms_dg_sex

                $ _count_anal_tip(girl, store.doggy_anal)

                if getattr(store, "_path1_tip_first_line_pending", False):
                    $ store._path1_tip_first_line_pending = False
                    $ Say_Line(girl, _cheat_tip_midline(girl))

                if _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False):
                    if _cheat_breaking_point_ready(girl) and renpy.random.random() < 0.30:
                        call _cheat_breaking_point(girl, "doggy") from _call_cheat_break_dgtip

                # Public attention
                if store._crowd_level > 0:
                    $ _pa_caught = public_attention_tick(girl, "keep_going", 1)
                    if _pa_caught:
                        if not _caught_keeps_going(girl):
                            call DG_End(girl, dress_up=False) from _call_DG_End_tip_pa
                        call caught_in_public(girl, _dg_scene_type) from _call_caught_public_dg_tip
                        return

                call _sex_interruption_check(girl, _dg_scene_type) from _call_interrupt_dg_tip
                $ store._witness_expression_lock = False
                if store._sex_interrupted:
                    call DG_End(girl, dress_up=False) from _call_DG_End_tip_int
                    return

                call _npc_partner_detection_tick(girl, _dg_scene_type) from _call_npc_detect_dg_tip
                if store._npc_witness_scene_aborted:
                    call DG_End(girl, dress_up=False) from _call_DG_End_tip_npc
                    return

                $ _se = sub_event_tick(girl, _dg_scene_type)
                if _se:
                    call SubEvent_Handle(girl, _dg_scene_type, _se) from _call_SubEvent_Handle_dg_tip
                    if store._sub_event_position_switched:
                        $ store._sub_event_position_switched = False
                        return

                call _cheat_bf_call_check(girl, _dg_scene_type) from _call_cheat_bf_dg_tip

                # Spontaneous escalation: she wants all the way (or anal if she prefers)
                if not store.doggy_anal:
                    call _girl_escalation_check(girl, "tip") from _call_girl_esc_dg_tip
                    if store._girl_esc_accepted:
                        $ store.doggy_tip_mode = False
                        call _girl_esc_accept_sex(girl, "doggy") from _call_girl_esc_accept_dg
                        if store._girl_esc_condom_denied:
                            call DG_End(girl, dress_up=False) from _call_DG_End_esc_condom
                            call _cheat_no_condom_breakdown(girl) from _call_condom_snap_dg_esc
                            return
                        if store._girl_esc_wants_anal:
                            $ store.doggy_anal = True
                            $ _dg_scene_type = "anal"
                        $ doggy_speed = 2
                        call DG_ApplySpeed(girl, 2) from _call_DG_ApplySpeed_esc_tip_sex
                        call DG_ControlMenu(girl, from_escalation=True) from _call_DG_ControlMenu_esc_tip
                        return

                if girl.Lust >= 100:
                    call GirlCumming(girl, _dg_scene_type, _dg_scene_type, scene_override="tip") from _call_GirlCumming_dg_tip
                if player_is_cumming():
                    if focus_overdue_tick():
                        call ForcedCumOverdue(girl, _dg_scene_type) from _call_ForcedCumOverdue_dg_tip
                        label _call_PlayerCumMenu_TipOutside_dg:
                        $ _handle_post_cum_exit("doggy", "tip")
                        return

            # ── grab her ass ────────────────────────────
            "Grab her ass" if not store.doggy_grab and dg_has_grab(girl):
                $ advance_round(1)
                $ store.doggy_grab = True
                call DG_ApplySpeed(girl, 1) from _call_DG_ApplySpeed_tip_grab
                python:
                    _grab_react = renpy.random.choice(["mouth_surprised", "mouth_tongue", "mouth_kiss"])
                    set_scene_expression(girl, None, mouth=_grab_react)
                call DG_ApplySpeed(girl, 1) from _call_DG_ApplySpeed_tip_grab_react

            "Let go" if store.doggy_grab:
                $ advance_round(1)
                $ store.doggy_grab = False
                call DG_ApplySpeed(girl, 1) from _call_DG_ApplySpeed_tip_letgo

            # ── spank her ───────────────────────────────
            "Spank her":
                $ advance_round(1)
                call SpankHer(girl, _dg_scene_type) from _call_SpankHer_dg_tip

            # ── Penetration submenu (centralized) ──────
            "Penetration...":
                call _escalation_menu(girl, "doggy") from _call_esc_menu_dg_tip
                if store._esc_result == "accepted":
                    call _dg_esc_dispatch(girl, "tip", doggy_speed) from _call_esc_disp_dg_tip
                    return
                elif store._esc_result == "scene_ended":
                    call DG_End(girl, dress_up=False) from _call_DG_End_esc_tip
                    return
                # denied/cancelled: stay in tip menu
            # ── strip her ───────────────────────────────
            "Strip her..." if not getattr(store, "_scene_restricted", False):
                $ advance_round(1)
                call DG_TipStripMenu(girl) from _call_DG_TipStripMenu

            "{color=#fbbf24}Cum{/color}" if player_is_cumming():
                call DG_PlayerCumMenu_TipOutside(girl) from _call_DG_PlayerCumMenu_TipOutside_voluntary
                $ _handle_post_cum_exit("doggy", "tip")
                return

            # ── stop ────────────────────────────────────
            "Stop now":
                $ debug_log("[DEBUG] Ask her to stop (DG-tip): Lust=%d" % girl.Lust)
                $ store._edge_lust_check = (girl.Lust >= 80)
                if store._edge_lust_check:
                    $ debug_log("[DEBUG] Lust >= 80, entering EdgeDenial (DG-tip)")
                    call EdgeDenial(girl, _dg_scene_type) from _call_EdgeDenial_dg_tip
                    if girl.Lust >= 100:
                        call GirlCumming(girl, _dg_scene_type, _dg_scene_type) from _call_GirlCumming_dg_edge_tip
                    if store._edge_scene_ended:
                        $ store._edge_scene_ended = False
                        return
                else:
                    $ debug_log("[DEBUG] Lust < 80, ending tip normally")
                    $ Say_Line(girl, _pick_stop_line(girl))
                    return

    return

# ═══════════════════════════════════════════════════════════
# Bottom clothes menu for doggy (skirt / panties displacement)
# ═══════════════════════════════════════════════════════════
label _dg_bottom_clothes_menu(girl):
    call DG_ApplySpeed(girl, doggy_speed) from _call_DG_ApplySpeed_btm_preview
    call _scene_bottom_clothes_menu(girl, "doggy") from _call_scene_btm_dg
    return

# ═══════════════════════════════════════════════════════════
# DG_HoleTransition — centralized exit/enter animation
# Handles first entry, same-hole noop, and cross-hole switch.
# Caller must call DG_ApplySpeed(girl, speed) after this.
# ═══════════════════════════════════════════════════════════
label DG_HoleTransition(girl, to_anal):
    python:
        _ht_switching = store.doggy_started and (store.doggy_anal != to_anal)
        _ht_first = not store.doggy_started
        debug_log("[HT] ENTER to_anal=%s started=%s cur_anal=%s | switching=%s first=%s" % (to_anal, store.doggy_started, store.doggy_anal, _ht_switching, _ht_first))

    if _ht_switching:
        $ debug_log("[HT] FREEZE at speed 0 before switch doggy_anal=%s" % store.doggy_anal)
        call DG_ApplySpeed(girl, 0) from _call_DG_ApplySpeed_ht_freeze
        $ renpy.hide("dg_penis")
        $ renpy.hide("dg_condom")

    python:
        store.doggy_anal = to_anal
        store.doggy_started = True
        debug_log("[HT] FLAGS SET doggy_anal=%s started=%s (had flags deferred)" % (store.doggy_anal, store.doggy_started))

    if _ht_first or _ht_switching:
        $ debug_log("[HT] ENTER ANIM doggy_anal=%s" % store.doggy_anal)
        call DG_PenisEnterAnim(girl) from _call_DG_PenisEnterAnim_ht
    else:
        $ debug_log("[HT] NOOP same hole, already started")

    python:
        if to_anal:
            store._dg_had_anal = True
        else:
            store._dg_had_pussy = True
        debug_log("[HT] DONE doggy_anal=%s had_p=%s had_a=%s" % (store.doggy_anal, store._dg_had_pussy, store._dg_had_anal))
    # only when he actually goes in (first entry or pussy -> ass), not on every speed change inside the same hole
    if to_anal and (_ht_first or _ht_switching):
        $ _watcher_scene_comment("anal_enter")
    return

# ═══════════════════════════════════════════════════════════
# DG_PenisEnterAnim — penis slide-in animation
# ═══════════════════════════════════════════════════════════
label DG_PenisEnterAnim(girl):
    if girl.gid == "shion":
        python:
            store._sdg_butt_state = "ass_open" if store.doggy_anal else "vagina_open"
            _sdg_apply_speed(girl, 1)
        $ renpy.pause(0.3)
        return
    python:
        debug_log("[ENTER] doggy_anal=%s condom=%s" % (store.doggy_anal, store.condom_active))

        _enter_attrs = _build_doggy_attributes(girl)
        _enter_attrs = [a for a in _enter_attrs if "butt_gap" not in a and "butt_top" not in a]
        _enter_attrs.extend(["butt_gap_none", "butt_top_none"])
        _o_val_e = girl.clothes.get("over")
        _o_map_e = {"long_shirt": "doggy_mesh_top"}
        _o_key_e = _o_map_e.get(_o_val_e)
        if _o_key_e and renpy.has_image("%s %s" % (girl.gid, _o_key_e), exact=True):
            _enter_attrs = [a for a in _enter_attrs if "torso_over" not in a]
            _enter_attrs.append("torso_over_none")
        _c_val_e = girl.clothes.get("chest")
        _c_map_e = {"corset": "doggy_corset", "crop_top": "doggy_corset", "bikini_top": "doggy_bikini_top"}
        _c_key_e = _c_map_e.get(_c_val_e)
        if _c_key_e and renpy.has_image("%s %s" % (girl.gid, _c_key_e), exact=True):
            _enter_attrs = [a for a in _enter_attrs if "torso_chest" not in a]
            _enter_attrs.append("torso_chest_none")
        _enter_img = "%s doggy" % girl.gid
        if _enter_attrs:
            _enter_img += " " + " ".join(_enter_attrs)
        _slot_at0 = [dg_get_slot_transform(0)]
        renpy.show(_enter_img, tag=girl.gid, at_list=_slot_at0, zorder=9980)

        _dg_show_butt_layers(girl, 0)

        renpy.hide("dg_penis")
        renpy.hide("dg_condom")
        _pen_img = "%s doggy_penis" % girl.gid
        _pen_z = _dg_pen_z()
        _slide_tf = dga_penis_slide_in if store.doggy_anal else dg_penis_slide_in
        debug_log("[ENTER] slide=%s" % ("ANAL" if store.doggy_anal else "VAGINAL"))
        renpy.show(_pen_img, tag="dg_penis", at_list=[_slide_tf], zorder=_pen_z)
        if store.condom_active:
            _cb_cimg = _condom_img_tag("dg_condom")
            renpy.show(_cb_cimg, tag="dg_condom", at_list=[_slide_tf], zorder=_pen_z)
        _bs_img = "%s doggy_body_safe" % girl.gid
        _bs_z = 10051 if not store.doggy_anal else 10059
        renpy.show(_bs_img, tag="dg_body_safe", at_list=_slot_at0, zorder=_bs_z)
        _c_val = girl.clothes.get("chest")
        _c_map = {"corset": "doggy_corset", "crop_top": "doggy_corset", "bikini_top": "doggy_bikini_top"}
        _c_key = _c_map.get(_c_val)
        if _c_key:
            _c_img = "%s %s" % (girl.gid, _c_key)
            if renpy.has_image(_c_img, exact=True):
                renpy.show(_c_img, tag="dg_chest_over", at_list=_slot_at0, zorder=_bs_z + 1)
        _over_z = 10054 if not store.doggy_anal else 10060
        _o_val = girl.clothes.get("over")
        _o_map = {"long_shirt": "doggy_mesh_top"}
        _o_key = _o_map.get(_o_val)
        if _o_key:
            _o_img = "%s %s" % (girl.gid, _o_key)
            if renpy.has_image(_o_img, exact=True):
                renpy.show(_o_img, tag="dg_over_above", at_list=_slot_at0, zorder=_over_z)
                _h_img = "%s doggy_head" % girl.gid
                if renpy.has_image(_h_img, exact=True):
                    renpy.show(_h_img, tag="dg_head_above", at_list=_slot_at0, zorder=_over_z + 1)

    $ renpy.pause(0.25)

    python:
        _butt_at = [dg_get_slot_transform(0), dg_get_butt_transform(0), dg_get_butt_shrink_transform(0)]
        if store.doggy_anal:
            debug_log("[ENTER] DURING ANAL")
            renpy.show("%s doggy_ass_during_anal_below" % girl.gid, tag="dg_during_below", at_list=_butt_at, zorder=10060)
            renpy.show("%s doggy_ass_during_anal" % girl.gid, tag="dg_during", at_list=_butt_at, zorder=10064)
            renpy.hide("dg_base_ass")
        else:
            debug_log("[ENTER] DURING PUSSY")
            renpy.show("%s doggy_ass_during_pussy_below" % girl.gid, tag="dg_during_below", at_list=_butt_at, zorder=10048)
            renpy.show("%s doggy_ass_during_pussy" % girl.gid, tag="dg_during", at_list=_butt_at, zorder=10053)
            renpy.hide("dg_base_pussy")

    $ renpy.pause(0.30)
    return

# ═══════════════════════════════════════════════════════════
# DG_PenisExitAnim — penis slide-out animation
# ═══════════════════════════════════════════════════════════
label DG_PenisExitAnim(girl):
    if girl.gid == "shion":
        # the penis layer carries her condom too (_sdg_show_penis)
        $ renpy.hide("sdg_penis")
        $ renpy.pause(0.3)
        return
    python:
        debug_log("[EXIT] doggy_anal=%s" % store.doggy_anal)

        _pen_img = "%s doggy_penis" % girl.gid
        _pen_z = _dg_pen_z()
        _slide_tf = dga_penis_slide_out if store.doggy_anal else dg_penis_slide_out
        debug_log("[EXIT] slide=%s" % ("ANAL" if store.doggy_anal else "VAGINAL"))
        renpy.show(_pen_img, tag="dg_penis", at_list=[_slide_tf], zorder=_pen_z)
        if store.condom_active:
            _cb_cimg = _condom_img_tag("dg_condom")
            renpy.show(_cb_cimg, tag="dg_condom", at_list=[_slide_tf], zorder=_pen_z)
    $ renpy.pause(0.55)
    python:
        renpy.hide("dg_penis")
        renpy.hide("dg_condom")
        debug_log("[EXIT] penis hidden")
    return

# ═══════════════════════════════════════════════════════════
# DG_CondomRemoveAnim — slide out with condom, slide back in raw
# Called AFTER _on_condom_removed already ran (condom layer hidden).
# We re-show the condom image so it slides out visibly.
# ═══════════════════════════════════════════════════════════
label DG_CondomRemoveAnim(girl):
    if girl.gid == "shion":
        # he pulls out (the penis layer carries the condom: _sdg_show_penis) and goes back in bare; re-show
        # everything so the penis comes back in phase with his thrusting body
        $ renpy.hide("sdg_penis")
        $ renpy.pause(0.3)
        $ _sdg_apply_speed(girl, store.doggy_speed)
        $ renpy.pause(0.3)
        return
    python:
        _pen_img = "%s doggy_penis" % girl.gid
        _pen_z = _dg_pen_z()
        _slide_tf = dga_penis_slide_out if store.doggy_anal else dg_penis_slide_out
        # Slide penis + condom out together
        _dg_condom_tag = _condom_img_tag("dg_condom")
        renpy.show(_pen_img, tag="dg_penis", at_list=[_slide_tf], zorder=_pen_z)
        renpy.show(_dg_condom_tag, tag="dg_condom", at_list=[_slide_tf], zorder=_pen_z)
    $ renpy.pause(0.6)
    # Everything off screen now — hide condom, slide penis back in raw
    python:
        renpy.hide("dg_condom")
        renpy.hide("dg_penis")
        _pen_img = "%s doggy_penis" % girl.gid
        _pen_z = _dg_pen_z()
        _slide_tf = dga_penis_slide_in if store.doggy_anal else dg_penis_slide_in
        renpy.show(_pen_img, tag="dg_penis", at_list=[_slide_tf], zorder=_pen_z)
    $ renpy.pause(0.6)
    return

# ═══════════════════════════════════════════════════════════
# DG_CumAnim — cum inside animation (speed 4 + screen shake)
# ═══════════════════════════════════════════════════════════

transform dg_penis_cum_pulse():
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    xoffset 0
    yoffset 75
    yzoom 1.0
    pause 0.45
    ease 0.08 yzoom 1.06
    ease 0.15 yzoom 1.0
    pause 0.27
    ease 0.08 yzoom 1.06
    ease 0.15 yzoom 1.0

transform dga_penis_cum_pulse():
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    xoffset 0
    yoffset -10
    yzoom 1.0
    pause 0.45
    ease 0.08 yzoom 1.06
    ease 0.15 yzoom 1.0

transform dg_penis_cum_freeze:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    xoffset 0
    yoffset 15
    yzoom 1.0
    pause 0.27
    ease 0.08 yzoom 1.06
    ease 0.15 yzoom 1.0

transform dga_penis_cum_freeze:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    xoffset 0
    yoffset -10
    pause 0.27
    ease 0.08 yzoom 1.06
    ease 0.15 yzoom 1.0

label DG_CumAnim(girl):
    if girl.gid == "shion":
        $ _apply_cum_expression(girl, "doggy", "inside")
        $ store.doggy_speed = 4
        call DG_ApplySpeed(girl, 4) from _call_DG_ApplySpeed_cum_shion
        call _cum_punch_pair("rear") from _call_cum_punch_dg_cum_shion
        $ store.doggy_speed = 0
        call DG_ApplySpeed(girl, 0) from _call_DG_ApplySpeed_cum_freeze_shion
        python:
            # only the layer of THIS load (process_cum has not written girl.Cum yet), riding her butt,
            # dripping under the penis (the author 2026-10-11: the old loop showed all three, static,
            # at z 10003 over everything). Nothing drips from her when it stayed in the condom
            _sdg_show_cum(girl, now=(None if condom_holds_load() else ("dripping_ass" if store.doggy_anal else "dripping")))
        return
    # Cum expression: intense orgasm face
    $ _dg_prev_cum_speed = store.doggy_speed
    $ _dg_prev_grab = store.doggy_grab
    $ _apply_cum_expression(girl, "doggy", "inside")

    # Activate grab (hands grip during cum)
    $ store.doggy_grab = True
    # Speed 4 (cumming: deep, short thrusts)
    $ store.doggy_speed = 4
    call DG_ApplySpeed(girl, 4) from _call_DG_ApplySpeed_cum

    # Penis pulse (+ condom if active)
    python:
        _cum_pulse = dga_penis_cum_pulse() if store.doggy_anal else dg_penis_cum_pulse()
        renpy.show("%s doggy_penis" % girl.gid, tag="dg_penis", at_list=[_cum_pulse], zorder=_dg_pen_z())
        if store.condom_active:
            _cb_cimg = _condom_img_tag("dg_condom")
            renpy.show(_cb_cimg, tag="dg_condom", at_list=[_cum_pulse], zorder=_dg_pen_z())

    call _cum_punch_pair("rear") from _call_cum_punch_dg_cum

    # Release grab, freeze at speed 0 for aftermath
    $ store.doggy_grab = _dg_prev_grab
    $ store.doggy_speed = 0
    call DG_ApplySpeed(girl, 0) from _call_DG_ApplySpeed_cum_freeze

    # Penis stays inside after cum — re-show "during" layer and static penis
    python:
        if store.doggy_started:
            _static_at = [dg_get_slot_transform(0), dg_get_butt_transform(0), dg_get_butt_shrink_transform(0)]
            if store.doggy_anal:
                renpy.show("%s doggy_ass_during_anal" % girl.gid, tag="dg_during", at_list=_static_at, zorder=10064)
            else:
                renpy.show("%s doggy_ass_during_pussy" % girl.gid, tag="dg_during", at_list=_static_at, zorder=10053)
                renpy.hide("dg_base_pussy")
            _pen_tf = dga_penis_cum_freeze if store.doggy_anal else dg_penis_cum_freeze
            _freeze_pen_z = _dg_pen_z() if store.doggy_anal else 10080
            renpy.show("%s doggy_penis" % girl.gid, tag="dg_penis", at_list=[_pen_tf], zorder=_freeze_pen_z)
            if store._condom_broken:
                renpy.show("dg_condom_broken", tag="dg_condom", at_list=[_pen_tf], zorder=_freeze_pen_z)
            else:
                renpy.hide("dg_condom")
            _bs_z = 10051 if not store.doggy_anal else 10059
            _slot_at0 = [dg_get_slot_transform(0)]
            renpy.show("%s doggy_body_safe" % girl.gid, tag="dg_body_safe", at_list=_slot_at0, zorder=_bs_z)
            _c_val = girl.clothes.get("chest")
            _c_map = {"corset": "doggy_corset", "crop_top": "doggy_corset", "bikini_top": "doggy_bikini_top"}
            _c_key = _c_map.get(_c_val)
            if _c_key:
                _c_img = "%s %s" % (girl.gid, _c_key)
                if renpy.has_image(_c_img, exact=True):
                    renpy.show(_c_img, tag="dg_chest_over", at_list=_slot_at0, zorder=_bs_z + 1)
            _over_z = 10054 if not store.doggy_anal else 10060
            _o_val = girl.clothes.get("over")
            _o_map = {"long_shirt": "doggy_mesh_top"}
            _o_key = _o_map.get(_o_val)
            if _o_key:
                _o_img = "%s %s" % (girl.gid, _o_key)
                if renpy.has_image(_o_img, exact=True):
                    renpy.show(_o_img, tag="dg_over_above", at_list=_slot_at0, zorder=_over_z)
                    _h_img = "%s doggy_head" % girl.gid
                    if renpy.has_image(_h_img, exact=True):
                        renpy.show(_h_img, tag="dg_head_above", at_list=_slot_at0, zorder=_over_z + 1)

    # Show dripping just below penis (above butt layers): only when his load went into her (not into the condom)
    python:
        _freeze_drip_z = _dg_pen_z() - 1 if store.doggy_anal else 10079
        if condom_holds_load():
            renpy.hide("dg_ca_dripping")
        elif store.doggy_anal:
            renpy.show("%s doggy_dripping_ass_cum" % girl.gid, tag="dg_ca_dripping", zorder=_freeze_drip_z)
        else:
            renpy.show("%s doggy_dripping_cum" % girl.gid, tag="dg_ca_dripping", zorder=_freeze_drip_z)

    return

# ═══════════════════════════════════════════════════════════
# DG_CumOutsideFreeze — freeze pose, slide penis out+in, shake
# ═══════════════════════════════════════════════════════════
label DG_CumOutsideFreeze(girl):
    if girl.gid == "shion":
        python:
            store.condom_active = False
            _apply_cum_expression(girl, "doggy", "outside")
            store.doggy_grab = False
            # he pulled out to cum on her: the penis over her, her hole closed (the "After" patch: he was in it)
            store._sdg_penis_out = "out"
        call DG_ApplySpeed(girl, 0) from _call_DG_ApplySpeed_cum_outside_shion
        call _cum_punch_pair("rear") from _call_cum_punch_dg_outside_shion
        python:
            # outside = on her butt only ("ass"), riding her (process_cum runs after this anim)
            _sdg_show_cum(girl, now="ass")
        return
    $ _had_condom = store.condom_active
    python:
        store.condom_active = False
        _apply_cum_expression(girl, "doggy", "outside")

        _static_slot = dg_get_slot_transform(0)
        _ca_at = [_static_slot]

        # Freeze body (layeredimage) — chest/over stripped exactly like DG_ApplySpeed
        # (their standalones stay shown below the freeze penis at z 10084)
        _fr_attrs = _build_doggy_attributes(girl)
        _fr_o_key = {"long_shirt": "doggy_mesh_top"}.get(girl.clothes.get("over"))
        _fr_show_over = bool(_fr_o_key) and renpy.has_image("%s %s" % (girl.gid, _fr_o_key), exact=True)
        if _fr_show_over:
            _fr_attrs = [a for a in _fr_attrs if "torso_over" not in a] + ["torso_over_none"]
        _fr_c_key = {"corset": "doggy_corset", "crop_top": "doggy_corset", "bikini_top": "doggy_bikini_top"}.get(girl.clothes.get("chest"))
        _fr_show_chest = bool(_fr_c_key) and renpy.has_image("%s %s" % (girl.gid, _fr_c_key), exact=True)
        if _fr_show_chest:
            _fr_attrs = [a for a in _fr_attrs if "torso_chest" not in a] + ["torso_chest_none"]
        _fr_img = "%s doggy" % girl.gid
        if _fr_attrs:
            _fr_img += " " + " ".join(_fr_attrs)
        renpy.show(_fr_img, tag=girl.gid, at_list=_ca_at, zorder=9980)

        # Freeze boobs, hide body_safe (penis sliding out)
        renpy.show("%s doggy_boobs" % girl.gid, tag="dg_boobs", at_list=_ca_at, zorder=9979)
        renpy.hide("dg_body_safe")
        if _fr_show_chest:
            renpy.show("%s %s" % (girl.gid, _fr_c_key), tag="dg_chest_over", at_list=_ca_at, zorder=10052)
        else:
            renpy.hide("dg_chest_over")
        if _fr_show_over:
            renpy.show("%s %s" % (girl.gid, _fr_o_key), tag="dg_over_above", at_list=_ca_at, zorder=10054)
            _fr_h_img = "%s doggy_head" % girl.gid
            if renpy.has_image(_fr_h_img, exact=True):
                renpy.show(_fr_h_img, tag="dg_head_above", at_list=_ca_at, zorder=10055)
        else:
            renpy.hide("dg_over_above")
            renpy.hide("dg_head_above")
        print("[DG_FREEZE] chest_over=%s over_above=%s" % (_fr_show_chest, _fr_show_over))

        # Freeze calves + legs + foot
        renpy.show("%s doggy_calves_left" % girl.gid, tag="dg_calves_left", at_list=[dg_calves_static], zorder=9970)
        renpy.show("%s doggy_calves_right" % girl.gid, tag="dg_calves_right", at_list=[dg_calves_static], zorder=9970)
        renpy.show("%s doggy_legs_left" % girl.gid, tag="dg_legs_left", at_list=[dg_calves_static], zorder=9972)
        renpy.show("%s doggy_legs_right" % girl.gid, tag="dg_legs_right", at_list=[dg_calves_static], zorder=9972)
        renpy.show("%s doggy_foot_left" % girl.gid, tag="dg_foot_left", at_list=[dg_calves_static], zorder=9974)
        renpy.show("%s doggy_foot_right" % girl.gid, tag="dg_foot_right", at_list=[dg_calves_static], zorder=9974)

        # Freeze butt layers — use sex-mode layout (matches DG_ApplySpeed(0))
        _dg_show_butt_layers(girl, 0)

        # Freeze clothing
        if getattr(girl, "Shoes", None):
            _thc_l = "%s doggy_thigh_highs_calves_left" % girl.gid
            if renpy.has_image(_thc_l, exact=True):
                renpy.show(_thc_l, tag="dg_thigh_highs_calves_left", at_list=[dg_calves_static], zorder=9971)
                renpy.show("%s doggy_thigh_highs_calves_right" % girl.gid, tag="dg_thigh_highs_calves_right", at_list=[dg_calves_static], zorder=9971)
            else:
                renpy.show("%s doggy_thigh_highs_calves" % girl.gid, tag="dg_thigh_highs_calves", at_list=[dg_calves_static], zorder=9971)
            _thf_l = "%s doggy_thigh_highs_foot_left" % girl.gid
            if renpy.has_image(_thf_l, exact=True):
                renpy.show(_thf_l, tag="dg_thigh_highs_foot_left", at_list=[dg_calves_static], zorder=9975)
                renpy.show("%s doggy_thigh_highs_foot_right" % girl.gid, tag="dg_thigh_highs_foot_right", at_list=[dg_calves_static], zorder=9975)
            renpy.show("%s doggy_thigh_highs_legs_left" % girl.gid, tag="dg_thigh_highs_legs_left", at_list=[dg_calves_static], zorder=9973)
            renpy.show("%s doggy_thigh_highs_legs_right" % girl.gid, tag="dg_thigh_highs_legs_right", at_list=[dg_calves_static], zorder=9973)

        renpy.hide("dg_panties")
        renpy.hide("dg_panties_right")
        renpy.hide("dg_panties_left")
        if girl.Panties:
            _ca_pan_state = girl.clothes_state.get("panties", "full")
            if store.doggy_started and _ca_pan_state == "full":
                pass
            elif _ca_pan_state == "side":
                _pan_r = "%s doggy_panties_%s_side_right" % (girl.gid, girl.Panties)
                _pan_l = "%s doggy_panties_%s_side_left" % (girl.gid, girl.Panties)
                if renpy.has_image(_pan_r, exact=True) and renpy.has_image(_pan_l, exact=True):
                    _bd0 = [_static_slot, dg_get_butt_transform(0), dg_get_butt_shrink_transform(0)]
                    renpy.show(_pan_r, tag="dg_panties_right", at_list=_bd0, zorder=10071)
                    renpy.show(_pan_l, tag="dg_panties_left", at_list=_bd0, zorder=10071)
                else:
                    _ca_pan_img = "%s doggy_panties_%s_side" % (girl.gid, girl.Panties)
                    if store.doggy_anal:
                        _ca_pan_anal = "%s doggy_panties_%s_side_anal" % (girl.gid, girl.Panties)
                        if renpy.has_image(_ca_pan_anal, exact=True):
                            _ca_pan_img = _ca_pan_anal
                    if renpy.has_image(_ca_pan_img, exact=True):
                        renpy.show(_ca_pan_img, tag="dg_panties", at_list=_ca_at, zorder=10079)
            elif _ca_pan_state != "full":
                _ca_pan_img = "%s doggy_panties_%s_%s" % (girl.gid, girl.Panties, _ca_pan_state)
                if renpy.has_image(_ca_pan_img, exact=True):
                    renpy.show(_ca_pan_img, tag="dg_panties", at_list=_ca_at, zorder=10079)

        if girl.Legs:
            _ca_skirt_state = girl.clothes_state.get("skirt", "full")
            _clothing_at0 = [_static_slot, dg_get_butt_transform(0), dg_get_skirt_zoom_transform(0)]
            if _ca_skirt_state == "up" or store.doggy_started:
                _ca_skirt_img = "%s doggy_skirt_up" % girl.gid
                _ca_skirt_safe = "%s doggy_skirt_up_safe" % girl.gid
                if renpy.has_image(_ca_skirt_img, exact=True):
                    renpy.show(_ca_skirt_img, tag="dg_skirt", at_list=_clothing_at0, zorder=10080)
                if renpy.has_image(_ca_skirt_safe, exact=True):
                    renpy.show(_ca_skirt_safe, tag="dg_skirt_safe", at_list=_clothing_at0, zorder=9985)
            else:
                _ca_skirt_img = "%s doggy_skirt" % girl.gid
                if renpy.has_image(_ca_skirt_img, exact=True):
                    renpy.show(_ca_skirt_img, tag="dg_skirt", at_list=_clothing_at0, zorder=10080)

        _sa = "%s doggy_shirt_arms" % girl.gid
        if girl.clothes.get("over") and renpy.has_image(_sa, exact=True):
            renpy.show(_sa, tag="dg_shirt_arms", at_list=_ca_at, zorder=9981)

        # Freeze existing cum at static transform (don't hide — previous cum must stay visible)
        _cum_z = _dg_cum_z()
        renpy.show("%s doggy_butt_cum" % girl.gid, tag="dg_butt_cum", at_list=_ca_at, zorder=_cum_z)
        renpy.show("%s doggy_back_cum" % girl.gid, tag="dg_back_cum", at_list=_ca_at, zorder=_cum_z + 1)
        renpy.show("%s doggy_dripping_cum" % girl.gid, tag="dg_dripping_cum", at_list=_ca_at, zorder=10049)
        renpy.show("%s doggy_dripping_ass_cum" % girl.gid, tag="dg_dripping_ass_cum", at_list=_ca_at, zorder=10049)
        for _t in ("dg_grab_left", "dg_grab_right"):
            renpy.hide(_t)
        store.doggy_grab = False

    python:
        _pen_z = 10084
        _pen_img = "%s doggy_penis" % girl.gid
        _was_rub = getattr(store, "doggy_rub_mode", False)

    if _was_rub:
        # Rub: penis was never inside, show on top directly
        python:
            _pen_tf = dga_get_penis_transform(0) if store.doggy_anal else dg_get_penis_transform(0)
            renpy.show(_pen_img, tag="dg_penis", at_list=[_pen_tf], zorder=_pen_z)
    else:
        # Sex/tip: slide penis out then back in on top
        python:
            _slide_out = dga_penis_slide_out if store.doggy_anal else dg_penis_slide_out
            if _had_condom:
                _cb_cimg = _condom_img_tag("dg_condom")
                renpy.show(_cb_cimg, tag="dg_condom", at_list=[_slide_out], zorder=_pen_z)
            renpy.show(_pen_img, tag="dg_penis", at_list=[_slide_out], zorder=_pen_z)
        $ renpy.pause(0.6)
        python:
            renpy.hide("dg_condom")
            renpy.hide("dg_penis")
            _pen_img = "%s doggy_penis" % girl.gid
            _slide_in = dga_penis_slide_in if store.doggy_anal else dg_penis_slide_in
            renpy.show(_pen_img, tag="dg_penis", at_list=[_slide_in], zorder=_pen_z)
        $ renpy.pause(0.6)

    # Override with cum pulse on top
    python:
        _cum_pulse = dga_penis_cum_pulse() if store.doggy_anal else dg_penis_cum_pulse()
        renpy.show("%s doggy_penis" % girl.gid, tag="dg_penis", at_list=[_cum_pulse], zorder=_pen_z)

    call _cum_punch_pair("rear") from _call_cum_punch_dg_outside

    # After punches: static penis
    python:
        _ca_at = [dg_get_slot_transform(0)]
        _pen_tf = dga_get_penis_transform(0) if store.doggy_anal else dg_get_penis_transform(0)
        renpy.show("%s doggy_penis" % girl.gid, tag="dg_penis", at_list=[_pen_tf], zorder=_pen_z)

    return

# ═══════════════════════════════════════════════════════════
# DG_CreampieAftermath — static pose after cum inside
# ═══════════════════════════════════════════════════════════
label DG_CreampieAftermath(girl):
    if girl.gid == "shion":
        python:
            # he pulls out of her at last: the penis gone, the hole he was in gaping ("After"), his cum dripping.
            # A hide of the penis alone came back with the DG_ApplySpeed below (his layers are redrawn there)
            store._sdg_penis_out = "hidden"
            store.doggy_grab = False
        # girl.Cum is written by now: this DG_ApplySpeed(0) draws the right cum layers riding her (_sdg_show_cum
        # inside _sdg_apply_speed); nothing more to show here
        call DG_ApplySpeed(girl, 0) from _call_DG_ApplySpeed_creampie_shion
        return
    python:
        if store.doggy_started:
            _static_at = [dg_get_slot_transform(0), dg_get_butt_transform(0), dg_get_butt_shrink_transform(0)]
            renpy.hide("dg_during")
            renpy.hide("dg_during_below")
            if store.doggy_anal:
                renpy.show("%s doggy_ass_after_ass" % girl.gid, tag="dg_base_ass", at_list=_static_at, zorder=10058)
                renpy.show("%s doggy_penis" % girl.gid, tag="dg_penis", at_list=[dga_penis_slide_out], zorder=10060)
            else:
                renpy.show("%s doggy_ass_after_pussy" % girl.gid, tag="dg_base_pussy", at_list=_static_at, zorder=10058)
                renpy.hide("dg_penis")
            renpy.hide("dg_condom")
    if store.doggy_started and store.doggy_anal:
        $ renpy.pause(0.45)
    $ renpy.hide("dg_penis")

    # Freeze entire scene at speed 0 (swaps to "after" layers)
    call DG_ApplySpeed(girl, 0) from _call_DG_ApplySpeed_creampie_aftermath

    # Hide condom, grabs
    python:
        renpy.hide("dg_condom")
        renpy.hide("dg_grab_left")
        renpy.hide("dg_grab_right")
        renpy.hide("dg_ass_safe")
        store.doggy_grab = False

        # Re-show body_safe + clothing (hidden by ApplySpeed at speed 0)
        _ca_slot = [dg_get_slot_transform(0)]
        _bs_z = 10051 if not store.doggy_anal else 10059
        renpy.show("%s doggy_body_safe" % girl.gid, tag="dg_body_safe", at_list=_ca_slot, zorder=_bs_z)
        _c_val = girl.clothes.get("chest")
        _c_map = {"corset": "doggy_corset", "crop_top": "doggy_corset", "bikini_top": "doggy_bikini_top"}
        _c_key = _c_map.get(_c_val)
        if _c_key:
            _c_img = "%s %s" % (girl.gid, _c_key)
            if renpy.has_image(_c_img, exact=True):
                renpy.show(_c_img, tag="dg_chest_over", at_list=_ca_slot, zorder=_bs_z + 1)
        _over_z = 10054 if not store.doggy_anal else 10060
        _o_val = girl.clothes.get("over")
        _o_map = {"long_shirt": "doggy_mesh_top"}
        _o_key = _o_map.get(_o_val)
        if _o_key:
            _o_img = "%s %s" % (girl.gid, _o_key)
            if renpy.has_image(_o_img, exact=True):
                renpy.show(_o_img, tag="dg_over_above", at_list=_ca_slot, zorder=_over_z)
                _h_img = "%s doggy_head" % girl.gid
                if renpy.has_image(_h_img, exact=True):
                    renpy.show(_h_img, tag="dg_head_above", at_list=_ca_slot, zorder=_over_z + 1)

        # Re-show panties with static transforms (animated halves killed)
        renpy.hide("dg_panties_right")
        renpy.hide("dg_panties_left")
        renpy.hide("dg_panties")
        _pan_item = girl.Panties
        if _pan_item:
            _pan_state = girl.clothes_state.get("panties", "full")
            if store.doggy_started and _pan_state == "full":
                pass
            elif _pan_state == "side":
                _pan_r = "%s doggy_panties_%s_side_right" % (girl.gid, _pan_item)
                _pan_l = "%s doggy_panties_%s_side_left" % (girl.gid, _pan_item)
                _bd0 = [dg_get_slot_transform(0), dg_get_butt_transform(0), dg_get_butt_shrink_transform(0)]
                if renpy.has_image(_pan_r, exact=True) and renpy.has_image(_pan_l, exact=True):
                    renpy.show(_pan_r, tag="dg_panties_right", at_list=_bd0, zorder=10071)
                    renpy.show(_pan_l, tag="dg_panties_left", at_list=_bd0, zorder=10071)
                else:
                    _pan_img = "%s doggy_panties_%s_side" % (girl.gid, _pan_item)
                    if store.doggy_anal:
                        _pan_img_anal = "%s doggy_panties_%s_side_anal" % (girl.gid, _pan_item)
                        if renpy.has_image(_pan_img_anal, exact=True):
                            _pan_img = _pan_img_anal
                    if renpy.has_image(_pan_img, exact=True):
                        renpy.show(_pan_img, tag="dg_panties", at_list=_ca_slot, zorder=10079)
            elif _pan_state != "full":
                _pan_img = "%s doggy_panties_%s_%s" % (girl.gid, _pan_item, _pan_state)
                if renpy.has_image(_pan_img, exact=True):
                    renpy.show(_pan_img, tag="dg_panties", at_list=_ca_slot, zorder=10079)

        # Re-show dripping at high zorder (above after_pussy/after_ass)
        renpy.hide("dg_dripping_cum")
        renpy.hide("dg_dripping_ass_cum")
        _ca_drip_z = _dg_pen_z() - 1 if store.doggy_anal else 10079
        if store.doggy_anal:
            renpy.show("%s doggy_dripping_ass_cum" % girl.gid, tag="dg_ca_dripping", zorder=_ca_drip_z)
        else:
            renpy.show("%s doggy_dripping_cum" % girl.gid, tag="dg_ca_dripping", zorder=_ca_drip_z)
        renpy.show("%s doggy_butt_cum" % girl.gid, tag="dg_ca_butt_cum", zorder=10091)
        if "back" in getattr(girl, "Cum", []):
            renpy.show("%s doggy_back_cum" % girl.gid, tag="dg_ca_back_cum", zorder=10092)

    return

# ═══════════════════════════════════════════════════════════
# DG_PlayerCumMenu_RubOutside — cum during doggy rub
# ═══════════════════════════════════════════════════════════
label DG_PlayerCumMenu_RubOutside(girl):

    "You feel yourself getting close..."
    $ _dg_scene_type = "anal" if store.doggy_anal else "doggy"

    menu:
        "Fire away":
            call DG_CumOutsideFreeze(girl) from _call_DG_CumOutsideFreeze_rub_fire
            "You cum."
            $ process_cum(girl, _dg_scene_type, "away")
            $ apply_cum_bonuses(girl, "cum_outside")

        "Cum outside":
            $ _dg_cum_type = "ass"
            menu:
                "On her ass":
                    $ _dg_cum_type = "ass"
                "On her back":
                    $ _dg_cum_type = "back"
                "All over her":
                    $ _dg_cum_type = "outside"

            call DG_CumOutsideFreeze(girl) from _call_DG_CumOutsideFreeze_rub_out

            if _dg_cum_type == "ass":
                "You cum on her ass."
                $ process_cum(girl, _dg_scene_type, "ass")
            elif _dg_cum_type == "back":
                "You cum on her back."
                $ process_cum(girl, _dg_scene_type, "back")
            else:
                "You cum all over her."
                $ process_cum(girl, _dg_scene_type, "outside", ["ass", "back"])

            $ apply_cum_bonuses(girl, "cum_outside")
            $ _cum_say_line(girl, _dg_cum_type, _dg_scene_type)

    $ Player.Focus = 0

    return

# ═══════════════════════════════════════════════════════════
# DG_TipDeniedCumVisual — outside cum sprites on denied creampie
# ═══════════════════════════════════════════════════════════
label DG_TipDeniedCumVisual(girl):
    if girl.gid == "shion":
        python:
            if renpy.has_image("shion sdg_cum_butt", exact=True):
                renpy.show("shion sdg_cum_butt", tag="sdg_cum_butt", zorder=10003)
        return
    python:
        _ca_at = [dg_get_slot_transform(0)]
        _cum_z = _dg_cum_z()
        renpy.show("%s doggy_butt_cum" % girl.gid, tag="dg_butt_cum", at_list=_ca_at, zorder=_cum_z)
    return

# ═══════════════════════════════════════════════════════════
# DG_PlayerCumMenu_TipOutside — cum during doggy tip
# ═══════════════════════════════════════════════════════════
label DG_PlayerCumMenu_TipOutside(girl):

    "You feel yourself getting close..."
    $ _dg_scene_type = "anal" if store.doggy_anal else "doggy"

    menu:
        "Fire away":
            call DG_CumOutsideFreeze(girl) from _call_DG_CumOutsideFreeze_tip_fire
            "You pull out and cum."
            $ process_cum(girl, _dg_scene_type, "away")
            $ apply_cum_bonuses(girl, "cum_outside")

        "Cum outside":
            $ _dg_cum_type = "ass"
            menu:
                "On her ass":
                    $ _dg_cum_type = "ass"
                "On her back":
                    $ _dg_cum_type = "back"
                "All over her":
                    $ _dg_cum_type = "outside"

            call DG_CumOutsideFreeze(girl) from _call_DG_CumOutsideFreeze_tip_out

            if _dg_cum_type == "ass":
                "You pull out and cum on her ass."
                $ process_cum(girl, _dg_scene_type, "ass")
            elif _dg_cum_type == "back":
                "You pull out and cum on her back."
                $ process_cum(girl, _dg_scene_type, "back")
            else:
                "You pull out and cum all over her."
                $ process_cum(girl, _dg_scene_type, "outside", ["ass", "back"])

            python:
                if girl.gid != "shion":
                    _ca_at = [dg_get_slot_transform(0)]
                    _cum_z = _dg_cum_z()
                    renpy.show("%s doggy_butt_cum" % girl.gid, tag="dg_butt_cum", at_list=_ca_at, zorder=_cum_z)
                    renpy.show("%s doggy_back_cum" % girl.gid, tag="dg_back_cum", at_list=_ca_at, zorder=_cum_z + 1)
            $ apply_cum_bonuses(girl, "cum_outside")

        "Ask to cum in her mouth":
            if _dg_scene_type == "anal":
                $ _cum_check = CumPermissionCheck(girl, "cum_in_mouth_from_anal_ask")
                if _cum_check["accepted"]:
                    python:
                        _atm_pre = renpy.random.choice([
                            _("From my ass to my mouth? ...Fine. Pull out and give it to me."),

                            _("You want me to taste where it's been? ...Okay. Do it."),

                        ])
                        Say_Line(girl, _atm_pre)
                    # Track first kiss flag for tip ATM (same as full ATM path)
                    $ store._never_kissed_before_atm = "kiss" not in getattr(girl, "intimacy_flags", set())
                    # ONE registration point for every ATM path (Cum.rpy atm_register): counters, Firsts["atm"],
                    # recording tag, achievement and the ATM context. Firsts["cum_mouth"] is written by process_cum().
                    $ atm_register(girl, where="dg_tip_menu")
                    call _cum_in_mouth_via_bj(girl, _dg_scene_type) from _call__cum_in_mouth_via_bj_tip_atm
                else:
                    python:
                        _atm_deny = renpy.random.choice([
                            _("From my ass to my mouth? No way. Not happening."),

                            _("It was in my ass. I'm not putting that in my mouth."),

                        ])
                        Say_Line(girl, _atm_deny)
                    call DG_CumOutsideFreeze(girl) from _call_DG_CumOutsideFreeze_tip_atm_denied
                    "You pull out and cum on her ass."
                    $ process_cum(girl, _dg_scene_type, "ass")
                    python:
                        if girl.gid != "shion":
                            _ca_at = [dg_get_slot_transform(0)]
                            _cum_z = _dg_cum_z()
                            renpy.show("%s doggy_butt_cum" % girl.gid, tag="dg_butt_cum", at_list=_ca_at, zorder=_cum_z)
                    $ apply_cum_bonuses(girl, "cum_outside")
            else:
                $ _cum_check = CumPermissionCheck(girl, "cum_in_mouth_ask")
                if _cum_check["accepted"]:
                    $ Say_Line(girl, scene_pick_line("cum_mouth_accepted", scene=_dg_scene_type, girl=girl) or "Go ahead... do it.")
                    call _cum_in_mouth_via_bj(girl, _dg_scene_type) from _call__cum_in_mouth_via_bj_tip_normal
                else:
                    $ Say_Line(girl, scene_pick_line("cum_mouth_denied", scene=_dg_scene_type, girl=girl) or "No way... not in my mouth.")
                    call DG_CumOutsideFreeze(girl) from _call_DG_CumOutsideFreeze_tip_mouth_denied
                    "You pull out and cum on her ass."
                    $ process_cum(girl, _dg_scene_type, "ass")
                    python:
                        if girl.gid != "shion":
                            _ca_at = [dg_get_slot_transform(0)]
                            _cum_z = _dg_cum_z()
                            renpy.show("%s doggy_butt_cum" % girl.gid, tag="dg_butt_cum", at_list=_ca_at, zorder=_cum_z)
                    $ apply_cum_bonuses(girl, "cum_outside")

        "Ask to cum inside":
            call _tip_ask_cum_inside(girl, _dg_scene_type) from _call_tip_ask_dg

        "Cum inside her":
            call _tip_force_cum_inside(girl, _dg_scene_type) from _call_tip_force_dg

    $ Player.Focus = 0

    return

# ============================================================
# Secret recording — filmed without her knowledge
# ============================================================
label _dg_secret_recording(girl, position):
    python:
        store._recording_active = True
        store._recording_girl = girl
        store._recording_face_locked = False
        store._player_hand_disabled = renpy.random.choice(["left", "right"])
        _pen = scene_type_is_penetration(position)
        vid = {
            "girl_gid": girl.gid,
            "type": position,
            "location": CurrentLocation,
            "committed": girl.has_npc_partner(),
            "consensual": False,
            "reluctant": False,
            "face_hidden": True,
            "hd": Player.has_item("tekmix_camera"),
            "snapshot": _make_vid_snapshot(girl),
        }
        if _pen:
            vid["condom"] = bool(store.condom_active)
        _tag_coercion_on_vid(vid)
        store.Player.recorded_videos.append(vid)
        renpy.show_screen("recording_overlay")
    "You quietly pull out your phone and start recording. She doesn't notice."
    return

# ============================================================
# Ask to record — consent check, no extra menu
# ============================================================
label _dg_ask_recording(girl, position):
    $ _rec_ok = recording_consent_check(girl, position)
    if _rec_ok["accepted"]:
        python:
            store._recording_active = True
            store._recording_girl = girl
            store._recording_face_locked = False
            store._player_hand_disabled = renpy.random.choice(["left", "right"])
            _pen = scene_type_is_penetration(position)
            _is_reluctant = girl.has_trait("camera_hater")
            vid = {
                "girl_gid": girl.gid,
                "type": position,
                "location": CurrentLocation,
                "committed": girl.has_npc_partner(),
                "consensual": True,
                "reluctant": _is_reluctant,
                "face_hidden": True,
                "hd": Player.has_item("tekmix_camera"),
                "snapshot": _make_vid_snapshot(girl),
            }
            if _pen:
                vid["condom"] = bool(store.condom_active)
            _tag_coercion_on_vid(vid)
            store.Player.recorded_videos.append(vid)
            renpy.show_screen("recording_overlay")
            if _is_reluctant:
                unlock_achievement("say_cheese")
                Change_Status(girl, "Love", -3)
                if girl.has_npc_partner():
                    Change_Status(girl, "Love", -2)
        $ _line = _format_partner_line(girl, scene_pick_line("record_accepted", scene=position, girl=girl))
        $ Say_Line(girl, _line)
        call _coercion_recording_react(girl) from _call_coercion_rec_dg_t1
    elif _rec_ok["result"] == "face_hidden_only":
        python:
            store._recording_active = True
            store._recording_girl = girl
            store._recording_face_locked = True
            store._player_hand_disabled = renpy.random.choice(["left", "right"])
            _pen = scene_type_is_penetration(position)
            vid = {
                "girl_gid": girl.gid,
                "type": position,
                "location": CurrentLocation,
                "committed": girl.has_npc_partner(),
                "consensual": True,
                "reluctant": True,
                "face_hidden": True,
                "hd": Player.has_item("tekmix_camera"),
                "snapshot": _make_vid_snapshot(girl),
            }
            if _pen:
                vid["condom"] = bool(store.condom_active)
            _tag_coercion_on_vid(vid)
            store.Player.recorded_videos.append(vid)
            renpy.show_screen("recording_overlay")
        $ _line = _pick_recording_line(girl, "face_hidden_accept")
        $ Say_Line(girl, _line)
        call _coercion_recording_react(girl) from _call_coercion_rec_dg_t2
    else:
        $ _line = _pick_recording_line(girl, "absolute_deny")
        $ Say_Line(girl, _line)
    return
