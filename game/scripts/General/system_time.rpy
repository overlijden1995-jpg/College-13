# ============================================
# TIME SYSTEM: DAY / TIME SLOTS / ROUND
# ============================================

init python:
    TIME_NAMES = ["Morning", "Midday", "Evening", "Night"]
    # _() = the marker only (the values stay English): a line shows one with [WEEK_DAYS[...]!t]
    WEEK_DAYS = [_("Sunday"), _("Monday"), _("Tuesday"), _("Wednesday"), _("Thursday"), _("Friday"), _("Saturday")]

    NIGHT_INDEX = TIME_NAMES.index("Night")

    def _scene_time_up_line():
        _lines = [
            _("We need to stop... I have somewhere to be."),
            _("Wait... what time is it? I really have to go!"),
            _("Sorry, I'm going to be late... we have to stop."),
            _("Hold on... I need to get going. I'm out of time."),
        ]
        # every control menu calls this when its Round reaches 100, right before ending the scene
        print("[SCENE_FLOW] TIME UP: Round=%s, the control menu ends the scene | %s" % (getattr(store, "Round", "?"), scene_flow_state()))
        return _tl(renpy.random.choice(_lines))

    # Her photo texts of her own accord (label Wait: 6b piercing, 6e spanked, 6f creampie, 6g bikini, 6c masturbation,
    # 6d tease, 6i camera tease): ONE per girl every PHOTO_TEXT_GAP days, whatever the kind (author 2026-10-07: "too
    # many tease texts in a row from the same girl, with a photo"). Each kind keeps its own rule on top (7 days for
    # the random ones, the morning after for spanked / creampie). A photo he asks for (phone_messaging.rpy) is not one.
    PHOTO_TEXT_GAP = 3

    def photo_text_ready(girl, kind):
        """She may text him a photo of her own accord today: never for a "no_photos" girl (girl_sends_photos,
        the one gate all 7 kinds share), none in the last PHOTO_TEXT_GAP days otherwise."""
        if not girl_sends_photos(girl):
            print("[PHOTO_TEXT] %s: no %s photo ever, her config says no_photos" % (girl.gid, kind))
            return False
        last = getattr(girl, "_photo_text_day", None)
        if last and (store.Day - last) < PHOTO_TEXT_GAP:
            print("[PHOTO_TEXT] %s: no %s photo today, her last photo text was day %d (next from day %d)" % (
                girl.gid, kind, last, last + PHOTO_TEXT_GAP))
            return False
        return True

    def photo_text_sent(girl, kind):
        """Her photo text of today, any kind: the next one waits PHOTO_TEXT_GAP days."""
        girl._photo_text_day = store.Day
        print("[PHOTO_TEXT] %s sent a %s photo on day %d, next from day %d" % (
            girl.gid, kind, store.Day, store.Day + PHOTO_TEXT_GAP))

    # --- SAFE GLOBAL INITIALIZATION ---

    # Create Day if it does not exist yet (1 = Monday)
    if "Day" not in globals():
        Day = 1

    # Create TimeIndex if it does not exist yet (0 = Morning)
    if "TimeIndex" not in globals():
        TimeIndex = 0

    # Ensure Party exists
    if "Party" not in globals():
        Party = []

    # Ensure Round exists
    if "Round" not in globals():
        Round = 0

    # Flag for auto sleep after Night -> next day
    if "NightAutoSleepPending" not in globals():
        NightAutoSleepPending = False

    # Generic time lock for scripted cutscenes
    def time_lock():
        store._time_locked = True
        print("[TIME_LOCK] Time locked")

    def time_unlock():
        store._time_locked = False
        print("[TIME_LOCK] Time unlocked")

    # Snapshot of girls at the same location before time change
    if "LastPresentGirls" not in globals():
        LastPresentGirls = []

    # Flag: Apply_Time_Cost already called Wait for this time change
    if "_atc_wait_done" not in globals():
        _atc_wait_done = False

    # Optional: world init flag (used em outro arquivo se quiser)
    if "world_initialized" not in globals():
        world_initialized = False

    def daily_lust_tick():
        """
        Called once per new day. Each girl's Lust rises a little
        (3-8 random). If Lust >= 80 and the girl is NOT with the
        player, she relieves herself off-screen and Lust drops.
        """
        for g in ALL_GIRLS:
            rise = renpy.random.randint(3, 8)
            g.Lust = min(100, getattr(g, "Lust", 0) + rise)

            # Off-screen auto-relief: Lust >= 80 and not with the player
            if g.Lust >= 80 and g.loc != store.CurrentLocation:
                g.Lust = renpy.random.randint(15, 30)
                g.RegisterAction("girl_masturbated_alone")

            # BF loyalty daily regen (recovers when player doesn't interact)
            if hasattr(g, "bf_loyalty_daily_regen"):
                g.bf_loyalty_daily_regen()

            # Hardcore Relationship Mode daily tick
            if getattr(store, "hardcore_relationship", False):
                if hasattr(g, "hardcore_relationship_tick"):
                    g.hardcore_relationship_tick()

            _sync_girl(g)

    def update_all_girls_locations_for_time(day, time_index, reset_outfit=True):
        """
        day: in-game day number (1-based, loops over schedule length).
        time_index: index in TIME_NAMES (0 = Morning, 1 = Midday, ...).
        This function sets girl.loc for every girl according to her schedule
        and optionally resets their outfit to the default preset.
        reset_outfit=False is used by after_load to keep snapshot clothing.
        """
        _player_loc = getattr(store, "CurrentLocation", "campus")
        store._girls_were_with_player = set(g.gid for g in ALL_GIRLS if getattr(g, "loc", None) == _player_loc)
        for girl in ALL_GIRLS:
            if getattr(girl, "_giving_birth", False):
                girl.loc = GIRL_AWAY_LOC
                continue
            if getattr(girl, "_arguing_in_room", 0) == day:
                continue
            new_loc = get_scheduled_location_for(girl, day, time_index)

            # Keep girl in showers if player is there and she has a shower state
            _sh_state = getattr(girl, "shower_state", None)
            if _player_loc in SHOWER_SPOTS and _sh_state and girl.loc == _player_loc:
                new_loc = _player_loc

            # On load (reset_outfit=False): preserve location if girl was
            # with the player (invite, event, etc.) — don't override with schedule
            if not reset_outfit and girl.loc == _player_loc:
                continue

            girl.loc = new_loc

            if getattr(girl, "_sleeps_in_player_room", False) and time_index >= NIGHT_INDEX - 1 and _sleep_arrange_can_tonight(girl):
                girl.loc = "room"
            # his phone order (player_phone_order.rpy): a submissive he told to be in his room tonight
            if player_phone_order_tonight(girl, day, time_index):
                girl.loc = "room"

            if reset_outfit:
                _prev_loc = getattr(girl, "_prev_scheduled_loc", None)

                # Always clear shower state when leaving showers
                if new_loc not in SHOWER_SPOTS:
                    _clear_shower_outfit(girl)

                if _prev_loc is not None and new_loc == _prev_loc:
                    pass
                elif new_loc in SHOWER_SPOTS and _sh_state and _sh_state != "dressed":
                    apply_shower_outfit(girl, refresh=False)
                elif new_loc == "pool":
                    if getattr(girl, "_bikini_unlocked", False):
                        girl.WearPreset("pool", apply_now=False)
                    else:
                        girl.WearPreset("casual", apply_now=False)
                else:
                    girl.WearPreset("casual", apply_now=False)
                girl._prev_scheduled_loc = new_loc
            _sync_girl(girl)

        if callable(globals().get("update_all_npc_locations", None)):
            update_all_npc_locations(day, time_index)

    def _per_slot_cleanup():
        """Centralized per-time-slot cleanup for ALL girls.
        Called once every time a slot advances (Morning->Midday, etc.).
        Consolidates resets that should always happen between periods."""

        if getattr(store, "_time_locked", False) and not getattr(store, "_scene_restricted", False):
            store._time_locked = False
            print("[TIME_LOCK] Safety unlock: time_locked was True but no scene active")

        for g in ALL_GIRLS:
            # Blush reset
            _gss = sprite_state.setdefault(g.Id, {})
            if _gss.get("blush", 0) > 0:
                _gss["blush"] = 0
            # Clothing state reset: girls fix displaced clothes between time slots
            if hasattr(g, "clothes_state") and hasattr(g, "clothes"):
                for _slot, _state in g.clothes_state.items():
                    if _state != "full" and g.clothes.get(_slot):
                        g.clothes_state[_slot] = "full"

            # Expression reset: clear scene-specific faces (angry/sad reapplied by set_girl_sprite)
            _gss["eyes"] = "eyes_normal"
            _gss["brows"] = "brows_normal"
            _gss["mouth"] = "mouth_normal"

            # Spank / face slap level decay: -3 per time slot, then re-derive butt_blush (spanks only)
            if getattr(g, "SpankLevel", 0) > 0:
                g.SpankLevel = max(0, g.SpankLevel - 3)
            if getattr(g, "SlapLevel", 0) > 0:
                g.SlapLevel = max(0, g.SlapLevel - 3)
            _sl = getattr(g, "SpankLevel", 0)
            if _sl >= 6:
                _gss["butt_blush"] = 2
            elif _sl >= 3:
                _gss["butt_blush"] = 1
            else:
                _gss["butt_blush"] = 0

            # LD after-pussy/anal visual reset
            g._ld_after_pussy = False
            g._ld_after_anal = False

        # Player energy recovery (+1 per slot, capped)
        _p = store.Player
        _emax = _p._get_energy_max()
        if _p.energy < _emax:
            _p.energy = min(_p.energy + 1, _emax)

        # Player arousal (Focus) decay: -15 per time slot, floor 0
        if _p.Focus > 0:
            _old_f = _p.Focus
            _p.Focus = max(0, _p.Focus - 15)
            debug_log("[TIME] Player.Focus %d -> %d (slot decay)" % (_old_f, _p.Focus))

        # Clear stale scene flags
        store._last_scene_was_anal = False

        # Girls visited at night: reset so shower picker allows them in the new slot
        store._girls_visited_night = set()

        debug_log("[TIME] _per_slot_cleanup done")

    def _per_day_cleanup():
        """Centralized per-new-day cleanup. Called once when Day increments, by advance_time (natural
        Night -> Morning rollover) and by start_next_day_manually (Sleep, sleepovers, restaurant night)."""

        # Pregnancy system daily tick. FIRST: a girl who goes into labor today is already away
        # (girl_is_away) when the NPC next-day processors, the hardcore neglect tick and the event
        # schedulers below look at her.
        if callable(globals().get("_pregnancy_daily_tick", None)):
            _pregnancy_daily_tick()

        for g in ALL_GIRLS:
            g.clear_expired_statuses()

            # Clear cum on new day (shower between days)
            g.Cum = []
            g._mouth_cum_persist = False

            # Reset spank / face slap level partially
            _sl = getattr(g, "SpankLevel", 0)
            if _sl > 0:
                g.SpankLevel = max(0, _sl - 3)
            if getattr(g, "SlapLevel", 0) > 0:
                g.SlapLevel = max(0, g.SlapLevel - 3)

            # Reset sexuality spectrum temp shift
            if getattr(g, "_spectrum_temp_shift", 0) > 0:
                g._spectrum_temp_shift = 0

        # Reset touch spectrum cooldown (keyed by girl+day+time, stale after day rolls)
        store._touch_spectrum_done = set()

        for g in ALL_GIRLS:
            # Sober up overnight (safety net; events also reset on exit)
            if getattr(g, "_hangout_alcohol", 0) > 0:
                reset_drunk(g)

        # NPC catch resolution
        debug_log("[TIME] _per_day_cleanup: Day=%d, running NPC catch/suspicion" % store.Day)
        # girls_reachable: every processor is driven by a pending flag on the girl. Away (giving birth):
        # nothing is resolved, the flags stay, and _pregnancy_return runs the same list the morning she is back.
        for _ncg in girls_reachable():
            npc_next_day_process(_ncg)

        if callable(globals().get("_npc_suspicion_daily_decay", None)):
            _npc_suspicion_daily_decay()

        # Reset sleepover consecutive counter for girls who didn't sleep over last night
        for _scg in ALL_GIRLS:
            if not getattr(_scg, "_slept_with_player_tonight", False):
                if getattr(_scg, "_sleepover_consecutive", 0) > 0:
                    _scg._sleepover_consecutive = 0
                    print("[SLEEPOVER] %s consecutive counter reset (didn't sleep over)" % _scg.gid)

        # NPC auto phone exchange (friendship >= 400)
        _npc_contacts = getattr(store.Player, "phone_npc_contacts", None)
        if _npc_contacts is None:
            store.Player.phone_npc_contacts = set()
            _npc_contacts = store.Player.phone_npc_contacts
        for _anpc in NPC_PARTNERS.values():
            if _anpc.partner_id in _npc_contacts:
                continue
            if _anpc.friendship_with_player >= 400:
                _npc_contacts.add(_anpc.partner_id)
                _intro_lines = [
                    _("Hey, got your number from the class group. It's %s."),
                    _("Yo, it's %s. Figured I'd add you."),
                    _("Hey! It's %s. We should text more."),
                ]
                phone_add_msg(_anpc.partner_id, _anpc.partner_id, _tl(renpy.random.choice(_intro_lines)) % _anpc.Name)
                debug_log("[NPC_PHONE] Auto-added %s (friendship=%d)" % (_anpc.name, _anpc.friendship_with_player))

        # Ensure any leftover cum state is wiped
        session_cum_reset()

        # Daily Lust buildup + off-screen relief
        daily_lust_tick()

        # Reset stale restaurant state from previous day (an orphaned list with day -1 too)
        if getattr(store, "_restaurant_day", -1) != -1 and getattr(store, "_restaurant_day", -1) != store.Day:
            store._restaurant_day = -1
            store._restaurant_girls = []
        elif getattr(store, "_restaurant_day", -1) == -1 and getattr(store, "_restaurant_girls", []):
            store._restaurant_girls = []

        # Reset daily flags
        store._gossip_used_today = False
        store._night_swim_fired_today = False

        # BigFans daily refresh + passive income
        store._bigfans_new_count = bigfans_daily_refresh()
        store._bigfans_daily_earned = bigfans_daily_income()

        # Sync virginity knowledge between close friends
        sync_virginity_by_friendship()

        # Cheat heat decay (very slow, preserves multi-session buildup)
        for g in ALL_GIRLS:
            _ch = getattr(g, "_cheat_heat", 0)
            if _ch > 0:
                _decay = 3 if getattr(g, "has_trait", lambda t: False)("loyal") else 1 if getattr(g, "has_trait", lambda t: False)("cheater") else 2
                g._cheat_heat = max(0, _ch - _decay)

        # Weekly workout check on Sundays
        if (store.Day - 1) % 7 == 0 and store.Day > 1:
            store.Player.weekly_workout_check()

        # Anniversary gift daily scheduling
        if callable(globals().get("_ag_daily_check", None)):
            _ag_daily_check()

        # NTR bet event daily scheduling
        if callable(globals().get("_bet_daily_check", None)):
            _bet_daily_check()

        # Femdom phone order (femdom_phone_order.rpy): an order older than last night is stale. Last night's
        # order stays: the next Wait judges it (5g).
        if callable(globals().get("femdom_phone_order_rollover", None)):
            femdom_phone_order_rollover()
        if callable(globals().get("player_phone_order_rollover", None)):
            player_phone_order_rollover()

        # The father (shion_family.rpy): his business trip starts / ends today (his text goes out this morning, 6zz2)
        dad_trip_daily()

    def start_next_day_manually():
        """Jump straight to the next morning WITHOUT advance_time: Sleep (do_sleep), both sleepovers and the
        restaurant night. Runs the SAME new-day routine as the natural rollover. Those paths used to
        hand-copy parts of _per_day_cleanup, and every system added to it later was missing from the copies:
        the pregnancy tick NEVER ran on those nights (no pregnancy days, pill, births, returns or child
        support for a player who goes to bed through the Sleep button), nor the suspicion decay, the
        anniversary / NTR bet schedulers on sleepovers, five NTR next-day processors on the restaurant night...
        Add new daily logic to _per_day_cleanup ONLY."""
        global Day, TimeIndex, Round
        _old_day = Day
        Day += 1
        TimeIndex = 0
        Round = 0
        # Overnight blush fade (the per-slot cleanup does it between slots; these paths skip the slots)
        for g in ALL_GIRLS:
            _gss = sprite_state.setdefault(g.Id, {})
            _sl = getattr(g, "SpankLevel", 0)
            if _sl >= 6:
                _gss["butt_blush"] = 2
            elif _sl >= 3:
                _gss["butt_blush"] = 1
            else:
                _gss["butt_blush"] = 0
            if _gss.get("blush", 0) > 0:
                _gss["blush"] = 0
        _per_day_cleanup()
        update_all_girls_locations_for_time(Day, TimeIndex)
        debug_log("[TIME] start_next_day_manually: Day %d -> %d" % (_old_day, Day))

    def advance_time(slots=1):
        """
        slots: how many time slots to advance (each one is a TIME_NAMES entry).
        - Moves TimeIndex forward by 'slots'.
        - Wraps to next Day when TimeIndex passes the last slot.
        - Calls update_all_girls_locations_for_time after a change.
        - Resets Round and sets NightAutoSleepPending when we move
        from Night into the next day.
        Returns True if time or day actually changed.
        """
        if getattr(store, "_time_locked", False):
            return False

        global TimeIndex, Day, Round, NightAutoSleepPending

        old_time = TimeIndex
        old_day = Day
        changed = False

        # Snapshot father's room before the time changes (for departure hints in Wait)
        store._dad_prev_room = dad_room() if store.CurrentLocation in APARTMENT_ROOMS else None

        TimeIndex += slots

        # Wrap to next day when we pass the last time slot
        while TimeIndex >= len(TIME_NAMES):
            TimeIndex -= len(TIME_NAMES)
            Day += 1

        if TimeIndex != old_time or Day != old_day:
            if Day != old_day and old_time == NIGHT_INDEX:
                NightAutoSleepPending = True

            # Centralized per-slot cleanup (blush, clothing, spank, energy, focus)
            _per_slot_cleanup()

            # Per-day cleanup (statuses, cum, lust, NPC, cheat heat, etc.)
            if Day != old_day:
                _per_day_cleanup()

            update_all_girls_locations_for_time(Day, TimeIndex)
            store._crowd_level = get_crowd_level()
            Round = 0
            changed = True

        return changed

    def advance_round(amount):
        """
        Accumulate time cost in Round.  Does NOT trigger time transitions.
        The caller (Apply_Time_Cost or a loop-entry guard) is responsible
        for checking Round >= 100 and calling advance_time + Wait.
        """
        global Round
        if getattr(store, "_time_locked", False):
            return
        Round += amount
        recording_tick(amount)

