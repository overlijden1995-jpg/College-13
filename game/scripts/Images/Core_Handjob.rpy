# ============================================================
# CORE HANDJOB SYSTEM (BODY STATIC / CHEST ONLY MOVES)
# ============================================================

default _hj_slot_transform = None
default hj_speed = 1
default _hj_girl = None
default hj_blink = False
default _hj_attrs = []
default _hj_face_ordered_shown = False

init python:
    # -----------------------------
    # PLAYER FOCUS
    # -----------------------------
    def add_player_focus(amount):
        """THE way his arousal (Player.Focus) goes up. Breath, trained by swimming, slows it
        (player_breath_focus_mult); the fraction a tick leaves over carries to the next one."""
        if not hasattr(store, "Player"):
            return
        _gain = round(amount * player_breath_focus_mult() + getattr(store, "_focus_carry", 0.0), 6)   # no float drift
        _add = int(_gain)
        store._focus_carry = _gain - _add
        Player.Focus = min(100, Player.Focus + _add)

    # -----------------------------
    # PENIS TRANSFORM GETTERS (mirrors BJ pattern: per-girl → BJ shared → generic)
    # -----------------------------
    def _hj_get_penis_cum_tf(girl):
        gid = getattr(girl, "gid", "")
        for _name in ["%s_hj_penis_cum_pulse" % gid, "%s_bj_penis_cum_pulse" % gid]:
            _found = getattr(renpy.store, _name, None)
            if _found is not None:
                return _found()
        return hj_penis_cum_pulse()

    def _hj_get_penis_tf(girl):
        gid = getattr(girl, "gid", "")
        for _name in ["%s_hj_penis_static" % gid, "%s_bj_penis_corner" % gid]:
            _found = getattr(renpy.store, _name, None)
            if _found is not None:
                return _found()
        _pov = _gsc(gid, 'pov_overlay', False, pose='handjob')
        return hj_guy_static if _pov else hj_center

    # -----------------------------
    # SLOT TRANSFORM
    # -----------------------------
    def hj_get_slot_transform(speed):
        _gid = getattr(getattr(store, "_scene_girl", None), "gid", "")
        if _gid == "tenny":
            if store._hj_slot_transform == "left":
                slot_map = {0: hj_slot_left_speed0, 1: tenny_hj_slot_left_speed1, 2: tenny_hj_slot_left_speed2, 3: tenny_hj_slot_left_speed3}
            elif store._hj_slot_transform == "right":
                slot_map = {0: hj_slot_right_speed0, 1: tenny_hj_slot_right_speed1, 2: tenny_hj_slot_right_speed2, 3: tenny_hj_slot_right_speed3}
            else:
                slot_map = {0: hj_slot_center_speed0, 1: tenny_hj_slot_center_speed1, 2: tenny_hj_slot_center_speed2, 3: tenny_hj_slot_center_speed3}
        else:
            if store._hj_slot_transform == "left":
                slot_map = {0: hj_slot_left_speed0, 1: hj_slot_left_speed1, 2: hj_slot_left_speed2, 3: hj_slot_left_speed3}
            elif store._hj_slot_transform == "right":
                slot_map = {0: hj_slot_right_speed0, 1: hj_slot_right_speed1, 2: hj_slot_right_speed2, 3: hj_slot_right_speed3}
            else:
                slot_map = {0: hj_slot_center_speed0, 1: hj_slot_center_speed1, 2: hj_slot_center_speed2, 3: hj_slot_center_speed3}

        return slot_map.get(speed, slot_map[1])

    # -----------------------------
    # EXPRESSION POOLS (by speed)
    # -----------------------------
    _HJ_EYES_BY_SPEED = {
        0: ["eyes_normal", "eyes_side", "eyes_side_2"],
        1: ["eyes_normal", "eyes_side", "eyes_squint"],
        2: ["eyes_squint", "eyes_squint_big", "eyes_surprised", "eyes_closed"],
    }

    _HJ_BROWS_BY_SPEED = {
        0: ["brows_normal"],
        1: ["brows_normal", "brows_confused"],
        2: ["brows_surprised", "brows_confused"],
    }

    _HJ_MOUTH_BY_SPEED = {
        0: ["mouth_normal", "mouth_smile"],
        1: ["mouth_normal", "mouth_smile", "mouth_serious"],
        2: ["mouth_surprised", "mouth_open_teeth", "mouth_sch"],
    }

    # -----------------------------
    # EXPRESSION CYCLE (background thread)
    # -----------------------------
    def _hj_update_attrs(girl):
        """Build and cache the full HJ attribute list."""
        attrs = _build_attributes_for_girl(girl, "handjob")
        store._hj_attrs = list(attrs)
        return attrs

    def _hj_show_sprite(girl, attrs=None):
        """Show HJ layeredimage with given attrs (or cached)."""
        if attrs is None:
            attrs = store._hj_attrs
        img_name = "%s handjob" % girl.gid
        if attrs:
            img_name += " " + " ".join(attrs)
        renpy.show(
            img_name,
            tag=girl.gid,
            at_list=[hj_get_slot_transform(store.hj_speed)],
            zorder=9980
        )

    def hj_hand_transform(speed, pov):
        """Her hand's transform at this speed: the hand of HJ_ApplySpeed and the hand cum that rides on it."""
        if pov:
            return {0: hj_pov_hand_static, 1: hj_pov_hand_speed1, 2: hj_pov_hand_speed2,
                    3: hj_pov_hand_speed3}.get(min(speed, 3), hj_pov_hand_speed2)
        return {0: hj_hand_speed0, 1: hj_hand_speed1}.get(speed, hj_hand_speed2)

    def hj_show_hand_cum(girl, speed, pov):
        """His cum on her hand ("hand" in girl.Cum: the ring, shion_netori.rpy), just above her hand."""
        _img = "%s hj_cum_hand" % girl.gid
        if renpy.has_image(_img):
            renpy.show(_img, tag="%s_hj_cum_hand" % girl.gid, at_list=[hj_hand_transform(speed, pov)],
                       zorder=10061 if pov else 9999)

    def _hj_pool_override(girl, speed, eyes_pool, brows_pool, mouth_pool):
        _recording = getattr(store, "_recording_active", False) and getattr(store, "_recording_girl", None) is girl
        if _recording and hasattr(girl, "has_trait") and girl.has_trait("camera_hater"):
            return (["eyes_side", "eyes_side_2", "eyes_squint"],
                    ["brows_confused", "brows_normal"],
                    ["mouth_serious", "mouth_normal"])
        elif _recording and hasattr(girl, "has_trait") and girl.has_trait("camera_lover"):
            return (["eyes_normal", "eyes_squint", "eyes_surprised"],
                    ["brows_normal", "brows_surprised"],
                    ["mouth_smile", "mouth_open_teeth", "mouth_surprised"])
        return (eyes_pool, brows_pool, mouth_pool)

    def _hj_expression_refresh(girl, state):
        if getattr(store, "hiding_face", False):
            state["eyes"] = "eyes_closed"
        new_attrs = []
        for a in store._hj_attrs:
            if a.startswith("brows_"):
                new_attrs.append(state["brows"])
            elif a.startswith("eyes_"):
                new_attrs.append(state["eyes"])
            elif a.startswith("mouth_"):
                new_attrs.append(state["mouth"])
            else:
                new_attrs.append(a)
        _hj_show_sprite(girl, new_attrs)
        renpy.restart_interaction()

    def _hj_expression_cycle(girl):
        _scene_expression_cycle(girl, "_hj_girl", "hj_speed",
            _HJ_EYES_BY_SPEED, _HJ_BROWS_BY_SPEED, _HJ_MOUTH_BY_SPEED,
            pool_override_fn=_hj_pool_override, refresh_fn=_hj_expression_refresh)

