## pregnancy.rpy — Fertility Cycle, Pill Mechanics & Pregnancy Engine
## Phase 2: cycle engine, pill effectiveness, daily tick
## Phase 3+: probability engine, cum hooks (added later)

init 1 python:
    def _impreg_render(st, at):
        idx = int(st / 0.042)
        if idx >= 72:
            if st >= 72 * 0.042 + 3.0:
                return Null(), None
            return Image("images/helpers/Preg/frames/impreg_3_23.png"), 0.042
        g = idx // 24 + 1
        f = idx % 24
        return Image("images/helpers/Preg/frames/impreg_%d_%02d.png" % (g, f)), 0.042

    renpy.image("impregnation_anim", DynamicDisplayable(_impreg_render))

init python:

    # ============================================================
    # CYCLE ENGINE
    # ============================================================

    # Phase → base conception chance (used by Phase 3)
    _CYCLE_CHANCE = {
        "safe":     0.03,
        "low_risk": 0.10,
        "fertile":  0.25,
        "peak":     0.40,
    }

    def get_cycle_day(girl):
        """Current day in the girl's 28-day cycle (1-28)."""
        return ((store.Day + girl._cycle_offset) % 28) + 1

    def _cycle_phase_for_day(d, breedable=False):
        """Phase string for cycle day d (1-28). Single source of truth for the
        roll, the dialogue and the phone Fertility app.
        breedable: expanded fertile window, days 10-20 count as at least fertile."""
        if 14 <= d <= 16:
            return "peak"
        if 12 <= d <= 18:
            return "fertile"
        if breedable and 10 <= d <= 20:
            return "fertile"
        if 9 <= d <= 11 or 19 <= d <= 21:
            return "low_risk"
        return "safe"

    def get_cycle_phase(girl):
        """Return phase string for the girl's current cycle day."""
        return _cycle_phase_for_day(get_cycle_day(girl))

    def get_cycle_base_chance(girl):
        """Base conception chance for the girl's current cycle phase."""
        return _CYCLE_CHANCE[get_cycle_phase(girl)]

    # ============================================================
    # PILL EFFECTIVENESS
    # ============================================================

    _PILL_MISS_MULTIPLIER = {
        0: 0.05,
        1: 0.20,
        2: 0.40,
    }

    def get_pill_effectiveness(girl):
        """Return pill multiplier (0.05 = 95% effective, 1.0 = no protection).
        Only meaningful when girl._on_pill is True."""
        if not girl._on_pill:
            return 1.0
        if girl._on_placebo:
            return 1.0
        missed = getattr(girl, "_pill_missed", 0)
        return _PILL_MISS_MULTIPLIER.get(missed, 1.0)

    # ============================================================
    # PILL SELF-START CHECK
    # ============================================================

    def _pill_self_start_check(girl):
        """Daily roll: girl autonomously decides to start taking the pill.
        Only called when not on pill, not pregnant, pregnancy mode != off,
        and girl has had sex (first_sex in player_firsts)."""
        if girl._on_pill or girl._pregnant:
            return False
        if getattr(girl, "_pill_stopped_for_him", False):
            # She agreed to stop FOR HIM (the pill_stop ask): she never quietly restarts on her own
            # (tester 2026-10-11: she kept going back on the pill after the first pregnancy, however
            # many times he asked or swapped placebos). Handing her a new pack is still his call.
            return False
        if store._pregnancy_mode == "off":
            return False
        # player_firsts means "he was her FIRST", and never had a "first_sex" key: this gate was
        # always False and no girl ever started the pill on her own. The act counter is the truth.
        if not girl_had_sex(girl):
            return False
        # After the procedure there is nothing left to prevent (comes before the traits: pregnancy_fear too)
        if pregnancy_had_procedure(girl):
            return False

        # Trait overrides
        if girl.has_trait("pregnancy_fetish"):
            return False
        if girl.has_trait("pregnancy_fear"):
            girl._on_pill = True
            girl._pill_missed = 0
            girl._pill_days_active = 0
            print("[PREGNANCY] %s: pill self-start (pregnancy_fear — immediate)" % girl.gid)
            return True
        if girl.has_trait("infertile"):
            return False

        # Base chance
        chance = 0.02
        cream_count = getattr(girl, "CreampieCounts", 0)
        chance += cream_count * 0.03
        cum_log = getattr(girl, "CumLog", {})
        if cum_log.get("inside", 0) > 0:
            chance += 0.10
        if cum_log.get("condom", 0) == 0 and (girl.Sex_acts.get("sex", 0) + girl.Sex_acts.get("anal", 0)) > 0:
            chance += 0.05

        # Economy multiplier
        if girl.has_trait("rich"):
            chance *= 2.0
        elif girl.has_trait("poor"):
            chance *= 0.4

        # Lesbian multiplier
        if girl.has_trait("lesbian"):
            res = getattr(girl, "sexuality_spectrum", 100)
            if res >= 70:
                chance *= 0.1
            elif res >= 40:
                chance *= 0.3
            elif res >= 20:
                chance *= 0.6
            # else: no extra barrier

            if getattr(girl, "_blackmail_leverage", 0) >= 2:
                chance = max(chance, 0.02 * 0.5)

        if renpy.random.random() < chance:
            girl._on_pill = True
            girl._pill_missed = 0
            girl._pill_days_active = 0
            print("[PREGNANCY] %s: pill self-start (chance=%.3f)" % (girl.gid, chance))
            return True

        return False

    # ============================================================
    # PILL DAILY TICK (miss roll + days tracking)
    # ============================================================

    def _pill_daily_tick(girl):
        """Process daily pill mechanics for one girl."""
        # her own pill (girl_holds_her_pill): always on it, never a missed day
        if girl_holds_her_pill(girl):
            if not girl._on_pill or getattr(girl, "_on_placebo", False):
                _pill_start(girl, False)
                print("[PREGNANCY] %s: back on her own pill (she holds it until her turn)" % girl.gid)
            girl._pill_missed = 0
            return
        if not girl._on_pill:
            return

        girl._pill_days_active += 1

        # pregnancy_fear never forgets
        if girl.has_trait("pregnancy_fear"):
            girl._pill_missed = 0
            return

        # Placebo pills — no miss mechanic (she thinks she's taking them fine)
        if girl._on_placebo:
            girl._pill_missed = 0
            return

        # 5% chance to miss a day
        if renpy.random.random() < 0.05:
            girl._pill_missed += 1
            print("[PREGNANCY] %s: pill missed (consecutive=%d)" % (girl.gid, girl._pill_missed))
        else:
            if girl._pill_missed > 0:
                girl._pill_missed = max(0, girl._pill_missed - 1)

    # ============================================================
    # PILL INITIAL STATE (called from _reset_all_girls)
    # ============================================================

    def _pregnancy_init_pill_state(girl):
        """Set initial pill state for a girl at new game start.
        Virgins never start on the pill. Non-virgins use trait-based chance."""
        if store._pregnancy_mode == "off":
            return
        if girl_holds_her_pill(girl):
            girl._on_pill = True
            girl._pill_missed = 0
            print("[PREGNANCY] %s: starts on her own pill" % girl.gid)
            return
        if girl.has_trait("virgin") or girl.has_trait("naive"):
            return
        if girl.has_trait("pregnancy_fetish"):
            return
        if girl.has_trait("lesbian"):
            return

        if girl.has_trait("pregnancy_fear"):
            girl._on_pill = True
            girl._pill_missed = 0
            return

        chance = 0.30
        if girl.has_trait("rich"):
            chance = 0.60
        elif girl.has_trait("poor"):
            chance = 0.10

        if renpy.random.random() < chance:
            girl._on_pill = True
            girl._pill_missed = 0
            print("[PREGNANCY] %s: starts on pill (chance=%.0f%%)" % (girl.gid, chance * 100))

    # ============================================================
    # PREGNANCY-SCOPED FLAGS (central reset)
    # ============================================================

    # Girl flags that belong to ONE pregnancy and / or ONE partner, with their neutral value.
    #   "cycle"   : wiped when a NEW pregnancy starts (_process_pregnancy_rolls).
    #   "partner" : wiped when her NPC partner goes away (Girl.clear_npc_partner). They describe what
    #               THAT partner believes / is about to do, never the next one.
    # NOT wiped at _pregnancy_return: the permanent postpartum "proud dad" chitchat (ChitChat.rpy,
    # chitchat_npc_postpartum) reads _npc_paternity_claimed for as long as he stays her partner.
    _PREG_SCOPED_FLAGS = {
        "_player_pregnancy_response":           {"reset": None,  "scopes": ("cycle",)},
        "_npc_paternity_claimed":               {"reset": False, "scopes": ("cycle", "partner")},
        "_npc_pregnancy_confrontation_pending": {"reset": False, "scopes": ("cycle", "partner")},
        "_npc_pregnancy_save_attempt":          {"reset": False, "scopes": ("cycle", "partner")},
        # he confronted the player about THIS pregnancy: he knows the child is not his (preg_partner_knows)
        "_npc_pregnancy_confronted":            {"reset": False, "scopes": ("cycle", "partner")},
        # body moments already played (pregnancy_body.rpy). Reset values are assigned as-is to every girl:
        # keep them IMMUTABLE (a tuple, never a list / set).
        "_preg_body_moments_done":              {"reset": (),    "scopes": ("cycle",)},
    }

    def _pregnancy_reset_flags(girl, scope, reason=""):
        """Reset every _PREG_SCOPED_FLAGS entry of `scope` ("cycle" / "partner") and log what changed."""
        _changed = []
        for _attr, _cfg in _PREG_SCOPED_FLAGS.items():
            if scope not in _cfg["scopes"]:
                continue
            _old = getattr(girl, _attr, _cfg["reset"])
            if _old != _cfg["reset"]:
                _changed.append("%s=%r" % (_attr, _old))
            setattr(girl, _attr, _cfg["reset"])
        # a campus confrontation already queued for this girl dies with her flag
        if getattr(store, "_npc_pregnancy_confrontation_pending", None) == girl.gid:
            store._npc_pregnancy_confrontation_pending = None
            _changed.append("store._npc_pregnancy_confrontation_pending")
        print("[PREGNANCY] %s: reset '%s' flags (%s), cleared: %s" % (girl.gid, scope, reason, ", ".join(_changed) or "nothing"))

    # ============================================================
    # PER-GIRL POOLS
    # ============================================================
    def girl_pool(table, girl, what="", key=None):
        """Her own entry of a per-girl pool table ({gid: ..., "_default": ...}), or "_default" for a girl who
        has no pool there yet. THE lookup of every per-girl pool table (chitchat pools, birth / return
        texts, body moments): a topic or a text never plays silent, and the fallback is logged.
        With `key` the table is {gid: {key: ...}, "_default": {key: ...}} and the fallback is PER KEY: a girl
        who only wrote some keys uses "_default" for the rest (by design, so it is not logged)."""
        if key is not None:
            _own = (table.get(girl.gid) or {}).get(key)
            return _own if _own else table["_default"][key]
        _pool = table.get(girl.gid)
        if not _pool:
            print("[PREGNANCY] %s: no pool of her own%s, using _default" % (girl.gid, (" in " + what) if what else ""))
            _pool = table["_default"]
        return _pool

    # ============================================================
    # THE PROCEDURE: the v0.12 one-child limit (removed in v0.12.1)
    # ============================================================
    # No birth limit: after each delivery she gets a 14-day cooldown, then her fertile cycle resumes.
    # pregnancy_procedure_apply can no longer fire (pregnancy_limit_reached is always False);
    # pregnancy_procedure_undo remains for the Baby Eraser, the console and the v0.12 save migration
    # (pregnancy_procedure_backfill, called from _backfill_girl_attrs on load).
    _PREGNANCY_MAX_BIRTHS = 0    # 0 = no limit; kept for debug prints
    _PROCEDURE_TRAIT = "infertile"

    def pregnancy_story_blocked(girl):
        """Her story does not allow a pregnancy yet: GIRLS_CONFIG "no_conception", or she still holds her own pill
        (girl_holds_her_pill: Shion before her turn). Not the "infertile" trait: nothing in the game says she can't
        have children. She never conceives, the Fertility app shows 0%, and the "every girl" pregnancy achievements
        do not count her while it lasts."""
        return (bool(GIRLS_CONFIG.get(getattr(girl, "gid", None), {}).get("no_conception"))
                or girl_holds_her_pill(girl))

    def girl_holds_her_pill(girl):
        """GIRLS_CONFIG "pill_own": she is on her own pill and he has no say in it until her story step opens
        "pill_stop" (story_steps.rpy): she never forgets it, refuses his packs (no placebo swap), never stops when he
        asks. A married CEO does not leave it to chance (docs/plan_shion.md, Shion's pregnancy)."""
        return (bool(GIRLS_CONFIG.get(getattr(girl, "gid", None), {}).get("pill_own"))
                and not story_act_open(girl, "pill_stop"))

    def pregnancy_candidates():
        """The girls the "every girl" pregnancy achievements count (full_house, baby_boom). Never a girl who can't
        be in it: her story blocks it, she is Infertile (she never conceives: one Infertile roll made both
        achievements impossible), or her optional route is off this run (girl_route_enabled: not in the game)."""
        return [_g for _g in ALL_GIRLS
                if not pregnancy_story_blocked(_g) and not _g.has_trait("infertile") and girl_route_enabled(_g)]

    def pregnancy_limit_reached(girl):
        """No longer enforced: a girl can have any number of children.
        After each birth she gets a 14-day cooldown, then her cycle resumes."""
        return False

    def pregnancy_had_procedure(girl):
        """Sterile BECAUSE of the procedure after her last birth. Never true for a girl born infertile, and
        no longer true if the trait was taken away from her (trait picker)."""
        return bool(getattr(girl, "_birth_procedure", False)) and girl.has_trait(_PROCEDURE_TRAIT)

    def pregnancy_procedure_apply(girl, reason=""):
        """Her last birth is done: she is infertile from now on. The opposite side of the trait pair goes
        away (kept in _birth_procedure_removed for the undo) and she has no use for the pill any more.
        Silent: the player learns it when she tells him. Returns True when something changed."""
        if getattr(girl, "_birth_procedure", False) or not pregnancy_limit_reached(girl):
            return False
        if girl.has_trait(_PROCEDURE_TRAIT):
            # born infertile AND a mother: only the console gets her here. Nothing to operate on.
            print("[PREGNANCY] %s: procedure skipped (%s), she already is %s" % (girl.gid, reason, _PROCEDURE_TRAIT))
            return False
        _removed = []
        for _pair in TRAIT_PAIRS:
            if _PROCEDURE_TRAIT in (_pair["a"], _pair["b"]):
                for _side in (_pair["a"], _pair["b"]):
                    if _side != _PROCEDURE_TRAIT and girl.has_trait(_side):
                        girl.remove_trait(_side)
                        _removed.append(_side)
        girl.add_trait(_PROCEDURE_TRAIT)
        girl._birth_procedure = True
        girl._birth_procedure_removed = tuple(_removed)
        girl._on_pill = False
        girl._on_placebo = False
        girl._pill_missed = 0
        print("[PREGNANCY] %s: PROCEDURE (%s): +%s, removed=%s, pill dropped, births=%d/%d" % (
            girl.gid, reason, _PROCEDURE_TRAIT, _removed or "nothing", getattr(girl, "_pregnancy_count", 0), _PREGNANCY_MAX_BIRTHS))
        return True

    def pregnancy_procedure_undo(girl, reason=""):
        """The birth never happened (Baby Eraser), so neither did the procedure: the trait goes, what it
        replaced comes back, and the player no longer knows it. Returns True when something changed."""
        if not getattr(girl, "_birth_procedure", False):
            return False
        girl.remove_trait(_PROCEDURE_TRAIT)
        _back = tuple(getattr(girl, "_birth_procedure_removed", None) or ())
        for _trait in _back:
            girl.add_trait(_trait)
        girl._birth_procedure = False
        girl._birth_procedure_removed = ()
        girl.clear_flag("discovered_trait_" + _PROCEDURE_TRAIT)
        print("[PREGNANCY] %s: procedure UNDONE (%s): -%s, restored=%s" % (girl.gid, reason, _PROCEDURE_TRAIT, list(_back) or "nothing"))
        return True

    def pregnancy_procedure_backfill(girl):
        """v0.12 saves: her birth ended in the procedure (the one-child limit). The limit is gone since v0.12.1,
        so the procedure goes too: trait back to what it replaced, _birth_procedure off. No-op for everybody
        else (a girl born infertile has no _birth_procedure) and on every later load."""
        if not getattr(girl, "_birth_procedure", False):
            return False
        return pregnancy_procedure_undo(girl, "v0.12 save, birth limit removed in v0.12.1")

    # ============================================================
    # PHASE 5: DISCOVERY CHECK
    # ============================================================

    def _check_pregnancy_discovery():
        """Check if any girl has reached her discovery day. Sets pending flag.
        Only one discovery per day; extras queue for the next day."""
        if getattr(store, "_pregnancy_discovery_pending", None):
            return
        for girl in ALL_GIRLS:
            if (girl._pregnant
                    and not girl._pregnancy_known
                    and girl._pregnancy_day >= getattr(girl, "_pregnancy_discovery_day", 999)):
                store._pregnancy_discovery_pending = girl.gid
                print("[PREGNANCY] %s: discovery pending (day=%d, discovery_day=%d)" % (
                    girl.gid, girl._pregnancy_day, girl._pregnancy_discovery_day))
                return

    # ============================================================
    # PHASE 6: STAGE PROGRESSION
    # ============================================================

    _BIRTH_AWAY_DAYS = 7   # days she spends with her family after the birth (children.rpy dates the birth from it)

    def _pregnancy_stage_tick(girl):
        """Advance pregnancy stage based on day count.
        Stage 0 (hidden): day 0-6, subtle narrations
        Stage 1 (discovered): day 7-12 (handled by Phase 5 discovery)
        Stage 2 (apparent): day 20+, visual stage 1
        Stage 3 (full): day 40+, visual stage 2
        Birth: day 65 (short) / 130 (long)
        """
        if not girl._pregnant:
            return
        if getattr(girl, "_giving_birth", False):
            return

        old_stage = girl._pregnancy_stage
        day = girl._pregnancy_day

        # Birth trigger
        _birth_day = _pregnancy_birth_day()
        if day >= _birth_day:
            girl._giving_birth = True
            girl._birth_return_day = store.Day + _BIRTH_AWAY_DAYS
            girl_sent_away(girl, "giving birth")   # off the map for a week: girl_is_away() keeps every picker off her
            _pregnancy_queue_birth(girl)
            print("[PREGNANCY] %s: birth triggered at day %d, returns Day %d" % (girl.gid, day, girl._birth_return_day))
            return

        if day >= 40 and old_stage < 3:
            girl._pregnancy_stage = 3
            print("[PREGNANCY] %s: stage -> 3 (full) at day %d" % (girl.gid, day))
        elif day >= 20 and old_stage < 2:
            girl._pregnancy_stage = 2
            print("[PREGNANCY] %s: stage -> 2 (apparent) at day %d" % (girl.gid, day))
            # her NPC partner confronts him once she shows: _queue_npc_confrontation (daily tick)
        elif day >= 7 and old_stage < 1 and girl._pregnancy_known:
            girl._pregnancy_stage = 1

    # Birth announcements: one slot (label _pregnancy_birth reads it) + a queue, because two girls can go into
    # labor on the same day. label Wait loops while the slot is set; the label refills it from the queue.
    def _pregnancy_queue_birth(girl):
        if not getattr(store, "_pregnancy_birth_pending", None):
            store._pregnancy_birth_pending = girl.gid
        elif store._pregnancy_birth_pending != girl.gid and girl.gid not in store._pregnancy_birth_queue:
            store._pregnancy_birth_queue.append(girl.gid)
            print("[PREGNANCY] %s: birth announcement queued behind %s" % (girl.gid, store._pregnancy_birth_pending))

    def _pregnancy_next_birth():
        """End of a birth announcement: the next girl who went into labor the same day, or None."""
        while store._pregnancy_birth_queue:
            _gid = store._pregnancy_birth_queue.pop(0)
            _g = GIRL_BY_ID.get(_gid)
            if _g is not None and getattr(_g, "_giving_birth", False):
                return _gid
        return None

    def pregnancy_return_apply(girl):
        """She is back on campus: the child exists from now on (child_register_birth, BEFORE the birth state is
        cleared: it dates the birth from _birth_return_day), the pregnancy is over, and whatever waited for
        her is resolved this very morning. State only, no text: label _pregnancy_return and the QA helper
        child_debug_birth share it."""
        child_register_birth(girl)
        girl._pregnant = False
        girl._pregnancy_day = 0
        girl._pregnancy_stage = 0
        girl._pregnancy_known = False
        girl._giving_birth = False
        girl._birth_return_day = 0
        girl._away_text_sent = False
        girl._pregnancy_count += 1
        girl._postpartum = True
        girl._pregnancy_cooldown = 14
        girl.loc = get_scheduled_location_for(girl, store.Day, store.TimeIndex)
        # the week away was not neglect: the hardcore relationship clock restarts today, the WHOLE clock
        # (same fields Change_Status clears on contact, plus the partner escalation day: both are absolute
        # days that kept running while he could not reach her)
        girl._hc_last_interaction_day = store.Day
        girl._hc_single_warned = 0
        girl._hc_partner_spawn_day = 0
        girl._hc_bf_next_escalation_day = 0
        # what waited for her (talk / fight / breakup with her partner) is resolved this very morning
        npc_next_day_process(girl)
        # her partner was placed for this slot while she was still away (locations are set at the slot change,
        # before this event): back to his schedule now, not one slot later
        _npc = get_npc_partner_for(girl) if girl.has_npc_partner() else None
        if _npc is not None:
            _npc.update_location_for_time(store.Day, store.TimeIndex)
        print("[PREGNANCY] %s: returned! births=%d children=%d cooldown=14 postpartum=True" % (
            girl.gid, girl._pregnancy_count, girl._children_count))

    def _pregnancy_next_return():
        """End of a return event: another girl whose week is over today, or None."""
        for _g in ALL_GIRLS:
            if getattr(_g, "_giving_birth", False) and store.Day >= getattr(_g, "_birth_return_day", 99999):
                return _g.gid
        return None

    # What her ART shows for each progression stage (Full mode only): 1 = small bump + bigger breasts,
    # 2 = full belly. Stages 0 / 1 (hidden / discovered) still look normal. The files per stage live in
    # PREG_ART (scripts/Images/preg_art.rpy).
    _PREG_VISUAL_STAGE = {2: 1, 3: 2}

    def pregnancy_visual_stage(girl):
        """Visual pregnancy stage of her art: 0 normal, 1 apparent, 2 full. Lite / Off never change the
        art. The console preview (preg_art_preview, preg_art.rpy) overrides the real state."""
        _preview = _PREG_ART_PREVIEW.get(girl.gid)
        if _preview is not None:
            return _preview
        if store._pregnancy_mode != "full" or not getattr(girl, "_pregnant", False):
            return 0
        return _PREG_VISUAL_STAGE.get(getattr(girl, "_pregnancy_stage", 0), 0)

    def preg_partner_knows(girl):
        """Her NPC partner KNOWS the child is not his: he confronted the player about it and stayed (she tried
        to save the relationship, or he is the NTR partner who stays). Nobody may describe him as the happy
        father-to-be, unless he took the child on anyway (_npc_paternity_claimed: "I'll raise the kid")."""
        return (girl.has_npc_partner() and getattr(girl, "_npc_pregnancy_confronted", False)
                and not getattr(girl, "_npc_paternity_claimed", False))

    def _flag_npc_confrontation(girl, reason=""):
        """THE writer of the girl flag: her NPC partner will confront him once her belly shows
        (_queue_npc_confrontation re-checks it every day). Set at the discovery, with or without her warning."""
        girl._npc_pregnancy_confrontation_pending = True
        print("[PREGNANCY] %s: NPC confrontation flagged for stage 2 (%s)" % (girl.gid, reason))

    def _queue_npc_confrontation():
        """Her NPC partner confronts him once her belly shows (stage 2+). One confrontation per morning (one
        store slot), re-checked EVERY day: it used to be queued only at the stage change, so a second girl who
        reached stage 2 the same day (or one who jumped straight to stage 3) lost hers forever."""
        if getattr(store, "_npc_pregnancy_confrontation_pending", None):
            return
        for _g in ALL_GIRLS:
            if (getattr(_g, "_npc_pregnancy_confrontation_pending", False)
                    and getattr(_g, "_pregnant", False) and getattr(_g, "_pregnancy_stage", 0) >= 2
                    and not getattr(_g, "_giving_birth", False)
                    and not getattr(_g, "_npc_paternity_claimed", False)
                    and _g.has_npc_partner()):
                store._npc_pregnancy_confrontation_pending = _g.gid
                print("[PREGNANCY] %s: NPC confrontation queued (stage %d)" % (_g.gid, _g._pregnancy_stage))
                return

    # ============================================================
    # PREGNANCY DAILY TICK (master function)
    # ============================================================

    def _pregnancy_daily_tick():
        """Main daily tick for pregnancy system. Called from _per_day_cleanup."""
        if store._pregnancy_mode == "off":
            return

        for g in ALL_GIRLS:
            # Pill mechanics
            _pill_daily_tick(g)

            # Pill self-start check (only if not on pill)
            if not g._on_pill:
                _pill_self_start_check(g)

            # Pregnancy day advancement + stage progression
            if g._pregnant:
                g._pregnancy_day += 1
                _pregnancy_stage_tick(g)

            # Birth return check
            if getattr(g, "_giving_birth", False) and store.Day >= getattr(g, "_birth_return_day", 99999):
                if not getattr(store, "_pregnancy_return_pending", None):
                    store._pregnancy_return_pending = g.gid
                    print("[PREGNANCY] %s: return pending on Day %d" % (g.gid, store.Day))

            # Pregnancy cooldown decrement
            if getattr(g, "_pregnancy_cooldown", 0) > 0:
                g._pregnancy_cooldown -= 1

            # Morning after pill: one used slot comes back per month
            _plan_b_regen_tick(g)

        # Child support: $250 / week per child, every 7 days. children.rpy charges every mother together
        # and queues the notice label Wait narrates (the money used to vanish without a word).
        if store.Day % 7 == 0:
            child_support_charge()

        # Discovery check (sets pending flag for morning hook)
        _check_pregnancy_discovery()
        # NPC confrontation check (same: one per morning, re-checked daily)
        _queue_npc_confrontation()

        # Fertility vitamin countdown
        if getattr(store, "_player_fertility_vitamin_active", False):
            _vd = getattr(store, "_player_fertility_vitamin_days", 0) - 1
            if _vd <= 0:
                store._player_fertility_vitamin_active = False
                store._player_fertility_vitamin_days = 0
                print("[PREGNANCY] fertility vitamin expired")
            else:
                store._player_fertility_vitamin_days = _vd

        debug_log("[PREGNANCY] daily tick done, Day=%d" % store.Day)

    # ============================================================
    # PHASE 3: PROBABILITY ENGINE + CUM INTEGRATION
    # ============================================================

    # Per-scene risk accumulator (reset by session_cum_reset)
    _scene_pregnancy_risks = []

    # Player's fertility vitamins: conception chance multiplier while active
    # (the pharmacy clerk sells them as "up to 200%": doubling)
    _FERT_VITAMIN_MULT = 2.0
    _FERT_VITAMIN_DAYS = 7

    def _calc_pregnancy_chance(girl, cum_type, known_only=False):
        """Calculate pregnancy chance for a single cum event.
        known_only: estimate shown to the player (phone Fertility app). Biological
        traits only count once discovered, so the UI never leaks hidden traits."""
        if store._pregnancy_mode == "off":
            return 0.0
        if pregnancy_story_blocked(girl):
            return 0.0

        # Pull out = flat 1%
        if cum_type in ("outside", "pull_out"):
            return 0.01

        # Non-vaginal = 0%
        if cum_type not in ("inside", "condom_removed_inside"):
            return 0.0

        _breedable = girl.has_trait("breedable")
        _infertile = girl.has_trait("infertile")
        if known_only:
            _breedable = _breedable and girl.get_flag("discovered_trait_breedable")
            _infertile = _infertile and girl.get_flag("discovered_trait_infertile")

        # Base from cycle phase (breedable: expanded fertile window, days 10-20 count as fertile)
        base = _CYCLE_CHANCE[_cycle_phase_for_day(get_cycle_day(girl), _breedable)]

        # Infertile = impossible
        if _infertile:
            return 0.0

        # Biological multiplier
        bio_mult = 1.5 if _breedable else 1.0

        # Pill multiplier
        pill_mult = get_pill_effectiveness(girl)

        # Player fertility vitamin
        vitamin_active = getattr(store, "_player_fertility_vitamin_active", False)
        vitamin_mult = _FERT_VITAMIN_MULT if vitamin_active else 1.0

        chance = base * bio_mult * pill_mult * vitamin_mult
        return min(chance, 1.0)

    def _register_pregnancy_risk(girl, cum_type, scene_type=None):
        """Register a pregnancy risk event during a scene.
        Called from process_cum() for relevant cum types."""
        if store._pregnancy_mode == "off":
            return

        # process_cum() uses cum_type "inside" for anal creampies too, and "outside" for every
        # scene: only vaginal penetration can get her pregnant.
        if scene_type in _FERT_ANAL_SCENES or scene_type in _FERT_NO_PENETRATION_SCENES:
            print("[PREGNANCY] %s: no risk, scene=%s type=%s" % (girl.gid, scene_type, cum_type))
            return

        # What SHE knows: he finished inside her with no condom on (a stealth-removed / broken condom
        # still looks like a condom to her). Feeds the morning after pill window; recorded even when
        # no roll will happen (already pregnant without knowing it, cooldown...).
        if cum_type == "condom_removed_inside" or (cum_type == "inside" and not getattr(store, "condom_active", False)):
            girl._last_inside_day = store.Day

        # Already pregnant, on cooldown, or already had every child she can have (_PREGNANCY_MAX_BIRTHS)
        if girl._pregnant or getattr(girl, "_pregnancy_cooldown", 0) > 0:
            return
        if pregnancy_limit_reached(girl):
            return

        # Condom check: intact condom = no risk
        _condom_on = getattr(store, "condom_active", False)
        _broken = getattr(store, "_condom_broken", False)
        _stealth = getattr(store, "_stealth_condom_removed", False)
        if _condom_on and not _broken and not _stealth:
            print("[PREGNANCY] %s: condom intact, no risk registered" % girl.gid)
            return

        if pregnancy_story_blocked(girl):
            print("[PREGNANCY] %s: no roll, her story does not allow a pregnancy yet (no_conception)" % girl.gid)
            return
        chance = _calc_pregnancy_chance(girl, cum_type)
        if chance > 0:
            roll = renpy.random.random()
            print("[PREGNANCY] %s: risk type=%s chance=%.3f roll=%.3f" % (girl.gid, cum_type, chance, roll))
            store._scene_pregnancy_risks.append({
                "gid": girl.gid,
                "type": cum_type,
                "chance": chance,
                "roll": roll,
                "result": "pregnant" if roll < chance else "safe",
            })
            if roll < chance:
                girl._pregnant = True
                girl._pregnancy_day = 0
                girl._pregnancy_stage = 0
                girl._pregnancy_known = False
                girl._pregnancy_discovery_day = renpy.random.randint(7, 12)
                _pregnancy_reset_flags(girl, "cycle", "conception")
                if girl._on_pill and getattr(girl, "_on_placebo", False):
                    unlock_achievement("sugar_pills")
                if all(getattr(_g, "_pregnant", False) for _g in pregnancy_candidates()):
                    unlock_achievement("baby_boom")
                # the turned queen carries his child (the FULL inversion: control corruption swapped her
                # femdom for submissive at 30, evolved_traits records the chain)
                if (getattr(girl, "evolved_traits", {}) or {}).get("femdom") == "submissive" and girl.has_trait("submissive"):
                    unlock_achievement("new_management")
                print("[PREGNANCY] %s: PREGNANT at moment of %s! discovery_day=%d" % (
                    girl.gid, cum_type, girl._pregnancy_discovery_day))
                if hasattr(store, "Player") and store.Player.has_item("instant_preg_test"):
                    renpy.show("impregnation_anim", zorder=99999)
                    print("[PREGNANCY] impregnation animation shown for %s (non-blocking)" % girl.gid)

    def _process_pregnancy_rolls():
        """Safety-net cleanup at scene end.
        Rolls now happen inline in _register_pregnancy_risk. This just
        logs the summary and clears the list."""
        _risks = store._scene_pregnancy_risks
        store._scene_pregnancy_risks = []

        if not _risks:
            return

        for entry in _risks:
            print("[PREGNANCY] scene-end summary: %s type=%s chance=%.3f roll=%.3f result=%s" % (
                entry["gid"], entry["type"], entry["chance"],
                entry.get("roll", -1), entry.get("result", "unknown")))

    # ============================================================
    # PHASE 4: PILL INTERACTION CHECKS
    # ============================================================

    _PILL_ACCEPT_OBED = 500     # obedient enough to accept without much Love
    _PILL_FORCE_OBED = 800      # this obedient, she cannot refuse the pills at all (any trait)
    _PILL_STRANGER_LOVE = 200   # below this, with no history, offering pills is an insult

    # Expression + stat changes for every outcome of offering her pills (keyed by dialogue key)
    # Outcome of offering her pills / the morning after pill, keyed by dialogue key:
    #   expr    : her face (must exist in POSE_EXPRESSIONS["standing"])
    #   stats   : Change_Status applied after the line
    #   reveals : True only when the LINE ITSELF makes it explicit whether she is on the pill.
    #             Only then does the player learn it (discovered_pill). With too little intimacy
    #             she shuts him down without giving anything away.
    _PILL_REACTION = {
        "pill_stash":                    {"expr": "smile",         "reveals": True},
        "pill_swap":                     {"expr": "smile",         "reveals": True},
        "pill_accept_forced_obed":       {"expr": "sad",           "reveals": True, "stats": {"Obed": 8}},
        "pill_accept_fetish_obed":       {"expr": "sad",           "reveals": True, "stats": {"Obed": 8, "Love": -5}},
        "pill_refuse_fetish":            {"expr": "smirk",         "reveals": True},
        "pill_accept_fear":              {"expr": "happy",         "reveals": True, "stats": {"Love": 8}},
        "pill_refuse_lesbian_res":       {"expr": "confused",      "reveals": True},
        "pill_accept_lesbian_reluctant": {"expr": "uncomfortable", "reveals": True, "stats": {"Obed": 3}},
        "pill_accept_lesbian_blackmail": {"expr": "angry",         "reveals": True, "stats": {"Obed": 5, "Love": -3}},
        "pill_offended_stranger":        {"expr": "disgusted",     "stats": {"Love": -20, "Obed": -8}},
        "pill_offended_partner_on":      {"expr": "angry",         "reveals": True, "stats": {"Love": -20, "Obed": -5}},
        "pill_offended_partner_off":     {"expr": "angry",         "reveals": True, "stats": {"Love": -20, "Obed": -5}},
        "pill_offended_virgin":          {"expr": "angry",         "stats": {"Love": -15, "Obed": -5}},
        "pill_offended_no_acts":         {"expr": "angry",         "stats": {"Love": -10, "Obed": -5}},
        "pill_refuse_virgin_gentle":     {"expr": "embarrassed",   "reveals": True},
        "pill_accept_hesitant":          {"expr": "shy",           "reveals": True, "stats": {"Love": 3}},
        "pill_accept_obed":              {"expr": "embarrassed",   "reveals": True, "stats": {"Obed": 5}},
        "pill_refuse_no_acts_on":        {"expr": "uncomfortable", "reveals": True},
        "pill_refuse_no_acts_off":       {"expr": "uncomfortable", "reveals": True},
        "pill_accept_love":              {"expr": "happy",         "reveals": True, "stats": {"Love": 5}},
        "pill_refuse_default":           {"expr": "annoyed"},
        "pill_refuse_procedure":         {"expr": "looking_down"},   # sterile since the procedure: no use for them
        "pill_stop_not_on":              {"expr": "confused"},
        "pill_stop_refuse_fear":         {"expr": "scared"},
        "pill_stop_accept_obed":         {"expr": "sad",           "stats": {"Obed": 5}},
        "pill_stop_accept_dating":       {"expr": "surprised",     "stats": {"Love": 5}},
        "pill_stop_accept_hesitant":     {"expr": "worried"},
        "pill_stop_refuse_lesbian":      {"expr": "angry"},
        "pill_stop_refuse_default":      {"expr": "serious"},
        "pill_refuse_own":               {"expr": "smug",          "reveals": True},
        "pill_stop_refuse_own":          {"expr": "serious",       "reveals": True},
        "pill_stop_accept_netori":       {"expr": "smirk",         "stats": {"Love": 5}},
        # Morning after pill. ma_offended / ma_no_risk / ma_accept also have per-girl lines + faces below.
        "ma_offended":                   {"expr": "angry",         "stats": {"Love": -10, "Obed": -5}},
        "ma_no_risk":                    {"expr": "confused"},
        "ma_refuse_limit":               {"expr": "sad"},
        "ma_refuse_procedure":           {"expr": "looking_down"},
        "ma_refuse_fetish":              {"expr": "smirk"},
        "ma_accept_fear":                {"expr": "scared",        "stats": {"Love": 5}},
        "ma_accept_obed":                {"expr": "sad",           "stats": {"Obed": 5}},
        "ma_refuse_dating_love":         {"expr": "shy"},
        "ma_accept":                     {"expr": "worried",       "stats": {"Love": 3}},
    }

    def _fert_act_counts(girl):
        """(penetration, other sexual acts) she has done with the player.
        Central reader in characters_stats.rpy: acts only ("sex" / "anal"), never a position."""
        return girl_act_counts(girl)

    def _pill_react(girl, key):
        """Expression + stat changes of a pill / morning-after outcome (data in _PILL_REACTION)."""
        _r = _PILL_REACTION.get(key, {})
        set_scene_expression(girl, _pill_expr(girl, key))
        for _stat, _amt in _r.get("stats", {}).items():
            Change_Status(girl, _stat, _amt)
        # Her outcome line voices the trait itself ("I was worried about this" / "I don't want anything in the way")
        if key.endswith("_fear") and girl.has_trait("pregnancy_fear"):
            girl.discover("discovered_trait_pregnancy_fear")
        elif "fetish" in key and girl.has_trait("pregnancy_fetish"):
            girl.discover("discovered_trait_pregnancy_fetish")

    def _pill_expr(girl, key):
        """Her face for this outcome: per-girl override first (_MA_GIRL_EXPR), then the shared table."""
        return _MA_GIRL_EXPR.get(girl.gid, {}).get(key) or _PILL_REACTION.get(key, {}).get("expr", "normal")

    def _pill_line_for(girl, key):
        """Her line for this outcome: per-girl pool first (_MA_GIRL_LINES), then _PILL_DIALOGUE."""
        return _MA_GIRL_LINES.get(girl.gid, {}).get(key) or _PILL_DIALOGUE.get(key, "...")

    def _pill_start(girl, is_placebo):
        girl._on_pill = True
        girl._on_placebo = is_placebo
        girl._pill_missed = 0
        girl._pill_days_active = 0

    def _pill_change_banner(girl, started):
        """Banner when she TELLS him she starts / stops the pill (she said yes to his request).
        A change she keeps to herself (a silent swap, a missed day) shows nothing."""
        if started:
            _sub = _tr("Placebo, 0% (she thinks it's real)") if girl._on_placebo else _tr("Check Fertility in her contact")
            _text = _tr("She started taking the pill") + "\n" + _sub
        else:
            _text = _tr("She stopped taking the pill") + "\n" + _tr("Check Fertility in her contact")
        renpy.music.play("audio/Information.mp3", channel="notify_sfx", loop=False)
        renpy.show_screen("discovery_banner", girl_name=girl.Name, info_text=_text, name_color=girl.color)
        print("[PREGNANCY] %s: pill change banner (started=%s on_placebo=%s)" % (girl.gid, started, girl._on_placebo))

    def _pill_stash_or_swap(girl, is_placebo):
        """She is already on the pill: keep her own pack, or silently swap real <-> placebo."""
        already_placebo = getattr(girl, "_on_placebo", False)
        if already_placebo != is_placebo:
            girl._on_placebo = is_placebo
            print("[PREGNANCY] %s: swapped pill type, on_placebo=%s" % (girl.gid, is_placebo))
            return {"result": "swap", "key": "pill_swap"}
        return {"result": "stash", "key": "pill_stash"}

    def _pill_offer_check(girl, is_placebo=False):
        """Check whether girl accepts birth control pills from the player.
        Returns dict with 'result' ('accept'/'refuse'/'offended'/'swap'/'stash')
        and 'key' for dialogue lookup (also the key into _PILL_REACTION).
        Order: sterile since the procedure (no use for them) > very high Obed cannot refuse > NO HISTORY
        (offended / refuse, whatever her traits or pill state) > already on it > traits > lesbian >
        Love / Obed."""

        if pregnancy_had_procedure(girl):
            return {"result": "refuse", "key": "pill_refuse_procedure"}
        # her own prescription: nothing he hands her goes in her mouth (no placebo swap either)
        if girl_holds_her_pill(girl):
            return {"result": "refuse", "key": "pill_refuse_own"}

        already_on_pill = girl._on_pill
        _state = "on" if already_on_pill else "off"

        # Very high Obed: she cannot say no, whatever she thinks of it
        if girl.Obed >= _PILL_FORCE_OBED:
            if already_on_pill:
                return _pill_stash_or_swap(girl, is_placebo)
            _pill_start(girl, is_placebo)
            if girl.has_trait("pregnancy_fetish"):
                return {"result": "accept", "key": "pill_accept_fetish_obed"}
            return {"result": "accept", "key": "pill_accept_forced_obed"}

        sex_count, manual_count = _fert_act_counts(girl)
        total_acts = sex_count + manual_count
        is_virgin = girl.has_trait("virgin")
        is_lesbian = girl.has_trait("lesbian")
        _dating = girl.is_dating_player()
        _obed_threshold = _PILL_ACCEPT_OBED
        if is_lesbian:
            _obed_threshold += 200

        # No sexual history with the player and not his girlfriend: what is he implying?
        # Comes before everything else: a stranger is a stranger, on the pill or not.
        if total_acts == 0 and not _dating:
            if girl.Love < _PILL_STRANGER_LOVE:
                return {"result": "offended", "key": "pill_offended_stranger"}
            if girl.has_npc_partner():
                return {"result": "offended", "key": "pill_offended_partner_" + _state}
            if is_virgin:
                if girl.Love < 600:
                    return {"result": "offended", "key": "pill_offended_virgin"}
                return {"result": "refuse", "key": "pill_refuse_virgin_gentle"}
            if girl.Obed >= _obed_threshold:
                if already_on_pill:
                    return _pill_stash_or_swap(girl, is_placebo)
                _pill_start(girl, is_placebo)
                return {"result": "accept", "key": "pill_accept_obed"}
            if girl.Love < 400:
                return {"result": "offended", "key": "pill_offended_no_acts"}
            return {"result": "refuse", "key": "pill_refuse_no_acts_" + _state}

        # Already on pill: stash or swap
        if already_on_pill:
            return _pill_stash_or_swap(girl, is_placebo)

        # Trait overrides (only once there is some history)
        if girl.has_trait("pregnancy_fetish"):
            return {"result": "refuse", "key": "pill_refuse_fetish"}
        if girl.has_trait("pregnancy_fear"):
            _pill_start(girl, is_placebo)
            return {"result": "accept", "key": "pill_accept_fear"}

        # Lesbian + high resistance
        if is_lesbian:
            _res = getattr(girl, "_lesbian_resistance", 100)
            if _res >= 50 and girl.Obed < _obed_threshold:
                return {"result": "refuse", "key": "pill_refuse_lesbian_res"}
            if _res < 50:
                _pill_start(girl, is_placebo)
                return {"result": "accept", "key": "pill_accept_lesbian_reluctant"}
            if getattr(girl, "_blackmail_leverage", 0) >= 2:
                _pill_start(girl, is_placebo)
                return {"result": "accept", "key": "pill_accept_lesbian_blackmail"}

        # Virgin who only did hj/bj/tj so far: things are heading that way
        if is_virgin and sex_count == 0 and total_acts < 3:
            if girl.Love >= 400:
                _pill_start(girl, is_placebo)
                return {"result": "accept", "key": "pill_accept_hesitant"}
            if girl.Obed >= _obed_threshold:
                _pill_start(girl, is_placebo)
                return {"result": "accept", "key": "pill_accept_obed"}
            return {"result": "refuse", "key": "pill_refuse_virgin_gentle"}

        # Has history (or is dating him): Love or Obed
        if girl.Love >= 400:
            _pill_start(girl, is_placebo)
            return {"result": "accept", "key": "pill_accept_love"}
        if girl.Obed >= _obed_threshold:
            _pill_start(girl, is_placebo)
            return {"result": "accept", "key": "pill_accept_obed"}

        return {"result": "refuse", "key": "pill_refuse_default"}

    def _pill_stop_check(girl):
        """Check whether girl agrees to stop taking the pill.
        Returns dict with 'result' ('accept'/'refuse') and 'key'."""
        if not girl._on_pill:
            return {"result": "refuse", "key": "pill_stop_not_on"}

        if girl.has_trait("pregnancy_fear"):
            return {"result": "refuse", "key": "pill_stop_refuse_fear"}
        if girl_holds_her_pill(girl):
            return {"result": "refuse", "key": "pill_stop_refuse_own"}
        # a married woman who betrays her husband with him (shion_netori.rpy): his baby, her husband's name
        if netori_willing(girl):
            girl._on_pill = False
            girl._on_placebo = False
            girl._pill_stopped_for_him = True   # the agreement is REMEMBERED (_pill_self_start_check)
            return {"result": "accept", "key": "pill_stop_accept_netori"}

        is_lesbian = girl.has_trait("lesbian")

        if girl.Obed >= 700:
            girl._on_pill = False
            girl._on_placebo = False
            girl._pill_stopped_for_him = True   # the agreement is REMEMBERED (_pill_self_start_check)
            return {"result": "accept", "key": "pill_stop_accept_obed"}

        _dating = girl.is_dating_player()
        if girl.Love >= 800 and _dating:
            girl._on_pill = False
            girl._on_placebo = False
            girl._pill_stopped_for_him = True   # the agreement is REMEMBERED (_pill_self_start_check)
            return {"result": "accept", "key": "pill_stop_accept_dating"}

        if girl.Love >= 600 and girl.Obed >= 400:
            girl._on_pill = False
            girl._on_placebo = False
            girl._pill_stopped_for_him = True   # the agreement is REMEMBERED (_pill_self_start_check)
            return {"result": "accept", "key": "pill_stop_accept_hesitant"}

        if is_lesbian and girl.Obed < 700:
            return {"result": "refuse", "key": "pill_stop_refuse_lesbian"}

        return {"result": "refuse", "key": "pill_stop_refuse_default"}

    _FERT_PLAN_B_WINDOW_DAYS = 2   # she only sees a point in it this long after he finished inside her raw

    def _plan_b_recent_risk(girl):
        """Did he finish inside her without a condom (as far as she knows) in the last few days?"""
        _last = getattr(girl, "_last_inside_day", None)
        return _last is not None and store.Day - _last <= _FERT_PLAN_B_WINDOW_DAYS

    def _morning_after_check(girl):
        """Check whether girl accepts the morning after pill.
        Returns dict with 'result' ('accept'/'refuse'/'offended') and 'key'.
        Same spirit as the pills: no sex with the player = an insult; and it only makes sense to
        her right after an unprotected finish inside."""
        if pregnancy_had_procedure(girl):
            return {"result": "refuse", "key": "ma_refuse_procedure"}

        uses = getattr(girl, "_morning_after_uses", 0)
        if uses >= _FERT_PLAN_B_LIMIT:
            return {"result": "refuse", "key": "ma_refuse_limit"}

        _sex_count, _other = _fert_act_counts(girl)

        # Never had sex with him: what exactly does he think happened?
        if _sex_count == 0:
            return {"result": "offended", "key": "ma_offended"}
        # Nothing risky lately: she has no use for it (very obedient girls included, there is nothing to prevent)
        if not _plan_b_recent_risk(girl):
            return {"result": "refuse", "key": "ma_no_risk"}

        # Very high Obed: she cannot say no, whatever she wants
        if girl.Obed >= _PILL_FORCE_OBED:
            return {"result": "accept", "key": "ma_accept_obed"}
        if girl.has_trait("pregnancy_fetish"):
            return {"result": "refuse", "key": "ma_refuse_fetish"}
        if girl.has_trait("pregnancy_fear"):
            return {"result": "accept", "key": "ma_accept_fear"}
        if girl.Obed >= 600:
            return {"result": "accept", "key": "ma_accept_obed"}
        if girl.Love >= 700 and girl.is_dating_player():
            return {"result": "refuse", "key": "ma_refuse_dating_love"}
        return {"result": "accept", "key": "ma_accept"}

    # ============================================================
    # PILL DIALOGUE POOLS
    # ============================================================

    _PILL_DIALOGUE = {
        "pill_accept_forced_obed":       _("...Whatever you say. I'll take them."),
        "pill_accept_fetish_obed":       _("I hate this... you know I don't want them. But fine. For you."),
        "pill_offended_stranger":        _("Excuse me?! I barely know you and you're handing me birth control? Get away from me."),
        # Partner + no history: offended, but these two make her pill status explicit (reveals=True)
        "pill_offended_partner_on":      _("I have a %(pl)s, and I already take these. So why exactly are YOU handing me birth control?"),
        "pill_offended_partner_off":     _("I have a %(pl)s, and I'm not even on the pill. I'm certainly not starting because YOU want me to."),
        "pill_stash":                    _("Oh, I'm already on the pill. But I'll save this pack for next month, thanks!"),
        "pill_swap":                     _("Oh, more pills? I'll use these next."),
        "pill_refuse_fetish":            _("I don't need those. I want to feel everything natural."),
        "pill_accept_fear":              _("Thank you! I was worried about this."),
        "pill_refuse_lesbian_res":       _("Why would I need birth control? I'm not sleeping with guys."),
        "pill_accept_lesbian_reluctant": _("...I guess I should be smart about this."),
        "pill_accept_lesbian_blackmail": _("Fine. Add it to the list of things you're making me do."),
        "pill_offended_virgin":          _("What the hell? Why would you give me these?"),
        "pill_refuse_virgin_gentle":     _("That's... sweet of you to think ahead? But I don't need these yet."),
        "pill_accept_hesitant":          _("I guess... things are heading that way, huh? Okay."),
        "pill_accept_obed":              _("O-okay... if you think I should..."),
        "pill_offended_no_acts":         _("Excuse me? We haven't even... what are you implying?"),
        "pill_refuse_no_acts_on":        _("I'm... already on the pill, actually. But why are you giving me these? We haven't done anything."),
        "pill_refuse_no_acts_off":       _("I'm not on the pill, and I don't need to be. We haven't done anything, remember?"),
        "pill_accept_love":              _("Smart thinking. Better safe than sorry."),
        "pill_refuse_default":           _("I can handle my own protection, thanks."),
        "pill_refuse_procedure":         _("I don't need those anymore. Not since the birth."),
        "pill_stop_not_on":              _("I'm not taking any pills."),
        "pill_stop_refuse_fear":         _("Are you crazy? No way I'm stopping."),
        "pill_stop_accept_obed":         _("If that's what you want..."),
        "pill_stop_accept_dating":       _("Are you saying you want a baby...?"),
        "pill_stop_accept_hesitant":     _("I don't know about this, but okay..."),
        "pill_stop_refuse_lesbian":      _("Absolutely not. I'm not taking any chances."),
        "pill_stop_refuse_default":      _("No, I'd rather keep taking them."),
        "pill_refuse_own":               _("I have my own prescription, thank you. I don't take pills from anyone."),
        "pill_stop_refuse_own":          _("My body, my prescription. You have no say in it."),
        "pill_stop_accept_netori":       _("Stop? ...You want to put a baby in a married woman. ...Fine. He'll think it's his."),
        "ma_refuse_limit":               _("I can't keep taking these, it's messing me up."),
        "ma_refuse_procedure":           _("I don't need that. I can't get pregnant anymore."),
        "ma_refuse_fetish":              _("No way. If it happened, it happened. I want this."),
        "ma_accept_fear":                _("Give me that right now!"),
        "ma_accept_obed":                _("If you think it's best..."),
        "ma_refuse_dating_love":         _("But... what if I want to keep it?"),
        "ma_accept":                     _("Okay, better safe than sorry."),
        "ma_offended":                   _("A morning after pill? We have never even slept together. What are you implying?"),
        "ma_no_risk":                    _("I don't need that. Nothing risky happened between us lately."),
    }

    # Per-girl pools for the morning after pill (missing gid / key -> shared line above).
    #   gwen  : sarcastic, finds it funny that he thinks she would need it
    #   rogue : insecure
    #   ntw   : strong and aggressive, offended at being offered
    #   tenny : insecure, flustered
    _MA_GIRL_LINES = {
        "gwen": {
            "ma_offended": _("Pfft, hahaha! A morning after pill? For what, exactly? Did I miss the part where we had sex?"),
            "ma_no_risk":  _("Cute. But you didn't finish in me, remember? Save it for when you actually screw up."),
            "ma_accept":   _("Yeah, hand it over. I like my life the way it is, thanks."),
        },
        "rogue": {
            "ma_offended": _("A... a mornin' after pill? Sugar, we ain't ever... why would you think I'd need that from you?"),
            "ma_no_risk":  _("I... don't think I need that, sugar. Nothin' happened I should worry about... right?"),
            "ma_accept":   _("Thank you, sugar... I was too scared to ask. Give it here."),
        },
        "ntw": {
            "ma_offended": _("Are you fucking kidding me? We have never had sex. Get that out of my face."),
            "ma_no_risk":  _("For what? You didn't cum in me. Do you even remember what we did?"),
            "ma_accept":   _("Give me that. And next time, pull out."),
        },
        "tenny": {
            "ma_offended": _("W-why are you giving me this? We never... d-do I look like that kind of girl to you?"),
            "ma_no_risk":  _("B-but you didn't finish inside... did you? I-I don't think I need it..."),
            "ma_accept":   _("Y-yes, please! I was so worried... thank you for thinking of it."),
        },
        # Shion (shion_family.rpy): contemptuous, in control; her own pill until her turn (girl_holds_her_pill)
        "shion": {
            "ma_offended":             _("A morning-after pill? From you? We have never... Get that out of my sight."),
            "ma_no_risk":              _("I'm on the pill, boy. I don't leave anything to chance. Least of all you."),
            "ma_accept":               _("Give it here. And not one word of this to your father."),
            "pill_refuse_own":         _("I have my own prescription. I don't take pills from boys."),
            "pill_stop_refuse_own":    _("You don't decide what goes in my body, boy. Not yet."),
            "pill_stop_accept_netori": _("You want me to stop? ...You want to put your baby in your father's wife. ...Fine. He'll think it's his."),
        },
    }
    _MA_GIRL_EXPR = {
        "gwen":  {"ma_offended": "laugh",   "ma_no_risk": "smirk",    "ma_accept": "serious"},
        "rogue": {"ma_offended": "worried", "ma_no_risk": "nervous",  "ma_accept": "worried"},
        "ntw":   {"ma_offended": "angry",   "ma_no_risk": "annoyed",  "ma_accept": "serious"},
        "tenny": {"ma_offended": "nervous", "ma_no_risk": "nervous",  "ma_accept": "worried"},
        "shion": {"ma_offended": "disgusted", "ma_no_risk": "smug", "ma_accept": "serious"},
    }

    # ============================================================
    # PLAYER KNOWLEDGE (discovery-gated) + PHONE FERTILITY APP DATA
    # ============================================================
    # The player only sees what he has discovered, like every other status screen:
    #   discovered_pill  : her birth control status (set by offering pills or asking her)
    #   discovered_cycle : her fertility cycle (set by asking her)
    # Both are plain Girl flags, so old saves need no migration.

    _FERT_PLAN_B_LIMIT = 3
    _FERT_PLAN_B_REGEN_DAYS = 30   # one used slot comes back every 30 days, counted from the first pill

    def _plan_b_register_use(girl):
        """She took a morning after pill. The regen clock starts with the first used slot."""
        _uses = getattr(girl, "_morning_after_uses", 0)
        if _uses <= 0:
            girl._morning_after_regen_day = store.Day
        girl._morning_after_uses = _uses + 1
        unlock_achievement("plan_b")
        print("[PREGNANCY] %s: plan B used (%d/%d), regen clock from Day %d" % (
            girl.gid, girl._morning_after_uses, _FERT_PLAN_B_LIMIT, getattr(girl, "_morning_after_regen_day", store.Day)))

    def _plan_b_next_slot_in(girl):
        """Days until her next used slot frees up (0 when nothing is used)."""
        if getattr(girl, "_morning_after_uses", 0) <= 0:
            return 0
        _anchor = getattr(girl, "_morning_after_regen_day", None)
        if _anchor is None:
            return _FERT_PLAN_B_REGEN_DAYS
        return max(0, _anchor + _FERT_PLAN_B_REGEN_DAYS - store.Day)

    def _plan_b_regen_tick(girl):
        """Daily: give back one slot per _FERT_PLAN_B_REGEN_DAYS. Pill on Day 5 -> slot back on Day 35."""
        _uses = getattr(girl, "_morning_after_uses", 0)
        if _uses <= 0:
            return
        # Saves from before the regen existed have uses but no clock: start it now
        if getattr(girl, "_morning_after_regen_day", None) is None:
            girl._morning_after_regen_day = store.Day
            return
        while _uses > 0 and store.Day - girl._morning_after_regen_day >= _FERT_PLAN_B_REGEN_DAYS:
            _uses -= 1
            girl._morning_after_regen_day += _FERT_PLAN_B_REGEN_DAYS
            print("[PREGNANCY] %s: plan B slot restored (%d/%d used)" % (girl.gid, _uses, _FERT_PLAN_B_LIMIT))
        girl._morning_after_uses = _uses
    _CHILD_SUPPORT_WEEKLY = 250   # per child. THE rule that uses it is child_support_due (children.rpy)
    # The part of it the PLAYER pays, by her family's money (author's rule, 2026-09-30): a rich family covers the
    # child support in full, a middle-class one (neither trait) half of it, a poor one none of it
    _CHILD_SUPPORT_PLAYER_SHARE = {"rich": 0.0, "poor": 1.0}
    _CHILD_SUPPORT_PLAYER_SHARE_MIDDLE = 0.5

    def _pregnancy_birth_day():
        return 65 if store._pregnancy_duration == "short" else 130

    def fert_knows_pill(girl):
        return girl.get_flag("discovered_pill")

    def fert_knows_cycle(girl):
        return girl.get_flag("discovered_cycle")

    def fert_learn(girl, what, source=""):
        """Player learns her birth control status ("pill") or her cycle ("cycle").
        Girl.discover() plays the sound and shows the banner the first time only."""
        _key = "discovered_" + what
        _was_new = not girl.get_flag(_key)
        girl.discover(_key)
        print("[FERTILITY] %s: player learns %s (source=%s new=%s)" % (girl.gid, what, source, _was_new))

    # Asking her straight out ("Are you on birth control?" / "When are your safe days?") is the
    # RISKY path: it is a very personal question. The natural ways to find out are chitchat hints
    # and what she says after you finish inside her (see FERTILITY HINTS below).
    # Per-girl entries only override the keys they list.
    #   *_love / *_obed : she answers once you are intimate (had sex with you, or dating)
    #   offend_love     : below this Love, asking with NO sexual history at all offends her
    _FERT_TELL_CONFIG = {
        "_default": {"pill_love": 450, "pill_obed": 600, "cycle_love": 650, "cycle_obed": 750, "offend_love": 500},
        "ntw":      {"pill_love": 650, "pill_obed": 800, "cycle_love": 800, "cycle_obed": 900, "offend_love": 650},
        "tenny":    {"pill_love": 350, "pill_obed": 400, "cycle_love": 550, "cycle_obed": 600, "offend_love": 350},
    }
    # Any "no" costs something: he pushed into her private life and she pushed back.
    _FERT_ASK_STATS = {
        "refuse":           {"Love": -3,  "Obed": -5},    # soft deny ("Nice try.")
        "offended":         {"Love": -10, "Obed": -8},    # hard deny
        "offended_partner": {"Love": -20, "Obed": -10},   # hard deny, she has a boyfriend / girlfriend
        "nag":              {"Love": -5,  "Obed": -5},    # asking again the same day after a "no"
    }

    def _fert_intimacy(girl):
        """How close the player is: "sex" (penetration), "acts" (anything else sexual), "none"."""
        _pen, _other = _fert_act_counts(girl)
        if _pen > 0:
            return "sex"
        return "acts" if _other > 0 else "none"

    def _fert_tell_check(girl, what):
        """Does she answer a direct question about her birth control ("pill") or cycle ("cycle")?
        Returns (outcome, reason) with outcome in "tell" / "refuse" / "offended" / "nag"."""
        if girl.get_flag("discovered_" + what):
            return ("tell", "already_known")

        # Same question again today after she already said no
        if store._fert_ask_day.get("%s_%s" % (girl.gid, what)) == store.Day:
            return ("nag", "asked_today")

        cfg = dict(_FERT_TELL_CONFIG["_default"])
        cfg.update(_FERT_TELL_CONFIG.get(girl.gid, {}))

        _intimacy = _fert_intimacy(girl)
        _dating = girl.is_dating_player()
        _has_partner = girl.has_npc_partner()

        # Never did anything with her and not her boyfriend: it is none of his business
        if _intimacy == "none" and not _dating:
            if _has_partner or girl.Love < cfg["offend_love"]:
                return ("offended", "partner" if _has_partner else "stranger")
            return ("refuse", "no_history")

        # Only her partner's business unless she is really into the player
        if _has_partner and _intimacy != "sex" and girl.Love < cfg[what + "_love"]:
            return ("offended", "partner")

        # The cycle is more private than the pill: it takes penetration or dating
        if what == "cycle" and _intimacy != "sex" and not _dating:
            return ("refuse", "not_intimate_enough")

        # Fear wants him careful, fetish loves the subject: both open up once intimate
        if girl.has_trait("pregnancy_fear") or girl.has_trait("pregnancy_fetish"):
            return ("tell", "trait")
        if girl.Love >= cfg[what + "_love"]:
            return ("tell", "love")
        if girl.Obed >= cfg[what + "_obed"]:
            return ("tell", "obed")
        return ("refuse", "low_stats")

    _FERT_ASK_EXPR = {
        "pill_yes": "normal",
        "pill_no": "worried",
        "pill_no_fetish": "smirk",
        "pill_refuse": "annoyed",
        "ask_offended": "angry",
        "ask_offended_partner": "angry",
        "ask_nag": "annoyed",
        "cycle_safe": "happy",
        "cycle_low": "thinking",
        "cycle_risky": "worried",
        "cycle_refuse": "annoyed",
        "infertile": "sad",
        "infertile_procedure": "looking_down",
        "pregnant_known": "neutral",
    }

    # Faces follow each girl's personality when she says no; anything not listed uses _FERT_ASK_EXPR.
    # Names MUST exist in POSE_EXPRESSIONS["standing"] (validated at init 1 below).
    #   ntw   : always the angriest
    #   tenny : flustered, never really angry
    #   gwen  : sarcastic, laughing at him for trying something that dumb this early
    #   rogue + any new girl: intentionally NOT listed. They use the _FERT_ASK_EXPR default
    #                         until the author decides a tone for them. Do not add entries on your own.
    _FERT_ASK_EXPR_GIRL = {
        "ntw": {
            "pill_refuse": "angry",
            "cycle_refuse": "angry",
            "ask_nag": "angry",
            "ask_offended": "disgusted",
            "ask_offended_partner": "disgusted",
        },
        "tenny": {
            "pill_refuse": "embarrassed",
            "cycle_refuse": "embarrassed",
            "ask_nag": "nervous",
            "ask_offended": "uncomfortable",
            "ask_offended_partner": "uncomfortable",
        },
        "gwen": {
            "pill_refuse": "smirk",
            "cycle_refuse": "smirk",
            "ask_nag": "bemused",
            "ask_offended": "laugh",
            "ask_offended_partner": "laugh",
        },
    }

    def _fert_ask_expr(girl, key):
        return _FERT_ASK_EXPR_GIRL.get(girl.gid, {}).get(key) or _FERT_ASK_EXPR.get(key, "normal")

    # Keyed by gid then answer key. Missing gid / key falls back to "_default".
    _FERT_ASK_LINES = {
        "_default": {
            "pill_yes":       _("Yes, I'm on the pill."),
            "pill_no":        _("No, I'm not on any birth control."),
            "pill_no_fetish": _("Pills? No way. I don't want anything getting in the way."),
            "pill_refuse":    _("That's a bit too personal for me."),
            "cycle_safe":     _("I should be in my safe days right now."),
            "cycle_low":      _("It's a low risk day, but not a safe one."),
            "cycle_risky":    _("These are my fertile days. It's the riskiest time."),
            "cycle_refuse":   _("I'd rather not talk about that with you."),
            "infertile":      _("I... can't have kids. The doctors told me years ago. So you don't need to worry about any of that."),
            # sterile since the procedure after her last birth (pregnancy_had_procedure), never "years ago"
            "infertile_procedure": _("After what happened at the birth, I can't get pregnant again. So none of that matters anymore."),
            "pregnant_known": _("I'm already pregnant, remember? It's kind of a moot point now."),
            "ask_offended":         _("Excuse me? That is none of your business."),
            "ask_offended_partner": _("I have a %(pl)s. Why on earth would I discuss that with you?"),
            "ask_nag":              _("I already said no. Drop it."),
        },
        "gwen": {
            "pill_yes":     _("Yeah, I'm on the pill. Have been for a while."),
            "pill_no":      _("No, I'm not on anything. So keep that in mind."),
            "pill_refuse":  _("Ha! You actually asked me that. Bold move. The answer is no."),
            "cycle_safe":   _("Let me think... I should be in my safe days right now."),
            "cycle_low":    _("I'm somewhere in between right now. Not the safest, not the worst."),
            "cycle_risky":  _("Honestly? These are my dangerous days. Be careful with me."),
            "cycle_refuse": _("I'm not handing you my calendar. Nice try."),
            "ask_offended":         _("Pfft, hahaha! We have done literally nothing and THAT is your question? Oh my god."),
            "ask_offended_partner": _("Hahaha, no. That's a question for my %(pl)s, and you are very much not my %(pl)s."),
            "ask_nag":              _("You're asking again? That's adorable. Still no."),
            "infertile_procedure":  _("Birth control? After the delivery room fiasco, I'm covered for life. One kid, no sequels."),
        },
        "rogue": {
            "pill_yes":     _("I'm on the pill, sugar. A girl's gotta be careful."),
            "pill_no":      _("I ain't on anything right now, sugar."),
            "pill_refuse":  _("Now that ain't somethin' you just ask a lady."),
            "cycle_safe":   _("Should be a safe stretch for me right now, darlin'."),
            "cycle_low":    _("It's a maybe kind of week. I wouldn't push my luck."),
            "cycle_risky":  _("Right now? Worst possible timing, sugar. I'm as fertile as it gets."),
            "cycle_refuse": _("My body's schedule is my business, sugar."),
            "ask_offended":         _("Excuse me?! You don't get to ask a girl that, sugar. Not you, not now."),
            "ask_offended_partner": _("I got a %(pl)s for that kinda talk, sugar. And it sure ain't you."),
            "ask_nag":              _("Asked and answered, sugar. Quit it."),
            "infertile_procedure":  _("Ain't no need for any of that now, sugar. Not since the birth. I can't carry another one."),
        },
        "ntw": {
            "pill_yes":     _("I'm on the pill. Obviously. Next question."),
            "pill_no":      _("No. And that's not an invitation."),
            "pill_refuse":  _("That is none of your damn business. Back off."),
            "cycle_safe":   _("Safe days. Don't make it weird."),
            "cycle_low":    _("Not safe, not terrible. Do the math yourself."),
            "cycle_risky":  _("Danger zone. So don't even think about it."),
            "cycle_refuse": _("You want my cycle schedule? Get lost."),
            "ask_offended":         _("What the hell kind of question is that? Get away from me."),
            "ask_offended_partner": _("That's my %(pl)s's business. Not yours. Never yours."),
            "ask_nag":              _("Ask me again and I walk."),
            "infertile_procedure":  _("Not needed. The birth took care of that for good. Next question."),
        },
        "tenny": {
            "pill_yes":     _("Y-yes, I take it every morning. I set an alarm and everything."),
            "pill_no":      _("N-no, I'm not taking anything like that..."),
            "pill_refuse":  _("T-that's really private... I don't want to talk about it."),
            "cycle_safe":   _("I-I track it in an app... it says I'm in my safe days right now."),
            "cycle_low":    _("The app says it's a low risk day. B-but low isn't zero..."),
            "cycle_risky":  _("The app has a big red warning today... it's my most fertile time."),
            "cycle_refuse": _("I-I'm too embarrassed to talk about that..."),
            "ask_offended":         _("W-what?! Why would you ask me that? That's so inappropriate..."),
            "ask_offended_partner": _("T-that's something only my %(pl)s should know... please don't ask me that."),
            "ask_nag":              _("P-please stop asking... I already said no."),
            "infertile_procedure":  _("I-I don't need to track any of that anymore... after the procedure, I can't get pregnant again."),
        },
    }

    def _fert_ask_line(girl, key):
        _line = _FERT_ASK_LINES.get(girl.gid, {}).get(key)
        if _line is None:
            _line = _FERT_ASK_LINES["_default"][key]
        return _line

    _FERT_CYCLE_ANSWER_KEY = {
        "safe": "cycle_safe",
        "low_risk": "cycle_low",
        "fertile": "cycle_risky",
        "peak": "cycle_risky",
    }

    def _fert_ask_answer(girl, what):
        """Resolve her answer to a direct question.
        Returns dict: outcome, key, line, expr, learn (flags to discover), love (stat change)."""
        _outcome, _reason = _fert_tell_check(girl, what)
        _tells = (_outcome == "tell")
        _stats_key = _outcome
        if _outcome == "offended":
            _partner = (_reason == "partner")
            _key = "ask_offended_partner" if _partner else "ask_offended"
            if _partner:
                _stats_key = "offended_partner"
            _learn = []
        elif _outcome == "nag":
            _key = "ask_nag"
            _learn = []
        elif _outcome == "refuse":
            _key = "%s_refuse" % what
            _learn = []
        elif girl._pregnant and girl._pregnancy_known:
            _key = "pregnant_known"
            _learn = [what]
        elif girl.has_trait("infertile"):
            # She knows, and once she opens up she tells the whole story (born that way, or the procedure)
            _key = "infertile_procedure" if pregnancy_had_procedure(girl) else "infertile"
            # Trait last: only the last banner stays on screen
            _learn = ["pill", "cycle", "trait_infertile"]
        elif what == "pill":
            if girl._on_pill:
                _key = "pill_yes"       # placebo included: she believes she is protected
            elif girl.has_trait("pregnancy_fetish"):
                _key = "pill_no_fetish"
            else:
                _key = "pill_no"
            _learn = ["pill"] + (["trait_pregnancy_fetish"] if _key == "pill_no_fetish" else [])
        else:
            # She reads her own calendar; she does not know about a breedable window
            _key = _FERT_CYCLE_ANSWER_KEY[get_cycle_phase(girl)]
            _learn = ["cycle"]

        _stats = dict(_FERT_ASK_STATS.get(_stats_key, {}))
        print("[FERTILITY] %s asked about %s: outcome=%s (%s) key=%s stats=%s" % (girl.gid, what, _outcome, _reason, _key, _stats))
        return {
            "outcome": _outcome,
            "tells": _tells,
            "key": _key,
            "line": _fert_ask_line(girl, _key),
            "expr": _fert_ask_expr(girl, _key),
            "learn": _learn,
            "stats": _stats,
        }

    _FERT_FERTILE_PHASES = ("fertile", "peak")

    def fert_app_data(girl):
        """Everything the phone Fertility app shows for one girl, already filtered to
        what the player has discovered. A pregnancy she has not found out about yet is
        never exposed: she keeps showing her regular cycle until the discovery event."""
        _knows_pill = fert_knows_pill(girl)
        _knows_cycle = fert_knows_cycle(girl)
        _breed_known = girl.has_trait("breedable") and girl.get_flag("discovered_trait_breedable")
        _infertile_known = girl.has_trait("infertile") and girl.get_flag("discovered_trait_infertile")

        d = {
            "knows_pill": _knows_pill,
            "knows_cycle": _knows_cycle,
            "plan_b_used": getattr(girl, "_morning_after_uses", 0),
            "plan_b_limit": _FERT_PLAN_B_LIMIT,
            "plan_b_next_in": _plan_b_next_slot_in(girl),
            "children": getattr(girl, "_children_count", 0),
            "support_weekly": child_support_due(girl),
            "support_share": child_support_player_share(girl),   # his part of it: 0 = her (rich) family pays all
            "child_age": child_age_label(girl),          # None when she has no child
            "raised_by": child_raised_by(girl),          # None unless her NPC partner stands as the father
            "breedable_known": _breed_known,
        }

        # ── State ──
        if getattr(girl, "_giving_birth", False):
            d["state"] = "away"
            d["away_days"] = max(0, getattr(girl, "_birth_return_day", 0) - store.Day)
        elif girl._pregnant and girl._pregnancy_known:
            _bd = _pregnancy_birth_day()
            d["state"] = "pregnant"
            d["preg_day"] = girl._pregnancy_day
            d["preg_total"] = _bd
            d["preg_stage"] = girl._pregnancy_stage
            d["due_in"] = max(0, _bd - girl._pregnancy_day)
        elif _infertile_known:
            if pregnancy_had_procedure(girl):
                d["state"] = "iud"
            else:
                d["state"] = "infertile"
        elif getattr(girl, "_pregnancy_cooldown", 0) > 0 or pregnancy_limit_reached(girl):
            d["state"] = "postpartum"
            d["cooldown"] = getattr(girl, "_pregnancy_cooldown", 0)
        else:
            d["state"] = "cycle"

        # ── Birth control ──
        if not _knows_pill:
            d["pill"] = "unknown"
        elif girl._on_pill and girl._on_placebo:
            d["pill"] = "placebo"
            d["pill_eff"] = 0
        elif girl._on_pill:
            d["pill"] = "on"
            d["pill_eff"] = int(round((1.0 - get_pill_effectiveness(girl)) * 100))
            d["pill_missed"] = getattr(girl, "_pill_missed", 0)
        else:
            d["pill"] = "off"

        # ── Cycle ──
        if _knows_cycle:
            _day = get_cycle_day(girl)
            _strip = [_cycle_phase_for_day(_i, _breed_known) for _i in range(1, 29)]
            _fertile_now = _strip[_day - 1] in _FERT_FERTILE_PHASES
            _flip = 0
            for _step in range(1, 29):
                _nd = ((_day - 1 + _step) % 28) + 1
                if (_strip[_nd - 1] in _FERT_FERTILE_PHASES) != _fertile_now:
                    _flip = _step
                    break
            d["cycle_day"] = _day
            d["cycle_strip"] = _strip
            d["cycle_phase"] = _strip[_day - 1]
            d["fertile_now"] = _fertile_now
            d["flip_days"] = _flip

        # ── Risk estimate (needs both pieces of knowledge) ──
        if d["state"] == "cycle" and _knows_pill and _knows_cycle:
            d["risk_inside"] = _calc_pregnancy_chance(girl, "inside", known_only=True) * 100.0
            d["risk_pullout"] = _calc_pregnancy_chance(girl, "pull_out", known_only=True) * 100.0

        return d

    def fert_player_data():
        """Player side of the Fertility app (vitamin, contraceptive stock) and of the player status page
        (CHILDREN block, child support in FINANCIALS). Pure and cheap: screens call it on every redraw."""
        _mothers = player_mothers()
        _children = sum(getattr(_g, "_children_count", 0) for _g in _mothers)
        return {
            "vitamin_active": getattr(store, "_player_fertility_vitamin_active", False),
            "vitamin_days": getattr(store, "_player_fertility_vitamin_days", 0),
            "vitamin_mult": ("%g" % _FERT_VITAMIN_MULT),
            "condoms": Player.get_item_count("condom") + Player.get_item_count("japanese_condom"),
            "pills": Player.get_item_count("birth_control"),
            "placebo": Player.get_item_count("placebo_pills"),
            "plan_b": Player.get_item_count("morning_after"),
            "children": _children,
            "support_weekly": child_support_total(),
            "support_next_in": child_support_next_in(),
            "mothers": [child_status_row(_g) for _g in _mothers],
        }

    def fert_pct_text(pct):
        if pct <= 0:
            return "0%"
        if pct < 1:
            return "<1%"
        return "%d%%" % int(round(pct))

    # ============================================================
    # IN-SCENE PREGNANCY LINES (spontaneous: by trait, protection state and girl)
    # ============================================================
    # scene_pick_line() resolves "first matching key wins" with the gid first, so plain modifiers
    # would either never play or take over every single moan. Instead this layer is asked FIRST
    # (one hook at the top of scene_pick_line) and answers only a share of the time.
    # Line pools live in pregnancy_lines.rpy: _FERT_SCENE_LINES[gid or "_default"]["<group>.<state>"].

    _FERT_ANAL_SCENES = _ANAL_SCENE_TYPES
    _FERT_NO_PENETRATION_SCENES = ("bj", "hj", "tj")
    _FERT_VAGINAL_SCENES = ("cowgirl", "reverse_cowgirl", "doggy", "laying_down", "full_nelson")

    # scene_pick_line base key -> line group
    _FERT_KEY_GROUP = {
        "moan.speed1": "moan",
        "moan.speed2": "moan",
        "moan.speed3": "moan",
        "cum_inside_accepted": "inside_ok",       # she agrees to a creampie / to losing the condom for one
        "cum_inside_denied": "inside_no",
        "cum_inside_consented": "inside_react",   # right after a creampie she wanted
        "cum_inside": "inside_react",
        "cum_inside_forced": "inside_forced",     # right after a creampie she did not want
        "creampie_aftermath": "aftermath",
        "cum_outside": "pull_out",
        "cum_condom": "cum_condom",
        "creampie_req": "creampie_req",           # spontaneous sub-events (SubEvents.rpy)
        "condom_ask": "condom_ask",
    }
    # Share (%) of those moments this layer takes over; the rest keep the regular trait pools
    _FERT_GROUP_CHANCE = {
        "moan": 15,
        "inside_ok": 70,
        "inside_no": 70,
        "inside_react": 70,
        "inside_forced": 70,
        "aftermath": 60,
        "pull_out": 60,
        "cum_condom": 60,
        "creampie_req": 70,
        "condom_ask": 70,
    }
    # Saying one of these out loud reveals something to the player
    _FERT_STATE_TRAIT = {
        "preg_fetish": "pregnancy_fetish",
        "preg_fetish_condom": "pregnancy_fetish",
        "preg_fear": "pregnancy_fear",
        "preg_fear_raw": "pregnancy_fear",
        "preg_fear_pill": "pregnancy_fear",
        "preg_fear_condom": "pregnancy_fear",
    }
    _FERT_STATE_REVEALS_PILL = ("on_pill", "no_protection", "preg_fear_pill", "preg_fear_raw")
    _fert_last_scene_line = {}   # gid -> last line, to avoid back-to-back repeats (not saved)

    def _fert_scene_states(girl):
        """What is on her mind about pregnancy right now, most specific first. [] = nothing to say.
        Uses what SHE believes: placebo counts as the pill, a stealth-removed or broken condom
        still counts as a condom."""
        if getattr(girl, "_pregnant", False) and getattr(girl, "_pregnancy_known", False):
            return ["pregnant_known"]
        # After the procedure pregnancy is off her mind for good: no fear, no breeding talk, no pill talk
        if pregnancy_had_procedure(girl):
            return []

        _condom = getattr(store, "condom_active", False)
        _pill = girl._on_pill
        _coerced = getattr(store, "_coercion_type", None) in ("blackmail", "financial")
        # Same comfort gate scene_lines.rpy uses for explicit personality traits
        _comfortable = (getattr(girl, "Love", 0) >= 300 or getattr(girl, "Inbt", 0) >= 200)

        if girl.has_trait("pregnancy_fetish"):
            # Breeding enthusiasm does not fit a blackmailed / paid scene (the teases have their own _coerced pools)
            if _coerced or not _comfortable:
                return []
            return ["preg_fetish_condom"] if _condom else ["preg_fetish"]
        if girl.has_trait("pregnancy_fear"):
            if _condom:
                return ["preg_fear_condom", "preg_fear"]
            if _pill:
                return ["preg_fear_pill", "preg_fear"]
            return ["preg_fear_raw", "preg_fear"]

        if _condom:
            return []               # status quo: the regular lines already cover it
        if girl.has_trait("infertile"):
            return []               # she knows she cannot conceive
        if _pill:
            return [] if (_coerced or not _comfortable) else ["on_pill"]
        if girl.has_trait("cum_slut"):
            return []               # plan section 8: she wants the cum and does not bring up pregnancy
        return ["no_protection"]

    def _fert_pick_scene_line(group, scene, girl):
        if girl is None or store._pregnancy_mode == "off":
            return None
        if scene not in _FERT_VAGINAL_SCENES:
            return None
        _all = globals().get("_FERT_SCENE_LINES", {})
        _pool, _state = None, None
        for _st in _fert_scene_states(girl):
            _pid = "%s.%s" % (group, _st)
            _pool = _all.get(girl.gid, {}).get(_pid) or _all.get("_default", {}).get(_pid)
            if _pool:
                _state = _st
                break
        if not _pool:
            return None
        if renpy.random.randint(1, 100) > _FERT_GROUP_CHANCE.get(group, 50):
            return None

        _last = _fert_last_scene_line.get(girl.gid)
        _choices = [_l for _l in _pool if _l != _last] or list(_pool)
        _line = renpy.random.choice(_choices)
        _fert_last_scene_line[girl.gid] = _line

        _trait = _FERT_STATE_TRAIT.get(_state)
        if _trait:
            girl.discover("discovered_trait_" + _trait)
        if _state in _FERT_STATE_REVEALS_PILL:
            fert_learn(girl, "pill", "scene_line")
        print("[FERTILITY] %s scene line: group=%s state=%s scene=%s" % (girl.gid, group, _state, scene))
        return _line

    def fert_scene_line(key, scene, girl):
        """Hook for scene_pick_line(): a pregnancy-aware line for this moment, or None."""
        _group = _FERT_KEY_GROUP.get(key)
        if not _group:
            return None
        return _fert_pick_scene_line(_group, scene, girl)

    def fert_override_line(girl, scene, group, fallback):
        """For the few flows that still pick from inline pools (Cum.rpy "Warn her")."""
        return _fert_pick_scene_line(group, scene, girl) or fallback

    # ============================================================
    # TRUTH FILTER: lines from other systems that claim something about her pill / cycle
    # ============================================================
    # Pools written before this system said "I'm not on the pill!" or "today is NOT safe!" no matter
    # what. A line listed in _FERT_LINE_CLAIMS only plays while its claim is TRUE (what SHE believes: a
    # placebo counts as the pill), and hearing it teaches the player that fact, the natural way.
    # Pick points: scene_pick_line() and the tease reaction. Key = the English source line.
    def _fert_claim_not_on_pill(girl):
        return not girl._on_pill

    def _fert_claim_on_pill(girl):
        return bool(girl._on_pill)

    def _fert_claim_unsafe_today(girl):
        return (not girl._on_pill) and get_cycle_phase(girl) in ("fertile", "peak")

    def _fert_claim_safe_today(girl):
        return get_cycle_phase(girl) in ("safe", "low_risk")

    # claim id -> (is it true for her right now?, what the player learns on hearing it)
    _FERT_CLAIMS = {
        "not_on_pill":  (_fert_claim_not_on_pill, "pill"),
        "on_pill":      (_fert_claim_on_pill, "pill"),
        "unsafe_today": (_fert_claim_unsafe_today, "cycle"),
        "safe_today":   (_fert_claim_safe_today, "cycle"),
    }
    _FERT_LINE_CLAIMS = {
        # scene_lines.rpy  cum_inside.nerd
        "You... inside?! I'm not on the pill! Why would you do that?!": "not_on_pill",
        "Did you just... inside me?! I'm not safe right now! This is bad!": "unsafe_today",
        # tease.rpy  cum_threat / breed_talk (the old breed_threat lines live there), nerd reactions
        "I tracked my cycle and today is NOT safe! Do you even understand biology?!": "unsafe_today",
        "I calculated the probability and it's way too high. Pull out!": "unsafe_today",
        "This is the WORST time in my cycle! You CAN'T do this!": "unsafe_today",
        "The probability of conception right now is... no, STOP!": "unsafe_today",
        "The pill is 99 percent effective, and I refuse to be the other 1 percent! Pull out!": "on_pill",
        "My chart says today is a low risk day, and that is still NOT permission!": "safe_today",
        "I take my pill at the same minute every day precisely so THIS can't happen!": "on_pill",
        "Statistically I'm in my safe window, but I am not testing that hypothesis with you!": "safe_today",
    }

    def fert_pick_truthful(girl, lines):
        """random.choice(lines) without the lines whose pill / cycle claim is false for her right now
        (all claim lines are dropped while pregnancy is off, and after her procedure: every claim is a
        way of saying "I could get pregnant"). If nothing is left the full pool is
        used and nothing is learned, so a pool can never come back empty."""
        _lines = list(lines or [])
        if not _lines:
            return None
        if girl is None:
            return renpy.random.choice(_lines)
        _off = store._pregnancy_mode == "off" or pregnancy_had_procedure(girl)
        _ok = []
        for _l in _lines:
            _claim = _FERT_LINE_CLAIMS.get(_l)
            if _claim is None or (not _off and _FERT_CLAIMS[_claim][0](girl)):
                _ok.append(_l)
        if not _ok:
            print("[FERTILITY] %s: every line of the pool makes a false claim, using it unfiltered" % girl.gid)
            return renpy.random.choice(_lines)
        _line = renpy.random.choice(_ok)
        _claim = _FERT_LINE_CLAIMS.get(_line)
        if _claim:
            print("[FERTILITY] %s: claim line spoken (%s), dropped %d false line(s)" % (girl.gid, _claim, len(_lines) - len(_ok)))
            fert_learn(girl, _FERT_CLAIMS[_claim][1], "claim_line:" + _claim)
        return _line

    # ============================================================
    # CUM PERMISSION: pill / traits / already pregnant (plan section 11.1)
    # ============================================================
    # Added to CumPermissionCheck()'s bonus for the asks that end in a raw vaginal creampie.
    # Deliberately softer than the plan (+250 / -350 / -600): most girls start OFF the pill, so the
    # plan's numbers would wall off creampies for nearly everyone. Tune here while playtesting.
    # For scale: never-went-raw is -350, cum_slut +500, hate_cum -400, hardcore_sex +200.
    _FERT_PERMISSION_ACTIONS = ("cum_inside_ask", "cum_remove_condom_ask", "condom_remove_midscene")
    _FERT_PERMISSION_BONUS = {
        "pregnant_known": 150,        # nothing left to lose
        "fetish": 200,                # she wants the baby
        "infertile": 150,             # she knows she cannot conceive
        "fear_on_pill": 50,           # trusts the pill, barely
        "fear_no_protection": -400,   # her worst nightmare
        "on_pill": 150,               # placebo included: she believes she is covered
        "no_protection": -150,        # she can actually get pregnant
    }

    def _fert_permission_state(girl):
        if getattr(girl, "_pregnant", False) and getattr(girl, "_pregnancy_known", False):
            return "pregnant_known"
        if girl.has_trait("pregnancy_fetish"):
            return "fetish"
        if girl.has_trait("infertile"):
            return "infertile"
        if girl.has_trait("pregnancy_fear"):
            return "fear_on_pill" if girl._on_pill else "fear_no_protection"
        return "on_pill" if girl._on_pill else "no_protection"

    def fert_cum_permission_bonus(girl, action):
        """Hook for CumPermissionCheck(). Anal asks use their own action and are never touched."""
        if store._pregnancy_mode == "off" or action not in _FERT_PERMISSION_ACTIONS:
            return 0
        _state = _fert_permission_state(girl)
        _bonus = _FERT_PERMISSION_BONUS.get(_state, 0)
        print("[FERTILITY] %s cum permission: action=%s state=%s bonus=%+d" % (girl.gid, action, _state, _bonus))
        return _bonus

    # ============================================================
    # BREEDING KINK WON'T LET HIM PULL OUT (plan section 17)
    # ============================================================
    # Reuses Cum.rpy's forced-creampie flow (_player_resist_forced_cum, auto-resist by strength / Obed).
    # pregnancy_fetish always comes with cum_slut, so that flow already exists for her; this only gives
    # her an earlier trigger ("breed" force type) and breeding lines instead of the cum_slut ones.
    _FERT_BREED_FORCE_MIN_CREAMPIES = 2   # cum_slut alone only starts forcing at 5

    def fert_breed_active(girl, scene_type):
        """Is her breeding kink driving this cum moment? (vaginal, not already pregnant, not coerced)"""
        if store._pregnancy_mode == "off" or girl is None:
            return False
        if not girl.has_trait("pregnancy_fetish") or scene_type not in _FERT_VAGINAL_SCENES:
            return False
        if getattr(girl, "_pregnant", False) and getattr(girl, "_pregnancy_known", False):
            return False
        if pregnancy_had_procedure(girl):
            return False   # she knows there is no baby to beg for any more (her cum_slut flow still exists)
        return getattr(store, "_coercion_type", None) not in ("blackmail", "financial")

    def fert_breed_force_type(girl, scene_type):
        """"breed" when she will try to keep him inside, else None."""
        if fert_breed_active(girl, scene_type) and getattr(girl, "CreampieCounts", 0) >= _FERT_BREED_FORCE_MIN_CREAMPIES:
            print("[FERTILITY] %s: breeding kink forces creampie (creampies=%d)" % (girl.gid, girl.CreampieCounts))
            return "breed"
        return None

    # Shared by all girls, like the cum_slut pools of this flow in Cum.rpy
    _FERT_BREED_LINES = {
        "beg": [
            _("Please... cum inside. I want you to get me pregnant..."),
            _("Don't pull out this time... I want your baby so bad..."),
            _("Do it inside... make me a mom..."),
        ],
        "followup": [
            _("YES! Breed me! Put a baby in me!"),
            _("Every drop! Get me pregnant!"),
            _("Deeper! I want to feel you knock me up!"),
        ],
        "despair": [
            _("No! Please! I want your baby, don't pull out!"),
            _("Wait! Don't waste it! I need you to get me pregnant!"),
            _("Please reconsider! I'm begging you, breed me!"),
        ],
        "relief": [
            _("Yes! Thank you! Get me pregnant!"),
            _("Oh god, yes! Put a baby in me!"),
        ],
        "ignored": [
            _("You pulled out... I wanted your baby so badly..."),
            _("All of it, wasted... how am I supposed to get pregnant like this..."),
            _("I begged you to breed me and you still pulled out..."),
        ],
    }

    def fert_debug(girl=None):
        """Console helper: fert_debug(Gwen) -> one line per fact about her pregnancy state and
        the creampie odds RIGHT NOW (true values, ignoring what the player knows).
        fert_debug() with no girl prints every girl."""
        if girl is None:
            return "\n\n".join(fert_debug(_g) for _g in ALL_GIRLS)
        _pill = "placebo (she thinks it is real)" if (girl._on_pill and girl._on_placebo) else ("yes" if girl._on_pill else "no")
        _lines = [
            "%s (Day %d, mode=%s, duration=%s)" % (girl.Name, store.Day, store._pregnancy_mode, store._pregnancy_duration),
            "  pregnant: %s  known: %s  day: %d  stage: %d  discovery_day: %d" % (
                girl._pregnant, girl._pregnancy_known, girl._pregnancy_day, girl._pregnancy_stage, getattr(girl, "_pregnancy_discovery_day", 0)),
            "  giving_birth: %s  cooldown: %d  count: %d  children: %d  postpartum: %s" % (
                getattr(girl, "_giving_birth", False), getattr(girl, "_pregnancy_cooldown", 0), getattr(girl, "_pregnancy_count", 0),
                getattr(girl, "_children_count", 0), getattr(girl, "_postpartum", False)),
            "  cycle day: %d/28  phase: %s  (base %.0f%%)" % (get_cycle_day(girl), get_cycle_phase(girl), get_cycle_base_chance(girl) * 100),
            "  pill: %s  missed: %d  effectiveness mult: %.2f" % (_pill, getattr(girl, "_pill_missed", 0), get_pill_effectiveness(girl)),
            "  traits: %s  vitamin: %s  condom on now: %s" % (
                ", ".join(sorted(_t for _t in ("breedable", "infertile", "pregnancy_fetish", "pregnancy_fear") if girl.has_trait(_t))) or "none",
                getattr(store, "_player_fertility_vitamin_active", False), getattr(store, "condom_active", False)),
            "  creampie chance NOW: %.1f%%   pull-out: %.1f%%" % (
                _calc_pregnancy_chance(girl, "inside") * 100, _calc_pregnancy_chance(girl, "pull_out") * 100),
            "  plan B used: %d/%d (next slot in %d days)   player knows pill/cycle: %s/%s" % (
                getattr(girl, "_morning_after_uses", 0), _FERT_PLAN_B_LIMIT, _plan_b_next_slot_in(girl), fert_knows_pill(girl), fert_knows_cycle(girl)),
        ]
        _lines.append("  births: %d/%d  procedure: %s (removed traits: %s)  told him: %s" % (
            getattr(girl, "_pregnancy_count", 0), _PREGNANCY_MAX_BIRTHS, pregnancy_had_procedure(girl),
            ", ".join(getattr(girl, "_birth_procedure_removed", None) or ()) or "none", girl.get_flag("discovered_trait_" + _PROCEDURE_TRAIT)))
        if girl._pregnant or getattr(girl, "_pregnancy_cooldown", 0) > 0 or pregnancy_limit_reached(girl):
            _lines.append("  NOTE: creampie chance is 0 in practice (already pregnant / cooldown / birth limit reached)")
        if girl_is_mother(girl):
            _lines.append("  child: age %s days (%s)  support $%d / week  partner fooled: %s  records: %s" % (
                child_age_days(girl), child_age_tier(girl), child_support_due(girl), child_father_fooled(girl), getattr(girl, "_children", None)))
        _out = "\n".join(_lines)
        print("[FERTILITY] debug\n" + _out)
        return _out

    def fert_breed_pool(girl, scene_type, key, fallback):
        """Swap one of Cum.rpy's inline cum_slut pools for the breeding version when her kink is active."""
        if fert_breed_active(girl, scene_type):
            _pool = _FERT_BREED_LINES.get(key)
            if _pool:
                girl.discover("discovered_trait_breedable")   # she is begging to be bred out loud
                return _pool
            return fallback
        return fallback

