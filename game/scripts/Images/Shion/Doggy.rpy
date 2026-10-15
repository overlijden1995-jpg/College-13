# ============================================================
# Shion Doggy -- Custom layer structure
# Different from standard Doggy: simpler, no separate limbs, 7 butt state variants.
# Two heads: 1 = from behind (no face), 2 = her face turned to him, with expressions (the scenes use 2).
# ============================================================

default _sdg_girl = None
default _sdg_butt_state = "closed"
default _sdg_head_pos = 1
default _sdg_guy_on = False   # his body and penis are drawn: from his first start in this scene (_sdg_apply_speed)
# he pulled out while the scene goes on: "out" = the penis drawn over her (his cum outside), "hidden" = not drawn (the
# creampie's aftermath), None = where the scene puts him (inside her once started, at ANY speed: speed 0 there is a
# pause, never a pull-out). Moving again (speed 1+) puts him back in (_sdg_apply_speed)
default _sdg_penis_out = None

# ── Thrust: his body and the penis go forward (toward her, +x: this view is from the side) and back, by speed ──
transform sdg_thrust(period, amp):
    xoffset 0
    ease period * 0.45 xoffset amp
    pause period * 0.10
    ease period * 0.45 xoffset 0
    repeat

# ── Her hand between her legs (her solo scene, DG_MASTURBATE_*, and while he is in her ass): a small rub, by
# speed, mostly up and down her slit (yamp) with a little forward (amp) ──
transform sdg_hand_rub(period, amp, yamp):
    xoffset 0 yoffset 0
    ease period / 2.0 xoffset amp yoffset (-yamp)
    ease period / 2.0 xoffset 0 yoffset 0
    repeat

# ── Her body on his thrust (the penetration and the thighjob), one pivot per group ──────────────
# The impact is the deepest point of sdg_thrust (same period, shown in the same call: in phase). Every group is
# pushed forward with him (+x, a fraction of his amplitude); on top of that the lower body squashes sideways at the
# point he hits (_SDG_PIVOT_BUTT) and jiggles back, the head nods forward on its neck (_SDG_PIVOT_NECK) and the
# hanging chest swings forward from where it meets the torso (_SDG_PIVOT_CHEST). transform_anchor + anchor = pos keeps
# every 1920 x 1080 layer in place while it zooms / rotates around that pivot.
# Nothing of hers moves up or down: her butt, the thigh mask and the pants run to the frame's bottom row (y 1079), so a
# vertical squash or lift opens a gap under them (author, 2026-10-09). The squash is xzoom only.
transform sdg_body_push(period, amp):
    subpixel True
    xoffset 0
    ease period * 0.45 xoffset amp
    pause period * 0.10
    ease period * 0.45 xoffset 0
    repeat

transform sdg_butt_jiggle(period, amp, sx):
    subpixel True
    transform_anchor True
    anchor _SDG_PIVOT_BUTT pos _SDG_PIVOT_BUTT
    xoffset 0 xzoom 1.0
    ease period * 0.45 xoffset amp xzoom sx
    pause period * 0.10
    ease period * 0.25 xoffset (amp * 0.3) xzoom (2.0 - sx)
    ease period * 0.20 xoffset 0 xzoom 1.0
    repeat

# rotate: positive = clockwise on screen. The head pivots at the neck below it, so a forward nod (its top toward
# her face side, +x) is a positive angle.
transform sdg_head_nod(period, amp, deg):
    subpixel True
    transform_anchor True
    anchor _SDG_PIVOT_NECK pos _SDG_PIVOT_NECK
    xoffset 0 rotate 0
    ease period * 0.45 xoffset amp rotate deg
    pause period * 0.10
    ease period * 0.45 xoffset 0 rotate 0
    repeat

# The chest hangs below its pivot: a forward swing (its bottom toward +x) is a negative angle, then it swings back
# past the rest a little.
transform sdg_chest_swing(period, amp, deg):
    subpixel True
    transform_anchor True
    anchor _SDG_PIVOT_CHEST pos _SDG_PIVOT_CHEST
    xoffset 0 rotate 0
    ease period * 0.45 xoffset amp rotate (-deg)
    pause period * 0.10
    ease period * 0.25 xoffset (amp * 0.3) rotate (deg * 0.4)
    ease period * 0.20 xoffset 0 rotate 0
    repeat