# -----------------------------
# CHEST MOVEMENT (VISIBLE)
# -----------------------------
transform hj_chest_speed0():
    subpixel True

transform hj_chest_speed1():
    subpixel True
    block:
        ease 0.55 yoffset 8
        ease 0.55 yoffset 0
        repeat

transform hj_chest_speed2():
    subpixel True
    block:
        ease 0.35 yoffset 14
        ease 0.35 yoffset 0
        ease 0.18 yoffset 6
        ease 0.18 yoffset 0
        repeat

# -----------------------------
# GUY / POV OVERLAY (full scale, no zoom)
# -----------------------------
transform hj_guy_static:
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0

# POV tunable values — shared with F12 Transform Tuner
init python:
    store._hj_pov_ar_ax = 1500
    store._hj_pov_ar_ay = 710
    store._hj_pov_ar_start = 16.0
    store._hj_pov_ar_end = 0.0
    store._hj_pov_al_ax = 1060
    store._hj_pov_al_ay = 745
    store._hj_pov_al_start = -5.0
    store._hj_pov_al_end = 4.0
    store._hj_pov_hand_start = -80
    store._hj_pov_hand_end = 0

transform hj_pov_hand_static:
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset store._hj_pov_hand_start

transform hj_pov_hand_speed1:
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset store._hj_pov_hand_start
    block:
        ease 0.50 yoffset store._hj_pov_hand_end
        ease 0.42 yoffset store._hj_pov_hand_start
        repeat

