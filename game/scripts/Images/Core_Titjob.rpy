# ============================================================
# CORE TITJOB SYSTEM
# ============================================================

default titjob_speed = 0
default titjob_started = False
default titjob_arms_pose = 1
default titjob_grab = False
default _titjob_girl = None

init python:
    # -----------------------------
    # SLOT TRANSFORM
    # -----------------------------
    def _is_petite_tj():
        g = store._titjob_girl
        if not g:
            return False
        return GIRLS_CONFIG.get(g.gid, {}).get("body_type", "medium") == "petite"

    def titjob_get_slot_transform(speed):
        if _is_petite_tj():
            slot_map = {0: titjob_slot_speed0, 1: titjob_slot_petite1, 2: titjob_slot_petite2, 3: titjob_slot_petite3}
        else:
            slot_map = {0: titjob_slot_speed0, 1: titjob_slot_speed1, 2: titjob_slot_speed2, 3: titjob_slot_speed3}
        return slot_map.get(speed, slot_map[1])

    def titjob_get_penis_transform():
        return titjob_penis_static

    def titjob_get_boobs_transform(speed):
        if _is_petite_tj():
            slot_map = {
                0: titjob_boobs_speed0,
                1: titjob_boobs_petite1,
                2: titjob_boobs_petite2,
                3: titjob_boobs_petite3,
            }
        else:
            slot_map = {
                0: titjob_boobs_speed0,
                1: titjob_boobs_speed1,
                2: titjob_boobs_speed2,
                3: titjob_boobs_speed3,
            }
            gid = store._titjob_girl.gid if store._titjob_girl else None
            overrides = _gsc(gid, "boobs_transforms", {}, "titjob")
            for spd, tf_name in overrides.items():
                slot_map[spd] = getattr(store, tf_name)
        return slot_map.get(speed, slot_map[1])

    def titjob_get_nipples_transform(speed):
        if _is_petite_tj():
            slot_map = {
                0: titjob_nipples_speed0,
                1: titjob_nipples_petite1,
                2: titjob_nipples_petite2,
                3: titjob_nipples_petite3,
            }
        else:
            slot_map = {
                0: titjob_nipples_speed0,
                1: titjob_nipples_speed1,
                2: titjob_nipples_speed2,
                3: titjob_nipples_speed3,
            }
            gid = store._titjob_girl.gid if store._titjob_girl else None
            overrides = _gsc(gid, "nipples_transforms", {}, "titjob")
            for spd, tf_name in overrides.items():
                slot_map[spd] = getattr(store, tf_name)
        return slot_map.get(speed, slot_map[1])

# -----------------------------
# TITJOB SLOT (CHARACTER MOVES)
# matrixanchor (960, 800) = pivot na cintura, independente do bounce
# rotacao lenta e suave, igual ao padrao Verity titjob
# -----------------------------
transform titjob_slot_speed0:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 30

transform titjob_slot_speed1:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 30
    block:
        pause 0.35
        ease 0.20 yoffset 90
        pause 0.25
        ease 1.20 yoffset 30
        repeat

transform titjob_slot_speed2:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 30
    block:
        pause 0.22
        ease 0.16 yoffset 110
        pause 0.18
        easein 0.75 yoffset 30
        repeat

transform titjob_slot_speed3:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 30
    block:
        ease 0.22 yoffset 115
        easein 0.22 yoffset 30
        repeat

# -----------------------------
# PETITE SLOT (much less vertical movement)
# -----------------------------
transform titjob_slot_petite1:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 30
    block:
        pause 0.35
        ease 0.20 yoffset 52
        pause 0.25
        ease 1.20 yoffset 30
        repeat

transform titjob_slot_petite2:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 30
    block:
        pause 0.22
        ease 0.16 yoffset 58
        pause 0.18
        easein 0.75 yoffset 30
        repeat

transform titjob_slot_petite3:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 30
    block:
        ease 0.22 yoffset 80
        easein 0.22 yoffset 30
        repeat

# -----------------------------
# SLAP
# -----------------------------
transform tj_slap_right_in:
    subpixel True
    anchor (0.5, 0.5)
    xpos 1.3
    ypos 0.52
    alpha 1.0
    easein 0.08 xpos 0.50
    pause 0.15
    easeout 0.25 xpos -0.3 alpha 0.0

