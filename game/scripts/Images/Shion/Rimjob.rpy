# ============================================================
# Shion Rimjob -- Completely new pose
# Two head positions (Head 1 / Head 2) with independent
# expression sets. Guy body + buttcheek layers.
# ============================================================

default _rj_girl = None
default _rj_head_pos = 1
default _rj_speed = 0

# ── Rimjob transforms ─────────────────────────────────────
# Life pass (author, 2026-10-09: the penis moves WITH his body, never on its own; his body keeps a minimal life;
# she moves organically, zoom and small turns around pivots instead of plain axis bobbing - the RCG vocabulary,
# rcg_player_breath_press / srcg_*). Pivots, px of the 1920 x 1080 layers, measured on the art (2026-10-09):
# her hips where the torso (1217-1509 x 245-849) folds onto her kneeling legs (tops at y 660-725), and her grip
# on his shaft (Fingers 1581-1669 x 554-593): his breath swells around that point, so what her hand holds and
# what her tongue presses (the cheek, right above it) barely travel. transform_anchor + anchor = pos keeps the
# full-canvas layer in place while it zooms and turns around the pivot (the srcg_butt_land trick).

transform rj_head_bounce(period, amp, rot):
    matrixanchor (1400, 150)
    yoffset 0 matrixtransform RotateMatrix(0, 0, 0)
    ease period / 2.0 yoffset -amp matrixtransform RotateMatrix(0, 0, rot)
    ease period / 2.0 yoffset 0 matrixtransform RotateMatrix(0, 0, 0)
    repeat

# Her head at rest (speed 0): she catches her breath, a soft bob and tilt in her breathing rhythm, never frozen
transform rj_head_idle(period, amp, deg):
    subpixel True
    matrixanchor (1400, 150)
    yoffset 0 matrixtransform RotateMatrix(0, 0, 0)
    ease period * 0.45 yoffset -amp matrixtransform RotateMatrix(0, 0, deg)
    ease period * 0.55 yoffset 0 matrixtransform RotateMatrix(0, 0, 0)
    repeat

transform rj_arm_left_static:
    xoffset 0 yoffset -40

transform rj_arm_left_move(period, y_amp, x_amp):
    xoffset 0 yoffset -40
    ease period / 2.0 xoffset (0 - x_amp) yoffset (-40 - y_amp)
    ease period / 2.0 xoffset 0 yoffset -40
    repeat

# Her torso group at rest (torso, belly, chest, bra, vest, jacket, far arm): she breathes around her hips - the
# ribcage swells (the chest and the shoulders rise, a hair wider on the inhale) - and her weight shifts in a slow,
# tiny sway. One anchor for the whole group: no layer can part from the torso.
transform rj_girl_body_idle(period, zx, zy, sway, sdeg):
    subpixel True
    transform_anchor True
    anchor _RJ_PIVOT_HIPS pos _RJ_PIVOT_HIPS
    xzoom 1.0 yzoom 1.0 rotate 0
    parallel:
        block:
            ease period * 0.45 xzoom zx yzoom zy
            ease period * 0.55 xzoom 1.0 yzoom 1.0
            repeat
    parallel:
        block:
            ease sway * 0.25 rotate sdeg
            ease sway * 0.50 rotate -sdeg
            ease sway * 0.25 rotate 0
            repeat

# The same group while she licks (speed 1-3): the breath goes on, and the push of her face into him travels down
# her back - she leans into him around her hips (rotate, clockwise = toward him) with a small push of the whole
# body, in the head bounce's own period and phase.
transform rj_girl_body_work(period, zx, zy, lick, ldeg, dx, dy):
    subpixel True
    transform_anchor True
    anchor _RJ_PIVOT_HIPS pos _RJ_PIVOT_HIPS
    xzoom 1.0 yzoom 1.0 rotate 0 xoffset 0 yoffset 0
    parallel:
        block:
            ease period * 0.45 xzoom zx yzoom zy
            ease period * 0.55 xzoom 1.0 yzoom 1.0
            repeat
    parallel:
        block:
            ease lick / 2.0 rotate ldeg xoffset dx yoffset (0 - dy)
            ease lick / 2.0 rotate 0 xoffset 0 yoffset 0
            repeat