transform hj_pov_hand_speed2:
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset store._hj_pov_hand_start
    block:
        ease 0.22 yoffset store._hj_pov_hand_end
        ease 0.18 yoffset store._hj_pov_hand_start
        repeat

transform hj_pov_hand_speed3:
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset store._hj_pov_hand_start
    block:
        ease 0.12 yoffset store._hj_pov_hand_end
        ease 0.10 yoffset store._hj_pov_hand_start
        repeat

# HJ ARM ROTATION (POV overlay)
transform hj_pov_arm_right_speed0():
    subpixel True
    matrixanchor (store._hj_pov_ar_ax, store._hj_pov_ar_ay)
    matrixtransform RotateMatrix(0, 0, store._hj_pov_ar_start)

transform hj_pov_arm_right_speed1():
    subpixel True
    matrixanchor (store._hj_pov_ar_ax, store._hj_pov_ar_ay)
    matrixtransform RotateMatrix(0, 0, store._hj_pov_ar_start)
    block:
        ease 0.50 matrixtransform RotateMatrix(0, 0, store._hj_pov_ar_end)
        ease 0.42 matrixtransform RotateMatrix(0, 0, store._hj_pov_ar_start)
        repeat

transform hj_pov_arm_right_speed2():
    subpixel True
    matrixanchor (store._hj_pov_ar_ax, store._hj_pov_ar_ay)
    matrixtransform RotateMatrix(0, 0, store._hj_pov_ar_start)
    block:
        ease 0.22 matrixtransform RotateMatrix(0, 0, store._hj_pov_ar_end)
        ease 0.18 matrixtransform RotateMatrix(0, 0, store._hj_pov_ar_start)
        repeat

transform hj_pov_arm_right_speed3():
    subpixel True
    matrixanchor (store._hj_pov_ar_ax, store._hj_pov_ar_ay)
    matrixtransform RotateMatrix(0, 0, store._hj_pov_ar_start)
    block:
        ease 0.12 matrixtransform RotateMatrix(0, 0, store._hj_pov_ar_end)
        ease 0.10 matrixtransform RotateMatrix(0, 0, store._hj_pov_ar_start)
        repeat

transform hj_pov_arm_left_speed0():
    subpixel True
    matrixanchor (store._hj_pov_al_ax, store._hj_pov_al_ay)
    matrixtransform RotateMatrix(0, 0, store._hj_pov_al_start)

transform hj_pov_arm_left_speed1():
    subpixel True
    matrixanchor (store._hj_pov_al_ax, store._hj_pov_al_ay)
    matrixtransform RotateMatrix(0, 0, store._hj_pov_al_start)
    block:
        ease 0.50 matrixtransform RotateMatrix(0, 0, store._hj_pov_al_end)
        ease 0.42 matrixtransform RotateMatrix(0, 0, store._hj_pov_al_start)
        repeat

transform hj_pov_arm_left_speed2():
    subpixel True
    matrixanchor (store._hj_pov_al_ax, store._hj_pov_al_ay)
    matrixtransform RotateMatrix(0, 0, store._hj_pov_al_start)
    block:
        ease 0.22 matrixtransform RotateMatrix(0, 0, store._hj_pov_al_end)
        ease 0.18 matrixtransform RotateMatrix(0, 0, store._hj_pov_al_start)
        repeat

transform hj_pov_arm_left_speed3():
    subpixel True
    matrixanchor (store._hj_pov_al_ax, store._hj_pov_al_ay)
    matrixtransform RotateMatrix(0, 0, store._hj_pov_al_start)
    block:
        ease 0.12 matrixtransform RotateMatrix(0, 0, store._hj_pov_al_end)
        ease 0.10 matrixtransform RotateMatrix(0, 0, store._hj_pov_al_start)
        repeat

# -----------------------------
# BODY POSITION (static — no animation)
# -----------------------------
transform hj_center:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.06
    xoffset 40
    zoom 0.65

# -----------------------------
# HANDJOB SLOT — Y-axis bounce only, no rotation
# -----------------------------
transform hj_slot_left_speed0:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageLeft
    yalign 2.0

transform hj_slot_left_speed1:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageLeft
    yalign 2.0
    block:
        ease 0.45 yoffset 12
        ease 0.45 yoffset 0
        repeat

transform hj_slot_left_speed2:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageLeft
    yalign 2.0
    block:
        ease 0.28 yoffset 16
        ease 0.28 yoffset 0
        repeat

transform hj_slot_left_speed3:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageLeft
    yalign 2.0
    block:
        ease 0.15 yoffset 18
        ease 0.15 yoffset 0
        repeat

