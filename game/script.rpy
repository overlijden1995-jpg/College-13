


# Stubs for removed label-scoped functions that old saves may reference during unpickle
define _shower_will_accept = None

image piracy_vid = Movie(play="audio/Arrgh.webm", loop=True, size=(1920, 1080))

screen piracy_warning():
    modal True
    frame:
        align (0.5, 0.5)
        padding (50, 40)
        background Frame(Solid("#000000dd"), 0, 0)
        xmaximum 1300
        vbox:
            spacing 30
            text _("It seems you downloaded the game from a sketchy source before the official version was public. I don't condemn piracy, but support the game and use official sources if you can, it's safe and keeps the project alive."):
                color "#ffffff"
                size 32
                text_align 0.5
                xalign 0.5
            hbox:
                spacing 40
                xalign 0.5
                textbutton _("I'll support the games if I can in the future!"):
                    action [SetVariable("_piracy_choice", "support"), Return()]
                    text_size 30
                    text_color "#4ade80"
                    text_hover_color "#86efac"
                textbutton _("I'm a nice guy"):
                    action [SetVariable("_piracy_choice", "quit"), Return()]
                    text_size 30
                    text_color "#f87171"
                    text_hover_color "#fca5a5"

label splashscreen:
    return
    $ _piracy_choice = None
    $ renpy.music.set_volume(1.0, channel="movie")
    scene black
    show piracy_vid
    $ renpy.pause(4.0, hard=True)
    call screen piracy_warning
    hide piracy_vid
    if _piracy_choice == "quit":
        $ renpy.quit()
    return

default corruption_enabled = False
default sexuality_locked = False
default hardcore_relationship = False
# The stepmother route (the girl whose GIRLS_CONFIG carries route_flag "_stepmom_route", her husband and their
# apartment). A NEW game asks (_stepmom_setup); an OLD save never had the variable, so this default turns it ON
# automatically on load. Off = she and the father are off the map for good (girl_away_reason "route_off") and the
# Downtown crossroads only leads to the mall.
default _stepmom_route = True
default _pre_launch_anal = False
default _pregnancy_mode = "off"
default _pregnancy_duration = "short"
default _player_fertility_vitamin_active = False
default _player_fertility_vitamin_days = 0
default _pregnancy_discovery_pending = None
default _npc_pat_accepted = False
default _npc_pregnancy_confrontation_pending = None
default _pregnancy_birth_pending = None
default _pregnancy_birth_queue = []      # more girls who went into labor the same day (_pregnancy_queue_birth)
default _wait_morning_done_day = -1      # label Wait: the once-per-morning region (6 to 6zz) ran for this Day (nested Wait)
default _stat_gain_carry = {}            # her personality's gain multiplier: the fraction each gain still owes her ("gid.Stat")
default _pregnancy_return_pending = None
default _cj_shady_intro = False
default _cj_harem_hint = False
default _cj_yuzu_intro = False
default _yuzu_purchased = False

label after_load:
    # The ONE rollback wall (the author, 2026-10-11: "sem rollback após save; antes disso, como era
    # antes"): a loaded game cannot roll back into the save's past. In-session rollback everywhere
    # else is free again (the scene-edge barriers of 2026-10-10 were removed).
    # purge=True EMPTIES the restored log, it does not just zero the counter: a plain block() leaves
    # the save's old entries in the log, and when the script changed since the save (every content
    # update), rollback skips the stale stop point, falls THROUGH the block into the save's past and
    # a return on that stale call stack lands on the MAIN MENU (the author, 2026-10-11, load+rollback).
    # With the log purged there is nothing before the load to fall into.
    $ renpy.block_rollback(purge=True)
    # CRITICAL: Restore init python functions that old saves may have overwritten with dicts.
    # Must run BEFORE anything that could trigger ConditionSwitch evaluation (renpy.show, set_girl_sprite).
    python:
        _RESTORE_MAP = [("_gs", "_orig_gs"), ("_ssg", "_orig_ssg"), ("_gsc", "_orig_gsc"),
                        ("_is_cheater", "_orig_is_cheater"), ("_tr", "_orig_tr"), ("_tl", "_orig_tl"),
                        ("_", "_orig_underscore")]
        for _fn_n, _orig_attr in _RESTORE_MAP:
            _cur = getattr(store, _fn_n, None)
            if not callable(_cur):
                _bk = getattr(renpy, _orig_attr, None)
                if _bk:
                    setattr(store, _fn_n, _bk)
                    print("[AFTER_LOAD] Restored %s from renpy.%s (was %s)" % (_fn_n, _orig_attr, type(_cur).__name__))
                else:
                    print("[AFTER_LOAD] WARNING: renpy.%s not found, cannot restore %s" % (_orig_attr, _fn_n))
    # init python recreates girls with default stats every launch.
    # Restore saved stats from the _girl_save snapshot.
    python:
        for _alg_dbg in ALL_GIRLS:
            _als = _girl_save.get(_alg_dbg.gid, {}) if _girl_save else {}
            debug_log("[AFTER_LOAD] gid=%s saved_clothes=%s saved_loc=%s" % (_alg_dbg.gid, str(_als.get("clothes", "MISSING")), str(_als.get("loc", "MISSING"))))
    $ _restore_girls(_girl_save)
    python:
        for _gid_mp, _cfg_mp in GIRLS_CONFIG.items():
            _g_mp = GIRL_BY_ID.get(_gid_mp)
            if _g_mp:
                _g_mp.mast_pose = _cfg_mp.get("mast_pose", "cowgirl")
    # Backfill any Girl/Player attributes added in newer versions
    python:
        _migration_patched = _backfill_girl_attrs()
        _player_patched = _backfill_player_attrs()
        _old_ver = getattr(store, "_save_version", None)
        _cur_ver = config.version
        _save_migrated = (_old_ver is None or _old_ver != _cur_ver)
        if _save_migrated:
            debug_log("[MIGRATE] Save version %s → %s" % (_old_ver, _cur_ver))
            if _migration_patched:
                for _mg, _ma in _migration_patched.items():
                    debug_log("[MIGRATE]   %s: %s" % (_mg, ", ".join(_ma)))
            if _player_patched:
                debug_log("[MIGRATE]   Player: %s" % ", ".join(_player_patched))
        for _alg_trait in ALL_GIRLS:
            _traits = getattr(_alg_trait, "traits", set()) or set()
            if "poly_friendly" in _traits:
                _traits.discard("poly_friendly")
                _traits.add("polyamorous")
                debug_log("[MIGRATE] %s: poly_friendly -> polyamorous" % _alg_trait.gid)
            # Migrate old lesbian proof/resistance -> sexuality_spectrum
            _had_old_proof = hasattr(_alg_trait, "_lesbian_proof")
            _had_old_res = hasattr(_alg_trait, "_lesbian_resistance")
            if _alg_trait.has_trait("lesbian") and (_had_old_proof or _had_old_res):
                _old_res = getattr(_alg_trait, "_lesbian_resistance", 100)
                _old_proof = getattr(_alg_trait, "_lesbian_proof", 0)
                if (_old_res < 100 or _old_proof > 0) and getattr(_alg_trait, "sexuality_spectrum", 100) == 100:
                    _old_dist = _old_res + 50 - _old_proof
                    _new_spec = max(50, min(100, int(75 + _old_dist / 4)))
                    _alg_trait.sexuality_spectrum = _new_spec
                    _alg_trait._lesbian_resistance = 100
                    _alg_trait._lesbian_proof = 0
                    _alg_trait._spectrum_temp_shift = 0
                    debug_log("[MIGRATE] %s: lesbian res=%d proof=%d -> spectrum=%d" % (_alg_trait.gid, _old_res, _old_proof, _new_spec))
            elif _had_old_proof and not (hasattr(_alg_trait, "sexuality_spectrum") and _alg_trait.sexuality_spectrum != 0):
                if _alg_trait.has_trait("bisexual"):
                    _alg_trait.sexuality_spectrum = 50
                    debug_log("[MIGRATE] %s: bisexual -> spectrum=50" % _alg_trait.gid)
                else:
                    _alg_trait.sexuality_spectrum = 0
                    debug_log("[MIGRATE] %s: hetero -> spectrum=0" % _alg_trait.gid)
                _alg_trait._spectrum_temp_shift = 0
        store._save_version = _cur_ver
    # Re-apply immutable config values that saves should not override
    python:
        for _alg_cfg in ALL_GIRLS:
            _cfg = GIRLS_CONFIG.get(_alg_cfg.gid, {})
            _alg_cfg.body_type = _cfg.get("body_type", "medium")
            _alg_cfg.bust = _cfg.get("bust", "medium")
    # Canon traits and the trait rules (girl type, blocked_traits) come from GIRLS_CONFIG: every save follows them
    python:
        for _alg_canon in ALL_GIRLS:
            enforce_canon_traits(_alg_canon, "load")
    # A girl who lives off campus follows the home / schedule of her config (Shion: the father's apartment)
    python:
        for _alg_home in ALL_GIRLS:
            sync_off_campus_home(_alg_home, "load")
        family_sync("load")
        exam_sync("load")
        story_sync("load")
        family_father_sync("load")
    # FamilyContact.Name is now a property (_tr); old saves have it in the instance dict, shadowing the property.
    python:
        if hasattr(store, "Dad") and isinstance(store.Dad, FamilyContact):
            _d = store.Dad.__dict__
            if "Name" in _d and not hasattr(store.Dad, "_name_en"):
                store.Dad._name_en = _d.pop("Name")
                debug_log("[MIGRATE] Dad: Name -> _name_en '%s'" % store.Dad._name_en)
            elif "Name" in _d:
                _d.pop("Name")
                debug_log("[MIGRATE] Dad: removed shadowing Name from instance dict")
    python:
        for _alg_dbg in ALL_GIRLS:
            debug_log("[AFTER_RESTORE] gid=%s clothes=%s loc=%s CurrentLocation=%s" % (_alg_dbg.gid, str(getattr(_alg_dbg, "clothes", {})), getattr(_alg_dbg, "loc", "?"), CurrentLocation))
    # Fallback: detect bikini store from CurrentLocation or girl clothes
    # (old saves created before _bk_in_store was tracked)
    python:
        if not store.bk_in_store:
            _al_loc = getattr(store, "CurrentLocation", "")
            if _al_loc == "dressing_room":
                store.bk_in_store = True
                store.bk_current_bg = "bg dressing_room"
                store.CurrentLocation = "mall"
                debug_log("[AFTER_LOAD] fallback: dressing_room -> _bk_in_store=True, CurrentLocation=mall")
            elif _al_loc == "mall":
                for _al_g in ALL_GIRLS:
                    if _al_g.loc == "mall" and getattr(_al_g, "clothes", {}).get("chest") in ("bikini_top",):
                        store.bk_in_store = True
                        store.bk_current_bg = "bg bikini_shop"
                        debug_log("[AFTER_LOAD] fallback: %s wearing bikini at mall -> _bk_in_store=True" % _al_g.gid)
                        break
    # Update scheduled locations but keep clothing from the snapshot
    # (outfit was already captured by the pre-save callback).
    $ update_all_girls_locations_for_time(Day, TimeIndex, reset_outfit=False)
    # Keep Party members with the player (update_all_girls moved them to schedule)
    python:
        for _alg_p in (Party if Party else []):
            _alg_p.loc = CurrentLocation
    if callable(globals().get("rebuild_npc_partners", None)):
        $ rebuild_npc_partners()
        $ update_all_npc_locations(Day, TimeIndex)
    # Ensure Player has inventory dict (old saves predate this attribute)
    if not hasattr(Player, "inventory"):
        $ Player.inventory = {}
    # Fertility vitamins are a buff, not an item (0.12.1): older saves kept a "Fertility Vitamins xN" that nothing uses
    python:
        if Player.inventory.pop("fertility_vitamin", None):
            print("[AFTER_LOAD] removed leftover fertility_vitamin inventory entry")
    # Migrate old saves to new clothes dict model
    python:
        for _alg in ALL_GIRLS:
            if not hasattr(_alg, "clothes") or not isinstance(getattr(_alg, "clothes", None), dict):
                _alg.clothes = {
                    "over": getattr(_alg, "_old_Over", None),
                    "chest": getattr(_alg, "_old_Chest", None),
                    "skirt": getattr(_alg, "_old_Legs", None),
                    "panties": getattr(_alg, "_old_Panties", None),
                    "shoes": getattr(_alg, "_old_Shoes", None),
                }
                _alg.clothes_state = {
                    "over": "up" if getattr(_alg, "_old_OverUp", False) else "full",
                    "chest": "up" if getattr(_alg, "_old_ChestUp", False) else "full",
                    "skirt": "up" if getattr(_alg, "_old_LegsDown", False) else "full",
                    "panties": "down" if getattr(_alg, "_old_PantiesDown", False) else "full",
                    "shoes": "full",
                }
    # Backfill oral key into Sex_acts for old saves
    python:
        for _alg in ALL_GIRLS:
            if hasattr(_alg, "Sex_acts") and "oral" not in _alg.Sex_acts:
                _alg.Sex_acts["oral"] = 0
    # Clean up stale random module reference from old saves
    if hasattr(store, "random") and not isinstance(getattr(store, "random", None), (int, float, str)):
        python:
            try:
                delattr(store, "random")
            except Exception:
                pass
    # Reset transient UI flags that may be stuck from crashed events
    $ store._phone_is_open = False
    # Reapply shower outfits if player is in showers
    if CurrentLocation == "showers":
        python:
            for _alg in ALL_GIRLS:
                _sh = getattr(_alg, "shower_state", None)
                if _sh and _sh != "dressed" and _alg.loc == "showers":
                    if _sh == "towel":
                        _alg.Over = "towel"
                        _alg.Chest = None
                        _alg.Legs = None
                        _alg.Panties = None
                        _alg.Shoes = None
                    elif _sh == "nude":
                        _alg.Over = None
                        _alg.Chest = None
                        _alg.Legs = None
                        _alg.Panties = None
                        _alg.Shoes = None
                    elif _sh == "underwear":
                        _alg.Over = None
                        _alg.Legs = None
                        _alg.Shoes = None
                    elif _sh == "missing_top":
                        _alg.Over = None
                        _alg.Chest = None
                        _alg.Shoes = None
                    elif _sh == "missing_bottom":
                        _alg.Legs = None
                        _alg.Panties = None
                        _alg.Shoes = None
    # Sanitize orphaned boolean flags: if the flag is True but
    # the corresponding girl ref is None, force to False so the
    # elif chain below reaches the correct branch.
    python:
        if getattr(store, "cowgirl_masturbating", False) and not getattr(store, "_cowgirl_girl", None):
            store.cowgirl_masturbating = False
        if getattr(store, "cowgirl_started", False) and not getattr(store, "_cowgirl_girl", None):
            store.cowgirl_started = False

    # ── Bikini store load-path diagnostics ──
    python:
        debug_log("[AFTER_LOAD] DIAG: _save_migrated=%s  _old_ver=%s  _cur_ver=%s" % (_save_migrated, _old_ver, _cur_ver))
        debug_log("[AFTER_LOAD] DIAG: _in_event=%s  _restaurant_bg=%s  _restaurant_girls=%s  CurrentLocation=%s" % (
            getattr(store, "_in_event", "MISSING"),
            getattr(store, "_restaurant_bg", "MISSING"),
            [g.gid for g in getattr(store, "_restaurant_girls", [])],
            getattr(store, "CurrentLocation", "MISSING")))
        debug_log("[AFTER_LOAD] DIAG: _bk_in_store=%s  _bk_current_bg=%s" % (
            getattr(store, "bk_in_store", "MISSING"),
            getattr(store, "bk_current_bg", "MISSING")))
        for _diag_g in ALL_GIRLS:
            debug_log("[AFTER_LOAD] DIAG: %s loc=%s clothes=%s" % (_diag_g.gid, _diag_g.loc, str(getattr(_diag_g, "clothes", {}))))

    # ── Safe-reset for saves from a different version ───────────
    # When loading a save created on ANY older (or newer) version,
    # abort whatever was happening and place the player in their room.
    # This avoids edge cases with changed functions mid-event.
    if _save_migrated:
        python:
            debug_log("[MIGRATE] Version change %s → %s, safe-resetting to room" % (_old_ver, _cur_ver))
            _migration_full_reset()
            _kill_scene_threads()
            renpy.scene()
            renpy.show("blackscreen")
        # rollback dies before the FIRST migration screen (tester report, 2026-10-09: wheeling up on the
        # arrival say still fell into the old save's log and skipped the whole migration)
        $ renpy.block_rollback()
        if _old_ver is not None:
            "Your save has been updated from v[_old_ver] to v[_cur_ver]. You've been moved to your room for safety. Your stats and progress are intact."
        else:
            "Your save is from an older version. You've been moved to your room for safety. Your stats and progress are intact. Starting a new game is recommended for the full experience."

        python:
            _ncr_old_known = getattr(store, "_known_trait_ids", None)
            _ncr_cur_ids = _all_trait_ids()
            _ncr_has_new = _ncr_old_known is None or bool(_ncr_cur_ids - _ncr_old_known)
            _ncr_old_girls = getattr(store, "_known_girl_gids", None)
            _ncr_has_new_girls = _ncr_old_girls is not None and bool(set(g.gid for g in ALL_GIRLS) - _ncr_old_girls)
            _ncr_offer = _ncr_has_new or _ncr_has_new_girls

        if _ncr_offer:
            # rollback dies HERE, before the first interaction: wheeling up at the review question used to
            # fall into the old save's own log (before the load) and cancel the whole migration (player
            # report, 2026-10-09). Inside the review the wheel can only reach this point: redo, never escape.
            $ renpy.block_rollback()
            $ renpy.say(None, _tl(_("New content has been added since your save was created. Would you like to review your girls' traits and pregnancy settings?")))
            menu:
                "Review new content":
                    call _new_content_review from _call_new_content_review
                "Skip, keep everything as is":
                    $ _stamp_known_content()
        else:
            $ _stamp_known_content()

        $ store._migration_needs_redirect = True; renpy.block_rollback()
        return

    # Rebuild the scene (background + girl sprites + HUD)
    # If in an active RCG scene, rebuild via ApplySpeed instead of Set_Scene
    if getattr(store, "cowgirl_masturbating", False):
        # Masturbation scene: rebuild cowgirl pose with correct expression
        python:
            _cg = getattr(store, "_cowgirl_girl", None)
            if _cg:
                store.cowgirl_arms_pose = 2
                store.cowgirl_guy_arms_visible = False
                store._cg_anim_origin = _time.time()
                store._mast_threads_running = True
                # Restore eyes closed if player is secretly watching
                if getattr(store, "_cg_eyes_locked", False):
                    _st = sprite_state.setdefault(_cg.Id, {})
                    _st["eyes"] = "eyes_closed"
                for _og in ALL_GIRLS:
                    if _og.gid != _cg.gid:
                        hide_girl_sprite(_og)
                renpy.invoke_in_thread(_scene_blink_loop, _cg, "_cowgirl_girl", "cg_blink")
                renpy.invoke_in_thread(_cg_expression_cycle, _cg)
        if _cg:
            call MASTURBATE_ApplySpeed(_cg, cowgirl_speed) from _call_MASTURBATE_ApplySpeed_after_load
            $ renpy.hide("cowgirl_guy")
        else:
            call Set_Scene(entry=False, quiet=True) from _call_Set_Scene_after_load_mast
    elif getattr(store, "_rcg_girl", None):
        python:
            _dg = store._rcg_girl
            _dg_speed = getattr(store, "rcg_speed", 0)
        if _dg:
            call RCG_ApplySpeed(_dg, _dg_speed) from _call_RCG_ApplySpeed_after_load
            python:
                renpy.invoke_in_thread(_scene_blink_loop, _dg, "_rcg_girl", "rcg_blink", is_active_fn=_rcg_is_active, cs_girls=_RCG_CS_GIRLS)
                renpy.invoke_in_thread(_rcg_expression_cycle, _dg)
        else:
            call Set_Scene(entry=False, quiet=True) from _call_Set_Scene_after_load
    elif getattr(store, "cowgirl_started", False):
        python:
            _cg = getattr(store, "_cowgirl_girl", None)
            if _cg:
                _cg_speed = getattr(store, "cowgirl_speed", 0)
        if _cg:
            call COWGIRL_ApplySpeed(_cg, _cg_speed) from _call_COWGIRL_ApplySpeed_after_load
            python:
                debug_log("[AFTER_LOAD] cowgirl branch: restarting blink/expression threads")
                renpy.invoke_in_thread(_scene_blink_loop, _cg, "_cowgirl_girl", "cg_blink")
                renpy.invoke_in_thread(_cg_expression_cycle, _cg)
        else:
            call Set_Scene(entry=False, quiet=True) from _call_Set_Scene_after_load_cg
    elif getattr(store, "_hj_girl", None):
        python:
            _hj = store._hj_girl
            debug_log("[AFTER_LOAD] hj branch: restarting blink/expression threads")
        call HJ_ApplySpeed(_hj, hj_speed) from _call_HJ_ApplySpeed_after_load
        python:
            renpy.invoke_in_thread(_scene_blink_loop, _hj, "_hj_girl", "hj_blink")
            renpy.invoke_in_thread(_hj_expression_cycle, _hj)
    elif getattr(store, "_bj_girl", None):
        python:
            _bj = store._bj_girl
            debug_log("[AFTER_LOAD] bj branch: restarting blink/cheeks threads")
            store._bj_cheeks_running = False
            store._bj_blink_running = False
        call BJ_ApplySpeed(_bj, bj_speed) from _call_BJ_ApplySpeed_after_load
        python:
            renpy.invoke_in_thread(_bj_cheeks_cycle)
            renpy.invoke_in_thread(_scene_blink_loop, _bj, "_bj_girl", "bj_blink", blink_timing=(0.10, 0.20), running_var="_bj_blink_running")
    elif getattr(store, "_titjob_girl", None):
        call TITJOB_ApplySpeed(store._titjob_girl, titjob_speed) from _call_TITJOB_ApplySpeed_after_load
    elif getattr(store, "_fn_girl", None):
        python:
            _fn_raw = store._fn_girl
            _fn_gid = getattr(_fn_raw, "gid", None)
            _fn = GIRL_BY_ID.get(_fn_gid, _fn_raw) if _fn_gid else _fn_raw
            store._fn_girl = _fn
            _fn_speed = getattr(store, "fn_speed", 0)
            debug_log("[AFTER_LOAD] fn branch: gid=%s clothes=%s states=%s speed=%d started=%s anal=%s" % (_fn_gid, str(_fn.clothes), str(_fn.clothes_state), _fn_speed, store.fn_started, store.fn_anal))
        if _fn:
            call FN_ApplySpeed(_fn, _fn_speed) from _call_FN_ApplySpeed_after_load
            python:
                renpy.invoke_in_thread(_scene_blink_loop, _fn, "_fn_girl", "fn_blink", is_active_fn=_fn_is_active, cs_girls={"ntw"}, blink_timing=(0.12, 0.22))
                renpy.invoke_in_thread(_fn_expression_cycle, _fn)
        else:
            call Set_Scene(entry=False, quiet=True) from _call_Set_Scene_after_load_fn
    elif getattr(store, "_doggy_girl", None):
        python:
            _dg_raw = store._doggy_girl
            _dg_gid = getattr(_dg_raw, "gid", None)
            _dg = GIRL_BY_ID.get(_dg_gid, _dg_raw) if _dg_gid else _dg_raw
            store._doggy_girl = _dg
            _dg_speed = getattr(store, "doggy_speed", 0)
            debug_log("[AFTER_LOAD] doggy branch: gid=%s clothes=%s states=%s speed=%d" % (_dg_gid, str(_dg.clothes), str(_dg.clothes_state), _dg_speed))
        if _dg:
            call DG_ApplySpeed(_dg, _dg_speed) from _call_DG_ApplySpeed_after_load
            python:
                renpy.invoke_in_thread(_scene_blink_loop, _dg, "_doggy_girl", "doggy_blink", cs_girls=_DG_CS_GIRLS, blink_timing=(0.12, 0.22))
                renpy.invoke_in_thread(_doggy_expression_cycle, _dg)
        else:
            call Set_Scene(entry=False, quiet=True) from _call_Set_Scene_after_load_dg
    elif getattr(store, "_in_event", False) and getattr(store, "_hangout_girl_a", None):
        python:
            _hg_a = store._hangout_girl_a
            _hg_b = getattr(store, "_hangout_girl_b", None)
            _hg_c = getattr(store, "_hangout_girl_c", None)
            _hg_npc = getattr(store, "_hangout_partner_npc", None)
            if not _hg_npc:
                _hg_npc = getattr(store, "_h_npc", None)
            if not _hg_npc:
                _hg_npc_id = getattr(store, "_hangout_partner_npc_id", None)
                if _hg_npc_id and _hg_npc_id in NPC_PARTNERS:
                    _hg_npc = NPC_PARTNERS[_hg_npc_id]
                    debug_log("[AFTER_LOAD] recovered NPC from id %s" % _hg_npc_id)
            _hg_all = [g for g in [_hg_a, _hg_b, _hg_c] if g is not None]
            if _hg_npc and len(_hg_all) < 3:
                store._hangout_partner_npc = _hg_npc
                store._h_npc = _hg_npc
            else:
                _hg_npc = None
                store._hangout_partner_npc = None
                store._h_npc = None
            debug_log("[AFTER_LOAD] hangout branch: ga=%s gb=%s gc=%s npc=%s girls=%d (src: partner=%s h_npc=%s id=%s)" % (
                _hg_a.gid if _hg_a else None,
                _hg_b.gid if _hg_b else None,
                _hg_c.gid if _hg_c else None,
                getattr(_hg_npc, "name", None) if _hg_npc else None,
                len(_hg_all),
                "yes" if getattr(store, "_hangout_partner_npc", None) else "no",
                "yes" if getattr(store, "_h_npc", None) else "no",
                getattr(store, "_hangout_partner_npc_id", None)))
        call Set_Scene(entry=False, show_chars=False, quiet=True) from _call_Set_Scene_after_load_hangout
        python:
            _hg_pos = [hangout_pos_a, hangout_pos_b, hangout_pos_c]
            for _hi, _hg in enumerate(_hg_all):
                if _hi < len(_hg_pos):
                    set_girl_sprite(_hg.gid, pose="standing", at_list=[_hg_pos[_hi]])
            if _hg_npc and hasattr(_hg_npc, "show_sprite"):
                _npc_slot = len(_hg_all)
                if _npc_slot < len(_hg_pos):
                    _hg_npc.show_sprite(_hg_pos[_npc_slot])
                store._h_npc = _hg_npc
            if not renpy.get_screen("tod_drunk_bars"):
                renpy.show_screen("tod_drunk_bars")
    elif getattr(store, "_restaurant_bg", None) and not any(getattr(store, _v, None) for _v in ("_laying_girl", "_doggy_girl", "_fn_girl", "_cowgirl_girl", "_rcg_girl", "_hj_girl", "_bj_girl", "_titjob_girl")):
        python:
            store._in_event = True
            _rest_bg = store._restaurant_bg
            renpy.scene()
            renpy.show(_rest_bg)
            if _rest_bg == "bg restaurant":
                renpy.show("restaurant_table", zorder=10)
            _rest_girls = getattr(store, "_restaurant_girls", [])
            if _rest_bg in ("bg restaurant", "bg campus_evening", "bg campus_night"):
                if len(_rest_girls) == 1:
                    set_girl_sprite(_rest_girls[0].gid, pose="standing", at_list=[slot_center])
                elif len(_rest_girls) >= 2:
                    set_girl_sprite(_rest_girls[0].gid, pose="standing", at_list=[slot_left])
                    set_girl_sprite(_rest_girls[1].gid, pose="standing", at_list=[slot_right])
            elif _rest_girls:
                set_girl_sprite(_rest_girls[0].gid, pose="standing", at_list=[slot_center])
            debug_log("[AFTER_LOAD] restaurant branch: bg=%s girls=%s _in_event_was=%s" % (_rest_bg, str([g.gid for g in _rest_girls]), getattr(store, "_in_event", "?")))
    elif getattr(store, "bk_in_store", False):
        python:
            _bk_bg = getattr(store, "bk_current_bg", "bg bikini_shop")
            renpy.scene()
            renpy.show(_bk_bg)
            _bk_girls = [g for g in Party if g.loc == "mall"]
            if _bk_bg == "bg bikini_shop":
                if len(_bk_girls) == 1:
                    set_girl_sprite(_bk_girls[0].gid, pose="standing", at_list=[slot_right])
                elif len(_bk_girls) >= 2:
                    set_girl_sprite(_bk_girls[0].gid, pose="standing", at_list=[slot_center])
                    set_girl_sprite(_bk_girls[1].gid, pose="standing", at_list=[slot_right])
            elif _bk_bg in ("bg dressing_room", "bg dressing_room_outside"):
                if len(_bk_girls) >= 1:
                    set_girl_sprite(_bk_girls[0].gid, pose="standing", at_list=[slot_center])
                if len(_bk_girls) >= 2:
                    set_girl_sprite(_bk_girls[1].gid, pose="standing", at_list=[slot_right])
            debug_log("[AFTER_LOAD] bikini store branch: bg=%s girls=%d" % (_bk_bg, len(_bk_girls)))
    elif getattr(store, "_laying_girl", None):
        python:
            _ld = store._laying_girl
            _ld_gid = getattr(_ld, "gid", None)
            _ld = GIRL_BY_ID.get(_ld_gid, _ld) if _ld_gid else _ld
            store._laying_girl = _ld
            _ld_mast = getattr(store, "_ld_masturbating", False)
            _ld_speed = getattr(store, "laying_speed", 0)
            debug_log("[AFTER_LOAD] laying_down branch: gid=%s mast=%s speed=%d" % (_ld_gid, _ld_mast, _ld_speed))
            _ld_bg = getattr(store, "_restaurant_bg", None) or get_bg_for_location()
            renpy.show(_ld_bg)
        if _ld_mast:
            call LD_MASTURBATE_ApplySpeed(_ld, _ld_speed) from _call_LD_MAST_AS_after_load
        else:
            call LD_ApplySpeed(_ld, _ld_speed) from _call_LD_AS_after_load
        python:
            renpy.invoke_in_thread(_ld_blink_loop, _ld)
            renpy.invoke_in_thread(_laying_expression_cycle, _ld)
    else:
        # Preserve saved display state: Ren'Py restores the display list from
        # save files natively. Calling Set_Scene here would run renpy.scene()
        # which clears all images and rebuilds from scratch, losing sprites
        # that were shown during events/menus/custom layouts.
        $ debug_log("[AFTER_LOAD] FALLTHROUGH: preserving saved display (no Set_Scene). _in_event=%s _bk_in_store=%s CurrentLocation=%s" % (getattr(store, "_in_event", "?"), getattr(store, "bk_in_store", "MISSING"), getattr(store, "CurrentLocation", "?")))
        # Refresh standing sprites for present girls so visuals match
        # the restored clothes state (the saved display may have been
        # cached before clothes were stripped).
        python:
            for _al_refresh in ALL_GIRLS:
                if _al_refresh.loc == CurrentLocation and renpy.showing(_al_refresh.Id):
                    set_girl_sprite(_al_refresh.Id, pose="standing")
                    debug_log("[AFTER_LOAD] refreshed sprite for %s" % _al_refresh.gid)

    # Block rollback past the load point to prevent stat zeroing
    $ renpy.block_rollback()
    return


