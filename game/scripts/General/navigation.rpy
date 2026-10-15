# ============================================
# NAVIGATION & SCENE HANDLING
# ============================================

init python:
    # Map each girl gid to her room location string
    GIRL_ROOMS = {
        "gwen": "gwen_room",
        "rogue": "rogue_room",
        "ntw": "ntw_room",
        "tenny": "tenny_room",
    }

    # The father's apartment (Downtown, off campus; Shion lives here). Reached through the Downtown crossroads (label
    # Downtown_Crossroads: campus "Go to Downtown"); the trip lands in the living room, the rooms are reached from
    # each other ("Go to the ..." in location_menu), "Leave (Downtown)" / "Back to Campus" are the ways out, from the
    # living room only (HOME_INNER_ROOMS). Family only: a girl following him who doesn't live there keeps him out
    # (apartment_company_block). The bathroom is a shower spot (SHOWER_SPOTS, Locations/Shower.rpy): found like the
    # campus showers.
    APARTMENT_ROOMS = ("apartment", "apartment_room", "apartment_shower")

    # Rooms inside a home with no front door of their own: no way out from there ("Leave (Downtown)" / "Back to
    # Campus" are not on their menu), he walks to the living room first (author, 2026-10-09)
    HOME_INNER_ROOMS = ("apartment_room", "apartment_shower")

    # Background variants by location and time of day
    _BG_VARIANTS = {
        "campus":     {2: "bg campus_evening", 3: "bg campus_night"},
        "room":       {3: "bg room_night"},
        "pool":       {2: "bg pool_evening", 3: "bg pool_night"},
        "gwen_room":  {3: "bg GwenRoom_night"},
        "rogue_room": {3: "bg RogueRoom_night"},
        "ntw_room":   {3: "bg NTWRoom_night"},
        "tenny_room":       {3: "bg TennyRoom_night"},
        "apartment":        {3: "bg apartment_night"},
        "apartment_room":   {3: "bg apartmentroom_night"},
        "apartment_shower": {3: "bg apartmentshower_night"},
    }
    _BG_DEFAULTS = {
        "campus": "bg campus", "room": "bg room_day", "pool": "bg pool_day",
        "showers": "bg showers", "classroom": "bg ClassRoom",
        "gwen_room": "bg GwenRoom", "rogue_room": "bg RogueRoom", "ntw_room": "bg NTWRoom",
        "tenny_room": "bg TennyRoom",
        "gym": "bg gym", "mall": "bg mall",
        "dressing_room": "bg dressing_room",
        "apartment": "bg apartment", "apartment_room": "bg apartment_room", "apartment_shower": "bg apartment_shower",
    }

    def get_bg_for_location(loc=None):
        """Return the bg image tag string for the given location and current TimeIndex."""
        if loc is None:
            loc = store.CurrentLocation
        variants = _BG_VARIANTS.get(loc, {})
        return variants.get(store.TimeIndex, _BG_DEFAULTS.get(loc, "black"))

    def _restore_clothing_on_move(girl):
        """Reset displaced/removed clothing when changing location.
        Girls fix their clothes when moving between areas."""
        if not hasattr(girl, "clothes_state"):
            return
        _any_displaced = False
        for slot, state in girl.clothes_state.items():
            if state != "full" and girl.clothes.get(slot):
                girl.clothes_state[slot] = "full"
                _any_displaced = True
        if _any_displaced:
            debug_log("[NAV] _restore_clothing_on_move: %s fixed displaced clothes" % getattr(girl, "gid", "?"))

    def navigate_to(to_location, girl=None):
        """
        Moves the player to another location.
        Any girl in Party will follow automatically.
        Does NOT handle time/round – that must be done in script.
        """
        global CurrentLocation, CurrentGirl, consecutive_room_sleeps

        # Reset the lazy-sleep counter whenever the player leaves the room
        if to_location != "room":
            consecutive_room_sleeps = 0

        # Unlock door when leaving a room
        if store.door_locked:
            print("[DOOR] Unlocked by navigate_to(%s) from %s" % (to_location, CurrentLocation))
        store.door_locked = False
        store._shy_door_prompted = False

        # Update player position
        CurrentLocation = to_location
        CurrentGirl = girl
        store._crowd_level = get_crowd_level(to_location)
        roster_clear_pins()

        # Girls in Party follow the player (never a girl who is away: girl_sent_away already took her out)
        for g in [_pg for _pg in Party if not girl_is_away(_pg)]:
            g.loc = to_location
            _gid = getattr(g, "gid", getattr(g, "Id", ""))

            # Restore displaced clothing (panties_side, chest_up, etc.)
            _restore_clothing_on_move(g)

            # Leaving showers: clear shower state + towel
            if to_location not in SHOWER_SPOTS:
                _clear_shower_outfit(g)

            # Going to pool with bikini
            if to_location == "pool" and getattr(g, "_bikini_unlocked", False) and _gid in OUTFIT_PRESETS and "pool" in OUTFIT_PRESETS[_gid]:
                g.WearPreset("pool", apply_now=False)
            # Leaving pool
            elif to_location != "pool" and getattr(g, "CurrentOutfitPreset", None) == "pool":
                g.WearPreset("casual", apply_now=False)

    def girls_on_scene(include_scene_girls=False):
        """
        Returns a list of girl objects that are actually present
        on the current scene. Uses renpy.showing() to check if the
        girl's sprite is actually visible, so HUD and sprite are
        always in sync regardless of girl.loc.

        include_scene_girls: also count a girl whose LIVE sex scene shows nothing under her own tag.
        Some scenes hide her sprite and re-tag every layer (the rimjob's rj_*, her split-leg sets:
        _SCENE_TAG_PREFIXES), so renpy.showing(girl) is False mid-scene and her HUD card vanished
        (tester 2026-10-10). The HUD passes True; the speech-bubble callers keep reading only the
        sprites they can actually see on screen.
        """
        return [g for g in ALL_GIRLS
                if (renpy.showing(g.Id) or (include_scene_girls and _girl_in_sex_scene(g)))
                and g.Id not in _sprite_suppressed]

    # ── Near/Far Roster System ──────────────────────────────────
    # Runtime-only (not saved). Rebuilt every Set_Scene.
    # Tracks which characters are visually on-screen (near, max 3)
    # vs present but off-screen (far).

    MAX_NEAR = 4

    def build_location_roster(girls_here, npc):
        """Build the near/far roster for the current location.
        girls_here: list of Girl objects at CurrentLocation.
        npc: NPCPartner or None.
        Returns {"near": [...], "far": [...]}, max MAX_NEAR near.
        Priority: pinned (player-called) > Party members > CurrentGirl > natural order.
        NPC is treated as a normal slot (not forced to last)."""
        all_present = []
        _party_set = set(id(g) for g in store.Party)
        _cur = store.CurrentGirl
        _pinned = getattr(store, "_roster_pinned_near", set())

        pinned_first = []
        party_next = []
        current_girl = []
        rest = []
        for g in girls_here:
            if id(g) in _pinned:
                pinned_first.append(g)
            elif id(g) in _party_set:
                party_next.append(g)
            elif g is _cur:
                current_girl.append(g)
            else:
                rest.append(g)
        if npc is not None:
            if id(npc) in _pinned:
                pinned_first.append(npc)
            else:
                rest.append(npc)
        # the family member in this room (his father in the apartment: family_father.rpy)
        for _fm in family_on_scene():
            (pinned_first if id(_fm) in _pinned else rest).append(_fm)
        all_present = pinned_first + party_next + current_girl + rest

        near = all_present[:MAX_NEAR]
        far = all_present[MAX_NEAR:]
        roster = {"near": near, "far": far}
        store._location_roster = roster
        print("[ROSTER] built for %s: near=[%s] far=[%s] pinned=%d" % (
            store.CurrentLocation,
            ", ".join(getattr(e, "Name", getattr(e, "name", "?")) for e in near),
            ", ".join(getattr(e, "Name", getattr(e, "name", "?")) for e in far),
            len(_pinned)))
        return roster

    def roster_get_near():
        r = getattr(store, "_location_roster", None)
        if r is None:
            return []
        return r.get("near", [])

    def roster_get_far():
        r = getattr(store, "_location_roster", None)
        if r is None:
            return []
        return r.get("far", [])

    def roster_is_far(entity):
        return entity in roster_get_far()

    def roster_is_near(entity):
        return entity in roster_get_near()

    def _roster_pin(entity):
        """Mark entity as player-called-near so rebuilds keep it near."""
        if not hasattr(store, "_roster_pinned_near"):
            store._roster_pinned_near = set()
        store._roster_pinned_near.add(id(entity))

    def _roster_unpin(entity):
        """Remove entity from pinned set."""
        _pinned = getattr(store, "_roster_pinned_near", None)
        if _pinned:
            _pinned.discard(id(entity))

    def roster_clear_pins():
        """Clear all pins (on navigation, location change, etc.)."""
        store._roster_pinned_near = set()

    def roster_call_near(entity):
        """Move entity from far to near (appended). If near was full,
        returns None without change -- use roster_swap instead."""
        r = getattr(store, "_location_roster", None)
        if r is None:
            return False
        near = r["near"]
        far = r["far"]
        if entity not in far:
            return False
        if len(near) >= MAX_NEAR:
            return False
        far.remove(entity)
        near.append(entity)
        _roster_pin(entity)
        _assign_near_sprite_locs(near)
        print("[ROSTER] call_near: %s added to near (pinned)" % getattr(entity, "Name", getattr(entity, "name", "?")))
        return True

    def roster_swap(incoming, outgoing):
        """Swap incoming (far) with outgoing (near). 1-for-1 trade."""
        r = getattr(store, "_location_roster", None)
        if r is None:
            return False
        near = r["near"]
        far = r["far"]
        if incoming not in far or outgoing not in near:
            return False
        idx = near.index(outgoing)
        near[idx] = incoming
        far.remove(incoming)
        far.append(outgoing)
        _roster_pin(incoming)
        _roster_unpin(outgoing)
        if hasattr(outgoing, "SpriteLoc"):
            outgoing.SpriteLoc = None
        _assign_near_sprite_locs(near)
        print("[ROSTER] swap: %s in (slot %d), %s out (pinned)" % (
            getattr(incoming, "Name", getattr(incoming, "name", "?")), idx,
            getattr(outgoing, "Name", getattr(outgoing, "name", "?"))))
        return True

    def roster_remove(entity):
        """Remove entity from roster (left the location).
        If near and far has members, promote first far to near.
        Repositions remaining near entities to match the new layout."""
        r = getattr(store, "_location_roster", None)
        if r is None:
            return
        near = r["near"]
        far = r["far"]
        was_near = entity in near
        if entity in near:
            near.remove(entity)
        if entity in far:
            far.remove(entity)
        _roster_unpin(entity)
        if was_near and far:
            promoted = far.pop(0)
            near.append(promoted)
        if was_near:
            _assign_near_sprite_locs(near)
            n = len(near)
            for idx, e in enumerate(near):
                tf = _get_slot_transform_for_index(idx, n)
                # a FamilyContact has no Id: renpy.showing("") is IndexError (tester 2026-10-10, the
                # father left alone in the living room when an angry girl walked out); no tag = re-show
                _e_id = getattr(e, "Id", "") or ""
                if isinstance(e, NPCPartner) or (_e_id and renpy.showing(_e_id)):
                    _roster_slide(e, tf)
                else:
                    _show_entity_sprite(e, near)
        if hasattr(entity, "SpriteLoc"):
            entity.SpriteLoc = None

    def roster_girl_leaves(girl):
        """She walks off the current location: sprite, roster, Party, CurrentGirl. She heads to her room
        (when her room is where you are: girl_home_exit). Returns where she went."""
        _dest = girl_home_loc(girl)
        if _dest == store.CurrentLocation:
            _dest = girl_home_exit(girl)
        hide_girl_sprite(girl)
        girl.loc = _dest
        if girl in store.Party:
            store.Party.remove(girl)
        roster_remove(girl)
        if store.CurrentGirl is girl:
            store.CurrentGirl = next((_e for _e in roster_get_near() if isinstance(_e, Girl)), None)
        print("[ROSTER] %s leaves %s for %s" % (girl.gid, store.CurrentLocation, _dest))
        return _dest

    def _assign_near_sprite_locs(near):
        """Set SpriteLoc on Girl objects in near list based on slot layout."""
        _SLOT_MAPS = {
            1: [StageCenter],
            2: [StageLeft, StageRight],
            3: [StageLeft, StageCenter, StageRight],
            4: [StageLeft, StageCenterLeft, StageCenterRight, StageRight],
        }
        smap = _SLOT_MAPS.get(len(near), _SLOT_MAPS[4])
        for idx, entity in enumerate(near):
            if idx < len(smap) and hasattr(entity, "SpriteLoc"):
                entity.SpriteLoc = smap[idx]

    def _get_slot_transform_for_index(idx, total):
        """Return the slot transform for position idx given total near count."""
        _SLOT_TRANSFORMS = {
            1: [slot_center],
            2: [slot_left, slot_right],
            3: [slot_left, slot_center, slot_right],
            4: [slot_left, slot_center_left, slot_center_right, slot_right],
        }
        slots = _SLOT_TRANSFORMS.get(total, _SLOT_TRANSFORMS[4])
        return slots[idx] if idx < len(slots) else slots[-1]

    def _show_entity_sprite(entity, near_list):
        """Show a single entity's sprite at its correct slot position."""
        idx = near_list.index(entity) if entity in near_list else -1
        if idx < 0:
            return
        tf = _get_slot_transform_for_index(idx, len(near_list))
        if isinstance(entity, NPCPartner):
            entity.show_sprite(tf)
        else:
            pose = getattr(entity, "default_pose", "standing")
            set_girl_sprite(entity.gid, pose=pose, at_list=[tf])

    def _roster_slide(entity, tf):
        """Move an already-visible entity to a new position. Does NOT rebuild
        the layeredimage -- just re-applies the transform on the existing show."""
        if isinstance(entity, NPCPartner) or getattr(entity, "is_family", False):
            _tag = entity.image_tag()
            _name = entity.image_name()
            renpy.show(_name, tag=_tag, at_list=[tf], zorder=5)
        else:
            _tag = entity.Id
            _cur = renpy.get_attributes(_tag)
            if _cur is not None:
                _full = _tag + " " + " ".join(_cur)
                renpy.show(_full, tag=_tag, at_list=[tf])
            else:
                pose = getattr(entity, "default_pose", "standing")
                set_girl_sprite(entity.gid, pose=pose, at_list=[tf])

    def _roster_anim(entity, tf):
        """Show an entity's sprite with a specific animation transform (full rebuild)."""
        if isinstance(entity, NPCPartner):
            entity.show_sprite(tf)
        else:
            pose = getattr(entity, "default_pose", "standing")
            set_girl_sprite(entity.gid, pose=pose, at_list=[tf])

    def show_roster_sprites(roster=None):
        """Hide all characters, then show near list at correct slots.
        Respects _sprite_suppressed for girls."""
        if roster is None:
            roster = getattr(store, "_location_roster", None)
        if roster is None:
            return

        for _g in ALL_GIRLS:
            hide_girl_sprite(_g)
        for _nh in NPC_PARTNERS.values():
            _nh.hide_sprite()
        for _fh in family_contacts():
            _fh.hide_sprite()

        near = roster.get("near", [])
        n = len(near)
        for idx, entity in enumerate(near):
            if idx >= MAX_NEAR:
                break
            tf = _get_slot_transform_for_index(idx, n)
            if isinstance(entity, NPCPartner) or getattr(entity, "is_family", False):
                entity.show_sprite(tf)
            else:
                if getattr(entity, "Id", None) in _sprite_suppressed:
                    continue
                _assign_near_sprite_locs(near)
                pose = getattr(entity, "default_pose", "standing")
                set_girl_sprite(entity.gid, pose=pose, at_list=[tf])

        for entity in roster.get("far", []):
            if hasattr(entity, "SpriteLoc"):
                entity.SpriteLoc = None

    def _apply_jealousy_expressions():
        """If a jealous GF (Jealousy >= 300) is near an intimate rival,
        set the GF's expression to side-eye angry (looking toward the rival).
        Only the jealous GF reacts, not the other girl."""
        roster = getattr(store, "_location_roster", None)
        if roster is None:
            return
        near = roster.get("near", [])
        near_girls = [(idx, e) for idx, e in enumerate(near) if isinstance(e, Girl)]
        if len(near_girls) < 2:
            return

        for gf_idx, gf in near_girls:
            if not gf.is_dating_player():
                continue
            jeal = getattr(gf, "Jealousy", 0)
            if jeal < 300:
                continue

            rival_idx = None
            for r_idx, r_girl in near_girls:
                if r_girl is gf:
                    continue
                if is_harem_exempt(gf, r_girl):
                    continue
                if getattr(r_girl, "intimacy_flags", None):
                    rival_idx = r_idx
                    break

            if rival_idx is None:
                continue

            if rival_idx > gf_idx:
                _eyes = "eyes_looking_right"
            else:
                _eyes = "eyes_looking_left"

            _brows = "brows_surprised"
            _mouth = "mouth_serious"

            n = len(near)
            tf = _get_slot_transform_for_index(gf_idx, n)
            set_girl_sprite(gf.gid, pose="standing", at_list=[tf],
                            eyes=_eyes, brows=_brows, mouth=_mouth)
            print("[JEALOUSY] %s side-eye toward rival at idx %d (Jealousy=%d)" % (gf.gid, rival_idx, jeal))

    def get_scheduled_location_for(girl, day, time_index):
        """
        Returns the location this girl should be in.
        Uses girl.schedule (may be modified by gym_rat etc.), falls back to GIRLS_CONFIG.
        While she is away for a reason (girl_away_reason: giving birth) her schedule is suspended.
        """
        if girl_away_reason(girl):
            return GIRL_AWAY_LOC
        schedule = getattr(girl, "schedule", None)
        if schedule is None:
            cfg = GIRLS_CONFIG.get(girl.gid)
            if not cfg:
                return girl.loc
            schedule = cfg.get("schedule", [])
        if not schedule:
            return girl.loc

        # Day treated as 1-based in game logic; adjust to 0-based index
        day_index = (day - 1) % len(schedule)
        day_row = schedule[day_index]

        # until he has met her at her home she stays there (family_father.rpy, GIRLS_CONFIG "meets_at_home")
        if 0 <= time_index < len(day_row):
            return girl_pre_intro_loc(girl, day_row[time_index])

        # Fallback: last entry in the row
        return girl_pre_intro_loc(girl, day_row[-1])

    # Friendly names for locations (for dialogue)
    LOC_NAMES = {
        "campus": "the campus",
        "pool": "the pool",
        "showers": "the showers",
        "room": "your room",
        "gwen_room": "my room",
        "rogue_room": "my room",
        "ntw_room": "my room",
        "tenny_room": "my room",
        "classroom": "the classroom",
        "gym": "the gym",
        "mall": "the mall",
        "apartment": "the apartment",
        "apartment_room": "the bedroom",
        "apartment_shower": "the bathroom",
    }

