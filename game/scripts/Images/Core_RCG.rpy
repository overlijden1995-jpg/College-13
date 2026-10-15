# ============================================================
# CORE RCG SYSTEM
# ============================================================

default rcg_speed = 0
default rcg_started = False
default rcg_butt_state = "butt_top_1"
default rcg_arms_pose = 1
default rcg_grab = False
default rcg_hold = False          # he holds her down by the thighs (girls with the art: rcg_has_hold)
default rcg_anal = False          # he is in her ass (the pose's flag in _ANAL_FLAGS; girls with the art: rcg_has_anal)
default _rcg_had_anal = False     # anal happened in this pose this session (her anus gapes while she hovers over him)
default rcg_rub_mode = False
default rcg_tip_mode = False
default _rcg_girl = None
default _rcg_escalated = False
default _rcg_secret_caught_end = False
default rcg_blink = False
default hiding_face = False

image rcg_condom = "images/characters/Player/RCG Condom.png"
image rcg_condom_broken = "images/characters/Player/Broken RCG Condom.png"

init python:
    # -----------------------------
    # RCG BLINK + EXPRESSION CYCLE
    # -----------------------------
    _RCG_EYES_BY_SPEED = {
        0: ["eyes_normal", "eyes_side", "eyes_side_2"],
        1: ["eyes_normal", "eyes_side", "eyes_squint"],
        2: ["eyes_squint", "eyes_squint_big", "eyes_looking_to_player"],
        3: ["eyes_squint_big", "eyes_looking_to_player", "eyes_surprised"],
    }
    _RCG_BROWS_BY_SPEED = {
        0: ["brows_normal"],
        1: ["brows_normal", "brows_confused"],
        2: ["brows_confused", "brows_surprised"],
        3: ["brows_surprised", "brows_horny"],
    }
    _RCG_MOUTH_BY_SPEED = {
        0: ["mouth_normal", "mouth_smile"],
        1: ["mouth_normal", "mouth_smile", "mouth_serious"],
        2: ["mouth_surprised", "mouth_open_teeth", "mouth_sch"],
        3: ["mouth_open_teeth", "mouth_sch", "mouth_surprised"],
    }

    def _rcg_cs_girls():
        return {gid for gid in GIRL_SCENE_CONFIG if GIRL_SCENE_CONFIG[gid].get("rcg", {}).get("uses_conditionswitch")}

    def _rcg_is_active(girl):
        """Return True only if RCG is the current active scene for this girl."""
        if store._rcg_girl is not girl:
            return False
        if store._doggy_girl is girl or store._cowgirl_girl is girl:
            return False
        return True

    def _rcg_expression_cycle(girl):
        _scene_expression_cycle(girl, "_rcg_girl", "rcg_speed",
            _RCG_EYES_BY_SPEED, _RCG_BROWS_BY_SPEED, _RCG_MOUTH_BY_SPEED,
            is_active_fn=_rcg_is_active, cs_girls=_rcg_cs_girls())

    # ── What a girl's art of this pose has (opt-in: a girl without the art never gets the option) ──
    def rcg_has_anal(girl):
        """He can take her ass in this pose (GIRL_SCENE_CONFIG "rcg" "anal": her art draws it). The flag is
        store.rcg_anal (_ANAL_FLAGS), the scene type "reverse_cowgirl_anal" (rcg_scene_type)."""
        return bool(_gsc(girl.gid, "anal", False, "rcg"))

    def rcg_has_hold(girl):
        """Her art has his hands holding her down ("<gid> rcg_hold_left" / "_right") AND the config allows it."""
        if not _gsc(girl.gid, "has_hold", True, "rcg"):
            return False
        return renpy.has_image("%s rcg_hold_left" % girl.gid, exact=True)

    def rcg_has_grab(girl):
        """Her art has his hands grabbing her ass ("<gid> rcg_grab_butt_left" / "_right", or the single image)."""
        return (renpy.has_image("%s rcg_grab_butt_left" % girl.gid, exact=True)
                or renpy.has_image("%s rcg_grab_butt" % girl.gid, exact=True))

    def rcg_has_arms_change(girl):
        return bool(_gsc(girl.gid, "has_arms_change", True, "rcg"))

    def rcg_has_hide_face(girl):
        return bool(_gsc(girl.gid, "has_hide_face", True, "rcg"))

    def rcg_has_rub(girl):
        return bool(_gsc(girl.gid, "has_rub", True, "rcg"))

    def rcg_hold_side_on(side):
        """That hand of his ("left" / "right") is on her right now: he holds her down (rcg_hold) and that hand is
        neither busy with the phone (_player_hand_disabled, while he records) nor spanking her (_slap_hide_hand)."""
        return (bool(getattr(store, "rcg_hold", False)) and getattr(store, "_player_hand_disabled", None) != side
                and getattr(store, "_slap_hide_hand", None) != side)

    def rcg_hold_redraw(girl):
        """A hand of his just let go of her (to spank her: SpankHer): her layer set takes it off right now."""
        if girl.gid == "shion":
            _srcg_redraw_hold(girl)

    def rcg_scene_type():
        """The type of the scene running in this pose: "reverse_cowgirl", or "reverse_cowgirl_anal" while the pose's
        anal flag is on (live_scene_type, interactions.rpy). What every tick / cum / tease / record call gets."""
        return live_scene_type("reverse_cowgirl")

    # ── Head turn (look forward / look back) ──
    _RCG_TURN_FORWARD_OBED_T = 400

    _RCG_TURN_REFUSE_LINES = {
        "cum_slut": [
            _("No way, I want to watch your face when you cum."),
            _("I like looking at you while we do this."),
            _("Turn around? And miss the show? No thanks."),
        ],
        # who gives the orders is femdom (docs/plan_femdom.md D3): hardcore keeps only the rough reasons
        "femdom": [
            _("I'll look wherever I want."),
            _("You're not the boss of me. I want to see you."),
            _("I'm the one on top. I decide where I look."),
        ],
        "hardcore_sex": [
            _("Nah. I like the view from here."),
            _("No. I want to watch you while you fuck me hard."),
            _("Turn around? I want to see your face when I slam down on you."),
        ],
        "cute_sex": [
            _("I want to keep looking at you... is that okay?"),
            _("I feel safer when I can see your face."),
            _("Please, I like being able to see you..."),
        ],
        "camera_hater": [
            _("Why? So you can record me without me knowing? No."),
            _("I don't trust you enough for that."),
            _("Nice try. I'm keeping my eyes on you."),
        ],
        "lesbian": [
            _("I'm already not looking at a woman. Don't make it worse."),
            _("At least let me pretend you're someone else."),
            _("If I can't see you, this gets even weirder for me."),
        ],
        "_default": [
            _("No, I want to keep looking at you."),
            _("I like seeing your face."),
            _("I'd rather keep eye contact."),
        ],
    }

    _RCG_TURN_ACCEPT_LINES = {
        "cum_slut": [
            _("Fine... but you better not finish without warning me."),
            _("Okay, but I'll be turning back soon."),
        ],
        "hardcore_sex": [
            _("Whatever. Just don't get any ideas."),
            _("Fine. But this doesn't mean I trust you."),
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

    def _rcg_turn_forward_check(girl):
        obed = getattr(girl, "Obed", 0)
        bonus = 0
        if girl.has_trait("hardcore_sex"):
            bonus -= 100
        if girl.has_trait("cute_sex"):
            bonus -= 50
        if girl.has_trait("camera_hater"):
            bonus -= 150
        if girl.has_trait("lesbian"):
            bonus -= 100
        if girl.has_trait("cum_slut"):
            bonus -= 50
        # an order about where she looks: a submissive takes it sooner, a femdom later (plan_submissive_pass S2)
        if girl.has_trait("submissive"):
            bonus += 100
        if girl.has_trait("femdom"):
            bonus -= 100
        return obed + bonus >= _RCG_TURN_FORWARD_OBED_T

    def _rcg_turn_trait_key(girl):
        for t in ("camera_hater", "cum_slut", "lesbian", "femdom", "hardcore_sex", "cute_sex"):
            if girl.has_trait(t):
                return t
        return "_default"

    # -----------------------------
    # SLOT TRANSFORM
    # -----------------------------
    def rcg_get_slot_transform(speed):
        slot_map = {0: rcg_slot_speed0, 1: rcg_slot_speed1, 2: rcg_slot_speed2, 3: rcg_slot_speed3, 4: rcg_slot_speed4}
        return slot_map.get(speed, slot_map[1])

    # Speed 4 (he cums inside) has no wobble: the slot's short fast bounces are the whole motion. It used to fall back to
    # the speed 1 wobble (a slow 2 s drop under 0.34 s bounces).
    def rcg_get_butt_transform(speed):
        butt_map = {0: rcg_butt_wobble_speed0, 1: rcg_butt_wobble_speed1, 2: rcg_butt_wobble_speed2, 3: rcg_butt_wobble_speed3, 4: rcg_butt_wobble_speed0}
        return butt_map.get(speed, butt_map[1])

    def rcg_get_butt_transform_arms2(speed):
        butt_map = {0: rcg_butt_wobble_arms2_speed0, 1: rcg_butt_wobble_arms2_speed1, 2: rcg_butt_wobble_arms2_speed2, 3: rcg_butt_wobble_arms2_speed3, 4: rcg_butt_wobble_arms2_speed0}
        return butt_map.get(speed, butt_map[1])

# -----------------------------
# RCG SLAP (butt spank hand)
# -----------------------------
transform rcg_slap_right_in:
    subpixel True
    anchor (0.5, 0.5)
    xpos 1.3
    ypos 0.55
    alpha 1.0
    easein 0.08 xpos 0.55
    pause 0.15
    easeout 0.25 xpos -0.3 alpha 0.0

transform rcg_slap_left_in:
    subpixel True
    anchor (0.5, 0.5)
    xpos -0.3
    ypos 0.55
    alpha 1.0
    easein 0.08 xpos 0.45
    pause 0.15
    easeout 0.25 xpos 1.3 alpha 0.0

# -----------------------------
# RCG SLOT (CHARACTER MOVES)
# -----------------------------
transform rcg_slot_speed0:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 30

transform rcg_slot_speed1:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 90
    block:
        pause 0.35
        ease 0.20 yoffset 110
        pause 0.25
        ease 1.20 yoffset 90
        repeat

transform rcg_slot_speed2:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 90
    block:
        pause 0.22
        ease 0.16 yoffset 118
        pause 0.18
        easein 0.75 yoffset 90
        repeat

transform rcg_slot_speed3:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 90
    block:
        ease 0.20 yoffset 210
        easein 0.20 yoffset 90
        repeat

# Speed 4 = cumming inside: deepest position, short fast bounces
transform rcg_slot_speed4:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 135
    block:
        ease 0.17 yoffset 120
        easein 0.17 yoffset 135
        repeat

# -----------------------------
# PER-GIRL SLOT OFFSET
# -----------------------------
transform rcg_slot_rogue_offset:
    yoffset 35

# -----------------------------
# WOBBLE: the deeper drop on top of the slot, by speed (body AND butt: RCG_ApplySpeed puts it on both lists)
# -----------------------------
transform rcg_butt_wobble_speed0:
    yoffset 0

transform rcg_butt_wobble_speed1:
    yoffset 0
    block:
        pause 0.35
        ease 0.20 yoffset 36
        pause 0.25
        ease 1.20 yoffset 0
        repeat

transform rcg_butt_wobble_speed2:
    yoffset 0
    block:
        pause 0.22
        ease 0.16 yoffset 44
        pause 0.18
        easein 0.75 yoffset 0
        repeat

transform rcg_butt_wobble_speed3:
    yoffset 0
    block:
        ease 0.20 yoffset 96
        easein 0.20 yoffset 0
        repeat

# Arms 2: smooth, minimal body movement (clean ease, no pauses)
transform rcg_butt_wobble_arms2_speed0:
    yoffset 0

transform rcg_butt_wobble_arms2_speed1:
    yoffset 0
    block:
        ease 1.0 yoffset 6
        ease 1.0 yoffset 0
        repeat

transform rcg_butt_wobble_arms2_speed2:
    yoffset 0
    block:
        ease 0.655 yoffset 8
        ease 0.655 yoffset 0
        repeat

transform rcg_butt_wobble_arms2_speed3:
    yoffset 0
    block:
        ease 0.20 yoffset 16
        ease 0.20 yoffset 0
        repeat

# (the butt's squash on the landing: rcg_butt_land, LIFE section below; it replaced a stretch from the top-left
# corner of the layer that had no pivot)

# -----------------------------
# PENIS MOVEMENT (PRIMARY)
# -----------------------------
transform rcg_penis_speed0:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    xoffset 0
    yoffset 185

transform rcg_penis_speed1:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    xoffset 0
    yoffset 154
    block:
        pause 0.35
        ease 0.20 yoffset 132
        pause 0.25
        ease 1.20 yoffset 154
        repeat

transform rcg_penis_speed2:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    xoffset 0
    yoffset 156
    block:
        pause 0.22
        ease 0.16 yoffset 126
        pause 0.18
        easein 0.75 yoffset 156
        repeat

transform rcg_penis_speed3:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    xoffset 0
    yoffset 158
    block:
        ease 0.20 yoffset 88
        easein 0.20 yoffset 158
        repeat

# Arms 2: penis with more Y range (smooth, dominant movement)
transform rcg_penis_arms2_speed1:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    xoffset 0
    yoffset 154
    block:
        ease 1.0 yoffset 110
        ease 1.0 yoffset 154
        repeat

transform rcg_penis_arms2_speed2:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    xoffset 0
    yoffset 156
    block:
        ease 0.655 yoffset 100
        ease 0.655 yoffset 156
        repeat

# Speed 4 = cumming inside: deep, short fast thrusts
transform rcg_penis_speed4:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    xoffset 0
    yoffset 80
    block:
        ease 0.17 yoffset 60
        easein 0.17 yoffset 80
        repeat

transform rcg_penis_arms2_speed3:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    xoffset 0
    yoffset 158
    block:
        ease 0.20 yoffset 58
        ease 0.20 yoffset 158
        repeat

# -----------------------------
# LIFE: breathing (him or her), her body on the ride, his body under her
# -----------------------------
# Pivots are px of the 1920 x 1080 art. These transforms go LAST in a layer's at_list: they turn and zoom the art
# around the pivot and the offsets of the transforms before them (slot, wobble, per-girl offset) still add.
#
# Breathing (rcg_breath): a slow swell and a small shift of weight, both around the pivot. His body in an RCG that
# draws him (today Shion's "Guy", around his hips), and her body while she is still (around her waist).
transform rcg_breath(pivot, breath, zx, zy, sway, deg):
    subpixel True
    transform_anchor True
    anchor pivot pos pivot
    xzoom 1.0 yzoom 1.0 rotate 0
    parallel:
        block:
            ease breath * 0.42 xzoom zx yzoom zy
            ease breath * 0.58 xzoom 1.0 yzoom 1.0
            repeat
    parallel:
        block:
            ease sway * 0.25 rotate deg
            ease sway * 0.50 rotate -deg
            ease sway * 0.25 rotate 0
            repeat

# His body under her: he never rises or drops on his own. He breathes (calm while she is still, faster and deeper with
# the pace) around his hips (pivot = where the penis sits on his body, so the penis never slides on him), and while she
# rides her landing presses him into the bed a few px, with the timing of her ride (ease 35% down, hold 10%, ease 55%
# back). rcg_player_body_at builds the at_lists.
transform rcg_player_breath_press(pivot, breath, zx, zy, sway, deg, period, press):
    subpixel True
    transform_anchor True
    anchor pivot pos pivot
    xzoom 1.0 yzoom 1.0 rotate 0 yoffset 0
    parallel:
        block:
            ease breath * 0.42 xzoom zx yzoom zy
            ease breath * 0.58 xzoom 1.0 yzoom 1.0
            repeat
    parallel:
        block:
            ease sway * 0.25 rotate deg
            ease sway * 0.50 rotate -deg
            ease sway * 0.25 rotate 0
            repeat
    parallel:
        block:
            ease period * 0.35 yoffset press
            pause period * 0.10
            ease period * 0.55 yoffset 0
            repeat

# the penis goes down with his hips when she lands (it does not breathe: the pivot is its base)
transform rcg_player_press(period, press):
    subpixel True
    yoffset 0
    block:
        ease period * 0.35 yoffset press
        pause period * 0.10
        ease period * 0.55 yoffset 0
        repeat

# Her body on the ride (girls drawn as one body image + butt layers: Gwen, Rogue, Negasonic; Shion has her own).
# On top of the slot / wobble drops (the ride itself, unchanged) and in step with them (RCG_RIDE_PHASES = the slot's
# timing per speed: the pause before the first drop, the drop, the hold at the bottom, the rise, the pause before the
# next drop). Her upper body (everything on slot_at_list) settles around her waist at each landing (the head dips like
# a nod) and leans to one side, then the other, on alternate landings ...
transform rcg_body_ride(pivot, lead, down, hold, up, rest, sx, sy, deg):
    subpixel True
    transform_anchor True
    anchor pivot pos pivot
    xzoom 1.0 yzoom 1.0 rotate 0
    pause lead
    parallel:
        block:
            ease down xzoom sx yzoom sy
            pause hold
            ease up xzoom 1.0 yzoom 1.0
            pause rest
            repeat
    parallel:
        block:
            ease down rotate deg
            pause hold
            ease up rotate 0
            pause rest
            ease down rotate -deg
            pause hold
            ease up rotate 0
            pause rest
            repeat

# ... and her butt (everything on butt_detail_at_list) squashes on the landing around the penetration point (wider and
# flatter), springs back past rest as she rises, then settles: the hole stays on the penis.
transform rcg_butt_land(pivot, lead, down, hold, up, rest, sx, sy):
    subpixel True
    transform_anchor True
    anchor pivot pos pivot
    xzoom 1.0 yzoom 1.0
    pause lead
    block:
        ease down xzoom sx yzoom sy
        pause hold
        ease up * 0.35 xzoom (2.0 - sx) yzoom (2.0 - sy)
        ease up * 0.65 xzoom 1.0 yzoom 1.0
        pause rest
        repeat

init python:
    # His breathing in any scene that draws his body (this RCG, Shion's cowgirl): speed -> (seconds per breath, xzoom
    # and yzoom at the top of the breath), calm at rest, panting while he cums; and his weight shifting
    PLAYER_BREATH = {
        0: (3.6, 1.010, 1.020),
        1: (3.2, 1.010, 1.020),
        2: (2.5, 1.012, 1.024),
        3: (1.6, 1.014, 1.028),
        4: (1.1, 1.018, 1.034),
    }
    PLAYER_SWAY = (7.0, 0.35)                    # (seconds per sway, degrees each side)
    RCG_PLAYER_PRESS = {1: 2, 2: 3, 3: 4, 4: 3}  # px her landing presses him into the bed, by speed

    def rcg_player_body_at(speed, pivot, ride=None):
        """at_lists {"body", "penis"} of his body in an RCG that draws it. pivot = the base of the penis on his body
        (px of the 1920 x 1080 layer); ride = (period s, drop px) of her ride, None while she is still (the penis
        stays put then)."""
        _breath, _zx, _zy = PLAYER_BREATH.get(speed, PLAYER_BREATH[0])
        _sway, _deg = PLAYER_SWAY
        _press = RCG_PLAYER_PRESS.get(speed, 0)
        if ride and _press:
            return {"body": [rcg_player_breath_press(pivot, _breath, _zx, _zy, _sway, _deg, ride[0], _press)],
                    "penis": [rcg_player_press(ride[0], _press)]}
        return {"body": [rcg_breath(pivot, _breath, _zx, _zy, _sway, _deg)], "penis": []}

    # Her life on the ride. The slot's timing per speed (rcg_slot_speedN): (pause before the first drop, drop, hold at
    # the bottom, rise, pause before the next drop). Speed 4 starts at the bottom and rises first.
    RCG_RIDE_PHASES = {
        1: (0.35, 0.20, 0.25, 1.20, 0.35),
        2: (0.22, 0.16, 0.18, 0.75, 0.22),
        3: (0.00, 0.20, 0.00, 0.20, 0.00),
        4: (0.17, 0.17, 0.00, 0.17, 0.00),
    }
    # speed -> (her upper body at the landing: xzoom, yzoom, lean in degrees; her butt at the landing: xzoom, yzoom)
    RCG_RIDE_LIFE = {
        1: (1.003, 0.990, 0.6, 1.012, 0.988),
        2: (1.004, 0.986, 0.8, 1.016, 0.984),
        3: (1.006, 0.980, 0.5, 1.024, 0.976),
        4: (1.004, 0.988, 0.3, 1.016, 0.984),
    }
    # her breathing while she is still (speed 0): (seconds per breath, xzoom, yzoom, seconds per sway, degrees)
    RCG_GIRL_BREATH = (3.4, 1.004, 1.008, 8.0, 0.25)
    # Pivots on her art (px): her waist, where the back meets the butt, and the penetration point. Measured on Gwen,
    # Rogue and Negasonic (2026-10-06: the same template, body 984-1339 x 260-682, the hole at 1160 x 790-800); a girl
    # drawn elsewhere sets "life_waist" / "life_seat" in GIRL_SCENE_CONFIG "rcg".
    RCG_LIFE_WAIST = (1161, 620)
    RCG_LIFE_SEAT = (1160, 800)

    def rcg_girl_life_at(girl, speed):
        """at_lists {"body", "butt"} of her life on the ride, to go LAST in her layers' lists. Nothing in arms pose 2:
        her hands are on her butt (the arms join the body to the butt) and that pose is kept minimal on purpose."""
        if getattr(store, "rcg_arms_pose", 1) == 2:
            return {"body": [], "butt": []}
        _waist = _gsc(girl.gid, "life_waist", RCG_LIFE_WAIST, "rcg")
        if speed not in RCG_RIDE_LIFE:
            _breath, _zx, _zy, _sway, _deg = RCG_GIRL_BREATH
            return {"body": [rcg_breath(_waist, _breath, _zx, _zy, _sway, _deg)], "butt": []}
        _seat = _gsc(girl.gid, "life_seat", RCG_LIFE_SEAT, "rcg")
        _lead, _down, _hold, _up, _rest = RCG_RIDE_PHASES[speed]
        _bx, _by, _deg, _sx, _sy = RCG_RIDE_LIFE[speed]
        return {"body": [rcg_body_ride(_waist, _lead, _down, _hold, _up, _rest, _bx, _by, _deg)],
                "butt": [rcg_butt_land(_seat, _lead, _down, _hold, _up, _rest, _sx, _sy)]}

# -----------------------------
# CLOTHING GUARD
# -----------------------------
label ensure_bottomless(girl, pose=None):
    # Only strips items still at "full" state. Displaced items are kept.
    if pose is None:
        $ pose = sprite_state.get(girl.Id, {}).get("pose") or getattr(girl, "default_pose", "standing")
    python:
        _need_strip = False
        if girl.Legs is not None and girl.clothes_state.get("skirt") == "full":
            _need_strip = True
        if girl.Panties is not None and girl.clothes_state.get("panties") == "full":
            _need_strip = True
    if _need_strip:
        call _rcg_bottom_clothes_menu(girl) from _call_rcg_bottom_menu_ensure
    return

# =============================================================
# RCG_RefreshClothing — ONE function for ALL clothing updates
# Call this after changing any clothes data in RCG.
# In scene: calls ApplySpeed (updates all standalones + layeredimage)
# Static:   calls set_girl_sprite (updates layeredimage only)
# =============================================================
label RCG_RefreshClothing(girl):
    $ debug_log("[PANTIES] RefreshClothing: Panties=%s state=%s started=%s rub=%s" % (girl.Panties, girl.clothes_state.get("panties"), getattr(store, "rcg_started", False), getattr(store, "rcg_rub_mode", False)))
    # Always use ApplySpeed to refresh standalones (skirt, panties, etc.)
    $ _dg_ref_speed = rcg_speed if (getattr(store, "rcg_started", False) or getattr(store, "rcg_rub_mode", False) or getattr(store, "rcg_tip_mode", False)) else 0
    call RCG_ApplySpeed(girl, _dg_ref_speed) from _call_RCG_ApplySpeed_refresh
    return

# ============================================================
# Apply speed
# ============================================================
label RCG_ApplySpeed(girl, speed=1):
    # he is in her ass: it happened this session (her anus gapes once he is out of it, in the layers that draw that)
    if store.rcg_started and store.rcg_anal:
        $ store._rcg_had_anal = True

    if girl.gid == "shion":
        $ _srcg_apply_speed(girl, speed)
        return

    $ penis_img = "%s rcg_penis" % girl.gid
    $ debug_log("[DEBUG] RCG_ApplySpeed: speed=%s rub_mode=%s started=%s" % (speed, store.rcg_rub_mode, store.rcg_started))

    python:
        if not store.rcg_started:
            store.rcg_butt_state = "butt_top_1"
        elif speed >= 3:  # includes speed 4 (cumming)
            store.rcg_butt_state = "butt_top_3"
        else:
            store.rcg_butt_state = "butt_top_2"

        slot_transform = rcg_get_slot_transform(speed)
        butt_transform = rcg_get_butt_transform(speed)
        # her life on the ride (rcg_girl_life_at): last in the lists, around her waist / the penetration point
        _life = rcg_girl_life_at(girl, speed)
        if "_build_rcg_attributes" in globals():
            attrs = _build_rcg_attributes(girl)
        else:
            attrs = _build_attributes_for_girl(girl, pose="reverse_cowgirl")
        img_name = "%s rcg" % girl.gid
        if attrs:
            img_name += " " + " ".join(attrs)

        # Arms 2: body/butt use reduced wobble, penis keeps full speed
        if store.rcg_arms_pose == 2:
            _butt_tf_body = rcg_get_butt_transform_arms2(speed)
        else:
            _butt_tf_body = butt_transform
        _rcg_offset = _gsc(girl.gid, "slot_offset", None, "rcg")

        # Her body drops WITH her butt (slot + the same wobble): with the body on the slot alone the butt dropped up to
        # 96 px more (speed 3) and uncovered the bottom of the body art (the cut above the butt shows from ~24 px).
        # What differs between them is only her life on the ride (the settle / lean of the body, the squash of the butt).
        slot_at_list = [slot_transform, _butt_tf_body]
        if _rcg_offset:
            slot_at_list.append(getattr(store, _rcg_offset))
        slot_at_list = slot_at_list + _life["body"]

        butt_at_list = [slot_transform, _butt_tf_body]
        if _rcg_offset:
            butt_at_list.append(getattr(store, _rcg_offset))

        renpy.show(
            img_name,
            tag=girl.gid,
            at_list=slot_at_list,
            zorder=9980
        )

        if store.rcg_arms_pose == 2:
            _arms2_ls = "%s rcg_arms_ls_2" % girl.gid
            _arms2_img = _arms2_ls if girl.Over and renpy.has_image(_arms2_ls, exact=True) else "%s rcg_arms_2" % girl.gid
            renpy.show(
                _arms2_img,
                tag="rcg_arms2",
                at_list=slot_at_list,
                zorder=10050
            )
            renpy.hide("rcg_arms1_over")
        else:
            renpy.hide("rcg_arms2")
            _arms1_ls = "%s rcg_arms_ls_1" % girl.gid
            if girl.Over and renpy.has_image(_arms1_ls, exact=True):
                renpy.show(
                    _arms1_ls,
                    tag="rcg_arms1_over",
                    at_list=slot_at_list,
                    zorder=10050
                )
            else:
                renpy.hide("rcg_arms1_over")

        # Crop top upper half (Rogue only) — standalone above arms
        _crop_top_img = "%s rcg_crop_top" % girl.gid
        _chest_at = slot_at_list
        if renpy.has_image(_crop_top_img, exact=True) and "torso_chest_corset" in attrs:
            renpy.show(
                _crop_top_img,
                tag="rcg_crop_top",
                at_list=_chest_at,
                zorder=10051
            )
        else:
            renpy.hide("rcg_crop_top")

        # Bikini top upper half — standalone above arms (same pattern as crop_top)
        _bikini_top_img = "%s rcg_bikini_top" % girl.gid
        if renpy.has_image(_bikini_top_img, exact=True) and "torso_chest_bikini_top" in attrs:
            renpy.show(
                _bikini_top_img,
                tag="rcg_bikini_top",
                at_list=_chest_at,
                zorder=10051
            )
        else:
            renpy.hide("rcg_bikini_top")

        butt_detail_at_list = butt_at_list + _life["butt"]

        # Standalone layers — FIXED zorders, never change based on clothing.
        # Adding/removing panties or skirt only shows/hides THAT layer.
        #
        # Order (bottom to top):
        #   butt_gap    9960
        #   thigh_highs 9968
        #   layeredimage 9980  (body, arms, butt_safe, torso clothes, head, expressions)
        #   butt_top    10005
        #   panties     10006  (just a layer on top — show/hide only)
        #   skirt       10007  (just a layer on top — show/hide only)
        #   blush       10008

        _butt_gap_z = 9960
        renpy.show(
            "%s rcg_butt_gap" % girl.gid,
            tag="rcg_butt_gap",
            at_list=butt_detail_at_list,
            zorder=_butt_gap_z,
        )

        if getattr(girl, "Shoes", None):
            renpy.show(
                "%s rcg_thigh_highs" % girl.gid,
                tag="rcg_thigh_highs",
                at_list=butt_detail_at_list,
                zorder=9968,
            )
        else:
            renpy.hide("rcg_thigh_highs")

        butt_img_map = {
            "butt_top_1": "%s rcg_butt_top_1" % girl.gid,
            "butt_top_2": "%s rcg_butt_top_2" % girl.gid,
            "butt_top_3": "%s rcg_butt_top_3" % girl.gid,
        }
        butt_img = butt_img_map.get(store.rcg_butt_state)
        if butt_img:
            renpy.show(
                butt_img,
                tag="rcg_butt_top",
                at_list=butt_detail_at_list,
                zorder=10005,
            )
        else:
            renpy.hide("rcg_butt_top")

        # Panties standalone (just show/hide, nothing else changes)
        # zorder: full/side1 above butt_top (10006), side2/down behind penis (9970)
        if not store.rcg_rub_mode:
            _pan_item = girl.Panties
            _pan_state = girl.clothes_state.get("panties", "full")
            debug_log("[PANTIES] ApplySpeed: item=%s state=%s rub=%s started=%s" % (_pan_item, _pan_state, store.rcg_rub_mode, store.rcg_started))
            if _pan_item:
                _pan_img = "%s rcg_panties_%s_%s" % (girl.gid, _pan_item, _pan_state)
                _pan_z = 9969 if _pan_state == "down" else 10006
                debug_log("[PANTIES] Showing standalone: %s at zorder %s" % (_pan_img, _pan_z))
                renpy.show(
                    _pan_img,
                    tag="rcg_panties",
                    at_list=butt_detail_at_list,
                    zorder=_pan_z,
                )
                # Side state: side2 — above butt(10005) when idle, below penis(9970) when active
                _pan_img2 = "%s rcg_panties_%s_side2" % (girl.gid, _pan_item)
                if _pan_state == "side" and renpy.has_image(_pan_img2, exact=True):
                    _pan2_z = 9969 if speed >= 1 else 10006
                    renpy.show(
                        _pan_img2,
                        tag="rcg_panties2",
                        at_list=butt_detail_at_list,
                        zorder=_pan2_z,
                    )
                else:
                    renpy.hide("rcg_panties2")
                # Side state: bottom part — above butt(10005) when idle, below penis(9970) when active
                _pan_side_bottom = "%s rcg_panties_%s_side_bottom" % (girl.gid, _pan_item)
                if _pan_state == "side" and renpy.has_image(_pan_side_bottom):
                    _psb_z = 9969 if speed >= 1 else 10006
                    renpy.show(
                        _pan_side_bottom,
                        tag="rcg_panties_side_bottom",
                        at_list=butt_detail_at_list,
                        zorder=_psb_z,
                    )
                else:
                    renpy.hide("rcg_panties_side_bottom")
            else:
                debug_log("[PANTIES] No panties, hiding standalone")
                renpy.hide("rcg_panties")
                renpy.hide("rcg_panties2")
                renpy.hide("rcg_panties_side_bottom")

        # Skirt standalone (just show/hide, nothing else changes)
        if girl.Legs:
            _skirt_state = girl.clothes_state.get("skirt", "full")
            _skirt_tag = "rcg_skirt_up" if _skirt_state == "up" else "rcg_skirt"
            renpy.show(
                "%s %s" % (girl.gid, _skirt_tag),
                tag="rcg_skirt",
                at_list=butt_detail_at_list,
                zorder=10007,
            )
        else:
            renpy.hide("rcg_skirt")

        # Over standalone: butt_clothed above butt layers (visible whenever over is equipped)
        if girl.Over:
            _rcg_butt_clothed = "%s rcg_butt_clothed" % girl.gid
            if renpy.has_image(_rcg_butt_clothed, exact=True):
                renpy.show(_rcg_butt_clothed, tag="rcg_butt_clothed", at_list=butt_detail_at_list, zorder=10008)
            else:
                renpy.hide("rcg_butt_clothed")
        else:
            renpy.hide("rcg_butt_clothed")

        # Butt blush (above butt_top 10005, below skirt 10007)
        renpy.show(
            "%s rcg_butt_blush" % girl.gid,
            tag="rcg_butt_blush",
            at_list=butt_detail_at_list,
            zorder=10006,
        )

        # Rub mode: override layer order above everything
        # Order: butt_gap(9960) < butt_top_1(10054) < blush(10055) < panties(10056) < skirt(10057) < grab(10059) < rub_top(10060)
        if store.rcg_rub_mode:
            if not store.rcg_started:
                renpy.show(
                    "%s rcg_butt_top_1" % girl.gid,
                    tag="rcg_butt_top",
                    at_list=butt_detail_at_list,
                    zorder=10054,
                )

            # Butt blush above butt_top but below clothes
            renpy.show(
                "%s rcg_butt_blush" % girl.gid,
                tag="rcg_butt_blush",
                at_list=butt_detail_at_list,
                zorder=10055,
            )

            # Panties above blush
            if girl.Panties:
                _rpan_state = girl.clothes_state.get("panties", "full")
                _rpan_img = "%s rcg_panties_%s_%s" % (girl.gid, girl.Panties, _rpan_state)
                renpy.show(
                    _rpan_img,
                    tag="rcg_panties",
                    at_list=butt_detail_at_list,
                    zorder=10056,
                )
                # Side bottom: below rub_top(10060), below panties_top(10056)
                _rpan_side_bottom = "%s rcg_panties_%s_side_bottom" % (girl.gid, girl.Panties)
                if _rpan_state == "side" and renpy.has_image(_rpan_side_bottom):
                    renpy.show(
                        _rpan_side_bottom,
                        tag="rcg_panties_side_bottom",
                        at_list=butt_detail_at_list,
                        zorder=10055,
                    )
                else:
                    renpy.hide("rcg_panties_side_bottom")
                # Side2 (bikini equivalent of side_bottom)
                _rpan_side2 = "%s rcg_panties_%s_side2" % (girl.gid, girl.Panties)
                if _rpan_state == "side" and renpy.has_image(_rpan_side2, exact=True):
                    renpy.show(
                        _rpan_side2,
                        tag="rcg_panties2",
                        at_list=butt_detail_at_list,
                        zorder=10055,
                    )
                else:
                    renpy.hide("rcg_panties2")
            else:
                renpy.hide("rcg_panties")
                renpy.hide("rcg_panties_side_bottom")
                renpy.hide("rcg_panties2")

            # Skirt above panties
            if girl.Legs:
                _rub_skirt_state = girl.clothes_state.get("skirt", "full")
                _rub_skirt_tag = "rcg_skirt_up" if _rub_skirt_state == "up" else "rcg_skirt"
                renpy.show(
                    "%s %s" % (girl.gid, _rub_skirt_tag),
                    tag="rcg_skirt",
                    at_list=butt_detail_at_list,
                    zorder=10057,
                )

            # Over butt_clothed above skirt, below grab
            if girl.Over:
                _rcg_butt_clothed = "%s rcg_butt_clothed" % girl.gid
                if renpy.has_image(_rcg_butt_clothed, exact=True):
                    renpy.show(_rcg_butt_clothed, tag="rcg_butt_clothed", at_list=butt_detail_at_list, zorder=10058)

            # Grab above blush (left/right independent)
            _hand_disabled = getattr(store, "_player_hand_disabled", None)
            _slap_hide = getattr(store, "_slap_hide_hand", None)
            if store.rcg_grab:
                _gb_left = "%s rcg_grab_butt_left" % girl.gid
                if renpy.has_image(_gb_left):
                    for _side in ("left", "right"):
                        _gb_img = "%s rcg_grab_butt_%s" % (girl.gid, _side)
                        _gb_tag = "rcg_grab_%s" % _side
                        if _hand_disabled != _side and _slap_hide != _side and renpy.has_image(_gb_img):
                            renpy.show(_gb_img, tag=_gb_tag, at_list=butt_detail_at_list, zorder=10059)
                        else:
                            renpy.hide(_gb_tag)
                else:
                    _gb_img = "%s rcg_grab_butt" % girl.gid
                    if renpy.has_image(_gb_img):
                        renpy.show(_gb_img, tag="rcg_grab_left", at_list=butt_detail_at_list, zorder=10059)
                    renpy.hide("rcg_grab_right")
            else:
                renpy.hide("rcg_grab_left")
                renpy.hide("rcg_grab_right")

            # Rub top at max
            renpy.show(
                "%s rcg_rub_top" % girl.gid,
                tag="rcg_rub_top",
                at_list=butt_detail_at_list,
                zorder=10060,
            )
        else:
            renpy.hide("rcg_rub_top")

            # Normal mode grab (left/right independent)
            _hand_disabled = getattr(store, "_player_hand_disabled", None)
            _slap_hide = getattr(store, "_slap_hide_hand", None)
            if store.rcg_grab:
                _gb_left = "%s rcg_grab_butt_left" % girl.gid
                if renpy.has_image(_gb_left):
                    for _side in ("left", "right"):
                        _gb_img = "%s rcg_grab_butt_%s" % (girl.gid, _side)
                        _gb_tag = "rcg_grab_%s" % _side
                        if _hand_disabled != _side and _slap_hide != _side and renpy.has_image(_gb_img):
                            renpy.show(_gb_img, tag=_gb_tag, at_list=butt_detail_at_list, zorder=10050)
                        else:
                            renpy.hide(_gb_tag)
                else:
                    _gb_img = "%s rcg_grab_butt" % girl.gid
                    if renpy.has_image(_gb_img):
                        renpy.show(_gb_img, tag="rcg_grab_left", at_list=butt_detail_at_list, zorder=10050)
                    renpy.hide("rcg_grab_right")
            else:
                renpy.hide("rcg_grab_left")
                renpy.hide("rcg_grab_right")

        # Butt cum (on her ass, above clothes, follows butt movement)
        renpy.show(
            "%s rcg_butt_cum" % girl.gid,
            tag="rcg_butt_cum",
            at_list=butt_detail_at_list,
            zorder=10050,
        )

        # Back cum (on her back, above clothes, follows body slot)
        renpy.show(
            "%s rcg_back_cum" % girl.gid,
            tag="rcg_back_cum",
            at_list=slot_at_list,
            zorder=10051,
        )

        # Face cum (follows body slot, hidden when hiding_face via ConditionSwitch)
        renpy.show(
            "%s rcg_cum_face" % girl.gid,
            tag="rcg_cum_face",
            at_list=slot_at_list,
            zorder=10053,
        )

        # Dripping cum: below penis (9970 < 9975), visible during the act too
        if not store.rcg_rub_mode:
            renpy.show(
                "%s rcg_dripping_cum" % girl.gid,
                tag="rcg_dripping_cum",
                at_list=butt_detail_at_list,
                zorder=9970,
            )
        else:
            renpy.hide("rcg_dripping_cum")

    python:
        if speed <= 0:
            renpy.hide("rcg_penis")
            renpy.hide("rcg_condom")
            renpy.hide("rcg_penis_cum")
        else:
            if speed == 4:
                _penis_tf = rcg_penis_speed4
            elif store.rcg_arms_pose == 2:
                _penis_map = {1: rcg_penis_arms2_speed1, 2: rcg_penis_arms2_speed2, 3: rcg_penis_arms2_speed3}
                _penis_tf = _penis_map.get(speed, _penis_map[1])
            else:
                _penis_map = {1: rcg_penis_speed1, 2: rcg_penis_speed2, 3: rcg_penis_speed3}
                _penis_tf = _penis_map.get(speed, _penis_map[1])

            _penis_at = [_penis_tf]
            _rcg_p_offset = _gsc(girl.gid, "slot_offset", None, "rcg")
            if _rcg_p_offset:
                _penis_at.append(getattr(store, _rcg_p_offset))

            # Penis above butt_gap, below butt_top. Rub mode above everything.
            _penis_z = 10060 if store.rcg_rub_mode else 9970
            renpy.show(penis_img, tag="rcg_penis", at_list=_penis_at, zorder=_penis_z)
            if store.condom_active:
                _rcg_condom_img = _condom_img_tag("rcg_condom")
                renpy.show(_rcg_condom_img, tag="rcg_condom", at_list=_penis_at, zorder=_penis_z)

            # Penis cum (after cum inside, follows penis movement)
            if not store.rcg_rub_mode:
                renpy.show(
                    "%s rcg_penis_cum" % girl.gid,
                    tag="rcg_penis_cum",
                    at_list=_penis_at,
                    zorder=9974,
                )

        if not store.condom_active:
            renpy.hide("rcg_condom")

    return

# ============================================================
# Launch
# ============================================================
label RCG_Launch(girl, from_switch=False):
    $ debug_log("[DEBUG] RCG_Launch: entered, from_switch=%s" % str(from_switch))
    $ _kill_scene_threads(keep_watchers=from_switch)
    $ stop_standing_blink(girl)

    if not from_switch:
        $ public_attention_reset()
        call PlayerExposure(girl) from _call_PlayerExposure_2

    $ girl._prev_pose = getattr(girl, "default_pose", "standing")
    $ girl._prev_slot = getattr(girl, "SpriteLoc", StageCenter)
    if not getattr(girl, "_saved_outfit", None):
        $ girl.SaveOutfit()

    python:
        # Clear other scene refs so set_scene_expression doesn't cross-contaminate
        _clear_scene_refs("rcg")
        store.cowgirl_started = False
        store.cowgirl_masturbating = False
        store.doggy_started = False
        _hide_all_scene_layers(girl)

        _hide_non_scene_girls(girl)

        # Her standing sprite: a pose drawn under her own tag replaces it, layers with tags of their own (Shion's
        # srcg_*) do not, and an End right before this (her position switch, the mouth finish) re-showed it
        # (scene_full_cleanup ResetVisuals). Hidden for every girl, as RCG_RubLaunch does
        hide_girl_sprite(girl)

        store._rcg_girl = girl
        sprite_state.setdefault(girl.Id, {})["pose"] = "reverse_cowgirl"
        store.rcg_started = False
        store.rcg_butt_state = "butt_top_1"
        store.rcg_arms_pose = 1
        store.rcg_grab = False
        store.rcg_hold = False
        store.rcg_rub_mode = False
        store.rcg_tip_mode = False
        store.hiding_face = False
        store._rcg_escalated = False
        # rcg_anal is NOT reset here: the caller set it just before (start_scene, a switch that carries the hole
        # over). Only a girl whose art has it can keep it. What already happened this session stays on a switch.
        if not rcg_has_anal(girl):
            store.rcg_anal = False
        if not from_switch:
            store._rcg_had_anal = False
        print("[RCG_LAUNCH] %s from_switch=%s anal=%s had_anal=%s" % (girl.gid, from_switch, store.rcg_anal, store._rcg_had_anal))

        # Shion custom RCG: set her scene ref
        if girl.gid == "shion":
            store._srcg_girl = girl

        # Auto-strip items that don't support RCG pose
        _gid = getattr(girl, "gid", getattr(girl, "Id", ""))
        _reg = CLOTHING_REGISTRY.get(_gid, {})
        for _slot_name, _slot_attr, _oc_param in [("over", "Over", "over"), ("chest", "Chest", "chest"), ("skirt", "Legs", "legs")]:
            _item = getattr(girl, _slot_attr, None)
            if not _item:
                _item = girl.clothes.get(_slot_name if _slot_name != "chest" else "chest")
            if _item:
                _item_cfg = _reg.get(_item, {})
                if "reverse_cowgirl" not in _item_cfg.get("poses", {}):
                    girl.Outfit_Change(**{_oc_param: "none"}, refresh=False)

    # Strip over for sex (keep for massage/sunscreen only)
    if girl.Over:
        $ _over_line = renpy.random.choice([_("I need to take this off first..."), _("Let me get this out of the way..."), _("Hold on, let me take this off.")])
        $ Say_Line(girl, _over_line)
        $ girl.Outfit_Change(over="none", pose="reverse_cowgirl")

    if "rcg_speed" not in globals():
        $ rcg_speed = 0

    $ sub_event_reset(girl)

    if from_switch:
        # Reset skirt state from previous position so rcg_skirt_up doesn't carry over
        if girl.clothes_state.get("skirt") == "up":
            $ girl.clothes_state["skirt"] = "full"
        # Coming from another position: strip remaining panties, skip menu
        if girl.Panties is not None:
            $ girl.Outfit_Change(panties="none", pose="reverse_cowgirl")
        if _rcg_sex_nude_needed(girl):
            $ girl.Outfit_Change(over="none", mid="none", chest="none", legs="none", pose="reverse_cowgirl")
            $ print("[RCG_NUDE] %s stripped on the switch into the pose" % girl.gid)
        call RCG_ApplySpeed(girl, 0) from _call_RCG_ApplySpeed_sw1
        with dissolve
    else:
        # Show RCG pose with clothes at speed 0 (static idle, proper z-orders)
        call RCG_ApplySpeed(girl, 0) from _call_RCG_ApplySpeed_launch_static
        with fade

        # --- BOTTOM CLOTHES MENU (skirt then panties) ---
        # Exposure (saw_pussy) is handled inside the menu.
        call _rcg_bottom_clothes_menu(girl) from _call_rcg_bottom_menu_launch

    # Start blink + expression threads
    python:
        if girl.gid == "shion":
            renpy.invoke_in_thread(_scene_cs_blink_loop, girl, "_rcg_girl", is_active_fn=_rcg_is_active)
        else:
            renpy.invoke_in_thread(_scene_blink_loop, girl, "_rcg_girl", "rcg_blink", is_active_fn=_rcg_is_active, cs_girls=_rcg_cs_girls())
        renpy.invoke_in_thread(_rcg_expression_cycle, girl)
    return

# ============================================================
# Control Menu
# ============================================================
label RCG_ControlMenu(girl):

    $ store._scene_phase = "sex"
    if "rcg_speed" not in globals():
        $ rcg_speed = 1

    # Reset position switch flag on entry (prevents premature exit from rub/tip escalation)
    $ store._sub_event_position_switched = False

    # Track highest act for afterscene detection
    $ store._cheat_shower_max_act = "sex"

    $ store._player_exhausted = False

    while True:
        # the scene's type right now: "reverse_cowgirl", or its anal variant while he is in her ass (rcg_scene_type)
        $ _rcg_scene = rcg_scene_type()
        $ debug_log("[DEBUG] RCG_ControlMenu: top of while loop, scene=%s speed=%s exhausted=%s pos_switch=%s" % (_rcg_scene, str(rcg_speed), store._player_exhausted, getattr(store, "_sub_event_position_switched", False)))

        if _scene_should_exit():
            $ debug_log("[DEBUG] RCG_ControlMenu: EXIT - _scene_should_exit()")
            return

        # Position-switch escape: if a sub-event switched us here, return
        if store._sub_event_position_switched:
            $ debug_log("[DEBUG] RCG_ControlMenu: EXIT - position_switched")
            $ store._sub_event_position_switched = False
            return

        if Round >= 100:
            $ Say_Line(girl, _scene_time_up_line())
            call RCG_End(girl, dress_up=False) from _call_RCG_End_timeout
            return

        menu:
            "Keep going" if rcg_speed >= 1:
                $ debug_log("[DEBUG] RCG_ControlMenu: chose KEEP GOING")
                # in her ass her Lust follows the anal rules (anal_lover / anal_hater), like every anal position
                $ _rcg_lust = _anal_lust_for_speed(girl, rcg_speed) if store.rcg_anal else -1
                call _sex_scene_tick(girl, _rcg_scene, rcg_speed, girl_lust=_rcg_lust) from _call_sst_rcg_kg
                $ _apply_anal_lust_cap(girl, store.rcg_anal)

                if store._sst_result == "condom_ripped":
                    call RCG_CondomRemoveAnim(girl) from _call_RCG_CondomRemoveAnim_sst_kg
                    call RCG_ApplySpeed(girl, rcg_speed) from _call_RCG_ApplySpeed_sst_rip

                if store._sst_result == "abort":
                    # (the type is read again: her own anal request may have changed the hole during the tick)
                    if store._sst_abort_reason == "post_cum":
                        $ _set_post_cum(rcg_scene_type(), "sex")
                        return
                    call _sex_scene_handle_abort(girl, rcg_scene_type()) from _call_sst_abort_rcg_kg
                    return

            "Speed up" if rcg_speed < 3:
                $ advance_round(TIME_COSTS["sex_tick"])
                $ debug_log("[DEBUG] RCG_ControlMenu: chose SPEED UP")
                $ Say_Player(_("Faster..."))
                $ _was_idle = (rcg_speed == 0)
                if _was_idle and (girl.Legs is not None or girl.Panties is not None or _rcg_sex_nude_needed(girl)):
                    call _rcg_bottom_clothes_menu(girl) from _call_rcg_bottom_menu_speedup
                $ _rcg_first_entry = not rcg_started
                $ rcg_started = True
                $ rcg_speed += 1
                if _was_idle:
                    call RCG_PenisEnterAnim(girl) from _call_RCG_PenisEnterAnim_speedup
                # the ride is drawn before anyone speaks: no frame of the old pose between his entry and the ride
                call RCG_ApplySpeed(girl, rcg_speed) from _call_RCG_ApplySpeed_9
                if _rcg_first_entry and store.rcg_anal:
                    # he goes into her ass (a scene started for it: start_scene anal=True)
                    $ _watcher_scene_comment("anal_enter")
                call _speed_change_tick(girl, _rcg_scene, 1) from _call_sct_rcg_su
                if _scene_should_exit():
                    return
                if rcg_speed >= 3:
                    $ _watcher_scene_comment("speed_max")
                $ Narration(_("She speeds up her movements."))

            "Speed down" if rcg_speed > 0:
                $ advance_round(1)
                $ rcg_speed -= 1
                call RCG_ApplySpeed(girl, rcg_speed) from _call_RCG_ApplySpeed_10
                call _speed_change_tick(girl, _rcg_scene, -1) from _call_sct_rcg_sd
                if store._sub_event_position_switched:
                    return
                $ _watcher_scene_comment("speed_down")
                $ Narration(_("She slows her movements."))

            "{color=#fbbf24}Cum{/color}" if player_is_cumming():
                $ store._cum_menu_cancelled = False
                call PlayerCumMenu(girl, _rcg_scene) from _call_PlayerCumMenu_voluntary_rcg
                if not store._cum_menu_cancelled:
                    $ _handle_post_cum_exit(_rcg_scene, "sex")
                    return

            # The other hole, or back to the tip / the rub (escalation.rpy): only a girl whose art has anal in this
            # pose gets the menu here (the others reach rub / tip from their own menus, as before)
            "Penetration..." if rcg_started and rcg_has_anal(girl):
                $ _es_from = "anal" if store.rcg_anal else "sex"
                call _escalation_menu(girl, "reverse_cowgirl") from _call_esc_menu_rcg_sex
                if store._esc_result == "accepted":
                    call _rcg_esc_dispatch(girl, _es_from, rcg_speed) from _call_esc_disp_rcg_sex
                    # the dispatch may have ended the scene (a cheat path condom breakdown) or left for rub / tip
                    if store._esc_is_deescalation or store._rcg_girl is None:
                        $ debug_log("[RCG_LOOP] EXIT after escalation: deesc=%s scene_ended=%s" % (store._esc_is_deescalation, store._rcg_girl is None))
                        return
                elif store._esc_result == "scene_ended":
                    call RCG_End(girl, dress_up=False) from _call_RCG_End_esc_sex
                    return

            "Change her arms" if rcg_has_arms_change(girl):
                $ rcg_arms_pose = 2 if rcg_arms_pose == 1 else 1
                $ rcg_grab = False
                call RCG_ApplySpeed(girl, rcg_speed) from _call_RCG_ApplySpeed_arms

            "Grab her ass" if not rcg_grab and rcg_arms_pose != 2 and rcg_has_grab(girl):
                $ advance_round(1)
                $ rcg_grab = True
                call RCG_ApplySpeed(girl, rcg_speed) from _call_RCG_ApplySpeed_grab
                python:
                    _grab_react = renpy.random.choice(["mouth_surprised", "mouth_tongue", "mouth_kiss"])
                    set_scene_expression(girl, None, mouth=_grab_react)
                call RCG_ApplySpeed(girl, rcg_speed) from _call_RCG_ApplySpeed_grab_react

            "Let go" if rcg_grab:
                $ advance_round(1)
                $ rcg_grab = False
                call RCG_ApplySpeed(girl, rcg_speed) from _call_RCG_ApplySpeed_letgo

            # His hands on her thighs (a girl whose art has them: rcg_has_hold): she rides a shorter stroke, held deep
            "Hold her down" if not rcg_hold and rcg_has_hold(girl):
                $ advance_round(1)
                call RCG_Hold(girl, True) from _call_RCG_Hold_on

            "Let go of her" if rcg_hold and rcg_has_hold(girl):
                $ advance_round(1)
                call RCG_Hold(girl, False) from _call_RCG_Hold_off

            "Spank her" if rcg_arms_pose != 2:
                $ advance_round(1)
                call SpankHer(girl, _rcg_scene) from _call_SpankHer_rcg

            "Tell her to look forward" if rcg_has_hide_face(girl) and not store.hiding_face and not getattr(store, "_recording_active", False):
                call _rcg_turn_head(girl) from _call_rcg_turn_head_fwd
                call RCG_ApplySpeed(girl, rcg_speed) from _call_RCG_ApplySpeed_turn_fwd

            "Tell her to look back" if rcg_has_hide_face(girl) and store.hiding_face and not getattr(store, "_recording_active", False):
                $ store.hiding_face = False
                call RCG_ApplySpeed(girl, rcg_speed) from _call_RCG_ApplySpeed_turn_back
                $ _turn_txt = _tl(_("She turns her head back to face you."))
                $ Narration(_turn_txt)
                if store._stealth_condom_removed:
                    call StealthCondomDiscovery(girl, "reverse_cowgirl") from _call_StealthDisc_rcg_lookback

            "Tease her..." if rcg_speed > 0:
                $ advance_round(1)
                call _tease_menu(girl, _rcg_scene) from _call_tease_menu_rcg

            "Strip her" if not getattr(store, "_scene_restricted", False):
                $ advance_round(1)
                call RCG_StripMenu(girl) from _call_RCG_StripMenu

            "Record Options..." if not getattr(store, "_recording_active", False) or getattr(store, "_recording_girl", None) == girl:
                menu:
                    "Record her..." if not getattr(store, "_recording_active", False) and not store.hiding_face:
                        call _sex_phone_menu(girl, "reverse_cowgirl") from _call__sex_phone_menu_4
                    "Record her..." if not getattr(store, "_recording_active", False) and store.hiding_face:
                        call _sex_phone_menu(girl, "reverse_cowgirl") from _call__sex_phone_menu_4b
                    "Record without telling her" if not getattr(store, "_recording_active", False) and store.hiding_face:
                        call _rcg_secret_recording(girl) from _call_rcg_secret_recording
                    "Ask [store._ntr_watching_npc.Name] to record" if store._ntr_partner_watching and not getattr(store, "_recording_active", False):
                        call _watcher_record_start(girl, "reverse_cowgirl") from _call_watcher_rec_start_rcg_npc
                    "Ask [store._witness_girl.Name] to record" if getattr(store, "_witness_watching", False) and getattr(store, "_witness_girl", None) is not None and not store._ntr_partner_watching and not getattr(store, "_recording_active", False):
                        call _watcher_record_start(girl, "reverse_cowgirl") from _call_watcher_rec_start_rcg_girl
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
                        call _rcg_look_back_during_recording(girl) from _call_rcg_look_back_rec
                    "Back":
                        pass
                if store._rcg_secret_caught_end:
                    $ store._rcg_secret_caught_end = False
                    call RCG_End(girl, dress_up=False) from _call_RCG_End_secret_caught
                    return
                call RCG_ApplySpeed(girl, rcg_speed) from _call_RCG_ApplySpeed_rec_opts

            "Condom..." if store.condom_active:
                call CondomMidsceneMenu(girl, _rcg_scene) from _call_CondomMidsceneMenu_1
                if not store.condom_active:
                    call RCG_CondomRemoveAnim(girl) from _call_RCG_CondomRemoveAnim_mid
                    call RCG_ApplySpeed(girl, rcg_speed) from _call_RCG_ApplySpeed_11

            "Switch position..." if rcg_started and not getattr(store, "_scene_restricted", False):
                if store._condom_broken_hidden:
                    call CondomBreakDiscovery(girl, "reverse_cowgirl") from _call_CondomBreakDisc_rcg
                if store._stealth_condom_removed:
                    call StealthCondomDiscovery(girl, "reverse_cowgirl") from _call_StealthDisc_rcg
                menu:
                    "Riding" if girl_has_pose(girl, "cowgirl"):
                        $ debug_log("[SWITCH] RCG->CG: clothes=%s states=%s condom=%s anal=%s" % (str(girl.clothes), str(girl.clothes_state), store.condom_active, store.rcg_anal))
                        $ Say_Player(_("Get on top..."))
                        # Anal scene -> vaginal-only position: same gates as "Switch to her pussy" (escalation.rpy)
                        $ store._switch_gate_ok = True
                        $ _sw_from_anal = bool(store.rcg_anal)   # only an ANAL scene makes this switch a hole switch
                        if _sw_from_anal:
                            call _switch_to_vaginal_gate(girl, "reverse_cowgirl") from _call_sw_gate_sw_rcg_cg
                            if store._switch_gate_scene_ended:
                                return
                        if store._switch_gate_ok:
                            python:
                                _switch_lines = [
                                    _("You want me on top? I like that..."),

                                    _("Mmm, let me ride you."),

                                    _("Okay... sit back and enjoy the view."),

                                ]
                            $ Say_Line(girl, _tl(renpy.random.choice(_switch_lines)))

                            # Clean up RCG standalones
                            $ _saved_condom = condom_carry_save()
                            python:
                                store._rcg_girl = None
                                store._srcg_girl = None   # her split RCG ref too: the switch leaked it, _in_sex never ended (tester 2026-10-10)
                                store.rcg_started = False
                                store.rcg_butt_state = "butt_top_none"
                                renpy.hide("rcg_penis")
                                renpy.hide("rcg_condom")
                                renpy.hide("rcg_butt_top")
                                renpy.hide("rcg_butt_gap")
                                renpy.hide("rcg_thigh_highs")
                                renpy.hide("rcg_butt_blush")
                                renpy.hide("rcg_arms2")
                                renpy.hide("rcg_crop_top")
                                renpy.hide("rcg_bikini_top")
                                renpy.hide("rcg_grab_left")
                                renpy.hide("rcg_grab_right")
                                renpy.hide("rcg_butt_cum")
                                renpy.hide("rcg_cum_face")
                                renpy.hide("rcg_dripping_cum")
                                renpy.hide("rcg_penis_cum")
                                renpy.hide("rcg_back_cum")
                                renpy.hide("rcg_rub_top")
                                renpy.hide("rcg_skirt")
                                renpy.hide("rcg_panties")
                                renpy.hide("rcg_panties2")
                                renpy.hide("rcg_panties_side_bottom")
                                hide_girl_sprite(girl)
                                store.rcg_arms_pose = 1
                                store.rcg_grab = False
                                store.rcg_hold = False
                                store.rcg_anal = False
                                store.rcg_rub_mode = False
                                store.rcg_tip_mode = False
                                store._rcg_escalated = False
                                store.condom_active = False
                            $ condom_carry_restore(_saved_condom)

                            $ cowgirl_speed = 0
                            $ _scene_position_switch(girl, "reverse_cowgirl", "cowgirl", anal=False)   # player switch: count the new position (and sex, if it is vaginal now)
                            call COWGIRL_Launch(girl, from_switch=True) from _call_COWGIRL_Launch_switch
                            if _sw_from_anal and girl.has_trait("virgin"):
                                # she was only doing anal: this switch is her first vaginal penetration
                                call virgin_first_time(girl, "cowgirl") from _call_virgin_sw_rcg_cg
                            call COWGIRL_ControlMenu(girl) from _call_COWGIRL_ControlMenu_switch

                            $ store._sub_event_position_switched = True

                    "Doggy" if girl_has_pose(girl, "doggy"):
                        $ Say_Player(_("Get on all fours..."))
                        call _femdom_position_gate(girl, "reverse_cowgirl", "doggy") from _call_fpg_rcg_dg
                        if store._femdom_gate_ok:
                            # Carry the current hole into the next pose (anal stays anal)
                            $ _switch_anal = bool(store.rcg_anal)
                            python:
                                _switch_lines = [
                                    _("You want me from behind? Okay..."),

                                    _("Mmm, doggy style? I like that."),

                                    _("Sure... let me get on all fours."),

                                ]
                            $ Say_Line(girl, _tl(renpy.random.choice(_switch_lines)))

                            # Clean up RCG standalones
                            $ _saved_condom = condom_carry_save()
                            python:
                                store._rcg_girl = None
                                store._srcg_girl = None   # her split RCG ref too: the switch leaked it, _in_sex never ended (tester 2026-10-10)
                                store.rcg_started = False
                                store.rcg_butt_state = "butt_top_none"
                                renpy.hide("rcg_penis")
                                renpy.hide("rcg_condom")
                                renpy.hide("rcg_butt_top")
                                renpy.hide("rcg_butt_gap")
                                renpy.hide("rcg_thigh_highs")
                                renpy.hide("rcg_butt_blush")
                                renpy.hide("rcg_arms2")
                                renpy.hide("rcg_crop_top")
                                renpy.hide("rcg_bikini_top")
                                renpy.hide("rcg_grab_left")
                                renpy.hide("rcg_grab_right")
                                renpy.hide("rcg_butt_cum")
                                renpy.hide("rcg_cum_face")
                                renpy.hide("rcg_dripping_cum")
                                renpy.hide("rcg_penis_cum")
                                renpy.hide("rcg_back_cum")
                                renpy.hide("rcg_rub_top")
                                renpy.hide("rcg_skirt")
                                renpy.hide("rcg_panties")
                                renpy.hide("rcg_panties2")
                                renpy.hide("rcg_panties_side_bottom")
                                hide_girl_sprite(girl)
                                store._rcg_girl = None
                                store._srcg_girl = None   # her split RCG ref too (tester 2026-10-10)
                                store.rcg_arms_pose = 1
                                store.rcg_grab = False
                                store.rcg_hold = False
                                store.rcg_anal = False
                                store.rcg_rub_mode = False
                                store.rcg_tip_mode = False
                                store._rcg_escalated = False
                                store.condom_active = False
                            $ condom_carry_restore(_saved_condom)

                            $ doggy_speed = 0
                            $ store.doggy_anal = _switch_anal
                            $ debug_log("[SWITCH] RCG->DG carry anal=%s" % store.doggy_anal)
                            $ _scene_position_switch(girl, "reverse_cowgirl", "doggy", anal=getattr(store, "doggy_anal", False))   # player switch: count the new position (and sex, if it is vaginal now)
                            call DG_Launch(girl, from_switch=True) from _call_DG_Launch_rcg_switch
                            call DG_ControlMenu(girl) from _call_DG_ControlMenu_rcg_switch

                            $ store._sub_event_position_switched = True

                    "Full Nelson" if girl_has_pose(girl, "full_nelson"):
                        $ Say_Player(_("Come here..."))
                        call _femdom_position_gate(girl, "reverse_cowgirl", "full_nelson") from _call_fpg_rcg_fn
                        if store._femdom_gate_ok:
                            # Carry the current hole into the next pose (anal stays anal)
                            $ _switch_anal = bool(store.rcg_anal)
                            python:
                                _switch_lines = [
                                    _("What are you... oh!"),

                                    _("You're picking me up...?!"),

                                    _("Whoa... okay...!"),

                                ]
                            $ Say_Line(girl, _tl(renpy.random.choice(_switch_lines)))

                            $ _saved_condom = condom_carry_save()
                            python:
                                store._rcg_girl = None
                                store._srcg_girl = None   # her split RCG ref too: the switch leaked it, _in_sex never ended (tester 2026-10-10)
                                store.rcg_started = False
                                store.rcg_butt_state = "butt_top_none"
                                renpy.hide("rcg_penis")
                                renpy.hide("rcg_condom")
                                renpy.hide("rcg_butt_top")
                                renpy.hide("rcg_butt_gap")
                                renpy.hide("rcg_thigh_highs")
                                renpy.hide("rcg_butt_blush")
                                renpy.hide("rcg_arms2")
                                renpy.hide("rcg_crop_top")
                                renpy.hide("rcg_bikini_top")
                                renpy.hide("rcg_grab_left")
                                renpy.hide("rcg_grab_right")
                                renpy.hide("rcg_butt_cum")
                                renpy.hide("rcg_cum_face")
                                renpy.hide("rcg_dripping_cum")
                                renpy.hide("rcg_penis_cum")
                                renpy.hide("rcg_back_cum")
                                renpy.hide("rcg_rub_top")
                                renpy.hide("rcg_skirt")
                                renpy.hide("rcg_panties")
                                renpy.hide("rcg_panties2")
                                renpy.hide("rcg_panties_side_bottom")
                                hide_girl_sprite(girl)
                                store.rcg_arms_pose = 1
                                store.rcg_grab = False
                                store.rcg_hold = False
                                store.rcg_anal = False
                                store.rcg_rub_mode = False
                                store.rcg_tip_mode = False
                                store._rcg_escalated = False
                                store.condom_active = False
                            $ condom_carry_restore(_saved_condom)

                            $ fn_speed = 0
                            $ store.fn_anal = _switch_anal
                            $ debug_log("[SWITCH] RCG->FN carry anal=%s" % store.fn_anal)
                            $ _scene_position_switch(girl, "reverse_cowgirl", "full_nelson", anal=getattr(store, "fn_anal", False))   # player switch: count the new position (and sex, if it is vaginal now)
                            call FN_Launch(girl, from_switch=True) from _call_FN_Launch_rcg_switch
                            call FN_ControlMenu(girl) from _call_FN_ControlMenu_rcg_switch

                            $ store._sub_event_position_switched = True

                    "Back":
                        pass

            "Stop now":
                $ debug_log("[DEBUG] RCG ControlMenu: ASK HER TO STOP clicked")
                if store._forced_creampie_end_after_orgasm:
                    $ debug_log("[DEBUG] forced_creampie path")
                    call _player_stops_after_forced_creampie(girl, _rcg_scene) from _call__player_stops_forced_dg
                elif rcg_speed >= 1:
                    $ debug_log("[DEBUG] Ask her to stop (RCG): Lust=%d speed=%d" % (girl.Lust, rcg_speed))
                    $ store._edge_lust_check = (girl.Lust >= 80)
                    if store._edge_lust_check:
                        $ debug_log("[DEBUG] Lust >= 80, entering EdgeDenial")
                        # She begs with him still in her: the scene stays exactly as it is until the action really stops
                        # (speed 0 here redrew her layers before anything had stopped). "Keep going" goes on at the same
                        # speed, her "No, stop." is the same stop as below (author, 2026-10-09)
                        call EdgeDenial(girl, _rcg_scene) from _call_EdgeDenial_rcg
                        if girl.Lust >= 100:
                            call GirlCumming(girl, _rcg_scene, _rcg_scene) from _call_GirlCumming_rcg_edge
                        if store._edge_scene_ended:
                            $ store._edge_scene_ended = False
                            call _cum_dispatch_aftermath(girl, _rcg_scene) from _call_ca_dispatch_rcg_edge_stop
                            return
                    else:
                        $ debug_log("[DEBUG] Lust < 80, ending scene normally")
                        call _cum_dispatch_aftermath(girl, _rcg_scene) from _call_ca_dispatch_rcg_stop_main
                        return
                else:
                    $ debug_log("[DEBUG] normal stop path")
                    $ Say_Line(girl, _pick_stop_line(girl))
                    call _cum_dispatch_aftermath(girl, _rcg_scene) from _call_ca_dispatch_rcg_stop
                    return

# ============================================================
# Head Turn — player asks girl to face forward or back
# ============================================================
label _rcg_turn_head(girl):
    $ Say_Player(_("Turn your head forward."))
    if _rcg_turn_forward_check(girl):
        python:
            _tk = _rcg_turn_trait_key(girl)
            _lines = _RCG_TURN_ACCEPT_LINES.get(_tk, _RCG_TURN_ACCEPT_LINES["_default"])
            _line = renpy.random.choice(_lines)
        $ Say_Line(girl, _tl(_line))
        $ store.hiding_face = True
    else:
        python:
            _tk = _rcg_turn_trait_key(girl)
            _lines = _RCG_TURN_REFUSE_LINES.get(_tk, _RCG_TURN_REFUSE_LINES["_default"])
            _line = renpy.random.choice(_lines)
        $ Say_Line(girl, _tl(_line))
    return

# ============================================================
# Secret Recording — she's facing forward and can't see
# ============================================================
label _rcg_secret_recording(girl):
    python:
        store._recording_active = True
        store._recording_girl = girl
        store._recording_face_locked = False
        store._player_hand_disabled = renpy.random.choice(["left", "right"])
        vid = {
            "girl_gid": girl.gid,
            "type": rcg_scene_type(),   # the anal variant while he is in her ass
            "location": CurrentLocation,
            "committed": girl.has_npc_partner(),
            "consensual": False,
            "reluctant": False,
            "face_hidden": True,
            "hd": Player.has_item("tekmix_camera"),
            "snapshot": _make_vid_snapshot(girl),
            "condom": bool(store.condom_active),
        }
        _tag_coercion_on_vid(vid)
        store.Player.recorded_videos.append(vid)
        renpy.show_screen("recording_overlay")
    $ _sec_txt = _tl(_("You quietly pull out your phone and start recording. She can't see a thing."))
    "[_sec_txt]"
    return

# ============================================================
# Look back during recording — discovers secret recording
# ============================================================
label _rcg_look_back_during_recording(girl):
    $ store._rcg_secret_caught_end = False
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
            $ _kick_txt = _tl(_("She pushes you away and gets off, furious."))
            "[_kick_txt]"
            $ store._rcg_secret_caught_end = True
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
            $ _kick_txt = _tl(_("She pushes you away and gets off, furious."))
            "[_kick_txt]"
            $ store._rcg_secret_caught_end = True
        else:
            $ Say_Line(girl, _tl(_("Wait, is that... are you recording?! Since when?!")))
            $ set_scene_expression(girl, "angry", blush="1")
            $ Change_Status(girl, "Love", -5)
            $ Change_Status(girl, "Inbt", 5)
            $ finalize_recording()
            $ _kick_txt = _tl(_("She pushes you away and gets off, furious."))
            "[_kick_txt]"
            $ store._rcg_secret_caught_end = True
    else:
        $ _look_txt = _tl(_("You tell her to look back at you."))
        "[_look_txt]"

    return

# ============================================================
# Bottom Clothes Menu — used by Launch and TipLaunch
# Asks player how to handle skirt and panties before sex/tip.
# ============================================================
# A girl whose RCG art has no dressed penetration (sex_nude in GIRL_SCENE_CONFIG "rcg": Shion) takes everything
# off before he goes in, the tip included; her layers never draw a stitch once rcg_started. Called wherever the
# bottom-clothes menu is (the launch, the tip, the escalations) and on a switch into the pose.
label _rcg_sex_nude(girl):
    if not _rcg_sex_nude_needed(girl):
        return
    $ Say_Line(girl, _("All of it comes off. I don't do this half dressed."))
    $ girl.Outfit_Change(over="none", mid="none", chest="none", legs="none", panties="none", pose="reverse_cowgirl")
    $ print("[RCG_NUDE] %s stripped for the penetration" % girl.gid)
    call RCG_RefreshClothing(girl) from _call_RCG_RefreshClothing_sex_nude
    call CheckExposure(girl) from _call_CheckExposure_sex_nude
    return

init python:
    def _rcg_sex_nude_needed(girl):
        if not _gsc(girl.gid, "sex_nude", False, "rcg"):
            return False
        return any(getattr(girl, _a, None) for _a in ("Over", "Mid", "Chest", "Legs", "Panties"))

label _rcg_bottom_clothes_menu(girl):
    # Centralized bottom clothing handler for ALL RCG transitions.
    # Skips items already displaced (side/down/up) or removed.
    # Handles exposure registration (saw_pussy) for any displacement.
    # Call this from Launch, TipLaunch, and ALL escalation paths.

    if _gsc(girl.gid, "sex_nude", False, "rcg"):
        call _rcg_sex_nude(girl) from _call_rcg_sex_nude_btm
        return

    $ _skirt_needs = girl.Legs is not None and girl.clothes_state.get("skirt") == "full"
    $ _pan_needs = girl.Panties is not None and girl.clothes_state.get("panties") == "full"

    if not _skirt_needs and not _pan_needs:
        return

    $ Say_Line(girl, _("Here... let me give you a better view."))

    # --- SKIRT (only if still at full) ---
    if _skirt_needs:
        $ _legs_label = _("Remove pants") if _strip_name_for_slot(girl, "skirt") == "pants" else _("Remove skirt")
        menu:
            "Lift skirt up" if _item_has_state(girl, "skirt", "up"):
                $ girl.clothes_state["skirt"] = "up"
            "[_legs_label]":
                $ girl.clothes["skirt"] = None
                $ girl.clothes_state["skirt"] = "full"
        call RCG_RefreshClothing(girl) from _call_RCG_RefreshClothing_btm_skirt

    # --- PANTIES (only if still at full) ---
    if _pan_needs:
        pause 0.3
        menu:
            "Pull panties to the side" if _item_has_state(girl, "panties", "side"):
                $ girl.clothes_state["panties"] = "side"
            "Pull panties down" if _item_has_state(girl, "panties", "down"):
                $ girl.clothes_state["panties"] = "down"
            "Remove panties":
                $ girl.clothes["panties"] = None
                $ girl.clothes_state["panties"] = "full"
        call RCG_RefreshClothing(girl) from _call_RCG_RefreshClothing_btm_pan

    # Check exposure for any displacement (boobs from chest up, pussy from panties side/down/remove)
    call CheckExposure(girl) from _call_CheckExposure_btm_menu

    return

label RCG_StripMenu(girl):
    while True:
        $ _legs_label = _("Remove pants") if _strip_name_for_slot(girl, "skirt") == "pants" else _("Remove skirt")
        menu:
            "Remove top" if girl.Over:
                call _strip_approval(girl, ["over"]) from _call__strip_approval_20
                if store._strip_approved:
                    $ girl.clothes["over"] = None
                    call RCG_RefreshClothing(girl) from _call_RCG_RefreshClothing_strip_over
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_18

            "Pull chest up" if girl.Chest and girl.clothes_state.get("chest") != "up" and _item_has_state(girl, "chest", "up"):
                call _strip_approval(girl, ["chest"]) from _call__strip_approval_dg_chest_up
                if store._strip_approved:
                    $ girl.clothes_state["chest"] = "up"
                    call RCG_RefreshClothing(girl) from _call_RCG_RefreshClothing_strip_chest_up
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_dg_chest_up

            "Remove chest" if girl.Chest:
                call _strip_approval(girl, ["chest"]) from _call__strip_approval_21
                if store._strip_approved:
                    $ girl.clothes["chest"] = None
                    $ girl.clothes_state["chest"] = "full"
                    call RCG_RefreshClothing(girl) from _call_RCG_RefreshClothing_strip_chest
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_19

            "Lift skirt up" if girl.Legs and _item_has_state(girl, "skirt", "up") and girl.clothes_state.get("skirt") != "up":
                call _strip_approval(girl, ["legs"]) from _call__strip_approval_dg_skirt_up
                if store._strip_approved:
                    $ girl.clothes_state["skirt"] = "up"
                    call RCG_RefreshClothing(girl) from _call_RCG_RefreshClothing_strip_skirt_up
                    call CheckExposure(girl) from _call_CheckExposure_dg_skirt_up

            "[_legs_label]" if girl.Legs:
                call _strip_approval(girl, ["legs"]) from _call__strip_approval_22
                if store._strip_approved:
                    $ girl.clothes["skirt"] = None
                    $ girl.clothes_state["skirt"] = "full"
                    call RCG_RefreshClothing(girl) from _call_RCG_RefreshClothing_strip_skirt
                    call CheckExposure(girl) from _call_CheckExposure_20

            "Remove panties" if girl.Panties:
                call _strip_approval(girl, ["panties"]) from _call__strip_approval_23
                if store._strip_approved:
                    $ girl.clothes["panties"] = None
                    $ girl.clothes_state["panties"] = "full"
                    call RCG_RefreshClothing(girl) from _call_RCG_RefreshClothing_strip_pan
                    call CheckExposure(girl) from _call_CheckExposure_21

            "Pull panties to the side" if girl.Panties and _panties_next_state(girl) == "side":
                call _strip_approval(girl, ["panties"]) from _call__strip_approval_dg_pan_side
                if store._strip_approved:
                    $ girl.clothes_state["panties"] = "side"
                    call RCG_RefreshClothing(girl) from _call_RCG_RefreshClothing_strip_pan_side
                    call CheckExposure(girl) from _call_CheckExposure_dg_pan_side

            "Pull panties down" if girl.Panties and _panties_next_state(girl) == "down":
                call _strip_approval(girl, ["panties"]) from _call__strip_approval_dg_pan_down
                if store._strip_approved:
                    $ girl.clothes_state["panties"] = "down"
                    call RCG_RefreshClothing(girl) from _call_RCG_RefreshClothing_strip_pan_down
                    call CheckExposure(girl) from _call_CheckExposure_dg_pan_down

            "Remove shoes" if getattr(girl, "Shoes", None):
                $ girl.clothes["shoes"] = None
                call RCG_RefreshClothing(girl) from _call_RCG_RefreshClothing_strip_shoes

            "Back":
                return

# ============================================================
# Cum Animation
# ============================================================
# Penis slide-in — slides up from below into position
transform rcg_penis_slide_in:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    alpha 1.0
    yoffset 350
    easein 0.45 yoffset 155

# Penis slide-out — slides down off screen
transform rcg_penis_slide_out:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    alpha 1.0
    yoffset 155
    easeout 0.45 yoffset 350

transform rcg_penis_cum_pulse():
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    xoffset 0
    yoffset 158
    yzoom 1.0
    pause 0.45
    ease 0.08 yzoom 1.06
    ease 0.15 yzoom 1.0
    pause 0.27
    ease 0.08 yzoom 1.06
    ease 0.15 yzoom 1.0

# ============================================================
# Penis Entry Animation (slide in from below)
# ============================================================
label RCG_PenisEnterAnim(girl):
    if girl.gid == "shion":
        # no frame of its own: the RCG_ApplySpeed every caller runs right after this draws him already inside her
        $ _srcg_penis_enter()
        return
    python:
        renpy.hide("rcg_penis")
        renpy.hide("rcg_condom")
        _pen_img = "%s rcg_penis" % girl.gid
        # Use high zorder during slide so penis appears above butt layers
        _pen_z = 10060
        renpy.show(_pen_img, tag="rcg_penis", at_list=[rcg_penis_slide_in], zorder=_pen_z)
        if store.condom_active:
            _cb_cimg = _condom_img_tag("rcg_condom")
            renpy.show(_cb_cimg, tag="rcg_condom", at_list=[rcg_penis_slide_in], zorder=_pen_z)
    $ renpy.pause(0.55)
    return

# ============================================================
# Hold her down: his hands on her thighs (girls whose art has them: rcg_has_hold), on / off. She keeps riding,
# a shorter stroke, held deep (her layer set reads store.rcg_hold). Her face answers it like a grab of her ass.
# ============================================================
label RCG_Hold(girl, on):
    $ store.rcg_hold = bool(on)
    $ print("[RCG_HOLD] %s: %s (speed %s)" % (girl.gid, "he holds her down" if on else "he lets go of her", rcg_speed))
    if on:
        python:
            _hold_react = renpy.random.choice(["mouth_surprised", "mouth_tongue", "mouth_kiss"])
            set_scene_expression(girl, None, mouth=_hold_react)
    call RCG_ApplySpeed(girl, rcg_speed) from _call_RCG_ApplySpeed_hold
    return

# ============================================================
# RCG_HoleTransition: he goes in, or out of one hole and into the other (a girl whose art has anal in this pose:
# rcg_has_anal; any other girl only ever enters her pussy here). First entry, the same hole again (nothing to
# do) or the switch. The caller calls RCG_ApplySpeed after it (the layers read store.rcg_anal).
# ============================================================
label RCG_HoleTransition(girl, to_anal):
    python:
        _rht_to_anal = bool(to_anal) and rcg_has_anal(girl)
        _rht_first = not store.rcg_started
        _rht_switching = store.rcg_started and (bool(store.rcg_anal) != _rht_to_anal)
        print("[RCG_HT] %s to_anal=%s started=%s cur_anal=%s | first=%s switching=%s" % (
            girl.gid, _rht_to_anal, store.rcg_started, store.rcg_anal, _rht_first, _rht_switching))

    if _rht_switching:
        # he pulls out: she stops for a moment, the penis out of her
        $ store.rcg_started = False
        call RCG_ApplySpeed(girl, 0) from _call_RCG_ApplySpeed_ht_out
        $ renpy.pause(0.3)

    python:
        store.rcg_anal = _rht_to_anal
        store.rcg_started = True

    if _rht_first or _rht_switching:
        call RCG_PenisEnterAnim(girl) from _call_RCG_PenisEnterAnim_ht
    # only when he actually goes into her ass (first entry or pussy -> ass), never on a speed change inside it
    if _rht_to_anal and (_rht_first or _rht_switching):
        $ _watcher_scene_comment("anal_enter")
    return

# ============================================================
# Condom Remove Animation (slide out with condom, slide back in raw)
# ============================================================
label RCG_CondomRemoveAnim(girl):
    if girl.gid == "shion":
        $ renpy.pause(0.3)
        $ _srcg_apply_speed(girl, store.rcg_speed)
        $ renpy.pause(0.3)
        return
    python:
        _pen_img = "%s rcg_penis" % girl.gid
        # High zorder so penis slides above butt layers
        _rcg_condom_tag = _condom_img_tag("rcg_condom")
        renpy.show(_pen_img, tag="rcg_penis", at_list=[rcg_penis_slide_out], zorder=10060)
        renpy.show(_rcg_condom_tag, tag="rcg_condom", at_list=[rcg_penis_slide_out], zorder=10060)
    $ renpy.pause(0.5)
    python:
        renpy.hide("rcg_condom")
        renpy.hide("rcg_penis")
        _pen_img = "%s rcg_penis" % girl.gid
        renpy.show(_pen_img, tag="rcg_penis", at_list=[rcg_penis_slide_in], zorder=10060)
    $ renpy.pause(0.5)
    return

label RCG_CumAnim(girl):
    if girl.gid == "shion":
        $ _apply_cum_expression(girl, "rcg", "inside")
        $ store.rcg_speed = 4
        call RCG_ApplySpeed(girl, 4) from _call_RCG_ApplySpeed_cum_shion
        call _cum_punch_pair("oral") from _call_cum_punch_rcg_cum_shion
        python:
            store.rcg_speed = 0
            for _tag in ("srcg_head", "srcg_left_arm", "srcg_right_arm",
                          "srcg_torso", "srcg_left_leg", "srcg_right_leg",
                          "srcg_left_thigh", "srcg_right_thigh",
                          "srcg_butt_bottom", "srcg_butt_top",
                          "srcg_hold_left", "srcg_hold_right"):
                renpy.hide(_tag)
        call RCG_ApplySpeed(girl, 0) from _call_RCG_ApplySpeed_cum_freeze_shion
        return
    # Cum expression: intense orgasm face
    $ _dg_prev_speed = store.rcg_speed
    $ _apply_cum_expression(girl, "rcg", "inside")
    # Activate grab + speed 4 (cumming inside: deep, short bounces)
    if store.rcg_arms_pose != 2:
        $ store.rcg_grab = True
    $ store.rcg_speed = 4
    call RCG_ApplySpeed(girl, 4) from _call_RCG_ApplySpeed_cum_grab

    # Penis pulse (+ condom if active)
    $ renpy.show("%s rcg_penis" % girl.gid, tag="rcg_penis", at_list=[rcg_penis_cum_pulse()], zorder=9975)
    if store.condom_active:
        $ _cb_cimg = _condom_img_tag("rcg_condom")
        $ renpy.show(_cb_cimg, tag="rcg_condom", at_list=[rcg_penis_cum_pulse()], zorder=9975)

    call _cum_punch_pair("oral") from _call_cum_punch_rcg_cum

    # Release grab + restore to previous speed
    $ store.rcg_grab = False
    $ store.rcg_speed = _dg_prev_speed
    call RCG_ApplySpeed(girl, _dg_prev_speed) from _call_RCG_ApplySpeed_cum_restore

    return

# ============================================================
# Cum Outside Freeze (condom off, frozen, penis on top, butt_cum)
# ============================================================
label RCG_CumOutsideFreeze(girl):
    if girl.gid == "shion":
        # he pulls out and cums on her: the penis over her, her holes as he left them (_srcg_penis_out), still
        python:
            store.condom_active = False
            _apply_cum_expression(girl, "rcg", "outside")
            store._srcg_penis_out = "out"
            store.rcg_speed = 0
            # Force-stop her ride: hide her layers so Ren'Py drops the ATL repeat state,
            # then _srcg_apply_speed re-shows them static (at_list=[])
            for _tag in ("srcg_head", "srcg_left_arm", "srcg_right_arm",
                          "srcg_torso", "srcg_left_leg", "srcg_right_leg",
                          "srcg_left_thigh", "srcg_right_thigh",
                          "srcg_butt_bottom", "srcg_butt_top",
                          "srcg_hold_left", "srcg_hold_right"):
                renpy.hide(_tag)
        call RCG_ApplySpeed(girl, 0) from _call_RCG_ApplySpeed_cum_outside_shion
        call _cum_punch_pair("oral") from _call_cum_punch_rcg_outside_shion
        $ _srcg_show_cum(cum_tags=["body"])
        return
    $ _had_condom = store.condom_active
    python:
        store.condom_active = False
        store.rcg_grab = False
        _apply_cum_expression(girl, "rcg", "outside")
        _static_slot = rcg_slot_speed0
        _ca_at = [_static_slot]

        # Freeze body
        if "_build_rcg_attributes" in globals():
            _fr_attrs = _build_rcg_attributes(girl)
        else:
            _fr_attrs = _build_attributes_for_girl(girl, pose="reverse_cowgirl")
        _fr_img = "%s rcg" % girl.gid
        if _fr_attrs:
            _fr_img += " " + " ".join(_fr_attrs)
        renpy.show(_fr_img, tag=girl.gid, at_list=_ca_at, zorder=9980)

        # Arms 2 if active
        if store.rcg_arms_pose == 2:
            _arms2_ls = "%s rcg_arms_ls_2" % girl.gid
            _arms2_img = _arms2_ls if girl.Over and renpy.has_image(_arms2_ls, exact=True) else "%s rcg_arms_2" % girl.gid
            renpy.show(_arms2_img, tag="rcg_arms2", at_list=_ca_at, zorder=10050)

        # Crop top upper half (above arms)
        _fr_ct = "%s rcg_crop_top" % girl.gid
        if renpy.has_image(_fr_ct, exact=True) and "torso_chest_corset" in _fr_attrs:
            renpy.show(_fr_ct, tag="rcg_crop_top", at_list=_ca_at, zorder=10051)
        else:
            renpy.hide("rcg_crop_top")

        # Bikini top upper half (above arms)
        _fr_bt = "%s rcg_bikini_top" % girl.gid
        if renpy.has_image(_fr_bt, exact=True) and "torso_chest_bikini_top" in _fr_attrs:
            renpy.show(_fr_bt, tag="rcg_bikini_top", at_list=_ca_at, zorder=10051)
        else:
            renpy.hide("rcg_bikini_top")

        # Freeze butt layers
        renpy.show("%s rcg_butt_gap" % girl.gid, tag="rcg_butt_gap", at_list=_ca_at, zorder=9960)
        _bt_img = "%s rcg_butt_top_1" % girl.gid if not store.rcg_started else "%s rcg_butt_top_2" % girl.gid
        renpy.show(_bt_img, tag="rcg_butt_top", at_list=_ca_at, zorder=10005)

        # Freeze panties if wearing (below skirt)
        if girl.Panties:
            _ca_pan_state = girl.clothes_state.get("panties", "full")
            _ca_pan_img = "%s rcg_panties_%s_%s" % (girl.gid, girl.Panties, _ca_pan_state)
            renpy.show(_ca_pan_img, tag="rcg_panties", at_list=_ca_at, zorder=10006)
            # Side bottom: freeze too
            _ca_pan_sb = "%s rcg_panties_%s_side_bottom" % (girl.gid, girl.Panties)
            if _ca_pan_state == "side" and renpy.has_image(_ca_pan_sb):
                renpy.show(_ca_pan_sb, tag="rcg_panties_side_bottom", at_list=_ca_at, zorder=9965)
            else:
                renpy.hide("rcg_panties_side_bottom")
            # Side2 (bikini equivalent of side_bottom): freeze too
            _ca_pan_s2 = "%s rcg_panties_%s_side2" % (girl.gid, girl.Panties)
            if _ca_pan_state == "side" and renpy.has_image(_ca_pan_s2, exact=True):
                renpy.show(_ca_pan_s2, tag="rcg_panties2", at_list=_ca_at, zorder=9965)
            else:
                renpy.hide("rcg_panties2")

        # Freeze skirt if wearing (above panties)
        if girl.Legs:
            _ca_skirt_state = girl.clothes_state.get("skirt", "full")
            _ca_skirt_tag = "rcg_skirt_up" if _ca_skirt_state == "up" else "rcg_skirt"
            renpy.show("%s %s" % (girl.gid, _ca_skirt_tag), tag="rcg_skirt", at_list=_ca_at, zorder=10007)

        renpy.show("%s rcg_butt_blush" % girl.gid, tag="rcg_butt_blush", at_list=_ca_at, zorder=10006)

        if getattr(girl, "Shoes", None):
            renpy.show("%s rcg_thigh_highs" % girl.gid, tag="rcg_thigh_highs", at_list=_ca_at, zorder=9968)

        # Hide grab, dripping, cum layers, rub_top (cum appears after punches)
        renpy.hide("rcg_grab_left")
        renpy.hide("rcg_grab_right")
        renpy.hide("rcg_butt_cum")
        renpy.hide("rcg_back_cum")
        renpy.hide("rcg_cum_face")
        renpy.hide("rcg_dripping_cum")
        renpy.hide("rcg_penis_cum")
        renpy.hide("rcg_rub_top")

    python:
        _pen_img = "%s rcg_penis" % girl.gid
        _was_rub = getattr(store, "rcg_rub_mode", False)

    if _was_rub:
        # Rub: penis was never inside, show on top directly
        python:
            renpy.show(_pen_img, tag="rcg_penis", at_list=[rcg_penis_speed0], zorder=10060)
    else:
        # Sex/tip: slide penis out (with condom if had one), then back in on top
        python:
            if _had_condom:
                _cb_cimg = _condom_img_tag("rcg_condom")
                renpy.show(_cb_cimg, tag="rcg_condom", at_list=[rcg_penis_slide_out], zorder=9975)
            renpy.show(_pen_img, tag="rcg_penis", at_list=[rcg_penis_slide_out], zorder=9975)
        $ renpy.pause(0.6)
        python:
            renpy.hide("rcg_condom")
            renpy.hide("rcg_penis")
            renpy.show(_pen_img, tag="rcg_penis", at_list=[rcg_penis_slide_in], zorder=10060)
        $ renpy.pause(0.6)

    # Override with cum pulse on top
    python:
        renpy.show("%s rcg_penis" % girl.gid, tag="rcg_penis", at_list=[rcg_penis_cum_pulse()], zorder=10060)

    call _cum_punch_pair("oral") from _call_cum_punch_rcg_outside

    # After punches: butt_top_1 if no fuck, penis static, cum layers visible
    python:
        _ca_at = [rcg_slot_speed0]
        if not store.rcg_started:
            renpy.show("%s rcg_butt_top_1" % girl.gid, tag="rcg_butt_top", at_list=_ca_at, zorder=10005)
        renpy.show("%s rcg_penis" % girl.gid, tag="rcg_penis", at_list=[rcg_penis_speed0], zorder=10060)
        renpy.show("%s rcg_butt_cum" % girl.gid, tag="rcg_butt_cum", at_list=_ca_at, zorder=10050)
        renpy.show("%s rcg_back_cum" % girl.gid, tag="rcg_back_cum", at_list=_ca_at, zorder=10051)
        renpy.show("%s rcg_cum_face" % girl.gid, tag="rcg_cum_face", at_list=_ca_at, zorder=10053)
        renpy.show("%s rcg_dripping_cum" % girl.gid, tag="rcg_dripping_cum", at_list=_ca_at, zorder=9970)

    return

# ============================================================
# Creampie Aftermath (static pose before ending)
# ============================================================
label RCG_CreampieAftermath(girl):
    if girl.gid == "shion":
        # he came inside: penis stays visible (pulled out, drawn over her), her holes as he left them, his cum on her
        $ store._srcg_penis_out = "out"
        call RCG_ApplySpeed(girl, 0) from _call_RCG_ApplySpeed_creampie_shion
        return
    # Show static: arms 2, butt_top_2, thigh_highs, no penis/grab
    python:
        store.rcg_arms_pose = 2
        store.rcg_grab = False
        _static_slot = rcg_slot_speed0

        # Build attrs with arms_none (arms2 shown externally)
        if "_build_rcg_attributes" in globals():
            _ca_attrs = _build_rcg_attributes(girl)
        else:
            _ca_attrs = _build_attributes_for_girl(girl, pose="reverse_cowgirl")
        _ca_img = "%s rcg" % girl.gid
        if _ca_attrs:
            _ca_img += " " + " ".join(_ca_attrs)

        _ca_at = [_static_slot]

        # Body static
        renpy.show(_ca_img, tag=girl.gid, at_list=_ca_at, zorder=9980)

        # Arms 2 on top
        _arms2_ls = "%s rcg_arms_ls_2" % girl.gid
        _arms2_img = _arms2_ls if girl.Over and renpy.has_image(_arms2_ls, exact=True) else "%s rcg_arms_2" % girl.gid
        renpy.show(_arms2_img, tag="rcg_arms2", at_list=_ca_at, zorder=10050)

        # Crop top upper half (above arms)
        _ca_ct = "%s rcg_crop_top" % girl.gid
        if renpy.has_image(_ca_ct, exact=True) and "torso_chest_corset" in _ca_attrs:
            renpy.show(_ca_ct, tag="rcg_crop_top", at_list=_ca_at, zorder=10051)
        else:
            renpy.hide("rcg_crop_top")

        # Bikini top upper half (above arms)
        _ca_bt = "%s rcg_bikini_top" % girl.gid
        if renpy.has_image(_ca_bt, exact=True) and "torso_chest_bikini_top" in _ca_attrs:
            renpy.show(_ca_bt, tag="rcg_bikini_top", at_list=_ca_at, zorder=10051)
        else:
            renpy.hide("rcg_bikini_top")

        # Butt layers static
        renpy.show("%s rcg_butt_gap" % girl.gid, tag="rcg_butt_gap", at_list=_ca_at, zorder=9960)
        renpy.show("%s rcg_butt_top_2" % girl.gid, tag="rcg_butt_top", at_list=_ca_at, zorder=10005)

        # Skirt if wearing (respect up state)
        if girl.Legs:
            _ca_skirt_state = girl.clothes_state.get("skirt", "full")
            _ca_skirt_tag = "rcg_skirt_up" if _ca_skirt_state == "up" else "rcg_skirt"
            renpy.show("%s %s" % (girl.gid, _ca_skirt_tag), tag="rcg_skirt", at_list=_ca_at, zorder=10006)
        else:
            renpy.hide("rcg_skirt")

        renpy.show("%s rcg_dripping_cum" % girl.gid, tag="rcg_dripping_cum", at_list=_ca_at, zorder=9970)
        renpy.show("%s rcg_butt_blush" % girl.gid, tag="rcg_butt_blush", at_list=_ca_at, zorder=10006)
        renpy.show("%s rcg_butt_cum" % girl.gid, tag="rcg_butt_cum", at_list=_ca_at, zorder=10008)

        # Back cum: re-show static if present (from a prior cum-outside)
        if "back" in getattr(girl, "Cum", []):
            renpy.show("%s rcg_back_cum" % girl.gid, tag="rcg_back_cum", at_list=_ca_at, zorder=10051)

        # Face cum: re-show static if present (from a prior cum-on-face)
        if "face" in getattr(girl, "Cum", []):
            renpy.show("%s rcg_cum_face" % girl.gid, tag="rcg_cum_face", at_list=_ca_at, zorder=10053)

        # Thigh highs if wearing
        if getattr(girl, "Shoes", None):
            renpy.show("%s rcg_thigh_highs" % girl.gid, tag="rcg_thigh_highs", at_list=_ca_at, zorder=9968)

        # Panties static (if wearing)
        _ca_pan = girl.Panties
        if _ca_pan:
            _ca_pan_state = girl.clothes_state.get("panties", "full")
            _ca_pan_img = "%s rcg_panties_%s_%s" % (girl.gid, _ca_pan, _ca_pan_state)
            _ca_pan_z = 9965 if _ca_pan_state == "down" else 10006
            renpy.show(_ca_pan_img, tag="rcg_panties", at_list=_ca_at, zorder=_ca_pan_z)
            # Side layer 2
            _ca_pan2 = "%s rcg_panties_%s_side2" % (girl.gid, _ca_pan)
            if _ca_pan_state == "side" and renpy.has_image(_ca_pan2, exact=True):
                renpy.show(_ca_pan2, tag="rcg_panties2", at_list=_ca_at, zorder=9965)
            else:
                renpy.hide("rcg_panties2")
            # Side bottom: freeze static
            _ca_pan_sb = "%s rcg_panties_%s_side_bottom" % (girl.gid, _ca_pan)
            if _ca_pan_state == "side" and renpy.has_image(_ca_pan_sb):
                renpy.show(_ca_pan_sb, tag="rcg_panties_side_bottom", at_list=_ca_at, zorder=9965)
            else:
                renpy.hide("rcg_panties_side_bottom")
        else:
            renpy.hide("rcg_panties")
            renpy.hide("rcg_panties2")

        # Hide penis, condom, grab, rub_top
        renpy.hide("rcg_penis")
        renpy.hide("rcg_condom")
        renpy.hide("rcg_penis_cum")
        renpy.hide("rcg_rub_top")
        renpy.hide("rcg_grab_left")
        renpy.hide("rcg_grab_right")

    return

# (Old _rcg_escalation_check removed — now uses centralized _girl_escalation_check)


# ============================================================
# End
# ============================================================
label RCG_End(girl, dress_up=True):
    $ debug_log("[DEBUG] RCG_End: entered, dress_up=%s" % str(dress_up))
    $ scene_full_cleanup(girl)
    $ finalize_recording()
    $ _player_cleanup(girl)

    $ pose = getattr(girl, "_prev_pose", "standing")
    $ slot = _safe_restore_slot(getattr(girl, "_prev_slot", StageCenter))

    python:
        slot_transform = _slot_to_transform(slot)
        _reset_expression_state(girl)

        store._rcg_girl = None
        store._srcg_girl = None
        store.rcg_blink = False
        store.rcg_started = False
        store.rcg_butt_state = "butt_top_none"
        girl.ResetVisuals(pose=pose, at_list=[slot_transform])
        _hide_scene_layers("reverse_cowgirl")
        if callable(globals().get("_srcg_hide_all")):
            _srcg_hide_all()
        store.rcg_arms_pose = 1
        store.rcg_grab = False
        store.rcg_hold = False
        store.rcg_anal = False
        store.rcg_rub_mode = False
        store.rcg_tip_mode = False
        store.hiding_face = False
        store.condom_active = False

    if dress_up:
        call DressUp_Sequence(girl) from _call_DressUp_Sequence_4
    $ debug_log("[DEBUG] RCG_End: returning")
    return

# ============================================================
# Rub Mode - Launch
# ============================================================
label RCG_RubLaunch(girl):
    $ sub_event_reset(girl)

    $ public_attention_reset()
    call PlayerExposure(girl) from _call_PlayerExposure_rub

    $ girl._prev_pose = getattr(girl, "default_pose", "standing")
    $ girl._prev_slot = getattr(girl, "SpriteLoc", StageCenter)
    if not getattr(girl, "_saved_outfit", None):
        $ girl.SaveOutfit()

    python:
        store._rcg_girl = girl
        store.rcg_started = False
        store.rcg_rub_mode = True
        store.rcg_butt_state = "butt_top_1"
        if girl.gid == "shion":
            store._srcg_girl = girl
        # Clear standing sprite before showing RCG pose
        hide_girl_sprite(girl)

    if "rcg_speed" not in globals():
        $ rcg_speed = 0

    call RCG_ApplySpeed(girl, 0) from _call_RCG_ApplySpeed_rub_launch
    with fade

    # Start blink + expression threads
    python:
        if girl.gid == "shion":
            renpy.invoke_in_thread(_scene_cs_blink_loop, girl, "_rcg_girl", is_active_fn=_rcg_is_active)
        else:
            renpy.invoke_in_thread(_scene_blink_loop, girl, "_rcg_girl", "rcg_blink", is_active_fn=_rcg_is_active, cs_girls=_rcg_cs_girls())
        renpy.invoke_in_thread(_rcg_expression_cycle, girl)

    return

# ═══════════════════════════════════════════════════════════
# _rcg_esc_dispatch — visual transitions after _escalation_menu
# Handles state vars, condom, visuals, and enters the next menu
# ═══════════════════════════════════════════════════════════
label _rcg_esc_dispatch(girl, from_state, current_speed):
    if store._esc_result != "accepted":
        return

    # ── De-escalation ──────────────────────────────────────
    if store._esc_is_deescalation:
        if store._esc_target == "rub":
            python:
                store.rcg_rub_mode = True
                store.rcg_tip_mode = False
                store.rcg_started = False
                store.rcg_anal = False   # the rub is never anal
            call RCG_ApplySpeed(girl, 0) from _call_RCG_ApplySpeed_deesc_rub
            call RCG_RubControlMenu(girl) from _call_RCG_RubCM_deesc
            return
        elif store._esc_target == "tip":
            # (the tip stays in the hole he is in: an anal scene goes back to the anal tip)
            $ store.rcg_tip_mode = True
            call RCG_ApplySpeed(girl, 1) from _call_RCG_ApplySpeed_deesc_tip
            call RCG_TipControlMenu(girl) from _call_RCG_TipCM_deesc
            return
        return

    # ── Tip (from rub) ─────────────────────────────────────
    if store._esc_target == "tip":
        if girl.Over and _gsc(girl.gid, "over_blocks_penetration", False, "rcg"):
            $ girl.Outfit_Change(over="none", pose="reverse_cowgirl")
            call RCG_ApplySpeed(girl, current_speed) from _call_RCG_ApplySpeed_esc_tip_strip_over
        call _rcg_bottom_clothes_menu(girl) from _call_rcg_bottom_esc_tip
        python:
            store.rcg_rub_mode = False
            store.rcg_tip_mode = True
            store.rcg_started = True
            # the anal tip ("Ask to put the tip in her ass"): only a girl whose art has anal in this pose is offered it
            store.rcg_anal = bool(store._esc_anal_choice) and rcg_has_anal(girl)
        call RCG_ApplySpeed(girl, 0) from _call_RCG_ApplySpeed_esc_tip_strip
        call RCG_PenisEnterAnim(girl) from _call_RCG_PenisEnterAnim_esc_tip
        if store.rcg_anal:
            $ _watcher_scene_comment("anal_enter")
        call RCG_ApplySpeed(girl, 1) from _call_RCG_ApplySpeed_esc_tip

        if store._esc_was_forced:
            $ Say_Line(girl, _esc_pick_line(girl, _ESC_TIP_FORCE_ACCEPT))
            $ Say_Player(_("It's just the tip, I promise..."))
            $ Say_Line(girl, _tl(renpy.random.choice(_ESC_TIP_FORCE_REACT)))

        call RCG_TipControlMenu(girl) from _call_RCG_TipCM_esc_tip
        return

    # ── Anal (from rub or tip): a girl whose art has it (ESCALATION_CAPS reads rcg_has_anal) ──
    if store._esc_target == "anal" and from_state != "sex":
        if from_state == "rub":
            if girl.Over and _gsc(girl.gid, "over_blocks_penetration", False, "rcg"):
                $ girl.Outfit_Change(over="none", pose="reverse_cowgirl")
                call RCG_ApplySpeed(girl, current_speed) from _call_RCG_ApplySpeed_esc_anal_strip_over
            call _rcg_bottom_clothes_menu(girl) from _call_rcg_bottom_esc_anal
        python:
            store.rcg_rub_mode = False
            store.rcg_tip_mode = False
            # no condom in her ass (the same rule as every anal position)
            store.condom_active = False
            store.condom_denied = False
        $ _scene_escalation(girl, "anal", "reverse_cowgirl")
        call RCG_HoleTransition(girl, True) from _call_RCG_HoleT_esc_anal
        $ rcg_speed = store._esc_speed
        call RCG_ApplySpeed(girl, rcg_speed) from _call_RCG_ApplySpeed_esc_anal

        if store._esc_was_forced:
            $ Say_Line(girl, _tl(renpy.random.choice(_ESC_ANAL_FORCE_POST)))

        call RCG_ControlMenu(girl) from _call_RCG_CM_esc_anal
        if not getattr(store, "_sub_event_position_switched", False):
            $ _track_raw_sex_start(girl)
        return

    # ── Anal from sex (hole switch) ────────────────────────
    if store._esc_target == "anal" and from_state == "sex":
        if store._esc_was_forced:
            $ set_scene_expression(girl, "surprised")
            call RCG_ApplySpeed(girl, current_speed) from _call_RCG_ApplySpeed_sw_fa_pre
            $ Say_Line(girl, _tl(renpy.random.choice(_ESC_SWITCH_TO_ANAL_PRE)))
            $ _scene_position_switch(girl, "reverse_cowgirl", "anal")
            $ mark_intimacy(girl, "anal")
            $ sex_accept_with_temptation(girl, "anal")
        else:
            $ _scene_position_switch(girl, "reverse_cowgirl", "anal")
            $ mark_intimacy(girl, "anal")

        $ Change_Status(girl, "Obed", 8)
        $ Change_Status(girl, "Inbt", 5)
        python:
            store.condom_active = False
            store.condom_denied = False
        call RCG_HoleTransition(girl, True) from _call_RCG_HoleT_sw_p2a
        call RCG_ApplySpeed(girl, current_speed) from _call_RCG_ApplySpeed_sw_p2a

        if store._esc_was_forced:
            $ Say_Line(girl, _tl(renpy.random.choice(_ESC_SWITCH_TO_ANAL_POST)))
        return

    # ── Sex from anal (hole switch, the ATP hygiene check already ran in _esc_ask_sex_from_anal) ──
    if store._esc_target == "sex" and from_state == "anal":
        python:
            _atp_outcome = store._esc_atp_result.get("outcome", "accept_raw") if store._esc_atp_result else "accept_raw"

        if _atp_outcome == "require_condom":
            $ Say_Line(girl, _atp_switch_line(girl, forced=store._esc_was_forced))   # pools: _ATP_SWITCH_LINES (escalation.rpy)
            # he pulls out while the condom goes on
            $ store._saved_rcg_started = store.rcg_started
            $ store.rcg_started = False
            call RCG_ApplySpeed(girl, 0) from _call_RCG_ApplySpeed_rest_sw_atp
            call condom_check(girl, True, "hard_deny") from _call_condom_sw_atp_rcg
            $ store.rcg_started = store._saved_rcg_started
            if store.condom_denied:
                call RCG_ApplySpeed(girl, current_speed) from _call_RCG_ApplySpeed_sw_atp_deny
                return

        if _atp_outcome == "accept_raw" and _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False):
            $ store._saved_rcg_started = store.rcg_started
            $ store.rcg_started = False
            call RCG_ApplySpeed(girl, 0) from _call_RCG_ApplySpeed_rest_sw_cheat
            call condom_check(girl, True, "hard_deny") from _call_condom_sw_cheat_rcg
            $ store.rcg_started = store._saved_rcg_started
            if store.condom_denied:
                call RCG_End(girl, dress_up=False) from _call_RCG_End_sw_cheat
                call _cheat_no_condom_breakdown(girl) from _call_condom_snap_sw_cheat_rcg
                return

        if store._esc_was_forced:
            $ set_scene_expression(girl, "surprised")
            $ Say_Line(girl, _tl(renpy.random.choice(_ESC_SWITCH_TO_PUSSY_PRE)))

        $ _scene_position_switch(girl, "anal", "reverse_cowgirl")
        if store._esc_was_forced:
            $ sex_accept_with_temptation(girl, "sex")
            $ Change_Status(girl, "Obed", 3)
            $ Change_Status(girl, "Inbt", 3)
        elif _is_on_cheat_path(girl) and _cheat_stage(girl) < 3:
            $ Say_Line(girl, _cheat_sex_first_line(girl))
        else:
            $ Say_Line(girl, _esc_pick_line(girl, _ESC_SWITCH_TO_PUSSY_ASK))

        call RCG_HoleTransition(girl, False) from _call_RCG_HoleT_sw_a2p
        call RCG_ApplySpeed(girl, current_speed) from _call_RCG_ApplySpeed_sw_a2p

        if store._esc_was_forced:
            $ Say_Line(girl, _tl(renpy.random.choice(_ESC_SWITCH_TO_PUSSY_POST)))
        return

    # ── Sex (from rub or tip) ──────────────────────────────
    if store._esc_target == "sex":
        $ _from_tip = (from_state == "tip")

        if not _from_tip:
            if girl.Over and _gsc(girl.gid, "over_blocks_penetration", False, "rcg"):
                $ girl.Outfit_Change(over="none", pose="reverse_cowgirl")
                call RCG_ApplySpeed(girl, current_speed) from _call_RCG_ApplySpeed_esc_sex_strip_over
            call _rcg_bottom_clothes_menu(girl) from _call_rcg_bottom_esc_sex

        python:
            store.rcg_rub_mode = False
            store.rcg_tip_mode = False
            store.rcg_anal = False   # from an anal tip this is the switch to her pussy (he goes in again below)
            store._saved_rcg_started = store.rcg_started
            store.rcg_started = False
        call RCG_ApplySpeed(girl, 0) from _call_RCG_ApplySpeed_rest_esc_sex

        if store._esc_was_forced:
            if _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False):
                call condom_check(girl, True, "hard_deny") from _call_condom_esc_rcg_sex_f_cheat
                if store.condom_denied:
                    $ store.rcg_started = store._saved_rcg_started
                    call RCG_End(girl, dress_up=False) from _call_RCG_End_esc_sex_f_cond
                    call _cheat_no_condom_breakdown(girl) from _call_condom_snap_esc_rcg_sex_f
                    return
            else:
                # She refuses raw: decide it NOW, before the act is counted and before a virgin loses it
                if not getattr(store, "_esc_skip_condom", False) and not _force_raw_accepts(girl):
                    call force_raw(girl) from _call_force_raw_esc_rcg_sex_pre
                    if store.condom_denied:
                        $ store.rcg_started = store._saved_rcg_started
                        call RCG_End(girl, dress_up=False) from _call_RCG_End_esc_sex_f_deny_pre
                        return
                # Defer force_raw until after visual transition (penis visible during dialogue)
                python:
                    store.condom_active = False
                    store.condom_denied = False
                    store._force_raw_pending = True
        else:
            if _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False):
                call condom_check(girl, True, "hard_deny") from _call_condom_esc_rcg_sex_a_cheat
            else:
                $ _pen = store._esc_pen_result
                call condom_check(girl, _pen["condom_required"], _pen["raw_outcome"]) from _call_condom_esc_rcg_sex_a
            if store.condom_denied:
                if _is_on_cheat_path(girl):
                    $ store.rcg_started = store._saved_rcg_started
                    call RCG_End(girl, dress_up=False) from _call_RCG_End_esc_sex_a_cond
                    call _cheat_no_condom_breakdown(girl) from _call_condom_snap_esc_rcg_sex_a
                    return
                python:
                    store.rcg_rub_mode = (from_state == "rub")
                    store.rcg_tip_mode = _from_tip
                    store.rcg_started = store._saved_rcg_started
                call RCG_ApplySpeed(girl, current_speed) from _call_RCG_ApplySpeed_esc_sex_cond_deny
                return

        $ store.rcg_started = store._saved_rcg_started
        if not store.condom_denied:
            $ _scene_escalation(girl, "sex", "reverse_cowgirl")
            $ _had_condom_esc = store.condom_active
            python:
                store.rcg_rub_mode = False
                store.rcg_tip_mode = False
                # From RUB the saved rcg_started is False (the rub never sets it), and
                # ApplySpeed then kept butt_top_1: the penis pumped at z 9970 hidden
                # behind the closed butt art. It IS sex now (DG / FN set this inside
                # their HoleTransition; RCG enters the penis directly).
                store.rcg_started = True
                print("[RCG_ESC] sex from %s: rcg_started forced True" % from_state)
            call RCG_PenisEnterAnim(girl) from _call_RCG_PenisEnterAnim_esc_sex
            if store._esc_virgin_check:
                call virgin_first_time(girl, "reverse_cowgirl") from _call_virgin_esc_rcg_sex
            $ rcg_speed = store._esc_speed
            call RCG_ApplySpeed(girl, rcg_speed) from _call_RCG_ApplySpeed_esc_sex_go

            # ── Deferred force_raw — penis now visible ──
            if getattr(store, "_force_raw_pending", False):
                $ store._force_raw_pending = False
                call force_raw(girl) from _call_force_raw_esc_rcg_sex
                if store.condom_denied:
                    call RCG_End(girl, dress_up=False) from _call_RCG_End_esc_sex_f_deny
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

            call RCG_ControlMenu(girl) from _call_RCG_CM_esc_sex
            if not _had_condom_esc and not store._condom_removed_midscene and not getattr(store, "_sub_event_position_switched", False):
                python:
                    _track_raw_sex_start(girl)
        return

    return

