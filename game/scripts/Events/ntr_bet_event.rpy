# ============================================
# NTR BET EVENT: Scripted NTR Bet
# One-time event: girl with NPC partner (NTR
# boundary 2, discovered) bets he can't resist
# watching. Player makes noise to win the bet.
# ============================================

default _bet_girl_gid = None
default _bet_scheduled_day = -1
default _bet_cooldown_until = -1
default _bet_event_active = False
default _bet_npc_looked = False
default _bet_last_looked = False   # result of the last finished bet (QA results); _bet_npc_looked is reset at cleanup

init python:

    # ── Position config (labels not in CUM_POSITION_CONFIG) ──

    _BET_POS_CONFIG = {
        "cowgirl": {
            "rub_label":    "COWGIRL_RubLaunch",
            "enter_label":  "CG_PenisEnterAnim",
            "started_var":  "cowgirl_started",
        },
        "reverse_cowgirl": {
            "rub_label":    "RCG_RubLaunch",
            "enter_label":  "RCG_PenisEnterAnim",
            "started_var":  "rcg_started",
        },
        "doggy": {
            "rub_label":    "DG_RubLaunch",
            "enter_label":  "DG_PenisEnterAnim",
            "started_var":  "doggy_started",
        },
        "full_nelson": {
            "rub_label":    "FN_RubLaunch",
            "enter_label":  "FN_PenisEnterAnim",
            "started_var":  "fn_started",
        },
        "laying_down": {
            "rub_label":    "LD_RubLaunch",
            "enter_label":  "LD_PenisEnterAnim",
            "started_var":  "laying_started",
        },
    }

    _BET_POS_DISPLAY = {
        "cowgirl":         _("Cowgirl"),
        "reverse_cowgirl": _("Reverse Cowgirl"),
        "doggy":           _("Doggy"),
        "full_nelson":     _("Full Nelson"),
        "laying_down":     _("Laying Down"),
    }

    _BET_MAX_TICKS = 12

    # ── Daily morning check (called from _per_day_cleanup) ──

    def _bet_reset_flags(reason="cleanup", mark_done=True):
        """SINGLE exit point of the bet-event state. Callers: _bet_cleanup, force_scene_reset (event aborted
        through jump main_loop, e.g. the heavy spank tier) and _bet_daily_check (stale saves).
        A leaked _bet_event_active disables the forced cum, the sub events, the NTR watcher clear and the
        time-lock safety unlock; a leaked _bet_npc_looked made the partner ignore protection forever."""
        _g = GIRL_BY_ID.get(getattr(store, "_bet_girl_gid", None))
        if _g is not None:
            if mark_done:
                _g._bet_event_done = True
            else:
                store._bet_cooldown_until = store.Day + 7   # aborted: she can invite again later
        store._bet_last_looked = getattr(store, "_bet_npc_looked", False)
        store._bet_event_active = False
        store._bet_npc_looked = False
        store._bet_noise = 0
        store._bet_tick = 0
        store._bet_scene_type = None
        store._bet_scheduled_day = -1
        store._bet_girl_gid = None
        store._scene_restricted = False
        time_unlock()
        print("[BET] flags reset (%s) done=%s last_looked=%s" % (reason, mark_done, store._bet_last_looked))

    def _bet_daily_check():
        print("[BET] daily check called. Day=%d scheduled=%d cooldown=%d" % (store.Day, store._bet_scheduled_day, store._bet_cooldown_until))
        if getattr(store, "_bet_event_active", False):
            # Time is locked while the event runs: a day rollover with the flag still set means it was
            # aborted without _bet_cleanup (old saves included)
            print("[BET] daily check: stale bet state, resetting")
            _bet_reset_flags("stale_daily_check", mark_done=False)
        elif getattr(store, "_bet_npc_looked", False):
            store._bet_npc_looked = False   # leaked by builds that never cleared it
            print("[BET] daily check: cleared leaked _bet_npc_looked")
        if 0 < store._bet_scheduled_day < store.Day:
            # the scheduled day passed without the event firing (player was not alone in his room):
            # it used to stay "scheduled" forever and no girl could ever invite again
            print("[BET] daily check: scheduled day %d missed, unscheduling" % store._bet_scheduled_day)
            store._bet_scheduled_day = -1
            store._bet_girl_gid = None
        if store._bet_scheduled_day > 0:
            print("[BET] daily check: already scheduled for day %d" % store._bet_scheduled_day)
            return
        if store.Day < 7:
            print("[BET] daily check: too early (Day < 7)")
            return
        if store._bet_cooldown_until > 0 and store.Day < store._bet_cooldown_until:
            print("[BET] daily check: cooldown until day %d" % store._bet_cooldown_until)
            return

        for girl in ALL_GIRLS:
            if getattr(girl, "_bet_event_done", False):
                print("[BET] daily check: skip %s (event already done)" % girl.gid)
                continue
            if not girl.has_npc_partner():
                continue
            _npc = get_npc_partner_for(girl)
            if _npc is None:
                print("[BET] daily check: %s has partner id but no NPC object" % girl.gid)
                continue
            _skip = None
            if girl_is_away(girl):
                _skip = "away (giving birth)"
            elif not getattr(_npc, "_ntr_active", False):
                _skip = "ntr not active"
            # Discovery flag lives on the girl (set by _ntr_activation_message_event);
            # the NPC attr is only set by the QA harness
            elif not (getattr(girl, "_ntr_boundary_discovered", False) or getattr(_npc, "_ntr_boundary_discovered", False)):
                _skip = "boundary not discovered"
            elif getattr(_npc, "_ntr_boundary_level", 0) != 2:
                _skip = "boundary level %s != 2" % getattr(_npc, "_ntr_boundary_level", 0)
            elif girl.has_trait("virgin"):
                _skip = "virgin"
            elif not girl_had_sex(girl):
                _skip = "no sex yet"
            if _skip:
                print("[BET] daily check: skip %s (%s)" % (girl.gid, _skip))
                continue

            store._bet_scheduled_day = store.Day
            store._bet_girl_gid = girl.gid
            print("[BET] Scheduled for today. Girl=%s Day=%d" % (girl.gid, store.Day))
            return

    # ── Dialogue pools ──

    _BET_DIALOGUE = {
        "phone": {
            "invite_1": [
                _("Hey, come to my room. I need your help with something."),
                _("Hey, come over. I have something fun planned with %(pn)s."),
            ],
            "invite_2": [
                _("Bring a condom. Trust me, you'll want to be here for this."),
                _("Make sure you have a condom. This is going to be fun."),
            ],
            "accept": [
                _("On my way."),
            ],
            "decline": [
                _("Not right now."),
            ],
            "girl_confirm": [
                _("Hurry up!"),
            ],
            "girl_decline_reply": [
                _("Seriously? Your loss."),
            ],
        },
        "arrival": {
            "girl_explain": [
                _("Ok, so... me and %(pn)s have a little bet going. Just play along, ok?"),
                _("So, I made a bet with %(pn)s. Don't worry about the details, just follow my lead."),
            ],
            "girl_to_npc": [
                _("Ok baby, turn around. And no peeking!"),
                _("Alright babe, face the wall. Remember our bet!"),
            ],
            "npc_agree": [
                _("Fine. You're going to lose this one."),
                _("Whatever. Deal."),
            ],
            "npc_turn": [
                _("This is stupid. I'm not going to look."),
                _("I won't even be tempted. This is easy."),
            ],
            "girl_whisper": [
                _("Just... be loud, ok? The louder the better. Trust me."),
                _("Make as much noise as you can. You'll see why."),
            ],
        },
        # partner pronouns are placeholders (a girlfriend can take the bet too): shown through _format_partner_line
        "sex_loop": {
            "noise_milestone_5": [
                _("I think %(pp)s's starting to sweat over there."),
                _("Look at %(po)s, %(pp)s's trying so hard not to turn around."),
            ],
            "noise_milestone_8": [
                _("%(Pp)s's so close to breaking! Keep going!"),
                _("Almost there! %(Pp)s can't take much more of this!"),
            ],
        },
        "npc_looks": {
            "narration_turn": [
                _("You hear a sharp intake of breath. %(Pp)s couldn't resist any longer."),
            ],
            "girl_victory": [
                _("HA! I KNEW IT! You couldn't resist, could you?!"),
                _("I WIN! You looked! I told you, you can't handle it!"),
            ],
            "npc_caught": [
                _("I... I just... I heard... Fine, you win."),
                _("It was... the sounds were... Okay, okay, you win!"),
            ],
            "girl_punishment": [
                _("And since you lost... the condom comes off. That was the deal."),
                _("Loser's punishment... no more condom. A bet is a bet."),
            ],
            "npc_react": [
                _("Damn it... a deal is a deal."),
                _("I knew I shouldn't have taken that bet..."),
            ],
            "girl_dismiss_npc": [
                _("Shhh. You lost. Now sit there and watch properly this time."),
                _("Too late, baby. You had your chance. Now enjoy the show."),
            ],
        },
        "cum": {
            "girl_feel": [
                _("Mmm... that was incredible. And %(pp)s saw everything."),
            ],
        },
        "post_win": {
            "girl_thanks": [
                _("That was amazing. Thanks for helping me win. Did you see %(poss)s face?"),
                _("Best bet I ever made. You were perfect. %(Poss)s expression was priceless."),
            ],
            "npc_defeated": [
                _("I... I need a moment."),
                _("I can't believe I lost..."),
            ],
        },
        "post_lose": {
            "girl_lose": [
                _("Well... I guess %(pp)s won that one. You finished too fast."),
                _("Ugh, %(pp)s didn't even flinch. I lost the bet."),
            ],
            "girl_consolation": [
                _("Whatever. Let's go watch Super Cuck Man, %(pn)s. You earned it."),
                _("Fine, fine. %(Pp)s can pick the movie tonight. Ugh."),
            ],
        },
        "exhausted": {
            "narration": [
                _("You can't hold it anymore. Your body gives in."),
            ],
        },
    }