# Her chest while she licks: the breath and the lean of the torso (the same anchor and params, so the bra and the
# breasts never part from it), plus the hang: her breast follows the push a moment late and a little further, then
# sags back past its rest before it settles.
transform rj_girl_chest_work(period, zx, zy, lick, ldeg, dx, dy):
    subpixel True
    transform_anchor True
    anchor _RJ_PIVOT_HIPS pos _RJ_PIVOT_HIPS
    xzoom 1.0 yzoom 1.0 rotate 0 xoffset 0 yoffset 0
    parallel:
        block:
            ease period * 0.45 xzoom zx yzoom zy
            ease period * 0.55 xzoom 1.0 yzoom 1.0
            repeat
    parallel:
        block:
            ease lick / 2.0 rotate ldeg
            ease lick / 2.0 rotate 0
            repeat
    parallel:
        block:
            pause lick * 0.12
            ease lick * 0.38 xoffset dx yoffset (0 - dy)
            ease lick * 0.30 xoffset (0 - dx * 0.3) yoffset (dy * 0.4)
            ease lick * 0.20 xoffset 0 yoffset 0
            repeat

# Her legs (and what they wear): slow, tiny weight shift
transform rj_idle_sway(period, amp):
    subpixel True
    yoffset 0
    ease period * 0.50 yoffset -amp
    ease period * 0.50 yoffset 0
    repeat

# His whole unit: body, buttcheek, penis and the cum on it all take this one transform, so nothing of his ever
# parts (author, 2026-10-09: the penis moves with his body, never on its own). He breathes (a swell around her
# grip on his shaft, PLAYER_BREATH-sized: smaller reads as static, author the same day) and shifts his weight in
# a slow sway; faster and deeper with the pace.
transform rj_guy_unit(period, zx, zy, sway, sdeg):
    subpixel True
    transform_anchor True
    anchor _RJ_PIVOT_GRIP pos _RJ_PIVOT_GRIP
    xzoom 1.0 yzoom 1.0 rotate 0
    parallel:
        block:
            ease period * 0.45 xzoom zx yzoom zy
            ease period * 0.55 xzoom 1.0 yzoom 1.0
            repeat
    parallel:
        block:
            ease sway * 0.25 rotate sdeg
            ease sway * 0.50 rotate -sdeg
            ease sway * 0.25 rotate 0
            repeat

# The same unit while she licks (speed 1-3): the push of her face rocks him forward a few px (away from her,
# +x) in the lick's period and phase; the whole unit takes it, so the penis rides it too.
transform rj_guy_unit_work(period, zx, zy, sway, sdeg, lick, px):
    subpixel True
    transform_anchor True
    anchor _RJ_PIVOT_GRIP pos _RJ_PIVOT_GRIP
    xzoom 1.0 yzoom 1.0 rotate 0 xoffset 0
    parallel:
        block:
            ease period * 0.45 xzoom zx yzoom zy
            ease period * 0.55 xzoom 1.0 yzoom 1.0
            repeat
    parallel:
        block:
            ease sway * 0.25 rotate sdeg
            ease sway * 0.50 rotate -sdeg
            ease sway * 0.25 rotate 0
            repeat
    parallel:
        block:
            ease lick / 2.0 xoffset px
            ease lick / 2.0 xoffset 0
            repeat

