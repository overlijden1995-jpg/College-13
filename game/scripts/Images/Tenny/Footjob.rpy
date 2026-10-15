# ============================================================
# Tenny Footjob -- Exclusive pose
# Core file: Core_Footjob.rpy (FT_ControlMenu, FT_End)
# ============================================================
# Unique animation system: pre-rendered GIF frames (extracted to PNG)
# organised by her legwear variant ("Legs" bare / "White Pants" = her white_legs, read at FT_Launch) and the
# player's skin color (Player.skin). The body is static layers (_FT_Z): bare arms and sleeves BEHIND the torso
# (she leans back on them), body and its clothing under the animation (frames have real alpha), head on top.
# Stages per variant: Moviment (24, loop), Before Cum (12), Cum (24, burst),
# Moviment With Cum (24, loop once he has cum on her).

# ── Store defaults ───────────────────────────────────────────

default _ft_girl = None
default _ft_speed = 0
default _ft_phase = "move"
default _ft_player_clothing = "Legs"
default _ft_player_skin = "White"
default _ft_move_t0 = None
default _ft_phase_t0 = None
default _ft_has_cum = False
default _ft_cum_spots = set()

# ── Animation engine ────────────────────────────────────────

init python:

    _FT_FRAME_DURS = {1: 0.07, 2: 0.045, 3: 0.03}
    _FT_MOVE_FRAMES = 24
    _FT_CUM_FRAMES = 24
    _FT_BEFORE_CUM_FRAMES = 12
    _FT_CLOTHING_VARIANTS = ["Legs", "White Pants"]
    _FT_SKIN_VARIANTS = ["White", "Black"]

    def _ft_anim_base():
        return "images/characters/Tenny/Footjob/Animation/%s/%s" % (
            store._ft_player_clothing, store._ft_player_skin)

    def _ft_move_folder():
        # once he has cum on her, the move loop keeps it visible (same 24 frames, same timing)
        return "Moviment With Cum" if getattr(store, "_ft_has_cum", False) else "Moviment"

    def _ft_anim_frame(st, at):
        import time as _time
        base = _ft_anim_base()
        phase = store._ft_phase
        speed = store._ft_speed

        if phase == "move":
            move = _ft_move_folder()
            if speed == 0:
                return renpy.displayable("%s/%s/001.png" % (base, move)), None
            frame_dur = _FT_FRAME_DURS.get(speed, 0.07)
            t0 = getattr(store, "_ft_move_t0", None)
            if t0 is None:
                store._ft_move_t0 = _time.time()
                return renpy.displayable("%s/%s/001.png" % (base, move)), frame_dur
            elapsed = _time.time() - t0
            frame = (int(elapsed / frame_dur) % _FT_MOVE_FRAMES) + 1
            return renpy.displayable("%s/%s/%03d.png" % (base, move, frame)), frame_dur - (elapsed % frame_dur)

        t0 = getattr(store, "_ft_phase_t0", None)
        if t0 is None:
            return renpy.displayable("%s/%s/001.png" % (base, _ft_move_folder())), 0.1

        elapsed = _time.time() - t0
        if phase == "before_cum":
            n = _FT_BEFORE_CUM_FRAMES
            frame_dur = 0.08
            idx = min(int(elapsed / frame_dur), n - 1)
            d = renpy.displayable("%s/Before Cum/%03d.png" % (base, idx + 1))
            if idx < n - 1:
                return d, frame_dur - (elapsed % frame_dur)
            return d, None

        elif phase == "cum":
            frame_dur = 0.06
            idx = int(elapsed / frame_dur)
            if idx < _FT_CUM_FRAMES:
                d = renpy.displayable("%s/Cum/%03d.png" % (base, idx + 1))
                return d, frame_dur - (elapsed % frame_dur)
            # burst over: keep moving with his cum on her until the phase changes
            loop_dur = 0.07
            loop_elapsed = elapsed - _FT_CUM_FRAMES * frame_dur
            frame = (int(loop_elapsed / loop_dur) % _FT_MOVE_FRAMES) + 1
            return renpy.displayable("%s/Moviment With Cum/%03d.png" % (base, frame)), loop_dur - (loop_elapsed % loop_dur)

        return renpy.displayable("%s/%s/001.png" % (base, _ft_move_folder())), None

    def _ft_before_cum_duration():
        return _FT_BEFORE_CUM_FRAMES * 0.08

    def _ft_show_anim(speed=None):
        if speed is not None:
            store._ft_speed = speed
        renpy.show("tenny ft_anim", tag="ft_anim", zorder=_FT_Z["anim"])

    # The stack, bottom to top: her bare arms BEHIND the torso (she leans back on them; the torso's own outline is
    # what separates body from arm — arms ABOVE the torso melt into one wide slab), their sleeves on them, the body,
    # its clothing, the animation (her legs, his body), the head. Nipples sit ON the chest or they vanish behind it.
    _FT_Z = {
        "arm": 9966, "arm_cloth": 9967, "over_arm_cloth": 9968,     # behind the torso
        "torso": 9970, "pelvis": 9972, "pelvis_cloth": 9973,
        "chest": 9976, "nipples": 9978,
        "chest_cloth": 9979, "mid_cloth": 9980, "over_cloth": 9981,
        "cum_body": 9982,       # his cum on her belly / boobs: on the skin or the clothes, BEHIND the penis (anim)
        "anim": 9983, "head": 9985,
        "cum_face": 9986,       # his cum on her face: over the head and its expressions
    }
    _FT_CLOTH_TAGS = ("ft_cloth_arm_l", "ft_cloth_arm_r", "ft_cloth_over_arm_l", "ft_cloth_over_arm_r",
                      "ft_cloth_mid_pelvis", "ft_cloth_chest", "ft_cloth_mid", "ft_cloth_over")

    # His cum on her body (PlayerCumMenu_Outside_Oral "On her face / tits / belly", Cum.rpy): spot -> (tag, image, z)
    _FT_CUM_OVERLAYS = {
        "face":  ("ft_cum_face",  "tenny ft_cum_face",  "cum_face"),
        "boobs": ("ft_cum_boobs", "tenny ft_cum_boobs", "cum_body"),
        "belly": ("ft_cum_belly", "tenny ft_cum_belly", "cum_body"),
    }

    def _ft_add_cum(*spots):
        """His cum lands on her ("face" / "boobs" / "belly"): remembered, then EVERY static re-shown together so the
        body sway of all layers stays in phase (a lone show would bob out of sync with the rest)."""
        store._ft_cum_spots = set(getattr(store, "_ft_cum_spots", set())) | set(spots)
        _ft_show_layers()
        print("[FT] cum overlays: %s" % sorted(store._ft_cum_spots))

    # The light rise and fall of her body with the pace (the frames only move her legs): one amplitude per speed,
    # period = one full animation loop. Every static layer takes the same transform IN THE SAME re-show, so they bob
    # as one body. Speed 0 = still.
    _FT_SWAY_AMP = {1: 2.0, 2: 3.0, 3: 4.0}

    def _ft_body_at():
        _amp = _FT_SWAY_AMP.get(store._ft_speed)
        if not _amp or store._ft_speed <= 0:
            return []
        _per = _FT_MOVE_FRAMES * _FT_FRAME_DURS.get(store._ft_speed, 0.07)
        return [ft_body_sway(_amp, _per)]

    def _ft_show_cum(at_list=None):
        _at = _ft_body_at() if at_list is None else at_list
        for _spot in getattr(store, "_ft_cum_spots", set()):
            _tag, _img, _zkey = _FT_CUM_OVERLAYS[_spot]
            renpy.show(_img, tag=_tag, at_list=_at, zorder=_FT_Z[_zkey])

    def _ft_clothing_layers(girl):
        """(tag, image, zorder) for what she is wearing. This unique pose draws its own statics (no CLOTHING_REGISTRY
        "footjob" entries), and no strip action reaches it: what she wears at launch stays. States follow the
        registry's meaning ("full" worn, "up" pulled up). Her legwear is the ANIMATION variant (_ft_player_clothing),
        and a piece with no footjob art (towel, panties, shoes) simply does not draw."""
        _out = []
        _cl = getattr(girl, "clothes", {}) or {}
        _st = getattr(girl, "clothes_state", {}) or {}
        # chest: the blue bikini top / the white bra ("Top" assets)
        _chest = _cl.get("chest")
        if _chest == "blue_bikini_top":
            _out.append(("ft_cloth_chest", "tenny ft_bikini_top_up" if _st.get("chest") == "up" else "tenny ft_bikini_top_down", _FT_Z["chest_cloth"]))
        elif _chest == "white_bra":
            _out.append(("ft_cloth_chest", "tenny ft_white_top_up" if _st.get("chest") == "up" else "tenny ft_white_top_down", _FT_Z["chest_cloth"]))
        # mid: the blue shirt. Pulled up, the sleeves stay on her arms; torso and hem are out of the way
        if _cl.get("mid") == "blue_shirt":
            _out.append(("ft_cloth_arm_l", "tenny ft_shirt_arm_left", _FT_Z["arm_cloth"]))
            _out.append(("ft_cloth_arm_r", "tenny ft_shirt_arm_right", _FT_Z["arm_cloth"]))
            if _st.get("mid") != "up":
                _out.append(("ft_cloth_mid", "tenny ft_shirt_torso", _FT_Z["mid_cloth"]))
                _out.append(("ft_cloth_mid_pelvis", "tenny ft_shirt_pelvis", _FT_Z["pelvis_cloth"]))
        # over: the blue jacket. Pulled up it hangs from her arms
        if _cl.get("over") == "blue_jacket":
            _out.append(("ft_cloth_over_arm_l", "tenny ft_jacket_arm_left", _FT_Z["over_arm_cloth"]))
            _out.append(("ft_cloth_over_arm_r", "tenny ft_jacket_arm_right", _FT_Z["over_arm_cloth"]))
            if _st.get("over") != "up":
                _out.append(("ft_cloth_over", "tenny ft_jacket_torso", _FT_Z["over_cloth"]))
        return _out

    def _ft_show_layers():
        _girl = store._ft_girl
        _at = _ft_body_at()
        renpy.show("tenny ft_arm_left", tag="ft_arm_left", at_list=_at, zorder=_FT_Z["arm"])
        renpy.show("tenny ft_arm_right", tag="ft_arm_right", at_list=_at, zorder=_FT_Z["arm"])
        renpy.show("tenny ft_torso", tag="ft_torso", at_list=_at, zorder=_FT_Z["torso"])
        renpy.show("tenny ft_pelvis", tag="ft_pelvis", at_list=_at, zorder=_FT_Z["pelvis"])
        renpy.show("tenny ft_chest", tag="ft_chest", at_list=_at, zorder=_FT_Z["chest"])
        _pierced = getattr(_girl, "Piercing", False) if _girl else False
        if _pierced:
            renpy.show("tenny ft_nipples_piercing", tag="ft_nipples", at_list=_at, zorder=_FT_Z["nipples"])
        else:
            renpy.show("tenny ft_nipples", tag="ft_nipples", at_list=_at, zorder=_FT_Z["nipples"])
        for _tag in _FT_CLOTH_TAGS:
            renpy.hide(_tag)
        if _girl is not None:
            for _tag, _img, _z in _ft_clothing_layers(_girl):
                renpy.show(_img, tag=_tag, at_list=_at, zorder=_z)
        renpy.show("tenny ft_head", tag="ft_head", at_list=_at, zorder=_FT_Z["head"])
        _ft_show_cum(_at)

    def _ft_hide_all():
        for _tag in ("ft_anim", "ft_pelvis", "ft_torso", "ft_nipples", "ft_chest",
                      "ft_arm_left", "ft_arm_right", "ft_head",
                      "ft_cum_face", "ft_cum_boobs", "ft_cum_belly") + _FT_CLOTH_TAGS:
            renpy.hide(_tag)

    # The in-pose strip actions (Core_Footjob "Strip her..."): (label, (slot, "up" | None)) for what she wears now.
    # "up" = pulled up / off the shoulders (the registry state), None = taken off for the scene (the saved outfit
    # comes back at the scene end, scene_full_cleanup)
    def _ft_strip_choices(girl):
        _cl = getattr(girl, "clothes", {}) or {}
        _st = getattr(girl, "clothes_state", {}) or {}
        _out = []
        if _cl.get("over") == "blue_jacket":
            if _st.get("over") != "up":
                _out.append((_tl(_("Slide her jacket off her shoulders")), ("over", "up")))
            _out.append((_tl(_("Take her jacket off")), ("over", None)))
        if _cl.get("mid") == "blue_shirt":
            if _st.get("mid") != "up":
                _out.append((_tl(_("Pull her shirt up")), ("mid", "up")))
            _out.append((_tl(_("Take her shirt off")), ("mid", None)))
        if _cl.get("chest") in ("blue_bikini_top", "white_bra"):
            if _st.get("chest") != "up":
                _out.append((_tl(_("Pull her top up")), ("chest", "up")))
            _out.append((_tl(_("Take her top off")), ("chest", None)))
        return _out

    def _ft_strip_apply(girl, slot, val):
        """One strip action: the state through Outfit_Change (refresh=False: this pose redraws itself)."""
        if val == "up":
            girl.Outfit_Change(refresh=False, **{slot + "_up": True})
        else:
            girl.Outfit_Change(refresh=False, **{slot: "none"})
        _ft_show_layers()
        print("[FT] strip: %s %s -> %s (clothes %s, states %s)" % (
            girl.gid, slot, val or "off", dict(girl.clothes), dict(girl.clothes_state)))

