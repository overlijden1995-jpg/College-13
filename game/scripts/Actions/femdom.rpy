# ============================================================
# femdom.rpy... the femdom trait's mechanics (docs/plan_femdom.md)
# Her Obed gain: TRAIT_STAT_GAIN_MULT (characters_stats.rpy). Her discovery phase: EAGER_TRAITS.
# The control corruption (femdom -> none -> submissive): CORRUPTION_RULES["control"].
# Who controls a scene: POSITION_CONTROL / ACT_CONTROL (approval.rpy, scene_control()).
# Lines: SCENE_LINES "femdom_*" keys in Dialogs/femdom_lines.rpy (scene_pick_line: her gid first).
#
# F2: her ORDERS during sex. They join the sub-event roll (SubEvents.rpy sub_event_dispatch); each one is a menu:
# obey (Love+) / refuse (she gets angry, Obed-, counts toward the control corruption) / stand up to her (won: Obed+,
# Love-, counts too; lost: she does it her way and mocks him). Only a veteran (past her discovery phase) FORCES:
# then refusing needs her Obed or his strength (the forced-cum rules). Standing orders (hold it, where to cum, me
# first) are judged when he cums (process_cum -> femdom_note_cum) and she says so after (_post_cum_central).
# ============================================================

default _femdom_refused = False
default _femdom_orders_done = {}
default _femdom_edge = None
default _femdom_cum_demand = None
default _femdom_me_first = None
default _femdom_verdicts = []
default _femdom_ticks = 0
default _femdom_gate_ok = True