# ============================================================
# Rub Mode - Control Menu
# ============================================================
label RCG_RubControlMenu(girl):

    $ store._scene_phase = "rub"
    if "rcg_speed" not in globals():
        $ rcg_speed = 1

    while True:

        if _scene_should_exit():
            return

        if Round >= 100:
            $ Say_Line(girl, _scene_time_up_line())
            call RCG_End(girl, dress_up=False) from _call_RCG_End_timeout_rub
            return

        $ debug_log("[DEBUG] RCG_RubControlMenu: top of loop, speed=%s rub_mode=%s stage=%s" % (rcg_speed, store.rcg_rub_mode, getattr(girl, "_cheat_sex_stage", 0)))
        menu:
            "Keep going" if rcg_speed >= 1:
                $ debug_log("[DEBUG] RUB_MENU: clicked KEEP GOING")
                $ advance_round(TIME_COSTS["sex_tick"])
                $ add_player_focus(get_player_lust_gain("reverse_cowgirl", rcg_speed))
                $ _girl_lust_gain(girl, (2 if rcg_speed == 1 else 3 if rcg_speed == 2 else 5), rcg_speed)
                $ _moan = scene_moan_tick(girl, "reverse_cowgirl", rcg_speed)
                if _moan:
                    call _moan_say(girl, _moan) from _call_ms_rcg_kg

                # Path 1: first rub commentary
                if getattr(store, "_path1_rub_first_line_pending", False):
                    $ store._path1_rub_first_line_pending = False
                    $ Say_Line(girl, _cheat_rub_midline(girl))

                # Cheat path breaking point (can fire during rub too)
                if _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False):
                    if _cheat_breaking_point_ready(girl) and renpy.random.random() < 0.30:
                        call _cheat_breaking_point(girl, "reverse_cowgirl") from _call_cheat_break_dg_rub

                # Public attention
                $ _pa_caught = public_attention_tick(girl, "keep_going", rcg_speed)
                if _pa_caught:
                    if not _caught_keeps_going(girl):
                        call RCG_End(girl, dress_up=False) from _call_RCG_End_rub_pa
                    call caught_in_public(girl, "reverse_cowgirl") from _call_caught_public_rub_kg
                    return

                call _sex_interruption_check(girl, "reverse_cowgirl") from _call_interrupt_rcg_rub
                $ store._witness_expression_lock = False
                if store._sex_interrupted:
                    call RCG_End(girl, dress_up=False) from _call_RCG_End_rub_int
                    return

                call _npc_partner_detection_tick(girl, "reverse_cowgirl") from _call_npc_detect_rcg_rub
                if store._npc_witness_scene_aborted:
                    call RCG_End(girl, dress_up=False) from _call_RCG_End_rub_npc
                    return

                $ _se = sub_event_tick(girl, "reverse_cowgirl")
                if _se:
                    call SubEvent_Handle(girl, "reverse_cowgirl", _se) from _call_SubEvent_Handle_rcg_rub
                    if store._sub_event_position_switched:
                        $ store._sub_event_position_switched = False
                        return

                call _cheat_bf_call_check(girl, "reverse_cowgirl") from _call_cheat_bf_rcg_rub

                # Spontaneous escalation: she wants more
                call _girl_escalation_check(girl, "rub") from _call_girl_esc_rcg_rub
                if store._girl_esc_accepted:
                    if girl.Over and _gsc(girl.gid, "over_blocks_penetration", False, "rcg"):
                        $ girl.Outfit_Change(over="none", pose="reverse_cowgirl")
                        call RCG_ApplySpeed(girl, rcg_speed) from _call_RCG_ApplySpeed_esc_strip_over2
                    call _rcg_bottom_clothes_menu(girl) from _call_rcg_bottom_menu_esc_tip2
                    $ store.rcg_rub_mode = False
                    $ store.rcg_tip_mode = True
                    $ store.rcg_started = True
                    call RCG_ApplySpeed(girl, 0) from _call_RCG_ApplySpeed_esc_strip2
                    call RCG_PenisEnterAnim(girl) from _call_RCG_PenisEnterAnim_esc_rub_tip2
                    call RCG_ApplySpeed(girl, 1) from _call_RCG_ApplySpeed_esc_rub_tip2
                    call RCG_TipControlMenu(girl) from _call_RCG_TipControlMenu_esc2
                    return

                if girl.Lust >= 100:
                    call GirlCumming(girl, "reverse_cowgirl", "reverse_cowgirl", scene_override="rub") from _call_GirlCumming_rub
                if player_is_cumming():
                    if focus_overdue_tick():
                        call ForcedCumOverdue(girl, "reverse_cowgirl") from _call_ForcedCumOverdue_rcg_rub
                        $ _handle_post_cum_exit("reverse_cowgirl", "rub")
                        return

            "Speed up" if rcg_speed < 3:
                $ advance_round(TIME_COSTS["sex_tick"])
                $ debug_log("[DEBUG] RUB_MENU: clicked SPEED UP")
                $ rcg_speed += 1
                call RCG_ApplySpeed(girl, rcg_speed) from _call_RCG_ApplySpeed_rub_su
                $ add_player_focus(get_player_lust_gain("reverse_cowgirl", rcg_speed))
                $ _girl_lust_gain(girl, (2 if rcg_speed == 1 else 3 if rcg_speed == 2 else 5), rcg_speed)
                $ Narration(_("You rub faster."))

            "Speed down" if rcg_speed > 0:
                $ advance_round(1)
                $ rcg_speed -= 1
                call RCG_ApplySpeed(girl, rcg_speed) from _call_RCG_ApplySpeed_rub_sd
                $ Narration(_("You slow down."))

            "Grab her ass" if not rcg_grab and rcg_has_grab(girl):
                $ advance_round(1)
                $ rcg_grab = True
                call RCG_ApplySpeed(girl, rcg_speed) from _call_RCG_ApplySpeed_rub_grab
                python:
                    _grab_react = renpy.random.choice(["mouth_surprised", "mouth_tongue", "mouth_kiss"])
                    set_scene_expression(girl, None, mouth=_grab_react)
                call RCG_ApplySpeed(girl, rcg_speed) from _call_RCG_ApplySpeed_rub_grab_r

            "Let go" if rcg_grab:
                $ advance_round(1)
                $ rcg_grab = False
                call RCG_ApplySpeed(girl, rcg_speed) from _call_RCG_ApplySpeed_rub_letgo

            "Hold her down" if not rcg_hold and rcg_has_hold(girl):
                $ advance_round(1)
                call RCG_Hold(girl, True) from _call_RCG_Hold_rub_on

            "Let go of her" if rcg_hold and rcg_has_hold(girl):
                $ advance_round(1)
                call RCG_Hold(girl, False) from _call_RCG_Hold_rub_off

            "Spank her":
                $ advance_round(1)
                call SpankHer(girl, "reverse_cowgirl") from _call_SpankHer_rub

            "Strip her" if not getattr(store, "_scene_restricted", False):
                $ advance_round(1)
                call RCG_RubStripMenu(girl) from _call_RCG_RubStripMenu

            "Penetration...":
                call _escalation_menu(girl, "reverse_cowgirl") from _call_esc_menu_rcg_rub
                if store._esc_result == "accepted":
                    call _rcg_esc_dispatch(girl, "rub", rcg_speed) from _call_esc_disp_rcg_rub
                    return
                elif store._esc_result == "scene_ended":
                    call RCG_End(girl, dress_up=False) from _call_RCG_End_esc_rub
                    return

            "{color=#fbbf24}Cum{/color}" if player_is_cumming():
                call PlayerCumMenu_RubOutside(girl) from _call_PlayerCumMenu_RubOutside_voluntary
                $ _handle_post_cum_exit("reverse_cowgirl", "rub")
                return

            "Stop now":
                call _scene_stop_reaction(girl) from _call_stop_react_rcg_rub
                if store._stop_accepted:
                    return

