# ============================================================
# CORE FULL NELSON SYSTEM
# ============================================================
# Front-facing, held up by the player. Available for NTW and Tenny.
# Girl bounces as a unit (slot transform), penis thrusts independently.
# Supports both vaginal and anal modes.

image fn_condom = "images/characters/Player/FN Condom.png"
image fn_condom_broken = "images/characters/Player/Broken FN Condom.png"

default fn_speed = 0
default fn_started = False
default fn_anal = False
default _fn_girl = None
default fn_blink = False
default _fn_tripod_result = None
default _fn_scene_type = "full_nelson"   # every FN menu assigns it at entry; safety net for old saves

init python:
    _FN_CHEST_UP_MAPS = {
        "ntw": {
            "yellow_top_up": ("yellow_top_none", preg_art("ntw", "Full Nelson/Clothes/Yellow Top Up.png")),
            "bikini_top_up": ("bikini_top_none", preg_art("ntw", "Full Nelson/Clothes/Bikini/Bikini Top Up.png")),
        },
        "tenny": {
            "white_top_up": ("white_top_none", preg_art("tenny", "Full Nelson/Clothes/White Top/White Top Up.png")),
            "bikini_top_up": ("bikini_top_none", preg_art("tenny", "Full Nelson/Clothes/Bikini/Bikini Top Up.png")),
        },
    }

    # -----------------------------
    # FN BLINK + EXPRESSION CYCLE
    # -----------------------------
    _FN_EYES_BY_SPEED = {
        0: ["eyes_normal", "eyes_side", "eyes_away"],
        1: ["eyes_normal", "eyes_squint", "eyes_closed_happy"],
        2: ["eyes_squint", "eyes_bliss", "eyes_closed_left", "eyes_up"],
        3: ["eyes_bliss", "eyes_ahegao", "eyes_up", "eyes_surprised"],
    }
    _FN_BROWS_BY_SPEED = {
        0: ["brows_normal"],
        1: ["brows_normal", "brows_surprised"],
        2: ["brows_surprised", "brows_scared"],
        3: ["brows_scared", "brows_horny"],
    }
    _FN_MOUTH_BY_SPEED = {
        0: ["mouth_normal", "mouth_angry"],
        1: ["mouth_normal", "mouth_moaning", "mouth_lipbite"],
        2: ["mouth_moaning", "mouth_moaning_2", "mouth_surprised"],
        3: ["mouth_moaning_2", "mouth_moaning_3", "mouth_screaming"],
    }

    # Anal/penetration: force panties attrs to none (strip from layeredimage)
    _FN_PANTIES_STRIP = {
        "yellow_bottom_on": "yellow_bottom_none",
        "bikini_bottom_on": "bikini_bottom_none",
        "striped_bottom_on": "striped_bottom_none",
    }

    _FN_CLOTHING_GROUPS = {
        "ntw": {
            "yellow_top": "yellow_top_none",
            "yellow_bottom": "yellow_bottom_none",
            "bikini_top": "bikini_top_none",
            "bikini_bottom": "bikini_bottom_none",
        },
        "tenny": {
            "white_top": "white_top_none",
            "striped_bottom": "striped_bottom_none",
            "bikini_top": "bikini_top_none",
            "bikini_bottom": "bikini_bottom_none",
        },
    }

    _FN_ANAL_EYES = {
        "anal_lover": {
            0: ["eyes_normal", "eyes_side", "eyes_away"],
            1: ["eyes_squint", "eyes_closed_happy", "eyes_bliss"],
            2: ["eyes_bliss", "eyes_squint", "eyes_up"],
            3: ["eyes_bliss", "eyes_ahegao", "eyes_ahegao_2", "eyes_up"],
        },
        "anal_hater": {
            0: ["eyes_squint", "eyes_side", "eyes_away"],
            1: ["eyes_squint", "eyes_surprised", "eyes_closed"],
            2: ["eyes_surprised", "eyes_closed_left", "eyes_up"],
            3: ["eyes_surprised", "eyes_up", "eyes_closed"],
        },
        "default": {
            0: ["eyes_normal", "eyes_side", "eyes_away"],
            1: ["eyes_squint", "eyes_closed_left", "eyes_side"],
            2: ["eyes_squint", "eyes_surprised", "eyes_up"],
            3: ["eyes_surprised", "eyes_up", "eyes_squint"],
        },
    }
    _FN_ANAL_BROWS = {
        "anal_lover": {
            0: ["brows_normal"],
            1: ["brows_normal", "brows_surprised"],
            2: ["brows_surprised", "brows_horny"],
            3: ["brows_horny", "brows_scared"],
        },
        "anal_hater": {
            0: ["brows_scared"],
            1: ["brows_scared", "brows_sad"],
            2: ["brows_scared", "brows_sad"],
            3: ["brows_scared", "brows_sad"],
        },
        "default": {
            0: ["brows_normal"],
            1: ["brows_surprised", "brows_scared"],
            2: ["brows_scared", "brows_surprised"],
            3: ["brows_scared", "brows_sad"],
        },
    }
    _FN_ANAL_MOUTH = {
        "anal_lover": {
            0: ["mouth_normal", "mouth_moaning"],
            1: ["mouth_moaning", "mouth_lipbite"],
            2: ["mouth_moaning", "mouth_moaning_2", "mouth_lipbite"],
            3: ["mouth_moaning_2", "mouth_moaning_3", "mouth_screaming"],
        },
        "anal_hater": {
            0: ["mouth_scared", "mouth_angry"],
            1: ["mouth_scared", "mouth_moaning"],
            2: ["mouth_screaming", "mouth_moaning_2", "mouth_scared"],
            3: ["mouth_screaming", "mouth_moaning_3", "mouth_scared"],
        },
        "default": {
            0: ["mouth_normal", "mouth_angry"],
            1: ["mouth_moaning", "mouth_surprised"],
            2: ["mouth_moaning_2", "mouth_screaming", "mouth_surprised"],
            3: ["mouth_screaming", "mouth_moaning_3", "mouth_moaning_2"],
        },
    }

    def _fn_effect_frame_anim(st, at, folder, prefix):
        n_frames = 31
        frame_dur = 0.083
        cycle_pos = int(st / frame_dur) % n_frames
        frame = cycle_pos + 1
        path = "images/characters/Tenny/Full Nelson/Effects/%s/%s %d.png" % (folder, prefix, frame)
        if frame == 1 and cycle_pos == 0:
            print("[FN_EFFECT_ANIM] folder=%s prefix=%s path=%s" % (folder, prefix, path))
        d = renpy.displayable(path)
        return d, frame_dur - (st % frame_dur)

    def _fn_is_active(girl):
        if store._fn_girl is not girl:
            return False
        if store._doggy_girl is girl or store._cowgirl_girl is girl or store._rcg_girl is girl:
            return False
        return True

    def _fn_pool_override(girl, speed, eyes_pool, brows_pool, mouth_pool):
        if not getattr(store, "fn_anal", False):
            return (eyes_pool, brows_pool, mouth_pool)
        if girl.has_trait("anal_lover"):
            key = "anal_lover"
        elif girl.has_trait("anal_hater"):
            key = "anal_hater"
        else:
            key = "default"
        return (
            _FN_ANAL_EYES[key].get(speed, eyes_pool),
            _FN_ANAL_BROWS[key].get(speed, brows_pool),
            _FN_ANAL_MOUTH[key].get(speed, mouth_pool),
        )

    def _fn_expression_cycle(girl):
        _scene_expression_cycle(girl, "_fn_girl", "fn_speed",
            _FN_EYES_BY_SPEED, _FN_BROWS_BY_SPEED, _FN_MOUTH_BY_SPEED,
            is_active_fn=_fn_is_active, cs_girls={"ntw", "tenny"},
            pool_override_fn=_fn_pool_override)

    # -----------------------------
    # SLOT TRANSFORM (BODY BOUNCE)
    # -----------------------------
    def fn_get_slot_transform(speed, anal=False):
        if getattr(store, "fn_tip_mode", False) and not anal and speed >= 1:
            return fnv_slot_tip
        if anal:
            slot_map = {0: fn_slot_speed0, 1: fn_slot_speed1, 2: fn_slot_speed2, 3: fn_slot_speed3, 4: fn_slot_speed4}
        else:
            slot_map = {0: fnv_slot_speed0, 1: fnv_slot_speed1, 2: fnv_slot_speed2, 3: fnv_slot_speed3, 4: fnv_slot_speed4}
        return slot_map.get(speed, slot_map[1])

    def fn_get_penis_transform(speed, anal=False):
        # Speed 0 is ALWAYS static (post-cum freeze, edge denial, hole switch,
        # pre-penetration idle). Anything that "moves with the penis" (legs,
        # cum_penis, scrotum) must go through here so it freezes together.
        if speed <= 0:
            return fn_penis_cum_hold if store.fn_started else fn_penis_speed0
        if getattr(store, "fn_tip_mode", False) and not anal:
            return fn_penis_tip
        if anal:
            p_map = {1: fna_penis_speed1, 2: fna_penis_speed2, 3: fna_penis_speed3, 4: fna_penis_speed4}
        else:
            p_map = {1: fn_penis_speed1, 2: fn_penis_speed2, 3: fn_penis_speed3, 4: fn_penis_speed4}
        return p_map.get(speed, p_map[1])

    def fn_get_chest_transform(speed, anal=False, covered=False):
        if covered:
            c_map = {0: fn_chest_covered_speed0, 1: fn_chest_covered_speed1, 2: fn_chest_covered_speed2, 3: fn_chest_covered_speed3, 4: fn_chest_covered_speed4}
        elif anal:
            c_map = {0: fna_chest_speed0, 1: fna_chest_speed1, 2: fna_chest_speed2, 3: fna_chest_speed3, 4: fna_chest_speed4}
        else:
            c_map = {0: fn_chest_speed0, 1: fn_chest_speed1, 2: fn_chest_speed2, 3: fn_chest_speed3, 4: fn_chest_speed4}
        return c_map.get(speed, c_map[1])

    def fn_get_nipple_transform(speed, anal=False):
        if anal:
            n_map = {0: fna_nipple_speed0, 1: fna_nipple_speed1, 2: fna_nipple_speed2, 3: fna_nipple_speed3, 4: fna_nipple_speed4}
        else:
            n_map = {0: fn_nipple_speed0, 1: fn_nipple_speed1, 2: fn_nipple_speed2, 3: fn_nipple_speed3, 4: fn_nipple_speed4}
        return n_map.get(speed, n_map[1])

    def fn_get_head_transform(speed):
        h_map = {0: fn_head_speed0, 1: fn_head_speed1, 2: fn_head_speed2, 3: fn_head_speed3, 4: fn_head_speed4}
        return h_map.get(speed, h_map[1])

    def fn_get_arm_left_transform(speed):
        a_map = {0: fn_arm_left_speed0, 1: fn_arm_left_speed1, 2: fn_arm_left_speed2, 3: fn_arm_left_speed3, 4: fn_arm_left_speed4}
        return a_map.get(speed, a_map[1])

    def fn_get_arm_right_transform(speed):
        a_map = {0: fn_arm_right_speed0, 1: fn_arm_right_speed1, 2: fn_arm_right_speed2, 3: fn_arm_right_speed3, 4: fn_arm_right_speed4}
        return a_map.get(speed, a_map[1])

    def fn_get_scrotum_transform(speed):
        s_map = {0: fn_scrotum_speed0, 1: fn_scrotum_speed1, 2: fn_scrotum_speed2, 3: fn_scrotum_speed3, 4: fn_scrotum_speed4}
        return s_map.get(speed, s_map[1])

    def fn_get_shin_left_transform(speed):
        s_map = {0: fn_shin_left_speed0, 1: fn_shin_left_speed1, 2: fn_shin_left_speed2, 3: fn_shin_left_speed3, 4: fn_shin_left_speed4}
        return s_map.get(speed, s_map[1])

    def fn_get_shin_right_transform(speed):
        s_map = {0: fn_shin_right_speed0, 1: fn_shin_right_speed1, 2: fn_shin_right_speed2, 3: fn_shin_right_speed3, 4: fn_shin_right_speed4}
        return s_map.get(speed, s_map[1])


# ============================================================
# SLOT TRANSFORMS (character bounce — whole body)
# ============================================================
transform fn_slot_speed0:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 0

transform fn_slot_speed1:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 0
    block:
        ease 0.40 yoffset -15
        ease 0.40 yoffset 15
        ease 0.40 yoffset 0
        repeat

transform fn_slot_speed2:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 0
    block:
        ease 0.26 yoffset -20
        ease 0.26 yoffset 20
        easein 0.28 yoffset 0
        repeat

transform fn_slot_speed3:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 0
    block:
        ease 0.13 yoffset -28
        ease 0.13 yoffset 28
        easein 0.14 yoffset 0
        repeat

transform fn_slot_speed4:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 0
    block:
        ease 0.08 yoffset -10
        ease 0.08 yoffset 10
        easein 0.08 yoffset 0
        repeat


# ============================================================
# SLOT TRANSFORMS — VAGINAL (girl drops lower on the bounce)
# ============================================================
transform fnv_slot_speed0:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 50

transform fnv_slot_speed1:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 30
    block:
        ease 0.40 yoffset 0
        ease 0.40 yoffset 80
        ease 0.40 yoffset 50
        repeat

transform fnv_slot_speed2:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 50
    block:
        ease 0.26 yoffset 0
        ease 0.26 yoffset 100
        easein 0.28 yoffset 50
        repeat

transform fnv_slot_speed3:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 50
    block:
        ease 0.13 yoffset -10
        ease 0.13 yoffset 120
        easein 0.14 yoffset 50
        repeat

