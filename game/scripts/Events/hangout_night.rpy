# ============================================================
# HANGOUT NIGHT EVENT
# Group hangout in the player's room with drinks, chat,
# and truth-or-dare.
#
# TOGGLE: Set HANGOUT_ENABLED = False to disable entirely.
# ============================================================

init python:

    # ── Master toggle ──────────────────────────────────────
    HANGOUT_ENABLED = True

    # ── Alcohol level (0-10) per participant ───────────────
    # Stored on Girl objects and Player during the event.
    # Reset at event end.

    def _hangout_base_check(group):
        """Shared checks for hangout invite (ignoring bottle)."""
        if not HANGOUT_ENABLED:
            return False
        if getattr(store, "_hangout_scheduled_day", -1) == store.Day:
            return False
        if store.TimeIndex >= NIGHT_INDEX:
            return False
        return True

    def hangout_can_invite(group):
        """Full check: base conditions + has a bottle."""
        if not _hangout_base_check(group):
            return False
        if not player_has_any_drink():
            return False
        return True

    def hangout_can_invite_no_bottle(group):
        """Base conditions pass but player has no bottle (gray-out state)."""
        if not _hangout_base_check(group):
            return False
        return not player_has_any_drink()

    def hangout_already_invited_today():
        """True when the player already sent an invite today (button stays gray)."""
        if not HANGOUT_ENABLED:
            return False
        return getattr(store, "_hangout_scheduled_day", -1) == store.Day

    def hangout_too_late():
        """True when it's night and no invite was sent today."""
        if not HANGOUT_ENABLED:
            return False
        if getattr(store, "_hangout_scheduled_day", -1) == store.Day:
            return False
        return store.TimeIndex >= NIGHT_INDEX

    def _hangout_girls_list():
        """Canonical list of participating girls (excludes NPC). Safe for iteration."""
        gl = getattr(store, "_hangout_girls", None)
        if gl:
            return list(gl)
        out = []
        for _alias in ("_hangout_girl_a", "_hangout_girl_b", "_hangout_girl_c"):
            _ag = getattr(store, _alias, None)
            if _ag:
                out.append(_ag)
        return out

    def _live_hangout_girls():
        """_hangout_girls_list, but only while the hangout event is RUNNING. The scheduled
        roster is set when the invite is accepted and used to survive a missed night; the
        scene abort / guilt handlers read THIS so a solo scene never 'returns to the hangout'."""
        if not getattr(store, "_hangout_running", False):
            return []
        return _hangout_girls_list()

    def _sync_hangout_girl_aliases():
        """Keep legacy _hangout_girl_a/b/c in sync with _hangout_girls."""
        gl = getattr(store, "_hangout_girls", None) or []
        store._hangout_girl_a = gl[0] if len(gl) > 0 else None
        store._hangout_girl_b = gl[1] if len(gl) > 1 else None
        store._hangout_girl_c = gl[2] if len(gl) > 2 else None

    _HANGOUT_POSITIONS = None
    _HANGOUT_XALIGNS = [0.60, 0.90, 0.35]

    def _hangout_pos_for(girl):
        """Return the named position transform for a girl based on her index in _hangout_girls."""
        global _HANGOUT_POSITIONS
        if _HANGOUT_POSITIONS is None:
            _HANGOUT_POSITIONS = [hangout_pos_a, hangout_pos_b, hangout_pos_c]
        girls = _hangout_girls_list()
        for i, g in enumerate(girls):
            if g.gid == girl.gid and i < len(_HANGOUT_POSITIONS):
                return _HANGOUT_POSITIONS[i]
        return hangout_pos_a

    def _hangout_npc_pos():
        """Return the hangout position for the NPC (slot after last girl)."""
        global _HANGOUT_POSITIONS
        if _HANGOUT_POSITIONS is None:
            _HANGOUT_POSITIONS = [hangout_pos_a, hangout_pos_b, hangout_pos_c]
        girls = _hangout_girls_list()
        _npc_slot = len(girls)
        if _npc_slot < len(_HANGOUT_POSITIONS):
            return _HANGOUT_POSITIONS[_npc_slot]
        return hangout_pos_c

    def _hangout_npc_xalign():
        """Return the xalign float for the NPC's hangout slot."""
        girls = _hangout_girls_list()
        _npc_slot = len(girls)
        if _npc_slot < len(_HANGOUT_XALIGNS):
            return _HANGOUT_XALIGNS[_npc_slot]
        return 0.35

    def _hangout_xalign_for(girl):
        """Return the xalign float for inline Transform usage."""
        girls = _hangout_girls_list()
        for i, g in enumerate(girls):
            if g.gid == girl.gid and i < len(_HANGOUT_XALIGNS):
                return _HANGOUT_XALIGNS[i]
        return 0.60

    def hangout_girl_accepts(girl, other_girl, brought_drink=None):
        """Decide if a girl accepts the hangout invite.
        - Love >= 500 OR Obed >= 500: always accepts (unless hostile / she hates the bottle)
        - Otherwise: scaled chance from Love + Girl_like + the bottle the player brings
        """
        if girl_is_away(girl):   # single gate of every hangout invite (group chat + partner group)
            print("[hangout] %s refuses hangout invite (away, giving birth)" % girl.gid)
            return False
        if girl_type(girl) != "student":
            # The dorm drinking night is a STUDENT thing (author 2026-10-10, "apenas estudantes"): a woman
            # of the house or a teacher never comes, whatever her stats. The invite button never hides;
            # her decline text speaks in her own voice (pool "hangout_not_student").
            print("[hangout] %s refuses hangout invite (type %s, students only)" % (girl.gid, girl_type(girl)))
            return False
        if getattr(girl, "_pregnant", False) and getattr(girl, "_pregnancy_known", False):
            # A known pregnancy keeps her out of the drinking night (author 2026-10-11): she can
            # still be invited, but she declines and says why (pool "hangout_pregnant"). Before
            # the discovery she does not know she is pregnant, so nothing changes for her.
            print("[hangout] %s refuses hangout invite (pregnant, she knows)" % girl.gid)
            return False
        if girl.is_dating_player() and getattr(girl, "Jealousy", 0) >= 600:
            if not (girl.has_trait("polyamorous") or is_player_harem_exempt(other_girl)):
                print("[hangout] %s refuses hangout invite (Jealousy %d >= 600)" % (girl.gid, girl.Jealousy))
                return False

        love = getattr(girl, "Love", 0)
        obed = getattr(girl, "Obed", 0)
        like_other = int(girl.Girl_like.get(other_girl.gid, 500)) if other_girl is not None else 500

        # The bottle the player is bringing nudges her willingness (see alcohol.rpy):
        # her favorite brand > her favorite type > neutral > a type she hates.
        if brought_drink is None:
            brought_drink = getattr(store, "_hangout_brought_drink", None)
        _dcat = drink_reaction(girl, brought_drink) if brought_drink else "neutral"
        _dmod = DRINK_ACCEPT_MOD.get(_dcat, 0.0)

        # Auto-accept if Love or Obed >= 500 (unless she hates the other girl OR the bottle)
        if (love >= 500 or obed >= 500) and like_other >= 250 and _dcat != "hate":
            return True

        # Base chance from Love (0-500 mapped to 30%-95%)
        base = 0.30 + (love / 500.0) * 0.65

        # Obed boost
        if obed >= 300:
            base += 0.20

        # Modifier from how much she likes the other girl
        if like_other < 250:
            base -= 0.40
        elif like_other < 500:
            base -= 0.10
        elif like_other >= 750:
            base += 0.15

        # Brought-bottle modifier
        base += _dmod

        # Clamp
        base = max(0.05, min(0.95, base))

        return renpy.random.random() < base

    def hangout_reset_alcohol():
        """Reset alcohol levels for everyone after the event."""
        store._hangout_player_alcohol = 0
        for g in store.ALL_GIRLS:
            if hasattr(g, "_hangout_alcohol"):
                g._hangout_alcohol = 0

    def hangout_add_alcohol(girl, amount=2):
        """Add alcohol to a girl (capped at DRUNK_MAX). Delegates to the
        central drunkenness meter (see alcohol.rpy)."""
        return add_drunk(girl, amount)

    def hangout_add_player_alcohol(amount=2):
        """Add alcohol to the player (capped at DRUNK_MAX)."""
        cur = getattr(store, "_hangout_player_alcohol", 0)
        store._hangout_player_alcohol = min(DRUNK_MAX, cur + amount)

    def hangout_get_alcohol(girl):
        """Get a girl's current alcohol level."""
        return get_drunk(girl)

    def hangout_get_player_alcohol():
        """Get the player's current alcohol level."""
        return getattr(store, "_hangout_player_alcohol", 0)

# ============================================================
# Slide-in transforms for hangout arrival
# ============================================================
transform hangout_enter_a:
    xalign 1.4
    yalign 2.0
    ease 0.7 xalign 0.60

transform hangout_enter_b:
    xalign 1.6
    yalign 2.0
    pause 0.25
    ease 0.7 xalign 0.90

transform hangout_pos_a:
    xalign 0.60
    yalign 2.0

transform hangout_pos_b:
    xalign 0.90
    yalign 2.0

transform hangout_enter_c:
    xalign -0.6
    yalign 2.0
    pause 0.45
    ease 0.7 xalign 0.35

transform hangout_pos_c:
    xalign 0.35
    yalign 2.0

# ============================================================
# Default variables
# ============================================================
default _hangout_scheduled_day = -1
default _hangout_group_id = None
default _hangout_members = []
default _hangout_player_alcohol = 0
default _hangout_accepted = []
default _hangout_girls = []
default _hangout_running = False   # True only between hangout_night_event start and its cleanup
default _hangout_girl_a = None
default _hangout_girl_b = None
default _hangout_girl_c = None
default _hangout_brought_drink = None
default _hangout_is_harem_night = False
default _hangout_partner_npc = None
default _hangout_partner_npc_id = None
default _tod_ended_sick = None
default _npc_passed_out = False

# Pulse the bar when a person is in the danger zone (>= TOD_SICK_START)
transform tod_danger_blink:
    alpha 1.0
    easein 0.45 alpha 0.3
    easeout 0.45 alpha 1.0
    repeat

transform tod_no_blink:
    alpha 1.0

# ============================================================
# Drunk-level HUD for Truth or Dare
# Small card (matches the energy card), one slim vertical bar per person.
# Fills with alcohol, NO numbers. Bar + initial use each girl's color.
# ============================================================
screen tod_drunk_bars():
    zorder 55
    frame:
        yalign 0.0
        xalign 1.0
        yoffset 20
        xoffset -265
        background Frame("images/menus/GirlsCard_Blue.png", 10, 10, 10, 10)
        padding (14, 10, 14, 10)
        vbox:
            spacing 6
            xalign 0.5
            text _tr("Drink Level"):
                size 14
                color "#e2e8f0"
                bold True
                xalign 0.5
            hbox:
                spacing 12
                yalign 1.0
                for _tb_lvl, _tb_lbl, _tb_col in tod_bar_data():
                    $ _tb_danger = _tb_lvl >= TOD_SICK_START
                    vbox:
                        spacing 3
                        fixed:
                            at (tod_danger_blink if _tb_danger else tod_no_blink)
                            xsize 14
                            ysize 54
                            add Solid("#00000055")
                            if _tb_lvl > 0:
                                fixed:
                                    yalign 1.0
                                    xsize 14
                                    ysize int(54 * max(0.06, min(1.0, _tb_lvl / float(DRUNK_MAX))))
                                    add Solid(_tb_col)
                        text "[_tb_lbl]":
                            size 14
                            color _tb_col
                            bold True
                            xalign 0.5

