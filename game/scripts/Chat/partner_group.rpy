# ============================================================
# partner_group.rpy
# Actions for a phone GROUP that is "a girl + HER OWN partner NPC".
# The group + gray-out creation live in phone_messaging.rpy; this file
# holds the 3 group actions (Invite / Send Video) and their dialogue.
# (Hangout Night forks into hangout_night.rpy / the ToD engine.)
# ============================================================

init python:

    def _partner_npc_friend_key(npc):
        """Friendship tier of an NPC partner toward the player."""
        if npc is None:
            return "neutral"
        if hasattr(npc, "is_friendly") and npc.is_friendly():
            return "friendly"
        if hasattr(npc, "is_hostile") and npc.is_hostile():
            return "hostile"
        return "neutral"

    # NPC tags along when his/her girl accepts a HANGOUT invite (drinks at night).
    PARTNER_ACCOMPANY_NPC_LINES = {
        "friendly": [
            _("Of course we're coming! It'll be fun."),
            _("Count us in. Should be a good time."),
            _("Sure! I'm always down to hang out with you two."),
        ],
        "neutral": [
            _("Drinks at his place, huh? ...Fine. I'll come too."),
            _("If you're going, I'm going. Someone's gotta keep an eye on things."),
            _("His room for drinks... alright. I'll tag along, I guess."),
        ],
        "hostile": [
            _("Seriously? Him? ...Whatever. I'm not letting you go alone."),
            _("Him again? Ugh. Then I'm coming with you. End of discussion."),
            _("You really like hanging around this guy... I'm coming. Just so we're clear."),
        ],
    }

    # NPC response to a daytime INVITE (come hang out at a location, not drinks).
    PARTNER_INVITE_NPC_LINES = {
        "friendly": [
            _("Sounds good, I'll tag along!"),
            _("Sure, we'll head over. See you there."),
            _("Yeah, why not? Let's go, babe."),
        ],
        "neutral": [
            _("...Alright, I'll come too. Just to be safe."),
            _("If she's going, I'm going. Simple as that."),
            _("I guess I'll come along. Someone has to."),
        ],
        "hostile": [
            _("I'm not letting her go alone with you. I'll be there."),
            _("Wherever she goes, I go. Don't get any ideas."),
            _("Fine. But I'm watching you."),
        ],
    }

    # NPC is already at the same location as the player during a daytime INVITE.
    PARTNER_ALREADY_HERE_NPC_LINES = [
        _("I'm right here too, you know."),
        _("Already here. You didn't notice me?"),
        _("I was here before you even asked."),
    ]

    # The partner watches his girl accept a lewd dare in Truth or Dare.
    # Keyed by (trait, alcohol tier, NTR discovery state).
    _TOD_PARTNER_WATCH_LINES = {
        "ntr_open": [
            _("God... watching you like this, I can't even be mad. Keep going."),
            _("This is doing something to me. Don't stop on my account."),
            _("Everyone can see you're mine, and you're still doing it... I love it."),
        ],
        "ntr_hidden": [
            _("That was... I mean, it's just a game, right?"),
            _("I should be mad about this. Weird that I'm not."),
            _("Huh. I thought I'd hate this. I don't."),
        ],
        "proud_sober": [
            _("Are you serious right now?! With me sitting RIGHT here?!"),
            _("I can't believe you. In front of me? Have some respect."),
            _("That's it? You'll do that for a stupid game but not for me?"),
        ],
        "proud_drunk": [
            _("I can't believe this... but I'm too wasted to fight about it."),
            _("If I wasn't this drunk, we'd be having a serious talk right now."),
            _("Whatever. I'll deal with this when I'm sober."),
        ],
        "neutral_sober": [
            _("Seriously? Right in front of me? Over a stupid game?"),
            _("I don't care if it's a dare. That's my girlfriend."),
            _("This is NOT okay. I'm sitting right here and you're all acting like it's normal."),
        ],
        "neutral_tipsy": [
            _("I shouldn't be watching this... but I can't look away."),
            _("The drinks are making this less weird than it should be."),
            _("Okay, this is... a lot. I don't really know how to feel about it."),
        ],
        "neutral_drunk": [
            _("You know what? Do it. I'm too drunk to care."),
            _("This is... actually kind of hot? Did I just say that out loud?"),
            _("Whatever, it's just a game. I'm way too drunk to be upset."),
        ],
        "proud_sober_intense": [
            _("What the fuck?! What kind of dare is THAT?!"),
            _("Are you out of your mind?! She's NOT doing that!"),
            _("Over my dead body! That's way too far!"),
            _("No. Absolutely not. This game is OVER."),
        ],
        "neutral_sober_intense": [
            _("What the fuck? What kind of dare is that?"),
            _("Whoa, whoa, whoa. That's crossing a line."),
            _("Are you serious? That's way too much."),
            _("Hold on, that's not just a dare. That's too far."),
        ],
        "neutral_tipsy_intense": [
            _("Wait... that's... that's way too much, even for a game."),
            _("I know I've been drinking, but THAT is crossing a line."),
            _("Even drunk me knows that's too far. Come on."),
        ],
    }

    def _tod_partner_watch_line(npc, girl=None, dare_intensity=0):
        """NPC reaction to his girl accepting a lewd dare, scaled by alcohol,
        NTR discovery state, and dare intensity."""
        is_ntr = _npc_is_ntr(npc) if callable(globals().get("_npc_is_ntr")) else False
        npc_alc = get_drunk(npc) if callable(globals().get("get_drunk")) else 0
        ntr_disc = getattr(girl, "_ntr_boundary_discovered", False) if girl else False

        if is_ntr and ntr_disc:
            _k = "ntr_open"
        elif is_ntr:
            _k = "ntr_hidden"
        elif npc.has_trait("proud") if hasattr(npc, "has_trait") else False:
            if npc_alc >= 5:
                _k = "proud_drunk"
            elif dare_intensity >= 5:
                _k = "proud_sober_intense"
            else:
                _k = "proud_sober"
        elif npc_alc >= 9:
            _k = "neutral_drunk"
        elif npc_alc >= 5:
            if dare_intensity >= 5:
                _k = "neutral_tipsy_intense"
            else:
                _k = "neutral_tipsy"
        elif dare_intensity >= 5:
            _k = "neutral_sober_intense"
        else:
            _k = "neutral_sober"

        return renpy.random.choice(_TOD_PARTNER_WATCH_LINES[_k])

    # Scenario 3: NTR active + a broken/hostile NPC — the girl twists the knife,
    # reinforcing his humiliation as he watches her video.
    GROUP_DISSOLVE_BYSTANDER_LINES = [
        _("Oh..."),
        _("Wow... drama!"),
        _("Well that happened."),
        _("Yikes..."),
        _("I did NOT need to see this today."),
        _("...I'm just gonna pretend I didn't see that."),
    ]

    GROUP_DISSOLVE_GF_SAD_LINES = [
        _("I can't believe this..."),
        _("How could you do this to %(pp)s..."),
        _("This is so messed up..."),
        _("I feel sick..."),
    ]

    GROUP_DISSOLVE_GF_INDIFFERENT_LINES = [
        _("...I mean, I'm not even surprised."),
        _("Lol saw that coming."),
        _("%(Pp)s had it coming tbh."),
        _("Oof. Anyway."),
    ]

    def _group_dissolve_reactions(group, leaving_npc):
        """Build the full dissolution sequence: bystander + GF reactions,
        all members leave, group gets deleted."""
        _reactions = []
        _npc_gid = leaving_npc.gid
        _gf_gid = getattr(leaving_npc, "girl_gid", "")

        for _m_gid in group.get("members", []):
            if str(_m_gid).startswith("npc_") or _m_gid == _gf_gid:
                continue
            _reactions.append((_m_gid, _tl(renpy.random.choice(GROUP_DISSOLVE_BYSTANDER_LINES))))

        _gf = GIRL_BY_ID.get(_gf_gid)
        if _gf and _gf_gid in group.get("members", []):
            _is_cheater = getattr(_gf, "CheatAttitude", 1) >= 6
            _is_loyal = _gf.has_trait("loyal") if hasattr(_gf, "has_trait") else False
            if _is_cheater and not _is_loyal:
                _pool = GROUP_DISSOLVE_GF_INDIFFERENT_LINES
            else:
                _pool = GROUP_DISSOLVE_GF_SAD_LINES
            _line = _format_partner_line(_gf, _tl(renpy.random.choice(_pool)))
            _reactions.append((_gf_gid, _line))

        return _reactions

    PARTNER_VIDEO_GIRL_REINFORCE = [
        _("See how good it looks? He does things to me you never could, %(pl)s~"),
        _("That's the difference. With him I actually finish. You should take notes."),
        _("Don't look away now, %(pl)s. This is what a real man gets out of me."),
        _("I know you're watching. Good. Remember this is what you're missing~"),
    ]