init python:

    # (period s, amplitude px) per speed: the standard doggy penis timings (speed 4 = cumming inside, short and deep)
    _SDG_THRUST_PARAMS = {1: (2.0, 50), 2: (0.8, 80), 3: (0.36, 110), 4: (0.34, 60)}
    # (period s, forward px, up px) of her hand per masturbation speed
    _SDG_HAND_PARAMS = {1: (0.9, 5, 9), 2: (0.5, 6, 12), 3: (0.3, 8, 15)}
    # Her body on each thrust, per speed: push px of every group, xzoom of the lower body at the impact (sideways
    # only: sdg_butt_jiggle), head nod degrees, chest swing degrees
    _SDG_BODY_PARAMS = {
        1: (10, 1.020, 2.0, 4.0),
        2: (16, 1.030, 3.0, 6.0),
        3: (22, 1.040, 4.5, 8.0),
        4: (14, 1.030, 3.0, 6.0),
    }
    # Her body on her own hand (her solo scene, nothing of his in her): the same groups at the hand's period, far
    # smaller than on his thrust (author, 2026-10-05: "the body must move much less"), so her thighs and her hand
    # rock together
    _SDG_MAST_BODY_PARAMS = {
        1: (2, 1.004, 0.5, 1.0),
        2: (3, 1.006, 0.8, 1.5),
        3: (4, 1.008, 1.0, 2.0),
    }
    # Pivots, px of the 1920 x 1080 layers, measured on the art (2026-10-05): where he hits her (between the two
    # holes: vagina patch 719-877 x 494-768, anus 733-866 x 376-516), her neck where Head 2 (1246-1687 x 30-471)
    # meets the shoulder (1223-1483 x 285-631), the top of the hanging chest (1279-1511 x 481-847)
    _SDG_PIVOT_BUTT = (790, 540)
    _SDG_PIVOT_NECK = (1330, 420)
    _SDG_PIVOT_CHEST = (1395, 485)

    def _sdg_body_params(speed):
        """(period, push, sx, nod, swing) of her body at that speed: his thrust while he works, her own hand's
        rhythm in her solo scene, None = still (speed 0, the preview)."""
        if _sdg_guy_at(speed):
            return (_SDG_THRUST_PARAMS[speed][0],) + _SDG_BODY_PARAMS.get(speed, _SDG_BODY_PARAMS[1])
        if _sdg_mode() == "mast" and _SDG_HAND_PARAMS.get(speed):
            return (_SDG_HAND_PARAMS[speed][0],) + _SDG_MAST_BODY_PARAMS.get(speed, _SDG_MAST_BODY_PARAMS[1])
        return None

    def _sdg_body_at(speed):
        """at_lists of her layer groups ({"body", "head", "chest", "butt"}): on his thrust while he works, on her
        own hand in her solo scene, all empty = still (speed 0, the preview)."""
        _p = _sdg_body_params(speed)
        if not _p:
            return {"body": [], "head": [], "chest": [], "butt": []}
        _period, _push, _sx, _nod, _swing = _p
        return {
            "body": [sdg_body_push(_period, _push)],
            "head": [sdg_head_nod(_period, _push, _nod)],
            "chest": [sdg_chest_swing(_period, _push, _swing)],
            "butt": [sdg_butt_jiggle(_period, _push, _sx)],
        }

    def _sdg_hand_at(speed, butt_at):
        """at_list of her hand between her legs: it rides on her lower body (the same motion as the thighs it is
        between, butt_at) and rubs on top of that at the SAME period, so the two never drift apart. Still at speed
        0."""
        _p = _sdg_body_params(speed)
        _hp = _SDG_HAND_PARAMS.get(speed) or (_SDG_HAND_PARAMS[3] if speed > 3 else None)
        if not _p or not _hp:
            return []
        return list(butt_at) + [sdg_hand_rub(_p[0], _hp[1], _hp[2])]

    def _sdg_hand_on():
        """Her hand between her legs: her solo scene, or her touching herself while he is in her ass (the player's
        "touch yourself" in the anal menu, self_touch_anal). Never during the vaginal penetration (no art for it),
        and never in the massage / sunscreen (_dg_massage: her solo DISPLAY borrowed with her hands to herself)."""
        if getattr(store, "_dg_massage", False):
            return False
        if not getattr(store, "_dg_masturbating", False):
            return False
        if getattr(store, "doggy_started", False) and not getattr(store, "doggy_anal", False):
            return False
        return True

    def _sdg_mode():
        """"mast": her solo scene (_dg_masturbating before anything of his is in her, DG_MASTURBATE_* in Core_Doggy:
        nothing of his drawn). "rub": his penis between her thighs (doggy_rub_mode before the scene starts, the
        thighjob pair). "sex": the penetration (her hand joins it in her ass: _sdg_hand_on), or the preview before
        it."""
        if getattr(store, "_dg_masturbating", False) and not getattr(store, "doggy_started", False):
            return "mast"
        if getattr(store, "doggy_rub_mode", False) and not getattr(store, "doggy_started", False):
            return "rub"
        return "sex"

    def _sdg_guy_at(speed):
        """at_list of his body and the penis: the thrust at that speed while he works (inside her, or between her
        thighs), still otherwise. Both are shown in the same call so they start in phase."""
        _m = _sdg_mode()
        _working = _m == "rub" or (_m == "sex" and getattr(store, "doggy_started", False))
        _p = _SDG_THRUST_PARAMS.get(speed) if _working else None
        return [sdg_thrust(_p[0], _p[1])] if _p else []

    # closed / <hole>_open (the penis inside). The hole he already used this session gapes on its own ("Butt Top
    # ... After" patches, from _dg_had_pussy / _dg_had_anal like the standard doggy's "after" bases). The "All Open"
    # files are out (the author renamed them "NOT USE").
    _SDG_BUTT_STATES = ["closed", "vagina_open", "ass_open"]

    def _sdg_show_layers(girl=None):
        _sdg_apply_speed(girl or store._sdg_girl, 0)

    def _sdg_guy_img():
        """His body (Player/<skin>/Doggy Shion, by his skin): the thighjob one for the rub (his hips low, the penis
        under her pussy), the anal one with his hips up at her anus, the other at her pussy. Not drawn at all in her
        solo scene (_sdg_apply_speed)."""
        if _sdg_mode() == "rub":
            return "shion sdg_guy_thighjob"
        return "shion sdg_guy_anal" if getattr(store, "doggy_anal", False) else "shion sdg_guy"

    def _sdg_penis_img():
        if _sdg_mode() == "rub":
            return "shion sdg_penis_thighjob"
        return "shion sdg_penis_anal" if getattr(store, "doggy_anal", False) else "shion sdg_penis"

    def _sdg_condom_img():
        """The condom on the penis, the same three as the penis: between her thighs, in her ass, in her pussy (the
        torn one: _condom_img_tag adds "_broken")."""
        if _sdg_mode() == "rub":
            return "shion sdg_condom_thighjob"
        return "shion sdg_condom_anal" if getattr(store, "doggy_anal", False) else "shion sdg_condom"

    def _sdg_show_penis(at_list, zorder=9978):
        """The penis (9978, between the two butt halves; 10060 = pulled out, over her) with the condom on it while he
        wears one: one displayable, so the condom rides every frame of the thrust."""
        _pen = _sdg_penis_img()
        if getattr(store, "condom_active", False):
            _con = _condom_img_tag(_sdg_condom_img())
            scene_show(_pen, what=Fixed(renpy.displayable(_pen), renpy.displayable(_con), fit_first=True),
                       tag="sdg_penis", at_list=at_list, zorder=zorder)
        else:
            scene_show(_pen, tag="sdg_penis", at_list=at_list, zorder=zorder)

    def _sdg_show_butt(at_list=None):
        """Her butt: the bottom half (9962) UNDER the penis, the top half and the "After" patches (9979) ABOVE
        the penis (9978), so the penis enters between the two halves. HandMask (9980) over everything.
        A hole already used this session gapes whenever he is not inside it. at_list: the lower body's
        motion on his thrust (_sdg_body_at "butt"), the same on every piece so the holes stay on the butt."""
        _at = at_list or []
        _state = store._sdg_butt_state
        _butt_bottom_map = {
            "closed": "shion sdg_butt",
            "vagina_open": "shion sdg_butt_bottom_vagina_open",
            "ass_open": "shion sdg_butt_bottom_ass_open",
        }
        _butt_top_map = {
            "closed": None,
            "vagina_open": "shion sdg_butt_top_vagina_open",
            "ass_open": "shion sdg_butt_top_ass_open",
        }
        scene_show(_butt_bottom_map.get(_state, "shion sdg_butt"), tag="sdg_butt_bottom", at_list=_at, zorder=9962)
        _top = _butt_top_map.get(_state)
        if _top:
            scene_show(_top, tag="sdg_butt_top", at_list=_at, zorder=9979)
        else:
            renpy.hide("sdg_butt_top")
        # what this session already did (the hole he is in counts once the scene started)
        _is_anal = getattr(store, "doggy_anal", False)
        _started = getattr(store, "doggy_started", False)
        _used_p = getattr(store, "_dg_had_pussy", False) or (_started and not _is_anal)
        _used_a = getattr(store, "_dg_had_anal", False) or (_started and _is_anal)
        if _used_p and _state != "vagina_open":
            scene_show("shion sdg_butt_top_vagina_after", tag="sdg_after_vagina", at_list=_at, zorder=9979)
        else:
            renpy.hide("sdg_after_vagina")
        if _used_a and _state != "ass_open":
            scene_show("shion sdg_butt_top_ass_after", tag="sdg_after_ass", at_list=_at, zorder=9979)
        else:
            renpy.hide("sdg_after_ass")
        print("[SDG_BUTT] state=%s anal=%s started=%s used_p=%s used_a=%s" % (_state, _is_anal, _started, _used_p, _used_a))

    def _sdg_hide_all():
        for _tag in ("sdg_guy", "sdg_shoulder", "sdg_shoulder_cl",
                      "sdg_chest", "sdg_bra", "sdg_over",
                      "sdg_penis", "sdg_butt_bottom", "sdg_butt_top",
                      "sdg_after_vagina", "sdg_after_ass", "sdg_hand", "sdg_hand_mask",
                      "sdg_head", "sdg_hair", "sdg_panties", "sdg_pants",
                      "sdg_cum_ass", "sdg_cum_butt", "sdg_cum_vagina"):
            renpy.hide(_tag)

    # Cum z (the author 2026-10-11): what drips FROM a hole hangs behind the shaft, so it runs UNDER the
    # penis (9977 < penis 9978, like the penis it ducks the near-thigh mask); cum sitting ON her skin
    # stays above the mask (9982). (tag, girl.Cum visual word, z)
    _SDG_CUM_LAYERS = (
        ("sdg_cum_ass",    "dripping_ass", 9977),
        ("sdg_cum_vagina", "dripping",     9977),
        ("sdg_cum_butt",   "ass",          9982),
    )

    def _sdg_show_cum(girl, butt_at=None, now=None):
        """Shion's doggy cum layers: each only where his load actually went (girl.Cum visual tags, plus
        `now` for the load of THIS instant: the cum anims run BEFORE process_cum writes girl.Cum).
        Riding the butt group keeps them moving with her."""
        if butt_at is None:
            butt_at = _sdg_body_at(0)["butt"]
        _vis = set(getattr(girl, "Cum", []) or [])
        if now:
            _vis.add(now)
        for _ct, _cwhere, _cz in _SDG_CUM_LAYERS:
            _ci = "shion %s" % _ct
            if _cwhere in _vis and renpy.has_image(_ci, exact=True):
                scene_show(_ci, tag=_ct, at_list=butt_at, zorder=_cz)
            else:
                renpy.hide(_ct)
        print("[SDG_CUM] visual=%s now=%s" % (sorted(_vis), now))

    def _sdg_apply_speed(girl, speed):
        """Show all Shion doggy layers with clothing/cum state.
        Z-order (back->front):
        Jacket(9950) Hair(9952) Head(9954) Chest(9956) Bra(9957)
        Shoulder(9958) ShoulderCl(9960) ButtBot(9962)
        Guy(9976) Penis(9978) ButtTop/After(9979) Hand(9980) HandMask(9981) Cum(9982) Panties(9983) Pants(9984):
        penis enters between ButtBot (below) and ButtTop (above), HandMask over everything.
        Penetration = no clothes; thighjob = no pants.
        Her solo scene dressed: the clothes drop UNDER her hand (Panties 9975, Pants 9976),
        she rubs through them, and the near thigh (Hand Mask) stays over the hand, always."""
        _pierced = getattr(girl, "Piercing", False)
        _is_anal = getattr(store, "doggy_anal", False)
        # her hand never joins the vaginal penetration (no art): a "touch yourself" from the anal menu ends when
        # he moves to her pussy
        if getattr(store, "_dg_masturbating", False) and store.doggy_started and not _is_anal:
            print("[SDG_APPLY] her hand off: vaginal penetration")
            store._dg_masturbating = False
        _mode = _sdg_mode()
        _hand = _sdg_hand_on()
        _chest = girl.clothes.get("chest")
        _over = girl.clothes.get("over")
        # Moving (speed 1+) means he is in her; before the start there is nothing to pull out of
        if speed >= 1 or not store.doggy_started:
            store._sdg_penis_out = None
        _out = getattr(store, "_sdg_penis_out", None)
        # her body on his thrust (or on her own hand), one at_list per group (all still at speed 0)
        _b = _sdg_body_at(speed)

        # Jacket (backmost layer)
        if _over:
            scene_show("shion sdg_cl_jacket", tag="sdg_over", at_list=_b["body"], zorder=9950)
        else:
            renpy.hide("sdg_over")

        # Hair (with the head: it hangs from it)
        scene_show("shion sdg_hair", tag="sdg_hair", at_list=_b["head"], zorder=9952)

        # Head: 2 = her face turned to him; 1 = from behind, no face (she hides it: hiding_face, dg_has_hide_face)
        _head_pos = 1 if getattr(store, "hiding_face", False) else getattr(store, "_sdg_head_pos", 1)
        if _head_pos == 2:
            scene_show("shion sdg_head_2", tag="sdg_head", at_list=_b["head"], zorder=9954)
        else:
            scene_show("shion sdg_head", tag="sdg_head", at_list=_b["head"], zorder=9954)

        # Chest (piercing / vest / normal)
        if _over == "vest" or (_chest and not girl.ChestUp):
            scene_show("shion sdg_chest_vest", tag="sdg_chest", at_list=_b["chest"], zorder=9956)
        elif _pierced:
            scene_show("shion sdg_chest_piercing", tag="sdg_chest", at_list=_b["chest"], zorder=9956)
        else:
            scene_show("shion sdg_chest", tag="sdg_chest", at_list=_b["chest"], zorder=9956)

        # Bra (with the chest)
        if _chest == "bra" and not girl.ChestUp:
            scene_show("shion sdg_bra", tag="sdg_bra", at_list=_b["chest"], zorder=9957)
        elif _chest == "bikini_top" and not girl.ChestUp:
            scene_show("shion sdg_cl_bikini_top", tag="sdg_bra", at_list=_b["chest"], zorder=9957)
        else:
            renpy.hide("sdg_bra")

        # Shoulder + clothing (the torso: the push only)
        scene_show("shion sdg_shoulder", tag="sdg_shoulder", at_list=_b["body"], zorder=9958)
        if _over:
            scene_show("shion sdg_cl_shoulder_clothing", tag="sdg_shoulder_cl", at_list=_b["body"], zorder=9960)
        else:
            renpy.hide("sdg_shoulder_cl")

        # Butt state: the hole open around him while he is in her, at any speed (the freeze of his cum inside her is
        # still him inside: the "After" patch of that hole over a penis still in her was the bug, author 2026-10-11);
        # closed once he pulled out or before he started (a hole already used this session gapes by itself:
        # _sdg_show_butt); the lower body squashes and jiggles on his thrust
        if store.doggy_started and not _out:
            store._sdg_butt_state = "ass_open" if _is_anal else "vagina_open"
        else:
            store._sdg_butt_state = "closed"
        _sdg_show_butt(_b["butt"])

        # Guy (9976) + Penis (9978) between ButtBot (below) and ButtTop (above); the anal pair when he is in her
        # ass, the thighjob pair for the rub, both thrusting by speed (sdg_thrust). Nothing of his in her solo
        # scene ("mast"), nor before his first start (the preview, the bottom-clothes menu: author, 2026-10-09): the
        # penetration starting, or the rub moving; from then on he stays until the scene ends. ButtTop (9979) and
        # HandMask (9980) over the penis: ButtTop is the hole edge around him, HandMask hides what is inside her (or
        # between her thighs) and covers her hand's wrist (9977).
        # tip mode counts as his start too (review 2026-10-10: "Just the tip" drew her alone, no guy, no
        # penis, the whole tip phase: doggy_started stays False there)
        if store.doggy_started or getattr(store, "doggy_tip_mode", False) or (_mode == "rub" and speed >= 1):
            store._sdg_guy_on = True
        _guy_at = _sdg_guy_at(speed)
        if _mode == "mast" or not store._sdg_guy_on:
            renpy.hide("sdg_guy")
            renpy.hide("sdg_penis")
        else:
            scene_show(_sdg_guy_img(), tag="sdg_guy", at_list=_guy_at, zorder=9976)
            if _out == "hidden":
                renpy.hide("sdg_penis")
            elif _out == "out":
                _sdg_show_penis([], zorder=10060)
            else:
                _sdg_show_penis(_guy_at)
        scene_show("shion sdg_hand_mask", tag="sdg_hand_mask", at_list=_b["butt"], zorder=9981)

        # Clothes and cum sit ON her skin, so above the near-half mask (9979): the penis between her thighs runs
        # under her panties. Nothing of them once he is inside her (the penetration never happens dressed: the
        # bottom-clothes menu stripped her), and no pants in the thighjob (they hide him whole: no pulled-down art
        # for them in this pose, so the rub is drawn with them off). Panties pulled aside while she touches herself
        # = out of the way (no aside art here).
        # In her solo scene the clothes go UNDER her hand (she rubs through them) and under the near thigh, which
        # stays over the hand, always.
        _pan_z, _pants_z = (9975, 9976) if _mode == "mast" else (9983, 9984)
        _pan = girl.Panties
        _pan_state = girl.clothes_state.get("panties", "full")
        if _pan and _pan_state != "down" and not store.doggy_started and not (_mode == "mast" and _pan_state != "full"):
            _pan_map = {"panties": "shion sdg_cl_panties", "bikini_bottom": "shion sdg_cl_bikini_bottom"}
            _pan_img = _pan_map.get(_pan)
            if _pan_img:
                scene_show(_pan_img, tag="sdg_panties", at_list=_b["butt"], zorder=_pan_z)
            else:
                renpy.hide("sdg_panties")
        else:
            renpy.hide("sdg_panties")

        if girl.Legs and not store.doggy_started and _mode != "rub":
            scene_show("shion sdg_cl_pants", tag="sdg_pants", at_list=_b["butt"], zorder=_pants_z)
        else:
            renpy.hide("sdg_pants")

        # Her hand between her legs (9977): under the near-half mask, over the clothes in her solo scene. It rides
        # on the thighs' motion and rubs up and down on top of that (_sdg_hand_at).
        if _hand:
            scene_show("shion sdg_hand", tag="sdg_hand", at_list=_sdg_hand_at(speed, _b["butt"]), zorder=9980)
        else:
            renpy.hide("sdg_hand")

        # Cum layers, each only where his load actually went: one central shower (_sdg_show_cum), riding
        # the butt group so they move with her (the author 2026-10-11: the cum-moment loops painted all
        # three tags, static, over the penis)
        _sdg_show_cum(girl, butt_at=_b["butt"])

        print("[SDG_APPLY] speed=%d mode=%s hand=%s started=%s guy=%s penis_out=%s anal=%s condom=%s broken=%s butt=%s head=%d skin=%s clothes=%s" % (
            speed, _mode, _hand, store.doggy_started, store._sdg_guy_on, _out, _is_anal, getattr(store, "condom_active", False),
            getattr(store, "_condom_broken", False), store._sdg_butt_state, _head_pos, getattr(Player, "skin", "White"), str(girl.clothes)))

    def _sdg_switch_head(pos):
        store._sdg_head_pos = pos
        if store._sdg_girl:
            _sdg_apply_speed(store._sdg_girl, getattr(store, "_at_speed", 0))