label start:
    # Reset all girls to config defaults (init python only runs on app
    # launch, so without this Main Menu → New Game keeps old stats/traits)
    $ _reset_all_girls()

    # Stamp save version on new games
    $ _save_version = config.version

    # Initial state could be defined here or rely on defaults
    $ CurrentLocation = "campus"
    $ Day = 1
    $ TimeIndex = 0
    $ Round = 0

    # Player name input
    call name_input from _call_name_input

    # Skin color selection
    menu:
        "Choose your {b}skin color{/b}."
        "Light skin":
            $ Player.skin = "White"
        "Dark skin":
            $ Player.skin = "Black"

    # Rod's Choice — auto-setup from achievement analysis
    "I'll check your missing achievements and set up a game configuration to maximize your chances of finding new content."
    menu:
        "Trust Rod and let him set up your game?\n\nYou can fully customize your experience, add NPC boyfriends or girlfriends that are present in the game, change the girls' sexuality, or give them unique personality traits. If this is your first run, I recommend choosing everything yourself to see the full customization potential."
        "Yes, I trust Rod":
            # The pregnancy system changes the whole game (child support included): it stays HIS call even when Rod
            # sets up the rest. Asked BEFORE the pick, so the seeds built around it (needs_pregnancy) are only in
            # the draw when he turned it on.
            "Before I pick, one choice stays yours."
            call _pregnancy_setup from _call_pregnancy_setup_rod
            # the stepmom route is HIS call too (it adds a family storyline some players skip)
            call _stepmom_setup from _call_stepmom_setup_rod
            python:
                _rc_all_done = achievement_progress()[0] >= len(ACHIEVEMENTS)
                _rc_template = _rods_choice_pick()
                _rods_choice_apply(_rc_template)
            if _rc_all_done:
                "You've already unlocked all achievements! I picked a fun configuration for you. Seed '[_rc_template]' selected."
            else:
                "Thank you. Seed '[_rc_template]' selected."
            jump _after_rods_choice
        "No, I want to choose everything":
            pass

    # The stepmom route question comes BEFORE the trait picker: a disabled route keeps her out of it
    call _stepmom_setup from _call_stepmom_setup

    # Trait selection at game start
    call trait_setup from _call_trait_setup

    # Corruption system toggle
    "Do you want to enable the {b}Corruption{/b} feature?"
    menu:
        "Girls will gradually lose naive traits (like hating cum, hating cameras, being shy in public, preferring gentle sex, or being loyal) and gain their opposites as you push their boundaries."
        "Enable Corruption":
            $ corruption_enabled = True
            "Corruption is {b}ON{/b}. Traits will evolve over time."
        "Disable Corruption":
            $ corruption_enabled = False
            "Corruption is {b}OFF{/b}. Traits will stay as assigned."

    # Sexuality lock toggle
    menu:
        "Can a girl's sexuality change during the game? Lesbians may discover attraction to men, and straight girls may explore attraction to women, eventually becoming bisexual."
        "Allow Sexuality Changes":
            $ sexuality_locked = False
        "Lock Initial Sexuality":
            $ sexuality_locked = True

    # Hardcore Relationship Mode toggle
    "Do you want to enable {b}Hardcore Relationship Mode{/b}?"
    menu:
        "Girls with partners will grow closer to them over time if you don't give them enough attention. Ignore them too long, and they'll start doing things with their partner they haven't done before. Single girls who feel neglected may even find a partner on their own."
        "Enable Hardcore Mode":
            $ hardcore_relationship = True
            "Hardcore Relationship Mode is {b}ON{/b}. Neglect has consequences."
        "Disable Hardcore Mode":
            $ hardcore_relationship = False
            "Hardcore Relationship Mode is {b}OFF{/b}. Boyfriends stay passive."

    # Pregnancy system toggle
    call _pregnancy_setup from _call_pregnancy_setup_manual

    # Player trait selection
    menu:
        "Choose a {b}Player Trait{/b}. This will affect your starting stats and passive bonuses."
        "{b}Athlete{/b} - Start with 4 max energy (instead of 2)":
            $ Player.player_trait = "athlete"
            $ Player.energy_max = 4
            $ Player.energy = 4
            "You start with more energy. Hit the gym to keep it up."

        "{b}Fast Learner{/b} - Study twice as fast":
            $ Player.player_trait = "fast_learner"
            "Your study sessions are twice as effective."

        "{b}Investor{/b} - Start with $500 + earn $50 daily passive income":
            $ Player.player_trait = "investor"
            $ Player.add_cash(400)
            "You start with extra cash and earn money passively every day."

        "{b}Charming{/b} - Girls start with +50 Love":
            $ Player.player_trait = "charming"
            python:
                for _g in ALL_GIRLS:
                    _g.Love = min(1000, _g.Love + 50)
            "Girls find you naturally attractive."

        "{b}No Trait{/b} - Play without bonuses":
            $ Player.player_trait = "none"
            "You chose the hard way. Good luck."

    # Secret variables menu
    menu:
        "Do you want to choose the {b}secret variables{/b}? They have a minor impact on the game and it can be fun to discover them through hints."
        "Choose manually":
            call _secret_variables_setup from _call_secret_vars
        "Keep it random":
            pass

label _after_rods_choice:

    # Initial pill state. It needs the pregnancy mode AND the girls' final traits, so it runs here, where the manual
    # setup and Rod's Choice meet (it used to run inside _reset_all_girls at the top of label start, with the
    # mode still "off" and no trait chosen: it never put anybody on the pill).
    python:
        for _ips_girl in ALL_GIRLS:
            _pregnancy_init_pill_state(_ips_girl)

    # Build NPC partners (after secret vars so NTR choice takes effect)
    if callable(globals().get("rebuild_npc_partners", None)):
        $ rebuild_npc_partners()
        $ update_all_npc_locations(Day, TimeIndex)

    # Stamp trait/girl catalog so future updates can detect new content
    $ _stamp_known_content()

    # First snapshot so saves during intro already have girl data
    $ _girl_save = _snapshot_girls()

    # Mark sandbox as inactive during pre-game setup
    $ store._in_sandbox = False
    $ debug_log("[STATE] _in_sandbox = False (pre-game setup)")

    # Virginity blood toggle
    menu:
        "Can virgin girls bleed when losing their virginity?"
        "No, no blood!":
            $ virginity_blood = False
            "Virginity blood is {b}OFF{/b}. No blood effects during first time scenes."
        "Yes, not afraid to get the sword dirty!":
            $ virginity_blood = True
            "Virginity blood is {b}ON{/b}. Virgin girls may bleed during their first time."

    menu:
        "Play Intro":
            # First-time campus tour intro
            $ store._in_intro = True
            $ debug_log("[STATE] _in_intro = True")
            call intro from _call_intro
            $ store._in_intro = False
            $ debug_log("[STATE] _in_intro = False")

        "Skip Intro (you will miss the first interactions)":
            "Have fun!"

    # His family (shion_family.rpy): their numbers are in his phone from the start
    $ family_sync("new game")
    $ exam_sync("new game")
    $ story_sync("new game")

    # Start gameplay in the player's room
    $ store._in_sandbox = True
    $ debug_log("[STATE] _in_sandbox = True (entering sandbox)")
    jump Player_Room_Entry


# ============================================================
# PREGNANCY SETUP: asked by the manual setup AND by Rod's Choice right before it picks a seed
# ============================================================
# Underscore label on purpose, placed before the next regular label: the translation ids of its lines stay
# under "start" (a label starting with "_" only adds an alternate id).
label _pregnancy_setup:
    $ renpy.say(None, _tl(_("Do you want to enable the {b}Pregnancy{/b} system?")))
    menu:
        "Girls can get pregnant from unprotected sex. Includes fertility cycles, contraceptives, discovery events, and consequences. Full mode adds visual belly stages."
        "Full Mode (visuals + mechanics)":
            $ _pregnancy_mode = "full"
            $ renpy.say(None, _tl(_("Pregnancy is {b}FULL{/b}. Visual stages, discovery events, and all mechanics.")))
        "Lite Mode (text only)":
            $ _pregnancy_mode = "lite"
            $ renpy.say(None, _tl(_("Pregnancy is {b}LITE{/b}. Text narration only, no visual changes.")))
        "Disable Pregnancy":
            $ _pregnancy_mode = "off"
            $ renpy.say(None, _tl(_("Pregnancy is {b}OFF{/b}. No one gets pregnant.")))

    if _pregnancy_mode != "off":
        $ renpy.say(None, _tl(_("Choose pregnancy duration. This affects how long each pregnancy lasts.")))
        menu:
            "Short (65 days)":
                $ _pregnancy_duration = "short"
                $ renpy.say(None, _tl(_("Short pregnancy. About two in-game months.")))
            "Long (130 days)":
                $ _pregnancy_duration = "long"
                $ renpy.say(None, _tl(_("Long pregnancy. Full in-game term.")))
    return

# ============================================================
# STEPMOM ROUTE SETUP: asked by the manual setup AND by Rod's Choice right before it picks a seed.
# An old save never gets asked: the `default _stepmom_route = True` turns the route on when it loads.
# ============================================================
label _stepmom_setup:
    $ renpy.say(None, _tl(_("One more choice: the {b}Stepmother{/b} route. {b}Warning{/b}: this storyline is about seducing a married woman of your own family, behind your father's back, in his house.")))
    menu:
        "It adds your father's apartment downtown, your father himself, his wife and her whole story. You can only choose this when starting a new game."
        "Enable the Stepmother route":
            $ _stepmom_route = True
            $ renpy.say(None, _tl(_("The Stepmother route is {b}ON{/b}. The apartment downtown is on your map.")))
        "Disable the Stepmother route":
            $ _stepmom_route = False
            $ renpy.say(None, _tl(_("The Stepmother route is {b}OFF{/b}. She and your father stay out of this run, and Downtown only leads to the mall.")))
    return


label main_loop:

    # Safety reset: ensure state flags are clean when entering the sandbox loop
    $ store._in_event = False
    $ store._in_intro = False
    $ store._in_sandbox = True
    python:
        for _sg in [("_hj_girl", None), ("_bj_girl", None), ("_titjob_girl", None),
                     ("_cowgirl_girl", None), ("_rcg_girl", None), ("_doggy_girl", None)]:
            if getattr(store, _sg[0], None) is not None:
                debug_log("[SAFETY] %s was stuck as not-None in main_loop, clearing" % _sg[0])
                setattr(store, _sg[0], None)
        store.doggy_started = False
        store.cowgirl_started = False
        store.cowgirl_masturbating = False

    call Set_Scene from _call_Set_Scene

    $ weekday_index = (Day - 1) % 7
    $ Narration(_("Day [Day] ([WEEK_DAYS[weekday_index]]), [TIME_NAMES[TimeIndex]] (Round [Round]/100)."))

    call location_menu from _call_location_menu

    # Snapshot girl state after all interactions (backup — _sync_girl handles per-change)
    $ _girl_save = _snapshot_girls()

    jump main_loop


# ============================================================
# TRAIT SETUP — Game start personality assignment
# ============================================================

label trait_setup:

    "Traits are how you customize your experience. They heavily influence gameplay and can lock or unlock different events."

    menu:
        "You can pick them yourself or let the game decide and discover them through the mechanics as you play. {b}Multiple runs may be needed to see everything.{/b}"
        "Randomize and Start":
            call trait_setup_random from _call_trait_setup_random
        "Select the same for all":
            call trait_setup_same_for_all from _call_trait_setup_same_for_all
        "Choose per girl (Manual or Random)":
            call trait_setup_per_girl from _call_trait_setup_per_girl

    return


# --- Randomize all girls ---
label trait_setup_random:

    python:
        for _g in ALL_GIRLS:
            randomize_traits_for(_g)
        if _check_hardcore_traits():
            unlock_achievement("hardcore_player")

    return


# --- Same traits for all girls ---
label trait_setup_same_for_all:

    python:
        _trait_opposites = {}
        for _pair in TRAIT_PAIRS:
            _trait_opposites[_pair["a"]] = _pair["b"]
            _trait_opposites[_pair["b"]] = _pair["a"]

        _trait_manual_pick(ALL_GIRLS[0], _trait_opposites)
        _shared_traits = set(t for pair in TRAIT_PAIRS for t in (pair["a"], pair["b"]) if ALL_GIRLS[0].has_trait(t))
        _shared_traits |= set(st["id"] for st in SYSTEM_TRAITS if ALL_GIRLS[0].has_trait(st["id"]))

        for _g in ALL_GIRLS[1:]:
            _clear_girl_traits(_g)
            _g_canon = set(GIRLS_CONFIG.get(_g.gid, {}).get("traits", []))
            # Only what she can ever have: her canon wins a conflict, her girl type / blocked_traits rule
            _merged = set(_t for _t in _shared_traits if trait_possible_for(_g, _t)) | _g_canon
            for tid in sorted(_merged, key=lambda t: 2 if t in ("experienced", "naive") else 0):
                st_match = [s for s in SYSTEM_TRAITS if s["id"] == tid]
                if st_match and st_match[0].get("on_add") == "set_npc_partner":
                    _g.add_trait(tid)
                    _g.set_npc_partner("npc_bf_%s" % _g.gid)
                elif st_match and st_match[0].get("on_add") == "set_npc_partner_female":
                    _g.add_trait(tid)
                    _g.set_npc_partner_female("npc_gf_%s" % _g.gid)
                elif st_match and st_match[0].get("on_add") == "set_experienced":
                    _g.add_trait(tid)
                    _apply_experienced(_g)
                elif st_match and st_match[0].get("on_add") == "set_naive":
                    _g.add_trait(tid)
                    _apply_naive(_g)
                else:
                    _g.add_trait(tid)
            enforce_canon_traits(_g, "same_for_all", fresh=True)
            _apply_gym_rat_schedule(_g)

    call _trait_show_summary from _call_trait_show_summary_2
    if _check_hardcore_traits():
        $ unlock_achievement("hardcore_player")
    return


# --- Per girl: choose manual or random individually ---
label trait_setup_per_girl:

    python:
        _trait_opposites = {}
        for _pair in TRAIT_PAIRS:
            _trait_opposites[_pair["a"]] = _pair["b"]
            _trait_opposites[_pair["b"]] = _pair["a"]

    python:
        # girls_reachable: a girl whose optional route is off (the stepmom, _stepmom_setup) never shows up here
        for _g in girls_reachable():
            _choice = renpy.display_menu([
                (_tl(_("Choose traits for %s manually")) % _g.Name, "manual"),
                (_tl(_("Randomize traits for %s")) % _g.Name, "random"),
            ])
            if _choice == "random":
                randomize_traits_for(_g)
                # Show immediate result
                _verbal = _trait_list_verbal(_g)
                if _verbal:
                    renpy.say(None, _tl(_("{b}%s{/b} (randomized): %s.")) % (_g.Name, ". ".join(_verbal)))
                else:
                    renpy.say(None, _tl(_("%s: No personality traits (random).")) % _g.Name)
            else:
                _trait_manual_pick(_g, _trait_opposites)
                _verbal = _trait_list_verbal(_g)
                if _verbal:
                    renpy.say(None, _tl("{b}%s{/b}: %s.") % (_g.Name, ". ".join(_verbal)))
                else:
                    renpy.say(None, _tl(_("%s: No personality traits.")) % _g.Name)

    if _check_hardcore_traits():
        $ unlock_achievement("hardcore_player")
    return


label _secret_variables_setup:

    # --- Attractiveness ---
    menu:
        "Are you {b}attractive{/b}?"
        "Yes (maximum attractiveness)":
            $ Player.attractiveness = 100
            "You know you look good."
        "No :c (minimum attractiveness)":
            $ Player.attractiveness = 0
            "Looks aren't everything... right?"
        "I'm ok (average)":
            $ Player.attractiveness = 50
            "Nothing special, nothing terrible."
        "Random":
            pass

    # --- NPC Partner Traits (per girl) ---
    $ _sv_partnered = [g for g in ALL_GIRLS if g.get_flag("has_npc_partner")]

    python:
        for _sv_g in _sv_partnered:
            _npc_trait_manual_pick(_sv_g)

    return