init python:
    TIME_COSTS = {
        "navigate": 5,
        "navigate_mall": 15,
        "navigate_apartment": 20,   # campus <-> the father's apartment, Downtown (each way)
        "chat": 10,
        "flirt": 10,
        "shower": 20,
        "shower_wait": 10,
        "swim": 30,
        "night_swim": 30,
        "action_attempt": 5,
        "strip": 1,             # one piece of clothing on / off (the approval check of it, _check_strip_approval)
        "sex_tick": 2,
        "study_min": 10,
        "attend_class_min": 50,
        "workout_min": 50,
    }

    # Places at the end of a trip away from campus -> the TIME_COSTS key of that trip. There is no "Leave (Campus)"
    # there (the 5-round walk of the campus places): "Back to Campus" costs the trip again.
    OFF_CAMPUS_TRIPS = {
        "mall": "navigate_mall",
        "apartment": "navigate_apartment", "apartment_room": "navigate_apartment", "apartment_shower": "navigate_apartment",
    }

    # The Downtown crossroads (label Downtown_Crossroads): the entry label of each way
    DOWNTOWN_ENTRY = {"campus": "Campus_Entry", "mall": "Mall_Entry", "apartment": "Apartment_Arrive"}

    def downtown_spot(loc):
        """The way of the crossroads a place is: "apartment" for any of its rooms, else the place ("campus", "mall")."""
        return "apartment" if loc in APARTMENT_ROOMS else loc

    def downtown_trip_cost(src, dst):
        """The trip between two ways of the crossroads: none back to where he came from; to or from campus, the trip
        of that place (OFF_CAMPUS_TRIPS); between the mall and the apartment, a walk (navigate)."""
        if src == dst:
            return 0
        if "campus" in (src, dst):
            return TIME_COSTS[OFF_CAMPUS_TRIPS[dst if src == "campus" else src]]
        return TIME_COSTS["navigate"]

    def apartment_company_block():
        """The girls following him who don't live in the father's apartment: family only, with any of them he can't go
        there (the button stays, disabled). A girl who lives there comes and goes with him, to campus too."""
        return [_g for _g in store.Party if girl_home_loc(_g) not in APARTMENT_ROOMS]

# -------------------------------------------------------
# Helper: apply time cost + optionally call Wait
# -------------------------------------------------------
label Apply_Time_Cost(cost=0):

    if cost > 0:
        $ advance_round(cost)

    if Round >= 100:
        $ LastPresentGirls = [g for g in ALL_GIRLS if g.loc == CurrentLocation]
        $ _atc_slots = Round // 100
        $ Round = Round % 100

        while _atc_slots > 0:
            $ _atc_pre_day = Day
            $ advance_time(1)
            $ _atc_slots -= 1
            $ store._atc_wait_done = True
            if not NightAutoSleepPending:
                $ _new_period = _tr(TIME_NAMES[TimeIndex]) if TimeIndex < len(TIME_NAMES) else "???"
                "It's now [_new_period]."
            call Wait from _call_Wait_1
            if Day != _atc_pre_day:
                $ _atc_slots = 0

    $ store._player_is_navigating = False

    return