# ── Body sway (the light rise and fall of her body with the pace) ──

transform ft_body_sway(amp=2.0, per=1.2):
    subpixel True
    block:
        easeout (per / 2.0) yoffset -amp
        easein (per / 2.0) yoffset 0.0
        repeat

# ── Animation image ─────────────────────────────────────────

image tenny ft_anim = DynamicDisplayable(_ft_anim_frame)

# ── Minimal layeredimage (for _AT_SCENES has_image check) ───

layeredimage tenny footjob:
    always:
        "images/characters/Tenny/Footjob/Torso.png"

# ── Head + Expression layeredimage ──────────────────────────

layeredimage tenny ft_head:

    always:
        "images/characters/Tenny/Footjob/Head/Head.png"

    # Blush
    always:
        ConditionSwitch(
            "_gs('ft', 'blush', 0) >= 2",
            "images/characters/Tenny/Footjob/Head/Blush 2.png",
            "_gs('ft', 'blush', 0) >= 1",
            "images/characters/Tenny/Footjob/Head/Blush 1.png",
            "True", Null()
        )

    # Mouth
    always:
        ConditionSwitch(
            "_gs('ft', 'mouth') == 'mouth_tongue'",
            "images/characters/Tenny/Footjob/Expression/Mouth/Tongue.png",
            "_gs('ft', 'mouth') == 'mouth_lipbite'",
            "images/characters/Tenny/Footjob/Expression/Mouth/Lipbite.png",
            "_gs('ft', 'mouth') == 'mouth_kiss'",
            "images/characters/Tenny/Footjob/Expression/Mouth/Kiss.png",
            "_gs('ft', 'mouth') == 'mouth_scared'",
            "images/characters/Tenny/Footjob/Expression/Mouth/Scared.png",
            "_gs('ft', 'mouth') == 'mouth_angry'",
            "images/characters/Tenny/Footjob/Expression/Mouth/Angry.png",
            "_gs('ft', 'mouth') == 'mouth_sad'",
            "images/characters/Tenny/Footjob/Expression/Mouth/Sad.png",
            "_gs('ft', 'mouth') == 'mouth_laugh'",
            "images/characters/Tenny/Footjob/Expression/Mouth/Laugh.png",
            "_gs('ft', 'mouth') == 'mouth_screaming'",
            "images/characters/Tenny/Footjob/Expression/Mouth/Screaming.png",
            "_gs('ft', 'mouth') in ('mouth_moaning_2', 'mouth_surprised', 'mouth_open_teeth', 'mouth_sch')",
            "images/characters/Tenny/Footjob/Expression/Mouth/Moaning 2.png",
            "_gs('ft', 'mouth') == 'mouth_moaning_3'",
            "images/characters/Tenny/Footjob/Expression/Mouth/Moaning 3.png",
            "_gs('ft', 'mouth') == 'mouth_smile'",
            "images/characters/Tenny/Footjob/Expression/Mouth/Smile.png",
            "_gs('ft', 'mouth') in ('mouth_moaning', 'mouth_serious')",
            "images/characters/Tenny/Footjob/Expression/Mouth/Moaning.png",
            "True",
            "images/characters/Tenny/Footjob/Expression/Mouth/Normal.png",
        )

    # Eyes
    always:
        ConditionSwitch(
            "getattr(store, 'ft_blink', False)",
            "images/characters/Tenny/Footjob/Expression/Eye/Closed.png",
            "_gs('ft', 'eyes') == 'eyes_ahegao'",
            "images/characters/Tenny/Footjob/Expression/Eye/Ahegao.png",
            "_gs('ft', 'eyes') == 'eyes_ahegao_2'",
            "images/characters/Tenny/Footjob/Expression/Eye/Ahegao 2.png",
            "_gs('ft', 'eyes') == 'eyes_bliss'",
            "images/characters/Tenny/Footjob/Expression/Eye/Bliss.png",
            "_gs('ft', 'eyes') == 'eyes_sexy'",
            "images/characters/Tenny/Footjob/Expression/Eye/Sexy.png",
            "_gs('ft', 'eyes') == 'eyes_sexy_2'",
            "images/characters/Tenny/Footjob/Expression/Eye/Sexy 2.png",
            "_gs('ft', 'eyes') == 'eyes_up'",
            "images/characters/Tenny/Footjob/Expression/Eye/Up.png",
            "_gs('ft', 'eyes') == 'eyes_away'",
            "images/characters/Tenny/Footjob/Expression/Eye/Away.png",
            "_gs('ft', 'eyes') == 'eyes_side'",
            "images/characters/Tenny/Footjob/Expression/Eye/Looking Left.png",
            "_gs('ft', 'eyes') == 'eyes_side_2'",
            "images/characters/Tenny/Footjob/Expression/Eye/Looking Right.png",
            "_gs('ft', 'eyes') == 'eyes_left_closed'",
            "images/characters/Tenny/Footjob/Expression/Eye/Left Closed.png",
            "_gs('ft', 'eyes') == 'eyes_right_closed'",
            "images/characters/Tenny/Footjob/Expression/Eye/Right Closed.png",
            "_gs('ft', 'eyes') == 'eyes_up_closed_left'",
            "images/characters/Tenny/Footjob/Expression/Eye/Up Closed Left.png",
            "_gs('ft', 'eyes') == 'eyes_up_closed_right'",
            "images/characters/Tenny/Footjob/Expression/Eye/Up Closed Right.png",
            "_gs('ft', 'eyes') == 'eyes_up_closed_surprised'",
            "images/characters/Tenny/Footjob/Expression/Eye/Up Closed Surprised.png",
            "_gs('ft', 'eyes') in ('eyes_closed', 'eyes_squint_big', 'eyes_closed_2')",
            "images/characters/Tenny/Footjob/Expression/Eye/Closed.png",
            "True",
            "images/characters/Tenny/Footjob/Expression/Eye/Normal.png",
        )

    # Brows
    always:
        ConditionSwitch(
            "_gs('ft', 'brows') == 'brows_angry'",
            "images/characters/Tenny/Footjob/Expression/Brown/Angry.png",
            "_gs('ft', 'brows') == 'brows_sad'",
            "images/characters/Tenny/Footjob/Expression/Brown/Sad.png",
            "_gs('ft', 'brows') == 'brows_scared'",
            "images/characters/Tenny/Footjob/Expression/Brown/Scared.png",
            "_gs('ft', 'brows') in ('brows_surprised', 'brows_confused')",
            "images/characters/Tenny/Footjob/Expression/Brown/Perplexed.png",
            "_gs('ft', 'brows') == 'brows_perplexed_2'",
            "images/characters/Tenny/Footjob/Expression/Brown/Perplexed 2.png",
            "_gs('ft', 'brows') == 'brows_determined'",
            "images/characters/Tenny/Footjob/Expression/Brown/Determinated.png",
            "True",
            "images/characters/Tenny/Footjob/Expression/Brown/Normal.png",
        )