# -------------------------------------------------------
# PREGNANCY MORNING EVENTS (called by label Wait, morning only)
# The "from" names are the ones these calls always had: a save made in the middle of one of these events
# still finds its return site.
# -------------------------------------------------------
label _pregnancy_morning_hooks:

    # 0c) Pregnancy discovery event (morning trigger)
    if TimeIndex == 0 and getattr(store, "_pregnancy_discovery_pending", None):
        call _pregnancy_discovery from _call_pregnancy_discovery

    # 0d) NPC pregnancy confrontation (morning trigger, campus arrival)
    if TimeIndex == 0 and getattr(store, "_npc_pregnancy_confrontation_pending", None):
        call _npc_pregnancy_confrontation from _call_npc_preg_confrontation

    # 0e) Pregnancy birth event (girl leaves for 7 days)
    # while, not if: _pregnancy_birth queues the next girl who went into labor the same day
    while TimeIndex == 0 and getattr(store, "_pregnancy_birth_pending", None):
        call _pregnancy_birth from _call_preg_birth

    # 0f) Pregnancy return event (girl comes back after birth)
    while TimeIndex == 0 and getattr(store, "_pregnancy_return_pending", None):
        call _pregnancy_return from _call_preg_return

    return

# -------------------------------------------------------
# INTERNAL "WAIT" LOGIC (USE AFTER TIME CHANGE)
# Call this ONLY when advance_round/advance_time returned True
# -------------------------------------------------------
label Wait:

    # 0) Sync Party locations BEFORE any processing (covers after_load / do_sleep edge cases)
    python:
        for g in list(Party):
            if girl_is_away(g):   # went into labor while following him: she is gone, not at his side
                Party.remove(g)
                continue
            g.loc = CurrentLocation

    # 0b) Night→Morning auto-sleep: must run BEFORE process_girls so nerd
    #     class invites / girl departure menus don't fire while the player
    #     is being sent to bed.
    if NightAutoSleepPending:
        $ NightAutoSleepPending = False
        $ Party = []
        $ LastPresentGirls = []

        if CurrentLocation != "room":
            "On your way, you realize how late it is and decide to head back to your room."
            $ navigate_to("room", None)
            call Set_Scene(entry=False) from _call_Set_Scene_15
            pause 0.5

        $ Player.recharge_energy()

        scene black
        with fade
        pause 0.5
        "You crash in your room and sleep through the night."

    # 0c-0f) Pregnancy morning events: discovery, NPC confrontation, births, returns (one label, called
    #        again after 5b / 5c because the day can roll over INSIDE this label)
    call _pregnancy_morning_hooks from _call_preg_morning_hooks

    # 0g) An exam slot that went by without the prompt (he slept through the Friday, a scene took the slot) is an F
    #     (exam.rpy: exam_record_grade)
    $ exam_missed_check()

    # 1) Exam check FIRST — intercepts girl movement on exam slots so
    #    the girl speaks the exam invite instead of the generic "I have
    #    something else to do." line from process_girls_after_time_change.
    if is_exam_slot(Day, TimeIndex):
        call exam_prompt from _call_exam_prompt
        # exam_prompt already placed every girl (classroom or stayed).
        # Skip the normal girl-movement pass to avoid double dialogue.
    else:
        # Normal slot: let girls react to the time change and move.
        call process_girls_after_time_change from _call_process_girls_after_time_change

    # Father departure hint: if he was in this room and left, he says where he's going
    python:
        _dad_old = getattr(store, "_dad_prev_room", None)
        _dad_new = dad_room()
        if _dad_old and _dad_old == CurrentLocation and _dad_new != _dad_old:
            _dad_dest_lines = DAD_DEPARTURE_LINES.get(_dad_new, DAD_DEPARTURE_LINES.get(None, []))
            if _dad_dest_lines:
                _dad_line = _tl(renpy.random.choice(_dad_dest_lines))
                renpy.say(Character(Dad.Name, who_color=Dad.color), _dad_line)
        store._dad_prev_room = None

    python:
        # 2) Keep followers in the same location as the player
        for g in Party:
            if not girl_is_away(g):
                g.loc = CurrentLocation

        # 3) Small passive Lust decay for everyone each time slot
        for girl in ALL_GIRLS:
            if getattr(girl, "Lust", 0) > 50:
                girl.Lust -= 5

        # 3b) Jealousy: daily decay + rise when GF sees player with intimate girls
        for _jg in ALL_GIRLS:
            if not _jg.is_dating_player():
                continue
            # Daily decay (once per morning)
            if TimeIndex == 0:
                Change_Status(_jg, "Jealousy", -20, show_popup=False)
                # Ex trust: +1/day for reconciled exes (any type)
                _etm = getattr(_jg, "_ex_trust_max", 0)
                if _etm > 0:
                    _cet = getattr(_jg, "_ex_trust", 0)
                    if _cet < _etm:
                        _jg._ex_trust = min(_etm, _cet + 1)
            # Rise: other girls with player intimacy at same location
            if getattr(_jg, "loc", None) == CurrentLocation:
                for _jo in ALL_GIRLS:
                    if _jo is _jg or _jo.gid == _jg.gid:
                        continue
                    if getattr(_jo, "loc", None) != CurrentLocation:
                        continue
                    if not getattr(_jo, "intimacy_flags", None):
                        continue
                    _j_like = (_jg.Girl_like or {}).get(_jo.gid, 500) if hasattr(_jg, "Girl_like") else 500
                    if _j_like < 250:
                        _j_rise = 30
                    elif _j_like < 500:
                        _j_rise = 20
                    else:
                        _j_rise = 10
                    if _jg.has_trait("polyamorous"):
                        _j_rise = 0
                    elif is_harem_exempt(_jg, _jo):
                        _j_rise = _j_rise // 3
                    if _j_rise > 0:
                        Change_Status(_jg, "Jealousy", _j_rise, show_popup=False)

        # 3c) Harem resentment: forced members gain Jealousy, unfreeze at Girl_like >= 400
        if TimeIndex == 0:
            for _rg in ALL_GIRLS:
                if not _rg.is_dating_player():
                    continue
                _rg_forced = getattr(_rg, "_harem_forced_by", None)
                if not _rg_forced:
                    continue
                _rg_resent = False
                for _rival_gid in list(_rg_forced):
                    _rival = GIRL_BY_ID.get(_rival_gid)
                    if not _rival or not _rival.is_dating_player():
                        _rg_forced.discard(_rival_gid)
                        continue
                    if _rg.get_like_for(_rival_gid) >= 400:
                        _rg_forced.discard(_rival_gid)
                        print("[HAREM_RESENT] %s no longer resents %s (Girl_like >= 400)" % (_rg.gid, _rival_gid))
                        continue
                    _rg_resent = True
                if _rg_resent:
                    Change_Status(_rg, "Jealousy", 10, show_popup=False)
                    print("[HAREM_RESENT] %s +10 Jealousy (forced resentment, rivals=%s)" % (_rg.gid, list(_rg_forced)))

        # 3d) Jealousy corrodes Girl_like (morning only, player must be present)
        _jealousy_corrode_events = []
        if TimeIndex == 0:
            for _jcg in ALL_GIRLS:
                if not _jcg.is_dating_player():
                    continue
                if getattr(_jcg, "Jealousy", 0) < 400:
                    continue
                if _jcg.has_trait("polyamorous"):
                    continue
                if getattr(_jcg, "loc", None) != CurrentLocation:
                    continue
                for _jcr in ALL_GIRLS:
                    if _jcr is _jcg or _jcr.gid == _jcg.gid:
                        continue
                    if getattr(_jcr, "loc", None) != CurrentLocation:
                        continue
                    if not getattr(_jcr, "intimacy_flags", None):
                        continue
                    if is_harem_exempt(_jcg, _jcr):
                        continue
                    _jc_old = _jcg.get_like_for(_jcr.gid)
                    if _jc_old > 0:
                        _jcg.add_like_for(_jcr.gid, -5)
                        _jealousy_corrode_events.append((_jcg.Name, _jcr.Name))
                        print("[JEALOUSY_CORRODE] %s -> %s: Girl_like -5 (was %d, now %d)" % (_jcg.gid, _jcr.gid, _jc_old, _jcg.get_like_for(_jcr.gid)))

        # 4) Study solo bonus: girls who are in their home room without the player.
        # Not at Night: she sleeps (the night credit made an F impossible: ~12 free points a cycle)
        if TimeIndex < 3:
            for g in ALL_GIRLS:
                girl_home = GIRLS_CONFIG.get(g.gid, {}).get("home")
                if girl_home and g.loc == girl_home and CurrentLocation != girl_home:
                    g.study_level += 1

    # 4b) Narrate jealousy-corroded friendships
    if len(_jealousy_corrode_events) > 0:
        python:
            for _jce in _jealousy_corrode_events:
                renpy.say(None, _tl(_("%s is around %s and doesn't seem happy about it. The jealousy is straining their friendship.")) % (_jce[0], _jce[1]))

    # 4c) His stepmother's text about his last grade (family_grades.rpy): from the Evening of the exam day, never in
    #     front of a girlfriend of his; the punishment (money, the breakup by text), his father's text
    $ _fgn_her = family_grade_news_now()
    if _fgn_her is not None:
        call _family_grade_news(_fgn_her) from _call_family_grade_news

    # 5) Kick player (and any remaining girls) out of locations that close at Night
    python:
        _closed_at_night = {"gym", "pool", "classroom", "mall"}
        _player_in_closed = (TimeIndex == NIGHT_INDEX and CurrentLocation in _closed_at_night)
    if _player_in_closed:
        # posted hours, no guard (tester 2026-10-10 asked WHO kicks him out of an unstaffed pool):
        # nothing stops anyone from wandering back in after dark, and the night events count on that
        "It's getting late. This place is closing for the night. Not that anyone stays behind to enforce it."
        python:
            _here = CurrentLocation
            # Move ALL girls still at this closed location to their scheduled spot
            for _g in ALL_GIRLS:
                if _g.loc == _here:
                    _g.loc = get_scheduled_location_for(_g, Day, TimeIndex)
                    _g.WearPreset("casual", apply_now=False)
                    _sync_girl(_g)
            Party = []
        $ navigate_to("campus", None)
        call Set_Scene(entry=True) from _call_Set_Scene_closed_loc

    # 5b) Restaurant date check (Evening)
    call restaurant_date_check from _call_restaurant_date_check

    # 5c) Hangout night check
    call hangout_night_check from _call_hangout_night_check

    # 5c2) The restaurant group night (5b) and the hangout night (5c) roll the day over INSIDE this label, below
    #      the morning hooks at the top: whatever that rollover made pending (a birth, a return, a discovery)
    #      plays now instead of a full day late. Nothing pending = nothing happens.
    call _pregnancy_morning_hooks from _call_preg_morning_hooks_rollover

    # 5d) Anniversary gift check
    call anniversary_gift_check from _call_anniversary_gift_check

    # 5e) NTR bet event check
    call ntr_bet_check from _call_ntr_bet_check

    # 5f) Activity buddy invite: moved to the END of the once-per-morning region (6zzz), see there.

    # 5g) Femdom phone order (femdom_phone_order.rpy): the Night she ordered him to her room is over. He never
    #     came: her angry text (Obed down, femdom_request_refused). He came: her line already played face to face
    #     when he reached her room. Outside the morning region: the order is consumed here, it can't play twice.
    $ _fdo_waited = femdom_phone_order_judge()
    if _fdo_waited is not None:
        call _femdom_phone_order_no_show(_fdo_waited) from _call_femdom_phone_order_no_show

    # 5g2) His phone order (player_phone_order.rpy, the mirror): the Night he told a submissive to be in his room is
    #      over and he never came: her hurt text (Love down). He came: her line already played when he walked in.
    $ _ppo_waited = player_phone_order_judge()
    if _ppo_waited is not None:
        call _player_phone_order_no_show(_ppo_waited) from _call_player_phone_order_no_show

    # 6*) ONCE PER MORNING. Everything from here to 6zz (allowance, income, child support, the girl-initiated
    #     photo / text events, the hardcore notices...) belongs to the morning of a Day and must run once.
    #     A dinner date that ends in a sleepover / Sleep runs label Wait NESTED inside the Evening Wait: the
    #     inner one does the morning, then the outer one came back HERE with TimeIndex 0 and did it all again
    #     (allowance and investor income paid twice, every photo event rolled twice).
    if TimeIndex == 0 and store._wait_morning_done_day == Day:
        $ print("[TIME] Wait: morning of Day %d already done (nested Wait), skipping 6 to 6zz" % Day)
        jump .wait_morning_done
    if TimeIndex == 0:
        $ store._wait_morning_done_day = Day

    # 6) Friday paycheck notification (frozen by his stepmother after a bad grade: family_grades.rpy)
    if (Day - 1) % 7 == 5 and TimeIndex == 0:
        $ _alw_frozen_by = allowance_frozen_by()
        if _alw_frozen_by is None:
            $ Player.cash += 100
            "It's Friday. You received your weekly allowance: {b}$100{/b}. Balance: {b}$[Player.cash]{/b}."
        else:
            $ Narration(_tl_fmt(_("It's Friday. No allowance this week: %s froze it. Balance: {b}$[Player.cash]{/b}."), _alw_frozen_by.Name))

    # 6a) Investor daily income notification
    if TimeIndex == 0 and getattr(Player, "player_trait", "") == "investor":
        $ Player.add_cash(50)
        "Your investments paid off. You earned {b}$50{/b} today. Balance: {b}$[Player.cash]{/b}."

    # 6a1) Sugar mommy weekly allowance (Actions/sugar_mommy.rpy): Fridays, on top of the family's $100 and
    #      never frozen (hers has nothing to do with the guardian's punishments)
    if (Day - 1) % 7 == 5 and TimeIndex == 0:
        python:
            for _sgm in sugar_girls_active():
                if girl_is_away(_sgm):
                    continue
                Player.add_cash(SUGAR_ALLOWANCE)
                unlock_achievement("sugar_baby")
                print("[SUGAR] %s weekly allowance +$%d (cash %d)" % (_sgm.gid, SUGAR_ALLOWANCE, Player.cash))
                renpy.say(None, _tl_fmt(_("A transfer from %s landed: {b}$%d{/b}. No note. There never is."), _sgm.Name, SUGAR_ALLOWANCE)
                          + " " + _tl(_("Balance:")) + " {b}$" + str(Player.cash) + "{/b}")

    # 6a2) Weekly child support. The daily tick charged it (children.rpy: child_support_charge); this is where
    #      he hears about it: total, who got how much, the balance NOW. The money used to vanish without a word.
    #      No TimeIndex test: a morning spent inside a scene reaches Wait at Noon, and the notice is consumed
    #      when shown (it can never play twice).
    if getattr(store, "_child_support_notice", None):
        python:
            for _csn_line in child_support_notice_lines():
                Narration(_csn_line)

    # 6b) Piercing changes (next morning) + clear sleepover flag + daily resets
    if TimeIndex == 0:
        python:
            _piercing_photo_girl = None
            for _pg in ALL_GIRLS:
                # Clear daily action tracking
                _pg.Recent_Actions = []
                _pg.Daily_Actions = []

                # Clear sleepover flag from last night
                _slept = getattr(_pg, "_slept_with_player_tonight", False)
                _pg._slept_with_player_tonight = False

                if getattr(_pg, "_piercing_pending", False) and girl_is_away(_pg):
                    _pg.Piercing = True            # she put them on, but nobody sees it and she sends nothing
                    _pg._piercing_pending = False
                elif getattr(_pg, "_piercing_pending", False):
                    _pg.Piercing = True
                    _pg._piercing_pending = False
                    _first_time = not getattr(_pg, "_piercing_photo_sent", False)
                    _has_phone = _pg.gid in getattr(store.Player, "phone_contacts", set())
                    _gwwp = getattr(store, "_girls_were_with_player", set())
                    _pvs_fn = globals().get("pregnancy_visual_stage")
                    _preg_vis = callable(_pvs_fn) and _pvs_fn(_pg) >= 1
                    if not _slept and _has_phone and _first_time and not _preg_vis and getattr(_pg, "loc", None) != store.CurrentLocation and _pg.gid not in _gwwp and photo_text_ready(_pg, "piercing"):
                        _piercing_photo_girl = _pg
                        _pg._piercing_photo_sent = True
                    else:
                        renpy.say(None, _tl(_("{b}%s{/b} is wearing the piercings you gave her.")) % _pg.Name)
                elif getattr(_pg, "_piercing_remove_pending", False):
                    _pg.Piercing = False
                    _pg._piercing_remove_pending = False
                    renpy.say(None, _tl(_("{b}%s{/b} took off her piercings.")) % _pg.Name)
        if _piercing_photo_girl is not None:
            $ photo_text_sent(_piercing_photo_girl, "piercing")
            call _piercing_photo_event(_piercing_photo_girl) from _call_piercing_photo

    # Her photo texts (6b piercing above, then 6e, 6f, 6g, 6c, 6d here and 6i below): ONE per girl every
    # PHOTO_TEXT_GAP days (photo_text_ready / photo_text_sent, top of this file). The photos that answer something he
    # did (spanked, creampie, bikini) come before the random ones (masturbation, tease): a random photo never takes
    # their morning, and the morning-after ones cannot wait.
    # 6e) Spanked photo event (next morning after SpankLevel reached 7+)
    if TimeIndex == 0:
        python:
            _spank_photo_girl = None
            _gwwp = getattr(store, "_girls_were_with_player", set())
            for _sg in ALL_GIRLS:
                if not girl_sends_lewd_photos(_sg):   # her turn (femdom_turn.rpy): no lewd photo before her stage 3
                    continue
                if girl_is_away(_sg):   # giving birth at her parents': she sends nothing
                    _sg._heavy_spank_yesterday = False   # "the morning after" is long gone when she is back
                    continue
                if callable(globals().get("pregnancy_visual_stage", None)) and pregnancy_visual_stage(_sg) >= 1:
                    continue
                if getattr(_sg, "loc", None) == store.CurrentLocation or _sg.gid in _gwwp:
                    continue
                if hasattr(_sg, "has_temp_status") and (_sg.has_temp_status("angry") or _sg.has_temp_status("sad")):
                    continue
                if getattr(_sg, "_npc_pregnancy_confrontation_pending", False):
                    continue
                if _sg.has_trait("camera_hater"):
                    continue
                _last_sp = getattr(_sg, "_spank_photo_day", 0) or 0
                if _last_sp > 0 and (store.Day - _last_sp) < 7:
                    continue
                if _sg.gid not in getattr(store.Player, "phone_contacts", set()):
                    continue
                # Need flag that heavy spank happened yesterday
                if not getattr(_sg, "_heavy_spank_yesterday", False):
                    continue
                _sg._heavy_spank_yesterday = False
                if not photo_text_ready(_sg, "spanked"):   # the morning after or never: the flag is already cleared
                    continue
                if renpy.random.random() > 0.30:
                    continue
                _spank_photo_girl = _sg
                break
        if _spank_photo_girl is not None:
            $ _spank_photo_girl._spank_photo_day = Day
            $ photo_text_sent(_spank_photo_girl, "spanked")
            call _spanked_photo_event(_spank_photo_girl) from _call_spank_photo

    # 6f) Creampie photo event (next morning after creampie + "leave it")
    if TimeIndex == 0:
        python:
            _cream_photo_girl = None
            _gwwp = getattr(store, "_girls_were_with_player", set())
            for _cg in ALL_GIRLS:
                if not girl_sends_lewd_photos(_cg):   # her turn (femdom_turn.rpy): no lewd photo before her stage 3
                    continue
                if girl_is_away(_cg):   # giving birth at her parents': she sends nothing
                    _cg._creampie_photo_pending = False   # "the morning after" is long gone when she is back
                    continue
                if callable(globals().get("pregnancy_visual_stage", None)) and pregnancy_visual_stage(_cg) >= 1:
                    continue
                if getattr(_cg, "loc", None) == store.CurrentLocation or _cg.gid in _gwwp:
                    continue
                if hasattr(_cg, "has_temp_status") and (_cg.has_temp_status("angry") or _cg.has_temp_status("sad")):
                    continue
                if _cg.has_trait("camera_hater"):
                    continue
                if _cg.gid not in getattr(store.Player, "phone_contacts", set()):
                    continue
                _cream_pending = getattr(_cg, "_creampie_photo_pending", False)
                if not _cream_pending:
                    continue
                _cg._creampie_photo_pending = False
                if not photo_text_ready(_cg, "creampie"):   # the morning after or never: the flag is already cleared
                    continue
                _cream_photo_girl = _cg
                break
        if _cream_photo_girl is not None:
            $ _cream_photo_girl._cream_photo_day = Day
            $ photo_text_sent(_cream_photo_girl, "creampie")
            call _creampie_photo_event(_cream_photo_girl) from _call_cream_photo

    # 6g) Bikini photo event (morning after receiving bikini gift, one-shot)
    if TimeIndex == 0:
        python:
            _bikini_photo_girl = None
            _gwwp = getattr(store, "_girls_were_with_player", set())
            for _bg in ALL_GIRLS:
                if girl_is_away(_bg):   # giving birth at her parents': she sends nothing
                    continue
                if callable(globals().get("pregnancy_visual_stage", None)) and pregnancy_visual_stage(_bg) >= 1:
                    continue
                if getattr(_bg, "loc", None) == store.CurrentLocation or _bg.gid in _gwwp:
                    continue
                if not getattr(_bg, "_bikini_unlocked", False):
                    continue
                if getattr(_bg, "_bikini_photo_sent", False):
                    continue
                if _bg.gid not in getattr(store.Player, "phone_contacts", set()):
                    continue
                if not photo_text_ready(_bg, "bikini"):   # she waits: the photo comes once the gap is over
                    continue
                _bikini_photo_girl = _bg
                break
        if _bikini_photo_girl is not None:
            $ _bikini_photo_girl._bikini_photo_sent = True
            $ photo_text_sent(_bikini_photo_girl, "bikini")
            call _bikini_photo_event(_bikini_photo_girl) from _call_bikini_photo

    # 6c) Masturbation photo event (25% chance daily)
    if TimeIndex == 0:
        python:
            _mast_photo_girl = None
            _gwwp = getattr(store, "_girls_were_with_player", set())
            for _mg in ALL_GIRLS:
                if not girl_sends_lewd_photos(_mg):   # her turn (femdom_turn.rpy): no lewd photo before her stage 3
                    continue
                if girl_is_away(_mg):   # giving birth at her parents': she sends nothing
                    continue
                if callable(globals().get("pregnancy_visual_stage", None)) and pregnancy_visual_stage(_mg) >= 1:
                    continue
                if getattr(_mg, "loc", None) == store.CurrentLocation or _mg.gid in _gwwp:
                    continue
                # Skip if angry, sad, or on cooldown (7 days)
                if hasattr(_mg, "has_temp_status") and (_mg.has_temp_status("angry") or _mg.has_temp_status("sad")):
                    continue
                # Skip ex who hasn't had the cheating confrontation yet
                if hasattr(_mg, "is_ex_of_player") and _mg.is_ex_of_player() and not getattr(_mg, "_ex_confrontation_done", False):
                    continue
                if getattr(_mg, "_npc_pregnancy_confrontation_pending", False):
                    continue
                _last_mast = getattr(_mg, "_mast_photo_day", 0) or 0
                if _last_mast > 0 and (store.Day - _last_mast) < 7:
                    continue
                # Skip cute_sex or camera_hater
                if _mg.has_trait("cute_sex") or _mg.has_trait("camera_hater"):
                    continue
                # Requirements: Love >= 300, has phone, 3+ sex acts with at least 1 being sex
                if getattr(_mg, "Love", 0) < 300:
                    continue
                if _mg.gid not in getattr(store.Player, "phone_contacts", set()):
                    continue
                _flags = getattr(_mg, "intimacy_flags", set()) or set()
                _sex_acts = len(_flags.intersection({"hj", "tj", "bj", "sex"}))
                if _sex_acts < 3 or "sex" not in _flags:
                    continue
                if not photo_text_ready(_mg, "masturbation"):   # one photo text every PHOTO_TEXT_GAP days, whatever the kind
                    continue
                # 25% chance
                if renpy.random.random() > 0.25:
                    continue
                _mast_photo_girl = _mg
                break
        if _mast_photo_girl is not None:
            $ _mast_photo_girl._mast_photo_day = Day
            $ photo_text_sent(_mast_photo_girl, "masturbation")
            $ _mast_photo_girl.Lust = max(getattr(_mast_photo_girl, "Lust", 0), 90)
            call _masturbate_photo_event(_mast_photo_girl) from _call_mast_photo

    # 6d) Tease photo event (20% daily, Love >= 500, 1+ sexual act)
    if TimeIndex == 0:
        python:
            _tease_photo_girl = None
            _gwwp = getattr(store, "_girls_were_with_player", set())
            for _tg in ALL_GIRLS:
                if not girl_sends_lewd_photos(_tg):   # her turn (femdom_turn.rpy): no lewd photo before her stage 3
                    continue
                if girl_is_away(_tg):   # giving birth at her parents': she sends nothing
                    continue
                if callable(globals().get("pregnancy_visual_stage", None)) and pregnancy_visual_stage(_tg) >= 1:
                    continue
                if getattr(_tg, "loc", None) == store.CurrentLocation or _tg.gid in _gwwp:
                    continue
                if hasattr(_tg, "has_temp_status") and (_tg.has_temp_status("angry") or _tg.has_temp_status("sad") or _tg.has_temp_status("unavailable")):
                    continue
                if getattr(_tg, "_npc_catch_pending", False) or getattr(_tg, "_npc_catch_msg_pending", False) or getattr(_tg, "_ntr_violation_pending", False):
                    continue
                # Skip ex who hasn't had the cheating confrontation yet
                if hasattr(_tg, "is_ex_of_player") and _tg.is_ex_of_player() and not getattr(_tg, "_ex_confrontation_done", False):
                    continue
                if getattr(_tg, "_npc_pregnancy_confrontation_pending", False):
                    continue
                if _tg.has_trait("camera_hater"):
                    continue
                _last_t = getattr(_tg, "_tease_photo_day", 0) or 0
                if _last_t > 0 and (store.Day - _last_t) < 7:
                    continue
                if getattr(_tg, "Love", 0) < 500:
                    continue
                if _tg.gid not in getattr(store.Player, "phone_contacts", set()):
                    continue
                _tf = getattr(_tg, "intimacy_flags", set()) or set()
                if not _tf.intersection({"hj", "tj", "bj", "sex", "rub"}):
                    continue
                if not photo_text_ready(_tg, "tease"):   # one photo text every PHOTO_TEXT_GAP days, whatever the kind
                    continue
                if renpy.random.random() > 0.20:
                    continue
                _tease_photo_girl = _tg
                break
        if _tease_photo_girl is not None:
            $ _tease_photo_girl._tease_photo_day = Day
            $ photo_text_sent(_tease_photo_girl, "tease")
            call _tease_photo_event(_tease_photo_girl) from _call_tease_photo

    # 6h) Sugar Daddy event (girl texts asking for money after reaching financial stage 3)
    if TimeIndex == 0:
        python:
            _sugar_daddy_girl = None
            _gwwp = getattr(store, "_girls_were_with_player", set())
            for _sg in ALL_GIRLS:
                if girl_is_away(_sg):   # giving birth at her parents': she sends nothing
                    continue
                if getattr(_sg, "loc", None) == store.CurrentLocation or _sg.gid in _gwwp:
                    continue
                if not getattr(_sg, "_sugar_daddy_pending", False):
                    continue
                if _sg.gid not in getattr(store.Player, "phone_contacts", set()):
                    continue
                if hasattr(_sg, "has_temp_status") and (_sg.has_temp_status("angry") or _sg.has_temp_status("sad")):
                    continue
                _sugar_daddy_girl = _sg
                break
        if _sugar_daddy_girl is not None:
            $ _sugar_daddy_girl._sugar_daddy_pending = False
            call _sugar_daddy_event(_sugar_daddy_girl) from _call_sugar_daddy

    # 6h2) Sugar MOMMY (Actions/sugar_mommy.rpy): a rich submissive offers to keep him; while the arrangement
    #      is on, a small spontaneous transfer may text him instead
    if TimeIndex == 0:
        $ _sugar_mommy_girl = sugar_offer_girl()
        if _sugar_mommy_girl is not None:
            call _sugar_mommy_offer(_sugar_mommy_girl) from _call_sugar_mommy_offer
        else:
            $ _sugar_mommy_girl = sugar_spont_girl()
            if _sugar_mommy_girl is not None:
                call _sugar_spont_gift(_sugar_mommy_girl) from _call_sugar_spont_gift

    # 6i) TeaseCamera photo event (girl sends flirty camera selfie)
    if TimeIndex in (1, 2):
        python:
            _camtease_girl = None
            _gwwp = getattr(store, "_girls_were_with_player", set())
            for _ctg in ALL_GIRLS:
                if not girl_sends_lewd_photos(_ctg):   # her turn (femdom_turn.rpy): no lewd photo before her stage 3
                    continue
                if girl_is_away(_ctg):   # giving birth at her parents': she sends nothing
                    continue
                if callable(globals().get("pregnancy_visual_stage", None)) and pregnancy_visual_stage(_ctg) >= 1:
                    continue
                if hasattr(_ctg, "has_temp_status") and (_ctg.has_temp_status("angry") or _ctg.has_temp_status("sad")):
                    continue
                _last_ct = getattr(_ctg, "_camtease_photo_day", 0) or 0
                if _last_ct > 0 and (store.Day - _last_ct) < 7:
                    continue
                if getattr(_ctg, "Love", 0) < 300:
                    continue
                if _ctg.gid not in getattr(store.Player, "phone_contacts", set()):
                    continue
                # Must NOT be at the same location as player (or was there before time change)
                if getattr(_ctg, "loc", None) == store.CurrentLocation or _ctg.gid in _gwwp:
                    continue
                _ctf = getattr(_ctg, "intimacy_flags", set()) or set()
                if not _ctf.intersection({"hj", "tj", "bj", "sex", "rub"}):
                    continue
                # Cannot be dating player (flirty tease, not girlfriend behavior)
                if hasattr(_ctg, "is_dating_player") and _ctg.is_dating_player():
                    continue
                if not photo_text_ready(_ctg, "camera tease"):   # one photo text every PHOTO_TEXT_GAP days, whatever the kind
                    continue
                # Higher chance for camera_lover
                _ct_chance = 0.30 if (hasattr(_ctg, "has_trait") and _ctg.has_trait("camera_lover")) else 0.10
                if renpy.random.random() > _ct_chance:
                    continue
                _camtease_girl = _ctg
                break
        if _camtease_girl is not None:
            $ _camtease_girl._camtease_photo_day = Day
            $ photo_text_sent(_camtease_girl, "camera tease")
            call _camtease_photo_event(_camtease_girl) from _call_camtease_photo

    # 6l) Femdom phone order (femdom_phone_order.rpy): a femdom girl texts him to be at her room tonight (Morning,
    #     Midday or Evening; the order is for that Night, judged by 5g). One pending order at a time.
    if TimeIndex < NIGHT_INDEX:
        $ _fdo_girl = femdom_phone_order_pick()
        if _fdo_girl is not None:
            call _femdom_phone_order_event(_fdo_girl) from _call_femdom_phone_order

    # 6m) Family dinner slot ping (shion_family.rpy): the Evening of a dinner day, him not at the apartment yet,
    #     his father texts once more so the dinner is not forgotten (the author 2026-10-11, tester idea).
    #     Arriving late still counts (apartment_event_now takes TimeIndex >= FAMILY_DINNER_SLOT).
    if (family_route_on() and TimeIndex == FAMILY_DINNER_SLOT
            and CurrentLocation not in APARTMENT_ROOMS
            and getattr(store, "_family_dinner_slot_ping", 0) != Day
            and ((_family_dinner == "invited" and Day == _family_dinner_day)
                 or (_family_dinner == "done" and _family_dinner_weekly_day == Day))):
        $ store._family_dinner_slot_ping = Day
        play sound "audio/Notification.mp3" noloop
        $ Narration(_("Your phone buzzes. A message from your father."))
        $ phone_add_msg(Dad.gid, Dad.gid, _tl(_("On my way home. Dinner's waiting when you get here.")))
        $ print("[FAMILY] dinner slot ping (Day %d)" % Day)

    # 6k) Children: at most ONE phone event per morning for all mothers together (children.rpy _CHILD_EVENTS:
    #     her text from the week away, her comment on the support money, baby news he can answer)
    if TimeIndex == 0:
        $ _child_ev = children_morning_pick()
        if _child_ev is not None:
            call _child_morning_event(_child_ev[0], GIRL_BY_ID[_child_ev[1]]) from _call_child_morning_event

    # 6i) Sunday weekly workout penalty notification
    if getattr(store, "_weekly_energy_lost", False):
        $ store._weekly_energy_lost = False
        "You've been eating too much pizza and not exercising enough. Your body feels sluggish. {b}Max Energy down!{/b} (Max Energy: [Player.energy_max]/5)"

    # 6c) BigFans daily earnings notification
    $ _bf_earned = getattr(store, "_bigfans_daily_earned", 0)
    if _bf_earned and _bf_earned > 0:
        $ store._bigfans_daily_earned = 0
        play sound "audio/Big Fans Notification.mp3" noloop
        "Your BigFans videos earned {b}$[_bf_earned]{/b} today!"

    # 6d) BigFans new requests notification (only if player has recorded videos)
    $ _bf_new = getattr(store, "_bigfans_new_count", 0)
    if _bf_new and _bf_new > 0 and len(getattr(store.Player, "recorded_videos", [])) > 0:
        $ store._bigfans_new_count = 0
        play sound "audio/Big Fans Notification.mp3" noloop
        "You got [_bf_new] new request(s) on BigFans. Check your phone!"

    # 6e) Hardcore Relationship warnings (morning only)
    python:
        _hc_warns = getattr(store, "_hc_warnings", [])
    if _hc_warns and len(_hc_warns) > 0 and TimeIndex == 0:
        python:
            store._hc_warnings = []
            for _hw_entry in _hc_warns:
                if isinstance(_hw_entry, tuple):
                    _hw_name, _hw_fem = _hw_entry
                else:
                    _hw_name, _hw_fem = _hw_entry, False
                _hw_pl = _tl(_("girlfriend")) if _hw_fem else _tl(_("boyfriend"))
                renpy.say(None, _tl(_("{b}%s{/b} is getting closer to her %s. You haven't given her enough attention.")) % (_hw_name, _hw_pl))

    # 6f) Hardcore Relationship BF escalation notifications (morning only)
    python:
        _hc_escs = getattr(store, "_hc_escalations", [])
    if _hc_escs and len(_hc_escs) > 0 and TimeIndex == 0:
        python:
            store._hc_escalations = []
            for _esc_entry in _hc_escs:
                if isinstance(_esc_entry, tuple):
                    _esc_name, _esc_fem = _esc_entry
                else:
                    _esc_name, _esc_fem = _esc_entry, False
                _esc_pl = _tl(_("girlfriend")) if _esc_fem else _tl(_("boyfriend"))
                renpy.say(None, _tl(_("{b}%s{/b} has been neglected and is discovering new things with her %s.")) % (_esc_name, _esc_pl))

    # 6g) Hardcore Relationship — Love maxed (platonic love notification)
    python:
        _hc_plat = getattr(store, "_hc_platonic", [])
    if _hc_plat and len(_hc_plat) > 0 and TimeIndex == 0:
        python:
            store._hc_platonic = []
            for _hp_entry in _hc_plat:
                if isinstance(_hp_entry, tuple):
                    _hp_name, _hp_fem = _hp_entry
                else:
                    _hp_name, _hp_fem = _hp_entry, False
                _hp_pl = _tl(_("girlfriend")) if _hp_fem else _tl(_("boyfriend"))
                renpy.say(None, _tl(_("{b}%s{/b} is now deeply in love with you. She won't pursue her %s anymore.")) % (_hp_name, _hp_pl))

    # 6h) Hardcore — single girl neglect warnings
    python:
        _hc_single_warns = getattr(store, "_hc_single_warnings", [])
    if _hc_single_warns and len(_hc_single_warns) > 0 and TimeIndex == 0:
        python:
            store._hc_single_warnings = []
            for _sw_entry in _hc_single_warns:
                _sw_name, _sw_type = _sw_entry
                if _sw_type == 1:
                    renpy.say(None, _tl(_("You don't seem to have given much attention to {b}%s{/b}. You notice she's been posting some sensual stories lately.")) % _sw_name)
                else:
                    renpy.say(None, _tl(_("You haven't given much attention to {b}%s{/b}. She seems to be meeting new people.")) % _sw_name)

    # 6i) Hardcore — single girl got a partner (Instabook announcement)
    python:
        _hc_new_partners = getattr(store, "_hc_new_partner", [])
    if _hc_new_partners and len(_hc_new_partners) > 0 and TimeIndex == 0:
        python:
            store._hc_new_partner = []
            for _np_entry in _hc_new_partners:
                _np_girl_name, _np_npc_name = _np_entry
                renpy.say(None, _tl(_("You check Instabook and {b}%s{/b} seems to have entered a relationship with {b}%s{/b}.")) % (_np_girl_name, _np_npc_name))

    # 6i2) Instabook: her birth post, the morning after she is back with the baby (children.rpy)
    if TimeIndex == 0 and getattr(store, "_child_birth_posts", None):
        python:
            for _cbp_line in child_birth_post_lines():
                Narration(_cbp_line)

    # 6j) Hardcore Relationship — girl goes back to BF after 5 days neglect
    if getattr(store, "hardcore_relationship", False) and TimeIndex == 0:
        python:
            _hc_return_girl = None
            for _hcg in girls_reachable():   # a week at her parents' is not "5 days of neglect"
                _dump_day = getattr(_hcg, "_hc_bf_dumped_day", 0) or 0
                if _dump_day <= 0:
                    continue
                if _hcg.has_npc_partner():
                    continue
                _last_int = getattr(_hcg, "_hc_last_interaction_day", 0) or 0
                _days_no_contact = Day - max(_dump_day, _last_int)
                if _days_no_contact >= 5:
                    _hc_return_girl = _hcg
                    break
        if _hc_return_girl is not None:
            call _hc_bf_return_event(_hc_return_girl) from _call_hc_bf_return

    # 6z) NPC catch message event (girl texts about breakup/reconciliation)
    if TimeIndex == 0:
        python:
            _npc_msg_girl = None
            for _nmg in girls_reachable():   # away: the flag stays, her text comes when she is back
                if getattr(_nmg, "_npc_catch_msg_pending", False):
                    _npc_msg_girl = _nmg
                    break
        if _npc_msg_girl is not None:
            call _npc_catch_message_event(_npc_msg_girl) from _call_npc_catch_msg_wait

    # 6zy) Harem acceptance phone event (GF caught player, accepted, asks about sharing)
    if TimeIndex == 0:
        python:
            _harem_ask_girl = None
            # away: the flag stays pending until she is back. Same when ANOTHER member of the harem group is away:
            # the event can end in a group vote, and nothing is decided without her (_harem_away_members).
            for _hag in ([] if _harem_away_members() else girls_reachable()):
                if getattr(_hag, "_harem_ask_pending", False):
                    _harem_ask_girl = _hag
                    break
        if _harem_ask_girl is not None:
            call _harem_ask_phone_event(_harem_ask_girl) from _call_harem_ask_phone

    # 6zy2) GF-initiated open relationship suggestion (trigger + Love + Inbt >= 1400)
    if TimeIndex == 0:
        python:
            _gf_suggest_girl = None
            for _gsg in girls_reachable():
                if not _gsg.is_dating_player():
                    continue
                if getattr(_gsg, "_open_relationship_consent", False):
                    continue
                if getattr(store, "_harem_group_id", None) is not None and _gsg.gid in (_get_harem_group() or {}).get("members", []):
                    continue
                # Must have a concrete trigger (flirt witness, threesome, caught)
                _gsg_trigger = getattr(_gsg, "_gf_open_rel_trigger", None)
                if _gsg_trigger is None:
                    continue
                _gsg_declined_day = getattr(_gsg, "_open_rel_declined_day", -999)
                if (store.Day - _gsg_declined_day) < 14:
                    continue
                if hasattr(_gsg, "has_temp_status") and _gsg.has_temp_status("angry"):
                    continue
                if (getattr(_gsg, "Love", 0) + getattr(_gsg, "Inbt", 0)) >= 1400:
                    _gf_suggest_girl = _gsg
                    print("[HAREM_GF_SUGGEST] %s qualifies (Love=%d Inbt=%d trigger=%s)" % (_gsg.gid, _gsg.Love, _gsg.Inbt, _gsg_trigger))
                    break
        if _gf_suggest_girl is not None:
            call _gf_suggests_open_rel(_gf_suggest_girl) from _call_gf_suggests_open

    # 6zz) NTR activation/level-up message event (NPC partner texts player)
    if TimeIndex == 0:
        python:
            _ntr_msg_girl = None
            for _nmg in ALL_GIRLS:
                if getattr(_nmg, "_ntr_activation_msg_pending", False):
                    _ntr_msg_girl = _nmg
                    break
        if _ntr_msg_girl is not None:
            call _ntr_activation_message_event(_ntr_msg_girl) from _call_ntr_activation_msg

    # 6zz2) The father's text of this morning (shion_family.rpy): the first dinner (invitation, reminder, missed),
    #       his business trips. One a morning.
    if TimeIndex == 0:
        $ _dad_key = dad_morning_text()
        if _dad_key is not None:
            call _dad_text_event(_dad_key) from _call_dad_text_event

    # 6zz3) His stepmother's text about his girlfriend (family_grades.rpy), every few days while he is dating
    $ _fgf_now = family_gf_text_now()
    if _fgf_now is not None:
        call _family_gf_text(_fgf_now[0], _fgf_now[1]) from _call_family_gf_text

    # 6zz4) Her story (story_steps.rpy, "text"): she texts him (an event of her step, never when she is with him)
    $ _story_txt = story_event_now("text")
    if _story_txt is not None:
        call story_event_play(_story_txt[0], _story_txt[1]) from _call_story_event_text

    # 6zz5) Her story (story_steps.rpy, "morning"): a morning event of hers. One that takes him somewhere returns from
    #       Wait, as the activity buddy below (it consumed its slot with its own Apply_Time_Cost)
    if TimeIndex == 0:
        $ store._story_morning_moved = False
        $ _story_mrn = story_event_now("morning")
        if _story_mrn is not None:
            call story_event_play(_story_mrn[0], _story_mrn[1]) from _call_story_event_morning
            if store._story_morning_moved:
                return
        else:
            # her call could have come this morning and did not: what is missing (story_unlock_hint)
            call story_unlock_hint_say("morning") from _call_story_hint_morning

    # 6zzz) Activity buddy invite check (was 5f, ABOVE the morning region). Accepting it returns from Wait:
    #       up there that skipped the whole morning of that Day (Friday allowance lost for good, investor income,
    #       the morning-after flags slipping a day). Here the morning has already run, and the outer Wait of a
    #       nested pair (it jumps over this) no longer rolls a second invite.
    $ store._buddy_invite_accepted = False
    python:
        _buddy_result = _buddy_check_all() if callable(globals().get("_buddy_check_all", None)) else None
    if _buddy_result is not None:
        call _activity_buddy_invite(_buddy_result[0], _buddy_result[1]) from _call_buddy_invite
        if store._buddy_invite_accepted:
            return

    # `hide`: a plain label would become the base of the translation ids of every say statement below it (the
    # photo event labels further down start with "_", so their ids hang from "Wait") and orphan their PT / ES blocks
    label .wait_morning_done hide:

    # 7) Safety: clear transient flags before returning to sandbox
    $ store._in_event = False
    $ store._phone_is_open = False

    # 8) Refresh the scene for the current location/time
    call Set_Scene(entry=True) from _call_Set_Scene_16

    return