transform fnv_slot_speed4:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 50
    block:
        ease 0.08 yoffset 0
        ease 0.08 yoffset 22
        easein 0.08 yoffset 10
        repeat

transform fnv_slot_tip:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 40
    block:
        ease 0.50 yoffset 20
        ease 0.50 yoffset 60
        ease 0.50 yoffset 40
        repeat


# ============================================================
# CHEST BOUNCE TRANSFORMS (small zoom pulse per speed)
# ============================================================
transform fn_chest_speed0:
    subpixel True
    zoom 1.0

transform fn_chest_speed1:
    subpixel True
    zoom 1.0
    block:
        ease 0.40 zoom 1.008 yoffset -2
        ease 0.40 zoom 1.0 yoffset 2
        ease 0.40 zoom 1.0 yoffset 0
        repeat

transform fn_chest_speed2:
    subpixel True
    zoom 1.0
    block:
        ease 0.26 zoom 1.012 yoffset -3
        ease 0.26 zoom 1.0 yoffset 3
        easein 0.28 zoom 1.0 yoffset 0
        repeat

transform fn_chest_speed3:
    subpixel True
    zoom 1.0
    block:
        ease 0.13 zoom 1.018 yoffset -5
        ease 0.13 zoom 1.0 yoffset 5
        easein 0.14 zoom 1.0 yoffset 0
        repeat

transform fn_chest_speed4:
    subpixel True
    zoom 1.0
    block:
        ease 0.08 zoom 1.010 yoffset -3
        ease 0.08 zoom 1.0 yoffset 3
        easein 0.08 zoom 1.0 yoffset 0
        repeat


# ============================================================
# CHEST BOUNCE (REDUCED) — when chest clothing is "up", less movement
# ============================================================
transform fn_chest_covered_speed0:
    subpixel True
    zoom 1.0

transform fn_chest_covered_speed1:
    subpixel True
    zoom 1.0
    block:
        ease 0.40 zoom 1.004 yoffset -1
        ease 0.40 zoom 1.0 yoffset 1
        ease 0.40 zoom 1.0 yoffset 0
        repeat

transform fn_chest_covered_speed2:
    subpixel True
    zoom 1.0
    block:
        ease 0.26 zoom 1.006 yoffset -1
        ease 0.26 zoom 1.0 yoffset 1
        easein 0.28 zoom 1.0 yoffset 0
        repeat

transform fn_chest_covered_speed3:
    subpixel True
    zoom 1.0
    block:
        ease 0.13 zoom 1.009 yoffset -2
        ease 0.13 zoom 1.0 yoffset 2
        easein 0.14 zoom 1.0 yoffset 0
        repeat

transform fn_chest_covered_speed4:
    subpixel True
    zoom 1.0
    block:
        ease 0.08 zoom 1.005 yoffset -1
        ease 0.08 zoom 1.0 yoffset 1
        easein 0.08 zoom 1.0 yoffset 0
        repeat

# ============================================================
# NIPPLE BOUNCE TRANSFORMS (larger movement than chest)
# ============================================================
transform fn_nipple_speed0:
    subpixel True
    yoffset 0

transform fn_nipple_speed1:
    subpixel True
    yoffset 0
    block:
        ease 0.40 yoffset -5
        ease 0.40 yoffset 5
        ease 0.40 yoffset 0
        repeat

transform fn_nipple_speed2:
    subpixel True
    yoffset 0
    block:
        ease 0.26 yoffset -8
        ease 0.26 yoffset 8
        easein 0.28 yoffset 0
        repeat

transform fn_nipple_speed3:
    subpixel True
    yoffset 0
    block:
        ease 0.13 yoffset -12
        ease 0.13 yoffset 12
        easein 0.14 yoffset 0
        repeat

transform fn_nipple_speed4:
    subpixel True
    yoffset 0
    block:
        ease 0.08 yoffset -7
        ease 0.08 yoffset 7
        easein 0.08 yoffset 0
        repeat


# ============================================================
# CHEST BOUNCE TRANSFORMS — ANAL (reduced movement)
# ============================================================
transform fna_chest_speed0:
    subpixel True
    zoom 1.0

transform fna_chest_speed1:
    subpixel True
    zoom 1.0
    block:
        ease 0.40 zoom 1.004 yoffset -1
        ease 0.40 zoom 1.0 yoffset 1
        ease 0.40 zoom 1.0 yoffset 0
        repeat

transform fna_chest_speed2:
    subpixel True
    zoom 1.0
    block:
        ease 0.26 zoom 1.006 yoffset -2
        ease 0.26 zoom 1.0 yoffset 2
        easein 0.28 zoom 1.0 yoffset 0
        repeat

transform fna_chest_speed3:
    subpixel True
    zoom 1.0
    block:
        ease 0.13 zoom 1.009 yoffset -3
        ease 0.13 zoom 1.0 yoffset 3
        easein 0.14 zoom 1.0 yoffset 0
        repeat

transform fna_chest_speed4:
    subpixel True
    zoom 1.0
    block:
        ease 0.08 zoom 1.005 yoffset -2
        ease 0.08 zoom 1.0 yoffset 2
        easein 0.08 zoom 1.0 yoffset 0
        repeat


# ============================================================
# NIPPLE BOUNCE TRANSFORMS — ANAL (reduced movement)
# ============================================================
transform fna_nipple_speed0:
    subpixel True
    yoffset 0

transform fna_nipple_speed1:
    subpixel True
    yoffset 0
    block:
        ease 0.40 yoffset -3
        ease 0.40 yoffset 3
        ease 0.40 yoffset 0
        repeat

transform fna_nipple_speed2:
    subpixel True
    yoffset 0
    block:
        ease 0.26 yoffset -4
        ease 0.26 yoffset 4
        easein 0.28 yoffset 0
        repeat

transform fna_nipple_speed3:
    subpixel True
    yoffset 0
    block:
        ease 0.13 yoffset -6
        ease 0.13 yoffset 6
        easein 0.14 yoffset 0
        repeat

transform fna_nipple_speed4:
    subpixel True
    yoffset 0
    block:
        ease 0.08 yoffset -4
        ease 0.08 yoffset 4
        easein 0.08 yoffset 0
        repeat


# ============================================================
# HEAD ROTATION TRANSFORMS — pivot at neck anchor (1325, 339)
# ============================================================
transform fn_head_speed0:
    subpixel True
    matrixanchor (1325, 339)
    matrixtransform RotateMatrix(0, 0, 0)

transform fn_head_speed1:
    subpixel True
    matrixanchor (1325, 339)
    matrixtransform RotateMatrix(0, 0, 0)
    block:
        ease 0.40 matrixtransform RotateMatrix(0, 0, 1.0)
        ease 0.40 matrixtransform RotateMatrix(0, 0, -1.0)
        ease 0.40 matrixtransform RotateMatrix(0, 0, 0)
        repeat

transform fn_head_speed2:
    subpixel True
    matrixanchor (1325, 339)
    matrixtransform RotateMatrix(0, 0, 0)
    block:
        ease 0.26 matrixtransform RotateMatrix(0, 0, 1.5)
        ease 0.26 matrixtransform RotateMatrix(0, 0, -1.5)
        easein 0.28 matrixtransform RotateMatrix(0, 0, 0)
        repeat

transform fn_head_speed3:
    subpixel True
    matrixanchor (1325, 339)
    matrixtransform RotateMatrix(0, 0, 0)
    block:
        ease 0.13 matrixtransform RotateMatrix(0, 0, 2.0)
        ease 0.13 matrixtransform RotateMatrix(0, 0, -2.0)
        easein 0.14 matrixtransform RotateMatrix(0, 0, 0)
        repeat

transform fn_head_speed4:
    subpixel True
    matrixanchor (1325, 339)
    matrixtransform RotateMatrix(0, 0, 0)
    block:
        ease 0.08 matrixtransform RotateMatrix(0, 0, 1.2)
        ease 0.08 matrixtransform RotateMatrix(0, 0, -1.2)
        easein 0.08 matrixtransform RotateMatrix(0, 0, 0)
        repeat


# ============================================================
# ARM ROTATION TRANSFORMS — pivot at shoulder anchor
# ============================================================
# Left arm — anchor (1150, 600)
transform fn_arm_left_speed0:
    subpixel True
    matrixanchor (1150, 600)
    matrixtransform RotateMatrix(0, 0, 0)

transform fn_arm_left_speed1:
    subpixel True
    matrixanchor (1150, 600)
    matrixtransform RotateMatrix(0, 0, 0)
    block:
        ease 0.40 matrixtransform RotateMatrix(0, 0, 1.0)
        ease 0.40 matrixtransform RotateMatrix(0, 0, -1.0)
        ease 0.40 matrixtransform RotateMatrix(0, 0, 0)
        repeat

transform fn_arm_left_speed2:
    subpixel True
    matrixanchor (1150, 600)
    matrixtransform RotateMatrix(0, 0, 0)
    block:
        ease 0.26 matrixtransform RotateMatrix(0, 0, 1.5)
        ease 0.26 matrixtransform RotateMatrix(0, 0, -1.5)
        easein 0.28 matrixtransform RotateMatrix(0, 0, 0)
        repeat

transform fn_arm_left_speed3:
    subpixel True
    matrixanchor (1150, 600)
    matrixtransform RotateMatrix(0, 0, 0)
    block:
        ease 0.13 matrixtransform RotateMatrix(0, 0, 2.5)
        ease 0.13 matrixtransform RotateMatrix(0, 0, -2.5)
        easein 0.14 matrixtransform RotateMatrix(0, 0, 0)
        repeat

transform fn_arm_left_speed4:
    subpixel True
    matrixanchor (1150, 600)
    matrixtransform RotateMatrix(0, 0, 0)
    block:
        ease 0.08 matrixtransform RotateMatrix(0, 0, 1.5)
        ease 0.08 matrixtransform RotateMatrix(0, 0, -1.5)
        easein 0.08 matrixtransform RotateMatrix(0, 0, 0)
        repeat

# Right arm — anchor (1500, 600), mirrored rotation
transform fn_arm_right_speed0:
    subpixel True
    matrixanchor (1500, 600)
    matrixtransform RotateMatrix(0, 0, 0)

transform fn_arm_right_speed1:
    subpixel True
    matrixanchor (1500, 600)
    matrixtransform RotateMatrix(0, 0, 0)
    block:
        ease 0.40 matrixtransform RotateMatrix(0, 0, -1.0)
        ease 0.40 matrixtransform RotateMatrix(0, 0, 1.0)
        ease 0.40 matrixtransform RotateMatrix(0, 0, 0)
        repeat

transform fn_arm_right_speed2:
    subpixel True
    matrixanchor (1500, 600)
    matrixtransform RotateMatrix(0, 0, 0)
    block:
        ease 0.26 matrixtransform RotateMatrix(0, 0, -1.5)
        ease 0.26 matrixtransform RotateMatrix(0, 0, 1.5)
        easein 0.28 matrixtransform RotateMatrix(0, 0, 0)
        repeat

transform fn_arm_right_speed3:
    subpixel True
    matrixanchor (1500, 600)
    matrixtransform RotateMatrix(0, 0, 0)
    block:
        ease 0.13 matrixtransform RotateMatrix(0, 0, -2.5)
        ease 0.13 matrixtransform RotateMatrix(0, 0, 2.5)
        easein 0.14 matrixtransform RotateMatrix(0, 0, 0)
        repeat

transform fn_arm_right_speed4:
    subpixel True
    matrixanchor (1500, 600)
    matrixtransform RotateMatrix(0, 0, 0)
    block:
        ease 0.08 matrixtransform RotateMatrix(0, 0, -1.5)
        ease 0.08 matrixtransform RotateMatrix(0, 0, 1.5)
        easein 0.08 matrixtransform RotateMatrix(0, 0, 0)
        repeat


# ============================================================
# SHIN ROTATION TRANSFORMS — pivot at knee anchor
# ============================================================
# Left shin — anchor (1214, 382)
transform fn_shin_left_speed0:
    subpixel True
    matrixanchor (1214, 382)
    matrixtransform RotateMatrix(0, 0, 0)

transform fn_shin_left_speed1:
    subpixel True
    matrixanchor (1214, 382)
    matrixtransform RotateMatrix(0, 0, 0)
    block:
        ease 0.40 matrixtransform RotateMatrix(0, 0, 1.5)
        ease 0.40 matrixtransform RotateMatrix(0, 0, -1.5)
        ease 0.40 matrixtransform RotateMatrix(0, 0, 0)
        repeat

transform fn_shin_left_speed2:
    subpixel True
    matrixanchor (1214, 382)
    matrixtransform RotateMatrix(0, 0, 0)
    block:
        ease 0.26 matrixtransform RotateMatrix(0, 0, 2.5)
        ease 0.26 matrixtransform RotateMatrix(0, 0, -2.5)
        easein 0.28 matrixtransform RotateMatrix(0, 0, 0)
        repeat

transform fn_shin_left_speed3:
    subpixel True
    matrixanchor (1214, 382)
    matrixtransform RotateMatrix(0, 0, 0)
    block:
        ease 0.13 matrixtransform RotateMatrix(0, 0, 3.5)
        ease 0.13 matrixtransform RotateMatrix(0, 0, -3.5)
        easein 0.14 matrixtransform RotateMatrix(0, 0, 0)
        repeat

transform fn_shin_left_speed4:
    subpixel True
    matrixanchor (1214, 382)
    matrixtransform RotateMatrix(0, 0, 0)
    block:
        ease 0.08 matrixtransform RotateMatrix(0, 0, 2.0)
        ease 0.08 matrixtransform RotateMatrix(0, 0, -2.0)
        easein 0.08 matrixtransform RotateMatrix(0, 0, 0)
        repeat

