# ============================================================
# Shion Reverse Cowgirl -- Custom layer structure
# Different from standard RCG: full expressions, Butt Bottom
# variants (3 states), separate L/R arms, L/R thighs and L/R lower
# legs (feet planted on the bed), Torso Piercing.
# Hers alone so far: anal in this pose (store.rcg_anal: the Butt
# Top is the mask over the penis) and his hands holding her down
# (store.rcg_hold). Both are opened by her art in scene_config.rpy
# ("anal" in GIRL_SCENE_CONFIG "rcg") / the "<gid> rcg_hold_left"
# images below; the flags and the menus live in Core_RCG.rpy.
# ============================================================

default _srcg_girl = None
default _srcg_speed = 0          # the speed her layers were last drawn at (_srcg_apply_speed)
default _srcg_penis_out = None   # he pulled out to cum while still "started": "out" (drawn over her) / "hidden" / None
default _srcg_extra_lift = 0     # extra px lift at the top of the ride stroke (marital bed tip: she barely has him inside)

# ── She rides him from her knees, by speed (her own timings, _SRCG_RIDE_PARAMS: a slow sit at speed 1 and 2, a steady bounce
# at 3, short and deep while he cums at 4): her hips, torso and head drop on him and rise (this transform), her feet
# and knees follow a little (srcg_leg_follow) and her thighs turn at the knee (srcg_thigh_turn), her hands rest on her legs
# (srcg_arm_plant). He never
# rises or drops on his own: the butt dropping over the penis is what makes it go in and out. He breathes and shifts
# his weight around his hips, and her landing presses him (and the penis) a few px into the bed (Core_RCG.rpy
# rcg_player_body_at).
# lo / hi = the px her layers sit below their drawn place at the top and at the bottom of the stroke: 0 and the whole
# drop of the speed, or only the lower part of it while he holds her down (_srcg_ride_params). ──
transform srcg_ride(period, lo, hi):
    subpixel True
    yoffset lo
    ease period * 0.35 yoffset hi
    pause period * 0.10
    ease period * 0.55 yoffset lo
    repeat

# ── Her butt on him: the ride, plus a squash where she lands (_SRCG_PIVOT_SEAT, the bottom of the butt on his hips:
# wider and flatter at the impact, then it springs back past the rest). transform_anchor + anchor = pos keeps the
# 1920 x 1080 layer in place while it zooms around that point. ──
transform srcg_butt_land(period, lo, hi, sx, sy):
    subpixel True
    transform_anchor True
    anchor _SRCG_PIVOT_SEAT pos _SRCG_PIVOT_SEAT
    yoffset lo xzoom 1.0 yzoom 1.0
    ease period * 0.35 yoffset hi xzoom sx yzoom sy
    pause period * 0.10
    ease period * 0.25 yoffset (lo + (hi - lo) * 0.4) xzoom (2.0 - sx) yzoom (2.0 - sy)
    ease period * 0.30 yoffset lo xzoom 1.0 yzoom 1.0
    repeat

# ── His hand holding her down (rcg_hold): it goes exactly where the point of her thigh it grips goes. That point
# rides srcg_butt_land (the thighs are part of the Butt Top layer): the drop, plus what the squash around the seat
# moves it (dx, dy at the landing, the opposite at the spring back; _srcg_cheek_shift). Same timings and warpers as
# srcg_butt_land, so the hand never slides off the thigh, and it keeps its own shape (it is moved, never squashed). ──
transform srcg_hold_follow(period, lo, hi, dx, dy):
    subpixel True
    xoffset 0 yoffset lo
    ease period * 0.35 xoffset dx yoffset (hi + dy)
    pause period * 0.10
    ease period * 0.25 xoffset (-dx) yoffset (lo + (hi - lo) * 0.4 - dy)
    ease period * 0.30 xoffset 0 yoffset lo
    repeat

# ── Her head: the ride, plus a nod on the landing around her neck (_SRCG_PIVOT_NECK). rotate: positive = clockwise
# on screen. ──
transform srcg_head_nod(period, lo, hi, deg):
    subpixel True
    transform_anchor True
    anchor _SRCG_PIVOT_NECK pos _SRCG_PIVOT_NECK
    yoffset lo rotate 0
    ease period * 0.35 yoffset hi rotate deg
    pause period * 0.10
    ease period * 0.55 yoffset lo rotate 0
    repeat

# ── Her left arm: the hand rests on her left knee (measured 2026-10-06: the hand, 410-520 x 590-650, lies on the
# kneecap, the top of the Left Leg layer, 400-550 x 587-700), and the knee never moves, so the hand is planted: the
# arm turns around it (pivot) as the shoulder comes down with the body (deg_lo at the top of the stroke, deg_hi at
# the bottom; the hand is at the bottom left of the shoulder, so clockwise lowers it). Her right hand rests on her
# right thigh, behind it (1300-1371 x 600-665, under the cheek's edge at y ~570), and that side of the thigh drops
# with her body: the right arm simply rides along (srcg_ride, no pivot). ──
transform srcg_arm_plant(period, pivot, deg_lo, deg_hi):
    subpixel True
    transform_anchor True
    anchor pivot pos pivot
    rotate deg_lo
    ease period * 0.35 rotate deg_hi
    pause period * 0.10
    ease period * 0.55 rotate deg_lo
    repeat

