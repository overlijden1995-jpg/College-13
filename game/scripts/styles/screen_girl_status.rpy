# ============================================================
# Phone: girl status. Hero header + three tabs of cards.
# ============================================================
# Same information (and the same discovery gates) the screen always had: it used to be ONE scroll of
# about 22 text sections. girl_status_view() works everything out, the screen only lays it out with the
# phone UI kit (screen_phone_kit.rpy: pk_page, pk_hero, pk_tabs, pk_card, pk_bar, pk_chip, pk_row, pk_box).
# The girl's own color is the accent; a padlock = the player has not discovered it yet.
#
# screen phone_girl_status_screen(girl, tab="overview")     tab: "overview" / "intimacy" / "life"

init -3 python:

    # tab id -> (caption, shown upper case; icon)
    _GS_TABS = [("overview", _("Overview"), "stats"), ("intimacy", _("Intimacy"), "flame"), ("life", _("Life"), "people")]

    # Captions borrowed from the "Head: value" lines this screen used to print: those pairs exist in PT / ES
    # (tl/<lang>/scripts/styles/screen_status.rpy), so the word comes out translated without a new pair.
    # key -> (the old line, which side of its colon). _() keeps the old lines alive for the translation tools.
    _GS_BORROW = {
        "kisses": (_("Kisses: [_kiss_count]"), 0), "showers": (_("Showered together: [_showered]x"), 0),
        "caught_you": (_("Caught you: [_caught_count]x"), 0), "caught_together": (_("Caught together: [_pub_caught]x"), 0),
        "blackmailed": (_("Blackmailed: [_st_bm_times]x"), 0), "paid": (_("Paid for acts: $[_st_fin_paid]"), 0),
        "gifts": (_("Gifts given: $[_st_gifts]"), 0), "spent": (_("Total spent: $[_st_spent]"), 0),
        "call_her": (_("You call her: [_pn_from]"), 0), "calls_you": (_("She calls you: [_pn_for]"), 0),
        "bf_uncertain": (_("- [_bf_display]: {color=#fbbf24}Never (?){/color}"), 1),
        "bf_done": (_("- [_bf_display]: {color=#f87171}Done{/color}"), 1),
        "bf_never": (_("- [_bf_display]: {color=#4ade80}Never{/color}"), 1),
    }
    # old lines a NAME goes into: translate the template, then put the name in
    _GS_PARTNER_TITLE = _("PARTNER: [_npc_p_name]")
    _GS_HUSBAND_TITLE = _("HUSBAND: [_npc_p_name]")
    _GS_HUSBAND_BARS = (_("His love"), _("Her love"))
    _GS_THINKS_VIRGIN = _("Thinks [_vk_n] is a virgin")

    def _gs_borrow(key):
        """The word of _GS_BORROW[key] in the current language (see _pk_borrow)."""
        return _pk_borrow(*_GS_BORROW[key])

    _GS_ACT_LABELS = [
        ("kiss", "Kiss"), ("hj", "Handjob"), ("bj", "Blowjob"), ("tj", "Titjob"), ("fj", "Footjob"), ("rj", "Rimjob"),
        ("masturbate", "Masturbation"),
        ("reverse_cowgirl", "Reverse Cowgirl"), ("cowgirl", "Cowgirl"), ("doggy", "Doggy"),
        ("full_nelson", "Full Nelson"), ("laying_down", "Laying Down"), ("sex", "Sex (total)"), ("anal", "Anal"),
    ]
    _GS_FAV_NAMES = {
        "kiss": "Kissing", "massage": "Massage", "hj": "Handjob", "bj": "Blowjob", "tj": "Titjob", "fj": "Footjob", "rj": "Rimjob",
        "reverse_cowgirl": "Reverse Cowgirl", "cowgirl": "Cowgirl", "doggy": "Doggy Style", "full_nelson": "Full Nelson",
        "laying_down": "Laying Down", "anal": "Anal", "masturbate": "Masturbation",
    }
    _GS_BF_ACTS = [("hj", "Handjob"), ("tj", "Titjob"), ("bj", "Blowjob"), ("masturbate", "Masturbation"),
                   ("sex", "Sex"), ("sex_raw", "Raw sex"), ("creampie", "Creampie")]
    # what he learned about her and her partner -> (chip text, color)
    _GS_BF_STATE = {"uncertain": ("bf_uncertain", "#fbbf24"), True: ("bf_done", "#f87171"), False: ("bf_never", "#4ade80")}
    _GS_TRAIT_NAMES = {
        "hate_cum": "Hates Cum", "cum_slut": "Cum Lover", "camera_hater": "Camera Hater", "camera_lover": "Camera Lover",
        "public_shy": "Public Shy", "public_fetish": "Public Fetish", "cute_sex": "Gentle", "hardcore_sex": "Hardcore", "loyal": "Loyal",
        "anal_hater": "Anal Hater", "anal_lover": "Anal Lover", "cheater": "Cheater", "monogamous": "Monogamous",
        # the control pair shows on the EVOLVED card once a femdom breaks (CANON_BREAK_RULES)
        "femdom": "Femdom", "submissive": "Submissive",
    }

    # The LANES of a story's routes on the card (story_route_lock): label, icon, color. Before the first
    # unlock the hint shows one block per lane (the first advanced locks the others out); after it, only hers.
    _GS_LANES = {
        "stats":     (_("Earn her"), "heart", "#f472b6"),
        "blackmail": (_("Own her secret"), "eye", "#a78bfa"),
    }
    _GS_LANE_ORDER = ("stats", "blackmail")

    def girl_status_view(girl):
        """Everything phone_girl_status_screen shows about `girl`, worked out once: plain values, (text, color)
        pairs and lists. None = the player has not discovered it yet (padlock)."""
        v = {"accent": getattr(girl, "color", None) or "#60a5fa"}
        _has_partner = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        _partner_known = _has_partner and _partner_discovered(girl)

        # ---- what she is to him (hero)
        _ps = getattr(girl, "Player_status", "none")
        _is_gf = _ps in ("dating", "exclusive")
        v["is_gf"] = _is_gf
        if _is_gf:
            v["relationship"] = (_tr("Your Girlfriend"), "#f472b6")
        elif girl.get_flag("discovered_relationship"):
            if _ps == "none":
                _love = getattr(girl, "Love", 0)
                if _love >= 700:
                    _rel_label = _tr("Intimate")
                elif _love >= 500:
                    _rel_label = _tr("Close Friend")
                elif _love >= 300:
                    _rel_label = _tr("Friend")
                elif _love >= 100:
                    _rel_label = _tr("Acquaintance")
                else:
                    _rel_label = _tr("Stranger")
            elif _ps == "ex":
                _rel_label = _tr("Ex")
            else:
                _rel_label = _ps.capitalize()
            v["relationship"] = (_rel_label, "#cbd5e1")
        else:
            v["relationship"] = None
        v["partner_chip"] = None
        if v["relationship"] and not _is_gf:
            if _partner_known:
                v["partner_chip"] = (_("Is dating someone"), "#f87171")
            elif girl.get_flag("discovered_single"):
                v["partner_chip"] = ("Single", "#4ade80")

        # ---- stat bars: (label, value, max, color)
        v["stats"] = [("Love", getattr(girl, "Love", 0), 1000, STAT_COLOR_LOVE),
                      ("Obed", getattr(girl, "Obed", 0), 1000, STAT_COLOR_OBED),
                      ("Inbt", getattr(girl, "Inbt", 0), 1000, STAT_COLOR_INBT)]
        if getattr(girl, "_cheat_escalation_path", 0) in (1, 2, 3):
            v["stats"].append(("Heat", int(getattr(girl, "_cheat_heat", 0)), 100, STAT_COLOR_HEAT))
        if _is_gf:
            v["stats"].append(("Jeal", int(getattr(girl, "Jealousy", 0)), 1000, STAT_COLOR_JEALOUSY))
        # her story step (story_steps.rpy): its name, and the ceiling of each stat at it (shown as value/ceiling)
        _st_name = story_step_name(girl)
        v["stat_caps"] = {}
        if _st_name:
            for _st in STORY_CAPPED_STATS:
                _cap = story_stat_cap(girl, _st)
                if _cap is not None:
                    v["stat_caps"][_st] = _cap

        # ---- story card (only for girls with a story ladder)
        v["story_card"] = None
        if _st_name:
            _sc_step = story_step(girl)
            _sc_taken = story_step_route(girl)
            _sc_top = len(STORY_LADDERS[story_key(girl)]) - 1
            _sc_route_labels = {"love": "Love", "obed": "Obed", "inbt": "Inbt",
                                "blackmail": "Blackmail", "evidence": "Evidence"}
            _sc_hint = None
            _sc_hint_routes = None
            if _sc_step < _sc_top:
                # a dict hint is one line per LANE (story_route_lock): locked = only her lane's line; before
                # the lock, one block per lane ("hint_routes": the first unlock locks the others out). A plain
                # string serves every lane. "ready" beats them all: a route of her unlock ALREADY passes, only
                # the MOMENT is missing, and the card says where it is (the narration hints are silent then).
                _sc_hint = (story_data(STORY_STATUS_HINTS, girl, {}) or {}).get(story_step_id(girl), "")
                if isinstance(_sc_hint, dict):
                    _sc_lock = story_route_lock(girl)
                    if _sc_hint.get("ready") and story_unlock_route(girl) is not None:
                        _sc_hint = _tl(_sc_hint["ready"])
                    elif _sc_lock and _sc_hint.get(_sc_lock):
                        _sc_hint = _tl(_sc_hint[_sc_lock])
                    else:
                        _sc_order = [_l for _l in _GS_LANE_ORDER if _l in _sc_hint] + sorted(
                            [_l for _l in _sc_hint if _l not in _GS_LANE_ORDER and _l != "ready"])
                        _sc_hint_routes = [(_l, _tl(_sc_hint[_l])) for _l in _sc_order]
                        _sc_hint = None
                else:
                    _sc_hint = _tl(_sc_hint) if _sc_hint else None
            # what THIS step opened (plan_shion_agency F4): the acts of her current rung, in card words
            _sc_key = story_key(girl)
            _sc_acts = (STORY_LADDERS[_sc_key][min(_sc_step, len(STORY_LADDERS[_sc_key]) - 1)].get("acts") or ()) if _sc_key else ()
            _sc_opened = ", ".join(_tl(STORY_ACT_NAMES[_a]) for _a in _sc_acts if _a in STORY_ACT_NAMES)
            v["story_card"] = {
                "step_name": _st_name,
                "step": _sc_step,
                "top": _sc_top,
                "route_taken": _sc_route_labels.get(_sc_taken, _sc_taken) if _sc_taken else None,
                "opened": _sc_opened or None,
                "hint": _sc_hint or None,
                "hint_routes": _sc_hint_routes,
            }
        _spec = spectrum_label(girl) if callable(globals().get("spectrum_label")) else ""
        v["sexuality"] = (_spec, _pk_tier("spectrum", getattr(girl, "sexuality_spectrum", 0))[1]) if _spec else None

        # ---- her partner: how loyal she is to him + his bars (word, value, max, bar color, tier label, tier color)
        v["partner"] = None
        if _partner_known and not _is_gf:
            _npc = get_npc_partner_for(girl)
            _loyalty = None
            if v["relationship"]:          # her loyalty is part of what he learned about her relationship
                _loyalty = ((girl.partner_label().upper() if hasattr(girl, "partner_label") else "BF"),
                            (girl.bf_loyalty_label() if hasattr(girl, "bf_loyalty_label") else "???"),
                            (girl.bf_loyalty_color() if hasattr(girl, "bf_loyalty_color") else _PK_MUTED))
            _bars = []
            if _npc is not None:
                _bond = getattr(_npc, "friendship_with_player", 0)
                _love = getattr(_npc, "love_for_girl", 0)
                _susp = getattr(_npc, "suspicion", 0)
                _sl, _sc = _pk_tier("npc_susp", _susp)
                _bars = [("Bond", _bond, 1000, "#7ecbff") + _pk_tier("npc_bond", _bond),
                         ("Love", _love, 1000, "#ff9e5e") + _pk_tier("npc_love", _love),
                         ("Suspc", _susp, 100, _sc, _sl, _sc)]
            if _loyalty or _bars:
                v["partner"] = {"title": _tl(_GS_PARTNER_TITLE).replace("[_npc_p_name]", (_npc.Name if _npc is not None else "???")),
                                "loyalty": _loyalty, "bars": _bars}
        # ---- her husband (a family member: family_father.rpy): his bond with the player, the love between them
        _hb = girl_husband(girl)
        if v["partner"] is None and _hb is not None and girl_met_player(girl):
            _hb_bond = family_stat(_hb, "friendship")
            _hb_his = family_stat(_hb, "love_for_wife")
            _hb_hers = wife_love(girl)
            _hb_susp = family_stat(_hb, "suspicion")
            _hsl, _hsc = _pk_tier("npc_susp", _hb_susp)
            v["partner"] = {"title": _tl(_GS_HUSBAND_TITLE).replace("[_npc_p_name]", _hb.Name), "loyalty": None,
                            "bars": [("Bond", _hb_bond, 1000, "#7ecbff") + _pk_tier("npc_bond", _hb_bond),
                                     (_GS_HUSBAND_BARS[0], _hb_his, 1000, "#ff9e5e") + _pk_tier("npc_love", _hb_his),
                                     (_GS_HUSBAND_BARS[1], _hb_hers, 1000, "#f472b6") + _pk_tier("npc_love", _hb_hers),
                                     ("Suspc", _hb_susp, 100, _hsc, _hsl, _hsc)]}

        # ---- personality
        v["traits"] = [(_pk_t(_desc), (girl.has_trait(_tid) if hasattr(girl, "has_trait") else True))
                       for _tid, _desc in TRAIT_HINT_DISPLAY.items() if girl.get_flag("discovered_trait_" + _tid)]
        # (what she was, what she became): None = she just lost it
        v["evolved"] = [(_pk_t(_GS_TRAIT_NAMES.get(_old, _old)), (_pk_t(_GS_TRAIT_NAMES.get(_new, _new)) if _new else None))
                        for _old, _new in getattr(girl, "evolved_traits", {}).items()]

        # ---- intimacy
        _al = getattr(girl, "ActionLog", {})
        _sa = getattr(girl, "Sex_acts", {})
        v["counters"] = [(_al.get("kiss", 0), _gs_borrow("kisses"), "#f472b6", "heart"),
                         (sum(getattr(girl, "Orgasms", {}).values()), _tl(_("ORGASMS")).capitalize(), "#c084fc", "sparkle"),
                         (_al.get("showered_together", 0), _gs_borrow("showers"), "#60a5fa", "drop")]
        v["seen"] = [_t for _t, _on in ((_("Saw boobs"), _al.get("player_saw_boobs", 0) > 0), (_("Saw pussy"), _al.get("player_saw_pussy", 0) > 0),
                                         (_("She saw you"), _al.get("girl_saw_penis", 0) > 0)) if _on]
        if not girl.get_flag("discovered_virgin"):
            v["virginity"] = None
        elif girl.has_trait("virgin"):
            v["virginity"] = ("Virgin", "#4ade80")
        elif getattr(girl, "_hc_virginity_uncertain", False):
            v["virginity"] = ("Virgin (?)", "#fbbf24")
        elif getattr(girl, "virginity_taken_by_player", False):
            v["virginity"] = (_("Not virgin (taken by you)"), "#f472b6")
        else:
            v["virginity"] = (_("Not virgin (before you)"), _PK_TEXT)
        # acts only count once: a position (cowgirl, ...) always comes with "sex"
        v["acts_total"] = sum(_n for _k, _n in _sa.items() if _k not in _SEX_POSITION_KEYS)
        v["acts"] = [(_pk_t(_label), _sa[_k], "#f472b6") for _k, _label in _GS_ACT_LABELS if _sa.get(_k, 0) > 0]
        if getattr(girl, "CreampieCounts", 0) > 0:
            v["acts"].append((_pk_t("Creampie"), girl.CreampieCounts, "#fb923c"))
        if getattr(girl, "_atm_count", 0) > 0:
            v["acts"].append(("ATM", girl._atm_count, "#fb923c"))
        v["fav_act"] = _pk_t(_GS_FAV_NAMES.get(getattr(girl, "FavoriteAct", None), "Unknown")) if girl.get_flag("discovered_fav_act") else None
        v["bf_exp"] = []
        if _partner_known:
            _bfh = getattr(girl, "bf_history", {})
            for _k, _label in _GS_BF_ACTS:
                _never = girl.get_flag("discovered_bf_never_%s" % _k)
                _done = girl.get_flag("discovered_bf_done_%s" % _k)
                # told "never" and hardcore mode changed it since = uncertain
                _state = ("uncertain" if _bfh.get(_k, False) else False) if _never else (True if _done else None)
                if _state is not None:
                    v["bf_exp"].append((_pk_t(_label), _gs_borrow(_GS_BF_STATE[_state][0]), _GS_BF_STATE[_state][1]))
        v["threesomes"] = [(_girl_avatar_by_gid(_g.gid), _g.Name, girl.get_history_with(_g.gid, "threesome")) for _g in ALL_GIRLS
                           if _g.gid != girl.gid and girl.get_history_with(_g.gid, "threesome") > 0]
        v["public_caught"] = girl.GetActionCount("caught_public_sex") if hasattr(girl, "GetActionCount") else 0

        # ---- life
        v["study"] = False if girl_type(girl) != "student" else (_pk_tier("study", getattr(girl, "study_level", 0)) if girl.get_flag("discovered_study_level") else None)
        _food = {"steak": _tr("Steak"), "pasta": _tr("Pasta"), "chicken": _tr("Chicken"), "salad": _tr("Salad")}
        _drink = {"low": _tr("Beer"), "med": _tr("Vodka"), "high": _tr("Whiskey")}
        _brand = getattr(girl, "FavoriteBrand", None)
        v["prefs"] = [(_tr("Favorite food"), _food.get(getattr(girl, "FavoriteDish", None), _tr("Unknown")) if girl.get_flag("discovered_fav_dish") else None),
                      (_tr("Favorite drink"), _drink.get(getattr(girl, "FavoriteDrink", None), _tr("Unknown")) if girl.get_flag("discovered_fav_drink") else None)]
        if girl.get_flag("discovered_fav_drink"):          # the brand only matters once he knows what she drinks
            v["prefs"].append((_tr("Preferred brand"), (_tr(DRINKS[_brand]["label"]) if _brand in DRINKS else _tr("Unknown")) if girl.get_flag("discovered_fav_brand") else None))
        _gt_loved, _gt_meh = gift_taste_discovered(girl)          # her taste in gifts, once each gift showed it (shop.rpy)
        if _gt_loved:
            v["prefs"].append((_tr("Loves"), ", ".join(_gt_loved)))
        if _gt_meh:
            v["prefs"].append((_tr("Not a fan"), ", ".join(_gt_meh)))
        v["friends"] = [(_girl_avatar_by_gid(_g.gid), _g.Name) + _pk_tier("friends", girl.get_like_for(_g.gid)) for _g in ALL_GIRLS if _g.gid != girl.gid and str(_g.gid) in girl.Girl_like]
        _pn_from = getattr(girl, "petname_from_player", None)
        _pn_for = getattr(girl, "petname_for_player", None)
        v["petnames"] = [(_gs_borrow(_cap), _tr(_pn)) for _cap, _pn in (("call_her", _pn_from), ("calls_you", _pn_for)) if _pn]
        _paid = getattr(girl, "_financial_total_paid", 0)
        _gifts = getattr(girl, "_total_gifts_value", 0)
        v["spending"] = [(_n, _gs_borrow(_cap), _col, _ic) for _n, _cap, _col, _ic in (
            ("%dx" % getattr(girl, "_blackmail_times", 0), "blackmailed", "#fca5a5", "eye"),
            ("$%d" % _paid, "paid", "#4ade80", "coin"),
            ("$%d" % _gifts, "gifts", "#4ade80", "coin")) if _n not in ("0x", "$0")]
        v["spent_total"] = (_paid + _gifts) if (_paid > 0 and _gifts > 0) else 0
        v["caught_cheating"] = _al.get("caught_player_cheating", 0)
        # words of the rows that are plain "caption ... number"
        v["cap"] = dict((_k, _gs_borrow(_k)) for _k in ("spent", "caught_you", "caught_together"))
        v["virgin_knowledge"] = [_tl(_GS_THINKS_VIRGIN).replace("[_vk_n]", GIRL_BY_ID[_gid].Name)
                                 for _gid, _val in getattr(girl, "knows_virgin", {}).items() if _val and _gid in GIRL_BY_ID]
        return v