# ============================================================
# Hardcore Relationship: girl returns to BF after neglect
# ============================================================
label _hc_bf_return_event(girl):

    python:
        # The partner was cleared at the breakup (clear_npc_partner wipes partner_is_female), so the flag is
        # always False here: read the ex's gender from the id saved by _ask_breakup instead.
        _hcr_pf = girl.resolve_npc_partner_gender(getattr(girl, "_hc_bf_dumped_npc", None)) == "female"
        print("[HC_RETURN] %s: event start, ex id=%s female=%s" % (girl.gid, getattr(girl, "_hc_bf_dumped_npc", None), _hcr_pf))
        # translated pronouns (PT / ES): they go into translated templates below
        _hcr_pp = _tr("she") if _hcr_pf else _tr("he")
        _hcr_Pp = _tr("She") if _hcr_pf else _tr("He")
        _hcr_po = _tr("her_obj") if _hcr_pf else _tr("him")

    play sound "audio/Notification.mp3" noloop
    "Your phone buzzes. Someone sent you a message."

    # Open phone chat and deliver messages one by one with typing
    # (inline typing to pass choices=[] and hide action buttons throughout)
    $ phone_add_msg(girl.gid, girl.gid, None, "typing")
    call screen phone_chat_screen(girl, auto_close=renpy.random.uniform(0.8, 1.4), choices=[])
    python:
        _t = phone_get_msgs(girl.gid)
        if _t and _t[-1].get("type") == "typing": _t.pop()
        phone_add_msg(girl.gid, girl.gid, _tl(_("Hey...")))

    $ phone_add_msg(girl.gid, girl.gid, None, "typing")
    call screen phone_chat_screen(girl, auto_close=renpy.random.uniform(0.8, 1.4), choices=[])
    python:
        _t = phone_get_msgs(girl.gid)
        if _t and _t[-1].get("type") == "typing": _t.pop()
        phone_add_msg(girl.gid, girl.gid, _tl(_("I've been thinking a lot these past few days.")))

    $ phone_add_msg(girl.gid, girl.gid, None, "typing")
    call screen phone_chat_screen(girl, auto_close=renpy.random.uniform(0.8, 1.4), choices=[])
    python:
        _t = phone_get_msgs(girl.gid)
        if _t and _t[-1].get("type") == "typing": _t.pop()
        phone_add_msg(girl.gid, girl.gid, _tl_fmt(_("You asked me to leave %s for you. And I did. Because I thought you cared."), _hcr_po))

    $ phone_add_msg(girl.gid, girl.gid, None, "typing")
    call screen phone_chat_screen(girl, auto_close=renpy.random.uniform(0.8, 1.4), choices=[])
    python:
        _t = phone_get_msgs(girl.gid)
        if _t and _t[-1].get("type") == "typing": _t.pop()
        phone_add_msg(girl.gid, girl.gid, _tl(_("But you haven't talked to me since. You haven't even looked at me.")))

    $ phone_add_msg(girl.gid, girl.gid, None, "typing")
    call screen phone_chat_screen(girl, auto_close=renpy.random.uniform(0.8, 1.4), choices=[])
    python:
        _t = phone_get_msgs(girl.gid)
        if _t and _t[-1].get("type") == "typing": _t.pop()
        phone_add_msg(girl.gid, girl.gid, _tl(_("I felt like an idiot. Like I gave up something real for nothing.")))

    $ phone_add_msg(girl.gid, girl.gid, None, "typing")
    call screen phone_chat_screen(girl, auto_close=renpy.random.uniform(0.8, 1.4), choices=[])
    python:
        _t = phone_get_msgs(girl.gid)
        if _t and _t[-1].get("type") == "typing": _t.pop()
        phone_add_msg(girl.gid, girl.gid, _tl_fmt(_("So... I talked to %s. And %s wants me back."), _hcr_po, _hcr_pp))

    $ phone_add_msg(girl.gid, girl.gid, None, "typing")
    call screen phone_chat_screen(girl, auto_close=renpy.random.uniform(0.8, 1.4), choices=[])
    python:
        _t = phone_get_msgs(girl.gid)
        if _t and _t[-1].get("type") == "typing": _t.pop()
        phone_add_msg(girl.gid, girl.gid, _tl_fmt(_("I'm going back to %s. At least %s pays attention to me."), _hcr_po, _hcr_pp))

    # Show choices inside the phone chat
    python:
        _hc_ret_choices = [
            (_tl(_("I'm sorry. I'll do better, I promise.")), "apologize"),
            (_tl(_("I understand. I'm sorry I hurt you.")), "understand"),
            (_tl(_("You'll come back for my dick anyway.")), "cocky"),
        ]
    call screen phone_chat_screen(girl, choices=_hc_ret_choices)
    $ _hc_ret_pick = _return

    if _hc_ret_pick == "apologize":
        $ phone_add_msg(girl.gid, "player", _tl(_("I'm sorry. I'll do better, I promise.")))
        call _hc_ret_typing(girl) from _typing_hc_ret_r1
        $ phone_add_msg(girl.gid, girl.gid, _tl_fmt(_("...You said that already by asking me to leave %s."), _hcr_po))
        call _hc_ret_typing(girl) from _typing_hc_ret_r1b
        python:
            phone_add_msg(girl.gid, girl.gid, _tl(_("I'll give you one more chance. But if you disappear again, I'm done.")))
            Change_Status(girl, "Love", -30)
            girl._hc_bf_dumped_day = store.Day
        call screen phone_chat_screen(girl, choices=[])

    elif _hc_ret_pick == "understand":
        $ phone_add_msg(girl.gid, "player", _tl(_("I understand. I'm sorry I hurt you.")))
        call _hc_ret_typing(girl) from _typing_hc_ret_r2
        $ phone_add_msg(girl.gid, girl.gid, _tl(_("...Thank you. That means more than you think.")))
        call _hc_ret_typing(girl) from _typing_hc_ret_r2b
        python:
            phone_add_msg(girl.gid, girl.gid, _tl(_("Take care of yourself, okay?")))
            Change_Status(girl, "Love", 20)
            girl.restore_ex_npc_partner()
            girl._hc_bf_dumped_day = 0
        call screen phone_chat_screen(girl, choices=[])

    elif _hc_ret_pick == "cocky":
        $ phone_add_msg(girl.gid, "player", _tl(_("You'll come back for my dick anyway.")))
        call _hc_ret_typing(girl) from _typing_hc_ret_r3
        $ phone_add_msg(girl.gid, girl.gid, _tl(_("You're disgusting.")))
        call _hc_ret_typing(girl) from _typing_hc_ret_r3b
        python:
            _pf = getattr(girl, "player_firsts", {})
            _had_sex = _pf.get("sex", False) or _pf.get("sex_raw", False)
            if _had_sex:
                phone_add_msg(girl.gid, girl.gid, _tl(_("I know your dick goes so deep inside me... and that you make me cum so hard...")))
            else:
                phone_add_msg(girl.gid, girl.gid, _tl(_("I know your dick is big and... good....")))
        call _hc_ret_typing(girl) from _typing_hc_ret_r3c
        python:
            phone_add_msg(girl.gid, girl.gid, _tl_fmt(_("But %s treats me better!"), _hcr_pp))
            Change_Status(girl, "Love", -40)
            Change_Status(girl, "Obed", 30)
            girl.restore_ex_npc_partner()
            girl._hc_bf_dumped_day = 0
        call screen phone_chat_screen(girl, choices=[])

    return

