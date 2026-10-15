# screens.rpy – College Traits

default _phone_is_open = False

##############################################################################
# SAY – diálogo e narração
##############################################################################
##############################################################################
screen say(who, what, side_image=None, two_window=False, CountWords = 0):

    on "show" action Function(_force_dismiss_sex_bubble)

    # =======================================================
    # Detecta se é o Player
    # =======================================================
    $ is_player = (
        who == getattr(store, "PlayerChar", None).name if hasattr(store, "PlayerChar") else False
    ) or (who == "Player") or (
        who == getattr(store, "Player", None).Name if hasattr(store, "Player") else False
    )

    # Sempre deixar o nome em CAPS
    $ capsname = who.upper() if who else ""

    # Identifica se é uma garota conhecida
    $ speaker_girl = find_girl_for_who(who) if who else None


    # =======================================================
    # DIÁLOGO (PLAYER OU GAROTAS) – BALÃO
    # =======================================================
    # GAG SYSTEM (mantém funcionamento)
    python:
        gagged = False
        if speaker_girl and getattr(speaker_girl, "Gag", False):
            gagged = True

    if gagged:
        $ CountWords = what.count(" ") if what.count(" ") <= 10 else 10
        $ CountWords = CountWords - what.count(".")
        $ what = ""
        python:
            while CountWords >= 0:
                CountWords -= 1
                what += renpy.random.choice([
                    "Mrph","Hrgaph","Rhgn","Phar","Geghs",
                    "Paha","Grde","Phraph","Ugh"
                ])
                what += " " if CountWords > 0 else "."


    # =======================================================
    # BALÃO DE DIÁLOGO — posiciona no espaço livre entre sprites
    # =======================================================
    python:
        # Collect all sprite x positions on screen
        _scene_girls = girls_on_scene()
        _sprite_xs = [getattr(g, "SpriteLoc", 0.5) or 0.5 for g in _scene_girls]

        # Candidate zones: (bubble_x, arrow_x, arrow_flip)
        _zones = [
            (0.15, 0.12, True),
            (0.30, 0.26, True),
            (0.50, 0.50, False),
            (0.70, 0.74, False),
            (0.85, 0.88, False),
        ]

        # Pick zone with max clearance from sprites (no lambda/def)
        _best_zone = _zones[2]  # default center
        _best_dist = -1.0
        for _z in _zones:
            if _sprite_xs:
                _d = min(abs(_z[0] - _sx) for _sx in _sprite_xs)
            else:
                _d = 1.0
            if _d > _best_dist:
                _best_dist = _d
                _best_zone = _z

        bubble_xalign = _best_zone[0]
        name_xalign   = _best_zone[0]
        arrow_xalign  = _best_zone[1]
        arrow_flip    = _best_zone[2]

        # During sex scenes, force balloon to the left
        _in_sex = (_hj_girl is not None or _bj_girl is not None or _titjob_girl is not None or _cowgirl_girl is not None or _rcg_girl is not None or _doggy_girl is not None or _laying_girl is not None)
        _text_len = len(what) if what else 0
        _balloon_xmax = 980  # default

        if _in_sex:
            if _text_len > 140:
                bubble_xalign = 0.02
                _balloon_xmax = 620
            elif _text_len > 90:
                bubble_xalign = 0.08
                _balloon_xmax = 720
            else:
                bubble_xalign = 0.15
            name_xalign = bubble_xalign
            arrow_flip = True
        elif speaker_girl:
            loc = getattr(speaker_girl, "SpriteLoc", StageCenter) or StageCenter
            if loc <= 0.5:
                bubble_xalign = min(0.85, loc + 0.25)
                arrow_flip = False
            else:
                bubble_xalign = max(0.15, loc - 0.25)
                arrow_flip = True
            name_xalign = bubble_xalign

    zorder 200

    vbox:
        xalign bubble_xalign
        yalign 0.14
        style "say_two_window_vbox"

        # Nome acima do balão, alinhado à esquerda
        if capsname:
            window:
                style "say_who_window"
                xalign 0.0
                text capsname id "who" size 24 font "fonts/WorkSans-SemiBold.ttf" color "#0b1324"

        window:
            style "say_balloon"
            xmaximum _balloon_xmax
            has vbox:
                style "say_vbox"

            # Texto
            text what id "what" size 30 font "fonts/WorkSans-Medium.ttf" text_align 0.5 color "#0b1324"


    # QUICK MENU
    use quick_menu

##############################################################################
# SEX BUBBLE — non-blocking dialogue overlay during sex scenes (except BJ)
##############################################################################

transform sex_bubble_fade:
    alpha 1.0
    pause 0.1
    alpha 1.0

transform sex_bubble_fadeout:
    alpha 1.0
    linear 0.4 alpha 0.0

screen sex_bubble():

    $ _sb_who = store._sex_bubble_who
    $ _sb_text = store._sex_bubble_text or ""
    $ _sb_color = store._sex_bubble_color or "#ffffff"

    $ _sb_len = len(_sb_text)
    $ _sb_duration = max(2.5, min(5.5, _sb_len * 0.04))

    python:
        if _sb_len > 140:
            _sb_xalign = 0.02
            _sb_xmax = 620
        elif _sb_len > 90:
            _sb_xalign = 0.08
            _sb_xmax = 720
        else:
            _sb_xalign = 0.15
            _sb_xmax = 780

    zorder 200

    vbox at sex_bubble_fade:
        xalign _sb_xalign
        yalign 0.14
        style "say_two_window_vbox"

        if _sb_who:
            window:
                style "say_who_window"
                xalign 0.0
                text _sb_who.upper() size 24 font "fonts/WorkSans-SemiBold.ttf" color _sb_color

        window:
            style "say_balloon"
            xmaximum _sb_xmax
            has vbox:
                style "say_vbox"

            text _sb_text size 30 font "fonts/WorkSans-Medium.ttf" text_align 0.5 color "#0b1324"

    timer _sb_duration action [Function(_sex_bubble_dismiss), Hide("sex_bubble")]

