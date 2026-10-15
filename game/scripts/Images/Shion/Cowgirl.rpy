# ============================================================
# Shion Cowgirl -- Custom layer structure (3-part torso)
# Different from standard Cowgirl: Torso Bottom/Ass/Pussy
# with penis sandwiched between them, separate Legs/Thighs.
# ============================================================

default _scg_girl = None

# ── Motion ───────────────────────────────────────────────────
# Her layers ride the standard Cowgirl clock (Core_Cowgirl: _cg_slot_func / _cg_boobs_func, driven by
# store.cowgirl_speed and store._cg_anim_origin, so speed, bounce, sway and zoom are the other girls'), shifted:
# her art is drawn SEATED, where that clock puts the girl at yoffset 104 (its idle and its static value), and his
# body is drawn in the same canvas where the standard guy sits at yoffset 30. The transforms are position-neutral
# for her 1920 x 1080 layers (anchor = align), exactly like the standard ones.

transform scg_girl:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    function _scg_slot_func

transform scg_boobs:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    function _scg_boobs_func

# speed 0 / frozen: nothing moves at all (author's call: no breathing, no sway, no micro-bounce)
transform scg_still:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0

transform scg_guy:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    function _scg_guy_func

transform scg_guy_body:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    function _scg_guy_body_func