# ============================================================
# PHONE: Send hangout invite (called from group chat flow)
# ============================================================
label hangout_send_invite(group):
    $ print("[HANGOUT_INVITE] ENTER group=%s members=%s" % (group.get("id", "?"), group.get("members", [])))
    python:
        _h_members = group["members"]
        _h_girls = []
        _h_invite_npc = None
        for _hgid in _h_members:
            if str(_hgid).startswith("npc_"):
                _h_invite_npc = NPC_PARTNERS.get(_hgid)
            else:
                _hg = GIRL_BY_ID.get(_hgid)
                if _hg:
                    _h_girls.append(_hg)

        print("[HANGOUT_INVITE] girls=%d npc=%s members=%d" % (len(_h_girls), getattr(_h_invite_npc, "name", None), len(_h_members)))

        if len(_h_girls) < 2:
            phone_group_add_msg(group["id"], "system", _("You need at least 2 members for a hangout."), "system")
            print("[HANGOUT_INVITE] NOT ENOUGH GIRLS, jumping to .done")
            renpy.jump("hangout_send_invite.done")

        # Check which drinks the player owns
        _h_owned = player_owned_drinks()
        print("[HANGOUT_INVITE] owned drinks=%s" % str(_h_owned))
        if len(_h_owned) <= 1:
            store._h_bottle = _h_owned[0][0] if _h_owned else None
        else:
            store._h_bottle = None
            store._h_bottle_choices = []
            for _bid, _bcnt in _h_owned:
                _binfo = drink_info(_bid)
                _blbl = _tr(_binfo["label"]) if _binfo else _tr("Drinks")
                store._h_bottle_choices.append((_tl(_("Bring %s")) % _blbl, _bid))

    # If multiple drinks, let the player pick
    if getattr(store, "_h_bottle_choices", None):
        call screen phone_group_chat_screen(group, choices=store._h_bottle_choices)
        $ store._h_bottle = _return
        $ store._h_bottle_choices = None

    # Send the invite with the selected bottle
    python:
        _h_bottle = store._h_bottle
        print("[HANGOUT_INVITE] bottle selected=%s" % _h_bottle)
        store._hangout_brought_drink = _h_bottle
        _h_bring = drink_bring_phrase(_h_bottle) if _h_bottle else _tl(_("some drinks"))
        if _h_invite_npc:
            phone_group_add_msg(group["id"], "player",
                _tl(_("Hey girls, come to my room tonight for some drinks? Bring %s along! I got %s.")) % (_h_invite_npc.Name, _h_bring),
                "text")
        else:
            phone_group_add_msg(group["id"], "player",
                _tl(_("Hey girls, come to my room tonight for some drinks and fun? I brought %s, we can share.")) % _h_bring,
                "text")
        player_consume_drink(_h_bottle)
        store._hangout_scheduled_day = store.Day
        print("[HANGOUT_INVITE] bottle=%s day=%d msg sent" % (_h_bottle, store.Day))

    # Show player message
    $ print("[HANGOUT_INVITE] showing player msg screen")
    call screen phone_group_chat_screen(group, auto_close=0.6)

    # Each girl responds in order
    python:
        _h_accept_pools = [
            [
                _("Sounds fun! I'm in."),
                _("Ooh, drinks? Count me in!"),
                _("Sure, why not? I could use a good night."),
                _("A party? I'm there!"),
                _("Yesss! What time?"),
            ],
            [
                _("I'm down! See you tonight~"),
                _("Absolutely! This is going to be great."),
                _("Count me in too!"),
                _("Sounds like a plan!"),
                _("Let's do it!"),
            ],
            [
                _("This sounds amazing! I'm coming!"),
                _("Drinks with you guys? Say no more."),
                _("I'll be there! Save me a seat."),
            ],
        ]
        _h_decline_pools = [
            [
                _("Hmm... I don't think I can tonight. Sorry."),
                _("Not really feeling it today. Maybe another time?"),
                _("I'll pass this time. Have fun though!"),
                _("Sorry, I've got other plans tonight."),
                _("I'm not in the mood, sorry."),
            ],
            [
                _("I think I'll sit this one out. Sorry!"),
                _("Not tonight for me... rain check?"),
                _("Ehh, I'm kind of tired. Next time!"),
                _("Sorry, can't make it tonight."),
                _("I'll have to pass, but have fun!"),
            ],
            [
                _("Not tonight, sorry! Have fun without me."),
                _("I'm going to pass this time. Next time for sure!"),
                _("Can't make it, but you guys have a great night."),
            ],
        ]
        _h_girl_accepts = {}

    $ _h_gi = 0
    while _h_gi < len(_h_girls):
        $ _h_cur = _h_girls[_h_gi]
        $ _h_pool_idx = min(_h_gi, len(_h_accept_pools) - 1)
        $ phone_group_add_msg(group["id"], _h_cur.gid, None, "typing")
        call screen phone_group_chat_screen(group, auto_close=renpy.random.uniform(1.0, 1.8))
        python:
            _g_msgs = phone_group_get_msgs(group["id"])
            if _g_msgs and _g_msgs[-1].get("type") == "typing":
                _g_msgs.pop()
            _other = [g for g in _h_girls if g.gid != _h_cur.gid]
            _h_cur_accepts = hangout_girl_accepts(_h_cur, _other[0] if _other else None)
            _h_cur_away = girl_is_away(_h_cur)
            _h_cur_student = girl_type(_h_cur) == "student"
            _h_cur_pregnant = getattr(_h_cur, "_pregnant", False) and getattr(_h_cur, "_pregnancy_known", False)
            # away, not a student or pregnant: she answers with no comment on a bottle she will not drink
            _h_cur_react = None if (_h_cur_away or not _h_cur_student or _h_cur_pregnant) else drink_event_greeting(_h_cur, getattr(store, "_hangout_brought_drink", None))
            if _h_cur_accepts:
                _h_cur_msg = _tl(renpy.random.choice(_h_accept_pools[_h_pool_idx]))
            elif _h_cur_away:
                _h_cur_msg = _tl(renpy.random.choice(FOLLOW_INVITE_DECLINE["away"]))
            elif not _h_cur_student:
                # students only (author 2026-10-10): her own voice, girl -> role -> Global
                # (rod_pick_line comes back translated: no _tl here)
                _h_cur_msg = rod_pick_line(_h_cur, "hangout_not_student")
            elif _h_cur_pregnant:
                # she knows she is pregnant (author 2026-10-11): no alcohol for her, and she says so
                _h_cur_msg = rod_pick_line(_h_cur, "hangout_pregnant")
            else:
                _h_cur_msg = _tl(renpy.random.choice(_h_decline_pools[_h_pool_idx]))
            if _h_cur_react:
                _h_cur_msg = _h_cur_react + " " + _h_cur_msg
            phone_group_add_msg(group["id"], _h_cur.gid, _h_cur_msg, "text")
            _h_girl_accepts[_h_cur.gid] = _h_cur_accepts
        call screen phone_group_chat_screen(group, auto_close=0.5)
        $ _h_gi += 1

    # NPC tags along if his GF accepted
    if _h_invite_npc is not None:
        python:
            _npc_gf_accepted = False
            if hasattr(_h_invite_npc, "girl_gid"):
                _npc_gf_accepted = _h_girl_accepts.get(_h_invite_npc.girl_gid, False)
        if _npc_gf_accepted:
            $ phone_group_add_msg(group["id"], _h_invite_npc.gid, None, "typing")
            call screen phone_group_chat_screen(group, auto_close=renpy.random.uniform(0.9, 1.6))
            python:
                _g_msgs = phone_group_get_msgs(group["id"])
                if _g_msgs and _g_msgs[-1].get("type") == "typing":
                    _g_msgs.pop()
                _npc_gf_obj = GIRL_BY_ID.get(_h_invite_npc.girl_gid)
                _npc_tag_raw = _tl(renpy.random.choice(PARTNER_ACCOMPANY_NPC_LINES[_partner_npc_friend_key(_h_invite_npc)]))
                phone_group_add_msg(group["id"], _h_invite_npc.gid, _format_npc_line(_h_invite_npc, _npc_tag_raw, _npc_gf_obj), "text")
            call screen phone_group_chat_screen(group, auto_close=0.5)

    python:
        _hangout_accepted_list = [g for g in _h_girls if _h_girl_accepts.get(g.gid, False)]

        if len(_hangout_accepted_list) < 2:
            if len(_hangout_accepted_list) == 0:
                phone_group_add_msg(group["id"], "system", _("Nobody's coming tonight. The hangout is off."), "system")
            else:
                _solo_name = _hangout_accepted_list[0].Name
                phone_group_add_msg(group["id"], "system",
                    _tl(_("Only %s accepted. You need at least two for a hangout. Maybe next time.")) % _solo_name,
                    "system")
            _refund_drink = getattr(store, "_hangout_brought_drink", "drinks")
            store.Player.add_item(_refund_drink if _refund_drink else "drinks", 1)
        else:
            store._hangout_group_id = group["id"]
            store._hangout_members = [g.gid for g in _hangout_accepted_list]
            store._hangout_girls = list(_hangout_accepted_list)
            _sync_hangout_girl_aliases()
            store._hangout_is_harem_night = False
            if len(store._hangout_girls) >= 2:
                _hn_all_dating = all(_hng.is_dating_player() for _hng in store._hangout_girls)
                if _hn_all_dating:
                    _hn_all_exempt = True
                    for _hni, _hng1 in enumerate(store._hangout_girls):
                        for _hng2 in store._hangout_girls[_hni+1:]:
                            if not is_harem_exempt(_hng1, _hng2):
                                _hn_all_exempt = False
                                break
                        if not _hn_all_exempt:
                            break
                    store._hangout_is_harem_night = _hn_all_exempt
                    if store._hangout_is_harem_night:
                        print("[HANGOUT] Harem night detected: %s" % [_hng.gid for _hng in store._hangout_girls])
            # NPC joins if his GF is in the accepted list AND there's screen space
            if _h_invite_npc and _npc_gf_accepted and len(_hangout_accepted_list) < 3:
                store._hangout_partner_npc = _h_invite_npc
                store._hangout_partner_npc_id = getattr(_h_invite_npc, "partner_id", None)
            phone_group_add_msg(group["id"], "player", _("Awesome! See you tonight then!"), "text")
            phone_group_add_msg(group["id"], "system", _("Hangout scheduled for tonight!"), "system")

    call screen phone_group_chat_screen(group, auto_close=0.8)

    label .done:
        return

# ============================================================
# NIGHT CHECK: Called from Wait label to trigger the event
# ============================================================
label hangout_night_check:
    if not HANGOUT_ENABLED:
        return
    if _hangout_scheduled_day not in (-1, Day):
        # the scheduled night was missed: the stale roster blocked partner walk-ins
        # (npc_partner_witness_check) and fed the scene-abort hangout branches
        python:
            store._hangout_scheduled_day = -1
            store._hangout_members = []
            store._hangout_girls = []
            store._hangout_girl_a = None
            store._hangout_girl_b = None
            store._hangout_girl_c = None
            print("[HANGOUT] missed night: stale roster cleared")
        return
    if _hangout_scheduled_day != Day:
        return
    if TimeIndex != NIGHT_INDEX:
        return
    if not _hangout_members:
        return

    # Event is scheduled for tonight!
    if CurrentLocation != "room":
        $ Narration(_("You remember you have a hangout tonight with the girls. You should head to your room."))
        $ navigate_to("room", None)
        call Set_Scene(entry=False) from _call_hangout_set_scene_1

    # Start the event
    call hangout_night_event from _call_hangout_night_event
    return