# ── Her thighs turn at the knee (Tight Left / Tight Right: the thigh from the kneecap to the hip crease, under the
# cheek). A rigid turn around the knee (pivot), nothing stretched or bent (author's call, 2026-10-06: what does not
# meet is fixed in the art): the hip side of the thigh comes down as the hips do (deg_lo at the top of the stroke,
# deg_hi at the bottom, deg_back at the spring back; _SRCG_THIGH_DEG_PER_PX of the drop; clockwise lowers the left
# thigh's hip side, so the right one takes the opposite sign), on the cheek's own four phases (srcg_butt_land: the
# drop, the hold, the spring back to 0.4 of the stroke, the settle) so it stays in step with the cheek's edge beside
# it. off_* = (dx, dy) px: where the lower leg's small follow takes the knee (_srcg_leg_knee), so the thigh keeps
# sitting on the shin. Seen from behind the thigh is a short, foreshortened sliver, so a turn that drops its hip
# side 50 px also shows 20-30 px more of its upper surface above the cheek's outline at the landing (the hip crease
# deepens) and turns its outline a little off the kneecap's: both are art (the thigh continued under the cheek, the
# kneecap drawn to take it), not code. ──
transform srcg_thigh_turn(period, pivot, deg_lo, deg_hi, deg_back, off_lo, off_hi, off_back):
    subpixel True
    transform_anchor True
    anchor pivot pos pivot
    rotate deg_lo offset off_lo
    ease period * 0.35 rotate deg_hi offset off_hi
    pause period * 0.10
    ease period * 0.25 rotate deg_back offset off_back
    ease period * 0.30 rotate deg_lo offset off_lo
    repeat

# ── Her lower legs follow a little (Left Leg / Right Leg, knee to foot; author, 2026-10-06: "as pernas precisam se
# mover um pouco"): rigid, around the foot (pivot = the sole on the bed). The leg sinks into the bed by y_* px (the
# sole is cut by the frame's bottom edge, so it sinks out of view) and the knee splays outward by deg_* (negative =
# the left knee goes left), the cheek's four phases again. Nothing above the drawn place: the foot never leaves the
# bed (_srcg_leg_knee clamps the stroke at 0). ──
transform srcg_leg_follow(period, pivot, deg_lo, deg_hi, deg_back, y_lo, y_hi, y_back):
    subpixel True
    transform_anchor True
    anchor pivot pos pivot
    rotate deg_lo yoffset y_lo
    ease period * 0.35 rotate deg_hi yoffset y_hi
    pause period * 0.10
    ease period * 0.25 rotate deg_back yoffset y_back
    ease period * 0.30 rotate deg_lo yoffset y_lo
    repeat