# ── NPC flipped transform ──

transform _bet_slot_right_flipped:
    xalign StageRight
    yalign 2.0
    xzoom -1.0

transform _bet_slot_right_normal:
    xalign StageRight
    yalign 2.0
    xzoom 1.0


# ── Check label (called from Wait label) ──

label ntr_bet_check:
    if _bet_scheduled_day != Day:
        return
    if _bet_girl_gid is None:
        return
    if CurrentLocation != "room":
        return
    if len(Party) > 0 or any(getattr(g, "loc", None) == "room" for g in ALL_GIRLS):
        return

    python:
        _bet_girl = GIRL_BY_ID.get(store._bet_girl_gid)
        if _bet_girl is None:
            store._bet_scheduled_day = -1
        elif girl_is_away(_bet_girl):
            # no cooldown, no "done": she can invite again when she is back
            print("[BET] %s is away: unscheduled" % _bet_girl.gid)
            store._bet_scheduled_day = -1
            store._bet_girl_gid = None
    if _bet_scheduled_day != Day:
        return

    python:
        _bet_npc = get_npc_partner_for(_bet_girl)
        if _bet_npc is None:
            store._bet_scheduled_day = -1
    if _bet_scheduled_day != Day:
        return

    # ── Phone notification ──
    play sound "audio/Notification.mp3" noloop
    "Your phone buzzes. Someone sent you a message."

    $ phone_add_msg(_bet_girl.gid, _bet_girl.gid, None, "typing")
    call screen phone_chat_screen(_bet_girl, auto_close=renpy.random.uniform(0.8, 1.4), choices=[])
    python:
        _t = phone_get_msgs(_bet_girl.gid)
        if _t and _t[-1].get("type") == "typing":
            _t.pop()
        _line = _format_partner_line(_bet_girl, _tl(renpy.random.choice(_BET_DIALOGUE["phone"]["invite_1"])))
        phone_add_msg(_bet_girl.gid, _bet_girl.gid, _line)

    call _phone_typing(_bet_girl) from _typing_bet_invite2
    python:
        phone_add_msg(_bet_girl.gid, _bet_girl.gid, _tl(renpy.random.choice(_BET_DIALOGUE["phone"]["invite_2"])))

    python:
        _bet_phone_choices = [
            (_tl(_BET_DIALOGUE["phone"]["accept"][0]), "accept"),
            (_tl(_BET_DIALOGUE["phone"]["decline"][0]), "decline"),
        ]
    call screen phone_chat_screen(_bet_girl, choices=_bet_phone_choices)
    $ _bet_pick = _return

    if _bet_pick == "accept":
        $ phone_add_msg(_bet_girl.gid, "player", _tl(_BET_DIALOGUE["phone"]["accept"][0]))
        call _phone_typing(_bet_girl) from _typing_bet_confirm
        $ phone_add_msg(_bet_girl.gid, _bet_girl.gid, _tl(_BET_DIALOGUE["phone"]["girl_confirm"][0]))
        call screen phone_chat_screen(_bet_girl, choices=[])

        python:
            if not hasattr(Player, "condoms") or Player.condoms < 1:
                Player.condoms = 1
            Player.Focus = 0

        scene black
        with fade
        "You head to [_bet_girl.Name]'s room."
        python:
            _bet_room = girl_home_loc(store._bet_girl_gid)
            navigate_to(_bet_room, None)
        call Set_Scene(entry=False) from _call_bet_set_scene
        call ntr_bet_event from _call_ntr_bet_event
    else:
        $ phone_add_msg(_bet_girl.gid, "player", _tl(_BET_DIALOGUE["phone"]["decline"][0]))
        call _phone_typing(_bet_girl) from _typing_bet_decline
        $ phone_add_msg(_bet_girl.gid, _bet_girl.gid, _tl(_BET_DIALOGUE["phone"]["girl_decline_reply"][0]))
        call screen phone_chat_screen(_bet_girl, auto_close=1.0, choices=[])

        python:
            Change_Status(_bet_girl, "Love", -5)
            store._bet_cooldown_until = store.Day + 7
            store._bet_scheduled_day = -1
            print("[BET] Player declined. Love -5. Cooldown until day %d." % store._bet_cooldown_until)
    return