init python:

    # Obed a femdom girl loses when he refuses one of her requests (D1), random in this range
    FEMDOM_REFUSAL_OBED = (5, 10)
    # Obed she gains when he stands up to her and wins (her femdom multiplier still applies), and the Love it costs
    FEMDOM_DEFY_OBED = 8
    FEMDOM_DEFY_LOVE = -3

    # How each girl gives orders (plan section 3). intensity: how often her orders come; humiliate: chance she mocks
    # him when he finishes too fast; pace: which way she pushes it ("faster" / "slower" / "mixed"); orders: weight of
    # each order when several can come. A girl missing here uses "_default". Shion's turning stages will scale hers.
    FEMDOM_PROFILE = {
        "gwen":  {"intensity": 1.0, "humiliate": 0.5, "pace": "mixed",
                  "orders": {"challenge": 30, "take_over": 15, "pace_order": 15, "no_cum": 15, "cum_demand": 15, "me_first": 10}},
        "rogue": {"intensity": 0.9, "humiliate": 0.25, "pace": "faster",
                  "orders": {"challenge": 15, "take_over": 20, "pace_order": 20, "no_cum": 10, "cum_demand": 15, "me_first": 20}},
        "ntw":   {"intensity": 1.5, "humiliate": 1.0, "pace": "faster",
                  "orders": {"challenge": 20, "take_over": 20, "pace_order": 20, "no_cum": 20, "cum_demand": 15, "me_first": 15}},
        "tenny": {"intensity": 1.2, "humiliate": 0.4, "pace": "faster",
                  "orders": {"challenge": 10, "take_over": 15, "pace_order": 20, "no_cum": 20, "cum_demand": 20, "me_first": 15}},
        "shion": {"intensity": 1.5, "humiliate": 0.8, "pace": "slower",
                  "orders": {"challenge": 15, "take_over": 20, "pace_order": 15, "no_cum": 25, "cum_demand": 15, "me_first": 10}},
        "_default": {"intensity": 1.0, "humiliate": 0.3, "pace": "mixed",
                  "orders": {"challenge": 15, "take_over": 15, "pace_order": 20, "no_cum": 15, "cum_demand": 15, "me_first": 15}},
    }

    # The sub-event roll has no "nothing happens" weight: her orders join a roll only with this chance x intensity,
    # each order comes at most FEMDOM_ORDER_CAP times per sex session (1 when missing), FEMDOM_ORDER_TOTAL in all.
    # Simulated (15-tick scene): Rogue ~1.7 orders, Gwen ~1.8, Tenny ~2.1, NTW ~2.4 (0.45 made all of them hit 3).
    FEMDOM_ORDER_CHANCE = 0.30
    FEMDOM_ORDER_CAP = {"pace_order": 2}
    FEMDOM_ORDER_TOTAL = 3
    FEMDOM_EDGE_TICKS = 3               # "Don't you dare cum yet": action ticks he has to hold it
    FEMDOM_ORDER_FOCUS = 60             # his Focus (0-100) from which she gives orders about his cum
    FEMDOM_POSITION_REFUSE = 0.5        # x intensity: she refuses to leave her position for his
    FEMDOM_FORCE_CUM_CHANCE = 0.30      # x intensity: a veteran on top keeps him inside (per cum)

    # What she may demand (femdom_cum_demand) -> the cum types (process_cum) that obey it
    FEMDOM_CUM_GROUPS = {
        "inside": ("inside", "condom_removed_inside"),
        "on_me":  ("outside", "tits", "ass", "face", "body", "back", "belly", "feet"),
        "mouth":  ("mouth",),
    }

    def femdom_profile(girl):
        return FEMDOM_PROFILE.get(getattr(girl, "gid", None), FEMDOM_PROFILE["_default"])

    def femdom_intensity(girl):
        """How strongly she gives orders (0 = she is not femdom). A canon femdom on her turn gives fewer orders at every
        stage (FEMDOM_TURN_INTENSITY, femdom_turn.rpy)."""
        if not girl.has_trait("femdom"):
            return 0.0
        return femdom_profile(girl)["intensity"] * FEMDOM_TURN_INTENSITY[femdom_stage(girl)]

    def femdom_on_path(girl):
        """Femdom now, or she lost it to his refusals and is on her way to submissive (CORRUPTION_RULES["control"])."""
        return girl.has_trait("femdom") or "femdom" in (getattr(girl, "evolved_traits", None) or {})

    def _femdom_count_refusal(girl, what):
        # A CANON femdom counts NOTHING before her gate (CANON_BREAK_RULES: her final story step; author's rule:
        # before it she never loses the trait, whatever he does). The first time the gate is open the old count is
        # zeroed: it grew all game long (only the firing was locked), and the residue would flip her instantly.
        if "femdom" in GIRLS_CONFIG.get(getattr(girl, "gid", None), {}).get("traits", ()):
            if not trait_canon_breakable(girl, "femdom"):
                print("[FEMDOM] %s: %s ignored by the control corruption (her canon gate is closed)" % (girl.gid, what))
                return
            if not getattr(girl, "_femdom_gate_opened", False):
                girl._femdom_gate_opened = True
                girl.CorruptionFemdomRefused = 0
                print("[FEMDOM] %s: her canon gate opened, the control count starts fresh" % girl.gid)
        girl.CorruptionFemdomRefused = getattr(girl, "CorruptionFemdomRefused", 0) + 1
        print("[FEMDOM] %s: %s counts toward the control corruption (%d)" % (girl.gid, what, girl.CorruptionFemdomRefused))
        girl.check_corruption("control")

    def femdom_request_refused(girl, what):
        """He refused one of her requests (what: "pace", "position", ...). On the femdom path the refusal counts
        toward the control corruption; while she still is femdom she also loses Obed. True = she is femdom: the
        caller plays her angry reaction (femdom_react_refused) instead of the usual one."""
        if not femdom_on_path(girl):
            return False
        _femdom = girl.has_trait("femdom")
        _loss = 0
        if _femdom:
            _loss = renpy.random.randint(*FEMDOM_REFUSAL_OBED)
            Change_Status(girl, "Obed", -_loss)
        print("[FEMDOM] %s: he refused her %s request (femdom=%s, Obed -%d)" % (girl.gid, what, _femdom, _loss))
        _femdom_count_refusal(girl, what)
        return _femdom and girl.has_trait("femdom")

    def femdom_react_refused(girl, what, scene_type=None):
        """The whole refusal: counted, and a femdom girl gets angry (face + line). True when she did."""
        _angry = femdom_request_refused(girl, what)
        if _angry:
            girl.discover("discovered_trait_femdom")
            set_scene_expression(girl, "angry")
            Say_Line(girl, scene_pick_line("femdom_refused", scene=scene_type, girl=girl))
            set_scene_expression(girl, "normal")
        return _angry

    def femdom_player_prevails(girl, scene_type):
        """He wins against her will: her Obed or his strength (the forced-cum rules of Cum.rpy)."""
        _why = _get_auto_resist_reason(girl)
        _won = bool(_why) or _resist_physical_check(scene_type)
        print("[FEMDOM] %s vs player in %s: %s (%s)" % (girl.gid, scene_type, "he wins" if _won else "she wins", _why or "physical"))
        return _won

    def femdom_defied(girl, scene_type, what):
        """He stood up to her. Won: Obed up, a little Love down, and it counts toward the control corruption.
        Lost: nothing changes, she does it her way (the caller plays that). Returns True when he won."""
        _won = femdom_player_prevails(girl, scene_type)
        if _won:
            Change_Status(girl, "Obed", FEMDOM_DEFY_OBED)
            Change_Status(girl, "Love", FEMDOM_DEFY_LOVE)
            _femdom_count_refusal(girl, what + " (stood up to her)")
            femdom_turn_note(girl, "defied", what)
        return _won

    def femdom_session_reset(why):
        """A new sex session: her order counts, her standing orders and her pending verdicts start over."""
        store._femdom_orders_done = {}
        store._femdom_edge = None
        store._femdom_cum_demand = None
        store._femdom_me_first = None
        store._femdom_verdicts = []
        store._femdom_ticks = 0
        store._femdom_turn_noted = set()
        store._subm_asks_done = 0
        store._sugar_scene_paid = 0
        print("[FEMDOM] session reset (%s)" % why)

    # ── Her orders: which can come now ──

    def femdom_pace_direction(girl, scene_type):
        """"faster" / "slower": where she pushes the pace now (her profile, bounded by the scene's speeds)."""
        _sv = _cum_cfg(scene_type, "speed_var")
        if not _sv:
            return None
        _spd = getattr(store, _sv, 0)
        _max = _cum_cfg(scene_type, "max_speed", 3)
        _dir = femdom_profile(girl)["pace"]
        if _dir == "mixed":
            _dir = renpy.random.choice(("faster", "slower"))
        if _dir == "faster" and _spd >= _max:
            _dir = "slower"
        elif _dir == "slower" and _spd <= 1:
            _dir = "faster"
        if (_dir == "faster" and _spd >= _max) or (_dir == "slower" and _spd <= 1):
            return None
        return _dir

    def femdom_cum_demand_options(girl, scene_type):
        """Where she may order him to cum in this scene ([] = she won't: hate_cum, a condom, a scene without a place)."""
        if girl.has_trait("hate_cum") or store.condom_active:
            return []
        if scene_type == "bj":
            return ["mouth"]
        if scene_type_is_penetration(scene_type):
            return (["inside"] if getattr(store, "_creampie_consent", None) == "allowed" else []) + ["on_me"]
        return []

    def _femdom_can_order(girl, scene_type, order):
        if store._femdom_orders_done.get(order, 0) >= FEMDOM_ORDER_CAP.get(order, 1):
            return False
        _focus = getattr(Player, "Focus", 0)
        _near = FEMDOM_ORDER_FOCUS <= _focus < 100
        _tv = _cum_cfg(scene_type, "tip_mode_var")
        _in_tip = bool(_tv and getattr(store, _tv, False))
        _sv = _cum_cfg(scene_type, "speed_var")
        _moving = bool(_sv) and getattr(store, _sv, 0) >= 1 and not _in_tip
        if order == "take_over":
            return (scene_type in ("doggy", "full_nelson", "laying_down") and not _any_rub_or_tip_active()
                    and store._femdom_ticks >= 3 and any(girl_has_pose(girl, _p) for _p in ("cowgirl", "reverse_cowgirl")))
        if order == "challenge":
            return _moving and store._femdom_ticks >= 2
        if order == "pace_order":
            return _moving and femdom_pace_direction(girl, scene_type) is not None
        if order == "no_cum":
            return _near and store._femdom_edge is None
        if order == "cum_demand":
            return _near and store._femdom_cum_demand is None and bool(femdom_cum_demand_options(girl, scene_type))
        if order == "me_first":
            return (FEMDOM_ORDER_FOCUS - 20 <= _focus < 100 and store._femdom_me_first is None
                    and store._session_girl_orgasms == 0 and girl.Lust < 90)
        return False

    # ── Her pace and take-over orders against her Obed (author, 2026-10-09): below 700 she never asks, the
    # pace and the position are hers whenever she wants ("rules"). From 700 the order comes back with his say
    # (the original obey / refuse / defy menu: "menu"). From 800 she asks instead of ordering ("asks"), and
    # from 900 she pleads and his word is final ("begs"). Any femdom girl, by her stat: never a gid check. ──
    FEMDOM_ORDER_OBED_MODES = ((900, "begs"), (800, "asks"), (700, "menu"))

    def femdom_order_mode(girl):
        """"rules" / "menu" / "asks" / "begs" for her pace_order and take_over, by her Obed. Only a CANON
        femdom rules without a menu below 700 (her trait cannot break before her story's gate); a common
        femdom keeps the refusable menu there, because his refusals are HOW her control corrodes
        (CORRUPTION_RULES "control", docs/plan_femdom.md D5)."""
        for _th, _m in FEMDOM_ORDER_OBED_MODES:
            if girl.Obed >= _th:
                return _m
        return "rules" if femdom_turn_applies(girl) else "menu"

    def femdom_order_candidates(girl, scene_type):
        """[("femdom_<order>", weight)]: her orders that can join this sub-event roll (none for a non-femdom girl,
        none past her session total, and only FEMDOM_ORDER_CHANCE x intensity of the time)."""
        _int = femdom_intensity(girl)
        if not _int or sum(store._femdom_orders_done.values()) >= FEMDOM_ORDER_TOTAL:
            return []
        if renpy.random.random() >= FEMDOM_ORDER_CHANCE * _int:
            return []
        return [("femdom_" + _o, _w) for _o, _w in sorted(femdom_profile(girl)["orders"].items())
                if _femdom_can_order(girl, scene_type, _o)]

    def femdom_tick(girl):
        """Once per action tick (sub_event_tick): her clock, and the end of her "don't cum yet". Returns
        "femdom_release" when he has held it long enough (the tick handles it like a sub-event)."""
        store._femdom_ticks += 1
        _edge = store._femdom_edge
        if _edge and _edge["gid"] == girl.gid and not _edge["released"]:
            _edge["ticks"] -= 1
            if _edge["ticks"] <= 0:
                _edge["released"] = True
                return "femdom_release"
        return None

    # ── He came: her standing orders are judged ──

    def femdom_note_cum(girl, scene_type, cum_type):
        """process_cum: did he keep her orders? The verdicts play after the cum (_post_cum_central)."""
        _v = []
        _edge = store._femdom_edge
        if _edge and _edge["gid"] == girl.gid:
            _v.append("edge_kept" if _edge["released"] else "edge_broken")
            store._femdom_edge = None
        _dem = store._femdom_cum_demand
        if _dem and _dem["gid"] == girl.gid:
            _v.append("demand_kept" if cum_type in FEMDOM_CUM_GROUPS[_dem["where"]] else "demand_broken")
            store._femdom_cum_demand = None
        _mf = store._femdom_me_first
        if _mf and _mf["gid"] == girl.gid:
            _v.append("me_first_kept" if store._session_girl_orgasms > _mf["orgasms"] else "me_first_broken")
            store._femdom_me_first = None
        if girl.has_trait("femdom") and store._femdom_ticks <= 3 and renpy.random.random() < femdom_profile(girl)["humiliate"]:
            _v.append("humiliate_fast")
        if _v:
            store._femdom_verdicts = store._femdom_verdicts + [(girl.gid, _x) for _x in _v]
            print("[FEMDOM] %s: he came (%s in %s), verdicts %s" % (girl.gid, cum_type, scene_type, _v))

    # What each verdict does: (line key, Love change, counts as a refusal of hers)
    FEMDOM_VERDICTS = {
        "edge_kept":       ("femdom_edge_kept", 5, False),
        "edge_broken":     ("femdom_edge_broken", 0, True),
        "demand_kept":     ("femdom_demand_kept", 5, False),
        "demand_broken":   ("femdom_demand_broken", 0, True),
        "me_first_kept":   ("femdom_me_first_kept", 5, False),
        "me_first_broken": ("femdom_me_first_broken", -8, True),
        "humiliate_fast":  ("femdom_humiliate_fast", 0, False),
    }

    def femdom_play_verdicts(girl, scene_type):
        """Her verdicts on the orders he just kept / broke (called by _post_cum_central)."""
        _mine = [_x for _g, _x in store._femdom_verdicts if _g == girl.gid]
        store._femdom_verdicts = [_p for _p in store._femdom_verdicts if _p[0] != girl.gid]
        for _x in _mine:
            _key, _love, _refused = FEMDOM_VERDICTS[_x]
            if _refused:
                femdom_request_refused(girl, _x)
            if _love:
                Change_Status(girl, "Love", _love)
            if girl.has_trait("femdom") or not _refused:
                set_scene_expression(girl, "angry" if _refused else "lusty")
                Say_Line(girl, scene_pick_line(_key, scene=scene_type, girl=girl))
                # her verdict IS the femdom showing ("humiliate_fast" can play with no earlier order this scene)
                if girl.has_trait("femdom"):
                    girl.discover("discovered_trait_femdom")
        if _mine:
            set_scene_expression(girl, "normal")

    # ── Forced cum (Cum.rpy PlayerCumMenu_Penetration_Raw) ──

    def femdom_force_type(girl, scene_type, consent):
        """"femdom" when a veteran on top won't let him pull out (she would take it inside anyway), else None."""
        if (trait_is_veteran(girl, "femdom") and scene_control(scene_type) == "her"
                and consent == "allowed" and not girl.has_trait("hate_cum")
                and renpy.random.random() < FEMDOM_FORCE_CUM_CHANCE * femdom_intensity(girl)):
            print("[FEMDOM] %s keeps him inside (%s)" % (girl.gid, scene_type))
            return "femdom"
        return None