# --- Shared helpers ---
init python:

    # ── Centralized translation dict for init-time strings ──
    # Ren'Py's _() doesn't work in init blocks or screen $ statements.
    # This dict + _tr() function handles runtime translation for those cases.
    _I18N = {
        "pt": {
            # TIME / WEEKDAY
            "Morning": "Manhã", "Midday": "Meio-dia", "Evening": "Entardecer", "Night": "Noite",
            "Sunday": "Domingo", "Monday": "Segunda", "Tuesday": "Terça",
            "Wednesday": "Quarta", "Thursday": "Quinta", "Friday": "Sexta", "Saturday": "Sábado",
            # HUD format
            "[weekday_name!u], DAY [Day]": "[weekday_name!u], DIA [Day]",
            # Trait categories
            "Camera": "Câmera", "Cum": "Sêmen", "Public": "Público",
            "Sex Style": "Estilo Sexual", "Loyalty": "Lealdade", "Anal": "Anal", "Economy": "Economia", "Sharing": "Compartilhamento", "Fertility": "Fertilidade", "Pregnancy": "Gravidez",
            # Trait pair labels
            "Camera Lover": "Ama Câmera", "Camera Hater": "Odeia Câmera",
            "Cum Lover": "Ama Sêmen", "Cum Hater": "Odeia Sêmen",
            "Public Fetish": "Fetiche Público", "Public Shy": "Tímida em Público",
            "Hardcore": "Hardcore", "Gentle": "Gentil",
            "Loyal": "Leal", "Cheater": "Traidora",
            "Anal Lover": "Ama Anal", "Anal Hater": "Odeia Anal",
            "Poor": "Pobre", "Rich": "Rica",
            # Trait pair descriptions
            "Loves being filmed. May ask to be recorded.": "Adora ser filmada. Pode pedir pra ser gravada.",
            "Hates cameras. Very resistant to filming.": "Odeia câmeras. Muito resistente a filmagens.",
            "Loves cum inside her. Hates condoms.": "Adora sêmen dentro dela. Odeia camisinhas.",
            "Hates cum contact. Demands condoms.": "Odeia contato com sêmen. Exige camisinhas.",
            "Turned on by public exposure and risk.": "Excitada por exposição pública e risco.",
            "Terrified of public exposure.": "Apavorada com exposição pública.",
            "Prefers rough, fast, intense sex.": "Prefere sexo bruto, rápido e intenso.",
            "Prefers slow, intimate, gentle sex.": "Prefere sexo lento, íntimo e gentil.",
            "Strongly resists cheating. Hard to corrupt.": "Resiste fortemente a trair. Difícil de corromper.",
            "Cheating is easy and enjoyable for her.": "Trair é fácil e prazeroso pra ela.",
            "Loves anal. Gets more pleasure, may ask for it.": "Adora anal. Sente mais prazer, pode pedir.",
            "Hates/fears anal. Pain-focused, very resistant.": "Odeia/tem medo de anal. Focada na dor, muito resistente.",
            "Struggles financially. Gifts mean more to her.": "Dificuldades financeiras. Presentes significam mais.",
            "Wealthy background. Hard to impress with gifts.": "Família rica. Difícil de impressionar com presentes.",
            # System trait labels
            "Naive": "Inocente", "Experienced": "Experiente", "Voyeur": "Voyeur",
            "Exhibitionist": "Exibicionista", "Has a Boyfriend": "Tem Namorado",
            "Has a Girlfriend": "Tem Namorada", "Lesbian": "Lésbica", "Bisexual": "Bissexual",
            # System trait descriptions
            "Has never done anything sexual. No history at all. Forces Virgin.": "Nunca fez nada sexual. Sem histórico algum. Força Virgem.",
            "Has not had sex yet.": "Ainda não fez sexo.",
            "Has done everything before with someone else. Not a virgin, knows what she's doing.": "Já fez de tudo antes com outra pessoa. Não é virgem, sabe o que está fazendo.",
            "Likes watching others.": "Gosta de assistir os outros.",
            "Likes being watched.": "Gosta de ser observada.",
            "She already has an NPC boyfriend at game start. The boyfriend will be present in the game.": "Ela já tem namorado no início do jogo. O namorado estará presente no jogo.",
            "She already has an NPC girlfriend at game start. The girlfriend will be present in the game.": "Ela já tem namorada no início do jogo. A namorada estará presente no jogo.",
            "Only attracted to women. Requires dominance or leverage for sexual acts.": "Só atraída por mulheres. Requer dominância ou chantagem para atos sexuais.",
            "Attracted to both men and women. Can have a boyfriend or girlfriend. Uses normal mechanics.": "Atraída por homens e mulheres. Pode ter namorado ou namorada. Usa mecânicas normais.",
            # Trait verbal (summary after selection)
            "She loves being on camera": "Ela adora estar na câmera",
            "She hates cameras": "Ela odeia câmeras",
            "She loves cum": "Ela adora sêmen",
            "She hates cum": "Ela odeia sêmen",
            "She likes doing it in public": "Ela gosta de fazer em público",
            "She's terrified of public exposure": "Ela tem pavor de exposição pública",
            "She likes it rough": "Ela gosta de sexo bruto",
            "She likes it gentle": "Ela gosta de sexo gentil",
            "She's very loyal": "Ela é muito leal",
            "She's open to cheating": "Ela é aberta a trair",
            "She's completely inexperienced": "Ela é completamente inexperiente",
            "She likes watching others": "Ela gosta de assistir os outros",
            "She likes being watched": "Ela gosta de ser observada",
            "She's open to sharing": "Ela é aberta a compartilhar",
            "She already has a boyfriend": "Ela já tem namorado",
            "She already has a girlfriend": "Ela já tem namorada",
            "She has done everything with her partner": "Ela já fez de tudo com o parceiro",
            "She loves anal": "Ela adora anal",
            "She hates anal": "Ela odeia anal",
            "She's only attracted to women": "Ela só é atraída por mulheres",
            "She's attracted to both men and women": "Ela é atraída por homens e mulheres",
            "She struggles financially": "Ela tem dificuldades financeiras",
            "She comes from a wealthy background": "Ela vem de uma família rica",
            "She can hold her liquor": "Ela aguenta bem a bebida",
            "She can't handle her drinks": "Ela não aguenta beber",
            "She's a total bookworm": "Ela é uma nerd total",
            "She lives at the gym": "Ela vive na academia",
            "Extra breedable": "Super fértil",
            "Infertile": "Infértil",
            "She has a pregnancy fetish": "Ela tem fetiche por gravidez",
            "She's terrified of getting pregnant": "Ela tem pavor de engravidar",
            # Screen UI
            "(not available)": "(não disponível)",
            "(opposite selected)": "(oposto selecionado)",
            "(locked: lesbian)": "(bloqueado: lésbica)",
            "(locked: pregnancy fetish)": "(bloqueado: fetiche por gravidez)",
            "(locked: has girlfriend)": "(bloqueado: tem namorada)",
            "(locked: naive)": "(bloqueado: inocente)",
            "(conflict)": "(conflito)",
            "Personality Traits": "Características de Personalidade",
            "Done": "Pronto",
            "Randomize the rest (fill to 3)": "Aleatorizar o resto (completar até 3)",
            "TRAITS": "CARACTERÍSTICAS",
            # Discovery banners
            "She is dating someone": "Ela está namorando alguém",
            "She has no boyfriend": "Ela não tem namorado",
            "Study habits discovered": "Hábitos de estudo descobertos",
            "Favorite act discovered": "Ato favorito descoberto",
            "She accepted your petname": "Ela aceitou seu apelido",
            "She has a name for you": "Ela tem um nome pra você",
            "Her first kiss": "Primeiro beijo dela",
            "You're her first handjob": "Você é a primeira punheta dela",
            "You're her first titjob": "Você é a primeira espanhola dela",
            "You're her first blowjob": "Você é o primeiro boquete dela",
            "She's never done this for anyone": "Ela nunca fez isso pra ninguém",
            "You took her virginity": "Você tirou a virgindade dela",
            "You're her first anal": "Você é o primeiro anal dela",
            "First time raw": "Primeira vez sem camisinha",
            "First creampie": "Primeiro creampie",
            "She struggles with money": "Ela tem dificuldades financeiras",
            "She comes from money": "Ela vem de família rica",
            "She's a virgin": "Ela é virgem",
            "She's not a virgin": "Ela não é virgem",
            "BF never did: %s": "Namorado nunca fez: %s",
            "BF has done: %s": "Namorado já fez: %s",
            "BF": "Namorado",
            "GF": "Namorada",
            "never did": "nunca fez",
            "has done": "ja fez",
            # Player discoveries
            "Your first kiss": "Seu primeiro beijo",
            "Your first handjob": "Sua primeira punheta",
            "Your first titjob": "Seu primeiro titjob",
            "Your first blowjob": "Seu primeiro boquete",
            "Lost your virginity": "Perdeu a virgindade",
            "Your first anal": "Seu primeiro anal",
            "Your first creampie": "Seu primeiro creampie",
            "First time going raw": "Primeira vez sem camisinha",
            "You took someone's virginity": "Você tirou a virgindade de alguém",
            "You got your first girlfriend": "Você conseguiu sua primeira namorada",
            "Peak physical condition": "Condição física máxima",
            "New intel acquired": "Nova informação adquirida",
            "New Trait Discovered": "Nova Característica Descoberta",
            # C. Johnson intel labels (Status screen)
            "C. JOHNSON'S INTEL": "INTEL DO C. JOHNSON",
            "People are gossiping": "Estão fofocando sobre você",
            "Your breakup is known": "Sabem do seu término",
            "Professors noticed you": "Professores notaram você",
            "Girls find you handsome": "Garotas te acham bonito",
            "You... You are ugly :c": "Você... Você é feio :c",
            "%s is changing": "%s está mudando",
            "%s is hostile to you": "%s é hostil com você",
            "%s is not jealous": "%s não é ciument(a)",
            "%s is jealous": "%s é ciument(a)",
            "Hotdogs recover energy": "Cachorro quente recupera energia",
            "Give gifts to pay for sex": "Dê presentes para pagar por sexo",
            "No intel yet": "Nenhuma intel ainda",
            # Status screen — relationship & NPC labels
            "Your Girlfriend": "Sua Namorada",
            "Stranger": "Desconhecida",
            "Acquaintance": "Conhecida",
            "Friend": "Amiga",
            "Close Friend": "Amiga Próxima",
            "Intimate": "Íntima",
            "Ex": "Ex",
            "Friendly": "Amigável",
            "Neutral": "Neutro",
            "Hostile": "Hostil",
            "NTR": "NTR",
            "Proud": "Orgulhoso",
            "PARTNER TRAITS": "CARACTERÍSTICAS DO PARCEIRO",
            "Disposition": "Disposição",
            "Enjoys watching and sharing. Never breaks up over cheating.": "Gosta de assistir e compartilhar. Nunca termina por traição.",
            "Jealous and possessive. Will break up quickly if caught.": "Ciumento e possessivo. Termina rápido se pegar no flagra.",
            "Slightly jealous. May break up eventually.": "Levemente ciumento. Pode terminar eventualmente.",
            "Preferences": "Preferências",
            "Wants to watch in person.": "Quer assistir pessoalmente.",
            "Wants videos of her.": "Quer vídeos dela.",
            "NTR Limits": "Limites NTR",
            "What is the initial boundary the partner is comfortable with? You can push these limits during gameplay and unlock new scenarios.": "Qual é o limite inicial que o parceiro se sente confortável? Você pode evoluir esses limites ao longo do jogo e criar vários cenários.",
            "Randomize All": "Aleatorizar Tudo",
            "Lesbian partners do not have boundary levels.": "Parceiras lésbicas não possuem níveis de limite.",
            "In love": "Apaixonado",
            "Moderate": "Moderado",
            "Low": "Baixo",
            "Very suspicious": "Muito desconfiado",
            "Suspicious": "Desconfiado",
            "Uneasy": "Inquieto",
            "Unaware": "Sem suspeitas",
            # Status screen — study levels
            "Very prepared": "Muito preparado",
            "Well studied": "Bem estudado",
            "Somewhat prepared": "Razoavelmente preparado",
            "Barely studied": "Mal estudou",
            "Hasn't studied at all": "Não estudou nada",
            # Status screen — friendship labels
            "Best Friends": "Melhores Amigas",
            "Friends": "Amigas",
            "Acquaintances": "Conhecidas",
            # Status screen — trait hints
            "Virgin": "Virgem",
            "Loves being filmed": "Adora ser filmada",
            "Hates cameras": "Odeia câmeras",
            "Loves cum": "Adora esperma",
            "Hates cum": "Odeia esperma",
            "Turned on by public risk": "Excitada pelo risco público",
            "Terrified of exposure": "Aterrorizada com exposição",
            "Likes it rough": "Gosta de sexo bruto",
            "Likes it gentle": "Gosta de sexo suave",
            "Very loyal": "Muito fiel",
            "Prone to cheating": "Tendência a trair",
            "Likes watching": "Gosta de observar",
            "Likes being watched": "Gosta de ser observada",
            "Open to sharing": "Aberta a compartilhar",
            # Status screen — player study (shorter variant)
            "Hasn't studied": "Não estudou",
            # Status screen — firsts act labels
            "Kiss": "Beijo",
            "Handjob": "Punheta",
            "Titjob": "Espanhola",
            "Footjob": "Footjob",
            "Rimjob": "Beijo grego",
            "Father's Apartment (Not with company)": "Apartamento do Pai (Não com companhia)",
            "Talk about her (Already today)": "Falar dela (Já hoje)",
            "Give him a drink (No drinks)": "Dar uma bebida (Sem bebidas)",
            "Blowjob": "Boquete",
            "Sex": "Sexo",
            # Status screen — BigFans labels & tags
            "Any video": "Qualquer vídeo",
            "cheating": "traição",
            "public": "público",
            "cuckold": "corno",
            "threesome": "menage",
            "face visible": "rosto visível",
            "face hidden": "rosto escondido",
            "secret": "secreto",
            "HD": "HD",
            "%s stopped the recording.": "%s parou de gravar.",
            "Masturbation": "Masturbação",
            "Cowgirl": "Cowgirl",
            "Reverse Cowgirl": "Reverse Cowgirl",
            "Doggy Style": "De Quatro",
            "Full Nelson": "Full Nelson",
            "Full Nelson Anal": "Full Nelson Anal",
            "Laying Down": "Deitada", "Laying Down Anal": "Anal Deitada",
            "Reverse Cowgirl Anal": "Reverse Cowgirl Anal",
            "Creampie": "Creampie",
            "LOSING VIRGINITY": "PERDENDO A VIRGINDADE",
            "%dd left": "%dd restante",
            "Expires today!": "Expira hoje!",
            # Status screen — video locations
            "%s's Room": "Quarto de %s",
            "Campus": "Campus",
            "Pool": "Piscina",
            "Showers": "Chuveiros",
            "Apartment": "Apartamento",
            "Apartment Bedroom": "Quarto do Apartamento",
            "Apartment Bathroom": "Banheiro do Apartamento",
            "Gym": "Academia",
            "Classroom": "Sala de Aula",
            "Mall": "Shopping",
            "Hall": "Corredor",
            "Street": "Rua",
            "Party": "Festa",
            "Restaurant Restroom": "Banheiro do Restaurante",
            "Gwen's Room": "Quarto da Gwen",
            "Rogue's Room": "Quarto da Rogue",
            "Negasonic's Room": "Quarto da Negasonic",
            # Navigation — disabled menu items
            "Class (Closing soon)": "Aula (Fechando em breve)",
            "Class (Closed)": "Aula (Fechada)",
            "Gym (Closing soon)": "Academia (Fechando em breve)",
            "Gym (Closed)": "Academia (Fechada)",
            "Mall (Closing soon)": "Shopping (Fechando em breve)",
            "Mall (Closed)": "Shopping (Fechado)",
            "Study (Too late)": "Estudar (Muito tarde)",
            "Wait (It's night)": "Esperar (É noite)",
            # Near/Far roster
            "Call someone over...": "Chamar alguém...",
            "Who do you want to call over?": "Quem você quer chamar?",
            "Who should leave?": "Quem deve sair?",
            "%s walks over.": "%s se aproxima.",
            "You hear %s arrive nearby.": "Você ouve %s chegando perto.",
            "After a while, %s arrives.": "Depois de um tempo, %s chega.",
            # Petname announcements
            "Hey... I've been thinking. Can I call you %s from now on?": "Ei... eu estava pensando. Posso te chamar de %s de agora em diante?",
            "You feel more like a %s to me now... is that okay?": "Você parece mais um %s pra mim agora... tudo bem?",
            "I want to start calling you %s. What do you think?": "Eu quero começar a te chamar de %s. O que você acha?",
            # Petnames (display)
            "Princess": "Princesa",
            "Babe": "Bebê",
            "Honey": "Docinho",
            "Love": "Amor",
            "Angel": "Anjo",
            "Slut": "Puta",
            "Whore": "Vagabunda",
            "Cumdumpster": "Vadia",
            "Cutie": "Fofinho",
            "Pumpkin": "Pudinzinho",
            "Sugar": "Docinho",
            "Sweetheart": "Lindinho",
            "Tiger": "Tigrão",
            "Daddy": "Papai",
            "Master": "Mestre",
            "Sir": "Senhor",
            "Queen": "Rainha",
            "Goddess": "Deusa",
            "Mistress": "Senhora",
            "Pet": "Bichinho",
            "Toy": "Brinquedo",
            "Good boy": "Bom garoto",
            "Stepmom": "Madrasta",
            "Boy": "Garoto",
            # Inventory
            "Condoms": "Camisinhas",
            "Japanese Condoms": "Camisinhas Japonesas",
            "Condom": "Camisinha",
            "JP Condom": "Camisinha JP",
            "Raw": "Sem Camisinha",
            "Bottle of Vodka": "Garrafa de Vodka",
            "Chocolate Box": "Caixa de Chocolate",
            "Flowers": "Flores",
            "Perfume": "Perfume",
            "Necklace": "Colar",
            "Handbag": "Bolsa",
            "Ring": "Anel",
            "Designer Watch": "Relogio de Grife",
            "Jewelry Set": "Conjunto de Joias",
            "Vodka": "Vodka",
            # Drinks (0.9) — brand names differ per language; refs stay generic
            "Cools Light Beer": "Cerveja Brahva",
            "Xitos Vodka": "Borote de Sabor",
            "Running Douglas Whiskey": "Cachaça 69",
            "Alinmus Beer": "Cerveja Alinmus",
            "HunterMaster": "Mansão da Bomba Sabor Energético",
            "UnusualAlias Moonshine": "Cachaça UnusualAlias",
            "light buzz": "efeito leve",
            "strong buzz": "efeito forte",
            "heavy buzz": "efeito pesado",
            "Beer": "Cerveja",
            "Whiskey": "Whisky",
            # Preferences panel (0.9)
            "Favorite food": "Comida favorita",
            "Favorite drink": "Bebida favorita",
            "Preferred brand": "Marca preferida",
            "Favorite food discovered": "Comida favorita descoberta",
            "Favorite drink discovered": "Bebida favorita descoberta",
            "Favorite brand discovered": "Marca favorita descoberta",
            "Steak": "Bife",
            "Pasta": "Macarrão",
            "Chicken": "Frango",
            "Salad": "Salada",
            "Unknown": "Desconhecido",
            # ToD "right dose" minigame (0.9)
            "You": "Você",
            "Drink Level": "Nível de Bebida",
            "Heavy Drinker": "Bom de Copo",
            "Lightweight": "Fraca para Bebida",
            "Holds her liquor. Alcohol affects her far less, so she gets drunk slowly and rarely gets sick. During Truth or Dare you'll need to keep the drinks coming to loosen her up.": "Segura bem o álcool. A bebida afeta ela muito menos, então ela fica bêbada devagar e raramente passa mal. No Verdade ou Desafio você vai precisar manter as doses vindo pra soltar ela.",
            "Low tolerance. She gets drunk fast and gets sick easily, so a few drinks go a long way. Push her too hard and she'll be sick and done for the night.": "Pouca tolerância. Ela fica bêbada rápido e passa mal fácil, então poucas doses já bastam. Force demais e ela passa mal e encerra a noite.",
            "Polyamorous": "Poliamorosa",
            "Monogamous": "Monogâmica",
            "Open to sharing a partner. Much more willing to accept a harem.": "Aberta a compartilhar o parceiro. Muito mais disposta a aceitar um harém.",
            "Demands exclusivity. Extremely resistant to sharing.": "Exige exclusividade. Extremamente resistente a compartilhar.",
            "Open to sharing. She can accept a harem arrangement where the player dates multiple girls at once. Less jealous in multi-girl scenarios and threesomes.": "Aberta a dividir. Ela pode aceitar um arranjo de harém onde o jogador namora várias garotas ao mesmo tempo. Menos ciumenta em cenários com múltiplas garotas e trios.",
            "Wants exclusivity. She demands a committed relationship and reacts badly if she discovers the player is with other girls. Higher jealousy during threesomes and multi-girl situations.": "Quer exclusividade. Ela exige um relacionamento comprometido e reage mal se descobrir que o jogador está com outras garotas. Mais ciumenta durante trios e situações com múltiplas garotas.",
            "She's open to sharing her partner": "Ela é aberta a compartilhar o parceiro",
            "She demands exclusivity": "Ela exige exclusividade",
            # Pregnancy trait pair labels + descriptions
            "Breedable": "Fértil",
            "Infertile": "Infértil",
            "Pregnancy Fetish": "Fetiche por Gravidez",
            "Pregnancy Fear": "Medo de Gravidez",
            "Extremely fertile. 1.5x conception chance and wider fertile window.": "Extremamente fértil. 1.5x chance de concepção e janela fértil mais ampla.",
            "Cannot get pregnant. Zero conception chance.": "Não pode engravidar. Chance zero de concepção.",
            "Wants to be bred. Refuses the pill, craves creampies.": "Quer ser engravidada. Recusa a pílula, deseja creampies.",
            "Terrified of pregnancy. Always on the pill, never forgets.": "Apavorada com gravidez. Sempre toma a pílula, nunca esquece.",
            "She's incredibly fertile": "Ela é incrivelmente fértil",
            "She can't get pregnant": "Ela não pode engravidar",
            "She wants to be bred": "Ela quer ser engravidada",
            "She's terrified of getting pregnant": "Ela tem pavor de engravidar",
            "Ask her about sharing": "Perguntar sobre compartilhar",
            "Tell her it was a mistake": "Dizer que foi um erro",
            "Pharmacy": "Farmácia",
            "Birth Control Pills": "Pílulas Anticoncepcionais",
            "Sunflower Fertility Shield": "Escudo de Fertilidade de Girassol",
            "Morning After Pill": "Pílula do Dia Seguinte",
            "Fertility Vitamins": "Vitaminas de Fertilidade",
            "Tripod": "Tripe",
            "Tekmix Camera": "Camera Tekmix",
            "Drinks": "Bebidas",
            "Gifts": "Presentes",
            "Hangout Night": "Noite de Rolezinho",
            "already invited today": "já convidou hoje",
            "too late": "muito tarde",
            "need to buy a bottle": "precisa comprar uma garrafa",
            "What about just as friends?": "E se for so como amigos?",
            "Never mind": "Deixa pra la",
            "Condom (x6-pack)": "Camisinha (pacote x6)",
            "Black Bikini": "Biquíni Preto",
            "Green Bikini": "Biquíni Verde",
            "Pink Bikini": "Biquíni Rosa",
            "Blue Bikini": "Biquíni Azul",
            "Red Bikini": "Biquíni Vermelho",
            # Quit menu
            "What do you think about the game?": "O que você acha do jogo?",
            # Partner labels & pronouns
            "boyfriend": "namorado",
            "girlfriend": "namorada",
            "partner": "parceiro",
            "he": "ele",
            "she": "ela",
            "He": "Ele",
            "She": "Ela",
            "him": "ele",
            "her_obj": "ela",
            "his": "dele",
            "her_poss": "dela",
            "His": "Dele",
            "Her_poss": "Dela",
            "npc_friend_m": "Amigo",
            "npc_friend_f": "Amiga",
            "A girl": "Uma garota",
            "A guy": "Um cara",
            # Tutorial — Traits tab
            "Traits": "Características",
            "Each girl has personality traits that shape her behavior, dialogue, approval thresholds, and scene outcomes. Check the {b}Traits{/b} tab for a full glossary.": "Cada garota tem características de personalidade que moldam seu comportamento, diálogos, limites de aprovação e resultados das cenas. Veja a aba {b}Características{/b} para o glossário completo.",
            "Personality Traits (Opposing Pairs)": "Características de Personalidade (Pares Opostos)",
            "Loves being filmed. She may ask to be recorded and reacts positively to it. Cannot be blackmailed if she's single, since she doesn't care about leaked videos.": "Adora ser filmada. Pode pedir pra ser gravada e reage positivamente. Não pode ser chantageada se for solteira, já que não liga pra vídeos vazados.",
            "Hates cameras. Very resistant to being filmed. Much harder to get recording consent. If she catches you recording, the consequences are worse.": "Odeia câmeras. Muito resistente a ser filmada. Muito mais difícil conseguir consentimento pra gravar. Se ela te pegar gravando, as consequências são piores.",
            "Loves cum inside her and hates condoms. She may try to force a creampie during sex. Reacts very positively to raw sex and finishing inside.": "Adora sêmen dentro dela e odeia camisinhas. Pode tentar forçar um creampie durante o sexo. Reage muito positivamente a sexo sem camisinha e gozar dentro.",
            "Hates any contact with cum. Demands condoms every time. Reacts very negatively to creampies and removing condoms.": "Odeia qualquer contato com sêmen. Exige camisinha toda vez. Reage muito negativamente a creampies e remover camisinhas.",
            "Turned on by public exposure and risk. Easier to seduce in public locations. Approval gets a bonus in public areas.": "Excitada por exposição pública e risco. Mais fácil seduzir em locais públicos. Aprovação recebe bônus em áreas públicas.",
            "Terrified of being seen. Much harder to convince for anything sexual in public. Stronger negative reaction if caught.": "Apavorada de ser vista. Muito mais difícil convencer pra qualquer coisa sexual em público. Reação negativa mais forte se pega.",
            "Prefers rough, fast, intense sex. Higher pleasure from fast speeds. Dialogue and reactions reflect her preference for dominance.": "Prefere sexo bruto, rápido e intenso. Mais prazer com velocidades rápidas. Diálogos e reações refletem sua preferência por dominância.",
            "Prefers slow, intimate, gentle sex. Higher pleasure from slow speeds. Reacts negatively to overly rough or degrading actions.": "Prefere sexo lento, íntimo e gentil. Mais prazer com velocidades lentas. Reage negativamente a ações muito brutas ou degradantes.",
            "Strongly resists cheating on her partner. Much harder to corrupt. High approval thresholds for sexual acts while she has a boyfriend/girlfriend. Can evolve into Cheater through corruption over time.": "Resiste fortemente a trair o parceiro. Muito mais difícil de corromper. Limites de aprovação altos para atos sexuais enquanto tem namorado(a). Pode evoluir para Traidora através da corrupção com o tempo.",
            "Cheating is easy and even enjoyable for her. Lower approval thresholds for acts while she has a partner. Less guilt after cheating.": "Trair é fácil e até prazeroso pra ela. Limites de aprovação menores para atos enquanto tem parceiro. Menos culpa depois de trair.",
            "Loves anal sex. Gets more pleasure from it and may ask for it. Lower thresholds for anal acts.": "Adora sexo anal. Sente mais prazer e pode pedir. Limites menores para atos anais.",
            "Hates and fears anal. Focused on pain over pleasure. Very high thresholds and strong resistance to anal acts.": "Odeia e tem medo de anal. Focada na dor em vez do prazer. Limites muito altos e forte resistência a atos anais.",
            "Struggles financially. Gifts have a stronger effect on her. She's more open to financial persuasion after enough gifts, and her prices are lower.": "Tem dificuldades financeiras. Presentes têm efeito mais forte nela. Mais aberta a persuasão financeira depois de presentes suficientes, e os preços são menores.",
            "Wealthy background. Hard to impress with gifts. She's more resistant to financial persuasion, requires more gifts to unlock it, and her prices are higher.": "Família rica. Difícil de impressionar com presentes. Mais resistente a persuasão financeira, precisa de mais presentes pra desbloquear, e os preços são maiores.",
            "Completely inexperienced. Has never done anything sexual, not even a handjob. Forces Virgin trait. Her boyfriend (if any) has zero sexual history with her.": "Completamente inexperiente. Nunca fez nada sexual, nem uma punheta. Força a característica Virgem. O namorado dela (se tiver) tem zero histórico sexual com ela.",
            "Has not had penetrative sex yet. A special scene plays during her first time. Her reaction depends on your approach and her personality.": "Ainda não fez sexo penetrativo. Uma cena especial acontece na primeira vez dela. A reação depende da sua abordagem e personalidade dela.",
            "Has done everything before with someone else. Not a virgin and knows what she's doing. Cannot coexist with Virgin or Naive.": "Já fez de tudo antes com outra pessoa. Não é virgem e sabe o que está fazendo. Não pode coexistir com Virgem ou Inocente.",
            "Likes watching others. May react differently during scenes involving multiple people.": "Gosta de assistir os outros. Pode reagir diferente em cenas com múltiplas pessoas.",
            "Likes being watched. Gets aroused by the idea of someone seeing her.": "Gosta de ser observada. Fica excitada com a ideia de alguém vendo ela.",
            "Only attracted to women. Love does NOT help with sexual acts. Only Obedience and Inhibition count. She must progress through acts in order. Kissing is the LAST act unlocked, not the first. Her resistance decays with each act. Asking for sexual acts costs Love.": "Só atraída por mulheres. Amor NÃO ajuda com atos sexuais. Só Obediência e Inibição contam. Ela precisa progredir pelos atos em ordem. Beijo é o ÚLTIMO ato desbloqueado, não o primeiro. A resistência dela diminui com cada ato. Pedir atos sexuais custa Amor.",
            "Attracted to both men and women. Can have a boyfriend or a girlfriend. Uses normal hetero mechanics for everything. No special thresholds or restrictions.": "Atraída por homens e mulheres. Pode ter namorado ou namorada. Usa mecânicas hetero normais para tudo. Sem limites ou restrições especiais.",
            "She already has a boyfriend at game start. You need to build Temptation to get past her loyalty. Her boyfriend may catch you, confront you, or react to rumors.": "Ela já tem namorado no início do jogo. Você precisa construir Tentação pra passar pela lealdade dela. O namorado pode te pegar, confrontar, ou reagir a rumores.",
            "She already has a girlfriend at game start. Works similarly to having a boyfriend but with a female NPC partner.": "Ela já tem namorada no início do jogo. Funciona similar a ter namorado, mas com uma parceira NPC feminina.",
            "Special Traits": "Características Especiais",
            # NTR Boundary level labels
            "Non-penetration only": "Apenas sem penetracao",
            "Condom-protected sex": "Sexo com camisinha",
            "Raw sex, no creampie or anal": "Sexo sem camisinha, sem gozar dentro ou anal",
            "No limits": "Sem limites",
            # Phone group create NPC label
            "(partner)": "(parceiro)",
            "%s's BF": "namorado da %s",
            "%s's GF": "namorada da %s",
            # Spectrum labels
            "Straight": "Hétero", "Party Bi": "Bi de Festa", "Curious": "Curiosa", "Bisexual": "Bissexual", "Lesbian": "Lésbica",
            "Sexuality": "Sexualidade",
            "Story": "História",
            # Stat popups (girl-to-girl + NPC partner)
            "Friendship": "Amizade",
            "NPC Love": "Amor do NPC",
            "Suspicion": "Suspeita",
            # Phone Fertility app (screen_fertility.rpy) + discovery banners
            "Birth control status discovered": "Status de anticoncepcional descoberto",
            "Fertility cycle discovered": "Ciclo fértil descoberto",
            "Safe": "Seguro", "Low risk": "Risco baixo", "Fertile": "Fértil", "Peak": "Pico",
            "Away": "Ausente", "Pregnant": "Grávida", "Postpartum": "Pós-parto",
            "Recovering after birth. Not fertile right now.": "Se recuperando do parto. Não está fértil no momento.",
            "She can't get pregnant.": "Ela não pode engravidar.",
            "Early": "Início", "Showing": "Aparecendo", "Full belly": "Barriga cheia",
            "%d day": "%d dia", "%d days": "%d dias",
            "Away giving birth. Back in %s.": "Fora para dar à luz. Volta em %s.",
            "Day %d": "Dia %d",
            "Due in %s": "Nasce em %s",
            "Day %d of 28": "Dia %d de 28",
            "Fertile window ends in %s": "Janela fértil termina em %s",
            "Fertile window in %s": "Janela fértil em %s",
            "Birth control: ???": "Anticoncepcional: ???",
            "Not on the pill": "Não toma pílula",
            "Placebo, 0% (she thinks it's real)": "Placebo, 0% (ela acha que é real)",
            "On the pill, %d%% effective": "Toma pílula, %d%% de eficácia",
            "missed: %s": "esqueceu: %s",
            "Fertility vitamins": "Vitaminas de fertilidade",
            "Not active": "Inativa",
            "Pills": "Pílulas", "Placebo": "Placebo", "Plan B": "Plano B",
            "Child support: $%d per week": "Pensão: $%d por semana",
            "Extra breedable: wider fertile window": "Super fértil: janela fértil maior",
            "Cycle unknown. Pay attention to her moods when you chat.": "Ciclo desconhecido. Repare no humor dela quando conversarem.",
            "Unknown. Listen for hints when you chat with her.": "Desconhecido. Fique atento às pistas quando conversar com ela.",
            "CYCLE": "CICLO",
            "STATUS": "STATUS",
            "BIRTH CONTROL": "ANTICONCEPCIONAL",
            "PLAN B": "PLANO B",
            "RISK TODAY": "RISCO HOJE",
            "YOUR SUPPLIES": "SEUS ITENS",
            "CHILDREN": "FILHOS",
            "Effectiveness": "Eficácia",
            "Used %d of %d": "Usou %d de %d",
            "She won't take any more for now.": "Ela não vai tomar mais nenhuma por enquanto.",
            "Next dose frees up in %s": "Próxima dose liberada em %s",
            "??? Needs her cycle and her birth control status.": "??? Precisa do ciclo e do status de anticoncepcional dela.",
            "Cycle, birth control and risk": "Ciclo, anticoncepcional e risco",
            "Check Fertility in her contact": "Veja Fertilidade no contato dela",
            "She started taking the pill": "Ela começou a tomar a pílula",
            "She stopped taking the pill": "Ela parou de tomar a pílula",
            "Inside": "Dentro", "Pull out": "Tirar antes",
            "Children: %d": "Filhos: %d",
            "Chit chat with her and listen to what she says after sex. Asking her directly is risky: she may refuse or take offense.": "Jogue conversa fora com ela e ouça o que ela diz depois do sexo. Perguntar direto é arriscado: ela pode recusar ou se ofender.",
            # Fertility vitamins (v0.12.1)
            "Includes your fertility vitamins (x%s).": "Inclui suas vitaminas de fertilidade (x%s).",
            "Active x%s, %s left": "Ativa x%s, faltam %s",
            # Player FIRSTS / discovery banner
            "You got her pregnant": "Você a engravidou",
            # Children age labels
            "Newborn": "Recém-nascido", "Infant": "Nenê", "Baby": "Bebê", "Toddler": "Criancinha",
            "Raised by %s": "Criado por %s",
            "Next payment in %s": "Próximo pagamento em %s",
            # C. Johnson intel
            "A baby costs money: work": "Bebê custa dinheiro: trabalhe",
            "Many babies, many bills: work": "Muitos bebês, muitas contas: trabalhe",
            # Gift discovery banner & preferences labels
            "Her taste in gifts discovered": "Gosto dela para presentes descoberto",
            "Loves": "Adora", "Not a fan": "Não curte",
            # Trait Picker tabs & section headers (v0.12.1)
            "Personality": "Personalidade", "Relationships": "Relacionamentos",
            "Experience": "Experiência", "Lifestyle": "Estilo de Vida",
            "Hobbies": "Hobbies", "Kinks": "Fetiches",
            "Orientation": "Orientação", "Partner": "Parceiro",
            # Fertility IUD state
            "IUD": "DIU",
            "IUD active after delivery. Protected for now.": "DIU ativo após o parto. Protegida por enquanto.",
            # BigFans ATM tag
            "ATM": "ATM",
            # Status screen trait hints (v0.12.1)
            "Nerd": "Nerd", "Gym Rat": "Rato de Academia",
            # Trait picker: the Control pair, Married, the short descriptions (2026-10-03)
            "Control": "Controle", "Femdom": "Femdom", "Submissive": "Submissa", "Married": "Casada", "Hates Cum": "Odeia Sêmen",
            "Wants to be in charge. Resists acts that put you in control.": "Quer estar no comando. Resiste aos atos que deixam você no controle.",
            "Likes being told what to do. Gives in to your control easily.": "Gosta que digam o que fazer. Cede ao seu controle com facilidade.",
            "Holds her liquor. Alcohol affects her far less.": "Segura bem o álcool. A bebida afeta ela muito menos.",
            "Low tolerance. Gets drunk fast and sick easily.": "Pouca tolerância. Fica bêbada rápido e passa mal fácil.",
            "Academically obsessed. Earns double study points and reacts strongly to class disruptions.": "Obcecada pelos estudos. Ganha o dobro de pontos de estudo e reage forte quando atrapalham a aula.",
            "Lives at the gym. Respects strength, despises weakness.": "Vive na academia. Respeita a força, despreza a fraqueza.",
            "She's married.": "Ela é casada.",
            "Loves anal": "Adora anal", "Hates anal": "Odeia anal",
            "Can hold her liquor": "Aguenta bebida", "Lightweight drinker": "Fraca pra bebida",
            "Struggling financially": "Dificuldades financeiras", "Wealthy": "Rica",
            "Breeding kink": "Fetiche por gravidez",
            "Wants to be a mom": "Quer ser mãe",
            "Terrified of pregnancy": "Pavor de engravidar",
            # CJ intel labels (v0.12.1)
            "A baby costs money: work": "Bebê custa dinheiro: trabalhe",
            "Many babies, many bills: work": "Muitos bebês, muitas contas: trabalhe",
            # CJ van items in the phone inventory (v0.12.1)
            "Girls Tracker": "Rastreador de Garotas", "Instant Pregnancy Test": "Teste de Gravidez Instantâneo",
            # BigFans video location (screen_status)
            "Dressing Room": "Provador",
            # Family contact names
            "Dad": "Pai",
        },
        "es": {
            # TIME / WEEKDAY
            "Morning": "Mañana", "Midday": "Mediodía", "Evening": "Atardecer", "Night": "Noche",
            "Sunday": "Domingo", "Monday": "Lunes", "Tuesday": "Martes",
            "Wednesday": "Miércoles", "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado",
            "[weekday_name!u], DAY [Day]": "[weekday_name!u], DÍA [Day]",
            # Trait categories
            "Camera": "Cámara", "Cum": "Semen", "Public": "Público",
            "Sex Style": "Estilo Sexual", "Loyalty": "Lealtad", "Anal": "Anal", "Economy": "Economía", "Sharing": "Compartir", "Fertility": "Fertilidad", "Pregnancy": "Embarazo",
            # Trait pair labels
            "Camera Lover": "Ama la Cámara", "Camera Hater": "Odia la Cámara",
            "Cum Lover": "Ama el Semen", "Cum Hater": "Odia el Semen",
            "Public Fetish": "Fetiche Público", "Public Shy": "Tímida en Público",
            "Hardcore": "Hardcore", "Gentle": "Gentil",
            "Loyal": "Leal", "Cheater": "Infiel",
            "Anal Lover": "Ama el Anal", "Anal Hater": "Odia el Anal",
            "Poor": "Pobre", "Rich": "Rica",
            # Trait pair descriptions
            "Loves being filmed. May ask to be recorded.": "Le encanta que la graben. Puede pedir que la filmen.",
            "Hates cameras. Very resistant to filming.": "Odia las cámaras. Muy resistente a ser filmada.",
            "Loves cum inside her. Hates condoms.": "Le encanta el semen adentro. Odia los condones.",
            "Hates cum contact. Demands condoms.": "Odia el contacto con semen. Exige condones.",
            "Turned on by public exposure and risk.": "Se excita con la exposición pública y el riesgo.",
            "Terrified of public exposure.": "Le aterroriza la exposición pública.",
            "Prefers rough, fast, intense sex.": "Prefiere sexo rudo, rápido e intenso.",
            "Prefers slow, intimate, gentle sex.": "Prefiere sexo lento, íntimo y gentil.",
            "Strongly resists cheating. Hard to corrupt.": "Resiste fuertemente la infidelidad. Difícil de corromper.",
            "Cheating is easy and enjoyable for her.": "Ser infiel es fácil y placentero para ella.",
            "Loves anal. Gets more pleasure, may ask for it.": "Ama el anal. Siente más placer, puede pedirlo.",
            "Hates/fears anal. Pain-focused, very resistant.": "Odia/teme el anal. Enfocada en el dolor, muy resistente.",
            "Struggles financially. Gifts mean more to her.": "Dificultades financieras. Los regalos significan más.",
            "Wealthy background. Hard to impress with gifts.": "Familia rica. Difícil de impresionar con regalos.",
            # System trait labels
            "Naive": "Inocente", "Experienced": "Experimentada", "Voyeur": "Voyeur",
            "Exhibitionist": "Exhibicionista", "Has a Boyfriend": "Tiene Novio",
            "Has a Girlfriend": "Tiene Novia", "Lesbian": "Lesbiana", "Bisexual": "Bisexual",
            # System trait descriptions
            "Has never done anything sexual. No history at all. Forces Virgin.": "Nunca ha hecho nada sexual. Sin historial alguno. Fuerza Virgen.",
            "Has not had sex yet.": "Aún no ha tenido sexo.",
            "Has done everything before with someone else. Not a virgin, knows what she's doing.": "Ya ha hecho de todo con otra persona. No es virgen, sabe lo que hace.",
            "Likes watching others.": "Le gusta mirar a otros.",
            "Likes being watched.": "Le gusta que la miren.",
            "She already has an NPC boyfriend at game start. The boyfriend will be present in the game.": "Ya tiene novio al inicio del juego. El novio estará presente en el juego.",
            "She already has an NPC girlfriend at game start. The girlfriend will be present in the game.": "Ya tiene novia al inicio del juego. La novia estará presente en el juego.",
            "Only attracted to women. Requires dominance or leverage for sexual acts.": "Solo atraída por mujeres. Requiere dominación o chantaje para actos sexuales.",
            "Attracted to both men and women. Can have a boyfriend or girlfriend. Uses normal mechanics.": "Atraída por hombres y mujeres. Puede tener novio o novia. Usa mecánicas normales.",
            # Trait verbal
            "She loves being on camera": "Le encanta estar frente a la cámara",
            "She hates cameras": "Odia las cámaras",
            "She loves cum": "Le encanta el semen",
            "She hates cum": "Odia el semen",
            "She likes doing it in public": "Le gusta hacerlo en público",
            "She's terrified of public exposure": "Le aterroriza la exposición pública",
            "She likes it rough": "Le gusta rudo",
            "She likes it gentle": "Le gusta gentil",
            "She's very loyal": "Es muy leal",
            "She's open to cheating": "Está abierta a ser infiel",
            "She's completely inexperienced": "Es completamente inexperta",
            "She's a virgin": "Es virgen",
            "She likes watching others": "Le gusta mirar a otros",
            "She likes being watched": "Le gusta que la miren",
            "She's open to sharing": "Está abierta a compartir",
            "She already has a boyfriend": "Ya tiene novio",
            "She already has a girlfriend": "Ya tiene novia",
            "She has done everything with her partner": "Ya ha hecho de todo con su pareja",
            "She loves anal": "Ama el anal",
            "She hates anal": "Odia el anal",
            "She's only attracted to women": "Solo se siente atraída por mujeres",
            "She's attracted to both men and women": "Se siente atraída tanto por hombres como por mujeres",
            "She struggles financially": "Tiene dificultades económicas",
            "She comes from a wealthy background": "Viene de una familia rica",
            "She can hold her liquor": "Aguanta bien el alcohol",
            "She can't handle her drinks": "No aguanta la bebida",
            "She's a total bookworm": "Es una nerd total",
            "She lives at the gym": "Vive en el gimnasio",
            "Extra breedable": "Super fértil",
            "Infertile": "Infértil",
            "She has a pregnancy fetish": "Tiene fetiche por el embarazo",
            # Screen UI
            "(not available)": "(no disponible)",
            "(opposite selected)": "(opuesto seleccionado)",
            "(locked: lesbian)": "(bloqueado: lesbiana)",
            "(locked: pregnancy fetish)": "(bloqueado: fetiche de embarazo)",
            "(locked: has girlfriend)": "(bloqueado: tiene novia)",
            "(locked: naive)": "(bloqueado: inocente)",
            "(conflict)": "(conflicto)",
            "Personality Traits": "Rasgos de Personalidad",
            "Done": "Listo",
            "Randomize the rest (fill to 3)": "Aleatorizar el resto (completar a 3)",
            "TRAITS": "RASGOS",
            # Discovery banners
            "She is dating someone": "Está saliendo con alguien",
            "She has no boyfriend": "No tiene novio",
            "Study habits discovered": "Hábitos de estudio descubiertos",
            "Favorite act discovered": "Acto favorito descubierto",
            "She accepted your petname": "Aceptó tu apodo",
            "She has a name for you": "Tiene un nombre para ti",
            "Her first kiss": "Su primer beso",
            "You're her first handjob": "Eres su primera paja",
            "You're her first titjob": "Eres su primera cubana",
            "You're her first blowjob": "Eres su primera mamada",
            "She's never done this for anyone": "Nunca ha hecho esto por nadie",
            "You took her virginity": "Le quitaste la virginidad",
            "You're her first anal": "Eres su primer anal",
            "First time raw": "Primera vez sin condón",
            "First creampie": "Primer creampie",
            "She struggles with money": "Tiene dificultades económicas",
            "She comes from money": "Viene de familia rica",
            "She's not a virgin": "No es virgen",
            "BF never did: %s": "El novio nunca hizo: %s",
            "BF has done: %s": "El novio ya hizo: %s",
            "BF": "Novio",
            "GF": "Novia",
            "never did": "nunca hizo",
            "has done": "ya hizo",
            # Player discoveries
            "Your first kiss": "Tu primer beso",
            "Your first handjob": "Tu primera paja",
            "Your first titjob": "Tu primera cubana",
            "Your first blowjob": "Tu primera mamada",
            "Lost your virginity": "Perdiste la virginidad",
            "Your first anal": "Tu primer anal",
            "Your first creampie": "Tu primer creampie",
            "First time going raw": "Primera vez sin condón",
            "You took someone's virginity": "Le quitaste la virginidad a alguien",
            "You got your first girlfriend": "Conseguiste tu primera novia",
            "Peak physical condition": "Condición física máxima",
            "New intel acquired": "Nueva información adquirida",
            "New Trait Discovered": "Nuevo Rasgo Descubierto",
            # C. Johnson intel labels (Status screen)
            "C. JOHNSON'S INTEL": "INTEL DE C. JOHNSON",
            "People are gossiping": "La gente está chismeando",
            "Your breakup is known": "Saben de tu ruptura",
            "Professors noticed you": "Los profesores te notaron",
            "Girls find you handsome": "Las chicas te encuentran guapo",
            "You... You are ugly :c": "Tú... Eres feo :c",
            "%s is changing": "%s está cambiando",
            "%s is hostile to you": "%s es hostil contigo",
            "%s is not jealous": "%s no es celos(a)",
            "%s is jealous": "%s tiene celos",
            "Hotdogs recover energy": "Los perros calientes recuperan energía",
            "Give gifts to pay for sex": "Dale regalos para pagar por sexo",
            "No intel yet": "Sin información aún",
            # Status screen — relationship & NPC labels
            "Your Girlfriend": "Tu Novia",
            "Stranger": "Desconocida",
            "Acquaintance": "Conocida",
            "Friend": "Amiga",
            "Close Friend": "Amiga Cercana",
            "Intimate": "Íntima",
            "Ex": "Ex",
            "Friendly": "Amigable",
            "Neutral": "Neutral",
            "Hostile": "Hostil",
            "NTR": "NTR",
            "Proud": "Orgulloso",
            "PARTNER TRAITS": "RASGOS DEL COMPAÑERO",
            "Disposition": "Disposición",
            "Enjoys watching and sharing. Never breaks up over cheating.": "Le gusta mirar y compartir. Nunca termina por infidelidad.",
            "Jealous and possessive. Will break up quickly if caught.": "Celoso y posesivo. Termina rápido si lo descubre.",
            "Slightly jealous. May break up eventually.": "Ligeramente celoso. Puede terminar eventualmente.",
            "Preferences": "Preferencias",
            "Wants to watch in person.": "Quiere mirar en persona.",
            "Wants videos of her.": "Quiere videos de ella.",
            "NTR Limits": "Límites NTR",
            "What is the initial boundary the partner is comfortable with? You can push these limits during gameplay and unlock new scenarios.": "Cuál es el límite inicial con el que el compañero se siente cómodo? Puedes evolucionar estos límites durante el juego y desbloquear nuevos escenarios.",
            "Randomize All": "Aleatorizar Todo",
            "Lesbian partners do not have boundary levels.": "Las parejas lesbianas no tienen niveles de límite.",
            "In love": "Enamorado",
            "Moderate": "Moderado",
            "Low": "Bajo",
            "Very suspicious": "Muy sospechoso",
            "Suspicious": "Sospechoso",
            "Uneasy": "Inquieto",
            "Unaware": "Sin sospechas",
            # Status screen — study levels
            "Very prepared": "Muy preparado",
            "Well studied": "Bien estudiado",
            "Somewhat prepared": "Algo preparado",
            "Barely studied": "Apenas estudió",
            "Hasn't studied at all": "No ha estudiado nada",
            # Status screen — friendship labels
            "Best Friends": "Mejores Amigas",
            "Friends": "Amigas",
            "Acquaintances": "Conocidas",
            # Status screen — trait hints
            "Virgin": "Virgen",
            "Loves being filmed": "Le encanta ser filmada",
            "Hates cameras": "Odia las cámaras",
            "Loves cum": "Le encanta el semen",
            "Hates cum": "Odia el semen",
            "Turned on by public risk": "Excitada por el riesgo público",
            "Terrified of exposure": "Aterrada de ser expuesta",
            "Likes it rough": "Le gusta el sexo rudo",
            "Likes it gentle": "Le gusta el sexo suave",
            "Very loyal": "Muy fiel",
            "Prone to cheating": "Tendencia a engañar",
            "Likes watching": "Le gusta observar",
            "Likes being watched": "Le gusta ser observada",
            "Open to sharing": "Abierta a compartir",
            # Status screen — player study (shorter variant)
            "Hasn't studied": "No ha estudiado",
            # Status screen — firsts act labels
            "Kiss": "Beso",
            "Handjob": "Paja",
            "Titjob": "Cubana",
            "Footjob": "Footjob",
            "Rimjob": "Beso negro",
            "Father's Apartment (Not with company)": "Departamento de Papá (No con compañía)",
            "Talk about her (Already today)": "Hablar de ella (Ya hoy)",
            "Give him a drink (No drinks)": "Darle una bebida (Sin bebidas)",
            "Blowjob": "Mamada",
            "Sex": "Sexo",
            # Status screen — BigFans labels & tags
            "Any video": "Cualquier video",
            "cheating": "infidelidad",
            "public": "público",
            "cuckold": "cornudo",
            "threesome": "trío",
            "face visible": "rostro visible",
            "face hidden": "rostro oculto",
            "secret": "secreto",
            "HD": "HD",
            "%s stopped the recording.": "%s dejó de grabar.",
            "Masturbation": "Masturbación",
            "Cowgirl": "Cowgirl",
            "Reverse Cowgirl": "Reverse Cowgirl",
            "Doggy Style": "De Perrito",
            "Full Nelson": "Full Nelson",
            "Full Nelson Anal": "Full Nelson Anal",
            "Laying Down": "Acostada", "Laying Down Anal": "Anal Acostada",
            "Reverse Cowgirl Anal": "Reverse Cowgirl Anal",
            "Creampie": "Creampie",
            "LOSING VIRGINITY": "PERDIENDO LA VIRGINIDAD",
            "%dd left": "%dd restante",
            "Expires today!": "¡Expira hoy!",
            # Status screen — video locations
            "%s's Room": "Cuarto de %s",
            "Campus": "Campus",
            "Pool": "Piscina",
            "Showers": "Duchas",
            "Apartment": "Departamento",
            "Apartment Bedroom": "Recámara del Departamento",
            "Apartment Bathroom": "Baño del Departamento",
            "Gym": "Gimnasio",
            "Classroom": "Salón de Clases",
            "Mall": "Centro Comercial",
            "Hall": "Pasillo",
            "Street": "Calle",
            "Party": "Fiesta",
            "Restaurant Restroom": "Baño del Restaurante",
            "Gwen's Room": "Cuarto de Gwen",
            "Rogue's Room": "Cuarto de Rogue",
            "Negasonic's Room": "Cuarto de Negasonic",
            # Navigation — disabled menu items
            "Class (Closing soon)": "Clase (Cierra pronto)",
            "Class (Closed)": "Clase (Cerrada)",
            "Gym (Closing soon)": "Gimnasio (Cierra pronto)",
            "Gym (Closed)": "Gimnasio (Cerrado)",
            "Mall (Closing soon)": "Centro Comercial (Cierra pronto)",
            "Mall (Closed)": "Centro Comercial (Cerrado)",
            "Study (Too late)": "Estudiar (Muy tarde)",
            "Wait (It's night)": "Esperar (Es de noche)",
            # Near/Far roster
            "Call someone over...": "Llamar a alguien...",
            "Who do you want to call over?": "¿A quién quieres llamar?",
            "Who should leave?": "¿Quién debería irse?",
            "%s walks over.": "%s se acerca.",
            "You hear %s arrive nearby.": "Escuchas a %s llegar cerca.",
            "After a while, %s arrives.": "Después de un rato, %s llega.",
            # Petname announcements
            "Hey... I've been thinking. Can I call you %s from now on?": "Oye... estuve pensando. ¿Puedo llamarte %s de ahora en adelante?",
            "You feel more like a %s to me now... is that okay?": "Me pareces más un %s ahora... ¿está bien?",
            "I want to start calling you %s. What do you think?": "Quiero empezar a llamarte %s. ¿Qué opinas?",
            # Petnames (display)
            "Princess": "Princesa",
            "Babe": "Nena",
            "Honey": "Cariño",
            "Love": "Amor",
            "Angel": "Ángel",
            "Slut": "Puta",
            "Whore": "Zorra",
            "Cumdumpster": "Tragaleche",
            "Cutie": "Lindito",
            "Pumpkin": "Calabacita",
            "Sugar": "Dulzura",
            "Sweetheart": "Cielito",
            "Tiger": "Tigre",
            "Daddy": "Papi",
            "Master": "Amo",
            "Sir": "Señor",
            "Queen": "Reina",
            "Goddess": "Diosa",
            "Mistress": "Ama",
            "Pet": "Mascota",
            "Toy": "Juguete",
            "Good boy": "Buen chico",
            "Stepmom": "Madrastra",
            "Boy": "Chico",
            # Inventory
            "Condoms": "Condones",
            "Japanese Condoms": "Condones Japoneses",
            "Condom": "Condón",
            "JP Condom": "Condón JP",
            "Raw": "Sin Condón",
            "Bottle of Vodka": "Botella de Vodka",
            "Chocolate Box": "Caja de Chocolate",
            "Flowers": "Flores",
            "Perfume": "Perfume",
            "Necklace": "Collar",
            "Handbag": "Bolso",
            "Ring": "Anillo",
            "Designer Watch": "Reloj de Diseñador",
            "Jewelry Set": "Conjunto de Joyas",
            "Vodka": "Vodka",
            # Drinks (0.9) — brand names differ per language; refs stay generic
            "Cools Light Beer": "Cerveza Lorona",
            "Xitos Vodka": "Ron Viejo Cacardi",
            "Running Douglas Whiskey": "Pisco PerChi",
            "Alinmus Beer": "Cerveza Alinmus",
            "HunterMaster": "Vino Casillero del Satanás",
            "UnusualAlias Moonshine": "Tequila UnusualAlias",
            "light buzz": "efecto leve",
            "strong buzz": "efecto fuerte",
            "heavy buzz": "efecto pesado",
            "Beer": "Cerveza",
            "Whiskey": "Whisky",
            # Preferences panel (0.9)
            "Favorite food": "Comida favorita",
            "Favorite drink": "Bebida favorita",
            "Preferred brand": "Marca preferida",
            "Favorite food discovered": "Comida favorita descubierta",
            "Favorite drink discovered": "Bebida favorita descubierta",
            "Favorite brand discovered": "Marca favorita descubierta",
            "Steak": "Bistec",
            "Pasta": "Pasta",
            "Chicken": "Pollo",
            "Salad": "Ensalada",
            "Unknown": "Desconocido",
            # ToD "right dose" minigame (0.9)
            "You": "Tú",
            "Drink Level": "Nivel de Bebida",
            "Heavy Drinker": "Aguanta Bien",
            "Lightweight": "Poca Tolerancia",
            "Holds her liquor. Alcohol affects her far less, so she gets drunk slowly and rarely gets sick. During Truth or Dare you'll need to keep the drinks coming to loosen her up.": "Aguanta bien el alcohol. La bebida la afecta mucho menos, así que se emborracha lento y rara vez se marea. En Verdad o Reto tendrás que seguir sirviéndole para soltarla.",
            "Low tolerance. She gets drunk fast and gets sick easily, so a few drinks go a long way. Push her too hard and she'll be sick and done for the night.": "Poca tolerancia. Se emborracha rápido y se marea con facilidad, así que unos pocos tragos hacen mucho. Si la presionas demasiado, se pondrá mal y se acabó la noche para ella.",
            "Polyamorous": "Poliamorosa",
            "Monogamous": "Monógama",
            "Open to sharing a partner. Much more willing to accept a harem.": "Abierta a compartir pareja. Mucho más dispuesta a aceptar un harén.",
            "Demands exclusivity. Extremely resistant to sharing.": "Exige exclusividad. Extremadamente resistente a compartir.",
            "Open to sharing. She can accept a harem arrangement where the player dates multiple girls at once. Less jealous in multi-girl scenarios and threesomes.": "Abierta a compartir. Puede aceptar un arreglo de harém donde el jugador sale con varias chicas a la vez. Menos celosa en escenarios con múltiples chicas y tríos.",
            "Wants exclusivity. She demands a committed relationship and reacts badly if she discovers the player is with other girls. Higher jealousy during threesomes and multi-girl situations.": "Quiere exclusividad. Exige una relación comprometida y reacciona mal si descubre que el jugador está con otras chicas. Más celosa durante tríos y situaciones con múltiples chicas.",
            "She's open to sharing her partner": "Ella está abierta a compartir su pareja",
            "She demands exclusivity": "Ella exige exclusividad",
            # Pregnancy trait pair labels + descriptions
            "Breedable": "Fértil",
            "Infertile": "Infértil",
            "Pregnancy Fetish": "Fetiche de Embarazo",
            "Pregnancy Fear": "Miedo al Embarazo",
            "Extremely fertile. 1.5x conception chance and wider fertile window.": "Extremadamente fértil. 1.5x probabilidad de concepción y ventana fértil más amplia.",
            "Cannot get pregnant. Zero conception chance.": "No puede quedar embarazada. Probabilidad cero de concepción.",
            "Wants to be bred. Refuses the pill, craves creampies.": "Quiere ser embarazada. Rechaza la pastilla, desea creampies.",
            "Terrified of pregnancy. Always on the pill, never forgets.": "Aterrorizada por el embarazo. Siempre toma la pastilla, nunca olvida.",
            "She's incredibly fertile": "Ella es increíblemente fértil",
            "She can't get pregnant": "Ella no puede quedar embarazada",
            "She wants to be bred": "Ella quiere ser embarazada",
            "She's terrified of getting pregnant": "Ella está aterrorizada de quedar embarazada",
            "Ask her about sharing": "Preguntarle sobre compartir",
            "Tell her it was a mistake": "Decirle que fue un error",
            "Pharmacy": "Farmacia",
            "Birth Control Pills": "Pastillas Anticonceptivas",
            "Sunflower Fertility Shield": "Escudo de Fertilidad de Girasol",
            "Morning After Pill": "Pastilla del Día Después",
            "Fertility Vitamins": "Vitaminas de Fertilidad",
            "Tripod": "Tripode",
            "Tekmix Camera": "Camara Tekmix",
            "Drinks": "Bebidas",
            "Gifts": "Regalos",
            "Hangout Night": "Noche de Fiesta",
            "already invited today": "ya invitaste hoy",
            "too late": "muy tarde",
            "need to buy a bottle": "necesitas comprar una botella",
            "What about just as friends?": "¿Y si vamos solo como amigos?",
            "Never mind": "Olvídalo",
            "Condom (x6-pack)": "Condón (paquete x6)",
            "Black Bikini": "Bikini Negro",
            "Green Bikini": "Bikini Verde",
            "Pink Bikini": "Bikini Rosa",
            "Blue Bikini": "Bikini Azul",
            "Red Bikini": "Bikini Rojo",
            # Quit menu
            "What do you think about the game?": "¿Qué te pareció el juego?",
            # Partner labels & pronouns
            "boyfriend": "novio",
            "girlfriend": "novia",
            "partner": "pareja",
            "he": "él",
            "she": "ella",
            "He": "Él",
            "She": "Ella",
            "him": "él",
            "her_obj": "ella",
            "his": "su",
            "her_poss": "su",
            "His": "Su",
            "Her_poss": "Su",
            "npc_friend_m": "Amigo",
            "npc_friend_f": "Amiga",
            "A girl": "Una chica",
            "A guy": "Un tipo",
            # Tutorial — Traits tab
            "Traits": "Rasgos",
            "Each girl has personality traits that shape her behavior, dialogue, approval thresholds, and scene outcomes. Check the {b}Traits{/b} tab for a full glossary.": "Cada chica tiene rasgos de personalidad que moldean su comportamiento, diálogos, umbrales de aprobación y resultados de escenas. Consulta la pestaña {b}Rasgos{/b} para el glosario completo.",
            "Personality Traits (Opposing Pairs)": "Rasgos de Personalidad (Pares Opuestos)",
            "Loves being filmed. She may ask to be recorded and reacts positively to it. Cannot be blackmailed if she's single, since she doesn't care about leaked videos.": "Le encanta ser filmada. Puede pedir que la graben y reacciona positivamente. No puede ser chantajeada si es soltera, ya que no le importan los videos filtrados.",
            "Hates cameras. Very resistant to being filmed. Much harder to get recording consent. If she catches you recording, the consequences are worse.": "Odia las cámaras. Muy resistente a ser filmada. Mucho más difícil obtener consentimiento para grabar. Si te atrapa grabando, las consecuencias son peores.",
            "Loves cum inside her and hates condoms. She may try to force a creampie during sex. Reacts very positively to raw sex and finishing inside.": "Le encanta el semen adentro y odia los condones. Puede intentar forzar un creampie durante el sexo. Reacciona muy positivamente al sexo sin condón y acabar adentro.",
            "Hates any contact with cum. Demands condoms every time. Reacts very negatively to creampies and removing condoms.": "Odia cualquier contacto con semen. Exige condones siempre. Reacciona muy negativamente a creampies y quitar condones.",
            "Turned on by public exposure and risk. Easier to seduce in public locations. Approval gets a bonus in public areas.": "Se excita con la exposición pública y el riesgo. Más fácil seducir en lugares públicos. La aprobación recibe bonificación en áreas públicas.",
            "Terrified of being seen. Much harder to convince for anything sexual in public. Stronger negative reaction if caught.": "Aterrorizada de ser vista. Mucho más difícil convencer para algo sexual en público. Reacción negativa más fuerte si la atrapan.",
            "Prefers rough, fast, intense sex. Higher pleasure from fast speeds. Dialogue and reactions reflect her preference for dominance.": "Prefiere sexo rudo, rápido e intenso. Más placer con velocidades rápidas. Los diálogos y reacciones reflejan su preferencia por la dominación.",
            "Prefers slow, intimate, gentle sex. Higher pleasure from slow speeds. Reacts negatively to overly rough or degrading actions.": "Prefiere sexo lento, íntimo y gentil. Más placer con velocidades lentas. Reacciona negativamente a acciones demasiado rudas o degradantes.",
            "Strongly resists cheating on her partner. Much harder to corrupt. High approval thresholds for sexual acts while she has a boyfriend/girlfriend. Can evolve into Cheater through corruption over time.": "Resiste fuertemente engañar a su pareja. Mucho más difícil de corromper. Umbrales de aprobación altos para actos sexuales mientras tiene novio/novia. Puede evolucionar a Infiel a través de la corrupción con el tiempo.",
            "Cheating is easy and even enjoyable for her. Lower approval thresholds for acts while she has a partner. Less guilt after cheating.": "Engañar es fácil y hasta placentero para ella. Umbrales de aprobación menores para actos mientras tiene pareja. Menos culpa después de engañar.",
            "Loves anal sex. Gets more pleasure from it and may ask for it. Lower thresholds for anal acts.": "Ama el sexo anal. Siente más placer y puede pedirlo. Umbrales menores para actos anales.",
            "Hates and fears anal. Focused on pain over pleasure. Very high thresholds and strong resistance to anal acts.": "Odia y teme el anal. Enfocada en el dolor sobre el placer. Umbrales muy altos y fuerte resistencia a actos anales.",
            "Struggles financially. Gifts have a stronger effect on her. She's more open to financial persuasion after enough gifts, and her prices are lower.": "Tiene dificultades económicas. Los regalos tienen un efecto más fuerte en ella. Más abierta a persuasión financiera después de suficientes regalos, y sus precios son menores.",
            "Wealthy background. Hard to impress with gifts. She's more resistant to financial persuasion, requires more gifts to unlock it, and her prices are higher.": "Familia rica. Difícil de impresionar con regalos. Más resistente a persuasión financiera, requiere más regalos para desbloquearla, y sus precios son mayores.",
            "Completely inexperienced. Has never done anything sexual, not even a handjob. Forces Virgin trait. Her boyfriend (if any) has zero sexual history with her.": "Completamente inexperta. Nunca ha hecho nada sexual, ni siquiera una paja. Fuerza el rasgo Virgen. Su novio (si tiene) tiene cero historial sexual con ella.",
            "Has not had penetrative sex yet. A special scene plays during her first time. Her reaction depends on your approach and her personality.": "Aún no ha tenido sexo penetrativo. Una escena especial ocurre en su primera vez. Su reacción depende de tu enfoque y su personalidad.",
            "Has done everything before with someone else. Not a virgin and knows what she's doing. Cannot coexist with Virgin or Naive.": "Ya ha hecho de todo con otra persona. No es virgen y sabe lo que hace. No puede coexistir con Virgen o Inocente.",
            "Likes watching others. May react differently during scenes involving multiple people.": "Le gusta observar a otros. Puede reaccionar diferente en escenas con múltiples personas.",
            "Likes being watched. Gets aroused by the idea of someone seeing her.": "Le gusta que la observen. Se excita con la idea de que alguien la vea.",
            "Only attracted to women. Love does NOT help with sexual acts. Only Obedience and Inhibition count. She must progress through acts in order. Kissing is the LAST act unlocked, not the first. Her resistance decays with each act. Asking for sexual acts costs Love.": "Solo atraída por mujeres. El Amor NO ayuda con actos sexuales. Solo Obediencia e Inhibición cuentan. Debe progresar por los actos en orden. El beso es el ÚLTIMO acto desbloqueado, no el primero. Su resistencia disminuye con cada acto. Pedir actos sexuales cuesta Amor.",
            "Attracted to both men and women. Can have a boyfriend or a girlfriend. Uses normal hetero mechanics for everything. No special thresholds or restrictions.": "Atraída por hombres y mujeres. Puede tener novio o novia. Usa mecánicas hetero normales para todo. Sin umbrales ni restricciones especiales.",
            "She already has a boyfriend at game start. You need to build Temptation to get past her loyalty. Her boyfriend may catch you, confront you, or react to rumors.": "Ya tiene novio al inicio del juego. Necesitas construir Tentación para superar su lealtad. Su novio puede atraparte, confrontarte o reaccionar a rumores.",
            "She already has a girlfriend at game start. Works similarly to having a boyfriend but with a female NPC partner.": "Ya tiene novia al inicio del juego. Funciona similar a tener novio pero con una pareja NPC femenina.",
            "Special Traits": "Rasgos Especiales",
            # NTR Boundary level labels
            "Non-penetration only": "Solo sin penetración",
            "Condom-protected sex": "Sexo con condón",
            "Raw sex, no creampie or anal": "Sexo sin condón, sin acabar dentro ni anal",
            "No limits": "Sin límites",
            # Phone group create NPC label
            "(partner)": "(pareja)",
            "%s's BF": "novio de %s",
            "%s's GF": "novia de %s",
            # Spectrum labels
            "Straight": "Hetero", "Party Bi": "Bi de Fiesta", "Curious": "Curiosa", "Bisexual": "Bisexual", "Lesbian": "Lesbiana",
            "Sexuality": "Sexualidad",
            "Story": "Historia",
            # Stat popups (girl-to-girl + NPC partner)
            "Friendship": "Amistad",
            "NPC Love": "Amor del NPC",
            "Suspicion": "Sospecha",
            # Phone Fertility app (screen_fertility.rpy) + discovery banners
            "Birth control status discovered": "Estado anticonceptivo descubierto",
            "Fertility cycle discovered": "Ciclo fértil descubierto",
            "Safe": "Seguro", "Low risk": "Riesgo bajo", "Fertile": "Fértil", "Peak": "Pico",
            "Away": "Ausente", "Pregnant": "Embarazada", "Postpartum": "Posparto",
            "Recovering after birth. Not fertile right now.": "Recuperándose del parto. No está fértil por ahora.",
            "She can't get pregnant.": "Ella no puede quedar embarazada.",
            "Early": "Inicio", "Showing": "Se nota", "Full belly": "Panza completa",
            "%d day": "%d día", "%d days": "%d días",
            "Away giving birth. Back in %s.": "Fuera para dar a luz. Vuelve en %s.",
            "Day %d": "Día %d",
            "Due in %s": "Nace en %s",
            "Day %d of 28": "Día %d de 28",
            "Fertile window ends in %s": "La ventana fértil termina en %s",
            "Fertile window in %s": "Ventana fértil en %s",
            "Birth control: ???": "Anticonceptivo: ???",
            "Not on the pill": "No toma la píldora",
            "Placebo, 0% (she thinks it's real)": "Placebo, 0% (ella cree que es real)",
            "On the pill, %d%% effective": "Toma la píldora, %d%% de eficacia",
            "missed: %s": "olvidó: %s",
            "Fertility vitamins": "Vitaminas de fertilidad",
            "Not active": "Inactiva",
            "Pills": "Píldoras", "Placebo": "Placebo", "Plan B": "Plan B",
            "Child support: $%d per week": "Manutención: $%d por semana",
            "Extra breedable: wider fertile window": "Súper fértil: ventana fértil más amplia",
            "Cycle unknown. Pay attention to her moods when you chat.": "Ciclo desconocido. Fíjate en su humor cuando charlen.",
            "Unknown. Listen for hints when you chat with her.": "Desconocido. Presta atención a las pistas cuando charles con ella.",
            "CYCLE": "CICLO",
            "STATUS": "ESTADO",
            "BIRTH CONTROL": "ANTICONCEPTIVO",
            "PLAN B": "PLAN B",
            "RISK TODAY": "RIESGO HOY",
            "YOUR SUPPLIES": "TUS OBJETOS",
            "CHILDREN": "HIJOS",
            "Effectiveness": "Eficacia",
            "Used %d of %d": "Usó %d de %d",
            "She won't take any more for now.": "Ella no va a tomar ninguna más por ahora.",
            "Next dose frees up in %s": "Próxima dosis disponible en %s",
            "??? Needs her cycle and her birth control status.": "??? Falta su ciclo y su estado anticonceptivo.",
            "Cycle, birth control and risk": "Ciclo, anticonceptivo y riesgo",
            "Check Fertility in her contact": "Mira Fertilidad en su contacto",
            "She started taking the pill": "Empezó a tomar la píldora",
            "She stopped taking the pill": "Dejó de tomar la píldora",
            "Inside": "Dentro", "Pull out": "Acabar fuera",
            "Children: %d": "Hijos: %d",
            "Chit chat with her and listen to what she says after sex. Asking her directly is risky: she may refuse or take offense.": "Charla con ella y escucha lo que dice después del sexo. Preguntarle directamente es arriesgado: puede negarse u ofenderse.",
            # Fertility vitamins (v0.12.1)
            "Includes your fertility vitamins (x%s).": "Incluye tus vitaminas de fertilidad (x%s).",
            "Active x%s, %s left": "Activa x%s, quedan %s",
            # Player FIRSTS / discovery banner
            "You got her pregnant": "La dejaste embarazada",
            # Children age labels
            "Newborn": "Recién nacido", "Infant": "Nene", "Baby": "Bebé", "Toddler": "Pequeñín",
            "Raised by %s": "Criado por %s",
            "Next payment in %s": "Próximo pago en %s",
            # C. Johnson intel
            "A baby costs money: work": "Un bebé cuesta dinero: trabaja",
            "Many babies, many bills: work": "Muchos bebés, muchas cuentas: trabaja",
            # Gift discovery banner & preferences labels
            "Her taste in gifts discovered": "Su gusto en regalos descubierto",
            "Loves": "Le encanta", "Not a fan": "No le gusta",
            # Trait Picker tabs & section headers (v0.12.1)
            "Personality": "Personalidad", "Relationships": "Relaciones",
            "Experience": "Experiencia", "Lifestyle": "Estilo de Vida",
            "Hobbies": "Pasatiempos", "Kinks": "Fetiches",
            "Orientation": "Orientación", "Partner": "Pareja",
            # Fertility IUD state
            "IUD": "DIU",
            "IUD active after delivery. Protected for now.": "DIU activo después del parto. Protegida por ahora.",
            # BigFans ATM tag
            "ATM": "ATM",
            # Status screen trait hints (v0.12.1)
            "Nerd": "Nerd", "Gym Rat": "Rata de Gimnasio",
            # Trait picker: the Control pair, Married, the short descriptions (2026-10-03)
            "Control": "Control", "Femdom": "Femdom", "Submissive": "Sumisa", "Married": "Casada", "Hates Cum": "Odia el Semen",
            "Wants to be in charge. Resists acts that put you in control.": "Quiere tener el mando. Se resiste a los actos que te dejan a ti el control.",
            "Likes being told what to do. Gives in to your control easily.": "Le gusta que le digan qué hacer. Cede a tu control con facilidad.",
            "Holds her liquor. Alcohol affects her far less.": "Aguanta bien el alcohol. La bebida la afecta mucho menos.",
            "Low tolerance. Gets drunk fast and sick easily.": "Poca tolerancia. Se emborracha rápido y se marea con facilidad.",
            "Academically obsessed. Earns double study points and reacts strongly to class disruptions.": "Obsesionada con los estudios. Gana el doble de puntos de estudio y reacciona fuerte cuando interrumpen la clase.",
            "Lives at the gym. Respects strength, despises weakness.": "Vive en el gimnasio. Respeta la fuerza, desprecia la debilidad.",
            "She's married.": "Está casada.",
            "Loves anal": "Ama el anal", "Hates anal": "Odia el anal",
            "Can hold her liquor": "Aguanta el alcohol", "Lightweight drinker": "No aguanta la bebida",
            "Struggling financially": "Dificultades económicas", "Wealthy": "Rica",
            "Breeding kink": "Fetiche de embarazo",
            "Wants to be a mom": "Quiere ser mamá",
            "Terrified of pregnancy": "Le aterra embarazarse",
            # CJ intel labels (v0.12.1)
            "A baby costs money: work": "Un bebé cuesta dinero: trabaja",
            "Many babies, many bills: work": "Muchos bebés, muchas cuentas: trabaja",
            # CJ van items in the phone inventory (v0.12.1)
            "Girls Tracker": "Rastreador de Chicas", "Instant Pregnancy Test": "Prueba de Embarazo Instantánea",
            # BigFans video location (screen_status)
            "Dressing Room": "Probador",
            # Family contact names
            "Dad": "Papá",
        },
        # Russian: prepared 2026-10-02, translation pending (docs/translation_ru.md)
        "ru": {
            "Morning": "Утро",
            "Midday": "День",
            "Evening": "Вечер",
            "Night": "Ночь",
            "Sunday": "Воскресенье",
            "Monday": "Понедельник",
            "Tuesday": "Вторник",
            "Wednesday": "Среда",
            "Thursday": "Четверг",
            "Friday": "Пятница",
            "Saturday": "Суббота",
            "[weekday_name!u], DAY [Day]": "[weekday_name!u], ДЕНЬ [Day]",
            "Camera": "Камера",
            "Cum": "Сперма",
            "Public": "На публике",
            "Sex Style": "Стиль секса",
            "Loyalty": "Верность",
            "Anal": "Анал",
            "Economy": "Деньги",
            "Sharing": "Делиться",
            "Fertility": "Фертильность",
            "Pregnancy": "Беременность",
            "Camera Lover": "Любит камеру",
            "Camera Hater": "Ненавидит камеру",
            "Cum Lover": "Любит сперму",
            "Cum Hater": "Ненавидит сперму",
            "Public Fetish": "Фетиш на публике",
            "Public Shy": "Стесняется на людях",
            "Hardcore": "Жёсткая",
            "Gentle": "Нежная",
            "Loyal": "Верная",
            "Cheater": "Изменщица",
            "Anal Lover": "Любит анал",
            "Anal Hater": "Ненавидит анал",
            "Poor": "Бедная",
            "Rich": "Богатая",
            "Loves being filmed. May ask to be recorded.": "Обожает, когда её снимают. Может сама попросить записать.",
            "Hates cameras. Very resistant to filming.": "Ненавидит камеры. Очень против съёмки.",
            "Loves cum inside her. Hates condoms.": "Обожает, когда кончают в неё. Ненавидит презервативы.",
            "Hates cum contact. Demands condoms.": "Не выносит контакта со спермой. Требует презерватив.",
            "Turned on by public exposure and risk.": "Заводится от риска и чужих глаз.",
            "Terrified of public exposure.": "До ужаса боится, что её увидят.",
            "Prefers rough, fast, intense sex.": "Любит грубый, быстрый, жёсткий секс.",
            "Prefers slow, intimate, gentle sex.": "Любит медленный, нежный, интимный секс.",
            "Strongly resists cheating. Hard to corrupt.": "Сильно сопротивляется измене. Её трудно развратить.",
            "Cheating is easy and enjoyable for her.": "Изменять ей легко и даже приятно.",
            "Loves anal. Gets more pleasure, may ask for it.": "Обожает анал. Получает больше удовольствия, может попросить сама.",
            "Hates/fears anal. Pain-focused, very resistant.": "Ненавидит и боится анала. Думает о боли, сильно сопротивляется.",
            "Struggles financially. Gifts mean more to her.": "С деньгами туго. Подарки значат для неё больше.",
            "Wealthy background. Hard to impress with gifts.": "Из богатой семьи. Подарками её не удивишь.",
            "Naive": "Наивная",
            "Experienced": "Опытная",
            "Voyeur": "Вуайеристка",
            "Exhibitionist": "Эксгибиционистка",
            "Has a Boyfriend": "Есть парень",
            "Has a Girlfriend": "Есть девушка",
            "Lesbian": "Лесбиянка",
            "Bisexual": "Бисексуалка",
            "Has never done anything sexual. No history at all. Forces Virgin.": "Никогда ничего не делала в сексе. Никакого опыта. Включает «Девственницу».",
            "Has not had sex yet.": "Ещё не занималась сексом.",
            "Has done everything before with someone else. Not a virgin, knows what she's doing.": "Уже всё пробовала с кем-то другим. Не девственница, знает, что делает.",
            "Likes watching others.": "Любит смотреть на других.",
            "Likes being watched.": "Любит, когда на неё смотрят.",
            "She already has an NPC boyfriend at game start. The boyfriend will be present in the game.": "У неё с самого начала есть парень (NPC). Он будет появляться в игре.",
            "She already has an NPC girlfriend at game start. The girlfriend will be present in the game.": "У неё с самого начала есть девушка (NPC). Она будет появляться в игре.",
            "Only attracted to women. Requires dominance or leverage for sexual acts.": "Её привлекают только женщины. Для секса нужны власть над ней или рычаги давления.",
            "Attracted to both men and women. Can have a boyfriend or girlfriend. Uses normal mechanics.": "Её привлекают и мужчины, и женщины. Может встречаться с парнем или девушкой. Обычные механики.",
            "She loves being on camera": "Она обожает камеру",
            "She hates cameras": "Она ненавидит камеры",
            "She loves cum": "Она обожает сперму",
            "She hates cum": "Она ненавидит сперму",
            "She likes doing it in public": "Ей нравится заниматься этим на людях",
            "She's terrified of public exposure": "Она до ужаса боится, что её увидят",
            "She likes it rough": "Она любит пожёстче",
            "She likes it gentle": "Она любит нежно",
            "She's very loyal": "Она очень верная",
            "She's open to cheating": "Она не против измены",
            "She's completely inexperienced": "У неё совсем нет опыта",
            "She likes watching others": "Она любит смотреть на других",
            "She likes being watched": "Она любит, когда на неё смотрят",
            "She's open to sharing": "Она не против делиться",
            "She already has a boyfriend": "У неё уже есть парень",
            "She already has a girlfriend": "У неё уже есть девушка",
            "She has done everything with her partner": "Она уже всё делала со своим партнёром",
            "She loves anal": "Она обожает анал",
            "She hates anal": "Она ненавидит анал",
            "She's only attracted to women": "Её привлекают только женщины",
            "She's attracted to both men and women": "Её привлекают и мужчины, и женщины",
            "She struggles financially": "У неё туго с деньгами",
            "She comes from a wealthy background": "Она из богатой семьи",
            "She can hold her liquor": "Она умеет пить",
            "She can't handle her drinks": "Она быстро пьянеет",
            "She's a total bookworm": "Она настоящий книжный червь",
            "She lives at the gym": "Она живёт в спортзале",
            "Extra breedable": "Очень плодовитая",
            "Infertile": "Бесплодная",
            "She has a pregnancy fetish": "У неё фетиш на беременность",
            "She's terrified of getting pregnant": "Она до ужаса боится забеременеть",
            "(not available)": "(недоступно)",
            "(opposite selected)": "(выбрано противоположное)",
            "(locked: lesbian)": "(заблокировано: лесбиянка)",
            "(locked: pregnancy fetish)": "(заблокировано: фетиш на беременность)",
            "(locked: has girlfriend)": "(заблокировано: есть девушка)",
            "(locked: naive)": "(заблокировано: наивная)",
            "(conflict)": "(конфликт)",
            "Personality Traits": "Черты характера",
            "Done": "Готово",
            "Randomize the rest (fill to 3)": "Остальное случайно (до 3)",
            "TRAITS": "ЧЕРТЫ",
            "She is dating someone": "Она с кем-то встречается",
            "She has no boyfriend": "У неё нет парня",
            "Study habits discovered": "Ты узнал, как она учится",
            "Favorite act discovered": "Ты узнал, что она любит в постели",
            "She accepted your petname": "Она приняла твоё прозвище",
            "She has a name for you": "У неё есть для тебя прозвище",
            "Her first kiss": "Её первый поцелуй",
            "You're her first handjob": "Ты первый, кому она подрочила",
            "You're her first titjob": "Ты первый, кому она дала между сисек",
            "You're her first blowjob": "Ты первый, кому она сделала минет",
            "She's never done this for anyone": "Она ни для кого такого не делала",
            "You took her virginity": "Ты лишил её девственности",
            "You're her first anal": "Ты первый, с кем у неё был анал",
            "First time raw": "Первый раз без презерватива",
            "First creampie": "Первый раз кончил в неё",
            "She struggles with money": "У неё туго с деньгами",
            "She comes from money": "Она из богатой семьи",
            "She's a virgin": "Она девственница",
            "She's not a virgin": "Она не девственница",
            "BF never did: %s": "С парнем не было: %s",
            "BF has done: %s": "С парнем было: %s",
            "BF": "Парень",
            "GF": "Девушка",
            "never did": "не было",
            "has done": "было",
            "Your first kiss": "Твой первый поцелуй",
            "Your first handjob": "Тебе впервые подрочили",
            "Your first titjob": "Тебе впервые сделали между сисек",
            "Your first blowjob": "Твой первый минет",
            "Lost your virginity": "Ты потерял девственность",
            "Your first anal": "Твой первый анал",
            "Your first creampie": "Ты впервые кончил внутрь",
            "First time going raw": "Первый раз без презерватива",
            "You took someone's virginity": "Ты лишил кого-то девственности",
            "You got your first girlfriend": "У тебя появилась первая девушка",
            "Peak physical condition": "Пик физической формы",
            "New intel acquired": "Получены новые сведения",
            "New Trait Discovered": "Открыта новая черта",
            "C. JOHNSON'S INTEL": "СВЕДЕНИЯ К. ДЖОНСОНА",
            "People are gossiping": "О тебе сплетничают",
            "Your breakup is known": "Все знают о твоём расставании",
            "Professors noticed you": "Преподаватели тебя заметили",
            "Girls find you handsome": "Девушки считают тебя красавчиком",
            "You... You are ugly :c": "Ты... Ты урод :c",
            "%s is changing": "%s меняется",
            "%s is hostile to you": "%s тебя недолюбливает",
            "%s is not jealous": "%s не ревнует",
            "%s is jealous": "%s ревнует",
            "Hotdogs recover energy": "Хот-доги восстанавливают энергию",
            "Give gifts to pay for sex": "Дари подарки, чтобы платить за секс",
            "No intel yet": "Сведений пока нет",
            "Your Girlfriend": "Твоя девушка",
            "Stranger": "Незнакомка",
            "Acquaintance": "Знакомая",
            "Friend": "Подруга",
            "Close Friend": "Близкая подруга",
            "Intimate": "Близкие",
            "Ex": "Бывшая",
            "Friendly": "Дружелюбный",
            "Neutral": "Нейтральный",
            "Hostile": "Враждебный",
            "NTR": "NTR",
            "Proud": "Гордый",
            "PARTNER TRAITS": "ЧЕРТЫ ПАРТНЁРА",
            "Disposition": "Настрой",
            "Enjoys watching and sharing. Never breaks up over cheating.": "Любит смотреть и делиться. Никогда не бросит из-за измены.",
            "Jealous and possessive. Will break up quickly if caught.": "Ревнивый собственник. Быстро бросит, если застукает.",
            "Slightly jealous. May break up eventually.": "Немного ревнует. Со временем может бросить.",
            "Preferences": "Предпочтения",
            "Wants to watch in person.": "Хочет смотреть вживую.",
            "Wants videos of her.": "Хочет видео с ней.",
            "NTR Limits": "Границы NTR",
            "What is the initial boundary the partner is comfortable with? You can push these limits during gameplay and unlock new scenarios.": "С какой границы партнёру комфортно начать? По ходу игры ты сможешь раздвигать эти границы и открывать новые сценарии.",
            "Randomize All": "Всё случайно",
            "Lesbian partners do not have boundary levels.": "У партнёрш-лесбиянок нет уровней границ.",
            "In love": "Без ума",
            "Moderate": "Умеренно",
            "Low": "Слабо",
            "Very suspicious": "Сильно подозревает",
            "Suspicious": "Подозревает",
            "Uneasy": "Неспокойно",
            "Unaware": "Ничего не знает",
            "Very prepared": "Отлично подготовилась",
            "Well studied": "Хорошо подготовилась",
            "Somewhat prepared": "Немного готовилась",
            "Barely studied": "Почти не учила",
            "Hasn't studied at all": "Совсем не учила",
            "Best Friends": "Лучшие подруги",
            "Friends": "Подруги",
            "Acquaintances": "Знакомые",
            "Virgin": "Девственница",
            "Loves being filmed": "Обожает съёмку",
            "Hates cameras": "Ненавидит камеры",
            "Loves cum": "Обожает сперму",
            "Hates cum": "Ненавидит сперму",
            "Turned on by public risk": "Заводится от риска на людях",
            "Terrified of exposure": "Боится, что увидят",
            "Likes it rough": "Любит пожёстче",
            "Likes it gentle": "Любит нежно",
            "Very loyal": "Очень верная",
            "Prone to cheating": "Склонна к измене",
            "Likes watching": "Любит смотреть",
            "Likes being watched": "Любит, когда смотрят",
            "Open to sharing": "Не против делиться",
            "Hasn't studied": "Не учила",
            "Kiss": "Поцелуй",
            "Handjob": "Дрочка",
            "Titjob": "Между сисек",
            "Footjob": "Ногами",
            "Rimjob": "Римминг",
            "Father's Apartment (Not with company)": "Квартира отца (не с компанией)",
            "Talk about her (Already today)": "Поговорить о ней (уже сегодня)",
            "Give him a drink (No drinks)": "Угостить выпивкой (нет напитков)",
            "Blowjob": "Минет",
            "Sex": "Секс",
            "Any video": "Любое видео",
            "cheating": "измена",
            "public": "на публике",
            "cuckold": "куколд",
            "threesome": "втроём",
            "face visible": "лицо видно",
            "face hidden": "лицо скрыто",
            "secret": "тайно",
            "HD": "HD",
            "%s stopped the recording.": "%s прекращает запись.",
            "Masturbation": "Мастурбация",
            "Cowgirl": "Наездница",
            "Reverse Cowgirl": "Обратная наездница",
            "Doggy Style": "Раком",
            "Full Nelson": "Фулл-нельсон",
            "Full Nelson Anal": "Фулл-нельсон анал",
            "Laying Down": "Лёжа",
            "Laying Down Anal": "Анал лёжа",
            "Reverse Cowgirl Anal": "Обратная наездница анал",
            "Creampie": "Кончить внутрь",
            "LOSING VIRGINITY": "ПОТЕРЯ ДЕВСТВЕННОСТИ",
            "%dd left": "осталось %d дн.",
            "Expires today!": "Истекает сегодня!",
            "%s's Room": "Комната {case=gen}%s{/case}",
            "Campus": "Кампус",
            "Pool": "Бассейн",
            "Showers": "Душевые",
            "Apartment": "Квартира",
            "Apartment Bedroom": "Спальня в квартире",
            "Apartment Bathroom": "Ванная в квартире",
            "Gym": "Спортзал",
            "Classroom": "Аудитория",
            "Mall": "Торговый центр",
            "Hall": "Коридор",
            "Street": "Улица",
            "Party": "Вечеринка",
            "Restaurant Restroom": "Туалет ресторана",
            "Gwen's Room": "Комната Гвен",
            "Rogue's Room": "Комната Шельмы",
            "Negasonic's Room": "Комната Боеголовки",
            "Class (Closing soon)": "Занятия (скоро закрытие)",
            "Class (Closed)": "Занятия (закрыто)",
            "Gym (Closing soon)": "Спортзал (скоро закрытие)",
            "Gym (Closed)": "Спортзал (закрыто)",
            "Mall (Closing soon)": "Торговый центр (скоро закрытие)",
            "Mall (Closed)": "Торговый центр (закрыто)",
            "Study (Too late)": "Учиться (слишком поздно)",
            "Wait (It's night)": "Ждать (уже ночь)",
            "Call someone over...": "Позвать кого-нибудь...",
            "Who do you want to call over?": "Кого позвать?",
            "Who should leave?": "Кому уйти?",
            "%s walks over.": "%s подходит.",
            "You hear %s arrive nearby.": "Ты слышишь, как %s подходит ближе.",
            "After a while, %s arrives.": "Через какое-то время приходит %s.",
            "Hey... I've been thinking. Can I call you %s from now on?": "Слушай... я тут подумала. Можно я теперь буду звать тебя «%s»?",
            "You feel more like a %s to me now... is that okay?": "Ты для меня теперь скорее «%s»... ничего?",
            "I want to start calling you %s. What do you think?": "Хочу звать тебя «%s». Что скажешь?",
            "Princess": "Принцесса",
            "Babe": "Малышка",
            "Honey": "Солнышко",
            "Love": "Любовь моя",
            "Angel": "Ангел",
            "Slut": "Шлюшка",
            "Whore": "Шлюха",
            "Cumdumpster": "Спермоприёмник",
            "Cutie": "Милашка",
            "Pumpkin": "Пупсик",
            "Sugar": "Сахарок",
            "Sweetheart": "Дорогой",
            "Tiger": "Тигр",
            "Daddy": "Папочка",
            "Master": "Хозяин",
            "Sir": "Господин",
            "Queen": "Королева",
            "Goddess": "Богиня",
            "Mistress": "Госпожа",
            "Pet": "Питомец",
            "Toy": "Игрушка",
            "Good boy": "Хороший мальчик",
            "Stepmom": "Мачеха",
            "Boy": "Мальчик",
            "Condoms": "Презервативы",
            "Japanese Condoms": "Японские презервативы",
            "Condom": "Презерватив",
            "JP Condom": "Японский презерватив",
            "Raw": "Без презерватива",
            "Bottle of Vodka": "Бутылка водки",
            "Chocolate Box": "Коробка конфет",
            "Flowers": "Цветы",
            "Perfume": "Духи",
            "Necklace": "Ожерелье",
            "Handbag": "Сумочка",
            "Ring": "Кольцо",
            "Designer Watch": "Дизайнерские часы",
            "Jewelry Set": "Набор украшений",
            "Vodka": "Водка",
            "Cools Light Beer": "Пиво «Кулс Лайт»",
            "Xitos Vodka": "Водка «Ксайтос»",
            "Running Douglas Whiskey": "Виски «Раннинг Дуглас»",
            "Alinmus Beer": "Пиво «Алинмус»",
            "HunterMaster": "«ХантерМастер»",
            "UnusualAlias Moonshine": "Самогон «Анъюжуал Элиас»",
            "light buzz": "лёгкий хмель",
            "strong buzz": "сильный хмель",
            "heavy buzz": "тяжёлый хмель",
            "Beer": "Пиво",
            "Whiskey": "Виски",
            "Favorite food": "Любимая еда",
            "Favorite drink": "Любимый напиток",
            "Preferred brand": "Любимая марка",
            "Favorite food discovered": "Ты узнал её любимую еду",
            "Favorite drink discovered": "Ты узнал её любимый напиток",
            "Favorite brand discovered": "Ты узнал её любимую марку",
            "Steak": "Стейк",
            "Pasta": "Паста",
            "Chicken": "Курица",
            "Salad": "Салат",
            "Unknown": "Неизвестно",
            "You": "Ты",
            "Drink Level": "Опьянение",
            "Heavy Drinker": "Умеет пить",
            "Lightweight": "Быстро пьянеет",
            "Holds her liquor. Alcohol affects her far less, so she gets drunk slowly and rarely gets sick. During Truth or Dare you'll need to keep the drinks coming to loosen her up.": "Умеет пить. Алкоголь действует на неё куда слабее: пьянеет медленно и почти никогда не перебирает. В «Правде или действии» придётся подливать почаще, чтобы её раскрепостить.",
            "Low tolerance. She gets drunk fast and gets sick easily, so a few drinks go a long way. Push her too hard and she'll be sick and done for the night.": "Слабая к алкоголю. Быстро пьянеет и легко перебирает, так что хватает пары стаканов. Перестараешься, и ей станет плохо, а вечер для неё закончится.",
            "Polyamorous": "Полиаморная",
            "Monogamous": "Моногамная",
            "Open to sharing a partner. Much more willing to accept a harem.": "Не против делить партнёра. Гораздо охотнее согласится на гарем.",
            "Demands exclusivity. Extremely resistant to sharing.": "Требует верности. Категорически против того, чтобы делить партнёра.",
            "Open to sharing. She can accept a harem arrangement where the player dates multiple girls at once. Less jealous in multi-girl scenarios and threesomes.": "Не против делиться. Может согласиться на гарем, где игрок встречается сразу с несколькими девушками. Меньше ревнует в сценах с несколькими девушками и втроём.",
            "Wants exclusivity. She demands a committed relationship and reacts badly if she discovers the player is with other girls. Higher jealousy during threesomes and multi-girl situations.": "Хочет верности. Требует серьёзных отношений и плохо реагирует, если узнаёт, что игрок с другими девушками. Сильнее ревнует втроём и в ситуациях с несколькими девушками.",
            "She's open to sharing her partner": "Она не против делить партнёра",
            "She demands exclusivity": "Она требует верности",
            "Breedable": "Плодовитая",
            "Pregnancy Fetish": "Фетиш на беременность",
            "Pregnancy Fear": "Боится беременности",
            "Extremely fertile. 1.5x conception chance and wider fertile window.": "Очень плодовитая. Шанс зачатия x1.5 и более широкое фертильное окно.",
            "Cannot get pregnant. Zero conception chance.": "Не может забеременеть. Шанс зачатия нулевой.",
            "Wants to be bred. Refuses the pill, craves creampies.": "Хочет, чтобы её обрюхатили. Отказывается от таблеток, обожает, когда кончают внутрь.",
            "Terrified of pregnancy. Always on the pill, never forgets.": "До ужаса боится беременности. Всегда на таблетках и никогда не забывает.",
            "She's incredibly fertile": "Она невероятно плодовитая",
            "She can't get pregnant": "Она не может забеременеть",
            "She wants to be bred": "Она хочет, чтобы её обрюхатили",
            "Ask her about sharing": "Спросить её о том, чтобы делиться",
            "Tell her it was a mistake": "Сказать, что это была ошибка",
            "Pharmacy": "Аптека",
            "Birth Control Pills": "Противозачаточные таблетки",
            "Sunflower Fertility Shield": "Защита от зачатия «Подсолнух»",
            "Morning After Pill": "Таблетка экстренной контрацепции",
            "Fertility Vitamins": "Витамины для зачатия",
            "Tripod": "Штатив",
            "Tekmix Camera": "Камера Tekmix",
            "Drinks": "Напитки",
            "Gifts": "Подарки",
            "Hangout Night": "Тусовка",
            "already invited today": "уже звал сегодня",
            "too late": "слишком поздно",
            "need to buy a bottle": "нужно купить бутылку",
            "What about just as friends?": "А если просто как друзья?",
            "Never mind": "Неважно",
            "Condom (x6-pack)": "Презервативы (6 шт.)",
            "Black Bikini": "Чёрное бикини",
            "Green Bikini": "Зелёное бикини",
            "Pink Bikini": "Розовое бикини",
            "Blue Bikini": "Синее бикини",
            "Red Bikini": "Красное бикини",
            "What do you think about the game?": "Что думаешь об игре?",
            "boyfriend": "парень",
            "girlfriend": "девушка",
            "partner": "партнёр",
            "he": "он",
            "she": "она",
            "He": "Он",
            "She": "Она",
            "him": "его",
            "her_obj": "её",
            "his": "его",
            "her_poss": "её",
            "His": "Его",
            "Her_poss": "Её",
            "npc_friend_m": "Друг",
            "npc_friend_f": "Подруга",
            "A girl": "Девушка",
            "A guy": "Парень",
            "Traits": "Черты",
            "Each girl has personality traits that shape her behavior, dialogue, approval thresholds, and scene outcomes. Check the {b}Traits{/b} tab for a full glossary.": "У каждой девушки есть черты характера: от них зависят её поведение, реплики, пороги согласия и исход сцен. Полный список во вкладке {b}Черты{/b}.",
            "Personality Traits (Opposing Pairs)": "Черты характера (противоположные пары)",
            "Loves being filmed. She may ask to be recorded and reacts positively to it. Cannot be blackmailed if she's single, since she doesn't care about leaked videos.": "Обожает, когда её снимают. Может сама попросить записать и реагирует на съёмку хорошо. Если она свободна, шантажировать её нельзя: слитые видео ей безразличны.",
            "Hates cameras. Very resistant to being filmed. Much harder to get recording consent. If she catches you recording, the consequences are worse.": "Ненавидит камеры. Очень против съёмки. Получить согласие на запись гораздо труднее. Если она поймает тебя на съёмке, последствия будут хуже.",
            "Loves cum inside her and hates condoms. She may try to force a creampie during sex. Reacts very positively to raw sex and finishing inside.": "Обожает, когда кончают в неё, и ненавидит презервативы. Во время секса может сама добиваться, чтобы ты кончил внутрь. Очень хорошо реагирует на секс без презерватива и на то, что ты кончаешь в неё.",
            "Hates any contact with cum. Demands condoms every time. Reacts very negatively to creampies and removing condoms.": "Не выносит любого контакта со спермой. Каждый раз требует презерватив. Очень плохо реагирует, если кончить в неё или снять презерватив.",
            "Turned on by public exposure and risk. Easier to seduce in public locations. Approval gets a bonus in public areas.": "Заводится от риска и чужих глаз. В людных местах её легче соблазнить. В общественных местах согласие получает бонус.",
            "Terrified of being seen. Much harder to convince for anything sexual in public. Stronger negative reaction if caught.": "До ужаса боится, что её увидят. Уговорить её на что-то сексуальное на людях гораздо труднее. Если вас застукают, реакция будет сильнее.",
            "Prefers rough, fast, intense sex. Higher pleasure from fast speeds. Dialogue and reactions reflect her preference for dominance.": "Любит грубый, быстрый, жёсткий секс. Больше удовольствия от быстрого темпа. Реплики и реакции показывают, что ей нравится, когда ею командуют.",
            "Prefers slow, intimate, gentle sex. Higher pleasure from slow speeds. Reacts negatively to overly rough or degrading actions.": "Любит медленный, нежный, интимный секс. Больше удовольствия от медленного темпа. Плохо реагирует на слишком грубое или унизительное обращение.",
            "Strongly resists cheating on her partner. Much harder to corrupt. High approval thresholds for sexual acts while she has a boyfriend/girlfriend. Can evolve into Cheater through corruption over time.": "Сильно сопротивляется измене партнёру. Её гораздо труднее развратить. Пока у неё есть парень или девушка, пороги согласия на секс высокие. Со временем может стать «Изменщицей».",
            "Cheating is easy and even enjoyable for her. Lower approval thresholds for acts while she has a partner. Less guilt after cheating.": "Изменять ей легко и даже приятно. Пока у неё есть партнёр, пороги согласия ниже. После измены меньше чувства вины.",
            "Loves anal sex. Gets more pleasure from it and may ask for it. Lower thresholds for anal acts.": "Обожает анальный секс. Получает от него больше удовольствия и может попросить сама. Пороги для анала ниже.",
            "Hates and fears anal. Focused on pain over pleasure. Very high thresholds and strong resistance to anal acts.": "Ненавидит и боится анала. Думает о боли, а не об удовольствии. Очень высокие пороги и сильное сопротивление аналу.",
            "Struggles financially. Gifts have a stronger effect on her. She's more open to financial persuasion after enough gifts, and her prices are lower.": "С деньгами туго. Подарки действуют на неё сильнее. После достаточного числа подарков её легче уговорить за деньги, и цены у неё ниже.",
            "Wealthy background. Hard to impress with gifts. She's more resistant to financial persuasion, requires more gifts to unlock it, and her prices are higher.": "Из богатой семьи. Подарками её не удивишь. Уговорить её за деньги труднее, для этого нужно больше подарков, и цены у неё выше.",
            "Completely inexperienced. Has never done anything sexual, not even a handjob. Forces Virgin trait. Her boyfriend (if any) has zero sexual history with her.": "Совсем без опыта. Никогда ничего не делала в сексе, даже не дрочила. Включает черту «Девственница». С её парнем (если он есть) у неё ничего не было.",
            "Has not had penetrative sex yet. A special scene plays during her first time. Her reaction depends on your approach and her personality.": "Ещё не было проникновения. Её первый раз идёт особой сценой. Её реакция зависит от твоего подхода и её характера.",
            "Has done everything before with someone else. Not a virgin and knows what she's doing. Cannot coexist with Virgin or Naive.": "Уже всё пробовала с кем-то другим. Не девственница и знает, что делает. Несовместима с «Девственницей» и «Наивной».",
            "Likes watching others. May react differently during scenes involving multiple people.": "Любит смотреть на других. Может по-другому вести себя в сценах с несколькими людьми.",
            "Likes being watched. Gets aroused by the idea of someone seeing her.": "Любит, когда на неё смотрят. Её заводит мысль, что кто-то её видит.",
            "Only attracted to women. Love does NOT help with sexual acts. Only Obedience and Inhibition count. She must progress through acts in order. Kissing is the LAST act unlocked, not the first. Her resistance decays with each act. Asking for sexual acts costs Love.": "Её привлекают только женщины. Любовь НЕ помогает в сексе. Считаются только Послушание и Раскованность. Действия открываются строго по порядку. Поцелуй открывается ПОСЛЕДНИМ, а не первым. Её сопротивление падает с каждым разом. Просьбы о сексе стоят Любви.",
            "Attracted to both men and women. Can have a boyfriend or a girlfriend. Uses normal hetero mechanics for everything. No special thresholds or restrictions.": "Её привлекают и мужчины, и женщины. Может встречаться с парнем или девушкой. Во всём работают обычные механики. Никаких особых порогов и ограничений.",
            "She already has a boyfriend at game start. You need to build Temptation to get past her loyalty. Her boyfriend may catch you, confront you, or react to rumors.": "У неё с самого начала есть парень. Чтобы пробить её верность, нужно копить Искушение. Её парень может вас застукать, разобраться с тобой или отреагировать на слухи.",
            "She already has a girlfriend at game start. Works similarly to having a boyfriend but with a female NPC partner.": "У неё с самого начала есть девушка. Работает так же, как с парнем, только партнёр NPC женского пола.",
            "Special Traits": "Особые черты",
            "Non-penetration only": "Только без проникновения",
            "Condom-protected sex": "Секс с презервативом",
            "Raw sex, no creampie or anal": "Без презерватива, но не внутрь и без анала",
            "No limits": "Без ограничений",
            "(partner)": "(партнёр)",
            "%s's BF": "парень {case=gen}%s{/case}",
            "%s's GF": "девушка {case=gen}%s{/case}",
            "Straight": "Натуралка",
            "Party Bi": "Би на вечеринках",
            "Curious": "Любопытная",
            "Sexuality": "Сексуальность",
            "Story": "История",
            "Friendship": "Дружба",
            "NPC Love": "Любовь NPC",
            "Suspicion": "Подозрение",
            "Birth control status discovered": "Ты узнал, предохраняется ли она",
            "Fertility cycle discovered": "Ты узнал её цикл",
            "Safe": "Безопасно",
            "Low risk": "Низкий риск",
            "Fertile": "Фертильна",
            "Peak": "Пик",
            "Away": "В отъезде",
            "Pregnant": "Беременна",
            "Postpartum": "После родов",
            "Recovering after birth. Not fertile right now.": "Восстанавливается после родов. Сейчас не фертильна.",
            "She can't get pregnant.": "Она не может забеременеть.",
            "Early": "Ранний срок",
            "Showing": "Живот заметен",
            "Full belly": "Большой живот",
            "%d day": "%d дн.",
            "%d days": "%d дн.",
            "Away giving birth. Back in %s.": "Уехала рожать. Вернётся через %s.",
            "Day %d": "День %d",
            "Due in %s": "Роды через %s",
            "Day %d of 28": "День %d из 28",
            "Fertile window ends in %s": "Фертильное окно закончится через %s",
            "Fertile window in %s": "Фертильное окно через %s",
            "Birth control: ???": "Контрацепция: ???",
            "Not on the pill": "Не пьёт таблетки",
            "Placebo, 0% (she thinks it's real)": "Плацебо, 0% (она думает, что настоящие)",
            "On the pill, %d%% effective": "Пьёт таблетки, надёжность %d%%",
            "missed: %s": "пропущено: %s",
            "Fertility vitamins": "Витамины для зачатия",
            "Not active": "Не действует",
            "Pills": "Таблетки",
            "Placebo": "Плацебо",
            "Plan B": "Экстренная таблетка",
            "Child support: $%d per week": "Алименты: $%d в неделю",
            "Extra breedable: wider fertile window": "Очень плодовитая: фертильное окно шире",
            "Cycle unknown. Pay attention to her moods when you chat.": "Цикл неизвестен. Следи за её настроением, когда болтаете.",
            "Unknown. Listen for hints when you chat with her.": "Неизвестно. Лови намёки, когда болтаешь с ней.",
            "CYCLE": "ЦИКЛ",
            "STATUS": "СОСТОЯНИЕ",
            "BIRTH CONTROL": "КОНТРАЦЕПЦИЯ",
            "PLAN B": "ЭКСТРЕННАЯ",
            "RISK TODAY": "РИСК СЕГОДНЯ",
            "YOUR SUPPLIES": "ТВОИ ЗАПАСЫ",
            "CHILDREN": "ДЕТИ",
            "Effectiveness": "Надёжность",
            "Used %d of %d": "Использовано %d из %d",
            "She won't take any more for now.": "Больше она пока принимать не будет.",
            "Next dose frees up in %s": "Следующая доза через %s",
            "??? Needs her cycle and her birth control status.": "??? Нужно знать её цикл и как она предохраняется.",
            "Cycle, birth control and risk": "Цикл, контрацепция и риск",
            "Check Fertility in her contact": "Смотри «Фертильность» в её контакте",
            "She started taking the pill": "Она начала пить таблетки",
            "She stopped taking the pill": "Она перестала пить таблетки",
            "Inside": "Внутрь",
            "Pull out": "Вытащить",
            "Children: %d": "Детей: %d",
            "Chit chat with her and listen to what she says after sex. Asking her directly is risky: she may refuse or take offense.": "Болтай с ней и слушай, что она говорит после секса. Спрашивать прямо рискованно: она может отказаться отвечать или обидеться.",
            "Includes your fertility vitamins (x%s).": "С учётом твоих витаминов для зачатия (x%s).",
            "Active x%s, %s left": "Действует x%s, осталось %s",
            "You got her pregnant": "Ты её обрюхатил",
            "Newborn": "Новорождённый",
            "Infant": "Младенец",
            "Baby": "Малыш",
            "Toddler": "Карапуз",
            "Raised by %s": "Растит %s",
            "Next payment in %s": "Следующий платёж через %s",
            "A baby costs money: work": "Ребёнок стоит денег: работай",
            "Many babies, many bills: work": "Много детей, много счетов: работай",
            "Her taste in gifts discovered": "Ты узнал, какие подарки она любит",
            "Loves": "Обожает",
            "Not a fan": "Не в восторге",
            "Personality": "Характер",
            "Relationships": "Отношения",
            "Experience": "Опыт",
            "Lifestyle": "Образ жизни",
            "Hobbies": "Хобби",
            "Kinks": "Фетиши",
            "Orientation": "Ориентация",
            "Partner": "Партнёр",
            "IUD": "Спираль",
            "IUD active after delivery. Protected for now.": "После родов стоит спираль. Пока защищена.",
            "ATM": "ATM",
            "Nerd": "Ботаник",
            "Gym Rat": "Фанатка спортзала",
            "Control": "Контроль",
            "Femdom": "Доминирует",
            "Submissive": "Покорная",
            "Married": "Замужем",
            "Hates Cum": "Ненавидит сперму",
            "Wants to be in charge. Resists acts that put you in control.": "Хочет командовать. Сопротивляется тому, где главный ты.",
            "Likes being told what to do. Gives in to your control easily.": "Любит, когда ей говорят, что делать. Легко отдаёт тебе контроль.",
            "Holds her liquor. Alcohol affects her far less.": "Умеет пить. Алкоголь действует на неё куда слабее.",
            "Low tolerance. Gets drunk fast and sick easily.": "Слабая к алкоголю. Быстро пьянеет, и ей легко становится плохо.",
            "Academically obsessed. Earns double study points and reacts strongly to class disruptions.": "Помешана на учёбе. Получает вдвое больше очков учёбы и остро реагирует, когда срывают занятия.",
            "Lives at the gym. Respects strength, despises weakness.": "Живёт в спортзале. Уважает силу, презирает слабость.",
            "She's married.": "Она замужем.",
            "Loves anal": "Обожает анал",
            "Hates anal": "Ненавидит анал",
            "Can hold her liquor": "Умеет пить",
            "Lightweight drinker": "Быстро пьянеет",
            "Struggling financially": "Туго с деньгами",
            "Wealthy": "Богатая",
            "Breeding kink": "Фетиш на зачатие",
            "Wants to be a mom": "Хочет стать мамой",
            "Terrified of pregnancy": "Боится беременности",
            "Girls Tracker": "Трекер девушек",
            "Instant Pregnancy Test": "Экспресс-тест на беременность",
            "Dressing Room": "Примерочная",
            # Family contact names
            "Dad": "Папа",
        },
    }

    _I18N_EN = {
        "her_obj": "her",
        "Her_obj": "Her",
        "her_poss": "her",
        "Her_poss": "Her",
    }

    def _tr(text):
        """Translate strings from _I18N dict at runtime; a key the language's _I18N lacks falls back to the tl string
        pair of its English text (a value shown through _tr(variable) used to stay English even with a pair)."""
        try:
            lang = renpy.game.preferences.language
        except Exception:
            lang = None
        if lang and lang in _I18N:
            _v = _I18N[lang].get(text)
            if _v is not None:
                return _v
        # a key the language has not translated yet: the English word (never the key), through its tl pair if any
        _en = _I18N_EN.get(text, text)
        return _tl(_en) if (lang and isinstance(_en, str)) else _en

    def _tl(text):
        """Translate a string at runtime using Ren'Py's translate pt strings: table."""
        try:
            return renpy.translation.translate_string(str(text))
        except Exception:
            return str(text)

    def _tl_fmt(template, *args):
        """Translate the TEMPLATE first, then %-format it with positional args (names / pronouns go in
        AFTER the lookup, so the key matches the old/new pair). If the translated string does not take
        the same arguments as the English template, fall back to English instead of crashing."""
        _t = _tl(template)
        if not args:
            return _t
        try:
            return _t % args
        except (TypeError, ValueError) as _e:
            print("[I18N] placeholder mismatch in the translation of %r (%s): English fallback" % (template, _e))
            return str(template) % args

    # ── The keys of a line about one person (her partner, an NPC): ONE builder for every formatter ──
    # English / PT / ES: %(pp)s %(Pp)s %(po)s %(poss)s %(Poss)s (+ %(ga)s, the PT / ES adjective ending). Russian declines,
    # so its translations use the "r_" keys: r_<word>_<case> (cases nom gen dat acc ins pre) and the endings below.
    # They exist in every language (an English line never uses them). docs/translation_ru.md lists them.
    RU_GENDER_FORMS = {
        # the person: он / она; "non" = after a preposition (с ним / с ней, о нём / о ней, у него / у неё)
        "on": ({"nom": "он", "gen": "его", "dat": "ему", "acc": "его", "ins": "им", "pre": "нём"},
               {"nom": "она", "gen": "её", "dat": "ей", "acc": "её", "ins": "ей", "pre": "ней"}),
        "non": ({"nom": "он", "gen": "него", "dat": "нему", "acc": "него", "ins": "ним", "pre": "нём"},
                {"nom": "она", "gen": "неё", "dat": "ней", "acc": "неё", "ins": "ней", "pre": "ней"}),
    }
    RU_GENDER_ENDINGS = {           # (him, her)
        "r_a": ("", "а"),            # past tense, short adjective: видел%(r_a)s, рад%(r_a)s
        "r_sya": ("ся", "ась"),      # reflexive past: вернул%(r_sya)s
        "r_yi": ("ый", "ая"),        # ревнив%(r_yi)s
        "r_ii": ("ий", "ая"),        # хорош%(r_ii)s
        "r_oi": ("ой", "ая"),        # друг%(r_oi)s
    }
    # the partner noun (boyfriend = парень, girlfriend = девушка) and the possessives that agree with it
    RU_PARTNER_FORMS = {
        "pl": ({"nom": "парень", "gen": "парня", "dat": "парню", "acc": "парня", "ins": "парнем", "pre": "парне"},
               {"nom": "девушка", "gen": "девушки", "dat": "девушке", "acc": "девушку", "ins": "девушкой", "pre": "девушке"}),
        "moi": ({"nom": "мой", "gen": "моего", "dat": "моему", "acc": "моего", "ins": "моим", "pre": "моём"},
                {"nom": "моя", "gen": "моей", "dat": "моей", "acc": "мою", "ins": "моей", "pre": "моей"}),
        "tvoi": ({"nom": "твой", "gen": "твоего", "dat": "твоему", "acc": "твоего", "ins": "твоим", "pre": "твоём"},
                 {"nom": "твоя", "gen": "твоей", "dat": "твоей", "acc": "твою", "ins": "твоей", "pre": "твоей"}),
        "svoi": ({"nom": "свой", "gen": "своего", "dat": "своему", "acc": "своего", "ins": "своим", "pre": "своём"},
                 {"nom": "своя", "gen": "своей", "dat": "своей", "acc": "свою", "ins": "своей", "pre": "своей"}),
    }

    def _ru_forms(table, female):
        return dict(("r_%s_%s" % (_w, _c), _f) for _w, _forms in table.items() for _c, _f in _forms[1 if female else 0].items())

    def gender_fmt(female):
        """The keys about one person, he or she: every formatter of lines about a partner or an NPC starts here."""
        _f = bool(female)
        _d = {
            "pp": _tr("she") if _f else _tr("he"),
            "Pp": _tr("She") if _f else _tr("He"),
            "po": _tr("her_obj") if _f else _tr("him"),
            "poss": _tr("her_poss") if _f else _tr("his"),
            "Poss": _tr("Her_poss") if _f else _tr("His"),
            "ga": "a" if _f else "o",
        }
        _d.update(_ru_forms(RU_GENDER_FORMS, _f))
        for _k, _pair in RU_GENDER_ENDINGS.items():
            _d[_k] = _pair[1 if _f else 0]
        return _d

    def partner_label_fmt(female, label=None):
        """The keys about the partner noun (boyfriend / girlfriend) and the words that agree with it."""
        _f = bool(female)
        _pl = label if label is not None else (_tr("girlfriend") if _f else _tr("boyfriend"))
        _d = {
            "pl": _pl, "Pl": _pl.capitalize(), "PL": _pl.upper(), "gn": _pl, "partner": _pl,
            "do": "da" if _f else "do", "Do": "Da" if _f else "Do",
            "meu": "minha" if _f else "meu", "Meu": "Minha" if _f else "Meu",
        }
        _d.update(_ru_forms(RU_PARTNER_FORMS, _f))
        return _d

    def fmt_safe(text, keys, english=None):
        """text % keys; a translation whose keys do not fit falls back to the English line (never a crash)."""
        try:
            return text % keys
        except (KeyError, ValueError, TypeError) as _e:
            print("[I18N] keys of %r do not fit (%s): English fallback" % (text, _e))
        if english is not None and english != text:
            try:
                return str(english) % keys if "%(" in str(english) else str(english)
            except (KeyError, ValueError, TypeError):
                pass
        return str(english if english is not None else text)

    renpy._orig_tr = _tr
    renpy._orig_tl = _tl
    # The translation marker itself: a label-level "_, x = f()" rebinds store._ to a plain value and the save keeps it.
    renpy._orig_underscore = _

    _TRAIT_VERBAL = {
        "camera_lover": _("She loves being on camera"),
        "camera_hater": _("She hates cameras"),
        "cum_slut": _("She loves cum"),
        "hate_cum": _("She hates cum"),
        "public_fetish": _("She likes doing it in public"),
        "public_shy": _("She's terrified of public exposure"),
        "hardcore_sex": _("She likes it rough"),
        "cute_sex": _("She likes it gentle"),
        "femdom": _("She likes to be in charge"),
        "submissive": _("She likes being told what to do"),
        "loyal": _("She's very loyal"),
        "cheater": _("She's open to cheating"),
        "naive": _("She's completely inexperienced"),
        "virgin": _("She's a virgin"),
        "voyeur": _("She likes watching others"),
        "exhibitionist": _("She likes being watched"),
        "polyamorous": _("She's open to sharing her partner"),
        "monogamous": _("She demands exclusivity"),
        "has_boyfriend": _("She already has a boyfriend"),
        "has_girlfriend": _("She already has a girlfriend"),
        "married": _("She's married"),
        "experienced": _("She has done everything with her partner"),
        "anal_lover": _("She loves anal"),
        "anal_hater": _("She hates anal"),
        "lesbian": _("She's only attracted to women"),
        "bisexual": _("She's attracted to both men and women"),
        "poor": _("She struggles financially"),
        "rich": _("She comes from a wealthy background"),
        "heavy_drinker": _("She can hold her liquor"),
        "lightweight": _("She can't handle her drinks"),
        "nerd": _("She's a total bookworm"),
        "gym_rat": _("She lives at the gym"),
        "breedable": _("Extra breedable"),
        "infertile": _("Infertile"),
        "pregnancy_fetish": _("She has a pregnancy fetish"),
        "pregnancy_fear": _("She's terrified of getting pregnant"),
    }

    def _trait_list_for(girl):
        """Return list of trait names assigned to a girl."""
        assigned = [t for pair in TRAIT_PAIRS for t in (pair["a"], pair["b"]) if girl.has_trait(t)]
        assigned += [st["id"] for st in SYSTEM_TRAITS if st.get("on_add") not in ("set_npc_partner", "set_npc_partner_female") and girl.has_trait(st["id"])]
        if girl.has_npc_partner():
            if girl.get_flag("partner_is_female"):
                assigned.append("has_girlfriend")
            else:
                assigned.append("has_boyfriend")
        return assigned

    def _trait_list_verbal(girl):
        """Return list of verbal trait descriptions for a girl, translated (_pk_t: the tl pair, else _I18N; the newer
        lines like femdom / submissive / married only have a pair). They go into formatted lines, so translated here."""
        ids = _trait_list_for(girl)
        verbal = []
        for t in ids:
            if t == "has_boyfriend" and girl.get_flag("partner_is_female"):
                verbal.append(_pk_t("She already has a girlfriend"))
            else:
                verbal.append(_pk_t(_TRAIT_VERBAL.get(t, t)))
        return verbal


    def _randomize_remaining_traits(selected, opposites, target=3, girl=None):
        """Add random traits until we reach `target`, respecting opposites
        AND SYSTEM_TRAITS conflicts (and, with a girl, what she can never have).
        If already at or above target, add exactly 1."""
        need = max(1, target - len(selected))

        def _is_blocked(tid, sel):
            if girl is not None and trait_blocked_for(girl, tid):
                return True
            opp = opposites.get(tid)
            if opp and opp in sel:
                return True
            for c in _get_system_conflicts(tid):
                if c in sel:
                    return True
            for other in sel:
                if tid in _get_system_conflicts(other):
                    return True
            if tid == "cum_slut" and "lesbian" in sel:
                return True
            if tid in ("lesbian", "has_girlfriend") and "cum_slut" in sel and "bisexual" not in sel:
                return True
            return False

        pool = []
        for pair in TRAIT_PAIRS:
            if pair["a"] not in selected and not _is_blocked(pair["a"], selected):
                pool.append(pair["a"])
            if pair["b"] not in selected and not _is_blocked(pair["b"], selected):
                pool.append(pair["b"])
        for st in SYSTEM_TRAITS:
            if st["id"] not in selected and not _is_blocked(st["id"], selected):
                pool.append(st["id"])

        renpy.random.shuffle(pool)
        added = 0
        for tid in pool:
            if added >= need:
                break
            if _is_blocked(tid, selected):
                continue
            selected.add(tid)
            if tid == "lesbian":
                selected.discard("has_boyfriend")
                selected.discard("bisexual")
                if "pregnancy_fetish" not in selected:
                    selected.discard("cum_slut")
                    selected.add("hate_cum")
            elif tid == "has_girlfriend" and "bisexual" not in selected:
                selected.add("lesbian")
                selected.discard("has_boyfriend")
                if "pregnancy_fetish" not in selected:
                    selected.discard("cum_slut")
                    selected.add("hate_cum")
            elif tid == "bisexual":
                selected.discard("lesbian")
            elif tid == "naive":
                selected.add("virgin")
            added += 1

    def _apply_naive(girl):
        girl.add_trait("naive")
        if not girl.has_trait("virgin"):
            girl.add_trait("virgin")
        girl.set_flag("virgin", True)
        girl.virginity_taken_by_player = False
        girl.bf_max_tier = 0
        girl.bf_history = {
            "hj": False, "masturbate": False, "tj": False,
            "bj": False, "sex": False, "sex_raw": False, "creampie": False,
        }
        girl.player_firsts = {}
        girl.Sex_acts = {k: 0 for k in _SEX_ACT_KEYS}
        debug_log("[NAIVE] %s: zero sexual history, virgin forced" % girl.gid)

    def _apply_experienced(girl):
        girl.add_trait("experienced")
        if girl.has_trait("virgin"):
            girl.remove_trait("virgin")
        girl.intimacy_flags = set()
        girl.Sex_acts = {k: 0 for k in _SEX_ACT_KEYS}
        girl.set_flag("virgin", False)
        girl.virginity_taken_by_player = False
        if girl.has_trait("lesbian"):
            girl.bf_history = {
                "kiss": True, "masturbate": True,
            }
        else:
            girl.bf_history = {
                "kiss": True, "hj": True, "masturbate": True, "tj": True,
                "bj": True, "rub": True, "tip": True,
                "cowgirl": True, "reverse_cowgirl": True, "doggy": True,
                "sex": True, "sex_raw": True, "anal": True,
                "creampie": True,
            }
        girl.player_firsts = {}
        debug_log("[EXPERIENCED] %s: NPC history in bf_history only, Sex_acts starts at zero (player-only), lesbian=%s" % (girl.gid, girl.has_trait("lesbian")))

    def _get_system_conflicts(tid):
        for s in SYSTEM_TRAITS:
            if s["id"] == tid:
                return s.get("conflicts", [])
        return []

    class _FrozenGuardSet(set):
        """A set that silently prevents removing elements in a frozen set."""
        def __init__(self, data, frozen):
            set.__init__(self, data)
            self._frozen = frozenset(frozen) if frozen else frozenset()
        def discard(self, elem):
            if elem not in self._frozen:
                set.discard(self, elem)
        def remove(self, elem):
            if elem not in self._frozen:
                set.remove(self, elem)
        def pop(self):
            for elem in self:
                if elem not in self._frozen:
                    set.discard(self, elem)
                    return elem
            raise KeyError("pop from frozen-only set")
        def clear(self):
            for elem in list(self):
                if elem not in self._frozen:
                    set.discard(self, elem)
        def difference_update(self, *others):
            to_remove = set()
            for o in others:
                to_remove.update(o)
            for elem in to_remove:
                if elem not in self._frozen:
                    set.discard(self, elem)
        def __isub__(self, other):
            self.difference_update(other)
            return self

    def _trait_manual_pick(girl, opposites, frozen=None):
        """Run the manual trait picker loop for one girl.
        frozen: set of trait IDs that cannot be removed/added (review mode).
        Returns set of newly added traits when frozen, else None."""
        _canon_traits = set(GIRLS_CONFIG.get(girl.gid, {}).get("traits", []))
        _locked = _canon_traits | (frozen or set())
        if frozen is not None:
            _girl_cur = set(tid for tid in _all_trait_ids() if girl.has_trait(tid))
            selected = _FrozenGuardSet(_girl_cur, frozen)
            print("[PICK] %s: REVIEW MODE  girl_traits=%r  frozen_count=%d  type(frozen)=%s" % (girl.gid, _girl_cur, len(frozen), type(frozen).__name__))
        else:
            selected = set(_canon_traits)
        done = False
        _tp_adj = ui.adjustment()
        store._tp_active_tab = "preferences"

        while not done:
            result = renpy.call_screen("trait_picker", girl=girl, selected=selected, opposites=opposites,
                                        vp_adj=_tp_adj, frozen=frozen)

            if frozen is not None:
                print("[PICK] %s: screen returned %r  in_frozen=%s  in_locked=%s" % (girl.gid, result, result in (frozen or set()), result in _locked))
            if result == "_done":
                done = True
            elif result == "_randomize":
                _randomize_remaining_traits(selected, opposites, target=3, girl=girl)
            elif result in selected:
                if result in _locked:
                    continue
                if result == "hate_cum" and "lesbian" in selected and "pregnancy_fetish" not in selected:
                    continue
                if result == "cum_slut" and "pregnancy_fetish" in selected:
                    continue
                if result == "virgin" and "naive" in selected:
                    continue
                selected.discard(result)
                if result == "lesbian":
                    selected.discard("hate_cum")
                    if "has_girlfriend" in selected and "bisexual" not in selected:
                        selected.add("bisexual")
                elif result == "bisexual" and "has_girlfriend" in selected:
                    selected.add("lesbian")
                    if "pregnancy_fetish" not in selected:
                        selected.add("hate_cum")
                        selected.discard("cum_slut")
                elif result == "naive":
                    pass
            else:
                opp = opposites.get(result)
                if opp:
                    selected.discard(opp)
                conflicts = _get_system_conflicts(result)
                for c in conflicts:
                    selected.discard(c)
                for other in list(selected):
                    if result in _get_system_conflicts(other):
                        selected.discard(other)
                if result == "cum_slut" and "lesbian" in selected and "pregnancy_fetish" not in selected:
                    continue
                selected.add(result)
                if result == "lesbian":
                    selected.discard("has_boyfriend")
                    selected.discard("bisexual")
                    if "pregnancy_fetish" not in selected:
                        selected.discard("cum_slut")
                        selected.add("hate_cum")
                elif result == "has_girlfriend":
                    selected.discard("has_boyfriend")
                    if "lesbian" not in selected and "bisexual" not in selected:
                        selected.add("bisexual")
                elif result == "bisexual":
                    if "lesbian" in selected:
                        selected.discard("hate_cum")
                    selected.discard("lesbian")
                elif result == "naive":
                    selected.add("virgin")
                elif result == "pregnancy_fetish":
                    selected.discard("hate_cum")
                    selected.add("cum_slut")

        # Safety net: has_girlfriend requires lesbian or bisexual
        if "has_girlfriend" in selected and "lesbian" not in selected and "bisexual" not in selected:
            selected.add("lesbian")
            if "pregnancy_fetish" not in selected:
                selected.add("hate_cum")
            selected.discard("cum_slut")

        if frozen is not None:
            _added = set(selected) - frozen
            for tid in sorted(_added, key=lambda t: 2 if t in ("experienced", "naive") else 0):
                st_match = [s for s in SYSTEM_TRAITS if s["id"] == tid]
                _on_add = st_match[0].get("on_add") if st_match else None
                if _on_add == "set_npc_partner":
                    girl.add_trait(tid)
                    girl.set_npc_partner("npc_bf_%s" % girl.gid)
                elif _on_add == "set_npc_partner_female":
                    girl.add_trait(tid)
                    girl.set_npc_partner_female("npc_gf_%s" % girl.gid)
                elif _on_add in ("set_experienced", "set_naive"):
                    girl.add_trait(tid)
                    if tid == "naive" and not girl.has_trait("virgin"):
                        girl.add_trait("virgin")
                    elif tid == "experienced" and girl.has_trait("virgin"):
                        girl.remove_trait("virgin")
                    print("[REVIEW] %s: added %s (mid-game, stat effects skipped)" % (girl.gid, tid))
                else:
                    girl.add_trait(tid)
                    print("[REVIEW] %s: added trait %s" % (girl.gid, tid))
            enforce_canon_traits(girl, "review")
            _apply_gym_rat_schedule(girl)
            return _added
        else:
            _clear_girl_traits(girl)
            for tid in sorted(selected, key=lambda t: 2 if t in ("experienced", "naive") else 0):
                st_match = [s for s in SYSTEM_TRAITS if s["id"] == tid]
                if st_match and st_match[0].get("on_add") == "set_npc_partner":
                    girl.add_trait(tid)
                    girl.set_npc_partner("npc_bf_%s" % girl.gid)
                elif st_match and st_match[0].get("on_add") == "set_npc_partner_female":
                    girl.add_trait(tid)
                    girl.set_npc_partner_female("npc_gf_%s" % girl.gid)
                elif st_match and st_match[0].get("on_add") == "set_experienced":
                    girl.add_trait(tid)
                    _apply_experienced(girl)
                elif st_match and st_match[0].get("on_add") == "set_naive":
                    girl.add_trait(tid)
                    _apply_naive(girl)
                else:
                    girl.add_trait(tid)
            enforce_canon_traits(girl, "manual_pick", fresh=True)
            _apply_gym_rat_schedule(girl)
            return None