# ── Main event ──

label ntr_bet_event:
    python:
        _bet_girl = GIRL_BY_ID.get(store._bet_girl_gid)
        _bet_npc = get_npc_partner_for(_bet_girl)
        store._scene_restricted = True
        time_lock()
        session_cum_reset()
        store._focus_overdue_count = 0
        store._focus_warning_shown = False
        store._ntr_partner_watching = True
        store._ntr_watching_npc = _bet_npc
        store._player_exhausted = False
        store._hate_cum_scene_aborted = False
        store._condom_removed_midscene = False
        store._creampie_consent = False
        store._player_exposed_this_session = False
        store._bet_event_active = True
        store._bet_noise = 0
        store._bet_tick = 0
        store._bet_npc_looked = False
        store._bet_scene_type = None
        print("[BET] Event starting. Girl=%s NPC=%s" % (_bet_girl.gid, _bet_npc.name))

    call _bet_phase_arrival from _call_bet_arrival
    call _bet_phase_position_pick from _call_bet_pos_pick

    # Result depends on whether NPC looked
    if store._bet_npc_looked:
        call _bet_post_win from _call_bet_post_win
    else:
        call _bet_post_lose from _call_bet_post_lose

    call _bet_cleanup from _call_bet_cleanup
    return


# ── Phase 1: Arrival ──