# Right shin — anchor (1434, 384), mirrored rotation
transform fn_shin_right_speed0:
    subpixel True
    matrixanchor (1434, 384)
    matrixtransform RotateMatrix(0, 0, 0)

transform fn_shin_right_speed1:
    subpixel True
    matrixanchor (1434, 384)
    matrixtransform RotateMatrix(0, 0, 0)
    block:
        ease 0.40 matrixtransform RotateMatrix(0, 0, -1.5)
        ease 0.40 matrixtransform RotateMatrix(0, 0, 1.5)
        ease 0.40 matrixtransform RotateMatrix(0, 0, 0)
        repeat

transform fn_shin_right_speed2:
    subpixel True
    matrixanchor (1434, 384)
    matrixtransform RotateMatrix(0, 0, 0)
    block:
        ease 0.26 matrixtransform RotateMatrix(0, 0, -2.5)
        ease 0.26 matrixtransform RotateMatrix(0, 0, 2.5)
        easein 0.28 matrixtransform RotateMatrix(0, 0, 0)
        repeat

transform fn_shin_right_speed3:
    subpixel True
    matrixanchor (1434, 384)
    matrixtransform RotateMatrix(0, 0, 0)
    block:
        ease 0.13 matrixtransform RotateMatrix(0, 0, -3.5)
        ease 0.13 matrixtransform RotateMatrix(0, 0, 3.5)
        easein 0.14 matrixtransform RotateMatrix(0, 0, 0)
        repeat

transform fn_shin_right_speed4:
    subpixel True
    matrixanchor (1434, 384)
    matrixtransform RotateMatrix(0, 0, 0)
    block:
        ease 0.08 matrixtransform RotateMatrix(0, 0, -2.0)
        ease 0.08 matrixtransform RotateMatrix(0, 0, 2.0)
        easein 0.08 matrixtransform RotateMatrix(0, 0, 0)
        repeat


# ============================================================
# SCROTUM ZOOM TRANSFORMS (subtle pulse per speed)
# ============================================================
transform fn_scrotum_speed0:
    subpixel True
    yzoom 1.0

transform fn_scrotum_speed1:
    subpixel True
    yzoom 1.0
    block:
        ease 0.40 yzoom 1.02
        ease 0.40 yzoom 1.0
        repeat

transform fn_scrotum_speed2:
    subpixel True
    yzoom 1.0
    block:
        ease 0.26 yzoom 1.03
        easein 0.28 yzoom 1.0
        repeat

transform fn_scrotum_speed3:
    subpixel True
    yzoom 1.0
    block:
        ease 0.13 yzoom 1.04
        easein 0.14 yzoom 1.0
        repeat

transform fn_scrotum_speed4:
    subpixel True
    yzoom 1.0
    block:
        ease 0.08 yzoom 1.025
        easein 0.08 yzoom 1.0
        repeat


# ============================================================
# PENIS TRANSFORMS — VAGINAL
# ============================================================
transform fn_penis_speed0:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    yoffset 50

transform fn_penis_cum_hold:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    yoffset 0

transform fn_penis_speed1:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    yoffset 0
    block:
        ease 0.40 yoffset 20
        ease 0.80 yoffset 0
        repeat

transform fn_penis_speed2:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    yoffset 0
    block:
        ease 0.28 yoffset 28
        easein 0.52 yoffset 0
        repeat

transform fn_penis_speed3:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    yoffset 0
    block:
        ease 0.15 yoffset 20
        easein 0.25 yoffset 0
        repeat

transform fn_penis_speed4:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    yoffset 0
    block:
        ease 0.12 yoffset 8
        easein 0.12 yoffset 0
        repeat

transform fn_penis_tip:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    yoffset 0
    block:
        ease 0.50 yoffset 10
        ease 1.00 yoffset 0
        repeat


# ============================================================
# PENIS TRANSFORMS — ANAL
# ============================================================
transform fna_penis_speed1:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    yoffset 0
    block:
        ease 0.40 yoffset 10
        ease 0.80 yoffset 0
        repeat

transform fna_penis_speed2:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    yoffset 0
    block:
        ease 0.28 yoffset 14
        easein 0.52 yoffset 0
        repeat

transform fna_penis_speed3:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    yoffset 0
    block:
        ease 0.15 yoffset 20
        easein 0.25 yoffset 0
        repeat

transform fna_penis_speed4:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    yoffset 0
    block:
        ease 0.12 yoffset 8
        easein 0.12 yoffset 0
        repeat


# ============================================================
# Apply speed — shows ALL layers at the given speed
# ============================================================
label FN_ApplySpeed(girl, speed=1):

    $ debug_log("[DEBUG] FN_ApplySpeed: speed=%s anal=%s started=%s tip=%s rub=%s" % (speed, store.fn_anal, store.fn_started, getattr(store, "fn_tip_mode", False), getattr(store, "fn_rub_mode", False)))

    python:
        _gid = girl.gid
        slot_tf = fn_get_slot_transform(speed, anal=store.fn_anal)
        slot_at = [slot_tf]

        # --- FN Legs (Player — below everything, moves with penis) ---
        # Same transform as the penis: speed 0 = static (hold if started, withdrawn if not)
        _legs_at = [fn_get_penis_transform(speed, anal=store.fn_anal)]
        renpy.show("%s fn_legs" % _gid, tag="fn_legs", at_list=_legs_at, zorder=9930)

        # --- Clothing attributes from registry ---
        _fn_clothing = _build_clothing_attributes(girl, "full_nelson")

        # Strip panties once penetration has begun (same rule for both holes).
        # At idle (not started) panties stay ON so the entry shows the pre-
        # penetration "before" art; the remove-panties menu / HoleTransition
        # strips them right before speed 1. (Previously anal stripped early via
        # `or store.fn_anal`, so anal entry jumped straight to penetration art.)
        if store.fn_started:
            _PANTIES_ON = set(_FN_PANTIES_STRIP.keys())
            _fn_clothing = [a for a in _fn_clothing if a not in _PANTIES_ON]

        # Normalize: force explicit _none defaults for every clothing group
        # Ren'Py layeredimage attributes are sticky -- without explicit _none,
        # stripped clothes persist visually after Outfit_Change removes them
        _grp_defaults = _FN_CLOTHING_GROUPS.get(_gid, {})
        for _grp_prefix, _grp_none in _grp_defaults.items():
            if not any(a.startswith(_grp_prefix) for a in _fn_clothing):
                _fn_clothing.append(_grp_none)

        # Detect chest states
        _chest_down = any(a.endswith("_down") for a in _fn_clothing)
        _chest_up_attr = None
        _CHEST_UP_MAP = _FN_CHEST_UP_MAPS.get(_gid, {})
        for _cu_attr, (_cu_none, _cu_path) in _CHEST_UP_MAP.items():
            if _cu_attr in _fn_clothing:
                _fn_clothing = [(_cu_none if a == _cu_attr else a) for a in _fn_clothing]
                _chest_up_attr = (_cu_attr, _cu_path)
                break

        print("[FN_APPLY] clothing=%s chest_down=%s chest_up=%s started=%s anal=%s speed=%s girl.panties=%s" % (_fn_clothing, _chest_down, _chest_up_attr, store.fn_started, store.fn_anal, speed, girl.clothes.get("panties", "NONE")))

        img_name = "%s fn" % _gid
        if _fn_clothing:
            img_name += " " + " ".join(_fn_clothing)
        print("[FN_APPLY] SHOW img='%s' | clothing=%s chest_up=%s started=%s anal=%s speed=%s" % (img_name, str(_fn_clothing), str(_chest_up_attr), store.fn_started, store.fn_anal, speed))

        # --- Layeredimage (Torso + Clothes) ---
        renpy.show(img_name, tag=_gid, at_list=slot_at, zorder=9990)

        # --- Chest/Nipples standalone layers ---
        # z-order: chest=9995, cum_boobs=9996, nipples=9997, clothing_up=9997, head=9998
        _chest_at = [slot_tf, fn_get_chest_transform(speed, anal=store.fn_anal)]
        _nipple_at = [slot_tf, fn_get_nipple_transform(speed, anal=store.fn_anal)]
        if _chest_down:
            renpy.hide("fn_chest_over")
            renpy.hide("fn_nipples_over")
            renpy.hide("fn_chest_clothing_up")
        elif _chest_up_attr:
            _chest_at = [slot_tf, fn_get_chest_transform(speed, anal=store.fn_anal, covered=True)]
            renpy.show("%s fn_chest_over" % _gid, tag="fn_chest_over", at_list=_chest_at, zorder=9995)
            renpy.show("%s fn_nipples_over" % _gid, tag="fn_nipples_over", at_list=_nipple_at, zorder=9997)
            renpy.show("fn_chest_clothing_up", what=renpy.displayable(_chest_up_attr[1]), tag="fn_chest_clothing_up", at_list=_chest_at, zorder=9997)
        else:
            renpy.show("%s fn_chest_over" % _gid, tag="fn_chest_over", at_list=_chest_at, zorder=9995)
            renpy.show("%s fn_nipples_over" % _gid, tag="fn_nipples_over", at_list=_nipple_at, zorder=9997)
            renpy.hide("fn_chest_clothing_up")

        # --- Head + Expressions (standalone with rotation) ---
        _head_at = [slot_tf, fn_get_head_transform(speed)]
        renpy.show("%s fn_head_over" % _gid, tag="fn_head_over", at_list=_head_at, zorder=9998)

        # --- Girl Arms (Layer 12 — bottom) ---
        _arm_left_at = [slot_tf, fn_get_arm_left_transform(speed)]
        renpy.show("%s fn_arm_left" % _gid, tag="fn_arm_left", at_list=_arm_left_at, zorder=9940)
        _arm_right_at = [slot_tf, fn_get_arm_right_transform(speed)]
        renpy.show("%s fn_arm_right" % _gid, tag="fn_arm_right", at_list=_arm_right_at, zorder=9940)

        # --- Ass Base Safe (Layer 11) ---
        renpy.show("%s fn_ass_safe" % _gid, tag="fn_ass_safe", at_list=slot_at, zorder=9950)

        # --- Legs (Layer 10 — bottom part) ---
        renpy.show("%s fn_thigh_left" % _gid, tag="fn_thigh_left", at_list=slot_at, zorder=9960)
        renpy.show("%s fn_thigh_right" % _gid, tag="fn_thigh_right", at_list=slot_at, zorder=9960)
        _shin_left_at = [slot_tf, fn_get_shin_left_transform(speed)]
        renpy.show("%s fn_shin_left" % _gid, tag="fn_shin_left", at_list=_shin_left_at, zorder=9961)
        _shin_right_at = [slot_tf, fn_get_shin_right_transform(speed)]
        renpy.show("%s fn_shin_right" % _gid, tag="fn_shin_right", at_list=_shin_right_at, zorder=9961)
        # --- Guy Arms (Layer 10 — above legs) ---
        renpy.show("%s fn_guy_arm_left" % _gid, tag="fn_guy_arm_left", at_list=slot_at, zorder=9966)
        renpy.show("%s fn_guy_arm_right" % _gid, tag="fn_guy_arm_right", at_list=slot_at, zorder=9966)

        # --- Pelvis Base Safe ---
        # Vaginal: below penis (9980) so penis is visible in front
        # Anal: above penis (9989) so pelvis covers penis entering from behind
        _pelvis_z = 9989 if store.fn_anal else 9980
        renpy.show("%s fn_pelvis_safe" % _gid, tag="fn_pelvis_safe", at_list=slot_at, zorder=_pelvis_z)

    # --- Vaginal / Anal layers ---
    # z-order: pelvis_safe=9980(vag)/9989(anal), genital_below=9985, scrotum=9986
    #          penis=9988, Torso@9990, during_fast=9994
    #          chest=9996, nipples/chest_clothing=9997, head=9998
    #          Rub: penis=9995, scrotum=9994 (ABOVE everything for grinding)
    python:
        # speed 0 -> static (cum_hold if started, withdrawn idle if not) — handled centrally
        _pen_tf = fn_get_penis_transform(speed, anal=store.fn_anal)
        _pen_at = [_pen_tf]
        _scrotum_at = [_pen_tf, fn_get_scrotum_transform(speed)]
        _tip_mode = getattr(store, "fn_tip_mode", False)
        _rub_mode = getattr(store, "fn_rub_mode", False) and not store.fn_started

        # Default penis z-order (overridden in vaginal branch for rub)
        _pen_z = 9988

        if store.fn_anal:
            # ANAL MODE — genital layers below Torso, fast above.
            # Idle (speed 0 & not started, or rub) shows the pre-penetration
            # "before ass" art with panties still on and the penis above the
            # pelvis (rub-like), matching the vaginal idle. Penetration art
            # appears only once started, so the entry no longer jumps straight in.
            _show_idle_anal = (speed <= 0 and not store.fn_started) or _rub_mode
            if _show_idle_anal:
                renpy.show("%s fn_before_ass" % _gid, tag="fn_before_ass", at_list=slot_at, zorder=9985)
                renpy.hide("fn_during_anal_below")
                renpy.hide("fn_during_anal_fast")
                _pen_z = 9995
                _scr_z = 9994
            else:
                renpy.hide("fn_before_ass")
                renpy.show("%s fn_during_anal_below" % _gid, tag="fn_during_anal_below", at_list=slot_at, zorder=9985)
                renpy.show("%s fn_during_anal_fast" % _gid, tag="fn_during_anal_fast", at_list=slot_at, zorder=9994)
                _pen_z = 9988
                _scr_z = 9986

            if store.condom_active:
                _condom_img = _condom_img_tag("fn_condom")
                _fn_penis_c = Fixed(renpy.displayable("%s fn_pussy_penis" % _gid), renpy.displayable(_condom_img), fit_first=True)
                renpy.show("fn_pussy_penis_combined", what=_fn_penis_c, tag="fn_pussy_penis", at_list=_pen_at, zorder=_pen_z)
            else:
                renpy.show("%s fn_pussy_penis" % _gid, tag="fn_pussy_penis", at_list=_pen_at, zorder=_pen_z)
            renpy.show("%s fn_scrotum" % _gid, tag="fn_scrotum", at_list=_scrotum_at, zorder=_scr_z)

            # Pussy-region art in ANAL mode. The panties live inside the Torso
            # layeredimage (9990) and are stripped only once `fn_started` (see the
            # panties-strip block above), so the z must follow that same flag:
            #   panties ON  (not fn_started -> remove-panties menu / idle tip):
            #       9987, BELOW the panties+pelvis so the pussy stays hidden behind
            #       the panties instead of drawing over them.
            #   panties OFF (fn_started -> full anal): 9991, ABOVE the body (no pussy
            #       cutout, so anything under 9990 would be covered) but BELOW the anal
            #       action art (during_anal_fast 9994): at 9995 the pussy gape/drip drew
            #       OVER the visible penetration (the author 2026-10-11, Tenny FN).
            _bp_z = 9991 if store.fn_started else 9987
            if store._fn_had_pussy:
                renpy.hide("fn_before_pussy")
                renpy.hide("fn_during_pussy_below")
                if _gid == "tenny":
                    renpy.show("tenny fn_after_pussy_anim", tag="fn_after_pussy", at_list=slot_at, zorder=_bp_z)
                else:
                    renpy.show("%s fn_cum_inside_pussy_2" % _gid, tag="fn_cum_inside_pussy_2", at_list=slot_at, zorder=_bp_z)
            else:
                renpy.show("%s fn_before_pussy" % _gid, tag="fn_before_pussy", at_list=slot_at, zorder=_bp_z)
                renpy.hide("fn_during_pussy_below")
                renpy.hide("fn_after_pussy")
                renpy.hide("fn_cum_inside_pussy_2")

            renpy.hide("fn_during_pussy_fast")
        else:
            # VAGINAL MODE — genital/penis below Torso, during_fast above Torso
            # Rub: penis above everything (grinding visual)
            # fn_started + speed 0 = freeze after cum, keep penetration state
            _show_idle = (speed <= 0 and not store.fn_started) or _rub_mode
            debug_log("[FN_APPLY] VAGINAL _show_idle=%s tip=%s rub=%s speed=%s started=%s | showing=%s" % (_show_idle, _tip_mode, _rub_mode, speed, store.fn_started, "before_pussy" if _show_idle else "during_pussy"))
            if _show_idle:
                renpy.show("%s fn_before_pussy" % _gid, tag="fn_before_pussy", at_list=slot_at, zorder=9985)
                renpy.hide("fn_during_pussy_below")
                renpy.hide("fn_during_pussy_fast")
            else:
                renpy.hide("fn_before_pussy")
                renpy.show("%s fn_during_pussy_below" % _gid, tag="fn_during_pussy_below", at_list=slot_at, zorder=9985)
                renpy.show("%s fn_during_pussy_fast" % _gid, tag="fn_during_pussy_fast", at_list=slot_at, zorder=9994)

            if not store.fn_started:
                _pen_z = 9995
                _scr_z = 9994
            else:
                _pen_z = 9988
                _scr_z = 9986
            debug_log("[FN_APPLY] ZORDER pen=%d scr=%d torso=9990 started=%s | penis %s torso" % (_pen_z, _scr_z, store.fn_started, "ABOVE" if not store.fn_started else "BELOW"))
            if store.condom_active:
                _condom_img = _condom_img_tag("fn_condom")
                _fn_penis_c = Fixed(renpy.displayable("%s fn_pussy_penis" % _gid), renpy.displayable(_condom_img), fit_first=True)
                renpy.show("fn_pussy_penis_combined", what=_fn_penis_c, tag="fn_pussy_penis", at_list=_pen_at, zorder=_pen_z)
            else:
                renpy.show("%s fn_pussy_penis" % _gid, tag="fn_pussy_penis", at_list=_pen_at, zorder=_pen_z)
            renpy.show("%s fn_scrotum" % _gid, tag="fn_scrotum", at_list=_scrotum_at, zorder=_scr_z)

            renpy.hide("fn_before_ass")
            renpy.hide("fn_during_anal_below")
            renpy.hide("fn_during_anal_fast")

    # --- Cum layers (persistent, based on girl.Cum) ---
    # z-order: cum_ass=9965 (above thighs), cum_inside_pussy_2=9987(vag)/9996(anal),
    #          cum_penis=same as penis, after_ass/cum_ass_inside=9987 (vaginal mode, below penis),
    #          cum_boobs=9996 (below nipples=9997)
    python:
        _cum_list = getattr(girl, "Cum", [])
        print("[FN_CUM] girl.Cum=%s anal=%s" % (_cum_list, store.fn_anal))

        # Cum Penis — moves with penis, after any cum inside (vaginal or anal)
        if "dripping" in _cum_list or "dripping_ass" in _cum_list:
            renpy.show("%s fn_cum_penis" % _gid, tag="fn_cum_penis", at_list=_pen_at, zorder=_pen_z)
        else:
            renpy.hide("fn_cum_penis")

        # After Pussy (animated for tenny, static for others)
        # During anal + _fn_had_pussy: genital section already shows after_pussy — only override z if cum adds dripping
        _genital_manages_after_pussy = store.fn_anal and store._fn_had_pussy
        if "dripping" in _cum_list:
            # Anal: above the torso (penis is in the other hole, no pussy cutout) but BELOW the anal
            # action art (9994): at 9996 the drip drew over the visible penetration (author 2026-10-11).
            # Vaginal full sex: below the penis (shaft fills the gape).
            # Vaginal tip IN MOTION: only the glans is in, so the gape/drip shows ABOVE the penis (9988)
            # but below the torso (9990); otherwise the drawn shaft hides it completely. At speed 0 the
            # freeze after an inside cum draws the deep shaft, so a (stale) tip flag must not lift the
            # drip over it (author 2026-10-11, Tenny FN).
            if store.fn_anal:
                _cp2_z = 9991
            elif _tip_mode and speed >= 1:
                _cp2_z = 9989
            else:
                _cp2_z = 9987
            if _gid == "tenny":
                renpy.hide("fn_cum_inside_pussy_2")
                print("[FN_CUM] SHOW tenny fn_after_pussy_anim z=%d" % _cp2_z)
                renpy.show("tenny fn_after_pussy_anim", tag="fn_after_pussy", at_list=slot_at, zorder=_cp2_z)
            else:
                renpy.hide("fn_after_pussy")
                renpy.show("%s fn_cum_inside_pussy_2" % _gid, tag="fn_cum_inside_pussy_2", at_list=slot_at, zorder=_cp2_z)
        elif not _genital_manages_after_pussy:
            renpy.hide("fn_after_pussy")
            renpy.hide("fn_cum_inside_pussy_2")

        # After Ass (animated for tenny, static for others)
        # Only show when NOT doing anal — penis covers the drip area during anal
        # Vaginal mode: the shaft enters from below and passes over the anus, so the gape/drip
        # sits BELOW the penis (9988), same tier as the vaginal after_pussy (9987)
        if "dripping_ass" in _cum_list and not store.fn_anal:
            print("[FN_CUM] SHOW fn_after_ass at z=9987 (vaginal mode, below penis)")
            if _gid == "tenny":
                renpy.hide("fn_cum_ass_inside")
                renpy.show("tenny fn_after_ass_anim", tag="fn_after_ass", at_list=slot_at, zorder=9987)
            else:
                renpy.hide("fn_after_ass")
                renpy.show("%s fn_cum_ass_inside" % _gid, tag="fn_cum_ass_inside", at_list=slot_at, zorder=9987)
        else:
            renpy.hide("fn_after_ass")
            renpy.hide("fn_cum_ass_inside")

        # Cum Boobs — with chest clothing: follows body (slot_at); without: follows chest bounce
        if "boobs" in _cum_list:
            _cum_has_top = girl.clothes.get("chest") is not None and girl.clothes_state.get("chest") not in ("down", None)
            _cum_boobs_at = slot_at if _cum_has_top else _chest_at
            renpy.show("%s fn_cum_boobs" % _gid, tag="fn_cum_boobs", at_list=_cum_boobs_at, zorder=9996)
        else:
            renpy.hide("fn_cum_boobs")

        # Cum Ass — above thighs (9960) so it's visible
        if "ass" in _cum_list:
            renpy.show("%s fn_cum_ass" % _gid, tag="fn_cum_ass", at_list=slot_at, zorder=9965)
        else:
            renpy.hide("fn_cum_ass")

        # Cum Face — above head (9998), follows head transform
        if "face" in _cum_list:
            renpy.show("%s fn_cum_face" % _gid, tag="fn_cum_face", at_list=_head_at, zorder=10000)
        else:
            renpy.hide("fn_cum_face")

    return


