# ============================================================
# QA: NTR System Tests (Interactive)
# Run from Ren'Py console (Shift+O):  renpy.jump("qa_ntr_menu")
# ============================================================

init 999 python:

    def _qa_ntr_setup(girl, level=2, trait=None, attitude=0, npc_same_loc=False):
        """Configure girl + NPC partner for NTR testing."""
        npc = get_npc_partner_for(girl)
        if npc is None:
            if not girl.has_npc_partner():
                # NEW partner: set_npc_partner() wipes the per-partner mirrors and creates the NPC itself
                girl.set_npc_partner(girl.npc_partner_canonical_id("male"), gender="male")
            else:
                girl._ensure_npc_partner_visual()   # flagged partner without an NPC object in the registry
            npc = get_npc_partner_for(girl)
            print("[QA_NTR] %s: test partner = %s" % (girl.gid, getattr(npc, "name", None)))

        npc._ntr_active = True
        npc._ntr_boundary_level = level
        npc._ntr_boundary_bar = 0
        npc.traits = set(["ntr"])
        npc.friendship_with_player = 500
        npc.love_for_girl = 750
        _ntr_save_state(npc, girl)
        girl._ntr_boundary_discovered = True   # her condom-rule pools need the arrangement to be KNOWN (_ntr_active_discovered)

        if npc_same_loc:
            npc.loc = getattr(store, "CurrentLocation", "room")
        else:
            npc.loc = "offscreen_qa"

        _qa_trait_pool = ("cum_slut", "hate_cum", "hardcore_sex", "cute_sex", "cheater", "loyal")
        for t in _qa_trait_pool:
            girl.traits.discard(t)
        if trait:
            girl.traits.add(trait)

        girl._financial_attitude = attitude
        girl._financial_times = {0: 0, 1: 4, 2: 10, 3: 20}.get(attitude, 0)

        store._scene_girl = girl
        store._doggy_girl = girl

        print("[QA_NTR] Setup: girl=%s level=%d trait=%s attitude=%d npc_loc=%s" % (
            girl.gid, level, trait, attitude, npc.loc))
        return npc

    def _qa_ntr_cleanup(girl):
        """Reset NTR state after test."""
        condom_break_reset()   # also clears the NTR level snapshot / partner_saw / notice looks
        store.condom_active = False
        store._ntr_partner_watching = False
        store._ntr_watching_npc = None
        store._ntr_discovery_kick = False
        store._financial_accepted = False
        store._financial_failed = False

    def _qa_ntr_get_girl():
        """Get first available girl for testing."""
        for gid in ("gwen", "rogue", "ntw"):
            g = GIRL_BY_ID.get(gid)
            if g and g in ALL_GIRLS:
                return g
        return None


label qa_ntr_menu:
    scene black
    python:
        _qa_girl = _qa_ntr_get_girl()
        if _qa_girl is None:
            renpy.say(None, "No enabled girl found for testing.")
            renpy.jump("main_loop")
        _qa_girl_name = _qa_girl.Name
    "[_qa_girl_name] selected for NTR QA tests."

label .main:
    menu:
        "== NTR QA Tests =="

        "Gap #1: Severity Witness Reactions":
            jump qa_ntr_severity

        "Gap #2: Condom Break + NTR Watching":
            jump qa_ntr_condom_break

        "Gap #5: Location Boundary Check":
            jump qa_ntr_location

        "Gap #6: Financial + NTR":
            jump qa_ntr_financial

        "Change test girl":
            jump qa_ntr_pick_girl

        "Exit QA":
            jump main_loop


label qa_ntr_pick_girl:
    menu:
        "Pick girl for testing:"
        "Gwen" if GIRL_BY_ID.get("gwen") and GIRL_BY_ID["gwen"] in ALL_GIRLS:
            $ _qa_girl = GIRL_BY_ID["gwen"]
        "Rogue" if GIRL_BY_ID.get("rogue") and GIRL_BY_ID["rogue"] in ALL_GIRLS:
            $ _qa_girl = GIRL_BY_ID["rogue"]
        "Negasonic" if GIRL_BY_ID.get("ntw") and GIRL_BY_ID["ntw"] in ALL_GIRLS:
            $ _qa_girl = GIRL_BY_ID["ntw"]
    $ _qa_girl_name = _qa_girl.Name
    "[_qa_girl_name] selected."
    jump qa_ntr_menu.main


