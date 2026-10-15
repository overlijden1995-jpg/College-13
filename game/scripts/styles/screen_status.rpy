transform focus_bar_pulse:
    alpha 1.0
    ease 0.5 alpha 0.3
    ease 0.5 alpha 1.0
    repeat

# ========================================
# HUD overlay + status for girls
# ========================================

init python:
    if "hud" not in config.overlay_screens:
        config.overlay_screens.append("hud")

    # Short labels + colors for trait display on HUD and phone
    TRAIT_HUD_LABELS = {
        "virgin":         "VRG",
        "voyeur":         "VOY",
        "exhibitionist":  "EXH",
        "camera_lover":   "CAM+",
        "camera_hater":   "CAM-",
        "polyamorous":    "POLY",
        "monogamous":     "MONO",
        "loyal":          "LOY",
        "cheater":        "CHT",
        "cum_slut":       "CUM+",
        "hate_cum":       "CUM-",
        "public_fetish":  "PUB+",
        "public_shy":     "PUB-",
        "shy":            "SHY",
    }
    def _toggle_trait(girl, trait_id):
        """Add or remove a trait from a girl."""
        traits = getattr(girl, "traits", set())
        if trait_id in traits:
            traits.discard(trait_id)
        else:
            traits.add(trait_id)
        girl.traits = traits

    # Long descriptions for trait hints (Status screen discovery)
    # Shown with _tr(): _() marks the ones _I18N lacks (the chip shows _tr's English fallback as a whole string = its pair)
    TRAIT_HINT_DISPLAY = {
        "virgin":           "Virgin",
        "camera_lover":     "Loves being filmed",
        "camera_hater":     "Hates cameras",
        "cum_slut":         "Loves cum",
        "hate_cum":         "Hates cum",
        "public_fetish":    "Turned on by public risk",
        "public_shy":       "Terrified of exposure",
        "hardcore_sex":     "Likes it rough",
        "cute_sex":         "Likes it gentle",
        "femdom":           _("Likes to be in charge"),
        "submissive":       _("Likes being told what to do"),
        "married":          "Married",
        "loyal":            "Very loyal",
        "cheater":          "Prone to cheating",
        "voyeur":           "Likes watching",
        "exhibitionist":    "Likes being watched",
        "polyamorous":      "Open to sharing",
        "monogamous":       _("Demands exclusivity"),
        "lesbian":          "Lesbian",
        "bisexual":         "Bisexual",
        "nerd":             "Nerd",
        "gym_rat":          "Gym Rat",
        "anal_lover":       "Loves anal",
        "anal_hater":       "Hates anal",
        "heavy_drinker":    "Can hold her liquor",
        "lightweight":      "Lightweight drinker",
        "poor":             "Struggling financially",
        "rich":             "Wealthy",
        "breedable":        "Breeding kink",
        "infertile":        "Infertile",
        "pregnancy_fetish": "Wants to be a mom",
        "pregnancy_fear":   "Terrified of pregnancy",
    }

    TRAIT_HUD_COLORS = {
        "virgin":           "#e2e8f0",
        "voyeur":           "#a78bfa",
        "exhibitionist":    "#f472b6",
        "camera_lover":     "#38bdf8",
        "camera_hater":     "#94a3b8",
        "polyamorous":      "#c084fc",
        "monogamous":       "#60a5fa",
        "loyal":            "#60a5fa",
        "cheater":          "#f87171",
        "cum_slut":         "#fb923c",
        "hate_cum":         "#94a3b8",
        "public_fetish":    "#4ade80",
        "public_shy":       "#facc15",
        "shy":              "#8ca0b4",
        "lesbian":          "#f472b6",
        "bisexual":         "#c084fc",
        "nerd":             "#60a5fa",
        "gym_rat":          "#4ade80",
        "anal_lover":       "#fb923c",
        "anal_hater":       "#94a3b8",
        "heavy_drinker":    "#fbbf24",
        "lightweight":      "#facc15",
        "poor":             "#94a3b8",
        "rich":             "#fbbf24",
        "breedable":        "#f472b6",
        "infertile":        "#94a3b8",
        "pregnancy_fetish": "#f472b6",
        "pregnancy_fear":   "#facc15",
        "femdom":           "#c084fc",
        "submissive":       "#f9a8d4",
        "married":          "#fbbf24",
    }

    # ----- Crowd / Danger HUD helpers -----
    def _level_tint(pct):
        """Return (r, g, b) tuple interpolated from green(0) -> yellow(50) -> red(100)."""
        pct = max(0.0, min(100.0, float(pct)))
        if pct <= 50.0:
            t = pct / 50.0
            return (t, 1.0, 0.0)
        else:
            t = (pct - 50.0) / 50.0
            return (1.0, 1.0 - t, 0.0)


init:
    style TopHudLabelOutline is TopHudLabel:
        color "#ffffff"
        outlines [(2, "#000000", 0, 0)]

    style phone_text:
        font "fonts/WorkSans-SemiBold.ttf"
        color "#ffffff"
        size 18
        outlines []


# -----------------------------------------------------------
# Status card for ONE girl
# -----------------------------------------------------------
screen girl_status_hud(g):

    $ _gs_in_sex = player_in_sex_scene()

    button:
        background Frame("images/menus/GirlsCard_Blue.png", 10, 10, 10, 10)
        hover_background Frame(Solid("#7dd3fc33"), 0, 0, 0, 0)
        padding (14, 12)
        xminimum 240
        action (Show("phone_girl_status_screen", girl=g) if not _gs_in_sex else None)

        hbox:
            spacing 10
            yalign 0.5

            # Portrait
            $ char_key  = getattr(g, "gid", g.Name)
            $ char_file = _girl_avatar_by_gid(char_key)

            add char_file:
                xalign 0.0
                yalign 0.5

            # Name + thin stacked bars (like companion GirlCard)
            vbox:
                spacing 2
                yalign 0.5
                xminimum 160

                # Girl name. Expression, not "[g.Name]": this screen is `use`d inline by hud(),
                # and late text substitution on per_interact can run with the parent scope
                # where `g` no longer exists (NameError in Ren'Py 8.4).
                text g.Name:
                    font "fonts/WorkSans-Bold.ttf"
                    size 22
                    color "#e2e8f0"

                # 4 thin bars stacked — no labels, no values (companion style)
                # Love (red/pink)
                bar value g.Love range 1000 style "GirlHudLoveBar" yalign 0.5
                # Obedience (blue)
                bar value g.Obed range 1000 style "GirlHudObedBar" yalign 0.5
                # Inhibition (orange)
                bar value g.Inbt range 1000 style "GirlHudInbtBar" yalign 0.5
                # Lust (pink/hot)
                bar value g.Lust range 100 style "GirlHudLustBar" yalign 0.5


# -----------------------------------------------------------
# Left HUD: weekday / day / time
# -----------------------------------------------------------
screen day_time_hud():

    $ _raw_time_name  = TIME_NAMES[TimeIndex]
    $ weekday_name    = _tr(WEEKDAY_NAMES[(Day - 1) % 7])
    $ current_time_name = _tr(_raw_time_name)
    $ time_icon       = TIME_ICONS.get(_raw_time_name, "images/menus/AfternoonIcon.png")
    $ remaining_rounds = max(0, 100 - Round)

    frame:
        background Frame("images/menus/GirlsCard_Blue.png", 10, 10, 10, 10)
        padding (20, 16)
        yalign 0.0

        vbox:
            spacing 6
            xalign 0.0

            # Period icon + name
            hbox:
                spacing 8
                yalign 0.5

                add time_icon:
                    yalign 0.5

                text "[current_time_name!u]":
                    font "fonts/WorkSans-Bold.ttf"
                    size 18
                    color "#e2e8f0"
                    kerning 1

            # Weekday + day
            text _("[weekday_name!u], DAY [Day]"):
                font "fonts/WorkSans-SemiBold.ttf"
                size 14
                kerning 2
                color "#8ca0b4"

            # Time left
            text _("TIME LEFT: [remaining_rounds]"):
                font "fonts/WorkSans-Bold.ttf"
                size 15
                color "#7dd3fc"

            # Exam countdown, always on the card (author 2026-10-11: it used to show only at 3
            # days or less, so most of the cycle had no exam line at all). exam_countdown_text
            # (exam.rpy) is shared with the phone status; urgent gets its color, calm the gray.
            $ _exam_txt, _exam_col = exam_countdown_text()
            text "[_exam_txt!u]":
                font ("fonts/WorkSans-Bold.ttf" if _exam_col else "fonts/WorkSans-SemiBold.ttf")
                size 14
                kerning 1
                color (_exam_col or "#8ca0b4")


# -----------------------------------------------------------
# Crowd Level + Danger Meter
# -----------------------------------------------------------
screen crowd_danger_hud():

    $ _cl = getattr(store, "_crowd_level", 0)
    $ _pa = getattr(store, "_public_attention", 0)
    $ _crowd_tint = Color(tuple(int(c * 255) for c in _level_tint(_cl)))
    $ _danger_tint = Color(tuple(int(c * 255) for c in _level_tint(_pa)))

    fixed:
        fit_first True
        yalign 0.0

        vbox:
            spacing 6

            button:
                background None
                hover_background None
                action NullAction()
                tooltip _("Crowd: how many people are nearby ([_cl]/100)")

                add "images/menus/Group Level.png":
                    zoom 0.55
                    matrixcolor TintMatrix(_crowd_tint)

            button:
                background None
                hover_background None
                action NullAction()
                tooltip _("Danger: risk of getting caught ([_pa]/100)")

                add "images/menus/Danger Level.png":
                    zoom 0.55
                    matrixcolor TintMatrix(_danger_tint)

        # Tooltip — overlaid, does not push layout
        $ _cd_tip = GetTooltip()
        if _cd_tip:
            frame:
                background Frame(Solid("#0f172dee"), 4, 4, 4, 4)
                padding (8, 4)
                ypos 150
                text _cd_tip:
                    font "fonts/WorkSans-SemiBold.ttf"
                    size 13
                    color "#e2e8f0"


# -----------------------------------------------------------
# MAIN HUD overlay
# -----------------------------------------------------------
screen hud():

    zorder 50

    $ girls_here = girls_on_scene(include_scene_girls=True)
    $ _p_energy = Player.energy
    $ _p_max_energy = Player._get_energy_max()
    $ _in_sex = player_in_sex_scene()

    # Full-screen container with uniform padding
    frame:
        xfill True
        yfill True
        background None
        padding (35, 20, 35, 20)

        # TOP ROW
        hbox:
            xfill True
            yalign 0.0
            spacing 16

            # LEFT: time / day
            use day_time_hud

            # Crowd/danger
            use crowd_danger_hud

            null xfill True

            # CENTER: girl status cards
            hbox:
                spacing 10
                yalign 0.0

                frame:
                    background None
                    xsize 320
                    if len(girls_here) >= 1:
                        use girl_status_hud(girls_here[0])

                frame:
                    background None
                    xsize 320
                    if len(girls_here) >= 2:
                        use girl_status_hud(girls_here[1])

                frame:
                    background None
                    xsize 320
                    if len(girls_here) >= 3:
                        use girl_status_hud(girls_here[2])

            null xfill True

            # RIGHT: phone icon + player stats grouped together
            hbox:
                spacing 10
                yalign 0.0
                xalign 1.0

                # PHONE ICON (hidden during sex, intro, events)
                if not _in_sex and not _in_intro and not _in_event:
                    imagebutton:
                        idle Transform("images/menus/Cellphone.png", zoom=0.22)
                        hover Transform("images/menus/Cellphone.png", zoom=0.22, matrixcolor=BrightnessMatrix(0.15))
                        action [Function(_phone_hide_others), Show("phone_screen")]
                        yalign 0.0

                # Player stats
                button:
                    background Frame("images/menus/GirlsCard_Blue.png", 10, 10, 10, 10)
                    hover_background Frame(Solid("#7dd3fc33"), 0, 0, 0, 0)
                    padding (20, 16)
                    yalign 0.0
                    action (Show("phone_player_status_screen") if not _in_sex else None)

                    vbox:
                        spacing 8

                        # Energy pips
                        hbox:
                            spacing 6
                            yalign 0.5

                            add "images/menus/EnergyIcon.png":
                                zoom 0.35
                                yalign 0.5

                            hbox:
                                spacing 2
                                yalign 0.5

                                for _ei in range(_p_max_energy):
                                    if _ei < _p_energy:
                                        frame:
                                            background Frame("#4ade80", 2, 2, 2, 2)
                                            xsize 18
                                            ysize 10
                                    else:
                                        frame:
                                            background Frame("#1e293b", 2, 2, 2, 2)
                                            xsize 18
                                            ysize 10

                        # Lust bar
                        hbox:
                            spacing 6
                            yalign 0.5

                            add "images/menus/FlameIcon.png":
                                zoom 0.35
                                yalign 0.5

                            frame:
                                background Frame("#1e293b", 3, 3, 3, 3)
                                xsize 120
                                ysize 10
                                yalign 0.5
                                # the theme frame pads 6px and the theme bar keeps 6px gutters: the fill sat
                                # 6px right and below its track and never reached the end (tester 2026-10-11)
                                padding (0, 0)

                                if Player.Focus >= 100:
                                    bar value Player.Focus range 100 at focus_bar_pulse id "focus_bar":
                                        left_bar Frame("#fbbf24", 3, 3, 3, 3)
                                        right_bar Frame("#1e293b00", 3, 3, 3, 3)
                                        xfill True
                                        ysize 10
                                        thumb None
                                        thumb_offset 0
                                        left_gutter 0
                                        right_gutter 0
                                else:
                                    bar value Player.Focus range 100 id "focus_bar":
                                        left_bar Frame("#ef4444", 3, 3, 3, 3)
                                        right_bar Frame("#1e293b00", 3, 3, 3, 3)
                                        xfill True
                                        ysize 10
                                        thumb None
                                        thumb_offset 0
                                        left_gutter 0
                                        right_gutter 0

                        # Money
                        text "$ [Player.cash]":
                            font "fonts/WorkSans-Bold.ttf"
                            size 16
                            color "#4ade80"


# -----------------------------------------------------------
# Phone UI — shared constants & transforms
# -----------------------------------------------------------
# Crop phone from 1920x1080 source, zoom 1.3x, position left
# -----------------------------------------------------------