# ============================================================
# PHASE 4 LABELS: PILL OFFER / STOP / MORNING AFTER
# ============================================================

label _pill_offer(girl, pill_item=None):
    # pill_item: "birth_control" or "placebo_pills" (chosen in the Give her... menu).
    # Without it (older callers) she is offered whatever the player carries.
    python:
        _has_real = Player.get_item_count("birth_control") > 0
        _has_placebo = Player.get_item_count("placebo_pills") > 0
        if pill_item is None:
            pill_item = "birth_control" if _has_real else ("placebo_pills" if _has_placebo else None)

    if pill_item is None or Player.get_item_count(pill_item) <= 0:
        return

    $ _pill_type = (pill_item == "placebo_pills")
    $ Player.remove_item(pill_item, 1)

    $ _pill_result = _pill_offer_check(girl, is_placebo=_pill_type)
    $ _pill_key = _pill_result["key"]
    $ _pill_line = _pill_line_for(girl, _pill_key)

    # Face first, then the line, then the stat popups (all from _PILL_REACTION)
    $ set_scene_expression(girl, _pill_expr(girl, _pill_key))
    $ Say_Line(girl, _format_partner_line(girl, _pill_line))
    $ _pill_react(girl, _pill_key)

    if _pill_result["result"] in ("offended", "refuse", "stash"):
        # She did not keep them (stash: she already has her own)
        $ Player.add_item(pill_item, 1)
        $ print("[PREGNANCY] %s: pill offer -> %s (%s), item returned" % (girl.gid, _pill_result["result"], _pill_key))
    else:
        $ print("[PREGNANCY] %s: pill offer -> %s (%s), on_pill=%s on_placebo=%s" % (girl.gid, _pill_result["result"], _pill_key, girl._on_pill, girl._on_placebo))

    # He only learns her pill status when her line made it explicit (see "reveals" in _PILL_REACTION)
    if _PILL_REACTION.get(_pill_key, {}).get("reveals", False):
        $ fert_learn(girl, "pill", "pill_offer")

    # She said yes and starts them: shown after fert_learn, so it takes the place of the "status discovered" banner
    if _pill_result["result"] == "accept":
        $ _pill_change_banner(girl, True)

    # After a bad reaction she keeps the face while the losses pop up
    if _pill_result["result"] not in ("offended", "refuse"):
        $ set_scene_expression(girl, "normal")
    return