label _trait_show_summary:
    python:
        for _g in ALL_GIRLS:
            _verbal = _trait_list_verbal(_g)
            if _verbal:
                _trait_str = ". ".join(_verbal) + "."
                renpy.say(None, "{b}%s{/b}: %s" % (_g.Name, _trait_str))
            else:
                renpy.say(None, _tl(_("%s: No personality traits.")) % _g.Name)
    return


# ============================================================
# NEW CONTENT REVIEW — trait review for updated saves
# ============================================================

default _known_trait_ids = None
default _known_girl_gids = None

init python:

    def _all_trait_ids():
        _ids = set()
        for _p in TRAIT_PAIRS:
            _ids.add(_p["a"])
            _ids.add(_p["b"])
        for _s in SYSTEM_TRAITS:
            _ids.add(_s["id"])
        return _ids

    def _stamp_known_content():
        store._known_trait_ids = _all_trait_ids()
        store._known_girl_gids = set(g.gid for g in ALL_GIRLS)
        print("[REVIEW] Stamped known content: %d traits, %d girls" % (
            len(store._known_trait_ids), len(store._known_girl_gids)))

    def _has_offerable_traits(girl, frozen, opposites):
        """True if the girl has at least one non-frozen, non-conflicting trait she could add."""
        _girl_cur = set(tid for tid in _all_trait_ids() if girl.has_trait(tid))
        for _p in TRAIT_PAIRS:
            for _tid in (_p["a"], _p["b"]):
                if _tid not in frozen:
                    _st, _ = _tp_btn_state(_tid, _girl_cur, opposites, girl, frozen)
                    if _st in ("normal",):
                        return True
        for _s in SYSTEM_TRAITS:
            _tid = _s["id"]
            if _tid not in frozen:
                _st, _ = _tp_btn_state(_tid, _girl_cur, opposites, girl, frozen)
                if _st in ("normal",):
                    return True
        return False