# ── Static body images ──────────────────────────────────────

image tenny ft_torso = "images/characters/Tenny/Footjob/Torso.png"
image tenny ft_chest = "images/characters/Tenny/Footjob/Chest.png"
image tenny ft_nipples = "images/characters/Tenny/Footjob/Nipples.png"
image tenny ft_nipples_piercing = "images/characters/Tenny/Footjob/Nipples Piercing.png"
image tenny ft_pelvis = "images/characters/Tenny/Footjob/Pelvis.png"
image tenny ft_arm_left = "images/characters/Tenny/Footjob/Arm Left.png"
image tenny ft_arm_right = "images/characters/Tenny/Footjob/Arm Right.png"

# ── Cum overlays (PlayerCumMenu_Outside_Oral: face / tits / belly) ──

image tenny ft_cum_face = "images/characters/Tenny/Footjob/Cum/Face Cum.png"
image tenny ft_cum_boobs = "images/characters/Tenny/Footjob/Cum/Boobs Cum.png"
image tenny ft_cum_belly = "images/characters/Tenny/Footjob/Cum/Belly Cum.png"

# ── Clothing images ──────────────────────────────────────────

image tenny ft_bikini_top_down = "images/characters/Tenny/Footjob/Clothing/Blue Bikini/Blue Bikini Top Down.png"
image tenny ft_bikini_top_up = "images/characters/Tenny/Footjob/Clothing/Blue Bikini/Blue Bikini Top Up.png"
image tenny ft_jacket_torso = "images/characters/Tenny/Footjob/Clothing/Blue Jacket/Blue Jacket Torso.png"
image tenny ft_jacket_arm_left = "images/characters/Tenny/Footjob/Clothing/Blue Jacket/Blue Jacket Arm Left.png"
image tenny ft_jacket_arm_right = "images/characters/Tenny/Footjob/Clothing/Blue Jacket/Blue Jacket Arm Right.png"
image tenny ft_shirt_torso = "images/characters/Tenny/Footjob/Clothing/Blue Shirt/Blue Shirt Torso.png"
image tenny ft_shirt_pelvis = "images/characters/Tenny/Footjob/Clothing/Blue Shirt/Blue Shirt Pelvis.png"
image tenny ft_shirt_arm_left = "images/characters/Tenny/Footjob/Clothing/Blue Shirt/Blue Shirt Arm Left.png"
image tenny ft_shirt_arm_right = "images/characters/Tenny/Footjob/Clothing/Blue Shirt/Blue Shirt Arm Right.png"
image tenny ft_white_top_down = "images/characters/Tenny/Footjob/Clothing/Top/White Top Down.png"
image tenny ft_white_top_up = "images/characters/Tenny/Footjob/Clothing/Top/White Top Up.png"