init -5 python:
    # Phone screen coordinates (measured from Phone.png 1920x1080)
    # Screen area: x=56-596, y=29-1043 (540x1014)

    # Position: image is fullscreen 1920x1080, phone already placed in it
    PH_X = 0
    PH_Y = 0

    # Content area (inside the phone screen)
    PH_CX = 66          # left padding from screen edge (56 + 10)
    PH_CW = 520         # usable content width (540 - 20 padding)

    # Y offsets (from top of image, below camera notch area)
    PH_CY_STATUS  = 100         # status bar (below camera)
    PH_CY_MAIN    = 140         # main content
    PH_CY_HEADER  = 105         # header bar
    PH_HEADER_H   = 70          # header height
    PH_CY_LINE    = 130         # accent line
    PH_CY_BODY    = PH_CY_HEADER + PH_HEADER_H + 4
    PH_CY_BODY2   = PH_CY_BODY + 46
    PH_CY_BODY3   = PH_CY_BODY + 56
    PH_CY_CLOSE   = 970         # close button area
    PH_CLOSE_X    = 310         # close button x

    PH_BTN_W      = 490         # button width
    PH_SCROLL_H   = 720         # viewport max
    PH_SCROLL_H2  = 660         # shorter viewports
    PH_SCROLL_H3  = 680         # gifts viewport

    # Info bar y (below header)
    PH_CY_INFO    = PH_CY_BODY
    PH_CY_INFO2   = PH_CY_BODY + 2
    PH_CY_ITEMS   = PH_CY_BODY + 40

    # Font sizes
    PH_FONT_XL    = 28
    PH_FONT_LG    = 26
    PH_FONT_MD    = 24
    PH_FONT_SM    = 20
    PH_FONT_XS    = 18
    PH_FONT_XXS   = 16
    PH_FONT_TINY  = 14
    PH_FONT_BACK  = 18
    PH_FONT_STATUS = 19

    # Button heights
    PH_BTN_H      = 71
    PH_BTN_H2     = 67
    PH_BTN_H3     = 64
    PH_BTN_H4     = 58
    PH_BTN_H5     = 62
    PH_CONTACT_H  = 76

    # Bar width for stats
    PH_BAR_W      = 300

    # Chin area (bottom of phone screen for nav buttons)
    _PH_IMG_H     = 1080
    _PH_SCREEN_BOTTOM = 940     # where screen content ends (above chin)
    PH_CHIN_Y     = 965         # chin button y position
    PH_CHIN_BTN   = 40

    # Phone image (already positioned and sized in the PNG)
    _phone_img = "images/menus/Phone.png"

    # Screens to hide when phone opens
    _PHONE_HIDE_SCREENS = ["hud"]

    def _phone_hide_others():
        store._phone_is_open = True
        for s in _PHONE_HIDE_SCREENS:
            if renpy.get_screen(s):
                renpy.hide_screen(s)
        renpy.restart_interaction()

    def _phone_open_chat_and_restore(label_name, girl):
        """Wrapper: runs a phone label in new context, then shows the girl's
        sprite if she arrived during the call (invite / come over)."""
        store._phone_girl_arrived = None
        store._phone_chat_exit = "back"
        renpy.call_in_new_context(label_name, girl)
        # After context returns, check if a girl arrived and needs her sprite shown
        gid = store._phone_girl_arrived
        if gid:
            store._phone_girl_arrived = None
            g = GIRL_BY_ID.get(gid)
            if g and getattr(g, "loc", None) == store.CurrentLocation:
                _sl = getattr(g, "SpriteLoc", StageCenter)
                if _sl == StageLeft:
                    _tf = slot_left
                elif _sl == StageRight:
                    _tf = slot_right
                else:
                    _tf = slot_center
                set_girl_sprite(g.gid, pose="standing", at_list=[_tf])
        # If user pressed "back", return to contact options instead of closing
        if store._phone_chat_exit == "back" and not gid:
            renpy.show_screen("phone_contact_options_screen", girl=girl)
            return
        # Restore phone state in the main context (hud, _phone_is_open)
        _phone_restore_others()
        # Force location loops (Shower_Loop etc.) to restart so the
        # menu re-evaluates with the newly arrived girl.
        if gid:
            _loc = store.CurrentLocation
            _jump_to = _LOC_LOOPS.get(_loc)   # central map (navigation.rpy); the local copy had no "tenny_room"
            if _jump_to:
                renpy.jump(_jump_to)

    def _phone_open_npc_chat_and_restore(npc):
        """Wrapper: runs NPC partner chat label in new context."""
        store._phone_chat_exit = "back"
        renpy.call_in_new_context("npc_phone_open_chat", npc)
        if store._phone_chat_exit == "back":
            renpy.show_screen("phone_contact_options_screen", girl=npc)
            return
        _phone_restore_others()

    def _phone_open_family_chat_and_restore(who):
        """Wrapper: runs a family contact's chat (the father, shion_family.rpy) in new context."""
        store._phone_chat_exit = "back"
        renpy.call_in_new_context("family_phone_open_chat", who)
        if store._phone_chat_exit == "back":
            renpy.show_screen("phone_contact_options_screen", girl=who)
            return
        _phone_restore_others()

    def _phone_open_group_and_restore(group):
        """Wrapper: runs a group chat label in new context, then shows
        sprites for ALL girls who arrived during the call."""
        print("[PHONE_GROUP] ENTER _phone_open_group_and_restore")
        store._phone_girls_arrived = []
        renpy.call_in_new_context("phone_open_group_chat", group)
        print("[PHONE_GROUP] context returned, _phone_girls_arrived=%s" % getattr(store, "_phone_girls_arrived", "MISSING"))
        # Re-show sprites for girls who arrived during the group chat
        arrived = getattr(store, "_phone_girls_arrived", [])
        for gid in arrived:
            g = GIRL_BY_ID.get(gid)
            if g and getattr(g, "loc", None) == store.CurrentLocation:
                _sl = getattr(g, "SpriteLoc", StageCenter)
                if _sl == StageLeft:
                    _tf = slot_left
                elif _sl == StageRight:
                    _tf = slot_right
                else:
                    _tf = slot_center
                set_girl_sprite(g.gid, pose="standing", at_list=[_tf])
        _any_arrived = len(arrived) > 0
        store._phone_girls_arrived = []
        # Restore phone state in the main context (hud, _phone_is_open)
        _phone_restore_others()
        # Force location loop restart if any girl arrived
        if _any_arrived:
            _loc = store.CurrentLocation
            _jump_to = _LOC_LOOPS.get(_loc)   # central map (navigation.rpy); the local copy had no "tenny_room"
            print("[PHONE_GROUP] arrived=%s loc=%s jump=%s" % ([g for g in arrived], _loc, _jump_to))
            if _jump_to:
                renpy.jump(_jump_to)
            else:
                print("[PHONE_GROUP] WARNING: no loop label for location '%s'" % _loc)

    def _phone_restore_others():
        store._phone_is_open = False
        for s in _PHONE_HIDE_SCREENS:
            if not renpy.get_screen(s):
                renpy.show_screen(s)
        renpy.restart_interaction()

    def _phone_shop_buy(item_id, qty, price):
        """Buy item and set feedback flag for the shop screen."""
        if phone_buy_item(item_id, qty, price):
            store._shop_bought_id = item_id

    def _phone_shop_buy_vitamin(item_id, qty, price):
        """Buy fertility vitamin and activate it. The purchase IS the buff (same as the pharmacy counter):
        no inventory item, nothing ever consumes one."""
        if Player.cash >= price:
            Player.spend_cash(price)
            store._shop_bought_id = item_id
            store._player_fertility_vitamin_active = True
            store._player_fertility_vitamin_days = _FERT_VITAMIN_DAYS
            print("[PREGNANCY] fertility vitamin purchased (phone), %d days active" % _FERT_VITAMIN_DAYS)

    def _phone_shop_buy_unique(item_id, qty, price):
        """Buy a one-time gift and mark it as permanently purchased."""
        if phone_buy_item(item_id, qty, price):
            store._shop_bought_id = item_id
            if not hasattr(store.Player, "_unique_gifts_purchased"):
                store.Player._unique_gifts_purchased = set()
            store.Player._unique_gifts_purchased.add(item_id)

    def _is_unique_gift_purchased(item_id):
        """Check if a one-time gift was ever purchased (covers old saves too)."""
        if item_id in getattr(store.Player, "_unique_gifts_purchased", set()):
            return True
        if store.Player.get_item_count(item_id) > 0:
            return True
        if item_id.startswith("piercing_"):
            _g = GIRL_BY_ID.get(item_id.replace("piercing_", ""))
            if _g and (getattr(_g, "Piercing", False) or getattr(_g, "_piercing_pending", False)):
                return True
        elif item_id.startswith("bikini_"):
            _g = GIRL_BY_ID.get(item_id.replace("bikini_", ""))
            if _g and getattr(_g, "_bikini_unlocked", False):
                return True
        return False

    def _phone_shop_clear_bought():
        """Clear the bought feedback flag."""
        store._shop_bought_id = ""

    # Item icons for inventory display
    _ITEM_ICONS = {
        "condom":    "\U0001F6E1",
        "japanese_condom": "\U0001F38C",
        "chocolate": "\U0001F36B",
        "flowers":   "\U0001F490",
        "perfume":   "\U0001F9F4",
        "necklace":  "\U0001F4FF",
        "handbag":   "\U0001F45C",
        "ring":      "\U0001F48D",
        "watch":     "\U0000231A",
        "jewelry_set": "\U0001F48E",
        "drinks":    "\U0001F378",
        "tripod":    "\U0001F4F7",
        "tekmix_camera": "\U0001F4F9",
        "girls_tracker": "\U0001F4CD",
        "instant_preg_test": "\U0001F9EA",
        "piercing_gwen":  "\U0001F48E",
        "piercing_rogue": "\U0001F48E",
        "piercing_ntw":   "\U0001F48E",
        "bikini_gwen":  "\U0001F459",
        "bikini_rogue": "\U0001F459",
        "bikini_ntw":   "\U0001F459",
        "piercing_tenny": "\U0001F48E",
        "bikini_tenny":   "\U0001F459",
        "piercing_shion": "\U0001F48E",
        "bikini_shion":   "\U0001F459",
        "blazing_flames":    "\U0001F3AE",
        "my_hero_college":   "\U0001F3AE",
        "one_frame_man":     "\U0001F3AE",
        "supra_marcio_kart": "\U0001F3AE",
        "catch_monsters_89": "\U0001F3AE",
        "fuckpop_bobblehead":"\U0001F3AE",
        "thisdendo_3ds":     "\U0001F3AE",
        "birth_control":     "\U0001F48A",
        "placebo_pills":     "\U0001F33B",
        "morning_after":     "\U0001F48A",
        "fertility_vitamin": "\U0001F48A",
    }

# Reusable chin buttons (Back + Home) for all phone screens
# back_action: what happens on Back press
# home_action: what happens on Home press (default = close phone)
screen phone_chin_buttons(back_action, home_action=None):
    if home_action is False:
        $ _ph_home = None
    elif home_action is None:
        $ _ph_home = [Hide(renpy.current_screen().tag), Function(_phone_restore_others)]
    else:
        $ _ph_home = home_action

    # Back button — left area, shifted right and up
    imagebutton:
        idle Transform("images/menus/BackButton.png", zoom=0.55, matrixcolor=BrightnessMatrix(0.0))
        hover Transform("images/menus/BackButton.png", zoom=0.55, matrixcolor=BrightnessMatrix(0.15))
        xpos PH_CX + 40
        ypos PH_CHIN_Y - 15
        action back_action

    # Home button — center, shifted left and up
    imagebutton:
        idle Transform("images/menus/HomeButton.png", zoom=0.50, matrixcolor=BrightnessMatrix(0.0))
        hover Transform("images/menus/HomeButton.png", zoom=0.50, matrixcolor=BrightnessMatrix(0.15))
        xpos PH_CX + int(PH_CW / 2) - 42
        ypos PH_CHIN_Y - 24
        action _ph_home


transform phone_slide_in:
    xoffset -650
    ease 0.3 xoffset 0

transform phone_slide_out:
    xoffset 0
    ease 0.25 xoffset -650


# -----------------------------------------------------------
# Phone main menu
# -----------------------------------------------------------
screen phone_screen():

    modal True
    zorder 200

    button:
        xfill True
        yfill True
        background "#00000088"
        action NullAction()

    frame at phone_slide_in:
        xpos PH_X
        ypos PH_Y
        background None
        padding (0, 0)

        fixed:
            fit_first True
            add _phone_img

            # --- Status bar (money) ---
            hbox:
                xpos PH_CX + 8
                ypos PH_CY_STATUS
                xsize PH_CW - 16
                spacing 6

                text "$ [Player.cash]":
                    style "phone_text"
                    size PH_FONT_STATUS
                    color "#4ade80"
                    bold True
                    yalign 0.5

            # --- Day/Period indicator ---
            $ _period_names = ["Morning", "Midday", "Evening", "Night"]
            $ _cur_period = _period_names[TimeIndex] if 0 <= TimeIndex < 4 else "???"
            vbox:
                xpos PH_CX
                ypos PH_CY_STATUS + 30
                xsize PH_CW
                spacing 0
                text _("Day [Day]"):
                    style "phone_text"
                    size 16
                    color "#ff9800"
                    xalign 0.5
                text _cur_period:
                    style "phone_text"
                    size 20
                    color "#e2e8f0"
                    xalign 0.5

            # --- App Grid (2 columns) ---
            $ _grid_x = PH_CX + 8
            $ _grid_y = PH_CY_STATUS + 100
            $ _gap = 10
            $ _btn_w = int((PH_CW - 16 - _gap) / 2)
            $ _btn_h = 120

            # Row 1: Contacts + Shop
            hbox:
                xpos _grid_x
                ypos _grid_y
                spacing _gap

                button:
                    xsize _btn_w
                    ysize _btn_h
                    background Frame("images/menus/Phone_Btn_contacts.png", 20, 20, 20, 20)
                    hover_background Frame("images/menus/Phone_Btn_contacts_hover.png", 20, 20, 20, 20)
                    action [Hide("phone_screen"), Show("phone_contacts_screen")]
                    vbox:
                        xalign 0.5
                        yalign 0.5
                        spacing 6
                        add "images/menus/Contact.png" xalign 0.5 zoom 0.5
                        text _("Contacts"):
                            style "phone_text"
                            size 18
                            color "#4da6ff"
                            xalign 0.5

                button:
                    xsize _btn_w
                    ysize _btn_h
                    background Frame("images/menus/Phone_Btn_shop.png", 20, 20, 20, 20)
                    hover_background Frame("images/menus/Phone_Btn_shop_hover.png", 20, 20, 20, 20)
                    action [Hide("phone_screen"), Show("phone_shop_screen")]
                    vbox:
                        xalign 0.5
                        yalign 0.5
                        spacing 6
                        add "images/menus/Shop.png" xalign 0.5 zoom 0.5
                        text _("Shop"):
                            style "phone_text"
                            size 18
                            color "#4ade80"
                            xalign 0.5

            # Row 2: Inventory + BigFans
            hbox:
                xpos _grid_x
                ypos _grid_y + _btn_h + _gap
                spacing _gap

                button:
                    xsize _btn_w
                    ysize _btn_h
                    background Frame("images/menus/Phone_Btn_inventory.png", 20, 20, 20, 20)
                    hover_background Frame("images/menus/Phone_Btn_inventory_hover.png", 20, 20, 20, 20)
                    action [Hide("phone_screen"), Show("phone_inventory_screen")]
                    vbox:
                        xalign 0.5
                        yalign 0.5
                        spacing 6
                        add "images/menus/Inventory.png" xalign 0.5 zoom 0.5
                        text _("Inventory"):
                            style "phone_text"
                            size 18
                            color "#b388ff"
                            xalign 0.5

                button:
                    xsize _btn_w
                    ysize _btn_h
                    background Frame("images/menus/Phone_Btn_bigfans.png", 20, 20, 20, 20)
                    hover_background Frame("images/menus/Phone_Btn_bigfans_hover.png", 20, 20, 20, 20)
                    action [Hide("phone_screen"), Show("phone_bigfans_screen")]
                    vbox:
                        xalign 0.5
                        yalign 0.5
                        spacing 6
                        add "images/menus/BigFans.png" xalign 0.5 zoom 0.5
                        text _("BigFans"):
                            style "phone_text"
                            size 18
                            color "#ff5c93"
                            xalign 0.5

            # Row 3: Status + Tutorial
            hbox:
                xpos _grid_x
                ypos _grid_y + (_btn_h + _gap) * 2
                spacing _gap

                button:
                    xsize _btn_w
                    ysize _btn_h
                    background Frame("images/menus/Phone_Btn_Status.png", 20, 20, 20, 20)
                    hover_background Frame("images/menus/Phone_Btn_Status_Hover.png", 20, 20, 20, 20)
                    action [Hide("phone_screen"), Show("phone_player_status_screen")]
                    vbox:
                        xalign 0.5
                        yalign 0.5
                        spacing 6
                        add "images/menus/Status.svg" xalign 0.5 zoom 0.5
                        text _("Status"):
                            style "phone_text"
                            size 18
                            color "#38bdf8"
                            xalign 0.5

                button:
                    xsize _btn_w
                    ysize _btn_h
                    background Frame("images/menus/Phone_Btn_tutorial.png", 20, 20, 20, 20)
                    hover_background Frame("images/menus/Phone_Btn_tutorial_hover.png", 20, 20, 20, 20)
                    action [Hide("phone_screen"), Show("phone_tutorial_screen")]
                    vbox:
                        xalign 0.5
                        yalign 0.5
                        spacing 6
                        add "images/menus/Tutorial.png" xalign 0.5 zoom 0.5
                        text _("Tutorial"):
                            style "phone_text"
                            size 18
                            color "#d4c87a"
                            xalign 0.5

            # Row 4: Cheats
            hbox:
                xpos _grid_x
                ypos _grid_y + (_btn_h + _gap) * 3
                spacing _gap

                button:
                    xsize _btn_w
                    ysize _btn_h
                    background Frame("#2a0a0a", 20, 20, 20, 20)
                    hover_background Frame("#3d1414", 20, 20, 20, 20)
                    action [Hide("phone_screen"), Show("phone_cheat_screen")]
                    vbox:
                        xalign 0.5
                        yalign 0.5
                        spacing 6
                        add "images/menus/cheat.png" xalign 0.5 zoom 0.5
                        text _("Cheats"):
                            style "phone_text"
                            size 18
                            color "#f87171"
                            xalign 0.5

            # Chin: main screen — both back and home close phone
            use phone_chin_buttons(
                back_action=[Hide("phone_screen"), Function(_phone_restore_others)],
                home_action=[Hide("phone_screen"), Function(_phone_restore_others)])


# -----------------------------------------------------------
# Phone contacts + contact options: live in screen_phone_contacts.rpy (phone UI kit)
# -----------------------------------------------------------


# -----------------------------------------------------------
# Phone NPC partner status screen: lives in screen_npc_status.rpy (phone UI kit)
# -----------------------------------------------------------


# -----------------------------------------------------------
# Phone girl status screen: lives in screen_girl_status.rpy (hero header + tabs of cards)
# -----------------------------------------------------------


# -----------------------------------------------------------
# Phone Player Status: lives in screen_player_status.rpy (phone UI kit)
# -----------------------------------------------------------