# ============================================================
# MAIN EVENT: The hangout itself
# ============================================================
label hangout_night_event:

    $ store._in_event = True
    $ store._hangout_running = True
    $ store._in_sandbox = False
    $ debug_log("[STATE] _in_event = True, _in_sandbox = False (hangout_night_event)")

    python:
        # Initialize alcohol levels
        store._hangout_player_alcohol = 0
        store._tod_ended_sick = None
        store._nhie_used_ids = set()
        _h_ga = store._hangout_girl_a
        _h_gb = store._hangout_girl_b
        _h_gc = store._hangout_girl_c
        _h_all = _hangout_girls_list()
        _h_count = len(_h_all)
        for _ig in _h_all:
            _ig._hangout_alcohol = 0
            _ig.loc = "room"
            _ig.WearPreset("casual", apply_now=False)
            setattr(store, "_hangout_strip_level_" + _ig.gid, 0)
        renpy.show_screen("tod_drunk_bars")

        store._h_npc = getattr(store, "_hangout_partner_npc", None)
        store._npc_passed_out = False
        if store._h_npc:
            store._h_npc.loc = "room"
            store._h_npc._hangout_alcohol = 0

    # Scene setup
    scene black
    with fade
    pause 0.3

    $ Narration(_("Later that evening..."))

    # Show the player's room
    $ navigate_to("room", None)
    call Set_Scene(entry=False, show_chars=False, quiet=True) from _call_hangout_set_scene_2

    # Girls arrive (unified path for 2-3 girls + optional NPC)
    if _h_count >= 2 and store._h_npc is None:
        play sound "audio/Knock.mp3" noloop
        $ Narration(_("Someone knocks on your door."))

        python:
            _enter_tfs = [hangout_enter_a, hangout_enter_b, hangout_enter_c]
            _pos_tfs = [hangout_pos_a, hangout_pos_b, hangout_pos_c]
            for _eg in _h_all:
                _gen = store._standing_blink_gen.get(_eg.gid, 0) + 1
                store._standing_blink_gen[_eg.gid] = _gen
            for _ei, _eg in enumerate(_h_all):
                if _ei < len(_enter_tfs):
                    set_girl_sprite(_eg.gid, pose="standing", at_list=[_enter_tfs[_ei]])
        pause 1.2
        python:
            for _ei, _eg in enumerate(_h_all):
                if _ei < len(_pos_tfs):
                    sprite_state.setdefault(_eg.Id, {})["_last_at_list"] = [_pos_tfs[_ei]]

        python:
            _arrive_pools = [
                [
                    _("Hey! We're here!"),
                    _("We made it!"),
                    _("Hope you're ready for us!"),
                    _("Okay, we're here. Let's do this!"),
                ],
                [
                    _("This is going to be fun."),
                    _("Finally! I've been looking forward to this."),
                    _("Hey! Nice place."),
                    _("I brought good vibes, that's all I need."),
                ],
                [
                    _("I'm so excited for tonight!"),
                    _("This is going to be a great night."),
                    _("Hey! Glad I could make it."),
                ],
            ]
            _arrive_exprs = ["happy", "smile", "surprised"]
            for _ai, _ag in enumerate(_h_all):
                set_scene_expression(_ag, _arrive_exprs[min(_ai, len(_arrive_exprs) - 1)])
                _ap = _arrive_pools[min(_ai, len(_arrive_pools) - 1)]
                Say_Line(_ag, _tl(renpy.random.choice(_ap)))

        $ Say_Player(_("Come in! I've got everything set up."))

        if _h_count == 3:
            $ Narration(_("The four of you settle in. You pull out the bottle and some glasses."))
        else:
            $ Narration(_("The three of you settle in. You pull out the bottle and some glasses."))

        python:
            _settle_pools = [
                [
                    _("Hey, what kind of drinks did you get?"),
                    _("Ooh, nice setup. I'm impressed."),
                    _("Wait, is that a real bottle? Fancy!"),
                    _("Love the decoration in here."),
                ],
                [
                    _("Let me connect my music app, I'll put on something good."),
                    _("Don't be stingy with the drinks~"),
                    _("What is your wifi password again?"),
                    _("I call dibs on the comfy spot!"),
                ],
                [
                    _("This place is actually cozy."),
                    _("I'm already having a good time."),
                    _("So, what's the plan for tonight?"),
                ],
            ]
            _settle_exprs = ["smile", "smirk", "normal"]
            for _si, _sg in enumerate(_h_all):
                set_scene_expression(_sg, _settle_exprs[min(_si, len(_settle_exprs) - 1)])
                _sp = _settle_pools[min(_si, len(_settle_pools) - 1)]
                Say_Line(_sg, _tl(renpy.random.choice(_sp)))

        $ unlock_achievement("girls_night")
        if _h_count >= 3:
            $ unlock_achievement("party_for_three")

        $ Narration(_("You pour drinks for everyone and raise your glass."))

        $ Say_Player(_("To a great night!"))

        python:
            for _cg in _h_all:
                set_scene_expression(_cg, "happy")
                Say_Line(_cg, _tl(_("Cheers!")))

        python:
            for _g in _h_all:
                tod_drink(_g, 1)
            tod_drink_player(1)

    elif _h_ga is not None and store._h_npc is not None:
        play sound "audio/Knock.mp3" noloop

        if _h_count >= 2:
            # Multi-girl + NPC
            python:
                _npc_name = store._h_npc.Name
                _enter_tfs = [hangout_enter_a, hangout_enter_b, hangout_enter_c]
                _pos_tfs = [hangout_pos_a, hangout_pos_b, hangout_pos_c]
                _npc_slot = _h_count
                for _ei, _eg in enumerate(_h_all):
                    if _ei < len(_enter_tfs):
                        set_girl_sprite(_eg.gid, pose="standing", at_list=[_enter_tfs[_ei]])
                if _npc_slot < len(_enter_tfs):
                    store._h_npc.show_sprite(_enter_tfs[_npc_slot])
            $ Narration(_("Someone knocks on your door."))
            pause 0.8
            python:
                for _ei, _eg in enumerate(_h_all):
                    if _ei < len(_pos_tfs):
                        sprite_state.setdefault(_eg.Id, {})["_last_at_list"] = [_pos_tfs[_ei]]
                if _npc_slot < len(_pos_tfs):
                    store._h_npc.show_sprite(_pos_tfs[_npc_slot])

            python:
                _arrive_pools = [
                    [
                        _("Hey! We're here!"),
                        _("We made it!"),
                        _("Hope you're ready for us!"),
                    ],
                    [
                        _("This is going to be fun."),
                        _("Finally! I've been looking forward to this."),
                        _("Hey! Nice place."),
                    ],
                    [
                        _("I'm so excited for tonight!"),
                        _("Glad I could make it!"),
                    ],
                ]
                for _ai, _ag in enumerate(_h_all):
                    _ap = _arrive_pools[min(_ai, len(_arrive_pools) - 1)]
                    Say_Line(_ag, _tl(renpy.random.choice(_ap)))
                _npc_gf_obj = GIRL_BY_ID.get(store._h_npc.girl_gid) if hasattr(store._h_npc, "girl_gid") else _h_ga
                _php_arr_npc = _format_npc_line(store._h_npc, _tl(renpy.random.choice(PARTNER_ACCOMPANY_NPC_LINES[_partner_npc_friend_key(store._h_npc)])), _npc_gf_obj)
            $ Say_Line(store._h_npc, _php_arr_npc)
            $ Say_Player(_("Come in! I've got everything set up."))
            $ unlock_achievement("cups_and_hangout")
            if _h_count == 2:
                $ Narration(_("The four of you settle in. You pour drinks."))
            else:
                $ Narration(_("Everyone settles in. You pour drinks."))
            python:
                for _g in _h_all:
                    tod_drink(_g, 1)
                tod_drink(store._h_npc, 1)
                tod_drink_player(1)
        else:
            # Legacy: 1 girl + her partner NPC
            $ _h_name_a = _h_ga.Name
            $ Narration(_tl(_("Someone knocks. %s and %s are here.")) % (_h_ga.Name, store._h_npc.Name))
            $ set_girl_sprite(_h_ga.gid, pose="standing", at_list=[hangout_enter_a])
            $ store._h_npc.show_sprite(hangout_enter_b)
            pause 0.8
            $ sprite_state.setdefault(_h_ga.Id, {})["_last_at_list"] = [hangout_pos_a]
            $ store._h_npc.show_sprite(hangout_pos_b)

            python:
                _php_arr_girl = _tl(renpy.random.choice([
                    _("Hey! Thanks for having us."),
                    _("We made it! This should be fun."),
                    _("Hope you don't mind us both crashing your place~"),
                ]))
                _php_arr_npc = _format_npc_line(store._h_npc, _tl(renpy.random.choice(PARTNER_ACCOMPANY_NPC_LINES[_partner_npc_friend_key(store._h_npc)])), _h_ga)
            $ Say_Line(_h_ga, _php_arr_girl)
            $ Say_Line(store._h_npc, _php_arr_npc)
            $ Say_Player(_("Come in, both of you! Drinks are ready."))
            $ Narration(_("The three of you settle in. You pour drinks."))
            python:
                tod_drink(_h_ga, 1)
                tod_drink(store._h_npc, 1)
                tod_drink_player(1)

    label .hangout_loop:
        python:
            _p_alc = hangout_get_player_alcohol()
            _h_girls_here = _hangout_girls_list()
            _h_count_here = len(_h_girls_here)
            _h_alc_list = [hangout_get_alcohol(g) for g in _h_girls_here]
            _h_name_list = [g.Name for g in _h_girls_here]
            # Keep legacy vars for backward compat
            _a_alc = _h_alc_list[0] if _h_count_here > 0 else 0
            _b_alc = _h_alc_list[1] if _h_count_here > 1 else 0
            _h_name_a = _h_name_list[0] if _h_count_here > 0 else "???"
            _h_name_b = _h_name_list[1] if _h_count_here > 1 else "???"

        # Check if someone hit the danger zone -- force wind down
        if _p_alc >= TOD_SICK_START or any(hangout_get_alcohol(g) >= TOD_SICK_START for g in _h_girls_here):
            $ Narration(_("You can tell at least one of them has had more than enough to drink for tonight."))
            $ Narration(_("You decide it is better to start winding things down before the night gets out of hand."))
            jump .hangout_end

        # Ambient line (player + girls + NPC if conscious)
        $ _total_present = 1 + _h_count_here + (1 if _npc_is_active() else 0)
        if _total_present >= 4:
            $ Narration(_("The music keeps playing while the four of you hang out, and you decide what to do next."))
        elif _total_present == 3:
            $ Narration(_("The music keeps playing while the three of you hang out, and you decide what to do next."))
        else:
            $ Narration(_("The music keeps playing while the two of you hang out, and you decide what to do next."))

        # Per-girl alcohol hints
        python:
            _alc_hint_pools = {
                11: [
                    _tl(_("%s has gone pale and clammy, swallowing hard like she might be sick any minute.")),
                    _tl(_("%s looks a little green, breathing carefully like one wrong move will tip her over.")),
                    _tl(_("%s is barely keeping it together, eyes glazed and breathing shallow.")),
                ],
                9: [
                    _tl(_("%s looks like she is barely staying upright, blinking slowly.")),
                    _tl(_("%s is almost passing out, barely paying attention to the music.")),
                    _tl(_("%s is swaying in place, struggling to focus on anything.")),
                ],
                7: [
                    _tl(_("%s sways a little when she laughs, words starting to blur together.")),
                    _tl(_("%s laughs at things that are not that funny, eyes unfocused.")),
                    _tl(_("%s keeps losing her train of thought mid-sentence, giggling about it.")),
                ],
                5: [
                    _tl(_("%s is clearly tipsy, a bit louder and more touchy than usual.")),
                    _tl(_("%s looks comfortably drunk, leaning closer without even thinking about it.")),
                    _tl(_("%s has that warm, uninhibited energy that only comes after a few drinks.")),
                ],
                3: [
                    _tl(_("%s seems more relaxed than normal, cheeks a little flushed.")),
                    _tl(_("%s seems warmer and more open than usual.")),
                    _tl(_("%s has loosened up nicely, her smile coming easier now.")),
                ],
                0: [
                    _tl(_("%s looks perfectly fine, just enjoying the night.")),
                    _tl(_("%s looks perfectly sober, casually sipping her drink.")),
                    _tl(_("%s is calm and collected, taking it easy with the drinks.")),
                ],
            }
            for _hi, _hg in enumerate(_h_girls_here):
                _ha = _h_alc_list[_hi]
                _hn = _hg.Name
                if _ha >= 11:
                    _hint_pool = _alc_hint_pools[11]
                elif _ha >= 9:
                    _hint_pool = _alc_hint_pools[9]
                elif _ha >= 7:
                    _hint_pool = _alc_hint_pools[7]
                elif _ha >= 5:
                    _hint_pool = _alc_hint_pools[5]
                elif _ha >= 3:
                    _hint_pool = _alc_hint_pools[3]
                else:
                    _hint_pool = _alc_hint_pools[0]
                Narration(_hint_pool[_hi % len(_hint_pool)] % _hn)

        # NPC vibe hint (varies by NPC alcohol level)
        if _npc_is_active():
            python:
                _npc_gf = GIRL_BY_ID.get(store._h_npc.girl_gid) if hasattr(store._h_npc, "girl_gid") else _h_ga
                _npc_alc = getattr(store._h_npc, "_hangout_alcohol", 0)
                _nv = {"npc": store._h_npc.Name, "gf": _npc_gf.Name if _npc_gf else "???"}
                if _npc_alc >= 11:
                    _npc_vibe_pool = [
                        _("%(npc)s is swaying, barely keeping upright. %(gf)s has to hold them steady."),
                        _("%(npc)s mumbles something incoherent and leans heavily on %(gf)s."),
                        _("%(npc)s can barely keep their eyes open. The drinks hit hard."),
                    ]
                elif _npc_alc >= 9:
                    _npc_vibe_pool = [
                        _("%(npc)s is laughing at everything, arm draped loosely over %(gf)s."),
                        _("%(npc)s keeps losing track of the conversation, grinning at nothing."),
                        _("%(npc)s leans into %(gf)s, giggling. Doesn't seem to care about much right now."),
                    ]
                elif _npc_alc >= 7:
                    _npc_vibe_pool = [
                        _("%(npc)s is relaxed, chatting freely with everyone. Less guarded than usual."),
                        _("%(npc)s leans back with a lazy smile. The drinks have loosened them up."),
                        _("%(npc)s keeps touching %(gf)s's shoulder, more affectionate than usual."),
                    ]
                elif _npc_alc >= 5:
                    _npc_vibe_pool = [
                        _("%(npc)s is loosening up, though still keeping an eye on you."),
                        _("%(npc)s seems more at ease, occasionally glancing your way."),
                        _("%(npc)s sips the drink, looking more comfortable than when the night started."),
                    ]
                else:
                    _npc_vibe_pool = [
                        _("%(npc)s keeps an arm around %(gf)s, watching you a little too closely."),
                        _("%(npc)s sits close to %(gf)s, occasionally giving you a sharp look."),
                        _("%(npc)s hasn't taken their eyes off you since you sat down."),
                    ]
                _npc_vibe_msg = _tl(renpy.random.choice(_npc_vibe_pool)) % _nv
            $ Narration(_npc_vibe_msg)

        # Player hint
        if _p_alc >= 11:
            $ Narration(_("Your stomach is churning and the room will not sit still. One more drink and you might lose it."))
        elif _p_alc >= 9:
            $ Narration(_("Your head feels heavy. Everything is slightly delayed."))
        elif _p_alc >= 7:
            $ Narration(_("You feel warm and loose. Your words come out a little slower than you intended."))
        elif _p_alc >= 5:
            $ Narration(_("You are feeling the buzz nicely. Confident, relaxed, a little bold."))
        elif _p_alc >= 3:
            $ Narration(_("You are starting to feel the drinks. A pleasant warmth spreads through your chest."))
        else:
            $ Narration(_("You feel completely in control. The night is still young."))

        menu:
            "What do you want to do?"

            "Drink and chat" if _p_alc < 10:
                call hangout_drink_and_chat from _call_hangout_drink
                $ print("[HANGOUT] After drink_and_chat returned. _secret_party_ended=%s" % (getattr(store, "_secret_party_ended", False)))
                if getattr(store, "_secret_party_ended", False):
                    $ store._secret_party_ended = False
                    $ print("[HANGOUT] Party ended after drink -> jumping to .hangout_end")
                    jump .hangout_end
                jump .hangout_loop

            "Propose a round of Truth or Dare":
                call hangout_tod_round from _call_hangout_tod
                $ print("[HANGOUT] After ToD round returned. _secret_party_ended=%s _tod_ended_sick=%s" % (getattr(store, "_secret_party_ended", False), getattr(store, "_tod_ended_sick", None)))
                if getattr(store, "_secret_party_ended", False):
                    $ store._secret_party_ended = False
                    $ print("[HANGOUT] Party ended -> jumping to .hangout_end")
                    jump .hangout_end
                if getattr(store, "_tod_ended_sick", None) is not None:
                    $ print("[HANGOUT] Someone sick -> jumping to .hangout_end")
                    jump .hangout_end
                $ print("[HANGOUT] ToD round over, back to .hangout_loop")
                jump .hangout_loop

            "Propose a round of Never Have I Ever":
                call nhie_round from _call_hangout_nhie
                $ print("[HANGOUT] After NHIE round returned. _secret_party_ended=%s _tod_ended_sick=%s" % (getattr(store, "_secret_party_ended", False), getattr(store, "_tod_ended_sick", None)))
                if getattr(store, "_secret_party_ended", False):
                    $ store._secret_party_ended = False
                    $ print("[HANGOUT] Party ended after NHIE -> jumping to .hangout_end")
                    jump .hangout_end
                if getattr(store, "_tod_ended_sick", None) is not None:
                    $ print("[HANGOUT] Someone sick after NHIE -> jumping to .hangout_end")
                    jump .hangout_end
                $ print("[HANGOUT] NHIE round over, back to .hangout_loop")
                jump .hangout_loop

            "End the night":
                jump .hangout_end

        jump .hangout_loop

    label .hangout_end:
        $ renpy.hide_screen("tod_drunk_bars")

        # If everyone already left (NPC pass-out), skip goodbyes
        if getattr(store, "_npc_passed_out", False):
            $ store._secret_party_ended = False
            scene black
            with fade
            $ Narration(_("The door closes and your room falls quiet. Not exactly how you pictured the night ending."))
            $ Narration(_("You toss the empty cups in the trash and flop onto your bed, staring at the ceiling."))
            jump .hangout_cleanup

        python:
            _p_alc = hangout_get_player_alcohol()
            _end_girls = _hangout_girls_list()
            _end_alcs = [hangout_get_alcohol(g) for g in _end_girls]
            _alc_sum = _p_alc + sum(_end_alcs)
            _avg_drunk = _alc_sum / float(len(_end_girls) + 1) if _end_girls else _p_alc
            # Legacy vars
            _a_alc = _end_alcs[0] if len(_end_alcs) > 0 else 0
            _b_alc = _end_alcs[1] if len(_end_alcs) > 1 else 0

            _goodbye_pools = [
                [
                    _("I should probably head out. Thanks for tonight!"),
                    _("Okay, I think that is my cue to leave. This was great."),
                    _("I had such a good time. We need to do this again."),
                    _("Alright, I'm heading out before I fall asleep here."),
                ],
                [
                    _("Yeah, me too. This was really fun."),
                    _("Same here. Goodnight, everyone!"),
                    _("I'll text you guys tomorrow. Tonight was awesome."),
                    _("Night! Don't let me forget my phone..."),
                ],
                [
                    _("This was the best night in a while. Thanks!"),
                    _("I had a blast. Let's do this again soon."),
                    _("Goodnight! I'm going to sleep so well tonight."),
                ],
            ]

        # Check for special drunk GF event before goodbyes
        python:
            _gf_girl = None
            _other_girl = None
            _trigger_drunk_gf = False
            _both_dating = False

            _dating_girls = [g for g in _end_girls if hasattr(g, "is_dating_player") and g.is_dating_player()]
            _non_dating = [g for g in _end_girls if g not in _dating_girls]

            if len(_dating_girls) >= 2:
                _both_dating = True
                _dating_girls.sort(key=lambda g: hangout_get_alcohol(g), reverse=True)
                _gf_girl = _dating_girls[0]
                _other_girl = _non_dating[0] if _non_dating else _dating_girls[1]
            elif len(_dating_girls) == 1:
                _gf_girl = _dating_girls[0]
                _other_girl = _non_dating[0] if _non_dating else None

            if _gf_girl and _other_girl:
                _gf_alc = hangout_get_alcohol(_gf_girl)
                _other_alc = hangout_get_alcohol(_other_girl)
                _other_acts = getattr(_other_girl, "Sex_acts", {})
                _other_did_stuff = any(_other_acts.get(a, 0) > 0 for a in ("hj", "bj", "tj", "sex", "anal"))
                _other_is_cheater = hasattr(_other_girl, "has_trait") and _other_girl.has_trait("cheater")

                if _gf_alc >= 8 and _other_did_stuff:
                    _trigger_chance = 0.60 if _other_is_cheater else 0.35
                    if _other_alc >= 4:
                        _trigger_chance += 0.20
                    if _both_dating:
                        _trigger_chance -= 0.10
                    _trigger_drunk_gf = renpy.random.random() < _trigger_chance

        if _trigger_drunk_gf:
            call hangout_drunk_gf_event(_gf_girl, _other_girl, _both_dating) from _call_hangout_drunk_gf
        else:
            python:
                _bye_exprs = ["happy", "smile", "normal"]
                for _gi, _gg in enumerate(_end_girls):
                    set_scene_expression(_gg, _bye_exprs[min(_gi, len(_bye_exprs) - 1)])
                    _gpool = _goodbye_pools[min(_gi, len(_goodbye_pools) - 1)]
                    Say_Line(_gg, _tl(renpy.random.choice(_gpool)))
            if len(_end_girls) > 1:
                $ Say_Player(_("Thanks for coming, girls. We should do this again."))
            elif len(_end_girls) == 1:
                $ Say_Player(_tl(_("Thanks for coming over, %s. We should do this again.")) % _end_girls[0].Name)

        # Girls leave
        scene black
        with fade

        $ Narration(_("After a while longer, the party in your room finally loses some of its edge, and the night comes to a natural end."))

        if _avg_drunk >= 8:
            $ Narration(_("Once the door finally closes, you just stand there for a second, letting the silence replace the music."))
            $ Narration(_("Your head spins a little when you move too fast, and you realize you are probably just as drunk as they were."))
            $ Narration(_("You flop down onto your bed, staring at the ceiling and wondering how much of tonight you are actually going to remember tomorrow."))
        elif _avg_drunk >= 4:
            $ Narration(_("When the room finally goes quiet, you feel the buzz still warm in your chest and cheeks."))
            $ Narration(_("You tidy up just enough that it won't look like a disaster in the morning, then let yourself collapse onto the bed with a satisfied sigh."))
        else:
            $ Narration(_("Once your room is empty again, the silence feels almost strange after all the music and laughter."))
            $ Narration(_("You take a moment to straighten things up and replay bits of the night in your head before finally calling it for the evening."))

    label .hangout_cleanup:
        # Cleanup
        python:
            # Small Love boost for spending time together
            _cleanup_girls = _hangout_girls_list()
            for _cg in _cleanup_girls:
                Change_Status(_cg, "Love", 15, show_popup=False)   # through Change_Status: her personality counts (it used to add straight to the stat)
                for _cog in _cleanup_girls:
                    if _cog.gid != _cg.gid:
                        _cg.add_like_for(_cog.gid, 10)

            # Track blackouts (alcohol >= 12) for NHIE "been so drunk I forgot"
            _peak_p = getattr(store, "_hangout_player_alcohol", 0)
            if _peak_p >= 12:
                store.Player._blackout_count = getattr(store.Player, "_blackout_count", 0) + 1
                print("[HANGOUT] Player blacked out (alc=%.1f), count=%d" % (_peak_p, store.Player._blackout_count))
            for _bg in _cleanup_girls:
                _bg_alc = hangout_get_alcohol(_bg)
                if _bg_alc >= 12:
                    _bg._blackout_count = getattr(_bg, "_blackout_count", 0) + 1
                    print("[HANGOUT] %s blacked out (alc=%.1f), count=%d" % (_bg.gid, _bg_alc, _bg._blackout_count))

            hangout_reset_alcohol()

            # Reset ToD round tracking
            store._hangout_tod_played = False
            store._tod_used_keys = set()
            store._tod_max_difficulty = 0

            store._hangout_running = False
            store._hangout_scheduled_day = -1
            store._hangout_group_id = None
            store._hangout_members = []
            store._hangout_girls = []
            store._hangout_girl_a = None
            store._hangout_girl_b = None
            store._hangout_girl_c = None

            # Girl + partner hangout: hide the NPC sprite and clear the pointer
            _h_npc_cleanup = getattr(store, "_hangout_partner_npc", None)
            if _h_npc_cleanup is not None:
                _h_npc_cleanup.hide_sprite()
            store._hangout_partner_npc = None
            store._hangout_partner_npc_id = None
            store._npc_passed_out = False

            # Girls go back to their rooms and reset outfit
            for _cg in _cleanup_girls:
                _cg.loc = girl_home_loc(_cg)
                _cg.WearPreset("casual", apply_now=False)

            # Clear party
            store.Party = []

        # Advance to next day (sleep)
        stop music fadeout 1.0
        scene black
        with fade
        pause 0.5
        $ Narration(_("You crash into bed and drift off to sleep."))

        python:
            advance_time(1)  # Night -> next Morning
            NightAutoSleepPending = False

        $ store._in_event = False
        $ store._in_sandbox = True
        $ debug_log("[STATE] _in_event = False, _in_sandbox = True (hangout_night_event end)")

        return