init python:

    _SCG_GIRL_SHIFT = -104.0
    _SCG_GUY_SHIFT = -30.0
    # her penetration point on her seated art (the landing's squash pivots there: Core_Cowgirl _cg_squash_matrix),
    # and his hips on his body, where the penis sits (he breathes around it, so the penis never slides on him)
    _SCG_SEAT = (1305, 828)
    _SCG_GUY_HIPS = (1305, 985)

    def _scg_slot_func(trans, st, at):
        _cg_slot_func(trans, st, at, seat=_SCG_SEAT)
        trans.yoffset += _SCG_GIRL_SHIFT
        return 0

    def _scg_boobs_func(trans, st, at):
        _cg_boobs_func(trans, st, at, seat=_SCG_SEAT)
        trans.yoffset += _SCG_GIRL_SHIFT
        return 0

    def _scg_guy_func(trans, st, at):
        """The penis and the condom: pressed down with her weight as she sits deeper (Core_Cowgirl _cg_guy_now, the
        standard penis's press, here from 0); still at speed 0 / frozen."""
        trans.yoffset = _cg_guy_now()
        return 0

    def _scg_guy_body_func(trans, st, at):
        """His body: the same press, and while she rides he breathes and shifts his weight around his hips
        (PLAYER_BREATH / PLAYER_SWAY, Core_RCG.rpy, the same as under her in the RCG). Speed 0 / frozen = still
        (author's call for this scene: nothing moves)."""
        trans.yoffset = _cg_guy_now()
        if _scg_is_still():
            trans.matrixtransform = ScaleMatrix(1.0, 1.0, 1.0)
            return 0
        _t = _time.time()
        _breath, _zx, _zy = PLAYER_BREATH.get(store.cowgirl_speed, PLAYER_BREATH[0])
        _sway, _deg = PLAYER_SWAY
        _in = 0.5 - 0.5 * math.cos(2.0 * math.pi * _t / _breath)
        trans.matrixanchor = _SCG_GUY_HIPS
        trans.matrixtransform = (ScaleMatrix(1.0 + (_zx - 1.0) * _in, 1.0 + (_zy - 1.0) * _in, 1.0)
                                 * RotateMatrix(0, 0, _deg * math.sin(2.0 * math.pi * _t / _sway)))
        return 0

    def _scg_is_still(speed=None):
        """Speed 0 (the argument when given, else store.cowgirl_speed) or frozen = completely still."""
        _s = store.cowgirl_speed if speed is None else speed
        return _s == 0 or getattr(store, "_cg_force_static", False)

    def _scg_girl_at(speed=None):
        """at_list of every layer of hers."""
        return [scg_still if _scg_is_still(speed) else scg_girl]

    def _scg_boobs_at(speed=None):
        return [scg_still if _scg_is_still(speed) else scg_boobs]

    def _scg_show_layers(girl=None):
        _scg_apply_speed(girl or store._scg_girl, 0)

    def _scg_hide_all():
        for _tag in ("scg_hair", "scg_guy", "scg_torso_bottom", "scg_penis",
                      "scg_condom", "scg_torso_ass", "scg_torso_pussy",
                      "scg_cum_ass", "scg_panties", "scg_cum_tummy",
                      "scg_arms", "scg_chest", "scg_nipples", "scg_bra",
                      "scg_over", "scg_head",
                      "scg_arms_cl", "scg_thigh_left", "scg_thigh_right",
                      "scg_leg_left", "scg_leg_right",
                      "scg_cum_legs", "scg_pants", "scg_hand",
                      "scg_cum_pussy", "scg_preg_belly"):
            renpy.hide(_tag)

    def _scg_apply_speed(girl, speed):
        """Show all Shion cowgirl layers with clothing/cum/condom state.
        Z-order from Photoshop (back->front):
        Hair(9950) Guy(9952) TorsoBot(9954) Penis(9956) Condom(9957)
        TorsoAss(9958) TorsoPussy(9959) CumPussy(9960) Panties(9962)
        CumTummy(9964) Arms(9966) Chest(9968) Nipples(9970) Bra(9971)
        Vest(9972) Jacket(9974) Head(9976) ArmsClothed(9980)
        Thighs(9982) Legs(9984) CumLegs(9986) Pants(9988) Hand(9992)
        Motion (see the transforms above): every layer of hers rides scg_girl (the boobs scg_boobs, their extra
        bounce), the penis and the condom ride scg_guy, his body scg_guy_body (the same press + his breathing); speed 0
        or frozen (_cg_force_static) = scg_still,
        nothing moves. The speed itself is store.cowgirl_speed (set by the caller, like the standard
        COWGIRL_ApplySpeed); the argument decides the stillness when the two disagree."""
        _pierced = getattr(girl, "Piercing", False)
        _girl_at = _scg_girl_at(speed)
        _boobs_at = _scg_boobs_at(speed)
        _guy_at = [scg_guy]

        # Back layers
        renpy.show("shion scg_hair", tag="scg_hair", at_list=_girl_at, zorder=9950)
        renpy.show("shion scg_guy", tag="scg_guy", at_list=[scg_guy_body], zorder=9952)
        renpy.show("shion scg_torso_bottom", tag="scg_torso_bottom", at_list=_girl_at, zorder=9954)
        renpy.show("shion scg_torso_ass", tag="scg_torso_ass", at_list=_girl_at, zorder=9958)
        renpy.show("shion scg_torso_pussy", tag="scg_torso_pussy", at_list=_girl_at, zorder=9959)

        # Penis -- between TorsoBottom and TorsoAss when inserted
        if speed >= 1 and store.cowgirl_started:
            renpy.show("shion scg_penis", tag="scg_penis", at_list=_guy_at, zorder=9956)
        else:
            renpy.show("shion scg_penis", tag="scg_penis", at_list=_guy_at, zorder=10060)

        # Condom -- just above Penis
        if store.condom_active and speed >= 1:
            renpy.show("shion scg_condom", tag="scg_condom", at_list=_guy_at, zorder=9957)
        else:
            renpy.hide("scg_condom")

        # Panties
        _pan = girl.Panties
        _pan_state = girl.clothes_state.get("panties", "full")
        if _pan:
            if _pan_state == "side":
                _pan_aside = "shion scg_cl_panties_aside" if _pan == "panties" else "shion scg_cl_bikini_bottom"
                renpy.show(_pan_aside, tag="scg_panties", at_list=_girl_at, zorder=9962)
            elif _pan_state != "down":
                _pan_img_map = {"panties": "shion scg_cl_panties", "bikini_bottom": "shion scg_cl_bikini_bottom"}
                _pan_img = _pan_img_map.get(_pan)
                if _pan_img:
                    renpy.show(_pan_img, tag="scg_panties", at_list=_girl_at, zorder=9962)
                else:
                    renpy.hide("scg_panties")
            else:
                renpy.hide("scg_panties")
        else:
            renpy.hide("scg_panties")

        # Arms (no clothing)
        _arms_v = getattr(store, "_scg_arms_variant", 1)
        _arms_map = {1: "shion scg_arms_1", 2: "shion scg_arms_2", "left": "shion scg_arms_left", "right": "shion scg_arm_right"}
        renpy.show(_arms_map.get(_arms_v, "shion scg_arms_1"), tag="scg_arms", at_list=_girl_at, zorder=9966)

        # Chest / Nipples (the boobs' own bounce)
        renpy.show("shion scg_chest", tag="scg_chest", at_list=_boobs_at, zorder=9968)
        if _pierced:
            renpy.show("shion scg_nipples_piercing", tag="scg_nipples", at_list=_boobs_at, zorder=9970)
        else:
            renpy.show("shion scg_nipples", tag="scg_nipples", at_list=_boobs_at, zorder=9970)

        # Chest clothing (bra/bikini_top), with the boobs
        _chest = girl.clothes.get("chest")
        _chest_up = girl.ChestUp
        if _chest == "bra" and not _chest_up:
            renpy.show("shion scg_bra", tag="scg_bra", at_list=_boobs_at, zorder=9971)
        elif _chest == "bikini_top" and not _chest_up:
            renpy.show("shion scg_cl_bikini_top", tag="scg_bra", at_list=_boobs_at, zorder=9971)
        else:
            renpy.hide("scg_bra")

        # Over clothing (vest/jacket)
        _over = girl.clothes.get("over")
        if _over == "vest":
            renpy.show("shion scg_cl_vest", tag="scg_over", at_list=_girl_at, zorder=9972)
        elif _over == "jacket":
            renpy.show("shion scg_cl_jacket", tag="scg_over", at_list=_girl_at, zorder=9974)
        else:
            renpy.hide("scg_over")

        # Head (includes blush/mouth/eyes/brows in layeredimage)
        renpy.show("shion scg_head", tag="scg_head", at_list=_girl_at, zorder=9976)

        # Arms clothing -- above Head
        if _over:
            _arms_cl_map = {1: "shion scg_cl_arms1_clothing", 2: "shion scg_cl_arms2_clothing", "left": "shion scg_cl_arm_left_clothing"}
            _arms_cl = _arms_cl_map.get(_arms_v)
            if _arms_cl and renpy.has_image(_arms_cl, exact=True):
                renpy.show(_arms_cl, tag="scg_arms_cl", at_list=_girl_at, zorder=9980)
            else:
                renpy.hide("scg_arms_cl")
        else:
            renpy.hide("scg_arms_cl")

        # Thighs and Legs -- in front
        renpy.show("shion scg_thigh_left", tag="scg_thigh_left", at_list=_girl_at, zorder=9982)
        renpy.show("shion scg_thigh_right", tag="scg_thigh_right", at_list=_girl_at, zorder=9982)
        renpy.show("shion scg_leg_left", tag="scg_leg_left", at_list=_girl_at, zorder=9984)
        renpy.show("shion scg_leg_right", tag="scg_leg_right", at_list=_girl_at, zorder=9984)

        # Pants
        _skirt = girl.Legs
        if _skirt:
            renpy.show("shion scg_cl_pants", tag="scg_pants", at_list=_girl_at, zorder=9988)
        else:
            renpy.hide("scg_pants")

        # Hand -- topmost (hers, on him: it moves with her like every layer of hers)
        renpy.show("shion scg_hand", tag="scg_hand", at_list=_girl_at, zorder=9992)

        # Cum layers
        if getattr(girl, "Cum", False):
            _cum_z = {"scg_cum_ass": 9960, "scg_cum_pussy": 9960, "scg_cum_tummy": 9964, "scg_cum_legs": 9986}
            for _cum_tag, _z in _cum_z.items():
                _cum_img = "shion %s" % _cum_tag
                if renpy.has_image(_cum_img, exact=True):
                    renpy.show(_cum_img, tag=_cum_tag, at_list=_girl_at, zorder=_z)
        else:
            for _cum_tag in ("scg_cum_ass", "scg_cum_legs", "scg_cum_pussy", "scg_cum_tummy"):
                renpy.hide(_cum_tag)

        # Pregnancy belly (PREG_ART, preg_art.rpy: Null before her first stage; the chest, nipples and bikini
        # top images follow her stage by themselves). It rides with her and adds its own small lag (preg_belly,
        # following scg_torso_bottom).
        renpy.show("shion scg_preg_belly", tag="scg_preg_belly", at_list=_girl_at, zorder=9961)

        print("[SCG_APPLY] speed=%d cowgirl_speed=%s started=%s frozen=%s clothes=%s" % (
            speed, getattr(store, "cowgirl_speed", None), store.cowgirl_started,
            getattr(store, "_cg_force_static", False), str(girl.clothes)))

    def _scg_set_arms(variant):
        store._scg_arms_variant = variant
        _girl_at = _scg_girl_at()
        _arms_map = {
            1: "shion scg_arms_1",
            2: "shion scg_arms_2",
            "left": "shion scg_arms_left",
            "right": "shion scg_arm_right",
        }
        _img = _arms_map.get(variant, "shion scg_arms_1")
        renpy.show(_img, tag="scg_arms", at_list=_girl_at, zorder=9966)
        _over = store._scg_girl.clothes.get("over") if store._scg_girl else None
        if _over:
            _arms_cl_map = {1: "shion scg_cl_arms1_clothing", 2: "shion scg_cl_arms2_clothing", "left": "shion scg_cl_arm_left_clothing"}
            _arms_cl = _arms_cl_map.get(variant)
            if _arms_cl and renpy.has_image(_arms_cl, exact=True):
                renpy.show(_arms_cl, tag="scg_arms_cl", at_list=_girl_at, zorder=9980)
            else:
                renpy.hide("scg_arms_cl")
        else:
            renpy.hide("scg_arms_cl")