init python:

    # (period s, stroke px) of her ride per speed. The stroke is the whole travel between the top and the bottom of
    # the ride, before the cap of the hole (_SRCG_RIDE_MAX_DROP); where the travel sits against the drawn place is
    # _SRCG_RIDE_LIFT. Speed 2 and 3 quickened on 2026-10-06 (author: "speed 2 esta muito devagar, aumente um pouco e
    # tambem a speed 3": 1.3 -> 1.05 s, 0.45 -> 0.38 s); the strokes of 1, 2 and 4 grew 8-10 px the same day ("faca
    # ambas descerem um pouco mais": the top stays, the bottom comes down; 3 is capped by the hole anyway).
    _SRCG_RIDE_PARAMS = {1: (2.0, 30), 2: (1.05, 44), 3: (0.38, 70), 4: (0.34, 38)}
    # the butt at the landing (xzoom, yzoom) and the head's nod (deg) per speed
    _SRCG_BODY_PARAMS = {1: (1.015, 0.985, 1.5), 2: (1.025, 0.975, 2.5), 3: (1.040, 0.960, 4.0), 4: (1.025, 0.975, 2.0)}
    # Pivots, px of the 1920 x 1080 layers, measured on the art (2026-10-05): the bottom of the butt on his hips
    # (Butt Bottom 792-1128 x 622-938), her neck where the head (741-1069 x 24-351) meets the torso (top at
    # 885-897 x 281), her left hand: the left arm's lowest point (416-420, 648), on her left knee. (The right arm has
    # no pivot: its hand is on her thigh, behind it, and the arm rides with her body.)
    _SRCG_PIVOT_SEAT = (960, 935)
    _SRCG_PIVOT_NECK = (900, 300)
    _SRCG_PIVOT_HAND_L = (418, 645)
    # Her feet, planted on the bed: the middle of the sole where it meets the frame's bottom edge (measured
    # 2026-10-06: Left Leg 449-542 x 1079, Right Leg 1377-1470 x 1079; the two layers mirror each other).
    _SRCG_PIVOT_FOOT_L = (496, 1079)
    _SRCG_PIVOT_FOOT_R = (1424, 1079)
    # Her knees, the pivots of the thighs' turn (srcg_thigh_turn): the centre of the kneecap under the thigh's cover
    # (measured 2026-10-06 on Left Leg / Tight Left: the kneecap spans 400-558 x 587-700, the thigh's bulge over it
    # peaks at (400, 702); the right leg mirrors it around x 959.5). Degrees per px of the hips' drop: 0.29 = 20
    # degrees at the speed-3 landing (70 px), 6 at speed 1 (22 px); the hip side of the thigh then comes down ~50 px
    # at the hip crease (the cheek comes down 70 + its squash: the difference shows as the upper surface of the
    # thigh above the cheek's outline, see srcg_thigh_turn).
    _SRCG_PIVOT_KNEE_L = (475, 650)
    _SRCG_PIVOT_KNEE_R = (1444, 650)
    _SRCG_THIGH_DEG_PER_PX = 0.29
    # The lower legs follow a little (srcg_leg_follow, author 2026-10-06): the leg sinks into the bed by this share
    # of the hips' drop below the drawn place (9 px at the speed-3 landing) and the knee splays outward around the
    # foot by these degrees per px of that drop (1.2 degrees = ~9 px at the knee at speed 3). The thigh's pivot goes
    # with the knee (_srcg_leg_knee). Nothing above the drawn place: the foot stays on the bed.
    _SRCG_LEG_SHARE = 0.30
    _SRCG_LEG_SPLAY = 0.02
    # Where the ride sits against the drawn place, by the hole he is taking (the drawn art is her seated on him; still,
    # at speed 0 or frozen, she sits at the drawn place): the top of the stroke is _SRCG_RIDE_LIFT px ABOVE it and the
    # bottom never deeper than _SRCG_RIDE_MAX_DROP px BELOW it (the stroke of a speed that would go deeper is
    # shortened to that: the same deepest point, a quicker bounce). Author's calls of 2026-10-06, in order: "suba mais
    # um pouco o riding dela" (lift 10 / 4), then "precisa aumentar o y no anal, esta quase nulo, desca mais um pouco
    # e suba mais tambem; vaginal esta descendo muito, precisa estar mais pra cima, mas pode subir mais tambem"
    # (lift 22 / 14, cap 34 / 28), then "faca ambas descerem um pouco mais no eixo y" (cap 44 / 38, the top kept).
    # What the art allows (measured 2026-10-06), so the author knows what shows: in her ass the mask's arch (Butt
    # Top 2) ends at y 703 at the centre and the rim of the glans is drawn down to y 697, so a lift above 5 shows the
    # rim under the arch at the very top of the stroke (14: ~9 px of rim; art: a taller arch); the hole piece's lower
    # edge runs 895-905 over the penis columns and the base of the penis 920-937 (937 at the centre, 920-924 at the
    # shaft's sides), so a drop past 23 shows her skin around the base's corners and the seam between the penis and
    # his body (38: ~15 px at the corners, the edge touching the base at the centre; art: that edge raised ~20 px
    # there). In her pussy the penis is under the piece (nothing to show) and "seated" is ~37 below the drawn place
    # (the piece's edge reaching his hips): 44 presses 7 px past it, her weight on him.
    _SRCG_RIDE_LIFT = {"pussy": 22, "ass": 14}
    _SRCG_RIDE_MAX_DROP = {"pussy": 44, "ass": 38}
    # his hips, where the penis sits on his body (Guy 531-1389 x 857-1080, the penis base at 901-1018 x 938): he
    # breathes around it, so the penis never slides on him
    _SRCG_PIVOT_HIPS = (960, 930)
    # an arm is ~577 px from hand to shoulder: a drop of 1 px at the shoulder is ~0.1 degree around the hand
    _SRCG_ARM_DEG_PER_PX = 0.1
    # He holds her down (store.rcg_hold, Core_RCG.rpy): his hands stop her before the top, so she only rides the
    # LOWER share of her stroke (the same deepest point, never higher than that share of it), and her landing (the
    # squash of the butt, the nod) shrinks by the same share.
    _SRCG_HOLD_STROKE = 0.5
    # Where each of his hands grips her: the middle of the hand, on her thigh where it meets the hip. Measured on the
    # art (2026-10-06): the hand above the wrist is 482-695 x 537-720 (the right one mirrors it around x 959.5), its
    # centre (589, 640), on the cheek (Butt Top) just inside the hip crease (the thigh, its own layer since
    # 2026-10-06, ends at x ~515 on that row), so the hands follow the cheek layer (_srcg_cheek_shift,
    # srcg_hold_follow); the fingertips over the thigh ride a few px off it at the landing.
    _SRCG_HOLD_GRIP = {"left": (589, 640), "right": (1330, 640)}
    # The penis by where it is (z-orders): in her pussy = under the hole piece (Butt Bottom, 9964); in her ass = above
    # every layer of hers except the mask (Butt Top, 9970: the cheeks hide what is inside); out of her = above all.
    # Going in has no z-order of its own (_srcg_penis_enter): the first frame of the ride already has him inside.
    _SRCG_Z_PENIS = {"pussy": 9962, "ass": 9969, "out": 10060}
    _SRCG_Z_HOLD = 9975

    def _srcg_riding(speed):
        """She moves only with him inside her (rcg_started): the tip at speed 1, the sex at 1-3, his cum at 4.
        Speed 0 (the preview above him, or frozen) = still."""
        return bool(getattr(store, "rcg_started", False)) and speed in _SRCG_RIDE_PARAMS

    def _srcg_ride_params(speed):
        """(period s, lo, hi, sx, sy, nod) of her ride at that speed, None = she is still. lo / hi = the px her layers
        sit below their drawn place at the top / the bottom of the stroke: the top _SRCG_RIDE_LIFT above it (lo is
        negative), the bottom the speed's stroke lower but never past _SRCG_RIDE_MAX_DROP (both by the hole he is
        taking), and only the lower _SRCG_HOLD_STROKE of that while he holds her down (with a landing that much
        softer)."""
        if not _srcg_riding(speed):
            return None
        _period, _amp = _SRCG_RIDE_PARAMS[speed]
        _sx, _sy, _nod = _SRCG_BODY_PARAMS.get(speed, _SRCG_BODY_PARAMS[1])
        _hole = "ass" if getattr(store, "rcg_anal", False) else "pussy"
        _extra = float(getattr(store, "_srcg_extra_lift", 0)) if getattr(store, "rcg_tip_mode", False) else 0.0
        _lo = -float(_SRCG_RIDE_LIFT[_hole]) - _extra
        _hi = min(_lo + _amp, float(_SRCG_RIDE_MAX_DROP[_hole]))
        if getattr(store, "rcg_hold", False):
            _k = _SRCG_HOLD_STROKE
            _lo = _lo + (_hi - _lo) * (1.0 - _k)
            _sx, _sy, _nod = 1.0 + (_sx - 1.0) * _k, 1.0 + (_sy - 1.0) * _k, _nod * _k
        return _period, _lo, _hi, _sx, _sy, _nod

    def _srcg_leg_knee(stroke, side):
        """The lower leg's small follow at one point of the stroke (px below the drawn place; nothing above it) and
        where it takes the knee: (deg, y, (knee_dx, knee_dy)). deg = the splay around the foot (negative = the left
        knee outward; the right one takes the opposite sign), y = the px the leg sinks into the bed; the thigh's
        pivot (the knee) moves by that same rigid motion, so the thigh keeps sitting on the shin."""
        import math
        _s = max(0.0, stroke)
        _y = _s * _SRCG_LEG_SHARE
        _deg = (-_s if side == "left" else _s) * _SRCG_LEG_SPLAY
        _foot = _SRCG_PIVOT_FOOT_L if side == "left" else _SRCG_PIVOT_FOOT_R
        _knee = _SRCG_PIVOT_KNEE_L if side == "left" else _SRCG_PIVOT_KNEE_R
        _r = math.radians(_deg)
        _rx, _ry = _knee[0] - _foot[0], _knee[1] - _foot[1]
        _dx = _rx * math.cos(_r) - _ry * math.sin(_r) - _rx
        _dy = _rx * math.sin(_r) + _ry * math.cos(_r) - _ry + _y
        return _deg, _y, (_dx, _dy)

    def _srcg_cheek_shift(point, sx, sy):
        """(dx, dy) px: how far the squash of her butt at the landing (srcg_butt_land: xzoom sx, yzoom sy around the
        seat) moves that point of the cheek layer (the point of her hip a hand of his grips). The drop itself is added
        by the caller (srcg_hold_follow); the spring back (zoom 2 - s) moves it the opposite way."""
        return (point[0] - _SRCG_PIVOT_SEAT[0]) * (sx - 1.0), (point[1] - _SRCG_PIVOT_SEAT[1]) * (sy - 1.0)

    def _srcg_body_at(speed):
        """at_lists of the layer groups: hers ({"body", "head", "arm_l", "arm_r", "thigh_l", "thigh_r", "leg_l",
        "leg_r", "butt"}, all empty = she is still), his ({"guy", "penis"}: he always breathes; the press of her
        landing only while she rides) and his hands on her thighs ({"hold": {"left", "right"}}: they move with the
        butt group, each at its own grip point). Her ride: the body group, the head and the butt take the drop
        (lo / hi, the whole stroke lifted by _SRCG_RIDE_LIFT); her lower legs follow a little (srcg_leg_follow: the
        foot pressing into the bed, the knee splaying out, _srcg_leg_knee); her thighs turn at the knee
        (srcg_thigh_turn: the hip side comes down as the hips do, the pivot going with the knee); her left hand is
        planted on her left knee (the arm turns around it) and her right arm goes down with her body (its hand on
        her thigh, behind it)."""
        _p = _srcg_ride_params(speed)
        if not _p:
            _his = rcg_player_body_at(speed, _SRCG_PIVOT_HIPS)
            return {"body": [], "head": [], "arm_l": [], "arm_r": [], "thigh_l": [], "thigh_r": [], "leg_l": [], "leg_r": [], "butt": [],
                    "hold": {"left": [], "right": []},
                    "guy": _his["body"], "penis": _his["penis"]}
        _period, _lo, _hi, _sx, _sy, _nod = _p
        _his = rcg_player_body_at(speed, _SRCG_PIVOT_HIPS, ride=(_period, _hi))
        _hold = {}
        for _side in ("left", "right"):
            _dx, _dy = _srcg_cheek_shift(_SRCG_HOLD_GRIP[_side], _sx, _sy)
            _hold[_side] = [srcg_hold_follow(_period, _lo, _hi, _dx, _dy)]
        # the legs and the thighs, on the cheek's four phases: the spring back passes at 0.4 of the stroke
        _back = _lo + (_hi - _lo) * 0.4
        _legs = {}
        for _side, _foot, _knee, _sign in (("left", _SRCG_PIVOT_FOOT_L, _SRCG_PIVOT_KNEE_L, 1.0),
                                           ("right", _SRCG_PIVOT_FOOT_R, _SRCG_PIVOT_KNEE_R, -1.0)):
            _k_lo, _k_hi, _k_back = [_srcg_leg_knee(_v, _side) for _v in (_lo, _hi, _back)]
            _legs[_side] = {
                # the lower leg: the foot pressing into the bed, the knee splaying out a little
                "leg": [srcg_leg_follow(_period, _foot, _k_lo[0], _k_hi[0], _k_back[0], _k_lo[1], _k_hi[1], _k_back[1])],
                # the thigh turns at the knee (left clockwise, right the other way), its pivot going where the knee goes
                "thigh": [srcg_thigh_turn(_period, _knee, _sign * _lo * _SRCG_THIGH_DEG_PER_PX, _sign * _hi * _SRCG_THIGH_DEG_PER_PX,
                                          _sign * _back * _SRCG_THIGH_DEG_PER_PX, _k_lo[2], _k_hi[2], _k_back[2])],
            }
        return {
            "body": [srcg_ride(_period, _lo, _hi)],
            "head": [srcg_head_nod(_period, _lo, _hi, _nod)],
            # the left hand planted on the knee: the arm turns around it as the shoulder drops
            "arm_l": [srcg_arm_plant(_period, _SRCG_PIVOT_HAND_L, _lo * _SRCG_ARM_DEG_PER_PX, _hi * _SRCG_ARM_DEG_PER_PX)],
            # the right hand on the thigh, behind it: shoulder and that side of the thigh drop together, so the arm does
            "arm_r": [srcg_ride(_period, _lo, _hi)],
            "thigh_l": _legs["left"]["thigh"],
            "thigh_r": _legs["right"]["thigh"],
            "leg_l": _legs["left"]["leg"],
            "leg_r": _legs["right"]["leg"],
            "butt": [srcg_butt_land(_period, _lo, _hi, _sx, _sy)],
            "hold": _hold,
            "guy": _his["body"],
            "penis": _his["penis"],
        }

    def _srcg_show_layers(girl=None):
        _srcg_apply_speed(girl or store._srcg_girl, 0)

    def _srcg_hide_all():
        for _tag in ("srcg_guy", "srcg_torso", "srcg_penis",
                      "srcg_butt_bottom", "srcg_butt_top",
                      "srcg_left_arm", "srcg_right_arm", "srcg_left_thigh", "srcg_right_thigh",
                      "srcg_left_leg", "srcg_right_leg", "srcg_head",
                      "srcg_torso_cl", "srcg_left_arm_cl", "srcg_bra",
                      "srcg_panties", "srcg_pants",
                      "srcg_cum_butt", "srcg_cum_pussy", "srcg_cum",
                      "srcg_hold_left", "srcg_hold_right"):
            renpy.hide(_tag)
        store._srcg_penis_out = None

    def _srcg_show_penis(where, at_list=None):
        """The penis by where it is (_SRCG_Z_PENIS): "pussy" / "ass" (inside her), "out". The condom on
        it while he wears one (torn after a break: _condom_img_tag): one displayable, so the condom rides every frame
        of the penis, at its z-order."""
        _z = _SRCG_Z_PENIS[where]
        if getattr(store, "condom_active", False):
            _con = _condom_img_tag("shion srcg_condom")
            renpy.show("shion srcg_penis", what=Fixed(renpy.displayable("shion srcg_penis"), renpy.displayable(_con), fit_first=True),
                       tag="srcg_penis", zorder=_z, at_list=at_list or [])
        else:
            renpy.show("shion srcg_penis", tag="srcg_penis", zorder=_z, at_list=at_list or [])

    def _srcg_penis_enter():
        """He goes in (RCG_PenisEnterAnim): no frame of its own. Every caller draws the pose right after this
        (RCG_ApplySpeed), and that first frame already has him inside her: the hole piece of that hole (Butt Bottom 2
        / 3), its mask (Butt Top 1 / 2) and the penis at the hole's z-order. The frame that used to come first showed
        the penis under the Butt Top but over the still closed Butt Bottom, and Top 1 in her ass too (author,
        2026-10-09: no transition gap)."""
        store._srcg_penis_out = None
        print("[SRCG_ENTER] he goes in: %s (the next apply draws it, no in-between frame)" % (
            "ass" if getattr(store, "rcg_anal", False) else "pussy"))

    # Shion cum layer → girl.Cum tags that trigger it
    _SRCG_CUM_LAYER_MAP = {
        "srcg_cum_pussy": ("dripping",),
        "srcg_cum_butt":  ("dripping_ass",),
        "srcg_cum":       ("body", "ass", "back", "outside"),
    }

    def _srcg_show_cum(at_list=None, cum_tags=None):
        """His cum on her: only the layers relevant to cum_tags (9973: on her skin, under his hands).
        cum_tags: explicit set/list of tags to show. If None, reads from girl.Cum."""
        if cum_tags is None:
            _girl = store._rcg_girl
            cum_tags = getattr(_girl, "Cum", []) if _girl else []
        _ct_set = set(cum_tags)
        for _ct, _triggers in _SRCG_CUM_LAYER_MAP.items():
            _ci = "shion %s" % _ct
            if _ct_set.intersection(_triggers) and renpy.has_image(_ci, exact=True):
                renpy.show(_ci, tag=_ct, zorder=9973, at_list=at_list or [])
            else:
                renpy.hide(_ct)

    def _srcg_show_hold(girl, at_lists):
        """His hands on her thighs while he holds her down (store.rcg_hold), one layer per hand (above every layer of
        hers, _SRCG_Z_HOLD). A hand busy with the phone or spanking her (rcg_hold_side_on, Core_RCG.rpy) lets go.
        In step with her thighs by construction: every apply re-shows every layer with fresh transforms, so all of
        them (hands included) start their cycle together."""
        for _side in ("left", "right"):
            _tag = "srcg_hold_%s" % _side
            if rcg_hold_side_on(_side):
                renpy.show("shion rcg_hold_%s" % _side, tag=_tag, zorder=_SRCG_Z_HOLD, at_list=at_lists[_side])
            else:
                renpy.hide(_tag)

    def _srcg_redraw_hold(girl):
        """A hand of his just let go (a spank): take it off her right now, the other one untouched (it keeps its
        cycle). A hand that comes back arrives with the next full apply, in step with everything else."""
        for _side in ("left", "right"):
            if not rcg_hold_side_on(_side):
                renpy.hide("srcg_hold_%s" % _side)

    def _srcg_butt_state(started, anal, penis_in):
        """(Butt Bottom, Butt Top, where the penis is) for what is happening. The two Butt Tops are the MASKS over
        the penis: 1 = her cheeks as they are, 2 = the same with the cleft closed in an arch over her anus, the ring
        the penis disappears under (measured 2026-10-06: Top 2 = Top 1 + a wedge at 926-993 x 658-726, the arch at
        y ~704). The Butt Bottoms are the holes: 1 = both closed, 2 = her pussy open around him (a cut-out), 3 = her
        anus gaping (painted, her pussy closed).
          she hovers over him        Bottom 1 (3 after anal this session), Top 1, the penis out
          he is in her pussy         Bottom 2, Top 1, the penis UNDER the Butt Bottom
          he is in her ass           Bottom 3, Top 2, the penis OVER every layer of hers but the Butt Top
          he pulled out (his cum)    her pussy still open (2) / her ass gaping (3), Top 1, the penis out"""
        _had_anal = bool(getattr(store, "_dg_had_anal", False) or getattr(store, "_rcg_had_anal", False))
        if not started:
            return (3 if _had_anal else 1), 1, "out"
        if anal:
            return (3, 2, "ass") if penis_in else (3, 1, "out")
        return 2, 1, ("pussy" if penis_in else "out")

    def _srcg_apply_speed(girl, speed):
        """Show all Shion RCG layers with clothing/cum/ride.
        Z-order (author's rules, 2026-10-05 and 2026-10-06; back->front):
        Guy(9952) Head(9954) LeftArm(9956) RightArm(9958) Legs(9959) Torso(9960) BikiniTop(9961) Penis in her
        pussy(9962) Thighs(9963) ButtBot(9964) TorsoCl(9966) ArmCl(9968) Penis in her ass(9969) ButtTop(9970)
        Panties(9971) Pants(9972) Cum(9973) his hands holding her(9975).
        Her lower legs (Left Leg / Right Leg, knee to foot) over her arms (the knee in front of her left hand), her
        thighs (Tight Left / Right, kneecap to hip crease) over the lower legs (the thigh over the kneecap) and under
        the Butt Top (the cheek over the hip end of the thigh); the pants cover all of it dressed.
        The penis under the hole piece (ButtBot) once he is in her pussy: what shows of it is between his body and
        her pussy, the rest is inside. In her ass it is over every layer of hers but the mask (ButtTop 2), whose
        arch hides what is inside her. Above everything (10060) while she still hovers over him, or after he pulled
        out to cum (_srcg_penis_out). Her bottom clothes sit ON the cheeks (above ButtTop), the pants over the
        panties; her top clothes over the arms and torso, and the cheeks over their hem (she sits on it). NOTHING of
        her clothes once he is inside her (the penetration and the tip are done naked: _rcg_sex_nude strips her, this
        never draws them started). No rub in this pose, only the tip (speed 1) and the sex.
        His hands (store.rcg_hold): on her thighs, over everything of hers, moving with the butt layers."""
        _pierced = getattr(girl, "Piercing", False)
        _started = bool(getattr(store, "rcg_started", False))
        _anal = bool(getattr(store, "rcg_anal", False))
        # he pulled out to cum ("out": drawn over her, "hidden": gone); going back to the ride puts him in again
        if speed >= 1 or not _started:
            store._srcg_penis_out = None
        _out = getattr(store, "_srcg_penis_out", None)
        store._srcg_speed = speed
        _b = _srcg_body_at(speed)
        _bottom, _top, _penis = _srcg_butt_state(_started, _anal, not _out)

        # ── His body breathes; her landing presses him and the penis (she does the riding) ──
        renpy.show("shion srcg_guy", tag="srcg_guy", zorder=9952, at_list=_b["guy"])
        if _out == "hidden":
            renpy.hide("srcg_penis")
        else:
            _srcg_show_penis(_penis, _b["penis"] if _penis != "out" else None)

        # ── Her body ──
        renpy.show("shion srcg_head", tag="srcg_head", zorder=9954, at_list=_b["head"])
        renpy.show("shion srcg_left_arm", tag="srcg_left_arm", zorder=9956, at_list=_b["arm_l"])
        renpy.show("shion srcg_right_arm", tag="srcg_right_arm", zorder=9958, at_list=_b["arm_r"])
        # her lower legs: the feet on the bed (pressing into it a little on the ride), the knees under the thighs
        # and in front of her left hand
        renpy.show("shion srcg_left_leg", tag="srcg_left_leg", zorder=9959, at_list=_b["leg_l"])
        renpy.show("shion srcg_right_leg", tag="srcg_right_leg", zorder=9959, at_list=_b["leg_r"])
        # her thighs: over the kneecaps, under the cheeks; they turn at the knee on the ride
        renpy.show("shion srcg_left_thigh", tag="srcg_left_thigh", zorder=9963, at_list=_b["thigh_l"])
        renpy.show("shion srcg_right_thigh", tag="srcg_right_thigh", zorder=9963, at_list=_b["thigh_r"])
        if _pierced:
            renpy.show("shion srcg_torso_piercing", tag="srcg_torso", zorder=9960, at_list=_b["body"])
        else:
            renpy.show("shion srcg_torso", tag="srcg_torso", zorder=9960, at_list=_b["body"])

        # Butt: the holes (Butt Bottom) and the mask over the penis (Butt Top), by what is happening
        _srcg_set_butt(_bottom, _top, _b["butt"])

        # ── Her clothes: only while she hovers over him (never started) ──
        _chest = girl.clothes.get("chest")
        if not _started and _chest == "bikini_top" and not girl.ChestUp:
            renpy.show("shion srcg_cl_bikini_top", tag="srcg_bra", zorder=9961, at_list=_b["body"])
        else:
            renpy.hide("srcg_bra")

        _over = girl.clothes.get("over")
        if not _started and _over:
            renpy.show("shion srcg_cl_torso_clothes", tag="srcg_torso_cl", zorder=9966, at_list=_b["body"])
            renpy.show("shion srcg_cl_left_arm_clothes", tag="srcg_left_arm_cl", zorder=9968, at_list=_b["arm_l"])
        else:
            renpy.hide("srcg_torso_cl")
            renpy.hide("srcg_left_arm_cl")

        # Panties on the cheeks: "full" = the wide back (Panties 3 / Bikini Bottom 1), "side" = pulled in between
        # the cheeks (Panties 2 / Bikini Bottom 2); "down" has no art here (off). Panties 1 (the narrow strip) is
        # not used.
        _pan = girl.Panties
        _pan_state = girl.clothes_state.get("panties", "full")
        _pan_map = {
            ("panties", "full"): "shion srcg_cl_panties_3",
            ("panties", "side"): "shion srcg_cl_panties_2",
            ("bikini_bottom", "full"): "shion srcg_cl_bikini_bottom_1",
            ("bikini_bottom", "side"): "shion srcg_cl_bikini_bottom_2",
        }
        _pan_img = _pan_map.get((_pan, _pan_state)) if (not _started and _pan and _pan_state != "down") else None
        if _pan_img:
            renpy.show(_pan_img, tag="srcg_panties", zorder=9971, at_list=_b["butt"])
        else:
            renpy.hide("srcg_panties")

        if not _started and girl.Legs:
            renpy.show("shion srcg_cl_pants", tag="srcg_pants", zorder=9972, at_list=_b["butt"])
        else:
            renpy.hide("srcg_pants")

        # Cum layers (on the butt)
        if getattr(girl, "Cum", False):
            _srcg_show_cum(_b["butt"])
        else:
            for _ct in ("srcg_cum_butt", "srcg_cum_pussy", "srcg_cum"):
                renpy.hide(_ct)

        # ── His hands holding her down: on her thighs, with the butt layers ──
        _srcg_show_hold(girl, _b["hold"])

        _rp = _srcg_ride_params(speed)
        print("[SRCG_APPLY] speed=%d started=%s anal=%s tip=%s penis=%s butt=%d/%d riding=%s hold=%s (left=%s right=%s) ride=%s thigh_deg=%s clothes=%s" % (
            speed, _started, _anal, getattr(store, "rcg_tip_mode", False), ("hidden" if _out == "hidden" else _penis), _bottom, _top,
            _srcg_riding(speed), getattr(store, "rcg_hold", False), rcg_hold_side_on("left"), rcg_hold_side_on("right"),
            _rp, ((_rp[1] * _SRCG_THIGH_DEG_PER_PX, _rp[2] * _SRCG_THIGH_DEG_PER_PX) if _rp else None), str(girl.clothes)))

    def _srcg_set_butt(bottom_idx, top_idx, at_list=None):
        """The hole piece (Butt Bottom, over his hips) and the mask over the penis (Butt Top)."""
        if at_list is None:
            at_list = []
        _bottom_map = {
            1: "shion srcg_butt_bottom_1",
            2: "shion srcg_butt_bottom_2",
            3: "shion srcg_butt_bottom_3",
        }
        _top_map = {
            1: "shion srcg_butt_top_1",
            2: "shion srcg_butt_top_2",
        }
        renpy.show(_bottom_map.get(bottom_idx, _bottom_map[1]), tag="srcg_butt_bottom", zorder=9964, at_list=at_list)
        renpy.show(_top_map.get(top_idx, _top_map[1]), tag="srcg_butt_top", zorder=9970, at_list=at_list)