# Typing helper for _hc_bf_return_event (hides action buttons)
label _hc_ret_typing(girl):
    $ phone_add_msg(girl.gid, girl.gid, None, "typing")
    call screen phone_chat_screen(girl, auto_close=renpy.random.uniform(0.8, 1.4), choices=[])
    python:
        _t = phone_get_msgs(girl.gid)
        if _t and _t[-1].get("type") == "typing": _t.pop()
    return

# ============================================================
# Masturbation photo event — girl sends naughty selfie
# ============================================================
label _masturbate_photo_event(girl):

    play sound "audio/Notification.mp3" noloop
    "Your phone buzzes. Someone sent you a message."

    # Pick message based on traits (priority order)
    python:
        _has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()

        if _has_bf:
            _mast_lines = [
                _("You're driving me crazy... %(Pp)s's right here sleeping..."),
                _("I can't stop thinking about you... %(Pp)s's asleep next to me..."),
                _("This is so wrong... %(pp)s's in the other room... but I need you to see this..."),
            ]
        elif girl.has_trait("cum_slut"):
            _mast_lines = [
                _("I can't stop thinking about you filling me up... We need to meet soon."),
            ]
            # lines that remember something only where it happened
            if getattr(girl, "CreampieCounts", 0) > 0:
                _mast_lines.append(_("Thinking about your cum dripping out of me... Are you free later?"))
            if girl_act_counts(girl)[0] > 0:
                _mast_lines.append(_("I need you inside me again... This isn't enough anymore..."))
        # being put in her place is submissive, not hardcore (docs/plan_femdom.md D3)
        elif girl.has_trait("submissive"):
            _mast_lines = [
                _("I'm so worked up... I need you to put me in my place tonight."),
                _("I touched myself thinking about you telling me what to do... Give me orders tonight?"),
                _("I'm all yours tonight. Just tell me what you want me to do."),
            ]
        # a femdom gives orders even in a selfie (docs/plan_femdom.md 7). Veteran only: while she is still
        # discovering the trait its voice stays silent (trait_line_keys) and the next pool speaks.
        elif trait_is_veteran(girl, "femdom"):
            _mast_lines = [
                _("I had to take care of myself because you weren't here. Next time, you do it. That's an order."),
                _("Look what you made me do. Now come here and earn the real thing."),
                _("This is what you're missing. Be ready when I call, and maybe you'll get it."),
            ]
        elif girl.has_trait("hardcore_sex"):
            _mast_lines = [
                _("I need a few slaps to calm me down... Are you free later?"),
                _("My hand isn't rough enough... I need yours. Come over?"),
            ]
        elif girl.has_trait("exhibitionist") or girl.has_trait("camera_lover"):
            _mast_lines = [
                _("Just wanted to give you a little gift to remind you of me... I look good on camera, don't I?"),
                _("Thought you'd enjoy a preview of tonight... You know I love when you watch."),
                _("I took this just for you... Maybe next time you can record the real thing?"),
            ]
        else:
            _mast_lines = [
                _("A little gift to brighten your day... I miss you."),
                _("Thinking of you... Hope this makes your day better."),
                _("I couldn't help myself... Don't show anyone, okay?"),
            ]

        _mast_text = _tl(renpy.random.choice(_mast_lines))
        if _has_bf:
            _mast_text = _format_partner_line(girl, _mast_text)

    $ phone_add_msg(girl.gid, girl.gid, None, "typing")
    call screen phone_chat_screen(girl, auto_close=renpy.random.uniform(0.8, 1.4), choices=[])
    python:
        _t = phone_get_msgs(girl.gid)
        if _t and _t[-1].get("type") == "typing": _t.pop()
        phone_add_msg(girl.gid, girl.gid, _mast_text)

    $ phone_add_msg(girl.gid, girl.gid, None, "typing")
    call screen phone_chat_screen(girl, auto_close=renpy.random.uniform(0.8, 1.4), choices=[])
    python:
        _t = phone_get_msgs(girl.gid)
        if _t and _t[-1].get("type") == "typing": _t.pop()
        phone_add_msg(girl.gid, girl.gid, "images/characters/%s/Photos/Masturbate.png" % girl_asset_folder(girl), "photo")

    call screen phone_chat_screen(girl, choices=[])

    return

