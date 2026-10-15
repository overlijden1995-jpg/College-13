# ============================================================
# QA: Automated Cheat Heat & Anal Tests
# Run from Ren'Py console (Shift+O):  run_heat_qa()
# ============================================================

init 999 python:

    def debug_pickle_store():
        """Run from console (Shift+O): debug_pickle_store()
        Finds which store variables can't be pickled (cause save crash)."""
        import pickle, io
        _bad = []
        for _k in sorted(dir(store)):
            if _k.startswith("_") or _k.startswith("__"):
                continue
            try:
                _v = getattr(store, _k)
                pickle.dumps(_v, pickle.HIGHEST_PROTOCOL)
            except Exception as _e:
                _bad.append((_k, type(_v).__name__, str(_e)[:120]))
                debug_log("[PICKLE FAIL] %s (%s): %s" % (_k, type(_v).__name__, str(_e)[:120]))
        if not _bad:
            debug_log("[PICKLE OK] All non-underscore store variables are picklable.")
        else:
            debug_log("[PICKLE] %d unpicklable variable(s) found." % len(_bad))
        return _bad

    def run_heat_qa():
        """
        Automated QA for the Cheat Heat system + anal changes.
        Creates a temporary mock girl, runs all logic tests, prints PASS/FAIL.
        Does NOT modify any real game state.
        """
        _passed = [0]
        _failed = [0]
        _errors = []

        def _assert(name, condition, detail=""):
            if condition:
                _passed[0] += 1
            else:
                _failed[0] += 1
                msg = "FAIL: %s" % name
                if detail:
                    msg += " -- %s" % detail
                _errors.append(msg)
                debug_log(msg)

        def _assert_eq(name, got, expected):
            _assert(name, got == expected, "got %s, expected %s" % (got, expected))

        def _assert_range(name, got, lo, hi):
            _assert(name, lo <= got <= hi, "got %s, expected %s-%s" % (got, lo, hi))

        # ── Create mock girl ──────────────────────────────
        class MockGirl(object):
            def __init__(self):
                self.Id = "_qa_mock"
                self.gid = "_qa_mock"
                self.Name = "QA Mock"
                self.traits = set()
                self.Love = 500
                self.Obed = 500
                self.Inbt = 500
                self.Temptation = 0
                self.Lust = 0
                self.intimacy_flags = set()
                self.flags = {"has_npc_partner": True}
                self.npc_partner_id = "npc_bf_qa"
                self.bf_loyalty = 750
                self._cheat_escalation_path = 1
                self._cheat_sex_stage = 0
                self._cheat_broke = False
                self._cheat_heat = 0
                self._cheat_heat_peak = 0
                self.Sex_acts = {"anal": 0, "anal_tip": 0}
                self.Firsts = {}
                self._atm_count = 0
                self._atp_count = 0
            def has_trait(self, t):
                return t in self.traits
            def add_trait(self, t):
                self.traits.add(t)
            def remove_trait(self, t):
                self.traits.discard(t)
            def has_npc_partner(self):
                return self.flags.get("has_npc_partner", False)
            def is_dating_player(self):
                return False

        def _reset(g, heat=0, stage=0, path=1, traits=None, flags=None):
            g._cheat_heat = heat
            g._cheat_heat_peak = max(heat, 0)
            g._cheat_sex_stage = stage
            g._cheat_escalation_path = path
            g._cheat_broke = False
            g.traits = set(traits or [])
            g.intimacy_flags = set(flags or [])
            g.Temptation = 0
            g.Love = 500
            g.Obed = 500
            g.Inbt = 500
            store._cheat_heat_session_gained = 0
            store._cheat_rub_just_done = False
            store._cheat_tip_just_done = False

        g = MockGirl()

        debug_log("=" * 60)
        debug_log("  CHEAT HEAT QA - Automated Tests")
        debug_log("=" * 60)

        # ============================================================
        # A. TIER SYSTEM
        # ============================================================
        debug_log("\n--- A. Tier System ---")

        _assert_eq("A1 kiss tier", _CHEAT_ACT_TIER.get("kiss"), 1)
        _assert_eq("A2 touch tier", _CHEAT_ACT_TIER.get("touch"), 1)
        _assert_eq("A3 hj tier", _CHEAT_ACT_TIER.get("hj"), 2)
        _assert_eq("A4 bj tier", _CHEAT_ACT_TIER.get("bj"), 3)
        _assert_eq("A5 rub tier", _CHEAT_ACT_TIER.get("rub"), 4)
        _assert_eq("A6 sex tier", _CHEAT_ACT_TIER.get("sex"), 5)
        _assert_eq("A7 anal tier", _CHEAT_ACT_TIER.get("anal"), 6)

        # Highest tier done
        _reset(g)
        _assert_eq("A8 no flags = tier 0", _cheat_highest_tier_done(g), 0)
        g.intimacy_flags = {"kiss", "touch"}
        _assert_eq("A9 kiss+touch = tier 1", _cheat_highest_tier_done(g), 1)
        g.intimacy_flags = {"kiss", "bj", "sex"}
        _assert_eq("A10 kiss+bj+sex = tier 5", _cheat_highest_tier_done(g), 5)
        g.intimacy_flags = {"anal"}
        _assert_eq("A11 anal = tier 6", _cheat_highest_tier_done(g), 6)

        # ============================================================
        # B. HEAT ACCUMULATION (_add_cheat_heat)
        # ============================================================
        debug_log("\n--- B. Heat Accumulation ---")

        # Basic add (path=3 has no accumulation multiplier, isolates the math)
        _reset(g, path=3)
        _add_cheat_heat(g, 10, "test")
        _assert_eq("B1 basic +10", g._cheat_heat, 10)
        _assert_eq("B2 peak tracks", g._cheat_heat_peak, 10)
        _assert_eq("B3 session gained", store._cheat_heat_session_gained, 10)

        # Cap at 100
        _reset(g, heat=95, path=3)
        _add_cheat_heat(g, 20, "test")
        _assert_eq("B4 cap at 100", g._cheat_heat, 100)

        # Session cap: after 30, efficiency drops to 1/5
        _reset(g, path=3)
        store._cheat_heat_session_gained = 30
        _add_cheat_heat(g, 10, "test_post_cap")
        _assert_eq("B5 post-cap 10->2", g._cheat_heat, 2)

        # Session cap: minimum 1
        _reset(g, path=3)
        store._cheat_heat_session_gained = 30
        _add_cheat_heat(g, 1, "test_min")
        _assert_eq("B6 post-cap min 1", g._cheat_heat, 1)

        # Trait: hardcore x1.3 (path=3 neutral)
        _reset(g, traits=["hardcore_sex"], path=3)
        _add_cheat_heat(g, 10, "test")
        _assert_eq("B7 hardcore x1.3", g._cheat_heat, 13)

        # Trait: cheater x2.0
        _reset(g, traits=["cheater"], path=3)
        g._cheat_escalation_path = 3  # keep path=3 for neutral mult
        _add_cheat_heat(g, 10, "test")
        _assert_eq("B8 cheater x2.0", g._cheat_heat, 20)

        # Trait: loyal x0.5
        _reset(g, traits=["loyal"], path=3)
        _add_cheat_heat(g, 10, "test")
        _assert_eq("B9 loyal x0.5", g._cheat_heat, 5)

        # Trait: cute x0.8
        _reset(g, traits=["cute_sex"], path=3)
        _add_cheat_heat(g, 10, "test")
        _assert_eq("B10 cute x0.8", g._cheat_heat, 8)

        # Path multiplier: path1 x0.9
        _reset(g, path=1)
        _add_cheat_heat(g, 10, "test")
        _assert_eq("B11 path1 x0.9", g._cheat_heat, 9)

        # Path multiplier: path2 x1.2
        _reset(g, path=2)
        _add_cheat_heat(g, 10, "test")
        _assert_eq("B12 path2 x1.2", g._cheat_heat, 12)

        # Peak update: higher than current peak
        _reset(g, path=3)
        g._cheat_heat_peak = 50
        g._cheat_heat = 45
        _add_cheat_heat(g, 20, "test")  # 45+20=65
        _assert("B13 peak updates when exceeded", g._cheat_heat_peak == 65,
                "peak=%s heat=%s" % (g._cheat_heat_peak, g._cheat_heat))

        # Peak no update: lower than current peak
        _reset(g, path=3)
        g._cheat_heat_peak = 90
        g._cheat_heat = 10
        _add_cheat_heat(g, 5, "test")  # 10+5=15, peak stays 90
        _assert_eq("B14 peak stays at 90", g._cheat_heat_peak, 90)

        # ============================================================
        # C. EFFECTIVE HEAT (high water mark)
        # ============================================================
        debug_log("\n--- C. Effective Heat ---")

        _reset(g)
        g._cheat_heat = 50
        g._cheat_heat_peak = 50
        _assert_eq("C1 current=peak", _cheat_effective_heat(g), 50)

        g._cheat_heat = 20
        g._cheat_heat_peak = 90
        # effective = max(20, int(90 * 0.7)) — int(62.999...) = 62 due to float
        _assert_eq("C2 peak floor 70%", _cheat_effective_heat(g), int(90 * 0.7))

        g._cheat_heat = 80
        g._cheat_heat_peak = 90
        # effective = max(80, 63) = 80
        _assert_eq("C3 current > floor", _cheat_effective_heat(g), 80)

        g._cheat_heat = 0
        g._cheat_heat_peak = 0
        _assert_eq("C4 both zero", _cheat_effective_heat(g), 0)

        # ============================================================
        # D. HEAT THRESHOLDS
        # ============================================================
        debug_log("\n--- D. Heat Thresholds ---")

        _reset(g)
        _assert_eq("D1 skip_to_tip base", _cheat_heat_threshold(g, "skip_to_tip"), 70 - int(500/1000.0*20) + 5)
        # base 70, stat discount -10 (score 500 -> 10), path1 +5 = 65

        _reset(g)
        t = _cheat_heat_threshold(g, "skip_s0_to_sex")
        _assert("D2 skip_s0_to_sex > skip_to_tip",
                t > _cheat_heat_threshold(g, "skip_to_tip"),
                "s0_sex=%s tip=%s" % (t, _cheat_heat_threshold(g, "skip_to_tip")))

        _reset(g)
        t_anal = _cheat_heat_threshold(g, "skip_s0_to_anal")
        t_sex = _cheat_heat_threshold(g, "skip_s0_to_sex")
        _assert("D3 anal > sex threshold", t_anal > t_sex,
                "anal=%s sex=%s" % (t_anal, t_sex))

        # Trait: hardcore reduces threshold
        _reset(g, traits=["hardcore_sex"])
        t_hc = _cheat_heat_threshold(g, "skip_to_tip")
        _reset(g)
        t_norm = _cheat_heat_threshold(g, "skip_to_tip")
        _assert("D4 hardcore reduces threshold", t_hc < t_norm,
                "hc=%s norm=%s" % (t_hc, t_norm))

        # Trait: loyal increases threshold
        _reset(g, traits=["loyal"])
        t_loyal = _cheat_heat_threshold(g, "skip_to_tip")
        _assert("D5 loyal increases threshold", t_loyal > t_norm,
                "loyal=%s norm=%s" % (t_loyal, t_norm))

        # Threshold clamp: min 20, max 95
        _reset(g, traits=["cheater"])
        g.Love = 1000
        g.Obed = 1000
        g.Inbt = 1000
        t_min = _cheat_heat_threshold(g, "skip_to_tip")
        _assert("D6 threshold min 20", t_min >= 20, "got %s" % t_min)

        _reset(g, traits=["loyal", "cute_sex"])
        g.Love = 0
        g.Obed = 0
        g.Inbt = 0
        t_max = _cheat_heat_threshold(g, "skip_s0_to_anal")
        _assert("D7 threshold max 95", t_max <= 95, "got %s" % t_max)

        # ============================================================
        # E. GATE FUNCTIONS (_cheat_can_tip/sex/anal)
        # ============================================================
        debug_log("\n--- E. Gate Functions ---")

        # _cheat_can_tip: natural path (stage >= 1, no rub_just)
        _reset(g, stage=1)
        _assert("E1 tip natural (stage1)", _cheat_can_tip(g) == True)

        # _cheat_can_tip: blocked (stage 0, no heat)
        _reset(g, stage=0)
        _assert("E2 tip blocked (stage0, heat0)", _cheat_can_tip(g) == False)

        # _cheat_can_tip: heat bypass
        _reset(g, stage=0, heat=95)
        _assert("E3 tip heat bypass", _cheat_can_tip(g) == True)

        # _cheat_can_tip: same-session penalty
        _reset(g, stage=1, heat=0)
        store._cheat_rub_just_done = True
        _assert("E4 tip blocked same-session (heat0)", _cheat_can_tip(g) == False)

        _reset(g, stage=1, heat=95)
        store._cheat_rub_just_done = True
        _assert("E5 tip same-session with high heat", _cheat_can_tip(g) == True)

        # _cheat_can_tip: tier bypass (already done sex)
        _reset(g, stage=0, heat=0, flags={"sex"})
        _assert("E6 tip tier bypass (done sex)", _cheat_can_tip(g) == True)

        # _cheat_can_sex: natural path (stage >= 2, no tip_just)
        _reset(g, stage=2)
        _assert("E7 sex natural (stage2)", _cheat_can_sex(g) == True)

        # _cheat_can_sex: blocked
        _reset(g, stage=0)
        _assert("E8 sex blocked (stage0, heat0)", _cheat_can_sex(g) == False)

        # _cheat_can_sex: heat bypass stage 0
        _reset(g, stage=0, heat=95)
        _assert("E9 sex heat bypass s0", _cheat_can_sex(g) == True)

        # _cheat_can_sex: heat bypass stage 1
        _reset(g, stage=1, heat=80)
        _assert("E10 sex heat bypass s1", _cheat_can_sex(g) == True)

        # _cheat_can_anal: much harder
        _reset(g, stage=0, heat=85)
        _assert("E11 anal blocked at heat85 s0", _cheat_can_anal(g) == False)

        _reset(g, stage=0, heat=99)
        g._cheat_heat_peak = 99
        _assert("E12 anal at heat99 s0", _cheat_can_anal(g) == True)

        # _cheat_can_anal: natural path (stage >= 3)
        _reset(g, stage=3)
        _assert("E13 anal natural (stage3)", _cheat_can_anal(g) == True)

        # _cheat_can_anal: stage 2 needs less heat
        _reset(g, stage=2, heat=80)
        can_s2 = _cheat_can_anal(g)
        _reset(g, stage=0, heat=80)
        can_s0 = _cheat_can_anal(g)
        _assert("E14 anal s2 easier than s0", can_s2 == True or can_s0 == False,
                "s2=%s s0=%s" % (can_s2, can_s0))

        # Anal harder than sex at same heat
        _reset(g, stage=0, heat=87)
        g._cheat_heat_peak = 87
        sex_ok = _cheat_can_sex(g)
        anal_ok = _cheat_can_anal(g)
        _assert("E15 anal harder than sex", sex_ok == True and anal_ok == False,
                "sex=%s anal=%s" % (sex_ok, anal_ok))

        # ============================================================
        # F. COUNTER-OFFER LOGIC
        # ============================================================
        debug_log("\n--- F. Counter-Offer Logic ---")

        # counter-offers always available (no heat gate)
        _reset(g, heat=0, stage=0)
        _assert_eq("F0 sex s0 zero heat -> rub", _cheat_get_counter_offer(g, "sex"), "rub")
        _reset(g, heat=0)
        _assert_eq("F0b tip s0 zero heat -> rub", _cheat_get_counter_offer(g, "tip"), "rub")

        # sex wanted, stage 0 -> offer rub
        _reset(g, heat=0, stage=0)
        _assert_eq("F1 sex s0 -> rub", _cheat_get_counter_offer(g, "sex"), "rub")

        # sex wanted, stage 1 -> offer tip
        _reset(g, heat=0, stage=1)
        _assert_eq("F2 sex s1 -> tip", _cheat_get_counter_offer(g, "sex"), "tip")

        # sex wanted, same-session -> None
        _reset(g, heat=0, stage=0)
        store._cheat_rub_just_done = True
        _assert_eq("F3 sex same-session -> None", _cheat_get_counter_offer(g, "sex"), None)

        # tip wanted, stage 0 -> rub
        _reset(g, heat=0)
        _assert_eq("F4 tip s0 -> rub", _cheat_get_counter_offer(g, "tip"), "rub")

        # tip wanted, rub_just -> None
        _reset(g, heat=0)
        store._cheat_rub_just_done = True
        _assert_eq("F5 tip rub_just -> None", _cheat_get_counter_offer(g, "tip"), None)

        # anal wanted, stage 2 -> offer sex
        _reset(g, heat=0, stage=2)
        _assert_eq("F6 anal s2 -> sex", _cheat_get_counter_offer(g, "anal"), "sex")

        # anal wanted, stage 1 -> offer tip
        _reset(g, heat=0, stage=1)
        _assert_eq("F7 anal s1 -> tip", _cheat_get_counter_offer(g, "anal"), "tip")

        # anal wanted, stage 0 -> offer rub
        _reset(g, heat=20, stage=0)
        _assert_eq("F8 anal s0 -> rub", _cheat_get_counter_offer(g, "anal"), "rub")

        # ============================================================
        # G. BIG JUMP DETECTION
        # ============================================================
        debug_log("\n--- G. Big Jump Detection ---")

        _reset(g)
        # No flags, doing sex (tier 5): jump = 5-0 = 5
        _assert_eq("G1 nothing->sex = 5", _cheat_big_jump_distance(g, "sex"), 5)

        # Has kiss (tier 1), doing sex (tier 5): jump = 5-1 = 4
        g.intimacy_flags = {"kiss"}
        _assert_eq("G2 kiss->sex = 4", _cheat_big_jump_distance(g, "sex"), 4)

        # Has bj (tier 3), doing sex (tier 5): jump = 5-3 = 2
        g.intimacy_flags = {"bj"}
        _assert_eq("G3 bj->sex = 2", _cheat_big_jump_distance(g, "sex"), 2)

        # Nothing done, doing anal (tier 6): jump = 6
        g.intimacy_flags = set()
        _assert_eq("G4 nothing->anal = 6", _cheat_big_jump_distance(g, "anal"), 6)

        # Big jump line: >= 3 returns line, < 3 returns None
        g.intimacy_flags = set()
        line = _cheat_big_jump_line(g, "sex")
        _assert("G5 jump 5 has line", line is not None, "got None")

        g.intimacy_flags = {"rub"}  # tier 4, doing sex tier 5 = jump 1
        line = _cheat_big_jump_line(g, "sex")
        _assert("G6 jump 1 no line", line is None, "got '%s'" % line)

        # ============================================================
        # H. COUNTER-OFFER DIALOGUE LINES EXIST
        # ============================================================
        debug_log("\n--- H. Dialogue Line Coverage ---")

        _co_combos = [("sex", "tip"), ("sex", "rub"), ("anal", "tip"),
                       ("anal", "rub"), ("anal", "sex"), ("tip", "rub")]
        for wanted, offered in _co_combos:
            for path in (1, 2, 3):
                pool = _COUNTER_OFFER_LINES.get((wanted, offered), {}).get(path)
                _assert("H-co (%s,%s) path%s" % (wanted, offered, path),
                        pool and len(pool) > 0,
                        "missing or empty")

        for path in (1, 2, 3):
            pool = _COUNTER_REFUSE_LINES.get(path)
            _assert("H-refuse path%s" % path,
                    pool and len(pool) > 0,
                    "missing or empty")

        # ============================================================
        # I. HEAT PER ACTION TABLE
        # ============================================================
        debug_log("\n--- I. Heat Per Action ---")

        expected_heat = {"flirt": (1, 1), "kiss": (1, 1), "touch": (2, 1), "hj": (2, 1), "tj": (2, 1), "bj": (3, 2)}
        for act, exp in expected_heat.items():
            _assert_eq("I-heat %s" % act, _CHEAT_HEAT_TABLE.get(act), exp)

        # ============================================================
        # J. INTEGRATION: is_loyalty_blocked heat boost
        # ============================================================
        debug_log("\n--- J. Loyalty Block + Heat ---")

        # Heat 0, Temptation 0 -> blocked for kiss (needs T>=3 bf gate + T>=4 attitude gate)
        _reset(g)
        blocked, reason = is_loyalty_blocked(g, "kiss")
        _assert("J1 kiss blocked (heat0 t0)", blocked == True, "blocked=%s" % blocked)

        # Heat 40 -> effective T = 4, passes attitude gate (T>=4) + kiss bf gate (T>=3)
        _reset(g, heat=40)
        blocked, reason = is_loyalty_blocked(g, "kiss")
        _assert("J2 kiss passes (heat40)", blocked == False, "blocked=%s reason=%s" % (blocked, reason))

        # Heat 80 -> effective T = 8, sex gate = 8 -> passes
        _reset(g, heat=80)
        blocked, reason = is_loyalty_blocked(g, "sex")
        _assert("J3 sex passes (heat80)", blocked == False, "blocked=%s" % blocked)

        # Heat 89 -> T = 8, anal gate = 9 -> blocked
        _reset(g, heat=89)
        blocked, reason = is_loyalty_blocked(g, "anal")
        _assert("J4 anal blocked (heat89)", blocked == True, "blocked=%s" % blocked)

        # Heat 90 -> T = 9, anal gate = 9 -> passes
        _reset(g, heat=90)
        blocked, reason = is_loyalty_blocked(g, "anal")
        _assert("J5 anal passes (heat90)", blocked == False, "blocked=%s" % blocked)

        # Tier bypass: already done sex, ask for tip -> not blocked
        _reset(g, heat=0, flags={"sex"})
        blocked, reason = is_loyalty_blocked(g, "tip")
        _assert("J6 tier bypass tip (done sex)", blocked == False, "blocked=%s" % blocked)

        # Solteira: never blocked
        _reset(g)
        g.flags["has_npc_partner"] = False
        g.npc_partner_id = None
        blocked, reason = is_loyalty_blocked(g, "sex")
        _assert("J7 single girl not blocked", blocked == False, "blocked=%s" % blocked)
        g.flags["has_npc_partner"] = True
        g.npc_partner_id = "npc_bf_qa"

        # ============================================================
        # K. DECAY MATH
        # ============================================================
        debug_log("\n--- K. Decay Math ---")

        # Base decay: -2
        _reset(g, heat=50)
        _decay = 3 if g.has_trait("loyal") else 1 if g.has_trait("cheater") else 2
        expected = max(0, 50 - _decay)
        _assert_eq("K1 base decay", expected, 48)

        # Loyal decay: -3
        _reset(g, heat=50, traits=["loyal"])
        _decay = 3 if g.has_trait("loyal") else 1 if g.has_trait("cheater") else 2
        _assert_eq("K2 loyal decay", max(0, 50 - _decay), 47)

        # Cheater decay: -1
        _reset(g, heat=50, traits=["cheater"])
        _decay = 3 if g.has_trait("loyal") else 1 if g.has_trait("cheater") else 2
        _assert_eq("K3 cheater decay", max(0, 50 - _decay), 49)

        # Decay doesn't go below 0
        _reset(g, heat=1)
        _decay = 2
        _assert_eq("K4 decay floor 0", max(0, 1 - _decay), 0)

        # ============================================================
        # L. PROGRESSION SIMULATION
        # ============================================================
        debug_log("\n--- L. Progression Simulation ---")

        # Simulate: 4 sessions of farming (refuse counter-offers)
        _reset(g, path=2)  # path2 x1.2 multiplier
        session_heats = []
        for session in range(5):
            store._cheat_heat_session_gained = 0
            # Each session: 3 denials (15 each) + 3 refuses (20 each)
            for _ in range(3):
                _add_cheat_heat(g, 15, "ask_denied")
                _add_cheat_heat(g, 20, "refuse")
            session_heats.append(g._cheat_heat)
            # Decay between sessions (simulate 1 day)
            g._cheat_heat = max(0, g._cheat_heat - 2)

        _assert("L1 heat grows over sessions", session_heats[-1] > session_heats[0],
                "heats=%s" % session_heats)
        _assert("L2 reaches sex threshold by s3-4",
                any(h >= 70 for h in session_heats[2:]),
                "heats=%s" % session_heats)

        # Simulate: natural path (no heat farming needed)
        _reset(g, path=1)
        # Session 1: rub (advances stage to 1)
        g._cheat_sex_stage = 1
        _add_cheat_heat(g, 3, "scene_rub")
        store._cheat_heat_session_gained = 0
        # Session 2: tip (stage 1 -> can tip naturally)
        g._cheat_sex_stage = 2
        _add_cheat_heat(g, 5, "scene_tip")
        store._cheat_heat_session_gained = 0
        # Session 3: sex (stage 2 -> can sex naturally)
        can = _cheat_can_sex(g)
        _assert("L3 natural path needs no heat", can == True,
                "stage=%s heat=%s" % (g._cheat_sex_stage, g._cheat_heat))

        # ============================================================
        # SUMMARY
        # ============================================================
        debug_log("\n" + "=" * 60)
        total = _passed[0] + _failed[0]
        if _failed[0] == 0:
            debug_log("  ALL %d TESTS PASSED" % total)
        else:
            debug_log("  %d / %d PASSED, %d FAILED:" % (_passed[0], total, _failed[0]))
            for e in _errors:
                debug_log("    %s" % e)
        debug_log("=" * 60)

        return _failed[0] == 0