# ── Minimal layeredimage (for _AT_SCENES has_image check) ───

layeredimage shion shion_rcg:
    always:
        "images/characters/Shion/Reverse Cowgirl/Torso.png"

# ── Head + Expression layeredimage. No blush in this pose: Reverse Cowgirl/Head/"Butt Blush Left / Right" are blush
# on her butt, never shown (author, 2026-10-09) ──────────────────────────

layeredimage shion srcg_head:

    always:
        "images/characters/Shion/Reverse Cowgirl/Head.png"

    always:
        ConditionSwitch(
            "_gs('srcg', 'mouth') == 'mouth_happy'",
            "images/characters/Shion/Reverse Cowgirl/Expression/Mouth/Happy.png",
            "_gs('srcg', 'mouth') == 'mouth_sad'",
            "images/characters/Shion/Reverse Cowgirl/Expression/Mouth/Sad.png",
            "_gs('srcg', 'mouth') == 'mouth_surprised'",
            "images/characters/Shion/Reverse Cowgirl/Expression/Mouth/Surprised.png",
            "_gs('srcg', 'mouth') == 'mouth_lipbite'",
            "images/characters/Shion/Reverse Cowgirl/Expression/Mouth/Bitting Lip.png",
            "_gs('srcg', 'mouth') == 'mouth_kiss'",
            "images/characters/Shion/Reverse Cowgirl/Expression/Mouth/Kiss.png",
            "_gs('srcg', 'mouth') == 'mouth_moaning'",
            "images/characters/Shion/Reverse Cowgirl/Expression/Mouth/Moaning.png",
            "_gs('srcg', 'mouth') == 'mouth_scared'",
            "images/characters/Shion/Reverse Cowgirl/Expression/Mouth/Scared.png",
            "_gs('srcg', 'mouth') == 'mouth_smile'",
            "images/characters/Shion/Reverse Cowgirl/Expression/Mouth/Smile.png",
            "_gs('srcg', 'mouth') == 'mouth_tongue'",
            "images/characters/Shion/Reverse Cowgirl/Expression/Mouth/Tongue.png",
            "True",
            "images/characters/Shion/Reverse Cowgirl/Expression/Mouth/Normal.png",
        )

    always:
        ConditionSwitch(
            "_gs('srcg', 'eyes') == 'eyes_ahegao'",
            "images/characters/Shion/Reverse Cowgirl/Expression/Eyes/Ahegao.png",
            "_gs('srcg', 'eyes') == 'eyes_ahegao_2'",
            "images/characters/Shion/Reverse Cowgirl/Expression/Eyes/Ahegao 2.png",
            "_gs('srcg', 'eyes') == 'eyes_happy'",
            "images/characters/Shion/Reverse Cowgirl/Expression/Eyes/Happy.png",
            "_gs('srcg', 'eyes') == 'eyes_sexy'",
            "images/characters/Shion/Reverse Cowgirl/Expression/Eyes/Sexy.png",
            "_gs('srcg', 'eyes') == 'eyes_side'",
            "images/characters/Shion/Reverse Cowgirl/Expression/Eyes/Looking Left.png",
            "_gs('srcg', 'eyes') == 'eyes_side_2'",
            "images/characters/Shion/Reverse Cowgirl/Expression/Eyes/Looking Right.png",
            "_gs('srcg', 'eyes') == 'eyes_surprised'",
            "images/characters/Shion/Reverse Cowgirl/Expression/Eyes/Surprised.png",
            "_gs('srcg', 'eyes') == 'eyes_blinking'",
            "images/characters/Shion/Reverse Cowgirl/Expression/Eyes/Blinking.png",
            "_gs('srcg', 'eyes') == 'eyes_looking_to_player'",
            "images/characters/Shion/Reverse Cowgirl/Expression/Eyes/Looking To Player.png",
            "_gs('srcg', 'eyes') == 'eyes_looking_up'",
            "images/characters/Shion/Reverse Cowgirl/Expression/Eyes/Looking Up.png",
            "_gs('srcg', 'eyes') in ('eyes_closed', 'eyes_closed_2')",
            "images/characters/Shion/Reverse Cowgirl/Expression/Eyes/Closed.png",
            "True",
            "images/characters/Shion/Reverse Cowgirl/Expression/Eyes/Normal.png",
        )

    always:
        ConditionSwitch(
            "_gs('srcg', 'brows') == 'brows_angry'",
            "images/characters/Shion/Reverse Cowgirl/Expression/Brows/Angry.png",
            "_gs('srcg', 'brows') == 'brows_sad'",
            "images/characters/Shion/Reverse Cowgirl/Expression/Brows/Sad.png",
            "_gs('srcg', 'brows') == 'brows_surprised'",
            "images/characters/Shion/Reverse Cowgirl/Expression/Brows/Surprised.png",
            "_gs('srcg', 'brows') == 'brows_worried'",
            "images/characters/Shion/Reverse Cowgirl/Expression/Brows/Worried.png",
            "_gs('srcg', 'brows') == 'brows_horny'",
            "images/characters/Shion/Reverse Cowgirl/Expression/Brows/Horny.png",
            "_gs('srcg', 'brows') == 'brows_up'",
            "images/characters/Shion/Reverse Cowgirl/Expression/Brows/Up.png",
            "True",
            "images/characters/Shion/Reverse Cowgirl/Expression/Brows/Normal.png",
        )