# ============================================================
# ACTION 1 — Invite the girl + her partner to your current place
# ============================================================
label _partner_group_invite(group):
    python:
        _pnpc, _pgirl = _group_partner_and_girl(group)
    if _pgirl is None or _pnpc is None:
        $ phone_group_add_msg(group["id"], "system", _("This group is no longer valid."), "system")
        return

    python:
        _pi_loc = store.CurrentLocation
        _pi_loc_label = LOC_NAMES.get(_pi_loc, _pi_loc)
        _pi_msg = _tl(_("Hey, want to come hang out with me at %s? Bring %s too.")) % (_pi_loc_label, _pnpc.Name)
        phone_group_add_msg(group["id"], "player", _pi_msg, "text")
        _pi_here = (getattr(_pgirl, "loc", None) == _pi_loc)
        _pi_npc_here = (getattr(_pnpc, "loc", None) == _pi_loc)
        _pi_best = max(getattr(_pgirl, "Love", 0), getattr(_pgirl, "Inbt", 0))
        _pi_away = girl_is_away(_pgirl)   # at her parents' giving birth: she answers, she does not come
        _pi_accept = (not _pi_here) and (not _pi_away) and (_pi_best >= 200)

    # Girl replies first
    $ phone_group_add_msg(group["id"], _pgirl.gid, None, "typing")
    call screen phone_group_chat_screen(group, auto_close=renpy.random.uniform(0.8, 1.4))
    python:
        _g_msgs = phone_group_get_msgs(group["id"])
        if _g_msgs and _g_msgs[-1].get("type") == "typing":
            _g_msgs.pop()
        if _pi_here:
            _pi_girl_line = _tl(_("I'm already here, silly!"))
        elif _pi_accept:
            _pi_girl_line = _tl(renpy.random.choice(_PHONE_INVITE_ACCEPT))
        elif _pi_away:
            _pi_girl_line = _tl(renpy.random.choice(FOLLOW_INVITE_DECLINE["away"]))
        else:
            _pi_girl_line = _tl(renpy.random.choice(_PHONE_INVITE_DECLINE))
        phone_group_add_msg(group["id"], _pgirl.gid, _pi_girl_line, "text")
    call screen phone_group_chat_screen(group, auto_close=0.5)

    # NPC tags along only if she is coming (accept or already here)
    if _pi_accept or _pi_here:
        $ phone_group_add_msg(group["id"], _pnpc.gid, None, "typing")
        call screen phone_group_chat_screen(group, auto_close=renpy.random.uniform(0.9, 1.6))
        python:
            _g_msgs = phone_group_get_msgs(group["id"])
            if _g_msgs and _g_msgs[-1].get("type") == "typing":
                _g_msgs.pop()
            if _pi_npc_here:
                _pi_npc_line = _tl(renpy.random.choice(PARTNER_ALREADY_HERE_NPC_LINES))
            else:
                _pi_npc_raw = _tl(renpy.random.choice(PARTNER_INVITE_NPC_LINES[_partner_npc_friend_key(_pnpc)]))
                _pi_npc_line = _format_npc_line(_pnpc, _pi_npc_raw, _pgirl)
            phone_group_add_msg(group["id"], _pnpc.gid, _pi_npc_line, "text")
        call screen phone_group_chat_screen(group, auto_close=0.5)

    # Move to the location and update sprites
    python:
        _pi_moved = False
        if _pi_accept:
            _pgirl.loc = _pi_loc
            _pi_moved = True
        if (_pi_accept or _pi_here) and not _pi_npc_here:
            _pnpc.loc = _pi_loc
            _pi_moved = True
        if _pi_moved:
            if _pi_here and not _pi_npc_here:
                phone_group_add_msg(group["id"], "system", _tl(_("%s is on the way.")) % _pnpc.Name, "system")
            elif _pi_accept:
                phone_group_add_msg(group["id"], "system", _tl(_("%s and %s are on their way.")) % (_pgirl.Name, _pnpc.Name), "system")
            _girls_now = [_g for _g in ALL_GIRLS if _g.loc == _pi_loc]
            build_location_roster(_girls_now, _pnpc)
            _sprite_suppressed.discard(_pgirl.Id)
            show_roster_sprites()
            if not hasattr(store, "_phone_girls_arrived"):
                store._phone_girls_arrived = []
            store._phone_girls_arrived.append(_pgirl.gid)
    if _pi_moved:
        call screen phone_group_chat_screen(group, auto_close=0.5)

    return