# ════════════════════════════════════════════
# GAP #1: ACT-SEVERITY WITNESS REACTIONS
# ════════════════════════════════════════════
label qa_ntr_severity:
    "Testing act-severity witness reactions."
    "NPC will 'catch' [_qa_girl_name] in acts of different severities."

    menu:
        "Pick severity tier:"
        "Mild (HJ)":
            $ _qa_sev_act = "hj"
        "Moderate (BJ)":
            $ _qa_sev_act = "bj"
        "Severe (sex)":
            $ _qa_sev_act = "sex"
        "Extreme (anal)":
            $ _qa_sev_act = "anal"

    $ _qa_npc = _qa_ntr_setup(_qa_girl, level=4)
    $ _qa_npc._ntr_active = False

    python:
        _sev = _NPC_ACT_SEVERITY.get(_qa_sev_act, "moderate")
        _f_before = _qa_npc.friendship_with_player
        _l_before = _qa_npc.love_for_girl
        print("[QA_NTR_SEV] act=%s severity=%s friendship=%d love=%d" % (_qa_sev_act, _sev, _f_before, _l_before))

    "Act: [_qa_sev_act] | Severity: [_sev]"
    "NPC friendship: [_f_before] | NPC love: [_l_before]"
    "Calling witness reaction..."

    call _npc_partner_witness_reaction(_qa_girl, _qa_npc, _qa_sev_act) from _qa_call_witness_sev

    python:
        _f_after = _qa_npc.friendship_with_player
        _l_after = _qa_npc.love_for_girl
        _f_delta = _f_after - _f_before
        _l_delta = _l_after - _l_before
    "Result: friendship [_f_before] -> [_f_after] ([_f_delta]) | love [_l_before] -> [_l_after] ([_l_delta])"

    $ _qa_ntr_cleanup(_qa_girl)
    jump qa_ntr_menu.main