# ── Static body images ──────────────────────────────────────
# (his body and the penis are still her folder's: no skin-color pair of them yet)

# his body and penis by his skin (_p_one_skin, variables.rpy: the artist drew him white only)
image shion srcg_guy = _p_one_skin("images/characters/Shion/Reverse Cowgirl/Guy/Guy.png")
image shion srcg_penis = _p_one_skin("images/characters/Shion/Reverse Cowgirl/Guy/Penis.png")
# the condom on it (the same for every skin), torn after a break (_condom_img_tag)
image shion srcg_condom = "images/characters/Player/RCG Shion Condom.png"
image shion srcg_condom_broken = "images/characters/Player/RCG Shion Condom Broke.png"

# ── His hands holding her down (store.rcg_hold), by his skin (Player/<skin>/RCG Shion, _p() like every scene).
# ONE drawing with both hands (his left one is the left half, 329-697 px; the right one 1222-1590), cut here into
# one full-size layer per hand, so each can let go on its own (the phone while he records, a spank). ──
image shion rcg_hold_left = Composite((1920, 1080), (0, 0), Crop((0, 0, 960, 1080), _p("RCG Shion/Player Hold.png")))
image shion rcg_hold_right = Composite((1920, 1080), (960, 0), Crop((960, 0, 960, 1080), _p("RCG Shion/Player Hold.png")))
image shion rcg_slap_left = _p("RCG Shion/Slap Left.png")
image shion rcg_slap_right = _p("RCG Shion/Slap Right.png")