# ============================================================
# He refused a request of hers: a femdom girl gets angry (face + line) and loses Obed.
# Returns _femdom_refused = True when that happened: the caller then skips its own refusal line and Obed gain.
# ============================================================
label _femdom_refused_react(girl, what, scene_type=None):
    $ store._femdom_refused = femdom_react_refused(girl, what, scene_type)
    return

# ============================================================
# HER ORDERS (sub-events "femdom_<order>", routed by SubEvent_Handle)
# ============================================================
label SubEvent_FemdomOrder(girl, scene_type, event_name):
    python:
        _fd_order = event_name[len("femdom_"):]
        store._femdom_orders_done[_fd_order] = store._femdom_orders_done.get(_fd_order, 0) + 1
        _fd_vet = trait_is_veteran(girl, "femdom")
        girl.discover("discovered_trait_femdom")
        print("[FEMDOM] %s orders: %s in %s (veteran=%s, orders this session=%s)" % (
            girl.gid, _fd_order, scene_type, _fd_vet, store._femdom_orders_done))
    $ set_scene_expression(girl, "lusty")
    call expression "_femdom_order_" + _fd_order pass (girl, scene_type, _fd_vet) from _call_femdom_order
    if not store._sub_event_position_switched:
        $ set_scene_expression(girl, "normal")
    return

