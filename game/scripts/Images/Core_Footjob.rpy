# ============================================================
# Core Footjob -- Tenny exclusive
# FT_Launch and FT_ApplySpeed live in Tenny/Footjob.rpy
# (animation engine). This file holds the sex-menu integration:
# ControlMenu, cum menu, end label.
# ============================================================

label FT_ControlMenu(girl):
    $ store._player_exhausted = False

    while True:

        if _scene_should_exit():
            return

        if Round >= 100:
            $ Say_Line(girl, _scene_time_up_line())
            call FT_End(girl, dress_up=False) from _call_FT_End_timeout
            return

        menu:
            "Keep going" if _ft_speed >= 1:
                $ advance_round(TIME_COSTS["sex_tick"])
                $ add_player_focus(get_player_lust_gain("fj", _ft_speed))
                $ _girl_lust_gain(girl, (2 if _ft_speed == 1 else 3 if _ft_speed == 2 else 5), _ft_speed)
                $ _moan = scene_moan_tick(girl, "fj", _ft_speed)
                if _moan:
                    call _moan_say(girl, _moan) from _call_ms_fj_kg

                $ _pa_caught = public_attention_tick(girl, "keep_going", _ft_speed)
                if _pa_caught:
                    if not _caught_keeps_going(girl):
                        call FT_End(girl, dress_up=False) from _call_FT_End_pa
                    call caught_in_public(girl, "fj") from _call_caught_public_fj_kg
                    return

                call _sex_interruption_check(girl, "fj") from _call_sex_irpt_fj
                $ store._witness_expression_lock = False
                if store._sex_interrupted:
                    call FT_End(girl, dress_up=False) from _call_FT_End_irpt
                    return

                call _npc_partner_detection_tick(girl, "fj") from _call_npc_detect_fj
                if store._npc_witness_scene_aborted:
                    call FT_End(girl, dress_up=False) from _call_FT_End_npc
                    return

                call _sub_event_tick_nonpen(girl, "fj") from _call_se_np_fj
                if store._sst_result == "abort":
                    call FT_End(girl, dress_up=False) from _call_FT_End_se
                    return

                if girl.Lust >= 100:
                    call GirlCumming(girl, "fj", "footjob") from _call_GirlCumming_fj
                if player_is_cumming():
                    if focus_overdue_tick():
                        call ForcedCumOverdue(girl, "fj") from _call_ForcedCumOverdue_fj_kg
                        $ _handle_post_cum_exit("fj", "sex")
                        return

            "Speed up" if _ft_speed < 3:
                $ advance_round(TIME_COSTS["sex_tick"])
                $ Say_Player(_("Faster..."))
                $ _ft_speed += 1
                call FT_ApplySpeed(girl, _ft_speed) from _call_FT_ApplySpeed_su
                $ add_player_focus(get_player_lust_gain("fj", _ft_speed))
                $ _girl_lust_gain(girl, (2 if _ft_speed == 1 else 3 if _ft_speed == 2 else 5), _ft_speed)
                $ _moan = scene_moan_tick(girl, "fj", _ft_speed)
                if _moan:
                    call _moan_say(girl, _moan) from _call_ms_fj_su
                $ _pa_caught = public_attention_tick(girl, "speed_up", _ft_speed)
                if _pa_caught:
                    if not _caught_keeps_going(girl):
                        call FT_End(girl, dress_up=False) from _call_FT_End_pa2
                    call caught_in_public(girl, "fj") from _call_caught_public_fj_su
                    return
                if girl.Lust >= 100:
                    call GirlCumming(girl, "fj", "footjob") from _call_GirlCumming_fj_su
                if player_is_cumming():
                    if focus_overdue_tick():
                        call ForcedCumOverdue(girl, "fj") from _call_ForcedCumOverdue_fj_su
                        $ _handle_post_cum_exit("fj", "sex")
                        return
                $ Narration(_("She picks up the pace with her feet."))

            "Speed down" if _ft_speed > 0:
                $ advance_round(1)
                $ _ft_speed -= 1
                call FT_ApplySpeed(girl, _ft_speed) from _call_FT_ApplySpeed_sd
                $ add_player_focus(10 if _ft_speed == 1 else 20 if _ft_speed >= 2 else 0)
                $ Narration(_("She slows her movements."))

            "Tease her..." if _ft_speed > 0:
                $ advance_round(1)
                call _tease_menu(girl, "fj") from _call_tease_menu_fj

            "Strip her..." if _ft_strip_choices(girl):
                $ advance_round(1)
                call _ft_strip_menu(girl) from _call_ft_strip_menu

            "Record Options..." if not getattr(store, "_recording_active", False) or getattr(store, "_recording_girl", None) == girl:
                menu:
                    "Record her" if not getattr(store, "_recording_active", False):
                        call _sex_phone_menu(girl, "fj") from _call__sex_phone_menu_fj
                    "Stop recording" if getattr(store, "_recording_active", False) and getattr(store, "_recording_girl", None) == girl:
                        $ finalize_recording()
                        $ Narration(_("You stop recording."))
                    "Back":
                        pass
                call FT_ApplySpeed(girl, _ft_speed) from _call_FT_ApplySpeed_rec

            "{color=#fbbf24}Cum{/color}" if player_is_cumming():
                call PlayerCumMenu(girl, "fj") from _call_PlayerCumMenu_voluntary_fj
                $ _handle_post_cum_exit("fj", "sex")
                return

            "Stop now":
                if store._forced_creampie_end_after_orgasm:
                    call _player_stops_after_forced_creampie(girl, "fj") from _call__player_stops_forced_fj
                else:
                    call _scene_stop_reaction(girl) from _call_scene_stop_reaction_fj
                    if store._stop_accepted:
                        call FT_End(girl, dress_up=False) from _call_FT_End_stop
                        return