# ============================================================
# Piercing photo event — girl sends selfie with new piercings
# ============================================================
label _piercing_photo_event(girl):

    play sound "audio/Notification.mp3" noloop
    "Your phone buzzes. Someone sent you a message."

    $ phone_add_msg(girl.gid, girl.gid, None, "typing")
    call screen phone_chat_screen(girl, auto_close=renpy.random.uniform(0.8, 1.4), choices=[])
    python:
        _t = phone_get_msgs(girl.gid)
        if _t and _t[-1].get("type") == "typing": _t.pop()
        phone_add_msg(girl.gid, girl.gid, _tl(_("Hey, thanks for the gift! I thought you'd like to see how they look...")))

    $ phone_add_msg(girl.gid, girl.gid, None, "typing")
    call screen phone_chat_screen(girl, auto_close=renpy.random.uniform(0.8, 1.4), choices=[])
    python:
        _t = phone_get_msgs(girl.gid)
        if _t and _t[-1].get("type") == "typing": _t.pop()
        _is_exb = getattr(girl, "Inbt", 0) >= 500 or (hasattr(girl, "has_trait") and girl.has_trait("exhibitionist"))
        if _is_exb:
            _photo_file = "New Piercings Exb.png"
        else:
            _photo_file = "New Piercings.png"
        phone_add_msg(girl.gid, girl.gid, "images/characters/%s/Photos/%s" % (girl_asset_folder(girl), _photo_file), "photo")

    call screen phone_chat_screen(girl, choices=[])

    return

