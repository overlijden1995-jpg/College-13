# ============================================================
# Phone: Inventory (phone UI kit). One card per kind of item.
# ============================================================
# Same items the flat list had (SHOP_CATALOG + geek store + pharmacy + utility gear), grouped.
#
# screen phone_inventory_screen()

init -3 python:

    _INV_ACCENT = "#b388ff"

    def phone_inventory_view():
        """[(card title, accent, icon, [(emoji, name, quantity)])], empty cards left out."""
        def _rows(pairs):
            return [(_ITEM_ICONS.get(_id, u"\U0001F4E6"), _name, Player.get_item_count(_id)) for _id, _name in pairs if Player.get_item_count(_id) > 0]
        _drinks = [(_d, _tr(DRINKS[_d]["label"])) for _d in DRINK_IDS] + [("drinks", _tr("Vodka"))]       # "drinks" = pre-0.9 vodka bottles of old saves
        _gifts = [(_g["id"], _g["label"]) for _g in SHOP_CATALOG["gifts"]["items"]]
        for _cat, _cat_gid, _cat_col in PHONE_SHOP_GIRL_SECTIONS:
            _gifts += [(_g["id"], GIFT_DISPLAY.get(_g["id"], _g["label"])) for _g in SHOP_CATALOG[_cat]["items"]]
        _gifts += [(_n, GIFT_DISPLAY.get(_n, _n)) for _n in sorted(NERD_GIFT_IDS)]
        _rx = [(_r, _tr(GIFT_DISPLAY.get(_r, _r))) for _r in ("birth_control", "placebo_pills", "morning_after", "fertility_vitamin")]
        _gear = [(_u, _tr(_l)) for _u, _l in (("tripod", "Tripod"), ("tekmix_camera", "Tekmix Camera"),
                                                ("girls_tracker", "Girls Tracker"), ("instant_preg_test", "Instant Pregnancy Test")) if Player.has_item(_u)]
        _cards = [(_pk_t("Condoms"), "#60a5fa", "shield", _rows([("condom", _tr("Condoms")), ("japanese_condom", _tr("Japanese Condoms"))])),
                  (_pk_t("Drinks"), "#a78bfa", "glass", _rows(_drinks)),
                  (_pk_t("Gifts"), "#f472b6", "heart", _rows(_gifts)),
                  (_pk_t("Pharmacy"), "#f9a8d4", "pill", _rows(_rx)),
                  (_tl(_("Equipment")), "#fbbf24", "camera", [(_ITEM_ICONS.get(_u, u"\U0001F4E6"), _l, 1) for _u, _l in _gear])]
        return [_c for _c in _cards if _c[3]]


screen phone_inventory_screen():

    modal True
    zorder 200

    $ _inv_cards = phone_inventory_view()
    $ _inv_body_y = PH_CY_HEADER + _PK_HEADER_H + 8
    $ _inv_body_h = _PH_SCREEN_BOTTOM - _inv_body_y - 6

    use pk_page():

        use pk_header(_tl(_("Inventory")), _INV_ACCENT, "bag"):
            use pk_chip("$%d" % getattr(Player, "cash", 0), "#4ade80")

        viewport:
            id "inv_vp"
            xpos PH_CX
            ypos _inv_body_y
            xsize PH_CW
            ysize _inv_body_h
            mousewheel True
            draggable True
            scrollbars None

            vbox:
                spacing 10
                xsize PH_CW - 14

                if not _inv_cards:
                    null height 40
                    text _("Your inventory is empty."):
                        style "phone_text"
                        size 18
                        color _PK_DIM
                        xalign 0.5

                for _title, _accent, _icon, _rows in _inv_cards:
                    use pk_card(_title.upper(), _accent, _icon):
                        for _emoji, _name, _qty in _rows:
                            hbox:
                                xfill True
                                hbox:
                                    spacing 10
                                    yalign 0.5
                                    text _emoji:
                                        size 20
                                        min_width 28
                                        yalign 0.5
                                    text _name:
                                        style "phone_text"
                                        size 17
                                        color _PK_TEXT
                                        yalign 0.5
                                hbox:
                                    xalign 1.0
                                    yalign 0.5
                                    use pk_chip("x%d" % _qty, _accent)

                null height 12

        use pk_scrollmark("inv_vp", _INV_ACCENT, _inv_body_y, _inv_body_h)

        use phone_chin_buttons(
            back_action=[Hide("phone_inventory_screen"), Show("phone_screen")])