transform hj_slot_center_speed0:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0

transform hj_slot_center_speed1:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    block:
        ease 0.45 yoffset 12
        ease 0.45 yoffset 0
        repeat

transform hj_slot_center_speed2:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    block:
        ease 0.28 yoffset 16
        ease 0.28 yoffset 0
        repeat

transform hj_slot_center_speed3:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    block:
        ease 0.15 yoffset 18
        ease 0.15 yoffset 0
        repeat

transform hj_slot_right_speed0:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageRight
    yalign 2.0

transform hj_slot_right_speed1:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageRight
    yalign 2.0
    block:
        ease 0.45 yoffset 12
        ease 0.45 yoffset 0
        repeat

transform hj_slot_right_speed2:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageRight
    yalign 2.0
    block:
        ease 0.28 yoffset 16
        ease 0.28 yoffset 0
        repeat

transform hj_slot_right_speed3:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageRight
    yalign 2.0
    block:
        ease 0.15 yoffset 18
        ease 0.15 yoffset 0
        repeat

# -----------------------------
# TENNY HJ SLOT — Y-axis bounce UP (her art is designed for upward motion)
# -----------------------------
transform tenny_hj_slot_left_speed1:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageLeft
    yalign 2.0
    block:
        ease 0.50 yoffset -5
        ease 0.42 yoffset 0
        repeat

transform tenny_hj_slot_left_speed2:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageLeft
    yalign 2.0
    block:
        ease 0.22 yoffset -6
        ease 0.18 yoffset 0
        repeat

transform tenny_hj_slot_left_speed3:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageLeft
    yalign 2.0
    block:
        ease 0.12 yoffset -6
        ease 0.10 yoffset 0
        repeat

transform tenny_hj_slot_center_speed1:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    block:
        ease 0.50 yoffset -5
        ease 0.42 yoffset 0
        repeat

transform tenny_hj_slot_center_speed2:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    block:
        ease 0.22 yoffset -6
        ease 0.18 yoffset 0
        repeat

transform tenny_hj_slot_center_speed3:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    block:
        ease 0.12 yoffset -6
        ease 0.10 yoffset 0
        repeat

transform tenny_hj_slot_right_speed1:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageRight
    yalign 2.0
    block:
        ease 0.50 yoffset -5
        ease 0.42 yoffset 0
        repeat

transform tenny_hj_slot_right_speed2:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageRight
    yalign 2.0
    block:
        ease 0.22 yoffset -6
        ease 0.18 yoffset 0
        repeat

transform tenny_hj_slot_right_speed3:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageRight
    yalign 2.0
    block:
        ease 0.12 yoffset -6
        ease 0.10 yoffset 0
        repeat

# -----------------------------
# HAND MOVEMENT (pure bounce — rotation comes from hj_rotation_speedN)
# -----------------------------
transform hj_hand_speed0():
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 0.92
    xoffset 40
    zoom 0.65

transform hj_hand_speed1(amp=32):
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.02
    xoffset 40
    zoom 0.65
    block:
        ease 0.42 yoffset -amp
        ease 0.42 yoffset 0
        repeat

transform hj_hand_speed2(amp=70):
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.02
    xoffset 40
    zoom 0.65
    block:
        ease 0.20 yoffset -amp
        ease 0.20 yoffset 0
        repeat