# ============================================================
# SUB-EVENT: Drunk GF passes out, other girl seduces player
# ============================================================
label hangout_drunk_gf_event(gf, other, both_dating=False):
    $ _gf_name = gf.Name
    $ _ot_name = other.Name
    python:
        _ot_is_cheater = hasattr(other, "has_trait") and other.has_trait("cheater")
        _ot_is_hardcore = hasattr(other, "has_trait") and other.has_trait("hardcore_sex")
        _ot_is_cute = hasattr(other, "has_trait") and other.has_trait("cute_sex")
        _ot_is_loyal = hasattr(other, "has_trait") and other.has_trait("loyal")
        _ot_alc = hangout_get_alcohol(other)
        _ot_has_bf = hasattr(other, "has_npc_partner") and other.has_npc_partner()
        # "both_dating" means both are dating the player
        # "_ot_has_bf" means the other girl has an NPC boyfriend (not the player)
        _ot_committed = both_dating or _ot_has_bf

    # GF starts falling asleep
    $ set_scene_expression(gf, "confused")
    $ Say_Line(gf, renpy.random.choice([
        _("I'm so... tired... the room is spinning..."),
        _("I think I drank too much... I can't keep my eyes open..."),
        _("Everything is so... fuzzy... I just need to close my eyes for a second..."),
    ]))

    $ gf.discover("discovered_trait_lightweight") if gf.has_trait("lightweight") else None
    $ Narration(_("[_gf_name] leans back and her eyes start to close. Within seconds, she's out cold."))

    $ Say_Player(renpy.random.choice([
        _("Hey, [_gf_name]? ...She's asleep."),
        _("[_gf_name]? Yeah, she's gone."),
        _("I think she passed out."),
    ]))

    # Other girl notices the opportunity
    pause 0.5

    # --- Initial reaction: depends on relationship status ---
    if both_dating:
        # Other girl is ALSO dating the player
        if _ot_is_cheater:
            $ set_scene_expression(other, "smirk")
            $ Say_Line(other, renpy.random.choice([
                _("She's out... You know, just because we're all together doesn't mean we can't have some private time~"),
                _("Your other girlfriend is sleeping. That leaves just us... her boyfriend and me."),
                _("I know we both date you, but she doesn't need to know about THIS part."),
            ]))
        elif _ot_alc >= 6:
            $ set_scene_expression(other, "shy")
            $ Say_Line(other, renpy.random.choice([
                _("She's really out, huh... I know we both share you, but right now... I want you all to myself."),
                _("I'm drunk enough to admit it... I get jealous when you're with her. Tonight, you're mine."),
                _("We're all in this together, but... she's asleep. And I've been wanting alone time with you all night."),
            ]))
        elif _ot_is_cute:
            $ set_scene_expression(other, "shy")
            $ Say_Line(other, renpy.random.choice([
                _("I know this is weird since we all... but when she's sleeping, it feels like it's just us. Like it used to be."),
                _("Is it wrong that I want you to myself right now? Even just for tonight?"),
                _("She wouldn't mind, right? We both date you... but something about doing it while she sleeps feels... exciting."),
            ]))
        else:
            $ set_scene_expression(other, "serious")
            $ Say_Line(other, renpy.random.choice([
                _("She's asleep. I know we're all together but... I've been wanting some time alone with you."),
                _("We share you, sure. But right now she doesn't have to watch. Just us."),
                _("I know the arrangement, but... tonight I want to be your only girl. Even if just for a little while."),
            ]))
    elif _ot_has_bf:
        # Other girl has an NPC boyfriend (double cheating)
        if _ot_is_cheater:
            $ set_scene_expression(other, "smirk")
            $ Say_Line(other, renpy.random.choice([
                _tl(_("Your girlfriend is out cold. My %s isn't here. Nobody's watching...")) % other.partner_label(),
                _tl(_("She's asleep, my %s is at home... it's like the universe is telling us something~")) % other.partner_label(),
                _("Two people who shouldn't be doing this, and zero people awake to stop us."),
            ]))
        elif _ot_alc >= 6:
            $ set_scene_expression(other, "worried")
            $ Say_Line(other, renpy.random.choice([
                _tl(_("I have a %s... you have a girlfriend... and she just fell asleep in your room. This is so wrong.")) % other.partner_label(),
                _format_partner_line(other, _("I keep thinking about my %(pl)s and how %(pp)s'd react. But then I look at you and the drinks make me not care.")),
                _tl(_("We're both terrible people if we do this. My %s, your girlfriend... but god, I want to.")) % other.partner_label(),
            ]))
        elif _ot_is_loyal:
            $ set_scene_expression(other, "worried")
            $ Say_Line(other, renpy.random.choice([
                _("I shouldn't even be thinking this. I have a [other.partner_label()]. You have a girlfriend. She's RIGHT THERE."),
                _("This is wrong on so many levels. My [other.partner_label()] trusts me. [_gf_name] trusts you. But..."),
                _("Every part of me says this is a mistake. I'm taken. You're taken. But I can't stop looking at you."),
            ]))
        else:
            $ set_scene_expression(other, "uncomfortable")
            $ Say_Line(other, renpy.random.choice([
                _tl(_("My %s has no idea I'm even here this late. And your girlfriend just passed out. This is dangerous.")) % other.partner_label(),
                _format_partner_line(other, _("I keep telling myself I have a %(pl)s. But right now, with the drinks and %(po)s sleeping...")),
                _("We both have someone else. And she's literally sleeping right there. This couldn't be more wrong."),
            ]))
    elif _ot_is_cheater:
        $ set_scene_expression(other, "smirk")
        $ Say_Line(other, renpy.random.choice([
            _("[_gf_name] is out cold. And we're alone now..."),
            _("Well well well... looks like your girlfriend can't handle her drinks~"),
            _("She's not waking up anytime soon. You know what that means, right?"),
        ]))
    elif _ot_alc >= 6:
        $ set_scene_expression(other, "shy")
        $ Say_Line(other, renpy.random.choice([
            _("She's really asleep, huh... It's just us now."),
            _("I probably shouldn't be thinking what I'm thinking right now..."),
            _("The drinks are making me brave... and she's not watching..."),
        ]))
    else:
        $ set_scene_expression(other, "uncomfortable")
        $ Say_Line(other, renpy.random.choice([
            _("She's asleep... we should probably call it a night too."),
            _("I guess the party is over... unless..."),
            _("So... it's just us two now. What do you want to do?"),
        ]))

    # Other girl moves closer
    python:
        set_girl_sprite(other.gid, pose="standing", at_list=[Transform(xalign=0.75, yalign=2.0)])

    # --- Second line: the proposition ---
    if both_dating:
        if _ot_is_cheater or _ot_alc >= 7:
            $ set_scene_expression(other, "lusty")
            $ Say_Line(other, renpy.random.choice([
                _("She won't know. It'll be our secret. Just you and me tonight."),
                _("I want all of you. Not sharing. Not tonight. Come here."),
                _("Don't think about her. Just think about me. Right now."),
            ]))
        elif _ot_is_cute:
            $ set_scene_expression(other, "shy")
            $ Say_Line(other, renpy.random.choice([
                _("I know we're all in this together... but can tonight be just ours? Please?"),
                _("I want a memory that's just mine... not hers, not shared. Just us."),
                _("My heart says this is okay because we're together... but the fact that she's asleep makes it feel so... forbidden."),
            ]))
        else:
            $ set_scene_expression(other, "smirk")
            $ Say_Line(other, renpy.random.choice([
                _("We don't get enough alone time. She's asleep. Let's take advantage of it."),
                _("I just want to feel like I'm the only one. Just for tonight."),
                _("She'll never know. And honestly... I need this."),
            ]))
    elif _ot_has_bf:
        if _ot_is_cheater:
            $ set_scene_expression(other, "sly")
            $ Say_Line(other, renpy.random.choice([
                _tl(_("My %s is boring anyway. And your girlfriend is unconscious. It's perfect.")) % other.partner_label(),
                _("I cheat. You cheat. We're made for each other tonight."),
                _("Two cheaters, one sleeping girlfriend, zero consequences. Come here."),
            ]))
        elif _ot_is_loyal:
            $ set_scene_expression(other, "nervous")
            $ Say_Line(other, renpy.random.choice([
                _("I can't believe I'm saying this... I've never cheated before. But tonight I want to break every rule."),
                _("My [other.partner_label()] would never forgive me. [_gf_name] would never forgive you. ...I don't care right now."),
                _("I'm shaking. I've never done anything like this. But I can't leave without... please."),
            ]))
        else:
            $ set_scene_expression(other, "uncomfortable")
            $ Say_Line(other, renpy.random.choice([
                _tl(_("My %s doesn't have to know. She doesn't have to know. Just us.")) % other.partner_label(),
                _("I know I'm taken. But you make me forget that."),
                _tl(_("This stays between us. My %s, your girlfriend... they'll never find out.")) % other.partner_label(),
            ]))
    elif _ot_is_cheater:
        $ set_scene_expression(other, "smug")
        $ Say_Line(other, renpy.random.choice([
            _("Come on... she won't know. It'll be our little secret."),
            _("Don't you want to have some real fun tonight? She's sleeping right there..."),
            _("I've been wanting to do this all night. Now there's nothing stopping us."),
        ]))
    elif _ot_is_hardcore:
        $ set_scene_expression(other, "lusty")
        $ Say_Line(other, renpy.random.choice([
            _("I know this is wrong. But I don't care right now."),
            _("Look, we both want this. She's asleep. Nobody has to know."),
            _("I'm too worked up from tonight to just go home. Are you?"),
        ]))
    elif _ot_is_cute:
        $ set_scene_expression(other, "embarrassed")
        $ Say_Line(other, renpy.random.choice([
            _("I know we shouldn't... but I can't stop thinking about you tonight."),
            _("This is so wrong... but my heart is pounding so fast right now..."),
            _("I've been holding back all night. And now she's asleep and I..."),
        ]))
    else:
        $ set_scene_expression(other, "nervous")
        $ Say_Line(other, renpy.random.choice([
            _("I know this is messed up. But tonight has been... a lot. And I want you."),
            _("We probably shouldn't. But... do you want to?"),
            _("The alcohol is talking, but... I've been thinking about this all night."),
        ]))

    menu:
        "What do you do?"

        "Go for it":
            $ set_scene_expression(other, "embarrassed")
            $ Say_Line(other, renpy.random.choice([
                _("Just be quiet... she's right there..."),
                _("If she wakes up, we're both dead."),
                _("Mmm... don't hold back. But keep it quiet."),
                _("I can't believe we're doing this..."),
            ]))

            # Block interruptions (GF is sleeping here, no one else should walk in)
            $ store._interruption_happened = True
            $ store._witness_check_done = True

            # Go straight to position select (she already agreed)
            $ print("[DRUNK_GF_EVENT] Entering sex_position_select: other=%s restricted=%s energy=%d exhausted=%s" % (other.gid, getattr(store, "_scene_restricted", False), Player.energy, store._player_exhausted))
            call sex_position_select(other) from _call_sex_pos_drunk_gf
            $ print("[DRUNK_GF_EVENT] sex_position_select returned: restricted=%s energy=%d exhausted=%s" % (getattr(store, "_scene_restricted", False), Player.energy, store._player_exhausted))

            # Bonus stats for the risky situation
            python:
                Change_Status(other, "Love", 15)
                Change_Status(other, "Inbt", 20)
                Change_Status(other, "Obed", 10)

            # Girl puts clothes back on before GF wakes up
            $ Narration(_("[_ot_name] quickly gets dressed before [_gf_name] wakes up."))
            python:
                other.WearPreset("casual", apply_now=False)
                set_girl_sprite(other.gid, pose="standing", at_list=[Transform(xalign=0.90, yalign=2.0)])

        "No, we can't do this. She's right there.":
            if both_dating:
                $ Say_Player(_("No. She's my girlfriend too. I'm not doing this behind her back."))
            else:
                $ Say_Player(_("No. She's my girlfriend. I can't do this to her."))

            if both_dating:
                $ set_scene_expression(other, "sad")
                $ Say_Line(other, renpy.random.choice([
                    _("You're right... we're all in this together. It wouldn't be fair."),
                    _("I know... I just got jealous for a moment. I'm sorry."),
                    _("Yeah... she'd be hurt if she found out. Even if we both date you."),
                ]))
            elif _ot_has_bf:
                if _ot_is_cheater:
                    $ set_scene_expression(other, "angry")
                    $ Say_Line(other, renpy.random.choice([
                        _tl(_("Your loss. My %s wouldn't have stopped me.")) % other.partner_label(),
                        _tl(_("Fine. Back to my boring %s then.")) % other.partner_label(),
                    ]))
                elif _ot_is_loyal:
                    $ set_scene_expression(other, "embarrassed")
                    $ Say_Line(other, renpy.random.choice([
                        _("Thank god you said no. I would have regretted it. My [other.partner_label()]... [_gf_name]... what was I thinking?"),
                        _("You're right. I have a [other.partner_label()]. You have a girlfriend. This was the alcohol talking."),
                    ]))
                else:
                    $ set_scene_expression(other, "uncomfortable")
                    $ Say_Line(other, renpy.random.choice([
                        _("Yeah... you're right. I have someone too. This would have been a disaster."),
                        _("My [other.partner_label()] doesn't deserve that. Neither does [_gf_name]. Good call."),
                    ]))
            elif _ot_is_cheater:
                $ set_scene_expression(other, "angry")
                $ Say_Line(other, renpy.random.choice([
                    _("Tch. Your loss. She wouldn't have known."),
                    _("Really? After everything tonight? Fine."),
                    _("Boring. But I respect it... barely."),
                ]))
            else:
                $ set_scene_expression(other, "embarrassed")
                $ Say_Line(other, renpy.random.choice([
                    _("You're right. I'm sorry. I don't know what got into me."),
                    _("Yeah... that was the alcohol talking. Forget I said anything."),
                    _("I knew you'd say that. You're a good guy. Annoyingly good."),
                ]))
            python:
                Change_Status(gf, "Love", 10)  # karma for being loyal
            return

    # After sex - both catch their breath
    $ Narration(_("When it's over, you both lie there in silence, breathing heavily, hyper-aware of [_gf_name] still sleeping nearby."))

    if both_dating:
        $ set_scene_expression(other, "shy")
        $ Say_Line(other, renpy.random.choice([
            _("That was... just ours. Not shared. Not a group thing. Just you and me."),
            _("She's going to wake up and have no idea... I feel guilty but also... alive."),
            _("We share everything with her. But this... this was mine."),
            _("I needed that. Just the two of us. Even if she'd be upset."),
        ]))
    elif _ot_has_bf:
        $ set_scene_expression(other, "embarrassed")
        $ Say_Line(other, renpy.random.choice([
            _tl(_("I just cheated on my %s... with you... while your girlfriend sleeps right there. What is wrong with me?")) % other.partner_label(),
            _tl(_("My %s is probably texting me right now. And I just... god. That was incredible though.")) % other.partner_label(),
            _("Two relationships, both betrayed in one night. We're horrible people. ...It was worth it."),
            _("I can still feel my heart racing. From the sex and the guilt. Mostly the sex."),
        ]))
    else:
        $ set_scene_expression(other, "shy")
        $ Say_Line(other, renpy.random.choice([
            _("That was... god. I can't believe we just did that."),
            _("She didn't wake up. I think my heart stopped twice."),
            _("Worth it. Completely worth it. Even if she kills us later."),
            _("I've never been so scared and so turned on at the same time."),
        ]))

    $ Say_Player(renpy.random.choice([
        _("That was insane."),
        _("If she had woken up..."),
        _("I can still hear my heartbeat."),
    ]))

    # Brief pause
    pause 1.0

    # GF starts stirring
    $ Narration(_("[_gf_name] shifts in her sleep and mumbles something."))

    $ set_scene_expression(other, "scared")
    $ Say_Line(other, renpy.random.choice([
        _("Oh god, she's moving!"),
        _("Quick, act normal!"),
        _("Shh! She's waking up!"),
    ]))

    # Other girl fixes herself up quickly
    python:
        other.WearPreset("casual", apply_now=False)
        set_girl_sprite(other.gid, pose="standing", at_list=[Transform(xalign=0.90, yalign=2.0)])

    pause 0.5

    # GF wakes up groggy
    $ set_scene_expression(gf, "confused")
    $ Say_Line(gf, renpy.random.choice([
        _("Mmm... what time is it...? Did I fall asleep?"),
        _("Huh...? How long was I out...?"),
        _("Ugh... my head... did I miss anything?"),
    ]))

    $ Say_Player(renpy.random.choice([
        _("Just a few minutes. We were about to wake you up."),
        _("Not long. We were just chatting."),
        _("You dozed off. We were about to call it a night."),
    ]))

    $ set_scene_expression(other, "normal")
    $ Say_Line(other, renpy.random.choice([
        _("Yeah, you just fell asleep for a bit. Nothing happened."),
        _("You were snoring. It was adorable. And that's it."),
        _("We were just sitting here waiting for you to wake up."),
    ]))

    $ set_scene_expression(gf, "embarrassed")
    $ Say_Line(gf, renpy.random.choice([
        _("Oh... okay. Sorry about that. I guess I drank too much."),
        _("Ugh, I'm so embarrassed. I never pass out like that."),
        _("My head is killing me... I should probably go home."),
    ]))

    $ set_scene_expression(other, "smile")
    $ Say_Line(other, renpy.random.choice([
        _("Yeah, me too. It's getting late. Goodnight, you two."),
        _("I should head out. Tonight was... really fun."),
        _("Alright, I'm going. Get some rest, both of you."),
    ]))

    $ set_scene_expression(gf, "smile")
    $ Say_Line(gf, renpy.random.choice([
        _("Goodnight... thanks for tonight."),
        _("Night... sorry for passing out..."),
        _("I'll text you guys tomorrow... if I survive this headache."),
    ]))

    # Suspicion check - GF might sense something is off
    python:
        # Small suspicion increase if she's perceptive
        if hasattr(gf, "suspicion"):
            gf.suspicion = min(100, gf.suspicion + 5)

    return