init python:
    _LOC_LOOPS = {
        "room": "Player_Room_Loop",
        "campus": "Campus_Loop",
        "pool": "Pool_Loop",
        "gym": "Gym_Loop",
        "classroom": "Classroom_Loop",
        "showers": "Shower_Loop",
        "mall": "Mall_Loop",
        "apartment": "Apartment_Loop",
        "apartment_room": "Apartment_Loop",
        "apartment_shower": "Shower_Loop",
        "gwen_room": "Girls_Room_Loop",
        "rogue_room": "Girls_Room_Loop",
        "ntw_room": "Girls_Room_Loop",
        "tenny_room": "Girls_Room_Loop",
    }

    def _get_location_loop(loc):
        """Return the loop label for a location."""
        return _LOC_LOOPS.get(loc, "Campus_Loop")

    # ------------------------------------------------------------
    # FACES ON THE "GO TO ..." BUTTONS: who is at that place right now
    # ------------------------------------------------------------
    # A travel item of a menu names its place with the menu argument `nav` (a loc, or a list of locs for
    # "Go to Girls' Rooms..."); the choice screen puts the faces of the girls there on the button
    # (screen choice_faces_button). The same knowledge the phone gives (_tracker_loc_label): only with the
    # Girls Tracker, and never a girl who is away.
    # NAV_FACE / NAV_FACE_STEP / NAV_FACE_GAP (ring size, overlap, caption gap) are set by
    # apply_menu_scale (styles.rpy, MENU_SCALE_PRESETS): they follow Preferences > Menu Size.

    def nav_faces(nav):
        """[(avatar, ring color), ...] of the girls at the place(s) `nav` names; [] without the tracker."""
        if not nav or not Player.has_item("girls_tracker"):
            return []
        _locs = (nav,) if isinstance(nav, str) else tuple(nav)
        return [(_girl_avatar_by_gid(_g.gid), getattr(_g, "color", None) or "#94a3b8")
                for _g in ALL_GIRLS if _g.loc in _locs and not girl_is_away(_g)]

    # ------------------------------------------------------------
    # LEAKED CALL FRAMES (Ren'Py return stack)
    # ------------------------------------------------------------
    # A Ren'Py `jump` NEVER pops the return stack. Every X_Loop is `call location_menu` + `jump X_Loop`, and
    # every travel option of location_menu leaves with `jump Y_Entry`, so the frame pushed by the loop was
    # orphaned on each trip. Scene aborts do the same from much deeper (force_scene_reset + `jump main_loop`,
    # start_scene force_end, the phone's renpy.jump, the migration redirect): 5 to 8 frames each. Player
    # tracebacks showed 483 and 178 leaked frames. They are never returned into, but they are copied into
    # each of the 128 rollback entries and pickled on every save and menu-choice autosave.
    #
    # The sandbox loop labels are only ever reached with `jump` (nothing `call`s them) and they never
    # return, so whatever is on the return stack when one is reached is garbage: drop it there.
    #   - NEVER `call` a *_Loop label or main_loop: the trim would erase that call's return.
    #   - NEVER trim in *_Entry labels or in location_menu: Girls_Room_Entry / Shower_Entry return through
    #     the location_menu / choose_girl_room frames (those are pushed AFTER the trim, so they are safe).
    #   - NEVER use renpy.set_return_stack([]) (leaves the engine's abnormal / dynamic stacks stale), and
    #     never "fix" the leak by turning the jumps into returns on an untrimmed stack.
    # renpy.pop_call() drops a frame without resolving its label (removed `from` labels cannot break it)
    # and restores the dropped labels' parameters (girl, loc, action...) exactly like a normal return.
    _NAV_TRIM_ENABLED = True   # False = only log how many frames leaked and from where, drop nothing
    _SANDBOX_LOOP_LABELS = frozenset(_LOC_LOOPS.values()) | frozenset(["main_loop"])

    def _nav_trim_call_stack(tag="?"):
        """Drop every leaked call frame. Returns how many were dropped."""
        if renpy.context_nesting_level() != 0:
            print("[NAV_STACK] %s reached in a nested context (level=%d), not trimming" % (tag, renpy.context_nesting_level()))
            return 0
        _depth = renpy.call_stack_depth()
        if _depth <= 0:
            return 0
        _sites = renpy.get_return_stack()[-6:]
        if not _NAV_TRIM_ENABLED:
            print("[NAV_STACK] %s: %d leaked call frame(s) (trim disabled), innermost return sites=%s" % (tag, _depth, _sites))
            return 0
        while renpy.call_stack_depth() > 0:   # pop_call() raises on an empty stack with config.developer
            renpy.pop_call()
        print("[NAV_STACK] %s: dropped %d leaked call frame(s), innermost return sites=%s" % (tag, _depth, _sites))
        return _depth

    def _nav_trim_label_callback(name, abnormal):
        if name in _SANDBOX_LOOP_LABELS:
            _nav_trim_call_stack(name)

    config.label_callbacks.append(_nav_trim_label_callback)

    # ------------------------------------------------------------
    # [ROLLBACK_DIAG] (author 2026-10-11: a rollback in the middle of the marital bed event dropped him
    # on the MAIN MENU; log.txt showed only the restart, nothing on the way). Every interaction notes
    # where it is and its call stack in a ring kept on the renpy MODULE (outside the store: never rolled
    # back, survives the restart). The main menu prints it (label before_main_menu): the last lines say
    # where the rollback landed (rollback=True) and what the call stack held when the script ran out.
    # ------------------------------------------------------------
    _RB_DIAG_KEEP = 8

    def _rb_diag_note():
        try:
            _fl = renpy.get_filename_line()
            _buf = getattr(renpy, "_rb_diag_buf", None)
            if _buf is None:
                _buf = []
                renpy._rb_diag_buf = _buf
            _buf.append("Day %s slot %s %s:%s rollback=%s nest=%d depth=%d stack=%s" % (
                getattr(store, "Day", "?"), getattr(store, "TimeIndex", "?"), _fl[0], _fl[1],
                renpy.game.after_rollback, renpy.context_nesting_level(),
                renpy.call_stack_depth(), renpy.get_return_stack()[-5:]))
            del _buf[:-_RB_DIAG_KEEP]
        except Exception as _rbd_e:
            print("[ROLLBACK_DIAG] note failed: %r" % (_rbd_e,))

    config.start_interact_callbacks.append(_rb_diag_note)

# Every main menu prints the [ROLLBACK_DIAG] ring (_rb_diag_note): the Main Menu button's, and the bug's
label before_main_menu:
    python:
        _rbd_buf = getattr(renpy, "_rb_diag_buf", None)
        if _rbd_buf:
            print("[ROLLBACK_DIAG] main menu reached (the Main Menu button, or the script ran out of call stack). Last interactions, oldest first:")
            for _rbd_line in _rbd_buf:
                print("[ROLLBACK_DIAG]   %s" % _rbd_line)
            del _rbd_buf[:]
    return