# ============================================================
# TEASE PHOTO EVENT
# TeaseShy: clothed from behind, no face (Love >= 500, 1+ act)
# TeaseNude: nude version (higher Inbt, more experience)
# TeaseExb: shows face (exhibitionist / camera_lover)
# ============================================================
label _tease_photo_event(girl):

    play sound "audio/Notification.mp3" noloop
    "Your phone buzzes. Someone sent you a message."

    python:
        _has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        _partner_is_female = _has_bf and hasattr(girl, "get_flag") and girl.get_flag("partner_is_female")
        _is_exb = girl.has_trait("exhibitionist") or girl.has_trait("camera_lover")
        # femdom: veteran only (while she is discovering the trait its voice stays silent, trait_line_keys)
        _is_fd = trait_is_veteran(girl, "femdom")
        _is_hc = girl.has_trait("hardcore_sex")
        _is_cute = girl.has_trait("cute_sex")
        _inbt = getattr(girl, "Inbt", 0)
        _flags = getattr(girl, "intimacy_flags", set()) or set()
        _has_sex = "sex" in _flags

        if _is_exb:
            _photo_file = "TeaseExb.png"
            if not renpy.loadable("images/characters/%s/Photos/%s" % (girl_asset_folder(girl), _photo_file)):
                _photo_file = "TeaseNude.png" if (_has_sex and _inbt >= 600) else "TeaseShy.png"
        elif _has_sex and _inbt >= 600:
            _photo_file = "TeaseNude.png"
        else:
            _photo_file = "TeaseShy.png"

        if _is_exb:
            _tease_lines = [
                _("I look so good today... thought you'd appreciate the view. Notice anything? I'm showing my face this time~"),
                _("Feeling confident. Want a little preview of tonight? I'm not hiding anymore."),
                _("Took about twenty of these. This is the best one. You're welcome."),
            ]
        elif _has_bf and _partner_is_female:
            if _is_fd:
                _tease_lines = [
                    _("She's not home, so today I make the rules. Rule one: you look."),
                    _("I don't need her permission to send you this. Or anyone's. Look."),
                    _("She's away. Look all you want. Touching is something you'll have to earn."),
                ]
            elif _is_hc:
                _tease_lines = [
                    _("She's not home. I'm all yours... at least in this photo. For now."),
                    _("Being bad while she's away... want to see how bad?"),
                    _("She'd lose her mind if she saw this. Makes it so much hotter."),
                ]
            elif _is_cute:
                _tease_lines = [
                    _("I shouldn't be sending you this... but I couldn't help it. Don't tell anyone, okay?"),
                    _("She's at work... and I'm thinking about you. Is that wrong?"),
                    _("I feel so naughty sending this... but you make me want to be naughty."),
                ]
            else:
                _tease_lines = [
                    _("She's not home. This is for your eyes only."),
                    _("Being bad while she's away... and it's so much fun."),
                    _("She'd kill me for sending you this. That makes it hotter."),
                ]
        elif _has_bf:
            if _is_fd:
                _tease_lines = [
                    _("He's not home, so today I make the rules. Rule one: you look."),
                    _("I don't need his permission to send you this. Or anyone's. Look."),
                    _("He's away. Look all you want. Touching is something you'll have to earn."),
                ]
            elif _is_hc:
                _tease_lines = [
                    _("He's not home. I'm all yours... at least in this photo. For now."),
                    _("Being bad while he's away... want to see how bad?"),
                    _("He'd lose his mind if he saw this. Makes it so much hotter."),
                ]
            elif _is_cute:
                _tease_lines = [
                    _("I shouldn't be sending you this... but I couldn't help it. Don't tell anyone, okay?"),
                    _("He's at work... and I'm thinking about you. Is that wrong?"),
                    _("I feel so naughty sending this... but you make me want to be naughty."),
                ]
            else:
                _tease_lines = [
                    _("He's not home. This is for your eyes only."),
                    _("Being bad while he's away... and it's so much fun."),
                    _("He'd kill me for sending you this. That makes it hotter."),
                ]
        # being put in her place is submissive, not hardcore (docs/plan_femdom.md D3)
        elif girl.has_trait("submissive"):
            _tease_lines = [
                _("I need someone to put me in my place. You up for it?"),
                _("Took this because I thought you'd like it. Tell me what you want to see next."),
                _("Just say the word and I'm yours tonight."),
            ]
        elif _is_fd:
            _tease_lines = [
                _("Look. Now come here and earn it."),
                _("You get to look. Touching is a privilege, and you haven't earned it yet."),
                _("This is what you get if you behave. Don't make me wait."),
            ]
        elif _is_hc:
            _tease_lines = [
                _("Getting ready for you. Hope you're bringing your A-game tonight."),
                _("Feeling restless. Thought this might motivate you to come over."),
            ]
        elif _is_cute:
            _tease_lines = [
                _("I... I took this for you. Don't laugh, okay? I've never done this before..."),
                _("Miss you. Thought this might make your day a little better..."),
                _("Is it weird that I want you to see me like this? Just... don't share it."),
            ]
        else:
            _tease_lines = [
                _("Just being playful. Don't you like this side of me?"),
                _("Feeling a little naughty today. This is why."),
                _("Miss you. Thought this might remind you what you're missing."),
            ]

    $ phone_add_msg(girl.gid, girl.gid, None, "typing")
    call screen phone_chat_screen(girl, auto_close=renpy.random.uniform(0.8, 1.4), choices=[])
    python:
        _t = phone_get_msgs(girl.gid)
        if _t and _t[-1].get("type") == "typing": _t.pop()
        phone_add_msg(girl.gid, girl.gid, _tl(renpy.random.choice(_tease_lines)))

    $ phone_add_msg(girl.gid, girl.gid, None, "typing")
    call screen phone_chat_screen(girl, auto_close=renpy.random.uniform(0.8, 1.4), choices=[])
    python:
        _t = phone_get_msgs(girl.gid)
        if _t and _t[-1].get("type") == "typing": _t.pop()
        phone_add_msg(girl.gid, girl.gid, "images/characters/%s/Photos/%s" % (girl_asset_folder(girl), _photo_file), "photo")

    call screen phone_chat_screen(girl, choices=[])
    return