init python:

    # Pivots (px of the 1920 x 1080 layers, measured on the art 2026-10-09, see the transform block's comment)
    _RJ_PIVOT_HIPS = (1350, 790)
    _RJ_PIVOT_GRIP = (1610, 575)

    # (period, head_amp, arm_y, arm_x, head_rot)
    _RJ_SPEED_PARAMS = {
        1: (0.8, 6, 60, 12, 2.0),
        2: (0.5, 10, 80, 16, 3.0),
        3: (0.35, 15, 100, 20, 5.0),
    }

    # Amplitudes sized like the shipped RCG breaths (PLAYER_BREATH yzoom up to 1.028, sway 0.35 deg): the first
    # pass used a fraction of that and the author saw "praticamente estatico" (2026-10-09). At these values her
    # neck travels ~5 px at rest / ~9 px at speed 3, his silhouette ~4-9 px: visible, still calm.

    # Her breath around her hips: speed -> (period, xzoom, yzoom); the sway under it is constant
    _RJ_HER_BREATH = {
        0: (3.6, 1.005, 1.010),
        1: (3.2, 1.006, 1.012),
        2: (2.7, 1.007, 1.014),
        3: (2.0, 1.008, 1.018),
    }
    _RJ_HER_SWAY = (8.0, 0.35)          # (seconds per sway, degrees each side)

    # While she licks (speed 1-3, the period of _RJ_SPEED_PARAMS):
    # speed -> (lean into him deg, body push dx, dy; breast swing dx, dy). The head group rides the torso's
    # transform (chained), so the lean can be this big without the neck ever parting.
    _RJ_WORK = {
        1: (0.7, 2, 2, 5, 7),
        2: (1.1, 3, 3, 8, 10),
        3: (1.5, 4, 4, 12, 14),
    }

    # Her head at rest: (bob px, tilt deg), on her breath's period, on top of the torso's breath
    _RJ_HEAD_IDLE = (3, 0.5)

    # His breath around her grip: speed -> (period, xzoom, yzoom); his sway is constant, and while she licks
    # her push rocks his whole unit by _RJ_GUY_PUSH px in the lick's rhythm
    _RJ_GUY_BREATH = {
        0: (4.0, 1.006, 1.012),
        1: (3.4, 1.007, 1.014),
        2: (2.8, 1.008, 1.016),
        3: (2.2, 1.010, 1.020),
    }
    _RJ_GUY_SWAY = (7.0, 0.4)
    _RJ_GUY_PUSH = {1: 2, 2: 3, 3: 4}

    # Her legs' weight shift: speed -> (period, amp px)
    _RJ_LEG_SWAY = {0: (6.0, 2), 1: (5.0, 2), 2: (4.5, 3), 3: (4.0, 3)}

    def _rj_penis_at(speed):
        """at_list of his whole unit: his body, his buttcheek, his penis and the cum on it are all shown with
        this same transform (rj_guy_unit / _work), so the penis moves with his body and never on its own
        (author, 2026-10-09). While she licks, her push rocks the unit. Core_Rimjob's spurt takes it too, in
        the same interaction = in step."""
        _gp, _gzx, _gzy = _RJ_GUY_BREATH.get(speed, _RJ_GUY_BREATH[0])
        _gsw, _gsdeg = _RJ_GUY_SWAY
        _lick = _RJ_SPEED_PARAMS.get(speed)
        _push = _RJ_GUY_PUSH.get(speed)
        if _lick and _push:
            return [rj_guy_unit_work(_gp, _gzx, _gzy, _gsw, _gsdeg, _lick[0], _push)]
        return [rj_guy_unit(_gp, _gzx, _gzy, _gsw, _gsdeg)]

    def _rj_show_layers(girl=None):
        _rj_apply_speed(girl or store._rj_girl, 0)

    def _rj_hide_all():
        for _tag in ("rj_guy_body", "rj_penis", "rj_torso",
                      "rj_fingers", "rj_arm_left", "rj_belly", "rj_chest",
                      "rj_bra", "rj_vest", "rj_over",
                      "rj_arm_right", "rj_leg_left", "rj_panties",
                      "rj_leg_right", "rj_pants",
                      "rj_lock_back", "rj_head", "rj_hair", "rj_tongue",
                      "rj_guy_buttcheek", "rj_lock_head",
                      "rj_cum_hand", "rj_cum_penis", "rj_cum_spour"):
            renpy.hide(_tag)

    def _rj_switch_head(pos):
        store._rj_head_pos = pos
        if store._rj_girl:
            _rj_apply_speed(store._rj_girl, store._rj_speed)

    def _rj_apply_speed(girl, speed):
        """Show all Rimjob layers with clothing/animation/cum.
        Z-order (back->front):
        GuyBody(9950) Penis(9952) Fingers(9953) ArmL(9953) Torso(9956)
        Belly(9963) Chest(9964) Bra(9965) Vest(9966) ArmR(9970)
        ArmRCl(9971) LegL(9972) Panties(9973) LegR(9974) Pants(9975)
        Jacket(9976) LockBack(9978) Head1(9980) Hair(9982) Tongue(9984)
        Head2(9986) Buttcheek(9988) LockHead(9990)
        Fingers and ArmL animate (stroking) above the penis."""
        store._rj_speed = speed
        _g = girl.gid
        _pierced = getattr(girl, "Piercing", False)
        _head = store._rj_head_pos

        _over = girl.clothes.get("over") if hasattr(girl, "clothes") else None
        _mid = girl.clothes.get("mid") if hasattr(girl, "clothes") else None
        _chest = girl.clothes.get("chest") if hasattr(girl, "clothes") else None
        _chest_up = getattr(girl, "ChestUp", False)

        _params = _RJ_SPEED_PARAMS.get(speed)
        _bp, _bzx, _bzy = _RJ_HER_BREATH.get(speed, _RJ_HER_BREATH[0])
        _sw, _sdeg = _RJ_HER_SWAY
        _work = _RJ_WORK.get(speed) if _params else None
        if _params:
            _period, _h_amp, _arm_y, _arm_x, _h_rot = _params

        # Her torso group: breath + sway at rest, breath + lean-and-push while she licks; the chest takes the
        # same breath and lean (same anchor and params: the bra and the breasts never part from the torso) plus
        # its own hang. Under the vest or the jacket the breasts are held by the cloth (author, 2026-10-09: the
        # hang made the bra slide out past the vest's edge): the chest group then takes the torso's own
        # transform, zero differential against the cloth over it; the hang only plays when they are free (bare,
        # or bra / bikini alone, which ride the chest itself). Her stroking arm and its fingers ride the group
        # and stroke on top of it (a pure-offset wrap: safe over the anchored transform).
        _chest_bound = (_mid == "vest") or (_over == "jacket")
        if _work:
            _ldeg, _dx, _dy, _sw_dx, _sw_dy = _work
            _body_at = [rj_girl_body_work(_bp, _bzx, _bzy, _period, _ldeg, _dx, _dy)]
            _chest_at = list(_body_at) if _chest_bound else [rj_girl_chest_work(_bp, _bzx, _bzy, _period, _ldeg, _sw_dx, _sw_dy)]
        else:
            _body_at = [rj_girl_body_idle(_bp, _bzx, _bzy, _sw, _sdeg)]
            _chest_at = list(_body_at)

        # Her head group rides the torso's transform (chained: it breathes and leans WITH her back, the neck can
        # never part), with its own bounce (licking) or soft bob (at rest) on top.
        if _params:
            _head_at = _body_at + [rj_head_bounce(_period, _h_amp, _h_rot)]
            _arm_stroke = rj_arm_left_move(_period, _arm_y, _arm_x)
        else:
            _head_at = _body_at + [rj_head_idle(_bp, _RJ_HEAD_IDLE[0], _RJ_HEAD_IDLE[1])]
            _arm_stroke = rj_arm_left_static
        _arm_at = _body_at + [_arm_stroke]
        # her far arm hangs from her shoulder: it breathes and leans with the torso group
        _arm_r_at = list(_body_at)
        _lsw = _RJ_LEG_SWAY.get(speed, _RJ_LEG_SWAY[0])
        _idle_at = [rj_idle_sway(_lsw[0], _lsw[1])]
        # his whole unit shares one at_list: body, buttcheek, penis, the cum on it
        _guy_at = _rj_penis_at(speed)

        # His body and his penis: one unit (rj_guy_unit), the penis never moves on its own
        renpy.show(_g + " rj_guy_body", tag="rj_guy_body", zorder=9950, at_list=_guy_at)
        renpy.show(_g + " rj_penis", tag="rj_penis", zorder=9952, at_list=_guy_at)
        renpy.show(_g + " rj_torso", tag="rj_torso", zorder=9956, at_list=_body_at)
        renpy.show(_g + " rj_fingers", tag="rj_fingers", zorder=9953, at_list=_arm_at)

        # Arm left (animated) -- bare or clothed depending on jacket
        if _over == "jacket":
            renpy.show(_g + " rj_cl_arm_left_clothed", tag="rj_arm_left", zorder=9953, at_list=_arm_at)
        else:
            renpy.show(_g + " rj_arm_left", tag="rj_arm_left", zorder=9953, at_list=_arm_at)

        # Belly (pregnancy: Null before her visual stage, preg_art.rpy): above the far arm, under the chest, the
        # bra / bikini top and the vest, behind the near thigh
        renpy.show(_g + " rj_belly", tag="rj_belly", zorder=9963, at_list=_body_at)

        # Chest: covered by the bra / bikini top = the no-nipples art (author, 2026-10-09): the nipples are drawn
        # past the cloth's edge (chest reaches x 1610, the bra x 1603) and would leak out of it; the piercing sits
        # on the nipple, so it goes under the cloth with it.
        _covered = _chest in ("bra", "bikini_top") and not _chest_up
        if _covered:
            renpy.show(_g + " rj_chest_covered", tag="rj_chest", zorder=9964, at_list=_chest_at)
        elif _pierced:
            renpy.show(_g + " rj_chest_piercing", tag="rj_chest", zorder=9964, at_list=_chest_at)
        else:
            renpy.show(_g + " rj_chest", tag="rj_chest", zorder=9964, at_list=_chest_at)

        # Chest clothing (bra/bikini_top) follows chest breathing
        if _chest == "bra" and not _chest_up:
            renpy.show(_g + " rj_cl_bra", tag="rj_bra", zorder=9965, at_list=_chest_at)
        elif _chest == "bikini_top" and not _chest_up:
            renpy.show(_g + " rj_cl_bikini_top", tag="rj_bra", zorder=9965, at_list=_chest_at)
        else:
            renpy.hide("rj_bra")

        # Vest (mid slot) follows body breathing
        if _mid == "vest":
            renpy.show(_g + " rj_cl_vest", tag="rj_vest", zorder=9966, at_list=_body_at)
        else:
            renpy.hide("rj_vest")

        # Arm right (breathes and leans with the torso group) -- bare or clothed depending on jacket
        if _over == "jacket":
            renpy.show(_g + " rj_cl_arm_right_clothed", tag="rj_arm_right", zorder=9971, at_list=_arm_r_at)
        else:
            renpy.show(_g + " rj_arm_right", tag="rj_arm_right", zorder=9970, at_list=_arm_r_at)

        # Legs (idle sway)
        renpy.show(_g + " rj_leg_left", tag="rj_leg_left", zorder=9972, at_list=_idle_at)
        renpy.show(_g + " rj_leg_right", tag="rj_leg_right", zorder=9974, at_list=_idle_at)

        # Bottom clothing
        _pan = getattr(girl, "Panties", None)
        if _pan:
            _pan_map = {"panties": _g + " rj_cl_panties", "bikini_bottom": _g + " rj_cl_bikini_bottom"}
            _pan_img = _pan_map.get(_pan)
            if _pan_img:
                renpy.show(_pan_img, tag="rj_panties", zorder=9973, at_list=_idle_at)
            else:
                renpy.hide("rj_panties")
        else:
            renpy.hide("rj_panties")

        if getattr(girl, "Legs", None):
            renpy.show(_g + " rj_cl_pants", tag="rj_pants", zorder=9975, at_list=_idle_at)
        else:
            renpy.hide("rj_pants")

        # Jacket (over slot, body breathing) -- above pants
        if _over == "jacket":
            renpy.show(_g + " rj_cl_jacket", tag="rj_over", zorder=9976, at_list=_body_at)
        else:
            renpy.hide("rj_over")

        # Head group (all animated together)
        renpy.show(_g + " rj_lock_back", tag="rj_lock_back", zorder=9978, at_list=_head_at)
        if _head == 1:
            renpy.show(_g + " rj_head_1", tag="rj_head", zorder=9980, at_list=_head_at)
        else:
            renpy.show(_g + " rj_head_2", tag="rj_head", zorder=9986, at_list=_head_at)
        renpy.show(_g + " rj_hair", tag="rj_hair", zorder=9982, at_list=_head_at)
        renpy.show(_g + " rj_tongue", tag="rj_tongue", zorder=9984, at_list=_head_at)
        renpy.show(_g + " rj_guy_buttcheek", tag="rj_guy_buttcheek", zorder=9988, at_list=_guy_at)
        if _head == 1:
            renpy.show(_g + " rj_lock_head_1", tag="rj_lock_head", zorder=9990, at_list=_head_at)
        else:
            renpy.show(_g + " rj_lock_head_2", tag="rj_lock_head", zorder=9990, at_list=_head_at)

        # Cum layers: his cum after he came in this scene (store._rj_cum, Core_Rimjob.rpy): the drip on him, and her
        # hand when she finished him with it. The spurt only shows during the shot (_rj_cum_shot).
        _cum = getattr(store, "_rj_cum", None)
        if _cum:
            # on him: it moves with his penis (the same unit transform)
            renpy.show(_g + " rj_cum_penis", tag="rj_cum_penis", zorder=9953, at_list=_guy_at)
        else:
            renpy.hide("rj_cum_penis")
        if _cum == "hand":
            renpy.show(_g + " rj_cum_hand", tag="rj_cum_hand", zorder=9961)
        else:
            renpy.hide("rj_cum_hand")
        renpy.hide("rj_cum_spour")

        print("[RJ_APPLY] %s speed=%d head=%d cum=%s work=%s covered=%s bound=%s skin=%s preg_stage=%s clothes=%s" % (
            _g, speed, _head, _cum, _work, _covered, _chest_bound, getattr(Player, "skin", "White"), preg_vstage(_g),
            str(getattr(girl, "clothes", {}))))