# ── Launch / ApplySpeed labels ───────────────────────────────

label FT_Launch(girl):
    $ sub_event_reset(girl)
    $ _kill_scene_threads()
    $ stop_standing_blink(girl)
    $ public_attention_reset()
    call PlayerExposure(girl) from _call_PlayerExposure_ft

    $ girl._prev_pose = getattr(girl, "default_pose", "standing")
    $ girl._prev_slot = getattr(girl, "SpriteLoc", StageCenter)
    if not getattr(girl, "_saved_outfit", None):
        $ girl.SaveOutfit()

    python:
        import time as _time
        _hide_all_scene_layers(girl)
        hide_girl_sprite(girl)
        store.hiding_face = False
        store._ft_girl = girl
        store._ft_speed = 0
        store._ft_phase = "move"
        store._ft_has_cum = False
        store._ft_cum_spots = set()
        store._ft_move_t0 = _time.time()
        store._ft_phase_t0 = None
        # a towel has no footjob art: it falls when she sits back
        if getattr(girl, "Over", None) == "towel":
            girl.Outfit_Change(over="none", refresh=False)
        # the animation variant: her white pants have their own frames; the player's skin picks the set
        _ft_pants = girl.clothes.get("skirt") == "white_legs" and girl.clothes_state.get("skirt", "full") == "full"
        store._ft_player_clothing = "White Pants" if _ft_pants else "Legs"
        unlock_achievement("best_foot_forward")
        _ft_skin = getattr(store.Player, "skin", "White")
        store._ft_player_skin = _ft_skin if _ft_skin in _FT_SKIN_VARIANTS else "White"
        sprite_state.setdefault(girl.Id, {})["pose"] = "footjob"
        print("[FT_Launch] %s clothing=%s skin=%s clothes=%s" % (
            girl.gid, store._ft_player_clothing, store._ft_player_skin, dict(girl.clothes)))
    # the room stays as the backdrop (a `scene black` here blacked the whole screen out for the scene)
    python:
        _ft_show_anim(0)
        _ft_show_layers()
    with dissolve
    return

