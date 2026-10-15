# ============================================================
# Phone: Contacts list + one contact's options (phone UI kit)
# ============================================================
# Same behavior the plain screens had: every girl and every active NPC partner is listed; a contact opens
# Status / Chat (/ Fertility for a girl while the pregnancy system is on); Chat needs the number first.
#
# screen phone_contacts_screen()
# screen phone_contact_options_screen(girl)      `girl` = a Girl or an NPCPartner

init -3 python:

    _CT_ACCENT = "#4da6ff"
    _CT_GROUPS_ACCENT = "#a78bfa"
    _CT_NPC_ACCENT = "#7ecbff"
    _CT_LOC_COLOR = "#94a3b8"

    # girls' rooms are not listed: _tracker_loc_label names them from GIRL_ROOMS with the girl's CURRENT name
    # ("Negasonic's Room" like the rest of the game, a renamed Tenny included)
    _TRACKER_LOC_NAMES = {
        "campus": _("Campus"), "pool": _("Pool"), "showers": _("Showers"),
        "apartment": _("Apartment"), "apartment_room": _("Apartment Bedroom"), "apartment_shower": _("Apartment Bathroom"),
        "room": _("Your Room"),
        "classroom": _("Classroom"), "gym": _("Gym"),
        "hall": _("Hall"), "street": _("Street"),
        "mall": _("Mall"), "party": _("Party"),
    }

    def _tracker_loc_label(who):
        if not Player.has_item("girls_tracker") or getattr(who, "is_family", False):
            return None
        _loc = getattr(who, "loc", None)
        _is_npc = getattr(who, "gid", "").startswith("npc_")
        if not _loc or _loc == GIRL_AWAY_LOC:
            return _tl(_("Away"))
        if not _is_npc and girl_is_away(who):
            return _tl(_("Away"))
        for _rg, _rl in GIRL_ROOMS.items():
            if _rl == _loc and _rg in GIRL_BY_ID:
                return _tl_fmt("%s's Room", GIRL_BY_ID[_rg].Name)
        return _tl(_TRACKER_LOC_NAMES.get(_loc, _loc.replace("_", " ").title()))

    # A family contact (shion_family.rpy: the father): where he is, under his name
    _CT_FAMILY_CHIPS = {
        "home": (_("Father"), "#94a3b8"),
        "work": (_("Father, at work"), "#94a3b8"),
        "trip": (_("Father, on a business trip"), "#fbbf24"),
    }

    def phone_contact_view(who):
        """What the contact screens show about a Girl, an NPCPartner or a family contact (the father): accent,
        avatar, the chip under the name."""
        if getattr(who, "is_family", False):
            _fc = _CT_FAMILY_CHIPS[dad_where()]
            return {"is_npc": False, "is_family": True, "accent": who.color, "avatar": "images/menus/Char_Default.png",
                    "chip": (_tl(_fc[0]), _fc[1]), "has_number": True, "no_number": "",
                    "status_screen": "phone_family_status_screen"}
        _is_npc = who.gid.startswith("npc_")
        if _is_npc:
            _girl = GIRL_BY_ID.get(getattr(who, "girl_gid", None))
            _male = getattr(who, "gender", "male") == "male"
            return {"is_npc": True, "accent": _CT_NPC_ACCENT, "avatar": "images/menus/Char_Default.png",
                    "chip": ((_girl.Name + _tl(_("'s Partner"))), getattr(_girl, "color", None) or _PK_TEXT) if _girl else None,
                    "has_number": who.partner_id in getattr(Player, "phone_npc_contacts", set()),
                    "no_number": _tl(_("Need his number first") if _male else _("Need her number first")),
                    "status_screen": "phone_npc_status_screen"}
        _chip = None
        if who.is_dating_player():
            _chip = (_tr("Your Girlfriend"), "#f472b6")
        elif getattr(who, "Player_status", "none") == "ex":
            _chip = (_tr("Ex"), "#f87171")
        return {"is_npc": False, "accent": getattr(who, "color", None) or _CT_ACCENT, "avatar": _girl_avatar_by_gid(who.gid),
                "chip": _chip, "has_number": who.gid in getattr(Player, "phone_contacts", set()),
                "no_number": _tl(_("Need her number first")), "status_screen": "phone_girl_status_screen"}