# ============================================================
# SUB-EVENT: Drink and chat
# ============================================================
label hangout_drink_and_chat:
    python:
        _dc_girls = _hangout_girls_list()
        _dc_count = len(_dc_girls)

        tod_drink_player(1)
        for _dcg in _dc_girls:
            tod_drink(_dcg, 1)
        _dc_npc_sick = False
        if _npc_is_active():
            tod_drink(store._h_npc, 1)
            if tod_rolls_sick(store._h_npc):
                _dc_npc_sick = True

        _p_alc = hangout_get_player_alcohol()
        _dc_alcs = [hangout_get_alcohol(g) for g in _dc_girls]
        _avg_alc = (_p_alc + sum(_dc_alcs)) / float(_dc_count + 1)

        # Assign speaker slots dynamically
        _ga = _dc_girls[0] if _dc_count > 0 else None
        _gb = _dc_girls[1] if _dc_count > 1 else None
        _gc = _dc_girls[2] if _dc_count > 2 else None

    if _dc_npc_sick:
        if _dc_count == 1:
            call _npc_pass_out_1girl_event from _call_npc_po_1g_dc
            if getattr(store, "_secret_party_ended", False):
                return
        else:
            call _npc_pass_out_event from _call_npc_po_dc

    $ Narration(_("You pour another round for everyone."))

    python:
        if _avg_alc <= 3:
            _chat_pool = [
                ((_ga, _("So... what's the most embarrassing thing that happened to you this week?")),
                 (_gb, _("Oh god, don't even get me started.")),
                 ("player", _("Come on, spill!"))),

                ((_gb, _("This is actually really nice. We should hang out more.")),
                 (_ga, _("Agreed. Beats studying alone in my room.")),
                 ("player", _("My door's always open."))),

                ((_ga, _("What kind of music do you guys listen to?")),
                 ("player", _("A bit of everything, honestly.")),
                 (_gb, _("Same here. Depends on the mood."))),

                ((_gb, _("Have you guys seen that new show everyone's talking about?")),
                 (_ga, _("Not yet! Is it good?")),
                 (_gb, _("So good. We should watch it together sometime."))),
            ]
            if _gc:
                _chat_pool.extend([
                    ((_gc, _("I brought snacks, by the way. Anyone want some?")),
                     (_ga, _("Yes please! What did you bring?")),
                     (_gc, _("A little of everything. Help yourselves.")),
                     ("player", _("You're the best."))),

                    ((_ga, _("So, what are you guys doing this weekend?")),
                     (_gb, _("Nothing planned yet. Why?")),
                     (_gc, _("Count me in for whatever it is.")),
                     ("player", _("I like where this is going."))),
                ])
        elif _avg_alc <= 6:
            _chat_pool = [
                ((_ga, _("Okay okay, real talk... what's your type?")),
                 (_gb, _("Hmmm... someone who can make me laugh, I guess.")),
                 ("player", _("What about looks?")),
                 (_gb, _("...That helps too."))),

                ((_gb, _("I'm starting to feel this. Are you guys feeling it?")),
                 (_ga, _("Oh yeah. Things are getting warm.")),
                 ("player", _("The night is just getting started."))),

                ((_ga, _("You know what? I'm glad we did this.")),
                 (_gb, _("Me too. It's nice to just... relax.")),
                 ("player", _("No pressure. Just vibes."))),

                (("player", _("Okay, honest question. Who here has the worst drunk stories?")),
                 (_ga, _("Definitely me. I once...")),
                 (_gb, _("Oh this I HAVE to hear!"))),
            ]
            if _gc:
                _chat_pool.extend([
                    ((_gc, _("I think we should all share a secret. Nothing leaves this room.")),
                     (_ga, _("That's dangerous territory...")),
                     (_gb, _("I'm in. But you go first.")),
                     (_gc, _("Fine... okay, so..."))),

                    ((_gb, _("Which one of us do you think is the wildest?")),
                     (_gc, _("Definitely not me. I'm very well-behaved.")),
                     (_ga, _("Sure you are.")),
                     ("player", _("I'm not answering that."))),
                ])
        else:
            _chat_pool = [
                ((_ga, _("Okay I'm definitely tipsy. Everything is funny right now.")),
                 (_gb, _("Same! Look at my face, I can't stop smiling!")),
                 ("player", _("You both look like you're having the time of your lives."))),

                ((_gb, _("I feel like I could say anything right now and not care.")),
                 (_ga, _("That's the drinks talking~")),
                 ("player", _("Nothing leaves this room."))),

                ((_ga, _("Okay, who here has a crush on someone in this room?")),
                 (_gb, _("...")),
                 (_ga, _("That silence says everything!")),
                 ("player", _("I plead the fifth."))),

                ((_gb, _("This is hands down the best night I've had in weeks.")),
                 (_ga, _("Same. Can we do this every week?")),
                 ("player", _("I'll buy more bottles."))),
            ]
            if _gc:
                _chat_pool.extend([
                    ((_gc, _("I love you guys. Like, genuinely. This is amazing.")),
                     (_ga, _("Aww! Group hug?")),
                     (_gb, _("Get over here!")),
                     ("player", _("Best night ever."))),

                    ((_ga, _("We should make this a weekly thing. Mandatory fun night.")),
                     (_gc, _("I second that motion!")),
                     (_gb, _("All in favor?")),
                     ("player", _("Motion passed. Unanimously."))),
                ])

        _chosen_chat = renpy.random.choice(_chat_pool)

    $ _ci = 0
    while _ci < len(_chosen_chat):
        python:
            _speaker, _line = _chosen_chat[_ci]
            if _speaker == "player":
                Say_Player(_line)
            elif _speaker is not None:
                Say_Line(_speaker, _line)
            _ci += 1

    # Ambient closing narration
    python:
        _dc_names = [g.Name for g in _dc_girls]
        _closer_general = [
            _tl(_("You keep the music low and let the conversation drift naturally, one story leading into another.")),
            _tl(_("You pour another round and keep chatting, the conversation jumping from random topics to personal ones.")),
            _tl(_("Time slips by as you talk about nothing in particular, the room feeling more relaxed with every minute.")),
        ]
        _closer_girl = [
            _tl(_("%s settles comfortably nearby, occasionally teasing you about something you said earlier.")),
            _tl(_("%s laughs easily, clearly relaxing as the drinks start to kick in.")),
            _tl(_("%s leans back against your bed, smiling whenever your eyes meet.")),
            _tl(_("%s seems more animated, gesturing a little too much as she talks.")),
            _tl(_("%s smiles more often now, her attention drifting between you and the music.")),
            _tl(_("%s stretches out comfortably, clearly at ease in your space.")),
        ]
        Narration(renpy.random.choice(_closer_general))
        renpy.random.shuffle(_closer_girl)
        for _cli, _clg in enumerate(_dc_girls):
            Narration(_closer_girl[_cli % len(_closer_girl)] % _clg.Name)

    return

