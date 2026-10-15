# ============================================================
# Art Test — press F9 to preview any scene at any speed
# For artists to test assets without playing through the game.
# Replace PNGs in game/images/ and press Shift+R to reload.
# ============================================================

screen art_test_hotkey():
    zorder 100
    key "K_F9" action Jump("art_test")

init python:
    config.overlay_screens.append("art_test_hotkey")

# ============================================================
# Expression Tester — press F10 to toggle overlay
# Works on any scene (standing, sex scenes, art test).
# ============================================================

init python:
    store._expr_tester_visible = False
    store._expr_tester_girl_idx = 0

    def _expr_tester_toggle():
        store._expr_tester_visible = not store._expr_tester_visible
        renpy.restart_interaction()

    def _expr_tester_get_girl():
        for var in ("_hj_girl", "_bj_girl", "_titjob_girl", "_cowgirl_girl", "_rcg_girl", "_doggy_girl", "_ft_girl", "_rj_girl"):
            g = getattr(store, var, None)
            if g is not None:
                return g
        g = getattr(store, "_at_girl", None)
        if g is not None:
            return g
        g = getattr(store, "CurrentGirl", None)
        if g is not None:
            return g
        if ALL_GIRLS:
            idx = store._expr_tester_girl_idx % len(ALL_GIRLS)
            return ALL_GIRLS[idx]
        return None

    def _expr_tester_cycle_girl(delta=1):
        if not ALL_GIRLS:
            return
        store._expr_tester_girl_idx = (store._expr_tester_girl_idx + delta) % len(ALL_GIRLS)
        renpy.restart_interaction()

    def _expr_tester_apply(expr_name):
        girl = _expr_tester_get_girl()
        if girl:
            set_scene_expression(girl, expr_name)
            renpy.restart_interaction()

    def _expr_tester_set_blush(val):
        girl = _expr_tester_get_girl()
        if girl:
            set_scene_expression(girl, None, blush=val)
            renpy.restart_interaction()

    def _expr_tester_set_part(part, val):
        girl = _expr_tester_get_girl()
        if girl:
            kwargs = {part: val}
            set_scene_expression(girl, None, **kwargs)
            renpy.restart_interaction()

    def _expr_tester_get_expressions():
        girl = _expr_tester_get_girl()
        if not girl:
            return []
        pose = _detect_scene_pose(girl)
        names = set()
        gpe = GIRL_POSE_EXPRESSIONS.get(girl.Id, {}).get(pose, {})
        names.update(gpe.keys())
        pe = POSE_EXPRESSIONS.get(pose, {})
        names.update(pe.keys())
        standing = POSE_EXPRESSIONS.get("standing", {})
        names.update(standing.keys())
        return sorted(names)

    config.overlay_screens.append("expr_tester_hotkey")

    # ============================================================
    # Arm Tester — press F11 to cycle arms for all outfits
    # ============================================================
    store._arm_tester_visible = False
    store._arm_tester_girl_idx = 0
    store._arm_tester_outfit_idx = 0
    store._arm_tester_arm_idx = 0

    # test outfits, shared by the F11 arm tester and the F9 art test: outfit -> (preset worn, slots taken off after).
    # No preset (or a girl without it) = every slot empty; the towel goes on the "over" slot.
    _AT_OUTFITS = ["casual", "no_over", "pool", "towel", "naked"]
    _AT_OUTFIT_RULES = {
        "casual":  ("casual", ()),
        "no_over": ("casual", ("over", "mid")),
        "pool":    ("pool", ()),
        "towel":   (None, ()),
        "naked":   (None, ()),
    }
    _ARM_TESTER_ARMS = [1, 2, 3, 4]

    def _at_apply_outfit(girl, outfit):
        """Dress `girl` in one of the _AT_OUTFITS, every clothing state back to "full"."""
        _preset, _off = _AT_OUTFIT_RULES[outfit]
        if _preset and _preset in OUTFIT_PRESETS.get(girl.Id, {}):
            girl.WearPreset(_preset, apply_now=False)
            for _slot in _off:
                girl.clothes[_slot] = None
        else:
            girl.clothes = {"over": "towel" if outfit == "towel" else None, "mid": None, "chest": None, "skirt": None, "panties": None, "shoes": None}
            girl.clothes_state = {"over": "full", "mid": "full", "chest": "full", "skirt": "full", "panties": "full", "shoes": "full"}
        if outfit == "towel":
            girl.shower_state = "towel"
        elif getattr(girl, "shower_state", None) == "towel":
            girl.shower_state = "dressed"

    def _at_show_standing(girl, arm):
        """Standing sprite at the centre with arm pose `arm` (1-4)."""
        stop_standing_blink(girl)
        hide_girl_sprite(girl)
        sprite_state.setdefault(girl.Id, {})["arm_pos"] = arm
        girl.loc = getattr(store, "CurrentLocation", "room")
        set_girl_sprite(girl, pose="standing", at_list=[slot_center])

    def _arm_tester_toggle():
        store._arm_tester_visible = not store._arm_tester_visible
        if store._arm_tester_visible:
            _arm_tester_refresh()
        renpy.restart_interaction()

    def _arm_tester_get_girl():
        if ALL_GIRLS:
            idx = store._arm_tester_girl_idx % len(ALL_GIRLS)
            return ALL_GIRLS[idx]
        return None

    def _arm_tester_cycle_girl(delta=1):
        if not ALL_GIRLS:
            return
        old_girl = _arm_tester_get_girl()
        store._arm_tester_girl_idx = (store._arm_tester_girl_idx + delta) % len(ALL_GIRLS)
        store._arm_tester_outfit_idx = 0
        store._arm_tester_arm_idx = 0
        if old_girl:
            hide_girl_sprite(old_girl)
        _arm_tester_refresh()

    def _arm_tester_cycle_outfit(delta=1):
        store._arm_tester_outfit_idx = (store._arm_tester_outfit_idx + delta) % len(_AT_OUTFITS)
        _arm_tester_refresh()

    def _arm_tester_cycle_arm(delta=1):
        store._arm_tester_arm_idx = (store._arm_tester_arm_idx + delta) % len(_ARM_TESTER_ARMS)
        _arm_tester_refresh()

    def _arm_tester_refresh():
        girl = _arm_tester_get_girl()
        if not girl:
            return
        outfit = _AT_OUTFITS[store._arm_tester_outfit_idx % len(_AT_OUTFITS)]
        arm = _ARM_TESTER_ARMS[store._arm_tester_arm_idx % len(_ARM_TESTER_ARMS)]

        _at_apply_outfit(girl, outfit)
        _at_show_standing(girl, arm)
        _test_attrs = _build_attributes_for_girl(girl, "standing")
        _arm_attrs = [a for a in _test_attrs if "arm" in a or "front" in a or "left" in a]
        print("[ARM_TESTER] %s outfit=%s arm=%d attrs=%s all=%s" % (girl.gid, outfit, arm, str(_arm_attrs), str(_test_attrs)))
        renpy.restart_interaction()

    config.overlay_screens.append("arm_tester_hotkey")

screen arm_tester_hotkey():
    zorder 99
    key "K_F11" action Function(_arm_tester_toggle)

screen arm_tester():
    zorder 201
    modal False

    python:
        _at_girl = _arm_tester_get_girl()
        _at_name = _at_girl.Name if _at_girl else "?"
        _at_outfit = _AT_OUTFITS[store._arm_tester_outfit_idx % len(_AT_OUTFITS)]
        _at_arm = _ARM_TESTER_ARMS[store._arm_tester_arm_idx % len(_ARM_TESTER_ARMS)]

    frame:
        xalign 0.5 yalign 0.0
        xpadding 15 ypadding 10
        background "#000000CC"

        vbox:
            spacing 8

            text "{b}ARM TESTER (F11){/b}" size 18 color "#FFD700"

            hbox:
                spacing 10
                textbutton "< Girl" action Function(_arm_tester_cycle_girl, -1) text_size 16
                text "[_at_name]" size 18 color "#FFFFFF" min_width 120 text_align 0.5
                textbutton "Girl >" action Function(_arm_tester_cycle_girl, 1) text_size 16

            hbox:
                spacing 10
                textbutton "< Outfit" action Function(_arm_tester_cycle_outfit, -1) text_size 16
                text "[_at_outfit]" size 18 color "#88FF88" min_width 120 text_align 0.5
                textbutton "Outfit >" action Function(_arm_tester_cycle_outfit, 1) text_size 16

            hbox:
                spacing 10
                textbutton "< Arm" action Function(_arm_tester_cycle_arm, -1) text_size 16
                text "Arm [_at_arm]" size 18 color "#88CCFF" min_width 120 text_align 0.5
                textbutton "Arm >" action Function(_arm_tester_cycle_arm, 1) text_size 16

            textbutton "Close (F11)" action Function(_arm_tester_toggle) text_size 14 xalign 0.5

screen _arm_tester_manager():
    if store._arm_tester_visible:
        use arm_tester

init python:
    config.overlay_screens.append("_arm_tester_manager")

screen expr_tester_hotkey():
    zorder 99
    key "K_F10" action Function(_expr_tester_toggle)