# ============================================================
# Rub Mode - Cum Menu (outside only)
# ============================================================
label PlayerCumMenu_RubOutside(girl):

    "You feel yourself getting close..."

    menu:
        "Fire away":
            call RCG_CumOutsideFreeze(girl) from _call_RCG_CumOutsideFreeze_rub_fire
            "You cum."
            $ process_cum(girl, "reverse_cowgirl", "away")
            $ apply_cum_bonuses(girl, "cum_outside")

        "Cum outside":
            $ _dg_cum_type = "ass"
            menu:
                "On her face":
                    $ _dg_cum_type = "face"
                "On her ass":
                    $ _dg_cum_type = "ass"
                "On her back":
                    $ _dg_cum_type = "back"
                "All over her":
                    $ _dg_cum_type = "outside"

            call RCG_CumOutsideFreeze(girl) from _call_RCG_CumOutsideFreeze_rub_out

            if _dg_cum_type == "face":
                "You cum on her face."
                $ process_cum(girl, "reverse_cowgirl", "face")
            elif _dg_cum_type == "ass":
                "You cum on her ass."
                $ process_cum(girl, "reverse_cowgirl", "ass")
            elif _dg_cum_type == "back":
                "You cum on her back."
                $ process_cum(girl, "reverse_cowgirl", "back")
            else:
                "You cum all over her."
                $ process_cum(girl, "reverse_cowgirl", "outside", ["ass", "back", "face"])

            $ apply_cum_bonuses(girl, "cum_outside")
            $ _cum_say_line(girl, _dg_cum_type, "reverse_cowgirl")

    return