# ── Minimal layeredimage (for _AT_SCENES has_image check) ───

layeredimage shion shion_doggy:
    always:
        "images/characters/Shion/Doggy/Shoulder.png"

# ── Head (no expressions). No blush in this pose: the files in Doggy/Head ("Blush Left / Right") are blush on her
# butt cheeks, never shown (author, 2026-10-09) ─────────────

layeredimage shion sdg_head:

    always:
        "images/characters/Shion/Doggy/Head.png"

# ── Head 2 (with full expressions) ──────────────────────────

layeredimage shion sdg_head_2:

    always:
        "images/characters/Shion/Doggy/Head 2/Head 2.png"

    always:
        ConditionSwitch(
            "_gs('sdg', 'mouth') == 'mouth_lipbite'",
            "images/characters/Shion/Doggy/Head 2/Mouth/Bitting Lip.png",
            "_gs('sdg', 'mouth') == 'mouth_happy'",
            "images/characters/Shion/Doggy/Head 2/Mouth/Happy.png",
            "_gs('sdg', 'mouth') == 'mouth_kiss'",
            "images/characters/Shion/Doggy/Head 2/Mouth/Kiss.png",
            "_gs('sdg', 'mouth') == 'mouth_moaning'",
            "images/characters/Shion/Doggy/Head 2/Mouth/Moaning.png",
            "_gs('sdg', 'mouth') == 'mouth_sad'",
            "images/characters/Shion/Doggy/Head 2/Mouth/Sad.png",
            "_gs('sdg', 'mouth') == 'mouth_scared'",
            "images/characters/Shion/Doggy/Head 2/Mouth/Scared.png",
            "_gs('sdg', 'mouth') == 'mouth_smile'",
            "images/characters/Shion/Doggy/Head 2/Mouth/Smile.png",
            "_gs('sdg', 'mouth') == 'mouth_surprised'",
            "images/characters/Shion/Doggy/Head 2/Mouth/Surprised.png",
            "_gs('sdg', 'mouth') == 'mouth_tongue'",
            "images/characters/Shion/Doggy/Head 2/Mouth/Tongue.png",
            "True",
            "images/characters/Shion/Doggy/Head 2/Mouth/Normal.png",
        )

    always:
        ConditionSwitch(
            "_gs('sdg', 'eyes') == 'eyes_ahegao'",
            "images/characters/Shion/Doggy/Head 2/Eyes/Ahegao.png",
            "_gs('sdg', 'eyes') == 'eyes_ahegao_2'",
            "images/characters/Shion/Doggy/Head 2/Eyes/Ahegao 2.png",
            "_gs('sdg', 'eyes') == 'eyes_blinking'",
            "images/characters/Shion/Doggy/Head 2/Eyes/Blinking.png",
            "_gs('sdg', 'eyes') == 'eyes_looking_left'",
            "images/characters/Shion/Doggy/Head 2/Eyes/Looking Left.png",
            "_gs('sdg', 'eyes') == 'eyes_looking_right'",
            "images/characters/Shion/Doggy/Head 2/Eyes/Looking Right.png",
            "_gs('sdg', 'eyes') == 'eyes_looking_to_player'",
            "images/characters/Shion/Doggy/Head 2/Eyes/Looking To Player.png",
            "_gs('sdg', 'eyes') == 'eyes_looking_up'",
            "images/characters/Shion/Doggy/Head 2/Eyes/Looking Up.png",
            "_gs('sdg', 'eyes') == 'eyes_sexy'",
            "images/characters/Shion/Doggy/Head 2/Eyes/Sexy.png",
            "_gs('sdg', 'eyes') == 'eyes_surprised'",
            "images/characters/Shion/Doggy/Head 2/Eyes/Surprised.png",
            "_gs('sdg', 'eyes') in ('eyes_closed', 'eyes_closed_2')",
            "images/characters/Shion/Doggy/Head 2/Eyes/Blinking.png",
            "True",
            "images/characters/Shion/Doggy/Head 2/Eyes/Normal.png",
        )

    always:
        ConditionSwitch(
            "_gs('sdg', 'brows') == 'brows_angry'",
            "images/characters/Shion/Doggy/Head 2/Brows/Angry.png",
            "_gs('sdg', 'brows') == 'brows_closed'",
            "images/characters/Shion/Doggy/Head 2/Brows/Closed.png",
            "_gs('sdg', 'brows') == 'brows_happy'",
            "images/characters/Shion/Doggy/Head 2/Brows/Happy.png",
            "_gs('sdg', 'brows') == 'brows_horny'",
            "images/characters/Shion/Doggy/Head 2/Brows/Horny.png",
            "_gs('sdg', 'brows') == 'brows_sad'",
            "images/characters/Shion/Doggy/Head 2/Brows/Sad.png",
            "_gs('sdg', 'brows') == 'brows_surprised'",
            "images/characters/Shion/Doggy/Head 2/Brows/Surprised.png",
            "_gs('sdg', 'brows') == 'brows_up'",
            "images/characters/Shion/Doggy/Head 2/Brows/Up.png",
            "_gs('sdg', 'brows') == 'brows_worried'",
            "images/characters/Shion/Doggy/Head 2/Brows/Worried.png",
            "True",
            "images/characters/Shion/Doggy/Head 2/Brows/Normal.png",
        )