screen expression_tester():
    zorder 200
    modal False

    python:
        _et_girl = _expr_tester_get_girl()
        _et_gid = _et_girl.Id if _et_girl else "?"
        _et_name = _et_girl.Name if _et_girl else "None"
        _et_pose = _detect_scene_pose(_et_girl) if _et_girl else "standing"
        _et_exprs = _expr_tester_get_expressions()
        _et_state = sprite_state.get(_et_gid, {})
        _et_cur_eyes = _et_state.get("eyes", "?")
        _et_cur_brows = _et_state.get("brows", "?")
        _et_cur_mouth = _et_state.get("mouth", "?")
        _et_cur_blush = _et_state.get("blush", 0)
        _et_cur_expr = getattr(_et_girl, "current_expression", "?") if _et_girl else "?"

    frame:
        xalign 0.0
        yalign 0.0
        xsize 340
        ymaximum 1000
        background "#000000cc"
        padding (12, 12)

        vbox:
            spacing 6

            # Header
            hbox:
                spacing 8
                text "EXPRESSION TESTER" size 18 color "#ffcc00" bold True
                textbutton "X" action Function(_expr_tester_toggle) text_size 18 text_color "#ff4444"

            # Girl selector
            hbox:
                spacing 6
                textbutton "<" action Function(_expr_tester_cycle_girl, -1) text_size 16 text_color "#88ccff"
                text "[_et_name]" size 16 color "#88ccff" bold True
                textbutton ">" action Function(_expr_tester_cycle_girl, 1) text_size 16 text_color "#88ccff"

            # Current state
            text "Pose: [_et_pose]" size 14 color "#aaaaaa"
            text "Expr: [_et_cur_expr]" size 14 color "#aaaaaa"
            text "E: [_et_cur_eyes]" size 12 color "#888888"
            text "B: [_et_cur_brows]" size 12 color "#888888"
            text "M: [_et_cur_mouth]" size 12 color "#888888"

            # Blush row
            hbox:
                spacing 4
                text "Blush:" size 14 color "#cccccc"
                for _bv in range(3):
                    textbutton str(_bv):
                        text_size 14
                        text_color ("#ffcc00" if _et_cur_blush == _bv else "#cccccc")
                        action Function(_expr_tester_set_blush, _bv)

            null height 4

            # Expression buttons
            text "--- Expressions ---" size 14 color "#ffcc00"

            viewport:
                scrollbars "vertical"
                mousewheel True
                ymaximum 600
                xfill True

                vbox:
                    spacing 3
                    for _ename in _et_exprs:
                        textbutton _ename:
                            text_size 15
                            text_color ("#ffcc00" if _et_cur_expr == _ename else "#cccccc")
                            text_hover_color "#ffffff"
                            xfill True
                            action Function(_expr_tester_apply, _ename)

    timer 0.5 repeat True action Function(renpy.restart_interaction)

init python:
    def _show_expr_tester():
        if store._expr_tester_visible:
            renpy.show_screen("expression_tester")
        else:
            if renpy.get_screen("expression_tester"):
                renpy.hide_screen("expression_tester")

    config.overlay_screens.append("_expr_tester_manager")

screen _expr_tester_manager():
    if store._expr_tester_visible:
        use expression_tester

# ============================================================
# Art Test options: pregnancy stage, outfit, clothing states, piercings. ONE menu for every scene,
# built from CLOTHING_REGISTRY / OUTFIT_PRESETS / POSE_SLOTS, so a new girl or garment shows up by itself.
# ============================================================
init python:
    # tester scenes: (caption, layeredimage tag proving the girl owns the pose, clothing pose = CLOTHING_REGISTRY /
    # POSE_SLOTS key, tester label, store flags set first). A pose shows up for every girl that has its
    # layeredimage. Laying Down has no tester label yet.
    _AT_SCENES = [
        (_("Standing"),        "standing", "standing",        "_at_standing", {}),
        (_("Handjob"),         "handjob",  "handjob",         "_at_hj",       {}),
        (_("Blowjob"),         "blowjob",  "blowjob",         "_at_bj",       {}),
        (_("Titjob"),          "titjob",   "titjob",          "_at_tj",       {}),
        (_("Cowgirl"),         "cowgirl",  "cowgirl",         "_at_cg",       {}),
        (_("Reverse Cowgirl"), "rcg",      "reverse_cowgirl", "_at_rcg",      {}),
        (_("Doggy"),           "doggy",    "doggy",           "_at_dg",       {"doggy_anal": False}),
        (_("Doggy (Anal)"),    "doggy",    "doggy",           "_at_dg",       {"doggy_anal": True}),
        (_("Full Nelson"),     "fn",       "full_nelson",     "_at_fn",       {}),
        (_("Footjob"),         "footjob",  "footjob",         "_at_ft",       {}),
        (_("Cowgirl (Shion)"),  "shion_cowgirl",  "cowgirl",  "_at_shion_cg",  {}),
        (_("Rev. Cowgirl (Shion)"), "shion_rcg",  "reverse_cowgirl", "_at_shion_rcg", {}),
        (_("Doggy (Shion)"),   "shion_doggy",    "doggy",    "_at_shion_dg",  {}),
        (_("Rimjob"),          "rimjob",          "rimjob",   "_at_rimjob",    {}),
    ]
    # visual pregnancy stages (pregnancy_visual_stage), shown through preg_art_preview: never the real state
    _AT_PREG_STAGES = [_("0, normal body"), _("1, bigger breasts + small bump"), _("2, full belly")]

    # what each girl wore / had before the test. Init-time dict mutated in place: never saved.
    _AT_SNAPSHOT = {}

    def _at_snapshot(girl):
        if girl.gid not in _AT_SNAPSHOT:
            _AT_SNAPSHOT[girl.gid] = (dict(girl.clothes), dict(girl.clothes_state), getattr(girl, "Piercing", False), getattr(girl, "shower_state", None))

    def _at_restore_all():
        """Leaving the test (or starting it again): every tested girl back to what she wore, no pregnancy preview left on."""
        for _gid, (_clothes, _states, _piercing, _shower) in _AT_SNAPSHOT.items():
            _g = GIRL_BY_ID[_gid]
            _g.clothes = _clothes
            _g.clothes_state = _states
            _g.Piercing = _piercing
            _g.shower_state = _shower
            print("[ART_TEST] %s restored: clothes=%s piercing=%s" % (_gid, _clothes, _piercing))
        _AT_SNAPSHOT.clear()
        preg_art_preview()

    def _at_outfits_for(girl, pose):
        """Test outfits that make sense here: the towel only where her registry draws it (pose None = no scene
        yet, everything), the bikini only if she has a pool preset."""
        _reg = CLOTHING_REGISTRY.get(girl.gid, {})
        _out = []
        for _o in _AT_OUTFITS:
            if _o == "towel" and pose and _reg.get("towel", {}).get("poses", {}).get(pose) is None:
                continue
            if _o == "pool" and "pool" not in OUTFIT_PRESETS.get(girl.Id, {}):
                continue
            _out.append(_o)
        return _out

    def _at_dress(girl, pose=None):
        """Put the chosen test outfit on, remember its items (a slot switched "off" can come back), then put the
        tester's own slot choices back, as far as this pose draws them."""
        _at_apply_outfit(girl, store._at_outfit_name)
        store._at_outfit_items = dict(girl.clothes)
        _reg = CLOTHING_REGISTRY.get(girl.gid, {})
        for _slot, _state in store._at_tweaks.items():
            _item = store._at_outfit_items.get(_slot)
            if not _item:
                continue
            if _state == "off":
                girl.clothes[_slot] = None
            elif pose is None or _state in (_reg.get(_item, {}).get("poses", {}).get(pose) or {}):
                girl.clothes_state[_slot] = _state

    def _at_state_rows(girl, pose):
        """[(slot, item, states)] for every garment of the test outfit this pose draws: its states for the pose,
        then "off". Same lookups as _build_clothing_attributes: a chest hidden by the WORN over / mid is left out."""
        _reg = CLOTHING_REGISTRY.get(girl.gid, {})
        _hides = any(_reg.get(girl.clothes.get(_s), {}).get("hides_chest")
                     and _reg.get(girl.clothes.get(_s), {}).get("poses", {}).get(pose) is not None
                     for _s in ("over", "mid"))
        _rows = []
        for _slot in POSE_SLOTS.get(pose, []):
            _item = store._at_outfit_items.get(_slot)
            _pose_map = _reg.get(_item, {}).get("poses", {}).get(pose) if _item else None
            if _pose_map is None or (_slot == "chest" and _hides):
                continue
            _rows.append((_slot, _item, [_st for _st in _reg[_item].get("states", ["full"]) if _st in _pose_map] + ["off"]))
        return _rows

    def _at_slot_state(girl, slot):
        return girl.clothes_state.get(slot, "full") if girl.clothes.get(slot) else "off"

    def _at_option_choices(girl, pose):
        _choices = [
            (_tl_fmt(_("Pregnancy stage: %s"), _tl(_AT_PREG_STAGES[preg_vstage(girl.gid)])), ("preg", None)),
            (_tl_fmt(_("Outfit: %s"), store._at_outfit_name), ("outfit", None)),
        ]
        for _slot, _item, _states in (_at_state_rows(girl, pose) if pose else []):
            _choices.append(("%s (%s): %s" % (_slot, _item, _at_slot_state(girl, _slot)), ("state", _slot)))
        _choices.append((_tl(_("Piercings: on") if getattr(girl, "Piercing", False) else _("Piercings: off")), ("piercing", None)))
        _choices.append((_tl(_("Back")), "back"))
        return _choices

    def _at_opt_preg(girl, pose, slot):
        preg_art_preview(girl, (preg_vstage(girl.gid) + 1) % len(_AT_PREG_STAGES))

    def _at_opt_outfit(girl, pose, slot):
        _list = _at_outfits_for(girl, pose)
        _i = _list.index(store._at_outfit_name) if store._at_outfit_name in _list else -1
        store._at_outfit_name = _list[(_i + 1) % len(_list)]
        store._at_tweaks = {}               # new outfit, new garments: the slot choices start over
        _at_dress(girl, pose)

    def _at_opt_state(girl, pose, slot):
        _row = [_r for _r in _at_state_rows(girl, pose) if _r[0] == slot]
        if not _row:
            return
        _item, _states = _row[0][1], _row[0][2]
        _cur = _at_slot_state(girl, slot)
        _new = _states[(_states.index(_cur) + 1) % len(_states)] if _cur in _states else _states[0]
        girl.clothes[slot] = None if _new == "off" else _item
        girl.clothes_state[slot] = "full" if _new == "off" else _new
        store._at_tweaks[slot] = _new

    def _at_opt_piercing(girl, pose, slot):
        girl.Piercing = not getattr(girl, "Piercing", False)

    _AT_OPTION_HANDLERS = {"preg": _at_opt_preg, "outfit": _at_opt_outfit, "state": _at_opt_state, "piercing": _at_opt_piercing}

    def _at_option_apply(girl, pose, pick):
        _AT_OPTION_HANDLERS[pick[0]](girl, pose, pick[1])
        print("[ART_TEST] %s pose=%s option=%s -> preg=%d outfit=%s clothes=%s states=%s piercing=%s" % (
            girl.gid, pose, pick, preg_vstage(girl.gid), store._at_outfit_name, girl.clothes, girl.clothes_state, getattr(girl, "Piercing", False)))

    def _at_scene_on_screen():
        """A tester scene is up (a girl picked, a scene running): every menu over it (screen choice) shows HIDE MENU.
        Both, because the console fn_test leaves _at_pose set behind it."""
        return getattr(store, "_at_girl", None) is not None and getattr(store, "_at_pose", None) is not None

    def _at_hide_menu():
        """HIDE MENU: the scene alone until a click brings the menu back. Ren'Py's own hide interface, the same as
        the H key / middle click; the scene keeps moving under it."""
        print("[ART_TEST] HIDE MENU %s pose=%s: menu back on a click" % (getattr(store._at_girl, "gid", None), store._at_pose))
        HideInterface()()