# -----------------------------------------------------------
# Phone BigFans sub-screen — Fan Requests
# -----------------------------------------------------------
screen phone_bigfans_screen(initial_tab="feed"):

    modal True
    zorder 200

    default _bf_tab = initial_tab
    default _bf_refresh = 0

    # Layout constants
    $ _bf_header_h = 40
    $ _bf_nav_h = 62
    $ _bf_body_y = PH_CY_HEADER + _bf_header_h + 2
    $ _bf_nav_y = _PH_SCREEN_BOTTOM - _bf_nav_h
    $ _bf_scroll = _bf_nav_y - _bf_body_y
    $ _bf_tab_w = int(PH_CW / 4)

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

            # --- Slim header ---
            frame:
                xpos PH_CX
                ypos PH_CY_HEADER
                xsize PH_CW
                ysize _bf_header_h
                background "#2a0f1e"
                padding (14, 0)

                text _("BigFans"):
                    font "fonts/DancingScript-Bold.ttf"
                    size 32
                    color "#ff5c93"
                    xalign 0.5
                    yalign 0.5

            # --- Bottom navigation bar ---
            frame:
                xpos PH_CX
                ypos _bf_nav_y
                xsize PH_CW
                ysize _bf_nav_h
                background "#0d1117"
                padding (0, 0)

                # Top border
                frame:
                    xpos 0
                    ypos 0
                    xsize PH_CW
                    ysize 1
                    background "#ffffff0a"

                python:
                    _bf_icon_zoom = 0.45
                    _bf_icon_active = BrightnessMatrix(0.0)
                    _bf_icon_inactive = BrightnessMatrix(-0.5)

                hbox:
                    xfill True
                    yalign 0.5

                    # Home / Feed
                    button:
                        xsize _bf_tab_w
                        ysize _bf_nav_h
                        background None
                        hover_background "#ffffff08"
                        action SetScreenVariable("_bf_tab", "feed")
                        add "images/menus/HomeBF.png":
                            zoom _bf_icon_zoom
                            xalign 0.5
                            yalign 0.5
                            matrixcolor (_bf_icon_active if _bf_tab == "feed" else _bf_icon_inactive)

                    # Upload / Publish
                    button:
                        xsize _bf_tab_w
                        ysize _bf_nav_h
                        background None
                        hover_background "#ffffff08"
                        action SetScreenVariable("_bf_tab", "upload")
                        add "images/menus/UploadVideosBF.png":
                            zoom _bf_icon_zoom
                            xalign 0.5
                            yalign 0.5
                            matrixcolor (_bf_icon_active if _bf_tab == "upload" else _bf_icon_inactive)

                    # DMs / Requests
                    button:
                        xsize _bf_tab_w
                        ysize _bf_nav_h
                        background None
                        hover_background "#ffffff08"
                        action SetScreenVariable("_bf_tab", "requests")
                        add "images/menus/DMBF.png":
                            zoom _bf_icon_zoom
                            xalign 0.5
                            yalign 0.5
                            matrixcolor (_bf_icon_active if _bf_tab == "requests" else _bf_icon_inactive)

                    # Stats / Account
                    button:
                        xsize _bf_tab_w
                        ysize _bf_nav_h
                        background None
                        hover_background "#ffffff08"
                        action SetScreenVariable("_bf_tab", "account")
                        add "images/menus/MyAccountBF.png":
                            zoom _bf_icon_zoom
                            xalign 0.5
                            yalign 0.5
                            matrixcolor (_bf_icon_active if _bf_tab == "account" else _bf_icon_inactive)

            # ============================================
            # TAB: Feed  (OnlyFans-style post cards)
            # ============================================
            if _bf_tab == "feed":
                $ _bf_published = sorted(getattr(Player, "bigfans_published", []), key=lambda e: (e.get("published_day", 0), e.get("published_seq", 0)), reverse=True)
                $ _bf_subs = getattr(Player, "bigfans_subscribers", 10)

                viewport:
                    xpos PH_CX
                    ypos _bf_body_y
                    xsize PH_CW
                    ymaximum _bf_scroll
                    mousewheel True
                    draggable True
                    scrollbars "vertical"
                    scrollbar_unscrollable "hide"

                    vbox:
                        spacing 0
                        xsize PH_CW

                        # --- Profile banner ---
                        frame:
                            xsize PH_CW
                            background None
                            padding (16, 14)

                            hbox:
                                spacing 14

                                # Avatar (PNG)
                                python:
                                    _pcount = len(_bf_published)
                                    _bf_subs_fmt = bigfans_format_number(_bf_subs)
                                    _player_initial = Player.Name[0].upper() if Player.Name else "P"
                                fixed:
                                    xsize 72
                                    ysize 72
                                    add "images/menus/bigfans/avatar_profile.png":
                                        xalign 0.5
                                        yalign 0.5
                                    text "[_player_initial]":
                                        style "phone_text"
                                        size 28
                                        color "#ffffff"
                                        bold True
                                        xalign 0.5
                                        yalign 0.5

                                vbox:
                                    spacing 4
                                    yalign 0.5
                                    text "[Player.Name]":
                                        style "phone_text"
                                        size 22
                                        color "#e2e8f0"
                                        bold True
                                    hbox:
                                        spacing 14
                                        hbox:
                                            spacing 4
                                            text "[_bf_subs_fmt]":
                                                style "phone_text"
                                                size 18
                                                color "#e8467c"
                                                bold True
                                            text _("subs"):
                                                style "phone_text"
                                                size 18
                                                color "#8ca0b4"
                                        hbox:
                                            spacing 4
                                            text "[_pcount]":
                                                style "phone_text"
                                                size 18
                                                color "#e2e8f0"
                                                bold True
                                            text _("posts"):
                                                style "phone_text"
                                                size 18
                                                color "#8ca0b4"

                        null height 8

                        # --- Published posts ---
                        if _bf_published:
                            for _pub in _bf_published:
                                python:
                                    _pub_title = bigfans_feed_title(_pub)
                                    _pub_lbl = bigfans_feed_label(_pub)
                                    _pub_dur = bigfans_video_duration(_pub)
                                    _pub_views = _pub["total_views"]
                                    _pub_earned = _pub["total_earned"]
                                    _pub_daily = _pub["daily_views"]
                                    _pub_views_fmt = bigfans_format_number(_pub_views)
                                    _pub_daily_fmt = bigfans_format_number(_pub_daily)

                                # Post card
                                frame:
                                    xsize PH_CW - 16
                                    xalign 0.5
                                    background Frame("images/menus/bigfans/card_bg_wide.png", 22, 22, 22, 22)
                                    padding (0, 0)

                                    vbox:
                                        xfill True
                                        spacing 0

                                        # Thumbnail (wide, stretches to card width)
                                        fixed:
                                            xsize PH_CW - 16
                                            ysize 160
                                            add "images/menus/bigfans/thumbnail_wide.png":
                                                xsize PH_CW - 16
                                                ysize 160

                                            # Play button center
                                            add "images/menus/bigfans/play_button.png":
                                                xalign 0.5
                                                yalign 0.5

                                            # Duration badge bottom-right
                                            frame:
                                                xalign 1.0
                                                yalign 1.0
                                                xoffset -8
                                                yoffset -8
                                                background Frame("#000000cc", 8, 8, 8, 8)
                                                padding (6, 3)
                                                text "[_pub_dur]":
                                                    style "phone_text"
                                                    size 13
                                                    color "#ffffffdd"

                                        # Post info
                                        frame:
                                            xfill True
                                            background None
                                            padding (14, 12, 14, 12)

                                            vbox:
                                                spacing 4
                                                xfill True

                                                text "[_pub_title]":
                                                    font "fonts/WorkSans-Bold.ttf"
                                                    size 18
                                                    color "#e2e8f0"

                                                text "[_pub_lbl]":
                                                    style "phone_text"
                                                    size 14
                                                    color "#8ca0b4"

                                                # Engagement row
                                                hbox:
                                                    xfill True
                                                    spacing 14
                                                    text _("[_pub_views_fmt] views"):
                                                        style "phone_text"
                                                        size 15
                                                        color "#8ca0b4"
                                                        yalign 0.5
                                                    text _("+[_pub_daily_fmt]/day"):
                                                        style "phone_text"
                                                        size 15
                                                        color "#60a5fa"
                                                        yalign 0.5
                                                    null xfill True
                                                    text "$[_pub_earned]":
                                                        style "phone_text"
                                                        size 20
                                                        color "#4ade80"
                                                        bold True
                                                        yalign 0.5

                                # Spacing
                                null height 12

                        else:
                            null height 60
                            text _("No posts yet"):
                                style "phone_text"
                                size 18
                                color "#555e6e"
                                xalign 0.5
                            null height 6
                            text _("Upload a video to get started"):
                                style "phone_text"
                                size 14
                                color "#e8467c88"
                                xalign 0.5
                            null height 10

            # ============================================
            # TAB: Upload  (publish new videos)
            # ============================================
            if _bf_tab == "upload":
                $ _bf_unpublished = [v for v in reversed(getattr(Player, "recorded_videos", [])) if not v.get("published", False) and not v.get("sold", False)]

                viewport:
                    xpos PH_CX
                    ypos _bf_body_y
                    xsize PH_CW
                    ymaximum _bf_scroll
                    mousewheel True
                    draggable True
                    scrollbars None

                    vbox:
                        spacing 0
                        xsize PH_CW

                        # Header
                        frame:
                            xsize PH_CW
                            background None
                            padding (12, 8)
                            vbox:
                                spacing 2
                                text _("UNPUBLISHED VIDEOS"):
                                    style "phone_text"
                                    size 16
                                    color "#8ca0b4"
                                    bold True
                                text _("Select a video to publish on your feed"):
                                    style "phone_text"
                                    size 13
                                    color "#555e6e"

                        null height 4

                        if not _bf_unpublished:
                            null height 50
                            text _("No videos available"):
                                style "phone_text"
                                size 18
                                color "#555e6e"
                                xalign 0.5
                            null height 4
                            text _("Record a video first"):
                                style "phone_text"
                                size 14
                                color "#3a3a4a"
                                xalign 0.5
                        else:
                            for _uv in _bf_unpublished:
                                python:
                                    _uv_girl = GIRL_BY_ID.get(_uv.get("girl_gid"))
                                    _uv_name = _uv_girl.Name if _uv_girl else _uv.get("girl_gid", "???")
                                    _uv_color = _uv_girl.color if _uv_girl and hasattr(_uv_girl, "color") else "#e2e8f0"
                                    _uv_special = _uv.get("special")
                                    _uv_type = _tr(SPECIAL_VIDEO_DISPLAY.get(_uv_special, VIDEO_TYPE_DISPLAY.get(_uv.get("type", "?"), _uv.get("type", "?")))) if _uv_special else _tr(VIDEO_TYPE_DISPLAY.get(_uv.get("type", "?"), _uv.get("type", "?")))
                                    _uv_title = "{color=%s}%s{/color} - %s" % (_uv_color, _uv_name, _uv_type)
                                    _uv_loc_map = {"campus": "Campus", "room": _tr("%s's Room") % store.Player.Name, "pool": _tr("Pool"), "showers": _tr("Showers"), "apartment": _tr("Apartment"), "apartment_room": _tr("Apartment Bedroom"), "apartment_shower": _tr("Apartment Bathroom"), "shower": _tr("Showers"), "gym": _tr("Gym"), "classroom": _tr("Classroom"), "mall": _tr("Mall"), "restaurant_restroom": _tr("Restaurant Restroom"), "dressing_room": _tr("Dressing Room"), "gwen_room": _tr("Gwen's Room"), "rogue_room": _tr("Rogue's Room"), "ntw_room": _tr("Negasonic's Room"), "tenny_room": _tr("%s's Room") % GIRL_BY_ID["tenny"].Name}
                                    _uv_loc = _uv_loc_map.get(_uv.get("location", ""), _uv.get("location", ""))
                                    _uv_dur = bigfans_video_duration({"vid": _uv, "published_day": Day})
                                    _uv_tags = []
                                    if not _uv.get("consensual", True):
                                        _uv_tags.append((_tr("secret"), "#facc15", "#facc1533"))
                                    if _uv.get("committed", False):
                                        _uv_tags.append((_tr("cheating"), "#f87171", "#f8717133"))
                                    if _is_public_location(_uv.get("location", "")):
                                        _uv_tags.append((_tr("public"), "#60a5fa", "#60a5fa33"))
                                    if _uv.get("hd", False):
                                        _uv_tags.append((_tr("HD"), "#38bdf8", "#38bdf833"))
                                    if _uv.get("cuckold", False):
                                        _uv_tags.append((_tr("cuckold"), "#a78bfa", "#a78bfa33"))
                                    elif _uv.get("threesome", False):
                                        _uv_tags.append((_tr("threesome"), "#fb923c", "#fb923c33"))
                                    if _uv.get("atm", False):
                                        _uv_tags.append((_tr("ATM"), "#f472b6", "#f472b633"))

                                button:
                                    xsize PH_CW - 16
                                    xalign 0.5
                                    background Frame("images/menus/bigfans/card_bg.png", 22, 22, 22, 22)
                                    hover_background Frame("images/menus/bigfans/card_bg.png", 22, 22, 22, 22)
                                    padding (12, 10)
                                    action [Function(bigfans_publish_video, _uv), SetScreenVariable("_bf_refresh", _bf_refresh + 1)]

                                    hbox:
                                        spacing 12
                                        yalign 0.5

                                        # Thumbnail
                                        fixed:
                                            xsize 80
                                            ysize 80
                                            add "images/menus/bigfans/thumbnail_bg.png"
                                            add "images/menus/bigfans/play_button.png":
                                                xalign 0.5
                                                yalign 0.5
                                                zoom 0.6

                                        # Info
                                        vbox:
                                            yalign 0.5
                                            spacing 4

                                            text "[_uv_title]":
                                                style "phone_text"
                                                size 18
                                                color "#e2e8f0"
                                                bold True

                                            hbox:
                                                spacing 8
                                                text "[_uv_loc]":
                                                    style "phone_text"
                                                    size 15
                                                    color "#8ca0b4"
                                                text "[_uv_dur]":
                                                    style "phone_text"
                                                    size 15
                                                    color "#94a3b8"

                                            if _uv_tags:
                                                hbox:
                                                    spacing 6
                                                    for _tag_name, _tag_color, _tag_bg in _uv_tags:
                                                        frame:
                                                            background Frame(_tag_bg, 10, 10, 10, 10)
                                                            padding (8, 4)
                                                            text "[_tag_name]":
                                                                style "phone_text"
                                                                size 13
                                                                color _tag_color
                                                                bold True

                                # Spacing
                                null height 8

            # ============================================
            # TAB: DMs  (fan request messages)
            # ============================================
            if _bf_tab == "requests":
                $ _bf_reqs = [r for r in getattr(Player, "bigfans_requests", []) if not r["fulfilled"] and r["expire_day"] >= Day]

                viewport:
                    xpos PH_CX
                    ypos _bf_body_y
                    xsize PH_CW
                    ymaximum _bf_scroll
                    mousewheel True
                    draggable True
                    scrollbars None

                    vbox:
                        spacing 0
                        xsize PH_CW

                        null height 6

                        if not _bf_reqs:
                            null height 50
                            text _("No messages yet"):
                                style "phone_text"
                                size 16
                                color "#555e6e"
                                xalign 0.5
                            null height 4
                            text _("Fans will DM you with requests"):
                                style "phone_text"
                                size 13
                                color "#3a3a4a"
                                xalign 0.5
                        else:
                            for _req in _bf_reqs:
                                python:
                                    _req_desc = bigfans_request_label(_req)
                                    _req_days = _req["expire_day"] - Day
                                    _req_days_str = _tr("%dd left") % _req_days if _req_days > 0 else _tr("Expires today!")
                                    _req_reward = _req["reward"]
                                    _req_phrase = _tl(_req.get("phrase", _("Send me something good")))
                                    _req_fan = _req["fan_name"]
                                    _req_initial = _req_fan[0].upper()
                                    _req_is_supporter = _req_fan in BIGFANS_SUPPORTERS
                                    if _req_is_supporter:
                                        _avatar_img = "images/menus/bigfans/avatar_circle_vip.png"
                                    else:
                                        _avatar_imgs = ["images/menus/bigfans/avatar_a.png", "images/menus/bigfans/avatar_b.png", "images/menus/bigfans/avatar_c.png"]
                                        _avatar_img = _avatar_imgs[hash(_req_fan) % len(_avatar_imgs)]

                                # Request card
                                $ _exp_color = "#f87171" if _req_days <= 0 else ("#6b5c3a" if _req_is_supporter else "#555e6e")

                                $ _card_png = "images/menus/bigfans/card_bg_vip.png" if _req_is_supporter else "images/menus/bigfans/card_bg.png"

                                frame:
                                    xsize PH_CW - 20
                                    xalign 0.5
                                    background Frame(_card_png, 22, 22, 22, 22)
                                    padding (14, 12)

                                    vbox:
                                        spacing 10
                                        xfill True

                                        # Row 1: Avatar + Name/Expiry/VIP + $amount
                                        hbox:
                                            xfill True

                                            hbox:
                                                spacing 10
                                                yalign 0.5

                                                fixed:
                                                    xsize 52
                                                    ysize 52
                                                    add _avatar_img
                                                    text "[_req_initial]":
                                                        style "phone_text"
                                                        size 20
                                                        color "#ffffff"
                                                        bold True
                                                        xalign 0.5
                                                        yalign 0.5

                                                vbox:
                                                    yalign 0.5
                                                    spacing 2
                                                    hbox:
                                                        spacing 6
                                                        text "[_req_fan]":
                                                            style "phone_text"
                                                            size 18
                                                            color ("#d4a017" if _req_is_supporter else "#e2e8f0")
                                                            bold True
                                                        if _req_is_supporter:
                                                            frame at vip_gold_shimmer:
                                                                yalign 0.5
                                                                background Frame("#d4a01755", 10, 10, 10, 10)
                                                                padding (6, 2)
                                                                text _("\u2B50 VIP"):
                                                                    style "phone_text"
                                                                    size 11
                                                                    color "#d4a017"
                                                                    bold True
                                                    text "[_req_days_str]":
                                                        style "phone_text"
                                                        size 14
                                                        color _exp_color

                                            null xfill True

                                            text "$[_req_reward]":
                                                style "phone_text"
                                                size 24
                                                color ("#d4a017" if _req_is_supporter else "#4ade80")
                                                bold True
                                                xalign 1.0
                                                yalign 0.5

                                        # Row 2: Message
                                        text "\"[_req_phrase]\"":
                                            style "phone_text"
                                            size 18
                                            color ("#a89070" if _req_is_supporter else "#8ca0b4")

                                        # Row 3: Tag + 2x PAY
                                        hbox:
                                            spacing 8
                                            frame:
                                                background Frame(("#d4a01733" if _req_is_supporter else "#e8467c33"), 12, 12, 12, 12)
                                                padding (10, 5)
                                                text "[_req_desc]":
                                                    style "phone_text"
                                                    size 14
                                                    color ("#d4a017" if _req_is_supporter else "#e8467c")
                                                    bold True
                                            if _req_is_supporter:
                                                frame:
                                                    background Frame("#d4a01733", 12, 12, 12, 12)
                                                    padding (10, 5)
                                                    text _("2\u00d7 PAY"):
                                                        style "phone_text"
                                                        size 14
                                                        color "#d4a017"
                                                        bold True

                                        # Row 4: Send Video (full width)
                                        button:
                                            xfill True
                                            ysize 44
                                            background Frame(("#d4a017" if _req_is_supporter else "#e8467c"), 14, 14, 14, 14)
                                            hover_background Frame(("#b8880f" if _req_is_supporter else "#cc3e6d"), 14, 14, 14, 14)
                                            action [Hide("phone_bigfans_screen"), Show("phone_bigfans_fill_screen", request=_req)]
                                            text _("Send Video"):
                                                style "phone_text"
                                                size 16
                                                color ("#1a1400" if _req_is_supporter else "#ffffff")
                                                bold True
                                                xalign 0.5
                                                yalign 0.5

                                # Spacing
                                null height 12

            # ============================================
            # TAB: Stats  (account dashboard + chart)
            # ============================================
            if _bf_tab == "account":
                python:
                    _bf_subs = getattr(Player, "bigfans_subscribers", 10)
                    _bf_total_earned = getattr(Player, "bigfans_total_earnings", 0)
                    _bf_pub_list = getattr(Player, "bigfans_published", [])
                    _bf_pub_count = len(_bf_pub_list)
                    _bf_total_views = sum(e["total_views"] for e in _bf_pub_list)
                    _bf_last_daily = getattr(store, "_bigfans_daily_earned", 0)
                    _bf_fulfilled_count = len([r for r in getattr(Player, "bigfans_requests", []) if r.get("fulfilled")])

                    # Earnings history for bar chart (last 7 days)
                    _bf_history = list(getattr(Player, "bigfans_earnings_history", []))
                    # Right-pad with empty if < 7
                    while len(_bf_history) < 7:
                        _bf_history.insert(0, {"day": 0, "earned": 0})
                    _bf_chart_data = _bf_history[-7:]
                    _bf_chart_max = 1
                    for _cd in _bf_chart_data:
                        if _cd["earned"] > _bf_chart_max:
                            _bf_chart_max = _cd["earned"]

                    # Per-video avg
                    _bf_avg_per_vid = int(_bf_total_earned / _bf_pub_count) if _bf_pub_count > 0 else 0

                    # Stat box width
                    _bf_box_w = int((PH_CW - 20) / 3)

                viewport:
                    xpos PH_CX
                    ypos _bf_body_y
                    xsize PH_CW
                    ymaximum _bf_scroll
                    mousewheel True
                    draggable True
                    scrollbars None

                    vbox:
                        spacing 6
                        xsize PH_CW
                        xpos 0

                        null height 6

                        # --- Total earnings hero ---
                        frame:
                            xsize PH_CW - 16
                            xalign 0.5
                            background Frame("images/menus/bigfans/card_bg_stats.png", 22, 22, 22, 22)
                            padding (14, 16)

                            vbox:
                                spacing 4
                                xfill True

                                text _("TOTAL EARNINGS"):
                                    style "phone_text"
                                    size 16
                                    color "#e8467caa"
                                    xalign 0.5
                                    bold True

                                text "$ [_bf_total_earned]":
                                    style "phone_text"
                                    size 36
                                    color "#e8467c"
                                    bold True
                                    xalign 0.5

                                null height 8

                                hbox:
                                    xfill True

                                    hbox:
                                        spacing 6
                                        text _("Today"):
                                            style "phone_text"
                                            size 15
                                            color "#8ca0b4"
                                            yalign 0.5
                                        text "+$[_bf_last_daily]":
                                            style "phone_text"
                                            size 20
                                            color "#4ade80"
                                            bold True
                                            yalign 0.5

                                    null xfill True

                                    hbox:
                                        spacing 6
                                        text _("Balance"):
                                            style "phone_text"
                                            size 15
                                            color "#8ca0b4"
                                            yalign 0.5
                                        text "$[Player.cash]":
                                            style "phone_text"
                                            size 20
                                            color "#facc15"
                                            bold True
                                            yalign 0.5

                        # --- Earnings bar chart ---
                        frame:
                            xsize PH_CW - 16
                            xalign 0.5
                            background Frame("images/menus/bigfans/card_bg_chart.png", 22, 22, 22, 22)
                            padding (12, 10)

                            vbox:
                                spacing 6
                                xsize PH_CW - 40

                                text _("LAST 7 DAYS"):
                                    style "phone_text"
                                    size 16
                                    color "#e2e8f0"
                                    bold True

                                # Bar chart — fixed height container
                                fixed:
                                    xsize PH_CW - 40
                                    ysize 100

                                    # 7 bars evenly spaced
                                    python:
                                        _bar_w = int((PH_CW - 40 - 36) / 7)  # ~50px each
                                        _bar_area_h = 70  # max bar height
                                        _label_h = 16  # space for day label at bottom
                                        _val_h = 14   # space for value label on top

                                    for _bi in range(7):
                                        $ _cd = _bf_chart_data[_bi]
                                        $ _bar_val = _cd["earned"]
                                        $ _bar_h = max(4, int(float(_bar_area_h) * _bar_val / _bf_chart_max)) if _bar_val > 0 else 4
                                        $ _bar_x = _bi * (_bar_w + 4) + 4
                                        $ _bar_day = _cd.get("day", 0)
                                        $ _bar_color = "#e8467c" if _bar_val > 0 else "#1c2333"

                                        # Bar
                                        frame:
                                            xpos _bar_x
                                            ypos 100 - _label_h - _bar_h
                                            xsize _bar_w
                                            ysize _bar_h
                                            background Frame(_bar_color, 3, 3, 3, 3)
                                            padding (0, 0)

                                        # Value on top of bar
                                        if _bar_val > 0:
                                            text "$[_bar_val]":
                                                style "phone_text"
                                                size 11
                                                color "#e8467ccc"
                                                xpos _bar_x
                                                xsize _bar_w
                                                text_align 0.5
                                                ypos 100 - _label_h - _bar_h - _val_h

                                        # Day label at bottom
                                        if _bar_day > 0:
                                            text "D[_bar_day]":
                                                style "phone_text"
                                                size 11
                                                color "#8ca0b4"
                                                xpos _bar_x
                                                xsize _bar_w
                                                text_align 0.5
                                                ypos 100 - _label_h + 1
                                        else:
                                            text "\u2014":
                                                style "phone_text"
                                                size 11
                                                color "#333"
                                                xpos _bar_x
                                                xsize _bar_w
                                                text_align 0.5
                                                ypos 100 - _label_h + 1

                        # --- Stats row (3 boxes) ---
                        python:
                            _bf_subs_fmt = bigfans_format_number(_bf_subs)
                            _bf_total_views_fmt = bigfans_format_number(_bf_total_views)
                        hbox:
                            xpos 8
                            spacing 4

                            frame:
                                xsize _bf_box_w
                                background Frame("images/menus/bigfans/card_bg_small.png", 16, 16, 16, 16)
                                padding (8, 14)
                                vbox:
                                    xalign 0.5
                                    spacing 4
                                    text "[_bf_subs_fmt]":
                                        style "phone_text"
                                        size 26
                                        color "#60a5fa"
                                        bold True
                                        xalign 0.5
                                    text _("Subscribers"):
                                        style "phone_text"
                                        size 13
                                        color "#8ca0b4"
                                        xalign 0.5

                            frame:
                                xsize _bf_box_w
                                background Frame("images/menus/bigfans/card_bg_small.png", 16, 16, 16, 16)
                                padding (8, 14)
                                vbox:
                                    xalign 0.5
                                    spacing 4
                                    text "[_bf_pub_count]":
                                        style "phone_text"
                                        size 26
                                        color "#e8467c"
                                        bold True
                                        xalign 0.5
                                    text _("Posts"):
                                        style "phone_text"
                                        size 13
                                        color "#8ca0b4"
                                        xalign 0.5

                            frame:
                                xsize _bf_box_w
                                background Frame("images/menus/bigfans/card_bg_small.png", 16, 16, 16, 16)
                                padding (8, 14)
                                vbox:
                                    xalign 0.5
                                    spacing 4
                                    text "[_bf_total_views_fmt]":
                                        style "phone_text"
                                        size 26
                                        color "#e2e8f0"
                                        bold True
                                        xalign 0.5
                                    text _("Views"):
                                        style "phone_text"
                                        size 13
                                        color "#8ca0b4"
                                        xalign 0.5

                        null height 4

                        # --- Details rows ---
                        frame:
                            xsize PH_CW - 16
                            xalign 0.5
                            background None
                            padding (8, 0)

                            vbox:
                                spacing 0
                                xfill True

                                # Avg earnings / post
                                frame:
                                    xfill True
                                    background None
                                    padding (8, 12)
                                    hbox:
                                        xfill True
                                        text _("Avg. earnings / post"):
                                            style "phone_text"
                                            size 16
                                            color "#8ca0b4"
                                            yalign 0.5
                                        null xfill True
                                        text "$[_bf_avg_per_vid]":
                                            style "phone_text"
                                            size 18
                                            color "#4ade80"
                                            bold True
                                            yalign 0.5

                                add "images/menus/bigfans/divider.png" xalign 0.5

                                # Requests sold
                                frame:
                                    xfill True
                                    background None
                                    padding (8, 12)
                                    hbox:
                                        xfill True
                                        text _("Pending requests"):
                                            style "phone_text"
                                            size 16
                                            color "#8ca0b4"
                                            yalign 0.5
                                        null xfill True
                                        text "[_bf_fulfilled_count]":
                                            style "phone_text"
                                            size 18
                                            color "#facc15"
                                            bold True
                                            yalign 0.5

                        null height 6

            use phone_chin_buttons(
                back_action=[Hide("phone_bigfans_screen"), Show("phone_screen")])