transform tj_slap_left_in:
    subpixel True
    anchor (0.5, 0.5)
    xpos -0.3
    ypos 0.52
    alpha 1.0
    easein 0.08 xpos 0.50
    pause 0.15
    easeout 0.25 xpos 1.3 alpha 0.0

# -----------------------------
# PENIS (STATIC)
# -----------------------------
transform titjob_penis_static:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    xoffset 0
    yoffset 0

# -----------------------------
# BOOBS (STRETCH)
# -----------------------------
transform titjob_boobs_speed0:
    subpixel True
    yoffset 0
    yzoom 1.0

transform titjob_boobs_speed1:
    subpixel True
    yoffset 0
    yzoom 1.015
    xzoom 1.0
    parallel:
        pause 0.35
        ease 0.20 yoffset 2
        pause 0.25
        easeout 1.20 yoffset 0
        repeat
    parallel:
        pause 0.35
        ease 0.20 yzoom 0.98
        pause 0.25
        easeout 1.20 yzoom 1.015
        repeat
    parallel:
        pause 0.35
        ease 0.20 xzoom 1.015
        pause 0.25
        easeout 1.20 xzoom 1.0
        repeat

transform titjob_boobs_speed2:
    subpixel True
    yoffset -1
    yzoom 1.02
    xzoom 1.0
    parallel:
        pause 0.22
        ease 0.16 yoffset 3
        pause 0.18
        easeout 0.75 yoffset -1
        repeat
    parallel:
        pause 0.22
        ease 0.16 yzoom 0.975
        pause 0.18
        easeout 0.75 yzoom 1.02
        repeat
    parallel:
        pause 0.22
        ease 0.16 xzoom 1.02
        pause 0.18
        easeout 0.75 xzoom 1.0
        repeat

transform titjob_boobs_speed3:
    subpixel True
    yoffset -1
    yzoom 1.02
    xzoom 1.0
    parallel:
        ease 0.22 yzoom 0.975
        easeout 0.22 yzoom 1.02
        repeat
    parallel:
        ease 0.22 yoffset 3
        easeout 0.22 yoffset -1
        repeat
    parallel:
        ease 0.22 xzoom 1.02
        easeout 0.22 xzoom 1.0
        repeat

# -----------------------------
# PETITE BOOBS (zoom only, no Y movement)
# -----------------------------
transform titjob_boobs_petite1:
    subpixel True
    yzoom 1.008
    xzoom 1.0
    parallel:
        pause 0.35
        ease 0.20 yzoom 0.992
        pause 0.25
        easeout 1.20 yzoom 1.008
        repeat
    parallel:
        pause 0.35
        ease 0.20 xzoom 1.008
        pause 0.25
        easeout 1.20 xzoom 1.0
        repeat

transform titjob_boobs_petite2:
    subpixel True
    yzoom 1.01
    xzoom 1.0
    parallel:
        pause 0.22
        ease 0.16 yzoom 0.988
        pause 0.18
        easeout 0.75 yzoom 1.01
        repeat
    parallel:
        pause 0.22
        ease 0.16 xzoom 1.01
        pause 0.18
        easeout 0.75 xzoom 1.0
        repeat

transform titjob_boobs_petite3:
    subpixel True
    yzoom 1.01
    xzoom 1.0
    parallel:
        ease 0.22 yzoom 0.988
        easeout 0.22 yzoom 1.01
        repeat
    parallel:
        ease 0.22 xzoom 1.01
        easeout 0.22 xzoom 1.0
        repeat

# -----------------------------
# ROGUE BOOBS (reduced bounce — ~30% less than standard)
# -----------------------------
transform titjob_boobs_rogue1:
    subpixel True
    yoffset 0
    yzoom 1.01
    xzoom 1.0
    parallel:
        pause 0.35
        ease 0.20 yoffset 1
        pause 0.25
        easeout 1.20 yoffset 0
        repeat
    parallel:
        pause 0.35
        ease 0.20 yzoom 0.987
        pause 0.25
        easeout 1.20 yzoom 1.01
        repeat
    parallel:
        pause 0.35
        ease 0.20 xzoom 1.01
        pause 0.25
        easeout 1.20 xzoom 1.0
        repeat