# ============================================================
# DEBUG: Test hangout scenarios directly
# Call from console: call debug_hangout_drunk_gf
# ============================================================

label debug_hangout_drunk_gf:
    $ _dg_gwen = GIRL_BY_ID.get("gwen")
    $ _dg_rogue = GIRL_BY_ID.get("rogue")

    menu:
        "Pick scenario to test:"

        "GF=Gwen passes out, Rogue seduces (single)":
            python:
                _dg_gwen.Player_status = "dating"
                _dg_rogue.Player_status = "none"
                _dg_rogue.clear_npc_partner()
                # Give Rogue some history with player
                _dg_rogue.Sex_acts["bj"] = max(_dg_rogue.Sex_acts.get("bj", 0), 1)
                _dg_rogue.Sex_acts["reverse_cowgirl"] = max(_dg_rogue.Sex_acts.get("reverse_cowgirl", 0), 1)
                girl_history_normalize(_dg_rogue)   # a position never exists without "sex"
            call debug_hangout_setup(_dg_gwen, _dg_rogue, 9, 5) from _call_dbg_setup_1
            call hangout_drunk_gf_event(_dg_gwen, _dg_rogue, False) from _call_dbg_drunk_1

        "GF=Gwen passes out, Rogue seduces (Rogue has BF)":
            python:
                _dg_gwen.Player_status = "dating"
                _dg_rogue.Player_status = "none"
                _dg_rogue.npc_partner_id = "npc_bf_rogue"
                _dg_rogue.flags["has_npc_partner"] = True
                _dg_rogue.Sex_acts["bj"] = max(_dg_rogue.Sex_acts.get("bj", 0), 1)
                _dg_rogue.Sex_acts["cowgirl"] = max(_dg_rogue.Sex_acts.get("cowgirl", 0), 1)
                girl_history_normalize(_dg_rogue)
            call debug_hangout_setup(_dg_gwen, _dg_rogue, 9, 6) from _call_dbg_setup_2
            call hangout_drunk_gf_event(_dg_gwen, _dg_rogue, False) from _call_dbg_drunk_2

        "Both dating player, Gwen passes out, Rogue seduces":
            python:
                _dg_gwen.Player_status = "dating"
                _dg_rogue.Player_status = "dating"
                _dg_rogue.clear_npc_partner()
                _dg_rogue.Sex_acts["reverse_cowgirl"] = max(_dg_rogue.Sex_acts.get("reverse_cowgirl", 0), 1)
                _dg_rogue.Sex_acts["tj"] = max(_dg_rogue.Sex_acts.get("tj", 0), 1)
                girl_history_normalize(_dg_rogue)
            call debug_hangout_setup(_dg_gwen, _dg_rogue, 9, 5) from _call_dbg_setup_3
            call hangout_drunk_gf_event(_dg_gwen, _dg_rogue, True) from _call_dbg_drunk_3

        "Both dating, Rogue passes out, Gwen seduces":
            python:
                _dg_gwen.Player_status = "dating"
                _dg_rogue.Player_status = "dating"
                _dg_gwen.clear_npc_partner()
                _dg_gwen.Sex_acts["cowgirl"] = max(_dg_gwen.Sex_acts.get("cowgirl", 0), 1)
                _dg_gwen.Sex_acts["bj"] = max(_dg_gwen.Sex_acts.get("bj", 0), 1)
                girl_history_normalize(_dg_gwen)
            call debug_hangout_setup(_dg_rogue, _dg_gwen, 9, 6) from _call_dbg_setup_4
            call hangout_drunk_gf_event(_dg_rogue, _dg_gwen, True) from _call_dbg_drunk_4

        "Rogue cheater + has BF, Gwen GF passes out":
            python:
                _dg_gwen.Player_status = "dating"
                _dg_rogue.Player_status = "none"
                _dg_rogue.npc_partner_id = "npc_bf_rogue"
                _dg_rogue.flags["has_npc_partner"] = True
                _dg_rogue.add_trait("cheater")
                _dg_rogue.Sex_acts["reverse_cowgirl"] = max(_dg_rogue.Sex_acts.get("reverse_cowgirl", 0), 3)
                girl_history_normalize(_dg_rogue)
            call debug_hangout_setup(_dg_gwen, _dg_rogue, 9, 7) from _call_dbg_setup_5
            call hangout_drunk_gf_event(_dg_gwen, _dg_rogue, False) from _call_dbg_drunk_5

        "Rogue loyal + has BF, Gwen GF passes out":
            python:
                _dg_gwen.Player_status = "dating"
                _dg_rogue.Player_status = "none"
                _dg_rogue.npc_partner_id = "npc_bf_rogue"
                _dg_rogue.flags["has_npc_partner"] = True
                _dg_rogue.add_trait("loyal")
                _dg_rogue.Sex_acts["hj"] = max(_dg_rogue.Sex_acts.get("hj", 0), 1)
            call debug_hangout_setup(_dg_gwen, _dg_rogue, 9, 4) from _call_dbg_setup_6
            call hangout_drunk_gf_event(_dg_gwen, _dg_rogue, False) from _call_dbg_drunk_6

        "Full hangout (normal flow)":
            python:
                store._hangout_scheduled_day = store.Day
                store._hangout_girls = [_dg_gwen, _dg_rogue]
                _sync_hangout_girl_aliases()
                store._hangout_player_alcohol = 0
                _dg_gwen._hangout_alcohol = 0
                _dg_rogue._hangout_alcohol = 0
                _dg_gwen.WearPreset("casual", apply_now=False)
                _dg_rogue.WearPreset("casual", apply_now=False)
                setattr(store, "_hangout_strip_level_gwen", 0)
                setattr(store, "_hangout_strip_level_rogue", 0)
                _dg_gwen.loc = "room"
                _dg_rogue.loc = "room"
                navigate_to("room", None)
            call Set_Scene(entry=False, show_chars=False, quiet=True) from _call_dbg_set_scene
            $ set_girl_sprite("gwen", pose="standing", at_list=[Transform(xalign=0.60, yalign=2.0)])
            $ set_girl_sprite("rogue", pose="standing", at_list=[Transform(xalign=0.90, yalign=2.0)])
            call hangout_night_event from _call_dbg_hangout_full

        "Cancel":
            return

    $ Narration(_("Debug scenario complete."))
    return

