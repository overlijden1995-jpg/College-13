# ============================================================
# Core Rimjob (docs/plan_shion.md Fase 5) -- an exclusive act (act key "rj", pose "rimjob", layers "rj_*")
# She kneels behind him: her tongue between his cheeks, her hand reaching around to stroke him. Only a girl with
# the art has it (POSE_ONLY_FOR["rimjob"], scene_config.rpy): Shion. Her layers and _rj_apply_speed live in
# Images/<Girl>/Rimjob.rpy; this file is the sex-menu side: launch, control menu, his cum, end.
# Head 1: she leans back, tongue out, looking at him. Head 2: her face pressed in (the "Push her face in" option).
# He is the one in control (ACT_CONTROL "rj": "him"): a girl with a story refuses it before the step that opens it
# whatever her stats (the stepmom: step 2, story_steps.rpy); nothing opens it sooner, not even his blackmail.
# ============================================================

default _rj_cum = None      # his cum in this scene: None / "hand" (in her hand) / "away" (fired away)

init python:

    # What the girl's lust gains per tick at each speed (she is the one working; little for her)
    RJ_GIRL_LUST = {1: 1, 2: 2, 3: 3}

label RJ_Launch(girl):
    $ sub_event_reset(girl)
    $ debug_log("[DEBUG] RJ_Launch: entered for %s" % girl.gid)
    $ _kill_scene_threads()
    $ stop_standing_blink(girl)
    $ public_attention_reset()
    call PlayerExposure(girl) from _call_PlayerExposure_rj

    $ girl._prev_pose = getattr(girl, "default_pose", "standing")
    $ girl._prev_slot = getattr(girl, "SpriteLoc", StageCenter)
    if not getattr(girl, "_saved_outfit", None):
        $ girl.SaveOutfit()

    python:
        _hide_all_scene_layers(girl)
        hide_girl_sprite(girl)
        store.hiding_face = False
        store._rj_girl = girl
        store._rj_speed = 0
        store._rj_head_pos = 1
        store._rj_cum = None
        store._slap_count = 0
        sprite_state.setdefault(girl.Id, {})["pose"] = "rimjob"
        # a towel has no rimjob art: it falls when she kneels
        if getattr(girl, "Over", None) == "towel":
            girl.Outfit_Change(over="none", refresh=False)
        unlock_achievement("kiss_the_throne")
        print("[RJ] launch: %s (clothes %s)" % (girl.gid, getattr(girl, "clothes", {})))

    call RJ_ApplySpeed(girl, 0) from _call_RJ_ApplySpeed_launch
    with fade
    return

label RJ_ApplySpeed(girl, speed=0):
    $ _rj_apply_speed(girl, speed)
    return

# His cum: in her hand (cum_anim) or fired away (fire_away_anim); the spurt shows for a moment, the rest stays
label RJ_CumAnim(girl):
    call _rj_cum_shot(girl, "hand") from _call_rj_cum_shot_hand
    return

label RJ_FireAwayAnim(girl):
    call _rj_cum_shot(girl, "away") from _call_rj_cum_shot_away
    return

label _rj_cum_shot(girl, where):
    python:
        store._rj_cum = where
        _rj_apply_speed(girl, 0)
        _rj_spurt = "%s rj_cum_spour" % girl.gid
        if renpy.has_image(_rj_spurt, exact=True):
            # from his penis: it moves with it (her layer set's _rj_penis_at, shown in the same interaction = in step)
            renpy.show(_rj_spurt, tag="rj_cum_spour", zorder=9954, at_list=_rj_penis_at(0))
        print("[RJ] his cum: %s" % where)
    with vpunch
    pause 0.8
    $ renpy.hide("rj_cum_spour")
    return

# ============================================================
# His cum menu in the rimjob (CUM_POSITION_CONFIG["rj"]["cum_menu"]): her hand is the only place he can reach
# ============================================================
label PlayerCumMenu_Hand(girl, scene_type):
    menu:
        "Let her finish you with her hand":
            call _cum_dispatch_anim(girl, scene_type) from _call__cum_dispatch_anim_hand
            $ process_cum(girl, scene_type, "hand")
            $ apply_cum_bonuses(girl, "cum_outside")
            if girl.has_trait("hate_cum"):
                $ Change_Status(girl, "Love", -5)
            $ _cum_say_line(girl, "hand", scene_type)

        "On her wedding ring" if girl_wears_ring(girl):
            call _netori_ring_cum(girl, scene_type) from _call__netori_ring_cum_hand

        "Fire away":
            call _cum_dispatch_fire_away(girl, scene_type) from _call__cum_dispatch_fire_away_hand
            $ process_cum(girl, scene_type, "away")
            $ apply_cum_bonuses(girl, "cum_outside")
            $ _cum_say_line(girl, "away", scene_type)

    $ Change_Status(girl, "Obed", 1)
    return