# ============================================================
# Rub Mode - Strip Menu
# ============================================================
label RCG_RubStripMenu(girl):
    while True:
        $ _legs_label = _("Remove pants") if _strip_name_for_slot(girl, "skirt") == "pants" else _("Remove skirt")
        menu:
            "Lift skirt up" if girl.Legs and _item_has_state(girl, "skirt", "up") and girl.clothes_state.get("skirt") != "up":
                call _strip_approval(girl, ["legs"]) from _call__strip_approval_rub_skirt_up
                if store._strip_approved:
                    $ girl.clothes_state["skirt"] = "up"
                    call RCG_RefreshClothing(girl) from _call_RCG_RefreshClothing_rub_skirt_up
                    call CheckExposure(girl) from _call_CheckExposure_rub_skirt_up

            "[_legs_label]" if girl.Legs:
                call _strip_approval(girl, ["legs"]) from _call__strip_approval_rub_legs
                if store._strip_approved:
                    $ girl.clothes["skirt"] = None
                    $ girl.clothes_state["skirt"] = "full"
                    call RCG_RefreshClothing(girl) from _call_RCG_RefreshClothing_rub_skirt
                    call CheckExposure(girl) from _call_CheckExposure_rub_skirt

            "Remove panties" if girl.Panties:
                call _strip_approval(girl, ["panties"]) from _call__strip_approval_rub_panties
                if store._strip_approved:
                    $ girl.clothes["panties"] = None
                    $ girl.clothes_state["panties"] = "full"
                    call RCG_RefreshClothing(girl) from _call_RCG_RefreshClothing_rub_pan
                    call CheckExposure(girl) from _call_CheckExposure_rub_pan

            "Pull panties to the side" if girl.Panties and _panties_next_state(girl) == "side":
                call _strip_approval(girl, ["panties"]) from _call__strip_approval_rub_pan_side
                if store._strip_approved:
                    $ girl.clothes_state["panties"] = "side"
                    call RCG_RefreshClothing(girl) from _call_RCG_RefreshClothing_rub_pan_side
                    call CheckExposure(girl) from _call_CheckExposure_rub_pan_side

            "Pull panties down" if girl.Panties and _panties_next_state(girl) == "down":
                call _strip_approval(girl, ["panties"]) from _call__strip_approval_rub_pan_down
                if store._strip_approved:
                    $ girl.clothes_state["panties"] = "down"
                    call RCG_RefreshClothing(girl) from _call_RCG_RefreshClothing_rub_pan_down
                    call CheckExposure(girl) from _call_CheckExposure_rub_pan_down

            "Remove top" if girl.Over:
                call _strip_approval(girl, ["over"]) from _call__strip_approval_rub_over
                if store._strip_approved:
                    $ girl.clothes["over"] = None
                    call RCG_RefreshClothing(girl) from _call_RCG_RefreshClothing_rub_over
                    call CheckExposure(girl) from _call_CheckExposure_rub_over

            "Pull chest up" if girl.Chest and girl.clothes_state.get("chest") != "up" and _item_has_state(girl, "chest", "up"):
                call _strip_approval(girl, ["chest"]) from _call__strip_approval_rub_chest_up
                if store._strip_approved:
                    $ girl.clothes_state["chest"] = "up"
                    call RCG_RefreshClothing(girl) from _call_RCG_RefreshClothing_rub_chest_up
                    call CheckExposure(girl) from _call_CheckExposure_rub_chest_up

            "Remove chest" if girl.Chest:
                call _strip_approval(girl, ["chest"]) from _call__strip_approval_rub_chest
                if store._strip_approved:
                    $ girl.clothes["chest"] = None
                    $ girl.clothes_state["chest"] = "full"
                    call RCG_RefreshClothing(girl) from _call_RCG_RefreshClothing_rub_chest
                    call CheckExposure(girl) from _call_CheckExposure_rub_chest

            "Remove shoes" if getattr(girl, "Shoes", None):
                $ girl.clothes["shoes"] = None
                call RCG_RefreshClothing(girl) from _call_RCG_RefreshClothing_rub_shoes

            "Back":
                return