# ── His side: the player, by his skin (Player/<skin>/Doggy Shion, _p() like every scene) ──────

image shion sdg_guy = _p("Doggy Shion/Guy.png")
image shion sdg_penis = _p("Doggy Shion/Penis.png")
image shion sdg_guy_anal = _p("Doggy Shion/Guy Anal.png")
image shion sdg_penis_anal = _p("Doggy Shion/Penis Anal.png")
image shion sdg_guy_thighjob = _p("Doggy Shion/Guy Thighjob.png")
image shion sdg_penis_thighjob = _p("Doggy Shion/Penis Thighjob.png")

# ── The condom on the penis (one per penis, the same for every skin), torn after a break (_condom_img_tag) ──
image shion sdg_condom = "images/characters/Player/Doggy Shion Condom.png"
image shion sdg_condom_broken = "images/characters/Player/Doggy Shion Condom Broke.png"
image shion sdg_condom_anal = "images/characters/Player/Doggy Shion Condom Anal.png"
image shion sdg_condom_anal_broken = "images/characters/Player/Doggy Shion Condom Anal Broke.png"
image shion sdg_condom_thighjob = "images/characters/Player/Doggy Shion Condom Thigh.png"
image shion sdg_condom_thighjob_broken = "images/characters/Player/Doggy Shion Condom Thigh Broke.png"