# one contact line: face in a ring of her color, name, the chip / caption under it, a chevron
screen ct_contact(who, action):
    $ _cv = phone_contact_view(who)
    button:
        xsize _PK_CARD_W
        xalign 0.5
        background Frame(_PK_CARD, 16, 16, 16, 16)
        hover_background Frame(Transform(_PK_CARD, matrixcolor=BrightnessMatrix(0.10)), 16, 16, 16, 16)
        padding (12, 10, 14, 10)
        action action
        hbox:
            xfill True
            hbox:
                spacing 14
                yalign 0.5
                fixed:
                    xsize 58
                    ysize 58
                    yalign 0.5
                    add Transform(_pk_tint(_PK_RING, _cv["accent"]), xysize=(58, 58))
                    add _pk_face(_cv["avatar"], 50) align (0.5, 0.5)
                vbox:
                    yalign 0.5
                    spacing 4
                    text who.Name:
                        style "phone_text"
                        size 20
                        bold True
                        color (_PK_TEXT if not _cv["is_npc"] else "#b0bec5")
                    if _cv["chip"]:
                        hbox:
                            use pk_chip(_cv["chip"][0], _cv["chip"][1])
                    $ _ct_loc = _tracker_loc_label(who)
                    if _ct_loc:
                        hbox:
                            use pk_chip(_ct_loc, _CT_LOC_COLOR)
            add _pk_icon("next", _PK_MUTED) xalign 1.0 yalign 0.5


# Players were missing the Groups tab (it looked like a disabled icon): until he opens it once, it breathes
# in its own color with a dot on it. Saved with the game, so it never nags again.
default _phone_groups_seen = False

screen phone_contacts_screen():

    modal True
    zorder 200

    default _contacts_tab = "contacts"

    $ _ct_nav_h = 62
    $ _ct_body_y = PH_CY_HEADER + _PK_HEADER_H + 8
    $ _ct_nav_y = _PH_SCREEN_BOTTOM - _ct_nav_h
    $ _ct_body_h = _ct_nav_y - _ct_body_y - 4
    $ _ct_tab_w = int(PH_CW / 2)

    use pk_page():

        use pk_header(_tl(_("Contacts")), _CT_ACCENT, "people")

        # --- bottom nav: Chat / Groups ---
        frame:
            xpos PH_CX
            ypos _ct_nav_y
            xsize PH_CW
            ysize _ct_nav_h
            background "#0b1220"
            padding (0, 0)

            hbox:
                # _() = the marker only (the caption was never extracted: Russian showed "Groups" in English)
                for _ct_id, _ct_cap, _ct_art in (("contacts", _("Chat"), "images/menus/Chat.png"), ("groups", _("Groups"), "images/menus/GroupChat.png")):
                    $ _ct_call = (_ct_id == "groups" and not _phone_groups_seen and _contacts_tab != "groups")
                    button:
                        xsize _ct_tab_w
                        ysize _ct_nav_h
                        padding (0, 0)
                        background (_pk_pill(_CT_GROUPS_ACCENT, 0.10) if _ct_call else None)
                        hover_background "#ffffff0a"
                        action ([SetScreenVariable("_contacts_tab", _ct_id), Function(_pk_scroll_top, "phone_contacts_screen", "ct_vp")]
                                + ([SetVariable("_phone_groups_seen", True)] if _ct_id == "groups" else []))
                        if _contacts_tab == _ct_id:
                            frame:
                                xsize 64
                                ysize 4
                                xalign 0.5
                                yalign 0.0
                                padding (0, 0)
                                background _pk_pill(_CT_ACCENT)
                        vbox:
                            xalign 0.5
                            yalign 0.55
                            spacing 2
                            at (pk_pulse if _ct_call else pk_still)
                            add _ct_art:
                                zoom 0.35
                                xalign 0.5
                                matrixcolor (TintMatrix(_CT_GROUPS_ACCENT) * BrightnessMatrix(0.25) if _ct_call else (BrightnessMatrix(0.0) if _contacts_tab == _ct_id else BrightnessMatrix(-0.30)))
                            text _ct_cap:
                                style "phone_text"
                                size 12
                                bold _ct_call
                                color (_CT_GROUPS_ACCENT if _ct_call else (_CT_ACCENT if _contacts_tab == _ct_id else _PK_MUTED))
                                xalign 0.5
                        if _ct_call:
                            # a dot on the tab: something here he has not looked at yet
                            frame at pk_pulse:
                                xsize 10
                                ysize 10
                                xalign 0.5
                                xoffset 22
                                yalign 0.16
                                padding (0, 0)
                                background _pk_pill("#f472b6")

        viewport:
            id "ct_vp"
            xpos PH_CX
            ypos _ct_body_y
            xsize PH_CW
            ysize _ct_body_h
            mousewheel True
            draggable True
            scrollbars None

            vbox:
                spacing 8
                xsize PH_CW - 14

                # ---- TAB: contacts (every girl, then every active NPC partner)
                if _contacts_tab == "contacts":
                    for _cg in ALL_GIRLS:
                        use ct_contact(_cg, [Hide("phone_contacts_screen"), Show("phone_contact_options_screen", girl=_cg)])
                    for _fam_c in family_contacts():
                        use ct_contact(_fam_c, [Hide("phone_contacts_screen"), Show("phone_contact_options_screen", girl=_fam_c)])
                    for _npc_c in sorted(NPC_PARTNERS.values(), key=lambda _n: _n.Name):
                        use ct_contact(_npc_c, [Hide("phone_contacts_screen"), Show("phone_contact_options_screen", girl=_npc_c)])

                # ---- TAB: groups
                else:
                    use pk_action("people", _tl(_("New Group")), None, "#a78bfa",
                                  [Hide("phone_contacts_screen"), Show("phone_create_group_screen")])

                    for _grp in phone_get_groups():
                        button:
                            xsize _PK_CARD_W
                            xalign 0.5
                            background Frame(_PK_CARD, 16, 16, 16, 16)
                            hover_background Frame(Transform(_PK_CARD, matrixcolor=BrightnessMatrix(0.10)), 16, 16, 16, 16)
                            padding (14, 12, 14, 12)
                            action [Hide("phone_contacts_screen"), Function(_phone_open_group_and_restore, _grp)]
                            hbox:
                                xfill True
                                hbox:
                                    spacing 12
                                    yalign 0.5
                                    hbox:
                                        spacing -10
                                        yalign 0.5
                                        for _mg in _grp["members"][:3]:
                                            add _pk_face(_girl_avatar_by_gid(_mg), 38) yalign 0.5
                                    vbox:
                                        yalign 0.5
                                        spacing 3
                                        text _grp["name"]:
                                            style "phone_text"
                                            size 19
                                            bold True
                                            color _PK_TEXT
                                        text format_name_list([_girl_name_by_gid(_m) for _m in _grp["members"]]):
                                            style "phone_text"
                                            font "fonts/WorkSans-Medium.ttf"
                                            size 14
                                            color _PK_MUTED
                                add _pk_icon("next", _PK_MUTED) xalign 1.0 yalign 0.5

                null height 8

        use pk_scrollmark("ct_vp", _CT_ACCENT, _ct_body_y, _ct_body_h)

        use phone_chin_buttons(
            back_action=[Hide("phone_contacts_screen"), Show("phone_screen")])


