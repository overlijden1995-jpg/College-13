# ============================================================
# Menu kit: the look of every screen outside the game world
# ============================================================
# Main menu, the game menu (save / load / preferences / achievements / credits) and the dialogs share one
# look, drawn with the phone kit's white art tinted at runtime (_pk_pill, _pk_icon, _pk_tint in
# screen_phone_kit.rpy). Layout: the content panel on the left, the menu column (screen navigation,
# screens.rpy) on the right, both over menu_backdrop_image().
#
# screen menu_panel()                         the content panel; the block given goes inside
# screen menu_header(title)                   title row of a panel; the block given goes on its right
# screen menu_card()                          a rounded card inside a panel; the block given goes inside
# screen menu_setting(label)                  one setting of a card: its name, then the block given (the control)
# screen menu_nav_button(label, icon, action) a button of the menu column
# screen menu_main_button(label, icon, action, primary=False)   a button of the main menu
# screen menu_dialog()                        a modal card in the middle of the screen; the block given goes inside
# Used screens take EXPRESSIONS (text title), never "[title]" (screen_phone_kit.rpy says why).
# init -3: after the phone kit (-4); the styles are init 1, after ROD_* (styles.rpy, init -1).

init -3 python:

    MENU_MARGIN = 44                                    # screen edge to the panel and to the menu column
    MENU_TOP = 44
    MENU_H = config.screen_height - 2 * MENU_TOP
    MENU_PANEL_W = 1424
    MENU_PAD = 30                                       # inside the panel, left and right
    MENU_INNER_W = MENU_PANEL_W - 2 * MENU_PAD
    MENU_GAP = 24                                       # panel to menu column
    MENU_NAV_X = MENU_MARGIN + MENU_PANEL_W + MENU_GAP
    MENU_NAV_W = config.screen_width - MENU_MARGIN - MENU_NAV_X
    MENU_GROUND = "#0c1525"                             # panels, the menu column, dialogs
    MENU_CARD = "#1a2840"
    MENU_INK = "#06121f"                                # text on an accent-filled button
    MENU_ART = "images/menus/poll_homescreen.jpg"       # the main menu art
    # Rajdhani for Latin (the headline font of the menu art), Inter for everything it lacks (Cyrillic)
    MENU_CALL_FONT = FontGroup().add("fonts/Rajdhani-Bold.ttf", 0x0000, 0x024F).add("fonts/Inter-SemiBold.ttf", None, None)

    def _menu_blurred(image, darken):
        return Transform(image, fit="cover", xysize=(config.screen_width, config.screen_height), blur=36,
                         matrixcolor=BrightnessMatrix(-darken) * SaturationMatrix(0.75))

    def menu_backdrop_image():
        """What the menu screens sit on. In a game: the scene the menu was opened over (the thumbnail Ren'Py
        takes on the way in, the one a save gets), blurred and darkened. On the main menu, or when there is no
        thumbnail: the main menu art, the same way."""
        if not main_menu:
            # the attribute, never get_screenshot(): with none taken, that one would photograph the menu itself
            _png = getattr(renpy.game.interface, "screenshot", None)
            if _png:
                return _menu_blurred(im.Data(_png, "menu_backdrop.png"), 0.3)
        return _menu_blurred(MENU_ART, 0.08)                 # the art is dark already

    def _menu_track(color, alpha=1.0):
        """A 10 px tall rounded track, vertically centred in whatever height the bar gives it."""
        return Fixed(Transform(Frame(_pk_tint(_PK_BAR, color, alpha), 6, 0), ysize=10, yalign=0.5))

    def _menu_knob(color):
        return Transform(_pk_tint(_PK_DISC, color), xysize=(26, 26))


screen menu_panel():
    frame:
        style "menu_panel"
        transclude

screen menu_header(title):
    fixed:
        xfill True
        ysize 56
        # translated first, then upper case: every panel title in capitals, in any language
        text _tl(title).upper() style "menu_title"
        hbox:
            xalign 1.0
            yalign 0.5
            spacing 14
            transclude

screen menu_card():
    frame:
        style "menu_card"
        transclude

screen menu_setting(label):
    vbox:
        spacing 10
        text label style "menu_setting_label"
        hbox:
            spacing 8
            transclude