# ════════════════════════════════════════════
# GAP #2: CONDOM BREAK + NTR WATCHING
# ════════════════════════════════════════════
label qa_ntr_condom_break:
    "Testing condom break while NPC watches (level 2)."

    menu:
        "Girl trait for this test:"
        "cum_slut":
            $ _qa_cb_trait = "cum_slut"
        "hate_cum":
            $ _qa_cb_trait = "hate_cum"
        "hardcore_sex":
            $ _qa_cb_trait = "hardcore_sex"
        "cute_sex":
            $ _qa_cb_trait = "cute_sex"
        "cheater":
            $ _qa_cb_trait = "cheater"
        "None (default)":
            $ _qa_cb_trait = None

    $ _qa_npc = _qa_ntr_setup(_qa_girl, level=2, trait=_qa_cb_trait)

    menu:
        "Condom break scenario:"
        "NPC watching + told (girl knows)":
            python:
                store._condom_broken = True
                store._condom_broken_told = True
                store._condom_broken_hidden = False
                store._ntr_partner_watching = True
                store._ntr_watching_npc = _qa_npc
            "Condom broke, girl was told. NPC is watching."
            "NPC level BEFORE: [_qa_npc._ntr_boundary_level]"
            call _ntr_condom_break_watching(_qa_girl, _qa_npc) from _qa_call_cbreak_told
            "NPC level AFTER: [_qa_npc._ntr_boundary_level] (should be 3)"

        "NPC watching + hidden (girl doesn't know)":
            python:
                store._condom_broken = True
                store._condom_broken_told = False
                store._condom_broken_hidden = True
                store.condom_active = True   # the torn condom is still on: that is what makes the mode "hidden"
                store._ntr_partner_watching = True
                store._ntr_watching_npc = _qa_npc
            "Condom broke, girl doesn't know. NPC is watching and NOTICES (label called directly, no roll)."
            "NPC level BEFORE: [_qa_npc._ntr_boundary_level]"
            call _ntr_condom_break_watching(_qa_girl, _qa_npc) from _qa_call_cbreak_hidden
            "NPC level AFTER: [_qa_npc._ntr_boundary_level] (should be 3). Partner saw: [_condom_break_partner_saw] (should be silent). She heard nothing."

        "NPC watching + hidden: notice ROLL through the tick (up to 12 ticks)":
            python:
                store._condom_broken = True
                store._condom_broken_told = False
                store._condom_broken_hidden = True
                store.condom_active = True
                store._condom_break_ntr_level = 2
                store._ntr_partner_watching = True
                store._ntr_watching_npc = _qa_npc
                _qa_cb_ticks = 0
            "Each tick rolls NTR_CBREAK_NOTICE (first look 35 percent, then 12 percent). log.txt shows one [NTR_CBREAK_NOTICE] line per roll."
            while _condom_break_partner_saw is None and _qa_cb_ticks < 12:
                $ _qa_cb_ticks += 1
                call _npc_partner_detection_tick(_qa_girl, "doggy") from _qa_call_cbreak_roll
            "Ticks: [_qa_cb_ticks]. Partner saw: [_condom_break_partner_saw]. NPC level: [_qa_npc._ntr_boundary_level]."

        "NPC noticed earlier + she finds out now (knew)":
            python:
                store._condom_broken = True
                store._condom_broken_told = False
                store._condom_broken_hidden = False
                store.condom_active = False
                store._condom_break_ntr_level = 2
                store._condom_break_partner_saw = "silent"
                _qa_npc._ntr_boundary_level = 3
                _ntr_save_state(_qa_npc, _qa_girl)
                store._ntr_partner_watching = True
                store._ntr_watching_npc = _qa_npc
            "He silently noticed before. She has just found out. Expect ONE spoken 'I already knew' line, level stays 3."
            call _npc_partner_detection_tick(_qa_girl, "doggy") from _qa_call_cbreak_knew
            "NPC level: [_qa_npc._ntr_boundary_level] (should be 3). Partner saw: [_condom_break_partner_saw] (should be spoken)."

        "Hidden + he noticed, then she discovers (snapshot keeps her level 2 pools)":
            python:
                store._condom_broken = True
                store._condom_broken_told = False
                store._condom_broken_hidden = True
                store.condom_active = True
                store._condom_break_ntr_level = 2
                store._condom_break_partner_saw = "silent"
                _qa_npc._ntr_boundary_level = 3
                _ntr_save_state(_qa_npc, _qa_girl)
            "The partner is ALREADY level 3 (he noticed silently). She must still react with the level 2 'the condom was his rule' pools."
            call CondomBreakDiscovery(_qa_girl, "doggy") from _qa_call_cbreak_disc_snap

        "Girl discovers hidden break (NTR context)":
            python:
                store._condom_broken = True
                store._condom_broken_hidden = True
                store._condom_broken_told = False
            "Girl discovers break with NTR level 2 context."
            "Trait: [_qa_cb_trait]. Calling CondomBreakDiscovery..."
            call CondomBreakDiscovery(_qa_girl, "doggy") from _qa_call_cbreak_disc

    $ _qa_ntr_cleanup(_qa_girl)
    jump qa_ntr_menu.main