screen phone_contact_options_screen(girl):

    modal True
    zorder 200

    $ _cv = phone_contact_view(girl)

    use pk_page():

        use pk_hero(girl.Name, _cv["accent"], avatar=_cv["avatar"]):
            if _cv["chip"]:
                hbox:
                    use pk_chip(_cv["chip"][0], _cv["chip"][1])

        vbox:
            xpos PH_CX
            ypos PH_CY_HEADER + _PK_HERO_H + 12
            xsize PH_CW
            spacing 8

            use pk_action("stats", _tl(_("Status")), _tl(_("View detailed stats")), "#60a5fa",
                          [Hide("phone_contact_options_screen"), Show(_cv["status_screen"], girl=girl)])

            # Chat needs the number: the line stays and says so (a family contact: always his number)
            if _cv.get("is_family"):
                use pk_action("bubble", _tl(_("Chat")), _tl(_("Open conversation")), "#4ade80",
                              [Hide("phone_contact_options_screen"), Function(_phone_open_family_chat_and_restore, girl)])
            elif _cv["is_npc"]:
                use pk_action("bubble", _tl(_("Chat")), (_tl(_("Open conversation")) if _cv["has_number"] else _cv["no_number"]), "#4ade80",
                              [Hide("phone_contact_options_screen"), Function(_phone_open_npc_chat_and_restore, girl)], enabled=_cv["has_number"])
            else:
                use pk_action("bubble", _tl(_("Chat")), (_tl(_("Open conversation")) if _cv["has_number"] else _cv["no_number"]), "#4ade80",
                              [Hide("phone_contact_options_screen"), Function(_phone_open_chat_and_restore, "phone_open_chat", girl)], enabled=_cv["has_number"])

            # Fertility (girls only, while the pregnancy system is on) -> screen_fertility.rpy
            if not _cv["is_npc"] and not _cv.get("is_family") and store._pregnancy_mode != "off":
                use pk_action("flower", _tr("Fertility"), _tr("Cycle, birth control and risk"), "#f9a8d4",
                              [Hide("phone_contact_options_screen"), Show("phone_fertility_screen", girl=girl)])

        use phone_chin_buttons(
            back_action=[Hide("phone_contact_options_screen"), Show("phone_contacts_screen")])