# -----------------------------------------------------------
# Phone BigFans — Fill Request sub-screen
# -----------------------------------------------------------
screen phone_bigfans_fill_screen(request):

    modal True
    zorder 200

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

            # --- Header bar ---
            frame:
                xpos PH_CX
                ypos PH_CY_HEADER
                xsize PH_CW
                ysize PH_HEADER_H
                background "#e8467c"
                padding (18, 12)

                vbox:
                    yalign 0.5
                    spacing 2
                    text _("Send Video"):
                        style "phone_text"
                        size PH_FONT_LG
                        color "#ffffff"
                        bold True

            # --- Request details ---
            $ _fill_desc = bigfans_request_label(request)
            $ _fill_reward = request["reward"]
            $ _fill_fan = request["fan_name"]
            $ _fill_phrase = _tl(request.get("phrase", _("Send me something good")))
            $ _fill_is_supporter = _fill_fan in BIGFANS_SUPPORTERS

            frame:
                xpos PH_CX
                ypos PH_CY_BODY
                xsize PH_CW
                background "#0f1318"
                padding (12, 10)

                vbox:
                    spacing 4
                    xfill True
                    hbox:
                        spacing 6
                        text "[_fill_fan]":
                            style "phone_text"
                            size 14
                            color ("#f59e0b" if _fill_is_supporter else "#e8467c")
                            bold True
                            yalign 0.5
                        null xfill True
                        text "$ [_fill_reward]":
                            style "phone_text"
                            size PH_FONT_XS
                            color "#4ade80"
                            bold True
                            yalign 0.5
                    text "\"[_fill_phrase]\"":
                        style "phone_text"
                        size 13
                        color "#8ca0b4"

            # --- Matching videos ---
            $ _all_vids = getattr(Player, "recorded_videos", [])
            $ _matching = [v for v in _all_vids if bigfans_video_matches_request(request, v)]
            $ _fill_body_y = PH_CY_BODY + 70

            viewport:
                xpos PH_CX
                ypos _fill_body_y
                xsize PH_CW
                ymaximum PH_SCROLL_H - 70
                mousewheel True
                draggable True
                scrollbars None

                vbox:
                    spacing 4
                    xsize PH_CW

                    null height 6

                    if not _matching:
                        null height 30
                        text _("No matching videos"):
                            style "phone_text"
                            size PH_FONT_SM
                            color "#555e6e"
                            xalign 0.5
                        text _("Record one and come back"):
                            style "phone_text"
                            size 13
                            color "#3a3a4a"
                            xalign 0.5
                    else:
                        for _mv in _matching:
                            python:
                                _mv_girl = GIRL_BY_ID.get(_mv.get("girl_gid"))
                                _mv_name = _mv_girl.Name if _mv_girl else _mv.get("girl_gid", "???")
                                _mv_special = _mv.get("special")
                                _mv_type = _tr(SPECIAL_VIDEO_DISPLAY.get(_mv_special, VIDEO_TYPE_DISPLAY.get(_mv.get("type", "?"), _mv.get("type", "?")))) if _mv_special else _tr(VIDEO_TYPE_DISPLAY.get(_mv.get("type", "?"), _mv.get("type", "?")))
                                _mv_color = _mv_girl.color if _mv_girl and hasattr(_mv_girl, "color") else "#c8d0de"
                                _mv_title = "{color=%s}%s{/color} - %s" % (_mv_color, _mv_name, _mv_type)

                            button:
                                xsize PH_CW - 14
                                xalign 0.5
                                background Frame("#0f1318", 8, 8, 8, 8)
                                hover_background Frame("#e8467c22", 8, 8, 8, 8)
                                padding (0, 0)
                                action [Function(bigfans_fulfill_request, request, _mv), Hide("phone_bigfans_fill_screen"), Show("phone_bigfans_screen", initial_tab="requests")]

                                hbox:
                                    spacing 0
                                    yalign 0.5

                                    # Mini thumbnail
                                    frame:
                                        xsize 60
                                        ysize 44
                                        background "#1a1f2e"
                                        padding (0, 0)
                                        add "images/menus/VideoBF.png":
                                            zoom 0.2
                                            xalign 0.5
                                            yalign 0.5

                                    frame:
                                        xfill True
                                        ysize 44
                                        background None
                                        padding (8, 4)
                                        vbox:
                                            yalign 0.5
                                            spacing 1
                                            text "[_mv_title]":
                                                style "phone_text"
                                                size 13
                                                color "#c8d0de"
                                            text _("Tap to send"):
                                                style "phone_text"
                                                size 11
                                                color "#4ade8088"

            use phone_chin_buttons(
                back_action=[Hide("phone_bigfans_fill_screen"), Show("phone_bigfans_screen", initial_tab="requests")])