# ------------------------------------------------------------ the screen
screen phone_girl_status_screen(girl, tab="overview"):

    modal True
    zorder 200

    default _gs_tab = tab
    default _gs_hint_open = False

    $ v = girl_status_view(girl)
    $ _gs_accent = v["accent"]
    $ _gs_body_y = PH_CY_HEADER + _PK_HERO_H + _PK_TABS_H + 8
    $ _gs_body_h = _PH_SCREEN_BOTTOM - _gs_body_y - 6

    use pk_page():

        # ---- hero: her face in her color, her name, what she is to him
        use pk_hero(girl.Name, _gs_accent, avatar=_girl_avatar_by_gid(girl.gid)):
            if v["relationship"]:
                hbox:
                    spacing 6
                    use pk_chip(v["relationship"][0], v["relationship"][1])
                    if v["partner_chip"]:
                        use pk_chip(v["partner_chip"][0], v["partner_chip"][1])
            else:
                hbox:
                    spacing 10
                    text _("RELATIONSHIP"):
                        style "phone_text"
                        size 13
                        kerning 1.0
                        color _PK_MUTED
                        yalign 0.5
                    use pk_locked()

        use pk_tabs([(_id, _tl(_cap).upper(), _ic) for _id, _cap, _ic in _GS_TABS], _gs_tab, _gs_accent, "_gs_tab",
                    PH_CY_HEADER + _PK_HERO_H, "phone_girl_status_screen", "gs_vp")

        # ---- body
        viewport:
            id "gs_vp"
            xpos PH_CX
            ypos _gs_body_y
            xsize PH_CW
            ysize _gs_body_h
            mousewheel True
            draggable True
            scrollbars None

            vbox:
                spacing 10
                xsize PH_CW - 14

                # ==================================================== OVERVIEW
                if _gs_tab == "overview":

                    use pk_card(_("STATS"), _gs_accent, "stats"):
                        for _l, _val, _max, _col in v["stats"]:
                            use pk_bar(_l, _val, _max, _col, ("%d/%d" % (_val, v["stat_caps"][_l])) if _l in v["stat_caps"] else str(_val))
                        if v["sexuality"]:
                            use pk_row(_tr("Sexuality"), v["sexuality"][0], v["sexuality"][1], chip=True)

                    if v["partner"]:
                        use pk_card(v["partner"]["title"], "#7ecbff", "person"):
                            if v["partner"]["loyalty"]:
                                use pk_row(v["partner"]["loyalty"][0], v["partner"]["loyalty"][1], v["partner"]["loyalty"][2], chip=True)
                            for _l, _val, _max, _col, _tier, _tcol in v["partner"]["bars"]:
                                use pk_bar(_l, _val, _max, _col, _tier, _tcol, 132)

                    use pk_card(_("PERSONALITY"), "#c084fc", "sparkle"):
                        if v["traits"]:
                            hbox:
                                spacing 6
                                box_wrap True
                                box_wrap_spacing 6
                                for _t, _on in v["traits"]:
                                    use pk_chip(_t, ("#c084fc" if _on else "#64748b"), strike=(not _on))
                        elif v["acts_total"] == 0:
                            text _("Nothing discovered yet"):
                                style "phone_text"
                                size 16
                                color _PK_DIM
                        else:
                            use pk_locked()

                    if v["evolved"]:
                        use pk_card(_("EVOLVED"), "#fbbf24", "evolve"):
                            for _old, _new in v["evolved"]:
                                hbox:
                                    spacing 8
                                    use pk_chip(_old, "#64748b", strike=True)
                                    if _new:
                                        add _pk_icon("next", "#fbbf24") yalign 0.5
                                        use pk_chip(_new, "#fbbf24")
                                    else:
                                        text _tl(_("lost")):
                                            style "phone_text"
                                            size 15
                                            color _PK_DIM
                                            yalign 0.5

                    # ==================================================== STORY
                    if v["story_card"]:
                        $ _sc = v["story_card"]
                        use pk_card(_("HER STORY"), "#f59e0b", "star"):
                            use pk_row(_("Step"), _sc["step_name"], "#f59e0b", chip=True)
                            if _sc["opened"]:
                                null height 2
                                text _tl_fmt(_("This step opened: %s"), _sc["opened"]):
                                    style "phone_text"
                                    size 13
                                    color "#cbd5e1"
                                    xsize _PK_INNER_W - 8
                            if _sc["route_taken"]:
                                use pk_row(_("Route"), _sc["route_taken"], "#a78bfa", chip=True)
                            if _sc["step"] >= _sc["top"]:
                                null height 4
                                text _("Story complete"):
                                    style "phone_text"
                                    size 15
                                    color "#4ade80"
                            if _sc["hint"] or _sc["hint_routes"]:
                                null height 6
                                if _gs_hint_open:
                                    button:
                                        xfill True
                                        background _pk_pill("#f59e0b", 0.12)
                                        padding (12, 10)
                                        action SetScreenVariable("_gs_hint_open", False)
                                        vbox:
                                            spacing 8
                                            if _sc["hint_routes"]:
                                                # before the first unlock: the lock warning, then one block
                                                # per lane (label, icon and color from _GS_LANES)
                                                hbox:
                                                    spacing 8
                                                    add _pk_icon("bolt", "#f59e0b") yalign 0.0 yoffset 2
                                                    text _("Two routes. The first you advance locks the other out."):
                                                        style "phone_text"
                                                        size 14
                                                        color "#fbbf24"
                                                        xsize _PK_INNER_W - 40
                                                for _gs_lane, _gs_lt in _sc["hint_routes"]:
                                                    $ _gs_ln, _gs_li, _gs_lc = _GS_LANES.get(_gs_lane, (_gs_lane, "star", "#f59e0b"))
                                                    frame:
                                                        background _pk_pill(_gs_lc, 0.10)
                                                        padding (10, 8)
                                                        xfill True
                                                        hbox:
                                                            spacing 8
                                                            add _pk_icon(_gs_li, _gs_lc) yalign 0.0 yoffset 2
                                                            vbox:
                                                                spacing 2
                                                                text _pk_t(_gs_ln):
                                                                    style "phone_text"
                                                                    size 14
                                                                    color _gs_lc
                                                                    bold True
                                                                text _gs_lt:
                                                                    style "phone_text"
                                                                    size 13
                                                                    color "#e2e8f0"
                                                                    xsize _PK_INNER_W - 78
                                            else:
                                                hbox:
                                                    spacing 8
                                                    add _pk_icon("bolt", "#f59e0b") yalign 0.0 yoffset 2
                                                    text _sc["hint"]:
                                                        style "phone_text"
                                                        size 14
                                                        color "#fbbf24"
                                                        xsize _PK_INNER_W - 40
                                else:
                                    button:
                                        xfill True
                                        background _pk_pill("#f59e0b", 0.12)
                                        hover_background _pk_pill("#f59e0b", 0.22)
                                        padding (10, 8)
                                        action SetScreenVariable("_gs_hint_open", True)
                                        at pk_pulse
                                        hbox:
                                            spacing 6
                                            add _pk_icon("bolt", "#f59e0b") yalign 0.5
                                            text _("Hint"):
                                                style "phone_text"
                                                size 14
                                                bold True
                                                color "#fbbf24"
                                                yalign 0.5

                # ==================================================== INTIMACY
                elif _gs_tab == "intimacy":

                    hbox:
                        xalign 0.5
                        spacing 6
                        for _n, _cap, _col, _ic in v["counters"]:
                            use pk_box(str(_n), _cap, _col, int((_PK_CARD_W - 12) / 3), _ic)

                    use pk_card(_("VIRGINITY"), "#4ade80", "flower"):
                        if v["virginity"]:
                            hbox:
                                use pk_chip(v["virginity"][0], v["virginity"][1])
                        else:
                            use pk_locked()

                    use pk_card(_("SEX HISTORY"), "#f472b6", "flame"):
                        if v["acts"]:
                            hbox:
                                spacing 6
                                box_wrap True
                                box_wrap_spacing 6
                                for _l, _n, _col in v["acts"]:
                                    use pk_chip(_l, _col, count=_n)
                        else:
                            text _("None yet"):
                                style "phone_text"
                                size 16
                                color _PK_DIM
                        if v["seen"]:
                            hbox:
                                spacing 6
                                box_wrap True
                                box_wrap_spacing 6
                                for _t in v["seen"]:
                                    use pk_chip(_t, "#4ade80")

                    use pk_card(_("FAVORITE ACT"), "#f9a8d4", "star"):
                        if v["fav_act"]:
                            hbox:
                                use pk_chip(v["fav_act"], "#f9a8d4")
                        else:
                            use pk_locked()

                    if v["bf_exp"]:
                        use pk_card(_("BF EXPERIENCE"), "#f87171", "couple"):
                            for _l, _state, _col in v["bf_exp"]:
                                use pk_row(_l, _state, _col, chip=True)

                    use pk_card(_("THREESOMES"), "#c084fc", "trio"):
                        if v["threesomes"]:
                            for _av, _name, _n in v["threesomes"]:
                                use pk_row(_name, "%dx" % _n, "#c084fc", chip=True, avatar=_av)
                        else:
                            use pk_row(_("None yet"), "", "#888")

                    if v["public_caught"] > 0:
                        use pk_card(_("CAUGHT IN PUBLIC"), "#fb923c", "eye"):
                            use pk_row(v["cap"]["caught_together"], "%dx" % v["public_caught"], "#fb923c", chip=True)

                # ==================================================== LIFE
                else:

                    if v["study"] is not False:
                        use pk_card(_("STUDY LEVEL"), "#60a5fa", "book"):
                            if v["study"]:
                                hbox:
                                    use pk_chip(v["study"][0], v["study"][1])
                            else:
                                use pk_locked()

                    use pk_card(_("PREFERENCES"), "#fbbf24", "glass"):
                        for _l, _val in v["prefs"]:
                            use pk_row(_l, _val)

                    if v["friends"]:
                        use pk_card(_("FRIENDSHIPS"), "#a3e635", "people"):
                            for _av, _name, _tier, _col in v["friends"]:
                                use pk_row(_name, _tier, _col, chip=True, avatar=_av)

                    if v["petnames"]:
                        use pk_card(_("PET NAMES"), "#f472b6", "bubble"):
                            for _cap, _pn in v["petnames"]:
                                use pk_row(_cap, _pn, "#f472b6", chip=True)

                    if v["spending"]:
                        use pk_card(_("COERCION & SPENDING"), "#fbbf24", "coin"):
                            hbox:
                                xalign 0.5
                                spacing 6
                                for _n, _cap, _col, _ic in v["spending"]:
                                    use pk_box(_n, _cap, _col, int((_PK_INNER_W - 12) / 3), _ic)
                            if v["spent_total"]:
                                use pk_row(v["cap"]["spent"], "$%d" % v["spent_total"])

                    if v["caught_cheating"] > 0:
                        use pk_card(_("CAUGHT CHEATING"), "#ef4444", "broken"):
                            use pk_row(v["cap"]["caught_you"], "%dx" % v["caught_cheating"], "#fca5a5", chip=True)

                    if v["virgin_knowledge"]:
                        use pk_card(_("VIRGINITY KNOWLEDGE"), "#f9a8d4", "bubble"):
                            for _vk_line in v["virgin_knowledge"]:
                                text _vk_line:
                                    style "phone_text"
                                    size 16
                                    color "#f9a8d4"

                null height 12

        use pk_scrollmark("gs_vp", _gs_accent, _gs_body_y, _gs_body_h)

        use phone_chin_buttons(
            back_action=[Hide("phone_girl_status_screen"), Show("phone_contact_options_screen", girl=girl)])