# ============================================================
# Apply speed
# ============================================================
label HJ_ApplySpeed(girl, speed=1):

    $ store.hj_speed = speed
    $ hand_img = "%s hj_hand" % girl.gid
    $ penis_img = "%s hj_penis" % girl.gid

    python:
        if store.hiding_face:
            # Force eyes closed in cached attrs
            _hj_update_attrs(girl)
            _closed_attrs = []
            for _a in store._hj_attrs:
                if _a.startswith("eyes_"):
                    _closed_attrs.append("eyes_closed")
                else:
                    _closed_attrs.append(_a)
            _hj_show_sprite(girl, _closed_attrs)
        else:
            _hj_update_attrs(girl)
            _hj_show_sprite(girl)

    python:
        _pov = _gsc(girl.gid, 'pov_overlay', False, pose='handjob')

        # Guy body
        _guy_img = "%s hj_guy" % girl.gid
        if renpy.has_image(_guy_img):
            renpy.show(_guy_img, tag="hj_guy", at_list=[hj_guy_static], zorder=10050 if _pov else 9960)
        else:
            renpy.hide("hj_guy")

        # Hide-face hand
        _hh_img = "%s hj_hide_hand" % girl.gid
        _hh_tag = "%s_hj_hide_hand" % girl.gid
        if store.hiding_face and renpy.has_image(_hh_img):
            renpy.show(_hh_img, tag=_hh_tag, at_list=[hj_get_slot_transform(speed)], zorder=10000)
        else:
            renpy.hide(_hh_tag)

        _palm_img = "%s hj_palm" % girl.gid
        _thumb_img = "%s hj_thumb" % girl.gid

    if _pov:
        # POV overlay: full scale, no zoom — guy(10050) < arms(10052/10053) < penis(10055) < hands(10060)
        hide hj_palm
        hide hj_thumb

        python:
            _hj_arm_left = "%s hj_arm_left" % girl.gid
            _hj_arm_right = "%s hj_arm_right" % girl.gid
            _arm_left_map = {0: hj_pov_arm_left_speed0, 1: hj_pov_arm_left_speed1, 2: hj_pov_arm_left_speed2, 3: hj_pov_arm_left_speed3}
            _arm_right_map = {0: hj_pov_arm_right_speed0, 1: hj_pov_arm_right_speed1, 2: hj_pov_arm_right_speed2, 3: hj_pov_arm_right_speed3}
            _arm_speed = min(speed, 3)

            if renpy.has_image(_hj_arm_left):
                _at_l = [hj_get_slot_transform(speed), _arm_left_map[_arm_speed]()]
                renpy.show(_hj_arm_left, tag="%s_hj_arm_left" % girl.gid, at_list=_at_l, zorder=10052)
            if renpy.has_image(_hj_arm_right):
                _at_r = [hj_get_slot_transform(speed), _arm_right_map[_arm_speed]()]
                renpy.show(_hj_arm_right, tag="%s_hj_arm_right" % girl.gid, at_list=_at_r, zorder=10053)

            if not renpy.has_image(_hj_arm_left) and not renpy.has_image(_hj_arm_right):
                _arm_img = "%s hj_arm_overlay" % girl.gid
                if renpy.has_image(_arm_img):
                    renpy.show(_arm_img, tag="%s_hj_arm_overlay" % girl.gid, at_list=[hj_get_slot_transform(speed)], zorder=10053)

        show expression penis_img as hj_penis at hj_guy_static zorder 10055
        $ _hj_hand_t = hj_hand_transform(speed, True)
        show expression hand_img as hj_hand at _hj_hand_t zorder 10060

    elif speed == 0:
        # Palm behind penis, thumb above, hand static
        if renpy.has_image(_palm_img):
            show expression _palm_img as hj_palm at hj_center zorder 9985
        show expression penis_img as hj_penis at hj_center zorder 9990
        if renpy.has_image(_thumb_img):
            show expression _thumb_img as hj_thumb at hj_center zorder 9995
        show expression hand_img as hj_hand at hj_hand_speed0 zorder 9998
    else:
        # Normal speed: hand animates, hide palm/thumb
        hide hj_palm
        hide hj_thumb
        show expression penis_img as hj_penis at hj_center zorder 9990
        if speed == 1:
            show expression hand_img as hj_hand at hj_hand_speed1 zorder 9995
        else:
            show expression hand_img as hj_hand at hj_hand_speed2 zorder 9995

    # Re-show standalone cum layers at current speed transform
    python:
        _hj_slot_tf = hj_get_slot_transform(speed)
        for _suffix, _z_normal, _z_pov in [("hj_cum_face", 10002, 10057), ("hj_cum_mouth", 10003, 10058)]:
            _hj_cum_img = "%s %s" % (girl.gid, _suffix)
            _hj_cum_z = _z_pov if _pov else _z_normal
            if renpy.has_image(_hj_cum_img):
                renpy.show(_hj_cum_img, tag="%s_%s" % (girl.gid, _suffix), at_list=[_hj_slot_tf], zorder=_hj_cum_z)
        hj_show_hand_cum(girl, speed, _pov)

    return

