# ============================================================
# Phone UI kit: the look every phone screen shares
# ============================================================
# Born as the building blocks of the girl status screen (2026-09-19); the author asked for the same look on
# the other phone screens, so the blocks live here and every screen `use`s them:
#
#   pk_page()                                   dimmer + phone art; the screen's content is the block it is given
#   pk_hero(title, accent, avatar, initial)     big header: a face in a ring of `accent`, a name, and a second
#                                               line given by the caller (chips)
#   pk_header(title, accent, icon)              slim header of a list screen; the caller's block sits on the right
#   pk_tabs(tabs, current, accent, var, top)    tab bar; tabs = [(id, caption, icon)]
#   pk_scrollmark(vp_id, accent, top, tall)     thin scroll mark, only while the viewport scrolls
#   pk_card(title, accent, icon)                a titled card; its rows are the block it is given
#   pk_bar / pk_chip / pk_row / pk_box / pk_locked / pk_action
#   pk_chat_header(title, accent, faces, top)   header of a conversation: faces in rings, a name, a caption
#   pk_tile(label, icon, color, action, ...)    one action of a chat menu (grid of tiles)
#   pk_answer(label, action, enabled)           one answer he can give in a chat
#   transform pk_pulse                          "this can be tapped": a slow breath
#
# Art = WHITE pngs tinted at runtime (images/menus/status/, generator: docs/tools/make_status_assets.py).
# Used screens take EXPRESSIONS (text title), never "[title]": late substitution in a used screen can run in
# the parent scope, where the local name is gone (NameError in Ren'Py 8.4, see girl_status_hud).
# init -4: after PH_CW (init -5, screen_status.rpy), before the screens' own view code (init -3).