# --------------------------------------------
# Main location menu (used by all *_Loop labels)
# --------------------------------------------
label location_menu:

    # ── Safety net: clear stale sex flags that should never be True here ──
    python:
        # THE one list (SCENE_GIRL_VARS, characters_stats.rpy). A hand-copied tuple here was missing
        # Shion's _scg/_srcg/_sdg: one of her scenes leaking its var kept player_in_sex_scene() True for
        # good: no phone on the HUD, no status clicks, reload kept it, until a force_scene_reset path
        # (getting caught) cleared the full list (tester 2026-10-10). The gid in the log names the leak.
        _stale_vars = []
        for _sv_name in SCENE_GIRL_VARS:
            _sv_ref = getattr(store, _sv_name, None)
            if _sv_ref is not None:
                _stale_vars.append("%s=%s" % (_sv_name, getattr(_sv_ref, "gid", _sv_ref)))
                setattr(store, _sv_name, None)
        if _stale_vars:
            print("[SAFETY_NET] location_menu cleared stale sex vars: %s" % _stale_vars)
        if store._in_event:
            print("[SAFETY_NET] location_menu cleared stale _in_event=True")
            store._in_event = False
        if store._sex_menu_active:
            print("[SAFETY_NET] location_menu cleared stale _sex_menu_active=True")
            store._sex_menu_active = False
        if getattr(store, "_recording_active", False):
            print("[SAFETY_NET] location_menu cleared stale _recording_active=True")
            finalize_recording()
        elif renpy.get_screen("recording_overlay"):
            print("[SAFETY_NET] location_menu cleared stale recording_overlay screen")
            renpy.hide_screen("recording_overlay")
        # A scripted scene (anniversary gift, NTR bet, her story's restricted scenes: story_steps.rpy) locks the clock
        # and marks itself restricted only inside its own flow; a scene that ended early (force end) jumps here with
        # both still on
        if getattr(store, "_time_locked", False):
            print("[SAFETY_NET] location_menu cleared a stale time lock (a scripted scene ended early)")
            time_unlock()
        if getattr(store, "_scene_restricted", False):
            print("[SAFETY_NET] location_menu cleared stale _scene_restricted=True")
            store._scene_restricted = False
        store._scene_cum_continues = False
    # ── Time transition guard (like Round10 in reference game) ──
    if Round >= 100:
        call Apply_Time_Cost(0) from _call_Apply_Time_Cost_round_guard

    # ── Catch pending auto-sleep (advance_round fired outside Apply_Time_Cost) ──
    if NightAutoSleepPending:
        $ NightAutoSleepPending = False
        $ Party = []
        if CurrentLocation != "room":
            "It's too late. You head back to your room."
            $ navigate_to("room", None)
            call Set_Scene(entry=False) from _call_Set_Scene_autosleep
        call do_sleep from _call_do_sleep_autosleep
        return

    # ── Force end of night: no time left at Night → auto-sleep ──
    if TimeIndex == NIGHT_INDEX and Round >= 90:
        if CurrentLocation != "room":
            "It's too late. You head back to your room."
            $ Party = []
            $ navigate_to("room", None)
            call Set_Scene(entry=False) from _call_Set_Scene_force_night
        call do_sleep from _call_do_sleep_forced
        return

    # Save current location to detect changes after calls
    $ _menu_loc = CurrentLocation

    # Which girls are at the same location as the player?
    $ girls_here = [girl for girl in ALL_GIRLS if girl.loc == CurrentLocation]
    # Validate NPC is actually at this location (can go stale after events)
    if _npc_on_scene is not None and getattr(_npc_on_scene, "loc", None) != CurrentLocation:
        $ store._npc_on_scene = None
    # Always rebuild roster for current location (handles Shower_Entry returns, etc.)
    $ resolve_npc_for_location(CurrentLocation)
    $ build_location_roster(girls_here, store._npc_on_scene)
    $ show_roster_sprites()
    # Would traveling (5 rounds) push us into Night?
    $ _night_or_closing = (TimeIndex == NIGHT_INDEX) or (TimeIndex == NIGHT_INDEX - 1 and (100 - Round) <= TIME_COSTS["navigate"])
    # The father's apartment (Events/shion_family.rpy): the first family dinner, her curfew at Night. The event
    # may send him away: the loop of wherever he is now starts over
    $ _apt_ev = apartment_event_now()
    if _apt_ev is not None:
        call expression "_apartment_" + _apt_ev from _call_apartment_event
        call Set_Scene(entry=True) from _call_Set_Scene_apartment_event
        jump expression _get_location_loop(CurrentLocation)

    # The story of a girl with one (story_steps.rpy): the unlock event of her step, or one of her step events. The
    # loop of wherever he is now starts over
    $ _story_now = story_event_now("location")
    if _story_now is not None:
        call story_event_play(_story_now[0], _story_now[1]) from _call_story_event_location
        call Set_Scene(entry=True) from _call_Set_Scene_story_event
        jump expression _get_location_loop(CurrentLocation)

    # Femdom phone order (femdom_phone_order.rpy): he came to her room the Night she ordered him there
    $ _fdo_here = femdom_phone_order_arrival()
    if _fdo_here is not None:
        call _femdom_phone_order_arrived(_fdo_here) from _call_femdom_phone_order_arrived

    # His phone order (player_phone_order.rpy): he walked into his room the Night he told a submissive to be there
    $ _ppo_here = player_phone_order_arrival()
    if _ppo_here is not None:
        call _player_phone_order_arrived(_ppo_here) from _call_player_phone_order_arrived

    menu:

        # -------------------------------------------------------
        # UNIVERSAL: CHAT (only if at least one girl is present)
        # -------------------------------------------------------
        "Chat..." if girls_here or _npc_on_scene is not None or family_on_scene():
            call do_talk(CurrentLocation, TimeIndex) from _call_do_talk
            if CurrentLocation != _menu_loc:
                call Set_Scene(entry=True) from _call_Set_Scene_menu_redir
                jump expression _get_location_loop(CurrentLocation)
            return

        # -------------------------------------------------------
        # CALL FAR CHARACTERS (only if roster has far members)
        # -------------------------------------------------------
        "[_tr('Call someone over...')]" if roster_get_far():
            call _show_call_menu from _call_show_call_menu
            return

        # -------------------------------------------------------
        # NAVIGATION OPTIONS - ONLY WHEN ON CAMPUS
        # -------------------------------------------------------
        "Go to Player Room" (nav="room") if CurrentLocation == "campus":
            $ _nav_origin = CurrentLocation
            $ store._player_is_navigating = True
            call Apply_Time_Cost(TIME_COSTS["navigate"]) from _call_Apply_Time_Cost_12
            if CurrentLocation != _nav_origin:
                call Set_Scene(entry=True) from _call_Set_Scene_redir_room
                return
            jump Player_Room_Entry

        "Go to Girls' Rooms..." (nav=list(GIRL_ROOMS.values())) if CurrentLocation == "campus":
            call choose_girl_room from _call_choose_girl_room
            return

        "Go to Class" (nav="classroom") if CurrentLocation == "campus" and not _night_or_closing:
            $ _nav_origin = CurrentLocation
            $ store._player_is_navigating = True
            call Apply_Time_Cost(TIME_COSTS["navigate"]) from _call_Apply_Time_Cost_13
            if CurrentLocation != _nav_origin:
                call Set_Scene(entry=True) from _call_Set_Scene_redir_class
                return
            jump Classroom_Entry

        "!disabled![_tr('Class (Closing soon)')]" if CurrentLocation == "campus" and _night_or_closing and TimeIndex != NIGHT_INDEX:
            return

        "!disabled![_tr('Class (Closed)')]" if CurrentLocation == "campus" and TimeIndex == NIGHT_INDEX:
            return

        "Go to Pool" (nav="pool") if CurrentLocation == "campus":
            $ _nav_origin = CurrentLocation
            $ store._player_is_navigating = True
            call Apply_Time_Cost(TIME_COSTS["navigate"]) from _call_Apply_Time_Cost_14
            if CurrentLocation != _nav_origin:
                call Set_Scene(entry=True) from _call_Set_Scene_redir_pool
                return
            jump Pool_Entry

        "Go to Gym" (nav="gym") if CurrentLocation == "campus" and not _night_or_closing:
            $ _nav_origin = CurrentLocation
            $ store._player_is_navigating = True
            call Apply_Time_Cost(TIME_COSTS["navigate"]) from _call_Apply_Time_Cost_15
            if CurrentLocation != _nav_origin:
                call Set_Scene(entry=True) from _call_Set_Scene_redir_gym
                return
            jump Gym_Entry

        "!disabled![_tr('Gym (Closing soon)')]" if CurrentLocation == "campus" and _night_or_closing and TimeIndex != NIGHT_INDEX:
            return

        "!disabled![_tr('Gym (Closed)')]" if CurrentLocation == "campus" and TimeIndex == NIGHT_INDEX:
            return

        "Go to Shower" (nav="showers") if CurrentLocation == "campus":
            $ _nav_origin = CurrentLocation
            $ store._player_is_navigating = True
            call Apply_Time_Cost(TIME_COSTS["navigate"]) from _call_Apply_Time_Cost_16
            if CurrentLocation != _nav_origin:
                call Set_Scene(entry=True) from _call_Set_Scene_redir_shower
                return
            $ _shower_spot = "showers"
            jump Shower_Entry

        # Off campus: the Downtown crossroads (the mall, the father's apartment; the trip is paid there)
        "Go to Downtown" (nav=["mall"] + list(APARTMENT_ROOMS)) if CurrentLocation == "campus":
            jump Downtown_Crossroads

        # -------------------------------------------------------
        # NAVIGATION INSIDE THE FATHER'S APARTMENT (the room he is in has no button)
        # -------------------------------------------------------
        "Go to the Living Room" (nav="apartment") if CurrentLocation in APARTMENT_ROOMS and CurrentLocation != "apartment":
            $ _nav_origin = CurrentLocation
            $ store._player_is_navigating = True
            call Apply_Time_Cost(TIME_COSTS["navigate"]) from _call_Apply_Time_Cost_apt_living
            if CurrentLocation != _nav_origin:
                call Set_Scene(entry=True) from _call_Set_Scene_redir_apt_living
                return
            jump Apartment_Entry

        "Go to the Bedroom" (nav="apartment_room") if CurrentLocation in APARTMENT_ROOMS and CurrentLocation != "apartment_room":
            $ _nav_origin = CurrentLocation
            $ store._player_is_navigating = True
            call Apply_Time_Cost(TIME_COSTS["navigate"]) from _call_Apply_Time_Cost_apt_bedroom
            if CurrentLocation != _nav_origin:
                call Set_Scene(entry=True) from _call_Set_Scene_redir_apt_bedroom
                return
            jump Apartment_Room_Entry

        "Go to the Bathroom" (nav="apartment_shower") if CurrentLocation in APARTMENT_ROOMS and CurrentLocation != "apartment_shower":
            $ _nav_origin = CurrentLocation
            $ store._player_is_navigating = True
            call Apply_Time_Cost(TIME_COSTS["navigate"]) from _call_Apply_Time_Cost_apt_bathroom
            if CurrentLocation != _nav_origin:
                call Set_Scene(entry=True) from _call_Set_Scene_redir_apt_bathroom
                return
            $ _shower_spot = "apartment_shower"
            jump Shower_Entry

        # -------------------------------------------------------
        # LOCAL ACTIONS BY LOCATION
        # -------------------------------------------------------

        # Player room or girls' rooms: study action (not at night)
        "Study" if CurrentLocation in ("room", "gwen_room", "rogue_room", "ntw_room", "tenny_room") and TimeIndex != NIGHT_INDEX:
            call do_study from _call_do_study
            return

        "!disabled![_tr('Study (Too late)')]" if CurrentLocation in ("room", "gwen_room", "rogue_room", "ntw_room", "tenny_room") and TimeIndex == NIGHT_INDEX:
            return

        # Sleep: player's room always, girl's room only at Night with girl present
        "Sleep" if CurrentLocation == "room" or (CurrentLocation in GIRL_ROOMS.values() and TimeIndex >= NIGHT_INDEX - 1 and any(_sleepover_can_happen(_sg) for _sg in ALL_GIRLS)):
            python:
                _sleep_eligible = _sleepover_eligible_girls() if TimeIndex >= NIGHT_INDEX - 1 else []
            if len(_sleep_eligible) >= 2:
                $ _day_before_sleepover = Day
                call sleepover_multi(_sleep_eligible) from _call_sleepover_multi
                if Day == _day_before_sleepover and CurrentLocation == "room":
                    call do_sleep from _call_do_sleep_after_multi
            elif len(_sleep_eligible) == 1:
                $ _day_before_sleepover = Day
                call sleepover_offer(_sleep_eligible[0]) from _call_sleepover_offer
                if Day == _day_before_sleepover and CurrentLocation == "room":
                    call do_sleep from _call_do_sleep_after_so
            else:
                if CurrentLocation in GIRL_ROOMS.values():
                    python:
                        _kick_girl = None
                        for _kg in ALL_GIRLS:
                            if GIRL_ROOMS.get(_kg.gid, "") == CurrentLocation and _kg.loc == CurrentLocation:
                                _kick_girl = _kg
                                break
                    if _kick_girl is not None:
                        $ Say_Line(_kick_girl, _tl(_("It's getting late... you should probably head back to your room.")))
                    $ Narration(_("You say goodnight and leave."))
                    $ navigate_to("room", None)
                    call Set_Scene(entry=False) from _call_Set_Scene_so_kicked
                call do_sleep from _call_do_sleep
            return

        # Pool: Swim action
        "Swim" if CurrentLocation == "pool":
            call do_swim from _call_do_swim
            return

        # Pool: breath-holding bet with a girl here (swimming.rpy); a girl with no bikini says why she can't
        "Challenge someone to hold their breath" if CurrentLocation == "pool" and girls_here:
            call breath_challenge from _call_breath_challenge
            return

        # Shower: Shower action (the campus showers and the bathroom of the apartment)
        "Shower" if CurrentLocation in SHOWER_SPOTS:
            call do_shower from _call_do_shower
            return

        # Gym: Work Out action
        "Work Out" if CurrentLocation == "gym":
            call do_workout from _call_do_workout
            return

        # Classroom: Attend Class action
        "Attend Class" if CurrentLocation == "classroom":
            call do_attend_class from _call_do_attend_class
            return

        # Mall: Pharmacy shop
        "Pharmacy" if CurrentLocation == "mall":
            call pharmacy_shop from _call_pharmacy_shop
            return

        # Mall: Bikini Store
        "Bikini Store" if CurrentLocation == "mall":
            call bikini_store from _call_bikini_store
            return

        # Mall: Geek Store
        "Geek Store" if CurrentLocation == "mall":
            call electronics_store from _call_electronics_store
            return

        # Mall: Walk around
        "Walk Around" if CurrentLocation == "mall":
            call mall_walk_around from _call_mall_walk_around
            return

        # -------------------------------------------------------
        # UNIVERSAL: WAIT + LEAVE
        # -------------------------------------------------------
        "Wait" if TimeIndex != NIGHT_INDEX:
            call do_wait from _call_do_wait
            return

        "!disabled![_tr(\"Wait (It's night)\")]" if TimeIndex == NIGHT_INDEX:
            return

        "Leave (Campus)" if CurrentLocation != "campus" and CurrentLocation not in OFF_CAMPUS_TRIPS:
            $ _nav_origin = CurrentLocation
            $ store._player_is_navigating = True
            call Apply_Time_Cost(TIME_COSTS["navigate"]) from _call_Apply_Time_Cost_17
            if CurrentLocation != _nav_origin:
                call Set_Scene(entry=True) from _call_Set_Scene_redir_campus
                return
            jump Campus_Entry

        # Mall / apartment: the Downtown crossroads (the other place downtown), then Back to Campus, always last (the
        # cost of the trip, OFF_CAMPUS_TRIPS). The apartment is left through its living room, where the front door is:
        # its bedroom and bathroom have neither (HOME_INNER_ROOMS, author, 2026-10-09)
        "Leave (Downtown)" if CurrentLocation in OFF_CAMPUS_TRIPS and CurrentLocation not in HOME_INNER_ROOMS:
            jump Downtown_Crossroads

        "Back to Campus" if CurrentLocation in OFF_CAMPUS_TRIPS and CurrentLocation not in HOME_INNER_ROOMS:
            # entered without the choice (a screen Call that resumed in the menu's last block, see the Jurassic Dog
            # van): not off campus, nothing to travel; the loop shows the menu again
            if CurrentLocation not in OFF_CAMPUS_TRIPS or CurrentLocation in HOME_INNER_ROOMS:
                $ print("[NAV] Back to Campus reached at %s (no way out from here): ignored" % CurrentLocation)
                return
            $ _nav_origin = CurrentLocation
            $ store._player_is_navigating = True
            call Apply_Time_Cost(TIME_COSTS[OFF_CAMPUS_TRIPS[CurrentLocation]]) from _call_Apply_Time_Cost_mall_back
            if CurrentLocation != _nav_origin:
                call Set_Scene(entry=True) from _call_Set_Scene_redir_mall_back
                return
            jump Campus_Entry

    return

# ── Near/Far: Call someone over (1-for-1 swap) ────────────
label _show_call_menu:
    # Step 1: who to call from far?
    python:
        _far = roster_get_far()
        renpy.say(None, _tl(_("Who do you want to call over?")), interact=False)
        _call_choices = []
        for _fe in _far:
            _fname = getattr(_fe, "Name", getattr(_fe, "name", "???"))
            _fcolor = getattr(_fe, "color", "#ffffff")
            _call_choices.append(("{color=%s}%s{/color}" % (_fcolor, _fname), _fe))
        _call_choices.append((_tl(_("Never mind")), "nevermind"))
        _call_result = renpy.display_menu(_call_choices)

    if _call_result is None or _call_result == "nevermind":
        return

    # If near has room, just add directly
    python:
        _near = roster_get_near()
        _need_swap = len(_near) >= MAX_NEAR

    if not _need_swap:
        python:
            roster_call_near(_call_result)
            show_roster_sprites()
        $ _call_name = getattr(_call_result, "Name", getattr(_call_result, "name", "???"))
        $ Narration(_tl(_("%s walks over.")) % _call_name)
        return

    # Step 2: near is full -- who should leave?
    python:
        renpy.say(None, _tl(_("Who should leave?")), interact=False)
        _swap_choices = []
        for _ne in _near:
            _nname = getattr(_ne, "Name", getattr(_ne, "name", "???"))
            _ncolor = getattr(_ne, "color", "#ffffff")
            _swap_choices.append(("{color=%s}%s{/color}" % (_ncolor, _nname), _ne))
        _swap_choices.append((_tl(_("Never mind")), "nevermind"))
        _swap_result = renpy.display_menu(_swap_choices)

    if _swap_result is None or _swap_result == "nevermind":
        return

    # Do the swap
    python:
        # Hide outgoing sprite
        if isinstance(_swap_result, NPCPartner):
            _swap_result.hide_sprite()
        else:
            hide_girl_sprite(_swap_result)
        # Swap in roster
        roster_swap(_call_result, _swap_result)
        # Show incoming at the slot the outgoing had
        show_roster_sprites()

    $ _call_name = getattr(_call_result, "Name", getattr(_call_result, "name", "???"))
    $ Narration(_tl(_("%s walks over.")) % _call_name)

    return