# He stood up to her: the line of who won
label _femdom_defy_outcome(girl, scene_type, what):
    if femdom_defied(girl, scene_type, what):
        $ set_scene_expression(girl, "angry")
        $ Say_Line(girl, scene_pick_line("femdom_defied_won", scene=scene_type, girl=girl))
        $ store._femdom_defy_won = True
    else:
        $ Say_Line(girl, scene_pick_line("femdom_defied_lost", scene=scene_type, girl=girl))
        $ store._femdom_defy_won = False
    return

label _femdom_order_take_over(girl, scene_type, veteran):
    python:
        _fd_target = renpy.random.choice([_p for _p in ("cowgirl", "reverse_cowgirl") if girl_has_pose(girl, _p)])
        _fd_mode = femdom_order_mode(girl)
    # Below 700 Obed she does not ask (femdom_order_mode): she announces it and takes the ride, no menu
    if _fd_mode == "rules":
        $ Say_Line(girl, scene_pick_line("femdom_take_over", scene=scene_type, girl=girl))
        "She doesn't wait for an answer. She shoves you onto your back and climbs on."
        call _femdom_do_take_over(girl, scene_type, _fd_target) from _call_fd_take_over_rules
        return
    # From 800 she asks; from 900 she pleads, and his no stands (the refusal still counts on her turn)
    if _fd_mode in ("asks", "begs"):
        $ Say_Line(girl, scene_pick_line("femdom_take_over_beg" if _fd_mode == "begs" else "femdom_take_over_ask", scene=scene_type, girl=girl))
        if _fd_mode == "begs":
            $ unlock_achievement("beg_for_it")
        menu:
            "Let her ride you":
                $ Change_Status(girl, "Love", 5 if _fd_mode == "begs" else 3)
                if _fd_mode == "begs":
                    $ Say_Line(girl, scene_pick_line("femdom_beg_granted", scene=scene_type, girl=girl))
                call _femdom_do_take_over(girl, scene_type, _fd_target) from _call_fd_take_over_asked
            "Not now":
                $ femdom_request_refused(girl, "take_over")
                $ set_scene_expression(girl, "sad" if _fd_mode == "begs" else "angry")
                $ Say_Line(girl, scene_pick_line("femdom_beg_denied" if _fd_mode == "begs" else "femdom_ask_denied", scene=scene_type, girl=girl))
        return
    # 700-799: her order, with his say (the original menu)
    $ Say_Line(girl, scene_pick_line("femdom_take_over", scene=scene_type, girl=girl))
    menu:
        "Let her ride you":
            $ Change_Status(girl, "Love", 3)
            call _femdom_do_take_over(girl, scene_type, _fd_target) from _call_fd_take_over_obey
        "Stay in control":
            if veteran and not femdom_player_prevails(girl, scene_type):
                "She shoves you onto your back anyway."
                $ Say_Line(girl, scene_pick_line("femdom_forced", scene=scene_type, girl=girl))
                call _femdom_do_take_over(girl, scene_type, _fd_target) from _call_fd_take_over_forced
            else:
                call _femdom_refused_react(girl, "take_over", scene_type) from _call_fdr_take_over
        "Pin her down instead":
            call _femdom_defy_outcome(girl, scene_type, "take_over") from _call_fd_defy_take_over
            if not store._femdom_defy_won:
                "She twists free and shoves you onto your back."
                call _femdom_do_take_over(girl, scene_type, _fd_target) from _call_fd_take_over_defy_lost
    return