# ============================================================
# Hide all FN layers
# ============================================================
init python:
    def _fn_hide_all():
        _fn_tags = [
            "fn_legs",
            "fn_arm_left", "fn_arm_right",
            "fn_ass_safe",
            "fn_thigh_left", "fn_thigh_right",
            "fn_shin_left", "fn_shin_right",
            "fn_guy_arm_left", "fn_guy_arm_right",
            "fn_pelvis_safe",
            "fn_chest_over", "fn_nipples_over", "fn_head_over", "fn_chest_clothing_up",
            "fn_before_pussy", "fn_during_pussy_below", "fn_during_pussy_fast", "fn_pussy_penis", "fn_scrotum",
            "fn_before_ass", "fn_during_anal_below", "fn_during_anal_fast",
            "fn_cum_penis", "fn_cum_inside_pussy_2", "fn_cum_ass_inside", "fn_cum_boobs", "fn_cum_ass",
            "fn_after_pussy", "fn_after_ass",
        ]
        for tag in _fn_tags:
            renpy.hide(tag)


# ============================================================
# TEST LABEL — Developer test for Full Nelson art
# ============================================================
label fn_test:
    # console entry (renpy.jump("fn_test")): same tester as F9 > Negasonic > Full Nelson (art_test.rpy)
    python:
        _at_snapshot(NTW)
        _at_pose = "full_nelson"
    call _at_fn(NTW) from _call_fn_test_at_fn
    $ _at_restore_all()
    return


# ============================================================
# ADDITIONAL DEFAULTS FOR FN STATE
# ============================================================
default fn_rub_mode = False
default fn_tip_mode = False
default _fn_had_pussy = False
default _fn_had_anal = False


# ============================================================
# FN_Launch — initialize Full Nelson scene
# ============================================================
label FN_Launch(girl, from_switch=False):
    $ sub_event_reset(girl)
    $ _kill_scene_threads(keep_watchers=from_switch)
    $ stop_standing_blink(girl)

    if not from_switch:
        $ public_attention_reset()

    python:
        _clear_scene_refs("fn")
        store.cowgirl_started = False
        store.cowgirl_masturbating = False
        store.doggy_started = False

        _hide_all_scene_layers(girl)

        _hide_non_scene_girls(girl)

        store.hiding_face = False
        store._fn_girl = girl
        if not from_switch:
            girl._prev_pose = sprite_state.get(girl.Id, {}).get("pose", "standing")
            girl._prev_slot = getattr(girl, "_current_slot", StageCenter)
        sprite_state.setdefault(girl.Id, {})["pose"] = "full_nelson"
        store.fn_speed = 0
        store.fn_started = False
        store.fn_rub_mode = False
        store.fn_tip_mode = False

        # FN only renders chest + panties — strip slots that don't show
        _fn_rendered = set(POSE_SLOTS.get("full_nelson", []))
        for _slot in ("over", "mid", "skirt", "shoes"):
            if _slot not in _fn_rendered and girl.clothes.get(_slot):
                girl.clothes[_slot] = None
                girl.clothes_state[_slot] = "full"
        store._fn_had_pussy = False
        store._fn_had_anal = False

    if from_switch:
        if girl.Panties is not None:
            $ girl.Outfit_Change(panties="none", pose="full_nelson")
        call FN_ApplySpeed(girl, 0) from _call_FN_ApplySpeed_launch_switch
        with dissolve
    else:
        $ hide_girl_sprite(girl)
        call FN_ApplySpeed(girl, 0) from _call_FN_ApplySpeed_launch_pre
        with fade

        call _fn_bottom_clothes_menu(girl) from _call_fn_bottom_menu_launch
        call FN_ApplySpeed(girl, 0) from _call_FN_ApplySpeed_launch_init

    python:
        renpy.invoke_in_thread(_scene_blink_loop, girl, "_fn_girl", "fn_blink", is_active_fn=_fn_is_active, cs_girls={"ntw", "tenny"}, blink_timing=(0.12, 0.22))
        renpy.invoke_in_thread(_fn_expression_cycle, girl)
    return