# --------------------------------------------
# Update scene: background + girls on screen
# --------------------------------------------
label Set_Scene(entry=False, show_chars=True, quiet=False):

    # Optional fade-in with a black screen
    if not quiet:
        show blackscreen

    # --------- Background based on current location + time ---------
    $ _bg_tag = get_bg_for_location()
    $ renpy.scene()
    $ renpy.show(_bg_tag)

    # Jurassic Dog van on master layer (above BG, below characters)
    python:
        _jd_wd = (Day - 1) % 7
        if CurrentLocation == "campus" and _jd_wd in (1, 3, 5) and TimeIndex in (0, 1):
            renpy.show("jurassic_dog_van")

    # Reset focused girl
    $ CurrentGirl = None

    # Followers override: girls in Party always stay with the player
    python:
        for g in Party:
            if not girl_is_away(g):
                g.loc = CurrentLocation

        # Which girls are in the same place as the player?
        girls_here = [_g for _g in ALL_GIRLS if _g.loc == CurrentLocation]

        for _g in girls_here:
            _enforce_location_outfit(_g)

    # --------- Show girls ---------
    if show_chars:

        $ CurrentGirl = None

        python:
            resolve_npc_for_location(CurrentLocation)
            _npc = store._npc_on_scene

            _roster = build_location_roster(girls_here, _npc)
            show_roster_sprites(_roster)

            # Set CurrentGirl to first Girl in near list
            for _e in _roster["near"]:
                if isinstance(_e, Girl):
                    store.CurrentGirl = _e
                    break

            _apply_jealousy_expressions()

        # Angry girls: show angry face and leave when player arrives
        if entry:
            python:
                _angry_leave = [_g for _g in girls_here if hasattr(_g, "has_temp_status") and _g.has_temp_status("angry") and _g not in Party]
                for _ag in _angry_leave:
                    _ag_lines = [
                        _("..."),
                        _("I have nothing to say to you."),
                        _("Don't even look at me."),
                    ]
                    Say_Line(_ag, _tl(renpy.random.choice(_ag_lines)))
                    renpy.pause(0.5)
                    roster_girl_leaves(_ag)
                    _narr = get_angry_narration(_ag)
                    if _narr:
                        renpy.say(None, _narr)
                girls_here = [_g for _g in girls_here if _g not in _angry_leave]
                if _angry_leave:
                    _near = roster_get_near()
                    _found_cg = False
                    for _e in _near:
                        if isinstance(_e, Girl):
                            store.CurrentGirl = _e
                            _found_cg = True
                            break
                    if not _found_cg:
                        store.CurrentGirl = None
                    show_roster_sprites()

            # Sad girls: avoid player and leave quietly
            python:
                _sad_leave = [_g for _g in girls_here if hasattr(_g, "has_temp_status") and _g.has_temp_status("sad") and _g not in Party]
                for _sg in _sad_leave:
                    _sg_lines = [
                        _("Sorry... I don't want to talk right now. Can we talk tomorrow?"),
                        _("Not now, please. I just... need to be alone for a bit."),
                        _("I'm fine, I just... I need some space. Tomorrow, okay?"),
                        _("Please don't. I can't look at you right now."),
                        _("I need to think. Just... give me until tomorrow."),
                    ]
                    Say_Line(_sg, _tl(renpy.random.choice(_sg_lines)))
                    renpy.pause(0.5)
                    roster_girl_leaves(_sg)
                    _narr = get_sad_narration(_sg) if callable(get_sad_narration) else None
                    if _narr:
                        renpy.say(None, _narr)
                girls_here = [_g for _g in girls_here if _g not in _sad_leave]
                if _sad_leave:
                    _near = roster_get_near()
                    _found_cg = False
                    for _e in _near:
                        if isinstance(_e, Girl):
                            store.CurrentGirl = _e
                            _found_cg = True
                            break
                    if not _found_cg:
                        store.CurrentGirl = None
                    show_roster_sprites()

    else:
        python:
            # Hide all sprites if we are not showing characters in this scene
            for _g in ALL_GIRLS:
                hide_girl_sprite(_g)

    # --------- End of scene setup ---------
    if not quiet:
        hide blackscreen

    # --------- Music for this location / time ---------
    $ _scene_track = get_scene_music(CurrentLocation, TimeIndex)
    if renpy.music.get_playing() != _scene_track:
        play music _scene_track fadein 1.0

    return

# ============================================
# TIME CHANGE DURING CHAT — centralized handler
# Called by talk_main when TimeIndex advances mid-conversation.
# Girl either leaves (with invite), or stays and mentions it.
# ============================================
label _on_time_change_chat(girl):
    # If Apply_Time_Cost called Wait, girls were already processed.
    # But raw advance_round calls (massage, kiss, touch) skip Apply_Time_Cost,
    # so update_all_girls_locations_for_time moved the girl silently.
    # Process her now so she either stays or leaves with proper dialogue.
    if not getattr(store, '_atc_wait_done', False):
        $ LastPresentGirls = [girl]
        call process_girls_after_time_change from _call_pgatch_otcc
    $ store._atc_wait_done = False
    return

# ENTRY + LOOP LABELS FOR EACH LOCATION
# ============================================

# -------- CAMPUS --------
label Campus_Entry:

    $ navigate_to("campus", None)
    call guess_who_check from _call_guess_who_check
    call Set_Scene(entry=True) from _call_Set_Scene_8
    call cjohnson_check from _call_cjohnson_check

    jump Campus_Loop

label Campus_Loop:

    call location_menu from _call_location_menu_1
    jump Campus_Loop

# -------- PLAYER ROOM --------
label Player_Room_Entry:

    $ navigate_to("room", None)
    call Set_Scene(entry=True) from _call_Set_Scene_9

    jump Player_Room_Loop

label Player_Room_Loop:

    call location_menu from _call_location_menu_2
    jump Player_Room_Loop

# -------- POOL --------
label Pool_Entry:

    $ navigate_to("pool", None)

    # Night swim random event check (before normal scene setup)
    call night_swim_check from _call_night_swim_check

    call Set_Scene(entry=True) from _call_Set_Scene_10

    jump Pool_Loop

label Pool_Loop:

    call location_menu from _call_location_menu_3
    jump Pool_Loop

# -------- GYM --------
label Gym_Entry:

    $ navigate_to("gym", None)
    call Set_Scene(entry=True) from _call_Set_Scene_11

    jump Gym_Loop

label Gym_Loop:

    call location_menu from _call_location_menu_4
    jump Gym_Loop

# -------- MALL --------
label Mall_Entry:

    $ navigate_to("mall", None)
    call Set_Scene(entry=True) from _call_Set_Scene_mall

    jump Mall_Loop

label Mall_Loop:

    call location_menu from _call_location_menu_mall
    jump Mall_Loop

# ============================================================
# DOWNTOWN: the crossroads off campus (the mall, the father's apartment, the bus back to campus). Not a place he
# stays: its picture and the way on. The trip is paid when he picks where to go (downtown_trip_cost); the way he
# came from ("Back to ...") costs nothing. A girl following him who doesn't live in the apartment keeps him out of it
# (apartment_company_block): the button stays, disabled.
# ============================================================
label Downtown_Crossroads:
    python:
        _dtc_from = downtown_spot(CurrentLocation)
        _dtc_to = None
        _dtc_mall_closing = (TimeIndex == NIGHT_INDEX) or (TimeIndex == NIGHT_INDEX - 1 and (100 - Round) <= downtown_trip_cost(_dtc_from, "mall"))
        _dtc_company = apartment_company_block()
        # the stepmom route off (family_route_on, shion_family.rpy): the crossroads only knows the mall
        _dtc_apartment_on = family_route_on()
        # he stands downtown now: the campus overlays (the Jurassic Dog van and its pulse) read this and stay hidden
        store._player_is_navigating = True
        print("[DOWNTOWN] crossroads from %s (mall closing %s, company %s)" % (_dtc_from, _dtc_mall_closing, [_g.gid for _g in _dtc_company]))
    scene expression ("bg downtown_night" if TimeIndex >= NIGHT_INDEX else "bg downtown")
    with dissolve
    menu:
        "Back to the Mall" if _dtc_from == "mall":
            $ _dtc_to = "mall"
        "Go to Mall" (nav="mall") if _dtc_from != "mall" and not _dtc_mall_closing:
            $ _dtc_to = "mall"
        "!disabled![_tr('Mall (Closing soon)')]" if _dtc_from != "mall" and _dtc_mall_closing and TimeIndex != NIGHT_INDEX:
            pass
        "!disabled![_tr('Mall (Closed)')]" if _dtc_from != "mall" and TimeIndex == NIGHT_INDEX:
            pass
        "Back to the Apartment" if _dtc_from == "apartment":
            $ _dtc_to = "apartment"
        "Go to Father's Apartment" (nav=list(APARTMENT_ROOMS)) if _dtc_apartment_on and _dtc_from != "apartment" and not _dtc_company:
            $ _dtc_to = "apartment"
        "!disabled![_tr(\"Father's Apartment (Not with company)\")]" if _dtc_apartment_on and _dtc_from != "apartment" and _dtc_company:
            pass
        "Back to Campus":
            $ _dtc_to = "campus"
    if _dtc_to is None or _dtc_to == _dtc_from:
        # the way he came: no trip
        $ store._player_is_navigating = False
        call Set_Scene(entry=False) from _call_Set_Scene_downtown_back
        return
    $ _nav_origin = CurrentLocation
    $ store._player_is_navigating = True
    $ print("[DOWNTOWN] %s -> %s (%d rounds)" % (_dtc_from, _dtc_to, downtown_trip_cost(_dtc_from, _dtc_to)))
    call Apply_Time_Cost(downtown_trip_cost(_dtc_from, _dtc_to)) from _call_Apply_Time_Cost_downtown
    if CurrentLocation != _nav_origin:
        call Set_Scene(entry=True) from _call_Set_Scene_redir_downtown
        return
    jump expression DOWNTOWN_ENTRY[_dtc_to]

# -------- FATHER'S APARTMENT (APARTMENT_ROOMS; the bathroom is Shower_Entry with _shower_spot = "apartment_shower") --------
label Apartment_Entry:

    $ navigate_to("apartment", None)
    call Set_Scene(entry=True) from _call_Set_Scene_apartment

    jump Apartment_Loop

# The trip from campus: the living room, and a line that says where his father is (shion_family.rpy)
label Apartment_Arrive:

    $ navigate_to("apartment", None)
    # his first visit: the intro of the girl of the house he has never met (family_father.rpy)
    $ _apt_intro_girl = family_intro_girl()
    if _apt_intro_girl is not None:
        call _apartment_intro(_apt_intro_girl) from _call_apartment_intro
        jump Apartment_Loop
    call Set_Scene(entry=True) from _call_Set_Scene_apartment_arrive
    $ print("[DAD] he arrives at the apartment: father %s" % dad_where())
    $ Narration(dad_arrival_line())

    jump Apartment_Loop

label Apartment_Room_Entry:

    python:
        _apt_girl = next((_g for _g in ALL_GIRLS if girl_home_loc(_g) == "apartment_room"), None)
    # she only bars the door she is BEHIND (review 2026-10-10): angry somewhere else (following him, the
    # living room) must never lock an empty bedroom and speak her line from inside it
    if _apt_girl is not None and _apt_girl.has_temp_status("angry") and getattr(_apt_girl, "loc", None) == "apartment_room":
        scene bg Door
        with dissolve
        $ Say_Line(_apt_girl, _("I don't want to see you right now. Get out."))
        $ _angry_narr = get_angry_narration(_apt_girl)
        if _angry_narr:
            "[_angry_narr]"
        jump Apartment_Entry

    $ navigate_to("apartment_room", None)
    call Set_Scene(entry=True) from _call_Set_Scene_apartment_room

    jump Apartment_Loop

label Apartment_Loop:

    call location_menu from _call_location_menu_apartment
    jump Apartment_Loop

# -------- MALL: WALK AROUND --------