label _bet_phase_arrival:
    $ print("[BET] Phase: Arrival")

    $ _bet_npc.show_sprite(slot_right)

    $ set_scene_expression(_bet_girl, "smile")
    python:
        _line = _format_partner_line(_bet_girl, _tl(renpy.random.choice(_BET_DIALOGUE["arrival"]["girl_explain"])))
    $ Say_Line(_bet_girl, _line)

    # Girl tells NPC to turn around
    $ set_scene_expression(_bet_girl, "happy")
    $ Say_Line(_bet_girl, _tl(renpy.random.choice(_BET_DIALOGUE["arrival"]["girl_to_npc"])))

    # NPC agrees reluctantly
    $ Say_Line(_bet_npc, _tl(renpy.random.choice(_BET_DIALOGUE["arrival"]["npc_agree"])))

    $ Say_Line(_bet_npc, _tl(renpy.random.choice(_BET_DIALOGUE["arrival"]["npc_turn"])))

    # NPC flips to face away
    $ renpy.show(_bet_npc.image_name(), tag=_bet_npc.image_tag(), at_list=[_bet_slot_right_flipped])
    $ renpy.pause(0.5)

    # Girl whispers to player
    $ set_scene_expression(_bet_girl, "sexy")
    $ Say_Line(_bet_girl, _tl(renpy.random.choice(_BET_DIALOGUE["arrival"]["girl_whisper"])))

    # Strip clothes before sex
    python:
        for _slot in ("over", "mid", "chest", "skirt", "panties", "shoes"):
            if _bet_girl.clothes.get(_slot):
                _bet_girl.clothes[_slot] = None
                _bet_girl.clothes_state[_slot] = "full"

    return


# ── Phase 2: Position pick ──