label _new_content_review:

    # NEVER a loop variable named like an init function in a label python block (it was _p, the player image helper):
    # the rollback log keeps the old function and every save within that window fails to pickle it.
    python:
        _ncr_opposites = {}
        for _ncr_pair in TRAIT_PAIRS:
            _ncr_opposites[_ncr_pair["a"]] = _ncr_pair["b"]
            _ncr_opposites[_ncr_pair["b"]] = _ncr_pair["a"]

    python:
        _ncr_old_known = getattr(store, "_known_trait_ids", None)
        _ncr_all_ids = _all_trait_ids()
        if _ncr_old_known is not None:
            _ncr_new_trait_ids = _ncr_all_ids - _ncr_old_known
        else:
            _ncr_new_trait_ids = set(_NEW_TRAITS_THIS_VERSION)
        print("[REVIEW] new trait IDs for this update: %r  (old_known=%s)" % (_ncr_new_trait_ids, "set(%d)" % len(_ncr_old_known) if _ncr_old_known is not None else "None"))

        _ncr_known_girls = getattr(store, "_known_girl_gids", None)
        _ncr_any_added = False
        for _ncr_g in ALL_GIRLS:
            # A girl this save never had gets the whole picker: only her canon and what she can't have stay locked
            _ncr_new_girl = _ncr_known_girls is not None and _ncr_g.gid not in _ncr_known_girls
            if _ncr_new_girl:
                _ncr_frozen = set()
            else:
                _ncr_frozen = _ncr_all_ids - _ncr_new_trait_ids
                for _tid in _ncr_new_trait_ids:
                    if _ncr_g.has_trait(_tid):
                        _ncr_frozen.add(_tid)

            print("[REVIEW] %s: new_girl=%s girl_traits=%r  frozen=%d  available=%r" % (_ncr_g.gid, _ncr_new_girl, getattr(_ncr_g, "traits", None), len(_ncr_frozen), _ncr_new_trait_ids - _ncr_frozen))
            if not _has_offerable_traits(_ncr_g, _ncr_frozen, _ncr_opposites):
                print("[REVIEW] %s: no offerable traits, skipping" % _ncr_g.gid)
                continue

            if _ncr_new_girl:
                renpy.say(None, _tl_fmt(_("{b}%s{/b} is new in this version. Choose her traits."), _ncr_g.Name))
            else:
                _ncr_avail = sorted(_t for _t in _ncr_new_trait_ids - _ncr_frozen if not trait_blocked_for(_ncr_g, _t))
                _ncr_id_to_label = {}
                for _ncr_pair in TRAIT_PAIRS:
                    _ncr_id_to_label[_ncr_pair["a"]] = _ncr_pair["a_label"]
                    _ncr_id_to_label[_ncr_pair["b"]] = _ncr_pair["b_label"]
                for _s in SYSTEM_TRAITS:
                    _ncr_id_to_label[_s["id"]] = _s["label"]
                _ncr_avail_str = ", ".join(_tr(_ncr_id_to_label.get(_t, _t)) for _t in _ncr_avail) if _ncr_avail else "none"
                renpy.say(None, _tl_fmt(_("New traits available for {b}%s{/b}: {b}%s{/b}. All other traits are locked."), _ncr_g.Name, _ncr_avail_str))
            _ncr_added = _trait_manual_pick(_ncr_g, _ncr_opposites, frozen=_ncr_frozen)
            if _ncr_added:
                _ncr_any_added = True
                _verbal = _trait_list_verbal(_ncr_g)
                _trait_str = ". ".join(_verbal) + "." if _verbal else _tl(_("No traits."))
                renpy.say(None, _tl_fmt(_("{b}%s{/b} updated: %s"), _ncr_g.Name, _trait_str))
            else:
                renpy.say(None, _tl_fmt(_("{b}%s{/b}: No changes."), _ncr_g.Name))

    if _pregnancy_mode == "off":
        $ renpy.say(None, _tl(_("The {b}Pregnancy{/b} system is currently disabled. Would you like to enable it?")))
        menu:
            "Review pregnancy settings":
                call _pregnancy_setup from _call_pregnancy_setup_review
                if _pregnancy_mode != "off":
                    python:
                        for _ips_girl in ALL_GIRLS:
                            _pregnancy_init_pill_state(_ips_girl)
            "Keep pregnancy disabled":
                pass
    else:
        $ renpy.say(None, _tl_fmt(_("Your pregnancy mode is currently {b}%s{/b}. Would you like to change it?"), _tl({"full": _("FULL"), "lite": _("LITE"), "off": _("OFF")}.get(_pregnancy_mode, _pregnancy_mode))))
        menu:
            "Change pregnancy settings":
                call _pregnancy_setup from _call_pregnancy_setup_review2
                python:
                    for _ips_girl in ALL_GIRLS:
                        _pregnancy_init_pill_state(_ips_girl)
            "Keep current settings":
                pass

    $ _stamp_known_content()
    $ _girl_save = _snapshot_girls()

    $ renpy.say(None, _tl(_("Review complete. Your stats and progress are intact.")))
    return