init -4 python:

    _PK_ART = "images/menus/status/"
    _PK_PILL = _PK_ART + "pill.png"
    _PK_BAR = _PK_ART + "bar.png"
    _PK_LOCK = _PK_ART + "lock.png"
    _PK_RING = _PK_ART + "ring.png"
    _PK_DISC = _PK_ART + "disc.png"
    _PK_GLOW = _PK_ART + "hero_glow.png"
    _PK_CARD = "images/menus/bigfans/card_bg_small.png"
    _PK_BOX = "images/menus/bigfans/stat_box.png"
    _PK_MUTED = "#8ca0b4"
    _PK_TEXT = "#e2e8f0"
    _PK_DIM = "#555e6e"
    _PK_GROUND = "#0f172a"                  # header ground
    _PK_CARD_W = PH_CW - 16                 # a card
    _PK_INNER_W = _PK_CARD_W - 32           # what fits inside its padding
    _PK_LABEL_W = 58                        # the word in front of a bar
    _PK_HERO_H = 118
    _PK_HEADER_H = 64
    _PK_TABS_H = 46

    def _pk_tint(image, color, alpha=1.0):
        """White art tinted to `color`."""
        return Transform(image, matrixcolor=TintMatrix(color), alpha=alpha)

    def _pk_pill(color, alpha=1.0):
        """The white 9-slice pill tinted to `color` (chips, the active-tab mark, icon plates)."""
        return Frame(_pk_tint(_PK_PILL, color, alpha), 14, 14)

    def _pk_bar_art(color):
        """The 12 px tall pill of a bar (track or fill) in `color`: it only stretches sideways."""
        return Frame(_pk_tint(_PK_BAR, color), 6, 0)

    def _pk_card_bg(flash=None):
        """The card ground of a list row; `flash` = a color it is washed with for a moment (just bought)."""
        if flash:
            return Frame(Transform(_PK_CARD, matrixcolor=TintMatrix(flash) * BrightnessMatrix(0.25)), 16, 16, 16, 16)
        return Frame(_PK_CARD, 16, 16, 16, 16)

    def _pk_icon(name, color):
        """A 20x20 icon of images/menus/status/ic_<name>.png in `color`."""
        return _pk_tint(_PK_ART + "ic_%s.png" % name, color)

    def _pk_face(image, size=84):
        """Any avatar art scaled to a `size` px face (the girls' art is 75 px, the NPC default is bigger)."""
        return Transform(image, xysize=(size, size), fit="contain")

    def _pk_bar_w(value, vmax, width):
        """Fill width of a bar `width` wide. Never narrower than the pill's round ends unless it is empty."""
        if value <= 0 or vmax <= 0:
            return 0
        return max(12, int(width * min(value, vmax) / float(vmax)))

    def _pk_t(text):
        """A display word through both translation tables: the tl pairs first, then _I18N. For words that
        end up INSIDE a bigger string (a whole string given to a text is looked up by the text itself)."""
        _t = _tl(text)
        return _t if _t != text else _tr(text)

    def _pk_borrow(template, part=0):
        """One side of an old "Head: value" line of the tl files, in the current language, text tags dropped.
        The phone screens used to be text lines ("Kisses: [_kiss_count]"); those pairs exist in PT / ES, so
        the word comes out translated without a new pair. A translation that lost its colon (or kept a
        [placeholder] on that side) falls back to the English word: never a raw placeholder on screen."""
        import re
        def _side(_s):
            if ":" not in _s:
                return None
            _w = re.sub(r"\{[^}]*\}", "", _s.split(":", 1)[part]).strip()
            return _w if (_w and "[" not in _w) else None
        return _side(_tl(template)) or _side(template) or template.replace(":", "").strip()

    def _pk_scroll_top(screen, vp_id):
        """Another tab starts at its top."""
        _vp = renpy.get_widget(screen, vp_id)
        if _vp is not None:
            _vp.yadjustment.change(0)

    # ---------------------------------------------------------------- tier words shared by the status screens:
    # first row whose minimum the value reaches -> (label, color)
    _PK_TIERS = {
        "study":    [(10, "Very prepared", "#4ade80"), (7, "Well studied", "#86efac"), (5, "Somewhat prepared", "#facc15"),
                     (3, "Barely studied", "#fb923c"), (None, "Hasn't studied at all", "#f87171")],
        "player_study": [(10, "Very prepared", "#4ade80"), (7, "Well studied", "#86efac"), (5, "Somewhat prepared", "#facc15"),
                         (3, "Barely studied", "#fb923c"), (None, "Hasn't studied", "#f87171")],
        "strength": [(5, "Athlete", "#22d3ee"), (4, "Strong", "#4ade80"), (3, "Fit", "#86efac"), (2, "Average", "#fbbf24"), (None, "Weak", "#f87171")],
        "friends":  [(800, "Best Friends", "#4ade80"), (500, "Friends", "#a3e635"), (200, "Acquaintances", "#fbbf24"), (None, "Hostile", "#f87171")],
        "npc_bond": [(500, "Friendly", "#4ade80"), (200, "Neutral", "#fbbf24"), (None, "Hostile", "#f87171")],
        "npc_love": [(700, "In love", "#f472b6"), (400, "Moderate", "#fbbf24"), (None, "Low", "#f87171")],
        "npc_susp": [(80, "Very suspicious", "#ef4444"), (50, "Suspicious", "#fb923c"), (20, "Uneasy", "#fbbf24"), (None, "Unaware", "#4ade80")],
        "spectrum": [(76, None, "#e879f9"), (26, None, "#c084fc"), (None, None, "#60a5fa")],
    }

    def _pk_tier(table, value):
        """(translated label, color) of `value` in _PK_TIERS[table]."""
        for _min, _label, _color in _PK_TIERS[table]:
            if _min is None or value >= _min:
                return (_tr(_label) if _label else None), _color


style pk_vscrollbar is vscrollbar:
    xsize 4
    base_bar Solid("#ffffff14")
    thumb_offset 0
    unscrollable "hide"


# ------------------------------------------------------------ page, headers, tabs, scroll mark
screen pk_page():
    button:
        xfill True
        yfill True
        background "#00000088"
        action NullAction()

    frame:
        xpos PH_X
        ypos PH_Y
        background None
        padding (0, 0)

        fixed:
            fit_first True
            add _phone_img
            transclude

