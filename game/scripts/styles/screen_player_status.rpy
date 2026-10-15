# ============================================================
# Phone: player status ("Status" app). Hero header + two tabs of cards (phone UI kit).
# ============================================================
# Same information the text screen had (PHYSICAL, SEXUAL HISTORY, FIRSTS, CHILDREN, RELATIONSHIPS, FINANCIALS,
# C. JOHNSON'S INTEL). player_status_view() works everything out, the screen only lays it out.
# Captions that used to be "Head: value" text lines are borrowed from their old tl pairs (_pk_borrow).
#
# screen phone_player_status_screen(tab="overview")     tab: "overview" / "intimacy"

init -3 python:

    _PS_ACCENT = "#38bdf8"
    _PS_TABS = [("overview", _("Overview"), "stats"), ("intimacy", _("Intimacy"), "flame")]
    # acts only. Positions (cowgirl, doggy, ...) are preference data: every vaginal scene already counts as
    # "sex", so adding them would count one scene twice.
    _PS_ACTS = [("kiss", "Kiss"), ("hj", "HJ"), ("tj", "TJ"), ("bj", "BJ"), ("sex", "Sex"), ("anal", "Anal")]
    _PS_FIRSTS = [("kiss", "Kiss"), ("hj", "Handjob"), ("tj", "Titjob"), ("bj", "Blowjob"), ("sex", "Sex"), ("anal", "Anal")]
    # old text lines whose words the cards borrow (pairs exist in tl/<lang>/scripts/styles/screen_status.rpy)
    _PS_BORROW = {
        "girlfriend": _("Girlfriend:"), "contacts": "Contacts: [_ps_contacts]",
        "cash": _("Cash: $[_ps_cash]"), "bf_earnings": _("BigFans earnings: $[_ps_bf_earnings]"),
        "bf_subs": _("BigFans subs: [_ps_bf_subs]"), "videos": _("Videos recorded: [_ps_vids]"),
    }
    _PS_WORKOUTS = _("[_ps_tw] total ([_ps_ww] this week)")

    def player_status_view():
        """Everything phone_player_status_screen shows, worked out once per render."""
        v = {"accent": _PS_ACCENT, "name": getattr(Player, "Name", "You")}
        v["cap"] = dict((_k, _pk_borrow(_t)) for _k, _t in _PS_BORROW.items())

        # ---- physical
        _emax = Player._get_energy_max()
        _ecur = getattr(Player, "energy", 0)
        v["energy"] = (_ecur, _emax)
        v["strength"] = _pk_tier("strength", _emax)
        v["study"] = _pk_tier("player_study", getattr(Player, "study_level", 0))
        v["workouts"] = (_tl(_PS_WORKOUTS).replace("[_ps_tw]", str(getattr(Player, "total_workouts", 0)))
                         .replace("[_ps_ww]", str(getattr(Player, "weekly_workouts", 0))))
        v["breath"] = "%d/%d" % (getattr(Player, "breath", 0), BREATH_MAX)   # trained by swimming (swimming.rpy)
        v["exam"] = exam_countdown_text()   # shared with the HUD's time card (exam.rpy)

        # ---- sexual history
        _totals = dict((_k, 0) for _k, _l in _PS_ACTS)
        _totals["masturbate"] = 0
        _cream = _raw = _virgins = _orgasms = 0
        for _g in ALL_GIRLS:
            _sa = getattr(_g, "Sex_acts", {})
            for _k in _totals:
                _totals[_k] += _sa.get(_k, 0)
            _cream += getattr(_g, "CreampieCounts", 0)
            _raw += getattr(_g, "raw_sex_count", 0)
            _virgins += 1 if getattr(_g, "virginity_taken_by_player", False) else 0
            _orgasms += sum(getattr(_g, "Orgasms", {}).values())
        v["acts_total"] = sum(_totals.values())
        v["acts"] = [(_label, _totals[_k]) for _k, _label in _PS_ACTS if _totals[_k] > 0]
        v["boxes"] = [(str(v["acts_total"]), _tl(_("Total acts")), "#f472b6", "flame"),
                      (str(_orgasms), _tl(_("Her orgasms")), "#c084fc", "sparkle"),
                      (str(_cream), _tl(_("Creampies")), "#fb923c", "drop")]
        v["extras"] = [(_tl(_cap), _val, _col) for _cap, _val, _col, _n in (
            (_("Raw sex"), str(_raw), "#fbbf24", _raw),
            (_("Virginities"), _tl(_("[_ps_virgins_taken] taken")).replace("[_ps_virgins_taken]", str(_virgins)), "#c084fc", _virgins)) if _n > 0]

        # ---- firsts: the girl of the EARLIEST logged day of each act (acts only: a position entry is also
        #      logged for anal scenes, so it never proves a first "sex")
        v["firsts"] = []
        for _k, _label in _PS_FIRSTS:
            _best, _best_day = None, 999999
            for _g in ALL_GIRLS:
                for _entry in getattr(_g, "Sex_act_locations", []):
                    if _entry.get("act", "") != _k:
                        continue
                    if _entry.get("day", 999999) < _best_day:
                        _best, _best_day = _g, _entry.get("day", 999999)
                    break
            v["firsts"].append((_tr(_label), _best))
        # first girl he got pregnant, dated from the day she TOLD him: a pregnancy he does not know about never shows
        v["kids"] = None
        if store._pregnancy_mode != "off":
            _preg = sorted([_g for _g in ALL_GIRLS if getattr(_g, "player_firsts", {}).get("first_pregnancy")],
                           key=lambda _g: getattr(_g, "_pregnancy_told_day", 0))
            v["firsts"].append((_tr("Pregnancy"), _preg[0] if _preg else None))
            v["kids"] = fert_player_data()

        # ---- relationships
        v["gfs"] = [_g for _g in ALL_GIRLS if _g.is_dating_player()]
        v["exes"] = [_g for _g in ALL_GIRLS if getattr(_g, "Player_status", "none") == "ex"]
        v["contacts"] = len(getattr(Player, "phone_contacts", set()))

        # ---- financials
        _cash = getattr(Player, "cash", 0)
        v["cash"] = _cash
        v["money"] = [("$%d" % _cash, v["cap"]["cash"], "#4ade80", "coin")]
        if getattr(Player, "bigfans_total_earnings", 0) > 0:
            v["money"].append(("$%d" % Player.bigfans_total_earnings, v["cap"]["bf_earnings"], "#ff5c93", "coin"))
        if getattr(Player, "bigfans_subscribers", 0) > 0:
            v["money"].append((str(Player.bigfans_subscribers), v["cap"]["bf_subs"], "#ff5c93", "people"))
        v["videos"] = len(getattr(Player, "recorded_videos", []))
        _kids = v["kids"] or fert_player_data()
        v["support"] = None
        if _kids["support_weekly"] > 0:
            v["support"] = (_tr("Child support: $%d per week") % _kids["support_weekly"],
                            _tr("Next payment in %s") % _fert_days(_kids["support_next_in"]))

        # ---- C. Johnson's intel
        _disc = getattr(Player, "discoveries", {})
        v["intel"] = [_l for _l in (_johnson_intel_label(_dk) for _dk in sorted(_disc) if _disc[_dk] and _dk.startswith("johnson_")) if _l]
        return v