transform titjob_boobs_rogue2:
    subpixel True
    yoffset 0
    yzoom 1.013
    xzoom 1.0
    parallel:
        pause 0.22
        ease 0.16 yoffset 2
        pause 0.18
        easeout 0.75 yoffset 0
        repeat
    parallel:
        pause 0.22
        ease 0.16 yzoom 0.983
        pause 0.18
        easeout 0.75 yzoom 1.013
        repeat
    parallel:
        pause 0.22
        ease 0.16 xzoom 1.013
        pause 0.18
        easeout 0.75 xzoom 1.0
        repeat

transform titjob_boobs_rogue3:
    subpixel True
    yoffset 0
    yzoom 1.013
    xzoom 1.0
    parallel:
        ease 0.22 yzoom 0.983
        easeout 0.22 yzoom 1.013
        repeat
    parallel:
        ease 0.22 yoffset 2
        easeout 0.22 yoffset 0
        repeat
    parallel:
        ease 0.22 xzoom 1.013
        easeout 0.22 xzoom 1.0
        repeat

# -----------------------------
# NIPPLES (extra jiggle on top of boobs)
# -----------------------------
transform titjob_nipples_speed0:
    subpixel True
    yoffset 0
    yzoom 1.0

transform titjob_nipples_speed1:
    subpixel True
    yoffset 0
    yzoom 1.025
    xzoom 1.0
    parallel:
        pause 0.35
        ease 0.20 yoffset 4
        pause 0.25
        easeout 1.20 yoffset 0
        repeat
    parallel:
        pause 0.35
        ease 0.20 yzoom 0.97
        pause 0.25
        easeout 1.20 yzoom 1.025
        repeat
    parallel:
        pause 0.35
        ease 0.20 xzoom 1.025
        pause 0.25
        easeout 1.20 xzoom 1.0
        repeat

transform titjob_nipples_speed2:
    subpixel True
    yoffset -1
    yzoom 1.03
    xzoom 1.0
    parallel:
        pause 0.22
        ease 0.16 yoffset 5
        pause 0.18
        easeout 0.75 yoffset -1
        repeat
    parallel:
        pause 0.22
        ease 0.16 yzoom 0.965
        pause 0.18
        easeout 0.75 yzoom 1.03
        repeat
    parallel:
        pause 0.22
        ease 0.16 xzoom 1.03
        pause 0.18
        easeout 0.75 xzoom 1.0
        repeat

transform titjob_nipples_speed3:
    subpixel True
    yoffset -1
    yzoom 1.03
    xzoom 1.0
    parallel:
        ease 0.22 yzoom 0.965
        easeout 0.22 yzoom 1.03
        repeat
    parallel:
        ease 0.22 yoffset 5
        easeout 0.22 yoffset -1
        repeat
    parallel:
        ease 0.22 xzoom 1.03
        easeout 0.22 xzoom 1.0
        repeat

# -----------------------------
# PETITE NIPPLES (zoom only, no Y movement)
# -----------------------------
transform titjob_nipples_petite1:
    subpixel True
    yzoom 1.012
    xzoom 1.0
    parallel:
        pause 0.35
        ease 0.20 yzoom 0.985
        pause 0.25
        easeout 1.20 yzoom 1.012
        repeat
    parallel:
        pause 0.35
        ease 0.20 xzoom 1.012
        pause 0.25
        easeout 1.20 xzoom 1.0
        repeat

transform titjob_nipples_petite2:
    subpixel True
    yzoom 1.015
    xzoom 1.0
    parallel:
        pause 0.22
        ease 0.16 yzoom 0.982
        pause 0.18
        easeout 0.75 yzoom 1.015
        repeat
    parallel:
        pause 0.22
        ease 0.16 xzoom 1.015
        pause 0.18
        easeout 0.75 xzoom 1.0
        repeat

transform titjob_nipples_petite3:
    subpixel True
    yzoom 1.015
    xzoom 1.0
    parallel:
        ease 0.22 yzoom 0.982
        easeout 0.22 yzoom 1.015
        repeat
    parallel:
        ease 0.22 xzoom 1.015
        easeout 0.22 xzoom 1.0
        repeat

# -----------------------------
# ROGUE NIPPLES (reduced jiggle — ~30% less than standard)
# -----------------------------
transform titjob_nipples_rogue1:
    subpixel True
    yoffset 0
    yzoom 1.017
    xzoom 1.0
    parallel:
        pause 0.35
        ease 0.20 yoffset 3
        pause 0.25
        easeout 1.20 yoffset 0
        repeat
    parallel:
        pause 0.35
        ease 0.20 yzoom 0.978
        pause 0.25
        easeout 1.20 yzoom 1.017
        repeat
    parallel:
        pause 0.35
        ease 0.20 xzoom 1.017
        pause 0.25
        easeout 1.20 xzoom 1.0
        repeat