# ============================================================
# Just The Tip - Launch
# ============================================================
label RCG_TipLaunch(girl):
    $ sub_event_reset(girl)

    $ public_attention_reset()
    call PlayerExposure(girl) from _call_PlayerExposure_tip

    $ girl._prev_pose = getattr(girl, "default_pose", "standing")
    $ girl._prev_slot = getattr(girl, "SpriteLoc", StageCenter)
    if not getattr(girl, "_saved_outfit", None):
        $ girl.SaveOutfit()

    python:
        store._rcg_girl = girl
        store.rcg_started = False
        store.rcg_tip_mode = False
        store.rcg_hold = False
        store.rcg_butt_state = "butt_top_1"
        # rcg_anal is NOT reset here: start_scene set it just before (the anal tip, a girl whose art has it)
        if not rcg_has_anal(girl):
            store.rcg_anal = False
        store._rcg_had_anal = False
        if girl.gid == "shion":
            store._srcg_girl = girl
        # her standing sprite goes for every girl (RCG_Launch): layers with tags of their own never replace it
        hide_girl_sprite(girl)
        sprite_state.setdefault(girl.Id, {})["pose"] = "reverse_cowgirl"
        if girl.Over and _gsc(girl.gid, "over_blocks_penetration", False, "rcg"):
            girl.Outfit_Change(over="none", pose="reverse_cowgirl")

    $ rcg_speed = 1

    # Show static RCG pose with clothes (no animation yet)
    if girl.gid == "shion":
        call RCG_ApplySpeed(girl, 0) from _call_RCG_ApplySpeed_tip_shion
    else:
        $ set_girl_sprite(girl, pose="reverse_cowgirl")
    with fade

    # --- BOTTOM CLOTHES MENU (skirt then panties) ---
    call _rcg_bottom_clothes_menu(girl) from _call_rcg_bottom_menu_tip

    # NOW mark scene as started and begin animation
    $ store.rcg_started = True
    $ store.rcg_tip_mode = True
    if store.rcg_anal:
        $ _watcher_scene_comment("anal_enter")
    call RCG_ApplySpeed(girl, 1) from _call_RCG_ApplySpeed_tip_launch

    # Start blink + expression threads
    python:
        if girl.gid == "shion":
            renpy.invoke_in_thread(_scene_cs_blink_loop, girl, "_rcg_girl", is_active_fn=_rcg_is_active)
        else:
            renpy.invoke_in_thread(_scene_blink_loop, girl, "_rcg_girl", "rcg_blink", is_active_fn=_rcg_is_active, cs_girls=_rcg_cs_girls())
        renpy.invoke_in_thread(_rcg_expression_cycle, girl)

    return