# ── Minimal layeredimage (for _AT_SCENES has_image check) ───

layeredimage shion rimjob:
    always:
        "images/characters/Shion/Rimjob/Torso.png"

# ── Head 1 layeredimage ─────────────────────────────────────

layeredimage shion rj_head_1:

    always:
        "images/characters/Shion/Rimjob/Head 1/Head 1.png"

    always:
        ConditionSwitch(
            "_gs('rj', 'blush', 0) >= 2",
            "images/characters/Shion/Rimjob/Head 1/Blush/Blush 2.png",
            "_gs('rj', 'blush', 0) >= 1",
            "images/characters/Shion/Rimjob/Head 1/Blush/Blush 1.png",
            "True", Null()
        )

    always:
        ConditionSwitch(
            "_gs('rj', 'eyes') == 'eyes_ahegao'",
            "images/characters/Shion/Rimjob/Head 1/Expression/Eyes/Ahegao.png",
            "_gs('rj', 'eyes') == 'eyes_squint'",
            "images/characters/Shion/Rimjob/Head 1/Expression/Eyes/Squint.png",
            "_gs('rj', 'eyes') == 'eyes_surprised'",
            "images/characters/Shion/Rimjob/Head 1/Expression/Eyes/Surprised.png",
            "_gs('rj', 'eyes') == 'eyes_side'",
            "images/characters/Shion/Rimjob/Head 1/Expression/Eyes/Looking Left.png",
            "_gs('rj', 'eyes') == 'eyes_wink'",
            "images/characters/Shion/Rimjob/Head 1/Expression/Eyes/Wink.png",
            "_gs('rj', 'eyes') == 'eyes_happy'",
            "images/characters/Shion/Rimjob/Head 1/Expression/Eyes/Closed Happy.png",
            "_gs('rj', 'eyes') in ('eyes_closed', 'eyes_closed_2')",
            "images/characters/Shion/Rimjob/Head 1/Expression/Eyes/Closed.png",
            "True",
            "images/characters/Shion/Rimjob/Head 1/Expression/Eyes/Normal.png",
        )

    always:
        ConditionSwitch(
            "_gs('rj', 'brows') == 'brows_angry'",
            "images/characters/Shion/Rimjob/Head 1/Expression/Brows/Angry.png",
            "_gs('rj', 'brows') == 'brows_sad'",
            "images/characters/Shion/Rimjob/Head 1/Expression/Brows/Sad.png",
            "_gs('rj', 'brows') == 'brows_surprised'",
            "images/characters/Shion/Rimjob/Head 1/Expression/Brows/Surprised.png",
            "True",
            "images/characters/Shion/Rimjob/Head 1/Expression/Brows/Normal.png",
        )

