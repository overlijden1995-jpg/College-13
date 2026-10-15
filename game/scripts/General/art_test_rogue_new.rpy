# ============================================================
# New Rogue — Art Test Screen & Label
# Standalone test for the new Rogue standing sprite.
# ============================================================

init python:

    _RN_FACES = ["base", "base_extend"]
    _RN_MOUTHS = ["smile", "grimace", "lipbite", "sad", "open", "tongue", "tongue2"]
    _RN_EYES = ["default", "love"]
    _RN_BROWS = ["normal", "anger", "sad", "confused", "shocked"]
    _RN_EYELIDS = ["normal", "shocked", "sultry", "closed", "squint", "squint2"]
    _RN_RIGHT_ARMS = ["idle", "1", "2", "none"]
    _RN_LEFT_ARMS = ["idle", "1", "none"]
    _RN_PUBES = ["none", "bush", "strip", "tri"]
    _RN_PANTIES = ["none", "thong", "thong_down", "panties", "panties_down", "bikini", "bikini_alt", "bikini_down"]
    _RN_SKIRTS = ["none", "skirt", "skirt_up", "skirt2", "skirt2_up", "latex", "latex_up", "latex_see", "latex_see_up"]
    _RN_FEET = ["none", "boots", "boots_nosocks"]
    _RN_LEGWEAR = ["none", "socks", "stockings"]
    # vest = the model; the Clothed / larger alt cut follows the chest state automatically
    _RN_VESTS = ["none", "vest", "vest_short"]
    _RN_CHEST_NORMAL = ["top", "bra", "bikini", "backing", "bare"]
    # crossed: merged bases (empty / bra / bikini); "bare" and "top" draw over the empty base
    _RN_CHEST_CROSSED = ["empty", "bra", "bikini", "bare", "top"]
    _RN_ZOOMS = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]

    def _rn_cycle(var_name, options):
        cur = getattr(store, var_name)
        idx = options.index(cur) if cur in options else -1
        setattr(store, var_name, options[(idx + 1) % len(options)])
        renpy.restart_interaction()

    def _rn_toggle(var_name):
        setattr(store, var_name, not getattr(store, var_name))
        renpy.restart_interaction()

    def _rn_chest_options():
        if store._rn_crossed:
            return _RN_CHEST_CROSSED
        return _RN_CHEST_NORMAL

    def _rn_toggle_crossed():
        store._rn_crossed = not store._rn_crossed
        valid = _rn_chest_options()
        if store._rn_chest not in valid:
            store._rn_chest = valid[0]
        renpy.restart_interaction()

    def _rn_cycle_zoom():
        cur = store._rn_zoom
        for i, z in enumerate(_RN_ZOOMS):
            if abs(z - cur) < 0.01:
                store._rn_zoom = _RN_ZOOMS[(i + 1) % len(_RN_ZOOMS)]
                renpy.restart_interaction()
                return
        store._rn_zoom = 1.0
        renpy.restart_interaction()

    def _rn_reset_all():
        store._rn_face = "base"
        store._rn_mouth = "smile"
        store._rn_whites = "default"
        store._rn_eyes = "default"
        store._rn_brows = "sad"
        store._rn_eyelids = "normal"
        store._rn_blush = False
        store._rn_crossed = False
        store._rn_right_arm = "idle"
        store._rn_right_glove = True
        store._rn_right_band = True
        store._rn_right_vest = True
        store._rn_left_arm = "idle"
        store._rn_left_glove = True
        store._rn_left_band = True
        store._rn_left_vest = True
        store._rn_chest = "top"
        store._rn_pierced = False
        store._rn_tape = False
        store._rn_vest = "vest_short"
        store._rn_pubes = "tri"
        store._rn_panties = "thong"
        store._rn_skirt = "latex"
        store._rn_feet = "boots_nosocks"
        store._rn_legwear = "stockings"
        store._rn_collar = True
        store._rn_zoom = 1.0
        renpy.restart_interaction()


# ── Screen ────────────────────────────────────────────────