# tester state. Defaults, so a tester label entered directly (console `fn_test`) finds it.
default _at_girl = None
default _at_pose = None
default _at_outfit_name = "casual"
default _at_outfit_items = {}
default _at_tweaks = {}
default _at_speed = 0
default _at_arm = 1
default _at_dg_mode = "vaginal"
default _at_rcg_mode = "vaginal"

label art_test:
    python:
        _kill_scene_threads()
        _clear_scene_refs()
        store.doggy_started = False
        store.doggy_anal = False
        store.cowgirl_started = False
        store.cowgirl_masturbating = False
        store.CurrentLocation = "room"
        store._player_exposed_this_session = True
        store._crowd_level = 0
        store.condom_active = False
        store._recording_active = False
        store._at_pose = None               # F9 pressed in a scene left it set: no scene up, no HIDE MENU on the girl list
        _at_restore_all()

    scene black

    python:
        _at_pick = renpy.display_menu(
            [("!section!" + _tl(_("--- ART TEST --- (Shift+R reloads images)")), None)]
            + [(_g.Name, _g.gid) for _g in ALL_GIRLS]
            + [("!section!" + _tl(_("--- STANDALONE TESTS ---")), None)]
            + [(_tl(_("New Rogue (Sprite Test)")), "new_rogue")]
            + [(_tl(_("Exit")), "exit")])
    if _at_pick == "exit":
        $ _at_girl = None
        return
    if _at_pick == "new_rogue":
        call _at_rogue_new from _at_c_rogue_new
        jump art_test
    python:
        _at_girl = GIRL_BY_ID[_at_pick]
        _at_snapshot(_at_girl)
        _at_outfit_name = "casual"
        _at_tweaks = {}
        _at_pose = None
        _at_dress(_at_girl)
        _at_girl.loc = store.CurrentLocation

label _at_scene_menu:
    python:
        _at_scenes = [_s for _s in _AT_SCENES if renpy.has_image("%s %s" % (_at_girl.gid, _s[1]), exact=True)]
        _at_pick = renpy.display_menu(
            [(_tl(_s[0]), _i) for _i, _s in enumerate(_at_scenes)]
            + [(_tl(_("Pregnancy / clothes...")), "options"), (_tl(_("GIF Layer Test")), "gif_test"), (_tl(_("Change Character")), "girl")])
    if _at_pick == "girl":
        jump art_test
    if _at_pick == "options":
        call _at_options(_at_girl, None, None) from _at_c_opt_menu
        jump _at_scene_menu
    if _at_pick == "gif_test":
        call _at_gif_layer_test from _at_c_gif_test
        scene black
        jump _at_scene_menu

    python:
        _at_scene = _at_scenes[_at_pick]
        _at_pose = _at_scene[2]
        for _at_flag, _at_value in _at_scene[4].items():
            setattr(store, _at_flag, _at_value)
        # a scene launch may strip her: every scene starts from the chosen outfit + the tester's slot choices
        _at_dress(_at_girl, _at_pose)
    call expression _at_scene[3] pass (_at_girl) from _at_c_scene

    python:
        _at_pose = None
        _kill_scene_threads()
        _clear_scene_refs()
        store.doggy_started = False
        store.cowgirl_started = False
        store.cowgirl_masturbating = False
    scene black
    jump _at_scene_menu

# ── Options (shared by every scene) ───────────────────────
# pose = clothing pose of the scene (CLOTHING_REGISTRY key), refresh = label that redraws it with (girl, speed).
# Both None from the scene menu: no clothing states there, nothing on screen to redraw.

label _at_options(girl, pose, refresh):
    while True:
        $ _at_opt_pick = renpy.display_menu(_at_option_choices(girl, pose))
        if _at_opt_pick == "back":
            return
        $ _at_option_apply(girl, pose, _at_opt_pick)
        if refresh:
            call expression refresh pass (girl, _at_speed) from _at_c_opt_refresh

# ── Standing ──────────────────────────────────────────────

label _at_standing_refresh(girl, speed=0):
    $ _at_show_standing(girl, _at_arm)
    return

label _at_standing(girl):
    scene black
    $ _at_speed = 0
    $ _at_arm = 1
    $ _at_show_standing(girl, _at_arm)
    while True:
        menu:
            "Arms 1" if _at_arm != 1:
                $ _at_arm = 1
            "Arms 2" if _at_arm != 2:
                $ _at_arm = 2
            "Arms 3" if _at_arm != 3:
                $ _at_arm = 3
            "Arms 4" if _at_arm != 4:
                $ _at_arm = 4
            "Pregnancy / clothes...":
                call _at_options(girl, _at_pose, "_at_standing_refresh") from _at_c_st_opt
            "Back":
                $ hide_girl_sprite(girl)
                return
        $ _at_show_standing(girl, _at_arm)

# ── Handjob ───────────────────────────────────────────────

# The player's skin (Player.skin: every _p() image, the slap hands included) flipped for the test and put back on Back
label _at_toggle_skin:
    $ Player.skin = "Black" if getattr(Player, "skin", "White") == "White" else "White"
    $ renpy.notify("Player skin: %s" % Player.skin)
    return

label _at_hj(girl):
    scene black
    $ _at_skin0 = getattr(Player, "skin", "White")
    call HJ_Launch(girl) from _at_c_hj_l
    $ _at_speed = 0
    while True:
        menu:
            "Speed 0" if _at_speed != 0:
                $ _at_speed = 0
                call HJ_ApplySpeed(girl, 0) from _at_c_hj_s0
            "Speed 1" if _at_speed != 1:
                $ _at_speed = 1
                call HJ_ApplySpeed(girl, 1) from _at_c_hj_s1
            "Speed 2" if _at_speed != 2:
                $ _at_speed = 2
                call HJ_ApplySpeed(girl, 2) from _at_c_hj_s2
            "Speed 3" if _at_speed != 3:
                $ _at_speed = 3
                call HJ_ApplySpeed(girl, 3) from _at_c_hj_s3
            "Slap her (the real slap: her face, a moan, +1 Obed / Inbt)":
                call SexScene_Slap(girl, "hj") from _at_c_hj_slap
            "Player skin: [Player.skin]":
                call _at_toggle_skin from _at_c_hj_skin
                call HJ_ApplySpeed(girl, _at_speed) from _at_c_hj_skin_apply
            "Pregnancy / clothes...":
                call _at_options(girl, _at_pose, "HJ_ApplySpeed") from _at_c_hj_opt
            "Back":
                $ Player.skin = _at_skin0
                return

# ── Blowjob ──────────────────────────────────────────────

label _at_bj(girl):
    scene black
    $ _at_skin0 = getattr(Player, "skin", "White")
    call BJ_Launch(girl) from _at_c_bj_l
    $ _at_speed = 0
    while True:
        menu:
            "Speed 0 (Lick)" if _at_speed != 0:
                $ _at_speed = 0
                $ store.bj_action = "lick"
                call BJ_ApplySpeed(girl, 0) from _at_c_bj_s0
            "Speed 1 (Suck)" if _at_speed != 1:
                $ _at_speed = 1
                $ store.bj_action = "suck"
                call BJ_ApplySpeed(girl, 1) from _at_c_bj_s1
            "Speed 2 (Suck)" if _at_speed != 2:
                $ _at_speed = 2
                $ store.bj_action = "suck"
                call BJ_ApplySpeed(girl, 2) from _at_c_bj_s2
            "Speed 3 (Suck)" if _at_speed != 3:
                $ _at_speed = 3
                $ store.bj_action = "suck"
                call BJ_ApplySpeed(girl, 3) from _at_c_bj_s3
            "Slap her (the real slap: her face, a moan, +1 Obed / Inbt)":
                call SexScene_Slap(girl, "bj") from _at_c_bj_slap
            "Player skin: [Player.skin]":
                call _at_toggle_skin from _at_c_bj_skin
                call BJ_ApplySpeed(girl, _at_speed) from _at_c_bj_skin_apply
            "Pregnancy / clothes...":
                call _at_options(girl, _at_pose, "BJ_ApplySpeed") from _at_c_bj_opt
            "Back":
                $ Player.skin = _at_skin0
                return