# ============================================================
# SPANKED PHOTO EVENT
# Next morning after heavy spanking (SpankLevel 7+)
# ============================================================
label _spanked_photo_event(girl):

    play sound "audio/Notification.mp3" noloop
    "Your phone buzzes. Someone sent you a message."

    python:
        _has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        _is_exb = girl.has_trait("exhibitionist") or girl.has_trait("camera_lover")
        _is_hc = girl.has_trait("hardcore_sex")
        _is_cs = girl.has_trait("cum_slut")

        if _is_exb:
            _photo_file = "SpankedExb.png"
            if not renpy.loadable("images/characters/%s/Photos/%s" % (girl_asset_folder(girl), _photo_file)):
                _photo_file = "SpankedShy.png"
        else:
            _photo_file = "SpankedShy.png"

        # femdom: veteran only (while she is discovering the trait its voice stays silent, trait_line_keys)
        if trait_is_veteran(girl, "femdom"):
            _spank_lines = [
                _("Look at what you did. I allowed it. Don't forget who allowed it."),
                _("Enjoy the view. Next time I'm the one holding the paddle."),
                _("Still red. Enjoy the photo, because next time it's your turn to bend over."),
            ]
        elif _is_hc:
            _spank_lines = [
                _("Look what you did to me yesterday. I LOVE it. Do it again tonight?"),
                _("Still sore from your hand. Best kind of sore. Here's the proof."),
                _("You left your mark on me. I wore it proudly all day. Want to add more?"),
            ]
        elif _has_bf:
            _spank_lines = [
                _("My {hint}%(pl)s{/hint} asked why I was sitting funny... I just smiled. Look what you did."),
                _("%(Pp)s has no idea why my ass is red. Our little secret. Check this out."),
                _("I can still feel your handprint... %(pp)s would never do this to me. Look."),
            ]
        elif _is_cs:
            _spank_lines = [
                _("You spanked me so hard yesterday... I'm still tingling. Want to see?"),
                _("I took this in the mirror this morning. You really went to town on me."),
                _("Still feeling it from yesterday. Took a photo for you... don't judge."),
            ]
        elif _is_exb:
            _spank_lines = [
                _("Look what you did! I almost showed everyone on campus. Thought you'd want the exclusive first."),
                _("I'm wearing this like a badge of honor. Check out your handiwork."),
                _("Took this photo right after. The marks are still there. I'm kind of proud."),
            ]
        else:
            _spank_lines = [
                _("You really left a mark on me yesterday... look at this."),
                _("I took this in the mirror this morning. I can't believe you did this."),
                _("I'm still sore from yesterday... thought you should see what you did."),
            ]

    $ phone_add_msg(girl.gid, girl.gid, None, "typing")
    call screen phone_chat_screen(girl, auto_close=renpy.random.uniform(0.8, 1.4), choices=[])
    python:
        _t = phone_get_msgs(girl.gid)
        if _t and _t[-1].get("type") == "typing": _t.pop()
        _picked = renpy.random.choice(_spank_lines)
        _msg = _format_partner_line(girl, _picked) if _has_bf else _tl(_picked)
        phone_add_msg(girl.gid, girl.gid, _msg)

    $ phone_add_msg(girl.gid, girl.gid, None, "typing")
    call screen phone_chat_screen(girl, auto_close=renpy.random.uniform(0.8, 1.4), choices=[])
    python:
        _t = phone_get_msgs(girl.gid)
        if _t and _t[-1].get("type") == "typing": _t.pop()
        phone_add_msg(girl.gid, girl.gid, "images/characters/%s/Photos/%s" % (girl_asset_folder(girl), _photo_file), "photo")

    call screen phone_chat_screen(girl, choices=[])
    return