init python:

    _MALL_WALK_SOLO = [
        _("You take a look at the new phones. They're exactly the same as last year, but they moved the camera."),
        _("You try to buy an ice cream. The machine is broken. You keep the diet."),
        _("You smell the popcorn and see teenagers in cosplay for a psychological horror movie with pleasant character design."),
        _("You see middle-aged ladies heading to a movie dressed very fancy. Interesting."),
        _("You think about buying a shirt. The price makes you give up. It's probably cheaper online."),
        _("Nice to just walk around for a bit."),
        _("The mall is pretty busy today."),
    ]

    _MALL_WALK_LINES = {
        "gwen": [
            (_("Oh look! That makeup store finally has a black lipstick that doesn't smudge. Miracles happen."), "surprised"),
            (_("Those combat boots in the window are SO cute. I need them."), "happy"),
            (_("This ice cream is amazing. We should do this more often."), "closed_happy"),
            (_("Did you see that dress? Way too expensive, but a girl can dream."), "surprised"),
            (_("I love this flavor. Want a taste?"), "sly"),
            (_("There's an art store on the second floor. I could lose a whole paycheck in the ink aisle."), "happy"),
            (_("That music store still has a vinyl section. Dark, moody and overpriced. My three favorite things."), "smirk"),
        ],
        "rogue": [
            (_("They finally opened a new gym nearby. About time."), "smirk"),
            (_("This ice cream's alright. Ain't my aunt's peach cobbler, but it'll do."), "bemused"),
            (_("There's a new protein shake bar over there. We should check it out later."), "happy"),
            (_("Not bad for a walk. At least the ice cream is good."), "bemused"),
            (_("Look at that sports store. They've got new boxing gloves."), "surprised"),
            (_("That western store's got real leather saddles in the window. Lord, I miss ridin'."), "happy"),
            (_("They sell sweet tea here, sugar. That ain't sweet tea. That's sad brown water."), "annoyed"),
        ],
        "ntw": [
            (_("They announced another movie about that guy who breaks the fourth wall and never shuts up. Great. More of him."), "annoyed"),
            (_("There's a new comic book store on the second floor. I might go. Don't make it a whole thing."), "smirk"),
            (_("This place has a flavor called 'Radioactive Lime.' It tastes like a lab accident. I respect it."), "smirk"),
            (_("They sell figurines of that loudmouth merc in the red suit now. Even the plastic one looks like it won't shut up."), "annoyed"),
            (_("There's a horror movie marathon this weekend. Finally, something worth leaving my room for."), "smirk"),
            (_("That electronics store sells laptops that would fry the second I touched them. Pass."), "annoyed"),
        ],
        "generic": [
            (_("This ice cream is really good."), "closed_happy"),
            (_("This place has so many stores. Hard to pick where to go."), "confused"),
            (_("I like walking around here. It's relaxing."), "happy"),
        ],
    }

    _MALL_WALK_DUO = [
        _("%(ga)s and %(gb)s won't stop talking about some kind of schubergelson that needs a tchunflay in front of the makeup store. You feel lost."),
        _("%(ga)s and %(gb)s argue about a new album at the music store. You get lost looking at vinyls older than your dad."),
        _("%(ga)s points at something in a window. %(gb)s disagrees. They go back and forth while you just stand there holding bags."),
        _("%(ga)s and %(gb)s take forever choosing between two nearly identical scarves. You question your life choices."),
    ]

    _MALL_WALK_DUO_FRIENDS = [
        _("%(ga)s and %(gb)s walk nonstop and try on 900 types of clothes together. You feel exhausted."),
        _("%(ga)s and %(gb)s keep finishing each other's sentences while browsing. You're basically invisible right now."),
        _("%(ga)s spots a buy-one-get-one deal and grabs %(gb)s by the arm. They vanish into the store. You wait outside."),
    ]

    _MALL_WALK_DUO_RIVALS = [
        _("%(ga)s and %(gb)s drag you between stores trying to get your attention and badmouthing each other's clothes. Stressful."),
        _("%(ga)s picks a jacket. %(gb)s says it looks awful. %(ga)s fires back. You pretend to check your phone."),
        _("Every store becomes a battlefield. %(ga)s goes left, %(gb)s goes right, and both want you to follow. Exhausting."),
    ]

label mall_walk_around:
    python:
        _mw_girls = [g for g in Party if g.loc == "mall"]
        _mw_count = len(_mw_girls)

    if _mw_count == 0:
        python:
            _mw_solo = renpy.random.choice(_MALL_WALK_SOLO)
        $ Narration(_tl(_mw_solo))

    elif _mw_count == 1:
        python:
            _mw_girl = _mw_girls[0]
            _mw_pool = _MALL_WALK_LINES.get(_mw_girl.gid, _MALL_WALK_LINES["generic"])
            _mw_line, _mw_expr = renpy.random.choice(_mw_pool)
        $ Narration(_("You walk around the mall together."))
        $ set_scene_expression(_mw_girl, _mw_expr, pose="standing")
        $ Say_Line(_mw_girl, _tl(_mw_line))
        $ set_scene_expression(_mw_girl, "normal", pose="standing")
        python:
            Change_Status(_mw_girl, "Love", 3)
            debug_log("[MALL_WALK] %s said a line (expr=%s), Love +3" % (_mw_girl.gid, _mw_expr))

    else:
        python:
            _mw_a = _mw_girls[0]
            _mw_b = _mw_girls[1]
            _mw_like = (_mw_a.get_like_for(_mw_b.gid) + _mw_b.get_like_for(_mw_a.gid)) / 2

            # ── Dressing room event check ──
            _mw_dr_event = None
            debug_log("[MALL_DR] --- Dressing room check: %s + %s, like=%d ---" % (_mw_a.gid, _mw_b.gid, _mw_like))
            if _mw_like > 350:
                _mw_gf = next((g for g in [_mw_a, _mw_b] if g.is_dating_player()), None)
                debug_log("[MALL_DR] like OK (>350). GF=%s" % (getattr(_mw_gf, 'gid', 'none')))
                _mw_bj_cands = [g for g in [_mw_a, _mw_b] if g.Sex_acts.get("bj", 0) > 0 and g.Obed >= 400]
                for _dbg_g in [_mw_a, _mw_b]:
                    _dbg_bj = _dbg_g.Sex_acts.get("bj", 0)
                    _dbg_obed = _dbg_g.Obed
                    _dbg_is_gf = (_dbg_g == _mw_gf)
                    _dbg_pass = _dbg_bj > 0 and _dbg_obed >= 400
                    debug_log("[MALL_DR]   %s: bj_count=%d %s, Obed=%d %s, is_gf=%s → %s" % (
                        _dbg_g.gid, _dbg_bj, "(OK)" if _dbg_bj > 0 else "(NEED >0)",
                        _dbg_obed, "(OK)" if _dbg_obed >= 400 else "(NEED >=400)",
                        _dbg_is_gf, "CANDIDATE" if (_dbg_pass and not _dbg_is_gf) else "EXCLUDED (gf)" if (_dbg_pass and _dbg_is_gf) else "FAIL"))
                if _mw_gf and _mw_gf in _mw_bj_cands:
                    _mw_bj_cands.remove(_mw_gf)
                _mw_sneaker = None
                if _mw_bj_cands:
                    _mw_sneaker = next((g for g in _mw_bj_cands if g.has_trait("cheater")), None) or next((g for g in _mw_bj_cands if g.has_trait("public_fetish")), None) or _mw_bj_cands[0]
                    debug_log("[MALL_DR] sneaker=%s (cheater=%s, public_fetish=%s)" % (_mw_sneaker.gid, _mw_sneaker.has_trait("cheater"), _mw_sneaker.has_trait("public_fetish")))
                else:
                    debug_log("[MALL_DR] NO sneaker candidates — full event blocked")

                if _mw_sneaker:
                    _mw_cover = _mw_a if _mw_sneaker == _mw_b else _mw_b
                    _mw_dr_chance = 15
                    if _mw_sneaker.has_trait("public_fetish"):
                        _mw_dr_chance += 10
                    if _mw_gf and _mw_gf == _mw_cover and _mw_sneaker.has_trait("cheater"):
                        _mw_dr_chance += 15
                    _mw_dr_roll = renpy.random.randint(1, 100)
                    debug_log("[MALL_DR] FULL chance=%d%%, roll=%d → %s" % (_mw_dr_chance, _mw_dr_roll, "TRIGGERED" if _mw_dr_roll <= _mw_dr_chance else "miss"))
                    if _mw_dr_roll <= _mw_dr_chance:
                        _mw_dr_event = "full"

                if not _mw_dr_event and _mw_like >= 500:
                    _mw_dr_lite_roll = renpy.random.randint(1, 100)
                    debug_log("[MALL_DR] LITE chance=20%%, roll=%d → %s" % (_mw_dr_lite_roll, "TRIGGERED" if _mw_dr_lite_roll <= 20 else "miss"))
                    if _mw_dr_lite_roll <= 20:
                        _mw_dr_event = "lite"
                        _mw_cover = _mw_a
                        _mw_sneaker = _mw_b
                elif not _mw_dr_event and _mw_like < 500:
                    debug_log("[MALL_DR] LITE blocked — like=%d (NEED >=500)" % _mw_like)
            else:
                debug_log("[MALL_DR] like=%d TOO LOW (NEED >350) — dressing room blocked" % _mw_like)

            if not _mw_dr_event:
                debug_log("[MALL_DR] result: normal duo walk")

        if _mw_dr_event == "full":
            call mall_dressing_bj(_mw_cover, _mw_sneaker) from _call_mall_dressing_bj
        elif _mw_dr_event == "lite":
            call mall_dressing_lite(_mw_cover, _mw_sneaker) from _call_mall_dressing_lite
        else:
            python:
                if _mw_like >= 600 and renpy.random.random() < 0.5:
                    _mw_duo_pool = _MALL_WALK_DUO_FRIENDS
                    _mw_duo_expr = "laugh"
                elif _mw_like <= 250 and renpy.random.random() < 0.5:
                    _mw_duo_pool = _MALL_WALK_DUO_RIVALS
                    _mw_duo_expr = "angry"
                else:
                    _mw_duo_pool = _MALL_WALK_DUO
                    _mw_duo_expr = "happy"
                _mw_duo_raw = renpy.random.choice(_mw_duo_pool)
                _mw_duo_text = _tl(_mw_duo_raw) % {"ga": _mw_a.Name, "gb": _mw_b.Name}
            $ set_scene_expression(_mw_a, _mw_duo_expr, pose="standing")
            $ set_scene_expression(_mw_b, _mw_duo_expr, pose="standing")
            $ Narration(_mw_duo_text)
            $ set_scene_expression(_mw_a, "normal", pose="standing")
            $ set_scene_expression(_mw_b, "normal", pose="standing")
            python:
                Change_Status(_mw_a, "Love", 2)
                Change_Status(_mw_b, "Love", 2)
                _mw_a.add_like_for(_mw_b.gid, 3)
                _mw_b.add_like_for(_mw_a.gid, 3)
                debug_log("[MALL_WALK] duo %s+%s, like=%d, expr=%s, Love +2 each, friendship +3 mutual" % (_mw_a.gid, _mw_b.gid, _mw_like, _mw_duo_expr))

    call Apply_Time_Cost(15) from _call_Apply_Time_Cost_mall_walk

    return

# -------- MALL: DRESSING ROOM EVENT (FULL BJ) --------

label mall_dressing_bj(cover_girl, sneaker_girl):

    # Girl A suggests going to the bikini store
    $ set_scene_expression(cover_girl, "surprised", pose="standing")
    $ Say_Line(cover_girl, _("Oh wow, look at that bikini! It's gorgeous."))
    $ set_scene_expression(cover_girl, "happy", pose="standing")
    $ Say_Line(cover_girl, _tl(_("%s, come with me, I want to try it on!")) % sneaker_girl.Name)
    $ set_scene_expression(sneaker_girl, "happy", pose="standing")
    $ Say_Line(sneaker_girl, _("Sure, let's go!"))

    # Transition to dressing room outside
    scene bg dressing_room_outside with dissolve
    $ cover_girl.SpriteLoc = StageLeft
    $ sneaker_girl.SpriteLoc = StageRight
    $ set_girl_sprite(cover_girl.gid, pose="standing", at_list=[slot_left])
    $ set_girl_sprite(sneaker_girl.gid, pose="standing", at_list=[slot_right])

    # Girl A goes to change
    $ set_scene_expression(cover_girl, "happy", pose="standing")
    $ Say_Line(cover_girl, _("I'll go try it on, wait here!"))
    $ renpy.show(cover_girl.gid, at_list=[witness_exit_left])
    pause 0.6
    $ renpy.hide(cover_girl.gid)
    pause 0.3

    # Girl B gets naughty
    $ set_scene_expression(sneaker_girl, "sly", pose="standing", blush=1)
    pause 0.4
    $ Say_Line(sneaker_girl, _tl(_("Hey %s, I'm gonna try something on too. See you in a bit!")) % cover_girl.Name)
    pause 0.2

    # Girl B pulls player into the cabin
    $ set_scene_expression(sneaker_girl, "smug", pose="standing", blush=1)
    $ Narration(_("She grabs your hand and pulls you into one of the changing rooms."))
    $ renpy.show(sneaker_girl.gid, at_list=[witness_exit_right])
    pause 0.5
    $ renpy.hide(sneaker_girl.gid)

    # Inside dressing room
    scene bg dressing_room with dissolve
    $ sneaker_girl.SpriteLoc = StageCenter
    $ set_girl_sprite(sneaker_girl.gid, pose="standing", at_list=[slot_center])
    $ set_scene_expression(sneaker_girl, "smug", pose="standing", blush=1)

    $ Say_Line(sneaker_girl, _("We don't have much time... but I can't help myself."))

    # Full interactive BJ scene (restricted: no NPC witness detection in mall)
    $ store._scene_restricted = True
    call start_scene(sneaker_girl, "bj") from _call_mall_dr_bj_scene
    $ store._scene_restricted = False

    # After scene ends — Girl A calls out
    scene bg dressing_room with dissolve
    $ sneaker_girl.SpriteLoc = StageCenter
    $ set_girl_sprite(sneaker_girl.gid, pose="standing", at_list=[slot_center])
    $ set_scene_expression(sneaker_girl, "smug", pose="standing", blush=1)

    $ Say_Line(cover_girl, _tl(_("Hey %s! I'm done. Where are you?")) % sneaker_girl.Name)
    pause 0.3

    $ Say_Line(sneaker_girl, _("Oops, time to go. I could feel how much you liked knowing she was right next to us, you perv."))
    pause 0.3

    # Girl B slides out
    $ renpy.show(sneaker_girl.gid, at_list=[witness_exit_right])
    pause 0.5
    $ renpy.hide(sneaker_girl.gid)

    # Back to bikini shop
    scene bg bikini_shop with dissolve
    $ cover_girl.SpriteLoc = StageLeft
    $ sneaker_girl.SpriteLoc = StageRight
    $ set_girl_sprite(cover_girl.gid, pose="standing", at_list=[slot_left])
    $ set_girl_sprite(sneaker_girl.gid, pose="standing", at_list=[slot_right])

    # Final dialogue
    $ set_scene_expression(cover_girl, "sad", pose="standing")
    $ Say_Line(cover_girl, _("Too bad... it looked so pretty, but they didn't have my size."))
    $ set_scene_expression(sneaker_girl, "sly", pose="standing")
    $ Say_Line(sneaker_girl, _("Yeah... they should carry bigger things. They fit so much better."))
    $ set_scene_expression(cover_girl, "normal", pose="standing")
    $ set_scene_expression(sneaker_girl, "normal", pose="standing")

    # Rewards (start_scene already handles BJ stats, add friendship/inbt)
    python:
        Change_Status(cover_girl, "Inbt", 5)
        sneaker_girl.add_like_for(cover_girl.gid, 5)
        cover_girl.add_like_for(sneaker_girl.gid, 5)
        unlock_achievement("perfect_fit")
        debug_log("[MALL_DRESSING] BJ complete: sneaker=%s, cover=%s" % (sneaker_girl.gid, cover_girl.gid))

    # Restore mall scene with proper slot assignment (girls + NPC)
    call Set_Scene(quiet=True) from _call_Set_Scene_mall_dr_bj

    return