label _femdom_do_take_over(girl, scene_type, target):
    if store._condom_broken_hidden:
        call CondomBreakDiscovery(girl, scene_type) from _call_CondomBreakDisc_fd_take_over
    $ _fav = target
    $ print("[FEMDOM] %s takes over: %s -> %s" % (girl.gid, scene_type, target))
    call _se_execute_pos_switch(girl, scene_type) from _call_ps_fd_take_over
    return

label _femdom_order_challenge(girl, scene_type, veteran):
    $ Say_Line(girl, scene_pick_line("femdom_challenge", scene=scene_type, girl=girl))
    menu:
        "Show her":
            python:
                _fd_sv = _cum_cfg(scene_type, "speed_var")
                _fd_up = getattr(store, _fd_sv, 0) < _cum_cfg(scene_type, "max_speed", 3)
                if _fd_up:
                    _se_adjust_pace(scene_type, 1)
            if _fd_up:
                call _cum_dispatch_apply_speed(girl, scene_type) from _call_cas_fd_challenge
            $ Change_Status(girl, "Lust", 8, max_val=100)
            $ Change_Status(girl, "Love", 3)
            $ Say_Line(girl, scene_pick_line("femdom_challenge_met", scene=scene_type, girl=girl))
        "Ignore her":
            call _femdom_refused_react(girl, "challenge", scene_type) from _call_fdr_challenge
        "Tell her who's in charge":
            call _femdom_defy_outcome(girl, scene_type, "challenge") from _call_fd_defy_challenge
    return