# ============================================================
# ACTION 2 — Send a recorded video (of THIS girl only) to the group.
# The NPC reacts (reusing the full NPC video-reaction machinery) and the
# girl reacts (reusing the group reaction, incl. face-hidden + Obed). A
# breakup/violation dissolves the group ("NPC left the group").
# ============================================================
label _partner_group_send_video(group):
    python:
        _pnpc, _pgirl = _group_partner_and_girl(group)
    if _pgirl is None or _pnpc is None:
        $ phone_group_add_msg(group["id"], "system", _("This group is no longer valid."), "system")
        return
    python:
        store._pv_girl_gid = _pgirl.gid
        store._pv_vids = [v for v in getattr(store.Player, "recorded_videos", []) if v.get("girl_gid") == store._pv_girl_gid]
        print("[PARTNER_VIDEO] girl=%s vids=%d" % (store._pv_girl_gid, len(store._pv_vids)))
    if not store._pv_vids:
        $ phone_group_add_msg(group["id"], "system", _tl(_("You don't have any recorded videos of %s.")) % _pgirl.Name, "system")
        return

    # Pick position (split by consent/face_hidden)
    python:
        _pv_combos = set()
        for _cv in store._pv_vids:
            if _cv.get("special"):
                continue
            _var = "nc" if not _cv.get("consensual", True) else ("h" if _cv.get("face_hidden", True) else "v")
            _pv_combos.add((_cv["type"], _var))
        _pv_combos = sorted(_pv_combos)
        _pv_pos_choices = []
        for _pos, _var in _pv_combos:
            _lbl = _pk_t(VIDEO_TYPE_DISPLAY.get(_pos, _pos.replace("_", " ").title()))
            if _var == "nc":
                _lbl += " {size=18}(" + _tl(_("non-consensual")) + "){/size}"
            elif _var == "h":
                _lbl += " {size=18}(" + _tl(_("hidden face")) + "){/size}"
            else:
                _lbl += " {size=18}(" + _("face visible") + "){/size}"
            _pv_pos_choices.append((_lbl, _pos + "|" + _var))
        if any(v.get("special") for v in store._pv_vids):
            _pv_pos_choices.append((_("SPECIAL"), "special"))
        print("[PARTNER_VIDEO] combos=%s choices=%d" % (str(_pv_combos), len(_pv_pos_choices)))
    call screen phone_group_chat_screen(group, choices=_pv_pos_choices)
    $ store._pv_choice = _return
    if store._pv_choice in ("home", "close", None):
        return
    python:
        store._pv_pos = store._pv_choice
        store._pv_fh = None
        store._pv_nc = False
        if "|" in str(store._pv_choice):
            _pp = str(store._pv_choice).split("|")
            store._pv_pos = _pp[0]
            if _pp[1] == "nc":
                store._pv_nc = True
            elif _pp[1] == "h":
                store._pv_fh = True
            else:
                store._pv_fh = False
        print("[PARTNER_VIDEO] parsed pos=%s fh=%s nc=%s" % (store._pv_pos, store._pv_fh, store._pv_nc))

    # Re-fetch videos (safe across call screen boundaries) and filter
    python:
        store._pv_vids = [v for v in getattr(store.Player, "recorded_videos", []) if v.get("girl_gid") == store._pv_girl_gid]
        if store._pv_pos == "special":
            store._pv_match = [v for v in store._pv_vids if v.get("special")]
        elif store._pv_nc:
            store._pv_match = [v for v in store._pv_vids if v["type"] == store._pv_pos and not v.get("special") and not v.get("consensual", True)]
        else:
            store._pv_match = [v for v in store._pv_vids if v["type"] == store._pv_pos and not v.get("special") and v.get("consensual", True)]
            if store._pv_fh is not None:
                store._pv_match = [v for v in store._pv_match if v.get("face_hidden", True) == store._pv_fh]
        store._pv_locs = sorted(set(v.get("location", "unknown") for v in store._pv_match))
        print("[PARTNER_VIDEO] match=%d locs=%s" % (len(store._pv_match), str(store._pv_locs)))
    if len(store._pv_locs) > 1:
        python:
            _pv_loc_choices = [(l.replace("_", " ").title(), l) for l in store._pv_locs]
        call screen phone_group_chat_screen(group, choices=_pv_loc_choices)
        $ store._pv_loc = _return
        if store._pv_loc in ("home", "close", None):
            return
    else:
        $ store._pv_loc = store._pv_locs[0] if store._pv_locs else None

    python:
        store._pv_sent = None
        for _v in reversed(store._pv_match):
            if _v.get("location", "unknown") == store._pv_loc:
                store._pv_sent = _v
                break
        if store._pv_sent is None and store._pv_match:
            store._pv_sent = store._pv_match[-1]
        print("[PARTNER_VIDEO] loc=%s sent=%s" % (store._pv_loc, "YES" if store._pv_sent else "NONE"))
    if store._pv_sent is None:
        $ phone_group_add_msg(group["id"], "system", _("Could not find that video."), "system")
        return

    # Player posts the video into the group
    python:
        _pv_type_lbl = _pk_t(VIDEO_TYPE_DISPLAY.get(store._pv_sent["type"], store._pv_sent["type"]))
        phone_group_add_msg(group["id"], "player", _tl(_("[[Sent a video: %s]")) % _pv_type_lbl, "text")
    call screen phone_group_chat_screen(group, auto_close=0.6)

    # Build the reactions: girl reacts, NPC reacts (with side effects), and in
    # the hostile-NTR case the girl reinforces his humiliation.
    python:
        _pv_reactions = []
        store._phone_msg_queue = []
        _phone_mode_on(_pgirl)
        try:
            group_video_reaction(_pgirl, store._pv_sent, group)
        finally:
            _phone_mode_off()
        for _qm in store._phone_msg_queue:
            _pv_reactions.append((_qm.get("sender", _pgirl.gid), _qm["text"]))
        store._phone_msg_queue = []

        _pv_girl_reads = not girl_is_away(_pgirl)   # away (giving birth): she is not reading the group
        _pv_npc_line = _npc_video_reaction(_pnpc, store._pv_sent, girl_present=_pv_girl_reads)   # girl + partner group: she is here
        if _pv_npc_line:
            _pv_reactions.append((_pnpc.gid, _pv_npc_line))

        if _pv_girl_reads and getattr(_pnpc, "_ntr_active", False) and hasattr(_pnpc, "is_hostile") and _pnpc.is_hostile():
            _gf_will_taunt = getattr(_pgirl, "CheatAttitude", 1) >= 6 or (hasattr(_pgirl, "has_trait") and _pgirl.has_trait("cheater"))
            _gf_is_loyal = hasattr(_pgirl, "has_trait") and _pgirl.has_trait("loyal")
            if _gf_will_taunt and not _gf_is_loyal:
                _pv_reinforce = _format_partner_line(_pgirl, _tl(renpy.random.choice(PARTNER_VIDEO_GIRL_REINFORCE)))
                _pv_reactions.append((_pgirl.gid, _pv_reinforce))

    # Replay each reaction with a typing indicator
    $ _pv_ri = 0
    while _pv_ri < len(_pv_reactions):
        $ _pvr_gid, _pvr_text = _pv_reactions[_pv_ri]
        if not _phone_ctrl_held():
            $ phone_group_add_msg(group["id"], _pvr_gid, None, "typing")
            call screen phone_group_chat_screen(group, auto_close=renpy.random.uniform(1.2, 2.0))
            python:
                _g_msgs = phone_group_get_msgs(group["id"])
                if _g_msgs and _g_msgs[-1].get("type") == "typing":
                    _g_msgs.pop()
        python:
            phone_group_add_msg(group["id"], _pvr_gid, _pvr_text, "text")
            _pv_ri += 1
        if not _phone_ctrl_held():
            call screen phone_group_chat_screen(group, auto_close=0.5)

    # Did the NPC's reaction trigger a breakup / boundary violation? Dissolve the group.
    python:
        _pv_dissolve = getattr(_pgirl, "_npc_video_pending", False) or getattr(_pgirl, "_ntr_violation_pending", False)
    if _pv_dissolve:
        # Bystander + GF reactions before everyone leaves
        python:
            _dissolve_reactions = _group_dissolve_reactions(group, _pnpc)
        $ _dr_i = 0
        while _dr_i < len(_dissolve_reactions):
            $ _dr_gid, _dr_text = _dissolve_reactions[_dr_i]
            if not _phone_ctrl_held():
                $ phone_group_add_msg(group["id"], _dr_gid, None, "typing")
                call screen phone_group_chat_screen(group, auto_close=renpy.random.uniform(1.0, 1.8))
                python:
                    _g_msgs = phone_group_get_msgs(group["id"])
                    if _g_msgs and _g_msgs[-1].get("type") == "typing":
                        _g_msgs.pop()
            python:
                phone_group_add_msg(group["id"], _dr_gid, _dr_text, "text")
                _dr_i += 1
            if not _phone_ctrl_held():
                call screen phone_group_chat_screen(group, auto_close=0.5)

        # NPC leaves
        $ phone_group_add_msg(group["id"], "system", _tl(_("%s left the group.")) % _pnpc.Name, "system")
        if not _phone_ctrl_held():
            call screen phone_group_chat_screen(group, auto_close=0.8)

        # All other members leave and group is deleted
        python:
            _pgirl._partner_confront_pending = True
            for _lv_gid in list(group.get("members", [])):
                if str(_lv_gid).startswith("npc_"):
                    continue
                _lv_girl = GIRL_BY_ID.get(_lv_gid)
                if _lv_girl:
                    phone_group_add_msg(group["id"], "system", _tl(_("%s left the group.")) % _lv_girl.Name, "system")
        call screen phone_group_chat_screen(group)
        python:
            _pgs = getattr(store.Player, "phone_groups", [])
            store.Player.phone_groups = [g for g in _pgs if g.get("id") != group["id"]]
            store._partner_group_dissolved = True
    return