# ============================================================
# Launch
# ============================================================
label HJ_Launch(girl):
    $ sub_event_reset(girl)
    $ debug_log("[DEBUG] HJ_Launch: entered")
    $ _kill_scene_threads()
    $ stop_standing_blink(girl)

    $ public_attention_reset()

    $ girl._prev_pose = getattr(girl, "default_pose", "standing")
    $ girl._prev_slot = getattr(girl, "SpriteLoc", StageCenter)
    if not getattr(girl, "_saved_outfit", None):
        $ girl.SaveOutfit()

    # Set _hj_girl BEFORE ApplySpeed so sprite system knows we're in HJ
    python:
        _hide_all_scene_layers(girl)
        store._hj_girl = girl
        store.hiding_face = False
        store._hj_face_ordered_shown = False
        if girl._prev_slot == StageLeft:
            store._hj_slot_transform = "left"
        elif girl._prev_slot == StageRight:
            store._hj_slot_transform = "right"
        else:
            store._hj_slot_transform = "center"

    $ store._slap_count = 0

    if "hj_speed" not in globals():
        $ hj_speed = 1

    # Show full HJ sprite (body + penis + hand) at speed 0 BEFORE the exposure line
    call HJ_ApplySpeed(girl, 0) from _call_HJ_ApplySpeed

    with fade

    # Girl reacts to seeing the penis — sprite is fully visible now
    call PlayerExposure(girl) from _call_PlayerExposure_3

    # Resume at normal speed + start background threads
    call HJ_ApplySpeed(girl, hj_speed) from _call_HJ_ApplySpeed_resume

    python:
        renpy.invoke_in_thread(_scene_blink_loop, girl, "_hj_girl", "hj_blink")
        renpy.invoke_in_thread(_hj_expression_cycle, girl)
    return

# ============================================================
# Control Menu
# ============================================================
label HJ_ControlMenu(girl):
    $ debug_log("[DEBUG] HJ_ControlMenu: entered")
    $ store._player_exhausted = False
    if "hj_speed" not in globals():
        $ hj_speed = 1

    while True:

        if _scene_should_exit():
            return

        if Round >= 100:
            $ Say_Line(girl, _scene_time_up_line())
            call HJ_End(girl, dress_up=False) from _call_HJ_End_timeout
            return

        menu:
            "Speed up" if hj_speed < 2:
                $ advance_round(TIME_COSTS["sex_tick"])
                $ Say_Player(_("Faster..."))
                $ hj_speed += 1
                call HJ_ApplySpeed(girl, hj_speed) from _call_HJ_ApplySpeed_1
                $ add_player_focus(get_player_lust_gain("hj", hj_speed))
                # Girl lust: only if she has high existing Lust (>= 70) — she shouldn't orgasm just from giving a HJ
                if girl.Lust >= 70:
                    $ _girl_lust_gain(girl, 1, hj_speed)
                $ _moan = scene_moan_tick(girl, "hj", hj_speed)
                if _moan:
                    call _moan_say(girl, _moan) from _call_ms_hj_su
                # Public attention
                $ _pa_caught = public_attention_tick(girl, "speed_up", hj_speed)
                if _pa_caught:
                    if not _caught_keeps_going(girl):
                        call HJ_End(girl, dress_up=False) from _call_HJ_End_pa
                    call caught_in_public(girl, "hj") from _call_caught_public_hj_su
                    return
                if girl.Lust >= 100:
                    call GirlCumming(girl, "hj", "handjob") from _call_GirlCumming_11
                if player_is_cumming():
                    if focus_overdue_tick():
                        call ForcedCumOverdue(girl, "hj") from _call_ForcedCumOverdue_hj_su
                        $ _handle_post_cum_exit("hj", "sex")
                        return
                $ set_scene_expression(girl, None, eyes="eyes_squint_big", mouth="mouth_smile", pose="handjob")
                $ Narration(_("She speeds up her hand."))

            "Keep going" if hj_speed in (1, 2):
                $ advance_round(TIME_COSTS["sex_tick"])
                $ add_player_focus(get_player_lust_gain("hj", hj_speed))
                # Girl lust: only if she has high existing Lust (>= 70) — she shouldn't orgasm just from giving a HJ
                if girl.Lust >= 70:
                    $ _girl_lust_gain(girl, 1, hj_speed)
                $ _moan = scene_moan_tick(girl, "hj", hj_speed)
                if _moan:
                    call _moan_say(girl, _moan) from _call_ms_hj_kg

                # Public attention
                $ _pa_caught = public_attention_tick(girl, "keep_going", hj_speed)
                if _pa_caught:
                    if not _caught_keeps_going(girl):
                        call HJ_End(girl, dress_up=False) from _call_HJ_End_pa2
                    call caught_in_public(girl, "hj") from _call_caught_public_hj_kg
                    return

                # Random interruption check
                call _sex_interruption_check(girl, "hj") from _call__sex_interruption_check_3
                $ store._witness_expression_lock = False
                if store._sex_interrupted:
                    call HJ_End(girl, dress_up=False) from _call_HJ_End_1
                    return

                call _npc_partner_detection_tick(girl, "hj") from _call_npc_detect_hj
                if store._npc_witness_scene_aborted:
                    call HJ_End(girl, dress_up=False) from _call_HJ_End_npc
                    return

                call _sub_event_tick_nonpen(girl, "hj") from _call_se_np_hj
                if store._sst_result == "abort":
                    call HJ_End(girl, dress_up=False) from _call_HJ_End_se
                    return

                if girl.Lust >= 100:
                    call GirlCumming(girl, "hj", "handjob") from _call_GirlCumming_12
                if player_is_cumming():
                    if focus_overdue_tick():
                        call ForcedCumOverdue(girl, "hj") from _call_ForcedCumOverdue_hj_kg
                        $ _handle_post_cum_exit("hj", "sex")
                        return
                $ Narration(_("She keeps the pace."))

            "Slow down" if hj_speed > 0:
                $ advance_round(1)
                $ hj_speed -= 1
                call HJ_ApplySpeed(girl, hj_speed) from _call_HJ_ApplySpeed_2
                $ add_player_focus(10 if hj_speed == 1 else 20 if hj_speed == 2 else 0)
                $ set_scene_expression(girl, None, eyes="eyes_normal", mouth="mouth_smile", pose="handjob")
                $ Narration(_("She slows her movements."))

            "Slap her" if hj_speed >= 1 and not hiding_face:
                $ advance_round(1)
                call SexScene_Slap(girl, "hj") from _call_SexScene_Slap_hj

            "Tease her..." if hj_speed > 0:
                $ advance_round(1)
                call _tease_menu(girl, "hj") from _call_tease_menu_hj

            "Strip her":
                $ advance_round(1)
                call HJ_StripMenu(girl) from _call_HJ_StripMenu

            "Record Options..." if (not getattr(store, "_recording_active", False) or getattr(store, "_recording_girl", None) == girl):
                menu:
                    "Record her" if not getattr(store, "_recording_active", False):
                        call _sex_phone_menu(girl, "hj") from _call__sex_phone_menu_5
                    "Ask [store._ntr_watching_npc.Name] to record" if store._ntr_partner_watching and not getattr(store, "_recording_active", False):
                        call _watcher_record_start(girl, "hj") from _call_watcher_rec_start_hj_npc
                    "Ask [store._witness_girl.Name] to record" if getattr(store, "_witness_watching", False) and getattr(store, "_witness_girl", None) is not None and not store._ntr_partner_watching and not getattr(store, "_recording_active", False):
                        call _watcher_record_start(girl, "hj") from _call_watcher_rec_start_hj_girl
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
                        $ store._hj_face_ordered_shown = True
                        $ Narration(_("You tell her to show her face."))
                    "Back":
                        pass
                call HJ_ApplySpeed(girl, hj_speed) from _call_HJ_ApplySpeed_rec_opts

            "{color=#fbbf24}Cum{/color}" if player_is_cumming():
                call PlayerCumMenu(girl, "hj") from _call_PlayerCumMenu_voluntary_hj
                $ _handle_post_cum_exit("hj", "sex")
                return

            "Stop now":
                if store._forced_creampie_end_after_orgasm:
                    call _player_stops_after_forced_creampie(girl, "hj") from _call__player_stops_forced_hj
                else:
                    call _scene_stop_reaction(girl) from _call_scene_stop_reaction_hj
                    if store._stop_accepted:
                        call HJ_End(girl, dress_up=False) from _call_HJ_End_3
                        return