# -----------------------------------------------------------
# Phone Shop — main category selection
# -----------------------------------------------------------
screen phone_shop_screen():

    modal True
    zorder 200

    # Clear "bought" feedback after 1s
    if getattr(store, "_shop_bought_id", ""):
        timer 1.0 action Function(_phone_shop_clear_bought)

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

            # --- Header (phone UI kit) with the cash on the right ---
            use pk_header(_tl(_("Shop")), "#4ade80", "bag"):
                use pk_chip("$%d" % Player.cash, "#4ade80")

            # --- All items (scrollable) ---
            # Buy feedback: flash green when last purchase timestamp is recent
            $ _shop_bought_at = getattr(store, "_shop_bought_at", 0.0)
            $ _shop_bought_id = getattr(store, "_shop_bought_id", "")

            $ _shop_body_y = PH_CY_HEADER + _PK_HEADER_H + 6
            $ _shop_scroll = _PH_SCREEN_BOTTOM - _shop_body_y

            viewport:
                xpos PH_CX
                ypos _shop_body_y
                xsize PH_CW
                ymaximum _shop_scroll
                mousewheel True
                draggable True
                scrollbars None

                vbox:
                    spacing 6
                    xsize PH_CW

                    null height 6

                    # ── Section: Condoms ──
                    hbox:
                        xpos 10
                        spacing 8
                        yalign 0.5
                        text "\U0001F6E1":
                            size PH_FONT_SM
                            yalign 0.5
                        text _("Condoms"):
                            style "phone_text"
                            size PH_FONT_SM
                            color "#60a5fa"
                            bold True
                            yalign 0.5

                    for _item in SHOP_CATALOG["condoms"]["items"]:
                        $ _can_buy = Player.cash >= _item["price"]
                        $ _c_lbl = _item["label"]
                        $ _c_price = "$%d" % _item["price"]
                        $ _c_stock = Player.get_item_count(_item["id"])
                        $ _c_just_bought = (_shop_bought_id == _item["id"])

                        frame:
                            xsize _PK_CARD_W
                            xalign 0.5
                            background _pk_card_bg("#4ade80" if _c_just_bought else None)
                            padding (12, 10, 12, 10)

                            hbox:
                                xfill True
                                yalign 0.5

                                vbox:
                                    yalign 0.5
                                    spacing 1
                                    text _c_lbl:
                                        style "phone_text"
                                        size PH_FONT_XS
                                        color ("#e2e8f0" if _can_buy else "#555e6e")
                                    text _("In stock: [_c_stock]"):
                                        style "phone_text"
                                        size 14
                                        color ("#4ade80" if _c_just_bought else "#8ca0b4")

                                if _c_just_bought:
                                    frame:
                                        xalign 1.0
                                        yalign 0.5
                                        xsize 90
                                        ysize 34
                                        background _pk_pill("#4ade80", 0.24)
                                        text _("Bought"):
                                            style "phone_text"
                                            size PH_FONT_TINY
                                            color "#4ade80"
                                            bold True
                                            xalign 0.5
                                            yalign 0.5
                                elif _can_buy:
                                    button:
                                        xalign 1.0
                                        yalign 0.5
                                        xsize 90
                                        ysize 34
                                        background _pk_pill("#4ade80", 0.16)
                                        hover_background _pk_pill("#4ade80", 0.32)
                                        action [Function(_phone_shop_buy, _item["id"], _item["qty"], _item["price"])]
                                        text _c_price:
                                            style "phone_text"
                                            size PH_FONT_TINY
                                            color "#4ade80"
                                            xalign 0.5
                                            yalign 0.5
                                else:
                                    frame:
                                        xalign 1.0
                                        yalign 0.5
                                        xsize 90
                                        ysize 34
                                        background _pk_pill("#64748b", 0.14)
                                        text _c_price:
                                            style "phone_text"
                                            size PH_FONT_TINY
                                            color "#3a3a4a"
                                            xalign 0.5
                                            yalign 0.5

                    # ── Section: Pharmacy (only when pregnancy mode active) ──
                    if store._pregnancy_mode != "off":
                        null height 8

                        hbox:
                            xpos 10
                            spacing 8
                            yalign 0.5
                            text "\U0001F48A":
                                size PH_FONT_SM
                                yalign 0.5
                            text _tr("Pharmacy"):
                                style "phone_text"
                                size PH_FONT_SM
                                color "#f472b6"
                                bold True
                                yalign 0.5

                        for _item in SHOP_CATALOG["pharmacy"]["items"]:
                            $ _can_buy = Player.cash >= _item["price"]
                            $ _rx_lbl = _tr(_item["label"])
                            $ _rx_price = "$%d" % _item["price"]
                            $ _rx_stock = Player.get_item_count(_item["id"])
                            $ _rx_just_bought = (_shop_bought_id == _item["id"])
                            $ _rx_is_vitamin = (_item["id"] == "fertility_vitamin")

                            frame:
                                xsize PH_CW - 16
                                xalign 0.5
                                background _pk_card_bg("#f472b6" if _rx_just_bought else None)
                                padding (12, 10, 12, 10)

                                hbox:
                                    xfill True
                                    yalign 0.5

                                    vbox:
                                        yalign 0.5
                                        spacing 1
                                        text _rx_lbl:
                                            style "phone_text"
                                            size PH_FONT_XS
                                            color ("#e2e8f0" if _can_buy else "#555e6e")
                                        text _("In stock: [_rx_stock]"):
                                            style "phone_text"
                                            size 14
                                            color ("#f472b6" if _rx_just_bought else "#8ca0b4")

                                    if _rx_just_bought:
                                        frame:
                                            xalign 1.0
                                            yalign 0.5
                                            xsize 90
                                            ysize 34
                                            background _pk_pill("#f472b6", 0.24)
                                            text _("Bought"):
                                                style "phone_text"
                                                size PH_FONT_TINY
                                                color "#f472b6"
                                                bold True
                                                xalign 0.5
                                                yalign 0.5
                                    elif _can_buy:
                                        button:
                                            xalign 1.0
                                            yalign 0.5
                                            xsize 90
                                            ysize 34
                                            background _pk_pill("#f472b6", 0.16)
                                            hover_background _pk_pill("#f472b6", 0.32)
                                            if _rx_is_vitamin:
                                                action [Function(_phone_shop_buy_vitamin, _item["id"], _item["qty"], _item["price"])]
                                            else:
                                                action [Function(_phone_shop_buy, _item["id"], _item["qty"], _item["price"])]
                                            text _rx_price:
                                                style "phone_text"
                                                size PH_FONT_TINY
                                                color "#f472b6"
                                                xalign 0.5
                                                yalign 0.5
                                    else:
                                        frame:
                                            xalign 1.0
                                            yalign 0.5
                                            xsize 90
                                            ysize 34
                                            background _pk_pill("#64748b", 0.14)
                                            text _rx_price:
                                                style "phone_text"
                                                size PH_FONT_TINY
                                                color "#3a3a4a"
                                                xalign 0.5
                                                yalign 0.5

                    null height 8

                    # ── Section: Drinks ──
                    hbox:
                        xpos 10
                        spacing 8
                        yalign 0.5
                        text "\U0001F37E":
                            size PH_FONT_SM
                            yalign 0.5
                        text _("Drinks"):
                            style "phone_text"
                            size PH_FONT_SM
                            color "#fbbf24"
                            bold True
                            yalign 0.5

                    for _item in SHOP_CATALOG["drinks"]["items"]:
                        $ _can_buy = Player.cash >= _item["price"]
                        $ _d_lbl = _tr(_item["label"])
                        $ _d_price = "$%d" % _item["price"]
                        $ _d_stock = Player.get_item_count(_item["id"])
                        $ _d_just_bought = (_shop_bought_id == _item["id"])
                        $ _d_info = DRINKS.get(_item["id"])
                        $ _d_buzz = {"low": _tr("light buzz"), "med": _tr("strong buzz"), "high": _tr("heavy buzz")}.get(_d_info["tier"], "") if _d_info else ""
                        $ _d_meta = ("%s ABV · %s" % (_d_info["abv"], _d_buzz)) if _d_info else ""

                        frame:
                            xsize _PK_CARD_W
                            xalign 0.5
                            background _pk_card_bg("#fbbf24" if _d_just_bought else None)
                            padding (12, 10, 12, 10)

                            hbox:
                                xfill True
                                yalign 0.5

                                vbox:
                                    yalign 0.5
                                    spacing 1
                                    text _d_lbl:
                                        style "phone_text"
                                        size PH_FONT_XS
                                        color ("#e2e8f0" if _can_buy else "#555e6e")
                                    if _d_meta:
                                        text "[_d_meta]":
                                            style "phone_text"
                                            size 13
                                            color "#8ca0b4"
                                    text _("In stock: [_d_stock]"):
                                        style "phone_text"
                                        size 14
                                        color ("#fbbf24" if _d_just_bought else "#8ca0b4")

                                if _d_just_bought:
                                    frame:
                                        xalign 1.0
                                        yalign 0.5
                                        xsize 90
                                        ysize 34
                                        background _pk_pill("#fbbf24", 0.24)
                                        text _("Bought"):
                                            style "phone_text"
                                            size PH_FONT_TINY
                                            color "#fbbf24"
                                            bold True
                                            xalign 0.5
                                            yalign 0.5
                                elif _can_buy:
                                    button:
                                        xalign 1.0
                                        yalign 0.5
                                        xsize 90
                                        ysize 34
                                        background _pk_pill("#fbbf24", 0.16)
                                        hover_background _pk_pill("#fbbf24", 0.32)
                                        action [Function(_phone_shop_buy, _item["id"], _item["qty"], _item["price"])]
                                        text _d_price:
                                            style "phone_text"
                                            size PH_FONT_TINY
                                            color "#fbbf24"
                                            xalign 0.5
                                            yalign 0.5
                                else:
                                    frame:
                                        xalign 1.0
                                        yalign 0.5
                                        xsize 90
                                        ysize 34
                                        background _pk_pill("#64748b", 0.14)
                                        text _d_price:
                                            style "phone_text"
                                            size PH_FONT_TINY
                                            color "#3a3a4a"
                                            xalign 0.5
                                            yalign 0.5

                    null height 8

                    # ── Section: Gifts ──
                    hbox:
                        xpos 10
                        spacing 8
                        yalign 0.5
                        text "\U0001F381":
                            size PH_FONT_SM
                            yalign 0.5
                        text _("Gifts"):
                            style "phone_text"
                            size PH_FONT_SM
                            color "#f472b6"
                            bold True
                            yalign 0.5

                    python:
                        _GIFT_ICONS = {
                            "chocolate": "\U0001F36B",
                            "flowers":   "\U0001F490",
                            "perfume":   "\U0001F9F4",
                            "necklace":  "\U0001F4FF",
                            "handbag":   "\U0001F45C",
                            "ring":      "\U0001F48D",
                            "watch":     "⌚",
                            "jewelry_set": "\U0001F48E",
                        }

                    for _item in SHOP_CATALOG["gifts"]["items"]:
                        $ _can_buy = Player.cash >= _item["price"]
                        $ _owned = Player.get_item_count(_item["id"])
                        $ _lbl = _item["label"]
                        $ _price_lbl = "$%d" % _item["price"]
                        $ _g_icon = _GIFT_ICONS.get(_item["id"], "\U0001F381")
                        $ _g_just_bought = (_shop_bought_id == _item["id"])

                        frame:
                            xsize _PK_CARD_W
                            xalign 0.5
                            background _pk_card_bg("#f472b6" if _g_just_bought else None)
                            padding (12, 10, 12, 10)

                            hbox:
                                xfill True
                                yalign 0.5
                                spacing 8

                                frame:
                                    xsize 28
                                    yalign 0.5
                                    background None
                                    padding (0, 0)
                                    text _g_icon:
                                        size PH_FONT_SM
                                        xalign 0.5

                                vbox:
                                    yalign 0.5
                                    spacing 1
                                    text _lbl:
                                        style "phone_text"
                                        size PH_FONT_XS
                                        color ("#e2e8f0" if _can_buy else "#555e6e")
                                    if _owned > 0:
                                        text _("Owned: [_owned]"):
                                            style "phone_text"
                                            size 14
                                            color ("#f472b6" if _g_just_bought else "#8ca0b4")
                                    else:
                                        text _("Not owned"):
                                            style "phone_text"
                                            size 14
                                            color "#555e6e"

                                if _g_just_bought:
                                    frame:
                                        xalign 1.0
                                        yalign 0.5
                                        xsize 90
                                        ysize 34
                                        background _pk_pill("#f472b6", 0.24)
                                        text _("Bought"):
                                            style "phone_text"
                                            size PH_FONT_TINY
                                            color "#f472b6"
                                            bold True
                                            xalign 0.5
                                            yalign 0.5
                                elif _can_buy:
                                    button:
                                        xalign 1.0
                                        yalign 0.5
                                        xsize 90
                                        ysize 34
                                        background _pk_pill("#f472b6", 0.16)
                                        hover_background _pk_pill("#f472b6", 0.32)
                                        action [Function(_phone_shop_buy, _item["id"], _item["qty"], _item["price"])]
                                        text _price_lbl:
                                            style "phone_text"
                                            size PH_FONT_TINY
                                            color "#f472b6"
                                            xalign 0.5
                                            yalign 0.5
                                else:
                                    frame:
                                        xalign 1.0
                                        yalign 0.5
                                        xsize 90
                                        ysize 34
                                        background _pk_pill("#64748b", 0.14)
                                        text _price_lbl:
                                            style "phone_text"
                                            size PH_FONT_TINY
                                            color "#3a3a4a"
                                            xalign 0.5
                                            yalign 0.5

                    null height 8

                    # ── Sections: "Gifts for <girl>" (PHONE_SHOP_GIRL_SECTIONS, shop.rpy): one loop
                    # for every girl, her accent color per row; a girl whose optional route is off
                    # (girl_route_enabled) has no section ──
                    for _gs_cat, _gs_gid, _gs_col in PHONE_SHOP_GIRL_SECTIONS:
                        $ _gs_girl = GIRL_BY_ID.get(_gs_gid)
                        if _gs_girl is not None and girl_route_enabled(_gs_girl):
                            hbox:
                                xpos 10
                                spacing 8
                                yalign 0.5
                                text "\U0001F48E":
                                    size PH_FONT_SM
                                    yalign 0.5
                                text _tl(SHOP_CATALOG[_gs_cat]["label"]):
                                    style "phone_text"
                                    size PH_FONT_SM
                                    color _gs_col
                                    bold True
                                    yalign 0.5

                            for _item in SHOP_CATALOG[_gs_cat]["items"]:
                                $ _lbl = _item["label"]
                                $ _price_lbl = "$%d" % _item["price"]
                                $ _g_just_bought = (_shop_bought_id == _item["id"])
                                $ _already_purchased = _is_unique_gift_purchased(_item["id"])
                                $ _can_buy = Player.cash >= _item["price"] and not _already_purchased

                                frame:
                                    xsize _PK_CARD_W
                                    xalign 0.5
                                    background _pk_card_bg(_gs_col if _g_just_bought else None)
                                    padding (12, 10, 12, 10)

                                    hbox:
                                        xfill True
                                        yalign 0.5
                                        spacing 8

                                        vbox:
                                            yalign 0.5
                                            spacing 1
                                            text _lbl:
                                                style "phone_text"
                                                size PH_FONT_XS
                                                color ("#e2e8f0" if _can_buy and not _already_purchased else "#555e6e")
                                            if _already_purchased:
                                                text _("Purchased"):
                                                    style "phone_text"
                                                    size 14
                                                    color _gs_col
                                            else:
                                                text _("Special gift"):
                                                    style "phone_text"
                                                    size 14
                                                    color "#555e6e"

                                        if _g_just_bought:
                                            frame:
                                                xalign 1.0
                                                yalign 0.5
                                                xsize 90
                                                ysize 34
                                                background _pk_pill(_gs_col, 0.24)
                                                text _("Bought"):
                                                    style "phone_text"
                                                    size PH_FONT_TINY
                                                    color _gs_col
                                                    bold True
                                                    xalign 0.5
                                                    yalign 0.5
                                        elif _already_purchased:
                                            frame:
                                                xalign 1.0
                                                yalign 0.5
                                                xsize 90
                                                ysize 34
                                                background _pk_pill("#64748b", 0.14)
                                                text "✔":
                                                    style "phone_text"
                                                    size PH_FONT_TINY
                                                    color (_gs_col + "88")
                                                    xalign 0.5
                                                    yalign 0.5
                                        elif _can_buy:
                                            button:
                                                xalign 1.0
                                                yalign 0.5
                                                xsize 90
                                                ysize 34
                                                background _pk_pill(_gs_col, 0.16)
                                                hover_background _pk_pill(_gs_col, 0.32)
                                                action [Function(_phone_shop_buy_unique, _item["id"], _item["qty"], _item["price"])]
                                                text _price_lbl:
                                                    style "phone_text"
                                                    size PH_FONT_TINY
                                                    color _gs_col
                                                    xalign 0.5
                                                    yalign 0.5
                                        else:
                                            frame:
                                                xalign 1.0
                                                yalign 0.5
                                                xsize 90
                                                ysize 34
                                                background _pk_pill("#64748b", 0.14)
                                                text _price_lbl:
                                                    style "phone_text"
                                                    size PH_FONT_TINY
                                                    color "#3a3a4a"
                                                    xalign 0.5
                                                    yalign 0.5

                            null height 8

            use phone_chin_buttons(
                back_action=[Function(_phone_shop_clear_bought), Hide("phone_shop_screen"), Show("phone_screen")])


# -----------------------------------------------------------
# Phone trait editor — add/remove traits per girl
# -----------------------------------------------------------
screen phone_trait_editor(girl):

    modal True
    zorder 210

    button:
        xfill True
        yfill True
        background "#00000088"
        action Hide("phone_trait_editor")

    frame:
        xalign 0.5
        yalign 0.4
        padding (20, 16)
        background Frame("#1a1a2eee", 6, 6, 6, 6)
        xminimum 320

        vbox:
            spacing 10

            text _("[girl.Name] - TRAITS"):
                style "phone_text"
                size 16
                color "#c084fc"
                xalign 0.5

            null height 4

            viewport:
                ymaximum PH_SCROLL_H
                mousewheel True
                draggable True
                scrollbars None

                vbox:
                    spacing 10

                    # List all traits from TRAIT_DEFS
                    for _tid in sorted(TRAIT_DEFS.keys()):
                        $ _tdef = TRAIT_DEFS[_tid]
                        $ _has = _tid in getattr(girl, "traits", set())
                        $ _lbl = TRAIT_HUD_LABELS.get(_tid, _tid[:3].upper())
                        $ _clr = TRAIT_HUD_COLORS.get(_tid, "#8ca0b4") if _has else "#555555"
                        $ _desc_clr = "#8ca0b4" if _has else "#444444"

                        hbox:
                            spacing 8
                            xalign 0.0
                            yalign 0.5

                            if _has:
                                textbutton "[[−]":
                                    text_style "phone_text"
                                    text_size 14
                                    text_color "#f87171"
                                    text_hover_color "#fca5a5"
                                    yalign 0.5
                                    action [Function(_toggle_trait, girl, _tid), Hide("phone_trait_editor"), Show("phone_trait_editor", girl=girl)]
                            else:
                                textbutton "[[+]":
                                    text_style "phone_text"
                                    text_size 14
                                    text_color "#4ade80"
                                    text_hover_color "#86efac"
                                    yalign 0.5
                                    action [Function(_toggle_trait, girl, _tid), Hide("phone_trait_editor"), Show("phone_trait_editor", girl=girl)]

                            text "[_lbl]":
                                style "phone_text"
                                size 13
                                color _clr
                                yalign 0.5

                            text _tdef["desc"]:
                                style "phone_text"
                                size 10
                                color _desc_clr
                                yalign 0.5

            null height 6

            textbutton _("Close"):
                text_style "phone_text"
                text_size 14
                text_color "#60a5fa"
                text_hover_color "#93c5fd"
                xalign 0.5
                action Hide("phone_trait_editor")