label debug_hangout_setup(gf_girl, other_girl, gf_alc, other_alc):
    python:
        # Setup hangout state
        store._hangout_girls = [gf_girl, other_girl]
        _sync_hangout_girl_aliases()
        store._hangout_player_alcohol = 5
        gf_girl._hangout_alcohol = gf_alc
        other_girl._hangout_alcohol = other_alc

        # Ensure casual outfit and strip level reset
        gf_girl.WearPreset("casual", apply_now=False)
        other_girl.WearPreset("casual", apply_now=False)
        setattr(store, "_hangout_strip_level_" + gf_girl.gid, 0)
        setattr(store, "_hangout_strip_level_" + other_girl.gid, 0)

        # Move to room
        gf_girl.loc = "room"
        other_girl.loc = "room"
        navigate_to("room", None)

    call Set_Scene(entry=False, show_chars=False, quiet=True) from _call_dbg_set_scene_setup
    $ set_girl_sprite(gf_girl.gid, pose="standing", at_list=[Transform(xalign=0.60, yalign=2.0)])
    $ set_girl_sprite(other_girl.gid, pose="standing", at_list=[Transform(xalign=0.90, yalign=2.0)])
    return


# ============================================================
# NPC PASS OUT EVENT (2+ girls present)
# ============================================================
label _npc_pass_out_event:
    python:
        _po_npc = store._h_npc
        _po_name = _po_npc.Name
        _po_gf = _bf_get_gf(_po_npc)
        _po_girls = _hangout_girls_list()
        _po_others = [g for g in _po_girls if _po_gf is None or g.gid != _po_gf.gid]
        _po_f = _po_npc.gender == "female"
        _npf = dict(gender_fmt(_po_f), name=_po_name)

    $ Narration(_tl(_("%(name)s sways hard, %(poss)s eyes rolling shut. %(Pp)s slumps back, glass slipping from %(poss)s hand.")) % _npf)
    $ Character(_po_npc.Name, color=_po_npc.color)(_tl(renpy.random.choice([
        _("I'm... done... everything is..."),
        _("Can't... hold it... sorry..."),
        _("Room's spinning... I need to..."),
    ])))

    if _po_gf is not None:
        $ set_scene_expression(_po_gf, "worried")
        $ Say_Line(_po_gf, renpy.random.choice([
            _tl(_("%s?! Hey, are you okay?")) % _po_name,
            _tl(_("Oh no, %s! How much did you drink?!")) % _po_name,
            _tl(_("%(name)s! Can you hear me? ...%(Pp)s's out.")) % _npf,
        ]))

    $ Say_Player(renpy.random.choice([
        _tl(_("%(Pp)s's out cold. Let me move %(po)s to the couch.")) % _npf,
        _tl(_("Yep, %(pp)s's done for the night. I'll make sure %(pp)s's comfortable.")) % _npf,
        _tl(_("%(Pp)s's breathing fine, just had too much. I'll set %(po)s on the couch.")) % _npf,
    ]))

    python:
        for _pog in _po_others:
            Say_Line(_pog, _tl(renpy.random.choice([
                _("Should we stop? Is %(pp)s going to be okay?"),
                _("Wow, %(pp)s really could not handle %(poss)s drinks tonight."),
                _("At least %(pp)s went down happy."),
            ])) % _npf)

    if _po_gf is not None:
        $ set_scene_expression(_po_gf, "serious")
        $ Say_Line(_po_gf, renpy.random.choice([
            _tl(_("%(Pp)s does this sometimes. %(Pp)s'll be fine by morning.")) % _npf,
            _tl(_("%(Pp)s's a lightweight. Always has been. Let %(po)s sleep it off.")) % _npf,
            _tl(_("%(Pp)s'll be fine. Let's not let %(po)s ruin the fun.")) % _npf,
        ]))

    python:
        _po_npc.hide_sprite()
        store._npc_passed_out = True
        unlock_achievement("party_must_go_on")
        print("[NPC-PASSOUT] %s passed out at alcohol level %.1f" % (_po_name, get_drunk(_po_npc)))

    $ Narration(_tl(_("With %s sleeping it off on the couch, the rest of you decide to keep going.")) % _po_name)
    return