# ── Head 2 layeredimage ─────────────────────────────────────

layeredimage shion rj_head_2:

    always:
        "images/characters/Shion/Rimjob/Head 2/Head 2.png"

    always:
        ConditionSwitch(
            "_gs('rj', 'blush', 0) >= 2",
            "images/characters/Shion/Rimjob/Head 2/Blush/Blush 2.png",
            "_gs('rj', 'blush', 0) >= 1",
            "images/characters/Shion/Rimjob/Head 2/Blush/Blush 1.png",
            "True", Null()
        )

    always:
        ConditionSwitch(
            "_gs('rj', 'eyes') == 'eyes_ahegao'",
            "images/characters/Shion/Rimjob/Head 2/Expression/Eyes/Ahegao.png",
            "_gs('rj', 'eyes') == 'eyes_squint'",
            "images/characters/Shion/Rimjob/Head 2/Expression/Eyes/Squint.png",
            "_gs('rj', 'eyes') == 'eyes_surprised'",
            "images/characters/Shion/Rimjob/Head 2/Expression/Eyes/Surprised.png",
            "_gs('rj', 'eyes') == 'eyes_side'",
            "images/characters/Shion/Rimjob/Head 2/Expression/Eyes/Looking Left.png",
            "_gs('rj', 'eyes') == 'eyes_happy'",
            "images/characters/Shion/Rimjob/Head 2/Expression/Eyes/Closed Happy.png",
            "_gs('rj', 'eyes') in ('eyes_closed', 'eyes_closed_2')",
            "images/characters/Shion/Rimjob/Head 2/Expression/Eyes/Closed.png",
            "True",
            "images/characters/Shion/Rimjob/Head 2/Expression/Eyes/Normal.png",
        )

    always:
        ConditionSwitch(
            "_gs('rj', 'brows') == 'brows_angry'",
            "images/characters/Shion/Rimjob/Head 2/Expression/Brows/Angry.png",
            "_gs('rj', 'brows') == 'brows_sad'",
            "images/characters/Shion/Rimjob/Head 2/Expression/Brows/Sad.png",
            "_gs('rj', 'brows') == 'brows_surprised'",
            "images/characters/Shion/Rimjob/Head 2/Expression/Brows/Surprised.png",
            "True",
            "images/characters/Shion/Rimjob/Head 2/Expression/Brows/Normal.png",
        )