# ============================================================
# ASK HER: birth control / cycle (discovery for the phone Fertility app)
# ============================================================

# {"<gid>_<pill|cycle>": Day she last said no}. Saved; `default` also covers old saves.
default _fert_ask_day = {}

label _ask_fertility(girl, what):
    if what == "pill":
        $ Say_Player(_("Are you on birth control?"))
    else:
        $ Say_Player(_("When are your safe days?"))

    $ _fa = _fert_ask_answer(girl, what)
    $ set_scene_expression(girl, _fa["expr"])
    # Partner lines carry %(pl)s and friends; _format_partner_line also translates
    $ Say_Line(girl, _format_partner_line(girl, _fa["line"]))

    python:
        for _fa_what in _fa["learn"]:
            fert_learn(girl, _fa_what, "asked_" + what)
        for _fa_stat, _fa_amt in _fa["stats"].items():
            Change_Status(girl, _fa_stat, _fa_amt)
        if not _fa["tells"]:
            # A "no" sticks for the rest of the day: asking again only annoys her
            store._fert_ask_day["%s_%s" % (girl.gid, what)] = store.Day

    # After a "no" she keeps the annoyed / angry face while the stat losses pop up
    if _fa["tells"]:
        $ set_scene_expression(girl, "normal")
    return

label _pill_stop_request(girl):
    $ Say_Player(_("Hey, I was thinking... maybe you should stop taking the pill."))

    $ _stop_result = _pill_stop_check(girl)
    $ _stop_key = _stop_result["key"]
    $ _stop_line = _PILL_DIALOGUE.get(_stop_key, "...")

    $ set_scene_expression(girl, _PILL_REACTION.get(_stop_key, {}).get("expr", "normal"))
    $ Say_Line(girl, _(_stop_line))
    $ _pill_react(girl, _stop_key)

    if _stop_result["result"] == "accept":
        python:
            _dating = girl.is_dating_player()
            if not (girl.has_trait("pregnancy_fetish") or (girl.Love >= 800 and _dating)):
                Change_Status(girl, "Love", -10)
            print("[PREGNANCY] %s: pill stop -> accepted (%s)" % (girl.gid, _stop_key))
            _pill_change_banner(girl, False)
        $ set_scene_expression(girl, "normal")
    else:
        $ print("[PREGNANCY] %s: pill stop -> refused (%s)" % (girl.gid, _stop_key))

    return