# -----------------------------------------------------------
# Cum tracker overlay (right side during sex)
# -----------------------------------------------------------
screen cum_tracker_hud():

    zorder 60

    $ _cum_items = session_cum_visible_items()

    if _cum_items:
        frame:
            xalign 1.0
            yalign 0.35
            xoffset -20
            padding (12, 8)
            background Frame("#1a1a2ecc", 6, 6, 6, 6)
            xminimum 120

            vbox:
                spacing 4

                text _("CUM"):
                    style "phone_text"
                    size 14
                    color "#f472b6"
                    xalign 0.5

                for _name, _count in _cum_items:
                    hbox:
                        spacing 6
                        xalign 0.5
                        text "[_name]":
                            style "phone_text"
                            size 13
                            color "#e2e8f0"
                        text "[_count]":
                            style "phone_text"
                            size 13
                            color "#fb923c"


transform _rec_dot_blink:
    alpha 1.0
    pause 0.6
    linear 0.3 alpha 0.0
    pause 0.2
    linear 0.3 alpha 1.0
    repeat

screen recording_overlay():
    zorder 999

    frame:
        background None
        xalign 0.98
        yalign 0.96
        padding (16, 10, 20, 10)

        hbox:
            spacing 10
            yalign 0.5

            # Red blinking dot with black outline
            fixed:
                xsize 22
                ysize 22
                yalign 0.57
                add Solid("#000000", xsize=22, ysize=22) xpos -2 ypos -2 at _rec_dot_blink
                add Solid("#ff2020", xsize=18, ysize=18) at _rec_dot_blink

            text _("REC") size 28 color "#ff2020" bold True yalign 0.5 outlines [(2, "#000", 0, 0)]

            $ _rec_m, _rec_s = _recording_current_duration()
            text "%d:%02d" % (_rec_m, _rec_s) size 24 color "#ff6060" bold True yalign 0.5 outlines [(2, "#000", 0, 0)]


screen narration_panel(msg):
    zorder 200

    frame:
        style "narration_box"
        text msg


# -----------------------------------------------------------
# Phone Inventory screen
# -----------------------------------------------------------
# phone_inventory_screen: lives in screen_phone_inventory.rpy (phone UI kit)


style tut_tab_scrollbar is scrollbar:
    base_bar Solid("#d4c87a22")
    thumb Solid("#d4c87a")
    ysize 6
    thumb_offset 0