label HJ_StripMenu(girl):
    while True:
        $ _legs_label = _("Remove pants") if _strip_name_for_slot(girl, "skirt") == "pants" else _("Remove skirt")
        menu:
            "Remove top" if girl.Over:
                call _strip_approval(girl, ["over"]) from _call__strip_approval_24
                if store._strip_approved:
                    $ girl.Outfit_Change(over="none", pose="handjob")
                    call HJ_ApplySpeed(girl, hj_speed) from _call_HJ_ApplySpeed_3
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_22

            "Remove shirt" if girl.Mid:
                call _strip_approval(girl, ["mid"]) from _call__strip_approval_hj_mid
                if store._strip_approved:
                    $ girl.Outfit_Change(mid="none", pose="handjob")
                    call HJ_ApplySpeed(girl, hj_speed) from _call_HJ_ApplySpeed_mid
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_hj_mid

            "Remove chest" if girl.Chest:
                call _strip_approval(girl, ["chest"]) from _call__strip_approval_25b
                if store._strip_approved:
                    $ girl.Outfit_Change(chest="none", pose="handjob")
                    call HJ_ApplySpeed(girl, hj_speed) from _call_HJ_ApplySpeed_4b
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_23b

            "[_legs_label]" if girl.Legs and _slot_renderable(girl, "skirt", "handjob"):
                call _strip_approval(girl, ["legs"]) from _call__strip_approval_26
                if store._strip_approved:
                    $ girl.Outfit_Change(legs="none", pose="handjob")
                    call HJ_ApplySpeed(girl, hj_speed) from _call_HJ_ApplySpeed_5
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_24

            "Remove panties" if girl.Panties and _slot_renderable(girl, "panties", "handjob"):
                call _strip_approval(girl, ["panties"]) from _call__strip_approval_27
                if store._strip_approved:
                    $ girl.Outfit_Change(panties="none", pose="handjob")
                    if girl.Legs:
                        # with her pants/skirt still on, the change shows nothing (tester 2026-10-11
                        # read it as a bug): a line says it happened
                        $ _hj_pan_word = _tl(_("pants")) if _strip_name_for_slot(girl, "skirt") == "pants" else _tl(_("skirt"))
                        $ Narration(_tl_fmt(_("She works them off from under her %s. You'll have to take her word for it."), _hj_pan_word))
                    call HJ_ApplySpeed(girl, hj_speed) from _call_HJ_ApplySpeed_6
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_25

            "Remove shoes" if getattr(girl, "Shoes", None) and _slot_renderable(girl, "shoes", "handjob"):
                $ girl.Outfit_Change(shoes="none", pose="handjob")
                call HJ_ApplySpeed(girl, hj_speed) from _call_HJ_ApplySpeed_7

            "Remove collar" if getattr(girl, "Collar", False) and girl.has_collar_art():
                $ girl.SetCollar(False, pose="handjob")
                call HJ_ApplySpeed(girl, hj_speed) from _call_HJ_ApplySpeed_8

            "Back":
                return