screen menu_nav_button(label, icon, action):
    button:
        style "menu_nav_button"
        action action
        hbox:
            spacing 16
            yalign 0.5
            add _pk_icon(icon, (ROD_ACCENT if renpy.is_selected(action) else ROD_TEXT_DIM)) zoom 1.1 yalign 0.5
            text label style "menu_nav_button_text"

screen menu_main_button(label, icon, action, primary=False):
    $ _live = action is not None and renpy.is_sensitive(action)
    button:
        style ("menu_main_primary" if primary else "menu_main_button")
        action action
        hbox:
            spacing 16
            yalign 0.5
            add _pk_icon(icon, ((MENU_INK if primary else ROD_ACCENT) if _live else "#4a5a6c")) zoom 1.2 yalign 0.5
            text label style ("menu_main_primary_text" if primary else "menu_main_button_text")

screen menu_dialog():
    frame:
        style "menu_dialog"
        vbox:
            xalign 0.5
            spacing 22
            transclude


init 1:
    # ---------------------------------------------------------------- panel, column, cards
    style menu_panel is frame:
        xpos MENU_MARGIN
        ypos MENU_TOP
        xysize (MENU_PANEL_W, MENU_H)
        padding (MENU_PAD, 26, MENU_PAD, 26)
        background _pk_pill(MENU_GROUND, 0.9)

    style menu_column is frame:
        xpos MENU_NAV_X
        ypos MENU_TOP
        xysize (MENU_NAV_W, MENU_H)
        padding (16, 30, 16, 22)
        background _pk_pill(MENU_GROUND, 0.9)

    style menu_card is frame:
        xfill True
        padding (24, 18, 24, 22)
        background _pk_pill(MENU_CARD, 0.7)

    style menu_main_frame is frame:
        xalign 0.955
        yalign 0.68
        xsize 440
        padding (22, 24, 22, 24)
        background _pk_pill(MENU_GROUND, 0.82)

    style menu_dialog is frame:
        xalign 0.5
        yalign 0.5
        xminimum 560
        xmaximum 920
        padding (52, 42, 52, 42)
        background _pk_pill("#101c30", 0.98)

    # ---------------------------------------------------------------- texts
    style menu_title is text:
        font "fonts/WorkSans-Bold.ttf"
        size 40
        color ROD_ACCENT
        outlines [(2, "#060d1a", 0, 0)]
        yalign 0.5

    style menu_subtitle is text:
        font "fonts/WorkSans-Medium.ttf"
        size 18
        color ROD_TEXT_DIM

    style menu_setting_label is text:
        font "fonts/WorkSans-Bold.ttf"
        size 17
        kerning 1
        color "#9fb3c8"

    style menu_brand is text:
        font "fonts/WorkSans-Bold.ttf"
        size 30
        kerning 1.5
        color ROD_TEXT

    style menu_brand_version is text:
        font "fonts/WorkSans-Medium.ttf"
        size 15
        color "#4a6a88"

    # the call to the polls beside the social icons on the main menu: the display font of the menu art
    # (Rajdhani has no Cyrillic: Inter takes those glyphs, MENU_CALL_FONT)
    style menu_social_call is text:
        font MENU_CALL_FONT
        size 34
        line_spacing -6
        color ROD_ACCENT_WARM
        text_align 1.0

    style menu_dialog_title is text:
        font "fonts/WorkSans-Bold.ttf"
        size 34
        color ROD_ACCENT
        xalign 0.5
        text_align 0.5

    style menu_dialog_text is text:
        font "fonts/WorkSans-SemiBold.ttf"
        size 28
        color ROD_TEXT
        xalign 0.5
        text_align 0.5

    style menu_dialog_note is menu_dialog_text:
        font "fonts/WorkSans-Medium.ttf"
        size 19
        color ROD_TEXT_DIM

    # ---------------------------------------------------------------- buttons
    # the menu column
    style menu_nav_button is button:
        xfill True
        ysize 54
        padding (20, 0, 16, 0)
        background None
        hover_background _pk_pill("#ffffff", 0.07)
        selected_background _pk_pill(ROD_ACCENT, 0.14)
        selected_hover_background _pk_pill(ROD_ACCENT, 0.2)

    style menu_nav_button_text is text:
        font "fonts/WorkSans-SemiBold.ttf"
        size 22
        color ROD_TEXT
        hover_color "#ffffff"
        selected_color ROD_ACCENT
        insensitive_color "#4a5a6c"
        yalign 0.5

    # the main menu
    style menu_main_button is button:
        xfill True
        ysize 58
        padding (24, 0, 18, 0)
        background _pk_pill("#ffffff", 0.05)
        hover_background _pk_pill("#ffffff", 0.13)
        insensitive_background _pk_pill("#ffffff", 0.03)

    style menu_main_button_text is text:
        font "fonts/WorkSans-SemiBold.ttf"
        size 24
        color ROD_TEXT
        hover_color "#ffffff"
        insensitive_color "#4a5a6c"
        yalign 0.5

    style menu_main_primary is menu_main_button:
        background _pk_pill(ROD_ACCENT, 0.95)
        hover_background _pk_pill("#bae6fd")
        insensitive_background _pk_pill("#ffffff", 0.05)

    style menu_main_primary_text is menu_main_button_text:
        font "fonts/WorkSans-Bold.ttf"
        color MENU_INK
        hover_color MENU_INK

    # a choice among a few (Window / Fullscreen, page tabs...): the chosen one is lit
    style menu_option_button is button:
        ysize 42
        padding (18, 0, 18, 0)
        yalign 0.5
        background _pk_pill("#ffffff", 0.06)
        hover_background _pk_pill("#ffffff", 0.13)
        selected_background _pk_pill(ROD_ACCENT, 0.24)
        selected_hover_background _pk_pill(ROD_ACCENT, 0.32)

    style menu_option_button_text is button_text:
        font "fonts/WorkSans-SemiBold.ttf"
        size 19
        color ROD_TEXT_DIM
        hover_color "#ffffff"
        selected_color ROD_ACCENT
        yalign 0.5

    style menu_danger_button is menu_option_button:
        background _pk_pill("#ef4444", 0.14)
        hover_background _pk_pill("#ef4444", 0.32)

    style menu_danger_button_text is menu_option_button_text:
        color "#fca5a5"
        hover_color "#ffffff"

    # dialog answers
    style menu_primary_button is button:
        minimum (180, 52)
        padding (28, 0, 28, 0)
        background _pk_pill(ROD_ACCENT, 0.95)
        hover_background _pk_pill("#bae6fd")

    style menu_primary_button_text is button_text:
        font "fonts/WorkSans-Bold.ttf"
        size 22
        color MENU_INK
        hover_color MENU_INK
        xalign 0.5
        yalign 0.5

    style menu_secondary_button is menu_primary_button:
        background _pk_pill("#ffffff", 0.09)
        hover_background _pk_pill("#ffffff", 0.18)

    style menu_secondary_button_text is menu_primary_button_text:
        color ROD_TEXT
        hover_color "#ffffff"

    style menu_quit_button is menu_primary_button:
        background _pk_pill("#ef4444", 0.92)
        hover_background _pk_pill("#f87171")

    style menu_quit_button_text is menu_primary_button_text:
        color "#ffffff"
        hover_color "#ffffff"

    # ---------------------------------------------------------------- bars
    style menu_slider is bar:
        xfill True
        ysize 26
        left_bar _menu_track(ROD_ACCENT)
        right_bar _menu_track("#ffffff", 0.1)
        thumb _menu_knob("#ffffff")
        hover_thumb _menu_knob("#bae6fd")
        thumb_offset 13
        left_gutter 0
        right_gutter 0

    style menu_progress is bar:
        ysize 12
        left_bar _menu_track(ROD_ACCENT_WARM)
        right_bar _menu_track("#ffffff", 0.1)
        thumb None
        thumb_offset 0
        left_gutter 0
        right_gutter 0

    style menu_vscrollbar is vscrollbar:
        xsize 6
        base_bar _pk_pill("#ffffff", 0.05)
        thumb _pk_pill(ROD_ACCENT, 0.5)
        hover_thumb _pk_pill(ROD_ACCENT, 0.8)
        thumb_offset 0
        unscrollable "hide"