# -----------------------------------------------------------
# Phone Tutorial screen
# -----------------------------------------------------------
screen phone_tutorial_screen():

    modal True
    zorder 200

    default _tut_tab = "player"

    $ _tut_header_h = _PK_HEADER_H
    $ _tut_nav_h = 50
    $ _tut_nav_total = _tut_nav_h + 10
    $ _tut_body_y = PH_CY_HEADER + _tut_header_h + _tut_nav_total + 4
    $ _tut_nav_y = PH_CY_HEADER + _tut_header_h + 2
    $ _tut_bottom = _PH_SCREEN_BOTTOM
    $ _tut_scroll = _tut_bottom - _tut_body_y

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

            # --- Header (phone UI kit) ---
            use pk_header(_tl(_("Tutorial")), "#d4c87a", "book")

            # --- Tab navigation ---
            frame:
                xpos PH_CX
                ypos _tut_nav_y
                xsize PH_CW
                ysize _tut_nav_total
                background "#0b1220"
                padding (0, 0)

                # Top border
                frame:
                    xpos 0
                    ypos 0
                    xsize PH_CW
                    ysize 1
                    background "#ffffff0a"

                viewport:
                    style_prefix "tut_tab"
                    xsize PH_CW
                    ysize _tut_nav_total
                    mousewheel "horizontal"
                    draggable True
                    scrollbars "horizontal"

                    hbox:
                        ysize _tut_nav_h
                        spacing 0

                        python:
                            _tut_tabs = [
                                ("player", _("Player")),
                                ("girls", _("Girls")),
                                ("traits", _tr("Traits")),
                                ("intimacy", _("Intimacy")),
                                ("time", _("Time")),
                                ("energy", _("Energy")),
                                ("exam", _("Exams")),
                                ("bigfans", _("BigFans")),
                                ("gifts", _("Items")),
                                ("weekly", _("Weekly")),
                                ("achieve", _("Achievements")),
                                ("paths", _("Paths")),
                            ]

                        for _tt_id, _tt_label in _tut_tabs:
                            button:
                                xsize int(PH_CW * 0.29)
                                ysize _tut_nav_h
                                background ("#d4c87a22" if _tut_tab == _tt_id else None)
                                hover_background "#ffffff08"
                                action SetScreenVariable("_tut_tab", _tt_id)
                                text _tt_label:
                                    style "phone_text"
                                    size 14
                                    color ("#d4c87a" if _tut_tab == _tt_id else "#8ca0b4")
                                    bold (_tut_tab == _tt_id)
                                    xalign 0.5
                                    yalign 0.5

            # --- Content area ---
            viewport:
                xpos PH_CX
                ypos _tut_body_y
                xsize PH_CW
                ymaximum _tut_scroll
                mousewheel True
                draggable True
                scrollbars None

                vbox:
                    spacing 0
                    xsize PH_CW

                    # ======= PLAYER STATS =======
                    if _tut_tab == "player":
                        use _tut_section(_("Your Stats"))

                        use _tut_entry(_("Cash  $"), _("Your money. Earn it through BigFans and Friday paychecks ($100/week). Spend on gifts, condoms, and shop items."))

                        use _tut_entry(_("Energy"), _("Your daily stamina. Each activity costs energy. You recover energy when you Wait, and it fully resets when you Sleep. Manage it wisely. When it hits 0, you're done for the day."))

                        use _tut_entry(_("Max Energy"), _("Starts at 2, can go up to 5. Do 5+ gym workouts in a week to increase it by 1. If you slack off (under 3 workouts), you lose 1 max energy on Sunday."))

                        use _tut_entry(_("Study Level"), _("Your exam prep score. Increases by attending class (+1) or studying in your room (+1). Study with a girl for +2. Resets to 0 after each exam."))

                        use _tut_entry(_("Inventory"), _("Holds condoms, gifts, and recorded videos. Use the phone apps to check and manage it."))

                        use _tut_entry(_("Player Trait"), _("At the start of the game, you choose one trait for your character:\n\n{b}Athlete{/b}: Start with higher Max Energy.\n{b}Fast Learner{/b}: Study more effectively.\n{b}Investor{/b}: Start with extra cash and earn daily passive income.\n{b}Charming{/b}: Girls start with a Love bonus.\n{b}No Trait{/b}: No bonuses, pure challenge.\n\nYour choice shapes your early game strategy."))

                    # ======= GIRL STATS =======
                    if _tut_tab == "girls":
                        use _tut_section(_("Girl Stats"))

                        use _tut_entry(_("Love  (0-1000)"), _("Romantic affection. Grows through chatting, gifts, and time together. Higher Love unlocks new interactions, phone number, dating, and eventually exclusive relationships."))

                        use _tut_entry(_("Obedience  (0-1000)"), _("How willing she is to follow your lead. Affects how easily she agrees to requests and responds to dominant actions."))

                        use _tut_entry(_("Inhibition  (0-1000)"), _("How much her psychological barriers have broken down. Higher Inhibition means she resists less when pressured into acts she would normally refuse."))

                        use _tut_entry(_("Lust  (0-100)"), _("Sexual arousal. Rises during flirting and sex scenes. At 100 she orgasms and it resets. If it stays high and she's alone, she may relieve herself off-screen."))

                        use _tut_entry(_("Relationship"), _("Starts as strangers. Progress to dating, then exclusive. Some girls already have a boyfriend when you meet them. Cheating raises Suspicion. Get caught and she (or her boyfriend) may confront you."))

                        use _tut_entry(_("Jealousy"), _("Girls can become jealous when they find out you are involved with others. Jealousy affects how she reacts during threesomes, multi-girl hangouts, and harem proposals. Monogamous girls are more jealous by nature, while Polyamorous girls handle sharing much better."))

                        use _tut_entry(_tr("Traits"), _tr("Each girl has personality traits that shape her behavior, dialogue, approval thresholds, and scene outcomes. Check the {b}Traits{/b} tab for a full glossary."))

                    # ======= TRAITS GLOSSARY =======
                    if _tut_tab == "traits":
                        use _tut_section(_tr("Personality Traits (Opposing Pairs)"))

                        use _tut_entry(_tr("Camera Lover"), _tr("Loves being filmed. She may ask to be recorded and reacts positively to it. Cannot be blackmailed if she's single, since she doesn't care about leaked videos."))

                        use _tut_entry(_tr("Camera Hater"), _tr("Hates cameras. Very resistant to being filmed. Much harder to get recording consent. If she catches you recording, the consequences are worse."))

                        use _tut_entry(_tr("Cum Lover"), _tr("Loves cum inside her and hates condoms. She may try to force a creampie during sex. Reacts very positively to raw sex and finishing inside."))

                        use _tut_entry(_tr("Cum Hater"), _tr("Hates any contact with cum. Demands condoms every time. Reacts very negatively to creampies and removing condoms."))

                        use _tut_entry(_tr("Public Fetish"), _tr("Turned on by public exposure and risk. Easier to seduce in public locations. Approval gets a bonus in public areas."))

                        use _tut_entry(_tr("Public Shy"), _tr("Terrified of being seen. Much harder to convince for anything sexual in public. Stronger negative reaction if caught."))

                        use _tut_entry(_tr("Hardcore"), _tr("Prefers rough, fast, intense sex. Higher pleasure from fast speeds. Dialogue and reactions reflect her preference for dominance."))

                        use _tut_entry(_tr("Gentle"), _tr("Prefers slow, intimate, gentle sex. Higher pleasure from slow speeds. Reacts negatively to overly rough or degrading actions."))

                        use _tut_entry(_tr("Loyal"), _tr("Strongly resists cheating on her partner. Much harder to corrupt. High approval thresholds for sexual acts while she has a boyfriend/girlfriend. Can evolve into Cheater through corruption over time."))

                        use _tut_entry(_tr("Cheater"), _tr("Cheating is easy and even enjoyable for her. Lower approval thresholds for acts while she has a partner. Less guilt after cheating."))

                        use _tut_entry(_tr("Anal Lover"), _tr("Loves anal sex. Gets more pleasure from it and may ask for it. Lower thresholds for anal acts."))

                        use _tut_entry(_tr("Anal Hater"), _tr("Hates and fears anal. Focused on pain over pleasure. Very high thresholds and strong resistance to anal acts."))

                        use _tut_entry(_tr("Poor"), _tr("Struggles financially. Gifts have a stronger effect on her. She's more open to financial persuasion after enough gifts, and her prices are lower."))

                        use _tut_entry(_tr("Rich"), _tr("Wealthy background. Hard to impress with gifts. She's more resistant to financial persuasion, requires more gifts to unlock it, and her prices are higher."))

                        use _tut_entry(_tr("Heavy Drinker"), _tr("Holds her liquor. Alcohol affects her far less, so she gets drunk slowly and rarely gets sick. During Truth or Dare you'll need to keep the drinks coming to loosen her up."))

                        use _tut_entry(_tr("Lightweight"), _tr("Low tolerance. She gets drunk fast and gets sick easily, so a few drinks go a long way. Push her too hard and she'll be sick and done for the night."))

                        use _tut_section(_tr("Special Traits"))

                        use _tut_entry(_tr("Naive"), _tr("Completely inexperienced. Has never done anything sexual, not even a handjob. Forces Virgin trait. Her boyfriend (if any) has zero sexual history with her."))

                        use _tut_entry(_tr("Virgin"), _tr("Has not had penetrative sex yet. A special scene plays during her first time. Her reaction depends on your approach and her personality."))

                        use _tut_entry(_tr("Experienced"), _tr("Has done everything before with someone else. Not a virgin and knows what she's doing. Cannot coexist with Virgin or Naive."))

                        use _tut_entry(_tr("Voyeur"), _tr("Likes watching others. May react differently during scenes involving multiple people."))

                        use _tut_entry(_tr("Exhibitionist"), _tr("Likes being watched. Gets aroused by the idea of someone seeing her."))

                        use _tut_entry(_tr("Lesbian"), _tr("Only attracted to women. Love does NOT help with sexual acts. Only Obedience and Inhibition count. She must progress through acts in order. Kissing is the LAST act unlocked, not the first. Her resistance decays with each act. Asking for sexual acts costs Love."))

                        use _tut_entry(_tr("Bisexual"), _tr("Attracted to both men and women. Can have a boyfriend or a girlfriend. Uses normal hetero mechanics for everything. No special thresholds or restrictions."))

                        use _tut_entry(_tr("Has a Boyfriend"), _tr("She already has a boyfriend at game start. You need to build Temptation to get past her loyalty. Her boyfriend may catch you, confront you, or react to rumors."))

                        use _tut_entry(_tr("Has a Girlfriend"), _tr("She already has a girlfriend at game start. Works similarly to having a boyfriend but with a female NPC partner."))

                        use _tut_entry(_tr("Polyamorous"), _tr("Open to sharing. She can accept a harem arrangement where the player dates multiple girls at once. Less jealous in multi-girl scenarios and threesomes."))

                        use _tut_entry(_tr("Monogamous"), _tr("Wants exclusivity. She demands a committed relationship and reacts badly if she discovers the player is with other girls. Higher jealousy during threesomes and multi-girl situations."))

                    # ======= INTIMACY / SEX =======
                    if _tut_tab == "intimacy":
                        use _tut_section(_("Intimacy & Sex"))

                        use _tut_entry(_("Approval"), _("Every action you attempt (kiss, touch, sex, etc.) runs an approval check using the girl's Love, Obedience, and Inhibition. Each act has its own threshold. Higher stats mean she's more likely to accept."))

                        use _tut_entry(_("Progression"), _("More intimate acts require higher stats. Start with lighter interactions and work your way up. Skipping steps is possible but requires much higher stats than going in order."))

                        use _tut_entry(_("Oral"), _("During cowgirl, you can go down on her (cunnilingus). Oral has its own approval checks and is tracked as a separate act. Her reaction depends on her traits and arousal level."))

                        use _tut_entry(_("Boyfriends"), _("Some girls have a boyfriend. To do anything intimate with them, you need to build Temptation. Flirt, touch, and keep trying even when denied. Each attempt raises her Temptation, making her more willing to cross the line."))

                        use _tut_entry(_("Temptation  (0-10)"), _("Measures how close a girl with a boyfriend is to giving in. Grows naturally through flirting, touching, and time spent together. Lighter acts require less Temptation, while going all the way requires much more. Temptation is separate from approval. Both must pass for her to accept."))

                        use _tut_entry(_("Heat  (0-100)"), _("A hidden desire meter for girls with boyfriends. Heat builds when she denies your advances, when you refuse her counter-offers, and from completing intimate acts together. Higher Heat makes her more willing to cross boundaries she normally wouldn't.\n\nHeat gain is limited per session, decays slowly over time, and she never fully forgets how far she's been pushed."))

                        use _tut_entry(_("Counter-Offers"), _("When you ask for an act she's not ready for (like sex when she's only done rubbing), she may offer a lesser act instead. You can accept her offer or refuse. Refusing gives a large Heat boost (+20), pushing her closer to accepting next time."))

                        use _tut_entry(_("Cheat Stages"), _("Girls with boyfriends progress through intimacy step by step across separate sessions. You can follow the natural progression, or skip stages entirely if her Heat is high enough."))

                        use _tut_entry(_("Lesbian Girls"), _("Lesbian girls are not attracted to men. Love does NOT help with sexual acts. Only Obedience and Inhibition count.\n\nShe must progress through acts in order, from lighter to harder. Each act she performs unlocks the possibility of the next one. Harder acts require higher Obedience to bypass. Kissing is the LAST act, not the first, because it is the most intimate for her. You cannot force a kiss through Obedience alone.\n\nHer resistance starts very high and decays with each act she performs. Lower resistance means lower thresholds for the next act. Every sexual act chips away at her defenses.\n\nAsking a lesbian for sexual acts costs Love. The more intimate the request, the more Love you lose. This means pushing for sex too aggressively can lock you out of kissing later.\n\n{b}Tip{/b}: Flirt and tease her to raise her Lust, then leave. If her Lust stays high and she's alone in her room or the showers, she may relieve herself. Catch her in the act for an easier first scene."))

                        use _tut_entry(_("Blackmail"), _("After a lesbian (or any girl) denies you, you may see a 'Blackmail her' option if you have recorded videos of her.\n\nBlackmail leverage depends on the type of videos you have. Heavier acts give more leverage. Each act she denies has its own difficulty. Your leverage must exceed the difficulty to succeed.\n\nThe first blackmail is easier (she's shocked), but each success makes the next one harder. Failed blackmail has consequences: she kicks you out, gets angry for 2 days, and you lose Love.\n\nFor lesbians specifically, blackmail leverage also adds a permanent bonus to approval checks, making future acts progressively easier even without actively blackmailing her."))

                        use _tut_entry(_("First Video Tip"), _("Getting your first recorded video of a lesbian is crucial. She will almost never consent to being filmed, so you will likely need to record secretly.\n\nStart a scene with a lighter act she accepts (handjob, rub). During the scene, hit Record. If she catches you, there will be consequences, but the video is still saved. That single video unlocks blackmail as a tool for everything that follows.\n\nOnce you have leverage, you can blackmail her into harder acts, record those acts, and build even more leverage. The cycle gets easier over time."))

                        use _tut_entry(_("Raising Obedience"), _("Obedience is the primary stat for lesbian sexual acts. Ways to raise it:\n- Dominant dialogue choices during conversations\n- Ordering her around (she may resist, but it still adds Obed)\n- Successful sexual acts raise Obedience\n- Blackmail success builds compliance over time\n\nInhibition also matters. It is the secondary stat for coerced acts and helps push past resistance when Obedience alone is not enough."))

                        use _tut_entry(_("Love vs Obedience"), _("With lesbian girls, Love and Obedience can work against each other. Every time you ask for a sexual act, you lose Love. The harder the act, the more Love you lose.\n\nThis creates a choice:\n- {b}Obedience path{/b}: Push for sexual acts early and often. You unlock scenes faster through blackmail and compliance, but your Love stays low. Kissing becomes very hard to reach since it requires very high Love.\n- {b}Love path{/b}: Build the relationship slowly through chatting and gifts. You get closer to kissing requirements, but without Obedience you cannot unlock the acts that lead to it.\n\nThe ideal strategy is a balance: raise Love through social interactions while gradually pushing Obedience through dominant choices. Use blackmail sparingly to avoid tanking Love too fast. Be patient."))

                        use _tut_entry(_("Virginity"), _("Some girls are virgins. When you have sex with a virgin for the first time, a special scene plays where she experiences her first penetration. Her reaction depends on your approach and her personality."))

                        use _tut_entry(_("Condoms"), _("Buy condoms at the shop ($15 each, $75 for 6). Some girls require them. During a scene, you may be able to remove the condom if her Obedience is high enough. Raw sex and creampies have stronger reactions."))

                        use _tut_entry(_("Stealth Removal"), _("In certain positions where the girl can't see you directly, you can try to secretly remove the condom without asking. Whether she notices depends on her arousal, the speed of the scene, and her traits. If she doesn't notice, the scene continues as raw sex silently. If she catches on, she reacts based on her personality."))

                        use _tut_entry(_("Condom Break"), _("When a condom breaks, you notice it before she does. You can choose to {b}tell her{/b} or {b}hide it{/b} and keep going.\n\nIf you hide it, she may discover the truth when you switch positions or when you finish. Her reaction depends on her traits and how she feels about you. You can try excuses, but whether she believes you varies."))

                        use _tut_entry(_("Focus  (0-100)"), _("Your arousal during sex scenes. Rises with each action. When it reaches 100, a voluntary Cum button appears. You can keep going, but each additional action risks losing control. Higher Max Energy makes it easier to hold on. If you lose control, the outcome depends on the position and condom state."))

                        use _tut_entry(_("Edge / Denial"), _("If you stop a scene while the girl is highly aroused, she may beg you to keep going. You can deny her and leave. Denying her multiple times in a row escalates her begging from pleading to desperate.\n\nRepeated denial affects her stats and can unlock an achievement."))

                        use _tut_entry(_("Recording"), _("You can secretly record sex scenes with your phone. Hit 'Record' during a scene to start. Recorded videos can be sold or published on BigFans. If she catches you recording, there will be consequences."))

                        use _tut_entry(_("Firsts"), _("The game tracks every 'first' act with each girl. When you're her first for something (first kiss, first sex, first anal, etc.), a discovery banner appears. Being her first in something her boyfriend never did gives extra stat bonuses."))

                        use _tut_entry(_("Threesomes"), _("If you are dating two girls who get along, you can set up a threesome. Both girls need enough affection and low enough jealousy to agree.\n\nDuring a threesome, one girl is active while the other watches. You can switch between them. The watching girl reacts based on her traits. Jealous girls may comment or get upset if you seem to favor the other.\n\nPolyamorous and Voyeur traits make threesomes much easier. Monogamous girls almost always refuse."))

                    # ======= TIME / DAY =======
                    if _tut_tab == "time":
                        use _tut_section(_("Time & Day System"))

                        use _tut_entry(_("Time Slots"), _("Each day has 4 periods: Morning, Midday, Evening, and Night. Actions spend time. Once you reach Night, the next advance puts you to sleep and starts a new day."))

                        use _tut_entry(_("Actions & Rounds"), _("Each action costs Round points. Every 100 points = 1 time slot. Plan your day around the 4 slots you have."))

                        use _tut_entry(_("Waiting"), _("Waiting advances time by 1 slot. You recover +1 energy when waiting. Girls may move to different locations between slots."))

                        use _tut_entry(_("Girl Schedules"), _("Girls follow daily schedules and move between locations each period. Check the HUD to see where each girl is right now."))

                        use _tut_entry(_("Day of the Week"), _("The week cycles Sunday through Saturday. Fridays bring paychecks and exams. Sundays check your gym routine."))

                    # ======= ENERGY =======
                    if _tut_tab == "energy":
                        use _tut_section(_("Energy System"))

                        use _tut_entry(_("How It Works"), _("You start each day with energy equal to your Max Energy. Almost every activity costs 1 energy. When you reach 0, you can only Wait or Sleep."))

                        use _tut_entry(_("Recovery"), _("You regain +1 energy each time you Wait. Sleeping fully restores your energy to max."))

                        use _tut_entry(_("Max Energy"), _("Your maximum starts at 2 and can reach 5. It increases when you do 5+ gym workouts in a week, and decreases if you do fewer than 3."))

                        use _tut_entry(_("Strategy"), _("Early game you only have 2 energy per day. Choose your actions carefully. Prioritize the gym to raise your max. At 5 energy you can do much more each day."))

                    # ======= EXAMS =======
                    if _tut_tab == "exam":
                        use _tut_section(_("Exam System"))

                        use _tut_entry(_("When"), _("Exams happen every 14 days, on Friday at Midday. The first exam is Day 13. A notification warns you in advance."))

                        use _tut_entry(_("Grades"), _("Your grade depends on your Study Level when the exam hits:\n- 10+ = A\n- 7-9 = B\n- 5-6 = C\n- 3-4 = D\n- 0-2 = F\nStudy Level resets to 0 after each exam."))

                        use _tut_entry(_("How to Study"), _("Attend class for +1 Study Level. Study solo in your room for +1 (+2 with Fast Learner). Study with a girl for +2 (+4 with Fast Learner). Girls study on their own when they're home alone."))

                        use _tut_entry(_("Girl Exams"), _("Girls with high Love may invite or insist you join them for the exam. At very high Love + Inhibition, you can convince them to skip it entirely."))

                    # ======= BIGFANS =======
                    if _tut_tab == "bigfans":
                        use _tut_section(_("BigFans"))

                        use _tut_entry(_("Overview"), _("BigFans is your main income source. Record videos during sex scenes, then publish or sell them through the app."))

                        use _tut_entry(_("Publishing (Feed)"), _("Publish videos to your feed for daily passive income. Each video earns views and money every day, with newer videos earning more. Builds subscribers over time."))

                        use _tut_entry(_("Fan Requests (DMs)"), _("Fans send requests for specific video types. Fulfill them by matching a recorded video to their criteria for instant cash. New requests appear daily."))

                        use _tut_entry(_("Video Value"), _("Riskier content pays more. Creampies earn the most, masturbation the least. Secret recordings and cheating scenarios add bonus value."))

                        use _tut_entry(_("Strategy"), _("Early game: sell videos for quick cash. Later: publish everything to build passive income. A diverse catalog and more subscribers = more daily earnings."))

                    # ======= GIFTS =======
                    if _tut_tab == "gifts":
                        use _tut_section(_("Items & Economy"))

                        use _tut_entry(_("Gifts"), _("Gifts raise a girl's stats. More expensive gifts give bigger boosts, and each type favors different stats. Giving enough gifts also unlocks Financial Persuasion."))

                        use _tut_entry(_("Financial Persuasion"), _("After enough gifts, a girl may accept money for sexual acts when she denies you. Poor girls unlock this faster. She names a price based on the act, her traits, and past transactions."))

                        use _tut_entry(_("Condoms"), _("Regular condoms are reliable and very rarely break. Some girls require them, and using one avoids creampie scenarios.\n\n{b}Japanese Condoms{/b} are ultra-thin and feel almost like raw sex, but they break easily. When a condom breaks, you notice first and must decide: tell her, or keep going and hope she doesn't find out."))

                        use _tut_entry(_("Drinks"), _("Buy drinks at the shop to host a Hangout Night. There are 3 tiers:\n\n{b}Low{/b} ($50): Cools Light, Alinmus\n{b}Medium{/b} ($70): Xitos Vodka, HunterMaster\n{b}High{/b} ($120): Running Douglas, UnusualAlias\n\nStronger drinks raise the drunk meter faster. The sweet spot is levels 5-10, where approval bonuses cap out. Over-drinking only adds sick risk with no extra benefit. Heavy Drinkers fill slower, Lightweights fill faster."))

                        use _tut_entry(_("Hangout Night"), _("Create a group chat with 2-3 girls and use 'Invite for drinks' to schedule a Hangout Night. If a girl has a partner, the NPC may join too (up to 3 screen slots total).\n\nDuring the hangout, everyone plays Truth or Dare. Colored bars at the top track each person's drink level. Alcohol makes girls bolder and more likely to pick Dare.\n\nNPC partners spin, answer truths, and do mild dares (funny dance, cheek kiss), but cannot strip. If an NPC drinks too much, they pass out, leaving you alone with the girls."))

                        use _tut_entry(_("Dinner Date"), _("Invite a girl to dinner via phone DMs or in person (up to 2 girls). At the restaurant you order food, talk, and build your relationship. You choose who pays at the end.\n\nDinner dates raise Love without costing energy on gifts. Special events can happen during dinner."))

                        use _tut_entry(_("Income"), _("Your income comes from BigFans (main source) and a weekly paycheck. Spend wisely early. Gifts are investments in relationships."))

                    # ======= WEEKLY =======
                    if _tut_tab == "weekly":
                        use _tut_section(_("Weekly Events"))

                        use _tut_entry(_("Friday"), _("Payday! You receive $100 automatically. Exams also happen on Fridays (every 14 days)."))

                        use _tut_entry(_("Sunday"), _("Gym check! The game counts your weekly workouts:\n- Under 3: you lose 1 Max Energy\n- 3-4: no change\n- 5+: you gain 1 Max Energy (up to 5)"))

                        use _tut_entry(_("Daily"), _("Each new day: your energy resets, girls move to their scheduled spots, BigFans generates passive income, and new fan requests may appear."))

                        use _tut_entry(_("Lust Cycle"), _("Girls gain 3-8 Lust daily. If a girl's Lust is above 80 and she's alone, she relieves herself (drops to 15-30). Keep an eye on timing for interactions."))

                    # ======= ACHIEVEMENTS =======
                    if _tut_tab == "achieve":
                        use _tut_section(_("Achievements"))

                        use _tut_entry(_("Overview"), _("The game has 40+ achievements across 3 categories: Campus, Intimate, and Dark Path. They are persistent across saves. A banner appears on screen when you unlock one."))

                        use _tut_entry(_("Categories"), _("{b}Campus{/b}: Social milestones like getting a girlfriend, acing exams, gym goals, and hosting hangouts.\n{b}Intimate{/b}: Sexual firsts, positions, threesomes, and special scenarios.\n{b}Dark Path{/b}: Blackmail, financial coercion, cheating, NTR milestones, and recording."))

                    # ======= PATHS / STRATEGY =======
                    if _tut_tab == "paths":
                        use _tut_section(_("Progression Paths"))

                        use _tut_entry(_("Building Stats"), _("Sex is not the only way to raise stats. Classroom events, conversations, gifts, and dominant dialogue choices all contribute to Obedience and Love. A balanced approach is often more effective than forcing sexual encounters."))

                        use _tut_entry(_("Hetero Girls (Single)"), _("Single hetero girls respond to Love, Obedience, and Inhibition equally. Build Love through chatting, gifts, and spending time together. Higher Love means she accepts more intimate acts willingly. This is the most straightforward path."))

                        use _tut_entry(_("Girls with Boyfriends"), _("Girls in relationships are blocked by loyalty. You need to build Temptation through flirting, touching, and persistence. Each denied attempt raises her Heat, making her more willing next time.\n\nProgression goes through stages: rubbing, then tip, then sex, then anal. Each stage must be reached in a separate session. Counter-offers let her suggest a lighter act when she is not ready for what you asked.\n\nHer boyfriend may catch you. If he does, the relationship may end, or she may talk her way out of it. Multiple catches increase the breakup chance."))

                        use _tut_entry(_("Lesbian Girls"), _("Lesbians are NOT attracted to men. Love does NOT influence sexual approval. Only Obedience and Inhibition matter.\n\nThey cannot be seduced, only broken down over time. Each act must be unlocked in order, and harder acts require higher Obedience. Kissing is the LAST act unlocked, not the first, because it is the most intimate for her.\n\nEven when a lesbian accepts, she does it out of submission, not desire. Her reactions reflect confusion and internal conflict, not attraction.\n\n{b}Tip{/b}: Classroom events, dominant dialogue choices, and ordering her around all raise Obedience without costing Love. Use these before pushing for sexual acts."))

                        use _tut_entry(_("NTR Partners"), _("Some NPC partners have the NTR trait. When this partner discovers the player is involved with their girl (through being caught or receiving a video), instead of breaking up, they set boundaries on what is allowed.\n\nThe partner must DISCOVER the acts first. Send them a face-visible video, or get caught by them during a scene. Only then will they send a message establishing their limits.\n\nBoundary levels range from 'non-penetrative only' to 'everything allowed'. The trust bar fills as they witness or receive videos of within-bounds acts. When the bar fills, the boundary level increases.\n\n{b}Note{/b}: NTR boundaries only apply to hetero and bisexual girls, not lesbians."))

                        use _tut_entry(_("Financial Coercion"), _("After a girl denies a sexual act, you may offer money. She names a price based on the act, her traits, and her financial situation. Poor girls accept more easily and at lower prices.\n\nHer financial attitude progresses through 4 stages: Reluctant (shocked), Resigned (tired acceptance), Transactional (business-like, discounts), and Dependent (she initiates the offer).\n\nAt higher stages she may counter-offer a lighter act at a discount. This is a separate system from approval and works even when stats are too low."))

                        use _tut_entry(_("Blackmail"), _("After a girl denies you, 'Blackmail her' appears if you have recorded videos. Heavier acts give more leverage.\n\nFor lesbians, blackmail also adds a permanent bonus to future approval checks, making each success compound.\n\nTo get your first video: start a lighter act she accepts, then hit Record during the scene. Even if caught, the video is saved."))

                        use _tut_entry(_("Obedience Tips"), _("Obedience rises from many sources, not just sex:\n- Dominant dialogue choices in conversations\n- Ordering her to do things (even if she resists)\n- Classroom events where you assert control\n- Successful blackmail builds compliance\n- Each completed sexual act raises Obedience\n\nFor lesbians especially, social dominance is more efficient than forcing scenes early."))

                        use _tut_entry(_("Public Scenes"), _("Having sex in public locations draws attention. Busier areas and peak hours mean higher risk. Each action during a scene builds up how much attention you draw.\n\nIf you draw too much attention, someone catches you. The consequences depend on the location. Girls with Public Fetish enjoy the risk, while Public Shy girls panic and react much worse."))

                        use _tut_entry(_("Harem"), _("If you are dating multiple girls, you can attempt to form a harem where all your girlfriends know about and accept each other.\n\nTo propose, create a group chat with your girlfriends. Each girl votes based on her traits, jealousy, and how she feels about the others. Polyamorous girls accept easily. Monogamous girls almost always refuse.\n\nOnce a harem is formed, jealousy penalties between members are removed and you can freely interact with all of them without cheating consequences."))

                        use _tut_entry(_("Sleepovers"), _("When it's Night and you are in a girl's room (or she's in yours), a sleepover can happen if your relationship is close enough. She stays the night, and you can interact before sleeping.\n\nMultiple girls can sleep over if they are compatible. Jealousy, traits, and how the girls feel about each other all factor in."))

                        use _tut_entry(_("Activity Buddy"), _("Some girls may invite you to join their routine activities based on their personality. Studious girls invite you to study together, athletic girls invite you to work out.\n\nAccepting builds your relationship and gives stat bonuses. After enough shared sessions, you establish a routine and the bonuses increase."))

                        use _tut_entry(_("NPC Confrontation"), _("If a girl's boyfriend catches you with her, he may confront you physically. The outcome depends on your physical condition: being athletic or having high energy gives you an advantage.\n\nA confrontation can end peacefully or escalate. Hostile boyfriends are harsher. Friendly ones may let it slide the first time."))

                        use _tut_entry(_("Rod's Choice"), _("When starting a new game, you can pick a Rod's Choice preset instead of configuring traits manually. Each preset sets up all girls' traits, NPC dispositions, and player trait for a specific play style.\n\nPresets are named after supporters and target specific achievements. You can also randomize traits or pick them one by one."))

                    null height 20

        use phone_chin_buttons(
            back_action=[Hide("phone_tutorial_screen"), Show("phone_screen")])




# -----------------------------------------------------------
# Phone Cheat Code screen
# -----------------------------------------------------------
default _cheat_input_text = ""
default _cheat_msg = ""
default _cheat_msg_color = "#f87171"
default _cheat_history = []

