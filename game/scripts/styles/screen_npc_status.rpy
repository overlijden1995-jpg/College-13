# ============================================================
# Phone: NPC partner status. Hero header + cards (phone UI kit).
# ============================================================
# Same information the text screen had: whose partner he / she is, friendship with the player, love for the
# girl, and either the NTR boundary (only once the player learned about it) or the suspicion bar.
#
# screen phone_npc_status_screen(girl)     `girl` is the NPCPartner (the contact screens call everyone "girl")

init -3 python:

    _NPC_STATUS_ACCENT = "#7ecbff"

    def npc_status_view(npc):
        """Everything phone_npc_status_screen shows about an NPC partner, worked out once."""
        _girl = GIRL_BY_ID.get(getattr(npc, "girl_gid", None))
        v = {"accent": _NPC_STATUS_ACCENT,
             "girl_name": _girl.Name if _girl else str(getattr(npc, "girl_gid", "")).capitalize(),
             "girl_color": getattr(_girl, "color", None) or _PK_TEXT,
             "girl_avatar": _girl_avatar_by_gid(_girl.gid) if _girl else None,
             "partner_chip": (_girl.Name + _tl(_("'s Partner"))) if _girl else ""}
        _friend = getattr(npc, "friendship_with_player", 0)
        _love = getattr(npc, "love_for_girl", 0)
        _susp = getattr(npc, "suspicion", 0)
        # (word, value, max, bar color, tier label, tier color)
        v["friend"] = (_("Friend"), _friend, 1000, "#7ecbff") + _pk_tier("npc_bond", _friend)
        v["love"] = ("Love", _love, 1000, "#ff9e5e") + _pk_tier("npc_love", _love)
        _sl, _sc = _pk_tier("npc_susp", _susp)
        v["susp"] = ("Suspc", _susp, 100, _sc, _sl, _sc)

        # NTR boundary: only after the player learned about it; the trust bar only once he learned THAT too
        v["boundary"] = None
        if getattr(npc, "_ntr_active", False) and getattr(_girl, "_ntr_boundary_discovered", False):
            _level = getattr(npc, "_ntr_boundary_level", 1)
            _trust = None
            if _level < 4 and getattr(_girl, "_ntr_trust_discovered", False):
                _trust = int(getattr(npc, "_ntr_boundary_bar", 0))
            v["boundary"] = {
                "limit": _ntr_boundary_level_label(_level),
                "trust": _trust,
                "traits": [(_label, _color) for _tid, _label, _color in (("voyeur", _("Voyeur"), "#fbbf24"), ("camera_lover", _("Camera Lover"), "#fb923c"))
                           if hasattr(npc, "has_trait") and npc.has_trait(_tid)]}
        # Y.U.Z.U.: what the report said about this partner when it was bought (jurassic_dog_event.rpy). None = not
        # bought, or a partner met after the purchase: the report never updates (CJ)
        v["yuzu_traits"] = []
        _yz = yuzu_npc_report_traits(npc)
        if _yz is not None:
            if "ntr" in _yz:
                v["yuzu_traits"].append((_("NTR"), "#a78bfa"))
            elif "proud" in _yz:
                v["yuzu_traits"].append((_("Proud"), "#f87171"))
            else:
                v["yuzu_traits"].append((_("Neutral"), "#94a3b8"))
            # the BOUNDARY card above already shows these two chips once it is on screen
            if v["boundary"] is None:
                if "voyeur" in _yz:
                    v["yuzu_traits"].append((_("Voyeur"), "#fbbf24"))
                if "camera_lover" in _yz:
                    v["yuzu_traits"].append((_("Camera Lover"), "#fb923c"))
        return v


screen phone_npc_status_screen(girl):

    modal True
    zorder 200

    $ v = npc_status_view(girl)
    $ _ns_body_y = PH_CY_HEADER + _PK_HERO_H + 10
    $ _ns_body_h = _PH_SCREEN_BOTTOM - _ns_body_y - 6

    use pk_page():

        use pk_hero(girl.Name, v["accent"], avatar="images/menus/Char_Default.png"):
            if v["partner_chip"]:
                hbox:
                    use pk_chip(v["partner_chip"], v["girl_color"])

        viewport:
            id "npc_vp"
            xpos PH_CX
            ypos _ns_body_y
            xsize PH_CW
            ysize _ns_body_h
            mousewheel True
            draggable True
            scrollbars None

            vbox:
                spacing 10
                xsize PH_CW - 14

                use pk_card(_("PARTNER OF"), v["girl_color"], "couple"):
                    use pk_row(v["girl_name"], "", avatar=v["girl_avatar"], label_color=v["girl_color"])

                use pk_card(_("FRIENDSHIP"), "#7ecbff", "people"):
                    use pk_bar(_tl(v["friend"][0]), v["friend"][1], v["friend"][2], v["friend"][3], v["friend"][4], v["friend"][5], 132)

                use pk_card(_("LOVE FOR PARTNER"), "#ff9e5e", "heart"):
                    use pk_bar(v["love"][0], v["love"][1], v["love"][2], v["love"][3], v["love"][4], v["love"][5], 132)

                if v["boundary"]:
                    use pk_card(_("BOUNDARY"), "#a78bfa", "shield"):
                        use pk_row(_tl(_("Limit")), v["boundary"]["limit"], "#c4b5fd", chip=True)
                        if v["boundary"]["trust"] is not None:
                            use pk_bar(_tl(_("Trust")), v["boundary"]["trust"], 100, "#a78bfa", "%d/100" % v["boundary"]["trust"], "#c4b5fd", 70)
                        if v["boundary"]["traits"]:
                            hbox:
                                spacing 6
                                box_wrap True
                                box_wrap_spacing 6
                                for _t, _col in v["boundary"]["traits"]:
                                    use pk_chip(_tl(_t), _col)
                else:
                    use pk_card(_("SUSPICION"), v["susp"][3], "eye"):
                        use pk_bar(v["susp"][0], v["susp"][1], v["susp"][2], v["susp"][3], v["susp"][4], v["susp"][5], 132)

                if v["yuzu_traits"]:
                    use pk_card(_("YUZU REPORT"), "#00ff88", "sparkle"):
                        hbox:
                            spacing 6
                            box_wrap True
                            box_wrap_spacing 6
                            for _t, _col in v["yuzu_traits"]:
                                use pk_chip(_tl(_t), _col)

                null height 12

        use pk_scrollmark("npc_vp", v["accent"], _ns_body_y, _ns_body_h)

        use phone_chin_buttons(
            back_action=[Hide("phone_npc_status_screen"), Show("phone_contact_options_screen", girl=girl)])
