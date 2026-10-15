## screen_fertility.rpy — Phone "Fertility" page of a girl
## Opened from her contact: Contacts -> girl -> Status / Chat / Fertility.
## Pure presentation. All logic (what the player knows, cycle math, risk estimate)
## lives in game/scripts/Actions/pregnancy.rpy: fert_app_data() / fert_player_data().

init python:

    _FERT_ACCENT = "#f9a8d4"

    _FERT_PHASE_COLOR = {
        "safe":     "#4ade80",
        "low_risk": "#facc15",
        "fertile":  "#fb923c",
        "peak":     "#f43f5e",
    }
    _FERT_PHASE_LABEL = {
        "safe":     _("Safe"),
        "low_risk": _("Low risk"),
        "fertile":  _("Fertile"),
        "peak":     _("Peak"),
    }
    _FERT_PHASE_ORDER = ("safe", "low_risk", "fertile", "peak")

    # Non-cycle states: chip label + color + one-line explanation
    _FERT_STATE_CHIP = {
        "away":       (_("Away"),       "#94a3b8"),
        "pregnant":   (_("Pregnant"),   "#f472b6"),
        "postpartum": (_("Postpartum"), "#c4b5fd"),
        "infertile":  (_("Infertile"),  "#94a3b8"),
        "iud":        (_("IUD"),        "#a78bfa"),
    }
    _FERT_STATE_NOTE = {
        "postpartum": _("Recovering after birth. Not fertile right now."),
        "infertile":  _("She can't get pregnant."),
        "iud":        _("IUD active after delivery. Protected for now."),
    }
    _FERT_STAGE_LABEL = {
        0: _("Early"),
        1: _("Early"),
        2: _("Showing"),
        3: _("Full belly"),
    }

    def _fert_days(n):
        return (_tr("%d day") if n == 1 else _tr("%d days")) % n

    def _fert_chip(fd):
        """(label, color) of the state chip on a girl card."""
        _chip = _FERT_STATE_CHIP.get(fd["state"])
        if _chip:
            return (_tr(_chip[0]), _chip[1])
        if not fd["knows_cycle"]:
            return ("???", "#64748b")
        return (_tr(_FERT_PHASE_LABEL[fd["cycle_phase"]]), _FERT_PHASE_COLOR[fd["cycle_phase"]])

    def _fert_state_line(fd):
        """One-line summary under the chip for the non-cycle states."""
        _st = fd["state"]
        if _st == "away":
            return _tr("Away giving birth. Back in %s.") % _fert_days(fd["away_days"])
        if _st == "pregnant":
            return "%s  ·  %s  ·  %s" % (
                _tr("Day %d") % fd["preg_day"],
                _tr(_FERT_STAGE_LABEL.get(fd["preg_stage"], _FERT_STAGE_LABEL[0])),
                _tr("Due in %s") % _fert_days(fd["due_in"]))
        return _tr(_FERT_STATE_NOTE.get(_st, ""))

    def _fert_cycle_line(fd):
        _head = _tr("Day %d of 28") % fd["cycle_day"]
        if fd["fertile_now"]:
            _tail = _tr("Fertile window ends in %s") % _fert_days(fd["flip_days"])
        else:
            _tail = _tr("Fertile window in %s") % _fert_days(fd["flip_days"])
        return "%s  ·  %s" % (_head, _tail)

    def _fert_pill_line(fd):
        """(text, color) of the birth control row."""
        _p = fd["pill"]
        if _p == "unknown":
            return (_tr("Birth control: ???"), "#64748b")
        if _p == "off":
            return (_tr("Not on the pill"), "#f87171")
        if _p == "placebo":
            return (_tr("Placebo, 0% (she thinks it's real)"), "#fb923c")
        _txt = _tr("On the pill, %d%% effective") % fd["pill_eff"]
        if fd.get("pill_missed", 0) > 0:
            _txt += "  ·  " + _tr("missed: %s") % _fert_days(fd["pill_missed"])
            return (_txt, "#facc15")
        return (_txt, "#4ade80")

    def _fert_risk_color(pct):
        if pct < 5:
            return "#4ade80"
        if pct < 15:
            return "#facc15"
        if pct < 30:
            return "#fb923c"
        return "#f43f5e"