# ── Titjob ───────────────────────────────────────────────

label _at_tj(girl):
    scene black
    $ _at_skin0 = getattr(Player, "skin", "White")
    call TITJOB_Launch(girl) from _at_c_tj_l
    $ _at_speed = 0
    $ _at_arms = 1
    while True:
        menu:
            "Speed 0" if _at_speed != 0:
                $ _at_speed = 0
                call TITJOB_ApplySpeed(girl, 0) from _at_c_tj_s0
            "Speed 1" if _at_speed != 1:
                $ _at_speed = 1
                call TITJOB_ApplySpeed(girl, 1) from _at_c_tj_s1
            "Speed 2" if _at_speed != 2:
                $ _at_speed = 2
                call TITJOB_ApplySpeed(girl, 2) from _at_c_tj_s2
            "Speed 3" if _at_speed != 3:
                $ _at_speed = 3
                call TITJOB_ApplySpeed(girl, 3) from _at_c_tj_s3
            "Arms 1" if _at_arms != 1:
                $ _at_arms = 1
                $ store.titjob_arms_pose = 1
                call TITJOB_ApplySpeed(girl, _at_speed) from _at_c_tj_a1
            "Arms 2" if _at_arms != 2:
                $ _at_arms = 2
                $ store.titjob_arms_pose = 2
                call TITJOB_ApplySpeed(girl, _at_speed) from _at_c_tj_a2
            "Arms 3" if _at_arms != 3:
                $ _at_arms = 3
                $ store.titjob_arms_pose = 3
                call TITJOB_ApplySpeed(girl, _at_speed) from _at_c_tj_a3
            "Grab Toggle":
                $ store.titjob_grab = not store.titjob_grab
                call TITJOB_ApplySpeed(girl, _at_speed) from _at_c_tj_grab
            "Slap her (the real slap: her face, a moan, +1 Obed / Inbt)":
                call SexScene_Slap(girl, "tj") from _at_c_tj_slap
            "Player skin: [Player.skin]":
                call _at_toggle_skin from _at_c_tj_skin
                call TITJOB_ApplySpeed(girl, _at_speed) from _at_c_tj_skin_apply
            "Pregnancy / clothes...":
                call _at_options(girl, _at_pose, "TITJOB_ApplySpeed") from _at_c_tj_opt
            "Back":
                $ Player.skin = _at_skin0
                return

# ── Cowgirl ──────────────────────────────────────────────

label _at_cg(girl):
    scene black
    call COWGIRL_Launch(girl) from _at_c_cg_l
    $ store.cowgirl_started = True
    $ _at_speed = 1
    call COWGIRL_ApplySpeed(girl, 1) from _at_c_cg_si
    while True:
        menu:
            "Speed 0 (Idle)" if _at_speed != 0:
                $ _at_speed = 0
                $ store.cowgirl_started = False
                call COWGIRL_ApplySpeed(girl, 0) from _at_c_cg_s0
            "Speed 1" if _at_speed != 1:
                $ _at_speed = 1
                $ store.cowgirl_started = True
                call COWGIRL_ApplySpeed(girl, 1) from _at_c_cg_s1
            "Speed 2" if _at_speed != 2:
                $ _at_speed = 2
                $ store.cowgirl_started = True
                call COWGIRL_ApplySpeed(girl, 2) from _at_c_cg_s2
            "Speed 3" if _at_speed != 3:
                $ _at_speed = 3
                $ store.cowgirl_started = True
                call COWGIRL_ApplySpeed(girl, 3) from _at_c_cg_s3
            "Pregnancy / clothes...":
                call _at_options(girl, _at_pose, "COWGIRL_ApplySpeed") from _at_c_cg_opt
            "Back":
                return

# ── Reverse Cowgirl ──────────────────────────────────────

label _at_rcg(girl):
    scene black
    call RCG_Launch(girl) from _at_c_rcg_l
    $ store.rcg_started = True
    $ _at_speed = 1
    call RCG_ApplySpeed(girl, 1) from _at_c_rcg_si
    while True:
        menu:
            "Speed 0 (Idle)" if _at_speed != 0:
                $ _at_speed = 0
                call RCG_ApplySpeed(girl, 0) from _at_c_rcg_s0
            "Speed 1" if _at_speed != 1:
                $ _at_speed = 1
                call RCG_ApplySpeed(girl, 1) from _at_c_rcg_s1
            "Speed 2" if _at_speed != 2:
                $ _at_speed = 2
                call RCG_ApplySpeed(girl, 2) from _at_c_rcg_s2
            "Speed 3" if _at_speed != 3:
                $ _at_speed = 3
                call RCG_ApplySpeed(girl, 3) from _at_c_rcg_s3
            "Pregnancy / clothes...":
                call _at_options(girl, _at_pose, "RCG_ApplySpeed") from _at_c_rcg_opt
            "Back":
                return

# ── Doggy ────────────────────────────────────────────────

label _at_dg(girl):
    scene black
    call DG_Launch(girl) from _at_c_dg_l
    $ store.doggy_started = True
    $ _at_speed = 1
    call DG_ApplySpeed(girl, 1) from _at_c_dg_si
    while True:
        menu:
            "Speed 0 (Preview)" if _at_speed != 0:
                $ _at_speed = 0
                $ store.doggy_started = False
                call DG_ApplySpeed(girl, 0) from _at_c_dg_s0
            "Speed 1" if _at_speed != 1:
                $ _at_speed = 1
                $ store.doggy_started = True
                call DG_ApplySpeed(girl, 1) from _at_c_dg_s1
            "Speed 2" if _at_speed != 2:
                $ _at_speed = 2
                $ store.doggy_started = True
                call DG_ApplySpeed(girl, 2) from _at_c_dg_s2
            "Speed 3" if _at_speed != 3:
                $ _at_speed = 3
                $ store.doggy_started = True
                call DG_ApplySpeed(girl, 3) from _at_c_dg_s3
            "Pregnancy / clothes...":
                call _at_options(girl, _at_pose, "DG_ApplySpeed") from _at_c_dg_opt
            "Back":
                return

# ── Full Nelson ──────────────────────────────────────────
# Set up by hand instead of FN_Launch: no bottom-clothes dialogue, no exposure check, any girl with the pose.
# Also what the console entry `fn_test` (Core_FullNelson.rpy) runs.

label _at_fn(girl):
    scene black
    python:
        _kill_scene_threads()
        _hide_all_scene_layers()
        _clear_scene_refs("fn")
        store._fn_girl = girl
        store.fn_speed = 0
        store.fn_started = False
        store.fn_anal = False
        sprite_state.setdefault(girl.Id, {})["pose"] = "full_nelson"
        _at_speed = 0

    call FN_ApplySpeed(girl, 0) from _at_c_fn_init
    with dissolve

    $ renpy.invoke_in_thread(_scene_blink_loop, girl, "_fn_girl", "fn_blink", is_active_fn=_fn_is_active, cs_girls={"ntw", "tenny"}, blink_timing=(0.12, 0.22))
    $ renpy.invoke_in_thread(_fn_expression_cycle, girl)

    while True:
        menu:
            "Speed 0 (Idle)" if _at_speed != 0:
                $ _at_speed = 0
                $ store.fn_started = False
            "Speed 1 (Slow)" if _at_speed != 1:
                $ _at_speed = 1
                $ store.fn_started = True
            "Speed 2 (Standard)" if _at_speed != 2:
                $ _at_speed = 2
                $ store.fn_started = True
            "Speed 3 (Fast)" if _at_speed != 3:
                $ _at_speed = 3
                $ store.fn_started = True
            "Speed 4 (Cumming)" if store.fn_started and _at_speed != 4:
                $ _at_speed = 4
            "Toggle Anal / Vaginal":
                $ store.fn_anal = not store.fn_anal
                $ renpy.notify("Mode: %s" % ("ANAL" if store.fn_anal else "VAGINAL"))
            "Toggle Condom":
                $ store.condom_active = not store.condom_active
                $ store._condom_broken = False
                $ renpy.notify("Condom: %s" % ("ON" if store.condom_active else "OFF"))
            "Toggle Broken Condom" if store.condom_active:
                $ store._condom_broken = not store._condom_broken
                $ renpy.notify("Condom: %s" % ("BROKEN" if store._condom_broken else "INTACT"))
            "Pregnancy / clothes...":
                call _at_options(girl, _at_pose, "FN_ApplySpeed") from _at_c_fn_opt
            "Back":
                python:
                    store._fn_girl = None
                    store.condom_active = False
                    store._condom_broken = False
                    _fn_hide_all()
                    renpy.hide(girl.gid)
                return
        $ store.fn_speed = _at_speed
        $ debug_log("[ART_TEST] FN %s speed=%d anal=%s condom=%s" % (girl.gid, _at_speed, store.fn_anal, store.condom_active))
        call FN_ApplySpeed(girl, _at_speed) from _at_c_fn_apply

# ── Footjob ─────────────────────────────────────────────────
# GIF-frame animation with player clothing/skin variants.
# Tenny-exclusive. No clothing integration yet -- nude body only.