##############################################################################
# CHOICE – menus in-game
##############################################################################

screen choice(items):

    # Auto-continue: find the "Keep going" action and fire it on a 3s timer
    python:
        _ac_keep_going_action = None
        if store._auto_continue:
            for _ac_cap, _ac_act, _ac_ch in items:
                if _ac_cap == "Keep going" and _ac_act:
                    _ac_keep_going_action = _ac_act
                    break

    if _ac_keep_going_action:
        timer 3.0 action _ac_keep_going_action

    frame:
        style "SideMenuFrame"
        anchor (0.0, 1.0)
        xpos 35
        ypos 1060
        if _phone_is_open:
            xoffset -1000

        vbox:
            spacing 0

            # Header with accent bar + auto-continue toggle
            hbox:
                spacing 8
                yalign 0.5

                frame:
                    background "#7dd3fc"
                    xsize 3
                    ysize 22
                    yalign 0.5

                text _("ACTIONS"):
                    size 19
                    color "#7dd3fc"
                    font "fonts/WorkSans-Bold.ttf"
                    outlines [(1, "#06101e", 0, 0)]
                    yalign 0.5

                # Show auto-continue toggle only when "Keep going" is available
                python:
                    _ac_has_keep_going = False
                    for _ac_c2, _ac_a2, _ac_ch2 in items:
                        if _ac_c2 == "Keep going" and _ac_a2:
                            _ac_has_keep_going = True
                            break

                if _ac_has_keep_going:
                    textbutton ("{color=#fbbf24}AUTO{/color}" if store._auto_continue else "{color=#555e6e}AUTO{/color}"):
                        action Function(_toggle_auto_continue)
                        yalign 0.5
                        text_size 16
                        text_font "fonts/WorkSans-Bold.ttf"
                        text_outlines [(1, "#06101e", 0, 0)]
                        background None
                        hover_background None
                        padding (8, 4)
                        xoffset 60

                # F9 Art Test with a scene up: the scene alone until a click (art_test.rpy, _at_hide_menu)
                if _at_scene_on_screen():
                    textbutton _("HIDE MENU"):
                        action Function(_at_hide_menu)
                        yalign 0.5
                        text_size 16
                        text_font "fonts/WorkSans-Bold.ttf"
                        text_color "#7dd3fc"
                        text_hover_color "#ffffff"
                        text_outlines [(1, "#06101e", 0, 0)]
                        background None
                        hover_background None
                        padding (8, 4)
                        xoffset 60

            $ _scroll_threshold = getattr(store, "_menu_scroll_threshold", 12)
            if len(items) > _scroll_threshold:
                # as wide as the widest row of the active menu size (Preferences > Menu Size):
                # a fixed 426 clipped the touch-sized buttons
                $ _choice_vp_w = style.SideMenuButton.xmaximum + 6
                hbox:
                    spacing 4
                    viewport id "choice_vp":
                        mousewheel True
                        draggable True
                        ymaximum 826
                        xsize _choice_vp_w

                        vbox:
                            xsize _choice_vp_w
                            for _ci in items:

                                $ caption, action, chosen = _ci
                                $ _ci_faces = nav_faces((getattr(_ci, "kwargs", None) or {}).get("nav"))
                                $ _is_section = caption.startswith("!section!")
                                $ _is_disabled = caption.startswith("!disabled!")

                                if _is_section:
                                    $ _section_label = caption[len("!section!"):]
                                    hbox:
                                        spacing 8
                                        yalign 0.5
                                        xoffset 6
                                        yoffset 4
                                        frame:
                                            background "#7dd3fc"
                                            xsize 3
                                            ysize 18
                                            yalign 0.5
                                        text _section_label:
                                            size 17
                                            color "#7dd3fc"
                                            font "fonts/WorkSans-Bold.ttf"
                                            outlines [(1, "#06101e", 0, 0)]
                                            yalign 0.5

                                elif _is_disabled:
                                    $ _display_caption = caption[len("!disabled!"):]
                                    textbutton _display_caption:
                                        style "SideMenuButtonDisabled"
                                        text_style "SideMenuButtonTextDisabled"
                                        action NullAction()
                                        sensitive False

                                elif action and _ci_faces:
                                    use choice_faces_button(caption, action, _ci_faces)

                                elif action:
                                    textbutton caption:
                                        style "SideMenuButton"
                                        text_style "SideMenuButtonText"
                                        action action

                                else:
                                    textbutton caption:
                                        style "SideMenuButtonDisabled"
                                        text_style "SideMenuButtonTextDisabled"
                                        action NullAction()
                                        sensitive False

                    vbar value YScrollValue("choice_vp"):
                        xsize 20
                        ymaximum 826
                        base_bar Solid("#1a2540")
                        thumb Solid("#7dd3fc")
                        thumb_offset 0

            else:
                for _ci in items:

                    $ caption, action, chosen = _ci
                    # a "Go to ..." item carries its place (menu argument `nav`): faces of the girls there
                    $ _ci_faces = nav_faces((getattr(_ci, "kwargs", None) or {}).get("nav"))
                    $ _is_section = caption.startswith("!section!")
                    $ _is_disabled = caption.startswith("!disabled!")

                    if _is_section:
                        $ _section_label = caption[len("!section!"):]
                        hbox:
                            spacing 8
                            yalign 0.5
                            xoffset 6
                            yoffset 4
                            frame:
                                background "#7dd3fc"
                                xsize 3
                                ysize 18
                                yalign 0.5
                            text _section_label:
                                size 17
                                color "#7dd3fc"
                                font "fonts/WorkSans-Bold.ttf"
                                outlines [(1, "#06101e", 0, 0)]
                                yalign 0.5

                    elif _is_disabled:
                        $ _display_caption = caption[len("!disabled!"):]
                        textbutton _display_caption:
                            style "SideMenuButtonDisabled"
                            text_style "SideMenuButtonTextDisabled"
                            action NullAction()
                            sensitive False

                    elif action and _ci_faces:
                        use choice_faces_button(caption, action, _ci_faces)

                    elif action:
                        textbutton caption:
                            style "SideMenuButton"
                            text_style "SideMenuButtonText"
                            action action

                    else:
                        textbutton caption:
                            style "SideMenuButtonDisabled"
                            text_style "SideMenuButtonTextDisabled"
                            action NullAction()
                            sensitive False