label _morning_after_offer(girl):
    $ _ma_result = _morning_after_check(girl)
    $ _ma_key = _ma_result["key"]
    $ _ma_line = _pill_line_for(girl, _ma_key)

    $ set_scene_expression(girl, _pill_expr(girl, _ma_key))
    $ Say_Line(girl, _(_ma_line))
    $ _pill_react(girl, _ma_key)

    if _ma_result["result"] == "accept":
        python:
            Player.remove_item("morning_after", 1)
            _plan_b_register_use(girl)
            # 85% chance to prevent pregnancy
            if girl._pregnant and girl._pregnancy_day <= 2:
                if renpy.random.random() < 0.85:
                    girl._pregnant = False
                    girl._pregnancy_day = 0
                    girl._pregnancy_stage = 0
                    print("[PREGNANCY] %s: morning after SUCCESS, pregnancy prevented" % girl.gid)
                else:
                    print("[PREGNANCY] %s: morning after FAILED, pregnancy continues" % girl.gid)
            else:
                # Clear any pending risks
                _cleared = 0
                _new_risks = []
                for _r in store._scene_pregnancy_risks:
                    if _r["gid"] == girl.gid:
                        _cleared += 1
                    else:
                        _new_risks.append(_r)
                store._scene_pregnancy_risks = _new_risks
                print("[PREGNANCY] %s: morning after used, cleared %d pending risks (uses=%d)" % (girl.gid, _cleared, girl._morning_after_uses))
        $ set_scene_expression(girl, "normal")
    else:
        # She keeps the face while the stat losses pop up; the pill stays with the player
        $ print("[PREGNANCY] %s: morning after -> %s (%s)" % (girl.gid, _ma_result["result"], _ma_key))

    return