label _femdom_order_pace_order(girl, scene_type, veteran):
    $ _fd_dir = femdom_pace_direction(girl, scene_type) or "faster"
    $ _fd_step = 1 if _fd_dir == "faster" else -1
    $ _fd_hers = scene_control(scene_type) == "her"
    $ _fd_mode = femdom_order_mode(girl)
    # Below 700 Obed she does not ask (femdom_order_mode): she calls the pace and sets it herself
    if _fd_mode == "rules":
        $ Say_Line(girl, scene_pick_line("femdom_pace_" + _fd_dir, scene=scene_type, girl=girl))
        "She doesn't leave it up to you. She sets the pace herself."
        $ _se_adjust_pace(scene_type, _fd_step)
        call _cum_dispatch_apply_speed(girl, scene_type) from _call_cas_fd_pace_rules
        return
    # From 800 she asks; from 900 she pleads, and his no stands (the refusal still counts on her turn)
    if _fd_mode in ("asks", "begs"):
        $ Say_Line(girl, scene_pick_line("femdom_pace_%s_%s" % (_fd_dir, "beg" if _fd_mode == "begs" else "ask"), scene=scene_type, girl=girl))
        if _fd_mode == "begs":
            $ unlock_achievement("beg_for_it")
        menu:
            "Do as she says":
                $ _se_adjust_pace(scene_type, _fd_step)
                call _cum_dispatch_apply_speed(girl, scene_type) from _call_cas_fd_pace_asked
                $ Change_Status(girl, "Love", 5 if _fd_mode == "begs" else 3)
                $ Say_Line(girl, scene_pick_line("femdom_beg_granted" if _fd_mode == "begs" else "femdom_obeyed", scene=scene_type, girl=girl))
            "Not now":
                $ femdom_request_refused(girl, "pace")
                $ set_scene_expression(girl, "sad" if _fd_mode == "begs" else "angry")
                $ Say_Line(girl, scene_pick_line("femdom_beg_denied" if _fd_mode == "begs" else "femdom_ask_denied", scene=scene_type, girl=girl))
        return
    # 700-799: her order, with his say (the original menu)
    $ Say_Line(girl, scene_pick_line("femdom_pace_" + _fd_dir, scene=scene_type, girl=girl))
    menu:
        "Do as she says":
            $ _se_adjust_pace(scene_type, _fd_step)
            call _cum_dispatch_apply_speed(girl, scene_type) from _call_cas_fd_pace_obey
            $ Change_Status(girl, "Love", 3)
            $ Say_Line(girl, scene_pick_line("femdom_obeyed", scene=scene_type, girl=girl))
        "Ignore her":
            call _femdom_refused_react(girl, "pace", scene_type) from _call_fdr_pace_order
            if veteran and _fd_hers:
                "She sets the pace herself anyway."
                $ _se_adjust_pace(scene_type, _fd_step)
                call _cum_dispatch_apply_speed(girl, scene_type) from _call_cas_fd_pace_forced
        "Tell her who's in charge":
            call _femdom_defy_outcome(girl, scene_type, "pace") from _call_fd_defy_pace
            if not store._femdom_defy_won and _fd_hers:
                "She sets the pace herself."
                $ _se_adjust_pace(scene_type, _fd_step)
                call _cum_dispatch_apply_speed(girl, scene_type) from _call_cas_fd_pace_defy_lost
    return

label _femdom_order_no_cum(girl, scene_type, veteran):
    $ Say_Line(girl, scene_pick_line("femdom_no_cum", scene=scene_type, girl=girl))
    menu:
        "Hold it for her":
            $ store._femdom_edge = {"gid": girl.gid, "ticks": FEMDOM_EDGE_TICKS, "released": False}
            $ Change_Status(girl, "Love", 2)
        "Ignore her":
            call _femdom_refused_react(girl, "no_cum", scene_type) from _call_fdr_no_cum
        "Tell her you'll cum when you want":
            call _femdom_defy_outcome(girl, scene_type, "no_cum") from _call_fd_defy_no_cum
            if not store._femdom_defy_won:
                $ store._femdom_edge = {"gid": girl.gid, "ticks": FEMDOM_EDGE_TICKS, "released": False}
    return