# A choice row with the faces of the girls at its destination on the right (nav_faces). As wide as a plain row
# with that caption (SideMenuButton xminimum..xmaximum) plus the faces; a caption that no longer fits wraps
# instead of running under them. The faces overlap a little (NAV_FACE_STEP), each in a ring of her color.
screen choice_faces_button(caption, action, faces):
    python:
        _fb = style.SideMenuButton
        _fb_pad = _fb.left_padding + _fb.right_padding
        _fb_faces_w = NAV_FACE + NAV_FACE_STEP * (len(faces) - 1)
        _fb_txt_max = _fb.xmaximum - _fb_pad - NAV_FACE_GAP - _fb_faces_w
        _fb_txt_w = min(_fb_txt_max, int(Text(caption, style="SideMenuButtonText").size()[0]) + 1)
        _fb_w = max(_fb.xminimum, min(_fb.xmaximum, _fb_txt_w + NAV_FACE_GAP + _fb_faces_w + _fb_pad))
        # what is left between the caption and the faces pushes them to the right edge. The caption sits in a
        # fixed of exactly _fb_txt_w: a wrapped text alone is only as wide as its longest line
        _fb_space = _fb_w - _fb_pad - _fb_txt_w - _fb_faces_w

    button:
        style "SideMenuButton"
        xsize _fb_w
        action action

        hbox:
            spacing _fb_space

            fixed:
                xsize _fb_txt_w
                yfit True
                yalign 0.5
                # yalign 0.0: the button text style inherits yalign 0.5, and a centered child makes the fitted
                # fixed as tall as the whole screen
                text caption:
                    style "SideMenuButtonText"
                    xmaximum _fb_txt_w
                    yalign 0.0

            hbox:
                yalign 0.5
                spacing NAV_FACE_STEP - NAV_FACE
                for _fb_img, _fb_col in faces:
                    fixed:
                        xysize (NAV_FACE, NAV_FACE)
                        add Transform(_pk_tint(_PK_RING, _fb_col), xysize=(NAV_FACE, NAV_FACE))
                        add _pk_face(_fb_img, NAV_FACE - 6) align (0.5, 0.5)



init -2:
    $ config.narrator_menu = True

    style menu_window is default

    style menu_choice is button_text:
        clear

    style menu_choice_button is button:
        xminimum int(config.screen_width * 0.35)
        xmaximum int(config.screen_width * 0.35)


##############################################################################
# INPUT
##############################################################################

screen input(prompt):

    window style "input_window":
        has vbox

        text prompt style "input_prompt" color "#000000" size 20
        input id "input" style "input_text" color "#222222" size 22

    use quick_menu


##############################################################################
# NVL
##############################################################################

screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox:
            style "nvl_vbox"

        for who, what, who_id, what_id, window_id in dialogue:
            window:
                id window_id

                has hbox:
                    spacing 10

                if who is not None:
                    text who id who_id

                text what id what_id

        if items:

            vbox:
                id "menu"

                for caption, action, chosen in items:

                    if action:

                        button:
                            style "nvl_menu_choice_button"
                            action action

                            text caption style "nvl_menu_choice"

                    else:
                        text caption style "nvl_dialogue"

    use quick_menu


##############################################################################
# MAIN MENU
##############################################################################

# the chevron beside the social icons nudges toward them
transform menu_social_arrow:
    subpixel True
    xoffset 0
    easeout 0.45 xoffset 10
    easein 0.45 xoffset 0
    pause 0.3
    repeat

init python:
    def main_menu_continue_slot():
        """The save "Continue" loads: the newest of them all (numbered pages, auto, quick). None = no save yet."""
        return renpy.newest_slot(r"(\d+|auto|quick)-")