screen phone_cheat_screen():

    modal True
    zorder 200

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

            # --- Header (phone UI kit) ---
            use pk_header(_tl(_("Cheats")), "#f87171", "bolt")

            # --- Input area ---
            $ _cheat_body_y = PH_CY_HEADER + _PK_HEADER_H + 6

            frame:
                xpos PH_CX
                ypos _cheat_body_y
                xsize PH_CW
                ysize _PH_SCREEN_BOTTOM - _cheat_body_y
                background "#060d11"
                padding (14, 20)

                vbox:
                    spacing 16
                    xsize PH_CW - 28
                    xalign 0.5

                    frame:
                        xsize PH_CW - 40
                        xalign 0.5
                        background Frame("#1a1a0a", 8, 8, 8, 8)
                        padding (10, 8)

                        text _("Warning: cheats speed up progression, but many mechanics depend on natural growth. Girls are expected to deny you sometimes. We recommend adding stats gradually instead of maxing them all at once."):
                            style "phone_text"
                            size PH_FONT_XXS
                            color "#c9b458"
                            text_align 0.5
                            xalign 0.5

                    text _("Enter cheat code:"):
                        style "phone_text"
                        size PH_FONT_SM
                        color "#8ca0b4"
                        xalign 0.5

                    frame:
                        xsize PH_CW - 40
                        xalign 0.5
                        background Frame("#1a1f2e", 10, 10, 10, 10)
                        padding (12, 8)

                        input:
                            value VariableInputValue("_cheat_input_text")
                            length 30
                            color "#ffffff"
                            size 20
                            xalign 0.5

                    textbutton _("Activate"):
                        xalign 0.5
                        xsize PH_CW - 60
                        ysize 42
                        background Frame("#2a0a0a", 12, 12, 12, 12)
                        hover_background Frame("#3d1414", 12, 12, 12, 12)
                        text_style "phone_text"
                        text_size 18
                        text_color "#f87171"
                        text_xalign 0.5
                        sensitive len(_cheat_input_text.strip()) > 0
                        action Function(_apply_cheat_code)

                    # !t: a plain message is an English _() marker, translated here (see _apply_cheat_code)
                    if _cheat_msg:
                        text "[_cheat_msg!t]":
                            style "phone_text"
                            size PH_FONT_XS
                            color _cheat_msg_color
                            xalign 0.5
                            text_align 0.5

                    if _cheat_history:
                        null height 12

                        hbox:
                            xsize PH_CW - 40
                            xalign 0.5
                            yalign 0.5
                            spacing 6
                            frame:
                                ysize 1
                                yalign 0.5
                                xsize 80
                                background "#2a3545"
                            text _("Recent"):
                                style "phone_text"
                                size PH_FONT_XXS
                                color "#4b5e72"
                                yalign 0.5
                            frame:
                                ysize 1
                                yalign 0.5
                                xfill True
                                background "#2a3545"

                        null height 6

                        viewport:
                            xsize PH_CW - 40
                            xalign 0.5
                            ysize min(len(_cheat_history) * 44, 220)
                            mousewheel True
                            scrollbars "vertical"

                            vbox:
                                spacing 6
                                xsize PH_CW - 56
                                for _ch_entry in _cheat_history:
                                    textbutton _ch_entry:
                                        xsize PH_CW - 56
                                        ysize 40
                                        background Frame("#141c28", 10, 10, 10, 10)
                                        hover_background Frame("#1e2a3a", 10, 10, 10, 10)
                                        text_style "phone_text"
                                        text_size PH_FONT_XS
                                        text_color "#6889a8"
                                        text_hover_color "#a0c4e0"
                                        text_xalign 0.5
                                        text_yalign 0.5
                                        action [SetVariable("_cheat_input_text", _ch_entry), Function(_apply_cheat_code)]

            use phone_chin_buttons(
                back_action=[SetVariable("_cheat_input_text", ""), SetVariable("_cheat_msg", ""), Hide("phone_cheat_screen"), Show("phone_screen")])


init python:

    def _apply_cheat_code():
        # _cheat_msg: a plain message is only marked _() (the screen shows it with [_cheat_msg!t]); one with
        # numbers is translated BEFORE they go in (_tl_fmt), so its old/new pair still matches.
        _raw = store._cheat_input_text.strip().lower()
        store._cheat_input_text = ""

        _parts = _raw.split(None, 1)
        code = _parts[0] if _parts else ""
        _arg = _parts[1].strip() if len(_parts) > 1 else ""

        _amount = None
        if _arg:
            try:
                _amount = int(_arg)
            except ValueError:
                pass

        _OLD_CHEATS = {"mrkrabs", "mooscles", "thiccgoth", "nogloves", "hiwade", "somedrama", "touchstarved", "hiwade100", "isthatcody", "isthatscott", "isthatyukio"}
        if code in _OLD_CHEATS:
            store._cheat_msg = _("Rod is sad because you don't read the changelog. +100 Guilt")
            store._cheat_msg_color = "#f87171"
            return

        if code == "liftheavystone":
            store.Player.energy_max = 5
            store.Player.energy = 5
            store._cheat_msg = _tl_fmt(_("Max energy! Energy: %d/%d"), store.Player.energy, store.Player.energy_max)
            store._cheat_msg_color = "#4ade80"

        elif code == "gimmemoney":
            if _amount is None or _amount <= 0:
                store._cheat_msg = _("Usage: gimmemoney [amount]")
                store._cheat_msg_color = "#f87171"
            else:
                store.Player.add_cash(_amount)
                store._cheat_msg = _tl_fmt(_("$$$ +%d cash! Balance: $%d"), _amount, store.Player.cash)
                store._cheat_msg_color = "#4ade80"

        elif code == "bigtitsgoth":
            g = GIRL_BY_ID.get("gwen")
            if not g:
                store._cheat_msg = _("Gwen not found.")
                store._cheat_msg_color = "#f87171"
            elif _amount is None or _amount == 0:
                store._cheat_msg = _("Usage: bigtitsgoth [amount]")
                store._cheat_msg_color = "#f87171"
            else:
                Change_Status(g, "Love", _amount, raw=True)
                Change_Status(g, "Obed", _amount, raw=True)
                Change_Status(g, "Inbt", _amount, raw=True)
                store._cheat_msg = _tl_fmt(_("Gwen %+d! Love=%d Obed=%d Inbt=%d"), _amount, g.Love, g.Obed, g.Inbt)
                store._cheat_msg_color = "#4ade80"

        elif code == "touchtouch":
            g = GIRL_BY_ID.get("rogue")
            if not g:
                store._cheat_msg = _("Rogue not found.")
                store._cheat_msg_color = "#f87171"
            elif _amount is None or _amount == 0:
                store._cheat_msg = _("Usage: touchtouch [amount]")
                store._cheat_msg_color = "#f87171"
            else:
                Change_Status(g, "Love", _amount, raw=True)
                Change_Status(g, "Obed", _amount, raw=True)
                Change_Status(g, "Inbt", _amount, raw=True)
                store._cheat_msg = _tl_fmt(_("Rogue %+d! Love=%d Obed=%d Inbt=%d"), _amount, g.Love, g.Obed, g.Inbt)
                store._cheat_msg_color = "#4ade80"

        elif code == "canonlesbian":
            g = GIRL_BY_ID.get("ntw")
            if not g:
                store._cheat_msg = _("NTW not found.")
                store._cheat_msg_color = "#f87171"
            elif _amount is None or _amount == 0:
                store._cheat_msg = _("Usage: canonlesbian [amount]")
                store._cheat_msg_color = "#f87171"
            else:
                Change_Status(g, "Love", _amount, raw=True)
                Change_Status(g, "Obed", _amount, raw=True)
                Change_Status(g, "Inbt", _amount, raw=True)
                store._cheat_msg = _tl_fmt(_("NTW %+d! Love=%d Obed=%d Inbt=%d"), _amount, g.Love, g.Obed, g.Inbt)
                store._cheat_msg_color = "#f5c842"

        elif code == "sgophers":
            g = GIRL_BY_ID.get("gwen")
            if g:
                Change_Status(g, "Lust", 80)
                store._cheat_msg = _tl_fmt(_("Gwen +80 Lust! Lust=%d"), g.Lust)
                store._cheat_msg_color = "#4ade80"
            else:
                store._cheat_msg = _("Gwen not found.")
                store._cheat_msg_color = "#f87171"

        elif code == "xxxmansion":
            g = GIRL_BY_ID.get("rogue")
            if g:
                Change_Status(g, "Lust", 80)
                store._cheat_msg = _tl_fmt(_("Rogue +80 Lust! Lust=%d"), g.Lust)
                store._cheat_msg_color = "#4ade80"
            else:
                store._cheat_msg = _("Rogue not found.")
                store._cheat_msg_color = "#f87171"

        elif code == "yukioparadise":
            g = GIRL_BY_ID.get("ntw")
            if g:
                Change_Status(g, "Lust", 80)
                store._cheat_msg = _tl_fmt(_("NTW +80 Lust! Lust=%d"), g.Lust)
                store._cheat_msg_color = "#f5c842"
            else:
                store._cheat_msg = _("NTW not found.")
                store._cheat_msg_color = "#f87171"

        elif code == "gothnetori":
            npc = NPC_PARTNERS.get("npc_bf_gwen") or NPC_PARTNERS.get("npc_gf_gwen")
            if npc:
                npc.friendship_with_player = 1000
                store._cheat_msg = _("Gwen's partner friendship maxed! (1000)")
                store._cheat_msg_color = "#4ade80"
            else:
                store._cheat_msg = _("Gwen has no partner.")
                store._cheat_msg_color = "#f87171"

        elif code == "gwenisangel":
            npc = NPC_PARTNERS.get("npc_bf_gwen") or NPC_PARTNERS.get("npc_gf_gwen")
            if npc:
                npc.suspicion = 0
                store._cheat_msg = _("Gwen's partner suspicion cleared! (0)")
                store._cheat_msg_color = "#4ade80"
            else:
                store._cheat_msg = _("Gwen has no partner.")
                store._cheat_msg_color = "#f87171"

        elif code == "friendlytouch":
            npc = NPC_PARTNERS.get("npc_bf_rogue") or NPC_PARTNERS.get("npc_gf_rogue")
            if npc:
                npc.friendship_with_player = 1000
                store._cheat_msg = _("Rogue's partner friendship maxed! (1000)")
                store._cheat_msg_color = "#4ade80"
            else:
                store._cheat_msg = _("Rogue has no partner.")
                store._cheat_msg_color = "#f87171"

        elif code == "canttouchthis":
            npc = NPC_PARTNERS.get("npc_bf_rogue") or NPC_PARTNERS.get("npc_gf_rogue")
            if npc:
                npc.suspicion = 0
                store._cheat_msg = _("Rogue's partner suspicion cleared! (0)")
                store._cheat_msg_color = "#4ade80"
            else:
                store._cheat_msg = _("Rogue has no partner.")
                store._cheat_msg_color = "#f87171"

        elif code == "yukiobff":
            npc = NPC_PARTNERS.get("npc_gf_ntw") or NPC_PARTNERS.get("npc_bf_ntw")
            if npc:
                npc.friendship_with_player = 1000
                store._cheat_msg = _("NTW's partner friendship maxed! (1000)")
                store._cheat_msg_color = "#f5c842"
            else:
                store._cheat_msg = _("NTW has no partner.")
                store._cheat_msg_color = "#f87171"

        elif code == "behindyukio":
            npc = NPC_PARTNERS.get("npc_gf_ntw") or NPC_PARTNERS.get("npc_bf_ntw")
            if npc:
                npc.suspicion = 0
                store._cheat_msg = _("NTW's partner suspicion cleared! (0)")
                store._cheat_msg_color = "#f5c842"
            else:
                store._cheat_msg = _("NTW has no partner.")
                store._cheat_msg_color = "#f87171"

        elif code == "luckyred":
            g = GIRL_BY_ID.get("tenny")
            if not g:
                store._cheat_msg = _("Tenny not found.")
                store._cheat_msg_color = "#f87171"
            elif _amount is None or _amount == 0:
                store._cheat_msg = _("Usage: luckyred [amount]")
                store._cheat_msg_color = "#f87171"
            else:
                Change_Status(g, "Love", _amount, raw=True)
                Change_Status(g, "Obed", _amount, raw=True)
                Change_Status(g, "Inbt", _amount, raw=True)
                store._cheat_msg = _tl_fmt(_("Tenny %+d! Love=%d Obed=%d Inbt=%d"), _amount, g.Love, g.Obed, g.Inbt)
                store._cheat_msg_color = "#7ecb8f"

        elif code == "plumbers":
            g = GIRL_BY_ID.get("tenny")
            if g:
                Change_Status(g, "Lust", 80)
                store._cheat_msg = _tl_fmt(_("Tenny +80 Lust! Lust=%d"), g.Lust)
                store._cheat_msg_color = "#7ecb8f"
            else:
                store._cheat_msg = _("Tenny not found.")
                store._cheat_msg_color = "#f87171"

        elif code == "kevinhere":
            npc = NPC_PARTNERS.get("npc_bf_tenny") or NPC_PARTNERS.get("npc_gf_tenny")
            if npc:
                npc.friendship_with_player = 1000
                store._cheat_msg = _("Tenny's partner friendship maxed! (1000)")
                store._cheat_msg_color = "#7ecb8f"
            else:
                store._cheat_msg = _("Tenny has no partner.")
                store._cheat_msg_color = "#f87171"

        elif code == "thatsben":
            npc = NPC_PARTNERS.get("npc_bf_tenny") or NPC_PARTNERS.get("npc_gf_tenny")
            if npc:
                npc.suspicion = 0
                store._cheat_msg = _("Tenny's partner suspicion cleared! (0)")
                store._cheat_msg_color = "#7ecb8f"
            else:
                store._cheat_msg = _("Tenny has no partner.")
                store._cheat_msg_color = "#f87171"

        # ── Shion (the author, 2026-10-12) ──
        elif code == "evilstep":
            g = GIRL_BY_ID.get("shion")
            if not g:
                store._cheat_msg = _("Shion not found.")
                store._cheat_msg_color = "#f87171"
            elif _amount is None or _amount == 0:
                store._cheat_msg = _("Usage: evilstep [amount]")
                store._cheat_msg_color = "#f87171"
            else:
                Change_Status(g, "Love", _amount, raw=True)
                Change_Status(g, "Obed", _amount, raw=True)
                Change_Status(g, "Inbt", _amount, raw=True)
                store._cheat_msg = _tl_fmt(_("Shion %+d! Love=%d Obed=%d Inbt=%d"), _amount, g.Love, g.Obed, g.Inbt)
                store._cheat_msg_color = "#c084fc"

        elif code == "whatudoingstepson":
            g = GIRL_BY_ID.get("shion")
            if g:
                Change_Status(g, "Lust", 80)
                store._cheat_msg = _tl_fmt(_("Shion +80 Lust! Lust=%d"), g.Lust)
                store._cheat_msg_color = "#c084fc"
            else:
                store._cheat_msg = _("Shion not found.")
                store._cheat_msg_color = "#f87171"

        elif code == "whatafamily":
            _dad = getattr(store, "Dad", None)
            if _dad is not None and family_route_on():
                family_change(_dad, "suspicion", -family_stat(_dad, "suspicion"), "cheat", show_popup=False)
                store._cheat_msg = _("Your father's suspicion cleared! (0)")
                store._cheat_msg_color = "#c084fc"
            else:
                store._cheat_msg = _("Your father is not in this run.")
                store._cheat_msg_color = "#f87171"

        else:
            store._cheat_msg = _("Invalid cheat code.")
            store._cheat_msg_color = "#f87171"
            return

        if store._cheat_msg_color != "#f87171":
            _hist = getattr(store, "_cheat_history", [])
            if _raw in _hist:
                _hist.remove(_raw)
            _hist.insert(0, _raw)
            if len(_hist) > 10:
                _hist[:] = _hist[:10]
            store._cheat_history = _hist


# Helper screens for tutorial entries
screen _tut_section(title):
    frame:
        xsize _PK_CARD_W
        xalign 0.5
        background _pk_pill("#d4c87a", 0.16)
        padding (16, 9)
        hbox:
            spacing 8
            add _pk_icon("book", "#d4c87a") yalign 0.5
            text title:
                style "phone_text"
                size 17
                color "#d4c87a"
                bold True
                kerning 0.6
                yalign 0.5

screen _tut_entry(title, body):
    frame:
        xsize _PK_CARD_W
        xalign 0.5
        background _pk_card_bg()
        padding (16, 12, 16, 14)
        vbox:
            spacing 5
            xfill True
            text title:
                style "phone_text"
                size 16
                color "#e2e8f0"
                bold True
            text body:
                style "phone_text"
                font "fonts/WorkSans-Medium.ttf"
                size 14
                color "#9fb0c3"


# -----------------------------------------------------------
# Discovery banner — slides in from the right
# -----------------------------------------------------------
transform discovery_banner_slide:
    xoffset 500
    ease 0.4 xoffset 0
    pause 3.0
    ease 0.3 xoffset 500

screen discovery_banner(girl_name, info_text, name_color="#60a5fa"):
    zorder 300

    frame at discovery_banner_slide:
        xalign 1.0
        ypos 80
        background Frame("#1e293bdd", 4, 4, 4, 4)
        padding (20, 12)

        vbox:
            spacing 4
            text "[girl_name]":
                style "phone_text"
                size 22
                bold True
                color name_color
            text "[info_text]":
                style "phone_text"
                size 18
                color "#e2e8f0"

    timer 5.0 action Hide("discovery_banner")