# ── Minimal layeredimage (for _AT_SCENES has_image check) ───

layeredimage shion shion_cowgirl:
    always:
        "images/characters/Shion/Cowgirl/Torso Bottom.png"

# ── Head + Expression layeredimage ──────────────────────────

layeredimage shion scg_head:

    always:
        "images/characters/Shion/Cowgirl/Head.png"

    always:
        ConditionSwitch(
            "_gs('scg', 'blush', 0) >= 2",
            "images/characters/Shion/Cowgirl/Head/Blush 2.png",
            "_gs('scg', 'blush', 0) >= 1",
            "images/characters/Shion/Cowgirl/Head/Blush 1.png",
            "True", Null()
        )

    always:
        ConditionSwitch(
            "_gs('scg', 'mouth') == 'mouth_tongue'",
            "images/characters/Shion/Cowgirl/Expression/Mouth/Tongue.png",
            "_gs('scg', 'mouth') == 'mouth_kiss'",
            "images/characters/Shion/Cowgirl/Expression/Mouth/Kiss.png",
            "_gs('scg', 'mouth') == 'mouth_sad'",
            "images/characters/Shion/Cowgirl/Expression/Mouth/Sad.png",
            "_gs('scg', 'mouth') == 'mouth_laugh'",
            "images/characters/Shion/Cowgirl/Expression/Mouth/Laugh.png",
            "_gs('scg', 'mouth') == 'mouth_screaming'",
            "images/characters/Shion/Cowgirl/Expression/Mouth/Screaming.png",
            "_gs('scg', 'mouth') == 'mouth_smile'",
            "images/characters/Shion/Cowgirl/Expression/Mouth/Smile.png",
            "_gs('scg', 'mouth') in ('mouth_moaning_2', 'mouth_surprised', 'mouth_open_teeth')",
            "images/characters/Shion/Cowgirl/Expression/Mouth/Moaning 2.png",
            "_gs('scg', 'mouth') == 'mouth_moaning_3'",
            "images/characters/Shion/Cowgirl/Expression/Mouth/Moaning 3.png",
            "_gs('scg', 'mouth') in ('mouth_moaning', 'mouth_serious')",
            "images/characters/Shion/Cowgirl/Expression/Mouth/Moaning 1.png",
            "_gs('scg', 'mouth') == 'mouth_angry'",
            "images/characters/Shion/Cowgirl/Expression/Mouth/Angry.png",
            "_gs('scg', 'mouth') == 'mouth_lipbite'",
            "images/characters/Shion/Cowgirl/Expression/Mouth/Lipbite.png",
            "_gs('scg', 'mouth') == 'mouth_scared'",
            "images/characters/Shion/Cowgirl/Expression/Mouth/Scared.png",
            "True",
            "images/characters/Shion/Cowgirl/Expression/Mouth/Normal.png",
        )

    always:
        ConditionSwitch(
            "_gs('scg', 'eyes') == 'eyes_ahegao'",
            "images/characters/Shion/Cowgirl/Expression/Eyes/Ahegao 1.png",
            "_gs('scg', 'eyes') == 'eyes_ahegao_2'",
            "images/characters/Shion/Cowgirl/Expression/Eyes/Ahegao 2.png",
            "_gs('scg', 'eyes') == 'eyes_bliss'",
            "images/characters/Shion/Cowgirl/Expression/Eyes/Bliss.png",
            "_gs('scg', 'eyes') == 'eyes_sexy'",
            "images/characters/Shion/Cowgirl/Expression/Eyes/Sexy.png",
            "_gs('scg', 'eyes') == 'eyes_away'",
            "images/characters/Shion/Cowgirl/Expression/Eyes/Away.png",
            "_gs('scg', 'eyes') == 'eyes_up'",
            "images/characters/Shion/Cowgirl/Expression/Eyes/Up.png",
            "_gs('scg', 'eyes') == 'eyes_squint'",
            "images/characters/Shion/Cowgirl/Expression/Eyes/Squint.png",
            "_gs('scg', 'eyes') == 'eyes_surprised'",
            "images/characters/Shion/Cowgirl/Expression/Eyes/Surprised.png",
            "_gs('scg', 'eyes') == 'eyes_left_closed'",
            "images/characters/Shion/Cowgirl/Expression/Eyes/Closed Left.png",
            "_gs('scg', 'eyes') == 'eyes_right_closed'",
            "images/characters/Shion/Cowgirl/Expression/Eyes/Closed Right.png",
            "_gs('scg', 'eyes') == 'eyes_closed_happy'",
            "images/characters/Shion/Cowgirl/Expression/Eyes/Closed Happy.png",
            "_gs('scg', 'eyes') in ('eyes_closed', 'eyes_closed_2')",
            "images/characters/Shion/Cowgirl/Expression/Eyes/Closed.png",
            "_gs('scg', 'eyes') == 'eyes_looking_left'",
            "images/characters/Shion/Cowgirl/Expression/Eyes/Looking Left.png",
            "_gs('scg', 'eyes') == 'eyes_looking_right'",
            "images/characters/Shion/Cowgirl/Expression/Eyes/Looking Right.png",
            "_gs('scg', 'eyes') == 'eyes_up_closed_left'",
            "images/characters/Shion/Cowgirl/Expression/Eyes/Up Closed Left.png",
            "_gs('scg', 'eyes') == 'eyes_up_closed_right'",
            "images/characters/Shion/Cowgirl/Expression/Eyes/Up Closed Right.png",
            "True",
            "images/characters/Shion/Cowgirl/Expression/Eyes/Normal.png",
        )

    always:
        ConditionSwitch(
            "_gs('scg', 'brows') == 'brows_sad'",
            "images/characters/Shion/Cowgirl/Expression/Brows/Sad.png",
            "_gs('scg', 'brows') in ('brows_surprised', 'brows_confused')",
            "images/characters/Shion/Cowgirl/Expression/Brows/Perplexed 1.png",
            "_gs('scg', 'brows') == 'brows_perplexed_2'",
            "images/characters/Shion/Cowgirl/Expression/Brows/Perplexed 2.png",
            "_gs('scg', 'brows') == 'brows_angry'",
            "images/characters/Shion/Cowgirl/Expression/Brows/Angry.png",
            "_gs('scg', 'brows') == 'brows_scared'",
            "images/characters/Shion/Cowgirl/Expression/Brows/Scared.png",
            "True",
            "images/characters/Shion/Cowgirl/Expression/Brows/Normal.png",
        )