# ============================================================
# TRAIT PICKER SCREEN — card-based tabbed UI.
# Three tabs: Preferences, Personality, Relationships.
# Data driven by _TRAIT_TABS / _PAIRS_BY_CAT / _SYS_BY_ID.
# Uses pk_pill / pk_card_bg from the phone UI kit.
# ============================================================

define _NEW_TRAITS_THIS_VERSION = {"femdom", "submissive", "married"}
default _tp_active_tab = "preferences"

init python:
    _TP_ACCENT = "#7dd3fc"
    _TP_MUTED  = "#8ca0b4"
    _TP_DIM    = "#555e6e"
    _TP_TEXT   = "#e2e8f0"
    _TP_LOCK_C = "#d946ef"
    _TP_CANON_C = "#e879f9"
    _TP_NEW_C  = "#fbbf24"
    _TP_PANEL  = "#0d1526"

    _TP_BTN_BG = {
        "canon":      ("#e879f9", 0.12),
        "frozen":     ("#94a3b8", 0.14),
        "locked":     ("#d946ef", 0.10),
        "locked_sel": ("#7dd3fc", 0.15),
        "blocked":    ("#ffffff", 0.03),
        "selected":   ("#7dd3fc", 0.22),
        "normal":     ("#ffffff", 0.06),
    }
    _TP_NAME_C = {
        "canon": "#e879f9", "frozen": "#94a3b8", "locked": "#555e6e", "locked_sel": "#7dd3fc",
        "blocked": "#555e6e", "selected": "#7dd3fc", "normal": "#e2e8f0",
    }

    _TP_MOBILE = renpy.variant("mobile")
    _TP_PNL_W = 1800 if _TP_MOBILE else 1200
    _TP_VP_W = _TP_PNL_W - 48
    _TP_VP_H = 750 if _TP_MOBILE else 680
    _TP_TAB_AREA = _TP_PNL_W - 40
    _TP_PAIR_BW = (_TP_VP_W - 36) // 2
    _TP_FULL_BW = _TP_VP_W - 52
    _TP_TAB_H = 70 if _TP_MOBILE else 44
    _TP_FS_TITLE = 32 if _TP_MOBILE else 20
    _TP_FS_TAB = 26 if _TP_MOBILE else 16
    _TP_FS_SEC = 22 if _TP_MOBILE else 17
    _TP_FS_CAT = 18 if _TP_MOBILE else 14
    _TP_FS_NAME = 26 if _TP_MOBILE else 19
    _TP_FS_DESC = 20 if _TP_MOBILE else 15
    _TP_FS_BADGE = 16 if _TP_MOBILE else 13
    _TP_FS_BTN = 24 if _TP_MOBILE else 17
    _TP_BTN_PAD = (20, 14, 20, 14) if _TP_MOBILE else (16, 12, 16, 12)

    _NTP_PNL_W = 1800 if _TP_MOBILE else 1000
    _NTP_COL_W = 850 if _TP_MOBILE else 470
    _NTP_VP_H = 700 if _TP_MOBILE else 520
    _NTP_FS_TITLE = 30 if _TP_MOBILE else 19
    _NTP_FS_HDR = 26 if _TP_MOBILE else 16
    _NTP_FS_BODY = 22 if _TP_MOBILE else 14
    _NTP_INLINE_SZ = 24 if _TP_MOBILE else 16