# Shion's slap images are full-screen with the hand at its FINAL position. The transforms slide the image
# from the side (xoffset) to xoffset 0 (impact), then slide it away and fade out.
transform srcg_slap_right_in:
    subpixel True
    pos (0, 0)
    xoffset 400
    alpha 1.0
    easein 0.08 xoffset 0
    pause 0.15
    easeout 0.25 xoffset -400 alpha 0.0

transform srcg_slap_left_in:
    subpixel True
    pos (0, 0)
    xoffset -400
    alpha 1.0
    easein 0.08 xoffset 0
    pause 0.15
    easeout 0.25 xoffset 400 alpha 0.0
image shion srcg_torso = "images/characters/Shion/Reverse Cowgirl/Torso.png"
image shion srcg_torso_piercing = "images/characters/Shion/Reverse Cowgirl/Torso Piercing.png"
image shion srcg_left_arm = "images/characters/Shion/Reverse Cowgirl/Left Arm.png"
image shion srcg_right_arm = "images/characters/Shion/Reverse Cowgirl/Right Arm.png"
image shion srcg_left_leg = "images/characters/Shion/Reverse Cowgirl/Left Leg.png"
image shion srcg_right_leg = "images/characters/Shion/Reverse Cowgirl/Right Leg.png"
# her thighs, kneecap to hip crease ("Tight" is the author's file name)
image shion srcg_left_thigh = "images/characters/Shion/Reverse Cowgirl/Butt/Tight Left.png"
image shion srcg_right_thigh = "images/characters/Shion/Reverse Cowgirl/Butt/Tight Right.png"
image shion srcg_butt_bottom_1 = "images/characters/Shion/Reverse Cowgirl/Butt/Butt Bottom 1.png"
image shion srcg_butt_bottom_2 = "images/characters/Shion/Reverse Cowgirl/Butt/Butt Bottom 2.png"
image shion srcg_butt_bottom_3 = "images/characters/Shion/Reverse Cowgirl/Butt/Butt Bottom 3.png"
# The cheeks alone (New Butt Top 1, 2026-10-06; the thighs are their own layers). The anal mask (Butt Top 2 = Top 1 +
# the wedge that closes the cleft in an arch over her anus, 926-993 x 658-726) has no cheeks-only file yet: it is the
# new Top 1 with that wedge cut out of the old Top 2 (the old Top 1 / Top 2 files still carry the thighs).
image shion srcg_butt_top_1 = "images/characters/Shion/Reverse Cowgirl/Butt/New Butt Top 1.png"
image shion srcg_butt_top_2 = Composite((1920, 1080),
    (0, 0), "images/characters/Shion/Reverse Cowgirl/Butt/New Butt Top 1.png",
    (926, 658), Crop((926, 658, 68, 69), "images/characters/Shion/Reverse Cowgirl/Butt/Butt Top 2.png"))