# ============================================================
# Just The Tip - Control Menu (locked at speed 1)
# ============================================================
label RCG_TipControlMenu(girl):

    $ store._scene_phase = "tip"
    $ store._cheat_shower_max_act = "tip"
    $ rcg_speed = 1
    $ store._anal_tip_counted = False

    while True:
        # the scene's type right now: "reverse_cowgirl", or its anal variant for the anal tip (rcg_scene_type)
        $ _rcg_scene = rcg_scene_type()

        if _scene_should_exit():
            return

        if Round >= 100:
            $ Say_Line(girl, _scene_time_up_line())
            call RCG_End(girl, dress_up=False) from _call_RCG_End_timeout_tip
            return

        $ debug_log("[DEBUG] RCG_TipControlMenu loop: scene=%s path=%s stage=%s tip_just=%s can_sex=%s" % (_rcg_scene, getattr(girl, "_cheat_escalation_path", 0), getattr(girl, "_cheat_sex_stage", 0), getattr(store, "_cheat_tip_just_done", False), _cheat_can_sex(girl) if _is_on_cheat_path(girl) else "N/A"))

        menu:
            "Keep going":
                $ advance_round(TIME_COSTS["sex_tick"])
                $ add_player_focus(get_player_lust_gain(_rcg_scene, 1))
                if store.rcg_anal:
                    # the anal tip: her Lust follows the anal rules (anal_lover / anal_hater), like the doggy's anal tip
                    $ _girl_lust_gain(girl, _anal_tip_lust(girl), 1)
                    $ _apply_anal_lust_cap(girl, True)
                    $ _count_anal_tip(girl, True)
                else:
                    $ _girl_lust_gain(girl, 2, 1)
                $ _moan = scene_moan_tick(girl, _rcg_scene, 1)
                if _moan:
                    call _moan_say(girl, _moan) from _call_ms_rcg_su

                # Path 1: first tip commentary
                if getattr(store, "_path1_tip_first_line_pending", False):
                    $ store._path1_tip_first_line_pending = False
                    $ Say_Line(girl, _cheat_tip_midline(girl))

                # Cheat path breaking point (can fire during tip too)
                if _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False):
                    if _cheat_breaking_point_ready(girl) and renpy.random.random() < 0.30:
                        call _cheat_breaking_point(girl, "reverse_cowgirl") from _call_cheat_break_dg_tip

                $ _pa_caught = public_attention_tick(girl, "keep_going", 1)
                if _pa_caught:
                    if not _caught_keeps_going(girl):
                        call RCG_End(girl, dress_up=False) from _call_RCG_End_tip_pa
                    call caught_in_public(girl, _rcg_scene) from _call_caught_public_tip_kg
                    return

                call _sex_interruption_check(girl, _rcg_scene) from _call_interrupt_rcg_tip
                $ store._witness_expression_lock = False
                if store._sex_interrupted:
                    call RCG_End(girl, dress_up=False) from _call_RCG_End_tip_int
                    return

                call _npc_partner_detection_tick(girl, _rcg_scene) from _call_npc_detect_rcg_tip
                if store._npc_witness_scene_aborted:
                    call RCG_End(girl, dress_up=False) from _call_RCG_End_tip_npc
                    return

                $ _se = sub_event_tick(girl, _rcg_scene)
                if _se:
                    call SubEvent_Handle(girl, _rcg_scene, _se) from _call_SubEvent_Handle_rcg_tip
                    if store._sub_event_position_switched:
                        $ store._sub_event_position_switched = False
                        return

                call _cheat_bf_call_check(girl, _rcg_scene) from _call_cheat_bf_rcg_tip

                # Spontaneous escalation: she wants all the way (never from the anal tip, like the doggy's)
                if not store.rcg_anal:
                    call _girl_escalation_check(girl, "tip") from _call_girl_esc_rcg_tip
                    if store._girl_esc_accepted:
                        $ store.rcg_tip_mode = False
                        call _girl_esc_accept_sex(girl, "reverse_cowgirl") from _call_girl_esc_accept_rcg
                        if store._girl_esc_condom_denied:
                            call RCG_End(girl, dress_up=False) from _call_RCG_End_esc_condom
                            call _cheat_no_condom_breakdown(girl) from _call_condom_snap_rcg_esc
                            return
                        $ rcg_speed = 2
                        call RCG_ApplySpeed(girl, 2) from _call_RCG_ApplySpeed_esc_tip_fuck2
                        call RCG_ControlMenu(girl) from _call_RCG_ControlMenu_esc2
                        return

                if girl.Lust >= 100:
                    call GirlCumming(girl, _rcg_scene, _rcg_scene, scene_override="tip") from _call_GirlCumming_tip
                if player_is_cumming():
                    if focus_overdue_tick():
                        call ForcedCumOverdue(girl, _rcg_scene) from _call_ForcedCumOverdue_rcg_tip
                        $ _handle_post_cum_exit("reverse_cowgirl", "tip")
                        return

            "Grab her ass" if not rcg_grab and rcg_has_grab(girl):
                $ advance_round(1)
                $ rcg_grab = True
                call RCG_ApplySpeed(girl, 1) from _call_RCG_ApplySpeed_tip_grab
                python:
                    _grab_react = renpy.random.choice(["mouth_surprised", "mouth_tongue", "mouth_kiss"])
                    set_scene_expression(girl, None, mouth=_grab_react)
                call RCG_ApplySpeed(girl, 1) from _call_RCG_ApplySpeed_tip_grab_r

            "Let go" if rcg_grab:
                $ advance_round(1)
                $ rcg_grab = False
                call RCG_ApplySpeed(girl, 1) from _call_RCG_ApplySpeed_tip_letgo

            "Hold her down" if not rcg_hold and rcg_has_hold(girl):
                $ advance_round(1)
                call RCG_Hold(girl, True) from _call_RCG_Hold_tip_on

            "Let go of her" if rcg_hold and rcg_has_hold(girl):
                $ advance_round(1)
                call RCG_Hold(girl, False) from _call_RCG_Hold_tip_off

            "Spank her":
                $ advance_round(1)
                call SpankHer(girl, _rcg_scene) from _call_SpankHer_tip

            "Strip her" if not getattr(store, "_scene_restricted", False):
                $ advance_round(1)
                call RCG_StripMenu(girl) from _call_RCG_StripMenu_tip

            "Penetration...":
                call _escalation_menu(girl, "reverse_cowgirl") from _call_esc_menu_rcg_tip
                if store._esc_result == "accepted":
                    call _rcg_esc_dispatch(girl, "tip", rcg_speed) from _call_esc_disp_rcg_tip
                    return
                elif store._esc_result == "scene_ended":
                    call RCG_End(girl, dress_up=False) from _call_RCG_End_esc_tip
                    return

            "{color=#fbbf24}Cum{/color}" if player_is_cumming():
                call PlayerCumMenu_TipOutside(girl) from _call_PlayerCumMenu_TipOutside_voluntary
                $ _handle_post_cum_exit("reverse_cowgirl", "tip")
                return

            "Stop now":
                call _scene_stop_reaction(girl) from _call_stop_react_rcg_tip
                if store._stop_accepted:
                    return