# ════════════════════════════════════════════
# GAP #5: LOCATION BOUNDARY CHECK
# ════════════════════════════════════════════
label qa_ntr_location:
    "Testing girl's location-aware NTR boundary check."

    menu:
        "NPC location:"
        "Same location as player (hard block expected)":
            $ _qa_loc_same = True
        "Different location (temptation gate)":
            $ _qa_loc_same = False

    $ _qa_npc = _qa_ntr_setup(_qa_girl, level=1, npc_same_loc=_qa_loc_same)
    $ _qa_girl.Temptation = 5

    python:
        _qa_loc_act = "sex"
        _blocked, _reason = is_loyalty_blocked(_qa_girl, _qa_loc_act, False)
        _npc_loc = _qa_npc.loc
        _player_loc = store.CurrentLocation

    "Action: [_qa_loc_act] | NTR level: 1 (non-penetration only)"
    "NPC location: [_npc_loc] | Player location: [_player_loc]"
    "Girl temptation: [_qa_girl.Temptation]"
    "Result: blocked=[_blocked] reason=[_reason]"

    if _qa_loc_same:
        "Expected: blocked=True, reason=ntr_boundary_nearby"
    else:
        "Expected: blocked=True, reason=ntr_boundary (temptation 5 < gate 9)"

    menu:
        "Test high temptation bypass (temptation=10)?"
        "Yes":
            $ _qa_girl.Temptation = 10
            python:
                _blocked2, _reason2 = is_loyalty_blocked(_qa_girl, _qa_loc_act, False)
            "Temptation 10: blocked=[_blocked2] reason=[_reason2]"
            if _qa_loc_same:
                "Same location = always blocked regardless of temptation."
            else:
                "Expected: blocked=False (temptation 10 >= gate 9)"
        "No":
            pass

    $ _qa_girl.Temptation = 0
    $ _qa_ntr_cleanup(_qa_girl)
    jump qa_ntr_menu.main


# ════════════════════════════════════════════
# GAP #6: FINANCIAL COERCION + NTR
# ════════════════════════════════════════════
label qa_ntr_financial:
    "Testing financial coercion with NTR boundary surcharge."

    menu:
        "Girl trait:"
        "cum_slut":
            $ _qa_fin_trait = "cum_slut"
        "hate_cum":
            $ _qa_fin_trait = "hate_cum"
        "cheater":
            $ _qa_fin_trait = "cheater"
        "poor":
            $ _qa_fin_trait = "poor"
        "None (default)":
            $ _qa_fin_trait = None

    menu:
        "Financial attitude stage:"
        "0 (Reluctant - should REFUSE)":
            $ _qa_fin_att = 0
        "1 (Resigned - hesitant price)":
            $ _qa_fin_att = 1
        "2 (Transactional - casual price)":
            $ _qa_fin_att = 2
        "3 (Dependent - lowest price)":
            $ _qa_fin_att = 3

    $ _qa_npc = _qa_ntr_setup(_qa_girl, level=1, trait=_qa_fin_trait, attitude=_qa_fin_att)
    $ store.Player.cash = 99999

    python:
        _qa_fin_act = "sex"
        _price_normal = _calc_financial_price(_qa_girl, _qa_fin_act)

    "Act: [_qa_fin_act] | NTR level: 1 (non-penetration only)"
    "Trait: [_qa_fin_trait] | Attitude: [_qa_fin_att]"
    "Price (includes NTR surcharge): $[_price_normal]"

    menu:
        "Run _financial_attempt for full dialogue flow?"
        "Yes (will show actual dialogue)":
            call _financial_attempt(_qa_girl, _qa_fin_act) from _qa_call_fin_ntr
            python:
                _qa_fin_accepted = store._financial_accepted
            "Financial accepted: [_qa_fin_accepted]"
        "No (price check only)":
            python:
                _qa_npc_temp = _qa_npc
                _qa_npc_temp._ntr_active = False
                _price_without_ntr = _calc_financial_price(_qa_girl, _qa_fin_act)
                _qa_npc_temp._ntr_active = True
            "Price WITHOUT NTR surcharge: $[_price_without_ntr]"
            "Price WITH NTR surcharge: $[_price_normal]"
            if _qa_fin_trait == "cheater":
                "Cheater mult: x1.3"
            else:
                "Normal mult: x2.0"

    menu:
        "Also test extras (condom_remove / creampie)?"
        "Yes":
            python:
                _ex_condom = _calc_financial_extra_price(_qa_girl, "condom_remove")
                _ex_cream = _calc_financial_extra_price(_qa_girl, "creampie")
            "Condom remove price: $[_ex_condom]"
            "Creampie price: $[_ex_cream]"
        "No":
            pass

    $ _qa_ntr_cleanup(_qa_girl)
    jump qa_ntr_menu.main