label FT_ApplySpeed(girl, speed=0):
    python:
        import time as _time
        store._ft_speed = speed
        store._ft_phase = "move"
        store._ft_move_t0 = _time.time()
        store._ft_phase_t0 = None
        _ft_show_anim(speed)
        _ft_show_layers()
        print("[FT_ApplySpeed] speed=%d clothing=%s skin=%s has_cum=%s" % (
            speed, store._ft_player_clothing, store._ft_player_skin, store._ft_has_cum))
    return

label FT_CumAnim(girl):
    # His cum on her feet ("On her feet" through _cum_dispatch_anim): Before Cum (12 frames),
    # the Cum burst (24), then _ft_anim_frame keeps the Moviment With Cum loop until the next phase.
    $ _apply_cum_expression(girl, "footjob", "outside")
    python:
        import time as _time
        store._ft_phase = "before_cum"
        store._ft_phase_t0 = _time.time()
        store._ft_has_cum = True
        print("[FT_CumAnim] before_cum %.2fs then cum" % _ft_before_cum_duration())
    $ renpy.pause(_ft_before_cum_duration(), hard=True)
    python:
        import time as _time
        store._ft_phase = "cum"
        store._ft_phase_t0 = _time.time()
    with vpunch
    $ renpy.pause(_FT_CUM_FRAMES * 0.06, hard=True)
    return