# ── His slap on her ass (SpankHer, _DOGGY_SLAP_OVERRIDES): one hand, full screen with the hand where it lands (on her
# far cheek, 982-1336 x 250-749). It swings in from the side to xoffset 0 (the impact), goes on and fades out ──
image shion sdg_slap = _p("Doggy Shion/Slap.png")

transform sdg_slap_in:
    subpixel True
    pos (0, 0)
    xoffset 400
    alpha 1.0
    easein 0.08 xoffset 0
    pause 0.15
    easeout 0.25 xoffset -400 alpha 0.0

# ── Her hand (masturbation) and the near thigh that goes over its wrist, and over the thighjob penis ──

image shion sdg_hand = "images/characters/Shion/Doggy/Hand.png"
image shion sdg_hand_mask = "images/characters/Shion/Doggy/Hand Mask.png"

# ── Static body images ──────────────────────────────────────

image shion sdg_shoulder = "images/characters/Shion/Doggy/Shoulder.png"
image shion sdg_head_only = "images/characters/Shion/Doggy/Head.png"
image shion sdg_hair = "images/characters/Shion/Doggy/Hair.png"
image shion sdg_chest = "images/characters/Shion/Doggy/Chest/Chest.png"
image shion sdg_chest_piercing = "images/characters/Shion/Doggy/Chest/Chest Piercing.png"
image shion sdg_chest_vest = "images/characters/Shion/Doggy/Chest/Chest Vest.png"
image shion sdg_bra = "images/characters/Shion/Doggy/Chest/Bra.png"