# ============================================================
# End
# ============================================================
# ============================================================
# HJ Cum Animation — penis pulse + screen shakes
# ============================================================
transform hj_penis_cum_pulse():
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.06
    xoffset 40
    zoom 0.65
    yzoom 1.0
    pause 0.45
    ease 0.08 yzoom 1.06
    ease 0.15 yzoom 1.0
    pause 0.27
    ease 0.08 yzoom 1.06
    ease 0.15 yzoom 1.0

label HJ_CumAnim(girl):
    python:
        _pov_cum = _gsc(girl.gid, 'pov_overlay', False, pose='handjob')
        _cum_z = 10055 if _pov_cum else 9990
        _penis_img = "%s hj_penis" % girl.gid
        print("[HJ_CUM_ANIM] gid=%s pov=%s z=%s" % (girl.gid, _pov_cum, _cum_z))
        _apply_cum_expression(girl, "handjob", "outside")
        _hj_update_attrs(girl)
        _hj_show_sprite(girl)

    # Penis pulse (centralized getter: per-girl HJ → BJ shared → generic)
    $ renpy.show(_penis_img, tag="hj_penis", at_list=[_hj_get_penis_cum_tf(girl)], zorder=_cum_z)

    call _cum_punch_pair("oral") from _call_cum_punch_hj_cum

    # Restore penis (centralized getter: per-girl HJ → BJ shared → generic)
    $ renpy.show(_penis_img, tag="hj_penis", at_list=[_hj_get_penis_tf(girl)], zorder=_cum_z)

    return

label HJ_End(girl, dress_up=True):
    $ debug_log("[DEBUG] HJ_End: entered, dress_up=%s" % str(dress_up))
    $ scene_full_cleanup(girl)
    $ finalize_recording()
    $ _player_cleanup(girl)
    $ store._hj_girl = None
    hide hj_penis
    hide hj_hand
    hide hj_palm
    hide hj_thumb
    hide hj_guy
    $ renpy.hide("%s_hj_arm_overlay" % girl.gid)
    $ renpy.hide("%s_hj_arm_left" % girl.gid)
    $ renpy.hide("%s_hj_arm_right" % girl.gid)
    $ renpy.hide("%s_hj_hide_hand" % girl.gid)
    $ renpy.hide("%s_hj_cum_face" % girl.gid)
    $ renpy.hide("%s_hj_cum_mouth" % girl.gid)
    $ renpy.hide("%s_hj_cum_hand" % girl.gid)

    $ pose = getattr(girl, "_prev_pose", "standing")
    $ slot = _safe_restore_slot(getattr(girl, "_prev_slot", StageCenter))

    python:
        slot_transform = _slot_to_transform(slot)
        _reset_expression_state(girl)
        store.hiding_face = False
        store._hj_slot_transform = None
        store.hj_blink = False
        girl.ResetVisuals(pose=pose, at_list=[slot_transform])

    if dress_up:
        call DressUp_Sequence(girl) from _call_DressUp_Sequence_5
    $ debug_log("[DEBUG] HJ_End: returning")
    return

# ============================================================
# Player climax placeholder
# (removed)
# ============================================================