label _at_ft(girl):
    scene black
    python:
        import time as _time
        store._ft_girl = girl
        store._ft_speed = 0
        store._ft_phase = "move"
        store._ft_player_clothing = "Legs"
        store._ft_player_skin = "White"
        store._ft_move_t0 = _time.time()
        store._ft_phase_t0 = None
        sprite_state.setdefault(girl.Id, {})["pose"] = "footjob"
        _at_speed = 0
        _ft_show_anim(0)
        _ft_show_layers()

    while True:
        menu:
            "Speed 0 (Idle)" if _at_speed != 0:
                $ _at_speed = 0
                $ store._ft_phase = "move"
                call FT_ApplySpeed(girl, 0) from _at_c_ft_s0
            "Speed 1" if _at_speed != 1 and store._ft_phase == "move":
                $ _at_speed = 1
                call FT_ApplySpeed(girl, 1) from _at_c_ft_s1
            "Speed 2" if _at_speed != 2 and store._ft_phase == "move":
                $ _at_speed = 2
                call FT_ApplySpeed(girl, 2) from _at_c_ft_s2
            "Speed 3" if _at_speed != 3 and store._ft_phase == "move":
                $ _at_speed = 3
                call FT_ApplySpeed(girl, 3) from _at_c_ft_s3
            "Before Cum -> Cum" if store._ft_phase == "move" and _at_speed > 0:
                python:
                    import time as _time
                    store._ft_phase = "before_cum"
                    store._ft_phase_t0 = _time.time()
                    _ft_show_anim()
                    _bc_dur = _ft_before_cum_duration()
                    renpy.pause(_bc_dur, hard=True)
                    store._ft_phase = "cum"
                    store._ft_phase_t0 = _time.time()
                    _ft_show_anim()
            "Reset to Movement" if store._ft_phase != "move":
                $ _at_speed = 1
                $ store._ft_phase = "move"
                call FT_ApplySpeed(girl, 1) from _at_c_ft_reset
            "Player Clothing: [_ft_player_clothing]":
                python:
                    import time as _time
                    _idx = _FT_CLOTHING_VARIANTS.index(store._ft_player_clothing)
                    store._ft_player_clothing = _FT_CLOTHING_VARIANTS[(_idx + 1) % len(_FT_CLOTHING_VARIANTS)]
                    store._ft_move_t0 = _time.time()
                    _ft_show_anim()
                    renpy.notify("Clothing: %s" % store._ft_player_clothing)
            "Player Skin: [_ft_player_skin]":
                python:
                    import time as _time
                    _idx = _FT_SKIN_VARIANTS.index(store._ft_player_skin)
                    store._ft_player_skin = _FT_SKIN_VARIANTS[(_idx + 1) % len(_FT_SKIN_VARIANTS)]
                    store._ft_move_t0 = _time.time()
                    _ft_show_anim()
                    renpy.notify("Skin: %s" % store._ft_player_skin)
            "Toggle Piercings":
                python:
                    girl.Piercing = not getattr(girl, "Piercing", False)
                    _ft_show_layers()
                    renpy.notify("Piercings: %s" % ("ON" if girl.Piercing else "OFF"))
            "Back":
                python:
                    store._ft_girl = None
                    _ft_hide_all()
                return
        $ debug_log("[ART_TEST] FT speed=%d phase=%s clothing=%s skin=%s" % (_at_speed, store._ft_phase, store._ft_player_clothing, store._ft_player_skin))

# ── Shion Cowgirl (custom layers) ───────────────────────────

label _at_shion_cg_refresh(girl, speed=0):
    $ _scg_apply_speed(girl, store._at_speed)
    return

# Her layers ride the standard cowgirl clock: the speed is store.cowgirl_speed and the clock starts at
# _cg_anim_origin, set here the way COWGIRL_ApplySpeed sets them in the real scene.
label _at_shion_cg_speed(girl, speed):
    python:
        store._at_speed = speed
        store.cowgirl_started = speed >= 1
        store.cowgirl_speed = speed
        store._cg_force_static = False
        store._cg_anim_origin = _time.time()
        _scg_apply_speed(girl, speed)
    return

label _at_shion_cg(girl):
    scene black
    python:
        store._scg_girl = girl
        store._cowgirl_girl = girl
        sprite_state.setdefault(girl.Id, {})["pose"] = "cowgirl"
        store._scg_arms_variant = 1
        store.condom_active = False
    call _at_shion_cg_speed(girl, 0) from _call_at_shion_cg_speed_0

    while True:
        menu:
            "Speed 0 (Idle)" if _at_speed != 0:
                call _at_shion_cg_speed(girl, 0) from _call_at_shion_cg_speed_idle
            "Speed 1" if _at_speed != 1:
                call _at_shion_cg_speed(girl, 1) from _call_at_shion_cg_speed_1
            "Speed 2" if _at_speed != 2:
                call _at_shion_cg_speed(girl, 2) from _call_at_shion_cg_speed_2
            "Speed 3" if _at_speed != 3:
                call _at_shion_cg_speed(girl, 3) from _call_at_shion_cg_speed_3
            "Arms 1" if store._scg_arms_variant != 1:
                $ _scg_set_arms(1)
            "Arms 2" if store._scg_arms_variant != 2:
                $ _scg_set_arms(2)
            "Arms Left" if store._scg_arms_variant != "left":
                $ _scg_set_arms("left")
            "Arm Right" if store._scg_arms_variant != "right":
                $ _scg_set_arms("right")
            "Toggle Piercings":
                python:
                    girl.Piercing = not getattr(girl, "Piercing", False)
                    _scg_apply_speed(girl, _at_speed)
                    renpy.notify("Piercings: %s" % ("ON" if girl.Piercing else "OFF"))
            "Toggle Condom":
                python:
                    store.condom_active = not store.condom_active
                    _scg_apply_speed(girl, _at_speed)
                    renpy.notify("Condom: %s" % ("ON" if store.condom_active else "OFF"))
            "Pregnancy / clothes...":
                call _at_options(girl, _at_pose, "_at_shion_cg_refresh") from _at_c_scg_opt
            "Back":
                python:
                    store._scg_girl = None
                    store.cowgirl_started = False
                    _scg_hide_all()
                return

# ── Shion Reverse Cowgirl (custom layers) ───────────────────

label _at_shion_rcg_refresh(girl, speed=0):
    $ _srcg_apply_speed(girl, store._at_speed)
    return

# Her RCG test: the speed is the whole state. 0 = she hovers over him (dressed as she is, the penis out), 1 = the
# tip / slow ride, 2, 3 = faster; the layers never draw clothes once he is in (started), like in play. The pussy
# opens around him on its own; "had anal this session" = Butt Bottom 3 (her anus gapes).
#   Mode vaginal / anal = the hole (anal: the penis over every layer of hers under the mask, Butt Top 2, over the
#   gaping Butt Bottom 3). Hold = his hands on her thighs (store.rcg_hold): she rides the lower half of her stroke.
label _at_shion_rcg_apply(girl, speed):
    python:
        store._at_speed = speed
        store.rcg_started = speed >= 1
        store.rcg_anal = (store._at_rcg_mode == "anal")
        _srcg_apply_speed(girl, speed)
    return

label _at_shion_rcg(girl):
    scene black
    $ _at_skin0 = getattr(Player, "skin", "White")
    python:
        store._srcg_girl = girl
        store._rcg_girl = girl
        sprite_state.setdefault(girl.Id, {})["pose"] = "reverse_cowgirl"
        store._dg_had_anal = False
        store._rcg_had_anal = False
        store._at_rcg_mode = "vaginal"
        store.rcg_anal = False
        store.rcg_hold = False
    call _at_shion_rcg_apply(girl, 0) from _call_at_shion_rcg_apply_0

    while True:
        python:
            _at_rcg_next = "anal" if store._at_rcg_mode == "vaginal" else "vaginal"
            _srcg_hold_lbl = "ON" if getattr(store, "rcg_hold", False) else "OFF"
            _srcg_had_a_lbl = "ON" if getattr(store, "_dg_had_anal", False) else "OFF"
            _srcg_pierce_lbl = "ON" if getattr(girl, "Piercing", False) else "OFF"
        menu:
            "Mode: [_at_rcg_mode]   (next: [_at_rcg_next])":
                $ store._at_rcg_mode = _at_rcg_next
                call _at_shion_rcg_apply(girl, _at_speed) from _call_at_shion_rcg_apply_mode
            "Speed 0 (above him, dressed as she is)" if _at_speed != 0:
                call _at_shion_rcg_apply(girl, 0) from _call_at_shion_rcg_apply_idle
            "Speed 1 (the tip / slow ride, naked)" if _at_speed != 1:
                call _at_shion_rcg_apply(girl, 1) from _call_at_shion_rcg_apply_1
            "Speed 2" if _at_speed != 2:
                call _at_shion_rcg_apply(girl, 2) from _call_at_shion_rcg_apply_2
            "Speed 3 (fast)" if _at_speed != 3:
                call _at_shion_rcg_apply(girl, 3) from _call_at_shion_rcg_apply_3
            "Hold her down (his hands on her thighs, half the stroke): [_srcg_hold_lbl]":
                $ store.rcg_hold = not getattr(store, "rcg_hold", False)
                $ _srcg_apply_speed(girl, _at_speed)
            "Had anal this session (anus gapes, Butt Bottom 3): [_srcg_had_a_lbl]":
                $ store._dg_had_anal = not getattr(store, "_dg_had_anal", False)
                $ _srcg_apply_speed(girl, _at_speed)
            "Piercings: [_srcg_pierce_lbl]   (switch)":
                python:
                    girl.Piercing = not getattr(girl, "Piercing", False)
                    _srcg_apply_speed(girl, _at_speed)
            "Player skin: [Player.skin]   (switch)":
                call _at_toggle_skin from _at_c_srcg_skin
                $ _srcg_apply_speed(girl, _at_speed)
            "Pregnancy / clothes...":
                call _at_options(girl, _at_pose, "_at_shion_rcg_refresh") from _at_c_srcg_opt
            "Back":
                python:
                    store._srcg_girl = None
                    store.rcg_started = False
                    store.rcg_anal = False
                    store.rcg_hold = False
                    store._dg_had_anal = False
                    store._rcg_had_anal = False
                    Player.skin = _at_skin0
                    _srcg_hide_all()
                return