# ============================================================
# BIKINI PHOTO EVENT
# Morning after player gifted the bikini (one-shot)
# ============================================================
label _bikini_photo_event(girl):

    play sound "audio/Notification.mp3" noloop
    "Your phone buzzes. Someone sent you a message."

    python:
        _has_partner = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        _has_gf = _has_partner and girl.get_flag("partner_is_female")
        _has_bf = _has_partner and not _has_gf
        _is_exb = girl.has_trait("exhibitionist") or girl.has_trait("public_fetish")
        _is_shy = girl.has_trait("public_shy") or girl.has_trait("shy")
        _is_cam = girl.has_trait("camera_lover")

        _photo_file = "Black Bikini.png"

        if _is_exb:
            _bikini_lines = [
                _("I tried the bikini on... it's a little small, don't you think? I LOVE it. Should've gotten an even smaller one, like a thong."),
                _("Your gift fits perfectly... if by perfectly you mean barely covers anything. Next time get me something even tinier~"),
                _("Okay this bikini is TINY. And I couldn't be happier. Imagine me in dental floss at the pool..."),
            ]
        elif _is_shy:
            _bikini_lines = [
                _("I tried your bikini gift... don't you think it shows a bit too much skin? I feel so exposed..."),
                _("It's a little small, isn't it? I'm not sure I can wear this in public... what if people stare?"),
                _("Thanks for the bikini but... is this really a bikini or a napkin? I feel practically naked in it!"),
            ]
        elif _is_cam:
            _bikini_lines = [
                _("I tried the bikini on and took about fifty photos. This is the best one. You have GREAT taste in gifts."),
                _("New bikini = new photoshoot. The lighting was perfect this morning. Check this out."),
                _("Your gift is so cute! I'm going to take so many photos at the pool in this. Here's a preview."),
            ]
        elif _has_gf:
            _bikini_lines = [
                _("I tried your bikini on... my {hint}girlfriend{/hint} hasn't seen it yet. Not sure if she'd approve... but I'm wearing it anyway."),

                _("Your gift fits... barely. She doesn't know I got a bikini from a guy. Let's keep it between us."),
                _("It's a little small but I love it. My {hint}girlfriend{/hint} would probably have something to say about it... too bad I don't care."),

            ]
        elif _has_bf:
            _bikini_lines = [
                _("I tried your bikini on... my {hint}boyfriend{/hint} hasn't seen it yet. Not sure if he'd approve... but I'm wearing it anyway."),

                _("Your gift fits... barely. He doesn't know I got a bikini from another guy. Let's keep it between us."),
                _("It's a little small but I love it. My {hint}boyfriend{/hint} would probably have something to say about it... too bad I don't care."),

            ]
        # femdom: veteran only (while she is discovering the trait its voice stays silent, trait_line_keys)
        elif trait_is_veteran(girl, "femdom"):
            _bikini_lines = [
                _("Your bikini fits. You'll see it in person when I decide you've earned it."),
                _("Nice gift. Good boy. Here's your reward: one photo. Don't ask for more."),
                _("I'm wearing your bikini. Look, but don't get ideas. The ideas are mine."),
            ]
        else:
            _bikini_lines = [
                _("I tried the bikini on... it's a little small, isn't it? But honestly, it looks great. Thanks!"),
                _("Your gift barely covers anything! ...I kind of love it though. See for yourself."),
                _("Okay the bikini is a little smaller than expected... but it works. What do you think?"),
            ]

    $ phone_add_msg(girl.gid, girl.gid, None, "typing")
    call screen phone_chat_screen(girl, auto_close=renpy.random.uniform(0.8, 1.4), choices=[])
    python:
        _t = phone_get_msgs(girl.gid)
        if _t and _t[-1].get("type") == "typing": _t.pop()
        phone_add_msg(girl.gid, girl.gid, _tl(renpy.random.choice(_bikini_lines)))

    $ phone_add_msg(girl.gid, girl.gid, None, "typing")
    call screen phone_chat_screen(girl, auto_close=renpy.random.uniform(0.8, 1.4), choices=[])
    python:
        _t = phone_get_msgs(girl.gid)
        if _t and _t[-1].get("type") == "typing": _t.pop()
        phone_add_msg(girl.gid, girl.gid, "images/characters/%s/Photos/%s" % (girl_asset_folder(girl), _photo_file), "photo")

    call screen phone_chat_screen(girl, choices=[])
    return

# ============================================================
# SUGAR DADDY EVENT
# Morning after girl reaches financial attitude stage 3
# ============================================================
label _sugar_daddy_event(girl):

    play sound "audio/Notification.mp3" noloop
    "Your phone buzzes. Someone sent you a message."

    $ phone_add_msg(girl.gid, girl.gid, None, "typing")
    call screen phone_chat_screen(girl, auto_close=renpy.random.uniform(0.8, 1.4), choices=[])
    python:
        _t = phone_get_msgs(girl.gid)
        if _t and _t[-1].get("type") == "typing": _t.pop()
        phone_add_msg(girl.gid, girl.gid, _("Hey daddy. How are you?"))

    $ phone_add_msg(girl.gid, girl.gid, None, "typing")
    call screen phone_chat_screen(girl, auto_close=renpy.random.uniform(1.0, 1.6), choices=[])
    python:
        _t = phone_get_msgs(girl.gid)
        if _t and _t[-1].get("type") == "typing": _t.pop()
        phone_add_msg(girl.gid, girl.gid, _("I saw a BEAUTIFUL lingerie at the mall yesterday"))

    $ phone_add_msg(girl.gid, girl.gid, None, "typing")
    call screen phone_chat_screen(girl, auto_close=renpy.random.uniform(1.2, 1.8), choices=[])
    python:
        _t = phone_get_msgs(girl.gid)
        if _t and _t[-1].get("type") == "typing": _t.pop()
        phone_add_msg(girl.gid, girl.gid, _("I was thinking... Maybe you could give me the money to buy it"))

    $ phone_add_msg(girl.gid, girl.gid, None, "typing")
    call screen phone_chat_screen(girl, auto_close=renpy.random.uniform(0.8, 1.2), choices=[])
    python:
        _t = phone_get_msgs(girl.gid)
        if _t and _t[-1].get("type") == "typing": _t.pop()
        phone_add_msg(girl.gid, girl.gid, _("And I could give you something in exchange hehe"))

    call screen phone_chat_screen(girl, choices=[])

    $ unlock_achievement("sugar_daddy")
    return

# ============================================================
# CREAMPIE PHOTO EVENT
# Next morning after player told her "Don't clean it. Leave it."
# ============================================================
label _creampie_photo_event(girl):

    play sound "audio/Notification.mp3" noloop
    "Your phone buzzes. Someone sent you a message."

    python:
        _has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        _is_exb = girl.has_trait("exhibitionist") or girl.has_trait("camera_lover")
        _is_hc = girl.has_trait("hardcore_sex")
        _is_cs = girl.has_trait("cum_slut")

        if _is_exb:
            _photo_file = "CreampieExb.png"
        else:
            _photo_file = "CreampieShy.png"

        if _is_cs:
            _cream_lines = [
                _("I took this photo for you yesterday... your cum was still dripping out of me. I didn't clean it for hours~"),
                _("Remember when you told me to leave it? I did. ALL night. Here's the proof."),
                _("I fell asleep with your cum inside me. Woke up and took this. Miss you already."),
            ]
        elif _has_bf:
            _cream_lines = [
                _("I took this yesterday after you left... %(pp)s almost saw it dripping. Our secret."),
                _("Your cum was still inside me when %(pp)s came home. I took this photo to remember."),
                _("I had to shower before %(pp)s got back... but first I took this. For us."),
            ]
        # "I'm yours" is submissive, not hardcore (docs/plan_femdom.md D3)
        elif girl.has_trait("submissive"):
            _cream_lines = [
                _("I took this right after you left. Your mess, your mark. I'm yours."),
                _("I kept your cum inside me like a good girl. Here's the proof."),
                _("Your cum, your girl. Took this so you'd know who I belong to."),
            ]
        # femdom: veteran only (while she is discovering the trait its voice stays silent, trait_line_keys)
        elif trait_is_veteran(girl, "femdom"):
            _cream_lines = [
                _("I left it in because I felt like it, not because you told me to. Look."),
                _("Your mess, my rules. You'll make another one when I say so."),
                _("Look at this. Next time you ask permission before you cum in me. Maybe I'll say yes."),
            ]
        elif _is_hc:
            _cream_lines = [
                _("Kept your cum inside me all evening. Took this as proof. Do it again tonight."),
                _("Look what you did to me. I wore it like a trophy. Come make another mess."),
            ]
        elif _is_exb:
            _cream_lines = [
                _("I almost walked to class like this... took this photo instead. You're welcome."),
                _("Took this for you yesterday. Almost posted it online. Almost."),
                _("Your cum, my body, one camera. The result? This masterpiece."),
            ]
        else:
            _cream_lines = [
                _("I took this photo for you yesterday... I can't believe I'm sending this."),
                _("You told me to leave it... so I did. And I took a picture. Don't show anyone."),
                _("I never thought I'd take a photo like this... but you asked me to leave it, so..."),
            ]

    $ phone_add_msg(girl.gid, girl.gid, None, "typing")
    call screen phone_chat_screen(girl, auto_close=renpy.random.uniform(0.8, 1.4), choices=[])
    python:
        _t = phone_get_msgs(girl.gid)
        if _t and _t[-1].get("type") == "typing": _t.pop()
        phone_add_msg(girl.gid, girl.gid, _format_partner_line(girl, renpy.random.choice(_cream_lines)))

    $ phone_add_msg(girl.gid, girl.gid, None, "typing")
    call screen phone_chat_screen(girl, auto_close=renpy.random.uniform(0.8, 1.4), choices=[])
    python:
        _t = phone_get_msgs(girl.gid)
        if _t and _t[-1].get("type") == "typing": _t.pop()
        phone_add_msg(girl.gid, girl.gid, "images/characters/%s/Photos/%s" % (girl_asset_folder(girl), _photo_file), "photo")

    call screen phone_chat_screen(girl, choices=[])
    return

# ============================================================
# TEASE CAMERA PHOTO EVENT
# Girl sends a flirty camera selfie. Not dating the player.
# Higher chance if camera_lover. Requires 1+ sexual act.
# ============================================================
label _camtease_photo_event(girl):

    play sound "audio/Notification.mp3" noloop
    "Your phone buzzes. Someone sent you a message."

    python:
        _has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        _partner_is_female = _has_bf and hasattr(girl, "get_flag") and girl.get_flag("partner_is_female")
        _is_cam_lover = hasattr(girl, "has_trait") and girl.has_trait("camera_lover")
        _is_hc = hasattr(girl, "has_trait") and girl.has_trait("hardcore_sex")
        _is_cute = hasattr(girl, "has_trait") and girl.has_trait("cute_sex")

        if _is_cam_lover:
            _ct_lines = [
                _("I was bored and the lighting was perfect... so I took this. Just for you."),
                _("New angle, new pose. Tell me which one you like best... or I'll just keep sending more."),
                _("I've been practicing my poses. You're my test audience. Enjoy."),
                _("Camera loves me. I love the camera. And you get to enjoy both."),
            ]
        elif _has_bf and _partner_is_female:
            _ct_lines = [
                _("Giving you a little gift while she's away. Don't think I want anything more."),
                _("She doesn't know I'm sending this. And she won't. Right?"),
                _("Don't get the wrong idea. I'm just... bored. That's all."),
            ]
        elif _has_bf:
            _ct_lines = [
                _("He's out. I'm bored. And I thought of you... so here."),
                _("I shouldn't be sending this to someone who isn't my boyfriend... but here we are."),
                _("Took this while thinking about last time... don't tell anyone."),
            ]
        # femdom: veteran only (while she is discovering the trait its voice stays silent, trait_line_keys)
        elif trait_is_veteran(girl, "femdom"):
            _ct_lines = [
                _("Here's what you're missing. Come find me, and beg nicely."),
                _("You get a photo today. Behave and you might get more."),
                _("Look all you want. Touching is by invitation only."),
            ]
        elif _is_hc:
            _ct_lines = [
                _("Feeling myself tonight. Thought you should see what you're missing."),
                _("This is your reminder that I exist. And I look damn good."),
                _("Come over. Or don't. Either way, look at this."),
            ]
        elif _is_cute:
            _ct_lines = [
                _("I... tried taking a photo for you. Is this okay? I've never done this..."),
                _("Don't laugh, okay? I just wanted to send you something nice..."),
                _("I spent like thirty minutes on this... I hope you like it."),
            ]
        else:
            _ct_lines = [
                _("Felt cute. Thought of you. Here."),
                _("Random selfie for you. Don't read too much into it... or do."),
                _("Bored and looking good. You're the lucky recipient."),
            ]

    $ phone_add_msg(girl.gid, girl.gid, None, "typing")
    call screen phone_chat_screen(girl, auto_close=renpy.random.uniform(0.8, 1.4), choices=[])
    python:
        _t = phone_get_msgs(girl.gid)
        if _t and _t[-1].get("type") == "typing": _t.pop()
        phone_add_msg(girl.gid, girl.gid, _tl(renpy.random.choice(_ct_lines)))

    $ phone_add_msg(girl.gid, girl.gid, None, "typing")
    call screen phone_chat_screen(girl, auto_close=renpy.random.uniform(0.8, 1.4), choices=[])
    python:
        _t = phone_get_msgs(girl.gid)
        if _t and _t[-1].get("type") == "typing": _t.pop()
        phone_add_msg(girl.gid, girl.gid, "images/characters/%s/Photos/TeaseCamera.png" % girl_asset_folder(girl), "photo")

    call screen phone_chat_screen(girl, choices=[])
    return