screen _tp_trait_btn(tid, label, desc, state, hint, is_new, btn_w):
    $ _tbc, _tba = _TP_BTN_BG.get(state, ("#ffffff", 0.06))
    $ _tnc = _TP_NAME_C.get(state, _TP_TEXT)
    $ _active = state in ("selected", "normal")

    button:
        xsize btn_w
        padding _TP_BTN_PAD
        background _pk_pill(_tbc, _tba)
        hover_background (_pk_pill(_tbc, min(_tba + 0.12, 1.0)) if _active else _pk_pill(_tbc, _tba))
        action (Return(tid) if _active else NullAction())
        sensitive _active

        vbox:
            spacing 3

            hbox:
                spacing 6
                yalign 0.5

                text label:
                    size _TP_FS_NAME
                    bold True
                    color _tnc
                    font "fonts/WorkSans-Bold.ttf"

                if is_new:
                    frame:
                        padding (6, 2, 6, 2)
                        yalign 0.5
                        background _pk_pill(_TP_NEW_C, 0.22)
                        text _("NEW"):
                            size _TP_FS_BADGE
                            bold True
                            color _TP_NEW_C
                            font "fonts/WorkSans-Bold.ttf"

                if state == "canon":
                    frame:
                        padding (6, 2, 6, 2)
                        yalign 0.5
                        background _pk_pill(_TP_CANON_C, 0.18)
                        text _("Canon"):
                            size _TP_FS_BADGE
                            bold True
                            color _TP_CANON_C
                            font "fonts/WorkSans-Bold.ttf"

                if state == "frozen":
                    frame:
                        padding (6, 2, 6, 2)
                        yalign 0.5
                        background _pk_pill("#94a3b8", 0.18)
                        text _("LOCKED"):
                            size _TP_FS_BADGE
                            bold True
                            color "#94a3b8"
                            font "fonts/WorkSans-Bold.ttf"

            if state in ("locked", "locked_sel", "blocked") and hint:
                text hint:
                    size _TP_FS_DESC
                    color (_TP_LOCK_C if state in ("locked", "locked_sel") else _TP_DIM)
                    font "fonts/WorkSans-Regular.ttf"
            elif state == "frozen" and desc:
                text desc:
                    size _TP_FS_DESC
                    color _TP_DIM
                    font "fonts/WorkSans-Regular.ttf"
            elif _active and desc:
                text desc:
                    size _TP_FS_DESC
                    color _TP_MUTED
                    font "fonts/WorkSans-Regular.ttf"