# ── Shion Doggy (custom layers) ─────────────────────────────

label _at_shion_dg_refresh(girl, speed=0):
    $ _sdg_apply_speed(girl, store._at_speed)
    return

# Her doggy test: ONE mode drives everything (his pair, the hole, her hand), the speed is his thrust (or her hand);
# the "After" patches come from the session-history flags, like in play.
#   vaginal / anal   = the penetration (speed 0 = the preview before he goes in; no clothes once he is inside)
#   anal_touch       = anal with her hand on herself (he is inside at every speed; the "Tell her to touch herself" of play)
#   thighjob         = the rub (his penis between her thighs, under the near thigh; no pants)
#   masturbation     = her solo scene (her hand, nothing of his; dressed = the hand over the clothes)
label _at_shion_dg_apply(girl, speed):
    python:
        store._at_speed = speed
        _m = store._at_dg_mode
        store.doggy_anal = _m in ("anal", "anal_touch")
        store.doggy_rub_mode = (_m == "thighjob")
        store._dg_masturbating = _m in ("masturbation", "anal_touch")
        store.doggy_started = (_m == "anal_touch") or (speed >= 1 and _m in ("vaginal", "anal"))
        # each test shot as play draws it fresh: his layers only once he started (_sdg_apply_speed latches it), in her
        store._sdg_guy_on = False
        store._sdg_penis_out = None
        _sdg_apply_speed(girl, speed)
    return

label _at_shion_dg(girl):
    scene black
    $ _at_skin0 = getattr(Player, "skin", "White")
    python:
        store._sdg_girl = girl
        store._doggy_girl = girl
        sprite_state.setdefault(girl.Id, {})["pose"] = "doggy"
        store._sdg_butt_state = "closed"
        store._sdg_head_pos = 2
        store._at_dg_mode = "vaginal"
        store._dg_had_pussy = False
        store._dg_had_anal = False
    call _at_shion_dg_apply(girl, 0) from _call_at_shion_dg_apply_0

    while True:
        python:
            _at_dg_modes = ["vaginal", "anal", "anal_touch", "thighjob", "masturbation"]
            _at_dg_next = _at_dg_modes[(_at_dg_modes.index(store._at_dg_mode) + 1) % len(_at_dg_modes)]
            _sdg_had_p_lbl = "ON" if getattr(store, "_dg_had_pussy", False) else "OFF"
            _sdg_had_a_lbl = "ON" if getattr(store, "_dg_had_anal", False) else "OFF"
            _sdg_head_lbl = "2, her face" if store._sdg_head_pos == 2 else "1, from behind"
        menu:
            "Mode: [_at_dg_mode]   (next: [_at_dg_next])":
                $ store._at_dg_mode = _at_dg_next
                call _at_shion_dg_apply(girl, _at_speed) from _call_at_shion_dg_apply_mode
            "Speed 0 (still)" if _at_speed != 0:
                call _at_shion_dg_apply(girl, 0) from _call_at_shion_dg_apply_idle
            "Speed 1 (slow)" if _at_speed != 1:
                call _at_shion_dg_apply(girl, 1) from _call_at_shion_dg_apply_1
            "Speed 2" if _at_speed != 2:
                call _at_shion_dg_apply(girl, 2) from _call_at_shion_dg_apply_2
            "Speed 3 (fast)" if _at_speed != 3:
                call _at_shion_dg_apply(girl, 3) from _call_at_shion_dg_apply_3
            "After patch, vaginal (had vaginal this session): [_sdg_had_p_lbl]":
                $ store._dg_had_pussy = not getattr(store, "_dg_had_pussy", False)
                $ _sdg_apply_speed(girl, _at_speed)
            "After patch, anal (had anal this session): [_sdg_had_a_lbl]":
                $ store._dg_had_anal = not getattr(store, "_dg_had_anal", False)
                $ _sdg_apply_speed(girl, _at_speed)
            "Head: [_sdg_head_lbl]   (switch)":
                $ _sdg_switch_head(1 if store._sdg_head_pos == 2 else 2)
            "Player skin: [Player.skin]   (switch)":
                call _at_toggle_skin from _at_c_sdg_skin
                $ _sdg_apply_speed(girl, _at_speed)
            "Pregnancy / clothes...":
                call _at_options(girl, _at_pose, "_at_shion_dg_refresh") from _at_c_sdg_opt
            "Back":
                python:
                    store._sdg_girl = None
                    store.doggy_started = False
                    store.doggy_anal = False
                    store.doggy_rub_mode = False
                    store._dg_masturbating = False
                    store._dg_had_pussy = False
                    store._dg_had_anal = False
                    Player.skin = _at_skin0
                    _sdg_hide_all()
                return

# ── Rimjob (new pose, custom layers) ───────────────────────

label _at_rimjob_refresh(girl, speed=0):
    $ _rj_apply_speed(girl, store._rj_speed)
    return

label _at_rimjob(girl):
    scene black
    python:
        store._rj_girl = girl
        sprite_state.setdefault(girl.Id, {})["pose"] = "rimjob"
        store._rj_head_pos = 1
        store._rj_speed = 0
        store._at_speed = 0
        _rj_apply_speed(girl, 0)

    while True:
        menu:
            "Speed 0 (Static)" if _at_speed != 0:
                python:
                    store._at_speed = 0
                    _rj_apply_speed(girl, 0)
            "Speed 1" if _at_speed != 1:
                python:
                    store._at_speed = 1
                    _rj_apply_speed(girl, 1)
            "Speed 2" if _at_speed != 2:
                python:
                    store._at_speed = 2
                    _rj_apply_speed(girl, 2)
            "Speed 3" if _at_speed != 3:
                python:
                    store._at_speed = 3
                    _rj_apply_speed(girl, 3)
            "Head Position 1" if store._rj_head_pos != 1:
                $ _rj_switch_head(1)
                $ renpy.notify("Head: Position 1")
            "Head Position 2" if store._rj_head_pos != 2:
                $ _rj_switch_head(2)
                $ renpy.notify("Head: Position 2")
            "Pregnancy / clothes...":
                call _at_options(girl, _at_pose, "_at_rimjob_refresh") from _at_c_rj_opt
            "Back":
                python:
                    store._rj_girl = None
                    store._rj_speed = 0
                    _rj_hide_all()
                return

# ============================================================
# Transform Tuner — press F12 during BJ/HJ to adjust live
# Reads/writes _bj_pov_* and _hj_pov_* variables directly.
# "Play" re-applies using the REAL transforms from Core files.
# ============================================================

