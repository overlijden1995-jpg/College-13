# ============================================================
# Phone: the status of a family member (his father, family_father.rpy). Hero header + cards (phone UI kit).
# ============================================================
# His bond with the player, where he is now (and the drinks the player gave him today), and the love between him
# and his wife (his for her, hers for him: wife_love) with his suspicion. Her side only once the player has met
# her (girl_met_player): a padlock before.
#
# screen phone_family_status_screen(girl)     `girl` is the FamilyContact (the contact screens call everyone "girl")

init -3 python:

    # where he is (family_where_key) -> the words on the card
    _FAMILY_WHERE_LABELS = {
        "apartment": _("Living room"),
        "apartment_room": _("Bedroom"),
        "apartment_shower": _("Bathroom"),
        "out": _("Out"),
        "work": _("At work"),
        "trip": _("On a business trip"),
        "nap": _("Asleep on the couch"),
    }

    def family_where_key(member):
        """Where a family member is now: a room of the apartment, "out", "work", "trip" or "nap"."""
        _room = family_room(member)
        if _room:
            return _room
        _where = dad_where() if member is store.Dad else "out"
        if _where != "home":
            return _where
        return "nap" if getattr(member, "_nap", None) == (store.Day, store.TimeIndex) else "out"

    def family_status_view(member):
        """Everything phone_family_status_screen shows about a family member, worked out once."""
        _wife = family_wife(member)
        _bond = family_stat(member, "friendship")
        _drinks = getattr(member, "_drinks", None) or (-1, 0)
        v = {"accent": member.color,
             "chip": phone_contact_view(member)["chip"],
             # (word, value, max, bar color, tier label, tier color)
             "bond": (_("Friend"), _bond, 1000, "#7ecbff") + _pk_tier("npc_bond", _bond),
             "where": _tl(_FAMILY_WHERE_LABELS.get(family_where_key(member), _("Out"))),
             "drinks": "%d/%d" % ((_drinks[1] if _drinks[0] == store.Day else 0), DAD_DRINKS_NAP),
             "wife": None, "wife_known": _wife is not None and girl_met_player(_wife)}
        if v["wife_known"]:
            _his = family_stat(member, "love_for_wife")
            _hers = wife_love(_wife)
            _susp = family_stat(member, "suspicion")
            _sl, _sc = _pk_tier("npc_susp", _susp)
            v["wife"] = {"name": _wife.Name, "color": getattr(_wife, "color", None) or _PK_TEXT,
                         "avatar": _girl_avatar_by_gid(_wife.gid),
                         "his": (_GS_HUSBAND_BARS[0], _his, 1000, "#ff9e5e") + _pk_tier("npc_love", _his),
                         "hers": (_GS_HUSBAND_BARS[1], _hers, 1000, "#f472b6") + _pk_tier("npc_love", _hers),
                         "susp": ("Suspc", _susp, 100, _sc, _sl, _sc)}
        return v


screen phone_family_status_screen(girl):

    modal True
    zorder 200

    $ v = family_status_view(girl)
    $ _fs_body_y = PH_CY_HEADER + _PK_HERO_H + 10
    $ _fs_body_h = _PH_SCREEN_BOTTOM - _fs_body_y - 6

    use pk_page():

        use pk_hero(girl.Name, v["accent"], avatar="images/menus/Char_Default.png"):
            if v["chip"]:
                hbox:
                    use pk_chip(v["chip"][0], v["chip"][1])

        viewport:
            id "family_vp"
            xpos PH_CX
            ypos _fs_body_y
            xsize PH_CW
            ysize _fs_body_h
            mousewheel True
            draggable True
            scrollbars None

            vbox:
                spacing 10
                xsize PH_CW - 14

                use pk_card(_("FRIENDSHIP"), "#7ecbff", "people"):
                    use pk_bar(_tl(v["bond"][0]), v["bond"][1], v["bond"][2], v["bond"][3], v["bond"][4], v["bond"][5], 132)

                use pk_card(_("WHERE HE IS"), v["accent"], "home"):
                    use pk_row(_tl(_("Now")), v["where"], "#cbd5e1", chip=True)
                    use pk_row(_tl(_("Drinks today")), v["drinks"], "#fbbf24")

                if v["wife"]:
                    use pk_card(_("MARRIAGE"), v["wife"]["color"], "couple"):
                        use pk_row(v["wife"]["name"], "", avatar=v["wife"]["avatar"], label_color=v["wife"]["color"])
                        use pk_bar(_tl(v["wife"]["his"][0]), v["wife"]["his"][1], v["wife"]["his"][2], v["wife"]["his"][3], v["wife"]["his"][4], v["wife"]["his"][5], 132)
                        use pk_bar(_tl(v["wife"]["hers"][0]), v["wife"]["hers"][1], v["wife"]["hers"][2], v["wife"]["hers"][3], v["wife"]["hers"][4], v["wife"]["hers"][5], 132)
                    use pk_card(_("SUSPICION"), v["wife"]["susp"][3], "eye"):
                        use pk_bar(v["wife"]["susp"][0], v["wife"]["susp"][1], v["wife"]["susp"][2], v["wife"]["susp"][3], v["wife"]["susp"][4], v["wife"]["susp"][5], 132)
                else:
                    use pk_card(_("MARRIAGE"), _PK_MUTED, "couple"):
                        use pk_locked()

                null height 12

        use pk_scrollmark("family_vp", v["accent"], _fs_body_y, _fs_body_h)

        use phone_chin_buttons(
            back_action=[Hide("phone_family_status_screen"), Show("phone_contact_options_screen", girl=girl)])