# ============================================================
# ACTION 3 — Hangout Night with the girl + her partner present.
# The girl decides first; the NPC tags along by friendship. Schedules a
# hangout with girl_a = the girl, girl_b = None, and _hangout_partner_npc set.
# ============================================================
label hangout_send_invite_partner(group):
    python:
        store._php_npc, store._php_girl = _group_partner_and_girl(group)
        print("[HANGOUT_PARTNER] npc=%s girl=%s" % (
            getattr(store._php_npc, "name", None), getattr(store._php_girl, "gid", None)))
    if store._php_girl is None or store._php_npc is None:
        $ phone_group_add_msg(group["id"], "system", _("This group is no longer valid."), "system")
        return

    # Check which drinks the player owns
    python:
        _php_owned = player_owned_drinks()
        print("[HANGOUT_PARTNER] owned drinks=%s" % str(_php_owned))
        if len(_php_owned) <= 1:
            store._php_bottle = _php_owned[0][0] if _php_owned else None
        else:
            store._php_bottle = None
            store._php_bottle_choices = []
            for _bid, _bcnt in _php_owned:
                _binfo = drink_info(_bid)
                _blbl = _tr(_binfo["label"]) if _binfo else _tr("Drinks")
                store._php_bottle_choices.append((_tl(_("Bring %s")) % _blbl, _bid))

    # If multiple drinks, let the player pick
    if getattr(store, "_php_bottle_choices", None):
        call screen phone_group_chat_screen(group, choices=store._php_bottle_choices)
        $ store._php_bottle = _return
        $ store._php_bottle_choices = None

    # Send the invite with the selected bottle
    python:
        store._hangout_brought_drink = store._php_bottle
        _php_bring = drink_bring_phrase(store._php_bottle) if store._php_bottle else _tl(_("some drinks"))
        phone_group_add_msg(group["id"], "player",
            _tl(_("Hey, come to my room tonight for some drinks? Bring %s along, I brought %s.")) % (store._php_npc.Name, _php_bring),
            "text")
        player_consume_drink(store._php_bottle)
        store._hangout_scheduled_day = store.Day
        print("[HANGOUT_PARTNER] bottle=%s day=%d" % (store._php_bottle, store.Day))
    call screen phone_group_chat_screen(group, auto_close=0.6)

    # The girl decides first
    $ phone_group_add_msg(group["id"], store._php_girl.gid, None, "typing")
    call screen phone_group_chat_screen(group, auto_close=renpy.random.uniform(1.0, 1.8))
    python:
        _g_msgs = phone_group_get_msgs(group["id"])
        if _g_msgs and _g_msgs[-1].get("type") == "typing":
            _g_msgs.pop()
        store._php_accepts = hangout_girl_accepts(store._php_girl, None, store._php_bottle)
        if store._php_accepts:
            _php_girl_line = _tl(renpy.random.choice([
                _("Sounds fun! We'll be there."),
                _("Ooh, drinks? Count us in!"),
                _("Sure, why not? Could be a fun night."),
            ]))
        elif girl_is_away(store._php_girl):   # hangout_girl_accepts already said no: she is at her parents'
            _php_girl_line = _tl(renpy.random.choice(FOLLOW_INVITE_DECLINE["away"]))
        elif getattr(store._php_girl, "_pregnant", False) and getattr(store._php_girl, "_pregnancy_known", False):
            # pregnant and she knows it (hangout_girl_accepts already said no): no alcohol for her,
            # and she says so (rod_pick_line comes back translated: no _tl here)
            _php_girl_line = rod_pick_line(store._php_girl, "hangout_pregnant")
        else:
            _php_girl_line = _tl(renpy.random.choice([
                _("Hmm, I don't think we can make it tonight. Sorry."),
                _("We're not really up for it tonight. Another time?"),
                _("We'll sit this one out. Have a good night!"),
            ]))
        phone_group_add_msg(group["id"], store._php_girl.gid, _php_girl_line, "text")
        print("[HANGOUT_PARTNER] girl accepts=%s" % store._php_accepts)
    call screen phone_group_chat_screen(group, auto_close=0.5)

    # NPC tags along only if she accepted; speaks by friendship
    if store._php_accepts:
        $ phone_group_add_msg(group["id"], store._php_npc.gid, None, "typing")
        call screen phone_group_chat_screen(group, auto_close=renpy.random.uniform(0.9, 1.6))
        python:
            _g_msgs = phone_group_get_msgs(group["id"])
            if _g_msgs and _g_msgs[-1].get("type") == "typing":
                _g_msgs.pop()
            _php_npc_raw = _tl(renpy.random.choice(PARTNER_ACCOMPANY_NPC_LINES[_partner_npc_friend_key(store._php_npc)]))
            phone_group_add_msg(group["id"], store._php_npc.gid, _format_npc_line(store._php_npc, _php_npc_raw, store._php_girl), "text")
        call screen phone_group_chat_screen(group, auto_close=0.5)

    # Schedule or refund
    python:
        if store._php_accepts:
            store._hangout_group_id = group["id"]
            store._hangout_members = [store._php_girl.gid]
            store._hangout_girls = [store._php_girl]
            _sync_hangout_girl_aliases()
            store._hangout_partner_npc = store._php_npc
            store._hangout_partner_npc_id = getattr(store._php_npc, "partner_id", None)
            phone_group_add_msg(group["id"], "player", _("Awesome, see you tonight!"), "text")
            phone_group_add_msg(group["id"], "system", _("Hangout scheduled for tonight!"), "system")
            print("[HANGOUT_PARTNER] scheduled: girl=%s npc=%s" % (store._php_girl.gid, store._php_npc.name))
        else:
            if store._php_bottle:
                store.Player.add_item(store._php_bottle, 1)
            else:
                store.Player.add_item("drinks", 1)
            print("[HANGOUT_PARTNER] declined, bottle refunded")
    call screen phone_group_chat_screen(group, auto_close=0.8)
    return