screen pk_hero(title, accent, avatar=None, initial=None):
    frame:
        xpos PH_CX
        ypos PH_CY_HEADER
        xsize PH_CW
        ysize _PK_HERO_H
        padding (0, 0)
        background _PK_GROUND

        add _pk_tint(_PK_GLOW, accent, 0.55)

        frame:
            xsize PH_CW
            ysize 4
            padding (0, 0)
            background accent

        hbox:
            xpos 16
            yalign 0.58
            spacing 16

            fixed:
                xsize 92
                ysize 92
                yalign 0.5
                add _pk_tint(_PK_RING, accent)
                if avatar:
                    add _pk_face(avatar) align (0.5, 0.5)
                else:
                    add _pk_tint(_PK_DISC, "#1e293b") align (0.5, 0.5)
                    text (initial or "?"):
                        style "phone_text"
                        size 40
                        bold True
                        color accent
                        align (0.5, 0.5)

            vbox:
                yalign 0.5
                spacing 8
                text title:
                    style "phone_text"
                    size 30
                    bold True
                    color "#ffffff"
                transclude

screen pk_header(title, accent, icon=None):
    frame:
        xpos PH_CX
        ypos PH_CY_HEADER
        xsize PH_CW
        ysize _PK_HEADER_H
        padding (0, 0)
        background _PK_GROUND

        add Transform(_pk_tint(_PK_GLOW, accent, 0.45), crop=(0, 0, PH_CW, _PK_HEADER_H))

        frame:
            xsize PH_CW
            ysize 4
            padding (0, 0)
            background accent

        hbox:
            xpos 18
            yalign 0.58
            spacing 10
            if icon:
                frame:
                    xsize 34
                    ysize 34
                    yalign 0.5
                    padding (0, 0)
                    background _pk_pill(accent, 0.18)
                    add _pk_icon(icon, accent) align (0.5, 0.5)
            text title:
                style "phone_text"
                size 24
                bold True
                color "#ffffff"
                yalign 0.5

        hbox:
            xalign 1.0
            xoffset -16
            yalign 0.58
            transclude

# tabs = [(id, caption already translated, icon)]; `var` = the screen variable that holds the current id
screen pk_tabs(tabs, current, accent, var, top, vp_screen=None, vp_id=None):
    frame:
        xpos PH_CX
        ypos top
        xsize PH_CW
        ysize _PK_TABS_H
        padding (0, 0)
        background "#0b1220"
        hbox:
            for _pk_id, _pk_cap, _pk_ic in tabs:
                button:
                    xsize int(PH_CW / len(tabs))
                    ysize _PK_TABS_H
                    padding (0, 0)
                    background None
                    hover_background "#ffffff0a"
                    action [SetScreenVariable(var, _pk_id), Function(_pk_scroll_top, vp_screen, vp_id)]
                    hbox:
                        xalign 0.5
                        yalign 0.42
                        spacing 7
                        add _pk_icon(_pk_ic, (accent if current == _pk_id else _PK_MUTED)) yalign 0.5
                        text _pk_cap:
                            style "phone_text"
                            size 16
                            bold True
                            kerning 1.0
                            color (accent if current == _pk_id else _PK_MUTED)
                            yalign 0.5
                    if current == _pk_id:
                        frame:
                            xsize 64
                            ysize 4
                            xalign 0.5
                            yalign 1.0
                            padding (0, 0)
                            background _pk_pill(accent)

# thin scroll mark in `accent`, only when the viewport is taller than the phone
screen pk_scrollmark(vp_id, accent, top, tall):
    vbar:
        style "pk_vscrollbar"
        value YScrollValue(vp_id)
        thumb Solid(accent)
        xpos PH_CX + PH_CW - 5
        ypos top
        ysize tall


# ------------------------------------------------------------ cards and what goes in them
screen pk_card(title, accent="#60a5fa", icon=None):
    frame:
        xsize _PK_CARD_W
        xalign 0.5
        background Frame(_PK_CARD, 16, 16, 16, 16)
        padding (16, 12, 16, 14)
        vbox:
            spacing 10
            xfill True
            hbox:
                spacing 8
                if icon:
                    add _pk_icon(icon, accent) yalign 0.5
                text title:
                    style "phone_text"
                    size 15
                    bold True
                    kerning 1.2
                    color accent
                    yalign 0.5
            transclude