label _bet_phase_position_pick:
    $ print("[BET] Phase: Position pick. noise=%d" % store._bet_noise)

    python:
        _bet_positions = []
        for _pos in ("cowgirl", "reverse_cowgirl", "doggy", "full_nelson", "laying_down"):
            if girl_has_pose(_bet_girl, _pos) and _pos in _BET_POS_CONFIG:
                _bet_positions.append(_pos)
        print("[BET] Available positions: %s" % _bet_positions)

    menu:
        "Pick a position."

        "Cowgirl" if "cowgirl" in _bet_positions:
            $ store._bet_scene_type = "cowgirl"
        "Reverse Cowgirl" if "reverse_cowgirl" in _bet_positions:
            $ store._bet_scene_type = "reverse_cowgirl"
        "Doggy" if "doggy" in _bet_positions:
            $ store._bet_scene_type = "doggy"
        "Full Nelson" if "full_nelson" in _bet_positions:
            $ store._bet_scene_type = "full_nelson"
        "Laying Down" if "laying_down" in _bet_positions:
            $ store._bet_scene_type = "laying_down"

    # Launch position
    python:
        _pos_cfg = _BET_POS_CONFIG[store._bet_scene_type]
        _cum_c = CUM_POSITION_CONFIG[store._bet_scene_type]
        print("[BET] Launching position: %s" % store._bet_scene_type)

    call expression _pos_cfg["rub_label"] pass (_bet_girl) from _call_bet_rub_launch

    # Transition from rub to sex with condom
    python:
        store.condom_active = True
        _rub_var = _cum_c.get("rub_mode_var")
        if _rub_var:
            setattr(store, _rub_var, False)
        _started_var = _pos_cfg.get("started_var")
        if _started_var:
            setattr(store, _started_var, True)

    call expression _pos_cfg["enter_label"] pass (_bet_girl) from _call_bet_enter_anim

    python:
        _spd_var = _cum_c.get("speed_var")
        if _spd_var:
            setattr(store, _spd_var, 1)
        store._scene_phase = "sex"

    call expression _cum_c["apply_speed_label"] pass (_bet_girl, 1) from _call_bet_apply_speed_init

    # Re-show NPC above sex layers (still facing away)
    $ renpy.show(_bet_npc.image_name(), tag=_bet_npc.image_tag(), at_list=[_bet_slot_right_flipped], zorder=10090)

    $ mark_intimacy(_bet_girl, store._bet_scene_type)

    # Enter sex loop
    $ store._bet_switch_pos = False
    call _bet_sex_loop from _call_bet_sex_loop

    # Switch position loops back without recursion
    if store._bet_switch_pos:
        $ store._bet_switch_pos = False
        jump _bet_phase_position_pick

    # Post-cum bet dialogue (while still in position)
    if store._bet_npc_looked:
        $ set_scene_expression(_bet_girl, "pleasure")
        $ Say_Line(_bet_girl, _format_partner_line(_bet_girl, _BET_DIALOGUE["cum"]["girl_feel"][0]))

    # End position
    python:
        _end_label = CUM_POSITION_CONFIG[store._bet_scene_type]["end_label"]
    call expression _end_label pass (_bet_girl, False) from _call_bet_end_pos

    # Re-show NPC for standing scene (always facing forward — bet is over)
    $ _bet_npc.show_sprite(slot_right)

    return


# ── Sex loop (uses real sex functions) ──