screen trait_picker(girl, selected, opposites, vp_adj=None, frozen=None):
    modal True
    zorder 200

    default _tp_tab = store._tp_active_tab
    default _tp_frozen_logged = False
    if not _tp_frozen_logged and frozen is not None:
        $ _tp_frozen_logged = True
        $ print("[SCREEN] trait_picker: frozen=%r type=%s len=%d" % (frozen, type(frozen).__name__, len(frozen)))

    frame:
        align (0.5, 0.5)
        xminimum _TP_PNL_W
        xmaximum _TP_PNL_W
        padding (20, 16)
        background _pk_pill(_TP_PANEL, 1.0)

        vbox:
            spacing 8

            # --- Header ---
            hbox:
                xfill True
                yalign 0.5

                hbox:
                    spacing 10
                    yalign 0.5

                    frame:
                        background _TP_ACCENT
                        xsize 3
                        ysize 24
                        yalign 0.5

                    text "%s - [girl.Name]" % _tr("TRAITS"):
                        size _TP_FS_TITLE
                        color _TP_ACCENT
                        font "fonts/WorkSans-Bold.ttf"
                        outlines [(1, "#06101e", 0, 0)]
                        yalign 0.5

                hbox:
                    xalign 1.0
                    spacing 10
                    yalign 0.5

                    $ _tp_avatar = _girl_avatar_by_gid(girl.gid)
                    add _tp_avatar:
                        yalign 0.5

            # --- Tab bar ---
            frame:
                xfill True
                ysize _TP_TAB_H
                padding (0, 0)
                background _pk_pill("#0b1220", 1.0)

                hbox:
                    for _tab_def in _TRAIT_TABS:
                        $ _tab_key = _tab_def["label"].lower()
                        $ _tab_active = _tp_tab == _tab_key
                        button:
                            xsize int(_TP_TAB_AREA / len(_TRAIT_TABS))
                            ysize _TP_TAB_H
                            padding (0, 0)
                            background None
                            hover_background "#ffffff0a"
                            action [SetScreenVariable("_tp_tab", _tab_key), SetVariable("_tp_active_tab", _tab_key)]

                            text _tr(_tab_def["label"]):
                                size _TP_FS_TAB
                                bold True
                                font "fonts/WorkSans-Bold.ttf"
                                color (_TP_ACCENT if _tab_active else _TP_MUTED)
                                xalign 0.5
                                yalign 0.42

                            if _tab_active:
                                frame:
                                    xsize 64
                                    ysize 4
                                    xalign 0.5
                                    yalign 1.0
                                    padding (0, 0)
                                    background _pk_pill(_TP_ACCENT)

            # --- Scrollable content ---
            hbox:
                spacing 4
                viewport id "trait_content_vp":
                    mousewheel True
                    draggable True
                    ymaximum _TP_VP_H
                    xsize _TP_VP_W
                    if vp_adj is not None:
                        yadjustment vp_adj

                    vbox:
                        spacing 12
                        xsize _TP_VP_W

                        $ _tp_cur = [t for t in _TRAIT_TABS if t["label"].lower() == _tp_tab][0]

                        for _sec in _tp_cur["sections"]:

                            # --- Section card ---
                            frame:
                                xfill True
                                padding (14, 12, 14, 14)
                                background _pk_card_bg()

                                vbox:
                                    spacing 10
                                    xfill True

                                    text _tr(_sec["header"]):
                                        size _TP_FS_SEC
                                        bold True
                                        color _TP_ACCENT
                                        font "fonts/WorkSans-Bold.ttf"

                                    # Pair traits: two buttons side by side
                                    if "pairs" in _sec:
                                        for _tp_cat in _sec["pairs"]:
                                            $ _tp_pair = _PAIRS_BY_CAT[_tp_cat]
                                            $ _tp_a = _tp_pair["a"]
                                            $ _tp_b = _tp_pair["b"]
                                            $ _tp_a_st, _tp_a_hint = _tp_btn_state(_tp_a, selected, opposites, girl, frozen)
                                            $ _tp_b_st, _tp_b_hint = _tp_btn_state(_tp_b, selected, opposites, girl, frozen)
                                            $ _tp_a_new = _tp_a in _NEW_TRAITS_THIS_VERSION and _tp_a_st not in ("canon", "frozen")
                                            $ _tp_b_new = _tp_b in _NEW_TRAITS_THIS_VERSION and _tp_b_st not in ("canon", "frozen")

                                            if len(_sec["pairs"]) > 1:
                                                text _tr(_tp_cat):
                                                    size _TP_FS_CAT
                                                    color _TP_DIM
                                                    font "fonts/WorkSans-Bold.ttf"

                                            hbox:
                                                spacing 8
                                                use _tp_trait_btn(_tp_a, _tr(_tp_pair["a_label"]), _tr(_tp_pair["a_desc"]), _tp_a_st, _tp_a_hint, _tp_a_new, _TP_PAIR_BW)
                                                use _tp_trait_btn(_tp_b, _tr(_tp_pair["b_label"]), _tr(_tp_pair["b_desc"]), _tp_b_st, _tp_b_hint, _tp_b_new, _TP_PAIR_BW)

                                    # Toggle traits: full-width buttons
                                    if "toggles" in _sec:
                                        for _tp_tid in _sec["toggles"]:
                                            $ _tp_sys = _SYS_BY_ID[_tp_tid]
                                            $ _tp_t_st, _tp_t_hint = _tp_btn_state(_tp_tid, selected, opposites, girl, frozen)
                                            $ _tp_t_new = _tp_tid in _NEW_TRAITS_THIS_VERSION and _tp_t_st not in ("canon", "frozen")
                                            use _tp_trait_btn(_tp_tid, _tr(_tp_sys["label"]), _tr(_tp_sys["desc"]), _tp_t_st, _tp_t_hint, _tp_t_new, _TP_FULL_BW)

                vbar value YScrollValue("trait_content_vp"):
                    xsize 4
                    ymaximum _TP_VP_H
                    base_bar Solid("#1a2540")
                    thumb _pk_pill(_TP_ACCENT, 0.6)
                    thumb_offset 0

            # --- Bottom bar: Randomize + Done ---
            hbox:
                spacing 12
                xalign 0.5

                if frozen is None:
                    button:
                        padding (20, 10, 20, 10)
                        background _pk_pill("#ffffff", 0.06)
                        hover_background _pk_pill("#ffffff", 0.14)
                        action Return("_randomize")
                        text _tr("Randomize the rest (fill to 3)"):
                            size _TP_FS_BTN
                            color _TP_TEXT
                            font "fonts/WorkSans-Bold.ttf"

                button:
                    padding (40, 10, 40, 10)
                    background _pk_pill(_TP_ACCENT, 0.22)
                    hover_background _pk_pill(_TP_ACCENT, 0.38)
                    action Return("_done")
                    text _tr("Done"):
                        size _TP_FS_BTN
                        bold True
                        color _TP_ACCENT
                        font "fonts/WorkSans-Bold.ttf"


# ============================================================
# NPC PARTNER TRAIT PICKER SCREEN
# ============================================================

init python:

    def _npc_trait_manual_pick(girl):
        _pl = _tr("girlfriend") if girl.get_flag("partner_is_female") else _tr("boyfriend")
        _gender = "female" if girl.get_flag("partner_is_female") else "male"
        _is_lesbian = girl.has_trait("lesbian")

        _selected = set()
        _boundary = [0]

        _done = False
        while not _done:
            result = renpy.call_screen("npc_trait_picker",
                girl=girl, partner_label=_pl, selected=_selected,
                boundary_level=_boundary[0], is_lesbian=_is_lesbian)

            if result == "_done":
                _done = True
            elif result == "_randomize":
                _selected.clear()
                _selected.update(_npc_roll_partner_traits())   # same roll as a random partner (create_npc_partner)
                if "ntr" in _selected and not _is_lesbian:
                    _boundary[0] = _ntr_roll_boundary_level(_gender)
                else:
                    _boundary[0] = 0
            elif result == "ntr":
                _selected.discard("proud")
                if "ntr" in _selected:
                    _selected.discard("ntr")
                    _boundary[0] = 0
                else:
                    _selected.add("ntr")
                    if _boundary[0] == 0 and not _is_lesbian:
                        _boundary[0] = 1
            elif result == "proud":
                _selected.discard("ntr")
                _boundary[0] = 0
                if "proud" in _selected:
                    _selected.discard("proud")
                else:
                    _selected.add("proud")
            elif result == "neutral":
                _selected.discard("ntr")
                _selected.discard("proud")
                _boundary[0] = 0
            elif result == "voyeur":
                if "voyeur" in _selected:
                    _selected.discard("voyeur")
                else:
                    _selected.add("voyeur")
            elif result == "camera_lover":
                if "camera_lover" in _selected:
                    _selected.discard("camera_lover")
                else:
                    _selected.add("camera_lover")
            elif result == "bl_1":
                _boundary[0] = 1
            elif result == "bl_2":
                _boundary[0] = 2
            elif result == "bl_3":
                _boundary[0] = 3
            elif result == "bl_4":
                _boundary[0] = 4

        girl._npc_partner_traits = set(_selected)
        # The partner was already rolled at random when he / she was assigned: drop that pre-rolled limit.
        # None = create_npc_partner() sets it at the rebuild (1 for a non-NTR partner or a lesbian's girlfriend).
        girl._ntr_boundary_level = None
        if "ntr" in _selected:
            girl._ntr_active = True
            if not _is_lesbian:
                girl._ntr_boundary_level = _boundary[0] if _boundary[0] > 0 else 1
        else:
            girl._ntr_active = False
        debug_log("[NPC_TRAIT_PICK] %s partner traits=%s boundary=%s" % (girl.Name, _selected, _boundary[0]))


screen npc_trait_picker(girl, partner_label, selected, boundary_level, is_lesbian):
    modal True
    zorder 200

    frame:
        style "SideMenuFrame"
        align (0.5, 0.5)
        xminimum _NTP_PNL_W
        xmaximum _NTP_PNL_W

        vbox:
            spacing 6

            # --- Header ---
            hbox:
                spacing 8
                yalign 0.5

                frame:
                    background "#a78bfa"
                    xsize 3
                    ysize 22
                    yalign 0.5

                text "%s - [girl.Name]'s [partner_label]" % _tr("PARTNER TRAITS"):
                    size _NTP_FS_TITLE
                    color "#a78bfa"
                    font "fonts/WorkSans-Bold.ttf"
                    outlines [(1, "#06101e", 0, 0)]
                    yalign 0.5

            null height 4

            # --- Randomize button ---
            textbutton _tr("Randomize All"):
                style "SideMenuButton"
                text_style "SideMenuButtonText"
                xalign 0.5
                action Return("_randomize")

            null height 4

            # --- Two-column layout ---
            hbox:
                spacing 20
                xfill True

                # === LEFT COLUMN: Disposition + Preferences ===
                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    ymaximum _NTP_VP_H
                    xsize _NTP_COL_W

                    vbox:
                        spacing 4

                        text _tr("Disposition"):
                            size _NTP_FS_HDR
                            color "#a78bfa"
                            font "fonts/WorkSans-Bold.ttf"
                            outlines [(1, "#060d1a", 0, 0)]
                            xalign 0.0

                        null height 4

                        # NTR
                        if "ntr" in selected:
                            textbutton "{color=#a78bfa}> %s{/color}  {size=%d}%s{/size}" % (_tr("NTR"), _NTP_INLINE_SZ, _tr("Enjoys watching and sharing. Never breaks up over cheating.")):
                                style "SideMenuButton"
                                text_style "SideMenuButtonText"
                                action Return("ntr")
                        else:
                            textbutton "%s  {size=%d}{color=#8ca0b4}%s{/color}{/size}" % (_tr("NTR"), _NTP_INLINE_SZ, _tr("Enjoys watching and sharing. Never breaks up over cheating.")):
                                style "SideMenuButton"
                                text_style "SideMenuButtonText"
                                action Return("ntr")

                        # Neutral
                        $ _is_neutral = "ntr" not in selected and "proud" not in selected
                        if _is_neutral:
                            textbutton "{color=#a78bfa}> %s{/color}  {size=%d}%s{/size}" % (_tr("Neutral"), _NTP_INLINE_SZ, _tr("Slightly jealous. May break up eventually.")):
                                style "SideMenuButton"
                                text_style "SideMenuButtonText"
                                action Return("neutral")
                        else:
                            textbutton "%s  {size=%d}{color=#8ca0b4}%s{/color}{/size}" % (_tr("Neutral"), _NTP_INLINE_SZ, _tr("Slightly jealous. May break up eventually.")):
                                style "SideMenuButton"
                                text_style "SideMenuButtonText"
                                action Return("neutral")

                        # Proud
                        if "proud" in selected:
                            textbutton "{color=#a78bfa}> %s{/color}  {size=%d}%s{/size}" % (_tr("Proud"), _NTP_INLINE_SZ, _tr("Jealous and possessive. Will break up quickly if caught.")):
                                style "SideMenuButton"
                                text_style "SideMenuButtonText"
                                action Return("proud")
                        else:
                            textbutton "%s  {size=%d}{color=#8ca0b4}%s{/color}{/size}" % (_tr("Proud"), _NTP_INLINE_SZ, _tr("Jealous and possessive. Will break up quickly if caught.")):
                                style "SideMenuButton"
                                text_style "SideMenuButtonText"
                                action Return("proud")

                        null height 10

                        text _tr("Preferences"):
                            size _NTP_FS_HDR
                            color "#a78bfa"
                            font "fonts/WorkSans-Bold.ttf"
                            outlines [(1, "#060d1a", 0, 0)]
                            xalign 0.0

                        null height 4

                        # Voyeur
                        if "voyeur" in selected:
                            textbutton "{color=#a78bfa}> %s{/color}  {size=%d}%s{/size}" % (_tr("Voyeur"), _NTP_INLINE_SZ, _tr("Wants to watch in person.")):
                                style "SideMenuButton"
                                text_style "SideMenuButtonText"
                                action Return("voyeur")
                        else:
                            textbutton "%s  {size=%d}{color=#8ca0b4}%s{/color}{/size}" % (_tr("Voyeur"), _NTP_INLINE_SZ, _tr("Wants to watch in person.")):
                                style "SideMenuButton"
                                text_style "SideMenuButtonText"
                                action Return("voyeur")

                        # Camera Lover
                        if "camera_lover" in selected:
                            textbutton "{color=#a78bfa}> %s{/color}  {size=%d}%s{/size}" % (_tr("Camera Lover"), _NTP_INLINE_SZ, _tr("Wants videos of her.")):
                                style "SideMenuButton"
                                text_style "SideMenuButtonText"
                                action Return("camera_lover")
                        else:
                            textbutton "%s  {size=%d}{color=#8ca0b4}%s{/color}{/size}" % (_tr("Camera Lover"), _NTP_INLINE_SZ, _tr("Wants videos of her.")):
                                style "SideMenuButton"
                                text_style "SideMenuButtonText"
                                action Return("camera_lover")

                # === RIGHT COLUMN: NTR Limits ===
                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    ymaximum _NTP_VP_H
                    xsize _NTP_COL_W

                    vbox:
                        spacing 4

                        if "ntr" in selected and not is_lesbian:
                            text _tr("NTR Limits"):
                                size _NTP_FS_HDR
                                color "#a78bfa"
                                font "fonts/WorkSans-Bold.ttf"
                                outlines [(1, "#060d1a", 0, 0)]
                                xalign 0.0

                            null height 2

                            text _tr("What is the initial boundary the partner is comfortable with? You can push these limits during gameplay and unlock new scenarios."):
                                size _NTP_FS_BODY
                                color "#8ca0b4"
                                outlines [(1, "#060d1a", 0, 0)]
                                xalign 0.0

                            null height 6

                            # Level 1
                            if boundary_level == 1:
                                textbutton "{color=#a78bfa}> %s{/color}" % _tr("Non-penetration only"):
                                    style "SideMenuButton"
                                    text_style "SideMenuButtonText"
                                    action Return("bl_1")
                            else:
                                textbutton "%s" % _tr("Non-penetration only"):
                                    style "SideMenuButton"
                                    text_style "SideMenuButtonText"
                                    action Return("bl_1")

                            # Level 2
                            if boundary_level == 2:
                                textbutton "{color=#a78bfa}> %s{/color}" % _tr("Condom-protected sex"):
                                    style "SideMenuButton"
                                    text_style "SideMenuButtonText"
                                    action Return("bl_2")
                            else:
                                textbutton "%s" % _tr("Condom-protected sex"):
                                    style "SideMenuButton"
                                    text_style "SideMenuButtonText"
                                    action Return("bl_2")

                            # Level 3
                            if boundary_level == 3:
                                textbutton "{color=#a78bfa}> %s{/color}" % _tr("Raw sex, no creampie or anal"):
                                    style "SideMenuButton"
                                    text_style "SideMenuButtonText"
                                    action Return("bl_3")
                            else:
                                textbutton "%s" % _tr("Raw sex, no creampie or anal"):
                                    style "SideMenuButton"
                                    text_style "SideMenuButtonText"
                                    action Return("bl_3")

                            # Level 4
                            if boundary_level == 4:
                                textbutton "{color=#a78bfa}> %s{/color}" % _tr("No limits"):
                                    style "SideMenuButton"
                                    text_style "SideMenuButtonText"
                                    action Return("bl_4")
                            else:
                                textbutton "%s" % _tr("No limits"):
                                    style "SideMenuButton"
                                    text_style "SideMenuButtonText"
                                    action Return("bl_4")

                        elif "ntr" in selected and is_lesbian:
                            text _tr("NTR Limits"):
                                size _NTP_FS_HDR
                                color "#a78bfa"
                                font "fonts/WorkSans-Bold.ttf"
                                outlines [(1, "#060d1a", 0, 0)]
                                xalign 0.0

                            null height 4

                            text _tr("Lesbian partners do not have boundary levels."):
                                size _NTP_FS_BODY
                                color "#555e6e"
                                outlines [(1, "#060d1a", 0, 0)]

            null height 8

            # --- Done button ---
            textbutton _tr("Done"):
                style "SideMenuButton"
                text_style "SideMenuButtonText"
                xalign 0.5
                action Return("_done")