# ── Cum images ──────────────────────────────────────────────

image shion srcg_cum_butt = "images/characters/Shion/Reverse Cowgirl/Cum/Cum Butt.png"
image shion srcg_cum_pussy = "images/characters/Shion/Reverse Cowgirl/Cum/Cum Pussy.png"
image shion srcg_cum = "images/characters/Shion/Reverse Cowgirl/Cum/Cum.png"

# ── Clothing images ─────────────────────────────────────────

image shion srcg_cl_torso_clothes = "images/characters/Shion/Reverse Cowgirl/Clothes/Torso Clothes.png"
image shion srcg_cl_left_arm_clothes = "images/characters/Shion/Reverse Cowgirl/Clothes/Left Arm Clothes.png"
image shion srcg_cl_bikini_top = "images/characters/Shion/Reverse Cowgirl/Clothes/Bikini Top Reverse Cowgirl.png"
image shion srcg_cl_bikini_bottom_1 = "images/characters/Shion/Reverse Cowgirl/Clothes/Reverse Cowgirl Bikini Bottom 1.png"
image shion srcg_cl_bikini_bottom_2 = "images/characters/Shion/Reverse Cowgirl/Clothes/Reverse Cowgirl Bikini Bottom 2.png"
image shion srcg_cl_panties_1 = "images/characters/Shion/Reverse Cowgirl/Clothes/Panties 1.png"
image shion srcg_cl_panties_2 = "images/characters/Shion/Reverse Cowgirl/Clothes/Panties 2.png"
image shion srcg_cl_panties_3 = "images/characters/Shion/Reverse Cowgirl/Clothes/Panties 3.png"
image shion srcg_cl_pants = "images/characters/Shion/Reverse Cowgirl/Clothes/Pants.png"