# ── His body: the player, by his skin (Player/<skin>/Rimjob, _p() like every scene) ───────────

image shion rj_guy_body = _p("Rimjob/Guy Body.png")
image shion rj_guy_buttcheek = _p("Rimjob/Guy Buttcheek.png")
image shion rj_penis = _p("Rimjob/Penis.png")

# ── Static body images (chest and belly XL / on from her visual pregnancy stage, preg_art.rpy) ──

image shion rj_torso = "images/characters/Shion/Rimjob/Torso.png"
image shion rj_belly = preg_art("shion", "+Rimjob/belly")
image shion rj_hair = "images/characters/Shion/Rimjob/Hair.png"
image shion rj_fingers = "images/characters/Shion/Rimjob/Fingers.png"
image shion rj_tongue = "images/characters/Shion/Rimjob/Tongue.png"
image shion rj_arm_left = "images/characters/Shion/Rimjob/Arm Left.png"
image shion rj_arm_right = "images/characters/Shion/Rimjob/Arm Right.png"
image shion rj_leg_left = "images/characters/Shion/Rimjob/Leg Left.png"
image shion rj_leg_right = "images/characters/Shion/Rimjob/Leg Right.png"
image shion rj_chest = preg_art("shion", "Rimjob/Chest/Chest.png")
image shion rj_chest_covered = preg_art("shion", "Rimjob/Chest/Chest No Niples.png")
image shion rj_chest_piercing = preg_art("shion", "Rimjob/Chest/Chest Piercing.png")
image shion rj_lock_back = "images/characters/Shion/Rimjob/Lock/Lock Back.png"
image shion rj_lock_head_1 = "images/characters/Shion/Rimjob/Lock/Lock Head 1.png"
image shion rj_lock_head_2 = "images/characters/Shion/Rimjob/Lock/Lock Head 2.png"