# ============================================================
# Control menu
# ============================================================
label RJ_ControlMenu(girl):
    $ store._player_exhausted = False

    while True:

        if _scene_should_exit():
            return

        if Round >= 100:
            $ Say_Line(girl, _scene_time_up_line())
            call RJ_End(girl, dress_up=False) from _call_RJ_End_timeout
            return

        menu:
            "Keep going" if _rj_speed >= 1:
                $ advance_round(TIME_COSTS["sex_tick"])
                call _rj_tick(girl, "keep_going") from _call_rj_tick_kg
                if _rj_tick_exit:
                    return

            "Speed up" if _rj_speed < 3:
                $ advance_round(TIME_COSTS["sex_tick"])
                $ Say_Player(_("Faster..."))
                $ _rj_speed += 1
                call RJ_ApplySpeed(girl, _rj_speed) from _call_RJ_ApplySpeed_su
                call _rj_tick(girl, "speed_up") from _call_rj_tick_su
                if _rj_tick_exit:
                    return
                $ Narration(_("She works her tongue deeper and strokes you faster."))

            "Speed down" if _rj_speed > 0:
                $ advance_round(1)
                $ _rj_speed -= 1
                call RJ_ApplySpeed(girl, _rj_speed) from _call_RJ_ApplySpeed_sd
                $ add_player_focus(10 if _rj_speed == 1 else 20 if _rj_speed >= 2 else 0)
                $ Narration(_("She slows down, her tongue lazy against you."))

            "Push her face in" if _rj_head_pos == 1:
                $ advance_round(1)
                $ _rj_switch_head(2)
                $ Narration(_("You reach back and press her face between your cheeks."))

            "Let her look up at you" if _rj_head_pos == 2:
                $ advance_round(1)
                $ _rj_switch_head(1)
                $ Narration(_("You let her pull back. She looks up at you, catching her breath, her tongue still out."))

            "Tease her..." if _rj_speed > 0:
                $ advance_round(1)
                call _tease_menu(girl, "rj") from _call_tease_menu_rj

            "Strip her":
                $ advance_round(1)
                call RJ_StripMenu(girl) from _call_RJ_StripMenu

            # the FN rule (tester 2026-10-10): nobody films their own back by hand; the tripod holds the phone
            "Record Options..." if (not getattr(store, "_recording_active", False) and Player.has_item("tripod")) or (getattr(store, "_recording_active", False) and getattr(store, "_recording_girl", None) == girl):
                menu:
                    "Record her" if Player.has_item("tripod") and not getattr(store, "_recording_active", False):
                        call _sex_phone_menu(girl, "rj") from _call__sex_phone_menu_rj
                    "Stop recording" if getattr(store, "_recording_active", False) and getattr(store, "_recording_girl", None) == girl:
                        $ finalize_recording()
                        $ Narration(_("You stop recording."))
                    "Back":
                        pass
                call RJ_ApplySpeed(girl, _rj_speed) from _call_RJ_ApplySpeed_rec

            "{color=#fbbf24}Cum{/color}" if player_is_cumming():
                call PlayerCumMenu(girl, "rj") from _call_PlayerCumMenu_voluntary_rj
                $ _handle_post_cum_exit("rj", "sex")
                return

            "Stop now":
                if store._forced_creampie_end_after_orgasm:
                    call _player_stops_after_forced_creampie(girl, "rj") from _call__player_stops_forced_rj
                else:
                    call _scene_stop_reaction(girl) from _call_scene_stop_reaction_rj
                    if store._stop_accepted:
                        $ Narration(_("You pull away and let her get up."))
                        call RJ_End(girl, dress_up=False) from _call_RJ_End_stop
                        return