transform titjob_nipples_rogue2:
    subpixel True
    yoffset 0
    yzoom 1.02
    xzoom 1.0
    parallel:
        pause 0.22
        ease 0.16 yoffset 3
        pause 0.18
        easeout 0.75 yoffset 0
        repeat
    parallel:
        pause 0.22
        ease 0.16 yzoom 0.975
        pause 0.18
        easeout 0.75 yzoom 1.02
        repeat
    parallel:
        pause 0.22
        ease 0.16 xzoom 1.02
        pause 0.18
        easeout 0.75 xzoom 1.0
        repeat

transform titjob_nipples_rogue3:
    subpixel True
    yoffset 0
    yzoom 1.02
    xzoom 1.0
    parallel:
        ease 0.22 yzoom 0.975
        easeout 0.22 yzoom 1.02
        repeat
    parallel:
        ease 0.22 yoffset 3
        easeout 0.22 yoffset 0
        repeat
    parallel:
        ease 0.22 xzoom 1.02
        easeout 0.22 xzoom 1.0
        repeat

# ============================================================
# Apply speed
# ============================================================
label TITJOB_ApplySpeed(girl, speed=1):

    $ penis_img = "%s titjob_penis" % girl.gid

    python:
        slot_transform = titjob_get_slot_transform(speed)
        penis_transform = titjob_get_penis_transform()
        boobs_transform = titjob_get_boobs_transform(speed)
        nipples_transform = titjob_get_nipples_transform(speed)
        boobs_at = [slot_transform, boobs_transform]
        nipples_at = [slot_transform, nipples_transform]
        print("[TJ] speed=%s petite=%s boobs_tf=%s" % (speed, _is_petite_tj(), boobs_transform))
        if "_build_titjob_attributes" in globals():
            attrs = _build_titjob_attributes(girl)
        else:
            attrs = _build_attributes_for_girl(girl, pose="titjob")
        img_name = "%s titjob" % girl.gid
        if attrs:
            img_name += " " + " ".join(attrs)

        renpy.show(
            img_name,
            tag=girl.gid,
            at_list=[slot_transform],
            zorder=9980
        )

        # Order: boobs(9982) -> nipples(9983) -> bikini(9984) -> boobs_cum(9986) -> grab(10050)
        renpy.show(
            "%s titjob_boobs" % girl.gid,
            tag="titjob_boobs",
            at_list=boobs_at,
            zorder=9982
        )

        renpy.show(
            "%s titjob_nipples" % girl.gid,
            tag="titjob_nipples",
            at_list=nipples_at,
            zorder=9983
        )

        renpy.show(
            penis_img,
            tag="titjob_penis",
            at_list=[penis_transform],
            zorder=9981
        )

        # Bikini top standalone (above boobs/nipples)
        _tj_chest = girl.Chest
        if _tj_chest and _tj_chest != "corset":
            _tj_top_img = "%s tj_%s" % (girl.gid, _tj_chest)
            _tj_top_up_img = "%s tj_%s_up" % (girl.gid, _tj_chest)
            if not girl.ChestUp and renpy.has_image(_tj_top_img):
                renpy.show(_tj_top_img, tag="titjob_chest_top", at_list=boobs_at, zorder=9984)
            elif girl.ChestUp and renpy.has_image(_tj_top_up_img):
                renpy.show(_tj_top_up_img, tag="titjob_chest_top", at_list=boobs_at, zorder=9984)
            else:
                renpy.hide("titjob_chest_top")
        else:
            renpy.hide("titjob_chest_top")

        # Boobs cum (above bikini)
        renpy.show(
            "%s titjob_boobs_cum" % girl.gid,
            tag="titjob_boobs_cum",
            at_list=boobs_at,
            zorder=9986
        )

        # Arms 3 hands overlay (above everything)
        _arms3_hands = "%s tj_arms3_hands" % girl.gid
        if store.titjob_arms_pose == 3 and renpy.has_image(_arms3_hands):
            renpy.show(_arms3_hands, tag="titjob_arms3_hands", at_list=[slot_transform], zorder=10060)
        else:
            renpy.hide("titjob_arms3_hands")

        # Grab boobs layer (above cum, left/right independent)
        _hand_disabled = getattr(store, "_player_hand_disabled", None)
        _slap_hide = getattr(store, "_slap_hide_hand", None)
        if store.titjob_grab:
            _gb_left = "%s tj_grab_boobs_left" % girl.gid
            if renpy.has_image(_gb_left):
                for _side in ("left", "right"):
                    _gb_img = "%s tj_grab_boobs_%s" % (girl.gid, _side)
                    _gb_tag = "titjob_grab_%s" % _side
                    if _hand_disabled != _side and _slap_hide != _side and renpy.has_image(_gb_img):
                        renpy.show(_gb_img, tag=_gb_tag, at_list=boobs_at, zorder=10070)
                    else:
                        renpy.hide(_gb_tag)
            else:
                _gb_img = "%s tj_grab_boobs" % girl.gid
                if renpy.has_image(_gb_img):
                    renpy.show(_gb_img, tag="titjob_grab_left", at_list=boobs_at, zorder=10070)
                renpy.hide("titjob_grab_right")
        else:
            renpy.hide("titjob_grab_left")
            renpy.hide("titjob_grab_right")

    return