screen rogue_new_test():
    zorder 200
    modal True

    # Sprite display (centered in remaining area after sidebar)
    add "rogue_new standing":
        anchor (0.5, 1.0)
        pos (1130, 1080)
        zoom _rn_zoom

    # Sidebar panel
    frame:
        xalign 0.0
        yalign 0.0
        xsize 360
        ysize 1080
        background "#000000CC"
        padding (12, 12, 12, 12)

        viewport:
            scrollbars "vertical"
            mousewheel True
            xsize 336
            ysize 1056

            vbox:
                spacing 4

                # ── TITLE ──
                text "NEW ROGUE — SPRITE TEST" size 16 color "#ffcc00" bold True xalign 0.5

                null height 8

                # ── HEAD ──
                text "HEAD" size 14 color "#ffcc00" bold True

                hbox:
                    spacing 4
                    text "Face:" size 13 color "#ccc" yalign 0.5 xsize 80
                    textbutton "[_rn_face]" action Function(_rn_cycle, "_rn_face", _RN_FACES) text_size 13 xsize 140

                hbox:
                    spacing 4
                    text "Mouth:" size 13 color "#ccc" yalign 0.5 xsize 80
                    textbutton "[_rn_mouth]" action Function(_rn_cycle, "_rn_mouth", _RN_MOUTHS) text_size 13 xsize 140

                hbox:
                    spacing 4
                    text "Whites:" size 13 color "#ccc" yalign 0.5 xsize 80
                    textbutton "[_rn_whites]" action Function(_rn_cycle, "_rn_whites", ["default", "shocked"]) text_size 13 xsize 100

                hbox:
                    spacing 4
                    text "Eyes:" size 13 color "#ccc" yalign 0.5 xsize 80
                    textbutton "[_rn_eyes]" action Function(_rn_cycle, "_rn_eyes", _RN_EYES) text_size 13 xsize 140

                hbox:
                    spacing 4
                    text "Brows:" size 13 color "#ccc" yalign 0.5 xsize 80
                    textbutton "[_rn_brows]" action Function(_rn_cycle, "_rn_brows", _RN_BROWS) text_size 13 xsize 140

                hbox:
                    spacing 4
                    text "EyeLids:" size 13 color "#ccc" yalign 0.5 xsize 80
                    textbutton "[_rn_eyelids]" action Function(_rn_cycle, "_rn_eyelids", _RN_EYELIDS) text_size 13 xsize 140

                hbox:
                    spacing 4
                    text "Blush:" size 13 color "#ccc" yalign 0.5 xsize 80
                    if _rn_blush:
                        textbutton "ON" action Function(_rn_toggle, "_rn_blush") text_size 13 text_color "#4f4" xsize 60
                    else:
                        textbutton "OFF" action Function(_rn_toggle, "_rn_blush") text_size 13 text_color "#f44" xsize 60

                null height 8

                # ── BODY ──
                text "BODY" size 14 color "#ffcc00" bold True

                hbox:
                    spacing 4
                    text "Pubes:" size 13 color "#ccc" yalign 0.5 xsize 80
                    textbutton "[_rn_pubes]" action Function(_rn_cycle, "_rn_pubes", _RN_PUBES) text_size 13 xsize 120

                hbox:
                    spacing 4
                    text "Panties:" size 13 color "#ccc" yalign 0.5 xsize 80
                    textbutton "[_rn_panties]" action Function(_rn_cycle, "_rn_panties", _RN_PANTIES) text_size 13 xsize 120

                hbox:
                    spacing 4
                    text "Skirt:" size 13 color "#ccc" yalign 0.5 xsize 80
                    textbutton "[_rn_skirt]" action Function(_rn_cycle, "_rn_skirt", _RN_SKIRTS) text_size 13 xsize 120

                hbox:
                    spacing 4
                    text "Feet:" size 13 color "#ccc" yalign 0.5 xsize 80
                    textbutton "[_rn_feet]" action Function(_rn_cycle, "_rn_feet", _RN_FEET) text_size 13 xsize 120

                hbox:
                    spacing 4
                    text "Legwear:" size 13 color "#ccc" yalign 0.5 xsize 80
                    textbutton "[_rn_legwear]" action Function(_rn_cycle, "_rn_legwear", _RN_LEGWEAR) text_size 13 xsize 120

                hbox:
                    spacing 4
                    text "Collar:" size 13 color "#ccc" yalign 0.5 xsize 80
                    if _rn_collar:
                        textbutton "ON" action Function(_rn_toggle, "_rn_collar") text_size 13 text_color "#4f4" xsize 60
                    else:
                        textbutton "OFF" action Function(_rn_toggle, "_rn_collar") text_size 13 text_color "#f44" xsize 60

                null height 8

                # ── CHEST ──
                text "CHEST" size 14 color "#ffcc00" bold True

                hbox:
                    spacing 4
                    text "Crossed:" size 13 color "#ccc" yalign 0.5 xsize 80
                    if _rn_crossed:
                        textbutton "ON" action Function(_rn_toggle_crossed) text_size 13 text_color "#4f4" xsize 60
                    else:
                        textbutton "OFF" action Function(_rn_toggle_crossed) text_size 13 text_color "#f44" xsize 60

                hbox:
                    spacing 4
                    text "Chest:" size 13 color "#ccc" yalign 0.5 xsize 80
                    textbutton "[_rn_chest]" action Function(_rn_cycle, "_rn_chest", _rn_chest_options()) text_size 13 xsize 120

                hbox:
                    spacing 4
                    text "Vest:" size 13 color "#ccc" yalign 0.5 xsize 80
                    textbutton "[_rn_vest]" action Function(_rn_cycle, "_rn_vest", _RN_VESTS) text_size 13 xsize 160

                hbox:
                    spacing 4
                    text "Pierced:" size 13 color "#ccc" yalign 0.5 xsize 80
                    if _rn_chest == "bare":
                        if _rn_pierced:
                            textbutton "ON" action Function(_rn_toggle, "_rn_pierced") text_size 13 text_color "#4f4" xsize 60
                        else:
                            textbutton "OFF" action Function(_rn_toggle, "_rn_pierced") text_size 13 text_color "#f44" xsize 60
                    else:
                        text "---" size 13 color "#555" yalign 0.5

                hbox:
                    spacing 4
                    text "Tape:" size 13 color "#ccc" yalign 0.5 xsize 80
                    if _rn_chest == "bare":
                        if _rn_tape:
                            textbutton "ON" action Function(_rn_toggle, "_rn_tape") text_size 13 text_color "#4f4" xsize 60
                        else:
                            textbutton "OFF" action Function(_rn_toggle, "_rn_tape") text_size 13 text_color "#f44" xsize 60
                    else:
                        text "---" size 13 color "#555" yalign 0.5

                null height 8

                # ── ARMS ──
                text "ARMS" size 14 color "#ffcc00" bold True

                if _rn_crossed:
                    text "(crossed — only Glv applies)" size 12 color "#888" italic True

                hbox:
                    spacing 4
                    text "R.Arm:" size 13 color "#ccc" yalign 0.5 xsize 80
                    textbutton "[_rn_right_arm]":
                        action Function(_rn_cycle, "_rn_right_arm", _RN_RIGHT_ARMS)
                        text_size 13
                        xsize 80
                        sensitive (not _rn_crossed)

                hbox:
                    spacing 4
                    text "R.Acc:" size 13 color "#ccc" yalign 0.5 xsize 80
                    if _rn_right_glove:
                        textbutton "Glv" action Function(_rn_toggle, "_rn_right_glove") text_size 12 text_color "#4f4" xsize 50
                    else:
                        textbutton "Glv" action Function(_rn_toggle, "_rn_right_glove") text_size 12 text_color "#f44" xsize 50
                    if _rn_right_band:
                        textbutton "Bnd" action Function(_rn_toggle, "_rn_right_band") text_size 12 text_color "#4f4" xsize 50 sensitive (not _rn_crossed)
                    else:
                        textbutton "Bnd" action Function(_rn_toggle, "_rn_right_band") text_size 12 text_color "#f44" xsize 50 sensitive (not _rn_crossed)
                    if _rn_right_vest:
                        textbutton "Vst" action Function(_rn_toggle, "_rn_right_vest") text_size 12 text_color "#4f4" xsize 50 sensitive (not _rn_crossed)
                    else:
                        textbutton "Vst" action Function(_rn_toggle, "_rn_right_vest") text_size 12 text_color "#f44" xsize 50 sensitive (not _rn_crossed)

                null height 4

                hbox:
                    spacing 4
                    text "L.Arm:" size 13 color "#ccc" yalign 0.5 xsize 80
                    textbutton "[_rn_left_arm]":
                        action Function(_rn_cycle, "_rn_left_arm", _RN_LEFT_ARMS)
                        text_size 13
                        xsize 80
                        sensitive (not _rn_crossed)

                hbox:
                    spacing 4
                    text "L.Acc:" size 13 color "#ccc" yalign 0.5 xsize 80
                    if _rn_left_glove:
                        textbutton "Glv" action Function(_rn_toggle, "_rn_left_glove") text_size 12 text_color "#4f4" xsize 50
                    else:
                        textbutton "Glv" action Function(_rn_toggle, "_rn_left_glove") text_size 12 text_color "#f44" xsize 50
                    if _rn_left_band:
                        textbutton "Bnd" action Function(_rn_toggle, "_rn_left_band") text_size 12 text_color "#4f4" xsize 50 sensitive (not _rn_crossed)
                    else:
                        textbutton "Bnd" action Function(_rn_toggle, "_rn_left_band") text_size 12 text_color "#f44" xsize 50 sensitive (not _rn_crossed)
                    if _rn_left_vest:
                        textbutton "Vst" action Function(_rn_toggle, "_rn_left_vest") text_size 12 text_color "#4f4" xsize 50 sensitive (not _rn_crossed)
                    else:
                        textbutton "Vst" action Function(_rn_toggle, "_rn_left_vest") text_size 12 text_color "#f44" xsize 50 sensitive (not _rn_crossed)

                null height 12

                # ── CONTROLS ──
                text "CONTROLS" size 14 color "#ffcc00" bold True

                hbox:
                    spacing 4
                    text "Zoom:" size 13 color "#ccc" yalign 0.5 xsize 80
                    textbutton "[_rn_zoom]x" action Function(_rn_cycle_zoom) text_size 13 xsize 80

                null height 4

                hbox:
                    spacing 8
                    textbutton "Reset All" action Function(_rn_reset_all) text_size 14 text_color "#ff8800"
                    textbutton "Back" action Return("back") text_size 14 text_color "#ff4444"


# ── Label ─────────────────────────────────────────────────

label _at_rogue_new:
    scene black
    $ _rn_reset_all()
    show screen rogue_new_test
    while True:
        $ _rn_result = ui.interact()
        if _rn_result == "back":
            hide screen rogue_new_test
            scene black
            return