screen phone_player_status_screen(tab="overview"):

    modal True
    zorder 200

    default _ps_tab = tab

    $ v = player_status_view()
    $ _ps_body_y = PH_CY_HEADER + _PK_HERO_H + _PK_TABS_H + 8
    $ _ps_body_h = _PH_SCREEN_BOTTOM - _ps_body_y - 6

    use pk_page():

        use pk_hero(v["name"], v["accent"], initial=v["name"][:1].upper()):
            hbox:
                spacing 6
                use pk_chip("$%d" % v["cash"], "#4ade80")
                use pk_chip(v["strength"][0], v["strength"][1])

        use pk_tabs([(_id, _tl(_cap).upper(), _ic) for _id, _cap, _ic in _PS_TABS], _ps_tab, v["accent"], "_ps_tab",
                    PH_CY_HEADER + _PK_HERO_H, "phone_player_status_screen", "ps_vp")

        viewport:
            id "ps_vp"
            xpos PH_CX
            ypos _ps_body_y
            xsize PH_CW
            ysize _ps_body_h
            mousewheel True
            draggable True
            scrollbars None

            vbox:
                spacing 10
                xsize PH_CW - 14

                # ==================================================== OVERVIEW
                if _ps_tab == "overview":

                    use pk_card(_("PHYSICAL"), "#4ade80", "bolt"):
                        use pk_bar(_tl(_("Energy")), v["energy"][0], v["energy"][1], "#4ade80", "%d/%d" % v["energy"], right_w=46, label_w=72)
                        use pk_row(_tl(_("Strength")), v["strength"][0], v["strength"][1], chip=True)
                        use pk_row(_tl(_("Study Level")), v["study"][0], v["study"][1], chip=True)
                        if v["exam"][1]:
                            use pk_row(v["exam"][0], "", v["exam"][1], label_color=v["exam"][1])
                        else:
                            use pk_row(v["exam"][0], "")
                        use pk_row(_tl(_("Workouts")), v["workouts"])
                        use pk_row(_tl(_("Breath")), v["breath"])

                    use pk_card(_("RELATIONSHIPS"), "#f472b6", "heart"):
                        if v["gfs"]:
                            for _g in v["gfs"]:
                                use pk_row(_g.Name, v["cap"]["girlfriend"], "#f472b6", chip=True, avatar=_girl_avatar_by_gid(_g.gid), label_color=_g.color)
                        else:
                            hbox:
                                use pk_chip(_tl(_("Not dating anyone")), "#fbbf24")
                        for _g in v["exes"]:
                            use pk_row(_g.Name, _tr("Ex"), "#f87171", chip=True, avatar=_girl_avatar_by_gid(_g.gid), label_color=_g.color)
                        use pk_row(v["cap"]["contacts"], str(v["contacts"]))

                    use pk_card(_("FINANCIALS"), "#4ade80", "coin"):
                        hbox:
                            xalign 0.5
                            spacing 6
                            for _n, _cap, _col, _ic in v["money"]:
                                use pk_box(_n, _cap, _col, int((_PK_INNER_W - 12) / 3), _ic)
                        if v["videos"] > 0:
                            use pk_row(v["cap"]["videos"], str(v["videos"]))
                        if v["support"]:
                            use pk_row(v["support"][0], "", "#f87171", label_color="#f87171")
                            use pk_row(v["support"][1], "")

                    use pk_card(_tr("C. JOHNSON'S INTEL"), "#ff8c00", "eye"):
                        if v["intel"]:
                            hbox:
                                spacing 6
                                box_wrap True
                                box_wrap_spacing 6
                                for _t in v["intel"]:
                                    use pk_chip(_t, "#ff8c00")
                        else:
                            text _tr("No intel yet"):
                                style "phone_text"
                                size 16
                                color _PK_DIM

                # ==================================================== INTIMACY
                else:

                    hbox:
                        xalign 0.5
                        spacing 6
                        for _n, _cap, _col, _ic in v["boxes"]:
                            use pk_box(_n, _cap, _col, int((_PK_CARD_W - 12) / 3), _ic)

                    use pk_card(_("SEXUAL HISTORY"), "#f472b6", "flame"):
                        if v["acts"]:
                            hbox:
                                spacing 6
                                box_wrap True
                                box_wrap_spacing 6
                                for _l, _n in v["acts"]:
                                    use pk_chip(_l, "#f472b6", count=_n)
                        else:
                            text _("None yet"):
                                style "phone_text"
                                size 16
                                color _PK_DIM
                        for _cap, _val, _col in v["extras"]:
                            use pk_row(_cap, _val, _col, chip=True)

                    use pk_card(_("FIRSTS"), "#fbbf24", "star"):
                        for _l, _g in v["firsts"]:
                            if _g is not None:
                                use pk_row(_l, _g.Name, _g.color, chip=True)
                            else:
                                use pk_row(_l, None)

                    if v["kids"] is not None:
                        use pk_card(_tr("CHILDREN"), "#f9a8d4", "person"):
                            if not v["kids"]["mothers"]:
                                text _("None yet"):
                                    style "phone_text"
                                    size 16
                                    color _PK_DIM
                            for _km in v["kids"]["mothers"]:
                                vbox:
                                    spacing 2
                                    use pk_row(_km["name"], _km["age"], label_color=_km["color"])
                                    if _km["raised_by"]:
                                        text _km["raised_by"]:
                                            style "phone_text"
                                            font "fonts/WorkSans-Medium.ttf"
                                            size 14
                                            color _PK_MUTED

                null height 12

        use pk_scrollmark("ps_vp", v["accent"], _ps_body_y, _ps_body_h)

        use phone_chin_buttons(
            back_action=[Hide("phone_player_status_screen"), Show("phone_screen")])