# ============================================================
# FN_ControlMenu — main sex loop
# ============================================================
label FN_ControlMenu(girl, from_escalation=False):

    $ store._player_exhausted = False
    $ store._scene_phase = "sex"
    $ store._cheat_shower_max_act = "sex"
    $ _fn_scene_type = "full_nelson_anal" if store.fn_anal else "full_nelson"

    if not from_escalation and not store.fn_started:
        $ fn_speed = 0
        call _fn_bottom_clothes_menu(girl) from _call_fn_bottom_control_entry

    while True:
        $ _fn_scene_type = "full_nelson_anal" if store.fn_anal else "full_nelson"
        $ print("[FN_LOOP] top: energy=%d exhausted=%s Focus=%d fn_started=%s fn_speed=%s post_cum=%s pos_switched=%s Round=%d" % (Player.energy, store._player_exhausted, Player.Focus, store.fn_started, fn_speed, store._post_cum_pending, getattr(store, "_sub_event_position_switched", False), Round))

        if store._post_cum_pending:
            $ print("[FN_LOOP] EXIT: _post_cum_pending=True")
            return

        if getattr(store, "_sub_event_position_switched", False):
            $ print("[FN_LOOP] EXIT: _sub_event_position_switched=True")
            $ store._sub_event_position_switched = False
            return

        # Scene ended or forced out by a sub-call (force_scene_reset, hate_cum, exhaustion...)
        if _scene_should_exit() or store._fn_girl is None:
            $ print("[FN_LOOP] EXIT: scene_should_exit=%s fn_girl_none=%s" % (_scene_should_exit(), store._fn_girl is None))
            return

        if Round >= 100:
            $ Say_Line(girl, _scene_time_up_line())
            call FN_End(girl, dress_up=False) from _call_FN_End_timeout
            return

        menu:
            "Keep going" if store.fn_started:
                python:
                    _fn_lust = _anal_lust_for_speed(girl, fn_speed) if store.fn_anal else -1

                call _sex_scene_tick(girl, _fn_scene_type, fn_speed, girl_lust=_fn_lust) from _call_sst_fn_kg

                $ _apply_anal_lust_cap(girl, store.fn_anal)

                if store._sst_result == "condom_ripped":
                    call FN_CondomRemoveAnim(girl) from _call_FN_CondomRemoveAnim_sst_kg
                    call FN_ApplySpeed(girl, fn_speed) from _call_FN_ApplySpeed_sst_rip

                if store._sst_result == "abort":
                    if store._sst_abort_reason == "post_cum":
                        $ _set_post_cum("full_nelson_anal" if store.fn_anal else "full_nelson", "sex")
                        return
                    if store._sst_abort_reason == "position_switch":
                        return
                    else:
                        call _sex_scene_handle_abort(girl, _fn_scene_type) from _call_sst_abort_fn_kg
                        return

            "Speed up" if fn_speed < 3:
                $ advance_round(TIME_COSTS["sex_tick"])
                $ fn_speed += 1
                call FN_HoleTransition(girl, store.fn_anal) from _call_FN_HoleTransition_su
                call FN_ApplySpeed(girl, fn_speed) from _call_FN_ApplySpeed_su
                $ _moan = scene_moan_tick(girl, _fn_scene_type, fn_speed)
                if _moan:
                    call _moan_say(girl, _moan) from _call_ms_fn_kg
                call _speed_change_tick(girl, _fn_scene_type, 1) from _call_sct_fn_su
                if _scene_should_exit():
                    return
                if fn_speed >= 3:
                    $ _watcher_scene_comment("speed_max")

            "Slow down" if fn_speed > 1:
                $ advance_round(1)
                $ fn_speed -= 1
                call FN_ApplySpeed(girl, fn_speed) from _call_FN_ApplySpeed_sd
                call _speed_change_tick(girl, _fn_scene_type, -1) from _call_sct_fn_sd
                if store._sub_event_position_switched:
                    return
                $ _watcher_scene_comment("speed_down")

            "Penetration..." if store.fn_started:
                $ _es_from = "anal" if store.fn_anal else "sex"
                call _escalation_menu(girl, "full_nelson") from _call_esc_menu_fn_sex
                if store._esc_result == "accepted":
                    call _fn_esc_dispatch(girl, _es_from, fn_speed) from _call_esc_disp_fn_sex
                    # Dispatch may have ended the scene (e.g. cheat condom breakdown on anal->pussy): FN_End clears _fn_girl
                    if store._esc_is_deescalation or store._fn_girl is None:
                        $ debug_log("[FN_LOOP] EXIT after escalation: deesc=%s scene_ended=%s" % (store._esc_is_deescalation, store._fn_girl is None))
                        return
                elif store._esc_result == "scene_ended":
                    call FN_End(girl, dress_up=False) from _call_FN_End_esc_sex
                    return

            "Tease her..." if store.fn_started or getattr(store, "fn_rub_mode", False) or getattr(store, "fn_tip_mode", False):
                # rub and tip tease too (tester 2026-10-11: the option vanished in FN rubbing; every
                # other pose teases at every stage)
                $ advance_round(1)
                call _tease_menu(girl, _fn_scene_type) from _call_tease_menu_fn
                call FN_ApplySpeed(girl, fn_speed) from _call_FN_ApplySpeed_tease

            "Condom..." if store.condom_active and store.fn_started:
                call CondomMidsceneMenu(girl, _fn_scene_type) from _call_CondomMidsceneMenu_fn
                if not store.condom_active:
                    call FN_CondomRemoveAnim(girl) from _call_FN_CondomRemoveAnim_mid
                    call FN_ApplySpeed(girl, fn_speed) from _call_FN_ApplySpeed_condom_rm

            "Switch position..." if store.fn_started and not getattr(store, "_scene_restricted", False):
                if store._condom_broken_hidden:
                    call CondomBreakDiscovery(girl, "full_nelson") from _call_CondomBreakDisc_fn
                if store._stealth_condom_removed:
                    call StealthCondomDiscovery(girl, "full_nelson") from _call_StealthDisc_fn
                # Discovery may have ended the scene (force_scene_reset): don't offer the switch
                if _scene_should_exit() or store._fn_girl is None:
                    return
                menu:
                    "Reverse Cowgirl" if girl_has_pose(girl, "reverse_cowgirl"):
                        $ Say_Player(_("Turn around..."))
                        # Anal scene -> vaginal-only position: same gates as "Switch to her pussy" (escalation.rpy).
                        # A girl whose RCG art has anal (rcg_has_anal) keeps the hole instead: anal stays anal.
                        $ store._switch_gate_ok = True
                        $ _sw_carry_anal = bool(store.fn_anal) and rcg_has_anal(girl)
                        $ _sw_from_anal = bool(store.fn_anal) and not _sw_carry_anal   # only an ANAL scene makes this switch a hole switch
                        if _sw_from_anal:
                            call _switch_to_vaginal_gate(girl, "full_nelson") from _call_sw_gate_sw_fn_rcg
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

                            $ _saved_condom = condom_carry_save()
                            python:
                                store._fn_girl = None
                                store.fn_started = False
                                store.fn_anal = False
                                store.fn_rub_mode = False
                                store.fn_tip_mode = False
                                _fn_hide_all()
                                hide_girl_sprite(girl)
                                store.condom_active = False
                            $ condom_carry_restore(_saved_condom)

                            $ rcg_speed = 0
                            $ store.rcg_anal = _sw_carry_anal
                            $ _scene_position_switch(girl, "full_nelson", "reverse_cowgirl", anal=_sw_carry_anal)   # player switch: count the new position (and sex, if it is vaginal now)
                            call RCG_Launch(girl, from_switch=True) from _call_RCG_Launch_fn_switch
                            if _sw_from_anal and girl.has_trait("virgin"):
                                # she was only doing anal: this switch is her first vaginal penetration
                                call virgin_first_time(girl, "reverse_cowgirl") from _call_virgin_sw_fn_rcg
                            call RCG_ControlMenu(girl) from _call_RCG_ControlMenu_fn_switch

                            $ store._sub_event_position_switched = True

                    "Riding" if girl_has_pose(girl, "cowgirl"):
                        $ Say_Player(_("Get on top..."))
                        # Anal scene -> vaginal-only position: same gates as "Switch to her pussy" (escalation.rpy)
                        $ store._switch_gate_ok = True
                        $ _sw_from_anal = bool(store.fn_anal)   # only an ANAL scene makes this switch a hole switch
                        if _sw_from_anal:
                            call _switch_to_vaginal_gate(girl, "full_nelson") from _call_sw_gate_sw_fn_cg
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

                            $ _saved_condom = condom_carry_save()
                            python:
                                store._fn_girl = None
                                store.fn_started = False
                                store.fn_anal = False
                                store.fn_rub_mode = False
                                store.fn_tip_mode = False
                                _fn_hide_all()
                                hide_girl_sprite(girl)
                                store.condom_active = False
                            $ condom_carry_restore(_saved_condom)

                            $ cowgirl_speed = 0
                            $ _scene_position_switch(girl, "full_nelson", "cowgirl", anal=False)   # player switch: count the new position (and sex, if it is vaginal now)
                            call COWGIRL_Launch(girl, from_switch=True) from _call_COWGIRL_Launch_fn_switch
                            if _sw_from_anal and girl.has_trait("virgin"):
                                # she was only doing anal: this switch is her first vaginal penetration
                                call virgin_first_time(girl, "cowgirl") from _call_virgin_sw_fn_cg
                            call COWGIRL_ControlMenu(girl) from _call_COWGIRL_ControlMenu_fn_switch

                            $ store._sub_event_position_switched = True

                    "Doggy" if girl_has_pose(girl, "doggy"):
                        $ Say_Player(_("Get on all fours..."))
                        # Carry the current hole into the next pose (anal stays anal)
                        $ _switch_anal = store.fn_anal
                        python:
                            _switch_lines = [
                                _("On all fours? Okay..."),

                                _("Mmm, let me get on my hands and knees."),

                                _("Sure... let me turn over."),

                            ]
                        $ Say_Line(girl, _tl(renpy.random.choice(_switch_lines)))

                        $ _saved_condom = condom_carry_save()
                        python:
                            store._fn_girl = None
                            store.fn_started = False
                            store.fn_anal = False
                            store.fn_rub_mode = False
                            store.fn_tip_mode = False
                            _fn_hide_all()
                            hide_girl_sprite(girl)
                            store.condom_active = False
                        $ condom_carry_restore(_saved_condom)

                        $ doggy_speed = 0
                        $ store.doggy_anal = _switch_anal
                        $ debug_log("[SWITCH] FN->DG carry anal=%s" % store.doggy_anal)
                        $ _scene_position_switch(girl, "full_nelson", "doggy", anal=getattr(store, "doggy_anal", False))   # player switch: count the new position (and sex, if it is vaginal now)
                        call DG_Launch(girl, from_switch=True) from _call_DG_Launch_fn_switch
                        call DG_ControlMenu(girl) from _call_DG_ControlMenu_fn_switch

                        $ store._sub_event_position_switched = True

                    "Laying Down" if girl_has_pose(girl, "laying_down"):
                        $ Say_Player(_("Lay down for me..."))
                        # Carry the current hole into the next pose (anal stays anal)
                        $ _switch_anal = store.fn_anal
                        python:
                            _switch_lines = [
                                _("You want me on my back? Okay..."),

                                _("Mmm, let me lay down for you."),

                                _("Sure... let me get comfortable."),

                            ]
                        $ Say_Line(girl, _tl(renpy.random.choice(_switch_lines)))

                        $ _saved_condom = condom_carry_save()
                        python:
                            store._fn_girl = None
                            store.fn_started = False
                            store.fn_anal = False
                            store.fn_rub_mode = False
                            store.fn_tip_mode = False
                            _fn_hide_all()
                            hide_girl_sprite(girl)
                            store.condom_active = False
                        $ condom_carry_restore(_saved_condom)

                        $ laying_speed = 0
                        $ store.laying_anal = _switch_anal
                        $ debug_log("[SWITCH] FN->LD carry anal=%s" % store.laying_anal)
                        $ _scene_position_switch(girl, "full_nelson", "laying_down", anal=getattr(store, "laying_anal", False))   # player switch: count the new position (and sex, if it is vaginal now)
                        call LD_Launch(girl, from_switch=True) from _call_LD_Launch_fn_switch
                        call LD_ControlMenu(girl) from _call_LD_ControlMenu_fn_switch

                        $ store._sub_event_position_switched = True

                    "Back":
                        pass

            "Strip her..." if not getattr(store, "_scene_restricted", False):
                $ advance_round(1)
                call FN_StripMenu(girl) from _call_FN_StripMenu

            "Record Options..." if (store.fn_started and not getattr(store, "_recording_active", False) and not getattr(store, "_scene_restricted", False) and (Player.has_item("tripod") or (getattr(store, "_witness_watching", False) and getattr(store, "_witness_girl", None) is not None) or store._ntr_partner_watching)) or (getattr(store, "_recording_active", False) and getattr(store, "_recording_girl", None) == girl):
                menu:
                    "Record her yourself" if Player.has_item("tripod") and not getattr(store, "_recording_active", False) and not getattr(store, "_scene_restricted", False):
                        call _fn_tripod_start_recording(girl, _fn_scene_type) from _call_fn_tripod_start_fn
                    "Ask [store._ntr_watching_npc.Name] to record" if store._ntr_partner_watching and not getattr(store, "_recording_active", False) and not getattr(store, "_scene_restricted", False):
                        call _watcher_record_start(girl, "full_nelson") from _call_watcher_rec_start_fn_npc
                    "Ask [store._witness_girl.Name] to record" if getattr(store, "_witness_watching", False) and getattr(store, "_witness_girl", None) is not None and not store._ntr_partner_watching and not getattr(store, "_recording_active", False) and not getattr(store, "_scene_restricted", False):
                        call _watcher_record_start(girl, "full_nelson") from _call_watcher_rec_start_fn_girl
                    "Stop recording" if getattr(store, "_recording_active", False) and getattr(store, "_recording_girl", None) == girl:
                        if getattr(store, "_recording_watcher_gid", None):
                            $ _rec_stop_name = _get_recording_stopper_name()
                            $ finalize_recording()
                            if _rec_stop_name:
                                $ _rec_stop_text = _tl(_("%s stopped the recording.")) % _rec_stop_name
                                $ Narration(_rec_stop_text)
                            else:
                                $ Narration(_("You stop recording."))
                        else:
                            call _fn_tripod_stop_recording(girl) from _call_fn_tripod_stop_fn
                    "Back":
                        pass
                call FN_ApplySpeed(girl, fn_speed) from _call_FN_ApplySpeed_rec_opts

            "{color=#fbbf24}Cum{/color}" if player_is_cumming():
                call PlayerCumMenu(girl, _fn_scene_type) from _call_PlayerCumMenu_voluntary_fn
                $ _handle_post_cum_exit("full_nelson_anal" if store.fn_anal else "full_nelson", "sex")
                return

            "Stop now" if store.fn_started:
                if store._forced_creampie_end_after_orgasm:
                    call _player_stops_after_forced_creampie(girl, _fn_scene_type) from _call__player_stops_forced_fn
                $ store._edge_lust_check = (girl.Lust >= 80)
                if store._edge_lust_check:
                    # She begs with him still in her: the scene stays exactly as it is until the action really stops.
                    # "Keep going" goes on at the same speed, her "No, stop." is the same stop as below (author, 2026-10-09)
                    call EdgeDenial(girl, _fn_scene_type) from _call_EdgeDenial_fn
                    if girl.Lust >= 100:
                        call GirlCumming(girl, _fn_scene_type, _fn_scene_type) from _call_GirlCumming_fn_edge
                    if store._edge_scene_ended:
                        $ store._edge_scene_ended = False
                        call _cum_dispatch_aftermath(girl, "full_nelson_anal" if store.fn_anal else "full_nelson") from _call_ca_dispatch_fn_edge_stop
                        return
                else:
                    call _cum_dispatch_aftermath(girl, "full_nelson_anal" if store.fn_anal else "full_nelson") from _call_ca_dispatch_fn_stop
                    return

    return