# ============================================================
# RCG_TipDeniedCumVisual — outside cum sprites on denied creampie
# ============================================================
label RCG_TipDeniedCumVisual(girl):
    if girl.gid == "shion":
        $ _srcg_show_cum(cum_tags=["ass"])
        return
    python:
        _ca_at = [rcg_slot_speed0]
        renpy.show("%s rcg_butt_cum" % girl.gid, tag="rcg_butt_cum", at_list=_ca_at, zorder=10050)
        renpy.show("%s rcg_cum_face" % girl.gid, tag="rcg_cum_face", at_list=_ca_at, zorder=10053)
    return

# ============================================================
# Just The Tip - Cum Menu
# ============================================================
label PlayerCumMenu_TipOutside(girl):

    "You feel yourself getting close..."
    # the scene's type: the anal variant for the anal tip (his cum then counts as anal, never as a creampie)
    $ _rcg_scene = rcg_scene_type()

    menu:
        "Fire away":
            call RCG_CumOutsideFreeze(girl) from _call_RCG_CumOutsideFreeze_tip_fire
            "You pull out and cum."
            $ process_cum(girl, _rcg_scene, "away")
            $ apply_cum_bonuses(girl, "cum_outside")

        "Cum outside":
            $ _dg_cum_type = "ass"
            menu:
                "On her face":
                    $ _dg_cum_type = "face"
                "On her ass":
                    $ _dg_cum_type = "ass"
                "On her back":
                    $ _dg_cum_type = "back"
                "All over her":
                    $ _dg_cum_type = "outside"

            call RCG_CumOutsideFreeze(girl) from _call_RCG_CumOutsideFreeze_tip_out

            if _dg_cum_type == "face":
                "You pull out and cum on her face."
                $ process_cum(girl, _rcg_scene, "face")
            elif _dg_cum_type == "ass":
                "You pull out and cum on her ass."
                $ process_cum(girl, _rcg_scene, "ass")
            elif _dg_cum_type == "back":
                "You pull out and cum on her back."
                $ process_cum(girl, _rcg_scene, "back")
            else:
                "You pull out and cum all over her."
                $ process_cum(girl, _rcg_scene, "outside", ["ass", "back", "face"])

            $ apply_cum_bonuses(girl, "cum_outside")

        "Ask to cum in her mouth":
            $ _cum_check = CumPermissionCheck(girl, "cum_in_mouth_ask")
            if _cum_check["accepted"]:
                $ Say_Line(girl, scene_pick_line("cum_mouth_accepted", scene=_rcg_scene, girl=girl) or "Go ahead... do it.")
                call _cum_in_mouth_via_bj(girl, _rcg_scene) from _call__cum_in_mouth_via_bj_rcg_tip
            else:
                $ Say_Line(girl, scene_pick_line("cum_mouth_denied", scene=_rcg_scene, girl=girl) or "No way... not in my mouth.")
                call RCG_CumOutsideFreeze(girl) from _call_RCG_CumOutsideFreeze_tip_mouth_denied
                "You pull out and cum on her ass."
                $ process_cum(girl, _rcg_scene, "ass")
                python:
                    if girl.gid != "shion":
                        _ca_at = [rcg_slot_speed0]
                        renpy.show("%s rcg_butt_cum" % girl.gid, tag="rcg_butt_cum", at_list=_ca_at, zorder=10050)
                        renpy.show("%s rcg_cum_face" % girl.gid, tag="rcg_cum_face", at_list=_ca_at, zorder=10053)
                $ apply_cum_bonuses(girl, "cum_outside")

        "Ask to cum inside":
            call _tip_ask_cum_inside(girl, _rcg_scene) from _call_tip_ask_rcg

        "Cum inside her":
            call _tip_force_cum_inside(girl, _rcg_scene) from _call_tip_force_rcg

    return