screen pk_bar(label, value, vmax, color, right_text, right_color="#e2e8f0", right_w=46, label_w=None):
    $ _pkb_lw = label_w or _PK_LABEL_W
    $ _pkb_w = _PK_INNER_W - _pkb_lw - 20 - right_w
    hbox:
        spacing 10
        text label:
            style "phone_text"
            size 16
            color _PK_MUTED
            min_width _pkb_lw
            yalign 0.5
        fixed:
            xsize _pkb_w
            ysize 12
            yalign 0.5
            frame:
                xsize _pkb_w
                ysize 12
                padding (0, 0)
                background _pk_bar_art("#1e293b")
            if _pk_bar_w(value, vmax, _pkb_w):
                frame:
                    xsize _pk_bar_w(value, vmax, _pkb_w)
                    ysize 12
                    padding (0, 0)
                    background _pk_bar_art(color)
        text right_text:
            style "phone_text"
            size 15
            color right_color
            min_width right_w
            text_align 1.0
            yalign 0.5

screen pk_chip(label, color, strike=False, count=None):
    frame:
        background _pk_pill(color, 0.16)
        padding (12, 5)
        hbox:
            spacing 8
            text ("{s}" + label + "{/s}" if strike else label):
                style "phone_text"
                size 15
                color color
            if count is not None:
                text str(count):
                    style "phone_text"
                    size 15
                    bold True
                    color "#ffffff"

screen pk_locked():
    hbox:
        spacing 8
        add _PK_LOCK yalign 0.5
        text "???":
            style "phone_text"
            size 16
            color _PK_DIM
            yalign 0.5

# A number with its caption. Every box is the same height; a long (translated) caption goes one size down to
# stay on one line, so the numbers of a row line up. Two lines remain possible as the last resort.
# The caption is WorkSans Medium: at 13 px the SemiBold of phone_text closes the gap between words.
screen pk_box(number, caption, color, box_w, icon=None):
    frame:
        xsize box_w
        ysize 88
        background Frame(_PK_BOX, 16, 16, 16, 16)
        padding (6, 8)
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 2
            hbox:
                xalign 0.5
                spacing 7
                if icon:
                    add _pk_icon(icon, color) yalign 0.5
                text number:
                    style "phone_text"
                    size 28
                    bold True
                    color color
                    yalign 0.5
            text caption:
                style "phone_text"
                font "fonts/WorkSans-Medium.ttf"
                size (13 if len(caption) <= 20 else 11)
                color _PK_MUTED
                xalign 0.5
                text_align 0.5
                xmaximum box_w - 16
                line_spacing -2

# One "label ..... value" line. value None = padlock, chip=True = the value sits in a chip, avatar = a face first,
# label_color = a name in its own color (a girl's).
screen pk_row(label, value, value_color="#e2e8f0", chip=False, avatar=None, label_color=None):
    hbox:
        xfill True
        hbox:
            spacing 10
            yalign 0.5
            if avatar:
                add _pk_face(avatar, 32) yalign 0.5
            text label:
                style "phone_text"
                size (17 if avatar else 16)
                color (label_color or (_PK_TEXT if avatar else _PK_MUTED))
                yalign 0.5
        hbox:
            xalign 1.0
            yalign 0.5
            if value is None:
                use pk_locked()
            elif chip:
                use pk_chip(value, value_color)
            else:
                text value:
                    style "phone_text"
                    size 16
                    color value_color