# ============================================================
# FN_End — cleanup and restore standing sprite
# ============================================================
label FN_End(girl, dress_up=True):
    $ debug_log("[DEBUG] FN_End: entered, dress_up=%s" % str(dress_up))
    $ store._last_scene_was_anal = store.fn_anal
    if store.fn_anal:
        $ store._atm_source_gid = girl.gid
    $ scene_full_cleanup(girl)
    $ finalize_recording()
    $ _player_cleanup(girl)

    $ pose = getattr(girl, "_prev_pose", "standing")
    $ slot = _safe_restore_slot(getattr(girl, "_prev_slot", StageCenter))

    python:
        slot_transform = _slot_to_transform(slot)
        _reset_expression_state(girl)

        store._fn_girl = None
        store.fn_blink = False
        store.fn_started = False
        store.fn_anal = False
        store.fn_rub_mode = False
        store.fn_tip_mode = False
        store.hiding_face = False

        girl.ResetVisuals(pose=pose, at_list=[slot_transform])
        _fn_hide_all()
        store.condom_active = False

    if dress_up:
        call DressUp_Sequence(girl) from _call_DressUp_Sequence_fn
    return


# ============================================================
# FN_StripMenu — clothing removal during full nelson
# ============================================================
label FN_StripMenu(girl):
    while True:
        menu:
            "Pull chest up" if girl.Chest and girl.clothes_state.get("chest") != "up" and _item_has_state(girl, "chest", "up"):
                call _strip_approval(girl, _get_strip_slots(girl, "chest")) from _call__strip_approval_fn_chest_up
                if store._strip_approved:
                    $ girl.clothes_state["chest"] = "up"
                    if store._fn_girl == girl:
                        call FN_ApplySpeed(girl, fn_speed) from _call_FN_ApplySpeed_strip_chest_up
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_fn_chest_up

            "Remove chest" if girl.Chest:
                call _strip_approval(girl, _get_strip_slots(girl, "chest")) from _call__strip_approval_fn_chest_r
                if store._strip_approved:
                    $ _do_strip_change(girl, "chest", "full_nelson")
                    if store._fn_girl == girl:
                        call FN_ApplySpeed(girl, fn_speed) from _call_FN_ApplySpeed_strip_chest
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_fn_chest

            "Remove panties" if girl.Panties:
                call _strip_approval(girl, ["panties"]) from _call__strip_approval_fn_pan
                if store._strip_approved:
                    $ girl.Outfit_Change(panties="none", pose="full_nelson")
                    if store._fn_girl == girl:
                        call FN_ApplySpeed(girl, fn_speed) from _call_FN_ApplySpeed_strip_pan
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_fn_pan

            "Back":
                return


# ============================================================
# Tripod Recording — centralized start/stop for FN
# ============================================================
label _fn_tripod_start_recording(girl, scene_type):
    $ _rec_ok = recording_consent_check(girl, scene_type)

    if _rec_ok["result"] == "denied":
        $ _line = _format_partner_line(girl, scene_pick_line("record_denied", scene=scene_type, girl=girl))
        $ Say_Line(girl, _line)
        $ store._fn_tripod_result = "denied"
        return

    $ _fn_rec_face_hidden = (_rec_ok["result"] == "face_hidden_only")
    $ _fn_rec_reluctant = girl.has_trait("camera_hater")
    # Recording state BEFORE her accept line: the camera_lover voice (and its auto-discover)
    # only plays while _recording_active is on (scene_lines.rpy). The block below re-sets these.
    python:
        store._recording_active = True
        store._recording_girl = girl
        store._recording_seconds = 0.0
        store._recording_face_locked = _fn_rec_face_hidden

    if _fn_rec_face_hidden:
        $ _line = _format_partner_line(girl, scene_pick_line("record_accepted", scene=scene_type, girl=girl))
        $ Say_Line(girl, _line)
        "She agrees, but insists on hiding her face from the camera."
    else:
        $ _line = _format_partner_line(girl, scene_pick_line("record_accepted", scene=scene_type, girl=girl))
        $ Say_Line(girl, _line)

    if _fn_rec_reluctant:
        $ Change_Status(girl, "Love", -3)
        if girl.has_npc_partner():
            $ Change_Status(girl, "Love", -2)
        $ unlock_achievement("say_cheese")

    show expression "#000" as tripod_black zorder 99999
    with fade
    "You set up the tripod and position the camera."

    python:
        store._recording_active = True
        store._recording_girl = girl
        store._recording_seconds = 0.0
        store._recording_face_locked = _fn_rec_face_hidden
        _pen = scene_type_is_penetration(scene_type)
        vid = {
            "girl_gid": girl.gid,
            "type": scene_type,
            "location": CurrentLocation,
            "committed": girl.has_npc_partner(),
            "consensual": True,
            "reluctant": _fn_rec_reluctant,
            "face_hidden": _fn_rec_face_hidden,
            "hd": Player.has_item("tekmix_camera"),
            "snapshot": _make_vid_snapshot(girl),
        }
        if _pen:
            vid["condom"] = bool(store.condom_active)
        _tag_coercion_on_vid(vid)
        store.Player.recorded_videos.append(vid)

    $ fn_speed = 1
    call FN_ApplySpeed(girl, 1) from _call_FN_ApplySpeed_tripod_start
    hide tripod_black
    with fade
    $ renpy.show_screen("recording_overlay")
    $ store._fn_tripod_result = "started"
    $ print("[FN_TRIPOD] Recording started: type=%s face_hidden=%s" % (scene_type, _fn_rec_face_hidden))
    call _coercion_recording_react(girl) from _call_coercion_rec_fn
    return

label _fn_tripod_stop_recording(girl):
    show expression "#000" as tripod_black zorder 99999
    with fade
    $ finalize_recording()
    "You take down the tripod and put it away."
    $ fn_speed = 1
    call FN_ApplySpeed(girl, 1) from _call_FN_ApplySpeed_tripod_stop
    hide tripod_black
    with fade
    $ store._fn_tripod_result = "stopped"
    $ print("[FN_TRIPOD] Recording stopped")
    return


# ============================================================
# FN_RubLaunch — setup for rub mode
# ============================================================
label FN_RubLaunch(girl):
    $ sub_event_reset(girl)

    $ public_attention_reset()
    call PlayerExposure(girl) from _call_PlayerExposure_fn_rub

    $ girl._prev_pose = getattr(girl, "default_pose", "standing")
    $ girl._prev_slot = getattr(girl, "SpriteLoc", StageCenter)
    if not getattr(girl, "_saved_outfit", None):
        $ girl.SaveOutfit()

    python:
        _clear_scene_refs("fn")

        _hide_all_scene_layers(girl)

        _hide_non_scene_girls(girl)

        store._fn_girl = girl
        store.fn_started = False
        store.fn_rub_mode = True
        store.fn_tip_mode = False
        store.fn_anal = False
        store._fn_had_pussy = False
        store._fn_had_anal = False
        sprite_state.setdefault(girl.Id, {})["pose"] = "full_nelson"
        hide_girl_sprite(girl)

        # FN only renders chest + panties — strip slots that don't show
        # so standing sprite between positions matches what the player saw
        _fn_rendered = set(POSE_SLOTS.get("full_nelson", []))
        for _slot in ("over", "mid", "skirt", "shoes"):
            if _slot not in _fn_rendered and girl.clothes.get(_slot):
                girl.clothes[_slot] = None
                girl.clothes_state[_slot] = "full"

    $ fn_speed = 0

    call FN_ApplySpeed(girl, 0) from _call_FN_ApplySpeed_rub_init
    with fade

    python:
        renpy.invoke_in_thread(_scene_blink_loop, girl, "_fn_girl", "fn_blink", is_active_fn=_fn_is_active, cs_girls={"ntw", "tenny"}, blink_timing=(0.12, 0.22))
        renpy.invoke_in_thread(_fn_expression_cycle, girl)
    return