# -------- MALL: DRESSING ROOM EVENT (LITE) --------

label mall_dressing_lite(cover_girl, sneaker_girl):

    # Girls suggest checking the bikini store together
    $ set_scene_expression(cover_girl, "surprised", pose="standing")
    $ Say_Line(cover_girl, _("Oh, that bikini store looks nice! Let's check it out."))
    $ set_scene_expression(sneaker_girl, "happy", pose="standing")
    $ Say_Line(sneaker_girl, _("Sure! Let's try some stuff on."))

    # They tell player to wait
    $ set_scene_expression(cover_girl, "happy", pose="standing")
    $ Say_Line(cover_girl, _("Wait here, okay? We'll be right back."))
    $ set_scene_expression(sneaker_girl, "sly", pose="standing")
    $ Say_Line(sneaker_girl, _("No peeking!"))

    # Both slide off
    $ renpy.show(cover_girl.gid, at_list=[witness_exit_left])
    pause 0.4
    $ renpy.show(sneaker_girl.gid, at_list=[witness_exit_right])
    pause 0.5
    $ renpy.hide(cover_girl.gid)
    $ renpy.hide(sneaker_girl.gid)

    # Wait
    $ Narration(_("You wait a few minutes..."))
    pause 0.8

    # They come back — use Set_Scene for proper slot assignment (avoids NPC overlap)
    call Set_Scene(quiet=True) from _call_Set_Scene_mall_dr_lite

    # Final dialogue
    $ set_scene_expression(cover_girl, "sad", pose="standing")
    $ Say_Line(cover_girl, _("Too bad they didn't have my size. It looked so pretty..."))
    $ set_scene_expression(sneaker_girl, "normal", pose="standing")
    $ Say_Line(sneaker_girl, _("Yeah... but it's okay, that's how it goes."))
    $ set_scene_expression(cover_girl, "normal", pose="standing")
    $ set_scene_expression(sneaker_girl, "normal", pose="standing")

    # Rewards (lighter)
    python:
        Change_Status(cover_girl, "Inbt", 3)
        Change_Status(sneaker_girl, "Inbt", 3)
        cover_girl.add_like_for(sneaker_girl.gid, 5)
        sneaker_girl.add_like_for(cover_girl.gid, 5)
        debug_log("[MALL_DRESSING] lite event: %s + %s, friendship +5 mutual, Inbt +3 each" % (cover_girl.gid, sneaker_girl.gid))

    return

# -------- CLASSROOM --------
label Classroom_Entry:

    $ navigate_to("classroom", None)
    call Set_Scene(entry=True) from _call_Set_Scene_12

    jump Classroom_Loop

label Classroom_Loop:

    call location_menu from _call_location_menu_5
    jump Classroom_Loop

# -------- GENERIC GIRL ROOM (ANY GIRL) --------
label Girls_Room_Entry:

    # Expects SelectedGirlGid to be set before jumping here
    python:
        girl = None
        for g in ALL_GIRLS:
            if g.gid == SelectedGirlGid:
                girl = g
                break

        if girl:
            room_loc = girl_home_loc(girl)
        else:
            room_loc = "room"


    # Away (at her parents' giving birth): nobody answers, whatever her mood
    if girl is not None and girl_is_away(girl):
        scene bg Door
        with dissolve
        play sound "audio/Knock.mp3" noloop
        $ renpy.say(None, _tl(_("You knock on [girl.Name]'s door. No answer. She is still away, with her family and the baby.")))
        $ navigate_to("campus", None)
        call Set_Scene(entry=True) from _call_Set_Scene_away_room
        return

    # Angry girl locks the player out of her room
    if girl is not None and hasattr(girl, "has_temp_status") and girl.has_temp_status("angry"):
        scene bg Door
        with dissolve
        "You go to [girl.Name]'s room. It's locked."
        $ Say_Line(girl, _("I don't want to see you right now. Get out."))
        $ _angry_narr = get_angry_narration(girl)
        if _angry_narr:
            "[_angry_narr]"
        $ navigate_to("campus", None)
        call Set_Scene(entry=True) from _call_Set_Scene_13
        return

    # Girl talking to NPC partner after being caught
    if girl is not None and getattr(girl, "_npc_catch_pending", False):
        $ debug_log("[NAV_BLOCK] %s room blocked: catch_pending=True Day=%d TI=%d unavailable=%s" % (girl.gid, Day, TimeIndex, girl.has_temp_status("unavailable") if hasattr(girl, "has_temp_status") else "?"))
        scene bg Door
        with dissolve
        "You hear people talking inside. Better not interfere right now."
        $ navigate_to("campus", None)
        call Set_Scene(entry=True) from _call_Set_Scene_npc_catch
        return

    # Sad girl softly turns the player away
    if girl is not None and hasattr(girl, "has_temp_status") and girl.has_temp_status("sad"):
        scene bg Door
        with dissolve
        play sound "audio/Knock.mp3" noloop
        "You knock on [girl.Name]'s door. After a moment, it opens slightly."
        python:
            _sad_door_lines = [
                _("Hey... I'm sorry, I just can't right now. Maybe tomorrow?"),
                _("Please... not today. I need to be alone for a while."),
                _("I appreciate you coming, but I really need some space right now."),
                _("I'm not mad at you, I just... I can't face you today. Come back tomorrow."),
                _("Can we talk tomorrow? I'm not feeling like myself right now."),
            ]
        $ Say_Line(girl, _tl(renpy.random.choice(_sad_door_lines)))
        "She gently closes the door."
        $ _sad_narr = get_sad_narration(girl)
        if _sad_narr:
            "[_sad_narr]"
        $ navigate_to("campus", None)
        call Set_Scene(entry=True) from _call_Set_Scene_sad_room
        return

    # Ex who hasn't had the first post-breakup confrontation.
    # If she's home she opens the door and the one-time confrontation
    # (_ex_first_confrontation) plays out right here, then the flag is set
    # so the room behaves normally afterward. If she's genuinely not home,
    # there is no answer and the confrontation waits until you catch her in
    # (talk_main also fires it when you find her at a public location).
    if girl is not None and hasattr(girl, "is_ex_of_player") and girl.is_ex_of_player() and not getattr(girl, "_ex_confrontation_done", False):
        if girl.loc == room_loc or girl in Party:
            scene bg Door
            with dissolve
            play sound "audio/Knock.mp3" noloop
            $ renpy.say(None, _tl(_("You knock on [girl.Name]'s door. After a long pause, she opens it.")))
            $ navigate_to(room_loc, girl)
            call Set_Scene(entry=True) from _call_Set_Scene_ex_confront_room
            $ girl._ex_confrontation_done = True
            call _ex_first_confrontation(girl) from _call_ex_first_confrontation_room
            $ navigate_to("campus", None)
            call Set_Scene(entry=True) from _call_Set_Scene_ex_confront_after
            return
        else:
            scene bg Door
            with dissolve
            play sound "audio/Knock.mp3" noloop
            "You knock on [girl.Name]'s door, but there is no answer."
            "She probably doesn't want to see you right now."
            $ navigate_to("campus", None)
            call Set_Scene(entry=True) from _call_Set_Scene_ex_room_block
            return

    # Girl not in her room (skip if she's following the player)
    if girl is not None and girl.loc != room_loc and girl not in Party:
        scene bg Door
        with dissolve
        $ renpy.say(None, _("She doesn't seem to be here right now."))
        $ navigate_to("campus", None)
        call Set_Scene(entry=True) from _call_Set_Scene_not_home
        return

    # Random masturbation event... base 3%, scales with lust, caps at 40%
    # Blocked in first 3 days for better flow
    python:
        _caught_chance = 0.0
        if girl is not None and girl.loc == room_loc and Day > 3:
            _npc = get_npc_partner_for(girl) if girl.has_npc_partner() else None
            _partner_here = _npc is not None and getattr(_npc, "loc", None) == room_loc
            if not _partner_here:
                _lust = getattr(girl, "Lust", 0)
                if _lust >= 80:
                    _caught_chance = 0.40
                else:
                    _caught_chance = 0.03 + (_lust / 100.0) * 0.37

    if _caught_chance > 0 and renpy.random.random() < _caught_chance:
        call caught_masturbating(girl, room_loc) from _call_caught_masturbating
        if _return == "left":
            return

    $ navigate_to(room_loc, girl)
    call Set_Scene(entry=True) from _call_Set_Scene_14

    jump Girls_Room_Loop

label Girls_Room_Loop:

    call location_menu from _call_location_menu_6
    jump Girls_Room_Loop

# --------------------------------------------
# Submenu: choose a girl's room to visit
# --------------------------------------------
label choose_girl_room:

    # Check which girls exist
    python:
        available = []
        for g in ALL_GIRLS:
            if g.gid in GIRL_ROOMS:
                available.append(g)

    if not available:
        "There is no girl's room to visit yet."
        return

    $ _tenny_room_label = _tl(_("%s's Room")) % GIRL_BY_ID["tenny"].Name if "tenny" in GIRL_BY_ID else _tl(_("Tenny's Room"))

    menu:
        "Choose a girl's room:"

        "Gwen's Room" (nav=GIRL_ROOMS["gwen"]) if any(g.gid == "gwen" for g in available):
            $ SelectedGirlGid = "gwen"
            $ _nav_origin = CurrentLocation
            $ store._player_is_navigating = True
            call Apply_Time_Cost(TIME_COSTS["navigate"]) from _call_Apply_Time_Cost_18
            if CurrentLocation != _nav_origin:
                call Set_Scene(entry=True) from _call_Set_Scene_redir_groom
                return
            jump Girls_Room_Entry

        "Rogue's Room" (nav=GIRL_ROOMS["rogue"]) if any(g.gid == "rogue" for g in available):
            $ SelectedGirlGid = "rogue"
            $ _nav_origin = CurrentLocation
            $ store._player_is_navigating = True
            call Apply_Time_Cost(TIME_COSTS["navigate"]) from _call_Apply_Time_Cost_19
            if CurrentLocation != _nav_origin:
                call Set_Scene(entry=True) from _call_Set_Scene_redir_rroom
                return
            jump Girls_Room_Entry

        "Negasonic's Room" (nav=GIRL_ROOMS["ntw"]) if any(g.gid == "ntw" for g in available):
            $ SelectedGirlGid = "ntw"
            $ _nav_origin = CurrentLocation
            $ store._player_is_navigating = True
            call Apply_Time_Cost(TIME_COSTS["navigate"]) from _call_Apply_Time_Cost_ntw
            if CurrentLocation != _nav_origin:
                call Set_Scene(entry=True) from _call_Set_Scene_redir_nroom
                return
            jump Girls_Room_Entry

        "[_tenny_room_label]" (nav=GIRL_ROOMS["tenny"]) if any(g.gid == "tenny" for g in available):
            $ SelectedGirlGid = "tenny"
            $ _nav_origin = CurrentLocation
            $ store._player_is_navigating = True
            call Apply_Time_Cost(TIME_COSTS["navigate"]) from _call_Apply_Time_Cost_tenny
            if CurrentLocation != _nav_origin:
                call Set_Scene(entry=True) from _call_Set_Scene_redir_troom
                return
            jump Girls_Room_Entry

        "Cancel":
            return