# ============================================================
# NPC PASS OUT EVENT (1 girl + NPC only)
# ============================================================
label _npc_pass_out_1girl_event:
    python:
        _po1_npc = store._h_npc
        _po1_name = _po1_npc.Name
        _po1_gf = _bf_get_gf(_po1_npc)
        _po1_girl = _po1_gf if _po1_gf else _hangout_girls_list()[0]
        _po1_f = _po1_npc.gender == "female"
        _npf = dict(gender_fmt(_po1_f), name=_po1_name)

    $ Narration(_tl(_("%(name)s sways dangerously and %(poss)s eyes glaze over. Before anyone can react, %(pp)s slumps sideways.")) % _npf)
    $ Character(_po1_npc.Name, color=_po1_npc.color)(_tl(renpy.random.choice([
        _("I can't... everything is... sorry..."),
        _("Too much... I'm out... goodnight..."),
    ])))

    $ set_scene_expression(_po1_girl, "worried")
    $ Say_Line(_po1_girl, renpy.random.choice([
        _tl(_("%s?! Oh no, not again...")) % _po1_name,
        _tl(_("Babe! Are you okay?! ...%(Pp)s's completely out.")) % _npf,
        _tl(_("%(name)s! ...%(Pp)s's gone.")) % _npf,
    ]))

    $ Say_Player(_tl(_("Let me move %(po)s to the couch. %(Pp)s'll be fine.")) % _npf)

    python:
        _po1_npc.hide_sprite()
        store._npc_passed_out = True
        unlock_achievement("party_must_go_on")
        print("[NPC-PASSOUT] %s (1-girl event) passed out at level %.1f" % (_po1_name, get_drunk(_po1_npc)))

    $ Narration(_tl(_("You set %(name)s up on the couch with a pillow. %(Pp)s's snoring within seconds.")) % _npf)

    python:
        _sa = getattr(_po1_girl, "Sex_acts", {}) or {}
        _po1_intimate = (
            _sa.get("bj", 0) > 0
            or _sa.get("hj", 0) > 0
            or _sa.get("sex", 0) > 0
            or _sa.get("tj", 0) > 0
            or _sa.get("anal", 0) > 0
        )

    if not _po1_intimate:
        $ set_scene_expression(_po1_girl, "worried")
        $ Say_Line(_po1_girl, renpy.random.choice([
            _tl(_("I should get %(po)s home. %(Pp)s's in bad shape.")) % _npf,
            _tl(_("I can't just leave %(po)s here... I should take %(po)s back.")) % _npf,
        ]))
        $ Say_Player(_tl(_("Yeah, that's probably best. Need help carrying %(po)s?")) % _npf)
        $ Say_Line(_po1_girl, _tl(renpy.random.choice([
            _("No, I got it. Thanks for having us over."),
            _("I'll manage. Thanks for tonight, it was fun while it lasted."),
        ])))
        $ Narration(_tl(_("She helps %(name)s up and heads out, supporting %(po)s on her shoulder.")) % _npf)
        $ Narration(_("Maybe next time, if you two are closer, the night won't end here."))
        $ store._secret_party_ended = True
        $ print("[NPC-PASSOUT-1G] Non-intimate path: setting _secret_party_ended=True, returning")
        return

    $ set_scene_expression(_po1_girl, "neutral")
    $ Say_Line(_po1_girl, renpy.random.choice([
        _("Well... I guess it is just us two now."),
        _("So much for a group hangout. It's just you and me."),
        _tl(_("%(Pp)s always does this. Guess we are on our own tonight.")) % _npf,
    ]))

    $ Say_Player(_tl(renpy.random.choice([
        _("Looks like it. Want to keep hanging out?"),
        _("We can still have a good time, right?"),
        _("More drinks for us, I guess."),
    ])))

    $ set_scene_expression(_po1_girl, "happy")
    $ Say_Line(_po1_girl, _tl(renpy.random.choice([
        _("Sure, why not? The night is still young."),
        _("Yeah, let's keep going. Might actually be more fun this way."),
        _("Alright. Pour me another."),
    ])))

    $ Narration(_("A few more drinks later, the room feels warmer. The snoring from the couch is the only background noise."))
    $ set_scene_expression(_po1_girl, "shy", blush=2)
    $ Say_Line(_po1_girl, _tl(renpy.random.choice([
        _("I think the drinks are getting to me..."),
        _("Okay, I'm definitely feeling it now..."),
    ])))
    $ Narration(_tl(_("She glances over at %s, snoring on the couch. Then back at you.")) % _po1_name)
    $ set_scene_expression(_po1_girl, "smirk", blush=2)
    $ Say_Line(_po1_girl, _tl(_("%(Pp)s's really out cold, huh?")) % _npf)
    $ Narration(_("She slides closer. Her hand lands on your thigh."))
    $ set_scene_expression(_po1_girl, "lusty", blush=2)
    $ Say_Line(_po1_girl, _tl(_("I've been wanting to do this all night...")))
    $ Narration(_("She slides off the couch and kneels in front of you."))

    # Launch restricted BJ scene (NPC asleep on couch — no tease/strip/record)
    python:
        store._scene_restricted = True
        store._interruption_happened = True
        store._witness_check_done = True
        session_cum_reset()
        _scene_exit_flags_reset()  # bypasses sex_menu; clear any leaked scene-exit flags before launch
        Player.Focus = 20
        print("[SECRET_PARTY] Launching BJ scene for %s" % _po1_girl.gid)

    call BJ_Launch(_po1_girl) from _call_secret_bj_launch
    call BJ_ControlMenu(_po1_girl) from _call_secret_bj_control
    call BJ_End(_po1_girl, dress_up=False) from _call_BJ_End_secret_bj
    python:
        store._scene_restricted = False
        store._player_exhausted = False
        store._interruption_happened = False
        store._witness_check_done = False
        _po1_cum_result = "none"
        if store._session_cum.get("mouth", 0) > 0:
            _po1_cum_result = "mouth"
        elif store._session_cum.get("face", 0) > 0:
            _po1_cum_result = "face"
        elif store._session_cum.get("outside", 0) > 0:
            _po1_cum_result = "outside"
        print("[SECRET_PARTY] BJ ended. Cum result: %s" % _po1_cum_result)

    # Restore hangout scene
    $ navigate_to("room", None)
    call Set_Scene(entry=False, show_chars=False, quiet=True) from _call_secret_restore_scene
    $ set_girl_sprite(_po1_girl.gid, pose="standing", at_list=[_hangout_pos_for(_po1_girl)])
    pause 0.3

    # Aftermath based on cum result
    if _po1_cum_result == "mouth":
        $ set_scene_expression(_po1_girl, "smug", blush=2)
        $ Say_Line(_po1_girl, _tl(_("Good thing %(pp)s's a heavy sleeper.")) % _npf)
    elif _po1_cum_result == "face":
        $ set_scene_expression(_po1_girl, "shy", blush=2)
        $ Say_Line(_po1_girl, _tl(_("You could have warned me... %(pp)s's RIGHT there.")) % _npf)
    elif _po1_cum_result == "outside":
        $ set_scene_expression(_po1_girl, "smirk", blush=1)
        $ Say_Line(_po1_girl, _tl(_("Close call. %(Pp)s almost woke up to THAT.")) % _npf)
    else:
        $ set_scene_expression(_po1_girl, "happy", blush=1)
        $ Say_Line(_po1_girl, _tl(_("Well... that happened.")))

    $ Narration(_tl(_("She fixes her hair and checks on %s. Still snoring.")) % _po1_name)
    $ set_scene_expression(_po1_girl, "happy", blush=1)
    $ Say_Line(_po1_girl, _tl(_("That... never happened. Right?")))
    $ Say_Player(_("What never happened?"))
    $ set_scene_expression(_po1_girl, "smirk")
    $ Say_Line(_po1_girl, _tl(_("Exactly.")))

    python:
        _po1_girl.RegisterAction("bj")
        Change_Status(_po1_girl, "Love", 10)
        Change_Status(_po1_girl, "Inbt", 8)
        mark_intimacy(_po1_girl, "bj")
    $ unlock_achievement("secret_party")

    # Escalation: if player has energy and girl is aroused, offer to keep going
    if Player.energy > 0 and _po1_girl.Lust > 0:
        $ set_scene_expression(_po1_girl, "lipbite", blush=2)
        $ Say_Line(_po1_girl, _tl(renpy.random.choice([
            _("That was... wow. But I'm not done yet."),
            _("Don't look at me like that. I can't help it, the alcohol is making me brave."),
        ])))
        $ Narration(_tl(_("She glances at %s on the couch. Still out cold.")) % _po1_name)
        $ set_scene_expression(_po1_girl, "lusty", blush=2)
        $ Say_Line(_po1_girl, _tl(_("%(Pp)s's not waking up anytime soon... want to keep going?")) % _npf)

        menu:
            "Keep going":
                $ set_scene_expression(_po1_girl, "smirk", blush=2)
                $ Say_Line(_po1_girl, _tl(_("Lock the door. Just in case.")))
                python:
                    store.door_locked = True
                    store._scene_restricted = True
                    print("[NPC_PASSOUT_ESCALATION] Entering sex_menu: restricted=%s energy=%d exhausted=%s" % (store._scene_restricted, Player.energy, store._player_exhausted))
                call sex_menu(_po1_girl, "room", store.TimeIndex) from _call_sex_menu_secret_party
                $ print("[NPC_PASSOUT_ESCALATION] sex_menu returned: restricted=%s energy=%d exhausted=%s" % (store._scene_restricted, Player.energy, store._player_exhausted))
                $ store._scene_restricted = False
                # Restore scene after sex_menu
                $ navigate_to("room", None)
                call Set_Scene(entry=False, show_chars=False, quiet=True) from _call_secret_restore_after_sex
                $ set_girl_sprite(_po1_girl.gid, pose="standing", at_list=[_hangout_pos_for(_po1_girl)])
                pause 0.3

            "That's enough for tonight":
                $ set_scene_expression(_po1_girl, "happy", blush=1)
                $ Say_Line(_po1_girl, _tl(_("Yeah... you're probably right.")))

    $ set_scene_expression(_po1_girl, "happy")
    $ Say_Line(_po1_girl, renpy.random.choice([
        _tl(_("I should get %(po)s home before %(pp)s wakes up. Goodnight.")) % _npf,
        _tl(_("I'll take %(po)s back. Tonight was... fun.")) % _npf,
    ]))
    $ Narration(_tl(_("She helps %(name)s up and heads out, leaving you alone with the silence.")) % _npf)
    $ store._secret_party_ended = True
    $ print("[NPC-PASSOUT-1G] Intimate path: setting _secret_party_ended=True, returning")
    return