# ═══════════════════════════════════════════════════════════
# _fn_esc_dispatch — visual transitions after _escalation_menu
# Handles state vars, condom, visuals, and enters the next menu
# ═══════════════════════════════════════════════════════════
label _fn_esc_dispatch(girl, from_state, current_speed):
    if store._esc_result != "accepted":
        return

    # ── De-escalation ──────────────────────────────────────
    if store._esc_is_deescalation:
        if store._esc_target == "rub":
            python:
                store.fn_rub_mode = True
                store.fn_tip_mode = False
                store.fn_started = False
                store.fn_anal = False
            call FN_ApplySpeed(girl, 0) from _call_FN_ApplySpeed_deesc_rub
            call FN_RubControlMenu(girl) from _call_FN_RubCM_deesc
            return
        elif store._esc_target == "tip":
            $ store.fn_tip_mode = True
            call FN_ApplySpeed(girl, 1) from _call_FN_ApplySpeed_deesc_tip
            call FN_TipControlMenu(girl) from _call_FN_TipCM_deesc
            return
        elif store._esc_target == "sex":
            python:
                store.fn_anal = False
                store.fn_tip_mode = False
            $ _fn_scene_type = "full_nelson"
            call FN_HoleTransition(girl, False) from _call_FN_HoleT_deesc_sex
            call FN_ApplySpeed(girl, current_speed) from _call_FN_ApplySpeed_deesc_sex
            return
        return

    # ── Tip (from rub) ─────────────────────────────────────
    if store._esc_target == "tip":
        $ store.fn_anal = store._esc_anal_choice
        call FN_ApplySpeed(girl, 0) from _call_FN_ApplySpeed_esc_tip_prep
        call _fn_bottom_clothes_menu(girl) from _call_fn_bottom_esc_tip
        python:
            store.fn_rub_mode = False
            store.fn_tip_mode = True
        call FN_HoleTransition(girl, store.fn_anal) from _call_FN_HoleT_esc_tip
        call FN_ApplySpeed(girl, 1) from _call_FN_ApplySpeed_esc_tip

        if store._esc_was_forced:
            $ Say_Line(girl, _esc_pick_line(girl, _ESC_TIP_FORCE_ACCEPT))
            $ Say_Player(_("It's just the tip, I promise..."))
            $ Say_Line(girl, _tl(renpy.random.choice(_ESC_TIP_FORCE_REACT)))

        call FN_TipControlMenu(girl) from _call_FN_TipCM_esc_tip
        return

    # ── Sex escalation (from rub or tip) ───────────────────
    if store._esc_target == "sex" and from_state != "anal":
        python:
            _from_tip = (from_state == "tip")
            store.fn_anal = False

        if not _from_tip:
            call _fn_bottom_clothes_menu(girl) from _call_fn_bottom_esc_sex

        python:
            store.fn_rub_mode = False
            store.fn_tip_mode = False
            store._saved_fn_started = store.fn_started
            store.fn_started = False
        call FN_ApplySpeed(girl, 0) from _call_FN_ApplySpeed_rest_esc_sex

        if store._esc_was_forced:
            if _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False):
                call condom_check(girl, True, "hard_deny") from _call_condom_esc_fn_sex_f_cheat
                if store.condom_denied:
                    $ store.fn_started = store._saved_fn_started
                    call FN_End(girl, dress_up=False) from _call_FN_End_esc_sex_f_cond
                    call _cheat_no_condom_breakdown(girl) from _call_condom_snap_esc_fn_sex_f
                    return
            else:
                # She refuses raw: decide it NOW, before the act is counted and before a virgin loses it
                if not getattr(store, "_esc_skip_condom", False) and not _force_raw_accepts(girl):
                    call force_raw(girl) from _call_force_raw_esc_fn_sex_pre
                    if store.condom_denied:
                        $ store.fn_started = store._saved_fn_started
                        call FN_End(girl, dress_up=False) from _call_FN_End_esc_sex_f_deny_pre
                        return
                # Defer force_raw until after visual transition (penis visible during dialogue)
                python:
                    store.condom_active = False
                    store.condom_denied = False
                    store._force_raw_pending = True
        else:
            if _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False):
                call condom_check(girl, True, "hard_deny") from _call_condom_esc_fn_sex_a_cheat
            else:
                $ _pen = store._esc_pen_result
                call condom_check(girl, _pen["condom_required"], _pen["raw_outcome"]) from _call_condom_esc_fn_sex_a
            if store.condom_denied:
                if _is_on_cheat_path(girl):
                    $ store.fn_started = store._saved_fn_started
                    call FN_End(girl, dress_up=False) from _call_FN_End_esc_sex_a_cond
                    call _cheat_no_condom_breakdown(girl) from _call_condom_snap_esc_fn_sex_a
                    return
                python:
                    store.fn_rub_mode = (from_state == "rub")
                    store.fn_tip_mode = _from_tip
                    store.fn_started = store._saved_fn_started
                call FN_ApplySpeed(girl, current_speed) from _call_FN_ApplySpeed_esc_sex_cond_deny
                return

        $ store.fn_started = store._saved_fn_started
        if not store.condom_denied:
            $ _scene_escalation(girl, "sex", "full_nelson")
            $ _had_condom_esc = store.condom_active
            python:
                store.fn_rub_mode = False
                store.fn_tip_mode = False
            $ _fn_scene_type = "full_nelson"
            call FN_HoleTransition(girl, False) from _call_FN_HoleT_esc_sex
            if store._esc_virgin_check:
                call virgin_first_time(girl, "full_nelson") from _call_virgin_esc_fn_sex
            $ fn_speed = store._esc_speed
            call FN_ApplySpeed(girl, fn_speed) from _call_FN_ApplySpeed_esc_sex_go

            # ── Deferred force_raw — penis now visible ──
            if getattr(store, "_force_raw_pending", False):
                $ store._force_raw_pending = False
                call force_raw(girl) from _call_force_raw_esc_fn_sex
                if store.condom_denied:
                    call FN_End(girl, dress_up=False) from _call_FN_End_esc_sex_f_deny
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

            call FN_ControlMenu(girl, from_escalation=True) from _call_FN_CM_esc_sex
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

            $ store._saved_fn_started = store.fn_started
            $ store.fn_started = False
            call FN_ApplySpeed(girl, 0) from _call_FN_ApplySpeed_rest_sw_atp
            call condom_check(girl, True, "hard_deny") from _call_condom_fn_sw_atp
            $ store.fn_started = store._saved_fn_started
            if store.condom_denied:
                call FN_ApplySpeed(girl, current_speed) from _call_FN_ApplySpeed_sw_atp_deny
                return

        if _atp_outcome == "accept_raw" and _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False):
            $ store._saved_fn_started = store.fn_started
            $ store.fn_started = False
            call FN_ApplySpeed(girl, 0) from _call_FN_ApplySpeed_rest_sw_cheat
            call condom_check(girl, True, "hard_deny") from _call_condom_fn_sw_cheat
            $ store.fn_started = store._saved_fn_started
            if store.condom_denied:
                call FN_End(girl, dress_up=False) from _call_FN_End_sw_cheat
                call _cheat_no_condom_breakdown(girl) from _call_condom_snap_fn_sw_cheat
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

        $ _scene_position_switch(girl, "anal", "full_nelson")
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

        $ _fn_scene_type = "full_nelson"
        call FN_HoleTransition(girl, False) from _call_FN_HoleT_sw_a2p
        call FN_ApplySpeed(girl, current_speed) from _call_FN_ApplySpeed_sw_a2p

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
            call _fn_bottom_clothes_menu(girl) from _call_fn_bottom_esc_anal
        python:
            store.fn_rub_mode = False
            store.fn_tip_mode = False
            store.fn_anal = True
            store.condom_active = False
            store.condom_denied = False
        $ _fn_scene_type = "full_nelson_anal"
        $ _scene_escalation(girl, "anal", "full_nelson")
        call FN_HoleTransition(girl, True) from _call_FN_HoleT_esc_anal
        $ fn_speed = store._esc_speed
        call FN_ApplySpeed(girl, fn_speed) from _call_FN_ApplySpeed_esc_anal

        if store._esc_was_forced:
            python:
                _post_lines = [
                    _("Ah! You just... put it in my ass... oh fuck..."),
                    _("W-wait! That's my ASS! Oh god..."),
                    _("You didn't even ask! ...ngh... it's so tight..."),
                ]
            $ Say_Line(girl, _tl(renpy.random.choice(_post_lines)))

        call FN_ControlMenu(girl, from_escalation=True) from _call_FN_CM_esc_anal
        if not getattr(store, "_sub_event_position_switched", False):
            python:
                _track_raw_sex_start(girl)
        return

    # ── Anal from sex (hole switch) ────────────────────────
    if store._esc_target == "anal" and from_state == "sex":
        if store._esc_was_forced:
            $ set_scene_expression(girl, "surprised")
            call FN_ApplySpeed(girl, current_speed) from _call_FN_ApplySpeed_sw_fa_pre
            python:
                _sw_pre = [
                    _("Wait, that's my..."),
                    _("H-hey! Wrong hole!"),
                    _("Hold on, that's not my..."),
                ]
            $ Say_Line(girl, _tl(renpy.random.choice(_sw_pre)))
            $ _scene_position_switch(girl, "full_nelson", "anal")
            $ mark_intimacy(girl, "anal")
            $ sex_accept_with_temptation(girl, "anal")
        else:
            $ _scene_position_switch(girl, "full_nelson", "anal")
            $ mark_intimacy(girl, "anal")

        $ Change_Status(girl, "Obed", 8)
        $ Change_Status(girl, "Inbt", 5)
        python:
            store.condom_active = False
            store.condom_denied = False
        $ _fn_scene_type = "full_nelson_anal"
        call FN_HoleTransition(girl, True) from _call_FN_HoleT_sw_p2a
        call FN_ApplySpeed(girl, current_speed) from _call_FN_ApplySpeed_sw_p2a

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


# ============================================================
# FN_RubControlMenu — rub mode main loop
# ============================================================
label FN_RubControlMenu(girl):

    $ store._scene_phase = "rub"
    $ fn_speed = 0
    $ _fn_scene_type = "full_nelson"
    call FN_ApplySpeed(girl, fn_speed) from _call_FN_ApplySpeed_rub_menu_init

    while True:

        if _scene_should_exit():
            return

        if Round >= 100:
            $ Say_Line(girl, _scene_time_up_line())
            call FN_End(girl, dress_up=False) from _call_FN_End_timeout_rub
            return

        menu:
            "Keep going" if fn_speed >= 1:
                $ advance_round(TIME_COSTS["sex_tick"])
                $ add_player_focus(get_player_lust_gain("full_nelson", fn_speed))
                $ _girl_lust_gain(girl, (2 if fn_speed == 1 else 3 if fn_speed == 2 else 5), fn_speed)
                $ _moan = scene_moan_tick(girl, "full_nelson", fn_speed)
                if _moan:
                    call _moan_say(girl, _moan) from _call_ms_fn_su

                if getattr(store, "_path1_rub_first_line_pending", False):
                    $ store._path1_rub_first_line_pending = False
                    $ Say_Line(girl, _cheat_rub_midline(girl))

                if _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False):
                    if _cheat_breaking_point_ready(girl) and renpy.random.random() < 0.30:
                        call _cheat_breaking_point(girl, "full_nelson") from _call_cheat_break_fnrub

                if store._crowd_level > 0:
                    $ _pa_caught = public_attention_tick(girl, "keep_going", fn_speed)
                    if _pa_caught:
                        if not _caught_keeps_going(girl):
                            call FN_End(girl, dress_up=False) from _call_FN_End_rub_pa
                        call caught_in_public(girl, "full_nelson") from _call_caught_public_fn_rub
                        return

                call _sex_interruption_check(girl, "full_nelson") from _call_interrupt_fn_rub
                $ store._witness_expression_lock = False
                if store._sex_interrupted:
                    call FN_End(girl, dress_up=False) from _call_FN_End_rub_int
                    return

                call _npc_partner_detection_tick(girl, "full_nelson") from _call_npc_detect_fn_rub
                if store._npc_witness_scene_aborted:
                    call FN_End(girl, dress_up=False) from _call_FN_End_rub_npc
                    return

                $ _se = sub_event_tick(girl, "full_nelson")
                if _se:
                    call SubEvent_Handle(girl, "full_nelson", _se) from _call_SubEvent_Handle_fn_rub
                    if store._sub_event_position_switched:
                        $ store._sub_event_position_switched = False
                        return

                call _cheat_bf_call_check(girl, "full_nelson") from _call_cheat_bf_fn_rub

                # Spontaneous escalation: she wants more
                call _girl_escalation_check(girl, "rub") from _call_girl_esc_fn_rub
                if store._girl_esc_accepted:
                    $ store.fn_rub_mode = False
                    $ store.fn_tip_mode = True
                    $ store.fn_started = True
                    call FN_ApplySpeed(girl, 0) from _call_FN_ApplySpeed_esc_strip_rub
                    call FN_HoleTransition(girl, False) from _call_FN_HoleTransition_esc_rub_tip
                    call FN_ApplySpeed(girl, 1) from _call_FN_ApplySpeed_esc_rub_tip
                    call FN_TipControlMenu(girl) from _call_FN_TipControlMenu_esc_rub
                    return

                if girl.Lust >= 100:
                    call GirlCumming(girl, "full_nelson", "full_nelson", scene_override="rub") from _call_GirlCumming_fn_rub
                if player_is_cumming():
                    if focus_overdue_tick():
                        call ForcedCumOverdue(girl, _fn_scene_type) from _call_ForcedCumOverdue_fn_rub
                        $ _handle_post_cum_exit("full_nelson", "rub")
                        return

            "Speed up" if fn_speed < 3:
                $ advance_round(TIME_COSTS["sex_tick"])
                $ fn_speed += 1
                call FN_ApplySpeed(girl, fn_speed) from _call_FN_ApplySpeed_rub_su
                $ add_player_focus(get_player_lust_gain("full_nelson", fn_speed))
                $ _girl_lust_gain(girl, (2 if fn_speed == 1 else 3 if fn_speed == 2 else 5), fn_speed)
                $ Narration(_("You rub faster against her."))

            "Slow down" if fn_speed > 0:
                $ advance_round(1)
                $ fn_speed -= 1
                call FN_ApplySpeed(girl, fn_speed) from _call_FN_ApplySpeed_rub_sd
                $ Narration(_("You slow down."))

            "Strip her..." if not getattr(store, "_scene_restricted", False):
                $ advance_round(1)
                call FN_StripMenu(girl) from _call_FN_StripMenu_rub

            "Penetration...":
                call _escalation_menu(girl, "full_nelson") from _call_esc_menu_fn_rub
                if store._esc_result == "accepted":
                    call _fn_esc_dispatch(girl, "rub", fn_speed) from _call_esc_disp_fn_rub
                    return
                elif store._esc_result == "scene_ended":
                    call FN_End(girl, dress_up=False) from _call_FN_End_esc_rub
                    return

            "{color=#fbbf24}Cum{/color}" if player_is_cumming():
                call FN_PlayerCumMenu_RubOutside(girl) from _call_FN_PlayerCumMenu_RubOutside_voluntary
                $ _handle_post_cum_exit("full_nelson", "rub")
                return

            "Stop now":
                call _scene_stop_reaction(girl) from _call_stop_react_fn_rub
                if store._stop_accepted:
                    return


# ============================================================
# FN_TipLaunch — setup for tip mode (direct entry from position menu)
# ============================================================
label FN_TipLaunch(girl):
    $ sub_event_reset(girl)

    $ public_attention_reset()
    call PlayerExposure(girl) from _call_PlayerExposure_fn_tip

    $ girl._prev_pose = getattr(girl, "default_pose", "standing")
    $ girl._prev_slot = getattr(girl, "SpriteLoc", StageCenter)
    if not getattr(girl, "_saved_outfit", None):
        $ girl.SaveOutfit()

    python:
        _clear_scene_refs("fn")

        _hide_all_scene_layers(girl)

        _hide_non_scene_girls(girl)

        store._fn_girl = girl
        store.fn_started = False
        store.fn_rub_mode = False
        store.fn_tip_mode = True
        store._fn_had_pussy = False
        store._fn_had_anal = False
        sprite_state.setdefault(girl.Id, {})["pose"] = "full_nelson"
        hide_girl_sprite(girl)

        # FN only renders chest + panties — strip slots that don't show
        _fn_rendered = set(POSE_SLOTS.get("full_nelson", []))
        for _slot in ("over", "mid", "skirt", "shoes"):
            if _slot not in _fn_rendered and girl.clothes.get(_slot):
                girl.clothes[_slot] = None
                girl.clothes_state[_slot] = "full"

    $ fn_speed = 1

    call FN_ApplySpeed(girl, 0) from _call_FN_ApplySpeed_tip_pre
    with fade

    call _fn_bottom_clothes_menu(girl) from _call_fn_bottom_tip_launch

    python:
        store.fn_started = True
        store._fn_had_pussy = not store.fn_anal
        store._fn_had_anal = store.fn_anal

    call FN_ApplySpeed(girl, 1) from _call_FN_ApplySpeed_tip_launch

    python:
        renpy.invoke_in_thread(_scene_blink_loop, girl, "_fn_girl", "fn_blink", is_active_fn=_fn_is_active, cs_girls={"ntw", "tenny"}, blink_timing=(0.12, 0.22))
        renpy.invoke_in_thread(_fn_expression_cycle, girl)
    return


