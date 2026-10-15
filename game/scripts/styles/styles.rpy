# styles.rpy
# ===========================
# Estilos usados no HUD e menus laterais
# ===========================

# Preferences > Menu Size: "small" / "large". Small everywhere by default (author 2026-10-11:
# the touch layout is gigantic on phones); "large" is the opt-in touch layout.
default persistent.menu_scale = "small"

init -1 python:

    # ----------------------------------
    # Shared UI palette
    # ----------------------------------
    ROD_ACCENT      = "#7dd3fc"   # sky blue – accent / hover
    ROD_ACCENT_WARM = "#fbbf24"   # gold – selected / highlight
    ROD_TEXT        = "#eef2f8"   # near-white
    ROD_TEXT_DIM    = "#8ca0b4"   # slate
    ROD_BG_DARK     = "#040b16"
    ROD_BG_SOFT     = "#09131ecc"
    ROD_BG_HOVER    = "#142233ee"
    ROD_BG_ACTIVE   = "#1a2d44ff"
    ROD_BORDER      = "#1e3c5a"

    # ----------------------------------
    # Stat colors — UI bars (phone, HUD)
    # ----------------------------------
    STAT_COLOR_LOVE = "#f472b6"   # pink
    STAT_COLOR_OBED = "#fb923c"   # orange
    STAT_COLOR_INBT = "#a78bfa"   # violet
    STAT_COLOR_LUST = "#ff9ad5"   # hot pink
    STAT_COLOR_TEMPTATION = "#c97bff"  # purple
    STAT_COLOR_HEAT = "#ff8c42"   # amber/orange
    STAT_COLOR_JEALOUSY = "#22d3ee"  # cyan/teal

    # ----------------------------------
    # Stat colors — popups (lighter for visibility over dark BG)
    # ----------------------------------
    STAT_POPUP_LOVE = "#ff6b81"   # brighter pink
    STAT_POPUP_OBED = "#4d7cff"   # brighter blue
    STAT_POPUP_INBT = "#ffe27a"   # bright yellow
    STAT_POPUP_LUST = "#ff9ad5"   # hot pink (same as UI)
    STAT_POPUP_TEMPTATION = "#c97bff"  # purple (same as UI)
    STAT_POPUP_JEALOUSY = "#22d3ee"        # cyan/teal (jealousy)
    STAT_POPUP_NPC_FRIENDSHIP = "#7ecbff"  # light blue (NPC friendship)
    STAT_POPUP_NPC_LOVE = "#ff9e5e"        # warm orange (NPC love for girl)
    STAT_POPUP_GIRL_FRIENDSHIP = "#7dffb0" # mint green (girl-to-girl friendship)

    # ----------------------------------
    # Helper: tinted card frame (replaces obsolete im.MatrixColor)
    # ----------------------------------
    def _card(brightness=0.0, corners=10):
        img = Transform("images/menus/GirlsCard_Blue.png",
                        matrixcolor=BrightnessMatrix(brightness))
        return Frame(img, corners, corners, corners, corners, tile=True)

    # ----------------------------------
    # SIDE MENU FRAME (choice card)
    # ----------------------------------
    style.SideMenuFrame = Style(style.default)
    style.SideMenuFrame.background = _card(-0.08)
    style.SideMenuFrame.padding    = (22, 18)
    style.SideMenuFrame.xminimum   = 400
    style.SideMenuFrame.xmaximum   = 500
    style.SideMenuFrame.yminimum   = 140
    style.SideMenuFrame.xfill      = False
    style.SideMenuFrame.yfill      = False

    # ----------------------------------
    # TEXTBOX (comic caption)
    # ----------------------------------
    style.textbox = Style(style.default)
    style.textbox.background = Frame("images/menus/ComicPanelCaption.png", 22, 22)
    style.textbox.padding    = (30, 24)
    style.textbox.xminimum   = 140
    style.textbox.xmaximum   = 520

    # ----------------------------------
    # SIDE MENU BUTTON
    # ----------------------------------
    style.SideMenuButton = Style(style.button)
    style.SideMenuButton.background       = None
    style.SideMenuButton.hover_background = _card( 0.20, 8)
    style.SideMenuButton.padding          = (16, 10)
    style.SideMenuButton.xminimum         = 380
    style.SideMenuButton.xmaximum         = 420
    style.SideMenuButton.yminimum         = 42
    style.SideMenuButton.top_margin       = 4
    style.SideMenuButton.bottom_margin    = 4

    style.SideMenuButtonText = Style(style.button_text)
    style.SideMenuButtonText.font           = "fonts/WorkSans-Bold.ttf"
    style.SideMenuButtonText.size           = 24
    style.SideMenuButtonText.color          = ROD_TEXT
    style.SideMenuButtonText.hover_color    = "#ffffff"
    style.SideMenuButtonText.selected_color = ROD_ACCENT
    style.SideMenuButtonText.outlines       = [(1, "#060d1a", 0, 0)]
    style.SideMenuButtonText.xalign         = 0.0
    style.SideMenuButtonText.text_align     = 0.0

    # Disabled / grayed-out variant
    style.SideMenuButtonDisabled = Style(style.SideMenuButton)
    style.SideMenuButtonDisabled.background       = None
    style.SideMenuButtonDisabled.hover_background = None

    style.SideMenuButtonTextDisabled = Style(style.SideMenuButtonText)
    style.SideMenuButtonTextDisabled.color       = "#555e6e"
    style.SideMenuButtonTextDisabled.hover_color = "#555e6e"

    # ----------------------------------
    # MENU SIZE (side menu / choice card + the nav faces on its rows)
    # ----------------------------------
    # On a phone (JoiPlay, the Android build) the touch-sized menu covers half the scene
    # (author 2026-10-11): "small" (the desktop layout) is the default EVERYWHERE, and the
    # player opts into "large" (the old touch layout) in Preferences > Menu Size.
    MENU_SCALE_PRESETS = {
        "small": {
            "frame_xmin": 400, "frame_xmax": 500,
            "btn_xmin": 380, "btn_xmax": 420, "btn_ymin": 42, "btn_padding": (16, 10),
            "text_size": 24,
            "nav_face": 30, "nav_face_step": 20, "nav_face_gap": 8,
        },
        # toned down from 700-900 / 640-820 / 36 (author 2026-10-11, "gigantesco"): a touch
        # bump over "small", not half the scene
        "large": {
            "frame_xmin": 560, "frame_xmax": 700,
            "btn_xmin": 520, "btn_xmax": 620, "btn_ymin": 54, "btn_padding": (20, 12),
            "text_size": 30,
            "nav_face": 38, "nav_face_step": 26, "nav_face_gap": 10,
        },
    }

    def menu_scale_mode():
        """The active menu size: the player's pick, "small" otherwise (also for the old
        Auto value None, saved by the first build of this preference)."""
        _m = getattr(persistent, "menu_scale", None)
        if _m in MENU_SCALE_PRESETS:
            return _m
        return "small"

    def apply_menu_scale(rebuild=False):
        """Size the side-menu styles and the nav-face constants from the active preset.
        Runs here at init and again when Menu Size changes in Preferences (rebuild=True)."""
        _p = MENU_SCALE_PRESETS[menu_scale_mode()]
        style.SideMenuFrame.xminimum = _p["frame_xmin"]
        style.SideMenuFrame.xmaximum = _p["frame_xmax"]
        for _st in (style.SideMenuButton, style.SideMenuButtonDisabled):
            _st.xminimum = _p["btn_xmin"]
            _st.xmaximum = _p["btn_xmax"]
            _st.yminimum = _p["btn_ymin"]
            _st.padding  = _p["btn_padding"]
        style.SideMenuButtonText.size         = _p["text_size"]
        style.SideMenuButtonTextDisabled.size = _p["text_size"]
        store.NAV_FACE      = _p["nav_face"]
        store.NAV_FACE_STEP = _p["nav_face_step"]
        store.NAV_FACE_GAP  = _p["nav_face_gap"]
        if rebuild:
            renpy.style.rebuild()
        print("[MENU_SCALE] applied %s (persistent=%s, mobile=%s, rebuild=%s)" % (
            menu_scale_mode(), getattr(persistent, "menu_scale", None), renpy.variant("mobile"), rebuild))

    apply_menu_scale()

    # ----------------------------------
    # WORLD ACTION BUTTON
    # ----------------------------------
    style.world_action_button = Style(style.button)
    style.world_action_button.xminimum          = 360
    style.world_action_button.xmaximum          = 360
    style.world_action_button.xfill             = False
    style.world_action_button.padding           = (14, 10)
    style.world_action_button.background        = "#0f172acc"
    style.world_action_button.hover_background  = "#1f2937dd"
    style.world_action_button.selected_background = "#334155dd"
    style.world_action_button.text_align        = 0.0

    # ----------------------------------
    # GIRL HUD – stat card frame
    # ----------------------------------
    style.GirlHudFrame = Style(style.default)
    style.GirlHudFrame.background = Frame("#0c1525dd", 8, 8, 8, 8)
    style.GirlHudFrame.padding    = (10, 8)
    style.GirlHudFrame.xminimum   = 360
    style.GirlHudFrame.xmaximum   = 360
    style.GirlHudFrame.yminimum   = 50

    # Generic bar base — thin like companion GirlCard
    style.GirlHudBarBase = Style(style.bar)
    style.GirlHudBarBase.xmaximum     = 140
    style.GirlHudBarBase.ymaximum     = 7
    style.GirlHudBarBase.thumb        = None
    style.GirlHudBarBase.thumb_offset = 0
    style.GirlHudBarBase.left_gutter  = 0
    style.GirlHudBarBase.right_gutter = 0

    # Stat bars
    style.GirlHudLoveBar = Style(style.GirlHudBarBase)
    style.GirlHudLoveBar.left_bar  = "images/menus/BarLoveFull.png"
    style.GirlHudLoveBar.right_bar = "images/menus/BarEmpty.png"

    style.GirlHudObedBar = Style(style.GirlHudBarBase)
    style.GirlHudObedBar.left_bar  = "images/menus/BarObedFull.png"
    style.GirlHudObedBar.right_bar = "images/menus/BarEmpty.png"

    style.GirlHudInbtBar = Style(style.GirlHudBarBase)
    style.GirlHudInbtBar.left_bar  = "images/menus/BarInbtFull.png"
    style.GirlHudInbtBar.right_bar = "images/menus/BarEmpty.png"

    style.GirlHudLustBar = Style(style.GirlHudBarBase)
    style.GirlHudLustBar.left_bar  = "images/menus/BarLustFull.png"
    style.GirlHudLustBar.right_bar = "images/menus/BarEmpty.png"

    style.GirlHudFocusBar = Style(style.GirlHudBarBase)
    style.GirlHudFocusBar.left_bar  = "images/menus/BarFocusFull.png"
    style.GirlHudFocusBar.right_bar = "images/menus/BarEmpty.png"

    # Stat label (3-letter tag beside each bar)
    style.GirlHudStatLabel = Style(style.default)
    style.GirlHudStatLabel.font   = "fonts/WorkSans-Bold.ttf"
    style.GirlHudStatLabel.size   = 12
    style.GirlHudStatLabel.color  = ROD_TEXT_DIM
    style.GirlHudStatLabel.xalign = 0.0

    # ----------------------------------
    # TOP HUD FRAME & LABEL
    # ----------------------------------
    style.TopHudFrame = Style(style.default)
    style.TopHudFrame.background = Frame("#0c1525dd", 8, 8, 8, 8)
    style.TopHudFrame.padding  = (16, 10)
    style.TopHudFrame.xminimum = 240
    style.TopHudFrame.yminimum = 64

    style.TopHudLabel = Style(style.default)
    style.TopHudLabel.font  = "fonts/WorkSans-SemiBold.ttf"
    style.TopHudLabel.size  = 19
    style.TopHudLabel.color = ROD_TEXT
    style.TopHudLabel.bold  = True

    # Main menu, game menu screens and dialogs: the menu kit (screen_menu_kit.rpy)

    # ----------------------------------
    # QUICK MENU (the pills of the menu kit, drawn with the phone kit's art: _pk_pill is init -4)
    # ----------------------------------
    style.quick_button = Style(style.button)
    style.quick_button.background          = None
    style.quick_button.hover_background    = _pk_pill("#ffffff", 0.1)
    style.quick_button.selected_background = _pk_pill(ROD_ACCENT, 0.22)
    style.quick_button.padding             = (14, 8)
    style.quick_button.xmargin             = 0
    style.quick_button.ymargin             = 0

    style.quick_button_text = Style(style.button_text)
    style.quick_button_text.font           = "fonts/WorkSans-Bold.ttf"
    style.quick_button_text.size           = 14
    style.quick_button_text.kerning        = 1
    style.quick_button_text.color          = "#8ca0b4"
    style.quick_button_text.hover_color    = "#ffffff"
    style.quick_button_text.selected_color = ROD_ACCENT
    style.quick_button_text.outlines       = [(1, "#030810", 0, 0)]