# ── Cum images ──────────────────────────────────────────────

image shion rj_cum_hand = "images/characters/Shion/Rimjob/Cum/Cum Hand.png"
image shion rj_cum_penis = "images/characters/Shion/Rimjob/Cum/Cum Penis.png"
image shion rj_cum_spour = "images/characters/Shion/Rimjob/Cum/Cum Spour.png"

# ── Clothing images ─────────────────────────────────────────

image shion rj_cl_vest = preg_art("shion", "Rimjob/Clothes/Vest.png")
image shion rj_cl_jacket = "images/characters/Shion/Rimjob/Clothes/Jacket.png"
image shion rj_cl_bra = preg_art("shion", "Rimjob/Clothes/Bra.png")
image shion rj_cl_bikini_top = preg_art("shion", "Rimjob/Clothes/Bikini Top.png")
image shion rj_cl_bikini_bottom = "images/characters/Shion/Rimjob/Clothes/Bikini Bottom.png"
image shion rj_cl_panties = "images/characters/Shion/Rimjob/Clothes/Panties.png"
image shion rj_cl_pants = "images/characters/Shion/Rimjob/Clothes/Pants.png"
image shion rj_cl_arm_left_clothed = "images/characters/Shion/Rimjob/Clothes/Arm Left Clothed.png"
image shion rj_cl_arm_right_clothed = "images/characters/Shion/Rimjob/Clothes/Arm Right Clothed.png"