# ============================================================
# FN_TipControlMenu — tip mode main loop
# ============================================================
label FN_TipControlMenu(girl):

    $ store._scene_phase = "tip"
    $ store._cheat_shower_max_act = "tip"
    $ fn_speed = 1
    $ _fn_scene_type = "full_nelson_anal" if store.fn_anal else "full_nelson"
    $ store._anal_tip_counted = False
    $ advance_round(TIME_COSTS["sex_tick"])
    call FN_ApplySpeed(girl, fn_speed) from _call_FN_ApplySpeed_tip_menu_init

    while True:

        if _scene_should_exit():
            return

        if Round >= 100:
            $ Say_Line(girl, _scene_time_up_line())
            call FN_End(girl, dress_up=False) from _call_FN_End_timeout_tip
            return

        menu:
            "Keep going":
                $ advance_round(TIME_COSTS["sex_tick"])
                $ add_player_focus(get_player_lust_gain(_fn_scene_type, 1))
                if store.fn_anal:
                    if girl.has_trait("anal_lover"):
                        $ _girl_lust_gain(girl, 2, 1)
                    elif girl.has_trait("anal_hater"):
                        $ _girl_lust_gain(girl, 0, 1)
                    else:
                        $ _girl_lust_gain(girl, 1, 1)
                else:
                    $ _girl_lust_gain(girl, 2, 1)
                $ _apply_anal_lust_cap(girl, store.fn_anal)
                $ _moan = scene_moan_tick(girl, _fn_scene_type, 1)
                if _moan:
                    call _moan_say(girl, _moan) from _call_ms_fn_sex

                $ _count_anal_tip(girl, store.fn_anal)

                if getattr(store, "_path1_tip_first_line_pending", False):
                    $ store._path1_tip_first_line_pending = False
                    $ Say_Line(girl, _cheat_tip_midline(girl))

                if _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False):
                    if _cheat_breaking_point_ready(girl) and renpy.random.random() < 0.30:
                        call _cheat_breaking_point(girl, "full_nelson") from _call_cheat_break_fntip

                if store._crowd_level > 0:
                    $ _pa_caught = public_attention_tick(girl, "keep_going", 1)
                    if _pa_caught:
                        if not _caught_keeps_going(girl):
                            call FN_End(girl, dress_up=False) from _call_FN_End_tip_pa
                        call caught_in_public(girl, _fn_scene_type) from _call_caught_public_fn_tip
                        return

                call _sex_interruption_check(girl, _fn_scene_type) from _call_interrupt_fn_tip
                $ store._witness_expression_lock = False
                if store._sex_interrupted:
                    call FN_End(girl, dress_up=False) from _call_FN_End_tip_int
                    return

                call _npc_partner_detection_tick(girl, _fn_scene_type) from _call_npc_detect_fn_tip
                if store._npc_witness_scene_aborted:
                    call FN_End(girl, dress_up=False) from _call_FN_End_tip_npc
                    return

                $ _se = sub_event_tick(girl, _fn_scene_type)
                if _se:
                    call SubEvent_Handle(girl, _fn_scene_type, _se) from _call_SubEvent_Handle_fn_tip
                    if store._sub_event_position_switched:
                        $ store._sub_event_position_switched = False
                        return

                call _cheat_bf_call_check(girl, _fn_scene_type) from _call_cheat_bf_fn_tip

                # Spontaneous escalation: she wants all the way (or anal if she prefers)
                if not store.fn_anal:
                    call _girl_escalation_check(girl, "tip") from _call_girl_esc_fn_tip
                    if store._girl_esc_accepted:
                        $ store.fn_tip_mode = False
                        call _girl_esc_accept_sex(girl, "full_nelson") from _call_girl_esc_accept_fn
                        if store._girl_esc_condom_denied:
                            call FN_End(girl, dress_up=False) from _call_FN_End_esc_condom
                            call _cheat_no_condom_breakdown(girl) from _call_condom_snap_fn_esc
                            return
                        if store._girl_esc_wants_anal:
                            $ store.fn_anal = True
                            $ _fn_scene_type = "full_nelson_anal"
                        $ fn_speed = 2
                        call FN_ApplySpeed(girl, 2) from _call_FN_ApplySpeed_esc_tip_sex
                        call FN_ControlMenu(girl, from_escalation=True) from _call_FN_ControlMenu_esc_tip
                        return

                if girl.Lust >= 100:
                    call GirlCumming(girl, _fn_scene_type, _fn_scene_type, scene_override="tip") from _call_GirlCumming_fn_tip
                if player_is_cumming():
                    if focus_overdue_tick():
                        call ForcedCumOverdue(girl, _fn_scene_type) from _call_ForcedCumOverdue_fn_tip
                        $ _handle_post_cum_exit("full_nelson_anal" if store.fn_anal else "full_nelson", "tip")
                        return

            "Penetration...":
                call _escalation_menu(girl, "full_nelson") from _call_esc_menu_fn_tip
                if store._esc_result == "accepted":
                    call _fn_esc_dispatch(girl, "tip", fn_speed) from _call_esc_disp_fn_tip
                    return
                elif store._esc_result == "scene_ended":
                    call FN_End(girl, dress_up=False) from _call_FN_End_esc_tip
                    return

            "Strip her..." if not getattr(store, "_scene_restricted", False):
                $ advance_round(1)
                call FN_StripMenu(girl) from _call_FN_StripMenu_tip

            "{color=#fbbf24}Cum{/color}" if player_is_cumming():
                call FN_PlayerCumMenu_TipOutside(girl) from _call_FN_PlayerCumMenu_TipOutside_voluntary
                $ _handle_post_cum_exit("full_nelson_anal" if store.fn_anal else "full_nelson", "tip")
                return

            "Stop now":
                call _scene_stop_reaction(girl) from _call_stop_react_fn_tip
                if store._stop_accepted:
                    return


# ============================================================
# FN_PlayerCumMenu_RubOutside — cum during rub mode
# ============================================================
label FN_PlayerCumMenu_RubOutside(girl):
    menu:
        "Cum on her":
            call FN_CumOutsideFreeze(girl) from _call_FN_CumOutsideFreeze_rub
            "You cum on her."
            # FN has no "body" cum art: "outside" alone showed nothing (tester 2026-10-11). Her "All over her" tags.
            $ process_cum(girl, "full_nelson", "outside", ["ass", "boobs", "face"])
            $ apply_cum_bonuses(girl, "cum_outside")
    return


# ============================================================
# FN_PlayerCumMenu_TipOutside — cum during tip mode
# ============================================================
label FN_PlayerCumMenu_TipOutside(girl):

    "You feel yourself getting close..."
    $ _fn_scene_type = "full_nelson_anal" if store.fn_anal else "full_nelson"

    menu:
        "Fire away":
            call FN_CumOutsideFreeze(girl) from _call_FN_CumOutsideFreeze_tip_fire
            "You pull out and cum."
            $ process_cum(girl, _fn_scene_type, "away")
            $ apply_cum_bonuses(girl, "cum_outside")

        "Pull out and cum on her":
            call FN_CumOutsideFreeze(girl) from _call_FN_CumOutsideFreeze_tip
            "You pull out and cum on her."
            # FN has no "body" cum art: "outside" alone showed nothing (tester 2026-10-11). Her "All over her" tags.
            $ process_cum(girl, _fn_scene_type, "outside", ["ass", "boobs", "face"])
            $ apply_cum_bonuses(girl, "cum_outside")

        "Ask to cum in her mouth":
            $ _cum_check = CumPermissionCheck(girl, "cum_in_mouth_ask")
            if _cum_check["accepted"]:
                $ Say_Line(girl, scene_pick_line("cum_mouth_accepted", scene=_fn_scene_type, girl=girl) or _("Go ahead... do it."))
                call _cum_in_mouth_via_bj(girl, _fn_scene_type) from _call_cum_in_mouth_via_bj_fn_tip
            else:
                $ set_scene_expression(girl, "angry")
                $ Say_Line(girl, scene_pick_line("cum_mouth_denied", scene=_fn_scene_type, girl=girl) or _("No way... not in my mouth."))
                call FN_CumOutsideFreeze(girl) from _call_FN_CumOutsideFreeze_tip_mouthdeny
                "You pull out and cum on her."
                $ process_cum(girl, _fn_scene_type, "outside", ["ass", "boobs", "face"])
                $ apply_cum_bonuses(girl, "cum_outside")

        "Ask to cum inside":
            call _tip_ask_cum_inside(girl, _fn_scene_type) from _call_tip_ask_fn

        "Cum inside her":
            call _tip_force_cum_inside(girl, _fn_scene_type) from _call_tip_force_fn
    return


# ============================================================
# FN_HoleTransition — centralized exit/enter animation
# ============================================================
label FN_HoleTransition(girl, to_anal):
    python:
        _ht_switching = store.fn_started and (store.fn_anal != to_anal)
        _ht_first = not store.fn_started
        debug_log("[FN_HT] ENTER to_anal=%s started=%s cur_anal=%s | switching=%s first=%s" % (to_anal, store.fn_started, store.fn_anal, _ht_switching, _ht_first))

    if _ht_switching:
        call FN_ApplySpeed(girl, 0) from _call_FN_ApplySpeed_ht_freeze
        python:
            renpy.hide("fn_pussy_penis")

    python:
        store.fn_anal = to_anal
        store.fn_started = True
        if girl.clothes.get("panties"):
            debug_log("[FN_HT] STRIP panties=%s (penetration auto-strip)" % girl.clothes["panties"])
            girl.clothes["panties"] = None
            girl.clothes_state["panties"] = "full"
        debug_log("[FN_HT] FLAGS SET fn_anal=%s started=%s" % (store.fn_anal, store.fn_started))

    if _ht_first or _ht_switching:
        call FN_PenisEnterAnim(girl) from _call_FN_PenisEnterAnim_ht

    python:
        if to_anal:
            store._fn_had_anal = True
        else:
            store._fn_had_pussy = True
        debug_log("[FN_HT] DONE fn_anal=%s had_p=%s had_a=%s" % (store.fn_anal, store._fn_had_pussy, store._fn_had_anal))
    # only when he actually goes in (first entry or pussy -> ass), not on every speed change inside the same hole
    if to_anal and (_ht_first or _ht_switching):
        $ _watcher_scene_comment("anal_enter")
    return


# ============================================================
# FN_PenisEnterAnim — penis slide-in animation
# ============================================================
label FN_PenisEnterAnim(girl):
    python:
        debug_log("[FN_ENTER] fn_anal=%s condom=%s" % (store.fn_anal, store.condom_active))
        _pen_tf = fn_get_penis_transform(1, anal=store.fn_anal)
        _pen_at = [_pen_tf]
        renpy.show("%s fn_pussy_penis" % girl.gid, tag="fn_pussy_penis", at_list=_pen_at, zorder=9988)
        if store.condom_active:
            _condom_img = _condom_img_tag("fn_condom")
            _fn_penis_c = Fixed(renpy.displayable("%s fn_pussy_penis" % girl.gid), renpy.displayable(_condom_img), fit_first=True)
            renpy.show("fn_pussy_penis_combined", what=_fn_penis_c, tag="fn_pussy_penis", at_list=_pen_at, zorder=9988)
    return


# ============================================================
# _fn_bottom_clothes_menu — strip bottoms on entry (centralized)
# ============================================================
label _fn_bottom_clothes_menu(girl):
    $ _fn_btm_pos = "full_nelson_anal" if store.fn_anal else "full_nelson"
    call _scene_bottom_clothes_menu(girl, _fn_btm_pos) from _call_scene_btm_fn
    return


# ============================================================
# CUM ANIMATION LABELS
# ============================================================

# FN_CumAnim — cum inside animation (speed 4 + screen shake)
label FN_CumAnim(girl):
    $ _fn_prev_cum_speed = store.fn_speed
    $ _apply_cum_expression(girl, "full_nelson_anal" if store.fn_anal else "full_nelson", "inside")

    $ store.fn_speed = 4
    call FN_ApplySpeed(girl, 4) from _call_FN_ApplySpeed_cum

    call _cum_punch_pair("rear") from _call_cum_punch_fn_cum

    $ store.fn_speed = 0
    call FN_ApplySpeed(girl, 0) from _call_FN_ApplySpeed_cum_freeze

    return


# FN_CumOutsideFreeze — cum outside freeze
label FN_CumOutsideFreeze(girl):
    python:
        store.condom_active = False
        _apply_cum_expression(girl, "full_nelson_anal" if store.fn_anal else "full_nelson", "outside")

    call FN_ApplySpeed(girl, 0) from _call_FN_ApplySpeed_cum_outside

    python:
        _pen_at = [fn_penis_speed0]
        renpy.show("%s fn_pussy_penis" % girl.gid, tag="fn_pussy_penis", at_list=_pen_at, zorder=9995)
        _scr_at = [fn_penis_speed0, fn_get_scrotum_transform(0)]
        renpy.show("%s fn_scrotum" % girl.gid, tag="fn_scrotum", at_list=_scr_at, zorder=9994)
        _legs_at = [fn_penis_speed0]
        renpy.show("%s fn_legs" % girl.gid, tag="fn_legs", at_list=_legs_at, zorder=9930)
        renpy.hide("fn_cum_penis")
        renpy.hide("fn_cum_face")

    call _cum_punch_pair("rear") from _call_cum_punch_fn_outside

    return


# FN_CondomRemoveAnim — condom removal mid-scene
label FN_CondomRemoveAnim(girl):
    python:
        _pen_tf = fn_get_penis_transform(0, anal=store.fn_anal)
        _pen_at = [_pen_tf]
        renpy.show("%s fn_pussy_penis" % girl.gid, tag="fn_pussy_penis", at_list=_pen_at, zorder=9988)
    $ renpy.pause(0.4)
    python:
        renpy.hide("fn_pussy_penis")
    $ renpy.pause(0.3)
    python:
        renpy.show("%s fn_pussy_penis" % girl.gid, tag="fn_pussy_penis", at_list=_pen_at, zorder=9988)
    $ renpy.pause(0.4)
    return


# FN_CreampieAftermath — static pose after cum inside
label FN_CreampieAftermath(girl):
    call FN_ApplySpeed(girl, 0) from _call_FN_ApplySpeed_creampie_aftermath

    return