# ============================================================
# Launch
# ============================================================
label TITJOB_Launch(girl):
    $ sub_event_reset(girl)
    $ debug_log("[DEBUG] TITJOB_Launch: entered")
    $ _kill_scene_threads()
    $ stop_standing_blink(girl)

    $ public_attention_reset()
    call PlayerExposure(girl) from _call_PlayerExposure_4

    $ girl._prev_pose = getattr(girl, "default_pose", "standing")
    $ girl._prev_slot = getattr(girl, "SpriteLoc", StageCenter)
    if not getattr(girl, "_saved_outfit", None):
        $ girl.SaveOutfit()

    python:
        _hide_all_scene_layers(girl)
        store.hiding_face = False
        store._titjob_girl = girl
        store.titjob_started = False
        store._slap_count = 0   # same as BJ / HJ launch: slaps from an earlier scene must not count toward this one's abort

        # Auto-strip items that don't support titjob pose (e.g. Rogue's mesh over, Shion's jacket and vest: her
        # titjob is only done in a bra / bikini top or bare, author's rule)
        _gid = getattr(girl, "gid", getattr(girl, "Id", ""))
        _reg = CLOTHING_REGISTRY.get(_gid, {})
        for _slot_name, _slot_attr in [("over", "Over"), ("mid", "Mid"), ("chest", "Chest")]:
            _item = getattr(girl, _slot_attr, None)
            if _item:
                _item_cfg = _reg.get(_item, {})
                if "titjob" not in _item_cfg.get("poses", {}):
                    girl.Outfit_Change(**{_slot_name: "none"}, refresh=False)

    if "titjob_speed" not in globals():
        $ titjob_speed = 0

    $ titjob_arms_pose = _gsc(girl.gid, "tj_arms_list", [1, 2, 3], "titjob")[0]

    call TITJOB_ApplySpeed(girl, titjob_speed) from _call_TITJOB_ApplySpeed
    with fade

    # Boobs are exposed via separate layer (titjob_boobs) regardless of clothing.
    # Corset Up and Long Shirt arms stay on.
    $ _exp = girl.RegisterAction("player_saw_boobs")
    if _exp["first_time"]:
        call FirstExposureReaction(girl, "boobs") from _call_FirstExposureReaction_9

    return