init python:
    store._tune_visible = False
    store._tune_mode = "arm_right"
    store._tune_last = None
    store._tune_playing = False
    store._tune_speed = 1

    store._tune_head_peak = 285
    store._tune_head_base = 145
    store._tune_body_yoff = 0

    def _tune_toggle():
        store._tune_visible = not store._tune_visible
        store._tune_last = None
        store._tune_playing = False
        if store._tune_visible:
            if getattr(store, '_bj_girl', None) is not None:
                store._tune_speed = getattr(store, 'bj_speed', 1)
            elif getattr(store, '_hj_girl', None) is not None:
                store._tune_speed = getattr(store, 'hj_speed', 1)
            _tune_force_apply()
        renpy.restart_interaction()

    def _tune_set_speed(spd):
        store._tune_speed = spd
        if getattr(store, '_bj_girl', None) is not None:
            store.bj_speed = spd
        elif getattr(store, '_hj_girl', None) is not None:
            store.hj_speed = spd
        store._tune_last = None
        _tune_force_apply()

    def _tune_play():
        store._tune_playing = True
        store._tune_last = None
        _tune_force_apply()

    def _tune_stop():
        store._tune_playing = False
        store._tune_last = None
        _tune_force_apply()

    def _tune_force_apply():
        girl = getattr(store, '_bj_girl', None) or getattr(store, '_hj_girl', None)
        if not girl:
            return
        gid = girl.gid
        is_bj = getattr(store, '_bj_girl', None) is not None
        speed = store._tune_speed
        if store._tune_playing:
            _tune_reapply_scene(gid, is_bj, speed)
        else:
            _tune_apply_static(gid, is_bj, speed)
        renpy.restart_interaction()

    def _tune_apply():
        if not store._tune_visible:
            return
        girl = getattr(store, '_bj_girl', None) or getattr(store, '_hj_girl', None)
        if not girl:
            return

        gid = girl.gid
        is_bj = getattr(store, '_bj_girl', None) is not None
        speed = store._tune_speed

        if is_bj:
            cur = (store._tune_playing, speed,
                   store._bj_pov_ar_ax, store._bj_pov_ar_ay,
                   store._bj_pov_ar_start, store._bj_pov_ar_end,
                   store._bj_pov_al_ax, store._bj_pov_al_ay,
                   store._bj_pov_al_start, store._bj_pov_al_end,
                   store._bj_pov_hand_static_y,
                   store._bj_pov_hand_start, store._bj_pov_hand_end,
                   store._tune_head_peak, store._tune_head_base,
                   store._tune_body_yoff)
        else:
            cur = (store._tune_playing, speed,
                   store._hj_pov_ar_ax, store._hj_pov_ar_ay,
                   store._hj_pov_ar_start, store._hj_pov_ar_end,
                   store._hj_pov_al_ax, store._hj_pov_al_ay,
                   store._hj_pov_al_start, store._hj_pov_al_end,
                   store._hj_pov_hand_start, store._hj_pov_hand_end,
                   store._tune_head_peak, store._tune_head_base,
                   store._tune_body_yoff)
        if cur == store._tune_last:
            return
        store._tune_last = cur

        if store._tune_playing:
            _tune_reapply_scene(gid, is_bj, speed)
        else:
            _tune_apply_static(gid, is_bj, speed)

    def _tune_apply_static(gid, is_bj, speed):
        if is_bj:
            slot_tf = bj_get_slot_transform(speed)
            if renpy.has_image("%s bj_right_arm" % gid):
                renpy.show("%s bj_right_arm" % gid, tag="%s_bj_right_arm" % gid,
                    at_list=[slot_tf, _tune_rot(store._bj_pov_ar_ax, store._bj_pov_ar_ay, store._bj_pov_ar_start)],
                    zorder=10051)
            if renpy.has_image("%s bj_arm" % gid):
                renpy.show("%s bj_arm" % gid, tag="%s_bj_arm" % gid,
                    at_list=[slot_tf, _tune_rot(store._bj_pov_al_ax, store._bj_pov_al_ay, store._bj_pov_al_start)],
                    zorder=10052)
            if renpy.has_image("%s bj_hand" % gid):
                renpy.show("%s bj_hand" % gid, tag="%s_bj_hand" % gid,
                    at_list=[_tune_ypos(store._bj_pov_hand_static_y)],
                    zorder=10057)
        else:
            slot_tf = hj_get_slot_transform(speed)
            if renpy.has_image("%s hj_arm_right" % gid):
                renpy.show("%s hj_arm_right" % gid, tag="%s_hj_arm_right" % gid,
                    at_list=[slot_tf, _tune_rot(store._hj_pov_ar_ax, store._hj_pov_ar_ay, store._hj_pov_ar_start)],
                    zorder=10053)
            if renpy.has_image("%s hj_arm_left" % gid):
                renpy.show("%s hj_arm_left" % gid, tag="%s_hj_arm_left" % gid,
                    at_list=[slot_tf, _tune_rot(store._hj_pov_al_ax, store._hj_pov_al_ay, store._hj_pov_al_start)],
                    zorder=10052)
            elif renpy.has_image("%s hj_arm_overlay" % gid):
                renpy.show("%s hj_arm_overlay" % gid, tag="%s_hj_arm_overlay" % gid,
                    at_list=[slot_tf], zorder=10053)
            if renpy.has_image("%s hj_hand" % gid):
                renpy.show("%s hj_hand" % gid, tag="hj_hand",
                    at_list=[_tune_ypos(store._hj_pov_hand_start)],
                    zorder=10060)

    def _tune_reapply_scene(gid, is_bj, speed):
        print("[TUNER] reapply_scene gid=%s is_bj=%s speed=%d" % (gid, is_bj, speed))
        if is_bj:
            slot_tf = bj_get_slot_transform(speed)
            _arm_right_map = {1: bj_pov_arm_right_speed1, 2: bj_pov_arm_right_speed2, 3: bj_pov_arm_right_speed3}
            _has_r = renpy.has_image("%s bj_right_arm" % gid)
            print("[TUNER]   bj right_arm has=%s speed_in_map=%s" % (_has_r, speed in _arm_right_map))
            if _has_r:
                _at_r = [slot_tf]
                if speed in _arm_right_map:
                    _at_r.append(_arm_right_map[speed]())
                renpy.show("%s bj_right_arm" % gid, tag="%s_bj_right_arm" % gid, at_list=_at_r, zorder=10051)
            _arm_left_map = {1: bj_pov_arm_left_speed1, 2: bj_pov_arm_left_speed2, 3: bj_pov_arm_left_speed3}
            if renpy.has_image("%s bj_arm" % gid):
                _at_l = [slot_tf]
                if speed in _arm_left_map:
                    _at_l.append(_arm_left_map[speed]())
                renpy.show("%s bj_arm" % gid, tag="%s_bj_arm" % gid, at_list=_at_l, zorder=10052)
            _pov_h = {0: bj_pov_hand_static, 1: bj_pov_hand_speed1, 2: bj_pov_hand_speed2, 3: bj_pov_hand_speed3}.get(speed, bj_pov_hand_speed1)
            if renpy.has_image("%s bj_hand" % gid):
                renpy.show("%s bj_hand" % gid, tag="%s_bj_hand" % gid, at_list=[_pov_h], zorder=10057)
        else:
            slot_tf = hj_get_slot_transform(speed)
            _arm_speed = min(speed, 3)
            _arm_left_map = {0: hj_pov_arm_left_speed0, 1: hj_pov_arm_left_speed1, 2: hj_pov_arm_left_speed2, 3: hj_pov_arm_left_speed3}
            _arm_right_map = {0: hj_pov_arm_right_speed0, 1: hj_pov_arm_right_speed1, 2: hj_pov_arm_right_speed2, 3: hj_pov_arm_right_speed3}
            _hj_arm_left = "%s hj_arm_left" % gid
            _hj_arm_right = "%s hj_arm_right" % gid
            if renpy.has_image(_hj_arm_left):
                renpy.show(_hj_arm_left, tag="%s_hj_arm_left" % gid, at_list=[slot_tf, _arm_left_map[_arm_speed]()], zorder=10052)
            if renpy.has_image(_hj_arm_right):
                renpy.show(_hj_arm_right, tag="%s_hj_arm_right" % gid, at_list=[slot_tf, _arm_right_map[_arm_speed]()], zorder=10053)
            if not renpy.has_image(_hj_arm_left) and not renpy.has_image(_hj_arm_right):
                _arm_img = "%s hj_arm_overlay" % gid
                if renpy.has_image(_arm_img):
                    renpy.show(_arm_img, tag="%s_hj_arm_overlay" % gid, at_list=[slot_tf], zorder=10053)
            _hj_hand_map = {0: hj_pov_hand_static, 1: hj_pov_hand_speed1, 2: hj_pov_hand_speed2, 3: hj_pov_hand_speed3}
            _hj_hand_t = _hj_hand_map.get(min(speed, 3), hj_pov_hand_speed2)
            _hj_hand_img = "%s hj_hand" % gid
            if renpy.has_image(_hj_hand_img):
                renpy.show(_hj_hand_img, tag="hj_hand", at_list=[_hj_hand_t], zorder=10060)

    config.overlay_screens.append("_tune_hotkey")
    config.overlay_screens.append("_tune_manager")

transform _tune_rot(ax, ay, angle):
    subpixel True
    matrixanchor (ax, ay)
    matrixtransform RotateMatrix(0, 0, angle)

transform _tune_ypos(yoff):
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset yoff

transform _tune_head(yoff):
    subpixel True
    anchor (0.5, 0.75)
    xalign StageCenter
    yalign 2.0
    yoffset yoff

transform _tune_body(yoff):
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset yoff

screen _tune_hotkey():
    key "K_F12" action Function(_tune_toggle)

screen _tune_manager():
    zorder 1500
    if store._tune_visible:
        use transform_tuner