# ── Static body images ──────────────────────────────────────

# his body and penis by his skin (_p_one_skin, variables.rpy: the artist drew him white only; the condom is skin-free)
image shion scg_guy = _p_one_skin("images/characters/Shion/Cowgirl/Guy/Guy.png")
image shion scg_penis = _p_one_skin("images/characters/Shion/Cowgirl/Guy/Penis.png")
image shion scg_condom = "images/characters/Shion/Cowgirl/Guy/Condom.png"
image shion scg_torso_bottom = "images/characters/Shion/Cowgirl/Torso Bottom.png"
image shion scg_torso_ass = "images/characters/Shion/Cowgirl/Torso Ass.png"
image shion scg_torso_pussy = "images/characters/Shion/Cowgirl/Torso Pussy.png"
image shion scg_leg_left = "images/characters/Shion/Cowgirl/Leg Left.png"
image shion scg_leg_right = "images/characters/Shion/Cowgirl/Leg Right.png"
image shion scg_thigh_left = "images/characters/Shion/Cowgirl/Thigh Left.png"
image shion scg_thigh_right = "images/characters/Shion/Cowgirl/Thigh Right.png"
image shion scg_hand = "images/characters/Shion/Cowgirl/Hand.png"
image shion scg_hair = "images/characters/Shion/Cowgirl/Hair.png"
image shion scg_chest = preg_art("shion", "Cowgirl/Chest/Chest.png")
image shion scg_nipples = preg_art("shion", "Cowgirl/Chest/Nipples.png")
image shion scg_nipples_piercing = preg_art("shion", "Cowgirl/Chest/Nipples Piercing.png")
image shion scg_bra = "images/characters/Shion/Cowgirl/Chest/Bra.png"
image shion scg_arms_1 = "images/characters/Shion/Cowgirl/Arms/Arms 1.png"
image shion scg_arms_2 = "images/characters/Shion/Cowgirl/Arms/Arms 2.png"
image shion scg_arms_left = "images/characters/Shion/Cowgirl/Arms/Arms Left.png"
image shion scg_arm_right = "images/characters/Shion/Cowgirl/Arms/Arm Right.png"