# ============================================================
# Control Menu
# ============================================================
label TITJOB_ControlMenu(girl):
    $ store._player_exhausted = False

    if "titjob_speed" not in globals():
        $ titjob_speed = 1

    while True:

        if _scene_should_exit():
            return

        if Round >= 100:
            $ Say_Line(girl, _scene_time_up_line())
            call TITJOB_End(girl, dress_up=False) from _call_TITJOB_End_timeout
            return

        menu:
            "Keep going" if titjob_speed >= 1:
                $ advance_round(TIME_COSTS["sex_tick"])
                $ add_player_focus(get_player_lust_gain("tj", titjob_speed))
                $ _girl_lust_gain(girl, (2 if titjob_speed == 1 else 3 if titjob_speed == 2 else 5), titjob_speed)
                $ _moan = scene_moan_tick(girl, "tj", titjob_speed)
                if _moan:
                    call _moan_say(girl, _moan) from _call_ms_tj_kg

                # Public attention
                $ _pa_caught = public_attention_tick(girl, "keep_going", titjob_speed)
                if _pa_caught:
                    if not _caught_keeps_going(girl):
                        call TITJOB_End(girl, dress_up=False) from _call_TITJOB_End_pa
                    call caught_in_public(girl, "tj") from _call_caught_public_tj_kg
                    return

                # Random interruption check
                call _sex_interruption_check(girl, "tj") from _call__sex_interruption_check_4
                $ store._witness_expression_lock = False
                if store._sex_interrupted:
                    call TITJOB_End(girl, dress_up=False) from _call_TITJOB_End
                    return

                call _npc_partner_detection_tick(girl, "tj") from _call_npc_detect_tj
                if store._npc_witness_scene_aborted:
                    call TITJOB_End(girl, dress_up=False) from _call_TITJOB_End_npc
                    return

                call _sub_event_tick_nonpen(girl, "tj") from _call_se_np_tj
                if store._sst_result == "abort":
                    call TITJOB_End(girl, dress_up=False) from _call_TITJOB_End_se
                    return

                if girl.Lust >= 100:
                    call GirlCumming(girl, "tj", "titjob") from _call_GirlCumming_13
                if player_is_cumming():
                    if focus_overdue_tick():
                        call ForcedCumOverdue(girl, "tj") from _call_ForcedCumOverdue_tj_kg
                        $ _handle_post_cum_exit("tj", "sex")
                        return

            "Speed up" if titjob_speed < 3:
                $ advance_round(TIME_COSTS["sex_tick"])
                $ Say_Player(_("Faster..."))
                $ titjob_started = True
                $ titjob_speed += 1
                call TITJOB_ApplySpeed(girl, titjob_speed) from _call_TITJOB_ApplySpeed_3
                $ add_player_focus(get_player_lust_gain("tj", titjob_speed))
                $ _girl_lust_gain(girl, (2 if titjob_speed == 1 else 3 if titjob_speed == 2 else 5), titjob_speed)
                $ _moan = scene_moan_tick(girl, "tj", titjob_speed)
                if _moan:
                    call _moan_say(girl, _moan) from _call_ms_tj_su
                # Public attention
                $ _pa_caught = public_attention_tick(girl, "speed_up", titjob_speed)
                if _pa_caught:
                    if not _caught_keeps_going(girl):
                        call TITJOB_End(girl, dress_up=False) from _call_TITJOB_End_pa2
                    call caught_in_public(girl, "tj") from _call_caught_public_tj_su
                    return
                if girl.Lust >= 100:
                    call GirlCumming(girl, "tj", "titjob") from _call_GirlCumming_14
                if player_is_cumming():
                    if focus_overdue_tick():
                        call ForcedCumOverdue(girl, "tj") from _call_ForcedCumOverdue_tj_su
                        $ _handle_post_cum_exit("tj", "sex")
                        return
                $ Narration(_("She speeds up her movements."))

            "Speed down" if titjob_speed > 0:
                $ advance_round(1)
                $ titjob_speed -= 1
                call TITJOB_ApplySpeed(girl, titjob_speed) from _call_TITJOB_ApplySpeed_4
                $ add_player_focus(10 if titjob_speed == 1 else 20 if titjob_speed >= 2 else 0)
                $ Narration(_("She slows her movements."))

            "Change her arms":
                python:
                    _arms_list = _gsc(girl.gid, "tj_arms_list", [1, 2, 3], "titjob")
                    _idx = _arms_list.index(titjob_arms_pose) if titjob_arms_pose in _arms_list else -1
                    titjob_arms_pose = _arms_list[(_idx + 1) % len(_arms_list)]
                call TITJOB_ApplySpeed(girl, titjob_speed) from _call_TITJOB_ApplySpeed_5

            "Grab her boobs" if not titjob_grab and not _is_petite_tj():
                $ advance_round(1)
                $ titjob_grab = True
                call TITJOB_ApplySpeed(girl, titjob_speed) from _call_TITJOB_ApplySpeed_grab
                python:
                    _grab_react = renpy.random.choice(["mouth_surprised", _("mouth_lipbite"), "mouth_kiss"])
                    set_scene_expression(girl, None, mouth=_grab_react)
                call TITJOB_ApplySpeed(girl, titjob_speed) from _call_TITJOB_ApplySpeed_grab_react

            "Let go" if titjob_grab:
                $ advance_round(1)
                $ titjob_grab = False
                call TITJOB_ApplySpeed(girl, titjob_speed) from _call_TITJOB_ApplySpeed_letgo

            "Slap her" if titjob_speed >= 1:
                $ advance_round(1)
                call SexScene_Slap(girl, "tj") from _call_SexScene_Slap_tj

            "Tease her..." if titjob_speed > 0:
                $ advance_round(1)
                call _tease_menu(girl, "tj") from _call_tease_menu_tj

            "Strip her":
                $ advance_round(1)
                call TITJOB_StripMenu(girl) from _call_TITJOB_StripMenu

            "Record Options..." if not getattr(store, "_recording_active", False) or getattr(store, "_recording_girl", None) == girl:
                menu:
                    "Record her" if not getattr(store, "_recording_active", False):
                        call _sex_phone_menu(girl, "tj") from _call__sex_phone_menu_6
                    "Ask [store._ntr_watching_npc.Name] to record" if store._ntr_partner_watching and not getattr(store, "_recording_active", False):
                        call _watcher_record_start(girl, "tj") from _call_watcher_rec_start_tj_npc
                    "Ask [store._witness_girl.Name] to record" if getattr(store, "_witness_watching", False) and getattr(store, "_witness_girl", None) is not None and not store._ntr_partner_watching and not getattr(store, "_recording_active", False):
                        call _watcher_record_start(girl, "tj") from _call_watcher_rec_start_tj_girl
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
                call TITJOB_ApplySpeed(girl, titjob_speed) from _call_TITJOB_ApplySpeed_rec_opts

            "{color=#fbbf24}Cum{/color}" if player_is_cumming():
                call PlayerCumMenu(girl, "tj") from _call_PlayerCumMenu_voluntary_tj
                $ _handle_post_cum_exit("tj", "sex")
                return

            "Stop now":
                if store._forced_creampie_end_after_orgasm:
                    call _player_stops_after_forced_creampie(girl, "tj") from _call__player_stops_forced_tj
                else:
                    call _scene_stop_reaction(girl) from _call_scene_stop_reaction_tj
                    if store._stop_accepted:
                        call TITJOB_End(girl, dress_up=False) from _call_TITJOB_End_3
                        return