label _bet_sex_loop:
    $ print("[BET] Sex loop start. noise=%d tick=%d npc_looked=%s" % (store._bet_noise, store._bet_tick, store._bet_npc_looked))
    if not store._bet_npc_looked:
        $ unlock_achievement("ntr_listening")

    while True:

        # Exit checks (real menu pattern)
        if store._player_exhausted or store._post_cum_pending:
            return

        # Forced cum at Focus 100 — no choice, auto-creampie (or condom if still on)
        if player_is_cumming():
            $ print("[BET] Focus >= 100! Forcing cum. condom=%s" % store.condom_active)
            $ set_scene_expression(_bet_girl, "moaning")
            python:
                _cum_anim = CUM_POSITION_CONFIG[store._bet_scene_type]["cum_anim"]
                _cum_type = "condom" if store.condom_active else "inside"
            call expression _cum_anim pass (_bet_girl) from _call_bet_forced_cum
            python:
                process_cum(_bet_girl, store._bet_scene_type, _cum_type)
                Player.Focus = 0
                Player.change_energy(-1)
                store._player_exhausted = True
            return

        # Read current speed from position-specific var
        python:
            _spd_var = CUM_POSITION_CONFIG[store._bet_scene_type].get("speed_var")
            _cur_speed = getattr(store, _spd_var, 0) if _spd_var else 0

        # Auto-noise from high speed
        if _cur_speed >= 3 and not store._bet_npc_looked:
            $ store._bet_noise += 1
            $ print("[BET] Auto-noise from speed %d. noise=%d" % (_cur_speed, store._bet_noise))

        # Check if NPC breaks
        if store._bet_noise >= 10 and not store._bet_npc_looked:
            call _bet_npc_looks from _call_bet_npc_looks_trigger

        # Noise milestones
        if store._bet_noise == 5 and not store._bet_npc_looked:
            $ set_scene_expression(_bet_girl, "smirk")
            $ Say_Line(_bet_girl, _format_partner_line(_bet_girl, renpy.random.choice(_BET_DIALOGUE["sex_loop"]["noise_milestone_5"])))

        if store._bet_noise == 8 and not store._bet_npc_looked:
            $ set_scene_expression(_bet_girl, "sexy")
            $ Say_Line(_bet_girl, _format_partner_line(_bet_girl, renpy.random.choice(_BET_DIALOGUE["sex_loop"]["noise_milestone_8"])))

        # Tick counter for exhaustion (only before NPC looks)
        $ store._bet_tick += 1
        if store._bet_tick >= _BET_MAX_TICKS and not store._bet_npc_looked:
            $ set_scene_expression(_bet_girl, "moaning")
            $ renpy.say(None, _tl(_BET_DIALOGUE["exhausted"]["narration"][0]))
            python:
                _cum_anim = CUM_POSITION_CONFIG[store._bet_scene_type]["cum_anim"]
            call expression _cum_anim pass (_bet_girl) from _call_bet_cum_exhaust
            python:
                process_cum(_bet_girl, store._bet_scene_type, "condom")
                Player.Focus = 0
                Player.change_energy(-1)
                store._player_exhausted = True
            return

        python:
            _bet_can_faster = _cur_speed < 3
            _bet_can_slower = _cur_speed > 1

        menu:
            "Keep going":
                call _sex_scene_tick(_bet_girl, store._bet_scene_type, _cur_speed) from _call_sst_bet
                if store._sst_result == "abort":
                    return

            "Speed up" if _bet_can_faster:
                $ advance_round(TIME_COSTS["sex_tick"])
                python:
                    setattr(store, _spd_var, _cur_speed + 1)
                call expression CUM_POSITION_CONFIG[store._bet_scene_type]["apply_speed_label"] pass (_bet_girl, _cur_speed + 1) from _call_bet_speed_up
                call _speed_change_tick(_bet_girl, store._bet_scene_type, 1) from _call_sct_bet_su
                if _scene_should_exit():
                    return

            "Slow down" if _bet_can_slower:
                $ advance_round(1)
                python:
                    setattr(store, _spd_var, _cur_speed - 1)
                call expression CUM_POSITION_CONFIG[store._bet_scene_type]["apply_speed_label"] pass (_bet_girl, _cur_speed - 1) from _call_bet_speed_down
                call _speed_change_tick(_bet_girl, store._bet_scene_type, -1) from _call_sct_bet_sd

            # no Full Nelson spank art (SpankHer would fall into the RCG hand): the regular FN menu never offers it.
            # In cowgirl SpankHer slaps her FACE (SPANK_FACE_SCENES): the button says so, like the regular cowgirl menu
            "Spank her" if store._bet_scene_type != "full_nelson" and store._bet_scene_type not in SPANK_FACE_SCENES:
                $ advance_round(1)
                call SpankHer(_bet_girl, store._bet_scene_type) from _call_SpankHer_bet
                if not store._bet_npc_looked:
                    $ store._bet_noise += 1
                    $ print("[BET] Spank noise. noise=%d" % store._bet_noise)

            "Slap her face" if store._bet_scene_type in SPANK_FACE_SCENES and not getattr(store, "hiding_face", False):
                $ advance_round(1)
                call SpankHer(_bet_girl, store._bet_scene_type) from _call_SpankHer_bet_face
                if not store._bet_npc_looked:
                    $ store._bet_noise += 1
                    $ print("[BET] Face slap noise. noise=%d" % store._bet_noise)

            "Tease her..." if _cur_speed > 0:
                $ advance_round(1)
                call _tease_menu(_bet_girl, store._bet_scene_type) from _call_tease_menu_bet
                if not store._bet_npc_looked:
                    $ store._bet_noise += 1
                    $ print("[BET] Tease noise. noise=%d" % store._bet_noise)

            "Switch position":
                python:
                    _end_label = CUM_POSITION_CONFIG[store._bet_scene_type]["end_label"]
                call expression _end_label pass (_bet_girl, False) from _call_bet_switch_end
                $ store._bet_switch_pos = True
                return


# ── NPC looks (noise >= 10) ──