# He held it long enough (femdom_tick): she lets him
label _femdom_edge_release(girl, scene_type):
    $ set_scene_expression(girl, "lusty")
    $ Say_Line(girl, scene_pick_line("femdom_edge_release", scene=scene_type, girl=girl))
    $ set_scene_expression(girl, "normal")
    return

label _femdom_order_cum_demand(girl, scene_type, veteran):
    $ _fd_where = renpy.random.choice(femdom_cum_demand_options(girl, scene_type))
    $ Say_Line(girl, scene_pick_line("femdom_demand_" + _fd_where, scene=scene_type, girl=girl))
    menu:
        "Promise her":
            $ store._femdom_cum_demand = {"gid": girl.gid, "where": _fd_where}
            $ Change_Status(girl, "Love", 2)
        "Ignore her":
            call _femdom_refused_react(girl, "cum_demand", scene_type) from _call_fdr_cum_demand
        "Tell her you'll decide":
            call _femdom_defy_outcome(girl, scene_type, "cum_demand") from _call_fd_defy_cum_demand
            if not store._femdom_defy_won:
                $ store._femdom_cum_demand = {"gid": girl.gid, "where": _fd_where}
    return

label _femdom_order_me_first(girl, scene_type, veteran):
    $ Say_Line(girl, scene_pick_line("femdom_me_first", scene=scene_type, girl=girl))
    menu:
        "Make her cum first":
            $ store._femdom_me_first = {"gid": girl.gid, "orgasms": store._session_girl_orgasms}
            $ Change_Status(girl, "Lust", 15, max_val=100)
            $ Change_Status(girl, "Love", 2)
        "Ignore her":
            call _femdom_refused_react(girl, "me_first", scene_type) from _call_fdr_me_first
        "Tell her who's in charge":
            call _femdom_defy_outcome(girl, scene_type, "me_first") from _call_fd_defy_me_first
            if not store._femdom_defy_won:
                $ store._femdom_me_first = {"gid": girl.gid, "orgasms": store._session_girl_orgasms}
    return

# ============================================================
# He wants to go from HER position to HIS (each Core's "Switch position..." to doggy / full nelson):
# she may refuse. Sets _femdom_gate_ok; the switch only happens when it is True. The button never hides.
# ============================================================
label _femdom_position_gate(girl, from_pos, to_pos):
    $ store._femdom_gate_ok = True
    python:
        _fg_int = femdom_intensity(girl)
        _fg_refuse = (_fg_int > 0 and scene_control(from_pos) == "her" and scene_control(to_pos) == "him"
                      and renpy.random.random() < FEMDOM_POSITION_REFUSE * _fg_int)
    if not _fg_refuse:
        return
    $ print("[FEMDOM] %s refuses to leave %s for %s" % (girl.gid, from_pos, to_pos))
    $ girl.discover("discovered_trait_femdom")
    $ set_scene_expression(girl, "lusty")
    $ Say_Line(girl, scene_pick_line("femdom_pos_refuse", scene=from_pos, girl=girl))
    menu:
        "Insist":
            call _femdom_defy_outcome(girl, from_pos, "position") from _call_fd_defy_position
            if not store._femdom_defy_won:
                "She doesn't move an inch."
                $ store._femdom_gate_ok = False
        "Let her stay on top":
            $ Change_Status(girl, "Love", 2)
            $ store._femdom_gate_ok = False
    $ set_scene_expression(girl, "normal")
    return

default _femdom_defy_won = False

# ============================================================
# SUBMISSIVE MIRROR (docs/plan_sugar_mommy.md, camada 2): she asks HIM to direct her.
# Same mold as her femdom orders: candidates join sub_event_dispatch (SubEvents.rpy), the router sends any
# "subm_" name to SubEvent_SubmAsk below, caps per scene, reset with the session. For ANY submissive girl,
# born or broken (CANON_BREAK_RULES); while she is discovering the trait her lines come out unsure
# (trait_is_discovering, domain "subm") and every completed ask counts subm_note_obeyed.
# ============================================================

default _subm_asks_done = 0         # per scene (reset: femdom_session_reset / sub_event_reset)