label TITJOB_StripMenu(girl):
    while True:
        $ _legs_label = _("Remove pants") if _strip_name_for_slot(girl, "skirt") == "pants" else _("Remove skirt")
        menu:
            "Remove top" if girl.Over:
                call _strip_approval(girl, ["over"]) from _call__strip_approval_28
                if store._strip_approved:
                    $ girl.Outfit_Change(over="none", pose="titjob")
                    if _titjob_girl == girl:
                        call TITJOB_ApplySpeed(girl, titjob_speed) from _call_TITJOB_ApplySpeed_8
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_26

            "Pull chest up" if girl.Chest and girl.clothes_state.get("chest") != "up" and _item_has_state(girl, "chest", "up"):
                call _strip_approval(girl, ["chest"]) from _call__strip_approval_29
                if store._strip_approved:
                    $ girl.Outfit_Change(chest_up=True, pose="titjob")
                    if _titjob_girl == girl:
                        call TITJOB_ApplySpeed(girl, titjob_speed) from _call_TITJOB_ApplySpeed_9
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_27

            "Pull chest down" if girl.Chest and girl.ChestUp:
                $ girl.Outfit_Change(chest_up=False, pose="titjob")
                if _titjob_girl == girl:
                    call TITJOB_ApplySpeed(girl, titjob_speed) from _call_TITJOB_ApplySpeed_7

            "Remove chest" if girl.Chest:
                call _strip_approval(girl, ["chest"]) from _call__strip_approval_29b
                if store._strip_approved:
                    $ girl.Outfit_Change(chest="none", pose="titjob")
                    if _titjob_girl == girl:
                        call TITJOB_ApplySpeed(girl, titjob_speed) from _call_TITJOB_ApplySpeed_9b
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_27b

            "[_legs_label]" if girl.Legs:
                call _strip_approval(girl, ["legs"]) from _call__strip_approval_30
                if store._strip_approved:
                    $ girl.Outfit_Change(legs="none", pose="titjob")
                    if _titjob_girl == girl:
                        call TITJOB_ApplySpeed(girl, titjob_speed) from _call_TITJOB_ApplySpeed_10
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_28

            "Remove panties" if girl.Panties:
                call _strip_approval(girl, ["panties"]) from _call__strip_approval_31
                if store._strip_approved:
                    $ girl.Outfit_Change(panties="none", pose="titjob")
                    if _titjob_girl == girl:
                        call TITJOB_ApplySpeed(girl, titjob_speed) from _call_TITJOB_ApplySpeed_11
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_29

            "Remove shoes" if getattr(girl, "Shoes", None):
                $ girl.Outfit_Change(shoes="none", pose="titjob")
                if _titjob_girl == girl:
                    call TITJOB_ApplySpeed(girl, titjob_speed) from _call_TITJOB_ApplySpeed_12

            "Back":
                return