label _bet_npc_looks:
    $ print("[BET] NPC LOOKS! noise=%d" % store._bet_noise)
    $ store._bet_npc_looked = True

    $ renpy.say(None, _format_partner_line(_bet_girl, _BET_DIALOGUE["npc_looks"]["narration_turn"][0]))

    # NPC flips back to original (now watching) — explicit xzoom 1.0 to override the -1.0
    $ renpy.show(_bet_npc.image_name(), tag=_bet_npc.image_tag(), at_list=[_bet_slot_right_normal], zorder=10090)
    $ renpy.pause(0.5)

    $ set_scene_expression(_bet_girl, "happy")
    $ Say_Line(_bet_girl, _tl(renpy.random.choice(_BET_DIALOGUE["npc_looks"]["girl_victory"])))

    $ Say_Line(_bet_npc, _tl(renpy.random.choice(_BET_DIALOGUE["npc_looks"]["npc_caught"])))

    # Girl announces punishment: condom comes off
    $ set_scene_expression(_bet_girl, "smirk")
    $ Say_Line(_bet_girl, _tl(renpy.random.choice(_BET_DIALOGUE["npc_looks"]["girl_punishment"])))

    $ Say_Line(_bet_npc, _tl(renpy.random.choice(_BET_DIALOGUE["npc_looks"]["npc_react"])))

    $ set_scene_expression(_bet_girl, "sexy")
    $ Say_Line(_bet_girl, _tl(renpy.random.choice(_BET_DIALOGUE["npc_looks"]["girl_dismiss_npc"])))

    # Remove condom
    $ _on_condom_removed(_bet_girl, skip_hide=True, force=True)

    python:
        _cr_label = CUM_POSITION_CONFIG[store._bet_scene_type].get("condom_remove_anim")
    if _cr_label is not None:
        call expression _cr_label pass (_bet_girl) from _call_bet_condom_remove

    $ store._creampie_consent = "allowed"
    $ store._creampie_warned = True

    python:
        _spd_var = CUM_POSITION_CONFIG[store._bet_scene_type].get("speed_var")
        _cur_speed = getattr(store, _spd_var, 0) if _spd_var else 0
    call expression CUM_POSITION_CONFIG[store._bet_scene_type]["apply_speed_label"] pass (_bet_girl, _cur_speed) from _call_bet_apply_speed_raw

    # Re-show NPC above sex layers (now watching)
    $ renpy.show(_bet_npc.image_name(), tag=_bet_npc.image_tag(), at_list=[slot_right], zorder=10090)

    return


# ── Post-scene: Win ──

label _bet_post_win:
    $ print("[BET] Post-scene: WIN")

    $ set_scene_expression(_bet_girl, "happy")
    $ Say_Line(_bet_girl, _format_partner_line(_bet_girl, renpy.random.choice(_BET_DIALOGUE["post_win"]["girl_thanks"])))

    $ Say_Line(_bet_npc, _tl(renpy.random.choice(_BET_DIALOGUE["post_win"]["npc_defeated"])))

    python:
        Change_Status(_bet_girl, "Love", 15)
        Change_Status(_bet_girl, "Obed", 10)
        _bet_npc.change_friendship(30)
        _npc_bar = getattr(_bet_npc, "_ntr_boundary_bar", 0)
        _bet_npc._ntr_boundary_bar = min(100, _npc_bar + 20)
        _ntr_save_state(_bet_npc, _bet_girl)   # NPC_PARTNERS is rebuilt lazily from the girl: without this the +20 was lost
        unlock_achievement("noisy_bet")
        print("[BET] Win rewards: Love+15, Obed+10, NPC friendship+30, boundary_bar+20 (now %d)" % _bet_npc._ntr_boundary_bar)

    return


# ── Post-scene: Lose ──

label _bet_post_lose:
    $ print("[BET] Post-scene: LOSE")

    $ set_scene_expression(_bet_girl, "sad")
    $ Say_Line(_bet_girl, _format_partner_line(_bet_girl, renpy.random.choice(_BET_DIALOGUE["post_lose"]["girl_lose"])))

    python:
        _line = _format_partner_line(_bet_girl, _tl(renpy.random.choice(_BET_DIALOGUE["post_lose"]["girl_consolation"])))
    $ Say_Line(_bet_girl, _line)

    python:
        Change_Status(_bet_girl, "Obed", -10)
        print("[BET] Lose penalty: Obed-10")

    return


# ── Cleanup ──