# --------------------------------------------
# Unified girl handler when time changes
# --------------------------------------------
label _shower_leave_dressup(girl):
    $ _needs_dressup = _prepare_shower_leave(girl)
    if _needs_dressup:
        with dissolve
        pause 0.3
        call DressUp_Sequence(girl) from _call_DressUp_shower_leave
    return

label Girl_TimeChange_Handler(girl):

    # She went away at this very time change (labor): no goodbye line, no invite. She is simply gone.
    if girl_is_away(girl):
        $ hide_girl_sprite(girl)
        return

    # Store-level variables so Ren'Py statements can see them
    $ was_follower = (girl in Party)
    $ Love = girl.Love
    $ dest_loc = get_scheduled_location_for(girl, Day, TimeIndex)
    $ dest_desc = _tl(LOC_NAMES.get(dest_loc, dest_loc))
    $ leaving = (dest_loc != CurrentLocation)

    # Is the player inside this girl's room?
    $ _in_her_room = (CurrentLocation == GIRL_ROOMS.get(girl.gid, ""))

    if not leaving:
        # She is not scheduled to move away from this location,
        # so we do nothing special here.
        return

    $ _leaving_shower = (CurrentLocation in SHOWER_SPOTS and getattr(girl, "shower_state", None) not in (None, "dressed"))

    # Angry / sad at him (a fight, "don't talk to me for a while" after the pregnancy talk...): she just goes, like
    # the low-Love tier. No invite to come along, no "I'd rather stay with you" (author report, 2026-09-19).
    $ _cold = girl.has_temp_status("angry") or girl.has_temp_status("sad")
    if _cold:
        $ print("[TIME_CHANGE] %s leaves for %s without an invite (angry=%s sad=%s)" % (girl.gid, dest_loc, girl.has_temp_status("angry"), girl.has_temp_status("sad")))

    # Nerd girls prioritize class — bypass Love tiers
    if "nerd" in girl.traits and dest_loc == "classroom" and not _cold:
        call _nerd_class_handler(girl) from _call_nerd_class_handler
        return

    # 0–400 (or angry / sad at him): she just leaves, but still hints where she is going
    if Love < 400 or _cold:

        if was_follower:
            $ Say_Line(girl, _tl(_("Sorry, I need to head to %s.")) % dest_desc)
            if girl in Party:
                $ Party.remove(girl)
        else:
            $ Say_Line(girl, _tl(_("I have to go to %s now.")) % dest_desc)

        if _leaving_shower:
            call _shower_leave_dressup(girl) from _call_shower_dressup_low
        $ girl.loc = dest_loc
        $ hide_girl_sprite(girl)

        # Player can't stay in her room alone
        if _in_her_room:
            "You leave [girl.Name]'s room as well."
            $ navigate_to("campus", None)
        return

    # 400–500: tells you where she is going, no invite
    elif Love < 500:

        $ line = _tl(_("I'm heading to %s. See you later.")) % dest_desc
        $ Say_Line(girl, line)

        if was_follower and girl in Party:
            $ Party.remove(girl)

        if _leaving_shower:
            call _shower_leave_dressup(girl) from _call_shower_dressup_mid
        $ girl.loc = dest_loc
        $ hide_girl_sprite(girl)

        # Player can't stay in her room alone
        if _in_her_room:
            "You leave [girl.Name]'s room as well."
            $ navigate_to("campus", None)
        return

    # 500–700: invites you to come with her
    elif Love < 700:

        $ line = _tl(_("I was thinking of going to %s. Want to come with me?")) % dest_desc
        $ Say_Line(girl, line)

        menu:
            "Sure, let's go.":
                # If she was not a follower before, she can become one now.
                if (not was_follower) and girl not in Party and len(Party) < MAX_PARTY_SIZE:
                    $ Party.append(girl)

                if _leaving_shower:
                    call _shower_leave_dressup(girl) from _call_shower_dressup_follow
                # Player moves with her to that location.
                $ navigate_to(dest_loc, girl)
                return

            "Not now.":

                $ Say_Line(girl, _("All right, I'll go on my own."))

                if was_follower and girl in Party:
                    $ Party.remove(girl)

                if _leaving_shower:
                    call _shower_leave_dressup(girl) from _call_shower_dressup_notnow
                $ girl.loc = dest_loc
                $ hide_girl_sprite(girl)

                # Player can't stay in her room alone
                if _in_her_room:
                    "You leave [girl.Name]'s room as well."
                    $ navigate_to("campus", None)
                return

    # 700+: she chooses to stay at this location (does NOT follow)
    else:
        # Don't stay at locations that close at Night — go to her room instead
        python:
            _closed_at_night = {"gym", "pool", "classroom", "hall", "mall"}
            _must_leave = (TimeIndex == NIGHT_INDEX and CurrentLocation in _closed_at_night)
            _player_leaving = getattr(store, "_player_is_navigating", False)

        if _must_leave:
            $ Say_Line(girl, _("This place is closing... let's head back."))
            if was_follower and girl in Party:
                $ Party.remove(girl)
            if _leaving_shower:
                call _shower_leave_dressup(girl) from _call_shower_dressup_close
            $ girl.loc = dest_loc
            $ hide_girl_sprite(girl)

            if _in_her_room:
                "You leave [girl.Name]'s room as well."
                $ navigate_to("campus", None)

        elif _player_leaving and len(Party) < MAX_PARTY_SIZE:
            # Player is navigating away — offer to follow instead of "I'll stay"
            $ Say_Line(girl, _("You're leaving already? Want me to come with you?"))

            menu:
                "Sure, come along.":
                    $ Say_Line(girl, _("Yay! Let's go."))
                    if _leaving_shower:
                        call _shower_leave_dressup(girl) from _call_shower_dressup_come
                    if girl not in Party and len(Party) < MAX_PARTY_SIZE:
                        $ Party.append(girl)

                "No, you stay. I'll be back.":
                    $ Say_Line(girl, _("Okay... don't take too long."))
                    if was_follower and girl in Party:
                        $ Party.remove(girl)
                    if _leaving_shower:
                        call _shower_leave_dressup(girl) from _call_shower_dressup_stay
                    $ girl.loc = dest_loc

        else:
            if was_follower:
                $ Say_Line(girl, _("Time is moving, but I would rather stay with you."))
            else:
                $ Say_Line(girl, _("I think I will stay here a bit longer."))
            $ girl.loc = CurrentLocation
        return

# --------------------------------------------
# Nerd class attendance override
# --------------------------------------------
label _nerd_class_handler(girl):

    python:
        _nerd_invite_pool = [
            _("Hey, class is about to start. Want to come with me?"),
            _("We should head to class. Come on, it'll be fun... well, educational at least."),
            _("I don't want to be late. Come to class with me?"),
        ]
    $ set_scene_expression(girl, "happy")
    $ Say_Line(girl, renpy.random.choice(_nerd_invite_pool))
    # the class invite only exists for a nerd: the chip follows her invite (audit 2026-10-04)
    $ girl.discover("discovered_trait_nerd") if girl.has_trait("nerd") else None

    menu:
        "Sure, let's go.":
            if (not was_follower) and girl not in Party and len(Party) < MAX_PARTY_SIZE:
                $ Party.append(girl)
            if _leaving_shower:
                call _shower_leave_dressup(girl) from _call_shower_nerd_go
            $ navigate_to("classroom", girl)
            return

        "I'll pass.":
            python:
                _nerd_alone_pool = [
                    _("Suit yourself. I'm not missing class though."),
                    _("Your loss. I'll save you a seat in case you change your mind."),
                    _("Fine, but don't blame me if you miss something important."),
                ]
            $ set_scene_expression(girl, "smug")
            $ Say_Line(girl, renpy.random.choice(_nerd_alone_pool))
            if was_follower and girl in Party:
                $ Party.remove(girl)
            if _leaving_shower:
                call _shower_leave_dressup(girl) from _call_shower_nerd_alone
            $ girl.loc = "classroom"
            $ hide_girl_sprite(girl)
            if _in_her_room:
                "You leave [girl.Name]'s room as well."
                $ navigate_to("campus", None)
            return

        "Stay with me instead.":
            python:
                _nerd_skip_count = getattr(girl, "_nerd_classes_skipped", 0)
                _nerd_exam_close = days_until_exam(Day) <= 7

            if girl.Obed >= 500:
                if _nerd_exam_close:
                    python:
                        _nerd_skip_pool = [
                            _("The exam is THIS WEEK! We need to study! I'm serious! ...Fine, but we're studying ALL night."),
                            _("Are you crazy?! The exam is in a few days! ...Ugh, okay, but only because you asked nicely."),
                            _("You're going to be the reason I fail... The exam is so close! ...Okay, but we study together later. No excuses."),
                        ]
                elif _nerd_skip_count == 0:
                    python:
                        _nerd_skip_pool = [
                            _("Fine... but we're studying together later, deal?"),
                            _("Okay, but only this once. And you're helping me catch up on notes later."),
                            _("You're a bad influence, you know that? ...Fine, I'll stay."),
                        ]
                elif _nerd_skip_count <= 3:
                    python:
                        _nerd_skip_pool = [
                            _("Again? You already asked me to skip... you're such a troublemaker."),
                            _("You know, I'm starting to notice a pattern here... Fine, but this is the last time!"),
                            _("Okay, okay. But this is the LAST time! We need to study!"),
                        ]
                else:
                    python:
                        _nerd_skip_pool = [
                            _("At this point, I don't even know why I bother going to class..."),
                            _("You've turned me into a delinquent, you know that? ...Let's go."),
                            _("My attendance is already ruined... what's one more class?"),
                        ]
                $ set_scene_expression(girl, "shy")
                $ Say_Line(girl, renpy.random.choice(_nerd_skip_pool))
                $ girl.loc = CurrentLocation
                $ girl._nerd_classes_skipped = _nerd_skip_count + 1
                # the skipped class costs her the study she would have gained (makes her F reachable)
                $ girl.study_level = max(0, girl.study_level - 2)
                $ print("[NERD_SKIP] %s skipped class #%d, study_level -> %d" % (girl.gid, girl._nerd_classes_skipped, girl.study_level))
            else:
                if _nerd_exam_close:
                    python:
                        _nerd_refuse_pool = [
                            _("Are you kidding?! The exam is THIS WEEK! I'm going to class and so should you!"),
                            _("No way! Not with the exam so close. I'll see you after, but I NEED to study!"),
                            _("Absolutely not. The exam is in a few days. I'm going, end of discussion."),
                        ]
                else:
                    python:
                        _nerd_refuse_pool = [
                            _("Sorry, I really can't skip. Maybe we can hang out after class?"),
                            _("I appreciate the offer, but class is important. We can study together later if you want."),
                            _("No, I really should go. Come find me after, okay?"),
                        ]
                $ set_scene_expression(girl, "worried")
                $ Say_Line(girl, renpy.random.choice(_nerd_refuse_pool))
                if was_follower and girl in Party:
                    $ Party.remove(girl)
                if _leaving_shower:
                    call _shower_leave_dressup(girl) from _call_shower_nerd_refuse
                $ girl.loc = "classroom"
                $ hide_girl_sprite(girl)
                if _in_her_room:
                    "You leave [girl.Name]'s room as well."
                    $ navigate_to("campus", None)
            return

# --------------------------------------------
# Unified processing of girls on time change
# --------------------------------------------
label process_girls_after_time_change:

    python:
        # We want each girl only once, even if she is both
        # in Party and in LastPresentGirls.
        to_process = []

        for g in Party:
            if g not in to_process:
                to_process.append(g)

        for g in LastPresentGirls:
            if g not in to_process:
                to_process.append(g)

        girls_list = to_process[:]

    while girls_list:
        $ g = girls_list.pop(0)
        call Girl_TimeChange_Handler(g) from _call_Girl_TimeChange_Handler

    return