# One tappable line: icon plate, title, what it does, a chevron. enabled=False = dimmed and not clickable
# (the line stays on screen and says why: "Need her number first").
screen pk_action(icon, title, subtitle, accent, action, enabled=True):
    $ _pka_col = accent if enabled else _PK_DIM
    button:
        xsize _PK_CARD_W
        xalign 0.5
        sensitive enabled
        background Frame(_PK_CARD, 16, 16, 16, 16)
        hover_background Frame(Transform(_PK_CARD, matrixcolor=BrightnessMatrix(0.10)), 16, 16, 16, 16)
        padding (14, 12, 14, 12)
        action action
        hbox:
            xfill True
            hbox:
                spacing 14
                yalign 0.5
                frame:
                    xsize 46
                    ysize 46
                    yalign 0.5
                    padding (0, 0)
                    background _pk_pill(_pka_col, 0.16)
                    add _pk_icon(icon, _pka_col) align (0.5, 0.5)
                vbox:
                    yalign 0.5
                    spacing 3
                    text title:
                        style "phone_text"
                        size 19
                        bold True
                        color (_PK_TEXT if enabled else _PK_DIM)
                    if subtitle:
                        text subtitle:
                            style "phone_text"
                            font "fonts/WorkSans-Medium.ttf"
                            size 14
                            color (_PK_MUTED if enabled else _PK_DIM)
            add _pk_icon("next", (_PK_MUTED if enabled else "#2b3340")) xalign 1.0 yalign 0.5


# ------------------------------------------------------------ conversations
# "this can be tapped": a slow breath, for a control the player tends to miss
transform pk_pulse:
    alpha 1.0
    ease 0.55 alpha 0.30
    ease 0.55 alpha 1.0
    repeat

# the same control once it no longer needs to call for attention (a transform that ends the breath at full alpha)
transform pk_still:
    alpha 1.0

# faces = up to three avatar images (one girl, or the first members of a group)
screen pk_chat_header(title, accent, faces, top, caption=None, caption_color=None):
    frame:
        xpos PH_CX
        ypos top
        xsize PH_CW
        ysize _PK_HEADER_H
        padding (0, 0)
        background _PK_GROUND

        add Transform(_pk_tint(_PK_GLOW, accent, 0.45), crop=(0, 0, PH_CW, _PK_HEADER_H))

        frame:
            xsize PH_CW
            ysize 4
            padding (0, 0)
            background accent

        hbox:
            xpos 14
            yalign 0.60
            spacing 12
            hbox:
                spacing -14
                yalign 0.5
                for _pk_f in faces[:3]:
                    fixed:
                        xsize 48
                        ysize 48
                        add Transform(_pk_tint(_PK_RING, accent), xysize=(48, 48))
                        add _pk_face(_pk_f, 40) align (0.5, 0.5)
            vbox:
                yalign 0.5
                spacing 2
                text title:
                    style "phone_text"
                    size 21
                    bold True
                    color "#ffffff"
                if caption:
                    text caption:
                        style "phone_text"
                        font "fonts/WorkSans-Medium.ttf"
                        size 13
                        color (caption_color or _PK_MUTED)

# One action of a chat menu. enabled=False = dimmed and not clickable; `note` says why ("too late").
screen pk_tile(label, icon, color, action, enabled=True, note=None, width=160, height=78):
    $ _pkt_col = color if enabled else _PK_DIM
    button:
        xsize width
        ysize height
        sensitive enabled
        padding (4, 6, 4, 6)
        background _pk_card_bg()
        hover_background _pk_card_bg(color)
        action action
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 3
            frame:
                xsize 30
                ysize 30
                xalign 0.5
                padding (0, 0)
                background _pk_pill(_pkt_col, 0.18)
                add _pk_icon(icon, _pkt_col) align (0.5, 0.5)
            text label:
                style "phone_text"
                size 14
                bold True
                color (_PK_TEXT if enabled else _PK_DIM)
                xalign 0.5
                text_align 0.5
            if note:
                text note:
                    style "phone_text"
                    font "fonts/WorkSans-Medium.ttf"
                    size 11
                    color _PK_DIM
                    xalign 0.5
                    text_align 0.5

# One answer he can give (chat events). Full width, one per line.
screen pk_answer(label, action, enabled=True):
    button:
        xfill True
        ysize 46
        sensitive enabled
        padding (12, 0, 12, 0)
        background _pk_pill(("#3b82f6" if enabled else "#64748b"), (0.22 if enabled else 0.12))
        hover_background _pk_pill("#3b82f6", 0.40)
        action action
        text label:
            style "phone_text"
            size 17
            bold True
            color ("#ffffff" if enabled else _PK_DIM)
            xalign 0.5
            yalign 0.5
            text_align 0.5