# The in-pose strip, the HJ_StripMenu shape (central _strip_approval: she can refuse, exposure line, CheckExposure).
# The rimjob draws its clothes as standalone layers in _rj_apply_speed (never the registry's pose attributes, so no
# _slot_renderable here): over = jacket (+ clothed arms), mid = vest ("Remove shirt", the mid label every strip menu
# uses), chest = bra / bikini top, legs = the pants art for any legs item, panties = panties / bikini bottom. No
# shoes or collar art in this pose. Outfit_Change with refresh=False: _rj_apply_speed redraws the scene itself
# (RJ_Launch's towel drop does the same).
label RJ_StripMenu(girl):
    while True:
        $ _legs_label = _("Remove pants") if _strip_name_for_slot(girl, "skirt") == "pants" else _("Remove skirt")
        menu:
            "Remove top" if girl.Over:
                call _strip_approval(girl, ["over"]) from _call__strip_approval_rj_over
                if store._strip_approved:
                    $ girl.Outfit_Change(over="none", refresh=False)
                    call RJ_ApplySpeed(girl, _rj_speed) from _call_RJ_ApplySpeed_strip_over
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_rj_over

            "Remove shirt" if girl.Mid:
                call _strip_approval(girl, ["mid"]) from _call__strip_approval_rj_mid
                if store._strip_approved:
                    $ girl.Outfit_Change(mid="none", refresh=False)
                    call RJ_ApplySpeed(girl, _rj_speed) from _call_RJ_ApplySpeed_strip_mid
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_rj_mid

            "Remove chest" if girl.Chest:
                call _strip_approval(girl, ["chest"]) from _call__strip_approval_rj_chest
                if store._strip_approved:
                    $ girl.Outfit_Change(chest="none", refresh=False)
                    call RJ_ApplySpeed(girl, _rj_speed) from _call_RJ_ApplySpeed_strip_chest
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_rj_chest

            "[_legs_label]" if girl.Legs:
                call _strip_approval(girl, ["legs"]) from _call__strip_approval_rj_legs
                if store._strip_approved:
                    $ girl.Outfit_Change(legs="none", refresh=False)
                    call RJ_ApplySpeed(girl, _rj_speed) from _call_RJ_ApplySpeed_strip_legs
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_rj_legs

            "Remove panties" if girl.Panties:
                call _strip_approval(girl, ["panties"]) from _call__strip_approval_rj_pan
                if store._strip_approved:
                    $ girl.Outfit_Change(panties="none", refresh=False)
                    call RJ_ApplySpeed(girl, _rj_speed) from _call_RJ_ApplySpeed_strip_pan
                    if store._strip_exp_part:
                        call CheckExposure(girl) from _call_CheckExposure_rj_pan

            "Back":
                return

# One tick of the scene (Keep going / Speed up): his focus, her lust and moans, the outside world, her orgasm, his
# overdue cum. Sets _rj_tick_exit when the scene is over (the control menu returns).
label _rj_tick(girl, action):
    $ _rj_tick_exit = False
    $ add_player_focus(get_player_lust_gain("rj", _rj_speed))
    $ _girl_lust_gain(girl, RJ_GIRL_LUST.get(_rj_speed, 1), _rj_speed)
    $ _moan = scene_moan_tick(girl, "rj", _rj_speed)
    if _moan:
        call _moan_say(girl, _moan) from _call_ms_rj

    $ _pa_caught = public_attention_tick(girl, action, _rj_speed)
    if _pa_caught:
        if not _caught_keeps_going(girl):
            call RJ_End(girl, dress_up=False) from _call_RJ_End_pa
        call caught_in_public(girl, "rj") from _call_caught_public_rj
        $ _rj_tick_exit = True
        return

    if action == "keep_going":
        call _sex_interruption_check(girl, "rj") from _call_sex_irpt_rj
        $ store._witness_expression_lock = False
        if store._sex_interrupted:
            call RJ_End(girl, dress_up=False) from _call_RJ_End_irpt
            $ _rj_tick_exit = True
            return

        call _npc_partner_detection_tick(girl, "rj") from _call_npc_detect_rj
        if store._npc_witness_scene_aborted:
            call RJ_End(girl, dress_up=False) from _call_RJ_End_npc
            $ _rj_tick_exit = True
            return

        call _sub_event_tick_nonpen(girl, "rj") from _call_se_np_rj
        if store._sst_result == "abort":
            call RJ_End(girl, dress_up=False) from _call_RJ_End_se
            $ _rj_tick_exit = True
            return

    if girl.Lust >= 100:
        call GirlCumming(girl, "rj", "rimjob") from _call_GirlCumming_rj
    if player_is_cumming():
        if focus_overdue_tick():
            call ForcedCumOverdue(girl, "rj") from _call_ForcedCumOverdue_rj
            $ _handle_post_cum_exit("rj", "sex")
            $ _rj_tick_exit = True
    return

label RJ_End(girl, dress_up=True):
    $ debug_log("[DEBUG] RJ_End: entered for %s, dress_up=%s" % (girl.gid, dress_up))
    $ scene_full_cleanup(girl)
    $ finalize_recording()
    $ _player_cleanup(girl)

    $ pose = getattr(girl, "_prev_pose", "standing")
    $ slot = _safe_restore_slot(getattr(girl, "_prev_slot", StageCenter))

    python:
        slot_transform = _slot_to_transform(slot)
        _reset_expression_state(girl)
        store._rj_girl = None
        store._rj_speed = 0
        store._rj_head_pos = 1
        store._rj_cum = None
        _rj_hide_all()
        girl.ResetVisuals(pose=pose, at_list=[slot_transform])

    if dress_up:
        python:
            if hasattr(girl, "_prev_outfit") and girl._prev_outfit:
                girl.Outfit_Change(**girl._prev_outfit)
    return