init python:

    SUBM_ASK_CHANCE = 0.35          # the roll that lets her asks join a dispatch
    SUBM_ASK_TOTAL = 2              # at most this many of her asks per scene
    _SUBM_POSITION_TARGETS = ("doggy", "laying_down")   # "his" positions she can offer (POSITION_CONTROL side)

    def _subm_position_target(girl, scene_type):
        """The position she could offer to switch to, or None: a 'his' position she has art for, from a vaginal
        penetration scene that is not already it."""
        if scene_type not in ("cowgirl", "reverse_cowgirl", "doggy", "laying_down"):
            return None
        for _p in _SUBM_POSITION_TARGETS:
            if _p != scene_type and girl_has_pose(girl, _p):
                return _p
        return None

    def subm_candidates(girl, scene_type):
        """Her asks for this dispatch roll: submissive only, capped per scene, one chance roll for the batch."""
        if not (hasattr(girl, "has_trait") and girl.has_trait("submissive")):
            return []
        if store._subm_asks_done >= SUBM_ASK_TOTAL or renpy.random.random() > SUBM_ASK_CHANCE:
            return []
        # his hands on the back of her head (bj_forcing): she cannot pull off to ask anything (tester 2026-10-11)
        if scene_type == "bj" and getattr(store, "bj_forcing", False):
            return []
        _out = [("subm_cum_where", 12)]
        # the pace ask needs a pace: tip mode has one speed (the same guard as _se_can_pace_request), and her
        # "Slower" there froze the FN tip at speed 0 with no speed item to recover (tester 2026-10-11)
        _tv = _cum_cfg(scene_type, "tip_mode_var")
        if not (_tv and getattr(store, _tv, False)):
            _out.insert(0, ("subm_orders", 18))
        if _subm_position_target(girl, scene_type):
            _out.append(("subm_position", 15))
        return _out

# Router target for every "subm_" sub-event (SubEvent_Handle, SubEvents.rpy)
label SubEvent_SubmAsk(girl, scene_type, event_name):
    $ store._subm_asks_done += 1
    $ _subm_new = trait_is_discovering(girl, "submissive")
    # her ASK is the submissive voice (mirrors SubEvent_FemdomOrder's discover before the order)
    if girl.has_trait("submissive"):
        $ girl.discover("discovered_trait_submissive")
    $ print("[SUBM] %s asks: %s (scene %s, %d/%d, discovering=%s)" % (girl.gid, event_name, scene_type, store._subm_asks_done, SUBM_ASK_TOTAL, _subm_new))
    call expression ("_" + event_name) pass (girl, scene_type, _subm_new) from _call_subm_ask
    return

label _subm_orders(girl, scene_type, newly):
    $ set_scene_expression(girl, "shy" if newly else "sexy")
    if newly:
        $ Say_Line(girl, renpy.random.choice([
            _("Tell me how you want me. I... I'm still learning to ask that."),
            _("Set the pace. Please. It's easier when you decide."),
        ]))
    else:
        $ Say_Line(girl, renpy.random.choice([
            _("However you want me. Just say it."),
            _("Give me the pace. I'll keep it."),
        ]))
    menu:
        "Faster":
            $ _se_adjust_pace(scene_type, 1)
            call _cum_dispatch_apply_speed(girl, scene_type) from _call_cas_subm_fast
            $ Say_Line(girl, _("Yes... like this."))
            $ Change_Status(girl, "Obed", 4)
            $ subm_note_obeyed(girl)
        "Slower":
            $ _se_adjust_pace(scene_type, -1)
            call _cum_dispatch_apply_speed(girl, scene_type) from _call_cas_subm_slow
            $ Say_Line(girl, _("Slow... okay. I can do slow."))
            $ Change_Status(girl, "Obed", 4)
            $ subm_note_obeyed(girl)
        "Keep going like this":
            $ Say_Line(girl, _("Like this, then. Tell me if that changes."))
            $ Change_Status(girl, "Obed", 2)
            $ subm_note_obeyed(girl)
    return

label _subm_position(girl, scene_type, newly):
    $ _subm_target = _subm_position_target(girl, scene_type)
    $ set_scene_expression(girl, "shy" if newly else "sexy")
    if newly:
        $ Say_Line(girl, _("We could... switch. To how YOU like it. If you want."))
    else:
        $ Say_Line(girl, _("Put me how you like me best. Go on."))
    menu:
        "Switch":
            if store._condom_broken_hidden:
                call CondomBreakDiscovery(girl, scene_type) from _call_CondomBreakDisc_subm
            $ Change_Status(girl, "Obed", 4)
            $ subm_note_obeyed(girl)
            $ _fav = _subm_target
            call _se_execute_pos_switch(girl, scene_type) from _call_ps_subm
        "Stay like this":
            $ Say_Line(girl, _("Then I'm not moving. Your call."))
            $ Change_Status(girl, "Love", 2)
    return

label _subm_cum_where(girl, scene_type, newly):
    $ set_scene_expression(girl, "shy" if newly else "lusty")
    if newly:
        $ Say_Line(girl, _("When it's time... where do you want to finish? I'd rather know. And accept it."))
    else:
        $ Say_Line(girl, _("Where am I taking it this time? Your choice. It always is."))
    menu:
        "Where I decide, when I decide":
            $ set_scene_expression(girl, "shy")
            $ Say_Line(girl, _("...Understood. I'll be ready."))
            $ Change_Status(girl, "Obed", 4)
            $ subm_note_obeyed(girl)
        "You'll find out":
            $ set_scene_expression(girl, "lipbite")
            $ Say_Line(girl, _("That answer shouldn't work on me. It does."))
            $ Change_Status(girl, "Inbt", 3)
            $ subm_note_obeyed(girl)
    return