# The in-pose strip (choices from _ft_strip_choices, Tenny/Footjob.rpy): her feet never stop, the scene redraws itself
label _ft_strip_menu(girl):
    python:
        _FT_STRIP_NARR = {
            ("over", "up"):   _("You slide her jacket off her shoulders. It hangs from her arms, and her feet never stop."),
            ("over", None):   _("You peel her jacket off one arm at a time. Her rhythm never breaks."),
            ("mid", "up"):    _("You pull her shirt up over her chest without slowing her down."),
            ("mid", None):    _("You work her shirt off over her head. Her feet keep their pace the whole time."),
            ("chest", "up"):  _("You tug her top up and her breasts spill free."),
            ("chest", None):  _("You pull her top off and toss it aside."),
        }
        _fts_choices = _ft_strip_choices(girl) + [(_tl(_("Back")), None)]
        _fts_pick = renpy.display_menu(_fts_choices)
    if _fts_pick is None:
        return
    python:
        _fts_slot, _fts_val = _fts_pick
        _ft_strip_apply(girl, _fts_slot, _fts_val)
        _fts_narr = _FT_STRIP_NARR[(_fts_slot, _fts_val)]
    $ set_scene_expression(girl, "sexy" if girl.Lust >= 50 else "shy")
    "[_fts_narr!t]"
    $ set_scene_expression(girl, "normal")
    return

label FT_End(girl, dress_up=True):
    $ debug_log("[DEBUG] FT_End: entered, dress_up=%s" % str(dress_up))
    $ scene_full_cleanup(girl)
    $ finalize_recording()
    $ _player_cleanup(girl)

    $ pose = getattr(girl, "_prev_pose", "standing")
    $ slot = _safe_restore_slot(getattr(girl, "_prev_slot", StageCenter))

    python:
        slot_transform = _slot_to_transform(slot)
        _reset_expression_state(girl)

        store._ft_girl = None
        store._ft_speed = 0
        _ft_hide_all()
        girl.ResetVisuals(pose=pose, at_list=[slot_transform])

    if dress_up:
        python:
            if hasattr(girl, "_prev_outfit") and girl._prev_outfit:
                girl.Outfit_Change(**girl._prev_outfit)
    return