screen main_menu():

    tag menu

    add MENU_ART

    # Social links, top-right corner, with the call to the polls pointing at them
    hbox:
        xalign 0.98
        yalign 0.04
        spacing 20

        hbox:
            yalign 0.5
            spacing 14
            text _("Vote on the next girl\nor suggest new mechanics here") style "menu_social_call"
            add _pk_icon("next", ROD_ACCENT_WARM) zoom 2.2 yalign 0.5 at menu_social_arrow

        imagebutton:
            idle Transform("images/menus/Patreon.png", zoom=0.15)
            hover Transform("images/menus/Patreon.png", zoom=0.15, matrixcolor=BrightnessMatrix(0.15))
            action OpenURL("https://patreon.com/RodProjectsDev")

        imagebutton:
            idle Transform("images/menus/SubscribeStar.png", zoom=0.15)
            hover Transform("images/menus/SubscribeStar.png", zoom=0.15, matrixcolor=BrightnessMatrix(0.15))
            action OpenURL("https://subscribestar.adult/rodprojects")

        imagebutton:
            idle Transform("images/menus/Discord.png", zoom=0.15)
            hover Transform("images/menus/Discord.png", zoom=0.15, matrixcolor=BrightnessMatrix(0.15))
            action OpenURL("https://discord.gg/SnzXf6z3Ke")

    # Continue (the newest save) leads when there is a save, Start Game when there is none
    $ _mm_last = main_menu_continue_slot()

    frame:
        style "menu_main_frame"

        vbox:
            spacing 10

            use menu_main_button(_("Continue"), "play", (FileLoad(_mm_last, slot=True) if _mm_last else None), primary=bool(_mm_last))
            use menu_main_button(_("Start Game"), "sparkle", Start(), primary=not _mm_last)
            use menu_main_button(_("Load Game"), "load", ShowMenu("load"))
            use menu_main_button(_("Preferences"), "gear", ShowMenu("preferences"))
            use menu_main_button(_("Achievements"), "star", ShowMenu("achievements_viewer"))
            use menu_main_button(_("Credits"), "heart", ShowMenu("credits_screen"))
            null height 4
            use menu_main_button(_("Quit"), "power", Show("quit_screen"))

    text ("v" + config.version):
        style "menu_brand_version"
        xalign 1.0
        yalign 1.0
        xoffset -20
        yoffset -12


##############################################################################
# NAVIGATION: the menu column of the game menu screens (save / load / preferences / achievements / credits)
##############################################################################

screen navigation():

    add menu_backdrop_image()

    frame:
        style "menu_column"

        vbox:
            spacing 4

            # the game's name and version on top
            vbox:
                xpos 20
                spacing 2
                text config.name.upper() style "menu_brand"
                text ("v" + config.version) style "menu_brand_version"

            null height 24

            # Same order as the main menu (Load before Preferences; player report 2026-10-09), and the
            # entries that make no sense FROM the main menu (saving, going to it) hide there instead of
            # graying out (this column also serves the main menu's load / preferences screens)
            use menu_nav_button(_("Return"), "back", Return())
            if not main_menu:
                use menu_nav_button(_("Save Game"), "save", ShowMenu("save"))
            use menu_nav_button(_("Load Game"), "load", ShowMenu("load"))
            use menu_nav_button(_("Preferences"), "gear", ShowMenu("preferences"))
            use menu_nav_button(_("Achievements"), "star", ShowMenu("achievements_viewer"))
            use menu_nav_button(_("Credits"), "heart", ShowMenu("credits_screen"))
            if not main_menu:
                use menu_nav_button(_("Main Menu"), "home", MainMenu())

        vbox:
            yalign 1.0
            use menu_nav_button(_("Quit"), "power", Show("quit_screen"))


##############################################################################
# SAVE / LOAD
##############################################################################
# Save and load draw the same screen (file_slots): FileAction(i) saves on the save screen and loads on the
# load screen. A card is the save's own thumbnail plus what file_slot_view says about it; the screen only draws.