screen transform_tuner():
    zorder 1500
    modal False

    python:
        _is_bj = getattr(store, '_bj_girl', None) is not None
        _scene_label = "BJ" if _is_bj else "HJ"

    frame:
        background "#000000dd"
        xalign 1.0
        yalign 0.0
        xsize 380
        ypadding 12
        xpadding 12

        vbox:
            spacing 4

            text "TUNER %s (F12)" % _scene_label size 16 color "#ffcc00" bold True

            null height 4

            hbox:
                spacing 4
                for _tmode in [("arm_right", "Arm R"), ("arm_left", "Arm L"), ("hand", "Hand"), ("head", "Head"), ("body", "Body")]:
                    textbutton _tmode[1]:
                        text_size 14
                        text_color ("#ffcc00" if store._tune_mode == _tmode[0] else "#888888")
                        text_hover_color "#ffffff"
                        action SetVariable("_tune_mode", _tmode[0])

            null height 4
            hbox:
                spacing 4
                text "Speed:" size 13 color "#aaaaaa" yalign 0.5
                for _tspd in [1, 2, 3]:
                    textbutton str(_tspd):
                        text_size 14
                        text_color ("#ffcc00" if store._tune_speed == _tspd else "#888888")
                        text_hover_color "#ffffff"
                        action Function(_tune_set_speed, _tspd)

            null height 8

            if store._tune_mode == "arm_right":
                if _is_bj:
                    use _tune_row("Anchor X", store._bj_pov_ar_ax, "_bj_pov_ar_ax", 10, 1)
                    use _tune_row("Anchor Y", store._bj_pov_ar_ay, "_bj_pov_ar_ay", 10, 1)
                    use _tune_row_f("Start Angle", store._bj_pov_ar_start, "_bj_pov_ar_start", 1.0, 0.5)
                    use _tune_row_f("End Angle", store._bj_pov_ar_end, "_bj_pov_ar_end", 1.0, 0.5)
                else:
                    use _tune_row("Anchor X", store._hj_pov_ar_ax, "_hj_pov_ar_ax", 10, 1)
                    use _tune_row("Anchor Y", store._hj_pov_ar_ay, "_hj_pov_ar_ay", 10, 1)
                    use _tune_row_f("Start Angle", store._hj_pov_ar_start, "_hj_pov_ar_start", 1.0, 0.5)
                    use _tune_row_f("End Angle", store._hj_pov_ar_end, "_hj_pov_ar_end", 1.0, 0.5)

            elif store._tune_mode == "arm_left":
                if _is_bj:
                    use _tune_row("Anchor X", store._bj_pov_al_ax, "_bj_pov_al_ax", 10, 1)
                    use _tune_row("Anchor Y", store._bj_pov_al_ay, "_bj_pov_al_ay", 10, 1)
                    use _tune_row_f("Start Angle", store._bj_pov_al_start, "_bj_pov_al_start", 1.0, 0.5)
                    use _tune_row_f("End Angle", store._bj_pov_al_end, "_bj_pov_al_end", 1.0, 0.5)
                else:
                    use _tune_row("Anchor X", store._hj_pov_al_ax, "_hj_pov_al_ax", 10, 1)
                    use _tune_row("Anchor Y", store._hj_pov_al_ay, "_hj_pov_al_ay", 10, 1)
                    use _tune_row_f("Start Angle", store._hj_pov_al_start, "_hj_pov_al_start", 1.0, 0.5)
                    use _tune_row_f("End Angle", store._hj_pov_al_end, "_hj_pov_al_end", 1.0, 0.5)

            elif store._tune_mode == "hand":
                if _is_bj:
                    use _tune_row("Static Y (spd0)", store._bj_pov_hand_static_y, "_bj_pov_hand_static_y", 10, 1)
                    use _tune_row("Start Y", store._bj_pov_hand_start, "_bj_pov_hand_start", 10, 1)
                    use _tune_row("End Y", store._bj_pov_hand_end, "_bj_pov_hand_end", 10, 1)
                else:
                    use _tune_row("Start Y", store._hj_pov_hand_start, "_hj_pov_hand_start", 10, 1)
                    use _tune_row("End Y", store._hj_pov_hand_end, "_hj_pov_hand_end", 10, 1)

            elif store._tune_mode == "head":
                use _tune_row("Head Peak", store._tune_head_peak, "_tune_head_peak", 10, 5)
                use _tune_row("Head Base", store._tune_head_base, "_tune_head_base", 10, 5)

            elif store._tune_mode == "body":
                use _tune_row("Body Y", store._tune_body_yoff, "_tune_body_yoff", 20, 5)

            null height 6
            hbox:
                spacing 8
                if store._tune_playing:
                    textbutton "STOP" text_size 14 text_color "#ff4444" text_hover_color "#ff8888" action Function(_tune_stop)
                else:
                    textbutton "PLAY" text_size 14 text_color "#44ff44" text_hover_color "#88ff88" action Function(_tune_play)

            null height 10

            text "=== %s VALUES (Speed %d) ===" % (_scene_label, store._tune_speed) size 13 color "#ffcc00"
            if _is_bj:
                text "Arm R: anchor(%d,%d) start=%.1f end=%.1f" % (store._bj_pov_ar_ax, store._bj_pov_ar_ay, store._bj_pov_ar_start, store._bj_pov_ar_end) size 12 color "#aaffaa"
                text "Arm L: anchor(%d,%d) start=%.1f end=%.1f" % (store._bj_pov_al_ax, store._bj_pov_al_ay, store._bj_pov_al_start, store._bj_pov_al_end) size 12 color "#aaffaa"
                text "Hand: static=%d start=%d end=%d" % (store._bj_pov_hand_static_y, store._bj_pov_hand_start, store._bj_pov_hand_end) size 12 color "#aaffaa"
            else:
                text "Arm R: anchor(%d,%d) start=%.1f end=%.1f" % (store._hj_pov_ar_ax, store._hj_pov_ar_ay, store._hj_pov_ar_start, store._hj_pov_ar_end) size 12 color "#aaffaa"
                text "Arm L: anchor(%d,%d) start=%.1f end=%.1f" % (store._hj_pov_al_ax, store._hj_pov_al_ay, store._hj_pov_al_start, store._hj_pov_al_end) size 12 color "#aaffaa"
                text "Hand: start=%d end=%d" % (store._hj_pov_hand_start, store._hj_pov_hand_end) size 12 color "#aaffaa"
            text "Head: base=%d peak=%d" % (store._tune_head_base, store._tune_head_peak) size 12 color "#aaffaa"
            text "Body: yoffset=%d" % store._tune_body_yoff size 12 color "#aaffaa"

    timer 0.15 repeat True action Function(_tune_apply)

screen _tune_row(label, val, var, big, small):
    hbox:
        spacing 3
        text "[label]: [val]" size 13 color "#ffffff" yalign 0.5 xsize 140
        textbutton "-[big]":
            text_size 12
            text_color "#ff8888"
            text_hover_color "#ffffff"
            action SetVariable(var, val - big)
        textbutton "-[small]":
            text_size 12
            text_color "#ffaaaa"
            text_hover_color "#ffffff"
            action SetVariable(var, val - small)
        textbutton "+[small]":
            text_size 12
            text_color "#aaffaa"
            text_hover_color "#ffffff"
            action SetVariable(var, val + small)
        textbutton "+[big]":
            text_size 12
            text_color "#88ff88"
            text_hover_color "#ffffff"
            action SetVariable(var, val + big)

screen _tune_row_f(label, val, var, big, small):
    hbox:
        spacing 3
        text "%s: %.1f" % (label, val) size 13 color "#ffffff" yalign 0.5 xsize 140
        textbutton "-%.0f" % big:
            text_size 12
            text_color "#ff8888"
            text_hover_color "#ffffff"
            action SetVariable(var, val - big)
        textbutton "-%.1f" % small:
            text_size 12
            text_color "#ffaaaa"
            text_hover_color "#ffffff"
            action SetVariable(var, val - small)
        textbutton "+%.1f" % small:
            text_size 12
            text_color "#aaffaa"
            text_hover_color "#ffffff"
            action SetVariable(var, val + small)
        textbutton "+%.0f" % big:
            text_size 12
            text_color "#88ff88"
            text_hover_color "#ffffff"
            action SetVariable(var, val + big)

# ============================================================
# GIF Layer Test — animated GIF multi-layer preview
# ============================================================
image gif_test_body:
    "images/test/Scene1body/000.png"
    0.06
    "images/test/Scene1body/001.png"
    0.06
    "images/test/Scene1body/002.png"
    0.06
    "images/test/Scene1body/003.png"
    0.06
    "images/test/Scene1body/004.png"
    0.06
    "images/test/Scene1body/005.png"
    0.06
    "images/test/Scene1body/006.png"
    0.06
    "images/test/Scene1body/007.png"
    0.06
    "images/test/Scene1body/008.png"
    0.06
    "images/test/Scene1body/009.png"
    0.06
    "images/test/Scene1body/010.png"
    0.06
    "images/test/Scene1body/011.png"
    0.06
    "images/test/Scene1body/012.png"
    0.06
    "images/test/Scene1body/013.png"
    0.06
    "images/test/Scene1body/014.png"
    0.06
    "images/test/Scene1body/015.png"
    0.06
    "images/test/Scene1body/016.png"
    0.06
    "images/test/Scene1body/017.png"
    0.06
    "images/test/Scene1body/018.png"
    0.06
    "images/test/Scene1body/019.png"
    0.06
    "images/test/Scene1body/020.png"
    0.06
    "images/test/Scene1body/021.png"
    0.06
    "images/test/Scene1body/022.png"
    0.06
    "images/test/Scene1body/023.png"
    0.06
    "images/test/Scene1body/024.png"
    0.06
    "images/test/Scene1body/025.png"
    0.06
    "images/test/Scene1body/026.png"
    0.06
    "images/test/Scene1body/027.png"
    0.06
    "images/test/Scene1body/028.png"
    0.06
    "images/test/Scene1body/029.png"
    0.06
    "images/test/Scene1body/030.png"
    0.06
    "images/test/Scene1body/031.png"
    0.06
    "images/test/Scene1body/032.png"
    0.06
    repeat

image gif_test_breast:
    "images/test/Scene1Breast/000.png"
    0.06
    "images/test/Scene1Breast/001.png"
    0.06
    "images/test/Scene1Breast/002.png"
    0.06
    "images/test/Scene1Breast/003.png"
    0.06
    "images/test/Scene1Breast/004.png"
    0.06
    "images/test/Scene1Breast/005.png"
    0.06
    "images/test/Scene1Breast/006.png"
    0.06
    "images/test/Scene1Breast/007.png"
    0.06
    "images/test/Scene1Breast/008.png"
    0.06
    "images/test/Scene1Breast/009.png"
    0.06
    "images/test/Scene1Breast/010.png"
    0.06
    "images/test/Scene1Breast/011.png"
    0.06
    "images/test/Scene1Breast/012.png"
    0.06
    "images/test/Scene1Breast/013.png"
    0.06
    "images/test/Scene1Breast/014.png"
    0.06
    "images/test/Scene1Breast/015.png"
    0.06
    "images/test/Scene1Breast/016.png"
    0.06
    "images/test/Scene1Breast/017.png"
    0.06
    "images/test/Scene1Breast/018.png"
    0.06
    "images/test/Scene1Breast/019.png"
    0.06
    "images/test/Scene1Breast/020.png"
    0.06
    "images/test/Scene1Breast/021.png"
    0.06
    "images/test/Scene1Breast/022.png"
    0.06
    "images/test/Scene1Breast/023.png"
    0.06
    "images/test/Scene1Breast/024.png"
    0.06
    "images/test/Scene1Breast/025.png"
    0.06
    "images/test/Scene1Breast/026.png"
    0.06
    "images/test/Scene1Breast/027.png"
    0.06
    "images/test/Scene1Breast/028.png"
    0.06
    "images/test/Scene1Breast/029.png"
    0.06
    "images/test/Scene1Breast/030.png"
    0.06
    "images/test/Scene1Breast/031.png"
    0.06
    "images/test/Scene1Breast/032.png"
    0.06
    repeat

label _at_gif_layer_test:
    scene black
    show gif_test_body zorder 100
    show gif_test_breast zorder 200
    "GIF Layer Test: body (z=100) + breast (z=200). Click to exit."
    hide gif_test_breast
    hide gif_test_body
    return