# ── Cum images ──────────────────────────────────────────────

image shion scg_cum_ass = "images/characters/Shion/Cowgirl/Cum/Cum Ass.png"
image shion scg_cum_legs = "images/characters/Shion/Cowgirl/Cum/Cum Legs.png"
image shion scg_cum_pussy = "images/characters/Shion/Cowgirl/Cum/Cum Pussy.png"
image shion scg_cum_tummy = "images/characters/Shion/Cowgirl/Cum/Cum Tummy.png"

# ── Clothing images ─────────────────────────────────────────

image shion scg_cl_vest = "images/characters/Shion/Cowgirl/Clothes/Vest.png"
image shion scg_cl_jacket = "images/characters/Shion/Cowgirl/Clothes/Jacket.png"
image shion scg_cl_bikini_top = preg_art("shion", "Cowgirl/Clothes/Bikini Top.png")
image shion scg_cl_bikini_bottom = "images/characters/Shion/Cowgirl/Clothes/Bikini Bottom.png"
image shion scg_cl_panties = "images/characters/Shion/Cowgirl/Clothes/Panties.png"
image shion scg_cl_panties_aside = "images/characters/Shion/Cowgirl/Clothes/Panties Aside.png"
image shion scg_cl_pants = "images/characters/Shion/Cowgirl/Clothes/Pants.png"
image shion scg_cl_arms1_clothing = "images/characters/Shion/Cowgirl/Clothes/Arms 1 Clothing.png"
image shion scg_cl_arms2_clothing = "images/characters/Shion/Cowgirl/Clothes/Arms 2 Clothing.png"
image shion scg_cl_arm_left_clothing = "images/characters/Shion/Cowgirl/Clothes/Arm Left Clothing.png"

# ── Pregnancy images ────────────────────────────────────────

image shion scg_preg_belly = preg_belly("shion", "+Cowgirl/belly", body_tag="scg_torso_bottom")