# ============================================================
# FERTILITY HINTS: the natural way to learn about her pill / cycle
#   1. Chitchat: side effects of the pill, mood swings on her period, mid-cycle restlessness
#   2. Action: what she blurts out after you finish inside her without a condom
# init 1: register_chitchat() lives in Chat/ChitChat.rpy, which loads after this file.
# ============================================================
init 1 python:

    _FERT_PERIOD_DAYS = (1, 5)       # cycle days she is on her period
    _FERT_OVULATION_DAYS = (14, 16)  # same window as the "peak" phase

    # Keyed by gid then hint key. Missing gid / key falls back to "_default".
    _FERT_HINT_LINES = {
        "_default": {
            "chat_pill_on":    _("My skin has been breaking out lately. {hint}Side effect of something new I started taking{/hint}, I guess."),
            "chat_pill_off":   _("A friend keeps telling me to get on the pill. {hint}I never have{/hint}. I don't like messing with my hormones."),
            "chat_period":     _("Sorry if I'm moody today. {hint}It's that time of the month{/hint}."),
            "chat_ovulation":  _("I don't know what's with me this week. {hint}I feel restless, warm, distracted{/hint}..."),
            "remark_pill_on":  _("Relax. {hint}I'm on the pill{/hint}."),
            "remark_pill_off": _("You do realize {hint}I'm not on any birth control{/hint}, right?"),
            "remark_cycle_safe":   _("Good thing {hint}these are my safe days{/hint}."),
            "remark_cycle_danger": _("That was reckless. {hint}These are my fertile days{/hint}."),
            # pregnancy_fetish on a fertile day: she is thrilled, not worried
            "remark_cycle_danger_fetish": _("Mmm... perfect timing. {hint}These are my most fertile days{/hint}."),
        },
        "gwen": {
            "chat_pill_on":    _("Ugh, look at this. Pimples. At my age. {hint}It's those new hormones I'm on{/hint}, I swear."),
            "chat_pill_off":   _("My roommate swears by the pill. {hint}I've never taken it{/hint}. Putting hormones in my body freaks me out."),
            "chat_period":     _("I cried at a dog food commercial this morning. A COMMERCIAL. {hint}My hormones are a mess this week{/hint}."),
            "chat_ovulation":  _("Is it me or is everyone hot this week? {hint}I get like this once a month{/hint}. It's embarrassing."),
            "remark_pill_on":  _("Don't look so worried. {hint}I take the pill{/hint} every morning."),
            "remark_pill_off": _("Just so you know, {hint}I'm not on the pill{/hint}. That was a gamble."),
            "remark_cycle_safe":   _("Good thing {hint}it's a safe day{/hint}... I think."),
            "remark_cycle_danger": _("That was risky. {hint}I'm right in my fertile window{/hint}, you know."),
        },
        "rogue": {
            "chat_pill_on":    _("My skin's actin' up somethin' awful. {hint}Doctor said the new pills might do that{/hint} for a month or two."),
            "chat_pill_off":   _("Girls in my dorm are all poppin' those little pills every mornin'. {hint}Not me, I never bothered{/hint}."),
            "chat_period":     _("Don't mind me, sugar. I'm all weepy and cranky and {hint}my cramps are killin' me{/hint}. Give it a few days."),
            "chat_ovulation":  _("I been feelin' real... energetic this week, sugar. {hint}Happens to me mid-month, every month{/hint}."),
            "remark_pill_on":  _("Easy, sugar. {hint}The pill's got me covered{/hint}."),
            "remark_pill_off": _("Sugar, {hint}I ain't on the pill{/hint}. You might wanna remember that next time."),
            "remark_cycle_safe":   _("Lucky for you, {hint}the timing's safe{/hint} this week."),
            "remark_cycle_danger": _("Lord... of all the days. {hint}This is my fertile week{/hint}!"),
        },
        "ntw": {
            "chat_pill_on":    _("If you mention the zit on my chin, I'll end you. {hint}It's a side effect of my prescription{/hint}. Moving on."),
            "chat_pill_off":   _("Everyone keeps pushing pills on me. Vitamins, hormones, whatever. {hint}I don't take any of it{/hint}."),
            "chat_period":     _("I want chocolate and I want to punch something. {hint}Once a month, like clockwork{/hint}. Don't comment."),
            "chat_ovulation":  _("Stop looking at me. {hint}My body does this stupid thing mid-cycle{/hint} and you are not helping."),
            "remark_pill_on":  _("Stop staring. {hint}I'm on the pill{/hint}. I'm not an idiot."),
            "remark_pill_off": _("{hint}I'm not on the pill{/hint}, genius. Think about that."),
            "remark_cycle_safe":   _("{hint}Safe days{/hint}. You got lucky."),
            "remark_cycle_danger": _("You're an idiot. {hint}I'm ovulating{/hint} right now."),
        },
        "tenny": {
            "chat_pill_on":    _("I-I've been breaking out... I read the leaflet and {hint}it's a common side effect in the first months{/hint}."),
            "chat_pill_off":   _("T-the campus clinic offered me a prescription for... you know... {hint}but I never picked it up{/hint}. I was too embarrassed."),
            "chat_period":     _("I-I got emotional in class over nothing... {hint}it always happens around this time of the month{/hint}. Sorry..."),
            "chat_ovulation":  _("M-my app says {hint}it's my peak week{/hint}... it explains why I can't concentrate on anything..."),
            "remark_pill_on":  _("I-it's okay... {hint}I take my pill every morning{/hint}, so we should be fine."),
            "remark_pill_off": _("B-but {hint}I'm not taking any pills{/hint}... what if something happens?"),
            "remark_cycle_safe":   _("I-it should be okay... {hint}my app says today is a safe day{/hint}."),
            "remark_cycle_danger": _("Oh no, oh no... {hint}my app said today is a high risk day{/hint}!"),
        },
    }

    # What the player works out from the hint (narration, skipped on the phone)
    _FERT_HINT_THOUGHT = {
        "chat_pill_on":   _("A new prescription with skin side effects... She is probably on the pill."),
        "chat_pill_off":  _("Sounds like she isn't on any birth control."),
        "chat_period":    _("That time of the month. You make a mental note of the date."),
        "chat_ovulation": _("Mid-cycle. You make a mental note of the date."),
    }

    _FERT_HINT_EXPR = {
        "chat_pill_on": "annoyed",
        "chat_pill_off": "normal",
        "chat_period": "sad",
        "chat_ovulation": "shy",
        "remark_pill_on": "normal",
        "remark_pill_off": "worried",
        "remark_cycle_safe": "normal",
        "remark_cycle_danger": "worried",
        "remark_cycle_danger_fetish": "lusty",
        "pill_no_fetish": "smirk",
        "cycle_low": "thinking",
    }

    # set_scene_expression() silently shows a neutral face for unknown names, so catch typos at startup.
    # Core_Images.rpy loads after this file, hence the check lives in this init 1 block.
    def _fert_validate_claim_lines():
        """A claim line that was reworded in its pool silently stops being filtered: warn at startup."""
        _seen = set()
        def _walk(_o):
            if isinstance(_o, dict):
                for _v in _o.values():
                    _walk(_v)
            elif isinstance(_o, (list, tuple)):
                for _v in _o:
                    _walk(_v)
            elif isinstance(_o, str):
                _seen.add(_o)
        _walk(globals().get("SCENE_LINES", {}))
        _walk(globals().get("TEASE_OPTIONS", {}))
        if not _seen:
            return
        for _l in _FERT_LINE_CLAIMS:
            if _l not in _seen:
                print("[FERTILITY] WARNING claim line not found in SCENE_LINES / TEASE_OPTIONS: %r" % _l)
    _fert_validate_claim_lines()

    def _fert_validate_expressions():
        _valid = POSE_EXPRESSIONS.get("standing", {})
        _used = set(_FERT_ASK_EXPR.values()) | set(_FERT_HINT_EXPR.values())
        _used |= set(_r.get("expr", "normal") for _r in _PILL_REACTION.values())
        for _per_girl in list(_FERT_ASK_EXPR_GIRL.values()) + list(_MA_GIRL_EXPR.values()):
            _used |= set(_per_girl.values())
        _bad = sorted(_e for _e in _used if _e not in _valid)
        if _bad:
            print("[FERTILITY] INVALID expression names (will render neutral): %s" % ", ".join(_bad))
        return _bad

    _fert_validate_expressions()

    def _fert_hint_line(girl, key):
        _line = _FERT_HINT_LINES.get(girl.gid, {}).get(key)
        if _line is None:
            _line = _FERT_HINT_LINES["_default"].get(key)
        if _line is None:
            _line = _fert_ask_line(girl, key)   # keys shared with the direct answers
        return _line

    def _fert_say_hint(girl, key):
        set_scene_expression(girl, _FERT_HINT_EXPR.get(key, "normal"))
        Say_Line(girl, _fert_hint_line(girl, key))
        if "fetish" in key and girl.has_trait("pregnancy_fetish"):
            girl.discover("discovered_trait_pregnancy_fetish")   # "I don't want anything getting in the way"
        _thought = _FERT_HINT_THOUGHT.get(key)
        if _thought:
            Narration(_thought)
        set_scene_expression(girl, "normal")

    # ── 1. Chitchat ──

    def _fert_in_days(girl, span):
        return span[0] <= get_cycle_day(girl) <= span[1]

    def _fert_chat_base_ok(girl):
        if store._pregnancy_mode == "off":
            return False
        if getattr(girl, "_pregnant", False) and getattr(girl, "_pregnancy_known", False):
            return False
        return getattr(girl, "Love", 0) >= 200

    def _fert_chat_pill_ok(girl, loc, t_index):
        return _fert_chat_base_ok(girl) and not fert_knows_pill(girl)

    def _fert_chat_cycle_ok(girl, loc, t_index):
        # A pregnant girl (even one who does not know yet) has no period to complain about
        if not _fert_chat_base_ok(girl) or fert_knows_cycle(girl) or getattr(girl, "_pregnant", False):
            return False
        return _fert_in_days(girl, _FERT_PERIOD_DAYS) or _fert_in_days(girl, _FERT_OVULATION_DAYS)

    def chitchat_hint_pill(girl, loc, t_index):
        _fert_say_hint(girl, "chat_pill_on" if girl._on_pill else "chat_pill_off")
        fert_learn(girl, "pill", "chitchat")
        Change_Status(girl, "Love", 1)

    def chitchat_hint_cycle(girl, loc, t_index):
        _fert_say_hint(girl, "chat_period" if _fert_in_days(girl, _FERT_PERIOD_DAYS) else "chat_ovulation")
        fert_learn(girl, "cycle", "chitchat")
        Change_Status(girl, "Love", 1)

    register_chitchat("global", chitchat_hint_pill, condition=_fert_chat_pill_ok, weight=2)
    # Narrow window (8 days out of 28), so it gets a higher weight when it is available
    register_chitchat("global", chitchat_hint_cycle, condition=_fert_chat_cycle_ok, weight=4)

    # ── 2. After finishing inside her without a condom ──

    # Chance (%) that she brings it up. Highest matching value wins.
    _FERT_REMARK_TRAIT_CHANCE = {"pregnancy_fear": 80, "pregnancy_fetish": 60}
    _FERT_REMARK_LOVE_CHANCE = ((700, 50), (400, 30), (0, 10))
    _FERT_REMARK_LESBIAN_CAP = 15
    _FERT_RAW_INSIDE_TYPES = ("inside", "condom_removed_inside")
    _FERT_REMARK_CYCLE_KEY = {
        "safe": "remark_cycle_safe",
        "low_risk": "cycle_low",
        "fertile": "remark_cycle_danger",
        "peak": "remark_cycle_danger",
    }

    def _fert_remark_chance(girl):
        _chance = 0
        for _min_love, _pct in _FERT_REMARK_LOVE_CHANCE:
            if girl.Love >= _min_love:
                _chance = _pct
                break
        if girl.has_trait("lesbian"):
            _chance = min(_chance, _FERT_REMARK_LESBIAN_CAP)
        for _trait, _pct in _FERT_REMARK_TRAIT_CHANCE.items():
            if girl.has_trait(_trait):
                _chance = max(_chance, _pct)
        return _chance

    def fert_scene_remark(girl):
        """Scene end, BEFORE the pregnancy rolls clear the risk list: if the player finished
        inside her without protection this scene, she may blurt out where she stands.
        One remark per scene: birth control first, her cycle once that is known."""
        if store._pregnancy_mode == "off" or girl is None:
            return
        if getattr(girl, "_pregnant", False) and getattr(girl, "_pregnancy_known", False):
            return
        _raw_inside = [_r for _r in store._scene_pregnancy_risks
                       if _r["gid"] == girl.gid and _r["type"] in _FERT_RAW_INSIDE_TYPES]
        if not _raw_inside:
            return
        if fert_knows_pill(girl) and fert_knows_cycle(girl):
            return

        _chance = _fert_remark_chance(girl)
        _roll = renpy.random.randint(1, 100)
        print("[FERTILITY] %s scene remark: chance=%d roll=%d" % (girl.gid, _chance, _roll))
        if _roll > _chance:
            return

        if not fert_knows_pill(girl):
            if girl._on_pill:
                _key = "remark_pill_on"      # placebo included: she believes she is protected
            elif girl.has_trait("pregnancy_fetish"):
                _key = "pill_no_fetish"
            else:
                _key = "remark_pill_off"
            _what = "pill"
        else:
            _key = _FERT_REMARK_CYCLE_KEY[get_cycle_phase(girl)]
            if _key == "remark_cycle_danger" and girl.has_trait("pregnancy_fetish"):
                _key = "remark_cycle_danger_fetish"
            _what = "cycle"

        _fert_say_hint(girl, _key)
        fert_learn(girl, _what, "scene_remark")

    # ── 3. Breeding kink: "breed" force type for Cum.rpy's forced-creampie flow ──
    # Cum.rpy indexes these two dicts by force type, so the new type needs its own entries.
    # (init 1: the dicts are created by Cum.rpy's init block.)
    RESIST_AUTO_OBED_GIRL["breed"] = [
        _("Stay inside! I want your baby, I'll make you... I..."),
        _("You're not pulling out! I need you to breed me! I'll... I..."),
        _("Get me pregnant! I won't let you... I..."),
    ]
    RESIST_AUTO_STRENGTH_GIRL["breed"] = [
        _("You're not pulling out! I want your baby!"),
        _("Stay in me! You're going to get me pregnant!"),
    ]