label _bet_cleanup:
    $ print("[BET] Cleanup")

    python:
        _bet_girl._bet_event_done = True
        _bet_reset_flags("cleanup")
        store._ntr_partner_watching = False
        store._ntr_watching_npc = None

        _bet_npc.hide_sprite()

        print("[BET] Event complete. Girl=%s done=True" % _bet_girl.gid)

    scene black
    with fade
    "You get dressed and leave."
    $ navigate_to("campus", None)
    call Set_Scene(entry=True) from _call_bet_set_scene_exit

    return


# ============================================
# QA TEST: renpy.jump("qa_ntr_bet")
# ============================================

label qa_ntr_bet:
    scene black

    python:
        _qa_bet_girl = None
        for _g in ALL_GIRLS:
            if _g in ALL_GIRLS:
                _qa_bet_girl = _g
                break

        if _qa_bet_girl is None:
            renpy.say(None, "No girl found for testing.")
            renpy.jump("main_loop")

        _qa_bet_girl.Sex_acts["sex"] = max(_qa_bet_girl.Sex_acts.get("sex", 0), 1)
        _qa_bet_girl.Sex_acts["cowgirl"] = max(_qa_bet_girl.Sex_acts.get("cowgirl", 0), 1)

        if not _qa_bet_girl.has_npc_partner():
            # NEW partner: set_npc_partner() wipes the per-partner mirrors and creates the NPC itself
            _qa_bet_girl.set_npc_partner(_qa_bet_girl.npc_partner_canonical_id("male"), gender="male")
        _qa_npc = get_npc_partner_for(_qa_bet_girl)
        print("[QA_BET] %s: test partner = %s" % (_qa_bet_girl.gid, getattr(_qa_npc, "name", None)))

        _qa_npc._ntr_active = True
        _qa_npc._ntr_boundary_discovered = True
        _qa_npc._ntr_boundary_level = 2
        _qa_npc._ntr_boundary_bar = 0
        _qa_npc.friendship_with_player = 500
        _qa_npc.love_for_girl = 750
        _ntr_save_state(_qa_npc, _qa_bet_girl)

        _qa_love_before = _qa_bet_girl.Love
        _qa_obed_before = _qa_bet_girl.Obed
        _qa_friend_before = _qa_npc.friendship_with_player
        _qa_boundary_before = _qa_npc._ntr_boundary_bar

        store._bet_girl_gid = _qa_bet_girl.gid
        store._bet_scheduled_day = store.Day
        store._bet_cooldown_until = -1

        print("[QA_BET] Setup done: girl=%s npc=%s" % (_qa_bet_girl.gid, _qa_npc.name))

    "[_qa_bet_girl.Name] configured: NPC [_qa_npc.name] with NTR active, boundary level 2."
    "Stats before: Love=[_qa_love_before], Obed=[_qa_obed_before]"
    "NPC before: boundary_bar=[_qa_boundary_before], friendship=[_qa_friend_before]"

    call ntr_bet_check from _call_qa_bet_check

    jump qa_ntr_bet.results


label .results:
    python:
        _qa_r_girl = GIRL_BY_ID.get(store._bet_girl_gid) or _qa_bet_girl
        _qa_r_npc = get_npc_partner_for(_qa_r_girl)
        _qa_r_love = _qa_r_girl.Love
        _qa_r_obed = _qa_r_girl.Obed
        _qa_r_boundary = getattr(_qa_r_npc, "_ntr_boundary_bar", -1) if _qa_r_npc else -1
        _qa_r_friend = getattr(_qa_r_npc, "friendship_with_player", -1) if _qa_r_npc else -1
        _qa_r_done = getattr(_qa_r_girl, "_bet_event_done", False)
        _qa_r_locked = getattr(store, "_time_locked", False)
        _qa_r_looked = getattr(store, "_bet_last_looked", False)   # _bet_npc_looked is reset by the cleanup

    "== RESULTS =="
    "Girl: Love [_qa_love_before]->[_qa_r_love], Obed [_qa_obed_before]->[_qa_r_obed]"
    "NPC: boundary_bar [_qa_boundary_before]->[_qa_r_boundary], friendship [_qa_friend_before]->[_qa_r_friend]"
    "NPC looked: [_qa_r_looked] | Event done: [_qa_r_done]"
    "Time locked (should be False): [_qa_r_locked]"

    menu:
        "Run again (full reset)":
            python:
                _qa_bet_girl._bet_event_done = False
                store._bet_scheduled_day = -1
                store._bet_girl_gid = None
                store._bet_cooldown_until = -1
            jump qa_ntr_bet
        "Done":
            return