# ============================================================
# Cum Animation
# ============================================================
transform titjob_penis_cum_pulse():
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

label TJ_CumAnim(girl):
    # Cum expression: intense reaction
    $ _apply_cum_expression(girl, "titjob", "inside")
    # Activate grab during cum
    $ store.titjob_grab = True
    call TITJOB_ApplySpeed(girl, titjob_speed) from _call_TITJOB_ApplySpeed_cum

    # Penis pulse
    $ renpy.show("%s titjob_penis" % girl.gid, tag="titjob_penis", at_list=[titjob_penis_cum_pulse()], zorder=9981)

    call _cum_punch_pair("oral") from _call_cum_punch_tj_cum

    # Restore penis + release grab
    $ store.titjob_grab = False
    $ renpy.show("%s titjob_penis" % girl.gid, tag="titjob_penis", at_list=[titjob_penis_static], zorder=9981)
    call TITJOB_ApplySpeed(girl, titjob_speed) from _call_TITJOB_ApplySpeed_cum_end

    return

label TJ_FireAwayCumAnim(girl):
    # Cum outside expression: surprised/amused + freeze ALL animation, release grab
    python:
        _apply_cum_expression(girl, "titjob", "outside")
        store.titjob_grab = False
        _static_slot = titjob_slot_speed0

        # Body static
        if "_build_titjob_attributes" in globals():
            _fa_attrs = _build_titjob_attributes(girl)
        else:
            _fa_attrs = _build_attributes_for_girl(girl, pose="titjob")
        _fa_img = "%s titjob" % girl.gid
        if _fa_attrs:
            _fa_img += " " + " ".join(_fa_attrs)
        renpy.show(_fa_img, tag=girl.gid, at_list=[_static_slot], zorder=9980)

        # Boobs + nipples static
        renpy.show(
            "%s titjob_boobs" % girl.gid,
            tag="titjob_boobs",
            at_list=[_static_slot, titjob_boobs_speed0],
            zorder=9982
        )
        renpy.show(
            "%s titjob_nipples" % girl.gid,
            tag="titjob_nipples",
            at_list=[_static_slot, titjob_nipples_speed0],
            zorder=9983
        )
        renpy.hide("titjob_grab_left")
        renpy.hide("titjob_grab_right")

    # Penis pulse above everything
    $ renpy.show("%s titjob_penis" % girl.gid, tag="titjob_penis", at_list=[titjob_penis_cum_pulse()], zorder=10060)

    call _cum_punch_pair("oral") from _call_cum_punch_tj_fire

    # Restore penis to static (everything else stays frozen)
    $ renpy.show("%s titjob_penis" % girl.gid, tag="titjob_penis", at_list=[titjob_penis_static], zorder=9981)

    return

# ============================================================
# End
# ============================================================
label TITJOB_End(girl, dress_up=True):
    $ debug_log("[DEBUG] TITJOB_End: entered, dress_up=%s" % str(dress_up))
    $ scene_full_cleanup(girl)
    $ finalize_recording()
    $ _player_cleanup(girl)

    $ pose = getattr(girl, "_prev_pose", "standing")
    $ slot = _safe_restore_slot(getattr(girl, "_prev_slot", StageCenter))

    python:
        slot_transform = _slot_to_transform(slot)
        _reset_expression_state(girl)
        store.hiding_face = False

        store._titjob_girl = None
        store.titjob_started = False
        _hide_all_scene_layers(girl)
        girl.ResetVisuals(pose=pose, at_list=[slot_transform])
        store.titjob_grab = False

    if dress_up:
        call DressUp_Sequence(girl) from _call_DressUp_Sequence_6
    $ debug_log("[DEBUG] TITJOB_End: returning")
    return