# ── Butt images ─────────────────────────────────────────────

image shion sdg_butt = "images/characters/Shion/Doggy/Butt/Butt.png"
image shion sdg_butt_bottom_vagina_open = "images/characters/Shion/Doggy/Butt/Butt Bottom Vagina Open.png"
image shion sdg_butt_bottom_ass_open = "images/characters/Shion/Doggy/Butt/Butt Bottom Ass Open.png"
image shion sdg_butt_top_vagina_open = "images/characters/Shion/Doggy/Butt/Butt Top Vagina Open.png"
image shion sdg_butt_top_ass_open = "images/characters/Shion/Doggy/Butt/Butt Top Ass Open.png"
image shion sdg_butt_top_vagina_after = "images/characters/Shion/Doggy/Butt/Butt Top Vagina After.png"
image shion sdg_butt_top_ass_after = "images/characters/Shion/Doggy/Butt/Butt Top Ass After.png"

# ── Cum images ──────────────────────────────────────────────

image shion sdg_cum_ass = "images/characters/Shion/Doggy/Cum/Cum Ass Dripping.png"
image shion sdg_cum_butt = "images/characters/Shion/Doggy/Cum/Cum Butt.png"
image shion sdg_cum_vagina = "images/characters/Shion/Doggy/Cum/Cum Vagina Dripping.png"

# ── Clothing images ─────────────────────────────────────────

image shion sdg_cl_bikini_top = "images/characters/Shion/Doggy/Clothes/Bikini Top.png"
image shion sdg_cl_bikini_bottom = "images/characters/Shion/Doggy/Clothes/Bikini Bottom.png"
image shion sdg_cl_panties = "images/characters/Shion/Doggy/Clothes/Panties.png"
image shion sdg_cl_pants = "images/characters/Shion/Doggy/Clothes/Pants.png"
image shion sdg_cl_jacket = "images/characters/Shion/Doggy/Clothes/Jacket.png"
image shion sdg_cl_shoulder_clothing = "images/characters/Shion/Doggy/Clothes/Shoulder Clothing.png"