# Small rounded label used all over the app
screen _fert_pill_chip(chip_label, chip_color):
    frame:
        background _pk_pill(chip_color, 0.18)
        padding (12, 4)
        yalign 0.5
        text chip_label:
            style "phone_text"
            size PH_FONT_TINY
            color chip_color
            bold True


# Section card: accent title + content supplied by the caller through `transclude`
screen _fert_card(title):
    frame:
        xsize _PK_CARD_W
        xalign 0.5
        background _pk_card_bg()
        padding (16, 12, 16, 14)
        vbox:
            spacing 9
            xfill True
            hbox:
                spacing 8
                add _pk_icon("flower", _FERT_ACCENT) yalign 0.5
                text title:
                    style "phone_text"
                    size 15
                    bold True
                    kerning 1.2
                    color _FERT_ACCENT
                    yalign 0.5
            transclude


# -----------------------------------------------------------
# Phone Fertility page (per girl)
# -----------------------------------------------------------
screen phone_fertility_screen(girl):

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

            $ _fd = fert_app_data(girl)
            $ _fp = fert_player_data()
            $ _chip_label, _chip_color = _fert_chip(_fd)
            $ _pill_txt, _pill_col = _fert_pill_line(_fd)
            $ _fert_inner_w = _PK_INNER_W
            $ _fert_body_y = PH_CY_HEADER + _PK_HERO_H + 8

            # --- Hero (phone UI kit): her face, her name, the app name and the state chip ---
            use pk_hero(girl.Name, _FERT_ACCENT, avatar=_girl_avatar_by_gid(girl.gid)):
                hbox:
                    spacing 6
                    use pk_chip(_tr("Fertility"), "#f9a8d4")
                    use pk_chip(_chip_label, _chip_color)

            # --- Scrollable content ---
            viewport:
                xpos PH_CX
                ypos _fert_body_y
                xsize PH_CW
                ymaximum _PH_SCREEN_BOTTOM - _fert_body_y - 6
                mousewheel True
                draggable True
                scrollbars None

                vbox:
                    spacing 8
                    xsize PH_CW

                    null height 2

                    # ── Cycle / pregnancy state ──
                    use _fert_card(_tr("CYCLE") if _fd["state"] == "cycle" else _tr("STATUS")):
                        if _fd["state"] == "cycle":
                            hbox:
                                spacing 2
                                ysize 30
                                xalign 0.5
                                if _fd["knows_cycle"]:
                                    for _ci, _cph in enumerate(_fd["cycle_strip"]):
                                        $ _c_today = (_ci + 1 == _fd["cycle_day"])
                                        frame:
                                            xsize 15
                                            ysize (30 if _c_today else 14)
                                            yalign 1.0
                                            padding (0, 0)
                                            background (_FERT_PHASE_COLOR[_cph] if _c_today else _FERT_PHASE_COLOR[_cph] + "66")
                                else:
                                    for _ci in range(28):
                                        frame:
                                            xsize 15
                                            ysize 14
                                            yalign 1.0
                                            padding (0, 0)
                                            background "#334155"

                            if _fd["knows_cycle"]:
                                text _fert_cycle_line(_fd):
                                    style "phone_text"
                                    size PH_FONT_XS
                                    color "#e2e8f0"
                                    xalign 0.5
                                if _fd["breedable_known"]:
                                    text _tr("Extra breedable: wider fertile window"):
                                        style "phone_text"
                                        size PH_FONT_TINY
                                        color "#fb923c"
                                        xalign 0.5

                                # Legend
                                hbox:
                                    xalign 0.5
                                    spacing 14
                                    for _lph in _FERT_PHASE_ORDER:
                                        hbox:
                                            spacing 5
                                            frame:
                                                xsize 12
                                                ysize 12
                                                yalign 0.5
                                                padding (0, 0)
                                                background _FERT_PHASE_COLOR[_lph]
                                            text _tr(_FERT_PHASE_LABEL[_lph]):
                                                style "phone_text"
                                                size PH_FONT_TINY
                                                color "#8ca0b4"
                                                yalign 0.5
                            else:
                                text _tr("Cycle unknown. Pay attention to her moods when you chat."):
                                    style "phone_text"
                                    size PH_FONT_XS
                                    color "#64748b"
                                    xalign 0.5

                        else:
                            if _fd["state"] == "pregnant":
                                frame:
                                    xsize _fert_inner_w
                                    ysize 12
                                    padding (0, 0)
                                    background "#1e293b"
                                    frame:
                                        xsize int(_fert_inner_w * min(1.0, float(_fd["preg_day"]) / max(1, _fd["preg_total"])))
                                        ysize 12
                                        padding (0, 0)
                                        background "#f472b6"
                            text _fert_state_line(_fd):
                                style "phone_text"
                                size PH_FONT_XS
                                color "#e2e8f0"

                    # ── Birth control ──
                    use _fert_card(_tr("BIRTH CONTROL")):
                        hbox:
                            spacing 8
                            text "\U0001F48A":
                                size PH_FONT_SM
                                yalign 0.5
                            text _pill_txt:
                                style "phone_text"
                                size PH_FONT_SM
                                color _pill_col
                                yalign 0.5

                        if _fd["pill"] == "on":
                            hbox:
                                spacing 8
                                text _tr("Effectiveness"):
                                    style "phone_text"
                                    size PH_FONT_TINY
                                    color "#8ca0b4"
                                    yalign 0.5
                                frame:
                                    yalign 0.5
                                    xsize PH_BAR_W
                                    ysize 10
                                    padding (0, 0)
                                    background "#1e293b"
                                    frame:
                                        xsize int(PH_BAR_W * _fd["pill_eff"] / 100.0)
                                        ysize 10
                                        padding (0, 0)
                                        background _pill_col
                        elif _fd["pill"] == "unknown":
                            text _tr("Unknown. Listen for hints when you chat with her."):
                                style "phone_text"
                                size PH_FONT_TINY
                                color "#64748b"

                    # ── Plan B ──
                    use _fert_card(_tr("PLAN B")):
                        hbox:
                            spacing 6
                            for _pi in range(_fd["plan_b_limit"]):
                                frame:
                                    xsize 16
                                    ysize 16
                                    yalign 0.5
                                    padding (0, 0)
                                    background ("#c4b5fd" if _pi < _fd["plan_b_used"] else "#334155")
                            null width 6
                            text (_tr("Used %d of %d") % (_fd["plan_b_used"], _fd["plan_b_limit"])):
                                style "phone_text"
                                size PH_FONT_XS
                                color ("#f87171" if _fd["plan_b_used"] >= _fd["plan_b_limit"] else "#e2e8f0")
                                yalign 0.5
                        if _fd["plan_b_used"] >= _fd["plan_b_limit"]:
                            text _tr("She won't take any more for now."):
                                style "phone_text"
                                size PH_FONT_TINY
                                color "#64748b"
                        if _fd["plan_b_used"] > 0:
                            text (_tr("Next dose frees up in %s") % _fert_days(_fd["plan_b_next_in"])):
                                style "phone_text"
                                size PH_FONT_TINY
                                color "#8ca0b4"

                    # ── Risk today (only while she can actually conceive) ──
                    if _fd["state"] == "cycle":
                        use _fert_card(_tr("RISK TODAY")):
                            if "risk_inside" in _fd:
                                hbox:
                                    spacing 6
                                    box_wrap True
                                    box_wrap_spacing 4
                                    use _fert_pill_chip("%s %s" % (_tr("Inside"), fert_pct_text(_fd["risk_inside"])), _fert_risk_color(_fd["risk_inside"]))
                                    use _fert_pill_chip("%s %s" % (_tr("Pull out"), fert_pct_text(_fd["risk_pullout"])), _fert_risk_color(_fd["risk_pullout"]))
                                    use _fert_pill_chip("%s 0%%" % _tr("Condom"), "#4ade80")
                                if _fp["vitamin_active"]:
                                    text (_tr("Includes your fertility vitamins (x%s).") % _fp["vitamin_mult"]):
                                        style "phone_text"
                                        size PH_FONT_TINY
                                        color "#8ca0b4"
                            else:
                                text _tr("??? Needs her cycle and her birth control status."):
                                    style "phone_text"
                                    size PH_FONT_XS
                                    color "#64748b"

                    # ── Player supplies ──
                    use _fert_card(_tr("YOUR SUPPLIES")):
                        hbox:
                            spacing 6
                            box_wrap True
                            box_wrap_spacing 6
                            use _fert_pill_chip("%s x%d" % (_tr("Condoms"), _fp["condoms"]), "#60a5fa")
                            use _fert_pill_chip("%s x%d" % (_tr("Pills"), _fp["pills"]), "#4ade80")
                            use _fert_pill_chip("%s x%d" % (_tr("Placebo"), _fp["placebo"]), "#fb923c")
                            use _fert_pill_chip("%s x%d" % (_tr("Plan B"), _fp["plan_b"]), "#c4b5fd")
                        hbox:
                            spacing 8
                            text _tr("Fertility vitamins"):
                                style "phone_text"
                                size PH_FONT_XS
                                color "#8ca0b4"
                                yalign 0.5
                            if _fp["vitamin_active"]:
                                use _fert_pill_chip(_tr("Active x%s, %s left") % (_fp["vitamin_mult"], _fert_days(_fp["vitamin_days"])), "#4ade80")
                            else:
                                use _fert_pill_chip(_tr("Not active"), "#64748b")

                    # ── Children (this girl) ──
                    if _fd["children"] > 0:
                        use _fert_card(_tr("CHILDREN")):
                            text (_tr("Children: %d") % _fd["children"]):
                                style "phone_text"
                                size PH_FONT_XS
                                color "#c4b5fd"
                            if _fd["child_age"]:
                                text _fd["child_age"]:
                                    style "phone_text"
                                    size PH_FONT_XS
                                    color "#e2e8f0"
                            if _fd["raised_by"]:
                                # her NPC partner stands as the father: the player pays nothing (no "$0 per week")
                                text _fd["raised_by"]:
                                    style "phone_text"
                                    size PH_FONT_XS
                                    color "#8ca0b4"
                            elif _fd["support_share"] <= 0:
                                # rich: her family pays all of it (child_support_player_share), no "$0 per week" either
                                text _("Her family pays the child support."):
                                    style "phone_text"
                                    size PH_FONT_XS
                                    color "#8ca0b4"
                            else:
                                text (_tr("Child support: $%d per week") % _fd["support_weekly"]):
                                    style "phone_text"
                                    size PH_FONT_XS
                                    color "#f87171"
                                if _fd["support_share"] < 1:
                                    # middle class: her family pays the rest
                                    text _("Her family pays the rest."):
                                        style "phone_text"
                                        size PH_FONT_XS
                                        color "#8ca0b4"

                    if not (_fd["knows_pill"] and _fd["knows_cycle"]):
                        text _tr("Chit chat with her and listen to what she says after sex. Asking her directly is risky: she may refuse or take offense."):
                            style "phone_text"
                            size PH_FONT_TINY
                            color "#64748b"
                            xalign 0.5
                            text_align 0.5
                            xmaximum PH_CW - 32

                    null height 10

            use phone_chin_buttons(
                back_action=[Hide("phone_fertility_screen"), Show("phone_contact_options_screen", girl=girl)])