init python:
    FILE_PAGE_BUTTONS = 8                       # numbered page buttons on screen
    FILE_SLOTS = 9                              # cards per page (3 x 3), the width of the menu panel
    FILE_CARD_W, FILE_CARD_H = 440, 248         # 16:9, like the thumbnails (config.thumbnail_*, gui.rpy)
    FILE_CARD_EDGE = 3                          # the border around a card's picture
    FILE_THUMB_W = FILE_CARD_W - 2 * FILE_CARD_EDGE
    FILE_THUMB_H = FILE_CARD_H - 2 * FILE_CARD_EDGE
    FILE_SMALL_THUMB = (270, 180)               # an old save's 180x120 thumbnail at 1.5x, never bigger

    def file_page_window(current):
        """The block of FILE_PAGE_BUTTONS pages that holds the current page (1-8, 9-16, 17-24...), so the
        page reached with the arrows is always on screen and highlighted."""
        _first = ((max(1, int(current)) - 1) // FILE_PAGE_BUTTONS) * FILE_PAGE_BUTTONS + 1
        return range(_first, _first + FILE_PAGE_BUTTONS)

    def file_newest_page():
        """Page of the newest save the player made on a numbered page: the save FileNewest marks (auto and
        quick saves have their own tabs). None when there is none."""
        _slot = renpy.newest_slot(r"\d+")
        return _slot.split("-", 1)[0] if _slot else None

    def file_screen_view():
        """Page state of the save / load screen: the numbered page on screen (None on Auto / Quick), its
        block of page buttons, and the page of the newest save ("Find my latest save" and its dot)."""
        _page = str(persistent._file_page or "1")
        _num = int(_page) if _page.isdigit() else None
        return {"num": _num, "window": file_page_window(_num or 1), "newest_page": file_newest_page(),
                "newest_dot": Transform(_pk_tint(_PK_DISC, ROD_ACCENT_WARM), xysize=(6, 6), xalign=0.5, yalign=1.0,
                                        yoffset=-4)}

    def file_slot_view(i):
        """What the card of slot `i` of the current page shows. None = empty slot."""
        if not FileLoadable(i):
            return None
        _json = FileJson(i) or {}
        _day, _time = _json.get("_ct_day"), _json.get("_ct_time")
        _when = _icon = None
        # saves made before 0.12.1 do not carry the in-game time: their card only says when they were saved
        if isinstance(_day, int) and isinstance(_time, int) and 0 <= _time < len(TIME_NAMES):
            _period = TIME_NAMES[_time]
            _when = u" · ".join((_tr(WEEKDAY_NAMES[(_day - 1) % 7]), _tr("Day %d") % _day, _tr(_period)))
            _icon = TIME_ICONS.get(_period, "images/menus/AfternoonIcon.png")
        _version = _json.get("_version")
        # saves made before the width was stamped all have 180 px thumbnails
        _thumb_w = _json.get("_ct_thumb_w") or 180
        return {
            "number": FileSlotName(i, FILE_SLOTS, auto="A", quick="Q"),
            "saved": FileTime(i),
            "when": _when,
            "icon": _icon,
            "version": ("v%s" % _version) if _version else None,
            "newest": FileNewest(i),
            "small": _thumb_w < FILE_THUMB_W,
        }

    # Catmull-Rom (bicubic) sampling of tex0, 9 taps: an image drawn bigger than its pixels comes out sharper
    # than with the GPU's bilinear. Only for the small thumbnails of old saves (180x120 shown at 1.5x): on a
    # big texture a phone GPU without highp floats would sample it off by a fraction of a pixel.
    renpy.register_shader("ct.bicubic", variables="""
        uniform sampler2D tex0;
        uniform vec2 res0;
        varying vec2 v_tex_coord;
    """, fragment_functions="""
        vec4 ct_bicubic(sampler2D tex, vec2 uv, vec2 size) {
            vec2 pos = uv * size;
            vec2 p1 = floor(pos - 0.5) + 0.5;
            vec2 f = pos - p1;
            vec2 w0 = f * (-0.5 + f * (1.0 - 0.5 * f));
            vec2 w1 = 1.0 + f * f * (-2.5 + 1.5 * f);
            vec2 w2 = f * (0.5 + f * (2.0 - 1.5 * f));
            vec2 w3 = f * f * (-0.5 + 0.5 * f);
            vec2 w12 = w1 + w2;
            vec2 p0 = (p1 - 1.0) / size;
            vec2 p3 = (p1 + 2.0) / size;
            vec2 p12 = (p1 + w2 / w12) / size;
            vec4 c = texture2D(tex, vec2(p0.x, p0.y)) * w0.x * w0.y
                + texture2D(tex, vec2(p12.x, p0.y)) * w12.x * w0.y
                + texture2D(tex, vec2(p3.x, p0.y)) * w3.x * w0.y
                + texture2D(tex, vec2(p0.x, p12.y)) * w0.x * w12.y
                + texture2D(tex, vec2(p12.x, p12.y)) * w12.x * w12.y
                + texture2D(tex, vec2(p3.x, p12.y)) * w3.x * w12.y
                + texture2D(tex, vec2(p0.x, p3.y)) * w0.x * w3.y
                + texture2D(tex, vec2(p12.x, p3.y)) * w12.x * w3.y
                + texture2D(tex, vec2(p3.x, p3.y)) * w3.x * w3.y;
            return clamp(c, 0.0, 1.0);
        }
    """, fragment_300="""
        gl_FragColor = ct_bicubic(tex0, v_tex_coord.xy, res0);
    """)

    def file_thumb(i, bar_h, small):
        """Slot i's thumbnail on a card (round corners), with the dark bar (bar_h tall) the card's text sits on.
        A thumbnail as big as the card (saves from 0.12.1 on) fills it, cropped to the card. A `small` one (older
        saves: 180x120, 3:2) blown up to the card came out pixelated: it keeps its shape at up to 1.5x (the old
        screen showed it at 1.33x), bicubic, over a blurred copy of itself that fills the card."""
        _shot = FileScreenshot(i)
        _w, _h = FILE_THUMB_W, FILE_THUMB_H
        if small:
            _layers = [
                Solid("#0b1220"),
                Transform(_shot, fit="cover", xysize=(_w, _h), align=(0.5, 0.5), blur=24,
                          matrixcolor=BrightnessMatrix(-0.2)),
                Fixed(AlphaMask(Transform(_shot, fit="contain", xysize=FILE_SMALL_THUMB, shader="ct.bicubic"),
                                _pk_pill("#ffffff"), align=(0.5, 0.5)),
                      xysize=(_w, _h - bar_h)),
            ]
        else:
            _layers = [Transform(_shot, fit="cover", xysize=(_w, _h), align=(0.5, 0.5))]
        _layers.append(Transform(Solid("#050b16d0"), xysize=(_w, bar_h), yalign=1.0))
        return AlphaMask(Fixed(*_layers, xysize=(_w, _h)), _pk_pill("#ffffff"))

    def _file_stamp_json(d):
        """Save json, for the save's card: the thumbnail width it was saved with, the in-game day and period."""
        d["_ct_thumb_w"] = config.thumbnail_width
        try:
            d["_ct_day"] = int(store.Day)
            d["_ct_time"] = int(store.TimeIndex)
        except Exception as _e:
            print("[SAVE] in-game time not stamped on the save: %r" % (_e,))

    config.save_json_callbacks.append(_file_stamp_json)


screen save():

    tag menu

    use file_slots(_("SAVE GAME"), True)


screen load():

    tag menu

    use file_slots(_("LOAD GAME"), False)


screen file_slots(title, saving):

    use navigation

    $ _fs_view = file_screen_view()

    use menu_panel():

        vbox:
            spacing 20

            # ── Title + the jump to the page of the newest save ──
            use menu_header(title):
                button:
                    style "file_latest_button"
                    action (FilePage(_fs_view["newest_page"]) if _fs_view["newest_page"] else None)

                    hbox:
                        spacing 10
                        yalign 0.5

                        add _pk_icon("star", ROD_ACCENT_WARM if _fs_view["newest_page"] else "#4a5a6c") yalign 0.5
                        text _("Find my latest save") style "file_latest_button_text"

            # ── Pages: Auto / Quick, then the numbered block and its arrows (10 pages / 1 page) ──
            hbox:
                spacing 6

                textbutton _("Auto") style "menu_option_button" action FilePage("auto")
                textbutton _("Quick") style "menu_option_button" action FilePage("quick")

                null width 10
                add Solid("#ffffff1c") xysize (2, 26) yalign 0.5
                null width 10

                # the double arrows jump exactly ONE window of page buttons (FILE_PAGE_BUTTONS, the 8 numbers
                # on screen): a 10-page jump used to land two sets away and confuse (player report 2026-10-09)
                textbutton "«":
                    style "file_arrow_button"
                    action FilePage(max(1, (_fs_view["num"] or 1) - FILE_PAGE_BUTTONS))
                    sensitive (_fs_view["num"] or 1) > FILE_PAGE_BUTTONS
                    selected False
                textbutton "‹" style "file_arrow_button" action FilePagePrevious()

                for _p in _fs_view["window"]:
                    button:
                        style "file_page_button"
                        action FilePage(_p)
                        # the page that holds the newest save gets a gold dot
                        foreground (_fs_view["newest_dot"] if str(_p) == _fs_view["newest_page"] else None)

                        text str(_p) style "file_page_button_text"

                textbutton "›" style "file_arrow_button" action FilePageNext()
                textbutton "»" style "file_arrow_button" action FilePage((_fs_view["num"] or 1) + FILE_PAGE_BUTTONS)

            # ── 3 x 3 cards ──
            grid 3 3:
                xspacing 22
                yspacing 18

                for i in range(1, FILE_SLOTS + 1):
                    use file_card(i, saving)


screen file_card(i, saving):

    $ _fs_card = file_slot_view(i)

    fixed:
        xysize (FILE_CARD_W, FILE_CARD_H)

        if _fs_card:
            button:
                style "file_card_button"
                action FileAction(i)

                add file_thumb(i, 62 if _fs_card["when"] else 40, _fs_card["small"])

                # chips: slot number, the newest save
                hbox:
                    pos (10, 10)
                    spacing 6

                    frame:
                        style "file_chip"
                        text _fs_card["number"] style "file_chip_text"

                    if _fs_card["newest"]:
                        frame:
                            style "file_chip"
                            background _pk_pill(ROD_ACCENT_WARM)

                            hbox:
                                spacing 5
                                add _pk_icon("star", "#1c1405") yalign 0.5
                                text _("LATEST") style "file_chip_text" color "#1c1405"

                # in-game day and period, then when it was saved; the game version it was saved in on the right
                vbox:
                    xpos 14
                    yalign 1.0
                    yoffset -9
                    spacing 1

                    if _fs_card["when"]:
                        hbox:
                            spacing 8
                            add _fs_card["icon"] xysize (26, 26) yalign 0.5
                            text _fs_card["when"] style "file_card_title" yalign 0.5
                        text _fs_card["saved"] style "file_card_sub"
                    else:
                        text _fs_card["saved"] style "file_card_title"

                if _fs_card["version"]:
                    text _fs_card["version"] style "file_card_version"

                key "save_delete" action FileDelete(i)

            # delete: a button of its own over the card (the topmost button under the mouse takes the focus)
            textbutton "×":
                style "file_delete_button"
                action FileDelete(i)

        else:
            button:
                style "file_card_button"
                action FileAction(i)

                add _pk_pill("#0f1a2b") xysize (FILE_THUMB_W, FILE_THUMB_H)

                vbox:
                    align (0.5, 0.5)

                    if saving:
                        text "+" style "file_empty_plus"
                    text _("Empty Slot") style "file_empty_text"


# init 1: after ROD_* (styles.rpy) and the phone kit's pill (screen_phone_kit.rpy); the panel, the title and
# the Auto / Quick tabs come from the menu kit (screen_menu_kit.rpy)
init 1:
    style file_latest_button is button:
        ysize 46
        padding (18, 0, 22, 0)
        background _pk_pill(ROD_ACCENT_WARM, 0.14)
        hover_background _pk_pill(ROD_ACCENT_WARM, 0.30)
        selected_background _pk_pill(ROD_ACCENT_WARM, 0.24)
        selected_hover_background _pk_pill(ROD_ACCENT_WARM, 0.34)
        insensitive_background _pk_pill("#ffffff", 0.04)

    style file_latest_button_text is text:
        font "fonts/WorkSans-Bold.ttf"
        size 20
        color ROD_ACCENT_WARM
        hover_color "#fde68a"
        insensitive_color "#4a5a6c"
        yalign 0.5

    style file_page_button is button:
        minimum (42, 42)                        # grows with the number (page 100+)
        padding (8, 0, 8, 0)
        yalign 0.5
        background None
        hover_background _pk_pill("#ffffff", 0.08)
        selected_background _pk_pill(ROD_ACCENT, 0.22)

    style file_page_button_text is text:
        font "fonts/WorkSans-SemiBold.ttf"
        size 20
        color ROD_TEXT_DIM
        hover_color "#ffffff"
        selected_color ROD_ACCENT
        xalign 0.5
        yalign 0.45

    style file_arrow_button is file_page_button:
        minimum (36, 42)
        padding (4, 0, 4, 0)
        hover_background None

    style file_arrow_button_text is button_text:
        font "fonts/WorkSans-Bold.ttf"
        size 28
        color ROD_TEXT_DIM
        hover_color ROD_ACCENT
        insensitive_color "#2a3a50"
        xalign 0.5
        yalign 0.5

    style file_card_button is button:
        xysize (FILE_CARD_W, FILE_CARD_H)
        padding (FILE_CARD_EDGE, FILE_CARD_EDGE, FILE_CARD_EDGE, FILE_CARD_EDGE)
        background _pk_pill("#ffffff", 0.10)
        hover_background _pk_pill(ROD_ACCENT)
        selected_background _pk_pill(ROD_ACCENT_WARM)
        selected_hover_background _pk_pill("#fde68a")
        insensitive_background _pk_pill("#ffffff", 0.05)
        hover_foreground _pk_pill("#ffffff", 0.06)

    style file_chip is frame:
        background _pk_pill("#050b16", 0.80)
        padding (10, 3, 10, 3)
        xmargin 0
        ymargin 0
        yalign 0.5

    style file_chip_text is text:
        font "fonts/WorkSans-Bold.ttf"
        size 15
        color "#e2e8f0"
        yalign 0.5

    style file_card_title is text:
        font "fonts/WorkSans-SemiBold.ttf"
        size 18
        color "#f1f5f9"

    style file_card_sub is text:
        font "fonts/WorkSans-Medium.ttf"
        size 15
        color "#94a3b8"

    style file_card_version is text:
        font "fonts/WorkSans-Medium.ttf"
        size 14
        color "#64748b"
        xalign 1.0
        yalign 1.0
        xoffset -14
        yoffset -11

    style file_delete_button is button:
        xysize (34, 34)
        padding (0, 0, 0, 0)
        xalign 1.0
        xoffset -10
        ypos 10
        background _pk_pill("#050b16", 0.72)
        hover_background _pk_pill("#dc2626", 0.95)

    style file_delete_button_text is button_text:
        font "fonts/WorkSans-SemiBold.ttf"
        size 26
        color "#cbd5e1"
        hover_color "#ffffff"
        xalign 0.5
        yalign 0.5
        yoffset -2

    style file_empty_plus is text:
        font "fonts/WorkSans-Medium.ttf"
        size 56
        color "#2f4257"
        hover_color ROD_ACCENT
        xalign 0.5

    style file_empty_text is text:
        font "fonts/WorkSans-SemiBold.ttf"
        size 18
        color "#4a6078"
        hover_color ROD_TEXT
        insensitive_color "#33455a"
        xalign 0.5


##############################################################################
# PREFERENCES
##############################################################################

screen preferences():

    tag menu

    use navigation

    use menu_panel():

        vbox:
            spacing 22

            use menu_header(_("PREFERENCES"))

            hbox:
                spacing 24

                # ── left: display, language, text ──
                vbox:
                    xsize (MENU_INNER_W - 24) // 2
                    spacing 18

                    use menu_card():
                        vbox:
                            spacing 24
                            use menu_setting(_("Display")):
                                textbutton _("Window") style "menu_option_button" action Preference("display", "window")
                                textbutton _("Fullscreen") style "menu_option_button" action Preference("display", "fullscreen")
                            # Side-menu size (apply_menu_scale, styles.rpy): Small is the default
                            # everywhere; Large is the opt-in touch layout that covers half the scene
                            use menu_setting(_("Menu Size")):
                                textbutton _("Small") style "menu_option_button" action [SetField(persistent, "menu_scale", "small"), Function(apply_menu_scale, rebuild=True)]
                                textbutton _("Large") style "menu_option_button" action [SetField(persistent, "menu_scale", "large"), Function(apply_menu_scale, rebuild=True)]
                            use menu_setting(_("Transitions")):
                                textbutton _("All") style "menu_option_button" action Preference("transitions", "all")
                                textbutton _("None") style "menu_option_button" action Preference("transitions", "none")
                            use menu_setting(_("Language")):
                                textbutton "English" style "menu_option_button" action Language(None)
                                textbutton "Português" style "menu_option_button" action Language("pt")
                                textbutton "Español" style "menu_option_button" action Language("es")
                                # tl/ru/fonts swaps Work Sans for Inter in Russian; the button needs Inter in every language
                                textbutton "Русский" style "menu_option_button" text_font "fonts/Inter-SemiBold.ttf" action Language("ru")

                    use menu_card():
                        vbox:
                            spacing 24
                            use menu_setting(_("Text Speed")):
                                bar value Preference("text speed") style "menu_slider"
                            use menu_setting(_("Auto-Forward Time")):
                                bar value Preference("auto-forward time") style "menu_slider"

                # ── right: sound, skipping, achievements ──
                vbox:
                    xsize (MENU_INNER_W - 24) // 2
                    spacing 18

                    use menu_card():
                        vbox:
                            spacing 24
                            use menu_setting(_("Music Volume")):
                                bar value Preference("music volume") style "menu_slider"
                            use menu_setting(_("Sound & Notifications")):
                                bar value Preference("sound volume") style "menu_slider"

                    use menu_card():
                        vbox:
                            spacing 24
                            use menu_setting(_("Skip")):
                                textbutton _("Seen Messages") style "menu_option_button" action Preference("skip", "seen")
                                textbutton _("All Messages") style "menu_option_button" action Preference("skip", "all")
                            use menu_setting(_("After Choices")):
                                textbutton _("Stop Skipping") style "menu_option_button" action Preference("after choices", "stop")
                                textbutton _("Keep Skipping") style "menu_option_button" action Preference("after choices", "skip")

                    use menu_card():
                        use menu_setting(_("Achievements")):
                            textbutton _("Clear All Achievements") style "menu_danger_button" action Confirm(
                                _("Are you sure you want to clear all achievements?\nThis cannot be undone."),
                                yes=Function(clear_all_achievements),
                            )


##############################################################################
# QUICK MENU
##############################################################################

screen quick_menu():

    frame:
        background _pk_pill(MENU_GROUND, 0.86)
        xalign 0.5
        yalign 0.988
        padding (10, 6, 10, 6)

        hbox:
            style_prefix "quick"
            spacing 2

            textbutton _("BACK") action Rollback()
            textbutton _("SAVE") action ShowMenu('save')
            textbutton _("QSAVE") action QuickSave()
            textbutton _("QLOAD") action QuickLoad()
            textbutton _("SKIP") action Skip()
            textbutton _("SKIP+") action Skip(fast=True, confirm=True)
            textbutton _("AUTO") action Preference("auto-forward", "toggle")
            textbutton _("PREFS") action ShowMenu('preferences')


init -2:
    style world_action_button is button:
        xminimum 220
        xmaximum 220
        background "#0b1220cc"
        hover_background "#1f2a44dd"
        selected_background "#2b3554dd"
        xalign 0.0
        xpadding 12
        ypadding 8

    style world_action_button_text is button_text:
        size 18
        color "#e5e7eb"
        hover_color "#ffffff"
        selected_color "#ffd166"
        outlines [(2, "#0b0f17", 0, 0)]
        xalign 0.0

init python:
    def get_bubble_side_for_talker(who):
        """
        Decide which side the speech bubble should be on
        based on which girl is talking and which girls are on screen.

        Returns: "left", "center", or "right".
        """
        from store import girls_on_scene  # usa a função que você já tem

        # Lista de garotas na cena, na ordem em que foram posicionadas
        girls_here = girls_on_scene()

        if not girls_here:
            return "center"

        # Tenta casar o nome do personagem com o objeto Girl
        for idx, g in enumerate(girls_here):
            g_name = getattr(g, "Name", None)
            g_gid  = getattr(g, "gid", None)

            if who == g_name or who == (g_gid.capitalize() if g_gid else None):
                # 1 garota -> centro
                if len(girls_here) == 1:
                    return "center"

                # 2+ garotas -> primeira à esquerda, segunda à direita
                if idx == 0:
                    return "left"
                elif idx == 1:
                    return "right"

        # Se não achou, usa centro
        return "center"


screen stat_popup(text_value, color, xpos):

    zorder 250

    frame:
        background None
        xalign xpos
        yalign 0.35

        text text_value:
            color color
            outlines [(2, "#000000", 0, 0)]
            size 26
            at stat_popup_move

    timer 1.6 action Hide("stat_popup")


transform stat_popup_move:
    on show:
        alpha 1.0
        yoffset 0
        pause 0.9
        linear 0.7 yoffset -40 alpha 0.0
    on hide:
        alpha 0.0


transform stat_popup_motion:
    alpha 0.0 yoffset 15
    linear 0.15 alpha 1.0 yoffset 0


init:

    screen StatHolder(value=0, prefix="+", color="#ffffff", xpos=0.75, ypos=0.25, label_text="", hide_tag="StatHolder"):
        # Popup de status tipo "Love -80" com contagem 0..value

        zorder 500
        default cur = 0
        default _step = max(1, (value + 65) // 66)

        frame:
            at stat_popup_motion
            background None
            xpos int(1920 * (xpos if xpos is not None else 0.75))
            xanchor 0.5
            yalign ypos

            hbox:
                spacing 4
                if label_text:
                    text "[label_text] ":
                        color color
                        size 22
                        outlines [(1, "#000000", 0, 0)]
                        bold True
                text "[prefix][cur]":
                    color color
                    size 26
                    outlines [(1, "#000000", 0, 0)]
                    bold True

        # Timer para contar 0 -> value (max 2s para qualquer valor)
        timer 0.03 repeat True action If(
            cur < value,
            SetScreenVariable("cur", min(cur + _step, value))
        )

        # Timer para remover (minimo 3s na tela)
        timer 3.5 action Hide(hide_tag)


##############################################################################
# CONFIRM: overwrite / delete a save, main menu, clear achievements...
##############################################################################
screen confirm(message, yes_action, no_action):

    modal True
    zorder 999

    add "#000000b8"

    use menu_dialog():
        text _(message) style "menu_dialog_text"

        hbox:
            xalign 0.5
            spacing 18
            textbutton _("Yes") style "menu_primary_button" action yes_action
            textbutton _("No") style "menu_secondary_button" action no_action

    key "game_menu" action no_action


##############################################################################
# QUIT: a word about the game and where to follow it, then quit or stay
##############################################################################
screen quit_screen():
    modal True
    zorder 200

    add "#000000b8"

    use menu_dialog():
        text _("What did you think of the game?") style "menu_dialog_title"

        vbox:
            xalign 0.5
            spacing 8
            text _("Follow us for updates and support the game!") style "menu_dialog_note"
            text _("Vote on the next girl and suggest new mechanics on Patreon or SubscribeStar!") style "menu_dialog_note" color ROD_ACCENT_WARM

        hbox:
            xalign 0.5
            spacing 32

            imagebutton:
                idle Transform("images/menus/Patreon.png", zoom=0.11)
                hover Transform("images/menus/Patreon.png", zoom=0.11, matrixcolor=BrightnessMatrix(0.15))
                action OpenURL("https://patreon.com/RodProjectsDev")

            imagebutton:
                idle Transform("images/menus/SubscribeStar.png", zoom=0.11)
                hover Transform("images/menus/SubscribeStar.png", zoom=0.11, matrixcolor=BrightnessMatrix(0.15))
                action OpenURL("https://subscribestar.adult/rodprojects")

            imagebutton:
                idle Transform("images/menus/Discord.png", zoom=0.11)
                hover Transform("images/menus/Discord.png", zoom=0.11, matrixcolor=BrightnessMatrix(0.15))
                action OpenURL("https://discord.gg/SnzXf6z3Ke")

        hbox:
            xalign 0.5
            spacing 18
            textbutton _("Quit") style "menu_quit_button" action Quit(confirm=False)
            textbutton _("Stay") style "menu_secondary_button" action Hide("quit_screen")

    key "game_menu" action Hide("quit_screen")
